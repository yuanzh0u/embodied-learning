---
title: Consolidate To Three Skills
status: accepted
date: 2026-09-14
tags: [adr, skills, query-planning, review-writing, literature-mining]
---

# ADR 0003: Consolidate To Three Skills

## Status

Accepted. Supersedes [ADR 0001](0001-separate-query-planning-from-literature-mining.md).

## Context

ADR 0001 把 query planning 拆成独立 Skill，当时的动因是 specialized family 快速增长导致 taxonomy 维护污染 evidence mining。实际运行后，技能层膨胀到 7 个：三个小 skill（`embodied-ai-query-planner`、`embodied-ai-influence-ranking`、`embodied-ai-problem-relevance-ranking`）主要承担 workflow 编排而非独立知识域，`embodied-ai-literature-review` 与 `embodied-ai-review-writer` 之间则出现了 orchestration 与写作职责的重复。Skill 边界过多带来的上下文加载成本和 cross-skill 路径耦合，已经超过 0001 所预期的"一层 Skill 边界"的维护成本。

## Decision

收敛为三个 skill，对应检索/阅读/写作三个阶段：

- **`embodied-ai-literature-hub`**（检索）：吸收 `embodied-ai-query-planner`（query planning 成为 skill 内的 planning stage，`build_query_plan.py` 直接落位 hub scripts，compat wrapper 移除）、`embodied-ai-influence-ranking` 和 `embodied-ai-problem-relevance-ranking`（作为 candidate triage 环节）。
- **`embodied-ai-paper-reader`**（阅读）：不变。
- **`embodied-ai-review-writer`**（写作）：吸收 `embodied-ai-literature-review` 的 orchestration 与 briefing 生成（run lifecycle、settlement gates、`build_review_packet.py`），与原有写作工作流合并。

## Consequences

- ADR 0001 中的两项 handoff 不变量**原样保留**，只是不再跨越 skill 边界：
  1. Query plan 的 channel 分离不变：`queries`（arXiv API）与 `browser_fallback_queries`、`web_calibration_queries` 保持独立；`search_arxiv.py --query-file` 只读顶层 `queries` 条目。
  2. Web/social calibration 仍然只影响 query wording 与候选发现，永远不能成为 accepted evidence。
- `scripts/serve_research_wiki.py` 的 pipeline-root 探测与 `scripts/wiki_chat.py` 的 kickoff prompt 跟随 SKILL.md 指向 `embodied-ai-review-writer`。
- `literature-review-<topic>-<date>` 目录名契约（bundle trigger）与 `evidence/` append-only 语义不变；已结算 run 中的 `"planner": "embodied-ai-query-planner"` 等历史元数据不改写。
- `docs/prd/` 中三份按旧 skill 划分的 PRD 作为历史文档保留，不再反映当前结构。
