# Review Packet: 近一年 ego-centric 数据中手部检测与追踪的问题和难点

## Scope

- Topic: 近一年 ego-centric 数据中手部检测与追踪的问题和难点
- Time range: 2025-07-29 至 2026-07-29
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-4D`
- Evidence events: 29
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 29
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-EGOHAND-2026-0007`, `EA-EGOHAND-2026-0009`, `EA-EGOHAND-2026-0018`, `EA-EGOHAND-2026-0020`, `EA-EGOHAND-2026-0026`, `EA-EGOHAND-2026-0004`, `EA-EGOHAND-2026-0008`, `EA-EGOHAND-2026-0010`, `EA-EGOHAND-2026-0012`, `EA-EGOHAND-2026-0015`, `EA-EGOHAND-2026-0017`, `EA-EGOHAND-2026-0022`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 15
- Structure mapped: 15
- Deep-read papers: 15
- Claim-verified papers: 15
- Accepted evidence papers: 15
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；数据污染则是来源、时间、任务、模型版本和评测边界的关系失真，治理必须贯穿采集、训练、生成和闭环评测。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。对视觉—触觉—力觉数据，同时间戳帧只是最低层记录，真正的训练单元还应保留 approach、contact、slip、release、recovery 等事件链，并记录传感器/硬件 ID、时钟、标定和换件历史。所有异构数据都应声明可信监督字段，以动作条件状态变化和真实闭环收益验收；规模化触觉数据不自动等于跨硬件通用性或...
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；腕部六维力/力矩提供低维全局载荷，触觉提供高维局部接触场，两者不能互换。最新综合更支持按功能和时标选择性耦合：视觉/语言负责慢速全局语义与计划，触觉/力觉进入快速接触反馈，动作条件世界模型负责预测与验证。目标不是堆传感器，而是形成“同步数据—接触表征—动作条件预测—高频纠偏—安全过程评测”的接触执行栈，并证明每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-HARDWARE` 采集硬件与设备路线: 采集硬件不会收敛到单一设备，而会收敛到少数数据协议和接口范式。单目适合规模化起步，双目/多目和 LiDAR 适合几何、遮挡、动态或弱纹理场景；ARKit/SLAM/Tracking 可作低成本位姿输入但不能当工业真值。视觉定位还需要把点云、SCR、3DGS 或参考图像集合视为有构建、存储、更新、隐私和可恢复域成本的“地图硬件”。UMI 的数据质量从采集器设计开始：人体工学、力分布、重量、刚度、传感器组合和部署端同构程度会直接改变示教速度、损伤、负担和可执行性。
  - 具身采集不必须双目，关键看任务是否依赖稳定几何、相对深度和遮挡恢复。
  - 行业偏好单目来自工程经济性：便宜、易标定、低带宽、易维护、适配视觉预训练。
  - 双目落地瓶颈是标定同步、弱纹理/反光匹配失败、深度噪声融合和系统成本。
  - ARKit 可用于低成本 VIO、位姿跟踪和快速原型，但不适合作唯一计量真值。
  - VR/AR tracking 是低成本人机输入，需记录置信度、丢踪事件和时间戳质量。
- `EA-4D` 4D 时空推理与世界动态: 具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。
  - 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
  - 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
  - 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
  - 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
  - 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 5 |
| `conditional` | 条件成立 | 7 |
| `limit` | 限制/负面 | 14 |
| `gap` | 缺口 | 3 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2509.13883: EvHand-FPV: Efficient Event-Based 3D Hand Tracking from First-Person View | 2025-09-17 | gap, limit | EA-EGOHAND-2026-0001; EA-EGOHAND-2026-0002 |
| 2510.02601: Ego-Exo 3D Hand Tracking in the Wild with a Mobile Multi-Camera Rig | 2025-10-02 | conditional, limit | EA-EGOHAND-2026-0003; EA-EGOHAND-2026-0004 |
| 2511.18127: SFHand: Learning Embodied Manipulation by Streaming Egocentric 3D Hand Forecasting | 2025-11-22 | limit | EA-EGOHAND-2026-0005; EA-EGOHAND-2026-0006 |
| 2601.01050: EgoGrasp: World-Space Hand-Object Interaction Estimation from Egocentric Videos | 2026-01-03 | conditional, support | EA-EGOHAND-2026-0007; EA-EGOHAND-2026-0008 |
| 2601.15516: DeltaDorsal: Enhancing Hand Pose Estimation with Dorsal Features in Egocentric Views | 2026-01-21 | conditional, support | EA-EGOHAND-2026-0009; EA-EGOHAND-2026-0010 |
| 2602.05159: AirGlove: Exploring Egocentric 3D Hand Tracking and Appearance Generalization for Sensing Gloves | 2026-02-05 | limit | EA-EGOHAND-2026-0011 |
| 2603.29733: Leveraging Synthetic Data for Enhancing Egocentric Hand-Object Interaction Detection | 2026-03-31 | conditional, limit | EA-EGOHAND-2026-0012; EA-EGOHAND-2026-0013 |
| 2604.12343: Detecting Precise Hand Touch Moments in Egocentric Video | 2026-04-14 | conditional, limit | EA-EGOHAND-2026-0014; EA-EGOHAND-2026-0015 |
| 2605.12297: EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras | 2026-05-12 | conditional, limit | EA-EGOHAND-2026-0016; EA-EGOHAND-2026-0017 |
| 2605.12498: EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera | 2026-05-12 | limit, support | EA-EGOHAND-2026-0018; EA-EGOHAND-2026-0019 |
| 2605.18553: StableHand: Quality-Aware Flow Matching for World-Space Dual-Hand Motion Estimation from Egocentric Video | 2026-05-18 | limit, support | EA-EGOHAND-2026-0020; EA-EGOHAND-2026-0021 |
| 2605.21714: AVI-HT: Adaptive Vision-IMU Fusion for 3D Hand Tracking | 2026-05-20 | conditional, limit | EA-EGOHAND-2026-0022; EA-EGOHAND-2026-0023 |
| 2606.10790: A Multimodal RGB and Events Dataset for Hand Detection in First-Person View | 2026-06-09 | gap, limit | EA-EGOHAND-2026-0024; EA-EGOHAND-2026-0025 |
| 2606.19156: Hand-4DGS: Feed-Forward 3D Gaussian Splatting for 4D Hand Reconstruction from Egocentric Videos | 2026-06-17 | limit, support | EA-EGOHAND-2026-0026; EA-EGOHAND-2026-0027 |
| 2606.30598: Towards in-the-wild Egocentric 3D Hand-Object Pose Estimation | 2026-06-29 | gap, limit | EA-EGOHAND-2026-0028; EA-EGOHAND-2026-0029 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-EGOHAND-2026-0007 | EA-DATA | `support` | `direct` | 第一视角的相机坐标会把头部抖动与物体运动混合，稳定 HOI 追踪需要世界坐标锚定。 | 原文直接描述相机自运动与物体运动的坐标耦合。 (1 Introduction) | hongming-fu; wenjia-wang; xiaozhen-qiao; et al. | 2601.01050 |
| EA-EGOHAND-2026-0009 | EA-DATA | `support` | `direct` | Egocentric 手指自遮挡是高频现象：跨四个数据集，超过 20% 帧至少有一根手指高度遮挡。 | 原文在四数据集分析中直接报告遮挡比例。 (3.2. Occlusion Prevalence in Egocentric Data) | william-huang; siyou-pei; leyi-zou; et al. | 2601.15516 |
| EA-EGOHAND-2026-0018 | EA-DATA | `support` | `direct` | 单目头戴相机中，绝对 3D 手追踪同时受深度–尺度歧义、自遮挡与宽 FOV/鱼眼变形限制。 | 原文在问题定义中直接并列了绝对 3D 手追踪的三个主要视觉/几何难点。 (1. Introduction) | christen-millerdurai; shaoxiang-wang; yaxu-xie; et al. | 2605.12498 |
| EA-EGOHAND-2026-0020 | EA-DATA | `support` | `direct` | Ego 双手追踪的观测质量具有左/右手与腕部/手指两个轴的异质性，不能用单一置信度概括。 | 原文直接给出单一质量分数会混淆的两类异质性。 (1 Introduction) | huajian-zeng; chaohua-yao; yuantai-zhang; et al. | 2605.18553 |
| EA-EGOHAND-2026-0026 | EA-DATA | `support` | `direct` | Egocentric 4D 手重建同时受移动相机、严重自遮挡、有限视角、快速手动与双手交互影响。 | 原文在问题定义中直接列出了移动相机、遮挡、视角、快速运动和双手交互等耦合困难。 (1 Introduction) | jeongmin-bae; seoha-kim; marc-pollefeys; et al. | 2606.19156 |
| EA-EGOHAND-2026-0004 | EA-DATA | `conditional` | `direct` | 在真实环境中获得精确 3D 手真值仍依赖多相机、同步、标定和重型移动采集硬件。 | 原文的硬件章节表明高精度真值来自多视图、MoCap、硬同步和标定的组合。 (3.1 Mobile Capture Rig) | patrick-rim; kun-he; kevin-harris; et al. | 2510.02601 |
| EA-EGOHAND-2026-0008 | EA-DATA | `conditional` | `direct` | 开放词表世界坐标 HOI 恢复的精度目前以重型离线管线为代价，不等于可实时部署。 | 推理设置明确使用 200 步扩散采样，且前文还有多步测试时优化。 (4.1 Implementation Details & Metrics) | hongming-fu; wenjia-wang; xiaozhen-qiao; et al. | 2601.01050 |
| EA-EGOHAND-2026-0010 | EA-DATA | `conditional` | `direct` | 手背皮肤形变只是条件性遮挡补充信号；手背不可见、低分辨率或快速运动会削弱其价值。 | 作者在泛化讨论中明确限定手背特征的可见性条件。 (8. Discussion) | william-huang; siyou-pei; leyi-zou; et al. | 2601.15516 |
| EA-EGOHAND-2026-0012 | EA-DATA | `conditional` | `direct` | 当前纯合成数据不能替代真实 egocentric HOI 数据；它主要是少标签和域适应下的补充资源。 | 讨论章直接给出纯合成方案的边界。 (5 Discussion) | rosario-leonardi; antonino-furnari; francesco-ragusa; et al. | 2603.29733 |
| EA-EGOHAND-2026-0015 | EA-DATA | `conditional` | `direct` | TouchMoment 的自动训练标注与手工标签平均相差 1.94 帧，这与严格评测容差处于同一量级。 | 原文给出自动工具相对手工标注的帧级差异。 (3.2 Touch Annotation) | huy-anh-nguyen; feras-dayoub; minh-hoai | 2604.12343 |
| EA-EGOHAND-2026-0017 | EA-DATA | `conditional` | `direct` | 双目事件的几何增益以更高硬件、标定和算力成本为代价，超低功耗部署仍需压缩。 | 作者在限制章明确承认当前架构对超低功耗部署仍有额外工程需求。 (V-I Limitations) | luming-wang; hao-shi; jiajun-zhai; et al. | 2605.12297 |
| EA-EGOHAND-2026-0022 | EA-DATA | `conditional` | `direct` | 视觉与 6-DoF IMU 的互补只有在准确同步下成立：视觉锚定全局位置，IMU 补足遮挡下的高频指部运动。 | 该句在上下文中明确指向视觉全局锚点与 IMU 局部动力学的互补。 (1 Introduction) | ziyi-kou; ankit-kumar; mia-huang; et al. | 2605.21714 |
| EA-EGOHAND-2026-0001 | EA-DATA | `limit` | `direct` | 事件手追踪存在显著视角域差：第三视角模型直接用于第一视角时性能会严重下降。 | 原文在同一表中报告了 EventHands 直接跨视角迁移的下降。 (IV-B Comparison with Prior Work) | zhen-xu; guorui-lu; chang-gao; et al. | 2509.13883 |
| EA-EGOHAND-2026-0003 | EA-DATA | `limit` | `direct` | 受控数据上训练的 3D 手追踪器不能保证野外泛化；在 EgoExo-Hands 上的 MKPE 从域内约 9–11 mm 上升到 16.28 mm。 | 该结论由同节 Table 2 的域内和跨域 MKPE 直接支持。 (3.3 Quantitative Evaluation) | patrick-rim; kun-he; kevin-harris; et al. | 2510.02601 |
| EA-EGOHAND-2026-0005 | EA-DATA | `limit` | `direct` | 流式手追踪/预测中，素朴时序记忆可能比无记忆更差，因为背景 token 会检索并放大历史队列中的自回归误差。 | 该句由同节 Table 4 的 ADE/FDE 消融数据直接支持。 (5.3.2 Ablation on ROI-enhanced memory) | ruicong-liu; yifei-huang; liangyang-ouyang; et al. | 2511.18127 |
| EA-EGOHAND-2026-0006 | EA-DATA | `limit` | `direct` | 自回归追踪/预测必须显式管理自身误差累积；被存入的错误可以被后续时刻再次检索并放大。 | 作者在消融解释中直接给出了记忆导致误差放大的机制。 (5.3.2 Ablation on ROI-enhanced memory) | ruicong-liu; yifei-huang; liangyang-ouyang; et al. | 2511.18127 |
| EA-EGOHAND-2026-0011 | EA-DATA | `limit` | `direct` | 裸手预训练的视觉手追踪器在传感手套上存在大幅外观域差，每种新手套都可能需要新的适配数据。 | 原文在四类手套评测表后直接总结了裸手到手套的性能下降。 (5 Evaluation) | wenhui-cui; ziyi-kou; chuan-qin; et al. | 2602.05159 |
| EA-EGOHAND-2026-0013 | EA-DATA | `limit` | `direct` | HOI-Synth 的证据是单帧检测证据，不包含轨迹连续性或时序追踪能力。 | 限制章明确声明不使用时序信息。 (5.1 Limitations and future work) | rosario-leonardi; antonino-furnari; francesco-ragusa; et al. | 2603.29733 |
| EA-EGOHAND-2026-0014 | EA-DATA | `limit` | `direct` | 精确触碰时刻检测不是普通手检测；它还需区分强自运动、近距遮挡和视觉上几乎相同的近接触帧。 | 原文直接列出了接触时刻定位中的第一视角特有干扰。 (1 Introduction) | huy-anh-nguyen; feras-dayoub; minh-hoai | 2604.12343 |
| EA-EGOHAND-2026-0016 | EA-DATA | `limit` | `direct` | 事件相机不会自动消除 egocentric 干扰：头部运动生成的背景事件会与手运动信号耦合。 | 原文直接描述了头部自运动对事件流的混入机制。 (I Introduction) | luming-wang; hao-shi; jiajun-zhai; et al. | 2605.12297 |
| EA-EGOHAND-2026-0019 | EA-DATA | `limit` | `direct` | 跨镜头单网络仍依赖已标定 3D 训练数据和相机内参，不等于无标定野外泛化。 | 作者在限制章明确把已标定 3D 训练依赖与野外泛化不足联系起来。 (5. Limitations) | christen-millerdurai; shaoxiang-wang; yaxu-xie; et al. | 2605.12498 |
| EA-EGOHAND-2026-0021 | EA-DATA | `limit` | `direct` | 当上游视觉完全没有可靠观测锚点时，生成恢复只能产生合理先验，可能形成错误轨迹。 | 作者在失败案例中明确区分了“合理”与“正确”。 (Appendix H Additional Qualitative Results) | huajian-zeng; chaohua-yao; yuantai-zhang; et al. | 2605.18553 |
| EA-EGOHAND-2026-0023 | EA-DATA | `limit` | `direct` | 手套型多模态追踪会引入新的外观域差，且对不同手套布局和 IMU 规格的泛化尚未验证。 | 原文在结论的限制段明确将跨手套泛化列为未验证问题。 (6 Conclusion) | ziyi-kou; ankit-kumar; mia-huang; et al. | 2605.21714 |
| EA-EGOHAND-2026-0024 | EA-DATA | `limit` | `direct` | 事件手检测的精度仍受慢变信号不可见与将事件流重新帧化的处理低效限制。 | 原文直接列出了事件传感器与处理表示两类瓶颈。 (I Introduction) | bharghav-kota; yulia-sandamirskaya | 2606.10790 |
| EA-EGOHAND-2026-0027 | EA-DATA | `limit` | `direct` | Hand-4DGS 的定量结果排除了手大部分出框或上游无法正确检测双手的帧，因而不能外推到最难丢检场景。 | 数据处理细节明确列出了两类被排除的高难样本。 (C.2 Training Setup and Model Architecture) | jeongmin-bae; seoha-kim; marc-pollefeys; et al. | 2606.19156 |
| EA-EGOHAND-2026-0029 | EA-DATA | `limit` | `direct` | 将中心帧的接触标注传播到整个 clip 会受手边别错误和相机跳变污染，需保留每帧置信度。 | 作者在限制中明确列出了标签传播的两类时序噪声。 (10 Limitations and Future Directions) | siddhant-bansal; zhifan-zhu; shashank-tripathi; et al. | 2606.30598 |
| EA-EGOHAND-2026-0002 | EA-DATA | `gap` | `direct` | 真实事件数据缺少 3D 真值，导致该方法的真实 3D 指标无法被直接验证。 | 原文明确将 3D 评测限定在合成数据。 (IV-A2 3D Metric) | zhen-xu; guorui-lu; chang-gao; et al. | 2509.13883 |
| EA-EGOHAND-2026-0025 | EA-DATA | `gap` | `direct` | 现有 EventEgoHands 仍缺少光照、肤色和活动多样性，真实数据覆盖是未解问题。 | 未来工作明确列出了数据人群与场景多样性边界。 (V conclusion and further work) | bharghav-kota; yulia-sandamirskaya | 2606.10790 |
| EA-EGOHAND-2026-0028 | EA-DATA | `gap` | `direct` | 野外 egocentric 手物 3D 估计的主要数据瓶颈是重遮挡与接触歧义下缺少便宜、可扩展的 3D 监督。 | 该句所在段落将野外遮挡/接触歧义与 MoCap 成本、环境空洞联系起来。 (1 Introduction) | siddhant-bansal; zhifan-zhu; shashank-tripathi; et al. | 2606.30598 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-EGOHAND-2026-0007 | hongming-fu; wenjia-wang; xiaozhen-qiao; et al. | unlisted | `support` | 第一视角的相机坐标会把头部抖动与物体运动混合，稳定 HOI 追踪需要世界坐标锚定。 |
| EA-EGOHAND-2026-0009 | william-huang; siyou-pei; leyi-zou; et al. | unlisted | `support` | Egocentric 手指自遮挡是高频现象：跨四个数据集，超过 20% 帧至少有一根手指高度遮挡。 |
| EA-EGOHAND-2026-0018 | christen-millerdurai; shaoxiang-wang; yaxu-xie; et al. | unlisted | `support` | 单目头戴相机中，绝对 3D 手追踪同时受深度–尺度歧义、自遮挡与宽 FOV/鱼眼变形限制。 |
| EA-EGOHAND-2026-0020 | huajian-zeng; chaohua-yao; yuantai-zhang; et al. | unlisted | `support` | Ego 双手追踪的观测质量具有左/右手与腕部/手指两个轴的异质性，不能用单一置信度概括。 |
| EA-EGOHAND-2026-0026 | jeongmin-bae; seoha-kim; marc-pollefeys; et al. | unlisted | `support` | Egocentric 4D 手重建同时受移动相机、严重自遮挡、有限视角、快速手动与双手交互影响。 |
| EA-EGOHAND-2026-0004 | patrick-rim; kun-he; kevin-harris; et al. | unlisted | `conditional` | 在真实环境中获得精确 3D 手真值仍依赖多相机、同步、标定和重型移动采集硬件。 |
| EA-EGOHAND-2026-0008 | hongming-fu; wenjia-wang; xiaozhen-qiao; et al. | unlisted | `conditional` | 开放词表世界坐标 HOI 恢复的精度目前以重型离线管线为代价，不等于可实时部署。 |
| EA-EGOHAND-2026-0010 | william-huang; siyou-pei; leyi-zou; et al. | unlisted | `conditional` | 手背皮肤形变只是条件性遮挡补充信号；手背不可见、低分辨率或快速运动会削弱其价值。 |
| EA-EGOHAND-2026-0012 | rosario-leonardi; antonino-furnari; francesco-ragusa; et al. | unlisted | `conditional` | 当前纯合成数据不能替代真实 egocentric HOI 数据；它主要是少标签和域适应下的补充资源。 |
| EA-EGOHAND-2026-0015 | huy-anh-nguyen; feras-dayoub; minh-hoai | unlisted | `conditional` | TouchMoment 的自动训练标注与手工标签平均相差 1.94 帧，这与严格评测容差处于同一量级。 |
| EA-EGOHAND-2026-0017 | luming-wang; hao-shi; jiajun-zhai; et al. | unlisted | `conditional` | 双目事件的几何增益以更高硬件、标定和算力成本为代价，超低功耗部署仍需压缩。 |
| EA-EGOHAND-2026-0022 | ziyi-kou; ankit-kumar; mia-huang; et al. | unlisted | `conditional` | 视觉与 6-DoF IMU 的互补只有在准确同步下成立：视觉锚定全局位置，IMU 补足遮挡下的高频指部运动。 |
| EA-EGOHAND-2026-0001 | zhen-xu; guorui-lu; chang-gao; et al. | unlisted | `limit` | 事件手追踪存在显著视角域差：第三视角模型直接用于第一视角时性能会严重下降。 |
| EA-EGOHAND-2026-0003 | patrick-rim; kun-he; kevin-harris; et al. | unlisted | `limit` | 受控数据上训练的 3D 手追踪器不能保证野外泛化；在 EgoExo-Hands 上的 MKPE 从域内约 9–11 mm 上升到 16.28 mm。 |
| EA-EGOHAND-2026-0005 | ruicong-liu; yifei-huang; liangyang-ouyang; et al. | unlisted | `limit` | 流式手追踪/预测中，素朴时序记忆可能比无记忆更差，因为背景 token 会检索并放大历史队列中的自回归误差。 |
| EA-EGOHAND-2026-0006 | ruicong-liu; yifei-huang; liangyang-ouyang; et al. | unlisted | `limit` | 自回归追踪/预测必须显式管理自身误差累积；被存入的错误可以被后续时刻再次检索并放大。 |
| EA-EGOHAND-2026-0011 | wenhui-cui; ziyi-kou; chuan-qin; et al. | unlisted | `limit` | 裸手预训练的视觉手追踪器在传感手套上存在大幅外观域差，每种新手套都可能需要新的适配数据。 |
| EA-EGOHAND-2026-0013 | rosario-leonardi; antonino-furnari; francesco-ragusa; et al. | unlisted | `limit` | HOI-Synth 的证据是单帧检测证据，不包含轨迹连续性或时序追踪能力。 |
| EA-EGOHAND-2026-0014 | huy-anh-nguyen; feras-dayoub; minh-hoai | unlisted | `limit` | 精确触碰时刻检测不是普通手检测；它还需区分强自运动、近距遮挡和视觉上几乎相同的近接触帧。 |
| EA-EGOHAND-2026-0016 | luming-wang; hao-shi; jiajun-zhai; et al. | unlisted | `limit` | 事件相机不会自动消除 egocentric 干扰：头部运动生成的背景事件会与手运动信号耦合。 |
| EA-EGOHAND-2026-0019 | christen-millerdurai; shaoxiang-wang; yaxu-xie; et al. | unlisted | `limit` | 跨镜头单网络仍依赖已标定 3D 训练数据和相机内参，不等于无标定野外泛化。 |
| EA-EGOHAND-2026-0021 | huajian-zeng; chaohua-yao; yuantai-zhang; et al. | unlisted | `limit` | 当上游视觉完全没有可靠观测锚点时，生成恢复只能产生合理先验，可能形成错误轨迹。 |
| EA-EGOHAND-2026-0023 | ziyi-kou; ankit-kumar; mia-huang; et al. | unlisted | `limit` | 手套型多模态追踪会引入新的外观域差，且对不同手套布局和 IMU 规格的泛化尚未验证。 |
| EA-EGOHAND-2026-0024 | bharghav-kota; yulia-sandamirskaya | unlisted | `limit` | 事件手检测的精度仍受慢变信号不可见与将事件流重新帧化的处理低效限制。 |
| EA-EGOHAND-2026-0027 | jeongmin-bae; seoha-kim; marc-pollefeys; et al. | unlisted | `limit` | Hand-4DGS 的定量结果排除了手大部分出框或上游无法正确检测双手的帧，因而不能外推到最难丢检场景。 |
| EA-EGOHAND-2026-0029 | siddhant-bansal; zhifan-zhu; shashank-tripathi; et al. | unlisted | `limit` | 将中心帧的接触标注传播到整个 clip 会受手边别错误和相机跳变污染，需保留每帧置信度。 |
| EA-EGOHAND-2026-0002 | zhen-xu; guorui-lu; chang-gao; et al. | unlisted | `gap` | 真实事件数据缺少 3D 真值，导致该方法的真实 3D 指标无法被直接验证。 |
| EA-EGOHAND-2026-0025 | bharghav-kota; yulia-sandamirskaya | unlisted | `gap` | 现有 EventEgoHands 仍缺少光照、肤色和活动多样性，真实数据覆盖是未解问题。 |
| EA-EGOHAND-2026-0028 | siddhant-bansal; zhifan-zhu; shashank-tripathi; et al. | unlisted | `gap` | 野外 egocentric 手物 3D 估计的主要数据瓶颈是重遮挡与接触歧义下缺少便宜、可扩展的 3D 监督。 |

## Synthesis Slots

### 共识/正向证据
- `EA-EGOHAND-2026-0007`: 第一视角的相机坐标会把头部抖动与物体运动混合，稳定 HOI 追踪需要世界坐标锚定。
- `EA-EGOHAND-2026-0009`: Egocentric 手指自遮挡是高频现象：跨四个数据集，超过 20% 帧至少有一根手指高度遮挡。
- `EA-EGOHAND-2026-0018`: 单目头戴相机中，绝对 3D 手追踪同时受深度–尺度歧义、自遮挡与宽 FOV/鱼眼变形限制。
- `EA-EGOHAND-2026-0020`: Ego 双手追踪的观测质量具有左/右手与腕部/手指两个轴的异质性，不能用单一置信度概括。
- `EA-EGOHAND-2026-0026`: Egocentric 4D 手重建同时受移动相机、严重自遮挡、有限视角、快速手动与双手交互影响。
### 条件成立
- `EA-EGOHAND-2026-0004`: 在真实环境中获得精确 3D 手真值仍依赖多相机、同步、标定和重型移动采集硬件。
- `EA-EGOHAND-2026-0008`: 开放词表世界坐标 HOI 恢复的精度目前以重型离线管线为代价，不等于可实时部署。
- `EA-EGOHAND-2026-0010`: 手背皮肤形变只是条件性遮挡补充信号；手背不可见、低分辨率或快速运动会削弱其价值。
- `EA-EGOHAND-2026-0012`: 当前纯合成数据不能替代真实 egocentric HOI 数据；它主要是少标签和域适应下的补充资源。
- `EA-EGOHAND-2026-0015`: TouchMoment 的自动训练标注与手工标签平均相差 1.94 帧，这与严格评测容差处于同一量级。
- `EA-EGOHAND-2026-0017`: 双目事件的几何增益以更高硬件、标定和算力成本为代价，超低功耗部署仍需压缩。
- `EA-EGOHAND-2026-0022`: 视觉与 6-DoF IMU 的互补只有在准确同步下成立：视觉锚定全局位置，IMU 补足遮挡下的高频指部运动。
### 限制与失败模式
- `EA-EGOHAND-2026-0001`: 事件手追踪存在显著视角域差：第三视角模型直接用于第一视角时性能会严重下降。
- `EA-EGOHAND-2026-0003`: 受控数据上训练的 3D 手追踪器不能保证野外泛化；在 EgoExo-Hands 上的 MKPE 从域内约 9–11 mm 上升到 16.28 mm。
- `EA-EGOHAND-2026-0005`: 流式手追踪/预测中，素朴时序记忆可能比无记忆更差，因为背景 token 会检索并放大历史队列中的自回归误差。
- `EA-EGOHAND-2026-0006`: 自回归追踪/预测必须显式管理自身误差累积；被存入的错误可以被后续时刻再次检索并放大。
- `EA-EGOHAND-2026-0011`: 裸手预训练的视觉手追踪器在传感手套上存在大幅外观域差，每种新手套都可能需要新的适配数据。
- `EA-EGOHAND-2026-0013`: HOI-Synth 的证据是单帧检测证据，不包含轨迹连续性或时序追踪能力。
- `EA-EGOHAND-2026-0014`: 精确触碰时刻检测不是普通手检测；它还需区分强自运动、近距遮挡和视觉上几乎相同的近接触帧。
- `EA-EGOHAND-2026-0016`: 事件相机不会自动消除 egocentric 干扰：头部运动生成的背景事件会与手运动信号耦合。
### 开放问题
- `EA-EGOHAND-2026-0002`: 真实事件数据缺少 3D 真值，导致该方法的真实 3D 指标无法被直接验证。
- `EA-EGOHAND-2026-0025`: 现有 EventEgoHands 仍缺少光照、肤色和活动多样性，真实数据覆盖是未解问题。
- `EA-EGOHAND-2026-0028`: 野外 egocentric 手物 3D 估计的主要数据瓶颈是重遮挡与接触歧义下缺少便宜、可扩展的 3D 监督。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-EGOHAND-2026-0007` 第一视角的相机坐标会把头部抖动与物体运动混合，稳定 HOI 追踪需要世界坐标锚定。
  - `EA-EGOHAND-2026-0009` Egocentric 手指自遮挡是高频现象：跨四个数据集，超过 20% 帧至少有一根手指高度遮挡。
  - `EA-EGOHAND-2026-0018` 单目头戴相机中，绝对 3D 手追踪同时受深度–尺度歧义、自遮挡与宽 FOV/鱼眼变形限制。
- Scientific memo preview: 《近一年 ego-centric 数据中手部检测与追踪的问题和难点》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年 ego-centric 数据中手部检测与追踪的问题和难点 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年 ego-centric 数据中手部检测与追踪的问题和难点: 先看证据边界，再谈一个可传播的反常识洞察。

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
