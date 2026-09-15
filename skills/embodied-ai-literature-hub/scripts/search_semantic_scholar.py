"""Thin entry point: Search the Semantic Scholar Graph API (default metadata backend).

Implementation lives in src/search/legacy/search_semantic_scholar.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.semantic_scholar import main

raise SystemExit(main())
