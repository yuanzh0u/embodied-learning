# Review Packet: 近一年具身感知问题是否已有效解决

## Scope

- Topic: 近一年具身感知问题是否已有效解决
- Time range: 2025-07-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-SENSOR`, `EA-4D`, `EA-EVAL`
- Evidence events: 20
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> full-text evidence -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval, HTML/PDF/OCR recovery, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 20
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-2026-DQ-0002`, `EA-DATA-2026-4DDATA-0002`, `EA-DATA-2026-4DDATA-0018`, `EA-DATA-2026-4DDATA-0014`, `EA-EVAL-2026-0007`, `EA-SENSOR-2026-0004`, `EA-SENSOR-2026-0003`, `EA-SENSOR-2026-0006`, `EA-SENSOR-2026-0011`, `EA-SENSOR-2026-0009`, `EA-SENSOR-2026-0001`, `EA-PNAV-2026-0002`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 19 / 15 floor (not a cap)
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
- `EA-4D` 4D 时空推理与世界动态: 具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。
  - 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
  - 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
  - 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
  - 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
  - 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测应分开记录预测保真与决策有效，防止“视频更真实”掩盖错误动作响应。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- `ERR-EMBODIED` 具身智能误差分层与溯源: 具身错误不应按“哪个模型模块报错”粗分，而应寻找第一处可证伪偏离点。感知误差发生在真实世界到状态表征：关键状态没被看到、对齐或记录；认知误差发生在状态表征到意图、计划或动作选择：可用状态足够，但任务、约束、阶段或未来后果判断错误。动作转译、控制执行和硬件响应还应单独记账。可靠归因依赖 probing、episode 遥测、对照实验和闭环结果，不能从失败表象直接猜测。
  - “看对了但做错了”可以通过 probing 证明：视觉骨干保持空间表征，而动作头塌缩回记忆轨迹。
  - 动作语义、坐标系、控制频率和本体 adapter 错配常伪装成感知误差。
  - 接触不可见、标定/同步偏差和缺失模态属于感知链问题；失败阶段判断、计划不可行和 what-if 推理缺失属于认知链问题。
  - 失败恢复是最适合分层诊断的实验场：依次检查状态可见、恢复数据存在、失败阶段判断和纠正动作可执行。
  - 世界模型横跨两层：未来状态预测保真属于感知型问题，候选动作排序与拒绝属于认知型问题。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 7 |
| `conditional` | 条件成立 | 9 |
| `limit` | 限制/负面 | 4 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2601.08325: ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation | 2026-01-13 | conditional | EA-PNAV-2026-0002 |
| 2603.08485: 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos | 2026-03-09 | conditional | EA-DATA-2026-4DDATA-0002 |
| 2603.11072: OA-NBV: Occlusion-Aware Next-Best-View Planning for Human-Centered Active Perception on Mobile Robots | 2026-03-10 | conditional | EA-PNAV-2026-0003 |
| 2605.14801: Exploring Bottlenecks in VLM-LLM Navigation: How 3D Scene Understanding Capability Impacts Zero-Shot VLN | 2026-05-14 | conditional | EA-PNAV-2026-0004 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional | EA-DATA-2026-4DDATA-0018 |
| 2606.08765: RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation | 2026-06-07 | conditional | EA-SENSOR-2026-0002 |
| 2606.10348: Rethinking Embodied Navigation via Relational Inductive Bias | 2026-06-09 | limit | EA-PNAV-2026-0013 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional | EA-DATA-2026-4DDATA-0014 |
| 2606.16690: PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation | 2026-06-15 | limit | EA-SENSOR-2026-0005 |
| 2606.18043: Uncertainty Quantification for Flow-Based Vision-Language-Action Models | 2026-06-16 | support | EA-SENSOR-2026-0004 |
| 2606.20754: Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models | 2026-06-18 | support | EA-SENSOR-2026-0003 |
| 2606.26663: Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention | 2026-06-25 | conditional | EA-SENSOR-2026-0008 |
| 2606.28899: You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact | 2026-06-27 | support | EA-SENSOR-2026-0006 |
| 2606.29384: Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model | 2026-06-28 | support | EA-SENSOR-2026-0011 |
| 2606.30988: Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force | 2026-06-29 | conditional | EA-SENSOR-2026-0010 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit, support | EA-SENSOR-2026-0009; EA-SENSOR-2026-DQ-0006 |
| 2607.04234: SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objec... | 2026-07-05 | limit | EA-EVAL-2026-0007 |
| 2607.06564: Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | support | EA-DATA-2026-DQ-0002 |
| 2607.07287: TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation | 2026-07-08 | support | EA-SENSOR-2026-0001 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-2026-DQ-0002 | EA-DATA | `support` | `direct` | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | 论文将 2D VLA 的困难归因于几何理解和空间推理不足、3D 数据和强 3D encoder 稀缺、跨模态 lifting/projection 损失几何 fidelity；其 GC-MAE 用伪点云监督当前点云重建和未来几何演化，并在仿真与真实任务中提升成功率。 (Abstract; I Introduction; IV-C Geometry-Centric Masked Autoencoding; V-B Multi-Task... | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | 2607.06564 |
| EA-DATA-2026-4DDATA-0002 | EA-DATA | `conditional` | `direct` | 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 | 论文用可见性mask保留部分遮挡轨迹并逐点逐时刻mask损失，认为这比丢弃含不可见点的轨迹能提供更多任务关键监督；附录说明真实视频需2D跟踪、深度提升到3D、SAM3分割人手并移除embodiment点。 (4.3 Results: 3D Point Track Prediction; Appendix D Data Collection Details; Appendix G Future Work) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | 2603.08485 |
| EA-DATA-2026-4DDATA-0018 | EA-DATA | `conditional` | `direct` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 | HapTile说明所有模态通过机器人控制循环同步，检查空/损坏轨迹和timestamp gaps，验证action-state consistency；附录还要求episode-level split避免temporal leakage，并保留raw/rectified tactile images。 (3.2 Synchronization and Data Quality Control; A.1 Data Formatting;... | amirhosein-alian; yongqiang-zhao; shiyi-gu | 2606.04825 |
| EA-DATA-2026-4DDATA-0014 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation; IV-C Main Results; Table I) | yujie-zang; yuhang-zheng; xian-nie | 2606.11184 |
| EA-EVAL-2026-0007 | EA-EVAL | `limit` | `direct` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 | 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。 (arXiv HTML Abstract; 1... | bowen-jing | 2607.04234 |
| EA-SENSOR-2026-0004 | EA-SENSOR | `support` | `direct` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 | 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。 (arXiv HTML Abstract; 1 Introduction; Appendix B.4 Uncertainty Quantificat... | ralf-romer | 2606.18043 |
| EA-SENSOR-2026-0003 | EA-SENSOR | `support` | `direct` | VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 | 作者指出现代 VLA 常用回归或 flow-based action generation，缺少显式预测概率；他们通过对 transformer hidden activations 注入高斯扰动，利用扰动后动作预测分歧估计不确定性，并在 LIBERO/LIBERO-PRO 的分布偏移下提升失败检测。 (arXiv HTML Abstract; I Introduction; IV-D Main Results) | yousung-lee | 2606.20754 |
| EA-SENSOR-2026-0006 | EA-SENSOR | `support` | `direct` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 | 作者明确指出视觉位姿估计常在遮挡、差光照、反光或透明表面下失败，并提出 tactile-only pose estimation：把触觉接触表示成局部 3D 点云，结合校准传感器位姿恢复完整 6-DoF object pose；实验在视觉不可靠时优于视觉和几何基线。 (arXiv HTML Abstract; 1 Introduction; 4.2 6-DoF Object Pose Estimation under Occlusio... | pengfei-ye | 2606.28899 |
| EA-SENSOR-2026-0011 | EA-SENSOR | `support` | `direct` | RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 | 作者指出现有 VLA 往往假设稳定明亮的室内环境，而真实操作中 illumination shifts 会造成 degraded RGB observations；Event-VLA 将 degraded visibility 定义为 RGB-centric policies 的鲁棒性问题，并通过 action-query routing 将 event streams 融入 action representation，仿真和真实部署... | jiaxin-liu | 2606.29384 |
| EA-SENSOR-2026-0009 | EA-SENSOR | `support` | `direct` | 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。 | 作者指出 VLA 在 contact-rich tasks 中会被小接触扰动触发不可恢复失败，且这些失败常难以单靠视觉检测；TACO 用 tactile-aware world model 识别 failure-adjacent states、想象局部 correction segments 并标注可执行纠正动作，真实接触任务报告相对 base policy 的成功率提升。 (arXiv HTML Abstract; 1 Introd... | shengbang-liu | 2607.02840 |
| EA-SENSOR-2026-0001 | EA-SENSOR | `support` | `direct` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 | 作者把日常灵巧操作的误差来源明确落在滑移、错位、不稳定抓取和力不匹配上，并指出视觉/语言不能可靠揭示力、滑移和接触稳定性；其分层策略将视觉语言子任务规划、触觉世界模型预测和高频触觉残差修正分开。 (arXiv HTML Abstract; 1 Introduction) | jianyi-zhou | 2607.07287 |
| EA-PNAV-2026-0002 | EA-SENSOR | `conditional` | `direct` | 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。 | 结果段在报告总体领先的同时明确指出最难L4任务性能下降。 (4.1 Experimental Results) | zhenyang-liu | 2601.08325 |
| EA-PNAV-2026-0003 | EA-SENSOR | `conditional` | `direct` | OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 | 限制段直接划定即时单步观测与完整多视图任务之间的边界。 (V-B Limitations and future work.) | boxun-hu | 2603.11072 |
| EA-PNAV-2026-0004 | EA-SENSOR | `conditional` | `direct` | 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 | 结论直接同时报告感知饱和和两类仍关键的误差。 (IV CONCLUSIONS) | ziyi-xia | 2605.14801 |
| EA-SENSOR-2026-0002 | EA-SENSOR | `conditional` | `direct` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 | 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。 (arXiv HTML Abstract; 1 Introduction; 3.2 Force-Aware Kinematic Projection; 4.3 Ablation on RGB-S Design Choices) | shengcheng-luo | 2606.08765 |
| EA-SENSOR-2026-0008 | EA-SENSOR | `conditional` | `direct` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 | 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。 (arXiv HTML Abstract; I Intro... | siyu-wu | 2606.26663 |
| EA-SENSOR-2026-0010 | EA-SENSOR | `conditional` | `direct` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 | 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only po... | jaden-clark | 2606.30988 |
| EA-PNAV-2026-0013 | EA-SENSOR | `limit` | `direct` | 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。 | 引言直接描述视觉相似、静态先验和缺少动作验证导致的持续污染。 (Abstract > first paragraph) | weitao-an | 2606.10348 |
| EA-SENSOR-2026-0005 | EA-SENSOR | `limit` | `direct` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 | 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差... | yanan-zhou | 2606.16690 |
| EA-SENSOR-2026-DQ-0006 | EA-SENSOR | `limit` | `direct` | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | 论文指出 VLA 在接触丰富任务中会因轻微接触扰动产生不可恢复失败，这些失败难以从视觉单独检测；TACO 用 tactile-aware world model 将真实 rollout 中的失败邻近状态转成想象的视触觉纠正片段和可执行纠正动作，在真实接触任务中相对 base policy 提升 44 个百分点成功率。 (Abstract; 1 Introduction; 2 Related Work; 3 Method; 5 Conc... | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-2026-DQ-0002 | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | unlisted | `support` | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 |
| EA-DATA-2026-4DDATA-0002 | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | unlisted | `conditional` | 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 |
| EA-DATA-2026-4DDATA-0018 | amirhosein-alian; yongqiang-zhao; shiyi-gu | unlisted | `conditional` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 |
| EA-DATA-2026-4DDATA-0014 | yujie-zang; yuhang-zheng; xian-nie | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-EVAL-2026-0007 | bowen-jing | unlisted | `limit` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 |
| EA-SENSOR-2026-0004 | ralf-romer | unlisted | `support` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 |
| EA-SENSOR-2026-0003 | yousung-lee | unlisted | `support` | VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 |
| EA-SENSOR-2026-0006 | pengfei-ye | unlisted | `support` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 |
| EA-SENSOR-2026-0011 | jiaxin-liu | unlisted | `support` | RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 |
| EA-SENSOR-2026-0009 | shengbang-liu | unlisted | `support` | 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。 |
| EA-SENSOR-2026-0001 | jianyi-zhou | unlisted | `support` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 |
| EA-PNAV-2026-0002 | zhenyang-liu | unlisted | `conditional` | 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。 |
| EA-PNAV-2026-0003 | boxun-hu | unlisted | `conditional` | OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 |
| EA-PNAV-2026-0004 | ziyi-xia | unlisted | `conditional` | 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 |
| EA-SENSOR-2026-0002 | shengcheng-luo | unlisted | `conditional` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 |
| EA-SENSOR-2026-0008 | siyu-wu | unlisted | `conditional` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 |
| EA-SENSOR-2026-0010 | jaden-clark | unlisted | `conditional` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 |
| EA-PNAV-2026-0013 | weitao-an | unlisted | `limit` | 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。 |
| EA-SENSOR-2026-0005 | yanan-zhou | unlisted | `limit` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 |
| EA-SENSOR-2026-DQ-0006 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-2026-DQ-0002`: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。
- `EA-SENSOR-2026-0004`: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
- `EA-SENSOR-2026-0003`: VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。
- `EA-SENSOR-2026-0006`: 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。
- `EA-SENSOR-2026-0011`: RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。
- `EA-SENSOR-2026-0009`: 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。
- `EA-SENSOR-2026-0001`: 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。
### 条件成立
- `EA-DATA-2026-4DDATA-0002`: 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。
- `EA-DATA-2026-4DDATA-0018`: 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- `EA-DATA-2026-4DDATA-0014`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- `EA-PNAV-2026-0002`: 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。
- `EA-PNAV-2026-0003`: OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。
- `EA-PNAV-2026-0004`: 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。
- `EA-SENSOR-2026-0002`: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- `EA-SENSOR-2026-0008`: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
### 限制与失败模式
- `EA-EVAL-2026-0007`: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- `EA-PNAV-2026-0013`: 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。
- `EA-SENSOR-2026-0005`: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- `EA-SENSOR-2026-DQ-0006`: 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 19 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DATA-2026-DQ-0002` 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。
  - `EA-DATA-2026-4DDATA-0002` 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。
  - `EA-DATA-2026-4DDATA-0018` 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- Scientific memo preview: 《近一年具身感知问题是否已有效解决》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年具身感知问题是否已有效解决 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年具身感知问题是否已有效解决: 先看证据边界，再谈一个可传播的反常识洞察。

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
