# Evidence Appendix: 具身数据感知误差溯源

- Time range: 2025-07-14..2026-07-14
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### ERR-TRACE-READ-0010

- Claim: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09056](https://arxiv.org/abs/2603.09056) Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning
- Locator: VI CONCLUSIONS
- Evidence: 论文指出人类遥操作会带来错误、操作约束、技能差异、噪声和次优行为；QoQ 用 influence functions 衡量训练 state-action 对验证示范的贡献，并在轨迹层聚合以降低噪声、保持覆盖，在仿真、真实机器人和 DROID in-the-wild 数据上改善策略成功率。
- Quote: “In this work, we propose QoQ, a method that curates robotic datasets based on direct performance contribution to the learned policy. We define a quality scoring mechanism for state-action pairs derived from influence functions.”
- Authors: haeone-lee; taywon-min; junsu-kim; et al.

### ERR-TRACE-READ-0011

- Claim: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.01544](https://arxiv.org/abs/2605.01544) An Efficient Metric for Data Quality Measurement in Imitation Learning
- Locator: Abstract (full-text section)
- Evidence: 论文把 poor-quality end-user demonstrations 具体化为 excessive corrective motions、oscillations 和 abrupt adjustments，并提出基于 demonstration trajectories PSD 的自动排序指标；实验比较未筛选、oracle、现有排序和 jerk/path-length 等 baseline，研究 PSD 筛选对下游 IL 成功率和平滑性的影响。
- Quote: “Abstract Imitation learning (IL) has seen remarkable progress, yet field deployment of IL-powered robots remains hindered by the challenge of out-of-distribution (OOD) scenarios. Fine-tuning pre-trained policies with end-user demonstrations collected in deployment environments is a promising strategy to address this challenge. However, end-user demonstrations are frequently of poor quality, characterized by excessive corrective motions, oscillations, and abrupt adjustments that degrade both lear”
- Authors: noushad-sojib; momotaz-begum

### ERR-TRACE-READ-0012

- Claim: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: Abstract (full-text section)
- Evidence: 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。
- Quote: “Abstract Industrial automation is at a pivotal moment, as Physical AI is driving a transition from rigid, hand-engineered automation systems toward more flexible and adaptive systems. This shift has created a growing demand for large-scale, real-world robot demonstration data, making teleoperation an increasingly important mechanism for data collection. However, high-quality teleoperated demonstrations remain difficult to obtain in practice, as novice operators often produce episodes that are ta”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

### ERR-TRACE-READ-0013

- Claim: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02642](https://arxiv.org/abs/2607.02642) GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation
- Locator: Abstract (full-text section)
- Evidence: 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-training 共同决定。
- Quote: “Using WMBench, we analyze 7 video world models, 4 action representation schemes, and over 324,000 simulated policy rollouts paired with real robot executions, further enriching our analysis with large-scale community submissions from the CVPR 2026 GigaBrain Challenge, curated synthetic trajectories, and a training videos spanning more than 12,000 hours. Our experiments deliver three core insights: evaluator quality is dominated by long-horizon, action-faithful rollout consistency rather than sho”
- Authors: gigaworld-team; angyuan-ma; boyuan-wang; et al.

### ERR-TRACE-READ-0014

- Claim: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06564](https://arxiv.org/abs/2607.06564) Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation
- Locator: I Introduction
- Evidence: 引言将操作需求归结为显式 3D 结构与时间一致性，并说明纯 2D 管线及有损的跨模态变换会削弱这些约束。
- Quote: “Despite this progress, robotic manipulation fundamentally requires spatial reasoning in the physical world [ 57 , 82 , 12 , 13 , 59 ] : the robot must infer 3D structure, reason about geometric relationships (e.g., reachability, occlusion, and contact), and plan actions that remain temporally consistent as the geometry evolves. Purely 2D VLA pipelines often struggle to reliably capture these geometric constraints, particularly in cluttered or dynamic environments. A natural direction is to expli”
- Authors: jiaming-liu; qingpo-wuwu; nuowei-han; et al.

### ERR-TRACE-READ-0005

- Claim: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: 3.3 Trajectory and Grasp Filtering via Simulation
- Evidence: PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。
- Quote: “Now that we have converted the human demonstrations into 6 DoF object pose trajectories, the next step is to execute them on a robot in simulation. This serves two purposes. One is to filter out those that may not be suitable for robot learning. There are two main reasons a trajectory may be unsuitable. First, pose estimation errors can lead to inaccurate trajectories. Second, the extracted trajectory may not be physically achievable by the robot. In either case, it would be harmful to train the”
- Authors: albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al.

### ERR-TRACE-READ-0007

- Claim: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction
- Evidence: 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。
- Quote: “The primary advantage of 3PoinTr is that it trains on data General Flow ignores. Real-world points are often temporarily occluded; General Flow removes any trajectory with invisible point-timestep pairs during preprocessing, whereas 3PoinTr retains all trajectories and masks losses for individual invisible point-timestep pairs. This provides additional supervision over task-critical object points that are temporarily occluded during manipulation. For example, in the Throw Away Paper task, every”
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### ERR-TRACE-READ-0008

- Claim: τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接列出四类交互数据和 modality-specific supervision masks。
- Quote: “Abstract Robotic manipulation requires models that generate executable actions while anticipating and evaluating their future consequences before physical execution. We present -World Model ( -WM), a unified video-action world model that integrates policy learning, video prediction, and action evaluation within a single future-predictive framework. Built on a shared video diffusion backbone, -WM provides two complementary interfaces. First, a video action model jointly predicts future visual lat”
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### ERR-TRACE-READ-0002

- Claim: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control
- Evidence: 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。
- Quote: “All data modalities are synchronized through the robot control loop. For policy learning, actions are converted to a unified 7D end-effector delta representation (1) where are translational deltas, are rotational deltas, and is the gripper command. This decouples learning from the exact robot configuration, enabling cross-embodiment by focusing the policy on local contact adjustment from tactile feedback. Several quality checks are applied to every collected trajectory. Empty or corrupted trajec”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### ERR-TRACE-READ-0003

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Quote: “Policies in this setting are trained using both nominal demonstrations and recovery interaction data.”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### ERR-TRACE-READ-0006

- Claim: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation
- Locator: Abstract (full-text section)
- Evidence: 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action chunks。
- Quote: “Abstract Scaling imitation learning requires large datasets, yet human teleoperation inevitably produces mixed-quality demonstrations containing hesitations and recoveries. Prior frame-level progress reward models supervise on absolute temporal progress proxies that suffer from label noise, or require costly human annotations to define subtask boundaries. We present WARP (Warp-Augmented Relative Progress), a novel fully self-supervised algorithm for learning dense, signed relative progress magni”
- Authors: justin-yu; andrew-goldberg; kavish-kondap; et al.

### ERR-TRACE-READ-0015

- Claim: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.16690](https://arxiv.org/abs/2606.16690) PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差作为介入信号。
- Quote: “Abstract Learning-based manipulation policies have made substantial progress in real-world robot manipulation, particularly for short-horizon action generation. However, deployment in open workspaces remains fragile under unexpected local scene dynamics, such as moving objects, transient occlusions, or disturbances near the intended motion. Existing runtime monitors often rely on global observation anomalies, policy uncertainty, or frame-level visual changes, and struggle to distinguish task-rel”
- Authors: yanan-zhou; ranpeng-qiu; yincong-chen; et al.

### ERR-TRACE-READ-0009

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: 3.2 Inconsistency of Control Commands across Robots
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Quote: “Recent work has scaled robot learning by training policies on data from multiple embodiments [ 27 , 23 , 32 ] , often using the Cartesian delta action space [ 23 , 32 ] since it is less dependent on robot-specific kinematics and invariant to base-frame translation [ 18 , 14 ] . In practice, this is typically realized by predicting Cartesian delta control commands that are fed to the underlying robot controller [ 23 , 32 ] . Figure 2: Different robots (e.g., UR5 vs. Franka Research 3) require dif”
- Authors: haeone-lee

### ERR-TRACE-READ-0001

- Claim: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: 5 Conclusion and Limitations
- Evidence: 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。
- Quote: “We presented TACO, a tactile-aware world-model-driven framework for scalable VLA post-training in contact-rich manipulation. Following a Recognize–Imagine–Label loop, TACO converts real-world failures into imagined corrections without repeated human intervention: a tactile-aware world model jointly denoises future video and force sequences, while a unified progress-action model recognizes failure-adjacent states and labels imagined segments with corrective actions. To incorporate this supervisio”
- Authors: shengbang-liu; yueru-jia; yuyang-yan; et al.

### ERR-TRACE-READ-0004

- Claim: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06442](https://arxiv.org/abs/2607.06442) SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: Introduction
- Evidence: 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。
- Quote: “Our contributions are as follows: • We propose a primitive-compositional view of trajectory utility, realized by Primitive Discovery and Structural Exposure Allocation, which allocate selection budgets according to reuse-aware primitive and transition exposure under diminishing returns. • We introduce Learning-Friendly Trajectory Selection, which selects medoid trajectories within each composition-pattern bucket to favor central, stable, and predictable realizations for behavior cloning. • We pr”
- Authors: changti-wu; bin-yu; zhaolong-shen; et al.

## References

- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.09056` [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056) (2026-03-10)
- `2605.01544` [An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544) (2026-05-02)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.16690` [PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation](https://arxiv.org/abs/2606.16690) (2026-06-15)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2606.28320` [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320) (2026-06-26)
- `2607.02642` [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
- `2607.06564` [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07)
