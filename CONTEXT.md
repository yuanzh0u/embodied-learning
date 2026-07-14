---
id: PROJECT-CONTEXT
title: 项目上下文词表
type: glossary
updated: 2026-07-14
tags: [context, glossary, embodied-ai, query-planning]
---

# 项目上下文词表

本文只定义本项目共享语言，不写 Skill implementation spec。更细的证据、来源与主题知识仍按 `knowledge/` 路由加载。

| 术语 | 工作定义 |
|---|---|
| query plan | 围绕一个研究问题形成的结构化检索策略，说明 topic mapping、query tier、query channel 和每条 query 的 rationale。它是检索前的计划，不是论文证据。 |
| arXiv API query | 面向官方 arXiv API 元数据检索的 query 字符串。它应使用 API 可理解的论文检索表达，不混入 `site:`、Browser 搜索语法或社交平台线索。 |
| browser fallback query | 当 arXiv API 结果过少、受限或需要补充候选线索时，用 Browser/web search 执行的 fallback query。它用于发现候选论文、项目页或作者页入口，不能直接提升为 evidence。 |
| web calibration | 用 arXiv 页面、项目页、作者页、实验室页面等 web sources 校准关键词、别名、方法族和社区新词的过程。它只调整 query wording 与覆盖面，不替代正文证据。 |
| social calibration | 用 Reddit、X/Twitter 等社交讨论观察研究者或用户实际使用的说法、抱怨和新词。它属于 noisy signal，默认只作为低置信 query 线索。 |
| specialized family | 一组可复用的具身智能专项检索族，例如 UMI、VLA、Sim2Real、retargeting、tactile/force 等，用于把 broad topic 展开到命名方法、邻接任务和常见 failure surface。 |
| query tier | query plan 中表达召回层级和意图的标签，如 direct、adjacent、family、limitation、negative 或 calibration。tier 解释这条 query 预计捕获哪类材料。 |
| low-confidence calibration | 来自社交平台、非正式网页或其他噪声较高来源的校准记录。它可以提示新 query 或别名，但必须保留低置信标记，不能当作 accepted claim 或 source evidence。 |
| candidate pool | 多轮检索、去重和初筛后形成的相关论文候选集合。它用于证明覆盖范围，不等于已阅读全文或最终引用数。 |
| full-text eligible | 已取得完整、可解析且可定位原文上下文的非 OCR 全文。摘要、搜索片段、残缺 PDF 和扫描件不属于本项目的可用全文。 |
| paper note | 对单篇完整论文进行 map read / deep read 后形成的结构化记录，包含研究问题、方法、结果、限制和带原文上下文的 evidence cards。 |
| claim-support audit | 检查 paper note 中每个主张是否被对应全文上下文支持的审计。只有通过审计的主张才能投影为 accepted evidence。 |
| accepted evidence event | 从通过审计的 paper note 投影出的论文级证据记录，具有当前有效 run 集合中全局唯一的 event ID。 |
| review packet | 面向研究者的中预算审计视图，汇总综述范围、证据分布、共识、限制和缺口；它不是读者成稿。 |
| reader-facing articles | 科研备忘录、知乎解释稿和小红书稿三类表达层。它们共享 accepted evidence，但必须按各自读者和文体独立组织。 |
| active review run | 由 [文献综述成果目录](knowledge/literature-review-catalog.md) 声明为当前知识卡证据入口的 append-only run；历史 run 保留但不默认加载。 |
