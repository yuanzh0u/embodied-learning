---
name: embodied-ai-literature-hub
description: Discover and recover large embodied-AI literature pools through multi-round Semantic Scholar/arXiv/browser search, candidate registries, coverage and saturation checks, HTML-to-TeX-source-to-text-layer-PDF fallback, extraction-quality gates, and a local public paper pool keyed by unique paper ID. Use for broad or systematic paper discovery, negative-evidence discovery, citation chasing, candidate screening, or when arXiv HTML is unavailable; hand complete readable text to embodied-ai-paper-reader for intellectual reading and evidence creation.
---

# Embodied AI Literature Hub

## Required inputs

- Topic, preferably mapped to one or more knowledge IDs such as `EA-DATA`, `EA-MODEL`, or `EA-EVAL`.
- Time range. In a literature-review run, consume the orchestrator's resolved range; otherwise default to the most recent six months and record it.
- Review mode from the planner: `rapid`, `scoping`, or `systematic`.

## Workflow

1. Load the local knowledge routing layer:
   - `knowledge/index.md`
   - `knowledge/embodied-ai/index.md`
   - relevant topic cards only.
2. Build a search plan with `$embodied-ai-query-planner`:
   - Query planning is owned by `$embodied-ai-query-planner`; this Skill only consumes the generated plan.
   - Use the planner before `search_arxiv.py`, passing topic, knowledge IDs, family hints, time range metadata, and any calibration files.
   - Review `queries`, `search_targets`, `coverage_dimensions`, `stopping_rule`, Browser fallbacks, and notes.
   - The legacy `scripts/build_query_plan.py` path is only a compatibility wrapper that delegates to `../../embodied-ai-query-planner/scripts/build_query_plan.py` relative to the wrapper file.
3. Search in batches and maintain a registry:
   - Default metadata-search backend is `scripts/search_semantic_scholar.py` (Semantic Scholar Graph API): zero-sleep with a 0.1s inter-query interval, disk-cached responses shared with `expand_via_citations.py`, and `--api-key`/`S2_API_KEY` optional. It accepts the same planner `--query-file` and `--start-date/--end-date` contract as `search_arxiv.py` and emits the same JSON shape.
   - Run `scripts/search_arxiv.py --query-file <planner-json>` as the arXiv Atom API pass — kept as a second channel and compatibility backend (3s politeness sleep applies).
   - `--query-file` accepts the planner JSON directly by reading top-level `queries` entries with `label` and `query`.
   - Planner `start_date`/`end_date` fields are scope metadata only; `search_arxiv.py --start-date` and `--end-date` perform the actual arXiv date filtering.
   - Direct `--query` remains available for narrow one-off searches, but literature mining runs should use a planner-generated query file.
   - Keep candidate papers separate from accepted evidence.
   - Use the official API as the first pass, but do not rely on it as the only candidate source.
   - If the API returns `429`, timeouts, SSL errors, or transient server errors, do not treat that as zero evidence. `search_arxiv.py` waits and retries up to 3 times per query, honoring `Retry-After` for `429` when present; after retries are exhausted, use the Browser fallback in `references/browser-fallback.md`.
   - Merge every API round (`--search-result`, `--semantic-scholar-result`), Browser round, and citation round with `scripts/build_candidate_registry.py`; do not maintain ad-hoc paper lists.
   - Update screening status (`discovered`, `title-screened`, `full-text-queued`, `extracted`, `accepted`, `rejected`, `unavailable`) instead of deleting candidates.
   - For registries with hundreds of papers, use `scripts/screen_candidates.py` to create a reproducible title/abstract priority queue. Prior evidence may seed ranking, but the script never marks a paper accepted.
   - Run `scripts/assess_review_coverage.py` after each round. Continue until candidate, full-text, accepted-paper, dimension, and saturation checks all pass. A target count alone never stops the run.
   - Browser/web results remain discovery-only candidates.
   - Keyword search alone under-covers a broad topic's sub-themes. Once a keyword round saturates but coverage still feels thin, run `scripts/expand_via_citations.py` against a handful of `accepted`/`full-text-queued` candidates as seeds to chase citation relationships (Semantic Scholar). It ranks 1-hop neighbors by bibliographic coupling/co-citation against the seed set — not a flat per-seed cap — to avoid citation-graph explosion, merges into the registry via `build_candidate_registry.py --citation-result`, and can emit a `--dynamic-file` for `$embodied-ai-query-planner` so the terms it finds widen the next keyword round. Read `references/citation-expansion.md` before using it.
4. Extract full text through one gateway:
   - Run `scripts/extract_arxiv_content.py`, which tries structured HTML, flat HTML, then text-layer PDF by default. `--preferred-source auto` inserts a markdown tier after HTML (HTML -> markdown -> PDF); `--preferred-source tex` forces the markdown tier first.
   - The markdown tier (`scripts/extract_arxiv_tex.py`) defaults to the **arxiv2md** transport: a public REST API fetched with plain curl (`GET https://arxiv2md.org/api/markdown?url=<id>`, no credentials, 30 req/min per IP) returning section-aware markdown with LaTeX math and pipe tables. Works for papers with arXiv HTML (roughly 2024-03 onward); papers without HTML answer HTTP 400 and the chain falls through. Requires nothing beyond curl.
   - The alternative `s3-tex` transport is **TODO**: `download_arxiv_source.py` fetches the TeX source tarball from `s3://arxiv/` (boto3, threaded, zero-sleep) and `extract_arxiv_tex.py --transport s3-tex` converts the main `.tex` with pypandoc. The bucket is requester-pays — needs AWS credentials (`RequestPayer=requester`), download bandwidth is billed per GB; pending account setup, `--anonymous` answers `AccessDenied`. Old-style IDs (pre-0704) have no S3 key.
   - Markdown-tier extractions are authoritative text: both `arxiv2md` and `tex-pandoc` methods never need visual validation.
   - Use `--ocr-mode never`. Scan-only or unreadable PDFs are outside this project's scope and remain `unavailable`.
   - Use section/paragraph locators for HTML and page locators for PDF. Preserve the extraction method and quality in the reading handoff.
   - Add `--include-full-text` for papers queued for `$embodied-ai-paper-reader`; selected passages alone are not a complete reading input.
   - Keep low-quality or unavailable documents as candidates. Never treat metadata/abstract text as full-text evidence.
   - Cache HTML/PDF outside the repository. Read [full-text-fallback.md](references/full-text-fallback.md) for the exact fallback contract.
   - For queues spanning many papers, use `scripts/extract_content_queue.py --paper-id-file ... --workers 2`. It checkpoints one JSON result per paper, resumes existing results, caps concurrency at four, and enforces a hard per-paper subprocess timeout; it does not create evidence events.
5. Hand complete papers to `$embodied-ai-paper-reader`:
   - The paper reader owns structure mapping, question-driven deep reading, critical appraisal, claim verification, paper notes, and evidence-event projection.
   - `scripts/promote_candidates.py` is a workflow-v2 compatibility path only. Its ranked digest and one-event skeleton do not satisfy the new deep-reading contract and must not create new workflow-v3 evidence.
   - Use `references/evidence-schema.md` only to validate the compatible events projected by the paper reader.

```bash
python3 skills/embodied-ai-literature-hub/scripts/promote_candidates.py \
  --paper-id 2606.03784 --paper-id 2607.00673 \
  --topic "..." --topic-id EA-MODEL \
  --id-prefix EA-XXX-2026 --start-seq 1 \
   --terms reasoning,planning,failure \
  --ocr-mode never \
  --output-skeleton work/<run>/evidence-skeleton.jsonl \
  --output-digest work/<run>/promotion-digest.md
```

For large screened queues, put one arXiv ID per line in a UTF-8 file and use
`--paper-id-file work/<run>/full-text-queue.txt`; the file input is repeatable
and stably deduplicated with any explicit `--paper-id` values.

   - Capture positive, negative, conditional, and gap discussions in the paper note, not in a metadata skeleton.
   - Every accepted paper needs a validated paper note, a passing claim-support audit, and at least one projected event.
   - **Downstream articles may only cite paper-reader-projected events.** A searched, browsed, or merely extracted paper remains a candidate.
   - If a claim's evidence depends on a cited paper, enqueue only that core citation as a candidate paper.
6. Produce outputs:
   - Source-entry draft for `knowledge/sources.md`.
   - Evidence JSONL plus a Markdown brief, using `references/output-templates.md`.
   - Allocate event IDs from the repo root with `python3 scripts/next_event_id.py --prefix <topic-prefix>-<year>` so sequences never collide across runs.
   - Validate the JSONL before settling it: `python skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py --evidence-jsonl <file> --validate-only` must pass.
   - Settle accepted assets into `evidence/literature-review-<topic>-<date>/`: evidence, brief, source draft, query plan, candidate registry, coverage report, and manifest. Full papers and extraction payloads stay in cache/`work/`.
   - Topic-card update suggestions only for high-signal synthesis.
7. Archive extracted papers into the local public paper pool:
   - The pool (default `~/Documents/arxiv/pool`) is a local shared store outside the repository — one folder per paper keyed by unique ID (`arxiv-2403.12550/` or `doi-<urlquoted>/`), holding `paper.md` (converted full text), `extraction.json`, an optional `note.md` reading note, and `meta.json`; `index.jsonl` indexes the pool. Source tarballs and HTML are temp-dir caches and are never archived here.
   - Add a paper after extraction: `python scripts/pool_add_paper.py add --extraction work/<run>/extractions/<id>.json --note work/<run>/paper-notes/<id>.md`. Re-adding is idempotent; `--force` refreshes. `list`, `get <id>`, and `import-existing` (migrate legacy flat `<id>.md`) manage the pool.
   - Topic cards cite pool papers directly instead of per-run duplicates: `- id: POOL-arxiv-2403.12550` + `file: <absolute path to paper.md>` + a semantic-anchor `locator` (same ADR-0002 anchors). `scripts/check_kb_links.py` exempts `POOL-*` entries with a `file:` from `sources.md` registration and validates the file exists.

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
  --review-mode scoping \
  --start-date 2023-01-01 \
  --end-date 2026-06-06 \
  --output /tmp/umi-query-plan.json \
  --markdown-output /tmp/umi-query-plan.md

python skills/embodied-ai-literature-hub/scripts/search_semantic_scholar.py \
  --query-file /tmp/umi-query-plan.json \
  --start-date 2023-01-01 \
  --end-date 2026-06-06 \
  --max-results 25 --batch-label round-1 \
  --output /tmp/umi-s2-candidates.json

python skills/embodied-ai-literature-hub/scripts/search_arxiv.py \
  --query-file /tmp/umi-query-plan.json \
  --start-date 2023-01-01 \
  --end-date 2026-06-06 \
  --max-results 25 --batch-label round-1 \
  --output /tmp/umi-arxiv-candidates.json

python skills/embodied-ai-literature-hub/scripts/parse_browser_candidates.py --input /tmp/browser-arxiv-results.json --start-date 2025-12-06 --end-date 2026-06-06 --output /tmp/browser-candidates.json
python skills/embodied-ai-literature-hub/scripts/build_candidate_registry.py --semantic-scholar-result /tmp/umi-s2-candidates.json --search-result /tmp/umi-arxiv-candidates.json --output work/<run>/candidate-registry.json
python skills/embodied-ai-literature-hub/scripts/assess_review_coverage.py --query-plan /tmp/umi-query-plan.json --candidate-registry work/<run>/candidate-registry.json --output work/<run>/coverage-report.json
python skills/embodied-ai-literature-hub/scripts/extract_arxiv_content.py --paper-id 2402.10329 --terms UMI,data,demonstration,teleoperation --ocr-mode never --include-selected-text --include-full-text --output work/<run>/extractions/2402.10329.json
# Markdown tier (default arxiv2md transport — needs only curl):
python skills/embodied-ai-literature-hub/scripts/extract_arxiv_content.py --paper-id 2402.10329 --terms UMI,data --preferred-source auto --include-full-text --output work/<run>/extractions/2402.10329.json
python skills/embodied-ai-literature-hub/scripts/pool_add_paper.py add --extraction work/<run>/extractions/2402.10329.json
python skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py --evidence-jsonl evidence.jsonl --brief-out brief.md
```

Once a keyword round saturates, chase citation relationships from vetted candidates to find sub-topics the taxonomy missed (see [citation-expansion.md](references/citation-expansion.md)):

```bash
python skills/embodied-ai-literature-hub/scripts/expand_via_citations.py \
  --seed-registry work/<run>/candidate-registry.json --seed-status accepted \
  --output work/<run>/citation-candidates.json \
  --graph-output work/<run>/citation-graph.json \
  --dynamic-output work/<run>/citation-dynamic.json
python skills/embodied-ai-literature-hub/scripts/build_candidate_registry.py \
  --search-result /tmp/umi-arxiv-candidates.json \
  --citation-result work/<run>/citation-candidates.json \
  --output work/<run>/candidate-registry.json
```


Legacy query-plan callers can still use:

```bash
python skills/embodied-ai-literature-hub/scripts/build_query_plan.py --list-topics
```

That command delegates to `$embodied-ai-query-planner` and keeps old `search_arxiv.py --query-file` workflows compatible.

## References

- Read [coverage-and-saturation.md](references/coverage-and-saturation.md) for multi-round registry and stopping logic.
- Read [full-text-fallback.md](references/full-text-fallback.md) whenever HTML is missing or extraction quality is not high.
- Read [evidence-schema.md](references/evidence-schema.md) before creating or validating events.
- Read [browser-fallback.md](references/browser-fallback.md) after API failure or query under-recovery.
- Read [citation-expansion.md](references/citation-expansion.md) before running `expand_via_citations.py` to widen discovery beyond keyword search.
