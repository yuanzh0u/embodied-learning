#!/usr/bin/env python3
"""Search Semantic Scholar (Graph API) and emit arXiv-search-compatible JSON.

Library API: :class:`SemanticScholarSearch` (batch execution) plus the
module-level helpers (query loading, retry/backoff, cache, response parsing).
The CLI surface owns argument parsing and lives in the skill entry
``skills/embodied-ai-literature-hub/scripts/search_semantic_scholar.py``.

The zero-sleep metadata-search counterpart to ``src/search/arxiv.py``:
responses are cached to disk (shared with the citation-expansion library),
queries run with a small inter-query interval (0.1s default) instead of
arXiv's 3s politeness delay, and transient 429/5xx responses back off
exponentially, honoring ``Retry-After``.

Only papers with an arXiv crosswalk (``externalIds.ArXiv``) are emitted — the
download pipeline keys on arXiv IDs. Skipped entries are counted in the output,
never silently dropped.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
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


class SemanticScholarSearch:
    """One batch of labeled Semantic Scholar metadata searches with retry/backoff.

    Options are explicit constructor parameters (the CLI entry translates
    argparse into these); call :meth:`run` with the query list.
    """

    def __init__(
        self,
        *,
        start_date: str,
        end_date: str,
        max_results: int = 25,
        batch_label: str = "",
        sort_by: str = "relevance",
        sort_order: str = "descending",
        sleep_seconds: float = 0.1,
        timeout: float = 20.0,
        retries: int = MAX_RETRIES,
        retry_base_seconds: float = 5.0,
        retry_max_seconds: float = 60.0,
        fail_fast: bool = False,
        api_key: str | None = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
        no_cache: bool = False,
        user_agent: str = "embodied-ai-literature-hub/1.0 (local research workflow)",
        output: str | None = None,
    ) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.max_results = max_results
        self.batch_label = batch_label
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.sleep_seconds = sleep_seconds
        self.timeout = timeout
        self.retries = retries
        self.retry_base_seconds = retry_base_seconds
        self.retry_max_seconds = retry_max_seconds
        self.fail_fast = fail_fast
        self.api_key = api_key or os.environ.get("S2_API_KEY")
        self.cache_dir = cache_dir
        self.no_cache = no_cache
        self.user_agent = user_agent
        self.output = output

    def run(self, queries: list[dict[str, str]]) -> int:
        """Execute every query, dedupe by arXiv ID, and write/print the JSON batch."""
        papers_by_id: dict[str, dict[str, object]] = {}
        query_results = []
        total_excluded = 0
        for index, item in enumerate(queries):
            try:
                papers, excluded = self.collect_papers(item["query"], item["label"])
                query_results.append({"label": item["label"], "query": item["query"], "result_count": len(papers)})
                total_excluded += excluded
            except Exception as exc:  # pragma: no cover - network dependent
                if self.fail_fast:
                    raise
                papers = []
                query_results.append({"label": item["label"], "query": item["query"], "result_count": 0, "error": str(exc)})
            for paper in papers:
                existing = papers_by_id.setdefault(str(paper["arxiv_id"]), paper)
                if existing is not paper:
                    labels = set(str(existing.get("query_label", "")).split(","))
                    labels.add(item["label"])
                    existing["query_label"] = ",".join(sorted(label for label in labels if label))
            if index < len(queries) - 1 and self.sleep_seconds > 0:
                time.sleep(self.sleep_seconds)

        output = {
            "generated_at": stable_now(),
            "batch": self.batch_label or "",
            "api": f"{API_BASE}/paper/search",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order,
            "queries": query_results,
            "paper_count": len(papers_by_id),
            "excluded_no_arxiv_id": total_excluded,
            "papers": list(papers_by_id.values()),
        }
        rendered = json.dumps(output, ensure_ascii=False, indent=2)
        if self.output:
            with open(self.output, "w", encoding="utf-8") as handle:
                handle.write(rendered + "\n")
        else:
            print(rendered)
        return 0

    def fetch(self, url: str) -> bytes:
        headers = {"User-Agent": self.user_agent}
        api_key = self.api_key or os.environ.get("S2_API_KEY")
        if api_key:
            headers["x-api-key"] = api_key
        request = urllib.request.Request(url, headers=headers)
        last_error: Exception | None = None
        attempts = 0
        retries = bounded_retries(self.retries)
        for attempt in range(retries + 1):
            attempts = attempt + 1
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return response.read()
            except Exception as exc:  # pragma: no cover - network dependent
                last_error = exc
                if attempt < retries and is_retryable(exc):
                    time.sleep(retry_wait_seconds(exc, attempt, self.retry_base_seconds, self.retry_max_seconds))
                    continue
                break
        raise RuntimeError(f"Semantic Scholar request failed after {attempts} attempt(s): {last_error}") from last_error

    def fetch_cached(self, url: str) -> bytes:
        cached = read_cache(self.cache_dir, url, not self.no_cache)
        if cached is not None:
            return cached
        payload = self.fetch(url)
        write_cache(self.cache_dir, url, payload, not self.no_cache)
        return payload

    def collect_papers(self, query: str, label: str) -> tuple[list[dict[str, object]], int]:
        """Page through S2 search results for one query.

        Returns (papers in window, count of hits excluded for lacking an arXiv ID).
        Entries outside the publication-date window are neither emitted nor counted
        as exclusions — the window is a scope, not a crosswalk failure.
        """
        start, end = parse_date_window(self.start_date, self.end_date)
        effective = f"{query} publicationDate:{start}..{end}"
        papers: dict[str, dict[str, object]] = {}
        excluded_no_arxiv = 0
        offset = 0
        remaining = max(1, self.max_results)
        while remaining > 0:
            limit = min(PAGE_SIZE, remaining)
            payload = self.fetch_cached(build_search_url(query, offset, limit))
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
            remaining = max(1, self.max_results) - len(papers)
            if len(entries) < limit:
                break
        ordered = list(papers.values())
        if self.sort_by == "pub_date":
            ordered.sort(key=lambda item: str(item["published"]), reverse=self.sort_order == "descending")
        return ordered, excluded_no_arxiv


def stable_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load_queries(queries: list[str] | None = None, query_file: str | None = None) -> list[dict[str, str]]:
    """Merge query-file entries with repeated --query values (CLI-side helper)."""
    queries = list(queries or [])
    if query_file:
        with open(query_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        existing = queries
        queries = []
        for index, item in enumerate(data.get("queries", []), start=1):
            query = item.get("query")
            if query:
                queries.append({"label": item.get("label", f"query-{index}"), "query": query})
        queries.extend(existing)
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


def retry_wait_seconds(exc: Exception, attempt: int, retry_base_seconds: float, retry_max_seconds: float) -> float:
    retry_after = retry_after_seconds(exc)
    if retry_after is not None:
        return max(0.0, min(retry_after, retry_max_seconds))
    return max(0.0, min(retry_base_seconds * (2**attempt), retry_max_seconds))


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
