#!/usr/bin/env python3
"""Parse arXiv paper candidates from Browser-exported text, HTML, or JSON."""

from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
import re
import sys
from pathlib import Path
from typing import Any

ARXIV_ID_RE = re.compile(
    r"(?:arxiv\.org/(?:abs|html|pdf)/|arXiv[:\s]*)(\d{4}\.\d{4,5})(?:v\d+)?",
    flags=re.IGNORECASE,
)
BARE_VERSIONED_RE = re.compile(r"\b(\d{4}\.\d{4,5})v\d+\b", flags=re.IGNORECASE)
NEXT_ARXIV_TOKEN_RE = re.compile(
    r"(?:arxiv\.org/(?:abs|html|pdf)/|arXiv[:\s]*|\b)(\d{4}\.\d{4,5})(?:v\d+)?",
    flags=re.IGNORECASE,
)
MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg", "math"}:
            self.skip_depth += 1
        if tag in {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg", "math"} and self.skip_depth:
            self.skip_depth -= 1
        if tag in {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self.parts.append(text + " ")

    def text(self) -> str:
        lines = [" ".join(line.split()) for line in "".join(self.parts).splitlines()]
        return "\n".join(line for line in lines if line).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Browser-exported JSON, HTML, text, or '-' for stdin.")
    parser.add_argument("--start-date", help="Inclusive YYYY-MM-DD filter.")
    parser.add_argument("--end-date", help="Inclusive YYYY-MM-DD filter.")
    parser.add_argument("--source-label", default="browser-fallback")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args()


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def html_to_text(value: str) -> str:
    parser = TextExtractor()
    parser.feed(value)
    text = parser.text()
    return text or " ".join(value.split())


def collect_raw(value: Any) -> tuple[str, str, list[dict[str, str]]]:
    if isinstance(value, dict):
        source_url = str(value.get("source_url") or value.get("url") or "")
        chunks: list[str] = []
        links: list[dict[str, str]] = []
        for key in ("title", "page_text", "text", "dom", "domSnapshot", "html"):
            if value.get(key):
                chunks.append(str(value[key]))
        for item in value.get("links", []) if isinstance(value.get("links"), list) else []:
            if not isinstance(item, dict):
                continue
            href = str(item.get("href") or "")
            text = str(item.get("text") or item.get("title") or "")
            links.append({"href": href, "text": text})
            chunks.append(f"{text} {href}")
        return "\n".join(chunks), source_url, links
    if isinstance(value, list):
        chunks = []
        links = []
        for item in value:
            raw, _, item_links = collect_raw(item)
            chunks.append(raw)
            links.extend(item_links)
        return "\n".join(chunks), "", links
    return str(value), "", []


def parse_payload(raw: str) -> tuple[str, str, list[dict[str, str]]]:
    stripped = raw.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            return collect_raw(json.loads(raw))
        except json.JSONDecodeError:
            pass
    return raw, "", []


def normalized_text(raw: str) -> str:
    if "<html" in raw[:2000].lower() or "</" in raw:
        return html_to_text(raw)
    lines = [" ".join(line.split()) for line in raw.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def parse_date(value: str) -> str | None:
    value = value.strip().replace(",", "")
    iso = re.search(r"\b(20\d{2})-(\d{2})-(\d{2})\b", value)
    if iso:
        return f"{iso.group(1)}-{iso.group(2)}-{iso.group(3)}"
    weekday = re.search(
        r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+"
        r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
        r"Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+(\d{1,2})(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?\s+(20\d{2})\b",
        value,
        flags=re.IGNORECASE,
    )
    if weekday:
        month = MONTHS[weekday.group(1).lower()]
        return dt.date(int(weekday.group(3)), month, int(weekday.group(2))).isoformat()
    named = re.search(
        r"\b(\d{1,2})\s+"
        r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
        r"Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+(20\d{2})\b",
        value,
        flags=re.IGNORECASE,
    )
    if not named:
        named = re.search(
            r"\b"
            r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
            r"Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
            r"\s+(\d{1,2})\s+(20\d{2})\b",
            value,
            flags=re.IGNORECASE,
        )
        if named:
            month = MONTHS[named.group(1).lower()]
            return dt.date(int(named.group(3)), month, int(named.group(2))).isoformat()
        return None
    month = MONTHS[named.group(2).lower()]
    return dt.date(int(named.group(3)), month, int(named.group(1))).isoformat()


def date_candidates(context: str) -> list[str]:
    results: list[str] = []
    seen: set[str] = set()
    patterns = [
        r"\b20\d{2}-\d{2}-\d{2}\b",
        r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?\s+20\d{2}\b",
        r"\b\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?),?\s+20\d{2}\b",
        r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+20\d{2}\b",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, context, flags=re.IGNORECASE):
            parsed = parse_date(match.group(0))
            if parsed and parsed not in seen:
                seen.add(parsed)
                results.append(parsed)
    return results


def infer_month(arxiv_id: str) -> str | None:
    match = re.match(r"^(\d{2})(\d{2})\.", arxiv_id)
    if not match:
        return None
    year = 2000 + int(match.group(1))
    month = int(match.group(2))
    if not 1 <= month <= 12:
        return None
    return f"{year:04d}-{month:02d}"


def in_window(dates: list[str], inferred: str | None, start: str | None, end: str | None) -> bool | None:
    if not start or not end:
        return None
    start_date = dt.date.fromisoformat(start)
    end_date = dt.date.fromisoformat(end)
    if dates:
        submitted_date = dt.date.fromisoformat(dates[0])
        return start_date <= submitted_date <= end_date
    if not inferred:
        return None
    year, month = (int(part) for part in inferred.split("-"))
    month_start = dt.date(year, month, 1)
    month_end = dt.date(year + int(month == 12), 1 if month == 12 else month + 1, 1) - dt.timedelta(days=1)
    return not (month_end < start_date or month_start > end_date)


def context_summary(text: str, position: int, size: int = 420) -> str:
    left = max(0, position - size)
    right = min(len(text), position + size)
    return " ".join(text[left:right].split())


def nearby_date_context(text: str, start: int, end: int) -> str:
    right = min(len(text), end + 180)
    newline = text.find("\n", end)
    if newline >= 0:
        right = min(right, newline)
    next_id = NEXT_ARXIV_TOKEN_RE.search(text, end)
    if next_id:
        right = min(right, next_id.start())
    return text[start:right]


def candidate_records(raw: str, source_links: list[dict[str, str]], start: str | None, end: str | None) -> list[dict[str, Any]]:
    text = normalized_text(raw)
    by_id: dict[str, dict[str, Any]] = {}

    def add(arxiv_id: str, context: str, source: str, date_context: str | None = None) -> None:
        record = by_id.setdefault(
            arxiv_id,
            {
                "arxiv_id": arxiv_id,
                "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
                "html_url": f"https://arxiv.org/html/{arxiv_id}",
                "source_type": "browser_export",
                "source_hits": [],
                "date_candidates": [],
                "inferred_month": infer_month(arxiv_id),
                "in_window": None,
                "context": "",
            },
        )
        if source not in record["source_hits"]:
            record["source_hits"].append(source)
        if not record["context"] or len(context) > len(record["context"]):
            record["context"] = context[:1200]
        for parsed in date_candidates(date_context or context):
            if parsed not in record["date_candidates"]:
                record["date_candidates"].append(parsed)

    for match in ARXIV_ID_RE.finditer(raw):
        add(
            match.group(1),
            context_summary(raw, match.start()),
            "raw-url-or-arxiv-token",
            nearby_date_context(raw, match.start(), match.end()),
        )
    for match in BARE_VERSIONED_RE.finditer(raw):
        add(
            match.group(1),
            context_summary(raw, match.start()),
            "versioned-id-token",
            nearby_date_context(raw, match.start(), match.end()),
        )
    for match in ARXIV_ID_RE.finditer(text):
        add(
            match.group(1),
            context_summary(text, match.start()),
            "visible-text",
            nearby_date_context(text, match.start(), match.end()),
        )
    for link in source_links:
        href = link.get("href", "")
        link_text = link.get("text", "")
        for match in ARXIV_ID_RE.finditer(href):
            fragment = f"{link_text} {href}".strip()
            add(match.group(1), fragment, "browser-link", fragment)

    for record in by_id.values():
        record["in_window"] = in_window(record["date_candidates"], record["inferred_month"], start, end)
        record["submitted_date_candidate"] = record["date_candidates"][0] if record["date_candidates"] else None
    return sorted(
        by_id.values(),
        key=lambda item: (item["in_window"] is not True, item.get("inferred_month") or "", item["arxiv_id"]),
    )


def main() -> int:
    args = parse_args()
    payload = read_input(args.input)
    raw, payload_source_url, links = parse_payload(payload)
    source_url = args.source_url or payload_source_url
    candidates = candidate_records(raw, links, args.start_date, args.end_date)
    output = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_label": args.source_label,
        "source_url": source_url,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
