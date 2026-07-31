# Review Packet: 近半年智能体技术在具身智能行业的发展应用

## Scope

- Topic: 近半年智能体技术在具身智能行业的发展应用
- Time range: 2026-01-25..2026-07-25
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-BIZ`
- Evidence events: 47
- Topic cards: 3
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 47
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-WMDATA-READ-0007`, `EA-WMDATA-READ-0009`, `EA-WMDATA-READ-0008`, `EA-4D-READ-0013`, `EA-4D-READ-0012`, `EA-4D-READ-0011`, `EA-WMEVAL-READ-0007`, `EA-WMEVAL-READ-0005`, `EA-WMEVAL-READ-0003`, `EA-WMEVAL-READ-0001`, `EA-WMEVAL-READ-0010`, `EA-WMEVAL-READ-0014`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 32 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 32
- Structure mapped: 32
- Deep-read papers: 32
- Claim-verified papers: 32
- Accepted evidence papers: 32
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- Fallback sources are review-packet context, not Hub evidence JSONL.

### official-context
- Gemini Robotics-ER 1.6: enhanced embodied reasoning - https://deepmind.google/blog/gemini-robotics-er-1-6/
- Open-source agent tools and skills for physical AI - https://nvidianews.nvidia.com/news/nvidia-releases-major-collection-of-open-source-agent-tools-and-skills-for-physical-ai
- Introducing Helix 02: Full-Body Autonomy - https://www.figure.ai/news/helix-02
- Figure signs agreement with Catalyst Brands - https://www.figure.ai/news/figure-signs-agreement-with-catalyst-brands
- Agility Robotics investor presentation - https://www.sec.gov/Archives/edgar/data/2074973/000121390026071287/ea029548401ex99-2.htm
- UBTECH and Hitachi strategic partnership - https://www.ubtrobot.com/en/about/news/826577556529221
- POSCO DX–NC AI industrial robot foundation model MOU - https://newsroom.posco.com/en/posco-dx-nc-ai-physical-ai-based-launch-of-joint-development-of-industrial-robot-foundation-model/
- PuduFM 1.0 - https://www.pudurobotics.com/en/news/pudu-robotics-unveils-pudufm-1-0-embodied-intelligence-foundation-model
- Unitree company timeline: UnifoLM-X1-0 factory test - https://www.unitree.com/about/
- Apptronik closes over $935 million Series A - https://apptronik.com/news-collection/apptronik-closes-over-935-million-series-a

### web-context
- Agility Robotics heads to Wall Street in a $2.5B bet - https://apnews.com/article/39f2356b9c1e167d0985b821f70079c5

## Topic Card Context

- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型、本体适配器与底层控制器组成的融合栈。近期突破不只是生成更长视频，而是把未来压缩成低频逻辑步骤、稀疏视觉子目标或结构化状态，并验证它与真实动作同步；BadWAM 说明“想象合理、动作错误”足以让系统失效。世界模型应先承担训练期教师、离线排序等低权限任务，再逐级争取在线规划权。Loco-manipulation 与多模态证据还表明，完整动作接口及按功能/时标分层的接触反馈会限制能力上限。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-BIZ` 产业落地与商业化: 具身智能 ToB 落地的核心瓶颈是可靠性与 ROI 闭环，而不是单点模型能力。客户关注稳定节拍、良率、安全、维护成本、集成周期和投资回收。短期最现实的不是通用机器人全场景替代，而是在结构化、数据可采、失败可控、工装可改造且价值密度高的工位形成商业闭环。“最后一厘米”需要视觉、力/力矩、触觉、末端执行器、柔顺控制和工装共同解决。
  - 短期最大约束常是场景和硬件，中期是数据，长期才更多转向模型。
  - 优先选择 ROI 明确、任务高频、失败可控、可采集数据、可改造工装的场景。
  - 最后一厘米本质是从视觉定位进入接触闭环，不能只靠视觉或大模型解决。
  - 节拍与成功率应作为风险控制问题动态平衡：高置信快，低置信慢并进入恢复策略。
  - 更可能先规模化的场景包括仓储物流、3C/电子制造、汽车零部件、半导体/光伏、医药实验室、食品饮料包装分拣。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。当前最可靠的应用位于权限阶梯低端：训练期 4D/几何教师、离线策略排序与淘汰、有本体锚定的数据/后训练，以及明确物理变量下的 what-if 检查；在线预演、直接控制和安全裁决需要逐级更强的真实闭环证据。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 17 |
| `conditional` | 条件成立 | 11 |
| `limit` | 限制/负面 | 17 |
| `gap` | 缺口 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2601.19510: ALRM: Agentic LLM for Robotic Manipulation | 2026-01-27 | conditional, limit, support | EA-AGENT-2026-0001; EA-AGENT-2026-0002; EA-AGENT-2026-0003 |
| 2602.11291: H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model | 2026-02-11T19:08:36Z | conditional, limit, support | EA-VLABREAK-2026-0001; EA-VLABREAK-2026-0002; EA-VLABREAK-2026-0003 |
| 2602.13081: Agentic AI for Robot Control: Flexible but still Fragile | 2026-02-13 | conditional, limit, support | EA-AGENT-2026-0004; EA-AGENT-2026-0005; EA-AGENT-2026-0006; EA-AGENT-2026-0007 |
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | gap | EA-WMEVAL-READ-0006 |
| 2603.03148: From Language to Action: Can LLM-Based Agents Be Used for Embodied Robot Cognition? | 2026-03-03 | conditional, limit | EA-AGENT-2026-0008; EA-AGENT-2026-0009; EA-AGENT-2026-0010 |
| 2603.05621: RACAS: Controlling Diverse Robots With a Single Agentic System | 2026-03-05 | limit, support | EA-AGENT-2026-0011; EA-AGENT-2026-0012; EA-AGENT-2026-0013 |
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
| 2606.29774: Analytic Concept-Centric Memory for Agentic Embodied Manipulation | 2026-06-29 | limit, support | EA-AGENT-2026-0014; EA-AGENT-2026-0015; EA-AGENT-2026-0016 |
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
| EA-AGENT-2026-0001 | EA-MODEL | `support` | `direct` | ALRM 将高层规划、执行与机器人 API 分层，并通过动作结果回传形成可修订计划的闭环。 | 规划器按思考—动作—观察循环拆解任务，执行器把结果作为观察返回。 (III LLM-Based Robotic Agent Architecture for Task Planning and Execution) | vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al. | 2601.19510 |
| EA-VLABREAK-2026-0001 | EA-MODEL | `support` | `direct` | H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 | 方法定义了逻辑世界模型、视觉世界模型、低层 VLA 和子任务完成检测的两时间尺度接口。 (IV-C Hierarchical World Model Guidance for VLA) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-AGENT-2026-0005 | EA-MODEL | `support` | `direct` | 同一高层循环在真实 Mobipick 上运行，并在约一天内通过更换提示与技能绑定迁移到 Valdemar 仿真场景。 | 迁移发生在高层编排层，低层平台 API 分别存在。 (6 Qualitative Validation on a Physical Robot with Simulated Transfer) | oscar-lima; marc-vinci; martin-gnther; et al. | 2602.13081 |
| EA-AGENT-2026-0011 | EA-MODEL | `support` | `direct` | RACAS 在三类差异显著的机器人上复用同一控制逻辑；适配只需更换机器人、动作和环境的提示配置。 | 轮式、机械肢体和水下平台均完成目标定位任务。 (III-B System Architecture) | dylan-r-ashley; jan-przepira; yimeng-chen; et al. | 2603.05621 |
| EA-VLABREAK-2026-0004 | EA-MODEL | `support` | `direct` | StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。 | 方法段给出动力学里程碑抽取和 planner-to-action 两阶段优化的完整链路。 (pages 5-8, Sections 3.1-3.3) | minghao-jin; mozheng-liao; mingfei-han; et al. | 2603.12553 |
| EA-ALIGN-READ-0015 | EA-MODEL | `support` | `direct` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 | ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classifi... | haodi-hu; chung-ta-huang; jing-liu; et al. | 2606.09630 |
| EA-AGENT-2026-0014 | EA-MODEL | `support` | `direct` | 具身智能体记忆可显式连接持久对象、场景状态、动作转移和可执行技能，并用前置条件与预期后果约束技能选择。 | 方法在检索后检查技能前置条件和预测后果，失败则写回并重检索。 (4.4 Memory-Grounded Reasoning and Execution) | mingyang-sun; xiujian-liang; jiude-wei; et al. | 2606.29774 |
| EA-AGENT-2026-0015 | EA-MODEL | `support` | `direct` | 在五个真实桌面记忆任务上，结构化记忆相对关键帧检索把平均成功率从 56% 提至 84%，检索准确率从 68% 提至 98%，检索努力从 4.5 降至 1.3。 | 最大增益出现在需要对象身份、场景关系和状态转移的任务。 (5.3 Real-World Memory Evaluation; Table 3) | mingyang-sun; xiujian-liang; jiude-wei; et al. | 2606.29774 |
| EA-AGENT-2026-0002 | EA-MODEL | `conditional` | `direct` | 在该 56 指令仿真基准上，Claude-4.1-Opus 的 TaP 成功率为 93.5%，CaP 为 92.6%，但平均延迟由 33.44 秒增至 82.60 秒。 | 同一模型在两种执行接口上的成功率差异很小，而延迟超过两倍。 (VI-A Operation Mode Comparison) | vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al. | 2601.19510 |
| EA-VLABREAK-2026-0002 | EA-MODEL | `conditional` | `direct` | 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 | H-WM 为 64.8%，logic-only 为 48.4%，H-WM-Stable-Diffusion 为 54.4%。 (VI Results) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-AGENT-2026-0004 | EA-MODEL | `conditional` | `direct` | 该架构把 LLM 限制在高层决策和技能调用；真实部署的前提是平台已有完整低层栈、语义状态快照及结构化成功/失败信号。 | 论文逐项列出导航、感知、抓取、运动规划、监控和技能返回要求。 (Real-World Execution Prerequisites) | oscar-lima; marc-vinci; martin-gnther; et al. | 2602.13081 |
| EA-AGENT-2026-0009 | EA-MODEL | `conditional` | `direct` | 在该实验中，情景记忆对任务成功率的作用因模型和任务而异，结论不确定；较稳定的收益是减少工具调用。 | 部分模型改善、部分任务下降；工具调用数总体减少。 (IV-D Benefits of Memory on Planning) | shinas-shaji; fabian-huppertz; alex-mitrevski; et al. | 2603.03148 |
| EA-AGENT-2026-0010 | EA-MODEL | `conditional` | `direct` | 模型可在占位空间、已占用位置等工具失败后自行重规划，但恢复过程仍可能受幻觉影响而产生新的失败。 | 定性观察同时记录自动恢复与恢复后误判。 (IV-E Qualitative Observations) | shinas-shaji; fabian-huppertz; alex-mitrevski; et al. | 2603.03148 |
| EA-VLABREAK-2026-0005 | EA-MODEL | `conditional` | `direct` | 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 | LIBERO 平均为 94.8%；实机 tidy-up 为 8/10，相同表面的 UniVLA 为 4/10。 (page 11) | minghao-jin; mozheng-liao; mingfei-han; et al. | 2603.12553 |
| EA-ALIGN-READ-0006 | EA-MODEL | `conditional` | `direct` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 | 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。 (Abstract (full-text section)) | nan-sun; yuan-zhang; yongkun-yang; et al. | 2606.03784 |
| EA-AGENT-2026-0003 | EA-MODEL | `limit` | `direct` | 该研究不能证明真实机器人部署可靠性，因为主要评测使用占位位姿和动作序列代理，作者也把真实机器人与感知整合列为后续工作。 | 评测目标是高层动作质量，不覆盖真实动力学、感知和连续运行。 (V-C Evaluation Design; VII Conclusion) | vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al. | 2601.19510 |
| EA-VLABREAK-2026-0003 | EA-MODEL | `limit` | `direct` | H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 | 结论明确列出额外组件/训练阶段的代价，以及对符号化状态的依赖。 (VII Conclusion) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-AGENT-2026-0006 | EA-MODEL | `limit` | `direct` | 长时执行仍会出现陈旧世界状态、提示约束违背、非确定性选择和不规则事件检查，因此灵活性没有转化为可预测可靠性。 | 多组实验分别暴露盲放、过期位姿、充电目标随机和事件检查不稳定。 (Abstract — cross-platform proof-of-concept fragility statement) | oscar-lima; marc-vinci; martin-gnther; et al. | 2602.13081 |
| EA-AGENT-2026-0007 | EA-MODEL | `limit` | `direct` | 基于轮询的事件检测无法在长动作中即时抢占；物理安全需要并发监控、可取消技能或把动作切成可中断检查点。 | 作者明确说明同步工具循环和现代智能体框架缺乏统一中断原语。 (7 Conclusions) | oscar-lima; marc-vinci; martin-gnther; et al. | 2602.13081 |
| EA-AGENT-2026-0008 | EA-MODEL | `limit` | `direct` | LLM 机器人智能体会在任务未真实完成时相信自己成功；这种误报会直接污染以自报结果标注的情景记忆。 | 论文用仿真世界状态对比模型自报状态，并观察到过度自信与错误记忆标签。 (IV-D Benefits of Memory on Planning) | shinas-shaji; fabian-huppertz; alex-mitrevski; et al. | 2603.03148 |
| EA-AGENT-2026-0012 | EA-MODEL | `limit` | `direct` | 当前系统约每 5–10 秒才执行一个动作；作者认为这种逐步推理成本让长时接触操作实验慢到不可行。 | 时延由 API 推理主导，作者建议把操作原语作为更粗粒度工具。 (IV-D Implementation Details; VII LIMITATIONS AND FUTURE WORK) | dylan-r-ashley; jan-przepira; yimeng-chen; et al. | 2603.05621 |
| EA-AGENT-2026-0013 | EA-MODEL | `limit` | `direct` | 缺少显式深度使 VLM 对碰撞风险的判断过度或不足自信，说明自然语言视觉接口不能替代安全几何感知。 | 作者把深度不足列为持续损害系统能力的问题。 (VII LIMITATIONS AND FUTURE WORK) | dylan-r-ashley; jan-przepira; yimeng-chen; et al. | 2603.05621 |
| EA-ALIGN-READ-0001 | EA-MODEL | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-AGENT-2026-0016 | EA-MODEL | `limit` | `direct` | 该记忆路线尚未证明可变形物和强感知/状态漂移下的鲁棒性，模板库覆盖是重要边界。 | 作者把扩展可变形物与抵抗感知噪声、状态漂移列为未来工作。 (6 Conclusion) | mingyang-sun; xiujian-liang; jiude-wei; et al. | 2606.29774 |
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
| EA-AGENT-2026-0001 | vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al. | unlisted | `support` | ALRM 将高层规划、执行与机器人 API 分层，并通过动作结果回传形成可修订计划的闭环。 |
| EA-VLABREAK-2026-0001 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `support` | H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 |
| EA-AGENT-2026-0005 | oscar-lima; marc-vinci; martin-gnther; et al. | unlisted | `support` | 同一高层循环在真实 Mobipick 上运行，并在约一天内通过更换提示与技能绑定迁移到 Valdemar 仿真场景。 |
| EA-AGENT-2026-0011 | dylan-r-ashley; jan-przepira; yimeng-chen; et al. | unlisted | `support` | RACAS 在三类差异显著的机器人上复用同一控制逻辑；适配只需更换机器人、动作和环境的提示配置。 |
| EA-VLABREAK-2026-0004 | minghao-jin; mozheng-liao; mingfei-han; et al. | unlisted | `support` | StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。 |
| EA-ALIGN-READ-0015 | haodi-hu; chung-ta-huang; jing-liu; et al. | unlisted | `support` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 |
| EA-AGENT-2026-0014 | mingyang-sun; xiujian-liang; jiude-wei; et al. | unlisted | `support` | 具身智能体记忆可显式连接持久对象、场景状态、动作转移和可执行技能，并用前置条件与预期后果约束技能选择。 |
| EA-AGENT-2026-0015 | mingyang-sun; xiujian-liang; jiude-wei; et al. | unlisted | `support` | 在五个真实桌面记忆任务上，结构化记忆相对关键帧检索把平均成功率从 56% 提至 84%，检索准确率从 68% 提至 98%，检索努力从 4.5 降至 1.3。 |
| EA-AGENT-2026-0002 | vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al. | unlisted | `conditional` | 在该 56 指令仿真基准上，Claude-4.1-Opus 的 TaP 成功率为 93.5%，CaP 为 92.6%，但平均延迟由 33.44 秒增至 82.60 秒。 |
| EA-VLABREAK-2026-0002 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `conditional` | 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 |
| EA-AGENT-2026-0004 | oscar-lima; marc-vinci; martin-gnther; et al. | unlisted | `conditional` | 该架构把 LLM 限制在高层决策和技能调用；真实部署的前提是平台已有完整低层栈、语义状态快照及结构化成功/失败信号。 |
| EA-AGENT-2026-0009 | shinas-shaji; fabian-huppertz; alex-mitrevski; et al. | unlisted | `conditional` | 在该实验中，情景记忆对任务成功率的作用因模型和任务而异，结论不确定；较稳定的收益是减少工具调用。 |
| EA-AGENT-2026-0010 | shinas-shaji; fabian-huppertz; alex-mitrevski; et al. | unlisted | `conditional` | 模型可在占位空间、已占用位置等工具失败后自行重规划，但恢复过程仍可能受幻觉影响而产生新的失败。 |
| EA-VLABREAK-2026-0005 | minghao-jin; mozheng-liao; mingfei-han; et al. | unlisted | `conditional` | 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 |
| EA-ALIGN-READ-0006 | nan-sun; yuan-zhang; yongkun-yang; et al. | unlisted | `conditional` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 |
| EA-AGENT-2026-0003 | vitor-gaboardi-dos-santos; ibrahim-khadraoui; ibrahim-farhat; et al. | unlisted | `limit` | 该研究不能证明真实机器人部署可靠性，因为主要评测使用占位位姿和动作序列代理，作者也把真实机器人与感知整合列为后续工作。 |
| EA-VLABREAK-2026-0003 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `limit` | H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 |
| EA-AGENT-2026-0006 | oscar-lima; marc-vinci; martin-gnther; et al. | unlisted | `limit` | 长时执行仍会出现陈旧世界状态、提示约束违背、非确定性选择和不规则事件检查，因此灵活性没有转化为可预测可靠性。 |
| EA-AGENT-2026-0007 | oscar-lima; marc-vinci; martin-gnther; et al. | unlisted | `limit` | 基于轮询的事件检测无法在长动作中即时抢占；物理安全需要并发监控、可取消技能或把动作切成可中断检查点。 |
| EA-AGENT-2026-0008 | shinas-shaji; fabian-huppertz; alex-mitrevski; et al. | unlisted | `limit` | LLM 机器人智能体会在任务未真实完成时相信自己成功；这种误报会直接污染以自报结果标注的情景记忆。 |
| EA-AGENT-2026-0012 | dylan-r-ashley; jan-przepira; yimeng-chen; et al. | unlisted | `limit` | 当前系统约每 5–10 秒才执行一个动作；作者认为这种逐步推理成本让长时接触操作实验慢到不可行。 |
| EA-AGENT-2026-0013 | dylan-r-ashley; jan-przepira; yimeng-chen; et al. | unlisted | `limit` | 缺少显式深度使 VLM 对碰撞风险的判断过度或不足自信，说明自然语言视觉接口不能替代安全几何感知。 |
| EA-ALIGN-READ-0001 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-AGENT-2026-0016 | mingyang-sun; xiujian-liang; jiude-wei; et al. | unlisted | `limit` | 该记忆路线尚未证明可变形物和强感知/状态漂移下的鲁棒性，模板库覆盖是重要边界。 |
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
- `EA-AGENT-2026-0002`: 在该 56 指令仿真基准上，Claude-4.1-Opus 的 TaP 成功率为 93.5%，CaP 为 92.6%，但平均延迟由 33.44 秒增至 82.60 秒。
- `EA-VLABREAK-2026-0002`: 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。
- `EA-AGENT-2026-0004`: 该架构把 LLM 限制在高层决策和技能调用；真实部署的前提是平台已有完整低层栈、语义状态快照及结构化成功/失败信号。
- `EA-AGENT-2026-0009`: 在该实验中，情景记忆对任务成功率的作用因模型和任务而异，结论不确定；较稳定的收益是减少工具调用。
### 限制与失败模式
- `EA-WMEVAL-READ-0008`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- `EA-WMEVAL-READ-0015`: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- `EA-WMEVAL-READ-0013`: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- `EA-AGENT-2026-0003`: 该研究不能证明真实机器人部署可靠性，因为主要评测使用占位位姿和动作序列代理，作者也把真实机器人与感知整合列为后续工作。
- `EA-VLABREAK-2026-0003`: H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。
- `EA-AGENT-2026-0006`: 长时执行仍会出现陈旧世界状态、提示约束违背、非确定性选择和不规则事件检查，因此灵活性没有转化为可预测可靠性。
- `EA-AGENT-2026-0007`: 基于轮询的事件检测无法在长动作中即时抢占；物理安全需要并发监控、可取消技能或把动作切成可中断检查点。
- `EA-AGENT-2026-0008`: LLM 机器人智能体会在任务未真实完成时相信自己成功；这种误报会直接污染以自报结果标注的情景记忆。
### 开放问题
- `EA-WMEVAL-READ-0006`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- `EA-WMEVAL-READ-0004`: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 32 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-WMDATA-READ-0007` A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its...
  - `EA-WMDATA-READ-0009` World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrati...
  - `EA-WMDATA-READ-0008` Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to repr...
- Scientific memo preview: 《近半年智能体技术在具身智能行业的发展应用》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近半年智能体技术在具身智能行业的发展应用 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近半年智能体技术在具身智能行业的发展应用: 先看证据边界，再谈一个可传播的反常识洞察。

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
