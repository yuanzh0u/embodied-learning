---
id: KB-INDEX
title: 智能体主索引
type: index
updated: 2026-07-08
tags: [agent-index, routing, embodied-ai, error-governance]
---

# 智能体主索引

本索引用于让智能体快速决定加载哪些材料。默认不要直接加载整篇原文。

## 加载策略

| 任务类型 | 推荐加载 |
|---|---|
| 项目语境与 query-planning 术语 | [../CONTEXT.md](../CONTEXT.md) |
| 了解项目整体背景 | [../CONTEXT.md](../CONTEXT.md)；完整背景经 git 存档读取（见 [sources.md](sources.md) 的 S-PROJECT-CONTEXT） |
| 查具身智能某个议题 | [embodied-ai/index.md](embodied-ai/index.md) + 对应主题卡 |
| 查测绘误差观或 AI 误差治理 | [error-governance/index.md](error-governance/index.md) + 对应主题卡 |
| 查论文级证据或历史文献 run | [../evidence/README.md](../evidence/README.md) + 对应 run 的 `run.json` 与 brief |
| 新增论文、报告、访谈、素材 | [ingestion-guide.md](ingestion-guide.md) + [templates/topic-card.md](templates/topic-card.md) |
| 统一术语 | [../CONTEXT.md](../CONTEXT.md) + [glossary.md](glossary.md) |
| 需要完整证据或参考资料 | [sources.md](sources.md) + `evidence/` 层；退役原文用登记的 `git show` 存档命令读取 |

## 主题卡路由

| ID | 主题 | 文件 | 关键词 |
|---|---|---|---|
| EA-DATA | 数据采集与数据质量 | [embodied-ai/data-collection-quality.md](embodied-ai/data-collection-quality.md) | UMI, DROID, Ego4D, 数据质量, scaling, 遮挡, 采集员 |
| EA-SENSOR | 传感器与多模态感知 | [embodied-ai/sensors-multimodal-perception.md](embodied-ai/sensors-multimodal-perception.md) | RGB, 3D, 点云, 触觉, 力控, proprioception |
| EA-HARDWARE | 采集硬件与设备路线 | [embodied-ai/hardware-collection-devices.md](embodied-ai/hardware-collection-devices.md) | 单目, 双目, ARKit, SLAM, Tracking, UMI, 指套 |
| EA-XEMBODIMENT | 跨本体与数据迁移 | [embodied-ai/cross-embodiment-transfer.md](embodied-ai/cross-embodiment-transfer.md) | retargeting, 灵巧手, 夹爪, embodiment adapter, 接触功能 |
| EA-MODEL | 模型与预训练 | [embodied-ai/models-pretraining.md](embodied-ai/models-pretraining.md) | VLA, RT-X, Octo, OpenVLA, 预训练, 微调, Sim2Real |
| EA-EVAL | 评测体系与世界模型 | [embodied-ai/evaluation-world-models.md](embodied-ai/evaluation-world-models.md) | 开放环, 闭环, benchmark, 世界模型, sim-real |
| EA-BIZ | 产业落地与商业化 | [embodied-ai/commercialization.md](embodied-ai/commercialization.md) | ToB, ROI, 节拍, 良率, 最后一厘米, 工业场景 |
| ERR-COMPARE | 测绘误差观与 AI 误差治理对照 | [error-governance/surveying-vs-ai-error-governance.md](error-governance/surveying-vs-ai-error-governance.md) | 量值误差, 语义风险, 真值, 验收, 平差 |
| ERR-PATTERN | 可迁移的误差治理模式 | [error-governance/transfer-patterns.md](error-governance/transfer-patterns.md) | 误差预算, 冗余检核, 适用边界, 残差分析, 风险等级 |

## 查询路由

| 用户问题包含 | 优先加载 |
|---|---|
| 数据采集、轨迹、数据质量、采集员、UMI、DROID、Ego4D | EA-DATA |
| 触觉、力、力矩、RGB、点云、3D、遮挡、可观测性 | EA-SENSOR |
| 单目、双目、ARKit、SLAM、VR、Pico、Quest、WebXR、指套 | EA-HARDWARE |
| 跨本体、人手到机器人、retargeting、灵巧手、夹爪、动作空间 | EA-XEMBODIMENT |
| 机器人基础模型、VLA、RT-X、Octo、OpenVLA、预训练、微调 | EA-MODEL |
| benchmark、开放环、闭环、仿真评测、世界模型、Sim2Real | EA-EVAL |
| ToB、商业化、ROI、行业落地、节拍、良率、最后一厘米 | EA-BIZ |
| 测绘、大模型误差、幻觉、可信等级、质量验收 | ERR-COMPARE, ERR-PATTERN |

## 上下文预算建议

- 低预算：只读本索引 + 1 张主题卡。
- 中预算：读领域索引 + 2-3 张主题卡。
- 高预算：读主题卡后，再按 `source` 打开 git 存档的对应章节,或按 `evidence/` run manifest 加载论文级证据。`evidence/` 中的 JSONL 不适合整读,先读 run.json 和 brief 再选择性加载。
