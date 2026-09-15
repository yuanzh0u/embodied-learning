"""Thin entry point: Download TeX source tarballs from requester-pays s3://arxiv/.

Implementation lives in src/fetch/legacy/download_arxiv_source.py (shared arXiv-data layer).
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.fetch.legacy.download_arxiv_source import main

raise SystemExit(main())
