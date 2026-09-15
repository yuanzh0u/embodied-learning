#!/usr/bin/env python3
"""CLI: rank papers by BM25 relevance to open research questions.

Library API lives in src/search/problem_relevance.py
(ProblemRelevanceRetrieval). This entry owns only argument parsing and
dispatch.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.problem_relevance import (  # noqa: E402
    DEFAULT_CACHE_DIR,
    DEFAULT_FIELD_WEIGHTS,
    MAX_RETRIES,
    ProblemRelevanceRetrieval,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", action="append", default=[], help="Open research question. May be repeated.")
    parser.add_argument("--seed-id", action="append", default=[], help="Seed arXiv ID. May be repeated.")
    parser.add_argument("--seed-id-file", help="File with one arXiv ID per line.")
    parser.add_argument("--seed-registry", help="candidate-registry.json to pull seeds from by status.")
    parser.add_argument("--seed-status", action="append", default=[],
                        help="Registry status treated as a seed. May be repeated; default accepted,full-text-queued,extracted.")
    parser.add_argument("--exclude-id-file", action="append", default=[],
                        help="File of arXiv IDs to exclude from results (e.g. papers already read in the review).")
    parser.add_argument("--rounds", type=int, default=2, help="Citation-expansion rounds.")
    parser.add_argument("--direction", choices=["references", "citations", "both"], default="both")
    parser.add_argument("--max-per-seed-per-direction", type=int, default=200, help="Per-request neighbor cap (API max 1000).")
    parser.add_argument("--min-shared-seeds", type=int, default=None,
                        help="Candidates must connect to at least this many seeds. Default: 2 if >=2 seeds, else 1.")
    parser.add_argument("--max-total-candidates", type=int, default=400, help="Cap on the corpus before retrieval.")
    parser.add_argument("--top-k-per-round", type=int, default=20, help="Candidates carried forward as next round's seeds.")
    parser.add_argument("--max-fulltext-per-round", type=int, default=40, help="Cap on arXiv HTML judgment-surface fetches per round.")
    parser.add_argument("--target-retrieved", type=int, default=50, help="How many papers to emit after BM25 retrieval.")
    parser.add_argument("--min-year", type=int, default=None, help="Drop papers published before this year (inclusive).")
    parser.add_argument("--require-terms", default=None,
                        help="Comma-separated terms; keep a candidate only if at least one appears (case-insensitive) in title+abstract.")
    parser.add_argument("--must-terms", default=None,
                        help="Comma-separated terms; a candidate is DROPPED unless at least one appears in title+abstract.")
    parser.add_argument("--field-weights", default=DEFAULT_FIELD_WEIGHTS,
                        help="Comma-separated field=weight for BM25 multi-field scoring.")
    parser.add_argument("--output", help="Retrieved JSON. Defaults to stdout.")
    parser.add_argument("--markdown-output", help="Retrieval table + explanation Markdown.")
    parser.add_argument("--sleep-seconds", type=float, default=1.0, help="Delay between network phases.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per request. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0)
    parser.add_argument("--retry-max-seconds", type=float, default=60.0)
    parser.add_argument("--fail-fast", action="store_true", help="Abort on first failed request.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR, help="arXiv HTML cache directory.")
    parser.add_argument("--user-agent", default="embodied-ai-literature-hub/1.0 (local research workflow)")
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to S2_API_KEY env var.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    retrieval = ProblemRelevanceRetrieval(
        question=args.question,
        seed_id=args.seed_id,
        seed_id_file=args.seed_id_file,
        seed_registry=args.seed_registry,
        seed_status=args.seed_status,
        exclude_id_file=args.exclude_id_file,
        rounds=args.rounds,
        direction=args.direction,
        max_per_seed_per_direction=args.max_per_seed_per_direction,
        min_shared_seeds=args.min_shared_seeds,
        max_total_candidates=args.max_total_candidates,
        top_k_per_round=args.top_k_per_round,
        max_fulltext_per_round=args.max_fulltext_per_round,
        target_retrieved=args.target_retrieved,
        min_year=args.min_year,
        require_terms=args.require_terms,
        must_terms=args.must_terms,
        field_weights=args.field_weights,
        output=args.output,
        markdown_output=args.markdown_output,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        cache_dir=args.cache_dir,
        user_agent=args.user_agent,
        api_key=args.api_key or os.environ.get("S2_API_KEY"),
    )
    return retrieval.run()


if __name__ == "__main__":
    sys.exit(main())
