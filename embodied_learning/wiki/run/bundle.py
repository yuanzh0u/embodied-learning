"""Check a literature-review run folder against the bundle-completeness contract.

The folder name `literature-review-<topic>-<date>` IS the contract trigger:
such a run must ship the three-style deliverable bundle, a self-contained
evidence set, and a standard-schema run.json — unless run.json explicitly
declares a reduced scope (`style` + `scope_note`). This catches the silent-
bypass failure mode where an agent hand-writes one article, invents manifest
field names, and skips the other deliverables with zero warnings.

Exit code is non-zero when any problem is found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from embodied_learning.config import STYLE_TO_FILE
from embodied_learning.wiki.run.manifest import declared_style

DELIVERABLES = [
    "scientific-memo_keyan.md",
    "zhihu-explainer_zhihu.md",
    "xiaohongshu-post_xiaohongshu.md",
]
APPENDIX = "evidence-appendix.md"
REQUIRED_FIELDS = ["run", "topic", "time_range", "event_count", "files"]
V2_REQUIRED_FILES = ["query_plan", "candidate_registry", "coverage_report"]
# Drifted names seen in real runs -> the standard field to use instead.
FIELD_DRIFT = {
    "selected_event_count": "event_count",
    "events": "event_count",
    "sources": "source_runs",
}
FILES_DRIFT = {
    "memo": "outputs (list)",
    "output": "outputs (list)",
    "articles": "outputs (list)",
}



def load_local_event_ids(run_dir: Path, files: dict) -> tuple[set[str], list[str]]:
    """Deduplicated event IDs from the run's own evidence set (fresh + reused)."""
    problems: list[str] = []
    ids: set[str] = set()
    paths: list[str] = []
    evidence = files.get("evidence")
    if isinstance(evidence, str):
        paths.append(evidence)
    reused = files.get("reused_evidence")
    if isinstance(reused, list):
        paths.extend(item for item in reused if isinstance(item, str))
    if not paths:
        problems.append(
            "no local evidence set: files.evidence (and/or files.reused_evidence) must list "
            "JSONL inside the run folder so it is self-contained"
        )
        return ids, problems
    for rel in paths:
        path = run_dir / rel
        if not path.is_file():
            problems.append(f"evidence file listed but missing: {rel}")
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"{rel}:{lineno}: invalid JSONL line")
                continue
            event_id = str(event.get("event_id") or "")
            if event_id:
                ids.add(event_id)
    return ids, problems


def check_run_bundle(run_dir: Path, *, pre_settle: bool = False) -> list[str]:
    """Problems in the bundle contract.

    ``pre_settle=True`` audits a run that is still ``in-progress`` (the writer
    stage, before ``run.py finalize``): the lifecycle line and the
    published-bundle-only checks are skipped, everything the writer can fix is
    still reported. Without it an in-progress run always fails by design.
    """
    problems: list[str] = []
    manifest_path = run_dir / "run.json"
    if not manifest_path.is_file():
        return [f"run.json missing in {run_dir}"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"run.json: invalid JSON ({exc})"]

    # Lifecycle: an in-progress run is by definition not a settled bundle.
    status = str(manifest.get("status") or "").strip()
    if status and status not in {"in-progress", "settled"}:
        problems.append(f"run.json: unknown status `{status}` (use `in-progress` or `settled`)")
    if status == "in-progress" and not pre_settle:
        problems.append(
            "run not settled: status is `in-progress` — finish the bundle (promote evidence, "
            "write the three articles, pass both gates) and flip status to `settled` "
            "(run.py finalize does the flip; for a pre-settle audit use --pre-settle)"
        )

    # Standard schema: required fields present, drifted names rejected.
    for drifted, standard in FIELD_DRIFT.items():
        if drifted in manifest:
            problems.append(f"run.json: non-standard field `{drifted}` — use `{standard}`")
    for field in REQUIRED_FIELDS:
        if field not in manifest:
            problems.append(f"run.json: missing required field `{field}`")
    files = manifest.get("files")
    if not isinstance(files, dict):
        return problems + ["run.json: `files` must be an object"]
    for drifted, standard in FILES_DRIFT.items():
        if drifted in files:
            problems.append(f"run.json: non-standard files key `{drifted}` — use `{standard}`")
    outputs = files.get("outputs")
    if outputs is not None and not isinstance(outputs, list):
        problems.append("run.json: files.outputs must be a list")
        outputs = None

    workflow_version = manifest.get("workflow_version", 1)
    if workflow_version == 2:
        review_mode = manifest.get("review_mode")
        if review_mode not in {"rapid", "scoping", "systematic"}:
            problems.append("run.json: workflow_version 2 requires review_mode rapid|scoping|systematic")
        # Self-containment (files.*) is a PUBLISHED-bundle contract: the keys
        # are stamped by run.py finalize, which runs AFTER the launcher's gate
        # loop. Enforcing them on an in-progress run is a chicken-and-egg that
        # the loop can never clear — it only ever passed because a writer agent
        # violated its instructions and ran finalize first (2026-10-13, run 08
        # died here while run 01 survived on that violation).
        if status == "settled":
            for key in V2_REQUIRED_FILES:
                if not isinstance(files.get(key), str):
                    problems.append(f"run.json: workflow_version 2 requires files.{key}")
        coverage_rel = files.get("coverage_report")
        if isinstance(coverage_rel, str) and (run_dir / coverage_rel).is_file():
            try:
                coverage = json.loads((run_dir / coverage_rel).read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                problems.append(f"coverage report is invalid JSON: {exc}")
            else:
                stop = coverage.get("stop_assessment") or {}
                if not bool(stop.get("ready_to_stop")):
                    unresolved = [str(item) for item in (stop.get("unresolved") or [])]
                    # Explicit escape hatch: a run may declare the gate names it
                    # is settling past (e.g. saturation on a broad field), with
                    # the justification carried in run.json notes. Undeclared
                    # failures stay hard failures.
                    declared = manifest.get("gate_exceptions") or []
                    still_open = [item for item in unresolved if item not in declared]
                    if still_open:
                        problems.append(
                            "coverage/saturation gate not passed"
                            + (f": {', '.join(still_open)}" if still_open else "")
                            + " — 修法二选一：①续跑 run.py pipeline --run-dir "
                            f"{run_dir} 补检索/深读后重算；②确属不可比的一次性检索时声明豁免——"
                            "python3 run.py finalize --run-dir "
                            f"{run_dir} --declare-gate-exception saturation --reason \"...\" "
                            "（理由会记入 notes；勿手改 run.json）。"
                            "已声明的豁免："
                            + (", ".join(str(item) for item in declared) if declared else "无")
                        )
    elif workflow_version != 1:
        problems.append(f"run.json: unsupported workflow_version {workflow_version!r}")

    # Every listed file must exist.
    listed: list[str] = []
    for value in files.values():
        if isinstance(value, str):
            listed.append(value)
        elif isinstance(value, list):
            listed.extend(item for item in value if isinstance(item, str))
    for name in listed:
        if not (run_dir / name).is_file():
            problems.append(
                f"run.json lists missing file: {name}"
                " — 修复产物缺失（evidence.jsonl/appendix 等可由 run.py finalize 重跑自动重建），"
                "或从 files 里移除过期条目；勿手改 run.json 的 event_count。"
            )

    # Self-contained evidence, and event_count must match it. Both are
    # published-bundle contracts: files.evidence is stamped by run.py finalize,
    # which runs after the launcher's gate loop (see the files.* note above).
    local_ids, evidence_problems = load_local_event_ids(run_dir, files)
    if status == "settled":
        problems.extend(evidence_problems)
    recorded = manifest.get("event_count")
    if isinstance(recorded, int) and local_ids and recorded != len(local_ids):
        problems.append(
            f"run.json event_count={recorded} but local evidence has {len(local_ids)} deduplicated events"
            " — 重跑 run.py finalize 会按 evidence/ 自动重建 evidence.jsonl 并重新盖章 event_count；"
            "勿手改 run.json。"
        )

    # Bundle completeness: three styles by default, or a declared reduced scope.
    # The declaration may live in `inputs.target_style` (the interview/CLI
    # choice stamped at run birth) because this gate runs at the writer stage,
    # BEFORE finalize stamps `style` + `scope_note` — reading only `style`
    # made a single-style run fail on two phantom deliverables (2026-10-21
    # 点云匹配). scope_note is finalize's field; the recorded interview answer
    # is the intent until then, so it is only demanded for a settled run.
    style = str(manifest.get("style") or "").strip()
    if style:
        if style not in STYLE_TO_FILE:
            problems.append(
                f"run.json: style `{style}` is not a supported settled scope ({', '.join(sorted(STYLE_TO_FILE))})"
            )
            required = []
        else:
            required = [STYLE_TO_FILE[style]]
            if status == "settled" and not str(manifest.get("scope_note") or "").strip():
                problems.append(
                    "run.json: reduced scope declared via `style` but `scope_note` is missing — "
                    "record why the user asked for a single style"
                )
    else:
        requested = declared_style(manifest)  # inputs.target_style fallback
        if requested and requested not in STYLE_TO_FILE:
            problems.append(
                f"run.json: inputs.target_style `{requested}` is not a supported settled scope "
                f"({', '.join(sorted(STYLE_TO_FILE))})"
            )
            required = []
        elif requested:
            style = requested
            required = [STYLE_TO_FILE[style]]
        else:
            required = list(DELIVERABLES)
    for name in required:
        if not (run_dir / name).is_file():
            problems.append(
                f"missing deliverable: {name}"
                + ("" if style else " (three styles are the default; declare style+scope_note to reduce)")
            )
        elif outputs is not None and name not in outputs:
            problems.append(f"run.json: deliverable {name} exists but is not listed in files.outputs")
    if required and not (run_dir / APPENDIX).is_file():
        problems.append(f"missing {APPENDIX} (citation anchors for the deliverables)")

    return problems


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/run.py."""
    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"not a directory: {run_dir}")
        return 1
    if not re.match(r"literature-review-.+", run_dir.name):
        print(f"note: {run_dir.name} does not match literature-review-<topic>-<date>; contract still applied")
    problems = check_run_bundle(run_dir, pre_settle=bool(getattr(args, "pre_settle", False)))
    if problems:
        print(f"{len(problems)} problem(s):")
        for item in problems:
            print(f"- {item}")
        return 1
    if getattr(args, "pre_settle", False):
        print("run bundle OK (pre-settle: lifecycle and published-bundle fields are finalize's job)")
    else:
        print("run bundle OK")
    return 0
