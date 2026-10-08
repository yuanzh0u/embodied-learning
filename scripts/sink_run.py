#!/usr/bin/env python3
"""Sink a settled literature-review run bundle into the evidence layer.

One idempotent command for the sink steps that were previously done by hand:
copy the bundle to evidence/, re-audit it in place, and stamp a sink checklist
into run.json. Sessions interrupted between those steps left runs with
status=settled but no evidence copy and no catalog entry — invisible until a
manual audit. This closes that window:

- refuses bundles that violate the check_run_bundle contract
- refuses gate-failed (coverage/saturation) runs unless --allow-gate-fail is
  passed; such runs must be registered in the catalog's dedicated
  gate-failed section, never the main results table
- stamps run.json with a sink_checklist so any later session can see how far
  the sink got
- detects catalog registration by searching the catalog for the evidence
  path and prints a ready-to-paste row template when it is missing

Exit code 0 on success (including an idempotent re-run), 1 on refusal.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path
from typing import Any

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
GATE_FAILED_SECTION = "覆盖门未过的补沉淀 run"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", help="Path to the settled run bundle (work/ scratch or a bundle subdir).")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root containing evidence/ and knowledge/ (default: this repo).",
    )
    parser.add_argument(
        "--allow-gate-fail",
        action="store_true",
        help="Sink a bundle whose coverage/saturation gate failed; its catalog row must then go to the dedicated gate-failed section.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the sink plan without writing anything.")
    return parser.parse_args()


def load_manifest(run_dir: Path) -> tuple[dict[str, Any], str | None]:
    path = run_dir / "run.json"
    if not path.is_file():
        return {}, f"no run.json in {run_dir}"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, f"run.json is invalid JSON ({exc})"
    return manifest, None


def coverage_scale(run_dir: Path, manifest: dict[str, Any]) -> str:
    rel = (manifest.get("files") or {}).get("coverage_report")
    if not isinstance(rel, str) or not (run_dir / rel).is_file():
        return "? / ? / ?"
    try:
        coverage = json.loads((run_dir / rel).read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "? / ? / ?"
    return " / ".join(str(coverage.get(key, "?")) for key in ("candidate_count", "full_text_count", "accepted_count"))


def catalog_row(manifest: dict[str, Any], run_dir: Path, gate_detail: str | None) -> str:
    topic = manifest.get("topic") or run_dir.name
    knowledge_ids = ", ".join(manifest.get("knowledge_ids") or []) or "EA-?"
    links = f"[run](../evidence/{run_dir.name}/run.json) · [packet](../evidence/{run_dir.name}/review-packet.md)"
    if gate_detail:
        return f"| LR-<NEW-ID> | {topic} | {knowledge_ids} | {coverage_scale(run_dir, manifest)} | {gate_detail} | {links} |"
    return f"| LR-<NEW-ID> | {topic} | {knowledge_ids} | {coverage_scale(run_dir, manifest)} | {links} |"


def main() -> int:
    args = parse_args()
    repo = Path(args.repo_root).resolve()
    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"not a directory: {run_dir}")
        return 1
    if not run_dir.name.startswith("literature-review-"):
        print(f"refusing: {run_dir.name} does not match literature-review-<topic>-<date>")
        return 1
    evidence_root = repo / "evidence"
    if evidence_root.is_dir() and run_dir.parent.resolve() == evidence_root.resolve():
        print("refusing: this bundle is already inside evidence/ — nothing to sink")
        return 1

    manifest, error = load_manifest(run_dir)
    if error:
        print(f"refusing: {error}")
        return 1
    status = str(manifest.get("status") or "")
    if status != "settled":
        print(f"refusing: status is {status!r}; finish the run and settle it before sinking")
        return 1

    problems = check_run_bundle(run_dir)
    gate = [item for item in problems if item.startswith(GATE_PREFIX)]
    hard = [item for item in problems if not item.startswith(GATE_PREFIX)]
    if hard:
        print(f"refusing: {len(hard)} bundle-contract problem(s):")
        for item in hard:
            print(f"- {item}")
        return 1
    gate_detail = "; ".join(gate) if gate else None
    if gate and not args.allow_gate_fail:
        print("refusing: coverage/saturation gate not passed")
        for item in gate:
            print(f"- {item}")
        print("pass --allow-gate-fail to sink anyway; the catalog row must then go to the")
        print(f"'{GATE_FAILED_SECTION}' section, never the main results table")
        return 1

    catalog_path = repo / "knowledge" / "literature-review-catalog.md"
    catalog = catalog_path.read_text(encoding="utf-8") if catalog_path.is_file() else ""
    registered = f"evidence/{run_dir.name}/" in catalog
    target = evidence_root / run_dir.name
    checklist = {
        "copied": True,
        "catalog_registered": registered,
        "bundle_audited": True,
        "gate_passed": not gate,
        "sinked_at": dt.date.today().isoformat(),
    }
    if args.dry_run:
        print(f"dry-run: would sink {run_dir.name} -> {target}")
        print(f"  gate_passed: {checklist['gate_passed']}")
        print(f"  catalog_registered: {registered}")
        return 0

    manifest["sink_checklist"] = checklist
    manifest_path = run_dir / "run.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if target.exists():
        missing = []
        for path in sorted(run_dir.rglob("*")):
            if not path.is_file() or path.name == ".DS_Store":
                continue
            rel = path.relative_to(run_dir)
            if not (target / rel).exists():
                missing.append(rel)
        for rel in missing:
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(run_dir / rel, dest)
        # the stamped manifest is authoritative; sync it into the evidence copy
        (target / "run.json").write_text(manifest_path.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"target exists: copied {len(missing)} missing file(s); existing files untouched")
    else:
        evidence_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(run_dir, target, ignore=shutil.ignore_patterns(".DS_Store"))
        print(f"copied bundle to {target}")

    problems = check_run_bundle(target)
    if gate:
        # the gate failure was explicitly allowed pre-copy; the same finding in
        # the evidence copy is expected, not a new problem
        problems = [item for item in problems if not item.startswith(GATE_PREFIX)]
    if problems:
        print("warning: evidence copy fails the bundle contract:")
        for item in problems:
            print(f"- {item}")
        return 1

    if registered:
        print("catalog: already registered")
    else:
        print("catalog: NOT registered — add this row:")
        print(catalog_row(manifest, run_dir, gate_detail))
        if gate:
            print(f"  ^ in the '{GATE_FAILED_SECTION}' section (gate failed)")
    print("sink complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
