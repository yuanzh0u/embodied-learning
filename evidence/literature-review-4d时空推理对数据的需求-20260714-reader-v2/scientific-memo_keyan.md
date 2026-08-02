# 4D时空推理对数据的需求研究备忘录

## 研究边界

版本说明：本轮以 15 篇可获取完整正文的论文为论证主干，逐篇核对问题、方法、结果与限制；未能取得可读全文的论文不再承担正文结论。

本文研究的问题是：如果具身智能系统要进行4D时空推理，也就是在3D空间中理解对象、机器人、接触和环境如何随时间演化，那么数据到底需要补什么。范围限定为 2026 年 1 月 14 日至 7 月 14 日公开论文，不把一般视频生成或静态三维重建自动算作具身 4D 数据研究。

本次范围综述从 915 条去重候选中核验 128 篇可用全文，并以 15 篇直接相关论文构成论证主干。检索同时覆盖几何时序、动作接口、接触感知、限制与迁移方向，并用连续两轮零新增确认搜索趋于饱和。未取得可核验正文的候选不支撑本文结论；这一规则保证“候选池很大”和“核心引用克制”可以同时成立。

## 核心结论

4D时空推理的数据需求不是“更多视频”四个字能概括的。现有论文共同指向一个分层数据栈：几何时序监督、可执行动作 grounding、异构数据的可靠性分级、触觉/力等接触状态、失败/恢复/奖励监督，以及采集硬件和同步质控。

换句话说，4D数据要同时回答四个问题：世界怎么动，机器人怎么动，接触怎么发生，动作失败时系统怎么知道并修正。

## 数据需求矩阵

| 数据层 | 最低可用形态 | 作用 | 证据 |
|---|---|---|---|
| 4D几何轨迹 | 3D point tracks、pointmaps、跨帧correspondence、可见性mask | 让模型学习同一物理点如何随时间运动，而不是只生成看起来合理的视频 | , [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549),  [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) |
| 可执行动作 grounding | 机器人动作chunk、本体状态、远程操作轨迹、少量真实机器人示教 | 把视觉/几何预测接到具体机器人控制空间 |,   |
| 异构监督治理 | robot demo、UMI式示教、第一视角人类视频、失败推演，并用mask区分可监督字段 | 防止把弱动作信号或无动作视频误当成机器人动作真值 | , [τ_0-WM](https://arxiv.org/abs/2606.01027) |
| 接触与多模态传感 | 双指触觉、腕部力/力矩、未来触觉潜在状态、触觉事件强度 | 补视觉不可观测的接触、滑移、抓取稳定性和局部形变 |,  [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737),  |
| 失败、恢复、奖励 | 合成失败轨迹、扰动恢复示教、任务进度/奖励/critic标签 | 让世界模型能评价候选动作，而不只是预测平均未来 | [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669), [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184),  [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) |
| 采集质量与硬件 | 时间同步、动作-状态一致性、episode级切分、触觉标记跟踪、示教器人体工学 | 保证数据能被学习，并减少示教工具本身引入的偏差 | [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485), [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825),  [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) |

## 主要共识

第一，动作标签不是世界动态标签。Pri4R明确指出，动作标签告诉策略“怎么动”，但不告诉它“动完世界会怎样”；3D点轨迹这类4D监督能把动作学习对齐到时空度量结构中（[Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549)）。

第二，人类视频有价值，但必须被转成机器人可用的中间表示。3PoinTr用无动作人类视频学习非embodiment点的3D点轨迹，再用少量机器人动作示教学习闭环策略，说明“广泛视觉动态”和“可执行动作”应分工而不是混用（[3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485)）。

第三，4D世界模型必须约束跨帧对应。GEM-4D把视频世界模型的关键失败定义为：未来视频看起来真实，但同一3D表面点跨帧漂移，导致动作提取不可靠。因此几何教师、点轨迹和pointmap监督是数据层面的必要补丁（, [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882)）。

第四，真实部署需要异构数据混合。τ0-WM把真实机器人远程操作、UMI式交互、第一视角人类视频和失败推演放进同一训练框架，但用modality-specific supervision masks区分每类数据能监督什么（, [τ_0-WM](https://arxiv.org/abs/2606.01027)）。

第五，接触任务会暴露纯视觉4D的盲区。TacForeSight、Dream-Tac和HapTile共同说明，触觉、力/力矩、触觉事件门控和haptic-informed示教对于插入、擦拭、切割、抓取柔性物体等任务不是锦上添花，而是状态可观测性的一部分（[TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184), [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737), [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825)）。

## 条件与限制

4D数据不是越密越好，而是要对齐任务物理。Pri4R的点密度消融显示，点数太少会损失交互几何；但GEM-4D也说明直接预测显式几何输出会带来标注和架构成本，因此“训练期几何教师、推理期轻量化”是一个折中方向（[Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549), [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882)）。

伪4D标注可以用，但要知道它在服务什么。Kinema4D接受ST-v2伪标注不是因为它等于高精度真值，而是因为相对几何和大规模覆盖足以训练生成式运动先验；这类数据适合世界模型，不应直接等同于控制精标数据（[Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669)）。

数据质量来自采集系统。HapTile强调同步、时间戳、动作-状态一致性和episode级切分；UMI示教质量研究进一步说明，夹爪力分布、刚度和人体工学会影响示教是否可学（[HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825), [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)）。

## 未解决问题

纯视觉世界模型仍然缺失隐藏物理状态。WEAVER作者明确指出，抓取稳定性、接触力、被遮挡几何、形变和颗粒动态可能无法从图像历史中恢复，需要触觉、力矩、深度、更广embodiment和更可靠奖励监督（[$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672)）。

示教设备需要与数据目标共同设计。手持夹爪或UMI式设备如果不能表达任务所需接触，后续算法很难补回这部分缺失；这仍缺少完整“示教工具-传感-学习-部署”闭环评估（[Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)）。

## 对本项目的启发

可以把“4D数据需求”定义为一个采集与标注规范，而不是单个数据集名称。第一，视觉动态、可执行动作、几何轨迹、接触传感、失败恢复和奖励监督必须分字段保存，每类来源只监督它真正可靠的部分；τ0-WM 的异构监督掩码就是这种思路的代表。第二，接触任务中的触觉和力矩属于状态可观测性，不是可有可无的附加输入。第三，验收世界模型时应同时检查视觉逼真度、几何对应一致性、动作可执行性、任务进度判断和失败恢复，而不能把任何一个指标当作总分。

## 数据工程决策

如果目标是让 4D 表征最终服务控制，数据验收应按用途拆开。第一类是动力学覆盖，回答物体与场景可能怎样变化；第二类是动作落地，回答某台机器人能够怎样施加干预；第三类是物理可观测性，记录接触、力、滑移和遮挡后的状态；第四类是时间一致性，保证不同传感流与动作状态使用同一时钟。

这意味着项目不宜用一个“总小时数”管理数据资产。人类视频可以扩大物体运动和场景变化的覆盖，机器人示教负责提供可执行动作，触觉与力矩补充视觉不可见状态，失败与恢复轨迹则定义控制边界。四类数据可以共同训练，但监督可靠性和缺失模态必须显式保存，不能在合并时被抹平。

最小验收也应从文件完整性升级为因果链完整性：动作发生前的状态是否可复原，动作是否与传感变化同步，关键物体在遮挡前后能否保持身份，失败是否能定位到接触丢失、几何漂移或动作不可达。只有这些条件成立，4D 数据才不只是更重的视频，而是可用于预测与纠错的交互记录。

## References
- [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549)
- [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882)
- [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027)
- [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737)
- [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669)
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184)
- [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672)
- [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485)
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825)
- [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)
