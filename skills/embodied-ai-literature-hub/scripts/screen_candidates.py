#!/usr/bin/env python3
"""CLI: prioritize the candidate registry for full-text recovery.

Library API lives in embodied_learning/search/screening.py (module-level
``select_candidates``). This entry owns only argument parsing and dispatch.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.search.screening import run  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-registry", required=True)
    parser.add_argument("--terms", required=True, help="Comma-separated title/abstract relevance terms.")
    parser.add_argument("--query-label-prefix", action="append", default=[], help="Prefer discoveries whose query label starts with this prefix.")
    parser.add_argument("--seed-evidence-jsonl", action="append", default=[], help="Previously accepted evidence used only as a priority seed.")
    parser.add_argument("--limit", type=int, default=40, help="Number of candidates to queue for full-text recovery.")
    parser.add_argument("--output-screening", required=True)
    parser.add_argument("--output-ids", required=True)
    parser.add_argument("--output-markdown")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run(
        candidate_registry=args.candidate_registry,
        terms_raw=args.terms,
        query_label_prefixes=args.query_label_prefix,
        seed_evidence_jsonl=args.seed_evidence_jsonl,
        limit=args.limit,
        output_screening=args.output_screening,
        output_ids=args.output_ids,
        output_markdown=args.output_markdown,
    )


if __name__ == "__main__":
    sys.exit(main())
