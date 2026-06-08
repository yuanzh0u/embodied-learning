#!/usr/bin/env python3
"""Fetch/cache arXiv HTML, extract readable text, term matches, and reference hints."""

from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_CACHE_DIR = os.path.join(
    os.environ.get("TMPDIR") or "/private/tmp",
    "embodied-ai-literature-hub",
    "html",
)


class TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.current_tag = ""
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        self.current_tag = tag.lower()
        if self.current_tag in {"script", "style", "noscript", "svg", "math"}:
            self.skip_depth += 1
        if self.current_tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n\n## ")
        elif self.current_tag in {"p", "div", "section", "article", "li", "tr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg", "math"} and self.skip_depth:
            self.skip_depth -= 1
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "tr"}:
            self.parts.append("\n")
        self.current_tag = ""

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self.parts.append(text + " ")

    def text(self) -> str:
        raw = "".join(self.parts)
        lines = [" ".join(line.split()) for line in raw.splitlines()]
        return "\n".join(line for line in lines if line).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", help="arXiv ID, with or without version.")
    parser.add_argument("--html-url", help="HTML URL. Defaults to https://arxiv.org/html/<paper-id>")
    parser.add_argument("--terms", help="Comma-separated terms to locate in extracted text.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-chars", type=int, default=0, help="0 means all extracted text.")
    parser.add_argument("--include-text", action="store_true", help="Include extracted text in JSON output.")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args()


def normalize_id(value: str) -> str:
    value = value.rsplit("/", 1)[-1]
    value = value.removesuffix(".html")
    return re.sub(r"v\d+$", "", value)


def html_url(args: argparse.Namespace) -> str:
    if args.html_url:
        return args.html_url
    if not args.paper_id:
        raise SystemExit("Provide --paper-id or --html-url.")
    return f"https://arxiv.org/html/{normalize_id(args.paper_id)}"


def cache_path(args: argparse.Namespace, url: str) -> Path:
    base = normalize_id(args.paper_id or url)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", base)
    return Path(args.cache_dir).expanduser() / f"{safe}.html"


def fetch_html(url: str, target: Path, timeout: float) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return True, target.read_text(encoding="utf-8", errors="replace")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "embodied-ai-literature-hub/1.0 (local research workflow)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if status >= 400:
                return False, ""
            payload = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code in {404, 410}:
            return False, ""
        raise
    target.write_text(payload, encoding="utf-8")
    return True, payload


def extract_text(html: str) -> str:
    parser = TextHTMLParser()
    parser.feed(html)
    return parser.text()


def current_heading(text: str, position: int) -> str:
    prefix = text[:position]
    headings = re.findall(r"^##\s+(.+)$", prefix, flags=re.MULTILINE)
    return headings[-1] if headings else "HTML body"


def find_matches(text: str, terms: list[str], window: int = 260) -> list[dict[str, object]]:
    matches = []
    lowered = text.lower()
    for raw_term in [term for term in terms if term.strip()]:
        term = raw_term.lower()
        start = 0
        while True:
            index = lowered.find(term, start)
            if index < 0:
                break
            left = max(0, index - window)
            right = min(len(text), index + len(term) + window)
            snippet = " ".join(text[left:right].split())
            matches.append(
                {
                    "term": raw_term,
                    "locator": current_heading(text, index),
                    "char_start": index,
                    "snippet": snippet,
                }
            )
            start = index + len(term)
            if len(matches) >= 120:
                return matches
    return matches


def reference_hints(text: str) -> list[dict[str, str]]:
    lower = text.lower()
    start = lower.rfind("references")
    ref_text = text[start:] if start >= 0 else text[-25000:]
    hints = []
    seen = set()
    for match in re.finditer(r"(?:arXiv[:\s]*)?(\d{4}\.\d{4,5})(?:v\d+)?", ref_text, flags=re.IGNORECASE):
        arxiv_id = match.group(1)
        if arxiv_id in seen:
            continue
        seen.add(arxiv_id)
        left = max(0, match.start() - 180)
        right = min(len(ref_text), match.end() + 260)
        hints.append({"arxiv_id": arxiv_id, "snippet": " ".join(ref_text[left:right].split())})
    return hints[:80]


def main() -> int:
    args = parse_args()
    url = html_url(args)
    target = cache_path(args, url)
    available, html = fetch_html(url, target, args.timeout)
    text = extract_text(html) if available else ""
    if args.max_chars and text:
        text = text[: args.max_chars]
    terms = [term.strip() for term in (args.terms or "").split(",") if term.strip()]
    output = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paper_id": normalize_id(args.paper_id or url),
        "html_url": url,
        "available": available,
        "cache_file": str(target) if available else "",
        "text_chars": len(text),
        "term_matches": find_matches(text, terms) if text else [],
        "reference_hints": reference_hints(text) if text else [],
    }
    if args.include_text:
        output["text"] = text
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
