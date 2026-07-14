# Evidence Appendix: 近半年 UMI 数据质量

- Time range: 2026-01-14..2026-07-14
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-UMI-READ-0011

- Claim: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09056](https://arxiv.org/abs/2603.09056) Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning
- Locator: VI CONCLUSIONS
- Evidence: 论文指出人类遥操作会带来错误、操作约束、技能差异、噪声和次优行为；QoQ 用 influence functions 衡量训练 state-action 对验证示范的贡献，并在轨迹层聚合以降低噪声、保持覆盖，在仿真、真实机器人和 DROID in-the-wild 数据上改善策略成功率。
- Quote: “In this work, we propose QoQ, a method that curates robotic datasets based on direct performance contribution to the learned policy. We define a quality scoring mechanism for state-action pairs derived from influence functions.”
- Authors: haeone-lee; taywon-min; junsu-kim; et al.

### EA-UMI-READ-0001

- Claim: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: V DISCUSSION
- Evidence: 论文指出 UMI 示教虽快于遥操作但仍比手工慢、工具重量会造成疲劳并影响 demonstration；实验中改变 UMI gripper fingers 的力分布显著影响打开绷带包装表现，concentrated load grippers 优于 distributed load grippers，作者将其连接到 demonstration quality 和 learned robot control policies。
- Quote: “Overall, the usability study demonstrated that altering the force distribution of UMI gripper fingers significantly affected participants’ ability to open bandage packages, with concentrated load grippers outperforming distributed load grippers. These findings highlight that subtle hardware changes can substantially improve demonstration quality and, in turn, the robot control policies learned from them.”
- Authors: gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al.

### EA-UMI-READ-0012

- Claim: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.01544](https://arxiv.org/abs/2605.01544) An Efficient Metric for Data Quality Measurement in Imitation Learning
- Locator: Abstract (full-text section)
- Evidence: 论文把 poor-quality end-user demonstrations 具体化为 excessive corrective motions、oscillations 和 abrupt adjustments，并提出基于 demonstration trajectories PSD 的自动排序指标；实验比较未筛选、oracle、现有排序和 jerk/path-length 等 baseline，研究 PSD 筛选对下游 IL 成功率和平滑性的影响。
- Quote: “Abstract Imitation learning (IL) has seen remarkable progress, yet field deployment of IL-powered robots remains hindered by the challenge of out-of-distribution (OOD) scenarios. Fine-tuning pre-trained policies with end-user demonstrations collected in deployment environments is a promising strategy to address this challenge. However, end-user demonstrations are frequently of poor quality, characterized by excessive corrective motions, oscillations, and abrupt adjustments that degrade both lear”
- Authors: noushad-sojib; momotaz-begum

### EA-UMI-READ-0013

- Claim: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: Abstract (full-text section)
- Evidence: 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。
- Quote: “Abstract Industrial automation is at a pivotal moment, as Physical AI is driving a transition from rigid, hand-engineered automation systems toward more flexible and adaptive systems. This shift has created a growing demand for large-scale, real-world robot demonstration data, making teleoperation an increasingly important mechanism for data collection. However, high-quality teleoperated demonstrations remain difficult to obtain in practice, as novice operators often produce episodes that are ta”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

### EA-UMI-READ-0014

- Claim: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02642](https://arxiv.org/abs/2607.02642) GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation
- Locator: Abstract (full-text section)
- Evidence: 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-training 共同决定。
- Quote: “Using WMBench, we analyze 7 video world models, 4 action representation schemes, and over 324,000 simulated policy rollouts paired with real robot executions, further enriching our analysis with large-scale community submissions from the CVPR 2026 GigaBrain Challenge, curated synthetic trajectories, and a training videos spanning more than 12,000 hours. Our experiments deliver three core insights: evaluator quality is dominated by long-horizon, action-faithful rollout consistency rather than sho”
- Authors: gigaworld-team; angyuan-ma; boyuan-wang; et al.

### EA-UMI-READ-0015

- Claim: 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05390](https://arxiv.org/abs/2607.05390) Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models
- Locator: Abstract (full-text section)
- Evidence: 论文认为形变物体有高维状态和复杂材料属性，接触诱发的局部形变常被末端执行器或物体遮挡；已有数据集常缺对象多样性、依赖合成数据，或缺高保真标注与接触形变。Deform360 采集 198 个日常物体、1,980 个交互序列、215 小时以上数据、41 个环视相机和双臂触觉 UMI gripper，并用 markerless 3D tracking 提取稠密几何与运动。
- Quote: “To address this, we present Deform360, a large-scale visuotactile dataset featuring 198 daily-life objects, 1,980 interaction sequences, and over 215 hours of observations from 41 surround-view cameras and bimanual tactile grippers to capture both global motion and contact-induced local deformations. Leveraging a novel markerless visuotactile 3D tracking pipeline to extract dense geometry and motion, we systematically evaluate current state-of-the-art world models, comparing 2D video models agai”
- Authors: hongyu-li; wanjia-fu; xiaoyan-cong; et al.

### EA-UMI-READ-0002

- Claim: UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only data is insufficient for force-sensitive tasks.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.09988](https://arxiv.org/abs/2601.09988) In-the-Wild Compliant Manipulation with UMI-FT
- Locator: Abstract (full-text section)
- Evidence: The HTML full text reports that UMI-FT mounts compact six-axis force/torque sensors on each finger, uses multimodal demonstrations to train adaptive compliance policies, and shows diverse in-the-wild data outperforming limited scene-diversity data in a skewer task.
- Quote: “Abstract Many manipulation tasks require careful force modulation. With insufficient force the task may fail, while excessive force could cause damage. The high cost, bulky size and fragility of commercial force/torque (F/T) sensors have limited large-scale, force-aware policy learning. We introduce UMI-FT, a handheld data-collection platform that mounts compact, six-axis force/torque sensors on each finger, enabling finger-level wrench measurements alongside RGB, depth, and pose. Using the mult”
- Authors: hojung-choi; yifan-hou; chuer-pan; et al.

### EA-UMI-READ-0008

- Claim: VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.10618](https://arxiv.org/abs/2602.10618) From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks
- Locator: 1 Introduction
- Evidence: 论文指出 VR 用于记录机器人学习示教时，visual fidelity 可能不如 user behavior 的 quality/reliability 重要；输入设备与可视化会影响工作负荷、运动效率、不必要动作和执行精度。实验发现 controller 与 motion-capture gloves 在 pick-and-place 与 manner-oriented tasks 上呈现不同轨迹策略和权衡。
- Quote: “In contrast, when VR is used to record demonstrations for robot learning, visual fidelity may be less important than the quality and reliability of user behavior during task execution.”
- Authors: robin-beierling; manuel-scheibl; jonas-dech; et al.

### EA-UMI-READ-0009

- Claim: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: 3.3 Trajectory and Grasp Filtering via Simulation
- Evidence: PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。
- Quote: “Now that we have converted the human demonstrations into 6 DoF object pose trajectories, the next step is to execute them on a robot in simulation. This serves two purposes. One is to filter out those that may not be suitable for robot learning. There are two main reasons a trajectory may be unsuitable. First, pose estimation errors can lead to inaccurate trajectories. Second, the extracted trajectory may not be physically achievable by the robot. In either case, it would be harmful to train the”
- Authors: albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al.

### EA-UMI-READ-0003

- Claim: UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.10647](https://arxiv.org/abs/2604.10647) OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction
- Locator: Abstract (full-text section)
- Evidence: The HTML full text repeatedly identifies limited physical interaction signals as a bottleneck of existing UMI-like systems and proposes synchronized RGB, depth, trajectory, tactile sensing, internal grasping force, and external wrench data to improve contact-rich policy learning.
- Quote: “Abstract UMI-style interfaces enable scalable robot learning, but existing systems remain largely visuomotor, relying primarily on RGB observations and trajectory while providing only limited access to physical interaction signals. This becomes a fundamental limitation in contact-rich manipulation, where success depends on contact dynamics such as tactile interaction, internal grasping force, and external interaction wrench that are difficult to infer from vision alone. We present OmniUMI, a uni”
- Authors: shaqi-luo; yuanyuan-li; youhao-hu; et al.

### EA-UMI-READ-0010

- Claim: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation
- Locator: Abstract (full-text section)
- Evidence: 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action chunks。
- Quote: “Abstract Scaling imitation learning requires large datasets, yet human teleoperation inevitably produces mixed-quality demonstrations containing hesitations and recoveries. Prior frame-level progress reward models supervise on absolute temporal progress proxies that suffer from label noise, or require costly human annotations to define subtask boundaries. We present WARP (Warp-Augmented Relative Progress), a novel fully self-supervised algorithm for learning dense, signed relative progress magni”
- Authors: justin-yu; andrew-goldberg; kavish-kondap; et al.

### EA-UMI-READ-0007

- Claim: RynnWorld-Teleop将数字遥操作作为生成式数据引擎，但论文明确限定了它对精细流体动力学、高形变物体和跨机器人平台扩展的能力。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: 6 Conclusion
- Evidence: 结论的限制段指出，模型在精细流体和高形变操作上仍会失败，而当前跨本体迁移仍要求每个平台单独微调。
- Quote: “Limitation. While RynnWorld-Teleop successfully demonstrates digital teleoperation as a viable data engine, several limitations remain. First, while the depth-modulated rendering captures 3D spatial dynamics, the model occasionally struggles with complex physical phenomena such as fine-grained liquid dynamics or the manipulation of highly deformable objects. Addressing these cases will likely require richer training data covering such interactions. Second, bridging the embodiment gap currently r”
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### EA-UMI-READ-0004

- Claim: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible task distribution.
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: Abstract (full-text section)
- Evidence: The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration data quality under challenging real-world conditions.
- Quote: “Abstract We present UMI-3D, a multimodal extension of the Universal Manipulation Interface (UMI) for robust and scalable data collection in embodied manipulation. While UMI enables portable, wrist-mounted data acquisition, its reliance on monocular visual SLAM makes it vulnerable to occlusions, dynamic scenes, and tracking failures, limiting its applicability in real-world environments. UMI-3D addresses these limitations by introducing a lightweight and low-cost LiDAR sensor tightly integrated i”
- Authors: ziming-wang

### EA-UMI-READ-0005

- Claim: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: 5 Conclusion and Limitations
- Evidence: 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。
- Quote: “We presented TACO, a tactile-aware world-model-driven framework for scalable VLA post-training in contact-rich manipulation. Following a Recognize–Imagine–Label loop, TACO converts real-world failures into imagined corrections without repeated human intervention: a tactile-aware world model jointly denoises future video and force sequences, while a unified progress-action model recognizes failure-adjacent states and labels imagined segments with corrective actions. To incorporate this supervisio”
- Authors: shengbang-liu; yueru-jia; yuyang-yan; et al.

### EA-UMI-READ-0006

- Claim: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06442](https://arxiv.org/abs/2607.06442) SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: Introduction
- Evidence: 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。
- Quote: “Our contributions are as follows: • We propose a primitive-compositional view of trajectory utility, realized by Primitive Discovery and Structural Exposure Allocation, which allocate selection budgets according to reuse-aware primitive and transition exposure under diminishing returns. • We introduce Learning-Friendly Trajectory Selection, which selects medoid trajectories within each composition-pattern bucket to favor central, stable, and predictable realizations for behavior cloning. • We pr”
- Authors: changti-wu; bin-yu; zhaolong-shen; et al.

## References

- `2601.09988` [In-the-Wild Compliant Manipulation with UMI-FT](https://arxiv.org/abs/2601.09988) (2026-01-15)
- `2602.10618` [From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks](https://arxiv.org/abs/2602.10618) (2026-02-11)
- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2603.09056` [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056) (2026-03-10)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17)
- `2604.10647` [OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction](https://arxiv.org/abs/2604.10647) (2026-04-12)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089) (2026-04-15)
- `2605.01544` [An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544) (2026-05-02)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.28320` [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320) (2026-06-26)
- `2607.02642` [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.05390` [Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models](https://arxiv.org/abs/2607.05390) (2026-07-06)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
- `2607.06558` [RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation](https://arxiv.org/abs/2607.06558) (2026-07-07)
