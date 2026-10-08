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
    from lib.layout import default_kb_root, find_roots, infer_kb_root
    from lib.review_runs import (
        CITED_PAPER_FLOORS,
        STANDARD_ARTICLES,
        STYLE_TO_FILE,
        build_trace_map,
        consolidate_evidence,
        register_run_in_catalog,
    )
except ImportError:  # installed console-script entry: package import path
    from wiki_scripts.lib.layout import default_kb_root, find_roots, infer_kb_root
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
    parser.add_argument(
        "--kb-root",
        default=None,
        help="KB root to publish into. Default: inferred from --run-dir "
        "(<kb-root>/work/<run> layout); only needed for non-standard layouts.",
    )
    parser.add_argument("--style", choices=sorted(STYLE_TO_FILE), help="Declare a reduced single-style scope.")
    parser.add_argument("--scope-note", help="Why the user asked for a single style (with --style).")
    parser.add_argument(
        "--declare-gate-exception",
        action="append",
        default=[],
        metavar="NAME",
        help="Mechanical gate_exceptions declaration: waive the named gate (e.g. "
        "saturation / cited_paper_floor) with a --reason justification recorded in "
        "run.json notes. Never hand-edit run.json for this.",
    )
    parser.add_argument("--reason", default="", help="Justification for --declare-gate-exception.")
    parser.add_argument("--skip-wiki", action="store_true", help="Skip the wiki snapshot rebuild.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_dir = Path(args.run_dir).expanduser().resolve()
    inferred = infer_kb_root(run_dir)
    if args.kb_root is None:
        kb_root = inferred or default_kb_root()
        if inferred is None:
            log(f"run-dir 不在 <kb-root>/work/ 布局下，无法推断知识库根；使用默认 {kb_root}。")
            log("若这不是目标知识库，请显式传 --kb-root。")
    else:
        kb_root = Path(args.kb_root).expanduser().resolve()
    # Guard: never publish a run into a KB that does not own its work/ dir.
    # (2026-09-30 absolute-pose: the writer omitted --kb-root, the default
    # swallowed it, and the whole publish landed in ~/Documents/arxiv while
    # the run lived under the /mount/TEST wiki KB.)
    if inferred is not None and kb_root != inferred:
        log(f"拒绝落盘：run-dir 归属知识库 {inferred}，与目标 --kb-root {kb_root} 不一致。")
        log(f"修法：去掉 --kb-root（会自动推断为 {inferred}），或改传 --kb-root {inferred}。")
        log("落错知识库 = evidence/、catalog、wiki 快照全部进错库。")
        return 2
    log(f"知识库根：{kb_root}" + ("（由 run-dir 推断）" if args.kb_root is None and inferred else ""))
    run_json_path = run_dir / "run.json"
    if not run_json_path.is_file():
        log(f"run.json 不存在：{run_json_path}")
        return 1
    manifest = load_json(run_json_path)

    # ---- 0. mechanical gate_exceptions declaration -------------------------
    if args.declare_gate_exception:
        if not str(args.reason or "").strip():
            log("--declare-gate-exception 必须带 --reason 写明正当理由（会记入 run.json notes）。")
            return 2
        names = [str(item) for item in args.declare_gate_exception]
        manifest["gate_exceptions"] = list(
            dict.fromkeys([*(str(x) for x in (manifest.get("gate_exceptions") or [])), *names])
        )
        notes = manifest.get("notes")
        entry = (
            f"{__import__('datetime').date.today().isoformat()}: gate_exception {', '.join(names)} — {args.reason}"
        )
        manifest["notes"] = [notes, entry] if isinstance(notes, str) else (notes or []) + [entry]
        write_json(run_json_path, manifest)
        log(f"已声明 gate 豁免：{', '.join(names)}（理由已记入 notes）")

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
    declared_gates = [str(item) for item in (manifest.get("gate_exceptions") or [])]
    if floor and papers < floor and "cited_paper_floor" not in declared_gates:
        # 精读数量不够 = 设计内的用户决策点（2026-09-30 定案），不是可修复故障：
        # 汇报选定的精读论文列表 → 停轮等决策（补充信息或扩大综述范围）。
        log(f"精读数量不够：证据仅覆盖 {papers} 篇论文，低于 {review_mode} 模式下限 {floor} 篇。")
        log("已选定并深读的论文列表（决策用）：")
        titles: dict[str, str] = {}
        registry_path = run_dir / "candidate-registry.json"
        if registry_path.is_file():
            for record in (load_json(registry_path).get("candidates") or []):
                if isinstance(record, dict) and record.get("arxiv_id"):
                    titles[str(record["arxiv_id"])] = str(record.get("title") or "")
        stems = sorted(
            path.stem
            for path in (run_dir / "evidence").glob("*.jsonl")
            if path.stem != ABSTRACT_TIER_STEM
            and any(line.strip() for line in path.read_text(encoding="utf-8").splitlines())
        )
        for stem in stems:
            log(f"  - {stem}  {titles.get(stem, '')}".rstrip())
        if not stems:
            log("  （无——尚无论文进入全文证据）")
        log("按定案行为：汇报上述列表后【立即停轮】，把 run 留在 in-progress，等待用户决策——"
            "补充信息（种子论文/关注重点）或扩大综述范围（review-mode/时间范围）。"
            "严禁薄审落盘（除非用户明示接受）、严禁更换选文策略、严禁删除或改写机械产物、严禁继续硬修。")
        return 2
    if floor and papers < floor:
        log(f"已声明豁免 cited_paper_floor（用户明示接受薄审）：{papers} 篇 < 下限 {floor} 篇，按 run.json notes 的理由继续落盘。")

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
