# Evidence Appendix: 近一年具身感知问题是否已有效解决

- Time range: 2025-07-14..2026-07-14
- Events: 19
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### ERR-PVC-READ-0015

- Claim: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06564](https://arxiv.org/abs/2607.06564) Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation
- Locator: I Introduction
- Evidence: 引言将操作需求归结为显式 3D 结构与时间一致性，并说明纯 2D 管线及有损的跨模态变换会削弱这些约束。
- Quote: “Despite this progress, robotic manipulation fundamentally requires spatial reasoning in the physical world [ 57 , 82 , 12 , 13 , 59 ] : the robot must infer 3D structure, reason about geometric relationships (e.g., reachability, occlusion, and contact), and plan actions that remain temporally consistent as the geometry evolves. Purely 2D VLA pipelines often struggle to reliably capture these geometric constraints, particularly in cluttered or dynamic environments. A natural direction is to expli”
- Authors: jiaming-liu; qingpo-wuwu; nuowei-han; et al.

### EA-4D-READ-0012

- Claim: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction
- Evidence: 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。
- Quote: “The primary advantage of 3PoinTr is that it trains on data General Flow ignores. Real-world points are often temporarily occluded; General Flow removes any trajectory with invisible point-timestep pairs during preprocessing, whereas 3PoinTr retains all trajectories and masks losses for individual invisible point-timestep pairs. This provides additional supervision over task-critical object points that are temporarily occluded during manipulation. For example, in the Throw Away Paper task, every”
- Authors: adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski

### EA-TWM-READ-0012

- Claim: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.04234](https://arxiv.org/abs/2607.04234) SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects
- Locator: 1 Introduction
- Evidence: 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。
- Quote: “Experiments show that success-only evaluation substantially overstates policy performance, as a large fraction of goal-completing rollouts violate physical safety, and that adding tactile sensing improves Safety Success while keeping Goal Success comparable and reduces object deformation during execution.”
- Authors: bowen-jing; mingxin-wang; ruiyang-hao; et al.

### EA-SENSORERR-READ-0008

- Claim: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.18043](https://arxiv.org/abs/2606.18043) Uncertainty Quantification for Flow-Based Vision-Language-Action Models
- Locator: Abstract (full-text section)
- Evidence: 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。
- Quote: “This presents a critical limitation for real-world deployment in non-stationary environments, where models inevitably encounter scenarios outside their pretraining distribution and may fail without warning. To address this, we derive an efficient method for quantifying epistemic uncertainty in flow-matching models by leveraging velocity-field disagreement (VFD) across a small ensemble.”
- Authors: ralf-rmer; maximilian-seeliger; saida-liu; et al.

### EA-SENSORERR-READ-0009

- Claim: VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.20754](https://arxiv.org/abs/2606.20754) Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models
- Locator: Abstract (full-text section)
- Evidence: 作者指出现代 VLA 常用回归或 flow-based action generation，缺少显式预测概率；他们通过对 transformer hidden activations 注入高斯扰动，利用扰动后动作预测分歧估计不确定性，并在 LIBERO/LIBERO-PRO 的分布偏移下提升失败检测。
- Quote: “Specifically, we inject Gaussian perturbations into transformer hidden activations and estimate epistemic signals from disagreement across perturbed action predictions. Experiments on LIBERO and LIBERO-PRO show that perturbation-based uncertainty consistently improves failure detection under distribution shift compared to sampling-based uncertainty, providing a practical uncertainty signal for VLA models.”
- Authors: yousung-lee; dongsoo-har

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

### EA-SENSORERR-READ-0014

- Claim: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control
- Evidence: 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。
- Quote: “All data modalities are synchronized through the robot control loop. For policy learning, actions are converted to a unified 7D end-effector delta representation (1) where are translational deltas, are rotational deltas, and is the gripper command. This decouples learning from the exact robot configuration, enabling cross-embodiment by focusing the policy on local contact adjustment from tactile feedback. Several quality checks are applied to every collected trajectory. Empty or corrupted trajec”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### EA-SENSORERR-READ-0007

- Claim: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08765](https://arxiv.org/abs/2606.08765) RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。
- Quote: “We then render force-modulated Gaussian saliency maps to model spatial uncertainty arising from kinematic and calibration errors.”
- Authors: shengcheng-luo

### EA-SENSORERR-READ-0015

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Quote: “Policies in this setting are trained using both nominal demonstrations and recovery interaction data.”
- Authors: yujie-zang; yuhang-zheng; xian-nie; et al.

### EA-SENSORERR-READ-0003

- Claim: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26663](https://arxiv.org/abs/2606.26663) Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention
- Locator: Abstract (full-text section)
- Evidence: 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。
- Quote: “In contact-rich manipulation, however, visually plausible futures can be physically incomplete: insertion, assembly, search, and reorientation often depend on slip, jamming, contact normals, or small alignment errors that are weakly visible or hidden in RGB. A natural solution is to predict future tactile states, however, we identify tactile pollution , a failure mode where unconstrained tactile-token injection degrades video and action prediction by forcing a visual dynamics model to absorb spa”
- Authors: siyu-wu

### EA-SENSORERR-READ-0004

- Claim: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30988](https://arxiv.org/abs/2606.30988) Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force
- Locator: Abstract (full-text section)
- Evidence: 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only policies，并以 force-torque sensing 做真实任务案例。
- Quote: “Abstract Robot manipulation often depends on sensory data beyond vision, especially in contact-rich tasks where force, tactile, or audio feedback reveals interaction states not directly visible from images. Yet such modalities are hardware- and task-specific, and large multisensory datasets remain scarce, making it impractical to pretrain policies with every sensor they may encounter. We study multi-sensory continual learning : adapting a pretrained robot policy to new tasks with newly introduce”
- Authors: jaden-clark; changhao-wang; yihuai-gao; et al.

### EA-PNAV-2026-0013

- Claim: 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.10348](https://arxiv.org/abs/2606.10348) Rethinking Embodied Navigation via Relational Inductive Bias
- Locator: Abstract > first paragraph
- Evidence: 引言直接描述视觉相似、静态先验和缺少动作验证导致的持续污染。
- Quote: “visual similarity can induce false positives, static priors are difficult to update once contradicted, and the lack of embodied verification may lead to repeated failed exploration, continuously contaminating map updates and navigation decisions.”
- Authors: weitao-an

### EA-SENSORERR-READ-0002

- Claim: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.16690](https://arxiv.org/abs/2606.16690) PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差作为介入信号。
- Quote: “Abstract Learning-based manipulation policies have made substantial progress in real-world robot manipulation, particularly for short-horizon action generation. However, deployment in open workspaces remains fragile under unexpected local scene dynamics, such as moving objects, transient occlusions, or disturbances near the intended motion. Existing runtime monitors often rely on global observation anomalies, policy uncertainty, or frame-level visual changes, and struggle to distinguish task-rel”
- Authors: yanan-zhou; ranpeng-qiu; yincong-chen; et al.

### EA-SENSORERR-READ-0001

- Claim: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: 5 Conclusion and Limitations
- Evidence: 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。
- Quote: “We presented TACO, a tactile-aware world-model-driven framework for scalable VLA post-training in contact-rich manipulation. Following a Recognize–Imagine–Label loop, TACO converts real-world failures into imagined corrections without repeated human intervention: a tactile-aware world model jointly denoises future video and force sequences, while a unified progress-action model recognizes failure-adjacent states and labels imagined segments with corrective actions. To incorporate this supervisio”
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
