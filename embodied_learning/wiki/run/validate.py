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


from embodied_learning.utils.git_history import require_full_history
from embodied_learning.utils.layout import find_roots
from embodied_learning.wiki.run.catalog import (
    catalog_run_paths,
    event_consistency_problems,
    evidence_paths,
    load_catalog_runs,
    reader_articles,
)

_REPO_ROOT_CHECKOUT, _SKILLS_ROOT, SCRIPT_DIR = find_roots()
# Historical REPO_ROOT semantics: the scripts dir's parent — the repo root on a
# checkout, site-packages in a wheel (path arithmetic must work in both).
REPO_ROOT = SCRIPT_DIR.parent



def run_command(command: list[str], root: Path) -> None:
    print(f"+ {shlex.join(command)}", flush=True)
    subprocess.run(command, cwd=root, check=True)


def validate(root: Path) -> None:
    root = root.resolve()
    require_full_history(root)
    selected_runs = load_catalog_runs(root)
    run_paths = [item.manifest_path for item in selected_runs]

    run_command([sys.executable, "scripts/wiki.py", "check-kb-links", "--root", "."], root)
    for run_json in run_paths:
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        run_dir = run_json.parent
        relative_run_dir = str(run_dir.relative_to(root))
        local_evidence = evidence_paths(run_json, manifest)
        run_command([sys.executable, "scripts/run.py", "check-bundle", relative_run_dir], root)
        for evidence_path in local_evidence:
            run_command(
                [
                    sys.executable,
                    "skills/embodied-ai-literature-hub/scripts/fetch.py", "write-lit-outputs",
                    "--evidence-jsonl",
                    str(evidence_path.relative_to(root)),
                    "--validate-only",
                ],
                root,
            )

        citation_command = [sys.executable, "scripts/run.py", "audit-citations"]
        for article in reader_articles(run_json, manifest):
            citation_command.extend(["--article", str((run_dir / article).relative_to(root))])
        citation_command.extend(
            ["--appendix", str((run_dir / "evidence-appendix.md").relative_to(root))]
        )
        for evidence_path in local_evidence:
            citation_command.extend(["--evidence-jsonl", str(evidence_path.relative_to(root))])
        citation_command.extend(["--run-json", str(run_json.relative_to(root))])
        run_command(citation_command, root)
        run_command(
            [
                sys.executable,
                "skills/embodied-ai-review-writer/scripts/write.py", "audit-article-quality",
                "--bundle-dir",
                relative_run_dir,
            ],
            root,
        )

    problems = event_consistency_problems(run_paths)
    if problems:
        raise ValueError("event consistency failed:\n- " + "\n- ".join(problems))
    print(f"validated {len(run_paths)} catalog-routed literature-review runs")


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/run.py."""
    try:
        validate(Path(args.root))
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    return 0
