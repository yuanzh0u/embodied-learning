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
| `candidate-registry.json` | workflow v2 必备 | 多轮检索去重后的候选库与筛选状态 |
| `coverage-report.json` | workflow v2 必备 | 规模、维度覆盖、全文、正式证据与饱和度闸门 |
| `review-packet.md` / `evidence-brief.md` | 可选 | 审计视图 |
| `reading-ledger.jsonl` / `reading-summary.json` | paper-reader run 必备 | 全文恢复、map read、deep read、审计和接纳状态 |
| `paper-note-index.json` / `paper-notes/` | paper-reader run 必备 | 单篇论文的结构化精读记录与原文上下文 |
| `claim-support-audit-index.json` / `claim-support-audits/` | paper-reader run 必备 | 主张是否被完整全文支持的逐篇审计 |
| `trace-map.json` | 正式三稿 bundle 必备 | 读者文章中的论文引用到 evidence event 的映射 |

## run.json 字段约定

```json
{
  "workflow_version": 2,
  "run": "literature-review-<topic>-<date>",
  "topic": "话题原文",
  "status": "settled",
  "review_mode": "scoping",
  "topic_id_prefix": "EA-TWM",
  "knowledge_ids": ["EA-EVAL"],
  "time_range": "2025-12-23..2026-06-23",
  "rounds": 1,
  "event_count": 18,
  "style": "scientific-memo",
  "scope_note": "用户明确只要求科研备忘录(缩减交付时必填;全量三风格 bundle 时省略 style/scope_note 两字段)",
  "source_runs": ["literature-review-<prior-topic>-<date>"],
  "files": {
    "evidence": "evidence.jsonl",
    "reused_evidence": ["reused/<prior-run>-evidence.jsonl"],
    "query_plan": "query-plan.json",
    "candidate_registry": "candidate-registry.json",
    "coverage_report": "coverage-report.json",
    "outputs": ["scientific-memo_keyan.md", "zhihu-explainer_zhihu.md", "xiaohongshu-post_xiaohongshu.md"],
    "appendix": "evidence-appendix.md",
    "source_entry_draft": "source-entry-draft.md"
  },
  "notes": "可选:检索限制、API 故障、覆盖缺口"
}
```

跨 run 证据规则:综述可以组合历史 run 的证据(这是证据层积累的意义),但必须满足:

- run 用 `python3 scripts/init_run.py` 创建,出生即带 `status: in-progress` 的 run.json;结算时翻为 `settled`。`in-progress` 的 run 是未完成品,不得当作交付物展示,也不得迁入 `evidence/`。

- `source_runs` 列出全部被复用的历史 run;本 run 只新挖证据时省略该字段。
- 新版本必须创建新的 append-only run 目录；旧版本继续保留。知识卡和 [文献综述成果目录](../knowledge/literature-review-catalog.md) 负责声明当前有效版本。
- `event_count` = 文章**实际可引用**的去重后事件总数(新挖 + 复用),不是只数新挖的。
- 复用的 evidence.jsonl 一并拷入 run 文件夹(如 `reused/` 子目录)或在 `files.reused_evidence` 中登记相对路径,保证 run 文件夹自含可审计。
- 结算前两道闸门都必须通过:
  - `python3 scripts/check_run_bundle.py <run-dir>`:bundle 完整性(默认三风格 + appendix,或已声明 `style`+`scope_note` 的缩减交付)、证据自含、run.json 标准字段(`selected_event_count`、`files.memo` 等自创字段会被拒)。
  - `python3 scripts/audit_citations.py --article <各成稿> --appendix evidence-appendix.md --evidence-jsonl <各证据文件> --run-json run.json`:无死锚、无越界引用、manifest 一致。

## Agent 加载方式

`evidence/` 中的 JSONL 不适合整读。按预算:

1. 先读本 README 与目标 run 的 `run.json`。
2. 中预算:读 run 的 brief 或 review-packet。
3. 高预算:按 event_id 选择性读取 `evidence.jsonl` 行,或读综述成品。
4. 需要核验论文主张时：从 `paper-note-index.json` 定位单篇 note，再读取对应 claim-support audit；不要默认加载全部 15 篇笔记。

## 事件 ID

事件 ID 在当前有效 run 集合中必须全局唯一。paper-reader 批量迁移应为每个 run 分配独立 `event_id_prefix` 并写入 `run.json`；分配前可用 `python3 scripts/next_event_id.py --prefix <topic_id_prefix>-<year>` 查询下一可用序号，避免跨 run 碰撞。
