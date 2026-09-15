#!/usr/bin/env python3
"""CLI: unified extraction gateway — HTML -> markdown -> PDF chain with quality gates.

Library API lives in src/fetch/chain.py (ContentOptions + extract_content plus
the module-level helpers). This entry owns only argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.fetch.chain import (  # noqa: E402
    DEFAULT_OUTPUT_DIR,
    ContentOptions,
    emit,
    extract_content,
    resolve_format,
    resolve_output_path,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "paper_id_pos", nargs="?",
        help=argparse.SUPPRESS)  # shortcut: leading bare arXiv ID
    parser.add_argument("--paper-id",
                        help="arXiv ID (with or without version).")
    parser.add_argument(
        "--terms",
        help="Comma-separated topic terms (optional for casual reading).")
    parser.add_argument(
        "--format",
        choices=["auto", "json", "markdown"],
        default="auto",
        help=
        "Output format. auto = markdown for .md files/terminals, JSON when piped.",
    )
    parser.add_argument("--html-url")
    parser.add_argument("--pdf-url")
    parser.add_argument("--pdf-file",
                        help="Local PDF for testing/offline extraction.")
    parser.add_argument("--preferred-source",
                        choices=["html", "tex", "auto"],
                        default="html",
                        help=("Full-text tier order. html (default) = html -> pdf, the legacy "
                              "chain. tex = markdown tier first (arxiv2md API by default, see "
                              "--tex-transport) -> html -> pdf. auto = html -> markdown tier "
                              "-> pdf. The markdown tier needs only curl (arxiv2md) and is "
                              "skipped gracefully when the API has no HTML for the paper."),)
    parser.add_argument(
        "--tex-transport",
        choices=["arxiv2md", "s3-tex"],
        default="arxiv2md",
        help=("Transport for the markdown tier. arxiv2md (default) = public "
              "REST API via curl, no credentials. s3-tex = S3 TeX source "
              "tarball + pandoc (TODO: needs AWS credentials — the "
              "s3://arxiv/ bucket is requester-pays)."),
    )
    parser.add_argument("--curl-timeout", type=float, default=120.0,
                        help="[arxiv2md] curl max time in seconds.")
    from src.fetch.chain import extract_arxiv_tex_default_cache_dir  # noqa: E402
    from src.fetch import html as _html, pdf as _pdf  # noqa: E402
    parser.add_argument("--html-cache-dir", default=_html.DEFAULT_CACHE_DIR)
    parser.add_argument("--pdf-cache-dir", default=_pdf.DEFAULT_CACHE_DIR)
    parser.add_argument("--tex-cache-dir",
                        default=extract_arxiv_tex_default_cache_dir(),
                        help="[s3-tex] Cache directory for S3 TeX source tarballs.")
    parser.add_argument("--source-tarball",
                        help="[s3-tex] Local TeX source .tar.gz; skips the S3 download.")
    parser.add_argument("--main-tex",
                        help="[s3-tex] Main .tex member inside the source tarball.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--top-sections", type=int, default=6)
    parser.add_argument("--max-pages", type=int, default=0)
    parser.add_argument(
        "--ocr-mode",
        choices=["auto", "never", "always"],
        default="never",
        help="Default 'never' per the full-text fallback contract.")
    parser.add_argument("--ocr-language", default="eng")
    parser.add_argument("--ocr-dpi", type=int, default=220)
    parser.add_argument("--min-chars-per-page", type=int, default=180)
    parser.add_argument("--minimum-html-chars", type=int, default=1000)
    parser.add_argument("--force-pdf",
                        action="store_true",
                        help="Skip HTML and exercise PDF/OCR path.")
    parser.add_argument("--include-selected-text", action="store_true")
    parser.add_argument(
        "--include-full-text",
        action="store_true",
        help=
        "Include complete HTML text or every text-layer PDF page for $embodied-ai-paper-reader.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help=("Write result here instead of stdout. Defaults to "
              f"{DEFAULT_OUTPUT_DIR}/<paper-id>.md; a directory gets "
              "<paper-id>.md appended (.md implies markdown under --format auto)."
              ),
    )
    args = parser.parse_args(argv)
    if args.paper_id_pos and not args.paper_id:
        args.paper_id = args.paper_id_pos
    if not args.paper_id:
        parser.error("Provide an arXiv ID, e.g. extract_arxiv 2403.12550")
    from src.fetch.chain import normalize_id  # noqa: E402
    paper_id = normalize_id(args.paper_id)
    if args.output is None and sys.stdout.isatty():
        args.output = f"{DEFAULT_OUTPUT_DIR}/{paper_id}.md"  # interactive default
    args.output = resolve_output_path(args.output, paper_id)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    options = ContentOptions(
        paper_id=args.paper_id,
        terms=args.terms,
        format=args.format,
        html_url=args.html_url,
        pdf_url=args.pdf_url,
        pdf_file=args.pdf_file,
        html_cache_dir=args.html_cache_dir,
        pdf_cache_dir=args.pdf_cache_dir,
        preferred_source=args.preferred_source,
        tex_transport=args.tex_transport,
        curl_timeout=args.curl_timeout,
        tex_cache_dir=args.tex_cache_dir,
        source_tarball=args.source_tarball,
        main_tex=args.main_tex,
        timeout=args.timeout,
        top_sections=args.top_sections,
        max_pages=args.max_pages,
        ocr_mode=args.ocr_mode,
        ocr_language=args.ocr_language,
        ocr_dpi=args.ocr_dpi,
        min_chars_per_page=args.min_chars_per_page,
        minimum_html_chars=args.minimum_html_chars,
        force_pdf=args.force_pdf,
        include_selected_text=args.include_selected_text,
        include_full_text=args.include_full_text,
        output=args.output,
    )
    output_format = resolve_format(options)
    options.render_markdown = output_format == "markdown"
    output = extract_content(options)
    emit(options, output, output_format)
    return 0 if output.get("evidence_eligible") else 2


if __name__ == "__main__":
    sys.exit(main())
