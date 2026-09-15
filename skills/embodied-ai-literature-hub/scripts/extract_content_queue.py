"""Thin entry point: Recover full text for a paper-ID queue with bounded concurrency.

Implementation lives in src/fetch/legacy/extract_content_queue.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.fetch.queue import main

raise SystemExit(main())
