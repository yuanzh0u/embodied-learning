#!/usr/bin/env python3
"""Soft-check LLM deep-read budget vs evidence floor (token-opt medium).

Evidence floors (rapid 8 / scoping 15 / systematic 30) remain floors for accepted
papers — they are never caps. Separately, an **LLM deep-read budget** limits how
many papers receive full deep-read / one-shot note generation:

    deep_read_budget = accepted_paper_floor + offset   (default offset = 10)

Papers beyond the budget should stay at map-read / background-only unless the
user explicitly raises the budget or chooses systematic high-stakes deep mode.

Exit codes:
  0 — within budget, or a warning when --strict is absent
  1 — over budget when --strict
  2 — input error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MODE_FLOORS = {"rapid": 8, "scoping": 15, "systematic": 30}
DEFAULT_OFFSET = 10


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reading-summary", required=True, help="reading-summary.json")
    parser.add_argument(
        "--review-mode",
        choices=sorted(MODE_FLOORS),
        help="Mode used to derive the accepted-paper floor",
    )
    parser.add_argument(
        "--accepted-floor",
        type=int,
        help="Override accepted-paper floor (else from --review-mode or summary)",
    )
    parser.add_argument(
        "--budget-offset",
        type=int,
        default=DEFAULT_OFFSET,
        help=f"deep_read_budget = floor + offset (default {DEFAULT_OFFSET})",
    )
    parser.add_argument(
        "--budget",
        type=int,
        help="Absolute deep-read budget; overrides floor+offset",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when over budget (default: warn only, exit 0)",
    )
    parser.add_argument("--json", action="store_true", help="Machine-readable report")
    return parser.parse_args()


def load_summary(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("reading-summary must be a JSON object")
    return value


def resolve_floor(args: argparse.Namespace, summary: dict[str, Any]) -> int:
    if args.accepted_floor is not None:
        return max(1, int(args.accepted_floor))
    if args.review_mode:
        return MODE_FLOORS[args.review_mode]
    # Best-effort from summary metadata if present
    mode = str(summary.get("review_mode") or "").strip().lower()
    if mode in MODE_FLOORS:
        return MODE_FLOORS[mode]
    raise ValueError("provide --review-mode or --accepted-floor")


def main() -> int:
    args = parse_args()
    try:
        summary = load_summary(Path(args.reading_summary))
        floor = resolve_floor(args, summary)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    deep_read = int(summary.get("deep_read_count") or 0)
    map_read = int(summary.get("map_read_count") or 0)
    accepted = int(summary.get("accepted_evidence_paper_count") or 0)
    budget = int(args.budget) if args.budget is not None else floor + max(0, args.budget_offset)
    over = deep_read > budget
    report = {
        "schema_version": 1,
        "accepted_paper_floor": floor,
        "llm_deep_read_budget": budget,
        "budget_offset": None if args.budget is not None else args.budget_offset,
        "deep_read_count": deep_read,
        "map_read_count": map_read,
        "accepted_evidence_paper_count": accepted,
        "within_budget": not over,
        "severity": (
            "Evidence floor is a minimum for formal outputs; LLM deep-read budget is a "
            "separate soft cap on how many papers get deep/one-shot reading. Excess "
            "recovered papers may remain map-read or background-only."
        ),
        "warning": (
            f"deep_read_count ({deep_read}) exceeds LLM deep-read budget ({budget}). "
            "Prefer map-read/background-only for additional papers, or raise the budget "
            "explicitly for systematic/high-stakes work."
            if over
            else None
        ),
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        status = "OK" if not over else "WARN"
        print(
            f"[{status}] deep_read={deep_read} budget={budget} "
            f"(floor={floor}{'+'+str(args.budget_offset) if args.budget is None else ''} absolute) "
            f"map_read={map_read} accepted={accepted}"
        )
        if report["warning"]:
            print(report["warning"], file=sys.stderr)
        print(report["severity"])

    if over and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
