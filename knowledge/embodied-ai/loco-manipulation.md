---
id: EA-LOCOMANIP
title: 全身移动操作
type: topic-card
domain: embodied-ai
updated: 2026-07-20
source:
  - id: RUN-LOCOMANIP-20260719
    file: ../../evidence/literature-review-近一年-loco-manipulation-研究进展-20260719/evidence.jsonl
    locator: EA-LOCOMANIP-2026-0001..0021
tags: [embodied-ai, loco-manipulation, whole-body, humanoid, quadruped, mobile-manipulation, sim2real, safety]
aliases: [Loco-Manipulation, 移动操作, 全身操作, WholeBodyVLA, humanoid manipulation, quadrupedal manipulation]
load_when:
  - 问题涉及移动/行走与操作耦合、全身动作接口、humanoid 或 quadruped 操作
  - 问题涉及全身操作数据采集、异构数据共训、状态估计、地形/接触反馈或长时序计划
  - 问题涉及 loco-manipulation 的真机评测、Sim2Real、故障恢复或 safety–completion 分账
confidence: working
---

# 全身移动操作

## Agent Load Hints

- Usually pair with: EA-MODEL, EA-EVAL, EA-SENSOR, EA-XEMBODIMENT.
- Raw evidence needed when: 需要具体真机试验、成功率、动作接口或状态估计来源。
- Evidence route: 先读 [文献综述成果目录](../literature-review-catalog.md) 中的 LR-LOCOMANIP；核验数字时再进入 review packet、paper note 与 audit。

## 30 秒摘要

Loco-manipulation 正从“上肢操作 + 下肢移动”的模块拼接，转向任务意图与全身执行分层：高层表达目标、阶段和接触意图，低层联合控制手臂、腰腿、足端与夹爪。能力上限首先受完整动作接口、目标本体全身数据和状态可观测性约束，而不是只受模型规模约束。人类视频、robot-free 数据和生成数据可以扩展语义、物体与粗运动先验，但新接触动作仍需要同形态数据和少量目标机器人闭环锚定。当前已有真机长时序、触觉全身控制和故障生存证据，但多来自受控任务；开放环境可靠性的主要瓶颈已上移到状态估计、地形/接触建模、计划可执行性和失败恢复。

## 关键判断

- 原生全身动作接口先于模型规模决定可表达能力；采集接口若不允许深蹲、脚部操作或腰腿协同，后续扩量无法补回这些动作。
- 系统分层边界更适合定义为“任务意图—全身执行”，而不是固定的“上肢—下肢”；规划、状态估计和全身控制需要共享任务阶段与接触目标。
- 异构数据应明确分工：少量目标本体全身数据负责动作锚定，同形态静态操作补充新动作，人类/robot-free 数据扩展物体、语言、场景和粗运动先验。
- 全身动作需要统一的几何、接触或 latent action 接口；仅靠 action-free 人类视频不能自动获得可执行控制，但在统一动作模型下可提供有效先验。
- 地形、目标物体、机器人自身空间状态和执行器故障都属于任务状态；依赖动捕、marker 或 ground-truth plan 的结果必须和机载自治分账。
- 触觉与力反馈应进入低层命令跟踪，同时影响夹爪、手臂和身体稳定；只在高层做接触分类不足以支持动态全身操作。
- Sim-to-real 不能只看平均成功率或平滑度；摩擦调参、视觉域偏移、柔性物和状态估计来源都可能制造假鲁棒性。
- 安全和完成必须分账：故障下保持站立或降低风险不等于完成任务，但应作为独立、可验收的生存能力。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 任务完成 | 分阶段进度、端到端成功率、完成时间、连续任务长度 |
| 全身执行 | 足端/基座稳定、手臂—腰腿协同、动作不可达率、控制延迟 |
| 状态估计 | 动捕/marker/机载传感器分账、物体/机器人位姿误差、失估持续时长 |
| 地形与接触 | 滑移、跌倒、接触面识别、触觉/力反馈消融、低层跟踪误差 |
| 计划可执行性 | ground-truth/预测计划分账、首次可行解时间、在线重规划与恢复率 |
| Sim2Real | 仿真—真机成功差、摩擦/延迟敏感性、多次真机试验与失败阶段 |
| 安全—完成 | survival、task success、碰撞/过力、急停、故障恢复与人工接管 |
| 数据价值 | 目标本体锚点比例、同形态静态数据增益、robot-free/人类数据消融 |

## 适用边界

- 现有证据覆盖 humanoid、quadruped 和 mobile manipulator，但任务数量、环境开放度与真机试验数仍有限，不能据此宣称通用全身操作已解决。
- Ground-truth plan、动捕或 marker 适合模块诊断，不是端到端机载自治证据。
- 仿真中的接触、摩擦与柔性物成功不能直接外推到真机；真实试验需报告状态估计来源、失败阶段与重复次数。
- 人类/robot-free 数据的收益以动作接口、同形态或目标本体锚点为条件；不能把语义迁移等同于接触技能迁移。
- 故障下 survival 与 task success 是不同目标，前者不能被包装成任务完成率。

## 证据锚点

- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0002..0003`, `0011`, `0014`, `0016`, `0018..0019` 覆盖任务意图—全身执行、在线规划、长时序与稀疏目标控制。
- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0006`, `0008..0009`, `0013`, `0020` 支持 action-free、人类示范、生成数据与同形态静态数据的条件性分工；其中同形态静态共训把留出任务平均进度从 33% 提高到 87%。
- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0012`, `0021` 支持触觉进入低层命令和全身闭环；匹配真机试验中触觉方案为 90%，固定夹爪基线为 50%。
- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0001`, `0004`, `0007`, `0015`, `0018` 限定柔性物、ground-truth plan、摩擦调参、窄任务迁移和机载状态估计边界；深度状态相对动捕在两类目标上分别由 80%/90% 降至 50%/60%。
- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0010`, `0017` 支持风险敏感控制与 safety–completion 分账；未见锁关节故障下 survival 为 70%，task success 为 45%。

## 待补问题

- 建立统一的任务阶段、全身动作、接触目标与恢复事件 schema。
- 建立动捕/marker、机载视觉、深度和触觉状态估计的分层验收协议。
- 比较目标本体全身、同形态静态、人类/robot-free 与生成数据的边际收益和最小配比。
- 建立同时覆盖长时序、柔性物、地形变化、执行器故障和安全—完成分账的真机 benchmark。
