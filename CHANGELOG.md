# CHANGELOG

## 0.1.0 (20261015)
1. evidence-first research hub: literature review pipeline with claim-support audits and bounded conclusions
2. three-skill consolidation (literature-hub / paper-reader / review-writer) and six-domain dispatchers (`run.py` / `wiki.py` / `search.py` / `fetch.py` / `read.py` / `write.py`)
3. `embodied_learning` library package with no CLI, no prompts and no policy knobs (ADR 0005)
4. headless end-to-end review launcher (`run.py launch`) and mechanical stage driver (`run.py pipeline`)
5. offline arXiv retrieval from an OAI metadata snapshot plus SQLite/FTS5 index
6. smart / influence / keywords / bm25 candidate selection strategies and abstract-tier evidence
7. multi-round retrieval with measured saturation and mode-aware evidence floors
8. figure and table evidence through deep read into the written deliverables
9. single-paper quick-read cards (速读) and reveal.js slide decks (汇报)
10. per-style article revisions with version switching and superseded-run rounds
11. self-contained wheel that bundles the skills tree and isolates spawned `claude` agents
12. CIFS-safe shared-KB locking (O_EXCL + atomic writes + append-only journal)
13. machine-wide arXiv/Semantic Scholar request gate with 429 backoff
14. research Wiki with workflow dialog, paper chat, live progress and atomic snapshots
15. crawlable static research site: per-topic canonical pages, sitemap, robots, `llms.txt`, JSON-LD and noindex PR previews
16. card-level evidence projection with a table-aware quantitative gate
17. loud, configurable agent/subprocess timeout budgets throughout the pipeline
18. publishable retrieval→evidence funnel (`funnel.json` per run, six layers with selection reasons; `kb-stats` summary + `kb-funnel` run/layer queries)
19. abstract-tier evidence scoped to the selection result (`screening-ids.txt`) instead of the raw candidate registry
20. `smart-jev` selection strategy: a System One (jev) decision-model binding in the harness (`judge_questions`, `POST /v1/systemone`, Noul per-paper probabilities) alongside the execution-model `smart` strategy; the interview card exposes both as parallel options; the strict "core contribution directly addresses the topic" wording lifts jev precision 59.5% → 80.0% at threshold 0.60
21. extraction throughput: the machine-wide gate reserves a slot under the lock and sleeps after releasing it (concurrent fetch workers no longer serialize); fetch calls pass `max_wait` so a 429 cooldown becomes a fast retryable HELD instead of a 600s hard timeout; the cooldown cap drops to 120s; full text is cached under `<kb-root>/.cache` for cross-run/cross-machine reuse; hard-timeout checkpoints keep the extractor's stderr tail
22. default deep-read selection is now `smart-jev` (`DEFAULT_SELECTION_STRATEGY` in `config.py`, applied by `run.py pipeline`/`launch`, the Wiki kickoff and the interview card). It fails fast before retrieval when the System One channel is unconfigured (`EMBODIED_SYSTEM_ONE_URL` / `EMBODIED_SYSTEM_ONE_API_KEY` or their `ANTHROPIC_*` fallbacks); pass `--selection-strategy smart` to run the execution-model pass instead
