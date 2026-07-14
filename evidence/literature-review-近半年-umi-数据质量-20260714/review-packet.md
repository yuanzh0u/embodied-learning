# Review Packet: 近半年 UMI 数据质量

## Scope

- Topic: 近半年 UMI 数据质量
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-XEMBODIMENT`
- Evidence events: 21
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> full-text evidence -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval, HTML/PDF/OCR recovery, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 21
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-2026-LY-0001`, `EA-DATA-2026-LY-0009`, `EA-DATA-2026-LY-0003`, `EA-DATA-2026-LY-0002`, `EA-DATA-2026-LY-0005`, `EA-DATA-2026-DQ-0002`, `UMI-6M-001`, `EA-DATA-2026-LY-0010`, `EA-DATA-2026-LY-0008`, `EA-DATA-2026-LY-0004`, `EA-DATA-2026-LY-0012`, `EA-DATA-2026-LY-0006`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 20 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；高分筛选还必须保留任务、本体、场景和长尾覆盖。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。所有异构数据都应声明其可信监督字段，并以真实闭环收益作为最终验收。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；触觉世界模型应预测动作条件下的接触演化，而不只是重建触觉图像。多模态建模的目标不是堆传感器，而是让每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-HARDWARE` 采集硬件与设备路线: 采集硬件不会收敛到单一设备，而会收敛到少数数据协议和接口范式。单目适合规模化起步，双目/多目和 LiDAR 适合几何、遮挡、动态或弱纹理场景；ARKit/SLAM/Tracking 可作低成本位姿输入但不能当工业真值。UMI 的数据质量从采集器设计开始：人体工学、力分布、重量、刚度、传感器组合和部署端同构程度会直接改变示教速度、损伤、负担和可执行性。
  - 具身采集不必须双目，关键看任务是否依赖稳定几何、相对深度和遮挡恢复。
  - 行业偏好单目来自工程经济性：便宜、易标定、低带宽、易维护、适配视觉预训练。
  - 双目落地瓶颈是标定同步、弱纹理/反光匹配失败、深度噪声融合和系统成本。
  - ARKit 可用于低成本 VIO、位姿跟踪和快速原型，但不适合作唯一计量真值。
  - VR/AR tracking 是低成本人机输入，需记录置信度、丢踪事件和时间戳质量。
- `EA-XEMBODIMENT` 跨本体与数据迁移: 跨本体迁移的核心不是复制姿态或控制命令，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。不同机器人即使记录相同 action command，也可能产生不同运动；更稳健的路线是共享 Cartesian state delta、对象状态变化或接触目标，再由机器人特定 adapter 和真实闭环校准落地。
  - 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
  - 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
  - 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
  - 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
  - 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 9 |
| `conditional` | 条件成立 | 8 |
| `limit` | 限制/负面 | 4 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2601.09988: In-the-Wild Compliant Manipulation with UMI-FT | unknown-date | conditional | UMI-6M-001 |
| 2602.10618: From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation... | 2026-02-11 | conditional | EA-DATA-2026-LY-0010 |
| 2602.13197: Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos | 2026-02-13 | conditional | EA-DATA-2026-LY-0008 |
| 2603.09056: Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning | 2026-03-10 | support | EA-DATA-2026-LY-0001 |
| 2603.11634: Diversity You Can Actually Measure: A Fast, Model-Free Diversity Metric for Robotics Datasets | 2026-03-12 | conditional | EA-DATA-2026-LY-0004 |
| 2603.17189: Influence of Gripper Design on Human Demonstration Quality for Robot Learning | 2026-03-17 | limit, support | EA-DATA-2026-LY-0009; UMI-6M-002 |
| 2604.10647: OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction | unknown-date | conditional | UMI-6M-003 |
| 2604.14089: UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception | unknown-date | limit | UMI-6M-004 |
| 2605.01544: An Efficient Metric for Data Quality Measurement in Imitation Learning | 2026-05-02 | support | EA-DATA-2026-LY-0003 |
| 2605.26349: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Co... | 2026-05-25 | support | EA-DATA-2026-LY-0002 |
| 2606.06033: RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning | unknown-date | support | UMI-6M-005 |
| 2606.12365: Ambient Diffusion Policy: Imitation Learning from Suboptimal Data in Robotics | 2026-06-10 | conditional | EA-DATA-2026-LY-0012 |
| 2606.16208: ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation | 2026-06-15 | support | EA-DATA-2026-LY-0005 |
| 2606.28320: WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation | 2026-06-26 | conditional | EA-DATA-2026-LY-0006 |
| 2607.02642: GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | support | EA-EVAL-2026-DQ-0004 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-SENSOR-2026-DQ-0006 |
| 2607.05390: Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | support | EA-SENSOR-2026-DQ-0005 |
| 2607.06442: SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | limit | EA-DATA-2026-DQ-0001 |
| 2607.06558: RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | conditional | EA-DATA-2026-DQ-0003 |
| 2607.06564: Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | support | EA-DATA-2026-DQ-0002 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-2026-LY-0001 | EA-DATA | `support` | `direct` | 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 | 论文指出人类遥操作会带来错误、操作约束、技能差异、噪声和次优行为；QoQ 用 influence functions 衡量训练 state-action 对验证示范的贡献，并在轨迹层聚合以降低噪声、保持覆盖，在仿真、真实机器人和 DROID in-the-wild 数据上改善策略成功率。 (I INTRODUCTION; II-B Robot data curation; VI CONCLUSIONS) | haeone-lee; taywon-min; junsu-kim; et al. | 2603.09056 |
| EA-DATA-2026-LY-0009 | EA-DATA | `support` | `direct` | 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 | 论文指出 UMI 示教虽快于遥操作但仍比手工慢、工具重量会造成疲劳并影响 demonstration；实验中改变 UMI gripper fingers 的力分布显著影响打开绷带包装表现，concentrated load grippers 优于 distributed load grippers，作者将其连接到 demonstration quality 和 learned robot control policies。 (II-A... | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | 2603.17189 |
| EA-DATA-2026-LY-0003 | EA-DATA | `support` | `direct` | 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 | 论文把 poor-quality end-user demonstrations 具体化为 excessive corrective motions、oscillations 和 abrupt adjustments，并提出基于 demonstration trajectories PSD 的自动排序指标；实验比较未筛选、oracle、现有排序和 jerk/path-length 等 baseline，研究 PSD 筛选对下游 IL... | noushad-sojib; momotaz-begum | 2605.01544 |
| EA-DATA-2026-LY-0002 | EA-DATA | `support` | `direct` | 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 | DQAF 框架从 sub-task progress、motion smoothness、stalls、kinematic limits 抽取质量信号，生成结构化质量评估和自然语言纠正建议；pilot study 中即时反馈条件呈现更高任务完成度、更高 episode-level quality scores 和更少 detected suboptimalities 的趋势。 (I INTRODUCTION; Abstract; V-... | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | 2605.26349 |
| EA-DATA-2026-LY-0005 | EA-DATA | `support` | `direct` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 | ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。 (1 Introduction; 2 R... | tao-xu; jiaxin-wang; runhao-zhang; et al. | 2606.16208 |
| EA-DATA-2026-DQ-0002 | EA-DATA | `support` | `direct` | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | 论文将 2D VLA 的困难归因于几何理解和空间推理不足、3D 数据和强 3D encoder 稀缺、跨模态 lifting/projection 损失几何 fidelity；其 GC-MAE 用伪点云监督当前点云重建和未来几何演化，并在仿真与真实任务中提升成功率。 (Abstract; I Introduction; IV-C Geometry-Centric Masked Autoencoding; V-B Multi-Task... | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | 2607.06564 |
| UMI-6M-001 | EA-DATA | `conditional` | `direct` | UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision... | The HTML full text reports that UMI-FT mounts compact six-axis force/torque sensors on each finger, uses multimodal demonstrations to train adaptive compliance policies, and shows diverse in-the-wild data outperforming... | choi-hojung; hou-yifan; pan-chuer; et al. | 2601.09988 |
| EA-DATA-2026-LY-0010 | EA-DATA | `conditional` | `direct` | VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 | 论文指出 VR 用于记录机器人学习示教时，visual fidelity 可能不如 user behavior 的 quality/reliability 重要；输入设备与可视化会影响工作负荷、运动效率、不必要动作和执行精度。实验发现 controller 与 motion-capture gloves 在 pick-and-place 与 manner-oriented tasks 上呈现不同轨迹策略和权衡。 (1 Introduc... | robin-beierling; manuel-scheibl; jonas-dech; et al. | 2602.10618 |
| EA-DATA-2026-LY-0008 | EA-DATA | `conditional` | `direct` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 | PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。 (1 Introduction; 3.3 T... | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | 2602.13197 |
| EA-DATA-2026-LY-0004 | EA-DATA | `conditional` | `direct` | 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 | FAKTUAL 用 signature-kernel entropy 直接在 demonstration dataset 上度量多样性并选择高熵子集；作者在结论中明确说明该方法不像其他 data curation 策略那样保证只选高质量轨迹，若数据集中存在有害轨迹，最 diverse 子集可能反而有损。 (I Introduction; Abstract; IX Conclusion and Limitations) | sreevardhan-sirigiri; nathan-samuel-de-lara; christopher-agia; et al. | 2603.11634 |
| EA-DATA-2026-LY-0012 | EA-DATA | `conditional` | `direct` | 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 | Ambient Diffusion Policy 指出高质量任务专用机器人数据昂贵，而 failures、不同质量轨迹、仿真、跨本体和 egocentric video 等 suboptimal/OOD sources 很丰富；作者认为过滤会浪费数据，常规 co-training 又会学习 harmful parts，因此提出 noise-dependent data usage，只在特定 diffusion times 让 subo... | adam-wei; nicholas-pfaff; thomas-cohn; et al. | 2606.12365 |
| EA-DATA-2026-LY-0006 | EA-DATA | `conditional` | `direct` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 | 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action... | justin-yu; andrew-goldberg; kavish-kondap; et al. | 2606.28320 |
| EA-DATA-2026-DQ-0003 | EA-DATA | `conditional` | `direct` | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | 论文认为物理遥操作把每条示教绑定到操作者、硬件和固定 workspace，难覆盖长尾交互；RynnWorld-Teleop 用动作条件世界模型从手姿流生成机器人中心视频和可 retarget 的动作标签，作为模仿学习数据。但作者也列出细粒度液体/高形变物体和 per-platform fine-tuning 等限制。 (Abstract; 1 Introduction; 4 RynnWorld-Teleop as a Digital... | haoyu-zhao; xingyue-zhao; hangyu-li; et al. | 2607.06558 |
| UMI-6M-002 | EA-DATA | `limit` | `direct` | UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefu... | The HTML full text frames UMI grippers as promising data-collection tools but reports that concentrated-load grippers improve over distributed-load grippers while both remain slower and less effective than hands, with d... | georgadarellis-gina-l; beslic-natalija; lee-seonhun; et al. | 2603.17189 |
| EA-DATA-2026-DQ-0001 | EA-DATA | `limit` | `direct` | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | 论文指出大规模机器人示教池常含轨迹冗余、噪声示教、次优行为和任务覆盖不均；SIEVE 按可复用 primitive 与 transition 选择中心、稳定、适合模仿的轨迹，在多数据集和 VLA 模型上可用 50% 示教与 50% 训练步数超过全量训练。 (Abstract; Introduction; SIEVE; Conclusion) | changti-wu; bin-yu; zhaolong-shen; et al. | 2607.06442 |
| EA-EVAL-2026-DQ-0004 | EA-EVAL | `support` | `direct` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-trai... | gigaworld-team; angyuan-ma; boyuan-wang; et al. | 2607.02642 |
| EA-SENSOR-2026-DQ-0005 | EA-SENSOR | `support` | `direct` | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | 论文认为形变物体有高维状态和复杂材料属性，接触诱发的局部形变常被末端执行器或物体遮挡；已有数据集常缺对象多样性、依赖合成数据，或缺高保真标注与接触形变。Deform360 采集 198 个日常物体、1,980 个交互序列、215 小时以上数据、41 个环视相机和双臂触觉 UMI gripper，并用 markerless 3D tracking 提取稠密几何与运动。 (Abstract; 1 Introduction; 2 Relat... | hongyu-li; wanjia-fu; xiaoyan-cong; et al. | 2607.05390 |
| UMI-6M-003 | EA-SENSOR | `conditional` | `direct` | UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical inter... | The HTML full text repeatedly identifies limited physical interaction signals as a bottleneck of existing UMI-like systems and proposes synchronized RGB, depth, trajectory, tactile sensing, internal grasping force, and... | luo-shaqi; li-yuanyuan; hu-youhao; et al. | 2604.10647 |
| UMI-6M-004 | EA-SENSOR | `limit` | `direct` | Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves... | The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration d... | wang-ziming | 2604.14089 |
| EA-SENSOR-2026-DQ-0006 | EA-SENSOR | `limit` | `direct` | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | 论文指出 VLA 在接触丰富任务中会因轻微接触扰动产生不可恢复失败，这些失败难以从视觉单独检测；TACO 用 tactile-aware world model 将真实 rollout 中的失败邻近状态转成想象的视触觉纠正片段和可执行纠正动作，在真实接触任务中相对 base policy 提升 44 个百分点成功率。 (Abstract; 1 Introduction; 2 Related Work; 3 Method; 5 Conc... | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |
| UMI-6M-005 | EA-XEMBODIMENT | `support` | `direct` | For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action space, avoiding retar... | The HTML full text argues that retargeting and embodiment conversion can distort contact-rich interactions, then presents RealDexUMI as a retargeting-free wearable interface whose shared hand and sensing modules preserv... | xu-chaoyi; jiang-yixuan; huan-jiahui; et al. | 2606.06033 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-2026-LY-0001 | haeone-lee; taywon-min; junsu-kim; et al. | unlisted | `support` | 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 |
| EA-DATA-2026-LY-0009 | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | unlisted | `support` | 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 |
| EA-DATA-2026-LY-0003 | noushad-sojib; momotaz-begum | unlisted | `support` | 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 |
| EA-DATA-2026-LY-0002 | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | unlisted | `support` | 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 |
| EA-DATA-2026-LY-0005 | tao-xu; jiaxin-wang; runhao-zhang; et al. | unlisted | `support` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 |
| EA-DATA-2026-DQ-0002 | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | unlisted | `support` | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 |
| UMI-6M-001 | choi-hojung; hou-yifan; pan-chuer; et al. | unlisted | `conditional` | UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also... |
| EA-DATA-2026-LY-0010 | robin-beierling; manuel-scheibl; jonas-dech; et al. | unlisted | `conditional` | VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 |
| EA-DATA-2026-LY-0008 | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | unlisted | `conditional` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 |
| EA-DATA-2026-LY-0004 | sreevardhan-sirigiri; nathan-samuel-de-lara; christopher-agia; et al. | unlisted | `conditional` | 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 |
| EA-DATA-2026-LY-0012 | adam-wei; nicholas-pfaff; thomas-cohn; et al. | unlisted | `conditional` | 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 |
| EA-DATA-2026-LY-0006 | justin-yu; andrew-goldberg; kavish-kondap; et al. | unlisted | `conditional` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 |
| EA-DATA-2026-DQ-0003 | haoyu-zhao; xingyue-zhao; hangyu-li; et al. | unlisted | `conditional` | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 |
| UMI-6M-002 | georgadarellis-gina-l; beslic-natalija; lee-seonhun; et al. | unlisted | `limit` | UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore d... |
| EA-DATA-2026-DQ-0001 | changti-wu; bin-yu; zhaolong-shen; et al. | unlisted | `limit` | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 |
| EA-EVAL-2026-DQ-0004 | gigaworld-team; angyuan-ma; boyuan-wang; et al. | unlisted | `support` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 |
| EA-SENSOR-2026-DQ-0005 | hongyu-li; wanjia-fu; xiaoyan-cong; et al. | unlisted | `support` | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 |
| UMI-6M-003 | luo-shaqi; li-yuanyuan; hu-youhao; et al. | unlisted | `conditional` | UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multi... |
| UMI-6M-004 | wang-ziming | unlisted | `limit` | Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric... |
| EA-SENSOR-2026-DQ-0006 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 |
| UMI-6M-005 | xu-chaoyi; jiang-yixuan; huan-jiahui; et al. | unlisted | `support` | For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action s... |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-2026-LY-0001`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
- `EA-DATA-2026-LY-0009`: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
- `EA-DATA-2026-LY-0003`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。
- `EA-DATA-2026-LY-0002`: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。
- `EA-DATA-2026-LY-0005`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
- `EA-DATA-2026-DQ-0002`: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。
- `EA-EVAL-2026-DQ-0004`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- `EA-SENSOR-2026-DQ-0005`: 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。
### 条件成立
- `UMI-6M-001`: UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only data is insufficient fo...
- `EA-DATA-2026-LY-0010`: VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。
- `EA-DATA-2026-LY-0008`: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- `EA-DATA-2026-LY-0004`: 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。
- `EA-DATA-2026-LY-0012`: 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。
- `EA-DATA-2026-LY-0006`: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- `EA-DATA-2026-DQ-0003`: 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。
- `UMI-6M-003`: UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data.
### 限制与失败模式
- `UMI-6M-002`: UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefulness.
- `EA-DATA-2026-DQ-0001`: VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。
- `UMI-6M-004`: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible ta...
- `EA-SENSOR-2026-DQ-0006`: 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 20 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DATA-2026-LY-0001` 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
  - `EA-DATA-2026-LY-0009` 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
  - `EA-DATA-2026-LY-0003` 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。
- Scientific memo preview: 《近半年 UMI 数据质量》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近半年 UMI 数据质量 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近半年 UMI 数据质量: 先看证据边界，再谈一个可传播的反常识洞察。

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
