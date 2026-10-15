"""Create a literature-review run folder with an in-progress birth-certificate run.json.

Writing run.json at the START (not at settle time) means an abandoned run is
visibly unfinished: `status: in-progress` makes run.py check-bundle fail until
the agent finishes the bundle and flips it to `settled`. This closes the
"pipeline abandoned mid-way, no trace" failure mode.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

from embodied_learning import locks
from embodied_learning.utils.layout import default_kb_root


def slugify_topic(topic: str) -> str:
    slug = re.sub(r"\s+", "-", topic.strip().lower())
    slug = re.sub(r"[^0-9A-Za-z一-鿿._-]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-._")
    return slug[:72] or "review"


def run_folder_name(topic: str, date_str: str, run_version: int = 1) -> str:
    """Run folder name: `literature-review-<topic>-<date>` for v1 (the ADR 0003
    contract), `literature-review-<topic>-<date>-v<N>` for repeat productions.
    Version is a suffix, never auto-incremented — callers pass it explicitly."""
    base = f"literature-review-{slugify_topic(topic)}-{date_str}"
    return base if run_version <= 1 else f"{base}-v{int(run_version)}"


def parse_run_folder_version(name: str) -> int:
    """Version mark embedded in a run folder name (1 when unmarked)."""
    match = re.search(r"-v(\d+)$", name)
    return int(match.group(1)) if match else 1


def run(args: argparse.Namespace) -> int:
    """Create the run folder + birth-certificate run.json.

    ``args`` is produced by the CLI parser (see scripts/run.py ``init``).
    """
    if args.date:
        date_str = args.date
    else:
        # Date.today is allowed here (plain CLI, not a workflow script).
        date_str = dt.date.today().strftime("%Y%m%d")
    run_dir = Path(args.work_dir) / run_folder_name(args.topic, date_str, args.run_version)
    manifest_path = run_dir / "run.json"
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "workflow_version": 2,
        "run": run_dir.name,
        "run_version": args.run_version,
        "topic": args.topic,
        "status": "in-progress",
        "review_mode": args.review_mode,
        "time_range": args.time_range or "",
        "knowledge_ids": args.knowledge_id,
        "event_count": 0,
        "files": {},
        "notes": "Created by run.py init. Flip status to 'settled' only after coverage/saturation, evidence, citation, and editorial gates pass.",
    }
    # Record the caller's real inputs separately from the EFFECTIVE fields
    # above. `review_mode` is the contract the run enforces; `inputs` is what
    # the user actually asked for. When they differ, that drift is itself the
    # bug we want to see (2026-10-09: a rapid request ran as scoping and the
    # only trace was a chat-sessions entry that later went missing).
    inputs: dict = {"source": "cli", "review_mode": args.review_mode}
    if args.inputs_json:
        try:
            parsed = json.loads(args.inputs_json)
        except json.JSONDecodeError as exc:
            print(f"--inputs-json is not valid JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(parsed, dict):
            print("--inputs-json must be a JSON object", file=sys.stderr)
            return 2
        inputs.update({str(k): v for k, v in parsed.items()})
    manifest["inputs"] = inputs
    # O_EXCL creation instead of check-then-create: two machines (or terminals)
    # starting the same topic+date run must not both "win". Lock root is the KB
    # root (work/ sits directly beneath it) so the same run__<name> lock the
    # driver holds also guards the --force rewrite path.
    lock_root = Path(args.work_dir).parent
    payload = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.force:
        with locks.kb_lock(lock_root, f"run__{run_dir.name}", stale=21600):
            manifest_path.unlink(missing_ok=True)
            fd = os.open(manifest_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            os.write(fd, payload)
            os.close(fd)
    else:
        try:
            fd = os.open(manifest_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            print(f"run.json already exists at {manifest_path}; pass --force to overwrite", file=sys.stderr)
            return 1
        os.write(fd, payload)
        os.close(fd)
    print(f"Initialized run: {run_dir}")
    print(f"- {manifest_path} (status: in-progress)")
    print("Next: planner -> candidate registry -> coverage rounds -> HTML/PDF/OCR extraction -> evidence -> writer -> settle.")
    return 0
