"""Thin entry point: Project a validated note + audit into evidence event JSONL.

Implementation lives in src/knowledge/legacy/project_evidence_events.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.knowledge.legacy.project_evidence_events import main

raise SystemExit(main())
