"""Chat backend for the research Wiki: bridge a browser chat box to the local
``claude`` CLI (Claude Code) with ``--print --output-format stream-json``.

The design mirrors lark-coding-agent-bridge's Claude adapter: the prompt goes
through stdin (never argv), stdout is parsed as NDJSON events, and a stop is
SIGTERM followed by SIGKILL after a grace window. One chat session id is bound
to each wiki topic and persisted in ``<data_dir>/chat-sessions.json`` so
conversations survive server restarts and are resumed with ``--resume``.
"""

from __future__ import annotations

import datetime as dt
import json
import hashlib
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

from embodied_learning.harness.claude import conversation_store  # noqa: F401  (compat re-export)
from embodied_learning.utils.jsonio import atomic_write_json
from embodied_learning import locks
# All claude invocation machinery lives in the harness (pybind-style binding);
# this module keeps prompts, session registry, and HTTP glue only.
from embodied_learning.harness.claude import (  # noqa: E402,F401
    ChatTurn,
    DEFAULT_PERMISSION_MODE,
    FALLBACK_CLI,
    build_claude_command,
    is_resume_failure,
    parse_stream_line,
    prepare_claude_config_dir,
)
from embodied_learning.harness.claude import resolve_cli as _harness_resolve_cli  # noqa: E402
from embodied_learning.harness.prompt import (  # noqa: F401  (prompt text + builders live there)
    CHAT_SYSTEM_PROMPT,
    PAPER_CHAT_SYSTEM_PROMPT,
    REVISION_QUALITY_FLAG,
    REVISION_STYLE_BY_KEY,
    REVISION_STYLE_LABEL,
    STYLE_VOICE_CONTRACTS,
    WORKFLOW_SYSTEM_PROMPT,
    build_continuation_prompt,
    build_paper_turn_prompt,
    build_revision_prompts,
    build_turn_prompt,
    build_workflow_prompt,
    substitute_prompt_roots,
    workflow_system_prompt,
    workflow_turn_prompts,
    workflow_turn_system_prompt,
)
from embodied_learning.utils.layout import resolve_pipeline_layout  # noqa: F401
from embodied_learning.config import DEFAULT_CHAT_TIMEOUT_S, FIRST_EVENT_TIMEOUT_S, MAX_HISTORY_MESSAGES, MAX_PROMPT_CONTEXT_FILES, STOP_GRACE_S
# DEFAULT_PERMISSION_MODE / FALLBACK_CLI are re-exported from the harness
# above (the single source for "how claude is invoked") — do not redeclare.


def local_registry_path(kb_root: Path | str) -> Path:
    """Machine-local home for the chat-session registry (a cache, never shared).

    Conversation history belongs to the server process serving THIS machine's
    browsers; cross-machine sharing would buy nothing (each machine's claude
    sessions are independent) while putting the highest-frequency
    read-merge-rewrite in the whole system — one per chat message — onto a
    possibly flaky NAS. The kb_root hash scopes the cache per knowledge base,
    so several servers on one machine (different ports, same KB) still share
    one history file and keep cross-process exclusion via a machine-local
    kb_lock. The shared KB keeps only deliverable outputs (evidence/pool/
    knowledge/runs/wiki snapshots); the store root itself archives every
    claude conversation (see harness.claude.conversation_store)."""

    digest = hashlib.sha256(str(Path(kb_root).resolve()).encode("utf-8")).hexdigest()[:16]
    return conversation_store() / "chat-sessions" / digest / "chat-sessions.json"

# The workflow system prompt has exactly ONE deliberate fork: the interactive
# wiki ("agent" publisher) finishes the mechanical settle itself (run.py finalize)
# and emits [STAGE:]/[TOPIC:] markers the wiki UI parses; the headless launcher
# ("launcher" publisher) stops right after the audit gates — the launcher process
# does finalize/publish in code. Everything else (role, boundaries, judgment
# duties, stop conditions, citation contract, resume discipline) is byte-identical
# for both entry points. Prompt text lives ONLY here; both scripts/serve_research_wiki.py
# and scripts/run.py launch compose through the factories below.
# Compatibility alias: the interactive call sites and existing tests read this
# name; it is always the interactive ("agent") variant.
TOPIC_ID_RE = re.compile(r"^topic-[0-9a-f]{6,16}$")
WS_ID_RE = re.compile(r"^ws-[0-9a-f]{6,16}$")
STAGE_RE = re.compile(r"^\[STAGE:([a-z_]+)\]\s*(.*)$")
TOPIC_MARKER_RE = re.compile(r"^\[TOPIC:([^\]]+)\]\s*$")
# Terminal marker for the designed user decision points (e.g. 精读数量不够):
# the writer reports and stops; the server must NOT auto-continue past it.
STOP_MARKER_RE = re.compile(r"^\[STOP:([a-z-]+)\]\s*$")
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

# Driver-stage lines emitted by scripts/run.py pipeline (the mechanical
# stages run in code before claude starts). Reuse the [STAGE:*] vocabulary so
# the frontend timeline lights the same pills: plan/retrieval/mining map from
# driver stage names; unknown names pass through.
DRIVER_STAGE_RE = re.compile(r"^\[DRIVER-STAGE:([a-z_-]+)\]\s*(.*)$")
DRIVER_STAGE_TO_WORKFLOW = {
    "plan": "plan",
    "retrieval-arxiv": "retrieval",
    "screening": "mining",
    "coverage": "mining",
    "extraction": "mining",
    "packets": "mining",
    "summary": "mining",
}

# [DRIVER-PHASE:<name>] marks the START of a driver block (plan/retrieval/
# mining); completion keeps using [DRIVER-STAGE:*]. Without start markers,
# free-form lines logged before the first completion line all land on the
# default stage and the timeline shows 全文挖掘 from the first second.
DRIVER_PHASE_RE = re.compile(r"^\[DRIVER-PHASE:([a-z_-]+)\]\s*(.*)$")
DRIVER_PHASE_TO_WORKFLOW = {
    "plan": "plan",
    "retrieval": "retrieval",
    "mining": "mining",
}

# [DRIVER-PROGRESS:<name>:<done>/<total>] — per-item progress (extraction
# queue, reading packets, deep read). Rendered as an in-place progress bar in
# the dialog; per-paper detail lines are deliberately NOT forwarded so the
# dialog stays readable.
DRIVER_PROGRESS_RE = re.compile(r"^\[DRIVER-PROGRESS:([a-z_-]+):(\d+)/(\d+)\]\s*(.*)$")

# [DRIVER-BRIEF:<stage>] <json> — per-stage results brief (title + lines).
# The human-checkable work product of that stage (query list, selected papers,
# deep-read outcomes…): what a reviewer verifies and what a debugger replays.
# One JSON object on the line so multi-line briefs survive stdout framing.
DRIVER_BRIEF_RE = re.compile(r"^\[DRIVER-BRIEF:([a-z_-]+)\]\s+(\{.*\})\s*$")



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
    standard install location. Raises ChatUnavailableError when none exists
    (the harness lookup is shared; only the failure contract differs here)."""

    found = _harness_resolve_cli(cli)
    if found is None:
        raise ChatUnavailableError(
            f"未找到 claude 命令（已尝试 PATH 与 {FALLBACK_CLI}）。请安装 Claude Code 或用 --chat-cli 指定路径。"
        )
    return found


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


def extract_driver_phase(line: str) -> tuple[str, str] | None:
    """Map one ``[DRIVER-PHASE:<name>]`` start-of-block line to a workflow
    stage plus its start detail, or None."""

    match = DRIVER_PHASE_RE.match(line.strip())
    if not match:
        return None
    stage = DRIVER_PHASE_TO_WORKFLOW.get(match.group(1))
    if stage is None:
        return None
    return stage, match.group(2).strip()


def extract_driver_progress(line: str) -> tuple[str, int, int, str] | None:
    """Parse one ``[DRIVER-PROGRESS:<name>:<done>/<total>]`` line into
    (name, done, total, detail), or None."""

    match = DRIVER_PROGRESS_RE.match(line.strip())
    if not match:
        return None
    return match.group(1), int(match.group(2)), int(match.group(3)), match.group(4).strip()


def extract_driver_brief(line: str) -> tuple[str, str, list[str]] | None:
    """Parse one ``[DRIVER-BRIEF:<stage>] {json}`` line into
    (stage, title, lines), or None. Malformed JSON is dropped (the stage
    detail lines already carry the counts)."""

    match = DRIVER_BRIEF_RE.match(line.strip())
    if not match:
        return None
    try:
        payload = json.loads(match.group(2))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    title = " ".join(str(payload.get("title") or "").split())
    raw_lines = payload.get("lines")
    lines = (
        [" ".join(str(item).split()) for item in raw_lines if str(item).strip()]
        if isinstance(raw_lines, list)
        else []
    )
    return match.group(1), title, lines


def extract_driver_detail(line: str) -> str | None:
    """Free-form progress lines from the pipeline driver (per-paper reads,
    assembly results, retrieval-plan notes). Anything printed as ``[PAPER] …``,
    ``[DRIVER] …`` or ``[DRIVER-WARN] …`` becomes dialog detail text; other
    lines are ignored."""

    stripped = line.strip()
    for prefix in ("[PAPER]", "[DRIVER]", "[DRIVER-WARN]"):
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


def extract_stop_marker(text: str) -> str | None:
    """Return the reason slug from a ``[STOP:<reason>]`` line, if any.

    ``[STOP:awaiting-user]`` marks a designed user decision point (e.g.
    精读数量不够): the writer has reported and stopped on purpose — the
    workflow must park and wait for the user, never auto-continue."""

    for line in text.splitlines():
        match = STOP_MARKER_RE.match(line.strip())
        if match:
            return match.group(1).strip()
    return None


# Per-style voice contracts injected into writer prompts. The writing brief is
# style-agnostic and speaks in tension/thesis language (the zhihu register), so
# without an explicit contract the one-shot writer drifts every style toward
# the zhihu-explainer voice (suspense headline, bold "不是A而是B" opening) —
# observed on both 2026-09-17 and 2026-09-18 scientific memos.
# ---- 成稿修订（版本管理）---------------------------------------------------
# The wiki's revision flow turns one user requirement into an additive
# revisions/<style>-v<N>.md next to the base deliverable — never an overwrite.

REVISION_MARKER_RE = re.compile(r"^\[REVISION:([^\]]+)\]\s*$")


class ChatSessionRegistry:
    """Persistent conversation store at ``<data_dir>/chat-sessions.json``::

        {"version": 1,
         "topics": {topic_id: {...}},
         "workspaces": {ws_id: {..., "workflow": {...}}}}

    Topic chats and workflow workspaces share the entry shape (session id,
    message history); workspaces additionally carry workflow state. Loading
    never raises: a missing or corrupt file simply means no conversations yet."""

    def __init__(self, path: Path, lock_root: Path | None = None):
        self.path = Path(path)
        # Cross-process lock root: <kb-root> when the wiki data dir is the
        # canonical <kb-root>/wiki/data (chat-sessions.json lives two levels
        # below the KB root). Multiple wiki servers — same machine on
        # different ports, or different machines on a shared mount — mutate
        # this one file, so load→mutate→save must hold the KB-shared lock.
        self.lock_root = (
            Path(lock_root)
            if lock_root
            else (self.path.parents[2] if len(self.path.parents) > 3 else self.path.parent)
        )

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

    def _mutate(self, key: str, mutate, *, namespace: str = "topics", require_existing: bool = False) -> None:
        with locks.kb_lock(self.lock_root, "wiki-chat-sessions", wait=30):
            data = self.load()
            space = data.setdefault(namespace, {})
            entry = space.get(key)
            if not isinstance(entry, dict):
                # require_existing: a reset() won the race — do not resurrect a
                # zombie entry from an in-flight turn's cleanup writes.
                if require_existing:
                    return
                entry = {"messages": []}
                space[key] = entry
            mutate(entry)
            entry["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            self._save(data)

    def record_session(self, key: str, session_id: str | None, model: str | None = None) -> None:
        """Bind the latest claude session id to a topic or workspace key.
        ``session_id=None`` with no model clears a stale id (resume failure)."""

        namespace = self._namespace_for(key)

        def mutate(entry: dict) -> None:
            if session_id:
                entry["session_id"] = session_id
            else:
                entry.pop("session_id", None)
            if model:
                entry["model"] = model

        # Clearing a stale id must not create a bare entry; binding a real
        # session (or a model at kickoff) does.
        self._mutate(
            key, mutate, namespace=namespace,
            require_existing=not (session_id or model),
        )

    def append_message(self, key: str, role: str, text: str, *, require_existing: bool = False) -> None:
        namespace = self._namespace_for(key)
        if not text:
            return

        def mutate(entry: dict) -> None:
            entry.setdefault("messages", []).append(
                {"role": role, "text": text, "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
            )
            del entry["messages"][:-MAX_HISTORY_MESSAGES]

        self._mutate(key, mutate, namespace=namespace, require_existing=require_existing)

    def set_workflow_state(self, ws_id: str, *, require_existing: bool = False, **fields) -> None:
        """Merge fields into a workspace's ``workflow`` sub-object (stage,
        awaiting_input, run_dir, params, ...)."""

        def mutate(entry: dict) -> None:
            workflow = entry.setdefault("workflow", {})
            workflow.update(fields)

        self._mutate(ws_id, mutate, namespace="workspaces", require_existing=require_existing)

    def link_topic(self, ws_id: str, topic_id: str) -> None:
        def mutate(entry: dict) -> None:
            entry["topic_id"] = topic_id

        self._mutate(ws_id, mutate, namespace="workspaces")

    def reset(self, key: str) -> None:
        with locks.kb_lock(self.lock_root, "wiki-chat-sessions", wait=30):
            data = self.load()
            space = data.get(self._namespace_for(key), {})
            if isinstance(space, dict) and key in space:
                del space[key]
                self._save(data)


class DialogJournal:
    """Append-only dialog transcript for one workflow workspace, persisted
    under the run dir (``<run_dir>/dialog/journal.jsonl``).

    The SSE dialog lives in the browser connection: a page refresh drops it.
    Every dialog-bearing event is mirrored here as one JSON line as it is
    streamed, so ``api/workflow/state`` can hand the transcript back and the
    frontend can rebuild the dialog after a reload.

    Record shapes (one JSON object per line):
      {"kind": "user", "text": ...}      — a user turn
      {"kind": "event", "event": {...}}  — a mirrored SSE event

    Deltas are coalesced into a small buffer (flushed at
    ``DELTA_FLUSH_CHARS`` or on any non-delta record) so a long reply does
    not become thousands of one-line writes."""

    DELTA_FLUSH_CHARS = 512

    def __init__(self, run_dir: Path):
        self.path = Path(run_dir) / "dialog" / "journal.jsonl"
        self._delta_buf: list[str] = []

    def start(self) -> None:
        """Truncate for a fresh dialog. Kickoff reuses an in-progress run dir
        on resume, but a kickoff always means a new conversation, so the old
        journal must not bleed into it."""

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._write_lines([])

    def user(self, text: str) -> None:
        self.flush_deltas()
        self._append({"kind": "user", "text": text})

    def event(self, event: dict) -> None:
        if event.get("type") == "delta":
            self._delta_buf.append(str(event.get("text") or ""))
            if sum(len(chunk) for chunk in self._delta_buf) >= self.DELTA_FLUSH_CHARS:
                self.flush_deltas()
            return
        self.flush_deltas()
        self._append({"kind": "event", "event": event})

    def flush_deltas(self) -> None:
        if not self._delta_buf:
            return
        text = "".join(self._delta_buf)
        self._delta_buf = []
        self._append({"kind": "event", "event": {"type": "delta", "text": text}})

    def _append(self, record: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record.setdefault("ts", dt.datetime.now().isoformat(timespec="seconds"))
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _write_lines(self, lines: list[str]) -> None:
        with self.path.open("w", encoding="utf-8") as fh:
            fh.writelines(lines)


def journalable_event(event: dict) -> bool:
    """True when an SSE event carries dialog content worth persisting.
    Spinner/transient state (status, progress, session ids, frame closing)
    is skipped; tool-activity status lines ARE dialog notes in the UI and
    are kept."""

    kind = event.get("type")
    if kind == "delta":
        return True
    if kind == "status":
        return event.get("stage") == "tool"
    return kind in (
        "stage", "brief", "awaiting_input", "topic_ready", "topic_error", "session_reset", "error",
    )


def read_dialog_journal(path: Path) -> list[dict]:
    """Load a journal for replay; a missing or partially written file yields
    whatever complete lines exist (last line may be torn after a crash)."""

    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError:
        return []
    records: list[dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    return records
