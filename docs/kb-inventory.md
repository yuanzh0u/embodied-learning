# KB 盘点、检索与跨根合并

给定一个知识库根（kb-root），统计跑了多少 run、多少论文有全文/精读，支持子串检索，并可将多个根的成果合并到一个目标根。库可调用 + CLI + 本文档。

## 对象模型

```
<kb-root>/
  evidence/<run>/          run.json + evidence.jsonl + 三成稿 + revisions/
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
  "reading": {"runs_with_ledger": 14, "ledger_rows": 235, "accepted_rows": 152}
}
```

`--runs-detail` 时额外输出 `runs_detail` 数组（每 run 的 topic / status / mode / event_count / papers / deep_read_count）。

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
