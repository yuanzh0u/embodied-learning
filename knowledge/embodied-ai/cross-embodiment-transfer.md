---
id: EA-XEMBODIMENT
title: 跨本体与数据迁移
type: topic-card
domain: embodied-ai
updated: 2026-07-15
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §四 跨本体与数据迁移(Q10-Q12)
  - id: RUN-VLA-ALIGN-20260714
    file: ../../evidence/literature-review-sparse-language-dense-vision-and-continuous-action-alignment-in-vla-syst-20260714-reader-v2/evidence.jsonl
    locator: EA-ALIGN-READ-0001..0015
  - id: RUN-UMI-QUALITY-20260714
    file: ../../evidence/literature-review-近半年-umi-数据质量-20260714-reader-v2/evidence.jsonl
    locator: EA-UMI-READ-0001..0015
  - id: RUN-EGO-DATA-20260715
    file: ../../evidence/literature-review-ego-centric-数据在具身模型训练中的问题与困难-20260715/evidence.jsonl
    locator: EA-EGO-2026-0001..0020
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
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 进入 VLA 对齐与 UMI run；核验跨本体结论时必须同时读取机器人状态、控制器和接触条件。

## 30 秒摘要

跨本体迁移的核心不是复制姿态或控制命令，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。不同机器人即使记录相同 action command，也可能产生不同运动；更稳健的路线是共享 Cartesian state delta、对象状态变化或接触目标，再由机器人特定 adapter 和真实闭环校准落地。

## 关键判断

- 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
- 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
- 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
- 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
- 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。
- action command 不是跨机器人通用监督信号，数据混合必须保留控制器、频率、坐标系和归一化语义。
- 共享末端、传感器、接触和动作空间的同构采集可减少 retargeting 与 embodiment-conversion 损失。
- motion transfer 不等于 contact transfer；稳定灵巧操作还要迁移接触载荷、力反馈和局部状态。
- Ego-human 数据通常只能部分替代目标机器人示范；少量 paired/aligned robot data 负责定义动作接口和闭环锚点，而非单纯修正视觉外观。
- Ego-centric retargeting 的误差链应分开记录坐标/尺度、运动学可达性、手—物接触和动力学可行性，避免用单一 pose error 掩盖接触失败。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 映射质量 | 可达率、自碰撞率、关节限位违规、动作平滑度 |
| 接触保持 | 接触点一致性、滑移率、力闭合质量、物体稳定性 |
| 迁移效果 | 少样本微调成功率、跨本体成功率、失败恢复率 |
| 安全执行 | 过力次数、碰撞次数、不可达动作比例、人工接管 |
| Adapter | state-delta 重建、命令到状态残差、少样本校准量、跨硬件单元方差 |

## 适用边界

- 语义、目标状态、粗动作和任务阶段迁移上限较高。
- 精细接触、in-hand manipulation、柔性物和高公差装配迁移上限较低。
- 如果目标本体缺少必要自由度、力控或触觉，模型无法凭空迁移同等技能。
- 朴素合并异构 action token 容易负迁移；必须先验证动作语义和状态变化是否可比。

## 证据锚点

- S-EA-QUESTIONS:46-48 覆盖人手数据到不同机器人本体的映射。
- S-EA-QUESTIONS:49-52 覆盖跨本体预训练和迁移上限。
- S-EA-QUESTIONS:53-55 覆盖 retargeting 瓶颈和优化方向。
- RUN-VLA-ALIGN-20260714：`EA-ALIGN-READ-0001`, `0003..0005` 支持控制命令非通用性、状态条件动作解码、系统对齐和平台特定 adapter；`0009` 支持 contact-rich 失败修正。
- RUN-UMI-QUALITY-20260714：`EA-UMI-READ-0002..0004`, `0009` 支持物理模态、3D sensing 和机器人可执行性过滤；跨本体可用性是条件结论，不等于动作命令可直接复用。
- RUN-EGO-DATA-20260715：`EA-EGO-2026-0001`, `0008..0011`, `0019..0020` 支持目标机器人锚定、人机对齐中间训练、人工重定向成本以及接触几何对迁移成功的独立作用。

## 待补问题

- 建立“形似 vs 功能等价”的 retargeting 评估框架。
- 补充不同机器人手/夹爪的中间表示适配表。
- 整理 paired human-robot data 的可用公开资源。
- 建立 action semantics 与 controller metadata 的跨本体字段规范。
