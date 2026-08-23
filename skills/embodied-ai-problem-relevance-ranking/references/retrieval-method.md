# Retrieval Method (the "regular method")

`rank_problem_relevance.py` filters the fetched corpus to `--target-retrieved` papers with
a **sparse lexical retriever** — Okapi BM25 — and, for each surviving paper, emits an
**explanation** of its relevance. This is the RAG retrieval step: the questions are the
query, each paper is a document, and the retriever scores how well each document answers
the query.

## Why BM25, not dense embeddings

The repo is **stdlib-only Python 3** — no torch, no sentence-transformers, no model
weights. Dense embedding retrieval is out of scope. BM25 is deterministic, needs no
weights, and is *explainable*: every point of score is traceable to a specific
term-in-field match, which is exactly what "explain relevance to the task" requires. A
dense vector would give a number but no reason.

## Document model: a paper is a multi-field document

Each paper is scored over four fields, with a weight per field
(`--field-weights`, default `title=2.0,abstract=1.0,introduction=1.5,related_work=1.5`):

| Field | Weight | Why |
|---|---|---|
| `title` | 2.0 | Strongest, shortest signal — a title that names the problem is decisive. |
| `introduction` | 1.5 | States the problem being solved and the motivation, so "does this paper address my question" lives here. |
| `related_work` | 1.5 | Positions the paper against prior methods — the section that tells you *how* (and against what) the paper does the thing. |
| `abstract` | 1.0 | Summary; present but diluted, so it weights less than the sections that actually explain. |

The two sections that most reliably state *how* the paper relates to the question
(introduction, related-work) weight above the abstract — that is the point of fetching
full text rather than metadata alone.

## Scoring: Okapi BM25

For one query term in one field:

```
idf        = log((N − df + 0.5) / (df + 0.5) + 1)
norm       = tf·(k1+1) / (tf + k1·(1 − b + b·(len/avg_len)))
score(f)   = idf · norm
```

- `N` = corpus size; `df` = number of docs where the term appears in that field;
  `tf` = term count in that field; `len`/`avg_len` = field length vs. the corpus average.
- `k1 = 1.5`, `b = 0.75` (Okapi defaults). `idf` up-weights *rare* terms (a term that only
  appears in a handful of papers is a sharper signal); the `b` length term stops long
  fields from winning just by being long.
- A paper's score for one question = `Σ_field field_weight · BM25(field)`.
- **Ranking**: `retrieval_score = max` over questions (a paper is as relevant as its best
  question); `retrieval_score_sum` is reported as a secondary signal, not the sort key.

The tokenizer lowercases, keeps hyphenated compounds, and emits both `multi-view` and
`multiview` (and `ego-exo` / `egoexo`) so common spelling variants match without a
stemmer. It drops function words and tokens shorter than three characters.

## The explanation: showing relevance, not asserting it

For every retrieved paper, `--markdown-output` carries an explanation per question:

- the top contributing **terms** (aggregated by concept — `multi-view` and `multiview`
  merge onto the hyphenated form),
- the **fields** each term matched in and its contribution,
- a **snippet** from the highest-contribution field, so you can see *where* the claim of
  relevance lives.

A paper whose explanation shows "camera" and "calibration" matching in `related_work` with
a snippet about camera placement is a very different signal from one whose abstract merely
contains the word "camera" once.

## Limits of lexical retrieval — and where the reader corrects them

- **Synonymy.** The query is the literal question text. A paper that solves "first↔third
  alignment" but calls it "cross-view registration" or "ego-exo pose alignment" will be
  under-scored if those exact words are absent. The questions you pass in should name the
  variants you care about (`--question "…align first and third person views / ego-exo
  correspondence / cross-view registration"`).
- **Mentions vs. solves.** BM25 cannot tell a paper that *mentions* "camera calibration"
  in passing from one whose Method section does it. This is the single biggest reason the
  retriever's job ends at ~50: stage 3 (reading the surfaces) and stage 4 (full-text
  reading) exist precisely to close this gap.
- **Section scope.** Only abstract / introduction / related-work are scored. A paper may
  put its camera-initialization detail in a Method/Implementation section and never say so
  in the scored surface; that paper is a false negative the retriever cannot see.
- **Hyphen variants** are emitted separately in the *per-question matched terms* JSON
  (for an auditable trace), but merged in the *explanation* display to keep it readable.

None of this is a reason to distrust the retriever; it is the reason the retriever is
deliberately only stage 2 of the funnel, not the final verdict.
