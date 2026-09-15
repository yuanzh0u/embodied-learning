#!/usr/bin/env python3
"""CLI: validate evidence JSONL and render the markdown brief.

Library API lives in src/parse/brief.py (load_events, render_brief,
STANCES/CONFIDENCE vocabularies). This entry owns only argument parsing and
dispatch; `--validate-only` is the gate invoked by
scripts/validate_current_reviews.py and the paper-reader pipeline.
"""
import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.parse.brief import load_events, render_brief  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-jsonl", required=True)
    parser.add_argument("--brief-out")
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    events = load_events(Path(args.evidence_jsonl))
    result = {"valid": True, "event_count": len(events)}
    if args.brief_out and not args.validate_only:
        Path(args.brief_out).write_text(render_brief(events), encoding="utf-8")
        result["brief_out"] = args.brief_out
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
