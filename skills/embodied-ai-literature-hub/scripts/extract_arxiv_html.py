#!/usr/bin/env python3
"""CLI: fetch/cache arXiv LaTeXML HTML and extract the section tree.

Library API lives in embodied_learning/fetch/html.py (HtmlExtraction plus the module-level
parsing helpers). This entry owns only argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.fetch.html import DEFAULT_CACHE_DIR, HtmlExtraction  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", help="arXiv ID, with or without version.")
    parser.add_argument("--html-url", help="HTML URL. Defaults to https://arxiv.org/html/<paper-id>")
    parser.add_argument("--terms", help="Comma-separated terms to locate and rank sections by.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-chars", type=int, default=0, help="0 means all extracted text.")
    parser.add_argument("--include-text", action="store_true", help="Include full extracted text in JSON output.")
    parser.add_argument("--top-sections", type=int, default=8, help="How many ranked sections to report.")
    parser.add_argument(
        "--include-section-text",
        action="store_true",
        help="Include full text for each ranked section (for selective deep reading).",
    )
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    extraction = HtmlExtraction(
        paper_id=args.paper_id or "",
        html_url=args.html_url,
        terms=args.terms,
        cache_dir=args.cache_dir,
        timeout=args.timeout,
        max_chars=args.max_chars,
        include_text=args.include_text,
        top_sections=args.top_sections,
        include_section_text=args.include_section_text,
        output=args.output,
    )
    extraction.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
