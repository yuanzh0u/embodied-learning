# Evidence Projection

## Source of truth

Project evidence events from a validated `paper-note.json`; never edit projected JSONL as the primary record. If a claim changes, edit and revalidate the paper note, then regenerate events.

## Projection rule

- One distinct verified evidence card becomes one evidence event.
- Zero cards produce zero events.
- Preserve the card's stance, confidence, locator, source context, extraction provenance, and verification rationale.
- Preserve paper metadata and conservative author identity.
- Preserve core citations only when they carry essential support.

## Compatibility

Projected events use the existing `$embodied-ai-literature-hub` evidence schema so `$embodied-ai-literature-review` and `$embodied-ai-review-writer` can consume them. Extra `paper_reading` metadata records paper-note schema, card ID, review mode, and reading status.

## Admission gate

Projection requires:

- note validation passes;
- reading status is `evidence-ready` or `accepted`;
- each card has `verification.status: passed`;
- full text is complete and non-OCR;
- every quantitative card is fully contextualized.

After projection, run the Hub's compatibility validator:

```bash
python3 skills/embodied-ai-literature-hub/scripts/write_lit_outputs.py \
  --evidence-jsonl <projected.jsonl> --validate-only
```
