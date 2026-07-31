# Evidence Appendix: 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同

- Time range: 2025-07-27..2026-07-27
- Events: 19
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-4DDATA-READ-0015

- Claim: Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.01799](https://arxiv.org/abs/2605.01799) Embody4D: A Generalist Data Engine for Embodied 4D World Modeling
- Locator: Abstract (full-text section)
- Evidence: The abstract ties fixed or sparse viewpoints to partial observations and introduces both novel-view video generation and a compositional synthesis pipeline to address data scarcity.
- Quote: “Abstract Embodied agents require robust and comprehensive 3D spatiotemporal representations to support spatial reasoning, manipulation understanding, and downstream decision making. However, existing robot data are typically captured from fixed or sparse viewpoints, providing only partial and view-dependent observations, which limits multi-view perception and generalization across viewpoints. Given the difficulty of collecting additional viewpoints in real-world settings, we propose Embody4D, a”
- Authors: peiyan-tu; hanxin-zhu; jingwen-sun; et al.

### EA-SPATIAL-2026-0003

- Claim: Production-grade HD-map ground truth is a multi-source and multi-pass QA product: occlusion-free aerial data and onboard 3D sensing must be fused, map changes checked, geometry and topology manually cross-reviewed, and structural consistency validated.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.02956](https://arxiv.org/abs/2606.02956) The Road Ahead in Autonomous Driving: The KITScenes Multimodal Dataset
- Locator: Appendix E Annotation Protocol and Quality Control
- Evidence: The annotation appendix describes complementary map passes, fusion, manual review and multiple automated integrity checks.
- Quote: “Map creation is split into two complementary annotation passes. Road-level content, like lane geometry, road markings, lane topology, crosswalks, as well as BEV traffic light and sign positions, are annotated from aerial imagery, which provides a geo-referenced, occlusion-free top-down view.”
- Authors: richard-schwarzkopf; fabian-immel; alexander-blumberg; et al.

### EA-SPATIAL-2026-0005

- Claim: Fleet-grade spatial truth requires an explicit pose-and-time production stack: urban GNSS degradation is mitigated with LiDAR-inertial and INS fusion, cameras and LiDAR are disciplined to a master clock, and scans are motion-compensated to image timestamps.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.17080](https://arxiv.org/abs/2606.17080) HRDX: A Large-Scale Vector HD-Map Dataset
- Locator: 3.3 Localization and Sensor Synchronization
- Evidence: The dataset construction section describes the degradation mechanism and concrete fusion, clock and motion-compensation measures.
- Quote: “In dense urban areas, GNSS degrades due to multipath and occlusions. We mitigate this by integrating LiDAR–Inertial Odometry (LIO) and fusing it with INS, yielding robust, drift-free localization.”
- Authors: sahith-reddy-chada; isht-dwivedi; nirav-savaliya

### EA-SPATIAL-2026-0006

- Claim: Vector HD-map ground truth is built on a globally registered dense 3D map and still requires expert geometry/topology annotation plus visual verification; high-quality coordinates alone do not supply regulatory semantics.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.17080](https://arxiv.org/abs/2606.17080) HRDX: A Large-Scale Vector HD-Map Dataset
- Locator: 3.5 Data Annotation and Ground-Truth Labels
- Evidence: The annotation section states how the metric substrate and expert semantic labeling are combined.
- Quote: “To construct reliable ground truth for static map elements, we accumulate LiDAR frames at an interval of 5m across each scene into a globally registered, high-density 3D map. This merged point cloud serves as the metric substrate for annotation. Expert annotators use the fused pointcloud to annotate road geometry in vector form (polylines and polygons) and encode topology (e.g., intersection centerlines), followed by visual verification to ensure spatial precision.”
- Authors: sahith-reddy-chada; isht-dwivedi; nirav-savaliya

### EA-DQ-YEAR-READ-0003

- Claim: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: 3.3 Trajectory and Grasp Filtering via Simulation
- Evidence: PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。
- Quote: “Now that we have converted the human demonstrations into 6 DoF object pose trajectories, the next step is to execute them on a robot in simulation. This serves two purposes. One is to filter out those that may not be suitable for robot learning. There are two main reasons a trajectory may be unsuitable. First, pose estimation errors can lead to inaccurate trajectories. Second, the extracted trajectory may not be physically achievable by the robot. In either case, it would be harmful to train the”
- Authors: albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al.

### EA-4DDATA-READ-0009

- Claim: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction
- Evidence: 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。
- Quote: “The primary advantage of 3PoinTr is that it trains on data General Flow ignores. Real-world points are often temporarily occluded; General Flow removes any trajectory with invisible point-timestep pairs during preprocessing, whereas 3PoinTr retains all trajectories and masks losses for individual invisible point-timestep pairs. This provides additional supervision over task-critical object points that are temporarily occluded during manipulation. For example, in the Throw Away Paper task, every”
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### EA-4DDATA-READ-0007

- Claim: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control
- Evidence: 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。
- Quote: “All data modalities are synchronized through the robot control loop. For policy learning, actions are converted to a unified 7D end-effector delta representation (1) where are translational deltas, are rotational deltas, and is the gripper command. This decouples learning from the exact robot configuration, enabling cross-embodiment by focusing the policy on local contact adjustment from tactile feedback. Several quality checks are applied to every collected trajectory. Empty or corrupted trajec”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### EA-4DDATA-READ-0008

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Quote: “Policies in this setting are trained using both nominal demonstrations and recovery interaction data.”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### EA-PRETRAIN-DATA-2026-0001

- Claim: 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.17200](https://arxiv.org/abs/2606.17200) ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining
- Locator: 5.2 Ablation Studies, Figure 5(b)
- Evidence: 三项组件消融均降低 RoboCasa 成功率，其中去掉人类伪动作可靠性加权的降幅最大。
- Quote: “Removing morphology tokens makes the success rate drop from 72.8% to 70.9%”
- Authors: hao-li; ganlong-zhao; yufei-liu; et al.

### EA-SPATIAL-2026-0001

- Claim: 4D radar auto-labeling remains bounded by the quality of the cross-modal teacher and correspondence: severe occlusion or lighting can degrade visual segmentation, while image-plane overlap makes radar point-to-instance assignment ambiguous.
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.21454](https://arxiv.org/abs/2601.21454) 4D-CAAL: 4D Radar-Camera Calibration and Auto-Labeling for Autonomous Driving
- Locator: IV-C Discussion
- Evidence: The discussion explicitly names visual-segmentation degradation and overlap ambiguity as residual annotation limits after the proposed calibration and refinement pipeline.
- Quote: “For auto-labeling, annotation quality is bounded by visual instance segmentation performance, which may degrade under severe occlusion or extreme lighting. Additionally, significant object overlap in the image plane leads to ambiguous point-to-instance correspondences.”
- Authors: shanliang-yao; zhuoxiao-li; runwei-guan; et al.

### EA-SPATIAL-2026-0002

- Claim: Synthetic occupancy generation does not escape the ground-truth bottleneck: OccSim reports that semantic occupancy still requires manual semantic annotation, leaving fewer than 100,000 training frames and constraining exploration of scaling limits.
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.28887](https://arxiv.org/abs/2603.28887) OccSim: Multi-kilometer Simulation with Long-horizon Occupancy World Models
- Locator: 10 Potential limitation and Future work
- Evidence: The limitations section directly attributes the small training volume to manual semantic occupancy annotation.
- Quote: “Compared to image data, semantic occupancy data requires manual semantic annotation, which limits the total amount of available training data to fewer than 100,000 frames. This volume is significantly smaller than the amount of available RGB video data, and it also restricts our ability to explore the upper limits of the model’s performance.”
- Authors: tianran-liu; shengwen-zhao; mozhgan-pourkeshavarz; et al.

### EA-UMI-READ-0004

- Claim: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible task distribution.
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: Abstract (full-text section)
- Evidence: The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration data quality under challenging real-world conditions.
- Quote: “Abstract We present UMI-3D, a multimodal extension of the Universal Manipulation Interface (UMI) for robust and scalable data collection in embodied manipulation. While UMI enables portable, wrist-mounted data acquisition, its reliance on monocular visual SLAM makes it vulnerable to occlusions, dynamic scenes, and tracking failures, limiting its applicability in real-world environments. UMI-3D addresses these limitations by introducing a lightweight and low-cost LiDAR sensor tightly integrated i”
- Authors: ziming-wang

### EA-SPATIAL-2026-0004

- Claim: Driving-data fragmentation is itself a production bottleneck: dataset-specific file formats, APIs, calibration conventions and modality coverage make preprocessing repeatedly reimplemented and cross-dataset experiments expensive and brittle.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04271](https://arxiv.org/abs/2606.04271) StandardE2E: A Unified Framework for End-to-End Autonomous Driving Datasets
- Locator: 1 Introduction
- Evidence: The introduction explicitly describes recurring per-project preprocessing and brittle adapter work caused by heterogeneous dataset conventions.
- Quote: “In practice, this fragmentation imposes a recurring tax on end-to-end driving research. Per project, researchers re-implement preprocessing pipelines from raw protobuf, parquet, pickled-frame, or city-wide GPKG sources into a representation their model can consume.”
- Authors: stepan-konev

### EA-EGO-2026-0016

- Claim: Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 3 Method
- Evidence: 方法段明确说明 current-frame wrist pose 与 first-frame camera path 的坐标差异会混合两类位移。
- Quote: “using these wrist poses directly as action supervision would therefore conflate wrist movement with camera motion”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-SPATIAL-2026-0007

- Claim: Synthetic driving corner cases still require human or programmatic validation: even with explicit collision zones and CARLA execution, the LLM may fail under multiple constraints and only 29.4% of generated outputs were judged valid by manual inspection.
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.07601](https://arxiv.org/abs/2607.07601) CARLA-GS: Decoupling Representation, Reasoning, and Physics Simulation for Autonomous Driving Corner-Case Synthesis
- Locator: IV-B Quantitative Evaluation
- Evidence: The evaluation directly reports LLM instability and manual validity for the generated outputs.
- Quote: “However, LLM instability can still limit planning reliability. As indicated by the zone hit rate and variance, the LLM may fail to reach the target zone under multiple constraints, even with explicit prompts, as shown in Case 3 of Fig. 6 . Manual inspection shows that 29.4% of LLM-generated outputs are valid.”
- Authors: kaicong-huang; meng-ma; ruimin-ke

### EA-SPATIAL-2026-0008

- Claim: Safety-critical driving data is hard to produce because the desired distribution conflicts with natural occurrence: geographic coverage is narrow, routine safe interactions dominate, and raw trajectories lack semantic labels for triggers such as occlusion and constrained maneuver space.
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.16943](https://arxiv.org/abs/2607.16943) SinD 2.0: A Multi-City UAV Dataset with Semantic Risk Annotations for SOTIF-Oriented Safety Validation at Signalized Intersections
- Locator: I Introduction
- Evidence: The introduction explicitly identifies geographic homogeneity, rare critical events and missing trigger semantics as separate data limitations.
- Quote: “Effective safety validation also requires a high degree of criticality, which conflicts with the sparsity of dangerous scenarios in naturalistic driving data. Rigorous evaluation must push the system to its performance boundaries, yet naturalistic datasets are dominated by safe, routine interactions.”
- Authors: yunwei-li; shengjie-fu; chunrong-chen; et al.

### EA-SPATIAL-2026-0009

- Claim: Rule-generated risk labels remain provisional ground truth because they inherit errors from trajectories, maps and signal binding; auditability does not substitute for manual accuracy and threshold-sensitivity validation.
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.16943](https://arxiv.org/abs/2607.16943) SinD 2.0: A Multi-City UAV Dataset with Semantic Risk Annotations for SOTIF-Oriented Safety Validation at Signalized Intersections
- Locator: V-E Narrow Feasible-Area Scenarios
- Evidence: The paper explicitly describes the inheritance of upstream errors and the unfinished manual audit.
- Quote: “This design makes each label reproducible and inspectable, but it also means that the labels inherit map, signal-binding, and trajectory-estimation errors. We therefore use the semantic layer as a queryable scenario-mining index whose thresholds and evidence can be inspected and revised, rather than as a finalized benchmark of human-verified annotation accuracy.”
- Authors: yunwei-li; shengjie-fu; chunrong-chen; et al.

### EA-ALIGN-READ-0001

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: 3.2 Inconsistency of Control Commands across Robots
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Quote: “Recent work has scaled robot learning by training policies on data from multiple embodiments [ 27 , 23 , 32 ] , often using the Cartesian delta action space [ 23 , 32 ] since it is less dependent on robot-specific kinematics and invariant to base-frame translation [ 18 , 14 ] . In practice, this is typically realized by predicting Cartesian delta control commands that are fed to the underlying robot controller [ 23 , 32 ] . Figure 2: Different robots (e.g., UR5 vs. Franka Research 3) require dif”
- Authors: haeone-lee

### EA-TACTILE-2026-0001

- Claim: 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19161](https://arxiv.org/abs/2606.19161) HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision
- Locator: Abstract; 3 HT-Bench: A Multi-Task Tactile Evaluation Benchmark
- Evidence: 摘要和基准设计章节直接给出数据规模、四项评测任务与任务级 OOD 划分。
- Quote: “comprising 10M RGB frames and 7.8M tactile frames collected across 226 tasks.”
- Authors: yuzhe-huang; jiaping-wu; jiaming-jiang; et al.

## References

- `2601.21454` [4D-CAAL: 4D Radar-Camera Calibration and Auto-Labeling for Autonomous Driving](https://arxiv.org/abs/2601.21454) (2026-01-29)
- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.28887` [OccSim: Multi-kilometer Simulation with Long-horizon Occupancy World Models](https://arxiv.org/abs/2603.28887) (2026-03-30)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089) (2026-04-15)
- `2605.01799` [Embody4D: A Generalist Data Engine for Embodied 4D World Modeling](https://arxiv.org/abs/2605.01799) (2026-05-03)
- `2606.02956` [The Road Ahead in Autonomous Driving: The KITScenes Multimodal Dataset](https://arxiv.org/abs/2606.02956) (2026-06-01)
- `2606.04271` [StandardE2E: A Unified Framework for End-to-End Autonomous Driving Datasets](https://arxiv.org/abs/2606.04271) (2026-06-02)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.06194` [ActiveMimic: Egocentric Video Pretraining with Active Perception](https://arxiv.org/abs/2606.06194) (2026-06-04T14:01:01Z)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.17080` [HRDX: A Large-Scale Vector HD-Map Dataset](https://arxiv.org/abs/2606.17080) (2026-06-11)
- `2606.17200` [ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining](https://arxiv.org/abs/2606.17200) (2026-06-15T18:40:18Z)
- `2606.19161` [HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision](https://arxiv.org/abs/2606.19161) (2026-06-17)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2607.07601` [CARLA-GS: Decoupling Representation, Reasoning, and Physics Simulation for Autonomous Driving Corner-Case Synthesis](https://arxiv.org/abs/2607.07601) (2026-07-08)
- `2607.16943` [SinD 2.0: A Multi-City UAV Dataset with Semantic Risk Annotations for SOTIF-Oriented Safety Validation at Signalized Intersections](https://arxiv.org/abs/2607.16943) (2026-07-18)
