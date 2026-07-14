#!/usr/bin/env python3
"""Search arXiv through the official Atom API and emit normalized JSON."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API_URL = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
MAX_RETRIES = 3
TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


def yyyymmdd(value: str, end: bool = False) -> str:
    parsed = dt.datetime.strptime(value, "%Y-%m-%d")
    suffix = "2359" if end else "0000"
    return parsed.strftime("%Y%m%d") + suffix


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


def retry_wait_seconds(exc: Exception, attempt: int, args: argparse.Namespace) -> float:
    retry_after = retry_after_seconds(exc)
    if retry_after is not None:
        return max(0.0, min(retry_after, args.retry_max_seconds))
    return max(0.0, min(args.retry_base_seconds * (2 ** attempt), args.retry_max_seconds))


def fetch(query: str, args: argparse.Namespace) -> bytes:
    params = {
        "search_query": query,
        "start": "0",
        "max_results": str(args.max_results),
        "sortBy": args.sort_by,
        "sortOrder": args.sort_order,
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": args.user_agent},
    )
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
    raise RuntimeError(f"arXiv request failed after {attempts} attempt(s): {last_error}") from last_error


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


def main() -> int:
    args = parse_args()
    queries = load_queries(args)
    papers_by_id: dict[str, dict[str, object]] = {}
    query_results = []
    for index, item in enumerate(queries):
        effective = with_date_filter(item["query"], args.start_date, args.end_date)
        try:
            payload = fetch(effective, args)
            papers = parse_feed(payload, item["label"], effective)
            query_results.append({"label": item["label"], "query": item["query"], "result_count": len(papers)})
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
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "batch": args.batch_label or "",
        "api": API_URL,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "sort_by": args.sort_by,
        "sort_order": args.sort_order,
        "queries": query_results,
        "paper_count": len(papers_by_id),
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
