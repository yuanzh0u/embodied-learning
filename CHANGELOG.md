# CHANGELOG

## 0.1.0 (20261015)
1. evidence-first research hub: literature review pipeline with claim-support audits and bounded conclusions
2. three-skill consolidation (literature-hub / paper-reader / review-writer) and six-domain dispatchers (`run.py` / `wiki.py` / `search.py` / `fetch.py` / `read.py` / `write.py`)
3. `embodied_learning` library package with no CLI, no prompts and no policy knobs (ADR 0005)
4. headless end-to-end review launcher (`run.py launch`) and mechanical stage driver (`run.py pipeline`) with loud timeout budgets
5. offline arXiv retrieval from an OAI metadata snapshot plus SQLite/FTS5 index
6. candidate selection strategies — `smart-jev` (default; System One jev decision model via `EMBODIED_SYSTEM_ONE_*`), `smart`, `keywords`, `influence`, `bm25` — and abstract-tier evidence
7. multi-round retrieval with measured saturation and mode-aware evidence floors
8. figure and table evidence through deep read into the written deliverables
9. single-paper quick-read cards (速读) and reveal.js slide decks (汇报)
10. per-style article revisions with version switching
11. self-contained wheel that bundles the skills tree and isolates spawned `claude` agents
12. CIFS-safe shared-KB locking (O_EXCL + atomic writes + append-only journal)
13. machine-wide arXiv/Semantic Scholar request gate with 429 backoff and shared full-text cache
14. research Wiki with workflow dialog, paper chat, live progress and atomic snapshots
15. crawlable static research site: per-topic canonical pages, sitemap, robots, `llms.txt`, JSON-LD and noindex PR previews
16. card-level evidence projection with a table-aware quantitative gate
17. retrieval→evidence funnel per run (`funnel.json`, six layers) with `kb-stats` / `kb-search` / `kb-funnel` / `kb-merge`
