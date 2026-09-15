#!/usr/bin/env python3
"""CLI: validate paper-note JSON against the note schema.

Library API lives in src/knowledge/paper_note.py (validate_note, load_note).
This entry owns only argument parsing and dispatch.
"""
import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.knowledge.paper_note import load_note, validate_note  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_note")
    parser.add_argument("--json-output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        note = load_note(Path(args.paper_note))
        errors, warnings = validate_note(note)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors, warnings = [str(exc)], []
    result = {"status": "pass" if not errors else "reject", "errors": errors, "warnings": warnings}
    if args.json_output:
        target = Path(args.json_output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        print(f"paper note rejected ({len(errors)} error(s)):")
        for error in errors:
            print(f"- {error}")
        return 1
    print("paper note OK")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
