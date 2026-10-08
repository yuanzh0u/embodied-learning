# Evidence Appendix: 近一年SLAM技术在具身智能领域是否有核心作用？在具身数据采集、操作、导航、空间推理各环节，SLAM是不可或缺的基础设施，还是正被端到端基础模型、世界模型或隐式空间记忆替代？

- Time range: 2025-09-03..2026-09-03
- Events: 224
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-SLAMCORE-2026-0073

- Claim: OGScene3D 的在线相机位姿估计完全由 DROID-SLAM 提供：位姿被增量计算的同时系统同步进行语义建图与场景图构建，从而构成一个完全在线的系统——在该 2026 年的具身场景理解系统中，SLAM 定位层是被组合消费的输入基础设施，而非被替代的组件
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16301](https://arxiv.org/abs/2603.16301) OGScene3D: Incremental Open-Vocabulary 3D Gaussian Scene Graph Mapping for Scene Understanding
- Locator: page 5
- Evidence: Sec III-A 'Pose Estimation' 一节：RGB-D 流 → DROID-SLAM 在线位姿 → 位姿增量计算的同时做语义建图与场景图构建 → 'fully online system'。ref [84]（Teed & Deng, NeurIPS）见 page 18。
- Quote: “We utilize DROID-SLAM [84] for online pose estimation from the RGB-D stream. As camera poses are incrementally computed, we simultaneously perform semantic mapping and scene graph construction, which enables our OGScene3D to be a fully online system.”
- Authors: siting-zhu; ziyun-lu; guangming-wang; et al.

### EA-SLAMCORE-2026-0074

- Claim: 论文的核心问题定位：已有开放词汇场景理解工作只能基于预建完整 3D 语义地图离线构图，这在环境被增量探索、任务需在渐进探索过程中执行的机器人应用中不可行——语义建图与场景图正在被重新设计为 SLAM 式的增量在线形态，且这一需求的驱动因素正是机器人任务
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16301](https://arxiv.org/abs/2603.16301) OGScene3D: Incremental Open-Vocabulary 3D Gaussian Scene Graph Mapping for Scene Understanding
- Locator: page 2
- Evidence: Sec I 第三条局限（page 2）：离线构图基于预建 3D 语义地图，对渐进探索中执行任务的机器人应用不切实际；摘要（page 1）同义表述为预建完整语义地图限制增量探索场景的适用性；page 1 将开放词汇场景理解定位为支撑导航与操作等下游任务的能力。
- Quote: “Third, existing works can only perform offline graph construction based on prebuilt 3D semantic maps. Such offline approach is impractical for robotic applications where environments are explored incrementally and tasks need to be performed during progressive scene exploration based on scene understanding.”
- Authors: siting-zhu; ziyun-lu; guangming-wang; et al.

### EA-SLAMCORE-2026-0075

- Claim: 在 Replica 8 个场景的零样本新视角语义分割上，OGScene3D 平均 mIoU 71.77 / mAcc 89.15，优于 3DGS 语义 SLAM 基线 OpenGS-SLAM（61.91/73.11）及 GS-Grouping（59.15/69.94）、Feature 3DGS（48.89/57.51），论文称相对基线平均提升 16% mIoU、22% mAcc
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16301](https://arxiv.org/abs/2603.16301) OGScene3D: Incremental Open-Vocabulary 3D Gaussian Scene Graph Mapping for Scene Understanding
- Locator: page 12, Table I
- Evidence: Table I（page 12）：四方法在 room0-room2/office0-office4 上的 mIoU/mAcc，OGScene3D 全部场景领先，Avg mIoU 71.77 vs 61.91（OpenGS-SLAM）；正文称平均 16% mIoU、22% mAcc 提升。
- Quote: “The quantitative results in Tab. I demonstrate that our method achieves superior novel-view seg- mentation performance across all test scenes, with an average 16% improvement in mIoU metric and 22% improvement in mAcc metric compared to baselines.”
- Authors: siting-zhu; ziyun-lu; guangming-wang; et al.

### EA-SLAMCORE-2026-0077

- Claim: 增量场景图构建在关系估计上大幅优于离线预建管线：3RScan 4 个场景的关系 Recall 为 28.7/25.6/22.8/18.3，离线基线 ConceptGraphs（先建完整语义地图再构图）仅 2.5/fail/3.5/0.9（一个场景完全失败）——随探索持续更新的增量构图在真实扫描数据上同时更准且更快（单场景 10m13s vs 122m5s，见 page 15 Table V）
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16301](https://arxiv.org/abs/2603.16301) OGScene3D: Incremental Open-Vocabulary 3D Gaussian Scene Graph Mapping for Scene Understanding
- Locator: page 14, Table IV
- Evidence: Table IV（page 14）：ConceptGraphs 2.5/fail/3.5/0.9 vs OGScene3D 28.7/25.6/22.8/18.3；作者为公平起见扩展了 ConceptGraphs 的关系词表（原文 3 种→覆盖 3RScan 全部关系）。运行时间对比（ConceptGraphs 122m5s、HOV-SG 31m56s、OGScene3D 10m13s）在 page 15 Table V。
- Quote: “As shown in Tab. IV, baseline struggles to accurately identify relationships in real-world scenes, while our approach achieves superior open-set relationship estimation results.”
- Authors: siting-zhu; ziyun-lu; guangming-wang; et al.

### EA-SLAMCORE-2026-0076

- Claim: 3D 语义分割主评测（Replica/ScanNet，Table II-III 结果）使用数据集真值位姿以与基线保持一致，尽管系统声称具备建图中自行估计位姿的能力；论文未报告任何位姿估计精度指标（无 ATE/轨迹误差），且局部优化被显式设计为对位姿估计与重建误差鲁棒——语义建图性能对 SLAM 位姿质量的依赖在该论文中是隐性且未量化的
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.16301](https://arxiv.org/abs/2603.16301) OGScene3D: Incremental Open-Vocabulary 3D Gaussian Scene Graph Mapping for Scene Understanding
- Locator: page 13
- Evidence: page 13 评测协议：为与基线一致，3D 语义分割评测用真值位姿（'although our approach is capable of estimating poses during mapping'）；page 6 'This segment-level label association enhances robustness against potential pose estimation or reconstruction errors'；全文无位姿精度/轨迹误差指标（已检索核对）。
- Quote: “Additionally, for consistency with baseline methods, we utilize ground truth poses for 3D semantic mapping during 3D segmentation evaluation, although our approach is capable of estimating poses during mapping.”
- Authors: siting-zhu; ziyun-lu; guangming-wang; et al.

### EA-SLAMCORE-2026-0011

- Claim: 作者将 Meta Quest 3s 头显定位为整个数据采集框架的'高精度定位中枢'（high-precision localization hub）：其鲁棒 SLAM 系统提供稳定可靠的世界坐标系（该句跨页续接 'coordinate system, concurrently tracking the 6-DoF poses of both the operator's head and the controller'，见 page 4），即示教管线中全部 6-DoF 位姿数据的度量基础是头显内置 SLAM，而非外部动捕或机器人本体。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 3, Section 3.1 Head-mounted display (HMD)
- Evidence: 头显 SLAM 是 ActiveUMI 全部位姿数据的度量基础（作者自述的'高精度定位中枢'）
- Quote: “Head-mounted display (HMD). The Meta Quest3s HMD plays a dual, critical role within our framework. Firstly, it serves as a high-precision localization hub. Its robust SLAM system provides a stable and reliable world”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### EA-SLAMCORE-2026-0012

- Claim: 该 SLAM 世界坐标系同时追踪操作者头部与控制器的 6-DoF 位姿（page 5 进一步说明系统实际追踪左右控制器末端与头显共三个关键点），头显前置彩色相机同时充当与操作者视线耦合的'动态顶相机'。即：主动感知的训练信号（操作者头部运动，即视觉注意）与动作信号（夹爪位姿）由同一 SLAM 系统的几何输出提供。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 4, Section 3.1 Head-mounted display (HMD) 续段
- Evidence: 头部主动视角信号与夹爪动作信号同源于 SLAM 世界坐标系的 6-DoF 追踪输出
- Quote: “coordinate system, concurrently tracking the 6-DoF poses of both the operator’s head and the controller. Secondly, the HMD’s front-facing color cameras function as a dynamic, top camera, offering a global perspective that is intrinsically coupled with the operator’s line of sight.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### EA-SLAMCORE-2026-0013

- Claim: 所有示教数据以绝对坐标记录于初始校准阶段建立的统一世界坐标系中，三个追踪点与机器人双夹爪末端及头部相机一一对应；为维持会话内参考系一致性，作者设计了 in-situ 零点重置（控制器 B 按钮重定位基坐标系）、夹爪 placeholder 停靠标定、以及接近零点 3cm 内的触觉振动反馈三种校准手段。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 5, Section 3.3 Calibrating End-Effector for Precise Data Collection
- Evidence: 示教数据以绝对坐标记录于统一世界坐标系，配三种校准手段保证度量一致性
- Quote: “During policy execution, these tracked points map one-to-one with the robot’s two gripper tips and its head-mounted camera. All data is recorded in absolute co- ordinates relative to a unified world coordinate system that is established during an initial calibration phase.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### EA-SLAMCORE-2026-0014

- Claim: 位姿回放精度实验（卷尺标称距离 100 cm 递减至 10 cm 共 10 个数据点、10 次试验平均，协议见 page 8）中，ActiveUMI 的相对位姿误差（RPE）为 4.0 mm，UMI 为 10.1 mm（约 2.5 倍差距）；作者将低误差归因于 VR 系统的优势。注意 page 8 原句 'The RPE of UMI is 2.5x smaller than UMI' 存在主语笔误，方向由 Figure 6(e) 数值确定：ActiveUMI 误差更小。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 7, Figure 6(e)
- Evidence: VR SLAM 追踪使位姿精度较 UMI 提升约 2.5 倍（RPE 4.0 mm vs 10.1 mm）
- Quote: “RPE(mm) UMI 10.1 ActiveUMI (Ours) 4.0 (e) Relative Pose Error (RPE) Comparison”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### EA-SLAMCORE-2026-0137

- Claim: RoSHI 的系统动机建立在两类传感的互补性上：低成本低密度 IMU 提供对遮挡与高速运动的鲁棒性，而 egocentric SLAM 负责锚定长时程运动并稳定上半身位姿；融合使系统仅凭 egocentric 感知即可在度量全局坐标系中估计穿戴者的完整 3D 位姿与体型。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07331](https://arxiv.org/abs/2604.07331) RoSHI: A Versatile Robot-oriented Suit for Human Data In-the-Wild
- Locator: page 1, Abstract
- Evidence: 系统动机：IMU 管遮挡鲁棒性，egocentric SLAM 管长时程全局锚定与上半身稳定
- Quote: “We introduce RoSHI, a hybrid wearable that fuses low-cost sparse IMUs with the Project Aria glasses to estimate the full 3D pose and body shape of the wearer in a metric global coordinate frame from egocentric perception. This system is motivated by the complementarity of the two sensors: IMUs provide robustness to occlusions and high-speed motions, while egocentric SLAM anchors long-horizon motion and stabilizes upper body pose.”
- Authors: wenjing-margaret-mao; jefferson-ng; luyang-hu; et al.

### EA-SLAMCORE-2026-0138

- Claim: 作者论证 IMU-only 路线的结构性缺口：高端商用 IMU 动捕（Xsens，约 $4,500-$14,000）'typically lack true global localization'（漂移随长时程累积）；即便相对准确的惯性信号可在长时程漂移下产出可用的运动追踪，低成本 IMU 方案也只支持局部身体位姿追踪、无法产出可靠的度量尺度全局轨迹，需要外部锚点或互补传感才能恢复全局一致的运动。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07331](https://arxiv.org/abs/2604.07331) RoSHI: A Versatile Robot-oriented Suit for Human Data In-the-Wild
- Locator: page 3, Section II Related Work
- Evidence: 商用（$4.5k-14k）与低成本 IMU 均无法提供可靠全局度量轨迹，需外部锚点或互补传感
- Quote: “In addition to that, while high-end suits can often rely on relatively accurate inertial signals to produce usable motion tracking despite long-horizon drift, low-cost IMU set ups only support local body pose tracking and do not yield reliable metric-scale global trajectories, requiring external anchors or complementary sensing to recover globally consistent motion.”
- Authors: wenjing-margaret-mao; jefferson-ng; luyang-hu; et al.

### EA-SLAMCORE-2026-0139

- Claim: 在 11 段运动序列（3 个数据集、OptiTrack 真值）上，RoSHI（以 Aria SLAM 位姿为条件、IMU 骨向为引导的扩散生成）取得所有方法中三个数据集的最低 MPJPE（9.6/9.9/10.3 cm）与数据集 1、2 的最低 JAE（12.0/11.0 deg；数据集 3 的 JAE 为 15.6 deg，劣于 IMU-only 的 8.9）；IMU-only（naive root）基线在所有数据集上 MPJPE 最差（16.7/18.8/16.1 cm）；外参 SAM3D 为 10.3/10.5/21.6 cm MPJPE，但仅在有效检测帧上计算。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07331](https://arxiv.org/abs/2604.07331) RoSHI: A Versatile Robot-oriented Suit for Human Data In-the-Wild
- Locator: page 6, Table III
- Evidence: Table III：RoSHI 三个数据集 MPJPE 全最优（9.6/9.9/10.3 cm）、IMU-only 最差（16.7/18.8/16.1 cm）；所有 egocentric 基线都消费 Aria SLAM
- Quote: “RoSHI achieves the best MPJPE on Datasets 1, 2, and 3 and the best JAE on Datasets 1 and 2, showing consistent improvements in both global joint localization and articulated pose. The IMU-only baseline performs worst in terms of MPJPE across all datasets.”
- Authors: wenjing-margaret-mao; jefferson-ng; luyang-hu; et al.

### EA-SLAMCORE-2026-0140

- Claim: 真机人形全身控制实验中，每个 RL 跟踪策略都以 egocentric SLAM 估计的全局轨迹为条件，以保持模仿位姿与示教路径之间的对齐；作者据此强调可靠的定位与精确的 3D 身体位姿同等重要。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07331](https://arxiv.org/abs/2604.07331) RoSHI: A Versatile Robot-oriented Suit for Human Data In-the-Wild
- Locator: page 7, Section IV-C Real-World Whole-Body Control
- Evidence: RL 策略以 egocentric SLAM 全局轨迹为条件；作者称可靠定位与精确 3D 位姿同等重要
- Quote: “Each policy is conditioned on a global trajectory estimated by egocentric SLAM, which preserves alignment between the imitated pose and the demonstrated path and highlights that reliable localization is as important as accurate 3D body pose.”
- Authors: wenjing-margaret-mao; jefferson-ng; luyang-hu; et al.

### EA-SLAMCORE-2026-0141

- Claim: 系统的 SLAM 供给被明确设计为可替换的商品化组件：Project Aria 眼镜可以换成其他 state-estimation 相机，甚至'标准 RGB 相机 + 开源 SLAM 算法'；同时 IMU 子系统全部采用货架级消费传感器（而非高精度商用动捕单元），总硬件成本约 $350（9 个 IMU + 一个 USB 接收器）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07331](https://arxiv.org/abs/2604.07331) RoSHI: A Versatile Robot-oriented Suit for Human Data In-the-Wild
- Locator: page 2, Section I Introduction
- Evidence: SLAM 供给可替换（标准 RGB 相机 + 开源 SLAM 亦可）；IMU 子系统约 $350——SLAM 是商品化基础设施
- Quote: “Similarly, one can replace the Aria glasses with alternative state-estimation cameras [15], [16] or even standard RGB cameras paired with open-source SLAM algorithms.”
- Authors: wenjing-margaret-mao; jefferson-ng; luyang-hu; et al.

### EA-SLAMCORE-2026-0001

- Claim: UMI-3D 论文明确将 SLAM 从辅助跟踪组件重新定位为保证度量一致、时间对齐的感知-动作数据的核心机制，主张可扩展具身数据采集的瓶颈根本上在于位姿估计的可靠性
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 2
- Evidence: 引言部分系统论证：数据规模定律成立的前提下，位姿估计可靠性决定了可采集的环境/任务/交互分布，SLAM 是统一度量空间中对齐感知与动作的基础机制。
- Quote: “Instead of treating SLAM as an auxiliary component for tracking, we elevate SLAM to a core mechanism for ensuring metric-consistent, temporally aligned perception-action data.”
- Authors: ziming-wang

### EA-SLAMCORE-2026-0003

- Claim: 基于 LiDAR-centric SLAM 采集的 3,500 条演示训练的扩散策略，在完全未见环境中的杯排列任务上：seen 组合 0.863、部分未见 0.788、完全未见 0.736 归一化得分，分布偏移下优雅退化
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 13
- Evidence: 64 物体组合 × 10 次的真实机器人评测，两阶段打分协议（抓取+放置各 0-3 分）。
- Quote: “For seen object pairs, the average normalized score reaches 0.863. Under partial distribution shift (either cup or saucer unseen), performance decreases moderately to 0.788, and further to 0.736 in fully unseen scenarios.”
- Authors: ziming-wang

### EA-SLAMCORE-2026-0004

- Claim: 大变形物体操作（窗帘拉动，原视觉 UMI 下难以可靠采集的任务）在仅推理用视觉的条件下达到三类材质 0.88/0.90/0.96 归一化得分，证明 LiDAR-centric SLAM 采集侧的改进解锁了视觉 SLAM 下不可行的任务类型
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 13
- Evidence: 769 条演示训练 DINOv2 编码的扩散策略，120 次评测含强光/逆光条件，推理时不用 LiDAR。
- Quote: “the policy achieves strong performance across all curtain types, with normalized scores of 0.88, 0.90, and 0.96, respectively. The system remains robust under significant variations in lighting and appearance”
- Authors: ziming-wang

### EA-SLAMCORE-2026-0142

- Claim: MobileEgo Anywhere 把现有 egocentric 数据集的两大限制（episode 短、采集硬件门槛高）定位为'用现代智能手机已内置的视觉-惯性里程计（VIO），具体为 iPhone Pro 上的 ARKit，做 6-DoF 位姿追踪、无需任何专用外设'来解决，并据此发布小时级（最长 108 分钟）的 200 小时/584 会话 egocentric 数据集。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: page 1, Section I Introduction
- Evidence: 定位：智能手机内置 VIO（ARKit）零专用外设做 6-DoF 追踪，支撑 200 小时小时级数据集
- Quote: “MobileEgo Anywhere addresses both by using the visual-inertial odometry (VIO) already built into modern smartphones, specifically ARKit on the iPhone Pro, for 6 DoF pose tracking with no specialized peripherals.”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathore; et al.

### EA-SLAMCORE-2026-0143

- Claim: 作者在 'Long-Term Egocentric SLAM and State Estimation' 一节评估 SLAM 技术形态：长会话的稳定状态追踪是 SLAM 在该场景的中心难题；COLMAP 等 SfM 管线在小时级轨迹上计算不可行，ORB-SLAM3 等特征 SLAM 在动态或弱纹理室内场景累积漂移；ARKit/ARCore 等移动 AR 框架通过融合高频 IMU 与视觉关键帧，在边缘设备上实现鲁棒的长时追踪——这是本文采用 ARKit 的显式技术选型依据。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: page 2, Section II-C Long-Term Egocentric SLAM and State Estimation
- Evidence: II-C 节：COLMAP 小时级不可行、ORB-SLAM3 动态/弱纹理漂移；移动 AR 框架（ARKit/ARCore）以 IMU+视觉关键帧解决长时追踪
- Quote: “Maintaining stable state tracking over long sessions is the central difficulty for SLAM in this setting. Structure-from- Motion pipelines such as COLMAP [22] become computa- tionally intractable on hour-long trajectories, while feature- based SLAM such as ORB-SLAM3 [23] accumulates drift in dynamic or texture-poor indoor scenes. Recent mobile AR frameworks, notably ARKit and ARCore, address this by integrating high-frequency IMU data with visual keyframes, enabling robust long-term tracking on e”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathore; et al.

### EA-SLAMCORE-2026-0144

- Claim: 以 30 相机 Vicon 动捕为真值评估 ARKit VIO（10 段序列）：相对 ATE 十段中九段低于 1%（唯一例外是快速旋转的短序列）、旋转 RPE 低于 4 度、平移 RPE 全程低于 5 cm——作者结论是消费级 iPhone Pro 上的 ARKit 视觉-惯性里程计提供了足以支撑世界系手部位姿锚定的轨迹精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: page 3, Section IV-A1
- Evidence: vs Vicon：相对 ATE 9/10 序列 <1%、平移 RPE <5 cm——ARKit VIO 精度足以支撑世界系手部锚定
- Quote: “Translational RPE remains below 5 cm throughout, so local pose consistency holds even where global drift is marginally elevated. ARKit visual-inertial odometry on a consumer iPhone Pro thus provides trajectory accuracy sufficient for the world-frame hand-pose anchoring of Section III-B.”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathore; et al.

### EA-SLAMCORE-2026-0145

- Claim: 长时程漂移评估（因 ARKit 闭源而采用 ArUco 标记重访法，会话开始放置标记并在时间中点与终点重访，跨 6 个环境）：漂移除全屋遍历（终点 1.5 cm）外均低于 1 cm，且在所有情形下低于轨迹长度的 0.1%——作者据此论证 ARKit 追踪对下游 VLA 应用的有效性。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: page 3, Section IV-A2
- Evidence: ArUco 重访：6 环境漂移 <1 cm（全屋 1.5 cm）、<轨迹长度 0.1%——小时级世界系一致性成立
- Quote: “We repeat this across six environments (Table III); drift is below 1 cm in all but the whole-house traversal (1.5 cm end-of-session) and below 0.1% of trajectory length in all cases, demonstrating the efficacy of ARKit tracking for downstream VLA applications.”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathore; et al.

### EA-SLAMCORE-2026-0146

- Claim: 数据产品的空间骨架由 ARKit VIO 提供：ARKit 视觉-惯性融合产出跨全会话连续的 6-DoF 位姿，用于在一致世界系中生成 3D 手部轨迹；具体管线是 WiLoR+MANO 估计的手部相对 3D 坐标经 ARKit 深度采样与外参相机变换进入全局系，产出用于模仿学习（IK 映射到机器人末端帧）的世界锚定轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: page 2, Fig. 1 caption 与 Section III-B
- Evidence: ARKit VIO 连续 6-DoF 位姿用于生成一致世界系的 3D 手部轨迹（模仿学习监督信号）
- Quote: “ARKit-based visual-inertial fusion yields continuous 6 DoF pose, used to generate 3D hand trajectories in a consistent world frame across the full session.”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathore; et al.

### EA-SLAMCORE-2026-0015

- Claim: 同一 π0 底座、同一任务集上的相机视角消融：ActiveUMI（主动头部相机，20-DoF）在 5 个 in-domain 双臂任务上平均成功率 70%，高于固定头相机（42%）与腕部相机-only 的 UMI 设定（26%）；新环境下 ActiveUMI 保持 56%，固定头相机降至 16%、UMI 降至 6%。部署时策略仅使用机器人平台可用的自我中心头部相机与腕部本体感知（page 2），视角控制由策略输出头部 6-DoF 位姿、低层控制器执行（page 4），部署回路不含在线 SLAM。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 7, Tables 1-2
- Evidence: 70% vs 26%（UMI 设定）成功率证明主动视角价值；部署仅靠相机+本体感知、无在线 SLAM
- Quote: “Tasks (In-Domain) Bottle placing Rope boxing Shirt folding Block disassembly Take Drink from Bag Average UMI 60% 20% 10% 0% 40% 26% UMI w/ Fixed Head Camera 60% 40% 40% 20% 50% 42% ActiveUMI 90% 70% 80% 30% 80% 70% Table 2. We compare our active perception approach to two variants in a new environment under the same task as Table 1. Camera View Tasks (New Environment) Bottle placing Rope boxing Shirt folding Block disassembly Take Drink from Bag Average UMI 30% 0% 0% 0% 0% 6% UMI w/ Fixed Head C”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### EA-SLAMCORE-2026-0010

- Claim: 真机对照实验（U-Arm Config-1 vs Joycon 遥操作 XArm6，5 个任务）：U-Arm 平均采集时间 17.70s vs Joycon 29.04s（作者称 39% 时间缩减），平均成功率 75.8% vs 83.0%；其中精细任务 Can-stacking 上 U-Arm 39.6% 显著低于 Joycon 64.0%，作者归因于 Joycon 松杆即停而主从实时映射更易引入小失误，并认为这是效率换精度的可接受权衡。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.02437](https://arxiv.org/abs/2509.02437) U-ARM : Ultra low-cost general teleoperation interface for robot manipulation
- Locator: page 6, Table IV
- Evidence: 比 Joycon 快 39% 且成功率相当（75.8% vs 83.0%），但精细任务落后 24.4 pp；无策略训练实验
- Quote: “Task U-Arm (Config-1) Joycon Time (s) Success (%) Time (s) Success (%) Fanta-from-shelf-2 14.43 88.8% 27.85 94.0% Oreo-from-shelf-1 11.28 88.5% 22.23 100.0% Fanta-to-shelf-2 19.88 72.2% 31.90 60.0% Can-stacking 20.93 39.6% 31.35 64.0% Block-from-litterbox 21.99 90.0% 31.89 96.0% Average 17.70 75.8% 29.04 83.0% a) Observations: Across all tasks, the U-Arm demon- strated a 39% reduction in operation time compared to the Joycon, without a substantial decrease in success rate.”
- Authors: yanwen-zou; zhaoye-zhou; chenyang-shi; et al.

### EA-SLAMCORE-2026-0005

- Claim: 即使有 SLAM 保障的高质量数据，长时程任务成功率仍沿阶段急剧衰减（开门 97.5% → 抓杯 47.5% → 放置 5.0%），其中 32.5% 的试验因演示运动违反机器人逆运动学约束而在放置阶段失败——数据质量提升不能替代本体可行性与控制约束
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 14
- Evidence: 40 次长时程评测的 Sankey 失败传播分析，作者将失败归因于 IK 约束违反与训练数据多样性不足。
- Quote: “the door opening stage achieves a high success rate of 97.5%, indicating that the policy reliably learns articulated object interaction. However, performance decreases in subsequent stages, with cup grasping success at 47.5% and final placement success at only 5.0%”
- Authors: ziming-wang

### EA-SLAMCORE-2026-0006

- Claim: SLAM/几何感知在 UMI-3D 中仅作用于数据采集阶段：学习到的策略在推理时主要依赖视觉观测，LiDAR 捕获的 3D 几何信息尚未进入策略学习——作者将'3D 感知直接用于策略学习'列为未来工作
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 15
- Evidence: 作者自述局限：LiDAR 对 SLAM 鲁棒性与数据质量至关重要，但策略推理仅用视觉，同步采集的 3D 几何是尚未利用的资源。
- Quote: “the learned policies in this work rely primarily on visual observations at inference time. However, the system inherently captures synchronized 3D geometric information during demonstrations”
- Authors: ziming-wang

### EA-SLAMCORE-2026-0007

- Claim: 作者将示教接口分为两类并主张：末端执行器轨迹记录设备（DexCap、UMI、OpenTelevision）虽然轻便易用，但采集的数据存在运动学奇异、超出机器人工作空间、精度不足或需要复杂后处理等问题；主从遥操作系统（ALOHA、GELLO）通过机械同构主臂实现直觉的、物理约束的示教，帮助保证采集轨迹物理可行、机器人可执行。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.02437](https://arxiv.org/abs/2509.02437) U-ARM : Ultra low-cost general teleoperation interface for robot manipulation
- Locator: page 1, Section I Introduction
- Evidence: 作者主张末端轨迹记录类设备（含 UMI）有结构性缺陷，主从遥操作是替代范式
- Quote: “End-effector trajectory recording devices such as DexCap [7], UMI [8], and OpenTelevision [9], are often lightweight and easy to use. However, the collected data can suffer from issues such as kinematic singularities, exceeding the robot’s workspace, insufficient precision or need complicated post-processing. In contrast, leader-follower teleoperation systems such as ALOHA [10] and GELLO [11] enable intuitive and physically constrained demonstrations through mechanically isomorphic leader arms.”
- Authors: yanwen-zou; zhaoye-zhou; chenyang-shi; et al.

### EA-SLAMCORE-2026-0008

- Claim: 作者主张真机遥操作数据的关键优势在于控制与记录的分离：遥操作设备只用于控制，用于学习的数据直接从执行任务的机器人上采集，从而保证记录的示教与部署分布最接近。在 U-Arm 的关节角映射架构下，这意味着训练数据的关节/位姿真值由从臂本体编码器给出，不经过任何外部位姿估计环节。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.02437](https://arxiv.org/abs/2509.02437) U-ARM : Ultra low-cost general teleoperation interface for robot manipulation
- Locator: page 3, Section II-B
- Evidence: 遥操作数据控制与记录分离：数据直接从机器人记录，架构上绕开外部位姿估计
- Quote: “A key advantage of real-world teleoperation data lies in the separation between control and recording: teleoperation devices are typically used only for control, while the data for learning is collected directly from the robot executing the task. This ensures that the recorded demonstrations share the closest distribution with deployment.”
- Authors: yanwen-zou; zhaoye-zhou; chenyang-shi; et al.

### EA-SLAMCORE-2026-0009

- Claim: 成本对比（Table I）：U-Arm 单臂 BOM 为 $50.5（摘要另报 7-DoF 版 $56.8，page 1），对比 GELLO $270（Dynamixel 电机每个 $24）、VR Headset（Meta Quest 3）$500、Space Mouse $220、Joycon $20、ALOHA $24,000、DexPilot $1700——U-Arm 约为 GELLO 的 1/5.4、VR 头显的 1/10、ALOHA 的 1/475。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.02437](https://arxiv.org/abs/2509.02437) U-ARM : Ultra low-cost general teleoperation interface for robot manipulation
- Locator: page 3, Table I
- Evidence: $50.5 单臂 BOM 比 GELLO/VR 头显低 5-10 倍、比 ALOHA 低约两个数量级（Table I）
- Quote: “Device Price (USD) Remarks VR Headset (Meta Quest 3) [30] $500 May cause motion sickness Space Mouse [31] $220 Hard to operate bi- manually GELLO [11] $270 Uses Dynamixel motors, $24 each Game Controller (Joycon) [12] $20 Difficult for dex- terous manipula- tion Ours $50.5 Sufficient for bi- manual manipula- tion ALOHA [10] $24,000 Identical leader- follower hardware design DexPilot [25] $1700 Faces occlusion problems”
- Authors: yanwen-zou; zhaoye-zhou; chenyang-shi; et al.

### EA-SLAMCORE-2026-0002

- Claim: 原 UMI 依赖的单目视觉 SLAM 在大物体遮挡（开门/抽屉）、动态干扰、无纹理场景下会误判运动或完全丢失跟踪，从而系统性限制可采集任务范围，使数据采集偏向视觉 SLAM 友好场景
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 2
- Evidence: 论文引用大规模 UMI 数据采集的实证研究 [15]，说明视觉 SLAM 失败导致任务分布收缩与数据后处理成本上升。
- Quote: “the SLAM system may misinterpret motion or even lose tracking entirely, thereby limiting the range of feasible tasks”
- Authors: ziming-wang

### EA-SLAMCORE-2026-0021

- Claim: 在 HM3D 验证集随机抽取的 200 个 episode 上，纯 RGB、无度量地图、无深度/GPS 的开放词汇 ObjectNav 方法 PanoNav 取得 SR 43.5 / SPL 23.7，超过同设定（RGB-only、mapless）基线 ZSON（SR 25.5 / SPL 12.6）与 PixNav（SR 37.9 / SPL 20.5）；相对 PixNav 提升 14.76%（SR）与 15.61%（SPL）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.06840](https://arxiv.org/abs/2511.06840) PanoNav: Mapless Zero-Shot Object Navigation with Panoramic Scene Parsing and Dynamic Memory
- Locator: page 5, Table 1
- Evidence: 无图纯 RGB 路线在 HM3D 200 episodes 上 SR 43.5 / SPL 23.7，超过同设定基线 ZSON 与 PixNav
- Quote: “ZSON RGB Only Open-Set mapless 25.5 12.6 PixNav RGB Only Open-Set mapless 37.9 20.5 PanoNav (Ours) RGB Only Open-Set mapless 43.5 23.7”
- Authors: qunchao-jin; yilin-wu; changhao-chen

### EA-SLAMCORE-2026-0024

- Claim: 作者将全局场景解析定位为提供'隐式自定位意识'（implicit self-location awareness）的机制：其全局摘要以房间/场景类型等语义线索（如 kitchen、hallway）提示智能体在更广环境中的位置，并作为决策模块构造动态记忆状态的基础输入——无图条件下的自定位由语义级线索承担，而非度量位姿。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.06840](https://arxiv.org/abs/2511.06840) PanoNav: Mapless Zero-Shot Object Navigation with Panoramic Scene Parsing and Dynamic Memory
- Locator: page 3
- Evidence: 全局场景摘要提供房间级语义位置线索，作为隐式自定位替代度量定位
- Quote: “offering cues about the agent’s position within the broader environment (e.g., kitchen, hallway).”
- Authors: qunchao-jin; yilin-wu; changhao-chen

### EA-SLAMCORE-2026-0168

- Claim: 组件消融显示端到端基础策略单独不可行：纯 NavDP 基础策略在 HM3D InstanceImageNav 上仅 24.7/12.6（SR/SPL），作者归因于其纯反应式控制与缺乏长程规划；引入 SMG 全局规划后升至 74.04/56.14，再加 VGGT-adapter 达 78.50/59.27。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.22609](https://arxiv.org/abs/2511.22609) MG-Nav: Dual-Scale Visual Navigation via Sparse Spatial Memory
- Locator: page 7, Sec 4.3 Component ablation
- Evidence: 纯 NavDP 基础策略 SR 仅 24.7，加 SMG 升至 74.04——端到端基础模型不能单独替代显式空间记忆
- Quote: “Component ablation. Table 3 reports a detailed ablation on model components. The foundation model achieves only 24.7/12.6 (SR/SPL), limited by its purely reactive con- trol and lack of long-range planning. Introducing SMG for global planning significantly boosts performance to 74.04/56.14, as it decomposes long-range navigation into reachable node-to-node subgoals, providing global guid- ance for the agent. Further incorporating the VGGT-adapter improves results to 78.50/59.27, confirming that g”
- Authors: bo-wang; jiehong-lin; chenzhi-liu; et al.

### EA-SLAMCORE-2026-0049

- Claim: 综述自述方法学：6 个互补数据库（Google Scholar/arXiv/ACM DL/IEEE Xplore/Semantic Scholar/DBLP）+ 11 类关键词初检 3000+ 篇；四阶段过滤（时间窗 2018–2026、顶会优先、低引用突破性工作与高引用基础方法并重的质量双策略、相关性）+ 雪球抽样；最终语料 2000+ 篇评审、742 篇直接引用；两名独立评审验证选择与分类法，标注者间一致性 94%（范围分歧 4%、分类归属分歧 2%，讨论至共识）。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.01644](https://arxiv.org/abs/2602.01644) From Perception to Action: Spatial AI Agents and World Models
- Locator: page 3, Section 2 Methodology
- Evidence: 2000+ 篇评审/742 直接引用/双评审 94% 一致性——方法学透明的领域级 survey，可用作社区认知证据
- Quote: “This process resulted in a final corpus of over 2,000 papers, from which 742 are directly cited, which were carefully analyzed to derive the taxonomy, identify key trends, and synthesize the findings presented in this survey. We employed a snowball sampling technique to ensure broad coverage of related works, following citation chains both forward and backward. Two independent reviewers validated the paper selection and taxonomy development, achieving 94% inter-annotator agreement on inclusion c”
- Authors: gloria-felicia; nolan-bryant; handi-putra; et al.

### EA-SLAMCORE-2026-0051

- Claim: 综述把空间记忆（智能体三能力之一）的实现清单从经典 SLAM 文献铺到神经方法：专门实现包括认知地图、拓扑表示与度量地图（引 Thrun et al. 2005、Durrant-Whyte & Bailey 2006、Cadena et al. 2016、ORB-SLAM 系、LSD/DSO 系）；神经方法包括 Neural SLAM（Active Neural SLAM 系）、语义图与场景图——即 SLAM 家族在该 agentic 框架中被吸收为'空间记忆'能力的实现族，而非被淘汰的旧范式；作者组件级结论是'记忆系统必须显式空间化：认知地图、语义图与场景图在空间任务上优于通用检索'。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.01644](https://arxiv.org/abs/2602.01644) From Perception to Action: Spatial AI Agents and World Models
- Locator: page 7, Section 5.1 Memory Systems
- Evidence: 空间记忆实现清单覆盖度量地图（ORB-SLAM 系）→Neural SLAM→语义图/场景图，且'显式空间记忆优于通用检索'——SLAM 家族被吸收为智能体记忆实现族
- Quote: “These failures cluster into four categories, each traceable to a specific representational gap: (1) spatial hallucination, where agents describe impossible spatial configurations (GPT-4V fails on 40% of spatial relationship questions in SpatialBench [Chen et al., 2024a]).”
- Authors: gloria-felicia; nolan-bryant; handi-putra; et al.

### EA-SLAMCORE-2026-0055

- Claim: 综述指出长时程评测缺口与 LLM 架构的直接关联：即使 128K token 上下文窗口，以 30 observations/second 接收观测的智能体在 90 分钟内耗尽上下文；更长任务需要外部记忆系统，而现行基准不评测——'智能体应如何在扩展时间视野上压缩、检索、更新空间知识'这一根本问题保持未测试状态；现实任务要求数小时到数天的持续性能与记忆持久化。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.01644](https://arxiv.org/abs/2602.01644) From Perception to Action: Spatial AI Agents and World Models
- Locator: page 19, Section 9.3 Long-Horizon Evaluation
- Evidence: 128K 上下文 @30 observations/second 在 90 分钟内耗尽——长时程任务必需外部记忆系统，而现行基准不评测（作者算术论证）
- Quote: “This limitation is directly tied to LLM architecture: even with 128K token context windows, an agent receiving 30 observations per second exhausts its context in under 90 minutes. Longer tasks require external memory systems that current benchmarks do not evaluate.”
- Authors: gloria-felicia; nolan-bryant; handi-putra; et al.

### EA-SLAMCORE-2026-0215

- Claim: 核心实证发现'主动-被动差距'（Active-Passive Gap）：当下游任务要求智能体自主采集信息而非消费预生成轨迹时性能系统性退化（摘要口径 GPT-5.2: 0.57→0.46，vision-world 被动→主动平均分）；并伴随第二个瓶颈'低效性'——模型以非系统、高冗余方式探索，效率不及程序化代理且结果并不更好。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 1, Abstract
- Evidence: 主动-被动差距：模型须自主采集信息时性能退化（GPT-5.2 0.57→0.46），且探索非系统、高冗余、效率不及程序代理
- Quote: “Our evaluation of state-of-the-art models on a suite of downstream tasks reveals critical bottlenecks: (1) The Active-Passive Gap: Performance degrades when agents must autonomously gather information (e.g., GPT-5.2: 0.57→0.46); (2) Inefficiency: Models explore in an unsystematic way and with high redundancy, failing to match the efficiency of program-based proxies while producing no better results.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0216

- Claim: 效率差距：基于规则的脚本代理约 9 步即达到目标覆盖率，而基础模型冗余探索需至少 14 步且不带来信念精度提升——程序化系统探索在效率与效果上均优于最前沿基础模型的自主探索。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 3, Section 1 Introduction 末段
- Evidence: 效率差距：规则代理约 9 步达目标覆盖率 vs 基础模型 ≥14 步且不提升信念精度
- Quote: “We also find a major efficiency gap: rule-based proxy agents reach target coverage in ∼ 9 steps, whereas foundation models explore redundantly, requiring ≥ 14 steps without improving belief accuracy.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0218

- Claim: 信念不稳定与退化：即使物体最初被正确感知，后续轮次智能体也频繁以错误预测覆写已验证事实，空间记忆随回合累积而退化——低最终正确性不只源于感知误差，更源于不稳定信念更新的累积效应（valid spatial memories degrade over the course of the episode）。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 12, Section 5.1 Stability & Decay 段
- Evidence: 信念不稳定：正确感知的事实被后续错误预测覆写，空间记忆随回合累积退化
- Quote: “This performance gap highlights a critical failure in state maintenance: even when objects are correctly perceived initially, the agent frequently overwrites these verified facts with incorrect predictions in subsequent turns. Thus, the low final Correctness stems not solely from perceptual errors, but from the cumulative effect of unstable belief updates, where valid spatial memories degrade over the course of the episode.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0219

- Claim: False Belief 范式揭示'空间信念惯性'（spatial belief inertia）：环境改变（物体重定位/重定向）后重新探索时，即使直接观测到新配置，模型仍坚持初始的、已不正确的坐标——基础模型缺乏响应物理变化修正内部认知地图的可塑性；该问题在文本智能体中存在、视觉模型中尤为严重。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 3, Section 1 Introduction 倒数第二段
- Evidence: 信念惯性：环境变化后即使直接观测到新配置，模型仍坚持初始错误坐标——缺乏修正内部认知地图的可塑性
- Quote: “By altering the environment (relocating or reorienting objects) after the agent’s initial exploration, we uncover a phenomenon we term spatial belief inertia: agents (particularly in vision-based settings) struggle to overwrite obsolete spatial priors with new sensory evidence. Despite directly observing the new configuration, models persist in their initial, now incorrect coordinates. This reveals a critical failure in spatial memory revision, where foundational models lack the plasticity to re”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0220

- Claim: 信念修正量化失败（Table 7，k=4 物体变化后重探索）：vision-world 中朝向信念惯性 GPT-5.2 达 68.9%、Gemini-3 Pro 51.1%（text 仅 5.5%/7.9%）；朝向变化识别 F1 低至 14.3%/23.9%（text 为 97.9%/98.7%）；位置信念正确性 vision 42.9%/63.1% vs text 69.7%/72.9%；冗余步数 vision 6.20/3.23 vs text 0.55/0.18——视觉智能体的朝向修正接近系统性失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 15, Table 7
- Evidence: Table 7 量化：vision 朝向惯性 68.9/51.1 vs text 5.5/7.9，朝向识别 F1 14.3/23.9 vs text 97.9/98.7——视觉模态修正灾难级失败
- Quote: “Table 7: Belief updating under environmental shifts. After relocating/reorienting k=4 objects, we evaluate change identification, re-exploration cost (including redundancy (red.)), and belief correctness/update in text- vs. vision-worlds. Vision agents require more redundant steps and show severe orientation inertia, failing to overwrite obsolete facing beliefs despite new evidence.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0221

- Claim: 充分性测试（Oracle Map）：将真值认知地图作为条件输入后，两个模型在两个世界中性能均升至约 95% 的近完美水平——认知地图表征已捕获任务所需全部信息，性能瓶颈在于模型无法准确构建该地图，而非表征格式本身。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 12, Section 5.1 Cognitive Map Validation & Correlation 消融段
- Evidence: Oracle 真值地图条件作答升至 ≈95%：显式地图表征充分，瓶颈在模型无法构建而非表征格式
- Quote: “Sufficiency Test (Oracle Map): We conditioned the model on the ground-truth cognitive map before generating answers for evaluation. Performance rose to near-perfect levels (≈ 95% for both models in both worlds). This confirms that our cognitive map representation captures all necessary information for the tasks; performance bottlenecks stem from the agent’s inability to accurately construct the map, not the representation format itself.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0223

- Claim: 方法论立场：认知地图（结构化、allocentric 的地图式表征）被采用为空间隐藏结构的规范（canonical）表征——要求模型在探索任意时刻外化其认知地图以直接评估表征胜任度，把空间评测从行为成功转向对内部空间模型的直接测量。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 4, Section 2.1 第三组件 Explicit Probing of the Internal Spatial Belief
- Evidence: 认知地图被采用为空间隐藏结构的规范表征：地图式显式表征仍是空间能力的度量基准语言
- Quote: “We require the agent to explicitly represent its spatial belief by probing its cognitive map at any point of exploration. Cognitive maps are structured allocentric representations of space, which is well-established in neuroscience (Tolman, 1948; O’Keefe & Dostrovsky, 1971; Hafting et al., 2005). Thus, we use cognitive maps as the canonical representation of the hidden structure of space.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0224

- Claim: 探索行为模式：GPT-5.2 的主动-被动差距源于非系统探索——发现新门即立即跳转检查、当前房间常留未探完，叠加物体遗漏与路径冗余；而表现最好的 Gemini-3 Pro 采用系统性'旋转-扫描'（rotate-and-scan）策略：先扫描周围再转移到新房间——其行为镜像 SCOUT 脚本代理。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 10, Section 4 Exploration Pattern 段
- Evidence: 最优模型 Gemini 的胜出行为恰是镜像 SCOUT 脚本代理的 rotate-and-scan 系统扫描策略；GPT-5.2 则因非系统探索失分
- Quote: “For GPT-5.2, the active-passive performance gap stems from unsystematic exploration. Specifically, the agent tends to prioritize any newly discovered door, immediately jumping to inspect it and often leaving the current room partially unexplored. This is compounded by object omission and path redundancy. In contrast, GEMINI-3 PRO adopts a more methodical “rotate-and-scan” strategy, scanning its surroundings before transitioning to new rooms, which is a behavior mirroring the SCOUT proxy agent.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0086

- Claim: NavMind 证明可行路径是把显式认知图作为可学习中间表示注入模型：基于 Qwen3-VL-8B 经两阶段认知引导渐进 SFT（CogRS 拒绝采样筛选 >3,000 条困难轨迹）后，较平均基线 SR_t/SR_p 提升 43.2%/34.2%、导航误差减少 3.33m、SPL 提升 31.5%——8B 模型大幅超越所有零样本前沿模型（Table 1 整体 SR_t 48.8/SR_p 38.0/SPL 35.2，见 page 5）
- Stance: `support` | Confidence: `direct`
- Paper: [2603.21577](https://arxiv.org/abs/2603.21577) Mind over Space: Can Multimodal Large Language Models Mentally Navigate?
- Locator: page 7
- Evidence: Sec 5.2（page 7）：NavMind 较平均基线 SR_t/SR_p +43.2%/34.2%、NE -3.33m、SPL +31.5%；中/长程 SR_p +36.0%/30.5%。Table 1（page 5）NavMind-Stage2 整体 NE 2.92、SR_t 48.8、SR_p 38.0、SPL 35.2。方法（Sec 5.1）：显式细粒度认知图为可学习中间表示 + CogRS。
- Quote: “Compared with the average baseline performance, NavMind improves SR t /SR p by 43.2%/34.2%, reduces the navigation error by 3.33 m, and increases route efficiency SP L by 31.5%.”
- Authors: qihui-zhu; shouwei-ruan; xiao-yang; et al.

### EA-SLAMCORE-2026-0087

- Claim: 下游 VLN 集成实验：反应式 VLN 模型 Uni-NaVid 单独执行时 274 步仍未找到目标（暴露其长程规划缺陷），接入 NavMind 的全局规划后仅 34 步高效到达；Fig 4(E) 在 20 个不同场景系统验证结构化认知图规划对 VLN 智能体的辅助——全局结构化规划信号是现有反应式导航智能体缺失的必要组件
- Stance: `support` | Confidence: `direct`
- Paper: [2603.21577](https://arxiv.org/abs/2603.21577) Mind over Space: Can Multimodal Large Language Models Mentally Navigate?
- Locator: page 8
- Evidence: Sec 5.3（pages 7-8）：274 步失败案例在 page 7 正文与 page 8 Fig 4（'274 Steps'/'34 Steps'）标注；34 步成功与 20 场景系统对比在 page 8。NavMind 定位为可复用 'navigation brain'，Uni-NaVid 为下游策略执行器。
- Quote: “In contrast, when NavMind is combined with Uni-NaVid, the agent reaches the target efficiently in only 34 actions, significantly improving navigation efficiency.”
- Authors: qihui-zhu; shouwei-ruan; xiao-yang; et al.

### EA-SLAMCORE-2026-0208

- Claim: Table 1 主结果中唯一的负增益出现在 EmbSpatial（具身空间理解基准）：SenseNova-SI-InternVL3-8B 相对基础模型 InternVL3-8B 下降 4.3 个点（72.0 vs 76.3），而同一行中 VSI-Bench 提升 26.7、MindCube 提升 44.2、平均提升 15.8——抽象空间 QA 的大幅提升未迁移到自我中心的具身空间理解。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 6, Table 1
- Evidence: EmbSpatial 是 8 项基准中唯一负增益（-4.3）：抽象空间 QA 提升未迁移到具身空间理解，三骨干全部回退
- Quote: “SenseNova-SI InternVL3-8B 61.5(+15.8) 68.8(+26.7) 43.3(+15.3) 85.7(+44.2) 54.7(+16.0) 47.7(+6.6) 63.9(+10.4) 55.5(+11.2) 72.0(-4.3)”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0209

- Claim: 数据构造：为填补任务覆盖缺口（MM/SR 占主导而 PT/MR 不足、异心视角变换与物体重建未被触及），作者利用富标注、场景多样的 3D 数据集（MessyTable、ScanNet、ScanNet++、SUN RGB-D、CA-1M、Ego-Exo4D、Matterport3D）生成大规模、精确且任务均衡的 QA 对，该缩放过程贡献 4.5M 数据，使语料总量达 8.5M QA 对。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 5, Section 3.2 Data Sources
- Evidence: 4.5M 增量空间 QA 由 ScanNet/ScanNet++/Matterport3D 等 7 个 3D 数据集生成——显式几何以训练监督形式进入基础模型
- Quote: “To address these gaps, we leverage richly annotated, scene-diverse 3D datasets, including MessyTable [ 6 ], ScanNet [14], ScanNet++ [69 ], SUN RGB-D [47], CA-1M [29 ], Ego-Exo4D [23], and Matterport3D [8], to generate large-scale, accurate and task-balanced QA pairs. This scaling process contributes 4.5M data, increasing the overall corpus size to 8.5M QA pairs.”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0214

- Claim: 下游具身操作验证的输入接口：EmbodiedBench 设定中 SenseNova-SI 控制仿真 Franka Panda 机械臂，agent 接收环境的符号化描述——每个物体表示为桌面坐标系中的离散 3D 位置——并被要求输出同一离散坐标系下的低层抓取动作序列（末端执行器位置、朝向与二值夹爪状态）；度量空间状态由外部供给而非模型自身感知。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 21, Appendix H.1
- Evidence: 具身验证接口：物体以外部供给的离散 3D 位置输入、输出 7 维离散动作——度量空间状态非模型自产，被静默外包给仿真器
- Quote: “Conditioned on a language instruction and the visual state of the scene, the agent receives a symbolic description of the environment, where each object is represented by a discrete 3D position in a table-top coordinate frame. The model is required to output a sequence of low-level gripper actions in a structured action space, where each action specifies the target end-effector position, orientation, and a binary gripper state, all expressed in the same discretized coordinate system.”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0048

- Claim: 作者结论：当前 LLM/VLM 更宜被视为辅助推理组件（assistive reasoning components）而非自主决策者（autonomous decision makers）；从『解决任务』到『安全且可靠地解决任务』的转变仍然脆弱，部署于安全关键机器人系统前需要失败中心的评测
- Stance: `support` | Confidence: `direct`
- Paper: [2601.05529](https://arxiv.org/abs/2601.05529) Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models
- Locator: page 7
- Evidence: 讨论（page 7）：能力在结构显式、约束易满足时成立，但不一致地迁移到不完全上下文推断、稳定视觉-空间接地或竞争线索下的安全优先；结论重申失败中心评测的必要性。
- Quote: “In their current form, they are better viewed as assistive reasoning components than as autonomous decision makers.”
- Authors: jua-han; jaeyoon-seo; jungbin-min; et al.

### EA-SLAMCORE-2026-0093

- Claim: 在 Target-Bench（真实世界非结构化室内外场景、语义目标导航轨迹预测基准）的投影 2D 像素空间评测中，WorldMAP（Qwen3-VL-8B 学生骨干，测试时仅运行轻量学生、无需在线建图）取得全部对比方法中最优的 ADE 42.06 与 FDE 38.87：相对最佳竞争基线 Gemini-3-Pro，ADE 从 51.27 降至 42.06（-18.0%）、FDE 从 67.19 降至 38.87（-42.1%），normalized DTW 31.95 与 Gemini-3-Pro 的 31.63 接近。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07957](https://arxiv.org/abs/2604.07957) WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models
- Locator: page 6, Table I
- Evidence: Target-Bench 上 WorldMAP ADE 42.06 / FDE 38.87 最优，相对 Gemini-3-Pro 降低 18.0% / 42.1%
- Quote: “WorldMAP achieves the best ADE and FDE among all compared methods. Relative to the best competing baseline, Gemini-3-Pro, it reduces ADE from 51.27 to 42.06 (18.0%) and FDE from 67.19 to 38.87 (42.1%), while remaining close on normalized DTW (31.95 vs. 31.63).”
- Authors: hongjin-chen; shangyun-jiang; tonghua-su; et al.

### EA-SLAMCORE-2026-0149

- Claim: 作者观察：在 LMM 导航中'用深度信息评估位置与距离是提升空间导航能力最直接的途径'，这类基于人类先验设计的方法持续提升性能（尽管泛化有限）；agent 方法因此仍是高效稳定的方案——即外部几何/位姿-距离评估对 LMM 导航有直接且稳定的价值。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07973](https://arxiv.org/abs/2604.07973) How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace
- Locator: page 6, Section 5.2
- Evidence: 用深度评估位置与距离是提升 LMM 空间导航最直接的途径（agent 方法 RGB+深度更稳）
- Quote: “Agent-based methods remain the efficient and stable solution. Incorporating depth information to assess position and distance is the most straightforward way to enhance spatial navigation capabilities. This approach, often designed based on human priors, consis- tently improves performance, albeit with limited generalization.”
- Authors: baining-zhao; ziyou-wang; jianjie-fang; et al.

### EA-SLAMCORE-2026-0150

- Claim: 几何感知增强实验（GPT-4o 骨干）：把 LMM 的职责缩小为'识别当前观测中的导航目标'，由 GroundingDINO 做 2D 定位、确定性控制器负责把目标居中并前进的两阶段模块化管线，使导航成功率提升 9.5%（Table 3：14.7→24.2）；作者据此判断 LMM 缺乏显式几何编码与对齐，建议未来引入几何编码器或几何感知训练目标。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07973](https://arxiv.org/abs/2604.07973) How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace
- Locator: page 7, Section 6 与 Table 3；page 14, Appendix D.1
- Evidence: 模块化几何管线（GroundingDINO+确定性控制器）使 SR 14.7→24.2（+9.5），LMM 缺几何编码
- Quote: “To address the limita- tions in LMMs’ geometric perception capabilities, we employed grounding models to first mark the targets that LMMs focus on before outputting actions. This approach improved navigation success rates by 9.5%. This indicates that LMMs may lack geo- metric encoding and alignment, suggesting future exploration of additional geometric encoders or strengthening through training loss enhancements.”
- Authors: baining-zhao; ziyou-wang; jianjie-fang; et al.

### EA-SLAMCORE-2026-0151

- Claim: 失败案例分析（Qwen2.5-VL-7B 案例）指出：持久空间记忆或类地图表征（map-like representation）的缺失，使模型无法推理未探索的区域、也无法回到有希望的方向——模型被局部视觉线索主导，重复访问相似视点、漂移出预期搜索空间（甚至进入室内并意外降落）；跨视角理解与全局朝向的缺失与之并存。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07973](https://arxiv.org/abs/2604.07973) How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace
- Locator: page 13, Appendix C
- Evidence: 持久空间记忆/类地图表征缺失使 LMM 无法推理未探索区域并回到有希望方向
- Quote: “The absence of a persistent spatial memory or map-like representation prevents the model from reasoning about unexplored regions or returning to promising directions.”
- Authors: baining-zhao; ziyou-wang; jianjie-fang; et al.

### EA-SLAMCORE-2026-0104

- Claim: 综述对稀疏特征 SLAM 的剖析显示：典型建筑级 ORB-SLAM3 会话产出约 55 MB 地图、α_CPU≈4（EuRoC 上 180–250 MB 峰值 CPU RSS，Intel i7-10700），低 α 意味着地图大小可可靠预测部署成本；三个稀疏系统（含峰值仅 150 MB 的 VINS-Mono）均在单核 CPU 上以 20–30 FPS 舒适实时运行（其 EuRoC ATE 3.5 cm 为表内最优，转引自 ORB-SLAM3 原论文）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.16482](https://arxiv.org/abs/2604.16482) A Survey of Spatial Memory Representations for Efficient Robot Navigation
- Locator: page 3, Section 3.2 + Table 1
- Evidence: 稀疏 SLAM：α_CPU≈4、180–250 MB 峰值 RSS、单核 CPU 20–30 FPS 实时——部署成本可预测的经典基础设施
- Quote: “VINS-Mono [52] (10.6 cm monocular-inertial, Eff. = 2.4) trails on ATE but operates within 150 MB peak using only a monocular camera. All three sparse systems sustain 20–30 FPS (Table 1), comfortably real-time on a single CPU core.”
- Authors: ma-madecheen-s-pangaliman; steven-s-sison; erwin-p-quilloy; et al.

### EA-SLAMCORE-2026-0106

- Claim: 综述指出场景图范式的语义抽象层并不自足：Hydra 及其后续在 Jetson Xavier NX（8 GB）上以 5 Hz 构建层级场景图、48 MB 图抽象层，但该数字不含底层 Kimera 度量-语义网格（ATE ∼5 cm），总内存随场景变化且被低估；作者结论：图抽象层本身紧凑，但度量后端可与神经地图相当——即场景图语义层之下仍是度量-语义 SLAM 后端。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.16482](https://arxiv.org/abs/2604.16482) A Survey of Spatial Memory Representations for Efficient Robot Navigation
- Locator: page 4, Section 3.4
- Evidence: 场景图 48 MB 图层不含 Kimera 度量-语义后端——'图紧凑但度量后端可与神经地图相当'，语义层之下仍是 SLAM
- Quote: “The key memory question for scene graphs is which layers count: the graph alone is compact, but the metric backend can rival a neural map.”
- Authors: ma-madecheen-s-pangaliman; steven-s-sison; erwin-p-quilloy; et al.

### EA-SLAMCORE-2026-0031

- Claim: Target-Bench 基准的全部真值基础设施建立在 SLAM 之上：450 个机器人采集场景以 SLAM 轨迹作为运动趋势参考，评测管线显式依赖 SLAM-based ground-truth robot paths
- Stance: `support` | Confidence: `direct`
- Paper: [2511.17792](https://arxiv.org/abs/2511.17792) Target-Bench: Can Video World Models Achieve Mapless Path Planning with Semantic Targets?
- Locator: page 1
- Evidence: 摘要与结论两处明确：SLAM 轨迹是 benchmark 的运动参考（摘要）且评测是 against SLAM-based ground-truth robot paths（结论）。无图方法的'图'由 SLAM 在评测侧补齐。
- Quote: “Target-Bench provides 450 robot-collected scenarios spanning 47 semantic categories, with SLAM-based trajectories serving as motion tendency references.”
- Authors: dingrui-wang; zhihao-liang; hongyuan-ye; et al.

### EA-SLAMCORE-2026-0032

- Claim: 数据采集栈采用 LiDAR 中心 SLAM 管线（IMU+腿式里程计 EKF 融合、运动补偿点云配准、G2O 后端轨迹优化），产出全部度量轨迹与点云地图，使该数据集成为唯一同时具备度量轨迹、语义目标、点云与运动学一致性的导航数据集
- Stance: `support` | Confidence: `direct`
- Paper: [2511.17792](https://arxiv.org/abs/2511.17792) Target-Bench: Can Video World Models Achieve Mapless Path Planning with Semantic Targets?
- Locator: page 5
- Evidence: Sec 3.1.1 描述软件栈：LiDAR-centric SLAM pipeline + multi-sensor fusion，EKF 融合 IMU 与腿式里程计产生基座位姿，SLAM 前端做运动补偿与增量配准，后端优化轨迹并建全局地图；Table 1 中该数据集是唯一四项全有的数据集。
- Quote: “centric SLAM pipeline [20, 33] with multi-sensor fusion. Inertial Measurement Unit (IMU) data and legged odometry are fused via an Extended Kalman Filter (EKF) to produce a stable base-frame pose”
- Authors: dingrui-wang; zhihao-liang; hongyuan-ye; et al.

### EA-SLAMCORE-2026-0033

- Claim: 在 125 场景基准集、8 秒时域、VGGT decoder 条件下，最强现成视频世界模型 Wan2.2-Flash 的加权总分仅 0.341（FDE 1.362m、ADE 1.005m、MR 38.75%），而真值视频噪声底为 0.862——当前世界模型的无图语义路径规划能力远不可靠
- Stance: `support` | Confidence: `direct`
- Paper: [2511.17792](https://arxiv.org/abs/2511.17792) Target-Bench: Can Video World Models Achieve Mapless Path Planning with Semantic Targets?
- Locator: page 12
- Evidence: Table 3 完整结果：11 个模型变体中 Wan2.2-Flash 最佳（0.341），Sora 2 仅 0.207、Veo 3.1 仅 0.210；MR 在 38.75%–77.25% 之间；讨论节明确'a significant gap between current world model capabilities and reliable path planning'。分母条件：125 基准场景、gt_video 噪声底 0.862 作为上界参照。
- Quote: “The best off-the-shelf video WM, Wan2.2-Flash, achieves only 0.341 overall score. This indicates a significant gap between cur-”
- Authors: dingrui-wang; zhihao-liang; hongyuan-ye; et al.

### EA-SLAMCORE-2026-0035

- Claim: 仅在 325 个 SLAM 标注的真实机器人场景（含 4 倍移帧增广）上 LoRA 微调开源 Wan2.2-5B，加权总分从 0.084 提升至 0.330，数据增广后达 0.394（较基座 +469%），超越全部现成模型——SLAM 标注的真实机器人数据是世界模型数据高效适应的关键使能
- Stance: `support` | Confidence: `direct`
- Paper: [2511.17792](https://arxiv.org/abs/2511.17792) Target-Bench: Can Video World Models Achieve Mapless Path Planning with Semantic Targets?
- Locator: page 12
- Evidence: Sec 4.3：用训练集 325 场景微调 Wan2.2-TI2V-5B（DiffSynth-Studio LoRA，8×A800 80GB），文本 prompt+首帧输入；FT 版 0.330、FT-DA 版 0.394，均为 8s/720p、VGGT decoder、unseen 数据评测；作者结论'微调小模型超越全部现成模型，说明 WM 能从有限真实数据有效学习导航任务'。
- Quote: “The fine-tuned Wan2.2-5B (Wan2.2-5B-FT) improves its score from 0.084 to 0.330. The augmented version (Wan2.2-5B-FT-DA) outperforms the base model by more than 469% and achieves the best overall score.”
- Authors: dingrui-wang; zhihao-liang; hongyuan-ye; et al.

### EA-SLAMCORE-2026-0036

- Claim: 规划时域从 8s 缩短到 4s 时，被测世界模型加权总分一致提升（Wan2.2-Flash 0.341→0.363，Wan2.2-Plus 0.290→0.339），作者结论为世界模型仅在较短时间窗口内规划更可靠——长时域无图导航的可靠性尚未建立
- Stance: `support` | Confidence: `direct`
- Paper: [2511.17792](https://arxiv.org/abs/2511.17792) Target-Bench: Can Video World Models Achieve Mapless Path Planning with Semantic Targets?
- Locator: page 14
- Evidence: Table 6：两个模型 × 三个时域（8s/6s/4s）的完整对比；Wan2.2-Flash 6s 时 MR 从 38.75% 降至 23.76%；Sec 4.5 原文结论 'the weighted score consistently improves as the horizon decreases, suggesting that WMs are more reliable when planning on shorter temporal windows'。
- Quote: “improves as the horizon decreases, suggesting that WMs are more reliable when planning on shorter temporal windows.”
- Authors: dingrui-wang; zhihao-liang; hongyuan-ye; et al.

### EA-SLAMCORE-2026-0123

- Claim: 无图探索路线内部仍消费几何基础模型：VANDERER 的新颖性度量使用 MASt3R 的快速互惠匹配做 patch 级几何对应，且消融显示去掉该几何匹配模块后 Area 从 12299 降至 11248（APL 3.120→2.856）
- Stance: `support` | Confidence: `direct`
- Paper: [2606.14879](https://arxiv.org/abs/2606.14879) VANDERER: Map-Free Exploration using Future-Aware and Visual-Curiosity-Guided Diffusion Policy
- Locator: page 4
- Evidence: Sec III-A：MASt3R fast reciprocal matching 建立 patch 一一对应，相似度 D 取 top-250 最远对应 patch 对的平均欧氏距离；Table II 消融：w/o fast reciprocal matching（换逐 patch L2）Area 11248/APL 2.856 vs 完整方法 12299/3.120，且作者论证互惠匹配'有效解释几何变化'（跨视角同一区域）。
- Quote: “we utilize MASt3R’s [34] fast reciprocal matching on patch-level features (Algorithm. 1).”
- Authors: venkata-naren-devarakonda; raktim-gautam-goswami; prashanth-krishnamurthy; et al.

### EA-SLAMCORE-2026-0124

- Claim: 扩散策略先验对无图探索不可或缺：去掉扩散策略（改高斯采样+CEM）后 Area 从 12299 骤降至 7072（APL 3.120→1.845，PF 0.03%→4.35%），执行时间约 4 倍——学习到的动作先验是该方法可行的前提
- Stance: `support` | Confidence: `direct`
- Paper: [2606.14879](https://arxiv.org/abs/2606.14879) VANDERER: Map-Free Exploration using Future-Aware and Visual-Curiosity-Guided Diffusion Policy
- Locator: page 7
- Evidence: Table II 第二行消融；作者分析：无强先验时'单步优化得次优动作且频繁碰撞，多步优化则计算不可行'，故约 4 倍执行时间。训练数据为 CARLA BasicAgent 无碰撞轨迹（每镇微调 20 epochs）。
- Quote: “Ablat- ing this component introduces a fundamental trade- off: a single optimization step (faster computation) yields suboptimal actions and frequent collisions, while increasing optimization iterations renders the method computationally impractical.”
- Authors: venkata-naren-devarakonda; raktim-gautam-goswami; prashanth-krishnamurthy; et al.

### EA-SLAMCORE-2026-0158

- Claim: 白皮书指出在具身数据采集与机器人执行中，功能算子起中心作用：把 RGB 图像、深度观测、视频、点云、机器人状态、语言指令、人类示教转换为可用标注、表征、规划与控制信号；典型输出包括物体位姿、相机轨迹、深度图、重建场景、手部运动轨迹、抓取位姿、无碰撞轨迹等，为示教解析、操作策略学习、模仿学习、仿真资产构建、任务规划与闭环执行提供必要支撑。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.03283](https://arxiv.org/abs/2607.03283) Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied Intelligence Systems
- Locator: page 2, Section 1 Introduction
- Evidence: 数据采集环节：算子起中心作用，典型输出含相机轨迹/物体位姿/深度图/重建场景（SLAM 类产物）
- Quote: “In embodied data collection and robot execution, these operators play a central role in converting RGB images, depth observations, videos, point clouds, robot states, language instructions, and human demon- strations into usable annotations, representations, plans, and control signals. Typical outputs include hand bounding boxes, hand masks, object poses, camera trajectories, depth maps, reconstructed scenes, hand key- points, hand motion trajectories, action proposals, grasp poses, collision-fr”
- Authors: junwu-xiong; jiaxuan-gao; wei-chai; et al.

### EA-SLAMCORE-2026-0159

- Claim: 该白皮书的中心主张：高质量具身智能系统不能只依赖端到端策略模型；在数据采集、示教理解、场景重建、机器人学习、任务决策与机器人执行的实际流水线中，需要大量可复用功能模块把原始多模态信号与中间系统状态转换为结构化表征、决策与可执行输出。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.03283](https://arxiv.org/abs/2607.03283) Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied Intelligence Systems
- Locator: page 1, Section 1 Introduction
- Evidence: 中心论题：具身系统不能只靠端到端策略模型，采集到执行各环节需可复用功能算子
- Quote: “However, high-quality embodied intelligence systems cannot rely solely on end-to-end policy models. In practical pipelines for data collec- tion, demonstration understanding, scene reconstruction, robot learning, task decision-making, and robot execution, numerous reusable functional modules are required to transform raw multimodal signals and in- termediate system states into structured representations, decisions, and executable outputs.”
- Authors: junwu-xiong; jiaxuan-gao; wei-chai; et al.

### EA-SLAMCORE-2026-0160

- Claim: 五类算子分类学把'空间定位与 3D 理解'列为与视觉感知、人体与动作理解、具身基础模型、规划控制并列的独立类别，其组成包括深度估计、6D 位姿估计、SLAM、点云处理、3D 重建、占用预测与视觉里程计；同页 Table 1 把 ORB-SLAM3 与 FoundationPose、Depth Anything、DUSt3R/MASt3R、VGGT 并列为该类代表算子，职能为'为操作与导航估计物体位姿、相机运动、深度、场景几何与空间约束'。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.03283](https://arxiv.org/abs/2607.03283) Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied Intelligence Systems
- Locator: page 4, Section 2.2 与 Table 1
- Evidence: 分类学：'空间定位与 3D 理解'是五大算子类别之一（含 SLAM 与视觉里程计），Table 1 中 ORB-SLAM3 与 DUSt3R/VGGT 并列
- Quote: “The second category is spatial localization and 3D understanding operators, including depth estimation, 6D pose estimation, SLAM, point cloud processing, 3D reconstruction, occupancy prediction, and visual odometry. These operators enable robots to infer object locations, camera or robot motion, and the geometric structure of the surrounding environment.”
- Authors: junwu-xiong; jiaxuan-gao; wei-chai; et al.

### EA-SLAMCORE-2026-0161

- Claim: 白皮书设专职小节把 SLAM 定义为具身系统中的定位算子：SLAM（同时定位与建图）指智能体在未知环境中同时估计自身位姿并构建环境地图的过程，作为定位算子为导航、路径规划、场景重建与操作任务提供连续空间参考；近年 SLAM 研究已从经典优化管线与早期学习方法快速转向基于 Transformer 与神经场景表征的方法；ORB-SLAM3 仍是特征点法中广泛使用的强基线，SplaTAM（3D 高斯泼溅稠密 RGB-D SLAM 高保真实时重建）与 MASt3R-SLAM（利用视觉基础模型几何重建先验实现复杂真实开放场景的鲁棒跟踪与稠密建图）代表新方向。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.03283](https://arxiv.org/abs/2607.03283) Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied Intelligence Systems
- Locator: page 7, Section 4.1
- Evidence: 4.1 专职小节：SLAM 为导航/规划/重建/操作提供连续空间参考；范式转向 Transformer/神经表征，ORB-SLAM3 仍是强基线
- Quote: “As a localization operator in embodied systems, SLAM provides a continuous spatial reference for navigation, path planning, scene reconstruction, and manipulation tasks. In recent years, SLAM research has rapidly shifted from classical optimization-based pipelines and early learning-based methods toward approaches based on Transformers and neural scene representations. ORB- SLAM3 [28] is a widely used classical visual SLAM system and remains a strong baseline among feature-based SLAM methods.”
- Authors: junwu-xiong; jiaxuan-gao; wei-chai; et al.

### EA-SLAMCORE-2026-0163

- Claim: 三阶段平台路线图中，近期（near-term）优先建设的算子集明确包括'SLAM 与导航'（引用 ORB-SLAM3 与 Nav2/Marathon 2 系），与开放词汇检测与视频分割、立体深度与 6D 位姿估计、抓取与轨迹规划、动作恢复、部署/通信/调度并列——即 SLAM 被列入产业平台近一年优先落地清单，而非被淘汰项。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.03283](https://arxiv.org/abs/2607.03283) Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied Intelligence Systems
- Locator: page 22, Section 8.6.5
- Evidence: 近期平台优先算子集明确包含 SLAM 与导航（引 ORB-SLAM3 与 Nav2/Marathon 2）
- Quote: “The priority set includes open-vocabulary detec- tion and video segmentation [22, 26], stereo depth and 6D pose estimation [31, 93], SLAM and navigation [28, 89], grasp and trajectory planning [58–61], motion recovery [13, 71], and deployment, communication, and scheduling [9–11, 62, 64, 74].”
- Authors: junwu-xiong; jiaxuan-gao; wei-chai; et al.

### EA-SLAMCORE-2026-0068

- Claim: 轨迹对齐预训练阶段将约 155 万条机器人轨迹（AgibotWorld Beta 真机 1M + InternData-A1 仿真 550K）的末端执行器位姿全部经由数据集提供的标定参数变换到统一相机中心坐标系，使非机器人 3D 数据与机器人示教数据共享同一几何参考系。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.19710](https://arxiv.org/abs/2602.19710) PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Policies
- Locator: page 5, Section III-F Pre-training Datasets
- Evidence: 约 1.55M 条轨迹经数据集标定参数投影到统一相机系构成预训练语料
- Quote: “This stage aligns spatial features with motion control using nearly 1.55M trajectories. All end-effector poses are transformed into a unified camera-centric frame via calibration parameters provided by datasets.”
- Authors: haitao-lin; hanyang-yu; jingshun-huang; et al.

### EA-SLAMCORE-2026-0071

- Claim: 在统一后训练预算（80K steps、batch 32）下的 RoboTwin 2.0 对比中，Pose-VLA（RGB-only 评测）Easy 79.91%/Hard 79.10%，超过 π0（67.00/65.12）约 12-14 个百分点、超过 vanilla PaliGemma+expert（35.40/33.36）逾 45 个百分点；LIBERO 四 suite 平均 96.0%（Long 92.4 与 π0.5 并列第一，平均仅次于 π0.5 的 96.8）。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.19710](https://arxiv.org/abs/2602.19710) PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Policies
- Locator: page 7, Table II（正文 SOTA 声明见 page 6）
- Evidence: RoboTwin 2.0 Easy 79.91/Hard 79.10（超 π0 约 12-14 pp）；LIBERO 96.0%
- Quote: “Average (%) 67.00 65.12 79.48 76.16 35.40 33.36 79.91 79.10 89.40 88.60”
- Authors: haitao-lin; hanyang-yu; jingshun-huang; et al.

### EA-SLAMCORE-2026-0022

- Claim: 在 5 个高欺骗性 episode × 10 次重复的死锁规避测试中，去掉记忆队列的无图导航 SR 仅 12.0、逃逸率（ER）32.0%；加入动态有界记忆队列后 SR 升至 48.0（4 倍）、ER 升至 82.0%，失败案例距目标距离 DTS(f) 从 6.7 降至 4.7——隐式文本记忆显著补偿了缺失度量地图的防重访功能，但欺骗性场景下成功率仍不足一半、死锁未完全消除。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.06840](https://arxiv.org/abs/2511.06840) PanoNav: Mapless Zero-Shot Object Navigation with Panoramic Scene Parsing and Dynamic Memory
- Locator: page 5, Table 2
- Evidence: 死锁测试：记忆队列使欺骗场景 SR 12.0→48.0、逃逸率 32.0%→82.0%，但 SR 仍仅 48%、死锁未根除
- Quote: “SR↑ SPL↑ DTS (f)↓ ER↑ without Memory 12.0 4.9 6.7 32.0 with Memory 48.0 19.2 4.7 82.0”
- Authors: qunchao-jin; yilin-wu; changhao-chen

### EA-SLAMCORE-2026-0169

- Claim: SMG 的构建显式依赖外部相机位姿：作者按标准做法（引 GaussNav、BSC-Nav）为每个室内场景采集带位姿的示教游览，对示教帧的外参相机位姿做最远点采样（FPS）得到稀疏空间代表位置，据此定义节点区域——即记忆图的几何骨架来自离线位姿输入，而非在线估计；论文未讨论这些位姿在真实部署中的来源。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.22609](https://arxiv.org/abs/2511.22609) MG-Nav: Dual-Scale Visual Navigation via Sparse Spatial Memory
- Locator: page 3, Sec 3.2
- Evidence: SMG 构建依赖带位姿示教游览（FPS 作用于外参相机位姿）——离线记忆构建仍需位姿基础设施
- Quote: “More specifically, for each indoor scene, we first fol- low standard practice to collect posed tour demonstrations [13, 24]. We then apply Farthest-Point Sampling (FPS) to the extrinsic camera poses of the demonstration frames to obtain sparse but spatially representative locations.”
- Authors: bo-wang; jiehong-lin; chenzhi-liu; et al.

### EA-SLAMCORE-2026-0050

- Claim: 综述以传感/执行约束论证空间尺度三分边界：中观尺度（1m–100m，房间导航/建筑探索/室内外局部场景）对应机载相机与激光雷达的有效视场——'metric SLAM remains tractable'（度量 SLAM 在此仍可解）；作者同时把宏观尺度（>100m）划为必须依赖外部感知（卫星、城市级传感网）且无法直接对环境执行动作的范围，微观尺度（<1m）划为触觉传感器有效范围与机械臂工作区。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.01644](https://arxiv.org/abs/2602.01644) From Perception to Action: Spatial AI Agents and World Models
- Locator: page 5, Section 4.1 Taxonomy Axes (Axis 3: Spatial Scale)
- Evidence: 尺度边界论证：1–100 m 中观尺度 = 机载相机/激光雷达视场内 metric SLAM 仍可解；<1m 属操作、>100 m 需外部感知
- Quote: “Meso-spatial (1m–100m): Room navigation, building exploration, indoor/outdoor local scenes. This range corresponds to the effective field of view of onboard cameras and lidar, where metric SLAM remains tractable.”
- Authors: gloria-felicia; nolan-bryant; handi-putra; et al.

### EA-SLAMCORE-2026-0053

- Claim: 在场景理解小节，综述指出 NeRF/3DGS 表示进展与 SLAM 的集成（引用链经参考文献核实：iMAP/Sucar 2021、NICE-SLAM/Zhu 2022、SplaTAM/Keetha 2024、DVM-SLAM/Bird 2025、DROID-SLAM/Teed & Deng 2021、DPVO/Teed et al. 2024、ORB-SLAM2/ORB-SLAM3）是在线重建的使能机制；同时 6.1 导航小节的微综述把领域叙事概括为'从显式建图到隐式空间推理的演化'（We highlight the evolution from explicit mapping to implicit spatial reasoning）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.01644](https://arxiv.org/abs/2602.01644) From Perception to Action: Spatial AI Agents and World Models
- Locator: page 10, Section 6.2 Scene Understanding
- Evidence: 在线重建路径 = 与 SLAM 集成（iMAP→NICE-SLAM→SplaTAM→DVM-SLAM→DROID-SLAM/DPVO）；叙事话语则是'显式建图→隐式空间推理'——话语与引用链存在张力
- Quote: “However, it is crucial to note that while LLMs can model abstract state transitions, they currently lack the fine-grained physical fidelity of dedicated world models, a critical limitation for tasks requiring precise geometric and physical reasoning.”
- Authors: gloria-felicia; nolan-bryant; handi-putra; et al.

### EA-SLAMCORE-2026-0217

- Claim: 模态差距贯穿全部认知地图质量指标：vision-world 认知地图朝向正确性仅 20.2%（GPT-5.2）/32.2%（Gemini-3 Pro），text-world 达 91.0%/92.5%；感知是最初的瓶颈，物体朝向识别近乎随机水平（near-chance facing Correctness）——视觉模态下基础模型的隐式空间信念构建远未成熟，而符号化输入下空间推理已相当强。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 12, Section 5.1 Cognitive Map Probing（Table 5 与分析段）
- Evidence: 模态差距：vision 朝向正确性 20.2/32.2 vs text 91.0/92.5，感知（尤其朝向）是瓶颈——符号输入下推理已强
- Quote: “Perception remains a key limitation for state-of-the-art models in visual world settings. In particular, recognizing an object’s facing direction is especially challenging: agents frequently fail to infer orientation and achieve near-chance (or worse) facing Correctness.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0020

- Claim: 真机实验中，注入深度与相机位姿显著增强 FALCON 的鲁棒性：在涉及物体高度变化的场景中任务成功率从 60% 提升到 80%；同时 RGB-only 训练的模型测试时注入深度即可将 CALVIN ABC→D 的 Avg. Len. 从 3.91 提到 3.95、达到 RGB-D 训练水平——几何传感器输入在可用时仍有增量价值，但模型对缺失保持鲁棒。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.17439](https://arxiv.org/abs/2510.17439) From Spatial to Actions: Grounding Vision-Language-Action Model in Spatial Foundation Priors
- Locator: page 11, Section 4.3 Modality Transferability
- Evidence: 条件性：深度+相机位姿使真机高度变化任务 60%→80%，但 RGB-only 仍可用且测试时可注入
- Quote: “Real-world experiments further validate that incorporating depth and camera poses significantly enhances FALCON’s robustness (Fig. 7), increasing task success rates from 60% to 80% in scenarios involving objects of varying heights.”
- Authors: zhengshen-zhang; hao-li; yalun-dai; et al.

### EA-SLAMCORE-2026-0085

- Claim: Video2Mental 把『带相机位姿的自我中心视频』定义为心理导航任务的感知输入（位姿为仿真器逐帧记录的真值），评测由 Habitat-Sim pointnavigator 完成物理交互验证——『不依赖显式地图』的心理导航范式仍以位姿流与仿真器世界模型为隐性基础设施前提
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.21577](https://arxiv.org/abs/2603.21577) Mind over Space: Can Multimodal Large Language Models Mentally Navigate?
- Locator: page 3
- Evidence: page 3 Sec 2 任务形式化：感知输入=视频+关联相机位姿 (x,y,z,θ_yaw)；Sec 3.1 数据四元组含 'an egocentric exploratory video with continu- ous pose tracking'；Sec 3.2 'At each frame, we log the agent's 3D position and yaw'；page 5 Sec 3.3 评测在 Habitat-Sim pointnavigator 上执行。全文 0 次提及 SLAM，位姿来源问题未被讨论。
- Quote: “The perceptual in- put is an egocentric video sequence V = {f 1 , . . . , f T } with associated camera poses (x i , y i , z i , θ yaw i ).”
- Authors: qihui-zhu; shouwei-ruan; xiao-yang; et al.

### EA-SLAMCORE-2026-0210

- Claim: 作者自认数据缩放的边界：性能增益随训练数据量增加而逐渐递减，作者'认同更广泛社区的观点——单靠数据缩放不太可能达到人类水平的空间智能'，并因此完全开源 SenseNova-SI 权重，让社区跳过昂贵的缩放阶段、转而在强空间能力基础上推进算法创新。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 7, Section 5.3.2 Saturation
- Evidence: 作者自认：收益递减，'单靠数据缩放不太可能达到人类水平空间智能'，需算法创新/范式转变
- Quote: “While it remains unclear whether continued scaling will eventually reach a tipping point that triggers stronger emergent capabilities (though we note some early signs discussed in Sec. 5.4), we concur with the broader community that data scaling alone is unlikely to achieve human-level spatial intelligence [67 ]. Motivated by this, we commit to fully open-sourcing the weights of SenseNova-SI, allowing the community to bypass the costly scaling stage and instead focus on advancing algorithmic inn”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0211

- Claim: 语言捷径与过拟合分析：MindCube 此前开源 SoTA 模型 MindCube-RawQA-SFT 在完全无图像输入时得 50.7 分——与有完整视觉输入时的表现几乎相同，暴露其对语言先验而非视觉推理的严重依赖；相比之下 SenseNova-SI 从 85.6 降至 52.5（无视觉设定），验证其真正使用视觉信息而非依赖语言捷径。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 9, Section 5.5 Overfit and Shortcut Analysis
- Evidence: 前任空间 SoTA 无图像仍得 50.7（语言先验）；SenseNova 85.6→52.5 证明真实视觉依赖——空间基准分数需去偏口径采信
- Quote: “the previous open-source SoTA on MindCube, MindCube-RawQA-SFT [70 ] achieves a score of 50.7 without any images, which is almost identical to its performance with full visual inputs, revealing a heavy dependence on language priors rather than visual reasoning. In contrast, SenseNova-SI drops from 85.6 to 52.5 in the no-vision setting, validating that it genuinely uses visual information rather than relying on language shortcuts.”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0212

- Claim: 空间链式思考的负结果：作者发现精心设计的 CoT 只能带来适度收益，纯文本推理可能既不是空间智能最有效也不是最高效的范式——尽管测试了三种文本 CoT 范式（GPT-5 标注、MindCube JSON 认知地图、自家长程序认知地图）与 GRPO 强化学习，所有变体收益有限、RL 无明确增益，结论指向'或需超越常规 CoT 的范式转变'。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 10, Section 5.6 Spatial Chain-of-Thought
- Evidence: 三种文本 CoT（含认知地图范式）+GRPO 均无法可靠超越 QA 数据缩放；'纯文本推理不是空间智能有效范式'
- Quote: “Our findings suggest that while carefully engineered CoT can offer modest benefits, text-based reasoning alone may be neither the most efficient nor the most effective paradigm for spatial intelligence. Hence, multimodal RL for spatial reasoning remains largely underexplored, consistent with observations in SpatialReasoner [40]. This may signal the need for a broader paradigm shift beyond conventional CoT.”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0213

- Claim: 下游具身操作验证（EmbodiedBench 空间子集，零微调）：SenseNova-SI-InternVL3-8B 在官方提示（OP）与空间智能提示（SIP）两种设定下相对基础模型分别提升 59.6%（10.4→16.6）与 60.0%（20.8→33.3），作者称增强的空间智能直接有益于具身操作；但绝对成功率仍远低于 GPT-4o（37.5/45.8）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 10, Section 5.7 Downstream Task
- Evidence: 零微调迁移具身操作相对 +60%（16.6/33.3 vs 10.4/20.8），但绝对值远低于 GPT-4o（37.5/45.8）——条件性弱证据
- Quote: “Across both OP and SIP, SenseNova-SI delivers substantial improvements, demonstrating that enhanced spatial intelli- gence directly benefits embodied manipulation: SenseNova- SI more reliably identifies key spatial cues, enabling more accurate reasoning and more consistent action planning.”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0094

- Claim: WorldMAP 教师管线把世界模型生成的未来视频转化为结构化轨迹监督的方式，是显式重建经典几何建图-规划链：接地的多视角证据被投影到共享导航平面并累积为 BEV 代价图（障碍格封锁、未观测区域保守视为不可通行、近障碍加代价），再由 Fast Marching Method 在 BEV 代价图上规划最小代价路径、平滑重采样为 waypoint 序列形成教师轨迹；作者明确定位：显式规划不是最终导航策略，而是把接地场景结构转化为结构化轨迹监督的机制。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.07957](https://arxiv.org/abs/2604.07957) WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models
- Locator: page 5, Section III-B.3（FMM planning）
- Evidence: 教师管线内部显式重建 BEV 代价图 + FMM 规划——世界模型替代观测来源而非建图/规划基础设施
- Quote: “Given the start position and the grounded target region, we run the Fast Marching Method (FMM) [35], [36] on the BEV cost map to obtain a minimum-cost path from start to goal. The raw grid path is then smoothed and resampled into a sparse waypoint sequence. These BEV waypoints are finally mapped back onto the navigation plane to form the teacher trajectory. In this way, explicit planning serves not as the final navigation policy, but as the mechanism that converts grounded scene structure into s”
- Authors: hongjin-chen; shangyun-jiang; tonghua-su; et al.

### EA-SLAMCORE-2026-0096

- Claim: WorldMAP 评测所用的 Target-Bench 以四足机器人 SLAM 估计的 3D 轨迹作为每个样本的真值，预处理把该机器人轨迹投影到真实首帧图像得到 2D 像素空间真值用于最终评测——该'无图导航/世界模型'路线的评测闭环建立在 SLAM 采集的轨迹数据与投影对齐之上。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.07957](https://arxiv.org/abs/2604.07957) WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models
- Locator: page 5, IV-A Experimental Setup
- Evidence: Target-Bench 真值是四足机器人 SLAM 估计轨迹——'无图'路线的评测闭环依赖 SLAM 基础设施
- Quote: “a natural-language navigation instruction, and a SLAM-estimated 3D trajectory of a quadruped robot.”
- Authors: hongjin-chen; shangyun-jiang; tonghua-su; et al.

### EA-SLAMCORE-2026-0152

- Claim: FOV 新颖性稀疏记忆实验（仅当新观测与已存观测的视场重叠低于阈值才写入记忆缓冲）减少了 token 消耗并提升导航性能（Table 3：+2.3 SR 至 17.0）；但作者同时指出：带专用记忆架构的 agent 系统在长期记忆管理上仍比当前 LMM 方法更有效，这是 LMM 与模块化具身 agent 之间的重要差距。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.07973](https://arxiv.org/abs/2604.07973) How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace
- Locator: page 14, Appendix D.4；page 7, Table 3
- Evidence: FOV 稀疏记忆 +2.3 SR（四方向最小增益）；带专用记忆架构的 agent 在长期记忆管理上仍更有效
- Quote: “Nonetheless, agent-based systems with dedicated memory architectures remain more effec- tive at long-term memory management, highlighting an important gap between current LMM-based approaches and modular embod- ied agents.”
- Authors: baining-zhao; ziyou-wang; jianjie-fang; et al.

### EA-SLAMCORE-2026-0108

- Claim: 综述的 Pareto 分析按基准显式分离：真实世界 EuRoC 上经典稀疏 ORB-SLAM3 取得最佳 ATE（3.5 cm @ 55 MB 地图），Basalt 以精度换更小地图（35 MB）；合成 Replica 上 3DGS 系统占优（ATE ≤ 0.58 cm、90–254 MB 地图，SplaTAM 最佳 0.36 cm）。作者强调两基准数值不可直接比较，跨范式结论只能依据 α 与 scaling 行为。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.16482](https://arxiv.org/abs/2604.16482) A Survey of Spatial Memory Representations for Efficient Robot Navigation
- Locator: page 6, Section 4.3 + Fig. 3
- Evidence: 分基准 Pareto：EuRoC 上 ORB-SLAM3 最佳（3.5 cm @ 55 MB），Replica 上 3DGS 最佳（0.36 cm）——无单一范式占优且跨基准不可比
- Quote: “On EuRoC (Fig. 3, left), ORB-SLAM3 achieves the best ATE (3.5 cm) at 55 MB; Basalt trades accuracy for a smaller map (35 MB).”
- Authors: ma-madecheen-s-pangaliman; steven-s-sison; erwin-p-quilloy; et al.

### EA-SLAMCORE-2026-0121

- Claim: VANDERER 的探索评测指标依赖仿真器的全局真值俯视地图（按 16m² 网格离散化计算覆盖面积）——'无图'方法的性能度量本身需要外部建图基础设施，该度量在真实部署中不可得
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.14879](https://arxiv.org/abs/2606.14879) VANDERER: Map-Free Exploration using Future-Aware and Visual-Curiosity-Guided Diffusion Policy
- Locator: page 5
- Evidence: Sec IV-A Evaluation Metric 原文：'we discretize the top-down maps of each town into a grid of 16m2 cells. Total coverage is calculated by summing the area of all unique cells visited'。评测管线的地图来自仿真器，非 agent 自建；论文全程无真机实验。
- Quote: “we discretize the top-down maps of each town into a grid of 16m 2 cells. Total coverage is calculated by summing the area of all unique cells visited over a fixed number of simulation steps.”
- Authors: venkata-naren-devarakonda; raktim-gautam-goswami; prashanth-krishnamurthy; et al.

### EA-SLAMCORE-2026-0122

- Claim: 视觉新颖性代理几何覆盖是显式假设：作者明示'在视觉差异充分的环境中，最大化视觉新颖性能有效最大化环境覆盖'——该代理在弱纹理或视觉重复环境中预期失效，且论文未测试此类场景
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.14879](https://arxiv.org/abs/2606.14879) VANDERER: Map-Free Exploration using Future-Aware and Visual-Curiosity-Guided Diffusion Policy
- Locator: page 4
- Evidence: Sec III-A 原文使用 'we hypothesize that...' 措辞；摘要进一步宣称视觉-几何好奇心直接相关，但正文无专门相关性实验。实验环境为视觉特征多样的 CARLA 城镇，全部在假设成立域内。
- Quote: “we hypoth- esize that in environments with sufficient visual variance, maximizing visual novelty effectively maximizes environ- mental coverage.”
- Authors: venkata-naren-devarakonda; raktim-gautam-goswami; prashanth-krishnamurthy; et al.

### EA-SLAMCORE-2026-0172

- Claim: WAM-Nav 的空间状态全部来自动作积分航位推算：部署时当前平面位姿由上一时刻位姿加已执行动作更新（Algorithm 1：s_t←s_{t−1}+a_{t−1}）并进入长度 k 的滑窗缓冲；缓冲在当前自我中心系中重表达（重定中心、旋转平移、包裹航向差），策略接收的是相对运动序列而非绝对场景坐标——系统不含全局定位、外部位姿输入或漂移校正。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04907](https://arxiv.org/abs/2606.04907) WAM-Nav: Asymmetric Latent World-Action Modeling for Unified Visual Navigation
- Locator: page 13, Sec C.1 Trajectory-Aware Motion History
- Evidence: 位姿由执行动作积分得到（无全局定位/漂移校正），空间状态=滑窗相对运动+视觉特征
- Quote: “At deployment, each executed action a t−1 updates the current planar pose s t , which is appended to a length-k sliding buffer and zero-padded at the front when the episode is shorter than k steps. The buffer is then re-expressed in the current egocentric frame—re-centering on s t , rotating translations by θ t , and wrapping heading differences—so that the stream receives a complete relative-motion sequence ˜ S t = {(∆x i , ∆y i , ∆θ i )} t i=t−k+1 rather than absolute scene coordinates.”
- Authors: ning-yang; yan-huang; kaiwen-peng; et al.

### EA-SLAMCORE-2026-0173

- Claim: 非对称视距消融（Table 7，Image-Goal，固定 H_act=24）：短视距潜在前瞻 H_vis=1 时性能最优（50.2/48.2），视觉前瞻视距增大单调退化——H_vis=4 为 46.2/43.8、H_vis=8 为 39.6/37.3、H_vis=24 为 30.4/28.1；作者结论：导航中视觉前瞻应提供可靠的近未来几何约束，而非在大自我中心视点变化下误差累积的长自回归视觉展开。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04907](https://arxiv.org/abs/2606.04907) WAM-Nav: Asymmetric Latent World-Action Modeling for Unified Visual Navigation
- Locator: page 16, Table 7 与 Sec F.3
- Evidence: 世界模型有效前瞻仅 1 步：H_vis 从 1 增至 24，SR 从 50.2 单调跌至 30.4
- Quote: “The best performance is obtained with short-horizon visual foresight (H vis = 1), while longer visual horizons progressively degrade performance. This supports our core design motiva- tion: in navigation, visual foresight should provide reliable near-future geometric constraints rather than long autoregressive visual rollouts, which are more prone to error accumulation under large egocentric viewpoint changes.”
- Authors: ning-yang; yan-huang; kaiwen-peng; et al.

### EA-SLAMCORE-2026-0177

- Claim: FutureNav 的空间信息来源是一个冻结的 VGGT 空间编码器：相同观测帧经空间编码器预处理管线输入冻结的 VGGT [62]，输出空间感知 token 特征，经轻量可训练 Merger（两层 MLP）投影进 VLM 隐空间并与视觉 token 残差融合（α=0.2）；空间编码器在训练中从不更新——几何感知特征来自前馈几何基础模型，而非在线 SLAM 建图与优化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30367](https://arxiv.org/abs/2606.30367) FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation
- Locator: page 5, Sec 3.2 Input Encoding（Spatial Encoder）
- Evidence: 空间特征来自冻结 VGGT 前馈几何基础模型（训练中不更新），非在线 SLAM
- Quote: “the same observation frames are loaded with the spatial-encoder prepro- cessing pipeline and passed through a frozen spatial encoder, implemented with VGGT [62]. The spa- tial encoder is never updated during training.”
- Authors: lingfeng-zhang; zeying-gong; xiaoshuai-hao; et al.

### EA-SLAMCORE-2026-0178

- Claim: 潜表征消融（Table 3，R2R-CE val-unseen，0K 设置）：以 VGGT 空间潜特征为世界建模监督目标最优——55.1 SR/50.1 SPL/NE 5.13，高于 DINO 语义潜特征（51.8/47.1/5.34）、VLM visual 潜特征（51.4/46.8）、VAE 潜特征（51.0/46.4）与无潜建模基线（50.1/45.1/6.00）；作者结论：显式建模空间感知潜状态对未来世界建模有益。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30367](https://arxiv.org/abs/2606.30367) FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation
- Locator: page 8, Sec 4.3 Ablation Studies（Table 3）
- Evidence: VGGT 空间潜特征作世界建模目标最优：55.1 SR vs DINO 语义 51.8、无潜建模 50.1
- Quote: “Our proposed spatial latent representation performs best, reaching 55.1 SR and 50.1 SPL with the lowest NE of 5.13, demonstrat- ing the benefit of explicitly modeling spatial-aware latent states for future world modeling.”
- Authors: lingfeng-zhang; zeying-gong; xiaoshuai-hao; et al.

### EA-SLAMCORE-2026-0179

- Claim: 世界建模仅作为训练期辅助监督：默认推理设置只用动作策略分支直接解码动作，动力学与未来预测模块可按需启用（显式世界状态估计或前瞻推理时），因此世界建模不引入任何额外推理开销——运行时既无显式地图/定位/里程计模块，也无活跃的世界模型模块，空间能力被蒸馏进策略权重与冻结 VGGT 特征。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30367](https://arxiv.org/abs/2606.30367) FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation
- Locator: page 6, Sec 3.4 Training Objective 末段
- Evidence: 世界建模为训练期辅助监督，推理仅走策略分支，无任何运行时空间状态模块
- Quote: “In our main setting, inference uses only the action policy branch for direct action decoding, so world modeling introduces no additional inference cost.”
- Authors: lingfeng-zhang; zeying-gong; xiaoshuai-hao; et al.

### EA-SLAMCORE-2026-0164

- Claim: 白皮书把基于神经表征（NeRF 系，如 NeRFPrior）与显式 3D 高斯表征（3DGS 系，如 ObjectGS）的重建方法定位为具身系统的互补性高保真 3D 场景表征，可支撑交互空间分析、视点选择与长期场景记忆；另指出 VGGT/DUSt3R/MASt3R 等前馈多视角重建方法降低了对传统 SfM/MVS 管线（复杂特征匹配、相机标定、迭代优化）的依赖。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.03283](https://arxiv.org/abs/2607.03283) Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied Intelligence Systems
- Locator: page 8, Section 4.3
- Evidence: 神经表征/3DGS 重建作为长期场景记忆的互补路线；前馈几何降低对 SfM/MVS 优化管线依赖
- Quote: “For embodied intelligence systems, these methods can serve as complementary high- fidelity 3D scene representations, supporting interaction space analysis, viewpoint selection, and long-term scene memory.”
- Authors: junwu-xiong; jiaxuan-gao; wei-chai; et al.

### EA-SLAMCORE-2026-0066

- Claim: 在 RoboTwin 2.0 增量消融（统一 80K steps、batch 32 后训练预算）中，为 vanilla PaliGemma+action expert（Easy 35.4%/Hard 33.4%）加入非机器人 3D grounding 预训练数据后，成功率提升至 Easy 70.2%/Hard 69.1%（+34.6/+35.7 个百分点）；作者据此判断 3D 空间任务预训练建立了比 VQA 主导预训练更稳健的几何基础。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.19710](https://arxiv.org/abs/2602.19710) PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Policies
- Locator: page 8, Table V
- Evidence: 非机器人 3D 数据预训练带来 +34.6/+35.7 pp 成功率提升（Table V）
- Quote: “As shown in the incremental analysis (Table V), incorporating diverse non-robotic 3D grounding data to the vanilla PaliGemma baseline yields a substantial +35.7% boost in success rate. This confirms that pre-training on 3D spatial tasks establishes a more robust geometric foundation than conventional VQA-dominated pre-training.”
- Authors: haitao-lin; hanyang-yu; jingshun-huang; et al.

### EA-SLAMCORE-2026-0069

- Claim: 坐标系选择的消融结果混合：把动作预测从相机中心系改为机器人基座系，在视觉/几何扰动大的 RoboTwin-Hard 设定中成功率下降 2.4 个百分点（79.1→76.7，数值见 page 8 Table V 末行），作者归因于相机中心表征面对显著视觉变化时更鲁棒；但同一消融的 Easy 设定中基座系反而上升 0.5 个百分点（79.9→80.4，Table V），相机系优势仅在 Hard 设定成立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.19710](https://arxiv.org/abs/2602.19710) PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Policies
- Locator: page 9, Section IV-D（数值表见 page 8, Table V 末行）
- Evidence: 相机系 vs 基座系消融混合：Hard −2.4 pp 相机系更稳，Easy +0.5 pp 基座系反超
- Quote: “Conversely, we observe that predicting actions in the base frame leads to a performance drop (−2.4%) in RoboTwin- Hard scenarios. This indicates that camera-centric representa- tions provide more robustness when facing significant visual variations in downstream policy transfer.”
- Authors: haitao-lin; hanyang-yu; jingshun-huang; et al.

### EA-SLAMCORE-2026-0072

- Claim: 正交数据混合消融（统一 80K steps、batch 32）显示：仅用机器人轨迹预训练 Easy 71.3%/Hard 68.3%，低于仅用非机器人 3D 数据的 77.2%/76.2% 与完整混合的 79.9%/79.1%——作者判断通用 3D 视觉数据（而非机器人数据）是该框架空间能力的关键驱动，并以此论证对昂贵机器人示教依赖的缓解。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.19710](https://arxiv.org/abs/2602.19710) PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Policies
- Locator: page 9, Table VI
- Evidence: 3D-only 预训练（77.2/76.2）优于 robotic-only（71.3/68.3），通用 3D 数据是关键驱动
- Quote: “Crucially, pre-training on robot data only severely degrades results, proving that generic 3D vision data is the key driver of our framework’s spatial capabilities. Conversely, relying solely on non-robotic 3D data (3D data only) maintains highly competitive performance.”
- Authors: haitao-lin; hanyang-yu; jingshun-huang; et al.

### EA-SLAMCORE-2026-0156

- Claim: 论文提出的缓解方案 CAG 是纯推理时双分支方案（条件 VLA 与语言无关 Vision-Action 先验按引导尺度混合动作，等效于锐化语言似然），不需要额外示教、不改架构与预训练权重：摘要报告在 LIBERO-CF 上使 π0.5 语言跟随准确率提升 9.7%（training-free）或 15.5%（配 VA 模型）、欠观测任务成功率提升 3.6%/8.5%；真实世界平均减少反事实失败 9.4%、提升任务成功率 17.2%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.17659](https://arxiv.org/abs/2602.17659) When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs
- Locator: page 1, Abstract
- Evidence: CAG 推理时双分支修复：语言跟随 +9.7%/+15.5%、真机 success +17.2%，全程无几何/SLAM 模块
- Quote: “For example, on LIBERO-CF, CAG improves π 0.5 by 9.7% in language following accuracy and 3.6% in task success on under- observed tasks using a training-free strategy, with further gains of 15.5% and 8.5%, respectively, when paired with a VA model. In real-world evaluations, CAG reduces counterfactual failures of 9.4% and improves task success by 17.2% on average.”
- Authors: yu-fang; yuchun-feng; dong-jing; et al.

### EA-SLAMCORE-2026-0023

- Claim: 尽管 PanoNav（SR 43.5 / SPL 23.7）的 SR 超过若干 map-based 方法（ESC 39.2、VoroNav 42.0），但仍低于表中所有 RGB-D 输入的 open-set 方法：map-based 的 VLFM（52.2 / 30.4）、L3MVN（50.4 / 23.1）与 mapless 的 ImagineNav（53.0 / 23.8），SR 差距 6.9–9.5 个百分点；SPL 低于 VLFM 6.7 个百分点（略高于 L3MVN 的 23.1）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.06840](https://arxiv.org/abs/2511.06840) PanoNav: Mapless Zero-Shot Object Navigation with Panoramic Scene Parsing and Dynamic Memory
- Locator: page 5, Table 1
- Evidence: PanoNav SR 43.5 仍低于 RGB-D 方法 VLFM 52.2、L3MVN 50.4、ImagineNav 53.0（差 6.9–9.5 个百分点）
- Quote: “VLFM RGB-D, GPS+Compass Open-Set map-based 52.2 30.4 ESC RGB-D, GPS+Compass Open-Set map-based 39.2 22.3 VoroNav RGB-D, GPS+Compass Open-Set map-based 42.0 26.0 L3MVN RGB-D, GPS+Compass Open-Set map-based 50.4 23.1 ImagineNav RGB-D Open-Set mapless 53.0 23.8 ZSON RGB Only Open-Set mapless 25.5 12.6 PixNav RGB Only Open-Set mapless 37.9 20.5 PanoNav (Ours) RGB Only Open-Set mapless 43.5 23.7”
- Authors: qunchao-jin; yilin-wu; changhao-chen

### EA-SLAMCORE-2026-0165

- Claim: 作者主张：现有记忆型零样本导航方法依赖稠密 RGB-D 重建，这类重建构建昂贵且在记忆构建完成后对轻微场景重排或动态变化脆弱；并以人类导航为据，主张稀疏视觉记忆（少量标志性快照）即可提供粗粒度而可靠的全局引导。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.22609](https://arxiv.org/abs/2511.22609) MG-Nav: Dual-Scale Visual Navigation via Sparse Spatial Memory
- Locator: page 2, Sec 1 Introduction
- Evidence: 作者定性主张：稠密 RGB-D 重建昂贵且对重排脆弱，稀疏视觉记忆足以提供全局引导
- Quote: “Memory-based zero-shot approaches construct persis- tent global maps [9, 12, 24] or scene graphs [36] to enable long-horizon planning without retraining. However, these methods typically rely on dense RGB-D reconstructions, which are expensive to build and brittle to even mild rear- rangements or dynamic changes after memory construction.”
- Authors: bo-wang; jiehong-lin; chenzhi-liu; et al.

### EA-SLAMCORE-2026-0166

- Claim: 在 HM3D InstanceImageNav 上，MG-Nav 以仅 RGB 输入的稀疏记忆图（SMG）取得 SR 78.5/SPL 59.3，超过全部稠密 RGBD 地图方法——GaussNav（3DGS Map）72.5/57.8、BSC-Nav（Scene Map）71.4/57.2、IEVE 70.2/25.2；在 MP3D ImageNav 上取得 SR 83.77/SPL 57.15，超过最强 RL 基线 FGPrompt-EF 77.71/51.09。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.22609](https://arxiv.org/abs/2511.22609) MG-Nav: Dual-Scale Visual Navigation via Sparse Spatial Memory
- Locator: page 6, Table 1 与 Table 2
- Evidence: RGB-only 稀疏记忆图在 HM3D/MP3D 两个基准上全面超过稠密 RGBD 地图方法
- Quote: “BSC-Nav [24] Scene Map (RGBD) 71.4 57.2 GaussNav [13] 3DGS Map (RGBD) 72.5 57.8 MG-Nav(Ours) SMG (RGB) 78.5 59.3”
- Authors: bo-wang; jiehong-lin; chenzhi-liu; et al.

### EA-SLAMCORE-2026-0167

- Claim: 在动态障碍测试（HM3D 100 episodes，导航阶段插入 0/5/10 个随机障碍物）中，地图类方法性能骤降（BSC-Nav SR 25.49→7.84，UniGoal 56.43→44.21），而 MG-Nav 仅小幅下降（SR 73.53→68.63，SPL 56.28→50.15）；作者归因于解耦的双尺度设计：稀疏 SMG 维持区域级全局规划稳定，零样本局部策略在不依赖全局地图的情况下避开未建模障碍。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.22609](https://arxiv.org/abs/2511.22609) MG-Nav: Dual-Scale Visual Navigation via Sparse Spatial Memory
- Locator: page 8, Table 4 与 Sec 4.4 归因段
- Evidence: 动态障碍下地图类方法 SR 骤降，MG-Nav 仅微降；局部避障由基础策略承担、不依赖全局地图
- Quote: “Obs. Num 0 5 10 Method SR SPL SR SPL SR SPL BSC-Nav [24] 25.49 19.91 8.64 4.63 7.84 4.94 UniGoal [36] 56.43 20.44 52.94 19.68 44.21 17.17 Ours 73.53 56.28 72.55 52.20 68.63 50.15 → 50.15). This resilience stems from a decoupled dual- scale design. The sparse SMG delivers robust region-level global planning, keeping the navigational goal stable, while the zero-shot local policy handles unmodeled obstacles and avoids them without relying on the global map, resulting in only minor drops in SR and S”
- Authors: bo-wang; jiehong-lin; chenzhi-liu; et al.

### EA-SLAMCORE-2026-0052

- Claim: 综述归纳语言智能体四类空间失效并给出转引数字：空间幻觉——GPT-4V 在 SpatialBench 空间关系问题上失败率 40%（转引 Chen et al. 2024a）；参考系混淆——VLN 智能体 15–20% 错误率来自自/他参考系错位（转引 Anderson et al. 2018c）；尺度不敏感——SayCan 供给模型在物体尺度偏离训练时失效；时间漂移——VLMaps 100+ 步无地图更新后语义漂移（转引 Huang et al. 2023a）。作者归因：语言-only 智能体缺乏接地的空间表示，每类失效可追溯到特定表示缺口。
- Stance: `limit` | Confidence: `citation-supported`
- Paper: [2602.01644](https://arxiv.org/abs/2602.01644) From Perception to Action: Spatial AI Agents and World Models
- Locator: page 7, Section 5.1 Spatial Failure Modes
- Evidence: GPT-4V 空间关系题 40% 失败、VLN 15–20% 参考系错误、VLMaps 100+ 步语义漂移——基础模型缺度量空间接地（转引数字）
- Quote: “Integration with SLAM [Sucar et al., 2021, Zhu et al., 2022, Keetha et al., 2024, Bird et al., 2025, Teed and Deng, 2021, Teed et al., 2024, Mur-Artal and Tard´os, 2017, Campos et al., 2021] enables online reconstruction.”
- Authors: gloria-felicia; nolan-bryant; handi-putra; et al.

### EA-SLAMCORE-2026-0054

- Claim: 综述三大发现之一是'世界模型对安全部署 essential'（作者综合，见摘要与结论），但作者在 7.2 节给出明确限定：LLM 世界模型虽能建模抽象状态转移，'currently lack the fine-grained physical fidelity of dedicated world models'，对需要精确几何与物理推理的任务是关键限制；作者并指出 LLM 世界模型仅在需要抽象高层预测的中观/宏观尺度上足够有效；Table 2 中世界模型代表 DreamerV3 的主要失效模式被标注为 model compounding error。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.01644](https://arxiv.org/abs/2602.01644) From Perception to Action: Spatial AI Agents and World Models
- Locator: page 14, Section 7.2 World Models
- Evidence: 世界模型 = 规划组件而非记忆替代：LLM 世界模型缺细粒度物理保真、DreamerV3 有 model compounding error、仅中观/宏观抽象预测足够——'essential'须与限定条款同读
- Quote: “Neural approaches to spatial memory include Neural SLAM [Chaplot et al., 2020c,d,b, 2021], semantic maps [Huang et al., 2023a, Henriques and Vedaldi, 2018, Shah et al., 2023b,a, Huang et al., 2023c, Chen et al., 2023a], and scene graphs [Armeni et al., 2019, Rosinol et al., 2020, Hughes et al., 2022, Gu et al., 2024, Wu et al., 2021, Wald et al., 2020, Kim et al., 2019].”
- Authors: gloria-felicia; nolan-bryant; handi-putra; et al.

### EA-SLAMCORE-2026-0222

- Claim: 外化差距（externalization gap）：模型被要求先生成认知地图再作答时性能轻微退化——潜在内部空间信念比其外化的离散 JSON 输出更丰富或更准确，显式地图是内部状态的有损压缩但仍是强诊断信号。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.07055](https://arxiv.org/abs/2602.07055) Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?
- Locator: page 12, Section 5.1 Cognitive Map Validation & Correlation 末段
- Evidence: 外化差距：隐含内部空间信念比外化 JSON 更丰富准确——探测分数可能低估模型隐式空间知识
- Quote: “These results reveal an externalization gap: the model’s latent internal spatial belief is richer or more accurate than the discretized JSON output it produces. While it is a lossy compression of the agent’s true internal state, the explicit map remains a strong diagnostic signal.”
- Authors: pingyue-zhang; zihan-huang; yue-wang; et al.

### EA-SLAMCORE-2026-0016

- Claim: 作者主张：FALCON 用空间基础模型从纯 RGB 输入提供强几何先验（作为 VLA 的空间 grounding 来源），Embodied Spatial Model 在深度或相机位姿可用时可选融合以获得更高保真度，且无需重训或改架构；空间 token 由 Spatial-Enhanced Action Head 消费而非拼进视觉-语言主干，以保留语言推理。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.17439](https://arxiv.org/abs/2510.17439) From Spatial to Actions: Grounding Vision-Language-Action Model in Spatial Foundation Priors
- Locator: page 1, Abstract
- Evidence: FALCON 核心主张：空间基础模型从 RGB 提供几何先验，深度/位姿为可选融合条件
- Quote: “FALCON leverages spatial foundation models to deliver strong geometric priors from RGB alone, and includes an Embodied Spatial Model that can optionally fuse depth, or pose for higher fidelity when available, without retraining or architectural changes. To preserve language reasoning, spatial tokens are consumed by a Spatial-Enhanced Action Head rather than being concatenated into the vision-language backbone.”
- Authors: zhengshen-zhang; hao-li; yalun-dai; et al.

### EA-SLAMCORE-2026-0017

- Claim: 作者给出避开显式 3D 输入管线的结构性理由：获取高质量 3D 输入需要昂贵且难以部署的专用传感器，且许多大规模操作数据集（如 Open X-Embodiment）缺乏对齐的 3D 标注、限制可扩展性——因此依赖显式 3D 输入的方法绑定特定模态、在该输入不可用时失效。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.17439](https://arxiv.org/abs/2510.17439) From Spatial to Actions: Grounding Vision-Language-Action Model in Spatial Foundation Priors
- Locator: page 2, Section 1 Introduction
- Evidence: 动机：专用传感器昂贵+OXE 缺 3D 标注，显式 3D 输入路线不可扩展
- Quote: “This stems from two fundamental issues. First, acquiring high-quality 3D inputs requires specialized sensors that are expensive and difficult to deploy in practice. Second, many large-scale manipulation datasets (e.g., Open X-Embodiment dataset [ 29]) lack aligned 3D annotations, limiting scalability.”
- Authors: zhengshen-zhang; hao-li; yalun-dai; et al.

### EA-SLAMCORE-2026-0018

- Claim: 论文相关工作把 DUSt3R 家族定位为传统 SfM 方法的替代：深度学习引入了 SfM 的新替代方案，DUSt3R 不依赖几何约束或归纳偏置、从图像对直接预测点云，代表对'依赖关键点匹配与几何优化的传统 SfM 管线'的重大偏离，在共享坐标系中生成预测从而对初始化敏感性与稀疏对应等经典问题更鲁棒；MASt3R/CUT3R/VGGT 在此范式上继续发展。
- Stance: `limit` | Confidence: `citation-supported`
- Paper: [2510.17439](https://arxiv.org/abs/2510.17439) From Spatial to Actions: Grounding Vision-Language-Action Model in Spatial Foundation Priors
- Locator: page 3, Section 2.2 Spatial Foundation Models
- Evidence: 相关工作：DUSt3R 家族被定位为 traditional SfM 的学习式替代（免关键点匹配/几何优化）
- Quote: “Recent advancements in deep learning have introduced novel alternatives to traditional SfM methods. DUSt3R [ 42] represents a significant deviation from conventional SfM pipelines by predicting point clouds from image pairs without relying on geometric constraints or inductive biases. Unlike traditional SfM, which depends on keypoint matching and geometric optimization, DUSt3R generates predictions in a shared coordinate frame, enabling robust reconstruction across diverse scenes.”
- Authors: zhengshen-zhang; hao-li; yalun-dai; et al.

### EA-SLAMCORE-2026-0019

- Claim: CALVIN 零样本 ABC→D 设定上，FALCON 超过依赖真值点云的先前方法 3DDP 与 3D Diffuser Actor，Avg. Len. 分别提升 4.13 与 1.05（Table 1 中 FALCON 4.40，3DDP 0.27、3D Diffuser Actor 3.35）；作者以此作为隐式（前馈）空间信息整合策略有效性的证据。注意该比较为跨方法整体比较（骨干/数据不同），非受控消融。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.17439](https://arxiv.org/abs/2510.17439) From Spatial to Actions: Grounding Vision-Language-Action Model in Spatial Foundation Priors
- Locator: page 8, Section 4.1；page 7, Table 1
- Evidence: CALVIN 零样本 ABC→D：RGB 前馈空间先验超过真值点云方法（+4.13/+1.05 Avg. Len.）
- Quote: “Notably, in the challenging zero-shot ABC→D setting, FALCON surpasses previous methods that rely on ground-truth point clouds (e.g., 3DDP [45 ] and 3D Diffuser Actor [13]), improving the Avg. Len. by 4.13 and 1.05, respectively. This provides clear evidence of the effectiveness of our implicit spatial information integration strategy.”
- Authors: zhengshen-zhang; hao-li; yalun-dai; et al.

### EA-SLAMCORE-2026-0083

- Claim: 在 Video2Mental 基准的心理导航设定（模型从长自我中心视频自建认知图并规划路径）下，11 个前沿 MLLM（含 GPT-5.1、Claude-Sonnet-4.6、Gemini-3-Pro、Qwen3.5-397B 与空间专用 Cambrian-S/RynnBrain-8B）平均目标成功率 SR_t 仅 5.54%、执行验证路径成功率 SR_p 仅 3.76%，预测认知图 Landmark-Mean IoU 低于 5%、Landmark-F1 低于 35%——心理导航能力不能从标准视觉-语言预训练中自然涌现
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.21577](https://arxiv.org/abs/2603.21577) Mind over Space: Can Multimodal Large Language Models Mentally Navigate?
- Locator: page 6
- Evidence: Sec 4.1（page 6）：平均 SR_t/SR_p 5.54%/3.76%；认知图诊断 IoU<5%、F1<35%；作者归因于缺乏长程空间整合的推理中心数据与端到端范式把空间记忆与动作规划不透明地纠缠。Table 1（page 5）逐模型数值。
- Quote: “As shown in Tab. 1, the average SR t and SR p remain as low as 5.54% and 3.76%, respectively.”
- Authors: qihui-zhu; shouwei-ruan; xiao-yang; et al.

### EA-SLAMCORE-2026-0084

- Claim: 给定真值认知图（oracle 设定）后前沿 MLLM 仍严重失败：oracle 地图仅使平均 SR_t/SR_p 提升 12.6/8.1 个百分点，论文报告即便有真值图平均成功率也只勉强达到 11.8%、导航误差持续 5.29m——作者结论：准确的空间表示是必要但非充分条件，瓶颈根植于结构化空间推理机制的缺失
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.21577](https://arxiv.org/abs/2603.21577) Mind over Space: Can Multimodal Large Language Models Mentally Navigate?
- Locator: page 6
- Evidence: Sec 4.2（page 6）：MN(w/ GT-Map) 设定下 oracle 地图带来 12.6%/8.1% 提升（remarkably limited）；'Even with ground- truth maps, the average SR t barely reaches 11.8%, with a persistent N E of 5.29m'（注：11.8% 与 Table 2 基线平均 SR_p 数值吻合，正文标签疑为笔误，已在 reader_inferred 记录）；'accurate spatial representation is a necessary but insufficient condition' 在同页。
- Quote: “While the oracle map boosts global planning performance: increasing average SR t and SR p by 12.6% and 8.1%, which is remarkably limited. Even with ground- truth maps, the average SR t barely reaches 11.8%, with a persistent N E of 5.29m.”
- Authors: qihui-zhu; shouwei-ruan; xiao-yang; et al.

### EA-SLAMCORE-2026-0206

- Claim: 作者立场：为保持与现有研究管线的兼容，刻意不改动基础模型的原始架构，转而采用数据中心（data-centric）路线，把数据缩放与训练策略作为空间理解能力的主要驱动因素——空间智能的获得被定位为数据问题而非架构/显式几何模块问题。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 2, Section 1 Introduction 第4段
- Evidence: 数据中心路线：刻意不改架构、不用 3D 专家，数据缩放是空间能力的主要驱动因素
- Quote: “To preserve compatibility with existing research pipelines, we deliberately avoid altering the original architectures of the base models. Instead, we adopt a data-centric approach, emphasizing the role of data scaling and training strategies as the primary drivers of spatial understanding capability.”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0207

- Claim: 主结果分析：SenseNova-SI 以明显优势超过所有开源通用模型、甚至超过 GPT-5 等强专有模型；并全面超过所有专用空间智能模型——作者据此提出'在大规模空间数据红利尚未充分实现之前，算法创新本身可能为时过早'，并以 2B 参数模型在可比数据预算下超过 VST-7B 与 Cambrian-S-7B 等强基线。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.13719](https://arxiv.org/abs/2511.13719) Scaling Spatial Intelligence with Multimodal Foundation Models
- Locator: page 7, Section 5.2 Main Results
- Evidence: 数据缩放全面胜过专用空间模型（含 VGGT 3D 专家路线）；作者称算法创新'为时过早'、2B 模型胜 7B 基线
- Quote: “(1) SenseNova-SI outperforms all general open-source models by clear margins, and even surpasses strong proprietary ones such as GPT-5 [42], revealing persistent knowledge gaps in existing foundation models. (2) SenseNova-SI also achieves superior performance over all dedicated spatial-intelligence models, suggesting that algorithmic innovation alone may be premature when the benefits of large-scale spatial data have not yet been fully realized.”
- Authors: zhongang-cai; ruisi-wang; chenyang-gu; et al.

### EA-SLAMCORE-2026-0042

- Claim: 在含未知格子的路径规划设定（部分可观测）下，GPT-5 取得 93% 高成功率，但失败案例暴露模型缺乏导航所必需的结构性空间理解；且更新模型并不总是比前代更可靠
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.05529](https://arxiv.org/abs/2601.05529) Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models
- Locator: page 1
- Evidence: 摘要（page 1）：GPT-5 未知格路径规划 93%；失败案例显示缺乏导航必需的结构性空间理解；新模型不总比前代可靠（疏散设定 Gemini-2.5 Flash 67% 低于 Gemini-2.0 Flash 100%）。
- Quote: “In a path-planning setting with unknown cells, GPT-5 achieved a high success rate of 93%; Yet, the failed cases exhibit fun- damental limitations of the models, e.g., the lack of structural spatial understanding essential for navigation.”
- Authors: jua-han; jaeyoon-seo; jungbin-min; et al.

### EA-SLAMCORE-2026-0043

- Claim: 在完全信息 ASCII 地图任务上，Gemini-2.0 Flash 与 GPT-4o 的成功率随地图复杂度增加从 100%/80%（easy）骤降至 0%（normal 与 hard），呈突变式崩塌而非渐进退化，路径频繁中途终止、无法维持拓扑连续性
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.05529](https://arxiv.org/abs/2601.05529) Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models
- Locator: page 4
- Evidence: Sec 完全信息结果（page 4）：Gemini-2.0 Flash 与 GPT-4o 的崩塌；Table 1 逐格数值；对照 GPT-5 全难度 100%。
- Quote: “Their success rates dropped sharply from 100% and 80% on the Easy map to 0% on both the Normal and Hard maps (Table 1, Map- Based Task–Complete), revealing an abrupt collapse rather than a gradual degradation.”
- Authors: jua-han; jaeyoon-seo; jungbin-min; et al.

### EA-SLAMCORE-2026-0044

- Claim: GPT-5 在未知格 Map 2 的失败中有 7%（两次）涉及被显式禁止的对角移动——高准确率并不意味着安全；此类约束违反在真实机器人设定中可能导致不安全或物理不可行的行为
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.05529](https://arxiv.org/abs/2601.05529) Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models
- Locator: page 5
- Evidence: Sec 未知格结果（page 5）：两次 Map 2 失败（7%）涉及对角移动；作者明示 high accuracy does not imply safety。
- Quote: “Although two Map 2 failures (7%) in- volved diagonal movement, an explicitly prohibited action, these violations highlight a critical insight: high accuracy does not imply safety.”
- Authors: jua-han; jaeyoon-seo; jungbin-min; et al.

### EA-SLAMCORE-2026-0045

- Claim: 自我中心序列推理中，模型表现出强烈的『右』回答偏置（无论实际转向方向），转向推断准确率多在 40–60%；缺帧选择准确率在多数情况下接近随机，并伴随捏造不存在选项等幻觉——模型未能真正接地观测到的轨迹
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.05529](https://arxiv.org/abs/2601.05529) Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models
- Locator: page 5
- Evidence: Sec 自我中心序列结果（page 5）：右偏置与 40–60% 准确率；缺帧选择接近随机（同页 Missing-frame selection results 段）；Table 2（page 6）逐模型数值，GPT-5 最高 64%/92%。
- Quote: “We observed a strong bias toward answering “right.” Regardless of the actual turn- ing direction, models frequently responded with “right,” re- sulting in accuracy rates mostly around 40–60%.”
- Authors: jua-han; jaeyoon-seo; jungbin-min; et al.

### EA-SLAMCORE-2026-0046

- Claim: 安全相关推理（hard 紧急疏散）中，Gemini-2.5 Flash 在 32% 的试验中把用户导向教授办公室（优先取回文件而非逃生）、1% 指向提示中从未提及的机房；其 hard 疏散表现比 Gemini-2.0 Flash 差 40%（Table 1：67% vs 100%）——新模型并不必然更安全
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.05529](https://arxiv.org/abs/2601.05529) Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models
- Locator: page 6
- Evidence: Sec 安全相关结果（page 6）：32% 办公室、1% 机房（幻觉高风险区域）；『Newer is not always safer』段：比 Gemini-2.0 Flash 差 40%；Table 1（page 4）hard 疏散 67% vs 100%；Fig 5 响应分布。
- Quote: “Gemini-2.5 Flash directed users toward the professor’s of- fice, where the prompt mentioned important personal mate- rials, in 32% of trials, prioritizing document retrieval over evacuation.”
- Authors: jua-han; jaeyoon-seo; jungbin-min; et al.

### EA-SLAMCORE-2026-0047

- Claim: 在真实建筑图像的 back-of-the-building 任务中，GPT-4o、Claude Opus 4.1、Claude Sonnet 4 无法在视觉场景与生成地图之间建立稳定空间对应：多数产出部分合理的布局，但无法一致识别正确朝向、保持建筑结构完整性或维持可行轨迹——第一人称视角到俯视布局的转换系统性失败
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.05529](https://arxiv.org/abs/2601.05529) Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models
- Locator: page 7
- Evidence: 补充实验结果（page 7）：三种提示策略下均不稳定；Fig 6 四类失败（结构崩塌/方向错误/约束违反/航点错误）；任务要求推断机器人位置并把第一人称视角转换为俯视布局。
- Quote: “The tested models showed limited ability to estab- lish stable spatial correspondences between the visual scene and the generated map.”
- Authors: jua-han; jaeyoon-seo; jungbin-min; et al.

### EA-SLAMCORE-2026-0095

- Claim: 在同一评测协议下，世界模型增强的测试时推理系统 MindJourney（o-series 推理模型 + SVC，按原文最佳配置）在 Target-Bench 全部三个指标上均差于其直接预测基线 o3（ADE 152.41 vs 112.14、FDE 250.17 vs 177.27、DTW 84.84 vs 57.30）——测试时直接消费生成的想象视角并非自动有益；作者归因于语义上合理但跨视角几何不一致的生成视图会引入误导性证据。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.07957](https://arxiv.org/abs/2604.07957) WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models
- Locator: page 6, Table I
- Evidence: MindJourney（测试时世界模型推理）在全部三指标上差于直接 o3 基线——想象视角当证据用反而有害
- Quote: “Notably, the o3-based MindJourney model also underperforms the direct o3 baseline on all three metrics, indicating that additional imagined views are not automatically beneficial in this benchmark.”
- Authors: hongjin-chen; shangyun-jiang; tonghua-su; et al.

### EA-SLAMCORE-2026-0097

- Claim: 学生训练监督消融：仅用世界模型伪标签（usable/borderline 档）训练的学生 ADE 95.98 / FDE 141.10 / DTW 88.25，仅用基准真值（Train GT）训练为 78.34 / 121.75 / 75.09，两者结合（Train GT + 伪标签 usable 档）达到最优 42.06 / 38.87 / 31.95——世界模型生成的监督单独不足以支撑训练（甚至差于仅用真实真值），其价值只在与真实轨迹数据结合时显现。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.07957](https://arxiv.org/abs/2604.07957) WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models
- Locator: page 8, Table III
- Evidence: 监督消融：WM 伪标签 alone ADE 95.98 差于 GT alone 78.34，结合才最优 42.06——世界模型监督不能独立支撑训练
- Quote: “WM pseudo-labels only (usable / borderline) 95.98 141.10 88.25 Train GT only 78.34 121.75 75.09 Train GT + WM pseudo-labels (usable / borderline) 42.85 40.97 31.78 Train GT + WM pseudo-labels (usable) 42.06 38.87 31.95”
- Authors: hongjin-chen; shangyun-jiang; tonghua-su; et al.

### EA-SLAMCORE-2026-0105

- Claim: 综述作者在 NVIDIA A100 上的独立剖析显示：仅神经 SLAM 方法内部，运行时开销因子 α（峰值运行内存与持久地图检查点大小之比）就跨越两个数量级——从 Point-SLAM 的 2.3 到 NICE-SLAM 的 215（47 MB 保存地图在运行时需要 10 GB GPU 内存）；作者据此指出决定部署可行性的是内存架构而非范式标签。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.16482](https://arxiv.org/abs/2604.16482) A Survey of Spatial Memory Representations for Efficient Robot Navigation
- Locator: page 1, Abstract
- Evidence: 神经 SLAM 内部 α 跨两个数量级（2.3→215；NICE-SLAM 47 MB 地图需 10 GB 运行时）——地图大小误导部署成本
- Quote: “Independent profiling on an NVIDIA A100 GPU reveals that α spans two orders of magnitude within neural methods alone, ranging from 2.3 (Point-SLAM) to 215 (NICE-SLAM, whose 47 MB map requires 10 GB at runtime), showing that memory architecture, not paradigm label, determines deployment feasibility.”
- Authors: ma-madecheen-s-pangaliman; steven-s-sison; erwin-p-quilloy; et al.

### EA-SLAMCORE-2026-0107

- Claim: 综述以 SplaTAM 为例论证神经空间记忆在具身平台上部署不可行：α_GPU=55 的 SplaTAM 运行时消耗 14 GB，在 16 GB 嵌入式 GPU 上仅剩 <2 GB 给感知、规划与操作系统，尽管其地图只有 254 MB——内存效率是可行性约束而非成本问题；外推到 100 m² 公寓地图约需 ∼200 GB，甚至超过数据中心级 A100（80 GB）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.16482](https://arxiv.org/abs/2604.16482) A Survey of Spatial Memory Representations for Efficient Robot Navigation
- Locator: page 2, Section 1 Introduction
- Evidence: SplaTAM 运行 14 GB、16 GB 嵌入式平台仅剩 <2 GB——神经空间记忆在具身平台上不可部署（内存=可行性约束）
- Quote: “SplaTAM (α GPU = 55) consuming 14 GB at runtime leaves <2 GB for perception, planning, and the OS, making the system infeasible despite the map being only 254 MB.”
- Authors: ma-madecheen-s-pangaliman; steven-s-sison; erwin-p-quilloy; et al.

### EA-SLAMCORE-2026-0034

- Claim: 在从生成视频恢复相机轨迹的 world-decoder 对比中，基于 SLAM 的视觉惯性管线 ViPE 表现最弱（真值视频 WO 仅 0.291），显著低于前馈式 VGGT（0.862）与 SpaTracker（0.623）——增量式 SLAM 估计在含幻觉/生成伪影的视频上比前馈几何基础模型更脆弱
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.17792](https://arxiv.org/abs/2511.17792) Target-Bench: Can Video World Models Achieve Mapless Path Planning with Semantic Targets?
- Locator: page 13
- Evidence: Table 5 与 Fig. 8 的三 decoder 对比：VGGT 在真值视频上 0.862（最佳）、SpaTracker 0.623、ViPE 0.291（最弱）；所有 12 个世界模型变体上 ViPE 的 WO 都低于 VGGT（如 Wan2.2-Flash：VGGT 0.341 vs ViPE 0.260）。ViPE 是融合视觉+IMU、带闭环的增量式度量管线，而 VGGT/SpaTracker 是前馈多视角重建。
- Quote: “VGGT achieves the best weighted overall score of 0.862 with the ground truth videos. SpaTracker shows lower performance, while ViPE produces the weakest results.”
- Authors: dingrui-wang; zhihao-liang; hongyuan-ye; et al.

### EA-SLAMCORE-2026-0120

- Claim: VANDERER 证明仅用单目 RGB（无占用地图、无 LiDAR/IMU/GPS、无显式定位）的探索可行且优于最强 RGB 基线：在 CARLA 五镇上较 NoMaD 平均多探索 13.4% 面积
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.14879](https://arxiv.org/abs/2606.14879) VANDERER: Map-Free Exploration using Future-Aware and Visual-Curiosity-Guided Diffusion Policy
- Locator: page 1
- Evidence: 摘要与 Table I：VANDERER 五镇 Area/APL 全面领先 NoMaD（13.4% 面积增益），且策略失败率 0.046% 远低于 NoMaD 0.278%。方法全程不构建占用地图，新颖性由预测末状态与历史观测数据库的匹配距离度量。
- Quote: “Evaluated across diverse simulated environments, VANDERER consistently outperforms established baselines, exploring an average of 13.4% more area than NoMaD [1].”
- Authors: venkata-naren-devarakonda; raktim-gautam-goswami; prashanth-krishnamurthy; et al.

### EA-SLAMCORE-2026-0170

- Claim: 作者对导航领域范式演变的定性判断：过去几年主导性导航范式已从传统解耦的建图-规划管线（其引用 [6, 7, 8] 分别为 ORB-SLAM3、RTAB-Map、Active Neural SLAM）逐渐转向基于学习的方法，端到端反应式方法直接把视觉观测映射为可执行动作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04907](https://arxiv.org/abs/2606.04907) WAM-Nav: Asymmetric Latent World-Action Modeling for Unified Visual Navigation
- Locator: page 1, Sec 1 Introduction
- Evidence: 作者宣称导航范式已从 SLAM 式解耦建图-规划管线（ORB-SLAM3/RTAB-Map/Active Neural SLAM）转向学习方法
- Quote: “Over the past few years, the dominant navigation paradigm has gradually transitioned from traditional de- coupled mapping-and-planning pipelines [6, 7, 8] to learning-based intelligent methods.”
- Authors: ning-yang; yan-huang; kaiwen-peng; et al.

### EA-SLAMCORE-2026-0171

- Claim: 零样本仿真评测（IsaacSim，ClutterScenes+InternScenes，6000 episodes）中，完全 mapless 的潜在世界-动作模型 WAM-Nav 在三任务上取得最优平均性能：Image-Goal 50.2% SR/48.2% SPL、Point-Goal 80.4% SR/78.0% SPL、No-Goal 探索面积 171.1 m²；相对最强基线 NavDP（Image-Goal 43.4/41.4、Point-Goal 77.8/74.8，Table 3），Image-Goal SR 相对提升 15.7%。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04907](https://arxiv.org/abs/2606.04907) WAM-Nav: Asymmetric Latent World-Action Modeling for Unified Visual Navigation
- Locator: page 7, Sec 4.1 Result Analysis (Q1)
- Evidence: 无地图世界-动作模型零样本三任务平均最优：Image-Goal 50.2/48.2、Point-Goal 80.4/78.0
- Quote: “For Q1, Table 3 (full results in Appendix F.1) summarizes the zero-shot evalua- tion results across Image-Goal, Point-Goal, and No-Goal exploration. WAM-Nav achieves the best average performance across the three task settings, reaching 50.2% SR / 48.2% SPL on Image-Goal, 80.4% SR / 78.0% SPL on Point-Goal, and 171.1 m 2 explored area in No-Goal exploration.”
- Authors: ning-yang; yan-huang; kaiwen-peng; et al.

### EA-SLAMCORE-2026-0174

- Claim: 真机零样本部署：WAM-Nav 在 Unitree G1 人形机器人（Intel RealSense D455 相机）上跨 4 个室内外环境（会议室/仓库/大厅/停车场，每环境 10 trials）实现平均 85% 任务成功率；部署为全机载（附录 G：RTX 4060 机载 1 Hz 推理，MPC 50 Hz 跟踪），全程无任何建图、定位或 SLAM 模块。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04907](https://arxiv.org/abs/2606.04907) WAM-Nav: Asymmetric Latent World-Action Modeling for Unified Visual Navigation
- Locator: page 8, Sec 4.2 Deployment on Real World
- Evidence: G1 人形真机零部署平均 85% 成功率，全机载且无任何建图/定位/SLAM 模块
- Quote: “For Q5, we deploy WAM-Nav in a zero-shot manner on a real-world Unitree G1 humanoid robot equipped with an Intel RealSense D455 camera. Evaluation is conducted across four indoor and outdoor environments: a meeting room, warehouse, lobby, and parking lot, with 10 trials per scene. As shown in Fig. 4(a), WAM-Nav consistently predicts feasible trajectories under diverse layouts and lighting conditions, achieving an average 85% success rate.”
- Authors: ning-yang; yan-huang; kaiwen-peng; et al.

### EA-SLAMCORE-2026-0175

- Claim: 作者对 VLN-CE 方法演进的定性叙述：早期连续环境 VLN 系统依赖显式导航结构——路标点预测、拓扑规划、语义地图与学习型空间记忆——来连接语言接地与可执行动作，并主张成功的具身导航需要理解周围世界状态及其在动作下的演化；同期 VLM 路线中 JanusVLN 以双隐式记忆分离语义与空间信息。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30367](https://arxiv.org/abs/2606.30367) FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation
- Locator: page 1, Sec 1 Introduction
- Evidence: 作者把路标点/拓扑规划/语义地图/空间记忆定位为早期 VLN-CE 手段，叙事转向 VLM 与世界状态建模
- Quote: “Early VLN-CE systems therefore relied on explicit navigation structures, such as waypoint pre- diction, topological planning, semantic maps, and learned spatial memories, to connect language ground- ing with physically executable actions [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]. These methods indicate that successful embodied navigation requires more than recognizing objects or instruction phrases: an agent must also understand the state of the surrounding world and”
- Authors: lingfeng-zhang; zeying-gong; xiaoshuai-hao; et al.

### EA-SLAMCORE-2026-0176

- Claim: 作者对当前 VLN 基础模型的批评性判断：NaVid/Uni-NaVid/NaVILA/StreamVLN 等方法提供了可扩展的动作解码接口，但大多仍把导航表述为直接的观测到动作生成，未显式监督世界状态表征、动作引起的状态转移或动作选择前的未来状态预测——即端到端 VLM 范式本身不含任何显式空间状态模块；本文的补足方案是潜空间世界-动作目标，而非恢复显式地图。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30367](https://arxiv.org/abs/2606.30367) FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation
- Locator: page 2, Sec 1 Introduction
- Evidence: VLM 导航方法被定性为纯观测到动作生成、无世界状态监督；补足方案是潜空间世界-动作目标而非地图
- Quote: “a scalable action-decoding interface for VLN, but most of them still formulate navigation primarily as direct observation-to-action generation. Conse- quently, they do not explicitly supervise world-state representation, action-induced state transition model- ing, or future-state prediction before action selection.”
- Authors: lingfeng-zhang; zeying-gong; xiaoshuai-hao; et al.

### EA-SLAMCORE-2026-0180

- Claim: 真机零样本部署链路：推理在 H20 GPU 服务器进行，遥控 Go2 四足机器人搭载 D435i 相机采集自我中心 RGB 观测流上传服务器，服务器从语言指令与接收的 RGB 历史预测低层动作，由 Go2 在物理环境执行；真机评测为零样本设置、无任何真机微调，且部署链路中无建图、定位或里程计模块。论文真机证据为定性展示（Figure 6 室内外三例成功轨迹），未报告真机成功率数字。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30367](https://arxiv.org/abs/2606.30367) FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation
- Locator: page 6, Sec 4.1 Real-world Deployment
- Evidence: Go2+D435i 单 RGB 流零样本真机 VLN 可行，部署链路无任何建图/定位/里程计模块（仅定性展示）
- Quote: “we deploy FutureNav on an H20 GPU server for infer- ence and use a remotely operated Go2 robot as the physical navigation platform. The robot is equipped with a D435i camera, which captures egocentric RGB observations and streams them to the inference server. At each navigation step, the server predicts a low- level action from the language instruction and the received RGB history, and the Go2 robot executes the returned action in the physical environment. We evaluate real-world navigation in a”
- Authors: lingfeng-zhang; zeying-gong; xiaoshuai-hao; et al.

### EA-SLAMCORE-2026-0181

- Claim: 主结果（Table 1，R2R-CE/RxR-CE val-unseen）：0K 设置下 FutureNav-4B 达 55.1 SR/50.1 SPL（R2R-CE）与 54.5 SR/46.0 SPL（RxR-CE），比同设置 JanusVLN†（52.8/49.2；51.4/44.3）高 4.4% R2R SR 与 6.0% RxR SR；全量数据下 FutureNav-4B 达 65.4 SR/61.3 SPL（R2R-CE）与 60.9 SR/52.8 SPL（RxR-CE），相对 JanusVLN（60.5/56.8；56.2/47.5）提升 11.3% NE/8.1% SR/7.9% SPL。Table 1 标注 FutureNav 仅用单一 RGB 传感器，而表中显式地图时代方法（Ego2-Map、GridMM、DreamWalker、MapNav 等）均需全景+里程计+深度输入且 R2R SR 最高仅 49.0。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30367](https://arxiv.org/abs/2606.30367) FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation
- Locator: page 7, Table 1 与 Sec 4.2 Main Results 首段
- Evidence: 单 RGB 4B 模型在 R2R-CE/RxR-CE 全面超过显式地图时代方法（SR≤49.0）与 7B/8B VLN 模型
- Quote: “FutureNav-4B † improves over JanusVLN † by 4.4% in R2R SR and 6.0% in RxR SR”
- Authors: lingfeng-zhang; zeying-gong; xiaoshuai-hao; et al.

### EA-SLAMCORE-2026-0162

- Claim: 作者主张的'更可辩护'部署架构是分层的：低频层（VLM、VLA、Gemini Robotics-ER、GR00T）执行语言 grounding、场景推理与任务分解；中频层（分割、深度、6D 位姿、扩散策略）支撑跟踪、位姿估计与子动作生成；高频层（MoveIt、Nav2、MPC、安全控制器）执行轨迹、避障、力控、平衡与急停；在该设计中 VLA 主要充当任务决策算子，而确定性规划器与控制器强制执行碰撞检查、运动约束、速度与力矩限制及安全关断。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.03283](https://arxiv.org/abs/2607.03283) Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied Intelligence Systems
- Locator: page 21, Section 8.6.3
- Evidence: 分层架构主张：VLA 限定为低频任务决策层，中频几何+高频确定性控制（MoveIt/Nav2/MPC）保留独立层
- Quote: “A more defensible architecture is hierarchical. A low-frequency layer, such as VLM, VLA, Gemini Robotics-ER, or GR00T, performs language grounding, scene reasoning, and task decomposition [2, 5, 75]. A mid-frequency layer, including segmentation, depth, 6D pose, and diffusion policy, supports tracking, pose estimation, and sub- action generation [26, 31, 87].”
- Authors: junwu-xiong; jiaxuan-gao; wei-chai; et al.

### EA-SLAMCORE-2026-0067

- Claim: 位姿预测在 Pose-VLA 中严格只是预训练阶段学习空间表征的辅助代理任务；推理时 action expert 将隐式特征端到端直接映射为连续动作，显式位姿估计或相机轨迹估计的额外开销为零。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.19710](https://arxiv.org/abs/2602.19710) PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Policies
- Locator: page 5, Section III-E Remark on Inference
- Evidence: 位姿仅是预训练代理任务，推理时零显式位姿/相机轨迹估计开销
- Quote: “At inference time, the action expert maps implicit features directly to continuous actions end-to-end, introducing zero overhead for explicit pose or camera trajectory estimation.”
- Authors: haitao-lin; hanyang-yu; jingshun-huang; et al.

### EA-SLAMCORE-2026-0056

- Claim: 综述把'统一空间表示'列为六大挑战之首并描述当前实践：不同尺度使用互不兼容的表示——点云用于抓取、拓扑地图用于导航（引 Thrun 1998、Kuipers & Byun 1991、Kuipers 2000、Konolige et al. 2008）、栅格影像用于地理空间分析；'统一表示将使跨尺度无缝推理成为可能'仍是愿景，研究方向包括跨物体部件到城市基础设施的层级场景图、多尺度查询的神经隐式表示与 3D 基础模型。
- Stance: `gap` | Confidence: `direct`
- Paper: [2602.01644](https://arxiv.org/abs/2602.01644) From Perception to Action: Spatial AI Agents and World Models
- Locator: page 21, Section 10.1 Grand Challenge 1
- Evidence: 统一跨尺度表示是 grand challenge 而非现实：当前实践仍是分尺度显式表示（导航=拓扑地图、抓取=点云、地理=栅格影像）
- Quote: “topological maps for navigation [Thrun, 1998, Kuipers and Byun, 1991, Kuipers, 2000, Konolige et al., 2008], and raster imagery for geospatial analysis [Goodfellow et al., 2016, LeCun et al., 2015]. A unified representation would enable seamless reasoning across scales.”
- Authors: gloria-felicia; nolan-bryant; handi-putra; et al.

### EA-SLAMCORE-2026-0147

- Claim: 在该城市空中目标导向导航基准上，17 个代表性模型（非推理 LMM、推理 LMM、agent 方法、VLA）的平均成功率为 4.2%–34.0%，远低于 92.0% 的人类水平；被测模型中最高者 GPT-5.1 平均 34.0%（Table 2，短程组 52.9%），作者结论为 LMM 呈现涌现的动作能力但离人类级空间行动仍很远。
- Stance: `gap` | Confidence: `direct`
- Paper: [2604.07973](https://arxiv.org/abs/2604.07973) How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace
- Locator: page 8, Section 7 Conclusion；page 5, Table 2
- Evidence: 17 模型平均 SR 4.2%–34.0% vs 人类 92.0%：端到端模型空间行动能力缺口巨大
- Quote: “We evaluate 17 representative models on this benchmark, achieving success rates of 4.2%–34.0%, far below the 92.0% human level.”
- Authors: baining-zhao; ziyou-wang; jianjie-fang; et al.

### EA-SLAMCORE-2026-0148

- Claim: 同一基准上，专为导航数据对齐动作语义的 VLA 模型（OpenFly 平均 SR 1.0%、Uni-NaVid 3.2%）表现劣于随机基线（平均 2.4%）与动作采样（2.5%）；作者归因于 VLA 对样本内数据过拟合、泛化能力甚至低于其原始骨干 VLM，而基于人类先验、用深度信息评估位置与距离的 agent 方法（SayNav/STMR/PRPSearcher，平均 18.0-21.2%）仍是高效稳定的方案。
- Stance: `gap` | Confidence: `direct`
- Paper: [2604.07973](https://arxiv.org/abs/2604.07973) How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace
- Locator: page 5, Table 2；page 6, Section 5.2
- Evidence: VLA 模型劣于随机基线（1.0/3.2 vs 2.4），agent 方法（RGB+深度位置距离评估）更稳
- Quote: “Action-as-Token: VLA Models OpenFly ✓ 3.0 3.0 63.3 0 0 114.1 0 0 258.7 1.0 1.0 146.5 Uni-NaVid ✓ 6.1 5.2 80.9 3.4 3.0 118.5 0 0 262.0 3.2 2.7 154.9”
- Authors: baining-zhao; ziyou-wang; jianjie-fang; et al.

### EA-SLAMCORE-2026-0103

- Claim: 综述范围声明：本文聚焦视觉空间记忆的表示层，明确排除完整自主系统栈、'无持久记忆的感知'以及 LiDAR 建图（BioSLAM 除外）；其语料为 1989–2025 年筛选出的 88 篇参考文献、约 52 个系统，全部是引入或评测持久空间记忆表示的系统。
- Stance: `gap` | Confidence: `direct`
- Paper: [2604.16482](https://arxiv.org/abs/2604.16482) A Survey of Spatial Memory Representations for Efficient Robot Navigation
- Locator: page 3, Section 2 Scope and Methodology
- Evidence: 综述显式排除无持久记忆的端到端感知与完整自主栈——'替代 SLAM'的对立路线不在其证据基础内
- Quote: “We exclude full autonomy stacks, perception without persistent memory, and LiDAR-based mapping (except BioSLAM [78]).”
- Authors: ma-madecheen-s-pangaliman; steven-s-sison; erwin-p-quilloy; et al.

### EA-SLAMCORE-2026-0070

- Claim: 作者将'从静态桌面设定过渡到移动与 egocentric 操作'明确列为未来工作——本文全部验证（RoboTwin 2.0、LIBERO、真实 4 任务）都在静态桌面操作设定内完成，移动操作、大范围空间一致性与动态环境未被触及。
- Stance: `gap` | Confidence: `direct`
- Paper: [2602.19710](https://arxiv.org/abs/2602.19710) PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Policies
- Locator: page 9, Section V Limitations and Future Work
- Evidence: 移动与 egocentric 操作被明确列为未来工作，桌面域结论不可外推
- Quote: “transitioning from static tabletop setups to mobile and egocentric manipulation presents an exciting frontier for future work”
- Authors: haitao-lin; hanyang-yu; jingshun-huang; et al.

### EA-SLAMCORE-2026-0153

- Claim: LIBERO 官方微调权重上的模态消融显示：OpenVLA-OFT、π0、π0.5 三个 SOTA VLA 在仅视觉输入时平均成功率仍达 69.1%/18.5%/51.7%，仅语言输入时全部崩溃至 0.9%/0.6%/0.0%（视觉+语言时为 97.1%/94.2%/96.9%）——动作预测主要由视觉先验驱动，语言在当前 VLA 中只是调制视觉驱动策略的次级条件信号。
- Stance: `gap` | Confidence: `direct`
- Paper: [2602.17659](https://arxiv.org/abs/2602.17659) When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs
- Locator: page 4, Table I 与正文
- Evidence: 模态消融：vision-only 平均成功率 18.5%-69.1% 而 language-only 崩溃至 0.0%-0.9%，语言只是次级条件信号
- Quote: “All evaluated VLAs preserve high performance even when only vision is provided, while performance collapses to near zero when only language is given. This indicates that VLAs primarily rely on visual cues for action prediction.”
- Authors: yu-fang; yuchun-feng; dong-jing; et al.

### EA-SLAMCORE-2026-0154

- Claim: LIBERO-CF 反事实基准上全部评测 VLA 严重失败：OpenVLA-OFT 平均 grounding 率仅 4.7%、成功率 0.4%；表现最好的 π0.5 也仅 30.8% grounding、13.2% 成功率——而同一模型在原训练任务上的偏置执行率高达 83.6%/78.6%（OpenVLA-OFT）与 65.6%/60.9%（π0.5），SOTA VLA 在反事实指令下几乎完全无法跟随语言，默认执行场景中训练过的任务。
- Stance: `gap` | Confidence: `direct`
- Paper: [2602.17659](https://arxiv.org/abs/2602.17659) When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs
- Locator: page 6, Section VI-B 与 Table III
- Evidence: LIBERO-CF：SOTA VLA 反事实指令 Faithful 成功率 0.4%-13.2% vs Biased 偏置执行 60.9%-78.6%
- Quote: “OpenVLA- OFT exhibits the most severe vision shortcuts, achieving only a 4.7% grounding rate and 0.4% success rate. Even π 0.5 , which reaches the best overall performance among the baselines, achieves only a 30.8% grounding rate and 13.2% success rate.”
- Authors: yu-fang; yuchun-feng; dong-jing; et al.

### EA-SLAMCORE-2026-0155

- Claim: 真实世界空间推理设定（三个相同物体放在不同位置、仅靠空间语言区分目标：Middle/Left/Right 与 Table/Plate/Bowl）中，π0.5 在欠观测空间目标上的 grounding 率仅 20%（Left）、30%（Right）、60%（Plate）、40%（Bowl）；作者结论：VLA 在空间差异化任务上尤其容易陷入视觉捷径，经常选错物体实例；CAG 将该维度的 grounding 改善 16.6%、任务成功改善 13.3%。
- Stance: `gap` | Confidence: `direct`
- Paper: [2602.17659](https://arxiv.org/abs/2602.17659) When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs
- Locator: page 8, Section VII-C Results（Spatial Reasoning）
- Evidence: 真机空间语言区分：π0.5 欠观测空间目标 grounding 仅 20%-60%，VLA 在空间差异化任务上尤其易陷入视觉捷径
- Quote: “However, π 0.5 achieves only 20% and 30% grounding rates on under-observed targets (i.e., left, right) in Middle/Left/Right, and 60% for Plate and 40% for Bowl in Table/Plate/Bowl. These results show that VLAs are particularly prone to vision shortcuts in spatially differentiated tasks, often failing to select the correct object instance.”
- Authors: yu-fang; yuchun-feng; dong-jing; et al.

### EA-SLAMCORE-2026-0157

- Claim: 作者把反事实失败的根因归于数据采集方式与模态失衡：在固定场景下，示教往往只为少数任务子集采集，促使 VLA 依赖视觉捷径而非忠实 grounding 语言——即当前具身操作数据集'任务子集化+语言多样性远低于视觉/动作模态'的结构性偏差是端到端路线失败行为的源头。
- Stance: `gap` | Confidence: `direct`
- Paper: [2602.17659](https://arxiv.org/abs/2602.17659) When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs
- Locator: page 2, Section I Introduction
- Evidence: 根因诊断：固定场景下示教只覆盖小任务子集，数据偏差催生视觉捷径（采集环节缺口在数据多样性，非几何）
- Quote: “Under a fixed scene, demon- strations are often collected for only a small subset of tasks, encouraging VLAs to rely on vision shortcuts rather than faithfully grounding language.”
- Authors: yu-fang; yuchun-feng; dong-jing; et al.

### EA-SLAMCORE-2026-0195

- Claim: 作者主张：前向神经网络点图回归（DUSt3R/MASt3R/VGGT 类基础模型）能直接从图像恢复高保真 3D 场景几何、以学习到的空间先验克服传统多视几何的局限，但这类流水线往往丢弃了概率多传感器信息融合已被广泛验证的优势；为此提出 MASt3R-Fusion，把前向点图回归与 IMU、GNSS 等互补传感器信息紧耦合进多传感器辅助视觉 SLAM 框架。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.20757](https://arxiv.org/abs/2509.20757) MASt3R-Fusion: Integrating Feed-Forward Visual Model with IMU, GNSS for High-Functionality SLAM
- Locator: page 1, Abstract
- Evidence: 前向点图回归基础模型丢弃多传感器融合优势；本文将其与 IMU/GNSS 紧耦合回 SLAM 框架
- Quote: “Recent advancements in feed-forward neural network- based pointmap regression have demonstrated the potential to recover high-fidelity 3D scene geometry directly from images, leveraging learned spatial priors to overcome limitations of tra- ditional multi-view geometry methods. However, the widely vali- dated advantages of probabilistic multi-sensor information fusion are often discarded in these pipelines. In this work, we propose MASt3R-Fusion, a multi-sensor-assisted visual SLAM framework tha”
- Authors: yuxuan-zhou; xingxing-li; shengyu-li; et al.

### EA-SLAMCORE-2026-0196

- Claim: KITTI-360 公里级序列（单目相机+IMU）：MASt3R-Fusion 的相对平移误差低于传统间接/直接 VIO 与学习型 VIO——平均 RTE 比 DM-VIO 低 43.0%、比 DBA-Fusion 低 17.7%，且在弱激励序列（0003、0010）上仍稳定；而视觉-only 的 MASt3R-SLAM 在这种大尺度下几乎无法完成 SLAM，其尺度估计严重受损于点图回归的不完美信息，需靠惯性信息的引入来缓解并充分利用稠密视觉约束实现稳定度量尺度位姿估计。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.20757](https://arxiv.org/abs/2509.20757) MASt3R-Fusion: Integrating Feed-Forward Visual Model with IMU, GNSS for High-Functionality SLAM
- Locator: page 9, Section VI-A 分析段
- Evidence: 视觉-only MASt3R-SLAM 在公里级几乎失败；MASt3R-Fusion 平均 RTE 比 DM-VIO 低 43.0%、比 DBA-Fusion 低 17.7%
- Quote: “It can be seen that the proposed MASt3R-Fusion achieves accurate pose estimation, yielding lower relative translation errors (RTEs) compared with both traditional indirect/direct VIO methods and learning-based VIO approaches. The aver- age RTE is 43.0% lower than DM-VIO and 17.7% lower than DBA-Fusion, which shows stable performance even for weak- excitation sequences (e.g., 0003 and 0010). This improvement can be attributed to the powerful data association enabled by the feed-forward model, as”
- Authors: yuxuan-zhou; xingxing-li; shengyu-li; et al.

### EA-SLAMCORE-2026-0197

- Claim: KITTI-360 含回环全局 SLAM（单目 V-I 数据）：MASt3R-Fusion 的绝对平移误差为 0.70-4.56 m（按长度归一化平均 0.05%），显著低于 ORB-SLAM3（6.95-45.17 m，0.63%）与视觉-only 的 VGGT-Long（26.46-310.76 m，2.91%）；作者称仅用单目 V-I 数据达到 0.05% 的 ATE/长度令人印象深刻，部分归因于更高里程计精度、部分归因于更强更丰富的回环信息（大视角差异下的回环使对向行驶也能保持位姿一致性）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.20757](https://arxiv.org/abs/2509.20757) MASt3R-Fusion: Integrating Feed-Forward Visual Model with IMU, GNSS for High-Functionality SLAM
- Locator: page 11, Table II
- Evidence: 全局 SLAM ATE 归一化 0.05% vs ORB-SLAM3 0.63% vs VGGT-Long 2.91%（Table II）
- Quote: “TABLE II ABSOLUTE TRANSLATION ERRORS (M) OF DIFFERENT GLOBAL SLAM SCHEMES (WITH LOOP CLOSURE) ON KITTI-360 DATASET. Seq. VGGT -Long * ORB -SLAM3 MASt3R -Fusion Leng. (m) 0000 103.64 26.03 2.13 8361 0002 310.76 32.57 2.82 11195 0003 26.46 28.63 0.70 1368 0004 165.67 42.82 4.56 8614 0005 234.48 10.37 1.28 4561 0006 179.95 9.51 2.52 7699 0009 135.23 6.95 1.90 8677 0010 211.54 45.17 4.38 3340 ave(%) 2.91 0.63 0.05 norm. * Visual-only, scaled using Sim(3)-based global alignment [43].”
- Authors: yuxuan-zhou; xingxing-li; shengyu-li; et al.

### EA-SLAMCORE-2026-0198

- Claim: SubT-MRS 非常规场景（两条喀斯特洞穴手持序列 + 一条四足机器人室内外序列）的含回环全局 SLAM：MASt3R-Fusion 的 ATE 为 0.26/1.04/0.43 m（按长度归一化平均 0.13%），优于 ORB-SLAM3 的 1.48/2.14/1.07 m（0.37%）；视觉-only 的 VGGT-Long 在全部三条序列上失败（fail）。作者据此主张前向模型方法在与 IMU 结合时对开放场景的泛化能力得到很大验证。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.20757](https://arxiv.org/abs/2509.20757) MASt3R-Fusion: Integrating Feed-Forward Visual Model with IMU, GNSS for High-Functionality SLAM
- Locator: page 11, Table IV
- Evidence: SubT-MRS 全局 SLAM：M-Fus 0.13% vs ORB-SLAM3 0.37%，视觉-only VGGT-Long 全部失败（Table IV）
- Quote: “TABLE IV ABSOLUTE TRANSLATION ERRORS (M) OF DIFFERENT GLOBAL SLAM SCHEMES (WITH LOOP CLOSURE) ON SUBT-MRS DATASET. Seq. VGGT -Long * ORB -SLAM3 MASt3R -Fusion Leng. (m) handheld1 fail 1.48 0.26 394 handheld2 fail 2.14 1.04 395 overexporsure fail 1.07 0.43 509 ave(%) - 0.37 0.13 norm. * Visual-only.”
- Authors: yuxuan-zhou; xingxing-li; shengyu-li; et al.

### EA-SLAMCORE-2026-0199

- Claim: Wuhan 城市自采数据集（车载，GNSS RTK 集成）：MASt3R-Fusion 带回环的水平定位 RMSE 为 0.21 m（序列 a）/0.09 m（b），优于 GNSS RTK 本身（4.36/1.46 m）、VINS-Fusion（2.54/0.62 m）与 DBA-Fusion（0.78/0.24 m）；在模拟 GNSS 间歇中断（100 秒级）下，VINS-Fusion 为 2.84/9.66 m、DBA-Fusion 为 3.20/2.94 m，而 MASt3R-Fusion 带回环仍维持 0.37/0.46 m——作者称全局因子图在 100 秒 GNSS 中断下仍能实现大部分亚米级轨迹平滑，完整保留的 V-I 信息通过迭代优化有效抵抗 GNSS 粗差并保持分米级精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.20757](https://arxiv.org/abs/2509.20757) MASt3R-Fusion: Integrating Feed-Forward Visual Model with IMU, GNSS for High-Functionality SLAM
- Locator: page 13, Table VI
- Evidence: GNSS 中断 100 秒仍维持 0.37/0.46 m 定位；带回环 0.21/0.09 m 优于 RTK 与 VINS/DBA-Fusion（Table VI）
- Quote: “TABLE VI HORIZONTAL POSITION RMSES (M) OF DIFFERENT POSITIONING SCHEMES WITH GNSS RTK INTEGRATION OR WITH SIMULATED GNSS INTEGRATION. Mode Seq. GNSS RTK VINS Fusion DBA Fusion M-Fus. w/o loop M-Fus. w/ loop Real (a) 4.36 2.54 0.78 0.24 0.21 (b) 1.46 0.62 0.24 0.13 0.09 Simu. (a) - 2.84 3.20 0.69 0.37 (b) - 9.66 2.94 1.02 0.46”
- Authors: yuxuan-zhou; xingxing-li; shengyu-li; et al.

### EA-SLAMCORE-2026-0037

- Claim: 在 TUM-RGBD 与 EuRoC 轨迹基准上，FoundationSLAM（冻结深度基础模型先验 + 流式可微 BA）取得表内最优的平均 ATE RMSE（TUM 0.024、EuRoC 0.019），TUM 9 个序列中 7 个第一、反射/低纹理序列尤佳；TUM 上同时低于基础模型先验式的 MASt3R-SLAM（0.030）与 VGGT-SLAM*（0.053），EuRoC 上低于 DROID-SLAM（0.022）与 MASt3R-SLAM（0.041）。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.25008](https://arxiv.org/abs/2512.25008) FoundationSLAM: Unleashing the Power of Depth Foundation Models for End-to-End Dense Visual SLAM
- Locator: page 5, Tables 1-2
- Evidence: Table 1：TUM 平均 Ours 0.024 < MASt3R-SLAM 0.030 < GO-SLAM 0.035 < DROID-SLAM 0.038；Table 2：EuRoC 平均 Ours 0.019 < DROID 0.022 < MASt3R-SLAM 0.041；Table 3：ETH3D ATE 0.069/AUC 24.775 亦最优。
- Quote: “As shown in Tables 1 and 2, FoundationSLAM achieves state-of-the- art ATE RMSE across all datasets. On TUM-RGBD, it ranks first on 7 out of 9 sequences, with particularly strong per- formance in reflective or low-texture environments.”
- Authors: yuchen-wu; jiahe-li; fabio-tosi; et al.

### EA-SLAMCORE-2026-0039

- Claim: FoundationSLAM 在单张 RTX 4090 上于 EuRoC 达到 18 FPS 实时推理，速度介于 VGGT-SLAM（26）/DROID-SLAM（24）与 MASt3R-SLAM（10）之间，作者称其在性能与效率间取得平衡；该速度依赖测试时的效率设计（ViT-S 主干 + 基础编码半分辨率运行）。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.25008](https://arxiv.org/abs/2512.25008) FoundationSLAM: Unleashing the Power of Depth Foundation Models for End-to-End Dense Visual SLAM
- Locator: page 7, Table 5
- Evidence: Table 5：DROID-SLAM 24、MASt3R-SLAM 10、VGGT-SLAM 26、Ours 18（EuRoC、单 4090）；page 5 实现细节给出 ViT-S 与半分辨率基础编码的效率设计。
- Quote: “Our system achieves real-time inference at 18 FPS, striking a balance between performance and efficiency.”
- Authors: yuchen-wu; jiahe-li; fabio-tosi; et al.

### EA-SLAMCORE-2026-0040

- Claim: 作者在 related work 中对基础模型 SLAM 路线给出两类批评：MASt3R-SLAM/VGGT-SLAM 一系的几何先验按帧/按对预测，『前端先验未被后端优化显式精化或引导』，导致困难区域先验失准且缺乏联合优化修正机制；SLAM3R 则完全去后端、直接融合基础模型点云，『效率以鲁棒性与长期精度为代价』——本文因此主张把几何先验嵌入强制多视图一致的紧耦合优化框架。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2512.25008](https://arxiv.org/abs/2512.25008) FoundationSLAM: Unleashing the Power of Depth Foundation Models for End-to-End Dense Visual SLAM
- Locator: page 2, Related Work（SLAM from 3D Reconstruction Models 段）
- Evidence: page 2 相关工作两段：先验未被后端精化→困难区域失准（MASt3R-SLAM/VGGT-SLAM/VGGT）；SLAM3R 去后端→效率换鲁棒性与长期精度；随后一句 'This work aims to unify these strengths by embedding geometry-aware priors into a tightly integrated optimization framework...' 表明融合立场。
- Quote: “However, these systems typically predict geometry on a per-frame or per-pair basis, and the frontend priors are not explicitly refined or guided by the backend optimization. As a result, these systems often suffer from inaccurate priors in challenging regions and lack a mecha- nism to correct them through joint optimization. Other ap- proaches (e.g., SLAM3R (Liu et al. 2025)) discard back- end optimization entirely and directly fuse point clouds from foundation models, achieving efficiency but a”
- Authors: yuchen-wu; jiahe-li; fabio-tosi; et al.

### EA-SLAMCORE-2026-0041

- Claim: FoundationSLAM 把深度基础模型作为冻结先验嵌入 SLAM 前端：受 FoundationStereo（整合 Depth Anything V2 深度先验，即 Yang et al. 2025）启发设计双分支结构——冻结的 FoundationStereo FeatureNet 编码器提供『从多样真实世界图像学到的稳定几何特征』，配可训练的任务适配 CNN 分支做单目 SLAM 数据关联；另加冻结 ContextNet 提供几何上下文，这些预训练模块在训练期间保持固定。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.25008](https://arxiv.org/abs/2512.25008) FoundationSLAM: Unleashing the Power of Depth Foundation Models for End-to-End Dense Visual SLAM
- Locator: page 3, Section 3.1 Backbone Design
- Evidence: page 3 Backbone Design：Geometric Prior Branch（冻结 FeatureNet）+ Task-Specific Adaptation Branch（可训练 CNN）经 3×3 卷积与残差层融合为匹配描述子；冻结 ContextNet 提供上下文；'remain fixed during training'。这是系统设计陈述（非实验结果），其有效性由 C01/C02 的整体对比间接支撑。
- Quote: “Backbone Design. Inspired by FoundationStereo’s (Wen et al. 2025) effective integration of depth priors (Yang et al. 2025), we design a dual-branch architecture: (1) a Geomet- ric Prior Branch utilizing the frozen FeatureNet encoder from FoundationStereo to provide stable geometric features learned from diverse real-world imagery, and (2) a Task- Specific Adaptation Branch with trainable CNN layers mir- roring parts of FeatureNet, optimized for monocular SLAM data association challenges.”
- Authors: yuchen-wu; jiahe-li; fabio-tosi; et al.

### EA-SLAMCORE-2026-0191

- Claim: 作者主张：大多数现有语义 SLAM 依赖闭集语义标签或场景特定特征，这类表征限制了开放词汇推理并阻碍与 LLM 的直接交互；相比之下 VLM 提供连续、语言对齐且可泛化的嵌入，可作为语义 SLAM 向开放词汇语言推理演化的语义来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06991](https://arxiv.org/abs/2602.06991) LangGS-SLAM: Real-Time Language-Feature Gaussian Splatting SLAM
- Locator: page 1, Section 1 Introduction
- Evidence: 现有语义 SLAM 闭集标签限制开放词汇推理与 LLM 交互，VLM 连续嵌入是演化方向
- Quote: “However, most existing semantic SLAM [46,19,45,18] rely on closed-set semantic labels or scene-specific features. Such representations limit open-vocabulary reason- ing and prevent direct interaction with LLMs. In contrast, Vision-Language Models (VLMs) [25,17,4] offer continuous, language-aligned embeddings that encode rich and generalizable semantics.”
- Authors: seongbo-ha; sibaek-lee; kyungsu-kang; et al.

### EA-SLAMCORE-2026-0192

- Claim: 在 Replica 与 TUM-RGBD 上，本系统在同时优化几何场与高维语义场的前提下取得领先的跟踪与几何指标：Replica 上 ATE RMSE 0.213 cm（四方法最优；Point-SLAM/SplaTAM/MonoGS 分别 0.471/0.367/0.318）、PSNR 35.92 dB、System FPS 15；TUM-RGBD 上 PSNR 23.78 dB（最高）、ATE 2.316 cm、System FPS 15，作者强调全部结果无任何后优化。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06991](https://arxiv.org/abs/2602.06991) LangGS-SLAM: Real-Time Language-Feature Gaussian Splatting SLAM
- Locator: page 9, Table 1
- Evidence: 15 FPS 同时双场优化：Replica ATE 0.213 cm 最优、PSNR 35.92，超过几何-only SLAM 基线（Table 1）
- Quote: “Table 1: Tracking Accuracy and Geometric fidelity Our method attains the best track- ing accuracy on Replica and competitive accuracy on TUM-RGBD, while maintaining high system (tracking and mapping) speed. Despite jointly optimizing both geometric and semantic fields, our system surpasses geometry-only baselines in both speed and geometric quality. All results are reported without any post-optimization. Method Replica Dataset TUM-RGBD Dataset PSNR [dB] ↑ SSIM ↑ LPIPS ↓ ATE RMSE [cm] ↓ System FP”
- Authors: seongbo-ha; sibaek-lee; kyungsu-kang; et al.

### EA-SLAMCORE-2026-0193

- Claim: Replica 语义保真度（对统一 LSeg GT 特征协议）：Ours 平均 Accuracy 0.883、mIoU 0.673、FPS 15，优于 LeRF（0.618/0.277/5.392）与 LangSplat（0.614/0.263/0.863），与离线 Feature3DGS 512-D（Accuracy 0.893 / mIoU 0.671 / FPS 0.300）像素精度相当、mIoU 略高，系统速度约为其 50 倍（15 vs 0.300 FPS）。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06991](https://arxiv.org/abs/2602.06991) LangGS-SLAM: Real-Time Language-Feature Gaussian Splatting SLAM
- Locator: page 10, Table 2
- Evidence: 语义保真度与离线 Feature3DGS 相当（mIoU 0.673 vs 0.671）且 FPS 15 vs 0.300，约 50 倍速（Table 2）
- Quote: “Table 2: Evaluation Results of Semantic Fidelity on Replica Dataset. The proposed method demonstrates higher semantic fidelity than LeRF and LangSplat, and compara- ble performance to Feature3DGS while delivering fast system speed. Method Metric r0 r1 r2 o0 o1 o2 o3 o4 Avg. LeRF [16] Accuracy ↑ 0.494 0.697 0.710 0.633 0.613 0.557 0.554 0.685 0.618 mIoU ↑ 0.272 0.217 0.358 0.362 0.323 0.150 0.201 0.333 0.277 FPS ↑ 5.376 5.323 5.368 5.402 5.427 5.413 5.428 5.403 5.392 LangSplat [24] Accuracy ↑ 0.5”
- Authors: seongbo-ha; sibaek-lee; kyungsu-kang; et al.

### EA-SLAMCORE-2026-0183

- Claim: 作者陈述：3D 视觉基础模型 Transformer 架构的二次复杂度 O(N²) 带来严重内存约束与计算瓶颈，使其无法直接部署于长时域序列；为此既有方法采用分治策略——滑窗（Maggio et al., 2025，即 VGGT-SLAM）与简单分块（Deng et al., 2025，即 VGGT-Long）——来扩展规模（page 2 随即论证这类运动无关的刚性分治引入几何断裂、零运动漂移与上下文不对称三大新问题，构成本文立论基础）。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 1, Sec 1 Introduction
- Evidence: 基础模型 O(N²) 复杂度使长时域直接部署不可行，必须依赖 SLAM 式分治组织
- Quote: “However, the quadratic complexity (O(N 2 )) of their Transformer-based architectures imposes severe memory constraints and computational bottlenecks, rendering direct deployment on long-horizon sequences infeasible. To this end, some methods adopt divide-and-conquer strate- gies, such as sliding windows (Maggio et al., 2025) or sim- ple chunking (Deng et al., 2025).”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0185

- Claim: 全局一致性由子图级轻量位姿图优化承担：节点为子图位姿（Sim(3)），与帧级方法不同，优化在子图级进行（K≪N 节点）显著降低计算复杂度；边纳入来自相邻重叠与回环的相对 Sim(3) 约束（各按内点率加权）——该表述绕开了昂贵的帧级束调整，把稠密几何信息浓缩为高效的子图级约束。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 5, Sec 3.3 Lightweight Pose Graph Optimization
- Evidence: 全局一致性仍由回环+子图级位姿图优化（Lie 群 LM）实现，仅绕开帧级束调整的复杂度
- Quote: “Unlike frame-level methods, our optimiza- tion is performed at the submap level (K ≪ N nodes), significantly reducing computational complexity. Edges E incorporate relative Sim(3) constraints ˆ S ij from adjacent overlaps and loop closures, each weighted by its inlier ratio w ij = η ij . This formulation bypasses expensive frame- level bundle adjustment by condensing dense geometric information into efficient submap-level constraints.”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0186

- Claim: 零样本长序列主结果（Sec 4.3，4Seasons/Complex Urban/A2D2，公里级、数万帧且均不在 VGGT 预训练语料内）：VGGT-Motion 相对 SOTA VGGT-Long 在 ATE 与 Drift 上均实现 85–95% 降低；作者将成功归因于针对性算法设计——几何锚点子图组合把回环关键帧注入为几何锚点以跨越季节外观差异（及锚点直接 Sim(3) 配准、运动感知子图构建，见同页续文）。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 6, Sec 4.3 Zero-Shot Generalization & Scalability
- Evidence: 零样本公里级序列 ATE/Drift 相对 VGGT-Long 降低 85–95%，归因于回环锚点注入+直接 Sim(3) 配准+运动感知构建
- Quote: “In contrast, our method delivers substantially more precise and robust trajectory estimation, with an 85–95% reduction in both ATE and Drift over VGGT-Long. We attribute this success to our targeted algorithmic designs: Submap Com- position with Geometric Anchors injects loop keyframes as geometric anchors to bridge appearance gaps across seasons”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0188

- Claim: 作者自述第三条局限：与传统单目 SLAM 类似，本系统在回环间隔较长的区间仍面临累积的尺度/旋转/平移漂移；集成可推断近度量几何的基础模型（如 MapAnything、Depth Anything-v3）可缓解尺度模糊并增强局部一致性，但仅靠学习视觉先验常不足以保证有界的全局误差——大规模环境中实现高精度度量精度仍需融合辅助传感器（如 IMU）以提供鲁棒的绝对约束。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 15, Appendix B.3 Limitation
- Evidence: 作者自认：仅靠学习视觉先验不足以保证有界全局误差，高精度度量仍需 IMU 等辅助传感器融合
- Quote: “Third, similar to traditional monocular SLAM, our system faces accumulated scale, rotation, and translation drift, particularly during extended intervals between loop closures. Although integrating foundation models that infer near- metric geometry (e.g., MapAnything, Depth Anything-v3) can mitigate scale ambiguity and enhance local consistency, relying solely on learned visual priors is often insufficient to guarantee bounded global error. Consequently, achieving high-precision metric accuracy”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0057

- Claim: 等记忆预算（0.057GB）下，隐式语言地图在 Isaac Sim 1.6km×1.8km 城市场景的零样本目标导航全面优于显式表示：SR(Easy) 0.67 vs 网格 0.08/节点 0.41，SR(Hard) 0.42 vs 0.0/0.21，GDist(Hard) 1.74m vs 4.14m；网格法需约 1000 倍记忆（56.34GB）才达到可比的 SR(Easy) 0.83
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11862](https://arxiv.org/abs/2602.11862) LAMP: Implicit Language Map for Robot Navigation
- Locator: page 6
- Evidence: Table I（等记忆）与 Table II（记忆密集）双重设定：网格稠密版 56.34GB 记忆换 SR(Easy) 0.83/SR(Hard) 0.36；节点稠密版 3.962GB 换 0.67/0.47；LAMP 以 0.057GB 达 0.67/0.42。查询时间 LAMP 0.80s（网格 0.10s、节点 0.34s）。
- Quote: “the grid-based method requires approximately 1,000 times more memory than our method to achieve comparable performance by setting the grid size to 40cm.”
- Authors: sibaek-lee; hyeonwoo-yu; giseop-kim; et al.

### EA-SLAMCORE-2026-0058

- Claim: 真机验证：M2 机器人在 28 层建筑（每层 20-30 稀疏节点）上零样本语言导航成功率 90%（与显式基线持平），剩余目标距离 1.89m 显著优于显式基线 5.19m，代价是查询时间 3.84s vs 1.82s
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11862](https://arxiv.org/abs/2602.11862) LAMP: Implicit Language Map for Robot Navigation
- Locator: page 7
- Evidence: Table IV 真机试验：两方法成功率同为 90.0%，LAMP GDist 1.89m vs 显式 5.19m（降低 64%），时间 3.84s vs 1.82s；定性案例（'drinks' 目标无节点直接观测）展示场插值推断能力。
- Quote: “we set approximately 20–30 nodes sparsely on each floor. During navigation, the robot first moves toward a target node based on the given natural language command and then refines its position through optimization.”
- Authors: sibaek-lee; hyeonwoo-yu; giseop-kim; et al.

### EA-SLAMCORE-2026-0061

- Claim: 粗到细两阶段管线各司其职：图上 A* 粗规划先达到 42-67% 成功率，场内梯度优化把目标距离稳定降低约 50%（易例总是更近、难例 90% 成功），单查询总耗时 <1s（RTX 4090）
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11862](https://arxiv.org/abs/2602.11862) LAMP: Implicit Language Map for Robot Navigation
- Locator: page 5
- Evidence: Sec IV-B：'The initial coarse stage achieves a success rate of 42-67%, after which the fine-grained optimization stage consistently reduces the goal distance by about 50%.'；时间 0.8041s（Table I）。细化阶段用多起点采样 + 距离正则（λ_dist=5）避免局部最优。
- Quote: “The initial coarse stage achieves a success rate of 42-67%, after which the fine-grained optimization stage consistently reduces the goal distance by about 50%. For easy cases, this optimization always moves closer to the target, and for hard cases, it succeeds in 90% of cases.”
- Authors: sibaek-lee; hyeonwoo-yu; giseop-kim; et al.

### EA-SLAMCORE-2026-0064

- Claim: ScaleMaster 的真值生产管线以商品化 SLAM/VIO 为度量骨干：基线相机轨迹由 Apple ARKit 框架生成（作者称其在大尺度室内空间有厘米级精度），稠密参考地图由高分辨率 LiDAR 点云投影到 ARKit 轨迹上构建；作者明确接受 ARKit 轨迹可能存在的长期漂移、以残余厘米级误差为可容忍代价，因为目标是暴露深度单目 SLAM 的根本性尺度失效。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.18174](https://arxiv.org/abs/2602.18174) Have We Mastered Scale in Deep Monocular Visual SLAM? The ScaleMaster Dataset and Benchmark
- Locator: page 3, Section IV-B Baseline Pose Generation
- Evidence: 基准真值轨迹由 Apple ARKit（商品化 SLAM/VIO）生成，参考地图由 LiDAR 投影到 ARKit 轨迹构建
- Quote: “The baseline camera trajectories were obtained using Apple’s ARKit framework, which is known to provide centimeter-level accuracy in large indoor spaces. Since our primary goal is to highlight the fundamental scale failures, ARKit trajectories that may potentially exhibit long-term drift are sufficient, where residual centimeter-scale errors are tolerable. To build reference maps, we projected high- resolution LiDAR point clouds onto the ARKit trajectories.”
- Authors: hyoseok-ju; bokeon-suh; giseop-kim

### EA-SLAMCORE-2026-0078

- Claim: 论文在相关工作部分明确主张：尽管前馈式重建/位姿估计方法（DUSt3R 系，如 MonST3R、CUT3R、TTT3R）能产生视觉上可信的几何，纯前馈管线在恢复准确相机轨迹和度量一致结构方面仍逊于 SLAM 式系统；其方法因立足于视觉 SLAM 框架而获得更准确的相机轨迹与重建。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19076](https://arxiv.org/abs/2603.19076) DROID-SLAM in the Wild
- Locator: page 3, Sec. 2 Feed-forward Approaches 末段
- Evidence: 作者立场：前馈基础模型管线在准确轨迹与度量一致结构上仍不如 SLAM 式优化系统。
- Quote: “purely feed-forward pipelines often struggle to recover accurate camera trajectories and metrically consis- tent structure compared to SLAM-style systems. In contrast, our method, grounded in a visual SLAM framework, yields more accurate camera trajectories and reconstructions.”
- Authors: moyang-li; zihan-zhu; marc-pollefeys; et al.

### EA-SLAMCORE-2026-0079

- Claim: 在作者自建的户外动态数据集 DROID-W（Downtown 1-7，Livox Mid-360 LiDAR 与 RGB 相机刚性安装采集，RTK/FAST-LIVO2 真值）上，优化式 SLAM 系统 DROID-W 平均 ATE RMSE 为 0.230 m，优于全部对比基线：前馈式 TTT3R 平均 7.309 m、DROID-SLAM 1.460 m、Splat-SLAM 1.597 m、WildGS-SLAM 0.637 m；作者据此陈述前馈方法在所有基准上的跟踪误差显著高于优化式 SLAM 系统。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19076](https://arxiv.org/abs/2603.19076) DROID-SLAM in the Wild
- Locator: page 7, Table 4 及其后讨论
- Evidence: 户外动态数据集实测：优化式 SLAM 平均 ATE 0.230 m，前馈 TTT3R 为 7.309 m，差距达一个数量级以上。
- Quote: “Feed-forward approaches such as MonST3R [ 62 ] and TTT3R [7] suffer from substantially higher tracking er- rors across all benchmarks compared to optimization-based SLAM systems.”
- Authors: moyang-li; zihan-zhu; marc-pollefeys; et al.

### EA-SLAMCORE-2026-0080

- Claim: 系统在 RTX 3090 GPU + 16 核 CPU 上保持约 10 FPS 的实时性能（Bonn 10.57 / TUM 14.92 / DyCheck 11.06 FPS），相比最新动态单目 SLAM 基线 WildGS-SLAM（0.22/0.32/0.18 FPS）取得 40 倍加速，仅略慢于 DROID-SLAM（19.89/26.97/17.50 FPS），降速来自单目深度估计与 DINOv2 特征提取的额外开销。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19076](https://arxiv.org/abs/2603.19076) DROID-SLAM in the Wild
- Locator: page 7, Table 5 及运行时讨论
- Evidence: 鲁棒动态 SLAM 在 RTX 3090 上实时约 10 FPS，较 WildGS-SLAM 提速 40 倍，仅略慢于 DROID-SLAM 基座。
- Quote: “Our system achieves a 40× speedup over WildGS-SLAM and maintains real-time performance at approximately 10 FPS. Our ap- proach is slightly slower than DROID-SLAM due to monoc- ular depth estimation and DINOv2 [ 37 ] feature extraction.”
- Authors: moyang-li; zihan-zhu; marc-pollefeys; et al.

### EA-SLAMCORE-2026-0082

- Claim: 论文引言将具身智能（embodied intelligence）与自动驾驶、机器人并列为 SLAM 的主要应用领域（以引用 [5,15,24] 支撑，分别涉及免训练具身目标导航、EgoDex 自我中心操作数据、城市级自我中心视觉-惯性 SLAM 基准），以此作为研究动机的一部分。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2603.19076](https://arxiv.org/abs/2603.19076) DROID-SLAM in the Wild
- Locator: page 1, Sec. 1 Introduction
- Evidence: SLAM 系统论文在引言中将具身智能与自动驾驶、机器人并列为 SLAM 的应用领域（引用支撑的动机陈述）。
- Quote: “in autonomous driving [3, 12], robotics [ 1 , 31, 69], and em- bodied intelligence [5, 15, 24].”
- Authors: moyang-li; zihan-zhu; marc-pollefeys; et al.

### EA-SLAMCORE-2026-0088

- Claim: 作者自述：先前基于 Transformer 的 VGGT-SLAM 管线主要依赖稀疏回环或全局 Sim(3) 流形约束，允许回环事件之间的短时程位姿漂移；VGGT-SLAM++ 通过空间校正后端恢复高频局部 Bundle Adjustment（LBA）来抑制该漂移。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.06830](https://arxiv.org/abs/2604.06830) VGGT-SLAM++
- Locator: page 1
- Evidence: 前馈 VGGT-SLAM 的短时漂移问题由补回的高频局部 BA 后端解决（作者自述设计动机）
- Quote: “While prior transformer-based SLAM pipelines such as VGGT-SLAM rely primarily on sparse loop clo- sures or global Sim(3) manifold constraints—allowing short-horizon pose drift—VGGT-SLAM++ restores high- cadence local bundle adjustment (LBA) through a spa- tially corrective back-end.”
- Authors: avilasha-mandal; rajesh-kumar; sudarshan-sunil-harithas; et al.

### EA-SLAMCORE-2026-0089

- Claim: 在五个基准上，VGGT-SLAM++ 相比 VGGT-SLAM 基线（Sim(3) 与 SL(4) 每数据集平均）将 ATE RMSE 从 17.13 m 降至 13.94 m（总体 -18.6%），其中 KITTI -20%、TUM -45%、7-Scenes -5%、Virtual KITTI -14%、EuRoC -9%。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.06830](https://arxiv.org/abs/2604.06830) VGGT-SLAM++
- Locator: page 7
- Evidence: 补回经典 SLAM 后端使 VGGT-SLAM 路线整体 ATE 降低 18.6%（17.13 m -> 13.94 m）
- Quote: “Compared to the VGGT-SLAM baseline (Sim(3)+SL(4) averaged per dataset), VGGT-SLAM++ reduces ATE by 20% on KITTI, 45% on TUM, 5% on 7-Scenes, 14% on Virtual KITTI, 9% on EuRoC [ 8] (see Appendix A1). The combined VGGT-SLAM baseline (Sim(3)+SL(4), averaged per-dataset) results in ATE RMSE 17.13 m whereas that of VGGT-SLAM++ is 13.94 m, across the four datasets, hence we achive an overall improvement by 18.6%.”
- Authors: avilasha-mandal; rajesh-kumar; sudarshan-sunil-harithas; et al.

### EA-SLAMCORE-2026-0098

- Claim: 作者把动态环境确立为稠密视觉 SLAM 的核心失效场景：移动机器人常在动态环境中运行，不可预测的变化会使稠密 SLAM 算法性能显著退化；其机制性原因是 SLAM 渐进式逐帧处理图像，单帧只能提供物体的静态属性（轮廓、形状、纹理、语义标签）而缺乏显式运动信息，运动本质由多帧序列中的位置变化定义。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12837](https://arxiv.org/abs/2604.12837) GGD-SLAM: Monocular 3DGS SLAM Powered by Generalizable Motion Model for Dynamic Environments
- Locator: page 1
- Evidence: 动态环境是稠密 SLAM 的核心挑战：单帧无运动信息，运动须由多帧时序定义。
- Quote: “In the context of SLAM, where image frames are processed progressively, a single frame can only pro- vide static attributes of objects, such as contour, shape, texture, and semantic labels [7], but lacks any explicit motion information. The motion nature is inherently defined by its positional change over a sequence of frames.”
- Authors: yi-liu; haoxuan-xu; hongbo-duan; et al.

### EA-SLAMCORE-2026-0099

- Claim: GGD-SLAM 的核心组件是专为渐进式 SLAM 输入设计的泛化运动模型（GMM）：对每帧提取 DINOv2 结构特征，经 FIFO 队列聚合历史帧特征，用序列注意力（当前帧为 query、历史帧为 key/value）做跨帧匹配，经动态/静态双头门控增强得到运动概率图，推理时以 OTSU 自适应阈值二值化并做形态学膨胀得到域无关动态先验二值掩码；该模型离线训练、无需逐场景在线训练，作为 GS-SLAM 系统的鲁棒先验使用。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12837](https://arxiv.org/abs/2604.12837) GGD-SLAM: Monocular 3DGS SLAM Powered by Generalizable Motion Model for Dynamic Environments
- Locator: page 3
- Evidence: 泛化运动模型机制：DINOv2+FIFO 历史帧队列+序列注意力，离线训练、免逐场景在线训练。
- Quote: “Our main contribution lies in designing a generalizable motion model for a dynamic semantics extractor within im- age sequences, designed specifically for progressive SLAM systems as Algorithm 1. This generalizable motion model eliminates the need for per-scene online training, serving as a robust prior for GS-SLAM systems.”
- Authors: yi-liu; haoxuan-xu; hongbo-duan; et al.

### EA-SLAMCORE-2026-0100

- Claim: 在 TUM 与 Bonn 动态序列的相机跟踪评测（Table I，ATE RMSE，单位 cm）中，单目 GGD-SLAM 在 fr3/w/half、bonn/crowd2 与 Bonn 平均值上分别取得 1.4、1.8、2.7 cm，均优于同为单目动态方法的最新基线 WildGS-SLAM（对应 1.5、2.3、2.9 cm）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12837](https://arxiv.org/abs/2604.12837) GGD-SLAM: Monocular 3DGS SLAM Powered by Generalizable Motion Model for Dynamic Environments
- Locator: page 6, Table I
- Evidence: Table I：单目 GGD-SLAM 跟踪 ATE 在所示序列与 Bonn 平均上全面优于最新单目动态基线 WildGS-SLAM。
- Quote: “WildGS-SLAM [6] 1.3 0.6 1.5 0.8 1.8 1.1 1.4 0.8 2.9 1.2 2.5 1.2 3.6 1.9 2.3 1.1 2.9 1.4 Ours 1.1 0.6 1.4 0.7 1.5 0.8 1.3 0.7 2.4 1.0 2.3 1.1 3.4 1.8 1.8 0.8 2.7 1.1”
- Authors: yi-liu; haoxuan-xu; hongbo-duan; et al.

### EA-SLAMCORE-2026-0101

- Claim: Bonn 消融（Table II）量化了泛化先验的价值：完整配置（Generalizable Prior + OTSU Binarize + Smoothness）在 ps_track / crowd2 上 ATE 为 3.41 / 1.79 cm；去掉泛化先验与 OTSU 后退化为 3.56 / 2.14 cm，其中 crowd2 退化最明显，表明学习型运动先验是动态场景跟踪精度的关键来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12837](https://arxiv.org/abs/2604.12837) GGD-SLAM: Monocular 3DGS SLAM Powered by Generalizable Motion Model for Dynamic Environments
- Locator: page 6, Table II
- Evidence: 消融：去掉泛化先验+OTSU 后 crowd2 ATE 从 1.79 退化到 2.14 cm，先验是动态跟踪关键。
- Quote: “Generalizable Prior refers to prior information from GMM; OTSU Binarize is our solution for ambiguous edges; and Smoothness refers to the smoothness term in Tracking. Generalizable Prior OTSU Binarize Smoothness ps track crowd2 ✓ ✓ × 3.47 1.95 ✓ × ✓ 3.44 1.86 × × ✓ 3.56 2.14 ✓ ✓ ✓ 3.41 1.79”
- Authors: yi-liu; haoxuan-xu; hongbo-duan; et al.

### EA-SLAMCORE-2026-0110

- Claim: 第一批（常规光照）序列确认事件相机在高速机动中的优势：帧相机 DPVO 的 ATE 更低（批1 平均 0.127 m vs SDEVO 0.271 m，arm norm 上 0.059 vs 0.069 m），但速度估计 AUC 不及事件-only 的 SDEVO（批1 平均 0.838 vs 0.876；arm norm 上 SDEVO 0.855 > DPVO 0.730 > 帧 VINS 0.694）；作者结论是事件相机在高速机动场景优于帧相机且优势随光流增大而扩大、帧相机与事件相机互补（帧提供纹理保中低速精度、事件借高时间分辨率与高动态范围抗高速干扰，论述见 page 11）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.24033](https://arxiv.org/abs/2604.24033) Event-based SLAM Benchmark for High-Speed Maneuvers
- Locator: page 12, Table VII
- Evidence: 常规光照高速机动中事件 SLAM 速度精度优于帧相机（arm norm AUC 0.855 vs 0.730），帧-事件互补
- Quote: “arm norm 0.048 / 0.831 0.033 / 0.857 0.164 / 0.784 0.033 / 0.857 0.069 / 0.855 0.078 / 0.655 1.966 / 0.805 0.170 / 0.694 0.059 / 0.730 car circle norm 0.149 / 0.904 0.076 / 0.904 0.131 / 0.873 0.179 / 0.844 0.263 / 0.854 0.064 / 0.913 1.505 / 0.784 0.150 / 0.887 0.215 / 0.815 Average 0.117 / 0.898 0.064 / 0.896 0.192 / 0.869 0.123 / 0.877 0.271 / 0.876 0.066 / 0.864 1.513 / 0.840 0.188 / 0.861 0.127 / 0.838”
- Authors: sheng-zhong; junkai-niu; guillermo-gallego; et al.

### EA-SLAMCORE-2026-0111

- Claim: EvSLAM 基准全部序列的真值由动捕系统提供：真值轨迹由手眼标定结果与 MoCap 数据融合生成，作者称达到亚毫米级 6-DoF 位姿精度；无人机序列用 LUSTER FZMotion MoCap（120 Hz 采样），其余序列用 NOKOV Mars26H（60 Hz 采样）；所有序列含多个闭环、在动捕可观测边界内录制。即高速机动场景的位姿评测以动捕（而非 SLAM）为度量基础设施。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.24033](https://arxiv.org/abs/2604.24033) Event-based SLAM Benchmark for High-Speed Maneuvers
- Locator: page 9, Section IV-D Sequences Overview
- Evidence: 全部序列真值由动捕（LUSTER 120 Hz / NOKOV 60 Hz）+ 手眼标定融合生成，作者称亚毫米级
- Quote: “incorporate multiple closed loops, whose ground-truth trajec- tories are derived by fusing hand-eye calibration results with MoCap data, yielding sub-millimeter-level accuracy for 6-DoF pose estimation. Specifically, the LUSTER FZMotion MoCap system, operating at a 120 Hz sampling rate, is deployed for drone sequences, while the NOKOV Mars26H system with a 60 Hz sampling rate is used for all remaining.”
- Authors: sheng-zhong; junkai-niu; guillermo-gallego; et al.

### EA-SLAMCORE-2026-0200

- Claim: 作者主张：把基础模型接地（grounding）到大尺度 3D 语义地图上是实现稳健高效上下文主动 SLAM 的关键——用小得多的 Qwen2.5-VL-7B 模型 RoboAtlas 仍达 88.8% SR、超过所有用 GPT-4o 的基线，揭示了语义建图框架获得的信息的重要性高于简单替换底层基础模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26046](https://arxiv.org/abs/2606.26046) RoboAtlas: Contextual Active SLAM
- Locator: page 1, Abstract
- Evidence: 把基础模型接地到大尺度 3D 语义地图：7B 骨干 88.8% SR 胜过所有 GPT-4o 基线，增益来自语义建图而非骨干容量
- Quote: “Using the much smaller Qwen2.5-VL-7B model, it still achieves 88.8% SR, outperforming all baselines using GPT- 4o in SR, and revealing the importance of the information gained by our semantic mapping framework over simply replacing the underlying foundation model. The results demonstrate that grounding foundation models with large-scale 3D semantic maps enables robust and efficient contextual Active SLAM.”
- Authors: alexander-schperberg; shivam-k-panda; abraham-p-vinod; et al.

### EA-SLAMCORE-2026-0201

- Claim: 作者对零样本 VLM/LLM 导航路线（VLFM、ASCENT、DyNaVLM 等）的批评：这类方法主要依赖图像感知与拓扑场景表征、不维护全局一致的度量地图，导致语义推理和导航常与几何定位和建图解耦；相比之下 RoboAtlas 把视觉-语言推理直接集成进实时 Active SLAM 管线与实例级 3D 语义地图，在做语言条件决策的同时保持可靠导航所需的度量一致性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26046](https://arxiv.org/abs/2606.26046) RoboAtlas: Contextual Active SLAM
- Locator: page 2, Section II-A 末段
- Evidence: 零样本 VLM 导航不维护全局一致度量地图、语义推理与几何定位解耦；RoboAtlas 将 VL 推理集成进实时 Active SLAM 保持度量一致性
- Quote: “However, these approaches primarily rely on image-based perception and topological scene representation that do not maintain a globally consistent metric map of the environment. As a result, semantic reasoning and navigation are often decoupled from geometric localization and mapping. In contrast, RoboAtlas integrates vision-language reasoning di- rectly with a real-time Active SLAM pipeline and an instance- level 3D semantic map, enabling language-conditioned deci- sion making while preserving”
- Authors: alexander-schperberg; shivam-k-panda; abraham-p-vinod; et al.

### EA-SLAMCORE-2026-0202

- Claim: 真实硬件部署的系统架构：机载 Jetson AGX Orin 在 ROS2 下运行 Active SLAM 栈——用 SLAM Toolbox 做定位与 2D 栅格建图、Nav2 做自主导航（SMAC 全向 A* 规划器在占据栅格上搜索）；Unitree Go2 API 以 500 Hz 提供融合板载 LiDAR 与关节编码器的 EKF 里程计，SLAM Toolbox 以 100 Hz 提供位姿估计，RGB-D 以 30 Hz 流入 RoboAtlas 生成 0.07-0.2 Hz 的导航目标。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26046](https://arxiv.org/abs/2606.26046) RoboAtlas: Contextual Active SLAM
- Locator: page 11, Section V-A Hardware 段
- Evidence: Go2 真机栈：SLAM Toolbox 定位+2D 栅格建图（100Hz 位姿）、Nav2 规划、500Hz EKF 里程计——基础模型只做目标选择
- Quote: “The Jetson runs the Active SLAM stack under ROS2, using SLAM Toolbox [54] for localization and 2D grid mapping and Nav2 [60] for autonomous navigation. We use the Nav2 SMAC planner, which performs a holonomic A* search over the occupancy grid while modeling the robot as a rectangular footprint for collision avoidance [61]. Odometry at 500 Hz is obtained from the Unitree Go2 API, which fuses onboard LiDAR and joint-encoder data through an Extended Kalman Filter, and the SLAM Toolbox provides pose”
- Authors: alexander-schperberg; shivam-k-panda; abraham-p-vinod; et al.

### EA-SLAMCORE-2026-0204

- Claim: GOAT-Bench Val Unseen 上的归因分析：RoboAtlas（Qwen2.5-VL-7B）在 SR 和 SPL 两项指标上都超过除 HIMM 外的所有 GPT-4o 基线——例如在 SR（88.8 vs 68.9）和 SPL（53.1 vs 48.9）上均超过 3D-Mem（GPT-4o）；对 HIMM 仍在成功率上领先（88.8 vs 72.8）、仅 SPL 落后。作者据此主张：一个 7B 骨干能与 GPT-4o 规模基线竞争，说明改进来自语义建图与上下文专家选择，而非骨干容量。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26046](https://arxiv.org/abs/2606.26046) RoboAtlas: Contextual Active SLAM
- Locator: page 17, Section V-C 基线对比分析段
- Evidence: 7B 骨干反超 GPT-4o 基线（SR 88.8 vs 68.9/72.8）：增益来自语义建图与专家选择而非基础模型容量
- Quote: “It surpasses 3D-Mem (GPT-4o), for instance, on both SR (88.8 vs. 68.9) and SPL (53.1 vs. 48.9). Against HIMM, RoboAtlas still leads in success rate (88.8 vs. 72.8) and trails only in SPL. A 7B backbone competing with GPT-4o-scale baselines suggests the improvements come from our semantic mapping and contextual expert selection rather than backbone capacity.”
- Authors: alexander-schperberg; shivam-k-panda; abraham-p-vinod; et al.

### EA-SLAMCORE-2026-0125

- Claim: 系统架构上，GaussLite 建立在 Gaussian-SLAM mapper 之上并把相机位姿显式当作外部输入，将建图贡献与位姿估计解耦：Replica 用仿真 GT 位姿，真实 Campus 数据集的位姿由 DLIO LiDAR-惯性里程计在线产出（数据在 Clearpath Husky rover 上以 ZED 2i 立体相机采集、RTX 4070 Laptop GPU 机载处理）。即该机器人建图系统的真实部署由经典 LiDAR-惯性里程计供给位姿，视觉位姿估计不在系统内。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.30809](https://arxiv.org/abs/2606.30809) GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Robotic Mapping
- Locator: page 4, Section III-C
- Evidence: 位姿被显式外部化：真机由经典 LIO（DLIO）在线供给，建图创新全部叠加其上
- Quote: “We build on the Gaussian-SLAM [2] mapper and treat camera poses as an external input, decoupling our mapping contribution from pose estimation; on Replica we use sim- ulation ground-truth poses, while on our campus dataset we use LiDAR-inertial odometry from DLIO [44].”
- Authors: annika-thomas; mason-peterson; jonathan-p-how

### EA-SLAMCORE-2026-0126

- Claim: GaussLite 是任务驱动的 3DGS 建图系统：表征密度以自然语言任务规格为条件——给定带位姿的 RGB-D 流与任务（如 'prepare to pick up the object on the desk'），一次性 LLM 解析器抽取目标与锚定对象，开放词汇检测器逐帧接地、分割产生实时逐像素相关性掩码，mapper 按任务相关性分配播种密度、梯度流与尺度。作者在引言中称其为首个接受自然语言任务输入并在线空间分配场景表征的系统，并首个把该原则扩展到机器人团队。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.30809](https://arxiv.org/abs/2606.30809) GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Robotic Mapping
- Locator: page 1, Abstract 与 Introduction
- Evidence: 任务驱动 3DGS 建图：自然语言任务 → LLM 解析 + 开放词汇检测 → 逐像素相关性 → 表征容量在线分配
- Quote: “We introduce GaussLite, a task-driven 3DGS mapping system that conditions its representation density on a natural-language task specification. Given a posed RGB-D stream and a task such as “prepare to pick up the object on the desk,” GaussLite uses a one- shot LLM parser to extract target and anchor objects, which are grounded per-frame by an open-vocabulary detector and segmented to produce per-pixel relevance masks in real time.”
- Authors: annika-thomas; mason-peterson; jonathan-p-how

### EA-SLAMCORE-2026-0127

- Claim: 匹配预算对比（同位姿源、同高斯预算、同每帧实时预算、无离线精化）：Campus 真机数据上 GaussLite 在全部设定取得最优 ROI PSNR，平均超 SplaTAM +1.70 dB、Gaussian-SLAM +2.99 dB、MonoGS +1.99 dB；Replica 上平均 ROI PSNR 29.81 dB 亦为三基线最优（超 SplaTAM +1.25、Gaussian-SLAM +3.19、MonoGS +3.71 dB，8 场景中 7 个胜出）。作者强调：由于所有对比在匹配高斯数与实时每帧预算下进行，这些增益完全归因于预算被花在哪里（where the budget is spent）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.30809](https://arxiv.org/abs/2606.30809) GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Robotic Mapping
- Locator: page 6, Section IV-B
- Evidence: 匹配预算下真机 +1.70/+2.99/+1.99 dB、Replica +1.25/+3.19/+3.71 dB ROI PSNR，增益全部来自预算重分配
- Quote: “On the Campus dataset (Tab. II), GaussLite achieves the best ROI PSNR in all settings, outperforming SplaTAM by +1.70 dB, Gaussian-SLAM by +2.99 dB, and MonoGS by +1.99 dB in mean ROI PSNR. Because all comparisons are at matched Gaussian count and real-time per-frame budget, these gains are entirely attributable to where the budget is spent.”
- Authors: annika-thomas; mason-peterson; jonathan-p-how

### EA-SLAMCORE-2026-0026

- Claim: 与最接近的实时开放词汇高斯建图系统 OLS（Online Language Splatting）在 Replica（8 场景平均）上的对比（Table I）：LEGO-SLAM 渲染质量 PSNR 36.99（OLS 35.81）、语义精度 mIoU 0.543（OLS 0.487），同时快约 12 倍（15.0 vs 1.25 FPS）；OLS 数值为论文自报值，对比采用 OLS 所用的 LangSplat 式文本查询协议。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.16144](https://arxiv.org/abs/2511.16144) LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM
- Locator: page 5, Table I
- Evidence: 较此前唯一在线开放词汇方案 OLS 快约 12 倍（15.0 vs 1.25 FPS）且渲染/语义精度更优（Replica）
- Quote: “As shown in Table I, LEGO-SLAM outperforms OLS in rendering quality (PSNR +1.2 dB) and semantic accuracy (mIoU +0.056) while running about 12× faster.”
- Authors: sibaek-lee; seongbo-ha; kyeongsu-kang; et al.

### EA-SLAMCORE-2026-0027

- Claim: 追踪精度（ATE RMSE）：LEGO-SLAM 在 Replica 上取得全部对比 NeRF-SLAM/3DGS-SLAM 系统中的最低平均 ATE（0.22 cm）；在真实 TUM-RGBD 上 2.23 cm、大规模 ScanNet 上 8.84 cm，作者表述为'保持竞争力'（remains competitive）——但同页表格显示真实数据集上并非最优：TUM 上 MonoGS 平均 1.51 cm、ScanNet 上 LoopSplat 7.28 cm 与 Loopy-SLAM 7.87 cm 均更低。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.16144](https://arxiv.org/abs/2511.16144) LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM
- Locator: page 5, Tables III-V
- Evidence: Replica 平均 ATE 0.22 cm 为对比系统最低；TUM 2.23 / ScanNet 8.84 cm 有竞争力但非最优
- Quote: “On the Replica dataset, LEGO-SLAM achieves the lowest average ATE (0.22 cm). It remains competitive on the challenging real-world TUM-RGBD sequences (2.23 cm) and large-scale ScanNet (8.84 cm).”
- Authors: sibaek-lee; seongbo-ha; kyeongsu-kang; et al.

### EA-SLAMCORE-2026-0029

- Claim: 语言回环检测消融（Table X）：复用建图阶段已计算的语言特征做地点识别，在三个数据集上的 ATE 均低于轻量位置基线 [47]（LIO-SAM 式位置回环）：Replica 0.22 vs 0.28 cm、TUM-RGBD 2.23 vs 3.13 cm、ScanNet 8.84 vs 10.19 cm。语言特征在此承担了经典 SLAM 回环检测（通常需 NetVLAD/ORB-SLAM2 词袋等单独地点识别模型）的职能。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.16144](https://arxiv.org/abs/2511.16144) LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM
- Locator: page 7, Table X
- Evidence: 语言回环检测复用建图特征，三个数据集 ATE 均低于位置基线（0.22/2.23/8.84 vs 0.28/3.13/10.19 cm）
- Quote: “TABLE X: Loop Detection Comparison. Our language-based method achieves lower tracking error (ATE RMSE [cm] ↓) than the position-based approach. Method Replica TUM-RGBD ScanNet Position-based [47] 0.28 3.13 10.19 Language-based 0.22 2.23 8.84”
- Authors: sibaek-lee; seongbo-ha; kyeongsu-kang; et al.

### EA-SLAMCORE-2026-0131

- Claim: SuperMap 论文主张：SLAM 维护的时空地图是 VLM 空间接地的必要接口——将几何细节委托给时空地图后，VLM 可对长期场景动态做零样本推理而无需处理原始点云或视频流；直接使用基础模型预测会因间歇性和视角依赖导致身份漂移与过期语义
- Stance: `support` | Confidence: `direct`
- Paper: [2608.22896](https://arxiv.org/abs/2608.22896) SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation
- Locator: page 5
- Evidence: 论文动机与方法节明确论证：基础模型零样本识别强但预测间歇、视角依赖，naive 集成导致 identity drift 和 stale semantics；4D 场景图作为 VLM 与物理空间的接口。
- Quote: “By delegating geometric detail to the spatio-temporal map, the VLM can perform zero-shot reasoning over long-term scene dynamics without processing raw point clouds or video streams.”
- Authors: shibo-zhao; guofei-chen; honghao-zhu; et al.

### EA-SLAMCORE-2026-0132

- Claim: 在线实例级开放词汇建图在 ScanNet 实例级分割上大幅超越离线基线：Chair mAP50 63.76 vs HOV-SG 4.58、ConceptGraphs 0.00；Window 42.20 vs 两者 0.00，证明 SLAM 几何先验驱动的 3D 感知跟踪-检测优于点特征聚类
- Stance: `support` | Confidence: `direct`
- Paper: [2608.22896](https://arxiv.org/abs/2608.22896) SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation
- Locator: page 6
- Evidence: Table III：零样本在线设置下 SuperMap 在 5 类物体上的 mAP50/mAP25 全面领先。
- Quote: “HOV-SG [30] 4.58 4.73 0.00 0.00 0.00 0.00 30.00 31.25 9.70 10.40 ConceptGraphs [5] 0.00 2.33 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 SuperMap (Ours) 63.76 74.72 42.20 67.92 62.50 62.50 33.35 83.35 10.00 25.00”
- Authors: shibo-zhao; guofei-chen; honghao-zhu; et al.

### EA-SLAMCORE-2026-0133

- Claim: 该系统在全板载（i9 CPU + RTX 4090 笔记本 GPU）实现实时运行：位姿估计 10Hz、3D 建图 3Hz、2D 实例分割 1Hz、4D 场景图更新 5Hz——实时性是区别于离线场景图方法（HOV-SG/ConceptGraphs 需数分钟到数小时）的关键部署属性
- Stance: `support` | Confidence: `direct`
- Paper: [2608.22896](https://arxiv.org/abs/2608.22896) SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation
- Locator: page 8
- Evidence: 运行时剖析节报告各模块更新频率；补充材料 Table I 报告 TPF 0.3604s/frame（HOV-SG 8.623s）。
- Quote: “The pose estimation module maintains a consistent 10 Hz output, while 2D instance segmentation operates at 1 Hz due to the heavy inference requirements of semantic segmentation. The remainder of the architecture performs 3D mapping and 4D scene graph updates at 3 Hz and 5 Hz, respectively.”
- Authors: shibo-zhao; guofei-chen; honghao-zhu; et al.

### EA-SLAMCORE-2026-0134

- Claim: 时空变化检测上 SuperMap 显著优于现有在线语义建图系统：出现物体检测 recall（桶 1.000/购物车 0.262/标志 0.583/植物 0.755/垃圾桶 0.434/椅子 1.000）对比 DualMap 全部接近零（0.000-0.310），Khronos 在该协议下无法产生结果
- Stance: `support` | Confidence: `direct`
- Paper: [2608.22896](https://arxiv.org/abs/2608.22896) SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation
- Locator: page 7
- Evidence: Table IV：6 个出现/消失事件的变化检测对比，DualMap 因不稳定的实例关联接近零 recall。
- Quote: “DualMap [8] 0.000 0.000 0.000 0.000 0.310 0.000 SuperMap (ours) 1.000 0.262 0.583 0.755 0.434 1.000”
- Authors: shibo-zhao; guofei-chen; honghao-zhu; et al.

### EA-SLAMCORE-2026-0113

- Claim: 追踪对照实验：正确初始化的经典特征 SLAM 在两种设定下均系统性优于全 GFM SLAM 系统——EuRoC 单目（排除初始化阶段）上 ORB-SLAM3 五序列 ATE 0.0206/0.0193/0.0298/0.0996/0.0459 m，全部低于 MASt3R-SLAM（0.0274/0.0291/0.0580/0.1180/0.0674）、VGGT-SLAM2（0.0614-0.6447）与 VGGT(D)-SLAM2（0.0620-0.3456）；ScaRF 鱼眼-惯性设定上经典单目-惯性方法（OV-SLAM 0.1075/0.0444/0.0316/0.0644/0.0309）显著优于紧耦合 GFM 方法（VGGT-SLAM2 达 0.7667-1.0573）。作者把性能差距归因于 GFM 预测的几何不精确性反向损害位姿估计。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00307](https://arxiv.org/abs/2606.00307) ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical Visual SLAM
- Locator: page 5, Tables I-II, Section V-A
- Evidence: EuRoC 与 ScaRF 两表：经典 SLAM（ORB-SLAM3/OV-SLAM）追踪精度系统性优于全 GFM SLAM，作者归因 GFM 几何不精确性损害位姿估计
- Quote: “The results show that, when properly initialized, ORB- SLAM3 consistently outperforms fully GFM-enabled methods in tracking. We attribute the performance gap to geometric inaccuracies in GFM predictions, which in turn adversely affect pose estimation.”
- Authors: yuhao-zhang; yifu-tao; frank-dellaert; et al.

### EA-SLAMCORE-2026-0114

- Claim: 作者对'部分全 GFM SLAM 方法在某些基准上报告追踪超过经典方法（如单目 ORB-SLAM3）'的现象给出反解释：归因于数据集偏差——这些数据集规模小且缺乏对经典单目方法至关重要的正确初始化；在具备正确初始化的数据集（EuRoC）上，经典视觉 SLAM 仍取得更高追踪精度。该归因是作者的分析性主张（引 [6][7] 即 TUM RGB-D/BAD SLAM 基准上的报告），非受控重放实验。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00307](https://arxiv.org/abs/2606.00307) ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical Visual SLAM
- Locator: page 2, Section I Introduction
- Evidence: 作者把全 GFM SLAM 报告的追踪优势归因于小规模数据集+缺乏正确初始化的偏差；正确初始化下经典 SLAM 仍更准
- Quote: “we attribute this to dataset bias: these datasets are small-scale and lack proper ini- tialization, which is critical for classical monocular methods. We show that when evaluated on datasets with proper initial- ization (e.g., EuRoC [8]), classical visual SLAM still achieves higher tracking accuracy (Section V-A).”
- Authors: yuhao-zhang; yifu-tao; frank-dellaert; et al.

### EA-SLAMCORE-2026-0115

- Claim: 系统架构主张：不用 GFM 做状态估计，而是利用经典 SLAM 的成熟度——支持多样模态（视觉-惯性）、相机装置（多相机）与相机模型（鱼眼）——做追踪，GFM 只用于稠密建图；建图锚定在 SLAM 位姿上、只优化深度尺度，从而避免 GFM 预测误差传播进追踪。摘要平行表述为'用经典视觉 SLAM 做鲁棒低延迟追踪、GFM 专用于建图'（page 1）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00307](https://arxiv.org/abs/2606.00307) ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical Visual SLAM
- Locator: page 2, Section I Introduction
- Evidence: 解耦架构：经典 SLAM（多模态/多相机/鱼眼成熟度）做追踪，GFM 仅做稠密建图，建图锚定 SLAM 位姿只优化尺度
- Quote: “Instead of relying on GFMs for state estimation, we leverage the maturity of classical SLAM that supports diverse modalities (e.g., visual-inertial), camera rigs (e.g., multi-camera), and camera models (e.g., fisheye) for tracking, while using GFMs for dense mapping only.”
- Authors: yuhao-zhang; yifu-tao; frank-dellaert; et al.

### EA-SLAMCORE-2026-0116

- Claim: 结论的普适主张：学习几何的进展不必替换经典几何管线，而可通过审慎的系统级集成实现——在学习预测之上施加轻量几何约束即可在精度、效率、鲁棒性之间取得有利平衡；作者并断言此类混合设计将在稠密建图系统走向真实部署中起关键作用。同页结论还限定当前 GFM 的局限'不在稠密几何生成，而在其预测对精确位姿估计的可靠性'。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00307](https://arxiv.org/abs/2606.00307) ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical Visual SLAM
- Locator: page 8, Section VI Conclusion
- Evidence: 结论主张：学习几何的进展不必替换经典几何管线，轻量几何约束叠加学习预测即可平衡精度/效率/鲁棒；混合设计是稠密建图走向真实部署的关键
- Quote: “Beyond the quantitative gains, our findings highlight a broader insight: progress in learned geometry does not neces- sarily require replacing classical geometric pipelines, but can instead be achieved through careful system level integration. In particular, enforcing lightweight geometric constraints on top of learned predictions provides a favorable balance between accuracy, efficiency, and robustness.”
- Authors: yuhao-zhang; yifu-tao; frank-dellaert; et al.

### EA-SLAMCORE-2026-0117

- Claim: 重建主结果（ScaRF 室内，chunk 10m、阈值 3cm、25% 置信度过滤、统一 3Hz、批次 6）：锚定经典 SLAM 位姿的 DA3 建图在精确度上超越全部对比方法 10-20%（Ours 81.06/80.44/81.26/81.63/82.90% vs 次优 VGGT(D)-SLAM2 44.13-64.20%、DA3-Long 50.32-65.64%），同时保持约 2cm 重建误差（Ours 0.0198-0.0216 m）；即使不给 DA3 提供位姿输入（w/o Ext.），仅靠尺度优化仍以 76.41-81.94% 精确度超过全部基线。作者把有位姿输入时的优势归因于解耦设计。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00307](https://arxiv.org/abs/2606.00307) ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical Visual SLAM
- Locator: page 6, Table III, Section V-B.1
- Evidence: 锚定 SLAM 位姿的 GFM 建图精确度超全部基线 10-20%、误差约 2cm/10m chunk；无位姿输入变体仍靠尺度优化取胜
- Quote: “Table III shows that our method outperforms the other approaches—including when operating without provid- ing poses to DA3. This highlights the effectiveness of the scale optimization of our method. With pose inputs enabled (benefiting from the decoupled design), it outperforms other methods in precision by 10%–20%, while maintaining around 2 cm reconstruction error.”
- Authors: yuhao-zhang; yifu-tao; frank-dellaert; et al.

### EA-SLAMCORE-2026-0118

- Claim: 批次大小敏感性消融（真值位姿、全局评估）：输入批次从 11 降到 6 时，本建图框架精确度仅降 1.60%，而直接聚合 DA3 预测降 8.03%——锚定 SLAM 位姿的尺度优化使建图对 GFM 在小批次（低视角多样性）下的退化鲁棒。作者指出该特性对 GPU 内存受限的设备、以及需要'反应式建图'（系统不能等待大量图像累积）的应用尤为重要，并明言'这在机器人领域很常见'。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00307](https://arxiv.org/abs/2606.00307) ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical Visual SLAM
- Locator: page 7, Tables IV-V, Section V-C.1
- Evidence: 批次 11→6 时锚定 SLAM 位姿的建图仅降 1.60% 精确度 vs 直接用 DA3 降 8.03%；作者自点这对机器人反应式建图与内存受限设备尤为重要
- Quote: “Comparing Table V and Table IV, we observe that our mapping framework is much less affected by reduced batch sizes compared to the direct use of DA3 (−1.60% and −8.03% in precision, respectively). This demonstrates the effectiveness of the proposed scale optimization. Notably, this characteristic is particularly important for devices with limited GPU memory or applications that require reactive mapping where the system must operate without waiting for a large number of incoming images, as is com”
- Authors: yuhao-zhang; yifu-tao; frank-dellaert; et al.

### EA-SLAMCORE-2026-0038

- Claim: 在 7Scenes（seq-01）与 EuRoC VICON 序列的稠密重建评测中，FoundationSLAM 在两子表全部四列指标（ATE/Acc/Comp/Chamfer）上均最优（7Scenes Chamfer 0.047、EuRoC 0.048）；作者将 MASt3R-SLAM 的重建劣化（EuRoC Acc 0.099、Chamfer 0.085）归因于未在灰度数据上训练导致的域差距，并以此论证其方法在快速运动、灰度、宽基线场景的鲁棒性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.25008](https://arxiv.org/abs/2512.25008) FoundationSLAM: Unleashing the Power of Depth Foundation Models for End-to-End Dense Visual SLAM
- Locator: page 6, Table 4
- Evidence: Table 4 上子表（7Scenes）：Ours 0.043/0.039/0.055/0.047 全列低于 DROID-SLAM、MASt3R-SLAM、VGGT-SLAM*；下子表（EuRoC）：Ours 0.019/0.035/0.063/0.048 优于 DROID-SLAM 与 MASt3R-SLAM；MASt3R-SLAM 域差距归因见正文。
- Quote: “In contrast, MASt3R-SLAM shows poor reconstruction quality, likely due to the do- main gap caused by its lack of training on grayscale data. These results demonstrate the robustness of our method in fast-motion, grayscale scenes with wide baselines.”
- Authors: yuchen-wu; jiahe-li; fabio-tosi; et al.

### EA-SLAMCORE-2026-0194

- Claim: 本文全部定量评估仅在 Replica（高质量合成 RGB-D）与 TUM-RGBD（真实世界序列、含显著噪声与深度缺失）两个标准 SLAM 基准上进行；论文虽以具身 AI 的 LLM 推理引擎为动机并演示文本驱动 3D 查询，但不含任何机器人本体或操作/导航/空间问答等具身下游任务的闭环验证——其'SLAM 支撑具身智能'的定位停留在动机与感知层演示。
- Stance: `conditional` | Confidence: `inference`
- Paper: [2602.06991](https://arxiv.org/abs/2602.06991) LangGS-SLAM: Real-Time Language-Feature Gaussian Splatting SLAM
- Locator: page 8, Section 4.1 Experimental Setup
- Evidence: 评估范围限于 Replica/TUM-RGBD 基准，无机器人或具身下游任务闭环
- Quote: “Datasets. We evaluate on Replica [33] and TUM-RGBD [34]. Replica provides high- quality synthetic RGB-D data, whereas TUM-RGBD offers real-world sequences with substantial noise and frequent depth missing regions.”
- Authors: seongbo-ha; sibaek-lee; kyungsu-kang; et al.

### EA-SLAMCORE-2026-0182

- Claim: 作者对 3D 视觉基础模型（DUSt3R/MASt3R/VGGT）的定位陈述：它们以统一可微框架联合推断相机位姿、内参与稠密几何，开创了变革性范式，使从原始图像数据做免标定重建成为可能，'让无约束环境中的 SLAM 成为切实可行'（引 MASt3R-SLAM, Murai et al., 2025）；同一句群随即指出其 Transformer 架构的二次复杂度带来严重内存约束与计算瓶颈。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 1, Sec 1 Introduction
- Evidence: 基础模型被定位为免标定 SLAM 的使能者（联合推断位姿/内参/稠密几何），SLAM 框架保留但内部被重写
- Quote: “The emergence of 3D vision foundation models, such as DUSt3R (Wang et al., 2024), MASt3R (Leroy et al., 2024) and VGGT (Wang et al., 2025a), have introduced a trans- formative paradigm by jointly inferring camera pose, in- trinsics, and dense geometry within unified differentiable frameworks. These models enable calibration-free recon- struction from raw image data, making SLAM in uncon- strained environments a tangible possibility (Murai et al., 2025).”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0187

- Claim: KITTI 主结果（Table 1）中经典标定 SLAM 与免标定基础模型 SLAM 的精度对比：在供真值内参的上界比较设置下，ORB-SLAM2 带回环时 Avg 54.82 m / Avg* 9.46 m（不带回环为 69.73 / 26.48），免标定的 VGGT-Motion（Ours）Avg 24.17 m / Avg* 18.26 m——含高速 Seq 01 的整体平均上 VGGT-Motion 更优，但剔除 Seq 01 的常规序列平均（Avg*）上 ORB-SLAM2+回环仍有约 2 倍精度优势；作者的整体表述为 VGGT-Motion 与 VGGT-Long 可靠扩展并'匹敌使用 GT 内参的标定基线'。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 7, Table 1（KITTI ATE RMSE 对照）
- Evidence: KITTI：ORB-SLAM2+LC（GT 内参）Avg* 9.46 vs Ours 18.26（常规序列经典仍领先）；整体 Avg 54.82 vs 24.17（免标定反超）
- Quote: “ORB-SLAM2 × 40.65 502.20 47.82 0.94 1.30 29.95 40.82 16.04 43.09 38.77 5.42 69.73 26.48 ORB-SLAM2 ✓ 6.03 508.34 14.76 1.02 1.57 4.04 11.16 2.19 38.85 8.39 6.63 54.82 9.46”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0189

- Claim: 作者对本文意义的元判断（附录 B.2）：结果凸显单目 SLAM 的根本转变——全局一致性不再仅靠越来越复杂的优化后端实现，而是可以通过显式尊重运动动态并利用现代基础模型提供的强结构先验达成；这一视角表明大规模鲁棒性不仅是优化问题，也是表征与运动感知问题。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 13, Appendix B.2 Discussion
- Evidence: 作者自判根本转变：全局一致性靠运动感知+基础模型结构先验，而非更复杂的优化后端；框架成为可换骨干的'壳'
- Quote: “The results presented in this work highlight a fundamental shift in monocular SLAM. Rather than relying solely on increasingly complex optimization backends, global consistency can be achieved by explicitly respecting motion dynamics and leveraging strong structural priors provided by modern foundation models. This perspective suggests that robustness at scale is not only an optimization problem, but also a representation and motion-awareness problem.”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0190

- Claim: 面向具身智能的演化方向（作者展望，附录 B.2 末段）：Anysplat 与 Depth Anything-v3 等新模型可直接从单目输入预测 3D Gaussian Splatting (3DGS) 参数；以这类表征替换中间点云后，本框架能够以完全前馈的方式生成高保真地图，支撑实时新视角合成与机器人/具身智能中更丰富的下游应用，超越传统稀疏或稠密点云地图（Figure 10 展示前馈 3DGS 模型与渲染结果）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 15, Appendix B.2（Evolution Toward Renderable Scene Representations 段）
- Evidence: SLAM 输出向前馈 3DGS 可渲染地图演化，定位服务机器人/具身智能下游（仅展望+单例展示，无任务验证）
- Quote: “By replacing intermediate point clouds with such representations, our framework can generate high-fidelity maps in a fully feed-forward manner. As illustrated in Figure 10, this evolution supports real-time novel-view synthesis and richer downstream applications in robotics and embodied AI, moving beyond traditional sparse or dense point cloud maps.”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0059

- Claim: LAMP 的隐式语言地图以相机位姿 x=[t,q] 为神经网络的输入域：问题定义显式假定机器人已'充分遍历环境、采集位姿-图像对'，且环境静态（M 不再变化）——位姿获取被前置为已解决问题，隐式表示替代的是地图的存储与表达方式，而非定位能力本身
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.11862](https://arxiv.org/abs/2602.11862) LAMP: Implicit Language Map for Robot Navigation
- Locator: page 3
- Evidence: Sec III-A/III-B1：F_Θ: x↦z 的定义域是 7 维位姿；'To construct M, we assume that the robot has traversed the environment extensively, collecting (x, I) pairs'；问题定义要求 'this static environment (i.e., M does not change)'。全文未讨论位姿估计误差或位姿来源。
- Quote: “To construct M, we assume that the robot has traversed the environment extensively, collecting (x, I) pairs, where x represents the camera pose and I is the corresponding image.”
- Authors: sibaek-lee; hyeonwoo-yu; giseop-kim; et al.

### EA-SLAMCORE-2026-0091

- Claim: 作者在自采集数据上做了初步机器人验证：1.8 m 路径上以人形机器人运动学为真值 ATE RMSE 0.02 m、以协作臂正向运动学为真值 ATE RMSE 0.01 m（OAK-1 相机）；406.8 m GoPro 路径以 2 m 精度 GPS 为真值 ATE RMSE 18±2 m。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.06830](https://arxiv.org/abs/2604.06830) VGGT-SLAM++
- Locator: page 7, Fig. 6
- Evidence: 具身证据限于 1.8 m 短路径（人形/协作臂运动学真值，ATE 0.02/0.01 m），无下游任务
- Quote: “(A) custom data (406.8m) recorded by GoPro HERO10 camera with GPS groundtruth with 2m precision. (ATE RMSE 18 ± 2 m); (B) custom data (1.8m) recorded by a OAK-1 camera with a Humanoid robot kinematics groundtruth (ATE RMSE 0.02m); (C) custom data (1.8m) recorded by a OAK-1 camera with Cobot forward kinematics groundtruth (ATE RMSE 0.01m)”
- Authors: avilasha-mandal; rajesh-kumar; sudarshan-sunil-harithas; et al.

### EA-SLAMCORE-2026-0092

- Claim: 运行剖面：VGGT-SLAM++ 前端约 16 FPS、空间校正后端 1.89 FPS，内存占用约 8 GB RAM 与 20 GB VRAM（NVIDIA RTX 4090 24GB），作者称内存有界并与 DROID-SLAM 的 8GB 前端 + 24GB 后端配置对比。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.06830](https://arxiv.org/abs/2604.06830) VGGT-SLAM++
- Locator: page 6
- Evidence: 前端 16 FPS / 后端 1.89 FPS、约 20 GB VRAM（RTX 4090）——近实时但非边缘级
- Quote: “The VGGT-SLAM++ front- end runs at ∼16 FPS and it’s spatially corrective back-end runs at 1.89 FPS, with bounded memory usage (∼8 GB RAM, ∼20 GB VRAM), averaged across datasets referred in Tables 1, 4, 3, and 2, showing bounded memory com- pared to prior work like DROID-SLAM [77 ] with 8GB front-end and 24GB back-end.”
- Authors: avilasha-mandal; rajesh-kumar; sudarshan-sunil-harithas; et al.

### EA-SLAMCORE-2026-0203

- Claim: 专家消融（Isaac Sim 办公环境找大罐子任务、15 试验、未探索地图设定）：单独使用语义地图专家失败——因为它依赖足够填充的场景字典，没有先行探索时语义推理是欠约束的；单独 egocentric VLM 成功率 67%，CMAB 在全部试验中达到 100% 成功率。CMAB 的动作分布随覆盖度自然演化：低覆盖阶段 frontier 探索占 63.6%，高覆盖阶段转向语义地图专家 55.9% 与 ego-VLM 41.2%、frontier 降至 2.9%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26046](https://arxiv.org/abs/2606.26046) RoboAtlas: Contextual Active SLAM
- Locator: page 13, Section V-B2 CMAB Validation 与 Policy Adaptation 段
- Evidence: 语义地图专家冷启动失败（欠约束）；CMAB 100% vs ego-VLM 67%；低覆盖 frontier 63.6% → 高覆盖语义 55.9%+VLM 41.2%
- Quote: “Frontier exploration consistently succeeds but is inefficient, as the robot explores nearly the entire map before locating the target. In contrast, the semantic map expert fails in this setting because it relies on a sufficiently populated scene dictionary; without prior exploration, semantic reasoning is under-constrained. The egocentric VLM exhibits more variable behavior: in some cases it identifies semantically meaningful structures (e.g., doorways) that accelerate discovery, while in others”
- Authors: alexander-schperberg; shivam-k-panda; abraham-p-vinod; et al.

### EA-SLAMCORE-2026-0128

- Claim: 任务条件化的代价：随各组件启用、预算从背景重分配到 ROI，ROI PSNR 单调上升的同时全图 PSNR 温和下降——作者称之为任务条件化建图的预期权衡（intended tradeoff）。即任务条件化地图以牺牲通用重建的全局保真度为代价；作者在讨论节补充：收益与任务区域-全场景的不对称性成正比，任务覆盖全图时系统优雅退化为近均匀建图（附少量注意开销）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30809](https://arxiv.org/abs/2606.30809) GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Robotic Mapping
- Locator: page 6, Section IV-C, Fig. 5
- Evidence: ROI PSNR 单调升、全图 PSNR 温和降——任务条件化以全局保真度为代价，收益取决于任务-场景不对称性
- Quote: “ROI PSNR rises monotonically, while full-image PSNR drops modestly as budget is reallocated away from the background, which is the intended tradeoff of task-conditioned mapping.”
- Authors: annika-thomas; mason-peterson; jonathan-p-how

### EA-SLAMCORE-2026-0028

- Claim: 编码器适应消融（Fig. 4，定性）：冻结的预训练编码器无法产生有意义的目标定位结果——其静态特征不能适应特定场景；场景自适应编码器成功定位目标。作者由此得出'持续在线学习对我们的开放词汇能力至关重要'。该结论基于定性图示对比，未报告定量指标。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.16144](https://arxiv.org/abs/2511.16144) LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM
- Locator: page 6, Section IV-C.1, Fig. 4
- Evidence: 冻结预训练编码器无法定位目标；作者称持续在线学习对开放词汇能力至关重要（定性消融）
- Quote: “As visualized in Fig. 4, the frozen encoder fails to produce meaningful localization results, as its static features cannot adapt to the specific scene, whereas our scene-adaptive encoder successfully localizes the object. This shows that continuous online learning is essential for our open-vocabulary capability.”
- Authors: sibaek-lee; seongbo-ha; kyeongsu-kang; et al.

### EA-SLAMCORE-2026-0184

- Claim: 锚点驱动直接 Sim(3) 配准以 VGGT 点图替代经典描述子匹配：作者称传统描述子匹配（ORB/SIFT）在低纹理驾驶场景脆弱且带来二次 O(N²) 代价，本文从 VGGT 点图导出稠密、免搜索的几何对应来施加 Sim(3) 约束，该设计取得 O(N) 复杂度（对有效像素线性），实现快速可靠的子图对齐。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.05508](https://arxiv.org/abs/2602.05508) VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency
- Locator: page 4, Sec 3.2 Anchor-Driven Direct Sim(3) Registration
- Evidence: ORB/SIFT 描述子匹配被 VGGT 点图像素索引稠密对应替代（O(N²)→O(N)），但 Sim(3) 估计与验证框架保留
- Quote: “Conven- tional descriptor matching (e.g., ORB (Rublee et al., 2011) or SIFT (Lowe, 2004)) is brittle in low-texture driving scenes and incurs quadratic O(N 2 ) cost. In contrast, we derive dense, search-free geometric correspondences from VGGT point maps to impose robust Sim(3) constraints. This design yields O(N ) complexity (linear in valid pixels), enabling fast and reliable submap alignment.”
- Authors: zhuang-xiong; chen-zhang; qingshan-xu; et al.

### EA-SLAMCORE-2026-0060

- Claim: 作者自述核心局限是 VLM 依赖：视觉特征相似的其他物体会导致选错节点，目标外观弱或语义模糊时难以正确识别——语义地图的可靠性上限由其 VLM 前端决定
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.11862](https://arxiv.org/abs/2602.11862) LAMP: Implicit Language Map for Robot Navigation
- Locator: page 7
- Evidence: Sec IV-C 末段原文：'Its effectiveness depends on the VLM's accuracy. For instance, if other objects share similar visual features with the target, the model may mistakenly select wrong nodes.'。
- Quote: “Its effec- tiveness depends on the VLM’s accuracy. For instance, if other objects share similar visual features with the target, the model may mistakenly select wrong nodes.”
- Authors: sibaek-lee; hyeonwoo-yu; giseop-kim; et al.

### EA-SLAMCORE-2026-0062

- Claim: 在 ScaleMaster 大尺度复杂室内序列上，三个代表性深度单目 SLAM 系统（官方实现）出现严重尺度失效：LargeHall 01（884.12 m 全楼环游，page 4 Table II）上 DROID-SLAM ATE 89.35 m、MASt3R-SLAM 80.54 m（calibrated 模式 91.62 m）；Parking 01 上 MASt3R-SLAM 32.37 m；Stairs 01 上 DROID-SLAM 20.20 m。VGGT-SLAM 在 25 条序列中的 17 条上因无效位姿更新（SL(4) 归一化负行列式）终止、ATE 无定义。而同批系统在 ARKitScenes 小尺度室内序列上平均 ATE 仅 0.32/0.24/0.09/0.05 m（Table III，同页）。作者将 LargeHall 01 的误差归因于长轨迹上的累计尺度漂移而非随机跟踪丢失（page 5）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.18174](https://arxiv.org/abs/2602.18174) Have We Mastered Scale in Deep Monocular Visual SLAM? The ScaleMaster Dataset and Benchmark
- Locator: page 6, Tables III-IV
- Evidence: SOTA 深度单目 SLAM 在楼宇尺度 ATE 达数十米级，VGGT-SLAM 17/25 序列运行失败
- Quote: “LargeHall 01 89.35 – 80.54 91.62 LargeHall 02 3.78 21.69 6.12 5.89 LargeHall 03 13.21 – 1.99 1.96 LargeHall 04 4.01 1.12 0.57 0.92 LargeHall 05 0.56 0.51 0.45 0.33 Library 01 1.68 – 5.29 3.61 Library 02 1.45 – 0.54 0.63 Library 03 0.09 – 0.09 0.06 Library 04 4.86 – 3.54 3.22 Library 05 4.35 13.26 3.08 4.00 Library 06 0.05 – 0.05 0.04 Library 07 0.13 0.22 0.13 0.12 Library 08 0.09 – 0.09 0.06 Library 09 0.04 – 0.07 0.05 Lobby 01 0.76 3.18 0.54 0.27 Lounge 01 4.51 – 0.47 0.16 Office 01 5.61 – 8.03”
- Authors: hyoseok-ju; bokeon-suh; giseop-kim

### EA-SLAMCORE-2026-0063

- Claim: 位姿误差低不保证地图正确：MASt3R-SLAM 在 Library 07 序列上 ATE 仅 0.12 m（Table IV），但稠密地图灾难性失效——对应距离阈值 1 m 时 89.1% 的地图点被作为外点丢弃，阈值放大到 10 m 时 Chamfer 距离达 9.99 m（近全图塌缩，Table V）；对照 Library 06（ATE 0.04 m）在 10 m 阈值下 Chamfer 仅 0.10 m、Drop Rate 0.0%。作者结论：这种尺度一致性感知的重建失效对 ATE 根本不可见、仅被地图质量指标捕捉，单靠轨迹误差（即使经单一全局尺度调整）不足以评估稠密 SLAM。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.18174](https://arxiv.org/abs/2602.18174) Have We Mastered Scale in Deep Monocular Visual SLAM? The ScaleMaster Dataset and Benchmark
- Locator: page 6, Table V 与 Section V-C
- Evidence: Library 07：ATE 仅 0.12 m 但 89.1% 地图点被丢弃、Chamfer 9.99 m——地图级尺度失效对 ATE 不可见
- Quote: “Catastrophic Failure Case: In contrast, Fig. 6 shows that the Library 07 sequence suffers a geometric failure even though the pose error is low (0.12 m in Table IV). With the correspondence distance threshold set to 1 m, 89.1% of the generated map points were dis- carded as outliers, and when the threshold was increased to 10 m, the Chamfer distance reached a massive 9.99 m. This scale consistency-aware reconstruction failure is fundamentally invisible to ATE but is captured perfectly by the map”
- Authors: hyoseok-ju; bokeon-suh; giseop-kim

### EA-SLAMCORE-2026-0081

- Claim: 作者自述局限：不确定性优化依赖帧到帧对齐，在 SLAM 初始化阶段位姿仍不可靠时会导致不确定性估计不准确；作者提出引入重建先验或可提升初始化阶段的鲁棒性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.19076](https://arxiv.org/abs/2603.19076) DROID-SLAM in the Wild
- Locator: page 8, Sec. 5 Limitations
- Evidence: 作者自述局限：初始化阶段（位姿尚不可靠时）不确定性估计可能不准确。
- Quote: “Our uncertainty optimization relies on frame- to-frame alignment, which can lead to inaccurate uncertainty estimation during SLAM initialization when pose estimates are still unreliable. Incorporating reconstruction priors could improve the robustness of the initialization stage.”
- Authors: moyang-li; zihan-zhu; marc-pollefeys; et al.

### EA-SLAMCORE-2026-0090

- Claim: 在未标定灰度数据集 EuRoC MAV（MH01-MH05）上，VGGT-SLAM++ 平均 ATE RMSE 为 2.666 m，而 DROID-SLAM 为 0.027 m、VGGT-SLAM (Sim(3)) 为 2.938 m；作者承认其在前端依赖特征跟踪或光流的经典管线面前欠佳，并归因于 VGGT 仅在 RGB 数据上训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.06830](https://arxiv.org/abs/2604.06830) VGGT-SLAM++
- Locator: page 13, Table 6
- Evidence: 灰度 EuRoC 上 VGGT-SLAM++（2.666 m）比 DROID-SLAM（0.027 m）差约两个数量级
- Quote: “DROID-SLAM [77] ✓ 0.013 0.014 0.022 0.043 0.043 0.027 VGGT-SLAM (Sim(3)) [50] ✓ 1.740 2.890 2.270 3.390 4.400 2.938 VGGT-SLAM (SL(4)) [50] ✓ 3.780 3.960 3.710 – – N/A VGGT-SLAM++ (Ours) ✓ 1.600 2.700 1.900 2.980 4.150 2.666”
- Authors: avilasha-mandal; rajesh-kumar; sudarshan-sunil-harithas; et al.

### EA-SLAMCORE-2026-0102

- Claim: 作者自述局限（以未来工作形式表述）：当前 GGD-SLAM 尚未实现对动态物体运动的实时重建，也尚未解决完全被遮挡区域的 inpainting；系统的设计取向是在保证静态场景稳定的前提下处理动态干扰。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.12837](https://arxiv.org/abs/2604.12837) GGD-SLAM: Monocular 3DGS SLAM Powered by Generalizable Motion Model for Dynamic Environments
- Locator: page 8
- Evidence: 作者自述：尚未支持动态物体运动的实时重建与完全遮挡区域的 inpainting。
- Quote: “In the future, we aim to develop a method for real-time reconstruction of dynamic object motion and inpainting of fully occluded regions, while ensuring the stability of the static scene.”
- Authors: yi-liu; haoxuan-xu; hongbo-duan; et al.

### EA-SLAMCORE-2026-0109

- Claim: 在第二批（更高角速度 + HDR/低光照）序列上，事件-only 的 SDEVO 平均 ATE 0.921 m 与速度精度 AUC 0.663 均劣于帧相机 DPVO（0.603 m / 0.676），多个 HDR/低光序列差距悬殊（drone 8 hdr：1.935 vs 0.352 m；arm hdr：0.512 vs 0.087 m；car circle hdr：1.713 vs 0.380 m），例外是 drone s 两序列（DPVO 的 ATE 反而更大：1.743/2.300 vs 1.502/2.044）。事件-帧-IMU 融合的 ESVIO 在第二批平均最优（ATE 0.512 m / AUC 0.710，帧 VINS-Fusion 最差 1.103 m / 0.593）。作者据此提出：事件相机在 HDR 与高速机动同时存在的场景存在潜在局限（论述见 page 11）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.24033](https://arxiv.org/abs/2604.24033) Event-based SLAM Benchmark for High-Speed Maneuvers
- Locator: page 12, Table VIII
- Evidence: HDR+高速并存时事件-only SLAM 劣于帧相机（SDEVO 平均 ATE 0.921 vs DPVO 0.603 m），融合方案最优
- Quote: “TABLE VIII: Results of SOTA event-based SLAM methods on the second batch of sequences [ATE:(m), AUC:(-)]. Method ESVIO [20] SDEVO [29] VINS [37] DPVO [44] Stereo EVIO Stereo EO Stereo VIO Mono VO Sequence ATE / AUC ATE / AUC ATE / AUC ATE / AUC drone 8 norm 0.403 / 0.934 0.881 / 0.880 1.031 / 0.921 0.333 / 0.943 drone 8 hdr 0.876 / 0.922 1.935 / 0.818 1.732 / 0.767 0.352 / 0.928 drone s norm 0.639 / 0.899 1.502 / 0.772 1.029 / 0.759 1.743 / 0.674 drone s hdr 0.445 / 0.822 2.044 / 0.691 2.425 /”
- Authors: sheng-zhong; junkai-niu; guillermo-gallego; et al.

### EA-SLAMCORE-2026-0205

- Claim: 评测设定的边界事实：GOAT-Bench 大规模评测在 Habitat 中进行，模拟器直接提供真值 agent 位姿与渲染的 RGB-D 观测，因此 SLAM Toolbox 定位被绕过——RoboAtlas 消费模拟器位姿构建 3D 语义地图与 Scene-Dictionary，目标由 Habitat agent 的导航接口执行；作者同时指出多数相关工作只在 Habitat 做基准，这抽象掉了物理部署的主要挑战：有界计算预算下的实时推理与规划、有噪里程计与真实世界 SLAM 的定位漂移、有噪深度感知、执行与足印约束、连续大规模运行时有界机载 GPU 显存。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.26046](https://arxiv.org/abs/2606.26046) RoboAtlas: Contextual Active SLAM
- Locator: page 11, Section V-A Habitat 段
- Evidence: GOAT-Bench 评测用真值位姿、SLAM Toolbox 定位被绕过；作者批评 Habitat 基准文化抽象掉真实世界 SLAM 漂移等部署挑战
- Quote: “Here the simulator provides ground-truth agent pose and rendered RGB-D obser- vations directly, so SLAM Toolbox localization is bypassed. RoboAtlas consumes the simulator pose and RGB-D render, builds the 3D semantic map and Scene-Dictionary as before, and issues goals that are executed by the Habitat agent’s navigation interface rather than Nav2. We note that most related works benchmark exclusively in Habitat, which abstracts away the principal challenges of physical deployment: real-time infe”
- Authors: alexander-schperberg; shivam-k-panda; abraham-p-vinod; et al.

### EA-SLAMCORE-2026-0129

- Claim: 作者明确承认的关键局限：当前系统在任务中途改变时不重新分配预算——欠重建的区域无法追溯精化，除非重新观测或离线进一步精化。同段另承认三项：空间谓词评估依赖渲染深度、深度严重噪声时可能误判；LLM 解析器在异常措辞下可能幻觉出目标对象；仅在少量任务措辞上评估、未覆盖自然语言变化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30809](https://arxiv.org/abs/2606.30809) GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Robotic Mapping
- Locator: page 7, Section V Discussion and Limitations
- Evidence: 作者自陈：任务中途改变不重分配预算、欠重建区域需重观测；另有深度噪声误判、LLM 幻觉、措辞覆盖窄三项局限
- Quote: “Finally, the current system does not re-allocate budget when the task changes mid- sequence: regions that were under-reconstructed cannot be retroactively refined without re-observing them or conducting further refinement offline.”
- Authors: annika-thomas; mason-peterson; jonathan-p-how

### EA-SLAMCORE-2026-0025

- Claim: 作者在引言中断言：3DGS-SLAM 产出的光度真实感地图'缺乏使 embodied AI 执行多样下游任务所需的语义理解'（所引 [5][6][7] 为 Clip-Fields、LAMP、LM-NAV 等机器人工作）；摘要中的平行表述为'缺乏机器人交互所需的开放词汇语义理解'。即论文以'SLAM 地图与具身任务需求之间的语义缺口'作为全部研究的出发点。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.16144](https://arxiv.org/abs/2511.16144) LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM
- Locator: page 1, Section I Introduction
- Evidence: 作者自陈：光度真实感 SLAM 地图缺乏 embodied AI 下游任务所需的语义理解
- Quote: “However, such photorealistic maps lack the semantic understanding required for enabling embodied AI to perform diverse down- stream tasks [5], [6], [7].”
- Authors: sibaek-lee; seongbo-ha; kyeongsu-kang; et al.

### EA-SLAMCORE-2026-0135

- Claim: SuperMap 类级分割精度不占优：ScanNet mIoU 27.42（无背景）低于 RayFronts 41.29——系统以类级精度换取实例级时空一致性，作者明确声明设计目标不是最大化逐帧分割分数
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.22896](https://arxiv.org/abs/2608.22896) SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation
- Locator: page 6
- Evidence: Table II 类级对比：SuperMap 27.42/43.50/55.48（mIoU/f-mIoU/Acc）vs RayFronts 41.29/46.42/56.76。
- Quote: “RayFronts [1] 41.29 46.42 56.76 32.29 39.04 49.15 ConceptGraphs [5] object-level 21.62 24.32 31.05 20.83 23.61 35.80 HOV-SG [30] 26.79 36.05 35.17 23.48 28.92 38.52 SuperMap (Ours) 27.42 43.50 55.48 22.61 29.10 33.00”
- Authors: shibo-zhao; guofei-chen; honghao-zhu; et al.

### EA-SLAMCORE-2026-0136

- Claim: 作者自述局限：高度动态物体的跟踪性能仍然受限；且开放词汇 2D 检测依赖预定义物体提示词列表，缺乏自动开放世界物体发现机制——系统尚不能在无语义先验的真正新颖环境中运行
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.22896](https://arxiv.org/abs/2608.22896) SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation
- Locator: page 8
- Evidence: LIMITATION 节两条自述：动态物体跟踪 + 提示词列表依赖。
- Quote: “its performance in tracking highly dynamic objects remains limited. Future iterations could address this by incorporating specialized tracking-by-detection modules or efficient segmentation-based tracking to improve temporal coherence.”
- Authors: shibo-zhao; guofei-chen; honghao-zhu; et al.

### EA-SLAMCORE-2026-0065

- Claim: 跨会话尺度歧义的实证缺口：将单段视频作为三个独立会话分别运行 MASt3R-SLAM，得到的三个地图碎片各自内部自洽、但以互不一致的尺度生成，无法对齐合并为单一全局尺度一致的地图；作者将其定位为长期建图或协同 SLAM 的主要挑战。
- Stance: `gap` | Confidence: `direct`
- Paper: [2602.18174](https://arxiv.org/abs/2602.18174) Have We Mastered Scale in Deep Monocular Visual SLAM? The ScaleMaster Dataset and Benchmark
- Locator: page 7, Section V-D Inter-session Scale Ambiguity（Fig. 9）
- Evidence: 同一视频按三会话切分后地图碎片尺度互不一致、无法合并——跨会话尺度一致性是未解决缺口
- Quote: “Inter-session Scale Ambiguity: Fig. 9 demonstrates another critical issue. When a single video is processed as three inde- pendent sessions, each resulting map fragment is generated at a different, inconsistent scale. While internally coherent, they cannot be merged into a single, globally scale-consistent map, highlighting a major challenge for long-term mapping or collaborative SLAM.”
- Authors: hyoseok-ju; bokeon-suh; giseop-kim

### EA-SLAMCORE-2026-0112

- Claim: 学习型事件 SLAM 的部署边界：作者指出（运行时分析）部分数据驱动方法在 VGA 分辨率事件数据上已能在桌面级 GPU 达到一定实时性、甚至超过部分 model-based 方法，但这些方法严重依赖高性能 GPU，部署到功耗受限的嵌入式平台时计算延迟显著增加；事件表征构建成本与事件量线性相关、传输开销未计入分析；作者结论是'这些方法与实际应用所需的实时性能之间仍有相当差距'，更高分辨率事件数据远超当前事件 SLAM 方法的能力（句子续接于 page 13）。
- Stance: `gap` | Confidence: `direct`
- Paper: [2604.24033](https://arxiv.org/abs/2604.24033) Event-based SLAM Benchmark for High-Speed Maneuvers
- Locator: page 12, Section V-C Runtime Analysis
- Evidence: 学习型事件 SLAM 仅在桌面级 GPU 接近实时，嵌入式部署与实际应用实时性仍有相当差距
- Quote: “Although Tab. IX suggests that some current data-driven deep learning methods demonstrate a certain level of real-time performance on VGA-resolution event data, even outperform- ing some model-based methods, it is important to note that these methods heavily rely on high-performance GPUs. When deployed on power-constrained embedded platforms, their computational latency increases significantly [29]. In addition, although the front-end runtime of learning-based methods is generally not sensitive”
- Authors: sheng-zhong; junkai-niu; guillermo-gallego; et al.

### EA-SLAMCORE-2026-0130

- Claim: 评估协议：全部定量结果为按任务相关性分层的渲染质量——在人工标注的 ROI 掩码内计算 PSNR/SSIM/LPIPS（各方法高斯数被 cap 在 Replica 1M / Campus 3M，并受 RTX 4070 Laptop GPU 实时约束）。三类任务（manipulation/search/navigation）仅作为建图的条件规格存在，论文没有任何机器人策略实际消费该地图完成操作/导航任务的闭环实验。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.30809](https://arxiv.org/abs/2606.30809) GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Robotic Mapping
- Locator: page 5, Section IV-A.4 Metrics
- Evidence: 评估全部为人工标注 ROI 内的渲染指标，无任何下游任务执行闭环
- Quote: “We report rendering quality stratified by task relevance using hand-annotated ROI masks including PSNR, SSIM, LPIPS computed within ground-truth task-relevant masks only.”
- Authors: annika-thomas; mason-peterson; jonathan-p-how

### EA-SLAMCORE-2026-0030

- Claim: 本文全部定量评估限于三个标准 SLAM/重建基准（合成 Replica、真实 TUM-RGBD、ScanNet）上的 SLAM 指标（ATE、PSNR/SSIM/LPIPS、开放词汇 mIoU/Accuracy、FPS）与消融；论文不含任何机器人平台实验或下游具身任务（操作、导航、数据采集）评估——摘要与引言中'服务 embodied AI/机器人交互'的定位没有任务级验证，仅由引用机器人导航工作（Clip-Fields/LAMP/LM-NAV）支撑。
- Stance: `gap` | Confidence: `direct`
- Paper: [2511.16144](https://arxiv.org/abs/2511.16144) LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM
- Locator: page 4, Section IV-A.1 Datasets and Metrics
- Evidence: 全部实验限于 SLAM 基准（Replica/TUM-RGBD/ScanNet），无机器人或具身下游任务验证
- Quote: “We evaluate our framework on the synthetic Replica dataset [25] and the real-world TUM-RGBD [26] and ScanNet [1] datasets.”
- Authors: sibaek-lee; seongbo-ha; kyeongsu-kang; et al.

### EA-SLAMCORE-2026-0119

- Claim: 本文全部定量评估限于 SLAM/重建指标（ATE、precision/recall、重建误差）于 SLAM 数据集（EuRoC/ScaRF/KITTI/Oxford Spires）；唯一的机器人实验是 ANYmal-D 四足平台采集数据（含室内外过渡与高约束空间）的定性评估——仅演示多会话、多相机（前后）、多模态（视觉-惯性）稠密 SLAM 的框架灵活性与'实际机器人场景中的可靠运行'，无任何定量指标，也无任何下游具身任务（操作、导航策略、空间推理）消费该地图。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.00307](https://arxiv.org/abs/2606.00307) ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical Visual SLAM
- Locator: page 7, Section V-E Robot Experiment
- Evidence: 全部定量结果为 SLAM/重建指标；唯一机器人实验（ANYmal-D 四足）仅定性演示，无具身下游任务消费地图
- Quote: “Our final experiment qualitatively evaluates ScaRF-SLAM using data collected by a quadruped robot (ANYmal-D) car- rying an Insta360 camera, including an outdoor-indoor tran- sition and operation in highly confined spaces. It showcases multi-session, multi-camera (front and rear), and multi-modal (visual-inertial) SLAM with our system, highlighting the flexi- bility of the proposed decoupled framework and demonstrating its reliable operation in practical robotic scenarios (Fig. 10).”
- Authors: yuhao-zhang; yifu-tao; frank-dellaert; et al.

## References

- `2509.02437` [U-ARM : Ultra low-cost general teleoperation interface for robot manipulation](https://arxiv.org/abs/2509.02437) (2026-03-19)
- `2509.20757` [MASt3R-Fusion: Integrating Feed-Forward Visual Model with IMU, GNSS for High-Functionality SLAM](https://arxiv.org/abs/2509.20757) (2025-11-16)
- `2510.01607` [ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations](https://arxiv.org/abs/2510.01607) (2025-10-02)
- `2510.17439` [From Spatial to Actions: Grounding Vision-Language-Action Model in Spatial Foundation Priors](https://arxiv.org/abs/2510.17439) (2026-03-10)
- `2511.06840` [PanoNav: Mapless Zero-Shot Object Navigation with Panoramic Scene Parsing and Dynamic Memory](https://arxiv.org/abs/2511.06840) (2025-11-10)
- `2511.13719` [Scaling Spatial Intelligence with Multimodal Foundation Models](https://arxiv.org/abs/2511.13719) (2026-03-28)
- `2511.16144` [LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM](https://arxiv.org/abs/2511.16144) (2026-07-14)
- `2511.17792` [Target-Bench: Can Video World Models Achieve Mapless Path Planning with Semantic Targets?](https://arxiv.org/abs/2511.17792) (2026-04-15)
- `2511.22609` [MG-Nav: Dual-Scale Visual Navigation via Sparse Spatial Memory](https://arxiv.org/abs/2511.22609) (2025-11-27)
- `2512.25008` [FoundationSLAM: Unleashing the Power of Depth Foundation Models for End-to-End Dense Visual SLAM](https://arxiv.org/abs/2512.25008) (2026-01-01)
- `2601.05529` [Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models](https://arxiv.org/abs/2601.05529) (2026-04-08)
- `2602.01644` [From Perception to Action: Spatial AI Agents and World Models](https://arxiv.org/abs/2602.01644) (2026-02-02)
- `2602.05508` [VGGT-Motion: Motion-Aware Calibration-Free Monocular SLAM for Long-Range Consistency](https://arxiv.org/abs/2602.05508) (2026-02-05)
- `2602.06991` [LangGS-SLAM: Real-Time Language-Feature Gaussian Splatting SLAM](https://arxiv.org/abs/2602.06991) (2026-01-28)
- `2602.07055` [Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?](https://arxiv.org/abs/2602.07055) (2026-02-04)
- `2602.11862` [LAMP: Implicit Language Map for Robot Navigation](https://arxiv.org/abs/2602.11862) (2026-02-12)
- `2602.17659` [When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs](https://arxiv.org/abs/2602.17659) (2026-07-15)
- `2602.18174` [Have We Mastered Scale in Deep Monocular Visual SLAM? The ScaleMaster Dataset and Benchmark](https://arxiv.org/abs/2602.18174) (2026-02-20)
- `2602.19710` [PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Policies](https://arxiv.org/abs/2602.19710) (2026-07-07)
- `2603.16301` [OGScene3D: Incremental Open-Vocabulary 3D Gaussian Scene Graph Mapping for Scene Understanding](https://arxiv.org/abs/2603.16301) (2026-03-18)
- `2603.19076` [DROID-SLAM in the Wild](https://arxiv.org/abs/2603.19076) (2026-03-19)
- `2603.21577` [Mind over Space: Can Multimodal Large Language Models Mentally Navigate?](https://arxiv.org/abs/2603.21577) (2026-03-23)
- `2604.06830` [VGGT-SLAM++](https://arxiv.org/abs/2604.06830) (2026-04-08)
- `2604.07331` [RoSHI: A Versatile Robot-oriented Suit for Human Data In-the-Wild](https://arxiv.org/abs/2604.07331) (2026-04-08)
- `2604.07957` [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](https://arxiv.org/abs/2604.07957) (2026-04-09)
- `2604.07973` [How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace](https://arxiv.org/abs/2604.07973) (2026-04-09)
- `2604.12837` [GGD-SLAM: Monocular 3DGS SLAM Powered by Generalizable Motion Model for Dynamic Environments](https://arxiv.org/abs/2604.12837) (2026-04-14)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089) (2026-04-15)
- `2604.16482` [A Survey of Spatial Memory Representations for Efficient Robot Navigation](https://arxiv.org/abs/2604.16482) (2026-04-13)
- `2604.24033` [Event-based SLAM Benchmark for High-Speed Maneuvers](https://arxiv.org/abs/2604.24033) (2026-04-27)
- `2605.05945` [MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware](https://arxiv.org/abs/2605.05945) (2026-07-08)
- `2606.00307` [ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical Visual SLAM](https://arxiv.org/abs/2606.00307) (2026-09-01)
- `2606.04907` [WAM-Nav: Asymmetric Latent World-Action Modeling for Unified Visual Navigation](https://arxiv.org/abs/2606.04907) (2026-06-13)
- `2606.14879` [VANDERER: Map-Free Exploration using Future-Aware and Visual-Curiosity-Guided Diffusion Policy](https://arxiv.org/abs/2606.14879) (2026-06-12)
- `2606.26046` [RoboAtlas: Contextual Active SLAM](https://arxiv.org/abs/2606.26046) (2026-06-24)
- `2606.30367` [FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation](https://arxiv.org/abs/2606.30367) (2026-06-29)
- `2606.30809` [GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Robotic Mapping](https://arxiv.org/abs/2606.30809) (2026-06-29)
- `2607.03283` [Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied Intelligence Systems](https://arxiv.org/abs/2607.03283) (2026-07-03)
- `2608.22896` [SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation](https://arxiv.org/abs/2608.22896) (2026-08-24)
