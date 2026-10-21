---
name: embodied-ai-review-writer
description: Orchestrate coverage-driven embodied-AI literature reviews end to end and write or rewrite publication-ready, natural Chinese content from a formal-ready brief and a potentially large evidence reservoir. Owns review-mode selection, candidate registries, saturation auditing, validated briefs, settled runs; use for researching, auditing, or producing evidence-grounded scientific research memos, 知乎专家解释稿, 小红书洞察帖, reveal.js 汇报展示 (slide decks), full three-style bundles, or when articles are traceable but shallow, packet-like, repetitive, formulaic, under-cited, or not audience-specific.
---

# Embodied AI Review Writer

## Purpose

Turn an embodied-AI question into validated writing inputs and then into genuinely different reader-facing articles. This Skill owns the review **end to end**: it orchestrates `$embodied-ai-literature-hub` (query planning, search, candidate registries, coverage/saturation, full-text recovery) and `$embodied-ai-paper-reader` (deep reading, claim verification, evidence projection), then writes and editorially audits the deliverables. It never presents candidates as evidence and never bypasses the projection gates.

The current migration path is `review mode -> planner -> candidate registry -> coverage/saturation -> HTML/PDF recovery -> $embodied-ai-paper-reader -> review packet -> writing brief -> $embodied-ai-review-writer`. Existing workflow-v2 runs remain readable; new evidence should use the paper-reading extension before workflow-v3 becomes mandatory.

Default final deliverable: three Markdown files under a new `work/literature-review-<topic>-<date>/` project folder:
- `scientific-memo_keyan.md`: 科研文献综述/研究备忘录风格。
- `zhihu-explainer_zhihu.md`: 知乎科普帖/专家解释帖风格。
- `xiaohongshu-post_xiaohongshu.md`: 小红书网文/KOL 洞察帖风格。
- `slide-deck_report.html`: 汇报展示风格（reveal.js 单文件放映件；源文件 `slide-deck_report.md`，由 `skills/embodied-ai-review-writer/scripts/write.py compile-slide-deck` 编译，代理只写 slide-source，见 [slide-deck.md](references/slide-deck.md)）。

Another style exists outside the review bundle: `quick-read_sudu.md`（速读卡，see [quick-read.md](references/quick-read.md)）is a **single-paper pool artifact**, not a literature-review deliverable. Its inputs are one paper's deep-read `note.json` + `paper.md` from the public pool — never a writing brief — and it is generated per paper by `skills/embodied-ai-paper-reader/scripts/read.py quick-read`; it never appears inside a `literature-review-<topic>-<date>/` folder.

**Division of labor:** `write.py review-packet` is a briefing generator, not an author. It emits `review-packet.md` + `writing-brief.md` + `evidence-appendix.md`; the writing stage writes and editorially audits the three reader-facing files. Never present mechanical renders (`*.scaffold.md`) as finished articles.

**Figures are part of the deliverable.** Evidence events may carry `evidence.figures[]/tables[]` (joined from the deep-read flow); `write.py review-packet` renders them into the brief's 可用图表 section and the appendix. The writing stage must embed those ready-made blocks in each style within its cap (memo ≤4 图+1 表 / zhihu ≤2 / xiaohongshu ≤1 — see each style reference's Figures section). Figure source discipline equals citation discipline: only `evidence`-carried figures, URLs and captions copied verbatim, never invented.

## Required inputs

- Topic or review question.
- Time range when discovering papers or invoking upstream literature mining. If no time range is provided, default to the most recent six months.
- Review mode: `rapid`, `scoping` (default), or `systematic`. Treat every size target as a floor, never as a cap.
- Target style: optional. If absent, write all three default Markdown outputs. Use `scientific-memo`, `expert-explainer`, `kol-thread`, or `slide-deck` for one formal style output, and `survey` for the explicit review packet/style menu.
- At least one of:
  - evidence JSONL from `$embodied-ai-literature-hub`
  - fallback source-tier JSON from lightweight Browser/web collection
  - relevant `knowledge/embodied-ai/*.md` topic cards
  - a user-provided draft with citations to audit

New formal outputs require both the mode's accepted-paper floor (`rapid` 8, `scoping` 15, `systematic` 30) and a passed coverage/saturation report. A high paper count without negative, evaluation, deployment, or adjacent coverage remains preliminary.

If no validated brief exists, produce one with the run lifecycle and briefing workflow below — candidate lists and raw search results are not writing evidence.
If the brief says `Writing readiness: preliminary` or its coverage gate is blocked, return it to research instead of writing formal articles.

## Run lifecycle and gates

0. **Decide the deliverable shape (before any writing).** Default is the full three-style bundle. A single style is allowed ONLY when the user explicitly asks for it — record that decision in `run.json` as `"style": "<formal-style>"` plus `"scope_note": "<the user's ask, in their words>"`. The ONLY recognized deliverable filenames are `scientific-memo_keyan.md` / `zhihu-explainer_zhihu.md` / `xiaohongshu-post_xiaohongshu.md` / `slide-deck_report.html` (with its `slide-deck_report.md` slide-source) — an invented filename (research-memo.md, main-*.md, …) is not a deliverable, whatever its quality. Non-review artifacts (research outlines, experiment designs, synthesis notes) must NOT use a `literature-review-<topic>-<date>` folder name — that name IS the bundle contract trigger; use e.g. `work/research-outline-<topic>-<date>/` instead.
1. Initialize the run, then load the repository routing layer:
   - `python3 scripts/run.py init --topic "..." --knowledge-id EA-… --time-range "..." --review-mode scoping` creates a workflow-v2 run with `status: in-progress`.
   - **If you stop for any reason before settling** (search failed, evidence insufficient, out of time), leave the run `in-progress` in `work/` and TELL THE USER explicitly that the run is unfinished, listing the missing steps. A silently abandoned run that looks like a deliverable is a contract violation; an honestly declared partial run is fine.
   - `knowledge/index.md`, `knowledge/embodied-ai/index.md`, and only the relevant topic cards.
2. Build and widen the candidate pool (via `$embodied-ai-literature-hub`):
   - Generate a mode-aware query plan with the Hub's in-skill planning step (`search.py build-query-plan`).
   - Search in multiple API/Browser batches; merge them with `search.py build-candidate-registry`.
   - Screen titles/abstracts for priority only. Candidate count is not evidence count.
   - Run `search.py assess-review-coverage` after every batch. Continue until all floors, all dimensions, and consecutive saturation rounds pass.
3. Recover, read, and verify full text:
   - Use the Hub's unified `fetch.py extract-content`: HTML -> text-layer PDF, with `--ocr-mode never --include-full-text`.
   - Keep scan-only or otherwise unrecoverable papers in the registry as `unavailable` rather than silently dropping them.
   - Pass complete extraction payloads to `$embodied-ai-paper-reader`; ranked passages are navigation hints, not reading evidence.
   - Prefer one-shot paper notes; keep six-pass as optional deep mode. Respect the **LLM deep-read budget** (`accepted_floor + 10` by default) while still meeting the **evidence floor** — see [review-contract.md](references/review-contract.md). Soft-check with `skills/embodied-ai-review-writer/scripts/write.py check-deep-read-budget`; a warning is a reason to narrow the next batch, not to bypass the evidence gate.
   - Require a validated paper note and passing claim-support audit before projecting evidence events.
   - Inspect evidence JSONL and briefs from `$embodied-ai-literature-hub`; inspect `knowledge/sources.md` for stable source IDs.
   - Use candidate lists only for search coverage, not accepted claims; use fallback source-tier JSON only as review-packet context, not Hub evidence JSONL.
   - **Articles cite verified evidence only.** If the synthesis needs a candidate paper, recover its complete text, read it with `$embodied-ai-paper-reader`, audit it, and project its events before writing.
7. Settle the run — one mechanical command, no manual steps:
   - `python3 scripts/run.py finalize --run-dir <run-dir> --kb-root <kb-root>` does ALL of the settle/publish mechanics: stamps run.json (`event_count`/`evidence_papers`/`candidate_count`/`full_text_count`, `files.evidence` by consolidating `evidence/*.jsonl`, `style`+`scope_note` when a single deliverable exists), enforces the per-mode cited-paper floor (rapid 6 / scoping 10 / systematic 15), copies accepted assets into `evidence/<run>/`, flips `settled`, registers the catalog row (scale triple 候选/全文/精读 included), and rebuilds the wiki snapshot. Gate failures print what is missing — fix and rerun; a gate miss is never a stop-and-explain condition. Never flip `run.json` status, hand-copy evidence assets, edit the catalog table, run `wiki.py build-wiki`, or verify the served `/data/current.json` topic count yourself — those are run.py finalize's mechanical duties, and redoing them by hand is a contract violation.
   - Insufficient deep-read count (cited-paper-floor shortfall, including honest selection shortfall) is a designed USER DECISION POINT (2026-09-30): report the selected deep-read paper list, stop immediately (emit `[STOP:awaiting-user]` in wiki workflow runs), leave the run `in-progress`, and wait for the user to supplement information (seeds/focus) or widen the review scope (review-mode/time range). Do NOT settle thin, switch `--selection-strategy`, delete/rewrite mechanical artifacts, hand-edit run.json, or keep force-fixing.
   - Cross-run evidence is supported but must be recorded: `run.json` lists `source_runs` (the prior runs whose evidence was combined) and `event_count` equals the deduplicated count actually available to the articles. Never cite an event that is not in the settled evidence set.
   - Audit before settling — all gates must pass:
     - `python3 scripts/run.py check-bundle <run-dir>` (bundle completeness: three styles or a declared `style`+`scope_note`, self-contained evidence, standard run.json schema).
     - `python3 scripts/run.py audit-citations --article <each article> --appendix <appendix> --evidence-jsonl <each evidence file> --run-json <run.json>` (no dead anchors, no citations outside the loaded evidence).
     - `python3 skills/embodied-ai-review-writer/scripts/write.py audit-article-quality --bundle-dir <run-dir>` (reader-facing editorial quality and cross-style differentiation). ERROR findings block; WARNING findings (long sentences, acronym load, prose length) do not — the command exits 0 on warnings alone. Judge each warning once on reader impact, fix the ones that matter, and report the rest instead of chasing a zero-warning draft. The long-sentence warning lists every offending sentence in one pass, quoted verbatim including its closing punctuation — use that text as the `old_string`.
   - `run.py check-bundle` enforces the v2 coverage artifacts and refuses settlement while `ready_to_stop=false`. The gate's own failure message lists the sanctioned remedies (resume the driver, or declare a non-floor exception mechanically via `run.py finalize --declare-gate-exception <name> --reason "..."` — the justification lands in `notes`; never hand-edit run.json). The cited-paper floor has no writer-side remedy: a shortfall is the user decision point described above.

For a legacy multi-run paper-reader upgrade, keep every old settled run immutable. Build and audit the replacement under `work/`, then publish it under a new suffixed directory such as `literature-review-<topic>-<date>-reader-v1`. The replacement run must include `paper-notes/`, `claim-support-audits/`, `reading-ledger.jsonl`, `reading-summary.json`, their indexes, regenerated evidence/brief/appendix/trace map, and all three audited articles. Only switch it to `settled` after all reading, citation, editorial, and bundle gates pass.

Post-settle article revisions go through the wiki revision flow (topic chat's 修订成稿 toggle → `/api/topic/revise`): the agent adds `revisions/<style>-v<N>.md` inside the published run and never edits the base deliverables, `run.json`, `trace-map.json`, or `evidence-appendix.md`. Revisions re-run the article gates (build-trace-map into `revisions/`, `audit-article-quality` single style, `audit_citations`) against the run's own evidence set.

## Briefing generation

Generate the briefing bundle with the coverage report attached; the script writes `review-packet.md` + `writing-brief.md` + `evidence-appendix.md` as validated writing inputs:

```bash
python skills/embodied-ai-review-writer/scripts/write.py review-packet \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --evidence-jsonl /tmp/umi-evidence.jsonl \
  --review-mode scoping \
  --coverage-report work/<run>/coverage-report.json \
  --reading-summary work/<run>/reading-summary.json \
  --topic-card knowledge/embodied-ai/data-collection-quality.md \
  --source-file knowledge/sources.md
```

Selective reuse from prior runs (pick specific events, and settle the working set as this run's own evidence.jsonl):

```bash
python skills/embodied-ai-review-writer/scripts/write.py review-packet \
  --topic "感知误差溯源" \
  --knowledge-id EA-DATA --knowledge-id EA-SENSOR \
  --evidence-jsonl evidence/literature-review-<prior-run-a>/evidence.jsonl \
  --evidence-jsonl evidence/literature-review-<prior-run-b>/evidence.jsonl \
  --select-events-file /tmp/selected-ids.txt \
  --consolidate-evidence
```

`--select-event`/`--select-events-file` filter to named event IDs (unknown IDs error out); `--consolidate-evidence` writes the working set as the run's local `evidence.jsonl`, so the folder is self-contained. Always pass `--consolidate-evidence` when reusing prior evidence.

Explicit review packet/style-menu output (`--style survey` when the user wants the intermediate review packet, source tiers, and style menu instead of the final prose artifacts):

```bash
python skills/embodied-ai-review-writer/scripts/write.py review-packet \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --evidence-jsonl /tmp/umi-evidence.jsonl \
  --style survey
```

Fallback packet input, which still degrades to a preliminary packet until paper-level evidence is sufficient. Omit `--time-range` to use the most recent six months; pass an explicit range only when the user asks:

```bash
python skills/embodied-ai-review-writer/scripts/write.py review-packet \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --fallback-source-json /tmp/fallback-sources.json
```

Use `--output -` only when the user explicitly wants inline Markdown or stdout for another tool.

### Abstract-tier evidence (`tier: abstract`)

A run may also load abstract-tier events (appendix section 「摘要级相关工作」, `tier: abstract`): registry-metadata positioning for the candidate landscape. Their object is the **selection result** (`screening-ids.txt`, including papers whose full text was held), not the raw candidate registry — a paper the selector rejected never enters the appendix. Use them only for related-work positioning sentences — who did what in which direction — never as mechanism conclusions, comparison evidence, or central-thesis support. Cite them in body prose with the ordinary arXiv paper link and append （摘要级） to the References entry. Abstract-tier events have no per-event appendix heading: their only anchor is the shared 「摘要级相关工作」 section. The cited-paper floor (`evidence_papers`) counts full-text-tier papers only.

Then hand the validated brief to the writing workflow below (mandatory for prose deliverables): pass `writing-brief.md`, `evidence-appendix.md`, every accepted evidence JSONL, and the requested style(s); save the exact deliverable filenames in the same run folder; run `write.py audit-article-quality` — `trace-map.json` is built mechanically at settle (run.py finalize; the headless launcher builds it before the gate loop), never hand-written. A traceable scaffold is not an article.

## Token / context soft guards

- Load this `SKILL.md` plus the **current step's** references only. Do not preload every upstream skill or the full `knowledge/literature-review-catalog.md` — grep topic/knowledge-ID rows when routing to an existing run.
- Hub stage: never dump `candidate-registry.json` or search-round JSON into context; use coverage reports / title-only slices.
- Reader stage: prefer `read.py build-reading-packet --summary-first` for scoping; full extraction stays on disk for locator windows.
- Writer stage: `write.py review-packet` applies stance caps to `writing-brief.md` / `evidence-appendix.md` (default support≤8, limit≤6, conditional≤6, gap≤4). Complete events remain in `evidence.jsonl` for claim/citation audits. Override with `--writer-stance-caps` or `--uncapped-writer` only when debugging.

## Load only the selected style guidance

- Scientific research memo: read [scientific-memo.md](references/scientific-memo.md).
- Zhihu expert explainer: read [zhihu-explainer.md](references/zhihu-explainer.md).
- Xiaohongshu insight post: read [xiaohongshu-post.md](references/xiaohongshu-post.md).
- Quick-read card (single paper): read [quick-read.md](references/quick-read.md).
- Always read [editorial-quality-rubric.md](references/editorial-quality-rubric.md) and [citation-projection.md](references/citation-projection.md).

For a full bundle, read all three style references, but plan and draft each article independently from the brief. Never derive Zhihu or Xiaohongshu prose by shortening the scientific memo.

## Writing workflow

With a validated brief in hand (from the briefing step above or supplied by the caller), draft the reader-facing articles:

10. **Use the existing evidence gates.** Run `scripts/run.py audit-citations` and `scripts/run.py check-bundle` before settlement. Editorial gates complement evidence gates; neither substitutes for the other.

## Migrating an existing three-style bundle

When a paper-reader migration replaces an old evidence set, preserve mature prose only where its cited papers remain accepted. Drop whole unsupported prose blocks, add manually authored replacement arguments from the new brief, rebuild compact references, and regenerate the trace map (`article-updates.json` remains a manually written editorial input, not a claim generator).

After migration, read all three articles again. Removing an unreadable citation is not enough if its unsupported claim remains in plain text. Run `build-trace-map`, `audit-article-quality`, and `audit-citations` on every migrated run.

```bash
python3 skills/embodied-ai-review-writer/scripts/write.py build-trace-map \
  --evidence-jsonl <run>/evidence.jsonl \
  --article <run>/scientific-memo_keyan.md \
  --article <run>/zhihu-explainer_zhihu.md \
  --article <run>/xiaohongshu-post_xiaohongshu.md \
  --output <run>/trace-map.json

python3 skills/embodied-ai-review-writer/scripts/write.py audit-article-quality \
  --memo <run>/scientific-memo_keyan.md \
  --zhihu <run>/zhihu-explainer_zhihu.md \
  --xiaohongshu <run>/xiaohongshu-post_xiaohongshu.md
```

For a published Zhihu collection, also audit corpus-level repetition, template concentration, and accessibility distributions:

```bash
python3 skills/embodied-ai-review-writer/scripts/write.py audit-zhihu-corpus \
  --topics-dir wiki/data/topics \
  --project-root .
```

### Outline-first (token optimization)

Do **not** feed the full brief / appendix into three independent genre drafts. Share a compact outline + projected cards instead.

1. **One outline LLM call.** From the writing brief (stance-capped when the briefing generator provides caps) and evidence reservoir, produce `writing-outline.json`:

```json
{
  "thesis": "一句话中心论点",
  "claim_clusters": ["…", "…"],
  "counterevidence_notes": ["…"],
  "mandatory_caveats": ["…"],
  "event_ids": ["EA-…-0001", "EA-…-0002"]
}
```

Select **8–12** `event_id`s that cover support, limit/conditional, and gap as needed. This call establishes the shared argument; it is not a draft of any genre.

2. **Project short evidence cards** for those IDs only (not the full brief thrice):

```bash
python3 skills/embodied-ai-review-writer/scripts/write.py project-outline-evidence \
  --outline work/<run>/writing-outline.json \
  --evidence-jsonl work/<run>/evidence.jsonl \
  --output work/<run>/outline-evidence.json \
  --markdown-output work/<run>/outline-evidence.md
```

Each genre draft loads `outline-evidence.md` (or JSON) plus the style reference — not a second full copy of `writing-brief.md` / `evidence-appendix.md`. Keep the brief available for audit, but do not re-ingest it as prompt ballast for every style.

3. **Write a reader contract and independent editorial plan for each style.** Name the intended reader, their live question, the one-sentence takeaway, the decision consequence, one evidence-backed running example, the core terms that need explanation, the representative source subset (subset of the outline `event_ids`), excluded details, and the ending. Do not reuse an outline-as-prose or simply cite every accepted paper. Independence still matters: three editorial plans, one shared evidence projection.

4. **Draft complete explanation units** from the projected cards. Move from concrete phenomenon to mechanism, representative evidence, reader consequence, and boundary. Write in natural Chinese. Translate and synthesize English evidence claims; never paste or mechanically translate event claims one by one. Use paper links in body prose where the selected style permits them.

5. **Project provenance.** Keep reader-facing citations compact and put event-level mapping in `trace-map.json` plus `evidence-appendix.md`. Follow [citation-projection.md](references/citation-projection.md).
6. **Edit the argument.** Check the thesis, counterevidence, causal order, and overclaiming before polishing individual sentences.
7. **Run an evidence-locked natural-writing pass.** Freeze every factual claim, paper link, number, date, named entity, quote, uncertainty marker, and boundary condition. Then remove chatbot residue, empty promotion, vague attribution, redundant signposting, synonym cycling, generic conclusions, and monotonous sentence rhythm. Do not add specificity, personal experience, or confidence to make the prose sound more human. Common technical words and punctuation are not faults by themselves; change them only when the surrounding sentence is weak. The selected platform guide outranks generic style heuristics.
8. **Inspect the publication surface.** Reject unresolved citation anchors, missing subjects, malformed punctuation, internal reasoning labels, unannotated reading lists, and reference dumps. Check whether a non-specialist can restate the thesis without the paper names or acronyms.
9. **Run deterministic gates.** Build the trace map, then audit the three outputs:

## Hard rules

- Treat the brief, claim map, stance buckets, and evidence appendix as inputs, never as article body.
- Prefer outline-first: one thesis + 8–12 event_ids, then genre drafts from projected short cards — do not paste the full brief into three genre prompts.
- Give each article one explicit central thesis and an evidence-bounded conclusion.
- Preserve `conditional`, `limit`, and `gap` evidence as visible boundaries; do not manufacture consensus.
- Keep event IDs out of body prose. Use arXiv paper links for readers and the trace map for audit.
- Do not leak workflow language such as “formal-ready”, “stance labels”, “output type”, “strong hook is allowed”, or instructions addressed to the writer.
- Do not use topic-agnostic filler or the same opening, paragraph, or conclusion in two styles.
- Do not present untranslated English evidence claims as Chinese articles.
- Do not leave generic citation anchors such as “相关研究” in publication-ready prose. Name the accepted paper or describe the supported function precisely enough for the reader to understand why the citation is present.
- Never introduce a fact, name, number, date, quote, example, personal experience, or citation that is absent from the validated inputs. When specificity is missing, keep the plain bounded claim or return to research.
- Preserve uncertainty and evidence scope. Do not delete words such as “可能”“仅”“尚未”“在……条件下” when they encode accepted `conditional`, `limit`, or `gap` evidence.
- Do not apply word blacklists mechanically. Terms such as “关键”“复杂”“此外”, technical dashes, structured lists, bold text, and emoji may be correct when the selected style requires them.
- Use first person only for an author-supplied voice or an evidence-bounded editorial synthesis in a style that permits opinion. Never fabricate personal observation to create personality.
- Use the accepted evidence as a reservoir: scientific memo cites at least 5 representative papers, Zhihu 3-12, and Xiaohongshu 3-5. More evidence should deepen synthesis and counterevidence, not inflate every bibliography.
- Never state or imply that the selected article references equal all papers in the field.
- Prefer claim maps over chronological summaries.
- Preserve stance labels: `support`, `limit`, `conditional`, `gap`. Preserve confidence labels: `direct`, `citation-supported`, `inference`.
- Keep author/institution statements conservative; do not infer affiliations from paper-level metadata.
- Use topic cards as compressed context, not as a substitute for paper-level evidence when exact claims matter.
- Topic-card updates are suggestions only unless the user explicitly asks to edit the knowledge base.
- Keep exact deliverable filenames when writing a literature-review bundle:
  - `scientific-memo_keyan.md`
  - `zhihu-explainer_zhihu.md`
  - `xiaohongshu-post_xiaohongshu.md`
- Quick-read cards are bounded by exactly one paper: every claim, number, and judgment must come from that paper's deep-read note or its own full text; citing any other paper disqualifies the card. The card is a pool artifact (`quick-read_sudu.md` in `pool/arxiv-<id>/`), never a bundle deliverable.

## References

- Read [review-contract.md](references/review-contract.md) before drafting or auditing a full review.
- Read [templates.md](references/templates.md) for the briefing-to-writer handoff.
- Load only the selected style guidance for drafting: [scientific-memo.md](references/scientific-memo.md), [zhihu-explainer.md](references/zhihu-explainer.md), [xiaohongshu-post.md](references/xiaohongshu-post.md), [quick-read.md](references/quick-read.md) (single-paper cards only), [slide-deck.md](references/slide-deck.md) (汇报展示 only), plus always [editorial-quality-rubric.md](references/editorial-quality-rubric.md) and [citation-projection.md](references/citation-projection.md).

## Completion standard

Finish only when the evidence gates pass, the editorial audit passes, the run is registered in the
owning KB's `literature-review-catalog.md` with its wiki snapshot rebuilt (run.py finalize does both
— never by hand), and a manual read confirms
that the three outputs sound like three publications for three audiences rather than three views of
one database. The natural-writing pass must improve clarity without changing the evidence surface.

**One-turn rule:** from a validated brief (or a driver-produced `pipeline-summary.json`), run
packet → writing → audit → settle → publish in the same turn. Do not stop to wait for outline
confirmation. The only sanctioned early stop is retrieval failure or insufficient evidence
(coverage/saturation unmet, accepted evidence below the mode floor, deep-read failures that gut the
evidence base): leave the run `in-progress`, tell the user explicitly what is missing, and stop.
