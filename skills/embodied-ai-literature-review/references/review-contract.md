# Review Contract

Use this reference before drafting or auditing a full embodied-AI literature review.

## Boundary

`$embodied-ai-literature-review` writes and audits synthesis. Its default path is `planner -> hub -> briefing bundle -> agent-written three-style Markdown bundle`. **`build_review_packet.py` is a briefing generator, not an author**: it emits `review-packet.md` (audit surface), `writing-brief.md` (thesis-candidate tension pairs, topic-clustered evidence, mandatory caveats, per-style voice notes), and `evidence-appendix.md` (citation anchors). The default final deliverable — `scientific-memo_keyan.md`, `zhihu-explainer_zhihu.md`, `xiaohongshu-post_xiaohongshu.md` under `work/literature-review-<topic>-<date>/` — is ALWAYS written by the agent from the brief as argument-organized prose. Mechanical renders exist only as bannered `*.scaffold.md` files and are never deliverables. This Skill does not own query generation, full-text extraction, or evidence promotion when upstream Skills are available; use `$embodied-ai-query-planner` for query strategy and `$embodied-ai-literature-hub` for paper mining.

If the user does not specify a time range for paper discovery or fallback collection, use the most recent six months. Preserve the resolved time range in the review packet and final Markdown artifact.

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

When the threshold is met and no style is specified, produce all three final styles. Use a single style only when the user explicitly requests `scientific-memo`, `expert-explainer`, or `kol-thread`. Use `survey` only when the user asks for the intermediate review packet, style menu, source tiers, or audit surface as the final visible artifact.

## Output location

- Default output root: repository `work/`.
- Create a new review project folder named `literature-review-<topic>-<date>/`.
- The script writes the briefing bundle there (`review-packet.md`, `writing-brief.md`, `evidence-appendix.md`); the agent writes the deliverables next to them: `scientific-memo_keyan.md`, `zhihu-explainer_zhihu.md`, `xiaohongshu-post_xiaohongshu.md`.
- Use inline/stdout output only when the user asks for inline text, piping, or an explicit non-file display.
- After the run is settled, copy accepted assets into `evidence/literature-review-<topic>-<date>/` with a `run.json` manifest.

## Cross-run evidence

Combining evidence from prior runs is supported and encouraged (it is the accumulation payoff of the evidence layer), with three hard rules:

- Load prior evidence explicitly via repeated `--evidence-jsonl`; `load_events` deduplicates by `event_id`.
- Settle **every** evidence file the articles drew from into the run folder, and record the prior runs in `run.json` `source_runs`; `event_count` is the deduplicated count of events available to the articles.
- An article may only cite events in the settled evidence set — `scripts/audit_citations.py` enforces this, plus dead-anchor and manifest-drift checks, and must pass before settling.

## Citation and link contract

Formal outputs (scientific-memo, expert-explainer, kol-thread) must be readable AND clickable:

- Every in-text event ID is a Markdown link into `evidence-appendix.md` anchors: `[EA-…-0001](evidence-appendix.md#ea--0001)`. Bare event IDs in formal prose are non-conforming.
- Link targets are relative to the article's own folder: exactly `evidence-appendix.md#<anchor>`, never an invented subdirectory path.
- Every paper mention in claim maps and references is a Markdown link to its arXiv abs page: `[2606.13877](https://arxiv.org/abs/2606.13877)`. Bare arXiv IDs in formal outputs are non-conforming.
- Every formal output ends with a `## References` section: deduplicated papers, one line each, with inline links.
- `evidence-appendix.md` ships with every formal bundle: one `### <event_id>` section per event (claim, stance, confidence, locator, short quote, paper link). Event links resolve to these anchors.
- The review packet (audit mode) may keep plain IDs; the link contract applies to formal deliverables.

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

- Use for Zhihu/Reddit-style readable explanation. In the default bundle this is saved as `zhihu-explainer_zhihu.md`.
- Required structure: TL;DR, misconception/debate, mechanisms, evidence and limits, further reading/confidence.

`kol-thread`:

- Use for Xiaohongshu/Weibo/Twitter-style short insight threads. In the default bundle this is saved as `xiaohongshu-post_xiaohongshu.md`.
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
- In formal outputs, every event ID is an appendix link and every arXiv ID is an abs-page link (see Citation and link contract).
- Candidate-only papers are not cited as accepted evidence.
- Claims about consensus name the evidence coverage and its limits.
- Gaps distinguish "not found in this run" from "the literature says this is open."
- The final review states scope boundaries such as topic IDs, resolved time range, and search/evidence limitations.
