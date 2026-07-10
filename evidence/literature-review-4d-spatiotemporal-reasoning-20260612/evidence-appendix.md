# Evidence Appendix: 4D 时空推理

- Time range: 2025-12-12..2026-06-12
- Events: 20
- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。

### EA-DATA-2026-4D-0007

- Claim: Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial constraints and motion priors.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Supplementary Material; The underlying logic behind 4D pseudo annotation
- Evidence: The supplementary discussion says ST-v2 pseudo-annotations may not be absolute sub-millimeter ground truth, but are sufficiently high-fidelity for relative spatial geometry; the authors prioritize breadth of data to learn generalizable motion priors.
- Authors: mutian-xu; tianbao-zhang; tianqi-liu

### EA-DATA-2026-4D-0011

- Claim: τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: I Introduction; Data Mixture and Supervision
- Evidence: The introduction contrasts broad visual dynamics in egocentric and human interaction video with narrow but executable robot demonstrations, then uses modality-specific supervision masks so each data source supervises only the signals it contains.
- Authors: pengfei-zhou; shengcong-chen; di-chen

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

### EA-EVAL-2026-4D-0002

- Claim: ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset, masking pipeline, and task setup.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.13788](https://arxiv.org/abs/2603.13788) ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation
- Locator: 4 Experimental Results; 5 Conclusion and Discussion
- Evidence: The evaluation reports 44.6% zero-shot success-rate gains in simulation and 30.3% real-world gains, while the conclusion notes degradation risks in extreme clutter and dependence on single-view execution and SAM2 segmentation.
- Authors: you-wu; zixuan-chen; cunxu-ou

### EA-EVAL-2026-4D-0012

- Claim: τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensing, uncertainty estimation, longer horizons, and harder contact tasks as future needs.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: V Experiments; VIII Conclusion and Future Work
- Evidence: The experiments report better performance on long-horizon real-robot tasks, data-mixture gains, and a single-attempt success-rate increase from 0.43 to 0.60 with action selection plus rectification; the conclusion notes remaining needs for tactile feedback, better uncertainty, longer-horizon evaluation, and complex manipulation.
- Authors: pengfei-zhou; shengcong-chen; di-chen

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

- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.13788` [ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation](https://arxiv.org/abs/2603.13788) (2026-03-14)
- `2603.15467` [Evaluating Time Awareness and Cross-modal Active Perception of Large Models via 4D Escape Room Task](https://arxiv.org/abs/2603.15467) (2026-03-16)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2605.00121` [Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes](https://arxiv.org/abs/2605.00121) (2026-04-30)
- `2605.17682` [GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning](https://arxiv.org/abs/2605.17682) (2026-05-17)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.29879` [DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding](https://arxiv.org/abs/2605.29879) (2026-05-28)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
