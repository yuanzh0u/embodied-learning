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
  on the registry's RLock before touching the file. Because of that, reaching
  the file acquire with our own pid in the owner record means the previous
  release leaked (CIFS unlink blip) — the leftover is stolen immediately
  instead of making the same process wait out its own lock.
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
STEAL_MARKER_MAX_AGE = 60.0
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


def _appendable(path: Path) -> bool:
    """Can we append to this path? A CIFS ghost shows up in readdir but every
    open fails — the one shape the journal design cannot ride out on the
    primary name (we only append, so we never make new ghosts; the primary
    may still be a leftover from the old delete/create mechanism)."""

    try:
        fd = os.open(path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o644)
    except OSError:
        return False
    else:
        os.close(fd)
        return True


def journal_path(root: Path | str, name: str) -> Path:
    """Journal file for ``name``: the canonical one, or ``~1``/``~2``/``~3``
    when the canonical name is an unkillable ghost. All waiters run the same
    probe so they land on the same fallback."""

    base = lock_path(root, name)
    if _appendable(base):
        return base
    for index in range(1, 4):
        alt = base.with_name(f"{base.name}~{index}")
        if _appendable(alt):
            print(
                f"[kb-lock] 锁 {name} 的原路径不可写（CIFS 幽灵 dentry），改用 {alt.name}",
                file=sys.stderr,
            )
            return alt
    return base


def claims_dir(root: Path | str) -> Path:
    return Path(root) / CLAIMS_DIRNAME


def _owner_record(name: str, detail: str, *, op: str = "acquire") -> dict[str, object]:
    now = time.time()
    return {
        "op": op,
        "name": name,
        "host": socket.gethostname(),
        "pid": os.getpid(),
        "ts": now,
        "ts_iso": datetime.fromtimestamp(now, tz=timezone.utc).isoformat(),
        "cmd": " ".join(sys.argv[:4]),
        "detail": detail,
        "claim_id": uuid.uuid4().hex,
    }


# ---- append-only lock journal -------------------------------------------
# CIFS does delete/create/rename badly (ghost dentries that answer EEXIST
# forever and cannot be unlinked). It appends fine. So the lock file is a
# NEVER-DELETED journal: every acquire/release is one appended JSON line,
# and the holder is reconstructed by replaying it. No O_EXCL, no unlink,
# no rename — the three operations that wedge on a flaky share (2026-10-12).
# Side benefit: the journal is a complete audit trail of who held the lock.


def _journal_events(path: Path) -> list[dict[str, object]]:
    """Parse the journal, skipping torn/unparseable lines. Each record gets
    ``_offset`` (its start byte) so a waiter can tell whether a rival appended
    after its own acquire. A legacy single-JSON-object file (one owner record,
    no ``op``) is read as a lone ``acquire`` so old locks still resolve."""

    try:
        raw = path.read_bytes()
    except OSError:
        return []
    if not raw.strip():
        return []
    events: list[dict[str, object]] = []
    offset = 0
    for line in raw.splitlines(keepends=True):
        start = offset
        offset += len(line)
        text = line.decode("utf-8", errors="replace").strip()
        if not text:
            continue
        try:
            record = json.loads(text)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        record = dict(record)
        record.setdefault("op", "acquire")  # legacy owner record = a lone acquire
        record["_offset"] = start
        events.append(record)
    return events


def _current_holder(events: list[dict[str, object]]) -> dict[str, object] | None:
    """Replay the journal: the holder is the last ``acquire`` with no
    ``release`` after it. A later ``acquire`` (a stale-steal) takes over."""

    open_claims: dict[str, dict[str, object]] = {}
    acquires: list[dict[str, object]] = []
    for record in events:
        claim_id = str(record.get("claim_id") or "")
        if not claim_id:
            continue
        if record.get("op") == "release":
            open_claims.pop(claim_id, None)
            continue
        open_claims[claim_id] = record
        acquires.append(record)
    for record in reversed(acquires):
        if str(record.get("claim_id")) in open_claims:
            return record
    return None


def _append_event(path: Path, record: dict[str, object]) -> int:
    """Append one journal line; return the byte offset it landed at.
    O_APPEND only — create-once, never unlink. A torn write at most costs
    one skipped line on the next read."""

    line = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o644)
    try:
        offset = os.lseek(fd, 0, os.SEEK_END)
        os.write(fd, line)
        os.fsync(fd)
        return offset
    finally:
        os.close(fd)


def _later_acquire(events: list[dict[str, object]], offset: int, claim_id: str) -> bool:
    """True when a rival appended an acquire after our byte offset."""

    for record in events:
        if record.get("op") != "acquire":
            continue
        if str(record.get("claim_id")) == claim_id:
            continue
        if int(record.get("_offset") or 0) > offset:
            return True
    return False


def read_owner(lock_file: Path | str) -> dict[str, object] | None:
    """Current holder reconstructed from the journal; None when unheld."""

    events = _journal_events(Path(lock_file))
    return _current_holder(events) if events else None


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
        # Cannot stat: ghost dentry, or the name is already gone on the server
        # while EEXIST is still cache-answered. Returning 0.0 here made the
        # unreadable-grace reclaim unreachable ("just created" forever), which
        # is exactly how a quick-read card write timed out against a ghost.
        # Treat age as unknown-but-old so the grace path can fire.
        return float("inf")










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


def _is_own_leftover(record: dict[str, object] | None) -> bool:
    """True when the lock file is a leftover of THIS process's own earlier
    acquisition.

    Reaching ``_acquire`` with depth==1 means the registry says we do not hold
    this lock (nested/reentrant takes skip the file acquire; sibling threads
    serialize on the entry RLock first). So a record stamped with our own live
    pid is a leaked file — release's unlink failed, typically a CIFS dentry
    hiccup — and must be reclaimable immediately. Without this, the next write
    in the same process (quick-read brief, then card) sits out the full wait
    against itself and times out. Same-pid is never a live foreign holder, and
    a recycled pid from a dead previous run is also a leftover, so stealing is
    safe either way.
    """

    if not record:
        return False
    host, pid = record.get("host"), record.get("pid")
    return (
        isinstance(host, str)
        and host == socket.gethostname()
        and isinstance(pid, int)
        and pid == os.getpid()
    )






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
    """Append one journal line (see _append_event). Kept as a seam for tests
    that want to observe the owner record being written."""

    _append_event(Path(lock_file), record)


def _holder_relinquished(holder: dict[str, object] | None, *, stale: float, now: float) -> bool:
    """True when the current holder no longer counts: gone, dead on this host,
    this process's own leftover, or past the stale TTL."""

    if holder is None:
        return True
    if _is_own_leftover(holder):
        return True
    if _holder_dead_locally(holder):
        return True
    ts = holder.get("ts")
    if isinstance(ts, (int, float)) and now - float(ts) > stale:
        return True
    return False


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

    Implementation is an append-only journal (one JSON line per
    acquire/release) — never delete/create/rename, the three operations a
    flaky CIFS share answers with ghost dentries. ``wait`` bounds the total
    blocking wait (default 120 s); expiry raises :class:`LockTimeout`.
    ``fail_fast=True`` makes a single non-blocking attempt and raises
    :class:`LockBusy`. ``stale`` is the age after which a crashed holder's
    lock may be stolen (by appending a new acquire)."""

    if locks_disabled():
        print(f"[kb-lock] 已禁用（EMBODIED_KB_LOCKS_DISABLED=1），跳过锁 {name}", file=sys.stderr)
        yield
        return

    wait = DEFAULT_WAIT if wait is None else float(wait)
    stale = DEFAULT_STALE if stale is None else float(stale)
    poll = DEFAULT_POLL if poll is None else float(poll)
    target = journal_path(root, name)
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
    """Win the lock by appending an acquire and proving nobody appended after.

    Protocol: only append when the journal shows no live holder (or the holder
    has been relinquished). Then read back; if a rival appended after our byte
    offset we lost and undo. A short confirm re-read closes the
    both-appended-then-both-read race."""

    last_progress = 0.0
    while True:
        now = time.time()
        events = _journal_events(target)
        holder = _current_holder(events)
        if _holder_relinquished(holder, stale=stale, now=now):
            record = _owner_record(name, detail, op="acquire")
            claim_id = str(record["claim_id"])
            try:
                offset = _append_event(target, record)
            except OSError as exc:
                raise LockTimeout(f"锁 {target} 无法写入：{exc}") from exc
            # Confirm we are still the holder after the append.
            confirm = _current_holder(_journal_events(target))
            if confirm and str(confirm.get("claim_id")) == claim_id:
                if not _later_acquire(_journal_events(target), offset, claim_id):
                    entry.claim_id = claim_id
                    return
            # A rival won the append race — undo ours and fall through to wait.
            try:
                _append_event(target, _owner_record(name, detail, op="release") | {"claim_id": claim_id})
            except OSError:
                pass
        now = time.monotonic()
        if deadline is not None and now >= deadline:
            if fail_fast:
                raise LockBusy(
                    f"锁 {target} 正被 {_format_owner(holder)} 持有；"
                    f"请确认没有重复启动"
                )
            waited = f"{wait:.0f}s" if wait else "等待窗口"
            raise LockTimeout(
                f"等待锁 {target} 超过 {waited}（{_format_owner(holder)}）；"
                f"确认持有进程已退出后重试，或调大 EMBODIED_KB_LOCK_STALE"
            )
        if now - last_progress >= PROGRESS_EVERY:
            print(f"[kb-lock] 等待共享锁 {name}（{_format_owner(holder)}）…", file=sys.stderr)
            last_progress = now
        if fail_fast:
            raise LockBusy(
                f"锁 {target} 正被 {_format_owner(holder)} 持有；请确认没有重复启动"
            )
        time.sleep(poll)


def _release(target: Path, entry: _Entry) -> None:
    if not entry.claim_id:
        return
    try:
        holder = read_owner(target)
    except OSError:
        holder = None
    # Only release our own hold: a stale-steal may have handed the lock to
    # someone else while we were still working.
    if holder and holder.get("claim_id") != entry.claim_id:
        entry.claim_id = None
        return
    record = _owner_record(str((holder or {}).get("name") or target.stem), "", op="release")
    record["claim_id"] = entry.claim_id
    try:
        _append_event(target, record)
    except OSError as exc:
        # Never fatal: the journal just keeps an unmatched acquire, which the
        # stale-TTL / dead-pid paths reclaim. No unlink to fail.
        print(f"[kb-lock] 释放锁 {target.name} 记账失败（{exc}），将由 TTL 回收", file=sys.stderr)
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
