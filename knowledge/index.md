---
id: KB-INDEX
title: 智能体主索引
type: index
updated: 2026-07-15
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
| 查已完成综述、论文池规模、精读状态或三类成稿 | [literature-review-catalog.md](literature-review-catalog.md)；再按预算进入主题卡、review packet 或 paper note |
| 新增论文、报告、访谈、素材 | [ingestion-guide.md](ingestion-guide.md) + [templates/topic-card.md](templates/topic-card.md) |
| 统一术语 | [../CONTEXT.md](../CONTEXT.md) + [glossary.md](glossary.md) |
| 需要完整证据或参考资料 | [sources.md](sources.md) + `evidence/` 层；退役原文用登记的 `git show` 存档命令读取 |

## 主题卡路由

| ID | 主题 | 文件 | 关键词 |
|---|---|---|---|
| EA-DATA | 数据采集与数据质量 | [embodied-ai/data-collection-quality.md](embodied-ai/data-collection-quality.md) | UMI, DROID, Ego4D, Ego-centric, 人类视频, 数据质量, L0-L3, episode, schema, 遮挡 |
| EA-SENSOR | 传感器与多模态感知 | [embodied-ai/sensors-multimodal-perception.md](embodied-ai/sensors-multimodal-perception.md) | RGB, 3D, 点云, 触觉, 力控, proprioception |
| EA-HARDWARE | 采集硬件与设备路线 | [embodied-ai/hardware-collection-devices.md](embodied-ai/hardware-collection-devices.md) | 单目, 双目, ARKit, SLAM, Tracking, UMI, 指套 |
| EA-VLOC | 图像视觉定位 | [embodied-ai/visual-localization.md](embodied-ai/visual-localization.md) | 图像定位, VPR, 相机重定位, SCR, 3DGS, PnP, 拒识覆盖 |
| EA-FIELD | 现场采集 Hub 与物流分拣考察 | [embodied-ai/field-data-collection-hubs.md](embodied-ai/field-data-collection-hubs.md) | 物流分拣, Hub, 现场考察, 岗位盘点, 视频验收, 试采 |
| EA-XEMBODIMENT | 跨本体与数据迁移 | [embodied-ai/cross-embodiment-transfer.md](embodied-ai/cross-embodiment-transfer.md) | retargeting, 灵巧手, 夹爪, embodiment adapter, 接触功能 |
| EA-MODEL | 模型与预训练 | [embodied-ai/models-pretraining.md](embodied-ai/models-pretraining.md) | VLA, RT-X, Octo, OpenVLA, 预训练, 微调, Sim2Real |
| EA-EVAL | 评测体系与世界模型 | [embodied-ai/evaluation-world-models.md](embodied-ai/evaluation-world-models.md) | 开放环, 闭环, benchmark, 世界模型, sim-real |
| EA-4D | 4D 时空推理与世界动态 | [embodied-ai/4d-spatiotemporal-reasoning.md](embodied-ai/4d-spatiotemporal-reasoning.md) | 4D, point tracks, correspondence, 动态场景图, action-conditioned rollout |
| EA-ALIGN | VLA 多模态与动作对齐 | [embodied-ai/vla-multimodal-action-alignment.md](embodied-ai/vla-multimodal-action-alignment.md) | 语言稀疏, 视觉稠密, 动作连续, action token, action adapter |
| EA-BIZ | 产业落地与商业化 | [embodied-ai/commercialization.md](embodied-ai/commercialization.md) | ToB, ROI, 节拍, 良率, 最后一厘米, 工业场景 |
| ERR-COMPARE | 测绘误差观与 AI 误差治理对照 | [error-governance/surveying-vs-ai-error-governance.md](error-governance/surveying-vs-ai-error-governance.md) | 量值误差, 语义风险, 真值, 验收, 平差 |
| ERR-PATTERN | 可迁移的误差治理模式 | [error-governance/transfer-patterns.md](error-governance/transfer-patterns.md) | 误差预算, 冗余检核, 适用边界, 残差分析, 风险等级 |
| ERR-EMBODIED | 具身智能误差分层与溯源 | [error-governance/embodied-error-traceability.md](error-governance/embodied-error-traceability.md) | 感知误差, 认知误差, 第一偏离点, 误差账本, 失败归因 |

## 查询路由

| 用户问题包含 | 优先加载 |
|---|---|
| 数据采集、轨迹、数据质量、采集员、UMI、DROID、Ego4D、L0/L1/L2/L3、episode schema、无本体采集 | EA-DATA |
| Ego-centric、人类第一视角视频、行为预训练、动作恢复、目标机器人锚定 | EA-DATA, EA-XEMBODIMENT, EA-MODEL, EA-SENSOR |
| 触觉、力、力矩、RGB、点云、3D、遮挡、可观测性 | EA-SENSOR |
| 单目、双目、ARKit、SLAM、VR、Pico、Quest、WebXR、指套 | EA-HARDWARE |
| 图像定位、视觉定位、VPR、地点识别、相机重定位、SCR、3DGS 位姿、PnP | EA-VLOC, EA-SENSOR, EA-EVAL |
| 物流分拣、Hub、现场考察、岗位盘点、视频验收、远程验收、试采、Top 5 岗位 | EA-FIELD, EA-DATA, EA-BIZ |
| 跨本体、人手到机器人、retargeting、灵巧手、夹爪、动作空间 | EA-XEMBODIMENT |
| 机器人基础模型、VLA、RT-X、Octo、OpenVLA、预训练、微调 | EA-MODEL |
| benchmark、开放环、闭环、仿真评测、世界模型、Sim2Real | EA-EVAL |
| 4D、point tracks、跨帧几何、动态场景图、世界动态、动作条件未来 | EA-4D, EA-EVAL, EA-MODEL |
| 语言动作对齐、视觉动作对齐、动作 token、action adapter、动作连续、语言稀疏 | EA-ALIGN, EA-MODEL, EA-XEMBODIMENT |
| ToB、商业化、ROI、行业落地、节拍、良率、最后一厘米 | EA-BIZ |
| 测绘、大模型误差、幻觉、可信等级、质量验收 | ERR-COMPARE, ERR-PATTERN |
| 感知误差、认知误差、传感器错误、失败归因、误差溯源、第一偏离点 | ERR-EMBODIED, ERR-PATTERN, EA-SENSOR |
| 文献综述、论文清单、候选池、全文、精读笔记、科研稿、知乎稿、小红书稿 | [文献综述成果目录](literature-review-catalog.md) |

## 上下文预算建议

- 低预算：只读本索引 + 1 张主题卡。
- 中预算：读领域索引 + 2-3 张主题卡。
- 高预算：读主题卡后，经 [文献综述成果目录](literature-review-catalog.md) 选择 run，先读 `run.json` 与 `review-packet.md`，再从 `paper-note-index.json` 选择性加载 paper note 和 claim-support audit。`evidence.jsonl` 与候选库都不适合默认整读。
