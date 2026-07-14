# 具身数据感知误差溯源：近一年论文研究备忘录

## 研究边界

- 时间范围：2025-07-08至2026-07-08。
- 证据范围：复用 `literature-review-embodied-data-quality-last-year-20260708` 与 `literature-review-data-quality-contradictions-20260708` 中的 15 条精选 evidence events。
- 覆盖知识单元：相关知识单元, 相关知识单元, 相关知识单元, 相关知识单元。
- 重要限制：这是 arXiv / public paper snapshot，不等于 仅限同行评审论文的完整普查。

## 中心判断

近一年论文显示，具身系统里的“感知误差”不应只归因于视觉模型看错了。更有解释力的框架是：**从数据采集、传感器可观测性、同步标定、监督字段、动作语义、本体控制到闭环评测的误差账本**。许多部署失败在表面上像 perception failure，实质上是上游数据缺失、模态错配、动作不可执行或接触隐变量不可观测在闭环中被放大。这一判断是跨事件综合推断，主要由 、、、 和  支撑（inference；见 [相关研究](https://arxiv.org/abs/2607.06564), [相关研究](https://arxiv.org/abs/2607.02840), [τ_0-WM](https://arxiv.org/abs/2606.01027), [相关研究](https://arxiv.org/abs/2605.26349), [相关研究](https://arxiv.org/abs/2607.02642)）。

## 核心机制

1. **可观测性缺口是感知误差的第一来源。** 2D VLA 会丢失 3D 几何、遮挡、接触和动态一致性，接触任务中的失败还常常视觉不可见；所以溯源时必须问“关键状态有没有被传感器看到”，而不是只问“模型有没有学会”。证据来自 、、 与 （[相关研究](https://arxiv.org/abs/2607.06564), [相关研究](https://arxiv.org/abs/2607.02840), [相关研究](https://arxiv.org/abs/2606.11184), [相关研究](https://arxiv.org/abs/2606.04825)）。

2. **episode 级遥测是把“感知失败”拆回数据原因的最小单元。** DQAF 表明，成功/失败标签不够，任务进度、运动平滑性、停顿、关节极限能解释一条示教为什么对学习有害；PSD metric 和 QoQ 则分别从运动频谱和下游贡献角度提供质量信号（[相关研究](https://arxiv.org/abs/2605.26349), [相关研究](https://arxiv.org/abs/2605.01544), [相关研究](https://arxiv.org/abs/2603.09056)）。

3. **异构数据必须带监督可靠性标签。** 人类视频、UMI、真实机器人和失败 推演 对 perception/action 的监督强度不同。tau0-WM 用 modality-specific supervision masks 处理缺失模态，PSI 用仿真过滤人类视频里的 pose estimation error、不可达轨迹和抓取不兼容问题，3PoinTr 用 visibility mask 保留被遮挡点的时序监督。

结论是：溯源账本要记录“这条数据能监督什么，不能监督什么”（[τ_0-WM](https://arxiv.org/abs/2606.01027), [相关研究](https://arxiv.org/abs/2602.13197), [相关研究](https://arxiv.org/abs/2603.08485)）。

4. **动作语义错配会伪装成感知误差。** SPACE 指出不同机器人为实现同一状态变化可能需要不同控制命令；HapTile 强调 action-state consistency、timestamp 空白s 和 episode-level split；这说明 perception error attribution 不能只看图像，还要看坐标系、控制频率、controller convention、动作归一化和目标本体适配是否一致（[相关研究](https://arxiv.org/abs/2606.24049), [相关研究](https://arxiv.org/abs/2606.04825)）。

5. **溯源粒度要下探到 primitive、chunk 和关键事件。** SIEVE 表明数据选择应保留可复用 primitive 与 transition，不是盲目保留全量；WARP-RM 表明次优长程示教里可能有高价值 recovery chunks。也就是说，失败不是简单归因到“这条轨迹坏了”，而要追踪到任务阶段、接触事件、恢复片段和动作 chunk（[相关研究](https://arxiv.org/abs/2607.06442), [相关研究](https://arxiv.org/abs/2606.28320)）。

6. **闭环评估决定归因是否成立。** GigaWorld-1 认为世界模型作为策略评估器的可靠性取决于长程 action-faithful 推演 consistency，而非短期视觉真实感；TACO 也把真实失败邻近状态转成可执行触觉纠正数据。由此可得：只有当数据诊断信号能解释或改善闭环成功率、恢复率、过力/碰撞/接管等指标时，它才算有效溯源（[相关研究](https://arxiv.org/abs/2607.02642), [相关研究](https://arxiv.org/abs/2607.02840)）。

## 误差账本模板

| 层级 | 常见误差来源 | 溯源证据 | 典型检核 |
|---|---|---|---|
| 观测/传感器 | 2D 丢几何、遮挡、接触不可见、触觉漂移 | 关键点可见性、3D/触觉/力事件、contact gate | 关键对象可见率、接触检测延迟、触觉/力异常 |
| 同步/标定/schema | 时间戳 空白s、action-state 不一致、episode split 泄漏 | 多模态 timestamp、控制循环、raw/rectified tactile | 同步误差、丢帧率、跨模态对齐残差 |
| episode 质量 | 停顿、振荡、过度纠正、关节极限 | DQAF 信号、PSD、质量分、人工反馈 | smoothness、stall count、joint-限制 proximity |
| 监督可靠性 | 缺失模态被当真值、人类视频不可执行 | supervision mask、sim filtering、visibility mask | 监督字段白名单、不可达率、pose estimation error |
| 动作/本体 | 坐标系、控制频率、adapter、动力学错配 | state delta、action adapter、controller metadata | action-state consistency、retargeting error |
| 结构/阶段 | 冗余、覆盖不均、坏轨迹中有好片段 | primitive/transition、progress/chunk labels | primitive 覆盖、recovery chunk 成功率 |
| 闭环结果 | 静态指标与真实部署不一致 | 推演 consistency、真实执行对照 | 成功率、恢复率、过力、碰撞、接管、sim-real ranking |

## 对后续研究的启发

这个话题可以命名为：**具身数据感知误差溯源：面向多模态采集与闭环部署的误差账本方法**。这是跨事件综合建议（inference；由 [相关研究](https://arxiv.org/abs/2607.06564), [相关研究](https://arxiv.org/abs/2607.02840), [相关研究](https://arxiv.org/abs/2607.02642) 共同支持）。

核心研究问题建议拆成三问：

1. 感知失败来自“看不见”、 “对不齐”、 “标错了”、 “动作不可执行”，还是“评估不闭环”？
2. 每类错误在 episode、chunk、primitive、contact event 哪个粒度上最可诊断？
3. 哪些数据质量信号能预测或改善真实闭环指标，而不是只提升离线指标？

## 条件、限制与未解决问题

- 本轮证据尚未覆盖统一的 perception-error provenance 基准测试；这是检索覆盖缺口，不能表述成整个领域已证明不存在此类标准（inference）。
- 多数方法能解释“哪类数据更好”，但本轮较少找到事故级追责链条：从某次失败反推具体数据源、模态、标定、动作字段和训练样本影响（inference）。
- 触觉/力/3D 数据正在变重要，但本轮对跨传感器实例、磨损、漂移和维护成本的长期证据不足（inference）。
- 世界模型可用于离线诊断和候选动作筛选，但 GigaWorld-1 和 TACO 都提醒：看起来真实的 推演 不等于接触和动作忠实，最终仍要回到真实闭环或高可信 sim-real ranking（[相关研究](https://arxiv.org/abs/2607.02642), [相关研究](https://arxiv.org/abs/2607.02840)）。

## 中心判断

感知误差溯源的核心不是为失败贴上“视觉、触觉或模型”的标签，而是找到因果链上的第一偏离点。一次抓取失败可能始于遮挡后的位姿漂移，也可能始于时间戳错位、动作坐标系误解、接触状态不可见，甚至是世界模型把视觉真实感误当成动作可靠性。若只看最终结果，这些机制会被压成同一种失败。

可操作的误差账本至少要同时保存原始观测、校准版本、状态估计、动作命令、控制器解释、接触与力信号，以及每一步的置信度。复盘时先问输入状态是否完整，再问状态是否被正确对齐，最后才检查策略如何使用状态。这样的顺序能减少“换更强视觉模型”却修不到根因的无效迭代。

溯源还必须允许多因一果。视觉遮挡可能使位姿略偏，动作语义错配再把偏差放大，接触不可见最终导致滑移。第一偏离点用于确定最早修复位置，后续放大环节则用于评估防线是否有效；两者不能互相替代。

为了让账本真正可用，每个失败都应保存可重放的时间窗口，而不是只截取最后一帧。窗口至少覆盖动作提出、控制器解释、首次状态偏离、恢复尝试和最终结果。这样才能判断误差是突然发生，还是由小偏差逐步积累；也能检验某个修复究竟消除了根因，还是只掩盖了末端症状。

溯源指标必须与干预相连。若系统认为问题来自标定，就应在重新标定后看到同类失败显著下降；若归因于动作语义，就应通过坐标统一或适配器修复验证。不能被干预复现或证伪的标签，只是事后叙述，还不是工程诊断。

最终可以形成三层防线：采集时拒绝不可解释的数据，训练时隔离可靠性不同的监督，部署时用不确定性和过程信号及时接管。误差账本的价值不是增加记录字段，而是让三层防线共享同一套因果语言。

## References

- [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349)
- [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056)
- [An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544)
- [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564)
- [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840)
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184)
- [tau0-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027)
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825)
- [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049)
- [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485)
- [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442)
- [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642)
- [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657)
- [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197)
- [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320)
