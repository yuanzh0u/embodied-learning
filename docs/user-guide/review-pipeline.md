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
| `--selection-strategy` | `smart` / `keywords` / `influence` / `bm25` |
| `--seed-arxiv-ids` | 给定种子论文，强制排到深读队列最前 |
| `--arxiv-snapshot` | 离线检索：OAI 快照 JSONL 或 SQLite/FTS5 库 |
| `--kb-root` | 目标知识库；run 落在 `<kb-root>/work/` |
| `--target-style` + `--scope-note` | 只交付单一文体（否则三文体） |

后台跑法（推荐，防终端断开）：

```bash
setsid nohup python3 scripts/run.py launch ... > /tmp/launch.log 2>&1 &
```

### 观察进度

```bash
python3 scripts/run.py status --run-dir <run-dir>
python3 scripts/run.py launch --status --run-dir <run-dir>
```

`status` 给漏斗数字（候选 → 全文 → 精读 → 证据事件）、逐篇证据、产物清单和
**下一步可执行命令**。不用逐个翻 `evidence/*.jsonl`。

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
     → pipeline-summary.json
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
# 3. 审计门
python3 scripts/run.py check-bundle <run-dir>
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
