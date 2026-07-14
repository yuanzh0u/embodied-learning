# Review Packet: 4D时空推理对数据的需求

## Scope

- Topic: 4D时空推理对数据的需求
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-4D`, `EA-DATA`, `EA-EVAL`, `EA-MODEL`, `EA-SENSOR`
- Evidence events: 40
- Topic cards: 5
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> full-text evidence -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval, HTML/PDF/OCR recovery, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 40
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-2026-4DDATA-0001`, `EA-DATA-2026-4DDATA-0005`, `EA-DATA-2026-4DDATA-0008`, `EA-DATA-2026-4DDATA-0009`, `EA-DATA-2026-4DDATA-0017`, `EA-DATA-2026-4DDATA-0004`, `EA-DATA-2026-4DDATA-0002`, `EA-DATA-2026-4D-0007`, `EA-DATA-2026-4DDATA-0006`, `EA-DATA-2026-4D-0011`, `EA-DATA-2026-4DDATA-0010`, `EA-DATA-2026-4DDATA-0018`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-4D` 4D 时空推理与世界动态: 具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。
  - 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
  - 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
  - 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
  - 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
  - 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。
- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；高分筛选还必须保留任务、本体、场景和长尾覆盖。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。所有异构数据都应声明其可信监督字段，并以真实闭环收益作为最终验收。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测应分开记录预测保真与决策有效，防止“视频更真实”掩盖错误动作响应。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。VLA 可以继承视觉和语言先验，却不会自动继承运动、接触和控制器先验；语言—视觉—动作接口需要显式对齐。4D 和世界模型可以提供几何动态监督、未来想象和动作筛选，但训练目标必须面向动作质量而非只追求视觉重建。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；触觉世界模型应预测动作条件下的接触演化，而不只是重建触觉图像。多模态建模的目标不是堆传感器，而是让每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 19 |
| `conditional` | 条件成立 | 11 |
| `limit` | 限制/负面 | 6 |
| `gap` | 缺口 | 4 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | conditional, gap, support | EA-DATA-2026-4DDATA-0004; EA-EVAL-2026-4D-0004; EA-MODEL-2026-4D-0003; EA-MODEL-2026-4D-0005; EA-MODEL-2026-4DDATA-0003 |
| 2603.08485: 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos | 2026-03-09 | conditional, support | EA-DATA-2026-4DDATA-0001; EA-DATA-2026-4DDATA-0002 |
| 2603.13788: ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation | 2026-03-14 | conditional, support | EA-EVAL-2026-4D-0002; EA-MODEL-2026-4D-0001 |
| 2603.15467: Evaluating Time Awareness and Cross-modal Active Perception of Large Models via 4D Escape Room Task | 2026-03-16 | gap | EA-EVAL-2026-4D-0020 |
| 2603.16669: Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation | 2026-03-17 | conditional, support | EA-DATA-2026-4D-0007; EA-DATA-2026-4DDATA-0005; EA-DATA-2026-4DDATA-0006; EA-EVAL-2026-4D-0006 |
| 2603.17189: Influence of Gripper Design on Human Demonstration Quality for Robot Learning | 2026-03-17 | gap, limit | EA-DATA-2026-4DDATA-0019; EA-DATA-2026-4DDATA-0020 |
| 2605.00121: Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes | 2026-04-30 | limit, support | EA-SENSOR-2026-4D-0015; EA-SENSOR-2026-4D-0016 |
| 2605.17682: GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning | 2026-05-17 | support | EA-SENSOR-2026-4D-0019 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | limit, support | EA-DATA-2026-4DDATA-0008; EA-MODEL-2026-4D-0008; EA-MODEL-2026-4D-0009; EA-MODEL-2026-4DDATA-0007 |
| 2605.29879: DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding | 2026-05-28 | limit, support | EA-SENSOR-2026-4D-0017; EA-SENSOR-2026-4D-0018 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional, support | EA-DATA-2026-4D-0011; EA-DATA-2026-4DDATA-0009; EA-DATA-2026-4DDATA-0010; EA-EVAL-2026-4D-0012; EA-MODEL-2026-4D-0010 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional, support | EA-DATA-2026-4DDATA-0017; EA-DATA-2026-4DDATA-0018 |
| 2606.08737: Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation | 2026-06-07 | conditional, support | EA-DATA-2026-4DDATA-0016; EA-SENSOR-2026-4DDATA-0015 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional, support | EA-DATA-2026-4DDATA-0014; EA-SENSOR-2026-4DDATA-0013 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | gap, limit, support | EA-EVAL-2026-4D-0013; EA-EVAL-2026-4D-0014; EA-EVAL-2026-4DDATA-0011; EA-SENSOR-2026-4DDATA-0012 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-2026-4DDATA-0001 | EA-DATA | `support` | `direct` | 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 | 3PoinTr先从无动作人类视频学习非 embodiment 点的密集3D点轨迹，再用20条机器人动作示教训练闭环策略；论文报告真实任务平均成功率相对最强基线提高25.0个百分点。 (Abstract; 1 Introduction; 4.1 Data collection; 4.4 Results) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | 2603.08485 |
| EA-DATA-2026-4DDATA-0005 | EA-DATA | `support` | `direct` | 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 | Kinema4D用URDF/重建机器人经正逆运动学产生4D robot pointmap控制信号，再训练模型生成同步RGB和pointmap未来；其Robo4D-200k包含201,426个带高质量4D标注的交互episode。 (Abstract; 1 Introduction; 3.1 Kinematics Control; 3.2 4D Generative Modeling; 3.3 Robo4D-200k) | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-DATA-2026-4DDATA-0008 | EA-DATA | `support` | `direct` | 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 | GEM-4D冻结几何基础模型，提取稠密几何表示作为correspondence teacher，并通过geometry flow把监督蒸馏进视频backbone；训练后几何分支丢弃，推理仍是单流视频生成。 (2.2 Feed-Forward 3D and 4D Geometry Models; 3.2.3 Correspondence Distillation via Geometry Flow; 5 Conclusion) | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-DATA-2026-4DDATA-0009 | EA-DATA | `support` | `direct` | 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 | τ0-WM构建27.3K小时语料：17.8K小时真实机器人远程操作、6.5K小时UMI式示教、3.0K小时开源第一视角人类交互视频，并用rollout或失败轨迹训练任务进度/低质量结果评估。 (Abstract; III Data Sources for Predictive Robot Learning; A Training Configuration) | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-DATA-2026-4DDATA-0017 | EA-DATA | `support` | `direct` | 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 | HapTile提供1,726条示教、38个任务、9类技能，15Hz同步语言、视觉、触觉、机器人状态和动作；其teleoperation平台还将触觉marker motion转成操作者侧haptic feedback。 (Abstract; 3.1 Dataset Statistics; 4 Data Collection Platform; 4.3 Haptic Feedback to the Operator) | amirhosein-alian; yongqiang-zhao; shiyi-gu | 2606.04825 |
| EA-DATA-2026-4DDATA-0004 | EA-DATA | `conditional` | `direct` | 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 | Pri4R比较多种监督目标，认为3D点轨迹兼具时间密集、几何度量和空间稀疏；附录中1024个点优于256/512点，且没有当前点云输入会退化，因为模型必须凭空生成而非预测给定场景演化。 (IV-B Why 3D Point Tracks as Privileged Supervision; S.III-A Additional Analysis on input; S.III-C Additional Ablations) | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-DATA-2026-4DDATA-0002 | EA-DATA | `conditional` | `direct` | 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 | 论文用可见性mask保留部分遮挡轨迹并逐点逐时刻mask损失，认为这比丢弃含不可见点的轨迹能提供更多任务关键监督；附录说明真实视频需2D跟踪、深度提升到3D、SAM3分割人手并移除embodiment点。 (4.3 Results: 3D Point Track Prediction; Appendix D Data Collection Details; Appendix G Future Work) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | 2603.08485 |
| EA-DATA-2026-4D-0007 | EA-DATA | `conditional` | `direct` | Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial cons... | The supplementary discussion says ST-v2 pseudo-annotations may not be absolute sub-millimeter ground truth, but are sufficiently high-fidelity for relative spatial geometry; the authors prioritize breadth of data to lea... | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-DATA-2026-4DDATA-0006 | EA-DATA | `conditional` | `direct` | 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 | Kinema4D补充材料说明ST-v2生成的4D伪标注未必达到绝对亚毫米真值，但足以学习相对几何；LIBERO数据生成中还从成功轨迹注入不同强度动作噪声，合成九种失败轨迹。 (Supplementary G.2 Dataset; Acquisition of LIBERO simulated data; The underlying logic behind 4D pseudo annotation) | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-DATA-2026-4D-0011 | EA-DATA | `conditional` | `direct` | τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding. | The introduction contrasts broad visual dynamics in egocentric and human interaction video with narrow but executable robot demonstrations, then uses modality-specific supervision masks so each data source supervises on... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-DATA-2026-4DDATA-0010 | EA-DATA | `conditional` | `direct` | 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 | 论文把真实robot data、UMI-style data和egocentric videos划分为不同监督等级，并用modality-specific supervision masks让每条样本只参与其实际拥有的视觉、状态、动作和进度损失。 (I Introduction; III Data Sources for Predictive Robot Learning; Unified supervision; IV-C Join... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-DATA-2026-4DDATA-0018 | EA-DATA | `conditional` | `direct` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 | HapTile说明所有模态通过机器人控制循环同步，检查空/损坏轨迹和timestamp gaps，验证action-state consistency；附录还要求episode-level split避免temporal leakage，并保留raw/rectified tactile images。 (3.2 Synchronization and Data Quality Control; A.1 Data Formatting;... | amirhosein-alian; yongqiang-zhao; shiyi-gu | 2606.04825 |
| EA-DATA-2026-4DDATA-0016 | EA-DATA | `conditional` | `direct` | 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 | Dream-Tac的contact gate直接从左右指尖触觉RGB的帧间平均绝对差得到，经过鲁棒归一化后在接触变化时提高触觉token注意力；附录统计显示大多数变化很小，较大变化对应关键交互事件。 (3.3 Contact-Aware Self Attention; A.6 Contact Gate Statistics) | yunfan-lou; yifan-ye; yankai-fu | 2606.08737 |
| EA-DATA-2026-4DDATA-0014 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation; IV-C Main Results; Table I) | yujie-zang; yuhang-zheng; xian-nie | 2606.11184 |
| EA-DATA-2026-4DDATA-0019 | EA-DATA | `limit` | `direct` | 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 | 该研究在医用绷带打开任务中比较不同UMI夹爪条件和裸手，发现集中载荷夹爪优于分布载荷夹爪，但仍明显慢于手；作者强调力分布、刚度和人体工学会影响示教质量和工作负荷。 (Abstract; II-A Performance and Usability Limitations; V Discussion; VI Conclusion) | gina-l-georgadarellis; natalija-beslic; seonhun-lee | 2603.17189 |
| EA-DATA-2026-4DDATA-0020 | EA-DATA | `gap` | `direct` | 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 | 作者指出UMI完整学习流程通常至少需要200条固定环境任务示教，手持夹爪仍可能比裸手慢；研究中的夹爪未集成完整传感/marker pipeline，后续需把传感和跟踪能力纳入完整示教到机器人流程评估。 (II-A Performance and Usability Limitations; V Discussion; VI Conclusion) | gina-l-georgadarellis; natalija-beslic; seonhun-lee | 2603.17189 |
| EA-EVAL-2026-4D-0004 | EA-EVAL | `support` | `direct` | Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only predic... | The paper compares supervision targets and reports that full-horizon 3D point-track supervision gives larger RoboCasa gains than 2D tracks, goal-only prediction, environment-only points, robot-only points, or future dep... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-EVAL-2026-4D-0006 | EA-EVAL | `support` | `direct` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... | The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap... | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-EVAL-2026-4D-0013 | EA-EVAL | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |
| EA-EVAL-2026-4DDATA-0011 | EA-EVAL | `support` | `direct` | 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。 | WEAVER在DROID上预训练并在真实任务数据上微调，输入右侧外部相机和腕部相机、proprioceptive state、action plan、memory/history latents，并蒸馏奖励/critic头来快速评分候选动作。 (3 WEAVER; 3.1 Key Design Decisions; 3.3 Accurate and Efficient Value Estimation; 4 Experimental... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |
| EA-EVAL-2026-4D-0002 | EA-EVAL | `conditional` | `direct` | ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset... | The evaluation reports 44.6% zero-shot success-rate gains in simulation and 30.3% real-world gains, while the conclusion notes degradation risks in extreme clutter and dependence on single-view execution and SAM2 segmen... | you-wu; zixuan-chen; cunxu-ou | 2603.13788 |
| EA-EVAL-2026-4D-0012 | EA-EVAL | `conditional` | `direct` | τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensing, uncertainty esti... | The experiments report better performance on long-horizon real-robot tasks, data-mixture gains, and a single-attempt success-rate increase from 0.43 to 0.60 with action selection plus rectification; the conclusion notes... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-EVAL-2026-4D-0014 | EA-EVAL | `limit` | `direct` | WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, dat... | The limitations section states that visual observations expose only partial physical state; tactile, force-torque, or depth sensing may be needed; deformable and granular dynamics remain difficult; latency restricts pla... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |
| EA-EVAL-2026-4D-0020 | EA-EVAL | `gap` | `direct` | EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual... | The benchmark introduces time-varying visual and audio cues, trigger-based evidence, and time-limited clues; results show models degrade under modality bias, missed triggers, and time-sensitive decisions, indicating gap... | yurui-dong; ziyue-wang; shuyun-lu | 2603.15467 |
| EA-MODEL-2026-4D-0003 | EA-MODEL | `support` | `direct` | Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geometry evolves over ti... | The authors state that action labels tell a policy how to move but not what will happen; Pri4R adds a point-track head during training and discards it at inference, leaving the original VLA interface unchanged. (Abstrac... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-MODEL-2026-4DDATA-0003 | EA-MODEL | `support` | `direct` | 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 | Pri4R指出动作标签主要鼓励模仿示教动作，但不给出世界动态；它给VLA添加点轨迹头，监督未来3D位移，训练后丢弃辅助头而不增加推理输入和计算。 (I Introduction; IV Pri4R: Learning World Dynamics via Privileged 4D Representations; IV-C Construction of 3D Point Track Supervision) | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-MODEL-2026-4D-0001 | EA-MODEL | `support` | `direct` | ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories and 4D temporal con... | The paper argues that 2D intermediate representations lose depth and temporal continuity, then proposes unified 3D-4D representations with trajectories and smooth spatial masks for online replanning and long-horizon exe... | you-wu; zixuan-chen; cunxu-ou | 2603.13788 |
| EA-MODEL-2026-4D-0009 | EA-MODEL | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-MODEL-2026-4D-0010 | EA-MODEL | `support` | `direct` | τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, then revise low-quality... | The paper describes a unified video-action world model with a video action model and an action-conditioned video simulator; at inference it samples candidates, ranks them, simulates futures, estimates progress, and rect... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-MODEL-2026-4D-0008 | EA-MODEL | `limit` | `direct` | GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences ov... | The introduction says photorealistic generated videos can have drifting contacts, inconsistent depth, and non-rigid deformation artifacts that break action extraction; pixel or latent losses do not guarantee corresponde... | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-MODEL-2026-4DDATA-0007 | EA-MODEL | `limit` | `direct` | 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 | GEM-4D指出像素或latent重建损失不能保证对应一致，可能出现接触漂移、深度不一致和非刚性变形；这些视觉上微妙的错误会破坏从视频rollout提取动作。 (Abstract; 1 Introduction; 3.1 Problem Formulation; 3.2.1 What Governs Inter-Frame Correspondence) | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-MODEL-2026-4D-0005 | EA-MODEL | `gap` | `direct` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. | The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could furth... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-SENSOR-2026-4D-0015 | EA-SENSOR | `support` | `direct` | PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-receptacle states and pl... | The paper builds Perpetua* Bayesian persistence filters into a 3D scene graph, validates future state prediction in simulation and a three-week real-world semi-static lab setting, and shows navigation can avoid an expec... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-SENSOR-2026-4D-0019 | EA-SENSOR | `support` | `direct` | GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autor... | The paper decouples spatial geometry, temporal support, semantics, opacity, and motion in Gaussian primitives, then slices and splats them into future occupancy volumes at arbitrary timestamps and supervises both occupa... | cheng-chen; hao-huang; saurabh-bagchi | 2605.17682 |
| EA-SENSOR-2026-4D-0017 | EA-SENSOR | `support` | `direct` | DGSG-Mind combines dynamic 3D Gaussian mapping with scene graphs so that embodied agents can update object-level topology and reason over spatial-semantic relations in changing en... | The system fuses probabilistic voxels and 3D Gaussians, performs Gaussian-based camera relocalization and localized masked refinement for additions/removals, synchronizes graph nodes, and uses annotated Gaussian renderi... | luzhou-ge; xiangyu-zhu; jinyan-liu | 2605.29879 |
| EA-SENSOR-2026-4DDATA-0015 | EA-SENSOR | `support` | `direct` | 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。 | Dream-Tac把当前视觉/触觉/语言作为条件，联合去噪未来视觉、未来触觉和动作chunk；其contact-aware self-attention用相邻触觉帧变化计算事件门控，强调接触发生、滑移或释放等时刻。 (Abstract; 3.1 Problem Formulation; 3.2 Dream-Tac Architecture; 3.3 Contact-Aware Self Attention) | yunfan-lou; yifan-ye; yankai-fu | 2606.08737 |
| EA-SENSOR-2026-4DDATA-0013 | EA-SENSOR | `support` | `direct` | 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。 | TacForeSight训练force-conditioned tactile world model，用高频wrist force/torque条件预测短时未来触觉latent；作者报告wrist wrench条件在MSE、cosine similarity和KL上优于无条件、RGB和机器人状态条件。 (Abstract; III-A Force-conditioned Tactile World Model; IV-D 1 Wor... | yujie-zang; yuhang-zheng; xian-nie | 2606.11184 |
| EA-SENSOR-2026-4D-0016 | EA-SENSOR | `limit` | `direct` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. | The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and plannin... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-SENSOR-2026-4D-0018 | EA-SENSOR | `limit` | `direct` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. | The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs. (V Conclus... | luzhou-ge; xiangyu-zhu; jinyan-liu | 2605.29879 |
| EA-SENSOR-2026-4DDATA-0012 | EA-SENSOR | `gap` | `direct` | 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 | WEAVER限制部分指出视觉只给部分物理状态，任务相关的接触、力和遮挡几何可能不可见；形变/动态物体、有限规划时域、DROID embodiment覆盖、以及reward labels噪声都是剩余瓶颈。 (A5 Limitations; A5.1 Partial Observability; A5.2 Complex Deformable and Dynamic Interactions; A5.4 Data Coverage and... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-2026-4DDATA-0001 | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | unlisted | `support` | 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 |
| EA-DATA-2026-4DDATA-0005 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `support` | 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 |
| EA-DATA-2026-4DDATA-0008 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `support` | 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 |
| EA-DATA-2026-4DDATA-0009 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `support` | 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 |
| EA-DATA-2026-4DDATA-0017 | amirhosein-alian; yongqiang-zhao; shiyi-gu | unlisted | `support` | 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 |
| EA-DATA-2026-4DDATA-0004 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `conditional` | 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 |
| EA-DATA-2026-4DDATA-0002 | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | unlisted | `conditional` | 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 |
| EA-DATA-2026-4D-0007 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `conditional` | Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning r... |
| EA-DATA-2026-4DDATA-0006 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `conditional` | 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 |
| EA-DATA-2026-4D-0011 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executab... |
| EA-DATA-2026-4DDATA-0010 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 |
| EA-DATA-2026-4DDATA-0018 | amirhosein-alian; yongqiang-zhao; shiyi-gu | unlisted | `conditional` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 |
| EA-DATA-2026-4DDATA-0016 | yunfan-lou; yifan-ye; yankai-fu | unlisted | `conditional` | 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 |
| EA-DATA-2026-4DDATA-0014 | yujie-zang; yuhang-zheng; xian-nie | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-DATA-2026-4DDATA-0019 | gina-l-georgadarellis; natalija-beslic; seonhun-lee | unlisted | `limit` | 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 |
| EA-DATA-2026-4DDATA-0020 | gina-l-georgadarellis; natalija-beslic; seonhun-lee | unlisted | `gap` | 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 |
| EA-EVAL-2026-4D-0004 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `support` | Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D trac... |
| EA-EVAL-2026-4D-0006 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `support` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while... |
| EA-EVAL-2026-4D-0013 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-EVAL-2026-4DDATA-0011 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `support` | 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。 |
| EA-EVAL-2026-4D-0002 | you-wu; zixuan-chen; cunxu-ou | unlisted | `conditional` | ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is... |
| EA-EVAL-2026-4D-0012 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensi... |
| EA-EVAL-2026-4D-0014 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `limit` | WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited pl... |
| EA-EVAL-2026-4D-0020 | yurui-dong; ziyue-wang; shuyun-lu | unlisted | `gap` | EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not on... |
| EA-MODEL-2026-4D-0003 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `support` | Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geom... |
| EA-MODEL-2026-4DDATA-0003 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `support` | 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 |
| EA-MODEL-2026-4D-0001 | you-wu; zixuan-chen; cunxu-ou | unlisted | `support` | ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories... |
| EA-MODEL-2026-4D-0009 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-MODEL-2026-4D-0010 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `support` | τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, the... |
| EA-MODEL-2026-4D-0008 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `limit` | GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3... |
| EA-MODEL-2026-4DDATA-0007 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `limit` | 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 |
| EA-MODEL-2026-4D-0005 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `gap` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. |
| EA-SENSOR-2026-4D-0015 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `support` | PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-rece... |
| EA-SENSOR-2026-4D-0019 | cheng-chen; hao-huang; saurabh-bagchi | unlisted | `support` | GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning with... |
| EA-SENSOR-2026-4D-0017 | luzhou-ge; xiangyu-zhu; jinyan-liu | unlisted | `support` | DGSG-Mind combines dynamic 3D Gaussian mapping with scene graphs so that embodied agents can update object-level topology and reason over spatial-semantic rela... |
| EA-SENSOR-2026-4DDATA-0015 | yunfan-lou; yifan-ye; yankai-fu | unlisted | `support` | 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。 |
| EA-SENSOR-2026-4DDATA-0013 | yujie-zang; yuhang-zheng; xian-nie | unlisted | `support` | 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。 |
| EA-SENSOR-2026-4D-0016 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `limit` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verifica... |
| EA-SENSOR-2026-4D-0018 | luzhou-ge; xiangyu-zhu; jinyan-liu | unlisted | `limit` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. |
| EA-SENSOR-2026-4DDATA-0012 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `gap` | 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-2026-4DDATA-0001`: 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。
- `EA-DATA-2026-4DDATA-0005`: 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。
- `EA-DATA-2026-4DDATA-0008`: 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。
- `EA-DATA-2026-4DDATA-0009`: 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。
- `EA-DATA-2026-4DDATA-0017`: 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。
- `EA-EVAL-2026-4D-0004`: Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only prediction, or dense depth prediction.
- `EA-EVAL-2026-4D-0006`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- `EA-EVAL-2026-4D-0013`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
### 条件成立
- `EA-DATA-2026-4DDATA-0004`: 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。
- `EA-DATA-2026-4DDATA-0002`: 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。
- `EA-DATA-2026-4D-0007`: Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial constraints and motion priors.
- `EA-DATA-2026-4DDATA-0006`: 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。
- `EA-DATA-2026-4D-0011`: τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding.
- `EA-DATA-2026-4DDATA-0010`: 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。
- `EA-DATA-2026-4DDATA-0018`: 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- `EA-DATA-2026-4DDATA-0016`: 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。
### 限制与失败模式
- `EA-DATA-2026-4DDATA-0019`: 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。
- `EA-EVAL-2026-4D-0014`: WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, data coverage, and noisy reward supervision...
- `EA-MODEL-2026-4D-0008`: GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences over time.
- `EA-MODEL-2026-4DDATA-0007`: 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。
- `EA-SENSOR-2026-4D-0016`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- `EA-SENSOR-2026-4D-0018`: DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory.
### 开放问题
- `EA-DATA-2026-4DDATA-0020`: 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。
- `EA-EVAL-2026-4D-0020`: EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual scenes.
- `EA-MODEL-2026-4D-0005`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- `EA-SENSOR-2026-4DDATA-0012`: 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DATA-2026-4DDATA-0001` 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。
  - `EA-DATA-2026-4DDATA-0005` 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。
  - `EA-DATA-2026-4DDATA-0008` 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。
- Scientific memo preview: 《4D时空推理对数据的需求》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 4D时空推理对数据的需求 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 4D时空推理对数据的需求: 先看证据边界，再谈一个可传播的反常识洞察。

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
