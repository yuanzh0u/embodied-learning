# 综述流水线

从研究问题到已发布综述。两条主线：**无头 launcher**（推荐）与**机械 driver**。

## 两条主线怎么选

| | `run.py launch` | `run.py pipeline` |
|---|---|---|
| 覆盖 | init → driver → 写作 agent → 审计门 → settle → catalog → wiki 快照 | 只做机械阶段（plan → 检索 → … → 投影） |
| 谁写成稿 | 无头 `claude -p` writer agent | 没人；产出 `writing-brief.md` 交给你 |
| 幂等 | `.launch/*.done` 标记 + driver 幂等，`--resume` 续跑 | 每阶段产物存在即跳过 |
| 失败重试 | driver 3 次 + writer 门禁 2 轮 continuation | 无（退出码交给你） |
| 场景 | **程序化 / 无人值守** | 交互式综述，或想手动分阶段控制 |

一句话：想一条命令出已发布综述用 `launch`；想自己（或交互式 Claude）做判断阶段用 `pipeline`。

## 无头端到端：`run.py launch`

```bash
python3 scripts/run.py launch \
  --topic "近半年具身智能中的数据时空一致性" \
  --review-mode scoping \
  --time-range 2025-01-01..2026-06-06 \
  --focus "时空一致性定义、采集约束、评测方式" \
  --knowledge-id EA-DATA \
  --kb-root ~/Documents/arxiv
```

关键参数：

| 参数 | 说明 |
|---|---|
| `--review-mode` | `rapid`（12 篇精读）/ `scoping`（22）/ `systematic`（43） |
| `--time-range` | `YYYY-MM-DD..YYYY-MM-DD`，实际过滤在这里，不是 query plan 里 |
| `--search-strategy` | `smart`（默认，代理选题）/ `fast` / `seeds` |
| `--selection-strategy` | `smart-jev`（决策模型 jev 选文，默认：逐篇概率判定，数秒完成）/ `smart`（执行模型选文，未配置 jev 时的回退）/ `keywords` / `influence` / `bm25` |
| `--selection-model` | `smart` 使用的执行模型（默认 harness 的 `DRIVER_AGENT_MODEL`；采访卡的 ⑧ 执行模型即此项）；`smart-jev` 忽略它 |
| `--selection-threshold` | `smart-jev` 的保留阈值（默认 `0.60`；jev 概率 ≥ 阈值入队） |
| `--seed-arxiv-ids` | 给定种子论文，强制排到深读队列最前 |
| `--arxiv-snapshot` | 离线检索：OAI 快照 JSONL 或 SQLite/FTS5 库 |
| `--kb-root` | 目标知识库；run 落在 `<kb-root>/work/` |
| `--target-style` + `--scope-note` | 只交付单一文体（否则三文体） |

`smart-jev` 是默认选文策略，需要 System One 端点的环境变量（只走环境，不写配置文件）：
`EMBODIED_SYSTEM_ONE_URL`（缺省时取 `ANTHROPIC_BASE_URL` + `/v1/systemone`）与
`EMBODIED_SYSTEM_ONE_API_KEY`（缺省时取 `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY`）。
未配置时 `launch` / `pipeline` 会在开跑前报错，不会跑到选文阶段才失败；
此时显式传 `--selection-strategy smart` 走执行模型。

后台跑法（推荐，防终端断开）：

```bash
setsid nohup python3 scripts/run.py launch ... > /tmp/launch.log 2>&1 &
```

### 观察进度

```bash
python3 scripts/run.py status --run-dir <run-dir>
python3 scripts/run.py launch --status --run-dir <run-dir>
```

`status` 给漏斗数字（候选 → 选文 → 全文 → 深读 → 证据论文）、逐篇证据、产物清单和
**下一步可执行命令**。不用逐个翻 `evidence/*.jsonl`。同一个漏斗也在 driver 收尾时落成
`<run>/funnel.json` 并随 `finalize` 发布，可用 `wiki.py kb-funnel` 跨 run 查询（见下）。

### 断点续跑

```bash
python3 scripts/run.py launch --resume --run-dir <run-dir>
python3 scripts/run.py launch --stop    --run-dir <run-dir>   # 请求停止
```

阶段标记在 `<run-dir>/.launch/`。换参数重跑同一 run = 证据代际替换，先想清楚。

## 机械 driver：`run.py pipeline`

```bash
python3 scripts/run.py pipeline \
  --run-dir ~/Documents/arxiv/work/literature-review-<主题>-<日期> \
  --topic "..." --review-mode scoping \
  --time-range 2024-01-01..2026-06-06 --focus "..."
```

阶段顺序：

```
plan → retrieval → registry → screening → coverage
     → extraction → packets → deep read → projection
     → funnel.json → pipeline-summary.json
```

- **种子优先**：`--seed-arxiv-ids` 的论文强制排到深读队列最前。
- **模式感知 limit**：rapid 12 / scoping 22 / systematic 43。
- **饱和是测出来的**：多轮检索合并候选，coverage 终态重算，不是断言停止。
- **证据地板**：可投影篇数不足地板时从候补按评分补读；仍不足则停轮汇报（不薄审落盘）。
- `--skip-deep-read`：深读交给外部编排（交互式 Claude 会话）。

跑完后交互式 Claude 接手判断阶段：

```bash
# 1. 生成写作简报包
python3 skills/embodied-ai-review-writer/scripts/write.py review-packet \
  --topic "..." --knowledge-id EA-DATA \
  --evidence-jsonl <run-dir>/evidence.jsonl

# 2. 人工/代理成稿（三文体，见 writing-brief.md）
# 3. 审计门（成稿阶段 run 还是 in-progress，check-bundle 必须带 --pre-settle）
python3 scripts/run.py check-bundle <run-dir> --pre-settle
python3 scripts/run.py audit-citations \
  --article <run-dir>/scientific-memo_keyan.md \
  --article <run-dir>/zhihu-explainer_zhihu.md \
  --article <run-dir>/xiaohongshu-post_xiaohongshu.md \
  --appendix <run-dir>/evidence-appendix.md \
  --evidence-jsonl <run-dir>/evidence.jsonl \
  --run-json <run-dir>/run.json

# 4. settle（盖章 → 引用篇数地板门 → 两道门 → 落库 → catalog → wiki 快照）
python3 scripts/run.py finalize --run-dir <run-dir> --kb-root ~/Documents/arxiv
```

门禁失败是**修复后重跑**的条件，不是停止理由。

## 离线检索

arXiv 被限流或无外网时，用本地元数据快照：

```bash
# 一次性构建（分钟级）
python3 skills/embodied-ai-literature-hub/scripts/search.py build-snapshot-db \
  --snapshot-jsonl ~/Documents/arxiv/arxiv-metadata-oai-snapshot.jsonl \
  --db ~/Documents/arxiv/arxiv-metadata-oai-snapshot.sqlite

# 之后每轮检索秒级
python3 scripts/run.py launch ... \
  --arxiv-snapshot ~/Documents/arxiv/arxiv-metadata-oai-snapshot.sqlite
```

快照库可以放在 CIFS 局域网共享盘上多机共用。默认禁止本地回退（避免一半在线一半离线的混合语料）。

## review-mode 与地板

| 模式 | 深读上限 | 引用篇数地板（finalize 门禁） |
|---|---:|---:|
| `rapid` | 12 | 6 |
| `scoping` | 22 | 10 |
| `systematic` | 43 | 15 |

地板数的是**不重复的已引用论文**。不足则 `finalize` 提示续跑 driver 补深读。

## 检索漏斗：六层口径

一次 run 的检索判断被固化成六层。每层的产出者、判据与失败语义：

| 层 | 谁产出 | 判据 | 失败/缺失语义 |
|---|---|---|---|
| `registry` | 检索 + 候选注册 | `candidate-registry.json` 的候选（多轮合并后） | 检索失败 → 候选 0，这是唯一允许的早停 |
| `screened` | 选文（smart / smart-jev / influence / keywords / bm25） | `screening-ids.txt`：策略判定相关的论文，**不按数量截断** | 选文 chunk 超时 → 覆盖缺口记入 `[DRIVER-WARN]`，其余照常 |
| `full_text` | 全文抽取队列 | `extraction-summary.json` 中 `evidence_eligible` 且 ∈ 选文 | 不可用 → `held`（暂扣）；通道故障 → `channel_down`，单列 |
| `deep_read` | 深读骨架（受模式预算约束） | `paper-notes/<id>.json` ∪ `<id>.failed.json`（**尝试过**的论文） | 审计不过 → `needs_review`；骨架失败 → `failed`；不虚报队列上限 |
| `evidence` | 投影 + claim-support audit | `evidence/*.jsonl` 非空（不含摘要级 tier） | 通过审计的论文才可引用 |
| `abstract` | 摘要级投影 | `evidence/abstract-tier.jsonl` | 见下方「摘要级范围」 |

三个口径要点：

- **摘要级只面向选文结果。** `abstract-tier` 的对象是 `screening-ids.txt` 通过集合（含抽取失败被 `held` 的论文），**不是** `candidate-registry.json` 全量。选文排除的论文不进入附录「摘要级相关工作」。缺 `screening-ids.txt` 时该阶段跳过并告警，**不回退全量**。摘要级事件共享唯一锚点 `#摘要级相关工作`，不计入引用篇数地板。
- **全文缓存落在 KB 里。** driver 把 HTML/PDF 缓存指到 `<kb-root>/.cache/{html,pdfs}`：早先 run 或速读抓过的论文直接复用，同一 KB 挂载上的其他机器也命中。arXiv 仍是机器级串行限速（3s/请求），所以 N 篇的**理论下限**约 `N × 3s`；并行只摊薄下载/解析时间，不突破礼貌速率。
- **漏斗不是严格嵌套。** `--seed-arxiv-ids` 的种子论文强制排在深读队列最前、可以不在选文集合内；差值记在 `funnel.json` 的 `detail.seeds_outside_screened`。
- **`deep_read` 数的是尝试数**，不是模式预算（rapid 12 / scoping 22 / systematic 43）。被中断的 run 不能报「已读完预算」。

上下游消费：driver 收尾写 `<run>/funnel.json`，`finalize` 随 bundle 发布；`wiki.py kb-stats` 汇总、`wiki.py kb-funnel` 查询逐 run 统计或某一层的论文（字段契约见 [KB 盘点](../kb-inventory.md)）。历史 run 不回填，缺数据标 `null`。

## 证据纪律

- Candidate ≠ Evidence：候选论文永远不是正式证据。
- 浏览器/网页/社媒结果只是低置信度校准，不能升格为证据。
- 升格条件：arXiv 全文（HTML 正文）核验过，且 claim-support audit 通过。
- 标签词表固定：stance = `support` / `limit` / `conditional` / `gap`；
  confidence = `direct` / `citation-supported` / `inference`。

## 常见失败与处置

| 现象 | 处置 |
|---|---|
| 检索失败 / 候选为 0 | 早停（唯一允许的提前停止），run 留 `in-progress`，说清缺什么 |
| 精读数量不够地板 | 停轮，汇报已精读列表，等用户决策（扩大范围/补充信息），**不**薄审落盘 |
| 门禁（bundle / citation）失败 | 修复成稿或 run.json 后重跑门禁 |
| 选文 chunk 超时 | 已记覆盖缺口并继续；见日志 `[DRIVER-WARN]` |
| 重复 launch | 先查重！并发 launch 会截断 registry |

## 相关文档

- [单篇工具](single-paper.md)：速读 / 汇报 deck / 论文对话
- [Wiki 使用](wiki.md)：在浏览器里跑工作流
- `scripts/README.md`：驱动内部阶段、锁与 harness 细节
