---
id: EA-SENSOR
title: 传感器与多模态感知
type: topic-card
domain: embodied-ai
updated: 2026-07-10
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §二 传感器与多模态感知(Q4-Q5)
  - id: RUN-TACTILE-WM-20260623
    file: ../../evidence/literature-review-tactile-world-model-20260623/evidence.jsonl
    locator: EA-TWM-2026-0001..0018
  - id: RUN-SENSOR-ERROR-20260709
    file: ../../evidence/literature-review-embodied-sensor-perception-error-2026-07-09/evidence.jsonl
    locator: EA-SENSOR-2026-0001..0011; EA-EVAL-2026-0007,0012
  - id: RUN-UMI-QUALITY-20260606
    file: ../../evidence/literature-review-umi-data-quality-six-month-20260606/evidence.jsonl
    locator: 5 accepted UMI events
tags: [embodied-ai, sensors, multimodal, rgb, point-cloud, tactile, force, proprioception, perception-error, tactile-world-model]
aliases: [传感器, 多模态感知, 触觉, 力控, 点云, 3D, RGB, 触觉世界模型, 感知误差]
load_when:
  - 问题涉及 RGB、深度、点云、触觉、力/力矩、接触状态、材料属性或传感器组合
  - 问题涉及传感器感知误差、模态融合污染、触觉未来预测、漂移磨损或世界模型接触状态
confidence: working
---

# 传感器与多模态感知

## Agent Load Hints

- Usually pair with: EA-DATA, EA-HARDWARE, EA-BIZ, EA-4D, ERR-EMBODIED.
- Raw source needed when: 需要触觉标准化、触觉任务清单或具体论文编号。

## 30 秒摘要

视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；触觉世界模型应预测动作条件下的接触演化，而不只是重建触觉图像。多模态建模的目标不是堆传感器，而是让每个模态在闭环中产生可验证收益且不污染已有先验。

## 关键判断

- RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
- 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
- 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
- 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
- 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- 触觉数据集要把磨损、漂移、换件和跨实例泛化当作数据集的一部分。
- 传感器误差应分为观测、接触、融合和评测四层，并记录每层的残差与版本信息。
- 触觉是稀疏、事件驱动信号；接触门控、时间同步和 action horizon 决定融合是否有效。
- 无约束触觉注入可能污染视觉 dynamics model，多模态不是无条件增益。
- 全局异常检测不足以代表任务风险；监控应关注当前 action chunk 的局部执行走廊。
- 触觉世界模型只有进入 MPC、动作验证、anticipatory prior 或反射控制，才证明闭环价值。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 3D 感知 | 深度噪声、位姿误差、遮挡恢复率、空间任务成功率 |
| 触觉 | 接触检测延迟、滑移检测率、压力分布稳定性、跨传感器实例性能 |
| 力/力矩 | 过力次数、接触阈值误报、力控稳定性、异常碰撞检测 |
| 多模态融合 | 模态 dropout 鲁棒性、缺失模态退化、闭环成功率提升 |
| 对齐与融合 | 时间残差、标定投影误差、contact gate、模态污染消融 |
| 过程安全 | Safety Success、滑移/掉落、形变、过力、恢复率 |
| 长期维护 | 漂移曲线、磨损、换件重标定、跨传感器实例退化 |

## 适用边界

- 开放空间、刚体、视觉可见任务：视觉模型可能已足够形成可用策略。
- 透明/反光/遮挡/软物/精密插入/易碎物：需要 3D、触觉、力控或柔顺执行补充。
- 多模态方案必须按任务收益验证，否则会增加标定、带宽、同步和维护成本。
- 触觉或力觉结果通常硬件特定，不能从单一传感器和小规模任务直接外推为通用能力。
- 世界模型预测视觉逼真不等于接触和动作响应正确，必须经过 admissibility 与真实闭环验证。

## 证据锚点

- S-EA-QUESTIONS:19-22 覆盖 RGB、3D、点云和物理模态。
- S-EA-QUESTIONS:23-29 覆盖触觉与视觉、力、pose 的关系，以及触觉标准化。
- RUN-TACTILE-WM-20260623：`EA-TWM-2026-0001..0003`, `0007..0012` 覆盖表征兼容、触觉未来、接触门控和推理期使用。
- RUN-SENSOR-ERROR-20260709：`EA-SENSOR-2026-0001..0011` 覆盖接触、几何、置信度、融合和事件视觉误差；`EA-EVAL-2026-0012` 覆盖世界模型 admissibility。
- RUN-UMI-QUALITY-20260606：UMI-FT、OmniUMI 与 UMI-3D 支持力/触觉、深度和 3D tracking 对采集质量的条件性增益。

## 待补问题

- 建立不同任务族的最小传感器组合建议。
- 补一份触觉数据标准字段表。
- 把“最后一厘米”拆成视觉、力控、触觉、末端执行器和柔顺控制的接口规范。
- 建立跨传感器实例、磨损和维护周期的长期基准。
