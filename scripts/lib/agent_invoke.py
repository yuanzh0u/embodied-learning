"""One-shot claude agent invocation + CLI discovery, shared by the pipeline
driver and the single-paper chat preparation script.

The user prompt is NEVER part of argv — it is written to stdin
(shell/quoting safety, mirroring wiki_chat.build_claude_command).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

FALLBACK_CLI = "/usr/local/bin/claude"
# The one-shot agents run outside any session: pin a fast model, otherwise the
# CLI default (opus) makes even a tiny structured-output call exceed 2 minutes.
DRIVER_AGENT_MODEL = "glm-5.3-flash"

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
# Isolated config dir for spawned agents: a per-user scratch, never inside a
# run dir (run dirs get registered in the catalog and may be synced — no
# credentials there). Redirecting CLAUDE_CONFIG_DIR hides the launcher's
# memory/projects/settings/user-CLAUDE.md from the spawned agent, which is the
# whole point: headless pipeline agents must work from the KB + packaged files
# only, not from whatever machine they happen to run on.
ISOLATED_CONFIG_DIR = Path.home() / ".cache" / "embodied-learning" / "claude-config"
CREDENTIALS_FILE = Path.home() / ".claude" / ".credentials.json"


def strip_nested_claude_env(env: dict[str, str] | None = None) -> dict[str, str]:
    """Copy of the environment without nested-claude session markers and
    shell-profile subagent-model overrides (see SPAWN_ENV_MODEL_KEYS)."""
    source = dict(os.environ) if env is None else dict(env)
    for key in NESTED_CLAUDE_ENV_KEYS + SPAWN_ENV_MODEL_KEYS:
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
    whether that degrades or fails). Mirrors wiki_chat.resolve_cli's lookup."""

    candidates = [cli] if cli else []
    candidates += ["claude", FALLBACK_CLI]
    for candidate in candidates:
        found = shutil.which(str(Path(candidate).expanduser()))
        if found:
            return found
    return None


def run_one_shot_agent(
    prompt: str,
    *,
    timeout_s: float,
    cli: str | None = None,
    model: str = DRIVER_AGENT_MODEL,
    permission_mode: str | None = "bypassPermissions",
    cwd: str | Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """Run one `claude -p` call with the prompt on stdin and return the
    CompletedProcess. Callers parse ``stdout`` themselves. ``env`` defaults to
    the isolated spawn environment (see isolated_claude_env); ``cwd`` should
    be the KB root so the agent sees no repo CLAUDE.md and a clean project
    scope."""
    command = [cli, "-p", "--model", model]
    if permission_mode:
        command += ["--permission-mode", permission_mode]
    return subprocess.run(
        command,
        input=prompt,
        text=True,
        capture_output=True,
        timeout=timeout_s,
        check=False,
        cwd=str(cwd) if cwd is not None else None,
        env=isolated_claude_env() if env is None else env,
    )


def pool_root_for(kb_root: str | Path) -> Path:
    """The shared public paper pool under the KB root (one folder per paper)."""

    return Path(kb_root).expanduser() / "pool"


SKELETON_PROMPT = """深读论文 {id}。输入（本地文件，直接 Read）：
{pool_root}/arxiv-{id}/paper.md（全文）
{pool_root}/arxiv-{id}/extraction.json（看 sections 列表定位，另看 figures/tables 清单——
每条含 id/题注/所在节，图带 image_url）

任务：通读后输出速记骨架（只输出一个 JSON 对象，不要写文件不要跑命令）：
{{
  "arxiv_id": "{id}",
  "paper_type": "method|system|dataset|survey|analysis|benchmark 之一",
  "relevance_reason": "…", "research_question": "…",
  "contributions": ["≤5"], "method_summary": "…",
  "findings": ["1-2"], "limitations": ["1-2"], "transfer_boundary": "…",
  "cards": [
    {{"claim": "中文主张", "stance": "support|limit|conditional|gap",
      "evidence_type": "method|experiment|dataset|claim|analysis",
      "quote": "正文节（非 Abstract/References）逐字英文整句",
      "locator_hint": "节标题关键词",
      "figure_id": "S4.F2 或缺省", "table_id": "S5.T1 或缺省",
      "figure_usage": "这张图/表对该主张的支撑作用，中文一句话，选了 id 就必填",
      "quantitative": {{"metric": "英文 token", "value_or_direction": "英文 token", "comparator": "英文 token"}} 或 false}}
  ]
}}
cards ≤4；quantitative 三个字段必须用论文原文英文 token，禁止中文；无可靠定量就 false。
figure_id/table_id 只从 extraction.json 的 figures/tables 清单里选，必须与某条主张直接相关
（方法流程图、系统结构图、数据采集/对比图优先；Abstract 区的 teaser 和纯 logo 不选）；
最多 2 张/篇，宁缺毋滥；id 只抄清单里的原值，不要编造。"""


def build_skeleton_prompt(paper_id: str, pool_root: Path) -> str:
    return SKELETON_PROMPT.format(id=paper_id, pool_root=str(pool_root))


def read_skeleton_output(raw: str) -> dict | None:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) and payload.get("cards") is not None else None
