"""Thin entry point: Validate evidence JSONL and render the markdown brief.

Implementation lives in src/parse/legacy/write_lit_outputs.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.parse.legacy.write_lit_outputs import main

raise SystemExit(main())
