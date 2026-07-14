# Output Templates

## Source entry draft

```md
## S-ARXIV-<ID>

- 文件/链接：[<title>](https://arxiv.org/abs/<id>)
- 类型：论文 / arXiv
- 时间标记：published <YYYY-MM-DD>; retrieved <YYYY-MM-DD>
- 可信等级：primary
- 主题范围：
  - <EA-ID>：<brief locator or evidence file>
- 适用：需要复核 <topic> 的论文论点、论据、作者立场或引用链时读取。
```

## Candidate list

```md
# Candidate Papers: <topic>

- Time range: <start> to <end>
- Search plan: <query labels>

| Status | arXiv ID | Title | Why candidate | Evidence found |
|---|---|---|---|---|
| full-text-recovered | 2402.10329 | ... | UMI/data direct hit | complete structured HTML text |
| full-text-recovered | 2402.10330 | ... | HTML unavailable | complete text-layer PDF pages |
| needs-visual-validation | 2402.10331 | ... | medium PDF text | cited pages not yet verified |
| candidate | 2501.00000 | ... | VLA data adjacent | not inspected |
| unavailable | 2501.00001 | ... | metadata hit | HTML/PDF text did not yield usable text; no OCR |
| rejected | 2502.00000 | ... | metadata hit only | no topic discussion |
```

## Research brief

```md
# <Topic> Literature Brief

## Search Scope

- Time range:
- Queries:
- Accepted papers:
- Candidate papers:

## Claim Map

| Claim | Stance | Evidence | Authors | Papers |
|---|---|---|---|---|
|  | support/limit/conditional/gap |  |  |  |

## High-Signal Findings

- Claim:
  - Evidence:
  - Caveat:
  - Candidate citations to chase:

## Author Stance Events

| Author key | Institutions | Paper | Date | Claim | Stance |
|---|---|---|---|---|---|

## Topic Card Update Suggestions

- Add to `<EA-ID>`:
  - Synthesized claim with source ID.
- Use this section as a candidate update list for topic cards. Do not auto-patch topic cards from it.
- Include only high-signal synthesis that changes the working memory of the topic card, not single-paper summaries.
```
