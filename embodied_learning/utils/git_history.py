"""Helpers for git history requirements used by archive-aware checks."""

from __future__ import annotations

import subprocess
from pathlib import Path


SHALLOW_CLONE_MESSAGE = (
    "shallow clone detected; need full history for archive checks "
    "(clone without --depth, or run: git fetch --unshallow)"
)


def is_shallow_repository(root: Path) -> bool:
    """Return True when ``root`` is a shallow git clone.

    Non-git directories and git failures return False so callers that only
    care about archive-object lookups can fall through to their existing
    error paths.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def require_full_history(root: Path) -> None:
    """Raise ``SystemExit`` with a clear message when the clone is shallow.

    Archive checks resolve retired sources via ``git show <ref>:<path>`` /
    ``git cat-file``. A ``--depth 1`` clone cannot see those historical
    objects and otherwise fails with cryptic "object not found" errors.
    """
    if is_shallow_repository(root):
        raise SystemExit(SHALLOW_CLONE_MESSAGE)
