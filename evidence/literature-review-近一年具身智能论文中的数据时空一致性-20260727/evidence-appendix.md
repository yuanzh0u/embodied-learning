# Evidence Appendix: 近一年具身智能论文中的数据时空一致性

- Time range: 2025-07-27..2026-07-27
- Events: 20
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-4D-READ-0014

- Claim: MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD observation and fuses the generated views into a more complete 3D structure over time.
- Stance: `support` | Confidence: `direct`
- Paper: [2602.09878](https://arxiv.org/abs/2602.09878) MVISTA-4D: View-Consistent 4D World Model with Test-Time Action Inference for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: The abstract describes single-view RGBD input, arbitrary-view RGBD generation, and back-projection/fusion as the route to complete time-varying 3D structure.
- Quote: “Abstract World-model-based imagine-then-act becomes a promising paradigm for robotic manipulation, yet existing approaches typically support either purely image-based forecasting or reasoning over partial 3D geometry, limiting their ability to predict complete 4D scene dynamics. To solve this, this work explores a novel embodied 4D world model that enables geometrically consistent, arbitrary-view RGBD generation: given only a single-view RGBD observation as input, the model “imagines” the remain”
- Authors: jiaxu-wang; yicheng-jiang; tianlun-he; et al.

### EA-4D-READ-0005

- Claim: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16669](https://arxiv.org/abs/2603.16669) Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation
- Locator: Abstract (full-text section)
- Evidence: The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap futures.
- Quote: “Abstract Simulating robot-world interactions is a cornerstone of Embodied AI. Recently, a few works have shown promise in leveraging video generations to transcend the rigid visual/physical constraints of traditional simulators. However, they primarily operate in 2D space or are guided by static environmental cues, ignoring the fundamental reality that robot-world interactions are inherently 4D spatiotemporal events that require precise interactive modeling. To restore this 4D essence while ensu”
- Authors: mutian-xu; tianbao-zhang; tianqi-liu; et al.

### EA-4D-READ-0015

- Claim: Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.01799](https://arxiv.org/abs/2605.01799) Embody4D: A Generalist Data Engine for Embodied 4D World Modeling
- Locator: Abstract (full-text section)
- Evidence: The abstract ties fixed or sparse viewpoints to partial observations and introduces both novel-view video generation and a compositional synthesis pipeline to address data scarcity.
- Quote: “Abstract Embodied agents require robust and comprehensive 3D spatiotemporal representations to support spatial reasoning, manipulation understanding, and downstream decision making. However, existing robot data are typically captured from fixed or sparse viewpoints, providing only partial and view-dependent observations, which limits multi-view perception and generalization across viewpoints. Given the difficulty of collecting additional viewpoints in real-world settings, we propose Embody4D, a”
- Authors: peiyan-tu; hanxin-zhu; jingwen-sun; et al.

### EA-4D-READ-0013

- Claim: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: 3.1. Problem Formulation
- Evidence: 问题建模段先定义动作与视觉未来的联合分布，再明确把未来触觉纳入联合预测目标。
- Quote: “Building on these two formulations, a world action model combines action prediction and future observation prediction into a unified framework. Specifically, it jointly models (3) or equivalently factorizes the joint distribution as (4) where future visual prediction provides predictive structure for action generation. However, in contact-rich manipulation, vision alone is often insufficient to capture physical interaction cues. To address this limitation, we introduce Dream-Tac, an enhanced wor”
- Authors: yunfan-lou; yifan-ye; yankai-fu; et al.

### EA-4D-READ-0003

- Claim: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13672](https://arxiv.org/abs/2606.13672) $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- Locator: 3 WEAVER : World Estimation Across Views for Embodied Reasoning
- Evidence: The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthetic policy improvement, and test-time planning.
- Quote: “Figure 2 : WEAVER Architecture. Left: The world model encodes memory, history, and action sequences to image future rollouts in latent space. Middle: The latent verifier, equipped with reward and critic heads, selects samples with high advantage to steer the policy distribution. Right: Decoded generation corresponding to different outcomes of action sequences. We now describe the key ingredients in WEAVER : a robot world model designed to support policy evaluation, policy improvement, and test-t”
- Authors: arnav-kumar-jain; yilin-wu; jesse-farebrother; et al.

### EA-TWM-READ-0003

- Claim: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13877](https://arxiv.org/abs/2606.13877) ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation
- Locator: Abstract (full-text section)
- Evidence: ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。
- Quote: “Abstract Contact-rich manipulation requires world models to reason over complex contact dynamics from multimodal sensory observations. However, it remains unclear which representation properties fundamentally support stable long-horizon planning in contact-rich settings. In this paper, we present ContactWorld, a benchmark and systematic empirical study of vision-tactile world models spanning 12 contact-rich manipulation tasks, including insertion, disassembly, screwing, and exploratory interacti”
- Authors: zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al.

### EA-PRETRAIN-DATA-2026-0003

- Claim: 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16253](https://arxiv.org/abs/2606.16253) SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models
- Locator: 1 Introduction and 3 Method
- Evidence: 论文指出不同机位和图像区域对控制的价值不均匀，SPARC 通过时序 mask 自适应分配比特。
- Quote: “Uniform bitrate allocation across cameras and image regions is therefore fundamentally inefficient.”
- Authors: sangyun-chung; mincheol-shin; jihyun-kim; et al.

### EA-PRETRAIN-DATA-2026-0006

- Claim: 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.11612](https://arxiv.org/abs/2512.11612) Embodied Image Compression: Towards Codec for Robotic Visual Systems
- Locator: Appendix C Subjective Data Collection
- Evidence: 真实管线同步记录腕部与第三人称 RealSense、关节角和末端增量动作，频率为 10 Hz。
- Quote: “Joint angles, two camera streams (wrist view and third-person view, captured by two Intel realsense cameras), and actions”
- Authors: zhenghao-chen; zijie-yue; haozhe-li; et al.

### EA-TWM-READ-0001

- Claim: VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.06001](https://arxiv.org/abs/2602.06001) Visuo-Tactile World Models
- Locator: B.0.1 Training dataset
- Evidence: 训练数据段明确列出了同步的本体状态、外部视频与双指触觉视频数据流。
- Quote: “Each sequence contains multimodal data streams: proprioceptive information (wrist pose, joint positions), exocentric video from the camera, and video from each Digit 360 fingertip sensor. All data streams were synchronized using timestamps and downsampled to 6 FPS for training the world model. Our training dataset for V-WM and VT-WM consists of 124 demonstrations totaling 112k datapoints, with each demonstration averaging 40 seconds. For validation, we use 26 demonstrations spanning all tasks, c”
- Authors: carolina-higuera; sergio-arnaud; byron-boots; et al.

### EA-4D-READ-0012

- Claim: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction
- Evidence: 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。
- Quote: “The primary advantage of 3PoinTr is that it trains on data General Flow ignores. Real-world points are often temporarily occluded; General Flow removes any trajectory with invisible point-timestep pairs during preprocessing, whereas 3PoinTr retains all trajectories and masks losses for individual invisible point-timestep pairs. This provides additional supervision over task-critical object points that are temporarily occluded during manipulation. For example, in the Throw Away Paper task, every”
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### EA-TWM-READ-0007

- Claim: 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.07308](https://arxiv.org/abs/2605.07308) AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models
- Locator: 5 Conclusion
- Evidence: AT-VLA 把系统分为慢速视觉语言流和快速触觉流，慢速流负责任务理解和视觉定位，快速流以高频处理触觉反馈；作者采用 3:1 的快慢流频率比，并在真实接触丰富任务中验证 adaptive tactile injection、tactile gate、adaptive cross-attention 和 reaction dual-stream 的作用。
- Quote: “In summary, AT-VLA introduces an adaptive framework that seamlessly integrates tactile sensing into vision-language-action models. Through the Adaptive Tactile Injection mechanism, AT-VLA dynamically balances pretrained visual-language knowledge with newly learned tactile representations, preserving model integrity while enhancing action precision. The Tactile Reaction Dual-Stream mechanism further enables rapid, high-frequency tactile responses by decoupling slow perceptual reasoning from fast”
- Authors: xiaoqi-li; muhe-cai; jiadong-xu; et al.

### EA-4D-READ-0010

- Claim: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control
- Evidence: 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。
- Quote: “All data modalities are synchronized through the robot control loop. For policy learning, actions are converted to a unified 7D end-effector delta representation (1) where are translational deltas, are rotational deltas, and is the gripper command. This decouples learning from the exact robot configuration, enabling cross-embodiment by focusing the policy on local contact adjustment from tactile feedback. Several quality checks are applied to every collected trajectory. Empty or corrupted trajec”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### EA-TWM-READ-0014

- Claim: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08765](https://arxiv.org/abs/2606.08765) RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。
- Quote: “We then render force-modulated Gaussian saliency maps to model spatial uncertainty arising from kinematic and calibration errors.”
- Authors: shengcheng-luo

### EA-PRETRAIN-DATA-2026-0001

- Claim: 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.17200](https://arxiv.org/abs/2606.17200) ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining
- Locator: 5.2 Ablation Studies, Figure 5(b)
- Evidence: 三项组件消融均降低 RoboCasa 成功率，其中去掉人类伪动作可靠性加权的降幅最大。
- Quote: “Removing morphology tokens makes the success rate drop from 72.8% to 70.9%”
- Authors: hao-li; ganlong-zhao; yufei-liu; et al.

### EA-EGO-2026-0016

- Claim: Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 3 Method
- Evidence: 方法段明确说明 current-frame wrist pose 与 first-frame camera path 的坐标差异会混合两类位移。
- Quote: “using these wrist poses directly as action supervision would therefore conflate wrist movement with camera motion”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-VLABREAK-2026-0001

- Claim: H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: IV-C Hierarchical World Model Guidance for VLA
- Evidence: 方法定义了逻辑世界模型、视觉世界模型、低层 VLA 和子任务完成检测的两时间尺度接口。
- Quote: “The hierarchical information at multiple abstraction level enables the VLA to maintain consistency with long-horizon task structure while remaining responsive to local visual feedback.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-ALIGN-READ-0004

- Claim: Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30456](https://arxiv.org/abs/2606.30456) Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform
- Locator: Abstract (full-text section)
- Evidence: The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone.
- Quote: “Instead, it is strongly influenced by a combination of factors, including action semantics, coordinate frame conventions, temporal alignment between modalities, image preprocessing consistency, and dataset coverage and quality. These observations lead to a key interpretation: the successful deployment of VLA systems in real-world settings depends less on incremental improvements in model capacity and more on precise control of the entire data–model–control pipeline.”
- Authors: mathilde-hochedel; marc-lalonde

### EA-VLABREAK-2026-0007

- Claim: 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.15207](https://arxiv.org/abs/2607.15207) BadWAM: When World-Action Models Dream Right but Act Wrong
- Locator: 5.8 What Do These Results Imply for WAM Safety?
- Evidence: 想象保持攻击在 40 个任务中有 39 个降低未来漂移，同时保留显著攻击强度。
- Quote: “The relevant security property is not plausibility of the imagined future in isolation, but synchronization between the imagined future and the action that will actually be executed.”
- Authors: qi-li; xingyi-yang; xinchao-wang

### EA-TACTILE-2026-0001

- Claim: 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19161](https://arxiv.org/abs/2606.19161) HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision
- Locator: Abstract; 3 HT-Bench: A Multi-Task Tactile Evaluation Benchmark
- Evidence: 摘要和基准设计章节直接给出数据规模、四项评测任务与任务级 OOD 划分。
- Quote: “comprising 10M RGB frames and 7.8M tactile frames collected across 226 tasks.”
- Authors: yuzhe-huang; jiaping-wu; jiaming-jiang; et al.

### EA-SENSORERR-READ-0011

- Claim: RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29384](https://arxiv.org/abs/2606.29384) Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model
- Locator: Abstract (full-text section)
- Evidence: 作者指出现有 VLA 往往假设稳定明亮的室内环境，而真实操作中 illumination shifts 会造成 degraded RGB observations；Event-VLA 将 degraded visibility 定义为 RGB-centric policies 的鲁棒性问题，并通过 action-query routing 将 event streams 融入 action representation，仿真和真实部署实验显示在不同可见性下保持更强鲁棒性。
- Quote: “Abstract Vision-Language-Action (VLA) models have become an important paradigm of embodied AI. However, existing VLA models typically assume well-lit and stable indoor settings, while real-world embodied manipulation may involve degraded RGB observations caused by illumination shifts, posing critical challenges for robust robotic manipulation. To address this gap, we propose Event-VLA , an event-enhanced VLA framework for generalizable manipulation across varying illumination conditions. We form”
- Authors: jiaxin-liu; xun-xu; zhenhao-zhang; et al.

## References

- `2512.11612` [Embodied Image Compression: Towards Codec for Robotic Visual Systems](https://arxiv.org/abs/2512.11612) (2025-12-12T18:59:07Z)
- `2602.06001` [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) (2026-02-05)
- `2602.09878` [MVISTA-4D: View-Consistent 4D World Model with Test-Time Action Inference for Robotic Manipulation](https://arxiv.org/abs/2602.09878) (2026-02-10)
- `2602.11291` [H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model](https://arxiv.org/abs/2602.11291) (2026-02-11T19:08:36Z)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2605.01799` [Embody4D: A Generalist Data Engine for Embodied 4D World Modeling](https://arxiv.org/abs/2605.01799) (2026-05-03)
- `2605.07308` [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](https://arxiv.org/abs/2605.07308) (2026-05-08)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.06194` [ActiveMimic: Egocentric Video Pretraining with Active Perception](https://arxiv.org/abs/2606.06194) (2026-06-04T14:01:01Z)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.08765` [RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation](https://arxiv.org/abs/2606.08765) (2026-06-07)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
- `2606.13877` [ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13877) (2026-06-11)
- `2606.16253` [SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models](https://arxiv.org/abs/2606.16253) (2026-06-15T03:38:29Z)
- `2606.17200` [ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining](https://arxiv.org/abs/2606.17200) (2026-06-15T18:40:18Z)
- `2606.19161` [HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision](https://arxiv.org/abs/2606.19161) (2026-06-17)
- `2606.29384` [Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model](https://arxiv.org/abs/2606.29384) (2026-06-28)
- `2606.30456` [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456) (2026-06-29)
- `2607.15207` [BadWAM: When World-Action Models Dream Right but Act Wrong](https://arxiv.org/abs/2607.15207) (2026-07-16T17:04:15Z)
