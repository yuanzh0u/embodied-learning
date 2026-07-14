---
id: ERR-EMBODIED
title: 具身智能误差分层与溯源
type: topic-card
domain: error-governance
updated: 2026-07-14
source:
  - id: RUN-PERCEPTION-TRACE-20260714
    file: ../../evidence/literature-review-具身数据感知误差溯源-20260714-reader-v1/evidence.jsonl
    locator: 15 selected events; scientific-memo §误差账本模板
  - id: RUN-PERCEPTION-COGNITION-20260714
    file: ../../evidence/literature-review-具身数据感知误差与认知误差区别-20260714-reader-v1/evidence.jsonl
    locator: EA-PVC-2026-0001..0007 and reused perception events
  - id: RUN-SENSOR-ERROR-20260714
    file: ../../evidence/literature-review-具身传感器感知误差-20260714-reader-v1/evidence.jsonl
    locator: EA-SENSOR-2026-0001..0011; EA-EVAL-2026-0007,0012
tags: [error-governance, embodied-ai, perception-error, cognitive-error, traceability, error-ledger]
aliases: [具身误差, 感知误差, 认知误差, 误差溯源, 误差账本, 第一偏离点]
load_when:
  - 问题涉及机器人失败归因、感知误差与认知误差区别、传感器错误或闭环错误追踪
  - 问题需要从一次部署失败反查数据、模态、动作、控制和评测环节
confidence: working
---

# 具身智能误差分层与溯源

## Agent Load Hints

- Usually pair with: ERR-PATTERN, EA-DATA, EA-SENSOR, EA-ALIGN, EA-EVAL.
- Raw evidence needed when: 需要具体 probing、失败恢复或世界模型 admissibility 实验。

## 30 秒摘要

具身错误不应按“哪个模型模块报错”粗分，而应寻找第一处可证伪偏离点。感知误差发生在真实世界到状态表征：关键状态没被看到、对齐或记录；认知误差发生在状态表征到意图、计划或动作选择：可用状态足够，但任务、约束、阶段或未来后果判断错误。动作转译、控制执行和硬件响应还应单独记账。可靠归因依赖 probing、episode 遥测、对照实验和闭环结果，不能从失败表象直接猜测。

## 关键判断

- “看对了但做错了”可以通过 probing 证明：视觉骨干保持空间表征，而动作头塌缩回记忆轨迹。
- 动作语义、坐标系、控制频率和本体 adapter 错配常伪装成感知误差。
- 接触不可见、标定/同步偏差和缺失模态属于感知链问题；失败阶段判断、计划不可行和 what-if 推理缺失属于认知链问题。
- 失败恢复是最适合分层诊断的实验场：依次检查状态可见、恢复数据存在、失败阶段判断和纠正动作可执行。
- 世界模型横跨两层：未来状态预测保真属于感知型问题，候选动作排序与拒绝属于认知型问题。
- 只有能解释或改善闭环成功、恢复、碰撞、过力和接管的诊断信号，才算有效溯源。

## 第一处偏离判据

| 层级 | 第一处可证伪偏离 | 典型证据 |
|---|---|---|
| 感知 | 世界 → 状态表征 | 可见率、接触事件、同步残差、位姿/标定误差 |
| 认知 | 状态表征 → 意图/计划 | probing、failure-mode 分类、阶段判断、plan feasibility |
| 动作转译 | 计划 → 控制命令 | action adapter、坐标系、归一化、控制频率 |
| 控制执行 | 控制命令 → 物理后果 | action-state residual、延迟、过力、硬件状态 |
| 评测 | 物理后果 → 结论 | 闭环指标、sim-real ranking、admissibility、人工复核 |

## 误差账本

| 账本层 | 常见来源 | 最小记录 |
|---|---|---|
| 观测/传感 | 遮挡、接触不可见、照明、漂移 | 原始模态、可见性、置信度、接触/力事件 |
| 同步/标定 | timestamp gap、外参偏差、action-state 错位 | 时间戳、标定版本、跨模态残差 |
| episode 质量 | 停顿、振荡、过度纠正、关节极限 | progress、smoothness、stall、joint-limit proximity |
| 监督可靠性 | 缺失字段被当真值、人类视频不可执行 | supervision mask、字段白名单、sim filtering |
| 动作/本体 | 坐标系、频率、adapter、动力学错配 | action semantics、state delta、controller metadata |
| 认知/阶段 | 子目标、失败模式、未来后果判断错误 | stage、plan、reward、verification result |
| 闭环结果 | 离线指标与部署不一致 | 成功、恢复、碰撞、过力、接管、真实对照 |

## 快速对照实验

- 换传感器或补模态后失败消失：优先归因感知链。
- 感知输入不变、换推理或动作头后失败消失：优先归因认知或动作转译。
- 控制命令一致但物理后果不一致：检查控制器、延迟、硬件和接触动力学。
- 世界模型视频更真实但动作排序不改善：评测器不具备决策 admissibility。

## 适用边界

- 第一偏离点是一种工程诊断规则，不代表各层统计独立；感知噪声仍会向认知和控制传播。
- 模块名不能替代责任边界：语言头可能产生动作转译误差，视觉模型也可能参与认知规划。
- 多数现有证据仍来自 benchmark、仿真或作者报告的实机任务，事故级跨系统追责尚缺统一标准。

## 证据锚点

- RUN-PERCEPTION-COGNITION-20260714：`EA-PVC-2026-0002..0005` 覆盖推理—动作转译、感知/动作解耦、失败恢复和阶段验证；`EA-PVC-2026-0007` 覆盖 what-if 规划错误。
- RUN-PERCEPTION-TRACE-20260714：15 条事件共同支持观测、同步、监督、动作、本体和闭环七层误差账本；该分类为跨事件 `inference`。
- RUN-SENSOR-ERROR-20260714：`EA-SENSOR-2026-0001..0011` 覆盖接触、几何、置信度和融合误差；`EA-EVAL-2026-0012` 支持世界模型 admissibility 缺口。

## 待补问题

- 建立统一的具身失败 provenance schema 和事故级回放格式。
- 将传感器漂移、磨损、标定版本和模型版本纳入长期误差预算。
- 设计“感知输入不变、只换认知/动作头”的标准对照评测。
