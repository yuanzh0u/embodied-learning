# Review Contract

Use this reference before drafting or auditing a full embodied-AI literature review.

## Boundary

`$embodied-ai-literature-review` owns evidence orchestration and the briefing bundle. Its default path is `planner -> hub -> review packet -> writing brief -> $embodied-ai-review-writer`. **`build_review_packet.py` is a briefing generator, not an author**: it emits `review-packet.md` (audit surface), `writing-brief.md` (thesis candidates, topic-clustered evidence, mandatory caveats), and `evidence-appendix.md` (citation anchors). `$embodied-ai-review-writer` independently drafts and editorially audits the three reader-facing files. Mechanical renders exist only as bannered `*.scaffold.md` files and are never deliverables.

If the user does not specify a time range for paper discovery or fallback collection, use the most recent six months. Preserve the resolved time range and review mode in the packet and final artifact.

Workflow-v2 reviews also require `candidate-registry.json` and
`coverage-report.json`. The registry preserves every discovered paper and its
screening state; the report proves that size floors, query dimensions,
full-text recovery, accepted evidence, and saturation all pass.

## Paper-reading extension

For new or migrated evidence, require `paper-notes/`, `reading-ledger.jsonl`,
and `reading-summary.json` from `$embodied-ai-paper-reader`. Keep these counts
separate: `full_text_recovered_count`, `map_read_count`, `deep_read_count`,
`claim_verified_paper_count`, and `accepted_evidence_paper_count`.

Full-text recovery is not reading. Candidate/query-label coverage is not
accepted-evidence coverage. New formal evidence must be projected from a
validated paper note with a passing claim-support audit. Legacy events remain
traceable but must not be reported as newly re-read until they pass this gate.

Use HTML or text-layer PDF only. Scan-only PDFs are `unavailable`; this project
does not use OCR/Tesseract.

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

Formal style outputs in workflow v2 require the mode floor (`rapid` 8,
`scoping` 15, `systematic` 30 accepted papers) plus a passed coverage/saturation
report. These are floors, not caps. Historical migrations without a v2
manifest retain the five-paper compatibility gate but must not be represented
as newly completed searches.

When the threshold is met and no style is specified, produce all three final styles. Use a single style only when the user explicitly requests `scientific-memo`, `expert-explainer`, or `kol-thread`. Use `survey` only when the user asks for the intermediate review packet, style menu, source tiers, or audit surface as the final visible artifact.

## Output location

- Default output root: repository `work/`.
- Create a new review project folder named `literature-review-<topic>-<date>/`.
- The script writes the briefing bundle there (`review-packet.md`, `writing-brief.md`, `evidence-appendix.md`); `$embodied-ai-review-writer` writes the deliverables next to them and generates `trace-map.json`.
- Use inline/stdout output only when the user asks for inline text, piping, or an explicit non-file display.
- After the run is settled, copy accepted assets into `evidence/literature-review-<topic>-<date>/` with a `run.json` manifest.

## Bundle completeness

**The folder name is the contract trigger.** Anything named `literature-review-<topic>-<date>` owes the full bundle; non-review artifacts (research outlines, experiment designs, synthesis notes) must use a different name (e.g. `research-outline-<topic>-<date>`).

- Runs begin with `python3 scripts/init_run.py` — a birth-certificate run.json with `status: in-progress`. The status flips to `settled` only when the bundle is complete and both gates pass. An `in-progress` run fails `check_run_bundle.py` by design.
- **Unfinished-run honesty**: stopping mid-pipeline for any reason is allowed, but must be declared — the run stays `in-progress` in `work/` and the user is told explicitly what is missing (search not run, candidates unpromoted, articles unwritten). A silently abandoned run presented as output is a contract violation.
- Default deliverables: all three styles (`scientific-memo_keyan.md`, `zhihu-explainer_zhihu.md`, `xiaohongshu-post_xiaohongshu.md`) plus `evidence-appendix.md`. These are the ONLY recognized deliverable filenames; an invented name is not a deliverable.
- Reduced scope is legal only when declared: `run.json` records `"style": "<formal-style>"` and `"scope_note": "<why — the user's explicit ask>"`. An undeclared missing style is a contract violation, not a judgment call.
- The run folder must be self-contained: `files.evidence` (fresh) and/or `files.reused_evidence` (copied from prior runs) exist inside the folder; `event_count` equals the deduplicated local evidence.
- Workflow-v2 manifests set `workflow_version: 2`, declare `review_mode`, and list `files.query_plan`, `files.candidate_registry`, and `files.coverage_report`. Settlement is blocked while `stop_assessment.ready_to_stop` is false.
- `run.json` uses the standard schema (see `evidence/README.md`); invented field names (`selected_event_count`, `files.memo`, …) are rejected by the checker.
- Gate: `python3 scripts/check_run_bundle.py <run-dir>` must pass before settling, alongside `audit_citations.py`.

## Cross-run evidence

Combining evidence from prior runs is supported and encouraged (it is the accumulation payoff of the evidence layer), with three hard rules:

- Load prior evidence explicitly via repeated `--evidence-jsonl`; `load_events` deduplicates by `event_id`. For targeted syntheses, select the relevant events with `--select-event`/`--select-events-file` instead of hand-curating an appendix, and pass `--consolidate-evidence` so the working set lands as the run's own `evidence.jsonl`.
- Settle **every** evidence file the articles drew from into the run folder, and record the prior runs in `run.json` `source_runs`; `event_count` is the deduplicated count of events available to the articles.
- An article may only cite events in the settled evidence set — `scripts/audit_citations.py` enforces this, plus dead-anchor and manifest-drift checks, and must pass before settling.

## Citation and link contract

Formal outputs must be readable and auditable, with **paper links on the reader surface and event-level traceability on a separate audit surface**:

- **Body citations are arXiv paper links**: `[SIEVE](https://arxiv.org/abs/2607.06442)` or `[2607.06442](https://arxiv.org/abs/2607.06442)` — the reader lands on the paper, not on an internal ID. Bare paper names, bare arXiv IDs, and bare event IDs in formal prose are all non-conforming.
- **Do not put `evidence-appendix.md#...` event links in body prose.** Event anchors live in `trace-map.json`, the appendix, and the review packet. A reader skimming the article should only ever be one click from arXiv.
- Every cited paper must be in the loaded evidence set (audit-enforced); citing a paper that no settled event covers is non-conforming.
- Citation surfaces vary by audience: the scientific memo keeps a full `## References`; Zhihu keeps 3-8 annotated readings or references; Xiaohongshu keeps only 3-5 representative links and a compact `📚 依据` note.
- `trace-map.json` maps every cited arXiv paper in every article to the accepted event IDs and appendix anchors that cover it. An uncovered paper is a hard error.
- `evidence-appendix.md` ships with every formal bundle: one `### <event_id>` section per event (claim, stance, confidence, locator, short quote, paper link). Reference-section event links resolve to these anchors, relative to the article's own folder — never an invented subdirectory path.
- The review packet (audit mode) keeps event-ID-first linking; the paper-first rule applies to formal deliverables.

## Source tiers

- `paper-level`: arXiv, OpenReview, conference pages/proceedings, author-hosted PDFs, and paper records that identify a paper.
- `official-context`: official project pages, repositories, lab pages, dataset/model cards.
- `web-context`: technical blogs, company posts, media articles, newsletters.
- `social-calibration`: Reddit, X/Twitter, 知乎, 微博, 小红书, and similar discussion surfaces.

Only `paper-level` sources and accepted evidence events can support scientific claims. The other tiers can shape framing, coverage gaps, and further-search suggestions.

## Style adapters

Style requirements live in `$embodied-ai-review-writer` and are loaded only for the requested audience. This contract defines evidence boundaries, not prose templates.

## Synthesis rules

- Organize by claims, mechanisms, assumptions, and failure modes, not by paper order.
- Preserve opposing and conditional evidence; do not flatten `limit` and `conditional` into neutral summaries.
- Separate "what papers show" from "what this implies for the user's project."
- Do not merge same-name authors or infer institutional positions unless evidence explicitly supports it.
- Use exact wording from raw sources only when wording matters. Otherwise paraphrase and cite the evidence event/source ID.
- Keep the knowledge base compact: put topic-card update suggestions in a separate section and edit cards only when requested.
- Style adapters may change framing, length, and ordering, but cannot upgrade `conditional`, `limit`, or `gap` into consensus.

## Minimum audit checklist

- Every reader-facing paper link maps to at least one accepted event in `trace-map.json`.
- Event stance, confidence, and locator remain complete in `evidence-appendix.md`.
- Body prose contains no event IDs, stance buckets, or packet metadata.
- Candidate-only papers are not cited as accepted evidence.
- Claims about consensus name the evidence coverage and its limits.
- Paper counts are described as accepted evidence coverage, not the size of the whole field.
- Gaps distinguish "not found in this run" from "the literature says this is open."
- The final review states scope boundaries such as topic IDs, resolved time range, and search/evidence limitations.
- The writer's editorial audit passes language, template-leakage, platform-density, length, and cross-style overlap gates.
