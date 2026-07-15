---
id: EA-INDEX
title: 具身智能领域索引
type: domain-index
domain: embodied-ai
updated: 2026-07-15
tags: [embodied-ai, index]
---

# 具身智能领域索引

## 主题卡

| ID | 主题 | 文件 | 主要来源 |
|---|---|---|---|
| EA-DATA | 数据采集与数据质量 | [data-collection-quality.md](data-collection-quality.md) | S-EA-QUESTIONS; S-EMBODIED-DATA-FRAMEWORK; LR-DQ-YEAR; LR-DQ-CONTRA; LR-WM-DATA; LR-UMI; LR-EGO-DATA |
| EA-SENSOR | 传感器与多模态感知 | [sensors-multimodal-perception.md](sensors-multimodal-perception.md) | S-EA-QUESTIONS; LR-TWM; LR-SENSOR-ERROR; LR-UMI; LR-EGO-DATA; LR-VLOC |
| EA-HARDWARE | 采集硬件与设备路线 | [hardware-collection-devices.md](hardware-collection-devices.md) | S-EA-QUESTIONS; LR-UMI; LR-VLOC |
| EA-VLOC | 图像视觉定位 | [visual-localization.md](visual-localization.md) | LR-VLOC |
| EA-FIELD | 现场采集 Hub 与物流分拣考察 | [field-data-collection-hubs.md](field-data-collection-hubs.md) | S-LOGISTICS-HUB-SURVEY; S-EMBODIED-DATA-FRAMEWORK |
| EA-XEMBODIMENT | 跨本体与数据迁移 | [cross-embodiment-transfer.md](cross-embodiment-transfer.md) | S-EA-QUESTIONS; LR-VLA-ALIGN; LR-UMI; LR-EGO-DATA |
| EA-MODEL | 模型与预训练 | [models-pretraining.md](models-pretraining.md) | S-EA-QUESTIONS; LR-VLA-ALIGN; LR-WM-DATA; LR-4D; LR-EGO-DATA |
| EA-EVAL | 评测体系与世界模型 | [evaluation-world-models.md](evaluation-world-models.md) | S-EA-QUESTIONS; LR-WM-EVAL; LR-WM-DATA; LR-SENSOR-ERROR; LR-VLOC |
| EA-4D | 4D 时空推理与世界动态 | [4d-spatiotemporal-reasoning.md](4d-spatiotemporal-reasoning.md) | LR-4D; LR-4D-DATA |
| EA-ALIGN | VLA 多模态与动作对齐 | [vla-multimodal-action-alignment.md](vla-multimodal-action-alignment.md) | LR-VLA-ALIGN |
| EA-BIZ | 产业落地与商业化 | [commercialization.md](commercialization.md) | S-EA-QUESTIONS:411-441 |

## 常见组合

| 问题 | 推荐组合 |
|---|---|
| 数据采集方案如何选 | EA-DATA + EA-HARDWARE + EA-SENSOR |
| Ego-centric 人类视频如何用于机器人预训练 | EA-DATA + EA-XEMBODIMENT + EA-MODEL + EA-SENSOR |
| 无目标机器人本体阶段如何建数据资产 | EA-DATA + EA-FIELD + EA-XEMBODIMENT |
| 物流分拣现场如何考察和验收 | EA-FIELD + EA-DATA + EA-BIZ |
| 为什么模型真实部署掉点 | EA-MODEL + EA-EVAL + EA-DATA |
| 世界模型为什么视频真实但动作不可用 | EA-4D + EA-EVAL + EA-DATA |
| 语言、视觉和动作如何对齐 | EA-ALIGN + EA-MODEL + EA-XEMBODIMENT |
| 人手数据如何迁移到机器人 | EA-XEMBODIMENT + EA-SENSOR + EA-HARDWARE |
| 工业落地如何验收 | EA-BIZ + EA-EVAL + ERR-PATTERN |
| 最后一厘米问题 | EA-SENSOR + EA-BIZ + EA-EVAL |
| 图像视觉定位方法如何选、为何失效 | EA-VLOC + EA-SENSOR + EA-EVAL |
| 机器人失败是看错还是想错 | ERR-EMBODIED + EA-SENSOR + EA-ALIGN + EA-EVAL |
| 查 14 项综述的范围、论文池或三类成稿 | [文献综述成果目录](../literature-review-catalog.md) |
