# Reading Depth Modes

## Rapid

Use for bounded decisions and early scans.

- Map the paper structure.
- Read the problem, review-relevant core, and conclusion/limitations.
- Inspect the exact result source for every projected card.
- Mark the note as non-exhaustive.

Required roles: `problem`, `relevant-core`, `conclusion-or-limitations`.

## Scoping

Use for normal topic mapping.

- Read problem, method/design, results/analysis, and conclusion/limitations.
- Inspect relevant data/task/embodiment details.
- Complete the critical appraisal.
- Record at least one transfer boundary for an included paper.

Required roles: `problem`, `method-or-design`, `results-or-analysis`, `conclusion-or-limitations`.

## Systematic

Use for explicitly exhaustive or high-consequence reviews.

- Meet all scoping requirements.
- Inspect every relevant table, figure, ablation, and appendix/supplement.
- Record explicit inclusion/exclusion reasons.
- Verify every numerical statement from its original result surface.
- Perform a second claim-support pass after drafting the evidence cards.

Required roles: all scoping roles plus `appendix-or-supplement`. If no appendix exists, record that role under `sections_skipped` with reason `not-applicable: no appendix or supplement`.

## Depth is not a paper quota

Mode controls how each selected paper is read. It does not require reading every recovered paper deeply and does not impose a fixed number of evidence cards per paper.
