# Evidence Appendix: 近一年 Ego-centric 数据在具身模型训练中的问题与困难

- Time range: 2025-07-15..2026-07-15
- Events: 26
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-EGO-2026-0007

- Claim: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.3 Policy Performance Scales with Pretraining Data Size
- Evidence: 五个数据规模的同架构实验报告单调提升，并限制结论不外推到测量区间之外。
- Quote: “Average task completion rises monotonically from 0.30 at 1k hours to 0.71 at 20k hours”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-WMDATA-READ-0001

- Claim: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接报告了异构数据组成与 modality-specific supervision masks。
- Quote: “Abstract Robotic manipulation requires models that generate executable actions while anticipating and evaluating their future consequences before physical execution. We present -World Model ( -WM), a unified video-action world model that integrates policy learning, video prediction, and action evaluation within a single future-predictive framework. Built on a shared video diffusion backbone, -WM provides two complementary interfaces. First, a video action model jointly predicts future visual lat”
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### EA-DQ-YEAR-READ-0010

- Claim: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation
- Locator: C.4 Retention Balance, Single-Task Curation, and Real-Robot Failure Modes
- Evidence: ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。
- Quote: “To further ablate the role of Multitask Influence Interaction (MII), we visualize the retained task distributions after data curation in Fig. 8 . We consider the six-task real-robot setting with 120 demonstrations per task and an overall retention ratio of 66.7%. Without MII, naively ranking demonstrations with a single global influence score results in a highly skewed retained set: Pick Fruits, Shelf Retrieval, and Wipe Board retain 115, 113, and 104 demonstrations, respectively, whereas Stack”
- Authors: tao-xu; jiaxin-wang; runhao-zhang; et al.

### EA-EGO-2026-0002

- Claim: 该预训练路线依赖 hand/wrist pose 注释，并仍需要中等规模目标机器人数据，因此 raw ego video 的可扩展性与可部署性之间存在结构性张力。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2507.12440](https://arxiv.org/abs/2507.12440) EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
- Locator: 7 Limitation
- Evidence: 作者在限制段同时指出 pose annotations 限制数据可得性与机器人微调依赖。
- Quote: “requires human data with hand and wrist pose annotations, which may limit data availability”
- Authors: ruihan-yang; qinxi-yu; yecheng-wu; et al.

### EA-UMI-READ-0002

- Claim: UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only data is insufficient for force-sensitive tasks.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.09988](https://arxiv.org/abs/2601.09988) In-the-Wild Compliant Manipulation with UMI-FT
- Locator: Abstract (full-text section)
- Evidence: The HTML full text reports that UMI-FT mounts compact six-axis force/torque sensors on each finger, uses multimodal demonstrations to train adaptive compliance policies, and shows diverse in-the-wild data outperforming limited scene-diversity data in a skewer task.
- Quote: “Abstract Many manipulation tasks require careful force modulation. With insufficient force the task may fail, while excessive force could cause damage. The high cost, bulky size and fragility of commercial force/torque (F/T) sensors have limited large-scale, force-aware policy learning. We introduce UMI-FT, a handheld data-collection platform that mounts compact, six-axis force/torque sensors on each finger, enabling finger-level wrench measurements alongside RGB, depth, and pose. Using the mult”
- Authors: hojung-choi; yifan-hou; chuer-pan; et al.

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

### EA-EGO-2026-0020

- Claim: 显式 contact geometry 在该系统中显著减少滑移并提高成功率，说明接触结构是 Ego-centric 数据转成可执行监督的独立质量维度。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.03828](https://arxiv.org/abs/2607.03828) ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Modeling
- Locator: IV-C 1 Hand–object geometric consistency module
- Evidence: 去除 hand geometry 后 object slip 变大且 success 下降，full ObjRetarget 最好。
- Quote: “also removing geometric consistency causes significant slippage, contact failures, and posture collapse”
- Authors: yuanchuan-lai; qing-gao; ziyan-liang; et al.

### EA-EGO-2026-0001

- Claim: EgoVLA 的人类第一视角预训练不能直接消除本体差距：没有机器人微调时，仿真 humanoid 的全部任务成功率为 0%。
- Stance: `limit` | Confidence: `direct`
- Paper: [2507.12440](https://arxiv.org/abs/2507.12440) EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
- Locator: 5.2 Humanoid Robot Evaluation
- Evidence: 论文把失败归因于外观、感知和运动学错配，并用同一 benchmark 的零样本结果明确展示。
- Quote: “zero-shot deployment on humanoid robots without fine-tuning on robot data results in 0% success across all tasks”
- Authors: ruihan-yang; qinxi-yu; yecheng-wu; et al.

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

### EA-EGO-2026-0019

- Claim: Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.03828](https://arxiv.org/abs/2607.03828) ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Modeling
- Locator: II-B Human-to-Robot Motion Retargeting
- Evidence: 相关工作和引言都指出现有方法多假设 object-free/weak-contact，忽略手臂与手的不同功能。
- Quote: “most methods assume object-free or weak-contact settings and focus on geometric consistency or joint error minimization”
- Authors: yuanchuan-lai; qing-gao; ziyan-liang; et al.

### EA-DQ-YEAR-READ-0015

- Claim: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06442](https://arxiv.org/abs/2607.06442) SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: Introduction
- Evidence: 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。
- Quote: “Our contributions are as follows: • We propose a primitive-compositional view of trajectory utility, realized by Primitive Discovery and Structural Exposure Allocation, which allocate selection budgets according to reuse-aware primitive and transition exposure under diminishing returns. • We introduce Learning-Friendly Trajectory Selection, which selects medoid trajectories within each composition-pattern bucket to favor central, stable, and predictable realizations for behavior cloning. • We pr”
- Authors: changti-wu; bin-yu; zhaolong-shen; et al.

## References

- `2507.12440` [EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos](https://arxiv.org/abs/2507.12440) (2025-07-16T17:27:44Z)
- `2509.21986` [Developing Vision-Language-Action Model from Egocentric Videos](https://arxiv.org/abs/2509.21986) (2025-09-26T07:09:33Z)
- `2601.09988` [In-the-Wild Compliant Manipulation with UMI-FT](https://arxiv.org/abs/2601.09988) (2026-01-15)
- `2602.09013` [Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction](https://arxiv.org/abs/2602.09013) (2026-02-09T18:56:02Z)
- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2602.16710` [EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data](https://arxiv.org/abs/2602.16710) (2026-02-18T18:59:05Z)
- `2603.22264` [UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos](https://arxiv.org/abs/2603.22264) (2026-03-23T17:49:12Z)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089) (2026-04-15)
- `2605.20373` [SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework](https://arxiv.org/abs/2605.20373) (2026-05-19T18:24:05Z)
- `2605.24934` [HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos](https://arxiv.org/abs/2605.24934) (2026-05-24T08:26:41Z)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.06194` [ActiveMimic: Egocentric Video Pretraining with Active Perception](https://arxiv.org/abs/2606.06194) (2026-06-04T14:01:01Z)
- `2606.16208` [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208) (2026-06-15)
- `2607.03828` [ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Modeling](https://arxiv.org/abs/2607.03828) (2026-07-04T11:31:23Z)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
