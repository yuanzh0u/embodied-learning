# Review Packet: LeWorldModel 技术谱系：JEPA 潜空间世界模型到规划控制

## Scope

- Topic: LeWorldModel 技术谱系：JEPA 潜空间世界模型到规划控制
- Time range: 2026-01-24..2026-07-24
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-4D`
- Evidence events: 76
- Topic cards: 3
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 76
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`, `inference`
- Trace IDs: `EA-JIMFAN-READ-0015`, `EA-WMDATA-READ-0007`, `EA-WMDATA-READ-0008`, `EA-TWM-READ-0003`, `EA-TWM-READ-0004`, `EA-WMEVAL-READ-0005`, `EA-WMEVAL-READ-0003`, `EA-WMEVAL-READ-0001`, `EA-WMEVAL-READ-0010`, `EA-WMEVAL-READ-0013`, `EA-WMEVAL-READ-0004`, `EA-LEWM-READ-0081`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 24 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 24
- Structure mapped: 24
- Deep-read papers: 24
- Claim-verified papers: 24
- Accepted evidence papers: 24
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。VLA 可以继承视觉和语言先验，却不会自动继承运动、接触和控制器先验；语言—视觉—动作接口需要显式对齐。4D 和世界模型可以提供几何动态监督、未来想象和动作筛选，但训练目标必须面向动作质量而非只追求视觉重建。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测应分开记录预测保真与决策有效，防止“视频更真实”掩盖错误动作响应。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- `EA-4D` 4D 时空推理与世界动态: 具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。
  - 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
  - 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
  - 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
  - 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
  - 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 36 |
| `conditional` | 条件成立 | 19 |
| `limit` | 限制/负面 | 20 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2506.09985: V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning | 2025-06-11 | conditional, limit, support | EA-LEWM-READ-0081; EA-LEWM-READ-0082; EA-LEWM-READ-0083; EA-LEWM-READ-0084; EA-LEWM-READ-0085; EA-LEWM-READ-0086 |
| 2511.08544: LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics | 2025-11-11 | conditional, limit, support | EA-LEWM-READ-0026; EA-LEWM-READ-0027; EA-LEWM-READ-0028; EA-LEWM-READ-0029; EA-LEWM-READ-0030; EA-LEWM-READ-0031 |
| 2601.09708: Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning | 2026-01-14 | support | EA-ALIGN-READ-0013 |
| 2602.06949: DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos | 2026-02-06 | conditional | EA-JIMFAN-READ-0015 |
| 2603.08546: Interactive World Simulator for Robot Policy Training and Evaluation | 2026-03-09 | support | EA-WMDATA-READ-0007 |
| 2603.19312: LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels | 2026-03-13 | conditional, limit, support | EA-LEWM-READ-0001; EA-LEWM-READ-0002; EA-LEWM-READ-0003; EA-LEWM-READ-0004; EA-LEWM-READ-0005; EA-LEWM-READ-0006; EA-LEWM-READ-0007 |
| 2605.00080: World Model for Robot Learning: A Comprehensive Survey | 2026-04-30 | support | EA-ALIGN-READ-0014 |
| 2605.06388: Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models | 2026-05-07T15:05:26Z | conditional, limit, support | EA-LEWM-READ-0087; EA-LEWM-READ-0088; EA-LEWM-READ-0089; EA-LEWM-READ-0090; EA-LEWM-READ-0091; EA-LEWM-READ-0092; EA-LEWM-READ-0093 |
| 2605.07278: Predictive but Not Plannable: RC-aux for Latent World Models | 2026-05-08T05:43:33Z | conditional, limit, support | EA-LEWM-READ-0041; EA-LEWM-READ-0042; EA-LEWM-READ-0043; EA-LEWM-READ-0044; EA-LEWM-READ-0045 |
| 2605.08732: Latent Geometry Beyond Search: Amortizing Planning in World Models | 2026-05-09 | conditional, limit, support | EA-LEWM-READ-0021; EA-LEWM-READ-0022; EA-LEWM-READ-0023; EA-LEWM-READ-0024; EA-LEWM-READ-0025 |
| 2605.20752: GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation | 2026-05-20 | support | EA-WMDATA-READ-0008 |
| 2605.22164: Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics | 2026-05-21T08:34:57Z | conditional, limit, support | EA-LEWM-READ-0046; EA-LEWM-READ-0047; EA-LEWM-READ-0048; EA-LEWM-READ-0049; EA-LEWM-READ-0050 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | support | EA-WMEVAL-READ-0005 |
| 2605.29360: MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models | 2026-05-28 | gap | EA-WMEVAL-READ-0004 |
| 2606.00664: SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models | 2026-05-30 | support | EA-WMEVAL-READ-0003 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | support | EA-WMEVAL-READ-0001 |
| 2606.12403: World Pilot: Steering Vision-Language-Action Models with World-Action Priors | 2026-06-10 | limit | EA-WMEVAL-READ-0013 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | support | EA-WMEVAL-READ-0010 |
| 2606.13877: ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation | 2026-06-11 | support | EA-TWM-READ-0003 |
| 2606.14981: Inference-time Policy Steering via Vision and Touch | 2026-06-12 | support | EA-TWM-READ-0004 |
| 2606.26217: Fast LeWorldModel | 2026-06-24 | conditional, limit, support | EA-LEWM-READ-0008; EA-LEWM-READ-0009; EA-LEWM-READ-0010; EA-LEWM-READ-0011; EA-LEWM-READ-0012; EA-LEWM-READ-0013 |
| 2606.30068: Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study | 2026-06-29 | conditional, limit | EA-LEWM-READ-0067; EA-LEWM-READ-0068; EA-LEWM-READ-0069; EA-LEWM-READ-0070; EA-LEWM-READ-0071; EA-LEWM-READ-0072 |
| 2606.31232: Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding | 2026-06-30 | conditional, limit, support | EA-LEWM-READ-0061; EA-LEWM-READ-0062; EA-LEWM-READ-0063; EA-LEWM-READ-0064; EA-LEWM-READ-0065; EA-LEWM-READ-0066 |
| 2607.12547: Mind the Gap: Promises and Pitfalls of Hierarchical Planning in LeWorldModel | 2026-07-14T09:18:44Z | conditional, limit, support | EA-LEWM-READ-0051; EA-LEWM-READ-0052; EA-LEWM-READ-0053; EA-LEWM-READ-0054 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-JIMFAN-READ-0015 | EA-4D | `conditional` | `direct` | DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and planning benefits after... | Its policy-evaluation correlation is measured on 20 fruit-packing scenes; the paper also acknowledges optimistic simulation and coverage limitations. (4.7 Downstream Applications) | shenyuan-gao; william-liang; kaiyuan-zheng; et al. | 2602.06949 |
| EA-WMDATA-READ-0007 | EA-DATA | `support` | `direct` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-c... | The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real perform... | yixuan-wang; rhythm-syed; fangyu-wu; et al. | 2603.08546 |
| EA-WMDATA-READ-0008 | EA-DATA | `support` | `direct` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and... | GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference. (3.... | zijian-zhang; yuqing-jiang; qian-cheng; et al. | 2605.20752 |
| EA-TWM-READ-0003 | EA-DATA | `support` | `direct` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 | ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。 (Abstract (full-text section)) | zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al. | 2606.13877 |
| EA-TWM-READ-0004 | EA-DATA | `support` | `direct` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 | ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。 (5 Experiments) | yilin-wu; zilin-si; zeynep-temel; et al. | 2606.14981 |
| EA-WMEVAL-READ-0005 | EA-EVAL | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | 2605.22882 |
| EA-WMEVAL-READ-0003 | EA-EVAL | `support` | `direct` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remov... | SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as pol... | ziheng-he; yixiang-chen; ning-yang; et al. | 2606.00664 |
| EA-WMEVAL-READ-0001 | EA-EVAL | `support` | `direct` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 | 摘要直接报告了异构数据组成与 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-WMEVAL-READ-0010 | EA-EVAL | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | 2606.13672 |
| EA-WMEVAL-READ-0013 | EA-EVAL | `limit` | `direct` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. | World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy. (Abstract... | zefu-lin; rongxu-cui; junjia-xu; et al. | 2606.12403 |
| EA-WMEVAL-READ-0004 | EA-EVAL | `gap` | `direct` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias... | The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias. (Abstract... | tianzhuo-yang; zihan-shen; zirui-mi; et al. | 2605.29360 |
| EA-LEWM-READ-0081 | EA-MODEL | `support` | `direct` | V-JEPA 2 的无动作视频预训练预测不直接包含机器人动作的因果效应；论文是在冻结视频编码器上另行训练帧因果、动作条件预测器，才把表征接到规划。 | 方法章节明确说明预训练后的缺失视频预测不考虑智能体动作因果，并把小规模交互数据后训练定义为使模型可用于规划的下一阶段。 (3 V-JEPA 2-AC: Learning an Action-Conditioned World Model) | mahmoud-assran; adrien-bardes; david-fan; et al. | 2506.09985 |
| EA-LEWM-READ-0082 | EA-MODEL | `support` | `direct` | V-JEPA 2 的表征目标是预测场景中可预测的方面，而不是复原生成目标强调的所有像素级不可预测细节。 | 引言把 JEPA 的可预测表征目标与像素生成目标并列，并用运动轨迹和草叶细节说明选择性。 (1 Introduction) | mahmoud-assran; adrien-bardes; david-fan; et al. | 2506.09985 |
| EA-LEWM-READ-0084 | EA-MODEL | `support` | `direct` | 在论文展示的三个单目标 reaching 实例中，V-JEPA 2-AC 把末端移动到距目标不足 4 cm，并选择使误差单调下降的动作。 | 结果章节用末端目标距离报告三个单目标 reaching 执行，并同时观察到误差单调下降。 (4.2 Results) | mahmoud-assran; adrien-bardes; david-fan; et al. | 2506.09985 |
| EA-LEWM-READ-0026 | EA-MODEL | `support` | `direct` | LeJEPA selects an Epps–Pulley empirical-characteristic-function regularizer because the implementation is DDP-friendly, has uniformly bounded gradients and curvature, and has line... | Section 4.2.3 明确比较统计检验家族后列出 Epps–Pulley 的 distributed、bounded 与 linear-complexity 性质。 (4.2.3 Characteristic Functions are Stable, Scalable and Identifiable) | randall-balestriero; yann-lecun | 2511.08544 |
| EA-LEWM-READ-0027 | EA-MODEL | `support` | `direct` | The LeJEPA objective combines the multi-view prediction loss with SIGReg and removes prototypes, stop-gradients, and teacher–student networks, leaving one coefficient to trade pre... | Section 5.1 给出最终组合损失并明确列出不再需要的 collapse-prevention 组件和 mixing coefficient 的含义。 (5.1 LeJEPA: SIGReg + Prediction Loss) | randall-balestriero; yann-lecun | 2511.08544 |
| EA-LEWM-READ-0029 | EA-MODEL | `support` | `direct` | On ImageNet-10, LeJEPA pretrained approximately 50 architectures from eight families with fewer than 20 million parameters, and all reached 91.5%–95% top-1 accuracy under frozen-b... | Section 6.1 直接给出模型数量、架构族、参数上限和 frozen linear-probe top-1 区间。 (6.1 LeJEPA’s Stability Across Hyper-Parameters and Architectures) | randall-balestriero; yann-lecun | 2511.08544 |
| EA-ALIGN-READ-0013 | EA-MODEL | `support` | `direct` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 | 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。 (5 Conclusion) | chi-pin-huang; yunze-man; zhiding-yu; et al. | 2601.09708 |
| EA-LEWM-READ-0001 | EA-MODEL | `support` | `direct` | LeWorldModel jointly trains a pixel encoder and an action-conditioned latent predictor; actions enter the predictor through AdaLN at every layer, and the predictor autoregressivel... | 方法段明确描述 encoder、predictor、AdaLN 动作注入、causal autoregression，并说明所有组件联合学习。 (3 Method: LeWorldModel) | lucas-maes; quentin-le-lidec; damien-scieur; et al. | 2603.19312 |
| EA-LEWM-READ-0002 | EA-MODEL | `support` | `direct` | SIGReg regularizes LeWM latents toward an isotropic Gaussian by projecting them onto random unit directions and matching each one-dimensional projection with an Epps–Pulley normal... | SIGReg 附录明确给出随机方向、一维 Epps–Pulley 匹配、Cramér–Wold 连接及其渐近限定。 (Appendix A SIGReg) | lucas-maes; quentin-le-lidec; damien-scieur; et al. | 2603.19312 |
| EA-LEWM-READ-0004 | EA-MODEL | `support` | `direct` | In the paper's simulated benchmark setup, LeWM achieved an 18% higher Push-T success rate than PLDM, while the fixed planning configuration completed a full plan in under one seco... | 4.2 同时报告 Push-T 相对 PLDM 的成功率差、低于一秒的完整规划，以及 Two-Room 反例。 (4.2 Towards Efficient Planning with WMs, Figure 3 and Figure 6) | lucas-maes; quentin-le-lidec; damien-scieur; et al. | 2603.19312 |
| EA-LEWM-READ-0005 | EA-MODEL | `support` | `direct` | The paper's direct cross-seed stability check is narrow: on Push-T, across three training seeds evaluated on the same 50 trajectories, PLDM exhibited higher success-rate variance... | Appendix G Table 5 报告三 seed、同一 50 条 Push-T 轨迹的 success rate 与方差，并明确 PLDM 方差更高。 (Appendix G Ablations., Table 5) | lucas-maes; quentin-le-lidec; damien-scieur; et al. | 2603.19312 |
| EA-ALIGN-READ-0014 | EA-MODEL | `support` | `direct` | 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 | 引言直接将纯反应 VLA 的三类困难列为长时程推理、temporal credit assignment 与 compounding errors。 (1 Introduction) | bohan-hou; gen-li; jindou-jia; et al. | 2605.00080 |
| EA-LEWM-READ-0087 | EA-MODEL | `support` | `direct` | 该研究固定数据、历史长度、动作条件、转移架构、优化器和训练日程，仅改变冻结编码器、可选适配器与解码路径，从而把编码器定义的潜接口作为主要实验变量。 | 训练协议章节逐项列出固定量和变化量，并为每个编码器—适配器组合从头训练 LDM。 (3.1 Dataset and Training) | nilaksh; saurav-jha; artem-zholus; et al. | 2605.06388 |
| EA-LEWM-READ-0041 | EA-MODEL | `support` | `direct` | RC-aux 通过多时域开放环预测修正时间错配，并以预算条件、方向敏感的轨迹可达性监督修正空间几何；测试时还可按剩余预算把可达性作为显式搜索信号。 | 引言明确把 RC-aux 分成时间与空间两条监督轴，并说明测试时规划器如何使用可达性信号。 (1 Introduction) | wenyuan-li; guang-li; keisuke-maeda; et al. | 2605.07278 |
| EA-LEWM-READ-0042 | EA-MODEL | `support` | `direct` | 在论文的五个匹配 LeWM-family 比较中，RC-aux 改善四项；Wall 成功率从 50.4±6.5 提升到 83.6±3.6，即提高 33.2 个百分点。 | 表 1 同时给出 LeWM、RC-aux 和 matched delta，正文说明 Wall 是最大增益且该任务没有 continuation checkpoint。 (4.2 Main Results) | wenyuan-li; guang-li; keisuke-maeda; et al. | 2605.07278 |
| EA-LEWM-READ-0021 | EA-MODEL | `support` | `direct` | GC-IDM freezes the LeWorldModel representation and amortizes planning into a horizon-conditioned inverse map from current and goal latents to the next action; at test time it re-e... | 方法图和正文明确给出冻结 LeWM embeddings、随机 horizon 训练元组、只更新 inverse module，以及逐步重编码/单次前向的推理路径。 (4 Method: Goal-Conditioned Inverse Dynamics Model (GC-IDM)) | hoang-nguyen; xiaohao-xu; xiaonan-huang | 2605.08732 |
| EA-LEWM-READ-0022 | EA-MODEL | `support` | `direct` | On the eight environment–protocol cells in the main LeWM benchmark comparison, GC-IDM matched or outperformed CEM in seven, with Push-T as the lone exception. | 主结果按 environment–protocol cell 汇总，明确报告 seven of eight，并指出 Push-T 是唯一例外。 (5.3 Main Results) | hoang-nguyen; xiaohao-xu; xiaonan-huang | 2605.08732 |
| EA-LEWM-READ-0046 | EA-MODEL | `support` | `direct` | 在固定 hard n100 TwoRoom 协议中，只替换终端 selector 的 full-horizon TRM 将 LeWM 平均成功率从 7.0% 提升到 97.0%，将本地 PLDM 从 32.7% 提升到 84.0%；同架构 shuffled-label heads 在两类模型上均为 0.0%。 | 6.1 节声明所有 checkpoint、cache、manifest、CEM 与候选采样保持不变，并在表 1 中报告真实时间标签与 shuffled control。 (6.1 TRM Repairs Hard TwoRoom in Fixed Terminal Selection) | liangyu-li; shengzhi-wang; qingwen-liu | 2605.22164 |
| EA-LEWM-READ-0047 | EA-MODEL | `support` | `direct` | 在 LeWM seed 3072 的 matched-b50 消融中，平衡满 episode TRM 使用 100,000 pairs 达到 97.5% 成功率，而相同 pair 预算的平衡短时域 max 版本仅 35.0%。 | 6.2 节与附录 C.5 在相同 pair 预算下比较 full-episode 和 max-horizon，并把 horizon matching 识别为最强因素。 (6.2 Horizon Matching and Temporal Structure Matter) | liangyu-li; shengzhi-wang; qingwen-liu | 2605.22164 |
| EA-LEWM-READ-0048 | EA-MODEL | `support` | `direct` | 在 matched-b50 TwoRoom 中，XY probe rowspace 只贡献 0.5–0.7% 的终端—目标潜 MSE，却使 rowspace-only planning 达到 90.8% 平均成功率；raw latent MSE 和 residual-only 均为 1.7%。 | 6.3 节的 rowspace surgery 直接保留或移除 XY probe 子空间，且规划时不使用真实 simulator state。 (6.3 Mechanism: Raw Latent MSE Hides the Useful State) | liangyu-li; shengzhi-wang; qingwen-liu | 2605.22164 |
| EA-LEWM-READ-0008 | EA-MODEL | `support` | `direct` | Fast-LeWM replaces LeWM's within-window autoregressive latent chain with action-prefix prediction: every future latent is predicted directly from the same observed anchor latent a... | 3.3 明确给出 anchor latent、prefix token、dense horizon targets 与并行预测，并说明 future predictions 不再顺序依赖彼此。 (3.3 Fast LeWorldModel) | yuntian-gao; xiangyu-xu | 2606.26217 |
| EA-LEWM-READ-0009 | EA-MODEL | `support` | `direct` | Under the same four-task LeWM planning protocol, base Fast-LeWM increased average success from 85.8% to 90.5%, and optional self-consistency increased it to 92.0%; no environment... | Table 1 完整列出四环境和平均成功率，base 与 self-consistency variant 在每列都不低于 LeWM。 (3.7 Planning with Action Prefixes and Self-Consistency) | yuntian-gao; xiangyu-xu | 2606.26217 |
| EA-LEWM-READ-0011 | EA-MODEL | `support` | `direct` | Across all four tasks, Fast-LeWM had lower initial open-loop latent error and a smaller least-squares error-growth slope than LeWM, while qualitative decoded rollouts showed less... | 4.3 以 ground-truth future-frame latents 对齐，比较 loss curve 起点、增长斜率和 decoder rollout。 (4.3 Open-Loop Latent Prediction) | yuntian-gao; xiangyu-xu | 2606.26217 |
| EA-LEWM-READ-0061 | EA-MODEL | `support` | `direct` | LDAD decodes the executed action from the latent displacement alone, so successful recovery requires local transition geometry to encode the action and encourages different action... | 方法段明确将 action decoder 的唯一输入设为 displacement，并解释 action recovery、transition distinguishability 与 planner candidate comparison 的关系。 (Action-Supervised Displacement Mechanism.) | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | 2606.31232 |
| EA-LEWM-READ-0062 | EA-MODEL | `support` | `direct` | Across the four evaluated environments, Delta-JEPA had the highest mean planning success; it exceeded the strongest OGB-Cube baseline by 15.14 percentage points and LeWM on Push-T... | 主结果段给出四环境全部最高及 OGB-Cube、Push-T 的明确百分点差。 (Planning Performance) | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | 2606.31232 |
| EA-LEWM-READ-0063 | EA-MODEL | `support` | `direct` | With the training and planning protocol held fixed, decoding actions from latent displacements improved planning relative to decoding from concatenated endpoint embeddings in ever... | 该消融明确说明两变体只在 action-decoder input 上不同，并报告 displacement variant 跨四环境一致改善。 (Ablation Study > Displacement-Based Action Decoding.) | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | 2606.31232 |
| EA-LEWM-READ-0064 | EA-MODEL | `support` | `direct` | When the starting history is fixed and only the action input is varied, Delta-JEPA produces separated action-wise predictor responses, whereas LeWM's responses remain concentrated... | 作者固定 512 个 Two-Room histories 并逐 action 干预 predictor，比较 action-wise mean displacement。 (Action-Sensitive Latent Dynamics) | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | 2606.31232 |
| EA-LEWM-READ-0052 | EA-MODEL | `support` | `direct` | Empirical-macro CEM 不在连续潜 macro-action 空间中无约束搜索，而从训练轨迹编码的 macro-action 序列 bank 采样 anchor，并只在其附近拟合局部 residual。 | 3.3 节给出方法动机，附录 C.6 进一步说明每轮重采样 anchor、只 refit residual 并保留零残差候选。 (3.3 Planning-Side Mitigations) | niccol-caselli; francesco-massafra; samuele-punzo; et al. | 2607.12547 |
| EA-LEWM-READ-0083 | EA-MODEL | `conditional` | `direct` | V-JEPA 2-AC 与论文基线使用同一套目标实验室协议部署在两座 Droid 未覆盖的实验室，输入为未标定、低分辨率单目 RGB，相同 V-JEPA 2-AC 权重和推理代码跨实验室复用。 | 规划章节明确记录两座新实验室、Franka 平台、未标定单目相机及跨机器人复用权重和推理代码。 (4 Planning: Zero-shot Robot Control) | mahmoud-assran; adrien-bardes; david-fan; et al. | 2506.09985 |
| EA-LEWM-READ-0028 | EA-MODEL | `conditional` | `direct` | The nonlinear-probe optimality result is conditional on a smooth embedding density with finite Fisher information and covariance, test queries drawn from the training distribution... | Appendix A.1 在给出 kNN 唯一最优解前逐项列出 density、query、target function 与 covariance constraints。 (A.1 kNN Probing) | randall-balestriero; yann-lecun | 2511.08544 |
| EA-LEWM-READ-0003 | EA-MODEL | `conditional` | `direct` | LeWM planning is explicitly short-horizon and conditional: longer autoregressive rollouts trade additional lookahead for more compute and model bias, so the controller executes on... | 规划段直接陈述 horizon 的计算/偏差权衡、误差累积和 MPC 重规划缓解机制。 (3.2 Latent Planning) | lucas-maes; quentin-le-lidec; damien-scieur; et al. | 2603.19312 |
| EA-LEWM-READ-0088 | EA-MODEL | `conditional` | `direct` | 在论文的共享 Bridge V2 任务统计中，语义潜空间家族相对重建家族的 VLA 成功率高 9.8 个百分点、OOD 成功率高 13.6 个百分点，并把一步 CEM 动作误差降低 0.0266；三项 95% 配对 bootstrap 区间均不跨零。 | 附录统计以共享任务做家族级配对 bootstrap，同时报告策略成功、OOD 成功和 CEM 动作恢复三个面向控制的指标。 (D.3 Statistical Analyses) | nilaksh; saurav-jha; artem-zholus; et al. | 2605.06388 |
| EA-LEWM-READ-0089 | EA-MODEL | `conditional` | `direct` | 在 DiT-S 的真实编码潜变量上，语义编码器的 IDM Pearson 为 0.772–0.829、轨迹成功分类准确率为 0.903–0.906；重建编码器对应范围为 0.507–0.626 和 0.835–0.868，且动作信息优势大体延续到世界模型生成潜变量。 | 表 2 同时报告真实编码潜变量与生成潜变量的 IDM 和成功分类结果，正文总结语义家族保留更多动作信息。 (4.2 Does the latent space affect action recoverability and preservation of task semantics?) | nilaksh; saurav-jha; artem-zholus; et al. | 2605.06388 |
| EA-LEWM-READ-0090 | EA-MODEL | `conditional` | `direct` | 在该受控实验中，重建对齐潜空间仍能保持较锐利的局部外观，但语义潜空间通常在全局结构和时序生成指标上更强；因此低层像素质量不足以解释策略效用。 | 视觉结果章节同时报告语义模型的结构与视频指标优势和 VAE 类模型的局部外观竞争力。 (4.3 How does the latent space affect visual fidelity?) | nilaksh; saurav-jha; artem-zholus; et al. | 2605.06388 |
| EA-LEWM-READ-0091 | EA-MODEL | `conditional` | `direct` | 论文的质性 rollout 显示两类潜空间会以不同方式失败：重建潜变量可能生成外观连贯但任务语义错误的状态，语义潜变量较能保持任务意图，却可能损失几何和接触精度。 | 失败分析用篮子、毛巾、抽屉和指令变化案例区分任务语义幻觉与几何接触不足。 (4.5 Do reconstruction-aligned and semantic encoders fail differently?) | nilaksh; saurav-jha; artem-zholus; et al. | 2605.06388 |
| EA-LEWM-READ-0092 | EA-MODEL | `conditional` | `direct` | 把高维语义特征压缩到适配器潜空间通常更利于扩散去噪和高层任务完成，但会恶化潜空间 CEM 动作误差、OOD 鲁棒性或点跟踪等精细控制指标。 | 适配器消融把多数指标的改善与 CEM、OOD 和 PCK 的例外并列，并给出压缩损失精细动作信息的解释。 (4.6 Do compressed adapter latents aid semantic encoders further for world modeling?) | nilaksh; saurav-jha; artem-zholus; et al. | 2605.06388 |
| EA-LEWM-READ-0043 | EA-MODEL | `conditional` | `direct` | Wall 消融中，RC-aux 训练后的模型即使仍用基础终端潜距离规划也达到 72.4±3.6%，高于 LeWM-family control 的 50.4±6.5%；加入可达性感知规划后进一步达到 83.6±3.6%。 | 表 2 在相同任务上并列 control、RC-aux-trained/base planner 与完整 RC-aux，能区分两层干预。 (4.2 Main Results) | wenyuan-li; guang-li; keisuke-maeda; et al. | 2605.07278 |
| EA-LEWM-READ-0044 | EA-MODEL | `conditional` | `direct` | 在 LIBERO-Goal 的可训练 no-repeat OFT-style 动作头协议中，RC-aux 表征的平均成功率为 0.812，高于 LeWM 表征的 0.712；repeat tuning 后 RC-aux 为 0.864。 | 表 5 明确区分 matched no-repeat 比较、repeat-tuned 结果和外部 OpenVLA-OFT 参考。 (4.4 Model Size and Computational Overhead, Table 5) | wenyuan-li; guang-li; keisuke-maeda; et al. | 2605.07278 |
| EA-LEWM-READ-0023 | EA-MODEL | `conditional` | `direct` | The paper's explanation that isotropic LeWM geometry makes inverse dynamics well conditioned is explicitly conditional: the authors did not verify that LeWM fully satisfies the st... | 理论附录开头明确将分析标为 conditional，并把假设验证与 non-isotropic 对照列为未完成。 (Appendix B Theoretical Analysis: Isotropy and Inverse-Dynamics Conditioning) | hoang-nguyen; xiaohao-xu; xiaonan-huang | 2605.08732 |
| EA-LEWM-READ-0049 | EA-MODEL | `conditional` | `direct` | PushT go50 的 true hybrid cost 在论文权重 sweep 中达到 52.7% 平均成功率，高于 raw latent 的 40.0% 和最佳 shuffled hybrid 的 42.7%，但该提升被作者定位为连续接触任务中的边界结果。 | 附录 C.6 表 19 给出 go50 的 weight sweep；正文 6.4 明确指出 SCSA 排序和 selected distance 的证据比闭环成功更清楚。 (C.6 PushT Details) | liangyu-li; shengzhi-wang; qingwen-liu | 2605.22164 |
| EA-LEWM-READ-0010 | EA-MODEL | `conditional` | `direct` | On Two-Room with the same CEM budget and one NVIDIA 4090, one prefix-model call reduced dynamics time from 31.4s to 8.0s, but unchanged encoding/scoring/data overhead limited the... | Table 2 报告相同 CEM budget、GPU、model calls、dynamics time 与 full solve time；正文说明 full CEM 还含图像编码、评分和数据操作。 (4.2 Planning Performance and Efficiency, Table 2) | yuntian-gao; xiangyu-xu | 2606.26217 |
| EA-LEWM-READ-0013 | EA-MODEL | `conditional` | `direct` | The quality-speed gain depends on structured prefixes and intermediate supervision: simply enlarging LeWM's action block performed poorly, terminal-only Fast-LeWM remained below t... | 4.5 的三组消融分别否定 naive long-action、terminal-only 和无 state token 的简化方案。 (4.5 Ablation Studies) | yuntian-gao; xiangyu-xu | 2606.26217 |
| EA-LEWM-READ-0069 | EA-MODEL | `conditional` | `direct` | Inverse-dynamics retention of the exogenous feature depends on the behavior policy: random actions provide no anchor, whereas an informative policy can retain it only because acti... | Objectives section 明确区分 random-policy failure 与 informative-policy rescue，并把后者归为 action supervision。 (3.3 Objectives) | ayan-pendharkar | 2606.30068 |
| EA-LEWM-READ-0071 | EA-MODEL | `conditional` | `direct` | The trained JEPA latent realized substantially less class separation for the exogenous reward-relevant feature than reconstruction and supervised references, but the authors chara... | Section 5 把 analytical reward-sensitive state distinction与实际 latent separation 对比，并明示 single seed、finite budget、large pretrained generality open。 (5 Empirical Comparison with Bisimulation Predictions) | ayan-pendharkar | 2606.30068 |
| EA-LEWM-READ-0065 | EA-MODEL | `conditional` | `direct` | LDAD is load-bearing but requires balance: removing or weakening its action-reconstruction term yields near-collapse or poor Push-T planning, while an excessively large weight als... | Push-T weight sweep 同时显示 zero/weak signal 失败、合理区间稳定和 excessive weight 退化。 (Action Reconstruction Weight.) | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | 2606.31232 |
| EA-LEWM-READ-0053 | EA-MODEL | `conditional` | `direct` | Support-constrained high-level search 的收益取决于执行模式和时间尺度：staged execution 在中等时域最有帮助，但在最长 PushT 时域低于 online constrained replanning。 | 3.3 节在同一 PushT sweep 中比较 online 与 staged，并明确把最长时域的 staged 退化解释为方法自然边界。 (3.3 Planning-Side Mitigations) | niccol-caselli; francesco-massafra; samuele-punzo; et al. | 2607.12547 |
| EA-LEWM-READ-0085 | EA-MODEL | `limit` | `direct` | V-JEPA 2-AC 的已验证规划时域约为 16 秒；简单 grasp 和 reach-with-object 可用单一目标图像，但更长程 pick-and-place 若不提供子目标仍需新的建模方法。 | 结论把约 16 秒预测、单目标简单操作和无子目标长时程任务明确分开。 (9 Conclusion) | mahmoud-assran; adrien-bardes; david-fan; et al. | 2506.09985 |
| EA-LEWM-READ-0086 | EA-MODEL | `limit` | `direct` | 未做显式相机标定时，V-JEPA 2-AC 必须从单目图像隐式推断笛卡尔动作坐标轴；机器人基座不可见会导致欠定和预测错误，作者实际人工尝试多个相机位置后才固定配置。 | 限制章节把相机坐标轴推断、基座不可见和人工选位连成明确的部署失败机制。 (4.3 Limitations) | mahmoud-assran; adrien-bardes; david-fan; et al. | 2506.09985 |
| EA-LEWM-READ-0030 | EA-MODEL | `limit` | `direct` | The practical minibatch SIGReg gradient is biased; the authors report the bias as small in their experiments but do not explore unbiased U-statistic or sample-splitting alternativ... | Section 5.1 明确承认 minibatch-induced bias、经验上影响小，以及未探索两类无偏替代。 (5.1 LeJEPA: SIGReg + Prediction Loss) | randall-balestriero; yann-lecun | 2511.08544 |
| EA-LEWM-READ-0031 | EA-MODEL | `limit` | `inference` | LeJEPA's empirical validation does not directly test action-conditioned dynamics, world-model rollouts, planning, or closed-loop control; using SIGReg in LeWorldModel is therefore... | 经验章节的完整任务清单只包括跨架构/数据稳定性、loss correlation、视觉 in-domain transfer、scaling 和语义分割；六遍结构图未发现动作条件 dynamics 或控制评测。 (6 LeJEPA: Empirical Validation) | randall-balestriero; yann-lecun | 2511.08544 |
| EA-LEWM-READ-0006 | EA-MODEL | `limit` | `direct` | LeWM underperformed on the simple Two-Room environment; the authors hypothesize that low data diversity and low intrinsic dimensionality conflict with matching a high-dimensional... | 正文直接报告 Two-Room 更差，并用 possible explanation/potential limitation 表明几何归因仍是假设。 (4.2 Towards Efficient Planning with WMs) | lucas-maes; quentin-le-lidec; damien-scieur; et al. | 2603.19312 |
| EA-LEWM-READ-0007 | EA-MODEL | `limit` | `direct` | The authors explicitly bound LeWM to short-horizon planning and sufficiently covering offline action-labeled datasets; low diversity weakens SIGReg, and removing the need for acti... | 结论限制段同时列出 short horizons、offline coverage、low diversity 和 action-label dependence。 (6 Conclusion) | lucas-maes; quentin-le-lidec; damien-scieur; et al. | 2603.19312 |
| EA-LEWM-READ-0093 | EA-MODEL | `limit` | `direct` | 该研究的结论局限于 Bridge V2 和共享机器人本体；策略内环只评估固定 VLA 在生成 rollout 中的表现，且部分成功判断依赖 VLM，尚未验证策略改进、sim-to-real 或更广本体。 | 限制章节连续列出数据与本体范围、固定策略代理和 VLM 评估偏差。 (7 Future Work and Limitations) | nilaksh; saurav-jha; artem-zholus; et al. | 2605.06388 |
| EA-LEWM-READ-0045 | EA-MODEL | `limit` | `direct` | RC-aux 的当前可达性监督仍以轨迹派生标签代理真实环境可达性，测试时也只采用简单可达性门控，因此尚未解决未观察捷径、不确定性和完整可行性决策。 | 结论明确列出轨迹代理和简单门控两项当前限制，并把不确定性感知可达性列为后续方向。 (5 Conclusion) | wenyuan-li; guang-li; keisuke-maeda; et al. | 2605.07278 |
| EA-LEWM-READ-0024 | EA-MODEL | `limit` | `direct` | For Push-T, GC-IDM success peaked at 93.0% with a 25-step evaluation budget and declined to 75.0% at 100 steps, which the authors associate with clamped horizon inputs outside the... | Table J 的预算扫描提供 Push-T 的完整序列，正文将长预算退化与未在训练中出现的 clamped horizon signal 联系起来。 (E.7 Evaluation Budget and Long-Horizon Control) | hoang-nguyen; xiaohao-xu; xiaonan-huang | 2605.08732 |
| EA-LEWM-READ-0025 | EA-MODEL | `limit` | `direct` | The evaluation is confined mainly to one LeWM backbone and the stable-worldmodel suite, and GC-IDM does not reason about multi-step consequences; cross-world-model transfer and se... | 限制附录直接列出单 backbone、跨模型架构修改和 reactive-policy 无多步后果推理，并把 hybrid GC-IDM+CEM 留作未来方向。 (Appendix G More Limitations and Future Works) | hoang-nguyen; xiaohao-xu; xiaonan-huang | 2605.08732 |
| EA-LEWM-READ-0050 | EA-MODEL | `limit` | `direct` | TRM 的时间度量依赖轨迹覆盖，且同 episode 时间标签只是对称标量可达性代理，不是有向或预算条件的目标可达性值。 | 限制节同时指出低覆盖/短时域显著退化，以及标签在方向性和预算条件上的结构缺失。 (8 Limitations) | liangyu-li; shengzhi-wang; qingwen-liu | 2605.22164 |
| EA-LEWM-READ-0012 | EA-MODEL | `limit` | `direct` | Fast-LeWM removes sequential dependence only within one maximum encoded prefix window; the paper's longer open-loop evaluation already requires composing two maximum-horizon predi... | 4.3 明确区分一个 maximum-horizon prediction 与需要两次该预测的更远时间点。 (4.3 Open-Loop Latent Prediction) | yuntian-gao; xiangyu-xu | 2606.26217 |
| EA-LEWM-READ-0067 | EA-MODEL | `limit` | `direct` | A reward-relevant feature can be temporally unpredictable, in which case a latent self-prediction objective receives no signal to retain information that a controller still needs. | 引言把 feature 的不可预测性与 payoff relevance 分离，并明确预测目标会把它视为 noise。 (1 Introduction) | ayan-pendharkar | 2606.30068 |
| EA-LEWM-READ-0068 | EA-MODEL | `limit` | `direct` | Across both controlled environments, every evaluated reward-free predictive variant left the exogenous control-relevant feature near chance, while the reward-grounded variant reco... | 主结果段按两环境和三 seeds 汇总 near-chance predictive variants 与 ceiling reward-grounded/reference outcomes。 (4.1 Reward-free predictive objectives do not retain the exogenous control-relevant feature) | ayan-pendharkar | 2606.30068 |
| EA-LEWM-READ-0070 | EA-MODEL | `limit` | `direct` | Increasing latent capacity did not rescue cell-4 retention for JEPA, while the reward-grounded variant remained high across the sweep, supporting an objective-structural rather th... | capacity sweep 显示 JEPA 始终不过 retain threshold，reward-grounded variant 跨容量保持近完美。 (4.3 The failure is not a capacity problem) | ayan-pendharkar | 2606.30068 |
| EA-LEWM-READ-0072 | EA-MODEL | `limit` | `direct` | The study establishes an objective-level failure mode only in small synthetic environments; it does not test large pretrained models, robotics, standard RL benchmarks, real data,... | Limitations section 明确列出 synthetic-only、无大模型/机器人/Atari/真实数据和非 benchmark/频率结论。 (6.7 Limitations) | ayan-pendharkar | 2606.30068 |
| EA-LEWM-READ-0066 | EA-MODEL | `limit` | `inference` | Delta-JEPA does not establish that action-sensitive latents are sufficient for task control: its offline training data contain no rewards, and its two losses supervise only latent... | Problem formulation 明示 reward-free/unknown-policy data；完整 method map 显示总目标仅 prediction + action reconstruction，未测试 exogenous reward-relevant feature retention。 (Problem Formulation) | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | 2606.31232 |
| EA-LEWM-READ-0051 | EA-MODEL | `limit` | `direct` | 在冻结低层 LeWM 的 Hi-LeWM 中，简单增加时间抽象层并不足以改善长时程控制；数据轨迹上的 oracle 中间 subgoal 通常可执行，而生成 subgoal 更不可靠、时间错位并对高层搜索空间敏感。 | 引言综合了 acting decomposition 的结论，并明确 naive hierarchy 经常低于 flat LeWM。 (1 Introduction) | niccol-caselli; francesco-massafra; samuele-punzo; et al. | 2607.12547 |
| EA-LEWM-READ-0054 | EA-MODEL | `limit` | `direct` | Hi-LeWM 的正面结论不能外推为 hierarchy 的一般优势：主分析集中于 PushT，VQ macro-actions 尚未充分评估，而且更高容量世界模型可能呈现不同结果。 | 讨论节逐项说明环境范围、未充分探索的 VQ 路线和模型规模条件。 (4 Discussion and Conclusion) | niccol-caselli; francesco-massafra; samuele-punzo; et al. | 2607.12547 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-JIMFAN-READ-0015 | shenyuan-gao; william-liang; kaiyuan-zheng; et al. | unlisted | `conditional` | DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and pla... |
| EA-WMDATA-READ-0007 | yixuan-wang; rhythm-syed; fangyu-wu; et al. | unlisted | `support` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depe... |
| EA-WMDATA-READ-0008 | zijian-zhang; yuqing-jiang; qian-cheng; et al. | unlisted | `support` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent curr... |
| EA-TWM-READ-0003 | zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al. | unlisted | `support` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 |
| EA-TWM-READ-0004 | yilin-wu; zilin-si; zeynep-temel; et al. | unlisted | `support` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 |
| EA-WMEVAL-READ-0005 | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-WMEVAL-READ-0003 | ziheng-he; yixiang-chen; ning-yang; et al. | unlisted | `support` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic fram... |
| EA-WMEVAL-READ-0001 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `support` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 |
| EA-WMEVAL-READ-0010 | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-WMEVAL-READ-0013 | zefu-lin; rongxu-cui; junjia-xu; et al. | unlisted | `limit` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution... |
| EA-WMEVAL-READ-0004 | tianzhuo-yang; zihan-shen; zirui-mi; et al. | unlisted | `gap` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelit... |
| EA-LEWM-READ-0081 | mahmoud-assran; adrien-bardes; david-fan; et al. | unlisted | `support` | V-JEPA 2 的无动作视频预训练预测不直接包含机器人动作的因果效应；论文是在冻结视频编码器上另行训练帧因果、动作条件预测器，才把表征接到规划。 |
| EA-LEWM-READ-0082 | mahmoud-assran; adrien-bardes; david-fan; et al. | unlisted | `support` | V-JEPA 2 的表征目标是预测场景中可预测的方面，而不是复原生成目标强调的所有像素级不可预测细节。 |
| EA-LEWM-READ-0084 | mahmoud-assran; adrien-bardes; david-fan; et al. | unlisted | `support` | 在论文展示的三个单目标 reaching 实例中，V-JEPA 2-AC 把末端移动到距目标不足 4 cm，并选择使误差单调下降的动作。 |
| EA-LEWM-READ-0026 | randall-balestriero; yann-lecun | unlisted | `support` | LeJEPA selects an Epps–Pulley empirical-characteristic-function regularizer because the implementation is DDP-friendly, has uniformly bounded gradients and cur... |
| EA-LEWM-READ-0027 | randall-balestriero; yann-lecun | unlisted | `support` | The LeJEPA objective combines the multi-view prediction loss with SIGReg and removes prototypes, stop-gradients, and teacher–student networks, leaving one coef... |
| EA-LEWM-READ-0029 | randall-balestriero; yann-lecun | unlisted | `support` | On ImageNet-10, LeJEPA pretrained approximately 50 architectures from eight families with fewer than 20 million parameters, and all reached 91.5%–95% top-1 acc... |
| EA-ALIGN-READ-0013 | chi-pin-huang; yunze-man; zhiding-yu; et al. | unlisted | `support` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 |
| EA-LEWM-READ-0001 | lucas-maes; quentin-le-lidec; damien-scieur; et al. | unlisted | `support` | LeWorldModel jointly trains a pixel encoder and an action-conditioned latent predictor; actions enter the predictor through AdaLN at every layer, and the predi... |
| EA-LEWM-READ-0002 | lucas-maes; quentin-le-lidec; damien-scieur; et al. | unlisted | `support` | SIGReg regularizes LeWM latents toward an isotropic Gaussian by projecting them onto random unit directions and matching each one-dimensional projection with a... |
| EA-LEWM-READ-0004 | lucas-maes; quentin-le-lidec; damien-scieur; et al. | unlisted | `support` | In the paper's simulated benchmark setup, LeWM achieved an 18% higher Push-T success rate than PLDM, while the fixed planning configuration completed a full pl... |
| EA-LEWM-READ-0005 | lucas-maes; quentin-le-lidec; damien-scieur; et al. | unlisted | `support` | The paper's direct cross-seed stability check is narrow: on Push-T, across three training seeds evaluated on the same 50 trajectories, PLDM exhibited higher su... |
| EA-ALIGN-READ-0014 | bohan-hou; gen-li; jindou-jia; et al. | unlisted | `support` | 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 |
| EA-LEWM-READ-0087 | nilaksh; saurav-jha; artem-zholus; et al. | unlisted | `support` | 该研究固定数据、历史长度、动作条件、转移架构、优化器和训练日程，仅改变冻结编码器、可选适配器与解码路径，从而把编码器定义的潜接口作为主要实验变量。 |
| EA-LEWM-READ-0041 | wenyuan-li; guang-li; keisuke-maeda; et al. | unlisted | `support` | RC-aux 通过多时域开放环预测修正时间错配，并以预算条件、方向敏感的轨迹可达性监督修正空间几何；测试时还可按剩余预算把可达性作为显式搜索信号。 |
| EA-LEWM-READ-0042 | wenyuan-li; guang-li; keisuke-maeda; et al. | unlisted | `support` | 在论文的五个匹配 LeWM-family 比较中，RC-aux 改善四项；Wall 成功率从 50.4±6.5 提升到 83.6±3.6，即提高 33.2 个百分点。 |
| EA-LEWM-READ-0021 | hoang-nguyen; xiaohao-xu; xiaonan-huang | unlisted | `support` | GC-IDM freezes the LeWorldModel representation and amortizes planning into a horizon-conditioned inverse map from current and goal latents to the next action;... |
| EA-LEWM-READ-0022 | hoang-nguyen; xiaohao-xu; xiaonan-huang | unlisted | `support` | On the eight environment–protocol cells in the main LeWM benchmark comparison, GC-IDM matched or outperformed CEM in seven, with Push-T as the lone exception. |
| EA-LEWM-READ-0046 | liangyu-li; shengzhi-wang; qingwen-liu | unlisted | `support` | 在固定 hard n100 TwoRoom 协议中，只替换终端 selector 的 full-horizon TRM 将 LeWM 平均成功率从 7.0% 提升到 97.0%，将本地 PLDM 从 32.7% 提升到 84.0%；同架构 shuffled-label heads 在两类模型上均为 0.0%。 |
| EA-LEWM-READ-0047 | liangyu-li; shengzhi-wang; qingwen-liu | unlisted | `support` | 在 LeWM seed 3072 的 matched-b50 消融中，平衡满 episode TRM 使用 100,000 pairs 达到 97.5% 成功率，而相同 pair 预算的平衡短时域 max 版本仅 35.0%。 |
| EA-LEWM-READ-0048 | liangyu-li; shengzhi-wang; qingwen-liu | unlisted | `support` | 在 matched-b50 TwoRoom 中，XY probe rowspace 只贡献 0.5–0.7% 的终端—目标潜 MSE，却使 rowspace-only planning 达到 90.8% 平均成功率；raw latent MSE 和 residual-only 均为 1.7%。 |
| EA-LEWM-READ-0008 | yuntian-gao; xiangyu-xu | unlisted | `support` | Fast-LeWM replaces LeWM's within-window autoregressive latent chain with action-prefix prediction: every future latent is predicted directly from the same obse... |
| EA-LEWM-READ-0009 | yuntian-gao; xiangyu-xu | unlisted | `support` | Under the same four-task LeWM planning protocol, base Fast-LeWM increased average success from 85.8% to 90.5%, and optional self-consistency increased it to 92... |
| EA-LEWM-READ-0011 | yuntian-gao; xiangyu-xu | unlisted | `support` | Across all four tasks, Fast-LeWM had lower initial open-loop latent error and a smaller least-squares error-growth slope than LeWM, while qualitative decoded r... |
| EA-LEWM-READ-0061 | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | unlisted | `support` | LDAD decodes the executed action from the latent displacement alone, so successful recovery requires local transition geometry to encode the action and encoura... |
| EA-LEWM-READ-0062 | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | unlisted | `support` | Across the four evaluated environments, Delta-JEPA had the highest mean planning success; it exceeded the strongest OGB-Cube baseline by 15.14 percentage point... |
| EA-LEWM-READ-0063 | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | unlisted | `support` | With the training and planning protocol held fixed, decoding actions from latent displacements improved planning relative to decoding from concatenated endpoin... |
| EA-LEWM-READ-0064 | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | unlisted | `support` | When the starting history is fixed and only the action input is varied, Delta-JEPA produces separated action-wise predictor responses, whereas LeWM's responses... |
| EA-LEWM-READ-0052 | niccol-caselli; francesco-massafra; samuele-punzo; et al. | unlisted | `support` | Empirical-macro CEM 不在连续潜 macro-action 空间中无约束搜索，而从训练轨迹编码的 macro-action 序列 bank 采样 anchor，并只在其附近拟合局部 residual。 |
| EA-LEWM-READ-0083 | mahmoud-assran; adrien-bardes; david-fan; et al. | unlisted | `conditional` | V-JEPA 2-AC 与论文基线使用同一套目标实验室协议部署在两座 Droid 未覆盖的实验室，输入为未标定、低分辨率单目 RGB，相同 V-JEPA 2-AC 权重和推理代码跨实验室复用。 |
| EA-LEWM-READ-0028 | randall-balestriero; yann-lecun | unlisted | `conditional` | The nonlinear-probe optimality result is conditional on a smooth embedding density with finite Fisher information and covariance, test queries drawn from the t... |
| EA-LEWM-READ-0003 | lucas-maes; quentin-le-lidec; damien-scieur; et al. | unlisted | `conditional` | LeWM planning is explicitly short-horizon and conditional: longer autoregressive rollouts trade additional lookahead for more compute and model bias, so the co... |
| EA-LEWM-READ-0088 | nilaksh; saurav-jha; artem-zholus; et al. | unlisted | `conditional` | 在论文的共享 Bridge V2 任务统计中，语义潜空间家族相对重建家族的 VLA 成功率高 9.8 个百分点、OOD 成功率高 13.6 个百分点，并把一步 CEM 动作误差降低 0.0266；三项 95% 配对 bootstrap 区间均不跨零。 |
| EA-LEWM-READ-0089 | nilaksh; saurav-jha; artem-zholus; et al. | unlisted | `conditional` | 在 DiT-S 的真实编码潜变量上，语义编码器的 IDM Pearson 为 0.772–0.829、轨迹成功分类准确率为 0.903–0.906；重建编码器对应范围为 0.507–0.626 和 0.835–0.868，且动作信息优势大体延续到世界模型生成潜变量。 |
| EA-LEWM-READ-0090 | nilaksh; saurav-jha; artem-zholus; et al. | unlisted | `conditional` | 在该受控实验中，重建对齐潜空间仍能保持较锐利的局部外观，但语义潜空间通常在全局结构和时序生成指标上更强；因此低层像素质量不足以解释策略效用。 |
| EA-LEWM-READ-0091 | nilaksh; saurav-jha; artem-zholus; et al. | unlisted | `conditional` | 论文的质性 rollout 显示两类潜空间会以不同方式失败：重建潜变量可能生成外观连贯但任务语义错误的状态，语义潜变量较能保持任务意图，却可能损失几何和接触精度。 |
| EA-LEWM-READ-0092 | nilaksh; saurav-jha; artem-zholus; et al. | unlisted | `conditional` | 把高维语义特征压缩到适配器潜空间通常更利于扩散去噪和高层任务完成，但会恶化潜空间 CEM 动作误差、OOD 鲁棒性或点跟踪等精细控制指标。 |
| EA-LEWM-READ-0043 | wenyuan-li; guang-li; keisuke-maeda; et al. | unlisted | `conditional` | Wall 消融中，RC-aux 训练后的模型即使仍用基础终端潜距离规划也达到 72.4±3.6%，高于 LeWM-family control 的 50.4±6.5%；加入可达性感知规划后进一步达到 83.6±3.6%。 |
| EA-LEWM-READ-0044 | wenyuan-li; guang-li; keisuke-maeda; et al. | unlisted | `conditional` | 在 LIBERO-Goal 的可训练 no-repeat OFT-style 动作头协议中，RC-aux 表征的平均成功率为 0.812，高于 LeWM 表征的 0.712；repeat tuning 后 RC-aux 为 0.864。 |
| EA-LEWM-READ-0023 | hoang-nguyen; xiaohao-xu; xiaonan-huang | unlisted | `conditional` | The paper's explanation that isotropic LeWM geometry makes inverse dynamics well conditioned is explicitly conditional: the authors did not verify that LeWM fu... |
| EA-LEWM-READ-0049 | liangyu-li; shengzhi-wang; qingwen-liu | unlisted | `conditional` | PushT go50 的 true hybrid cost 在论文权重 sweep 中达到 52.7% 平均成功率，高于 raw latent 的 40.0% 和最佳 shuffled hybrid 的 42.7%，但该提升被作者定位为连续接触任务中的边界结果。 |
| EA-LEWM-READ-0010 | yuntian-gao; xiangyu-xu | unlisted | `conditional` | On Two-Room with the same CEM budget and one NVIDIA 4090, one prefix-model call reduced dynamics time from 31.4s to 8.0s, but unchanged encoding/scoring/data o... |
| EA-LEWM-READ-0013 | yuntian-gao; xiangyu-xu | unlisted | `conditional` | The quality-speed gain depends on structured prefixes and intermediate supervision: simply enlarging LeWM's action block performed poorly, terminal-only Fast-L... |
| EA-LEWM-READ-0069 | ayan-pendharkar | unlisted | `conditional` | Inverse-dynamics retention of the exogenous feature depends on the behavior policy: random actions provide no anchor, whereas an informative policy can retain... |
| EA-LEWM-READ-0071 | ayan-pendharkar | unlisted | `conditional` | The trained JEPA latent realized substantially less class separation for the exogenous reward-relevant feature than reconstruction and supervised references, b... |
| EA-LEWM-READ-0065 | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | unlisted | `conditional` | LDAD is load-bearing but requires balance: removing or weakening its action-reconstruction term yields near-collapse or poor Push-T planning, while an excessiv... |
| EA-LEWM-READ-0053 | niccol-caselli; francesco-massafra; samuele-punzo; et al. | unlisted | `conditional` | Support-constrained high-level search 的收益取决于执行模式和时间尺度：staged execution 在中等时域最有帮助，但在最长 PushT 时域低于 online constrained replanning。 |
| EA-LEWM-READ-0085 | mahmoud-assran; adrien-bardes; david-fan; et al. | unlisted | `limit` | V-JEPA 2-AC 的已验证规划时域约为 16 秒；简单 grasp 和 reach-with-object 可用单一目标图像，但更长程 pick-and-place 若不提供子目标仍需新的建模方法。 |
| EA-LEWM-READ-0086 | mahmoud-assran; adrien-bardes; david-fan; et al. | unlisted | `limit` | 未做显式相机标定时，V-JEPA 2-AC 必须从单目图像隐式推断笛卡尔动作坐标轴；机器人基座不可见会导致欠定和预测错误，作者实际人工尝试多个相机位置后才固定配置。 |
| EA-LEWM-READ-0030 | randall-balestriero; yann-lecun | unlisted | `limit` | The practical minibatch SIGReg gradient is biased; the authors report the bias as small in their experiments but do not explore unbiased U-statistic or sample-... |
| EA-LEWM-READ-0031 | randall-balestriero; yann-lecun | unlisted | `limit` | LeJEPA's empirical validation does not directly test action-conditioned dynamics, world-model rollouts, planning, or closed-loop control; using SIGReg in LeWor... |
| EA-LEWM-READ-0006 | lucas-maes; quentin-le-lidec; damien-scieur; et al. | unlisted | `limit` | LeWM underperformed on the simple Two-Room environment; the authors hypothesize that low data diversity and low intrinsic dimensionality conflict with matching... |
| EA-LEWM-READ-0007 | lucas-maes; quentin-le-lidec; damien-scieur; et al. | unlisted | `limit` | The authors explicitly bound LeWM to short-horizon planning and sufficiently covering offline action-labeled datasets; low diversity weakens SIGReg, and removi... |
| EA-LEWM-READ-0093 | nilaksh; saurav-jha; artem-zholus; et al. | unlisted | `limit` | 该研究的结论局限于 Bridge V2 和共享机器人本体；策略内环只评估固定 VLA 在生成 rollout 中的表现，且部分成功判断依赖 VLM，尚未验证策略改进、sim-to-real 或更广本体。 |
| EA-LEWM-READ-0045 | wenyuan-li; guang-li; keisuke-maeda; et al. | unlisted | `limit` | RC-aux 的当前可达性监督仍以轨迹派生标签代理真实环境可达性，测试时也只采用简单可达性门控，因此尚未解决未观察捷径、不确定性和完整可行性决策。 |
| EA-LEWM-READ-0024 | hoang-nguyen; xiaohao-xu; xiaonan-huang | unlisted | `limit` | For Push-T, GC-IDM success peaked at 93.0% with a 25-step evaluation budget and declined to 75.0% at 100 steps, which the authors associate with clamped horizo... |
| EA-LEWM-READ-0025 | hoang-nguyen; xiaohao-xu; xiaonan-huang | unlisted | `limit` | The evaluation is confined mainly to one LeWM backbone and the stable-worldmodel suite, and GC-IDM does not reason about multi-step consequences; cross-world-m... |
| EA-LEWM-READ-0050 | liangyu-li; shengzhi-wang; qingwen-liu | unlisted | `limit` | TRM 的时间度量依赖轨迹覆盖，且同 episode 时间标签只是对称标量可达性代理，不是有向或预算条件的目标可达性值。 |
| EA-LEWM-READ-0012 | yuntian-gao; xiangyu-xu | unlisted | `limit` | Fast-LeWM removes sequential dependence only within one maximum encoded prefix window; the paper's longer open-loop evaluation already requires composing two m... |
| EA-LEWM-READ-0067 | ayan-pendharkar | unlisted | `limit` | A reward-relevant feature can be temporally unpredictable, in which case a latent self-prediction objective receives no signal to retain information that a con... |
| EA-LEWM-READ-0068 | ayan-pendharkar | unlisted | `limit` | Across both controlled environments, every evaluated reward-free predictive variant left the exogenous control-relevant feature near chance, while the reward-g... |
| EA-LEWM-READ-0070 | ayan-pendharkar | unlisted | `limit` | Increasing latent capacity did not rescue cell-4 retention for JEPA, while the reward-grounded variant remained high across the sweep, supporting an objective-... |
| EA-LEWM-READ-0072 | ayan-pendharkar | unlisted | `limit` | The study establishes an objective-level failure mode only in small synthetic environments; it does not test large pretrained models, robotics, standard RL ben... |
| EA-LEWM-READ-0066 | zhenghao-zhang; yuanxiang-wang; zhenyu-guan; et al. | unlisted | `limit` | Delta-JEPA does not establish that action-sensitive latents are sufficient for task control: its offline training data contain no rewards, and its two losses s... |
| EA-LEWM-READ-0051 | niccol-caselli; francesco-massafra; samuele-punzo; et al. | unlisted | `limit` | 在冻结低层 LeWM 的 Hi-LeWM 中，简单增加时间抽象层并不足以改善长时程控制；数据轨迹上的 oracle 中间 subgoal 通常可执行，而生成 subgoal 更不可靠、时间错位并对高层搜索空间敏感。 |
| EA-LEWM-READ-0054 | niccol-caselli; francesco-massafra; samuele-punzo; et al. | unlisted | `limit` | Hi-LeWM 的正面结论不能外推为 hierarchy 的一般优势：主分析集中于 PushT，VQ macro-actions 尚未充分评估，而且更高容量世界模型可能呈现不同结果。 |

## Synthesis Slots

### 共识/正向证据
- `EA-WMDATA-READ-0007`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-...
- `EA-WMDATA-READ-0008`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon future evolution rather t...
- `EA-TWM-READ-0003`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- `EA-TWM-READ-0004`: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。
- `EA-WMEVAL-READ-0005`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- `EA-WMEVAL-READ-0003`: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information downstream policies ne...
- `EA-WMEVAL-READ-0001`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- `EA-WMEVAL-READ-0010`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
### 条件成立
- `EA-JIMFAN-READ-0015`: DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and planning benefits after robot post-training.
- `EA-LEWM-READ-0083`: V-JEPA 2-AC 与论文基线使用同一套目标实验室协议部署在两座 Droid 未覆盖的实验室，输入为未标定、低分辨率单目 RGB，相同 V-JEPA 2-AC 权重和推理代码跨实验室复用。
- `EA-LEWM-READ-0028`: The nonlinear-probe optimality result is conditional on a smooth embedding density with finite Fisher information and covariance, test queries drawn from the training distribution, an isotropic mean-zero target-gradient...
- `EA-LEWM-READ-0003`: LeWM planning is explicitly short-horizon and conditional: longer autoregressive rollouts trade additional lookahead for more compute and model bias, so the controller executes only a planned action block before replann...
- `EA-LEWM-READ-0088`: 在论文的共享 Bridge V2 任务统计中，语义潜空间家族相对重建家族的 VLA 成功率高 9.8 个百分点、OOD 成功率高 13.6 个百分点，并把一步 CEM 动作误差降低 0.0266；三项 95% 配对 bootstrap 区间均不跨零。
- `EA-LEWM-READ-0089`: 在 DiT-S 的真实编码潜变量上，语义编码器的 IDM Pearson 为 0.772–0.829、轨迹成功分类准确率为 0.903–0.906；重建编码器对应范围为 0.507–0.626 和 0.835–0.868，且动作信息优势大体延续到世界模型生成潜变量。
- `EA-LEWM-READ-0090`: 在该受控实验中，重建对齐潜空间仍能保持较锐利的局部外观，但语义潜空间通常在全局结构和时序生成指标上更强；因此低层像素质量不足以解释策略效用。
- `EA-LEWM-READ-0091`: 论文的质性 rollout 显示两类潜空间会以不同方式失败：重建潜变量可能生成外观连贯但任务语义错误的状态，语义潜变量较能保持任务意图，却可能损失几何和接触精度。
### 限制与失败模式
- `EA-WMEVAL-READ-0013`: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- `EA-LEWM-READ-0085`: V-JEPA 2-AC 的已验证规划时域约为 16 秒；简单 grasp 和 reach-with-object 可用单一目标图像，但更长程 pick-and-place 若不提供子目标仍需新的建模方法。
- `EA-LEWM-READ-0086`: 未做显式相机标定时，V-JEPA 2-AC 必须从单目图像隐式推断笛卡尔动作坐标轴；机器人基座不可见会导致欠定和预测错误，作者实际人工尝试多个相机位置后才固定配置。
- `EA-LEWM-READ-0030`: The practical minibatch SIGReg gradient is biased; the authors report the bias as small in their experiments but do not explore unbiased U-statistic or sample-splitting alternatives.
- `EA-LEWM-READ-0031`: LeJEPA's empirical validation does not directly test action-conditioned dynamics, world-model rollouts, planning, or closed-loop control; using SIGReg in LeWorldModel is therefore a downstream mechanism transfer rather...
- `EA-LEWM-READ-0006`: LeWM underperformed on the simple Two-Room environment; the authors hypothesize that low data diversity and low intrinsic dimensionality conflict with matching a high-dimensional isotropic Gaussian prior, making this a...
- `EA-LEWM-READ-0007`: The authors explicitly bound LeWM to short-horizon planning and sufficiently covering offline action-labeled datasets; low diversity weakens SIGReg, and removing the need for action labels remains future work.
- `EA-LEWM-READ-0093`: 该研究的结论局限于 Bridge V2 和共享机器人本体；策略内环只评估固定 VLA 在生成 rollout 中的表现，且部分成功判断依赖 VLM，尚未验证策略改进、sim-to-real 或更广本体。
### 开放问题
- `EA-WMEVAL-READ-0004`: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 24 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-JIMFAN-READ-0015` DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluati...
  - `EA-WMDATA-READ-0007` A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its...
  - `EA-WMDATA-READ-0008` Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to repr...
- Scientific memo preview: 《LeWorldModel 技术谱系：JEPA 潜空间世界模型到规划控制》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: LeWorldModel 技术谱系：JEPA 潜空间世界模型到规划控制 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: LeWorldModel 技术谱系：JEPA 潜空间世界模型到规划控制: 先看证据边界，再谈一个可传播的反常识洞察。

## Draft Outline

1. 研究边界与证据范围
2. 概念与问题结构
3. 主要共识
4. 条件、限制与分歧
5. 未解决问题
6. 对后续研究/项目的启发

## Traceability Checklist

- Cite event IDs for paper-specific claims.
- Cite stable source IDs for topic-card background.
- Mark cross-event synthesis as `inference` with a short reason.
- Do not cite candidate-only papers as accepted evidence.
- Open raw sources before using exact wording.
