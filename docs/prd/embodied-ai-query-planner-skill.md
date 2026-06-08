---
title: 具身智能 Query Planner Skill PRD
status: ready-for-agent
created: 2026-06-08
tags: [prd, skill, embodied-ai, query-planning, arxiv, literature-mining]
---

# 具身智能 Query Planner Skill PRD

## Problem Statement

研究者在围绕具身智能话题检索论文时，常常需要把一个中文研究问题拆成多层英文检索 query：直接主题词、邻接主题词、命名方法族、负面讨论、作者或社区新词、Browser fallback 线索等。现有 `embodied-ai-literature-hub` 已经承担 arXiv 检索、候选论文管理、HTML正文挖掘和证据输出，但 query planning 仍混在文献汇聚流程里，且目前只有 UMI/data-usability 一个确定性查询计划。

这导致三个问题：第一，新的具身话题不能稳定生成可复现 query；第二，人工或 Agent 临场扩展 query 时容易遗漏 `EA-*` 主题卡中的邻接面；第三，社交讨论、项目页或 arXiv 页面中出现的新术语缺少清晰的低置信校准位置，容易和论文证据混在一起。

## Solution

构建一个独立 Codex Skill：`embodied-ai-query-planner`。它根据给定的具身话题生成结构化 query plan，并作为 `embodied-ai-literature-hub` 的上游能力使用。Query Planner 负责话题映射、检索层级、query 字符串、query rationale、候选来源通道和联网校准记录；Literature Hub 只负责执行检索、正文挖掘和证据判断。

新 Skill 支持七个知识库主题 `EA-DATA`、`EA-SENSOR`、`EA-HARDWARE`、`EA-XEMBODIMENT`、`EA-MODEL`、`EA-EVAL`、`EA-BIZ`，并内置十个专项族：UMI、DROID/Ego4D、teleoperation/demo-quality、VLA、Sim2Real、world-model、retargeting、tactile/force、last-centimeter、industrial-deployment。输出以 JSON 为主，Markdown 为人工审查视图。Agent 可用 arXiv、Reddit、X/Twitter 做关键词校准，但这些来源只用于发现新词、别名和 query 变体，不作为论文证据。

## User Stories

1. As a 具身智能研究者, I want to provide a Chinese or English research topic, so that I can get usable paper-search queries without manually translating and expanding every term.
2. As a researcher, I want a topic to map to one or more `EA-*` knowledge IDs, so that query generation follows the repository's domain routing layer.
3. As a researcher, I want query plans to include direct and adjacent search surfaces, so that hidden discussions in neighboring topics are not missed.
4. As a researcher, I want query plans to include `label`, `tier`, `query`, and `why`, so that I can audit why each query exists.
5. As a researcher, I want JSON output to be the primary artifact, so that downstream scripts can consume it without parsing prose.
6. As a researcher, I want a Markdown review output, so that I can inspect and tune query strategy before running expensive searches.
7. As a literature-mining agent, I want a query plan compatible with arXiv search scripts, so that I can pass it directly into the retrieval workflow.
8. As a literature-mining agent, I want arXiv API queries separated from Browser fallback queries, so that I do not run site-search syntax against the arXiv API.
9. As a literature-mining agent, I want web calibration queries separated from arXiv API queries, so that social or web discovery remains clearly marked.
10. As a researcher, I want UMI topics to expand into named variants, hardware-language queries, limitation queries, adjacent model queries, author/citation hints, and known family candidates, so that exact keyword scarcity does not create false negatives.
11. As a researcher, I want DROID/Ego4D topics to expand into robot data, human demonstration data, in-the-wild collection, dataset curation, and cross-dataset reuse queries, so that large data discussions are discoverable.
12. As a researcher, I want teleoperation and demonstration-quality topics to include operator burden, latency, action interface, trajectory quality, and imitation-learning queries, so that data usability issues are visible.
13. As a researcher, I want VLA topics to expand into robot foundation models, RT-X, Octo, OpenVLA, fine-tuning data, action tokenization, data mixture, and negative transfer queries, so that model papers expose data and embodiment assumptions.
14. As a researcher, I want Sim2Real topics to include simulation validity, real-robot validation, synthetic data, closed-loop evaluation, and sim-real correlation queries, so that evaluation limits are not hidden.
15. As a researcher, I want world-model topics to include prediction, planning, contact realism, long-horizon consistency, and offline evaluation queries, so that world-model claims can be located across model and evaluation literature.
16. As a researcher, I want retargeting topics to include cross-embodiment transfer, morphology gap, action representation, human-to-robot mapping, dexterous hand, and gripper queries, so that embodiment adaptation is covered.
17. As a researcher, I want tactile and force topics to include tactile sensing, force/torque, contact-rich manipulation, slip detection, sensor fusion, and multimodal policy queries, so that physical observability is represented.
18. As a researcher, I want last-centimeter topics to include visual-servoing, contact transition, force control, failure recovery, insertion, fixture design, and deployment queries, so that contact-closure bottlenecks are searchable.
19. As a researcher, I want industrial-deployment topics to include reliability, cycle time, yield, acceptance testing, operator takeover, maintenance, and ROI-adjacent queries, so that ToB evidence can be investigated without pretending demos equal deployment.
20. As a researcher, I want default query generation to avoid hard `cat:` filters, so that cross-disciplinary papers are not accidentally excluded.
21. As a researcher, I want suggested arXiv categories included separately, so that I can manually narrow searches when noise is too high.
22. As a researcher, I want a wide-recall default budget, so that broad topics can produce enough candidates for later strong filtering.
23. As a researcher, I want duplicate queries removed while preserving labels and rationales, so that the plan stays readable.
24. As a researcher, I want time range to be accepted as optional metadata, so that query planning can support both brainstorming and bounded literature mining.
25. As a researcher, I want calibration notes to record which web sources were used, so that I can distinguish stable taxonomy from fresh social vocabulary.
26. As a researcher, I want Reddit and X/Twitter terms marked as low-confidence calibration, so that community language does not become accepted evidence.
27. As a researcher, I want arXiv pages and project or author pages to be preferred calibration sources, so that query terms remain close to paper vocabulary.
28. As a researcher, I want query generation to degrade gracefully when web calibration fails, so that offline or restricted-network environments still produce useful plans.
29. As a Skill user, I want the Skill to explain when to use `references/topic-taxonomy.md`, so that the main instructions stay compact.
30. As a Skill user, I want the Skill to explain when to use `references/web-calibration.md`, so that live-search behavior is consistent.
31. As a future maintainer, I want the query taxonomy to be built into the Skill but allow local knowledge overrides, so that the global Skill remains usable outside this repo while respecting this repository's `knowledge/` layer when present.
32. As a future maintainer, I want query planning separated from literature mining, so that retrieval/extraction changes do not require changing topic taxonomy logic.
33. As a future maintainer, I want `embodied-ai-literature-hub` to call this new Skill instead of maintaining its own query plan table, so that there is a single source for query strategy.
34. As a future maintainer, I want an ADR for the Skill split, so that future agents understand why the responsibilities are separated.
35. As a future agent, I want `CONTEXT.md` to define query-planning terms without implementation details, so that domain language remains stable.
36. As a future agent, I want `knowledge/index.md` to point to `CONTEXT.md`, so that the new glossary entry is discoverable through the repository's loading order.
37. As a reviewer, I want query planner tests to validate generated behavior rather than implementation details, so that taxonomy refactors do not break tests unnecessarily.
38. As a reviewer, I want compatibility tests against the existing arXiv search script, so that the handoff between Skills does not silently break.
39. As a reviewer, I want sample outputs for representative topics, so that query quality can be inspected quickly.
40. As a researcher, I want the resulting query plan to be reusable in later literature runs, so that search strategy becomes traceable rather than trapped in chat history.

## Implementation Decisions

- Build a new Skill named `embodied-ai-query-planner`.
- Keep the Skill versioned in the repository and sync it to the global Codex skills directory after implementation and validation.
- Make query planning a separate upstream responsibility from literature mining.
- Migrate `embodied-ai-literature-hub` so that it uses the new query planner for search-plan generation and no longer owns topic expansion logic.
- Use the repository's `EA-*` knowledge IDs as the primary domain taxonomy.
- Include ten built-in specialized topic families in v1: UMI, DROID/Ego4D, teleoperation/demo-quality, VLA, Sim2Real, world-model, retargeting, tactile/force, last-centimeter, and industrial-deployment.
- Provide a deterministic query-plan script for stable baseline plans.
- Allow Agent-supplied calibration input from live web search, but keep the script responsible for merging, deduplicating, labeling, and emitting the final plan.
- Treat arXiv, project pages, author pages, Reddit, and X/Twitter as calibration surfaces for query wording, not as accepted literature evidence.
- Mark Reddit and X/Twitter discoveries as low-confidence social calibration.
- Keep arXiv API queries, Browser fallback queries, and web calibration queries in separate output channels.
- Preserve a top-level `queries` field compatible with the existing arXiv search script.
- Do not hard-filter by arXiv category by default; include suggested categories as metadata.
- Prefer wide recall by default, with a maximum query budget around 50 query entries per generated plan.
- Support Chinese and English topic input.
- Accept optional knowledge ID, specialized family, date range, calibration file, query budget, JSON output path, and Markdown output path.
- Build in a baseline taxonomy but allow local repository knowledge to override or enrich it when the Skill runs inside this knowledge base.
- Add `CONTEXT.md` as a glossary-only document for query-planning terms and route it from the knowledge index.
- Add a short ADR recording the separation between query planning and literature mining.
- Do not move evidence extraction, HTML mining, source entry drafting, or topic-card update suggestions into the query planner.

## Testing Decisions

- Test the highest useful seams: Skill CLI output, query-plan schema, calibration merge behavior, and compatibility with the arXiv search script.
- Query planner tests should assert observable output: topic mappings, query channels, labels, tiers, rationales, deduplication, and budget limits.
- Mapping tests should cover representative Chinese and English topics for each `EA-*` theme.
- Specialized-family tests should cover all ten v1 families and verify that each produces a non-empty, labeled query set.
- Calibration tests should verify that arXiv/project/author/social sources remain labeled and that social calibration is never promoted to evidence.
- Degradation tests should verify that a missing or failed calibration file still produces an offline query plan with notes.
- Compatibility tests should verify that the generated JSON can be consumed by the existing arXiv search script through its query-file interface.
- Markdown-output tests should verify that the review view includes the topic mapping, query tiers, and rationale without becoming the source of truth.
- Skill metadata tests should validate that the Skill frontmatter and UI metadata are present and triggerable.
- Documentation tests should inspect that `embodied-ai-literature-hub` points to the query planner instead of carrying its own topic expansion workflow.
- Tests should not assert the internal structure of taxonomy constants beyond the public query-plan behavior.
- Current repository testing prior art is script-level validation around the literature hub utilities, so v1 should follow that seam rather than introduce a larger test framework.

## Out of Scope

- Running the actual arXiv search or accepting papers as evidence.
- Mining arXiv HTML正文, PDFs, or references.
- Treating Reddit, X/Twitter, project pages, or author pages as primary evidence.
- Building a full web crawler for social platforms.
- Solving global author identity disambiguation.
- Automatically updating topic cards from query plans.
- Creating a plugin or MCP server.
- Recurring monitoring, alerts, or scheduled literature scans.
- Replacing the repository's `EA-*` topic-card system.
- Adding hard arXiv category filters as the default behavior.

## Further Notes

The main testing seams are:

- Query planner CLI output for representative topics.
- Calibration-file merge and source labeling.
- JSON compatibility with the arXiv search script.
- Literature hub documentation handoff to the query planner.

This PRD is ready to publish as a `ready-for-agent` issue when the project issue tracker and label vocabulary are configured. This repository currently has no visible remote issue tracker configuration, so the PRD is kept as a local project document.
