# Citation Projection

Keep two layers: a clean reader surface and a complete audit surface.

## Reader surface

- Body citations point to the paper: `[SIEVE](https://arxiv.org/abs/2607.06442)` (Zhihu, Xiaohongshu).
- Scientific memo: **superscript numbered citations, one marker per cited number** — `^[1]^`, `^[2]^` in the text (Pandoc-style superscript with square brackets). NEVER batch numbers into one marker (`^[1,2,3]^` is a style violation): write each cited number as its own adjacent marker, e.g. `^[1]^ ^[2]^ ^[3]^`. Each marker resolves, at Wiki build time, against the document's own `## References` list into a clickable reader link — so the References section must keep its per-entry arXiv links (`[arXiv:2602.11323](https://arxiv.org/abs/2602.11323)`). Cite at least 5 representative papers, then list them under a full `## References` section: one line per entry, numbered to match the superscripts, each giving the paper's English title, first author et al., year, and the arXiv link. Add sources only when they contribute a distinct mechanism, result, or boundary.
- Zhihu: use a small number of paper links in prose and 3-12 annotated items under `## 延伸阅读` or `## References`.
- Xiaohongshu: use 3-5 representative paper links and one compact `📚 依据` line; do not add a full bibliography.
- Never expose event IDs, stance labels, confidence labels, or appendix anchors in body prose.

## Audit surface

- `evidence-appendix.md` remains the source for event claim, stance, confidence, locator, and short quote.
- Generate `trace-map.json` with `writing_audit.py build-trace-map`. It records each article's cited arXiv papers and the accepted event IDs that cover them.
- Keep every reader-facing paper inside the accepted evidence set. An uncovered paper is an error, not an editorial exception.
- For an inference spanning several papers, cite the papers in prose and record all contributing events in the trace map. Explain the inference and its falsifier in the scientific memo.
- `accepted evidence count` and `article citation count` are different metrics. The former measures the research reservoir; the latter is an editorial selection.

## Why projection is necessary

Traceability must be lossless, but it does not have to be visually identical across platforms. Event IDs are useful to auditors; paper names, examples, and conclusions are useful to readers. Preserve both by separating surfaces rather than forcing audit syntax into every sentence.
