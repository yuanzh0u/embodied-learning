# Evidence Appendix: LeWorldModel 技术谱系：JEPA 潜空间世界模型到规划控制

- Time range: 2026-01-24..2026-07-24
- Events: 76
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-JIMFAN-READ-0015

- Claim: DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and planning benefits after robot post-training.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.06949](https://arxiv.org/abs/2602.06949) DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos
- Locator: 4.7 Downstream Applications
- Evidence: Its policy-evaluation correlation is measured on 20 fruit-packing scenes; the paper also acknowledges optimistic simulation and coverage limitations.
- Authors: shenyuan-gao; william-liang; kaiyuan-zheng; et al.

### EA-WMDATA-READ-0007

- Claim: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-real correlation.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08546](https://arxiv.org/abs/2603.08546) Interactive World Simulator for Robot Policy Training and Evaluation
- Locator: IV-C Data Generation for Policy Training
- Evidence: The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real performance correlation.
- Authors: yixuan-wang; rhythm-syed; fangyu-wu; et al.

### EA-WMDATA-READ-0008

- Claim: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon future evolution rather than only behavior-cloning actions.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.20752](https://arxiv.org/abs/2605.20752) GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation
- Locator: 3.4 GaussianDream Training and Efficient Inference
- Evidence: GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference.
- Authors: zijian-zhang; yuqing-jiang; qian-cheng; et al.

### EA-TWM-READ-0003

- Claim: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13877](https://arxiv.org/abs/2606.13877) ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation
- Locator: Abstract (full-text section)
- Evidence: ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。
- Authors: zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al.

### EA-TWM-READ-0004

- Claim: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.14981](https://arxiv.org/abs/2606.14981) Inference-time Policy Steering via Vision and Touch
- Locator: 5 Experiments
- Evidence: ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。
- Authors: yilin-wu; zilin-si; zeynep-temel; et al.

### EA-WMEVAL-READ-0005

- Claim: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22882](https://arxiv.org/abs/2605.22882) GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into executable trajectories; the paper reports real-world manipulation success improving from 61% to 81%.
- Authors: kaichen-zhou; yuzhen-chen; fangneng-zhan; et al.

### EA-WMEVAL-READ-0003

- Claim: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information downstream policies need.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00664](https://arxiv.org/abs/2606.00664) SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models
- Locator: Abstract (full-text section)
- Evidence: SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as policy-training data.
- Authors: ziheng-he; yixiang-chen; ning-yang; et al.

### EA-WMEVAL-READ-0001

- Claim: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接报告了异构数据组成与 modality-specific supervision masks。
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### EA-WMEVAL-READ-0010

- Claim: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13672](https://arxiv.org/abs/2606.13672) $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
- Locator: 3 WEAVER : World Estimation Across Views for Embodied Reasoning
- Evidence: The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthetic policy improvement, and test-time planning.
- Authors: arnav-kumar-jain; yilin-wu; jesse-farebrother; et al.

### EA-WMEVAL-READ-0013

- Claim: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.12403](https://arxiv.org/abs/2606.12403) World Pilot: Steering Vision-Language-Action Models with World-Action Priors
- Locator: Abstract (full-text section)
- Evidence: World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy.
- Authors: zefu-lin; rongxu-cui; junjia-xu; et al.

### EA-WMEVAL-READ-0004

- Claim: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.
- Stance: `gap` | Confidence: `direct`
- Paper: [2605.29360](https://arxiv.org/abs/2605.29360) MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models
- Locator: Abstract (full-text section)
- Evidence: The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias.
- Authors: tianzhuo-yang; zihan-shen; zirui-mi; et al.

### EA-LEWM-READ-0081

- Claim: V-JEPA 2 的无动作视频预训练预测不直接包含机器人动作的因果效应；论文是在冻结视频编码器上另行训练帧因果、动作条件预测器，才把表征接到规划。
- Stance: `support` | Confidence: `direct`
- Paper: [2506.09985](https://arxiv.org/abs/2506.09985) V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning
- Locator: 3 V-JEPA 2-AC: Learning an Action-Conditioned World Model
- Evidence: 方法章节明确说明预训练后的缺失视频预测不考虑智能体动作因果，并把小规模交互数据后训练定义为使模型可用于规划的下一阶段。
- Authors: mahmoud-assran; adrien-bardes; david-fan; et al.

### EA-LEWM-READ-0082

- Claim: V-JEPA 2 的表征目标是预测场景中可预测的方面，而不是复原生成目标强调的所有像素级不可预测细节。
- Stance: `support` | Confidence: `direct`
- Paper: [2506.09985](https://arxiv.org/abs/2506.09985) V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning
- Locator: 1 Introduction
- Evidence: 引言把 JEPA 的可预测表征目标与像素生成目标并列，并用运动轨迹和草叶细节说明选择性。
- Authors: mahmoud-assran; adrien-bardes; david-fan; et al.

### EA-LEWM-READ-0084

- Claim: 在论文展示的三个单目标 reaching 实例中，V-JEPA 2-AC 把末端移动到距目标不足 4 cm，并选择使误差单调下降的动作。
- Stance: `support` | Confidence: `direct`
- Paper: [2506.09985](https://arxiv.org/abs/2506.09985) V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning
- Locator: 4.2 Results
- Evidence: 结果章节用末端目标距离报告三个单目标 reaching 执行，并同时观察到误差单调下降。
- Authors: mahmoud-assran; adrien-bardes; david-fan; et al.

### EA-LEWM-READ-0026

- Claim: LeJEPA selects an Epps–Pulley empirical-characteristic-function regularizer because the implementation is DDP-friendly, has uniformly bounded gradients and curvature, and has linear memory and computational complexity.
- Stance: `support` | Confidence: `direct`
- Paper: [2511.08544](https://arxiv.org/abs/2511.08544) LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics
- Locator: 4.2.3 Characteristic Functions are Stable, Scalable and Identifiable
- Evidence: Section 4.2.3 明确比较统计检验家族后列出 Epps–Pulley 的 distributed、bounded 与 linear-complexity 性质。
- Authors: randall-balestriero; yann-lecun

### EA-LEWM-READ-0027

- Claim: The LeJEPA objective combines the multi-view prediction loss with SIGReg and removes prototypes, stop-gradients, and teacher–student networks, leaving one coefficient to trade prediction against isotropic-Gaussian regularization.
- Stance: `support` | Confidence: `direct`
- Paper: [2511.08544](https://arxiv.org/abs/2511.08544) LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics
- Locator: 5.1 LeJEPA: SIGReg + Prediction Loss
- Evidence: Section 5.1 给出最终组合损失并明确列出不再需要的 collapse-prevention 组件和 mixing coefficient 的含义。
- Authors: randall-balestriero; yann-lecun

### EA-LEWM-READ-0029

- Claim: On ImageNet-10, LeJEPA pretrained approximately 50 architectures from eight families with fewer than 20 million parameters, and all reached 91.5%–95% top-1 accuracy under frozen-backbone linear probing.
- Stance: `support` | Confidence: `direct`
- Paper: [2511.08544](https://arxiv.org/abs/2511.08544) LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics
- Locator: 6.1 LeJEPA’s Stability Across Hyper-Parameters and Architectures
- Evidence: Section 6.1 直接给出模型数量、架构族、参数上限和 frozen linear-probe top-1 区间。
- Authors: randall-balestriero; yann-lecun

### EA-ALIGN-READ-0013

- Claim: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.09708](https://arxiv.org/abs/2601.09708) Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning
- Locator: 5 Conclusion
- Evidence: 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。
- Authors: chi-pin-huang; yunze-man; zhiding-yu; et al.

### EA-LEWM-READ-0001

- Claim: LeWorldModel jointly trains a pixel encoder and an action-conditioned latent predictor; actions enter the predictor through AdaLN at every layer, and the predictor autoregressively forecasts the next latent from a history of frame representations.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19312](https://arxiv.org/abs/2603.19312) LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
- Locator: 3 Method: LeWorldModel
- Evidence: 方法段明确描述 encoder、predictor、AdaLN 动作注入、causal autoregression，并说明所有组件联合学习。
- Authors: lucas-maes; quentin-le-lidec; damien-scieur; et al.

### EA-LEWM-READ-0002

- Claim: SIGReg regularizes LeWM latents toward an isotropic Gaussian by projecting them onto random unit directions and matching each one-dimensional projection with an Epps–Pulley normality statistic; the joint-distribution argument is asymptotic in the number of projections.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19312](https://arxiv.org/abs/2603.19312) LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
- Locator: Appendix A SIGReg
- Evidence: SIGReg 附录明确给出随机方向、一维 Epps–Pulley 匹配、Cramér–Wold 连接及其渐近限定。
- Authors: lucas-maes; quentin-le-lidec; damien-scieur; et al.

### EA-LEWM-READ-0004

- Claim: In the paper's simulated benchmark setup, LeWM achieved an 18% higher Push-T success rate than PLDM, while the fixed planning configuration completed a full plan in under one second; this did not translate into dominance on every environment.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19312](https://arxiv.org/abs/2603.19312) LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
- Locator: 4.2 Towards Efficient Planning with WMs, Figure 3 and Figure 6
- Evidence: 4.2 同时报告 Push-T 相对 PLDM 的成功率差、低于一秒的完整规划，以及 Two-Room 反例。
- Authors: lucas-maes; quentin-le-lidec; damien-scieur; et al.

### EA-LEWM-READ-0005

- Claim: The paper's direct cross-seed stability check is narrow: on Push-T, across three training seeds evaluated on the same 50 trajectories, PLDM exhibited higher success-rate variance than LeWM.
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19312](https://arxiv.org/abs/2603.19312) LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
- Locator: Appendix G Ablations., Table 5
- Evidence: Appendix G Table 5 报告三 seed、同一 50 条 Push-T 轨迹的 success rate 与方差，并明确 PLDM 方差更高。
- Authors: lucas-maes; quentin-le-lidec; damien-scieur; et al.

### EA-ALIGN-READ-0014

- Claim: 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.00080](https://arxiv.org/abs/2605.00080) World Model for Robot Learning: A Comprehensive Survey
- Locator: 1 Introduction
- Evidence: 引言直接将纯反应 VLA 的三类困难列为长时程推理、temporal credit assignment 与 compounding errors。
- Authors: bohan-hou; gen-li; jindou-jia; et al.

### EA-LEWM-READ-0087

- Claim: 该研究固定数据、历史长度、动作条件、转移架构、优化器和训练日程，仅改变冻结编码器、可选适配器与解码路径，从而把编码器定义的潜接口作为主要实验变量。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.06388](https://arxiv.org/abs/2605.06388) Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models
- Locator: 3.1 Dataset and Training
- Evidence: 训练协议章节逐项列出固定量和变化量，并为每个编码器—适配器组合从头训练 LDM。
- Authors: nilaksh; saurav-jha; artem-zholus; et al.

### EA-LEWM-READ-0041

- Claim: RC-aux 通过多时域开放环预测修正时间错配，并以预算条件、方向敏感的轨迹可达性监督修正空间几何；测试时还可按剩余预算把可达性作为显式搜索信号。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.07278](https://arxiv.org/abs/2605.07278) Predictive but Not Plannable: RC-aux for Latent World Models
- Locator: 1 Introduction
- Evidence: 引言明确把 RC-aux 分成时间与空间两条监督轴，并说明测试时规划器如何使用可达性信号。
- Authors: wenyuan-li; guang-li; keisuke-maeda; et al.

### EA-LEWM-READ-0042

- Claim: 在论文的五个匹配 LeWM-family 比较中，RC-aux 改善四项；Wall 成功率从 50.4±6.5 提升到 83.6±3.6，即提高 33.2 个百分点。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.07278](https://arxiv.org/abs/2605.07278) Predictive but Not Plannable: RC-aux for Latent World Models
- Locator: 4.2 Main Results
- Evidence: 表 1 同时给出 LeWM、RC-aux 和 matched delta，正文说明 Wall 是最大增益且该任务没有 continuation checkpoint。
- Authors: wenyuan-li; guang-li; keisuke-maeda; et al.

### EA-LEWM-READ-0021

- Claim: GC-IDM freezes the LeWorldModel representation and amortizes planning into a horizon-conditioned inverse map from current and goal latents to the next action; at test time it re-encodes the actual observation each step and performs no latent rollout or online search.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.08732](https://arxiv.org/abs/2605.08732) Latent Geometry Beyond Search: Amortizing Planning in World Models
- Locator: 4 Method: Goal-Conditioned Inverse Dynamics Model (GC-IDM)
- Evidence: 方法图和正文明确给出冻结 LeWM embeddings、随机 horizon 训练元组、只更新 inverse module，以及逐步重编码/单次前向的推理路径。
- Authors: hoang-nguyen; xiaohao-xu; xiaonan-huang

### EA-LEWM-READ-0022

- Claim: On the eight environment–protocol cells in the main LeWM benchmark comparison, GC-IDM matched or outperformed CEM in seven, with Push-T as the lone exception.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.08732](https://arxiv.org/abs/2605.08732) Latent Geometry Beyond Search: Amortizing Planning in World Models
- Locator: 5.3 Main Results
- Evidence: 主结果按 environment–protocol cell 汇总，明确报告 seven of eight，并指出 Push-T 是唯一例外。
- Authors: hoang-nguyen; xiaohao-xu; xiaonan-huang

### EA-LEWM-READ-0046

- Claim: 在固定 hard n100 TwoRoom 协议中，只替换终端 selector 的 full-horizon TRM 将 LeWM 平均成功率从 7.0% 提升到 97.0%，将本地 PLDM 从 32.7% 提升到 84.0%；同架构 shuffled-label heads 在两类模型上均为 0.0%。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22164](https://arxiv.org/abs/2605.22164) Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics
- Locator: 6.1 TRM Repairs Hard TwoRoom in Fixed Terminal Selection
- Evidence: 6.1 节声明所有 checkpoint、cache、manifest、CEM 与候选采样保持不变，并在表 1 中报告真实时间标签与 shuffled control。
- Authors: liangyu-li; shengzhi-wang; qingwen-liu

### EA-LEWM-READ-0047

- Claim: 在 LeWM seed 3072 的 matched-b50 消融中，平衡满 episode TRM 使用 100,000 pairs 达到 97.5% 成功率，而相同 pair 预算的平衡短时域 max 版本仅 35.0%。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22164](https://arxiv.org/abs/2605.22164) Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics
- Locator: 6.2 Horizon Matching and Temporal Structure Matter
- Evidence: 6.2 节与附录 C.5 在相同 pair 预算下比较 full-episode 和 max-horizon，并把 horizon matching 识别为最强因素。
- Authors: liangyu-li; shengzhi-wang; qingwen-liu

### EA-LEWM-READ-0048

- Claim: 在 matched-b50 TwoRoom 中，XY probe rowspace 只贡献 0.5–0.7% 的终端—目标潜 MSE，却使 rowspace-only planning 达到 90.8% 平均成功率；raw latent MSE 和 residual-only 均为 1.7%。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.22164](https://arxiv.org/abs/2605.22164) Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics
- Locator: 6.3 Mechanism: Raw Latent MSE Hides the Useful State
- Evidence: 6.3 节的 rowspace surgery 直接保留或移除 XY probe 子空间，且规划时不使用真实 simulator state。
- Authors: liangyu-li; shengzhi-wang; qingwen-liu

### EA-LEWM-READ-0008

- Claim: Fast-LeWM replaces LeWM's within-window autoregressive latent chain with action-prefix prediction: every future latent is predicted directly from the same observed anchor latent and its causal action prefix, so all queried horizons can be produced in parallel.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26217](https://arxiv.org/abs/2606.26217) Fast LeWorldModel
- Locator: 3.3 Fast LeWorldModel
- Evidence: 3.3 明确给出 anchor latent、prefix token、dense horizon targets 与并行预测，并说明 future predictions 不再顺序依赖彼此。
- Authors: yuntian-gao; xiangyu-xu

### EA-LEWM-READ-0009

- Claim: Under the same four-task LeWM planning protocol, base Fast-LeWM increased average success from 85.8% to 90.5%, and optional self-consistency increased it to 92.0%; no environment had lower point-estimate success than LeWM.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26217](https://arxiv.org/abs/2606.26217) Fast LeWorldModel
- Locator: 3.7 Planning with Action Prefixes and Self-Consistency
- Evidence: Table 1 完整列出四环境和平均成功率，base 与 self-consistency variant 在每列都不低于 LeWM。
- Authors: yuntian-gao; xiangyu-xu

### EA-LEWM-READ-0011

- Claim: Across all four tasks, Fast-LeWM had lower initial open-loop latent error and a smaller least-squares error-growth slope than LeWM, while qualitative decoded rollouts showed less long-horizon drift.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26217](https://arxiv.org/abs/2606.26217) Fast LeWorldModel
- Locator: 4.3 Open-Loop Latent Prediction
- Evidence: 4.3 以 ground-truth future-frame latents 对齐，比较 loss curve 起点、增长斜率和 decoder rollout。
- Authors: yuntian-gao; xiangyu-xu

### EA-LEWM-READ-0061

- Claim: LDAD decodes the executed action from the latent displacement alone, so successful recovery requires local transition geometry to encode the action and encourages different actions to induce distinguishable latent changes for planning.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.31232](https://arxiv.org/abs/2606.31232) Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding
- Locator: Action-Supervised Displacement Mechanism.
- Evidence: 方法段明确将 action decoder 的唯一输入设为 displacement，并解释 action recovery、transition distinguishability 与 planner candidate comparison 的关系。
- Authors: zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al.

### EA-LEWM-READ-0062

- Claim: Across the four evaluated environments, Delta-JEPA had the highest mean planning success; it exceeded the strongest OGB-Cube baseline by 15.14 percentage points and LeWM on Push-T by 4.54 points.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.31232](https://arxiv.org/abs/2606.31232) Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding
- Locator: Planning Performance
- Evidence: 主结果段给出四环境全部最高及 OGB-Cube、Push-T 的明确百分点差。
- Authors: zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al.

### EA-LEWM-READ-0063

- Claim: With the training and planning protocol held fixed, decoding actions from latent displacements improved planning relative to decoding from concatenated endpoint embeddings in every evaluated environment.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.31232](https://arxiv.org/abs/2606.31232) Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding
- Locator: Ablation Study > Displacement-Based Action Decoding.
- Evidence: 该消融明确说明两变体只在 action-decoder input 上不同，并报告 displacement variant 跨四环境一致改善。
- Authors: zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al.

### EA-LEWM-READ-0064

- Claim: When the starting history is fixed and only the action input is varied, Delta-JEPA produces separated action-wise predictor responses, whereas LeWM's responses remain concentrated near the origin and substantially overlap.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.31232](https://arxiv.org/abs/2606.31232) Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding
- Locator: Action-Sensitive Latent Dynamics
- Evidence: 作者固定 512 个 Two-Room histories 并逐 action 干预 predictor，比较 action-wise mean displacement。
- Authors: zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al.

### EA-LEWM-READ-0052

- Claim: Empirical-macro CEM 不在连续潜 macro-action 空间中无约束搜索，而从训练轨迹编码的 macro-action 序列 bank 采样 anchor，并只在其附近拟合局部 residual。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12547](https://arxiv.org/abs/2607.12547) Mind the Gap: Promises and Pitfalls of Hierarchical Planning in LeWorldModel
- Locator: 3.3 Planning-Side Mitigations
- Evidence: 3.3 节给出方法动机，附录 C.6 进一步说明每轮重采样 anchor、只 refit residual 并保留零残差候选。
- Authors: niccol-caselli; francesco-massafra; samuele-punzo; et al.

### EA-LEWM-READ-0083

- Claim: V-JEPA 2-AC 与论文基线使用同一套目标实验室协议部署在两座 Droid 未覆盖的实验室，输入为未标定、低分辨率单目 RGB，相同 V-JEPA 2-AC 权重和推理代码跨实验室复用。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2506.09985](https://arxiv.org/abs/2506.09985) V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning
- Locator: 4 Planning: Zero-shot Robot Control
- Evidence: 规划章节明确记录两座新实验室、Franka 平台、未标定单目相机及跨机器人复用权重和推理代码。
- Authors: mahmoud-assran; adrien-bardes; david-fan; et al.

### EA-LEWM-READ-0028

- Claim: The nonlinear-probe optimality result is conditional on a smooth embedding density with finite Fisher information and covariance, test queries drawn from the training distribution, an isotropic mean-zero target-gradient prior, and a fixed scalar covariance constraint.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.08544](https://arxiv.org/abs/2511.08544) LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics
- Locator: A.1 kNN Probing
- Evidence: Appendix A.1 在给出 kNN 唯一最优解前逐项列出 density、query、target function 与 covariance constraints。
- Authors: randall-balestriero; yann-lecun

### EA-LEWM-READ-0003

- Claim: LeWM planning is explicitly short-horizon and conditional: longer autoregressive rollouts trade additional lookahead for more compute and model bias, so the controller executes only a planned action block before replanning from a new observation.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.19312](https://arxiv.org/abs/2603.19312) LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
- Locator: 3.2 Latent Planning
- Evidence: 规划段直接陈述 horizon 的计算/偏差权衡、误差累积和 MPC 重规划缓解机制。
- Authors: lucas-maes; quentin-le-lidec; damien-scieur; et al.

### EA-LEWM-READ-0088

- Claim: 在论文的共享 Bridge V2 任务统计中，语义潜空间家族相对重建家族的 VLA 成功率高 9.8 个百分点、OOD 成功率高 13.6 个百分点，并把一步 CEM 动作误差降低 0.0266；三项 95% 配对 bootstrap 区间均不跨零。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.06388](https://arxiv.org/abs/2605.06388) Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models
- Locator: D.3 Statistical Analyses
- Evidence: 附录统计以共享任务做家族级配对 bootstrap，同时报告策略成功、OOD 成功和 CEM 动作恢复三个面向控制的指标。
- Authors: nilaksh; saurav-jha; artem-zholus; et al.

### EA-LEWM-READ-0089

- Claim: 在 DiT-S 的真实编码潜变量上，语义编码器的 IDM Pearson 为 0.772–0.829、轨迹成功分类准确率为 0.903–0.906；重建编码器对应范围为 0.507–0.626 和 0.835–0.868，且动作信息优势大体延续到世界模型生成潜变量。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.06388](https://arxiv.org/abs/2605.06388) Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models
- Locator: 4.2 Does the latent space affect action recoverability and preservation of task semantics?
- Evidence: 表 2 同时报告真实编码潜变量与生成潜变量的 IDM 和成功分类结果，正文总结语义家族保留更多动作信息。
- Authors: nilaksh; saurav-jha; artem-zholus; et al.

### EA-LEWM-READ-0090

- Claim: 在该受控实验中，重建对齐潜空间仍能保持较锐利的局部外观，但语义潜空间通常在全局结构和时序生成指标上更强；因此低层像素质量不足以解释策略效用。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.06388](https://arxiv.org/abs/2605.06388) Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models
- Locator: 4.3 How does the latent space affect visual fidelity?
- Evidence: 视觉结果章节同时报告语义模型的结构与视频指标优势和 VAE 类模型的局部外观竞争力。
- Authors: nilaksh; saurav-jha; artem-zholus; et al.

### EA-LEWM-READ-0091

- Claim: 论文的质性 rollout 显示两类潜空间会以不同方式失败：重建潜变量可能生成外观连贯但任务语义错误的状态，语义潜变量较能保持任务意图，却可能损失几何和接触精度。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.06388](https://arxiv.org/abs/2605.06388) Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models
- Locator: 4.5 Do reconstruction-aligned and semantic encoders fail differently?
- Evidence: 失败分析用篮子、毛巾、抽屉和指令变化案例区分任务语义幻觉与几何接触不足。
- Authors: nilaksh; saurav-jha; artem-zholus; et al.

### EA-LEWM-READ-0092

- Claim: 把高维语义特征压缩到适配器潜空间通常更利于扩散去噪和高层任务完成，但会恶化潜空间 CEM 动作误差、OOD 鲁棒性或点跟踪等精细控制指标。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.06388](https://arxiv.org/abs/2605.06388) Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models
- Locator: 4.6 Do compressed adapter latents aid semantic encoders further for world modeling?
- Evidence: 适配器消融把多数指标的改善与 CEM、OOD 和 PCK 的例外并列，并给出压缩损失精细动作信息的解释。
- Authors: nilaksh; saurav-jha; artem-zholus; et al.

### EA-LEWM-READ-0043

- Claim: Wall 消融中，RC-aux 训练后的模型即使仍用基础终端潜距离规划也达到 72.4±3.6%，高于 LeWM-family control 的 50.4±6.5%；加入可达性感知规划后进一步达到 83.6±3.6%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.07278](https://arxiv.org/abs/2605.07278) Predictive but Not Plannable: RC-aux for Latent World Models
- Locator: 4.2 Main Results
- Evidence: 表 2 在相同任务上并列 control、RC-aux-trained/base planner 与完整 RC-aux，能区分两层干预。
- Authors: wenyuan-li; guang-li; keisuke-maeda; et al.

### EA-LEWM-READ-0044

- Claim: 在 LIBERO-Goal 的可训练 no-repeat OFT-style 动作头协议中，RC-aux 表征的平均成功率为 0.812，高于 LeWM 表征的 0.712；repeat tuning 后 RC-aux 为 0.864。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.07278](https://arxiv.org/abs/2605.07278) Predictive but Not Plannable: RC-aux for Latent World Models
- Locator: 4.4 Model Size and Computational Overhead, Table 5
- Evidence: 表 5 明确区分 matched no-repeat 比较、repeat-tuned 结果和外部 OpenVLA-OFT 参考。
- Authors: wenyuan-li; guang-li; keisuke-maeda; et al.

### EA-LEWM-READ-0023

- Claim: The paper's explanation that isotropic LeWM geometry makes inverse dynamics well conditioned is explicitly conditional: the authors did not verify that LeWM fully satisfies the stated geometric assumptions and did not ablate against a non-isotropic baseline.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.08732](https://arxiv.org/abs/2605.08732) Latent Geometry Beyond Search: Amortizing Planning in World Models
- Locator: Appendix B Theoretical Analysis: Isotropy and Inverse-Dynamics Conditioning
- Evidence: 理论附录开头明确将分析标为 conditional，并把假设验证与 non-isotropic 对照列为未完成。
- Authors: hoang-nguyen; xiaohao-xu; xiaonan-huang

### EA-LEWM-READ-0049

- Claim: PushT go50 的 true hybrid cost 在论文权重 sweep 中达到 52.7% 平均成功率，高于 raw latent 的 40.0% 和最佳 shuffled hybrid 的 42.7%，但该提升被作者定位为连续接触任务中的边界结果。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.22164](https://arxiv.org/abs/2605.22164) Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics
- Locator: C.6 PushT Details
- Evidence: 附录 C.6 表 19 给出 go50 的 weight sweep；正文 6.4 明确指出 SCSA 排序和 selected distance 的证据比闭环成功更清楚。
- Authors: liangyu-li; shengzhi-wang; qingwen-liu

### EA-LEWM-READ-0010

- Claim: On Two-Room with the same CEM budget and one NVIDIA 4090, one prefix-model call reduced dynamics time from 31.4s to 8.0s, but unchanged encoding/scoring/data overhead limited the full CEM solve reduction from 54.4s to 28.3s.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26217](https://arxiv.org/abs/2606.26217) Fast LeWorldModel
- Locator: 4.2 Planning Performance and Efficiency, Table 2
- Evidence: Table 2 报告相同 CEM budget、GPU、model calls、dynamics time 与 full solve time；正文说明 full CEM 还含图像编码、评分和数据操作。
- Authors: yuntian-gao; xiangyu-xu

### EA-LEWM-READ-0013

- Claim: The quality-speed gain depends on structured prefixes and intermediate supervision: simply enlarging LeWM's action block performed poorly, terminal-only Fast-LeWM remained below the dense-prefix model, and conditioning the prefix encoder on the current-state token improved results.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26217](https://arxiv.org/abs/2606.26217) Fast LeWorldModel
- Locator: 4.5 Ablation Studies
- Evidence: 4.5 的三组消融分别否定 naive long-action、terminal-only 和无 state token 的简化方案。
- Authors: yuntian-gao; xiangyu-xu

### EA-LEWM-READ-0069

- Claim: Inverse-dynamics retention of the exogenous feature depends on the behavior policy: random actions provide no anchor, whereas an informative policy can retain it only because actions correlate with the feature.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30068](https://arxiv.org/abs/2606.30068) Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study
- Locator: 3.3 Objectives
- Evidence: Objectives section 明确区分 random-policy failure 与 informative-policy rescue，并把后者归为 action supervision。
- Authors: ayan-pendharkar

### EA-LEWM-READ-0071

- Claim: The trained JEPA latent realized substantially less class separation for the exogenous reward-relevant feature than reconstruction and supervised references, but the authors characterize this as a single-seed controlled measurement rather than a theorem or large-model result.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.30068](https://arxiv.org/abs/2606.30068) Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study
- Locator: 5 Empirical Comparison with Bisimulation Predictions
- Evidence: Section 5 把 analytical reward-sensitive state distinction与实际 latent separation 对比，并明示 single seed、finite budget、large pretrained generality open。
- Authors: ayan-pendharkar

### EA-LEWM-READ-0065

- Claim: LDAD is load-bearing but requires balance: removing or weakening its action-reconstruction term yields near-collapse or poor Push-T planning, while an excessively large weight also degrades performance.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.31232](https://arxiv.org/abs/2606.31232) Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding
- Locator: Action Reconstruction Weight.
- Evidence: Push-T weight sweep 同时显示 zero/weak signal 失败、合理区间稳定和 excessive weight 退化。
- Authors: zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al.

### EA-LEWM-READ-0053

- Claim: Support-constrained high-level search 的收益取决于执行模式和时间尺度：staged execution 在中等时域最有帮助，但在最长 PushT 时域低于 online constrained replanning。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.12547](https://arxiv.org/abs/2607.12547) Mind the Gap: Promises and Pitfalls of Hierarchical Planning in LeWorldModel
- Locator: 3.3 Planning-Side Mitigations
- Evidence: 3.3 节在同一 PushT sweep 中比较 online 与 staged，并明确把最长时域的 staged 退化解释为方法自然边界。
- Authors: niccol-caselli; francesco-massafra; samuele-punzo; et al.

### EA-LEWM-READ-0085

- Claim: V-JEPA 2-AC 的已验证规划时域约为 16 秒；简单 grasp 和 reach-with-object 可用单一目标图像，但更长程 pick-and-place 若不提供子目标仍需新的建模方法。
- Stance: `limit` | Confidence: `direct`
- Paper: [2506.09985](https://arxiv.org/abs/2506.09985) V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning
- Locator: 9 Conclusion
- Evidence: 结论把约 16 秒预测、单目标简单操作和无子目标长时程任务明确分开。
- Authors: mahmoud-assran; adrien-bardes; david-fan; et al.

### EA-LEWM-READ-0086

- Claim: 未做显式相机标定时，V-JEPA 2-AC 必须从单目图像隐式推断笛卡尔动作坐标轴；机器人基座不可见会导致欠定和预测错误，作者实际人工尝试多个相机位置后才固定配置。
- Stance: `limit` | Confidence: `direct`
- Paper: [2506.09985](https://arxiv.org/abs/2506.09985) V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning
- Locator: 4.3 Limitations
- Evidence: 限制章节把相机坐标轴推断、基座不可见和人工选位连成明确的部署失败机制。
- Authors: mahmoud-assran; adrien-bardes; david-fan; et al.

### EA-LEWM-READ-0030

- Claim: The practical minibatch SIGReg gradient is biased; the authors report the bias as small in their experiments but do not explore unbiased U-statistic or sample-splitting alternatives.
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.08544](https://arxiv.org/abs/2511.08544) LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics
- Locator: 5.1 LeJEPA: SIGReg + Prediction Loss
- Evidence: Section 5.1 明确承认 minibatch-induced bias、经验上影响小，以及未探索两类无偏替代。
- Authors: randall-balestriero; yann-lecun

### EA-LEWM-READ-0031

- Claim: LeJEPA's empirical validation does not directly test action-conditioned dynamics, world-model rollouts, planning, or closed-loop control; using SIGReg in LeWorldModel is therefore a downstream mechanism transfer rather than direct control evidence from LeJEPA.
- Stance: `limit` | Confidence: `inference`
- Paper: [2511.08544](https://arxiv.org/abs/2511.08544) LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics
- Locator: 6 LeJEPA: Empirical Validation
- Evidence: 经验章节的完整任务清单只包括跨架构/数据稳定性、loss correlation、视觉 in-domain transfer、scaling 和语义分割；六遍结构图未发现动作条件 dynamics 或控制评测。
- Authors: randall-balestriero; yann-lecun

### EA-LEWM-READ-0006

- Claim: LeWM underperformed on the simple Two-Room environment; the authors hypothesize that low data diversity and low intrinsic dimensionality conflict with matching a high-dimensional isotropic Gaussian prior, making this a potential SIGReg failure condition rather than a universal causal conclusion.
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.19312](https://arxiv.org/abs/2603.19312) LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
- Locator: 4.2 Towards Efficient Planning with WMs
- Evidence: 正文直接报告 Two-Room 更差，并用 possible explanation/potential limitation 表明几何归因仍是假设。
- Authors: lucas-maes; quentin-le-lidec; damien-scieur; et al.

### EA-LEWM-READ-0007

- Claim: The authors explicitly bound LeWM to short-horizon planning and sufficiently covering offline action-labeled datasets; low diversity weakens SIGReg, and removing the need for action labels remains future work.
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.19312](https://arxiv.org/abs/2603.19312) LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
- Locator: 6 Conclusion
- Evidence: 结论限制段同时列出 short horizons、offline coverage、low diversity 和 action-label dependence。
- Authors: lucas-maes; quentin-le-lidec; damien-scieur; et al.

### EA-LEWM-READ-0093

- Claim: 该研究的结论局限于 Bridge V2 和共享机器人本体；策略内环只评估固定 VLA 在生成 rollout 中的表现，且部分成功判断依赖 VLM，尚未验证策略改进、sim-to-real 或更广本体。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.06388](https://arxiv.org/abs/2605.06388) Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models
- Locator: 7 Future Work and Limitations
- Evidence: 限制章节连续列出数据与本体范围、固定策略代理和 VLM 评估偏差。
- Authors: nilaksh; saurav-jha; artem-zholus; et al.

### EA-LEWM-READ-0045

- Claim: RC-aux 的当前可达性监督仍以轨迹派生标签代理真实环境可达性，测试时也只采用简单可达性门控，因此尚未解决未观察捷径、不确定性和完整可行性决策。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.07278](https://arxiv.org/abs/2605.07278) Predictive but Not Plannable: RC-aux for Latent World Models
- Locator: 5 Conclusion
- Evidence: 结论明确列出轨迹代理和简单门控两项当前限制，并把不确定性感知可达性列为后续方向。
- Authors: wenyuan-li; guang-li; keisuke-maeda; et al.

### EA-LEWM-READ-0024

- Claim: For Push-T, GC-IDM success peaked at 93.0% with a 25-step evaluation budget and declined to 75.0% at 100 steps, which the authors associate with clamped horizon inputs outside the training-time range.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.08732](https://arxiv.org/abs/2605.08732) Latent Geometry Beyond Search: Amortizing Planning in World Models
- Locator: E.7 Evaluation Budget and Long-Horizon Control
- Evidence: Table J 的预算扫描提供 Push-T 的完整序列，正文将长预算退化与未在训练中出现的 clamped horizon signal 联系起来。
- Authors: hoang-nguyen; xiaohao-xu; xiaonan-huang

### EA-LEWM-READ-0025

- Claim: The evaluation is confined mainly to one LeWM backbone and the stable-worldmodel suite, and GC-IDM does not reason about multi-step consequences; cross-world-model transfer and severely irreversible tasks therefore remain open.
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.08732](https://arxiv.org/abs/2605.08732) Latent Geometry Beyond Search: Amortizing Planning in World Models
- Locator: Appendix G More Limitations and Future Works
- Evidence: 限制附录直接列出单 backbone、跨模型架构修改和 reactive-policy 无多步后果推理，并把 hybrid GC-IDM+CEM 留作未来方向。
- Authors: hoang-nguyen; xiaohao-xu; xiaonan-huang

### EA-LEWM-READ-0050

- Claim: TRM 的时间度量依赖轨迹覆盖，且同 episode 时间标签只是对称标量可达性代理，不是有向或预算条件的目标可达性值。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.22164](https://arxiv.org/abs/2605.22164) Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics
- Locator: 8 Limitations
- Evidence: 限制节同时指出低覆盖/短时域显著退化，以及标签在方向性和预算条件上的结构缺失。
- Authors: liangyu-li; shengzhi-wang; qingwen-liu

### EA-LEWM-READ-0012

- Claim: Fast-LeWM removes sequential dependence only within one maximum encoded prefix window; the paper's longer open-loop evaluation already requires composing two maximum-horizon predictions, so long-range recurrence is reduced rather than eliminated.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.26217](https://arxiv.org/abs/2606.26217) Fast LeWorldModel
- Locator: 4.3 Open-Loop Latent Prediction
- Evidence: 4.3 明确区分一个 maximum-horizon prediction 与需要两次该预测的更远时间点。
- Authors: yuntian-gao; xiangyu-xu

### EA-LEWM-READ-0067

- Claim: A reward-relevant feature can be temporally unpredictable, in which case a latent self-prediction objective receives no signal to retain information that a controller still needs.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30068](https://arxiv.org/abs/2606.30068) Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study
- Locator: 1 Introduction
- Evidence: 引言把 feature 的不可预测性与 payoff relevance 分离，并明确预测目标会把它视为 noise。
- Authors: ayan-pendharkar

### EA-LEWM-READ-0068

- Claim: Across both controlled environments, every evaluated reward-free predictive variant left the exogenous control-relevant feature near chance, while the reward-grounded variant recovered it at the one-bit ceiling alongside reconstruction and supervised references.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30068](https://arxiv.org/abs/2606.30068) Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study
- Locator: 4.1 Reward-free predictive objectives do not retain the exogenous control-relevant feature
- Evidence: 主结果段按两环境和三 seeds 汇总 near-chance predictive variants 与 ceiling reward-grounded/reference outcomes。
- Authors: ayan-pendharkar

### EA-LEWM-READ-0070

- Claim: Increasing latent capacity did not rescue cell-4 retention for JEPA, while the reward-grounded variant remained high across the sweep, supporting an objective-structural rather than capacity explanation.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30068](https://arxiv.org/abs/2606.30068) Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study
- Locator: 4.3 The failure is not a capacity problem
- Evidence: capacity sweep 显示 JEPA 始终不过 retain threshold，reward-grounded variant 跨容量保持近完美。
- Authors: ayan-pendharkar

### EA-LEWM-READ-0072

- Claim: The study establishes an objective-level failure mode only in small synthetic environments; it does not test large pretrained models, robotics, standard RL benchmarks, real data, or how often the failure occurs naturally.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30068](https://arxiv.org/abs/2606.30068) Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study
- Locator: 6.7 Limitations
- Evidence: Limitations section 明确列出 synthetic-only、无大模型/机器人/Atari/真实数据和非 benchmark/频率结论。
- Authors: ayan-pendharkar

### EA-LEWM-READ-0066

- Claim: Delta-JEPA does not establish that action-sensitive latents are sufficient for task control: its offline training data contain no rewards, and its two losses supervise only latent prediction and executed-action reconstruction.
- Stance: `limit` | Confidence: `inference`
- Paper: [2606.31232](https://arxiv.org/abs/2606.31232) Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding
- Locator: Problem Formulation
- Evidence: Problem formulation 明示 reward-free/unknown-policy data；完整 method map 显示总目标仅 prediction + action reconstruction，未测试 exogenous reward-relevant feature retention。
- Authors: zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al.

### EA-LEWM-READ-0051

- Claim: 在冻结低层 LeWM 的 Hi-LeWM 中，简单增加时间抽象层并不足以改善长时程控制；数据轨迹上的 oracle 中间 subgoal 通常可执行，而生成 subgoal 更不可靠、时间错位并对高层搜索空间敏感。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.12547](https://arxiv.org/abs/2607.12547) Mind the Gap: Promises and Pitfalls of Hierarchical Planning in LeWorldModel
- Locator: 1 Introduction
- Evidence: 引言综合了 acting decomposition 的结论，并明确 naive hierarchy 经常低于 flat LeWM。
- Authors: niccol-caselli; francesco-massafra; samuele-punzo; et al.

### EA-LEWM-READ-0054

- Claim: Hi-LeWM 的正面结论不能外推为 hierarchy 的一般优势：主分析集中于 PushT，VQ macro-actions 尚未充分评估，而且更高容量世界模型可能呈现不同结果。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.12547](https://arxiv.org/abs/2607.12547) Mind the Gap: Promises and Pitfalls of Hierarchical Planning in LeWorldModel
- Locator: 4 Discussion and Conclusion
- Evidence: 讨论节逐项说明环境范围、未充分探索的 VQ 路线和模型规模条件。
- Authors: niccol-caselli; francesco-massafra; samuele-punzo; et al.

## References

- `2506.09985` [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/abs/2506.09985) (2025-06-11)
- `2511.08544` [LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics](https://arxiv.org/abs/2511.08544) (2025-11-11)
- `2601.09708` [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](https://arxiv.org/abs/2601.09708) (2026-01-14)
- `2602.06949` [DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos](https://arxiv.org/abs/2602.06949) (2026-02-06)
- `2603.08546` [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546) (2026-03-09)
- `2603.19312` [LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels](https://arxiv.org/abs/2603.19312) (2026-03-13)
- `2605.00080` [World Model for Robot Learning: A Comprehensive Survey](https://arxiv.org/abs/2605.00080) (2026-04-30)
- `2605.06388` [Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models](https://arxiv.org/abs/2605.06388) (2026-05-07T15:05:26Z)
- `2605.07278` [Predictive but Not Plannable: RC-aux for Latent World Models](https://arxiv.org/abs/2605.07278) (2026-05-08T05:43:33Z)
- `2605.08732` [Latent Geometry Beyond Search: Amortizing Planning in World Models](https://arxiv.org/abs/2605.08732) (2026-05-09)
- `2605.20752` [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](https://arxiv.org/abs/2605.20752) (2026-05-20)
- `2605.22164` [Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics](https://arxiv.org/abs/2605.22164) (2026-05-21T08:34:57Z)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.29360` [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360) (2026-05-28)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.12403` [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403) (2026-06-10)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
- `2606.13877` [ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13877) (2026-06-11)
- `2606.14981` [Inference-time Policy Steering via Vision and Touch](https://arxiv.org/abs/2606.14981) (2026-06-12)
- `2606.26217` [Fast LeWorldModel](https://arxiv.org/abs/2606.26217) (2026-06-24)
- `2606.30068` [Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study](https://arxiv.org/abs/2606.30068) (2026-06-29)
- `2606.31232` [Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding](https://arxiv.org/abs/2606.31232) (2026-06-30)
- `2607.12547` [Mind the Gap: Promises and Pitfalls of Hierarchical Planning in LeWorldModel](https://arxiv.org/abs/2607.12547) (2026-07-14T09:18:44Z)
