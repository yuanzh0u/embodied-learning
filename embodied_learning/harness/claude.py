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
import urllib.error
import urllib.request
from pathlib import Path
from embodied_learning import ratelimit
from embodied_learning.config import (
    AGENT_SESSION_LEDGER_ENV,
    AGENT_SESSION_LOG_ENV,
    SESSION_EVENT_TEXT_MAX_CHARS,
    STOP_GRACE_S,
    SYSTEM_ONE_BACKOFF_BASE,
    SYSTEM_ONE_ENDPOINT_SUFFIX,
    SYSTEM_ONE_KEY_ENV,
    SYSTEM_ONE_KEY_FALLBACK_ENVS,
    SYSTEM_ONE_MODEL,
    SYSTEM_ONE_RETRIES,
    SYSTEM_ONE_TIMEOUT_S,
    SYSTEM_ONE_URL_ENV,
    SYSTEM_ONE_URL_FALLBACK_ENVS,
    TOOL_COMMAND_DETAIL_MAX_CHARS,
    TOOL_DETAIL_MAX_CHARS,
    TOOL_OUTPUT_MAX_CHARS,
    TOOL_OUTPUT_STAGES,
    TOOL_OUTPUT_TOOLS,
    TOOL_REASON_CARRIED_MAX_CHARS,
    TOOL_REASON_MAX_CHARS,
    TOOL_STAGE_RULES,
)
from embodied_learning.harness.session_log import (
    SessionLog,
    canonical_usage,
    usage_totals,
)

# ---- constants ------------------------------------------------------------

FALLBACK_CLI = "/usr/local/bin/claude"
# One-shot calls request the JSON envelope so usage/cost/session metadata is
# available for the session ledger; ``complete()`` unwraps ``result`` so every
# caller keeps its plain-text stdout contract.
ONE_SHOT_OUTPUT_FORMAT = "json"
# The one-shot agents run outside any session: pin a fast model, otherwise the
# CLI default (opus) makes even a tiny structured-output call exceed 2 minutes.
DRIVER_AGENT_MODEL = "glm-5.3-flash"
DEFAULT_PERMISSION_MODE = "bypassPermissions"
# Stream-truncation fallback model ( 2026-10-20, mirrors monica's
# core.fallback_model): the dmxapi glm upstream cuts the response mid-stream
# (no terminal frame) and same-model retry is a coin flip — switching the
# --model name on the same gateway is the escape (probe: deepseek-v4.1-flash
# -1017 landed 6/6 while glm failed 5/6). Empty string disables the switch
# and keeps the plain same-model retry.
STREAM_FALLBACK_MODEL = "deepseek-v4.1-flash-1017"
# Truncation detection keywords — the gateway's own error text, exactly as it
# arrives (the message must not be reworded: problem-card fingerprints hash
# the wording). Retry budget/backoff mirror monica's harness.
STREAM_TRUNCATION_KEYWORDS = ("upstream stream ended", "without a terminal frame",
                              "response is truncated")
STREAM_RETRIES = 2         # retries after the first attempt (same as monica)
STREAM_BACKOFF_BASE = 2.0  # first retry wait, then x2 (2s -> 4s)
# Grace before SIGKILL after a requested stop (ChatTurn).

# Workflow markers the agent prints as standalone lines. They are stripped
# from narration before it becomes a tool-call reason, otherwise the journal
# reads "原因：[STAGE:packet] 综述包已就绪…" on a writing-stage edit.
_STAGE_MARKER_RE = re.compile(r"\[STAGE:[a-z_]+\]")
_TOPIC_MARKER_RE = re.compile(r"\[TOPIC:[^\]]*\]")

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


def session_log_path(kind: str, label: str = "") -> Path:
    """Ledger file for one agent invocation/session.

    ``<store>/usage-<kind>-<YYYYMMDD>-<HHMMSS>-<pid>-<label>.jsonl`` — one file
    per invocation/session. It sits DIRECTLY in the store root on purpose:
    monica attributes a session by ``path.parent.name``, and a dated subfolder
    would make the project name a date (归属退化为杂项). The store dir itself
    is ``embodied-learning-work``, which repo-matches W-ai-dev. The label keeps
    a cost row traceable to a paper/run without opening the file.

    A parent process that already owns a run ledger exports
    ``EMBODIED_AGENT_LEDGER=<path>``; spawned stage scripts then append their
    agent calls to that same file (one trajectory + one bill per run) instead
    of opening a sibling ledger."""

    inherited = os.environ.get(AGENT_SESSION_LEDGER_ENV, "").strip()
    if inherited:
        return Path(inherited).expanduser()
    store = conversation_store()
    now = dt.datetime.now()
    stem = (
        f"usage-{kind}-{now.strftime('%Y%m%d-%H%M%S')}-"
        f"{os.getpid()}-{_slugify(label)}"
    )
    return store / f"{stem}.jsonl"


def open_session_log(kind: str, label: str = "") -> SessionLog | None:
    """Best-effort ledger open: recording must never break the agent call."""

    try:
        return SessionLog(session_log_path(kind, label))
    except OSError:
        return None


def session_ledger_enabled() -> bool:
    """Kill switch for the usage/trace ledger (``EMBODIED_AGENT_SESSION_LOG``)."""

    return os.environ.get(AGENT_SESSION_LOG_ENV, "").strip().lower() not in {
        "0", "false", "no", "off",
    }


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
    usage: dict | None = None,
) -> Path | None:
    """Archive one claude invocation: per-call folder (prompt/output/meta) plus
    a line in ``invocations.jsonl``. ``usage`` (the CLI result envelope, when
    available) is folded into the metadata so the index doubles as a local
    cost ledger. Best-effort — recording must never break the agent call it
    wraps, so any storage failure returns None."""

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
        if usage is not None:
            meta.update(
                {
                    "session_id": usage.get("session_id"),
                    "num_turns": usage.get("num_turns"),
                    "cost_usd": usage.get("total_cost_usd"),
                    "usage": usage_totals(_usage_record_from_envelope(usage, model or "")),
                }
            )
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


def warn_timeout(what: str, timeout_s: float, label: str = "") -> None:
    """Every agent-call timeout must be loud. A silent timeout is
    indistinguishable from an ordinary failure downstream, so the budget
    problem stays invisible (2026-10-14: a 900s smart-selection chunk timeout
    quietly dropped half a candidate registry and starved the evidence floor).

    stderr only — callers parse ``complete()``'s stdout as their payload."""

    where = f" [{label}]" if label else ""
    print(f"[WARN] timeout{where}: {what} exceeded {timeout_s:.0f}s", file=sys.stderr, flush=True)


# ---- result envelope / ledger helpers --------------------------------------


def parse_result_envelope(stdout: str) -> dict | None:
    """Parse the ``--output-format json`` envelope from a one-shot call.

    The CLI may print warnings before the JSON object, so scan backwards for
    the last line that parses. Returns None for plain-text output (older CLI,
    mocked runs) — callers then keep the raw stdout."""

    for line in reversed((stdout or "").strip().splitlines()):
        stripped = line.strip()
        if not stripped.startswith("{"):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and payload.get("type") == "result":
            return payload
    return None


def is_stream_truncation(text: str) -> bool:
    """True for the gateway's stream-truncation error (no terminal frame).

    Mirrors monica's harness classifier; the retry loop in ``complete()`` and
    ``ChatTurn`` switches to ``STREAM_FALLBACK_MODEL`` when this fires."""

    lowered = (text or "").lower()
    return any(k in lowered for k in STREAM_TRUNCATION_KEYWORDS)


def _usage_record_from_envelope(envelope: dict, default_model: str) -> list[dict]:
    """Authoritative per-model usage from a result envelope.

    ``modelUsage`` aggregates every turn of the invocation (including tool
    turns), so it is preferred over the top-level ``usage`` (which describes
    only the final turn). Falls back to the top-level usage when the CLI does
    not report per-model totals — attributed to ``default_model`` (the model
    the caller asked for; NOT the stream-truncation fallback)."""

    records: list[dict] = []
    model_usage = envelope.get("modelUsage")
    if isinstance(model_usage, dict):
        for model, raw in model_usage.items():
            if not isinstance(raw, dict):
                continue
            usage = {
                "input_tokens": raw.get("inputTokens"),
                "output_tokens": raw.get("outputTokens"),
                "cache_read_input_tokens": raw.get("cacheReadInputTokens"),
                "cache_creation_input_tokens": raw.get("cacheCreationInputTokens"),
            }
            records.append({
                "model": str(model),
                "usage": canonical_usage(usage),
                "cost_usd": raw.get("costUSD"),
            })
    if not records and isinstance(envelope.get("usage"), dict):
        records.append({
            "model": default_model,
            "usage": canonical_usage(envelope.get("usage")),
            "cost_usd": envelope.get("total_cost_usd"),
        })
    return records


def _write_envelope_to_ledger(
    log: SessionLog,
    envelope: dict,
    *,
    model: str,
    label: str,
    duration_s: float,
    returncode: int | None,
) -> None:
    """Emit the usage + metric lines for one finished invocation."""

    records = _usage_record_from_envelope(envelope, model)
    # Dedup key: readers keep one row per message.id (largest output). A
    # retried agent reuses the same label, so the label alone would collapse
    # two real invocations into one bill — the CLI's session id is unique per
    # invocation and keeps every retry countable.
    invocation_id = str(envelope.get("session_id") or f"{label}-{time.monotonic_ns()}")
    for index, record in enumerate(records):
        log.usage(
            usage=record["usage"],
            model=record["model"],
            msg_id=f"{invocation_id}:{index}",
            attrs={
                "stage": label or "agent",
                "duration_s": round(duration_s, 3),
                "cost_usd": record.get("cost_usd"),
                "returncode": returncode,
                "num_turns": envelope.get("num_turns"),
                "session_id": envelope.get("session_id"),
                "is_error": bool(envelope.get("is_error")),
            },
        )
    log.metric(
        label or "agent",
        duration_s,
        model=model,
        returncode=returncode,
        cost_usd=envelope.get("total_cost_usd"),
        num_turns=envelope.get("num_turns"),
        session_id=envelope.get("session_id"),
        is_error=bool(envelope.get("is_error")),
        terminal_reason=envelope.get("terminal_reason"),
    )


def _last_result_from_stream(path: str | Path, offset: int = 0) -> dict | None:
    """Last ``type=result`` line written to a stream-json file after ``offset``."""

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            handle.seek(offset)
            tail = handle.read()
    except OSError:
        return None
    for line in reversed(tail.splitlines()):
        stripped = line.strip()
        if not stripped.startswith("{"):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and payload.get("type") == "result":
            return payload
    return None


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
    ledger: SessionLog | None = None,
    fallback_model: str | None = None,
) -> subprocess.CompletedProcess:
    """One `claude -p` call with the prompt on stdin; returns a CompletedProcess
    whose ``stdout`` is the plain-text result the caller parses (NOT
    stream-json; use ChatTurn for streaming).

    Without ``stream`` the CLI is asked for ``--output-format json`` and the
    envelope is unwrapped here, so usage/cost/session metadata can be recorded
    while every caller keeps its plain-text contract. With ``stream=True`` the
    command switches to ``--output-format stream-json --verbose`` and, when
    ``stream_to`` (a writable file object) is given, the transcript is written
    there instead of captured in memory; the ledger still gets the final
    result envelope from the tail of that file.

    Stream truncation (the upstream cut the dmxapi glm link is prone to,
    2026-10-20) retries with backoff and switches to ``fallback_model`` —
    same gateway, different ``--model`` name (default ``STREAM_FALLBACK_MODEL``).
    Pass ``fallback_model=""`` to keep the plain same-model retry. Every
    attempt is archived and billed on its own; the caller sees the last one.

    ``env`` defaults to the isolated spawn environment; ``cwd`` should be the
    KB root so the agent sees no repo CLAUDE.md and a clean project scope.
    Every invocation is archived in the conversation store (``label``
    identifies it, e.g. paper id / run name) and, unless disabled, recorded in
    the usage/trace ledger (``usage-<kind>-<date>-<time>-<pid>-<label>.jsonl``).
    Pass ``ledger`` to append into an existing session file instead (the
    pipeline driver keeps ONE file for the whole run); the caller then owns
    closing it.
    """

    owns_ledger = ledger is None
    if ledger is None and session_ledger_enabled():
        ledger = open_session_log("one-shot", label)
    if ledger is not None:
        ledger.step(label or "one-shot", model=model, cwd=str(cwd) if cwd else "")

    stream_fallback = STREAM_FALLBACK_MODEL if fallback_model is None else fallback_model
    current_model = model
    stream_offset = 0
    stream_path: Path | None = None
    if stream_to is not None:
        stream_path = Path(getattr(stream_to, "name", "")) if getattr(stream_to, "name", None) else None
        try:
            stream_offset = stream_to.tell()
        except (AttributeError, OSError, ValueError):
            stream_offset = 0

    result: subprocess.CompletedProcess | None = None
    for attempt in range(1, 2 + STREAM_RETRIES):
        if attempt > 1:
            time.sleep(STREAM_BACKOFF_BASE * (2 ** (attempt - 2)))
            if stream_fallback and stream_fallback != current_model:
                current_model = stream_fallback

        if stream:
            command = build_claude_command(
                cli=cli,
                model=current_model,
                permission_mode=permission_mode,
                system_prompt=system_prompt,
            )
        else:
            command = [cli, "-p", "--model", current_model, "--output-format", ONE_SHOT_OUTPUT_FORMAT]
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
            duration_s = time.monotonic() - begun
            warn_timeout("one-shot agent call", timeout_s, label)
            partial = exc.stdout if isinstance(exc.stdout, str) else ""
            record_agent_invocation(
                kind="one-shot", label=label, prompt=prompt,
                stdout=partial,
                stderr=str(exc.stderr or "")[-20000:],
                returncode=None, cwd=cwd, model=current_model,
                duration_s=duration_s,
            )
            if ledger is not None:
                ledger.error(
                    f"timeout after {timeout_s:.0f}s",
                    stage=label or "one-shot",
                    exit_code=None,
                    model=current_model,
                    timeout_s=timeout_s,
                    duration_s=round(duration_s, 3),
                )
                if owns_ledger:
                    ledger.close()
            raise
        except OSError:
            # Spawn failure (missing CLI, permission): never leak the ledger we
            # opened — the caller may retry and would otherwise append to a file
            # nobody closes.
            if ledger is not None and owns_ledger:
                ledger.error(
                    "agent spawn failed", stage=label or "one-shot", model=current_model,
                    duration_s=round(time.monotonic() - begun, 3),
                )
                ledger.close()
            raise
        duration_s = time.monotonic() - begun

        # Envelope: plain JSON in non-stream mode, last result line of the stream
        # file (or of the captured stdout) in stream mode.
        envelope: dict | None = None
        if not stream:
            envelope = parse_result_envelope(result.stdout or "")
            if envelope is not None:
                result.stdout = str(envelope.get("result") or "")
        elif stream_path is not None:
            envelope = _last_result_from_stream(stream_path, stream_offset)
        else:
            envelope = parse_result_envelope(result.stdout or "")

        record_agent_invocation(
            kind="one-shot", label=label, prompt=prompt,
            stdout=result.stdout or "", stderr=result.stderr or "",
            returncode=result.returncode, cwd=cwd, model=current_model,
            duration_s=duration_s,
            usage=envelope,
        )
        if ledger is not None:
            if envelope is not None:
                _write_envelope_to_ledger(
                    ledger, envelope, model=current_model, label=label,
                    duration_s=duration_s, returncode=result.returncode,
                )
            else:
                ledger.metric(
                    label or "one-shot", duration_s, model=current_model,
                    returncode=result.returncode,
                )
            if result.returncode:
                ledger.error(
                    f"agent exit {result.returncode}",
                    stage=label or "one-shot",
                    exit_code=result.returncode,
                    model=current_model,
                    duration_s=round(duration_s, 3),
                )

        # Truncation surfaces as the gateway's own error text in the envelope
        # result and/or stderr — match the wording regardless of returncode.
        surfaces = [result.stdout or "", result.stderr or ""]
        if envelope is not None:
            surfaces.append(str(envelope.get("result") or ""))
        if not any(is_stream_truncation(t) for t in surfaces):
            break

    if ledger is not None and owns_ledger:
        ledger.close()
    return result


# ---- decision model: System One (jev) --------------------------------------
#
# The second binding beside the claude CLI. jev is not a language model: it
# answers a set of TYPED questions about one state (Choice / Score / Noul) and
# returns probabilities, so it speaks TypeSafe's System One protocol — never
# the OpenAI chat or Anthropic messages endpoints (both answer
# "is an evaluation model, not a language model"). Everything about the wire
# lives here; callers pass a state and a question map and get the answers back.

SYSTEM_ONE_TRANSIENT_CODES = frozenset({429, 500, 502, 503, 504})


class SystemOneError(RuntimeError):
    """A decision-model call that could not be completed (no key, non-200,
    malformed payload). Callers degrade to a coverage gap like a failed chunk."""


def _configured_value(
    env: dict[str, str] | None, primary: str, fallbacks: tuple[str, ...]
) -> str:
    source = os.environ if env is None else env
    for key in (primary, *fallbacks):
        value = str(source.get(key) or "").strip()
        if value:
            return value
    return ""


def resolve_system_one_endpoint(env: dict[str, str] | None = None) -> str | None:
    """Full System One URL, or None when no base URL is configured.

    ``EMBODIED_SYSTEM_ONE_URL`` is the complete endpoint; otherwise the
    gateway base URL the claude CLI already uses gets the protocol suffix.
    The key/value never come from config files — environment only."""

    explicit = str((os.environ if env is None else env).get(SYSTEM_ONE_URL_ENV) or "").strip()
    if explicit:
        return explicit
    base = _configured_value(env, "", SYSTEM_ONE_URL_FALLBACK_ENVS)
    if not base:
        return None
    if base.rstrip("/").endswith(SYSTEM_ONE_ENDPOINT_SUFFIX):
        return base.rstrip("/")
    return base.rstrip("/") + SYSTEM_ONE_ENDPOINT_SUFFIX


def resolve_system_one_key(env: dict[str, str] | None = None) -> str | None:
    """Bearer key for the decision model, or None when unconfigured."""

    key = _configured_value(env, SYSTEM_ONE_KEY_ENV, SYSTEM_ONE_KEY_FALLBACK_ENVS)
    return key or None


def system_one_ready(env: dict[str, str] | None = None) -> bool:
    """True when both an endpoint and a key are resolvable — the decision-model
    strategy's preflight (mirrors :func:`claude_auth_ready`)."""

    return bool(resolve_system_one_endpoint(env) and resolve_system_one_key(env))


def judge_questions(
    state: str,
    questions: dict[str, dict],
    *,
    model: str = SYSTEM_ONE_MODEL,
    timeout_s: float = SYSTEM_ONE_TIMEOUT_S,
    env: dict[str, str] | None = None,
    label: str = "",
    ledger: SessionLog | None = None,
) -> dict:
    """One System One request: ``questions`` maps a caller-chosen name to
    ``{"type": "noul"|"choice"|"score", ...}``. Returns the decoded payload
    (``answers`` + ``usage``).

    Transient rejections retry with backoff; every attempt archives through
    :func:`record_agent_invocation` (kind ``system-one``) and writes usage to
    the ledger, so decision-model cost lands in the same bill as claude calls.
    Raises :class:`SystemOneError` when no attempt lands."""

    endpoint = resolve_system_one_endpoint(env)
    key = resolve_system_one_key(env)
    if not endpoint or not key:
        raise SystemOneError(
            "决策模型未配置：需要 "
            f"{SYSTEM_ONE_URL_ENV}（或 {SYSTEM_ONE_URL_FALLBACK_ENVS[0]}）"
            f" 与 {SYSTEM_ONE_KEY_ENV}（或 {SYSTEM_ONE_KEY_FALLBACK_ENVS[0]}）"
        )
    body = json.dumps(
        {"model": model, "state": state, "questions": questions},
        ensure_ascii=False,
    )
    # Same ledger contract as complete(): a caller that owns the run ledger
    # passes it in; otherwise open one so decision-model spend is never
    # invisible (the driver exports EMBODIED_AGENT_LEDGER to stage scripts).
    owns_ledger = ledger is None
    if ledger is None and session_ledger_enabled():
        ledger = open_session_log("system-one", label)
    if ledger is not None:
        ledger.step(label or "system-one", model=model)

    def _close_if_owned() -> None:
        if owns_ledger and ledger is not None and not ledger.closed:
            ledger.close()

    last_error = ""
    for attempt in range(1, 1 + SYSTEM_ONE_RETRIES):
        if attempt > 1:
            time.sleep(SYSTEM_ONE_BACKOFF_BASE * (2 ** (attempt - 2)))
        request = urllib.request.Request(
            endpoint,
            data=body.encode("utf-8"),
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        begun = time.monotonic()
        try:
            with ratelimit.gated_urlopen(
                request, group="systemone", timeout=timeout_s
            ) as response:
                raw = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            duration_s = time.monotonic() - begun
            detail = ""
            try:
                detail = exc.read().decode("utf-8", errors="replace")[:2000]
            except (OSError, ValueError):
                pass
            last_error = f"HTTP {exc.code}: {detail or exc.reason}"
            record_agent_invocation(
                kind="system-one", label=label, prompt=body, stdout=detail,
                stderr=last_error, returncode=exc.code, model=model,
                duration_s=duration_s,
            )
            if ledger is not None:
                ledger.error(
                    f"system-one HTTP {exc.code}", stage=label or "system-one",
                    exit_code=exc.code, model=model,
                    duration_s=round(duration_s, 3),
                )
            if exc.code not in SYSTEM_ONE_TRANSIENT_CODES:
                _close_if_owned()
                raise SystemOneError(last_error) from exc
            continue
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            duration_s = time.monotonic() - begun
            last_error = f"{type(exc).__name__}: {exc}"
            record_agent_invocation(
                kind="system-one", label=label, prompt=body, stdout="",
                stderr=last_error, returncode=None, model=model,
                duration_s=duration_s,
            )
            if ledger is not None:
                ledger.error(
                    last_error, stage=label or "system-one", model=model,
                    duration_s=round(duration_s, 3),
                )
            continue
        duration_s = time.monotonic() - begun
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            last_error = f"malformed System One payload: {raw[:400]}"
            record_agent_invocation(
                kind="system-one", label=label, prompt=body, stdout=raw[:20000],
                stderr=last_error, returncode=0, model=model, duration_s=duration_s,
            )
            _close_if_owned()
            raise SystemOneError(last_error) from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("answers"), dict):
            last_error = f"System One payload without answers: {raw[:400]}"
            record_agent_invocation(
                kind="system-one", label=label, prompt=body, stdout=raw[:20000],
                stderr=last_error, returncode=0, model=model, duration_s=duration_s,
            )
            _close_if_owned()
            raise SystemOneError(last_error)
        usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}
        record_agent_invocation(
            kind="system-one", label=label, prompt=body, stdout=raw[:20000],
            returncode=0, model=str(payload.get("model") or model),
            duration_s=duration_s,
            usage={"usage": usage, "session_id": f"system-one:{label or model}"},
        )
        if ledger is not None:
            ledger.usage(
                usage=usage,
                model=str(payload.get("model") or model),
                msg_id=f"system-one:{label or model}:{time.monotonic_ns()}",
                attrs={
                    "stage": label or "system-one",
                    "duration_s": round(duration_s, 3),
                    "questions": len(questions),
                },
            )
            ledger.metric(label or "system-one", duration_s, model=str(payload.get("model") or model))
        _close_if_owned()
        return payload

    if ledger is not None:
        ledger.error(
            f"system-one failed after {SYSTEM_ONE_RETRIES} attempts: {last_error}",
            stage=label or "system-one",
        )
    _close_if_owned()
    raise SystemOneError(last_error or "System One call failed")


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


def parse_stream_line(
    line: str,
    *,
    prior_text: str = "",
    tool_index: dict[str, dict] | None = None,
) -> list[dict]:
    """Translate one stream-json line into 0..n normalized events
    (session / delta / status / done).

    ``prior_text`` is the narration the caller last saw in this turn. A
    ``tool_use`` block carries no reason of its own, so it is attached to the
    tool event as ``reason`` — the dialog journal then answers "why was this
    file edited?" instead of only "which file" (2026-10-20 审计门).
    ``reason_source`` says whether that text came from the call's own message
    (``inline``), is the previous narration (``carried``), or the tool call
    stated no motive at all (``none``).

    ``user`` frames carrying ``tool_result`` blocks become ``tool_output``
    events: gate stdout (PASS/ERROR lines, ``run.py status`` digests) reaches
    the dialog, which otherwise showed only "正在运行" for every audit gate
    (2026-10-21 hdmap生成 / 深度图补全). ``tool_index`` maps ``tool_use_id`` →
    ``{"name": ..., "workflow_stage": ...}`` so the output line says which
    tool produced it and lands in the same workflow card."""

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
        blocks = (raw.get("message") or {}).get("content") or []
        # The reason travels in text blocks of the same message (usually
        # before the call); fall back to the previous message's narration.
        narration = " ".join(
            str(block.get("text") or "")
            for block in blocks
            if isinstance(block, dict) and block.get("type") == "text"
        )
        events: list[dict] = []
        for block in blocks:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text" and block.get("text"):
                events.append({"type": "delta", "text": block["text"]})
            elif block_type == "thinking":
                events.append({"type": "status", "stage": "thinking"})
            elif block_type == "tool_use" and block.get("name"):
                stage = _tool_stage(block)
                if tool_index is not None and block.get("id"):
                    # Remember which tool (and node) a later tool_result belongs to.
                    tool_index[str(block["id"])] = {
                        "name": str(block["name"]),
                        "workflow_stage": stage,
                    }
                reason = _tool_reason(narration, prior_text)
                event = {
                    "type": "status",
                    "stage": "tool",
                    "tool": block["name"],
                    "detail": _tool_detail(block),
                    "reason": reason,
                    # A tool-only message has no narration of its own; the
                    # reason is then the tail of the previous narration and
                    # says nothing new about THIS call. Without the marker
                    # fifteen consecutive edits looked like fifteen
                    # identical motives (2026-10-20 视频流式重建 audit loop).
                    "reason_source": _reason_source(narration, reason),
                }
                # The workflow node this call belongs to, inferred from the
                # file/command it touches. Absent = keep the announced stage.
                if stage:
                    event["workflow_stage"] = stage
                events.append(event)
        return events

    if kind == "user":
        # Tool stdout/stderr (Bash results, gate verdicts) comes back as a
        # user frame with ``tool_result`` blocks. Until 2026-10-21 these were
        # dropped, so the audit-gate card showed only "正在运行" and the writer
        # could not see in the dialog whether a gate passed.
        blocks = (raw.get("message") or {}).get("content") or []
        if not isinstance(blocks, list):
            return []
        events = []
        for block in blocks:
            if not isinstance(block, dict) or block.get("type") != "tool_result":
                continue
            origin = (tool_index or {}).get(str(block.get("tool_use_id") or ""), {})
            output = _tool_output_text(block)
            if not output:
                continue
            events.append(
                {
                    "type": "tool_output",
                    "tool": origin.get("name", ""),
                    "workflow_stage": origin.get("workflow_stage", ""),
                    "output": output,
                    "is_error": block.get("is_error") is True,
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


def _tail_text(prior: str, text: str) -> str:
    """Narration buffer for tool-call reasons — the latest narration only.

    It used to append every message's text, so a long writer turn carried
    stale recaps (and their ``[STAGE:*]`` markers) into the reason of
    unrelated edits: the 2026-10-21 hdmap run showed "首先是科研备忘录：" as
    the motive for zhihu edits. Each narration replaces the buffer instead
    and markers are stripped."""

    fresh = _narration_text(text)[-TOOL_REASON_CARRIED_MAX_CHARS:]
    return fresh or prior


def _narration_text(text: str) -> str:
    """Strip workflow markers and compact a narration for the journal."""

    cleaned = _STAGE_MARKER_RE.sub(" ", str(text or ""))
    cleaned = _TOPIC_MARKER_RE.sub(" ", cleaned)
    return " ".join(cleaned.split())


def _tool_reason(narration: str, prior_text: str) -> str:
    """The agent's stated motive for a tool call, compacted for the journal.

    Prefer the text of the same assistant message (that is where the agent
    explains the call it is about to make); fall back to the latest prior
    narration, clipped shorter because that text talks about the PREVIOUS
    call, not this one. A trailing colon is dropped — the agent's lead-in
    ("首先是科研备忘录：") otherwise reads as a truncated sentence."""

    text = _narration_text(narration or prior_text)
    if not text:
        return ""
    limit = TOOL_REASON_MAX_CHARS if narration else TOOL_REASON_CARRIED_MAX_CHARS
    if len(text) > limit:
        tail = text[-limit:]
        boundary = re.search(r"[。！？；!?;]\s*", tail)
        # Cut on the first complete sentence inside the window so the reason
        # never starts mid-clause.
        if boundary and boundary.end() < len(tail):
            tail = tail[boundary.end():]
        text = "…" + tail
    return text.rstrip("：:，,、 ")


def _reason_source(narration: str, reason: str) -> str:
    """Which narration the reason was taken from: ``inline`` (same message,
    i.e. a motive for this very call), ``carried`` (the previous narration —
    context, not a per-call motive), or ``none``."""

    if not reason:
        return "none"
    return "inline" if str(narration or "").strip() else "carried"


_TOOL_STAGE_RES = tuple((stage, re.compile(pattern)) for stage, pattern in TOOL_STAGE_RULES)


def _tool_stage(block: dict) -> str:
    """The workflow node a tool call belongs to, or "" to defer to the UI.

    The agent only emits ``[STAGE:*]`` between phases, so a long writing
    stretch used to file every write/edit/gate under whatever stage line came
    last (2026-10-21 hdmap生成: all three articles and the audit gates landed
    in 综述包). Classify by the file or command actually touched instead.

    The earliest match wins: ``audit-citations ... && run.py finalize`` is one
    shell step whose output is the gates' verdicts, so it belongs on the audit
    card, not the settle card (the server logs 已落盘 itself)."""

    target = _tool_detail(block)
    if not target:
        return ""
    best: tuple[int, str] | None = None
    for stage, pattern in _TOOL_STAGE_RES:
        match = pattern.search(target)
        if match and (best is None or match.start() < best[0]):
            best = (match.start(), stage)
    return best[1] if best else ""


def _tool_detail(block: dict) -> str:
    """Human-readable summary of a tool call input (file path / command etc.).

    ``command`` keeps essentially the whole invocation (``TOOL_COMMAND_DETAIL_MAX_CHARS``)
    because the dialog journal is the audit trail for flag-mistake diagnosis —
    a 120-char cut used to truncate ``audit-citations`` mid-flag and make real
    wrong-flag retries look like log noise. Shorter keys (paths, patterns, URLs)
    stay compact at ``TOOL_DETAIL_MAX_CHARS``; the UI may shorten further for
    the transient status spinner.
    """

    payload = block.get("input")
    if not isinstance(payload, dict):
        return ""
    for key in ("file_path", "notebook_path", "path", "pattern", "command", "url", "query"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            limit = (
                TOOL_COMMAND_DETAIL_MAX_CHARS
                if key == "command"
                else TOOL_DETAIL_MAX_CHARS
            )
            return value[:limit]
    return ""


def _tool_output_text(block: dict) -> str:
    """The visible part of a ``tool_result``: string content, or the text
    blocks of a list content. Clipped to the TAIL (``TOOL_OUTPUT_MAX_CHARS``)
    because gate verdicts land at the end of the output."""

    content = block.get("content")
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        text = "\n".join(
            str(item.get("text") or "")
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        )
    else:
        text = ""
    text = text.strip()
    if not text:
        return ""
    if len(text) > TOOL_OUTPUT_MAX_CHARS:
        text = "…" + text[-TOOL_OUTPUT_MAX_CHARS:]
    if block.get("is_error") is True and not text.startswith("ERROR"):
        text = f"退出码非 0：\n{text}"
    return text


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
        fallback_model: str | None = None,
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
        # Stream-truncation escape ( 2026-10-20, same semantic as complete()):
        # empty string disables the switch and keeps plain same-model retries.
        self.fallback_model = STREAM_FALLBACK_MODEL if fallback_model is None else fallback_model
        self.stop_requested = False
        self._queue: queue.Queue = queue.Queue()
        self._process: subprocess.Popen | None = None
        self._stderr_tail: list[str] = []
        self._stderr_truncation = False
        self._timer: threading.Timer | None = None
        self._timed_out = False
        self._peeked: dict | None = None
        self._early_exit_seen = False
        self._begun = 0.0
        self._ledger: SessionLog | None = None
        self._tool_counts: dict[str, int] = {}
        self._stream_usage: dict[str, dict] = {}  # msg id -> deduped usage
        self._result_envelope: dict | None = None

    # -- lifecycle ---------------------------------------------------------

    def _spawn_process(self) -> None:
        """Start one claude child (first run and fallback retry share this).
        Raises OSError on spawn failure — callers turn it into an error event."""

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
        self._result_envelope = None
        self._stderr_truncation = False
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
        # Prompt travels through stdin; close immediately so claude sees EOF.
        try:
            assert self._process.stdin is not None
            self._process.stdin.write(self.prompt)
            self._process.stdin.close()
        except OSError:
            pass  # the stderr/stdout readers will surface the failure
        threading.Thread(
            target=self._read_stderr, args=(self._process,), daemon=True
        ).start()

    def start(self) -> None:
        self._begun = time.monotonic()
        if session_ledger_enabled():
            self._ledger = open_session_log(
                "chat", f"{self.cwd.name}-{self.session_id or 'new'}"
            )
            if self._ledger is not None:
                self._ledger.step(
                    "chat",
                    model=self.model or "",
                    cwd=str(self.cwd),
                    session_id=self.session_id or "",
                    resumed=bool(self.session_id),
                )
        try:
            self._spawn_process()
        except OSError as exc:
            resume_failed = is_resume_failure(str(exc))
            self._record_error(f"无法启动 claude：{exc}", stage="chat-spawn")
            if self._ledger is not None:
                self._ledger.close()
            self._queue.put(
                ("error", {"type": "error", "message": f"无法启动 claude：{exc}", "resume_failed": resume_failed})
            )
            self._queue.put(("exit", None))
            return
        threading.Thread(target=self._read_stdout, daemon=True).start()
        if self.timeout_s and self.timeout_s > 0:
            self._timer = threading.Timer(self.timeout_s, self._on_timeout)
            self._timer.daemon = True
            self._timer.start()

    def _read_stdout(self) -> None:
        stream_lines: list[str] = []  # every attempt's raw frames, for the archive
        code: int | None = None
        try:
            for attempt in range(1, 2 + STREAM_RETRIES):
                held_done, code = self._read_one_attempt(stream_lines)
                if not self._truncation_retry_needed(held_done):
                    if held_done is not None:
                        self._queue.put(("event", held_done))
                    break
                # Stream truncation — switch to the fallback model and respawn
                # (same gateway, different --model name). The held done event is
                # dropped: the retry's own stream supplies the real one.
                if self.fallback_model and self.model != self.fallback_model:
                    self.model = self.fallback_model
                self._queue.put(("event", {
                    "type": "status",
                    "stage": "retry",
                    "detail": f"流断帧，已切换到 {self.model} 重试",
                }))
                time.sleep(STREAM_BACKOFF_BASE * (2 ** (attempt - 2)))
                try:
                    self._spawn_process()
                except OSError as exc:
                    self._record_error(f"重试启动失败：{exc}", stage="chat-spawn")
                    if held_done is not None:
                        self._queue.put(("event", held_done))
                    break
        finally:
            # Archive BEFORE the exit marker: consumers (events()) must be
            # able to rely on the transcript being on disk once they see the
            # turn end. Same for the ledger lines.
            self._archive_turn("".join(stream_lines), code)
            self._finish_ledger(code)
            self._queue.put(("exit", code))
        if self._timer:
            self._timer.cancel()

    def _read_one_attempt(self, stream_lines: list[str]) -> tuple[dict | None, int | None]:
        """Drain one child's stdout. Returns (held truncation-done event, exit code).

        A truncation ``done`` is held back instead of queued — the caller may
        respawn with the fallback model, and a mid-turn done event would make
        the consumer think the turn already ended."""

        assert self._process is not None and self._process.stdout is not None
        # Latest narration in this turn — the fallback "why" for a tool call
        # that arrives in its own message with no text block.
        prior_text = ""
        # tool_use_id -> {name, workflow_stage}, so a later tool_result says
        # which tool produced the output and where it belongs in the log.
        tool_index: dict[str, dict] = {}
        held_done: dict | None = None
        try:
            for line in self._process.stdout:
                stream_lines.append(line)
                self._observe_stream(line)
                for event in parse_stream_line(
                    line, prior_text=prior_text, tool_index=tool_index
                ):
                    if event.get("type") == "delta":
                        prior_text = _tail_text(prior_text, event.get("text") or "")
                    elif (
                        event.get("type") == "status"
                        and event.get("stage") == "tool"
                        and event.get("reason_source") == "carried"
                    ):
                        # The narration explained the message it followed; a
                        # tool-only message reuses it once, then the buffer is
                        # spent. Otherwise the memo's lead-in kept reappearing
                        # under zhihu/xiaohongshu edits and audit commands
                        # (2026-10-21 hdmap生成) — a motive those calls never
                        # stated. They now log `none` instead.
                        prior_text = ""
                    elif event.get("type") == "tool_output":
                        # Echo the tool's stdout into the dialog (audit gates,
                        # status digests) — capped, Bash-only, and only for the
                        # gate nodes or a failed call. An unknown origin is
                        # skipped too: file contents are not dialog.
                        if event.get("tool") not in TOOL_OUTPUT_TOOLS:
                            continue
                        if not event.get("is_error") and event.get(
                            "workflow_stage"
                        ) not in TOOL_OUTPUT_STAGES:
                            continue
                    if (
                        event.get("type") == "done"
                        and event.get("is_error")
                        and is_stream_truncation(str(event.get("result_text") or ""))
                    ):
                        held_done = event
                        continue
                    self._queue.put(("event", event))
        except (OSError, ValueError):
            pass
        # stdout EOF means the child is exiting; wait (bounded) for the
        # real exit code instead of poll(), which races process teardown
        # and would archive returncode=None.
        code = None
        if self._process is not None:
            try:
                self._process.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                # Bounded drain after stdout EOF, not a budget overrun —
                # still log it: a child that never exits is a zombie that
                # will hold the chat lock.
                warn_timeout("post-EOF exit-code drain", 5.0)
            code = self._process.poll()
        return held_done, code

    def _truncation_retry_needed(self, held_done: dict | None) -> bool:
        """True when this attempt hit a stream truncation and a retry may run.

        User stop / watchdog timeout never retry. ``fallback_model=""`` only
        disables the model SWITCH — same-model retries still apply."""

        if self.stop_requested or self._timed_out:
            return False
        return held_done is not None or self._stderr_truncation

    def _observe_stream(self, line: str) -> None:
        """Fold one stream-json line into the turn's ledger state: per-message
        usage (deduped by message id, keeping the largest output count — the
        CLI writes partial frames before the final one), tool-call counts, and
        the terminal result envelope (cost / turns / session)."""

        stripped = line.strip()
        if not stripped.startswith("{"):
            return
        try:
            raw = json.loads(stripped)
        except json.JSONDecodeError:
            return
        if not isinstance(raw, dict):
            return
        if raw.get("type") == "assistant":
            message = raw.get("message") or {}
            if not isinstance(message, dict):
                return
            usage = message.get("usage")
            if isinstance(usage, dict) and usage:
                canonical = canonical_usage(usage)
                mid = str(message.get("id") or "")
                key = mid or f"anon-{len(self._stream_usage)}"
                previous = self._stream_usage.get(key)
                if previous is None or canonical["output_tokens"] > previous["usage"]["output_tokens"]:
                    self._stream_usage[key] = {
                        "model": str(message.get("model") or self.model or ""),
                        "usage": canonical,
                        "timestamp": raw.get("timestamp"),
                    }
            for block in message.get("content") or []:
                if (
                    isinstance(block, dict)
                    and block.get("type") == "tool_use"
                    and block.get("name")
                ):
                    name = str(block["name"])
                    self._tool_counts[name] = self._tool_counts.get(name, 0) + 1
        elif raw.get("type") == "result":
            self._result_envelope = raw

    def _record_error(
        self,
        text: str,
        *,
        stage: str = "chat",
        exit_code: int | None = None,
        level: str = "error",
        **attrs: object,
    ) -> None:
        if self._ledger is None:
            return
        self._ledger.event(
            level=level,
            kind="error" if level == "error" else "warn",
            text=text[:SESSION_EVENT_TEXT_MAX_CHARS],
            stage=stage,
            exit_code=exit_code,
            **attrs,
        )

    def _finish_ledger(self, returncode: int | None) -> None:
        """Write usage lines + the turn metric/outcome and close the ledger."""

        log = self._ledger
        if log is None:
            return
        duration_s = time.monotonic() - self._begun
        for msg_id, item in self._stream_usage.items():
            ts = None
            if isinstance(item.get("timestamp"), str):
                try:
                    ts = dt.datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
                except ValueError:
                    ts = None
            log.usage(
                ts=ts,
                usage=item["usage"],
                model=item["model"],
                msg_id=msg_id,
                attrs={"stage": "chat", "session_id": self.session_id or ""},
            )
        totals = usage_totals([{"usage": item["usage"]} for item in self._stream_usage.values()])
        envelope = self._result_envelope or {}
        log.metric(
            "chat",
            duration_s,
            model=self.model or "",
            session_id=(envelope.get("session_id") or self.session_id or ""),
            returncode=returncode,
            num_turns=envelope.get("num_turns"),
            cost_usd=envelope.get("total_cost_usd"),
            tool_calls=dict(self._tool_counts),
            **totals,
        )
        if self._timed_out:
            self._record_error(
                f"chat turn timed out after {self.timeout_s:.0f}s",
                stage="chat-timeout",
            )
        elif self.stop_requested:
            self._record_error("chat turn stopped by user", stage="chat-stop", level="warn")
        elif returncode not in (0, None):
            self._record_error(
                f"claude exited with code {returncode}",
                stage="chat-exit",
                exit_code=returncode,
            )
        log.close()

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

    def _read_stderr(self, process: subprocess.Popen) -> None:
        assert process.stderr is not None
        try:
            for line in process.stderr:
                text = line.strip()
                if text:
                    self._stderr_tail.append(text)
                    del self._stderr_tail[:-20]
                    if is_stream_truncation(text):
                        self._stderr_truncation = True
        except (OSError, ValueError):
            pass

    def _on_timeout(self) -> None:
        self._timed_out = True
        warn_timeout("chat turn", self.timeout_s)
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
            warn_timeout(
                "first chat event", 120.0 if timeout_s is None else timeout_s
            )
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
