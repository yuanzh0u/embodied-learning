# Evidence Appendix: 近一年具身感知问题是否已有效解决

- Time range: 2025-07-14..2026-07-14
- Events: 20
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DATA-2026-DQ-0002

- Claim: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06564](https://arxiv.org/abs/2607.06564) Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation
- Locator: Abstract; I Introduction; IV-C Geometry-Centric Masked Autoencoding; V-B Multi-Task on MetaWorld and RLBench
- Evidence: 论文将 2D VLA 的困难归因于几何理解和空间推理不足、3D 数据和强 3D encoder 稀缺、跨模态 lifting/projection 损失几何 fidelity；其 GC-MAE 用伪点云监督当前点云重建和未来几何演化，并在仿真与真实任务中提升成功率。
- Authors: jiaming-liu; qingpo-wuwu; nuowei-han; et al.

### EA-DATA-2026-4DDATA-0002

- Claim: 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction; Appendix D Data Collection Details; Appendix G Future Work
- Evidence: 论文用可见性mask保留部分遮挡轨迹并逐点逐时刻mask损失，认为这比丢弃含不可见点的轨迹能提供更多任务关键监督；附录说明真实视频需2D跟踪、深度提升到3D、SAM3分割人手并移除embodiment点。
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### EA-DATA-2026-4DDATA-0018

- Claim: 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control; A.1 Data Formatting; A.2 Tactile Sensor Data Processing
- Evidence: HapTile说明所有模态通过机器人控制循环同步，检查空/损坏轨迹和timestamp gaps，验证action-state consistency；附录还要求episode-level split避免temporal leakage，并保留raw/rectified tactile images。
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu

### EA-DATA-2026-4DDATA-0014

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation; IV-C Main Results; Table I
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Authors: yujie-zang; yuhang-zheng; xian-nie

### EA-EVAL-2026-0007

- Claim: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.04234](https://arxiv.org/abs/2607.04234) SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects
- Locator: arXiv HTML Abstract; 1 Introduction; 3.1 Benchmark Design; 4.2 Main Results
- Evidence: 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。
- Quote: “success-only evaluation substantially overstates policy performance”
- Authors: bowen-jing

### EA-SENSOR-2026-0004

- Claim: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.18043](https://arxiv.org/abs/2606.18043) Uncertainty Quantification for Flow-Based Vision-Language-Action Models
- Locator: arXiv HTML Abstract; 1 Introduction; Appendix B.4 Uncertainty Quantification
- Evidence: 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。
- Quote: “may fail without warning”
- Authors: ralf-romer

### EA-SENSOR-2026-0003

- Claim: VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.20754](https://arxiv.org/abs/2606.20754) Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models
- Locator: arXiv HTML Abstract; I Introduction; IV-D Main Results
- Evidence: 作者指出现代 VLA 常用回归或 flow-based action generation，缺少显式预测概率；他们通过对 transformer hidden activations 注入高斯扰动，利用扰动后动作预测分歧估计不确定性，并在 LIBERO/LIBERO-PRO 的分布偏移下提升失败检测。
- Quote: “failure detection under distribution shift”
- Authors: yousung-lee

### EA-SENSOR-2026-0006

- Claim: 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.28899](https://arxiv.org/abs/2606.28899) You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact
- Locator: arXiv HTML Abstract; 1 Introduction; 4.2 6-DoF Object Pose Estimation under Occlusion
- Evidence: 作者明确指出视觉位姿估计常在遮挡、差光照、反光或透明表面下失败，并提出 tactile-only pose estimation：把触觉接触表示成局部 3D 点云，结合校准传感器位姿恢复完整 6-DoF object pose；实验在视觉不可靠时优于视觉和几何基线。
- Quote: “vision-based methods often fail under occlusion”
- Authors: pengfei-ye

### EA-SENSOR-2026-0011

- Claim: RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29384](https://arxiv.org/abs/2606.29384) Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model
- Locator: arXiv HTML Abstract; 1 Introduction; B.2 Event Encoder and Feature Distillation
- Evidence: 作者指出现有 VLA 往往假设稳定明亮的室内环境，而真实操作中 illumination shifts 会造成 degraded RGB observations；Event-VLA 将 degraded visibility 定义为 RGB-centric policies 的鲁棒性问题，并通过 action-query routing 将 event streams 融入 action representation，仿真和真实部署实验显示在不同可见性下保持更强鲁棒性。
- Quote: “degraded RGB observations caused by illumination shifts”
- Authors: jiaxin-liu

### EA-SENSOR-2026-0009

- Claim: 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: arXiv HTML Abstract; 1 Introduction; 3.1 Tactile-Aware World Model; 4.2 Main Results
- Evidence: 作者指出 VLA 在 contact-rich tasks 中会被小接触扰动触发不可恢复失败，且这些失败常难以单靠视觉检测；TACO 用 tactile-aware world model 识别 failure-adjacent states、想象局部 correction segments 并标注可执行纠正动作，真实接触任务报告相对 base policy 的成功率提升。
- Quote: “hard to detect from vision alone”
- Authors: shengbang-liu

### EA-SENSOR-2026-0001

- Claim: 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.07287](https://arxiv.org/abs/2607.07287) TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation
- Locator: arXiv HTML Abstract; 1 Introduction
- Evidence: 作者把日常灵巧操作的误差来源明确落在滑移、错位、不稳定抓取和力不匹配上，并指出视觉/语言不能可靠揭示力、滑移和接触稳定性；其分层策略将视觉语言子任务规划、触觉世界模型预测和高频触觉残差修正分开。
- Quote: “hidden contact states such as force, slip, and contact stability”
- Authors: jianyi-zhou

### EA-PNAV-2026-0002

- Claim: 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.08325](https://arxiv.org/abs/2601.08325) ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation
- Locator: 4.1 Experimental Results
- Evidence: 结果段在报告总体领先的同时明确指出最难L4任务性能下降。
- Quote: “Although performance decreases on the most difficult L4 tasks (1.2%), ActiveVLA still demonstrates promising long-horizon reasoning and strong 3D perception for precise manipulation.”
- Authors: zhenyang-liu

### EA-PNAV-2026-0003

- Claim: OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.11072](https://arxiv.org/abs/2603.11072) OA-NBV: Occlusion-Aware Next-Best-View Planning for Human-Centered Active Perception on Mobile Robots
- Locator: V-B Limitations and future work.
- Evidence: 限制段直接划定即时单步观测与完整多视图任务之间的边界。
- Quote: “Finally, OA-NBV targets single-step viewpoint selection for immediate observation quality, rather than multi-view reconstruction.”
- Authors: boxun-hu

### EA-PNAV-2026-0004

- Claim: 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.14801](https://arxiv.org/abs/2605.14801) Exploring Bottlenecks in VLM-LLM Navigation: How 3D Scene Understanding Capability Impacts Zero-Shot VLN
- Locator: IV CONCLUSIONS
- Evidence: 结论直接同时报告感知饱和和两类仍关键的误差。
- Quote: “Our analysis also revealed that false positives and distorted bounding box aspect ratios are critical factors affecting navigation performance, and that a small set of core navigation-relevant object categories is sufficient for successful navigation.”
- Authors: ziyi-xia

### EA-SENSOR-2026-0002

- Claim: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08765](https://arxiv.org/abs/2606.08765) RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation
- Locator: arXiv HTML Abstract; 1 Introduction; 3.2 Force-Aware Kinematic Projection; 4.3 Ablation on RGB-S Design Choices
- Evidence: 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。
- Quote: “spatial uncertainty arising from kinematic and calibration errors”
- Authors: shengcheng-luo

### EA-SENSOR-2026-0008

- Claim: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26663](https://arxiv.org/abs/2606.26663) Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention
- Locator: arXiv HTML Abstract; I Introduction; Appendix B Method Details; Appendix D Limitations and Future Work
- Evidence: 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。
- Quote: “visually plausible futures can be physically incomplete”
- Authors: siyu-wu

### EA-SENSOR-2026-0010

- Claim: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30988](https://arxiv.org/abs/2606.30988) Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force
- Locator: arXiv HTML Abstract; 1 Introduction; 4.1 Cross-Modal Generalization
- Evidence: 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only policies，并以 force-torque sensing 做真实任务案例。
- Quote: “interaction states not directly visible from images”
- Authors: jaden-clark

### EA-PNAV-2026-0013

- Claim: 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.10348](https://arxiv.org/abs/2606.10348) Rethinking Embodied Navigation via Relational Inductive Bias
- Locator: Abstract > first paragraph
- Evidence: 引言直接描述视觉相似、静态先验和缺少动作验证导致的持续污染。
- Quote: “visual similarity can induce false positives, static priors are difficult to update once contradicted, and the lack of embodied verification may lead to repeated failed exploration, continuously contaminating map updates and navigation decisions.”
- Authors: weitao-an

### EA-SENSOR-2026-0005

- Claim: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.16690](https://arxiv.org/abs/2606.16690) PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation
- Locator: arXiv HTML Abstract; 1 Introduction ¶ S1.p1-S1.p3; 3.2 PATCH Monitor
- Evidence: 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差作为介入信号。
- Quote: “task-relevant execution risk from benign visual variation”
- Authors: yanan-zhou

### EA-SENSOR-2026-DQ-0006

- Claim: 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: Abstract; 1 Introduction; 2 Related Work; 3 Method; 5 Conclusion and Limitations
- Evidence: 论文指出 VLA 在接触丰富任务中会因轻微接触扰动产生不可恢复失败，这些失败难以从视觉单独检测；TACO 用 tactile-aware world model 将真实 rollout 中的失败邻近状态转成想象的视触觉纠正片段和可执行纠正动作，在真实接触任务中相对 base policy 提升 44 个百分点成功率。
- Authors: shengbang-liu; yueru-jia; yuyang-yan; et al.

## References

- `2601.08325` [ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation](https://arxiv.org/abs/2601.08325) (2026-01-13)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.11072` [OA-NBV: Occlusion-Aware Next-Best-View Planning for Human-Centered Active Perception on Mobile Robots](https://arxiv.org/abs/2603.11072) (2026-03-10)
- `2605.14801` [Exploring Bottlenecks in VLM-LLM Navigation: How 3D Scene Understanding Capability Impacts Zero-Shot VLN](https://arxiv.org/abs/2605.14801) (2026-05-14)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.08765` [RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation](https://arxiv.org/abs/2606.08765) (2026-06-07)
- `2606.10348` [Rethinking Embodied Navigation via Relational Inductive Bias](https://arxiv.org/abs/2606.10348) (2026-06-09)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.16690` [PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation](https://arxiv.org/abs/2606.16690) (2026-06-15)
- `2606.18043` [Uncertainty Quantification for Flow-Based Vision-Language-Action Models](https://arxiv.org/abs/2606.18043) (2026-06-16)
- `2606.20754` [Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models](https://arxiv.org/abs/2606.20754) (2026-06-18)
- `2606.26663` [Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention](https://arxiv.org/abs/2606.26663) (2026-06-25)
- `2606.28899` [You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact](https://arxiv.org/abs/2606.28899) (2026-06-27)
- `2606.29384` [Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model](https://arxiv.org/abs/2606.29384) (2026-06-28)
- `2606.30988` [Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force](https://arxiv.org/abs/2606.30988) (2026-06-29)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.04234` [SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects](https://arxiv.org/abs/2607.04234) (2026-07-05)
- `2607.06564` [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07)
- `2607.07287` [TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation](https://arxiv.org/abs/2607.07287) (2026-07-08)
