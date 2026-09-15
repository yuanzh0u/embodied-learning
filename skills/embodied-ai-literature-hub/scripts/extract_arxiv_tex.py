#!/usr/bin/env python3
"""CLI: Markdown tier — arxiv2md REST API (default) or S3 TeX + pandoc.

Library API lives in src/fetch/tex.py (TexExtraction plus the module-level
helpers). This entry owns only argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.fetch.tex import DEFAULT_SOURCE_CACHE_DIR, DEFAULT_TO, TexExtraction  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", help="arXiv ID; fetches full text via the selected transport.")
    parser.add_argument("--transport", choices=["arxiv2md", "s3-tex"], default="arxiv2md",
                        help="arxiv2md = public REST API via curl (default, no credentials); "
                             "s3-tex = S3 tarball + pandoc (TODO: needs AWS credentials).")
    parser.add_argument("--source", help="[s3-tex] Local .tar.gz source package (skips the S3 download).")
    parser.add_argument("--source-cache-dir", default=DEFAULT_SOURCE_CACHE_DIR)
    parser.add_argument("--main-tex", help="[s3-tex] Main .tex member name; overrides automatic discovery.")
    parser.add_argument("--terms", help="Comma-separated topic terms for term matching (optional).")
    parser.add_argument("--minimum-chars", type=int, default=1000, help="Minimum markdown chars for medium quality.")
    parser.add_argument("--to", default=DEFAULT_TO, help="[s3-tex] Pandoc target format (default preserves $...$ math and pipe tables).")
    parser.add_argument("--pandoc-timeout", type=float, default=60.0, help="[s3-tex] pypandoc.convert_file timeout budget hint.")
    parser.add_argument("--curl-timeout", type=float, default=120.0, help="[arxiv2md] curl max time in seconds.")
    parser.add_argument("--output", help="Write the extraction JSON here instead of stdout.")
    parser.add_argument("--markdown-output", help="Write the converted Markdown here; defaults to <output>.md alongside the JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
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
    from src.fetch.tex import emit  # noqa: E402  (avoid importing JSON plumbing early)

    emit(output, args.output, args.markdown_output)
    return 0 if output.get("evidence_eligible") else 2


if __name__ == "__main__":
    sys.exit(main())
