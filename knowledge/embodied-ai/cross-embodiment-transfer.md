---
id: EA-XEMBODIMENT
title: 跨本体与数据迁移
type: topic-card
domain: embodied-ai
updated: 2026-07-20
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
  - id: RUN-LOCOMANIP-20260719
    file: ../../evidence/literature-review-近一年-loco-manipulation-研究进展-20260719/evidence.jsonl
    locator: EA-LOCOMANIP-2026-0005..0006; EA-LOCOMANIP-2026-0008..0009; EA-LOCOMANIP-2026-0013; EA-LOCOMANIP-2026-0018; EA-LOCOMANIP-2026-0020
  - id: RUN-MULTIMODAL-TRAINING-20260720
    file: ../../evidence/literature-review-近一年触觉-力觉-视觉-语言等多模态数据在具身机器人训练方法中的演进-20260720/evidence.jsonl
    locator: EA-ALIGN-READ-0001..0005; EA-TWM-READ-0001..0003; EA-TWM-READ-0010..0011; EA-LOCOMANIP-2026-0006; EA-LOCOMANIP-2026-0012; EA-LOCOMANIP-2026-0018; EA-LOCOMANIP-2026-0021
tags: [embodied-ai, cross-embodiment, retargeting, dexterous-hand, gripper, action-space, sensor-adaptation, state-change]
aliases: [跨本体, Retargeting, 人手迁移, 灵巧手, 夹爪, 动作空间, 状态变化接口, 目标硬件适配]
load_when:
  - 问题涉及人手数据迁移、灵巧手与夹爪统一学习、retargeting 或本体适配
  - 问题涉及多模态跨平台迁移、传感器硬件差异、状态变化共享接口或少量目标硬件适配
confidence: working
---

# 跨本体与数据迁移

## Agent Load Hints

- Usually pair with: EA-MODEL, EA-SENSOR.
- Raw source needed when: 需要 DexPilot、AnyTeleop、DexCap、DEXOP 等具体引用。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 进入 VLA 对齐与 UMI run；核验跨本体结论时必须同时读取机器人状态、控制器和接触条件。

## 30 秒摘要

跨本体迁移的核心不是复制姿态、控制命令或传感器 token，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。语言/视觉语义、对象状态变化和粗运动先验较易共享；局部接触载荷、传感器频率、硬件标定和控制接口更依赖目标平台。更稳健的路线是共享 Cartesian/object state delta 或接触目标，再由机器人和传感器特定 adapter、少量目标硬件数据与真实闭环校准落地。

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
- 在 humanoid loco-manipulation 中，robot-free 数据更稳定地迁移语义、物体与粗运动先验；新接触动作仍更依赖同形态数据和目标机器人闭环锚定。
- 人体示范的结构化扩增可显著提升任务策略，但技能分段、环境模型、成功判据和固定技能顺序会把迁移成本转移到任务工程。
- 多模态迁移也应区分“可共享状态”与“硬件特定观测”：视觉语义和动作条件状态变化可作为中间接口，触觉图样、六维载荷、采样频率与漂移不能直接跨平台等同。
- 硬件依赖模态更适合用少量目标传感器数据适配既有视觉/动作策略，而不是要求预训练阶段穷尽所有传感器形态。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 映射质量 | 可达率、自碰撞率、关节限位违规、动作平滑度 |
| 接触保持 | 接触点一致性、滑移率、力闭合质量、物体稳定性 |
| 迁移效果 | 少样本微调成功率、跨本体成功率、失败恢复率 |
| 安全执行 | 过力次数、碰撞次数、不可达动作比例、人工接管 |
| Adapter | state-delta 重建、命令到状态残差、少样本校准量、跨硬件单元方差 |
| 传感器迁移 | 目标硬件样本量、跨实例退化、重标定成本、缺失模态退化、接触状态一致性 |

## 适用边界

- 语义、目标状态、粗动作和任务阶段迁移上限较高。
- 精细接触、in-hand manipulation、柔性物和高公差装配迁移上限较低。
- 如果目标本体缺少必要自由度、力控或触觉，模型无法凭空迁移同等技能。
- 朴素合并异构 action token 容易负迁移；必须先验证动作语义和状态变化是否可比。
- 共享 action-conditioned state change 只能缓解接口差异，不能消除触觉材料、安装位置、力/力矩量程和控制频率的硬件依赖。

## 证据锚点

- S-EA-QUESTIONS:46-48 覆盖人手数据到不同机器人本体的映射。
- S-EA-QUESTIONS:49-52 覆盖跨本体预训练和迁移上限。
- S-EA-QUESTIONS:53-55 覆盖 retargeting 瓶颈和优化方向。
- RUN-VLA-ALIGN-20260714：`EA-ALIGN-READ-0001`, `0003..0005` 支持控制命令非通用性、状态条件动作解码、系统对齐和平台特定 adapter；`0009` 支持 contact-rich 失败修正。
- RUN-UMI-QUALITY-20260714：`EA-UMI-READ-0002..0004`, `0009` 支持物理模态、3D sensing 和机器人可执行性过滤；跨本体可用性是条件结论，不等于动作命令可直接复用。
- RUN-EGO-DATA-20260715：`EA-EGO-2026-0001`, `0008..0011`, `0019..0020` 支持目标机器人锚定、人机对齐中间训练、人工重定向成本以及接触几何对迁移成功的独立作用。
- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0008..0009`, `0013`, `0020` 共同限定 robot-free、人类第一视角、生成数据和同形态数据的迁移分工；`0005..0006`, `0018` 支持几何接触、潜在动作和物理 retargeting 对全身执行的作用。
- RUN-MULTIMODAL-TRAINING-20260720：`EA-ALIGN-READ-0001..0005`, `EA-TWM-READ-0001..0003`, `0010..0011`, `EA-LOCOMANIP-2026-0006`, `0012`, `0018`, `0021` 支持状态变化共享接口、选择性多模态耦合与少量目标硬件适配；结论为复用证据的跨 run synthesis。

## 待补问题

- 建立“形似 vs 功能等价”的 retargeting 评估框架。
- 补充不同机器人手/夹爪的中间表示适配表。
- 整理 paired human-robot data 的可用公开资源。
- 建立 action semantics 与 controller metadata 的跨本体字段规范。
- 建立机器人本体、传感器型号、标定版本和控制频率共同条件化的多模态 adapter 基准。
