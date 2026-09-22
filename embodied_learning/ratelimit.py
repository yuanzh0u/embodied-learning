"""Machine-wide request throttling for arXiv / Semantic Scholar traffic.

Every process that talks to arXiv or S2 (review drivers, wiki workflows,
quick-reads) previously paced only itself, so N concurrent runs multiplied the
request rate and tripped 429/406 storms. This module replaces per-process
pacing with a machine-shared gate: a ``fcntl.flock``-serialized slot file per
policy group plus a shared cooldown that any process can extend after a 429/503
so the whole machine backs off together.

Usage at a call site — replace ``urllib.request.urlopen``::

    from .. import ratelimit

    with ratelimit.gated_urlopen(request, group="arxiv", timeout=20.0) as response:
        payload = response.read()

and for non-urllib transports (curl) use :func:`gate` directly::

    with ratelimit.gate("arxiv2md"):
        subprocess.run(["curl", ...])

Design notes:

- Sleeping happens while holding the lock on purpose — that *is* the global
  lock: concurrent processes queue on ``flock`` and are released one interval
  apart. ``flock`` operates on open file descriptions, so threads of one
  process (e.g. the fetch queue's thread pool) are mutually excluded as well.
- The gate covers request dispatch only; the response body is read after the
  slot is released (``next_ok_ts`` was already advanced, so pacing holds).
- ``report_rejection`` shares backoff machine-wide: one process's 429 with a
  ``Retry-After`` delays every process's next request in that group.
"""

from __future__ import annotations

import errno
import fcntl
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from contextlib import contextmanager
from pathlib import Path

TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}

# Policy groups: one shared slot/cooldown file per group. arXiv's official
# politeness rate is 1 request / 3 s for API+export; S2 429s aggressively
# without an API key; arxiv2md publishes 30 req/min per IP.
DEFAULT_INTERVALS = {
    "arxiv": 3.0,
    "semanticscholar": 1.0,
    "arxiv2md": 2.0,
}

DEFAULT_RETRY_BASE_SECONDS = 20.0
DEFAULT_RETRY_CAP_SECONDS = 600.0

_LOCK_POLL_SECONDS = 0.05


class GateTimeout(RuntimeError):
    """Raised when a gate could not be acquired within ``max_wait`` seconds."""


def state_dir() -> Path:
    """Machine-shared state directory (env-overridable for tests/containers)."""
    override = os.environ.get("EMBODIED_RATELIMIT_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".cache" / "embodied-learning" / "ratelimit"


def resolve_interval(group: str, min_interval: float | None = None) -> float:
    """Effective spacing for a group: explicit argument > env override > default."""
    if min_interval is not None and min_interval > 0:
        return float(min_interval)
    env_key = "EMBODIED_RATELIMIT_" + group.upper() + "_INTERVAL"
    env_value = os.environ.get(env_key)
    if env_value:
        try:
            parsed = float(env_value)
        except ValueError:
            parsed = 0.0
        if parsed > 0:
            return parsed
    return DEFAULT_INTERVALS.get(group, 1.0)


def group_for_url(url: str) -> str:
    """Best-effort policy group for a URL; unknown hosts get their own group."""
    host = urllib.parse.urlsplit(url).netloc.rsplit("@", 1)[-1].split(":", 1)[0].lower()
    if host.endswith("arxiv.org"):
        return "arxiv"
    if host.endswith("semanticscholar.org"):
        return "semanticscholar"
    if "arxiv2md" in host:
        return "arxiv2md"
    return host or "unknown"


def _lock_path(group: str) -> Path:
    return state_dir() / f"{group}.lock"


def _state_path(group: str) -> Path:
    return state_dir() / f"{group}.json"


def _read_state(group: str) -> dict[str, float]:
    try:
        payload = json.loads(_state_path(group).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_state(group: str, state: dict[str, float]) -> None:
    target = _state_path(group)
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state), encoding="utf-8")
    os.replace(tmp, target)


def _retry_after_seconds(exc: Exception) -> float | None:
    headers = getattr(exc, "headers", None)
    value = headers.get("Retry-After") if headers is not None else None
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _acquire_lock(lock_fd: int, max_wait: float | None, group: str) -> None:
    """Exclusive flock with polling; raises GateTimeout when bounded past deadline."""
    deadline = None if max_wait is None else time.monotonic() + max_wait
    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except OSError as exc:
            if exc.errno not in (errno.EACCES, errno.EAGAIN):
                raise
            if deadline is not None and time.monotonic() >= deadline:
                raise GateTimeout(f"gate '{group}' queue wait exceeded {max_wait}s") from exc
            time.sleep(_LOCK_POLL_SECONDS)


@contextmanager
def gate(group: str, *, min_interval: float | None = None, max_wait: float | None = None):
    """Reserve one request slot for ``group``, machine-wide.

    Blocks (queuing on flock) until the group's shared ``next_ok_ts`` /
    ``cooldown_until`` have passed, then advances ``next_ok_ts`` by the group
    interval. Each wait (queueing and spacing separately) is bounded by
    ``max_wait``; expiry raises :class:`GateTimeout` so callers can reach their
    degradation paths.
    """
    interval = resolve_interval(group, min_interval)
    state_dir().mkdir(parents=True, exist_ok=True)
    lock_fd = os.open(_lock_path(group), os.O_RDWR | os.O_CREAT, 0o600)
    try:
        _acquire_lock(lock_fd, max_wait, group)
        state = _read_state(group)
        now = time.time()
        earliest = max(float(state.get("next_ok_ts", 0.0)), float(state.get("cooldown_until", 0.0)))
        wait = earliest - now
        if wait > 0:
            if max_wait is not None and wait > max_wait:
                raise GateTimeout(f"gate '{group}' spacing wait {wait:.1f}s exceeded {max_wait}s")
            time.sleep(wait)
        reserved = time.time()
        state["next_ok_ts"] = max(reserved, earliest) + interval
        if state.get("cooldown_until", 0) <= reserved:
            state.pop("cooldown_until", None)  # expired cooldown: clear it
        _write_state(group, state)
        yield
    finally:
        os.close(lock_fd)  # releases the flock


def report_rejection(
    group: str,
    retry_after: float | None = None,
    *,
    base_seconds: float = DEFAULT_RETRY_BASE_SECONDS,
    cap_seconds: float = DEFAULT_RETRY_CAP_SECONDS,
) -> float:
    """Record a 429/503 rejection: every process's next gate in ``group`` waits.

    ``retry_after`` (from the response) wins; otherwise a default backoff is
    applied. Returns the cooldown actually recorded, relative to now."""
    wait = retry_after if retry_after is not None else base_seconds
    wait = max(0.0, min(float(wait), cap_seconds))
    state_dir().mkdir(parents=True, exist_ok=True)
    lock_fd = os.open(_lock_path(group), os.O_RDWR | os.O_CREAT, 0o600)
    try:
        # Bounded, non-blocking acquisition: a sibling process may legitimately
        # hold this lock while sleeping out its slot, and recording the cooldown
        # must never wedge the caller for a full cooldown period.
        _acquire_lock(lock_fd, 10.0, group)
        state = _read_state(group)
        now = time.time()
        until = now + wait
        state["cooldown_until"] = max(float(state.get("cooldown_until", 0.0)), until)
        _write_state(group, state)
        return state["cooldown_until"] - now
    finally:
        os.close(lock_fd)


def gated_urlopen(
    request: urllib.request.Request,
    *,
    group: str | None = None,
    timeout: float,
    max_wait: float | None = None,
    min_interval: float | None = None,
):
    """``urlopen`` behind the machine-wide gate. Transient rejections (429/503
    family) extend the group's shared cooldown before re-raising, so sibling
    processes back off too; the caller's existing retry loop decides what to do
    with the exception. Pass ``group=None`` to derive it from the URL. The
    cooldown is recorded after the gate is released (report_rejection takes the
    same lock — recording inside the gate would self-deadlock)."""
    resolved_group = group or group_for_url(request.full_url)
    try:
        with gate(resolved_group, min_interval=min_interval, max_wait=max_wait):
            return urllib.request.urlopen(request, timeout=timeout)
    except urllib.error.HTTPError as exc:
        if exc.code in TRANSIENT_HTTP_CODES:
            report_rejection(resolved_group, _retry_after_seconds(exc))
        raise
