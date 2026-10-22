# 0004. Unify entry dispatchers and sink all logic into the library

Date: 2026-10-12
Status: Accepted

## Context

Before this decision the repository carried ~47 entry scripts across `scripts/`
(25) and `skills/*/scripts/` (23), with the same capability often implemented
several times: HTTP retry policy ×5, `normalize_arxiv_id` ×6, `load_json` ×9,
`parse_frontmatter` ×4, `event_anchor` ×3, `slugify_topic` ×2 (the
`literature-review-<topic>-<date>` folder contract), two `emit()` variants, and
three single-paper pipeline skeletons. Entry shapes were inconsistent (one
13-subcommand dispatcher next to a field of flat-flag scripts), so a fix landed
in one entry rarely reached its siblings. A dual-import shim
(`try: from lib.X except: from wiki_scripts.lib.X`) had spread across ~21 files
to paper over the three module roots (`embodied_learning`, `hub_scripts`,
`wiki_scripts`). Tests loaded scripts via `importlib.util.spec_from_file_location`
and patched module globals, binding them to file paths.

## Decision

1. **Six domain dispatchers**, each an argparse `_SUBCOMMANDS` table over the
   library (the hub's `search.py` pattern, generalized):

   | Dispatcher | Domain | Subcommands |
   |---|---|---|
   | `scripts/run.py` | run lifecycle / gates / orchestration | 12 |
   | `scripts/wiki.py` | publishing / serving | 6 |
   | `skills/.../hub/scripts/search.py` | retrieval | 17 |
   | `skills/.../hub/scripts/fetch.py` | full-text acquisition | 8 |
   | `skills/.../reader/scripts/read.py` | reading stages | 10 |
   | `skills/.../writer/scripts/write.py` | writing + editorial audit | 10 |

   Historical command names survive as `pyproject [project.scripts]` aliases
   (`extract_arxiv`, `serve_research_wiki`, `run_review_pipeline`,
   `launch_review`, `quick_read_paper`, `paper_slide_deck`, `run_slide_deck`)
   implemented as `*_main()` functions that prepend their subcommand.

2. **All business logic lives in `embodied_learning/`**; entries own only
   argument parsing and dispatch. New packages (minimal, deliberately):

   - `wiki/` — run lifecycle and publishing in one package, files split into
     two groups: `wiki/run/` (manifest, driver, launcher, finalize, catalog,
     gates, status, events, validate, meter) and `wiki/publish/` (snapshot,
     site, knowledge_map, mind_omni, links, server, chat, markdown).
     Rationale: both concerns are "the review-run workflow around the data
     layers", and one package keeps the run→publish call graph internal.
     Rejected: `run/`+`site/` as separate top-level packages (two roots for
     one workflow); `lifecycle/`/`pipeline/` (too narrow for settle/publish).
   - `writer/` — deliverable rendering and editorial audit in one domain
     (`packet`, `quality`, `trace_map`, `zhihu_corpus`, `slide_audit`,
     `slide_compile`, `budget`, `outline`, `deck`, `run_deck`).
     **Every writing path is gated by its audit** — generation and audit are
     one domain by design. Rejected: `review/` (clashes with "literature
     review" the run domain); `writing/` (too close to `write.py`).
   - `utils/` — misc shared helpers: `jsonio`, `frontmatter`, `arxiv_id`,
     `layout`, `git_history`.
   - `harness/prompt.py` — every LLM prompt template in one place (the
     repo-wide form of workflow-prompt-single-source). Wording is contract;
     moves are verbatim.
   - `config.py` — constants and review-mode default parameters: evidence
     floors (8/15/30), cited-paper floors (6/10/15), screen/deep-read limits,
     stance caps, style contracts, agent timeouts.

   `scripts/lib/` is dissolved: `layout.py`/`git_history.py` rose into
   `utils/`, `review_runs.py` split into `wiki/run/catalog.py` +
   `knowledge/evidence.py` + `config.py`, `markdown_semantics.py` into
   `wiki/publish/markdown.py`; `jsonio.py`/`agent_invoke.py` were compatibility
   shims and are deleted.

3. **One-shot cutover, no shims.** Old entry files are deleted in the same
   change that repoints every caller (driver/launcher/finalize/server spawn
   tables, CI workflows, Makefile, `pyproject.toml`, `.command` launcher,
   tests). During migration the old files briefly existed as thin forwarders;
   they are gone now.

4. **Tests load implementation modules** (`importlib.import_module`) so
   `mock.patch` on module attributes reaches the live globals; dispatchers
   keep working under bare `spec_from_file_location` (they import only stdlib
   + `embodied_learning.*`).

## Consequences

- The three-module-root comment in `pyproject.toml` is superseded by this ADR;
  `hub_scripts` packaging is extended to `reader_scripts`/`writer_scripts`.
- Spawn paths are a compatibility surface: `SKILL.md`, workflow prompts and CI
  must move together. Filename tokens inside prompts were updated; wording was
  not.
- Old filenames (`finalize_run.py`, `build_review_packet.py`, `writing_audit.py`,
  …) no longer exist. Historical run metadata is never rewritten; the §1
  disposition table in the refactor plan is the archaeology map.
- `make test` covers the same four suites as CI (tests + three skill test
  dirs); `make validate` runs `scripts/run.py validate-reviews`.
- If `wiki/` grows too large, split `wiki/run/` into a top-level package later
  — the group boundary is already the module boundary.

## Supersedes / relates to

- Supplements [0003](0003-consolidate-to-three-skills.md) (skill structure)
  and [0002](0002-retire-raw-sources-promote-evidence-layer.md) (evidence
  layer); supersedes no prior ADR. The single-source prompt convention
  (workflow-prompt-single-source) is generalized here to `harness/prompt.py`.
