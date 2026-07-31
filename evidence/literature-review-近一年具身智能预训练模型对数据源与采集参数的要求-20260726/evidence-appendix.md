# Evidence Appendix: 近一年具身智能预训练模型对数据源与采集参数的要求

- Time range: 2025-07-26..2026-07-26
- Events: 33
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DQ-YEAR-READ-0008

- Claim: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.01657](https://arxiv.org/abs/2509.01657) Data Retrieval with Importance Weights for Few-Shot Imitation Learning
- Locator: Abstract (full-text section)
- Evidence: IWR 将 retrieval-based imitation learning 的常用最近邻规则解释为目标数据分布 KDE 的极限，指出其高方差、易受噪声影响且不考虑 prior data distribution；方法用目标/先验分布概率比进行 importance-weighted retrieval，并在仿真和 Bridge 真实评估中改善现有检索方法。
- Quote: “Abstract While large-scale robot datasets have propelled recent progress in imitation learning, learning from smaller task specific datasets remains critical for deployment in new environments and unseen tasks. One such approach to few-shot imitation learning is retrieval-based imitation learning, which extracts relevant samples from large, widely available prior datasets to augment a limited demonstration dataset. To determine the relevant data from prior datasets, retrieval-based approaches mo”
- Authors: amber-xie; rahul-chand; dorsa-sadigh; et al.

### EA-DQ-YEAR-READ-0009

- Claim: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.13100](https://arxiv.org/abs/2512.13100) OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning
- Locator: Abstract (full-text section)
- Evidence: 论文指出 OXE 聚合 60 多个机器人数据集，但 top four robot types 占超过 85% 真实数据，带来过拟合风险；OXE-AugE 用 9 种不同机器人本体扩增 16 个 OXE 子集，形成 4.4M trajectories，并研究扩增对 cross-embodiment learning 的影响。
- Quote: “Abstract Large and diverse datasets are needed for training generalist robot policies that have potential to control a variety of robot embodiments—robot arm and gripper combinations—across diverse tasks and environments. As re-collecting demonstrations and retraining for each new hardware platform are prohibitively costly, we show that existing robot data can be augmented for transfer and generalization. The Open X-Embodiment (OXE) dataset, which aggregates demonstrations from over 60 robot dat”
- Authors: guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al.

### EA-EGO-2026-0007

- Claim: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.3 Policy Performance Scales with Pretraining Data Size
- Evidence: 五个数据规模的同架构实验报告单调提升，并限制结论不外推到测量区间之外。
- Quote: “Average task completion rises monotonically from 0.30 at 1k hours to 0.71 at 20k hours”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-DQ-YEAR-READ-0010

- Claim: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation
- Locator: C.4 Retention Balance, Single-Task Curation, and Real-Robot Failure Modes
- Evidence: ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。
- Quote: “To further ablate the role of Multitask Influence Interaction (MII), we visualize the retained task distributions after data curation in Fig. 8 . We consider the six-task real-robot setting with 120 demonstrations per task and an overall retention ratio of 66.7%. Without MII, naively ranking demonstrations with a single global influence score results in a highly skewed retained set: Pick Fruits, Shelf Retrieval, and Wipe Board retain 115, 113, and 104 demonstrations, respectively, whereas Stack”
- Authors: tao-xu; jiaxin-wang; runhao-zhang; et al.

### EA-PRETRAIN-DATA-2026-0003

- Claim: 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16253](https://arxiv.org/abs/2606.16253) SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models
- Locator: 1 Introduction and 3 Method
- Evidence: 论文指出不同机位和图像区域对控制的价值不均匀，SPARC 通过时序 mask 自适应分配比特。
- Quote: “Uniform bitrate allocation across cameras and image regions is therefore fundamentally inefficient.”
- Authors: sangyun-chung; mincheol-shin; jihyun-kim; et al.

### EA-PRETRAIN-DATA-2026-0002

- Claim: 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.17200](https://arxiv.org/abs/2606.17200) ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining
- Locator: 5.3 Human Data for Augmented Fine-Tuning, Figure 6
- Evidence: 419 条人类视频的工作空间覆盖是 34 条机器人示范的 4.8 倍，联合微调将 10 试验成功率从 10% 提高到 40%。
- Quote: “The 419 episodes of task-matched human video spread across 0.296 m 2 , 4.8 broader coverage”
- Authors: hao-li; ganlong-zhao; yufei-liu; et al.

### EA-PRETRAIN-DATA-2026-0005

- Claim: VLA 对压缩往往呈‘轻压缩稳定、越过任务特定转折后骤降’，因此码率验收应看闭环成功曲线，不应只看人眼画质。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.11612](https://arxiv.org/abs/2512.11612) Embodied Image Compression: Towards Codec for Robotic Visual Systems
- Locator: 5.3 Experiment Result and Discussions
- Evidence: 该基准中 RVS 从 0.10 到 0.06 bpp 约下降 5%，约 0.04 bpp 出现转折，0.02 bpp 附近快速失效。
- Quote: “RVS curves stay flat from 0.10 to 0.06 bpp (5% drop), then kink sharply around 0.04 bpp”
- Authors: zhenghao-chen; zijie-yue; haozhe-li; et al.

### EA-PRETRAIN-DATA-2026-0006

- Claim: 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.11612](https://arxiv.org/abs/2512.11612) Embodied Image Compression: Towards Codec for Robotic Visual Systems
- Locator: Appendix C Subjective Data Collection
- Evidence: 真实管线同步记录腕部与第三人称 RealSense、关节角和末端增量动作，频率为 10 Hz。
- Quote: “Joint angles, two camera streams (wrist view and third-person view, captured by two Intel realsense cameras), and actions”
- Authors: zhenghao-chen; zijie-yue; haozhe-li; et al.

### EA-DQ-YEAR-READ-0003

- Claim: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: 3.3 Trajectory and Grasp Filtering via Simulation
- Evidence: PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。
- Quote: “Now that we have converted the human demonstrations into 6 DoF object pose trajectories, the next step is to execute them on a robot in simulation. This serves two purposes. One is to filter out those that may not be suitable for robot learning. There are two main reasons a trajectory may be unsuitable. First, pose estimation errors can lead to inaccurate trajectories. Second, the extracted trajectory may not be physically achievable by the robot. In either case, it would be harmful to train the”
- Authors: albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al.

### EA-EGO-2026-0008

- Claim: 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.2 Large-Scale Human Pretraining Is Key to Strong Dexterous Manipulation Policy Performance
- Evidence: 四类 checkpoint 的消融中，pretrain+midtrain 最好；human pretraining 提供结构，mid-training 负责控制锚定。
- Quote: “combining human pretraining with a small amount of aligned mid-training yields the best overall performance”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-EGO-2026-0011

- Claim: Retargeted ego-human 数据只能部分替代目标机器人示范：在论文的 Make Coffee co-training 实验中，没有 robot data 时成功始终接近 0。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.22264](https://arxiv.org/abs/2603.22264) UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos
- Locator: 5.4 UniDex-Cap for Human-Robot Data Co-train
- Evidence: 作者明确总结 human data helps but robot data is indispensable，并给出约 2:1 的局部替代斜率。
- Quote: “Retargeted human data helps, but robot data is indispensable”
- Authors: gu-zhang; qicheng-xu; haozhe-zhang; et al.

### EA-UMI-READ-0003

- Claim: UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.10647](https://arxiv.org/abs/2604.10647) OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction
- Locator: Abstract (full-text section)
- Evidence: The HTML full text repeatedly identifies limited physical interaction signals as a bottleneck of existing UMI-like systems and proposes synchronized RGB, depth, trajectory, tactile sensing, internal grasping force, and external wrench data to improve contact-rich policy learning.
- Quote: “Abstract UMI-style interfaces enable scalable robot learning, but existing systems remain largely visuomotor, relying primarily on RGB observations and trajectory while providing only limited access to physical interaction signals. This becomes a fundamental limitation in contact-rich manipulation, where success depends on contact dynamics such as tactile interaction, internal grasping force, and external interaction wrench that are difficult to infer from vision alone. We present OmniUMI, a uni”
- Authors: shaqi-luo; yuanyuan-li; youhao-hu; et al.

### EA-EGO-2026-0013

- Claim: Physics refiner 和 interaction reward 是把 Ego-centric 视频数据变成可执行技能的必要中间层；只跟踪运动会在接触任务中失败。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.20373](https://arxiv.org/abs/2605.20373) SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework
- Locator: 4.4 Component Analysis
- Evidence: 组件消融中去除 Refiner 显著退化，去除 interaction reward 时机器人只模仿弯腰而无法抬起物体。
- Quote: “Removing the Refiner leads to substantial performance degradation”
- Authors: tianshu-wu; xiangqi-kong; yue-chen; et al.

### EA-EGO-2026-0014

- Claim: 缩小 human/robot 图像外观差距并不足以让 ego 数据可训练；Water Flowers 消融中 visual-only 最高约 32.5%，显式 hand-object 6DoF ICT 才带来大幅闭环提升。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.24934](https://arxiv.org/abs/2605.24934) HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos
- Locator: 4.4 What Drives Performance of HumanEgo?
- Evidence: raw RGB、inpainting、robot RGB 和 ICT 的阶梯消融把视觉外观与空间关系作用分离。
- Quote: “Monocular RGB encodes appearance , not the 3D spatial relationships that manipulation demands.”
- Authors: zhi-wang; botao-he; kelin-yu; et al.

### EA-EGO-2026-0017

- Claim: 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 4.3 Egocentric Video Yields Effective Pretraining Labels
- Evidence: HOT3D ground truth 上的 10% sample 验证给出 head/wrist 三类严格阈值 recovery rate。
- Quote: “Under the strict tier ( , rot6d L2 ), head recovery reaches 78.82%, with left and right wrist recovery at 65.93% and 61.72%, respectively;”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-EGO-2026-0018

- Claim: 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 4.4 The Head Camera Enables Pretrained Active Perception
- Evidence: Restocking 中 egocentric-pretrained model 的 placement 为 24/27，SFT-only 为 6/27；移除 head camera 降到 1/27。
- Quote: “ActiveMimic scores 24 out of 27 on placement, whereas ActiveMimic sft-only achieves only 6 out of 27”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-PRETRAIN-DATA-2026-0004

- Claim: 带宽要求必须在目标 VLA 和任务上用闭环成功率标定，感知画质或单一固定 bpp 不能替代。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.16253](https://arxiv.org/abs/2606.16253) SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models
- Locator: C.1 Analysis of Key Components
- Evidence: VLABench 中 0.0333/0.0685 bpp 的 SPARC 成功率接近但低于未压缩，而极低 bpp 下所有变体失效。
- Quote: “SPARC (Ours) 0.0333 37.5 0.0685 38.3 Uncompressed - 40.5 - 40.5”
- Authors: sangyun-chung; mincheol-shin; jihyun-kim; et al.

### EA-PRETRAIN-DATA-2026-0001

- Claim: 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.17200](https://arxiv.org/abs/2606.17200) ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining
- Locator: 5.2 Ablation Studies, Figure 5(b)
- Evidence: 三项组件消融均降低 RoboCasa 成功率，其中去掉人类伪动作可靠性加权的降幅最大。
- Quote: “Removing morphology tokens makes the success rate drop from 72.8% to 70.9%”
- Authors: hao-li; ganlong-zhao; yufei-liu; et al.

### EA-EGO-2026-0003

- Claim: 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: III-C Policy Training
- Evidence: 策略训练段明确说明 gripper state 缺失，并以 object pose displacement 作为替代动作。
- Quote: “Because gripper states cannot be obtained from Section III-B , each action is represented by a 9-dimensional vector”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGO-2026-0004

- Claim: Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: IV-C Ablation Study
- Evidence: BGTS=1.0 保留 86,427 episodes 但真实机器人分数低于 BGTS=0.7 的 45,157 episodes。
- Quote: “Setting an appropriate curation threshold is crucial to balancing the scale and quality of our dataset”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGO-2026-0005

- Claim: 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.09013](https://arxiv.org/abs/2602.09013) Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
- Locator: III-B Dexterous Grasp and Manipulation Learning
- Evidence: 方法段明确说明重建运动正确时，机器人—对象交互仍可能因几何误差而无效。
- Quote: “the resulting robot–object interactions are not always physically feasible due to reconstruction errors”
- Authors: hongyi-chen; tony-dong; tiancheng-wu; et al.

### EA-EGO-2026-0006

- Claim: 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.09013](https://arxiv.org/abs/2602.09013) Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
- Locator: V Conclusion, Limitations, and Future Work
- Evidence: 作者在限制段明确列出 dynamic camera 未覆盖；实验段说明对象点云被 LEAP Hand 遮挡时采用固定相对位姿近似。
- Quote: “The current framework assumes static or approximately static camera setups”
- Authors: hongyi-chen; tony-dong; tiancheng-wu; et al.

### EA-EGO-2026-0009

- Claim: Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.6 Hand Action Space Design for Human Pretraining
- Evidence: 动作空间消融中 wrist-only 普遍较差，fingertip mapping 在 Cards/Bottle 等接触敏感任务不稳定。
- Quote: “Small errors in fingertip pose often lead to implausible joint configurations after mapping”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-EGO-2026-0010

- Claim: 将 egocentric hand trajectories 转为机器人可执行数据仍需 human-in-the-loop retargeting：基础坐标/形态偏差和 contact-rich 片段要人工校准。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.22264](https://arxiv.org/abs/2603.22264) UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos
- Locator: 3.2.1 Kinematic Retargeting
- Evidence: 论文的两阶段 retargeting 先自动 IK，再用 GUI 调整 6DoF offset；接触片段需人工复核。
- Quote: “The whole pipeline is a two-stage, human-in-the-loop retargeting procedure”
- Authors: gu-zhang; qicheng-xu; haozhe-zhang; et al.

### EA-UMI-READ-0004

- Claim: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible task distribution.
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: Abstract (full-text section)
- Evidence: The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration data quality under challenging real-world conditions.
- Quote: “Abstract We present UMI-3D, a multimodal extension of the Universal Manipulation Interface (UMI) for robust and scalable data collection in embodied manipulation. While UMI enables portable, wrist-mounted data acquisition, its reliance on monocular visual SLAM makes it vulnerable to occlusions, dynamic scenes, and tracking failures, limiting its applicability in real-world environments. UMI-3D addresses these limitations by introducing a lightweight and low-cost LiDAR sensor tightly integrated i”
- Authors: ziming-wang

### EA-EGO-2026-0012

- Claim: 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.20373](https://arxiv.org/abs/2605.20373) SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework
- Locator: 1 Introduction
- Evidence: 引言直接列出三类误差并说明它们使数据 unsuitable for direct policy learning。
- Quote: “Severe occlusion, contact artifacts, and retargeting errors render this data physically implausible for direct imitation”
- Authors: tianshu-wu; xiangqi-kong; yue-chen; et al.

### EA-EGO-2026-0015

- Claim: HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.24934](https://arxiv.org/abs/2605.24934) HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos
- Locator: 5 Conclusion
- Evidence: 作者在 limitation 段逐项列出 stereo hand tracking、occlusion-robust tracking、cascading failures 和 1 cm plateau。
- Quote: “monocular substitutes drop real-world success sharply”
- Authors: zhi-wang; botao-he; kelin-yu; et al.

### EA-EGO-2026-0016

- Claim: Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 3 Method
- Evidence: 方法段明确说明 current-frame wrist pose 与 first-frame camera path 的坐标差异会混合两类位移。
- Quote: “using these wrist poses directly as action supervision would therefore conflate wrist movement with camera motion”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-DQ-YEAR-READ-0015

- Claim: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06442](https://arxiv.org/abs/2607.06442) SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: Introduction
- Evidence: 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。
- Quote: “Our contributions are as follows: • We propose a primitive-compositional view of trajectory utility, realized by Primitive Discovery and Structural Exposure Allocation, which allocate selection budgets according to reuse-aware primitive and transition exposure under diminishing returns. • We introduce Learning-Friendly Trajectory Selection, which selects medoid trajectories within each composition-pattern bucket to favor central, stable, and predictable realizations for behavior cloning. • We pr”
- Authors: changti-wu; bin-yu; zhaolong-shen; et al.

### EA-ALIGN-READ-0012

- Claim: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: Abstract (full-text section)
- Evidence: 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。
- Quote: “Abstract Industrial automation is at a pivotal moment, as Physical AI is driving a transition from rigid, hand-engineered automation systems toward more flexible and adaptive systems. This shift has created a growing demand for large-scale, real-world robot demonstration data, making teleoperation an increasingly important mechanism for data collection. However, high-quality teleoperated demonstrations remain difficult to obtain in practice, as novice operators often produce episodes that are ta”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

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

### EA-TACTILE-2026-0002

- Claim: HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19161](https://arxiv.org/abs/2606.19161) HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision
- Locator: 6 Limitations and Future Work
- Evidence: 作者在限制章节明确列出硬件/本体覆盖和闭环下游评测缺失。
- Quote: “While these tasks assess structural, cross-modal, and temporal understanding, they do not directly measure downstream robotic performance.”
- Authors: yuzhe-huang; jiaping-wu; jiaming-jiang; et al.

## References

- `2509.01657` [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657) (2025-09-01)
- `2509.21986` [Developing Vision-Language-Action Model from Egocentric Videos](https://arxiv.org/abs/2509.21986) (2025-09-26T07:09:33Z)
- `2512.11612` [Embodied Image Compression: Towards Codec for Robotic Visual Systems](https://arxiv.org/abs/2512.11612) (2025-12-12T18:59:07Z)
- `2512.13100` [OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning](https://arxiv.org/abs/2512.13100) (2025-12-15)
- `2602.09013` [Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction](https://arxiv.org/abs/2602.09013) (2026-02-09T18:56:02Z)
- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2602.16710` [EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data](https://arxiv.org/abs/2602.16710) (2026-02-18T18:59:05Z)
- `2603.22264` [UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos](https://arxiv.org/abs/2603.22264) (2026-03-23T17:49:12Z)
- `2604.10647` [OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction](https://arxiv.org/abs/2604.10647) (2026-04-12)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089) (2026-04-15)
- `2605.20373` [SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework](https://arxiv.org/abs/2605.20373) (2026-05-19T18:24:05Z)
- `2605.24934` [HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos](https://arxiv.org/abs/2605.24934) (2026-05-24T08:26:41Z)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.06194` [ActiveMimic: Egocentric Video Pretraining with Active Perception](https://arxiv.org/abs/2606.06194) (2026-06-04T14:01:01Z)
- `2606.16208` [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208) (2026-06-15)
- `2606.16253` [SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models](https://arxiv.org/abs/2606.16253) (2026-06-15T03:38:29Z)
- `2606.17200` [ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining](https://arxiv.org/abs/2606.17200) (2026-06-15T18:40:18Z)
- `2606.19161` [HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision](https://arxiv.org/abs/2606.19161) (2026-06-17)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
