#!/usr/bin/env python3
"""Headless literature-review launcher: one command, run to published.

Chains the mechanical driver (run_review_pipeline.py) with the judgment
stages as a detached one-shot claude agent (the wiki workflow prompt), then
settles/publishes via finalize_run.py, then verifies catalog + wiki snapshot.
Designed to survive the launching session ending: stages are marked on disk,
idempotent, and re-enterable via --resume.

Usage:
  # launch detached (default); returns immediately with a log path
  python3 scripts/launch_review.py \
    --topic "ego-exo 数据集：采集与标注" --review-mode systematic \
    --time-range 2016-09-17..2026-09-17 \
    --focus "以 Ego-Exo4D (2311.18259) 为核心，综述采集与标注" \
    --seed-arxiv-ids 2311.18259 \
    [--arxiv-snapshot ~/Documents/arxiv/arxiv-metadata-oai-snapshot.sqlite]

  # watch progress / re-enter after an interruption / stop
  python3 scripts/launch_review.py --status --run-dir work/<run>
  python3 scripts/launch_review.py --resume --run-dir work/<run>
  python3 scripts/launch_review.py --stop   --run-dir work/<run>

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

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
try:
    from lib.layout import default_kb_root, find_roots  # noqa: E402
    from lib.review_runs import STYLE_TO_FILE  # noqa: E402
except ImportError:  # installed console-script entry: package import path
    from wiki_scripts.lib.layout import default_kb_root, find_roots  # noqa: E402
    from wiki_scripts.lib.review_runs import STYLE_TO_FILE  # noqa: E402
# AI-model capability goes through the harness binding (pybind-style); prompts and KB layout stay with the feature module.
from embodied_learning.harness.claude import (  # noqa: E402
    DRIVER_AGENT_MODEL,
    claude_auth_ready,
    complete,
    isolated_claude_env,
    resolve_cli,
)

_REPO_ROOT, SKILLS_ROOT, SCRIPTS_ROOT = find_roots()
STYLE_VALUES = tuple(STYLE_TO_FILE)
LAUNCH_DIRNAME = ".launch"
CATALOG_PATH = Path("knowledge/literature-review-catalog.md")


def load_wiki_prompts():
    """Importlib-load build_workflow_prompt / build_continuation_prompt from
    wiki_chat without standing up the chat server."""
    wiki_chat_path = SCRIPTS_ROOT / "wiki_chat.py"
    spec = importlib.util.spec_from_file_location("wiki_chat_lib", wiki_chat_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


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
        sys.executable, str(SCRIPTS_ROOT / "run_review_pipeline.py"),
        "--run-dir", str(run_dir),
        "--topic", args.topic,
        "--review-mode", args.review_mode,
        "--focus", args.focus or "",
        "--search-strategy", args.search_strategy,
        "--deep-read-limit", str(args.deep_read_limit),
    ]
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


def run_writer(args: argparse.Namespace, run_dir: Path, prompt: str, system_prompt: str) -> None:
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


def prepare_gate_inputs(run_dir: Path) -> None:
    """The gates read merged evidence files; produce them when the writer
    agent did not."""
    evidence_dir = run_dir / "evidence"
    merged = run_dir / "evidence-all.jsonl"
    canonical = run_dir / "evidence.jsonl"
    if evidence_dir.is_dir() and not merged.is_file():
        lines: list[str] = []
        for evidence_file in sorted(evidence_dir.glob("*.jsonl")):
            lines.extend(line for line in evidence_file.read_text(encoding="utf-8").splitlines() if line.strip())
        merged.write_text("\n".join(lines) + "\n", encoding="utf-8")
    elif not evidence_dir.is_dir() and not merged.is_file() and canonical.is_file():
        # Flat runs keep canonical evidence at the run root with no evidence/
        # subdir to merge; the gates still read the merged path.
        merged.write_text(canonical.read_text(encoding="utf-8"), encoding="utf-8")
    if merged.is_file() and not canonical.is_file():
        canonical.write_text(merged.read_text(encoding="utf-8"), encoding="utf-8")


MEMO_FORMAT_RULE_IDS = {
    # _article_quality reports these as warnings (pre-contract settled runs
    # must keep passing validate_current_reviews); for a freshly written run
    # they are hard gate problems — the wiki renders memo superscripts into
    # reading links and inline arXiv links break that rendering.
    "memo-inline-arxiv-link",
    "memo-superscript-citations",
    "memo-grouped-citation",
}


def memo_format_problems(run_dir: Path) -> list[str]:
    memo = run_dir / "scientific-memo_keyan.md"
    if not memo.is_file():
        return []
    result = subprocess.run(
        [sys.executable,
         str(pipeline_root() / "skills" / "embodied-ai-review-writer" / "scripts" / "writing_audit.py"),
         "audit-article-quality", "--memo", str(memo), "--json"],
        capture_output=True, text=True, cwd=str(pipeline_root()),
    )
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return [f"editorial quality audit did not emit JSON (exit {result.returncode}): {(result.stderr or '')[-200:]}"]
    return [
        f"{finding['rule']}: {finding['message']}"
        for finding in payload.get("findings", [])
        if finding.get("rule") in MEMO_FORMAT_RULE_IDS
    ]


def collect_gate_problems(run_dir: Path) -> list[str]:
    problems: list[str] = []
    prepare_gate_inputs(run_dir)
    if not (run_dir / "scientific-memo_keyan.md").is_file() and not (run_dir / "zhihu-explainer_zhihu.md").is_file():
        return ["run 目录没有成稿（scientific-memo_keyan.md / zhihu-explainer_zhihu.md 均缺失）"]
    problems.extend(memo_format_problems(run_dir))
    audit = subprocess.run(
        [sys.executable, str(SCRIPTS_ROOT / "audit_citations.py"),
         "--article", str(run_dir / "scientific-memo_keyan.md"),
         "--appendix", str(run_dir / "evidence-appendix.md"),
         "--evidence-jsonl", str(run_dir / "evidence-all.jsonl")],
        capture_output=True, text=True,
    )
    if audit.returncode:
        problems.extend(line for line in audit.stdout.splitlines() if line.strip())
    bundle = subprocess.run(
        [sys.executable, str(SCRIPTS_ROOT / "check_run_bundle.py"), str(run_dir)],
        capture_output=True, text=True,
    )
    if bundle.returncode:
        # The gate loop runs BEFORE finalize_run.py, so the run is still
        # in-progress and check_run_bundle's "run not settled" line is timing
        # noise that would burn a --max-agent-retries round; settle semantics
        # are re-checked by finalize under the settled status.
        problems.extend(
            line for line in bundle.stdout.splitlines()
            if line.strip() and "run not settled" not in line)
    return problems


def run_finalize(args: argparse.Namespace, run_dir: Path) -> None:
    """机械 settle/publish 尾：finalize_run.py 盖章 run.json、复跑两道门、
    拷 evidence/、翻 settled、登记 catalog、重建 wiki 快照——即 launcher
    publisher prompt 里明说"不要触碰"的那一串。幂等，可随 --resume 重入。"""
    command = [
        sys.executable, str(SCRIPTS_ROOT / "finalize_run.py"),
        "--run-dir", str(run_dir), "--kb-root", str(resolve_kb_root(args)),
    ]
    if args.target_style in STYLE_VALUES:  # "all" 不声明，保持三风格推断
        command += ["--style", args.target_style]
    if args.scope_note:
        command += ["--scope-note", args.scope_note]
    log("finalize: " + " ".join(command))
    if subprocess.run(command, cwd=str(resolve_kb_root(args))).returncode:
        raise RuntimeError("finalize_run.py 未过（按其输出修复后 --resume 重跑）")


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
        problems.append("wiki 快照不存在（build_research_wiki.py 未跑）")
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
            # the "literature-review-" prefix and the date suffix).
            slug = re.sub(r"-\d{8}$", "", run_dir.name.replace("literature-review-", ""))
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

    # fresh launch: create the run birth certificate via init_run.py
    if run_dir is None:
        kb_root = resolve_kb_root(args)
        init_command = [
            sys.executable, str(SCRIPTS_ROOT / "init_run.py"),
            "--topic", args.topic, "--review-mode", args.review_mode,
            "--work-dir", str(kb_root / "work"),
        ]
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
            run_writer(args, run_dir, user_prompt, system_prompt)
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
            feedback = "\n".join(problems)
            continuation = wiki.build_continuation_prompt(
                feedback=feedback, target_style=args.target_style, publisher="launcher")
            continuation_system = wiki.workflow_turn_system_prompt(
                pipeline_root(), resolve_kb_root(args), publisher="launcher")
            run_writer(args, run_dir, continuation, continuation_system)

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
        log(f"resume with: launch_review --resume --run-dir {run_dir}")
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--topic")
    parser.add_argument("--review-mode", choices=["rapid", "scoping", "systematic"], default="systematic")
    parser.add_argument("--time-range", help="YYYY-MM-DD..YYYY-MM-DD")
    parser.add_argument("--focus")
    parser.add_argument("--search-strategy", choices=["smart", "fast", "seeds"], default="smart")
    parser.add_argument("--seed-arxiv-ids")
    parser.add_argument("--external-candidates", action="append", default=[],
                        help="harvest-curated-list JSON as the candidate source; forwarded to the driver (repeatable)")
    parser.add_argument("--agents-parallel", type=int, default=10,
                        help="deep-read one-shot agents running concurrently (forwarded to the driver)")
    parser.add_argument("--arxiv-snapshot", help="OAI JSONL or SQLite/FTS5 db for offline arXiv retrieval")
    parser.add_argument("--kb-root", help=f"KB root (default: {default_kb_root()})")
    parser.add_argument("--knowledge-id", action="append", help="EA/ERR knowledge id; repeatable (default EA-DATA)")
    parser.add_argument("--target-style", default="scientific-memo",
                        help="writer 交付风格（all=三风格；scientific-memo/expert-explainer/kol-thread/survey）")
    parser.add_argument("--scope-note", help="收窄范围时必须说明原因")
    parser.add_argument("--run-dir", help="已有 run 目录（--status/--stop/--resume 必填）")
    parser.add_argument("--deep-read-limit", type=int, default=48)
    parser.add_argument("--mechanical-retries", type=int, default=3)
    parser.add_argument("--max-agent-retries", type=int, default=2)
    parser.add_argument("--writer-timeout", type=float, default=5400.0)
    parser.add_argument(
        "--writer-model", default=None,
        help="Model for the spawned writer agent (default: ANTHROPIC_MODEL env > "
        "CLAUDE_CODE_SUBAGENT_MODEL env > the driver's pinned fast model). "
        "Pin it — an unpinned claude -p can fall back to an expensive frontier model.",
    )
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--stop", action="store_true")
    parser.add_argument("--resume", action="store_true",
                        help="续跑已有 run。续跑本就靠阶段标记幂等（直接重跑 --run-dir 即可）；"
                             "此旗子只为让失败提示里的命令字面可用，无额外行为。")
    args = parser.parse_args(argv)
    return launch(args)


if __name__ == "__main__":
    sys.exit(main())
