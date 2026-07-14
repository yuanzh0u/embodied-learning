# Citation Projection

Keep two layers: a clean reader surface and a complete audit surface.

## Reader surface

- Body citations point to the paper: `[SIEVE](https://arxiv.org/abs/2607.06442)`.
- Scientific memo: use paper links in prose, cite at least 5 representative papers, and keep a full `## References`; add sources only when they contribute a distinct mechanism, result, or boundary.
- Zhihu: use a small number of paper links in prose and 3-12 annotated items under `## 延伸阅读` or `## References`.
- Xiaohongshu: use 3-5 representative paper links and one compact `📚 依据` line; do not add a full bibliography.
- Never expose event IDs, stance labels, confidence labels, or appendix anchors in body prose.

## Audit surface

- `evidence-appendix.md` remains the source for event claim, stance, confidence, locator, and short quote.
- Generate `trace-map.json` with `build_trace_map.py`. It records each article's cited arXiv papers and the accepted event IDs that cover them.
- Keep every reader-facing paper inside the accepted evidence set. An uncovered paper is an error, not an editorial exception.
- For an inference spanning several papers, cite the papers in prose and record all contributing events in the trace map. Explain the inference and its falsifier in the scientific memo.
- `accepted evidence count` and `article citation count` are different metrics. The former measures the research reservoir; the latter is an editorial selection.

## Why projection is necessary

Traceability must be lossless, but it does not have to be visually identical across platforms. Event IDs are useful to auditors; paper names, examples, and conclusions are useful to readers. Preserve both by separating surfaces rather than forcing audit syntax into every sentence.
