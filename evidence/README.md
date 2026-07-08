# Evidence 层说明

`evidence/` 是版本化的证据真相层(见 [ADR-0002](../docs/adr/0002-retire-raw-sources-promote-evidence-layer.md))。规则与管线的 candidate ≠ evidence 纪律同构:

- **candidate 与中间产物住 `work/`**(gitignored scratch):arXiv 候选列表、HTML 抽取 JSON、动态扩展文件、smoke test 产物。
- **accepted 资产住 `evidence/`**(版本控制):accepted evidence JSONL、正式综述成品、source-entry draft、query plan、run manifest。

## Run 文件夹布局

每次文献 run 一个文件夹,命名与 `work/` 镜像:`literature-review-<topic>-<date>/`。

| 文件 | 必备 | 说明 |
|---|---|---|
| `run.json` | 是 | run manifest,字段见下 |
| `evidence.jsonl` | 是 | accepted 证据事件(经 `write_lit_outputs.py --validate-only` 校验) |
| `scientific-memo_keyan.md` 等三风格成品 | 正式 run | `evidence-appendix.md` 属于 bundle 的第 4 个文件 |
| `source-entry-draft.md` | 有则收 | 待结算入 `knowledge/sources.md` 的来源草稿 |
| `query-plan.json` / `query-plan.md` | 有则收 | 本次 run 的检索策略(可复现性) |
| `review-packet.md` / `evidence-brief.md` | 可选 | 审计视图 |

## run.json 字段约定

```json
{
  "run": "literature-review-<topic>-<date>",
  "topic": "话题原文",
  "topic_id_prefix": "EA-TWM",
  "knowledge_ids": ["EA-EVAL"],
  "time_range": "2025-12-23..2026-06-23",
  "rounds": 1,
  "event_count": 18,
  "source_runs": ["literature-review-<prior-topic>-<date>"],
  "files": {
    "evidence": "evidence.jsonl",
    "reused_evidence": ["reused/<prior-run>-evidence.jsonl"],
    "query_plan": "query-plan.json",
    "outputs": ["scientific-memo_keyan.md", "zhihu-explainer_zhihu.md", "xiaohongshu-post_xiaohongshu.md"],
    "appendix": "evidence-appendix.md",
    "source_entry_draft": "source-entry-draft.md"
  },
  "notes": "可选:检索限制、API 故障、覆盖缺口"
}
```

跨 run 证据规则:综述可以组合历史 run 的证据(这是证据层积累的意义),但必须满足:

- `source_runs` 列出全部被复用的历史 run;本 run 只新挖证据时省略该字段。
- `event_count` = 文章**实际可引用**的去重后事件总数(新挖 + 复用),不是只数新挖的。
- 复用的 evidence.jsonl 一并拷入 run 文件夹(如 `reused/` 子目录)或在 `files.reused_evidence` 中登记相对路径,保证 run 文件夹自含可审计。
- 结算前 `python3 scripts/audit_citations.py --article <各成稿> --appendix evidence-appendix.md --evidence-jsonl <各证据文件> --run-json run.json` 必须通过(无死锚、无越界引用、manifest 一致)。

## Agent 加载方式

`evidence/` 中的 JSONL 不适合整读。按预算:

1. 先读本 README 与目标 run 的 `run.json`。
2. 中预算:读 run 的 brief 或 review-packet。
3. 高预算:按 event_id 选择性读取 `evidence.jsonl` 行,或读综述成品。

## 事件 ID

事件 ID 全局唯一,分配前用 `python3 scripts/next_event_id.py --prefix <topic_id_prefix>-<year>` 查询下一可用序号,避免跨 run 碰撞。
