# Review Packet: 世界模型需要什么样的训练数据

## Scope

- Topic: 世界模型需要什么样的训练数据
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-MODEL`, `EA-EVAL`, `EA-4D`
- Evidence events: 39
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> full-text evidence -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval, HTML/PDF/OCR recovery, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 39
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-2026-WMDATA-0001`, `EA-DATA-2026-WMDATA-0003`, `EA-DATA-2026-WMDATA-0014`, `EA-DATA-2026-WMDATA-0002`, `EA-DATA-2026-4D-0007`, `EA-DATA-2026-WMDATA-0006`, `EA-DATA-2026-4D-0011`, `EA-DATA-2026-WMDATA-0004`, `EA-DATA-2026-WMDATA-0012`, `EA-DATA-2026-WMDATA-0011`, `EA-EVAL-2026-4D-0004`, `EA-EVAL-2026-4D-0006`
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

- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；高分筛选还必须保留任务、本体、场景和长尾覆盖。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。所有异构数据都应声明其可信监督字段，并以真实闭环收益作为最终验收。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。VLA 可以继承视觉和语言先验，却不会自动继承运动、接触和控制器先验；语言—视觉—动作接口需要显式对齐。4D 和世界模型可以提供几何动态监督、未来想象和动作筛选，但训练目标必须面向动作质量而非只追求视觉重建。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测应分开记录预测保真与决策有效，防止“视频更真实”掩盖错误动作响应。
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
| `support` | 支持 | 17 |
| `conditional` | 条件成立 | 10 |
| `limit` | 限制/负面 | 9 |
| `gap` | 缺口 | 3 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.15549: VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing | 2026-02-17 | conditional, limit | EA-EVAL-2026-SMOKE-0004; EA-EVAL-2026-SMOKE-0005 |
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | gap, support | EA-EVAL-2026-4D-0004; EA-MODEL-2026-4D-0003; EA-MODEL-2026-4D-0005 |
| 2603.08546: Interactive World Simulator for Robot Policy Training and Evaluation | 2026-03-09 | support | EA-DATA-2026-WMDATA-0001 |
| 2603.13788: ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation | 2026-03-14 | conditional, support | EA-EVAL-2026-4D-0002; EA-MODEL-2026-4D-0001 |
| 2603.15467: Evaluating Time Awareness and Cross-modal Active Perception of Large Models via 4D Escape Room Task | 2026-03-16 | gap | EA-EVAL-2026-4D-0020 |
| 2603.16669: Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation | 2026-03-17 | conditional, support | EA-DATA-2026-4D-0007; EA-EVAL-2026-4D-0006 |
| 2604.11386: ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation | 2026-04-13 | conditional | EA-DATA-2026-WMDATA-0006 |
| 2604.21741: Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training | 2026-04-23 | support | EA-DATA-2026-WMDATA-0003 |
| 2605.00121: Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes | 2026-04-30 | limit, support | EA-SENSOR-2026-4D-0015; EA-SENSOR-2026-4D-0016 |
| 2605.17682: GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning | 2026-05-17 | support | EA-SENSOR-2026-4D-0019 |
| 2605.20752: GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation | 2026-05-20 | support | EA-MODEL-2026-WMDATA-0009 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | limit, support | EA-MODEL-2026-4D-0008; EA-MODEL-2026-4D-0009; EA-MODEL-2026-WMDATA-0008 |
| 2605.27947: SANTS: A State-Adaptive Scheduler for World Action Models | 2026-05-27 | limit | EA-EVAL-2026-WMDATA-0013 |
| 2605.29360: MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models | 2026-05-28 | gap | EA-EVAL-2026-SMOKE-0001 |
| 2605.29879: DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding | 2026-05-28 | limit, support | EA-SENSOR-2026-4D-0017; EA-SENSOR-2026-4D-0018 |
| 2606.00113: World Models for Robotic Manipulation: A Survey | 2026-05-27 | support | EA-DATA-2026-WMDATA-0014 |
| 2606.00664: SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models | 2026-05-30 | conditional, support | EA-EVAL-2026-MEMO-0006; EA-MODEL-2026-WMDATA-0007 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional, support | EA-DATA-2026-4D-0011; EA-DATA-2026-WMDATA-0002; EA-EVAL-2026-4D-0012; EA-EVAL-2026-SMOKE-0003; EA-MODEL-2026-4D-0010 |
| 2606.01600: RoboTrustBench: Benchmarking the Trustworthiness of Video World Models for Robotic Manipulation | 2026-06-01 | limit | EA-EVAL-2026-SMOKE-0002 |
| 2606.02577: RoboDream: Compositional World Models for Scalable Robot Data Synthesis | 2026-06-01 | conditional | EA-DATA-2026-WMDATA-0004 |
| 2606.12072: World Model Self-Distillation: Training World Models to Solve General Tasks | 2026-06-10 | conditional | EA-DATA-2026-WMDATA-0012 |
| 2606.12217: Making Foresight Actionable: Repurposing Representation Alignment in World Action Models | 2026-06-10 | limit | EA-MODEL-2026-WMDATA-0010 |
| 2606.12403: World Pilot: Steering Vision-Language-Action Models with World-Action Priors | 2026-06-10 | limit | EA-DATA-2026-WMDATA-0011 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | limit, support | EA-EVAL-2026-4D-0013; EA-EVAL-2026-4D-0014 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-2026-WMDATA-0001 | EA-DATA | `support` | `direct` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-c... | The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real perform... | yixuan-wang | 2603.08546 |
| EA-DATA-2026-WMDATA-0003 | EA-DATA | `support` | `direct` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. | Hi-WM rolls policies inside a world model, lets humans intervene when rollouts become incorrect or failure-prone, caches and branches failure states, and adds corrective trajectories back into the training set for post-... | yaxuan-li | 2604.21741 |
| EA-DATA-2026-WMDATA-0014 | EA-DATA | `support` | `direct` | A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under intervention, with mo... | The survey distinguishes ordinary policy datasets from world-model datasets, reviews 34 manipulation datasets, and states that useful world-model data should include temporally aligned observations/actions, diversity fo... | wm-manipulation-survey-authors | 2606.00113 |
| EA-DATA-2026-WMDATA-0002 | EA-DATA | `support` | `direct` | Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations, broad egocentric hu... | τ0-WM reports a 27.3K-hour corpus containing real-robot teleoperation, UMI-style interaction, egocentric human videos, and rollout/failure trajectories; the paper explains that these sources differ in action fidelity, e... | pengfei-zhou | 2606.01027 |
| EA-DATA-2026-4D-0007 | EA-DATA | `conditional` | `direct` | Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial cons... | The supplementary discussion says ST-v2 pseudo-annotations may not be absolute sub-millimeter ground truth, but are sufficiently high-fidelity for relative spatial geometry; the authors prioritize breadth of data to lea... | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-DATA-2026-WMDATA-0006 | EA-DATA | `conditional` | `direct` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve re... | ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate... | yiran-qin | 2604.11386 |
| EA-DATA-2026-4D-0011 | EA-DATA | `conditional` | `direct` | τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding. | The introduction contrasts broad visual dynamics in egocentric and human interaction video with narrow but executable robot demonstrations, then uses modality-specific supervision masks so each data source supervises on... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-DATA-2026-WMDATA-0004 | EA-DATA | `conditional` | `direct` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel object... | RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost... | junjie-ye | 2606.02577 |
| EA-DATA-2026-WMDATA-0012 | EA-DATA | `conditional` | `direct` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and... | WMSD frames supervised fine-tuning on paired task-execution videos as costly, then proposes self-distillation and reinforcement learning where a VLM generates tasks/solutions from unlabeled scene images and feedback ver... | sebastian-stapf | 2606.12072 |
| EA-DATA-2026-WMDATA-0011 | EA-DATA | `limit` | `direct` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. | World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy. (Abstract... | world-pilot-authors | 2606.12403 |
| EA-EVAL-2026-4D-0004 | EA-EVAL | `support` | `direct` | Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only predic... | The paper compares supervision targets and reports that full-horizon 3D point-track supervision gives larger RoboCasa gains than 2D tracks, goal-only prediction, environment-only points, robot-only points, or future dep... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-EVAL-2026-4D-0006 | EA-EVAL | `support` | `direct` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... | The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap... | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-EVAL-2026-4D-0013 | EA-EVAL | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |
| EA-EVAL-2026-SMOKE-0004 | EA-EVAL | `conditional` | `direct` | For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking d... | VLM-DEWM validates each VLM decision against a persistent world model and uses discrepancy analysis for targeted recovery, with reported gains in state tracking and recovery success in long-horizon manufacturing tasks.... | guoqin-tang | 2602.15549 |
| EA-EVAL-2026-4D-0002 | EA-EVAL | `conditional` | `direct` | ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset... | The evaluation reports 44.6% zero-shot success-rate gains in simulation and 30.3% real-world gains, while the conclusion notes degradation risks in extreme clutter and dependence on single-view execution and SAM2 segmen... | you-wu; zixuan-chen; cunxu-ou | 2603.13788 |
| EA-EVAL-2026-MEMO-0006 | EA-EVAL | `conditional` | `direct` | Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic fr... | The paper argues that pixel-space rollout is expensive, but indiscriminate frame dropping is misaligned with embodied manipulation because critical task events may involve only small visual changes and become unrecovera... | ziheng-he | 2606.00664 |
| EA-EVAL-2026-4D-0012 | EA-EVAL | `conditional` | `direct` | τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensing, uncertainty esti... | The experiments report better performance on long-horizon real-robot tasks, data-mixture gains, and a single-attempt success-rate increase from 0.43 to 0.60 with action selection plus rectification; the conclusion notes... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-EVAL-2026-SMOKE-0003 | EA-EVAL | `conditional` | `direct` | A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action candidates. | The paper presents a unified video-action world model that combines policy learning, video prediction, and action evaluation, using test-time sampling, ranking, and simulator-based rectification before execution. (Abstr... | pengfei-zhou | 2606.01027 |
| EA-EVAL-2026-SMOKE-0005 | EA-EVAL | `limit` | `direct` | External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometr... | The limitations section identifies upstream perception errors, open-vocabulary failures under closed-world assumptions, and a dynamics gap in the physical verification scope. (4.4.2 Limitations and Failure Mode Analysis... | guoqin-tang | 2602.15549 |
| EA-EVAL-2026-WMDATA-0013 | EA-EVAL | `limit` | `direct` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less acti... | SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video... | sants-authors | 2605.27947 |
| EA-EVAL-2026-SMOKE-0002 | EA-EVAL | `limit` | `direct` | Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following d... | RoboTrustBench evaluates video world models with four scenario types and a six-dimensional protocol, reporting failures in constraint reasoning, counterfactual grounding, physical interaction, and unsafe-instruction sup... | huiqiong-li | 2606.01600 |
| EA-EVAL-2026-4D-0014 | EA-EVAL | `limit` | `direct` | WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, dat... | The limitations section states that visual observations expose only partial physical state; tactile, force-torque, or depth sensing may be needed; deformable and granular dynamics remain difficult; latency restricts pla... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |
| EA-EVAL-2026-4D-0020 | EA-EVAL | `gap` | `direct` | EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual... | The benchmark introduces time-varying visual and audio cues, trigger-based evidence, and time-limited clues; results show models degrade under modality bias, missed triggers, and time-sensitive decisions, indicating gap... | yurui-dong; ziyue-wang; shuyun-lu | 2603.15467 |
| EA-EVAL-2026-SMOKE-0001 | EA-EVAL | `gap` | `direct` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias... | The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias. (Abstract... | tianzhuo-yang | 2605.29360 |
| EA-MODEL-2026-4D-0003 | EA-MODEL | `support` | `direct` | Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geometry evolves over ti... | The authors state that action labels tell a policy how to move but not what will happen; Pri4R adds a point-track head during training and discards it at inference, leaving the original VLA interface unchanged. (Abstrac... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-MODEL-2026-4D-0001 | EA-MODEL | `support` | `direct` | ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories and 4D temporal con... | The paper argues that 2D intermediate representations lose depth and temporal continuity, then proposes unified 3D-4D representations with trajectories and smooth spatial masks for online replanning and long-horizon exe... | you-wu; zixuan-chen; cunxu-ou | 2603.13788 |
| EA-MODEL-2026-4D-0009 | EA-MODEL | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-MODEL-2026-WMDATA-0008 | EA-MODEL | `support` | `direct` | World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions. | GEM-4D injects dense 4D correspondence supervision from a geometry foundation model into a video generative backbone during training, arguing that correspondence consistency makes future rollouts more reliable for actio... | gem-4d-authors | 2605.22882 |
| EA-MODEL-2026-WMDATA-0009 | EA-MODEL | `support` | `direct` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and... | GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference. (Ab... | gaussiandream-authors | 2605.20752 |
| EA-MODEL-2026-WMDATA-0007 | EA-MODEL | `support` | `direct` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remov... | SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as pol... | ziheng-he | 2606.00664 |
| EA-MODEL-2026-4D-0010 | EA-MODEL | `support` | `direct` | τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, then revise low-quality... | The paper describes a unified video-action world model with a video action model and an action-conditioned video simulator; at inference it samples candidates, ranks them, simulates futures, estimates progress, and rect... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-MODEL-2026-4D-0008 | EA-MODEL | `limit` | `direct` | GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences ov... | The introduction says photorealistic generated videos can have drifting contacts, inconsistent depth, and non-rigid deformation artifacts that break action extraction; pixel or latent losses do not guarantee corresponde... | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-MODEL-2026-WMDATA-0010 | EA-MODEL | `limit` | `direct` | World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to t... | The paper diagnoses a representation mismatch in WAMs, where action decoders attend to task-irrelevant areas despite plausible visual futures, and proposes an Action-Grounded Representation Alignment objective for the w... | yuying-ge | 2606.12217 |
| EA-MODEL-2026-4D-0005 | EA-MODEL | `gap` | `direct` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. | The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could furth... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-SENSOR-2026-4D-0015 | EA-SENSOR | `support` | `direct` | PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-receptacle states and pl... | The paper builds Perpetua* Bayesian persistence filters into a 3D scene graph, validates future state prediction in simulation and a three-week real-world semi-static lab setting, and shows navigation can avoid an expec... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-SENSOR-2026-4D-0019 | EA-SENSOR | `support` | `direct` | GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autor... | The paper decouples spatial geometry, temporal support, semantics, opacity, and motion in Gaussian primitives, then slices and splats them into future occupancy volumes at arbitrary timestamps and supervises both occupa... | cheng-chen; hao-huang; saurabh-bagchi | 2605.17682 |
| EA-SENSOR-2026-4D-0017 | EA-SENSOR | `support` | `direct` | DGSG-Mind combines dynamic 3D Gaussian mapping with scene graphs so that embodied agents can update object-level topology and reason over spatial-semantic relations in changing en... | The system fuses probabilistic voxels and 3D Gaussians, performs Gaussian-based camera relocalization and localized masked refinement for additions/removals, synchronizes graph nodes, and uses annotated Gaussian renderi... | luzhou-ge; xiangyu-zhu; jinyan-liu | 2605.29879 |
| EA-SENSOR-2026-4D-0016 | EA-SENSOR | `limit` | `direct` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. | The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and plannin... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-SENSOR-2026-4D-0018 | EA-SENSOR | `limit` | `direct` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. | The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs. (V Conclus... | luzhou-ge; xiangyu-zhu; jinyan-liu | 2605.29879 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-2026-WMDATA-0001 | yixuan-wang | unlisted | `support` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depe... |
| EA-DATA-2026-WMDATA-0003 | yaxuan-li | unlisted | `support` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. |
| EA-DATA-2026-WMDATA-0014 | wm-manipulation-survey-authors | unlisted | `support` | A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under i... |
| EA-DATA-2026-WMDATA-0002 | pengfei-zhou | unlisted | `support` | Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations,... |
| EA-DATA-2026-4D-0007 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `conditional` | Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning r... |
| EA-DATA-2026-WMDATA-0006 | yiran-qin | unlisted | `conditional` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pa... |
| EA-DATA-2026-4D-0011 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executab... |
| EA-DATA-2026-WMDATA-0004 | junjie-ye | USC | `conditional` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrat... |
| EA-DATA-2026-WMDATA-0012 | sebastian-stapf | University of Bern | `conditional` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM... |
| EA-DATA-2026-WMDATA-0011 | world-pilot-authors | unlisted | `limit` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution... |
| EA-EVAL-2026-4D-0004 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `support` | Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D trac... |
| EA-EVAL-2026-4D-0006 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `support` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while... |
| EA-EVAL-2026-4D-0013 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-EVAL-2026-SMOKE-0004 | guoqin-tang | Beijing University of Posts and Telecommunications | `conditional` | For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reas... |
| EA-EVAL-2026-4D-0002 | you-wu; zixuan-chen; cunxu-ou | unlisted | `conditional` | ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is... |
| EA-EVAL-2026-MEMO-0006 | ziheng-he | UCAS | `conditional` | Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inferenc... |
| EA-EVAL-2026-4D-0012 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensi... |
| EA-EVAL-2026-SMOKE-0003 | pengfei-zhou | unlisted | `conditional` | A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action... |
| EA-EVAL-2026-SMOKE-0005 | guoqin-tang | Beijing University of Posts and Telecommunications | `limit` | External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel... |
| EA-EVAL-2026-WMDATA-0013 | sants-authors | unlisted | `limit` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising... |
| EA-EVAL-2026-SMOKE-0002 | huiqiong-li | Singapore Management University | `limit` | Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface ins... |
| EA-EVAL-2026-4D-0014 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `limit` | WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited pl... |
| EA-EVAL-2026-4D-0020 | yurui-dong; ziyue-wang; shuyun-lu | unlisted | `gap` | EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not on... |
| EA-EVAL-2026-SMOKE-0001 | tianzhuo-yang | Peking University | `gap` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelit... |
| EA-MODEL-2026-4D-0003 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `support` | Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geom... |
| EA-MODEL-2026-4D-0001 | you-wu; zixuan-chen; cunxu-ou | unlisted | `support` | ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories... |
| EA-MODEL-2026-4D-0009 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-MODEL-2026-WMDATA-0008 | gem-4d-authors | unlisted | `support` | World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable r... |
| EA-MODEL-2026-WMDATA-0009 | gaussiandream-authors | unlisted | `support` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent curr... |
| EA-MODEL-2026-WMDATA-0007 | ziheng-he | UCAS | `support` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic fram... |
| EA-MODEL-2026-4D-0010 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `support` | τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, the... |
| EA-MODEL-2026-4D-0008 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `limit` | GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3... |
| EA-MODEL-2026-WMDATA-0010 | yuying-ge | unlisted | `limit` | World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control... |
| EA-MODEL-2026-4D-0005 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `gap` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. |
| EA-SENSOR-2026-4D-0015 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `support` | PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-rece... |
| EA-SENSOR-2026-4D-0019 | cheng-chen; hao-huang; saurabh-bagchi | unlisted | `support` | GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning with... |
| EA-SENSOR-2026-4D-0017 | luzhou-ge; xiangyu-zhu; jinyan-liu | unlisted | `support` | DGSG-Mind combines dynamic 3D Gaussian mapping with scene graphs so that embodied agents can update object-level topology and reason over spatial-semantic rela... |
| EA-SENSOR-2026-4D-0016 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `limit` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verifica... |
| EA-SENSOR-2026-4D-0018 | luzhou-ge; xiangyu-zhu; jinyan-liu | unlisted | `limit` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-2026-WMDATA-0001`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-...
- `EA-DATA-2026-WMDATA-0003`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations.
- `EA-DATA-2026-WMDATA-0014`: A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under intervention, with modalities beyond RGB when physical intera...
- `EA-DATA-2026-WMDATA-0002`: Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations, broad egocentric human videos, and rollout or failure traje...
- `EA-EVAL-2026-4D-0004`: Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only prediction, or dense depth prediction.
- `EA-EVAL-2026-4D-0006`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- `EA-EVAL-2026-4D-0013`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
- `EA-MODEL-2026-4D-0003`: Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geometry evolves over time.
### 条件成立
- `EA-DATA-2026-4D-0007`: Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial constraints and motion priors.
- `EA-DATA-2026-WMDATA-0006`: A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenari...
- `EA-DATA-2026-4D-0011`: τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding.
- `EA-DATA-2026-WMDATA-0004`: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing...
- `EA-DATA-2026-WMDATA-0012`: Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM feedback as weak ver...
- `EA-EVAL-2026-SMOKE-0004`: For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before execution.
- `EA-EVAL-2026-4D-0002`: ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset, masking pipeline, and task setup.
- `EA-EVAL-2026-MEMO-0006`: Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic frame dropping can remove exactly the even...
### 限制与失败模式
- `EA-DATA-2026-WMDATA-0011`: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- `EA-EVAL-2026-SMOKE-0005`: External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometry-only checks do not verify dynamics or...
- `EA-EVAL-2026-WMDATA-0013`: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- `EA-EVAL-2026-SMOKE-0002`: Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following do not establish robotic trustworthiness.
- `EA-EVAL-2026-4D-0014`: WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, data coverage, and noisy reward supervision...
- `EA-MODEL-2026-4D-0008`: GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences over time.
- `EA-MODEL-2026-WMDATA-0010`: World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to task-relevant interaction regions.
- `EA-SENSOR-2026-4D-0016`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
### 开放问题
- `EA-EVAL-2026-4D-0020`: EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual scenes.
- `EA-EVAL-2026-SMOKE-0001`: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.
- `EA-MODEL-2026-4D-0005`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 24 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DATA-2026-WMDATA-0001` A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its...
  - `EA-DATA-2026-WMDATA-0003` World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrati...
  - `EA-DATA-2026-WMDATA-0014` A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evol...
- Scientific memo preview: 《世界模型需要什么样的训练数据》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 世界模型需要什么样的训练数据 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 世界模型需要什么样的训练数据: 先看证据边界，再谈一个可传播的反常识洞察。

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
