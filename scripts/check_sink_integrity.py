#!/usr/bin/env python3
"""Reconcile work/ runs, evidence/ bundles, and the literature-review catalog.

Interrupted sinks leave drift that no single artifact records: a run can be
settled in work/ without an evidence/ copy, the catalog can link to a missing
bundle, or a gate-failed run can sit in a catalog section that requires
passing gates. This script re-derives the truth from those three places and
reports mismatches. Informational notes (in-flight runs, unregistered legacy
bundles, work copies of already-sunk runs) never affect the exit code.

Exit code is non-zero when hard drift is found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from check_run_bundle import check_run_bundle
except ImportError:  # loaded as a module by tests
    import importlib.util

    _spec = importlib.util.spec_from_file_location(
        "check_run_bundle", Path(__file__).resolve().parent / "check_run_bundle.py"
    )
    assert _spec and _spec.loader
    _module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    check_run_bundle = _module.check_run_bundle

GATE_PREFIX = "coverage/saturation gate not passed"
GATE_FAILED_MARKER = "覆盖门未过"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root containing work/, evidence/, and knowledge/ (default: this repo).",
    )
    return parser.parse_args()


def catalog_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    header = "(top)"
    pattern = re.compile(r"\]\(\.\./evidence/(literature-review-[^)/\s]+)/")
    for line in text.splitlines():
        if line.startswith("## "):
            header = line[3:].strip()
        for match in pattern.finditer(line):
            sections.setdefault(header, []).append(match.group(1))
    return sections


def main() -> int:
    args = parse_args()
    repo = Path(args.repo_root).resolve()
    work = repo / "work"
    evidence = repo / "evidence"
    work_runs = {d.name: d for d in sorted(work.glob("literature-review-*")) if d.is_dir()} if work.is_dir() else {}
    evidence_runs = {d.name: d for d in sorted(evidence.glob("literature-review-*")) if d.is_dir()}

    drift: list[str] = []
    notes: list[str] = []

    for name, run_dir in work_runs.items():
        manifest_path = run_dir / "run.json"
        if not manifest_path.is_file():
            notes.append(f"work run without run.json: {name}")
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            drift.append(f"work run.json invalid JSON: {name} ({exc})")
            continue
        status = str(manifest.get("status") or "")
        if status == "settled":
            if name not in evidence_runs:
                drift.append(f"settled run never sunk to evidence/: work/{name}")
            else:
                notes.append(f"settled run already sunk; work copy is a deletable remnant: work/{name}")
        elif status == "in-progress":
            notes.append(f"in-flight run: work/{name}")

    catalog_path = repo / "knowledge" / "literature-review-catalog.md"
    sections = catalog_sections(catalog_path.read_text(encoding="utf-8")) if catalog_path.is_file() else {}
    registered: set[str] = set()
    for header, names in sections.items():
        gate_exempt = GATE_FAILED_MARKER in header
        for name in names:
            registered.add(name)
            if name not in evidence_runs:
                drift.append(f"catalog link to missing evidence dir (under '{header}'): {name}")
                continue
            problems = check_run_bundle(evidence_runs[name])
            gate = [item for item in problems if item.startswith(GATE_PREFIX)]
            hard = [item for item in problems if not item.startswith(GATE_PREFIX)]
            if hard:
                drift.append(
                    f"registered bundle violates the contract (under '{header}'): {name}: {'; '.join(hard[:2])}"
                )
            if gate and not gate_exempt:
                drift.append(f"gate-failed run registered under '{header}'; move it to the gate-failed section: {name}")

    for name in evidence_runs:
        if name not in registered and "-reader-v" not in name:
            notes.append(f"evidence bundle not referenced in catalog: {name}")

    print(f"work runs: {len(work_runs)} | evidence bundles: {len(evidence_runs)} | catalog-registered: {len(registered)}")
    if notes:
        print(f"\n{len(notes)} note(s) (informational):")
        for item in notes:
            print(f"- {item}")
    if drift:
        print(f"\n{len(drift)} drift item(s):")
        for item in drift:
            print(f"- {item}")
        return 1
    print("\nno drift")
    return 0


if __name__ == "__main__":
    sys.exit(main())
