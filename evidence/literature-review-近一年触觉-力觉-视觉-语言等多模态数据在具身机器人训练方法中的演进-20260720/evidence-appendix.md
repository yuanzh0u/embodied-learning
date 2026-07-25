# Evidence Appendix: 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进

- Time range: 2025-07-20..2026-07-20
- Events: 56
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-EGO-2026-0007

- Claim: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.3 Policy Performance Scales with Pretraining Data Size
- Evidence: 五个数据规模的同架构实验报告单调提升，并限制结论不外推到测量区间之外。
- Quote: “Average task completion rises monotonically from 0.30 at 1k hours to 0.71 at 20k hours”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-TWM-READ-0008

- Claim: TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07335](https://arxiv.org/abs/2604.07335) TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks
- Locator: Abstract (full-text section)
- Evidence: 摘要明确列出精度/便携双模式采集、触觉恢复遥操作和人在环恢复数据。
- Quote: “To balance data quality and environmental diversity, we implement a dual-mode acquisition pipeline: a precision mode leveraging motion capture for high-fidelity demonstrations, and a portable mode utilizing VR-based tracking for in-the-wild acquisition and tactile-visualized recovery teleoperation. Building on this hardware, we unify large-scale tactile pretraining, task-specific bimanual demonstrations, and human-in-the-loop recovery data into a pyramid-structured data regime, enabling closed-l”
- Authors: longyan-wu; jieji-ren; chenghang-jiang; et al.

### EA-TWM-READ-0005

- Claim: 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 4.2 Vision-Based Tactile Sensing and Marker Tracking
- Evidence: HapTile 的每个夹爪手指安装视觉触觉传感器，接触会带来图像变化和 marker displacement；论文把 marker-motion 信号保存进数据集并用于 haptic feedback，实验也比较 vision-only、vision+tactile image 与 vision+tactile+marker 表征。
- Quote: “We smooth the signal with separate rise and release factors, producing a stable tactile motion estimate. The resulting marker-motion signal is stored in HapTile and is also used to drive haptic feedback.”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### EA-TWM-READ-0002

- Claim: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: Dream-Tac 把 world action model 扩展到触觉，联合建模当前视觉、触觉、语言指令下的未来视觉观测、未来触觉观测和动作 chunk，并加入 contact-gated visuotactile fusion 与 contact-aware attention bias。
- Quote: “In this paper, we propose Dream-Tac, a unified Tactile-World Action Model that jointly models actions, future visual observations, and tactile dynamics. Specifically, Dream-Tac introduces (i) contact-gated visuotactile fusion to selectively integrate tactile signals and (ii) a contact-aware attention bias to better regulate cross-modal interactions during manipulation.”
- Authors: yunfan-lou; yifan-ye; yankai-fu; et al.

### EA-TWM-READ-0006

- Claim: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-D 1 World Model Conditioning
- Evidence: TacForeSight 的 TacForceWM 从双指触觉观测出发，以高频腕部 force/torque 为条件预测短时域触觉 latent dynamics；ablation 中 wrist wrench 条件的未来触觉预测优于无条件版本，MSE 从 0.027 降到 0.017，cosine 从 0.954 提升到 0.992。
- Quote: “We first ablate the conditioning modality used in the tactile world model. We compare four conditioning designs: no external condition, RGB image condition, robot state condition, and wrist wrench condition. Prediction quality is evaluated using Mean Squared Error (MSE), cosine similarity (Cos), and symmetric KL divergence (KL sym ), which respectively measure element-wise prediction error, latent directional consistency, and latent distribution consistency. As shown in Table II , wrist wrench c”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### EA-TWM-READ-0003

- Claim: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13877](https://arxiv.org/abs/2606.13877) ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation
- Locator: Abstract (full-text section)
- Evidence: ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。
- Quote: “Abstract Contact-rich manipulation requires world models to reason over complex contact dynamics from multimodal sensory observations. However, it remains unclear which representation properties fundamentally support stable long-horizon planning in contact-rich settings. In this paper, we present ContactWorld, a benchmark and systematic empirical study of vision-tactile world models spanning 12 contact-rich manipulation tasks, including insertion, disassembly, screwing, and exploratory interacti”
- Authors: zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al.

### EA-TWM-READ-0004

- Claim: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.14981](https://arxiv.org/abs/2606.14981) Inference-time Policy Steering via Vision and Touch
- Locator: 5 Experiments
- Evidence: ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。
- Quote: “We evaluate ViTaL on three real-world contact-rich manipulation tasks. Our experiments are designed to answer three questions: whether multimodal visuo-tactile steering improves policy over unimodal guidance (Sec. 5.1 ); whether a learned latent world model and semantically aligned verifier provides reliable rewards for predicted outcomes (Sec. 5.2 ); and whether the proposed bi-level optimization balances performance and efficiency compared to naive visual-tactile fusion (Sec. 5.3 ). Robot Setu”
- Authors: yilin-wu; zilin-si; zeynep-temel; et al.

### EA-TWM-READ-0015

- Claim: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.18043](https://arxiv.org/abs/2606.18043) Uncertainty Quantification for Flow-Based Vision-Language-Action Models
- Locator: Abstract (full-text section)
- Evidence: 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。
- Quote: “This presents a critical limitation for real-world deployment in non-stationary environments, where models inevitably encounter scenarios outside their pretraining distribution and may fail without warning. To address this, we derive an efficient method for quantifying epistemic uncertainty in flow-matching models by leveraging velocity-field disagreement (VFD) across a small ensemble.”
- Authors: ralf-rmer

### EA-TWM-READ-0001

- Claim: VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.06001](https://arxiv.org/abs/2602.06001) Visuo-Tactile World Models
- Locator: B.0.1 Training dataset
- Evidence: 训练数据段明确列出了同步的本体状态、外部视频与双指触觉视频数据流。
- Quote: “Each sequence contains multimodal data streams: proprioceptive information (wrist pose, joint positions), exocentric video from the camera, and video from each Digit 360 fingertip sensor. All data streams were synchronized using timestamps and downsampled to 6 FPS for training the world model. Our training dataset for V-WM and VT-WM consists of 124 demonstrations totaling 112k datapoints, with each demonstration averaging 40 seconds. For validation, we use 26 demonstrations spanning all tasks, c”
- Authors: carolina-higuera; sergio-arnaud; byron-boots; et al.

### EA-EGO-2026-0008

- Claim: 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.2 Large-Scale Human Pretraining Is Key to Strong Dexterous Manipulation Policy Performance
- Evidence: 四类 checkpoint 的消融中，pretrain+midtrain 最好；human pretraining 提供结构，mid-training 负责控制锚定。
- Quote: “combining human pretraining with a small amount of aligned mid-training yields the best overall performance”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-TWM-READ-0007

- Claim: 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.07308](https://arxiv.org/abs/2605.07308) AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models
- Locator: 5 Conclusion
- Evidence: AT-VLA 把系统分为慢速视觉语言流和快速触觉流，慢速流负责任务理解和视觉定位，快速流以高频处理触觉反馈；作者采用 3:1 的快慢流频率比，并在真实接触丰富任务中验证 adaptive tactile injection、tactile gate、adaptive cross-attention 和 reaction dual-stream 的作用。
- Quote: “In summary, AT-VLA introduces an adaptive framework that seamlessly integrates tactile sensing into vision-language-action models. Through the Adaptive Tactile Injection mechanism, AT-VLA dynamically balances pretrained visual-language knowledge with newly learned tactile representations, preserving model integrity while enhancing action precision. The Tactile Reaction Dual-Stream mechanism further enables rapid, high-frequency tactile responses by decoupling slow perceptual reasoning from fast”
- Authors: xiaoqi-li; muhe-cai; jiadong-xu; et al.

### EA-EGO-2026-0017

- Claim: 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 4.3 Egocentric Video Yields Effective Pretraining Labels
- Evidence: HOT3D ground truth 上的 10% sample 验证给出 head/wrist 三类严格阈值 recovery rate。
- Quote: “Under the strict tier ( , rot6d L2 ), head recovery reaches 78.82%, with left and right wrist recovery at 65.93% and 61.72%, respectively;”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-EGO-2026-0018

- Claim: 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 4.4 The Head Camera Enables Pretrained Active Perception
- Evidence: Restocking 中 egocentric-pretrained model 的 placement 为 24/27，SFT-only 为 6/27；移除 head camera 降到 1/27。
- Quote: “ActiveMimic scores 24 out of 27 on placement, whereas ActiveMimic sft-only achieves only 6 out of 27”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-TWM-READ-0014

- Claim: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08765](https://arxiv.org/abs/2606.08765) RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。
- Quote: “We then render force-modulated Gaussian saliency maps to model spatial uncertainty arising from kinematic and calibration errors.”
- Authors: shengcheng-luo

### EA-TWM-READ-0010

- Claim: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26663](https://arxiv.org/abs/2606.26663) Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention
- Locator: Abstract (full-text section)
- Evidence: 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。
- Quote: “In contact-rich manipulation, however, visually plausible futures can be physically incomplete: insertion, assembly, search, and reorientation often depend on slip, jamming, contact normals, or small alignment errors that are weakly visible or hidden in RGB. A natural solution is to predict future tactile states, however, we identify tactile pollution , a failure mode where unconstrained tactile-token injection degrades video and action prediction by forcing a visual dynamics model to absorb spa”
- Authors: siyu-wu; linjing-you; junjie-zhu; et al.

### EA-TWM-READ-0011

- Claim: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30988](https://arxiv.org/abs/2606.30988) Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force
- Locator: Abstract (full-text section)
- Evidence: 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only policies，并以 force-torque sensing 做真实任务案例。
- Quote: “Abstract Robot manipulation often depends on sensory data beyond vision, especially in contact-rich tasks where force, tactile, or audio feedback reveals interaction states not directly visible from images. Yet such modalities are hardware- and task-specific, and large multisensory datasets remain scarce, making it impractical to pretrain policies with every sensor they may encounter. We study multi-sensory continual learning : adapting a pretrained robot policy to new tasks with newly introduce”
- Authors: jaden-clark; changhao-wang; yihuai-gao; et al.

### EA-EGO-2026-0020

- Claim: 显式 contact geometry 在该系统中显著减少滑移并提高成功率，说明接触结构是 Ego-centric 数据转成可执行监督的独立质量维度。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.03828](https://arxiv.org/abs/2607.03828) ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Modeling
- Locator: IV-C 1 Hand–object geometric consistency module
- Evidence: 去除 hand geometry 后 object slip 变大且 success 下降，full ObjRetarget 最好。
- Quote: “also removing geometric consistency causes significant slippage, contact failures, and posture collapse”
- Authors: yuanchuan-lai; qing-gao; ziyan-liang; et al.

### EA-EGO-2026-0003

- Claim: 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: III-C Policy Training
- Evidence: 策略训练段明确说明 gripper state 缺失，并以 object pose displacement 作为替代动作。
- Quote: “Because gripper states cannot be obtained from Section III-B , each action is represented by a 9-dimensional vector”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGO-2026-0004

- Claim: Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: IV-C Ablation Study
- Evidence: BGTS=1.0 保留 86,427 episodes 但真实机器人分数低于 BGTS=0.7 的 45,157 episodes。
- Quote: “Setting an appropriate curation threshold is crucial to balancing the scale and quality of our dataset”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGO-2026-0009

- Claim: Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.6 Hand Action Space Design for Human Pretraining
- Evidence: 动作空间消融中 wrist-only 普遍较差，fingertip mapping 在 Cards/Bottle 等接触敏感任务不稳定。
- Quote: “Small errors in fingertip pose often lead to implausible joint configurations after mapping”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-EGO-2026-0016

- Claim: Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 3 Method
- Evidence: 方法段明确说明 current-frame wrist pose 与 first-frame camera path 的坐标差异会混合两类位移。
- Quote: “using these wrist poses directly as action supervision would therefore conflate wrist movement with camera motion”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-TWM-READ-0009

- Claim: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.16690](https://arxiv.org/abs/2606.16690) PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差作为介入信号。
- Quote: “Abstract Learning-based manipulation policies have made substantial progress in real-world robot manipulation, particularly for short-horizon action generation. However, deployment in open workspaces remains fragile under unexpected local scene dynamics, such as moving objects, transient occlusions, or disturbances near the intended motion. Existing runtime monitors often rely on global observation anomalies, policy uncertainty, or frame-level visual changes, and struggle to distinguish task-rel”
- Authors: yanan-zhou; ranpeng-qiu; yincong-chen; et al.

### EA-EGO-2026-0019

- Claim: Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.03828](https://arxiv.org/abs/2607.03828) ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Modeling
- Locator: II-B Human-to-Robot Motion Retargeting
- Evidence: 相关工作和引言都指出现有方法多假设 object-free/weak-contact，忽略手臂与手的不同功能。
- Quote: “most methods assume object-free or weak-contact settings and focus on geometric consistency or joint error minimization”
- Authors: yuanchuan-lai; qing-gao; ziyan-liang; et al.

### EA-TWM-READ-0012

- Claim: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.04234](https://arxiv.org/abs/2607.04234) SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects
- Locator: 1 Introduction
- Evidence: 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。
- Quote: “Experiments show that success-only evaluation substantially overstates policy performance, as a large fraction of goal-completing rollouts violate physical safety, and that adding tactile sensing improves Safety Success while keeping Goal Success comparable and reduces object deformation during execution.”
- Authors: bowen-jing; mingxin-wang; ruiyang-hao; et al.

### EA-TWM-READ-0013

- Claim: 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。
- Stance: `gap` | Confidence: `direct`
- Paper: [2607.07196](https://arxiv.org/abs/2607.07196) Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators
- Locator: Abstract (full-text section)
- Evidence: 作者指出机器人中 World Models 越来越被用于模拟动作后果并给出 success/safety verdict，但视频生成指标如 FVD 奖励视觉真实感，却忽略世界是否对 policy actions 正确响应；他们主张作为 test oracle 的 WM 需要先通过 accreditation，并提出 L0-L4 admissibility ladder。
- Quote: “Abstract Across robotics, World Models (WMs) are increasingly used to evaluate action policies by simulating the consequences of actions in an imagined world, and returning a success or safety verdict. Yet a verdict is only as trustworthy as the WM that produced it, and the WM itself needs to be certified. In video-generation WMs , fidelity metrics such as Fréchet Video Distance (FVD) reward visual realism, but ignore whether the world responds correctly to the policy’s actions, including those”
- Authors: christian-oefinger

### EA-LOCOMANIP-2026-0006

- Claim: Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the evaluated tasks.
- Stance: `support` | Confidence: `direct`
- Paper: [2512.11047](https://arxiv.org/abs/2512.11047) WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control
- Locator: 4.3 How does action-free videos contribute to loco–manipulation?
- Evidence: The ablation directly compares the full model with removal of unified latent learning.
- Quote: “As shown in Table 4.2 , the full model improves success rate by 38.7%, indicating that unified latent learning extracts useful priors from action-free human videos and enhances downstream policy learning.”
- Authors: haoran-jiang; jin-chen; qingwen-bu; et al.

### EA-ALIGN-READ-0013

- Claim: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.09708](https://arxiv.org/abs/2601.09708) Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning
- Locator: 5 Conclusion
- Evidence: 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。
- Quote: “By distilling lengthy textual reasoning into compact latent representations via preference-guided distillation and visual trajectory alignment, our approach bridges high-level embodied reasoning with low-level action execution through reasoning-enhanced policy learning. Extensive experiments across diverse robotic manipulation and embodied reasoning benchmarks demonstrate that Fast-ThinkAct achieves strong performance with significantly reduced inference latency while enabling effective long-hor”
- Authors: chi-pin-huang; yunze-man; zhiding-yu; et al.

### EA-VLABREAK-2026-0001

- Claim: H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: IV-C Hierarchical World Model Guidance for VLA
- Evidence: 方法定义了逻辑世界模型、视觉世界模型、低层 VLA 和子任务完成检测的两时间尺度接口。
- Quote: “The hierarchical information at multiple abstraction level enables the VLA to maintain consistency with long-horizon task structure while remaining responsive to local visual feedback.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-VLABREAK-2026-0004

- Claim: StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.12553](https://arxiv.org/abs/2603.12553) Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation
- Locator: pages 5-8, Sections 3.1-3.3
- Evidence: 方法段给出动力学里程碑抽取和 planner-to-action 两阶段优化的完整链路。
- Quote: “Structured frames provide compact progress anchors that connect task intent to executable motion phases.”
- Authors: minghao-jin; mozheng-liao; mingfei-han; et al.

### EA-LOCOMANIP-2026-0012

- Claim: Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to 0.85.
- Stance: `support` | Confidence: `direct`
- Paper: [2604.27224](https://arxiv.org/abs/2604.27224) Learning Tactile-Aware Quadrupedal Loco-Manipulation Policies
- Locator: IV-B Experimental Results and Analyze
- Evidence: The paper compares variants with the same tactile-aware high level but different low-level tactile tracking.
- Quote: “Finally, comparing Baseline 3 (P3) with our full method demonstrates the benefit of incorporating tactile commands into the low-level policy: our method further increases the success rate from 0.70 to 0.85 on Task 1 insertion (+0.15), from 0.60 to 0.80 on Task 1 whole (+0.20), and from 0.80 to 0.85 on Task 2 (+0.05), and achieves 1.00 on Task 3 (compared to 0.20 for P1).”
- Authors: pokuang-zhou; yuhao-zhou; quan-khanh-luu; et al.

### EA-ALIGN-READ-0014

- Claim: 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.00080](https://arxiv.org/abs/2605.00080) World Model for Robot Learning: A Comprehensive Survey
- Locator: 1 Introduction
- Evidence: 引言直接将纯反应 VLA 的三类困难列为长时程推理、temporal credit assignment 与 compounding errors。
- Quote: “Yet despite strong scaling trends ( Xiao et al. , 2025 ; Li et al. , 2025b ; Zhu et al. , 2026 ) , purely reactive VLA policies remain limited in complex physical environments, where they often struggle with long-horizon reasoning, temporal credit assignment, and robustness under compounding errors. A growing body of work argues that these limitations stem not only from insufficient action prediction capacity ( Ye et al. , 2026b ; Dang et al. , 2026 ) , but also from the lack of explicit predict”
- Authors: bohan-hou; gen-li; jindou-jia; et al.

### EA-ALIGN-READ-0012

- Claim: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: Abstract (full-text section)
- Evidence: 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。
- Quote: “Abstract Industrial automation is at a pivotal moment, as Physical AI is driving a transition from rigid, hand-engineered automation systems toward more flexible and adaptive systems. This shift has created a growing demand for large-scale, real-world robot demonstration data, making teleoperation an increasingly important mechanism for data collection. However, high-quality teleoperated demonstrations remain difficult to obtain in practice, as novice operators often produce episodes that are ta”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

### EA-ALIGN-READ-0015

- Claim: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09630](https://arxiv.org/abs/2606.09630) ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies
- Locator: 1 Introduction
- Evidence: ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classification mistakes 与 perception errors、sim-to-real mismatch 并列为失败来源。
- Quote: “Instead, it produces a structured recovery descriptor containing the failure type, recovery stage, active entities, confidence, and reward mask.”
- Authors: haodi-hu; chung-ta-huang; jing-liu; et al.

### EA-ALIGN-READ-0005

- Claim: Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.30552](https://arxiv.org/abs/2606.30552) Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision
- Locator: Abstract (full-text section)
- Evidence: The paper frames low-level state/action heterogeneity as a core cross-embodiment challenge, then uses dense embodied chain-of-thought supervision in the VLM stream and a flow-matching action expert that outputs continuous action chunks.
- Quote: “Abstract Cross-embodiment transfer in vision-language-action (VLA) models remains challenging because low-level state and action spaces differ fundamentally across robot platforms. We observe that the high-level cognitive process underlying manipulation, including scene perception, object identification, task planning, and sub-task decomposition, is largely shared across embodiments. Based on this observation, we present ZR-0 , a 2.6 billion parameter end-to-end VLA model that uses dense Embodie”
- Authors: haoyang-li; guanlin-li; youhe-feng; et al.

### EA-LOCOMANIP-2026-0021

- Claim: In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper.
- Stance: `support` | Confidence: `direct`
- Paper: [2607.10132](https://arxiv.org/abs/2607.10132) TAC-LOCO: Unified Whole-Body Control for Quadrupedal TACtile-Informed LOCO-Manipulation
- Locator: 6.5 Baseline comparison
- Evidence: The hardware baseline comparison isolates learned grasp regulation under the same command set.
- Quote: “We conduct 10 hardware trials using the same set of loco-manipulation commands as in Sec. 6 . Table 4 compares the success rates of our policy and the baseline, showing that our tactile-informed policy achieves a substantially higher success rate. Figure 11 shows that the baseline suffers from gradual object slip during the task. Since the gripper width remains fixed, the policy cannot actively suppress slip once the external force changes. Table 4: Deployment success rate comparison with baseli”
- Authors: muqun-hu; yuhao-zhou; kabir-ray-malik; et al.

### EA-VLABREAK-2026-0002

- Claim: 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: VI Results
- Evidence: H-WM 为 64.8%，logic-only 为 48.4%，H-WM-Stable-Diffusion 为 54.4%。
- Quote: “Incorporating visual guidance yields consistent additional gains, providing more than 10% further improvement in Q-score and 17% in success rate.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-ALIGN-READ-0010

- Claim: ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.21161](https://arxiv.org/abs/2602.21161) ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking
- Locator: II-B LLM/VLM Based Robotic Operation
- Evidence: 相关工作段明确提出解耦视觉部件，让 LLM 在已知感知状态上做 3D 物理与动作推理。
- Quote: “To address this, we argue for decoupling the visual component: assuming the robot already has sufficiently accurate perceptual information via computer vision algorithms, and the LLMs are asked to focus only on action reasoning. This approach significantly reduces data requirements while also leveraging the wealth of existing research in computer vision. For example, the ReKep series [ 11 , 16 ] use vision-language models to identify keypoints for robotic manipulation, which significantly reduce”
- Authors: guangming-wang; qizhen-ying; yixiong-jing; et al.

### EA-LOCOMANIP-2026-0018

- Claim: On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.03279](https://arxiv.org/abs/2603.03279) ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation
- Locator: V-E Real-World Deployment
- Evidence: The real-world table separates external-state and onboard egocentric control modes.
- Quote: “TABLE IV : Real-world success rates on the OMOMO subset using a Unitree G1 humanoid. Each task is evaluated over two trials. MoCap provides object pose tracking for non-egocentric control modes, while the egocentric setting relies only on onboard sensing. MoCap is used for success evaluation in all settings. Dense reference tracking is direction-agnostic and thus reported as a single success rate. Setting Vertical Lateral Dense Reference Tracking 73% (19/26) Sparse Goal Following (MoCap) 80% (8/”
- Authors: xialin-he; sirui-xu; xinyao-li; et al.

### EA-VLABREAK-2026-0005

- Claim: 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.12553](https://arxiv.org/abs/2603.12553) Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation
- Locator: page 11
- Evidence: LIBERO 平均为 94.8%；实机 tidy-up 为 8/10，相同表面的 UniVLA 为 4/10。
- Quote: “StructVLA completes8/10trials,comparedwith4/10forUniVLAand2/10forSpatialVLA, indicating stronger stability over extended execution.”
- Authors: minghao-jin; mozheng-liao; mingfei-han; et al.

### EA-ALIGN-READ-0011

- Claim: τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接列出四类交互数据和 modality-specific supervision masks。
- Quote: “Abstract Robotic manipulation requires models that generate executable actions while anticipating and evaluating their future consequences before physical execution. We present -World Model ( -WM), a unified video-action world model that integrates policy learning, video prediction, and action evaluation within a single future-predictive framework. Built on a shared video diffusion backbone, -WM provides two complementary interfaces. First, a video action model jointly predicts future visual lat”
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### EA-ALIGN-READ-0006

- Claim: ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.03784](https://arxiv.org/abs/2606.03784) Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。
- Quote: “Abstract Embodied chain-of-thought (CoT) aims to bridge linguistic reasoning with robotic control, yet its effective form and integration remain underexplored. In this paper, we revisit embodied CoT for robotic control at an unprecedented scale. We curate the largest embodied CoT corpus to date, comprising 978,743 trajectories, 226.3M samples, and 2592.5 hours of data. Through extensive experiments, we show that effective CoT must ground high-level semantic understaning in concrete linguistic ac”
- Authors: nan-sun; yuan-zhang; yongkun-yang; et al.

### EA-ALIGN-READ-0007

- Claim: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control
- Evidence: 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。
- Quote: “All data modalities are synchronized through the robot control loop. For policy learning, actions are converted to a unified 7D end-effector delta representation (1) where are translational deltas, are rotational deltas, and is the gripper command. This decouples learning from the exact robot configuration, enabling cross-embodiment by focusing the policy on local contact adjustment from tactile feedback. Several quality checks are applied to every collected trajectory. Empty or corrupted trajec”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### EA-ALIGN-READ-0008

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Quote: “Policies in this setting are trained using both nominal demonstrations and recovery interaction data.”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### EA-ALIGN-READ-0002

- Claim: A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26800](https://arxiv.org/abs/2606.26800) SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: SSI-Policy builds an RGB-only structured scene interface encoding monocular depth features, language-grounded layouts, and instruction-conditioned 2D motion trajectories; it reports few-shot gains but notes failures from perception noise and contact limitations.
- Quote: “Abstract Real-world robotic manipulation demands spatial grounding, task-aware reasoning, and precise control. Learning such capabilities becomes particularly challenging in the low-data regime. Prior methods often trade off scalable task-level reasoning and explicit physical structure: video-based approaches can drift geometrically over long horizons, 3D approaches often require depth sensing, and many flow/trajectory interfaces emphasize motion without an explicit RGB-only geometric representa”
- Authors: kaijun-wang; zikai-ouyang; xuping-wu; et al.

### EA-VLABREAK-2026-0003

- Claim: H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: VII Conclusion
- Evidence: 结论明确列出额外组件/训练阶段的代价，以及对符号化状态的依赖。
- Quote: “The logical world model depends on structured logical state representations, which assume that the task can be meaningfully formulated in a symbolic logical space.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

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

### EA-SENSORERR-READ-0010

- Claim: 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.28899](https://arxiv.org/abs/2606.28899) You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact
- Locator: Abstract (full-text section)
- Evidence: 作者明确指出视觉位姿估计常在遮挡、差光照、反光或透明表面下失败，并提出 tactile-only pose estimation：把触觉接触表示成局部 3D 点云，结合校准传感器位姿恢复完整 6-DoF object pose；实验在视觉不可靠时优于视觉和几何基线。
- Quote: “Abstract Accurate 6-DoF object pose estimation is fundamental to robotic manipulation, yet vision-based methods often fail under occlusion, poor lighting, and reflective or transparent surfaces.”
- Authors: pengfei-ye; yuxiang-ma; haonan-chen; et al.

### EA-SENSORERR-READ-0011

- Claim: RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29384](https://arxiv.org/abs/2606.29384) Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model
- Locator: Abstract (full-text section)
- Evidence: 作者指出现有 VLA 往往假设稳定明亮的室内环境，而真实操作中 illumination shifts 会造成 degraded RGB observations；Event-VLA 将 degraded visibility 定义为 RGB-centric policies 的鲁棒性问题，并通过 action-query routing 将 event streams 融入 action representation，仿真和真实部署实验显示在不同可见性下保持更强鲁棒性。
- Quote: “Abstract Vision-Language-Action (VLA) models have become an important paradigm of embodied AI. However, existing VLA models typically assume well-lit and stable indoor settings, while real-world embodied manipulation may involve degraded RGB observations caused by illumination shifts, posing critical challenges for robust robotic manipulation. To address this gap, we propose Event-VLA , an event-enhanced VLA framework for generalizable manipulation across varying illumination conditions. We form”
- Authors: jiaxin-liu; xun-xu; zhenhao-zhang; et al.

### EA-SENSORERR-READ-0012

- Claim: 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.07287](https://arxiv.org/abs/2607.07287) TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者把日常灵巧操作的误差来源明确落在滑移、错位、不稳定抓取和力不匹配上，并指出视觉/语言不能可靠揭示力、滑移和接触稳定性；其分层策略将视觉语言子任务规划、触觉世界模型预测和高频触觉残差修正分开。
- Quote: “Vision and language provide semantic and geometric guidance, but they cannot reliably reveal hidden contact states such as force, slip, and contact stability.”
- Authors: jianyi-zhou; feiyang-hong; yunhao-li; et al.

### EA-SENSORERR-READ-0007

- Claim: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08765](https://arxiv.org/abs/2606.08765) RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。
- Quote: “We then render force-modulated Gaussian saliency maps to model spatial uncertainty arising from kinematic and calibration errors.”
- Authors: shengcheng-luo

### EA-SENSORERR-READ-0004

- Claim: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30988](https://arxiv.org/abs/2606.30988) Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force
- Locator: Abstract (full-text section)
- Evidence: 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only policies，并以 force-torque sensing 做真实任务案例。
- Quote: “Abstract Robot manipulation often depends on sensory data beyond vision, especially in contact-rich tasks where force, tactile, or audio feedback reveals interaction states not directly visible from images. Yet such modalities are hardware- and task-specific, and large multisensory datasets remain scarce, making it impractical to pretrain policies with every sensor they may encounter. We study multi-sensory continual learning : adapting a pretrained robot policy to new tasks with newly introduce”
- Authors: jaden-clark; changhao-wang; yihuai-gao; et al.

## References

- `2509.21986` [Developing Vision-Language-Action Model from Egocentric Videos](https://arxiv.org/abs/2509.21986) (2025-09-26T07:09:33Z)
- `2512.11047` [WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control](https://arxiv.org/abs/2512.11047) (2025-12-11T19:07:31Z)
- `2601.09708` [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](https://arxiv.org/abs/2601.09708) (2026-01-14)
- `2602.06001` [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) (2026-02-05)
- `2602.11291` [H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model](https://arxiv.org/abs/2602.11291) (2026-02-11T19:08:36Z)
- `2602.16710` [EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data](https://arxiv.org/abs/2602.16710) (2026-02-18T18:59:05Z)
- `2602.21161` [ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking](https://arxiv.org/abs/2602.21161) (2026-02-24)
- `2603.03279` [ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation](https://arxiv.org/abs/2603.03279) (2026-03-03T18:59:29Z)
- `2603.12553` [Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation](https://arxiv.org/abs/2603.12553) (2026-03-13T01:33:48Z)
- `2604.07335` [TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks](https://arxiv.org/abs/2604.07335) (2026-04-08)
- `2604.27224` [Learning Tactile-Aware Quadrupedal Loco-Manipulation Policies](https://arxiv.org/abs/2604.27224) (2026-04-29T21:46:58Z)
- `2605.00080` [World Model for Robot Learning: A Comprehensive Survey](https://arxiv.org/abs/2605.00080) (2026-04-30)
- `2605.07308` [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](https://arxiv.org/abs/2605.07308) (2026-05-08)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.03784` [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](https://arxiv.org/abs/2606.03784) (2026-06-02)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.06194` [ActiveMimic: Egocentric Video Pretraining with Active Perception](https://arxiv.org/abs/2606.06194) (2026-06-04T14:01:01Z)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.08765` [RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation](https://arxiv.org/abs/2606.08765) (2026-06-07)
- `2606.09630` [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630) (2026-06-08)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.13877` [ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13877) (2026-06-11)
- `2606.14981` [Inference-time Policy Steering via Vision and Touch](https://arxiv.org/abs/2606.14981) (2026-06-12)
- `2606.16690` [PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation](https://arxiv.org/abs/2606.16690) (2026-06-15)
- `2606.18043` [Uncertainty Quantification for Flow-Based Vision-Language-Action Models](https://arxiv.org/abs/2606.18043) (2026-06-16)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2606.26663` [Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention](https://arxiv.org/abs/2606.26663) (2026-06-25)
- `2606.26800` [SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation](https://arxiv.org/abs/2606.26800) (2026-06-25)
- `2606.28899` [You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact](https://arxiv.org/abs/2606.28899) (2026-06-27)
- `2606.29384` [Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model](https://arxiv.org/abs/2606.29384) (2026-06-28)
- `2606.30113` [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113) (2026-06-29)
- `2606.30456` [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456) (2026-06-29)
- `2606.30552` [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](https://arxiv.org/abs/2606.30552) (2026-06-29)
- `2606.30988` [Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force](https://arxiv.org/abs/2606.30988) (2026-06-29)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.03828` [ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Modeling](https://arxiv.org/abs/2607.03828) (2026-07-04T11:31:23Z)
- `2607.04234` [SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects](https://arxiv.org/abs/2607.04234) (2026-07-05)
- `2607.07196` [Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators](https://arxiv.org/abs/2607.07196) (2026-07-08)
- `2607.07287` [TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation](https://arxiv.org/abs/2607.07287) (2026-07-08)
- `2607.10132` [TAC-LOCO: Unified Whole-Body Control for Quadrupedal TACtile-Informed LOCO-Manipulation](https://arxiv.org/abs/2607.10132) (2026-07-11T05:45:24Z)
- `2607.15207` [BadWAM: When World-Action Models Dream Right but Act Wrong](https://arxiv.org/abs/2607.15207) (2026-07-16T17:04:15Z)
