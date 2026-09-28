# Agent Instructions

This repository is a research knowledge base. Optimize for context efficiency and traceability.

## Loading Order

1. Start with [knowledge/index.md](knowledge/index.md).
2. Load the domain index that matches the task:
   - [knowledge/embodied-ai/index.md](knowledge/embodied-ai/index.md)
   - [knowledge/error-governance/index.md](knowledge/error-governance/index.md)
3. When the task concerns an existing literature review, **do not** paste the full [knowledge/literature-review-catalog.md](knowledge/literature-review-catalog.md) into context. Grep/search for the topic or knowledge ID, or read only the matching table rows / run folder; then open that run's `run.json` / coverage report.
4. Load only the topic cards listed in `load_when` or `query_routes`.
5. Open paper notes or raw source documents only when exact wording, detailed evidence, or references are needed.
6. Load **only the current skill's `SKILL.md`**, then step-specific `references/` as needed. Do not preload every literature-review skill or the full catalog.

## Token / context soft guards

- **NEVER** `Read` full `candidate-registry.json` into LLM context (often 2–5 MB). Use `coverage-report.json`, `screening-*.md`, `status_counts`, or `skills/embodied-ai-literature-hub/scripts/print_registry_titles.py` (title-only top-N).
- Coverage decisions: read the coverage report only — **do not** paste search-round JSON (`openalex-candidates-round*.json`, raw arXiv batch files) into the conversation.
- Paper reading: prefer `build_reading_packet.py --summary-first` (structure map + section windows). Keep full extraction on disk; open locator windows for claim cards. Do not re-paste Complete extracted text every pass.
- Writer inputs: `writing-brief.md` / `evidence-appendix.md` are stance-capped; complete events stay in `evidence.jsonl` for audits.

## Context Rules

- Prefer topic cards over raw long-form materials.
- Preserve frontmatter fields when editing topic cards.
- Add new material through [knowledge/ingestion-guide.md](knowledge/ingestion-guide.md).
- Keep every synthesized claim traceable to a `source` entry or mark it as an inference.
- Use stable IDs such as `EA-DATA`, `EA-EVAL`, and `ERR-PATTERN` when referring to knowledge units.

## Research Workflow

- When researching a topic, first use the project skill `embodied-ai-literature-review`; it orchestrates `embodied-ai-query-planner` and `embodied-ai-literature-hub` for search planning, evidence extraction, and final review drafting.
- A paper may enter accepted evidence only after complete non-OCR full text, a validated paper note, and a passing claim-support audit. Scanned-only papers are out of scope.

## Source Of Truth

- `evidence/` is the source of truth for paper-level evidence and finished literature reviews (versioned, append-only per run).
- Settled runs sink into `evidence/` via `scripts/sink_run.py` (idempotent; stamps a `sink_checklist` into run.json; refuses gate-failed bundles unless `--allow-gate-fail`). Run `scripts/check_sink_integrity.py` after any sink or cleanup — it reconciles `work/`, `evidence/`, and the catalog, and exits non-zero on drift.
- Retired raw documents remain traceable through their registered git archives in [knowledge/sources.md](knowledge/sources.md) (`git show 081e898:<file>`).
- Topic cards are compressed working memory for agents.
- The master index is the topic routing layer; [knowledge/literature-review-catalog.md](knowledge/literature-review-catalog.md) declares current literature-review versions — load topic-filtered rows only, never the whole file by default.
- Candidates and intermediate artifacts live in `work/` (gitignored scratch); accepted assets live in `evidence/`.

## Cross-Project Knowledge

- Keep research knowledge and paper evidence in this project as the source of truth.
- For company positioning, PR expression, business planning, compliance, or other cross-project tasks, read `/Users/ryan/Documents/个人知识库/indexes/global-routing.md`.
- Load only the routed shared card or project index; do not scan every connected project.
- Update this project's owner file first, then synchronize any affected shared note.
