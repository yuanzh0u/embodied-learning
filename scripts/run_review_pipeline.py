#!/usr/bin/env python3
"""Run the fixed mechanical stages of a literature review end to end.

Moves every deterministic stage into this driver so a kickoff no longer
replans search queries, re-reads knowledge routing, or re-learns rate limits
each run:

    plan -> retrieval (S2 best-effort + arXiv, one process) -> registry
         -> screening -> coverage -> extraction -> reading packets
         -> deep read (parallel skeleton agents + local assembly, default on)
         -> evidence projection -> pipeline-summary.json

Deep read + projection run inside the driver too (parallel one-shot claude
skeleton agents); ``--skip-deep-read`` stops after the reading packets so an
external orchestrator can own deep reading instead. Either way, downstream
claude sessions only do the judgment stages: review packet, outline, writing,
audit gates.

Idempotent: a stage whose outputs already exist on disk is skipped, so an
interrupted run resumes for free. Every completed stage prints one
``[DRIVER-STAGE:<name>] ok <detail>`` line; the summary JSON reports stage
durations, counts, coverage status, S2 degradation, and the terms source.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import concurrent.futures
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT))  # repo root (embodied_learning)
from lib.agent_invoke import (  # noqa: E402
    DRIVER_AGENT_MODEL,
    build_skeleton_prompt,
    pool_root_for,
    read_skeleton_output,
    resolve_cli,
    run_one_shot_agent,
)
HUB_SCRIPTS = REPO_ROOT / "skills" / "embodied-ai-literature-hub" / "scripts"
PLANNER_SCRIPT = HUB_SCRIPTS / "search.py"
PACKET_SCRIPT = REPO_ROOT / "skills" / "embodied-ai-paper-reader" / "scripts" / "build_reading_packet.py"

REVIEW_MODES = {"rapid", "scoping", "systematic"}
SCREEN_LIMITS = {"rapid": 24, "scoping": 40, "systematic": 80}
SEARCH_STRATEGIES = {"smart", "fast", "seeds"}
S2_BUDGET_S = 90.0  # best-effort source: give up rather than retry into a 429 storm
TERMS_AGENT_TIMEOUT_S = 90.0
DYNAMIC_AGENT_TIMEOUT_S = 240.0  # 10-20 structured queries take the one-shot agent ~2-4min
FALLBACK_STOPWORDS = {
    "的", "在", "和", "与", "或", "对", "从", "到", "了", "是",
    "the", "a", "an", "of", "for", "and", "to", "in", "on", "with", "via",
}


def stage_line(name: str, detail: str = "") -> str:
    """One protocol line per completed stage; the wiki server turns each into
    a timeline event."""
    suffix = f" {detail}" if detail else ""
    return f"[DRIVER-STAGE:{name}] ok{suffix}"


def log(message: str) -> None:
    print(message, flush=True)


def run_command(command: list[str], *, timeout: float | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def fail(stage: str, message: str) -> "DriverError":
    return DriverError(f"[{stage}] {message}")


class DriverError(RuntimeError):
    pass


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    today = dt.date.today().strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="In-progress run folder under work/.")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--review-mode", choices=sorted(REVIEW_MODES), default="rapid")
    parser.add_argument("--time-range", default=f"2023-01-01..{today}")
    parser.add_argument("--focus", default="", help="Interview focus text; feeds the terms selection.")
    parser.add_argument("--kb-root", default=".", help="Knowledge base root (run dir parent conventions).")
    parser.add_argument(
        "--search-strategy",
        choices=sorted(SEARCH_STRATEGIES),
        default="smart",
        help="smart: taxonomy plan + agent dynamic queries (+ citation expansion when seeds given); "
        "fast: taxonomy plan only; seeds: citation-graph expansion only (requires seeds).",
    )
    parser.add_argument(
        "--seed-arxiv-ids",
        default="",
        help="Comma/space-separated arXiv IDs used as citation-expansion seeds (optional).",
    )
    parser.add_argument(
        "--external-candidates",
        action="append",
        default=[],
        help=(
            "harvest-curated-list JSON used AS the candidate source (repeatable). Keyword "
            "retrieval (S2 + arXiv) is skipped; the plan stage still runs for knowledge IDs "
            "and the coverage report. For curated-list runs declare workflow_version 1 + "
            "selection_method in run.json — no coverage/saturation gate applies."
        ),
    )
    parser.add_argument("--skip-s2", action="store_true", help="Skip the best-effort Semantic Scholar source.")
    parser.add_argument(
        "--arxiv-snapshot",
        help="Offline arXiv retrieval: path to a local metadata OAI snapshot (JSONL). "
        "Passed to search-arxiv --metadata-snapshot; no live arXiv API calls.",
    )
    parser.add_argument("--no-terms-agent", action="store_true", help="Use mechanical terms only (skip the one-shot claude call).")
    parser.add_argument("--no-dynamic-agent", action="store_true", help="Skip the one-shot dynamic-query agent (smart strategy).")
    parser.add_argument("--terms-timeout", type=float, default=TERMS_AGENT_TIMEOUT_S)
    parser.add_argument("--dynamic-timeout", type=float, default=DYNAMIC_AGENT_TIMEOUT_S)
    parser.add_argument("--s2-budget", type=float, default=S2_BUDGET_S)
    parser.add_argument("--workers", type=int, default=4, help="Full-text extraction workers (capped 4 downstream).")
    parser.add_argument("--force", action="store_true", help="Re-run every stage even when outputs exist.")
    parser.add_argument("--skip-deep-read", action="store_true", help="Stop after reading packets (no skeleton agents).")
    parser.add_argument("--deep-read-limit", type=int, default=10, help="Max papers to deep-read this run.")
    parser.add_argument("--agent-timeout", type=float, default=420.0, help="Per-paper skeleton agent timeout (s).")
    parser.add_argument("--agents-parallel", type=int, default=5, help="Concurrent skeleton agents.")
    return parser.parse_args(argv)


def parse_time_range(time_range: str) -> tuple[str, str]:
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})", time_range.strip())
    if not match:
        raise ValueError(f"time range must be YYYY-MM-DD..YYYY-MM-DD: {time_range!r}")
    return match.group(1), match.group(2)


def mechanical_terms(topic: str, focus: str) -> list[str]:
    """Fallback terms: split topic + focus, drop stopwords, dedupe, cap at 12.

    Title/abstract matching is substring-based against English papers, so raw
    Chinese words never match — the useful fallback terms are the Latin-word
    runs inside topic/focus (e.g. "3D Gaussian" → "3d", "gaussian"). When the
    text has no Latin tokens at all, fall through to the Chinese tokens."""
    latin: list[str] = []
    cjk: list[str] = []
    for word in re.findall(r"[0-9A-Za-z]+|[一-鿿]+", f"{topic} {focus}"):
        lowered = word.lower()
        if lowered in FALLBACK_STOPWORDS or len(lowered) < 2:
            continue
        target = latin if word.isascii() else cjk
        if lowered not in latin and lowered not in cjk:
            target.append(lowered)
    return (latin or cjk)[:12]


TERMS_PROMPT = (
    "为以下文献综述主题给出 arXiv 检索筛选关键词。只输出一行严格 JSON，"
    '形如 {{"terms": ["词1", "词2", ...]}}，不超过 12 个词。'
    "要求：每个词 1-3 个英文单词（短 token 命中率远高于长短语），"
    "必须是论文标题/摘要里高频出现的写法（如 'registration'、'coarse registration'，"
    "而不是 'correspondence-free registration' 这类长描述），不要输出任何其他文字。"
    "\n主题：{topic}\n关注重点：{focus}"
)


def extract_terms_json(text: str) -> list[str] | None:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    terms = payload.get("terms") if isinstance(payload, dict) else None
    if not isinstance(terms, list):
        return None
    cleaned = [str(item).strip() for item in terms if str(item).strip()]
    return cleaned[:12] or None


def agent_terms(topic: str, focus: str, timeout_s: float, cli: str | None) -> list[str] | None:
    """One-shot claude call for screening terms. Returns None on any failure —
    the caller falls back to mechanical terms. This is a function call with a
    timeout, not a decision-maker."""
    if not cli:
        return None
    try:
        result = run_one_shot_agent(
            TERMS_PROMPT.format(topic=topic, focus=focus or "无"), timeout_s=timeout_s, cli=cli
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode:
        return None
    return extract_terms_json(result.stdout)


DYNAMIC_QUERIES_PROMPT = (
    "为文献综述主题生成 arXiv API 检索查询。只输出一个严格 JSON 对象，形如：\n"
    '{{"queries": [{{"label": "...", "tier": "...", "query": "...", "why": "..."}}, ...]}}\n'
    "要求：\n"
    "- 10-20 条查询，覆盖：任务本身的直接术语、核心机制/方法、局限性/失效模式、评测/基准、部署工程。\n"
    "- query 使用 arXiv API 语法（all: 字段前缀、AND/OR、双引号短语），全部英文。\n"
    "- tier 取 direct / mechanism / limit / evaluation / deployment 之一，可加后缀，如 direct-anchor。\n"
    "- label 用英文小写连字符，前缀标明 tier（如 direct-online-temporal-calibration）。\n"
    "- 不要输出任何其他文字。\n"
    "\n主题：{topic}\n关注重点：{focus}{seed_line}"
)

SEED_LINE = "\n种子论文（以此为锚扩展查询词汇）：{seeds}"


def parse_seed_ids(raw: str) -> list[str]:
    """Comma/space separated arXiv IDs → normalized list (dedup, version-stripped).
    Per-token normalization delegates to the shared arXiv-ID grammar; a bare
    ``arxiv:`` prefix is stripped first since parse_arxiv_id only knows URLs."""

    from embodied_learning.knowledge.arxiv_reader import parse_arxiv_id

    ids: list[str] = []
    for token in re.split(r"[,\s]+", (raw or "").strip()):
        normalized = parse_arxiv_id(re.sub(r"^arxiv:", "", token, flags=re.IGNORECASE))
        if normalized and normalized not in ids:
            ids.append(normalized)
    return ids


def extract_dynamic_queries_json(text: str) -> dict | None:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    queries = payload.get("queries") if isinstance(payload, dict) else None
    if not isinstance(queries, list):
        return None
    cleaned: list[dict] = []
    for item in queries:
        if not isinstance(item, dict) or not str(item.get("query") or "").strip():
            continue
        cleaned.append(
            {
                "label": str(item.get("label") or "dynamic-agent"),
                "tier": str(item.get("tier") or "dynamic-association"),
                "query": str(item["query"]),
                "why": str(item.get("why") or "Agent-generated dynamic query."),
            }
        )
    if not cleaned:
        return None
    return {"queries": cleaned[:20]}


def agent_dynamic_queries(
    topic: str, focus: str, seed_ids: list[str], timeout_s: float, cli: str | None
) -> dict | None:
    """One-shot claude call generating the run's dynamic arXiv queries.

    This is the stage the failed 2026-09-11 runs were missing: their topics
    matched no taxonomy card, the mechanical latin-term fallback was empty for
    pure-Chinese topics, and retrieval ran 4 off-topic card queries. Returns
    None on any failure — the plan still contains the generic fallback."""
    if not cli:
        return None
    seed_line = SEED_LINE.format(seeds=", ".join(seed_ids)) if seed_ids else ""
    prompt = DYNAMIC_QUERIES_PROMPT.format(topic=topic, focus=focus or "无", seed_line=seed_line)
    try:
        result = run_one_shot_agent(prompt, timeout_s=timeout_s, cli=cli)
    except (subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode:
        return None
    return extract_dynamic_queries_json(result.stdout)


class TermsSelector:
    """Runs the terms selection in a thread so it overlaps retrieval; the main
    flow only blocks on it right before screening."""

    def __init__(self, topic: str, focus: str, *, use_agent: bool, timeout_s: float, cli: str | None):
        self._result: list[str] | None = None
        self._source = "mechanical"
        self._thread: threading.Thread | None = None
        if not use_agent:
            self._result = mechanical_terms(topic, focus)
            return
        def worker() -> None:
            terms = agent_terms(topic, focus, timeout_s, cli)
            if terms:
                self._result = terms
                self._source = "agent"
            else:
                self._result = mechanical_terms(topic, focus)
                self._source = "mechanical-fallback"
        self._thread = threading.Thread(target=worker, daemon=True)

    def start(self) -> None:
        if self._thread is not None:
            self._thread.start()

    def join(self) -> tuple[list[str], str]:
        if self._thread is not None:
            self._thread.join()
        assert self._result is not None
        return self._result, self._source


def outputs_exist(*paths: Path) -> bool:
    return all(path.is_file() and path.stat().st_size > 0 for path in paths)


PROJECT_SCRIPT = REPO_ROOT / "skills" / "embodied-ai-paper-reader" / "scripts" / "note_tools.py"


def build_screening_updates(screening_path: Path, extraction_summary_path: Path) -> list[dict] | None:
    """Merge extraction results into screening statuses for registry rebuild.

    The in-pipeline screening stage emits ``full-text-queued`` statuses that
    predate extraction; ``build-candidate-registry --screening-file`` needs
    ``extracted`` + ``extraction.evidence_eligible`` for the full-text floor to
    count recovered papers. Returns None when either input is missing."""
    if not screening_path.is_file() or not extraction_summary_path.is_file():
        return None
    screening = json.loads(screening_path.read_text(encoding="utf-8"))
    extraction = {
        str(result.get("paper_id")): result
        for result in json.loads(extraction_summary_path.read_text(encoding="utf-8")).get("results", [])
        if isinstance(result, dict) and result.get("paper_id")
    }
    updates = []
    for entry in screening.get("candidates", []):
        result = extraction.get(str(entry.get("arxiv_id")))
        if result and result.get("evidence_eligible"):
            entry = dict(entry)
            entry["status"] = "extracted"
            entry["extraction"] = {"evidence_eligible": True, "path": result.get("path")}
        updates.append(entry)
    return updates


def finalize_coverage(run_dir: Path, registry_command: list[str], coverage_output: Path) -> str:
    """Post-deep-read coverage reassessment (idempotent, cheap).

    The in-pipeline coverage stage runs before extraction/deep-read, so its
    full-text and accepted-paper floors are always stale-mid-run. After
    projection: rebuild the registry with extraction statuses merged in, then
    re-run assess-review-coverage with the projected evidence JSONL."""
    evidence_files = sorted((run_dir / "evidence").glob("*.jsonl"))
    if not evidence_files:
        return "skipped (no evidence projected)"
    detail = "ok"
    updates = build_screening_updates(run_dir / "screening.json", run_dir / "extraction-summary.json")
    if updates:
        updates_path = run_dir / "screening-updates.json"
        updates_path.write_text(
            json.dumps({"version": 1, "candidates": updates}, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        result = run_command(list(registry_command) + ["--screening-file", str(updates_path)])
        if result.returncode:
            detail = f"degraded: registry rebuild exit {result.returncode}"
    command = [sys.executable, str(PLANNER_SCRIPT), "assess-review-coverage",
               "--query-plan", str(run_dir / "query-plan.json"),
               "--candidate-registry", str(run_dir / "candidate-registry.json")]
    for evidence_file in evidence_files:
        command += ["--evidence-jsonl", str(evidence_file)]
    command += ["--output", str(coverage_output)]
    result = run_command(command)
    if result.returncode:
        detail = f"degraded: coverage reassessment exit {result.returncode}"
    return detail


def project_evidence(run_dir: Path, run_json_path: Path, summary_extra: dict) -> None:
    """Project evidence events from every audited paper note. Pure script
    chain: next_event_id → project_evidence_events per paper → merged JSONL."""
    notes_dir = run_dir / "paper-notes"
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(evidence_dir.glob("*.jsonl"))
    if existing:
        total = sum(1 for path in existing for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        if total:
            log(stage_line("project", f"已有 {total} 条证据事件，跳过重复投影"))
            summary_extra["evidence_events"] = total
            return
    manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
    year = dt.date.today().strftime("%Y")
    base = re.sub(r"[^0-9A-Za-z]+", "", manifest.get("topic") or "REVIEW")[:8].upper() or "REVIEW"
    id_prefix = f"EA-{base}-{year}"
    start_seq = 1
    projected = 0
    for note_path in sorted(notes_dir.glob("*.json")):
        if note_path.name.endswith(".audit.json"):
            continue
        audit_path = note_path.with_name(note_path.stem + ".audit.json")
        if not audit_path.is_file():
            continue
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if audit.get("status") not in {"pass", "needs-review"}:
            continue
        output = evidence_dir / f"{note_path.stem}.jsonl"
        result = run_command([
            sys.executable, str(PROJECT_SCRIPT), "project-evidence-events",
            "--paper-note", str(note_path),
            "--audit", str(audit_path),
            "--id-prefix", id_prefix,
            "--start-seq", str(start_seq),
            "--output", str(output),
        ])
        if result.returncode:
            log(f"[DRIVER-WARN] project {note_path.stem}: exit {result.returncode}")
            continue
        count = sum(1 for line in output.read_text(encoding="utf-8").splitlines() if line.strip())
        start_seq += count
        projected += count
        log(f"[PAPER] {note_path.stem} 投影 {count} 条证据事件")
    summary_extra["evidence_events"] = projected
    log(stage_line("project", f"{projected} 条证据事件（前缀 {id_prefix}）"))


def _audited_note(note_path: Path, audit_path: Path | None = None) -> bool:
    """A note counts as done only when its audit actually passed — reject/failed
    stubs (empty note + status: reject audit) must stay retryable."""
    audit_path = audit_path or note_path.with_name(note_path.stem + ".audit.json")
    if not note_path.is_file() or not audit_path.is_file():
        return False
    try:
        return json.loads(audit_path.read_text(encoding="utf-8")).get("status") in {"pass", "needs-review"}
    except (OSError, ValueError):
        return False


def deep_read(run_dir: Path, run_json_path: Path, screening_ids: Path, args, summary_extra: dict) -> None:
    """Per-paper skeleton agents (parallel one-shot claude) + local assembly.

    Progress is one stdout line per paper event so the wiki dialog shows
    movement instead of a silent wait."""
    cli = resolve_cli()
    if not cli:
        log("[DRIVER] claude CLI 不存在，跳过深读阶段（note 不会生成）")
        return
    pool_root = pool_root_for(args.kb_root)
    manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
    order = [
        line.strip()
        for line in screening_ids.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ][: args.deep_read_limit]

    notes_dir = run_dir / "paper-notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    todo = [
        paper_id
        for paper_id in order
        if not (
            _audited_note(notes_dir / f"{paper_id}.json")
            and _audited_note(
                pool_root / f"arxiv-{paper_id}" / "note.json",
                pool_root / f"arxiv-{paper_id}" / "note.json.audit.json",
            )
        )
    ]
    reused = len(order) - len(todo)
    if reused:
        log(f"[DRIVER] 复用池内已有深读笔记 {reused} 篇")
    log(f"[DRIVER] 深读开始：{len(todo)} 篇并行（每批 {args.agents_parallel}）")

    passed = needs_review = failed = 0
    papers = list(todo)
    for batch_start in range(0, len(papers), args.agents_parallel):
        chunk = papers[batch_start : batch_start + args.agents_parallel]
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(chunk)) as executor:
            futures = {}
            for paper_id in chunk:
                if not (pool_root / f"arxiv-{paper_id}" / "extraction.json").is_file():
                    futures[paper_id] = None
                    log(f"[PAPER] {paper_id} 未入池，跳过")
                    continue
                log(f"[PAPER] {paper_id} 深读 agent 启动")
                futures[paper_id] = executor.submit(
                    deep_read_paper, paper_id, pool_root, cli,
                    agent_timeout_s=args.agent_timeout,
                    skeleton_path=run_dir / f"skel-{paper_id}.json",
                )
            for paper_id, future in futures.items():
                try:
                    outcome = future.result() if future is not None else "failed"
                except Exception as exc:  # noqa: BLE001 - per-paper isolation
                    outcome = "failed"
                    log(f"[PAPER] {paper_id} agent 异常：{exc}")
                pooled_note = pool_root / f"arxiv-{paper_id}" / "note.json"
                pooled_audit = pool_root / f"arxiv-{paper_id}" / "note.json.audit.json"
                if pooled_note.is_file():
                    shutil.copyfile(pooled_note, notes_dir / f"{paper_id}.json")
                    if pooled_audit.is_file():
                        shutil.copyfile(pooled_audit, notes_dir / f"{paper_id}.audit.json")
                if outcome == "pass":
                    passed += 1
                    log(f"[PAPER] {paper_id} 审计通过")
                elif outcome == "needs-review":
                    needs_review += 1
                    log(f"[PAPER] {paper_id} 审计 needs-review（可用）")
                else:
                    failed += 1
                    log(f"[PAPER] {paper_id} 深读失败（{outcome}）")
    summary_extra["deep_read"] = {"total": len(order), "pass": passed, "needs_review": needs_review, "failed": failed}
    log(stage_line("deep-read", f"{passed} pass / {needs_review} needs-review / {failed} failed（共 {len(order)} 篇）"))


def run_skeleton_agent(cli: str, paper_id: str, pool_root: Path, timeout_s: float) -> dict | None:
    """One one-shot claude call returning the paper's claim skeleton."""
    try:
        result = run_one_shot_agent(
            build_skeleton_prompt(paper_id, pool_root), timeout_s=timeout_s, cli=cli
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode:
        return None
    return read_skeleton_output(result.stdout)


def deep_read_paper(
    paper_id: str,
    pool_root: Path,
    cli: str,
    *,
    agent_timeout_s: float = 420.0,
    skeleton_path: Path | None = None,
) -> str:
    """Deep-read one pooled paper: skeleton agent → build_paper_note assembly
    + audit. Returns 'pass' | 'needs-review' | 'failed'. Shared by the batch
    driver and the single-paper chat preparation (they log differently, so
    logging stays with the callers)."""

    skeleton = run_skeleton_agent(cli, paper_id, pool_root, agent_timeout_s)
    if not skeleton:
        return "failed"
    if skeleton_path is None:
        skeleton_path = Path(tempfile.gettempdir()) / f"skel-{paper_id}-{os.getpid()}.json"
    skeleton_path.write_text(json.dumps(skeleton, ensure_ascii=False), encoding="utf-8")
    result = run_command([
        sys.executable, str(REPO_ROOT / "scripts" / "build_paper_note.py"),
        "--arxiv-id", paper_id,
        "--skeleton", str(skeleton_path),
        "--pool-root", str(pool_root.parent),
    ])
    outcome = "unknown"
    try:
        outcome = str(json.loads(result.stdout).get("status") or "unknown")
    except (json.JSONDecodeError, TypeError):
        pass
    if result.returncode == 0 and outcome == "pass":
        return "pass"
    if outcome == "needs-review" or (result.returncode == 3 and outcome == "unknown"):
        return "needs-review"
    return "failed"


def pool_seed(summary_extra: dict, screening_ids: Path, run_dir: Path, args) -> None:
    """Backfill the shared pool from this run's fresh extractions/HTML so later
    topics (and the wiki reader) answer from the pool instead of re-fetching.
    Also records how many screened papers were already pool-warm."""
    pool_root = pool_root_for(args.kb_root)
    if not screening_ids.is_file():
        return
    warm = cold = 0
    add_cmd_base = [
        sys.executable, str(HUB_SCRIPTS / "knowledge.py"), "pool-add-paper", "add",
        "--pool-root", str(pool_root),
    ]
    ids = [line.strip() for line in screening_ids.read_text(encoding="utf-8").splitlines() if line.strip()]
    for paper_id in ids:
        pool_dir = pool_root / f"arxiv-{paper_id}"
        if pool_dir.is_dir() and (pool_dir / "extraction.json").is_file():
            warm += 1
            continue  # already pooled
        extraction = run_dir / "extractions" / f"{paper_id}.json"
        if not extraction.is_file():
            continue
        html_cache = Path(tempfile.gettempdir()) / "embodied-ai-literature-hub" / "html" / f"{paper_id}.html"
        command = list(add_cmd_base) + ["--extraction", str(extraction), "--force"]
        if html_cache.is_file():
            command += ["--html", str(html_cache)]
        result = run_command(command)
        if result.returncode == 0:
            cold += 1
    summary_extra["pool_warm"] = warm
    summary_extra["pool_seeded"] = cold


def run_stage(
    name: str,
    outputs: list[Path],
    force: bool,
    command_builder: "callable",
    *,
    timeout: float | None = None,
) -> str:
    """Idempotent stage runner: skip when outputs exist, else run the built
    command and verify the outputs landed."""
    if not force and outputs_exist(*outputs):
        detail = "skipped (outputs present)"
        log(stage_line(name, detail))
        return detail
    command = command_builder()
    result = run_command(command, timeout=timeout)
    if result.returncode:
        raise fail(name, f"exit {result.returncode}: {(result.stderr or result.stdout)[-400:]}")
    missing = [str(path) for path in outputs if not outputs_exist(path)]
    if missing:
        raise fail(name, f"outputs missing after run: {', '.join(missing)}")
    detail = f"ran: {Path(command[0]).name}"
    log(stage_line(name, detail))
    return detail


def write_sync(run_json_path: Path, mutate) -> None:
    manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
    mutate(manifest)
    run_json_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        start_date, end_date = parse_time_range(args.time_range)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "run.json").is_file():
        print(f"run.json not found in {run_dir}", file=sys.stderr)
        return 2
    for path in args.external_candidates:
        if not Path(path).is_file():
            print(f"external candidates file not found: {path}", file=sys.stderr)
            return 2
    run_json_path = run_dir / "run.json"

    started = time.monotonic()
    stage_seconds: dict[str, float] = {}
    summary_extra: dict[str, object] = {}
    cli = resolve_cli()

    def mark(stage: str, begun: float) -> None:
        stage_seconds[stage] = round(time.monotonic() - begun, 2)

    try:
        # ---- plan -------------------------------------------------------
        begun = time.monotonic()
        plan_outputs = [run_dir / "query-plan.json", run_dir / "query-plan.md"]
        seed_ids = parse_seed_ids(args.seed_arxiv_ids)

        # Bilingual bootstrapping: a pure-Chinese topic produces Chinese-only
        # arXiv queries that match nothing. Always inject the Latin keyword
        # tokens (mechanical split, same as the screening fallback) as dynamic
        # planner queries. The file also acts as the merge point for dynamic
        # queries from a prior claude session or the dynamic-query agent:
        # replanning (retry after a failure) must not silently drop them.
        dynamic_path = run_dir / "dynamic-queries.json"
        latin_terms = mechanical_terms(args.topic, args.focus)
        merged_queries: list[dict[str, str]] = []
        existing_dynamic: dict[str, Any] = {}
        if dynamic_path.is_file():
            try:
                existing_dynamic = json.loads(dynamic_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                existing_dynamic = {}
        merged_queries.extend(
            item
            for item in existing_dynamic.get("queries") or []
            if isinstance(item, dict) and item.get("query")
        )
        for index, term in enumerate(latin_terms, start=1):
            if term.isascii() and term not in {str(item.get("query")) for item in merged_queries}:
                merged_queries.append({"label": f"latin-{index}", "query": term, "tier": "dynamic-core"})

        # Smart strategy: one-shot agent generates the topic's own arXiv
        # queries (the stage whose absence sank the pure-Chinese topics on
        # 2026-09-11). Failure is non-fatal — the plan falls back to generic.
        dynamic_source = "merged-from-disk"
        if args.search_strategy == "smart" and not args.no_dynamic_agent and not args.external_candidates:
            agent_payload = agent_dynamic_queries(
                args.topic, args.focus, seed_ids, args.dynamic_timeout, cli
            )
            if agent_payload:
                known = {str(item.get("query")) for item in merged_queries}
                fresh = [item for item in agent_payload["queries"] if item["query"] not in known]
                merged_queries.extend(fresh)
                dynamic_source = "agent"
                log(f"[DRIVER] 动态查询 agent 生成 {len(fresh)} 条查询")
            else:
                dynamic_source = "agent-failed"
                log("[DRIVER-WARN] 动态查询 agent 失败，回退分类法+通用查询")
        elif args.search_strategy == "fast":
            dynamic_source = "disabled (fast strategy)"

        dynamic_payload = {"queries": merged_queries}
        dynamic_path.write_text(json.dumps(dynamic_payload, ensure_ascii=False), encoding="utf-8")
        summary_extra["dynamic_source"] = dynamic_source
        summary_extra["seed_ids"] = seed_ids
        summary_extra["search_strategy"] = args.search_strategy
        if args.external_candidates:
            summary_extra["external_candidates"] = args.external_candidates

        def plan_cmd_builder() -> list[str]:  # noqa: E306
            return [
                sys.executable, str(PLANNER_SCRIPT), "build-query-plan",
                "--topic", args.topic,
                "--review-mode", args.review_mode,
                "--start-date", start_date,
                "--end-date", end_date,
                "--dynamic-file", str(dynamic_path),
                "--output", str(run_dir / "query-plan.json"),
                "--markdown-output", str(run_dir / "query-plan.md"),
            ]

        run_stage("plan", plan_outputs, args.force, plan_cmd_builder)
        mark("plan", begun)
        plan = json.loads((run_dir / "query-plan.json").read_text(encoding="utf-8"))
        knowledge_ids = [str(item) for item in plan.get("knowledge_ids") or []]
        query_count = len(plan.get("queries") or [])
        if knowledge_ids:
            write_sync(run_json_path, lambda m: m.update({"knowledge_ids": knowledge_ids}))
        plan_notes = [str(note) for note in plan.get("notes") or []]
        log(f"[DRIVER] 检索计划完成：{query_count} 条查询（策略 {args.search_strategy}）"
            + (f"，知识卡 {','.join(knowledge_ids)}" if knowledge_ids else "，无知识卡匹配"))
        for note in plan_notes[:3]:
            log(f"[DRIVER] 规划提示: {note}")

        # ---- terms selection (overlaps retrieval) -----------------------
        selector = TermsSelector(
            args.topic, args.focus,
            use_agent=not args.no_terms_agent and cli is not None,
            timeout_s=args.terms_timeout,
            cli=cli,
        )
        selector.start()

        # ---- retrieval: S2 best-effort + arXiv single process -----------
        begun = time.monotonic()
        s2_output = run_dir / "search-semantic-scholar.json"
        arxiv_output = run_dir / "search-arxiv.json"
        citation_output = run_dir / "citation-expansion.json"
        s2_detail = "skipped (--skip-s2)"
        s2_process = None
        seeds_strategy = args.search_strategy == "seeds"
        external_only = bool(args.external_candidates)
        skip_arxiv = (seeds_strategy and bool(seed_ids)) or external_only
        if external_only:
            log(f"[DRIVER] 外注候选模式：跳过关键词检索，registry 只收 --external-candidates "
                f"({len(args.external_candidates)} 个文件)")
        if not skip_arxiv:
            if not args.skip_s2:
                s2_cmd = lambda: [  # noqa: E731
                    sys.executable, str(HUB_SCRIPTS / "search.py"), "search-semantic-scholar",
                    "--query-file", str(run_dir / "query-plan.json"),
                    "--start-date", start_date,
                    "--end-date", end_date,
                    "--sleep-seconds", "1.0",
                    "--retries", "1",
                    "--retry-max-seconds", "20",
                    "--timeout", "20.0",
                    "--output", str(s2_output),
                ]
                try:
                    s2_process = subprocess.Popen(
                        s2_cmd(), cwd=str(REPO_ROOT), text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    )
                    try:
                        s2_process.communicate(timeout=args.s2_budget)
                    except subprocess.TimeoutExpired:
                        s2_process.kill()
                        s2_process.communicate()
                        s2_detail = f"degraded: exceeded {args.s2_budget:.0f}s budget"
                    if s2_process.returncode:
                        s2_detail = f"degraded: exit {s2_process.returncode} (rate limited or unreachable)"
                    elif s2_output.is_file():
                        s2_detail = "ok"
                except OSError as exc:
                    s2_detail = f"degraded: {exc}"
                summary_extra["s2_detail"] = s2_detail
        if not skip_arxiv:
            arxiv_cmd = lambda: [  # noqa: E731
                sys.executable, str(HUB_SCRIPTS / "search.py"), "search-arxiv",
                "--query-file", str(run_dir / "query-plan.json"),
                "--start-date", start_date,
                "--end-date", end_date,
                "--batch-label", "r1",
                *([] if not args.arxiv_snapshot else ["--metadata-snapshot", args.arxiv_snapshot]),
                "--output", str(arxiv_output),
            ]
            # arXiv 429s return exit 0 with zero results; a screening over an empty
            # registry would fail confusingly later. Retry once after a cooldown
            # when a fresh first pass comes back empty (a skipped stage with
            # pre-existing outputs is trusted as-is).
            arxiv_detail = run_stage("retrieval-arxiv", [arxiv_output], args.force, arxiv_cmd)
            if arxiv_detail.startswith("ran") and arxiv_output.is_file():
                try:
                    hits = sum(
                        len(item.get("results") or item.get("papers") or [])
                        for item in json.loads(arxiv_output.read_text(encoding="utf-8")).get("queries", [])
                    )
                except (json.JSONDecodeError, OSError):
                    hits = 0
                if hits == 0:
                    log("[DRIVER-WARN] arXiv returned 0 results (rate limited?) — cooling down 120s and retrying once")
                    time.sleep(120)
                    arxiv_output.unlink(missing_ok=True)
                    arxiv_detail = run_stage("retrieval-arxiv", [arxiv_output], True, arxiv_cmd)
            if arxiv_output.is_file():
                try:
                    arxiv_papers = json.loads(arxiv_output.read_text(encoding="utf-8")).get("paper_count") or 0
                    log(f"[DRIVER] arXiv 关键词检索命中 {arxiv_papers} 篇")
                except (json.JSONDecodeError, OSError):
                    pass
        else:
            arxiv_detail = (
                "skipped (external candidates replace keyword retrieval)"
                if external_only
                else "skipped (seeds strategy: citation-graph expansion replaces keyword retrieval)"
            )
            log(stage_line("retrieval-arxiv", arxiv_detail))
        summary_extra["s2_detail"] = s2_detail
        mark("retrieval", begun)

        # ---- citation expansion (seed-driven, smart w/ seeds or seeds) ---
        begun = time.monotonic()
        citation_detail = "skipped (no seeds)"
        if seed_ids and (args.search_strategy in ("seeds", "smart")):
            citation_cmd = lambda: [  # noqa: E731
                sys.executable, str(HUB_SCRIPTS / "search.py"), "expand-via-citations",
                *[item for seed in seed_ids for item in ("--seed-id", seed)],
                "--direction", "both",
                "--batch-label", "citation-seeds",
                "--max-total-candidates", "200",
                "--start-date", start_date,
                "--end-date", end_date,
                "--sleep-seconds", "1.0",
                "--graph-output", str(run_dir / "citation-graph.json"),
                "--output", str(citation_output),
            ]
            try:
                citation_result = run_command(citation_cmd(), timeout=300.0)
            except subprocess.TimeoutExpired:
                citation_result = subprocess.CompletedProcess(
                    citation_cmd(), returncode=1, stdout="", stderr="timeout after 300s"
                )
            if citation_result.returncode:
                # best-effort: keyword retrieval candidates still proceed
                citation_detail = f"degraded: exit {citation_result.returncode} {(citation_result.stderr or '')[-200:]}"
                log(stage_line("citation-expansion", citation_detail))
            else:
                citation_detail = (citation_result.stderr or "").strip().splitlines()[-1] if (citation_result.stderr or "").strip() else "ok"
                log(stage_line("citation-expansion", citation_detail))
        summary_extra["citation_expansion"] = citation_detail
        mark("citation", begun)

        # ---- registry ---------------------------------------------------
        begun = time.monotonic()
        registry_output = run_dir / "candidate-registry.json"
        def registry_cmd():
            command = [
                sys.executable, str(HUB_SCRIPTS / "search.py"), "build-candidate-registry",
                "--output", str(registry_output),
            ]
            if not skip_arxiv and arxiv_output.is_file():
                command += ["--search-result", str(arxiv_output)]
            if not args.skip_s2 and s2_output.is_file() and s2_process is not None and s2_process.returncode == 0:
                command += ["--semantic-scholar-result", str(s2_output)]
            if citation_output.is_file():
                command += ["--citation-result", str(citation_output)]
            for path in args.external_candidates:
                command += ["--curated-list-result", str(path)]
            return command
        run_stage("registry", [registry_output], args.force, registry_cmd)
        mark("registry", begun)

        # ---- screening + coverage (joins the terms thread) --------------
        begun = time.monotonic()
        terms, terms_source = selector.join()
        # Chinese-only screening terms match nothing against English titles —
        # the second half of the 2026-09-11 failure chain. When the fallback
        # terms carry no Latin token, mine English terms from the run's own
        # dynamic queries (the same vocabulary that just retrieved candidates).
        if not any(term.isascii() for term in terms) and dynamic_payload["queries"]:
            mined: list[str] = []
            for item in dynamic_payload["queries"]:
                for token in re.findall(r'"([a-z0-9 \-]+)"', str(item.get("query", "")).lower()):
                    token = token.strip()
                    if 2 <= len(token) <= 40 and token not in mined:
                        mined.append(token)
                if len(mined) >= 12:
                    break
            if mined:
                terms = mined
                terms_source = "dynamic-queries"
        summary_extra["terms"] = terms
        summary_extra["terms_source"] = terms_source
        screen_limit = SCREEN_LIMITS[args.review_mode]
        screening_output = run_dir / "screening.json"
        screening_ids = run_dir / "screening-ids.txt"
        screening_cmd = lambda: [  # noqa: E731
            sys.executable, str(HUB_SCRIPTS / "search.py"), "screen-candidates",
            "--candidate-registry", str(registry_output),
            "--terms", ",".join(terms),
            "--limit", str(screen_limit),
            "--output-screening", str(screening_output),
            "--output-ids", str(screening_ids),
            "--output-markdown", str(run_dir / "screening.md"),
        ]
        run_stage("screening", [screening_output, screening_ids], args.force, screening_cmd)
        screened_ids = [
            line.strip()
            for line in screening_ids.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        summary_extra["screened_count"] = len(screened_ids)
        log(f"[DRIVER] 精读候选 {len(screened_ids)} 篇（screening.md 已写入运行目录）")
        coverage_output = run_dir / "coverage-report.json"
        coverage_cmd = lambda: [  # noqa: E731
            sys.executable, str(HUB_SCRIPTS / "search.py"), "assess-review-coverage",
            "--query-plan", str(run_dir / "query-plan.json"),
            "--candidate-registry", str(registry_output),
            "--output", str(coverage_output),
        ]
        run_stage("coverage", [coverage_output], args.force, coverage_cmd)
        mark("screening", begun)
        coverage = json.loads(coverage_output.read_text(encoding="utf-8"))

        # ---- full-text extraction --------------------------------------
        begun = time.monotonic()
        extraction_summary = run_dir / "extraction-summary.json"
        extraction_cmd = lambda: [  # noqa: E731
            sys.executable, str(HUB_SCRIPTS / "fetch.py"), "extract-content-queue",
            "--paper-id-file", str(screening_ids),
            "--terms", ",".join(terms),
            "--output-dir", str(run_dir / "extractions"),
            "--workers", str(max(1, min(args.workers, 4))),
            "--ocr-mode", "never",
            "--include-full-text",
            "--summary-output", str(extraction_summary),
        ]
        run_stage("extraction", [extraction_summary], args.force, extraction_cmd, timeout=1800.0)
        mark("extraction", begun)
        pool_seed(summary_extra, screening_ids, run_dir, args)

        # ---- reading packets --------------------------------------------
        begun = time.monotonic()
        packets_dir = run_dir / "reading-packets"
        packets_dir.mkdir(parents=True, exist_ok=True)
        packet_count = 0
        extraction_files = sorted((run_dir / "extractions").glob("*.json"))
        for extraction_path in extraction_files:
            paper_id = extraction_path.stem
            packet_output = packets_dir / f"{paper_id}.md"
            if not args.force and packet_output.is_file() and packet_output.stat().st_size > 0:
                packet_count += 1
                continue
            result = run_command([
                sys.executable, str(PACKET_SCRIPT),
                "--extraction", str(extraction_path),
                "--review-question", args.topic,
                "--topic-id", *(knowledge_ids or ["EA-DATA"]),
                "--review-mode", args.review_mode,
                "--output", str(packet_output),
            ])
            if result.returncode:
                # One unrecoverable paper must not sink the queue.
                log(f"[DRIVER-WARN] packet {paper_id}: exit {result.returncode}")
                continue
            packet_count += 1
        mark("packets", begun)
        log(stage_line("packets", f"{packet_count}/{len(extraction_files)} packets"))

        # ---- deep read (skeleton agents + local assembly) ---------------
        if not args.skip_deep_read:
            begun = time.monotonic()
            deep_read(run_dir, run_json_path, screening_ids, args, summary_extra)
            mark("deep-read", begun)
            begun = time.monotonic()
            project_evidence(run_dir, run_json_path, summary_extra)
            mark("project", begun)
            # ---- coverage finalize: statuses + evidence-aware reassessment
            begun = time.monotonic()
            summary_extra["coverage_final"] = finalize_coverage(run_dir, registry_cmd(), coverage_output)
            mark("coverage-final", begun)
            log(stage_line("coverage-final", summary_extra["coverage_final"]))

        # ---- summary ----------------------------------------------------
        registry = json.loads(registry_output.read_text(encoding="utf-8"))
        observed = coverage.get("observed") or {}
        checks = ((coverage.get("stop_assessment") or {}).get("checks") or {})
        # At driver time only discovery-side floors can pass (full text and
        # accepted papers come later, from deep reading) — report those two
        # honestly instead of expecting ready_to_stop.
        summary = {
            "version": 1,
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "topic": args.topic,
            "review_mode": args.review_mode,
            "time_range": args.time_range,
            "knowledge_ids": knowledge_ids,
            "query_count": query_count,
            "stage_seconds": stage_seconds,
            "candidate_count": int(registry.get("candidate_count") or 0),
            "screening_limit": screen_limit,
            "screened_count": len(screened_ids),
            "full_text_recovered_count": int(observed.get("full_text_recovered_count") or 0),
            "coverage_dimensions_passed": bool(coverage.get("coverage_dimensions")),
            "candidate_floor_passed": bool(checks.get("candidate_floor")),
            "saturation_passed": bool(checks.get("saturation")),
            "packet_count": packet_count,
            # Artifacts a reviewer reads first: the plan, the candidate list,
            # and the screened (deep-read) list.
            "artifacts": {
                "search_plan": "query-plan.md",
                "candidate_registry": "candidate-registry.json",
                "screened_list": "screening.md",
                "citation_graph": "citation-graph.json" if citation_output.is_file() else None,
            },
            **summary_extra,
        }
        (run_dir / "pipeline-summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        log(stage_line("summary", f"total {time.monotonic() - started:.0f}s"))
        log(
            f"[DRIVER] 检索计划 query-plan.md · 候选 {summary['candidate_count']} 篇 · "
            f"精读候选 {len(screened_ids)} 篇 · 详情见运行目录 pipeline-summary.json"
        )
        return 0
    except DriverError as exc:
        print(f"pipeline failed: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"pipeline failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())