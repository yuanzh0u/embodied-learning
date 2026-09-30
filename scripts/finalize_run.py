#!/usr/bin/env python3
"""Mechanize the settle/publish tail of a literature-review run.

One command replaces the error-prone hand sequence the writer agent used to
perform (patch run.json fields → run both gates → copy evidence/ → flip
settled → register catalog → rebuild wiki). Steps, each idempotent:

1. Fill run.json mechanically: event_count / evidence_papers (from the
   evidence set), candidate_count / full_text_count (from
   pipeline-summary.json), files.evidence (always rebuilding
   evidence.jsonl from evidence/*.jsonl + the flat-run canonical via
   lib.review_runs.consolidate_evidence), files.outputs, and
   style + scope_note when only one deliverable exists.
2. Coverage floor: a systematic review citing too few papers is a filter
   failure, not a writing failure — refuse (exit 2) with the exact driver
   resume command when the evidence covers fewer papers than the mode floor.
3. Gate 1: check_run_bundle.py.
4. Gate 2: audit_citations.py over every deliverable.
5. Flip status → settled and publish run.json + deliverables + evidence into
   <kb-root>/evidence/<run>/.
6. register_run.py (idempotent, KB-locked catalog append).
7. build_research_wiki.py snapshot rebuild (unless --skip-wiki).

Gate failures print mechanically what is missing; they are fix-and-rerun
conditions, never stop-and-explain conditions.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from lib.layout import default_kb_root, find_roots
    from lib.review_runs import (
        CITED_PAPER_FLOORS,
        STANDARD_ARTICLES,
        STYLE_TO_FILE,
        build_trace_map,
        consolidate_evidence,
        register_run_in_catalog,
    )
except ImportError:  # installed console-script entry: package import path
    from wiki_scripts.lib.layout import default_kb_root, find_roots
    from wiki_scripts.lib.review_runs import (
        CITED_PAPER_FLOORS,
        STANDARD_ARTICLES,
        STYLE_TO_FILE,
        build_trace_map,
        consolidate_evidence,
        register_run_in_catalog,
    )

APPENDIX = "evidence-appendix.md"
PUBLISH_FILES = [APPENDIX, "trace-map.json", "evidence.jsonl", "pipeline-summary.json"]
# Positioning-only tier inside evidence/: its per-paper JSONL is one virtual
# file (abstract-tier.jsonl), never a deep-read paper, so both the per-file and
# the consolidated counting paths must skip it.
ABSTRACT_TIER = "abstract"
ABSTRACT_TIER_STEM = "abstract-tier"


def log(message: str) -> None:
    print(f"[finalize] {message}", flush=True)


def run_step(title: str, command: list[str]) -> None:
    """Run one gate/publish subprocess; a failure is a fix-and-rerun signal."""
    log(f"{title}：{' '.join(command[-3:])}")
    result = subprocess.run(command)
    if result.returncode != 0:
        log(f"{title} 未过（exit {result.returncode}）。按上方输出修复后重跑 finalize_run.py；"
            "门禁未过不是提前停止的理由。")
        raise SystemExit(2)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def evidence_papers(run_dir: Path, evidence_jsonl: Path) -> int:
    """Distinct papers backing the full-text evidence.

    Abstract-tier events are positioning-only: they never count toward the
    cited-paper floor, so both counting paths skip ``tier: abstract``."""
    per_paper = {
        path.stem
        for path in (run_dir / "evidence").glob("*.jsonl")
        if path.stem != ABSTRACT_TIER_STEM
        and any(line.strip() for line in path.read_text(encoding="utf-8").splitlines())
    }
    if per_paper:
        return len(per_paper)
    # Consolidated-only fallback: distinct source paper ids across events.
    papers: set[str] = set()
    for line in evidence_jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if str(event.get("tier") or "") == ABSTRACT_TIER:
            continue
        paper = event.get("paper") if isinstance(event.get("paper"), dict) else {}
        paper_id = (
            paper.get("arxiv_id")
            or (event.get("source") or {}).get("paper_id")
            or event.get("paper_id")
        )
        if paper_id:
            papers.add(str(paper_id))
    return len(papers)


def abstract_papers(evidence_jsonl: Path) -> int:
    """Distinct papers contributing abstract-tier (positioning) events."""
    papers: set[str] = set()
    for line in evidence_jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if str(event.get("tier") or "") != ABSTRACT_TIER:
            continue
        paper = event.get("paper") if isinstance(event.get("paper"), dict) else {}
        arxiv_id = str(paper.get("arxiv_id") or "").strip()
        if arxiv_id:
            papers.add(arxiv_id)
    return len(papers)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="In-progress run directory (holds run.json).")
    parser.add_argument("--kb-root", default=str(default_kb_root()), help="KB root to publish into.")
    parser.add_argument("--style", choices=sorted(STYLE_TO_FILE), help="Declare a reduced single-style scope.")
    parser.add_argument("--scope-note", help="Why the user asked for a single style (with --style).")
    parser.add_argument("--skip-wiki", action="store_true", help="Skip the wiki snapshot rebuild.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_dir = Path(args.run_dir).expanduser().resolve()
    kb_root = Path(args.kb_root).expanduser().resolve()
    run_json_path = run_dir / "run.json"
    if not run_json_path.is_file():
        log(f"run.json 不存在：{run_json_path}")
        return 1
    manifest = load_json(run_json_path)

    # ---- 1. fill the manifest mechanically -------------------------------
    evidence_jsonl = consolidate_evidence(run_dir)
    event_ids: set[str] = set()
    for line in evidence_jsonl.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                event_ids.add(str(json.loads(line).get("id") or line))
            except json.JSONDecodeError:
                event_ids.add(line)
    papers = evidence_papers(run_dir, evidence_jsonl)
    manifest["event_count"] = len(event_ids)
    manifest["evidence_papers"] = papers
    manifest["abstract_papers"] = abstract_papers(evidence_jsonl)
    summary_path = run_dir / "pipeline-summary.json"
    if summary_path.is_file():
        summary = load_json(summary_path)
        for key in ("candidate_count", "full_text_recovered_count"):
            value = summary.get(key)
            if isinstance(value, int):
                manifest["candidate_count" if key == "candidate_count" else "full_text_count"] = value
    style = args.style or manifest.get("style")
    if style and style in STYLE_TO_FILE:
        # Declared style → its own file is the only deliverable. A disk scan
        # over STYLE_TO_FILE would sweep in mechanically generated artifacts
        # that happen to share a filename (survey maps to review-packet.md,
        # which the packet script also emits as a briefing) and then fail the
        # citation gate on the packet's bare inventory IDs.
        declared_file = STYLE_TO_FILE[style]
        if not (run_dir / declared_file).is_file():
            log(f"声明了 style={style} 但交付物 {declared_file} 不存在：先补写成稿再 finalize。")
            return 2
        deliverables = [declared_file]
    else:
        # Undeclared scope → the three prose deliverables only. The mechanical
        # briefing (review-packet.md) shares its filename with survey's style
        # file and exists in every run, so sweeping STYLE_TO_FILE.values()
        # would audit the briefing's bare inventory IDs as if it were prose.
        # survey/slide-deck become deliverables only via explicit --style.
        deliverables = [name for name in STANDARD_ARTICLES if (run_dir / name).is_file()]
    if not style and len(deliverables) == 1:
        style = next(name for name, filename in STYLE_TO_FILE.items() if filename == deliverables[0])
    if style:
        manifest["style"] = style
        scope_note = args.scope_note or manifest.get("scope_note") or "用户只要单一风格成稿（见工作流对话记录）"
        manifest["scope_note"] = scope_note
    elif not args.style and not manifest.get("style") and len(deliverables) < 3:
        log(f"成稿不足三种且未声明 --style：现有 {deliverables or '无'}；请补写成稿或用 --style 声明缩减范围。")
        return 2
    manifest.setdefault("files", {})
    manifest["files"]["evidence"] = evidence_jsonl.relative_to(run_dir).as_posix()
    outputs = deliverables + ([APPENDIX] if (run_dir / APPENDIX).is_file() else [])
    if outputs:
        manifest["files"]["outputs"] = outputs
    write_json(run_json_path, manifest)
    log(f"run.json 已盖章：event_count={len(event_ids)} evidence_papers={papers} "
        f"abstract_papers={manifest['abstract_papers']} style={style or '（三风格）'}")

    # ---- 2. coverage floor -------------------------------------------------
    review_mode = str(manifest.get("review_mode") or "")
    if not review_mode and summary_path.is_file():
        review_mode = str(load_json(summary_path).get("review_mode") or "")
    floor = CITED_PAPER_FLOORS.get(review_mode)
    if floor and papers < floor:
        log(f"证据仅覆盖 {papers} 篇论文，低于 {review_mode} 模式下限 {floor} 篇。"
            "这是筛选/深读环节的覆盖不足，不是写作问题：续跑驱动补足深读后重跑 finalize：\n"
            f"  python3 run_review_pipeline.py --run-dir {run_dir} --kb-root {args.kb_root} "
            f"--review-mode {review_mode} --deep-read-limit {max(papers * 2, floor * 2)}")
        return 2

    # ---- 2b. trace map (mechanical; the writer never hand-builds it) ------
    _, skills_root, _ = find_roots()
    trace_ok, trace_problems = build_trace_map(run_dir, skills_root)
    if not trace_ok:
        for line in trace_problems:
            log(f"trace-map: {line}")
        log("trace-map 未生成：成稿引用了证据集之外的论文（UNCOVERED）或输入缺失。"
            "修法：删改成稿中无证据支撑的 arXiv 引用，或补证据后重跑 finalize_run.py。"
            "门禁未过不是提前停止的理由。")
        return 2

    # ---- 3+4. the two gates -------------------------------------------------
    # check_run_bundle demands status=settled, so flip first and revert on
    # failure: a gate-failed run must never stay marked settled.
    manifest["status"] = "settled"
    write_json(run_json_path, manifest)
    try:
        scripts_root = Path(__file__).resolve().parent
        run_step("check_run_bundle", [sys.executable, str(scripts_root / "check_run_bundle.py"), str(run_dir)])
        audit_cmd = [sys.executable, str(scripts_root / "audit_citations.py")]
        for name in (deliverables or [n for n in STANDARD_ARTICLES if (run_dir / n).is_file()]):
            audit_cmd += ["--article", str(run_dir / name)]
        audit_cmd += [
            "--appendix", str(run_dir / APPENDIX),
            "--evidence-jsonl", str(evidence_jsonl),
            "--run-json", str(run_json_path),
        ]
        run_step("audit_citations", audit_cmd)
    except SystemExit:
        manifest["status"] = "in-progress"
        write_json(run_json_path, manifest)
        log("门禁未过，run.json 已回退 in-progress。")
        raise

    # ---- 5. publish ----------------------------------------------------------
    manifest["status"] = "settled"
    write_json(run_json_path, manifest)
    dest = kb_root / "evidence" / run_dir.name
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(run_json_path, dest / "run.json")
    for name in PUBLISH_FILES + list(STYLE_TO_FILE.values()):
        source = run_dir / name
        if source.is_file():
            shutil.copy2(source, dest / name)
    if (run_dir / "evidence").is_dir():
        shutil.copytree(run_dir / "evidence", dest / "evidence", dirs_exist_ok=True)
    log(f"已落盘 evidence/{dest.name}/")

    # ---- 6+7. catalog row + wiki snapshot ----------------------------------
    registered = register_run_in_catalog(kb_root, dest / "run.json")
    log("catalog 已登记" if registered else "catalog 已包含该 run（幂等跳过）")
    if not args.skip_wiki:
        run_step("build_research_wiki", [
            sys.executable, str(scripts_root / "build_research_wiki.py"),
            "--kb-root", str(kb_root), "--output", str(kb_root / "wiki" / "data"),
        ])
    log("settle 完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
