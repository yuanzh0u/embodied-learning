# Evidence Appendix: 世界模型需要什么样的训练数据

- Time range: 2026-01-14..2026-07-14
- Events: 39
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DATA-2026-WMDATA-0001

- Claim: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-real correlation.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08546](https://arxiv.org/abs/2603.08546) Interactive World Simulator for Robot Policy Training and Evaluation
- Locator: Abstract; I Introduction; IV-C Data Generation for Policy Training; IV-D Sim-to-Real Correlation for Faithful Policy Evaluation
- Evidence: The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real performance correlation.
- Authors: yixuan-wang

### EA-DATA-2026-WMDATA-0003

- Claim: World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations.
- Stance: `support` | Confidence: `direct`
- Paper: [2604.21741](https://arxiv.org/abs/2604.21741) Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training
- Locator: Abstract; 1 Introduction; 3.5 Collecting Corrective Trajectories for Post-Training; 4.3 Policy Performance via Hi-WM
- Evidence: Hi-WM rolls policies inside a world model, lets humans intervene when rollouts become incorrect or failure-prone, caches and branches failure states, and adds corrective trajectories back into the training set for post-training.
- Authors: yaxuan-li

### EA-DATA-2026-WMDATA-0014

- Claim: A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under intervention, with modalities beyond RGB when physical interaction variables are otherwise hidden.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00113](https://arxiv.org/abs/2606.00113) World Models for Robotic Manipulation: A Survey
- Locator: Abstract; I Introduction; VII Datasets for World-Model Learning; VII-C Demonstration Collection and Imitation Learning; VII-E Multimodal and Contact-Rich Data
- Evidence: The survey distinguishes ordinary policy datasets from world-model datasets, reviews 34 manipulation datasets, and states that useful world-model data should include temporally aligned observations/actions, diversity for counterfactual generalization, and modalities revealing relevant physical variables such as contact-rich signals.
- Authors: wm-manipulation-survey-authors

### EA-DATA-2026-WMDATA-0002

- Claim: Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations, broad egocentric human videos, and rollout or failure trajectories with modality-specific supervision masks.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) τ0-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract; I Introduction; III Data Sources for Predictive Robot Learning; IV-C Joint Flow-Matching Objective; Appendix A.1 Training Configuration
- Evidence: τ0-WM reports a 27.3K-hour corpus containing real-robot teleoperation, UMI-style interaction, egocentric human videos, and rollout/failure trajectories; the paper explains that these sources differ in action fidelity, embodiment, viewpoint, cost, and behavioral diversity, and uses supervision masks for missing modalities.
- Authors: pengfei-zhou

### EA-DATA-2026-4D-0007

- Claim: Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial constraints and motion priors.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Supplementary Material; The underlying logic behind 4D pseudo annotation
- Evidence: The supplementary discussion says ST-v2 pseudo-annotations may not be absolute sub-millimeter ground truth, but are sufficiently high-fidelity for relative spatial geometry; the authors prioritize breadth of data to learn generalizable motion priors.
- Authors: mutian-xu; tianbao-zhang; tianqi-liu

### EA-DATA-2026-WMDATA-0006

- Claim: A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenario coverage.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.11386](https://arxiv.org/abs/2604.11386) ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation
- Locator: Abstract; 1 Introduction; 3.1 Problem Formulation; 3.2 Real2Sim Data Collection; 5 Conclusion
- Evidence: ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate large-scale action-video training datasets.
- Authors: yiran-qin

### EA-DATA-2026-4D-0011

- Claim: τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: I Introduction; Data Mixture and Supervision
- Evidence: The introduction contrasts broad visual dynamics in egocentric and human interaction video with narrow but executable robot demonstrations, then uses modality-specific supervision masks so each data source supervises only the signals it contains.
- Authors: pengfei-zhou; shengcong-chen; di-chen

### EA-DATA-2026-WMDATA-0004

- Claim: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing teleoperation burden.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.02577](https://arxiv.org/abs/2606.02577) RoboDream: Compositional World Models for Scalable Robot Data Synthesis
- Locator: Abstract; I Introduction; III-D Deployment Modes; IV-C Prop-Free vs. Real Data Collection; VI Conclusion
- Evidence: RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost.
- Authors: junjie-ye

### EA-DATA-2026-WMDATA-0012

- Claim: Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM feedback as weak verification.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.12072](https://arxiv.org/abs/2606.12072) World Model Self-Distillation: Training World Models to Solve General Tasks
- Locator: Abstract; 1 Introduction; Task-Conditioned World Models; 4.7 Generalization to Robotic Tasks; 4.8 Discussion & Limitations
- Evidence: WMSD frames supervised fine-tuning on paired task-execution videos as costly, then proposes self-distillation and reinforcement learning where a VLM generates tasks/solutions from unlabeled scene images and feedback verifies sampled videos.
- Authors: sebastian-stapf

### EA-DATA-2026-WMDATA-0011

- Claim: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.12403](https://arxiv.org/abs/2606.12403) World Pilot: Steering Vision-Language-Action Models with World-Action Priors
- Locator: Abstract; 1 Introduction; World-Action Models; 3.1 Problem Formulation; 3.2 Latent Steering
- Evidence: World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy.
- Authors: world-pilot-authors

### EA-EVAL-2026-4D-0004

- Claim: Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only prediction, or dense depth prediction.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.01549](https://arxiv.org/abs/2603.01549) Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation
- Locator: V Experiments; Temporality & Spatiality; Spatial redundancy; Table III
- Evidence: The paper compares supervision targets and reports that full-horizon 3D point-track supervision gives larger RoboCasa gains than 2D tracks, goal-only prediction, environment-only points, robot-only points, or future depth-map prediction.
- Authors: jisoo-kim; jungbin-cho; sanghyeok-chu

### EA-EVAL-2026-4D-0006

- Claim: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Abstract; 1 Introduction; 3 Our Approach
- Evidence: The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap futures.
- Authors: mutian-xu; tianbao-zhang; tianqi-liu

### EA-EVAL-2026-4D-0013

- Claim: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13672](https://arxiv.org/abs/2606.13672) $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- Locator: Abstract; 1 Introduction; 3 WEAVER
- Evidence: The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthetic policy improvement, and test-time planning.
- Authors: arnav-kumar-jain; yilin-wu; jesse-farebrother

### EA-EVAL-2026-SMOKE-0004

- Claim: For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before execution.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.15549](https://arxiv.org/abs/2602.15549) VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing
- Locator: Abstract; 1 Introduction; Methodology
- Evidence: VLM-DEWM validates each VLM decision against a persistent world model and uses discrepancy analysis for targeted recovery, with reported gains in state tracking and recovery success in long-horizon manufacturing tasks.
- Authors: guoqin-tang

### EA-EVAL-2026-4D-0002

- Claim: ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset, masking pipeline, and task setup.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.13788](https://arxiv.org/abs/2603.13788) ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation
- Locator: 4 Experimental Results; 5 Conclusion and Discussion
- Evidence: The evaluation reports 44.6% zero-shot success-rate gains in simulation and 30.3% real-world gains, while the conclusion notes degradation risks in extreme clutter and dependence on single-view execution and SAM2 segmentation.
- Authors: you-wu; zixuan-chen; cunxu-ou

### EA-EVAL-2026-MEMO-0006

- Claim: Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic frame dropping can remove exactly the events downstream policies need.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.00664](https://arxiv.org/abs/2606.00664) SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models
- Locator: Abstract; 1 Introduction
- Evidence: The paper argues that pixel-space rollout is expensive, but indiscriminate frame dropping is misaligned with embodied manipulation because critical task events may involve only small visual changes and become unrecoverable if omitted.
- Authors: ziheng-he

### EA-EVAL-2026-4D-0012

- Claim: τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensing, uncertainty estimation, longer horizons, and harder contact tasks as future needs.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: V Experiments; VIII Conclusion and Future Work
- Evidence: The experiments report better performance on long-horizon real-robot tasks, data-mixture gains, and a single-attempt success-rate increase from 0.43 to 0.60 with action selection plus rectification; the conclusion notes remaining needs for tactile feedback, better uncertainty, longer-horizon evaluation, and complex manipulation.
- Authors: pengfei-zhou; shengcong-chen; di-chen

### EA-EVAL-2026-SMOKE-0003

- Claim: A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action candidates.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) τ0-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract; I Introduction
- Evidence: The paper presents a unified video-action world model that combines policy learning, video prediction, and action evaluation, using test-time sampling, ranking, and simulator-based rectification before execution.
- Authors: pengfei-zhou

### EA-EVAL-2026-SMOKE-0005

- Claim: External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometry-only checks do not verify dynamics or kinematics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.15549](https://arxiv.org/abs/2602.15549) VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing
- Locator: 4.4.2 Limitations and Failure Mode Analysis; Scope of Physical Verification (Dynamics Gap)
- Evidence: The limitations section identifies upstream perception errors, open-vocabulary failures under closed-world assumptions, and a dynamics gap in the physical verification scope.
- Authors: guoqin-tang

### EA-EVAL-2026-WMDATA-0013

- Claim: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.27947](https://arxiv.org/abs/2605.27947) SANTS: A State-Adaptive Scheduler for World Action Models
- Locator: Abstract; 1 Introduction; 3.3 Path-Level Reward and Scheduler Post-Training; 6 Conclusion
- Evidence: SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video fidelity.
- Authors: sants-authors

### EA-EVAL-2026-SMOKE-0002

- Claim: Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following do not establish robotic trustworthiness.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.01600](https://arxiv.org/abs/2606.01600) RoboTrustBench: Benchmarking the Trustworthiness of Video World Models for Robotic Manipulation
- Locator: Abstract; Evaluation Dimensions; Analysis of Trustworthiness Failures
- Evidence: RoboTrustBench evaluates video world models with four scenario types and a six-dimensional protocol, reporting failures in constraint reasoning, counterfactual grounding, physical interaction, and unsafe-instruction suppression.
- Authors: huiqiong-li

### EA-EVAL-2026-4D-0014

- Claim: WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, data coverage, and noisy reward supervision can all break imagined rollout reliability.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.13672](https://arxiv.org/abs/2606.13672) $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- Locator: 6 Conclusion; A5 Limitations
- Evidence: The limitations section states that visual observations expose only partial physical state; tactile, force-torque, or depth sensing may be needed; deformable and granular dynamics remain difficult; latency restricts planning to near-term action chunks; and reward labels can be noisy.
- Authors: arnav-kumar-jain; yilin-wu; jesse-farebrother

### EA-EVAL-2026-4D-0020

- Claim: EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual scenes.
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.15467](https://arxiv.org/abs/2603.15467) Evaluating Time Awareness and Cross-modal Active Perception of Large Models via 4D Escape Room Task
- Locator: Abstract; 1 Introduction; 3.1 Overview of EscapeCraft-4D; 6 Conclusion
- Evidence: The benchmark introduces time-varying visual and audio cues, trigger-based evidence, and time-limited clues; results show models degrade under modality bias, missed triggers, and time-sensitive decisions, indicating gaps not captured by conventional static multimodal benchmarks.
- Authors: yurui-dong; ziyue-wang; shuyun-lu

### EA-EVAL-2026-SMOKE-0001

- Claim: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.
- Stance: `gap` | Confidence: `direct`
- Paper: [2605.29360](https://arxiv.org/abs/2605.29360) MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models
- Locator: Abstract; Problem Formulation; Design of MIRABENCH
- Evidence: The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias.
- Authors: tianzhuo-yang

### EA-MODEL-2026-4D-0003

- Claim: Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geometry evolves over time.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.01549](https://arxiv.org/abs/2603.01549) Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation
- Locator: Abstract; I Introduction; IV Pri4R: Learning World Dynamics via Privileged 4D Representations
- Evidence: The authors state that action labels tell a policy how to move but not what will happen; Pri4R adds a point-track head during training and discards it at inference, leaving the original VLA interface unchanged.
- Authors: jisoo-kim; jungbin-cho; sanghyeok-chu

### EA-MODEL-2026-4D-0001

- Claim: ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories and 4D temporal context.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13788](https://arxiv.org/abs/2603.13788) ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation
- Locator: Abstract; 1 Introduction; 3 Methodology
- Evidence: The paper argues that 2D intermediate representations lose depth and temporal continuity, then proposes unified 3D-4D representations with trajectories and smooth spatial masks for online replanning and long-horizon execution.
- Authors: you-wu; zixuan-chen; cunxu-ou

### EA-MODEL-2026-4D-0009

- Claim: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: Abstract; 3 Method; 4 Experiments; 5 Conclusion
- Evidence: The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into executable trajectories; the paper reports real-world manipulation success improving from 61% to 81%.
- Authors: kaichen-zhou; yuzhen-chen; fangneng-zhan

### EA-MODEL-2026-WMDATA-0008

- Claim: World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: Abstract; 1 Introduction; 2.2 Feed-Forward 3D and 4D Geometry Models; 3 GEM-4D; 3.1 Problem Formulation
- Evidence: GEM-4D injects dense 4D correspondence supervision from a geometry foundation model into a video generative backbone during training, arguing that correspondence consistency makes future rollouts more reliable for action extraction.
- Authors: gem-4d-authors

### EA-MODEL-2026-WMDATA-0009

- Claim: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon future evolution rather than only behavior-cloning actions.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.20752](https://arxiv.org/abs/2605.20752) GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation
- Locator: Abstract; 1 Introduction; 3D-enhanced manipulation policies; 3.1 Overview of GaussianDream; 3.4 GaussianDream Training and Efficient Inference
- Evidence: GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference.
- Authors: gaussiandream-authors

### EA-MODEL-2026-WMDATA-0007

- Claim: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information downstream policies need.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00664](https://arxiv.org/abs/2606.00664) SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models
- Locator: Abstract; 1 Introduction; 3.2 SKIP-Selector and SKIP-Generator; 4.3 Replacing real demonstrations; 5 Conclusion
- Evidence: SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as policy-training data.
- Authors: ziheng-he

### EA-MODEL-2026-4D-0010

- Claim: τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, then revise low-quality candidates before execution.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract; I Introduction; Action-Conditioned Video Simulator
- Evidence: The paper describes a unified video-action world model with a video action model and an action-conditioned video simulator; at inference it samples candidates, ranks them, simulates futures, estimates progress, and rectifies actions.
- Authors: pengfei-zhou; shengcong-chen; di-chen

### EA-MODEL-2026-4D-0008

- Claim: GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences over time.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: Abstract; 1 Introduction
- Evidence: The introduction says photorealistic generated videos can have drifting contacts, inconsistent depth, and non-rigid deformation artifacts that break action extraction; pixel or latent losses do not guarantee correspondence consistency.
- Authors: kaichen-zhou; yuzhen-chen; fangneng-zhan

### EA-MODEL-2026-WMDATA-0010

- Claim: World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to task-relevant interaction regions.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.12217](https://arxiv.org/abs/2606.12217) Making Foresight Actionable: Repurposing Representation Alignment in World Action Models
- Locator: Abstract; 1 Introduction; 3 AGRA; 3.3 Repurposing Representation Alignment for Action Grounding
- Evidence: The paper diagnoses a representation mismatch in WAMs, where action decoders attend to task-irrelevant areas despite plausible visual futures, and proposes an Action-Grounded Representation Alignment objective for the world-action interface.
- Authors: yuying-ge

### EA-MODEL-2026-4D-0005

- Claim: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.01549](https://arxiv.org/abs/2603.01549) Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation
- Locator: Conclusion
- Evidence: The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could further improve robustness.
- Authors: jisoo-kim; jungbin-cho; sanghyeok-chu

### EA-SENSOR-2026-4D-0015

- Claim: PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-receptacle states and plan navigation accordingly.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.00121](https://arxiv.org/abs/2605.00121) Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes
- Locator: Abstract; V-C Embodied LLM Planning; VI Evaluation; VII Conclusion
- Evidence: The paper builds Perpetua* Bayesian persistence filters into a 3D scene graph, validates future state prediction in simulation and a three-week real-world semi-static lab setting, and shows navigation can avoid an expected blocked path.
- Authors: miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta

### EA-SENSOR-2026-4D-0019

- Claim: GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autoregressive rollout.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.17682](https://arxiv.org/abs/2605.17682) GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning
- Locator: Abstract; 1 Introduction; 2.2 Continuous Decoupled 4D Gaussian World Model; 4 Conclusion
- Evidence: The paper decouples spatial geometry, temporal support, semantics, opacity, and motion in Gaussian primitives, then slices and splats them into future occupancy volumes at arbitrary timestamps and supervises both occupancy and planned ego trajectories.
- Authors: cheng-chen; hao-huang; saurabh-bagchi

### EA-SENSOR-2026-4D-0017

- Claim: DGSG-Mind combines dynamic 3D Gaussian mapping with scene graphs so that embodied agents can update object-level topology and reason over spatial-semantic relations in changing environments.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.29879](https://arxiv.org/abs/2605.29879) DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding
- Locator: Abstract; I Introduction; III-E Dynamic Scene Update; III-F 3D Gaussian Mind
- Evidence: The system fuses probabilistic voxels and 3D Gaussians, performs Gaussian-based camera relocalization and localized masked refinement for additions/removals, synchronizes graph nodes, and uses annotated Gaussian renderings plus scene graph context for zero-shot 3D grounding.
- Authors: luzhou-ge; xiangyu-zhu; jinyan-liu

### EA-SENSOR-2026-4D-0016

- Claim: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.00121](https://arxiv.org/abs/2605.00121) Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes
- Locator: VIII Limitations
- Evidence: The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and planning.
- Authors: miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta

### EA-SENSOR-2026-4D-0018

- Claim: DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.29879](https://arxiv.org/abs/2605.29879) DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding
- Locator: V Conclusion
- Evidence: The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs.
- Authors: luzhou-ge; xiangyu-zhu; jinyan-liu

## References

- `2602.15549` [VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing](https://arxiv.org/abs/2602.15549) (2026-02-17)
- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.08546` [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546) (2026-03-09)
- `2603.13788` [ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation](https://arxiv.org/abs/2603.13788) (2026-03-14)
- `2603.15467` [Evaluating Time Awareness and Cross-modal Active Perception of Large Models via 4D Escape Room Task](https://arxiv.org/abs/2603.15467) (2026-03-16)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2604.11386` [ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation](https://arxiv.org/abs/2604.11386) (2026-04-13)
- `2604.21741` [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](https://arxiv.org/abs/2604.21741) (2026-04-23)
- `2605.00121` [Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes](https://arxiv.org/abs/2605.00121) (2026-04-30)
- `2605.17682` [GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning](https://arxiv.org/abs/2605.17682) (2026-05-17)
- `2605.20752` [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](https://arxiv.org/abs/2605.20752) (2026-05-20)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.27947` [SANTS: A State-Adaptive Scheduler for World Action Models](https://arxiv.org/abs/2605.27947) (2026-05-27)
- `2605.29360` [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360) (2026-05-28)
- `2605.29879` [DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding](https://arxiv.org/abs/2605.29879) (2026-05-28)
- `2606.00113` [World Models for Robotic Manipulation: A Survey](https://arxiv.org/abs/2606.00113) (2026-05-27)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.01600` [RoboTrustBench: Benchmarking the Trustworthiness of Video World Models for Robotic Manipulation](https://arxiv.org/abs/2606.01600) (2026-06-01)
- `2606.02577` [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](https://arxiv.org/abs/2606.02577) (2026-06-01)
- `2606.12072` [World Model Self-Distillation: Training World Models to Solve General Tasks](https://arxiv.org/abs/2606.12072) (2026-06-10)
- `2606.12217` [Making Foresight Actionable: Repurposing Representation Alignment in World Action Models](https://arxiv.org/abs/2606.12217) (2026-06-10)
- `2606.12403` [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403) (2026-06-10)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
