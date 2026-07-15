---
id: EA-EVAL
title: 评测体系与世界模型
type: topic-card
domain: embodied-ai
updated: 2026-07-15
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §六 评测体系与世界模型(Q16-Q17)
  - id: RUN-WMEVAL-20260714
    file: ../../evidence/literature-review-世界模型评测边界-20260714-reader-v2/evidence.jsonl
    locator: EA-WMEVAL-READ-0001..0015
  - id: RUN-WMDATA-20260714
    file: ../../evidence/literature-review-世界模型需要什么样的训练数据-20260714-reader-v2/evidence.jsonl
    locator: EA-WMDATA-READ-0001..0015
  - id: RUN-SENSOR-ERROR-20260714
    file: ../../evidence/literature-review-具身传感器感知误差-20260714-reader-v2/evidence.jsonl
    locator: EA-SENSORERR-READ-0001..0015
  - id: RUN-VLOC-20260715
    file: ../../evidence/literature-review-近一年图像视觉定位方法的发展与挑战-20260715/evidence.jsonl
    locator: EA-VLOC-2026-0004; EA-VLOC-2026-0006; EA-VLOC-2026-0008..0011; EA-VLOC-2026-0015
tags: [embodied-ai, evaluation, benchmark, closed-loop, world-model, sim-real, admissibility, action-fidelity, risk-coverage, visual-localization]
aliases: [评测体系, 闭环评测, 开放环评测, 世界模型, Benchmark, Sim2Real, 动作忠实, 世界模型可采信性, 风险覆盖, 定位评测]
load_when:
  - 问题涉及具身智能评测、benchmark、开放环/闭环、世界模型或长程规划
  - 问题涉及 world-model admissibility、动作忠实、反事实、乐观偏差或策略评估器可信度
confidence: working
---

# 评测体系与世界模型

## Agent Load Hints

- Usually pair with: EA-MODEL, EA-DATA, EA-BIZ, EA-4D, ERR-PATTERN, ERR-EMBODIED.
- Raw source needed when: 需要具体 benchmark 和世界模型论文引用。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 进入世界模型相关 run；评测裁决需要同时读取 limit/gap 事件，不能只加载支持性论文。

## 30 秒摘要

开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测应分开记录预测保真与决策有效，防止“视频更真实”掩盖错误动作响应。

## 关键判断

- 机器人策略最终必须在真实或高保真仿真闭环中验证。
- 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
- 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
- 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
- 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- 世界模型评测应覆盖 action-following fidelity、physics adherence、failure optimism、反事实和对抗约束。
- 稀疏的 approach、contact、grasp、release 等关键事件必须保留，普通视频抽帧会删除动作所需信号。
- Goal Success 会高估柔性物和接触任务，应同时记录 Safety Success、形变、滑移、掉落和过力。
- 外部世界模型验证也会被上游感知污染，并受封闭词表和动力学验证能力限制。
- 预测保真属于感知账本，候选动作排序、拒绝和 what-if 规划属于认知账本。
- 视觉定位的 Recall@K 只评估候选前端；最终验收还要覆盖几何验证、位姿误差、可恢复域、连续失定位和恢复能力。
- 定位拒识必须用风险—覆盖曲线评估；固定地理半径真值也要与视觉重叠、地形高度和任务可达性做一致性审计。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 开放环 | 动作误差、trajectory likelihood、阶段预测、数据分布内外表现 |
| 闭环 | 成功率、平均完成时间、失败恢复率、人工接管、连续运行小时 |
| 安全 | 碰撞次数、过力次数、急停、越界、人机距离违规 |
| 稳定性 | MTBF、重试次数、成功率方差、标定频率 |
| 世界模型 | 多步预测一致性、物体永久性、几何/接触一致、action fidelity、sim-real ranking |
| 可采信性 | physics adherence、failure optimism、反事实、对抗约束、排序相关性 |
| 过程安全 | Safety Success、滑移/掉落、形变、过力、碰撞、接管 |
| 效率 | 关键事件保留、rollout 延迟、在线规划预算、恢复耗时 |
| 视觉定位 | 分条件 Recall@K、PnP/细化成功率、6DoF 误差、风险—覆盖、连续失定位时长、恢复率 |

## 适用边界

- 仿真适合算法 ablation、危险动作过滤、失败模式预筛和控制器调参。
- 高接触、柔性物、透明/反光物、复杂摩擦和触觉任务必须做真实验证。
- 世界模型近期更适合作离线评估、候选动作筛选和数据生成工具。
- 未通过真实闭环或可靠 sim-real ranking 的世界模型，不应单独承担上线验收或安全裁决。
- 视觉一致但接触、动作或奖励响应错误的模型不具备策略评估 admissibility。
- 允许拒识的定位安全结论只适用于系统可以停机、重定位或切换传感器的场景；必须持续输出位姿时，低覆盖会转化为任务风险。

## 证据锚点

- S-EA-QUESTIONS:67-70 覆盖具身智能评测。
- S-EA-QUESTIONS:71-75 覆盖世界模型。
- RUN-WMEVAL-20260714：`EA-WMEVAL-READ-0001..0015` 覆盖异构监督、外部可查询状态、关键事件保留、动作/物理忠实、长程效率、具身锚定合成数据和下游动作质量目标。
- RUN-WMDATA-20260714：`EA-WMDATA-READ-0003..0007`, `0015` 支持关键事件、具身锚定合成数据、sim-real 对齐、动作质量目标和长程 rollout 可用性。
- RUN-SENSOR-ERROR-20260714：`EA-SENSORERR-READ-0002`, `0005..0009` 支持局部执行走廊、Safety Success、world-model admissibility 和部署置信度。
- RUN-VLOC-20260715：`EA-VLOC-2026-0004`, `0006`, `0008..0011`, `0015` 支持不确定性拒识、真值协议、初始化/几何失败、风险—覆盖和地理长尾评测边界。

## 待补问题

- 建立任务族评测模板。
- 补充 PoC、实验室 benchmark、工业验收之间的指标映射。
- 整理世界模型可落地用法与不可替代真实验证的边界。
- 建立预测保真、决策有效和安全裁决三套分账指标。
- 建立贯通 VPR、几何验证、最终位姿和任务恢复的定位评测模板。
