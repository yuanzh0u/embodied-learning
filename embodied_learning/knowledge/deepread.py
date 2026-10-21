"""Prepare one arXiv paper for wiki paper-chat: ensure pooled + deep-read.

Idempotent single-paper pipeline used by the wiki server's paper-chat entry:

    1. pool check  — pool/arxiv-<id>/extraction.json present?
    2. extraction  — fetch.py extract-content --include-full-text → pool add
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

from embodied_learning.harness.claude import resolve_cli
from embodied_learning.harness.prompt import (
    build_skeleton_prompt,
    pool_root_for,
    read_skeleton_output,
)
from embodied_learning.utils.layout import find_roots

_REPO_ROOT, _SKILLS_ROOT, SCRIPTS_ROOT = find_roots()
HUB_SCRIPTS = _SKILLS_ROOT / "embodied-ai-literature-hub" / "scripts"
# Skill dispatchers live under skills/<name>/scripts/, not the scripts root
# (ADR 0005). SCRIPTS_ROOT/read.py does not exist in either layout.
READ_SCRIPT = _SKILLS_ROOT / "embodied-ai-paper-reader" / "scripts" / "read.py"
from embodied_learning.utils.arxiv_id import normalize_arxiv_id as _normalize_arxiv_id  # noqa: E402
from embodied_learning import locks  # noqa: E402
from embodied_learning.wiki.run.driver import deep_read_paper  # noqa: E402
from embodied_learning.config import SKELETON_TIMEOUT_S



def log(message: str) -> None:
    print(f"[PAPER-CHAT] {message}", flush=True)


def _paper_lock(pool_root: Path, paper_dir_name: str, *, wait: float):
    """Per-paper pool lock (see embodied_learning.locks)."""

    return locks.kb_lock(pool_root, f"pool-paper__{paper_dir_name}", wait=wait)


def normalize_arxiv_id(raw: str) -> str:
    """Shared arXiv-ID grammar; raises with the offending value (see
    embodied_learning.utils.arxiv_id)."""

    return _normalize_arxiv_id(raw, strict=True)


def run_command(command: list[str], *, timeout: float) -> subprocess.CompletedProcess:
    return subprocess.run(
        command, cwd=str(SCRIPTS_ROOT), text=True, capture_output=True, timeout=timeout, check=False
    )


def ensure_extraction(paper_id: str, pool_root: Path, force: bool) -> bool:
    pool_dir = pool_root / f"arxiv-{paper_id}"
    if (pool_dir / "extraction.json").is_file() and not force:
        log(f"pool 命中：{pool_dir}")
        return True
    # Serialize per-paper work: two terminals racing on the same paper would
    # otherwise both fetch and both write pool/arxiv-<id>/extraction.json in
    # place. The waiter re-checks after acquiring (the holder usually already
    # finished the fetch). Network fetch inside the lock is deliberate —
    # duplicating it is the waste we are avoiding. The pool-add child runs
    # OUTSIDE the lock: it takes pool locks in its own process, and re-taking
    # this process's per-paper lock from a child would deadlock.
    with _paper_lock(pool_root, pool_dir.name, wait=600.0):
        if (pool_dir / "extraction.json").is_file() and not force:
            log(f"pool 命中（等待后）：{pool_dir}")
            return True
        log("未入池，开始全文抽取（HTML → markdown）…")
        output = pool_dir / "extraction.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        result = run_command(
            [
                sys.executable, str(HUB_SCRIPTS / "fetch.py"), "extract-content",
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
    add = run_command(
        [
            sys.executable, str(READ_SCRIPT),
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
    outcome, reason = deep_read_paper(
        paper_id, pool_root, cli,
        agent_timeout_s=SKELETON_TIMEOUT_S,
        skeleton_path=pool_dir / "skeleton-latest.json",
    )
    if outcome == "pass":
        log("深读完成：审计通过，已入池")
    elif outcome == "needs-review":
        log("深读完成：needs-review（可用），已入池")
    else:
        log(f"深读审计未过：{reason or outcome}（按原文对话）")
    return outcome


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in the dispatcher."""
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
