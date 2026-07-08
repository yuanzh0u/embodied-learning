# Review Packet: 4D时空推理对数据的需求

## Scope

- Topic: 4D时空推理对数据的需求
- Time range: 2025-12-12..2026-06-12
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-MODEL`, `EA-EVAL`
- Evidence events: 20
- Topic cards: 4
- Registered source IDs available: `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: planner -> hub -> review packet -> style menu.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for retrieval, HTML mining, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 20
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-2026-4DDATA-0001`, `EA-DATA-2026-4DDATA-0005`, `EA-DATA-2026-4DDATA-0008`, `EA-DATA-2026-4DDATA-0009`, `EA-DATA-2026-4DDATA-0017`, `EA-DATA-2026-4DDATA-0004`, `EA-DATA-2026-4DDATA-0002`, `EA-DATA-2026-4DDATA-0006`, `EA-DATA-2026-4DDATA-0010`, `EA-DATA-2026-4DDATA-0018`, `EA-DATA-2026-4DDATA-0016`, `EA-DATA-2026-4DDATA-0014`
- Registered sources: `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Paper-level sources: 10 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、时间同步、标定、动作表示、元数据、采集员规范和质量审计组成的工程体系。UMI 更接近可学控制数据，Ego/Ego4D 更接近感知与任务先验，DROID 展示了自然场景大规模机器人数据的组织难度。泛化任务优先任务/场景多样性，工业单任务优先数据精度、边界工况和失败恢复。遮挡、异构数据有效性和单视角限制必须用任务相关指标验证。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是基础能力底座，但不是完整机器人感知系统。RGB 擅长语义和外观，弱于深度、接触、力、摩擦、滑移、材料和被遮挡几何。3D/点云在空间约束和精密操作中改变上限，触觉与力/力矩在接触闭环中提供视觉无法直接观测的状态。多模态建模的目标不是堆传感器，而是让每个模态对应可验证的控制收益。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-MODEL` 模型与预训练: 机器人统一模型会成为重要方向，但短中期更可能是“共享骨干 + 本体/任务适配器”，而不是一个模型直接控制所有机器人。当前已有机器人基础模型雏形，但不具备大语言模型那样的成熟度，因为机器人数据昂贵、动作空间异构、评测必须闭环、失败有物理代价。预训练价值应通过目标任务真实闭环样本复杂度下降来验证，而不是只看训练 loss 或 benchmark 分数。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功率。闭环评测难在误差会改变后续观测并累积，还涉及硬件安全、任务重置、失败恢复和随机接触。当前没有覆盖全行业、全本体、全任务的统一评测体系，未来更可能按任务族分层。世界模型当前主要解决预测、想象和筛选问题，能辅助规划和降低试错成本，但还不能替代真实环境验证。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 9 |
| `conditional` | 条件成立 | 7 |
| `limit` | 限制/负面 | 2 |
| `gap` | 缺口 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | conditional, support | EA-MODEL-2026-4DDATA-0003; EA-DATA-2026-4DDATA-0004 |
| 2603.08485: 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos | 2026-03-09 | conditional, support | EA-DATA-2026-4DDATA-0001; EA-DATA-2026-4DDATA-0002 |
| 2603.16669: Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation | 2026-03-17 | conditional, support | EA-DATA-2026-4DDATA-0005; EA-DATA-2026-4DDATA-0006 |
| 2603.17189: Influence of Gripper Design on Human Demonstration Quality for Robot Learning | 2026-03-17 | gap, limit | EA-DATA-2026-4DDATA-0019; EA-DATA-2026-4DDATA-0020 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | limit, support | EA-MODEL-2026-4DDATA-0007; EA-DATA-2026-4DDATA-0008 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional, support | EA-DATA-2026-4DDATA-0009; EA-DATA-2026-4DDATA-0010 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional, support | EA-DATA-2026-4DDATA-0017; EA-DATA-2026-4DDATA-0018 |
| 2606.08737: Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation | 2026-06-07 | conditional, support | EA-SENSOR-2026-4DDATA-0015; EA-DATA-2026-4DDATA-0016 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional, support | EA-SENSOR-2026-4DDATA-0013; EA-DATA-2026-4DDATA-0014 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | gap, support | EA-EVAL-2026-4DDATA-0011; EA-SENSOR-2026-4DDATA-0012 |

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
| EA-DATA-2026-4DDATA-0006 | EA-DATA | `conditional` | `direct` | 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 | Kinema4D补充材料说明ST-v2生成的4D伪标注未必达到绝对亚毫米真值，但足以学习相对几何；LIBERO数据生成中还从成功轨迹注入不同强度动作噪声，合成九种失败轨迹。 (Supplementary G.2 Dataset; Acquisition of LIBERO simulated data; The underlying logic behind 4D pseudo annotation) | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-DATA-2026-4DDATA-0010 | EA-DATA | `conditional` | `direct` | 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 | 论文把真实robot data、UMI-style data和egocentric videos划分为不同监督等级，并用modality-specific supervision masks让每条样本只参与其实际拥有的视觉、状态、动作和进度损失。 (I Introduction; III Data Sources for Predictive Robot Learning; Unified supervision; IV-C Join... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-DATA-2026-4DDATA-0018 | EA-DATA | `conditional` | `direct` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 | HapTile说明所有模态通过机器人控制循环同步，检查空/损坏轨迹和timestamp gaps，验证action-state consistency；附录还要求episode-level split避免temporal leakage，并保留raw/rectified tactile images。 (3.2 Synchronization and Data Quality Control; A.1 Data Formatting;... | amirhosein-alian; yongqiang-zhao; shiyi-gu | 2606.04825 |
| EA-DATA-2026-4DDATA-0016 | EA-DATA | `conditional` | `direct` | 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 | Dream-Tac的contact gate直接从左右指尖触觉RGB的帧间平均绝对差得到，经过鲁棒归一化后在接触变化时提高触觉token注意力；附录统计显示大多数变化很小，较大变化对应关键交互事件。 (3.3 Contact-Aware Self Attention; A.6 Contact Gate Statistics) | yunfan-lou; yifan-ye; yankai-fu | 2606.08737 |
| EA-DATA-2026-4DDATA-0014 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation; IV-C Main Results; Table I) | yujie-zang; yuhang-zheng; xian-nie | 2606.11184 |
| EA-DATA-2026-4DDATA-0019 | EA-DATA | `limit` | `direct` | 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 | 该研究在医用绷带打开任务中比较不同UMI夹爪条件和裸手，发现集中载荷夹爪优于分布载荷夹爪，但仍明显慢于手；作者强调力分布、刚度和人体工学会影响示教质量和工作负荷。 (Abstract; II-A Performance and Usability Limitations; V Discussion; VI Conclusion) | gina-l-georgadarellis; natalija-beslic; seonhun-lee | 2603.17189 |
| EA-DATA-2026-4DDATA-0020 | EA-DATA | `gap` | `direct` | 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 | 作者指出UMI完整学习流程通常至少需要200条固定环境任务示教，手持夹爪仍可能比裸手慢；研究中的夹爪未集成完整传感/marker pipeline，后续需把传感和跟踪能力纳入完整示教到机器人流程评估。 (II-A Performance and Usability Limitations; V Discussion; VI Conclusion) | gina-l-georgadarellis; natalija-beslic; seonhun-lee | 2603.17189 |
| EA-EVAL-2026-4DDATA-0011 | EA-EVAL | `support` | `direct` | 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。 | WEAVER在DROID上预训练并在真实任务数据上微调，输入右侧外部相机和腕部相机、proprioceptive state、action plan、memory/history latents，并蒸馏奖励/critic头来快速评分候选动作。 (3 WEAVER; 3.1 Key Design Decisions; 3.3 Accurate and Efficient Value Estimation; 4 Experimental... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |
| EA-MODEL-2026-4DDATA-0003 | EA-MODEL | `support` | `direct` | 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 | Pri4R指出动作标签主要鼓励模仿示教动作，但不给出世界动态；它给VLA添加点轨迹头，监督未来3D位移，训练后丢弃辅助头而不增加推理输入和计算。 (I Introduction; IV Pri4R: Learning World Dynamics via Privileged 4D Representations; IV-C Construction of 3D Point Track Supervision) | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-MODEL-2026-4DDATA-0007 | EA-MODEL | `limit` | `direct` | 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 | GEM-4D指出像素或latent重建损失不能保证对应一致，可能出现接触漂移、深度不一致和非刚性变形；这些视觉上微妙的错误会破坏从视频rollout提取动作。 (Abstract; 1 Introduction; 3.1 Problem Formulation; 3.2.1 What Governs Inter-Frame Correspondence) | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-SENSOR-2026-4DDATA-0015 | EA-SENSOR | `support` | `direct` | 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。 | Dream-Tac把当前视觉/触觉/语言作为条件，联合去噪未来视觉、未来触觉和动作chunk；其contact-aware self-attention用相邻触觉帧变化计算事件门控，强调接触发生、滑移或释放等时刻。 (Abstract; 3.1 Problem Formulation; 3.2 Dream-Tac Architecture; 3.3 Contact-Aware Self Attention) | yunfan-lou; yifan-ye; yankai-fu | 2606.08737 |
| EA-SENSOR-2026-4DDATA-0013 | EA-SENSOR | `support` | `direct` | 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。 | TacForeSight训练force-conditioned tactile world model，用高频wrist force/torque条件预测短时未来触觉latent；作者报告wrist wrench条件在MSE、cosine similarity和KL上优于无条件、RGB和机器人状态条件。 (Abstract; III-A Force-conditioned Tactile World Model; IV-D 1 Wor... | yujie-zang; yuhang-zheng; xian-nie | 2606.11184 |
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
| EA-DATA-2026-4DDATA-0006 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `conditional` | 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 |
| EA-DATA-2026-4DDATA-0010 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 |
| EA-DATA-2026-4DDATA-0018 | amirhosein-alian; yongqiang-zhao; shiyi-gu | unlisted | `conditional` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 |
| EA-DATA-2026-4DDATA-0016 | yunfan-lou; yifan-ye; yankai-fu | unlisted | `conditional` | 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 |
| EA-DATA-2026-4DDATA-0014 | yujie-zang; yuhang-zheng; xian-nie | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-DATA-2026-4DDATA-0019 | gina-l-georgadarellis; natalija-beslic; seonhun-lee | unlisted | `limit` | 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 |
| EA-DATA-2026-4DDATA-0020 | gina-l-georgadarellis; natalija-beslic; seonhun-lee | unlisted | `gap` | 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 |
| EA-EVAL-2026-4DDATA-0011 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `support` | 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。 |
| EA-MODEL-2026-4DDATA-0003 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `support` | 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 |
| EA-MODEL-2026-4DDATA-0007 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `limit` | 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 |
| EA-SENSOR-2026-4DDATA-0015 | yunfan-lou; yifan-ye; yankai-fu | unlisted | `support` | 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。 |
| EA-SENSOR-2026-4DDATA-0013 | yujie-zang; yuhang-zheng; xian-nie | unlisted | `support` | 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。 |
| EA-SENSOR-2026-4DDATA-0012 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `gap` | 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-2026-4DDATA-0001`: 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。
- `EA-DATA-2026-4DDATA-0005`: 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。
- `EA-DATA-2026-4DDATA-0008`: 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。
- `EA-DATA-2026-4DDATA-0009`: 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。
- `EA-DATA-2026-4DDATA-0017`: 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。
- `EA-EVAL-2026-4DDATA-0011`: 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。
- `EA-MODEL-2026-4DDATA-0003`: 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。
- `EA-SENSOR-2026-4DDATA-0015`: 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。
### 条件成立
- `EA-DATA-2026-4DDATA-0004`: 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。
- `EA-DATA-2026-4DDATA-0002`: 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。
- `EA-DATA-2026-4DDATA-0006`: 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。
- `EA-DATA-2026-4DDATA-0010`: 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。
- `EA-DATA-2026-4DDATA-0018`: 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- `EA-DATA-2026-4DDATA-0016`: 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。
- `EA-DATA-2026-4DDATA-0014`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
### 限制与失败模式
- `EA-DATA-2026-4DDATA-0019`: 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。
- `EA-MODEL-2026-4DDATA-0007`: 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。
### 开放问题
- `EA-DATA-2026-4DDATA-0020`: 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。
- `EA-SENSOR-2026-4DDATA-0012`: 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 10 / 5
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
