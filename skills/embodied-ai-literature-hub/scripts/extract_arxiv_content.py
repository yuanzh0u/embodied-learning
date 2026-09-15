"""Thin entry point: Unified extraction gateway: HTML -> markdown -> PDF chain.

Implementation lives in src/fetch/legacy/extract_arxiv_content.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.fetch.legacy.extract_arxiv_content import main

raise SystemExit(main())
