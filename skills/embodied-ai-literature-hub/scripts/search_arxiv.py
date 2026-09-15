#!/usr/bin/env python3
"""CLI: search arXiv through the official Atom API and emit normalized JSON.

Library API lives in embodied_learning/search/arxiv.py (ArxivSearch). This entry owns only
argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.search.arxiv import MAX_RETRIES, ArxivSearch, load_queries  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", action="append", help="Raw arXiv search_query string. May be repeated.")
    parser.add_argument("--query-file", help="JSON file with {'queries': [{'label': str, 'query': str}]}.")
    parser.add_argument("--start-date", required=True, help="Inclusive YYYY-MM-DD submitted date.")
    parser.add_argument("--end-date", required=True, help="Inclusive YYYY-MM-DD submitted date.")
    parser.add_argument("--max-results", type=int, default=25, help="Results per query for this discovery batch.")
    parser.add_argument("--batch-label", help="Stable round label stored for candidate-registry saturation analysis.")
    parser.add_argument("--sort-by", default="submittedDate", choices=["relevance", "lastUpdatedDate", "submittedDate"])
    parser.add_argument("--sort-order", default="descending", choices=["ascending", "descending"])
    parser.add_argument("--sleep-seconds", type=float, default=3.0, help="Delay between multiple API requests.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per query after transient failures. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0, help="Base wait before retrying transient failures.")
    parser.add_argument("--retry-max-seconds", type=float, default=60.0, help="Maximum wait before a single retry.")
    parser.add_argument("--fail-fast", action="store_true", help="Abort on the first failed query.")
    parser.add_argument(
        "--user-agent",
        default="embodied-ai-literature-hub/1.0 (local research workflow)",
        help="HTTP User-Agent sent to arXiv.",
    )
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    search = ArxivSearch(
        start_date=args.start_date,
        end_date=args.end_date,
        max_results=args.max_results,
        batch_label=args.batch_label or "",
        sort_by=args.sort_by,
        sort_order=args.sort_order,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        user_agent=args.user_agent,
        output=args.output,
    )
    return search.run(load_queries(queries=args.query, query_file=args.query_file))


if __name__ == "__main__":
    sys.exit(main())
