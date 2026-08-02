# Editorial Quality Rubric

Apply this rubric after evidence and citation validation. A file can be traceable and still fail as an article.

## Shared gates

| Dimension | Pass condition |
|---|---|
| Thesis | One explicit, evidence-bounded answer to the reader's question |
| Audience outcome | The intended reader, takeaway, and changed judgment are explicit in the editorial plan and visible in the article |
| Synthesis | Claims grouped by mechanism, tension, or decision—not paper order |
| Explanation | Major sections connect phenomenon, mechanism, evidence, consequence, and boundary instead of stopping at paper summaries |
| Counterevidence | At least one visible limit, condition, or falsifier |
| Language | Natural Chinese; English retained only for necessary technical labels |
| Cognitive load | Acronyms, long sentences, citations, and model names do not crowd out the explanation |
| Context | Important numbers identify the task, comparison, or scope needed to interpret them |
| Naturalness | Direct, concrete prose with varied rhythm; no chatbot residue, empty promotion, or generic uplift |
| Integrity | Natural-language edits add no facts and preserve numbers, citations, uncertainty, and boundary conditions |
| Provenance | Reader-facing paper links plus an auditable trace map |
| Cleanliness | No packet headings, event dumps, template instructions, or truncated claims |
| Independence | Each style has a different opening, outline, examples, and ending |
| Source selection | Each style selects representative evidence from the accepted reservoir instead of dumping all papers |

## Default quantitative gates

- Chinese share in visible prose: at least 65% of Chinese plus Latin letters.
- Exact substantive-line overlap between scientific and Zhihu drafts: at most 25%.
- No visible event IDs in body prose.
- No empty annotated-reading bullets, `stance:`/`trace:`/`inference` labels, source-entry IDs, empty citation slots, malformed generated punctuation, or placeholders such as “随附证据附录/相关知识单元”.
- No topic-agnostic canned phrases from the packet scaffolds.
- No conversational assistant residue or exactly repeated substantive prose blocks; generic uplift, vague attribution, and promotional wording require manual review.
- No unresolved generic citation anchors, detached citation punctuation, missing citation subjects, or unannotated publication reading lists.
- Xiaohongshu source/reference material: at most 20% of non-empty lines.
- Xiaohongshu insight count: 3-5.
- Unique arXiv sources: scientific memo at least 5; Zhihu 3-12; Xiaohongshu 3-5.

Quantitative gates catch regressions; they do not certify editorial quality. Always complete a manual read.

For a published collection, also review corpus distributions and exact cross-article reuse. Treat repeated substantive prose and a heading template shared by at least 40% of three or more articles as editorial warnings, not automatic evidence failures.

## Evidence-locked natural-writing pass

Apply these checks only after the argument and evidence surface are stable.

| Improve | Preserve |
|---|---|
| Delete conversational residue such as “希望这对你有帮助” or “如果需要我可以继续” | Every factual claim, number, date, paper link, quote, and named entity |
| Replace empty promotion, inflated significance, and generic positive conclusions with the supported result | `conditional`, `limit`, and `gap` language, including explicit uncertainty |
| Replace vague authority claims with a named source already present in the inputs; otherwise narrow or remove the claim | Technical terms, necessary repetition, and punctuation that carries domain meaning |
| Remove redundant signposting, synonym cycling, and exact paragraph repetition | Platform grammar: research structure, Zhihu explanation, Xiaohongshu emoji navigation and insight cards |
| Vary sentence length when several consecutive sentences have the same cadence | The writer's supplied voice; never manufacture a personal anecdote or emotional reaction |

Do not use a blacklist of isolated words. “此外”“关键”“复杂”“不仅……而且……” and em dashes can be ordinary Chinese or technical notation. Edit the sentence only when the expression is actually empty, repetitive, or misleading.

## Manual read

Ask:

1. Can the thesis be stated without mentioning the workflow or evidence count?
2. Does each section advance the argument rather than repeat a source?
3. Are opposing results explained instead of flattened?
4. Would the intended reader understand why the evidence matters?
5. After removing citations, does a coherent article remain?
6. Could any paragraph be pasted into another topic unchanged? If yes, rewrite it.
7. Do the three styles sound written for different readers rather than reformatted from one draft?
8. Is every major evidence tension represented somewhere, even when not every accepted paper is cited?
9. Did the final language pass add, remove, or strengthen any fact, number, citation, or boundary condition?
10. Is every first-person statement either supported by an author-supplied voice or clearly an evidence-bounded editorial synthesis, rather than invented experience?
11. Could the intended reader restate the thesis without using paper names or unexplained acronyms?
12. Does at least one example carry the reader from a concrete phenomenon through the main mechanism and its boundary?
13. Does every evidence-heavy section state what the evidence changes for data collection, training, evaluation, or deployment?
14. Are quantitative results accompanied by the comparison and scope needed to understand them?
15. Is the article structure chosen for this question, or could the headings be swapped into another topic unchanged?
16. Would a schematic materially reduce the effort needed to understand three or more linked stages, branches, or comparisons?

## Rule provenance

The natural-writing checks adapt high-precision ideas from [op7418/Humanizer-zh at `91f3d394`](https://github.com/op7418/Humanizer-zh/tree/91f3d394db8419c20d67ebe22a96cf8fee0a404b) and its [upstream Humanizer](https://github.com/blader/humanizer), both MIT-licensed. This project deliberately excludes their unsafe or channel-incompatible behavior: invented specificity, forced first person, deliberate messiness, mechanical word removal, unconditional emoji removal, and weakened evidence qualifications.
