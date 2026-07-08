# Research Outline: 具身数据感知误差溯源

## 推荐研究题名

具身数据感知误差溯源：面向多模态采集与闭环部署的误差账本方法

## 一句话问题

当机器人“看错、拿错、接触失败或恢复失败”时，如何把错误从最终行为反推到可观测性、同步标定、监督字段、动作语义、本体控制和闭环评测中的具体来源？

## 三个可写章节

1. 从视觉感知错误到多模态可观测性错误：2D、3D、触觉、力和遮挡。
2. 从坏数据清洗到误差账本：episode、chunk、primitive、contact event 的多粒度追踪。
3. 从离线指标到闭环归因：用真实 rollout、世界模型和恢复数据验证溯源是否有效。

## 可落地实验设计

| 实验 | 目标 | 数据字段 | 输出 |
|---|---|---|---|
| episode 诊断 | 区分成功但低质的示教 | progress, smoothness, stalls, joint limits | episode-level error report |
| contact attribution | 区分视觉不可见接触失败 | tactile, force/torque, wrist/external views | contact event ledger |
| embodiment/action audit | 区分 perception error 与 action mismatch | coordinate frame, control frequency, action adapter | action-state consistency report |
| closed-loop validation | 验证归因是否有用 | rollout outcome, recovery, intervention, safety events | traceability-to-success curve |

## 后续资料缺口

- 需要再补一轮专门搜索：robot failure diagnosis, perception error attribution, causal robot data debugging, multimodal logging for manipulation。
- 需要把误差账本模板转成 episode schema 字段，和现有 `EA-DATA` 数据质量指标接起来。
