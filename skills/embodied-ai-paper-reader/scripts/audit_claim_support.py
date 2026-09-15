"""Thin entry point: Audit claim/quote verbatim support in a paper note.

Implementation lives in src/knowledge/legacy/audit_claim_support.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.knowledge.legacy.audit_claim_support import main

raise SystemExit(main())
