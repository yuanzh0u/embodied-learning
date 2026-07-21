# Review Packet: 近一年世界视频模型最可靠的应用任务

## Scope

- Topic: 近一年世界视频模型最可靠的应用任务
- Time range: 2025-07-19..2026-07-19
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-4D`
- Evidence events: 31
- Topic cards: 3
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
- Trace IDs: `EA-WMDATA-READ-0007`, `EA-WMDATA-READ-0009`, `EA-WMDATA-READ-0008`, `EA-4D-READ-0013`, `ERR-PVC-READ-0013`, `ERR-PVC-READ-0014`, `EA-4D-READ-0012`, `EA-4D-READ-0011`, `EA-EGO-2026-0003`, `EA-CONTAM-2026-0007`, `EA-WMEVAL-READ-0007`, `EA-WMEVAL-READ-0005`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 30 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 30
- Structure mapped: 30
- Deep-read papers: 30
- Claim-verified papers: 30
- Accepted evidence papers: 30
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型后果预演、本体适配器与底层控制器组成的融合栈。Ego-centric 人类视频可扩展行为与视点先验，但只有经过动作恢复、本体对齐和目标机器人锚定后，才可能转成可执行控制。基础模型、适配模块与检查点还构成需要独立审计的供应链。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
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

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 13 |
| `conditional` | 条件成立 | 6 |
| `limit` | 限制/负面 | 10 |
| `gap` | 缺口 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2509.21986: Developing Vision-Language-Action Model from Egocentric Videos | 2025-09-26T07:09:33Z | limit | EA-EGO-2026-0003 |
| 2510.03827: LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization | 2025-10-04 | limit | EA-CONTAM-2026-0007 |
| 2601.09708: Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning | 2026-01-14 | support | EA-ALIGN-READ-0013 |
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | gap | EA-WMEVAL-READ-0006 |
| 2603.08485: 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos | 2026-03-09 | conditional | EA-4D-READ-0012 |
| 2603.08546: Interactive World Simulator for Robot Policy Training and Evaluation | 2026-03-09 | support | EA-WMDATA-READ-0007 |
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
| 2607.00673: Path Planning in Physically Viable World Models | 2026-07-01 | support | ERR-PVC-READ-0013 |
| 2607.01060: RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation | 2026-07-01T15:22:41Z | conditional, limit | EA-WMTASK-2026-0001; EA-WMTASK-2026-0002 |
| 2607.02642: GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | support | ERR-PVC-READ-0014 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-ALIGN-READ-0009 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-WMDATA-READ-0007 | EA-DATA | `support` | `direct` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-c... | The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real perform... | yixuan-wang; rhythm-syed; fangyu-wu; et al. | 2603.08546 |
| EA-WMDATA-READ-0009 | EA-DATA | `support` | `direct` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. | Hi-WM rolls policies inside a world model, lets humans intervene when rollouts become incorrect or failure-prone, caches and branches failure states, and adds corrective trajectories back into the training set for post-... | yaxuan-li; zhongyi-zhou; yefei-chen; et al. | 2604.21741 |
| EA-WMDATA-READ-0008 | EA-DATA | `support` | `direct` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and... | GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference. (3.... | zijian-zhang; yuqing-jiang; qian-cheng; et al. | 2605.20752 |
| EA-4D-READ-0013 | EA-DATA | `support` | `direct` | Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 | 问题建模段先定义动作与视觉未来的联合分布，再明确把未来触觉纳入联合预测目标。 (3.1. Problem Formulation) | yunfan-lou; yifan-ye; yankai-fu; et al. | 2606.08737 |
| ERR-PVC-READ-0013 | EA-DATA | `support` | `direct` | 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 | 摘要对比了原始重建环境与物理修改场景下的路线可行性，并报告后者能揭示前者不可见的失败。 (Abstract (full-text section)) | su-ann-low; cheng-hsi-hsiao; xingjian-li; et al. | 2607.00673 |
| ERR-PVC-READ-0014 | EA-DATA | `support` | `direct` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-trai... | gigaworld-team; angyuan-ma; boyuan-wang; et al. | 2607.02642 |
| EA-4D-READ-0012 | EA-DATA | `conditional` | `direct` | 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 | 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。 (4.3 Results: 3D Point Track Prediction) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | 2603.08485 |
| EA-4D-READ-0011 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-EGO-2026-0003 | EA-DATA | `limit` | `direct` | 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 | 策略训练段明确说明 gripper state 缺失，并以 object pose displacement 作为替代动作。 (III-C Policy Training) | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | 2509.21986 |
| EA-CONTAM-2026-0007 | EA-DATA | `limit` | `direct` | LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 | LIBERO-PRO 在保持逻辑可执行的前提下改变物体位置与任务，标准设置中的高分模型在这些轻微改变下近乎崩溃。 (5.2 Main Results) | xueyang-zhou; yangming-xu; guiyao-tie; et al. | 2510.03827 |
| EA-WMEVAL-READ-0007 | EA-EVAL | `support` | `direct` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... | The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap... | mutian-xu; tianbao-zhang; tianqi-liu; et al. | 2603.16669 |
| EA-WMEVAL-READ-0005 | EA-EVAL | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | 2605.22882 |
| EA-WMEVAL-READ-0003 | EA-EVAL | `support` | `direct` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remov... | SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as pol... | ziheng-he; yixiang-chen; ning-yang; et al. | 2606.00664 |
| EA-WMEVAL-READ-0001 | EA-EVAL | `support` | `direct` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 | 摘要直接报告了异构数据组成与 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-WMEVAL-READ-0010 | EA-EVAL | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | 2606.13672 |
| EA-WMEVAL-READ-0014 | EA-EVAL | `conditional` | `direct` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve re... | ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate... | yiran-qin; jiahua-ma; li-kang; et al. | 2604.11386 |
| EA-WMEVAL-READ-0011 | EA-EVAL | `conditional` | `direct` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel object... | RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost... | junjie-ye; rong-xue; basile-van-hoorick; et al. | 2606.02577 |
| EA-WMTASK-2026-0001 | EA-EVAL | `conditional` | `direct` | In the DROID/RoboArena setting, a closed-loop video-world-model evaluator produced a policy ranking that closely matched the real-robot leaderboard across the evaluated policies,... | The paper runs the same policies from RoboArena initial observations entirely inside RoboWorld and reports strong positive agreement between the induced ranking and the real leaderboard; the claim is bounded to the eigh... | byeongguk-jeon; seonghyeon-ye; jaehyeok-doo; et al. | 2607.01060 |
| EA-WMEVAL-READ-0008 | EA-EVAL | `limit` | `direct` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. | The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and plannin... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-WMEVAL-READ-0015 | EA-EVAL | `limit` | `direct` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less acti... | SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video... | sants-authors | 2605.27947 |
| EA-WMEVAL-READ-0013 | EA-EVAL | `limit` | `direct` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. | World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy. (Abstract... | zefu-lin; rongxu-cui; junjia-xu; et al. | 2606.12403 |
| EA-WMTASK-2026-0002 | EA-EVAL | `limit` | `direct` | RoboWorld's principal qualitative failures occur after object contact, when manipulated objects may disintegrate, morph unrealistically, or become visually inconsistent, limiting... | The appendix contrasts stable pre-contact scenes with post-contact artifacts and identifies contact-rich object dynamics as a key remaining limitation. (E.3 Failure Case Analysis) | byeongguk-jeon; seonghyeon-ye; jaehyeok-doo; et al. | 2607.01060 |
| EA-WMEVAL-READ-0006 | EA-EVAL | `gap` | `direct` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. | The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could furth... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-WMEVAL-READ-0004 | EA-EVAL | `gap` | `direct` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias... | The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias. (Abstract... | tianzhuo-yang; zihan-shen; zirui-mi; et al. | 2605.29360 |
| EA-ALIGN-READ-0013 | EA-MODEL | `support` | `direct` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 | 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。 (5 Conclusion) | chi-pin-huang; yunze-man; zhiding-yu; et al. | 2601.09708 |
| EA-ALIGN-READ-0015 | EA-MODEL | `support` | `direct` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 | ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classifi... | haodi-hu; chung-ta-huang; jing-liu; et al. | 2606.09630 |
| EA-ALIGN-READ-0006 | EA-MODEL | `conditional` | `direct` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 | 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。 (Abstract (full-text section)) | nan-sun; yuan-zhang; yongkun-yang; et al. | 2606.03784 |
| EA-ALIGN-READ-0001 | EA-MODEL | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-ALIGN-READ-0003 | EA-MODEL | `limit` | `direct` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same to... | SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines. (Abstract (full-text section)) | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | 2606.30113 |
| EA-ALIGN-READ-0004 | EA-MODEL | `limit` | `direct` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset c... | The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone. (Abstract (full-text section... | mathilde-hochedel; marc-lalonde | 2606.30456 |
| EA-ALIGN-READ-0009 | EA-MODEL | `limit` | `direct` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 | 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。 (5 Conclusion and Limitations) | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-WMDATA-READ-0007 | yixuan-wang; rhythm-syed; fangyu-wu; et al. | unlisted | `support` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depe... |
| EA-WMDATA-READ-0009 | yaxuan-li; zhongyi-zhou; yefei-chen; et al. | unlisted | `support` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. |
| EA-WMDATA-READ-0008 | zijian-zhang; yuqing-jiang; qian-cheng; et al. | unlisted | `support` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent curr... |
| EA-4D-READ-0013 | yunfan-lou; yifan-ye; yankai-fu; et al. | unlisted | `support` | Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 |
| ERR-PVC-READ-0013 | su-ann-low; cheng-hsi-hsiao; xingjian-li; et al. | unlisted | `support` | 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 |
| ERR-PVC-READ-0014 | gigaworld-team; angyuan-ma; boyuan-wang; et al. | unlisted | `support` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 |
| EA-4D-READ-0012 | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | unlisted | `conditional` | 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 |
| EA-4D-READ-0011 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-EGO-2026-0003 | tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al. | unlisted | `limit` | 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 |
| EA-CONTAM-2026-0007 | xueyang-zhou; yangming-xu; guiyao-tie; et al. | unlisted | `limit` | LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 |
| EA-WMEVAL-READ-0007 | mutian-xu; tianbao-zhang; tianqi-liu; et al. | unlisted | `support` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while... |
| EA-WMEVAL-READ-0005 | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-WMEVAL-READ-0003 | ziheng-he; yixiang-chen; ning-yang; et al. | unlisted | `support` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic fram... |
| EA-WMEVAL-READ-0001 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `support` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 |
| EA-WMEVAL-READ-0010 | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-WMEVAL-READ-0014 | yiran-qin; jiahua-ma; li-kang; et al. | unlisted | `conditional` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pa... |
| EA-WMEVAL-READ-0011 | junjie-ye; rong-xue; basile-van-hoorick; et al. | unlisted | `conditional` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrat... |
| EA-WMTASK-2026-0001 | byeongguk-jeon; seonghyeon-ye; jaehyeok-doo; et al. | unlisted | `conditional` | In the DROID/RoboArena setting, a closed-loop video-world-model evaluator produced a policy ranking that closely matched the real-robot leaderboard across the... |
| EA-WMEVAL-READ-0008 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `limit` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verifica... |
| EA-WMEVAL-READ-0015 | sants-authors | unlisted | `limit` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising... |
| EA-WMEVAL-READ-0013 | zefu-lin; rongxu-cui; junjia-xu; et al. | unlisted | `limit` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution... |
| EA-WMTASK-2026-0002 | byeongguk-jeon; seonghyeon-ye; jaehyeok-doo; et al. | unlisted | `limit` | RoboWorld's principal qualitative failures occur after object contact, when manipulated objects may disintegrate, morph unrealistically, or become visually inc... |
| EA-WMEVAL-READ-0006 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `gap` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. |
| EA-WMEVAL-READ-0004 | tianzhuo-yang; zihan-shen; zirui-mi; et al. | unlisted | `gap` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelit... |
| EA-ALIGN-READ-0013 | chi-pin-huang; yunze-man; zhiding-yu; et al. | unlisted | `support` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 |
| EA-ALIGN-READ-0015 | haodi-hu; chung-ta-huang; jing-liu; et al. | unlisted | `support` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 |
| EA-ALIGN-READ-0006 | nan-sun; yuan-zhang; yongkun-yang; et al. | unlisted | `conditional` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 |
| EA-ALIGN-READ-0001 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-ALIGN-READ-0003 | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | unlisted | `limit` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottlen... |
| EA-ALIGN-READ-0004 | mathilde-hochedel; marc-lalonde | unlisted | `limit` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preproce... |
| EA-ALIGN-READ-0009 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 |

## Synthesis Slots

### 共识/正向证据
- `EA-WMDATA-READ-0007`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-...
- `EA-WMDATA-READ-0009`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations.
- `EA-WMDATA-READ-0008`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon future evolution rather t...
- `EA-4D-READ-0013`: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。
- `ERR-PVC-READ-0013`: 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。
- `ERR-PVC-READ-0014`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- `EA-WMEVAL-READ-0007`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- `EA-WMEVAL-READ-0005`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
### 条件成立
- `EA-4D-READ-0012`: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- `EA-4D-READ-0011`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- `EA-WMEVAL-READ-0014`: A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenari...
- `EA-WMEVAL-READ-0011`: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing...
- `EA-WMTASK-2026-0001`: In the DROID/RoboArena setting, a closed-loop video-world-model evaluator produced a policy ranking that closely matched the real-robot leaderboard across the evaluated policies, supporting policy ranking as a condition...
- `EA-ALIGN-READ-0006`: ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。
### 限制与失败模式
- `EA-EGO-2026-0003`: 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。
- `EA-CONTAM-2026-0007`: LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。
- `EA-WMEVAL-READ-0008`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- `EA-WMEVAL-READ-0015`: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- `EA-WMEVAL-READ-0013`: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- `EA-WMTASK-2026-0002`: RoboWorld's principal qualitative failures occur after object contact, when manipulated objects may disintegrate, morph unrealistically, or become visually inconsistent, limiting contact-rich manipulation evaluation and...
- `EA-ALIGN-READ-0001`: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- `EA-ALIGN-READ-0003`: Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under d...
### 开放问题
- `EA-WMEVAL-READ-0006`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- `EA-WMEVAL-READ-0004`: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 30 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-WMDATA-READ-0007` A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its...
  - `EA-WMDATA-READ-0009` World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrati...
  - `EA-WMDATA-READ-0008` Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to repr...
- Scientific memo preview: 《近一年世界视频模型最可靠的应用任务》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年世界视频模型最可靠的应用任务 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年世界视频模型最可靠的应用任务: 先看证据边界，再谈一个可传播的反常识洞察。

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
