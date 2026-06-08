#!/usr/bin/env python3
"""Download/cache an arXiv PDF, extract page text, term matches, and reference hints."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path


DEFAULT_CACHE_DIR = os.path.join(
    os.environ.get("TMPDIR") or "/private/tmp",
    "embodied-ai-literature-hub",
    "pdfs",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", help="arXiv ID, with or without version.")
    parser.add_argument("--pdf-url", help="PDF URL. Defaults to https://arxiv.org/pdf/<paper-id>.pdf")
    parser.add_argument("--terms", help="Comma-separated terms to locate in extracted text.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--max-pages", type=int, default=0, help="0 means all pages.")
    parser.add_argument("--include-pages", action="store_true", help="Include full extracted page text in JSON output.")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args()


def import_pypdf():
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on runtime
        raise SystemExit(
            "pypdf is required for PDF extraction. Use the Codex bundled Python runtime if available."
        ) from exc
    return PdfReader


def normalize_id(value: str) -> str:
    value = value.rsplit("/", 1)[-1]
    value = value.removesuffix(".pdf")
    return re.sub(r"v\d+$", "", value)


def pdf_url(args: argparse.Namespace) -> str:
    if args.pdf_url:
        return args.pdf_url
    if not args.paper_id:
        raise SystemExit("Provide --paper-id or --pdf-url.")
    return f"https://arxiv.org/pdf/{normalize_id(args.paper_id)}.pdf"


def cache_path(args: argparse.Namespace, url: str) -> Path:
    base = normalize_id(args.paper_id or url)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", base)
    return Path(args.cache_dir).expanduser() / f"{safe}.pdf"


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "embodied-ai-literature-hub/1.0 (research workflow)"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        target.write_bytes(response.read())


def extract_pages(pdf_file: Path, max_pages: int) -> list[dict[str, object]]:
    PdfReader = import_pypdf()
    reader = PdfReader(str(pdf_file))
    limit = len(reader.pages) if max_pages <= 0 else min(len(reader.pages), max_pages)
    pages = []
    for index in range(limit):
        text = reader.pages[index].extract_text() or ""
        pages.append({"page": index + 1, "text": "\n".join(line.rstrip() for line in text.splitlines())})
    return pages


def find_matches(pages: list[dict[str, object]], terms: list[str], window: int = 220) -> list[dict[str, object]]:
    matches = []
    lowered_terms = [term.lower() for term in terms if term.strip()]
    if not lowered_terms:
        return matches
    for page in pages:
        text = str(page["text"])
        lowered = text.lower()
        for term in lowered_terms:
            start = 0
            while True:
                index = lowered.find(term, start)
                if index < 0:
                    break
                left = max(0, index - window)
                right = min(len(text), index + len(term) + window)
                snippet = " ".join(text[left:right].split())
                matches.append({"page": page["page"], "term": term, "snippet": snippet})
                start = index + len(term)
                if len(matches) >= 80:
                    return matches
    return matches


def reference_hints(pages: list[dict[str, object]]) -> list[dict[str, str]]:
    joined = "\n".join(f"\n--- page {page['page']} ---\n{page['text']}" for page in pages[-8:])
    refs_index = joined.lower().find("references")
    if refs_index >= 0:
        joined = joined[refs_index:]
    hints = []
    seen = set()
    for line in joined.splitlines():
        compact = " ".join(line.split())
        if not compact:
            continue
        ids = re.findall(r"arXiv[:\s]+(\d{4}\.\d{4,5})(?:v\d+)?", compact, flags=re.IGNORECASE)
        if not ids:
            ids = re.findall(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b", compact)
        for arxiv_id in ids:
            if arxiv_id not in seen:
                seen.add(arxiv_id)
                hints.append({"arxiv_id": arxiv_id, "line": compact[:500]})
    return hints[:60]


def main() -> int:
    args = parse_args()
    url = pdf_url(args)
    target = cache_path(args, url)
    download(url, target)
    pages = extract_pages(target, args.max_pages)
    terms = [term.strip() for term in (args.terms or "").split(",") if term.strip()]
    output = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paper_id": normalize_id(args.paper_id or url),
        "pdf_url": url,
        "cache_file": str(target),
        "page_count_extracted": len(pages),
        "term_matches": find_matches(pages, terms),
        "reference_hints": reference_hints(pages),
    }
    if args.include_pages:
        output["pages"] = pages
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
