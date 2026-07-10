---
id: EA-4D
title: 4D 时空推理与世界动态
type: topic-card
domain: embodied-ai
updated: 2026-07-10
source:
  - id: RUN-4D-REASONING-20260612
    file: ../../evidence/literature-review-4d-spatiotemporal-reasoning-20260612/evidence.jsonl
    locator: EA-MODEL-2026-4D-0001..0010; EA-EVAL-2026-4D-0002..0020; EA-SENSOR-2026-4D-0015..0019
  - id: RUN-4D-DATA-20260612
    file: ../../evidence/literature-review-4d-data-requirements-20260612/evidence.jsonl
    locator: EA-DATA-2026-4DDATA-0001..0020
tags: [embodied-ai, 4d, spatiotemporal, point-tracks, world-model, geometry, dynamics]
aliases: [4D 时空推理, 4D 世界模型, 3D point tracks, 时空场景图, 动态世界]
load_when:
  - 问题涉及 4D 时空推理、跨帧几何、动态场景图、动作条件未来预测或世界动态监督
  - 问题涉及视频世界模型为何“看起来真实”却不能转成机器人动作
confidence: working
---

# 4D 时空推理与世界动态

## Agent Load Hints

- Usually pair with: EA-DATA, EA-MODEL, EA-EVAL, EA-SENSOR.
- Raw evidence needed when: 需要具体论文结果、消融、数据规模或事件立场。

## 30 秒摘要

具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。

## 关键判断

- 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
- 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
- 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
- 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
- 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。
- 接触、力、被遮挡几何和可变形物状态常无法从纯视觉历史恢复，需要触觉、力/力矩或深度补充。

## 数据需求

| 数据层 | 最低可用内容 | 主要作用 |
|---|---|---|
| 几何时序 | 3D point tracks、跨帧 correspondence、可见性 mask | 保留点身份、运动和度量一致性 |
| 动作 grounding | action chunk、机器人状态、控制频率、坐标系 | 将预测落到可执行动作空间 |
| 接触状态 | 触觉、力/力矩、接触事件、局部形变 | 补视觉不可观测状态 |
| 失败与恢复 | near-miss、扰动、接管、恢复、进度/奖励 | 学习后果判断和纠错 |
| 数据治理 | 时间同步、标定、episode 切分、监督字段 | 防止异构弱监督被误当真值 |

## 指标与检核

| 层级 | 可用指标 |
|---|---|
| 表征 | 点/物体身份一致性、3D 轨迹误差、遮挡恢复、相机运动解耦 |
| 预测 | 几何 correspondence、接触一致性、长程漂移、action fidelity |
| 控制 | 候选动作排序相关性、闭环成功率提升、恢复率、推理延迟 |
| 交互 | 瞬态证据、不可逆时间窗口、跨模态主动感知、失败检测 |

## 适用边界

- 4D 伪标注适合学习相对几何和运动先验，不应自动视为高精度控制真值。
- 训练期几何教师可以提高内部动态表征，但推理期是否保留显式几何取决于延迟和系统成本。
- 世界模型可用于数据生成、离线评估、动作筛选和 test-time planning，不能替代真实闭环验收。
- 可变形物、颗粒、长程接触和强遮挡仍是高风险区域。

## 证据锚点

- RUN-4D-REASONING-20260612：`EA-MODEL-2026-4D-0003` 支持 4D point-track privileged supervision；`EA-MODEL-2026-4D-0008..0010` 覆盖几何一致和部署时世界模型。
- RUN-4D-REASONING-20260612：`EA-EVAL-2026-4D-0013..0014` 覆盖 fidelity、长程一致、效率与视觉盲区；`EA-EVAL-2026-4D-0020` 覆盖时空交互评测缺口。
- RUN-4D-DATA-20260612：`EA-DATA-2026-4DDATA-0009..0010` 覆盖异构监督分级；`EA-DATA-2026-4DDATA-0014..0020` 覆盖恢复、接触和采集质控。

## 待补问题

- 建立 4D benchmark 的表征—预测—控制—交互四层最小任务集。
- 明确伪 4D 标注在不同任务族中的精度阈值和适用边界。
- 研究接触丰富任务中视觉、触觉、力与几何状态的统一时间接口。
