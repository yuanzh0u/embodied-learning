---
title: 具身智能文献综述 Skill PRD
status: ready-for-agent
created: 2026-06-11
tags: [prd, skill, embodied-ai, literature-review, synthesis, style-adapter]
---

# 具身智能文献综述 Skill PRD

## Problem Statement

现有 `$embodied-ai-query-planner` 已经能把具身智能话题拆成可审查的 query plan，`$embodied-ai-literature-hub` 已经能执行 arXiv 检索、候选管理、HTML正文挖掘和 evidence JSONL/brief 输出。但研究者真正写综述时，还缺少一个稳定桥梁：把 claim map、stance events、topic cards 和 source entries 组织成可审计、可阅读、可转换风格的综述。

这个断层会带来三类问题。第一，证据层和综述层混在一起时，Agent 容易重复造轮子，把 query planning、文献挖掘和写作都塞进一个流程。第二，同一证据核心需要转成科学研究备忘录、知乎/Reddit 科普长帖、小红书/微博/Twitter 洞察短帖时，人工改写容易丢失 stance、confidence 和 caveat。第三，当上游 Planner/Hub 不可用时，Agent 仍需要轻量联网收集材料，但不能把网页摘要或社交讨论伪装成正文级论文证据。

## Solution

构建一个 repo-first Codex Skill：`embodied-ai-literature-review`。它作为“证据到综述”的编排与写作层，优先复用 `$embodied-ai-query-planner` 和 `$embodied-ai-literature-hub` 的结果；在上游不可用时，只做轻量联网证据包，生成可审计的 `review packet`，不复制完整文献挖掘管线。

Skill 的核心中间产物是统一的 `evidence core` 和 `review packet`。`evidence core` 保存被接受的论文级来源、claim map、stance distribution、confidence、event/source ID 和 inference 标记；`review packet` 在 evidence core 之上加入 source tiers、coverage gaps、style menu previews 和推荐输出风格。默认最终交付物是三份排版好的、阅读性强的 Markdown 文件：科研文献风格 `scientific-memo_keyan.md`、知乎科普风格 `zhihu-explainer_zhihu.md`、小红书网文风格 `xiaohongshu-post_xiaohongshu.md`，并统一存放在 `work/literature-review-<topic>-<date>/` 综述项目子文件夹中。其他最终写作由 `style adapter` 完成：同一 evidence core 可转换为科学研究备忘录、知乎/Reddit 专家解释帖、小红书/微博/Twitter 洞察卡片/串，但不同风格不得改变事实强度或升级 stance/confidence。

默认主入口是：用户给出具身话题和可选时间范围，Review Skill 自动编排 `planner -> hub -> review packet -> three-style Markdown bundle`。如果用户未指定时间范围，默认检索窗口为近半年。当用户显式请求审计、菜单或 `survey` 风格时，输出 review packet 与 style menu；当用户显式指定单一 `style` 时，只输出该风格 Markdown。当 Planner/Hub 不存在或不可用时，Review Skill 通过 Browser/web search 收集论文入口优先材料，生成 preliminary review packet；如果论文级来源不足 5 篇，则不输出正式综述，只输出材料不足说明、缺口清单和下一步检索建议。

## User Stories

1. As a 具身智能研究者, I want to provide a topic and optional time range, so that the Review Skill can produce a bounded and reproducible review workflow while defaulting to recent literature when I omit dates.
2. As a researcher, I want the Review Skill to reuse `$embodied-ai-query-planner`, so that query strategy is not reinvented inside the review layer.
3. As a researcher, I want the Review Skill to reuse `$embodied-ai-literature-hub`, so that accepted evidence comes from the existing mining and promotion rules.
4. As a researcher, I want the Review Skill to work when Planner/Hub are unavailable, so that I can still get a preliminary review packet from lightweight web collection.
5. As a researcher, I want fallback collection to prioritize paper-level sources, so that preliminary synthesis remains research-grounded.
6. As a reviewer, I want social/web content marked as calibration or context only, so that Reddit/X/知乎/微博 discussion does not become accepted paper evidence.
7. As a researcher, I want a shared evidence core before style conversion, so that multiple output styles stay factually consistent.
8. As a researcher, I want the default output to be three polished, readable Markdown articles stored in a `work/` project folder, so that I can compare scientific, Zhihu, and Xiaohongshu versions without rerunning synthesis.
9. As a researcher, I want the default bundle to include scientific memo, Zhihu expert explainer, and Xiaohongshu/KOL post variants, so that one evidence core can support research writing and public-facing communication together.
10. As a researcher, I want a review packet that includes source tiers, stance distribution, claim map, style previews, and coverage gaps when I request audit mode, so that I can inspect the material before choosing or transforming an output.
11. As a researcher, I want scientific review output to use readable references plus event/source IDs, so that both humans and future agents can audit claims.
12. As a researcher, I want 知乎/Reddit output to explain mechanisms, misconceptions, evidence, limits, and further reading, so that it reads like an expert explainer rather than a paper list.
13. As a researcher, I want 小红书/微博/Twitter output to have a strong hook and compact insight structure, so that research can be translated into short-form content without factual overreach.
14. As a reviewer, I want KOL-style writing to preserve caveats, so that `conditional`, `limit`, and `gap` claims are not rewritten as consensus.
15. As a knowledge-base maintainer, I want topic-card updates to be suggestions by default, so that polished prose does not automatically pollute compact working memory.
16. As a knowledge-base maintainer, I want source gaps reported separately, so that missing raw sources or weak provenance can be fixed intentionally.
17. As a researcher, I want the Skill to refuse formal review output when evidence is insufficient, so that a small candidate set is not overstated as a literature review.
18. As a researcher, I want preliminary output when evidence is insufficient, so that I still get useful next-step search guidance.
19. As a Skill maintainer, I want the Review Skill to stay repo-first in v1, so that it can exploit this repository's `EA-*` topic cards and existing skills before generalizing globally.
20. As a future agent, I want the PRD to define `review packet`, `evidence core`, `style adapter`, and `style menu`, so that implementation can update `CONTEXT.md` later without mixing glossary and implementation detail.

## Implementation Decisions

- Build the v1 feature as a repository Skill named `embodied-ai-literature-review`.
- Treat Review Skill as an orchestrator and synthesis layer, not a replacement for `$embodied-ai-query-planner` or `$embodied-ai-literature-hub`.
- Main flow when upstream Skills are available:
  - Load `knowledge/index.md`, `knowledge/embodied-ai/index.md`, and relevant topic cards.
  - Use `$embodied-ai-query-planner` for topic mapping, specialized family mapping, query tiers, and Browser fallback query planning.
  - Use `$embodied-ai-literature-hub` for retrieval execution, candidate filtering, HTML正文 mining, evidence JSONL, source-entry drafts, and topic-card update suggestions.
  - Build a review packet from Hub outputs, topic cards, and source entries.
  - Produce three readable Markdown files by default: `scientific-memo_keyan.md`, `zhihu-explainer_zhihu.md`, and `xiaohongshu-post_xiaohongshu.md`.
  - Store generated review artifacts under `work/literature-review-<topic>-<date>/` unless the user explicitly asks for inline output or a custom path.
  - Present a style menu and review packet when the user specifies `survey` or asks for audit/selection.
- Fallback flow when upstream Skills are unavailable:
  - Require a topic for any new paper discovery.
  - Use the most recent six months as the default discovery window when `time_range` is absent.
  - Use Browser/web search to collect paper-entry-first materials from arXiv, OpenReview, conference pages, Semantic Scholar, Papers with Code, official project pages, GitHub repositories, and author/lab pages.
  - Treat official project pages as source context for the corresponding paper or system, not as a substitute for independent paper evidence.
  - Treat Reddit, X/Twitter, 知乎, 微博, 小红书 and other community content as low-confidence calibration, pain-point examples, or topic-selection context only.
  - Emit a preliminary review packet rather than Hub-style evidence JSONL.
- Formal output requires at least 5 paper-level sources. If fewer than 5 are available, output a preliminary packet, coverage gaps, and next-step search recommendations.
- Source tiers:
  - `paper-level`: arXiv, OpenReview, conference proceedings/pages, author-hosted PDFs, Semantic Scholar paper records when they identify a paper.
  - `official-context`: official project pages, GitHub repositories, lab pages, dataset/model cards.
  - `web-context`: technical blogs, company posts, media articles, newsletters.
  - `social-calibration`: Reddit, X/Twitter, 知乎, 微博, 小红书 and similar public discussion surfaces.
- Do not promote `web-context` or `social-calibration` into accepted evidence for scientific claims.
- Preserve stance labels from the evidence layer: `support`, `limit`, `conditional`, `gap`.
- Preserve confidence labels from the evidence layer: `direct`, `citation-supported`, `inference`.
- Use a shared evidence core for all style adapters; style adapters change ordering, framing, vocabulary, length, and source presentation, not claim meaning.
- Default language is Chinese. Reddit/Twitter are treated as structure/style references unless the user explicitly asks for English.
- Default length preset is medium:
  - 科学研究备忘录：约 2000-4000 中文字。
  - 知乎/Reddit 专家解释帖：约 1500-3000 中文字。
  - 小红书/微博/Twitter 洞察卡片/串：约 300-800 中文字或 5-8 条。
- Default knowledge-base behavior is non-mutating: produce topic-card update suggestions and source gaps, but do not edit `knowledge/sources.md` or topic cards unless the user explicitly asks.
- v1 PRD does not require a new ADR. The existing ADR covering query-planning/literature-mining separation remains the architectural backdrop.

## Public Interface

### Required Inputs

- `topic`: Chinese or English embodied-AI review topic.

### Optional Inputs

- `time_range`: review/search range; default is the most recent six months.
- `knowledge_id`: one or more `EA-*` IDs such as `EA-DATA`, `EA-MODEL`, or `EA-EVAL`.
- `style`: `all`, `scientific-memo`, `expert-explainer`, `kol-thread`, or `survey`; default is `all`.
- `work_dir`: output root; default is repository `work/`.
- `output`: explicit Markdown output path or inline/stdout mode.
- `platform`: optional platform hint such as `zhihu`, `reddit`, `xiaohongshu`, `weibo`, or `twitter`.
- `evidence_jsonl`: Hub evidence events.
- `brief`: Hub Markdown brief.
- `source_file`: source index or generated source-entry draft.
- `draft`: user-provided text to audit or transform.

### Review Packet Contract

The review packet is the intermediate artifact. It is visible when material is insufficient, when fallback collection is preliminary, or when the user asks for `survey`/audit output. It should include:

- Scope: topic, time range, knowledge IDs, source of upstream/fallback collection.
- Evidence sufficiency: formal or preliminary status, paper-level source count, coverage limits.
- Evidence core: accepted claims, stance distribution, confidence distribution, event/source IDs, inference labels.
- Source tiers: paper-level, official-context, web-context, social-calibration.
- Claim map: claim, stance, confidence, trace, implication.
- Coverage gaps: missing source types, under-covered subtopics, weak or conflicting evidence.
- Style menu previews: title/opening preview for each supported style.
- Default final bundle: `scientific-memo_keyan.md`, `zhihu-explainer_zhihu.md`, and `xiaohongshu-post_xiaohongshu.md`; single-style output is available only when requested.
- Output location: generated Markdown artifacts live in the review project folder under `work/` by default.
- Topic-card update suggestions and source gaps, separated from final prose.

### Style Menu Contract

When the user requests `survey`, audit mode, or style selection, show a compact menu with:

- Evidence sufficiency status and paper-level source count.
- 3-5 core claims from the evidence core.
- One preview title/opening for each style:
  - 科学研究备忘录。
  - 知乎/Reddit 专家解释帖。
  - 小红书/微博/Twitter 洞察卡片/串。
- A default final style and transformation guidance:
  - Default to the three-style bundle for the initial readable Markdown artifacts.
  - Use scientific memo when evidence is complex, contested, or methodologically dense.
  - Use expert explainer for concepts, mechanisms, misconceptions, caveats, and further reading.
  - Use KOL thread only when the evidence core supports a clear, bounded, communicable insight.

## Style Contracts

### Scientific Memo

Required moves:

- State research boundary, time range, source coverage, and evidence sufficiency.
- Present a claim map before or near the main synthesis.
- Organize by mechanism, assumption, disagreement, and gap rather than paper-by-paper summary.
- Preserve limitations, negative evidence, and conditional claims.
- Use readable citations in prose plus event/source IDs in claim map or notes.
- End with research implications, open questions, and topic-card update suggestions.

Prohibited moves:

- Do not cite candidate-only papers as evidence.
- Do not hide inference behind source-backed language.
- Do not turn "not found in this run" into "the literature has no evidence."

### Zhihu/Reddit Expert Explainer

Required moves:

- Start with a TL;DR or direct answer.
- Explain the core misconception or debate.
- Break down mechanisms and evidence in readable sections.
- Include opposing evidence, caveats, or "when this is not true."
- End with a source/further-reading section and a confidence note.

Prohibited moves:

- Do not flatten unresolved gaps into confident advice.
- Do not use platform tone to remove caveats.
- Do not over-index on social discussion as proof.

### Xiaohongshu/Weibo/Twitter KOL Thread

Required moves:

- Start with a strong hook grounded in the evidence core.
- Provide 3-5 compact insights or a 5-8 item thread.
- Include at least one反常识点 only if supported by evidence.
- Include one concise caveat/boundary reminder.
- End with a compact source section or "依据来自..." note.

Allowed:

- Stronger framing, sharper hooks, analogy, and memorable phrasing.

Prohibited:

- Do not upgrade `conditional` into consensus.
- Do not turn `limit` or `gap` into hype.
- Do not imply investment, product, or deployment certainty from research evidence alone.

## Testing Decisions

- Workflow tests should verify that Review Skill calls/uses Planner and Hub outputs when available instead of rebuilding query planning or evidence mining internally.
- Default tests should verify that missing `time_range` uses the most recent six months and that missing `output` writes to a review project folder under `work/`.
- Fallback tests should verify that no-Hub collection emits a preliminary review packet and source tiers, not evidence JSONL.
- Sufficiency tests should verify that fewer than 5 paper-level sources prevents formal output and produces coverage gaps plus next-step recommendations.
- Style conversion tests should verify that all style adapters consume the same evidence core and preserve stance/confidence.
- Scientific memo tests should verify claim map presence, double citation layer, caveat preservation, and topic-card update suggestions.
- Expert explainer tests should verify TL;DR, misconception framing, evidence/limit sections, and source/further-reading section.
- KOL thread tests should verify strong hook, 3-5 evidence-bounded insights or 5-8 thread items, caveat, and compact source note.
- Source-tier tests should verify that social calibration and web context cannot support accepted scientific claims.
- Regression tests should include topics with mixed `support`, `conditional`, `limit`, and `gap` events to ensure style adapters do not flatten nuance.
- Tests should focus on generated artifact contracts and traceability, not exact prose.

## Acceptance Scenarios

- Planner/Hub available: Given topic `VLA 的数据金字塔` and no explicit time range, the Review Skill uses the most recent six months, consumes Planner and Hub outputs, then writes `scientific-memo_keyan.md`, `zhihu-explainer_zhihu.md`, and `xiaohongshu-post_xiaohongshu.md` under `work/literature-review-<topic>-<date>/` without inventing a new query taxonomy; `survey` mode can expose the packet and style menu.
- Planner/Hub unavailable: Given topic `UMI 数据可用性` and no explicit time range, the Review Skill uses the most recent six months, collects paper-entry-first web materials, labels source tiers, and produces a preliminary review packet under the review project folder.
- Insufficient evidence: Given only 3 paper-level sources, the Skill refuses formal scientific, longform, and short-form outputs, and instead lists missing coverage and recommended next searches.
- Multi-style conversion: Given one evidence core with at least 5 paper-level sources, the Skill can produce a scientific memo, expert explainer, and KOL thread with consistent claims and differing structure.
- Citation audit: Given a formal output, every substantive claim can be traced to event/source ID, paper-level source, or explicit inference.
- Propagation safety: Given a `conditional` claim, KOL output may sharpen the hook but must keep the condition visible.

## Out of Scope

- Replacing `$embodied-ai-query-planner`.
- Replacing `$embodied-ai-literature-hub`.
- Full-text HTML/PDF mining inside the Review Skill when Hub is available.
- Treating Reddit, X/Twitter, 知乎, 微博, 小红书 or other social content as accepted paper evidence.
- Automatically publishing to social platforms.
- Generating images, cards, cover art, or platform-specific visual layouts.
- Managing social accounts, comments, metrics, or scheduling.
- Automatically editing `knowledge/sources.md` or topic cards.
- Building a full web crawler or general literature-search MCP server.
- Creating a global plugin in v1.

## Further Notes

Future implementation should consider adding glossary entries to `CONTEXT.md` for `review packet`, `evidence core`, `style adapter`, and `style menu`. Those terms should remain glossary-only and avoid implementation details. If later implementation chooses to make Review Skill a long-term orchestrator with stable fallback source tiers, a separate ADR may be warranted; v1 keeps that decision inside this PRD.
