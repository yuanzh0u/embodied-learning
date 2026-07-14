# Evidence Appendix: 世界模型评测边界

- Time range: 2026-01-14..2026-07-14
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

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

### EA-WMEVAL-READ-0002

- Claim: For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before execution.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.15549](https://arxiv.org/abs/2602.15549) VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing
- Locator: Abstract (full-text section)
- Evidence: VLM-DEWM validates each VLM decision against a persistent world model and uses discrepancy analysis for targeted recovery, with reported gains in state tracking and recovery success in long-horizon manufacturing tasks.
- Quote: “Abstract Vision-language model (VLM) shows promise for high-level planning in smart manufacturing, yet their deployment in dynamic workcells faces two critical challenges: (1) stateless operation—they cannot persistently track out-of-view states, causing world-state drift; and (2) opaque reasoning—failures are difficult to diagnose, leading to costly blind retries. This paper presents VLM-DEWM, a cognitive architecture that decouples VLM reasoning from world-state management through a persistent”
- Authors: guoqin-tang; qingxuan-jia; gang-chen; et al.

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

### EA-WMEVAL-READ-0012

- Claim: Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM feedback as weak verification.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.12072](https://arxiv.org/abs/2606.12072) World Model Self-Distillation: Training World Models to Solve General Tasks
- Locator: Abstract (full-text section)
- Evidence: WMSD frames supervised fine-tuning on paired task-execution videos as costly, then proposes self-distillation and reinforcement learning where a VLM generates tasks/solutions from unlabeled scene images and feedback verifies sampled videos.
- Quote: “Abstract Pretrained video generators are promising visual world models that exhibit emergent task-solving abilities; however, their reliance on detailed textual descriptions limits their direct use for planning and decision-making. Existing approaches either outsource this reasoning to language or vision-language models, or rely on supervised fine-tuning with paired task-execution videos, which are costly to collect and difficult to scale. We propose a scalable framework that elicits task-solvin”
- Authors: sebastian-stapf; pablo-acuaviva-huertos; aram-davtyan; et al.

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

### EA-WMEVAL-READ-0009

- Claim: DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.29879](https://arxiv.org/abs/2605.29879) DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding
- Locator: V Conclusion
- Evidence: The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs.
- Quote: “Nevertheless, the system still relies on SLAM pose accuracy for initial reconstruction and ACE training, and its scalability to large-scale outdoor scenes is limited by the storage and GPU memory costs of 3D Gaussians.”
- Authors: luzhou-ge; xiangyu-zhu; jinyan-liu

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

## References

- `2602.15549` [VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing](https://arxiv.org/abs/2602.15549) (2026-02-17)
- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2604.11386` [ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation](https://arxiv.org/abs/2604.11386) (2026-04-13)
- `2605.00121` [Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes](https://arxiv.org/abs/2605.00121) (2026-04-30)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.27947` [SANTS: A State-Adaptive Scheduler for World Action Models](https://arxiv.org/abs/2605.27947) (2026-05-27)
- `2605.29360` [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360) (2026-05-28)
- `2605.29879` [DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding](https://arxiv.org/abs/2605.29879) (2026-05-28)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.02577` [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](https://arxiv.org/abs/2606.02577) (2026-06-01)
- `2606.12072` [World Model Self-Distillation: Training World Models to Solve General Tasks](https://arxiv.org/abs/2606.12072) (2026-06-10)
- `2606.12403` [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403) (2026-06-10)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
