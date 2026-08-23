---
name: embodied-ai-literature-review
description: Orchestrate coverage-driven embodied-AI literature reviews from review-mode selection and large candidate registries through complete HTML/PDF recovery, paper-level deep reading and claim verification, saturation auditing, validated briefs, audience-specific writing, and settled runs. Use for researching, auditing, or producing evidence-grounded scientific memos, Zhihu explainers, and Xiaohongshu posts.
---

# Embodied AI Literature Review

## Overview

Turn an embodied-AI question into validated writing inputs. The current migration path is `review mode -> planner -> candidate registry -> coverage/saturation -> HTML/PDF recovery -> $embodied-ai-paper-reader -> review packet -> writing brief -> $embodied-ai-review-writer`. Existing workflow-v2 runs remain readable; new evidence should use the paper-reading extension before workflow-v3 becomes mandatory.

Default final deliverable: three Markdown files under a new `work/literature-review-<topic>-<date>/` project folder:
- `scientific-memo_keyan.md`: 科研文献综述/研究备忘录风格。
- `zhihu-explainer_zhihu.md`: 知乎科普帖/专家解释帖风格。
- `xiaohongshu-post_xiaohongshu.md`: 小红书网文/KOL 洞察帖风格。

**Division of labor:** `build_review_packet.py` is a briefing generator, not an author. It emits `review-packet.md` + `writing-brief.md` + `evidence-appendix.md`; `$embodied-ai-review-writer` writes and editorially audits the three reader-facing files. Never present mechanical renders (`*.scaffold.md`) as finished articles.

Use `--style scientific-memo`, `--style expert-explainer`, or `--style kol-thread` only when the user asks for a single style. Use `survey` explicitly when the user wants the intermediate review packet, source tiers, and style menu instead of the final prose artifacts.

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

## Workflow

0. **Decide the deliverable shape (before any writing).** Default is the full three-style bundle. A single style is allowed ONLY when the user explicitly asks for it — record that decision in `run.json` as `"style": "<formal-style>"` plus `"scope_note": "<the user's ask, in their words>"`. The ONLY recognized deliverable filenames are `scientific-memo_keyan.md` / `zhihu-explainer_zhihu.md` / `xiaohongshu-post_xiaohongshu.md` — an invented filename (research-memo.md, main-*.md, …) is not a deliverable, whatever its quality. Non-review artifacts (research outlines, experiment designs, synthesis notes) must NOT use a `literature-review-<topic>-<date>` folder name — that name IS the bundle contract trigger; use e.g. `work/research-outline-<topic>-<date>/` instead.
1. Initialize the run, then load the repository routing layer:
   - `python3 scripts/init_run.py --topic "..." --knowledge-id EA-… --time-range "..." --review-mode scoping` creates a workflow-v2 run with `status: in-progress`.
   - **If you stop for any reason before settling** (search failed, evidence insufficient, out of time), leave the run `in-progress` in `work/` and TELL THE USER explicitly that the run is unfinished, listing the missing steps. A silently abandoned run that looks like a deliverable is a contract violation; an honestly declared partial run is fine.
   - `knowledge/index.md`
   - `knowledge/embodied-ai/index.md`
   - only the relevant topic cards.
2. Build and widen the candidate pool:
   - Generate a mode-aware query plan with `$embodied-ai-query-planner`.
   - Search in multiple API/Browser batches; merge them with the Hub's `build_candidate_registry.py`.
   - Screen titles/abstracts for priority only. Candidate count is not evidence count.
   - Run `assess_review_coverage.py` after every batch. Continue until all floors, all dimensions, and consecutive saturation rounds pass.
3. Recover, read, and verify full text:
   - Use the Hub's unified `extract_arxiv_content.py`: HTML -> text-layer PDF, with `--ocr-mode never --include-full-text`.
   - Keep scan-only or otherwise unrecoverable papers in the registry as `unavailable` rather than silently dropping them.
   - Pass complete extraction payloads to `$embodied-ai-paper-reader`; ranked passages are navigation hints, not reading evidence.
   - Require a validated paper note and passing claim-support audit before projecting evidence events.
   - Inspect evidence JSONL and briefs from `$embodied-ai-literature-hub`.
   - Inspect `knowledge/sources.md` for stable source IDs.
   - Use candidate lists only for search coverage, not accepted claims.
   - Use fallback source-tier JSON only as review-packet context, not Hub evidence JSONL.
   - **Articles cite verified evidence only.** If the synthesis needs a candidate paper, recover its complete text, read it with `$embodied-ai-paper-reader`, audit it, and project its events before writing.
4. Generate the briefing bundle. Pass the coverage report; the script writes `review-packet.md` + `writing-brief.md` + `evidence-appendix.md` as writing inputs:

```bash
python skills/embodied-ai-literature-review/scripts/build_review_packet.py \
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
python skills/embodied-ai-literature-review/scripts/build_review_packet.py \
  --topic "感知误差溯源" \
  --knowledge-id EA-DATA --knowledge-id EA-SENSOR \
  --evidence-jsonl evidence/literature-review-<prior-run-a>/evidence.jsonl \
  --evidence-jsonl evidence/literature-review-<prior-run-b>/evidence.jsonl \
  --select-events-file /tmp/selected-ids.txt \
  --consolidate-evidence
```

`--select-event`/`--select-events-file` filter to named event IDs (unknown IDs error out); `--consolidate-evidence` writes the working set as the run's local `evidence.jsonl`, so the folder is self-contained. Always pass `--consolidate-evidence` when reusing prior evidence.

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

5. **Hand the validated brief to `$embodied-ai-review-writer` (mandatory for prose deliverables).**
   - Pass `writing-brief.md`, `evidence-appendix.md`, every accepted evidence JSONL, and the requested style(s).
   - Let the writer load its style-specific references and draft each article independently for its audience.
   - Save the exact deliverable filenames in the same run folder.
   - Generate `trace-map.json`, then run the writer's `audit_article_quality.py`. A traceable scaffold is not an article.
6. Audit traceability and editorial quality:
   - Every substantive claim has an evidence event, topic-card source, or `inference` marker.
   - Candidate-only papers are not cited as established evidence.
   - Exact quotes come only from opened raw sources and stay short.
   - Reader-facing body links point to accepted papers; event-level provenance lives in `trace-map.json` and `evidence-appendix.md`.
   - The scientific, Zhihu, and Xiaohongshu drafts pass the writer Skill's language, template-leakage, citation-density, length, and overlap gates.
7. Settle the run:
   - Validate the evidence JSONL: `python3 skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py --evidence-jsonl <file> --validate-only`.
   - Flip `run.json` `status` from `in-progress` to `settled`.
   - Sink the bundle with one idempotent command: `python3 scripts/sink_run.py <run-dir>` — it re-runs the bundle audit, copies accepted assets into `evidence/literature-review-<topic>-<date>/` (every used evidence JSONL, final articles, appendix, source draft, query plan, candidate registry, coverage report; full texts/extraction payloads stay in cache/`work/`), stamps a `sink_checklist` into run.json, and prints a ready-to-paste catalog row. Gate-failed runs require `--allow-gate-fail` and their catalog row must go to the dedicated gate-failed section, never the main table.
   - After sinking, run `python3 scripts/check_sink_integrity.py` (work/ ↔ evidence/ ↔ catalog reconciliation) and add the printed catalog row if it reports the run as unregistered.
   - Cross-run evidence is supported but must be recorded: `run.json` lists `source_runs` (the prior runs whose evidence was combined) and `event_count` equals the deduplicated count actually available to the articles. Never cite an event that is not in the settled evidence set.
   - Audit before settling — all gates must pass:
     - `python3 scripts/check_run_bundle.py <run-dir>` (bundle completeness: three styles or a declared `style`+`scope_note`, self-contained evidence, standard run.json schema).
     - `python3 scripts/audit_citations.py --article <each article> --appendix <appendix> --evidence-jsonl <each evidence file> --run-json <run.json>` (no dead anchors, no citations outside the loaded evidence).
     - `python3 skills/embodied-ai-review-writer/scripts/audit_article_quality.py --bundle-dir <run-dir>` (reader-facing editorial quality and cross-style differentiation).
   - `check_run_bundle.py` enforces the v2 coverage artifacts and refuses settlement while `ready_to_stop=false`.

For a legacy multi-run paper-reader upgrade, keep every old settled run immutable. Build and audit the replacement under `work/`, then publish it under a new suffixed directory such as `literature-review-<topic>-<date>-reader-v1`. The replacement run must include `paper-notes/`, `claim-support-audits/`, `reading-ledger.jsonl`, `reading-summary.json`, their indexes, regenerated evidence/brief/appendix/trace map, and all three audited articles. Only switch it to `settled` after all reading, citation, editorial, and bundle gates pass.

## Review rules

- Prefer claim maps over chronological summaries.
- Preserve stance labels: `support`, `limit`, `conditional`, `gap`.
- Preserve confidence labels: `direct`, `citation-supported`, `inference`.
- Keep author/institution statements conservative; do not infer affiliations from paper-level metadata.
- Use topic cards as compressed context, not as a substitute for paper-level evidence when exact claims matter.
- Topic-card updates are suggestions only unless the user explicitly asks to edit the knowledge base.

## References

- Read [review-contract.md](references/review-contract.md) before drafting or auditing a full review.
- Read [templates.md](references/templates.md) for the briefing-to-writer handoff. Reader-facing style rules belong to `$embodied-ai-review-writer`.
