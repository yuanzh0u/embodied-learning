# Reading Contract

## Boundary

The Hub owns discovery, full-text recovery, extraction method, and extraction quality. This Skill owns interpreting the recovered full text. The Review Skill owns cross-paper synthesis. The Writer owns audience-specific prose.

Never recreate search, download, PDF parsing, field synthesis, or article writing here.

## Six-pass protocol

### Pass 0: relevance triage

Decide `include`, `background-only`, or `exclude` from title/abstract and the review question. Record the reason. Triage does not create evidence.

### Pass 1: structure map

Locate:

- problem and claimed contribution;
- method, study design, or organizing framework;
- data, tasks, embodiments, and experimental setting;
- results, analysis, ablations, or examples;
- conclusion and limitations;
- relevant appendix or supplementary material.

Record each role and locator. A keyword-ranked passage is a navigation hint, not a substitute for this pass.

### Pass 2: question-driven deep read

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
