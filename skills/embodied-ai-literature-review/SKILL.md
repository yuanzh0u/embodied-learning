---
name: embodied-ai-literature-review
description: Orchestrate traceable embodied-AI literature reviews into three readable Markdown deliverables by default, with audit packets and single-style conversion available. Use when the user asks to write, outline, revise, audit, or transform a 具身智能/embodied-AI 文献综述, related-work section, scientific memo, Zhihu/Reddit explainer, Xiaohongshu/Weibo/Twitter thread, review packet, or claim map.
---

# Embodied AI Literature Review

## Overview

Turn embodied-AI evidence into a review, not another search run. The default orchestration path is `planner -> hub -> review packet -> style menu`: use `$embodied-ai-query-planner` for query strategy, `$embodied-ai-literature-hub` for accepted evidence, build a review packet internally, then synthesize the final artifact.

Default final deliverable: three Markdown files under a new `work/literature-review-<topic>-<date>/` project folder:
- `scientific-memo_keyan.md`: 科研文献综述/研究备忘录风格。
- `zhihu-explainer_zhihu.md`: 知乎科普帖/专家解释帖风格。
- `xiaohongshu-post_xiaohongshu.md`: 小红书网文/KOL 洞察帖风格。

**Division of labor:** `build_review_packet.py` is a briefing generator, not an author. It emits the writing inputs (`review-packet.md` + `writing-brief.md` + `evidence-appendix.md`); the three readable Markdown files above are ALWAYS written by the agent from `writing-brief.md`, as argument-organized prose. Never present the script's mechanical renders (claim-map tables, stance-bucket lists, `*.scaffold.md` files) as the finished articles.

Use `--style scientific-memo`, `--style expert-explainer`, or `--style kol-thread` only when the user asks for a single style. Use `survey` explicitly when the user wants the intermediate review packet, source tiers, and style menu instead of the final prose artifacts.

## Required inputs

- Topic or review question.
- Time range when discovering papers or invoking upstream literature mining. If no time range is provided, default to the most recent six months.
- Target style: optional. If absent, write all three default Markdown outputs. Use `scientific-memo`, `expert-explainer`, or `kol-thread` for one formal style output, and `survey` for the explicit review packet/style menu.
- At least one of:
  - evidence JSONL from `$embodied-ai-literature-hub`
  - fallback source-tier JSON from lightweight Browser/web collection
  - relevant `knowledge/embodied-ai/*.md` topic cards
  - a user-provided draft with citations to audit

Formal style outputs require at least 5 paper-level sources. If fewer are available, produce a preliminary packet, source gaps, and next search recommendations.

## Workflow

1. Load the repository routing layer:
   - `knowledge/index.md`
   - `knowledge/embodied-ai/index.md`
   - only the relevant topic cards.
2. Inspect available evidence:
   - Evidence JSONL and briefs from `$embodied-ai-literature-hub`.
   - `knowledge/sources.md` for stable source IDs.
   - Candidate lists only for search coverage, not accepted claims.
   - Fallback source-tier JSON only as review-packet context, not Hub evidence JSONL.
3. Generate the briefing bundle. By default the script creates a new project folder under `work/` and writes `review-packet.md` + `writing-brief.md` + `evidence-appendix.md` — these are writing inputs, not deliverables:

```bash
python skills/embodied-ai-literature-review/scripts/build_review_packet.py \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --evidence-jsonl /tmp/umi-evidence.jsonl \
  --topic-card knowledge/embodied-ai/data-collection-quality.md \
  --source-file knowledge/sources.md
```

Explicit review packet/style-menu output:

```bash
python skills/embodied-ai-literature-review/scripts/build_review_packet.py \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --evidence-jsonl /tmp/umi-evidence.jsonl \
  --style survey
```

Fallback packet input, which still degrades to a preliminary packet until paper-level evidence is sufficient. Omit `--time-range` to use the most recent six months; pass an explicit range only when the user asks:

```bash
python skills/embodied-ai-literature-review/scripts/build_review_packet.py \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --fallback-source-json /tmp/fallback-sources.json
```

Use `--output -` only when the user explicitly wants inline Markdown or stdout for another tool.

4. **Write the three articles (mandatory, never skipped).** From `writing-brief.md`, write each deliverable as continuous prose organized by argument, using the tension pairs as thesis candidates:
   - `scientific-memo`: 中心论点 → 派生矛盾/机制(prose 小节)→ 可操作框架 → 最短结论。research boundary, evidence scope, caveats, source gaps.
   - `expert-explainer`: 先破一个具体误区 → 讲机制 → 给适用边界 → 延伸阅读。TL;DR up front.
   - `kol-thread`: strong hook, 3-5 evidence-bounded insights, visible caveat, compact source note.
   - Save them under the same project folder with the exact deliverable filenames (`scientific-memo_keyan.md`, `zhihu-explainer_zhihu.md`, `xiaohongshu-post_xiaohongshu.md`), next to `evidence-appendix.md` so event links resolve.
   - Anti-patterns (a draft with any of these is NOT a deliverable): claim-map tables as body text; one-event-per-line/paragraph enumerations; stance-bucket lists presented as synthesis; the three styles sharing the same canned sentences; topic-agnostic filler ("不能只看一个漂亮结论"). If it reads like the review packet, rewrite it.
   - Organize by argument, mechanism, disagreement, and gap; do not write one paragraph per paper unless the user asks.
   - Cite event IDs such as `EA-DATA-2026-0001` and stable source IDs such as `S-ARXIV-2402.10329`.
   - In formal outputs, event IDs and arXiv IDs must be Markdown links (appendix anchors and abs pages); see the citation and link contract in [review-contract.md](references/review-contract.md). Link targets are relative to the article's own folder (`evidence-appendix.md#...`, never an invented path).
   - Mark inferences explicitly when a paragraph combines evidence across events.
5. Audit traceability:
   - Every substantive claim has an evidence event, topic-card source, or `inference` marker.
   - Candidate-only papers are not cited as established evidence.
   - Exact quotes come only from opened raw sources and stay short.
6. Settle the run:
   - Validate the evidence JSONL: `python3 skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py --evidence-jsonl <file> --validate-only`.
   - Copy accepted assets into `evidence/literature-review-<topic>-<date>/` with a `run.json` manifest (see `evidence/README.md`): **every** evidence JSONL the articles drew from (fresh and reused), the final Markdown articles, `evidence-appendix.md`, source-entry draft, and query plan. Intermediates stay in `work/`.
   - Cross-run evidence is supported but must be recorded: `run.json` lists `source_runs` (the prior runs whose evidence was combined) and `event_count` equals the deduplicated count actually available to the articles. Never cite an event that is not in the settled evidence set.
   - Audit before settling: `python3 scripts/audit_citations.py --article <each article> --appendix <appendix> --evidence-jsonl <each evidence file>` must pass (no dead anchors, no citations outside the loaded evidence).

## Review rules

- Prefer claim maps over chronological summaries.
- Preserve stance labels: `support`, `limit`, `conditional`, `gap`.
- Preserve confidence labels: `direct`, `citation-supported`, `inference`.
- Keep author/institution statements conservative; do not infer affiliations from paper-level metadata.
- Use topic cards as compressed context, not as a substitute for paper-level evidence when exact claims matter.
- Topic-card updates are suggestions only unless the user explicitly asks to edit the knowledge base.

## References

- Read [review-contract.md](references/review-contract.md) before drafting or auditing a full review.
- Read [templates.md](references/templates.md) when the user asks for a specific section shape, Chinese wording, or a related-work draft.
