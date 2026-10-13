"""Central home for every LLM prompt template.

Single source of prompt wording (the repo-wide form of workflow-prompt-
single-source): feature modules assemble inputs, this module owns the text.
Relocations must move the wording verbatim — prompt text is a contract with
the agents that consume it (see docs/adr/0004).

Do not paraphrase templates here as part of unrelated edits; wording changes
are their own review.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from embodied_learning.config import MAX_PROMPT_CONTEXT_FILES
from embodied_learning.utils.layout import resolve_pipeline_layout

# ---- deep-read skeleton (paper-reader stage) ---------------------------------

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


def pool_root_for(kb_root: str | Path) -> Path:
    """The shared public paper pool under the KB root (one folder per paper)."""

    return Path(kb_root).expanduser() / "pool"


def read_skeleton_output(raw: str) -> dict | None:
    import json
    import re

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) and payload.get("cards") is not None else None


# ---- persona regeneration triggers (query-planner layer) ---------------------

PERSONA_REGENERATION_RETRIEVAL_TRIGGER = (
    "After each literature-hub retrieval round, run search.py persona-suggest: "
    "any coverage dimension with passed=false or unique_candidates below minimum_unique_candidates "
    "requests a targeted gap-filling persona."
)
PERSONA_REGENERATION_READING_TRIGGER = (
    "During deep reading, if accepted-evidence stance distribution has limit+gap share below "
    "0.20, request a counter-evidence seeker persona."
)
PERSONA_REGENERATION_NOTE = (
    "Regeneration output re-enters the plan only via --persona-file after review; "
    "it never bypasses coverage gates."
)

# ---- retrieval-term selection (driver) -----------------------------------

TERMS_PROMPT = (
    "为以下文献综述主题给出 arXiv 检索筛选关键词。只输出一行严格 JSON，"
    '形如 {{"terms": ["词1", "词2", ...]}}，不超过 12 个词。'
    "要求：每个词 1-3 个英文单词（短 token 命中率远高于长短语），"
    "必须是论文标题/摘要里高频出现的写法（如 'registration'、'coarse registration'，"
    "而不是 'correspondence-free registration' 这类长描述），不要输出任何其他文字。"
    "\n主题：{topic}\n关注重点：{focus}"
)

# ---- dynamic retrieval queries (driver) ----------------------------------

DYNAMIC_QUERIES_PROMPT = (
    "为文献综述主题生成 arXiv API 检索查询。只输出一个严格 JSON 对象，形如：\n"
    '{{"queries": [{{"label": "...", "tier": "...", "query": "...", "why": "..."}}, ...]}}\n'
    "要求：\n"
    "- 10-20 条查询，覆盖：任务本身的直接术语、核心机制/方法、局限性/失效模式、评测/基准、部署工程。\n"
    "- query 使用 arXiv API 语法（all: 字段前缀、AND/OR、双引号短语），全部英文。\n"
    "- tier 取 direct / mechanism / limit / evaluation / deployment 之一，可加后缀，如 direct-anchor。\n"
    "- label 用英文小写连字符，前缀标明 tier（如 direct-online-temporal-calibration）。\n"
    "- 不要输出任何其他文字。\n"
    "\n主题：{topic}\n关注重点：{focus}{seed_line}"
)

# Appended to DYNAMIC_QUERIES_PROMPT's {seed_line} when seed papers are given.
SEED_LINE = "\n种子论文（以此为锚扩展查询词汇）：{seeds}"

# ---- smart deep-read queue selection --------------------------------------

SMART_SELECTION_PROMPT = (
    "你是综述选题助手。下面是综述话题和候选论文清单（编号 + arXiv ID + 年份 + 标题 + 摘要）。\n"
    "话题：{topic}\n"
    "{focus_line}\n"
    "任务：判断哪些候选与话题真正相关（能进入综述的相关工作或机制讨论，而不是只沾边）。\n"
    "要求：\n"
    "1. 最多输出 {limit} 篇；与话题核心无关的宁缺毋滥。\n"
    "2. 只输出一个 JSON 对象，格式：{{\"relevant\": [{{\"arxiv_id\": \"<id>\", \"reason\": \"<一句话选中理由>\"}}, ...], "
    "\"shortfall_note\": \"<如数量不足，一句话说明为什么其余不相关>\"}}。\n"
    "2b. 每条选中都要给 reason：它与话题哪条主线相关、可贡献什么证据（机制/对比/边界），不要复述标题。\n"
    "3. arXiv ID 必须逐字取自清单方括号内，不要改写。\n"
    "不要输出 JSON 以外的任何内容。\n\n"
    "候选清单：\n{candidates}"
)


# ---- slide-source agents (paper deck / run deck) -------------------------
# Path and sentinel arguments are supplied by the calling module (each deck
# owns its reference paths and DSL sentinels); only the wording lives here.

SLIDE_SOURCE_AGENT_PROMPT = """为论文 {paper_id} 制作一份组会汇报（reveal.js 幻灯片）的 slide-source。

输入（本地文件，直接 Read，不要联网）：
1. 写作简报：{brief_path}
2. 风格参考（DSL 语法、页面结构、密度红线，必须遵守）：{style_reference}
3. 论文全文（仅当简报某节标注「（笔记未提供，需从 paper.md 核对）」时才去核对，不得引入简报之外的数字或论文）：{paper_path}

任务：按风格参考的 DSL 写出完整 slide-source，按主题组织（问题 → 方法 → 结果 → 局限 → 启示），
不要按论文章节顺序照抄。
- 只输出两个标记之间的内容，不要写文件，不要跑命令，不要输出标记之外的任何文字。
- 文档头必须含 # title / # subtitle；不要写 # refs（脚本提供）；首页 class: cover；每张内容页带 verdict。
- 引文只用 {{{{main}}}}；不用 @fig；简报未支撑的判断写「论文未给出」。

{open_sentinel}
（在此输出 slide-source DSL）
{close_sentinel}"""


def slide_source_agent_prompt(
    *, paper_id: str, brief_path: str, style_reference: str, paper_path: str,
    open_sentinel: str, close_sentinel: str,
) -> str:
    return SLIDE_SOURCE_AGENT_PROMPT.format(
        paper_id=paper_id, brief_path=brief_path, style_reference=style_reference,
        paper_path=paper_path, open_sentinel=open_sentinel, close_sentinel=close_sentinel,
    )


RUN_DECK_SOURCE_AGENT_PROMPT = """为综述 run 制作一份汇报（reveal.js 幻灯片）的 slide-source。

输入（本地文件，直接 Read，不要联网）：
1. 写作简报（内容与组织的唯一依据）：{brief_path}
2. 证据附录（引文来源，含 References）：{appendix_path}
3. 风格参考（DSL 语法、页面结构、密度红线，必须遵守）：{style_reference}

可用引文键（refs 已由脚本生成，正文只用这些键，禁止自造）：
{ref_lines}

任务：按主题组织汇报（背景 → 谱系 → 对比 → 机制 → 局限 → 启示），
不要按任何一篇文章的章节顺序照抄；每页一个论点、页底 verdict。
- 只输出两个标记之间的内容，不要写文件，不要跑命令，不要输出标记之外的任何文字。
- 文档头必须含 # title / # subtitle；不要写 # refs（脚本提供）；首页 class: cover；每张内容页带 verdict。
- 没有 @fig 指令可用的本地图片，完全不用 @fig；不要引用任何 URL 图片。
- 简报未支撑的判断不要写；保留 可能/仅/尚未/在……条件下 等限定词。

{open_sentinel}
（在此输出 slide-source DSL）
{close_sentinel}"""


def run_deck_source_agent_prompt(
    *, brief_path: str, appendix_path: str, style_reference: str, ref_lines: str,
    open_sentinel: str, close_sentinel: str,
) -> str:
    return RUN_DECK_SOURCE_AGENT_PROMPT.format(
        brief_path=brief_path, appendix_path=appendix_path,
        style_reference=style_reference, ref_lines=ref_lines,
        open_sentinel=open_sentinel, close_sentinel=close_sentinel,
    )


# ---- quick-read card agent ----------------------------------------------

QUICK_READ_AGENT_PROMPT = """为论文 {paper_id} 撰写一张速读卡（quick-read card）。

输入（本地文件，直接 Read，不要联网）：
1. 写作简报：{brief_path}
2. 风格参考（结构、语气、拒绝条件，必须遵守）：{style_reference}
3. 引用投影规范：{citation_reference}
4. 论文全文（仅当简报某节标注「（笔记未提供，需从 paper.md 核对）」时才去核对，不得引入简报之外的数字或论文）：{paper_path}

任务：按风格参考的固定结构输出一张中文速读卡。
- 只输出两个标记之间的内容，不要写文件，不要跑命令，不要输出标记之外的任何文字。
- 正文 600-1200 中文字符；禁表格；固定 8 节；链接节只有论文自己的 arXiv 链接。
- 简报未支撑的判断写「论文未给出」；保留 可能/仅/尚未/在……条件下 等限定词。

{open_sentinel}
（在此输出速读卡 Markdown）
{close_sentinel}"""


def quick_read_agent_prompt(
    *, paper_id: str, brief_path: str, style_reference: str, citation_reference: str,
    paper_path: str, open_sentinel: str, close_sentinel: str,
) -> str:
    return QUICK_READ_AGENT_PROMPT.format(
        paper_id=paper_id, brief_path=brief_path, style_reference=style_reference,
        citation_reference=citation_reference, paper_path=paper_path,
        open_sentinel=open_sentinel, close_sentinel=close_sentinel,
    )


# ---- wiki workflow / chat prompts ------------------------------------------
# (Moved verbatim from wiki/publish/chat.py; that module keeps session
#  registry, HTTP glue and output-marker parsing.)

CHAT_SYSTEM_PROMPT = (
    "你是「空间智能研究 Wiki」的研究助手，工作目录即本地知识库根目录。"
    "evidence/ 下每个 literature-review-* 文件夹是一次研究运行：含三种成稿"
    "（scientific-memo_keyan.md、zhihu-explainer_zhihu.md、xiaohongshu-post_xiaohongshu.md）、"
    "evidence-appendix.md 与 run.json；pool/ 存放已抽取的论文全文 markdown；knowledge/ 是主题卡片。"
    "回答要基于证据：先读相关文件再下结论，引用时给出文件相对路径。"
    "用户可能请你撰写综述草稿：用 Write 把新文件写进当前话题的运行目录，文件名以 survey- 开头，"
    "不要覆盖已有成稿。用中文回答，先给中心判断，再给证据与反例。"
)

_WORKFLOW_BASE_SYSTEM_PROMPT = (
    "你是「空间智能研究 Wiki」的综述工作流执行器，工作目录即本地知识库根目录。"
    "<skills-root> 下是本仓库的技能树（每个子目录含 SKILL.md 与 scripts/），"
    "<scripts-root> 下是顶层脚本（run.py check-bundle、run.py audit-citations 等）。"
    "按照 <skills-root>/embodied-ai-review-writer/SKILL.md 的综述契约执行，"
    "SKILL.md 中出现的相对路径按其所在目录解析：路径以 skills/ 开头时替换为 <skills-root>，"
    "以 scripts/ 开头时替换为 <scripts-root>。"
    "只遵循 SKILL.md 的成稿、风格与引文契约；其「Run lifecycle and gates」里的检索、深读、"
    "投影段落以及所有手动 settle/publish 步骤（翻 run.json status、手工拷贝 evidence 资产、"
    "手工登记 catalog 表格、重建 wiki 快照并核对发布结果）已全部由系统机械化——"
    "一律跳过，更不要照着手动执行。"
    "\n\n【职责边界——固定流程已由系统完成】\n"
    "查询规划、候选检索（Semantic Scholar + arXiv）、候选注册、筛选、覆盖度评估、"
    "全文 HTML 抽取、论文深读（速记骨架+审计）与证据投影已由驱动脚本 run.py pipeline 一次性完成，"
    "运行现状用 python3 <scripts-root>/run.py status --run-dir <run-dir> 一次性读取："
    "漏斗数字、逐篇证据与 claim、References 作者/年份元数据、逐篇深读漏斗（held / deep-read-failed 及筛选命中词）、"
    "产物清单与建议命令都在它的输出里。"
    "禁止用内联 python 循环或 grep 统计 screening.json、candidate-registry.json、paper-notes/、evidence/——"
    "那是一次调用就能拿到的机械聚合；也不要读脚本源码或用 --help 探查参数。"
    "不要手动执行任何检索/抽取/筛选/深读/投影命令（search.py search-arxiv、search.py search-semantic-scholar、"
    "search.py build-candidate-registry、search.py screen-candidates、search.py assess-review-coverage、"
    "fetch.py extract-content-queue、read.py build-reading-packet、read.py build-paper-note、"
    "read.py project-evidence-events、run.py pipeline）"
    "——重复执行只会浪费时长且可能触发限流。若 summary 显示维度、地板或深读未过，如实向用户说明，不要自行补救检索。"
    "\n\n【你的判断职责】\n"
    "1. 论文深读与证据投影：已由系统驱动脚本完成（速记骨架 + 审计 + 投影）。"
    "不要派发深读 subagent、不要跑 read.py project-evidence-events；"
    "若 pipeline-summary.json 的 deep_read 字段显示失败篇目，如实说明。\n"
    "2. 综述包与成稿：review-packet.md / writing-brief.md / evidence-appendix.md 已由驱动的 "
    "review-packet 阶段按最终证据集渲染好——直接读它们撰写成稿；仅当缺失时才用 "
    "run.py status [next] 给出的 write.py review-packet 完整命令补生成（逐字执行，"
    "不要读脚本源码探查参数）。review-packet 是简报不是成稿；然后亲自撰写成稿（trace-map.json 由 run.py finalize/launcher 机械生成，不要手写）；"
    "成稿必须落图：writing-brief 的「可用图表」段给出带图的证据事件与现成 markdown 块，"
    "按各风格配额把图插到所支撑的段落之后（图源只能是 evidence 携带的图，URL/题注照抄，禁止自造图片）。\n"
    "3. 审计门：逐一通过 <scripts-root>/run.py check-bundle、<scripts-root>/run.py audit-citations、"
    "<skills-root>/embodied-ai-review-writer/scripts/write.py audit-article-quality "
    "（加 --evidence-jsonl 以启用带图可用但成稿未落图的告警）；"
    "审计门全过之前不要把证据落盘到 evidence/。"
    "门禁失败消息自带修法（指标 vs 阈值 + 补救命令/写法）——按消息执行即可，"
    "不要读门禁脚本源码。写作契约（必需节/篇幅/链接预算/句长）已写进 writing-brief，"
    "首稿按契约写即可；不要用内联 python 预检中文字符数、💡 数、链接数——write.py audit-article-quality 全覆盖；"
    "风格修复（长句拆分、措辞调整）用 Edit 直接改文本，不要写内联 python 字符串手术脚本。"
    "豁免逃生门的机械入口：run.py finalize --declare-gate-exception "
    "<name> --reason \"...\"（可豁免 saturation / cited_paper_floor 等，理由自动记入 notes），"
    "严禁手改 run.json。\n"
    "摘要级事件（附录「摘要级相关工作」节，tier: abstract）只用于相关工作定位句"
    "——“谁在什么方向做了什么”，不得作为机制结论或中心论点的证据；"
    "References 中对应条目末尾标注（摘要级）。"
    "\n\n【停轮与决策点】\n"
    "精读数量不够（引用篇数地板未过，含筛选如实 shortfall）是设计内的用户决策点："
    "汇报【选定的精读论文列表】（run_status [papers] 节的全文档论文）后立即停止，"
    "把 run 留在 in-progress，并在回复末尾单独一行输出 [STOP:awaiting-user]，"
    "等待用户决策：补充信息（种子论文/关注重点）或扩大综述范围（review-mode/时间范围）。"
    "这是正确终态，不是失败。严禁薄审落盘（除非用户明示接受）、严禁更换选文策略、"
    "严禁删除或改写机械产物（screening*.json、extraction-summary.json、pipeline-summary.json、"
    "evidence/、paper-notes/）、严禁手改 run.json（gate_exceptions/notes/status/event_count）、"
    "严禁继续硬修或反复重试。"
    "其余一切：检索通道整体失败时同样停下如实说明（[STOP:awaiting-user]）；"
    "其他门禁失败（引文/编辑/bundle，含 coverage/saturation）一律是修复重跑条件，绝不停轮——"
    "按门禁消息里给的修法执行；coverage/saturation 未过可续跑驱动，也可用 "
    "run.py finalize --declare-gate-exception <name> --reason \"...\" 声明豁免（勿手改 run.json）。"
    "不要因大纲确认、风格选择等原因中途停轮等待用户——综述从综述包到 settle 一轮写完。"
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
    "面向用户的对话回复里不要使用 markdown 表格（对话框不渲染表格，会坍成一行纯文本）——"
    "论文清单、门禁对比、漏斗数字一律用编号列表或短段落；成稿文件（*_keyan.md 等）里的表格不受此限。"
)

_WORKFLOW_AGENT_TAIL = (
    "\n\n【机械落盘由你收尾】\n"
    "审计门全过后，用 python3 <scripts-root>/run.py finalize --run-dir <run-dir> "
    "一步完成机械落盘：补齐 run.json 字段（含单风格时的 style/scope_note）、复跑两道门、拷贝 evidence/<run>/、"
    "翻 settled、登记 catalog、重建 wiki 快照——这些全是 run.py finalize 的机械职责，"
    "不要手改 run.json，也不要再手动跑登记表格或重建快照的脚本、逐项核对 wiki 端口的发布结果。"
    "--kb-root 可省：脚本自动从运行目录推断知识库根（<kb-root>/work/<run> 布局），"
    "显式传错目标会被拒绝落盘（防落错库）；run.py status [next] 给出带 --kb-root 的逐字命令。"
    "run.py finalize 门禁不过时会机械打印缺失项：按提示修复后重跑 finalize 即可，门禁未过不是提前停止的理由。"
    "\n\n在开始每个阶段前，先单独输出一行阶段标记（普通文本，不要放进代码块）："
    "[STAGE:mining] / [STAGE:packet] / [STAGE:writing] / [STAGE:audit] / [STAGE:settle]，后跟一句话进度说明。"
    "落盘到 evidence/ 后，在最终回复的单独一行输出 "
    "[TOPIC:<evidence/ 下新运行目录的相对路径>]，不要带其他后缀。"
)

_WORKFLOW_LAUNCHER_TAIL = (
    "\n\n【机械落盘与发布不归你】\n"
    "通过全部审计门后【立即停止本轮回复】，不要再做任何落盘或发布动作："
    "run.py finalize、run.json 盖章、evidence/ 落盘拷贝、catalog 登记、"
    "wiki 快照重建与 publish 校验由 launcher 在你停止后机械完成，"
    "不要执行这些脚本、不要手改 run.json。"
    "成稿文件按目标风格直接写在运行目录根"
    "（scientific-memo_keyan.md / zhihu-explainer_zhihu.md / xiaohongshu-post_xiaohongshu.md / survey-*.md），"
    "evidence-appendix.md 落在运行目录根（trace-map.json 由 launcher 机械生成，不要手写），"
    "launcher 会从那里取件做门禁与发布。不需要输出任何阶段或话题标记。"
)

def workflow_system_prompt(publisher: str = "agent") -> str:
    """Workflow system prompt: shared base + the one deliberate fork.

    ``publisher="agent"``（交互 wiki 面）让代理自己跑 run.py finalize 收尾，
    并要求输出 wiki UI 解析的 [STAGE:]/[TOPIC:] 标记；``publisher="launcher"``
    （headless writer）在审计门后立即停止——机械落盘/发布由 launcher 在代码里做。
    """
    if publisher == "agent":
        return _WORKFLOW_BASE_SYSTEM_PROMPT + _WORKFLOW_AGENT_TAIL
    if publisher == "launcher":
        return _WORKFLOW_BASE_SYSTEM_PROMPT + _WORKFLOW_LAUNCHER_TAIL
    raise ValueError(f"unknown workflow publisher: {publisher}")

WORKFLOW_SYSTEM_PROMPT = workflow_system_prompt("agent")

def substitute_prompt_roots(
    text: str,
    *,
    skills_root: Path,
    scripts_root: Path,
    pool_root: Path | None = None,
    kb_root: Path | None = None,
) -> str:
    """Fill the <skills-root>/<scripts-root>/<pool-root>/<kb-root> placeholders
    in a workflow prompt. Paths travel KB-relative like all other prompt
    context (no absolute leak); an absent pool keeps the placeholder literal
    (the pool-lookup instruction just never matches). <kb-root> is filled when
    known so the writer never has to guess the publish target (2026-09-30
    absolute-pose published into the wrong KB)."""

    text = text.replace("<skills-root>", skills_root.as_posix()).replace(
        "<scripts-root>", scripts_root.as_posix()
    )
    if pool_root is not None:
        text = text.replace("<pool-root>", pool_root.as_posix())
    if kb_root is not None:
        text = text.replace("<kb-root>", kb_root.as_posix())
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
        kb_root=kb_root,
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
    # Survey 的交付物是机械渲染的综述包本身（finalize 的 survey 风格文件就是
    # review-packet.md），没有 prose 成稿；slide-deck 只写 DSL，编译交给脚本。
    # 此前这两个键缺失时上述注入为空，one-shot writer 会自行发挥。
    "survey": (
        "风格契约（survey）：交付物是机械渲染的综述包（review-packet.md + writing-brief.md + "
        "evidence-appendix.md），不是 prose 成稿——确认综述包已在运行目录根后直接进入审计门与落盘，"
        "不要重写或改写包内容，也不要另写记忆体成稿文件。"
    ),
    "slide-deck": (
        "风格契约（slide-deck）：只写 slide-source DSL 源文件，"
        "用 <skills-root>/embodied-ai-review-writer/scripts/write.py compile-slide-deck "
        "编译成 slide-deck_report.html 单文件；禁止手写 HTML。"
        "图与引文纪律同综述：图源只能是 evidence 携带的图，引文只引已接纳证据。"
    ),
    # 刻意没有 "all" 键：三风格 run 不注入任何单风格口吻契约（风格契约的
    # 作用是防单稿漂移到知乎腔），全风格共用 writing-brief「各风格写作契约」节
    # ——tests/test_wiki_chat.py 的 no_single_style_contract 契约钉死这一点。
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
    the settle tail: "agent" (interactive wiki) runs run.py finalize itself,
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
            "综述包（review-packet/writing-brief/evidence-appendix）已由驱动生成直接读，缺失时才用 run.py status [next] 的 write.py review-packet 完整命令补生成"
            + stage("packet")
            + "（逐字执行，不要读脚本源码探查参数）；"
            "亲自阅读证据事件与综述包后撰写成稿" + stage("writing")
            + "、逐项跑审计脚本" + stage("audit") + "；"
            "审计门全过后按系统提示的落盘契约执行 run.py finalize --run-dir <运行目录>"
            "（--kb-root 可省，自动从运行目录推断知识库根）"
            + stage("settle")
            + "一步完成机械落盘，不要手改 run.json、不要手动登记表格或重建快照。"
        )
    else:
        execution_chain = (
            "然后一气呵成执行到审计门："
            "综述包（review-packet/writing-brief/evidence-appendix）已由驱动生成直接读，缺失时才用 run.py status [next] 的 write.py review-packet 完整命令补生成"
            "（逐字执行，不要读脚本源码探查参数）；"
            "亲自阅读证据事件与综述包后撰写成稿、逐项跑审计脚本。"
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
        f"选文策略：{params.get('selection_strategy', 'smart')}",
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
        f"顶层脚本目录（run.py check-bundle / run.py audit-citations）：<scripts-root>={scripts_rel}",
        "执行状态：上述机械阶段已由系统驱动脚本 run.py pipeline 全部完成"
        "（产物见运行目录的 pipeline-summary.json、paper-notes/、evidence/），"
        "不要重跑任何检索/抽取/筛选/深读/投影命令。",
        "执行要求：运行现状一律用 run.py status --run-dir <运行目录> 一次性读取"
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
        "精读数量不够时汇报选定的精读论文列表并【立即停轮】（末尾单独一行 [STOP:awaiting-user]，"
        "run 留在 in-progress），等待用户决策：补充信息或扩大综述范围——这是正确终态；"
        "严禁薄审落盘、擅自更换选文策略、删改机械产物、手改 run.json 或继续硬修。"
        "汇报时用编号列表逐篇给出（篇名/作者/年份/证据构成），不要输出 markdown 表格——"
        "对话框不渲染表格。"
        "检索通道整体失败同样停轮报告。其余门禁失败（含覆盖/饱和）一律修复重跑，"
        "按门禁消息修法执行，豁免走 --declare-gate-exception 机械入口；"
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
            "审计门过后按系统提示的落盘契约执行 run.py finalize --run-dir <运行目录>"
            "（--kb-root 可省，自动从运行目录推断知识库根）"
            "完成机械落盘（不要手改 run.json，也不要手动登记表格或重建快照）；"
            "门禁不过时修复后重跑即可，不要因此停止；"
            "最后输出 [TOPIC:<运行目录相对路径>]。"
        )
        mid_seq = "（[STAGE:packet] → [STAGE:writing] → [STAGE:audit] → [STAGE:settle]）"
        writing_seq = "（[STAGE:writing] → [STAGE:audit] → [STAGE:settle]）"
        fields_clause = (
            "run.json 的 status/files 字段由 run.py finalize 机械补齐；"
            "style 与 scope_note 字段（单风格缩减范围声明）也由 run.py finalize 机械补齐，不要手改；"
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
            "用户发来消息。先用 run.py status --run-dir <运行目录> 一次性读取现状"
            "（已完成的环节不要重做；深读结果、References 元数据、筛选命中词都已在输出里，"
            "禁止内联 python 逐文件循环或 grep 统计）；"
            "综述包未生成时用其 [next] 给出的 write.py review-packet 完整命令逐字执行；"
            f"然后一气呵成走完剩余阶段{mid_seq}："
            + settle_clause,
            f"用户消息：{opinion}",
        ]
        return "\n".join(lines)
    lines = [
        f"用户发来消息，请继续执行剩余阶段{writing_seq}：{writing_clause}、{settle_clause}"
        f"{parallel_clause}，尽量压缩总时长。"
        "可用 run.py status --run-dir <运行目录> 一次性核对现状，禁止内联 python 逐文件循环。",
        fields_clause,
        f"用户消息：{opinion}",
    ]
    return "\n".join(lines)

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
        f"python3 {rel(skills_root / 'embodied-ai-review-writer' / 'scripts' / 'write.py')} "
        f"build-trace-map --evidence-jsonl {evidence_rel} --article {target_rel} "
        f"--output {rel(run_dir / 'revisions' / f'trace-map-{version_key}.json')}",
        f"python3 {rel(skills_root / 'embodied-ai-review-writer' / 'scripts' / 'write.py')} "
        f"audit-article-quality {REVISION_QUALITY_FLAG[style]} {target_rel}",
        f"python3 {rel(scripts_root / 'run.py audit-citations')} --article {target_rel} "
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


# ---- brief / scaffold notes the writer agent reads ------------------------

SCAFFOLD_BANNER = (
    "<!-- SCAFFOLD: 机械渲染的证据脚手架,非成稿。 -->\n"
    "> **警告:本文件不是综述成稿。** 它是 claim map 与 stance 分桶的机械渲染,\n"
    "> 仅供对照检查。成稿必须由 `$embodied-ai-review-writer` 依 `writing-brief.md` 撰写,\n"
    "> 并保存为不带 `.scaffold` 后缀的正式文件名。\n\n"
)

ABSTRACT_TIER_NOTE = "tier: abstract，仅定位用，不得作为机制结论。"

FIGURE_CAPS_NOTE = (
    "每风格配额（上限，不是下限）：科研备忘录 ≤4 图 + 1 表；知乎解释版 ≤2 图；"
    "小红书版 ≤1 图；slide-deck 每页 ≤2 图、全册 ≤10 图；evidence-appendix 全量保留。"
    "图只能来自下面列出的 evidence 事件图表（URL 与题注照抄，禁止自造或外搜图片）；"
    "插入位置：紧跟其支撑的段落之后；无合适图就少配或不配，禁止为凑数放 teaser/logo。"
)

# ---- deep-read question the skeleton agent is asked ----------------------

GENERAL_QUESTION = "该论文的核心贡献、方法有效性的量化证据、适用边界与局限（通用深读问题）"

# ---- stop markers the writer emits (parsed by chat.STOP_MARKER_RE) -------
# The writer's terminal-decision token. The launcher treats this as the
# designed user-decision stop (deep-read shortfall), not a failure.
USER_DECISION_STOP = "[STOP:awaiting-user]"
