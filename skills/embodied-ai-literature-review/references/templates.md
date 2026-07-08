# Review Templates

Use these templates when drafting a Chinese embodied-AI literature review or related-work section. Unless the user specifies one style, produce the final artifact bundle in the review project folder under `work/`:

- `scientific-memo_keyan.md`
- `zhihu-explainer_zhihu.md`
- `xiaohongshu-post_xiaohongshu.md`
- `evidence-appendix.md`（每个 event 一节,正文中的 event ID 链接跳到这里）

Link rules for all formal styles (see review-contract.md "Citation and link contract"):

- In-text event IDs are links: `[EA-…-0001](evidence-appendix.md#ea--0001)`, not bare `EA-…-0001`.
- Paper mentions are links: `[2606.13877](https://arxiv.org/abs/2606.13877)`.
- Every formal artifact ends with a `## References` section of deduplicated linked papers.

## Scientific memo skeleton

```md
# <主题>研究备忘录

## 研究边界

本文聚焦 <topic>，主要覆盖 <EA-ID 列表>。证据来自 <evidence files/source IDs>；未完成正文核验的候选论文只用于说明检索覆盖，不作为结论依据。

## Evidence Core

- Evidence sufficiency: formal-ready/preliminary
- Paper-level sources: <n> / 5
- Stance labels: <support/conditional/limit/gap>

## Claim Map

| Claim | Trace | Stance | Confidence | Implication |
|---|---|---|---|---|
| <claim in agent words> | <event-id/source-id> | support/limit/conditional/gap | direct/citation-supported/inference | <why it matters> |

## 问题结构

从现有证据看，<topic> 不是单点技术问题，而是由 <机制 A>、<机制 B>、<评测/落地约束> 共同决定。

## 主要共识

<共识 1>（evidence-event: <event-id>; confidence: <label>）。

## 条件与分歧

<限制/条件>（evidence-event: <event-id>; stance: limit/conditional）。

## 未解决问题

<gap>（evidence-event: <event-id>; stance: gap）或 <inference: reason>。

## 对后续研究的启发

<project-facing synthesis>（inference: connects <event-id> and <source-id>）。
```

## Expert explainer pattern (default)

```md
# <主题>：专家解释帖

## TL;DR

<direct answer in 2-4 sentences, with caveat>

## 检索范围

- Time range: <explicit range or resolved recent-six-month default>
- Paper-level sources: <n> / 5
- Output type: expert-explainer

## 常见误区或争议

<what people usually get wrong>

## 证据与限制

<mechanism-oriented synthesis with event/source IDs>

## 延伸阅读与可信度

<source list and confidence note>
```

## KOL thread pattern

```md
# <主题>：洞察短串

## Hook

<sharp but evidence-bounded hook>

## 证据约束洞察

1. <claim>（[<event-id>](evidence-appendix.md#<anchor>); stance: <label>）
2. <claim>（[<event-id>](evidence-appendix.md#<anchor>); stance: <label>）
3. <claim>（[<event-id>](evidence-appendix.md#<anchor>); stance: <label>）

## 边界提醒

<visible caveat, especially for conditional/limit/gap>

## 依据来源

<compact source note>
```

## Gap language

Use careful language:

- "本轮证据尚未覆盖..." when the run did not inspect enough sources.
- "已有论文明确指出..." only when an evidence event has `stance: gap`.
- "可以推断..." only with `inference` and a short reason.

## Topic-card update suggestion

```md
## Topic Card Update Suggestions

- Add to `<EA-ID>`:
  - <one compact working-memory claim>（source: <event-id/source-id>; confidence: <label>）
- Do not add:
  - single-paper summaries
  - candidate-only findings
  - claims without locator evidence
```
