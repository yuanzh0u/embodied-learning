#!/usr/bin/env python3
"""Chat backend for the research Wiki: bridge a browser chat box to the local
``claude`` CLI (Claude Code) with ``--print --output-format stream-json``.

The design mirrors lark-coding-agent-bridge's Claude adapter: the prompt goes
through stdin (never argv), stdout is parsed as NDJSON events, and a stop is
SIGTERM followed by SIGKILL after a grace window. One chat session id is bound
to each wiki topic and persisted in ``<data_dir>/chat-sessions.json`` so
conversations survive server restarts and are resumed with ``--resume``.
"""

from __future__ import annotations

import json
import os
import queue
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.jsonio import atomic_write_json  # noqa: E402

DEFAULT_PERMISSION_MODE = "bypassPermissions"
DEFAULT_CHAT_TIMEOUT_S = 900
STOP_GRACE_S = 5.0
MAX_HISTORY_MESSAGES = 40
MAX_PROMPT_CONTEXT_FILES = 40
# When ``claude`` is not on PATH (e.g. launched from a desktop launcher), the
# standard install location is the fallback.
FALLBACK_CLI = "/usr/local/bin/claude"

CHAT_SYSTEM_PROMPT = (
    "你是「空间智能研究 Wiki」的研究助手，工作目录即本地知识库根目录。"
    "evidence/ 下每个 literature-review-* 文件夹是一次研究运行：含三种成稿"
    "（scientific-memo_keyan.md、zhihu-explainer_zhihu.md、xiaohongshu-post_xiaohongshu.md）、"
    "evidence-appendix.md 与 run.json；pool/ 存放已抽取的论文全文 markdown；knowledge/ 是主题卡片。"
    "回答要基于证据：先读相关文件再下结论，引用时给出文件相对路径。"
    "用户可能请你撰写综述草稿：用 Write 把新文件写进当前话题的运行目录，文件名以 survey- 开头，"
    "不要覆盖已有成稿。用中文回答，先给中心判断，再给证据与反例。"
)

TOPIC_ID_RE = re.compile(r"^topic-[0-9a-f]{6,16}$")

# Nested-claude guard variables: the wiki server may itself run inside a Claude
# Code session, and these would make the spawned claude refuse or misbehave.
_STRIPRED_ENV_KEYS = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT")


class ChatConfig:
    """Chat settings resolved once at startup and passed to the handler as one
    object. ``cli=None`` means chat is disabled (CLI missing or --no-chat)."""

    def __init__(
        self,
        *,
        cli: str | None = None,
        model: str | None = None,
        permission_mode: str = DEFAULT_PERMISSION_MODE,
        allowed_tools: str | None = None,
        timeout_s: float = DEFAULT_CHAT_TIMEOUT_S,
    ):
        self.cli = cli
        self.model = model
        self.permission_mode = permission_mode
        self.allowed_tools = allowed_tools
        self.timeout_s = timeout_s

    @property
    def enabled(self) -> bool:
        return self.cli is not None

    def new_turn(self, *, prompt: str, cwd: Path, session_id: str | None = None) -> "ChatTurn":
        assert self.cli is not None, "new_turn() on a disabled ChatConfig"
        return ChatTurn(
            cli=self.cli,
            prompt=prompt,
            cwd=cwd,
            session_id=session_id,
            model=self.model,
            permission_mode=self.permission_mode,
            allowed_tools=self.allowed_tools,
            timeout_s=self.timeout_s,
        )


class ChatUnavailableError(RuntimeError):
    """Raised when no usable claude binary can be located."""


def resolve_cli(cli: str | None = None) -> str:
    """Return a usable claude binary path: explicit arg, then PATH, then the
    standard install location. Raises ChatUnavailableError when none exists.

    ``shutil.which`` already resolves absolute/relative paths (executable file
    or None), so one lookup covers both bare names and explicit paths."""

    candidates = [cli] if cli else []
    candidates += ["claude", FALLBACK_CLI]
    for candidate in candidates:
        found = shutil.which(str(Path(candidate).expanduser()))
        if found:
            return found
    raise ChatUnavailableError(
        f"未找到 claude 命令（已尝试 PATH 与 {FALLBACK_CLI}）。请安装 Claude Code 或用 --chat-cli 指定路径。"
    )


def build_claude_command(
    *,
    cli: str,
    session_id: str | None = None,
    model: str | None = None,
    permission_mode: str = DEFAULT_PERMISSION_MODE,
    allowed_tools: str | None = None,
) -> list[str]:
    """Assemble the one-shot claude invocation. The user prompt is NEVER part
    of argv — it is written to stdin by ChatTurn (shell/quoting safety)."""

    argv = [
        cli,
        "-p",
        "--output-format",
        "stream-json",
        "--verbose",
        "--permission-mode",
        permission_mode,
        "--append-system-prompt",
        CHAT_SYSTEM_PROMPT,
    ]
    if session_id:
        argv += ["--resume", session_id]
    if model:
        argv += ["--model", model]
    if allowed_tools:
        argv += ["--allowedTools", allowed_tools]
    return argv


def parse_stream_line(line: str) -> list[dict]:
    """Translate one stream-json line into 0..n frontend chat events."""

    stripped = line.strip()
    if not stripped:
        return []
    try:
        raw = json.loads(stripped)
    except json.JSONDecodeError:
        return []
    if not isinstance(raw, dict):
        return []

    kind = raw.get("type")
    if kind == "system" and raw.get("subtype") == "init":
        return [
            {
                "type": "session",
                "session_id": raw.get("session_id"),
                "model": raw.get("model"),
            }
        ]

    if kind == "assistant":
        events: list[dict] = []
        for block in (raw.get("message") or {}).get("content") or []:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text" and block.get("text"):
                events.append({"type": "delta", "text": block["text"]})
            elif block_type == "thinking":
                events.append({"type": "status", "stage": "thinking"})
            elif block_type == "tool_use" and block.get("name"):
                events.append(
                    {
                        "type": "status",
                        "stage": "tool",
                        "tool": block["name"],
                        "detail": _tool_detail(block),
                    }
                )
        return events

    if kind == "result":
        return [
            {
                "type": "done",
                "session_id": raw.get("session_id"),
                "is_error": raw.get("is_error") is True,
                "result_text": raw.get("result"),
                "cost_usd": raw.get("total_cost_usd"),
                "num_turns": raw.get("num_turns"),
            }
        ]

    return []


def _tool_detail(block: dict) -> str:
    """Short human-readable summary of a tool call input (file path etc.)."""

    payload = block.get("input")
    if not isinstance(payload, dict):
        return ""
    for key in ("file_path", "notebook_path", "path", "pattern", "command", "url", "query"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value[:120]
    return ""


def is_resume_failure(stderr_text: str) -> bool:
    """Best-effort detection of a stale ``--resume`` session id."""

    lowered = stderr_text.lower()
    return (
        "no conversation found" in lowered
        or "session not found" in lowered
        or "no such session" in lowered
    )


class ChatTurn:
    """One claude chat turn: a spawned ``claude -p`` process bridged to a
    thread-safe event queue so the HTTP handler can stream events while a
    second request (stop) can terminate the process concurrently."""

    def __init__(
        self,
        *,
        cli: str,
        prompt: str,
        cwd: Path,
        session_id: str | None = None,
        model: str | None = None,
        permission_mode: str = DEFAULT_PERMISSION_MODE,
        allowed_tools: str | None = None,
        timeout_s: float = DEFAULT_CHAT_TIMEOUT_S,
    ):
        self.cli = cli
        self.prompt = prompt
        self.cwd = Path(cwd)
        self.session_id = session_id
        self.model = model
        self.permission_mode = permission_mode
        self.allowed_tools = allowed_tools
        self.timeout_s = timeout_s
        self.stop_requested = False
        self._queue: queue.Queue = queue.Queue()
        self._process: subprocess.Popen | None = None
        self._stderr_tail: list[str] = []
        self._timer: threading.Timer | None = None
        self._timed_out = False
        self._peeked: dict | None = None
        self._early_exit_seen = False

    # -- lifecycle ---------------------------------------------------------

    def start(self) -> None:
        command = build_claude_command(
            cli=self.cli,
            session_id=self.session_id,
            model=self.model,
            permission_mode=self.permission_mode,
            allowed_tools=self.allowed_tools,
        )
        env = dict(os.environ)
        for key in _STRIPRED_ENV_KEYS:
            env.pop(key, None)
        try:
            self._process = subprocess.Popen(
                command,
                cwd=str(self.cwd),
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
        except OSError as exc:
            resume_failed = is_resume_failure(str(exc))
            self._queue.put(
                ("error", {"type": "error", "message": f"无法启动 claude：{exc}", "resume_failed": resume_failed})
            )
            self._queue.put(("exit", None))
            return
        # Prompt travels through stdin; close immediately so claude sees EOF.
        try:
            assert self._process.stdin is not None
            self._process.stdin.write(self.prompt)
            self._process.stdin.close()
        except OSError:
            pass  # the stderr/stdout readers will surface the failure
        threading.Thread(target=self._read_stdout, daemon=True).start()
        threading.Thread(target=self._read_stderr, daemon=True).start()
        if self.timeout_s and self.timeout_s > 0:
            self._timer = threading.Timer(self.timeout_s, self._on_timeout)
            self._timer.daemon = True
            self._timer.start()

    def _read_stdout(self) -> None:
        assert self._process is not None and self._process.stdout is not None
        try:
            for line in self._process.stdout:
                for event in parse_stream_line(line):
                    self._queue.put(("event", event))
        except (OSError, ValueError):
            pass
        finally:
            code = self._process.poll() if self._process else None
            self._queue.put(("exit", code))
        if self._timer:
            self._timer.cancel()

    def _read_stderr(self) -> None:
        assert self._process is not None and self._process.stderr is not None
        try:
            for line in self._process.stderr:
                text = line.strip()
                if text:
                    self._stderr_tail.append(text)
                    del self._stderr_tail[:-20]
        except (OSError, ValueError):
            pass

    def _on_timeout(self) -> None:
        self._timed_out = True
        self.stop()

    # -- consumption -------------------------------------------------------

    def _next_item(self):
        item = self._queue.get()
        if item[0] == "exit":
            self._early_exit_seen = True
        return item

    def peek_event(self) -> dict | None:
        """Block for the first queue item and return it if it is an event.
        Used by the caller to detect a resume failure before streaming starts;
        the item stays queued for events() (or is remembered if it was the
        exit marker)."""

        if self._early_exit_seen:
            return None
        kind, payload = self._next_item()
        if kind == "event":
            self._peeked = payload
            return payload
        if kind == "error":
            self._peeked = payload
            return payload
        return None  # exit marker consumed; events() will finish immediately

    def events(self):
        """Yield chat events until the process exits; errors are yielded as
        ``{"type": "error", ...}`` dicts, never raised."""

        if self._peeked is not None:
            yield self._peeked
            self._peeked = None
        if self._early_exit_seen:
            return
        while True:
            kind, payload = self._queue.get()
            if kind == "event":
                yield payload
            elif kind == "error":
                yield payload
            elif kind == "exit":
                exit_code = payload
                stderr_text = "\n".join(self._stderr_tail)
                if self._timed_out:
                    yield {"type": "error", "message": f"对话超时（{int(self.timeout_s)} 秒），已中断。"}
                elif self.stop_requested:
                    yield {"type": "done", "session_id": None, "stopped": True}
                elif exit_code not in (0, None):
                    resume_failed = is_resume_failure(stderr_text)
                    detail = stderr_text[-500:] if stderr_text else f"退出码 {exit_code}"
                    yield {
                        "type": "error",
                        "message": f"claude 执行失败：{detail}",
                        "resume_failed": resume_failed,
                    }
                return

    def stop(self) -> None:
        """SIGTERM, then SIGKILL after a grace window. Safe to call from any
        thread and on an already-exited process."""

        self.stop_requested = True
        process = self._process
        if process is None or process.poll() is not None:
            return
        try:
            process.send_signal(signal.SIGTERM)
        except OSError:
            return

        def _kill_after_grace() -> None:
            if process.poll() is None:
                try:
                    process.kill()
                except OSError:
                    pass

        timer = threading.Timer(STOP_GRACE_S, _kill_after_grace)
        timer.daemon = True
        timer.start()


def build_turn_prompt(
    *,
    topic: dict,
    run_dir: Path,
    kb_root: Path,
    message: str,
) -> str:
    """Compose the stdin prompt: a topic-context block with paths relative to
    the KB root, followed by the raw user message. Prior turns are carried by
    ``claude --resume`` itself, so no history is replayed here."""

    def rel(path: Path) -> str:
        try:
            return Path(os.path.relpath(path, kb_root)).as_posix()
        except ValueError:
            return str(path)

    try:
        file_names = sorted(p.name for p in run_dir.iterdir() if p.is_file())
    except OSError:
        file_names = []
    listed = ", ".join(file_names[:MAX_PROMPT_CONTEXT_FILES])
    if len(file_names) > MAX_PROMPT_CONTEXT_FILES:
        listed += ", …"

    lines = [
        "<topic_context>",
        f"话题：{topic.get('title', '')}（id: {topic.get('id', '')}）",
        f"本次研究运行目录：{rel(run_dir)}/",
        f"证据附录：{rel(run_dir)}/evidence-appendix.md",
        f"运行清单：{rel(run_dir)}/run.json",
        f"运行目录文件：{listed}",
        "论文全文缓存目录：pool/（需要原文时自行检索）",
        "</topic_context>",
        "",
        message,
    ]
    return "\n".join(lines)


class ChatSessionRegistry:
    """Persistent ``{topic_id -> {session_id, messages, ...}}`` map stored at
    ``<data_dir>/chat-sessions.json``. Loading never raises: a missing or
    corrupt file simply means no conversations yet."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> dict:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"version": 1, "topics": {}}
        if not isinstance(data, dict) or not isinstance(data.get("topics"), dict):
            return {"version": 1, "topics": {}}
        data.setdefault("version", 1)
        return data

    def get(self, topic_id: str) -> dict | None:
        entry = self.load()["topics"].get(topic_id)
        return entry if isinstance(entry, dict) else None

    def _save(self, data: dict) -> None:
        atomic_write_json(self.path, data)

    def _mutate(self, topic_id: str, mutate) -> None:
        data = self.load()
        topics = data["topics"]
        entry = topics.get(topic_id)
        if not isinstance(entry, dict):
            entry = {"messages": []}
            topics[topic_id] = entry
        mutate(entry)
        entry["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        self._save(data)

    def record_session(self, topic_id: str, session_id: str | None, model: str | None = None) -> None:
        if not session_id:
            return

        def mutate(entry: dict) -> None:
            entry["session_id"] = session_id
            if model:
                entry["model"] = model

        self._mutate(topic_id, mutate)

    def append_message(self, topic_id: str, role: str, text: str) -> None:
        if not text:
            return

        def mutate(entry: dict) -> None:
            entry.setdefault("messages", []).append(
                {"role": role, "text": text, "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
            )
            del entry["messages"][:-MAX_HISTORY_MESSAGES]

        self._mutate(topic_id, mutate)

    def reset(self, topic_id: str) -> None:
        data = self.load()
        if topic_id in data["topics"]:
            del data["topics"][topic_id]
            self._save(data)
