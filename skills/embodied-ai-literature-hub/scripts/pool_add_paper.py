"""Thin entry point: manage the local public paper pool (add/list/get/import).

Implementation lives in src/knowledge/legacy/pool_add_paper.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.knowledge.legacy.pool_add_paper import main

raise SystemExit(main())
