#!/usr/bin/env python3
"""Headless literature-review launcher: one command, run to published.

Chains the mechanical driver (run_review_pipeline.py) with the judgment
stages as a detached one-shot claude agent (the wiki workflow prompt), then
verifies the gates, settle state, catalog registration, and wiki snapshot.
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
import signal
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT))
from lib.agent_invoke import run_one_shot_agent, resolve_cli  # noqa: E402
from lib.review_runs import STYLE_TO_FILE  # noqa: E402

STYLE_VALUES = tuple(STYLE_TO_FILE)
LAUNCH_DIRNAME = ".launch"
NESTED_CLAUDE_ENV_KEYS = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT")
CATALOG_PATH = Path("knowledge/literature-review-catalog.md")


def load_wiki_prompts():
    """Importlib-load build_workflow_prompt / build_continuation_prompt from
    scripts/wiki_chat.py without standing up the chat server."""
    spec = importlib.util.spec_from_file_location("wiki_chat_lib", REPO_ROOT / "scripts" / "wiki_chat.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def strip_nested_claude_env() -> dict:
    env = dict(os.environ)
    for key in NESTED_CLAUDE_ENV_KEYS:
        env.pop(key, None)
    return env


def stage_done(run_dir: Path, stage: str) -> bool:
    return (run_dir / LAUNCH_DIRNAME / f"{stage}.done").is_file()


def mark_stage(run_dir: Path, stage: str, detail: str = "") -> None:
    marker = run_dir / LAUNCH_DIRNAME / f"{stage}.done"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {detail}\n", encoding="utf-8")


def log(message: str) -> None:
    print(f"[LAUNCH] {message}", flush=True)


def run_mechanical(args: argparse.Namespace, run_dir: Path) -> None:
    """Run the mechanical driver with bounded retries; idempotent stages make
    each retry a resume."""
    command = [
        sys.executable, str(REPO_ROOT / "scripts" / "run_review_pipeline.py"),
        "--run-dir", str(run_dir),
        "--topic", args.topic,
        "--review-mode", args.review_mode,
        "--time-range", args.time_range,
        "--focus", args.focus or "",
        "--search-strategy", args.search_strategy,
        "--deep-read-limit", str(args.deep_read_limit),
    ]
    if args.seed_arxiv_ids:
        command += ["--seed-arxiv-ids", args.seed_arxiv_ids]
    if args.arxiv_snapshot:
        command += ["--arxiv-snapshot", str(Path(args.arxiv_snapshot).expanduser())]
    if args.kb_root:
        command += ["--kb-root", str(Path(args.kb_root).expanduser())]
    for attempt in range(1, args.mechanical_retries + 1):
        log(f"mechanical driver attempt {attempt}/{args.mechanical_retries}")
        result = subprocess.run(command, cwd=str(REPO_ROOT), env=strip_nested_claude_env())
        if result.returncode == 0:
            return
        log(f"driver exit {result.returncode}; cooling down 60s before retry")
        time.sleep(60)
    raise RuntimeError(f"mechanical driver failed after {args.mechanical_retries} attempts")


def writer_prompt(run_dir: Path, args: argparse.Namespace, wiki: object) -> str:
    params = {
        "topic": args.topic,
        "review_mode": args.review_mode,
        "time_range": args.time_range,
        "search_strategy": args.search_strategy,
        "seed_arxiv_ids": args.seed_arxiv_ids,
        "target_style": args.target_style,
        "focus": args.focus,
    }
    return wiki.build_workflow_prompt(
        params=params, run_dir=run_dir,
        kb_root=Path(args.kb_root or REPO_ROOT).expanduser().resolve(),
        pipeline_root=REPO_ROOT / "skills",
    )


def run_writer(args: argparse.Namespace, run_dir: Path, prompt: str) -> None:
    cli = resolve_cli()
    if not cli:
        raise RuntimeError("claude CLI not found; writer stage cannot run")
    writer_log = run_dir / LAUNCH_DIRNAME / "writer.log"
    log(f"writer agent starting (log: {writer_log})")
    with open(writer_log, "a", encoding="utf-8") as handle:
        handle.write(f"\n===== writer round {time.strftime('%Y-%m-%dT%H:%M:%S')} =====\n")
        handle.flush()
        result = subprocess.run(
            [cli, "-p", "--permission-mode", "bypassPermissions",
             "--output-format", "stream-json"],
            input=prompt, text=True, stdout=handle, stderr=handle,
            timeout=args.writer_timeout, cwd=str(REPO_ROOT),
            env=strip_nested_claude_env(),
        )
    if result.returncode:
        raise RuntimeError(f"writer agent exit {result.returncode} (see {writer_log})")


def prepare_gate_inputs(run_dir: Path) -> None:
    """The gates read merged evidence files; produce them when the writer
    agent did not."""
    evidence_dir = run_dir / "evidence"
    merged = run_dir / "evidence-all.jsonl"
    if evidence_dir.is_dir() and not merged.is_file():
        lines: list[str] = []
        for evidence_file in sorted(evidence_dir.glob("*.jsonl")):
            lines.extend(line for line in evidence_file.read_text(encoding="utf-8").splitlines() if line.strip())
        merged.write_text("\n".join(lines) + "\n", encoding="utf-8")
    canonical = run_dir / "evidence.jsonl"
    if merged.is_file() and not canonical.is_file():
        canonical.write_text(merged.read_text(encoding="utf-8"), encoding="utf-8")


def collect_gate_problems(run_dir: Path) -> list[str]:
    problems: list[str] = []
    prepare_gate_inputs(run_dir)
    if not (run_dir / "scientific-memo_keyan.md").is_file() and not (run_dir / "zhihu-explainer_zhihu.md").is_file():
        return ["run 目录没有成稿（scientific-memo_keyan.md / zhihu-explainer_zhihu.md 均缺失）"]
    audit = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "audit_citations.py"),
         "--article", str(run_dir / "scientific-memo_keyan.md"),
         "--appendix", str(run_dir / "evidence-appendix.md"),
         "--evidence-jsonl", str(run_dir / "evidence-all.jsonl")],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if audit.returncode:
        problems.extend(line for line in audit.stdout.splitlines() if line.strip())
    bundle = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "check_run_bundle.py"), str(run_dir)],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if bundle.returncode:
        problems.extend(line for line in bundle.stdout.splitlines() if line.strip())
    return problems


def ensure_settled(run_dir: Path, args: argparse.Namespace) -> None:
    run_json_path = run_dir / "run.json"
    manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
    if manifest.get("status") == "settled":
        return
    if not str(manifest.get("style") or "").strip():
        manifest["style"] = args.target_style if args.target_style in STYLE_VALUES else "scientific-memo"
        manifest["scope_note"] = args.scope_note or "单风格交付：launcher 程序化运行声明的收窄范围。"
    manifest.setdefault("files", {
        "query_plan": "query-plan.json",
        "candidate_registry": "candidate-registry.json",
        "coverage_report": "coverage-report.json",
        "evidence": "evidence.jsonl",
        "review_packet": "review-packet.md",
        "writing_brief": "writing-brief.md",
        "evidence_appendix": "evidence-appendix.md",
        "outputs": [],
    })
    manifest["status"] = "settled"
    run_json_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_publish(args: argparse.Namespace, run_dir: Path, wiki: object) -> list[str]:
    """Post-settle publish checks; fix what is mechanically fixable, report
    what needs eyes."""
    problems: list[str] = []
    kb_root = Path(args.kb_root or REPO_ROOT).resolve()
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
            if not any(run_dir.name.replace("literature-review-", "") in str(topic) for topic in manifest.get("topics", [])):
                problems.append("wiki 最新快照不含本 run 话题")
        except (OSError, ValueError, IndexError) as exc:
            problems.append(f"wiki 快照校验失败：{exc}")
    return problems


def launch(args: argparse.Namespace) -> int:
    wiki = load_wiki_prompts()
    run_dir = Path(args.run_dir) if args.run_dir else None

    if args.status:
        return print_status(run_dir)
    if args.stop:
        return print_stop(run_dir)

    # fresh launch: create the run birth certificate via init_run.py
    if run_dir is None:
        init_command = [
            sys.executable, str(REPO_ROOT / "scripts" / "init_run.py"),
            "--topic", args.topic, "--review-mode", args.review_mode,
            "--time-range", args.time_range,
        ]
        for kid in (args.knowledge_id or ["EA-DATA"]):
            init_command += ["--knowledge-id", kid]
        init = subprocess.run(init_command, capture_output=True, text=True, cwd=str(REPO_ROOT))
        if init.returncode:
            print(init.stderr, file=sys.stderr)
            return 1
        run_dir = Path(init.stdout.strip().splitlines()[0].replace("Initialized run: ", ""))
    run_dir = run_dir.resolve()
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
            run_writer(args, run_dir, writer_prompt(run_dir, args, wiki))
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
                feedback=feedback, target_style=args.target_style)
            run_writer(args, run_dir, continuation)

        ensure_settled(run_dir, args)
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
        log(f"resume with: python3 scripts/launch_review.py --resume --run-dir {run_dir}")
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
    parser.add_argument("--arxiv-snapshot", help="OAI JSONL or SQLite/FTS5 db for offline arXiv retrieval")
    parser.add_argument("--kb-root", help="KB root (default: repo)")
    parser.add_argument("--knowledge-id", action="append", help="EA/ERR knowledge id; repeatable (default EA-DATA)")
    parser.add_argument("--target-style", default="scientific-memo",
                        help="writer 交付风格（all=三风格；scientific-memo/expert-explainer/kol-thread/survey）")
    parser.add_argument("--scope-note", help="收窄范围时必须说明原因")
    parser.add_argument("--run-dir", help="已有 run 目录（--status/--stop/--resume 必填）")
    parser.add_argument("--deep-read-limit", type=int, default=48)
    parser.add_argument("--mechanical-retries", type=int, default=3)
    parser.add_argument("--max-agent-retries", type=int, default=2)
    parser.add_argument("--writer-timeout", type=float, default=5400.0)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--stop", action="store_true")
    args = parser.parse_args(argv)
    return launch(args)


if __name__ == "__main__":
    sys.exit(main())
