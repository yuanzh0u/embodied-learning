#!/usr/bin/env python3
"""CLI: merge discovery rounds into a deduplicated candidate registry.

Library API lives in embodied_learning/search/candidate_registry.py (module-level
``build_registry``). This entry owns only argument parsing and dispatch.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.search.candidate_registry import run  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search-result", action="append", default=[], help="search_arxiv.py JSON; repeat by round.")
    parser.add_argument(
        "--semantic-scholar-result",
        action="append",
        default=[],
        help="search_semantic_scholar.py JSON; repeat by round.",
    )
    parser.add_argument("--browser-result", action="append", default=[], help="parse_browser_candidates.py JSON; repeatable.")
    parser.add_argument("--citation-result", action="append", default=[], help="expand_via_citations.py JSON; repeatable.")
    parser.add_argument("--screening-file", help="Optional JSON candidate/status updates.")
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run(
        [Path(path) for path in args.search_result],
        [Path(path) for path in args.browser_result],
        [Path(path) for path in args.citation_result],
        [Path(path) for path in args.semantic_scholar_result],
        Path(args.screening_file) if args.screening_file else None,
        Path(args.output),
    )


if __name__ == "__main__":
    sys.exit(main())
