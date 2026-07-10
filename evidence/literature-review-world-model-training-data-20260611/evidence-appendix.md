# Evidence Appendix: 世界模型训练数据

- Time range: 2025-12-11..2026-06-11
- Events: 14
- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。

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

### EA-DATA-2026-WMDATA-0005

- Claim: Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation demonstrations, because off-the-shelf generative models can hallucinate robot bodies or implausible motions.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.11797](https://arxiv.org/abs/2512.11797) AnchorDream: Repurposing Video Diffusion for Embodiment-Aware Robot Data Synthesis
- Locator: Abstract; I Introduction; IV-A2 Training setup; IV-C Can scaling AnchorDream data help?; V Conclusion
- Evidence: AnchorDream conditions video diffusion on robot motion renderings, starts from a small set of human teleoperation demonstrations, and frames embodiment grounding as necessary to avoid implausible motions while scaling diverse datasets.
- Authors: junjie-ye

### EA-DATA-2026-WMDATA-0006

- Claim: A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenario coverage.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.11386](https://arxiv.org/abs/2604.11386) ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation
- Locator: Abstract; 1 Introduction; 3.1 Problem Formulation; 3.2 Real2Sim Data Collection; 5 Conclusion
- Evidence: ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate large-scale action-video training datasets.
- Authors: yiran-qin

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

### EA-EVAL-2026-WMDATA-0013

- Claim: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.27947](https://arxiv.org/abs/2605.27947) SANTS: A State-Adaptive Scheduler for World Action Models
- Locator: Abstract; 1 Introduction; 3.3 Path-Level Reward and Scheduler Post-Training; 6 Conclusion
- Evidence: SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video fidelity.
- Authors: sants-authors

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

### EA-MODEL-2026-WMDATA-0010

- Claim: World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to task-relevant interaction regions.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.12217](https://arxiv.org/abs/2606.12217) Making Foresight Actionable: Repurposing Representation Alignment in World Action Models
- Locator: Abstract; 1 Introduction; 3 AGRA; 3.3 Repurposing Representation Alignment for Action Grounding
- Evidence: The paper diagnoses a representation mismatch in WAMs, where action decoders attend to task-irrelevant areas despite plausible visual futures, and proposes an Action-Grounded Representation Alignment objective for the world-action interface.
- Authors: yuying-ge

## References

- `2512.11797` [AnchorDream: Repurposing Video Diffusion for Embodiment-Aware Robot Data Synthesis](https://arxiv.org/abs/2512.11797) (2025-12-12)
- `2603.08546` [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546) (2026-03-09)
- `2604.11386` [ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation](https://arxiv.org/abs/2604.11386) (2026-04-13)
- `2604.21741` [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](https://arxiv.org/abs/2604.21741) (2026-04-23)
- `2605.20752` [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](https://arxiv.org/abs/2605.20752) (2026-05-20)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.27947` [SANTS: A State-Adaptive Scheduler for World Action Models](https://arxiv.org/abs/2605.27947) (2026-05-27)
- `2606.00113` [World Models for Robotic Manipulation: A Survey](https://arxiv.org/abs/2606.00113) (2026-05-27)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [τ0-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.02577` [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](https://arxiv.org/abs/2606.02577) (2026-06-01)
- `2606.12072` [World Model Self-Distillation: Training World Models to Solve General Tasks](https://arxiv.org/abs/2606.12072) (2026-06-10)
- `2606.12217` [Making Foresight Actionable: Repurposing Representation Alignment in World Action Models](https://arxiv.org/abs/2606.12217) (2026-06-10)
- `2606.12403` [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403) (2026-06-10)
