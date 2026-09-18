# scripts/ — 运维层脚本指南

`scripts/` 是仓库的**运维层**：知识库（`knowledge/`、`evidence/`）的完整性检查、文献综述流水线的编排、公共论文池的维护、本地 Wiki 的构建与服务。它是给**人和 CI** 直接敲命令的地方。

与之相对的两层：

- `embodied_learning/`（Python 包）——数据处理的具体实现（检索、抓取、解析、知识库模型），无 CLI；
- `skills/*/scripts/`——三个技能（检索 hub / 阅读 reader / 写作 writer）的**薄入口**，每个文件只做 argparse 翻译然后 import `embodied_learning.*`；技能内部约定见各 `SKILL.md`。

一句话分工：**skills 管单阶段能力，scripts 管跨阶段的编排、门禁与发布。**

---

## 最容易混淆的两个脚本：launch_review vs run_review_pipeline

| | `run_review_pipeline.py`（driver） | `launch_review.py`（launcher） |
|---|---|---|
| 覆盖范围 | **只做机械阶段**：plan → 检索 → 引文扩张 → registry → 筛选 → coverage → 抽取 → 阅读包 → 深读（并行 one-shot agent）→ 证据投影 → coverage 终态重算 | **端到端**：init_run → driver（上面全部）→ writer agent（写综述成稿）→ 审计门 → settle → 登记 catalog + 重建 wiki |
| 谁写综述 | 没人——它产出的 `writing-brief.md` / `review-packet.md` 是写作输入 | 一个脱离交互的 one-shot `claude -p` agent（复用 wiki 的 workflow prompt），失败自动带问题清单续跑 |
| 幂等性 | 每阶段产物存在即跳过，可反复续跑 | 阶段标记（`.launch/*.done`）+ driver 幂等，`--resume` 从断点继续 |
| 失败重试 | 无（退出码交给你） | driver 3 次重试带冷却；writer 门禁失败最多 2 轮 continuation |
| 使用场景 | claude 交互式综述（claude 自己做 packet→成稿→审计）或想手动分阶段控制 | **程序化/无人值守**：一条命令出已发布的综述，不依赖任何交互会话 |

简言之：**driver 是流水线的“上半场”，launcher 是把上半场和下半场（写作、门禁、发布）接起来并加固防失败的整场指挥**。交互式工作流用 driver 就够；想程序化启动、或被“后台任务莫名被杀”坑过，用 launcher。

---

## 全景关系图

```
                        launch_review.py（无头端到端，程序化入口）
                                │ 调用
        ┌───────────────────────┼──────────────────────────┐
        ▼                       ▼                          ▼
  init_run.py            run_review_pipeline.py        wiki workflow prompt
  （run 出生证明）        （机械阶段 driver）           （claude -p writer agent）
                                │                           │
        ┌───────────┬───────────┼───────────┐              │
        ▼           ▼           ▼           ▼              ▼
   search.py   extract_arxiv  build_reading  build_paper  门禁三件套
   （检索）     _content.py    _packet.py     _note.py    audit_citations.py
   fetch.py    （全文抽取）   （阅读包）     （深读组装）  check_run_bundle.py
   knowledge.py                                          validate_current_reviews.py
   （skills 薄入口）                                           │
                                                              ▼
                                        knowledge/literature-review-catalog.md 登记
                                                              │
                                            build_research_wiki.py → wiki/data/ 快照
                                                              │
                                            serve_research_wiki.py + wiki_chat.py（浏览器阅读/对话）
```

---

## 按用途分类

### A. 综述流水线（生产主线）

| 脚本 | 作用 | 典型用法 |
|---|---|---|
| `launch_review.py` | 无头端到端 launcher（见上表） | `setsid nohup python3 scripts/launch_review.py --topic ... --review-mode systematic --time-range A..B --focus ... --arxiv-snapshot ~/Documents/arxiv/arxiv-metadata-oai-snapshot.sqlite > /tmp/launch.log 2>&1 &`；`--status` / `--resume` / `--stop` 均需 `--run-dir` |
| `init_run.py` | 生成 run 出生证明（`run.json` status=in-progress），防“管线烂尾无痕迹” | `init_run.py --topic ... --knowledge-id EA-DATA --time-range A..B --review-mode systematic`（launcher 内部也调它） |
| `run_review_pipeline.py` | 机械阶段 driver（见上表）；`--skip-deep-read` 可把深读交给外部编排 | `run_review_pipeline.py --run-dir work/<run> --topic ... --review-mode systematic --time-range A..B --focus ... --arxiv-snapshot <sqlite>` |
| `next_event_id.py` | 扫描 evidence/**/evidence.jsonl，给出下一个无冲突事件 ID | `next_event_id.py --prefix EA-XXX-2026` |
| `check_run_bundle.py` | **settle 前门禁**：bundle 完整性（三风格或声明的 style+scope_note、files 清单、事件数、coverage ready_to_stop） | `check_run_bundle.py <run-dir>` |
| `audit_citations.py` | **settle 前门禁**：成稿引用审计（死锚点、超出加载证据集的引用、run.json 漂移） | `audit_citations.py --article <成稿> --appendix evidence-appendix.md --evidence-jsonl <jsonl>` |
| `validate_current_reviews.py` | 批量校验 catalog 路由的全部已发布 run | `validate_current_reviews.py`（知识库改动后跑） |

### B. 知识库与 Wiki 运维

| 脚本 | 作用 | 典型用法 |
|---|---|---|
| `check_kb_links.py` | 知识库链接完整性（sources、主题卡、索引、evidence 清单、POOL 路径） | `check_kb_links.py`（改完 knowledge/ 必跑） |
| `build_research_wiki.py` | 从 KB 构建 Wiki 静态快照（原子发布到 `wiki/data/`） | `build_research_wiki.py --kb-root <kb-root> --output <kb-root>/wiki/data` |
| `serve_research_wiki.py` | 本地起 Wiki 服务（含安全的 refresh 端点） | `serve_research_wiki.py`（默认读 `~/Documents/arxiv`） |
| `wiki_chat.py` | Wiki 聊天/工作流的 claude 会话后端（stream-json 桥接、嵌套 claude 环境防护、workflow/continuation prompt 的定义处） | 由 `serve_research_wiki.py` 内部使用，不直接手跑 |
| `visualize_kb_index.py` | 把 `knowledge/index.md` 渲染成可浏览文档站 | `visualize_kb_index.py` |

### C. 论文池与单篇入口

公共池默认 `~/Documents/arxiv/pool/`，一论文一目录（`arxiv-<id>/`：paper.md、extraction.json、note.json、meta.json）。

| 脚本 | 作用 | 典型用法 |
|---|---|---|
| `quick_read_paper.py` | 单篇速读卡（速读）：保证入池+深读（强制），写 `quick-read_sudu.md` | `quick_read_paper.py --arxiv-id 2302.01109` |
| `prepare_paper_chat.py` | 为 Wiki「论文对话」备料：保证入池+深读（与速读同链路，不做卡片） | 由 wiki `/api/paper/chat` 内部调用 |
| `build_paper_note.py` | 深读组装器：agent 只出速记骨架，它负责 locator 解析/逐字校验/组装/审计 | 由 driver 的深读阶段调用；单篇手跑 `build_paper_note.py --help` |

### D. 共享库 `scripts/lib/`

| 模块 | 作用 |
|---|---|
| `agent_invoke.py` | one-shot `claude -p` 调用原语、CLI 发现、深读/骨架 prompt |
| `review_runs.py` | catalog 路由的 run 清单加载、`STYLE_TO_FILE` 等合同常量 |
| `jsonio.py` | 原子写 JSON 等文件小工具 |
| `markdown_semantics.py` | Wiki/知识图谱渲染共用的安全 Markdown 语义 |

---

## 能力状态：三段工作流各能力在脚本层的落地情况

对照 [docs/review-workflow-three-stages.md](../docs/review-workflow-three-stages.md) 的能力清单，
逐项给出典型用法与状态。**状态标准是"无人值守可交付"**：一条命令（或一次 `launch_review.py`）
不依赖交互会话现场调整就能跑通的算"已实现"；要人/交互会话手动串步骤或现场发挥的只能算
"部分（组合式 SOP）"——这类是固定流程而非可交付功能。知识产出阶段（成稿、门禁、settle、
catalog、wiki）由 launcher spawn 的 writer agent 完成，交互会话只做调度与代码维护。

### 检索段

| 能力 | 状态 | 典型用法 |
|---|---|---|
| 种子引文扩张 | 已实现 | launcher 传 `--seed-arxiv-ids`；或 `search.py expand-via-citations --seed-id <id> --direction both --output ...` |
| 策展列表通道（awesome-list 整库收割） | 已实现（2026-09-18） | `search.py harvest-curated-list --repo <owner/repo> --resolve-db <snapshot.sqlite> --output harvest.json`（全库文本文件扫描；非 arXiv 条目先快照标题匹配、后 S2 退避解析）；launcher 传 `--external-candidates harvest.json` 跳过关键词检索；run.json 声明 `workflow_version: 1` + `selection_method: curated-list`（不走 coverage/饱和门） |
| 引文图派生综述 | 已实现 | `search.py rank-influential-papers / rank-problem-relevance --extra-ids-file <ids.txt>` 选篇 + launcher 成稿；run.json 声明 `workflow_version: 1` + `selection_method` |
| 选题调研（只要文献地图） | 部分（组合式 SOP） | `search.py build-query-plan → search-* → build-candidate-registry → screen-candidates → assess-review-coverage` 需手动串；driver 无"停在 coverage"的截断旗标 |
| 文献地图维护（跨 run 候选池增量复用） | **未实现** | registry 每 run 从零建；`build-candidate-registry` 无 `--registry-input` 合并旧 run 候选池（证据层复用已有：`--select-events-file`） |

### 阅读段

| 能力 | 状态 | 典型用法 |
|---|---|---|
| 单篇速读卡 | 已实现 | `scripts/quick_read_paper.py --arxiv-id <id>`（强制入池+深读，产出 `quick-read_sudu.md`） |
| 单篇问答 | 已实现 | wiki「论文对话」（`scripts/prepare_paper_chat.py` 备料，`serve_research_wiki.py` 服务） |
| 批量深读（run 内） | 已实现 | driver 深读阶段并行 one-shot agents（launcher `--agents-parallel`，默认 10）；幂等：只有 audit status ∈ {pass, needs-review} 的笔记才算完成，reject/失败自动重试 |
| 补充深读（单篇缺口） | 已实现 | `scripts/build_paper_note.py` 单篇手跑；driver 重跑自动补 |
| 批量入池（给裸 ID 列表建库，不入 run） | 部分（SOP） | 无专门入口：循环 `quick_read_paper.py` 或走一次最小 run |

### 写作段

| 能力 | 状态 | 典型用法 |
|---|---|---|
| 完整综述（无人值守，标准入口） | 已实现 | `scripts/launch_review.py --topic ... --review-mode ... --time-range A..B [--target-style scientific-memo --scope-note ...]`：init → driver（重试+幂等续跑）→ writer agent 成稿 → 门禁（audit_citations + check_run_bundle，失败自动 continuation）→ settle → catalog/wiki 发布校验；`--run-dir` 对已有 run 续跑，`--status`/`--stop` 管生命周期 |
| 跨 run 综合（换问题重组既有证据） | 部分（组合式 SOP） | `build_review_packet.py --select-events-file <ids> --consolidate-evidence` 后仍需 writer agent 成稿；无专用 launcher 模式 |
| 换风格重写 / 修订成稿 | 已实现 | launcher `--target-style <style> --run-dir <已有 run>` 续跑 writer 阶段（run.json 声明单 `style`+`scope_note`） |

---

## 三条典型工作流

**1. 程序化出综述（无人值守，推荐入口）**

```bash
setsid nohup python3 scripts/launch_review.py \
  --topic "..." --review-mode systematic \
  --time-range 2023-01-01..2026-09-17 --focus "..." \
  --seed-arxiv-ids 2311.18259 \
  --arxiv-snapshot ~/Documents/arxiv/arxiv-metadata-oai-snapshot.sqlite \
  > /tmp/launch.log 2>&1 &
# 观察：scripts/launch_review.py --status --run-dir work/literature-review-<主题>-<日期>
```

产出：`work/<run>/` 内的成稿 + settle + `evidence/` 落库 + catalog 登记 + wiki 快照，一条龙。中断后 `--resume` 续跑。

**2. 交互式综述（claude 会话内）**

```bash
python3 scripts/init_run.py --topic ... --knowledge-id EA-DATA --time-range A..B --review-mode systematic
python3 scripts/run_review_pipeline.py --run-dir work/<run> --topic ... --review-mode systematic \
  --time-range A..B --focus ... --arxiv-snapshot ~/Documents/arxiv/arxiv-metadata-oai-snapshot.sqlite
# 之后 claude 接手判断阶段：packet → 成稿 → audit_citations → check_run_bundle → settle
# → 登记 knowledge/literature-review-catalog.md → build_research_wiki.py
```

**3. 单篇速读 / 论文对话**

```bash
python3 scripts/quick_read_paper.py --arxiv-id 2311.18259   # 入池+深读+速读卡
```

---

## 约定与不变量

- **全部 stdlib-only Python 3**（解释器 `python3`，`python` 不在 PATH）；每个脚本的合同用 `--help` 查看。
- 中间产物只进 gitignored 的 `work/`；settle 时按 run.json 的 `files` 清单拷核心文件进 `evidence/`（大 registry 需瘦身，见 run 内的 slim 说明）。
- driver 的 stdout 协议行 `[DRIVER-STAGE:<name>] ok <detail>` 与 `[PAPER] <id> ...` 是 wiki 工作流和外部监控的解析面，改格式需同步 `wiki_chat.py` 的映射。
- 离线检索：`--arxiv-snapshot` 接受 OAI JSONL 或 `search.py build-snapshot-db` 产出的 SQLite/FTS5 库；arXiv API 有 406 间歇封禁（curl 可过而 urllib 被拒），联网检索前先读 `scripts/lib/agent_invoke.py` 注释与记忆条目。
- 嵌套 claude 防护：凡从脚本里 spawn `claude -p`，必须剥掉 `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` / `CLAUDE_CODE_SSE_PORT`（`launch_review.py` 的 `strip_nested_claude_env` 是参考实现）。
- settle ≠ 完事：`check_run_bundle` 过 + status 翻 settled 之后，必须登记 `knowledge/literature-review-catalog.md` 并重建 wiki 快照，否则该 run 对读者不可见。
