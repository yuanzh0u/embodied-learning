# Review Packet: 近一年具身智能预训练模型对数据源与采集参数的要求

## Scope

- Topic: 近一年具身智能预训练模型对数据源与采集参数的要求
- Time range: 2025-07-26..2026-07-26
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-HARDWARE`, `EA-SENSOR`, `EA-MODEL`, `EA-XEMBODIMENT`
- Evidence events: 33
- Topic cards: 5
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 33
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DQ-YEAR-READ-0008`, `EA-DQ-YEAR-READ-0009`, `EA-EGO-2026-0007`, `EA-DQ-YEAR-READ-0010`, `EA-PRETRAIN-DATA-2026-0003`, `EA-PRETRAIN-DATA-2026-0002`, `EA-PRETRAIN-DATA-2026-0005`, `EA-PRETRAIN-DATA-2026-0006`, `EA-DQ-YEAR-READ-0003`, `EA-EGO-2026-0008`, `EA-EGO-2026-0011`, `EA-UMI-READ-0003`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 20 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 20
- Structure mapped: 20
- Deep-read papers: 20
- Claim-verified papers: 20
- Accepted evidence papers: 20
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
- `EA-HARDWARE` 采集硬件与设备路线: 采集硬件不会收敛到单一设备，而会收敛到少数数据协议和接口范式。单目适合规模化起步，双目/多目和 LiDAR 适合几何、遮挡、动态或弱纹理场景；ARKit/SLAM/Tracking 可作低成本位姿输入但不能当工业真值。视觉定位还需要把点云、SCR、3DGS 或参考图像集合视为有构建、存储、更新、隐私和可恢复域成本的“地图硬件”。UMI 的数据质量从采集器设计开始：人体工学、力分布、重量、刚度、传感器组合和部署端同构程度会直接改变示教速度、损伤、负担和可执行性。
  - 具身采集不必须双目，关键看任务是否依赖稳定几何、相对深度和遮挡恢复。
  - 行业偏好单目来自工程经济性：便宜、易标定、低带宽、易维护、适配视觉预训练。
  - 双目落地瓶颈是标定同步、弱纹理/反光匹配失败、深度噪声融合和系统成本。
  - ARKit 可用于低成本 VIO、位姿跟踪和快速原型，但不适合作唯一计量真值。
  - VR/AR tracking 是低成本人机输入，需记录置信度、丢踪事件和时间戳质量。
- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；腕部六维力/力矩提供低维全局载荷，触觉提供高维局部接触场，两者不能互换。最新综合更支持按功能和时标选择性耦合：视觉/语言负责慢速全局语义与计划，触觉/力觉进入快速接触反馈，动作条件世界模型负责预测与验证。目标不是堆传感器，而是形成“同步数据—接触表征—动作条件预测—高频纠偏—安全过程评测”的接触执行栈，并证明每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型、本体适配器与底层控制器组成的融合栈。近期突破不只是生成更长视频，而是把未来压缩成低频逻辑步骤、稀疏视觉子目标或结构化状态，并验证它与真实动作同步；BadWAM 说明“想象合理、动作错误”足以让系统失效。世界模型应先承担训练期教师、离线排序等低权限任务，再逐级争取在线规划权。Loco-manipulation 与多模态证据还表明，完整动作接口及按功能/时标分层的接触反馈会限制能力上限。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-XEMBODIMENT` 跨本体与数据迁移: 跨本体迁移的核心不是复制姿态、控制命令或传感器 token，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。语言/视觉语义、对象状态变化和粗运动先验较易共享；局部接触载荷、传感器频率、硬件标定和控制接口更依赖目标平台。更稳健的路线是共享 Cartesian/object state delta 或接触目标，再由机器人和传感器特定 adapter、少量目标硬件数据与真实闭环校准落地。
  - 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
  - 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
  - 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
  - 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
  - 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 8 |
| `conditional` | 条件成立 | 12 |
| `limit` | 限制/负面 | 13 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2509.01657: Data Retrieval with Importance Weights for Few-Shot Imitation Learning | 2025-09-01 | support | EA-DQ-YEAR-READ-0008 |
| 2509.21986: Developing Vision-Language-Action Model from Egocentric Videos | 2025-09-26T07:09:33Z | limit | EA-EGO-2026-0003; EA-EGO-2026-0004 |
| 2512.11612: Embodied Image Compression: Towards Codec for Robotic Visual Systems | 2025-12-12T18:59:07Z | conditional | EA-PRETRAIN-DATA-2026-0005; EA-PRETRAIN-DATA-2026-0006 |
| 2512.13100: OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning | 2025-12-15 | support | EA-DQ-YEAR-READ-0009 |
| 2602.09013: Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction | 2026-02-09T18:56:02Z | limit | EA-EGO-2026-0005; EA-EGO-2026-0006 |
| 2602.13197: Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos | 2026-02-13 | conditional | EA-DQ-YEAR-READ-0003 |
| 2602.16710: EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data | 2026-02-18T18:59:05Z | conditional, limit, support | EA-EGO-2026-0007; EA-EGO-2026-0008; EA-EGO-2026-0009 |
| 2603.22264: UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos | 2026-03-23T17:49:12Z | conditional, limit | EA-EGO-2026-0010; EA-EGO-2026-0011 |
| 2604.10647: OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction | 2026-04-12 | conditional | EA-UMI-READ-0003 |
| 2604.14089: UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception | 2026-04-15 | limit | EA-UMI-READ-0004 |
| 2605.20373: SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework | 2026-05-19T18:24:05Z | conditional, limit | EA-EGO-2026-0012; EA-EGO-2026-0013 |
| 2605.24934: HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos | 2026-05-24T08:26:41Z | conditional, limit | EA-EGO-2026-0014; EA-EGO-2026-0015 |
| 2605.26349: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Co... | 2026-05-25 | support | EA-ALIGN-READ-0012 |
| 2606.06194: ActiveMimic: Egocentric Video Pretraining with Active Perception | 2026-06-04T14:01:01Z | conditional, limit | EA-EGO-2026-0016; EA-EGO-2026-0017; EA-EGO-2026-0018 |
| 2606.16208: ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation | 2026-06-15 | support | EA-DQ-YEAR-READ-0010 |
| 2606.16253: SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models | 2026-06-15T03:38:29Z | conditional, support | EA-PRETRAIN-DATA-2026-0003; EA-PRETRAIN-DATA-2026-0004 |
| 2606.17200: ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining | 2026-06-15T18:40:18Z | conditional, support | EA-PRETRAIN-DATA-2026-0001; EA-PRETRAIN-DATA-2026-0002 |
| 2606.19161: HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision | 2026-06-17 | limit, support | EA-TACTILE-2026-0001; EA-TACTILE-2026-0002 |
| 2606.24049: SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies | 2026-06-23 | limit | EA-ALIGN-READ-0001 |
| 2607.06442: SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | limit | EA-DQ-YEAR-READ-0015 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DQ-YEAR-READ-0008 | EA-DATA | `support` | `direct` | 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 | IWR 将 retrieval-based imitation learning 的常用最近邻规则解释为目标数据分布 KDE 的极限，指出其高方差、易受噪声影响且不考虑 prior data distribution；方法用目标/先验分布概率比进行 importance-weighted retrieval，并在仿真和 Bridge 真实评估中改善现有检索方法。 (Abstract (full-text section)) | amber-xie; rahul-chand; dorsa-sadigh; et al. | 2509.01657 |
| EA-DQ-YEAR-READ-0009 | EA-DATA | `support` | `direct` | 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 | 论文指出 OXE 聚合 60 多个机器人数据集，但 top four robot types 占超过 85% 真实数据，带来过拟合风险；OXE-AugE 用 9 种不同机器人本体扩增 16 个 OXE 子集，形成 4.4M trajectories，并研究扩增对 cross-embodiment learning 的影响。 (Abstract (full-text section)) | guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al. | 2512.13100 |
| EA-EGO-2026-0007 | EA-DATA | `support` | `direct` | 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 | 五个数据规模的同架构实验报告单调提升，并限制结论不外推到测量区间之外。 (3.3 Policy Performance Scales with Pretraining Data Size) | ruijie-zheng; dantong-niu; yuqi-xie; et al. | 2602.16710 |
| EA-DQ-YEAR-READ-0010 | EA-DATA | `support` | `direct` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 | ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。 (C.4 Retention Balan... | tao-xu; jiaxin-wang; runhao-zhang; et al. | 2606.16208 |
| EA-PRETRAIN-DATA-2026-0003 | EA-DATA | `support` | `direct` | 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。 | 论文指出不同机位和图像区域对控制的价值不均匀，SPARC 通过时序 mask 自适应分配比特。 (1 Introduction and 3 Method) | sangyun-chung; mincheol-shin; jihyun-kim; et al. | 2606.16253 |
| EA-PRETRAIN-DATA-2026-0002 | EA-DATA | `support` | `direct` | 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。 | 419 条人类视频的工作空间覆盖是 34 条机器人示范的 4.8 倍，联合微调将 10 试验成功率从 10% 提高到 40%。 (5.3 Human Data for Augmented Fine-Tuning, Figure 6) | hao-li; ganlong-zhao; yufei-liu; et al. | 2606.17200 |
| EA-PRETRAIN-DATA-2026-0005 | EA-DATA | `conditional` | `direct` | VLA 对压缩往往呈‘轻压缩稳定、越过任务特定转折后骤降’，因此码率验收应看闭环成功曲线，不应只看人眼画质。 | 该基准中 RVS 从 0.10 到 0.06 bpp 约下降 5%，约 0.04 bpp 出现转折，0.02 bpp 附近快速失效。 (5.3 Experiment Result and Discussions) | zhenghao-chen; zijie-yue; haozhe-li; et al. | 2512.11612 |
| EA-PRETRAIN-DATA-2026-0006 | EA-DATA | `conditional` | `direct` | 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。 | 真实管线同步记录腕部与第三人称 RealSense、关节角和末端增量动作，频率为 10 Hz。 (Appendix C Subjective Data Collection) | zhenghao-chen; zijie-yue; haozhe-li; et al. | 2512.11612 |
| EA-DQ-YEAR-READ-0003 | EA-DATA | `conditional` | `direct` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 | PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。 (3.3 Trajectory and Gr... | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | 2602.13197 |
| EA-EGO-2026-0008 | EA-DATA | `conditional` | `direct` | 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 | 四类 checkpoint 的消融中，pretrain+midtrain 最好；human pretraining 提供结构，mid-training 负责控制锚定。 (3.2 Large-Scale Human Pretraining Is Key to Strong Dexterous Manipulation Policy Performance) | ruijie-zheng; dantong-niu; yuqi-xie; et al. | 2602.16710 |
| EA-EGO-2026-0011 | EA-DATA | `conditional` | `direct` | Retargeted ego-human 数据只能部分替代目标机器人示范：在论文的 Make Coffee co-training 实验中，没有 robot data 时成功始终接近 0。 | 作者明确总结 human data helps but robot data is indispensable，并给出约 2:1 的局部替代斜率。 (5.4 UniDex-Cap for Human-Robot Data Co-train) | gu-zhang; qicheng-xu; haozhe-zhang; et al. | 2603.22264 |
| EA-UMI-READ-0003 | EA-DATA | `conditional` | `direct` | UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical inter... | The HTML full text repeatedly identifies limited physical interaction signals as a bottleneck of existing UMI-like systems and proposes synchronized RGB, depth, trajectory, tactile sensing, internal grasping force, and... | shaqi-luo; yuanyuan-li; youhao-hu; et al. | 2604.10647 |
| EA-EGO-2026-0013 | EA-DATA | `conditional` | `direct` | Physics refiner 和 interaction reward 是把 Ego-centric 视频数据变成可执行技能的必要中间层；只跟踪运动会在接触任务中失败。 | 组件消融中去除 Refiner 显著退化，去除 interaction reward 时机器人只模仿弯腰而无法抬起物体。 (4.4 Component Analysis) | tianshu-wu; xiangqi-kong; yue-chen; et al. | 2605.20373 |
| EA-EGO-2026-0014 | EA-DATA | `conditional` | `direct` | 缩小 human/robot 图像外观差距并不足以让 ego 数据可训练；Water Flowers 消融中 visual-only 最高约 32.5%，显式 hand-object 6DoF ICT 才带来大幅闭环提升。 | raw RGB、inpainting、robot RGB 和 ICT 的阶梯消融把视觉外观与空间关系作用分离。 (4.4 What Drives Performance of HumanEgo?) | zhi-wang; botao-he; kelin-yu; et al. | 2605.24934 |
| EA-EGO-2026-0017 | EA-DATA | `conditional` | `direct` | 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 | HOT3D ground truth 上的 10% sample 验证给出 head/wrist 三类严格阈值 recovery rate。 (4.3 Egocentric Video Yields Effective Pretraining Labels) | xingyao-lin; guojin-zhong; tianyi-lu; et al. | 2606.06194 |
| EA-EGO-2026-0018 | EA-DATA | `conditional` | `direct` | 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 | Restocking 中 egocentric-pretrained model 的 placement 为 24/27，SFT-only 为 6/27；移除 head camera 降到 1/27。 (4.4 The Head Camera Enables Pretrained Active Perception) | xingyao-lin; guojin-zhong; tianyi-lu; et al. | 2606.06194 |
| EA-PRETRAIN-DATA-2026-0004 | EA-DATA | `conditional` | `direct` | 带宽要求必须在目标 VLA 和任务上用闭环成功率标定，感知画质或单一固定 bpp 不能替代。 | VLABench 中 0.0333/0.0685 bpp 的 SPARC 成功率接近但低于未压缩，而极低 bpp 下所有变体失效。 (C.1 Analysis of Key Components) | sangyun-chung; mincheol-shin; jihyun-kim; et al. | 2606.16253 |
| EA-PRETRAIN-DATA-2026-0001 | EA-DATA | `conditional` | `direct` | 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 | 三项组件消融均降低 RoboCasa 成功率，其中去掉人类伪动作可靠性加权的降幅最大。 (5.2 Ablation Studies, Figure 5(b)) | hao-li; ganlong-zhao; yufei-liu; et al. | 2606.17200 |
| EA-EGO-2026-0003 | EA-DATA | `limit` | `direct` | 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 | 策略训练段明确说明 gripper state 缺失，并以 object pose displacement 作为替代动作。 (III-C Policy Training) | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | 2509.21986 |
| EA-EGO-2026-0004 | EA-DATA | `limit` | `direct` | Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 | BGTS=1.0 保留 86,427 episodes 但真实机器人分数低于 BGTS=0.7 的 45,157 episodes。 (IV-C Ablation Study) | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | 2509.21986 |
| EA-EGO-2026-0005 | EA-DATA | `limit` | `direct` | 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。 | 方法段明确说明重建运动正确时，机器人—对象交互仍可能因几何误差而无效。 (III-B Dexterous Grasp and Manipulation Learning) | hongyi-chen; tony-dong; tiancheng-wu; et al. | 2602.09013 |
| EA-EGO-2026-0006 | EA-DATA | `limit` | `direct` | 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。 | 作者在限制段明确列出 dynamic camera 未覆盖；实验段说明对象点云被 LEAP Hand 遮挡时采用固定相对位姿近似。 (V Conclusion, Limitations, and Future Work) | hongyi-chen; tony-dong; tiancheng-wu; et al. | 2602.09013 |
| EA-EGO-2026-0009 | EA-DATA | `limit` | `direct` | Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 | 动作空间消融中 wrist-only 普遍较差，fingertip mapping 在 Cards/Bottle 等接触敏感任务不稳定。 (3.6 Hand Action Space Design for Human Pretraining) | ruijie-zheng; dantong-niu; yuqi-xie; et al. | 2602.16710 |
| EA-EGO-2026-0010 | EA-DATA | `limit` | `direct` | 将 egocentric hand trajectories 转为机器人可执行数据仍需 human-in-the-loop retargeting：基础坐标/形态偏差和 contact-rich 片段要人工校准。 | 论文的两阶段 retargeting 先自动 IK，再用 GUI 调整 6DoF offset；接触片段需人工复核。 (3.2.1 Kinematic Retargeting) | gu-zhang; qicheng-xu; haozhe-zhang; et al. | 2603.22264 |
| EA-UMI-READ-0004 | EA-DATA | `limit` | `direct` | Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves... | The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration d... | ziming-wang | 2604.14089 |
| EA-EGO-2026-0012 | EA-DATA | `limit` | `direct` | 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。 | 引言直接列出三类误差并说明它们使数据 unsuitable for direct policy learning。 (1 Introduction) | tianshu-wu; xiangqi-kong; yue-chen; et al. | 2605.20373 |
| EA-EGO-2026-0015 | EA-DATA | `limit` | `direct` | HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。 | 作者在 limitation 段逐项列出 stereo hand tracking、occlusion-robust tracking、cascading failures 和 1 cm plateau。 (5 Conclusion) | zhi-wang; botao-he; kelin-yu; et al. | 2605.24934 |
| EA-EGO-2026-0016 | EA-DATA | `limit` | `direct` | Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 | 方法段明确说明 current-frame wrist pose 与 first-frame camera path 的坐标差异会混合两类位移。 (3 Method) | xingyao-lin; guojin-zhong; tianyi-lu; et al. | 2606.06194 |
| EA-DQ-YEAR-READ-0015 | EA-DATA | `limit` | `direct` | SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 | 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。 (Introduction) | changti-wu; bin-yu; zhaolong-shen; et al. | 2607.06442 |
| EA-ALIGN-READ-0012 | EA-MODEL | `support` | `direct` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 | 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。 (Abstract (full-text section)) | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | 2605.26349 |
| EA-ALIGN-READ-0001 | EA-MODEL | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-TACTILE-2026-0001 | EA-SENSOR | `support` | `direct` | 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 | 摘要和基准设计章节直接给出数据规模、四项评测任务与任务级 OOD 划分。 (Abstract; 3 HT-Bench: A Multi-Task Tactile Evaluation Benchmark) | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | 2606.19161 |
| EA-TACTILE-2026-0002 | EA-SENSOR | `limit` | `direct` | HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 | 作者在限制章节明确列出硬件/本体覆盖和闭环下游评测缺失。 (6 Limitations and Future Work) | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | 2606.19161 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DQ-YEAR-READ-0008 | amber-xie; rahul-chand; dorsa-sadigh; et al. | unlisted | `support` | 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 |
| EA-DQ-YEAR-READ-0009 | guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al. | unlisted | `support` | 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 |
| EA-EGO-2026-0007 | ruijie-zheng; dantong-niu; yuqi-xie; et al. | unlisted | `support` | 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 |
| EA-DQ-YEAR-READ-0010 | tao-xu; jiaxin-wang; runhao-zhang; et al. | unlisted | `support` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 |
| EA-PRETRAIN-DATA-2026-0003 | sangyun-chung; mincheol-shin; jihyun-kim; et al. | unlisted | `support` | 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。 |
| EA-PRETRAIN-DATA-2026-0002 | hao-li; ganlong-zhao; yufei-liu; et al. | unlisted | `support` | 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。 |
| EA-PRETRAIN-DATA-2026-0005 | zhenghao-chen; zijie-yue; haozhe-li; et al. | unlisted | `conditional` | VLA 对压缩往往呈‘轻压缩稳定、越过任务特定转折后骤降’，因此码率验收应看闭环成功曲线，不应只看人眼画质。 |
| EA-PRETRAIN-DATA-2026-0006 | zhenghao-chen; zijie-yue; haozhe-li; et al. | unlisted | `conditional` | 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。 |
| EA-DQ-YEAR-READ-0003 | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | unlisted | `conditional` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 |
| EA-EGO-2026-0008 | ruijie-zheng; dantong-niu; yuqi-xie; et al. | unlisted | `conditional` | 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 |
| EA-EGO-2026-0011 | gu-zhang; qicheng-xu; haozhe-zhang; et al. | unlisted | `conditional` | Retargeted ego-human 数据只能部分替代目标机器人示范：在论文的 Make Coffee co-training 实验中，没有 robot data 时成功始终接近 0。 |
| EA-UMI-READ-0003 | shaqi-luo; yuanyuan-li; youhao-hu; et al. | unlisted | `conditional` | UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multi... |
| EA-EGO-2026-0013 | tianshu-wu; xiangqi-kong; yue-chen; et al. | unlisted | `conditional` | Physics refiner 和 interaction reward 是把 Ego-centric 视频数据变成可执行技能的必要中间层；只跟踪运动会在接触任务中失败。 |
| EA-EGO-2026-0014 | zhi-wang; botao-he; kelin-yu; et al. | unlisted | `conditional` | 缩小 human/robot 图像外观差距并不足以让 ego 数据可训练；Water Flowers 消融中 visual-only 最高约 32.5%，显式 hand-object 6DoF ICT 才带来大幅闭环提升。 |
| EA-EGO-2026-0017 | xingyao-lin; guojin-zhong; tianyi-lu; et al. | unlisted | `conditional` | 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 |
| EA-EGO-2026-0018 | xingyao-lin; guojin-zhong; tianyi-lu; et al. | unlisted | `conditional` | 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 |
| EA-PRETRAIN-DATA-2026-0004 | sangyun-chung; mincheol-shin; jihyun-kim; et al. | unlisted | `conditional` | 带宽要求必须在目标 VLA 和任务上用闭环成功率标定，感知画质或单一固定 bpp 不能替代。 |
| EA-PRETRAIN-DATA-2026-0001 | hao-li; ganlong-zhao; yufei-liu; et al. | unlisted | `conditional` | 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 |
| EA-EGO-2026-0003 | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | unlisted | `limit` | 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 |
| EA-EGO-2026-0004 | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | unlisted | `limit` | Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 |
| EA-EGO-2026-0005 | hongyi-chen; tony-dong; tiancheng-wu; et al. | unlisted | `limit` | 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。 |
| EA-EGO-2026-0006 | hongyi-chen; tony-dong; tiancheng-wu; et al. | unlisted | `limit` | 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。 |
| EA-EGO-2026-0009 | ruijie-zheng; dantong-niu; yuqi-xie; et al. | unlisted | `limit` | Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 |
| EA-EGO-2026-0010 | gu-zhang; qicheng-xu; haozhe-zhang; et al. | unlisted | `limit` | 将 egocentric hand trajectories 转为机器人可执行数据仍需 human-in-the-loop retargeting：基础坐标/形态偏差和 contact-rich 片段要人工校准。 |
| EA-UMI-READ-0004 | ziming-wang | unlisted | `limit` | Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric... |
| EA-EGO-2026-0012 | tianshu-wu; xiangqi-kong; yue-chen; et al. | unlisted | `limit` | 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。 |
| EA-EGO-2026-0015 | zhi-wang; botao-he; kelin-yu; et al. | unlisted | `limit` | HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。 |
| EA-EGO-2026-0016 | xingyao-lin; guojin-zhong; tianyi-lu; et al. | unlisted | `limit` | Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 |
| EA-DQ-YEAR-READ-0015 | changti-wu; bin-yu; zhaolong-shen; et al. | unlisted | `limit` | SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 |
| EA-ALIGN-READ-0012 | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | unlisted | `support` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 |
| EA-ALIGN-READ-0001 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-TACTILE-2026-0001 | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | unlisted | `support` | 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 |
| EA-TACTILE-2026-0002 | yuzhe-huang; jiaping-wu; jiaming-jiang; et al. | unlisted | `limit` | HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DQ-YEAR-READ-0008`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
- `EA-DQ-YEAR-READ-0009`: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
- `EA-EGO-2026-0007`: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。
- `EA-DQ-YEAR-READ-0010`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
- `EA-PRETRAIN-DATA-2026-0003`: 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。
- `EA-PRETRAIN-DATA-2026-0002`: 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。
- `EA-ALIGN-READ-0012`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- `EA-TACTILE-2026-0001`: 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。
### 条件成立
- `EA-PRETRAIN-DATA-2026-0005`: VLA 对压缩往往呈‘轻压缩稳定、越过任务特定转折后骤降’，因此码率验收应看闭环成功曲线，不应只看人眼画质。
- `EA-PRETRAIN-DATA-2026-0006`: 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。
- `EA-DQ-YEAR-READ-0003`: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- `EA-EGO-2026-0008`: 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。
- `EA-EGO-2026-0011`: Retargeted ego-human 数据只能部分替代目标机器人示范：在论文的 Make Coffee co-training 实验中，没有 robot data 时成功始终接近 0。
- `EA-UMI-READ-0003`: UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data.
- `EA-EGO-2026-0013`: Physics refiner 和 interaction reward 是把 Ego-centric 视频数据变成可执行技能的必要中间层；只跟踪运动会在接触任务中失败。
- `EA-EGO-2026-0014`: 缩小 human/robot 图像外观差距并不足以让 ego 数据可训练；Water Flowers 消融中 visual-only 最高约 32.5%，显式 hand-object 6DoF ICT 才带来大幅闭环提升。
### 限制与失败模式
- `EA-EGO-2026-0003`: 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。
- `EA-EGO-2026-0004`: Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。
- `EA-EGO-2026-0005`: 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。
- `EA-EGO-2026-0006`: 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。
- `EA-EGO-2026-0009`: Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。
- `EA-EGO-2026-0010`: 将 egocentric hand trajectories 转为机器人可执行数据仍需 human-in-the-loop retargeting：基础坐标/形态偏差和 contact-rich 片段要人工校准。
- `EA-UMI-READ-0004`: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible ta...
- `EA-EGO-2026-0012`: 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 20 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DQ-YEAR-READ-0008` 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
  - `EA-DQ-YEAR-READ-0009` 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
  - `EA-EGO-2026-0007` 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。
- Scientific memo preview: 《近一年具身智能预训练模型对数据源与采集参数的要求》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年具身智能预训练模型对数据源与采集参数的要求 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年具身智能预训练模型对数据源与采集参数的要求: 先看证据边界，再谈一个可传播的反常识洞察。

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
