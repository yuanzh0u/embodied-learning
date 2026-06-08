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
2. Build a search plan:
   - Use wide recall plus strong filtering.
   - Read `references/topic-expansion.md` for static adjacent queries.
   - Add dynamic query variants only when you can explain why they may expose topic-related discussion.
   - For UMI-like named methods, do not stop at exact keyword matches. Build a tiered plan that includes named variants, derived systems, author follow-ups, method-adjacent papers, and explicit limitation/usability papers.
   - If fewer than 12 candidate papers are found for a named method family, expand the search before concluding scarcity unless the run is blocked by API/network limits.
3. Search arXiv:
   - Run `scripts/search_arxiv.py` with explicit date range and one or more query strings.
   - Keep candidate papers separate from accepted evidence.
   - Use the official API as the first pass, but do not rely on it as the only candidate source.
   - If the API returns `429`, timeouts, SSL errors, or query-level errors, do not treat that as zero evidence. Back off, retry sparingly, then use the Browser fallback in `references/browser-fallback.md`.
   - If the API succeeds but returns fewer than the topic-family minimum candidate count, use the Browser fallback to widen candidate discovery before judging scarcity.
   - Browser/web results are candidate-discovery evidence only. Promote claims only after arXiv HTML正文 verification.
4. Mine HTML full text:
   - Prefer arXiv HTML full text. Run `scripts/extract_arxiv_html.py` first for promising candidates.
   - If HTML is unavailable, keep the paper as a metadata candidate and do not perform正文挖掘 or promote it to正文-level evidence.
   - Cache HTML outside the repo; do not store full papers or full extracted text in the knowledge base.
   - If HTML download stalls, stop the run and continue with metadata/abstract-level evidence only, clearly marking the confidence and limitation.
5. Extract discussion events:
   - Use `references/evidence-schema.md`.
   - Capture positive, negative, conditional, and gap discussions.
   - Every accepted paper needs at least one topic-relevant claim with locator evidence.
   - If a claim's evidence depends on a cited paper, enqueue only that core citation as a candidate paper.
6. Produce outputs:
   - Source-entry draft for `knowledge/sources.md`.
   - Evidence JSONL plus a Markdown brief, using `references/output-templates.md`.
   - Topic-card update suggestions only for high-signal synthesis.

## Evidence rules

- Stance labels: `support`, `limit`, `conditional`, `gap`.
- Confidence labels: `direct`, `citation-supported`, `inference`.
- Author identity is conservative: normalize names, but do not merge same-name authors unless the paper gives stronger evidence such as ORCID, homepage, or clear affiliation continuity.
- Use short quotes only when useful; prefer precise paraphrase plus page/section locator.

## Script quick start

```bash
python scripts/search_arxiv.py --query 'all:"Universal Manipulation Interface" AND all:data' --start-date 2023-01-01 --end-date 2026-06-06 --max-results 5
python scripts/build_query_plan.py --topic umi-data-usability --output /tmp/umi-query-plan.json
python scripts/parse_browser_candidates.py --input /tmp/browser-arxiv-results.json --start-date 2025-12-06 --end-date 2026-06-06 --output /tmp/browser-candidates.json
python scripts/extract_arxiv_html.py --paper-id 2402.10329 --terms UMI,data,demonstration,teleoperation
python scripts/write_lit_outputs.py --evidence-jsonl evidence.jsonl --brief-out brief.md
```
