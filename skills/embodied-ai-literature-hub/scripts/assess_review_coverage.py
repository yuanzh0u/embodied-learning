#!/usr/bin/env python3
"""CLI: assess query-dimension coverage and saturation.

Library API lives in embodied_learning/search/coverage.py (module-level ``assess``). This
entry owns only argument parsing and dispatch.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.search.coverage import run  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-plan", required=True)
    parser.add_argument("--candidate-registry", required=True)
    parser.add_argument("--evidence-jsonl", action="append", default=[], help="Accepted evidence; repeatable.")
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run(
        Path(args.query_plan),
        Path(args.candidate_registry),
        [Path(path) for path in args.evidence_jsonl],
        Path(args.output),
    )


if __name__ == "__main__":
    sys.exit(main())
