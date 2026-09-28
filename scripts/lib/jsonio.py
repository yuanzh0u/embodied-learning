"""Small filesystem helpers shared by the Wiki scripts.

Atomic writers live in :mod:`embodied_learning.atomicio` (single home for the
package layer and the scripts layer); this module re-exports them so existing
``from lib.jsonio import atomic_write_json`` callers keep working. ``load_json``
stays here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from embodied_learning.atomicio import (  # noqa: F401
        atomic_copy,
        atomic_write_bytes,
        atomic_write_json,
        atomic_write_text,
    )
except ImportError:  # repo checkout: repo root may not be on sys.path yet
    _repo_root = Path(__file__).resolve().parents[2]
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))
    from embodied_learning.atomicio import (  # noqa: F401
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
