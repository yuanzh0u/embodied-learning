"""Small filesystem helpers shared by the Wiki scripts."""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path


def load_json(path: Path | str) -> dict | list:
    """Read a JSON document, raising ValueError with the path on decode errors."""

    path = Path(path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON ({exc})") from exc


def atomic_write_json(path: Path, value: object, *, indent: int | None = 2) -> None:
    """Write ``value`` as JSON via tmp file + ``os.replace`` so readers never
    see a half-written file. Cleans up the tmp file on failure."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    payload = json.dumps(value, ensure_ascii=False, indent=indent) + "\n"
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
