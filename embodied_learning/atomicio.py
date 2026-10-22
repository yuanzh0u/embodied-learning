"""Torn-read-safe filesystem writes shared by the package and the Wiki scripts.

Readers on a shared knowledge base (possibly a CIFS mount served to several
machines) never take a lock when they read ``index.jsonl``, ``current.json`` or
a pool paper's files. Every rewrite of such a file therefore goes through one
of the helpers here: write to a sibling ``.tmp-<uuid>`` file, fsync, then
``os.replace`` — readers see either the old or the new content, never a
truncated mix. Pair the helpers with :mod:`embodied_learning.locks` where a
read-merge-rewrite round trip must not lose a concurrent writer's update.
"""

from __future__ import annotations

import json
import os
import shutil
import uuid
from pathlib import Path


def _tmp_name(path: Path) -> Path:
    return path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")


def atomic_write_bytes(path: Path | str, data: bytes) -> None:
    """Replace ``path`` with ``data`` atomically (tmp + fsync + ``os.replace``)."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = _tmp_name(path)
    try:
        with temporary.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_write_text(path: Path | str, text: str) -> None:
    """Replace ``path`` with ``text`` atomically (tmp + fsync + ``os.replace``)."""

    atomic_write_bytes(path, text.encode("utf-8"))


def atomic_write_json(path: Path | str, value: object, *, indent: int | None = 2) -> None:
    """Write ``value`` as JSON via tmp file + ``os.replace`` so readers never
    see a half-written file. Cleans up the tmp file on failure."""

    payload = json.dumps(value, ensure_ascii=False, indent=indent) + "\n"
    atomic_write_text(Path(path), payload)


def atomic_copy(src: Path | str, dst: Path | str) -> None:
    """Copy ``src`` over ``dst`` atomically (metadata-preserving)."""

    src, dst = Path(src), Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    temporary = _tmp_name(dst)
    try:
        shutil.copy2(src, temporary)
        os.replace(temporary, dst)
    finally:
        temporary.unlink(missing_ok=True)
