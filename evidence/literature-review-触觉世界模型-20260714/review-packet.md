# Review Packet: 触觉世界模型

## Scope

- Topic: 触觉世界模型
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-SENSOR`, `EA-DATA`, `EA-MODEL`, `EA-EVAL`
- Evidence events: 30
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> full-text evidence -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval, HTML/PDF/OCR recovery, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 30
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-TWM-2026-0005`, `EA-TWM-2026-0014`, `EA-TWM-2026-0013`, `EA-TWM-2026-0004`, `EA-TWM-2026-0008`, `EA-TWM-2026-0001`, `EA-TWM-2026-0010`, `EA-TWM-2026-0002`, `EA-TWM-2026-0012`, `EA-EVAL-2026-0007`, `EA-TWM-2026-0015`, `EA-EVAL-2026-0012`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 23 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；触觉世界模型应预测动作条件下的接触演化，而不只是重建触觉图像。多模态建模的目标不是堆传感器，而是让每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；高分筛选还必须保留任务、本体、场景和长尾覆盖。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。所有异构数据都应声明其可信监督字段，并以真实闭环收益作为最终验收。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
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

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 17 |
| `conditional` | 条件成立 | 8 |
| `limit` | 限制/负面 | 3 |
| `gap` | 缺口 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.06001: Visuo-Tactile World Models | 2026-02-05 | conditional, support | EA-TWM-2026-0003; EA-TWM-2026-0004 |
| 2603.15257: HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing | 2026-03-16 | conditional | EA-TWM-2026-0017 |
| 2603.19201: OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation | 2026-03-19 | support | EA-TWM-2026-0005; EA-TWM-2026-0006 |
| 2604.07335: TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks | 2026-04-08 | support | EA-TWM-2026-0014 |
| 2605.07308: AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models | 2026-05-08 | conditional | EA-TWM-2026-0016 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | support | EA-TWM-2026-0013; EA-TWM-2026-0018 |
| 2606.08737: Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation | 2026-06-07 | conditional, support | EA-TWM-2026-0009; EA-TWM-2026-0010 |
| 2606.08765: RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation | 2026-06-07 | conditional | EA-SENSOR-2026-0002 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | support | EA-TWM-2026-0007; EA-TWM-2026-0008 |
| 2606.13877: ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation | 2026-06-11 | conditional, support | EA-TWM-2026-0001; EA-TWM-2026-0002 |
| 2606.14981: Inference-time Policy Steering via Vision and Touch | 2026-06-12 | limit, support | EA-TWM-2026-0011; EA-TWM-2026-0012 |
| 2606.16690: PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation | 2026-06-15 | limit | EA-SENSOR-2026-0005 |
| 2606.18043: Uncertainty Quantification for Flow-Based Vision-Language-Action Models | 2026-06-16 | support | EA-SENSOR-2026-0004 |
| 2606.19161: HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision | 2026-06-17 | gap | EA-TWM-2026-0015 |
| 2606.20754: Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models | 2026-06-18 | support | EA-SENSOR-2026-0003 |
| 2606.26663: Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention | 2026-06-25 | conditional | EA-SENSOR-2026-0008 |
| 2606.28899: You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact | 2026-06-27 | support | EA-SENSOR-2026-0006 |
| 2606.29384: Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model | 2026-06-28 | support | EA-SENSOR-2026-0011 |
| 2606.30988: Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force | 2026-06-29 | conditional | EA-SENSOR-2026-0010 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | support | EA-SENSOR-2026-0009 |
| 2607.04234: SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objec... | 2026-07-05 | limit | EA-EVAL-2026-0007 |
| 2607.07196: Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators | 2026-07-08 | gap | EA-EVAL-2026-0012 |
| 2607.07287: TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation | 2026-07-08 | support | EA-SENSOR-2026-0001 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-TWM-2026-0005 | EA-DATA | `support` | `direct` | 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。 | OmniVTA 提出 OmniViTac 数据集，包含 21,879 条轨迹、86 个任务、126 个对象，覆盖擦拭、剥离、切割、抓取、装配、手内调整等六类物理接触模式，并使用 RGB-D、高频触觉和动作数据；系统支持多种触觉传感器并做时间对齐、可视化和人工核验。 (Figure 2; Section III The OmniViTac Dataset; Section III-A Hardware Setup and Data Co... | yuhang-zheng | 2603.19201 |
| EA-TWM-2026-0014 | EA-DATA | `support` | `direct` | 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。 | TAMEn 提出双模式采集管线：MoCap 精准模式和 VR in-the-wild 模式，并引入 feasibility-aware acquisition、触觉可视化 recovery teleoperation 和金字塔数据 regime；论文报告平均任务成功率从 34% 提升到 75%，且 tactile pretraining 从 55% 进一步到 65%。 (Abstract; Section III-C Feasibil... | longyan-wu | 2604.07335 |
| EA-TWM-2026-0013 | EA-DATA | `support` | `direct` | 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。 | HapTile 包含 1,726 条演示、38 个任务、9 类操作技能，由 9 名操作者通过带 haptic feedback 的遥操作接口采集；每条演示含语言指令、同步视觉、触觉、机器人状态和动作轨迹，15Hz 采样，总交互时长 750.33 分钟。 (Abstract; Section 3.1 Dataset Statistics; Section 3.2 Synchronization and Data Quality Cont... | amirhosein-alian | 2606.04825 |
| EA-TWM-2026-0004 | EA-DATA | `conditional` | `direct` | 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 | 该论文训练数据包含 124 条遥操作演示、约 112k datapoints、8 个接触丰富任务、成功与失败演示、proprioception、外部视频和四个 Digit 360 指尖视频，并通过时间戳同步后降采样到 6 FPS；限制部分说明评测主要在同场景同对象，触觉模态限于 Digit 360，CEM 规划成本高且以开环 action chunk 执行。 (Appendix B.0.1 Training Dataset; Appe... | carolina-higuera | 2602.06001 |
| EA-TWM-2026-0008 | EA-EVAL | `support` | `direct` | 触觉世界模型必须在扰动与恢复数据上评估，否则会高估接触丰富任务的稳定性。 | TacForeSight 在五个任务和三类 in-process perturbation 上评测，并纳入 recovery demonstrations；完整模型平均成功率 79.0%，扰动设置平均 86.7%，去掉预测触觉或简单拼接力触觉都会削弱表现。 (Section IV-B Experimental Setup; Section IV-C Results; Section IV-D Ablation) | yujie-zang | 2606.11184 |
| EA-TWM-2026-0001 | EA-EVAL | `support` | `direct` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 | ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。 (Abstract; Section 2.2 Sensory Modalities and Representation Structure; Section 3 What Represe... | zhiyuan-zhang | 2606.13877 |
| EA-TWM-2026-0010 | EA-EVAL | `conditional` | `direct` | 在触觉世界动作模型中，触觉融合需要对接触事件做门控，否则会把稀疏、事件驱动的触觉信号当作持续视觉信号处理。 | Dream-Tac 的接触门控和 contact-aware attention 只在触觉变化明显时增强跨模态作用；作者报告六个真实接触丰富任务平均成功率 83.3%，高于 Cosmos-Policy 51.7%、ForceVLA 50.8% 等，并报告训练最高 2.9 倍、推理最高 1.8 倍加速。 (Abstract; Section 4.2 Performance on Real-World Experiments; Secti... | yunfan-lou | 2606.08737 |
| EA-TWM-2026-0002 | EA-EVAL | `conditional` | `direct` | 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。 | ContactWorld 报告触觉在长时域规划下更能缓解接触不确定性积累；真实阀门旋拧实验中，点云达到 90% 成功率，TacRGB 对图像视角有帮助，但 TacDepth/TacFF 不稳定，作者把差异归因于标记跟踪、深度、力推断和触觉标定噪声。 (Abstract; Appendix F.2 Tactile Representation Ablation; Appendix G Real-World Experiment) | zhiyuan-zhang | 2606.13877 |
| EA-TWM-2026-0012 | EA-EVAL | `limit` | `direct` | 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。 | ViTaL 的限制部分指出，latent world model 的保真度会影响验证，尤其是细微接触事件；触觉 verifier 受限于较小规模触觉编码器预训练，作者认为更大规模触觉预训练可能提升接触推理。 (Section 6 Conclusion and Limitations) | yilin-wu | 2606.14981 |
| EA-EVAL-2026-0007 | EA-EVAL | `limit` | `direct` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 | 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。 (arXiv HTML Abstract; 1... | bowen-jing | 2607.04234 |
| EA-TWM-2026-0015 | EA-EVAL | `gap` | `direct` | 触觉表征评测正在扩展到大规模全手触觉和自我中心视觉，但多数评测仍停留在表征层，不能直接证明下游机器人性能。 | HT-Bench 含 10M RGB frames、7.8M tactile frames、226 个任务，评估接触几何、视觉-触觉对齐和未见任务泛化，包括触觉检索、inpainting、vision-to-tactile synthesis 和 multimodal tactile prediction；限制部分说明当前评测不直接测量下游机器人表现。 (Abstract; Section 3 HT-Bench; Section 6... | yuzhe-huang | 2606.19161 |
| EA-EVAL-2026-0012 | EA-EVAL | `gap` | `direct` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 | 作者指出机器人中 World Models 越来越被用于模拟动作后果并给出 success/safety verdict，但视频生成指标如 FVD 奖励视觉真实感，却忽略世界是否对 policy actions 正确响应；他们主张作为 test oracle 的 WM 需要先通过 accreditation，并提出 L0-L4 admissibility ladder。 (arXiv HTML Abstract; I Introduc... | christian-oefinger | 2607.07196 |
| EA-TWM-2026-0003 | EA-MODEL | `support` | `direct` | 把触觉作为接触 grounding 信号注入世界模型，可以改善被遮挡或视觉混淆场景中的物体持续性、物理一致性和零样本接触规划。 | Visuo-Tactile World Models 使用外部视觉 latent、Digit 360 触觉 latent 和动作条件 transformer 预测未来；论文报告触觉 grounding 带来物体持续性 +33%、物理规律符合度 +29%，并在真实机器人接触丰富规划中最高提升 +35% 成功率。 (Abstract; Section 3.1 What vision does not see; Section 3.2 Vi... | carolina-higuera | 2602.06001 |
| EA-TWM-2026-0006 | EA-MODEL | `support` | `direct` | 触觉世界模型的落地形态正在从被动观测转向预测接触演化并驱动快速反射式控制。 | OmniVTA 由自监督触觉编码器、双流视觉-触觉世界模型、接触感知融合策略和 60Hz reflexive latent tactile controller 组成；作者称模型预测短时域接触演化，并在预测与观测触觉信号偏离时修正动作。 (Abstract; Section I Introduction; Section IV Method; Section VI Conclusion) | yuhang-zheng | 2603.19201 |
| EA-TWM-2026-0009 | EA-MODEL | `support` | `direct` | 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 | Dream-Tac 把 world action model 扩展到触觉，联合建模当前视觉、触觉、语言指令下的未来视觉观测、未来触觉观测和动作 chunk，并加入 contact-gated visuotactile fusion 与 contact-aware attention bias。 (Abstract; Section 3.2 Dream-Tac Architecture; Section 3.4 Training Obj... | yunfan-lou | 2606.08737 |
| EA-TWM-2026-0007 | EA-MODEL | `support` | `direct` | 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 | TacForeSight 的 TacForceWM 从双指触觉观测出发，以高频腕部 force/torque 为条件预测短时域触觉 latent dynamics；ablation 中 wrist wrench 条件的未来触觉预测优于无条件版本，MSE 从 0.027 降到 0.017，cosine 从 0.954 提升到 0.992。 (Abstract; Section III-A TacForceWM; Section IV-D... | yujie-zang | 2606.11184 |
| EA-TWM-2026-0011 | EA-MODEL | `support` | `direct` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 | ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。 (Abstract; Section 4 ViTaL; Section 5 Experiments) | yilin-wu | 2606.14981 |
| EA-TWM-2026-0017 | EA-MODEL | `conditional` | `direct` | 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。 | HapticVLA 提出 Safety-Aware Reward-Weighted Flow Matching 和 Tactile Distillation，把惩罚过大抓取力和不良抓取轨迹的触觉奖励编码进 VLA；论文报告不使用推理期力传感器也达到 86.7% 平均成功率，并优于若干直接使用触觉反馈的 VLA 基线。 (Abstract; Section III Method; Section IV Experiments) | konstantin-gubernatorov | 2603.15257 |
| EA-TWM-2026-0016 | EA-MODEL | `conditional` | `direct` | 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 | AT-VLA 把系统分为慢速视觉语言流和快速触觉流，慢速流负责任务理解和视觉定位，快速流以高频处理触觉反馈；作者采用 3:1 的快慢流频率比，并在真实接触丰富任务中验证 adaptive tactile injection、tactile gate、adaptive cross-attention 和 reaction dual-stream 的作用。 (Abstract; Section 3.3 Effective Tactile... | xiaoqi-li | 2605.07308 |
| EA-TWM-2026-0018 | EA-SENSOR | `support` | `direct` | 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 | HapTile 的每个夹爪手指安装视觉触觉传感器，接触会带来图像变化和 marker displacement；论文把 marker-motion 信号保存进数据集并用于 haptic feedback，实验也比较 vision-only、vision+tactile image 与 vision+tactile+marker 表征。 (Section 4.2 Vision-Based Tactile Sensing and Mark... | amirhosein-alian | 2606.04825 |
| EA-SENSOR-2026-0004 | EA-SENSOR | `support` | `direct` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 | 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。 (arXiv HTML Abstract; 1 Introduction; Appendix B.4 Uncertainty Quantificat... | ralf-romer | 2606.18043 |
| EA-SENSOR-2026-0003 | EA-SENSOR | `support` | `direct` | VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 | 作者指出现代 VLA 常用回归或 flow-based action generation，缺少显式预测概率；他们通过对 transformer hidden activations 注入高斯扰动，利用扰动后动作预测分歧估计不确定性，并在 LIBERO/LIBERO-PRO 的分布偏移下提升失败检测。 (arXiv HTML Abstract; I Introduction; IV-D Main Results) | yousung-lee | 2606.20754 |
| EA-SENSOR-2026-0006 | EA-SENSOR | `support` | `direct` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 | 作者明确指出视觉位姿估计常在遮挡、差光照、反光或透明表面下失败，并提出 tactile-only pose estimation：把触觉接触表示成局部 3D 点云，结合校准传感器位姿恢复完整 6-DoF object pose；实验在视觉不可靠时优于视觉和几何基线。 (arXiv HTML Abstract; 1 Introduction; 4.2 6-DoF Object Pose Estimation under Occlusio... | pengfei-ye | 2606.28899 |
| EA-SENSOR-2026-0011 | EA-SENSOR | `support` | `direct` | RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 | 作者指出现有 VLA 往往假设稳定明亮的室内环境，而真实操作中 illumination shifts 会造成 degraded RGB observations；Event-VLA 将 degraded visibility 定义为 RGB-centric policies 的鲁棒性问题，并通过 action-query routing 将 event streams 融入 action representation，仿真和真实部署... | jiaxin-liu | 2606.29384 |
| EA-SENSOR-2026-0009 | EA-SENSOR | `support` | `direct` | 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。 | 作者指出 VLA 在 contact-rich tasks 中会被小接触扰动触发不可恢复失败，且这些失败常难以单靠视觉检测；TACO 用 tactile-aware world model 识别 failure-adjacent states、想象局部 correction segments 并标注可执行纠正动作，真实接触任务报告相对 base policy 的成功率提升。 (arXiv HTML Abstract; 1 Introd... | shengbang-liu | 2607.02840 |
| EA-SENSOR-2026-0001 | EA-SENSOR | `support` | `direct` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 | 作者把日常灵巧操作的误差来源明确落在滑移、错位、不稳定抓取和力不匹配上，并指出视觉/语言不能可靠揭示力、滑移和接触稳定性；其分层策略将视觉语言子任务规划、触觉世界模型预测和高频触觉残差修正分开。 (arXiv HTML Abstract; 1 Introduction) | jianyi-zhou | 2607.07287 |
| EA-SENSOR-2026-0002 | EA-SENSOR | `conditional` | `direct` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 | 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。 (arXiv HTML Abstract; 1 Introduction; 3.2 Force-Aware Kinematic Projection; 4.3 Ablation on RGB-S Design Choices) | shengcheng-luo | 2606.08765 |
| EA-SENSOR-2026-0008 | EA-SENSOR | `conditional` | `direct` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 | 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。 (arXiv HTML Abstract; I Intro... | siyu-wu | 2606.26663 |
| EA-SENSOR-2026-0010 | EA-SENSOR | `conditional` | `direct` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 | 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only po... | jaden-clark | 2606.30988 |
| EA-SENSOR-2026-0005 | EA-SENSOR | `limit` | `direct` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 | 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差... | yanan-zhou | 2606.16690 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-TWM-2026-0005 | yuhang-zheng | unlisted | `support` | 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。 |
| EA-TWM-2026-0014 | longyan-wu | unlisted | `support` | 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。 |
| EA-TWM-2026-0013 | amirhosein-alian | unlisted | `support` | 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。 |
| EA-TWM-2026-0004 | carolina-higuera | unlisted | `conditional` | 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 |
| EA-TWM-2026-0008 | yujie-zang | unlisted | `support` | 触觉世界模型必须在扰动与恢复数据上评估，否则会高估接触丰富任务的稳定性。 |
| EA-TWM-2026-0001 | zhiyuan-zhang | unlisted | `support` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 |
| EA-TWM-2026-0010 | yunfan-lou | unlisted | `conditional` | 在触觉世界动作模型中，触觉融合需要对接触事件做门控，否则会把稀疏、事件驱动的触觉信号当作持续视觉信号处理。 |
| EA-TWM-2026-0002 | zhiyuan-zhang | unlisted | `conditional` | 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。 |
| EA-TWM-2026-0012 | yilin-wu | unlisted | `limit` | 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。 |
| EA-EVAL-2026-0007 | bowen-jing | unlisted | `limit` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 |
| EA-TWM-2026-0015 | yuzhe-huang | unlisted | `gap` | 触觉表征评测正在扩展到大规模全手触觉和自我中心视觉，但多数评测仍停留在表征层，不能直接证明下游机器人性能。 |
| EA-EVAL-2026-0012 | christian-oefinger | unlisted | `gap` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 |
| EA-TWM-2026-0003 | carolina-higuera | unlisted | `support` | 把触觉作为接触 grounding 信号注入世界模型，可以改善被遮挡或视觉混淆场景中的物体持续性、物理一致性和零样本接触规划。 |
| EA-TWM-2026-0006 | yuhang-zheng | unlisted | `support` | 触觉世界模型的落地形态正在从被动观测转向预测接触演化并驱动快速反射式控制。 |
| EA-TWM-2026-0009 | yunfan-lou | unlisted | `support` | 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 |
| EA-TWM-2026-0007 | yujie-zang | unlisted | `support` | 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 |
| EA-TWM-2026-0011 | yilin-wu | unlisted | `support` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 |
| EA-TWM-2026-0017 | konstantin-gubernatorov | unlisted | `conditional` | 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。 |
| EA-TWM-2026-0016 | xiaoqi-li | unlisted | `conditional` | 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 |
| EA-TWM-2026-0018 | amirhosein-alian | unlisted | `support` | 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 |
| EA-SENSOR-2026-0004 | ralf-romer | unlisted | `support` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 |
| EA-SENSOR-2026-0003 | yousung-lee | unlisted | `support` | VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 |
| EA-SENSOR-2026-0006 | pengfei-ye | unlisted | `support` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 |
| EA-SENSOR-2026-0011 | jiaxin-liu | unlisted | `support` | RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 |
| EA-SENSOR-2026-0009 | shengbang-liu | unlisted | `support` | 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。 |
| EA-SENSOR-2026-0001 | jianyi-zhou | unlisted | `support` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 |
| EA-SENSOR-2026-0002 | shengcheng-luo | unlisted | `conditional` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 |
| EA-SENSOR-2026-0008 | siyu-wu | unlisted | `conditional` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 |
| EA-SENSOR-2026-0010 | jaden-clark | unlisted | `conditional` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 |
| EA-SENSOR-2026-0005 | yanan-zhou | unlisted | `limit` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 |

## Synthesis Slots

### 共识/正向证据
- `EA-TWM-2026-0005`: 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。
- `EA-TWM-2026-0014`: 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。
- `EA-TWM-2026-0013`: 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。
- `EA-TWM-2026-0008`: 触觉世界模型必须在扰动与恢复数据上评估，否则会高估接触丰富任务的稳定性。
- `EA-TWM-2026-0001`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- `EA-TWM-2026-0003`: 把触觉作为接触 grounding 信号注入世界模型，可以改善被遮挡或视觉混淆场景中的物体持续性、物理一致性和零样本接触规划。
- `EA-TWM-2026-0006`: 触觉世界模型的落地形态正在从被动观测转向预测接触演化并驱动快速反射式控制。
- `EA-TWM-2026-0009`: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
### 条件成立
- `EA-TWM-2026-0004`: 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。
- `EA-TWM-2026-0010`: 在触觉世界动作模型中，触觉融合需要对接触事件做门控，否则会把稀疏、事件驱动的触觉信号当作持续视觉信号处理。
- `EA-TWM-2026-0002`: 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。
- `EA-TWM-2026-0017`: 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。
- `EA-TWM-2026-0016`: 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。
- `EA-SENSOR-2026-0002`: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- `EA-SENSOR-2026-0008`: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- `EA-SENSOR-2026-0010`: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
### 限制与失败模式
- `EA-TWM-2026-0012`: 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。
- `EA-EVAL-2026-0007`: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- `EA-SENSOR-2026-0005`: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
### 开放问题
- `EA-TWM-2026-0015`: 触觉表征评测正在扩展到大规模全手触觉和自我中心视觉，但多数评测仍停留在表征层，不能直接证明下游机器人性能。
- `EA-EVAL-2026-0012`: 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 23 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-TWM-2026-0005` 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。
  - `EA-TWM-2026-0014` 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。
  - `EA-TWM-2026-0013` 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。
- Scientific memo preview: 《触觉世界模型》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 触觉世界模型 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 触觉世界模型: 先看证据边界，再谈一个可传播的反常识洞察。

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
