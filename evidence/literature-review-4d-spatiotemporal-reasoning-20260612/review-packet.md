# Review Packet: 4D时空推理

## Scope

- Topic: 4D时空推理
- Time range: 2025-12-12..2026-06-12
- Review style: `survey`
- Knowledge IDs: `EA-SENSOR`, `EA-MODEL`, `EA-EVAL`
- Evidence events: 20
- Topic cards: 3
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
- Trace IDs: `EA-DATA-2026-4D-0007`, `EA-DATA-2026-4D-0011`, `EA-EVAL-2026-4D-0004`, `EA-EVAL-2026-4D-0006`, `EA-EVAL-2026-4D-0013`, `EA-EVAL-2026-4D-0002`, `EA-EVAL-2026-4D-0012`, `EA-EVAL-2026-4D-0014`, `EA-EVAL-2026-4D-0020`, `EA-MODEL-2026-4D-0003`, `EA-MODEL-2026-4D-0001`, `EA-MODEL-2026-4D-0009`
- Registered sources: `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Paper-level sources: 10 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

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
| `support` | 支持 | 10 |
| `conditional` | 条件成立 | 4 |
| `limit` | 限制/负面 | 4 |
| `gap` | 缺口 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | gap, support | EA-MODEL-2026-4D-0003; EA-EVAL-2026-4D-0004; EA-MODEL-2026-4D-0005 |
| 2603.13788: ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation | 2026-03-14 | conditional, support | EA-MODEL-2026-4D-0001; EA-EVAL-2026-4D-0002 |
| 2603.15467: Evaluating Time Awareness and Cross-modal Active Perception of Large Models via 4D Escape Room Task | 2026-03-16 | gap | EA-EVAL-2026-4D-0020 |
| 2603.16669: Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation | 2026-03-17 | conditional, support | EA-EVAL-2026-4D-0006; EA-DATA-2026-4D-0007 |
| 2605.00121: Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes | 2026-04-30 | limit, support | EA-SENSOR-2026-4D-0015; EA-SENSOR-2026-4D-0016 |
| 2605.17682: GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning | 2026-05-17 | support | EA-SENSOR-2026-4D-0019 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | limit, support | EA-MODEL-2026-4D-0008; EA-MODEL-2026-4D-0009 |
| 2605.29879: DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding | 2026-05-28 | limit, support | EA-SENSOR-2026-4D-0017; EA-SENSOR-2026-4D-0018 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional, support | EA-MODEL-2026-4D-0010; EA-DATA-2026-4D-0011; EA-EVAL-2026-4D-0012 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | limit, support | EA-EVAL-2026-4D-0013; EA-EVAL-2026-4D-0014 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-2026-4D-0007 | EA-DATA | `conditional` | `direct` | Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial cons... | The supplementary discussion says ST-v2 pseudo-annotations may not be absolute sub-millimeter ground truth, but are sufficiently high-fidelity for relative spatial geometry; the authors prioritize breadth of data to lea... | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-DATA-2026-4D-0011 | EA-DATA | `conditional` | `direct` | τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding. | The introduction contrasts broad visual dynamics in egocentric and human interaction video with narrow but executable robot demonstrations, then uses modality-specific supervision masks so each data source supervises on... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-EVAL-2026-4D-0004 | EA-EVAL | `support` | `direct` | Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only predic... | The paper compares supervision targets and reports that full-horizon 3D point-track supervision gives larger RoboCasa gains than 2D tracks, goal-only prediction, environment-only points, robot-only points, or future dep... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-EVAL-2026-4D-0006 | EA-EVAL | `support` | `direct` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... | The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap... | mutian-xu; tianbao-zhang; tianqi-liu | 2603.16669 |
| EA-EVAL-2026-4D-0013 | EA-EVAL | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |
| EA-EVAL-2026-4D-0002 | EA-EVAL | `conditional` | `direct` | ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset... | The evaluation reports 44.6% zero-shot success-rate gains in simulation and 30.3% real-world gains, while the conclusion notes degradation risks in extreme clutter and dependence on single-view execution and SAM2 segmen... | you-wu; zixuan-chen; cunxu-ou | 2603.13788 |
| EA-EVAL-2026-4D-0012 | EA-EVAL | `conditional` | `direct` | τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensing, uncertainty esti... | The experiments report better performance on long-horizon real-robot tasks, data-mixture gains, and a single-attempt success-rate increase from 0.43 to 0.60 with action selection plus rectification; the conclusion notes... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-EVAL-2026-4D-0014 | EA-EVAL | `limit` | `direct` | WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, dat... | The limitations section states that visual observations expose only partial physical state; tactile, force-torque, or depth sensing may be needed; deformable and granular dynamics remain difficult; latency restricts pla... | arnav-kumar-jain; yilin-wu; jesse-farebrother | 2606.13672 |
| EA-EVAL-2026-4D-0020 | EA-EVAL | `gap` | `direct` | EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual... | The benchmark introduces time-varying visual and audio cues, trigger-based evidence, and time-limited clues; results show models degrade under modality bias, missed triggers, and time-sensitive decisions, indicating gap... | yurui-dong; ziyue-wang; shuyun-lu | 2603.15467 |
| EA-MODEL-2026-4D-0003 | EA-MODEL | `support` | `direct` | Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geometry evolves over ti... | The authors state that action labels tell a policy how to move but not what will happen; Pri4R adds a point-track head during training and discards it at inference, leaving the original VLA interface unchanged. (Abstrac... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-MODEL-2026-4D-0001 | EA-MODEL | `support` | `direct` | ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories and 4D temporal con... | The paper argues that 2D intermediate representations lose depth and temporal continuity, then proposes unified 3D-4D representations with trajectories and smooth spatial masks for online replanning and long-horizon exe... | you-wu; zixuan-chen; cunxu-ou | 2603.13788 |
| EA-MODEL-2026-4D-0009 | EA-MODEL | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-MODEL-2026-4D-0010 | EA-MODEL | `support` | `direct` | τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, then revise low-quality... | The paper describes a unified video-action world model with a video action model and an action-conditioned video simulator; at inference it samples candidates, ranks them, simulates futures, estimates progress, and rect... | pengfei-zhou; shengcong-chen; di-chen | 2606.01027 |
| EA-MODEL-2026-4D-0008 | EA-MODEL | `limit` | `direct` | GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences ov... | The introduction says photorealistic generated videos can have drifting contacts, inconsistent depth, and non-rigid deformation artifacts that break action extraction; pixel or latent losses do not guarantee corresponde... | kaichen-zhou; yuzhen-chen; fangneng-zhan | 2605.22882 |
| EA-MODEL-2026-4D-0005 | EA-MODEL | `gap` | `direct` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. | The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could furth... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-SENSOR-2026-4D-0015 | EA-SENSOR | `support` | `direct` | PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-receptacle states and pl... | The paper builds Perpetua* Bayesian persistence filters into a 3D scene graph, validates future state prediction in simulation and a three-week real-world semi-static lab setting, and shows navigation can avoid an expec... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-SENSOR-2026-4D-0019 | EA-SENSOR | `support` | `direct` | GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autor... | The paper decouples spatial geometry, temporal support, semantics, opacity, and motion in Gaussian primitives, then slices and splats them into future occupancy volumes at arbitrary timestamps and supervises both occupa... | cheng-chen; hao-huang; saurabh-bagchi | 2605.17682 |
| EA-SENSOR-2026-4D-0017 | EA-SENSOR | `support` | `direct` | DGSG-Mind combines dynamic 3D Gaussian mapping with scene graphs so that embodied agents can update object-level topology and reason over spatial-semantic relations in changing en... | The system fuses probabilistic voxels and 3D Gaussians, performs Gaussian-based camera relocalization and localized masked refinement for additions/removals, synchronizes graph nodes, and uses annotated Gaussian renderi... | luzhou-ge; xiangyu-zhu; jinyan-liu | 2605.29879 |
| EA-SENSOR-2026-4D-0016 | EA-SENSOR | `limit` | `direct` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. | The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and plannin... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-SENSOR-2026-4D-0018 | EA-SENSOR | `limit` | `direct` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. | The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs. (V Conclus... | luzhou-ge; xiangyu-zhu; jinyan-liu | 2605.29879 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-2026-4D-0007 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `conditional` | Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning r... |
| EA-DATA-2026-4D-0011 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executab... |
| EA-EVAL-2026-4D-0004 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `support` | Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D trac... |
| EA-EVAL-2026-4D-0006 | mutian-xu; tianbao-zhang; tianqi-liu | unlisted | `support` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while... |
| EA-EVAL-2026-4D-0013 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-EVAL-2026-4D-0002 | you-wu; zixuan-chen; cunxu-ou | unlisted | `conditional` | ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is... |
| EA-EVAL-2026-4D-0012 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `conditional` | τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensi... |
| EA-EVAL-2026-4D-0014 | arnav-kumar-jain; yilin-wu; jesse-farebrother | unlisted | `limit` | WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited pl... |
| EA-EVAL-2026-4D-0020 | yurui-dong; ziyue-wang; shuyun-lu | unlisted | `gap` | EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not on... |
| EA-MODEL-2026-4D-0003 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `support` | Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geom... |
| EA-MODEL-2026-4D-0001 | you-wu; zixuan-chen; cunxu-ou | unlisted | `support` | ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories... |
| EA-MODEL-2026-4D-0009 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-MODEL-2026-4D-0010 | pengfei-zhou; shengcong-chen; di-chen | unlisted | `support` | τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, the... |
| EA-MODEL-2026-4D-0008 | kaichen-zhou; yuzhen-chen; fangneng-zhan | unlisted | `limit` | GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3... |
| EA-MODEL-2026-4D-0005 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `gap` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. |
| EA-SENSOR-2026-4D-0015 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `support` | PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-rece... |
| EA-SENSOR-2026-4D-0019 | cheng-chen; hao-huang; saurabh-bagchi | unlisted | `support` | GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning with... |
| EA-SENSOR-2026-4D-0017 | luzhou-ge; xiangyu-zhu; jinyan-liu | unlisted | `support` | DGSG-Mind combines dynamic 3D Gaussian mapping with scene graphs so that embodied agents can update object-level topology and reason over spatial-semantic rela... |
| EA-SENSOR-2026-4D-0016 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `limit` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verifica... |
| EA-SENSOR-2026-4D-0018 | luzhou-ge; xiangyu-zhu; jinyan-liu | unlisted | `limit` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. |

## Synthesis Slots

### 共识/正向证据
- `EA-EVAL-2026-4D-0004`: Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only prediction, or dense depth prediction.
- `EA-EVAL-2026-4D-0006`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- `EA-EVAL-2026-4D-0013`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
- `EA-MODEL-2026-4D-0003`: Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geometry evolves over time.
- `EA-MODEL-2026-4D-0001`: ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories and 4D temporal context.
- `EA-MODEL-2026-4D-0009`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- `EA-MODEL-2026-4D-0010`: τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, then revise low-quality candidates before execution.
- `EA-SENSOR-2026-4D-0015`: PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-receptacle states and plan navigation accordingly.
### 条件成立
- `EA-DATA-2026-4D-0007`: Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial constraints and motion priors.
- `EA-DATA-2026-4D-0011`: τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding.
- `EA-EVAL-2026-4D-0002`: ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset, masking pipeline, and task setup.
- `EA-EVAL-2026-4D-0012`: τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensing, uncertainty estimation, longer horizons, and harder cont...
### 限制与失败模式
- `EA-EVAL-2026-4D-0014`: WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, data coverage, and noisy reward supervision...
- `EA-MODEL-2026-4D-0008`: GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences over time.
- `EA-SENSOR-2026-4D-0016`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- `EA-SENSOR-2026-4D-0018`: DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory.
### 开放问题
- `EA-EVAL-2026-4D-0020`: EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual scenes.
- `EA-MODEL-2026-4D-0005`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 10 / 5
- Recommended default: expert-explainer
- Core claims:
  - `EA-DATA-2026-4D-0007` Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for...
  - `EA-DATA-2026-4D-0011` τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed fo...
  - `EA-EVAL-2026-4D-0004` Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target th...
- Scientific memo preview: 《4D时空推理》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 4D时空推理 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 4D时空推理: 先看证据边界，再谈一个可传播的反常识洞察。

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
