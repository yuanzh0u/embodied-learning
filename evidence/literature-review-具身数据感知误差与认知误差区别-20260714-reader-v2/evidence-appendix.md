# Evidence Appendix: 具身数据感知误差与认知误差区别

- Time range: 2026-01-14..2026-07-14
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### ERR-PVC-READ-0009

- Claim: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.09708](https://arxiv.org/abs/2601.09708) Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning
- Locator: 5 Conclusion
- Evidence: 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。
- Quote: “By distilling lengthy textual reasoning into compact latent representations via preference-guided distillation and visual trajectory alignment, our approach bridges high-level embodied reasoning with low-level action execution through reasoning-enhanced policy learning. Extensive experiments across diverse robotic manipulation and embodied reasoning benchmarks demonstrate that Fast-ThinkAct achieves strong performance with significantly reduced inference latency while enabling effective long-hor”
- Authors: chi-pin-huang; yunze-man; zhiding-yu; et al.

### ERR-PVC-READ-0010

- Claim: 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.00080](https://arxiv.org/abs/2605.00080) World Model for Robot Learning: A Comprehensive Survey
- Locator: 1 Introduction
- Evidence: 引言直接将纯反应 VLA 的三类困难列为长时程推理、temporal credit assignment 与 compounding errors。
- Quote: “Yet despite strong scaling trends ( Xiao et al. , 2025 ; Li et al. , 2025b ; Zhu et al. , 2026 ) , purely reactive VLA policies remain limited in complex physical environments, where they often struggle with long-horizon reasoning, temporal credit assignment, and robustness under compounding errors. A growing body of work argues that these limitations stem not only from insufficient action prediction capacity ( Ye et al. , 2026b ; Dang et al. , 2026 ) , but also from the lack of explicit predict”
- Authors: bohan-hou; gen-li; jindou-jia; et al.

### ERR-PVC-READ-0008

- Claim: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: Abstract (full-text section)
- Evidence: 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。
- Quote: “Abstract Industrial automation is at a pivotal moment, as Physical AI is driving a transition from rigid, hand-engineered automation systems toward more flexible and adaptive systems. This shift has created a growing demand for large-scale, real-world robot demonstration data, making teleoperation an increasingly important mechanism for data collection. However, high-quality teleoperated demonstrations remain difficult to obtain in practice, as novice operators often produce episodes that are ta”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

### ERR-PVC-READ-0011

- Claim: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09630](https://arxiv.org/abs/2606.09630) ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies
- Locator: 1 Introduction
- Evidence: ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classification mistakes 与 perception errors、sim-to-real mismatch 并列为失败来源。
- Quote: “Instead, it produces a structured recovery descriptor containing the failure type, recovery stage, active entities, confidence, and reward mask.”
- Authors: haodi-hu; chung-ta-huang; jing-liu; et al.

### ERR-PVC-READ-0012

- Claim: ProbeAct 的探针实验表明，扰动下 VLA 视觉骨干仍保留目标物空间表示，而失败集中在动作头回落到记忆的训练轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09740](https://arxiv.org/abs/2606.09740) ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models
- Locator: 1 Introduction
- Evidence: 引言将该失败定义为 latent perception 与 motor execution 的解耦，并把瓶颈定位到过拟合的 action head。
- Quote: “Critically, this memory trap manifests as a stark decoupling between latent perception and motor execution [ 28 , 8 , 21 ] . As corroborated by our own probing experiments, the VLA’s visual backbone successfully processes the perturbed scene, maintaining accurate spatial representations of the target object. The failure bottleneck lies exclusively within the action head: constrained by an overfitted mapping, the network collapses to the nominal trajectory of its training distribution. We systema”
- Authors: fan-zhang; seongbin-park; baharan-mirzasoleiman; et al.

### ERR-PVC-READ-0013

- Claim: 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.00673](https://arxiv.org/abs/2607.00673) Path Planning in Physically Viable World Models
- Locator: Abstract (full-text section)
- Evidence: 摘要对比了原始重建环境与物理修改场景下的路线可行性，并报告后者能揭示前者不可见的失败。
- Quote: “Abstract Robots deployed in unstructured outdoor environments often plan from scene reconstructions collected before deployment because operators cannot remap large or remote sites before every mission. As a result, robots must make long-horizon planning decisions using stale maps that assume the terrain remains unchanged, even though physical changes to the environment may render previously feasible routes unsafe or unreachable at execution time. We present a physically viable world model for e”
- Authors: su-ann-low; cheng-hsi-hsiao; xingjian-li; et al.

### ERR-PVC-READ-0014

- Claim: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02642](https://arxiv.org/abs/2607.02642) GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation
- Locator: Abstract (full-text section)
- Evidence: 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-training 共同决定。
- Quote: “Using WMBench, we analyze 7 video world models, 4 action representation schemes, and over 324,000 simulated policy rollouts paired with real robot executions, further enriching our analysis with large-scale community submissions from the CVPR 2026 GigaBrain Challenge, curated synthetic trajectories, and a training videos spanning more than 12,000 hours. Our experiments deliver three core insights: evaluator quality is dominated by long-horizon, action-faithful rollout consistency rather than sho”
- Authors: gigaworld-team; angyuan-ma; boyuan-wang; et al.

### ERR-PVC-READ-0015

- Claim: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06564](https://arxiv.org/abs/2607.06564) Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation
- Locator: I Introduction
- Evidence: 引言将操作需求归结为显式 3D 结构与时间一致性，并说明纯 2D 管线及有损的跨模态变换会削弱这些约束。
- Quote: “Despite this progress, robotic manipulation fundamentally requires spatial reasoning in the physical world [ 57 , 82 , 12 , 13 , 59 ] : the robot must infer 3D structure, reason about geometric relationships (e.g., reachability, occlusion, and contact), and plan actions that remain temporally consistent as the geometry evolves. Purely 2D VLA pipelines often struggle to reliably capture these geometric constraints, particularly in cluttered or dynamic environments. A natural direction is to expli”
- Authors: jiaming-liu; qingpo-wuwu; nuowei-han; et al.

### ERR-PVC-READ-0005

- Claim: ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.21161](https://arxiv.org/abs/2602.21161) ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking
- Locator: II-B LLM/VLM Based Robotic Operation
- Evidence: 相关工作段明确提出解耦视觉部件，让 LLM 在已知感知状态上做 3D 物理与动作推理。
- Quote: “To address this, we argue for decoupling the visual component: assuming the robot already has sufficiently accurate perceptual information via computer vision algorithms, and the LLMs are asked to focus only on action reasoning. This approach significantly reduces data requirements while also leveraging the wealth of existing research in computer vision. For example, the ReKep series [ 11 , 16 ] use vision-language models to identify keypoints for robotic manipulation, which significantly reduce”
- Authors: guangming-wang; qizhen-ying; yixiong-jing; et al.

### ERR-PVC-READ-0006

- Claim: τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接列出四类交互数据和 modality-specific supervision masks。
- Quote: “Abstract Robotic manipulation requires models that generate executable actions while anticipating and evaluating their future consequences before physical execution. We present -World Model ( -WM), a unified video-action world model that integrates policy learning, video prediction, and action evaluation within a single future-predictive framework. Built on a shared video diffusion backbone, -WM provides two complementary interfaces. First, a video action model jointly predicts future visual lat”
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### ERR-PVC-READ-0002

- Claim: ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.03784](https://arxiv.org/abs/2606.03784) Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。
- Quote: “Abstract Embodied chain-of-thought (CoT) aims to bridge linguistic reasoning with robotic control, yet its effective form and integration remain underexplored. In this paper, we revisit embodied CoT for robotic control at an unprecedented scale. We curate the largest embodied CoT corpus to date, comprising 978,743 trajectories, 226.3M samples, and 2592.5 hours of data. Through extensive experiments, we show that effective CoT must ground high-level semantic understaning in concrete linguistic ac”
- Authors: nan-sun; yuan-zhang; yongkun-yang; et al.

### ERR-PVC-READ-0003

- Claim: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control
- Evidence: 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。
- Quote: “All data modalities are synchronized through the robot control loop. For policy learning, actions are converted to a unified 7D end-effector delta representation (1) where are translational deltas, are rotational deltas, and is the gripper command. This decouples learning from the exact robot configuration, enabling cross-embodiment by focusing the policy on local contact adjustment from tactile feedback. Several quality checks are applied to every collected trajectory. Empty or corrupted trajec”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### ERR-PVC-READ-0004

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Quote: “Policies in this setting are trained using both nominal demonstrations and recovery interaction data.”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### ERR-PVC-READ-0007

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: 3.2 Inconsistency of Control Commands across Robots
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Quote: “Recent work has scaled robot learning by training policies on data from multiple embodiments [ 27 , 23 , 32 ] , often using the Cartesian delta action space [ 23 , 32 ] since it is less dependent on robot-specific kinematics and invariant to base-frame translation [ 18 , 14 ] . In practice, this is typically realized by predicting Cartesian delta control commands that are fed to the underlying robot controller [ 23 , 32 ] . Figure 2: Different robots (e.g., UR5 vs. Franka Research 3) require dif”
- Authors: haeone-lee

### ERR-PVC-READ-0001

- Claim: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: 5 Conclusion and Limitations
- Evidence: 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。
- Quote: “We presented TACO, a tactile-aware world-model-driven framework for scalable VLA post-training in contact-rich manipulation. Following a Recognize–Imagine–Label loop, TACO converts real-world failures into imagined corrections without repeated human intervention: a tactile-aware world model jointly denoises future video and force sequences, while a unified progress-action model recognizes failure-adjacent states and labels imagined segments with corrective actions. To incorporate this supervisio”
- Authors: shengbang-liu; yueru-jia; yuyang-yan; et al.

## References

- `2601.09708` [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](https://arxiv.org/abs/2601.09708) (2026-01-14)
- `2602.21161` [ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking](https://arxiv.org/abs/2602.21161) (2026-02-24)
- `2605.00080` [World Model for Robot Learning: A Comprehensive Survey](https://arxiv.org/abs/2605.00080) (2026-04-30)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.03784` [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](https://arxiv.org/abs/2606.03784) (2026-06-02)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.09630` [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630) (2026-06-08)
- `2606.09740` [ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models](https://arxiv.org/abs/2606.09740) (2026-06-08)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2607.00673` [Path Planning in Physically Viable World Models](https://arxiv.org/abs/2607.00673) (2026-07-01)
- `2607.02642` [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.06564` [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07)
