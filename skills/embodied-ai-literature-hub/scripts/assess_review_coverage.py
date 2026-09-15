"""Thin entry point: Assess query-dimension coverage and saturation.

Implementation lives in src/search/legacy/assess_review_coverage.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.legacy.assess_review_coverage import main

raise SystemExit(main())
