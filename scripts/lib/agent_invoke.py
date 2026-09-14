"""One-shot claude agent invocation + CLI discovery, shared by the pipeline
driver and the single-paper chat preparation script.

The user prompt is NEVER part of argv — it is written to stdin
(shell/quoting safety, mirroring wiki_chat.build_claude_command).
"""

from __future__ import annotations

import json
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
) -> subprocess.CompletedProcess:
    """Run one `claude -p` call with the prompt on stdin and return the
    CompletedProcess. Callers parse ``stdout`` themselves."""

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
    )


def pool_root_for(kb_root: str | Path) -> Path:
    """The shared public paper pool under the KB root (one folder per paper)."""

    return Path(kb_root).expanduser() / "pool"


SKELETON_PROMPT = """深读论文 {id}。输入（本地文件，直接 Read）：
{pool_root}/arxiv-{id}/paper.md（全文）
{pool_root}/arxiv-{id}/extraction.json（只看 sections 列表，用于 locator_hint）

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
      "quantitative": {{"metric": "英文 token", "value_or_direction": "英文 token", "comparator": "英文 token"}} 或 false}}
  ]
}}
cards ≤4；quantitative 三个字段必须用论文原文英文 token，禁止中文；无可靠定量就 false。"""


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
