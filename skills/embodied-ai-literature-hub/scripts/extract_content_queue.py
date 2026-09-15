#!/usr/bin/env python3
"""CLI: recover arXiv full text for a paper-ID queue with bounded concurrency.

Library API lives in embodied_learning/fetch/queue.py (QueueOptions + run_queue plus the
module-level helpers). This entry owns only argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.fetch.queue import QueueOptions, run_queue  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
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


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
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


if __name__ == "__main__":
    sys.exit(main())
