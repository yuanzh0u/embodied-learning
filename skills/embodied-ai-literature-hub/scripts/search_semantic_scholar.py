#!/usr/bin/env python3
"""CLI: search the Semantic Scholar Graph API and emit arXiv-compatible JSON.

Library API lives in src/search/semantic_scholar.py (SemanticScholarSearch).
This entry owns only argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.semantic_scholar import DEFAULT_CACHE_DIR, MAX_RETRIES, SemanticScholarSearch, load_queries  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", action="append", help="Search query string. May be repeated.")
    parser.add_argument("--query-file",
                        help="JSON file with {'queries': [{'label': str, 'query': str}]}, the planner contract.")
    parser.add_argument("--start-date", required=True, help="Inclusive YYYY-MM-DD publication date.")
    parser.add_argument("--end-date", required=True, help="Inclusive YYYY-MM-DD publication date.")
    parser.add_argument("--max-results", type=int, default=25, help="Results per query for this discovery batch.")
    parser.add_argument("--batch-label", help="Stable round label stored for candidate-registry saturation analysis.")
    parser.add_argument("--sort-by", default="relevance", choices=["relevance", "pub_date"],
                        help="relevance uses S2 ordering; pub_date sorts client-side after fetch.")
    parser.add_argument("--sort-order", default="descending", choices=["ascending", "descending"],
                        help="Only applied with --sort-by pub_date.")
    parser.add_argument("--sleep-seconds", type=float, default=0.1,
                        help="Delay between queries; the S2 pool tolerates small intervals.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per request after transient failures. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0, help="Base wait before retrying transient failures.")
    parser.add_argument("--retry-max-seconds", type=float, default=60.0, help="Maximum wait before a single retry.")
    parser.add_argument("--fail-fast", action="store_true", help="Abort on the first failed query.")
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to the S2_API_KEY env var.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR,
                        help="Response cache (shared with expand_via_citations.py).")
    parser.add_argument("--no-cache", action="store_true", help="Bypass the response cache for reads and writes.")
    parser.add_argument("--user-agent",
                        default="embodied-ai-literature-hub/1.0 (local research workflow)",
                        help="HTTP User-Agent sent to Semantic Scholar.")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    search = SemanticScholarSearch(
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
        api_key=args.api_key,
        cache_dir=args.cache_dir,
        no_cache=args.no_cache,
        user_agent=args.user_agent,
        output=args.output,
    )
    return search.run(load_queries(queries=args.query, query_file=args.query_file))


if __name__ == "__main__":
    sys.exit(main())
