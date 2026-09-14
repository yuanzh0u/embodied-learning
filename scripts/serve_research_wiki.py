#!/usr/bin/env python3
"""Serve the research Wiki locally and expose its safe refresh endpoint."""

from __future__ import annotations

import argparse
import datetime as dt
import errno
import json
import os
import re
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_research_wiki import resolve_snapshot_directory  # noqa: E402
from init_run import run_folder_name, slugify_topic  # noqa: E402
from lib import arxiv_reader  # noqa: E402
import wiki_chat  # noqa: E402


# Sibling scripts resolve next to this file, so the installed console command
# (site-packages/wiki_scripts/) and a repo checkout behave identically.
BUILDER = SCRIPT_DIR / "build_research_wiki.py"
GRAPH_BUILDER = SCRIPT_DIR / "visualize_kb_index.py"
# Frontend serving rule: an *editable* install (or a plain repo run) serves the
# repo checkout's wiki/ in place — code edits show up on refresh. A *non-editable*
# install has no repo next to it, so it serves <kb-root>/wiki (the copy beside the
# knowledge base), bootstrapping that copy from the wheel-bundled frontend
# (packaged as wiki_scripts/wiki_assets, mapped from the repo's wiki/ at build
# time) or, failing that, the repo checkout.
DEFAULT_KB_ROOT = Path.home() / "Documents" / "arxiv"
REPO_ROOT = SCRIPT_DIR.parent
REPO_WIKI_ROOT = REPO_ROOT / "wiki"
IS_REPO_CHECKOUT = (REPO_ROOT / "pyproject.toml").is_file()
FRONTEND_ASSETS = SCRIPT_DIR / "wiki_assets"
CATALOG_RELPATH = Path("knowledge") / "literature-review-catalog.md"
REFRESH_LOCK = threading.Lock()


def resolve_pipeline_root() -> Path | None:
    """The skills/ root the agent-driven pipeline reads its SKILL.mds from.
    Order: explicit --pipeline-root → the repo checkout next to the script →
    the conventional clone location → the wheel-bundled tree
    (site-packages/wiki_scripts/skills). None = workflow unavailable.

    The result is static for the process lifetime (PIPELINE_ROOT_OVERRIDE is
    set in main() before any handler runs), so it is cached after the first
    lookup — every state probe would otherwise re-stat the candidates."""

    global _PIPELINE_ROOT_CACHE
    if _PIPELINE_ROOT_CACHE is not _PIPELINE_ROOT_UNSET:
        return _PIPELINE_ROOT_CACHE

    bundled = SCRIPT_DIR / "skills"
    candidates = [REPO_ROOT, Path.home() / "code" / "embodied-learning", bundled]
    if PIPELINE_ROOT_OVERRIDE is not None:
        candidates.insert(0, PIPELINE_ROOT_OVERRIDE)
    for candidate in candidates:
        if (candidate / "skills" / "embodied-ai-literature-review" / "SKILL.md").is_file():
            _PIPELINE_ROOT_CACHE = candidate
            return candidate
        # The bundled copy IS the skills root itself (site-packages layout).
        if candidate == bundled and (bundled / "embodied-ai-literature-review" / "SKILL.md").is_file():
            _PIPELINE_ROOT_CACHE = bundled
            return bundled
    _PIPELINE_ROOT_CACHE = None
    return None


_PIPELINE_ROOT_UNSET = object()
_PIPELINE_ROOT_CACHE: Path | None | object = _PIPELINE_ROOT_UNSET


# Set in main() from --pipeline-root before handler construction.
PIPELINE_ROOT_OVERRIDE: Path | None = None

# Starter catalog for a brand-new knowledge base: routes zero runs, so the
# first refresh reports "nothing publishable" and the wiki serves its
# empty-library state until the first review is settled into evidence/.
STARTER_CATALOG = """---
id: KB-LIT-REVIEWS
title: 文献综述成果目录
type: evidence-routing-index
local-only: true  # 本地知识库：仅路由本地 evidence/ 中实际存在的 run
tags: [literature-review, evidence-routing, paper-reading, provenance]
---

# 文献综述成果目录

本目录连接主题卡与论文级证据，不重复存放论文摘要。每次综述 run 结算进
`evidence/` 后，在这里登记一行，Wiki 刷新时即会发布该话题。

## 成果索引

“规模”依次表示候选池 / 可读全文 / 精读并接纳论文数。

| ID | 综述主题 | 主要知识卡 | 规模 | 审计入口 |
|---|---|---|---:|---|
"""


def ensure_default_kb(kb_root: Path) -> Path:
    """First run with no knowledge base anywhere: create the minimal skeleton
    (knowledge/ + a starter catalog routing zero runs) at the default location
    and say so. Explicit --kb-root never gets auto-created."""

    catalog = kb_root / CATALOG_RELPATH
    catalog.parent.mkdir(parents=True, exist_ok=True)
    if not catalog.is_file():
        catalog.write_text(STARTER_CATALOG, encoding="utf-8")
        (kb_root / "evidence").mkdir(exist_ok=True)
        print(f"已初始化本地知识库：{kb_root}（knowledge/ + evidence/）")
    return kb_root


class ChatBadRequest(ValueError):
    """Malformed chat request (bad topic id, empty message, bad JSON body)."""


# ---- literature-review workflow (STORM-style one-click survey) -----------
# The pipeline itself is agent-driven: the local claude CLI reads the skills'
# SKILL.mds and executes it. The server only launches it, streams its progress,
# and holds the outline checkpoint. Workflow capability additionally requires
# the repo checkout (skills/ tree); wheel-only installs disable it honestly.
WORKFLOW_CHECKPOINT_STAGE = "packet"
WORKFLOW_REVIEW_MODES = {"rapid", "scoping", "systematic"}
WORKFLOW_STYLES = {"all", "scientific-memo", "expert-explainer"}
WORKFLOW_SEARCH_STRATEGIES = {"smart", "fast", "seeds"}
WORKFLOW_MIN_TIMEOUT_S = 3600.0  # pipeline segments outlive the chat default
WORKFLOW_DRIVER_TIMEOUT_S = 900.0  # mechanical stages; idempotent so retry is cheap
PIPELINE_DRIVER = SCRIPT_DIR / "run_review_pipeline.py"
# Chat model: the browser's composer picks per conversation; this is the
# default shown there and used when no explicit model arrives. Empty string
# or --chat-model overrides change it at the CLI level.
DEFAULT_CHAT_MODEL = "glm-5.3-flash"
# Per-conversation locks: a long workflow segment must not block topic chat
# (and vice versa). Keyed by session key (topic-*/ws-*); one claude process
# per key at a time.
CHAT_LOCKS: dict[str, threading.Lock] = {}
CHAT_LOCKS_GUARD = threading.Lock()


def acquire_chat_lock(key: str) -> bool:
    with CHAT_LOCKS_GUARD:
        lock = CHAT_LOCKS.setdefault(key, threading.Lock())
    return lock.acquire(blocking=False)


def release_chat_lock(key: str) -> None:
    with CHAT_LOCKS_GUARD:
        lock = CHAT_LOCKS.get(key)
    if lock is not None:
        lock.release()


# The in-flight ChatTurn, guarded by its own tiny lock so /api/chat/stop never
# blocks on the streaming thread. CURRENT_DRIVER mirrors it for the pre-claude
# pipeline driver subprocess (a kickoff stop kills the driver, not a turn).
CHAT_GUARD = threading.Lock()
CURRENT_CHAT: wiki_chat.ChatTurn | None = None
CURRENT_DRIVER: subprocess.Popen | None = None


def resolve_kb_root(requested: Path | None) -> Path | None:
    """KB root: an explicit --kb-root (must carry a catalog, validated by the
    caller), else ~/Documents/arxiv, else the repo checkout. None = not found."""

    candidates: list[Path] = []
    if requested is not None:
        candidates.append(requested)
    else:
        candidates.append(DEFAULT_KB_ROOT)
        candidates.append(REPO_ROOT)
    for candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if (resolved / CATALOG_RELPATH).is_file():
            return resolved
    return None


def pool_root(kb_root: Path) -> Path:
    """The shared public paper pool next to the knowledge base."""
    return kb_root / "pool"


def resolve_wiki_root(kb_root: Path) -> Path:
    """Pick the wiki/ folder to serve. An editable install (repo checkout)
    serves the repo's own wiki/ so frontend edits show up immediately; a
    non-editable install serves <kb-root>/wiki, bootstrapping a first-run copy
    from the repo checkout's wiki/ when the folder does not exist yet."""

    if IS_REPO_CHECKOUT and (REPO_WIKI_ROOT / "index.html").is_file():
        return REPO_WIKI_ROOT
    kb_wiki = kb_root / "wiki"
    if (kb_wiki / "index.html").is_file():
        return kb_wiki
    bootstrap_wiki_frontend(kb_wiki)
    return kb_wiki


def bootstrap_wiki_frontend(target: Path) -> None:
    """First run against a KB without wiki/: copy the frontend shell from the
    wheel-bundled assets (a non-editable install) or the repo checkout, so the
    server can serve and later refresh data/ in place next to the KB."""

    candidates = [FRONTEND_ASSETS, REPO_WIKI_ROOT]
    source = next((c for c in candidates if (c / "index.html").is_file()), None)
    if source is None:
        raise RuntimeError(
            f"未找到 Wiki 前端资源（{FRONTEND_ASSETS} 或 {REPO_WIKI_ROOT}）。"
            "请重新安装本软件包，或手动复制仓库的 wiki/ 目录到该路径。"
        )
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("data", "__pycache__", "__init__.py"),
    )
    print(f"已初始化 Wiki 前端目录：{target}")


def build_refresh_command(kb_root: Path, data_dir: Path) -> list[str]:
    command = [sys.executable, str(BUILDER), "--output", str(data_dir)]
    if (kb_root / CATALOG_RELPATH).is_file():
        command += ["--kb-root", str(kb_root)]
    return command


def _set_current_chat(turn: wiki_chat.ChatTurn | None) -> None:
    global CURRENT_CHAT
    with CHAT_GUARD:
        CURRENT_CHAT = turn


def stop_current_chat() -> bool:
    """Stop the in-flight chat turn or pipeline driver, if any. Returns True
    when one was running."""

    with CHAT_GUARD:
        turn = CURRENT_CHAT
        driver = CURRENT_DRIVER
    if driver is not None and driver.poll() is None:
        driver.kill()
        return True
    if turn is None:
        return False
    turn.stop()
    return True


class WikiHandler(SimpleHTTPRequestHandler):
    server_version = "ResearchWiki/1.1"

    def __init__(
        self,
        *args,
        knowledge_map: Path | None = None,
        kb_root: Path,
        wiki_root: Path,
        data_dir: Path,
        chat: wiki_chat.ChatConfig | None = None,
        workflow_model: str | None = None,
        workflow_effort: str | None = None,
        **kwargs,
    ):
        self.knowledge_map = knowledge_map
        self.kb_root = kb_root
        self.data_dir = data_dir
        self.workflow_model = workflow_model
        self.workflow_effort = workflow_effort
        self.refresh_command = build_refresh_command(kb_root, data_dir)
        self.chat = chat or wiki_chat.ChatConfig()
        self.chat_sessions = wiki_chat.ChatSessionRegistry(data_dir / "chat-sessions.json")
        super().__init__(*args, directory=str(wiki_root), **kwargs)

    def end_headers(self) -> None:
        if self.path.startswith("/data/"):
            self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        print(f"[Wiki] {format % args}")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/knowledge-map", "/knowledge-map/", "/knowledge-map/index.html"}:
            self._serve_knowledge_map()
            return
        if path.startswith("/api/reader/"):
            self._handle_reader()
            return
        if path == "/api/chat/state":
            self._handle_chat_state()
            return
        if path == "/api/paper/chat/state":
            self._handle_paper_chat_state()
            return
        if path == "/api/workflow/state":
            self._handle_workflow_state()
            return
        super().do_GET()

    def _handle_reader(self) -> None:
        """Inline arXiv paper reader: /api/reader/<arxiv-id> serves the
        paper's (cleaned, cached) HTML rendering. GET only, no params — the
        paper id is the whole request; bad ids get a friendly page."""

        paper_id = arxiv_reader.parse_arxiv_id(urlparse(self.path).path.removeprefix("/api/reader/"))
        if paper_id is None:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "无效的 arXiv ID。"})
            return
        payload = ""
        # Pool first: papers already extracted by any review run carry a
        # cleaned copy in the shared pool — zero network, zero re-parse.
        pooled = pool_root(self.kb_root) / f"arxiv-{paper_id}" / "paper.html"
        if pooled.is_file() and pooled.stat().st_size > 0:
            try:
                payload = pooled.read_text(encoding="utf-8", errors="replace")
            except OSError:
                payload = ""
        if not payload.strip():
            cache_dir = self.kb_root / "work" / "reader-cache"
            result = arxiv_reader.fetch_paper(paper_id, cache_dir)
            payload = result["html"] if result["ok"] else arxiv_reader.unavailable_page(paper_id, result["error"])
        body = payload.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/refresh":
            self._handle_refresh()
            return
        if path == "/api/chat":
            self._handle_chat()
            return
        if path == "/api/chat/stop":
            self._handle_chat_stop()
            return
        if path == "/api/chat/reset":
            self._handle_chat_reset()
            return
        if path == "/api/paper/chat":
            self._handle_paper_chat()
            return
        if path == "/api/paper/chat/reset":
            self._handle_paper_chat_reset()
            return
        if path == "/api/workflow":
            self._handle_workflow()
            return
        if path == "/api/workflow/stop":
            self._handle_workflow_stop()
            return
        if path == "/api/workflow/reset":
            self._handle_workflow_reset()
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def _handle_refresh(self) -> None:
        if not REFRESH_LOCK.acquire(blocking=False):
            self._send_json(HTTPStatus.CONFLICT, {"error": "已有刷新正在进行，请稍候。"})
            return
        try:
            result = subprocess.run(
                self.refresh_command,
                cwd=str(self.kb_root),
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            if result.returncode:
                message = (result.stderr or result.stdout or "刷新脚本执行失败").strip()
                self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": message})
                return
            snapshot_dir = resolve_snapshot_directory(self.data_dir)
            manifest = json.loads((snapshot_dir / "manifest.json").read_text(encoding="utf-8"))
            self._send_json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "topics": len(manifest["topics"]),
                    "generated_at": manifest["generated_at"],
                    "message": result.stdout.strip(),
                },
            )
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
        finally:
            REFRESH_LOCK.release()

    # ---- chat ------------------------------------------------------------

    def _read_json_body(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0 or length > 1_000_000:
            raise ChatBadRequest("请求体为空或过大。")
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ChatBadRequest(f"请求体不是合法 JSON：{exc}") from exc
        if not isinstance(body, dict):
            raise ChatBadRequest("请求体必须是 JSON 对象。")
        return body

    def _chat_precheck(self) -> dict | None:
        """Shared guard for the POST endpoints: 503 when chat is disabled, then
        the parsed JSON body (400 on a malformed one). None = already replied."""

        if not self.chat.enabled:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "聊天服务未启用（未找到 claude 或已用 --no-chat 关闭）。"})
            return None
        try:
            return self._read_json_body()
        except ChatBadRequest as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return None

    def _require_topic_id(self, raw: object) -> str | None:
        """Validate a browser-supplied topic id; 400 and return None if bad."""

        topic_id = raw if isinstance(raw, str) else ""
        if not wiki_chat.TOPIC_ID_RE.match(topic_id):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "话题 ID 无效。"})
            return None
        return topic_id

    def resolve_topic(self, topic_id: str) -> tuple[Path, dict]:
        """Turn a browser-supplied topic id into (run_dir, topic). The topic
        JSON comes from the snapshot this server built, and the run directory
        must live inside the KB root — the browser never supplies paths."""

        if not wiki_chat.TOPIC_ID_RE.match(topic_id or ""):
            raise ChatBadRequest("话题 ID 无效。")
        snapshot_dir = resolve_snapshot_directory(self.data_dir)
        topic_path = snapshot_dir / "topics" / f"{topic_id}.json"
        if not topic_path.is_file():
            raise ChatBadRequest("话题不存在或快照已更新，请刷新页面。")
        try:
            topic = json.loads(topic_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ChatBadRequest(f"话题数据读取失败：{exc}") from exc
        source = topic.get("source_directory")
        if not isinstance(source, str) or not source:
            raise ChatBadRequest("话题缺少运行目录信息。")
        run_dir = Path(source).expanduser().resolve()
        if not run_dir.is_relative_to(self.kb_root):
            raise ChatBadRequest("话题运行目录不在知识库内。")
        if not run_dir.is_dir():
            raise ChatBadRequest("话题运行目录不存在。")
        return run_dir, topic

    def _handle_chat_state(self) -> None:
        # Capability probe: the frontend calls this once at init to decide
        # whether to show the chat triggers, so chat must report "disabled"
        # as a normal state, not an error. Without ?topic= it answers the
        # capability question only; with a topic it also returns history.
        # "workflow" reports the homepage survey entry (needs a resolvable
        # skills/ tree — see resolve_pipeline_root).
        workflow_available = self.workflow_available()
        if not self.chat.enabled:
            self._send_json(HTTPStatus.OK, {"enabled": False, "workflow": False})
            return
        query = parse_qs(urlparse(self.path).query)
        raw_topic = (query.get("topic") or [""])[0]
        if not raw_topic:
            self._send_json(HTTPStatus.OK, {"enabled": True, "workflow": workflow_available})
            return
        topic_id = self._require_topic_id(raw_topic)
        if topic_id is None:
            return
        entry = self.chat_sessions.get(topic_id) or {}
        self._send_json(
            HTTPStatus.OK,
            {
                "enabled": True,
                "topic_id": topic_id,
                "session_id": entry.get("session_id"),
                "messages": entry.get("messages", []),
                "model": entry.get("model"),
                "updated_at": entry.get("updated_at"),
            },
        )

    def _stream_chat_turn(
        self,
        *,
        key: str,
        turn: wiki_chat.ChatTurn,
        registry,
        on_delta=None,
        record_user_message: str | None = None,
    ) -> str:
        """Shared streaming loop for every conversation surface (topic / paper
        chat / workflow): record the user message, forward events (persisting
        session ids and the assistant reply), stop on a closed browser pipe.
        ``on_delta`` lets the workflow extract stage markers; returns the
        full assistant text."""

        _set_current_chat(turn)
        if record_user_message:
            registry.append_message(key, "user", record_user_message)
        assistant_text: list[str] = []
        try:
            for event in turn.events():
                if event["type"] == "session":
                    registry.record_session(key, event.get("session_id"), event.get("model"))
                elif event["type"] == "delta":
                    text = event.get("text") or ""
                    assistant_text.append(text)
                    if on_delta:
                        on_delta(text)
                self._write_sse_event(event)
        except (BrokenPipeError, ConnectionResetError):
            turn.stop()  # browser tab closed / navigated away
        full_text = "".join(assistant_text)
        if full_text.strip():
            registry.append_message(key, "assistant", full_text)
        return full_text

    def _handle_chat(self) -> None:
        body = self._chat_precheck()
        if body is None:
            return
        message = (body.get("message") or "").strip()
        if not message:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "消息为空。"})
            return
        model = self._resolve_request_model(body.get("model"))
        try:
            run_dir, topic = self.resolve_topic(body.get("topic_id") or "")
        except ChatBadRequest as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        topic_id = topic.get("id") or body["topic_id"]

        if not acquire_chat_lock(topic_id):
            self._send_json(HTTPStatus.CONFLICT, {"error": "该话题已有对话正在进行，请先停止或稍候。"})
            return
        try:
            self._send_sse_headers()
            registry = self.chat_sessions
            resumed = (registry.get(topic_id) or {}).get("session_id")
            prompt = wiki_chat.build_turn_prompt(
                topic=topic, run_dir=run_dir, kb_root=self.kb_root, message=message
            )
            turn, session_was_reset = self._spawn_chat_turn(prompt, resumed, model)
            if session_was_reset:
                registry.reset(topic_id)
                self._write_sse_event({"type": "session_reset"})
            self._stream_chat_turn(
                key=topic_id, turn=turn, registry=registry, record_user_message=message
            )
        finally:
            _set_current_chat(None)
            release_chat_lock(topic_id)

    # ---- paper chat: per-arXiv-id conversations over the shared pool -------

    @staticmethod
    def _paper_chat_key(arxiv_id: str) -> str:
        # Registry keys starting with "ws-" are workspaces; anything else
        # lands in the topics namespace. "paper-" prefix keeps ids distinct.
        return f"paper-{arxiv_id}"

    def _handle_paper_chat_state(self) -> None:
        """Capability + history probe for the paper-chat pane. With ?id= it
        reports that paper's pooled/deep-read status and prior messages."""

        if not self.chat.enabled:
            self._send_json(HTTPStatus.OK, {"enabled": False})
            return
        query = parse_qs(urlparse(self.path).query)
        raw_id = (query.get("id") or [""])[0]
        if not raw_id:
            self._send_json(HTTPStatus.OK, {"enabled": True})
            return
        paper_id = arxiv_reader.parse_arxiv_id(raw_id)
        if paper_id is None:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "无效的 arXiv ID。"})
            return
        pool_dir = pool_root(self.kb_root) / f"arxiv-{paper_id}"
        entry = self.chat_sessions.get(self._paper_chat_key(paper_id)) or {}
        self._send_json(
            HTTPStatus.OK,
            {
                "enabled": True,
                "arxiv_id": paper_id,
                "pooled": (pool_dir / "extraction.json").is_file(),
                "deep_read_status": self._pool_deep_read_status(pool_dir),
                "session_id": entry.get("session_id"),
                "messages": entry.get("messages", []),
                "model": entry.get("model"),
                "updated_at": entry.get("updated_at"),
            },
        )

    @staticmethod
    def _pool_deep_read_status(pool_dir: Path) -> str | None:
        audit_path = pool_dir / "note.json.audit.json"
        if not audit_path.is_file():
            return None
        try:
            return str(json.loads(audit_path.read_text(encoding="utf-8")).get("status") or "") or None
        except (OSError, json.JSONDecodeError):
            return None

    def _handle_paper_chat(self) -> None:
        """One conversational turn about a single arXiv paper. On first contact
        the paper is pulled into the shared pool and deep-read (cached on later
        visits); the claude session is keyed by the paper id, so each paper
        keeps its own conversation thread."""

        body = self._chat_precheck()
        if body is None:
            return
        message = (body.get("message") or "").strip()
        if not message:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "消息为空。"})
            return
        paper_id = arxiv_reader.parse_arxiv_id(str(body.get("arxiv_id") or ""))
        if paper_id is None:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "无效的 arXiv ID。"})
            return
        model = self._resolve_request_model(body.get("model"))
        key = self._paper_chat_key(paper_id)

        if not acquire_chat_lock(key):
            self._send_json(HTTPStatus.CONFLICT, {"error": "该论文已有对话正在进行，请先停止或稍候。"})
            return
        try:
            self._send_sse_headers()
            registry = self.chat_sessions

            def paper_stage(stage: str, detail: str) -> None:
                registry.set_workflow_state(key, stage=stage, awaiting_input=False)
                self._write_sse_event({"type": "stage", "stage": stage, "detail": detail})

            pool_dir = pool_root(self.kb_root) / f"arxiv-{paper_id}"
            pooled = (pool_dir / "extraction.json").is_file()
            deep_status = self._pool_deep_read_status(pool_dir)
            if not pooled or deep_status not in {"pass", "needs-review"}:
                # First contact: prepare (extraction + deep read) in code, the
                # user watches real progress instead of a silent wait.
                paper_stage("mining", f"准备论文 {paper_id}（{'入池' if not pooled else '深读'}中）…")
                prepared = self._run_paper_preparation(paper_id)
                if prepared is None:
                    self._write_sse_event(
                        {
                            "type": "topic_error",
                            "message": f"论文 {paper_id} 准备失败（抽取或深读出错），请稍后重试。",
                        }
                    )
                    return
                deep_status, pooled = prepared
                paper_stage(
                    "mining",
                    f"准备完成：{'已入池' if pooled else '入池失败'}，深读 {deep_status or '未完成'}",
                )
            else:
                cached = f"深读 {deep_status}" if deep_status else "已入池"
                paper_stage("mining", f"使用缓存：{cached}")

            resumed = (registry.get(key) or {}).get("session_id")
            prompt = wiki_chat.build_paper_turn_prompt(arxiv_id=paper_id, message=message)
            turn, session_was_reset = self._spawn_turn(self._new_paper_chat_turn, prompt, resumed, model)
            if session_was_reset:
                registry.reset(key)
                self._write_sse_event({"type": "session_reset"})
            self._stream_chat_turn(key=key, turn=turn, registry=registry, record_user_message=message)
        finally:
            _set_current_chat(None)
            release_chat_lock(key)

    def _run_paper_preparation(self, paper_id: str) -> tuple[str | None, bool] | None:
        """Run prepare_paper_chat.py (extraction → pool → deep read), returning
        (deep_read_status, pooled). Returns None on hard failure so the caller
        can surface an error instead of starting a conversation on nothing."""

        command = [
            sys.executable,
            str(SCRIPT_DIR / "prepare_paper_chat.py"),
            "--arxiv-id", paper_id,
            "--kb-root", str(self.kb_root),
        ]
        try:
            process = subprocess.Popen(
                command, cwd=str(self.kb_root), text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            assert process.stdout is not None
            for line in process.stdout:
                detail = line.strip()
                if detail.startswith("[PAPER-CHAT] "):
                    self._write_sse_event(
                        {"type": "stage", "stage": "mining", "detail": detail.removeprefix("[PAPER-CHAT] ")}
                    )
            try:
                returncode = process.wait(timeout=720)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                returncode = -1
        except (OSError, subprocess.SubprocessError):
            return None
        if returncode not in (0, 3):
            return None
        pool_dir = pool_root(self.kb_root) / f"arxiv-{paper_id}"
        pooled = (pool_dir / "extraction.json").is_file()
        return self._pool_deep_read_status(pool_dir), pooled

    def _new_paper_chat_turn(self, prompt: str, session_id: str | None, model: str | None) -> wiki_chat.ChatTurn:
        return self.chat.new_turn(
            prompt=prompt,
            cwd=self.kb_root,
            session_id=session_id,
            system_prompt=wiki_chat.substitute_prompt_roots(
                wiki_chat.PAPER_CHAT_SYSTEM_PROMPT,
                skills_root=self._paper_chat_skills_root(),
                scripts_root=self._paper_chat_scripts_root(),
                pool_root=pool_root(self.kb_root),
            ),
            model=model or DEFAULT_CHAT_MODEL,
        )

    def _paper_chat_skills_root(self) -> Path:
        pipeline_root = resolve_pipeline_root()
        if pipeline_root is None:
            return Path("skills")
        skills_root, _ = wiki_chat.resolve_pipeline_layout(pipeline_root)
        return skills_root

    def _paper_chat_scripts_root(self) -> Path:
        pipeline_root = resolve_pipeline_root()
        if pipeline_root is None:
            return Path("scripts")
        _, scripts_root = wiki_chat.resolve_pipeline_layout(pipeline_root)
        return scripts_root

    def _handle_paper_chat_reset(self) -> None:
        body = self._chat_precheck()
        if body is None:
            return
        paper_id = arxiv_reader.parse_arxiv_id(str((body or {}).get("arxiv_id") or ""))
        if paper_id is None:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "无效的 arXiv ID。"})
            return
        self.chat_sessions.reset(self._paper_chat_key(paper_id))
        self._send_json(HTTPStatus.OK, {"ok": True})

    def _spawn_turn(
        self, new_turn, prompt: str, session_id: str | None, model: str | None = None
    ) -> tuple[wiki_chat.ChatTurn, bool]:
        """Spawn a turn via ``new_turn(prompt, session_id, model)``; when the
        session id turns out to be stale (resume failure), fall back once to a
        fresh session. Returns (turn, was_reset): ``was_reset`` tells the caller
        to clear the registry entry and announce the reset. A None first event
        with a live process is a first-event timeout: the turn is killed so
        events() finishes instead of the handler blocking on a silent stream."""

        turn = new_turn(prompt, session_id, model)
        turn.start()
        first = turn.peek_event()
        if first is not None and first.get("type") == "error" and first.get("resume_failed"):
            turn.stop()
            turn = new_turn(prompt, None, model)
            turn.start()
            return turn, True
        if first is None and turn.is_alive:
            turn.stop()
        return turn, False

    def _spawn_chat_turn(
        self, prompt: str, session_id: str | None, model: str | None = None
    ) -> tuple[wiki_chat.ChatTurn, bool]:
        return self._spawn_turn(self._new_chat_turn, prompt, session_id, model)

    def _resolve_request_model(self, raw: object) -> str | None:
        """Per-conversation model override from the chat composer. Free string
        (the claude CLI decides what names it accepts); capped length."""

        if not isinstance(raw, str):
            return None
        model = raw.strip()
        return model[:80] or None

    def _new_chat_turn(self, prompt: str, session_id: str | None, model: str | None = None) -> wiki_chat.ChatTurn:
        return self.chat.new_turn(
            prompt=prompt,
            cwd=self.kb_root,
            session_id=session_id,
            model=model or DEFAULT_CHAT_MODEL,
        )

    def _handle_chat_stop(self) -> None:
        idle = not stop_current_chat()
        self._send_json(HTTPStatus.OK, {"ok": True, "idle": idle})

    def _handle_chat_reset(self) -> None:
        body = self._chat_precheck()
        if body is None:
            return
        topic_id = self._require_topic_id(body.get("topic_id"))
        if topic_id is None:
            return
        self.chat_sessions.reset(topic_id)
        self._send_json(HTTPStatus.OK, {"ok": True})

    # ---- literature-review workflow ---------------------------------------

    def workflow_available(self) -> bool:
        return self.chat.enabled and resolve_pipeline_root() is not None

    def _validate_workflow_params(self, params: object) -> dict:
        """Normalize the interview card's answers; raise ChatBadRequest."""

        if not isinstance(params, dict):
            raise ChatBadRequest("综述参数缺失或格式无效。")
        topic = str(params.get("topic") or "").strip()
        if not (2 <= len(topic) <= 120):
            raise ChatBadRequest("综述主题需要在 2-120 个字符之间。")
        mode = str(params.get("review_mode") or "rapid")
        if mode not in WORKFLOW_REVIEW_MODES:
            raise ChatBadRequest("综述模式无效（rapid / scoping / systematic）。")
        style = str(params.get("target_style") or "scientific-memo")
        if style not in WORKFLOW_STYLES:
            raise ChatBadRequest("目标风格无效。")
        time_range = self._resolve_time_range(params.get("time_range") or "3y")
        search_strategy = str(params.get("search_strategy") or "smart")
        if search_strategy not in WORKFLOW_SEARCH_STRATEGIES:
            raise ChatBadRequest("检索策略无效（smart / fast / seeds）。")
        seed_raw = str(params.get("seed_arxiv_ids") or "").strip()
        return {
            "topic": topic,
            "review_mode": mode,
            "target_style": style,
            "time_range": time_range,
            "focus": str(params.get("focus") or "").strip()[:500],
            "search_strategy": search_strategy,
            "seed_arxiv_ids": seed_raw[:300],
        }

    def _resolve_time_range(self, raw: object) -> str:
        """Accept a preset name, a ``{"range": "A..B"}`` dict (the interview
        card's custom wire format), or an explicit ``A..B`` string; return the
        canonical ``YYYY-MM-DD..YYYY-MM-DD`` string for the run manifest.

        Presets: 6mo / 3y (default) / 10y / 20y. Legacy names ("recent" =
        6mo, "since2023" ≈ 3y) still map for old clients."""

        today = dt.date.today()
        today_s = today.strftime("%Y-%m-%d")

        def years_back(n: int) -> str:
            return f"{today.replace(year=today.year - n).strftime('%Y-%m-%d')}..{today_s}"

        custom = ""
        if isinstance(raw, dict):
            custom = str(raw.get("range") or "")
            preset = "custom"
        else:
            preset = str(raw or "")
        if preset in ("", "recent", "6mo"):
            start = (today - dt.timedelta(days=183)).strftime("%Y-%m-%d")
            return f"{start}..{today_s}"
        if preset in ("3y", "since2023"):
            return years_back(3)
        if preset == "10y":
            return years_back(10)
        if preset == "20y":
            return years_back(20)
        if preset == "custom":
            match = re.fullmatch(r"\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}", custom)
            if not match:
                raise ChatBadRequest("自定义时间范围格式应为 YYYY-MM-DD..YYYY-MM-DD。")
            return custom
        raise ChatBadRequest("时间范围无效。")

    def _prepare_workflow_run(self, params: dict) -> Path:
        """Create (or find) the in-progress run dir under <kb-root>/work/ via
        init_run.py conventions, so the run dir is known deterministically for
        resume and topic matching. Raises ChatBadRequest on conflict.

        Resume first matches any existing in-progress run with the same topic
        slug regardless of date — a kickoff after midnight must not fork a
        second run dir for a topic already in progress under yesterday's
        date."""

        work_dir = self.kb_root / "work"
        # init_run slug: literature-review-<slug>-<date>; match on the slug part.
        prefix = "literature-review-" + slugify_topic(params["topic"])
        for candidate in sorted(work_dir.glob(f"{prefix}-*")):
            if not candidate.is_dir() or candidate.name == prefix:
                continue
            candidate_manifest = candidate / "run.json"
            if not candidate_manifest.is_file():
                continue
            try:
                manifest = json.loads(candidate_manifest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(manifest, dict) and manifest.get("status") == "in-progress":
                return candidate  # resume-from-disk: same topic, any date
        run_dir = work_dir / run_folder_name(params["topic"], dt.date.today().strftime("%Y%m%d"))
        manifest_path = run_dir / "run.json"
        if manifest_path.is_file():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                manifest = None
            if isinstance(manifest, dict) and manifest.get("status") == "in-progress":
                return run_dir  # resume-from-disk: same topic retried today
            raise ChatBadRequest("同名运行目录已存在且已结束，请换一个主题表述或明天再试。")
        command = [
            sys.executable,
            str(SCRIPT_DIR / "init_run.py"),
            "--topic",
            params["topic"],
            "--review-mode",
            params["review_mode"],
            "--work-dir",
            str(work_dir),
            "--force",
        ]
        if params["time_range"]:
            command += ["--time-range", params["time_range"]]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
        if result.returncode or not manifest_path.is_file():
            detail = (result.stderr or result.stdout or "").strip()
            raise ChatBadRequest(f"初始化运行目录失败：{detail[:300]}")
        return run_dir

    def _snapshot_topic_items(self) -> list[dict]:
        """The published topics of the current snapshot with their
        ``source_directory`` (only present in topics/<id>.json, not in the
        manifest's summary entries)."""

        try:
            snapshot_dir = resolve_snapshot_directory(self.data_dir)
            topics_dir = snapshot_dir / "topics"
            items = []
            for topic_path in sorted(topics_dir.glob("topic-*.json")):
                try:
                    item = json.loads(topic_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                if isinstance(item, dict) and item.get("source_directory"):
                    items.append(item)
            return items
        except (OSError, RuntimeError):
            return []

    def _manifest_source_dirs(self) -> set[str]:
        """Source dirs of every topic in the current snapshot — the baseline
        for the topic_ready fallback match after the settle refresh."""

        return {
            item["source_directory"]
            for item in self._snapshot_topic_items()
            if isinstance(item.get("source_directory"), str)
        }

    def _find_topic_for_run_dir(self, run_dir: Path, before_dirs: set[str], marker_run: str | None) -> dict | None:
        """After the settle refresh, find the published topic the workflow
        produced. The settled run lands in evidence/ under the same folder
        name as the work/ run dir; match that first, then the claude marker's
        own path, then — fallback, when the marker is missing — the single
        evidence topic absent from the pre-run baseline.

        source_directory in topic JSON is repo-relative for runs inside the
        repo and absolute otherwise (builder _relative()), so match on the
        folder name and the resolved path."""

        expected_name = run_dir.name
        marker_name = Path(marker_run.strip("/")).name if marker_run else None
        fresh: list[dict] = []
        for item in self._snapshot_topic_items():
            source = item.get("source_directory")
            if not isinstance(source, str) or not source:
                continue
            source_dir = (self.kb_root / source).resolve() if not Path(source).is_absolute() else Path(source)
            if source_dir.name == expected_name or (marker_name and source_dir.name == marker_name):
                return item
            if source.startswith("evidence/") and source not in before_dirs:
                fresh.append(item)
        return fresh[0] if len(fresh) == 1 else None

    def _handle_workflow_state(self) -> None:
        if not self.chat.enabled:
            self._send_json(HTTPStatus.OK, {"enabled": False, "workflow": False})
            return
        query = parse_qs(urlparse(self.path).query)
        raw_ws = (query.get("ws_id") or [""])[0]
        if not raw_ws:
            self._send_json(HTTPStatus.OK, {"enabled": True, "workflow": self.workflow_available()})
            return
        if not wiki_chat.WS_ID_RE.match(raw_ws):
            self._send_json(HTTPStatus.OK, {"enabled": True, "workflow": self.workflow_available(), "ws_id": None})
            return
        entry = self.chat_sessions.get_workspace(raw_ws) or {}
        workflow = entry.get("workflow") or {}
        self._send_json(
            HTTPStatus.OK,
            {
                "enabled": True,
                "workflow": self.workflow_available(),
                "ws_id": raw_ws,
                "stage": workflow.get("stage"),
                "awaiting_input": bool(workflow.get("awaiting_input")),
                "run_dir": workflow.get("run_dir"),
                "params": workflow.get("params"),
                "topic_id": entry.get("topic_id"),
                "session_id": entry.get("session_id"),
                "messages": entry.get("messages", []),
            },
        )

    def _handle_workflow(self) -> None:
        body = self._chat_precheck()
        if body is None:
            return
        pipeline_root = resolve_pipeline_root()
        if pipeline_root is None:
            self._send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {"error": "综述工作流需要包含 skills/ 的仓库检出（可用 --pipeline-root 指定）。"},
            )
            return
        message = (body.get("message") or "").strip()
        ws_id = body.get("ws_id") if isinstance(body.get("ws_id"), str) else ""
        entry = self.chat_sessions.get_workspace(ws_id) if ws_id else None
        # The model is chosen at kickoff and sticks for the whole workflow
        # (switching models mid-session is incoherent).
        ws_model = self._resolve_request_model(body.get("model")) if entry is None else (entry.get("model") or None)

        if entry is not None:
            # Continuation (or a free question) on an existing workspace.
            workflow = entry.get("workflow") or {}
            awaiting = bool(workflow.get("awaiting_input"))
            settled = workflow.get("stage") == "settle" and entry.get("topic_id")
            run_rel = workflow.get("run_dir") or ""
            run_dir = (self.kb_root / run_rel).resolve() if run_rel else None
            if run_dir is None or not run_dir.is_dir():
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": "工作流的运行目录已丢失，请重置后重试。"})
                return
            if not message:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": "消息为空。"})
                return
            ws_style = str((workflow.get("params") or {}).get("target_style") or "all")
            ws_stage = str(workflow.get("stage") or "")
            if settled:
                # The survey already published; treat the message as ordinary
                # follow-up on the same session, not pipeline continuation.
                prompt = f"综述已完成并发布。用户说：{message}\n如需修改成稿，直接编辑运行目录中的文件。"
            elif message.strip().lower() in {"继续", "continue"}:
                # An explicit 继续 is always a continuation instruction, even
                # when a previous segment died mid-stage (awaiting=False).
                prompt = wiki_chat.build_continuation_prompt(feedback="", target_style=ws_style, stage=ws_stage)
            else:
                prompt = wiki_chat.build_continuation_prompt(feedback=message, target_style=ws_style, stage=ws_stage)
        else:
            # Kickoff: validate interview answers and prepare the run dir.
            try:
                params = self._validate_workflow_params(body.get("params"))
            except ChatBadRequest as exc:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                return
            try:
                run_dir = self._prepare_workflow_run(params)
            except ChatBadRequest as exc:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                return
            except (OSError, subprocess.SubprocessError) as exc:
                self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"初始化运行目录失败：{exc}"})
                return
            ws_id = f"ws-{secrets.token_hex(4)}"
            prompt = wiki_chat.build_workflow_prompt(
                params=params,
                run_dir=run_dir,
                kb_root=self.kb_root,
                pipeline_root=pipeline_root,
            )
            self.chat_sessions.record_session(ws_id, None, ws_model)
            self.chat_sessions.set_workflow_state(
                ws_id,
                stage="init",
                awaiting_input=False,
                run_dir=run_dir.relative_to(self.kb_root).as_posix(),
                params=params,
            )
            self.chat_sessions.append_message(ws_id, "user", params["topic"])

        before_dirs = self._manifest_source_dirs() if entry is not None else set()
        if not acquire_chat_lock(ws_id):
            self._send_json(HTTPStatus.CONFLICT, {"error": "该工作流已有阶段正在执行，请先停止或稍候。"})
            return
        try:
            self._send_sse_headers(workflow_id=ws_id)
            registry = self.chat_sessions
            if entry is None:
                # Kickoff: run the mechanical stages in code first. claude only
                # starts when the driver completed; a failed driver leaves the
                # run in-progress so a retry resumes idempotently.
                if not self._run_pipeline_driver(ws_id, params, run_dir, registry):
                    return
            self._write_sse_event({"type": "status", "stage": "starting", "detail": "正在启动 claude 会话"})
            resumed = (entry or {}).get("session_id")
            turn, session_was_reset = self._spawn_workflow_turn(prompt, resumed, ws_model)
            if session_was_reset:
                registry.record_session(ws_id, None)
                self._write_sse_event({"type": "session_reset"})
            emitted_stages: set[str] = set()

            def on_delta(text: str) -> None:
                for stage, detail in wiki_chat.extract_stage_markers(text):
                    if stage not in emitted_stages:
                        emitted_stages.add(stage)
                        registry.set_workflow_state(ws_id, stage=stage, awaiting_input=False)
                        self._write_sse_event({"type": "stage", "stage": stage, "detail": detail})

            full_text = self._stream_chat_turn(
                key=ws_id, turn=turn, registry=registry, on_delta=on_delta,
                record_user_message=message if entry is not None else None,
            )

            marker_run = wiki_chat.extract_topic_marker(full_text)
            if marker_run:
                # Settle finished: publish and hand the topic back.
                registry.set_workflow_state(ws_id, stage="settle", awaiting_input=False)
                self._write_sse_event({"type": "stage", "stage": "settle", "detail": "已落盘"})
                try:
                    refresh_snapshot(self.kb_root, self.data_dir)
                except (EmptyCorpusError, RuntimeError) as exc:
                    self._write_sse_event({"type": "topic_error", "message": f"快照刷新失败：{exc}"})
                    return
                topic_item = self._find_topic_for_run_dir(run_dir, before_dirs, marker_run)
                if topic_item:
                    registry.link_topic(ws_id, topic_item["id"])
                    self._write_sse_event(
                        {
                            "type": "topic_ready",
                            "topic_id": topic_item["id"],
                            "title": topic_item.get("title", ""),
                        }
                    )
                else:
                    self._write_sse_event(
                        {"type": "topic_error", "message": "综述已落盘，但快照中尚未找到新话题；请稍后手动刷新。"}
                    )
            else:
                # Pipeline reached the outline checkpoint (or was interrupted):
                # park the workspace and wait for the user's 继续 / feedback.
                current_stage = (self.chat_sessions.get_workspace(ws_id) or {}).get("workflow", {}).get("stage")
                stopped = not turn.stop_requested
                if stopped:
                    registry.set_workflow_state(
                        ws_id, stage=current_stage or WORKFLOW_CHECKPOINT_STAGE, awaiting_input=True
                    )
                    self._write_sse_event(
                        {"type": "awaiting_input", "stage": current_stage or WORKFLOW_CHECKPOINT_STAGE}
                    )
                elif not full_text.strip():
                    # Segment produced nothing and wasn't user-stopped (claude
                    # died silently / first-event timeout). Say so — a silent
                    # empty stream is what looked like "继续没有反应".
                    self._write_sse_event(
                        {
                            "type": "topic_error",
                            "message": "本段没有产生任何输出（claude 可能无响应或会话已失效）。"
                            "请点击 ⟳ 新对话后重新发起，或稍后重试。",
                        }
                    )
        finally:
            _set_current_chat(None)
            release_chat_lock(ws_id)

    def _start_pipeline_driver(self, params: dict, run_dir: Path) -> subprocess.Popen:
        """Launch the mechanical-stage driver subprocess. Split from the
        streaming loop so tests can patch it with a fake Popen."""

        # Prefer the repo checkout's driver: the driver derives the pipeline
        # script paths from its own __file__, so a site-packages copy would
        # point at a nonexistent skills/ tree. (Workflow requires a repo
        # checkout anyway.)
        pipeline_root = resolve_pipeline_root()
        driver = PIPELINE_DRIVER
        if pipeline_root is not None and pipeline_root.name != "skills":
            repo_driver = pipeline_root / "scripts" / "run_review_pipeline.py"
            if repo_driver.is_file():
                driver = repo_driver
        command = [
            sys.executable,
            str(driver),
            "--run-dir", str(run_dir),
            "--topic", str(params.get("topic") or ""),
            "--review-mode", str(params.get("review_mode") or "rapid"),
            "--time-range", str(params.get("time_range") or ""),
            "--kb-root", str(self.kb_root),
            "--search-strategy", str(params.get("search_strategy") or "smart"),
        ]
        focus = str(params.get("focus") or "")
        if focus:
            command += ["--focus", focus]
        seed_ids = str(params.get("seed_arxiv_ids") or "")
        if seed_ids:
            command += ["--seed-arxiv-ids", seed_ids]
        return subprocess.Popen(
            command,
            cwd=str(self.kb_root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _run_pipeline_driver(
        self, ws_id: str, params: dict, run_dir: Path, registry
    ) -> bool:
        """Run the mechanical pipeline stages before claude starts, forwarding
        each [DRIVER-STAGE:*] line as a timeline event. Returns True when the
        driver completed; on failure emits an SSE error and returns False (the
        run dir stays in-progress, so a retry resumes idempotently)."""

        driver = self._start_pipeline_driver(params, run_dir)
        global CURRENT_DRIVER
        with CHAT_GUARD:
            CURRENT_DRIVER = driver
        try:
            self._write_sse_event(
                {"type": "status", "stage": "driver", "detail": "正在运行固定流程（检索/抽取/深读）"}
            )
            assert driver.stdout is not None
            for line in driver.stdout:
                mapped = wiki_chat.extract_driver_stage(line)
                if mapped:
                    stage, detail = mapped
                    registry.set_workflow_state(ws_id, stage=stage, awaiting_input=False)
                    self._write_sse_event({"type": "stage", "stage": stage, "detail": detail})
                    continue
                detail = wiki_chat.extract_driver_detail(line)
                if detail:
                    # Free-form progress lines (per-paper reads, assembly
                    # results) land in the dialog so the user sees movement.
                    self._write_sse_event({"type": "stage", "stage": "mining", "detail": detail})
            try:
                returncode = driver.wait(timeout=WORKFLOW_DRIVER_TIMEOUT_S)
            except subprocess.TimeoutExpired:
                driver.kill()
                driver.wait()
                returncode = -1
        finally:
            with CHAT_GUARD:
                CURRENT_DRIVER = None
        if returncode != 0:
            stderr_tail = ""
            if driver.stderr is not None:
                stderr_tail = (driver.stderr.read() or "")[-300:]
            self._write_sse_event(
                {
                    "type": "topic_error",
                    "message": f"固定流程执行失败（exit {returncode}），可重试续跑：{stderr_tail}",
                }
            )
            return False
        return True

    def _spawn_workflow_turn(
        self, prompt: str, session_id: str | None, model: str | None = None
    ) -> tuple[wiki_chat.ChatTurn, bool]:
        return self._spawn_turn(self._new_workflow_turn, prompt, session_id, model)

    def _new_workflow_turn(self, prompt: str, session_id: str | None, model: str | None = None) -> wiki_chat.ChatTurn:
        # STORM-style tiering: the workflow session gets the (usually lighter)
        # workflow model for its mechanical loop, and its system prompt tells
        # subagents to use fast models too. The main thread's deep-reading
        # synthesis and final prose still happen inside this session. The
        # browser may pick the model per conversation (default glm-5.3-flash);
        # --workflow-model keeps the highest precedence for CLI-driven setups.
        pipeline_root = resolve_pipeline_root()
        system_prompt = wiki_chat.WORKFLOW_SYSTEM_PROMPT
        if pipeline_root is not None:
            skills_root, scripts_root = wiki_chat.resolve_pipeline_layout(pipeline_root)
            system_prompt = wiki_chat.substitute_prompt_roots(
                system_prompt,
                skills_root=skills_root,
                scripts_root=scripts_root,
                pool_root=pool_root(self.kb_root),
            )
        return self.chat.new_turn(
            prompt=prompt,
            cwd=self.kb_root,
            session_id=session_id,
            system_prompt=system_prompt,
            timeout_s=max(self.chat.timeout_s, WORKFLOW_MIN_TIMEOUT_S),
            model=self.workflow_model or model or DEFAULT_CHAT_MODEL,
            effort=self.workflow_effort,
        )

    def _handle_workflow_stop(self) -> None:
        idle = not stop_current_chat()
        self._send_json(HTTPStatus.OK, {"ok": True, "idle": idle})

    def _handle_workflow_reset(self) -> None:
        body = self._chat_precheck()
        if body is None:
            return
        raw = body.get("ws_id")
        ws_id = raw if isinstance(raw, str) else ""
        if not wiki_chat.WS_ID_RE.match(ws_id):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "工作流 ID 无效。"})
            return
        self.chat_sessions.reset(ws_id)
        self._send_json(HTTPStatus.OK, {"ok": True})

    def _send_sse_headers(self, workflow_id: str | None = None) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")
        if workflow_id:
            self.send_header("X-Workflow-Id", workflow_id)
        self.end_headers()
        self.close_connection = True

    def _write_sse_event(self, event: dict) -> None:
        payload = json.dumps(event, ensure_ascii=False)
        self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
        self.wfile.flush()

    def _serve_knowledge_map(self) -> None:
        if not self.knowledge_map or not self.knowledge_map.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "知识图谱尚未生成")
            return
        payload = self.knowledge_map.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_json(self, status: HTTPStatus, value: object) -> None:
        payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class EmptyCorpusError(RuntimeError):
    """The knowledge base has no publishable topics yet (first-run shape)."""


def refresh_snapshot(kb_root: Path, data_dir: Path) -> None:
    """Rebuild the snapshot. Raises EmptyCorpusError for the "nothing
    publishable yet" builder exit (kept distinct from real failures)."""

    result = subprocess.run(
        build_refresh_command(kb_root, data_dir),
        cwd=str(kb_root),
        text=True,
        check=False,
    )
    if result.returncode == 3:
        raise EmptyCorpusError("没有发现同时包含三种成稿的完整话题。")
    if result.returncode:
        raise RuntimeError("初始成果快照构建失败。")


def build_knowledge_map(output: Path, kb_root: Path) -> None:
    command = [sys.executable, str(GRAPH_BUILDER), "--no-open", "--output", str(output)]
    if (kb_root / "knowledge" / "index.md").is_file():
        command += ["--root", str(kb_root)]
    result = subprocess.run(
        command,
        cwd=str(kb_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        print("知识图谱本地预览生成失败，Wiki 阅读功能仍可正常使用。", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="在本地打开空间智能研究 Wiki")
    parser.add_argument("--port", type=int, default=8018, help="本地端口，默认 8018")
    parser.add_argument("--open", action="store_true", help="启动后自动打开浏览器")
    parser.add_argument("--no-refresh", action="store_true", help="启动时不重新扫描成果")
    parser.add_argument(
        "--close",
        action="store_true",
        help="关闭已在运行的 Wiki 实例（按端口找到监听进程并优雅停止）后退出",
    )
    parser.add_argument(
        "--kb-root",
        type=Path,
        default=None,
        help=f"本地知识库根目录（含 knowledge/ 与 evidence/），默认优先 {DEFAULT_KB_ROOT}",
    )
    chat = parser.add_argument_group("研究助手对话（本地 claude CLI）")
    chat.add_argument(
        "--chat-cli",
        default=None,
        help="claude 可执行文件路径，默认从 PATH 查找（回退 /usr/local/bin/claude）",
    )
    chat.add_argument("--chat-model", default=None, help="对话使用的模型，默认跟随 claude 配置")
    chat.add_argument(
        "--chat-permission-mode",
        default=wiki_chat.DEFAULT_PERMISSION_MODE,
        choices=["bypassPermissions", "acceptEdits", "plan", "default"],
        help=f"对话的权限模式，默认 {wiki_chat.DEFAULT_PERMISSION_MODE}",
    )
    chat.add_argument(
        "--chat-allowed-tools",
        default=None,
        help="限制对话可用的工具（传给 claude --allowedTools），默认不限制",
    )
    chat.add_argument(
        "--chat-timeout-s",
        type=float,
        default=wiki_chat.DEFAULT_CHAT_TIMEOUT_S,
        help="单轮对话超时秒数，默认 900",
    )
    chat.add_argument("--no-chat", action="store_true", help="禁用研究助手对话功能")
    wf = parser.add_argument_group("综述工作流（STORM 式加速）")
    wf.add_argument(
        "--pipeline-root",
        type=Path,
        default=None,
        help="包含 skills/ 的仓库根目录（工作流读取 SKILL.md 用）；默认自动探测脚本旁的仓库检出",
    )
    wf.add_argument(
        "--workflow-model",
        default=None,
        help="工作流主线程使用的模型（显式指定时优先于页面选择）；默认跟随页面采访选择或 --chat-model",
    )
    wf.add_argument(
        "--workflow-effort",
        default=None,
        choices=["low", "medium", "high"],
        help="工作流推理力度（低档更快）；默认跟随 claude 配置",
    )
    return parser.parse_args()


def find_listener_pid(port: int) -> int | None:
    """Return the pid of the process listening on 127.0.0.1:<port>, or None.
    Used by --close; on this machine that can only be another Wiki instance."""

    try:
        output = subprocess.run(
            ["ss", "-tlnp", "-o", "sport", "=", f":{port}"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        ).stdout
    except (OSError, subprocess.TimeoutExpired):
        return None
    for line in output.splitlines():
        if "127.0.0.1" not in line and "::1" not in line:
            continue
        match = re.search(r"pid=(\d+)", line)
        if match:
            return int(match.group(1))
    return None


def close_running_instance(port: int) -> int:
    """--close: stop an already-running Wiki on this port. SIGTERM lets it run
    its finally block (stopping any in-flight claude chat) before exiting."""

    pid = find_listener_pid(port)
    if pid is None:
        print(f"端口 {port} 上没有正在运行的 Wiki 实例。")
        return 0
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError as exc:
        print(f"无法停止进程 {pid}：{exc}", file=sys.stderr)
        return 1
    for _ in range(50):  # up to 5 s for a graceful exit
        if not Path(f"/proc/{pid}").exists():
            print(f"已关闭 Wiki 实例（pid {pid}，端口 {port}）。")
            return 0
        time.sleep(0.1)
    print(f"实例（pid {pid}）未在 5 秒内退出，已发送强制终止。")
    try:
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass
    return 0


def main() -> int:
    args = parse_args()
    if args.close:
        return close_running_instance(args.port)
    if args.pipeline_root is not None:
        global PIPELINE_ROOT_OVERRIDE
        PIPELINE_ROOT_OVERRIDE = args.pipeline_root.expanduser().resolve()
    if args.kb_root is not None:
        # An explicit --kb-root is authoritative: never fall back to defaults.
        kb_root = args.kb_root.expanduser().resolve()
        if not (kb_root / CATALOG_RELPATH).is_file():
            print(
                f"--kb-root 指定的目录缺少 {CATALOG_RELPATH}：{kb_root}",
                file=sys.stderr,
            )
            return 1
    else:
        # No explicit --kb-root and the default location has no catalog:
        # a brand-new user gets a skeleton knowledge base created in place.
        kb_root = resolve_kb_root(None)
        if kb_root is None:
            kb_root = ensure_default_kb(DEFAULT_KB_ROOT)
    if kb_root is None:
        print(
            f"未找到本地知识库（默认查找 {DEFAULT_KB_ROOT}）。"
            "请用 --kb-root 指定包含 knowledge/literature-review-catalog.md 的目录。",
            file=sys.stderr,
        )
        return 1
    wiki_root = resolve_wiki_root(kb_root)
    data_dir = wiki_root / "data"
    if not args.no_refresh:
        try:
            refresh_snapshot(kb_root, data_dir)
        except EmptyCorpusError as exc:
            # A first-run KB has nothing publishable yet; that must not block
            # serving — the frontend shows its empty-library state.
            print(f"{exc}\nWiki 将以空状态启动；完成第一次综述后重新启动即可。", file=sys.stderr)
        except RuntimeError as exc:
            # A real build failure keeps the last valid snapshot serving
            # (atomic publish never replaces a good snapshot with a bad one).
            print(f"{exc}", file=sys.stderr)

    chat: wiki_chat.ChatConfig | None = None
    if not args.no_chat:
        try:
            chat = wiki_chat.ChatConfig(
                cli=wiki_chat.resolve_cli(args.chat_cli),
                model=args.chat_model,
                permission_mode=args.chat_permission_mode,
                allowed_tools=args.chat_allowed_tools,
                timeout_s=args.chat_timeout_s,
            )
        except wiki_chat.ChatUnavailableError as exc:
            print(f"研究助手对话未启用：{exc}", file=sys.stderr)

    with tempfile.TemporaryDirectory(prefix="research-wiki-map-") as temp_dir:
        knowledge_map = Path(temp_dir) / "index.html"
        build_knowledge_map(knowledge_map, kb_root)
        handler = partial(
            WikiHandler,
            knowledge_map=knowledge_map,
            kb_root=kb_root,
            wiki_root=wiki_root,
            data_dir=data_dir,
            chat=chat,
            workflow_model=args.workflow_model,
            workflow_effort=args.workflow_effort,
        )
        url = f"http://127.0.0.1:{args.port}/"
        try:
            server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
        except OSError as exc:
            if exc.errno != errno.EADDRINUSE:
                raise
            print(f"已有实例正在运行：{url}")
            if args.open:
                threading.Timer(0.45, lambda: webbrowser.open(url)).start()
            return 0
        print(f"空间智能研究 Wiki 已准备好：{url}")
        if chat is not None and chat.enabled:
            model_label = args.chat_model or "默认模型"
            print(f"研究助手对话已启用（{args.chat_permission_mode} / {model_label}）。")
        print("保持此窗口打开即可阅读；按 Control-C 关闭。")
        if args.open:
            threading.Timer(0.45, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nWiki 已关闭。")
        finally:
            stop_current_chat()  # don't orphan a running claude child
            server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
