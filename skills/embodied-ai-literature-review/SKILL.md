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
3. Build the default readable Markdown review bundle. By default the script creates a new project folder under `work/` and prints the artifact paths: three style files plus `evidence-appendix.md` (per-event anchors that in-text event links resolve to):

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

4. Draft or transform from the packet:
   - `scientific-memo`: research boundary, evidence scope, claim map, caveats, source gaps.
   - `expert-explainer`: TL;DR, misconception/debate, mechanisms, evidence and limits, further reading.
   - `kol-thread`: strong hook, 3-5 evidence-bounded insights, visible caveat, compact source note.
   - Organize by argument, mechanism, disagreement, and gap; do not write one paragraph per paper unless the user asks.
   - Cite event IDs such as `EA-DATA-2026-0001` and stable source IDs such as `S-ARXIV-2402.10329`.
   - In formal outputs, event IDs and arXiv IDs must be Markdown links (appendix anchors and abs pages); see the citation and link contract in [review-contract.md](references/review-contract.md).
   - Mark inferences explicitly when a paragraph combines evidence across events.
5. Audit traceability:
   - Every substantive claim has an evidence event, topic-card source, or `inference` marker.
   - Candidate-only papers are not cited as established evidence.
   - Exact quotes come only from opened raw sources and stay short.
6. Settle the run:
   - Validate the evidence JSONL: `python3 skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py --evidence-jsonl <file> --validate-only`.
   - Copy accepted assets into `evidence/literature-review-<topic>-<date>/` with a `run.json` manifest (see `evidence/README.md`): evidence JSONL, the final Markdown artifacts, source-entry draft, and query plan. Intermediates stay in `work/`.

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
