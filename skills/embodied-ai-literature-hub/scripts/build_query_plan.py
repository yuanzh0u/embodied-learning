"""Thin entry point: Build a structured arXiv query plan from a topic (planning stage).

Implementation lives in src/search/legacy/build_query_plan.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.legacy.build_query_plan import main

raise SystemExit(main())
