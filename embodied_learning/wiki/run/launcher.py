"""Headless literature-review launcher: one command, run to published.

Chains the mechanical driver (run.py pipeline) with the judgment
stages as a detached one-shot claude agent (the wiki workflow prompt), then
settles/publishes via run.py finalize, then verifies catalog + wiki snapshot.
Designed to survive the launching session ending: stages are marked on disk,
idempotent, and re-enterable via --resume.

Usage:
  # launch detached (default); returns immediately with a log path
  python3 scripts/run.py launch \
    --topic "ego-exo 数据集：采集与标注" --review-mode systematic \
    --time-range 2016-09-17..2026-09-17 \
    --focus "以 Ego-Exo4D (2311.18259) 为核心，综述采集与标注" \
    --seed-arxiv-ids 2311.18259 \
    [--arxiv-snapshot ~/Documents/arxiv/arxiv-metadata-oai-snapshot.sqlite]

  # watch progress / re-enter after an interruption / stop
  python3 scripts/run.py launch --status --run-dir work/<run>
  python3 scripts/run.py launch --resume --run-dir work/<run>
  python3 scripts/run.py launch --stop   --run-dir work/<run>

Failure model: every stage is idempotent (outputs present → skipped), the
mechanical driver retries with backoff, and gate failures feed the audit
problems back to one continuation agent round. Nested-claude environment
variables are stripped before spawning claude (same guard as wiki_chat).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

from embodied_learning.config import STYLE_TO_FILE, STANDARD_ARTICLES
from embodied_learning.knowledge.evidence import consolidate_evidence
from embodied_learning.utils.layout import default_kb_root, find_roots
from embodied_learning.wiki.run.catalog import build_trace_map
from embodied_learning.wiki.run.manifest import declared_style
# AI-model capability goes through the harness binding (pybind-style); prompts and KB layout stay with the feature module.
from embodied_learning.harness.claude import (
    DRIVER_AGENT_MODEL,
    claude_auth_ready,
    complete,
    isolated_claude_env,
    resolve_cli,
    system_one_ready,
)
from embodied_learning.harness.prompt import USER_DECISION_STOP

_REPO_ROOT, SKILLS_ROOT, SCRIPTS_ROOT = find_roots()
STYLE_VALUES = tuple(STYLE_TO_FILE)
LAUNCH_DIRNAME = ".launch"
CATALOG_PATH = Path("knowledge/literature-review-catalog.md")


def load_wiki_prompts():
    """Load build_workflow_prompt / build_continuation_prompt from the chat
    module without standing up the chat server."""
    from embodied_learning.wiki.publish import chat as wiki_chat_lib

    return wiki_chat_lib


def stage_done(run_dir: Path, stage: str) -> bool:
    return (run_dir / LAUNCH_DIRNAME / f"{stage}.done").is_file()


def mark_stage(run_dir: Path, stage: str, detail: str = "") -> None:
    marker = run_dir / LAUNCH_DIRNAME / f"{stage}.done"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {detail}\n", encoding="utf-8")


def log(message: str) -> None:
    print(f"[LAUNCH] {message}", flush=True)


def pipeline_root() -> Path:
    """Root that wiki_chat.resolve_pipeline_layout understands: the repo root
    on a checkout, the installed wiki_scripts dir (which contains skills/) on
    a wheel install."""
    return _REPO_ROOT if _REPO_ROOT is not None else SCRIPTS_ROOT


def resolve_kb_root(args: argparse.Namespace) -> Path:
    return Path(args.kb_root).expanduser().resolve() if args.kb_root else default_kb_root()


def run_mechanical(args: argparse.Namespace, run_dir: Path) -> None:
    """Run the mechanical driver with bounded retries; idempotent stages make
    each retry a resume."""
    kb_root = resolve_kb_root(args)
    command = [
        sys.executable, str(SCRIPTS_ROOT / "run.py"), "pipeline",
        "--run-dir", str(run_dir),
        "--topic", args.topic,
        "--review-mode", args.review_mode,
        "--focus", args.focus or "",
        "--search-strategy", args.search_strategy,
        "--selection-strategy", args.selection_strategy,
        "--deep-read-limit", str(args.deep_read_limit),
    ]
    if getattr(args, "selection_model", None) and args.selection_strategy == "smart":
        command += ["--selection-model", args.selection_model]
    if args.selection_strategy == "smart-jev":
        command += ["--selection-threshold", str(args.selection_threshold)]
    if args.time_range:
        command += ["--time-range", args.time_range]
    if args.seed_arxiv_ids:
        command += ["--seed-arxiv-ids", args.seed_arxiv_ids]
    for path in args.external_candidates:
        command += ["--external-candidates", str(Path(path).expanduser())]
    command += ["--agents-parallel", str(max(1, args.agents_parallel))]
    if args.arxiv_snapshot:
        command += ["--arxiv-snapshot", str(Path(args.arxiv_snapshot).expanduser())]
    if args.kb_root:
        command += ["--kb-root", str(Path(args.kb_root).expanduser())]
    for attempt in range(1, args.mechanical_retries + 1):
        log(f"mechanical driver attempt {attempt}/{args.mechanical_retries}")
        result = subprocess.run(command, cwd=str(kb_root), env=isolated_claude_env())
        if result.returncode == 0:
            return
        if result.returncode == 2:
            # Usage/config refusal (bad run.json, mode drift, unconfigured
            # decision model): retrying the identical argv cannot succeed and
            # would only burn two 60s cooldowns on the default smart-jev path.
            raise RuntimeError(
                f"mechanical driver refused the run (exit 2); fix the reported "
                f"configuration and re-run with --resume"
            )
        log(f"driver exit {result.returncode}; cooling down 60s before retry")
        time.sleep(60)
    raise RuntimeError(f"mechanical driver failed after {args.mechanical_retries} attempts")


def writer_prompts(run_dir: Path, args: argparse.Namespace, wiki: object) -> tuple[str, str]:
    """(system_prompt, user_prompt) for the headless writer — composed by the
    same wiki_chat factory the interactive wiki uses; the only divergence is
    publisher="launcher"（审计门后停止，机械尾部归 launcher）."""
    params = {
        "topic": args.topic,
        "review_mode": args.review_mode,
        "time_range": args.time_range,
        "search_strategy": args.search_strategy,
        "selection_strategy": args.selection_strategy,
        "selection_model": getattr(args, "selection_model", "") or "",
        "seed_arxiv_ids": args.seed_arxiv_ids,
        "target_style": args.target_style,
        "focus": args.focus,
    }
    return wiki.workflow_turn_prompts(
        params=params,
        run_dir=run_dir,
        kb_root=resolve_kb_root(args),
        pipeline_root=pipeline_root(),
        publisher="launcher",
    )


def resolve_writer_model(args: argparse.Namespace) -> str:
    """Pin the spawned writer's model. Without --model the spawned ``claude -p``
    resolves its own default, which can fall back to an expensive frontier
    model mid-session (opus-4-8 was billed on 2026-09-18). Priority: explicit
    flag > ANTHROPIC_MODEL > the driver's pinned fast model. Deliberately does
    NOT consult CLAUDE_CODE_SUBAGENT_MODEL: shell profiles export it globally
    (e.g. the "-cc" SKU), and treating it as an intent signal made the pinned
    default unreachable. Subagent consistency is handled at spawn time instead
    (isolated_claude_env strips the var so Task subagents inherit this model)."""
    return (
        getattr(args, "writer_model", None)
        or os.environ.get("ANTHROPIC_MODEL")
        or DRIVER_AGENT_MODEL
    )




def run_writer(args: argparse.Namespace, run_dir: Path, prompt: str, system_prompt: str) -> bool:
    """Run one writer round. Returns True when the writer signalled a
    user-decision stop (deep-read shortfall is a designed decision point, not a
    failure) — the caller must then stop instead of feeding more rounds."""
    cli = resolve_cli()
    if not cli:
        raise RuntimeError("claude CLI not found; writer stage cannot run")
    env = isolated_claude_env()
    auth_problem = claude_auth_ready(env)
    if auth_problem:
        raise RuntimeError(auth_problem)
    model = resolve_writer_model(args)
    writer_log = run_dir / LAUNCH_DIRNAME / "writer.log"
    log(f"writer agent starting (model: {model}, log: {writer_log})")
    with open(writer_log, "a", encoding="utf-8") as handle:
        handle.write(f"\n===== writer round {time.strftime('%Y-%m-%dT%H:%M:%S')} (model: {model}) =====\n")
        handle.flush()
        result = complete(
            prompt,
            timeout_s=args.writer_timeout,
            cli=cli,
            model=model,
            cwd=resolve_kb_root(args),
            env=env,
            label=f"writer-{run_dir.name}",
            system_prompt=system_prompt,
            stream=True,
            stream_to=handle,
        )
    if result.returncode:
        raise RuntimeError(f"writer agent exit {result.returncode} (see {writer_log})")
    try:
        tail = writer_log.read_text(encoding="utf-8")[-20000:]
    except OSError:
        tail = ""
    return USER_DECISION_STOP in tail


def prepare_gate_inputs(run_dir: Path) -> None:
    """Gates read ONE merged evidence set: always rebuild evidence.jsonl via
    the shared consolidation (same function finalize_run uses). A cached
    merge lags resumed deep-read rounds and made the launcher gate and the
    finalize gate audit different evidence sets (20260929 split-brain)."""
    consolidate_evidence(run_dir)


MEMO_FORMAT_RULE_IDS = {
    # _article_quality reports these as warnings (pre-contract settled runs
    # must keep passing validate_current_reviews); for a freshly written run
    # they are hard gate problems — the wiki renders memo superscripts into
    # reading links and inline arXiv links break that rendering.
    "memo-inline-arxiv-link",
    "memo-superscript-citations",
    "memo-grouped-citation",
}


def editorial_problems(run_dir: Path) -> list[str]:
    """Full editorial-quality gate over every deliverable that exists (all
    styles), with --evidence-jsonl so the figures-available check is live.
    Findings that are errors gate; the memo format trio upgrades its warnings
    to gate problems (wiki rendering contract); other warnings stay advisory
    in the audit output only."""
    style_flags = {
        "memo": "scientific-memo_keyan.md",
        "zhihu": "zhihu-explainer_zhihu.md",
        "xiaohongshu": "xiaohongshu-post_xiaohongshu.md",
    }
    command = [
        sys.executable,
        str(SKILLS_ROOT / "embodied-ai-review-writer" / "scripts" / "write.py"),
        "audit-article-quality", "--json",
        "--evidence-jsonl", str(run_dir / "evidence.jsonl"),
    ]
    present = False
    for flag, name in style_flags.items():
        if (run_dir / name).is_file():
            command += [f"--{flag}", str(run_dir / name)]
            present = True
    if not present:
        return []
    result = subprocess.run(command, capture_output=True, text=True, cwd=str(pipeline_root()))
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return [f"editorial quality audit did not emit JSON (exit {result.returncode}): {(result.stderr or '')[-200:]}"]
    problems = []
    for finding in payload.get("findings", []):
        rule = str(finding.get("rule") or "")
        if finding.get("severity") == "error" or rule in MEMO_FORMAT_RULE_IDS:
            problems.append(f"editorial {rule}: {finding.get('message')}")
    return problems


def gate_articles(run_dir: Path) -> list[str]:
    """Deliverables the citation gate must audit: the declared single style,
    else every standard face that exists. A zhihu-only or xiaohongshu-only run
    has no memo file, so auditing a hard-coded memo path reported
    "article missing" for an article this run never promised."""
    manifest: dict = {}
    try:
        loaded = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            manifest = loaded
    except (OSError, json.JSONDecodeError):
        pass
    style = declared_style(manifest)
    if style in STYLE_TO_FILE:
        return [STYLE_TO_FILE[style]]
    return [name for name in STANDARD_ARTICLES if (run_dir / name).is_file()]


def collect_gate_problems(run_dir: Path) -> list[str]:
    problems: list[str] = []
    # The gates print a bare "N problem(s):" header before the itemized
    # lines; a kept header becomes a phantom problem that burns
    # continuation rounds on nothing.
    gate_header = re.compile(r"^\d+ problem\(s\):$")
    prepare_gate_inputs(run_dir)
    articles = gate_articles(run_dir)
    if not articles:
        return ["run 目录没有成稿（scientific-memo_keyan.md / zhihu-explainer_zhihu.md / "
                "xiaohongshu-post_xiaohongshu.md 均缺失）"]
    problems.extend(editorial_problems(run_dir))
    trace_ok, trace_problems = build_trace_map(run_dir, SKILLS_ROOT)
    if not trace_ok:
        problems.extend(f"trace-map: {line}" for line in trace_problems)
        problems.append("trace-map 未生成：删改成稿中无证据支撑的 arXiv 引用（UNCOVERED 行），或补证据后重跑；勿手写 trace-map.json")
    audit_command = [sys.executable, str(SCRIPTS_ROOT / "run.py"), "audit-citations"]
    for name in articles:
        audit_command += ["--article", str(run_dir / name)]
    audit_command += [
        "--appendix", str(run_dir / "evidence-appendix.md"),
        "--evidence-jsonl", str(run_dir / "evidence.jsonl"),
    ]
    audit = subprocess.run(audit_command, capture_output=True, text=True)
    if audit.returncode:
        problems.extend(
            line for line in audit.stdout.splitlines()
            if line.strip() and not gate_header.match(line.strip()))
    bundle = subprocess.run(
        [sys.executable, str(SCRIPTS_ROOT / "run.py"), "check-bundle", str(run_dir), "--pre-settle"],
        capture_output=True, text=True,
    )
    if bundle.returncode:
        # The gate loop runs BEFORE run.py finalize, so the run is still
        # in-progress: --pre-settle keeps the lifecycle line out of the output
        # (settle semantics are re-checked by finalize under the settled
        # status). The "run not settled" filter stays as a belt-and-braces for
        # an older scripts root that does not know the flag yet.
        problems.extend(
            line for line in bundle.stdout.splitlines()
            if line.strip() and "run not settled" not in line
            and not gate_header.match(line.strip()))
    return problems


def is_evidence_problem(problem: str) -> bool:
    """True when the problem is missing EVIDENCE (not prose the writer can fix).

    Floor/coverage failures say "续跑 run.py pipeline 补检索/深读" — that is a
    mechanical-driver job. Feeding them to the writer continuation can never
    resolve them (the writer is forbidden from re-running retrieval), so the
    loop burned every retry round on an unsolvable problem (2026-10-13, run 02:
    79 extractions died on a network outage and the launcher spent 3 writer
    rounds unable to help)."""
    text = problem.lower()
    return any(
        token in text
        for token in (
            "full_text_floor",
            "accepted_paper_floor",
            "cited_paper_floor",
            "candidate_floor",
            "coverage/saturation",
            "补检索",
            "深读",
            "evidence-floor",
        )
    )


def run_finalize(args: argparse.Namespace, run_dir: Path) -> None:
    """机械 settle/publish 尾：run.py finalize 盖章 run.json、复跑两道门、
    拷 evidence/、翻 settled、登记 catalog、重建 wiki 快照——即 launcher
    publisher prompt 里明说"不要触碰"的那一串。幂等，可随 --resume 重入。"""
    command = [
        sys.executable, str(SCRIPTS_ROOT / "run.py"), "finalize",
        "--run-dir", str(run_dir), "--kb-root", str(resolve_kb_root(args)),
    ]
    if args.target_style in STYLE_VALUES:  # "all" 不声明，保持三风格推断
        command += ["--style", args.target_style]
    if args.scope_note:
        command += ["--scope-note", args.scope_note]
    log("finalize: " + " ".join(command))
    if subprocess.run(command, cwd=str(resolve_kb_root(args))).returncode:
        raise RuntimeError(
            "run.py finalize 未过：按其输出执行。若是「精读数量不够」，那是用户决策点——"
            "汇报选定的精读论文列表后等待用户决策（补充信息或扩大综述范围），"
            "勿 --resume 硬修；其他门禁问题修复后 --resume 重跑。"
        )


def verify_publish(args: argparse.Namespace, run_dir: Path, wiki: object) -> list[str]:
    """Post-settle publish checks; fix what is mechanically fixable, report
    what needs eyes."""
    problems: list[str] = []
    kb_root = resolve_kb_root(args)
    catalog = kb_root / CATALOG_PATH
    if not catalog.is_file() or run_dir.name not in catalog.read_text(encoding="utf-8"):
        problems.append(f"catalog 未登记本 run：{catalog} 缺少 {run_dir.name}")
    current = kb_root / "wiki" / "data" / "current.json"
    if not current.is_file():
        problems.append("wiki 快照不存在（wiki.py build-wiki 未跑）")
    else:
        try:
            snapshot = json.loads(current.read_text(encoding="utf-8"))
            latest = sorted((kb_root / "wiki" / "data" / "snapshots").iterdir())[-1]
            manifest = json.loads((latest / "manifest.json").read_text(encoding="utf-8"))

            def topic_haystack(topic: object) -> str:
                if isinstance(topic, dict):
                    return " ".join(str(topic.get(key, "")) for key in ("topic_key", "title"))
                return str(topic)

            # The wiki indexes topics by topic_key/title (folder name without
            # the "literature-review-" prefix, the date suffix and the optional
            # -v<N> repeat-production mark).
            slug = re.sub(r"-(\d{8})(-v\d+)?$", "", run_dir.name.replace("literature-review-", ""))
            if not any(slug in topic_haystack(topic) for topic in manifest.get("topics", [])):
                problems.append("wiki 最新快照不含本 run 话题")
        except (OSError, ValueError, IndexError) as exc:
            problems.append(f"wiki 快照校验失败：{exc}")
    return problems


def backfill_reentry_params(args: argparse.Namespace, run_dir: Path) -> None:
    """Re-entry (--run-dir): the run manifest defines the run identity — load
    topic/mode/range (and infer the KB root) instead of requiring CLI
    re-statement, which a bare `--run-dir` resume never provides."""
    run_json = run_dir / "run.json"
    if run_json.is_file():
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        args.topic = manifest.get("topic") or args.topic
        args.review_mode = manifest.get("review_mode") or args.review_mode
        args.time_range = manifest.get("time_range") or args.time_range
        # A bare --resume leaves --target-style at the parser default
        # (scientific-memo) and run_finalize would forward that as --style,
        # shrinking a three-style run at settle. The birth input is the run's
        # real scope; "all"/missing keeps the CLI value for legacy runs.
        inputs = manifest.get("inputs")
        if isinstance(inputs, dict) and str(inputs.get("target_style") or "").strip():
            args.target_style = str(inputs["target_style"]).strip()
    if not args.kb_root:
        # init_run places runs at <kb-root>/work/<run>; infer the root from
        # the run dir so publish steps land in the right KB.
        args.kb_root = str(run_dir.parent.parent)


def launch(args: argparse.Namespace) -> int:
    wiki = load_wiki_prompts()
    run_dir = Path(args.run_dir) if args.run_dir else None

    if args.status:
        return print_status(run_dir)
    if args.stop:
        return print_stop(run_dir)
    if args.selection_strategy == "smart-jev" and not system_one_ready():
        # The default strategy is the decision model; refuse before creating a
        # run dir instead of failing inside the driver (same stance as the wiki
        # kickoff's 400 and the driver's own preflight).
        print(
            "决策模型（System One / jev）未配置：需要 "
            "EMBODIED_SYSTEM_ONE_URL（或 ANTHROPIC_BASE_URL）与 "
            "EMBODIED_SYSTEM_ONE_API_KEY（或 ANTHROPIC_AUTH_TOKEN）。"
            "可改用 --selection-strategy smart（执行模型）。",
            file=sys.stderr,
        )
        return 2

    # fresh launch: create the run birth certificate via run.py init
    if run_dir is None:
        kb_root = resolve_kb_root(args)
        # The interview answers must reach run.json `inputs`, like the wiki
        # kickoff's payload: the writer's --pre-settle gates run before
        # finalize stamps `style`, so `inputs.target_style` is the only scope
        # declaration on disk at that point. Without it a CLI single-style
        # launch was told to ship the whole triplet.
        inputs_payload = {
            "source": "cli",
            "requested_review_mode": args.review_mode,
            "target_style": getattr(args, "target_style", "") or "",
            "focus": getattr(args, "focus", "") or "",
            "search_strategy": getattr(args, "search_strategy", "") or "",
            "selection_strategy": getattr(args, "selection_strategy", "") or "",
            "seed_arxiv_ids": getattr(args, "seed_arxiv_ids", "") or "",
        }
        init_command = [
            sys.executable, str(SCRIPTS_ROOT / "run.py"), "init",
            "--topic", args.topic, "--review-mode", args.review_mode,
            "--work-dir", str(kb_root / "work"),
            "--inputs-json", json.dumps(inputs_payload, ensure_ascii=False),
        ]
        if getattr(args, "run_version", 1) > 1:
            init_command += ["--run-version", str(args.run_version)]
        # time-range is scope metadata only and defaults to None (the
        # curated-list channel legitimately has no date scope).
        if args.time_range:
            init_command += ["--time-range", args.time_range]
        for kid in (args.knowledge_id or ["EA-DATA"]):
            init_command += ["--knowledge-id", kid]
        init = subprocess.run(init_command, capture_output=True, text=True, cwd=str(kb_root))
        if init.returncode:
            print(init.stderr, file=sys.stderr)
            return 1
        run_dir = Path(init.stdout.strip().splitlines()[0].replace("Initialized run: ", ""))
    run_dir = run_dir.resolve()
    backfill_reentry_params(args, run_dir)
    if stage_done(run_dir, "published"):
        log("run already published; nothing to do")
        return 0

    pid_path = run_dir / LAUNCH_DIRNAME / "pid"
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    pid_path.write_text(f"{os.getpid()}\n", encoding="utf-8")

    try:
        if not stage_done(run_dir, "mechanical"):
            run_mechanical(args, run_dir)
            mark_stage(run_dir, "mechanical")

        if not stage_done(run_dir, "writer"):
            system_prompt, user_prompt = writer_prompts(run_dir, args, wiki)
            if run_writer(args, run_dir, user_prompt, system_prompt):
                mark_stage(run_dir, "writer", USER_DECISION_STOP)
                log(f"writer 停轮等待用户决策（{USER_DECISION_STOP}）：run 保持 in-progress，"
                    "补充信息（种子/关注重点）或扩大综述范围后 --resume 续跑。这是正确终态，不是失败。")
                return 4
            mark_stage(run_dir, "writer")

        # gates with one continuation round per retry budget
        for round_index in range(args.max_agent_retries + 1):
            problems = collect_gate_problems(run_dir)
            if not problems:
                break
            log(f"gate problems ({len(problems)}); continuation round {round_index + 1}")
            if round_index == args.max_agent_retries:
                for problem in problems:
                    log(f"UNRESOLVED: {problem}")
                return 2
            # Evidence-side failures are a mechanical-driver job (the driver is
            # idempotent and retries HELD extractions); a writer continuation
            # is forbidden from touching retrieval and would just re-report.
            if any(is_evidence_problem(p) for p in problems):
                for problem in problems:
                    if is_evidence_problem(problem):
                        log(f"evidence shortfall, re-running mechanical driver: {problem}")
                # clear the stage marker so the driver re-runs (it is
                # idempotent and retries HELD extractions)
                (run_dir / LAUNCH_DIRNAME / "mechanical.done").unlink(missing_ok=True)
                run_mechanical(args, run_dir)
                mark_stage(run_dir, "mechanical")
                continue
            feedback = "\n".join(problems)
            continuation = wiki.build_continuation_prompt(
                feedback=feedback, target_style=args.target_style, publisher="launcher")
            continuation_system = wiki.workflow_turn_system_prompt(
                pipeline_root(), resolve_kb_root(args), publisher="launcher")
            if run_writer(args, run_dir, continuation, continuation_system):
                log(f"writer 停轮等待用户决策（{USER_DECISION_STOP}）：run 保持 in-progress。")
                return 4

        run_finalize(args, run_dir)
        publish_problems = verify_publish(args, run_dir, wiki)
        mark_stage(run_dir, "published", "; ".join(publish_problems) or "ok")
        if publish_problems:
            log("publish 需要人工确认：")
            for problem in publish_problems:
                log(f"  - {problem}")
            return 3
        log("published: gates passed, settled, catalog registered, wiki snapshot rebuilt")
        return 0
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        log(f"FAILED: {exc}")
        log(f"resume with: run.py launch --resume --run-dir {run_dir}")
        return 1


def print_status(run_dir: Path | None) -> int:
    if run_dir is None or not run_dir.is_dir():
        print("需要 --run-dir（或对应的 run 目录不存在）", file=sys.stderr)
        return 1
    stages = ["mechanical", "writer", "published"]
    for stage in stages:
        marker = run_dir / LAUNCH_DIRNAME / f"{stage}.done"
        print(f"{stage}: {'done' if marker.is_file() else 'pending'}"
              + (f" ({marker.read_text(encoding='utf-8').strip()})" if marker.is_file() else ""))
    pid_path = run_dir / LAUNCH_DIRNAME / "pid"
    if pid_path.is_file():
        pid = int(pid_path.read_text().strip())
        running = Path(f"/proc/{pid}").is_dir()
        print(f"launcher pid: {pid} ({'running' if running else 'not running'})")
    writer_log = run_dir / LAUNCH_DIRNAME / "writer.log"
    if writer_log.is_file():
        print(f"writer log: {writer_log}")
    return 0


def print_stop(run_dir: Path | None) -> int:
    pid_path = (run_dir / LAUNCH_DIRNAME / "pid") if run_dir else None
    if not pid_path or not pid_path.is_file():
        print("no pid file; nothing to stop", file=sys.stderr)
        return 1
    pid = int(pid_path.read_text().strip())
    os.kill(pid, signal.SIGTERM)
    print(f"sent SIGTERM to {pid}")
    return 0


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/run.py."""
    return launch(args)
