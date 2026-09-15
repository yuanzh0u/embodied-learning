#!/usr/bin/env python3
"""CLI: parse browser-exported arXiv candidate lists.

Library API lives in src/search/browser_candidates.py (module-level
``build_output``). This entry owns only argument parsing and dispatch.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.search.browser_candidates import build_output, read_input  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Browser-exported JSON, HTML, text, or '-' for stdin.")
    parser.add_argument("--start-date", help="Inclusive YYYY-MM-DD filter.")
    parser.add_argument("--end-date", help="Inclusive YYYY-MM-DD filter.")
    parser.add_argument("--source-label", default="browser-fallback")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    import json

    args = parse_args(argv)
    payload = read_input(args.input)
    output = build_output(
        payload,
        source_label=args.source_label,
        source_url=args.source_url,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
