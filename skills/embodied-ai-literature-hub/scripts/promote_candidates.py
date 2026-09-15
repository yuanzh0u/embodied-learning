#!/usr/bin/env python3
"""CLI: promote verified candidates toward evidence with digests and skeletons.

Library API lives in src/parse/promotion.py (run_promotion + helpers). This
entry owns only argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.fetch import chain as extract_arxiv_content  # noqa: E402
from src.parse.promotion import load_paper_ids, run_promotion  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", action="append", default=[], help="arXiv ID to promote. Repeatable.")
    parser.add_argument(
        "--paper-id-file",
        action="append",
        default=[],
        help="UTF-8 file with one arXiv ID per line; blank lines and # comments are ignored. Repeatable.",
    )
    parser.add_argument("--topic", required=True, help="Run topic (copied into each skeleton event).")
    parser.add_argument("--topic-id", required=True, help="Knowledge ID for these events, e.g. EA-MODEL.")
    parser.add_argument("--id-prefix", required=True, help="Event ID prefix, e.g. EA-PVC-2026.")
    parser.add_argument("--start-seq", type=int, default=1, help="First sequence number (use scripts/next_event_id.py).")
    parser.add_argument("--terms", required=True, help="Comma-separated terms for section ranking.")
    parser.add_argument("--top-sections", type=int, default=4, help="Ranked sections per paper in the digest.")
    parser.add_argument("--cache-dir", default=extract_arxiv_content.extract_arxiv_html.DEFAULT_CACHE_DIR)
    parser.add_argument("--pdf-cache-dir", default=extract_arxiv_content.extract_arxiv_pdf.DEFAULT_CACHE_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--ocr-mode", choices=["auto", "never", "always"], default="auto")
    parser.add_argument("--ocr-language", default="eng")
    parser.add_argument("--output-skeleton", required=True, help="Path for the evidence skeleton JSONL.")
    parser.add_argument("--output-digest", required=True, help="Path for the reading digest Markdown.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    terms = [term.strip() for term in args.terms.split(",") if term.strip()]
    paper_ids = load_paper_ids(args.paper_id, args.paper_id_file)
    if not paper_ids:
        print("Provide --paper-id or --paper-id-file.", file=sys.stderr)
        return 2
    return run_promotion(
        paper_ids=paper_ids,
        terms=terms,
        topic=args.topic,
        topic_id=args.topic_id,
        id_prefix=args.id_prefix,
        start_seq=args.start_seq,
        top_sections=args.top_sections,
        cache_dir=args.cache_dir,
        pdf_cache_dir=args.pdf_cache_dir,
        timeout=args.timeout,
        ocr_mode=args.ocr_mode,
        ocr_language=args.ocr_language,
        output_skeleton=args.output_skeleton,
        output_digest=args.output_digest,
    )


if __name__ == "__main__":
    sys.exit(main())
