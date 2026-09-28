"""Prompt templates + KB layout for spawned agents, and the compatibility
facade over the AI-invocation harness.

Everything that talks to claude (CLI discovery, spawn-environment isolation,
authentication preflight, one-shot completion, streaming turns, invocation
archiving) lives in :mod:`embodied_learning.harness.claude` — call it from new
code instead of importing the names re-exported here. This module keeps only:

- ``pool_root_for`` and the deep-read skeleton prompt/parse helpers
  (mechanical, deterministic);
- re-exports of the harness surface so existing callers
  (``from lib.agent_invoke import resolve_cli, run_one_shot_agent``) keep
  working during the migration.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parents[2]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from embodied_learning.harness.claude import (  # noqa: E401,F401
    CREDENTIALS_FILE,
    DRIVER_AGENT_MODEL,
    FALLBACK_CLI,
    ISOLATED_CONFIG_DIR,
    NESTED_CLAUDE_ENV_KEYS,
    SPAWN_ENV_MODEL_KEYS,
    STRIPPED_SPAWN_ENV_KEYS,
    ChatTurn,
    claude_auth_ready,
    complete,
    conversation_store,
    build_claude_command,
    isolated_claude_env,
    parse_stream_line,
    prepare_claude_config_dir,
    record_agent_invocation,
    resolve_cli,
    strip_nested_claude_env,
)

# Backward-compatible name: the harness primitive is complete(); historical
# callers (and tests) know run_one_shot_agent.
run_one_shot_agent = complete


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
