---
name: embodied-ai-paper-reader
description: Read recovered embodied-AI paper full text into validated, auditable paper notes and evidence events. Use after literature discovery/full-text recovery and before cross-paper synthesis when Codex must map a paper's structure, perform question-driven deep reading, verify qualitative or quantitative claims against exact locators, record limitations and transfer boundaries, critically appraise methods/evaluation, or migrate legacy evidence that was created from abstracts or ranked passages.
---

# Embodied AI Paper Reader

## Purpose

Convert one recovered paper into a structured paper note, verified evidence cards, and compatible evidence JSONL. Own intellectual reading and claim verification; do not search for papers, recover HTML/PDF, synthesize a literature field, or write reader-facing articles.

Use this pipeline position:

`$embodied-ai-literature-hub -> $embodied-ai-paper-reader -> $embodied-ai-literature-review -> $embodied-ai-review-writer`

## Required inputs

- Review question, topic ID, and review mode: `rapid`, `scoping`, or `systematic`.
- Paper metadata.
- A complete text extraction from `$embodied-ai-literature-hub`, not only an abstract or ranked passages.
- HTML or text-layer PDF extraction with `high` or `medium` quality.

Reject OCR-derived or scan-only papers as `unavailable`. The workflow does not use Tesseract or other OCR.

## Workflow

1. **Build the reading packet.** Require complete `text` for HTML or complete `pages` for PDF. Selected passages alone are insufficient.

```bash
python3 skills/embodied-ai-paper-reader/scripts/build_reading_packet.py \
  --extraction work/<run>/extractions/2402.10329.json \
  --metadata work/<run>/paper-metadata/2402.10329.json \
  --review-question "UMI 数据在什么条件下可迁移到机器人策略?" \
  --topic-id EA-DATA --topic-id EA-XEMBODIMENT \
  --review-mode scoping \
  --output work/<run>/reading-packets/2402.10329.md \
  --note-template work/<run>/paper-notes/2402.10329.json
```

2. **Map before deep reading.** Identify the paper type, problem, method/design, results/analysis, conclusion/limitations, and relevant appendix. Never infer the paper from the top-ranked passages alone.
3. **Read against the review question.** Follow the mode-specific depth in [reading-depth-modes.md](references/reading-depth-modes.md) and the six-pass protocol in [reading-contract.md](references/reading-contract.md).
4. **Write the paper note.** Follow [paper-note-schema.md](references/paper-note-schema.md). A paper may yield zero, one, or multiple evidence cards; never manufacture a card to satisfy a quota.
5. **Critically appraise it.** Read [critical-appraisal.md](references/critical-appraisal.md). Separate author-stated limitations from reader-inferred transfer boundaries.
6. **Validate and audit.** Structural validation does not replace semantic judgment. Confirm that each card's claim is entailed by its cited context and record the manual verification rationale.

```bash
python3 skills/embodied-ai-paper-reader/scripts/validate_paper_note.py \
  work/<run>/paper-notes/2402.10329.json

python3 skills/embodied-ai-paper-reader/scripts/audit_claim_support.py \
  --paper-note work/<run>/paper-notes/2402.10329.json \
  --extraction work/<run>/extractions/2402.10329.json \
  --output work/<run>/paper-notes/2402.10329.audit.json
```

7. **Project evidence only after the gates pass.** Read [evidence-projection.md](references/evidence-projection.md).

```bash
python3 skills/embodied-ai-paper-reader/scripts/project_evidence_events.py \
  --paper-note work/<run>/paper-notes/2402.10329.json \
  --audit work/<run>/paper-notes/2402.10329.audit.json \
  --id-prefix EA-DATA-2026 --start-seq 1 \
  --output work/<run>/evidence/2402.10329.jsonl
```

8. **Update the reading ledger.** Keep recovered, mapped, deeply read, verified, and accepted counts separate.

```bash
python3 skills/embodied-ai-paper-reader/scripts/update_reading_ledger.py \
  --ledger work/<run>/reading-ledger.jsonl \
  --paper-note work/<run>/paper-notes/2402.10329.json \
  --audit work/<run>/paper-notes/2402.10329.audit.json \
  --summary-output work/<run>/reading-summary.json
```

## Hard gates

- `full-text-recovered` never means `map-read`, `deep-read`, or `claim-verified`.
- Do not accept a paper from metadata, abstract, ranked snippets, or selected passages alone.
- Require an exact section/paragraph or page/table/figure locator for every evidence card.
- Require metric, value/direction, comparator, task/sample, and locator for every quantitative card.
- Keep `direct`, `citation-supported`, and `inference` epistemically distinct.
- Require a manual support check for every projected card; deterministic context matching is only a pre-check.
- Preserve negative, limiting, conditional, and gap evidence.
- Do not force one paper into one event. Project one event per distinct verified card.
- Do not count legacy evidence as newly read until a paper note and support audit pass.

## Outputs

- `reading-packet.md`: complete text plus structure and reading instructions; working material only.
- `paper-note.json`: paper-level source of truth for reading decisions.
- `paper-note.audit.json`: locator/context and manual-verification gate result.
- `evidence.jsonl`: compatibility projection for the existing review workflow.
- `reading-ledger.jsonl` and `reading-summary.json`: auditable state and counts.

## Legacy multi-run migration

Plan a deduplicated migration before recovering or reading papers. The planner prioritizes papers already cited by reader-facing articles, then limiting/conditional/gap and multi-event papers until each run reaches its mode floor. After recovery, rerun the planner with `--require-readable`; never preserve an old citation merely because it was once accepted. Use `--supplement-file` for explicitly reviewed backfills when an old run has no spare readable accepted paper:

```bash
python3 skills/embodied-ai-paper-reader/scripts/plan_review_migration.py \
  --runs-root evidence --run-pattern 'literature-review-*-20260714' \
  --extraction-dir work/paper-reader-migration/full-text \
  --paper-floor 15 --require-readable \
  --supplement-file work/paper-reader-migration/readable-backfills.json \
  --output work/paper-reader-migration/final-migration-plan.json \
  --paper-id-output work/paper-reader-migration/final-paper-ids.txt
```

Build new draft runs without modifying settled evidence. `migrate_review_runs.py` reconstructs section maps, uses exact full-text contexts, validates every note, audits every card, and projects compatible evidence. Its lexical matcher is only a navigation aid: low-quality or over-broad legacy claims must be manually narrowed in an override JSON before they can be marked verified.

```bash
python3 skills/embodied-ai-paper-reader/scripts/migrate_review_runs.py \
  --plan work/paper-reader-migration/final-migration-plan.json \
  --extraction-dir work/paper-reader-migration/full-text \
  --output-root work/paper-reader-migration/draft-runs \
  --diagnostics work/paper-reader-migration/migration-diagnostics.json \
  --override-file work/paper-reader-migration/reviewed-context-overrides.json \
  --event-prefix-file work/paper-reader-migration/event-prefixes.json \
  --cards-per-paper 1 --minimum-match-score 0.16
```

Migration rules:

- Keep prior settled runs immutable; publish a suffixed append-only run.
- Give every migrated run its own globally unique event prefix. Prefer an audited mapping file; without one, the script appends a deterministic run-name fingerprint and records the result in `run.json`.
- Count only complete, evidence-eligible, non-OCR full text toward the paper floor.
- Inspect the lowest-scoring selected matches and every manually narrowed claim.
- An override must name an exact full-text section and start marker; it may narrow a legacy claim but must never broaden it.
- Draft runs remain `in-progress` until the review writer and every bundle gate pass.
