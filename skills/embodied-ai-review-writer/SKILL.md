---
name: embodied-ai-review-writer
description: Orchestrate coverage-driven embodied-AI literature reviews end to end and write or rewrite publication-ready, natural Chinese content from a formal-ready brief and a potentially large evidence reservoir. Owns review-mode selection, candidate registries, saturation auditing, validated briefs, settled runs; use for researching, auditing, or producing evidence-grounded scientific research memos, 知乎专家解释稿, 小红书洞察帖, full three-style bundles, or when articles are traceable but shallow, packet-like, repetitive, formulaic, under-cited, or not audience-specific.
---

# Embodied AI Review Writer

## Purpose

Turn an embodied-AI question into validated writing inputs and then into genuinely different reader-facing articles. This Skill owns the review **end to end**: it orchestrates `$embodied-ai-literature-hub` (query planning, search, candidate registries, coverage/saturation, full-text recovery) and `$embodied-ai-paper-reader` (deep reading, claim verification, evidence projection), then writes and editorially audits the deliverables. It never presents candidates as evidence and never bypasses the projection gates.

The current migration path is `review mode -> planner -> candidate registry -> coverage/saturation -> HTML/PDF recovery -> $embodied-ai-paper-reader -> review packet -> writing brief -> $embodied-ai-review-writer`. Existing workflow-v2 runs remain readable; new evidence should use the paper-reading extension before workflow-v3 becomes mandatory.

Default final deliverable: three Markdown files under a new `work/literature-review-<topic>-<date>/` project folder:
- `scientific-memo_keyan.md`: 科研文献综述/研究备忘录风格。
- `zhihu-explainer_zhihu.md`: 知乎科普帖/专家解释帖风格。
- `xiaohongshu-post_xiaohongshu.md`: 小红书网文/KOL 洞察帖风格。

A fourth style exists outside the review bundle: `quick-read_sudu.md`（速读卡，see [quick-read.md](references/quick-read.md)）is a **single-paper pool artifact**, not a literature-review deliverable. Its inputs are one paper's deep-read `note.json` + `paper.md` from the public pool — never a writing brief — and it is generated per paper by `scripts/quick_read_paper.py`; it never appears inside a `literature-review-<topic>-<date>/` folder.

**Division of labor:** `build_review_packet.py` is a briefing generator, not an author. It emits `review-packet.md` + `writing-brief.md` + `evidence-appendix.md`; the writing stage writes and editorially audits the three reader-facing files. Never present mechanical renders (`*.scaffold.md`) as finished articles.

## Required inputs

- Topic or review question.
- Time range when discovering papers or invoking upstream literature mining. If no time range is provided, default to the most recent six months.
- Review mode: `rapid`, `scoping` (default), or `systematic`. Treat every size target as a floor, never as a cap.
- Target style: optional. If absent, write all three default Markdown outputs. Use `scientific-memo`, `expert-explainer`, or `kol-thread` for one formal style output, and `survey` for the explicit review packet/style menu.
- At least one of:
  - evidence JSONL from `$embodied-ai-literature-hub`
  - fallback source-tier JSON from lightweight Browser/web collection
  - relevant `knowledge/embodied-ai/*.md` topic cards
  - a user-provided draft with citations to audit

New formal outputs require both the mode's accepted-paper floor (`rapid` 8, `scoping` 15, `systematic` 30) and a passed coverage/saturation report. A high paper count without negative, evaluation, deployment, or adjacent coverage remains preliminary.

If no validated brief exists, produce one with the run lifecycle and briefing workflow below — candidate lists and raw search results are not writing evidence.
If the brief says `Writing readiness: preliminary` or its coverage gate is blocked, return it to research instead of writing formal articles.

## Run lifecycle and gates

0. **Decide the deliverable shape (before any writing).** Default is the full three-style bundle. A single style is allowed ONLY when the user explicitly asks for it — record that decision in `run.json` as `"style": "<formal-style>"` plus `"scope_note": "<the user's ask, in their words>"`. The ONLY recognized deliverable filenames are `scientific-memo_keyan.md` / `zhihu-explainer_zhihu.md` / `xiaohongshu-post_xiaohongshu.md` — an invented filename (research-memo.md, main-*.md, …) is not a deliverable, whatever its quality. Non-review artifacts (research outlines, experiment designs, synthesis notes) must NOT use a `literature-review-<topic>-<date>` folder name — that name IS the bundle contract trigger; use e.g. `work/research-outline-<topic>-<date>/` instead.
1. Initialize the run, then load the repository routing layer:
   - `python3 scripts/init_run.py --topic "..." --knowledge-id EA-… --time-range "..." --review-mode scoping` creates a workflow-v2 run with `status: in-progress`.
   - **If you stop for any reason before settling** (search failed, evidence insufficient, out of time), leave the run `in-progress` in `work/` and TELL THE USER explicitly that the run is unfinished, listing the missing steps. A silently abandoned run that looks like a deliverable is a contract violation; an honestly declared partial run is fine.
   - `knowledge/index.md`, `knowledge/embodied-ai/index.md`, and only the relevant topic cards.
2. Build and widen the candidate pool (via `$embodied-ai-literature-hub`):
   - Generate a mode-aware query plan with the Hub's in-skill planning step (`search.py build-query-plan`).
   - Search in multiple API/Browser batches; merge them with `search.py build-candidate-registry`.
   - Screen titles/abstracts for priority only. Candidate count is not evidence count.
   - Run `search.py assess-review-coverage` after every batch. Continue until all floors, all dimensions, and consecutive saturation rounds pass.
3. Recover, read, and verify full text:
   - Use the Hub's unified `extract_arxiv_content.py`: HTML -> text-layer PDF, with `--ocr-mode never --include-full-text`.
   - Keep scan-only or otherwise unrecoverable papers in the registry as `unavailable` rather than silently dropping them.
   - Pass complete extraction payloads to `$embodied-ai-paper-reader`; ranked passages are navigation hints, not reading evidence.
   - Require a validated paper note and passing claim-support audit before projecting evidence events.
   - Inspect evidence JSONL and briefs from `$embodied-ai-literature-hub`; inspect `knowledge/sources.md` for stable source IDs.
   - Use candidate lists only for search coverage, not accepted claims; use fallback source-tier JSON only as review-packet context, not Hub evidence JSONL.
   - **Articles cite verified evidence only.** If the synthesis needs a candidate paper, recover its complete text, read it with `$embodied-ai-paper-reader`, audit it, and project its events before writing.
7. Settle the run:
   - Validate the evidence JSONL: `python3 skills/embodied-ai-literature-hub/scripts/parse.py write-lit-outputs --evidence-jsonl <file> --validate-only`.
   - Flip `run.json` `status` from `in-progress` to `settled`.
   - Copy accepted assets into `evidence/literature-review-<topic>-<date>/`: every used evidence JSONL, final articles, appendix, source draft, query plan, candidate registry, and coverage report. Full texts/extraction payloads stay in cache/`work/`.
   - Cross-run evidence is supported but must be recorded: `run.json` lists `source_runs` (the prior runs whose evidence was combined) and `event_count` equals the deduplicated count actually available to the articles. Never cite an event that is not in the settled evidence set.
   - Audit before settling — all gates must pass:
     - `python3 scripts/check_run_bundle.py <run-dir>` (bundle completeness: three styles or a declared `style`+`scope_note`, self-contained evidence, standard run.json schema).
     - `python3 scripts/audit_citations.py --article <each article> --appendix <appendix> --evidence-jsonl <each evidence file> --run-json <run.json>` (no dead anchors, no citations outside the loaded evidence).
     - `python3 skills/embodied-ai-review-writer/scripts/writing_audit.py audit-article-quality --bundle-dir <run-dir>` (reader-facing editorial quality and cross-style differentiation).
   - `check_run_bundle.py` enforces the v2 coverage artifacts and refuses settlement while `ready_to_stop=false`.

For a legacy multi-run paper-reader upgrade, keep every old settled run immutable. Build and audit the replacement under `work/`, then publish it under a new suffixed directory such as `literature-review-<topic>-<date>-reader-v1`. The replacement run must include `paper-notes/`, `claim-support-audits/`, `reading-ledger.jsonl`, `reading-summary.json`, their indexes, regenerated evidence/brief/appendix/trace map, and all three audited articles. Only switch it to `settled` after all reading, citation, editorial, and bundle gates pass.

## Briefing generation

Generate the briefing bundle with the coverage report attached; the script writes `review-packet.md` + `writing-brief.md` + `evidence-appendix.md` as validated writing inputs:

```bash
python skills/embodied-ai-review-writer/scripts/build_review_packet.py \
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
python skills/embodied-ai-review-writer/scripts/build_review_packet.py \
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
python skills/embodied-ai-review-writer/scripts/build_review_packet.py \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --evidence-jsonl /tmp/umi-evidence.jsonl \
  --style survey
```

Fallback packet input, which still degrades to a preliminary packet until paper-level evidence is sufficient. Omit `--time-range` to use the most recent six months; pass an explicit range only when the user asks:

```bash
python skills/embodied-ai-review-writer/scripts/build_review_packet.py \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --fallback-source-json /tmp/fallback-sources.json
```

Use `--output -` only when the user explicitly wants inline Markdown or stdout for another tool.

Then hand the validated brief to the writing workflow below (mandatory for prose deliverables): pass `writing-brief.md`, `evidence-appendix.md`, every accepted evidence JSONL, and the requested style(s); save the exact deliverable filenames in the same run folder; generate `trace-map.json`, then run `writing_audit.py audit-article-quality`. A traceable scaffold is not an article.

## Load only the selected style guidance

- Scientific research memo: read [scientific-memo.md](references/scientific-memo.md).
- Zhihu expert explainer: read [zhihu-explainer.md](references/zhihu-explainer.md).
- Xiaohongshu insight post: read [xiaohongshu-post.md](references/xiaohongshu-post.md).
- Quick-read card (single paper): read [quick-read.md](references/quick-read.md).
- Always read [editorial-quality-rubric.md](references/editorial-quality-rubric.md) and [citation-projection.md](references/citation-projection.md).

For a full bundle, read all three style references, but plan and draft each article independently from the brief. Never derive Zhihu or Xiaohongshu prose by shortening the scientific memo.

## Writing workflow

With a validated brief in hand (from the briefing step above or supplied by the caller), draft the reader-facing articles:

1. **Interrogate the evidence reservoir.** Extract one central thesis, 3-5 claim clusters, the strongest counterevidence, mandatory caveats, and the evidence boundary. Separate field size, discovered candidates, extracted full text, accepted papers, and papers selected for each article.
2. **Write a reader contract and independent editorial plan for each style.** Name the intended reader, their live question, the one-sentence takeaway, the decision consequence, one evidence-backed running example, the core terms that need explanation, the representative source subset, excluded details, and the ending. Do not reuse an outline or simply cite every accepted paper.
3. **Draft complete explanation units.** Move from concrete phenomenon to mechanism, representative evidence, reader consequence, and boundary. Write in natural Chinese. Translate and synthesize English evidence claims; never paste or mechanically translate event claims one by one. Use paper links in body prose where the selected style permits them.
4. **Project provenance.** Keep reader-facing citations compact and put event-level mapping in `trace-map.json` plus `evidence-appendix.md`. Follow [citation-projection.md](references/citation-projection.md).
5. **Edit the argument.** Check the thesis, counterevidence, causal order, and overclaiming before polishing individual sentences.
6. **Run an evidence-locked natural-writing pass.** Freeze every factual claim, paper link, number, date, named entity, quote, uncertainty marker, and boundary condition. Then remove chatbot residue, empty promotion, vague attribution, redundant signposting, synonym cycling, generic conclusions, and monotonous sentence rhythm. Do not add specificity, personal experience, or confidence to make the prose sound more human. Common technical words and punctuation are not faults by themselves; change them only when the surrounding sentence is weak. The selected platform guide outranks generic style heuristics.
7. **Inspect the publication surface.** Reject unresolved citation anchors, missing subjects, malformed punctuation, internal reasoning labels, unannotated reading lists, and reference dumps. Check whether a non-specialist can restate the thesis without the paper names or acronyms.
8. **Run deterministic gates.** Build the trace map, then audit the three outputs:

```bash
python3 skills/embodied-ai-review-writer/scripts/writing_audit.py build-trace-map \
  --evidence-jsonl <run>/evidence.jsonl \
  --article <run>/scientific-memo_keyan.md \
  --article <run>/zhihu-explainer_zhihu.md \
  --article <run>/xiaohongshu-post_xiaohongshu.md \
  --output <run>/trace-map.json

python3 skills/embodied-ai-review-writer/scripts/writing_audit.py audit-article-quality \
  --memo <run>/scientific-memo_keyan.md \
  --zhihu <run>/zhihu-explainer_zhihu.md \
  --xiaohongshu <run>/xiaohongshu-post_xiaohongshu.md
```

For a published Zhihu collection, also audit corpus-level repetition, template concentration, and accessibility distributions:

```bash
python3 skills/embodied-ai-review-writer/scripts/writing_audit.py audit-zhihu-corpus \
  --topics-dir wiki/data/topics \
  --project-root .
```

9. **Settle with the full evidence gates.** Run the settlement workflow in "Run lifecycle and gates" above: `scripts/audit_citations.py` and `scripts/check_run_bundle.py` before status flip. Editorial gates complement evidence gates; neither substitutes for the other.

## Hard rules

- Treat the brief, claim map, stance buckets, and evidence appendix as inputs, never as article body.
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
- Load only the selected style guidance for drafting: [scientific-memo.md](references/scientific-memo.md), [zhihu-explainer.md](references/zhihu-explainer.md), [xiaohongshu-post.md](references/xiaohongshu-post.md), [quick-read.md](references/quick-read.md) (single-paper cards only), plus always [editorial-quality-rubric.md](references/editorial-quality-rubric.md) and [citation-projection.md](references/citation-projection.md).

## Completion standard

Finish only when the evidence gates pass, the editorial audit passes, and a manual read confirms that the three outputs sound like three publications for three audiences rather than three views of one database. The natural-writing pass must improve clarity without changing the evidence surface.
