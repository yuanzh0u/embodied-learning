#!/usr/bin/env python3
"""Compatibility wrapper for embodied-ai-query-planner."""

from __future__ import annotations

import os
from pathlib import Path
import sys


def planner_script() -> Path:
    skills_dir = Path(__file__).resolve().parents[2]
    return skills_dir / "embodied-ai-query-planner" / "scripts" / "build_query_plan.py"


def main() -> int:
    planner = planner_script()
    if not planner.is_file():
        print(
            "embodied-ai-literature-hub no longer owns query planning. "
            "Expected $embodied-ai-query-planner script at wrapper-relative path "
            f"../../embodied-ai-query-planner/scripts/build_query_plan.py ({planner}). "
            "Restore or install that Skill, then run the planner directly or re-run this compatibility path.",
            file=sys.stderr,
        )
        return 2

    os.execv(sys.executable, [sys.executable, str(planner), *sys.argv[1:]])
    return 127


if __name__ == "__main__":
    sys.exit(main())
