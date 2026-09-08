#!/usr/bin/env python3
"""Serve the research Wiki locally and expose its safe refresh endpoint."""

from __future__ import annotations

import argparse
import errno
import json
import os
import re
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


# One claude chat turn at a time for the whole server; deliberately separate
# from REFRESH_LOCK so a snapshot refresh during a chat still works.
CHAT_LOCK = threading.Lock()
# The in-flight ChatTurn, guarded by its own tiny lock so /api/chat/stop never
# blocks on the streaming thread.
CHAT_GUARD = threading.Lock()
CURRENT_CHAT: wiki_chat.ChatTurn | None = None


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
    """Stop the in-flight chat turn, if any. Returns True when one was running."""

    with CHAT_GUARD:
        turn = CURRENT_CHAT
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
        **kwargs,
    ):
        self.knowledge_map = knowledge_map
        self.kb_root = kb_root
        self.data_dir = data_dir
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
        if path == "/api/chat/state":
            self._handle_chat_state()
            return
        super().do_GET()

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
        if not self.chat.enabled:
            self._send_json(HTTPStatus.OK, {"enabled": False})
            return
        query = parse_qs(urlparse(self.path).query)
        raw_topic = (query.get("topic") or [""])[0]
        if not raw_topic:
            self._send_json(HTTPStatus.OK, {"enabled": True})
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

    def _handle_chat(self) -> None:
        body = self._chat_precheck()
        if body is None:
            return
        message = (body.get("message") or "").strip()
        if not message:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "消息为空。"})
            return
        try:
            run_dir, topic = self.resolve_topic(body.get("topic_id") or "")
        except ChatBadRequest as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        topic_id = topic.get("id") or body["topic_id"]

        if not CHAT_LOCK.acquire(blocking=False):
            self._send_json(HTTPStatus.CONFLICT, {"error": "已有对话正在进行，请先停止或稍候。"})
            return
        try:
            self._send_sse_headers()
            registry = self.chat_sessions
            resumed = (registry.get(topic_id) or {}).get("session_id")
            prompt = wiki_chat.build_turn_prompt(
                topic=topic, run_dir=run_dir, kb_root=self.kb_root, message=message
            )
            turn, session_was_reset = self._spawn_chat_turn(prompt, resumed)
            if session_was_reset:
                registry.reset(topic_id)
                self._write_sse_event({"type": "session_reset"})
            _set_current_chat(turn)
            registry.append_message(topic_id, "user", message)
            assistant_text: list[str] = []
            try:
                for event in turn.events():
                    if event["type"] == "session":
                        registry.record_session(topic_id, event.get("session_id"), event.get("model"))
                    elif event["type"] == "delta":
                        assistant_text.append(event.get("text") or "")
                    self._write_sse_event(event)
            except (BrokenPipeError, ConnectionResetError):
                turn.stop()  # browser tab closed / navigated away
                return
            if "".join(assistant_text).strip():
                registry.append_message(topic_id, "assistant", "".join(assistant_text))
        finally:
            _set_current_chat(None)
            CHAT_LOCK.release()

    def _spawn_chat_turn(self, prompt: str, session_id: str | None) -> tuple[wiki_chat.ChatTurn, bool]:
        """Spawn a turn; when the session id turns out to be stale (resume
        failure), fall back once to a fresh session. Returns (turn, was_reset):
        ``was_reset`` tells the caller to clear the topic's registry entry and
        announce the reset so the UI drops its local history view."""

        turn = self._new_chat_turn(prompt, session_id)
        turn.start()
        first = turn.peek_event()
        if first is not None and first.get("type") == "error" and first.get("resume_failed"):
            turn.stop()
            turn = self._new_chat_turn(prompt, None)
            turn.start()
            return turn, True
        return turn, False

    def _new_chat_turn(self, prompt: str, session_id: str | None) -> wiki_chat.ChatTurn:
        return self.chat.new_turn(prompt=prompt, cwd=self.kb_root, session_id=session_id)

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

    def _send_sse_headers(self) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")
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
