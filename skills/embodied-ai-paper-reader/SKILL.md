---
name: embodied-ai-paper-reader
description: Read recovered embodied-AI paper full text into validated, auditable paper notes and evidence events. Use after literature discovery/full-text recovery and before cross-paper synthesis when Codex must map a paper's structure, perform question-driven deep reading, verify qualitative or quantitative claims against exact locators, record limitations and transfer boundaries, critically appraise methods/evaluation, or migrate legacy evidence that was created from abstracts or ranked passages.
---

# Embodied AI Paper Reader

## Purpose

Convert one recovered paper into a structured paper note, verified evidence cards, and compatible evidence JSONL. Own intellectual reading and claim verification; do not search for papers, recover HTML/PDF, synthesize a literature field, or write reader-facing articles.

Use this pipeline position:

`$embodied-ai-literature-hub -> $embodied-ai-paper-reader -> $embodied-ai-review-writer`

## Required inputs

- Review question, topic ID, and review mode: `rapid`, `scoping`, or `systematic`.
- Paper metadata.
- A complete text extraction from `$embodied-ai-literature-hub`, not only an abstract or ranked passages.
- HTML or text-layer PDF extraction with `high` or `medium` quality.

Reject OCR-derived or scan-only papers as `unavailable`. The workflow does not use Tesseract or other OCR.

## Workflow

1. **Build the reading packet.** Require complete `text` for HTML or complete `pages` for PDF. Selected passages alone are insufficient.

```bash
# Prefer --summary-first for scoping / structure-map passes (H1 token guard).
# Full extraction JSON stays on disk for locator windows and claim-support audits.
python3 skills/embodied-ai-paper-reader/scripts/read.py build-reading-packet \
  --extraction work/<run>/extractions/2402.10329.json \
  --metadata work/<run>/paper-metadata/2402.10329.json \
  --review-question "UMI 数据在什么条件下可迁移到机器人策略?" \
  --topic-id EA-DATA --topic-id EA-XEMBODIMENT \
  --review-mode scoping \
  --summary-first --max-section-chars 4000 \
  --output work/<run>/reading-packets/2402.10329.md \
  --note-template work/<run>/paper-notes/2402.10329.json
```

2. **Prefer one-shot paper-note (default for rapid/scoping).** Follow [reading-contract.md](references/reading-contract.md): one LLM call on the summary-first packet produces a complete `paper-note.json` per [paper-note-schema.md](references/paper-note-schema.md), covering triage, structure map, question-driven reading, evidence cards, critical appraisal ([critical-appraisal.md](references/critical-appraisal.md)), and verification rationale. Mode depth still follows [reading-depth-modes.md](references/reading-depth-modes.md). Never infer the paper from top-ranked passages alone; for evidence cards prefer **locator windows** from the extraction JSON rather than re-pasting Complete extracted text. A paper may yield zero, one, or multiple evidence cards; never manufacture a card to satisfy a quota.
3. **Optional six-pass deep mode.** Use the six-pass protocol in [reading-contract.md](references/reading-contract.md) only for `systematic` / high-stakes reviews or when one-shot notes repeatedly fail claim-support. Do not default to six full-text reloads on scoping runs.
4. **Validate and audit locally.** Structural validation does not replace semantic judgment. Confirm that each card's claim is entailed by its cited context and record the manual verification rationale.

```bash
python3 skills/embodied-ai-paper-reader/scripts/read.py validate-paper-note \
  work/<run>/paper-notes/2402.10329.json

python3 skills/embodied-ai-paper-reader/scripts/read.py audit-claim-support \
  --paper-note work/<run>/paper-notes/2402.10329.json \
  --extraction work/<run>/extractions/2402.10329.json \
  --output work/<run>/paper-notes/2402.10329.audit.json
```

5. **On audit failure, retry only failing cards with a locator window** (not a full re-read):

```bash
python3 skills/embodied-ai-paper-reader/scripts/read.py extract-failed-card-window \
  --audit work/<run>/paper-notes/2402.10329.audit.json \
  --extraction work/<run>/extractions/2402.10329.json \
  --paper-note work/<run>/paper-notes/2402.10329.json \
  --output work/<run>/paper-notes/2402.10329.retry-windows.json \
  --markdown-output work/<run>/paper-notes/2402.10329.retry-windows.md
```

Patch only the failing cards, then re-run validate + audit.

6. **Project evidence only after the gates pass.** Read [evidence-projection.md](references/evidence-projection.md).

```bash
python3 skills/embodied-ai-paper-reader/scripts/read.py project-evidence-events \
  --paper-note work/<run>/paper-notes/2402.10329.json \
  --audit work/<run>/paper-notes/2402.10329.audit.json \
  --id-prefix EA-DATA-2026 --start-seq 1 \
  --output work/<run>/evidence/2402.10329.jsonl
```

7. **Update the reading ledger.** Keep recovered, mapped, deeply read, verified, and accepted counts separate.

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

- `reading-packet.md`: structure map + reading instructions; use `--summary-first` for scoping (section windows) and keep full text on disk in the extraction JSON. Working material only.
- `paper-note.json`: paper-level source of truth for reading decisions.
- `paper-note.audit.json`: locator/context and manual-verification gate result.
- `evidence.jsonl`: compatibility projection for the existing review workflow.
- `reading-ledger.jsonl` and `reading-summary.json`: auditable state and counts.
