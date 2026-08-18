---
name: embodied-ai-problem-relevance-ranking
description: Rank papers by problem relevance to open research questions a review still needs to answer. From the review's existing papers as seeds it does multi-round citation expansion, extracts each candidate's abstract + introduction + related-work ("judgment surface"), then retrieves the ~50 most task-relevant papers with a BM25 explanation of why each is relevant. Use to fill the specific gaps in a review before you write it; output is candidate-level discovery, never accepted evidence.
---

# Embodied AI Problem-Relevance Ranking

## What it does

Given a review-in-progress — its existing papers as seeds plus the **open research
questions** it has not fully answered — `rank_problem_relevance.py` finds the papers
**most relevant to those questions**, judged by reading each candidate's
*judgment surface* (abstract + introduction + related-work), not just title/abstract.

The core filter is a **sparse lexical retriever (BM25)** — a RAG retrieval step that
treats the questions as the query and each paper's judgment surface as a multi-field
document, then **explains** why each paper is relevant (which question, which terms, which
field, and a snippet). Relevance is *shown*, not asserted.

## When to use it

- A review's evidence already answers the headline topic but leaves **specific sub-questions
  open** (e.g. "how is the third-person camera configuration initialized?"), and you want
  the papers that actually address those, ranked.
- You have a handful of vetted papers (the review's seeds) and want citation-graph
  discovery plus a relevance ranking in one pass.
- **Not** when you want *influence* (citation count / venue / author) — that is
  `$embodied-ai-influence-ranking`. This skill ranks by *fit to the question*, and reads
  full text to do it; the two are complementary.

## Workflow — a four-stage budget funnel

The expensive steps (reading + full-text recovery) only ever touch a few papers:

| Stage | Who | Input → Output | Budget |
|---|---|---|---|
| 1. **Fetch** | script | seeds → citation neighbors + judgment surfaces | all fetched (capped), *no reading* |
| 2. **Retrieve** | script (BM25) | corpus → explained relevance shortlist | **~50** |
| 3. **Rank** | you (the agent) read the judgment packet | 50 → relevance-ranked | **20** |
| 4. **Deep-read** | you → `$embodied-ai-paper-reader` | 20 → full-text shortlist | **10** |

1. **Run stages 1–2** (one command). Give it the questions and the review's papers as seeds:

```bash
python3 skills/embodied-ai-problem-relevance-ranking/scripts/rank_problem_relevance.py \
  --question "How is the third-person (exocentric) camera configuration initialized?" \
  --question "How are first-person and third-person views aligned?" \
  --question "How are multiple third-person (multiview) cameras aligned?" \
  --seed-id 2104.07905 --seed-id 2203.09905 --seed-id 2208.13196 \
  --seed-id 2303.09665 --seed-id 2306.05526 --seed-id 2311.18259 \
  --seed-id 2312.02638 --seed-id 2401.00789 --seed-id 2403.16182 \
  --seed-id 2406.08877 --seed-id 2411.19083 \
  --rounds 2 --direction both --min-year 2021 \
  --require-terms "egocentric,exocentric,ego-exo,cross-view,first-person,third-person,multiview,multi-view,camera,calibration" \
  --must-terms "third-person,exo,cross-view,multiview,multi-view,camera,calibration" \
  --target-retrieved 50 \
  --output work/<run>/problem-relevance-egoexo.json \
  --markdown-output work/<run>/problem-relevance-egoexo.md
```

2. **Read the ~50** in the `--markdown-output` judgment packet (not the full text of
   everything — just the ~50 surfaces). Assign each a relevance tier per question using
   `references/problem-relevance-rubric.md`, then re-rank to a top **20**.

3. **Pick the 10** from the 20 that most warrant full-text reading, and hand them to
   `$embodied-ai-paper-reader` for recovery + claim-support audit. Only *after* that gate
   can any of them become citable evidence.

## Required inputs

- `--question` (repeatable): the open research questions. These are the *query*.
- Seeds: `--seed-id` / `--seed-id-file` / `--seed-registry` — the review's existing papers.

## Outputs

- Retrieved JSON (`--output`): the ~50 papers with `judgment_surface` (abstract /
  introduction / related-work), per-question BM25 + matched terms, `retrieval_score`,
  and an `explanation` per question (term → fields → contribution → snippet).
- Judgment packet Markdown (`--markdown-output`): the same, pre-ranked, in one file for
  stage 3 reading.
- Stage 3–4 deliverables (`relevance-ranked-20`, `fulltext-shortlist-10`) are
  **agent-written**; the script intentionally stops at stage 2.

## Epistemic boundaries

- Output is **candidate-level discovery**, exactly like keyword/browser/citation channels.
  A high BM25 score does not make a paper evidence: it still needs complete non-OCR full
  text, a validated paper note, and a passing claim-support audit.
- BM25 is **lexical**. It matches surface terms, so it can over-rank a paper that *mentions*
  "camera calibration" but never *solves* it, and under-rank a paper that uses synonyms
  ("pose estimation", "rig registration") the questions don't literally contain. That is
  exactly why stage 3 is a human/agent read of the surfaces — the retriever narrows 1000s →
  50, it does not make the final call.
- The `judgment_surface` is *not* a full read: a paper may address a question in its Method
  section without saying so in abstract/intro/related-work. A `surface_complete: false`
  paper fell back to abstract-only; treat its intro/related-work evidence as absent, not negative.

## References

- [retrieval-method.md](references/retrieval-method.md) — the BM25 "regular method": field
  weights, idf/length normalization, how the explanation is built, and its limits.
- [problem-relevance-rubric.md](references/problem-relevance-rubric.md) — the four relevance
  tiers for stage 3, with worked cues for the ego-exo questions.
