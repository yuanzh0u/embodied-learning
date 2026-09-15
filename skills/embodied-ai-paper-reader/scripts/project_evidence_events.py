#!/usr/bin/env python3
"""CLI: project a validated note + audit into evidence event JSONL.

Library API lives in src/knowledge/evidence_projection.py (project,
load_object). This entry owns only argument parsing and dispatch.
"""
import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.knowledge.evidence_projection import load_object, project  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-note", required=True)
    parser.add_argument("--audit", required=True, help="Passing audit JSON from audit_claim_support.py.")
    parser.add_argument("--id-prefix", required=True)
    parser.add_argument("--start-seq", type=int, default=1)
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        note = load_object(Path(args.paper_note))
        audit = load_object(Path(args.audit))
        events = project(note, audit, args.id_prefix, args.start_seq)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"evidence projection blocked: {exc}", file=sys.stderr)
        return 2
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n", encoding="utf-8")
    print(f"Projected {len(events)} verified evidence event(s): {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
