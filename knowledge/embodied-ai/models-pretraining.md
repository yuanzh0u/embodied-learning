---
id: EA-MODEL
title: 模型与预训练
type: topic-card
domain: embodied-ai
updated: 2026-07-15
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §五 模型与预训练(Q13-Q15)
  - id: RUN-VLA-ALIGN-20260714
    file: ../../evidence/literature-review-sparse-language-dense-vision-and-continuous-action-alignment-in-vla-syst-20260714-reader-v2/evidence.jsonl
    locator: EA-ALIGN-READ-0001..0015
  - id: RUN-WMDATA-20260714
    file: ../../evidence/literature-review-世界模型需要什么样的训练数据-20260714-reader-v2/evidence.jsonl
    locator: EA-WMDATA-READ-0001..0015
  - id: RUN-4D-REASONING-20260714
    file: ../../evidence/literature-review-4d时空推理-20260714-reader-v2/evidence.jsonl
    locator: EA-4D-READ-0001..0015
  - id: RUN-EGO-DATA-20260715
    file: ../../evidence/literature-review-ego-centric-数据在具身模型训练中的问题与困难-20260715/evidence.jsonl
    locator: EA-EGO-2026-0001..0002; EA-EGO-2026-0007..0008; EA-EGO-2026-0011; EA-EGO-2026-0014; EA-EGO-2026-0018
tags: [embodied-ai, model, pretraining, vla, rt-x, octo, openvla, sim2real, ego-centric]
aliases: [机器人基础模型, Unified Model, VLA, Octo, OpenVLA, RT-X, 预训练, 微调, Ego-centric预训练]
load_when:
  - 问题涉及统一机器人模型、VLA、开源模型泛化、预训练有效性或 Sim2Real
confidence: working
---

# 模型与预训练

## Agent Load Hints

- Usually pair with: EA-DATA, EA-XEMBODIMENT, EA-EVAL, EA-ALIGN, EA-4D.
- Raw source needed when: 需要具体模型或论文引用编号。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 选择 run；中预算读 review packet，高预算按 paper-note index 核验。

## 30 秒摘要

机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。VLA 可以继承视觉和语言先验，却不会自动继承运动、接触和控制器先验；语言—视觉—动作接口需要显式对齐。Ego-centric 人类视频可扩展行为与视点先验，但只有经过动作恢复、本体对齐和目标机器人锚定后，才可能转成可执行控制。4D 和世界模型可以提供几何动态监督、未来想象和动作筛选，但训练目标必须面向动作质量而非只追求视觉重建。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。

## 关键判断

- VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
- Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
- Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
- 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
- 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- 仿真可降低筛选成本，但真实机器人评测仍是最终证据。
- 语言、视觉和动作的主要矛盾是粒度与物理接口错配，不是简单缺少更大的 VLM。
- action module 可通过 motion prior、flow/diffusion 或状态条件 tokenizer 独立学习连续动作结构。
- 4D point tracks 和几何 correspondence 可作为训练期监督，提高动作相关世界动态而不一定增加推理成本。
- 世界动作模型不能只优化视频重建；内部表示还应与接触、轨迹和任务相关区域对齐。
- Ego-centric 预训练存在实测规模收益，但规模与本体对齐是互补条件；没有机器人微调或 aligned human-robot 中间训练时，收益不能直接落到目标控制。
- 缩小 human/robot 视觉外观差距不等于解决动作接口；hand-object 6DoF、接触结构和目标机器人数据仍决定闭环可执行性。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 离线预训练 | action prediction loss、next state prediction、任务阶段分类、OOD 距离 |
| 迁移价值 | 目标演示数下降、少样本成功率、transfer matrix、负迁移检查 |
| 真实泛化 | 跨物体/场景/任务成功率、失败恢复率、人工接管次数 |
| 系统问题定位 | 开放环误差、闭环失败分类、控制延迟、标定偏差 |
| Sim2Real | sim-real correlation、真实噪声注入、延迟建模、少量真实验证 |
| 多模态对齐 | 语言消融、action-grounded attention、动作解码误差、阶段一致性 |
| 世界动态 | 3D correspondence、action fidelity、长程 rollout、未来评分相关性 |
| Ego 预训练 | 有效视频小时、自动标签通过率、robot-anchor 比例、预训练/中间训练/微调消融、真实闭环增益 |

## 适用边界

- 当前统一模型更适合作为初始化、表征模型、高层 planner 或 action prior。
- 工业部署必须结合目标本体数据、动作接口校准、底层控制器和闭环评测。
- 高接触、柔性物、透明/反光物和长程任务对预训练泛化要求更高，风险也更大。
- 现有 Ego-centric 规模曲线来自特定灵巧操作和主动感知设置，不能外推为 raw video 对所有机器人任务都遵循同一 scaling law。

## 证据锚点

- S-EA-QUESTIONS:56-58 覆盖 Unified Model 和 scaling 挑战。
- S-EA-QUESTIONS:59-62 覆盖 benchmark 与真实泛化问题。
- S-EA-QUESTIONS:63-66 覆盖预训练评估和 Sim2Real。
- RUN-VLA-ALIGN-20260714：`EA-ALIGN-READ-0001..0006`, `0013..0015` 覆盖动作语义、结构化接口、跨本体适配以及长程推理与恢复。
- RUN-WMDATA-20260714：`EA-WMDATA-READ-0001..0010` 覆盖异构视频—动作数据、关键事件、具身锚定合成数据、几何未来和失败附近纠正轨迹。
- RUN-4D-REASONING-20260714：`EA-4D-READ-0001..0005`, `0008`, `0014..0015` 覆盖 4D 监督、几何增强 rollout、连续 4D 表征和多视角训练数据。
- RUN-EGO-DATA-20260715：`EA-EGO-2026-0001..0002`, `0007..0008`, `0011`, `0014`, `0018` 支持 Ego 规模收益、本体/动作接口边界、aligned mid-training、目标机器人数据不可缺以及主动视点先验的条件性。

## 待补问题

- 建立公开 VLA 模型比较表。
- 把模型失败拆成数据、模型、控制、硬件和任务定义五类。
- 补充企业内部复验预训练价值的实验设计模板。
- 建立 action prior、离散 tokenizer 和 continuous expert 的统一对照。
- 建立 Ego-human、aligned human-robot 与目标机器人数据的混合比例和边际收益曲线。
