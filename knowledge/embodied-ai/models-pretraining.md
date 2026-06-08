---
id: EA-MODEL
title: 模型与预训练
type: topic-card
domain: embodied-ai
updated: 2026-06-05
source:
  - id: S-EA-QUESTIONS
    file: ../../具身智能研究问题清单.md
    locator: lines 303-359
tags: [embodied-ai, model, pretraining, vla, rt-x, octo, openvla, sim2real]
aliases: [机器人基础模型, Unified Model, VLA, Octo, OpenVLA, RT-X, 预训练, 微调]
load_when:
  - 问题涉及统一机器人模型、VLA、开源模型泛化、预训练有效性或 Sim2Real
confidence: working
---

# 模型与预训练

## Agent Load Hints

- Usually pair with: EA-DATA, EA-XEMBODIMENT, EA-EVAL.
- Raw source needed when: 需要具体模型或论文引用编号。

## 30 秒摘要

机器人统一模型会成为重要方向，但短中期更可能是“共享骨干 + 本体/任务适配器”，而不是一个模型直接控制所有机器人。当前已有机器人基础模型雏形，但不具备大语言模型那样的成熟度，因为机器人数据昂贵、动作空间异构、评测必须闭环、失败有物理代价。预训练价值应通过目标任务真实闭环样本复杂度下降来验证，而不是只看训练 loss 或 benchmark 分数。

## 关键判断

- VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
- Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
- Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
- 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
- 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- 仿真可降低筛选成本，但真实机器人评测仍是最终证据。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 离线预训练 | action prediction loss、next state prediction、任务阶段分类、OOD 距离 |
| 迁移价值 | 目标演示数下降、少样本成功率、transfer matrix、负迁移检查 |
| 真实泛化 | 跨物体/场景/任务成功率、失败恢复率、人工接管次数 |
| 系统问题定位 | 开放环误差、闭环失败分类、控制延迟、标定偏差 |
| Sim2Real | sim-real correlation、真实噪声注入、延迟建模、少量真实验证 |

## 适用边界

- 当前统一模型更适合作为初始化、表征模型、高层 planner 或 action prior。
- 工业部署必须结合目标本体数据、动作接口校准、底层控制器和闭环评测。
- 高接触、柔性物、透明/反光物和长程任务对预训练泛化要求更高，风险也更大。

## 证据锚点

- S-EA-QUESTIONS:56-58 覆盖 Unified Model 和 scaling 挑战。
- S-EA-QUESTIONS:59-62 覆盖 benchmark 与真实泛化问题。
- S-EA-QUESTIONS:63-66 覆盖预训练评估和 Sim2Real。

## 待补问题

- 建立公开 VLA 模型比较表。
- 把模型失败拆成数据、模型、控制、硬件和任务定义五类。
- 补充企业内部复验预训练价值的实验设计模板。
