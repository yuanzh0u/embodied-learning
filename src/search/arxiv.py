#!/usr/bin/env python3
"""Search arXiv through the official Atom API and emit normalized candidate JSON.

Library API: :class:`ArxivSearch` (batch execution) plus the module-level
helpers (query loading, retry/backoff, Atom feed parsing). The CLI surface
owns argument parsing and lives in the skill entry
``skills/embodied-ai-literature-hub/scripts/search_arxiv.py``.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API_URL = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
MAX_RETRIES = 3
TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}


class ArxivSearch:
    """One batch of labeled arXiv Atom API queries with retry/backoff.

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
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
        sleep_seconds: float = 3.0,
        timeout: float = 20.0,
        retries: int = MAX_RETRIES,
        retry_base_seconds: float = 5.0,
        retry_max_seconds: float = 60.0,
        fail_fast: bool = False,
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
        self.user_agent = user_agent
        self.output = output

    def run(self, queries: list[dict[str, str]]) -> int:
        """Execute every query, dedupe by arXiv ID, and write/print the JSON batch."""
        papers_by_id: dict[str, dict[str, object]] = {}
        query_results = []
        for index, item in enumerate(queries):
            effective = with_date_filter(item["query"], self.start_date, self.end_date)
            try:
                payload = self.fetch(effective)
                papers = parse_feed(payload, item["label"], effective)
                query_results.append({"label": item["label"], "query": item["query"], "result_count": len(papers)})
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
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "batch": self.batch_label or "",
            "api": API_URL,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order,
            "queries": query_results,
            "paper_count": len(papers_by_id),
            "papers": list(papers_by_id.values()),
        }
        rendered = json.dumps(output, ensure_ascii=False, indent=2)
        if self.output:
            with open(self.output, "w", encoding="utf-8") as handle:
                handle.write(rendered + "\n")
        else:
            print(rendered)
        return 0

    def fetch(self, query: str) -> bytes:
        params = {
            "search_query": query,
            "start": "0",
            "max_results": str(self.max_results),
            "sortBy": self.sort_by,
            "sortOrder": self.sort_order,
        }
        url = API_URL + "?" + urllib.parse.urlencode(params)
        request = urllib.request.Request(
            url,
            headers={"User-Agent": self.user_agent},
        )
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
                    time.sleep(self.retry_wait_seconds(exc, attempt))
                    continue
                break
        raise RuntimeError(f"arXiv request failed after {attempts} attempt(s): {last_error}") from last_error

    def retry_wait_seconds(self, exc: Exception, attempt: int) -> float:
        retry_after = retry_after_seconds(exc)
        if retry_after is not None:
            return max(0.0, min(retry_after, self.retry_max_seconds))
        return max(0.0, min(self.retry_base_seconds * (2 ** attempt), self.retry_max_seconds))


def load_queries(queries: list[str] | None = None, query_file: str | None = None) -> list[dict[str, str]]:
    """Merge query-file entries with repeated --query values (CLI-side helper)."""
    merged: list[dict[str, str]] = []
    if query_file:
        with open(query_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        for index, item in enumerate(data.get("queries", []), start=1):
            query = item.get("query")
            if query:
                merged.append({"label": item.get("label", f"query-{index}"), "query": query})
    for index, query in enumerate(queries or [], start=1):
        merged.append({"label": f"cli-{index}", "query": query})
    if not merged:
        raise SystemExit("Provide --query or --query-file.")
    return merged


def yyyymmdd(value: str, end: bool = False) -> str:
    parsed = dt.datetime.strptime(value, "%Y-%m-%d")
    suffix = "2359" if end else "0000"
    return parsed.strftime("%Y%m%d") + suffix


def with_date_filter(query: str, start_date: str, end_date: str) -> str:
    start = yyyymmdd(start_date)
    end = yyyymmdd(end_date, end=True)
    return f"({query}) AND submittedDate:[{start} TO {end}]"


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


def text(element: ET.Element, name: str) -> str:
    found = element.find(ATOM + name)
    return " ".join((found.text or "").split()) if found is not None else ""


def arxiv_ids(entry_id: str) -> tuple[str, str]:
    versioned = entry_id.rsplit("/", 1)[-1]
    base = re.sub(r"v\d+$", "", versioned)
    return base, versioned


def parse_feed(payload: bytes, query_label: str, effective_query: str) -> list[dict[str, object]]:
    root = ET.fromstring(payload)
    papers: list[dict[str, object]] = []
    for entry in root.findall(ATOM + "entry"):
        entry_id = text(entry, "id")
        arxiv_id, versioned_id = arxiv_ids(entry_id)
        authors = [text(author, "name") for author in entry.findall(ATOM + "author")]
        pdf_url = ""
        for link in entry.findall(ATOM + "link"):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href", "")
        categories = [cat.attrib.get("term", "") for cat in entry.findall(ATOM + "category") if cat.attrib.get("term")]
        papers.append(
            {
                "arxiv_id": arxiv_id,
                "versioned_id": versioned_id,
                "title": text(entry, "title"),
                "authors": authors,
                "published": text(entry, "published"),
                "updated": text(entry, "updated"),
                "summary": text(entry, "summary"),
                "categories": categories,
                "abs_url": entry_id,
                "pdf_url": pdf_url or f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                "query_label": query_label,
                "effective_query": effective_query,
            }
        )
    return papers
