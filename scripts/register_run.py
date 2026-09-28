#!/usr/bin/env python3
"""Register a settled review run in the KB's literature-review catalog.

The settle flow should call this (or let launch_review.py do it) instead of
hand-editing the catalog table: the read→append→write round trip runs under
the KB-shared ``catalog`` lock and the link check makes it idempotent —
registering the same run twice is a no-op, not a duplicate row. Agents doing
manual settles (wiki workflow) use this entry point.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from lib.layout import default_kb_root
    from lib.review_runs import register_run_in_catalog
except ImportError:  # installed console-script entry: package import path
    from wiki_scripts.lib.layout import default_kb_root
    from wiki_scripts.lib.review_runs import register_run_in_catalog


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="Settled run directory (holds run.json).")
    parser.add_argument("--kb-root", default=str(default_kb_root()), help="KB root owning the catalog.")
    parser.add_argument("--row", help="Custom 成果索引 Markdown row (default: generated from run.json).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_json = Path(args.run_dir).expanduser().resolve() / "run.json"
    if not run_json.is_file():
        print(f"run.json not found: {run_json}", file=sys.stderr)
        return 1
    registered = register_run_in_catalog(Path(args.kb_root).expanduser(), run_json, args.row)
    if registered:
        print(f"catalog 已登记：{run_json.parent.name}")
    else:
        print(f"catalog 已包含该 run，跳过（幂等）：{run_json.parent.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
