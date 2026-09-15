#!/usr/bin/env python3
"""Search Semantic Scholar (Graph API) and emit arXiv-search-compatible JSON.

The zero-sleep metadata-search counterpart to ``search_arxiv.py``: responses
are cached to disk (shared with ``expand_via_citations.py``), queries run with
a small inter-query interval (0.1s default) instead of arXiv's 3s politeness
delay, and transient 429/5xx responses back off exponentially, honoring
``Retry-After``.

Only papers with an arXiv crosswalk (``externalIds.ArXiv``) are emitted — the
download pipeline keys on arXiv IDs. Skipped entries are counted in the output,
never silently dropped.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://api.semanticscholar.org/graph/v1"
SEARCH_FIELDS = "title,abstract,year,publicationDate,authors,externalIds,fieldsOfStudy,citationCount"
DEFAULT_CACHE_DIR = os.path.join(tempfile.gettempdir(), "embodied-ai-literature-hub", "s2")
MAX_RETRIES = 3
TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}
PAGE_SIZE = 100


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


def stable_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load_queries(args: argparse.Namespace) -> list[dict[str, str]]:
    queries: list[dict[str, str]] = []
    if args.query_file:
        with open(args.query_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        for index, item in enumerate(data.get("queries", []), start=1):
            query = item.get("query")
            if query:
                queries.append({"label": item.get("label", f"query-{index}"), "query": query})
    if args.query:
        for index, query in enumerate(args.query, start=1):
            queries.append({"label": f"cli-{index}", "query": query})
    if not queries:
        raise SystemExit("Provide --query or --query-file.")
    return queries


# ---------------------------------------------------------------------------
# Network: retry/backoff mirrors search_arxiv.py so both backends behave the
# same under rate limiting; only URL construction and response parsing differ.
# ---------------------------------------------------------------------------


def bounded_retries(value: int) -> int:
    return max(0, min(value, MAX_RETRIES))


def retry_after_seconds(exc: Exception) -> float | None:
    if not isinstance(exc, urllib.error.HTTPError):
        return None
    retry_after = exc.headers.get("Retry-After") if exc.headers else None
    if not retry_after:
        return None
    try:
        parsed = float(retry_after)
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


def is_retryable(exc: Exception) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in TRANSIENT_HTTP_CODES
    return isinstance(exc, (TimeoutError, urllib.error.URLError, OSError))


def retry_wait_seconds(exc: Exception, attempt: int, args: argparse.Namespace) -> float:
    retry_after = retry_after_seconds(exc)
    if retry_after is not None:
        return max(0.0, min(retry_after, args.retry_max_seconds))
    return max(0.0, min(args.retry_base_seconds * (2**attempt), args.retry_max_seconds))


def build_search_url(query: str, offset: int, limit: int) -> str:
    params = {
        "query": query,
        "fields": SEARCH_FIELDS,
        "limit": str(limit),
        "offset": str(offset),
    }
    return f"{API_BASE}/paper/search?" + urllib.parse.urlencode(params)


def cache_key(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()


def cache_path(cache_dir: str, url: str) -> Path:
    return Path(cache_dir).expanduser() / f"{cache_key(url)}.json"


def read_cache(cache_dir: str, url: str, enabled: bool) -> bytes | None:
    if not enabled:
        return None
    path = cache_path(cache_dir, url)
    if path.is_file() and path.stat().st_size > 0:
        return path.read_bytes()
    return None


def write_cache(cache_dir: str, url: str, payload: bytes, enabled: bool) -> None:
    if not enabled:
        return
    path = cache_path(cache_dir, url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def fetch(url: str, args: argparse.Namespace) -> bytes:
    headers = {"User-Agent": args.user_agent}
    api_key = getattr(args, "api_key", None) or os.environ.get("S2_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key
    request = urllib.request.Request(url, headers=headers)
    last_error: Exception | None = None
    attempts = 0
    retries = bounded_retries(args.retries)
    for attempt in range(retries + 1):
        attempts = attempt + 1
        try:
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                return response.read()
        except Exception as exc:  # pragma: no cover - network dependent
            last_error = exc
            if attempt < retries and is_retryable(exc):
                time.sleep(retry_wait_seconds(exc, attempt, args))
                continue
            break
    raise RuntimeError(f"Semantic Scholar request failed after {attempts} attempt(s): {last_error}") from last_error


def fetch_cached(url: str, args: argparse.Namespace) -> bytes:
    cached = read_cache(args.cache_dir, url, not args.no_cache)
    if cached is not None:
        return cached
    payload = fetch(url, args)
    write_cache(args.cache_dir, url, payload, not args.no_cache)
    return payload


# ---------------------------------------------------------------------------
# Pure logic: response -> paper records. No network access; unit-testable.
# ---------------------------------------------------------------------------


def parse_date_window(start_date: str, end_date: str) -> tuple[str, str]:
    start = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    end = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    return start.isoformat(), end.isoformat()


def in_window(publication_date: str, start: str, end: str) -> bool:
    if not publication_date:
        return False
    day = publication_date[:10]
    return start <= day <= end


def normalize_arxiv_id(value: object) -> str:
    raw = str(value or "").rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html")
    return re.sub(r"v\d+$", "", raw.strip())


def parse_paper(entry: dict, query_label: str, effective_query: str) -> dict[str, object] | None:
    """Map an S2 search hit to the search_arxiv.py paper shape.

    Returns None for entries without an arXiv crosswalk; callers count them.
    """
    external = entry.get("externalIds") or {}
    arxiv_id = normalize_arxiv_id(external.get("ArXiv"))
    if not arxiv_id:
        return None
    published = str(entry.get("publicationDate") or "")
    open_pdf = ((entry.get("openAccessPdf") or {}) if isinstance(entry.get("openAccessPdf"), dict) else {}).get("url") or ""
    authors = [
        str(author.get("name") or "")
        for author in entry.get("authors") or []
        if isinstance(author, dict) and author.get("name")
    ]
    return {
        "arxiv_id": arxiv_id,
        "versioned_id": arxiv_id,
        "title": " ".join(str(entry.get("title") or "").split()),
        "authors": authors,
        "published": published,
        "updated": published,
        "summary": " ".join(str(entry.get("abstract") or "").split()),
        "categories": [str(field) for field in entry.get("fieldsOfStudy") or [] if field],
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": open_pdf or f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "doi": str(external.get("DOI") or ""),
        "citation_count": int(entry.get("citationCount") or 0),
        "query_label": query_label,
        "effective_query": effective_query,
    }


def collect_papers(query: str, label: str, args: argparse.Namespace) -> tuple[list[dict[str, object]], int]:
    """Page through S2 search results for one query.

    Returns (papers in window, count of hits excluded for lacking an arXiv ID).
    Entries outside the publication-date window are neither emitted nor counted
    as exclusions — the window is a scope, not a crosswalk failure.
    """
    start, end = parse_date_window(args.start_date, args.end_date)
    effective = f"{query} publicationDate:{start}..{end}"
    papers: list[dict[str, object]] = {}
    excluded_no_arxiv = 0
    offset = 0
    remaining = max(1, args.max_results)
    while remaining > 0:
        limit = min(PAGE_SIZE, remaining)
        payload = fetch_cached(build_search_url(query, offset, limit), args)
        data = json.loads(payload.decode("utf-8"))
        entries = data.get("data") or []
        if not entries:
            break
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            paper = parse_paper(entry, label, effective)
            if paper is None:
                excluded_no_arxiv += 1
                continue
            if not in_window(str(paper["published"]), start, end):
                continue
            existing = papers.setdefault(str(paper["arxiv_id"]), paper)
            if existing is not paper:
                labels = set(str(existing.get("query_label", "")).split(","))
                labels.add(label)
                existing["query_label"] = ",".join(sorted(label for label in labels if label))
        offset += len(entries)
        remaining = max(1, args.max_results) - len(papers)
        if len(entries) < limit:
            break
    ordered = list(papers.values())
    if args.sort_by == "pub_date":
        ordered.sort(key=lambda item: str(item["published"]), reverse=args.sort_order == "descending")
    return ordered, excluded_no_arxiv


def main() -> int:
    args = parse_args()
    queries = load_queries(args)
    papers_by_id: dict[str, dict[str, object]] = {}
    query_results = []
    total_excluded = 0
    for index, item in enumerate(queries):
        try:
            papers, excluded = collect_papers(item["query"], item["label"], args)
            query_results.append({"label": item["label"], "query": item["query"], "result_count": len(papers)})
            total_excluded += excluded
        except Exception as exc:  # pragma: no cover - network dependent
            if args.fail_fast:
                raise
            papers = []
            query_results.append({"label": item["label"], "query": item["query"], "result_count": 0, "error": str(exc)})
        for paper in papers:
            existing = papers_by_id.setdefault(str(paper["arxiv_id"]), paper)
            if existing is not paper:
                labels = set(str(existing.get("query_label", "")).split(","))
                labels.add(item["label"])
                existing["query_label"] = ",".join(sorted(label for label in labels if label))
        if index < len(queries) - 1 and args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)

    output = {
        "generated_at": stable_now(),
        "batch": args.batch_label or "",
        "api": f"{API_BASE}/paper/search",
        "start_date": args.start_date,
        "end_date": args.end_date,
        "sort_by": args.sort_by,
        "sort_order": args.sort_order,
        "queries": query_results,
        "paper_count": len(papers_by_id),
        "excluded_no_arxiv_id": total_excluded,
        "papers": list(papers_by_id.values()),
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
