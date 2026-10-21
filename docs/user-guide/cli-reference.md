# CLI 参考

全部命令行入口。每个子命令的完整 flag 表以 `--help` 为准（flag 名是契约，不会静默改名）。

## 六域 dispatcher

| 入口 | 域 | 位置 |
|---|---|---|
| `scripts/run.py` | 综述 run 生命周期 | init / 门禁 / settle / driver / launcher |
| `scripts/wiki.py` | Wiki 与站点 | 快照、静态站、知识图谱、链接审计、serve |
| `skills/embodied-ai-literature-hub/scripts/search.py` | 检索 | 查询计划、arXiv/S2、候选注册表、筛选、覆盖 |
| `skills/embodied-ai-literature-hub/scripts/fetch.py` | 抽取 | HTML/PDF/TeX 全文恢复、图文块 |
| `skills/embodied-ai-paper-reader/scripts/read.py` | 阅读 | 阅读包、深读笔记、速读、证据投影、论文池 |
| `skills/embodied-ai-review-writer/scripts/write.py` | 写作 | review-packet、审计、slide deck |

`embodied_learning/**` 库本身**没有 CLI**（ADR 0005）：只有 `run(args) -> int`，
flag 表与退出码全部在上面六个 dispatcher 里。`pip install .` 注册的控制台命令是这些入口的别名
（见[安装](installation.md)）。

> 老读者注意：consolidation 前的独立脚本（`build_query_plan.py`、`serve_research_wiki.py` 等）
> 已改成上述 dispatcher 的子命令，kebab-case 同名；`docs/adr/` 与已结算的 `evidence/` 交付物里
> 保留的是当时写法，不要照抄。

## `scripts/run.py`

| 子命令 | 作用 |
|---|---|
| `init` | 建 run 目录 + `status: in-progress` 的 `run.json` |
| `pipeline` | 机械阶段 driver：plan → 检索 → 注册 → 筛选 → 覆盖 → 抽取 → 包 → 深读 → 投影 |
| `launch` | 无头端到端：init → driver → 写作代理 → 审计门 → finalize；`--status` / `--resume` / `--stop` |
| `status` | 一次性 run 摘要（漏斗、逐篇证据、产物清单、下一步命令） |
| `check-bundle` | 打包完整性门（settle 前） |
| `audit-citations` | 引用审计门（死锚、越界引用、run.json 漂移） |
| `finalize` | 机械 settle：盖章 → 引用篇数地板门 → 两道门 → 发布 `evidence/` → catalog → wiki 快照 |
| `register` | 把已 settle 的 run 手工登记进 catalog |
| `next-event-id` | 下一个不冲突的证据事件 ID（含前缀预留） |
| `check-sink-integrity` | 对账 `work/` vs `evidence/` vs catalog |
| `validate-reviews` | 批量校验 catalog 中每个 run（CI 用，需完整 git 历史） |
| `token-meter` | 追加一条 token 计量记录（`EMBODIED_TOKEN_METER=1`） |

run 目录命名即契约：`literature-review-<topic>-<date>/`，其他命名不触发综述打包逻辑。

## `scripts/wiki.py`

| 子命令 | 作用 |
|---|---|
| `build-wiki` | 从 catalog 重建 wiki 内容快照 |
| `build-site` | 从快照构建静态研究站（**只接受 schema v2**） |
| `build-knowledge-map` | 渲染知识库图谱 |
| `build-mind-omni-reader` | 为单个 run 构建 mind-omni 阅读页 |
| `check-kb-links` | 审计 `knowledge/` 链接、source ID、locator（需完整 git 历史） |
| `kb-stats` | KB 盘点：runs / pool / wiki 数量与检索漏斗汇总 |
| `kb-search` | 跨 KB 子串检索（runs / papers / events / topics） |
| `kb-funnel` | 检索→证据漏斗：逐 run 统计，或 `--layer` 查某一层论文 |
| `kb-merge` | 把多个 KB 根的成果合并进目标根（先 `--dry-run`） |
| `serve` | 本地研究 Wiki |

快照 schema：

| 调用 | catalog 来源 | site-config | schema |
|---|---|---|---|
| `build-wiki`（无参） | **仓库** `knowledge/literature-review-catalog.md` | `wiki/site-config.json` | **v2**（公开部署） |
| `build-wiki --kb-root ~/Documents/arxiv` | 该 KB 的 catalog | 该 KB 的 `wiki/site-config.json`（有才用） | v1 或 v2 |
| `build-wiki --source ... --site-config ...` | 显式指定 | 显式指定 | 视配置而定 |

CI 的部署 workflow 走第一行——这正是 SEO/GEO 链路的入口，改默认值会打断发布。

## `skills/.../search.py`

`build-query-plan`, `build-snapshot-db`, `search-arxiv`, `search-semantic-scholar`,
`expand-via-citations`, `build-candidate-registry`, `screen-candidates`, `select-candidates`,
`assess-review-coverage`, `rank-influential-papers`, `rank-problem-relevance`,
`parse-browser-candidates`, `harvest-curated-list`, `plan-cache`, `persona-context`,
`persona-suggest`, `registry-titles`

要点：

- planner 的 `start_date`/`end_date` 只是范围元数据；**实际日期过滤看 `search-arxiv --start-date/--end-date`**。
- `search-arxiv --query-file` 只读 plan 顶层的 `queries`（`browser_fallback_queries` / `web_calibration_queries` 走别的通道）。
- `build-snapshot-db` 建一次离线检索库；`--metadata-snapshot` 接收 JSONL 或 SQLite。
- `registry-titles` 只打印标题切片——**不要**把整个 `candidate-registry.json` 塞进模型上下文。

## `skills/.../fetch.py`

`extract-arxiv-html`, `extract-arxiv-pdf`, `extract-arxiv-tex`, `download-arxiv-source`,
`extract-content-queue`, `extract-content`, `write-lit-outputs`, `render-figure-table-block`

要点：默认 transport 是 arxiv2md（公开 REST API）；`--transport s3-tex` 需要 AWS 凭证
（requester-pays 桶，TODO）。全文缓存写在仓库之外。

## `skills/.../read.py`

`build-reading-packet`, `build-paper-note`, `quick-read`, `prepare-chat`,
`extract-failed-card-window`, `update-reading-ledger`, `validate-paper-note`,
`audit-claim-support`, `project-evidence-events`, `pool-add-paper`

要点：`quick-read` / 深读相关在精读不可用时退出码 `3`；`prepare-chat` 允许降级。

## `skills/.../write.py`

`review-packet`, `build-trace-map`, `audit-article-quality`, `audit-zhihu-corpus`,
`audit-slide-deck`, `check-deep-read-budget`, `project-outline-evidence`,
`compile-slide-deck`, `paper-deck`, `run-deck`

要点：

- `review-packet` 是**简报生成器，不是作者**：产出 `review-packet.md` + `writing-brief.md` +
  `evidence-appendix.md`。三篇成稿永远由代理从 `writing-brief.md` 写，不发脚本的机械渲染
  （`--emit-scaffold` 只产出带横幅的 `*.scaffold.md`）。
- stance 配额默认 support 8 / limit 6 / conditional 6 / gap 4（`--uncapped-writer` 仅调试）。
- slide deck：代理只写 slide-source DSL，HTML 由 `compile-slide-deck` 编译。

## 环境变量

| 变量 | 作用 |
|---|---|
| `EMBODIED_KB_LOCK_{DIR,WAIT,STALE,POLL}` | 共享 KB 锁参数 |
| `EMBODIED_KB_LOCKS_DISABLED=1` | 紧急把锁退化为 no-op |
| `EMBODIED_TOKEN_METER=1` | 开启 token 计量 → `work/<run>/token-meter.jsonl` |

## 调用约定

- 解释器是 `python3`（`python` 可能不在 PATH）。
- AI 调用**只**走 `embodied_learning/harness/claude.py`；不要自己 `subprocess` 起 `claude`。
- 共享文件的读-改-写走 `embodied_learning/atomicio.py` + `.locks/`；run 目录内产物无锁。
- 慢通道默认关（S2 keyword 检索等），要快先用默认，要全显式 opt-in（如 `--with-s2`）。
