---
title: 具身智能 arXiv 文献汇聚 Skill PRD
status: ready-for-agent
created: 2026-06-06
tags: [prd, skill, embodied-ai, arxiv, literature-mining]
---

# 具身智能 arXiv 文献汇聚 Skill PRD

## Problem Statement

研究者需要围绕具身智能主题持续汇聚 arXiv 文献，但“相关论文”常常不只出现在显性主题里。例如研究数据质量时，仿真数据、VLA 微调、评测失败、跨本体迁移论文里也会出现更真实的正反讨论。现有知识库有主题卡、source 登记和术语表，但缺少一个可复用 Skill，把话题扩展检索、HTML正文讨论挖掘、引用链追踪、作者观点事件和知识库入库组织成稳定流程。

## Solution

构建一个全局 Codex Skill，用于按照给定话题和时间范围从 arXiv 检索潜在相关论文，采用“宽召回 + 强过滤”发现候选论文，再从论文正文中抽取与话题相关的论点、论据、立场、作者和引用来源。检索项规划由上游 `$embodied-ai-query-planner` 负责；本 Skill 消费 planner 产出的 arXiv API queries、Browser fallback queries 和 web calibration queries，并专注于检索执行、HTML正文挖掘与证据判断。Skill 输出双轨产物：一份按论点地图组织的研究简报，以及可长期积累的知识库证据层记录。

## User Stories

1. As a 具身智能研究者, I want to provide a topic and time range, so that literature mining is bounded and reproducible.
2. As a researcher, I want data topics to expand into simulation, VLA tuning, evaluation, and transfer papers, so that hidden data discussions are not missed.
3. As a researcher, I want the Skill to explain why each expanded query exists, so that search strategy is auditable.
4. As a researcher, I want arXiv metadata searched through the official API first and Browser/web discovery used as fallback, so that retrieval is stable when the API is rate-limited.
5. As a researcher, I want candidate papers filtered by actual topic discussion, so that irrelevant papers do not pollute the knowledge base.
6. As a researcher, I want the Skill to avoid stopping at a tiny exact-match set, so that specialized topics like UMI still produce enough candidates for literature mining.
7. As a researcher, I want HTML正文挖掘 as the default full-text path, so that negative or conditional discussions can be captured with lower latency and fewer download failures.
8. As a researcher, I want both positive and negative discussions, so that the brief reflects real trade-offs.
9. As a researcher, I want claims separated from evidence, so that I can inspect what was argued and why.
10. As a researcher, I want each claim linked to paper, page/section, and source ID, so that evidence is traceable.
11. As a researcher, I want cited evidence papers queued as candidates, so that argument chains can be followed.
12. As a researcher, I want citation chasing bounded to core evidence citations, so that the workflow does not explode.
13. As a researcher, I want stance labels for support, limit, conditional, and gap, so that nuanced positions survive summarization.
14. As a researcher, I want confidence labels for direct, citation-supported, and inference, so that claim certainty is visible.
15. As a researcher, I want author identities conservatively normalized, so that same-name authors are not accidentally merged.
16. As a researcher, I want author-level first-level institutions, so that later work can track viewpoint changes across both people and organizations.
17. As a researcher, I want author stance events, so that later work can track viewpoint changes across papers.
18. As a future agent, I want topic cards to stay compact, so that working memory remains efficient.
19. As a future agent, I want detailed evidence stored separately, so that topic cards do not become raw literature dumps.
20. As a reviewer, I want short evidence excerpts plus paraphrases, so that copyright and context efficiency are respected.
21. As a reviewer, I want HTML caches kept outside the repo, so that the repo stores evidence rather than full papers.
22. As a knowledge-base maintainer, I want source entries generated consistently, so that new papers fit existing source rules.
23. As a knowledge-base maintainer, I want JSONL evidence plus Markdown summaries, so that both scripts and humans can use the output.
24. As a researcher, I want a 论点地图 brief, so that I see consensus, disagreement, and unresolved gaps quickly.
25. As a researcher, I want candidate papers that fail filtering listed separately, so that search coverage remains visible.
26. As a Skill user, I want the Skill to ask for a missing time range, so that default windows do not bias conclusions.
27. As an implementer, I want deterministic scripts for search and extraction, so that the Skill does not repeatedly improvise tooling.

## Implementation Decisions

- The feature is a global Codex Skill, not a repo-local Skill, MCP server, or plugin in v1.
- Literature aggregation is split across two Skills: `$embodied-ai-query-planner` owns topic-to-query planning, while `$embodied-ai-literature-hub` owns retrieval execution, candidate filtering, HTML正文 mining, and evidence output.
- OpenAI official materials do not provide an arXiv-specific Skill/tool; the design follows the documented split: Skill for workflow, scripts for deterministic retrieval/extraction, MCP/plugin only for future distribution or external-tool integration.
- The arXiv interface uses the official arXiv API for first-pass search and metadata retrieval, with API etiquette including one request at a time and request spacing.
- When the API returns 429/timeouts/SSL errors or an implausibly small candidate pool, Browser/web discovery becomes the candidate fallback. Browser results are not accepted evidence until arXiv HTML正文 is verified.
- The Skill requires an explicit topic and time range. If the time range is absent, it asks before searching.
- Topic expansion uses the upstream query planner's static embodied-AI taxonomy, dynamic query suggestions, and family-aware Browser fallback queries with written rationale.
- Specialized topic families such as UMI use tiered candidate discovery: exact lineage, named variants, citing/derived work, author follow-ups, method-adjacent data papers, and negative/usability papers.
- For narrow topics, a small accepted-evidence set is allowed, but a small candidate set is a search failure unless blocked by API/network limits and clearly reported.
- Candidate promotion requires at least one topic-relevant discussion record with evidence locator.
- The evidence model records topic ID, paper ID, author keys, author-level first-level institutions, claim, stance, evidence, locator, confidence, and core cited-paper candidates.
- Author tracking is event-based rather than author-summary-based.
- Institution tracking is conservative and first-level only: subunits such as schools, departments, labs, teams, and centers are omitted; unreliable author-to-institution mappings stay empty instead of being inferred from paper-level metadata.
- HTML full text is the only default正文 source. If HTML full text is unavailable, keep the paper as a metadata candidate and do not perform正文挖掘 for that paper in the default workflow.
- HTML/PDF and extracted full text are temporary/cache artifacts; the knowledge base stores links, locators, short excerpts, and paraphrased evidence.
- Topic cards receive only high-signal synthesis; detailed evidence lives in a dedicated evidence layer.
- Research briefs are organized by 论点地图, not by 逐篇论文摘要.

## Testing Decisions

- Test at the highest seams: Skill workflow outputs, arXiv API search results, Browser fallback candidate parsing, HTML extraction output, evidence schema validation, and generated brief/source drafts.
- Search-script tests should cover normal results, zero results, malformed XML, date filtering, sorting, and rate-limit behavior.
- HTML extraction tests should verify section locators, missing HTML handling, reference-section detection, and graceful metadata-only behavior for papers without HTML.
- Evidence tests should validate required fields, stance labels, confidence labels, author-key format, first-level institution folding, old evidence without institutions, and duplicate paper handling.
- Knowledge-output tests should verify that source entries, candidate lists, topic-card update blocks, and brief sections follow existing repository conventions.
- Tests should assert external behavior and generated artifacts, not internal implementation details.
- Current repo has knowledge indices and topic-card templates but no existing automated test suite, so v1 introduces focused script-level validation fixtures.

## Out of Scope

- Building a full arXiv MCP server.
- Packaging as a personal or shared plugin.
- Recurring monitoring automation.
- Crawling all references from every paper.
- Storing full PDFs or full extracted paper text in the repo.
- Solving global author identity disambiguation beyond conservative local matching.
- Searching non-arXiv sources in v1.

## Further Notes

This PRD is ready to publish as a `ready-for-agent` issue when the project issue tracker and label vocabulary are configured. This repository does not currently expose an issue tracker configuration, so the PRD is kept as a local project document.
