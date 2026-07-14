---
id: ERR-PATTERN
title: 可迁移的误差治理模式
type: topic-card
domain: error-governance
updated: 2026-07-14
source:
  - id: S-ERR-COMPARE
    status: retired
    archive: "git show 081e898:测绘误差观与大模型误差治理比较.md"
    locator: §四 二者能否互补、§五 测绘方法能补大模型行业的短板、§六 大模型行业能反哺测绘行业
  - id: RUN-PERCEPTION-COGNITION-20260714
    file: ../../evidence/literature-review-具身数据感知误差与认知误差区别-20260714-reader-v2/evidence.jsonl
    locator: ERR-PVC-READ-0001..0015
  - id: RUN-PERCEPTION-TRACE-20260714
    file: ../../evidence/literature-review-具身数据感知误差溯源-20260714-reader-v2/evidence.jsonl
    locator: ERR-TRACE-READ-0001..0015
tags: [error-governance, error-budget, redundancy, residual-analysis, acceptance, risk-grade]
aliases: [误差预算, 冗余检核, 残差分析, 精度分级, 适用边界, 可信智能]
load_when:
  - 问题涉及如何把测绘质量控制迁移到 AI、智能体、具身智能或工程验收
confidence: working
---

# 可迁移的误差治理模式

## Agent Load Hints

- Usually pair with: ERR-COMPARE, ERR-EMBODIED, EA-EVAL, EA-BIZ.
- Raw source needed when: 需要红利、不能机械照搬或最终判断的完整论述。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 进入误差类 run；跨事件治理框架必须明确标记为 synthesis/inference。

## 30 秒摘要

测绘方法对 AI 的价值不是公式照搬，而是工程精神迁移：误差预算、冗余检核、精度分级、误差传播、残差分析和成果验收。具身系统还应寻找“第一处可证伪偏离点”，按世界到表征、表征到计划、计划到控制、控制到物理后果分账，避免把所有失败都归因于感知或模型。最终目标是让可信系统说明误差来源、传播路径、适用边界、可信等级和风险后果。

## 关键模式

| 测绘概念 | AI / 具身智能迁移 |
|---|---|
| 误差预算 | 拆分数据、传感器、标定、模型、控制、检索、工具和评测误差 |
| 冗余观测 | 多源证据、多个工具、独立校验器、人工复核 |
| 精度分级 | 场景可信等级、风险等级、自动化等级 |
| 误差传播 | 追踪上游数据或工具错误如何影响最终输出/动作 |
| 残差分析 | 分析输出与证据、约束、工具结果、任务目标之间的偏离 |
| 成果验收 | 上线前后 eval、监控、回归、复核和降级策略 |
| 第一偏离点 | 找到世界→表征→计划→控制→后果链中最早可被证据否定的环节 |

## 具身智能应用

- 数据采集：把时间同步、标定、传感器噪声和采集员差异纳入误差预算。
- 策略模型：区分数据问题、模型问题、控制问题和硬件问题。
- 闭环评测：记录成功率之外的失败类型、接管、过力、碰撞和恢复能力。
- 工业落地：给出适用工况、节拍边界、安全边界和维护要求。
- 智能体工具链：对关键工具调用结果做交叉验证和反向验证。
- 失败溯源：用 probing、遥测和对照实验确认第一偏离点，再决定补传感、改推理或修控制。

## 指标与检核

| 关注点 | 可用问题 |
|---|---|
| 来源 | 错误从哪里来 |
| 传播 | 哪些环节放大错误 |
| 检核 | 是否有独立证据或工具复核 |
| 分级 | 该输出/动作属于什么可信等级 |
| 边界 | 哪些场景必须降级、拒绝或人工复核 |
| 验收 | 是否通过上线前后持续评测 |

## 适用边界

- 适合高风险、工程化、需验收、需追责的 AI 和具身智能系统。
- 不适合把复杂语义问题简化成单一数值误差。
- 需要结合场景任务定义，不能只移植测绘术语。

## 证据锚点

- S-ERR-COMPARE:232-298 覆盖误差预算、冗余检核、适用范围、误差传播和残差分析。
- S-ERR-COMPARE:300-391 覆盖大模型反哺测绘和可能红利。
- S-ERR-COMPARE:393-419 覆盖不能机械照搬和最终判断。
- RUN-PERCEPTION-COGNITION-20260714：`ERR-PVC-READ-0005`, `0009..0014` 支持感知/认知/动作转译解耦、阶段验证、失败恢复、probing 和 what-if 规划。
- RUN-PERCEPTION-TRACE-20260714：`ERR-TRACE-READ-0001..0015` 支持把同步、监督、动作语义、轨迹效用、几何和局部风险纳入误差预算；分层账本与第一偏离点规则为跨事件 `inference`。

## 待补问题

- 建立“具身智能 PoC 验收报告”模板。
- 将误差治理模式嵌入新素材入库时的证据等级字段。
- 将第一偏离点、传播路径和恢复验证纳入统一事故回放格式。
