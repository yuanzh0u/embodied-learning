#!/usr/bin/env python3
"""CLI: download/cache an arXiv PDF and extract text-layer content with OCR fallback.

Library API lives in embodied_learning/fetch/pdf.py (PdfExtraction plus the module-level
quality/matching helpers). This entry owns only argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.fetch.pdf import DEFAULT_CACHE_DIR, PdfExtraction  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", help="arXiv ID, with or without version.")
    parser.add_argument("--pdf-url", help="PDF URL. Defaults to https://arxiv.org/pdf/<paper-id>.pdf")
    parser.add_argument("--pdf-file", help="Use an existing local PDF instead of downloading.")
    parser.add_argument("--terms", help="Comma-separated terms to locate in extracted text.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--max-pages", type=int, default=0, help="0 means all pages.")
    parser.add_argument("--top-pages", type=int, default=8, help="Ranked topic-relevant pages to report.")
    parser.add_argument("--ocr-mode", choices=["auto", "never", "always"], default="auto")
    parser.add_argument("--ocr-language", default="eng", help="Tesseract language expression, e.g. eng or eng+chi_sim.")
    parser.add_argument("--ocr-dpi", type=int, default=220)
    parser.add_argument("--min-chars-per-page", type=int, default=180)
    parser.add_argument("--include-pages", action="store_true", help="Include full extracted page text in JSON output.")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    extraction = PdfExtraction(
        paper_id=args.paper_id or "",
        pdf_url=args.pdf_url,
        pdf_file=args.pdf_file,
        terms=args.terms,
        cache_dir=args.cache_dir,
        max_pages=args.max_pages,
        top_pages=args.top_pages,
        ocr_mode=args.ocr_mode,
        ocr_language=args.ocr_language,
        ocr_dpi=args.ocr_dpi,
        min_chars_per_page=args.min_chars_per_page,
        include_pages=args.include_pages,
        output=args.output,
    )
    extraction.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
