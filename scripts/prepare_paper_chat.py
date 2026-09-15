#!/usr/bin/env python3
"""Prepare one arXiv paper for wiki paper-chat: ensure pooled + deep-read.

Idempotent single-paper pipeline used by the wiki server's paper-chat entry:

    1. pool check  — pool/arxiv-<id>/extraction.json present?
    2. extraction  — extract_arxiv_content.py --include-full-text → pool add
    3. deep read   — one-shot claude skeleton agent → build_paper_note.py
                     (locator resolution, verbatim audit, auto-repair)

Exit codes: 0 ready (note pass or needs-review), 3 deep-read incomplete but
paper pooled (chat can proceed on raw text), 1 hard failure. Progress prints
one ``[PAPER-CHAT] <stage> <detail>`` line per step for SSE forwarding.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HUB_SCRIPTS = REPO_ROOT / "skills" / "embodied-ai-literature-hub" / "scripts"
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from lib.agent_invoke import (  # noqa: E402
    build_skeleton_prompt,
    pool_root_for,
    read_skeleton_output,
    resolve_cli,
    run_one_shot_agent,
)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root (embodied_learning)
from embodied_learning.knowledge.arxiv_reader import parse_arxiv_id  # noqa: E402
from run_review_pipeline import deep_read_paper  # noqa: E402

SKELETON_TIMEOUT_S = 420.0


def log(message: str) -> None:
    print(f"[PAPER-CHAT] {message}", flush=True)


def normalize_arxiv_id(raw: str) -> str:
    """Shared arXiv-ID grammar; raises with the offending value (the lib
    helper returns None instead, which is awkward for CLI error messages)."""

    normalized = parse_arxiv_id(re.sub(r"^arxiv:", "", str(raw or "").strip(), flags=re.IGNORECASE))
    if normalized is None:
        raise ValueError(f"无效的 arXiv ID：{raw!r}")
    return normalized


def run(command: list[str], *, timeout: float) -> subprocess.CompletedProcess:
    return subprocess.run(
        command, cwd=str(REPO_ROOT), text=True, capture_output=True, timeout=timeout, check=False
    )


def ensure_extraction(paper_id: str, pool_root: Path, force: bool) -> bool:
    pool_dir = pool_root / f"arxiv-{paper_id}"
    if (pool_dir / "extraction.json").is_file() and not force:
        log(f"pool 命中：{pool_dir}")
        return True
    log("未入池，开始全文抽取（HTML → markdown）…")
    output = pool_dir / "extraction.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    result = run(
        [
            sys.executable, str(HUB_SCRIPTS / "extract_arxiv_content.py"),
            "--paper-id", paper_id,
            "--preferred-source", "auto",
            "--include-full-text",
            "--ocr-mode", "never",
            "-o", str(output),
        ],
        timeout=300.0,
    )
    if result.returncode or not output.is_file():
        log(f"抽取失败：exit {result.returncode} {(result.stderr or '')[-200:]}")
        return False
    add = run(
        [
            sys.executable, str(HUB_SCRIPTS / "knowledge.py"),
            "pool-add-paper", "add", "--extraction", str(output), "--pool-root", str(pool_root),
        ],
        timeout=60.0,
    )
    if add.returncode:
        log(f"入池失败：exit {add.returncode} {(add.stderr or '')[-200:]}")
        return False
    log(f"抽取完成并入池：{pool_dir}")
    return True


def ensure_deep_read(paper_id: str, pool_root: Path, cli: str | None, force: bool) -> str:
    """Cache check + delegation to the driver's shared single-paper flow.
    Returns 'pass' | 'needs-review' | 'failed' | 'skipped'."""

    pool_dir = pool_root / f"arxiv-{paper_id}"
    audit_path = pool_dir / "note.json.audit.json"
    if audit_path.is_file() and not force:
        try:
            status = str(json.loads(audit_path.read_text(encoding="utf-8")).get("status") or "")
        except (json.JSONDecodeError, OSError):
            status = ""
        if status in {"pass", "needs-review"}:
            log(f"深读缓存命中：{status}")
            return status
    if not cli:
        log("claude CLI 不存在，跳过深读（按原文对话）")
        return "skipped"
    log("深读 agent 启动（速记骨架 + 审计组装）…")
    outcome = deep_read_paper(
        paper_id, pool_root, cli,
        agent_timeout_s=SKELETON_TIMEOUT_S,
        skeleton_path=pool_dir / "skeleton-latest.json",
    )
    if outcome == "pass":
        log("深读完成：审计通过，已入池")
    elif outcome == "needs-review":
        log("深读完成：needs-review（可用），已入池")
    else:
        log(f"深读审计未过：{outcome}（按原文对话）")
    return outcome


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--kb-root", default=str(Path.home() / "Documents" / "arxiv"))
    parser.add_argument("--force", action="store_true", help="Re-extract / re-deep-read even when pooled.")
    args = parser.parse_args(argv)

    try:
        paper_id = normalize_arxiv_id(args.arxiv_id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    pool_root = pool_root_for(args.kb_root)
    log(f"准备论文 {paper_id}")

    if not ensure_extraction(paper_id, pool_root, args.force):
        return 1
    status = ensure_deep_read(paper_id, pool_root, resolve_cli(), args.force)
    print(
        json.dumps(
            {
                "arxiv_id": paper_id,
                "pool_dir": str(pool_root / f"arxiv-{paper_id}"),
                "deep_read": status,
                "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
            },
            ensure_ascii=False,
        )
    )
    return 0 if status in {"pass", "needs-review"} else 3


if __name__ == "__main__":
    sys.exit(main())
