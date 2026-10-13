# Slide-Deck（汇报展示）

Use this style when the user wants a 汇报/展示/放映件 — a presentation deck built from deep-read evidence, organized **by topic** (背景 → 方法谱系 → 横向对比 → 机制 → 局限 → 启示), never by copying a paper's section order. The deliverable is a single-file, offline, reveal.js HTML deck.

## The division of labor is absolute

- **The agent writes ONLY the slide-source** (`slide-deck_report.md`, a restricted DSL — see below). The agent NEVER hand-writes HTML, never edits the compiled file, never inlines base64.
- **`build_slide_deck.py` compiles** slide-source → single-file HTML deterministically: citation numbering, References pages, figure base64 inlining, and div balance are all structural guarantees of the compiler.
- Every edit cycle is: edit slide-source → recompile → (visual QA) → recompile. The compiled HTML is a build artifact; the slide-source is the deliverable's source of truth.

```bash
python3 skills/embodied-ai-review-writer/scripts/write.py compile-slide-deck \
  --source <run-dir>/slide-deck_report.md --output <run-dir>/slide-deck_report.html \
  [--refs <run-dir>/refs.json] [--qa /tmp/deck-qa]
```

## Slide-source DSL

Document head (before the first `---`): `# title:` / `# subtitle:` / `# date:` / `# refs:` (JSON mapping citation keys → `{title, url}`) / optional `# end:`. Slides are separated by bare `---` lines. Each slide has head fields (`kicker:`, `title:`, optional `verdict:`, optional `class: cover|end`) and a body of blocks:

- `- ` bullets (≤7/slide), `1. ` numbered steps (render as a step tracker)
- `@stat <value> | <label>` — number cards; adjacent @stats merge into one row (≤4)
- `@bars A 0.30 ; *B 0.85 ; !C 60%` — horizontal bars; `*` = ours highlight, `!` = risk
- `@card 标题 | 一句话` / `@cards A | x ;; B | y` — cards / side-by-side card row
- `@tier 环节一 > *核心环节` — pipeline/spectrum chips, `*` marks the hot stage
- `@fix 已核验一 ; 已核验二` — checklist; `@care 一句话` — risk callout
- `@fig <path> | 图注` — figure inlined base64 (≤2/slide); `| ... |` pipe rows render as a table (≤1/slide)
- Citations: `{{key}}` inline → `^[N]^` numbered by first appearance; unresolved key = compile error

## Content rules

- **One slide, one claim.** The slide title states the claim, the body carries the evidence, the `verdict` states the so-what. A slide without a verdict is a bullet dump, not a report page (every content page needs one; the audit warns above 40% missing).
- **Organize by topic, not by paper and not by source section order.** Merge papers that make the same point onto one page; keep a dissenting result adjacent to the claim it bounds. Honesty rules from the other styles apply verbatim: no claim without a citation key, no number not present in the evidence, uncertainty markers preserved (`conditional`/`limit` claims stay marked).
- **Density red lines** (compiler-enforced): ≤7 bullets, ≤2 figures, ≤1 table, ≤4 stat cards per page. If a page overflows, split it — do not shrink content.
- **Figures**: only figures carried by evidence events (`evidence.figures[]`), same discipline as citations — source URL/caption verbatim, never invented. For run-level decks the figure files must be materialized locally so `@fig` can inline them.
- **References**: cited keys only; the compiler builds the appendix pages automatically. The refs JSON is derived from the run's evidence appendix (or the paper's note for single-paper decks) — never hand-invented titles.

## Structure of a full deck

`cover`（题 + 副题 + 日期）→ 路线图页（今天讲什么，3-5 chips 用 `@tier`）→ 主题页（每页一论点）→ 结论页（3 条 take-away，全册 verdict）→ References（编译器生成）→ `end` 页。

## Visual QA loop (mandatory before delivering)

```bash
# --qa screenshots every slide (reveal #/N hash navigation); then READ each png
python3 ... build_slide_deck.py --source ... --output ... --qa /tmp/deck-qa
```

Read the screenshots and fix: overflowing pages (split the page), label/number collisions in `.bars`, figures too small to read (crop tighter from the source PDF instead of scaling down), text over the verdict bar. Recompile and re-screenshot changed pages until clean.
