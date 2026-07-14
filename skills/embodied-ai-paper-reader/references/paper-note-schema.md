# Paper Note Schema

`paper-note.json` is the source of truth for what was actually read. Evidence JSONL is a downstream projection.

## Top-level fields

```json
{
  "schema_version": 1,
  "paper": {
    "arxiv_id": "2402.10329",
    "title": "Universal Manipulation Interface",
    "published": "2024-02-15",
    "url": "https://arxiv.org/abs/2402.10329",
    "authors": []
  },
  "review": {
    "question": "Review question",
    "topic_ids": ["EA-DATA"],
    "mode": "scoping"
  },
  "extraction": {
    "source_format": "html",
    "method": "html-latexml",
    "quality": "high",
    "full_text_available": true,
    "ocr_pages": [],
    "visual_validation": "not-required"
  },
  "reading": {
    "status": "evidence-ready",
    "paper_type": "method",
    "relevance": {"decision": "include", "reason": "..."},
    "sections_read": [
      {"locator": "1 Introduction", "role": "problem", "purpose": "..."},
      {"locator": "3 Method", "role": "method-or-design", "purpose": "..."},
      {"locator": "4 Experiments", "role": "results-or-analysis", "purpose": "..."},
      {"locator": "6 Limitations", "role": "conclusion-or-limitations", "purpose": "..."}
    ],
    "sections_skipped": []
  },
  "research_question": "...",
  "contributions": ["..."],
  "method": {"summary": "...", "assumptions": ["..."]},
  "study_context": {"datasets": [], "tasks": [], "embodiments": [], "sample_or_scale": "..."},
  "evaluation": {"design": "...", "baselines": [], "metrics": [], "ablations": []},
  "findings": [{"finding": "...", "scope": "...", "locator": "..."}],
  "limitations": {
    "author_status": "found",
    "author_stated": [{"limitation": "...", "locator": "..."}],
    "reader_inferred": [{"boundary": "...", "basis": "..."}]
  },
  "transfer_boundary": "...",
  "critical_appraisal": {
    "design_strengths": [],
    "design_risks": [],
    "baseline_fairness": "...",
    "metric_validity": "...",
    "reproducibility": "...",
    "external_validity": "..."
  },
  "evidence_cards": [],
  "core_citations": [],
  "notes": ""
}
```

## Allowed values

- `review.mode`: `rapid`, `scoping`, `systematic`.
- `reading.paper_type`: `method`, `empirical`, `dataset`, `benchmark`, `survey`, `position`, `theory`, `system`, `other`.
- `reading.relevance.decision`: `include`, `background-only`, `exclude`.
- Section roles: `problem`, `relevant-core`, `method-or-design`, `data-or-setting`, `results-or-analysis`, `conclusion-or-limitations`, `appendix-or-supplement`.
- `limitations.author_status`: `found`, `not-found`.

## Evidence card

```json
{
  "card_id": "2402.10329-C01",
  "claim": "A precise claim bounded to the paper's experiment.",
  "stance": "conditional",
  "relation": "What review proposition this supports or limits.",
  "confidence": "direct",
  "claim_basis": "reported-result",
  "summary": "Why the cited material supports the claim.",
  "locator": "page 6, Table 2",
  "source_context": "A short verbatim or tightly preserved context from the extracted full text.",
  "evidence_type": "experiment",
  "quantitative": {
    "metric": "success rate",
    "value_or_direction": "+12 percentage points",
    "comparator": "baseline X",
    "task_or_sample": "three real-robot tasks",
    "locator": "page 6, Table 2"
  },
  "verification": {
    "status": "passed",
    "checked_against": "full-text",
    "rationale": "The table reports the same task, metric, comparator, and direction; the claim does not generalize beyond those tasks."
  }
}
```

Use `quantitative: false` for qualitative cards. Allowed `claim_basis` values are `author-claim`, `reported-result`, `cited-work`, and `reader-inference`.

## Zero-event papers

A deeply read paper may have `evidence_cards: []`. Keep its status at `deep-read`, `rejected`, or another accurate state. Do not mark it `evidence-ready` or project an empty placeholder event.
