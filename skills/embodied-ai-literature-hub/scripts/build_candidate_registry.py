"""Thin entry point: Merge discovery rounds into a deduplicated candidate registry.

Implementation lives in src/search/legacy/build_candidate_registry.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.legacy.build_candidate_registry import main

raise SystemExit(main())
