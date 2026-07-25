# Review Packet: 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进

## Scope

- Topic: 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进
- Time range: 2025-07-20..2026-07-20
- Review style: `survey`
- Knowledge IDs: `EA-SENSOR`, `EA-MODEL`, `EA-ALIGN`, `EA-XEMBODIMENT`, `EA-DATA`
- Evidence events: 56
- Topic cards: 5
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 56
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-EGO-2026-0007`, `EA-TWM-READ-0008`, `EA-TWM-READ-0005`, `EA-TWM-READ-0002`, `EA-TWM-READ-0006`, `EA-TWM-READ-0003`, `EA-TWM-READ-0004`, `EA-TWM-READ-0015`, `EA-TWM-READ-0001`, `EA-EGO-2026-0008`, `EA-TWM-READ-0007`, `EA-EGO-2026-0017`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 42 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 42
- Structure mapped: 42
- Deep-read papers: 42
- Claim-verified papers: 42
- Accepted evidence papers: 42
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。第一视角视频尤其要分开相机自运动、手物运动与主动视点动作；视觉定位也要把外观召回、几何可恢复性和拒识覆盖分账。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；触觉世界模型应预测动作条件下的接触演化，而不只是重建触觉图像。多模态建模的目标不是堆传感器，而是让每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型后果预演、本体适配器与底层控制器组成的融合栈。近期 loco-manipulation 证据进一步表明，系统分层边界应从上肢/下肢改为任务意图/全身执行，完整动作接口本身会限制模型能力上限。Ego-centric 人类视频可扩展行为与视点先验，但只有经过动作恢复、本体对齐和目标机器人锚定后，才可能转成可执行控制。基础模型、适配模块与检查点还构成需要独立审计的供应链。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-ALIGN` VLA 多模态与动作对齐: VLA 对齐的核心不是把语言、视觉和动作都变成 token，而是处理三种信号的粒度与物理语义错配：语言通常任务级且稀疏，视觉高维稠密并容易形成捷径，动作连续、闭环且受本体和控制器约束。可靠系统需要显式连接语言到任务阶段、视觉几何到可执行动作、共享状态变化到机器人特定控制器。动作表示应以物理状态变化和可执行性为中心，而不是以模型输出方便为中心。
  - 稠密 visual-action 监督可能压过稀疏 language-action 信号，使语言退化为装饰性条件。
  - 阶段级语言、dense reasoning 或独立 language-action pretraining 可以增强语言对动作的约束，但会引入新的标注和误差传播问题。
  - 视觉不是越稠密越好；应通过 task-space action、结构化场景接口、affordance 或轨迹监督组织成动作相关表示。
  - 离散 action token 便于接入自回归模型，但解码到连续控制时必须条件化机器人状态、本体、接触和控制器。
  - VLA 可以继承视觉与语言先验，却不会自动继承连续运动先验；action prior 或 flow/diffusion action expert 可独立预训练。
- `EA-XEMBODIMENT` 跨本体与数据迁移: 跨本体迁移的核心不是复制姿态或控制命令，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。不同机器人即使记录相同 action command，也可能产生不同运动；更稳健的路线是共享 Cartesian state delta、对象状态变化或接触目标，再由机器人特定 adapter 和真实闭环校准落地。
  - 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
  - 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
  - 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
  - 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
  - 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。
- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；高分筛选还必须保留任务、本体、场景和长尾覆盖。数据污染则是样本与来源、时间、任务、模型版本和评测边界的关系失真，治理必须贯穿采集、选择、训练、生成和闭环评测。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。所有异构数据都应声明其可信监督字段，并以真实闭环收益作为最终验收。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 21 |
| `conditional` | 条件成立 | 20 |
| `limit` | 限制/负面 | 14 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2509.21986: Developing Vision-Language-Action Model from Egocentric Videos | 2025-09-26T07:09:33Z | limit | EA-EGO-2026-0003; EA-EGO-2026-0004 |
| 2512.11047: WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control | 2025-12-11T19:07:31Z | support | EA-LOCOMANIP-2026-0006 |
| 2601.09708: Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning | 2026-01-14 | support | EA-ALIGN-READ-0013 |
| 2602.06001: Visuo-Tactile World Models | 2026-02-05 | conditional | EA-TWM-READ-0001 |
| 2602.11291: H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model | 2026-02-11T19:08:36Z | conditional, limit, support | EA-VLABREAK-2026-0001; EA-VLABREAK-2026-0002; EA-VLABREAK-2026-0003 |
| 2602.16710: EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data | 2026-02-18T18:59:05Z | conditional, limit, support | EA-EGO-2026-0007; EA-EGO-2026-0008; EA-EGO-2026-0009 |
| 2602.21161: ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking | 2026-02-24 | conditional | EA-ALIGN-READ-0010 |
| 2603.03279: ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation | 2026-03-03T18:59:29Z | conditional | EA-LOCOMANIP-2026-0018 |
| 2603.12553: Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation | 2026-03-13T01:33:48Z | conditional, support | EA-VLABREAK-2026-0004; EA-VLABREAK-2026-0005 |
| 2604.07335: TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks | 2026-04-08 | support | EA-TWM-READ-0008 |
| 2604.27224: Learning Tactile-Aware Quadrupedal Loco-Manipulation Policies | 2026-04-29T21:46:58Z | support | EA-LOCOMANIP-2026-0012 |
| 2605.00080: World Model for Robot Learning: A Comprehensive Survey | 2026-04-30 | support | EA-ALIGN-READ-0014 |
| 2605.07308: AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models | 2026-05-08 | conditional | EA-TWM-READ-0007 |
| 2605.26349: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Co... | 2026-05-25 | support | EA-ALIGN-READ-0012 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional | EA-ALIGN-READ-0011 |
| 2606.03784: Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation | 2026-06-02 | conditional | EA-ALIGN-READ-0006 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional, support | EA-ALIGN-READ-0007; EA-TWM-READ-0005 |
| 2606.06194: ActiveMimic: Egocentric Video Pretraining with Active Perception | 2026-06-04T14:01:01Z | conditional, limit | EA-EGO-2026-0016; EA-EGO-2026-0017; EA-EGO-2026-0018 |
| 2606.08737: Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation | 2026-06-07 | support | EA-TWM-READ-0002 |
| 2606.08765: RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation | 2026-06-07 | conditional | EA-SENSORERR-READ-0007; EA-TWM-READ-0014 |
| 2606.09630: ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies | 2026-06-08 | support | EA-ALIGN-READ-0015 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional, support | EA-ALIGN-READ-0008; EA-TWM-READ-0006 |
| 2606.13877: ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation | 2026-06-11 | support | EA-TWM-READ-0003 |
| 2606.14981: Inference-time Policy Steering via Vision and Touch | 2026-06-12 | support | EA-TWM-READ-0004 |
| 2606.16690: PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation | 2026-06-15 | limit | EA-TWM-READ-0009 |
| 2606.18043: Uncertainty Quantification for Flow-Based Vision-Language-Action Models | 2026-06-16 | support | EA-TWM-READ-0015 |
| 2606.24049: SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies | 2026-06-23 | limit | EA-ALIGN-READ-0001 |
| 2606.26663: Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention | 2026-06-25 | conditional | EA-TWM-READ-0010 |
| 2606.26800: SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation | 2026-06-25 | conditional | EA-ALIGN-READ-0002 |
| 2606.28899: You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact | 2026-06-27 | support | EA-SENSORERR-READ-0010 |
| 2606.29384: Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model | 2026-06-28 | support | EA-SENSORERR-READ-0011 |
| 2606.30113: SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance | 2026-06-29 | limit | EA-ALIGN-READ-0003 |
| 2606.30456: Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform | 2026-06-29 | limit | EA-ALIGN-READ-0004 |
| 2606.30552: Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision | 2026-06-29 | support | EA-ALIGN-READ-0005 |
| 2606.30988: Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force | 2026-06-29 | conditional | EA-SENSORERR-READ-0004; EA-TWM-READ-0011 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-ALIGN-READ-0009 |
| 2607.03828: ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Mode... | 2026-07-04T11:31:23Z | conditional, limit | EA-EGO-2026-0019; EA-EGO-2026-0020 |
| 2607.04234: SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objec... | 2026-07-05 | limit | EA-TWM-READ-0012 |
| 2607.07196: Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators | 2026-07-08 | gap | EA-TWM-READ-0013 |
| 2607.07287: TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation | 2026-07-08 | support | EA-SENSORERR-READ-0012 |
| 2607.10132: TAC-LOCO: Unified Whole-Body Control for Quadrupedal TACtile-Informed LOCO-Manipulation | 2026-07-11T05:45:24Z | support | EA-LOCOMANIP-2026-0021 |
| 2607.15207: BadWAM: When World-Action Models Dream Right but Act Wrong | 2026-07-16T17:04:15Z | limit | EA-VLABREAK-2026-0006; EA-VLABREAK-2026-0007 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-EGO-2026-0007 | EA-DATA | `support` | `direct` | 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 | 五个数据规模的同架构实验报告单调提升，并限制结论不外推到测量区间之外。 (3.3 Policy Performance Scales with Pretraining Data Size) | ruijie-zheng; dantong-niu; yuqi-xie; et al. | 2602.16710 |
| EA-TWM-READ-0008 | EA-DATA | `support` | `direct` | TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 | 摘要明确列出精度/便携双模式采集、触觉恢复遥操作和人在环恢复数据。 (Abstract (full-text section)) | longyan-wu; jieji-ren; chenghang-jiang; et al. | 2604.07335 |
| EA-TWM-READ-0005 | EA-DATA | `support` | `direct` | 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 | HapTile 的每个夹爪手指安装视觉触觉传感器，接触会带来图像变化和 marker displacement；论文把 marker-motion 信号保存进数据集并用于 haptic feedback，实验也比较 vision-only、vision+tactile image 与 vision+tactile+marker 表征。 (4.2 Vision-Based Tactile Sensing and Marker Track... | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-TWM-READ-0002 | EA-DATA | `support` | `direct` | 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 | Dream-Tac 把 world action model 扩展到触觉，联合建模当前视觉、触觉、语言指令下的未来视觉观测、未来触觉观测和动作 chunk，并加入 contact-gated visuotactile fusion 与 contact-aware attention bias。 (Abstract (full-text section)) | yunfan-lou; yifan-ye; yankai-fu; et al. | 2606.08737 |
| EA-TWM-READ-0006 | EA-DATA | `support` | `direct` | 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 | TacForeSight 的 TacForceWM 从双指触觉观测出发，以高频腕部 force/torque 为条件预测短时域触觉 latent dynamics；ablation 中 wrist wrench 条件的未来触觉预测优于无条件版本，MSE 从 0.027 降到 0.017，cosine 从 0.954 提升到 0.992。 (IV-D 1 World Model Conditioning) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-TWM-READ-0003 | EA-DATA | `support` | `direct` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 | ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。 (Abstract (full-text section)) | zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al. | 2606.13877 |
| EA-TWM-READ-0004 | EA-DATA | `support` | `direct` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 | ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。 (5 Experiments) | yilin-wu; zilin-si; zeynep-temel; et al. | 2606.14981 |
| EA-TWM-READ-0015 | EA-DATA | `support` | `direct` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 | 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。 (Abstract (full-text section)) | ralf-rmer | 2606.18043 |
| EA-TWM-READ-0001 | EA-DATA | `conditional` | `direct` | VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 | 训练数据段明确列出了同步的本体状态、外部视频与双指触觉视频数据流。 (B.0.1 Training dataset) | carolina-higuera; sergio-arnaud; byron-boots; et al. | 2602.06001 |
| EA-EGO-2026-0008 | EA-DATA | `conditional` | `direct` | 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 | 四类 checkpoint 的消融中，pretrain+midtrain 最好；human pretraining 提供结构，mid-training 负责控制锚定。 (3.2 Large-Scale Human Pretraining Is Key to Strong Dexterous Manipulation Policy Performance) | ruijie-zheng; dantong-niu; yuqi-xie; et al. | 2602.16710 |
| EA-TWM-READ-0007 | EA-DATA | `conditional` | `direct` | 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 | AT-VLA 把系统分为慢速视觉语言流和快速触觉流，慢速流负责任务理解和视觉定位，快速流以高频处理触觉反馈；作者采用 3:1 的快慢流频率比，并在真实接触丰富任务中验证 adaptive tactile injection、tactile gate、adaptive cross-attention 和 reaction dual-stream 的作用。 (5 Conclusion) | xiaoqi-li; muhe-cai; jiadong-xu; et al. | 2605.07308 |
| EA-EGO-2026-0017 | EA-DATA | `conditional` | `direct` | 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 | HOT3D ground truth 上的 10% sample 验证给出 head/wrist 三类严格阈值 recovery rate。 (4.3 Egocentric Video Yields Effective Pretraining Labels) | xingyao-lin; guojin-zhong; tianyi-lu; et al. | 2606.06194 |
| EA-EGO-2026-0018 | EA-DATA | `conditional` | `direct` | 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 | Restocking 中 egocentric-pretrained model 的 placement 为 24/27，SFT-only 为 6/27；移除 head camera 降到 1/27。 (4.4 The Head Camera Enables Pretrained Active Perception) | xingyao-lin; guojin-zhong; tianyi-lu; et al. | 2606.06194 |
| EA-TWM-READ-0014 | EA-DATA | `conditional` | `direct` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 | 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。 (Abstract (full-text section)) | shengcheng-luo | 2606.08765 |
| EA-TWM-READ-0010 | EA-DATA | `conditional` | `direct` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 | 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。 (Abstract (full-text section)) | siyu-wu; linjing-you; junjie-zhu; et al. | 2606.26663 |
| EA-TWM-READ-0011 | EA-DATA | `conditional` | `direct` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 | 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only po... | jaden-clark; changhao-wang; yihuai-gao; et al. | 2606.30988 |
| EA-EGO-2026-0020 | EA-DATA | `conditional` | `direct` | 显式 contact geometry 在该系统中显著减少滑移并提高成功率，说明接触结构是 Ego-centric 数据转成可执行监督的独立质量维度。 | 去除 hand geometry 后 object slip 变大且 success 下降，full ObjRetarget 最好。 (IV-C 1 Hand–object geometric consistency module) | yuanchuan-lai; qing-gao; ziyan-liang; et al. | 2607.03828 |
| EA-EGO-2026-0003 | EA-DATA | `limit` | `direct` | 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 | 策略训练段明确说明 gripper state 缺失，并以 object pose displacement 作为替代动作。 (III-C Policy Training) | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | 2509.21986 |
| EA-EGO-2026-0004 | EA-DATA | `limit` | `direct` | Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 | BGTS=1.0 保留 86,427 episodes 但真实机器人分数低于 BGTS=0.7 的 45,157 episodes。 (IV-C Ablation Study) | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | 2509.21986 |
| EA-EGO-2026-0009 | EA-DATA | `limit` | `direct` | Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 | 动作空间消融中 wrist-only 普遍较差，fingertip mapping 在 Cards/Bottle 等接触敏感任务不稳定。 (3.6 Hand Action Space Design for Human Pretraining) | ruijie-zheng; dantong-niu; yuqi-xie; et al. | 2602.16710 |
| EA-EGO-2026-0016 | EA-DATA | `limit` | `direct` | Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 | 方法段明确说明 current-frame wrist pose 与 first-frame camera path 的坐标差异会混合两类位移。 (3 Method) | xingyao-lin; guojin-zhong; tianyi-lu; et al. | 2606.06194 |
| EA-TWM-READ-0009 | EA-DATA | `limit` | `direct` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 | 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差... | yanan-zhou; ranpeng-qiu; yincong-chen; et al. | 2606.16690 |
| EA-EGO-2026-0019 | EA-DATA | `limit` | `direct` | Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。 | 相关工作和引言都指出现有方法多假设 object-free/weak-contact，忽略手臂与手的不同功能。 (II-B Human-to-Robot Motion Retargeting) | yuanchuan-lai; qing-gao; ziyan-liang; et al. | 2607.03828 |
| EA-TWM-READ-0012 | EA-DATA | `limit` | `direct` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 | 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。 (1 Introduction) | bowen-jing; mingxin-wang; ruiyang-hao; et al. | 2607.04234 |
| EA-TWM-READ-0013 | EA-DATA | `gap` | `direct` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 | 作者指出机器人中 World Models 越来越被用于模拟动作后果并给出 success/safety verdict，但视频生成指标如 FVD 奖励视觉真实感，却忽略世界是否对 policy actions 正确响应；他们主张作为 test oracle 的 WM 需要先通过 accreditation，并提出 L0-L4 admissibility ladder。 (Abstract (full-text section)) | christian-oefinger | 2607.07196 |
| EA-LOCOMANIP-2026-0006 | EA-MODEL | `support` | `direct` | Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the evaluated tasks. | The ablation directly compares the full model with removal of unified latent learning. (4.3 How does action-free videos contribute to loco–manipulation?) | haoran-jiang; jin-chen; qingwen-bu; et al. | 2512.11047 |
| EA-ALIGN-READ-0013 | EA-MODEL | `support` | `direct` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 | 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。 (5 Conclusion) | chi-pin-huang; yunze-man; zhiding-yu; et al. | 2601.09708 |
| EA-VLABREAK-2026-0001 | EA-MODEL | `support` | `direct` | H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 | 方法定义了逻辑世界模型、视觉世界模型、低层 VLA 和子任务完成检测的两时间尺度接口。 (IV-C Hierarchical World Model Guidance for VLA) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-VLABREAK-2026-0004 | EA-MODEL | `support` | `direct` | StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。 | 方法段给出动力学里程碑抽取和 planner-to-action 两阶段优化的完整链路。 (pages 5-8, Sections 3.1-3.3) | minghao-jin; mozheng-liao; mingfei-han; et al. | 2603.12553 |
| EA-LOCOMANIP-2026-0012 | EA-MODEL | `support` | `direct` | Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to... | The paper compares variants with the same tactile-aware high level but different low-level tactile tracking. (IV-B Experimental Results and Analyze) | pokuang-zhou; yuhao-zhou; quan-khanh-luu; et al. | 2604.27224 |
| EA-ALIGN-READ-0014 | EA-MODEL | `support` | `direct` | 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 | 引言直接将纯反应 VLA 的三类困难列为长时程推理、temporal credit assignment 与 compounding errors。 (1 Introduction) | bohan-hou; gen-li; jindou-jia; et al. | 2605.00080 |
| EA-ALIGN-READ-0012 | EA-MODEL | `support` | `direct` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 | 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。 (Abstract (full-text section)) | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | 2605.26349 |
| EA-ALIGN-READ-0015 | EA-MODEL | `support` | `direct` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 | ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classifi... | haodi-hu; chung-ta-huang; jing-liu; et al. | 2606.09630 |
| EA-ALIGN-READ-0005 | EA-MODEL | `support` | `direct` | Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. | The paper frames low-level state/action heterogeneity as a core cross-embodiment challenge, then uses dense embodied chain-of-thought supervision in the VLM stream and a flow-matching action expert that outputs continuo... | haoyang-li; guanlin-li; youhe-feng; et al. | 2606.30552 |
| EA-LOCOMANIP-2026-0021 | EA-MODEL | `support` | `direct` | In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. | The hardware baseline comparison isolates learned grasp regulation under the same command set. (6.5 Baseline comparison) | muqun-hu; yuhao-zhou; kabir-ray-malik; et al. | 2607.10132 |
| EA-VLABREAK-2026-0002 | EA-MODEL | `conditional` | `direct` | 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 | H-WM 为 64.8%，logic-only 为 48.4%，H-WM-Stable-Diffusion 为 54.4%。 (VI Results) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-ALIGN-READ-0010 | EA-MODEL | `conditional` | `direct` | ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 | 相关工作段明确提出解耦视觉部件，让 LLM 在已知感知状态上做 3D 物理与动作推理。 (II-B LLM/VLM Based Robotic Operation) | guangming-wang; qizhen-ying; yixiong-jing; et al. | 2602.21161 |
| EA-LOCOMANIP-2026-0018 | EA-MODEL | `conditional` | `direct` | On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively. | The real-world table separates external-state and onboard egocentric control modes. (V-E Real-World Deployment) | xialin-he; sirui-xu; xinyao-li; et al. | 2603.03279 |
| EA-VLABREAK-2026-0005 | EA-MODEL | `conditional` | `direct` | 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 | LIBERO 平均为 94.8%；实机 tidy-up 为 8/10，相同表面的 UniVLA 为 4/10。 (page 11) | minghao-jin; mozheng-liao; mingfei-han; et al. | 2603.12553 |
| EA-ALIGN-READ-0011 | EA-MODEL | `conditional` | `direct` | τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 | 摘要直接列出四类交互数据和 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-ALIGN-READ-0006 | EA-MODEL | `conditional` | `direct` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 | 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。 (Abstract (full-text section)) | nan-sun; yuan-zhang; yongkun-yang; et al. | 2606.03784 |
| EA-ALIGN-READ-0007 | EA-MODEL | `conditional` | `direct` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 | 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。 (3.2 Synchronization and Data Quality Control) | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-ALIGN-READ-0008 | EA-MODEL | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-ALIGN-READ-0002 | EA-MODEL | `conditional` | `direct` | A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. | SSI-Policy builds an RGB-only structured scene interface encoding monocular depth features, language-grounded layouts, and instruction-conditioned 2D motion trajectories; it reports few-shot gains but notes failures fro... | kaijun-wang; zikai-ouyang; xuping-wu; et al. | 2606.26800 |
| EA-VLABREAK-2026-0003 | EA-MODEL | `limit` | `direct` | H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 | 结论明确列出额外组件/训练阶段的代价，以及对符号化状态的依赖。 (VII Conclusion) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-ALIGN-READ-0001 | EA-MODEL | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-ALIGN-READ-0003 | EA-MODEL | `limit` | `direct` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same to... | SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines. (Abstract (full-text section)) | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | 2606.30113 |
| EA-ALIGN-READ-0004 | EA-MODEL | `limit` | `direct` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset c... | The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone. (Abstract (full-text section... | mathilde-hochedel; marc-lalonde | 2606.30456 |
| EA-ALIGN-READ-0009 | EA-MODEL | `limit` | `direct` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 | 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。 (5 Conclusion and Limitations) | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |
| EA-VLABREAK-2026-0006 | EA-MODEL | `limit` | `direct` | 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 | 主实验在 40 个 LIBERO 任务、每任务 20 次试验上使用闭环攻击，并报告任务族级下降。 (5.2 BadWAM Reliably Induces Task Failures) | qi-li; xingyi-yang; xinchao-wang | 2607.15207 |
| EA-VLABREAK-2026-0007 | EA-MODEL | `limit` | `direct` | 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 | 想象保持攻击在 40 个任务中有 39 个降低未来漂移，同时保留显著攻击强度。 (5.8 What Do These Results Imply for WAM Safety?) | qi-li; xingyi-yang; xinchao-wang | 2607.15207 |
| EA-SENSORERR-READ-0010 | EA-SENSOR | `support` | `direct` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 | 作者明确指出视觉位姿估计常在遮挡、差光照、反光或透明表面下失败，并提出 tactile-only pose estimation：把触觉接触表示成局部 3D 点云，结合校准传感器位姿恢复完整 6-DoF object pose；实验在视觉不可靠时优于视觉和几何基线。 (Abstract (full-text section)) | pengfei-ye; yuxiang-ma; haonan-chen; et al. | 2606.28899 |
| EA-SENSORERR-READ-0011 | EA-SENSOR | `support` | `direct` | RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 | 作者指出现有 VLA 往往假设稳定明亮的室内环境，而真实操作中 illumination shifts 会造成 degraded RGB observations；Event-VLA 将 degraded visibility 定义为 RGB-centric policies 的鲁棒性问题，并通过 action-query routing 将 event streams 融入 action representation，仿真和真实部署... | jiaxin-liu; xun-xu; zhenhao-zhang; et al. | 2606.29384 |
| EA-SENSORERR-READ-0012 | EA-SENSOR | `support` | `direct` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 | 作者把日常灵巧操作的误差来源明确落在滑移、错位、不稳定抓取和力不匹配上，并指出视觉/语言不能可靠揭示力、滑移和接触稳定性；其分层策略将视觉语言子任务规划、触觉世界模型预测和高频触觉残差修正分开。 (Abstract (full-text section)) | jianyi-zhou; feiyang-hong; yunhao-li; et al. | 2607.07287 |
| EA-SENSORERR-READ-0007 | EA-SENSOR | `conditional` | `direct` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 | 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。 (Abstract (full-text section)) | shengcheng-luo | 2606.08765 |
| EA-SENSORERR-READ-0004 | EA-SENSOR | `conditional` | `direct` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 | 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only po... | jaden-clark; changhao-wang; yihuai-gao; et al. | 2606.30988 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-EGO-2026-0007 | ruijie-zheng; dantong-niu; yuqi-xie; et al. | unlisted | `support` | 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 |
| EA-TWM-READ-0008 | longyan-wu; jieji-ren; chenghang-jiang; et al. | unlisted | `support` | TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 |
| EA-TWM-READ-0005 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `support` | 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 |
| EA-TWM-READ-0002 | yunfan-lou; yifan-ye; yankai-fu; et al. | unlisted | `support` | 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 |
| EA-TWM-READ-0006 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `support` | 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 |
| EA-TWM-READ-0003 | zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al. | unlisted | `support` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 |
| EA-TWM-READ-0004 | yilin-wu; zilin-si; zeynep-temel; et al. | unlisted | `support` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 |
| EA-TWM-READ-0015 | ralf-rmer | unlisted | `support` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 |
| EA-TWM-READ-0001 | carolina-higuera; sergio-arnaud; byron-boots; et al. | unlisted | `conditional` | VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 |
| EA-EGO-2026-0008 | ruijie-zheng; dantong-niu; yuqi-xie; et al. | unlisted | `conditional` | 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 |
| EA-TWM-READ-0007 | xiaoqi-li; muhe-cai; jiadong-xu; et al. | unlisted | `conditional` | 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 |
| EA-EGO-2026-0017 | xingyao-lin; guojin-zhong; tianyi-lu; et al. | unlisted | `conditional` | 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 |
| EA-EGO-2026-0018 | xingyao-lin; guojin-zhong; tianyi-lu; et al. | unlisted | `conditional` | 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 |
| EA-TWM-READ-0014 | shengcheng-luo | unlisted | `conditional` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 |
| EA-TWM-READ-0010 | siyu-wu; linjing-you; junjie-zhu; et al. | unlisted | `conditional` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 |
| EA-TWM-READ-0011 | jaden-clark; changhao-wang; yihuai-gao; et al. | unlisted | `conditional` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 |
| EA-EGO-2026-0020 | yuanchuan-lai; qing-gao; ziyan-liang; et al. | unlisted | `conditional` | 显式 contact geometry 在该系统中显著减少滑移并提高成功率，说明接触结构是 Ego-centric 数据转成可执行监督的独立质量维度。 |
| EA-EGO-2026-0003 | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | unlisted | `limit` | 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 |
| EA-EGO-2026-0004 | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | unlisted | `limit` | Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 |
| EA-EGO-2026-0009 | ruijie-zheng; dantong-niu; yuqi-xie; et al. | unlisted | `limit` | Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 |
| EA-EGO-2026-0016 | xingyao-lin; guojin-zhong; tianyi-lu; et al. | unlisted | `limit` | Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 |
| EA-TWM-READ-0009 | yanan-zhou; ranpeng-qiu; yincong-chen; et al. | unlisted | `limit` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 |
| EA-EGO-2026-0019 | yuanchuan-lai; qing-gao; ziyan-liang; et al. | unlisted | `limit` | Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。 |
| EA-TWM-READ-0012 | bowen-jing; mingxin-wang; ruiyang-hao; et al. | unlisted | `limit` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 |
| EA-TWM-READ-0013 | christian-oefinger | unlisted | `gap` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 |
| EA-LOCOMANIP-2026-0006 | haoran-jiang; jin-chen; qingwen-bu; et al. | unlisted | `support` | Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the ev... |
| EA-ALIGN-READ-0013 | chi-pin-huang; yunze-man; zhiding-yu; et al. | unlisted | `support` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 |
| EA-VLABREAK-2026-0001 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `support` | H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 |
| EA-VLABREAK-2026-0004 | minghao-jin; mozheng-liao; mingfei-han; et al. | unlisted | `support` | StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。 |
| EA-LOCOMANIP-2026-0012 | pokuang-zhou; yuhao-zhou; quan-khanh-luu; et al. | unlisted | `support` | Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tig... |
| EA-ALIGN-READ-0014 | bohan-hou; gen-li; jindou-jia; et al. | unlisted | `support` | 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 |
| EA-ALIGN-READ-0012 | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | unlisted | `support` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 |
| EA-ALIGN-READ-0015 | haodi-hu; chung-ta-huang; jing-liu; et al. | unlisted | `support` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 |
| EA-ALIGN-READ-0005 | haoyang-li; guanlin-li; youhe-feng; et al. | unlisted | `support` | Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action s... |
| EA-LOCOMANIP-2026-0021 | muqun-hu; yuhao-zhou; kabir-ray-malik; et al. | unlisted | `support` | In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. |
| EA-VLABREAK-2026-0002 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `conditional` | 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 |
| EA-ALIGN-READ-0010 | guangming-wang; qizhen-ying; yixiong-jing; et al. | unlisted | `conditional` | ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 |
| EA-LOCOMANIP-2026-0018 | xialin-he; sirui-xu; xinyao-li; et al. | unlisted | `conditional` | On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively. |
| EA-VLABREAK-2026-0005 | minghao-jin; mozheng-liao; mingfei-han; et al. | unlisted | `conditional` | 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 |
| EA-ALIGN-READ-0011 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `conditional` | τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 |
| EA-ALIGN-READ-0006 | nan-sun; yuan-zhang; yongkun-yang; et al. | unlisted | `conditional` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 |
| EA-ALIGN-READ-0007 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `conditional` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 |
| EA-ALIGN-READ-0008 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-ALIGN-READ-0002 | kaijun-wang; zikai-ouyang; xuping-wu; et al. | unlisted | `conditional` | A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action con... |
| EA-VLABREAK-2026-0003 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `limit` | H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 |
| EA-ALIGN-READ-0001 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-ALIGN-READ-0003 | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | unlisted | `limit` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottlen... |
| EA-ALIGN-READ-0004 | mathilde-hochedel; marc-lalonde | unlisted | `limit` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preproce... |
| EA-ALIGN-READ-0009 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 |
| EA-VLABREAK-2026-0006 | qi-li; xingyi-yang; xinchao-wang | unlisted | `limit` | 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 |
| EA-VLABREAK-2026-0007 | qi-li; xingyi-yang; xinchao-wang | unlisted | `limit` | 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 |
| EA-SENSORERR-READ-0010 | pengfei-ye; yuxiang-ma; haonan-chen; et al. | unlisted | `support` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 |
| EA-SENSORERR-READ-0011 | jiaxin-liu; xun-xu; zhenhao-zhang; et al. | unlisted | `support` | RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 |
| EA-SENSORERR-READ-0012 | jianyi-zhou; feiyang-hong; yunhao-li; et al. | unlisted | `support` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 |
| EA-SENSORERR-READ-0007 | shengcheng-luo | unlisted | `conditional` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 |
| EA-SENSORERR-READ-0004 | jaden-clark; changhao-wang; yihuai-gao; et al. | unlisted | `conditional` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 |

## Synthesis Slots

### 共识/正向证据
- `EA-EGO-2026-0007`: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。
- `EA-TWM-READ-0008`: TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。
- `EA-TWM-READ-0005`: 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
- `EA-TWM-READ-0002`: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
- `EA-TWM-READ-0006`: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。
- `EA-TWM-READ-0003`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- `EA-TWM-READ-0004`: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。
- `EA-TWM-READ-0015`: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
### 条件成立
- `EA-TWM-READ-0001`: VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。
- `EA-EGO-2026-0008`: 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。
- `EA-TWM-READ-0007`: 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。
- `EA-EGO-2026-0017`: 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。
- `EA-EGO-2026-0018`: 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。
- `EA-TWM-READ-0014`: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- `EA-TWM-READ-0010`: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- `EA-TWM-READ-0011`: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
### 限制与失败模式
- `EA-EGO-2026-0003`: 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。
- `EA-EGO-2026-0004`: Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。
- `EA-EGO-2026-0009`: Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。
- `EA-EGO-2026-0016`: Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。
- `EA-TWM-READ-0009`: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- `EA-EGO-2026-0019`: Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。
- `EA-TWM-READ-0012`: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- `EA-VLABREAK-2026-0003`: H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。
### 开放问题
- `EA-TWM-READ-0013`: 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 42 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-EGO-2026-0007` 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。
  - `EA-TWM-READ-0008` TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。
  - `EA-TWM-READ-0005` 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
- Scientific memo preview: 《近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进: 先看证据边界，再谈一个可传播的反常识洞察。

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
