"""Thin entry point: Parse browser-exported arXiv candidate lists.

Implementation lives in src/search/legacy/parse_browser_candidates.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.browser_candidates import main

raise SystemExit(main())
