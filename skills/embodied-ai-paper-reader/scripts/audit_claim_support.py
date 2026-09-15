#!/usr/bin/env python3
"""CLI: audit claim/quote verbatim support in a paper note.

Library API lives in embodied_learning/knowledge/claim_support.py (audit, extraction_text,
locator_surface). This entry owns only argument parsing and dispatch.
"""
import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.knowledge.claim_support import audit, load_object  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-note", required=True)
    parser.add_argument("--extraction", required=True)
    parser.add_argument("--output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        note = load_object(Path(args.paper_note))
        extraction = load_object(Path(args.extraction))
        result = audit(note, extraction)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"schema_version": 1, "paper_id": "", "status": "reject", "reason": str(exc), "cards": []}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    print(f"claim-support audit: {result['status']}", file=sys.stderr)
    return {"pass": 0, "needs-review": 1, "reject": 2}[str(result["status"])]


if __name__ == "__main__":
    sys.exit(main())
