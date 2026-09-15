#!/usr/bin/env python3
"""fetch-layer CLI: one entry, one subcommand per tool.

Each subcommand owns its original flags (per-subcommand parsers, so legacy
flag names never collide); implementation lives in the embodied_learning
fetch layer. Subcommand names are the old single-purpose scripts
kebab-cased: `extract-arxiv-html` was `scripts/extract_arxiv_html.py`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# ---- extract-arxiv-html (was scripts/extract_arxiv_html.py) ----------------------

import argparse

from embodied_learning.fetch.html import DEFAULT_CACHE_DIR, HtmlExtraction  # noqa: E402


def _extract_arxiv_html_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
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


def _extract_arxiv_html_main(argv: list[str] | None = None) -> int:
    args = _extract_arxiv_html_parse_args(argv)
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

# ---- extract-arxiv-pdf (was scripts/extract_arxiv_pdf.py) -----------------------

import argparse

from embodied_learning.fetch.pdf import DEFAULT_CACHE_DIR, PdfExtraction  # noqa: E402


def _extract_arxiv_pdf_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
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


def _extract_arxiv_pdf_main(argv: list[str] | None = None) -> int:
    args = _extract_arxiv_pdf_parse_args(argv)
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

# ---- extract-arxiv-tex (was scripts/extract_arxiv_tex.py) -----------------------

import argparse

from embodied_learning.fetch.tex import DEFAULT_SOURCE_CACHE_DIR, DEFAULT_TO, TexExtraction  # noqa: E402


def _extract_arxiv_tex_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", help="arXiv ID; fetches full text via the selected transport.")
    parser.add_argument("--transport", choices=["arxiv2md", "s3-tex"], default="arxiv2md",
                        help="arxiv2md = public REST API via curl (default, no credentials); "
                             "s3-tex = S3 tarball + pandoc (TODO: needs AWS credentials).")
    parser.add_argument("--source", help="[s3-tex] Local .tar.gz source package (skips the S3 download).")
    parser.add_argument("--source-cache-dir", default=DEFAULT_SOURCE_CACHE_DIR)
    parser.add_argument("--_extract_arxiv_tex_main-tex", help="[s3-tex] Main .tex member name; overrides automatic discovery.")
    parser.add_argument("--terms", help="Comma-separated topic terms for term matching (optional).")
    parser.add_argument("--minimum-chars", type=int, default=1000, help="Minimum markdown chars for medium quality.")
    parser.add_argument("--to", default=DEFAULT_TO, help="[s3-tex] Pandoc target format (default preserves $...$ math and pipe tables).")
    parser.add_argument("--pandoc-timeout", type=float, default=60.0, help="[s3-tex] pypandoc.convert_file timeout budget hint.")
    parser.add_argument("--curl-timeout", type=float, default=120.0, help="[arxiv2md] curl max time in seconds.")
    parser.add_argument("--output", help="Write the extraction JSON here instead of stdout.")
    parser.add_argument("--markdown-output", help="Write the converted Markdown here; defaults to <output>.md alongside the JSON.")
    return parser.parse_args(argv)


def _extract_arxiv_tex_main(argv: list[str] | None = None) -> int:
    args = _extract_arxiv_tex_parse_args(argv)
    extraction = TexExtraction(
        paper_id=args.paper_id or "",
        transport=args.transport,
        source=args.source,
        source_cache_dir=args.source_cache_dir,
        main_tex=args.main_tex,
        terms=args.terms,
        minimum_chars=args.minimum_chars,
        to=args.to,
        pandoc_timeout=args.pandoc_timeout,
        curl_timeout=args.curl_timeout,
        output=args.output,
        markdown_output=args.markdown_output,
    )
    output = extraction.run()
    from embodied_learning.fetch.tex import emit  # noqa: E402  (avoid importing JSON plumbing early)

    emit(output, args.output, args.markdown_output)
    return 0 if output.get("evidence_eligible") else 2

# ---- download-arxiv-source (was scripts/download_arxiv_source.py) -------------------

import argparse
import json

from embodied_learning.fetch.s3_source import (  # noqa: E402
    DEFAULT_CACHE_DIR,
    MAX_WORKERS,
    REGION,
    S3DownloadOptions,
    collect_ids,
    make_client,
    run_queue,
)


def _download_arxiv_source_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", action="append", default=[], help="arXiv ID. May be repeated.")
    parser.add_argument("--paper-id-file", help="UTF-8 file with one arXiv ID per line (# comments allowed).")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR, help="Tarball cache directory.")
    parser.add_argument("--workers", type=int, default=8, help=f"Bounded I/O workers; capped at {MAX_WORKERS}.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Per-request read timeout in seconds.")
    parser.add_argument("--retries", type=int, default=2, help="Retries per paper after transient S3 errors. Capped at 3.")
    parser.add_argument("--region", default=REGION, help="S3 region of the arXiv bucket.")
    requester = parser.add_mutually_exclusive_group()
    requester.add_argument("--requester-pays", dest="requester_pays", action="store_true", default=True,
                           help="Sign requests with standard AWS credentials and pass RequestPayer=requester "
                                "(default: s3://arxiv/ is a requester-pays bucket).")
    requester.add_argument("--anonymous", dest="requester_pays", action="store_false",
                           help="Use the botocore.UNSIGNED anonymous client (no credentials; the bucket "
                                "currently answers AccessDenied to anonymous requests).")
    parser.add_argument("--force", action="store_true", help="Re-download even when the cache file exists.")
    parser.add_argument("--summary-output", help="Write the run summary JSON here.")
    return parser.parse_args(argv)


def _download_arxiv_source_main(argv: list[str] | None = None) -> int:
    args = _download_arxiv_source_parse_args(argv)
    options = S3DownloadOptions(
        cache_dir=args.cache_dir,
        workers=args.workers,
        timeout=args.timeout,
        retries=args.retries,
        region=args.region,
        requester_pays=args.requester_pays,
        force=args.force,
    )
    paper_ids = collect_ids(args.paper_id, args.paper_id_file)
    client = make_client(options.region, anonymous=not options.requester_pays)
    summary = run_queue(paper_ids, options, client)
    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.summary_output:
        path = Path(args.summary_output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    ok = summary["states"].get("downloaded", 0) + summary["states"].get("cached", 0)
    return 0 if ok else 2

# ---- extract-content-queue (was scripts/extract_content_queue.py) -------------------

import argparse

from embodied_learning.fetch.queue import QueueOptions, run_queue  # noqa: E402


def _extract_content_queue_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id-file", required=True)
    parser.add_argument("--terms", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--html-cache-dir",
        help="Explicit HTML cache directory forwarded to extract_arxiv_content.py.",
    )
    parser.add_argument(
        "--pdf-cache-dir",
        help="Explicit PDF cache directory forwarded to extract_arxiv_content.py.",
    )
    parser.add_argument("--workers", type=int, default=2, help="Bounded I/O workers; capped at 4.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--paper-timeout", type=float, default=120.0, help="Hard wall-clock limit per paper subprocess.")
    parser.add_argument("--top-sections", type=int, default=3)
    parser.add_argument("--ocr-mode", choices=["auto", "never", "always"], default="never")
    parser.add_argument("--ocr-language", default="eng")
    parser.add_argument(
        "--include-full-text",
        action="store_true",
        help="Checkpoint complete HTML text/PDF pages for $embodied-ai-paper-reader.",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--preferred-source",
        choices=["html", "tex", "auto"],
        default="html",
        help="Forwarded to extract_arxiv_content.py; default keeps the legacy html->pdf chain.",
    )
    parser.add_argument(
        "--tex-transport",
        choices=["arxiv2md", "s3-tex"],
        default="arxiv2md",
        help="Markdown-tier transport, forwarded to extract_arxiv_content.py.",
    )
    parser.add_argument("--curl-timeout", type=float, default=120.0,
                        help="[arxiv2md] curl max time in seconds, forwarded to the gateway.")
    parser.add_argument(
        "--tex-cache-dir",
        help="[s3-tex] Cache directory for S3 TeX source tarballs, forwarded to extract_arxiv_content.py.",
    )
    parser.add_argument("--summary-output")
    return parser.parse_args(argv)


def _extract_content_queue_main(argv: list[str] | None = None) -> int:
    args = _extract_content_queue_parse_args(argv)
    options = QueueOptions(
        paper_id_file=args.paper_id_file,
        terms=args.terms,
        output_dir=args.output_dir,
        html_cache_dir=args.html_cache_dir,
        pdf_cache_dir=args.pdf_cache_dir,
        workers=args.workers,
        timeout=args.timeout,
        paper_timeout=args.paper_timeout,
        top_sections=args.top_sections,
        ocr_mode=args.ocr_mode,
        ocr_language=args.ocr_language,
        include_full_text=args.include_full_text,
        force=args.force,
        preferred_source=args.preferred_source,
        tex_transport=args.tex_transport,
        curl_timeout=args.curl_timeout,
        tex_cache_dir=args.tex_cache_dir,
        summary_output=args.summary_output,
    )
    summary = run_queue(options)
    print(f"Recovered {summary['evidence_eligible_count']} of {summary['paper_count']} papers; held {summary['held_count']}.")
    return 0 if summary["evidence_eligible_count"] else 2



_SUBCOMMANDS = {
    "extract-arxiv-html": _extract_arxiv_html_main,
    "extract-arxiv-pdf": _extract_arxiv_pdf_main,
    "extract-arxiv-tex": _extract_arxiv_tex_main,
    "download-arxiv-source": _download_arxiv_source_main,
    "extract-content-queue": _extract_content_queue_main,
}


def main(argv: list[str] | None = None) -> int:
    """Dispatch to the tool's own parser: `{layer}.py <subcommand> [flags...]`.

    Each subcommand reuses its original single-purpose parser verbatim, so
    flags, help text, and exit codes are unchanged from the old scripts.
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("\nsubcommands: " + ", ".join(_SUBCOMMANDS))
        return 0
    handler = _SUBCOMMANDS.get(argv[0])
    if handler is None:
        print(f"unknown subcommand: {argv[0]}", file=sys.stderr)
        print("\nsubcommands: " + ", ".join(_SUBCOMMANDS))
        return 2
    return handler(argv[1:])


if __name__ == "__main__":
    sys.exit(main())
