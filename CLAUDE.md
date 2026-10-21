# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a Chinese-first **embodied-AI (具身智能) research knowledge base** paired with a three-skill
literature-review pipeline. Content is bilingual; prose, topic cards, and deliverables are primarily
in Chinese while code and CLI flags are English. `AGENTS.md` is the authority for context-loading
order — read it before loading knowledge files.

## Match the workflow to the question

Follow the request-routing table in `AGENTS.md` before selecting a skill. Continuing a discussion uses existing topic cards and selected notes; explaining one paper uses that paper's evidence or the paper-reader. Only a requested literature review/survey starts the full search, coverage, and publication pipeline. The commands below describe that formal pipeline, not the default response to every technical question.

## Commands

The interpreter is `python3` (`python` is not on PATH). Scripts are **stdlib-only Python 3** — there
is no build, lint, install, or dependency step. The full script map (purpose, categories,
relationships, workflows) lives in `scripts/README.md`. Run any script with `--help` to see its contract.
Optionally, `pip install .` (editable `-e .` also works) registers `extract_arxiv`,
`serve_research_wiki`, `run_review_pipeline`, `launch_review`, `quick_read_paper`,
`paper_slide_deck`, and `run_slide_deck`. The wheel is
**self-contained**: it bundles the three-skill tree (`SKILL.md`/references/agents/scripts, packaged
as `wiki_scripts.skills`), so an installed environment matches a repo checkout — path resolution
goes through `embodied_learning/utils/layout.py` (repo checkout vs site-packages), never `parent.parent`
guesses. The installed layout: the `wiki_scripts` package dir IS the scripts root and contains the
bundled `skills/`. Spawned headless `claude -p` agents (driver, writer, chat) run with
`cwd=<kb-root>` and an isolated `CLAUDE_CONFIG_DIR` (`~/.cache/embodied-learning/claude-config`,
credentials auto-seeded) so they cannot read the launching session's memory or any repo —
see `embodied_learning/harness/claude.py` (`isolated_claude_env` / `claude_auth_ready`).
`wiki.py serve` (console script `serve_research_wiki`) serves the local research Wiki and defaults to the local knowledge base at
`~/Documents/arxiv` (override with `--kb-root`; falls back to the repo catalog). Install is not
required for any pipeline step.

Tests are stdlib `unittest` (network is mocked with `unittest.mock`; no live arXiv calls).
The Makefile mirrors the CI discovery list in `.github/workflows/research-validation.yml`:

```bash
make test                 # same suites as research-validation CI
make test-knowledge       # top-level tests/ only
make validate             # scripts/run.py validate-reviews (needs full git history)

# Run one skill's suite (skill dirs are hyphenated, so scope discovery to the tests dir)
python3 -m unittest discover -s skills/embodied-ai-literature-hub/tests -p 'test_*.py'

# Top-level knowledge-layer suite
python3 -m unittest discover -s tests -p 'test_*.py'

# Run a single test file directly
python3 skills/embodied-ai-literature-hub/tests/test_search.py  # see test file for usage
```

Knowledge-base integrity and ID allocation (top-level `scripts/`):

```bash
python3 scripts/wiki.py check-kb-links            # broken links, unregistered source IDs, line-number locators
python3 scripts/wiki.py kb-stats [--kb-root ...] [--json] [--runs-detail]   # inventory: runs, pool full-text/deep-read, wiki topics (docs/kb-inventory.md)
python3 scripts/wiki.py kb-search "query" [--scope all|runs|papers|events|topics] [--limit N]   # substring search across the KB
python3 scripts/wiki.py kb-funnel [--layer registry|screened|full_text|deep_read|evidence|abstract] [--run NAME] [--sort ...] [--limit N] [--json]   # retrieval→evidence funnel per run, or the papers in one layer (published funnel.json)
python3 scripts/wiki.py kb-merge --kb-root <target> --source <src> [--source ...] [--dry-run]   # fold runs/pool/cards/slugs into target (newer wins; docs/kb-inventory.md)
python3 scripts/run.py next-event-id --prefix EA-TWM-2026   # next collision-free evidence event ID
python3 scripts/run.py init --topic "..." --knowledge-id EA-...   # run birth certificate (status: in-progress)
python3 scripts/run.py pipeline --run-dir <run-dir> --topic "..." --review-mode ...   # mechanical stages driver: plan -> retrieval -> registry -> screening -> coverage -> extraction -> packets -> deep read (skeleton agents; seeds forced to the front, limit mode-aware: rapid 12 / scoping 22 / systematic 43) -> projection (stamps run.json event_count/evidence_papers) -> funnel.json (six-layer retrieval funnel, published by finalize) -> pipeline-summary.json; idempotent/resumable; --skip-deep-read hands deep reading to an external orchestrator
python3 scripts/run.py check-bundle <run-dir> --pre-settle   # bundle completeness gate (writer stage: run is still in-progress; the bare form is finalize's post-flip re-check)
python3 scripts/run.py audit-citations --article ... --appendix ... --evidence-jsonl ...   # citation gate
python3 scripts/run.py finalize --run-dir <run-dir> --kb-root <kb-root>   # mechanical settle: stamp run.json fields -> cited-paper floor gate (rapid 6 / scoping 10 / systematic 15 distinct papers) -> both gates -> publish evidence/ -> settled -> catalog row -> wiki snapshot
python3 scripts/run.py status --run-dir <run-dir>   # one-shot run digest (funnel, per-paper evidence + References metadata, artifact checklist, next commands) — agents read this instead of looping over evidence/*.jsonl
```

**Literature review runs are driver-first.** Default to `scripts/run.py pipeline` for every
mechanical stage instead of hand-running search/extraction/deep-read steps (it encodes rate-limit
degradation, dynamic-query merging, and skeleton-agent deep reading). Claude sessions own only the
judgment stages (packet via `write.py review-packet --run-dir` → writing → audit gates →
`run.py finalize`) and run them **in one turn** — no outline stop-and-wait checkpoint; the only
sanctioned early stop is retrieval failure or insufficient evidence (leave the run `in-progress`
and say what is missing) — a gate failure is a fix-and-rerun condition, never a stop. Settling a
run is not the last step: `run.py finalize` performs publish + catalog registration + wiki
snapshot rebuild (`scripts/wiki.py build-wiki --kb-root <kb-root> --output
<kb-root>/wiki/data`); runs may also be registered by hand in `knowledge/literature-review-catalog.md`
(or the local KB's catalog, e.g. `~/Documents/arxiv/knowledge/literature-review-catalog.md` for
LiDAR/SLAM/calibration topics) — an unregistered run is invisible in the wiki.

**Post-settle revisions are additive versions.** The wiki topic chat's 修订成稿 toggle (`POST
/api/topic/revise`) regenerates one deliverable as `evidence/<run>/revisions/<style>-v<N>.md`
(file numbering: base deliverable = v0, first revision = v1; provenance in `revisions/index.json`,
written by the server only). The snapshot builder publishes each revision as its own version key
(`keyan-v1`) ordered after its base style, and labels the whole per-style chain **chronologically**
(`v0` = oldest — a superseded 第N轮综述 run or the base — then newer revisions); `latest_version`
is the landing version a reader opens, so the default is never a stale `v0`. The base deliverables,
`run.json`, `trace-map.json`, and `evidence-appendix.md` are never edited. Revisions use the run's
existing evidence set only.

Note: repo-wide `unittest discover -s skills` finds **0 tests** — the hyphenated skill directories
are not importable packages and have no `__init__.py`. Always scope to a `*/tests` directory or a file.

Canonical literature-mining chain (see `embodied-ai-literature-hub/SKILL.md` for the full version).
`work/` is gitignored scratch — write intermediate artifacts there, not into the repo:

```bash
python3 skills/embodied-ai-literature-hub/scripts/search.py build-query-plan --topic "..." --family umi \
  --knowledge-id EA-DATA --output /tmp/plan.json --markdown-output /tmp/plan.md
python3 skills/embodied-ai-literature-hub/scripts/search.py search-semantic-scholar --query-file /tmp/plan.json \
  --start-date 2023-01-01 --end-date 2026-06-06 --output /tmp/s2-candidates.json   # default metadata-search backend
python3 skills/embodied-ai-literature-hub/scripts/search.py search-arxiv --query-file /tmp/plan.json \
  --start-date 2023-01-01 --end-date 2026-06-06 --output /tmp/candidates.json
# Offline retrieval (no network): pass --metadata-snapshot with an OAI JSONL snapshot, or a
# SQLite/FTS5 database built once via `search.py build-snapshot-db --snapshot-jsonl <jsonl> --db <db>`
# (seconds per round vs minutes; db at ~/Documents/arxiv/arxiv-metadata-oai-snapshot.sqlite).
# run.py pipeline forwards the same choice as --arxiv-snapshot.
python3 skills/embodied-ai-literature-hub/scripts/search.py build-candidate-registry \
  --semantic-scholar-result /tmp/s2-candidates.json --search-result /tmp/candidates.json --output work/<run>/registry.json
python3 skills/embodied-ai-literature-hub/scripts/fetch.py extract-arxiv-html --paper-id 2402.10329 --terms UMI,data
# Markdown tier (default arxiv2md transport: public REST API via curl, no credentials;
# `--transport s3-tex` = S3 tarball + pandoc, TODO pending AWS credentials — requester-pays bucket)
python3 skills/embodied-ai-literature-hub/scripts/fetch.py extract-content --paper-id 2402.10329 \
  --terms UMI,data --preferred-source auto --include-full-text --output /tmp/extraction.json
python3 skills/embodied-ai-review-writer/scripts/write.py review-packet --topic "..." \
  --knowledge-id EA-DATA --evidence-jsonl /tmp/evidence.jsonl
# Local public paper pool (default ~/Documents/arxiv/pool, outside the repo): one folder per paper
python3 skills/embodied-ai-paper-reader/scripts/read.py pool-add-paper add --extraction /tmp/extraction.json
# Single-paper quick-read card (速读): ensures pooled + deep-read, then writes
# quick-read_sudu.md into the pool dir (wiki reader 速读 tab browses it)
python3 skills/embodied-ai-paper-reader/scripts/read.py quick-read --arxiv-id 2302.01109
```

The paper pool is a local store outside the repository (`~/Documents/arxiv/pool` by default) where
each paper owns one folder keyed by unique ID (`arxiv-<id>/` with `paper.md`, `extraction.json`,
`note.md`, `meta.json`). Topic cards may cite pool papers with a `POOL-<...>` frontmatter `source`
entry carrying an absolute `file:` path and a semantic-anchor `locator`; `scripts/wiki.py check-kb-links`
validates the file exists without requiring `sources.md` registration.

## Architecture: the skill pipeline

Three skills under `skills/` form a strict one-directional pipeline (rationale in
`docs/adr/0003-consolidate-to-three-skills.md`). Each stage's responsibility boundary is
deliberate — do not blur them:

1. **`embodied-ai-literature-hub`** (检索) — plans queries (in-skill `search.py build-query-plan` stage),
   searches arXiv/Semantic Scholar, triages candidates (influence, problem relevance), mines HTML
   正文, and emits evidence records. It plans and mines only; it never writes reader-facing prose.
2. **`embodied-ai-paper-reader`** (阅读) — deep-reads recovered full text, verifies claims, projects
   evidence events.
3. **`embodied-ai-review-writer`** (写作) — owns the review end to end: orchestrates
   `hub → reader → review packet → writing brief` and synthesizes the final deliverable.

**Handoff contract (easy to get wrong):**
- The planner JSON keeps channels separate: `queries` (arXiv API) vs. `browser_fallback_queries` vs.
  `web_calibration_queries`. `search.py search-arxiv --query-file` reads only the top-level `queries` entries.
- Planner `start_date`/`end_date` are **scope metadata only**. The actual date filtering is done by
  `search.py search-arxiv --start-date/--end-date` — always pass those explicitly.
- Query planning is a stage inside `$embodied-ai-literature-hub`
  (`skills/embodied-ai-literature-hub/scripts/search.py build-query-plan`).
- `write.py review-packet` is a **briefing generator, not an author**: by default it writes
  `review-packet.md` + `writing-brief.md` + `evidence-appendix.md` into a new
  `work/literature-review-<topic>-<date>/` folder. The three prose deliverables
  (`scientific-memo_keyan.md` / `zhihu-explainer_zhihu.md` / `xiaohongshu-post_xiaohongshu.md`)
  are ALWAYS written by the agent from `writing-brief.md` as argument-organized prose — never
  ship the script's mechanical renders (`--emit-scaffold` produces bannered `*.scaffold.md` only).
  Use `--style survey` for the packet alone; `--select-event`/`--select-events-file` +
  `--consolidate-evidence` for targeted reuse of prior runs' evidence. Before settling a run into
  `evidence/`, two gates must pass: `scripts/run.py check-bundle --pre-settle` (three styles or declared
  `style`+`scope_note` in run.json; self-contained evidence; standard manifest fields; `--pre-settle`
  because the run is still `in-progress` — never hand-flip the status) and
  `scripts/run.py audit-citations` (dead anchors, citations outside the loaded evidence, run.json drift).
  The `literature-review-<topic>-<date>` folder name IS the bundle contract trigger — non-review
  artifacts use a different naming.

## Knowledge base model

`knowledge/` is a routing + compression layer over a versioned evidence layer (see `docs/adr/0002-*`):
- **`evidence/`** is the source of truth for paper-level evidence and finished reviews. One folder per
  run (`literature-review-<topic>-<date>/`) with a `run.json` manifest. Accepted assets live here;
  candidates and intermediates stay in gitignored `work/`.
- **Retired raw documents** are archived in git history only — recover via the `git show <ref>:<file>`
  commands registered in `knowledge/sources.md`. Locators use semantic anchors (section titles, Q&A
  numbers), never line numbers. Archive-aware checks (`wiki.py check-kb-links`, `run.py validate-reviews`)
  therefore need a **full-history clone** (not `git clone --depth 1`). Shallow clones get a clear
  early error; deepen with `git fetch --unshallow` before re-running validation.
- **Topic cards** (`knowledge/embodied-ai/*.md`, `knowledge/error-governance/*.md`) are compressed
  working memory — one topic per card, with `id`/`tags`/`source`/`load_when` frontmatter to preserve.
- **`knowledge/index.md`** is the routing layer: it maps user questions to stable IDs
  (`EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `ERR-PATTERN`, …) and the cards to load. Prefer loading cards
  over raw docs; open archives or `evidence/` only when exact wording or references are needed.

Add new material via `knowledge/ingestion-guide.md` (register source → extract to card → update index).
Run `python3 scripts/wiki.py check-kb-links` after editing knowledge files.

**Local KB first (`~/Documents/arxiv`).** The canonical working knowledge base is the local KB at
`~/Documents/arxiv` (its own `knowledge/`, `evidence/`, `pool/`, `work/`); two KB roots exist and
topics choose the root (e.g. LiDAR/SLAM/calibration topics are already local-KB only). New
knowledge outputs — settled runs, topic cards, pool papers, deep-read notes, wiki snapshots — are
work content and belong in the local KB; when the in-repo `knowledge/` tree and the local KB
disagree, prefer the local KB. The repo (and the `local-db` branch in particular) records **code
changes only**; never commit knowledge-bearing artifacts here (`pool/` is gitignored as a guard —
a pool dir inside the repo is a mis-resolved default, migrate it out and delete it).

## Token / context soft guards

- Load `AGENTS.md` + the **current** skill `SKILL.md` only; pull `references/` per step. Do not preload the full `knowledge/literature-review-catalog.md` — grep relevant rows.
- Never dump `candidate-registry.json` into the model; use coverage reports / title-only slices (`search.py registry-titles`).
- Prefer `read.py build-reading-packet --summary-first` for scoping; full text stays on disk for locator audits.
- `write.py review-packet` stance-caps writer brief/appendix (default support 8 / limit 6 / conditional 6 / gap 4); pass `--uncapped-writer` only for debug.
- Optional metering: `EMBODIED_TOKEN_METER=1` + `scripts/run.py token-meter` → `work/<run>/token-meter.jsonl` (see `docs/token-meter.md`).

## Conventions and invariants

- **The library has no CLI, no prompt text, and no policy constants** (docs/adr/0005).
  `embodied_learning/**` exposes exactly `run(args: argparse.Namespace) -> int` — no
  `parse_args`, no `main`, no `if __name__`. The six dispatchers
  (`scripts/{run,wiki}.py`, `skills/*/scripts/{search,fetch,read,write}.py`) own every
  argparse flag table and argv/exit-code plumbing. LLM prompt wording lives only in
  `embodied_learning/harness/prompt.py`; tunable policy knobs (limits, timeouts, thresholds,
  budgets) live only in `embodied_learning/config.py`. Flag strings, prompt wording and
  constant values are contracts — moving them is not a license to edit them.
- **All model-capability calls go through `embodied_learning/harness/claude.py`** (pybind-style
  binding layer). Feature modules keep prompts and output parsing; the harness owns CLI discovery,
  spawn-environment isolation, auth preflight, one-shot `complete()`, streaming `ChatTurn`, and the
  machine-local conversation archive (`~/.claude/projects/embodied-learning-work/`). Never spawn
  `claude` via `subprocess` anywhere else — there is no bypass shim; everything goes through the
  harness.
- **Shared-KB concurrency is O_EXCL-based, never flock.** The KB may live on a CIFS mount shared by
  several machines; all cross-process coordination lives under `<kb-root>/.locks/` (owner-record
  lock files created with `O_CREAT|O_EXCL`, stale-steal via a fixed `.steal` marker) and
  `<kb-root>/.claims/` (event-ID prefix reservations). Never use `fcntl.flock` for a KB resource
  (unreliable across CIFS clients; `ratelimit.py`'s flock gate is machine-local request pacing
  only). Lock ONLY the read-merge-rewrite of shared files (`pool/index.jsonl`, catalog,
  run.json, chat-sessions.json, wiki publish, cold-start bootstrap); per-run outputs
  (`work/<run>/`, `evidence/<run>/`) stay lock-free. Every rewrite of a shared file goes through
  `embodied_learning/atomicio.py` (tmp + `os.replace`). Knobs:
  `EMBODIED_KB_LOCK_{DIR,WAIT,STALE,POLL}` / `EMBODIED_KB_LOCKS_DISABLED=1` (emergency no-op).
  Details in `scripts/README.md` (「共享知识库的并发与锁」).
- **Evidence discipline is the core invariant.** Candidate papers are never accepted evidence.
  Browser/web/social results are low-confidence *calibration* only and must not be promoted to
  evidence; promote a claim only after arXiv HTML 正文 verification.
- **Fixed label vocabularies — preserve them exactly.** Stance: `support` / `limit` / `conditional` /
  `gap`. Confidence: `direct` / `citation-supported` / `inference`. Mark cross-event synthesis as
  `inference` explicitly.
- **Author/institution tracking is conservative.** Record first-level org only (e.g. `北京大学`,
  `Google`); no departments/labs. Use `institutions: []` when the mapping is unreliable, and do not
  merge same-name authors without stronger evidence.
- **Topic-card edits are suggestions** unless the user explicitly asks to edit the knowledge base.
- **Do not store full papers or full extracted text in the repo** — cache HTML/tarballs outside it. The
  one sanctioned full-text store is the **local public paper pool outside the repository**
  (`~/Documents/arxiv/pool`, managed by `read.py pool-add-paper`), which the repo references but never contains.
- **Skill layout convention:** each skill is `SKILL.md` + `scripts/` + `references/` + `tests/` +
  `agents/openai.yaml`. A new script gets a matching stdlib-only `unittest` file in the skill's `tests/`
  that loads the script via `importlib.util.spec_from_file_location`. Shared arXiv data-processing
  logic lives in `embodied_learning/<search|fetch|parse|knowledge>/`; `scripts/` files are thin entry points
  that bootstrap the repo root and import from `embodied_learning.*`.
