---
id: ERR-INDEX
title: 误差治理领域索引
type: domain-index
domain: error-governance
updated: 2026-07-14
tags: [error-governance, index]
---

# 误差治理领域索引

## 主题卡

| ID | 主题 | 文件 | 原始来源 |
|---|---|---|---|
| ERR-COMPARE | 测绘误差观与 AI 误差治理对照 | [surveying-vs-ai-error-governance.md](surveying-vs-ai-error-governance.md) | S-ERR-COMPARE:5-224 |
| ERR-PATTERN | 可迁移的误差治理模式 | [transfer-patterns.md](transfer-patterns.md) | S-ERR-COMPARE; LR-PVC; LR-TRACE |
| ERR-EMBODIED | 具身智能误差分层与溯源 | [embodied-error-traceability.md](embodied-error-traceability.md) | LR-TRACE; LR-PVC; LR-SENSOR-ERROR |

## 常见组合

| 问题 | 推荐组合 |
|---|---|
| 大模型幻觉如何工程治理 | ERR-COMPARE + ERR-PATTERN |
| 具身智能如何建立验收标准 | ERR-PATTERN + EA-EVAL + EA-BIZ |
| 机器人失败如何区分感知、认知、动作和控制错误 | ERR-EMBODIED + ERR-PATTERN + EA-SENSOR + EA-ALIGN |
| 测绘误差理论能否迁移到 AI | ERR-COMPARE + ERR-PATTERN |
| 智能体工具链错误如何追踪 | ERR-PATTERN + EA-EVAL |
| 查感知误差、认知误差或溯源综述的论文级证据 | [文献综述成果目录](../literature-review-catalog.md) + ERR-EMBODIED |
