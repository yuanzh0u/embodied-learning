# Reading Contract

## Boundary

The Hub owns discovery, full-text recovery, extraction method, and extraction quality. This Skill owns interpreting the recovered full text. The Review Skill owns cross-paper synthesis. The Writer owns audience-specific prose.

Never recreate search, download, PDF parsing, field synthesis, or article writing here.

## Preferred mode: one-shot paper-note (token optimization)

For normal `rapid` / `scoping` runs, prefer **one LLM call per paper** that emits a complete `paper-note.json` conforming to [paper-note-schema.md](paper-note-schema.md). The single call must still cover the intellectual work of triage, structure mapping, question-driven reading, evidence cards, critical appraisal, and verification rationale — just without reloading the full text five more times.

Workflow:

1. Build the reading packet (complete extraction remains on disk; use a summary-first packet when available).
2. **One LLM call** → complete paper-note JSON (including `verification` on every card).
3. Local gates only:
   - `validate_paper_note.py`
   - `audit_claim_support.py`
4. On failure, **retry only failing cards** with a locator window — never a full re-read:

```bash
python3 skills/embodied-ai-paper-reader/scripts/extract_failed_card_window.py \
  --audit work/<run>/paper-notes/<id>.audit.json \
  --extraction work/<run>/extractions/<id>.json \
  --paper-note work/<run>/paper-notes/<id>.json \
  --output work/<run>/paper-notes/<id>.retry-windows.json \
  --markdown-output work/<run>/paper-notes/<id>.retry-windows.md
```

5. Patch the failing cards in the note, re-run validate + audit, then project.

Hard quality bars are unchanged: exact locators, quantitative fields, epistemic tags, and manual `verification` rationale remain mandatory. One-shot is a **calling convention**, not a relaxation of claim-support.

For papers with very long extractions (roughly >80k `text_chars`), still do a cheap structure-map pass first (titles/abstract/conclusion windows only), then one-shot the note from those windows plus on-demand locator pulls — do not dump the entire text into a single truncated prompt.

## Optional deep mode: six-pass protocol

Keep the six-pass protocol for **systematic** reviews, high-stakes decisions, or when one-shot notes repeatedly fail claim-support. It is optional deep mode, not the default for scoping.

### Pass 0: relevance triage

Decide `include`, `background-only`, or `exclude` from title/abstract and the review question. Record the reason. Triage does not create evidence.

### Pass 1: structure map

Prefer a **summary-first reading packet** (`build_reading_packet.py --summary-first`): structure outline + truncated section windows. Selected passages alone still cannot *accept* a paper, but they are valid navigation. Keep the complete extraction JSON on disk; do not paste Complete extracted text into every pass.


Locate:

- problem and claimed contribution;
- method, study design, or organizing framework;
- data, tasks, embodiments, and experimental setting;
- results, analysis, ablations, or examples;
- conclusion and limitations;
- relevant appendix or supplementary material.

Record each role and locator. A keyword-ranked passage is a navigation hint, not a substitute for this pass.

### Pass 2: question-driven deep read

Load only the section/page windows needed for the review question (typically a few thousand characters around each locator). Re-open the full extraction only when a locator window is insufficient.


Read the sections needed to answer the review question. Record every read and skipped section with a reason. Distinguish the paper's stated question from the review's question.

### Pass 3: evidence cards

Create a card only when a distinct review-relevant claim has a precise locator and source context. Use `support`, `limit`, `conditional`, or `gap`. A conflicting result normally uses `limit` and explains the contradicted claim in `relation`.

### Pass 4: critical appraisal

Evaluate study design, data/task representativeness, baseline fairness, metric validity, ablations, reproducibility, and external validity. Record missing information rather than guessing.

### Pass 5: verification and cross-paper routing

Return to the cited context and decide whether it entails the card's exact wording. Check all quantities in their table/figure/page context. Record `verification.status: passed` and a substantive rationale. Route only indispensable cited work into the candidate registry; do not recursively chase every citation.

## Status model

Use exactly one current state:

`discovered -> abstract-screened -> full-text-recovered -> map-read -> deep-read -> claim-verified -> evidence-ready -> accepted`

Terminal alternatives are `rejected` and `unavailable`.

- `unavailable`: no complete readable HTML/text-layer PDF, including scan-only PDF.
- `rejected`: readable and assessed, but irrelevant or unable to yield trustworthy evidence.
- `evidence-ready`: at least one verified evidence card exists.
- `accepted`: evidence-ready and admitted to the run's accepted evidence set.

## Non-OCR rule

Accepted extraction methods are `html-latexml`, `html-flat`, and `pdf-text`. Reject `pdf-ocr` and any payload whose OCR pages are non-empty. Do not install or invoke Tesseract for this workflow.

## Claim-strength rules

- Use `direct` only for an author claim or result directly reported by the paper.
- Use `citation-supported` when the statement depends on another cited work; enqueue that core citation when the claim matters.
- Use `inference` only for a reader synthesis, name its premises, and state what would weaken it.
- Never convert association into causation.
- Never generalize beyond the paper's tasks, data, embodiments, horizon, or evaluation setting without marking an inference.

## Token note

Full-text recovery remains mandatory on disk. Summary-first packets, one-shot notes, and failed-card windows optimize **LLM calls and context**, not the evidence eligibility gate: claim-support audits still match against the complete extraction.
