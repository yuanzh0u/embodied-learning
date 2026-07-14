# Review Packet: 世界模型需要什么样的训练数据

## Scope

- Topic: 世界模型需要什么样的训练数据
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-MODEL`, `EA-EVAL`
- Evidence events: 15
- Topic cards: 0
- Registered source IDs available: not loaded

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 15
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-WMDATA-READ-0007`, `EA-WMDATA-READ-0012`, `EA-WMDATA-READ-0009`, `EA-WMDATA-READ-0002`, `EA-WMDATA-READ-0008`, `EA-WMDATA-READ-0003`, `EA-WMDATA-READ-0001`, `EA-WMDATA-READ-0015`, `EA-WMDATA-READ-0011`, `EA-WMDATA-READ-0005`, `EA-WMDATA-READ-0004`, `EA-WMDATA-READ-0013`
- Registered sources: not loaded

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 15
- Structure mapped: 15
- Deep-read papers: 15
- Claim-verified papers: 15
- Accepted evidence papers: 15
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- No topic cards provided.

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 8 |
| `conditional` | 条件成立 | 3 |
| `limit` | 限制/负面 | 3 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.15549: VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing | 2026-02-17 | conditional | EA-WMDATA-READ-0011 |
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | gap | EA-WMDATA-READ-0010 |
| 2603.08546: Interactive World Simulator for Robot Policy Training and Evaluation | 2026-03-09 | support | EA-WMDATA-READ-0007 |
| 2603.16669: Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation | 2026-03-17 | support | EA-WMDATA-READ-0012 |
| 2604.11386: ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation | 2026-04-13 | conditional | EA-WMDATA-READ-0005 |
| 2604.21741: Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training | 2026-04-23 | support | EA-WMDATA-READ-0009 |
| 2605.00121: Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes | 2026-04-30 | limit | EA-WMDATA-READ-0013 |
| 2605.20752: GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation | 2026-05-20 | support | EA-WMDATA-READ-0008 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | support | EA-WMDATA-READ-0002 |
| 2605.27947: SANTS: A State-Adaptive Scheduler for World Action Models | 2026-05-27 | limit | EA-WMDATA-READ-0006 |
| 2605.29879: DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding | 2026-05-28 | limit | EA-WMDATA-READ-0014 |
| 2606.00664: SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models | 2026-05-30 | support | EA-WMDATA-READ-0003 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | support | EA-WMDATA-READ-0001 |
| 2606.02577: RoboDream: Compositional World Models for Scalable Robot Data Synthesis | 2026-06-01 | conditional | EA-WMDATA-READ-0004 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | support | EA-WMDATA-READ-0015 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-WMDATA-READ-0007 | EA-DATA | `support` | `direct` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-c... | The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real perform... | yixuan-wang; rhythm-syed; fangyu-wu; et al. | 2603.08546 |
| EA-WMDATA-READ-0012 | EA-DATA | `support` | `direct` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... | The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap... | mutian-xu; tianbao-zhang; tianqi-liu; et al. | 2603.16669 |
| EA-WMDATA-READ-0009 | EA-DATA | `support` | `direct` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. | Hi-WM rolls policies inside a world model, lets humans intervene when rollouts become incorrect or failure-prone, caches and branches failure states, and adds corrective trajectories back into the training set for post-... | yaxuan-li; zhongyi-zhou; yefei-chen; et al. | 2604.21741 |
| EA-WMDATA-READ-0002 | EA-DATA | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | 2605.22882 |
| EA-WMDATA-READ-0008 | EA-DATA | `support` | `direct` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and... | GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference. (3.... | zijian-zhang; yuqing-jiang; qian-cheng; et al. | 2605.20752 |
| EA-WMDATA-READ-0003 | EA-DATA | `support` | `direct` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remov... | SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as pol... | ziheng-he; yixiang-chen; ning-yang; et al. | 2606.00664 |
| EA-WMDATA-READ-0001 | EA-DATA | `support` | `direct` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 | 摘要直接报告了异构数据组成与 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-WMDATA-READ-0015 | EA-DATA | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | 2606.13672 |
| EA-WMDATA-READ-0011 | EA-DATA | `conditional` | `direct` | For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking d... | VLM-DEWM validates each VLM decision against a persistent world model and uses discrepancy analysis for targeted recovery, with reported gains in state tracking and recovery success in long-horizon manufacturing tasks.... | guoqin-tang; qingxuan-jia; gang-chen; et al. | 2602.15549 |
| EA-WMDATA-READ-0005 | EA-DATA | `conditional` | `direct` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve re... | ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate... | yiran-qin; jiahua-ma; li-kang; et al. | 2604.11386 |
| EA-WMDATA-READ-0004 | EA-DATA | `conditional` | `direct` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel object... | RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost... | junjie-ye; rong-xue; basile-van-hoorick; et al. | 2606.02577 |
| EA-WMDATA-READ-0013 | EA-DATA | `limit` | `direct` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. | The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and plannin... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-WMDATA-READ-0006 | EA-DATA | `limit` | `direct` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less acti... | SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video... | sants-authors | 2605.27947 |
| EA-WMDATA-READ-0014 | EA-DATA | `limit` | `direct` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. | The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs. (V Conclus... | luzhou-ge; xiangyu-zhu; jinyan-liu | 2605.29879 |
| EA-WMDATA-READ-0010 | EA-DATA | `gap` | `direct` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. | The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could furth... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-WMDATA-READ-0007 | yixuan-wang; rhythm-syed; fangyu-wu; et al. | unlisted | `support` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depe... |
| EA-WMDATA-READ-0012 | mutian-xu; tianbao-zhang; tianqi-liu; et al. | unlisted | `support` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while... |
| EA-WMDATA-READ-0009 | yaxuan-li; zhongyi-zhou; yefei-chen; et al. | unlisted | `support` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. |
| EA-WMDATA-READ-0002 | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-WMDATA-READ-0008 | zijian-zhang; yuqing-jiang; qian-cheng; et al. | unlisted | `support` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent curr... |
| EA-WMDATA-READ-0003 | ziheng-he; yixiang-chen; ning-yang; et al. | unlisted | `support` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic fram... |
| EA-WMDATA-READ-0001 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `support` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 |
| EA-WMDATA-READ-0015 | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-WMDATA-READ-0011 | guoqin-tang; qingxuan-jia; gang-chen; et al. | unlisted | `conditional` | For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reas... |
| EA-WMDATA-READ-0005 | yiran-qin; jiahua-ma; li-kang; et al. | unlisted | `conditional` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pa... |
| EA-WMDATA-READ-0004 | junjie-ye; rong-xue; basile-van-hoorick; et al. | unlisted | `conditional` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrat... |
| EA-WMDATA-READ-0013 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `limit` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verifica... |
| EA-WMDATA-READ-0006 | sants-authors | unlisted | `limit` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising... |
| EA-WMDATA-READ-0014 | luzhou-ge; xiangyu-zhu; jinyan-liu | unlisted | `limit` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. |
| EA-WMDATA-READ-0010 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `gap` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. |

## Synthesis Slots

### 共识/正向证据
- `EA-WMDATA-READ-0007`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-...
- `EA-WMDATA-READ-0012`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- `EA-WMDATA-READ-0009`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations.
- `EA-WMDATA-READ-0002`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- `EA-WMDATA-READ-0008`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon future evolution rather t...
- `EA-WMDATA-READ-0003`: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information downstream policies ne...
- `EA-WMDATA-READ-0001`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- `EA-WMDATA-READ-0015`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
### 条件成立
- `EA-WMDATA-READ-0011`: For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before execution.
- `EA-WMDATA-READ-0005`: A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenari...
- `EA-WMDATA-READ-0004`: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing...
### 限制与失败模式
- `EA-WMDATA-READ-0013`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- `EA-WMDATA-READ-0006`: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- `EA-WMDATA-READ-0014`: DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory.
### 开放问题
- `EA-WMDATA-READ-0010`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-WMDATA-READ-0007` A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its...
  - `EA-WMDATA-READ-0012` Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectori...
  - `EA-WMDATA-READ-0009` World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrati...
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
