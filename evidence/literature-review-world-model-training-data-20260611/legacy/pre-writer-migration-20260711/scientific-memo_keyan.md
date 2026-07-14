# 世界模型训练数据研究备忘录

## 研究边界与证据范围

- Topic: 世界模型训练数据
- Time range: 2025-12-11..2026-06-11
- Knowledge IDs: `EA-DATA`, `EA-MODEL`, `EA-EVAL`
- Paper-level sources: 14 / 5
- Output type: scientific-memo

## Evidence Core

- Accepted events: 14
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: [EA-DATA-2026-WMDATA-0001](evidence-appendix.md#ea-data-2026-wmdata-0001), [EA-DATA-2026-WMDATA-0003](evidence-appendix.md#ea-data-2026-wmdata-0003), [EA-DATA-2026-WMDATA-0014](evidence-appendix.md#ea-data-2026-wmdata-0014), [EA-DATA-2026-WMDATA-0002](evidence-appendix.md#ea-data-2026-wmdata-0002), [EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005), [EA-DATA-2026-WMDATA-0006](evidence-appendix.md#ea-data-2026-wmdata-0006), [EA-DATA-2026-WMDATA-0004](evidence-appendix.md#ea-data-2026-wmdata-0004), [EA-DATA-2026-WMDATA-0012](evidence-appendix.md#ea-data-2026-wmdata-0012), [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011), [EA-EVAL-2026-WMDATA-0013](evidence-appendix.md#ea-eval-2026-wmdata-0013), [EA-MODEL-2026-WMDATA-0008](evidence-appendix.md#ea-model-2026-wmdata-0008), [EA-MODEL-2026-WMDATA-0009](evidence-appendix.md#ea-model-2026-wmdata-0009)
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| [EA-DATA-2026-WMDATA-0001](evidence-appendix.md#ea-data-2026-wmdata-0001) | EA-DATA | `support` | `direct` | A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-c... | The paper builds an Interactive World Simulator from a moderate-sized robot interaction dataset, reports world-model-generated policy data comparable to the same amount of real-world data, and evaluates sim-real perform... | yixuan-wang | [2603.08546](https://arxiv.org/abs/2603.08546) |
| [EA-DATA-2026-WMDATA-0003](evidence-appendix.md#ea-data-2026-wmdata-0003) | EA-DATA | `support` | `direct` | World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. | Hi-WM rolls policies inside a world model, lets humans intervene when rollouts become incorrect or failure-prone, caches and branches failure states, and adds corrective trajectories back into the training set for post-... | yaxuan-li | [2604.21741](https://arxiv.org/abs/2604.21741) |
| [EA-DATA-2026-WMDATA-0014](evidence-appendix.md#ea-data-2026-wmdata-0014) | EA-DATA | `support` | `direct` | A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under intervention, with mo... | The survey distinguishes ordinary policy datasets from world-model datasets, reviews 34 manipulation datasets, and states that useful world-model data should include temporally aligned observations/actions, diversity fo... | wm-manipulation-survey-authors | [2606.00113](https://arxiv.org/abs/2606.00113) |
| [EA-DATA-2026-WMDATA-0002](evidence-appendix.md#ea-data-2026-wmdata-0002) | EA-DATA | `support` | `direct` | Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations, broad egocentric hu... | τ0-WM reports a 27.3K-hour corpus containing real-robot teleoperation, UMI-style interaction, egocentric human videos, and rollout/failure trajectories; the paper explains that these sources differ in action fidelity, e... | pengfei-zhou | [2606.01027](https://arxiv.org/abs/2606.01027) |
| [EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005) | EA-DATA | `conditional` | `direct` | Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation demonstrations, because off-the-shelf generative models can ha... | AnchorDream conditions video diffusion on robot motion renderings, starts from a small set of human teleoperation demonstrations, and frames embodiment grounding as necessary to avoid implausible motions while scaling d... | junjie-ye | [2512.11797](https://arxiv.org/abs/2512.11797) |
| [EA-DATA-2026-WMDATA-0006](evidence-appendix.md#ea-data-2026-wmdata-0006) | EA-DATA | `conditional` | `direct` | A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve re... | ComSim proposes a real-sim-real data augmentation pipeline: collect a small real trajectory set, align classical simulation to the real platform, transform simulation videos into real-world representations, and generate... | yiran-qin | [2604.11386](https://arxiv.org/abs/2604.11386) |
| [EA-DATA-2026-WMDATA-0004](evidence-appendix.md#ea-data-2026-wmdata-0004) | EA-DATA | `conditional` | `direct` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel object... | RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost... | junjie-ye | [2606.02577](https://arxiv.org/abs/2606.02577) |
| [EA-DATA-2026-WMDATA-0012](evidence-appendix.md#ea-data-2026-wmdata-0012) | EA-DATA | `conditional` | `direct` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and... | WMSD frames supervised fine-tuning on paired task-execution videos as costly, then proposes self-distillation and reinforcement learning where a VLM generates tasks/solutions from unlabeled scene images and feedback ver... | sebastian-stapf | [2606.12072](https://arxiv.org/abs/2606.12072) |
| [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011) | EA-DATA | `limit` | `direct` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. | World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy. (Abstract... | world-pilot-authors | [2606.12403](https://arxiv.org/abs/2606.12403) |
| [EA-EVAL-2026-WMDATA-0013](evidence-appendix.md#ea-eval-2026-wmdata-0013) | EA-EVAL | `limit` | `direct` | World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less acti... | SANTS reports that fully denoised video is not always the best action condition, trains a scheduler with a path-level reward after action generation, and explicitly optimizes downstream action quality rather than video... | sants-authors | [2605.27947](https://arxiv.org/abs/2605.27947) |
| [EA-MODEL-2026-WMDATA-0008](evidence-appendix.md#ea-model-2026-wmdata-0008) | EA-MODEL | `support` | `direct` | World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions. | GEM-4D injects dense 4D correspondence supervision from a geometry foundation model into a video generative backbone during training, arguing that correspondence consistency makes future rollouts more reliable for actio... | gem-4d-authors | [2605.22882](https://arxiv.org/abs/2605.22882) |
| [EA-MODEL-2026-WMDATA-0009](evidence-appendix.md#ea-model-2026-wmdata-0009) | EA-MODEL | `support` | `direct` | Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and... | GaussianDream trains current Gaussian reconstruction and future Gaussian prediction heads with RGB rendering, depth, and pseudo 3D scene-flow supervision, then retains only a compact prefix for control at inference. (Ab... | gaussiandream-authors | [2605.20752](https://arxiv.org/abs/2605.20752) |
| [EA-MODEL-2026-WMDATA-0007](evidence-appendix.md#ea-model-2026-wmdata-0007) | EA-MODEL | `support` | `direct` | Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remov... | SKIP argues that manipulation rollouts concentrate task-relevant information in sparse events, selects event-preserving keyframes through robot-aware multimodal fusion, and reports that generated videos can serve as pol... | ziheng-he | [2606.00664](https://arxiv.org/abs/2606.00664) |
| [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010) | EA-MODEL | `limit` | `direct` | World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to t... | The paper diagnoses a representation mismatch in WAMs, where action decoders attend to task-irrelevant areas despite plausible visual futures, and proposes an Action-Grounded Representation Alignment objective for the w... | yuying-ge | [2606.12217](https://arxiv.org/abs/2606.12217) |

## 主要综合

### 共识/正向证据
- [EA-DATA-2026-WMDATA-0001](evidence-appendix.md#ea-data-2026-wmdata-0001): A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horizon rollouts and sim-...
- [EA-DATA-2026-WMDATA-0003](evidence-appendix.md#ea-data-2026-wmdata-0003): World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations.
- [EA-DATA-2026-WMDATA-0014](evidence-appendix.md#ea-data-2026-wmdata-0014): A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under intervention, with modalities beyond RGB when physical intera...
- [EA-DATA-2026-WMDATA-0002](evidence-appendix.md#ea-data-2026-wmdata-0002): Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations, broad egocentric human videos, and rollout or failure traje...
- [EA-MODEL-2026-WMDATA-0008](evidence-appendix.md#ea-model-2026-wmdata-0008): World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions.
- [EA-MODEL-2026-WMDATA-0009](evidence-appendix.md#ea-model-2026-wmdata-0009): Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon future evolution rather t...
- [EA-MODEL-2026-WMDATA-0007](evidence-appendix.md#ea-model-2026-wmdata-0007): Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information downstream policies ne...
### 条件成立
- [EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005): Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation demonstrations, because off-the-shelf generative models can hallucinate robot bodies or implausible mo...
- [EA-DATA-2026-WMDATA-0006](evidence-appendix.md#ea-data-2026-wmdata-0006): A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency and broaden scenari...
- [EA-DATA-2026-WMDATA-0004](evidence-appendix.md#ea-data-2026-wmdata-0004): Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing...
- [EA-DATA-2026-WMDATA-0012](evidence-appendix.md#ea-data-2026-wmdata-0012): Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM feedback as weak ver...
### 限制与失败模式
- [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011): Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- [EA-EVAL-2026-WMDATA-0013](evidence-appendix.md#ea-eval-2026-wmdata-0013): World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physically unreliable.
- [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010): World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to task-relevant interaction regions.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## References

- `2512.11797` [AnchorDream: Repurposing Video Diffusion for Embodiment-Aware Robot Data Synthesis](https://arxiv.org/abs/2512.11797) (2025-12-12)
- `2603.08546` [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546) (2026-03-09)
- `2604.11386` [ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation](https://arxiv.org/abs/2604.11386) (2026-04-13)
- `2604.21741` [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](https://arxiv.org/abs/2604.21741) (2026-04-23)
- `2605.20752` [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](https://arxiv.org/abs/2605.20752) (2026-05-20)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.27947` [SANTS: A State-Adaptive Scheduler for World Action Models](https://arxiv.org/abs/2605.27947) (2026-05-27)
- `2606.00113` [World Models for Robotic Manipulation: A Survey](https://arxiv.org/abs/2606.00113) (2026-05-27)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [τ0-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.02577` [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](https://arxiv.org/abs/2606.02577) (2026-06-01)
- `2606.12072` [World Model Self-Distillation: Training World Models to Solve General Tasks](https://arxiv.org/abs/2606.12072) (2026-06-10)
- `2606.12217` [Making Foresight Actionable: Repurposing Representation Alignment in World Action Models](https://arxiv.org/abs/2606.12217) (2026-06-10)
- `2606.12403` [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403) (2026-06-10)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。

## 研究启发与开放问题

- Treat support, conditional, limit, and gap events as separate signals before writing topic-card updates.
- Mark cross-event synthesis as `inference` unless a claim is directly backed by an event/source ID.
- Use topic-card update suggestions only after checking source gaps.
