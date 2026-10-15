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
  "figures": [],
  "tables": [],
  "notes": ""
}
```

## Figures and tables (auto-filled by the deep-read flow)

`figures: []` and `tables: []` are **card-level optional fields** filled automatically by the
deep-read assembly: the skeleton agent picks at most one `figure_id`/`table_id` per evidence
card from the extraction's figure/table inventory (with a one-line Chinese `usage`), and
`read.py build-paper-note` joins those ids against `extraction.json`'s `figures[]/tables[]` records —
caption, `image_url` (figures) and `rows` (tables) come from the extraction, never from the
agent; ids that do not match an extraction record are dropped. Each figure/table records the
caption and the usage only — the pipeline never parses figure/table *content*. Figures
reference the paper's external arXiv HTML image URL; tables carry their captured cell rows
(LaTeXML tables have no image link). Evidence projection copies the card's records onto the
event as `evidence.figures[] / evidence.tables[]`.

```json
"figures": [
  {
    "figure_id": "S3.F3",
    "caption": "The Aria device used for egocentric recordings.",
    "image_url": "https://arxiv.org/html/2311.18259v4/figs/aria/aria.png",
    "section": "3 Ego-Exo4D dataset",
    "usage": "作者用该图展示采集 rig 中 Aria 眼镜本体。"
  }
],
"tables": [
  {
    "table_id": "S1.T1",
    "caption": "Comparison between Ego-Exo4D and relevant datasets.",
    "section": "3 Ego-Exo4D dataset",
    "rows": [["Dataset", "Year"], ["Ego-Exo4D", "2023"]],
    "usage": "作者用该表对比数据集。"
  }
]
```

The `fetch.py render-figure-table-block` helper in the literature-hub skill turns these records
into markdown snippets for the review deliverables (figures render as `![caption](image_url)`
which the research wiki displays as a real `<img>`; tables render as a markdown grid).
`write.py review-packet` already renders them into the evidence appendix and the writing
brief's 可用图表 section.

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
