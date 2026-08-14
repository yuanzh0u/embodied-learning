# Citation-Graph Expansion

Keyword search alone under-covers a broad topic: a big topic usually has several
sub-themes that a fixed keyword taxonomy never anticipated. `expand_via_citations.py`
widens discovery by chasing citation relationships one hop out from a set of seed
papers, using Semantic Scholar's Graph API (arXiv-only crosswalk via
`externalIds.ArXiv`) instead of a second query taxonomy.

## When to use it

- A keyword round has reached saturation (`assess_review_coverage.py` reports
  `ready_to_stop`), but you suspect there are sub-topics the static taxonomy
  never named.
- You already have a handful of `accepted`/`full-text-queued` candidates for the
  topic — these make the best seeds, since they are already vetted rather than
  raw unscreened hits.

## Why naive citation chasing explodes, and how this script avoids it

Pulling every reference and every citing paper of a seed does not work: a single
seed can have 50-100 references and a highly-cited seed can have hundreds of
citing papers, almost all irrelevant to the specific sub-topic you care about.

Instead of a flat per-seed cap, this script scores every 1-hop neighbor by how
many **distinct seeds** connect to it — the same signal
[Connected Papers](https://www.connectedpapers.com/) uses:

- **Bibliographic coupling**: a paper referenced by two or more seeds is a likely
  shared foundational/ancestor paper for the sub-topic those seeds have in common.
- **Co-citation**: a paper that cites two or more seeds together is likely
  synthesizing or connecting that same sub-topic.

`--min-shared-seeds` (default: 2 once you give it 2+ seeds, otherwise 1) is the
real filter — not `--max-per-seed-per-direction`, which is only a safety valve
against a single request returning thousands of items. Candidates that don't
clear the threshold are **not silently dropped**: they are counted in
`below_threshold_count` and, if you pass `--include-below-threshold-output`,
written to their own file for anyone who wants the noisier, wider recall.
`--max-total-candidates` is a last-resort cap after ranking by shared-seed count;
if it truncates anything, `truncated_count` says so.

With a single seed, `--min-shared-seeds` degenerates to 1 (there is nothing to
couple against) — you get plain 1-hop citation chasing, no de-noising. The
coupling/co-citation benefit specifically needs 2+ seeds, which is why
`--seed-registry --seed-status accepted` (pulling several already-vetted papers)
is the recommended way to seed a run.

## Reading the seed-similarity matrix

`--graph-output` includes a `seed_similarity` list: for every pair of seeds, a
Jaccard-normalized `reference_coupling_jaccard` (shared references) and
`citation_cocitation_jaccard` (shared citers), sorted by combined score
descending. A seed whose similarity to every other seed is consistently low is
a signal that it belongs to a **different sub-topic** than the rest of the set —
worth pulling out and running as its own seed group in a separate invocation.
This script does not auto-cluster seeds into sub-topic groups; the matrix gives
you (or an agent) the signal to decide that manually. Automatic clustering is a
plausible future enhancement built on the same data, not something this version
does.

## The two-hop loop: candidates now, keywords for the next round

```bash
python3 skills/embodied-ai-literature-hub/scripts/expand_via_citations.py \
  --seed-registry work/<run>/candidate-registry.json \
  --seed-status accepted --seed-status full-text-queued \
  --direction both \
  --output work/<run>/citation-candidates.json \
  --graph-output work/<run>/citation-graph.json \
  --dynamic-output work/<run>/citation-dynamic.json

python3 skills/embodied-ai-literature-hub/scripts/build_candidate_registry.py \
  --search-result work/<run>/round-1-arxiv.json \
  --citation-result work/<run>/citation-candidates.json \
  --output work/<run>/candidate-registry.json

python3 skills/embodied-ai-query-planner/scripts/build_query_plan.py \
  --topic "..." --knowledge-id EA-DATA \
  --dynamic-file work/<run>/citation-dynamic.json \
  --output work/<run>/query-plan-round-2.json
```

The third command feeds the terms mined from citation-expansion candidates back
into the planner as `tier: dynamic-association` queries; `coverage_group()`
automatically buckets them under `adjacent-and-transfer`, so re-running
`search_arxiv.py` against the round-2 plan produces properly labeled candidates
that *do* count toward `coverage_dimensions` — unlike the citation-graph
candidates themselves (see below).

To chase a second hop, take this round's `citation-candidates.json` `papers[]`
arXiv IDs and feed them back in as `--seed-id`/`--seed-id-file` for another
invocation. The script does not do this automatically — uncontrolled multi-hop
fan-out is exactly the explosion problem the coupling filter exists to avoid,
so each additional hop is a deliberate, visible decision.

## Epistemic boundaries

- Citation-graph discovery only produces **candidates**, exactly like the
  keyword/browser channels. They still need full-text recovery, six-pass
  reading, and a passing claim-support audit before anything in them can be
  cited as evidence. Nothing here is exempt from that gate.
- Semantic Scholar's index lags for very recent papers (days to a few weeks);
  a paper that should be a citing neighbor may simply not be indexed yet.
- `channel: "citation-graph"` candidates do not automatically satisfy any
  `coverage_dimensions` entry in the query plan (dimensions match on
  `query_labels` from the taxonomy, not on discovery channel). What eventually
  earns them dimension credit is the derived keywords being re-searched through
  the planner, as shown above. If you want citation-graph candidates to count
  directly, you would need to add a query-plan dimension keyed on the
  `citation:` label prefix yourself.
- `screen_candidates.py` has no native notion of "found by N independent
  sources." A zero-code-change proxy: each `(seed, direction)` pair produces its
  own `citation:<seed>:<direction>` query label, so running
  `screen_candidates.py --query-label-prefix citation:` already weights
  multiply-connected candidates higher through the existing
  `matched_query_labels` scoring — one match per connected seed.

## API key

Anonymous access works but is rate-limited more aggressively. If you have a
Semantic Scholar API key, pass `--api-key <key>` or set `S2_API_KEY` in the
environment; the script sends it as the `x-api-key` header. Retry/backoff
(including honoring `Retry-After` on 429s) is identical to `search_arxiv.py`'s,
so anonymous runs degrade gracefully rather than failing outright.
