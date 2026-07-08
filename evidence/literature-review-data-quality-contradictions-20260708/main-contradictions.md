# 具身智能数据质量的主要矛盾

## 研究范围

- 时间范围：2026-01-08..2026-07-08。
- 证据范围：34 篇 paper-level 来源，54 条 evidence events；新增 6 条 2026-07-02..2026-07-07 正文级事件。
- 覆盖知识单元：`EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-XEMBODIMENT`, `EA-MODEL`, `EA-EVAL`。
- 完整证据条目见 [evidence-appendix.md](evidence-appendix.md)；本轮新增证据：`evidence.jsonl`，复用历史证据见 `run.json` 的 `source_runs`。

## 中心判断

具身智能数据质量的主要矛盾是：**低成本、规模化、异构数据生产，与机器人闭环执行所需的物理真实性、动作可执行性和任务可验证性之间的矛盾**。

这不是“数据量不够”一个问题，而是数据在六个层面同时失配：采集规模、物理可观测性、动作语义、跨本体迁移、失败恢复、闭环评测。数据越大，如果这些层面的可用性没有被治理，模型学到的可能只是视觉相关性、平均动作或数据源偏差。

## 六个派生矛盾

### 1. 规模数量 vs 有效结构

机器人示教数据并非越多越好。`SIEVE` 明确指出，大规模 VLA 示教池常包含冗余轨迹、噪声示教、次优行为和任务覆盖不均；按可复用 primitive 和 transition 选择中心、稳定轨迹时，50% 示教和 50% 训练步数可以超过全量训练（[2607.06442](https://arxiv.org/abs/2607.06442)）。

结论：第一优先级不是扩轨迹数，而是提高单位轨迹的信息密度、结构覆盖、动作一致性和长尾覆盖。

### 2. 视觉可得性 vs 物理可观测性

RGB、视频、第一视角人类数据便宜且可扩展，但它们天然缺深度、接触、力、摩擦、滑移、遮挡几何和材料状态。`Lift3D-VLA` 把 2D VLA 的瓶颈指向几何理解和动态一致性不足（[2607.06564](https://arxiv.org/abs/2607.06564)）；`TACO` 进一步说明，接触失败常视觉不可见，vision-only world model 可能生成看似合理但接触不一致的轨迹（[2607.02840](https://arxiv.org/abs/2607.02840)）。

结论：数据质量要从“图像清晰”转向“状态可观测”。开放空间抓放可以视觉优先；插入、擦拭、旋拧、柔性物、易碎物和高公差装配必须补 3D、触觉、力/力矩或事件级接触标注。

### 3. 异构复用 vs 监督可靠性

真实机器人、UMI、第一视角视频、仿真、生成数据都能提供价值，但它们能监督的字段不同。`τ0-WM` 把真实 robot data、UMI-style data 和 egocentric video 分成不同监督等级，并用 modality-specific masks 防止缺失模态被强行当真值（[2606.01027](https://arxiv.org/abs/2606.01027)）。

结论：异构数据不能简单 merge。要给每类数据贴“可信监督字段”：机器人数据给可执行动作，UMI 给低成本交互，egocentric video 给日常任务结构，失败 rollout 给后果和恢复，合成数据给受控覆盖与反事实。

### 4. 动作标签 vs 可执行动作语义

同一动作 token、同一末端轨迹、甚至同一控制命令，在不同本体、控制器、频率、坐标系和硬件状态下可能不是同一个物理动作。`SPACE` 的证据说明 recorded action 不是通用监督信号，需要共享状态变化表示和机器人特定 adapter（[2606.24049](https://arxiv.org/abs/2606.24049)）。手持夹爪研究也显示，示教器力分布、刚度和人体工学会直接影响示教质量（[2603.17189](https://arxiv.org/abs/2603.17189)）。

结论：高质量数据必须记录 action semantics 的上下文：坐标系、控制频率、归一化参数、controller convention、延迟、夹爪状态、接触状态、失败接管和硬件置信度。

### 5. 成功示教 vs 失败恢复

成功轨迹只教“正常完成”，不教“接触丢失后如何回来”。TacForeSight 需要 nominal demonstrations 与 recovery interaction data 才能学习扰动恢复（[2606.11184](https://arxiv.org/abs/2606.11184)）；TAMEn 也把 feasibility-aware acquisition 和 recovery teleoperation 放进触觉数据管线（[2604.07335](https://arxiv.org/abs/2604.07335)）。

结论：数据集不能只收好看的成功示教，还要系统收 near-miss、失败、人工接管、恢复、奖励/进度标签和边界工况。

### 6. 视觉真实感 vs 闭环可验证性

生成数据和世界模型会缓解采集成本，但“看起来真实”不等于“能评估或训练真实策略”。`GigaWorld-1` 认为世界模型作为策略评估器的质量主要取决于长程、动作忠实的 rollout 一致性，而不是短期视觉真实感（[2607.02642](https://arxiv.org/abs/2607.02642)）。`GEM-4D` 也指出，视频重建损失可能让模型停在“看起来像”，但机器人需要跨帧同一 3D 表面点的一致对应（[2605.22882](https://arxiv.org/abs/2605.22882)）。

结论：生成/仿真数据必须通过动作忠实性、几何对应、接触一致性、sim-real ranking 和真实闭环收益验证。

## 可操作框架

可以把具身数据质量拆成 6 个验收维度：

| 维度 | 核心问题 | 典型指标 |
|---|---|---|
| 信息密度 | 每条轨迹是否提供可复用结构，而不是重复动作 | primitive/transition 覆盖、冗余率、次优动作率 |
| 可观测性 | 关键物理状态是否被传感器看到 | 关键对象可见率、遮挡帧、触觉事件强度、力/力矩异常 |
| 可执行性 | 动作能否在目标本体和控制器上复现 | 坐标系一致性、action unnormalizer、控制频率、不可达率 |
| 同步与标定 | 多模态是否对齐 | 时间同步误差、丢帧率、action-state consistency、episode split |
| 边界与恢复 | 数据是否覆盖失败和恢复 | near-miss、失败类型、人工接管、recovery success、扰动恢复率 |
| 闭环收益 | 数据是否真实提升策略 | 少样本成功率、跨场景成功率、失败恢复率、负迁移检查 |

## 最短结论

具身智能数据质量的主要矛盾，不是“量不够”，而是**便宜可扩展的数据通常缺物理闭环所需的真信号；真实可执行的数据又昂贵、窄域、难规模化**。解决路径不是二选一，而是建立分层数据栈：真实机器人数据锚定可执行动作，UMI/人类视频扩展行为和场景，3D/触觉/力补齐不可观测状态，失败/恢复数据训练鲁棒性，世界模型和仿真负责低成本扩展，但所有层都必须经闭环指标验收。

## References

- [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17) — 证据: [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019)
- [TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks](https://arxiv.org/abs/2604.07335) (2026-04-08) — 证据: [EA-TWM-2026-0014](evidence-appendix.md#ea-twm-2026-0014)
- [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20) — 证据: [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007)
- [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31) — 证据: [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010)
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09) — 证据: [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014)
- [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23) — 证据: [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010)
- [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02) — 证据: [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004)
- [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03) — 证据: [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006)
- [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07) — 证据: [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001)
- [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07) — 证据: [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002)
