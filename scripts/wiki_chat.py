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

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.agent_invoke import conversation_store  # noqa: E402,F401  (compat re-export)
from lib.jsonio import atomic_write_json  # noqa: E402
sys.path.insert(0, str(SCRIPT_DIR.parent))  # repo root, for the embodied_learning package
from embodied_learning import locks  # noqa: E402
# All claude invocation machinery lives in the harness (pybind-style binding);
# this module keeps prompts, session registry, and HTTP glue only.
from embodied_learning.harness.claude import (  # noqa: E402,F401
    ChatTurn,
    build_claude_command,
    is_resume_failure,
    parse_stream_line,
    prepare_claude_config_dir,
)
from embodied_learning.harness.claude import resolve_cli as _harness_resolve_cli  # noqa: E402

DEFAULT_PERMISSION_MODE = "bypassPermissions"
DEFAULT_CHAT_TIMEOUT_S = 900
STOP_GRACE_S = 5.0
FIRST_EVENT_TIMEOUT_S = 120.0  # claude must show its first event within this window
MAX_HISTORY_MESSAGES = 40
MAX_PROMPT_CONTEXT_FILES = 40
# When ``claude`` is not on PATH (e.g. launched from a desktop launcher), the
# standard install location is the fallback.
FALLBACK_CLI = "/usr/local/bin/claude"


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

CHAT_SYSTEM_PROMPT = (
    "你是「空间智能研究 Wiki」的研究助手，工作目录即本地知识库根目录。"
    "evidence/ 下每个 literature-review-* 文件夹是一次研究运行：含三种成稿"
    "（scientific-memo_keyan.md、zhihu-explainer_zhihu.md、xiaohongshu-post_xiaohongshu.md）、"
    "evidence-appendix.md 与 run.json；pool/ 存放已抽取的论文全文 markdown；knowledge/ 是主题卡片。"
    "回答要基于证据：先读相关文件再下结论，引用时给出文件相对路径。"
    "用户可能请你撰写综述草稿：用 Write 把新文件写进当前话题的运行目录，文件名以 survey- 开头，"
    "不要覆盖已有成稿。用中文回答，先给中心判断，再给证据与反例。"
)

# The workflow system prompt has exactly ONE deliberate fork: the interactive
# wiki ("agent" publisher) finishes the mechanical settle itself (finalize_run.py)
# and emits [STAGE:]/[TOPIC:] markers the wiki UI parses; the headless launcher
# ("launcher" publisher) stops right after the audit gates — the launcher process
# does finalize/publish in code. Everything else (role, boundaries, judgment
# duties, stop conditions, citation contract, resume discipline) is byte-identical
# for both entry points. Prompt text lives ONLY here; both scripts/serve_research_wiki.py
# and scripts/launch_review.py compose through the factories below.
_WORKFLOW_BASE_SYSTEM_PROMPT = (
    "你是「空间智能研究 Wiki」的综述工作流执行器，工作目录即本地知识库根目录。"
    "<skills-root> 下是本仓库的技能树（每个子目录含 SKILL.md 与 scripts/），"
    "<scripts-root> 下是顶层脚本（check_run_bundle.py、audit_citations.py 等）。"
    "按照 <skills-root>/embodied-ai-review-writer/SKILL.md 的综述契约执行，"
    "SKILL.md 中出现的相对路径按其所在目录解析：路径以 skills/ 开头时替换为 <skills-root>，"
    "以 scripts/ 开头时替换为 <scripts-root>。"
    "只遵循 SKILL.md 的成稿、风格与引文契约；其「Run lifecycle and gates」里的检索、深读、"
    "投影段落以及所有手动 settle/publish 步骤（翻 run.json status、手工拷贝 evidence 资产、"
    "手工登记 catalog 表格、重建 wiki 快照并核对发布结果）已全部由系统机械化——"
    "一律跳过，更不要照着手动执行。"
    "\n\n【职责边界——固定流程已由系统完成】\n"
    "查询规划、候选检索（Semantic Scholar + arXiv）、候选注册、筛选、覆盖度评估、"
    "全文 HTML 抽取、论文深读（速记骨架+审计）与证据投影已由驱动脚本 run_review_pipeline.py 一次性完成，"
    "运行现状用 python3 <scripts-root>/run_status.py --run-dir <run-dir> 一次性读取："
    "漏斗数字、逐篇证据与 claim、References 作者/年份元数据、逐篇深读漏斗（held / deep-read-failed 及筛选命中词）、"
    "产物清单与建议命令都在它的输出里。"
    "禁止用内联 python 循环或 grep 统计 screening.json、candidate-registry.json、paper-notes/、evidence/——"
    "那是一次调用就能拿到的机械聚合；也不要读脚本源码或用 --help 探查参数。"
    "不要手动执行任何检索/抽取/筛选/深读/投影命令（search.py search-arxiv、search.py search-semantic-scholar、"
    "search.py build-candidate-registry、search.py screen-candidates、search.py assess-review-coverage、"
    "fetch.py extract-content-queue、build_reading_packet.py、build_paper_note.py、"
    "note_tools.py project-evidence-events、run_review_pipeline.py）"
    "——重复执行只会浪费时长且可能触发限流。若 summary 显示维度、地板或深读未过，如实向用户说明，不要自行补救检索。"
    "\n\n【你的判断职责】\n"
    "1. 论文深读与证据投影：已由系统驱动脚本完成（速记骨架 + 审计 + 投影）。"
    "不要派发深读 subagent、不要跑 note_tools.py project-evidence-events；"
    "若 pipeline-summary.json 的 deep_read 字段显示失败篇目，如实说明。\n"
    "2. 综述包与成稿：跑 <skills-root>/embodied-ai-review-writer/scripts/build_review_packet.py "
    "生成综述包（review-packet 是简报不是成稿），然后亲自撰写成稿、生成 trace-map.json；"
    "成稿必须落图：writing-brief 的「可用图表」段给出带图的证据事件与现成 markdown 块，"
    "按各风格配额把图插到所支撑的段落之后（图源只能是 evidence 携带的图，URL/题注照抄，禁止自造图片）。\n"
    "3. 审计门：逐一通过 <scripts-root>/check_run_bundle.py、<scripts-root>/audit_citations.py、"
    "<skills-root>/embodied-ai-review-writer/scripts/writing_audit.py audit-article-quality "
    "（加 --evidence-jsonl 以启用带图可用但成稿未落图的告警）；"
    "审计门全过之前不要把证据落盘到 evidence/。"
    "\n\n【唯一允许提前停止的条件】\n"
    "检索失败或文献不足：pipeline-summary.json 显示检索通道整体失败、coverage/saturation 未过、"
    "或验收证据不足以支撑目标风格的成稿。此时停下并如实说明缺什么，把 run 留在 in-progress。"
    "除此之外不要因大纲确认、风格选择等原因中途停轮等待用户——综述从综述包到 settle 一轮写完。"
    "\n\n【科研备忘录（scientific-memo_keyan.md）引文格式（Wiki 渲染依赖，必须遵守）】\n"
    "正文引用用上标编号，每条引用单独一个标记、带方括号：单条 ^[1]^；多条时逐条并列写成 "
    "^[1]^ ^[2]^ ^[3]^，严禁把多个编号塞进同一个标记（^[1,2,3]^ 是格式错误）。"
    "文末「参考文献」编号列表：编号对应正文上标，每条列出论文名称（英文原题）、"
    "作者（第一作者 et al.）、年份，并附 arXiv 链接（[arXiv:2602.11323](https://arxiv.org/abs/2602.11323) 形式）"
    "——Wiki 构建时会按这条链接把正文上标解析成可点击的阅读链接。"
    "除参考文献列表外，正文叙述中不要出现 arxiv.org 链接或 [arXiv:2402.xxxxx] 式前缀"
    "——但 ![](https://arxiv.org/html/...) 图片 URL 例外：它是图源，不是叙述性链接，按图表规范正常使用。"
    "知乎版与小红书版不受此约束（沿用各自的宽松风格）。"
    "\n\n若指定的运行目录已存在中间产物（extractions/、paper-notes/ 等），从磁盘已有进度继续"
    "（已通过审计的笔记直接复用，不要重读重写），只补缺失部分。"
    "除落盘阶段外只写入 <work-dir> 运行目录；用中文与用户交流。"
)

_WORKFLOW_AGENT_TAIL = (
    "\n\n【机械落盘由你收尾】\n"
    "审计门全过后，用 python3 <scripts-root>/finalize_run.py --run-dir <run-dir> --kb-root <kb-root> "
    "一步完成机械落盘：补齐 run.json 字段（含单风格时的 style/scope_note）、复跑两道门、拷贝 evidence/<run>/、"
    "翻 settled、登记 catalog、重建 wiki 快照——这些全是 finalize_run.py 的机械职责，"
    "不要手改 run.json，也不要再手动跑登记表格或重建快照的脚本、逐项核对 wiki 端口的发布结果。"
    "finalize_run.py 门禁不过时会机械打印缺失项：按提示修复后重跑 finalize 即可，门禁未过不是提前停止的理由。"
    "\n\n在开始每个阶段前，先单独输出一行阶段标记（普通文本，不要放进代码块）："
    "[STAGE:mining] / [STAGE:packet] / [STAGE:writing] / [STAGE:audit] / [STAGE:settle]，后跟一句话进度说明。"
    "落盘到 evidence/ 后，在最终回复的单独一行输出 "
    "[TOPIC:<evidence/ 下新运行目录的相对路径>]，不要带其他后缀。"
)

_WORKFLOW_LAUNCHER_TAIL = (
    "\n\n【机械落盘与发布不归你】\n"
    "通过全部审计门后【立即停止本轮回复】，不要再做任何落盘或发布动作："
    "finalize_run.py、run.json 盖章、evidence/ 落盘拷贝、catalog 登记、"
    "wiki 快照重建与 publish 校验由 launcher 在你停止后机械完成，"
    "不要执行这些脚本、不要手改 run.json。"
    "成稿文件按目标风格直接写在运行目录根"
    "（scientific-memo_keyan.md / zhihu-explainer_zhihu.md / xiaohongshu-post_xiaohongshu.md / survey-*.md），"
    "trace-map.json 与 evidence-appendix.md 同样落在运行目录根，"
    "launcher 会从那里取件做门禁与发布。不需要输出任何阶段或话题标记。"
)


def workflow_system_prompt(publisher: str = "agent") -> str:
    """Workflow system prompt: shared base + the one deliberate fork.

    ``publisher="agent"``（交互 wiki 面）让代理自己跑 finalize_run.py 收尾，
    并要求输出 wiki UI 解析的 [STAGE:]/[TOPIC:] 标记；``publisher="launcher"``
    （headless writer）在审计门后立即停止——机械落盘/发布由 launcher 在代码里做。
    """
    if publisher == "agent":
        return _WORKFLOW_BASE_SYSTEM_PROMPT + _WORKFLOW_AGENT_TAIL
    if publisher == "launcher":
        return _WORKFLOW_BASE_SYSTEM_PROMPT + _WORKFLOW_LAUNCHER_TAIL
    raise ValueError(f"unknown workflow publisher: {publisher}")


# Compatibility alias: the interactive call sites and existing tests read this
# name; it is always the interactive ("agent") variant.
WORKFLOW_SYSTEM_PROMPT = workflow_system_prompt("agent")


def resolve_pipeline_layout(pipeline_root: Path) -> tuple[Path, Path]:
    """Given the pipeline root, return (skills_root, scripts_root).

    Three shapes: repo checkout (``<root>/skills`` + ``<root>/scripts``), wheel
    install where the root IS the scripts package dir (contains ``init_run.py``
    and the bundled ``skills/``), and a bare skills/ root (the wheel's
    ``wiki_scripts/skills`` — its parent holds the scripts)."""

    skills_root = pipeline_root if pipeline_root.name == "skills" else pipeline_root / "skills"
    if (pipeline_root / "scripts" / "init_run.py").is_file():
        scripts_root = pipeline_root / "scripts"
    elif (pipeline_root / "init_run.py").is_file():
        scripts_root = pipeline_root  # installed: the wiki_scripts dir itself
    elif pipeline_root.name == "skills" and (pipeline_root.parent / "init_run.py").is_file():
        scripts_root = pipeline_root.parent  # installed: wiki_scripts/skills shape
    else:
        scripts_root = pipeline_root.parent / "scripts"
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


def workflow_turn_system_prompt(
    pipeline_root: Path | None, kb_root: Path | None = None, *, publisher: str = "agent"
) -> str:
    """Substituted workflow system prompt for one turn. ``pipeline_root=None``
    keeps the placeholders literal (与今天 _new_workflow_turn 的降级一致):
    根目录解析规则只是不命中，不换人格。"""
    if pipeline_root is None:
        return workflow_system_prompt(publisher)
    skills_root, scripts_root = resolve_pipeline_layout(pipeline_root)
    return substitute_prompt_roots(
        workflow_system_prompt(publisher),
        skills_root=skills_root,
        scripts_root=scripts_root,
        pool_root=(kb_root / "pool") if kb_root is not None else None,
    )


def workflow_turn_prompts(
    *,
    params: dict,
    run_dir: Path,
    kb_root: Path,
    pipeline_root: Path,
    publisher: str = "agent",
) -> tuple[str, str]:
    """唯一的两入口 prompt 组装点：返回 (system_prompt, user_prompt)，根目录
    占位符已替换。交互 wiki 与 headless launcher 都必须走这里，prompt 修复
    只落一处；唯一分叉是 publisher。"""
    return (
        workflow_turn_system_prompt(pipeline_root, kb_root, publisher=publisher),
        build_workflow_prompt(
            params=params, run_dir=run_dir, kb_root=kb_root,
            pipeline_root=pipeline_root, publisher=publisher,
        ),
    )

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


# Per-style voice contracts injected into writer prompts. The writing brief is
# style-agnostic and speaks in tension/thesis language (the zhihu register), so
# without an explicit contract the one-shot writer drifts every style toward
# the zhihu-explainer voice (suspense headline, bold "不是A而是B" opening) —
# observed on both 2026-09-17 and 2026-09-18 scientific memos.
STYLE_VOICE_CONTRACTS = {
    "scientific-memo": (
        "风格契约（scientific-memo）：动笔前先读"
        " <skills-root>/embodied-ai-review-writer/references/scientific-memo.md，"
        "并逐条执行其 Voice 段——中性研究声音、无修辞戏剧、无条件限定不得删除。"
        "writing-brief 里的'中心论点候选/张力对'只是素材提炼指引，不是成稿声音样板。"
        "硬性禁令：标题必须是研究对象的中性陈述，不得用悬念/转折式标题；"
        "开头不得出现加粗的'不是A，而是B'式口号段；"
        "正文不得使用知乎解释稿的演化弧叙事口吻。混入即返工。"
        "\n图表（必须遵守）：writing-brief「可用图表」段有图就落图，≤4 图 + 1 表，"
        "插在所支撑段落后，格式 `![题注](url)` + `> 用法：…`；图源只能是 evidence 携带的图，禁止自造 URL。"
        "\n引文格式按系统提示的科研备忘录引文契约执行（门禁会机械检查）。"
    ),
    "expert-explainer": (
        "风格契约（expert-explainer）：动笔前先读"
        " <skills-root>/embodied-ai-review-writer/references/zhihu-explainer.md 并执行其契约："
        "question-led 标题、TL;DR、机制先行、延伸阅读带编辑注。"
        "writing-brief「可用图表」段有图就落图（≤2 图），机制图优先，"
        "格式 `![题注](url)` + `> 用法：…`；图源只能是 evidence 携带的图，禁止自造 URL。"
    ),
    "kol-thread": (
        "风格契约（kol-thread）：动笔前先读"
        " <skills-root>/embodied-ai-review-writer/references/xiaohongshu-post.md 并执行其契约。"
        "writing-brief「可用图表」段有图就落 1 张最强洞察图，"
        "格式 `![题注](url)` + `> 用法：…`；图源只能是 evidence 携带的图，禁止自造 URL。"
    ),
}


def build_workflow_prompt(
    *,
    params: dict,
    run_dir: Path,
    kb_root: Path,
    pipeline_root: Path,
    publisher: str = "agent",
) -> str:
    """Compose the workflow kickoff prompt from the interview parameters.

    ``pipeline_root`` is the skills/ root (repo checkout or the wheel-bundled
    tree — claude reads the SKILL.mds and pipeline scripts from there);
    ``run_dir`` is the pre-created in-progress run under ``<kb-root>/work/``.
    Paths travel KB-relative like build_turn_prompt. ``publisher`` forks only
    the settle tail: "agent" (interactive wiki) runs finalize_run.py itself,
    "launcher" (headless writer) stops after the audit gates and lets the
    launcher process finalize/publish in code."""

    def rel(path: Path) -> str:
        try:
            return Path(os.path.relpath(path, kb_root)).as_posix()
        except ValueError:
            return str(path)

    agent = publisher == "agent"

    def stage(tag: str) -> str:
        return f"（[STAGE:{tag}]）" if agent else ""

    topic = str(params.get("topic", "")).strip()
    skills_root, scripts_root = resolve_pipeline_layout(pipeline_root)
    skills_rel = rel(skills_root)
    scripts_rel = rel(scripts_root)
    if agent:
        execution_chain = (
            "然后一气呵成执行到 settle："
            "综述包用 run_status.py 输出中 [next] 给出的 build_review_packet.py 完整命令"
            + stage("packet")
            + "逐字执行（直接写进运行目录，不要新建日期文件夹，不要读脚本源码探查参数）；"
            "亲自阅读证据事件与综述包后撰写成稿" + stage("writing")
            + "、生成 trace-map.json 并逐项跑审计脚本" + stage("audit") + "；"
            "审计门全过后按系统提示的落盘契约执行 finalize_run.py --run-dir <运行目录> --kb-root <kb-root>"
            + stage("settle")
            + "一步完成机械落盘，不要手改 run.json、不要手动登记表格或重建快照。"
        )
    else:
        execution_chain = (
            "然后一气呵成执行到审计门："
            "综述包用 run_status.py 输出中 [next] 给出的 build_review_packet.py 完整命令逐字执行"
            "（直接写进运行目录，不要新建日期文件夹，不要读脚本源码探查参数）；"
            "亲自阅读证据事件与综述包后撰写成稿、生成 trace-map.json 并逐项跑审计脚本。"
            "全部审计门通过后【立即停止本轮回复】——机械落盘、catalog 登记、"
            "wiki 快照重建与 publish 校验由 launcher 机械完成，不要触碰（见系统提示的停止契约）。"
            "成稿与 trace-map.json、evidence-appendix.md 一律落在运行目录根。"
        )
    lines = [
        "<workflow_request>",
        f"综述主题：{topic}",
        f"综述模式：{params.get('review_mode', 'scoping')}",
        f"时间范围：{params.get('time_range', '')}",
        f"检索策略：{params.get('search_strategy', 'smart')}",
        f"种子论文：{params.get('seed_arxiv_ids') or '无'}",
        f"目标风格：{params.get('target_style', 'all')}",
        *(
            [STYLE_VOICE_CONTRACTS[str(params.get("target_style"))]]
            if str(params.get("target_style") or "") in STYLE_VOICE_CONTRACTS
            else []
        ),
        f"关注重点：{params.get('focus') or '无'}",
        f"运行目录（已由系统创建，status: in-progress）：{rel(run_dir)}/",
        f"skills 根目录（SKILL.md 所在，读技能与脚本用）：<skills-root>={skills_rel}",
        f"顶层脚本目录（check_run_bundle/audit_citations）：<scripts-root>={scripts_rel}",
        "执行状态：上述机械阶段已由系统驱动脚本 run_review_pipeline.py 全部完成"
        "（产物见运行目录的 pipeline-summary.json、paper-notes/、evidence/），"
        "不要重跑任何检索/抽取/筛选/深读/投影命令。",
        "执行要求：运行现状一律用 run_status.py --run-dir <运行目录> 一次性读取"
        "（含漏斗数字、逐篇证据与 claim 摘要、References 作者/年份元数据、"
        "逐篇深读漏斗——held / deep-read-failed 及筛选命中词、产物清单、"
        "引用篇数下限门禁与建议命令），"
        "深读结果、References 元数据、筛选命中词均已在 run_status 输出："
        "禁止用内联 python 循环或 grep 统计 evidence/*.jsonl、screening.json、"
        "candidate-registry.json、paper-notes/，禁止逐个 cat 探查产物、"
        "对脚本跑 --help 探查或翻历史 run 的成稿当格式样板；"
        "成稿输入读渲染好的 review-packet.md / writing-brief.md / evidence-appendix.md，"
        "引文/图表格式契约以风格 references 文件与写作包为准。"
        + execution_chain,
        *(
            ["仅撰写目标风格成稿，不要写其他风格。"]
            if str(params.get("target_style") or "") not in ("", "all")
            else ["撰写三种成稿（scientific-memo / zhihu / xiaohongshu），可用 3 个并行 subagent 起草。"]
        ),
        "成稿落图：writing-brief「可用图表」段按各风格配额插图"
        "（URL/题注照抄 evidence 携带的图，插在所支撑段落后），appendix 全量保留图表。"
        "唯一允许提前停止的条件：检索失败或文献不足"
        "（覆盖/饱和未过、验收证据不足以成稿），"
        "此时停下如实说明并把 run 留在 in-progress；"
        "若 pipeline-summary 显示深读有失败篇目，如实说明影响。",
        "</workflow_request>",
    ]
    return "\n".join(lines)


def build_continuation_prompt(
    *, feedback: str = "", target_style: str = "", stage: str = "", publisher: str = "agent"
) -> str:
    """Resume the workflow after an interruption (crash, session end, user
    feedback mid-run). The prompt is stage-aware: a run that never produced
    the packet finishes the interrupted stage first; a run that already has
    the packet goes straight to writing. There is no outline checkpoint —
    both branches continue through settle in the same turn. ``publisher``
    forks only the settle tail (agent finalizes itself; launcher stops after
    the gates)."""

    agent = publisher == "agent"
    feedback = (feedback or "").strip()
    opinion = feedback if feedback else "无，按现有证据继续"
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
        writing_clause = (
            f"仅撰写采访中选定的风格：{style_label}，不要写其他风格。"
            + (STYLE_VOICE_CONTRACTS[style] if style in STYLE_VOICE_CONTRACTS else "")
        )
        parallel_clause = "单一成稿由主线程直接撰写润色，再走审计门"
    if agent:
        settle_clause = (
            "审计门过后按系统提示的落盘契约执行 finalize_run.py --run-dir <运行目录> --kb-root <kb-root>"
            "完成机械落盘（不要手改 run.json，也不要手动登记表格或重建快照）；"
            "门禁不过时修复后重跑即可，不要因此停止；"
            "最后输出 [TOPIC:<运行目录相对路径>]。"
        )
        mid_seq = "（[STAGE:packet] → [STAGE:writing] → [STAGE:audit] → [STAGE:settle]）"
        writing_seq = "（[STAGE:writing] → [STAGE:audit] → [STAGE:settle]）"
        fields_clause = (
            "run.json 的 status/files 字段由 finalize_run.py 机械补齐；"
            "style 与 scope_note 字段（单风格缩减范围声明）也由 finalize_run.py 机械补齐，不要手改；"
        )
    else:
        settle_clause = (
            "全部审计门通过后【立即停止本轮回复】；机械落盘（run.json 盖章、evidence/ 落盘拷贝）、"
            "catalog 登记、wiki 快照重建与 publish 校验由 launcher 机械完成，"
            "不要执行这些收尾动作、不要手改 run.json；不需要输出任何阶段或话题标记。"
        )
        mid_seq = "（综述包 → 成稿 → 审计门 → 停止）"
        writing_seq = "（成稿 → 审计门 → 停止）"
        fields_clause = "run.json 的 status/files/style/scope_note 字段一律不要手改（由 launcher 机械补齐）；"
    if stage in ("init", "plan", "retrieval", "mining", ""):
        lines = [
            "用户发来消息。先用 run_status.py --run-dir <运行目录> 一次性读取现状"
            "（已完成的环节不要重做；深读结果、References 元数据、筛选命中词都已在输出里，"
            "禁止内联 python 逐文件循环或 grep 统计）；"
            "综述包未生成时用其 [next] 给出的 build_review_packet.py 完整命令逐字执行；"
            f"然后一气呵成走完剩余阶段{mid_seq}："
            + settle_clause,
            f"用户消息：{opinion}",
        ]
        return "\n".join(lines)
    lines = [
        f"用户发来消息，请继续执行剩余阶段{writing_seq}：{writing_clause}、{settle_clause}"
        f"{parallel_clause}，尽量压缩总时长。"
        "可用 run_status.py --run-dir <运行目录> 一次性核对现状，禁止内联 python 逐文件循环。",
        fields_clause,
        f"用户消息：{opinion}",
    ]
    return "\n".join(lines)


# ---- 成稿修订（版本管理）---------------------------------------------------
# The wiki's revision flow turns one user requirement into an additive
# revisions/<style>-v<N>.md next to the base deliverable — never an overwrite.

REVISION_STYLE_BY_KEY = {
    "keyan": "scientific-memo",
    "zhihu": "expert-explainer",
    "xiaohongshu": "kol-thread",
}
REVISION_QUALITY_FLAG = {
    "scientific-memo": "--memo",
    "expert-explainer": "--zhihu",
    "kol-thread": "--xiaohongshu",
}
REVISION_STYLE_LABEL = {
    "keyan": "科研备忘录",
    "zhihu": "知乎解释版",
    "xiaohongshu": "小红书版",
}
REVISION_MARKER_RE = re.compile(r"^\[REVISION:([^\]]+)\]\s*$")


def build_revision_prompts(
    *,
    run_dir: Path,
    kb_root: Path,
    style_key: str,
    revision_number: int,
    topic_title: str,
    base_filename: str,
    pipeline_root: Path | None,
    message: str,
) -> tuple[str, str]:
    """(system_prompt, user_prompt) for one revision turn.

    ``style_key`` is the base version key (keyan/zhihu/xiaohongshu); the new
    file — and the snapshot version key — is ``<style_key>-v<N>``. The agent
    writes exactly one new file and runs the three article gates verbatim —
    same philosophy as the workflow prompts: concrete paths, no source
    reading, no parameter probing.
    """

    def rel(path: Path) -> str:
        try:
            return Path(os.path.relpath(path, kb_root)).as_posix()
        except ValueError:
            return str(path)

    style = REVISION_STYLE_BY_KEY.get(style_key)
    if style is None:
        raise ValueError(f"未知修订风格键：{style_key}")
    if pipeline_root is not None:
        skills_root, scripts_root = resolve_pipeline_layout(pipeline_root)
    else:
        # Same degradation as workflow_turn_system_prompt: keep placeholders
        # literal instead of guessing a layout.
        skills_root = kb_root / "<skills-root>"
        scripts_root = kb_root / "<scripts-root>"
    version_key = f"{style_key}-v{revision_number}"
    target_rel = f"revisions/{version_key}.md"
    evidence_rel = rel(run_dir / "evidence.jsonl")
    if not (run_dir / "evidence.jsonl").is_file():
        evidence_rel = rel(run_dir / "evidence") + "/*.jsonl"
    appendix_rel = rel(run_dir / "evidence-appendix.md")
    gate_commands = "\n".join([
        f"python3 {rel(skills_root / 'embodied-ai-review-writer' / 'scripts' / 'writing_audit.py')} "
        f"build-trace-map --evidence-jsonl {evidence_rel} --article {target_rel} "
        f"--output {rel(run_dir / 'revisions' / f'trace-map-{version_key}.json')}",
        f"python3 {rel(skills_root / 'embodied-ai-review-writer' / 'scripts' / 'writing_audit.py')} "
        f"audit-article-quality {REVISION_QUALITY_FLAG[style]} {target_rel}",
        f"python3 {rel(scripts_root / 'audit_citations.py')} --article {target_rel} "
        f"--appendix {appendix_rel} --evidence-jsonl {evidence_rel} --run-json {rel(run_dir / 'run.json')}",
    ])
    style_contract = STYLE_VOICE_CONTRACTS.get(style, "").replace("<skills-root>", rel(skills_root))
    system_prompt = (
        "你是「空间智能研究 Wiki」的成稿修订执行器，工作目录即本地知识库根目录。"
        "用户的修订要求针对某个已发布综述话题的一篇成稿。你生成一个**新修订版本**，绝不覆盖任何既有文件。\n\n"
        "【铁律】\n"
        "1. 只允许新建一个文件：目标路径见任务消息（revisions/<version>.md）；"
        "基底成稿、evidence-appendix.md、trace-map.json、run.json、evidence/ 目录一律只读。"
        "证据集不变：不得引入证据附录之外的论文、事件或图片 URL，不得增删参考文献编号。\n"
        "2. 动笔前先读：基底成稿（记住它的结构与优点）、evidence-appendix.md；"
        "需要核对引文时再读 evidence/ 下的 JSONL。\n"
        "3. 用户的修订要求优先：与要求冲突的段落按要求改写；其余内容保持原文水准——"
        "是定向修订，不是整体重写，更不能退化为缩写摘要。\n"
        + (f"\n{style_contract}\n" if style_contract else "\n")
        + "\n【门禁（逐字执行，命令里的路径不要改）】\n"
        f"{gate_commands}\n"
        "任一门禁未过：按其输出修复成稿后重跑该命令；门禁未过不是停止理由，"
        "也不要为过门禁删掉有支撑的引文或图表。\n\n"
        "【完成标记】\n"
        "三道门禁全部通过后，在最终回复的单独一行输出 "
        f"[REVISION:{target_rel}]，不要带其他后缀；"
        "无法完成修订时如实说明原因，绝不输出该标记。用中文与用户交流。"
    )
    user_prompt = "\n".join([
        "<revision_request>",
        f"话题：{topic_title}（运行目录：{rel(run_dir)}/）",
        f"修订风格：{REVISION_STYLE_LABEL.get(style_key, style_key)}"
        f"（基底文件：{base_filename}，作为 v{revision_number} 的底本）",
        f"目标文件（唯一允许新建的文件）：{target_rel}",
        "用户修订要求：",
        message.strip() or "（无具体要求，请改善整体质量）",
        "先读基底成稿与证据附录，再按要求生成修订版，然后逐字跑完上面系统提示里的门禁命令。",
        "</revision_request>",
    ])
    return system_prompt, user_prompt


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

    def _mutate(self, key: str, mutate, *, namespace: str = "topics") -> None:
        with locks.kb_lock(self.lock_root, "wiki-chat-sessions", wait=30):
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
    return kind in ("stage", "awaiting_input", "topic_ready", "topic_error", "session_reset", "error")


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
