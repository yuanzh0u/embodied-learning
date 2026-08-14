# EgoVerse 生态综述证据附录

本附录列出正式综述使用的 15 个 paper-level evidence event。每个事件均对应 accepted paper note 和通过的 claim-support audit；完整事件载于 `evidence.jsonl`。

| Event ID | Paper | Stance | Full-text locator | 支持范围 |
|---|---|---|---|---|
| `EA-EGOVERSE-2026-0001` | EgoMimic: Scaling Imitation Learning via Egocentric Video | conditional | IV-B Results | 动作归一化对人机联合训练的重要性；Object-in-Bowl 消融 |
| `EA-EGOVERSE-2026-0002` | What Matters in Learning from Large-Scale Datasets for Robot Manipulation | limit | 5.4.2 Retriever’s Perspective (Real World) using DROID | 六个真实 DROID 检索任务中，全量联合训练失败；目标对齐与检索重要 |
| `EA-EGOVERSE-2026-0003` | Emergence of Human to Robot Transfer in Vision-Language-Action Models | conditional | V-C Human to robot transfer emerges… | 人类数据收益依赖 VLA 预训练的场景、任务与本体多样性 |
| `EA-EGOVERSE-2026-0004` | EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data | conditional | 3.3 Policy Performance Scales with Pretraining Data Size | 1k–20k 小时范围内任务完成度随人类预训练数据增加 |
| `EA-EGOVERSE-2026-0005` | EgoVerse: An Egocentric Human Dataset for Robot Learning from Around the World | conditional | IV-E Does Human Data Scale Robot Performance? | 域对齐数据作为锚点时才观察到正向扩量 |
| `EA-UMI-READ-0001` | Influence of Gripper Design on Human Demonstration Quality for Robot Learning | support | V DISCUSSION | gripper 力分布和人体工学影响示范质量 |
| `EA-UMI-READ-0003` | OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction | conditional | Abstract (full-text section) | 接触丰富任务需要视觉之外的深度、触觉和力信号 |
| `EA-UMI-READ-0004` | UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception | limit | Abstract (full-text section) | 遮挡、动态场景和弱纹理限制视觉 UMI；3D 感知补足 |
| `EA-UMI-READ-0006` | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | limit | Introduction | 结构化选择可用一半数据和训练步数优于全量训练 |
| `EA-UMI-READ-0008` | From Interaction to Demonstration Quality in Virtual Reality | conditional | 1 Introduction | VR 交互设备和视觉表示改变示范行为与质量 |
| `EA-UMI-READ-0009` | Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos | conditional | 3.3 Trajectory and Grasp Filtering via Simulation | 仿真过滤位姿错误、不可达轨迹与不兼容抓取 |
| `EA-UMI-READ-0010` | WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation | conditional | Abstract (full-text section) | 长程示范应在 frame/chunk 粒度保留高价值恢复片段 |
| `EA-UMI-READ-0011` | Quality over Quantity: Demonstration Curation via Influence Functions | support | VI CONCLUSIONS | 用对目标验证损失和策略表现的贡献定义数据质量 |
| `EA-UMI-READ-0012` | An Efficient Metric for Data Quality Measurement in Imitation Learning | support | Abstract (full-text section) | 轨迹 PSD 可作为低成本质量排序指标 |
| `EA-UMI-READ-0013` | Closing the Loop in Teleoperation | support | Abstract (full-text section) | episode 质量评估应返回操作者，形成采集纠偏闭环 |

## 核心论文原文锚点

### `EA-EGOVERSE-2026-0001`

- Paper: [EgoMimic](https://arxiv.org/abs/2410.24221)
- Locator: `IV-B Results`
- Quantitative anchor: removing action normalization produced a 38% drop in task score.
- Boundary: EgoMimic 平台、Object-in-Bowl 任务和论文联合训练配置。

### `EA-EGOVERSE-2026-0002`

- Paper: [What Matters in Learning from Large-Scale Datasets for Robot Manipulation](https://arxiv.org/abs/2506.13536)
- Locator: `5.4.2 Retriever’s Perspective (Real World) using DROID`
- Anchor: models co-trained with all of DROID failed to learn the tested target tasks.
- Boundary: 六个真实机器人任务、作者的数据重平衡和训练配方；不能外推为大数据普遍有害。

### `EA-EGOVERSE-2026-0003`

- Paper: [Emergence of Human to Robot Transfer in Vision-Language-Action Models](https://arxiv.org/abs/2512.22414)
- Locator: `V-C Human to robot transfer emerges…`
- Anchor: no/little pretraining did not benefit from human co-training; diverse pretraining did.
- Boundary: 0/25/75/100% 是论文特定覆盖设置，不是跨模型固定阈值。

### `EA-EGOVERSE-2026-0004`

- Paper: [EgoScale](https://arxiv.org/abs/2602.16710)
- Locator: `3.3 Policy Performance Scales with Pretraining Data Size`
- Quantitative anchor: average task completion increased from 0.30 at 1k hours to 0.71 at 20k hours.
- Boundary: 不外推到 20k 小时之外，也不假设其他标签管线或供应商数据具有相同曲线。

### `EA-EGOVERSE-2026-0005`

- Paper: [EgoVerse](https://arxiv.org/abs/2604.07607)
- Locator: `IV-E Does Human Data Scale Robot Performance?`
- Anchor: positive scaling appeared when domain-aligned data anchored learning.
- Boundary: 共享协议下已测试的实验室、任务、本体及 ID/OOD 设置。

### `EA-UMI-READ-0001`

- Paper: Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: `V DISCUSSION`
- Boundary: 采集硬件与操作者实验设置。

### `EA-UMI-READ-0003`

- Paper: OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction
- Locator: `Abstract (full-text section)`
- Boundary: 多模态 UMI 系统及论文测试的接触丰富任务。

### `EA-UMI-READ-0004`

- Paper: UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: `Abstract (full-text section)`
- Boundary: 论文报告的遮挡、动态场景、弱纹理和跟踪失败条件。

### `EA-UMI-READ-0006`

- Paper: SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: `Introduction`
- Boundary: 论文的数据预算、结构分组和 VLA 训练设置。

### `EA-UMI-READ-0008`

- Paper: From Interaction to Demonstration Quality in Virtual Reality
- Locator: `1 Introduction`
- Boundary: 论文比较的 VR 输入设备、视觉表示和日常任务。

### `EA-UMI-READ-0009`

- Paper: Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: `3.3 Trajectory and Grasp Filtering via Simulation`
- Boundary: 刚性或近似刚性物体、6DoF 轨迹恢复和论文仿真过滤管线。

### `EA-UMI-READ-0010`

- Paper: WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation
- Locator: `Abstract (full-text section)`
- Boundary: 长程遥操作示范中的局部进度与恢复片段选择。

### `EA-UMI-READ-0011`

- Paper: Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning
- Locator: `VI CONCLUSIONS`
- Boundary: influence-function 近似、目标验证集和论文的策略训练配置。

### `EA-UMI-READ-0012`

- Paper: An Efficient Metric for Data Quality Measurement in Imitation Learning
- Locator: `Abstract (full-text section)`
- Boundary: 轨迹功率谱密度与论文测试的示范质量任务。

### `EA-UMI-READ-0013`

- Paper: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: `Abstract (full-text section)`
- Boundary: episode 质量信号与操作者反馈系统。

## 非论文上下文

以下信息不进入科学证据事件，只用于生态和会议状态：

- EgoVerse 项目官网：联盟关系、数据/工具入口与项目更新。
- EgoVerse GitHub：Scale 和 Mecka 数据重处理记录。
- RSS 2026 官方议程：EgoVerse Paper 92、Datasets and Benchmarks session。
- Data-Centric Robotics workshop 官方页面：相邻议题与研究者导航。
- Danfei Xu 社交媒体更新：用于发现新伙伴和会议线索；只有一手页面确认后才升级状态。
