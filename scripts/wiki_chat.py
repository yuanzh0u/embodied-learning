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
FIRST_EVENT_TIMEOUT_S = 120.0  # claude must show its first event within this window
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

WORKFLOW_SYSTEM_PROMPT = (
    "你是「空间智能研究 Wiki」的综述工作流执行器，工作目录即本地知识库根目录。"
    "<skills-root> 下是本仓库的技能树（每个子目录含 SKILL.md 与 scripts/），"
    "<scripts-root> 下是顶层脚本（check_run_bundle.py、audit_citations.py 等）。"
    "按照 <skills-root>/embodied-ai-literature-review/SKILL.md 的综述契约执行，"
    "SKILL.md 中出现的相对路径按其所在目录解析：路径以 skills/ 开头时替换为 <skills-root>，"
    "以 scripts/ 开头时替换为 <scripts-root>。"
    "\n\n【职责边界——固定流程已由系统完成】\n"
    "查询规划、候选检索（Semantic Scholar + arXiv）、候选注册、筛选、覆盖度评估、"
    "全文 HTML 抽取、论文深读（速记骨架+审计）与证据投影已由驱动脚本 run_review_pipeline.py 一次性完成，"
    "产物都在运行目录：先读 pipeline-summary.json（各阶段耗时、候选/全文/深读/证据计数、覆盖维度、筛选词及来源），"
    "再按需读 screening.json、coverage-report.json、paper-notes/、evidence/。"
    "不要手动执行任何检索/抽取/筛选/深读/投影命令（search_arxiv.py、search_semantic_scholar.py、"
    "build_candidate_registry.py、screen_candidates.py、assess_review_coverage.py、"
    "extract_content_queue.py、build_reading_packet.py、build_paper_note.py、"
    "project_evidence_events.py、run_review_pipeline.py）"
    "——重复执行只会浪费时长且可能触发限流。若 summary 显示维度、地板或深读未过，如实向用户说明，不要自行补救检索。"
    "\n\n【你的三个判断职责】\n"
    "1. 论文深读与证据投影：已由系统驱动脚本完成（速记骨架 + 审计 + 投影）。"
    "不要派发深读 subagent、不要跑 project_evidence_events.py；"
    "若 pipeline-summary.json 的 deep_read 字段显示失败篇目，如实向用户说明。\n"
    "2. 综述包与大纲：跑 <scripts-root> 同级的 "
    "build_review_packet.py（--topic … --knowledge-id … --evidence-jsonl work/<run>/evidence/*.jsonl "
    "--review-mode … --coverage-report …），然后亲自输出综述大纲与选文摘要，"
    "立即停止输出、结束本轮回复，等待用户确认——不要自行撰写成稿。\n"
    "3. 成稿与审计（用户确认后续轮）：按目标风格亲自撰写成稿（review-packet 是简报不是成稿），"
    "生成 trace-map.json，逐一通过 check_run_bundle.py、audit_citations.py、audit_article_quality.py "
    "审计门后才允许落盘 evidence/ 并注册目录。\n"
    "\n\n在开始每个阶段前，先单独输出一行阶段标记（普通文本，不要放进代码块）："
    "[STAGE:mining] / [STAGE:packet] / [STAGE:writing] / [STAGE:audit] / [STAGE:settle]，后跟一句话进度说明。"
    "落盘到 evidence/ 后，在最终回复的单独一行输出 "
    "[TOPIC:<evidence/ 下新运行目录的相对路径>]，不要带其他后缀。"
    "\n\n【科研备忘录（scientific-memo_keyan.md）引文格式——必须遵守】\n"
    "正文引用用上标编号，每条引用单独一个标记、带方括号：单条 ^[1]^；多条时逐条并列写成 "
    "^[1]^ ^[2]^ ^[3]^，严禁把多个编号塞进同一个标记（^[1,2,3]^ 是格式错误）。"
    "文末「参考文献」编号列表：编号对应正文上标，每条列出论文名称（英文原题）、"
    "作者（第一作者 et al.）、年份，并附 arXiv 链接（[arXiv:2602.11323](https://arxiv.org/abs/2602.11323) 形式）"
    "——Wiki 构建时会按这条链接把正文上标解析成可点击的阅读链接。"
    "除参考文献列表外，正文叙述中不要出现 arxiv.org 链接或 [arXiv:2402.xxxxx] 式前缀。"
    "知乎版与小红书版不受此约束（沿用各自的宽松风格）。"
    "\n\n若指定的运行目录已存在中间产物（extractions/、paper-notes/ 等），从磁盘已有进度继续"
    "（已通过审计的笔记直接复用，不要重读重写），只补缺失部分。"
    "除落盘阶段外只写入 <work-dir> 运行目录；用中文与用户交流。"
)


def resolve_pipeline_layout(pipeline_root: Path) -> tuple[Path, Path]:
    """Given the pipeline root, return (skills_root, scripts_root).

    Repo checkout / clone: <root>/skills/...; wheel-bundled tree: <root> IS
    the skills/ dir itself. scripts/ sits beside skills/ when the checkout
    has it, otherwise at <root>/../scripts (bundled layout)."""

    skills_root = pipeline_root if pipeline_root.name == "skills" else pipeline_root / "skills"
    scripts_root = (
        pipeline_root / "scripts"
        if (pipeline_root / "scripts" / "init_run.py").is_file()
        else pipeline_root.parent / "scripts"
    )
    return skills_root, scripts_root


def substitute_prompt_roots(
    text: str, *, skills_root: Path, scripts_root: Path, pool_root: Path | None = None
) -> str:
    """Fill the <skills-root>/<scripts-root>/<pool-root> placeholders in a
    workflow prompt. Paths travel KB-relative like all other prompt context
    (no absolute leak); an absent pool keeps the placeholder literal (the
    pool-lookup instruction just never matches)."""

    text = text.replace("<skills-root>", skills_root.as_posix()).replace(
        "<scripts-root>", scripts_root.as_posix()
    )
    if pool_root is not None:
        text = text.replace("<pool-root>", pool_root.as_posix())
    return text

TOPIC_ID_RE = re.compile(r"^topic-[0-9a-f]{6,16}$")
WS_ID_RE = re.compile(r"^ws-[0-9a-f]{6,16}$")
STAGE_RE = re.compile(r"^\[STAGE:([a-z_]+)\]\s*(.*)$")
TOPIC_MARKER_RE = re.compile(r"^\[TOPIC:([^\]]+)\]\s*$")
WORKFLOW_STAGE_NAMES = (
    "init",
    "plan",
    "retrieval",
    "mining",
    "packet",
    "writing",
    "audit",
    "settle",
)

# Driver-stage lines emitted by scripts/run_review_pipeline.py (the mechanical
# stages run in code before claude starts). Reuse the [STAGE:*] vocabulary so
# the frontend timeline lights the same pills: plan/retrieval/mining map from
# driver stage names; unknown names pass through.
DRIVER_STAGE_RE = re.compile(r"^\[DRIVER-STAGE:([a-z_-]+)\]\s*(.*)$")
DRIVER_STAGE_TO_WORKFLOW = {
    "plan": "plan",
    "retrieval-arxiv": "retrieval",
    "registry": "retrieval",
    "screening": "mining",
    "coverage": "mining",
    "extraction": "mining",
    "packets": "mining",
    "summary": "mining",
}

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

    def new_turn(
        self,
        *,
        prompt: str,
        cwd: Path,
        session_id: str | None = None,
        system_prompt: str | None = None,
        timeout_s: float | None = None,
        model: str | None = None,
        effort: str | None = None,
    ) -> "ChatTurn":
        assert self.cli is not None, "new_turn() on a disabled ChatConfig"
        return ChatTurn(
            cli=self.cli,
            prompt=prompt,
            cwd=cwd,
            session_id=session_id,
            model=model if model is not None else self.model,
            permission_mode=self.permission_mode,
            allowed_tools=self.allowed_tools,
            system_prompt=system_prompt if system_prompt is not None else CHAT_SYSTEM_PROMPT,
            timeout_s=self.timeout_s if timeout_s is None else timeout_s,
            effort=effort,
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
    system_prompt: str | None = None,
    effort: str | None = None,
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
        system_prompt if system_prompt is not None else CHAT_SYSTEM_PROMPT,
    ]
    if session_id:
        argv += ["--resume", session_id]
    if model:
        argv += ["--model", model]
    if effort:
        argv += ["--effort", effort]
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
        system_prompt: str | None = None,
        effort: str | None = None,
    ):
        self.cli = cli
        self.prompt = prompt
        self.cwd = Path(cwd)
        self.session_id = session_id
        self.model = model
        self.permission_mode = permission_mode
        self.allowed_tools = allowed_tools
        self.timeout_s = timeout_s
        self.system_prompt = system_prompt if system_prompt is not None else CHAT_SYSTEM_PROMPT
        self.effort = effort
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
            system_prompt=self.system_prompt,
            effort=self.effort,
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

    def peek_event(self, timeout_s: float | None = None) -> dict | None:
        """Wait up to ``timeout_s`` (default FIRST_EVENT_TIMEOUT_S) for the
        first queue item and return it if it is an event. Used by the caller
        to detect a resume failure before streaming starts; the item stays
        queued for events() (or is remembered if it was the exit marker).
        Returns None on timeout or early exit — a timeout means claude
        produced nothing at all (hung process / stalled API), and the caller
        should surface that instead of holding the HTTP request open forever."""

        if self._early_exit_seen:
            return None
        try:
            kind, payload = self._queue.get(timeout=FIRST_EVENT_TIMEOUT_S if timeout_s is None else timeout_s)
        except queue.Empty:
            return None
        if kind == "exit":
            self._early_exit_seen = True
            return None
        if kind == "event":
            self._peeked = payload
            return payload
        self._peeked = payload
        return payload  # error event

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

    @property
    def is_alive(self) -> bool:
        """True while the claude process exists and hasn't exited."""

        return self._process is not None and self._process.poll() is None

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


def build_paper_turn_prompt(*, arxiv_id: str, message: str) -> str:
    """Paper-chat kickoff/continuation prompt. The system prompt carries the
    standing instructions; this block pins the paper identity and points at
    the pooled full text + deep-read note. Prior turns ride on claude
    --resume, keyed by the paper id."""

    lines = [
        "<paper_context>",
        f"论文 arXiv ID：{arxiv_id}",
        f"全文（Markdown）：pool/arxiv-{arxiv_id}/paper.md",
        f"全文（HTML，给用户的阅读链接）：/api/reader/{arxiv_id}",
        f"深读笔记（若存在）：pool/arxiv-{arxiv_id}/note.json",
        f"抽取元数据：pool/arxiv-{arxiv_id}/extraction.json",
        "回答前先读 paper.md 的相关章节；结论引用原文时给出所在小节标题。",
        "</paper_context>",
        "",
        message,
    ]
    return "\n".join(lines)


PAPER_CHAT_SYSTEM_PROMPT = (
    "你是「空间智能研究 Wiki」的单篇论文精读助手，工作目录即本地知识库根目录。"
    "用户正围绕一篇 arXiv 论文提问，论文全文与深读笔记在 pool/arxiv-<id>/ 下。"
    "回答规则：先读 paper.md 相关章节再下结论；引用原文用英文短引 + 中文解释，"
    "并注明所在小节；论文没写的内容明确说「论文未涉及」，不要脑补；"
    "公式、表格、实验数字以原文为准，不要凭记忆复述。"
    "用户可能想了解：方法细节、与相关工作的对比、可复用性、局限性。"
    "若 pool/arxiv-<id>/note.json 存在，优先采信其中已通过逐字审计的 claim 卡。"
    "用中文回答，先给中心判断，再给证据。"
)


def extract_stage_markers(text: str) -> list[tuple[str, str]]:
    """Extract ``[STAGE:<name>] detail`` lines from streamed text, in order.

    The workflow system prompt tells claude to print one marker line before
    each pipeline stage; the server turns them into structured timeline
    events. Unknown stage names are kept so the UI can still show them."""

    markers: list[tuple[str, str]] = []
    for line in text.splitlines():
        match = STAGE_RE.match(line.strip())
        if match:
            markers.append((match.group(1), match.group(2).strip()))
    return markers


def extract_driver_stage(line: str) -> tuple[str, str] | None:
    """Map one driver stdout line to a (workflow_stage, detail) tuple, or None.

    The driver runs before claude in a kickoff; the server forwards its
    progress onto the same timeline so the user sees plan → retrieval →
    mining advance in code, not in agent narration."""

    match = DRIVER_STAGE_RE.match(line.strip())
    if not match:
        return None
    return DRIVER_STAGE_TO_WORKFLOW.get(match.group(1), "mining"), match.group(2).strip()


def extract_driver_detail(line: str) -> str | None:
    """Free-form progress lines from the pipeline driver (per-paper reads,
    assembly results, retrieval-plan notes). Anything printed as ``[PAPER] …``,
    ``[DRIVER] …`` or ``[DRIVER-WARN] …`` becomes dialog detail text; other
    lines are ignored."""

    stripped = line.strip()
    for prefix in ("[PAPER]", "[DRIVER]"):
        if stripped.startswith(prefix):
            detail = stripped[len(prefix):].strip()
            return detail or None
    return None


def extract_topic_marker(text: str) -> str | None:
    """Return the run-dir relpath from a ``[TOPIC:<relpath>]`` line, if any."""

    for line in text.splitlines():
        match = TOPIC_MARKER_RE.match(line.strip())
        if match:
            return match.group(1).strip()
    return None


def build_workflow_prompt(
    *,
    params: dict,
    run_dir: Path,
    kb_root: Path,
    pipeline_root: Path,
) -> str:
    """Compose the workflow kickoff prompt from the interview parameters.

    ``pipeline_root`` is the skills/ root (repo checkout or the wheel-bundled
    tree — claude reads the SKILL.mds and pipeline scripts from there);
    ``run_dir`` is the pre-created in-progress run under ``<kb-root>/work/``.
    Paths travel KB-relative like build_turn_prompt."""

    def rel(path: Path) -> str:
        try:
            return Path(os.path.relpath(path, kb_root)).as_posix()
        except ValueError:
            return str(path)

    topic = str(params.get("topic", "")).strip()
    skills_root, scripts_root = resolve_pipeline_layout(pipeline_root)
    skills_rel = rel(skills_root)
    scripts_rel = rel(scripts_root)
    lines = [
        "<workflow_request>",
        f"综述主题：{topic}",
        f"综述模式：{params.get('review_mode', 'scoping')}",
        f"时间范围：{params.get('time_range', '')}",
        f"检索策略：{params.get('search_strategy', 'smart')}",
        f"种子论文：{params.get('seed_arxiv_ids') or '无'}",
        f"目标风格：{params.get('target_style', 'all')}",
        f"关注重点：{params.get('focus') or '无'}",
        f"运行目录（已由系统创建，status: in-progress）：{rel(run_dir)}/",
        f"skills 根目录（SKILL.md 所在，读技能与脚本用）：<skills-root>={skills_rel}",
        f"顶层脚本目录（check_run_bundle/audit_citations）：<scripts-root>={scripts_rel}",
        "执行状态：查询规划、检索、筛选、全文抽取、深读（每篇速记骨架+审计）与证据投影"
        "已由系统驱动脚本 run_review_pipeline.py 全部完成"
        "（产物见运行目录的 pipeline-summary.json、paper-notes/、evidence/），"
        "不要重跑任何检索/抽取/筛选/深读/投影命令。",
        "执行要求：先读 pipeline-summary.json 与 writing 输入现状，"
        "然后直接跑 build_review_packet.py 生成综述包（[STAGE:packet]），"
        "亲自阅读证据事件与综述包后输出大纲与选文摘要，立即停止本轮回复，等待用户确认；"
        "不要自行撰写成稿。若 pipeline-summary 显示深读有失败篇目，如实向用户说明影响。",
        "</workflow_request>",
    ]
    return "\n".join(lines)


def build_continuation_prompt(
    *, feedback: str = "", target_style: str = "", stage: str = ""
) -> str:
    """Resume the workflow after a pause. The prompt is stage-aware: a run
    parked before the outline checkpoint finishes mining first; only a run
    that already produced the packet goes straight to writing."""

    feedback = (feedback or "").strip()
    opinion = feedback if feedback else "无，按现有大纲继续"
    style = (target_style or "all").strip()
    if style == "all":
        writing_clause = "撰写三种成稿（scientific-memo / zhihu / xiaohongshu）"
        parallel_clause = (
            "成稿阶段用 3 个并行 subagent 分别起草三种风格，主线程统一润色对齐后再走审计门"
        )
    else:
        style_label = {
            "scientific-memo": "科研备忘录（scientific-memo_keyan.md）",
            "expert-explainer": "知乎解释版（zhihu-explainer_zhihu.md）",
            "kol-thread": "小红书版（xiaohongshu-post_xiaohongshu.md）",
        }.get(style, style)
        writing_clause = f"仅撰写采访中选定的风格：{style_label}，不要写其他风格"
        parallel_clause = "单一成稿由主线程直接撰写润色，再走审计门"
    if stage in ("init", "plan", "retrieval", "mining", ""):
        # The outline checkpoint was never reached: finish the interrupted
        # stage first, then run packet → stop at the checkpoint again.
        lines = [
            "用户发来消息。先从磁盘已有进度继续当前阶段（检查 pipeline-summary.json 与运行目录产物，"
            "已完成的环节不要重做），完成深读与证据投影后生成综述包（[STAGE:packet]），"
            "输出大纲与选文摘要后立即停止本轮回复，等待用户确认——不要自行撰写成稿。",
            f"用户消息：{opinion}",
        ]
        return "\n".join(lines)
    lines = [
        "用户已确认综述包大纲，请继续执行剩余阶段（[STAGE:writing] → [STAGE:audit] → "
        f"[STAGE:settle]）：{writing_clause}、通过审计门、落盘 evidence/ 并在目录中注册，"
        "最后输出 [TOPIC:<运行目录相对路径>]。",
        f"{parallel_clause}，尽量压缩总时长。",
        "落盘前把 run.json 的 status 改为 settled，并按实际产出声明 files.outputs；"
        + (
            "若只产出单一成稿，同时写入 style 与 scope_note 字段（说明用户只要这一风格）。"
            if style != "all"
            else "三种成稿齐全时无需 style/scope_note 字段。"
        ),
        f"用户对大纲的意见：{opinion}",
    ]
    return "\n".join(lines)


class ChatSessionRegistry:
    """Persistent conversation store at ``<data_dir>/chat-sessions.json``::

        {"version": 1,
         "topics": {topic_id: {...}},
         "workspaces": {ws_id: {..., "workflow": {...}}}}

    Topic chats and workflow workspaces share the entry shape (session id,
    message history); workspaces additionally carry workflow state. Loading
    never raises: a missing or corrupt file simply means no conversations yet."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> dict:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"version": 1, "topics": {}, "workspaces": {}}
        if not isinstance(data, dict) or not isinstance(data.get("topics"), dict):
            return {"version": 1, "topics": {}, "workspaces": {}}
        data.setdefault("version", 1)
        data.setdefault("workspaces", {})
        return data

    def get(self, topic_id: str) -> dict | None:
        entry = self.load()["topics"].get(topic_id)
        return entry if isinstance(entry, dict) else None

    def get_workspace(self, ws_id: str) -> dict | None:
        entry = self.load()["workspaces"].get(ws_id)
        return entry if isinstance(entry, dict) else None

    @staticmethod
    def _namespace_for(key: str) -> str:
        """Workspaces are "ws-"-prefixed; every other key (topics, paper chats)
        lands in the topics namespace."""

        return "workspaces" if key.startswith("ws-") else "topics"

    def _save(self, data: dict) -> None:
        atomic_write_json(self.path, data)

    def _mutate(self, key: str, mutate, *, namespace: str = "topics") -> None:
        data = self.load()
        space = data.setdefault(namespace, {})
        entry = space.get(key)
        if not isinstance(entry, dict):
            entry = {"messages": []}
            space[key] = entry
        mutate(entry)
        entry["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        self._save(data)

    def record_session(self, key: str, session_id: str | None, model: str | None = None) -> None:
        """Bind the latest claude session id to a topic or workspace key."""

        namespace = self._namespace_for(key)
        if not session_id:
            return

        def mutate(entry: dict) -> None:
            entry["session_id"] = session_id
            if model:
                entry["model"] = model

        self._mutate(key, mutate, namespace=namespace)

    def append_message(self, key: str, role: str, text: str) -> None:
        namespace = self._namespace_for(key)
        if not text:
            return

        def mutate(entry: dict) -> None:
            entry.setdefault("messages", []).append(
                {"role": role, "text": text, "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
            )
            del entry["messages"][:-MAX_HISTORY_MESSAGES]

        self._mutate(key, mutate, namespace=namespace)

    def set_workflow_state(self, ws_id: str, **fields) -> None:
        """Merge fields into a workspace's ``workflow`` sub-object (stage,
        awaiting_input, run_dir, params, ...)."""

        def mutate(entry: dict) -> None:
            workflow = entry.setdefault("workflow", {})
            workflow.update(fields)

        self._mutate(ws_id, mutate, namespace="workspaces")

    def link_topic(self, ws_id: str, topic_id: str) -> None:
        def mutate(entry: dict) -> None:
            entry["topic_id"] = topic_id

        self._mutate(ws_id, mutate, namespace="workspaces")

    def reset(self, key: str) -> None:
        data = self.load()
        space = data.get(self._namespace_for(key), {})
        if isinstance(space, dict) and key in space:
            del space[key]
            self._save(data)
