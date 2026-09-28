"""The single binding to the ``claude`` CLI: every model-capability call in
the codebase goes through this module — one-shot :func:`complete` for
structured agent tasks (review writer, quick-read, slide decks, deep-read
skeletons, citation expansion) and :class:`ChatTurn` for interactive
streaming (wiki topic/workflow chat). Callers own prompts and output
parsing; this module owns everything else about talking to claude:

- CLI discovery and authentication preflight (:func:`resolve_cli`,
  :func:`claude_auth_ready`);
- spawn-environment isolation so headless agents never see the launching
  session's memory/projects/settings (:func:`isolated_claude_env`);
- nested-session guards (:data:`NESTED_CLAUDE_ENV_KEYS`, command assembly
  :func:`build_claude_command`, stream-json decoding :func:`parse_stream_line`);
- the machine-local conversation archive (``~/.claude/projects/
  embodied-learning-work``, :func:`record_agent_invocation`) where every
  invocation — topic chat, writer, quick-read, slide deck, deep-read
  skeleton — leaves prompt/output/metadata records.

Design rule: no module may spawn ``claude`` directly. Add capabilities here,
not at call sites.
"""

from __future__ import annotations

import datetime as dt
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

# ---- constants ------------------------------------------------------------

FALLBACK_CLI = "/usr/local/bin/claude"
# The one-shot agents run outside any session: pin a fast model, otherwise the
# CLI default (opus) makes even a tiny structured-output call exceed 2 minutes.
DRIVER_AGENT_MODEL = "glm-5.3-flash"
DEFAULT_PERMISSION_MODE = "bypassPermissions"
# Grace before SIGKILL after a requested stop (ChatTurn).
STOP_GRACE_S = 5.0

# Environment markers of a running claude session — a spawned headless agent
# must never think it is nested inside one.
NESTED_CLAUDE_ENV_KEYS = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT")
# Shell profiles often export CLAUDE_CODE_SUBAGENT_MODEL (e.g. a "-cc" SKU for
# interactive work). On claude CLI < 2.1.251 that env var has top precedence and
# forces every Task subagent inside a spawned session onto that model, beating
# even an explicit per-call model. Stripping it lets subagents fall through to
# "inherit the main conversation's model" — i.e. the pinned --model the caller
# passed, so subagents stay consistent with the main loop.
SPAWN_ENV_MODEL_KEYS = ("CLAUDE_CODE_SUBAGENT_MODEL",)
# Everything a spawned claude must not see, in one list (ChatTurn's inline
# guard and isolated_claude_env agree on this).
STRIPPED_SPAWN_ENV_KEYS = NESTED_CLAUDE_ENV_KEYS + SPAWN_ENV_MODEL_KEYS

# Isolated config dir for spawned agents: a per-user scratch, never inside a
# run dir (run dirs get registered in the catalog and may be synced — no
# credentials there). Redirecting CLAUDE_CONFIG_DIR hides the launcher's
# memory/projects/settings/user-CLAUDE.md from the spawned agent, which is the
# whole point: headless pipeline agents must work from the KB + packaged files
# only, not from whatever machine they happen to run on.
ISOLATED_CONFIG_DIR = Path.home() / ".cache" / "embodied-learning" / "claude-config"
CREDENTIALS_FILE = Path.home() / ".claude" / ".credentials.json"


# ---- conversation archive -------------------------------------------------


def conversation_store() -> Path:
    """Machine-local archive of every claude conversation/invocation record.

    A cache, never on the shared KB: it belongs to this machine, and the
    shared drive keeps only deliverable outputs. Env-overridable for tests."""

    override = os.environ.get("EMBODIED_CONVERSATION_STORE")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".claude" / "projects" / "embodied-learning-work"


def _slugify(label: str) -> str:
    slug = re.sub(r"\s+", "-", label.strip().lower())
    slug = re.sub(r"[^0-9A-Za-z一-鿿._-]+", "-", slug)
    return re.sub(r"-{2,}", "-", slug).strip("-._")[:60] or "invocation"


def record_agent_invocation(
    *,
    kind: str,
    label: str = "",
    prompt: str = "",
    stdout: str = "",
    stderr: str = "",
    returncode: int | None = None,
    cwd: str | Path | None = None,
    model: str | None = None,
    duration_s: float | None = None,
) -> Path | None:
    """Archive one claude invocation: per-call folder (prompt/output/meta) plus
    a line in ``invocations.jsonl``. Best-effort — recording must never break
    the agent call it wraps, so any storage failure returns None."""

    try:
        store = conversation_store()
        now = dt.datetime.now()
        stamp = now.strftime("%Y%m%d-%H%M%S")
        folder = store / kind / f"{stamp}-{os.getpid()}-{_slugify(label)}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "prompt.md").write_text(prompt, encoding="utf-8")
        (folder / "output.txt").write_text(stdout or "", encoding="utf-8")
        if stderr:
            (folder / "stderr.txt").write_text(stderr[-20000:], encoding="utf-8")
        meta = {
            "kind": kind,
            "label": label,
            "model": model,
            "cwd": str(cwd) if cwd else "",
            "returncode": returncode,
            "duration_s": round(duration_s, 2) if duration_s is not None else None,
            "ts": now.isoformat(timespec="seconds"),
            "prompt_chars": len(prompt),
            "output_chars": len(stdout or ""),
        }
        (folder / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        index_line = {**meta, "folder": str(folder.relative_to(store))}
        with (store / "invocations.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(index_line, ensure_ascii=False) + "\n")
        return folder
    except OSError:
        return None


# ---- spawn environment ----------------------------------------------------


def strip_nested_claude_env(env: dict[str, str] | None = None) -> dict[str, str]:
    """Copy of the environment without nested-claude session markers and
    shell-profile subagent-model overrides (see SPAWN_ENV_MODEL_KEYS)."""
    source = dict(os.environ) if env is None else dict(env)
    for key in STRIPPED_SPAWN_ENV_KEYS:
        source.pop(key, None)
    return source


def prepare_claude_config_dir(config_dir: Path | None = None) -> Path:
    """Create the isolated config dir, seeding credentials when the standard
    Linux credentials file exists. Idempotent; keeps the copy 0600."""
    target_dir = config_dir or ISOLATED_CONFIG_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / ".credentials.json"
    if not target.exists() and CREDENTIALS_FILE.is_file():
        shutil.copy2(CREDENTIALS_FILE, target)
        target.chmod(0o600)
    return target_dir


def isolated_claude_env(env: dict[str, str] | None = None) -> dict[str, str]:
    """Environment for spawned headless claude agents: nested-session markers
    stripped and CLAUDE_CONFIG_DIR pointed at the isolated scratch dir, so the
    agent starts from the KB + packaged files instead of the launcher's
    memory, project history, and settings."""
    prepared = strip_nested_claude_env(env)
    prepared["CLAUDE_CONFIG_DIR"] = str(prepare_claude_config_dir())
    return prepared


def claude_auth_ready(env: dict[str, str] | None = None) -> str | None:
    """Return an error message when spawned agents cannot authenticate.

    The isolated config dir has no keychain access; auth must come from the
    copied credentials file or an API key in the environment. Callers fail
    fast with this message instead of letting the writer stage time out on a
    confusing auth prompt."""
    source = os.environ if env is None else env
    if source.get("ANTHROPIC_API_KEY", "").strip():
        return None
    config_dir = source.get("CLAUDE_CONFIG_DIR", str(ISOLATED_CONFIG_DIR))
    if (Path(config_dir) / ".credentials.json").is_file():
        return None
    return (
        "无法认证 spawn 的 claude 代理：隔离配置目录缺少 .credentials.json，"
        "且环境未设置 ANTHROPIC_API_KEY。请先在 ~/.claude 登录一次或导出 API key。"
    )


def resolve_cli(cli: str | None = None) -> str | None:
    """Return a usable claude binary path, or None when absent (callers decide
    whether that degrades or fails). Explicit arg, then PATH, then the
    standard install location."""

    candidates = [cli] if cli else []
    candidates += ["claude", FALLBACK_CLI]
    for candidate in candidates:
        found = shutil.which(str(Path(candidate).expanduser()))
        if found:
            return found
    return None


# ---- one-shot completion ----------------------------------------------------


def complete(
    prompt: str,
    *,
    timeout_s: float,
    cli: str | None = None,
    model: str = DRIVER_AGENT_MODEL,
    permission_mode: str | None = DEFAULT_PERMISSION_MODE,
    cwd: str | Path | None = None,
    env: dict[str, str] | None = None,
    label: str = "",
    system_prompt: str | None = None,
    stream: bool = False,
    stream_to=None,
) -> subprocess.CompletedProcess:
    """One `claude -p` call with the prompt on stdin; returns the raw
    CompletedProcess. Without ``stream`` the stdout is plain text the caller
    parses itself (NOT stream-json; use ChatTurn for streaming). With
    ``stream=True`` the command switches to ``--output-format stream-json
    --verbose`` and, when ``stream_to`` (a writable file object) is given,
    the transcript is written there instead of captured in memory. ``env``
    defaults to the isolated spawn environment; ``cwd`` should be the KB root
    so the agent sees no repo CLAUDE.md and a clean project scope. Every
    invocation is archived in the conversation store (``label`` identifies it
    in invocations.jsonl, e.g. paper id / run name)."""

    if stream:
        command = build_claude_command(
            cli=cli,
            model=model,
            permission_mode=permission_mode,
            system_prompt=system_prompt,
        )
    else:
        command = [cli, "-p", "--model", model]
        if permission_mode:
            command += ["--permission-mode", permission_mode]
        if system_prompt:
            command += ["--append-system-prompt", system_prompt]
    begun = time.monotonic()
    run_kwargs: dict = {}
    if stream_to is not None:
        run_kwargs["stdout"] = stream_to
        run_kwargs["stderr"] = stream_to
    try:
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=stream_to is None,
            timeout=timeout_s,
            check=False,
            cwd=str(cwd) if cwd is not None else None,
            env=isolated_claude_env() if env is None else env,
            **run_kwargs,
        )
    except subprocess.TimeoutExpired as exc:
        record_agent_invocation(
            kind="one-shot", label=label, prompt=prompt,
            stdout=exc.stdout or "" if isinstance(exc.stdout, str) else "",
            stderr=str(exc.stderr or "")[-20000:],
            returncode=None, cwd=cwd, model=model,
            duration_s=time.monotonic() - begun,
        )
        raise
    record_agent_invocation(
        kind="one-shot", label=label, prompt=prompt,
        stdout=result.stdout or "", stderr=result.stderr or "",
        returncode=result.returncode, cwd=cwd, model=model,
        duration_s=time.monotonic() - begun,
    )
    return result


# ---- streaming (interactive chat) -------------------------------------------


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
    """Assemble the streaming (``--output-format stream-json``) claude
    invocation. The user prompt is NEVER part of argv — it is written to
    stdin by ChatTurn (shell/quoting safety)."""

    argv = [cli, "-p", "--output-format", "stream-json", "--verbose"]
    if permission_mode:
        argv += ["--permission-mode", permission_mode]
    if system_prompt:
        argv += ["--append-system-prompt", system_prompt]
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
    """Translate one stream-json line into 0..n normalized events
    (session / delta / status / done)."""

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
    )


class ChatTurn:
    """One claude chat turn: a spawned ``claude -p`` process bridged to a
    thread-safe event queue so an HTTP handler can stream events while a
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
        timeout_s: float = 900.0,
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
        self.system_prompt = system_prompt
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
        env = strip_nested_claude_env()
        # Isolate the spawned chat from the launcher session's memory and
        # settings (same guarantee as isolated_claude_env) so the chat only
        # sees the KB, not the server operator's projects.
        env["CLAUDE_CONFIG_DIR"] = str(prepare_claude_config_dir())
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
        stream_lines: list[str] = []
        try:
            for line in self._process.stdout:
                stream_lines.append(line)
                for event in parse_stream_line(line):
                    self._queue.put(("event", event))
        except (OSError, ValueError):
            pass
        finally:
            code = self._process.poll() if self._process else None
            # Archive BEFORE the exit marker: consumers (events()) must be
            # able to rely on the transcript being on disk once they see the
            # turn end.
            self._archive_turn("".join(stream_lines), code)
            self._queue.put(("exit", code))
        if self._timer:
            self._timer.cancel()

    def _archive_turn(self, stream: str, returncode: int | None):
        """Archive the raw stream-json transcript of this turn into the
        conversation store — chat transcripts and one-shot calls live in one
        archive (see conversation_store)."""

        return record_agent_invocation(
            kind="chat",
            label=f"{self.cwd.name}-{self.session_id or 'new'}",
            prompt=self.prompt,
            stdout=stream,
            stderr="\n".join(self._stderr_tail),
            returncode=returncode,
            cwd=self.cwd,
            model=self.model,
        )

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
        """Wait up to ``timeout_s`` (default 120s) for the first queue item and
        return it if it is an event. Used by the caller to detect a resume
        failure before streaming starts; the item stays queued for events()
        (or is remembered if it was the exit marker). Returns None on timeout
        or early exit — a timeout means claude produced nothing at all (hung
        process / stalled API), and the caller should surface that instead of
        holding the HTTP request open forever."""

        if self._early_exit_seen:
            return None
        try:
            kind, payload = self._queue.get(timeout=120.0 if timeout_s is None else timeout_s)
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
