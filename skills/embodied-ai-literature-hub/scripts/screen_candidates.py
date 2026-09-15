"""Thin entry point: Prioritize the candidate registry for full-text recovery.

Implementation lives in src/search/legacy/screen_candidates.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.screening import main

raise SystemExit(main())
