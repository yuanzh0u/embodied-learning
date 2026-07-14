# Evidence Appendix: 4D时空推理

- Time range: 2026-01-14..2026-07-14
- Events: 40
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DATA-2026-4DDATA-0001

- Claim: 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: Abstract; 1 Introduction; 4.1 Data collection; 4.4 Results
- Evidence: 3PoinTr先从无动作人类视频学习非 embodiment 点的密集3D点轨迹，再用20条机器人动作示教训练闭环策略；论文报告真实任务平均成功率相对最强基线提高25.0个百分点。
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### EA-DATA-2026-4DDATA-0005

- Claim: 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Abstract; 1 Introduction; 3.1 Kinematics Control; 3.2 4D Generative Modeling; 3.3 Robo4D-200k
- Evidence: Kinema4D用URDF/重建机器人经正逆运动学产生4D robot pointmap控制信号，再训练模型生成同步RGB和pointmap未来；其Robo4D-200k包含201,426个带高质量4D标注的交互episode。
- Authors: mutian-xu; tianbao-zhang; tianqi-liu

### EA-DATA-2026-4DDATA-0008

- Claim: 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: 2.2 Feed-Forward 3D and 4D Geometry Models; 3.2.3 Correspondence Distillation via Geometry Flow; 5 Conclusion
- Evidence: GEM-4D冻结几何基础模型，提取稠密几何表示作为correspondence teacher，并通过geometry flow把监督蒸馏进视频backbone；训练后几何分支丢弃，推理仍是单流视频生成。
- Authors: kaichen-zhou; yuzhen-chen; fangneng-zhan

### EA-DATA-2026-4DDATA-0009

- Claim: 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract; III Data Sources for Predictive Robot Learning; A Training Configuration
- Evidence: τ0-WM构建27.3K小时语料：17.8K小时真实机器人远程操作、6.5K小时UMI式示教、3.0K小时开源第一视角人类交互视频，并用rollout或失败轨迹训练任务进度/低质量结果评估。
- Authors: pengfei-zhou; shengcong-chen; di-chen

### EA-DATA-2026-4DDATA-0017

- Claim: 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: Abstract; 3.1 Dataset Statistics; 4 Data Collection Platform; 4.3 Haptic Feedback to the Operator
- Evidence: HapTile提供1,726条示教、38个任务、9类技能，15Hz同步语言、视觉、触觉、机器人状态和动作；其teleoperation平台还将触觉marker motion转成操作者侧haptic feedback。
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu

### EA-DATA-2026-4DDATA-0004

- Claim: 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.01549](https://arxiv.org/abs/2603.01549) Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation
- Locator: IV-B Why 3D Point Tracks as Privileged Supervision; S.III-A Additional Analysis on input; S.III-C Additional Ablations
- Evidence: Pri4R比较多种监督目标，认为3D点轨迹兼具时间密集、几何度量和空间稀疏；附录中1024个点优于256/512点，且没有当前点云输入会退化，因为模型必须凭空生成而非预测给定场景演化。
- Authors: jisoo-kim; jungbin-cho; sanghyeok-chu

### EA-DATA-2026-4DDATA-0002

- Claim: 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction; Appendix D Data Collection Details; Appendix G Future Work
- Evidence: 论文用可见性mask保留部分遮挡轨迹并逐点逐时刻mask损失，认为这比丢弃含不可见点的轨迹能提供更多任务关键监督；附录说明真实视频需2D跟踪、深度提升到3D、SAM3分割人手并移除embodiment点。
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### EA-DATA-2026-4D-0007

- Claim: Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial constraints and motion priors.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Supplementary Material; The underlying logic behind 4D pseudo annotation
- Evidence: The supplementary discussion says ST-v2 pseudo-annotations may not be absolute sub-millimeter ground truth, but are sufficiently high-fidelity for relative spatial geometry; the authors prioritize breadth of data to learn generalizable motion priors.
- Authors: mutian-xu; tianbao-zhang; tianqi-liu

### EA-DATA-2026-4DDATA-0006

- Claim: 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Supplementary G.2 Dataset; Acquisition of LIBERO simulated data; The underlying logic behind 4D pseudo annotation
- Evidence: Kinema4D补充材料说明ST-v2生成的4D伪标注未必达到绝对亚毫米真值，但足以学习相对几何；LIBERO数据生成中还从成功轨迹注入不同强度动作噪声，合成九种失败轨迹。
- Authors: mutian-xu; tianbao-zhang; tianqi-liu

### EA-DATA-2026-4D-0011

- Claim: τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: I Introduction; Data Mixture and Supervision
- Evidence: The introduction contrasts broad visual dynamics in egocentric and human interaction video with narrow but executable robot demonstrations, then uses modality-specific supervision masks so each data source supervises only the signals it contains.
- Authors: pengfei-zhou; shengcong-chen; di-chen

### EA-DATA-2026-4DDATA-0010

- Claim: 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: I Introduction; III Data Sources for Predictive Robot Learning; Unified supervision; IV-C Joint Flow-Matching Objective
- Evidence: 论文把真实robot data、UMI-style data和egocentric videos划分为不同监督等级，并用modality-specific supervision masks让每条样本只参与其实际拥有的视觉、状态、动作和进度损失。
- Authors: pengfei-zhou; shengcong-chen; di-chen

### EA-DATA-2026-4DDATA-0018

- Claim: 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control; A.1 Data Formatting; A.2 Tactile Sensor Data Processing
- Evidence: HapTile说明所有模态通过机器人控制循环同步，检查空/损坏轨迹和timestamp gaps，验证action-state consistency；附录还要求episode-level split避免temporal leakage，并保留raw/rectified tactile images。
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu

### EA-DATA-2026-4DDATA-0016

- Claim: 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: 3.3 Contact-Aware Self Attention; A.6 Contact Gate Statistics
- Evidence: Dream-Tac的contact gate直接从左右指尖触觉RGB的帧间平均绝对差得到，经过鲁棒归一化后在接触变化时提高触觉token注意力；附录统计显示大多数变化很小，较大变化对应关键交互事件。
- Authors: yunfan-lou; yifan-ye; yankai-fu

### EA-DATA-2026-4DDATA-0014

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation; IV-C Main Results; Table I
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Authors: yujie-zang; yuhang-zheng; xian-nie

### EA-DATA-2026-4DDATA-0019

- Claim: 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: Abstract; II-A Performance and Usability Limitations; V Discussion; VI Conclusion
- Evidence: 该研究在医用绷带打开任务中比较不同UMI夹爪条件和裸手，发现集中载荷夹爪优于分布载荷夹爪，但仍明显慢于手；作者强调力分布、刚度和人体工学会影响示教质量和工作负荷。
- Authors: gina-l-georgadarellis; natalija-beslic; seonhun-lee

### EA-DATA-2026-4DDATA-0020

- Claim: 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: II-A Performance and Usability Limitations; V Discussion; VI Conclusion
- Evidence: 作者指出UMI完整学习流程通常至少需要200条固定环境任务示教，手持夹爪仍可能比裸手慢；研究中的夹爪未集成完整传感/marker pipeline，后续需把传感和跟踪能力纳入完整示教到机器人流程评估。
- Authors: gina-l-georgadarellis; natalija-beslic; seonhun-lee

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

### EA-EVAL-2026-4DDATA-0011

- Claim: 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13672](https://arxiv.org/abs/2606.13672) $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- Locator: 3 WEAVER; 3.1 Key Design Decisions; 3.3 Accurate and Efficient Value Estimation; 4 Experimental Setup
- Evidence: WEAVER在DROID上预训练并在真实任务数据上微调，输入右侧外部相机和腕部相机、proprioceptive state、action plan、memory/history latents，并蒸馏奖励/critic头来快速评分候选动作。
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

### EA-MODEL-2026-4DDATA-0003

- Claim: 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.01549](https://arxiv.org/abs/2603.01549) Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation
- Locator: I Introduction; IV Pri4R: Learning World Dynamics via Privileged 4D Representations; IV-C Construction of 3D Point Track Supervision
- Evidence: Pri4R指出动作标签主要鼓励模仿示教动作，但不给出世界动态；它给VLA添加点轨迹头，监督未来3D位移，训练后丢弃辅助头而不增加推理输入和计算。
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

### EA-MODEL-2026-4DDATA-0007

- Claim: 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: Abstract; 1 Introduction; 3.1 Problem Formulation; 3.2.1 What Governs Inter-Frame Correspondence
- Evidence: GEM-4D指出像素或latent重建损失不能保证对应一致，可能出现接触漂移、深度不一致和非刚性变形；这些视觉上微妙的错误会破坏从视频rollout提取动作。
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

### EA-SENSOR-2026-4DDATA-0015

- Claim: 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: Abstract; 3.1 Problem Formulation; 3.2 Dream-Tac Architecture; 3.3 Contact-Aware Self Attention
- Evidence: Dream-Tac把当前视觉/触觉/语言作为条件，联合去噪未来视觉、未来触觉和动作chunk；其contact-aware self-attention用相邻触觉帧变化计算事件门控，强调接触发生、滑移或释放等时刻。
- Authors: yunfan-lou; yifan-ye; yankai-fu

### EA-SENSOR-2026-4DDATA-0013

- Claim: 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: Abstract; III-A Force-conditioned Tactile World Model; IV-D 1 World Model Conditioning; Table II
- Evidence: TacForeSight训练force-conditioned tactile world model，用高频wrist force/torque条件预测短时未来触觉latent；作者报告wrist wrench条件在MSE、cosine similarity和KL上优于无条件、RGB和机器人状态条件。
- Authors: yujie-zang; yuhang-zheng; xian-nie

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

### EA-SENSOR-2026-4DDATA-0012

- Claim: 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.13672](https://arxiv.org/abs/2606.13672) $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- Locator: A5 Limitations; A5.1 Partial Observability; A5.2 Complex Deformable and Dynamic Interactions; A5.4 Data Coverage and Embodiment Diversity; A5.5 Noisy Reward Supervision
- Evidence: WEAVER限制部分指出视觉只给部分物理状态，任务相关的接触、力和遮挡几何可能不可见；形变/动态物体、有限规划时域、DROID embodiment覆盖、以及reward labels噪声都是剩余瓶颈。
- Authors: arnav-kumar-jain; yilin-wu; jesse-farebrother

## References

- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.13788` [ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation](https://arxiv.org/abs/2603.13788) (2026-03-14)
- `2603.15467` [Evaluating Time Awareness and Cross-modal Active Perception of Large Models via 4D Escape Room Task](https://arxiv.org/abs/2603.15467) (2026-03-16)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17)
- `2605.00121` [Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes](https://arxiv.org/abs/2605.00121) (2026-04-30)
- `2605.17682` [GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning](https://arxiv.org/abs/2605.17682) (2026-05-17)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.29879` [DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding](https://arxiv.org/abs/2605.29879) (2026-05-28)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
