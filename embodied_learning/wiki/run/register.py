"""Register a settled review run in the KB's literature-review catalog.

The settle flow should call this (or let run.py launch do it) instead of
hand-editing the catalog table: the read→append→write round trip runs under
the KB-shared ``catalog`` lock and the link check makes it idempotent —
registering the same run twice is a no-op, not a duplicate row. Agents doing
manual settles (wiki workflow) use this entry point.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from embodied_learning.utils.layout import default_kb_root
from embodied_learning.wiki.run.catalog import register_run_in_catalog



def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/run.py."""
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
