---
title: Separate Query Planning From Literature Mining
status: accepted
date: 2026-06-08
tags: [adr, embodied-ai, query-planning, literature-mining]
---

# ADR 0001: Separate Query Planning From Literature Mining

## Status

Accepted.

## Context

`embodied-ai-literature-hub` 负责 arXiv 检索、候选论文管理、HTML 正文挖掘、证据记录和 brief 输出。随着具身智能问题从 UMI/data usability 扩展到 VLA、Sim2Real、retargeting、tactile/force、industrial deployment 等 specialized family，query planning 本身已经变成独立问题。

如果 query taxonomy、Browser fallback、web calibration 和 social calibration 继续混在 literature mining workflow 里，后续 Agent 很难判断哪些内容是检索策略、哪些内容是已验证论文证据，也难以复用同一套 query plan。

## Decision

将 query planning 拆成独立 Skill：`embodied-ai-query-planner`，作为 `embodied-ai-literature-hub` 的 upstream capability。

Query Planner 负责把中英文 research topic 映射到 `EA-*` knowledge IDs、specialized family、query tier 和不同 query channel，并明确标记 arXiv API query、browser fallback query、web calibration 与 low-confidence social calibration。Literature Hub 只消费 query plan，继续负责执行检索、正文挖掘、证据判断和知识库入库建议。

## Consequences

- Query strategy 有单独的 source of truth，便于审查、复用和测试。
- `embodied-ai-literature-hub` 的职责更窄，减少 taxonomy 变化对 evidence mining 的影响。
- Query plan 与 literature mining 之间需要稳定 handoff contract，尤其要保持 arXiv API query 和 Browser fallback query 分离。
- Web/social calibration 只能影响 query wording 或候选发现，不能直接成为 accepted evidence。
- 维护成本增加一层 Skill 边界，但换来更清晰的 traceability 和更低的后续耦合。
