"""Thin entry point: Render markdown figure/table blocks from captured captions.

Implementation lives in src/parse/legacy/render_figure_table_block.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.parse.legacy.render_figure_table_block import main

raise SystemExit(main())
