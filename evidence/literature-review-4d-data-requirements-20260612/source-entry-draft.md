# Source Entry Draft: 4D时空推理对数据的需求

> Draft only. These entries are not yet merged into `knowledge/sources.md`.

## S-ARXIV-2603-08485

- 标题：3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- URL：https://arxiv.org/abs/2603.08485
- 类型：arXiv paper / robot learning from human videos / 3D point tracks
- 时间：2026-03-09
- 本轮用途：支持“人类视频需要转成3D点轨迹，并配少量机器人动作示教”的数据需求判断。
- 关联证据：`EA-DATA-2026-4DDATA-0001`, `EA-DATA-2026-4DDATA-0002`

## S-ARXIV-2603-01549

- 标题：Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation
- URL：https://arxiv.org/abs/2603.01549
- 类型：arXiv paper / VLA / privileged 4D supervision
- 时间：2026-03-02
- 本轮用途：支持“动作标签不足以学习世界动态，训练期需要3D点轨迹等4D监督”。
- 关联证据：`EA-MODEL-2026-4DDATA-0003`, `EA-DATA-2026-4DDATA-0004`

## S-ARXIV-2603-16669

- 标题：Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- URL：https://arxiv.org/abs/2603.16669
- 类型：arXiv paper / 4D robotic simulation / Robo4D-200k
- 时间：2026-03-17
- 本轮用途：支持“动作应展开为URDF/kinematics驱动的4D robot pointmap，并监督环境RGB/pointmap响应”。
- 关联证据：`EA-DATA-2026-4DDATA-0005`, `EA-DATA-2026-4DDATA-0006`

## S-ARXIV-2605-22882

- 标题：GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- URL：https://arxiv.org/abs/2605.22882
- 类型：arXiv paper / geometry-enhanced video world model
- 时间：2026-05-20
- 本轮用途：支持“视频逼真不等于4D可行动，跨帧3D correspondence是关键数据监督”。
- 关联证据：`EA-MODEL-2026-4DDATA-0007`, `EA-DATA-2026-4DDATA-0008`

## S-ARXIV-2606-01027

- 标题：$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- URL：https://arxiv.org/abs/2606.01027
- 类型：arXiv paper / video-action world model / heterogeneous data mixture
- 时间：2026-05-31
- 本轮用途：支持“robot teleop、UMI、人类第一视角视频、失败rollout应分层混合，并用supervision masks治理监督可靠性”。
- 关联证据：`EA-DATA-2026-4DDATA-0009`, `EA-DATA-2026-4DDATA-0010`

## S-ARXIV-2606-13672

- 标题：WEAVER, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- URL：https://arxiv.org/abs/2606.13672
- 类型：arXiv paper / robot world model / policy evaluation and planning
- 时间：2026-06-11
- 本轮用途：支持“4D世界模型需要多视角、本体状态、动作、历史/记忆、奖励/价值监督”，并提供纯视觉世界模型的状态不可观测边界。
- 关联证据：`EA-EVAL-2026-4DDATA-0011`, `EA-SENSOR-2026-4DDATA-0012`

## S-ARXIV-2606-11184

- 标题：TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- URL：https://arxiv.org/abs/2606.11184
- 类型：arXiv paper / tactile world model / force-torque conditioning
- 时间：2026-06-09
- 本轮用途：支持“接触丰富任务需要高频腕部力/力矩和双指触觉序列，并需要恢复示教”。
- 关联证据：`EA-SENSOR-2026-4DDATA-0013`, `EA-DATA-2026-4DDATA-0014`

## S-ARXIV-2606-08737

- 标题：Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- URL：https://arxiv.org/abs/2606.08737
- 类型：arXiv paper / tactile world action model / contact-aware attention
- 时间：2026-06-07
- 本轮用途：支持“接触任务应联合预测未来视觉、未来触觉和动作，并用触觉事件强度区分静默期与接触期”。
- 关联证据：`EA-SENSOR-2026-4DDATA-0015`, `EA-DATA-2026-4DDATA-0016`

## S-ARXIV-2606-04825

- 标题：HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- URL：https://arxiv.org/abs/2606.04825
- 类型：arXiv paper / visuo-tactile-language-action dataset
- 时间：2026-06-03
- 本轮用途：支持“接触导向数据集应同步语言、视觉、触觉、状态、动作和操作者侧haptic feedback，并执行数据质控”。
- 关联证据：`EA-DATA-2026-4DDATA-0017`, `EA-DATA-2026-4DDATA-0018`

## S-ARXIV-2603-17189

- 标题：Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- URL：https://arxiv.org/abs/2603.17189
- 类型：arXiv paper / demonstration quality / UMI gripper usability
- 时间：2026-03-17
- 本轮用途：支持“示教采集硬件的人体工学、力分布和可用性会影响数据质量，不能只追求示教数量”。
- 关联证据：`EA-DATA-2026-4DDATA-0019`, `EA-DATA-2026-4DDATA-0020`
