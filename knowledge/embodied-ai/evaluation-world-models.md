---
id: EA-EVAL
title: 评测体系与世界模型
type: topic-card
domain: embodied-ai
updated: 2026-07-08
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §六 评测体系与世界模型(Q16-Q17)
tags: [embodied-ai, evaluation, benchmark, closed-loop, world-model, sim-real]
aliases: [评测体系, 闭环评测, 开放环评测, 世界模型, Benchmark, Sim2Real]
load_when:
  - 问题涉及具身智能评测、benchmark、开放环/闭环、世界模型或长程规划
confidence: working
---

# 评测体系与世界模型

## Agent Load Hints

- Usually pair with: EA-MODEL, EA-DATA, EA-BIZ, ERR-PATTERN.
- Raw source needed when: 需要具体 benchmark 和世界模型论文引用。

## 30 秒摘要

开放环评测适合快速筛模型，但不能替代闭环成功率。闭环评测难在误差会改变后续观测并累积，还涉及硬件安全、任务重置、失败恢复和随机接触。当前没有覆盖全行业、全本体、全任务的统一评测体系，未来更可能按任务族分层。世界模型当前主要解决预测、想象和筛选问题，能辅助规划和降低试错成本，但还不能替代真实环境验证。

## 关键判断

- 机器人策略最终必须在真实或高保真仿真闭环中验证。
- 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
- 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
- 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
- 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 开放环 | 动作误差、trajectory likelihood、阶段预测、数据分布内外表现 |
| 闭环 | 成功率、平均完成时间、失败恢复率、人工接管、连续运行小时 |
| 安全 | 碰撞次数、过力次数、急停、越界、人机距离违规 |
| 稳定性 | MTBF、重试次数、成功率方差、标定频率 |
| 世界模型 | 多步预测一致性、物体永久性、接触结果预测、sim-real ranking |

## 适用边界

- 仿真适合算法 ablation、危险动作过滤、失败模式预筛和控制器调参。
- 高接触、柔性物、透明/反光物、复杂摩擦和触觉任务必须做真实验证。
- 世界模型近期更适合作离线评估、候选动作筛选和数据生成工具。

## 证据锚点

- S-EA-QUESTIONS:67-70 覆盖具身智能评测。
- S-EA-QUESTIONS:71-75 覆盖世界模型。

## 待补问题

- 建立任务族评测模板。
- 补充 PoC、实验室 benchmark、工业验收之间的指标映射。
- 整理世界模型可落地用法与不可替代真实验证的边界。
