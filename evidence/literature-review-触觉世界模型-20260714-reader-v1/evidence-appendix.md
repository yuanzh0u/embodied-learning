# Evidence Appendix: 触觉世界模型

- Time range: 2026-01-14..2026-07-14
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DATA-READ-0008

- Claim: TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07335](https://arxiv.org/abs/2604.07335) TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks
- Locator: Abstract (full-text section)
- Evidence: 摘要明确列出精度/便携双模式采集、触觉恢复遥操作和人在环恢复数据。
- Quote: “To balance data quality and environmental diversity, we implement a dual-mode acquisition pipeline: a precision mode leveraging motion capture for high-fidelity demonstrations, and a portable mode utilizing VR-based tracking for in-the-wild acquisition and tactile-visualized recovery teleoperation. Building on this hardware, we unify large-scale tactile pretraining, task-specific bimanual demonstrations, and human-in-the-loop recovery data into a pyramid-structured data regime, enabling closed-l”
- Authors: longyan-wu; jieji-ren; chenghang-jiang; et al.

### EA-DATA-READ-0005

- Claim: 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 4.2 Vision-Based Tactile Sensing and Marker Tracking
- Evidence: HapTile 的每个夹爪手指安装视觉触觉传感器，接触会带来图像变化和 marker displacement；论文把 marker-motion 信号保存进数据集并用于 haptic feedback，实验也比较 vision-only、vision+tactile image 与 vision+tactile+marker 表征。
- Quote: “We smooth the signal with separate rise and release factors, producing a stable tactile motion estimate. The resulting marker-motion signal is stored in HapTile and is also used to drive haptic feedback.”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### EA-DATA-READ-0002

- Claim: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: Dream-Tac 把 world action model 扩展到触觉，联合建模当前视觉、触觉、语言指令下的未来视觉观测、未来触觉观测和动作 chunk，并加入 contact-gated visuotactile fusion 与 contact-aware attention bias。
- Quote: “In this paper, we propose Dream-Tac, a unified Tactile-World Action Model that jointly models actions, future visual observations, and tactile dynamics. Specifically, Dream-Tac introduces (i) contact-gated visuotactile fusion to selectively integrate tactile signals and (ii) a contact-aware attention bias to better regulate cross-modal interactions during manipulation.”
- Authors: yunfan-lou; yifan-ye; yankai-fu; et al.

### EA-DATA-READ-0006

- Claim: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-D 1 World Model Conditioning
- Evidence: TacForeSight 的 TacForceWM 从双指触觉观测出发，以高频腕部 force/torque 为条件预测短时域触觉 latent dynamics；ablation 中 wrist wrench 条件的未来触觉预测优于无条件版本，MSE 从 0.027 降到 0.017，cosine 从 0.954 提升到 0.992。
- Quote: “We first ablate the conditioning modality used in the tactile world model. We compare four conditioning designs: no external condition, RGB image condition, robot state condition, and wrist wrench condition. Prediction quality is evaluated using Mean Squared Error (MSE), cosine similarity (Cos), and symmetric KL divergence (KL sym ), which respectively measure element-wise prediction error, latent directional consistency, and latent distribution consistency. As shown in Table II , wrist wrench c”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### EA-DATA-READ-0003

- Claim: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13877](https://arxiv.org/abs/2606.13877) ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation
- Locator: Abstract (full-text section)
- Evidence: ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。
- Quote: “Abstract Contact-rich manipulation requires world models to reason over complex contact dynamics from multimodal sensory observations. However, it remains unclear which representation properties fundamentally support stable long-horizon planning in contact-rich settings. In this paper, we present ContactWorld, a benchmark and systematic empirical study of vision-tactile world models spanning 12 contact-rich manipulation tasks, including insertion, disassembly, screwing, and exploratory interacti”
- Authors: zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al.

### EA-DATA-READ-0004

- Claim: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.14981](https://arxiv.org/abs/2606.14981) Inference-time Policy Steering via Vision and Touch
- Locator: 5 Experiments
- Evidence: ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。
- Quote: “We evaluate ViTaL on three real-world contact-rich manipulation tasks. Our experiments are designed to answer three questions: whether multimodal visuo-tactile steering improves policy over unimodal guidance (Sec. 5.1 ); whether a learned latent world model and semantically aligned verifier provides reliable rewards for predicted outcomes (Sec. 5.2 ); and whether the proposed bi-level optimization balances performance and efficiency compared to naive visual-tactile fusion (Sec. 5.3 ). Robot Setu”
- Authors: yilin-wu; zilin-si; zeynep-temel; et al.

### EA-DATA-READ-0015

- Claim: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.18043](https://arxiv.org/abs/2606.18043) Uncertainty Quantification for Flow-Based Vision-Language-Action Models
- Locator: Abstract (full-text section)
- Evidence: 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。
- Quote: “This presents a critical limitation for real-world deployment in non-stationary environments, where models inevitably encounter scenarios outside their pretraining distribution and may fail without warning. To address this, we derive an efficient method for quantifying epistemic uncertainty in flow-matching models by leveraging velocity-field disagreement (VFD) across a small ensemble.”
- Authors: ralf-rmer

### EA-DATA-READ-0001

- Claim: VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.06001](https://arxiv.org/abs/2602.06001) Visuo-Tactile World Models
- Locator: B.0.1 Training dataset
- Evidence: 训练数据段明确列出了同步的本体状态、外部视频与双指触觉视频数据流。
- Quote: “Each sequence contains multimodal data streams: proprioceptive information (wrist pose, joint positions), exocentric video from the camera, and video from each Digit 360 fingertip sensor. All data streams were synchronized using timestamps and downsampled to 6 FPS for training the world model. Our training dataset for V-WM and VT-WM consists of 124 demonstrations totaling 112k datapoints, with each demonstration averaging 40 seconds. For validation, we use 26 demonstrations spanning all tasks, c”
- Authors: carolina-higuera; sergio-arnaud; byron-boots; et al.

### EA-DATA-READ-0007

- Claim: 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.07308](https://arxiv.org/abs/2605.07308) AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models
- Locator: 5 Conclusion
- Evidence: AT-VLA 把系统分为慢速视觉语言流和快速触觉流，慢速流负责任务理解和视觉定位，快速流以高频处理触觉反馈；作者采用 3:1 的快慢流频率比，并在真实接触丰富任务中验证 adaptive tactile injection、tactile gate、adaptive cross-attention 和 reaction dual-stream 的作用。
- Quote: “In summary, AT-VLA introduces an adaptive framework that seamlessly integrates tactile sensing into vision-language-action models. Through the Adaptive Tactile Injection mechanism, AT-VLA dynamically balances pretrained visual-language knowledge with newly learned tactile representations, preserving model integrity while enhancing action precision. The Tactile Reaction Dual-Stream mechanism further enables rapid, high-frequency tactile responses by decoupling slow perceptual reasoning from fast”
- Authors: xiaoqi-li; muhe-cai; jiadong-xu; et al.

### EA-DATA-READ-0014

- Claim: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08765](https://arxiv.org/abs/2606.08765) RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。
- Quote: “We then render force-modulated Gaussian saliency maps to model spatial uncertainty arising from kinematic and calibration errors.”
- Authors: shengcheng-luo

### EA-DATA-READ-0010

- Claim: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26663](https://arxiv.org/abs/2606.26663) Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention
- Locator: Abstract (full-text section)
- Evidence: 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。
- Quote: “In contact-rich manipulation, however, visually plausible futures can be physically incomplete: insertion, assembly, search, and reorientation often depend on slip, jamming, contact normals, or small alignment errors that are weakly visible or hidden in RGB. A natural solution is to predict future tactile states, however, we identify tactile pollution , a failure mode where unconstrained tactile-token injection degrades video and action prediction by forcing a visual dynamics model to absorb spa”
- Authors: siyu-wu; linjing-you; junjie-zhu; et al.

### EA-DATA-READ-0011

- Claim: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30988](https://arxiv.org/abs/2606.30988) Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force
- Locator: Abstract (full-text section)
- Evidence: 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only policies，并以 force-torque sensing 做真实任务案例。
- Quote: “Abstract Robot manipulation often depends on sensory data beyond vision, especially in contact-rich tasks where force, tactile, or audio feedback reveals interaction states not directly visible from images. Yet such modalities are hardware- and task-specific, and large multisensory datasets remain scarce, making it impractical to pretrain policies with every sensor they may encounter. We study multi-sensory continual learning : adapting a pretrained robot policy to new tasks with newly introduce”
- Authors: jaden-clark; changhao-wang; yihuai-gao; et al.

### EA-DATA-READ-0009

- Claim: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.16690](https://arxiv.org/abs/2606.16690) PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差作为介入信号。
- Quote: “Abstract Learning-based manipulation policies have made substantial progress in real-world robot manipulation, particularly for short-horizon action generation. However, deployment in open workspaces remains fragile under unexpected local scene dynamics, such as moving objects, transient occlusions, or disturbances near the intended motion. Existing runtime monitors often rely on global observation anomalies, policy uncertainty, or frame-level visual changes, and struggle to distinguish task-rel”
- Authors: yanan-zhou; ranpeng-qiu; yincong-chen; et al.

### EA-DATA-READ-0012

- Claim: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.04234](https://arxiv.org/abs/2607.04234) SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects
- Locator: 1 Introduction
- Evidence: 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。
- Quote: “Experiments show that success-only evaluation substantially overstates policy performance, as a large fraction of goal-completing rollouts violate physical safety, and that adding tactile sensing improves Safety Success while keeping Goal Success comparable and reduces object deformation during execution.”
- Authors: bowen-jing; mingxin-wang; ruiyang-hao; et al.

### EA-DATA-READ-0013

- Claim: 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。
- Stance: `gap` | Confidence: `direct`
- Paper: [2607.07196](https://arxiv.org/abs/2607.07196) Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators
- Locator: Abstract (full-text section)
- Evidence: 作者指出机器人中 World Models 越来越被用于模拟动作后果并给出 success/safety verdict，但视频生成指标如 FVD 奖励视觉真实感，却忽略世界是否对 policy actions 正确响应；他们主张作为 test oracle 的 WM 需要先通过 accreditation，并提出 L0-L4 admissibility ladder。
- Quote: “Abstract Across robotics, World Models (WMs) are increasingly used to evaluate action policies by simulating the consequences of actions in an imagined world, and returning a success or safety verdict. Yet a verdict is only as trustworthy as the WM that produced it, and the WM itself needs to be certified. In video-generation WMs , fidelity metrics such as Fréchet Video Distance (FVD) reward visual realism, but ignore whether the world responds correctly to the policy’s actions, including those”
- Authors: christian-oefinger

## References

- `2602.06001` [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) (2026-02-05)
- `2604.07335` [TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks](https://arxiv.org/abs/2604.07335) (2026-04-08)
- `2605.07308` [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](https://arxiv.org/abs/2605.07308) (2026-05-08)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.08765` [RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation](https://arxiv.org/abs/2606.08765) (2026-06-07)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.13877` [ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13877) (2026-06-11)
- `2606.14981` [Inference-time Policy Steering via Vision and Touch](https://arxiv.org/abs/2606.14981) (2026-06-12)
- `2606.16690` [PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation](https://arxiv.org/abs/2606.16690) (2026-06-15)
- `2606.18043` [Uncertainty Quantification for Flow-Based Vision-Language-Action Models](https://arxiv.org/abs/2606.18043) (2026-06-16)
- `2606.26663` [Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention](https://arxiv.org/abs/2606.26663) (2026-06-25)
- `2606.30988` [Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force](https://arxiv.org/abs/2606.30988) (2026-06-29)
- `2607.04234` [SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects](https://arxiv.org/abs/2607.04234) (2026-07-05)
- `2607.07196` [Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators](https://arxiv.org/abs/2607.07196) (2026-07-08)
