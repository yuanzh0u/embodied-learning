# 0005. The library has no CLI, no prompt text, and no policy constants

Date: 2026-10-13
Status: Accepted

## Context

ADR [0004](0004-unify-entry-dispatchers.md) merged 47 entry scripts into 6
domain dispatchers and sank all business logic into `embodied_learning/`. That
step **moved code**; it did not draw the boundary. Reviewing the result found
three leaks:

1. **The library ate argv.** 67 `parse_args()`/`main()` pairs across 39
   library modules. The dispatchers reached them with
   `sys.argv = [name, *rest]; mod.main()` — argparse, exit codes and even
   `sys.stdout.reconfigure` lived below the line. Roughly half the
   `parse_args()` took no argv parameter at all, which is *why* the dispatchers
   mutated `sys.argv`.
2. **Prompt text was scattered.** Ten files held LLM prompt templates and
   their builders (`quick_read.build_agent_prompt`, `deck.build_agent_prompt`,
   `selection.SMART_PROMPT_TEMPLATE`, `driver.TERMS_PROMPT`,
   `chat.py`'s whole workflow/paper-chat/revision surface).
3. **Policy constants were copy-pasted.** 481 module-level constants, of which
   ~58 scalar knobs and 10 policy tables are things an operator would tune
   (`MAX_TERM_MATCHES`, `CHANNEL_DOWN_LIMIT`, floors, timeouts, retry budgets).
   Four were verbatim duplicates (`STOP_GRACE_S` ×2, `TRANSIENT_HTTP_CODES` ×2,
   `MAX_TERM_MATCHES` ×2, `status.CITED_PAPER_FLOORS` duplicating `config.py`).

## Decision

The library is a pure business layer. Three single sources, one each:

| Concern | Home | Library modules expose |
|---|---|---|
| argv, flag tables, exit-code plumbing | the 6 dispatchers (`scripts/{run,wiki}.py`, `skills/*/scripts/{search,fetch,read,write}.py`) | `run(args: argparse.Namespace) -> int` |
| LLM prompt wording + pure prompt builders | `embodied_learning/harness/prompt.py` | `*_prompt(...)` functions returning strings |
| tunable policy knobs and tables | `embodied_learning/config.py` | imported names |

Concretely:

- **No `parse_args`, no `main`, no `if __name__` in `embodied_learning/`.**
  Every module exposes exactly `run(args) -> int`. `argparse` appears only as
  a `Namespace` type annotation.
- **Each dispatcher owns a `PARSERS` table** mapping subcommand → parser
  builder. `description=<module>.__doc__` keeps `--help` output byte-identical
  to the pre-merge scripts; `parser.prog = <subcommand>` keeps the usage line
  identical. Flag strings, `choices`, and help text are copied **verbatim**.
- **Process-level side effects live in the dispatcher** (`sys.stdout.reconfigure`,
  `print` of user-facing output routing, `sys.exit`). `run()` returns an exit
  code and does the work.
- **`harness/prompt.py` owns every prompt string.** Feature modules assemble
  inputs and call the builders; `chat.py` keeps session registry, HTTP glue,
  SSE, and output-marker parsing. The publisher fork (one base system prompt,
  `agent`/`launcher` tails, three fork points) is preserved verbatim.
- **`config.py` owns every tunable knob**: extraction caps, network retry and
  pacing, agent/chat timeouts, ranking thresholds, writing budgets, rendering
  caps, lock patience. Compiled regexes, tag sets, lookup tables that document
  structure, and path derivations stay next to the code that interprets them.

### Rejected

- **Keeping `build_parser()` in the library.** Removes `parse_args`/`main` by
  name but leaves `argparse` in the business layer; the boundary is the point.
- **A `cli/` package inside the library.** Business and CLI parsing both live
  in the library, just split — same leak, one level deeper.
- **Sinking every constant, including regexes and lookup tables.** `config.py`
  becomes a grab-bag and structural constants lose their interpretive context.
- **Shims keeping `mod.main()` working.** One-shot cutover, like 0004.

## Consequences

- Tests that called `mod.main([...])` go through `tests/_entry.py`
  (`invoke(entry, subcommand, argv)` / `parse(...)`), which builds the
  dispatcher's parser and calls `mod.run(args)`. `mock.patch.object(mod, …)`
  on module globals is unchanged — the module object is the same one the
  dispatcher imports.
- `--help` output is pinned by construction (`description=<module>.__doc__`,
  `parser.prog=<subcommand>`). The flag table is the contract; moving it is
  not a license to edit it.
- A `main`→`run` rename can collide with an existing helper named `run`
  (`deepread.run(command, …)`, `validate.run(...)`). Those helpers become
  `run_command`; a naming scan catches it.
- Prompt wording and constant **values** are unchanged. Moving them is not a
  license to retune them; wording and value edits are their own review.
- `scripts/README.md` and `CLAUDE.md` carry the invariant list; a regression
  test asserts the dispatcher flag tables against a frozen inventory.

## Supersedes / relates to

- Completes [0004](0004-unify-entry-dispatchers.md): 0004 unified the entry
  points, 0005 draws the layer boundary under them.
- Extends the `harness/prompt.py` convention first named in 0004's decision 2.
