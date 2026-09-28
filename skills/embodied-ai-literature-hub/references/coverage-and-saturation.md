# Coverage And Saturation

Use this reference for reviews that may involve tens or hundreds of papers.

## Candidate Registry

Build one append-only logical registry from every API and Browser batch. Keep a
paper after rejection or extraction failure; change its status and record the
reason. Deduplicate on base arXiv ID while preserving all query labels and
discovery batches.

```bash
python3 skills/embodied-ai-literature-hub/scripts/build_candidate_registry.py \
  --search-result work/<run>/search-round-1.json \
  --search-result work/<run>/search-round-2.json \
  --browser-result work/<run>/browser-round-3.json \
  --screening-file work/<run>/screening.json \
  --output work/<run>/candidate-registry.json
```

## Stop Assessment

Run after each search/screening round:

```bash
python3 skills/embodied-ai-literature-hub/scripts/assess_review_coverage.py \
  --query-plan work/<run>/query-plan.json \
  --candidate-registry work/<run>/candidate-registry.json \
  --evidence-jsonl work/<run>/evidence.jsonl \
  --output work/<run>/coverage-report.json
```

Stop only when all five checks pass:

1. candidate floor;
2. full-text extraction floor;
3. accepted-paper floor;
4. every query-derived coverage dimension;
5. the configured number of consecutive low-new-unique-paper batches.

A pool of 200 papers can still fail if it covers only direct positive papers.
A pool below the target can be useful for a preliminary brief, but it is not a
completed review. Distinguish “this run did not cover it” from “the literature
identifies an open problem”.


## Agent context rules (token optimization)

- **NEVER** load the full `candidate-registry.json` into the model context. Registries are commonly 2–5 MB with long summaries.
- Allowed context inputs for coverage decisions:
  - `coverage-report.json` (primary);
  - `screening-*.md` / screening JSON summaries;
  - `status_counts` and title-only top-N via:

```bash
python3 skills/embodied-ai-literature-hub/scripts/print_registry_titles.py \
  --candidate-registry work/<run>/candidate-registry.json \
  --status full-text-queued --status extracted --limit 80
```

- Do **not** paste raw search-round JSON (`search-round-*.json`, large OpenAlex/arXiv batch files) into the conversation; merge them into the registry with scripts, then read the coverage report.
