---
id: KB-INGEST
title: 新素材入库规范
type: workflow
updated: 2026-06-05
tags: [ingestion, workflow, agent-process]
---

# 新素材入库规范

新增论文、报告、访谈、网页、产品信息或项目经验时，按以下流程处理。

## 1. 登记来源

在 [sources.md](sources.md) 记录：

- source id
- 文件或链接
- 类型：论文、报告、访谈、产品页、会议纪要、项目经验
- 时间范围或发布日期
- 可信等级：primary、secondary、industry-observation、inference
- 可复核链接或本地路径

## 2. 抽取主题

判断素材属于哪些主题卡：

- 数据采集与质量：EA-DATA
- 传感器与感知：EA-SENSOR
- 采集硬件：EA-HARDWARE
- 跨本体迁移：EA-XEMBODIMENT
- 模型与预训练：EA-MODEL
- 评测与世界模型：EA-EVAL
- 商业化：EA-BIZ
- 误差治理：ERR-COMPARE / ERR-PATTERN

如果没有合适主题，复制 [templates/topic-card.md](templates/topic-card.md) 创建新卡。

## 3. 更新主题卡

每次更新尽量只添加高信噪比内容：

- 新增关键判断
- 新增证据锚点
- 新增指标或评估方法
- 新增适用边界
- 新增待复核问题

避免把整段论文摘要直接粘进主题卡。长摘要应放到单独 source note 或保留在原文。

## 4. 更新索引

新增主题卡后必须更新：

- [index.md](index.md) 的主题卡路由
- 对应领域的 `index.md`
- [glossary.md](glossary.md)，如果引入新术语

## 5. 标记不确定性

快速变化信息必须写明日期，例如模型版本、产品规格、行业规模、政策、benchmark 排名。判断来自推断时，在卡片中标记 `inference`。

