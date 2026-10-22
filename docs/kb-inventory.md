# KB 盘点、检索与跨根合并

给定一个知识库根（kb-root），统计跑了多少 run、多少论文有全文/精读，支持子串检索，并可将多个根的成果合并到一个目标根。库可调用 + CLI + 本文档。

## 对象模型

```
<kb-root>/
  evidence/<run>/          run.json + evidence.jsonl + 三成稿 + funnel.json + revisions/
  pool/<dir>/              meta.json + extraction.json + paper.md + note.json
  knowledge/               literature-review-catalog.md + {embodied-ai,error-governance}/*.md
  wiki/data/               snapshots/<id>/{manifest.json,topics/*.json}
  wiki/site-config.json    slug / 品牌配置（可选）
```

| 类 | 职责 |
|---|---|
| `KnowledgeBase` | 聚合根：`open(root)` 后惰性扫描 runs / papers / cards / catalog / wiki_topics |
| `ReviewRun` | 一个 `evidence/<run>/` 目录：manifest、events、deliverables（含 revisions） |
| `PoolPaper` | 一个 `pool/<dir>/` 目录：`has_full_text`（paper.md 存在）、`has_deep_read`（note.json 存在）、`in_index` |
| `TopicCard` | `knowledge/{embodied-ai,error-governance}/*.md` 路由卡 |
| `WikiTopic` | 已发布话题（wiki 快照的显示单元） |
| `Catalog` | `knowledge/literature-review-catalog.md` 成果索引 |

职责边界：**`knowledge/` 管数据结构 + 下游消费**（stats / search / merge）；`wiki/publish/` 管显示阅读；`wiki/run/` 管单篇综述生成工作流。

## kb-stats — 盘点

回答"这个根有多少 run、多少论文有精读/全文"。

```bash
python3 scripts/wiki.py kb-stats                           # 默认 ~/Documents/arxiv
python3 scripts/wiki.py kb-stats --kb-root /mount/TEST/public/wiki
python3 scripts/wiki.py kb-stats --json                    # 机器可读
python3 scripts/wiki.py kb-stats --runs-detail             # 附逐 run 明细表
```

输出口径：

| 指标 | 判据 |
|---|---|
| `runs.total` | `evidence/*/run.json` 文件数 |
| `pool.full_text` | `pool/<dir>/paper.md` 存在 |
| `pool.deep_read` | `pool/<dir>/note.json` 存在（**存在性，非审计通过**） |
| `pool.not_in_index` | 目录在磁盘但不在 `pool/index.jsonl`（漂移检测） |
| `wiki.published_topics` | 当前快照 `topics/*.json` 文件数 |
| `reading.*` | 跨 run 的 `reading-ledger.jsonl` 行数求和，**非去重论文** |

JSON 契约（`schema_version: 1`）：

```json
{
  "schema_version": 1,
  "kb_root": "/home/ming/Documents/arxiv",
  "generated_at": "2026-10-15T…",
  "runs": {
    "total": 29,
    "by_status": {"settled": 29},
    "by_review_mode": {"rapid": 13, "scoping": 11, "systematic": 5},
    "registered_in_catalog": 29,
    "unregistered": 0,
    "total_events": 5348,
    "sum_evidence_papers": 227
  },
  "pool": {
    "papers": 1766,
    "in_index": 1765,
    "not_in_index": ["arxiv-2605.11709"],
    "full_text": 1760,
    "deep_read": 858,
    "full_text_and_deep_read": 854,
    "deep_read_without_full_text": 4
  },
  "wiki": {"published_topics": 29, "superseded_versions": 0, "snapshot_id": "…"},
  "reading": {"runs_with_ledger": 14, "ledger_rows": 235, "accepted_rows": 152},
  "funnel": {
    "runs_with_funnel": 0,
    "runs_without_funnel": 135,
    "sums": {"candidates": 0, "screened": 0, "full_text": 0,
             "deep_read": 0, "evidence_papers": 0, "abstract_papers": 0},
    "rates": {"screen": null, "full_text": null, "deep_read": null, "evidence_yield": null},
    "note": "跨 run 求和口径，非去重；空分母或该层 null 时为 null"
  }
}
```

`funnel` 是 **v1 的加法扩展**（`schema_version` 仍为 1）：只在 `funnel.json` 出现之后才有非零值，仓内无消费者按版本分支。求和是**跨 run 的求和，不是去重论文数**——漏斗度量的是 run，同一篇论文被两个 run 选中会各计一次。某层从未被任何 run 报告（例如全部是旧 run）时，对应率是 `null` 而非 `0.0`：没跑过深读不等于深读产出为零。

`--runs-detail` 时额外输出 `runs_detail` 数组（每 run 的 topic / status / mode / event_count / papers / deep_read_count，以及 `funnel`：该 run 的 `funnel.json` 内容，无则 `null`）。

## kb-search — 检索

子串检索（大小写不敏感），空格分词为 AND。不用 regex。

```bash
python3 scripts/wiki.py kb-search "外参标定" --scope events --limit 5
python3 scripts/wiki.py kb-search "LiDAR" --scope papers
python3 scripts/wiki.py kb-search "标定" --scope all --json
```

| scope | 检索字段 |
|---|---|
| `runs` | topic, run name, review_mode, status, notes, time_range, knowledge_ids |
| `papers` | title, dir_name, arxiv_id, published |
| `events` | claim, evidence.summary, paper.title, paper.arxiv_id, topic_id, event_id |
| `topics` | title, topic_key, excerpt, field |
| `all` | 以上全部（每范围各限 `--limit`，默认 20） |

字段命中 = 所有 term 是该字段的子串；记录命中 = 任一字段命中。

## kb-funnel — 检索→证据漏斗

一次综述 run 的检索漏斗（候选 → 选文 → 全文 → 深读 → 证据）是检索阶段最贵的判断产物。它落成每 run 的 `funnel.json`（driver 收尾写，`run.py finalize` 随 bundle 发布），由 `kb-funnel` 提供两种查询：**逐 run 统计**与**某一层的论文明细**。

```bash
python3 scripts/wiki.py kb-funnel                                  # 逐 run 一行
python3 scripts/wiki.py kb-funnel --layer screened --run <run>     # 某 run 的选文篇目
python3 scripts/wiki.py kb-funnel --layer deep_read --review-mode systematic --json
python3 scripts/wiki.py kb-funnel --sort evidence_yield --limit 5  # 证据产出率最高的 run
```

| flag | 作用 |
|---|---|
| `--layer L` | 切换到层查询；`L ∈ registry / screened / full_text / deep_read / evidence / abstract` |
| `--run NAME` | 只保留该 run（层查询时通常必带） |
| `--topic 子串` / `--review-mode M` | 过滤 run |
| `--sort run\|screened\|screen_rate\|evidence_yield` | 逐 run 行排序；数值降序，`null` 恒排最后；默认 `run` 升序 |
| `--limit N` | 返回行数上限，默认 20 |
| `--json` | 机器可读输出 |

逐 run 行含 `stages`（`candidates / screened / full_text / deep_read / evidence_papers / evidence_events / abstract_papers / abstract_events`）、`rates`、`funnel_available`。旧 run 没有 `funnel.json` 时 `stages` 与 `rates` 为 `null`、`funnel_available` 为 `false`，**退出码仍是 0**：缺数据是事实，不是错误。

**与 `kb-search` 分工**：文本检索走 `kb-search`，数值筛选与分层篇目走 `kb-funnel`。

### `funnel.json` 契约（`schema_version: 1`）

```json
{
  "schema_version": 1,
  "run": "literature-review-<主题>-<日期>",
  "topic": "<主题>",
  "review_mode": "systematic",
  "generated_at": "2026-10-20T…",
  "stages": {"candidates": 308, "screened": 200, "full_text": 191,
             "deep_read": 48, "evidence_papers": 23, "evidence_events": 88,
             "abstract_papers": 200, "abstract_events": 200},
  "detail": {"selection_strategy": "influence", "deep_read_pass": 23,
             "deep_read_needs_review": 21, "deep_read_failed": 4,
             "held": 9, "channel_down": 0, "seeds_outside_screened": 0,
             "abstract_basis": "screened", "abstract_leaked": 0,
             "cited_floor": 15, "floor_met": true, "skipped": []},
  "papers": {"2402.10329": {"title": "UMI…", "published": "2024-02-16", "reason": "…"}},
  "layers": {"registry": ["…"], "screened": ["…"], "full_text": ["…"],
             "deep_read": ["…"], "evidence": ["…"], "abstract": ["…"]},
  "truncated": false
}
```

自包含：`layers` 存每层论文 id，`papers` 存标题/日期/选文理由——因为 `screening.json` / `extraction-summary.json` 不随 finalize 发布，下游只靠这一个文件就能回答「留下了哪些、为什么」。

层推导口径（`embodied_learning/knowledge/funnel.py`）：

| 层 | 来源 | 说明 |
|---|---|---|
| `registry` | `candidate-registry.json` | `candidates` 为空时 `stages.candidates` 回退 `candidate_count` |
| `screened` | `screening-ids.txt` | 选文通过集合 |
| `full_text` | `extraction-summary.json` 中 `evidence_eligible` | **与 `screened` 取交集**（旧 summary 可能滞后） |
| `deep_read` | `paper-notes/<id>.json` ∪ `<id>.failed.json` | 计**尝试**数，不是队列上限；排除 `*.audit.json` |
| `evidence` | `evidence/*.jsonl` 非空 | 排除 `abstract-tier.jsonl` |
| `abstract` | `evidence/abstract-tier.jsonl` | 与 `evidence` 层**有意重叠** |

阅读契约的三条硬规则：

- **`null` 只表示产物不存在**，从不猜测。`--skip-deep-read` 自身不制造 `null`：盘上有旧产物就照常统计，`detail.skipped` 只记录本次跳过。
- **漏斗不是严格嵌套**：种子论文被强制排在深读队列最前、可以不在选文集合内，差值记在 `detail.seeds_outside_screened`；率类指标的分母因此以相邻层为准，不要假设单调包含。
- **裁剪不静默**：任一层超过 `FUNNEL_LAYER_PAPER_CAP`（5000）时截断并置 `truncated: true`，driver 同时打日志。

`detail.screen_limit` 是**旧 run 专有**字段：2026-10-20 起选文不再按数量截断（深读队列的模式预算是唯一截断点），新 run 恒为 `null`；保留键是为了读懂旧 run 的选文规模。

历史 run（funnel 引入前 settle）**不回填**：口径不稳定（只有部分 run 保留 `pipeline-summary.json` / `screening.json`），凑出来的数字比 `null` 更危险。

## kb-merge — 跨根合并

把多个来源 KB 根的成果并入一个目标根。**合并前先 `--dry-run`**——尤其是 CIFS 挂载（mtime 不可靠）。

```bash
# 先看报告
python3 scripts/wiki.py kb-merge --kb-root ~/Documents/arxiv \
  --source /home/ming/code/embodied-learning \
  --source /mount/TEST/public/wiki \
  --dry-run

# 确认后执行（会重建 wiki 快照）
python3 scripts/wiki.py kb-merge --kb-root ~/Documents/arxiv \
  --source /home/ming/code/embodied-learning \
  --source /mount/TEST/public/wiki

# 只合并 runs（pool 全文慢，可分批）
python3 scripts/wiki.py kb-merge --kb-root ~/Documents/arxiv \
  --source /mount/TEST/public/wiki --what runs --dry-run
```

| 对象 | 源 → 目标 | 「新」判据 |
|---|---|---|
| runs | `evidence/<run>/` 整目录 | `run.json` mtime |
| pool | `pool/<dir>/` | `meta.json` 的 `added_at` ISO；缺则 mtime |
| cards | `knowledge/{embodied-ai,error-governance}/*.md` | 文件 mtime |
| slugs | `wiki/site-config.json` 的 `topics` 映射 | key 不存在则写入；存在则新者胜出 |

冲突策略 `--prefer`：

- `newer`（默认）— 新者胜出
- `target` — 永不覆盖（CIFS mtime 不可靠时的保守选项）
- `source` — 永远覆盖

行为约定：

- **不同名 run 不去重**（`图像粗配准-…-20260911` 与 `图像粗配准-…-20260929` 是两次 run，都保留）
- 新拷入的 run 会自动补 catalog 行；覆盖的 run 重写 catalog 行
- `pool/index.jsonl` 在共享锁下合并
- 新卡片只报告 `unrouted_ids`，**不自动改 `knowledge/index.md`**（那是手工路由表）
- 末尾默认重建 wiki 快照；`--no-wiki` 跳过
- `--dry-run` 时目标树逐字节不变

## Python 库调用

```python
from pathlib import Path
from embodied_learning.knowledge.model import KnowledgeBase

local = KnowledgeBase.open(Path.home() / "Documents" / "arxiv")

# 盘点
stats = local.stats(include_runs=True)
print(stats["runs"]["total"], stats["pool"]["deep_read"])

# 检索
hits = local.search("外参标定", scope="events", limit=10)
for h in hits:
    print(h["id"], h["claim"][:80])

# 漏斗：逐 run 统计 / 某一层的论文
for row in local.funnel(sort="evidence_yield"):
    print(row["run"], row["stages"], row["rates"])
for row in local.funnel(layer="screened", run="literature-review-…"):
    print(row["arxiv_id"], row["title"], row["reason"])

# 合并（先 dry-run）
report = local.merge_from(
    Path("/mount/TEST/public/wiki"),
    what=frozenset({"runs"}),
    dry_run=True,
)
print(report["runs"]["copied"], report["runs"]["skipped_target_newer"])
```

模型对象也可直接遍历：

```python
for run in local.runs():
    print(run.name, run.status, len(run.events()))

for paper in local.papers():
    if paper.has_full_text and paper.has_deep_read:
        print(paper.arxiv_id, paper.title)
```
