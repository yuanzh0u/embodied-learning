---
id: DOMAIN-SLUG
title: 主题标题
type: topic-card
domain: domain-name
updated: YYYY-MM-DD
source:
  - id: SOURCE-ID
    file: relative/path.md
    locator: section or lines
tags: [tag1, tag2]
aliases: []
load_when:
  - 用户问题包含哪些关键词时加载
confidence: working
---

# 主题标题

## Agent Load Hints

- Load this when:
- Usually pair with:
- Raw source only needed when:
- Evidence route: 先读对应 review packet；只有核验具体主张时才加载 paper note 与 claim-support audit。

## 30 秒摘要

用 3-5 句话说明本主题的核心判断。

## 关键判断

- 判断 1。
- 判断 2。
- 判断 3。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
|  |  |

## 适用边界

- 哪些任务/场景适用。
- 哪些任务/场景不适用。

## 证据锚点

- SOURCE-ID：当前有效 evidence run 中实际存在的 event ID 或连续区间。
- 跨论文综合判断必须标记为 `synthesis` 或 `inference`，不能伪装成单篇论文结论。

## 待补问题

- 待补问题。
