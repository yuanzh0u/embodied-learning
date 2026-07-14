# Evidence Appendix: 近半年 UMI 数据质量

- Time range: 2026-01-14..2026-07-14
- Events: 21
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DATA-2026-LY-0001

- Claim: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09056](https://arxiv.org/abs/2603.09056) Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning
- Locator: I INTRODUCTION; II-B Robot data curation; VI CONCLUSIONS
- Evidence: 论文指出人类遥操作会带来错误、操作约束、技能差异、噪声和次优行为；QoQ 用 influence functions 衡量训练 state-action 对验证示范的贡献，并在轨迹层聚合以降低噪声、保持覆盖，在仿真、真实机器人和 DROID in-the-wild 数据上改善策略成功率。
- Quote: “direct contribution to policy performance”
- Authors: haeone-lee; taywon-min; junsu-kim; et al.

### EA-DATA-2026-LY-0009

- Claim: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: II-A Performance and Usability Limitations; V DISCUSSION
- Evidence: 论文指出 UMI 示教虽快于遥操作但仍比手工慢、工具重量会造成疲劳并影响 demonstration；实验中改变 UMI gripper fingers 的力分布显著影响打开绷带包装表现，concentrated load grippers 优于 distributed load grippers，作者将其连接到 demonstration quality 和 learned robot control policies。
- Quote: “subtle hardware changes”
- Authors: gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al.

### EA-DATA-2026-LY-0003

- Claim: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.01544](https://arxiv.org/abs/2605.01544) An Efficient Metric for Data Quality Measurement in Imitation Learning
- Locator: Abstract; I INTRODUCTION; V Experiments
- Evidence: 论文把 poor-quality end-user demonstrations 具体化为 excessive corrective motions、oscillations 和 abrupt adjustments，并提出基于 demonstration trajectories PSD 的自动排序指标；实验比较未筛选、oracle、现有排序和 jerk/path-length 等 baseline，研究 PSD 筛选对下游 IL 成功率和平滑性的影响。
- Quote: “excessive corrective motions, oscillations”
- Authors: noushad-sojib; momotaz-begum

### EA-DATA-2026-LY-0002

- Claim: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: I INTRODUCTION; Abstract; V-D Pilot Study Design; VI-B Pilot Study Results
- Evidence: DQAF 框架从 sub-task progress、motion smoothness、stalls、kinematic limits 抽取质量信号，生成结构化质量评估和自然语言纠正建议；pilot study 中即时反馈条件呈现更高任务完成度、更高 episode-level quality scores 和更少 detected suboptimalities 的趋势。
- Quote: “not only on task completion”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

### EA-DATA-2026-LY-0005

- Claim: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation
- Locator: 1 Introduction; 2 Related Work; Appendix C.4 Retention Balance, Single-Task Curation, and Real-Robot Failure Modes
- Evidence: ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。
- Quote: “not only on data scale”
- Authors: tao-xu; jiaxin-wang; runhao-zhang; et al.

### EA-DATA-2026-DQ-0002

- Claim: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06564](https://arxiv.org/abs/2607.06564) Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation
- Locator: Abstract; I Introduction; IV-C Geometry-Centric Masked Autoencoding; V-B Multi-Task on MetaWorld and RLBench
- Evidence: 论文将 2D VLA 的困难归因于几何理解和空间推理不足、3D 数据和强 3D encoder 稀缺、跨模态 lifting/projection 损失几何 fidelity；其 GC-MAE 用伪点云监督当前点云重建和未来几何演化，并在仿真与真实任务中提升成功率。
- Authors: jiaming-liu; qingpo-wuwu; nuowei-han; et al.

### UMI-6M-001

- Claim: UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only data is insufficient for force-sensitive tasks.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.09988](https://arxiv.org/abs/2601.09988) In-the-Wild Compliant Manipulation with UMI-FT
- Locator: Abstract; V-B In-the-Wild Experiments
- Evidence: The HTML full text reports that UMI-FT mounts compact six-axis force/torque sensors on each finger, uses multimodal demonstrations to train adaptive compliance policies, and shows diverse in-the-wild data outperforming limited scene-diversity data in a skewer task.
- Authors: choi-hojung; hou-yifan; pan-chuer; et al.

### EA-DATA-2026-LY-0010

- Claim: VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.10618](https://arxiv.org/abs/2602.10618) From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks
- Locator: 1 Introduction; 2 Related Work; Abstract
- Evidence: 论文指出 VR 用于记录机器人学习示教时，visual fidelity 可能不如 user behavior 的 quality/reliability 重要；输入设备与可视化会影响工作负荷、运动效率、不必要动作和执行精度。实验发现 controller 与 motion-capture gloves 在 pick-and-place 与 manner-oriented tasks 上呈现不同轨迹策略和权衡。
- Quote: “quality and reliability of user behavior”
- Authors: robin-beierling; manuel-scheibl; jonas-dech; et al.

### EA-DATA-2026-LY-0008

- Claim: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: 1 Introduction; 3.3 Trajectory and Grasp Filtering via Simulation; Abstract
- Evidence: PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。
- Quote: “harmful to train the robot”
- Authors: albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al.

### EA-DATA-2026-LY-0004

- Claim: 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.11634](https://arxiv.org/abs/2603.11634) Diversity You Can Actually Measure: A Fast, Model-Free Diversity Metric for Robotics Datasets
- Locator: I Introduction; Abstract; IX Conclusion and Limitations
- Evidence: FAKTUAL 用 signature-kernel entropy 直接在 demonstration dataset 上度量多样性并选择高熵子集；作者在结论中明确说明该方法不像其他 data curation 策略那样保证只选高质量轨迹，若数据集中存在有害轨迹，最 diverse 子集可能反而有损。
- Quote: “does not guarantee the selection”
- Authors: sreevardhan-sirigiri; nathan-samuel-de-lara; christopher-agia; et al.

### EA-DATA-2026-LY-0012

- Claim: 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.12365](https://arxiv.org/abs/2606.12365) Ambient Diffusion Policy: Imitation Learning from Suboptimal Data in Robotics
- Locator: 1 Introduction; 2 Related Work; 10 Conclusion; Abstract
- Evidence: Ambient Diffusion Policy 指出高质量任务专用机器人数据昂贵，而 failures、不同质量轨迹、仿真、跨本体和 egocentric video 等 suboptimal/OOD sources 很丰富；作者认为过滤会浪费数据，常规 co-training 又会学习 harmful parts，因此提出 noise-dependent data usage，只在特定 diffusion times 让 suboptimal samples 贡献训练。
- Quote: “suboptimal data will continue to grow”
- Authors: adam-wei; nicholas-pfaff; thomas-cohn; et al.

### EA-DATA-2026-LY-0006

- Claim: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation
- Locator: 1 Introduction; Abstract; 2 Related Work
- Evidence: 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action chunks。
- Quote: “valuable recovery behaviors”
- Authors: justin-yu; andrew-goldberg; kavish-kondap; et al.

### EA-DATA-2026-DQ-0003

- Claim: 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: Abstract; 1 Introduction; 4 RynnWorld-Teleop as a Digital Teleoperation System; 6 Conclusion
- Evidence: 论文认为物理遥操作把每条示教绑定到操作者、硬件和固定 workspace，难覆盖长尾交互；RynnWorld-Teleop 用动作条件世界模型从手姿流生成机器人中心视频和可 retarget 的动作标签，作为模仿学习数据。但作者也列出细粒度液体/高形变物体和 per-platform fine-tuning 等限制。
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### UMI-6M-002

- Claim: UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefulness.
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: Abstract; II-A Performance and Usability Limitations; V Discussion; VI Conclusion
- Evidence: The HTML full text frames UMI grippers as promising data-collection tools but reports that concentrated-load grippers improve over distributed-load grippers while both remain slower and less effective than hands, with design refinements needed to reduce user burden and improve demonstration quality.
- Authors: georgadarellis-gina-l; beslic-natalija; lee-seonhun; et al.

### EA-DATA-2026-DQ-0001

- Claim: VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06442](https://arxiv.org/abs/2607.06442) SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: Abstract; Introduction; SIEVE; Conclusion
- Evidence: 论文指出大规模机器人示教池常含轨迹冗余、噪声示教、次优行为和任务覆盖不均；SIEVE 按可复用 primitive 与 transition 选择中心、稳定、适合模仿的轨迹，在多数据集和 VLA 模型上可用 50% 示教与 50% 训练步数超过全量训练。
- Authors: changti-wu; bin-yu; zhaolong-shen; et al.

### EA-EVAL-2026-DQ-0004

- Claim: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02642](https://arxiv.org/abs/2607.02642) GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation
- Locator: Abstract; 1 Introduction; 4.2 Evaluation Protocol; 5.2 How Do Pretraining and Training Data Matter?; 7 Discussion and Conclusion
- Evidence: 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-training 共同决定。
- Authors: gigaworld-team; angyuan-ma; boyuan-wang; et al.

### EA-SENSOR-2026-DQ-0005

- Claim: 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05390](https://arxiv.org/abs/2607.05390) Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models
- Locator: Abstract; 1 Introduction; 2 Related Work; 5 Experiments; 7 Conclusion
- Evidence: 论文认为形变物体有高维状态和复杂材料属性，接触诱发的局部形变常被末端执行器或物体遮挡；已有数据集常缺对象多样性、依赖合成数据，或缺高保真标注与接触形变。Deform360 采集 198 个日常物体、1,980 个交互序列、215 小时以上数据、41 个环视相机和双臂触觉 UMI gripper，并用 markerless 3D tracking 提取稠密几何与运动。
- Authors: hongyu-li; wanjia-fu; xiaoyan-cong; et al.

### UMI-6M-003

- Claim: UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.10647](https://arxiv.org/abs/2604.10647) OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction
- Locator: Abstract; 1 Introduction; 2.1 Robot-free Interfaces; 2.5 Multimodal Policy Learning; 5 Conclusion
- Evidence: The HTML full text repeatedly identifies limited physical interaction signals as a bottleneck of existing UMI-like systems and proposes synchronized RGB, depth, trajectory, tactile sensing, internal grasping force, and external wrench data to improve contact-rich policy learning.
- Authors: luo-shaqi; li-yuanyuan; hu-youhao; et al.

### UMI-6M-004

- Claim: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible task distribution.
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: Abstract; I Introduction; II-A UMI Variants and System Evolution; IV Evaluations
- Evidence: The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration data quality under challenging real-world conditions.
- Authors: wang-ziming

### EA-SENSOR-2026-DQ-0006

- Claim: 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: Abstract; 1 Introduction; 2 Related Work; 3 Method; 5 Conclusion and Limitations
- Evidence: 论文指出 VLA 在接触丰富任务中会因轻微接触扰动产生不可恢复失败，这些失败难以从视觉单独检测；TACO 用 tactile-aware world model 将真实 rollout 中的失败邻近状态转成想象的视触觉纠正片段和可执行纠正动作，在真实接触任务中相对 base policy 提升 44 个百分点成功率。
- Authors: shengbang-liu; yueru-jia; yuyang-yan; et al.

### UMI-6M-005

- Claim: For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action space, avoiding retargeting and embodiment-conversion losses.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.06033](https://arxiv.org/abs/2606.06033) RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning
- Locator: Abstract; 1 Introduction; 2.2 Dexterous Demonstration Interfaces; 3.3 Palm-Side Isomorphic Teleoperation Glove; A.1 Glove Sensing Interface
- Evidence: The HTML full text argues that retargeting and embodiment conversion can distort contact-rich interactions, then presents RealDexUMI as a retargeting-free wearable interface whose shared hand and sensing modules preserve deployment-aligned observations, tactile signals, contacts, and executable hand actions.
- Authors: xu-chaoyi; jiang-yixuan; huan-jiahui; et al.

## References

- `2601.09988` [In-the-Wild Compliant Manipulation with UMI-FT](https://arxiv.org/abs/2601.09988)
- `2602.10618` [From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks](https://arxiv.org/abs/2602.10618) (2026-02-11)
- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2603.09056` [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056) (2026-03-10)
- `2603.11634` [Diversity You Can Actually Measure: A Fast, Model-Free Diversity Metric for Robotics Datasets](https://arxiv.org/abs/2603.11634) (2026-03-12)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17)
- `2604.10647` [OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction](https://arxiv.org/abs/2604.10647)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089)
- `2605.01544` [An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544) (2026-05-02)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.06033` [RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning](https://arxiv.org/abs/2606.06033)
- `2606.12365` [Ambient Diffusion Policy: Imitation Learning from Suboptimal Data in Robotics](https://arxiv.org/abs/2606.12365) (2026-06-10)
- `2606.16208` [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208) (2026-06-15)
- `2606.28320` [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320) (2026-06-26)
- `2607.02642` [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.05390` [Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models](https://arxiv.org/abs/2607.05390) (2026-07-06)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
- `2607.06558` [RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation](https://arxiv.org/abs/2607.06558) (2026-07-07)
- `2607.06564` [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07)
