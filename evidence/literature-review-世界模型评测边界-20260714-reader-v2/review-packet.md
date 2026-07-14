# Review Packet: 世界模型评测边界

## Scope

- Topic: 世界模型评测边界
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-EVAL`, `EA-MODEL`
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
- Trace IDs: `EA-WMEVAL-READ-0007`, `EA-WMEVAL-READ-0005`, `EA-WMEVAL-READ-0003`, `EA-WMEVAL-READ-0001`, `EA-WMEVAL-READ-0010`, `EA-WMEVAL-READ-0002`, `EA-WMEVAL-READ-0014`, `EA-WMEVAL-READ-0011`, `EA-WMEVAL-READ-0012`, `EA-WMEVAL-READ-0008`, `EA-WMEVAL-READ-0015`, `EA-WMEVAL-READ-0009`
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
| `support` | 支持 | 5 |
| `conditional` | 条件成立 | 4 |
| `limit` | 限制/负面 | 4 |
| `gap` | 缺口 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.15549: VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing | 2026-02-17 | conditional | EA-WMEVAL-READ-0002 |
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | gap | EA-WMEVAL-READ-0006 |
| 2603.16669: Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation | 2026-03-17 | support | EA-WMEVAL-READ-0007 |
| 2604.11386: ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation | 2026-04-13 | conditional | EA-WMEVAL-READ-0014 |
| 2605.00121: Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes | 2026-04-30 | limit | EA-WMEVAL-READ-0008 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | support | EA-WMEVAL-READ-0005 |
| 2605.27947: SANTS: A State-Adaptive Scheduler for World Action Models | 2026-05-27 | limit | EA-WMEVAL-READ-0015 |
| 2605.29360: MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models | 2026-05-28 | gap | EA-WMEVAL-READ-0004 |
| 2605.29879: DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding | 2026-05-28 | limit | EA-WMEVAL-READ-0009 |
| 2606.00664: SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models | 2026-05-30 | support | EA-WMEVAL-READ-0003 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | support | EA-WMEVAL-READ-0001 |
| 2606.02577: RoboDream: Compositional World Models for Scalable Robot Data Synthesis | 2026-06-01 | conditional | EA-WMEVAL-READ-0011 |
| 2606.12072: World Model Self-Distillation: Training World Models to Solve General Tasks | 2026-06-10 | conditional | EA-WMEVAL-READ-0012 |
| 2606.12403: World Pilot: Steering Vision-Language-Action Models with World-Action Priors | 2026-06-10 | limit | EA-WMEVAL-READ-0013 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | support | EA-WMEVAL-READ-0010 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-WMEVAL-READ-0007 | EA-EVAL | `support` | `direct` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... | The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap... | mutian-xu; tianbao-zhang; tianqi-liu; et al. | 2603.16669 |
| EA-WMEVAL-READ-0005 | EA-EVAL | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | 2605.22882 |
| EA-WMEVAL-READ-0003 | EA-EVAL | `support` | `direct` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remov... | SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as pol... | ziheng-he; yixiang-chen; ning-yang; et al. | 2606.00664 |
| EA-WMEVAL-READ-0001 | EA-EVAL | `support` | `direct` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 | 摘要直接报告了异构数据组成与 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-WMEVAL-READ-0010 | EA-EVAL | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | 2606.13672 |
| EA-WMEVAL-READ-0002 | EA-EVAL | `conditional` | `direct` | For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking d... | VLM-DEWM validates each VLM decision against a persistent world model and uses discrepancy analysis for targeted recovery, with reported gains in state tracking and recovery success in long-horizon manufacturing tasks.... | guoqin-tang; qingxuan-jia; gang-chen; et al. | 2602.15549 |
| EA-WMEVAL-READ-0014 | EA-EVAL | `conditional` | `direct` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve re... | ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate... | yiran-qin; jiahua-ma; li-kang; et al. | 2604.11386 |
| EA-WMEVAL-READ-0011 | EA-EVAL | `conditional` | `direct` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel object... | RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost... | junjie-ye; rong-xue; basile-van-hoorick; et al. | 2606.02577 |
| EA-WMEVAL-READ-0012 | EA-EVAL | `conditional` | `direct` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and... | WMSD frames supervised fine-tuning on paired task-execution videos as costly, then proposes self-distillation and reinforcement learning where a VLM generates tasks/solutions from unlabeled scene images and feedback ver... | sebastian-stapf; pablo-acuaviva-huertos; aram-davtyan; et al. | 2606.12072 |
| EA-WMEVAL-READ-0008 | EA-EVAL | `limit` | `direct` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. | The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and plannin... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-WMEVAL-READ-0015 | EA-EVAL | `limit` | `direct` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less acti... | SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video... | sants-authors | 2605.27947 |
| EA-WMEVAL-READ-0009 | EA-EVAL | `limit` | `direct` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. | The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs. (V Conclus... | luzhou-ge; xiangyu-zhu; jinyan-liu | 2605.29879 |
| EA-WMEVAL-READ-0013 | EA-EVAL | `limit` | `direct` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. | World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy. (Abstract... | zefu-lin; rongxu-cui; junjia-xu; et al. | 2606.12403 |
| EA-WMEVAL-READ-0006 | EA-EVAL | `gap` | `direct` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. | The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could furth... | jisoo-kim; jungbin-cho; sanghyeok-chu | 2603.01549 |
| EA-WMEVAL-READ-0004 | EA-EVAL | `gap` | `direct` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias... | The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias. (Abstract... | tianzhuo-yang; zihan-shen; zirui-mi; et al. | 2605.29360 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-WMEVAL-READ-0007 | mutian-xu; tianbao-zhang; tianqi-liu; et al. | unlisted | `support` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while... |
| EA-WMEVAL-READ-0005 | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-WMEVAL-READ-0003 | ziheng-he; yixiang-chen; ning-yang; et al. | unlisted | `support` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic fram... |
| EA-WMEVAL-READ-0001 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `support` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 |
| EA-WMEVAL-READ-0010 | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-WMEVAL-READ-0002 | guoqin-tang; qingxuan-jia; gang-chen; et al. | unlisted | `conditional` | For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reas... |
| EA-WMEVAL-READ-0014 | yiran-qin; jiahua-ma; li-kang; et al. | unlisted | `conditional` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pa... |
| EA-WMEVAL-READ-0011 | junjie-ye; rong-xue; basile-van-hoorick; et al. | unlisted | `conditional` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrat... |
| EA-WMEVAL-READ-0012 | sebastian-stapf; pablo-acuaviva-huertos; aram-davtyan; et al. | unlisted | `conditional` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM... |
| EA-WMEVAL-READ-0008 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `limit` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verifica... |
| EA-WMEVAL-READ-0015 | sants-authors | unlisted | `limit` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising... |
| EA-WMEVAL-READ-0009 | luzhou-ge; xiangyu-zhu; jinyan-liu | unlisted | `limit` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. |
| EA-WMEVAL-READ-0013 | zefu-lin; rongxu-cui; junjia-xu; et al. | unlisted | `limit` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution... |
| EA-WMEVAL-READ-0006 | jisoo-kim; jungbin-cho; sanghyeok-chu | unlisted | `gap` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. |
| EA-WMEVAL-READ-0004 | tianzhuo-yang; zihan-shen; zirui-mi; et al. | unlisted | `gap` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelit... |

## Synthesis Slots

### 共识/正向证据
- `EA-WMEVAL-READ-0007`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- `EA-WMEVAL-READ-0005`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- `EA-WMEVAL-READ-0003`: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information downstream policies ne...
- `EA-WMEVAL-READ-0001`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- `EA-WMEVAL-READ-0010`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
### 条件成立
- `EA-WMEVAL-READ-0002`: For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before execution.
- `EA-WMEVAL-READ-0014`: A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenari...
- `EA-WMEVAL-READ-0011`: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing...
- `EA-WMEVAL-READ-0012`: Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM feedback as weak ver...
### 限制与失败模式
- `EA-WMEVAL-READ-0008`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- `EA-WMEVAL-READ-0015`: World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- `EA-WMEVAL-READ-0009`: DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory.
- `EA-WMEVAL-READ-0013`: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
### 开放问题
- `EA-WMEVAL-READ-0006`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- `EA-WMEVAL-READ-0004`: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-WMEVAL-READ-0007` Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectori...
  - `EA-WMEVAL-READ-0005` GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-tim...
  - `EA-WMEVAL-READ-0003` Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; ge...
- Scientific memo preview: 《世界模型评测边界》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 世界模型评测边界 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 世界模型评测边界: 先看证据边界，再谈一个可传播的反常识洞察。

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
