# 机器人"看走眼",为什么换个更强的视觉模型常常没用?

## TL;DR

机器人抓错、放偏、接触失败,直觉上是"视觉模型不行"。但近一年的论文给出的答案是:**多数"感知误差"其实是数据链路上游的错——关键状态根本没被传感器看到、多模态没对齐、动作标签在目标机器人上不可执行、或者评估从来没闭环**。换更大的视觉模型治不了这些病;能治的是给数据建一本"误差账本",逐层追责。

## 误区从哪来

"看错了就是视觉的锅"之所以流行,是因为失败的表象几乎总是视觉的:机器人对着错误的位置伸手,谁都会先怀疑眼睛。这个直觉在纯视觉任务里也确实成立。

但机器人是闭环系统。[TACO](https://arxiv.org/abs/2607.02840) 在接触丰富任务上给了一个直接反例:很多不可恢复的失败来自**轻微的接触扰动,而这些扰动在图像里根本不可见**——纯视觉的世界模型会生成"看起来很合理、接触上完全错误"的轨迹。也就是说,模型不是"看错了",是**这个信息从来没进过数据**。[Lift3D-VLA](https://arxiv.org/abs/2607.06564) 从另一头补刀:2D 视觉预训练天然丢失 3D 几何、遮挡关系和动态一致性,再大的模型也只能在丢失后的信息里打转。

## 真实机制:感知误差的五个藏身处

**第一层:可观测性。** 关键物理状态(接触、力、被遮挡的物体点)没被任何传感器记录。[TacForeSight](https://arxiv.org/abs/2606.11184) 发现,要学会扰动恢复,数据集必须显式包含恢复示教——成功轨迹里没有这个信息,模型自然学不会。追责时第一问不是"模型学没学会",而是"数据里有没有"。

**第二层:同步与标定。** [HapTile](https://arxiv.org/abs/2606.04825) 专门强调 action-state consistency、时间戳缺口和 episode 级切分:模态之间差几十毫秒,接触信号就和动作对不上,模型学到的是错位的因果。这类错误在表象上和"视觉不准"几乎无法区分。

**第三层:episode 质量。** [DQAF](https://arxiv.org/abs/2605.26349) 表明成功/失败标签远远不够——一条"成功"的示教可能满是停顿、振荡和关节极限抖动,照样教坏模型;[PSD 频谱指标](https://arxiv.org/abs/2605.01544) 和 [QoQ 影响函数](https://arxiv.org/abs/2603.09056) 分别从运动频谱和"对下游到底有没有贡献"给出了更硬的质量信号。

**第四层:动作语义。** [SPACE](https://arxiv.org/abs/2606.24049) 指出同一个"动作"在不同本体、控制器、坐标系下不是同一个物理事件——recorded action 不是通用监督信号。动作语义错配的失败,表象上就像"机器人没看准",实质是动作在这台机器上不可执行。

**第五层:闭环评估。** [GigaWorld-1](https://arxiv.org/abs/2607.02642) 的结论很清醒:世界模型作为评估器,可靠性取决于长程动作忠实的 rollout 一致性,而不是画面逼真。离线指标涨了、真机没变好,这不是感知误差,是**评估从来没闭环**。

## 什么时候"换视觉模型"确实有用

边界要讲清楚:如果任务是开放空间的抓放、遮挡少、不涉及接触精度,而且数据同步和动作语义都干净,那视觉表征确实是主要瓶颈,升级视觉骨干有直接收益([Lift3D-VLA](https://arxiv.org/abs/2607.06564) 的 3D lifting 就是这个方向的正面证据)。误差账本的意义不是"视觉不重要",而是**先排除上游,再优化模型**——顺序反了,就是拿最贵的手段修最不可能的原因。

## 延伸阅读

- 想看"接触失败视觉不可见"的实锤:[TACO](https://arxiv.org/abs/2607.02840)
- 想给采集流程装质量仪表盘:[DQAF](https://arxiv.org/abs/2605.26349)、[PSD metric](https://arxiv.org/abs/2605.01544)
- 想理解异构数据为什么不能直接混:[tau0-WM](https://arxiv.org/abs/2606.01027)(监督可靠性分级)
- 想看数据选择比堆量更有效的证据:[SIEVE](https://arxiv.org/abs/2607.06442)、[WARP-RM](https://arxiv.org/abs/2606.28320)

可信度说明:以上判断基于 15 条正文级证据事件(2025-07 至 2026-07 的 arXiv 论文),完整的立场/置信/定位见文末条目。这是公开论文快照,不是同行评审普查。

## References

- [TACO: TActile World Model as a Self-COrrector for Scalable VLA Post-Training](https://arxiv.org/abs/2607.02840) — 证据: [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006)
- [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) — 证据: [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002)
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) — 证据: [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014)
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset](https://arxiv.org/abs/2606.04825) — 证据: [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018)
- [Closing the Loop in Teleoperation (DQAF)](https://arxiv.org/abs/2605.26349) — 证据: [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002)
- [An Efficient Metric for Data Quality Measurement (PSD)](https://arxiv.org/abs/2605.01544) — 证据: [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003)
- [Quality over Quantity (QoQ)](https://arxiv.org/abs/2603.09056) — 证据: [EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001)
- [SPACE: Enabling Learning from Cross-Robot Data](https://arxiv.org/abs/2606.24049) — 证据: [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010)
- [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) — 证据: [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004)
- [tau0-WM: A Unified Video-Action World Model](https://arxiv.org/abs/2606.01027) — 证据: [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010)
- [SIEVE: Structure-Aware Data Selection for Imitation Learning](https://arxiv.org/abs/2607.06442) — 证据: [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001)
- [WARP-RM: A Warp-Augmented Relative Progress Reward Model](https://arxiv.org/abs/2606.28320) — 证据: [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006)
- [3PoinTr: 3D Point Tracks for Learning Manipulation from Human Videos](https://arxiv.org/abs/2603.08485) — 证据: [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002)
- [Imitating What Works: Simulation-Filtered Modular Policy Learning (PSI)](https://arxiv.org/abs/2602.13197) — 证据: [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008)
- [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657) — 证据: [EA-DATA-2026-LY-0007](evidence-appendix.md#ea-data-2026-ly-0007)

完整证据条目(claim/stance/locator)见 [evidence-appendix.md](evidence-appendix.md)。
