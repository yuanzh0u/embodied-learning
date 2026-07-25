# Review Packet: 近半年VLA在具身领域最大的技术突破

## Scope

- Topic: 近半年VLA在具身领域最大的技术突破
- Time range: 2026-01-19..2026-07-19
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-4D`, `EA-ALIGN`
- Evidence events: 31
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 31
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-WMDATA-READ-0007`, `EA-WMDATA-READ-0009`, `EA-WMDATA-READ-0008`, `EA-4D-READ-0013`, `EA-4D-READ-0012`, `EA-4D-READ-0011`, `EA-WMEVAL-READ-0007`, `EA-WMEVAL-READ-0005`, `EA-WMEVAL-READ-0003`, `EA-WMEVAL-READ-0001`, `EA-WMEVAL-READ-0010`, `EA-WMEVAL-READ-0014`
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

- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型后果预演、本体适配器与底层控制器组成的融合栈。近期 loco-manipulation 证据进一步表明，系统分层边界应从上肢/下肢改为任务意图/全身执行，完整动作接口本身会限制模型能力上限。Ego-centric 人类视频可扩展行为与视点先验，但只有经过动作恢复、本体对齐和目标机器人锚定后，才可能转成可执行控制。基础模型、适配模块与检查点还构成需要独立审计的供应链。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测还要审计训练—测试结构独立性，并把干净性能、触发/扰动风险、检测误报与恢复代价分开记录，防止记忆式高分或 episode 平均值掩盖动作窗风险。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- `EA-4D` 4D 时空推理与世界动态: 具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。
  - 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
  - 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
  - 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
  - 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
  - 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。
- `EA-ALIGN` VLA 多模态与动作对齐: VLA 对齐的核心不是把语言、视觉和动作都变成 token，而是处理三种信号的粒度与物理语义错配：语言通常任务级且稀疏，视觉高维稠密并容易形成捷径，动作连续、闭环且受本体和控制器约束。可靠系统需要显式连接语言到任务阶段、视觉几何到可执行动作、共享状态变化到机器人特定控制器。动作表示应以物理状态变化和可执行性为中心，而不是以模型输出方便为中心。
  - 稠密 visual-action 监督可能压过稀疏 language-action 信号，使语言退化为装饰性条件。
  - 阶段级语言、dense reasoning 或独立 language-action pretraining 可以增强语言对动作的约束，但会引入新的标注和误差传播问题。
  - 视觉不是越稠密越好；应通过 task-space action、结构化场景接口、affordance 或轨迹监督组织成动作相关表示。
  - 离散 action token 便于接入自回归模型，但解码到连续控制时必须条件化机器人状态、本体、接触和控制器。
  - VLA 可以继承视觉与语言先验，却不会自动继承连续运动先验；action prior 或 flow/diffusion action expert 可独立预训练。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 12 |
| `conditional` | 条件成立 | 7 |
| `limit` | 限制/负面 | 10 |
| `gap` | 缺口 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.11291: H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model | 2026-02-11T19:08:36Z | conditional, limit, support | EA-VLABREAK-2026-0001; EA-VLABREAK-2026-0002; EA-VLABREAK-2026-0003 |
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | gap | EA-WMEVAL-READ-0006 |
| 2603.08485: 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos | 2026-03-09 | conditional | EA-4D-READ-0012 |
| 2603.08546: Interactive World Simulator for Robot Policy Training and Evaluation | 2026-03-09 | support | EA-WMDATA-READ-0007 |
| 2603.12553: Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation | 2026-03-13T01:33:48Z | conditional, support | EA-VLABREAK-2026-0004; EA-VLABREAK-2026-0005 |
| 2603.16669: Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation | 2026-03-17 | support | EA-WMEVAL-READ-0007 |
| 2604.11386: ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation | 2026-04-13 | conditional | EA-WMEVAL-READ-0014 |
| 2604.21741: Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training | 2026-04-23 | support | EA-WMDATA-READ-0009 |
| 2605.00121: Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes | 2026-04-30 | limit | EA-WMEVAL-READ-0008 |
| 2605.20752: GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation | 2026-05-20 | support | EA-WMDATA-READ-0008 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | support | EA-WMEVAL-READ-0005 |
| 2605.27947: SANTS: A State-Adaptive Scheduler for World Action Models | 2026-05-27 | limit | EA-WMEVAL-READ-0015 |
| 2605.29360: MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models | 2026-05-28 | gap | EA-WMEVAL-READ-0004 |
| 2606.00664: SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models | 2026-05-30 | support | EA-WMEVAL-READ-0003 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | support | EA-WMEVAL-READ-0001 |
| 2606.02577: RoboDream: Compositional World Models for Scalable Robot Data Synthesis | 2026-06-01 | conditional | EA-WMEVAL-READ-0011 |
| 2606.03784: Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation | 2026-06-02 | conditional | EA-ALIGN-READ-0006 |
| 2606.08737: Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation | 2026-06-07 | support | EA-4D-READ-0013 |
| 2606.09630: ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies | 2026-06-08 | support | EA-ALIGN-READ-0015 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional | EA-4D-READ-0011 |
| 2606.12403: World Pilot: Steering Vision-Language-Action Models with World-Action Priors | 2026-06-10 | limit | EA-WMEVAL-READ-0013 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | support | EA-WMEVAL-READ-0010 |
| 2606.24049: SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies | 2026-06-23 | limit | EA-ALIGN-READ-0001 |
| 2606.30113: SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance | 2026-06-29 | limit | EA-ALIGN-READ-0003 |
| 2606.30456: Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform | 2026-06-29 | limit | EA-ALIGN-READ-0004 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-ALIGN-READ-0009 |
| 2607.15207: BadWAM: When World-Action Models Dream Right but Act Wrong | 2026-07-16T17:04:15Z | limit | EA-VLABREAK-2026-0006; EA-VLABREAK-2026-0007 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-WMDATA-READ-0007 | EA-DATA | `support` | `direct` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-c... | The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real perform... | yixuan-wang; rhythm-syed; fangyu-wu; et al. | 2603.08546 |
| EA-WMDATA-READ-0009 | EA-DATA | `support` | `direct` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. | Hi-WM rolls policies inside a world model, lets humans intervene when rollouts become incorrect or failure-prone, caches and branches failure states, and adds corrective trajectories back into the training set for post-... | yaxuan-li; zhongyi-zhou; yefei-chen; et al. | 2604.21741 |
| EA-WMDATA-READ-0008 | EA-DATA | `support` | `direct` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and... | GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference. (3.... | zijian-zhang; yuqing-jiang; qian-cheng; et al. | 2605.20752 |
| EA-4D-READ-0013 | EA-DATA | `support` | `direct` | Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 | 问题建模段先定义动作与视觉未来的联合分布，再明确把未来触觉纳入联合预测目标。 (3.1. Problem Formulation) | yunfan-lou; yifan-ye; yankai-fu; et al. | 2606.08737 |
| EA-4D-READ-0012 | EA-DATA | `conditional` | `direct` | 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 | 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。 (4.3 Results: 3D Point Track Prediction) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | 2603.08485 |
| EA-4D-READ-0011 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-WMEVAL-READ-0007 | EA-EVAL | `support` | `direct` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... | The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap... | mutian-xu; tianbao-zhang; tianqi-liu; et al. | 2603.16669 |
| EA-WMEVAL-READ-0005 | EA-EVAL | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | 2605.22882 |
| EA-WMEVAL-READ-0003 | EA-EVAL | `support` | `direct` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remov... | SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as pol... | ziheng-he; yixiang-chen; ning-yang; et al. | 2606.00664 |
| EA-WMEVAL-READ-0001 | EA-EVAL | `support` | `direct` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 | 摘要直接报告了异构数据组成与 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-WMEVAL-READ-0010 | EA-EVAL | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | 2606.13672 |
| EA-WMEVAL-READ-0014 | EA-EVAL | `conditional` | `direct` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve re... | ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate... | yiran-qin; jiahua-ma; li-kang; et al. | 2604.11386 |
| EA-WMEVAL-READ-0011 | EA-EVAL | `conditional` | `direct` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel object... | RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost... | junjie-ye; rong-xue; basile-van-hoorick; et al. | 2606.02577 |
| EA-WMEVAL-READ-0008 | EA-EVAL | `limit` | `direct` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. | The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and plannin... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-WMEVAL-READ-0015 | EA-EVAL | `limit` | `direct` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less acti... | SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video... | sants-authors | 2605.27947 |
| EA-WMEVAL-READ-0013 | EA-EVAL | `limit` | `direct` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. | World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy. (Abstract... | zefu-lin; rongxu-cui; junjia-xu; et al. | 2606.12403 |
| EA-WMEVAL-READ-0006 | EA-EVAL | `gap` | `direct` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. | The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could furth... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-WMEVAL-READ-0004 | EA-EVAL | `gap` | `direct` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias... | The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias. (Abstract... | tianzhuo-yang; zihan-shen; zirui-mi; et al. | 2605.29360 |
| EA-VLABREAK-2026-0001 | EA-MODEL | `support` | `direct` | H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 | 方法定义了逻辑世界模型、视觉世界模型、低层 VLA 和子任务完成检测的两时间尺度接口。 (IV-C Hierarchical World Model Guidance for VLA) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-VLABREAK-2026-0004 | EA-MODEL | `support` | `direct` | StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。 | 方法段给出动力学里程碑抽取和 planner-to-action 两阶段优化的完整链路。 (pages 5-8, Sections 3.1-3.3) | minghao-jin; mozheng-liao; mingfei-han; et al. | 2603.12553 |
| EA-ALIGN-READ-0015 | EA-MODEL | `support` | `direct` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 | ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classifi... | haodi-hu; chung-ta-huang; jing-liu; et al. | 2606.09630 |
| EA-VLABREAK-2026-0002 | EA-MODEL | `conditional` | `direct` | 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 | H-WM 为 64.8%，logic-only 为 48.4%，H-WM-Stable-Diffusion 为 54.4%。 (VI Results) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-VLABREAK-2026-0005 | EA-MODEL | `conditional` | `direct` | 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 | LIBERO 平均为 94.8%；实机 tidy-up 为 8/10，相同表面的 UniVLA 为 4/10。 (page 11) | minghao-jin; mozheng-liao; mingfei-han; et al. | 2603.12553 |
| EA-ALIGN-READ-0006 | EA-MODEL | `conditional` | `direct` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 | 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。 (Abstract (full-text section)) | nan-sun; yuan-zhang; yongkun-yang; et al. | 2606.03784 |
| EA-VLABREAK-2026-0003 | EA-MODEL | `limit` | `direct` | H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 | 结论明确列出额外组件/训练阶段的代价，以及对符号化状态的依赖。 (VII Conclusion) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-ALIGN-READ-0001 | EA-MODEL | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-ALIGN-READ-0003 | EA-MODEL | `limit` | `direct` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same to... | SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines. (Abstract (full-text section)) | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | 2606.30113 |
| EA-ALIGN-READ-0004 | EA-MODEL | `limit` | `direct` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset c... | The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone. (Abstract (full-text section... | mathilde-hochedel; marc-lalonde | 2606.30456 |
| EA-ALIGN-READ-0009 | EA-MODEL | `limit` | `direct` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 | 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。 (5 Conclusion and Limitations) | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |
| EA-VLABREAK-2026-0006 | EA-MODEL | `limit` | `direct` | 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 | 主实验在 40 个 LIBERO 任务、每任务 20 次试验上使用闭环攻击，并报告任务族级下降。 (5.2 BadWAM Reliably Induces Task Failures) | qi-li; xingyi-yang; xinchao-wang | 2607.15207 |
| EA-VLABREAK-2026-0007 | EA-MODEL | `limit` | `direct` | 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 | 想象保持攻击在 40 个任务中有 39 个降低未来漂移，同时保留显著攻击强度。 (5.8 What Do These Results Imply for WAM Safety?) | qi-li; xingyi-yang; xinchao-wang | 2607.15207 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-WMDATA-READ-0007 | yixuan-wang; rhythm-syed; fangyu-wu; et al. | unlisted | `support` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depe... |
| EA-WMDATA-READ-0009 | yaxuan-li; zhongyi-zhou; yefei-chen; et al. | unlisted | `support` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. |
| EA-WMDATA-READ-0008 | zijian-zhang; yuqing-jiang; qian-cheng; et al. | unlisted | `support` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent curr... |
| EA-4D-READ-0013 | yunfan-lou; yifan-ye; yankai-fu; et al. | unlisted | `support` | Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 |
| EA-4D-READ-0012 | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | unlisted | `conditional` | 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 |
| EA-4D-READ-0011 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-WMEVAL-READ-0007 | mutian-xu; tianbao-zhang; tianqi-liu; et al. | unlisted | `support` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while... |
| EA-WMEVAL-READ-0005 | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-WMEVAL-READ-0003 | ziheng-he; yixiang-chen; ning-yang; et al. | unlisted | `support` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic fram... |
| EA-WMEVAL-READ-0001 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `support` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 |
| EA-WMEVAL-READ-0010 | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-WMEVAL-READ-0014 | yiran-qin; jiahua-ma; li-kang; et al. | unlisted | `conditional` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pa... |
| EA-WMEVAL-READ-0011 | junjie-ye; rong-xue; basile-van-hoorick; et al. | unlisted | `conditional` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrat... |
| EA-WMEVAL-READ-0008 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `limit` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verifica... |
| EA-WMEVAL-READ-0015 | sants-authors | unlisted | `limit` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising... |
| EA-WMEVAL-READ-0013 | zefu-lin; rongxu-cui; junjia-xu; et al. | unlisted | `limit` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution... |
| EA-WMEVAL-READ-0006 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `gap` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. |
| EA-WMEVAL-READ-0004 | tianzhuo-yang; zihan-shen; zirui-mi; et al. | unlisted | `gap` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelit... |
| EA-VLABREAK-2026-0001 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `support` | H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 |
| EA-VLABREAK-2026-0004 | minghao-jin; mozheng-liao; mingfei-han; et al. | unlisted | `support` | StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。 |
| EA-ALIGN-READ-0015 | haodi-hu; chung-ta-huang; jing-liu; et al. | unlisted | `support` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 |
| EA-VLABREAK-2026-0002 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `conditional` | 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 |
| EA-VLABREAK-2026-0005 | minghao-jin; mozheng-liao; mingfei-han; et al. | unlisted | `conditional` | 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 |
| EA-ALIGN-READ-0006 | nan-sun; yuan-zhang; yongkun-yang; et al. | unlisted | `conditional` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 |
| EA-VLABREAK-2026-0003 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `limit` | H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 |
| EA-ALIGN-READ-0001 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-ALIGN-READ-0003 | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | unlisted | `limit` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottlen... |
| EA-ALIGN-READ-0004 | mathilde-hochedel; marc-lalonde | unlisted | `limit` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preproce... |
| EA-ALIGN-READ-0009 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 |
| EA-VLABREAK-2026-0006 | qi-li; xingyi-yang; xinchao-wang | unlisted | `limit` | 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 |
| EA-VLABREAK-2026-0007 | qi-li; xingyi-yang; xinchao-wang | unlisted | `limit` | 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 |

## Synthesis Slots

### 共识/正向证据
- `EA-WMDATA-READ-0007`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-...
- `EA-WMDATA-READ-0009`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations.
- `EA-WMDATA-READ-0008`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon future evolution rather t...
- `EA-4D-READ-0013`: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。
- `EA-WMEVAL-READ-0007`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- `EA-WMEVAL-READ-0005`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- `EA-WMEVAL-READ-0003`: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information downstream policies ne...
- `EA-WMEVAL-READ-0001`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
### 条件成立
- `EA-4D-READ-0012`: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- `EA-4D-READ-0011`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- `EA-WMEVAL-READ-0014`: A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenari...
- `EA-WMEVAL-READ-0011`: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing...
- `EA-VLABREAK-2026-0002`: 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。
- `EA-VLABREAK-2026-0005`: 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。
- `EA-ALIGN-READ-0006`: ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。
### 限制与失败模式
- `EA-WMEVAL-READ-0008`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- `EA-WMEVAL-READ-0015`: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- `EA-WMEVAL-READ-0013`: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- `EA-VLABREAK-2026-0003`: H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。
- `EA-ALIGN-READ-0001`: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- `EA-ALIGN-READ-0003`: Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under d...
- `EA-ALIGN-READ-0004`: Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- `EA-ALIGN-READ-0009`: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
### 开放问题
- `EA-WMEVAL-READ-0006`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- `EA-WMEVAL-READ-0004`: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 27 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-WMDATA-READ-0007` A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its...
  - `EA-WMDATA-READ-0009` World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrati...
  - `EA-WMDATA-READ-0008` Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to repr...
- Scientific memo preview: 《近半年VLA在具身领域最大的技术突破》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近半年VLA在具身领域最大的技术突破 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近半年VLA在具身领域最大的技术突破: 先看证据边界，再谈一个可传播的反常识洞察。

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
