---
name: embodied-ai-literature-hub
description: Discover and recover large embodied-AI literature pools through scale-aware query planning, multi-round Semantic Scholar/arXiv/browser search, candidate registries, influence and problem-relevance triage rankings, coverage and saturation checks, HTML-to-TeX-source-to-text-layer-PDF fallback, extraction-quality gates, and a local public paper pool keyed by unique paper ID. Use for broad or systematic paper discovery, query planning and topic expansion, negative-evidence discovery, citation chasing, candidate screening, or when arXiv HTML is unavailable; hand complete readable text to embodied-ai-paper-reader for intellectual reading and evidence creation.
---

# Embodied AI Literature Hub

## Required inputs

- Topic, preferably mapped to one or more knowledge IDs such as `EA-DATA`, `EA-MODEL`, or `EA-EVAL`.
- Time range. In a literature-review run, consume the orchestrator's resolved range; otherwise default to the most recent six months and record it.
- Review mode from the planning step: `rapid`, `scoping`, or `systematic`.

## Workflow

1. Load the local knowledge routing layer:
   - `knowledge/index.md`
   - `knowledge/embodied-ai/index.md`
   - relevant topic cards only.
2. Plan the queries (in-Skill planning step, `scripts/search.py build-query-plan`):
   - Inputs: topic; optional `knowledge_id` (`EA-DATA`, `EA-MODEL`, ...); optional specialized family (`umi`, `vla`, `sim2real`, `retargeting`, `tactile-force`, `last-centimeter`); time range (recorded as scope metadata only — the actual date filtering is `--start-date/--end-date` on the search scripts); review mode `rapid`/`scoping`/`systematic`; explicit candidate/full-text/accepted-evidence floors (never caps); optional `--dynamic-file` suggestions and `--calibration-file` notes.
   - If the topic needs associative expansion beyond the static taxonomy, create a dynamic suggestion file (see [dynamic-expansion.md](references/dynamic-expansion.md)). For fresh calibration, search arXiv pages, project pages, author pages, Reddit, and X/Twitter for current terms — save only terms/query hints, not claims (see [web-calibration.md](references/web-calibration.md)) — then re-run with `--dynamic-file` and/or `--calibration-file`.
   - Review `queries`, `search_targets`, `coverage_dimensions`, `stopping_rule`, Browser fallbacks, and notes.
   - Topic taxonomy details: [topic-taxonomy.md](references/topic-taxonomy.md).

## Query plan contract

- `queries`: arXiv API-compatible query entries, read by `search.py search-arxiv --query-file` (top-level `queries` only). Each entry carries `label`, `tier`, `query`, and `why`.
- `browser_fallback_queries`: web/browser search strings for candidate discovery when the API under-recovers.
- `web_calibration_queries`: search strings for fresh keyword calibration.
- `dynamic_suggestions`: LLM/agent-suggested query additions and adjacent families, separate from static taxonomy.
- `calibration_notes`: source and confidence notes, especially for social calibration.
- `review_mode` and `search_targets`: candidate/full-text/accepted-paper floors scaled by the query surface.
- `coverage_dimensions`: query labels grouped into direct, mechanism, limit, evaluation, deployment, and adjacent evidence surfaces.
- `stopping_rule`: minimum rounds plus consecutive low-new-paper rounds; all floors and dimensions must pass.

Planning rules: prefer wide recall plus strong downstream filtering; never stop because a fixed paper count was reached — counts are floors, and coverage and saturation decide completion; `rapid` is for a bounded decision or early scan, `scoping` for normal topic maps, `systematic` for high-consequence or explicitly exhaustive work; keep static taxonomy, dynamic suggestions, and web calibration visibly separate; do not hard-filter with `cat:` by default — include suggested categories as metadata; treat Reddit and X/Twitter as low-confidence social calibration only; **do not use web or social content as accepted paper evidence**.
3. Search in batches and maintain a registry:
   - Default metadata-search backend is `scripts/search.py search-semantic-scholar` (Semantic Scholar Graph API): zero-sleep with a 0.1s inter-query interval, disk-cached responses shared with `search.py expand-via-citations`, and `--api-key`/`S2_API_KEY` optional. It accepts the same planner `--query-file` and `--start-date/--end-date` contract as `search.py search-arxiv` and emits the same JSON shape.
   - Run `scripts/search.py search-arxiv --query-file <planner-json>` as the arXiv Atom API pass — kept as a second channel and compatibility backend (3s politeness sleep applies).
   - `--query-file` accepts the planner JSON directly by reading top-level `queries` entries with `label` and `query`.
   - Planner `start_date`/`end_date` fields are scope metadata only; `search.py search-arxiv --start-date` and `--end-date` perform the actual arXiv date filtering.
   - Direct `--query` remains available for narrow one-off searches, but literature mining runs should use a planner-generated query file.
   - Keep candidate papers separate from accepted evidence.
   - Use the official API as the first pass, but do not rely on it as the only candidate source.
   - If the API returns `429`, timeouts, SSL errors, or transient server errors, do not treat that as zero evidence. `search.py search-arxiv` waits and retries up to 3 times per query, honoring `Retry-After` for `429` when present; after retries are exhausted, use the Browser fallback in `references/browser-fallback.md`.
   - Merge every API round (`--search-result`, `--semantic-scholar-result`), Browser round, and citation round with `scripts/search.py build-candidate-registry`; do not maintain ad-hoc paper lists.
   - Update screening status (`discovered`, `title-screened`, `full-text-queued`, `extracted`, `accepted`, `rejected`, `unavailable`) instead of deleting candidates.
   - For registries with hundreds of papers, use `scripts/search.py screen-candidates` to create a reproducible title/abstract priority queue. Prior evidence may seed ranking, but the script never marks a paper accepted.
   - Run `scripts/search.py assess-review-coverage` after each round. Continue until candidate, full-text, accepted-paper, dimension, and saturation checks all pass. A target count alone never stops the run.
   - Browser/web results remain discovery-only candidates.
   - Keyword search alone under-covers a broad topic's sub-themes. Once a keyword round saturates but coverage still feels thin, run `scripts/search.py expand-via-citations` against a handful of `accepted`/`full-text-queued` candidates as seeds to chase citation relationships (Semantic Scholar). It ranks 1-hop neighbors by bibliographic coupling/co-citation against the seed set — not a flat per-seed cap — to avoid citation-graph explosion, merges into the registry via `search.py build-candidate-registry --citation-result`, and can emit a `--dynamic-file` for this Skill's planning step so the terms it finds widen the next keyword round. Read `references/citation-expansion.md` before using it.

## Candidate triage: influence ranking

`scripts/search.py rank-influential-papers` ranks the most influential papers in a root paper's
1-hop Semantic Scholar citation neighborhood (what it cites and/or what cites it) by a
**multi-dimensional composite** — citation count, venue prestige, author h-index, code
availability — not by raw citation count alone.

Use it when "most influential around this root paper" must mean more than "most cited",
or to triage a large neighborhood into a shortlist for full-text recovery and deep reading
through `$embodied-ai-paper-reader`. It is **complementary** to `search.py expand-via-citations`:
that script finds de-noised multi-seed sub-topic discoveries; this one scores one root
paper's neighborhood by influence.

1. Decide direction: `--direction references` (foundations the root builds on), `citations` (what it seeded), or `both` (default). Scope with `--min-year`, and gate recall/precision with `--require-terms` (title+abstract OR), `--require-title-terms` (title-only OR), and `--must-terms` (hard AND — how you require a specific perspective).

```bash
python3 skills/embodied-ai-literature-hub/scripts/search.py rank-influential-papers \
  --seed-id 2104.07905 --direction citations --top 10 --min-year 2021 \
  --require-terms "egocentric,exocentric,ego-exo,cross-view,view-invariant,affordance" \
  --must-terms "third-person,third person,exocentric,exo-centric,exo" \
  --output work/<run>/influence-ranking-derived.json \
  --markdown-output work/<run>/influence-ranking-derived.md
```

2. The 1-hop neighborhood is often too small. Enlarge via 2-hop citation expansion, then feed the discovered IDs back in as `--paper-id-file`:

```bash
python3 skills/embodied-ai-literature-hub/scripts/search.py expand-via-citations \
  --seed-id-file work/<run>/hop1-citers.txt --direction citations \
  --min-shared-seeds 2 --output work/<run>/hop2-candidates.json

python3 skills/embodied-ai-literature-hub/scripts/search.py rank-influential-papers \
  --seed-id 2104.07905 --direction citations --top 10 --min-year 2021 \
  --require-terms "egocentric,exocentric,ego-exo,first-person,third-person,cross-view" \
  --paper-id-file work/<run>/hop2-ids.txt \
  --output work/<run>/influence-ranking-enlarged.json
```

3. Read the ranking, then hand the shortlist to `$embodied-ai-paper-reader` for full-text recovery and claim-support audit **before** any of it can be cited as evidence.

Epistemic boundaries: output is **candidate-level discovery**, exactly like keyword/browser/citation channels — a high composite does not make a paper evidence. The **code** signal is the weakest dimension (`abstract` mode is confirm-only; `pwc` mode is best-effort and degrades to neutral). Author h-index is approximate and records *author-level* standing. Read [scoring-rubric.md](references/scoring-rubric.md) before trusting the scores.

## Candidate triage: problem-relevance ranking

`scripts/search.py rank-problem-relevance` fills the **specific gaps** a review still has: given
the review's existing papers as seeds plus its **open research questions**, it does
multi-round citation expansion, extracts each candidate's *judgment surface* (abstract +
introduction + related work), then retrieves the ~50 most task-relevant papers with a BM25
**explanation** of why each is relevant (which question, which terms, which field, a
snippet). Relevance is *shown*, not asserted. Use it when evidence answers the headline
topic but leaves sub-questions open.

Four-stage budget funnel — expensive steps only touch a few papers:

| Stage | Who | Input → Output | Budget |
|---|---|---|---|
| 1. **Fetch** | script | seeds → citation neighbors + judgment surfaces | all fetched (capped), *no reading* |
| 2. **Retrieve** | script (BM25) | corpus → explained relevance shortlist | **~50** |
| 3. **Rank** | you (the agent) read the judgment packet | 50 → relevance-ranked | **20** |
| 4. **Deep-read** | you → `$embodied-ai-paper-reader` | 20 → full-text shortlist | **10** |

1. **Run stages 1–2** (one command):

```bash
python3 skills/embodied-ai-literature-hub/scripts/search.py rank-problem-relevance \
  --question "How is the third-person (exocentric) camera configuration initialized?" \
  --seed-id 2104.07905 --seed-id 2203.09905 \
  --rounds 2 --direction both --min-year 2021 \
  --require-terms "egocentric,exocentric,ego-exo,cross-view,first-person,third-person" \
  --must-terms "third-person,exo,cross-view" \
  --target-retrieved 50 \
  --output work/<run>/problem-relevance.json \
  --markdown-output work/<run>/problem-relevance.md
```

2. **Read the ~50** in the `--markdown-output` judgment packet. Assign each a relevance tier per question using [problem-relevance-rubric.md](references/problem-relevance-rubric.md), then re-rank to a top **20**.
3. **Pick the 10** that most warrant full-text reading and hand them to `$embodied-ai-paper-reader`. Only after that gate can any of them become citable evidence. Stage 3–4 deliverables are **agent-written**; the script intentionally stops at stage 2.

Epistemic boundaries: output is **candidate-level discovery**. BM25 is **lexical** — it can over-rank a paper that *mentions* a concept but never *solves* it, and under-rank papers using synonyms the questions don't literally contain; that is why stage 3 is a human/agent read. The `judgment_surface` is not a full read: a `surface_complete: false` paper fell back to abstract-only — treat its intro/related-work evidence as absent, not negative. Read [retrieval-method.md](references/retrieval-method.md) for the BM25 method and its limits.
4. Extract full text through one gateway:
   - Run `scripts/extract_arxiv_content.py`, which tries structured HTML, flat HTML, then text-layer PDF by default. `--preferred-source auto` inserts a markdown tier after HTML (HTML -> markdown -> PDF); `--preferred-source tex` forces the markdown tier first.
   - The markdown tier (`scripts/fetch.py extract-arxiv-tex`) defaults to the **arxiv2md** transport: a public REST API fetched with plain curl (`GET https://arxiv2md.org/api/markdown?url=<id>`, no credentials, 30 req/min per IP) returning section-aware markdown with LaTeX math and pipe tables. Works for papers with arXiv HTML (roughly 2024-03 onward); papers without HTML answer HTTP 400 and the chain falls through. Requires nothing beyond curl.
   - The alternative `s3-tex` transport is **TODO**: `fetch.py download-arxiv-source` fetches the TeX source tarball from `s3://arxiv/` (boto3, threaded, zero-sleep) and `fetch.py extract-arxiv-tex --transport s3-tex` converts the main `.tex` with pypandoc. The bucket is requester-pays — needs AWS credentials (`RequestPayer=requester`), download bandwidth is billed per GB; pending account setup, `--anonymous` answers `AccessDenied`. Old-style IDs (pre-0704) have no S3 key.
   - Markdown-tier extractions are authoritative text: both `arxiv2md` and `tex-pandoc` methods never need visual validation.
   - Use `--ocr-mode never`. Scan-only or unreadable PDFs are outside this project's scope and remain `unavailable`.
   - Use section/paragraph locators for HTML and page locators for PDF. Preserve the extraction method and quality in the reading handoff.
   - Add `--include-full-text` for papers queued for `$embodied-ai-paper-reader`; selected passages alone are not a complete reading input.
   - Keep low-quality or unavailable documents as candidates. Never treat metadata/abstract text as full-text evidence.
   - Cache HTML/PDF outside the repository. Read [full-text-fallback.md](references/full-text-fallback.md) for the exact fallback contract.
   - For queues spanning many papers, use `scripts/fetch.py extract-content-queue --paper-id-file ... --workers 2`. It checkpoints one JSON result per paper, resumes existing results, caps concurrency at four, and enforces a hard per-paper subprocess timeout; it does not create evidence events.
5. Hand complete papers to `$embodied-ai-paper-reader`:
   - The paper reader owns structure mapping, question-driven deep reading, critical appraisal, claim verification, paper notes, and evidence-event projection.
   - Use `references/evidence-schema.md` only to validate the compatible events projected by the paper reader.

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
   - Validate the JSONL before settling it: `python skills/embodied-ai-literature-hub/scripts/parse.py write-lit-outputs --evidence-jsonl <file> --validate-only` must pass.
   - Settle accepted assets into `evidence/literature-review-<topic>-<date>/`: evidence, brief, source draft, query plan, candidate registry, coverage report, and manifest. Full papers and extraction payloads stay in cache/`work/`.
   - Topic-card update suggestions only for high-signal synthesis.
7. Archive extracted papers into the local public paper pool:
   - The pool (default `~/Documents/arxiv/pool`) is a local shared store outside the repository — one folder per paper keyed by unique ID (`arxiv-2403.12550/` or `doi-<urlquoted>/`), holding `paper.md` (converted full text), `extraction.json`, an optional `note.md` reading note, and `meta.json`; `index.jsonl` indexes the pool. Source tarballs and HTML are temp-dir caches and are never archived here.
   - Add a paper after extraction: `python scripts/knowledge.py pool-add-paper add --extraction work/<run>/extractions/<id>.json --note work/<run>/paper-notes/<id>.md`. Re-adding is idempotent; `--force` refreshes. `list`, `get <id>`, and `import-existing` (migrate legacy flat `<id>.md`) manage the pool.
   - Topic cards cite pool papers directly instead of per-run duplicates: `- id: POOL-arxiv-2403.12550` + `file: <absolute path to paper.md>` + a semantic-anchor `locator` (same ADR-0002 anchors). `scripts/check_kb_links.py` exempts `POOL-*` entries with a `file:` from `sources.md` registration and validates the file exists.

## Evidence rules

- Stance labels: `support`, `limit`, `conditional`, `gap`.
- Confidence labels: `direct`, `citation-supported`, `inference`.
- Author identity is conservative: normalize names, but do not merge same-name authors unless the paper gives stronger evidence such as ORCID, homepage, or clear affiliation continuity.
- Author institution tracking is author-level and first-level only: record the top organization such as `北京大学`, `Google`, `Stanford University`, or `MIT`; omit departments, labs, teams, and centers. If author-to-institution mapping is unreliable, leave `institutions: []`.
- Use short quotes only when useful; prefer precise paraphrase plus page/section locator.

## Script quick start

From the repository root, the in-Skill planning step and search backends:

```bash
python skills/embodied-ai-literature-hub/scripts/search.py build-query-plan \
  --topic "UMI 数据可用性" \
  --knowledge-id EA-DATA \
  --family umi \
  --review-mode scoping \
  --start-date 2023-01-01 \
  --end-date 2026-06-06 \
  --output /tmp/umi-query-plan.json \
  --markdown-output /tmp/umi-query-plan.md

python skills/embodied-ai-literature-hub/scripts/search.py search-semantic-scholar \
  --query-file /tmp/umi-query-plan.json \
  --start-date 2023-01-01 \
  --end-date 2026-06-06 \
  --max-results 25 --batch-label round-1 \
  --output /tmp/umi-s2-candidates.json

python skills/embodied-ai-literature-hub/scripts/search.py search-arxiv \
  --query-file /tmp/umi-query-plan.json \
  --start-date 2023-01-01 \
  --end-date 2026-06-06 \
  --max-results 25 --batch-label round-1 \
  --output /tmp/umi-arxiv-candidates.json

python skills/embodied-ai-literature-hub/scripts/search.py parse-browser-candidates --input /tmp/browser-arxiv-results.json --start-date 2025-12-06 --end-date 2026-06-06 --output /tmp/browser-candidates.json
python skills/embodied-ai-literature-hub/scripts/search.py build-candidate-registry --semantic-scholar-result /tmp/umi-s2-candidates.json --search-result /tmp/umi-arxiv-candidates.json --output work/<run>/candidate-registry.json
python skills/embodied-ai-literature-hub/scripts/search.py assess-review-coverage --query-plan /tmp/umi-query-plan.json --candidate-registry work/<run>/candidate-registry.json --output work/<run>/coverage-report.json
python skills/embodied-ai-literature-hub/scripts/extract_arxiv_content.py --paper-id 2402.10329 --terms UMI,data,demonstration,teleoperation --ocr-mode never --include-selected-text --include-full-text --output work/<run>/extractions/2402.10329.json
# Markdown tier (default arxiv2md transport — needs only curl):
python skills/embodied-ai-literature-hub/scripts/extract_arxiv_content.py --paper-id 2402.10329 --terms UMI,data --preferred-source auto --include-full-text --output work/<run>/extractions/2402.10329.json
python skills/embodied-ai-literature-hub/scripts/knowledge.py pool-add-paper add --extraction work/<run>/extractions/2402.10329.json
python skills/embodied-ai-literature-hub/scripts/parse.py write-lit-outputs --evidence-jsonl evidence.jsonl --brief-out brief.md
```

Once a keyword round saturates, chase citation relationships from vetted candidates to find sub-topics the taxonomy missed (see [citation-expansion.md](references/citation-expansion.md)):

```bash
python skills/embodied-ai-literature-hub/scripts/search.py expand-via-citations \
  --seed-registry work/<run>/candidate-registry.json --seed-status accepted \
  --output work/<run>/citation-candidates.json \
  --graph-output work/<run>/citation-graph.json \
  --dynamic-output work/<run>/citation-dynamic.json
python skills/embodied-ai-literature-hub/scripts/search.py build-candidate-registry \
  --search-result /tmp/umi-arxiv-candidates.json \
  --citation-result work/<run>/citation-candidates.json \
  --output work/<run>/candidate-registry.json
```

The planning step also supports `--list-topics` to enumerate the built-in taxonomy families:

```bash
python skills/embodied-ai-literature-hub/scripts/search.py build-query-plan --list-topics
```

## References

- Read [coverage-and-saturation.md](references/coverage-and-saturation.md) for multi-round registry and stopping logic.
- Read [full-text-fallback.md](references/full-text-fallback.md) whenever HTML is missing or extraction quality is not high.
- Read [evidence-schema.md](references/evidence-schema.md) before creating or validating events.
- Read [browser-fallback.md](references/browser-fallback.md) after API failure or query under-recovery.
- Read [citation-expansion.md](references/citation-expansion.md) before running `search.py expand-via-citations` to widen discovery beyond keyword search.
- Read [topic-taxonomy.md](references/topic-taxonomy.md), [dynamic-expansion.md](references/dynamic-expansion.md), and [web-calibration.md](references/web-calibration.md) for the planning step's taxonomy, dynamic suggestions, and calibration rules.
- Read [scoring-rubric.md](references/scoring-rubric.md) before trusting influence-ranking composites.
- Read [retrieval-method.md](references/retrieval-method.md) and [problem-relevance-rubric.md](references/problem-relevance-rubric.md) before ranking by problem relevance.
