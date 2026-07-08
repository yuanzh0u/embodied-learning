---
id: EA-XEMBODIMENT
title: 跨本体与数据迁移
type: topic-card
domain: embodied-ai
updated: 2026-07-08
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §四 跨本体与数据迁移(Q10-Q12)
tags: [embodied-ai, cross-embodiment, retargeting, dexterous-hand, gripper, action-space]
aliases: [跨本体, Retargeting, 人手迁移, 灵巧手, 夹爪, 动作空间]
load_when:
  - 问题涉及人手数据迁移、灵巧手与夹爪统一学习、retargeting 或本体适配
confidence: working
---

# 跨本体与数据迁移

## Agent Load Hints

- Usually pair with: EA-MODEL, EA-SENSOR.
- Raw source needed when: 需要 DexPilot、AnyTeleop、DexCap、DEXOP 等具体引用。

## 30 秒摘要

跨本体迁移的核心不是复制姿态，而是保留任务相关接触功能。人手 26 自由度数据映射到灵巧手、双指夹爪或多指夹爪时，应优先抽象抓取意图、接触区域、物体中心轨迹和 affordance，而不是逐关节模仿。统一模型可以共享感知和任务表征，但低层动作通常需要本体适配器、动作头、IK、MPC、RL 或真实闭环校准。迁移上限由目标机器人真实物理能力和反馈可观测性决定。

## 关键判断

- 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
- 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
- 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
- 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
- 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 映射质量 | 可达率、自碰撞率、关节限位违规、动作平滑度 |
| 接触保持 | 接触点一致性、滑移率、力闭合质量、物体稳定性 |
| 迁移效果 | 少样本微调成功率、跨本体成功率、失败恢复率 |
| 安全执行 | 过力次数、碰撞次数、不可达动作比例、人工接管 |

## 适用边界

- 语义、目标状态、粗动作和任务阶段迁移上限较高。
- 精细接触、in-hand manipulation、柔性物和高公差装配迁移上限较低。
- 如果目标本体缺少必要自由度、力控或触觉，模型无法凭空迁移同等技能。

## 证据锚点

- S-EA-QUESTIONS:46-48 覆盖人手数据到不同机器人本体的映射。
- S-EA-QUESTIONS:49-52 覆盖跨本体预训练和迁移上限。
- S-EA-QUESTIONS:53-55 覆盖 retargeting 瓶颈和优化方向。

## 待补问题

- 建立“形似 vs 功能等价”的 retargeting 评估框架。
- 补充不同机器人手/夹爪的中间表示适配表。
- 整理 paired human-robot data 的可用公开资源。
