# Zhihu Expert Explainer

Use this style for technically curious readers who need a difficult embodied-AI question explained, not surveyed.

## Default shape

- Chinese body length: roughly 1,800-4,500 Chinese characters, excluding references.
- Treat that range as an explanation-completeness target, not a padding quota. Review 1,000-1,799-character drafts for over-compression; reject only when the argument cannot be completed within the shorter form.
- Begin with one concrete reader question or misconception.
- Explain 2-4 mechanisms, one counterexample, and one boundary condition.
- End with a memorable answer and 3-12 items of further reading.
- Cite 3-12 representative accepted papers across the explanation and annotated reading list.
- Default to 2-4 anchor papers in the body. Put supporting coverage in annotated further reading unless another paper materially changes the mechanism, decision, or boundary.

## Reader contract

Before drafting, write a private plan that names:

- the technically curious reader and what they already know;
- the question they should be able to answer after reading;
- the practical judgment changed by the evidence;
- one running example drawn from accepted evidence, or a clearly labeled schematic example that asserts no new empirical fact;
- the 3-5 core terms that need a first-use explanation;
- the representative evidence, counterevidence, and closing boundary.

## Choose an article arc

Use the topic to choose an arc instead of forcing identical headings:

- **Mechanism:** failure scene → causal chain → evidence → intervention → boundary.
- **Comparison:** shared problem → decisive differences → selection conditions → counterexample.
- **Evolution:** old bottleneck → turning evidence → current capability → unresolved limit.
- **Diagnosis:** symptom → ordered checks → evidence-backed causes → decision checklist.

Keep TL;DR and a visible boundary, but vary section names and order when clarity improves.

## Functional checklist

1. **Question-led title** — expose the tension or mistaken intuition.
2. **TL;DR** — answer directly in 2-4 sentences, including the caveat.
3. **Plausible intuition** — explain why the mistaken or incomplete view is reasonable.
4. **Mechanism** — use the running example to connect phenomenon, cause, evidence, and consequence.
5. **Judgment change** — compare a small number of papers and state what the reader should now judge differently.
6. **Boundary** — convert limit and conditional evidence into practical boundary clauses.
7. **Ending** — answer the opening question in plainer language.
8. **Further reading** — link 3-8 papers and give one sentence on why each matters.

## Voice

- Sound like an expert colleague, not a review database or marketing account.
- Use analogies only when they preserve the mechanism.
- Explain jargon at first use; avoid mixed Chinese-English noun chains.
- Put the Chinese mechanism before the acronym or English label. After first use, prefer a stable functional name over repeated paper abbreviations.
- Let citations support the explanation rather than replace it.
- Prefer a direct question, concrete failure, or decision consequence over “下面我们深入探讨” and other conversational stage directions.
- A confident editorial judgment must remain distinguishable from a paper result. Do not invent meetings, experiments, personal experiences, or reader anecdotes to manufacture a human voice.
- Keep necessary caveats in the answer. Natural prose may compress them, but must not turn a conditional finding into a universal conclusion.
- Consider one original schematic when the explanation has at least three dependent stages, branches, or repeated-field comparisons. Label it as a schematic and do not add unsupported facts.

## Reject the draft when

- More than a quarter of substantive lines are shared verbatim with the scientific memo.
- The opening is generic and could be attached to any topic.
- The body contains a Claim Map table, stance labels, event IDs, or formal-readiness metadata.
- “延伸阅读” is a full bibliography without editorial annotations.
- The body contains generic anchors such as unlinked “相关研究” or `[相关研究](...)`.
- Paper names and acronyms remain the paragraph structure after citations are removed.
