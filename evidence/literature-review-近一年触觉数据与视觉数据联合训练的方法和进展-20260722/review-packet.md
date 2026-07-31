# Review Packet: 近一年触觉数据与视觉数据联合训练的方法和进展

## Scope

- Topic: 近一年触觉数据与视觉数据联合训练的方法和进展
- Time range: 2025-07-22..2026-07-22
- Review style: `survey`
- Knowledge IDs: `EA-SENSOR`, `EA-ALIGN`, `EA-MODEL`, `EA-DATA`, `EA-XEMBODIMENT`
- Evidence events: 30
- Topic cards: 5
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 30
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-TWM-READ-0008`, `EA-TWM-READ-0005`, `EA-TWM-READ-0002`, `EA-TWM-READ-0006`, `EA-TWM-READ-0003`, `EA-TWM-READ-0004`, `EA-TWM-READ-0015`, `EA-UMI-READ-0015`, `EA-UMI-READ-0002`, `EA-TWM-READ-0001`, `EA-TWM-READ-0007`, `EA-TWM-READ-0014`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 27 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 27
- Structure mapped: 27
- Deep-read papers: 27
- Claim-verified papers: 27
- Accepted evidence papers: 27
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；腕部六维力/力矩提供低维全局载荷，触觉提供高维局部接触场，两者不能互换。最新综合更支持按功能和时标选择性耦合：视觉/语言负责慢速全局语义与计划，触觉/力觉进入快速接触反馈，动作条件世界模型负责预测与验证。目标不是堆传感器，而是形成“同步数据—接触表征—动作条件预测—高频纠偏—安全过程评测”的接触执行栈，并证明每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-ALIGN` VLA 多模态与动作对齐: VLA 对齐的核心不是把语言、视觉和动作都变成 token，而是处理多种信号的粒度、功能、频率和物理语义错配：语言通常任务级且稀疏，视觉高维稠密，动作连续且受本体/控制器约束，触觉与力觉则在接触后进入更快的反馈环。可靠系统需要把低频逻辑与视觉子目标、高频 VLA 执行、机器人特定控制器和接触反馈分层连接，并用动作条件状态变化作为共享接口。动作表示应以物理状态变化和可执行性为中心，而不是以模型输出方便为中心。
  - 稠密 visual-action 监督可能压过稀疏 language-action 信号，使语言退化为装饰性条件。
  - 阶段级语言、dense reasoning 或独立 language-action pretraining 可以增强语言对动作的约束，但会引入新的标注和误差传播问题。
  - 视觉不是越稠密越好；应通过 task-space action、结构化场景接口、affordance 或轨迹监督组织成动作相关表示。
  - 离散 action token 便于接入自回归模型，但解码到连续控制时必须条件化机器人状态、本体、接触和控制器。
  - VLA 可以继承视觉与语言先验，却不会自动继承连续运动先验；action prior 或 flow/diffusion action expert 可独立预训练。
- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型、本体适配器与底层控制器组成的融合栈。近期突破不只是生成更长视频，而是把未来压缩成低频逻辑步骤、稀疏视觉子目标或结构化状态，并验证它与真实动作同步；BadWAM 说明“想象合理、动作错误”足以让系统失效。世界模型应先承担训练期教师、离线排序等低权限任务，再逐级争取在线规划权。Loco-manipulation 与多模态证据还表明，完整动作接口及按功能/时标分层的接触反馈会限制能力上限。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；数据污染则是来源、时间、任务、模型版本和评测边界的关系失真，治理必须贯穿采集、训练、生成和闭环评测。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。对视觉—触觉—力觉数据，同时间戳帧只是最低层记录，真正的训练单元还应保留 approach、contact、slip、release、recovery 等事件链，并记录传感器/硬件 ID、时钟、标定和换件历史。所有异构数据都应声明可信监督字段，以动作条件状态变化和真实闭环收益验收；规模化触觉数据不自动等于跨硬件通用性或...
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- `EA-XEMBODIMENT` 跨本体与数据迁移: 跨本体迁移的核心不是复制姿态、控制命令或传感器 token，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。语言/视觉语义、对象状态变化和粗运动先验较易共享；局部接触载荷、传感器频率、硬件标定和控制接口更依赖目标平台。更稳健的路线是共享 Cartesian/object state delta 或接触目标，再由机器人和传感器特定 adapter、少量目标硬件数据与真实闭环校准落地。
  - 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
  - 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
  - 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
  - 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
  - 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 17 |
| `conditional` | 条件成立 | 7 |
| `limit` | 限制/负面 | 5 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2601.09988: In-the-Wild Compliant Manipulation with UMI-FT | 2026-01-15 | conditional | EA-UMI-READ-0002 |
| 2602.06001: Visuo-Tactile World Models | 2026-02-05 | conditional | EA-TWM-READ-0001 |
| 2603.15257: HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing | 2026-03-16T13:24:58Z | conditional | EA-VTTRAIN-2026-0002 |
| 2603.19201: OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation | 2026-03-19T17:52:42Z | support | EA-VTTRAIN-2026-0003; EA-VTTRAIN-2026-0004 |
| 2604.07335: TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks | 2026-04-08 | support | EA-TWM-READ-0008 |
| 2604.27224: Learning Tactile-Aware Quadrupedal Loco-Manipulation Policies | 2026-04-29T21:46:58Z | support | EA-LOCOMANIP-2026-0012 |
| 2605.07308: AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models | 2026-05-08 | conditional | EA-TWM-READ-0007 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | support | EA-TWM-READ-0005 |
| 2606.08737: Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation | 2026-06-07 | support | EA-TWM-READ-0002 |
| 2606.08765: RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation | 2026-06-07 | conditional | EA-TWM-READ-0014 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | support | EA-TWM-READ-0006 |
| 2606.13877: ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation | 2026-06-11 | support | EA-TWM-READ-0003 |
| 2606.14981: Inference-time Policy Steering via Vision and Touch | 2026-06-12 | support | EA-TWM-READ-0004 |
| 2606.16690: PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation | 2026-06-15 | limit | EA-TWM-READ-0009 |
| 2606.18043: Uncertainty Quantification for Flow-Based Vision-Language-Action Models | 2026-06-16 | support | EA-TWM-READ-0015 |
| 2606.19161: HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision | 2026-06-17 | limit, support | EA-TACTILE-2026-0001; EA-TACTILE-2026-0002 |
| 2606.26663: Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention | 2026-06-25 | conditional | EA-TWM-READ-0010 |
| 2606.28899: You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact | 2026-06-27 | support | EA-SENSORERR-READ-0010 |
| 2606.30988: Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force | 2026-06-29 | conditional | EA-TWM-READ-0011 |
| 2606.31694: RCT: A Robot-Collected Touch-Vision-Language Dataset for Tactile Generalization | 2026-06-30T14:05:33Z | limit, support | EA-VTTRAIN-2026-0005; EA-VTTRAIN-2026-0006 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-SENSORERR-READ-0001 |
| 2607.04234: SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objec... | 2026-07-05 | limit | EA-TWM-READ-0012 |
| 2607.05390: Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | support | EA-UMI-READ-0015 |
| 2607.07196: Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators | 2026-07-08 | gap | EA-TWM-READ-0013 |
| 2607.07287: TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation | 2026-07-08 | support | EA-SENSORERR-READ-0012 |
| 2607.10132: TAC-LOCO: Unified Whole-Body Control for Quadrupedal TACtile-Informed LOCO-Manipulation | 2026-07-11T05:45:24Z | support | EA-LOCOMANIP-2026-0021 |
| 2607.14609: Representation-Aligned Tactile Grounding for Contact-Rich Robotic Manipulation | 2026-07-16T06:12:05Z | support | EA-VTTRAIN-2026-0001 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-TWM-READ-0008 | EA-DATA | `support` | `direct` | TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 | 摘要明确列出精度/便携双模式采集、触觉恢复遥操作和人在环恢复数据。 (Abstract (full-text section)) | longyan-wu; jieji-ren; chenghang-jiang; et al. | 2604.07335 |
| EA-TWM-READ-0005 | EA-DATA | `support` | `direct` | 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 | HapTile 的每个夹爪手指安装视觉触觉传感器，接触会带来图像变化和 marker displacement；论文把 marker-motion 信号保存进数据集并用于 haptic feedback，实验也比较 vision-only、vision+tactile image 与 vision+tactile+marker 表征。 (4.2 Vision-Based Tactile Sensing and Marker Track... | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-TWM-READ-0002 | EA-DATA | `support` | `direct` | 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 | Dream-Tac 把 world action model 扩展到触觉，联合建模当前视觉、触觉、语言指令下的未来视觉观测、未来触觉观测和动作 chunk，并加入 contact-gated visuotactile fusion 与 contact-aware attention bias。 (Abstract (full-text section)) | yunfan-lou; yifan-ye; yankai-fu; et al. | 2606.08737 |
| EA-TWM-READ-0006 | EA-DATA | `support` | `direct` | 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 | TacForeSight 的 TacForceWM 从双指触觉观测出发，以高频腕部 force/torque 为条件预测短时域触觉 latent dynamics；ablation 中 wrist wrench 条件的未来触觉预测优于无条件版本，MSE 从 0.027 降到 0.017，cosine 从 0.954 提升到 0.992。 (IV-D 1 World Model Conditioning) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-TWM-READ-0003 | EA-DATA | `support` | `direct` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 | ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。 (Abstract (full-text section)) | zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al. | 2606.13877 |
| EA-TWM-READ-0004 | EA-DATA | `support` | `direct` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 | ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。 (5 Experiments) | yilin-wu; zilin-si; zeynep-temel; et al. | 2606.14981 |
| EA-TWM-READ-0015 | EA-DATA | `support` | `direct` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 | 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。 (Abstract (full-text section)) | ralf-rmer | 2606.18043 |
| EA-UMI-READ-0015 | EA-DATA | `support` | `direct` | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | 论文认为形变物体有高维状态和复杂材料属性，接触诱发的局部形变常被末端执行器或物体遮挡；已有数据集常缺对象多样性、依赖合成数据，或缺高保真标注与接触形变。Deform360 采集 198 个日常物体、1,980 个交互序列、215 小时以上数据、41 个环视相机和双臂触觉 UMI gripper，并用 markerless 3D tracking 提取稠密几何与运动。 (Abstract (full-text section)) | hongyu-li; wanjia-fu; xiaoyan-cong; et al. | 2607.05390 |
| EA-UMI-READ-0002 | EA-DATA | `conditional` | `direct` | UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision... | The HTML full text reports that UMI-FT mounts compact six-axis force/torque sensors on each finger, uses multimodal demonstrations to train adaptive compliance policies, and shows diverse in-the-wild data outperforming... | hojung-choi; yifan-hou; chuer-pan; et al. | 2601.09988 |
| EA-TWM-READ-0001 | EA-DATA | `conditional` | `direct` | VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 | 训练数据段明确列出了同步的本体状态、外部视频与双指触觉视频数据流。 (B.0.1 Training dataset) | carolina-higuera; sergio-arnaud; byron-boots; et al. | 2602.06001 |
| EA-TWM-READ-0007 | EA-DATA | `conditional` | `direct` | 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 | AT-VLA 把系统分为慢速视觉语言流和快速触觉流，慢速流负责任务理解和视觉定位，快速流以高频处理触觉反馈；作者采用 3:1 的快慢流频率比，并在真实接触丰富任务中验证 adaptive tactile injection、tactile gate、adaptive cross-attention 和 reaction dual-stream 的作用。 (5 Conclusion) | xiaoqi-li; muhe-cai; jiadong-xu; et al. | 2605.07308 |
| EA-TWM-READ-0014 | EA-DATA | `conditional` | `direct` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 | 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。 (Abstract (full-text section)) | shengcheng-luo | 2606.08765 |
| EA-TWM-READ-0010 | EA-DATA | `conditional` | `direct` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 | 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。 (Abstract (full-text section)) | siyu-wu; linjing-you; junjie-zhu; et al. | 2606.26663 |
| EA-TWM-READ-0011 | EA-DATA | `conditional` | `direct` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 | 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only po... | jaden-clark; changhao-wang; yihuai-gao; et al. | 2606.30988 |
| EA-TWM-READ-0009 | EA-DATA | `limit` | `direct` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 | 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差... | yanan-zhou; ranpeng-qiu; yincong-chen; et al. | 2606.16690 |
| EA-TWM-READ-0012 | EA-DATA | `limit` | `direct` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 | 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。 (1 Introduction) | bowen-jing; mingxin-wang; ruiyang-hao; et al. | 2607.04234 |
| EA-TWM-READ-0013 | EA-DATA | `gap` | `direct` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 | 作者指出机器人中 World Models 越来越被用于模拟动作后果并给出 success/safety verdict，但视频生成指标如 FVD 奖励视觉真实感，却忽略世界是否对 policy actions 正确响应；他们主张作为 test oracle 的 WM 需要先通过 accreditation，并提出 L0-L4 admissibility ladder。 (Abstract (full-text section)) | christian-oefinger | 2607.07196 |
| EA-LOCOMANIP-2026-0012 | EA-MODEL | `support` | `direct` | Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to... | The paper compares variants with the same tactile-aware high level but different low-level tactile tracking. (IV-B Experimental Results and Analyze) | pokuang-zhou; yuhao-zhou; quan-khanh-luu; et al. | 2604.27224 |
| EA-LOCOMANIP-2026-0021 | EA-MODEL | `support` | `direct` | In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. | The hardware baseline comparison isolates learned grasp regulation under the same command set. (6.5 Baseline comparison) | muqun-hu; yuhao-zhou; kabir-ray-malik; et al. | 2607.10132 |
| EA-VTTRAIN-2026-0003 | EA-SENSOR | `support` | `direct` | OmniViTac 将视觉—触觉—动作联合训练的数据底座扩展到 21,879 条轨迹、86 个任务和 126 个物体，覆盖六类接触交互模式。 | Table I 报告任务、轨迹、物体、视觉、触觉和采集设置的规模。 (III-A 2 Dual-Embodiment Data Collection) | yuhang-zheng; songen-gu; weize-li; et al. | 2603.19201 |
| EA-VTTRAIN-2026-0004 | EA-SENSOR | `support` | `direct` | 在 OmniVTA 的真实机器人评测中，60 Hz 触觉反射闭环相对移除该控制器的开放环版本，把擦拭成功率从 0.66 提到 0.80、切割从 0.50 提到 0.85；预测触觉只有连接到快速纠偏才形成完整控制收益。 | Table III 的 object-diversity 列隔离了移除 RLTC 的开放环变体，两个代表任务均显著提升。 (V-B Overall Performance) | yuhang-zheng; songen-gu; weize-li; et al. | 2603.19201 |
| EA-TACTILE-2026-0001 | EA-SENSOR | `support` | `direct` | 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 | 摘要和基准设计章节直接给出数据规模、四项评测任务与任务级 OOD 划分。 (Abstract; 3 HT-Bench: A Multi-Task Tactile Evaluation Benchmark) | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | 2606.19161 |
| EA-SENSORERR-READ-0010 | EA-SENSOR | `support` | `direct` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 | 作者明确指出视觉位姿估计常在遮挡、差光照、反光或透明表面下失败，并提出 tactile-only pose estimation：把触觉接触表示成局部 3D 点云，结合校准传感器位姿恢复完整 6-DoF object pose；实验在视觉不可靠时优于视觉和几何基线。 (Abstract (full-text section)) | pengfei-ye; yuxiang-ma; haonan-chen; et al. | 2606.28899 |
| EA-VTTRAIN-2026-0006 | EA-SENSOR | `support` | `direct` | 在相同 held-out-contact-sequence 测试池上，沿一次按压从浅到深均匀取 5 帧只用 7,055 个训练帧，却把触觉—文本 Recall@1 提到 68.18%，高于使用 22,576 帧完整按压的 62.44% 和只取最深 5 帧的 59.52%。 | Uniform5 在相同测试池和模型配方下以更少帧取得更高检索性能。 (5 Experimental Evaluation, Table 5) | jingbo-he; michael-frber; roberto-calandra | 2606.31694 |
| EA-SENSORERR-READ-0012 | EA-SENSOR | `support` | `direct` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 | 作者把日常灵巧操作的误差来源明确落在滑移、错位、不稳定抓取和力不匹配上，并指出视觉/语言不能可靠揭示力、滑移和接触稳定性；其分层策略将视觉语言子任务规划、触觉世界模型预测和高频触觉残差修正分开。 (Abstract (full-text section)) | jianyi-zhou; feiyang-hong; yunhao-li; et al. | 2607.07287 |
| EA-VTTRAIN-2026-0001 | EA-SENSOR | `support` | `direct` | 在五项真实接触操作中，把未来触觉 latent 监督施加到动作专家中间层取得 74% 平均成功率，高于 VLM 侧的 58% 和最终动作态的 62%；联合训练的收益取决于监督接口是否与动作条件接触动力学对齐。 | 同一触觉条件 VLA 下的接口控制比较表明，中间动作专家表示优于感知侧和最终动作侧。 (4.2 Main Results) | ruilin-chen; jingkai-jia; tong-yang; et al. | 2607.14609 |
| EA-VTTRAIN-2026-0002 | EA-SENSOR | `conditional` | `direct` | 触觉可以作为训练期 teacher 和安全奖励的监督，再蒸馏进只使用视觉与本体状态的部署 VLA；在三项易损物体任务、每项 20 次测试中，该无触觉 student 达到 86.7% 平均成功率。 | Tactile Distillation 将触觉条件 teacher 的动作目标与真实示教混合训练 student，Table I 报告三任务平均成功率。 (V CONCLUSION) | konstantin-gubernatorov; mikhail-sannikov; ilya-mikhalchuk; et al. | 2603.15257 |
| EA-TACTILE-2026-0002 | EA-SENSOR | `limit` | `direct` | HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 | 作者在限制章节明确列出硬件/本体覆盖和闭环下游评测缺失。 (6 Limitations and Future Work) | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | 2606.19161 |
| EA-VTTRAIN-2026-0005 | EA-SENSOR | `limit` | `direct` | 视觉—触觉表示训练不能把单帧当独立数据单元：同一次机器人按压的相邻帧是近重复观测，frame-random 切分会把物理交互泄漏到训练和测试，因此至少应按 contact sequence、最好再按材料或传感器实例做 holdout。 | RCT 与 TVL/HCT 审计都显示同一按压序列可同时出现在训练和测试，原始像素近邻也能利用该结构。 (4 Evaluation Protocol) | jingbo-he; michael-frber; roberto-calandra | 2606.31694 |
| EA-SENSORERR-READ-0001 | EA-SENSOR | `limit` | `direct` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 | 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。 (5 Conclusion and Limitations) | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-TWM-READ-0008 | longyan-wu; jieji-ren; chenghang-jiang; et al. | unlisted | `support` | TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 |
| EA-TWM-READ-0005 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `support` | 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 |
| EA-TWM-READ-0002 | yunfan-lou; yifan-ye; yankai-fu; et al. | unlisted | `support` | 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 |
| EA-TWM-READ-0006 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `support` | 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 |
| EA-TWM-READ-0003 | zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al. | unlisted | `support` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 |
| EA-TWM-READ-0004 | yilin-wu; zilin-si; zeynep-temel; et al. | unlisted | `support` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 |
| EA-TWM-READ-0015 | ralf-rmer | unlisted | `support` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 |
| EA-UMI-READ-0015 | hongyu-li; wanjia-fu; xiaoyan-cong; et al. | unlisted | `support` | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 |
| EA-UMI-READ-0002 | hojung-choi; yifan-hou; chuer-pan; et al. | unlisted | `conditional` | UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also... |
| EA-TWM-READ-0001 | carolina-higuera; sergio-arnaud; byron-boots; et al. | unlisted | `conditional` | VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 |
| EA-TWM-READ-0007 | xiaoqi-li; muhe-cai; jiadong-xu; et al. | unlisted | `conditional` | 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 |
| EA-TWM-READ-0014 | shengcheng-luo | unlisted | `conditional` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 |
| EA-TWM-READ-0010 | siyu-wu; linjing-you; junjie-zhu; et al. | unlisted | `conditional` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 |
| EA-TWM-READ-0011 | jaden-clark; changhao-wang; yihuai-gao; et al. | unlisted | `conditional` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 |
| EA-TWM-READ-0009 | yanan-zhou; ranpeng-qiu; yincong-chen; et al. | unlisted | `limit` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 |
| EA-TWM-READ-0012 | bowen-jing; mingxin-wang; ruiyang-hao; et al. | unlisted | `limit` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 |
| EA-TWM-READ-0013 | christian-oefinger | unlisted | `gap` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 |
| EA-LOCOMANIP-2026-0012 | pokuang-zhou; yuhao-zhou; quan-khanh-luu; et al. | unlisted | `support` | Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tig... |
| EA-LOCOMANIP-2026-0021 | muqun-hu; yuhao-zhou; kabir-ray-malik; et al. | unlisted | `support` | In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. |
| EA-VTTRAIN-2026-0003 | yuhang-zheng; songen-gu; weize-li; et al. | unlisted | `support` | OmniViTac 将视觉—触觉—动作联合训练的数据底座扩展到 21,879 条轨迹、86 个任务和 126 个物体，覆盖六类接触交互模式。 |
| EA-VTTRAIN-2026-0004 | yuhang-zheng; songen-gu; weize-li; et al. | unlisted | `support` | 在 OmniVTA 的真实机器人评测中，60 Hz 触觉反射闭环相对移除该控制器的开放环版本，把擦拭成功率从 0.66 提到 0.80、切割从 0.50 提到 0.85；预测触觉只有连接到快速纠偏才形成完整控制收益。 |
| EA-TACTILE-2026-0001 | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | unlisted | `support` | 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 |
| EA-SENSORERR-READ-0010 | pengfei-ye; yuxiang-ma; haonan-chen; et al. | unlisted | `support` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 |
| EA-VTTRAIN-2026-0006 | jingbo-he; michael-frber; roberto-calandra | unlisted | `support` | 在相同 held-out-contact-sequence 测试池上，沿一次按压从浅到深均匀取 5 帧只用 7,055 个训练帧，却把触觉—文本 Recall@1 提到 68.18%，高于使用 22,576 帧完整按压的 62.44% 和只取最深 5 帧的 59.52%。 |
| EA-SENSORERR-READ-0012 | jianyi-zhou; feiyang-hong; yunhao-li; et al. | unlisted | `support` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 |
| EA-VTTRAIN-2026-0001 | ruilin-chen; jingkai-jia; tong-yang; et al. | unlisted | `support` | 在五项真实接触操作中，把未来触觉 latent 监督施加到动作专家中间层取得 74% 平均成功率，高于 VLM 侧的 58% 和最终动作态的 62%；联合训练的收益取决于监督接口是否与动作条件接触动力学对齐。 |
| EA-VTTRAIN-2026-0002 | konstantin-gubernatorov; mikhail-sannikov; ilya-mikhalchuk; et al. | unlisted | `conditional` | 触觉可以作为训练期 teacher 和安全奖励的监督，再蒸馏进只使用视觉与本体状态的部署 VLA；在三项易损物体任务、每项 20 次测试中，该无触觉 student 达到 86.7% 平均成功率。 |
| EA-TACTILE-2026-0002 | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | unlisted | `limit` | HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 |
| EA-VTTRAIN-2026-0005 | jingbo-he; michael-frber; roberto-calandra | unlisted | `limit` | 视觉—触觉表示训练不能把单帧当独立数据单元：同一次机器人按压的相邻帧是近重复观测，frame-random 切分会把物理交互泄漏到训练和测试，因此至少应按 contact sequence、最好再按材料或传感器实例做 holdout。 |
| EA-SENSORERR-READ-0001 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 |

## Synthesis Slots

### 共识/正向证据
- `EA-TWM-READ-0008`: TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。
- `EA-TWM-READ-0005`: 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
- `EA-TWM-READ-0002`: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
- `EA-TWM-READ-0006`: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。
- `EA-TWM-READ-0003`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- `EA-TWM-READ-0004`: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。
- `EA-TWM-READ-0015`: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
- `EA-UMI-READ-0015`: 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。
### 条件成立
- `EA-UMI-READ-0002`: UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only data is insufficient fo...
- `EA-TWM-READ-0001`: VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。
- `EA-TWM-READ-0007`: 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。
- `EA-TWM-READ-0014`: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- `EA-TWM-READ-0010`: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- `EA-TWM-READ-0011`: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
- `EA-VTTRAIN-2026-0002`: 触觉可以作为训练期 teacher 和安全奖励的监督，再蒸馏进只使用视觉与本体状态的部署 VLA；在三项易损物体任务、每项 20 次测试中，该无触觉 student 达到 86.7% 平均成功率。
### 限制与失败模式
- `EA-TWM-READ-0009`: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- `EA-TWM-READ-0012`: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- `EA-TACTILE-2026-0002`: HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。
- `EA-VTTRAIN-2026-0005`: 视觉—触觉表示训练不能把单帧当独立数据单元：同一次机器人按压的相邻帧是近重复观测，frame-random 切分会把物理交互泄漏到训练和测试，因此至少应按 contact sequence、最好再按材料或传感器实例做 holdout。
- `EA-SENSORERR-READ-0001`: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
### 开放问题
- `EA-TWM-READ-0013`: 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 27 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-TWM-READ-0008` TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。
  - `EA-TWM-READ-0005` 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
  - `EA-TWM-READ-0002` 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
- Scientific memo preview: 《近一年触觉数据与视觉数据联合训练的方法和进展》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年触觉数据与视觉数据联合训练的方法和进展 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年触觉数据与视觉数据联合训练的方法和进展: 先看证据边界，再谈一个可传播的反常识洞察。

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
