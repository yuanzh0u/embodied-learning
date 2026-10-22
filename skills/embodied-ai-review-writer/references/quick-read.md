# Quick-Read Card（速读卡）

Use this style when the user wants to decide in one minute whether a single paper deserves a deep read. The card compresses exactly one paper — never a topic, never a field — into a fixed skeleton so that cards are horizontally comparable.

## Default shape

- Subject: exactly one paper. Every claim, number, and judgment is bounded by that paper's deep-read note (`note.json`) and its own full text (`paper.md`). No cross-paper synthesis, no field-survey claims, no "该领域普遍认为".
- Chinese body length: roughly 600-1,200 Chinese characters, excluding the link line.
- Numbers may appear only from the note's `evidence_cards[].quantitative` or a verbatim `source_context` quote. A number absent from those inputs must not be written.
- No tables. Headings and lists only — the card must render inside the wiki's inline reader.
- One arXiv link, exactly once, in the 链接 section.

## Recommended structure

```md
# 速读：<论文标题>

arXiv:<id> · <method|system|dataset|survey|analysis|benchmark>

## 一句话定位

<1-2 句：这篇论文做了什么 + 一句可证伪的 takeaway。>

## 问题与动机

<2-4 句：它声称填补的空隙，以及为什么现有方法不够。>

## 方法步骤

1. <步骤一>
2. <步骤二>
3. <步骤三（3-6 步）>

## 关键结果与数字

- <中文主张>（<metric> <value_or_direction> <comparator>）
- <无定量结果时：本笔记未提取到可靠的定量结果。>

## 三分法评价

- 创新点：<一条，绑定证据卡或“论文未给出”>
- 性能：<一条，绑定证据卡或“论文未给出”>
- 工作量：<一条，绑定证据卡或“论文未给出”>

## 局限与边界

- 论文承认：<来自 limitations.author_stated，可能为空>
- 读者推断：<来自 limitations.reader_inferred 或 transfer_boundary>
- <保留 可能/仅/尚未/在……条件下一类限定词，不得为通顺而删除。>

## 链接

[arXiv:<id>](https://arxiv.org/abs/<id>)
```

## Voice

- Neutral, dense, no hook, no emoji. The card optimizes decision speed, not persuasion.
- Translate established technical terms once into Chinese; retain English only when it is the community-standard label.
- Separate “论文显示” from “读者推断”. The 三分法评价 labels a judgment that is not verbatim from the paper as such.
- Keep qualification words: 可能、仅、尚未、在……条件下. A smoother sentence is not better if it erases the boundary.
- Method steps decompose the note's method summary into concrete actions; do not copy abstract machinery.

## Citation surface

- Link only the subject paper. Citing any other paper disqualifies the card.
- Do not print event IDs, stance labels, card IDs, or note field names in the prose.

## Reject the draft when

- It cites, compares against, or borrows numbers from any paper other than the subject.
- A table appears, or the card exceeds roughly 1,200 Chinese characters.
- The 三分法评价 invents innovation/performance/workload judgments the note does not support.
- Workflow language (stance, evidence card, locator, note fields) leaks into the prose.
- The 局限与边界 section is empty — a card without a boundary is not publishable.
