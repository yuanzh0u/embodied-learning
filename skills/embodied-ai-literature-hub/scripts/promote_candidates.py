"""Thin entry point: Promote verified candidates toward evidence with digests and skeletons.

Implementation lives in src/parse/legacy/promote_candidates.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.parse.legacy.promote_candidates import main

raise SystemExit(main())
