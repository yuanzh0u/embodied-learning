"""Cross-process, cross-machine locks for the shared knowledge base.

The KB may live on a CIFS mount shared by several machines, and one machine
may run several processes against the same root (multiple terminals, multiple
wiki servers on different ports). ``fcntl.flock`` is machine-local and not
reliable across CIFS clients, so every primitive here rests on the one thing a
SMB server does guarantee: exclusive creation of a path (``O_CREAT|O_EXCL``).

Layout under the caller-supplied root (never guessed inside this module)::

    <root>/.locks/<name>.lock                  # owner-record JSON while held
    <root>/.locks/<name>.lock.steal-<uuid>     # transient steal markers
    <root>/.claims/<name>.json                 # long-lived reservations

Locks are advisory, like all file locks: a process running older code simply
ignores them and behavior degrades to the unlocked present, never worse.

Usage::

    from .. import locks

    with locks.kb_lock(kb_root, "pool-index"):
        entries = read_index(); entries.append(...); write_index(entries)

    if locks.claim(kb_root, f"event-prefix/{prefix}", payload):
        ...  # we own the prefix until release_claim / forever

Design notes:

- Waiting is a poll loop over ``O_EXCL`` attempts. A waiter that sees an
  existing lock reads the owner record and prints a one-line progress message
  at most every ``PROGRESS_EVERY`` seconds; expiry raises LockTimeout with the
  owner record and remediation in the message.
- Stale locks (crashed holder) are stolen via a claim-then-verify dance: the
  waiter creates ``.steal-<uuid>`` with O_EXCL (losers keep polling), the
  winner unlinks the old lock, sweeps stale steal markers, and re-enters the
  normal acquire loop. Because "stale" is judged from wall-clock timestamps, a
  live holder can in principle be stolen from; that is recoverable because
  release only unlinks when the record's ``claim_id`` still matches ours —
  the victim's release becomes a no-op instead of deleting the new owner's
  lock. Defaults are deliberately generous (stale 900 s) to keep this rare.
- Reentrancy is handled per process with a registry keyed by lock path: the
  same thread re-entering the same lock increments a depth counter instead of
  deadlocking on itself; a second thread of the same process still serializes
  on the registry's RLock before touching the file.
- ``claim``/``release_claim`` use the same O_EXCL create with the steal dance
  for TTL takeover. Claims under ``.claims/`` are reservations (event-ID
  prefixes), not locks: nothing garbage-collects them.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

LOCKS_DIRNAME = ".locks"
CLAIMS_DIRNAME = ".claims"
STEAL_SUFFIX = ".steal-"
STEAL_MARKER_MAX_AGE = 60.0
# Upper bound for reclaiming a lock whose owner record stays unreadable
# (0-byte leftover / corrupt content / client-side ghost dentry): live holders
# write the record within milliseconds of O_EXCL creation, so 60s is generous.
UNREADABLE_STEAL_GRACE = 60.0
# Consecutive polls with an unreadable/absent owner record after EEXIST: a
# live holder writes its record within milliseconds, so a streak this long
# means the EEXIST is a cache lie (ghost dentry variants) or a leftover —
# unlink to drop the cached entry and retry.
UNREADABLE_STREAK_LIMIT = 3
PROGRESS_EVERY = 10.0

DEFAULT_WAIT = 120.0
DEFAULT_STALE = 900.0
DEFAULT_POLL = 1.0


class LockBusy(RuntimeError):
    """Raised by ``fail_fast=True`` when the lock is held by someone else."""


class LockTimeout(RuntimeError):
    """Raised when the bounded wait expired without acquiring the lock."""


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        parsed = float(raw)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def locks_disabled() -> bool:
    """Emergency escape hatch: EMBODIED_KB_LOCKS_DISABLED=1 no-ops everything."""

    return os.environ.get("EMBODIED_KB_LOCKS_DISABLED", "") == "1"


def locks_dir(root: Path | str) -> Path:
    """Directory holding lock files for ``root`` (env-overridable for tests)."""

    override = os.environ.get("EMBODIED_KB_LOCK_DIR")
    if override:
        return Path(override).expanduser()
    return Path(root) / LOCKS_DIRNAME


def lock_path(root: Path | str, name: str) -> Path:
    return locks_dir(root) / f"{name}.lock"


def claims_dir(root: Path | str) -> Path:
    return Path(root) / CLAIMS_DIRNAME


def _owner_record(name: str, detail: str) -> dict[str, object]:
    now = time.time()
    return {
        "name": name,
        "host": socket.gethostname(),
        "pid": os.getpid(),
        "ts": now,
        "ts_iso": datetime.fromtimestamp(now, tz=timezone.utc).isoformat(),
        "cmd": " ".join(sys.argv[:4]),
        "detail": detail,
        "claim_id": uuid.uuid4().hex,
    }


def read_owner(lock_file: Path | str) -> dict[str, object] | None:
    """Parse a lock file's owner record; None when absent or unreadable."""

    try:
        payload = json.loads(Path(lock_file).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _format_owner(record: dict[str, object] | None) -> str:
    if not record:
        return "未知持有者"
    held = ""
    ts = record.get("ts")
    if isinstance(ts, (int, float)):
        held = f"，已持有 {max(0.0, time.time() - float(ts)):.0f}s"
    cmd = str(record.get("cmd") or "")
    return (
        f"{record.get('host', '?')}/{record.get('pid', '?')}{held}"
        + (f"（{cmd}）" if cmd else "")
    )


def _record_age(record: dict[str, object] | None, lock_file: Path) -> float:
    if record and isinstance(record.get("ts"), (int, float)):
        return max(0.0, time.time() - float(record["ts"]))
    try:
        return max(0.0, time.time() - lock_file.stat().st_mtime)
    except OSError:
        return 0.0


def _unreadable_grace(wait: float, stale: float, poll: float) -> float:
    """How long an unreadable owner record may block a waiter before it is
    treated as a leftover.

    Bounded by the caller's own patience: a grace longer than ``wait`` would
    make the waiter time out BEFORE the reclaim can ever fire (the exact trap
    that hit wiki-publish wait=600 vs stale=1800 and chat-sessions wait=30 vs
    grace=60). Floor of two polls protects a live holder's record-write
    window; cap of UNREADABLE_STEAL_GRACE protects against clock skew."""
    return max(2.0 * poll, min(wait, stale, UNREADABLE_STEAL_GRACE))


def _is_ghost_dentry(path: Path) -> bool:
    """True when ``path`` exists only as a client-cached dying inode.

    Flaky NAS/SMB clients keep a deleted file's dentry cached: ``stat``
    succeeds (with ``st_nlink == 0`` — impossible for any real file, POSIX
    guarantees nlink >= 1 while a path reaches the inode), reads return
    ENOENT, and — the killer — ``O_CREAT|O_EXCL`` gets its EEXIST answered
    from that cache without ever reaching the server. A waiter locked out by
    such a ghost must unlink the path once (server answers ENOENT, the
    client drops the dentry) and retry; waiting never helps.
    """

    try:
        return path.stat().st_nlink == 0
    except OSError:
        return False


def _holder_dead_locally(record: dict[str, object] | None) -> bool:
    """True when the holder is provably gone: same-host record whose pid no
    longer exists on this machine. Cross-machine holders can't be probed, so
    they still age out via the stale TTL. A reused pid could mask a dead
    holder as alive — harmless, the TTL reclaims it later."""

    if not record:
        return False
    host, pid = record.get("host"), record.get("pid")
    if not isinstance(host, str) or host != socket.gethostname():
        return False
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return True  # pid gone: holder crashed without releasing
    except PermissionError:
        return False  # pid alive, owned by another user
    except OSError:
        return False
    return False


def _try_steal(lock_file: Path) -> bool:
    """Claim the right to steal ``lock_file``; True means we won the race.

    All waiters contend on one fixed marker path (``<lock>.steal``), so only
    one of them proceeds to unlink the stale lock; the others see the fresh
    marker and keep polling. A leftover marker older than
    ``STEAL_MARKER_MAX_AGE`` is itself replaceable (its creator died).
    """

    marker = lock_file.with_name(lock_file.name + STEAL_SUFFIX)
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        os.close(fd)
    except FileExistsError:
        try:
            if time.time() - marker.stat().st_mtime <= STEAL_MARKER_MAX_AGE:
                return False
            marker.unlink()
        except OSError:
            return False
        return _try_steal(lock_file)
    except OSError:
        return False
    try:
        os.unlink(lock_file)  # safe: the O_EXCL marker, not the unlink, gates the race
    except OSError:
        pass
    try:
        marker.unlink()
    except OSError:
        pass
    return True


class _Entry:
    __slots__ = ("lock", "depth", "claim_id")

    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.depth = 0
        self.claim_id: str | None = None


_REGISTRY: dict[str, _Entry] = {}
_REGISTRY_GUARD = threading.Lock()


def _enter_registry(key: str, deadline: float | None, poll: float, *, fail_fast: bool) -> _Entry:
    """Take this thread's turn on the entry for ``key`` (reentrancy-aware).

    The per-entry RLock is only ever taken non-blocking and polled with the
    same deadline as the file lock — a second thread of this process must hit
    the caller's ``wait`` bound, not block unbounded behind the holder. All of
    this happens under ``_REGISTRY_GUARD``, so an acquired entry cannot be
    popped underneath us.
    """

    while True:
        with _REGISTRY_GUARD:
            entry = _REGISTRY.get(key)
            if entry is None:
                entry = _Entry()
                _REGISTRY[key] = entry
            if entry.lock.acquire(blocking=False):
                entry.depth += 1
                return entry
        if deadline is None or time.monotonic() >= deadline:
            if fail_fast:
                raise LockBusy(
                    f"锁 {key} 正被同进程另一线程持有（pid {os.getpid()}）；"
                    f"请确认没有重复启动"
                )
            raise LockTimeout(
                f"等待锁 {key} 超过等待上限（同进程另一线程正在持有）；"
                f"确认没有并发驱动同一资源后重试"
            )
        time.sleep(poll)


def _exit_registry(key: str, entry: _Entry) -> bool:
    """Drop one depth level; True when the file lock must be released."""

    with _REGISTRY_GUARD:
        entry.depth -= 1
        last = entry.depth == 0
        if last and _REGISTRY.get(key) is entry:
            _REGISTRY.pop(key, None)
    if last:
        entry.lock.release()
    return last


def _acquire_file_lock(lock_file: Path, record: dict[str, object]) -> None:
    payload = json.dumps(record, ensure_ascii=False)
    fd = os.open(lock_file, os.O_WRONLY | os.O_TRUNC, 0o644)
    try:
        os.write(fd, payload.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)


@contextmanager
def kb_lock(
    root: Path | str,
    name: str,
    *,
    wait: float | None = None,
    stale: float | None = None,
    poll: float | None = None,
    fail_fast: bool = False,
    detail: str = "",
):
    """Hold an exclusive lock named ``name`` under ``<root>/.locks/``.

    ``wait`` bounds the total blocking wait (default 120 s); expiry raises
    :class:`LockTimeout`. ``fail_fast=True`` makes a single non-blocking
    attempt and raises :class:`LockBusy` instead — for whole-run driver locks
    where waiting would only duplicate a running pipeline. ``stale`` is the
    age after which a crashed holder's lock may be stolen.
    """

    if locks_disabled():
        print(f"[kb-lock] 已禁用（EMBODIED_KB_LOCKS_DISABLED=1），跳过锁 {name}", file=sys.stderr)
        yield
        return

    wait = DEFAULT_WAIT if wait is None else float(wait)
    stale = DEFAULT_STALE if stale is None else float(stale)
    poll = DEFAULT_POLL if poll is None else float(poll)
    target = lock_path(root, name)
    key = str(target)

    deadline = None if fail_fast else time.monotonic() + wait
    entry = _enter_registry(key, deadline, poll, fail_fast=fail_fast)
    try:
        if entry.depth == 1:
            _acquire(target, name, deadline, wait, stale, poll, fail_fast, detail, entry)
        yield
    finally:
        if _exit_registry(key, entry):
            _release(target, entry)


def _acquire(
    target: Path,
    name: str,
    deadline: float | None,
    wait: float,
    stale: float,
    poll: float,
    fail_fast: bool,
    detail: str,
    entry: _Entry,
) -> None:
    last_progress = 0.0
    unreadable_streak = 0
    while True:
        target.parent.mkdir(parents=True, exist_ok=True)
        record = _owner_record(name, detail)
        try:
            fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            pass
        except OSError as exc:  # e.g. read-only share: degrade loudly, do not block
            raise LockTimeout(f"锁 {target} 无法创建：{exc}") from exc
        else:
            _acquire_file_lock(target, record)
            entry.claim_id = str(record["claim_id"])
            return

        holder = read_owner(target)
        if holder is None:
            unreadable_streak += 1
            # Ghost dentry first: nothing else can unblock it (the EEXIST is
            # cache-answered, so retrying or waiting never reaches the
            # server). st_nlink==0 is the definitive dying-inode marker, but
            # flaky NAS clients lie in more shapes — stat may say ENOENT or
            # report nlink=1 for an entry that cannot be opened — so after a
            # short streak of unreadable records, unlink unconditionally: it
            # drops whichever cached state is blocking the create, and a live
            # holder (record written within ms) never accumulates the streak.
            if _is_ghost_dentry(target) or unreadable_streak >= UNREADABLE_STREAK_LIMIT:
                target.unlink(missing_ok=True)  # server may say ENOENT; that's the point
                unreadable_streak = 0
                print(f"[kb-lock] 清除 {name} 的客户端缓存幽灵 dentry，重试", file=sys.stderr)
                continue
        else:
            unreadable_streak = 0
        # Third steal path: the owner record is unreadable (0-byte leftover
        # from a crash between create and record-write, or corrupt content).
        # The grace is bounded by the caller's own wait so the reclaim always
        # fires before a timeout; its unlink attempt also clears ghost
        # dentries, which is what actually un-blocks the next O_EXCL create.
        if holder is None and _record_age(holder, target) > _unreadable_grace(wait, stale, poll):
            if _try_steal(target):
                print(f"[kb-lock] 锁 {name} 的持有者记录不可读（空/损坏/客户端缓存幽灵），判定遗留，已抢占", file=sys.stderr)
                continue
        # Same-host holder provably dead → steal immediately, regardless of
        # wait/stale (a crashed driver's run-lock must not block its own
        # rerun for the full TTL). Cross-machine holders still age out.
        if _holder_dead_locally(holder):
            if _try_steal(target):
                print(
                    f"[kb-lock] 锁 {name} 的持有进程（{_format_owner(holder)}）已退出，判定遗留，已抢占",
                    file=sys.stderr,
                )
                continue
        elif _record_age(holder, target) > stale and _try_steal(target):
            print(f"[kb-lock] 锁 {name} 疑似遗留（超过 {stale:.0f}s），已抢占", file=sys.stderr)
            continue
        if fail_fast:
            raise LockBusy(
                f"锁 {target} 已被占用（{_format_owner(holder)}）；请确认没有重复启动，"
                f"确认原进程已结束后可删除该锁文件重试"
            )

        now = time.monotonic()
        if deadline is not None and now >= deadline:
            waited = f"{wait:.0f}s" if wait else "等待窗口"
            raise LockTimeout(
                f"等待锁 {target} 超过 {waited}（{_format_owner(holder)}）；"
                f"确认持有进程已退出后删除该锁文件，或调大 EMBODIED_KB_LOCK_STALE"
            )
        if now - last_progress >= PROGRESS_EVERY:
            print(f"[kb-lock] 等待共享锁 {name}（{_format_owner(holder)}）…", file=sys.stderr)
            last_progress = now
        time.sleep(poll)


def _release(target: Path, entry: _Entry) -> None:
    if not entry.claim_id:
        # Never acquired (e.g. LockTimeout/LockBusy propagating through the
        # finally block) — must not unlink someone else's live lock.
        return
    try:
        holder = read_owner(target)
    except OSError:
        return
    # Only unlink while we are still the recorded owner: a stale-steal may have
    # handed the lock to someone else while we were still working.
    if holder and entry.claim_id and holder.get("claim_id") != entry.claim_id:
        return
    try:
        target.unlink()
    except OSError:
        pass
    entry.claim_id = None


def claim(root: Path | str, name: str, payload: dict[str, object], *, ttl: float | None = None) -> bool:
    """Reserve ``name`` under ``<root>/.claims/`` via O_EXCL creation.

    Returns True when this process now owns the claim. With ``ttl`` set, an
    older claim may be taken over through the same steal-marker dance. The
    claim file is permanent (a reservation, not a lock) unless explicitly
    released.
    """

    if locks_disabled():
        return True
    target = claims_dir(root) / f"{name}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    record = dict(payload)
    record.setdefault("claim_id", uuid.uuid4().hex)
    record.setdefault("host", socket.gethostname())
    record.setdefault("ts", time.time())
    while True:
        try:
            fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            pass
        except OSError as exc:
            raise LockTimeout(f"预留 {target} 无法创建：{exc}") from exc
        else:
            os.write(fd, json.dumps(record, ensure_ascii=False).encode("utf-8"))
            os.fsync(fd)
            os.close(fd)
            return True

        holder = read_owner(target)
        if ttl is not None and _record_age(holder, target) > ttl and _try_steal(target):
            continue
        return False


def release_claim(root: Path | str, name: str, *, claim_id: str | None = None) -> None:
    """Remove a reservation — but only if ``claim_id`` matches its owner."""

    if locks_disabled():
        return
    target = claims_dir(root) / f"{name}.json"
    holder = read_owner(target)
    if holder and claim_id and holder.get("claim_id") != claim_id:
        return
    try:
        target.unlink()
    except OSError:
        pass
