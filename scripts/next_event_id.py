#!/usr/bin/env python3
"""Scan evidence/**/evidence.jsonl and report the next available event ID per prefix."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVENT_ID = re.compile(r"^(?P<prefix>.+)-(?P<seq>\d{4})$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", default=str(REPO_ROOT / "evidence"), help="Evidence layer root.")
    parser.add_argument("--prefix", help="Only report this event-ID prefix, e.g. EA-TWM-2026.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args()


def scan(evidence_dir: Path) -> dict[str, int]:
    highest: dict[str, int] = {}
    for jsonl in sorted(evidence_dir.glob("*/evidence.jsonl")):
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            match = EVENT_ID.match(str(event.get("event_id") or ""))
            if not match:
                continue
            prefix = match.group("prefix")
            seq = int(match.group("seq"))
            if seq > highest.get(prefix, 0):
                highest[prefix] = seq
    return highest


def main() -> int:
    args = parse_args()
    evidence_dir = Path(args.evidence_dir)
    highest = scan(evidence_dir)
    if args.prefix:
        used = highest.get(args.prefix, 0)
        report = {args.prefix: {"max_used": used, "next_id": f"{args.prefix}-{used + 1:04d}"}}
    else:
        report = {
            prefix: {"max_used": used, "next_id": f"{prefix}-{used + 1:04d}"}
            for prefix, used in sorted(highest.items())
        }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if not report:
            print("no event IDs found")
        for prefix, info in report.items():
            print(f"{prefix}: max used {info['max_used']:04d}, next {info['next_id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
