"""Thin entry point: Fetch/cache arXiv LaTeXML HTML and extract the section tree.

Implementation lives in src/fetch/legacy/extract_arxiv_html.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.fetch.html import main

raise SystemExit(main())
