"""JSON document I/O helpers.

``load_json`` is the single reader (ValueError with the path on decode
errors); writers are thin wrappers over :mod:`embodied_learning.atomicio`
(the shared-file rewrite engine — every rewrite of a shared file must stay
atomic). Replaces the ``load_json`` copies that were scattered across
scripts and search modules.
"""

from __future__ import annotations

import json
from pathlib import Path

from embodied_learning.atomicio import (  # noqa: F401  (re-exported for callers)
    atomic_copy,
    atomic_write_bytes,
    atomic_write_json,
    atomic_write_text,
)


def load_json(path: Path | str) -> dict | list:
    """Read a JSON document, raising ValueError with the path on decode errors."""

    path = Path(path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON ({exc})") from exc
