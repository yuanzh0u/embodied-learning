"""Thin entry point: Rank papers by BM25 relevance to open research questions.

Implementation lives in src/search/legacy/rank_problem_relevance.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.problem_relevance import main

raise SystemExit(main())
