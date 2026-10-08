# 精读契约（Agent 版）

本文是"近两年 Diffusion Transformer 在视频生成与世界模型中的发展"（scoping 综述）的精读执行规范。每个精读代理必须严格遵守。

## 根目录
RUN=/Users/eason/Documents/具身学习/work/literature-review-近两年-diffusion-transformer-在视频生成与世界模型中的发展-20260823

## 综述问题（用于 Pass 2 的 guided deep read）
近两年（2024-08 至 2026-08）Diffusion Transformer（DiT）在视频生成与世界模型方向的：能力如何演进（架构/微缩化/Video VAE/流匹配/缩放律）、向"世界模型"转型的机制、物理/时序/实体一致性等限制、评测方法与基准、部署/加速（缓存/蒸馏/稀疏化/量化）、以及 action-conditioned 世界模型与具身交叉。对每篇论文，关注其为该综述提供的证据，并保持立场（support / limit / conditional / gap）与置信度（direct / citation-supported / inference）的区分。

## 输入
- 元数据：RUN/metadata/<arxiv_id>.json（含 arxiv_id, title, published, url, authors）
- 完整全文：RUN/fulltext/<arxiv_id>.json
  - 关键字段：`text`（HTML 全文）、`sections`（含标题与定位）、`ranked_sections`、`quality`、`evidence_eligible`、`source_format`、`structure`
  - 全文较大，请用 Read 的 offset/limit 分段读取，不要一次全读；定位 locate 到 section 名。
- 论文均为 HTML 提取、非 OCR、quality high，可直接精读。

## scoping 阅读要求（必读部分 + 必须记录的 role）
每篇必须阅读并记录以下 sections（在 paper-note 的 `reading.sections_read` 中，每项 locator 指向 section）：
- `problem`（引言/问题）
- `method-or-design`（方法/设计）
- `results-or-analysis`（实验/结果/消融）
- `conclusion-or-limitations`（结论/限制）
若某部分无，记入 `sections_skipped`。对 included 论文必须至少记录 1 个 transfer_boundary。

## Paper-note.json 必须字段（schema_version 1）
```json
{
  "schema_version": 1,
  "paper": { "arxiv_id","title","published","url","authors" },   // 从 metadata 取
  "review": { "question": "...", "topic_ids": ["EA-4D","EA-EVAL","EA-MODEL"], "mode": "scoping" },
  "extraction": { "source_format","method","quality","full_text_available": true, "ocr_pages": [], "visual_validation": "not-required" },
  "reading": { "status":"evidence-ready"|"rejected"|"deep-read", "paper_type", "relevance":{"decision":"include"|"background-only"|"exclude","reason"}, "sections_read":[{locator,role,purpose}], "sections_skipped":[] },
  "research_question": "...",
  "contributions": ["..."],
  "method": {"summary":"...", "assumptions":[]},
  "study_context": {"datasets":[],"tasks":[],"embodiments":[],"sample_or_scale":"..."},
  "evaluation": {"design":"...","baselines":[],"metrics":[],"ablations":[]},
  "findings": [{"finding":"...","scope":"...","locator":"..."}],
  "limitations": { "author_status":"found"|"not-found", "author_stated":[{limitation,locator}], "reader_inferred":[{boundary,basis}] },
  "transfer_boundary": "...",
  "critical_appraisal": { "design_strengths":[],"design_risks":[],"baseline_fairness":"...","metric_validity":"...","reproducibility":"...","external_validity":"..." },
  "evidence_cards": [ ... 见下 ... ],
  "core_citations": [],
  "notes": ""
}
```

## Evidence card 规格（每卡必填）
```json
{
  "card_id": "<arxiv>_C01",
  "claim": "受限于该论文实验的精确主张",
  "stance": "support|limit|conditional|gap",
  "relation": "这条支持/限制综述的哪个命题",
  "confidence": "direct|citation-supported|inference",
  "claim_basis": "author-claim|reported-result|cited-work|reader-inference",
  "summary": "为什么引材料支持该主张",
  "locator": "Section 名 或 page/Table/Figure 精确定位",
  "source_context": "提取自全文的一小段忠实上下文（verbatim 或紧贴原文）",
  "evidence_type": "experiment|architecture|analysis|survey|position|other",
  "quantitative": false 或 { "metric","value_or_direction","comparator","task_or_sample","locator" },
  "verification": { "status": "passed", "checked_against": "full-text", "rationale": "说明该 claim 如何被精确上下文蕴含" }
}
```
规则：
- 只在高相关处建卡；每篇可在 0~多个卡之间，绝不凑数。整篇无可信证据则 status=rejected, evidence_cards=[]。
- 定量卡必须 metric/value_or_direction/comparator/task_or_sample/locator 全有。
- 每卡必须背诵 `verification.status: passed` 并在 rationale 说明人工核验依据（这是 claim-support audit 的手动复核依据）。
- 保持 Negative/limiting/gap 证据，不要只写正面的。
- 不要泛化该论文未覆盖的任务/本体/视界/评测。

## 六遍协议（顺序执行）
Pass0 相关性初筛(include/exclude) → Pass1 结构映射 → Pass2 深度阅读 → Pass3 证据卡 → Pass4 批判性评估 → Pass5 回到原文核验每卡 + 记录 rationale。

## 输出 gate（每篇必须跑，顺序如下）
```bash
# 1) 结构校验（必须通过，否则修订 note）
python3 skills/embodied-ai-paper-reader/scripts/validate_paper_note.py RUN/paper-notes/<arxiv_id>.json
# 2) claim-support 审计（必须通过/无 blocking 失败）
python3 skills/embodied-ai-paper-reader/scripts/audit_claim_support.py \
  --paper-note RUN/paper-notes/<arxiv_id>.json \
  --extraction RUN/fulltext/<arxiv_id>.json \
  --output RUN/claim-support-audits/<arxiv_id>.audit.json
```
- 若 validate 或 audit 报错/不通过：阅读报错，修订 paper-note 直到通过；反复失败则该篇标记 `unavailable`/`rejected` 并在报告说明。
- 若 audit 通过：每卡 `verification.status` 必须已被你人工确认 passed。
- **不要运行 project_evidence_events.py**（由主编统一投影以分配全局唯一事件 ID）。

## 交付（在你的最终报告中为每篇给出）
`<(arxiv_id) (title) | status=evidence-ready|rejected|unavailable | evidence_cards=N | validate=pass | audit=pass>`

## 质量红线
- locator 必须能在 fulltext 中找到真实验证位置；不得捏造 section/页码。
- source_context 必须忠实于全文原话。
- 不得用 abstract 或排名段落代替完整全文深读。
- 不得把作者观点当实测结果（用 stance/claim_basis 区分）。
- 不推断机构归属。