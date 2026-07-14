# Evidence Appendix: 具身智能数据质量的主要矛盾

- Time range: 2026-01-14..2026-07-14
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DQ-CONTRA-READ-0008

- Claim: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: V DISCUSSION
- Evidence: 论文指出 UMI 示教虽快于遥操作但仍比手工慢、工具重量会造成疲劳并影响 demonstration；实验中改变 UMI gripper fingers 的力分布显著影响打开绷带包装表现，concentrated load grippers 优于 distributed load grippers，作者将其连接到 demonstration quality 和 learned robot control policies。
- Quote: “Overall, the usability study demonstrated that altering the force distribution of UMI gripper fingers significantly affected participants’ ability to open bandage packages, with concentrated load grippers outperforming distributed load grippers. These findings highlight that subtle hardware changes can substantially improve demonstration quality and, in turn, the robot control policies learned from them.”
- Authors: gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al.

### EA-DQ-CONTRA-READ-0003

- Claim: World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: GEM-4D injects dense 4D correspondence supervision from a geometry foundation model into a video generative backbone during training, arguing that correspondence consistency makes future rollouts more reliable for action extraction.
- Quote: “Abstract Video world models can generate realistic futures from a single instruction, but they often fail to track the same physical points consistently across time. As a result, the generated videos appear plausible, yet lack the physical grounding required for reliable action execution, such as robot manipulation. We present GEM-4D , a geometry-grounded video world model that resolves this limitation by injecting dense 4D correspondence supervision distilled from a pretrained geometry foundati”
- Authors: kaichen-zhou; yuzhen-chen; fangneng-zhan; et al.

### EA-DQ-CONTRA-READ-0007

- Claim: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) τ0-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接报告了异构数据组成与 modality-specific supervision masks。
- Quote: “Abstract Robotic manipulation requires models that generate executable actions while anticipating and evaluating their future consequences before physical execution. We present -World Model ( -WM), a unified video-action world model that integrates policy learning, video prediction, and action evaluation within a single future-predictive framework. Built on a shared video diffusion backbone, -WM provides two complementary interfaces. First, a video action model jointly predicts future visual lat”
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### EA-DQ-CONTRA-READ-0004

- Claim: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02642](https://arxiv.org/abs/2607.02642) GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation
- Locator: Abstract (full-text section)
- Evidence: 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-training 共同决定。
- Quote: “Using WMBench, we analyze 7 video world models, 4 action representation schemes, and over 324,000 simulated policy rollouts paired with real robot executions, further enriching our analysis with large-scale community submissions from the CVPR 2026 GigaBrain Challenge, curated synthetic trajectories, and a training videos spanning more than 12,000 hours. Our experiments deliver three core insights: evaluator quality is dominated by long-horizon, action-faithful rollout consistency rather than sho”
- Authors: gigaworld-team; angyuan-ma; boyuan-wang; et al.

### EA-DQ-CONTRA-READ-0005

- Claim: 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05390](https://arxiv.org/abs/2607.05390) Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models
- Locator: Abstract (full-text section)
- Evidence: 论文认为形变物体有高维状态和复杂材料属性，接触诱发的局部形变常被末端执行器或物体遮挡；已有数据集常缺对象多样性、依赖合成数据，或缺高保真标注与接触形变。Deform360 采集 198 个日常物体、1,980 个交互序列、215 小时以上数据、41 个环视相机和双臂触觉 UMI gripper，并用 markerless 3D tracking 提取稠密几何与运动。
- Quote: “To address this, we present Deform360, a large-scale visuotactile dataset featuring 198 daily-life objects, 1,980 interaction sequences, and over 215 hours of observations from 41 surround-view cameras and bimanual tactile grippers to capture both global motion and contact-induced local deformations. Leveraging a novel markerless visuotactile 3D tracking pipeline to extract dense geometry and motion, we systematically evaluate current state-of-the-art world models, comparing 2D video models agai”
- Authors: hongyu-li; wanjia-fu; xiaoyan-cong; et al.

### EA-DQ-CONTRA-READ-0006

- Claim: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06564](https://arxiv.org/abs/2607.06564) Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation
- Locator: I Introduction
- Evidence: 引言将操作需求归结为显式 3D 结构与时间一致性，并说明纯 2D 管线及有损的跨模态变换会削弱这些约束。
- Quote: “Despite this progress, robotic manipulation fundamentally requires spatial reasoning in the physical world [ 57 , 82 , 12 , 13 , 59 ] : the robot must infer 3D structure, reason about geometric relationships (e.g., reachability, occlusion, and contact), and plan actions that remain temporally consistent as the geometry evolves. Purely 2D VLA pipelines often struggle to reliably capture these geometric constraints, particularly in cluttered or dynamic environments. A natural direction is to expli”
- Authors: jiaming-liu; qingpo-wuwu; nuowei-han; et al.

### EA-DQ-CONTRA-READ-0013

- Claim: VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.10618](https://arxiv.org/abs/2602.10618) From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks
- Locator: 1 Introduction
- Evidence: 论文指出 VR 用于记录机器人学习示教时，visual fidelity 可能不如 user behavior 的 quality/reliability 重要；输入设备与可视化会影响工作负荷、运动效率、不必要动作和执行精度。实验发现 controller 与 motion-capture gloves 在 pick-and-place 与 manner-oriented tasks 上呈现不同轨迹策略和权衡。
- Quote: “In contrast, when VR is used to record demonstrations for robot learning, visual fidelity may be less important than the quality and reliability of user behavior during task execution.”
- Authors: robin-beierling; manuel-scheibl; jonas-dech; et al.

### EA-DQ-CONTRA-READ-0014

- Claim: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: 3.3 Trajectory and Grasp Filtering via Simulation
- Evidence: PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。
- Quote: “Now that we have converted the human demonstrations into 6 DoF object pose trajectories, the next step is to execute them on a robot in simulation. This serves two purposes. One is to filter out those that may not be suitable for robot learning. There are two main reasons a trajectory may be unsuitable. First, pose estimation errors can lead to inaccurate trajectories. Second, the extracted trajectory may not be physically achievable by the robot. In either case, it would be harmful to train the”
- Authors: albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al.

### EA-DQ-CONTRA-READ-0009

- Claim: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing teleoperation burden.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.02577](https://arxiv.org/abs/2606.02577) RoboDream: Compositional World Models for Scalable Robot Data Synthesis
- Locator: Abstract (full-text section)
- Evidence: RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost.
- Quote: “Abstract Scaling robot learning requires large-scale, diverse demonstrations, yet real-world data collection via teleoperation remains prohibitively expensive and time-consuming. While video diffusion models offer a promising avenue for data scaling, existing generative approaches are often limited to superficial visual augmentation, or suffer from embodiment hallucinations that yield physically infeasible motions. We present a generalizable embodiment-centric world model that achieves scalable”
- Authors: junjie-ye; rong-xue; basile-van-hoorick; et al.

### EA-DQ-CONTRA-READ-0010

- Claim: Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM feedback as weak verification.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.12072](https://arxiv.org/abs/2606.12072) World Model Self-Distillation: Training World Models to Solve General Tasks
- Locator: Abstract (full-text section)
- Evidence: WMSD frames supervised fine-tuning on paired task-execution videos as costly, then proposes self-distillation and reinforcement learning where a VLM generates tasks/solutions from unlabeled scene images and feedback verifies sampled videos.
- Quote: “Abstract Pretrained video generators are promising visual world models that exhibit emergent task-solving abilities; however, their reliance on detailed textual descriptions limits their direct use for planning and decision-making. Existing approaches either outsource this reasoning to language or vision-language models, or rely on supervised fine-tuning with paired task-execution videos, which are costly to collect and difficult to scale. We propose a scalable framework that elicits task-solvin”
- Authors: sebastian-stapf; pablo-acuaviva-huertos; aram-davtyan; et al.

### EA-DQ-CONTRA-READ-0015

- Claim: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation
- Locator: Abstract (full-text section)
- Evidence: 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action chunks。
- Quote: “Abstract Scaling imitation learning requires large datasets, yet human teleoperation inevitably produces mixed-quality demonstrations containing hesitations and recoveries. Prior frame-level progress reward models supervise on absolute temporal progress proxies that suffer from label noise, or require costly human annotations to define subtask boundaries. We present WARP (Warp-Augmented Relative Progress), a novel fully self-supervised algorithm for learning dense, signed relative progress magni”
- Authors: justin-yu; andrew-goldberg; kavish-kondap; et al.

### EA-DQ-CONTRA-READ-0012

- Claim: RynnWorld-Teleop将数字遥操作作为生成式数据引擎，但论文明确限定了它对精细流体动力学、高形变物体和跨机器人平台扩展的能力。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: 6 Conclusion
- Evidence: 结论的限制段指出，模型在精细流体和高形变操作上仍会失败，而当前跨本体迁移仍要求每个平台单独微调。
- Quote: “Limitation. While RynnWorld-Teleop successfully demonstrates digital teleoperation as a viable data engine, several limitations remain. First, while the depth-modulated rendering captures 3D spatial dynamics, the model occasionally struggles with complex physical phenomena such as fine-grained liquid dynamics or the manipulation of highly deformable objects. Addressing these cases will likely require richer training data covering such interactions. Second, bridging the embodiment gap currently r”
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### EA-DQ-CONTRA-READ-0011

- Claim: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.12403](https://arxiv.org/abs/2606.12403) World Pilot: Steering Vision-Language-Action Models with World-Action Priors
- Locator: Abstract (full-text section)
- Evidence: World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy.
- Quote: “Abstract Vision-Language-Action (VLA) models inherit semantic grounding from large-scale pretraining and perform competently across in-distribution manipulation tasks. This grounding, however, is built on static image-text pairs, whereas manipulation is a continuous, contact-rich process whose dynamics this pretraining cannot capture. We present World Pilot, a VLA framework that augments the policy with priors from a World-Action Model (WAM), routed into the decision chain through two complement”
- Authors: zefu-lin; rongxu-cui; junjia-xu; et al.

### EA-DQ-CONTRA-READ-0001

- Claim: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: 5 Conclusion and Limitations
- Evidence: 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。
- Quote: “We presented TACO, a tactile-aware world-model-driven framework for scalable VLA post-training in contact-rich manipulation. Following a Recognize–Imagine–Label loop, TACO converts real-world failures into imagined corrections without repeated human intervention: a tactile-aware world model jointly denoises future video and force sequences, while a unified progress-action model recognizes failure-adjacent states and labels imagined segments with corrective actions. To incorporate this supervisio”
- Authors: shengbang-liu; yueru-jia; yuyang-yan; et al.

### EA-DQ-CONTRA-READ-0002

- Claim: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06442](https://arxiv.org/abs/2607.06442) SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: Introduction
- Evidence: 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。
- Quote: “Our contributions are as follows: • We propose a primitive-compositional view of trajectory utility, realized by Primitive Discovery and Structural Exposure Allocation, which allocate selection budgets according to reuse-aware primitive and transition exposure under diminishing returns. • We introduce Learning-Friendly Trajectory Selection, which selects medoid trajectories within each composition-pattern bucket to favor central, stable, and predictable realizations for behavior cloning. • We pr”
- Authors: changti-wu; bin-yu; zhaolong-shen; et al.

## References

- `2602.10618` [From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks](https://arxiv.org/abs/2602.10618) (2026-02-11)
- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2606.01027` [τ0-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.02577` [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](https://arxiv.org/abs/2606.02577) (2026-06-01)
- `2606.12072` [World Model Self-Distillation: Training World Models to Solve General Tasks](https://arxiv.org/abs/2606.12072) (2026-06-10)
- `2606.12403` [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403) (2026-06-10)
- `2606.28320` [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320) (2026-06-26)
- `2607.02642` [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.05390` [Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models](https://arxiv.org/abs/2607.05390) (2026-07-06)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
- `2607.06558` [RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation](https://arxiv.org/abs/2607.06558) (2026-07-07)
- `2607.06564` [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07)
