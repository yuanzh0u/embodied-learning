#!/usr/bin/env python3
"""Validate every literature-review run routed by the current catalog.

The catalog is the version-selection layer for this repository. Historical
and superseded runs remain append-only under ``evidence/`` but are not CI
targets unless the catalog routes to them.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_LINK = re.compile(r"\]\(\.\./(evidence/[^)]+/run\.json)\)")
STANDARD_ARTICLES = [
    "scientific-memo_keyan.md",
    "zhihu-explainer_zhihu.md",
    "xiaohongshu-post_xiaohongshu.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root to validate.")
    return parser.parse_args()


def catalog_run_paths(root: Path) -> list[Path]:
    catalog = root / "knowledge" / "literature-review-catalog.md"
    text = catalog.read_text(encoding="utf-8")
    relative_paths = sorted(set(CATALOG_LINK.findall(text)))
    if not relative_paths:
        raise ValueError(f"no run manifests routed by {catalog.relative_to(root)}")

    paths: list[Path] = []
    for relative in relative_paths:
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"catalog run escapes repository root: {relative}") from exc
        paths.append(path)
    return paths


def evidence_paths(run_json: Path, manifest: dict[str, object]) -> list[Path]:
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError(f"{run_json}: files must be an object")

    names: list[str] = []
    evidence = files.get("evidence")
    if isinstance(evidence, str):
        names.append(evidence)
    reused = files.get("reused_evidence")
    if isinstance(reused, list):
        names.extend(item for item in reused if isinstance(item, str))
    if not names:
        raise ValueError(f"{run_json}: no local evidence file is declared")
    return [run_json.parent / name for name in names]


def event_consistency_problems(run_paths: Iterable[Path]) -> list[str]:
    """Allow exact event reuse while rejecting ID collisions or local duplicates."""

    owners: dict[str, tuple[str, str]] = {}
    problems: list[str] = []
    for run_json in run_paths:
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        for evidence_path in evidence_paths(run_json, manifest):
            local_ids: set[str] = set()
            for line_number, line in enumerate(evidence_path.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                event = json.loads(line)
                event_id = str(event.get("event_id") or "")
                if not event_id:
                    problems.append(f"{evidence_path}:{line_number}: missing event_id")
                    continue
                if event_id in local_ids:
                    problems.append(f"{evidence_path}:{line_number}: duplicate event_id {event_id}")
                    continue
                local_ids.add(event_id)

                canonical = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                prior = owners.get(event_id)
                location = f"{evidence_path}:{line_number}"
                if prior is None:
                    owners[event_id] = (canonical, location)
                elif prior[0] != canonical:
                    problems.append(f"event_id {event_id} differs between {prior[1]} and {location}")
    return problems


def run(command: list[str], root: Path) -> None:
    print(f"+ {shlex.join(command)}", flush=True)
    subprocess.run(command, cwd=root, check=True)


def validate(root: Path) -> None:
    root = root.resolve()
    run_paths = catalog_run_paths(root)

    run([sys.executable, "scripts/check_kb_links.py", "--root", "."], root)
    for run_json in run_paths:
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        if manifest.get("status") != "settled":
            raise ValueError(f"catalog routes to non-settled run: {run_json.relative_to(root)}")

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
