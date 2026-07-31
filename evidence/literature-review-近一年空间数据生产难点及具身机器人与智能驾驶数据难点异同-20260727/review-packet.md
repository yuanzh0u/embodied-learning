# Review Packet: 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同

## Scope

- Topic: 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同
- Time range: 2025-07-27..2026-07-27
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-4D`, `EA-EVAL`
- Evidence events: 19
- Topic cards: 3
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 19
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-4DDATA-READ-0015`, `EA-SPATIAL-2026-0003`, `EA-SPATIAL-2026-0005`, `EA-SPATIAL-2026-0006`, `EA-DQ-YEAR-READ-0003`, `EA-4DDATA-READ-0009`, `EA-4DDATA-READ-0007`, `EA-4DDATA-READ-0008`, `EA-PRETRAIN-DATA-2026-0001`, `EA-SPATIAL-2026-0001`, `EA-SPATIAL-2026-0002`, `EA-UMI-READ-0004`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 17 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 17
- Structure mapped: 17
- Deep-read papers: 17
- Claim-verified papers: 17
- Accepted evidence papers: 17
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；数据污染则是来源、时间、任务、模型版本和评测边界的关系失真，治理必须贯穿采集、训练、生成和闭环评测。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。对视觉—触觉—力觉数据，同时间戳帧只是最低层记录，真正的训练单元还应保留 approach、contact、slip、release、recovery 等事件链，并记录传感器/硬件 ID、时钟、标定和换件历史。所有异构数据都应声明可信监督字段，以动作条件状态变化和真实闭环收益验收；规模化触觉数据不自动等于跨硬件通用性或...
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；腕部六维力/力矩提供低维全局载荷，触觉提供高维局部接触场，两者不能互换。最新综合更支持按功能和时标选择性耦合：视觉/语言负责慢速全局语义与计划，触觉/力觉进入快速接触反馈，动作条件世界模型负责预测与验证。目标不是堆传感器，而是形成“同步数据—接触表征—动作条件预测—高频纠偏—安全过程评测”的接触执行栈，并证明每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-4D` 4D 时空推理与世界动态: 具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。
  - 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
  - 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
  - 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
  - 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
  - 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 5 |
| `conditional` | 条件成立 | 5 |
| `limit` | 限制/负面 | 9 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2601.21454: 4D-CAAL: 4D Radar-Camera Calibration and Auto-Labeling for Autonomous Driving | 2026-01-29 | limit | EA-SPATIAL-2026-0001 |
| 2602.13197: Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos | 2026-02-13 | conditional | EA-DQ-YEAR-READ-0003 |
| 2603.08485: 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos | 2026-03-09 | conditional | EA-4DDATA-READ-0009 |
| 2603.28887: OccSim: Multi-kilometer Simulation with Long-horizon Occupancy World Models | 2026-03-30 | limit | EA-SPATIAL-2026-0002 |
| 2604.14089: UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception | 2026-04-15 | limit | EA-UMI-READ-0004 |
| 2605.01799: Embody4D: A Generalist Data Engine for Embodied 4D World Modeling | 2026-05-03 | support | EA-4DDATA-READ-0015 |
| 2606.02956: The Road Ahead in Autonomous Driving: The KITScenes Multimodal Dataset | 2026-06-01 | support | EA-SPATIAL-2026-0003 |
| 2606.04271: StandardE2E: A Unified Framework for End-to-End Autonomous Driving Datasets | 2026-06-02 | limit | EA-SPATIAL-2026-0004 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional | EA-4DDATA-READ-0007 |
| 2606.06194: ActiveMimic: Egocentric Video Pretraining with Active Perception | 2026-06-04T14:01:01Z | limit | EA-EGO-2026-0016 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional | EA-4DDATA-READ-0008 |
| 2606.17080: HRDX: A Large-Scale Vector HD-Map Dataset | 2026-06-11 | support | EA-SPATIAL-2026-0005; EA-SPATIAL-2026-0006 |
| 2606.17200: ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining | 2026-06-15T18:40:18Z | conditional | EA-PRETRAIN-DATA-2026-0001 |
| 2606.19161: HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision | 2026-06-17 | support | EA-TACTILE-2026-0001 |
| 2606.24049: SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies | 2026-06-23 | limit | EA-ALIGN-READ-0001 |
| 2607.07601: CARLA-GS: Decoupling Representation, Reasoning, and Physics Simulation for Autonomous Driving Corner-Case Synthesis | 2026-07-08 | limit | EA-SPATIAL-2026-0007 |
| 2607.16943: SinD 2.0: A Multi-City UAV Dataset with Semantic Risk Annotations for SOTIF-Oriented Safety Validation at Signalized In... | 2026-07-18 | limit | EA-SPATIAL-2026-0008; EA-SPATIAL-2026-0009 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-4DDATA-READ-0015 | EA-DATA | `support` | `direct` | Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data. | The abstract ties fixed or sparse viewpoints to partial observations and introduces both novel-view video generation and a compositional synthesis pipeline to address data scarcity. (Abstract (full-text section)) | peiyan-tu; hanxin-zhu; jingwen-sun; et al. | 2605.01799 |
| EA-SPATIAL-2026-0003 | EA-DATA | `support` | `direct` | Production-grade HD-map ground truth is a multi-source and multi-pass QA product: occlusion-free aerial data and onboard 3D sensing must be fused, map changes checked, geometry an... | The annotation appendix describes complementary map passes, fusion, manual review and multiple automated integrity checks. (Appendix E Annotation Protocol and Quality Control) | richard-schwarzkopf; fabian-immel; alexander-blumberg; et al. | 2606.02956 |
| EA-SPATIAL-2026-0005 | EA-DATA | `support` | `direct` | Fleet-grade spatial truth requires an explicit pose-and-time production stack: urban GNSS degradation is mitigated with LiDAR-inertial and INS fusion, cameras and LiDAR are discip... | The dataset construction section describes the degradation mechanism and concrete fusion, clock and motion-compensation measures. (3.3 Localization and Sensor Synchronization) | sahith-reddy-chada; isht-dwivedi; nirav-savaliya | 2606.17080 |
| EA-SPATIAL-2026-0006 | EA-DATA | `support` | `direct` | Vector HD-map ground truth is built on a globally registered dense 3D map and still requires expert geometry/topology annotation plus visual verification; high-quality coordinates... | The annotation section states how the metric substrate and expert semantic labeling are combined. (3.5 Data Annotation and Ground-Truth Labels) | sahith-reddy-chada; isht-dwivedi; nirav-savaliya | 2606.17080 |
| EA-DQ-YEAR-READ-0003 | EA-DATA | `conditional` | `direct` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 | PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。 (3.3 Trajectory and Gr... | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | 2602.13197 |
| EA-4DDATA-READ-0009 | EA-DATA | `conditional` | `direct` | 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 | 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。 (4.3 Results: 3D Point Track Prediction) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | 2603.08485 |
| EA-4DDATA-READ-0007 | EA-DATA | `conditional` | `direct` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 | 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。 (3.2 Synchronization and Data Quality Control) | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-4DDATA-READ-0008 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-PRETRAIN-DATA-2026-0001 | EA-DATA | `conditional` | `direct` | 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 | 三项组件消融均降低 RoboCasa 成功率，其中去掉人类伪动作可靠性加权的降幅最大。 (5.2 Ablation Studies, Figure 5(b)) | hao-li; ganlong-zhao; yufei-liu; et al. | 2606.17200 |
| EA-SPATIAL-2026-0001 | EA-DATA | `limit` | `direct` | 4D radar auto-labeling remains bounded by the quality of the cross-modal teacher and correspondence: severe occlusion or lighting can degrade visual segmentation, while image-plan... | The discussion explicitly names visual-segmentation degradation and overlap ambiguity as residual annotation limits after the proposed calibration and refinement pipeline. (IV-C Discussion) | shanliang-yao; zhuoxiao-li; runwei-guan; et al. | 2601.21454 |
| EA-SPATIAL-2026-0002 | EA-DATA | `limit` | `direct` | Synthetic occupancy generation does not escape the ground-truth bottleneck: OccSim reports that semantic occupancy still requires manual semantic annotation, leaving fewer than 10... | The limitations section directly attributes the small training volume to manual semantic occupancy annotation. (10 Potential limitation and Future work) | tianran-liu; shengwen-zhao; mozhgan-pourkeshavarz; et al. | 2603.28887 |
| EA-UMI-READ-0004 | EA-DATA | `limit` | `direct` | Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves... | The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration d... | ziming-wang | 2604.14089 |
| EA-SPATIAL-2026-0004 | EA-DATA | `limit` | `direct` | Driving-data fragmentation is itself a production bottleneck: dataset-specific file formats, APIs, calibration conventions and modality coverage make preprocessing repeatedly reim... | The introduction explicitly describes recurring per-project preprocessing and brittle adapter work caused by heterogeneous dataset conventions. (1 Introduction) | stepan-konev | 2606.04271 |
| EA-EGO-2026-0016 | EA-DATA | `limit` | `direct` | Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 | 方法段明确说明 current-frame wrist pose 与 first-frame camera path 的坐标差异会混合两类位移。 (3 Method) | xingyao-lin; guojin-zhong; tianyi-lu; et al. | 2606.06194 |
| EA-SPATIAL-2026-0007 | EA-DATA | `limit` | `direct` | Synthetic driving corner cases still require human or programmatic validation: even with explicit collision zones and CARLA execution, the LLM may fail under multiple constraints... | The evaluation directly reports LLM instability and manual validity for the generated outputs. (IV-B Quantitative Evaluation) | kaicong-huang; meng-ma; ruimin-ke | 2607.07601 |
| EA-SPATIAL-2026-0008 | EA-DATA | `limit` | `direct` | Safety-critical driving data is hard to produce because the desired distribution conflicts with natural occurrence: geographic coverage is narrow, routine safe interactions domina... | The introduction explicitly identifies geographic homogeneity, rare critical events and missing trigger semantics as separate data limitations. (I Introduction) | yunwei-li; shengjie-fu; chunrong-chen; et al. | 2607.16943 |
| EA-SPATIAL-2026-0009 | EA-DATA | `limit` | `direct` | Rule-generated risk labels remain provisional ground truth because they inherit errors from trajectories, maps and signal binding; auditability does not substitute for manual accu... | The paper explicitly describes the inheritance of upstream errors and the unfinished manual audit. (V-E Narrow Feasible-Area Scenarios) | yunwei-li; shengjie-fu; chunrong-chen; et al. | 2607.16943 |
| EA-ALIGN-READ-0001 | EA-MODEL | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-TACTILE-2026-0001 | EA-SENSOR | `support` | `direct` | 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 | 摘要和基准设计章节直接给出数据规模、四项评测任务与任务级 OOD 划分。 (Abstract; 3 HT-Bench: A Multi-Task Tactile Evaluation Benchmark) | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | 2606.19161 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-4DDATA-READ-0015 | peiyan-tu; hanxin-zhu; jingwen-sun; et al. | unlisted | `support` | Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeli... |
| EA-SPATIAL-2026-0003 | richard-schwarzkopf; fabian-immel; alexander-blumberg; et al. | unlisted | `support` | Production-grade HD-map ground truth is a multi-source and multi-pass QA product: occlusion-free aerial data and onboard 3D sensing must be fused, map changes... |
| EA-SPATIAL-2026-0005 | sahith-reddy-chada; isht-dwivedi; nirav-savaliya | unlisted | `support` | Fleet-grade spatial truth requires an explicit pose-and-time production stack: urban GNSS degradation is mitigated with LiDAR-inertial and INS fusion, cameras... |
| EA-SPATIAL-2026-0006 | sahith-reddy-chada; isht-dwivedi; nirav-savaliya | unlisted | `support` | Vector HD-map ground truth is built on a globally registered dense 3D map and still requires expert geometry/topology annotation plus visual verification; high... |
| EA-DQ-YEAR-READ-0003 | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | unlisted | `conditional` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 |
| EA-4DDATA-READ-0009 | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | unlisted | `conditional` | 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 |
| EA-4DDATA-READ-0007 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `conditional` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 |
| EA-4DDATA-READ-0008 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-PRETRAIN-DATA-2026-0001 | hao-li; ganlong-zhao; yufei-liu; et al. | unlisted | `conditional` | 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 |
| EA-SPATIAL-2026-0001 | shanliang-yao; zhuoxiao-li; runwei-guan; et al. | unlisted | `limit` | 4D radar auto-labeling remains bounded by the quality of the cross-modal teacher and correspondence: severe occlusion or lighting can degrade visual segmentati... |
| EA-SPATIAL-2026-0002 | tianran-liu; shengwen-zhao; mozhgan-pourkeshavarz; et al. | unlisted | `limit` | Synthetic occupancy generation does not escape the ground-truth bottleneck: OccSim reports that semantic occupancy still requires manual semantic annotation, l... |
| EA-UMI-READ-0004 | ziming-wang | unlisted | `limit` | Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric... |
| EA-SPATIAL-2026-0004 | stepan-konev | unlisted | `limit` | Driving-data fragmentation is itself a production bottleneck: dataset-specific file formats, APIs, calibration conventions and modality coverage make preproces... |
| EA-EGO-2026-0016 | xingyao-lin; guojin-zhong; tianyi-lu; et al. | unlisted | `limit` | Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 |
| EA-SPATIAL-2026-0007 | kaicong-huang; meng-ma; ruimin-ke | unlisted | `limit` | Synthetic driving corner cases still require human or programmatic validation: even with explicit collision zones and CARLA execution, the LLM may fail under m... |
| EA-SPATIAL-2026-0008 | yunwei-li; shengjie-fu; chunrong-chen; et al. | unlisted | `limit` | Safety-critical driving data is hard to produce because the desired distribution conflicts with natural occurrence: geographic coverage is narrow, routine safe... |
| EA-SPATIAL-2026-0009 | yunwei-li; shengjie-fu; chunrong-chen; et al. | unlisted | `limit` | Rule-generated risk labels remain provisional ground truth because they inherit errors from trajectories, maps and signal binding; auditability does not substi... |
| EA-ALIGN-READ-0001 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-TACTILE-2026-0001 | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | unlisted | `support` | 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 |

## Synthesis Slots

### 共识/正向证据
- `EA-4DDATA-READ-0015`: Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data.
- `EA-SPATIAL-2026-0003`: Production-grade HD-map ground truth is a multi-source and multi-pass QA product: occlusion-free aerial data and onboard 3D sensing must be fused, map changes checked, geometry and topology manually cross-reviewed, and...
- `EA-SPATIAL-2026-0005`: Fleet-grade spatial truth requires an explicit pose-and-time production stack: urban GNSS degradation is mitigated with LiDAR-inertial and INS fusion, cameras and LiDAR are disciplined to a master clock, and scans are m...
- `EA-SPATIAL-2026-0006`: Vector HD-map ground truth is built on a globally registered dense 3D map and still requires expert geometry/topology annotation plus visual verification; high-quality coordinates alone do not supply regulatory semantic...
- `EA-TACTILE-2026-0001`: 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。
### 条件成立
- `EA-DQ-YEAR-READ-0003`: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- `EA-4DDATA-READ-0009`: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- `EA-4DDATA-READ-0007`: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- `EA-4DDATA-READ-0008`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- `EA-PRETRAIN-DATA-2026-0001`: 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。
### 限制与失败模式
- `EA-SPATIAL-2026-0001`: 4D radar auto-labeling remains bounded by the quality of the cross-modal teacher and correspondence: severe occlusion or lighting can degrade visual segmentation, while image-plane overlap makes radar point-to-instance...
- `EA-SPATIAL-2026-0002`: Synthetic occupancy generation does not escape the ground-truth bottleneck: OccSim reports that semantic occupancy still requires manual semantic annotation, leaving fewer than 100,000 training frames and constraining e...
- `EA-UMI-READ-0004`: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible ta...
- `EA-SPATIAL-2026-0004`: Driving-data fragmentation is itself a production bottleneck: dataset-specific file formats, APIs, calibration conventions and modality coverage make preprocessing repeatedly reimplemented and cross-dataset experiments...
- `EA-EGO-2026-0016`: Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。
- `EA-SPATIAL-2026-0007`: Synthetic driving corner cases still require human or programmatic validation: even with explicit collision zones and CARLA execution, the LLM may fail under multiple constraints and only 29.4% of generated outputs were...
- `EA-SPATIAL-2026-0008`: Safety-critical driving data is hard to produce because the desired distribution conflicts with natural occurrence: geographic coverage is narrow, routine safe interactions dominate, and raw trajectories lack semantic l...
- `EA-SPATIAL-2026-0009`: Rule-generated risk labels remain provisional ground truth because they inherit errors from trajectories, maps and signal binding; auditability does not substitute for manual accuracy and threshold-sensitivity validatio...

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 17 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-4DDATA-READ-0015` Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthe...
  - `EA-SPATIAL-2026-0003` Production-grade HD-map ground truth is a multi-source and multi-pass QA product: occlusion-free aerial data and onboard 3D sensing must be fused, ma...
  - `EA-SPATIAL-2026-0005` Fleet-grade spatial truth requires an explicit pose-and-time production stack: urban GNSS degradation is mitigated with LiDAR-inertial and INS fusion...
- Scientific memo preview: 《近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同: 先看证据边界，再谈一个可传播的反常识洞察。

## Draft Outline

1. 研究边界与证据范围
2. 概念与问题结构
3. 主要共识
4. 条件、限制与分歧
5. 未解决问题
6. 对后续研究/项目的启发

## Traceability Checklist

- Cite event IDs for paper-specific claims.
- Cite stable source IDs for topic-card background.
- Mark cross-event synthesis as `inference` with a short reason.
- Do not cite candidate-only papers as accepted evidence.
- Open raw sources before using exact wording.
