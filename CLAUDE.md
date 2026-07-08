# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a Chinese-first **embodied-AI (具身智能) research knowledge base** paired with a three-skill
literature-review pipeline. Content is bilingual; prose, topic cards, and deliverables are primarily
in Chinese while code and CLI flags are English. `AGENTS.md` is the authority for context-loading
order — read it before loading knowledge files.

## Commands

The interpreter is `python3` (`python` is not on PATH). Scripts are **stdlib-only Python 3** — there
is no build, lint, install, or dependency step. Run any script with `--help` to see its contract.

Tests are stdlib `unittest` (network is mocked with `unittest.mock`; no live arXiv calls):

```bash
# Run one skill's suite (skill dirs are hyphenated, so scope discovery to the tests dir)
python3 -m unittest discover -s skills/embodied-ai-query-planner/tests -p 'test_*.py'

# Top-level knowledge-layer suite
python3 -m unittest discover -s tests -p 'test_*.py'

# Run a single test file directly
python3 skills/embodied-ai-literature-hub/tests/test_search_arxiv.py
```

Knowledge-base integrity and ID allocation (top-level `scripts/`):

```bash
python3 scripts/check_kb_links.py            # broken links, unregistered source IDs, line-number locators
python3 scripts/next_event_id.py --prefix EA-TWM-2026   # next collision-free evidence event ID
python3 scripts/check_run_bundle.py <run-dir>           # bundle completeness gate (pre-settle)
python3 scripts/audit_citations.py --article ... --appendix ... --evidence-jsonl ...   # citation gate
```

Note: repo-wide `unittest discover -s skills` finds **0 tests** — the hyphenated skill directories
are not importable packages and have no `__init__.py`. Always scope to a `*/tests` directory or a file.

Canonical literature-mining chain (see `embodied-ai-literature-hub/SKILL.md` for the full version).
`work/` is gitignored scratch — write intermediate artifacts there, not into the repo:

```bash
python3 skills/embodied-ai-query-planner/scripts/build_query_plan.py --topic "..." --family umi \
  --knowledge-id EA-DATA --output /tmp/plan.json --markdown-output /tmp/plan.md
python3 skills/embodied-ai-literature-hub/scripts/search_arxiv.py --query-file /tmp/plan.json \
  --start-date 2023-01-01 --end-date 2026-06-06 --output /tmp/candidates.json
python3 skills/embodied-ai-literature-hub/scripts/extract_arxiv_html.py --paper-id 2402.10329 --terms UMI,data
python3 skills/embodied-ai-literature-review/scripts/build_review_packet.py --topic "..." \
  --knowledge-id EA-DATA --evidence-jsonl /tmp/evidence.jsonl
```

## Architecture: the skill pipeline

Three skills under `skills/` form a strict one-directional pipeline (rationale in
`docs/adr/0001-separate-query-planning-from-literature-mining.md`). Each stage's responsibility
boundary is deliberate — do not blur them:

1. **`embodied-ai-query-planner`** — turns a topic into a structured query plan. Plans searches only;
   it never accepts papers as evidence or mines full text.
2. **`embodied-ai-literature-hub`** — consumes the plan, searches arXiv, mines HTML 正文, and emits
   evidence records. It owns no query taxonomy; it only consumes the planner's plan.
3. **`embodied-ai-literature-review`** — orchestrates `planner → hub → review packet → style menu` and
   synthesizes the final deliverable.

**Handoff contract (easy to get wrong):**
- The planner JSON keeps channels separate: `queries` (arXiv API) vs. `browser_fallback_queries` vs.
  `web_calibration_queries`. `search_arxiv.py --query-file` reads only the top-level `queries` entries.
- Planner `start_date`/`end_date` are **scope metadata only**. The actual date filtering is done by
  `search_arxiv.py --start-date/--end-date` — always pass those explicitly.
- `skills/embodied-ai-literature-hub/scripts/build_query_plan.py` is a **compat wrapper** that delegates
  to the planner's copy; new work should call the planner script directly.
- `build_review_packet.py` is a **briefing generator, not an author**: by default it writes
  `review-packet.md` + `writing-brief.md` + `evidence-appendix.md` into a new
  `work/literature-review-<topic>-<date>/` folder. The three prose deliverables
  (`scientific-memo_keyan.md` / `zhihu-explainer_zhihu.md` / `xiaohongshu-post_xiaohongshu.md`)
  are ALWAYS written by the agent from `writing-brief.md` as argument-organized prose — never
  ship the script's mechanical renders (`--emit-scaffold` produces bannered `*.scaffold.md` only).
  Use `--style survey` for the packet alone; `--select-event`/`--select-events-file` +
  `--consolidate-evidence` for targeted reuse of prior runs' evidence. Before settling a run into
  `evidence/`, two gates must pass: `scripts/check_run_bundle.py` (three styles or declared
  `style`+`scope_note` in run.json; self-contained evidence; standard manifest fields) and
  `scripts/audit_citations.py` (dead anchors, citations outside the loaded evidence, run.json drift).
  The `literature-review-<topic>-<date>` folder name IS the bundle contract trigger — non-review
  artifacts use a different naming.

## Knowledge base model

`knowledge/` is a routing + compression layer over a versioned evidence layer (see `docs/adr/0002-*`):
- **`evidence/`** is the source of truth for paper-level evidence and finished reviews. One folder per
  run (`literature-review-<topic>-<date>/`) with a `run.json` manifest. Accepted assets live here;
  candidates and intermediates stay in gitignored `work/`.
- **Retired raw documents** are archived in git history only — recover via the `git show <ref>:<file>`
  commands registered in `knowledge/sources.md`. Locators use semantic anchors (section titles, Q&A
  numbers), never line numbers.
- **Topic cards** (`knowledge/embodied-ai/*.md`, `knowledge/error-governance/*.md`) are compressed
  working memory — one topic per card, with `id`/`tags`/`source`/`load_when` frontmatter to preserve.
- **`knowledge/index.md`** is the routing layer: it maps user questions to stable IDs
  (`EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `ERR-PATTERN`, …) and the cards to load. Prefer loading cards
  over raw docs; open archives or `evidence/` only when exact wording or references are needed.

Add new material via `knowledge/ingestion-guide.md` (register source → extract to card → update index).
Run `python3 scripts/check_kb_links.py` after editing knowledge files.

## Conventions and invariants

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
- **Do not store full papers or full extracted text in the repo** — cache HTML outside it.
- **Skill layout convention:** each skill is `SKILL.md` + `scripts/` + `references/` + `tests/` +
  `agents/openai.yaml`. A new script gets a matching stdlib-only `unittest` file in the skill's `tests/`
  that loads the script via `importlib.util.spec_from_file_location`.
