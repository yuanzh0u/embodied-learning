# Review Packet: Sparse language, dense vision, and continuous action alignment in VLA systems

## Scope

- Topic: Sparse language, dense vision, and continuous action alignment in VLA systems
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-ALIGN`, `EA-MODEL`, `EA-SENSOR`, `EA-XEMBODIMENT`
- Evidence events: 24
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> full-text evidence -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval, HTML/PDF/OCR recovery, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 24
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-2026-LY-0002`, `EA-DATA-2026-DQ-0002`, `EA-DATA-2026-4DDATA-0010`, `EA-DATA-2026-4DDATA-0018`, `EA-DATA-2026-4DDATA-0014`, `EA-EVAL-2026-DQ-0004`, `EA-PVC-2026-0001`, `EA-PVC-2026-0006`, `EA-PVC-2026-0003`, `EA-PVC-2026-0004`, `EA-ALIGN-2026-0008`, `EA-ALIGN-2026-0001`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 24 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-ALIGN` VLA 多模态与动作对齐: VLA 对齐的核心不是把语言、视觉和动作都变成 token，而是处理三种信号的粒度与物理语义错配：语言通常任务级且稀疏，视觉高维稠密并容易形成捷径，动作连续、闭环且受本体和控制器约束。可靠系统需要显式连接语言到任务阶段、视觉几何到可执行动作、共享状态变化到机器人特定控制器。动作表示应以物理状态变化和可执行性为中心，而不是以模型输出方便为中心。
  - 稠密 visual-action 监督可能压过稀疏 language-action 信号，使语言退化为装饰性条件。
  - 阶段级语言、dense reasoning 或独立 language-action pretraining 可以增强语言对动作的约束，但会引入新的标注和误差传播问题。
  - 视觉不是越稠密越好；应通过 task-space action、结构化场景接口、affordance 或轨迹监督组织成动作相关表示。
  - 离散 action token 便于接入自回归模型，但解码到连续控制时必须条件化机器人状态、本体、接触和控制器。
  - VLA 可以继承视觉与语言先验，却不会自动继承连续运动先验；action prior 或 flow/diffusion action expert 可独立预训练。
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
- `EA-XEMBODIMENT` 跨本体与数据迁移: 跨本体迁移的核心不是复制姿态或控制命令，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。不同机器人即使记录相同 action command，也可能产生不同运动；更稳健的路线是共享 Cartesian state delta、对象状态变化或接触目标，再由机器人特定 adapter 和真实闭环校准落地。
  - 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
  - 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
  - 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
  - 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
  - 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 12 |
| `conditional` | 条件成立 | 6 |
| `limit` | 限制/负面 | 6 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2601.09708: Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning | 2026-01-14 | support | EA-PVC-2026-0001 |
| 2602.09722: Rethinking Visual-Language-Action Model Scaling: Alignment, Mixture, and Regularization | 2026-02-10 | limit | EA-ALIGN-2026-0007 |
| 2602.21161: ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking | 2026-02-24 | conditional | EA-PVC-2026-0005 |
| 2605.00080: World Model for Robot Learning: A Comprehensive Survey | 2026-04-30 | support | EA-PVC-2026-0006 |
| 2605.26349: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Co... | 2026-05-25 | support | EA-DATA-2026-LY-0002 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional | EA-DATA-2026-4DDATA-0010 |
| 2606.03784: Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation | 2026-06-02 | conditional | EA-PVC-2026-0002 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional | EA-DATA-2026-4DDATA-0018 |
| 2606.09630: ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies | 2026-06-08 | support | EA-PVC-2026-0003 |
| 2606.09740: ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models | 2026-06-08 | support | EA-PVC-2026-0004 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional | EA-DATA-2026-4DDATA-0014 |
| 2606.12759: Sparse2Act: Learning Action-Aligned Sparse 3D Representations for Cross-Domain Robot Manipulation | 2026-06-10 | support | EA-ALIGN-2026-0005 |
| 2606.15516: Transferring Contact, Not Just Motion: Compliant Grasping Across Dexterous Hands | 2026-06-17 | limit | EA-ALIGN-2026-0009 |
| 2606.24049: SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies | 2026-06-23 | limit | EA-ALIGN-2026-0010 |
| 2606.26095: Learning Action Priors for Cross-embodiment Robot Manipulation | 2026-06-24 | support | EA-ALIGN-2026-0003 |
| 2606.26800: SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation | 2026-06-25 | conditional | EA-ALIGN-2026-0006 |
| 2606.27295: LA4VLA: Learning to Act without Seeing via Language-Action Pretraining | 2026-06-25 | support | EA-ALIGN-2026-0008 |
| 2606.30113: SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance | 2026-06-29 | limit | EA-ALIGN-2026-0004 |
| 2606.30456: Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform | 2026-06-29 | limit | EA-ALIGN-2026-0002 |
| 2606.30552: Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision | 2026-06-29 | support | EA-ALIGN-2026-0001 |
| 2607.00673: Path Planning in Physically Viable World Models | 2026-07-01 | support | EA-PVC-2026-0007 |
| 2607.02642: GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | support | EA-EVAL-2026-DQ-0004 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-SENSOR-2026-DQ-0006 |
| 2607.06564: Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | support | EA-DATA-2026-DQ-0002 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-2026-LY-0002 | EA-DATA | `support` | `direct` | 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 | DQAF 框架从 sub-task progress、motion smoothness、stalls、kinematic limits 抽取质量信号，生成结构化质量评估和自然语言纠正建议；pilot study 中即时反馈条件呈现更高任务完成度、更高 episode-level quality scores 和更少 detected suboptimalities 的趋势。 (I INTRODUCTION; Abstract; V-... | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | 2605.26349 |
| EA-DATA-2026-DQ-0002 | EA-DATA | `support` | `direct` | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | 论文将 2D VLA 的困难归因于几何理解和空间推理不足、3D 数据和强 3D encoder 稀缺、跨模态 lifting/projection 损失几何 fidelity；其 GC-MAE 用伪点云监督当前点云重建和未来几何演化，并在仿真与真实任务中提升成功率。 (Abstract; I Introduction; IV-C Geometry-Centric Masked Autoencoding; V-B Multi-Task... | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | 2607.06564 |
| EA-DATA-2026-4DDATA-0010 | EA-DATA | `conditional` | `direct` | 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 | 论文把真实robot data、UMI-style data和egocentric videos划分为不同监督等级，并用modality-specific supervision masks让每条样本只参与其实际拥有的视觉、状态、动作和进度损失。 (I Introduction; III Data Sources for Predictive Robot Learning; Unified supervision; IV-C Join... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-DATA-2026-4DDATA-0018 | EA-DATA | `conditional` | `direct` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 | HapTile说明所有模态通过机器人控制循环同步，检查空/损坏轨迹和timestamp gaps，验证action-state consistency；附录还要求episode-level split避免temporal leakage，并保留raw/rectified tactile images。 (3.2 Synchronization and Data Quality Control; A.1 Data Formatting;... | amirhosein-alian; yongqiang-zhao; shiyi-gu | 2606.04825 |
| EA-DATA-2026-4DDATA-0014 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation; IV-C Main Results; Table I) | yujie-zang; yuhang-zheng; xian-nie | 2606.11184 |
| EA-EVAL-2026-DQ-0004 | EA-EVAL | `support` | `direct` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-trai... | gigaworld-team; angyuan-ma; boyuan-wang; et al. | 2607.02642 |
| EA-PVC-2026-0001 | EA-MODEL | `support` | `direct` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 | 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。 (Abstract; 1 Introduction; 5 Co... | chi-pin-huang; yunze-man; zhiding-yu; et al. | 2601.09708 |
| EA-PVC-2026-0006 | EA-MODEL | `support` | `direct` | 纯反应式 VLA 的长程推理、时序 credit assignment 与误差复合问题源于缺少显式预测结构;世界模型既可作决策期评估器(认知层验证),其像素级 rollout 的长程误差积累又是自身的感知型缺陷,需符号结构缓解。 | 综述指出 reactive VLA 在复杂物理环境中受限于 long-horizon reasoning、temporal credit assignment 与 compounding errors,归因于缺少对世界演化的显式预测结构;世界模型作为 evaluator 可对候选动作做 rollout 排序/拒绝/安全过滤(GPC、IRASim、World-in-World);8.5 节指出 pixel-based rollout 的... | bohan-hou; gen-li; jindou-jia; et al. | 2605.00080 |
| EA-PVC-2026-0003 | EA-MODEL | `support` | `direct` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 | ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classifi... | haodi-hu; chung-ta-huang; jing-liu; et al. | 2606.09630 |
| EA-PVC-2026-0004 | EA-MODEL | `support` | `direct` | 感知正确不等于执行正确:VLA 的视觉骨干在扰动场景下仍保持准确空间表征,失败瓶颈在动作头塌缩到记忆轨迹——即 latent perception 与 motor execution 解耦,这是可与感知误差区分的下游错误。 | 论文用 probing 实验证明扰动下 VLA 视觉骨干维持目标物体的准确空间表征,失败仅在 action head:过拟合映射使网络塌缩回训练分布的名义轨迹(memory trap);ProbeAct 从内部 hidden states 提取 3D 目标位置、用运动学状态机检测失败、以 CBF 做最小动作修正,全程无需外部 3D 传感。 (1 Introduction; 2 Related Work; 3 Method) | fan-zhang; seongbin-park; baharan-mirzasoleiman; et al. | 2606.09740 |
| EA-ALIGN-2026-0008 | EA-MODEL | `support` | `direct` | In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and underdeveloped language... | LA4VLA removes visual observations during pretraining and pairs atomic action segments with low-level language descriptions to strengthen language-conditioned action priors before or alongside VLA training. (Abstract; S... | tao-lin | 2606.27295 |
| EA-ALIGN-2026-0001 | EA-MODEL | `support` | `direct` | Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. | The paper frames low-level state/action heterogeneity as a core cross-embodiment challenge, then uses dense embodied chain-of-thought supervision in the VLM stream and a flow-matching action expert that outputs continuo... | haoyang-li | 2606.30552 |
| EA-PVC-2026-0007 | EA-MODEL | `support` | `direct` | 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。 | 论文指出多数路径规划假设地图不变,只问 which path is best 而不问 mission 是否在指定物理变化下仍可行;PVWM 用 Gaussian splat 重建加 MPM 物理仿真生成 query-conditioned 修改场景,真实野外场地的洪水多严重度实验显示:仅在原始重建上规划看不到的长程路线失败与改线行为被暴露出来。 (Abstract; 1 Introduction; 2 Related Work) | su-ann-low; cheng-hsi-hsiao; xingjian-li; et al. | 2607.00673 |
| EA-PVC-2026-0005 | EA-MODEL | `conditional` | `direct` | 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 | 论文主张解耦视觉组件:由成熟视觉管线提供准确 3D 状态,LLM 只做 physical reasoning 并直接在 SE(3) 输出分阶段动作;single-agent 消融显示缺少阶段间验证时早期错误传播,前四块砖放置误差显著增大并频繁碰塌墙体,支持多阶段推理与角色分工的必要性。 (I Introduction; II-B LLM/VLM Based Robotic Operation; IV-D 2 Single-Agent... | guangming-wang; qizhen-ying; yixiong-jing; et al. | 2602.21161 |
| EA-PVC-2026-0002 | EA-MODEL | `conditional` | `direct` | 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 | 论文明确写到 enhanced perception and broader semantic coverage do not inherently guarantee better action generation;系统研究显示推理信号必须落到 end-effector motion、image-space trajectory 等动作相关表示;reasoning-as-prefix 慢且脆,长推理链在推理期误差复合;附录指出语言... | nan-sun; yuan-zhang; yongkun-yang; et al. | 2606.03784 |
| EA-ALIGN-2026-0007 | EA-MODEL | `limit` | `direct` | Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixin... | The paper reports that unified end-effector-relative action representation is critical for cross-embodiment transfer, while indiscriminate pooling of heterogeneous robot datasets can degrade performance. (Abstract; Sect... | ye-wang | 2602.09722 |
| EA-ALIGN-2026-0002 | EA-MODEL | `limit` | `direct` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset c... | The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone. (Abstract; Section 1.1 Proje... | mathilde-hochedel | 2606.30456 |
| EA-ALIGN-2026-0004 | EA-MODEL | `limit` | `direct` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same to... | SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines. (Abstract; Section 1 Introduction;... | tengyue-jiang | 2606.30113 |
| EA-ALIGN-2026-0005 | EA-SENSOR | `support` | `direct` | Dense or sparse visual geometry becomes more useful for manipulation when it is explicitly aligned to task-space actions rather than learned only through downstream policy losses. | Sparse2Act uses task-space end-effector actions as geometric supervision for masked sparse 3D tokens, arguing that point-cloud observations and motions share a metric workspace. (Abstract; Figure 1 caption; Section 1 In... | yu-guo | 2606.12759 |
| EA-ALIGN-2026-0006 | EA-SENSOR | `conditional` | `direct` | A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. | SSI-Policy builds an RGB-only structured scene interface encoding monocular depth features, language-grounded layouts, and instruction-conditioned 2D motion trajectories; it reports few-shot gains but notes failures fro... | kaijun-wang | 2606.26800 |
| EA-ALIGN-2026-0009 | EA-SENSOR | `limit` | `direct` | For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self... | The paper introduces a force-position interface that maps hand-specific effort signals into calibrated torques, fingertip forces, and load descriptors, and trains a mask-aware flow-matching policy to rely on force/propr... | soofiyan-atar | 2606.15516 |
| EA-SENSOR-2026-DQ-0006 | EA-SENSOR | `limit` | `direct` | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | 论文指出 VLA 在接触丰富任务中会因轻微接触扰动产生不可恢复失败，这些失败难以从视觉单独检测；TACO 用 tactile-aware world model 将真实 rollout 中的失败邻近状态转成想象的视触觉纠正片段和可执行纠正动作，在真实接触任务中相对 base policy 提升 44 个百分点成功率。 (Abstract; 1 Introduction; 2 Related Work; 3 Method; 5 Conc... | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |
| EA-ALIGN-2026-0003 | EA-XEMBODIMENT | `support` | `direct` | A VLA that inherits visual and linguistic priors from a VLM still lacks an explicit physical motion prior; pretraining the action module on unconditioned trajectories can reduce t... | The method first trains a flow-matching encoder-decoder action module on action trajectories without visual/language tokens, then transfers this prior into VLA training through decoder reuse and latent distillation. (Ab... | dong-jing | 2606.26095 |
| EA-ALIGN-2026-0010 | EA-XEMBODIMENT | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-2026-LY-0002 | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | unlisted | `support` | 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 |
| EA-DATA-2026-DQ-0002 | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | unlisted | `support` | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 |
| EA-DATA-2026-4DDATA-0010 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 |
| EA-DATA-2026-4DDATA-0018 | amirhosein-alian; yongqiang-zhao; shiyi-gu | unlisted | `conditional` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 |
| EA-DATA-2026-4DDATA-0014 | yujie-zang; yuhang-zheng; xian-nie | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-EVAL-2026-DQ-0004 | gigaworld-team; angyuan-ma; boyuan-wang; et al. | unlisted | `support` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 |
| EA-PVC-2026-0001 | chi-pin-huang; yunze-man; zhiding-yu; et al. | unlisted | `support` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 |
| EA-PVC-2026-0006 | bohan-hou; gen-li; jindou-jia; et al. | unlisted | `support` | 纯反应式 VLA 的长程推理、时序 credit assignment 与误差复合问题源于缺少显式预测结构;世界模型既可作决策期评估器(认知层验证),其像素级 rollout 的长程误差积累又是自身的感知型缺陷,需符号结构缓解。 |
| EA-PVC-2026-0003 | haodi-hu; chung-ta-huang; jing-liu; et al. | unlisted | `support` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 |
| EA-PVC-2026-0004 | fan-zhang; seongbin-park; baharan-mirzasoleiman; et al. | unlisted | `support` | 感知正确不等于执行正确:VLA 的视觉骨干在扰动场景下仍保持准确空间表征,失败瓶颈在动作头塌缩到记忆轨迹——即 latent perception 与 motor execution 解耦,这是可与感知误差区分的下游错误。 |
| EA-ALIGN-2026-0008 | tao-lin | unlisted | `support` | In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and und... |
| EA-ALIGN-2026-0001 | haoyang-li | unlisted | `support` | Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action s... |
| EA-PVC-2026-0007 | su-ann-low; cheng-hsi-hsiao; xingjian-li; et al. | unlisted | `support` | 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。 |
| EA-PVC-2026-0005 | guangming-wang; qizhen-ying; yixiong-jing; et al. | unlisted | `conditional` | 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 |
| EA-PVC-2026-0002 | nan-sun; yuan-zhang; yongkun-yang; et al. | unlisted | `conditional` | 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 |
| EA-ALIGN-2026-0007 | ye-wang | unlisted | `limit` | Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action spa... |
| EA-ALIGN-2026-0002 | mathilde-hochedel | unlisted | `limit` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preproce... |
| EA-ALIGN-2026-0004 | tengyue-jiang | unlisted | `limit` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottlen... |
| EA-ALIGN-2026-0005 | yu-guo | unlisted | `support` | Dense or sparse visual geometry becomes more useful for manipulation when it is explicitly aligned to task-space actions rather than learned only through downs... |
| EA-ALIGN-2026-0006 | kaijun-wang | unlisted | `conditional` | A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action con... |
| EA-ALIGN-2026-0009 | soofiyan-atar | unlisted | `limit` | For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when vis... |
| EA-SENSOR-2026-DQ-0006 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 |
| EA-ALIGN-2026-0003 | dong-jing | unlisted | `support` | A VLA that inherits visual and linguistic priors from a VLM still lacks an explicit physical motion prior; pretraining the action module on unconditioned traje... |
| EA-ALIGN-2026-0010 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-2026-LY-0002`: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。
- `EA-DATA-2026-DQ-0002`: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。
- `EA-EVAL-2026-DQ-0004`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- `EA-PVC-2026-0001`: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
- `EA-PVC-2026-0006`: 纯反应式 VLA 的长程推理、时序 credit assignment 与误差复合问题源于缺少显式预测结构;世界模型既可作决策期评估器(认知层验证),其像素级 rollout 的长程误差积累又是自身的感知型缺陷,需符号结构缓解。
- `EA-PVC-2026-0003`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- `EA-PVC-2026-0004`: 感知正确不等于执行正确:VLA 的视觉骨干在扰动场景下仍保持准确空间表征,失败瓶颈在动作头塌缩到记忆轨迹——即 latent perception 与 motor execution 解耦,这是可与感知误差区分的下游错误。
- `EA-ALIGN-2026-0008`: In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and underdeveloped language-action grounding.
### 条件成立
- `EA-DATA-2026-4DDATA-0010`: 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。
- `EA-DATA-2026-4DDATA-0018`: 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- `EA-DATA-2026-4DDATA-0014`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- `EA-PVC-2026-0005`: 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。
- `EA-PVC-2026-0002`: 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。
- `EA-ALIGN-2026-0006`: A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control.
### 限制与失败模式
- `EA-ALIGN-2026-0007`: Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixing can cause negative transfer.
- `EA-ALIGN-2026-0002`: Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- `EA-ALIGN-2026-0004`: Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under d...
- `EA-ALIGN-2026-0009`: For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self-occluded.
- `EA-SENSOR-2026-DQ-0006`: 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。
- `EA-ALIGN-2026-0010`: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 24 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DATA-2026-LY-0002` 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。
  - `EA-DATA-2026-DQ-0002` 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。
  - `EA-DATA-2026-4DDATA-0010` 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。
- Scientific memo preview: 《Sparse language, dense vision, and continuous action alignment in VLA systems》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: Sparse language, dense vision, and continuous action alignment in VLA systems 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: Sparse language, dense vision, and continuous action alignment in VLA systems: 先看证据边界，再谈一个可传播的反常识洞察。

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
