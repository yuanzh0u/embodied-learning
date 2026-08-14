---
name: embodied-ai-influence-ranking
description: Rank the most influential papers in a root paper's citation neighborhood across four dimensions (citation count, venue prestige, author h-index, code availability), producing an auditable composite score. Use to answer "which of the papers around this root paper are the most influential" for discovery and triage; outputs are candidate-level, never accepted evidence.
---

# Embodied AI Influence Ranking

## What it does

Given a root arXiv paper, `rank_influential_papers.py` walks its 1-hop citation
neighborhood (what it cites and/or what cites it) via Semantic Scholar and ranks
every neighbor by a **multi-dimensional influence score**, not by raw citation
count alone.

## When to use it

- A reviewer wants the "most influential" papers around a known root paper, and
  wants that "influence" to mean more than "most cited" — venue prestige, author
  standing, and code availability matter too.
- Triaging a large citation neighborhood into a shortlist of papers worth
  full-text recovery and deep reading through `$embodied-ai-paper-reader`.
- **Not** when you need de-noised *multi-seed* sub-topic discovery — that is
  `$embodied-ai-literature-hub`'s `expand_via_citations.py` (bibliographic
  coupling / co-citation). This skill scores one root paper's neighborhood by
  influence; the two are complementary.

## Workflow

1. Decide direction: `--direction references` (foundations the root builds on),
   `citations` (what it seeded), or `both` (default).
2. Optionally scope to a subfield / time window: `--min-year YYYY` (drop older
   neighbors), `--require-terms "…"` (title+abstract OR match, recall gate),
   `--require-title-terms "…"` (title-only OR match, precision gate), and
   `--must-terms "…"` (hard AND gate — a paper is dropped unless at least one
   must-term appears). `--must-terms` is how you require a specific perspective,
   e.g. "third-person/exo must be present, ego-only is not wanted":

```bash
python3 skills/embodied-ai-influence-ranking/scripts/rank_influential_papers.py \
  --seed-id 2104.07905 --direction citations --top 10 --min-year 2021 \
  --require-terms "egocentric,exocentric,ego-exo,cross-view,view-invariant,affordance" \
  --must-terms "third-person,third person,exocentric,exo-centric,exo" \
  --output work/<run>/influence-ranking-derived.json \
  --markdown-output work/<run>/influence-ranking-derived.md
```

3. Enlarge the pool (the 1-hop neighborhood is often too small). Chase 2-hop
   downstream via `$embodied-ai-literature-hub`'s citation expansion, then feed
   the discovered IDs back in as `--paper-id-file`:

```bash
# 2-hop: what cites Ego-Exo's direct citers
python3 skills/embodied-ai-literature-hub/scripts/expand_via_citations.py \
  --seed-id-file work/<run>/hop1-citers.txt --direction citations \
  --min-shared-seeds 2 --output work/<run>/hop2-candidates.json

# rank 1-hop + 2-hop together (year-normalized, field-gated)
python3 skills/embodied-ai-influence-ranking/scripts/rank_influential_papers.py \
  --seed-id 2104.07905 --direction citations --top 10 --min-year 2021 \
  --require-terms "egocentric,exocentric,ego-exo,first-person,third-person,cross-view" \
  --paper-id-file work/<run>/hop2-ids.txt \
  --output work/<run>/influence-ranking-enlarged.json
```

4. Read the ranking, then hand the shortlist to `$embodied-ai-paper-reader` for
   full-text recovery and claim-support audit **before** any of it can be cited
   as evidence.

## Required inputs

- `--seed-id` (repeatable): the root arXiv ID(s).

## Outputs

- Ranked JSON (`--output`): one record per paper with raw signals, per-dimension
  sub-scores, the composite, and non-scored flags (survey/dataset, citation
  velocity, direction).
- Ranking table Markdown (`--markdown-output`).

## Epistemic boundaries

- Output is **candidate-level discovery**, exactly like keyword/browser/citation
  channels. A high composite does not make a paper evidence: it still needs
  complete non-OCR full text, a validated paper note, and a passing
  claim-support audit.
- The **code** signal is the weakest dimension: `abstract` mode (default) is
  confirm-only (a mention scores 1.0, absence is neutral 0.5, never penalized);
  `pwc` mode is best-effort and degrades to neutral when PapersWithCode is
  unreachable. Read [scoring-rubric.md](references/scoring-rubric.md) before
  trusting it.
- Author h-index comes from Semantic Scholar and is approximate; it records
  *author-level* standing, not a claim about the paper itself.

## References

- [scoring-rubric.md](references/scoring-rubric.md) — dimensions, weights,
  normalization, venue tiers, and the reasons each signal is bounded the way it
  is.
