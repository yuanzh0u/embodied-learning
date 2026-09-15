#!/usr/bin/env python3
"""CLI: build a structured arXiv query plan from a topic (planning stage).

Library API lives in embodied_learning/search/query_plan.py (module-level ``build_plan``).
This entry owns argument parsing and dispatch, including the
``--list-topics``/``--list-families`` listing modes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.search.query_plan import (  # noqa: E402
    DEFAULT_MAX_QUERIES,
    FAMILY_PLANS,
    REVIEW_MODES,
    TOPIC_PLANS,
    build_plan,
    render_markdown,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=False, help="Chinese or English embodied-AI topic.")
    parser.add_argument("--knowledge-id", action="append", default=[], help="EA knowledge ID. May be repeated.")
    parser.add_argument("--family", action="append", default=[], help="Specialized query family. May be repeated.")
    parser.add_argument("--start-date", help="Optional YYYY-MM-DD scope metadata.")
    parser.add_argument("--end-date", help="Optional YYYY-MM-DD scope metadata.")
    parser.add_argument("--dynamic-file", action="append", default=[], help="JSON file with LLM/agent dynamic query suggestions. May be repeated.")
    parser.add_argument("--calibration-file", action="append", default=[], help="JSON calibration file. May be repeated.")
    parser.add_argument(
        "--review-mode",
        choices=sorted(REVIEW_MODES),
        default="scoping",
        help="Search-depth contract. Targets are floors, never caps.",
    )
    parser.add_argument("--target-candidates", type=int, help="Override the mode's candidate floor.")
    parser.add_argument("--target-full-text", type=int, help="Override the mode's full-text screening floor.")
    parser.add_argument("--target-evidence", type=int, help="Override the mode's accepted-paper floor.")
    parser.add_argument("--max-queries", type=int, default=DEFAULT_MAX_QUERIES, help="Max arXiv API query entries.")
    parser.add_argument("--output", help="Write JSON plan to this path instead of stdout.")
    parser.add_argument("--markdown-output", help="Write a Markdown review view to this path.")
    parser.add_argument("--list-topics", action="store_true", help="List supported EA topic IDs and exit.")
    parser.add_argument("--list-families", action="store_true", help="List supported specialized families and exit.")
    return parser.parse_args(argv)


def list_and_exit(items: dict[str, Any]) -> int:
    for key in sorted(items):
        print(key)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.list_topics:
        return list_and_exit(TOPIC_PLANS)
    if args.list_families:
        return list_and_exit(FAMILY_PLANS)
    if not args.topic:
        raise SystemExit("--topic is required unless --list-topics or --list-families is used.")
    plan = build_plan(
        args.topic,
        knowledge_id=args.knowledge_id,
        family=args.family,
        start_date=args.start_date,
        end_date=args.end_date,
        dynamic_file=args.dynamic_file,
        calibration_file=args.calibration_file,
        review_mode=args.review_mode,
        target_candidates=args.target_candidates,
        target_full_text=args.target_full_text,
        target_evidence=args.target_evidence,
        max_queries=args.max_queries,
    )
    rendered = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    if args.markdown_output:
        Path(args.markdown_output).write_text(render_markdown(plan), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
