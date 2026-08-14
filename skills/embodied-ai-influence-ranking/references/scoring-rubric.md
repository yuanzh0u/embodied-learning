# Scoring Rubric

`rank_influential_papers.py` scores every 1-hop neighbor of a root paper with a
weighted composite in `[0, 1]`. Each dimension is normalized independently so no
single raw magnitude (e.g. a 10,000-citation paper) can swamp the others.

## Dimensions and default weights

| Dimension | Weight | Raw signal (source) | Normalization | Bounded as |
|---|---|---|---|---|
| citation | 0.40 | citations/year = `citationCount / age` (Semantic Scholar) | `log1p(v) / log1p(max_v_in_set)` | 0..1 |
| venue | 0.25 | `venue` string → tier | tier1=1.0, tier2=0.66, tier3=0.33 | preprint 0.0, unknown 0.5 |
| author | 0.20 | `authors[].hIndex` (Semantic Scholar batch) | `log1p(h) / log1p(100)` | unknown → 0.5 |
| code | 0.15 | code repo signal (see below) | 1.0 / 0.0 / 0.5 | confirm-only |

Override with `--weights citation=…,venue=…,author=…,code=…` (renormalized to sum 1).

## Why each signal is bounded this way

- **Citation is year-normalized.** A 2015 paper had a decade to accumulate
  citations; a 2025 paper had one year. Raw count alone therefore systematically
  over-credits older papers. The citation dimension uses **citations/year**
  (`citationCount / age`, where age = current year − publication year), so a
  young, fast-rising paper can outrank an older paper with more total citations.
  Raw `citation_count` is still emitted for transparency; only the *score* is
  velocity-based. As with any count, it is power-law distributed, so `log1p`
  compresses the tail and the value is normalized against the largest velocity
  in the candidate set.
- **Venue is ordinal, not cardinal.** A tier is a coarse prestige band. The
  three-tier scheme deliberately avoids pretending we can rank "CVPR vs ICCV vs
  ECCV" — they are peers. An **empty** venue means "preprint" (scores below any
  peer-reviewed venue). An **unmappable** non-empty venue scores a neutral 0.5
  rather than guessing low (a missed venue is our failure, not the paper's).
- **Author standing is a log-scale proxy.** `hIndex` also grows slowly; cap the
  reference at 100 so an h-index of 100+ saturates the score. `--author-strategy
  max-hindex` (default) credits the most established author; `first-author`
  credits the lead author, which is a different (often fairer) signal for
  student-led work. Authors missing an hIndex are treated as *unknown* (0.5),
  not zero.
- **Code availability is the weakest and most fragile signal** — see the next
  section.

## Code availability (weight 0.15)

The user cares about "does it ship a public repo / project", but there is no
single reliable arXiv→code crosswalk. Three modes:

- `abstract` (default): scan title + abstract for release language
  ("github", "open-source", "we release", "code available", "implementation").
  **Confirm-only** — a mention scores 1.0; no mention is *unknown* (0.5), never
  0.0, because absence of a sentence is not absence of a repo.
- `pwc`: query PapersWithCode for `num_repositories`. Confirmed repo → 1.0,
  confirmed zero → 0.0, unreachable/non-JSON → unknown 0.5. This is best-effort;
  PapersWithCode's API has been observed serving HTML instead of JSON, in which
  case the dimension quietly degrades to neutral.
- `none`: always neutral 0.5 (drop the dimension effectively).

Because the weight is the smallest and the signal degrades to neutral rather
than failing, a bad code source cannot corrupt a ranking — it can only cost the
dimension's discrimination.

## Venue tiers

Normalization matches Semantic Scholar's shortened venue strings (substring,
case-insensitive), more-specific-first:

- **tier1 (1.0)**: CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, TPAMI, IJCV,
  Nature/Science, RSS.
- **tier2 (0.66)**: ICRA, IROS, CoRL, AAAI, IJCAI, JMLR, TMLR, RA-L, T-RO,
  SIGGRAPH.
- **tier3 (0.33)**: WACV, ACCV, BMVC, ACMMM.
- **preprint (0.0)**: empty venue.
- **unknown (0.5)**: non-empty but unmappable.

The mapping is a single `VENUE_RULES` list in the script; edit it there if a
venue misclassifies, and add a `classify_venue` test.

## Non-scored context flags

These are emitted for the reviewer but do **not** enter the composite:

- `citations_per_year` — citation velocity (count / age). Age is already
  reflected in raw count, so velocity is reported, not double-counted.
- `is_survey` / `is_dataset` — title heuristic. Surveys, reviews, and
  dataset/benchmark papers attract citations that do not signal method
  influence; they are flagged so the reviewer can read the ranking with that
  distortion in mind, not penalized.
- `direction` — whether the paper is a `references` neighbor (foundation) or a
  `citations` neighbor (descendant), or both.

## Worked example

Root `2104.07905` (Ego-Exo, CVPR 2021, 128 citations). Its neighborhood mixes
highly-cited descendants (Ego4D-style egocentric works) and foundational
references (EPIC-Kitchens, SlowFast, representation distillation). A paper that
is itself a CVPR/NeurIPS paper, with 1,000+ citations and a Grauman/Malik-level
co-author, scores high on all of citation, venue, and author — and will outrank
a preprint with a code repo but 30 citations, even though the preprint wins the
code dimension.
