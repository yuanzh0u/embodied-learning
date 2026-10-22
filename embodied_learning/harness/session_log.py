"""Agent session ledger writer — the embodied-learning side of
``monica/spec/usage-records-format.md``.

One JSONL file per agent session, one JSON object per line, in the Claude
Code session shape plus the loglens extension layer:

- ``type=assistant`` + ``message.usage`` lines: billing / cost analysis;
- ``type=system`` + ``level``/``kind``/``text``/``attrs`` lines: mechanical
  workflow events (step / metric / error) for log analysis.

Discipline (from the spec):

- append only, never rewrite history;
- timestamps carry a timezone offset (naive timestamps are dropped by readers);
- ``input_tokens`` excludes cache reads and images;
- ``message.id`` enables dedup of streamed partial writes — the consumer keeps
  the entry with the largest ``output_tokens`` per id;
- no prompt/response bodies: ``text`` is a short diagnostic string.

The file lives under :func:`embodied_learning.harness.claude.conversation_store`
(``~/.claude/projects/embodied-learning-work`` by default), so monica's session
scanner discovers it as project ``embodied-learning-work``.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, TextIO

from embodied_learning.config import SESSION_EVENT_TEXT_MAX_CHARS

# Raw usage keys -> canonical Claude keys.
_KNOWN_USAGE_KEYS = {
    "input_tokens": "input_tokens",
    "output_tokens": "output_tokens",
    "cache_read_input_tokens": "cache_read_input_tokens",
    "cache_creation_input_tokens": "cache_creation_input_tokens",
}
# ``claude_cache_creation_{5m,1h}_tokens`` are variants of the same counter.
_CACHE_WRITE_PREFIX = "claude_cache_creation"

CANONICAL_USAGE_KEYS = (
    "input_tokens",
    "output_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
)


def iso_ts(ts: datetime | None = None) -> str:
    """ISO 8601 with a timezone offset (spec requires one)."""

    value = ts or datetime.now().astimezone()
    if value.tzinfo is None:
        value = value.astimezone()
    return value.isoformat()


def _as_int(value: Any) -> int:
    """Only real integer counters; bool/str/dict/list never count."""

    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return value


def canonical_usage(raw: dict | None) -> dict[str, int]:
    """Normalize an API ``usage`` object to the four canonical counters.

    ``cache_creation_input_tokens`` wins when present; the
    ``claude_cache_creation_*`` variants are summed only as a fallback, so a
    provider emitting both forms cannot double-count. Unknown keys are ignored
    (the spec's readers do the same).
    """

    out = {key: 0 for key in CANONICAL_USAGE_KEYS}
    if not isinstance(raw, dict):
        return out
    variants = 0
    for key, value in raw.items():
        canonical = _KNOWN_USAGE_KEYS.get(key)
        if canonical:
            out[canonical] = _as_int(value)
        elif str(key).startswith(_CACHE_WRITE_PREFIX):
            variants += _as_int(value)
    if "cache_creation_input_tokens" not in raw:
        out["cache_creation_input_tokens"] = variants
    return out


def usage_totals(records: list[dict]) -> dict[str, int]:
    """Sum canonical usage records (``[{"usage": {...}}, ...]``)."""

    total = {key: 0 for key in CANONICAL_USAGE_KEYS}
    for record in records:
        usage = record.get("usage") if isinstance(record, dict) else None
        if not isinstance(usage, dict):
            continue
        for key in CANONICAL_USAGE_KEYS:
            total[key] += _as_int(usage.get(key))
    return total


# ---- free-function writers (mirror monica's reference implementation) -------


def write_usage(
    fh: TextIO,
    *,
    ts: datetime | None = None,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_read: int = 0,
    cache_write: int = 0,
    msg_id: str = "",
    attrs: dict | None = None,
    **extra: Any,
) -> dict:
    """One billing-readable usage line (``message.usage``)."""

    entry: dict[str, Any] = {
        "type": "assistant",
        "timestamp": iso_ts(ts),
        "message": {
            "model": model,
            "usage": {
                "input_tokens": _as_int(input_tokens),
                "output_tokens": _as_int(output_tokens),
                "cache_read_input_tokens": _as_int(cache_read),
                "cache_creation_input_tokens": _as_int(cache_write),
            },
        },
    }
    if msg_id:
        entry["message"]["id"] = msg_id
    if attrs:
        entry["attrs"] = attrs
    entry.update(extra)
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def write_event(
    fh: TextIO,
    *,
    ts: datetime | None = None,
    level: str = "info",
    kind: str = "note",
    text: str = "",
    **attrs: Any,
) -> dict:
    """One loglens-readable mechanical event line."""

    entry: dict[str, Any] = {
        "type": "system",
        "timestamp": iso_ts(ts),
        "level": level,
        "kind": kind,
        # D9: no prompt/response bodies — diagnostics are clipped at the cap.
        "text": str(text)[:SESSION_EVENT_TEXT_MAX_CHARS],
    }
    if attrs:
        entry["attrs"] = attrs
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def write_step(fh: TextIO, *, ts: datetime | None = None, stage: str, **attrs: Any) -> dict:
    return write_event(fh, ts=ts, level="info", kind="step", text=stage, stage=stage, **attrs)


def write_metric(
    fh: TextIO,
    *,
    ts: datetime | None = None,
    stage: str,
    duration_s: float,
    **attrs: Any,
) -> dict:
    return write_event(
        fh,
        ts=ts,
        level="info",
        kind="metric",
        text=f"{stage} completed",
        stage=stage,
        duration_s=round(float(duration_s), 3),
        **attrs,
    )


def write_error(
    fh: TextIO,
    *,
    ts: datetime | None = None,
    text: str,
    stage: str = "",
    exit_code: int | None = None,
    **attrs: Any,
) -> dict:
    if exit_code is not None:
        attrs["exit_code"] = exit_code
    return write_event(fh, ts=ts, level="error", kind="error", text=text, stage=stage, **attrs)


class SessionLog:
    """Append-only, thread-safe writer for one session ledger file.

    Long-lived agents (``ChatTurn``) keep one instance for the whole session;
    one-shot calls open one, write step/usage/metric, and close. Every method
    returns the written dict so callers can reuse it.
    """

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._fh = self.path.open("a", encoding="utf-8")

    @property
    def closed(self) -> bool:
        return self._fh.closed

    def _emit(self, writer, *args: Any, **kwargs: Any) -> dict:
        """Best-effort append: a full disk or a dead mount must never break
        the model call the ledger is observing (spec: recording is a side
        channel). Returns ``{}`` when the write failed."""

        with self._lock:
            if self._fh.closed:
                return {}
            try:
                entry = writer(self._fh, *args, **kwargs)
                # Flush per line: a long pipeline run is exactly when a crash
                # (or a killed driver) must not cost the trajectory so far.
                self._fh.flush()
                return entry
            except (OSError, ValueError, TypeError):
                return {}

    # -- usage -------------------------------------------------------------

    def usage(self, *, usage: dict | None = None, **kwargs: Any) -> dict:
        """Write a usage record. Pass either a raw ``usage`` dict or explicit
        ``input_tokens``/``output_tokens``/``cache_read``/``cache_write``."""

        if usage is not None:
            canonical = canonical_usage(usage)
            kwargs.setdefault("input_tokens", canonical["input_tokens"])
            kwargs.setdefault("output_tokens", canonical["output_tokens"])
            kwargs.setdefault("cache_read", canonical["cache_read_input_tokens"])
            kwargs.setdefault("cache_write", canonical["cache_creation_input_tokens"])
        return self._emit(write_usage, **kwargs)

    # -- mechanical events -------------------------------------------------

    def event(self, **kwargs: Any) -> dict:
        return self._emit(write_event, **kwargs)

    def step(self, stage: str, **kwargs: Any) -> dict:
        return self._emit(write_step, stage=stage, **kwargs)

    def metric(self, stage: str, duration_s: float, **kwargs: Any) -> dict:
        return self._emit(write_metric, stage=stage, duration_s=duration_s, **kwargs)

    def error(self, text: str, **kwargs: Any) -> dict:
        return self._emit(write_error, text=text, **kwargs)

    # -- lifecycle ---------------------------------------------------------

    def close(self) -> None:
        with self._lock:
            if not self._fh.closed:
                try:
                    self._fh.close()
                except OSError:
                    pass

    def __enter__(self) -> "SessionLog":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
