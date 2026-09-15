"""Thin entry point: Rank a root paper's 1-hop neighborhood by composite influence.

Implementation lives in src/search/legacy/rank_influential_papers.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.legacy.rank_influential_papers import main

raise SystemExit(main())
