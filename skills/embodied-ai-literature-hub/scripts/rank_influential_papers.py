#!/usr/bin/env python3
"""CLI: rank a root paper's 1-hop neighborhood by composite influence.

Library API lives in src/search/influence.py (InfluenceRanking). This entry
owns only argument parsing and dispatch.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.influence import MAX_RETRIES, InfluenceRanking  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-id", action="append", default=[], help="Root arXiv ID. May be repeated.")
    parser.add_argument("--direction", choices=["references", "citations", "both"], default="both")
    parser.add_argument("--top", type=int, default=10, help="Number of ranked papers to emit.")
    parser.add_argument("--max-per-seed-per-direction", type=int, default=500, help="Neighbor cap per direction (pagination walks the whole list up to this).")
    parser.add_argument(
        "--weights",
        default="citation=0.40,venue=0.25,author=0.20,code=0.15",
        help="Comma-separated dimension=weight. Normalized to sum 1 if not already.",
    )
    parser.add_argument("--author-strategy", choices=["max-hindex", "first-author"], default="max-hindex")
    parser.add_argument("--code-source", choices=["pwc", "abstract", "none"], default="abstract",
                        help="How to detect code availability. 'abstract' is a confirm-only heuristic; 'pwc' hits PapersWithCode; 'none' is neutral.")
    parser.add_argument("--min-year", type=int, default=None,
                        help="Drop neighbors published before this year (inclusive). Unknown-year papers are kept, not dropped.")
    parser.add_argument("--require-terms", default=None,
                        help="Comma-separated terms; keep a neighbor only if at least one term appears (case-insensitive) in its title+abstract.")
    parser.add_argument("--require-title-terms", default=None,
                        help="Comma-separated terms; keep a neighbor only if at least one term appears (case-insensitive) in its TITLE. Tighter field gate than --require-terms.")
    parser.add_argument("--must-terms", default=None,
                        help="Comma-separated terms; a paper is DROPPED unless at least one appears (case-insensitive) in title+abstract. A hard AND-gate on top of --require-terms/--require-title-terms (e.g. require the third-person/exo side).")
    parser.add_argument("--paper-id-file", action="append", default=[],
                        help="File of extra arXiv IDs (one per line) to add to the candidate pool and enrich via the batch endpoint. Repeatable. Use with expand_via_citations.py output to enlarge the pool (e.g. 2-hop downstream).")
    parser.add_argument("--output", help="Ranked JSON. Defaults to stdout.")
    parser.add_argument("--markdown-output", help="Ranking table Markdown.")
    parser.add_argument("--sleep-seconds", type=float, default=1.0, help="Delay between network phases.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per request. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0)
    parser.add_argument("--retry-max-seconds", type=float, default=60.0)
    parser.add_argument("--fail-fast", action="store_true", help="Abort on first failed request.")
    parser.add_argument("--user-agent", default="embodied-ai-literature-hub/1.0 (local research workflow)")
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to S2_API_KEY env var.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ranking = InfluenceRanking(
        seed_id=args.seed_id,
        direction=args.direction,
        top=args.top,
        max_per_seed_per_direction=args.max_per_seed_per_direction,
        weights=args.weights,
        author_strategy=args.author_strategy,
        code_source=args.code_source,
        min_year=args.min_year,
        require_terms=args.require_terms,
        require_title_terms=args.require_title_terms,
        must_terms=args.must_terms,
        paper_id_file=args.paper_id_file,
        output=args.output,
        markdown_output=args.markdown_output,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        user_agent=args.user_agent,
        api_key=args.api_key or os.environ.get("S2_API_KEY"),
    )
    return ranking.run()


if __name__ == "__main__":
    sys.exit(main())
