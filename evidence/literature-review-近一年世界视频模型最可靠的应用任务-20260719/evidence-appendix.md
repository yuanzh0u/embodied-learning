# Evidence Appendix: 近一年世界视频模型最可靠的应用任务

- Time range: 2025-07-19..2026-07-19
- Events: 31
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

### EA-EGO-2026-0003

- Claim: 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: III-C Policy Training
- Evidence: 策略训练段明确说明 gripper state 缺失，并以 object pose displacement 作为替代动作。
- Quote: “Because gripper states cannot be obtained from Section III-B , each action is represented by a 9-dimensional vector”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-CONTAM-2026-0007

- Claim: LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.03827](https://arxiv.org/abs/2510.03827) LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization
- Locator: 5.2 Main Results
- Evidence: LIBERO-PRO 在保持逻辑可执行的前提下改变物体位置与任务，标准设置中的高分模型在这些轻微改变下近乎崩溃。
- Quote: “Despite achieving success rates above 90% on the standard LIBERO benchmark, models nearly collapse under changes to object positions or minor task modifications, even when constructed from training components.”
- Authors: xueyang-zhou; yangming-xu; guiyao-tie; et al.

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

### EA-WMTASK-2026-0001

- Claim: In the DROID/RoboArena setting, a closed-loop video-world-model evaluator produced a policy ranking that closely matched the real-robot leaderboard across the evaluated policies, supporting policy ranking as a conditional high-reliability application rather than a universal replacement for real evaluation.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.01060](https://arxiv.org/abs/2607.01060) RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation
- Locator: 5.3 Correlation with Real World Evaluation
- Evidence: The paper runs the same policies from RoboArena initial observations entirely inside RoboWorld and reports strong positive agreement between the induced ranking and the real leaderboard; the claim is bounded to the eight evaluated policies and the DROID/RoboArena setup.
- Quote: “The resulting policy ranking closely matches the real-world leaderboard under GPT-4o scoring.”
- Authors: byeongguk-jeon; seonghyeon-ye; jaehyeok-doo; et al.

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

### EA-WMTASK-2026-0002

- Claim: RoboWorld's principal qualitative failures occur after object contact, when manipulated objects may disintegrate, morph unrealistically, or become visually inconsistent, limiting contact-rich manipulation evaluation and direct control use.
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.01060](https://arxiv.org/abs/2607.01060) RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation
- Locator: E.3 Failure Case Analysis
- Evidence: The appendix contrasts stable pre-contact scenes with post-contact artifacts and identifies contact-rich object dynamics as a key remaining limitation.
- Quote: “Before contact, the generated scene is typically stable, but after the robot begins manipulating the object, the object may disintegrate, morph into unrealistic shapes, or become visually inconsistent.”
- Authors: byeongguk-jeon; seonghyeon-ye; jaehyeok-doo; et al.

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

### EA-ALIGN-READ-0013

- Claim: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.09708](https://arxiv.org/abs/2601.09708) Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning
- Locator: 5 Conclusion
- Evidence: 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。
- Quote: “By distilling lengthy textual reasoning into compact latent representations via preference-guided distillation and visual trajectory alignment, our approach bridges high-level embodied reasoning with low-level action execution through reasoning-enhanced policy learning. Extensive experiments across diverse robotic manipulation and embodied reasoning benchmarks demonstrate that Fast-ThinkAct achieves strong performance with significantly reduced inference latency while enabling effective long-hor”
- Authors: chi-pin-huang; yunze-man; zhiding-yu; et al.

### EA-ALIGN-READ-0015

- Claim: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09630](https://arxiv.org/abs/2606.09630) ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies
- Locator: 1 Introduction
- Evidence: ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classification mistakes 与 perception errors、sim-to-real mismatch 并列为失败来源。
- Quote: “Instead, it produces a structured recovery descriptor containing the failure type, recovery stage, active entities, confidence, and reward mask.”
- Authors: haodi-hu; chung-ta-huang; jing-liu; et al.

### EA-ALIGN-READ-0006

- Claim: ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.03784](https://arxiv.org/abs/2606.03784) Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。
- Quote: “Abstract Embodied chain-of-thought (CoT) aims to bridge linguistic reasoning with robotic control, yet its effective form and integration remain underexplored. In this paper, we revisit embodied CoT for robotic control at an unprecedented scale. We curate the largest embodied CoT corpus to date, comprising 978,743 trajectories, 226.3M samples, and 2592.5 hours of data. Through extensive experiments, we show that effective CoT must ground high-level semantic understaning in concrete linguistic ac”
- Authors: nan-sun; yuan-zhang; yongkun-yang; et al.

### EA-ALIGN-READ-0001

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: 3.2 Inconsistency of Control Commands across Robots
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Quote: “Recent work has scaled robot learning by training policies on data from multiple embodiments [ 27 , 23 , 32 ] , often using the Cartesian delta action space [ 23 , 32 ] since it is less dependent on robot-specific kinematics and invariant to base-frame translation [ 18 , 14 ] . In practice, this is typically realized by predicting Cartesian delta control commands that are fed to the underlying robot controller [ 23 , 32 ] . Figure 2: Different robots (e.g., UR5 vs. Franka Research 3) require dif”
- Authors: haeone-lee

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

## References

- `2509.21986` [Developing Vision-Language-Action Model from Egocentric Videos](https://arxiv.org/abs/2509.21986) (2025-09-26T07:09:33Z)
- `2510.03827` [LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization](https://arxiv.org/abs/2510.03827) (2025-10-04)
- `2601.09708` [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](https://arxiv.org/abs/2601.09708) (2026-01-14)
- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.08546` [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546) (2026-03-09)
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
- `2606.30113` [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113) (2026-06-29)
- `2606.30456` [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456) (2026-06-29)
- `2607.00673` [Path Planning in Physically Viable World Models](https://arxiv.org/abs/2607.00673) (2026-07-01)
- `2607.01060` [RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation](https://arxiv.org/abs/2607.01060) (2026-07-01T15:22:41Z)
- `2607.02642` [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
