#!/usr/bin/env python3
"""Validate every literature-review run routed by the current catalog.

The catalog is the version-selection layer for this repository. Historical
and superseded runs remain append-only under ``evidence/`` but are not CI
targets unless the catalog routes to them.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.review_runs import (  # noqa: E402
    STANDARD_ARTICLES,
    catalog_run_paths,
    event_consistency_problems,
    evidence_paths,
    load_catalog_runs,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root to validate.")
    return parser.parse_args()


def run(command: list[str], root: Path) -> None:
    print(f"+ {shlex.join(command)}", flush=True)
    subprocess.run(command, cwd=root, check=True)


def validate(root: Path) -> None:
    root = root.resolve()
    selected_runs = load_catalog_runs(root)
    run_paths = [item.manifest_path for item in selected_runs]

    run([sys.executable, "scripts/check_kb_links.py", "--root", "."], root)
    for run_json in run_paths:
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        run_dir = run_json.parent
        relative_run_dir = str(run_dir.relative_to(root))
        local_evidence = evidence_paths(run_json, manifest)
        run([sys.executable, "scripts/check_run_bundle.py", relative_run_dir], root)
        for evidence_path in local_evidence:
            run(
                [
                    sys.executable,
                    "skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py",
                    "--evidence-jsonl",
                    str(evidence_path.relative_to(root)),
                    "--validate-only",
                ],
                root,
            )

        citation_command = [sys.executable, "scripts/audit_citations.py"]
        for article in STANDARD_ARTICLES:
            citation_command.extend(["--article", str((run_dir / article).relative_to(root))])
        citation_command.extend(
            ["--appendix", str((run_dir / "evidence-appendix.md").relative_to(root))]
        )
        for evidence_path in local_evidence:
            citation_command.extend(["--evidence-jsonl", str(evidence_path.relative_to(root))])
        citation_command.extend(["--run-json", str(run_json.relative_to(root))])
        run(citation_command, root)
        run(
            [
                sys.executable,
                "skills/embodied-ai-review-writer/scripts/audit_article_quality.py",
                "--bundle-dir",
                relative_run_dir,
            ],
            root,
        )

    problems = event_consistency_problems(run_paths)
    if problems:
        raise ValueError("event consistency failed:\n- " + "\n- ".join(problems))
    print(f"validated {len(run_paths)} catalog-routed literature-review runs")


def main() -> int:
    args = parse_args()
    try:
        validate(Path(args.root))
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
