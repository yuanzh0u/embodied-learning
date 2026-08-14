# Candidate Coverage and Saturation Report

## Gate result

- Status: **passed / ready to stop**
- Review mode: `scoping`
- Candidate registry: 471 unique records
- Complete non-OCR full texts recovered: 47
- Accepted evidence papers: 17
- Discovery batches: 6

## Query-dimension coverage

| Dimension | Required | Observed | Result |
|---|---:|---:|---|
| direct-topic | 3 | 141 | pass |
| adjacent-and-transfer | 3 | 200 | pass |
| limits-and-counterevidence | 3 | 20 | pass |
| evaluation-and-validation | 3 | 50 | pass |
| mechanisms-and-interfaces | 3 | 100 | pass |

## Saturation

| Batch | Channel | Unique | New | New rate |
|---|---|---:|---:|---:|
| plan-relevance-1 | arXiv API | 286 | 286 | 100.00% |
| known-works-2 | arXiv API | 4 | 3 | 75.00% |
| missing-dimensions-3 | arXiv API | 147 | 146 | 99.32% |
| author-recall-4 | arXiv API | 61 | 35 | 57.38% |
| title-recall-5 | arXiv API | 13 | 0 | 0.00% |
| browser-fallback | Browser | 13 | 0 | 0.00% |

The stopping rule required at least three batches and two consecutive tail batches with at most 10% new unique records. The final exact-title recall and independent Browser fallback both added no new papers, so the saturation gate passed.

## Interpretation

Candidate counts establish search breadth, not evidence quality. Only the 17 papers listed in `paper-note-index.json` entered accepted evidence after complete full-text recovery, scoping-depth reading, paper-note validation, and a passing claim-support audit. The machine-readable source of truth is `coverage-report.json`.
