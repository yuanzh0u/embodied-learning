#!/usr/bin/env python3
"""Create a literature-review run folder with an in-progress birth-certificate run.json.

Writing run.json at the START (not at settle time) means an abandoned run is
visibly unfinished: `status: in-progress` makes check_run_bundle.py fail until
the agent finishes the bundle and flips it to `settled`. This closes the
"pipeline abandoned mid-way, no trace" failure mode.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Review topic or question.")
    parser.add_argument("--knowledge-id", action="append", default=[], help="EA/ERR knowledge ID. Repeatable.")
    parser.add_argument("--time-range", help="Resolved review window, e.g. 2026-01-09..2026-07-09.")
    parser.add_argument("--date", help="Run date YYYYMMDD for the folder name (default: today).")
    parser.add_argument("--work-dir", default=str(REPO_ROOT / "work"), help="Parent directory for the run folder.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing run.json in the target folder.")
    return parser.parse_args()


def slugify_topic(topic: str) -> str:
    slug = re.sub(r"\s+", "-", topic.strip().lower())
    slug = re.sub(r"[^0-9A-Za-z一-鿿._-]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-._")
    return slug[:72] or "review"


def run_folder_name(topic: str, date_str: str) -> str:
    return f"literature-review-{slugify_topic(topic)}-{date_str}"


def main() -> int:
    args = parse_args()
    if args.date:
        date_str = args.date
    else:
        # Date.today is allowed here (plain CLI, not a workflow script).
        date_str = dt.date.today().strftime("%Y%m%d")
    run_dir = Path(args.work_dir) / run_folder_name(args.topic, date_str)
    manifest_path = run_dir / "run.json"
    if manifest_path.exists() and not args.force:
        print(f"run.json already exists at {manifest_path}; pass --force to overwrite", file=sys.stderr)
        return 1
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "run": run_dir.name,
        "topic": args.topic,
        "status": "in-progress",
        "time_range": args.time_range or "",
        "knowledge_ids": args.knowledge_id,
        "event_count": 0,
        "files": {},
        "notes": "Created by init_run.py. Flip status to 'settled' only after the full bundle passes check_run_bundle.py and audit_citations.py.",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Initialized run: {run_dir}")
    print(f"- {manifest_path} (status: in-progress)")
    print("Next: run planner -> hub (search, extract, promote_candidates) -> build_review_packet -> write three articles -> settle.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
