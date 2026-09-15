"""Thin entry point: Validate paper-note JSON against the note schema.

Implementation lives in src/knowledge/legacy/validate_paper_note.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.knowledge.paper_note import main

raise SystemExit(main())
