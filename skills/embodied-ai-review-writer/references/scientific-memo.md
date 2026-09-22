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

## Figures

- 配额：≤4 图 + 1 表（上限，不是配额指标；证据事件没带图就保持纯文字）。
- 图源纪律：只允许使用 writing-brief「可用图表」段列出的 evidence 事件图表——URL 与题注照抄，
  禁止自造、外搜或引用未进入证据层的图片。
- 格式：`![题注](image_url)` 空行后跟 `> 用法：<中文一句话>（论文短名，locator）`；
  插入位置为该图所支撑的论证段之后。表格用 brief 里的现成 markdown 网格。
- memo 正文禁止的是 `arxiv.org/abs/` 链接（引文格式约束）；`arxiv.org/html/...` 图片 URL
  不受此限——它是图源，不是叙述性链接。图注/alt 文本中不得出现事件 ID 形 token（`EA-…-NNNN`）。

## Reject the draft when

- A Claim Map or evidence inventory is the largest section.
- The thesis is merely “the topic is complex” or “more evidence needed”.
- Sections are stance buckets rather than arguments.
- The memo contains writer instructions, raw event claims, or English abstract fragments.
- Removing citations leaves no coherent argument.
- The title is a suspense or antithesis headline (“不是A，而是B”, “瓶颈转移到…”, “从X到Y的逆袭”) instead of a neutral statement of the research object.
- The memo opens with a bold TL;DR/slogan paragraph in the zhihu-explainer voice, or narrates the literature as a dramatic evolution arc (“第一代→第二代→第三阶段”) instead of arguing mechanisms against evidence.
- Bold emphasis is used for punchlines rather than genuinely load-bearing terms.
