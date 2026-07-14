# Evidence Appendix: 4D时空推理

- Time range: 2026-01-14..2026-07-14
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DATA-READ-0014

- Claim: MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD observation and fuses the generated views into a more complete 3D structure over time.
- Stance: `support` | Confidence: `direct`
- Paper: [2602.09878](https://arxiv.org/abs/2602.09878) MVISTA-4D: View-Consistent 4D World Model with Test-Time Action Inference for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: The abstract describes single-view RGBD input, arbitrary-view RGBD generation, and back-projection/fusion as the route to complete time-varying 3D structure.
- Quote: “Abstract World-model-based imagine-then-act becomes a promising paradigm for robotic manipulation, yet existing approaches typically support either purely image-based forecasting or reasoning over partial 3D geometry, limiting their ability to predict complete 4D scene dynamics. To solve this, this work explores a novel embodied 4D world model that enables geometrically consistent, arbitrary-view RGBD generation: given only a single-view RGBD observation as input, the model “imagines” the remain”
- Authors: jiaxu-wang; yicheng-jiang; tianlun-he; et al.

### EA-DATA-READ-0005

- Claim: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Abstract (full-text section)
- Evidence: The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap futures.
- Quote: “Abstract Simulating robot-world interactions is a cornerstone of Embodied AI. Recently, a few works have shown promise in leveraging video generations to transcend the rigid visual/physical constraints of traditional simulators. However, they primarily operate in 2D space or are guided by static environmental cues, ignoring the fundamental reality that robot-world interactions are inherently 4D spatiotemporal events that require precise interactive modeling. To restore this 4D essence while ensu”
- Authors: mutian-xu; tianbao-zhang; tianqi-liu; et al.

### EA-DATA-READ-0015

- Claim: Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.01799](https://arxiv.org/abs/2605.01799) Embody4D: A Generalist Data Engine for Embodied 4D World Modeling
- Locator: Abstract (full-text section)
- Evidence: The abstract ties fixed or sparse viewpoints to partial observations and introduces both novel-view video generation and a compositional synthesis pipeline to address data scarcity.
- Quote: “Abstract Embodied agents require robust and comprehensive 3D spatiotemporal representations to support spatial reasoning, manipulation understanding, and downstream decision making. However, existing robot data are typically captured from fixed or sparse viewpoints, providing only partial and view-dependent observations, which limits multi-view perception and generalization across viewpoints. Given the difficulty of collecting additional viewpoints in real-world settings, we propose Embody4D, a”
- Authors: peiyan-tu; hanxin-zhu; jingwen-sun; et al.

### EA-DATA-READ-0008

- Claim: GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autoregressive rollout.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.17682](https://arxiv.org/abs/2605.17682) GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning
- Locator: 1 Introduction
- Evidence: The paper decouples spatial geometry, temporal support, semantics, opacity, and motion in Gaussian primitives, then slices and splats them into future occupancy volumes at arbitrary timestamps and supervises both occupancy and planned ego trajectories.
- Quote: “It also delivers comparable or better motion planning performance, with competitive trajectory accuracy and lower collision rates, while retaining an explicit and continuously queryable Gaussian world representation. We summarize our contributions are as follows: • We introduce GEM , a vision-centric, non-autoregressive occupancy world model that represents dynamic driving scenes as evolving 4D semantic Gaussian primitives. • We propose a structured continuous-time Gaussian formulation that deco”
- Authors: cheng-chen; hao-huang; saurabh-bagchi

### EA-DATA-READ-0004

- Claim: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into executable trajectories; the paper reports real-world manipulation success improving from 61% to 81%.
- Quote: “Abstract Video world models can generate realistic futures from a single instruction, but they often fail to track the same physical points consistently across time. As a result, the generated videos appear plausible, yet lack the physical grounding required for reliable action execution, such as robot manipulation. We present GEM-4D , a geometry-grounded video world model that resolves this limitation by injecting dense 4D correspondence supervision distilled from a pretrained geometry foundati”
- Authors: kaichen-zhou; yuzhen-chen; fangneng-zhan; et al.

### EA-DATA-READ-0013

- Claim: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: 3.1. Problem Formulation
- Evidence: 问题建模段先定义动作与视觉未来的联合分布，再明确把未来触觉纳入联合预测目标。
- Quote: “Building on these two formulations, a world action model combines action prediction and future observation prediction into a unified framework. Specifically, it jointly models (3) or equivalently factorizes the joint distribution as (4) where future visual prediction provides predictive structure for action generation. However, in contact-rich manipulation, vision alone is often insufficient to capture physical interaction cues. To address this limitation, we introduce Dream-Tac, an enhanced wor”
- Authors: yunfan-lou; yifan-ye; yankai-fu; et al.

### EA-DATA-READ-0003

- Claim: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13672](https://arxiv.org/abs/2606.13672) $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- Locator: 3 WEAVER : World Estimation Across Views for Embodied Reasoning
- Evidence: The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthetic policy improvement, and test-time planning.
- Quote: “Figure 2 : WEAVER Architecture. Left: The world model encodes memory, history, and action sequences to image future rollouts in latent space. Middle: The latent verifier, equipped with reward and critic heads, selects samples with high advantage to steer the policy distribution. Right: Decoded generation corresponding to different outcomes of action sequences. We now describe the key ingredients in WEAVER : a robot world model designed to support policy evaluation, policy improvement, and test-t”
- Authors: arnav-kumar-jain; yilin-wu; jesse-farebrother; et al.

### EA-DATA-READ-0012

- Claim: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction
- Evidence: 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。
- Quote: “The primary advantage of 3PoinTr is that it trains on data General Flow ignores. Real-world points are often temporarily occluded; General Flow removes any trajectory with invisible point-timestep pairs during preprocessing, whereas 3PoinTr retains all trajectories and masks losses for individual invisible point-timestep pairs. This provides additional supervision over task-critical object points that are temporarily occluded during manipulation. For example, in the Throw Away Paper task, every”
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### EA-DATA-READ-0002

- Claim: τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接列出四类交互数据和 modality-specific supervision masks。
- Quote: “Abstract Robotic manipulation requires models that generate executable actions while anticipating and evaluating their future consequences before physical execution. We present -World Model ( -WM), a unified video-action world model that integrates policy learning, video prediction, and action evaluation within a single future-predictive framework. Built on a shared video diffusion backbone, -WM provides two complementary interfaces. First, a video action model jointly predicts future visual lat”
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### EA-DATA-READ-0010

- Claim: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control
- Evidence: 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。
- Quote: “All data modalities are synchronized through the robot control loop. For policy learning, actions are converted to a unified 7D end-effector delta representation (1) where are translational deltas, are rotational deltas, and is the gripper command. This decouples learning from the exact robot configuration, enabling cross-embodiment by focusing the policy on local contact adjustment from tactile feedback. Several quality checks are applied to every collected trajectory. Empty or corrupted trajec”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### EA-DATA-READ-0011

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Quote: “Policies in this setting are trained using both nominal demonstrations and recovery interaction data.”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### EA-DATA-READ-0006

- Claim: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.00121](https://arxiv.org/abs/2605.00121) Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes
- Locator: VIII Limitations
- Evidence: The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and planning.
- Quote: “While embedding open-vocabulary scene graphs with persistence estimators yields tempo-spatio-semantic capabilities, our approach is not free of limitations. First, object-receptacle edges are modelled independently. While joint distributions over multiple locations are possible [ 30 ] , inference costs grow with the number of observed locations per object, inducing a trade-off between expressivity and real-time performance. We believe that striking the right balance in this trade-off is a promis”
- Authors: miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta

### EA-DATA-READ-0007

- Claim: DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.29879](https://arxiv.org/abs/2605.29879) DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding
- Locator: V Conclusion
- Evidence: The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs.
- Quote: “Nevertheless, the system still relies on SLAM pose accuracy for initial reconstruction and ACE training, and its scalability to large-scale outdoor scenes is limited by the storage and GPU memory costs of 3D Gaussians.”
- Authors: luzhou-ge; xiangyu-zhu; jinyan-liu; et al.

### EA-DATA-READ-0001

- Claim: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.01549](https://arxiv.org/abs/2603.01549) Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation
- Locator: VI Discussion, Limitations, and Future Work
- Evidence: The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could further improve robustness.
- Quote: “We presented Pri4R, a framework that enhances the world dynamics understanding of VLA models through privileged 4D representations. By supervising the model to predict 3D point tracks during training, we demonstrated that VLA backbones can develop a more physically-aware context, leading to improved control performance without any inference-time overhead. Our results across various benchmarks suggest that capturing the spatiotemporal evolution of a scene is a critical component for robust robot”
- Authors: jisoo-kim; jungbin-cho; sanghyeok-chu; et al.

### EA-DATA-READ-0009

- Claim: UMI 夹爪手指的力分布会显著改变操作者的任务表现和示教质量，说明数据采集硬件本身是学习管线需要优化的一部分。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: V DISCUSSION
- Evidence: 讨论段报告集中载荷夹爪优于分布载荷夹爪，并将小幅硬件改动与示教质量及后续策略学习联系起来。
- Quote: “Overall, the usability study demonstrated that altering the force distribution of UMI gripper fingers significantly affected participants’ ability to open bandage packages, with concentrated load grippers outperforming distributed load grippers. These findings highlight that subtle hardware changes can substantially improve demonstration quality and, in turn, the robot control policies learned from them. Accordingly, perceived workload was highest with the distributed load grippers. No significa”
- Authors: gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al.

## References

- `2602.09878` [MVISTA-4D: View-Consistent 4D World Model with Test-Time Action Inference for Robotic Manipulation](https://arxiv.org/abs/2602.09878) (2026-02-10)
- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17)
- `2605.00121` [Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes](https://arxiv.org/abs/2605.00121) (2026-04-30)
- `2605.01799` [Embody4D: A Generalist Data Engine for Embodied 4D World Modeling](https://arxiv.org/abs/2605.01799) (2026-05-03)
- `2605.17682` [GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning](https://arxiv.org/abs/2605.17682) (2026-05-17)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.29879` [DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding](https://arxiv.org/abs/2605.29879) (2026-05-28)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
