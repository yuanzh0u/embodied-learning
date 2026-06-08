---
id: KB-README
title: 知识库说明
type: guide
updated: 2026-06-05
tags: [knowledge-base, agent-index, context-efficiency]
---

# 知识库说明

`knowledge/` 是面向智能体使用的结构化知识层。它不替代原始材料，而是把长文拆成可快速检索、可低成本加载、可继续扩展的主题卡片。

## 目录结构

| 路径 | 用途 |
|---|---|
| [index.md](index.md) | 全局路由索引，智能体优先读取 |
| [sources.md](sources.md) | 原始材料登记表和来源行段 |
| [glossary.md](glossary.md) | 术语表 |
| [ingestion-guide.md](ingestion-guide.md) | 新素材入库规范 |
| [templates/topic-card.md](templates/topic-card.md) | 新主题卡片模板 |
| [embodied-ai/](embodied-ai/index.md) | 具身智能主题卡片 |
| [error-governance/](error-governance/index.md) | 误差治理主题卡片 |

## 设计原则

- 一张卡只服务一个主题，控制上下文体积。
- 每张卡必须有 `id`、`tags`、`source`、`load_when`。
- 主题卡优先沉淀判断、指标、适用边界和检索关键词。
- 原文保留完整论述，主题卡只做高信噪比压缩。
- 新素材先登记，再抽取成主题卡，避免资料堆成不可检索长文。

## 智能体使用方式

1. 读取 [index.md](index.md) 判断应该加载哪些卡片。
2. 读取对应领域索引，例如 [embodied-ai/index.md](embodied-ai/index.md)。
3. 读取 1-3 张最相关主题卡。
4. 只有在需要证据细节、原始表达或参考链接时，才读取原始材料。

