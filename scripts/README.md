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
| `finalize_run.py` | **机械 settle 一条龙**：盖章 run.json（event_count/evidence_papers/candidate_count/full_text_count、files.evidence、单风格 style+scope_note）→ 引用篇数下限门禁（rapid 6 / scoping 10 / systematic 15，不足则提示续跑 driver 补深读）→ 两道门 → 拷贝 evidence/ → 翻 settled → 登记 catalog → 重建 wiki 快照。幂等；门禁失败打印缺失项（修复重跑，不是停止理由） | `finalize_run.py --run-dir work/<run> --kb-root <kb-root>` |
| `run_status.py` | **run 现状一次性摘要**（替代 agent 逐文件循环）：漏斗数字、逐篇证据与 claim 摘要、从 candidate-registry join 的 References 作者/年份元数据、逐篇深读漏斗（held / deep-read-failed 及筛选命中词）、产物清单、引用篇数下限核对、建议命令——含**逐字可执行的综述包完整命令**；`--json` 出机器可读 | `run_status.py --run-dir work/<run>` |
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
| `paper_slide_deck.py` | 单篇组会汇报（汇报展示）：保证入池+深读（强制），agent 写 slide-source，编译 `slide-deck_report.html`（reveal.js 单文件） | `paper_slide_deck.py --arxiv-id 2302.01109` |
| `run_slide_deck.py` | run 级汇报（汇报展示）：从 run 目录的 writing-brief + evidence-appendix 生成，引文键 = 附录 References 的 arXiv ID，agent 写 slide-source 后编译+审计 | `run_slide_deck.py --run-dir <run-dir>` |
| `prepare_paper_chat.py` | 为 Wiki「论文对话」备料：保证入池+深读（与速读同链路，不做卡片） | 由 wiki `/api/paper/chat` 内部调用 |
| `build_paper_note.py` | 深读组装器：agent 只出速记骨架，它负责 locator 解析/逐字校验/组装/审计 | 由 driver 的深读阶段调用；单篇手跑 `build_paper_note.py --help` |

### D. 共享库 `scripts/lib/`

| 模块 | 作用 |
|---|---|
| `agent_invoke.py` | **兼容 shim**：re-export `embodied_learning.harness.claude` 全部调用原语；自留深读/骨架 prompt 与解析、`pool_root_for`（机械代码） |
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
| 单篇组会汇报（reveal.js） | 已实现 | `scripts/paper_slide_deck.py --arxiv-id <id>`（强制入池+深读，产出 `slide-deck_report.html`；编译器 `skills/embodied-ai-review-writer/scripts/build_slide_deck.py`，审计 `writing_audit.py audit-slide-deck`） |
| run 级汇报（wiki 话题页） | 已实现 | wiki「汇报放映」按钮（无 deck 时确认后生成，走 `serve_research_wiki.py /api/deck/generate` → `scripts/run_slide_deck.py`）；也可手跑 `run_slide_deck.py --run-dir <dir>`，生成后重建快照点亮入口 |
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
# 之后 claude 接手判断阶段：packet（build_review_packet.py --run-dir work/<run>）→ 成稿 → 审计
# → python3 scripts/finalize_run.py --run-dir work/<run> --kb-root <kb-root>
#   （盖章 run.json + 引用篇数门禁 + 两道门 + evidence/ 落库 + 翻 settled + 登记 catalog + wiki 快照，一条龙幂等）
```

**3. 单篇速读 / 论文对话**

```bash
python3 scripts/quick_read_paper.py --arxiv-id 2311.18259   # 入池+深读+速读卡
```

---

## 约定与不变量

- **全部 stdlib-only Python 3**（解释器 `python3`，`python` 不在 PATH）；每个脚本的合同用 `--help` 查看。
- **布局解析只走 `lib/layout.py`**：仓库检出与 wheel 安装（`wiki_scripts` 包目录自带打包的 `skills/` 树）两种布局都成立；禁止新增 `Path(__file__).parent.parent` 式的 REPO_ROOT 猜测——装到 site-packages 后全部失准。wheel 是自包含的：`pyproject.toml` 把 `skills/` 打成 `wiki_scripts.skills` 包数据（SKILL.md/references/agents/scripts，tests 不进包）。
- **spawn 的 claude 代理必须隔离**：cwd=kb_root、env 走 harness 的 `isolated_claude_env()`（剥 `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` / `CLAUDE_CODE_SSE_PORT` + 重定向 `CLAUDE_CONFIG_DIR` 到 `~/.cache/embodied-learning/claude-config`，凭据自动播种）——代理只能看到 KB 与打包内容，看不到 launcher 会话的记忆/代码库；认证缺失用 `claude_auth_ready()` 提前报错。

## AI 调用 harness（pybind 式绑定层）

**任何需要模型能力的代码一律经 `embodied_learning/harness/claude.py` 调用，其余模块只维护机械确定性代码**（prompt 内容与输出解析归各功能模块，spawn/env/鉴权/转录/归档归 harness）。新增模型后端 = 在 `harness/` 加兄弟模块，调用方不动。接口面：

| 入口 | 用途 |
|---|---|
| `complete(prompt, *, timeout_s, model, cwd, label, stream=False, stream_to=None)` | one-shot 文本完成（writer/速读/汇报/骨架/引文扩张）；`stream=True` 切 stream-json，`stream_to` 落文件 |
| `ChatTurn` | 交互式流式回合（wiki 主题/工作流聊天） |
| `resolve_cli` / `claude_auth_ready` / `isolated_claude_env` | CLI 发现、鉴权预检、隔离 spawn 环境 |
| `build_claude_command` / `parse_stream_line` / `is_resume_failure` | 命令组装与 stream-json 协议解码 |
| `conversation_store` / `record_agent_invocation` | 机器本地调用归档（`~/.claude/projects/embodied-learning-work/`） |

铁律：**任何模块禁止直接 `subprocess` spawn `claude`**（历史上 launch_review 的 writer 旁路已被收编）；`scripts/lib/agent_invoke.py` 保留为兼容 shim，新代码直接 `from embodied_learning.harness import claude`。
- 中间产物只进 gitignored 的 `work/`；settle 时按 run.json 的 `files` 清单拷核心文件进 `evidence/`（大 registry 需瘦身，见 run 内的 slim 说明）。
- driver 的 stdout 协议行 `[DRIVER-STAGE:<name>] ok <detail>` 与 `[PAPER] <id> ...` 是 wiki 工作流和外部监控的解析面，改格式需同步 `wiki_chat.py` 的映射。
- 离线检索：`--arxiv-snapshot` 接受 OAI JSONL 或 `search.py build-snapshot-db` 产出的 SQLite/FTS5 库；arXiv API 有 406 间歇封禁（curl 可过而 urllib 被拒），联网检索前先读 `scripts/lib/agent_invoke.py` 注释与记忆条目。
- 嵌套 claude 防护：凡从脚本里 spawn `claude -p`，必须剥掉 `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` / `CLAUDE_CODE_SSE_PORT`（`lib/agent_invoke.py` 的 `isolated_claude_env` 是唯一参考实现）。
- settle ≠ 完事：`check_run_bundle` 过 + status 翻 settled 之后，必须登记 `knowledge/literature-review-catalog.md` 并重建 wiki 快照，否则该 run 对读者不可见。

## 共享知识库的并发与锁（CIFS 安全）

KB 可能整体部署在局域网 CIFS 挂载上（如 `/mount/TEST/public/wiki/`），多人跨机器、同机多终端/多端口并发使用。所有跨进程协调只走两类原子原语（`embodied_learning/locks.py` + `embodied_learning/atomicio.py`），**禁止 `fcntl.flock` 做 KB 锁**（CIFS 上跨机不可靠；`ratelimit.py` 的 flock 闸门只管本机出站请求，职责不同）：

| 锁名 | 保护范围 | 默认等待 |
|---|---|---|
| `pool-index` | `pool/index.jsonl` 的读-合并-重写（`PaperPool.add`/`import_existing`） | 120s，超时报错 |
| `pool-paper__<dir>` | 单篇论文的 pool 目录写（深读 note 三连写、速读卡、抽取） | 120s |
| `catalog` | `literature-review-catalog.md` 追加（`register_run.py`，幂等） | 120s |
| `run__<run>` | run.json 读改写；**驱动全程持有且 fail-fast**（重复 launch 直接报持有者退出，不等待） | 0 / 6h 陈旧回收 |
| `wiki-publish` | wiki 快照发布全程（快照 ID 带 uuid 后缀，prune 有 10 分钟最小年龄下限） | 600s |
| `wiki-chat-sessions` | `chat-sessions.json` 读改写——**已迁至机器本地** `~/.claude/projects/embodied-learning-work/`（对话历史属本机缓存，跨机共享无收益却把最高频写压上共享盘；旧共享文件在服务首次启动时自动迁移过来） | 30s |
| `kb-bootstrap` | 冷启动建骨架 + 前端同步 | 60s |

机制与约定：

- 锁文件在 `<kb-root>/.locks/<name>.lock`，`O_CREAT|O_EXCL` 原子创建（CIFS 服务端保证原子性），内容为持有者 JSON（host/pid/ts/cmd/claim_id）；等待方约 10s 打一行进度到 stderr，超时 `LockTimeout` 带持有者与解锁指引。
- 遗留锁四条抢占路径：**客户端缓存幽灵/缓存谎言即时清除**（NAS 缓存已删文件的死 dentry：`stat` 说在但 `st_nlink==0`——POSIX 保证真实文件 nlink≥1；该 NAS 的谎言还有别的形态——stat ENOENT 或 nlink=1 但打不开——所以 **EEXIST 后连续 3 个轮询都读不到持有者记录就无条件 unlink 清缓存重试**，活跃持有者毫秒级写入记录、绝不积累此 streak）；**同机持有进程已死立即抢占**（owner 记录 host=本机且 pid 经 `kill 0` 验证不存在——崩溃的 driver/发布进程不用等 TTL 就能重跑）；**持有者记录不可读（空/损坏）超过宽限即抢占**（宽限随调用方 `wait` 自适应：`max(2×poll, min(wait, stale, 60s))`，保证抢占先于超时触发）；跨机持有者无法探测，按 `EMBODIED_KB_LOCK_STALE`（默认 900s）TTL 抢占。固定 `.steal` 标记 O_EXCL 决出唯一抢占者；释放时校验 claim_id，误抢活跃持有者可恢复（pid 复用会暂时掩盖遗留锁，由 TTL 兜底）。这台 NAS（192.168.3.2）已实测会出幽灵 dentry 与多形态缓存谎言，重挂务必加 `noleases`/`actimeo=0`。
- 事件 ID 前缀预留走 `<kb-root>/.claims/event-prefix/<PREFIX>.json`（永久保留，不 GC）：`next_event_id.py --claim-prefix <P> --run <run>`；驱动在投影前自动 claim，冲突自动加后缀，`run.json` 记 `event_prefix`。
- 嵌套规则：`pool-paper__*` 可嵌套于 `pool-index` 内，反向禁止；其余锁互不嵌套。
- 环境旋钮：`EMBODIED_KB_LOCK_DIR` / `EMBODIED_KB_LOCK_WAIT` / `EMBODIED_KB_LOCK_STALE` / `EMBODIED_KB_LOCK_POLL` / `EMBODIED_KB_LOCKS_DISABLED=1`（紧急逃生口，全部 no-op）。
- **锁是协作式的**：某台机器跑旧代码会无视 `.locks/`，行为退化为无锁现状（不会更糟）；两台机器指向不同 KB root 时锁自然不共享。
- 不加锁的写：`work/<run>/` 全部产物、`evidence/<run>/` 内容、只读检查器、sqlite 快照读。口诀：**只锁共享文件的读-合并-重写，per-run 产物不加锁**；所有共享文件的重写一律走 `atomicio`（tmp + `os.replace`），读者永不看到半写状态。

## 对话记录归档（机器本地）

所有 claude 交互——主题聊天、子代理综述 writer、速读、汇报制作、深读骨架——统一归档在 **`~/.claude/projects/embodied-learning-work/`**（env `EMBODIED_CONVERSATION_STORE` 可重定向，仅测试用）：

- `invocations.jsonl`：逐次调用索引（kind/label/model/cwd/returncode/时长）。
- `<kind>/<时间戳>-<pid>-<label>/`：每次调用的 `prompt.md`、`output.txt`（one-shot 含 stderr）、`meta.json`；`kind` 分 `one-shot`（`lib/agent_invoke.run_one_shot_agent` 的所有调用方：writer、速读、深读骨架、汇报 slide-source、引文扩张 agent 等，可用 `label` 标注论文 ID/run 名）与 `chat`（wiki 主题/工作流聊天的原始 stream-json 转录，`wiki_chat.ChatTurn`）。
- `chat-sessions/<kb-hash>/chat-sessions.json`：wiki 对话历史的机器本地缓存（按 kb-root 哈希分库；同机多端口同 KB 共享一份）。共享 KB 上只保留**成果输出**：evidence/、pool/、knowledge/、work/<run>/、wiki 快照。
