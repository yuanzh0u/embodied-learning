#!/usr/bin/env python3
"""CLI: expand candidates via S2 citation/reference neighborhoods (coupling/co-citation).

Library API lives in src/search/citation_expansion.py (CitationExpansion).
This entry owns only argument parsing and dispatch.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.citation_expansion import DEFAULT_S2_CACHE_DIR, MAX_RETRIES, CitationExpansion  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-id", action="append", default=[], help="Seed arXiv ID. May be repeated.")
    parser.add_argument("--seed-id-file", help="File with one arXiv ID per line.")
    parser.add_argument("--seed-registry", help="candidate-registry.json to pull seeds from by status.")
    parser.add_argument(
        "--seed-status",
        action="append",
        default=[],
        help="Registry status treated as a seed. May be repeated; default accepted,full-text-queued,extracted.",
    )
    parser.add_argument("--direction", choices=["references", "citations", "both"], default="both")
    parser.add_argument("--max-per-seed-per-direction", type=int, default=200, help="Per-request neighbor cap (API max 1000).")
    parser.add_argument(
        "--min-shared-seeds",
        type=int,
        default=None,
        help="Candidates must connect to at least this many seeds. Default: 2 if >=2 seeds, else 1.",
    )
    parser.add_argument("--max-total-candidates", type=int, default=200, help="Cap after ranking by shared-seed count.")
    parser.add_argument("--include-below-threshold-output", help="Also write candidates below the shared-seed threshold here.")
    parser.add_argument("--start-date", help="Optional YYYY-MM-DD; coarse year-level filter on discovered papers.")
    parser.add_argument("--end-date", help="Optional YYYY-MM-DD; coarse year-level filter on discovered papers.")
    parser.add_argument("--top-terms", type=int, default=20)
    parser.add_argument("--min-doc-frequency", type=int, default=2)
    parser.add_argument("--extra-stopwords-file", help="Extra stopwords, one per line.")
    parser.add_argument("--batch-label", help="Stable round label stored for candidate-registry saturation analysis.")
    parser.add_argument("--output", help="Candidate-registry-compatible JSON. Defaults to stdout.")
    parser.add_argument("--graph-output", help="Citation edges + seed-similarity JSON.")
    parser.add_argument("--dynamic-output", help="query-planner --dynamic-file compatible JSON.")
    parser.add_argument("--sleep-seconds", type=float, default=0.1, help="Delay between seeds.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per request after transient failures. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0, help="Base wait before retrying transient failures.")
    parser.add_argument("--retry-max-seconds", type=float, default=60.0, help="Maximum wait before a single retry.")
    parser.add_argument("--fail-fast", action="store_true", help="Abort on the first failed seed/direction request.")
    parser.add_argument(
        "--user-agent",
        default="embodied-ai-literature-hub/1.0 (local research workflow)",
        help="HTTP User-Agent sent to Semantic Scholar.",
    )
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to the S2_API_KEY env var.")
    parser.add_argument(
        "--cache-dir",
        default=DEFAULT_S2_CACHE_DIR,
        help="Semantic Scholar response cache, shared with search_semantic_scholar.py.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Bypass the response cache for reads and writes.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    expansion = CitationExpansion(
        seed_id=args.seed_id,
        seed_id_file=args.seed_id_file,
        seed_registry=args.seed_registry,
        seed_status=args.seed_status,
        direction=args.direction,
        max_per_seed_per_direction=args.max_per_seed_per_direction,
        min_shared_seeds=args.min_shared_seeds,
        max_total_candidates=args.max_total_candidates,
        include_below_threshold_output=args.include_below_threshold_output,
        start_date=args.start_date,
        end_date=args.end_date,
        top_terms=args.top_terms,
        min_doc_frequency=args.min_doc_frequency,
        extra_stopwords_file=args.extra_stopwords_file,
        batch_label=args.batch_label,
        output=args.output,
        graph_output=args.graph_output,
        dynamic_output=args.dynamic_output,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        user_agent=args.user_agent,
        api_key=args.api_key or os.environ.get("S2_API_KEY"),
        cache_dir=args.cache_dir,
        no_cache=args.no_cache,
    )
    return expansion.run()


if __name__ == "__main__":
    sys.exit(main())
