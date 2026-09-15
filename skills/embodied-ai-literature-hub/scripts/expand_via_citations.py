"""Thin entry point: Expand candidates via S2 citation/reference neighborhoods (coupling/co-citation).

Implementation lives in src/search/legacy/expand_via_citations.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.legacy.expand_via_citations import main

raise SystemExit(main())
