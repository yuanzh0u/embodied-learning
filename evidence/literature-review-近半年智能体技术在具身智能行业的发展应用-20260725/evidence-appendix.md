# Evidence Appendix: 近半年智能体技术在具身智能行业的发展应用

- Time range: 2026-01-25..2026-07-25
- Events: 47
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-WMDATA-READ-0007

- Claim: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-real correlation.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08546](https://arxiv.org/abs/2603.08546) Interactive World Simulator for Robot Policy Training and Evaluation
- Locator: IV-C Data Generation for Policy Training
- Evidence: The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real performance correlation.
- Quote: “Notably, policies trained on 100% world simulator data perform comparably to those trained on an equivalent volume of real-robot expert data. This suggests that our simulator can generate data with quality similar to that of real-world demonstrations.”
- Authors: yixuan-wang; rhythm-syed; fangyu-wu; et al.

### EA-WMDATA-READ-0009

- Claim: World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations.
- Stance: `support` | Confidence: `direct`
- Paper: [2604.21741](https://arxiv.org/abs/2604.21741) Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training
- Locator: 3.5 Collecting Corrective Trajectories for Post-Training
- Evidence: Hi-WM rolls policies inside a world model, lets humans intervene when rollouts become incorrect or failure-prone, caches and branches failure states, and adds corrective trajectories back into the training set for post-training.
- Quote: “Within Hi-WM, post-training data are collected in a closed-loop inside the interactive world model. The pre-trained policy first runs in the world model from the current observation and generates a rollout. When the rollout enters unfamiliar or failure-prone states, a human operator intervenes through the hardware-agnostic interface and provides corrective actions. The world model then continues the rollout from the current state using these human actions. Once the rollout has been guided back t”
- Authors: yaxuan-li; zhongyi-zhou; yefei-chen; et al.

### EA-WMDATA-READ-0008

- Claim: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon future evolution rather than only behavior-cloning actions.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.20752](https://arxiv.org/abs/2605.20752) GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation
- Locator: 3.4 GaussianDream Training and Efficient Inference
- Evidence: GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference.
- Quote: “GaussianDream follows an asymmetric strategy: dense Gaussian reconstruction and prediction supervise training, while only the compact prefix is retained for online control. Stage I: GaussianDream pretraining. We first train the reconstruction and prediction heads without action learning. For each demonstration sequence, RGB frames are paired with pseudo depth and pseudo 3D scene-flow targets constructed from adjacent frames. The GaussianDream objective combines current reconstruction and future”
- Authors: zijian-zhang; yuqing-jiang; qian-cheng; et al.

### EA-4D-READ-0013

- Claim: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: 3.1. Problem Formulation
- Evidence: 问题建模段先定义动作与视觉未来的联合分布，再明确把未来触觉纳入联合预测目标。
- Quote: “Building on these two formulations, a world action model combines action prediction and future observation prediction into a unified framework. Specifically, it jointly models (3) or equivalently factorizes the joint distribution as (4) where future visual prediction provides predictive structure for action generation. However, in contact-rich manipulation, vision alone is often insufficient to capture physical interaction cues. To address this limitation, we introduce Dream-Tac, an enhanced wor”
- Authors: yunfan-lou; yifan-ye; yankai-fu; et al.

### EA-4D-READ-0012

- Claim: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction
- Evidence: 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。
- Quote: “The primary advantage of 3PoinTr is that it trains on data General Flow ignores. Real-world points are often temporarily occluded; General Flow removes any trajectory with invisible point-timestep pairs during preprocessing, whereas 3PoinTr retains all trajectories and masks losses for individual invisible point-timestep pairs. This provides additional supervision over task-critical object points that are temporarily occluded during manipulation. For example, in the Throw Away Paper task, every”
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### EA-4D-READ-0011

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Quote: “Policies in this setting are trained using both nominal demonstrations and recovery interaction data.”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### EA-WMEVAL-READ-0007

- Claim: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Abstract (full-text section)
- Evidence: The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap futures.
- Quote: “Abstract Simulating robot-world interactions is a cornerstone of Embodied AI. Recently, a few works have shown promise in leveraging video generations to transcend the rigid visual/physical constraints of traditional simulators. However, they primarily operate in 2D space or are guided by static environmental cues, ignoring the fundamental reality that robot-world interactions are inherently 4D spatiotemporal events that require precise interactive modeling. To restore this 4D essence while ensu”
- Authors: mutian-xu; tianbao-zhang; tianqi-liu; et al.

### EA-WMEVAL-READ-0005

- Claim: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into executable trajectories; the paper reports real-world manipulation success improving from 61% to 81%.
- Quote: “Abstract Video world models can generate realistic futures from a single instruction, but they often fail to track the same physical points consistently across time. As a result, the generated videos appear plausible, yet lack the physical grounding required for reliable action execution, such as robot manipulation. We present GEM-4D , a geometry-grounded video world model that resolves this limitation by injecting dense 4D correspondence supervision distilled from a pretrained geometry foundati”
- Authors: kaichen-zhou; yuzhen-chen; fangneng-zhan; et al.

### EA-WMEVAL-READ-0003

- Claim: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information downstream policies need.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00664](https://arxiv.org/abs/2606.00664) SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models
- Locator: Abstract (full-text section)
- Evidence: SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as policy-training data.
- Quote: “Abstract Embodied world models have emerged as a promising paradigm in robotics by predicting how robot actions affect the surrounding scene. However, the rollout inference remains computationally expensive in pixel space, as long-horizon manipulation videos typically have to be generated frame by frame. This cost cannot be easily reduced by indiscriminately dropping frames, since downstream policies rely on complete preservation of sparse task-relevant events such as approach, contact, grasp, a”
- Authors: ziheng-he; yixiang-chen; ning-yang; et al.

### EA-WMEVAL-READ-0001

- Claim: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接报告了异构数据组成与 modality-specific supervision masks。
- Quote: “Abstract Robotic manipulation requires models that generate executable actions while anticipating and evaluating their future consequences before physical execution. We present -World Model ( -WM), a unified video-action world model that integrates policy learning, video prediction, and action evaluation within a single future-predictive framework. Built on a shared video diffusion backbone, -WM provides two complementary interfaces. First, a video action model jointly predicts future visual lat”
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### EA-WMEVAL-READ-0010

- Claim: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13672](https://arxiv.org/abs/2606.13672) $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- Locator: 3 WEAVER : World Estimation Across Views for Embodied Reasoning
- Evidence: The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthetic policy improvement, and test-time planning.
- Quote: “Figure 2 : WEAVER Architecture. Left: The world model encodes memory, history, and action sequences to image future rollouts in latent space. Middle: The latent verifier, equipped with reward and critic heads, selects samples with high advantage to steer the policy distribution. Right: Decoded generation corresponding to different outcomes of action sequences. We now describe the key ingredients in WEAVER : a robot world model designed to support policy evaluation, policy improvement, and test-t”
- Authors: arnav-kumar-jain; yilin-wu; jesse-farebrother; et al.

### EA-WMEVAL-READ-0014

- Claim: A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenario coverage.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.11386](https://arxiv.org/abs/2604.11386) ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation
- Locator: Abstract (full-text section)
- Evidence: ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate large-scale action-video training datasets.
- Quote: “Abstract Recent advancements in foundational models, such as large language models and world models, have greatly enhanced the capabilities of robotics, enabling robots to autonomously perform complex tasks. However, acquiring large-scale, high-quality training data for robotics remains a challenge, as it often requires substantial manual effort and is limited in its coverage of diverse real-world environments. To address this, we propose a novel hybrid approach called Compositional Simulation ,”
- Authors: yiran-qin; jiahua-ma; li-kang; et al.

### EA-WMEVAL-READ-0011

- Claim: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing teleoperation burden.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.02577](https://arxiv.org/abs/2606.02577) RoboDream: Compositional World Models for Scalable Robot Data Synthesis
- Locator: Abstract (full-text section)
- Evidence: RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost.
- Quote: “Abstract Scaling robot learning requires large-scale, diverse demonstrations, yet real-world data collection via teleoperation remains prohibitively expensive and time-consuming. While video diffusion models offer a promising avenue for data scaling, existing generative approaches are often limited to superficial visual augmentation, or suffer from embodiment hallucinations that yield physically infeasible motions. We present a generalizable embodiment-centric world model that achieves scalable”
- Authors: junjie-ye; rong-xue; basile-van-hoorick; et al.

### EA-WMEVAL-READ-0008

- Claim: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.00121](https://arxiv.org/abs/2605.00121) Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes
- Locator: VIII Limitations
- Evidence: The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and planning.
- Quote: “While embedding open-vocabulary scene graphs with persistence estimators yields tempo-spatio-semantic capabilities, our approach is not free of limitations. First, object-receptacle edges are modelled independently. While joint distributions over multiple locations are possible [ 30 ] , inference costs grow with the number of observed locations per object, inducing a trade-off between expressivity and real-time performance. We believe that striking the right balance in this trade-off is a promis”
- Authors: miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta

### EA-WMEVAL-READ-0015

- Claim: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.27947](https://arxiv.org/abs/2605.27947) SANTS: A State-Adaptive Scheduler for World Action Models
- Locator: Abstract (full-text section)
- Evidence: SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video fidelity.
- Quote: “Abstract World Action Models (WAMs) improve robot manipulation by using video-based future representations to condition action generation. In pixel-space WAMs, however, the best action condition is not necessarily the fully denoised video. Controlled denoising-depth scans show that video refinement can reduce action error up to a state-dependent point, after which the gain may saturate or even reverse when late predictions become less action-relevant or physically unreliable. This suggests that”
- Authors: sants-authors

### EA-WMEVAL-READ-0013

- Claim: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.12403](https://arxiv.org/abs/2606.12403) World Pilot: Steering Vision-Language-Action Models with World-Action Priors
- Locator: Abstract (full-text section)
- Evidence: World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy.
- Quote: “Abstract Vision-Language-Action (VLA) models inherit semantic grounding from large-scale pretraining and perform competently across in-distribution manipulation tasks. This grounding, however, is built on static image-text pairs, whereas manipulation is a continuous, contact-rich process whose dynamics this pretraining cannot capture. We present World Pilot, a VLA framework that augments the policy with priors from a World-Action Model (WAM), routed into the decision chain through two complement”
- Authors: zefu-lin; rongxu-cui; junjia-xu; et al.

### EA-WMEVAL-READ-0006

- Claim: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.01549](https://arxiv.org/abs/2603.01549) Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation
- Locator: VI Discussion, Limitations, and Future Work
- Evidence: The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could further improve robustness.
- Quote: “We presented Pri4R, a framework that enhances the world dynamics understanding of VLA models through privileged 4D representations. By supervising the model to predict 3D point tracks during training, we demonstrated that VLA backbones can develop a more physically-aware context, leading to improved control performance without any inference-time overhead. Our results across various benchmarks suggest that capturing the spatiotemporal evolution of a scene is a critical component for robust robot”
- Authors: jisoo-kim; jungbin-cho; sanghyeok-chu

### EA-WMEVAL-READ-0004

- Claim: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.
- Stance: `gap` | Confidence: `direct`
- Paper: [2605.29360](https://arxiv.org/abs/2605.29360) MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models
- Locator: Abstract (full-text section)
- Evidence: The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias.
- Quote: “Abstract Action-conditioned world models are increasingly used as scalable simulators for robot learning, yet current evaluations provide limited evidence that their predictions are reliable under the actions they condition on. Existing benchmarks largely emphasize visual fidelity, leaving unclear whether predicted futures are physically plausible, faithful to commanded actions, and calibrated to failure when actions should not succeed. We introduce MiraBench , a hierarchical benchmark that defi”
- Authors: tianzhuo-yang; zihan-shen; zirui-mi; et al.

### EA-AGENT-2026-0001

- Claim: ALRM 将高层规划、执行与机器人 API 分层，并通过动作结果回传形成可修订计划的闭环。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.19510](https://arxiv.org/abs/2601.19510) ALRM: Agentic LLM for Robotic Manipulation
- Locator: III LLM-Based Robotic Agent Architecture for Task Planning and Execution
- Evidence: 规划器按思考—动作—观察循环拆解任务，执行器把结果作为观察返回。
- Quote: “These interactive steps continue until the original user task is fulfilled, or it reaches the maximum number of steps.”
- Authors: vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al.

### EA-VLABREAK-2026-0001

- Claim: H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: IV-C Hierarchical World Model Guidance for VLA
- Evidence: 方法定义了逻辑世界模型、视觉世界模型、低层 VLA 和子任务完成检测的两时间尺度接口。
- Quote: “The hierarchical information at multiple abstraction level enables the VLA to maintain consistency with long-horizon task structure while remaining responsive to local visual feedback.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-AGENT-2026-0005

- Claim: 同一高层循环在真实 Mobipick 上运行，并在约一天内通过更换提示与技能绑定迁移到 Valdemar 仿真场景。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.13081](https://arxiv.org/abs/2602.13081) Agentic AI for Robot Control: Flexible but still Fragile
- Locator: 6 Qualitative Validation on a Physical Robot with Simulated Transfer
- Evidence: 迁移发生在高层编排层，低层平台 API 分别存在。
- Quote: “within approximately one day of development effort, the same system was adapted”
- Authors: oscar-lima; marc-vinci; martin-gnther; et al.

### EA-AGENT-2026-0011

- Claim: RACAS 在三类差异显著的机器人上复用同一控制逻辑；适配只需更换机器人、动作和环境的提示配置。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05621](https://arxiv.org/abs/2603.05621) RACAS: Controlling Diverse Robots With a Single Agentic System
- Locator: III-B System Architecture
- Evidence: 轮式、机械肢体和水下平台均完成目标定位任务。
- Quote: “Adapting the system to a new robot requires only replacing the prompt configuration files (the robot description , the action definitions , and the environment context), with no modification to the control logic itself.”
- Authors: dylan-r-ashley; jan-przepira; yimeng-chen; et al.

### EA-VLABREAK-2026-0004

- Claim: StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.12553](https://arxiv.org/abs/2603.12553) Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation
- Locator: pages 5-8, Sections 3.1-3.3
- Evidence: 方法段给出动力学里程碑抽取和 planner-to-action 两阶段优化的完整链路。
- Quote: “Structured frames provide compact progress anchors that connect task intent to executable motion phases.”
- Authors: minghao-jin; mozheng-liao; mingfei-han; et al.

### EA-ALIGN-READ-0015

- Claim: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09630](https://arxiv.org/abs/2606.09630) ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies
- Locator: 1 Introduction
- Evidence: ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classification mistakes 与 perception errors、sim-to-real mismatch 并列为失败来源。
- Quote: “Instead, it produces a structured recovery descriptor containing the failure type, recovery stage, active entities, confidence, and reward mask.”
- Authors: haodi-hu; chung-ta-huang; jing-liu; et al.

### EA-AGENT-2026-0014

- Claim: 具身智能体记忆可显式连接持久对象、场景状态、动作转移和可执行技能，并用前置条件与预期后果约束技能选择。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29774](https://arxiv.org/abs/2606.29774) Analytic Concept-Centric Memory for Agentic Embodied Manipulation
- Locator: 4.4 Memory-Grounded Reasoning and Execution
- Evidence: 方法在检索后检查技能前置条件和预测后果，失败则写回并重检索。
- Quote: “This closes the loop between structured retrieval, state-consistent reasoning, physical execution, and memory update.”
- Authors: mingyang-sun; xiujian-liang; jiude-wei; et al.

### EA-AGENT-2026-0015

- Claim: 在五个真实桌面记忆任务上，结构化记忆相对关键帧检索把平均成功率从 56% 提至 84%，检索准确率从 68% 提至 98%，检索努力从 4.5 降至 1.3。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29774](https://arxiv.org/abs/2606.29774) Analytic Concept-Centric Memory for Agentic Embodied Manipulation
- Locator: 5.3 Real-World Memory Evaluation; Table 3
- Evidence: 最大增益出现在需要对象身份、场景关系和状态转移的任务。
- Quote: “our method improves the average success rate from 56% to 84%”
- Authors: mingyang-sun; xiujian-liang; jiude-wei; et al.

### EA-AGENT-2026-0002

- Claim: 在该 56 指令仿真基准上，Claude-4.1-Opus 的 TaP 成功率为 93.5%，CaP 为 92.6%，但平均延迟由 33.44 秒增至 82.60 秒。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.19510](https://arxiv.org/abs/2601.19510) ALRM: Agentic LLM for Robotic Manipulation
- Locator: VI-A Operation Mode Comparison
- Evidence: 同一模型在两种执行接口上的成功率差异很小，而延迟超过两倍。
- Quote: “Claude-4.1-Opus reached the highest average success rate using TaP (93.5%), representing a 0.9% improvement over CaP, while latency increased from 33.44s to 82.60s.”
- Authors: vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al.

### EA-VLABREAK-2026-0002

- Claim: 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: VI Results
- Evidence: H-WM 为 64.8%，logic-only 为 48.4%，H-WM-Stable-Diffusion 为 54.4%。
- Quote: “Incorporating visual guidance yields consistent additional gains, providing more than 10% further improvement in Q-score and 17% in success rate.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-AGENT-2026-0004

- Claim: 该架构把 LLM 限制在高层决策和技能调用；真实部署的前提是平台已有完整低层栈、语义状态快照及结构化成功/失败信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13081](https://arxiv.org/abs/2602.13081) Agentic AI for Robot Control: Flexible but still Fragile
- Locator: Real-World Execution Prerequisites
- Evidence: 论文逐项列出导航、感知、抓取、运动规划、监控和技能返回要求。
- Quote: “the architectural requirement remains an action API exposing executable skills and returning structured success or failure signals.”
- Authors: oscar-lima; marc-vinci; martin-gnther; et al.

### EA-AGENT-2026-0009

- Claim: 在该实验中，情景记忆对任务成功率的作用因模型和任务而异，结论不确定；较稳定的收益是减少工具调用。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.03148](https://arxiv.org/abs/2603.03148) From Language to Action: Can LLM-Based Agents Be Used for Embodied Robot Cognition?
- Locator: IV-D Benefits of Memory on Planning
- Evidence: 部分模型改善、部分任务下降；工具调用数总体减少。
- Quote: “the overall effect of the memory on the task completion success is inconclusive”
- Authors: shinas-shaji; fabian-huppertz; alex-mitrevski; et al.

### EA-AGENT-2026-0010

- Claim: 模型可在占位空间、已占用位置等工具失败后自行重规划，但恢复过程仍可能受幻觉影响而产生新的失败。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.03148](https://arxiv.org/abs/2603.03148) From Language to Action: Can LLM-Based Agents Be Used for Embodied Robot Cognition?
- Locator: IV-E Qualitative Observations
- Evidence: 定性观察同时记录自动恢复与恢复后误判。
- Quote: “the models tend to automatically replan without any human intervention”
- Authors: shinas-shaji; fabian-huppertz; alex-mitrevski; et al.

### EA-VLABREAK-2026-0005

- Claim: 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.12553](https://arxiv.org/abs/2603.12553) Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation
- Locator: page 11
- Evidence: LIBERO 平均为 94.8%；实机 tidy-up 为 8/10，相同表面的 UniVLA 为 4/10。
- Quote: “StructVLA completes8/10trials,comparedwith4/10forUniVLAand2/10forSpatialVLA, indicating stronger stability over extended execution.”
- Authors: minghao-jin; mozheng-liao; mingfei-han; et al.

### EA-ALIGN-READ-0006

- Claim: ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.03784](https://arxiv.org/abs/2606.03784) Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。
- Quote: “Abstract Embodied chain-of-thought (CoT) aims to bridge linguistic reasoning with robotic control, yet its effective form and integration remain underexplored. In this paper, we revisit embodied CoT for robotic control at an unprecedented scale. We curate the largest embodied CoT corpus to date, comprising 978,743 trajectories, 226.3M samples, and 2592.5 hours of data. Through extensive experiments, we show that effective CoT must ground high-level semantic understaning in concrete linguistic ac”
- Authors: nan-sun; yuan-zhang; yongkun-yang; et al.

### EA-AGENT-2026-0003

- Claim: 该研究不能证明真实机器人部署可靠性，因为主要评测使用占位位姿和动作序列代理，作者也把真实机器人与感知整合列为后续工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.19510](https://arxiv.org/abs/2601.19510) ALRM: Agentic LLM for Robotic Manipulation
- Locator: V-C Evaluation Design; VII Conclusion
- Evidence: 评测目标是高层动作质量，不覆盖真实动力学、感知和连续运行。
- Quote: “integrating real robots and perception components would offer a clearer understanding”
- Authors: vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al.

### EA-VLABREAK-2026-0003

- Claim: H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: VII Conclusion
- Evidence: 结论明确列出额外组件/训练阶段的代价，以及对符号化状态的依赖。
- Quote: “The logical world model depends on structured logical state representations, which assume that the task can be meaningfully formulated in a symbolic logical space.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-AGENT-2026-0006

- Claim: 长时执行仍会出现陈旧世界状态、提示约束违背、非确定性选择和不规则事件检查，因此灵活性没有转化为可预测可靠性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.13081](https://arxiv.org/abs/2602.13081) Agentic AI for Robot Control: Flexible but still Fragile
- Locator: Abstract — cross-platform proof-of-concept fragility statement
- Evidence: 多组实验分别暴露盲放、过期位姿、充电目标随机和事件检查不稳定。
- Quote: “Across both platforms, our proof-of-concept experiments reveal substantial fragility, including non-deterministic suboptimal behaviour, instruction-following errors, and high sensitivity to prompt specification.”
- Authors: oscar-lima; marc-vinci; martin-gnther; et al.

### EA-AGENT-2026-0007

- Claim: 基于轮询的事件检测无法在长动作中即时抢占；物理安全需要并发监控、可取消技能或把动作切成可中断检查点。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.13081](https://arxiv.org/abs/2602.13081) Agentic AI for Robot Control: Flexible but still Fragile
- Locator: 7 Conclusions
- Evidence: 作者明确说明同步工具循环和现代智能体框架缺乏统一中断原语。
- Quote: “Most contemporary LLM agent frameworks do not provide hard preemption”
- Authors: oscar-lima; marc-vinci; martin-gnther; et al.

### EA-AGENT-2026-0008

- Claim: LLM 机器人智能体会在任务未真实完成时相信自己成功；这种误报会直接污染以自报结果标注的情景记忆。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.03148](https://arxiv.org/abs/2603.03148) From Language to Action: Can LLM-Based Agents Be Used for Embodied Robot Cognition?
- Locator: IV-D Benefits of Memory on Planning
- Evidence: 论文用仿真世界状态对比模型自报状态，并观察到过度自信与错误记忆标签。
- Quote: “this is possible because memories are labelled with the agent’s belief about its execution success, and this belief can be hallucinated.”
- Authors: shinas-shaji; fabian-huppertz; alex-mitrevski; et al.

### EA-AGENT-2026-0012

- Claim: 当前系统约每 5–10 秒才执行一个动作；作者认为这种逐步推理成本让长时接触操作实验慢到不可行。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05621](https://arxiv.org/abs/2603.05621) RACAS: Controlling Diverse Robots With a Single Agentic System
- Locator: IV-D Implementation Details; VII LIMITATIONS AND FUTURE WORK
- Evidence: 时延由 API 推理主导，作者建议把操作原语作为更粗粒度工具。
- Quote: “The control loop executes at approximately one action per 5–10 seconds”
- Authors: dylan-r-ashley; jan-przepira; yimeng-chen; et al.

### EA-AGENT-2026-0013

- Claim: 缺少显式深度使 VLM 对碰撞风险的判断过度或不足自信，说明自然语言视觉接口不能替代安全几何感知。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05621](https://arxiv.org/abs/2603.05621) RACAS: Controlling Diverse Robots With a Single Agentic System
- Locator: VII LIMITATIONS AND FUTURE WORK
- Evidence: 作者把深度不足列为持续损害系统能力的问题。
- Quote: “such inferences were sub-optimal”
- Authors: dylan-r-ashley; jan-przepira; yimeng-chen; et al.

### EA-ALIGN-READ-0001

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: 3.2 Inconsistency of Control Commands across Robots
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Quote: “Recent work has scaled robot learning by training policies on data from multiple embodiments [ 27 , 23 , 32 ] , often using the Cartesian delta action space [ 23 , 32 ] since it is less dependent on robot-specific kinematics and invariant to base-frame translation [ 18 , 14 ] . In practice, this is typically realized by predicting Cartesian delta control commands that are fed to the underlying robot controller [ 23 , 32 ] . Figure 2: Different robots (e.g., UR5 vs. Franka Research 3) require dif”
- Authors: haeone-lee

### EA-AGENT-2026-0016

- Claim: 该记忆路线尚未证明可变形物和强感知/状态漂移下的鲁棒性，模板库覆盖是重要边界。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.29774](https://arxiv.org/abs/2606.29774) Analytic Concept-Centric Memory for Agentic Embodied Manipulation
- Locator: 6 Conclusion
- Evidence: 作者把扩展可变形物与抵抗感知噪声、状态漂移列为未来工作。
- Quote: “improve robustness to perception noise and state drift”
- Authors: mingyang-sun; xiujian-liang; jiude-wei; et al.

### EA-ALIGN-READ-0003

- Claim: Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under different robot states and contacts.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30113](https://arxiv.org/abs/2606.30113) SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance
- Locator: Abstract (full-text section)
- Evidence: SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines.
- Quote: “Abstract Discrete action tokenization provides a compact interface for autoregressive VLA policies, but accurately recovering continuous robot actions from discrete codes remains challenging. Existing tokenizers typically map each discrete code to a fixed continuous action prototype, ignoring the robot’s current proprioceptive state. This limitation is particularly pronounced in manipulation, where the same action token may require different continuous controls under different joint configuratio”
- Authors: tengyue-jiang; chunpu-xu; jiayue-kang; et al.

### EA-ALIGN-READ-0004

- Claim: Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30456](https://arxiv.org/abs/2606.30456) Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform
- Locator: Abstract (full-text section)
- Evidence: The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone.
- Quote: “Instead, it is strongly influenced by a combination of factors, including action semantics, coordinate frame conventions, temporal alignment between modalities, image preprocessing consistency, and dataset coverage and quality. These observations lead to a key interpretation: the successful deployment of VLA systems in real-world settings depends less on incremental improvements in model capacity and more on precise control of the entire data–model–control pipeline.”
- Authors: mathilde-hochedel; marc-lalonde

### EA-ALIGN-READ-0009

- Claim: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: 5 Conclusion and Limitations
- Evidence: 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。
- Quote: “We presented TACO, a tactile-aware world-model-driven framework for scalable VLA post-training in contact-rich manipulation. Following a Recognize–Imagine–Label loop, TACO converts real-world failures into imagined corrections without repeated human intervention: a tactile-aware world model jointly denoises future video and force sequences, while a unified progress-action model recognizes failure-adjacent states and labels imagined segments with corrective actions. To incorporate this supervisio”
- Authors: shengbang-liu; yueru-jia; yuyang-yan; et al.

### EA-VLABREAK-2026-0006

- Claim: 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.15207](https://arxiv.org/abs/2607.15207) BadWAM: When World-Action Models Dream Right but Act Wrong
- Locator: 5.2 BadWAM Reliably Induces Task Failures
- Evidence: 主实验在 40 个 LIBERO 任务、每任务 20 次试验上使用闭环攻击，并报告任务族级下降。
- Quote: “On the action-only WAM, the action-only attack lowers success to 43.1%, a 53.4% drop.”
- Authors: qi-li; xingyi-yang; xinchao-wang

### EA-VLABREAK-2026-0007

- Claim: 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.15207](https://arxiv.org/abs/2607.15207) BadWAM: When World-Action Models Dream Right but Act Wrong
- Locator: 5.8 What Do These Results Imply for WAM Safety?
- Evidence: 想象保持攻击在 40 个任务中有 39 个降低未来漂移，同时保留显著攻击强度。
- Quote: “The relevant security property is not plausibility of the imagined future in isolation, but synchronization between the imagined future and the action that will actually be executed.”
- Authors: qi-li; xingyi-yang; xinchao-wang

## References

- `2601.19510` [ALRM: Agentic LLM for Robotic Manipulation](https://arxiv.org/abs/2601.19510) (2026-01-27)
- `2602.11291` [H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model](https://arxiv.org/abs/2602.11291) (2026-02-11T19:08:36Z)
- `2602.13081` [Agentic AI for Robot Control: Flexible but still Fragile](https://arxiv.org/abs/2602.13081) (2026-02-13)
- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.03148` [From Language to Action: Can LLM-Based Agents Be Used for Embodied Robot Cognition?](https://arxiv.org/abs/2603.03148) (2026-03-03)
- `2603.05621` [RACAS: Controlling Diverse Robots With a Single Agentic System](https://arxiv.org/abs/2603.05621) (2026-03-05)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.08546` [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546) (2026-03-09)
- `2603.12553` [Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation](https://arxiv.org/abs/2603.12553) (2026-03-13T01:33:48Z)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2604.11386` [ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation](https://arxiv.org/abs/2604.11386) (2026-04-13)
- `2604.21741` [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](https://arxiv.org/abs/2604.21741) (2026-04-23)
- `2605.00121` [Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes](https://arxiv.org/abs/2605.00121) (2026-04-30)
- `2605.20752` [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](https://arxiv.org/abs/2605.20752) (2026-05-20)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.27947` [SANTS: A State-Adaptive Scheduler for World Action Models](https://arxiv.org/abs/2605.27947) (2026-05-27)
- `2605.29360` [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360) (2026-05-28)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.02577` [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](https://arxiv.org/abs/2606.02577) (2026-06-01)
- `2606.03784` [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](https://arxiv.org/abs/2606.03784) (2026-06-02)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.09630` [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630) (2026-06-08)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.12403` [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403) (2026-06-10)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2606.29774` [Analytic Concept-Centric Memory for Agentic Embodied Manipulation](https://arxiv.org/abs/2606.29774) (2026-06-29)
- `2606.30113` [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113) (2026-06-29)
- `2606.30456` [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456) (2026-06-29)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.15207` [BadWAM: When World-Action Models Dream Right but Act Wrong](https://arxiv.org/abs/2607.15207) (2026-07-16T17:04:15Z)
