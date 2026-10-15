"""One-shot status digest for an in-progress literature-review run.

Replaces the per-file inline-python loops writer agents used to improvise
(looping evidence/*.jsonl, catting pipeline-summary.json, probing artifacts,
--help exploration): everything homogenous about "读取运行现状" is aggregated
here in a single call — run identity, retrieval→evidence funnel, a per-paper
evidence table (with title/first-author/year for the References section,
joined from the candidate registry), artifact checklist, manifest gaps
run.py finalize would fill, and the exact next commands.

Output is plain text for agent consumption; --json emits the same payload
machine-readably.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from embodied_learning.utils.layout import default_kb_root, find_roots, infer_kb_root
from embodied_learning.config import CITED_PAPER_FLOORS

STYLE_FILES = {
    "scientific-memo": "scientific-memo_keyan.md",
    "expert-explainer": "zhihu-explainer_zhihu.md",
    "kol-thread": "xiaohongshu-post_xiaohongshu.md",
}
ARTIFACTS = [
    "review-packet.md", "writing-brief.md", "evidence-appendix.md",
    "trace-map.json", "evidence.jsonl",
]


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def evidence_digest(run_dir: Path) -> tuple[list[dict], int, int]:
    """Per-paper aggregation over evidence/*.jsonl (the loop the agents wrote
    by hand, ~10 bash calls per run)."""
    papers: dict[str, dict] = {}
    total_events = 0
    for path in sorted((run_dir / "evidence").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            total_events += 1
            paper = event.get("paper") or {}
            arxiv_id = str(paper.get("arxiv_id") or path.stem)
            entry = papers.setdefault(arxiv_id, {
                "arxiv_id": arxiv_id, "title": paper.get("title") or "",
                "published": paper.get("published") or "",
                "events": 0, "stances": Counter(), "claims": [], "figures": 0,
            })
            entry["events"] += 1
            entry["stances"][str(event.get("stance") or "?")] += 1
            if len(entry["claims"]) < 3:
                entry["claims"].append(str(event.get("claim") or ""))
            if event.get("figures"):
                entry["figures"] += len(event["figures"])
    return list(papers.values()), len(papers), total_events


def registry_metadata(run_dir: Path) -> dict[str, dict]:
    """arxiv_id -> {title, authors, published} from the candidate registry."""
    registry = load_json(run_dir / "candidate-registry.json")
    records = registry if isinstance(registry, list) else registry.get("candidates") or []
    return {
        str(record.get("arxiv_id")): record
        for record in records
        if isinstance(record, dict) and record.get("arxiv_id")
    }


def year_of(published: str) -> str:
    return published[:4] if len(published) >= 4 else ""


def audit_statuses(run_dir: Path) -> dict[str, str]:
    """paper_id -> claim-support audit status (pass / needs-review / reject)."""
    out: dict[str, str] = {}
    notes_dir = run_dir / "paper-notes"
    if not notes_dir.is_dir():
        return out
    for path in notes_dir.glob("*.audit.json"):
        data = load_json(path)
        out[path.name[: -len(".audit.json")]] = str(data.get("status") or "?")
    return out


def evidence_paper_ids(run_dir: Path) -> set[str]:
    """Papers with at least one projected evidence event."""
    return {
        path.stem
        for path in (run_dir / "evidence").glob("*.jsonl")
        if any(line.strip() for line in path.read_text(encoding="utf-8").splitlines())
    }


def failure_reason(run_dir: Path, paper_id: str) -> str:
    """Why a paper stopped: audit payload problems first (richer), then the
    driver's persisted failed.json (skeleton/agent failures)."""
    audit_path = run_dir / "paper-notes" / f"{paper_id}.audit.json"
    if audit_path.is_file():
        data = load_json(audit_path)
        problems = data.get("errors") or data.get("problems") or []
        if problems:
            return str(problems[0])[:80]
    failed_path = run_dir / "paper-notes" / f"{paper_id}.failed.json"
    if failed_path.is_file():
        data = load_json(failed_path)
        return str(data.get("reason") or data.get("outcome") or "")[:80]
    return ""


def paper_funnel(run_dir: Path) -> list[dict]:
    """Per screened paper: where it stopped in extraction → pool → deep-read
    → audit → evidence. The writer used to reconstruct this with a dozen
    inline-python loops over screening/registry/audit files."""
    ids_path = run_dir / "screening-ids.txt"
    if not ids_path.is_file():
        return []
    ids = [line.strip() for line in ids_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    extraction = load_json(run_dir / "extraction-summary.json")
    eligible = {
        str(result.get("paper_id")): bool(result.get("evidence_eligible"))
        for result in extraction.get("results") or []
    }
    audits = audit_statuses(run_dir)
    evidence_ids = evidence_paper_ids(run_dir)
    metadata = registry_metadata(run_dir)
    screening = load_json(run_dir / "screening.json")
    screened = {
        str(item.get("arxiv_id")): item
        for item in (screening.get("candidates") or [])
        if isinstance(item, dict)
    }
    pool_root = run_dir.parent.parent / "pool"
    rows: list[dict] = []
    for paper_id in ids:
        audit = audits.get(paper_id)
        if paper_id in evidence_ids:
            stage = "evidence"
        elif audit == "reject":
            stage = "audit-reject"
        elif (run_dir / "paper-notes" / f"{paper_id}.json").is_file():
            # Note assembled but not projected into evidence. When an audit
            # exists the deep-read itself is done — calling this
            # deep-read-failed misdirected every shortfall review (2026-10-15
            # 纹理映射: 5 complete notes were reported as deep-read failures
            # when projection had rejected them). Only a note without a usable
            # audit is a deep-read failure.
            stage = "projection-blocked" if audit in {"pass", "needs-review"} else "deep-read-failed"
        elif pool_root.is_dir() and (pool_root / f"arxiv-{paper_id}" / "extraction.json").is_file():
            stage = "pooled-unread"
        elif eligible.get(paper_id) is False:
            stage = "held"
        elif paper_id in eligible:
            stage = "extracted-unpooled"
        else:
            stage = "unknown"
        item = screened.get(paper_id) or {}
        record = metadata.get(paper_id) or {}
        rows.append({
            "arxiv_id": paper_id,
            "stage": stage,
            "audit": audit,
            "reason": failure_reason(run_dir, paper_id),
            "selection_reason": " ".join(str(item.get("selection_reason") or "").split()),
            "title": str(record.get("title") or ""),
            "matched_title_terms": (item.get("matched_title_terms") or [])[:3],
        })
    return rows


def packet_command(run_dir: Path, report: dict, skills_root: Path) -> str:
    """The exact, fully-specified packet invocation — the writer used to read
    the packet script's argparse source to discover these flags."""
    script = skills_root / "embodied-ai-review-writer" / "scripts" / "write.py"
    parts = ["python3", str(script), "review-packet", "--run-dir", str(run_dir)]
    if report.get("topic"):
        parts += ["--topic", str(report["topic"])]
    for knowledge_id in report.get("knowledge_ids") or []:
        parts += ["--knowledge-id", str(knowledge_id)]
    if report.get("review_mode"):
        parts += ["--review-mode", str(report["review_mode"])]
    consolidated = run_dir / "evidence.jsonl"
    if consolidated.is_file():
        parts += ["--evidence-jsonl", str(consolidated)]
    else:
        for path in sorted((run_dir / "evidence").glob("*.jsonl")):
            if any(line.strip() for line in path.read_text(encoding="utf-8").splitlines()):
                parts += ["--evidence-jsonl", str(path)]
    for flag, filename in (("--coverage-report", "coverage-report.json"),
                           ("--reading-summary", "reading-summary.json")):
        if (run_dir / filename).is_file():
            parts += [flag, str(run_dir / filename)]
    parts.append("--consolidate-evidence")
    return " ".join(parts)


def gates_block(run_dir: Path, manifest: dict) -> dict:
    """Coverage/saturation gate state + declared exceptions: the writer used
    to rediscover all of this by reading gate source."""
    coverage = load_json(run_dir / "coverage-report.json")
    stop = coverage.get("stop_assessment") or {}
    return {
        "checks": stop.get("checks") or {},
        "unresolved": stop.get("unresolved") or [],
        "saturation_rounds": [
            {
                "batch": str(item.get("batch") or ""),
                "channel": str(item.get("channel") or ""),
                "new_unique_rate": item.get("new_unique_rate"),
            }
            for item in coverage.get("saturation_rounds") or []
        ],
        "gate_exceptions": list(manifest.get("gate_exceptions") or []),
    }


def build_report(run_dir: Path) -> dict:
    manifest = load_json(run_dir / "run.json")
    summary = load_json(run_dir / "pipeline-summary.json")
    papers, paper_count, event_count = evidence_digest(run_dir)
    metadata = registry_metadata(run_dir)
    for entry in papers:
        record = metadata.get(entry["arxiv_id"]) or {}
        entry["title"] = entry["title"] or record.get("title") or ""
        entry["authors"] = record.get("authors") or []
        entry["published"] = entry["published"] or record.get("published") or ""
    papers.sort(key=lambda entry: (-entry["events"], entry["arxiv_id"]))

    deep_read = summary.get("deep_read") or {}
    # pipeline-summary.json is written at the driver's tail — mid-run it is
    # absent and the funnel used to read "候选 None → 筛选 None" while the
    # registry and screening list were already on disk. Fall back to those
    # artifacts so an agent reading status mid-run sees the real funnel.
    candidates = summary.get("candidate_count")
    if candidates is None:
        registry = load_json(run_dir / "candidate-registry.json")
        records = (registry.get("candidates") if isinstance(registry, dict) else None) or []
        candidates = len(records) if records else None
    screened = summary.get("screened_count")
    if screened is None:
        ids_file = run_dir / "screening-ids.txt"
        if ids_file.is_file():
            screened = len([ln for ln in ids_file.read_text(encoding="utf-8").splitlines() if ln.strip()])
    deliverables = {name: (run_dir / filename).is_file() for name, filename in STYLE_FILES.items()}
    present = {name: (run_dir / name).is_file() for name in ARTIFACTS}
    mode = str(manifest.get("review_mode") or summary.get("review_mode") or "")
    floor = CITED_PAPER_FLOORS.get(mode)
    return {
        "run": run_dir.name,
        "status": manifest.get("status") or "unknown",
        "topic": manifest.get("topic"),
        "knowledge_ids": manifest.get("knowledge_ids"),
        "review_mode": mode,
        # What the caller/user actually asked for, stamped by init_run. Kept
        # separate from `review_mode` (the effective contract) so a drift
        # between the two is visible without opening logs.
        "inputs": manifest.get("inputs") or {},
        "style": manifest.get("style"),
        "scope_note": manifest.get("scope_note"),
        "funnel": {
            "candidates": candidates,
            "screened": screened,
            "deep_read": deep_read,
            "paper_count": paper_count,
            "event_count": event_count,
            "cited_floor": floor,
            "floor_met": (paper_count >= floor) if floor else None,
        },
        "papers": papers,
        "paper_funnel": paper_funnel(run_dir),
        "gates": gates_block(run_dir, manifest),
        "artifacts": {**present, **deliverables},
        "paper_notes": len(list((run_dir / "paper-notes").glob("*.json"))) if (run_dir / "paper-notes").is_dir() else 0,
    }


def render(report: dict, run_dir: Path, scripts_root: Path, skills_root: Path) -> str:
    lines: list[str] = []
    funnel = report["funnel"]
    deep_read = funnel["deep_read"] or {}
    lines.append(
        f"[run] {report['run']}  status={report['status']}  mode={report['review_mode'] or '—'}"
        + (f"  style={report['style']}（scope_note 已声明）" if report.get("style") else "")
    )
    inputs = report.get("inputs") or {}
    requested = inputs.get("requested_review_mode") or inputs.get("review_mode")
    if requested and requested != report["review_mode"]:
        lines.append(
            f"[inputs] 请求模式 {requested} ≠ 生效模式 {report['review_mode']} —— "
            "以 run.json inputs 为准核对（这正是该被记录下来的漂移）"
        )
    if inputs:
        lines.append(f"[inputs] {json.dumps(inputs, ensure_ascii=False)}")
    read_bits = " / ".join(
        f"{key} {deep_read[key]}"
        for key in ("pass", "needs_review", "failed")
        if key in deep_read
    )
    lines.append(
        f"[funnel] 候选 {funnel['candidates']} → 筛选 {funnel['screened']} → "
        f"深读 {deep_read.get('total', '—')}（{read_bits or '未运行'}）→ "
        f"证据 {funnel['paper_count']} 篇 / {funnel['event_count']} 事件"
    )
    if funnel["cited_floor"] is not None:
        verdict = "达标" if funnel["floor_met"] else (
            f"不足（下限 {funnel['cited_floor']} 篇：续跑驱动补深读后重跑 finalize）"
            if funnel["floor_met"] is False else ""
        )
        lines.append(f"[floor] 模式 {report['review_mode']} 引用篇数下限 {funnel['cited_floor']}：{verdict}")
    gates = report.get("gates") or {}
    checks = gates.get("checks") or {}
    if checks:
        verdicts = " ".join(f"{name}={'过' if ok else '未过'}" for name, ok in checks.items())
        lines.append(f"[gates] 覆盖/饱和：{verdicts}")
        if gates.get("unresolved"):
            lines.append(
                "  未过：" + ", ".join(str(item) for item in gates["unresolved"])
                + " —— 修法二选一：续跑 run.py pipeline 补检索/深读；或 run.json 声明 "
                '"gate_exceptions": [...] 并在 notes 写明正当理由（勿手改 event_count）'
            )
        for rnd in gates.get("saturation_rounds") or []:
            rate = rnd.get("new_unique_rate")
            lines.append(f"  饱和轮 {rnd.get('batch')}（{rnd.get('channel')}）新篇目率 {rate}")
        if gates.get("gate_exceptions"):
            lines.append("  已声明豁免：" + ", ".join(str(item) for item in gates["gate_exceptions"]))
    lines.append(f"[papers] 逐篇证据（References 元数据已从 candidate-registry join）：")
    for entry in report["papers"]:
        authors = entry["authors"]
        first = authors[0] if authors else ""
        etal = f"{first} et al." if len(authors) > 1 else (first or "作者缺失")
        stances = " ".join(f"{stance}×{count}" for stance, count in entry["stances"].most_common())
        lines.append(
            f"  {entry['arxiv_id']}  {entry['title']}  {etal}  {year_of(entry['published'])}  "
            f"{entry['events']}事件 {stances}"
            + (f" 图{entry['figures']}" if entry["figures"] else "")
        )
        for claim in entry["claims"]:
            lines.append(f"    · {claim}")
    missing = [name for name, exists in report["artifacts"].items() if not exists]
    have = [name for name, exists in report["artifacts"].items() if exists]
    lines.append(f"[artifacts] 有：{', '.join(have) or '无'}；缺：{', '.join(missing) or '无'}")
    funnel_rows = report.get("paper_funnel") or []
    if funnel_rows:
        stuck = [row for row in funnel_rows if row["stage"] not in ("evidence",)]
        lines.append(
            f"[deep-read] 队列 {len(funnel_rows)} 篇：evidence "
            f"{len(funnel_rows) - len(stuck)}，其余 {len(stuck)} 篇停在下述阶段"
            "（projection-blocked 为审计未过卡导致证据未投影；deep-read-failed / "
            "audit-reject 可续跑驱动重试；held 为全文未恢复）："
        )
        for row in stuck:
            title = row["title"][:36]
            terms = ",".join(row["matched_title_terms"])
            lines.append(
                f"  {row['arxiv_id']}  {row['stage']}"
                + (f"  命中:{terms}" if terms else "")
                + (f"  选中:{row['selection_reason']}" if row.get("selection_reason") else "")
                + (f"  因:{row['reason']}" if row.get("reason") else "")
                + (f"  {title}" if title else "")
            )
    if not report["artifacts"].get("review-packet.md"):
        lines.append("[next] 生成综述包（直接写进运行目录，逐字执行即可）：")
        lines.append(f"  {packet_command(run_dir, report, skills_root)}")
    # Gate commands verbatim: the writer used to guess check/audit flags wrong
    # (positional vs --run-dir) and burn calls re-discovering the CLI.
    style_flags = {
        "scientific-memo_keyan.md": "memo",
        "zhihu-explainer_zhihu.md": "zhihu",
        "xiaohongshu-post_xiaohongshu.md": "xiaohongshu",
    }
    gate_articles = [name for name in style_flags if (run_dir / name).is_file()]
    if gate_articles:
        lines.append("[next] 审计门（逐字执行，参数勿猜）：")
        lines.append(f"  python3 {scripts_root / 'run.py'} check-bundle {run_dir}")
        art = " ".join(f"--article {run_dir / name}" for name in gate_articles)
        lines.append(
            f"  python3 {scripts_root / 'run.py'} audit-citations {art} "
            f"--appendix {run_dir / 'evidence-appendix.md'} "
            f"--evidence-jsonl {run_dir / 'evidence.jsonl'} --run-json {run_dir / 'run.json'}"
        )
        style_args = " ".join(f"--{style_flags[name]} {run_dir / name}" for name in gate_articles)
        lines.append(
            f"  python3 {skills_root / 'embodied-ai-review-writer' / 'scripts' / 'write.py'} "
            f"audit-article-quality {style_args} --evidence-jsonl {run_dir / 'evidence.jsonl'}"
        )
    kb_root = infer_kb_root(run_dir) or default_kb_root()
    lines.append(
        f"[next] 成稿+审计门全过后一次落盘：python3 {scripts_root / 'run.py'} finalize "
        f"--run-dir {run_dir} --kb-root {kb_root}"
    )
    lines.append(
        f"[next] 地板/饱和要豁免时用机械入口（勿手改 run.json）：python3 {scripts_root / 'run.py'} finalize "
        f"--run-dir {run_dir} --kb-root {kb_root} "
        f"--declare-gate-exception <cited_paper_floor|saturation> --reason \"...\""
    )
    return "\n".join(lines)



def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/run.py."""
    run_dir = Path(args.run_dir).expanduser().resolve()
    if not (run_dir / "run.json").is_file():
        print(f"run.json 不存在：{run_dir}", file=sys.stderr)
        return 1
    report = build_report(run_dir)
    if args.json:
        report["papers"] = [
            {**entry, "stances": dict(entry["stances"])} for entry in report["papers"]
        ]
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        # find_roots() is the only legal root resolver (layout.py): [2] is the
        # scripts root (repo checkout: <repo>/scripts, wheel: site-packages),
        # [1] is the skills tree. Path(__file__).parent here is the wiki/run
        # package dir and produced [next] commands pointing at
        # embodied_learning/wiki/run/run.py — which does not exist; and
        # scripts_root/"skills"/... collapsed the two roots into one bogus path.
        _repo, skills_root, scripts_root = find_roots()
        print(render(report, run_dir, scripts_root, skills_root))
    return 0
