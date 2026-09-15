"""Thin entry point: Search the arXiv Atom API and emit normalized candidate JSON.

Implementation lives in src/search/legacy/search_arxiv.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.arxiv import main

raise SystemExit(main())
