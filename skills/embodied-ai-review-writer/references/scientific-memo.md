# Scientific Research Memo

Use this style for researchers, technical leads, and project decision-makers. The memo must help the reader decide what the literature changes about a research question.

## Default shape

- Chinese body length: roughly 2,500-6,000 Chinese characters, excluding references.
- Citation density: enough to support claims, never enough to interrupt every sentence.
- One central thesis, 3-5 derived tensions or mechanisms, at least one limiting condition, and a project-facing implication.
- Cite at least 5 representative accepted papers; for a large review, select enough papers to cover each distinct mechanism and major counterclaim rather than listing the whole registry.

## Recommended structure

1. **Title** — state the research object, not the workflow.
2. **研究边界** — question, time range, evidence coverage, and what the run cannot establish.
3. **中心判断** — answer the research question in one falsifiable paragraph.
4. **核心机制或派生矛盾** — prose sections that compare evidence on both sides and end with a takeaway.
5. **条件与分歧** — explain when the thesis weakens, reverses, or lacks evidence.
6. **可操作框架** — optional compact table only when it supports research or system design.
7. **研究空白与下一步** — distinguish run coverage gaps from literature-declared gaps.
8. **结论** — restate what changed, not what files were inspected.
9. **References** — full deduplicated paper list; event mapping belongs in `trace-map.json` and the appendix.

## Voice

- Prefer precise Chinese verbs and concrete mechanisms.
- Translate established technical terms once; retain English only when it is the community-standard label.
- Separate “论文显示” from “本文推断” and explain why the inference follows.
- Compare methods around a question; do not allocate one paragraph to each paper.
- Keep a neutral research voice unless the user explicitly supplies another voice. Do not add first-person reactions, personal experience, rhetorical drama, or informal asides to make the memo sound human.
- Preserve calibrated qualification. A shorter sentence is not better if it erases the task, dataset, embodiment, time-range, or evaluation condition under which a claim holds.
- Treat technical punctuation as semantic. Keep compounds such as “深度—尺度歧义” and other established notation when a dash expresses a real relation.

## Reject the draft when

- A Claim Map or evidence inventory is the largest section.
- The thesis is merely “the topic is complex” or “more evidence is needed”.
- Sections are stance buckets rather than arguments.
- The memo contains writer instructions, raw event claims, or English abstract fragments.
- Removing citations leaves no coherent argument.
