# Review Contract

Use this reference before drafting or auditing a full embodied-AI literature review.

## Boundary

`$embodied-ai-literature-review` writes and audits synthesis. Its default path is `planner -> hub -> review packet -> style menu`. It does not own query generation, full-text extraction, or evidence promotion when upstream Skills are available. Use `$embodied-ai-query-planner` for query strategy and `$embodied-ai-literature-hub` for paper mining.

## Evidence inputs

Accepted inputs, strongest first:

1. Evidence JSONL events from `$embodied-ai-literature-hub`.
2. Source entries in `knowledge/sources.md` or a generated source-entry draft.
3. Topic cards under `knowledge/embodied-ai/`.
4. Fallback source-tier JSON from lightweight Browser/web collection.
5. User-provided drafts, notes, or bibliographies.
6. Candidate lists, only to describe search coverage and missing evidence.

Candidate-only papers cannot support a review claim. They may appear in a "coverage and future inspection" note.

Fallback source-tier records are review-packet context, not Hub evidence JSONL. They may identify paper-level sources, official context, web context, or social calibration, but they do not become accepted evidence unless later promoted by the literature-mining workflow.

## Traceability levels

Use one of these labels for every synthesized claim:

- `evidence-event`: backed by an evidence JSONL event with locator.
- `topic-card-source`: backed by an existing topic-card claim and its source entry.
- `source-entry`: backed by a registered source but not yet atomized into JSONL.
- `inference`: synthesized by the agent from multiple sources; state why the inference follows and what would falsify it.

Prefer `evidence-event` for paper-specific claims and `topic-card-source` for stable domain background.

## Sufficiency gate

Formal style outputs require at least 5 paper-level sources and accepted evidence events. If this threshold is not met, produce a preliminary review packet with coverage gaps and next search recommendations instead of a formal review, explainer, or KOL thread.

## Source tiers

- `paper-level`: arXiv, OpenReview, conference pages/proceedings, author-hosted PDFs, and paper records that identify a paper.
- `official-context`: official project pages, repositories, lab pages, dataset/model cards.
- `web-context`: technical blogs, company posts, media articles, newsletters.
- `social-calibration`: Reddit, X/Twitter, 知乎, 微博, 小红书, and similar discussion surfaces.

Only `paper-level` sources and accepted evidence events can support scientific claims. The other tiers can shape framing, coverage gaps, and further-search suggestions.

## Style adapters

`scientific-memo`:

- Use for research-facing synthesis.
- Required structure: scope, evidence sufficiency, claim map, evidence clusters, disagreements/conditions, gaps, implications.

`expert-explainer`:

- Use for Zhihu/Reddit-style readable explanation.
- Required structure: TL;DR, misconception/debate, mechanisms, evidence and limits, further reading/confidence.

`kol-thread`:

- Use for Xiaohongshu/Weibo/Twitter-style short insight threads.
- Required structure: strong hook, 3-5 evidence-bounded insights or 5-8 thread items, visible caveat, compact source note.

## Synthesis rules

- Organize by claims, mechanisms, assumptions, and failure modes, not by paper order.
- Preserve opposing and conditional evidence; do not flatten `limit` and `conditional` into neutral summaries.
- Separate "what papers show" from "what this implies for the user's project."
- Do not merge same-name authors or infer institutional positions unless evidence explicitly supports it.
- Use exact wording from raw sources only when wording matters. Otherwise paraphrase and cite the evidence event/source ID.
- Keep the knowledge base compact: put topic-card update suggestions in a separate section and edit cards only when requested.
- Style adapters may change framing, length, and ordering, but cannot upgrade `conditional`, `limit`, or `gap` into consensus.

## Minimum audit checklist

- Each paragraph has at least one event ID, source ID, or explicit `inference` marker.
- Each cited event includes stance and confidence.
- Candidate-only papers are not cited as accepted evidence.
- Claims about consensus name the evidence coverage and its limits.
- Gaps distinguish "not found in this run" from "the literature says this is open."
- The final review states scope boundaries such as topic IDs, time range, and search/evidence limitations when known.
