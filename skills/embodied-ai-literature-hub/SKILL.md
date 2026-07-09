---
name: embodied-ai-literature-hub
description: Mine arXiv literature for embodied AI topics, expanding adjacent paper searches and extracting claim/evidence/stance/author records. Use when the user asks for embodied AI literature aggregation, arXiv paper mining, UMI/data/VLA/simulation/evaluation paper discovery, negative discussion mining, citation chasing, or author viewpoint tracking.
---

# Embodied AI Literature Hub

## Required inputs

- Topic, preferably mapped to one or more knowledge IDs such as `EA-DATA`, `EA-MODEL`, or `EA-EVAL`.
- Time range. If absent, ask for it before searching; do not silently default.

## Workflow

1. Load the local knowledge routing layer:
   - `knowledge/index.md`
   - `knowledge/embodied-ai/index.md`
   - relevant topic cards only.
2. Build a search plan with `$embodied-ai-query-planner`:
   - Query planning is owned by `$embodied-ai-query-planner`; this Skill only consumes the generated plan.
   - Use the planner before `search_arxiv.py`, passing topic, knowledge IDs, family hints, time range metadata, and any calibration files.
   - Review the planner's `queries`, `browser_fallback_queries`, `minimum_candidate_count`, and notes before searching.
   - The legacy `scripts/build_query_plan.py` path is only a compatibility wrapper that delegates to `../../embodied-ai-query-planner/scripts/build_query_plan.py` relative to the wrapper file.
3. Search arXiv:
   - Run `scripts/search_arxiv.py --query-file <planner-json>` with an explicit date range.
   - `--query-file` accepts the planner JSON directly by reading top-level `queries` entries with `label` and `query`.
   - Planner `start_date`/`end_date` fields are scope metadata only; `search_arxiv.py --start-date` and `--end-date` perform the actual arXiv date filtering.
   - Direct `--query` remains available for narrow one-off searches, but literature mining runs should use a planner-generated query file.
   - Keep candidate papers separate from accepted evidence.
   - Use the official API as the first pass, but do not rely on it as the only candidate source.
   - If the API returns `429`, timeouts, SSL errors, or transient server errors, do not treat that as zero evidence. `search_arxiv.py` waits and retries up to 3 times per query, honoring `Retry-After` for `429` when present; after retries are exhausted, use the Browser fallback in `references/browser-fallback.md`.
   - If the API succeeds but returns fewer than the topic-family minimum candidate count, use the Browser fallback to widen candidate discovery before judging scarcity.
   - Browser/web results are candidate-discovery evidence only. Promote claims only after arXiv HTML正文 verification.
4. Mine HTML full text:
   - Prefer arXiv HTML full text. Run `scripts/extract_arxiv_html.py` first for promising candidates.
   - The extractor is section-aware for LaTeXML pages: read `ranked_sections` to decide which sections to deep-read (pass `--include-section-text` for their full text), use `term_matches` locators (`section path ¶ paragraph id`) as evidence locators, and use `citation_contexts` to capture how the paper discusses its cited works — the primary source for "paper A evaluates dataset B" style evidence.
   - Non-LaTeXML pages degrade to flat extraction (`structure: "flat"`); locators fall back to nearest headings.
   - If HTML is unavailable, keep the paper as a metadata candidate and do not perform正文挖掘 or promote it to正文-level evidence.
   - Cache HTML outside the repo; do not store full papers or full extracted text in the knowledge base.
   - If HTML download stalls, stop the run and continue with metadata/abstract-level evidence only, clearly marking the confidence and limitation.
5. Extract discussion events:
   - Use `references/evidence-schema.md`.
   - **Preferred path — `scripts/promote_candidates.py`**: one command per batch of confirmed-relevant candidates pulls API metadata + section-aware extraction, and emits a reading digest plus an evidence skeleton JSONL (event IDs, paper metadata, authors, locator prefilled; `claim`/`stance`/`evidence.summary` left as TODO). Fill the TODO fields from the digest, then validate. The validator rejects unfilled skeletons, so promotion cannot be silently skipped:

```bash
python3 skills/embodied-ai-literature-hub/scripts/promote_candidates.py \
  --paper-id 2606.03784 --paper-id 2607.00673 \
  --topic "..." --topic-id EA-MODEL \
  --id-prefix EA-XXX-2026 --start-seq 1 \
  --terms reasoning,planning,failure \
  --output-skeleton work/<run>/evidence-skeleton.jsonl \
  --output-digest work/<run>/promotion-digest.md
```

   - Capture positive, negative, conditional, and gap discussions.
   - Every accepted paper needs at least one topic-relevant claim with locator evidence.
   - **Downstream articles may only cite promoted events.** A candidate that was searched or browsed but never promoted cannot appear in a review; promotion is not optional effort, it is the boundary between candidate and evidence.
   - If a claim's evidence depends on a cited paper, enqueue only that core citation as a candidate paper.
6. Produce outputs:
   - Source-entry draft for `knowledge/sources.md`.
   - Evidence JSONL plus a Markdown brief, using `references/output-templates.md`.
   - Allocate event IDs from the repo root with `python3 scripts/next_event_id.py --prefix <topic-prefix>-<year>` so sequences never collide across runs.
   - Validate the JSONL before settling it: `python skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py --evidence-jsonl <file> --validate-only` must pass.
   - Settle accepted assets into `evidence/literature-review-<topic>-<date>/` (evidence JSONL, brief, source-entry draft, query plan, `run.json` manifest — see `evidence/README.md`). Candidates, HTML extraction JSON, and other intermediates stay in `work/`.
   - Topic-card update suggestions only for high-signal synthesis.

## Evidence rules

- Stance labels: `support`, `limit`, `conditional`, `gap`.
- Confidence labels: `direct`, `citation-supported`, `inference`.
- Author identity is conservative: normalize names, but do not merge same-name authors unless the paper gives stronger evidence such as ORCID, homepage, or clear affiliation continuity.
- Author institution tracking is author-level and first-level only: record the top organization such as `北京大学`, `Google`, `Stanford University`, or `MIT`; omit departments, labs, teams, and centers. If author-to-institution mapping is unreliable, leave `institutions: []`.
- Use short quotes only when useful; prefer precise paraphrase plus page/section locator.

## Script quick start

From the repository root, prefer the planner Skill path:

```bash
python skills/embodied-ai-query-planner/scripts/build_query_plan.py \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --family umi \
  --start-date 2023-01-01 \
  --end-date 2026-06-06 \
  --output /tmp/umi-query-plan.json \
  --markdown-output /tmp/umi-query-plan.md

python skills/embodied-ai-literature-hub/scripts/search_arxiv.py \
  --query-file /tmp/umi-query-plan.json \
  --start-date 2023-01-01 \
  --end-date 2026-06-06 \
  --max-results 5 \
  --output /tmp/umi-arxiv-candidates.json

python skills/embodied-ai-literature-hub/scripts/parse_browser_candidates.py --input /tmp/browser-arxiv-results.json --start-date 2025-12-06 --end-date 2026-06-06 --output /tmp/browser-candidates.json
python skills/embodied-ai-literature-hub/scripts/extract_arxiv_html.py --paper-id 2402.10329 --terms UMI,data,demonstration,teleoperation
python skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py --evidence-jsonl evidence.jsonl --brief-out brief.md
```

Legacy query-plan callers can still use:

```bash
python skills/embodied-ai-literature-hub/scripts/build_query_plan.py --list-topics
```

That command delegates to `$embodied-ai-query-planner` and keeps old `search_arxiv.py --query-file` workflows compatible.
