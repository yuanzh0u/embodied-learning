# Review Packet: 4D时空推理对数据的需求

## Scope

- Topic: 4D时空推理对数据的需求
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-EVAL`, `EA-MODEL`, `EA-SENSOR`
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
- Trace IDs: `EA-4DDATA-READ-0014`, `EA-4DDATA-READ-0005`, `EA-4DDATA-READ-0015`, `EA-4DDATA-READ-0013`, `EA-4DDATA-READ-0004`, `EA-4DDATA-READ-0010`, `EA-4DDATA-READ-0003`, `EA-4DDATA-READ-0009`, `EA-4DDATA-READ-0002`, `EA-4DDATA-READ-0007`, `EA-4DDATA-READ-0008`, `EA-4DDATA-READ-0011`
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
| `support` | 支持 | 7 |
| `conditional` | 条件成立 | 4 |
| `limit` | 限制/负面 | 2 |
| `gap` | 缺口 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.09878: MVISTA-4D: View-Consistent 4D World Model with Test-Time Action Inference for Robotic Manipulation | 2026-02-10 | support | EA-4DDATA-READ-0014 |
| 2603.01549: Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation | 2026-03-02 | gap | EA-4DDATA-READ-0001 |
| 2603.08485: 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos | 2026-03-09 | conditional | EA-4DDATA-READ-0009 |
| 2603.16669: Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation | 2026-03-17 | support | EA-4DDATA-READ-0005 |
| 2603.17189: Influence of Gripper Design on Human Demonstration Quality for Robot Learning | 2026-03-17 | gap | EA-4DDATA-READ-0006 |
| 2605.00121: Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes | 2026-04-30 | limit | EA-4DDATA-READ-0011 |
| 2605.01799: Embody4D: A Generalist Data Engine for Embodied 4D World Modeling | 2026-05-03 | support | EA-4DDATA-READ-0015 |
| 2605.17682: GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning | 2026-05-17 | support | EA-4DDATA-READ-0013 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | support | EA-4DDATA-READ-0004 |
| 2605.29879: DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding | 2026-05-28 | limit | EA-4DDATA-READ-0012 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional | EA-4DDATA-READ-0002 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional | EA-4DDATA-READ-0007 |
| 2606.08737: Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation | 2026-06-07 | support | EA-4DDATA-READ-0010 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional | EA-4DDATA-READ-0008 |
| 2606.13672: $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation | 2026-06-11 | support | EA-4DDATA-READ-0003 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-4DDATA-READ-0014 | EA-DATA | `support` | `direct` | MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD observation and fuses the generated views into a more complet... | The abstract describes single-view RGBD input, arbitrary-view RGBD generation, and back-projection/fusion as the route to complete time-varying 3D structure. (Abstract (full-text section)) | jiaxu-wang; yicheng-jiang; tianlun-he; et al. | 2602.09878 |
| EA-4DDATA-READ-0005 | EA-DATA | `support` | `direct` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... | The method disentangles precise robot control from generative environmental reaction by driving a URDF robot through kinematics, projecting a 4D robot pointmap sequence, and jointly generating synchronized RGB/pointmap... | mutian-xu; tianbao-zhang; tianqi-liu; et al. | 2603.16669 |
| EA-4DDATA-READ-0015 | EA-DATA | `support` | `direct` | Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data. | The abstract ties fixed or sparse viewpoints to partial observations and introduces both novel-view video generation and a compositional synthesis pipeline to address data scarcity. (Abstract (full-text section)) | peiyan-tu; hanxin-zhu; jingwen-sun; et al. | 2605.01799 |
| EA-4DDATA-READ-0013 | EA-DATA | `support` | `direct` | GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autor... | The paper decouples spatial geometry, temporal support, semantics, opacity, and motion in Gaussian primitives, then slices and splats them into future occupancy volumes at arbitrary timestamps and supervises both occupa... | cheng-chen; hao-huang; saurabh-bagchi | 2605.17682 |
| EA-4DDATA-READ-0004 | EA-DATA | `support` | `direct` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. | The model distills 4D geometry foundation-model representations into a video backbone during training, discards the geometry branch at inference, and uses an inverse dynamics module to convert generated rollouts into ex... | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | 2605.22882 |
| EA-4DDATA-READ-0010 | EA-DATA | `support` | `direct` | Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 | 问题建模段先定义动作与视觉未来的联合分布，再明确把未来触觉纳入联合预测目标。 (3.1. Problem Formulation) | yunfan-lou; yifan-ye; yankai-fu; et al. | 2606.08737 |
| EA-4DDATA-READ-0003 | EA-DATA | `support` | `direct` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... | The paper argues that manipulation world models must satisfy fidelity, consistency, and efficiency together, then designs a multi-view latent world model with reward/value prediction to support policy evaluation, synthe... | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | 2606.13672 |
| EA-4DDATA-READ-0009 | EA-DATA | `conditional` | `direct` | 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 | 结果段对比了删除整条不可见轨迹的基线与仅屏蔽不可见 point-timestep 损失的 3PoinTr。 (4.3 Results: 3D Point Track Prediction) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | 2603.08485 |
| EA-4DDATA-READ-0002 | EA-DATA | `conditional` | `direct` | τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 | 摘要直接列出四类交互数据和 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-4DDATA-READ-0007 | EA-DATA | `conditional` | `direct` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 | 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。 (3.2 Synchronization and Data Quality Control) | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-4DDATA-READ-0008 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-4DDATA-READ-0011 | EA-DATA | `limit` | `direct` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. | The limitations section says object-receptacle edges are modeled independently, indistinguishable objects are treated as interchangeable, and LLM hallucinations remain a risk for open-vocabulary verification and plannin... | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | 2605.00121 |
| EA-4DDATA-READ-0012 | EA-DATA | `limit` | `direct` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. | The conclusion states that the system relies on SLAM pose accuracy for initial reconstruction and ACE training, and that scaling to large outdoor scenes is limited by 3D Gaussian storage and GPU memory costs. (V Conclus... | luzhou-ge; xiangyu-zhu; jinyan-liu; et al. | 2605.29879 |
| EA-4DDATA-READ-0001 | EA-DATA | `gap` | `direct` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. | The conclusion says Pri4R was evaluated mainly as fine-tuning on demonstrations and small real-world rollouts, and suggests that pretraining-scale 3D point-track supervision or explicit test-time computation could furth... | jisoo-kim; jungbin-cho; sanghyeok-chu; et al. | 2603.01549 |
| EA-4DDATA-READ-0006 | EA-DATA | `gap` | `direct` | UMI 夹爪手指的力分布会显著改变操作者的任务表现和示教质量，说明数据采集硬件本身是学习管线需要优化的一部分。 | 讨论段报告集中载荷夹爪优于分布载荷夹爪，并将小幅硬件改动与示教质量及后续策略学习联系起来。 (V DISCUSSION) | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | 2603.17189 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-4DDATA-READ-0014 | jiaxu-wang; yicheng-jiang; tianlun-he; et al. | unlisted | `support` | MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD observation and fuses the generated views... |
| EA-4DDATA-READ-0005 | mutian-xu; tianbao-zhang; tianqi-liu; et al. | unlisted | `support` | Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while... |
| EA-4DDATA-READ-0015 | peiyan-tu; hanxin-zhu; jingwen-sun; et al. | unlisted | `support` | Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeli... |
| EA-4DDATA-READ-0013 | cheng-chen; hao-huang; saurabh-bagchi | unlisted | `support` | GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning with... |
| EA-4DDATA-READ-0004 | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | unlisted | `support` | GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. |
| EA-4DDATA-READ-0010 | yunfan-lou; yifan-ye; yankai-fu; et al. | unlisted | `support` | Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 |
| EA-4DDATA-READ-0003 | arnav-kumar-jain; yilin-wu; jesse-farebrother; et al. | unlisted | `support` | WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency... |
| EA-4DDATA-READ-0009 | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | unlisted | `conditional` | 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 |
| EA-4DDATA-READ-0002 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `conditional` | τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 |
| EA-4DDATA-READ-0007 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `conditional` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 |
| EA-4DDATA-READ-0008 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-4DDATA-READ-0011 | miguel-saavedra-ruiz; charlie-gauthier; kumaraditya-gupta | unlisted | `limit` | PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verifica... |
| EA-4DDATA-READ-0012 | luzhou-ge; xiangyu-zhu; jinyan-liu; et al. | unlisted | `limit` | DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. |
| EA-4DDATA-READ-0001 | jisoo-kim; jungbin-cho; sanghyeok-chu; et al. | unlisted | `gap` | Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. |
| EA-4DDATA-READ-0006 | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | unlisted | `gap` | UMI 夹爪手指的力分布会显著改变操作者的任务表现和示教质量，说明数据采集硬件本身是学习管线需要优化的一部分。 |

## Synthesis Slots

### 共识/正向证据
- `EA-4DDATA-READ-0014`: MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD observation and fuses the generated views into a more complete 3D structure over time.
- `EA-4DDATA-READ-0005`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment reactions.
- `EA-4DDATA-READ-0015`: Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data.
- `EA-4DDATA-READ-0013`: GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autoregressive rollout.
- `EA-4DDATA-READ-0004`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost.
- `EA-4DDATA-READ-0010`: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。
- `EA-4DDATA-READ-0003`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planning.
### 条件成立
- `EA-4DDATA-READ-0009`: 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。
- `EA-4DDATA-READ-0002`: τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。
- `EA-4DDATA-READ-0007`: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- `EA-4DDATA-READ-0008`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
### 限制与失败模式
- `EA-4DDATA-READ-0011`: PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning.
- `EA-4DDATA-READ-0012`: DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory.
### 开放问题
- `EA-4DDATA-READ-0001`: Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs.
- `EA-4DDATA-READ-0006`: UMI 夹爪手指的力分布会显著改变操作者的任务表现和示教质量，说明数据采集硬件本身是学习管线需要优化的一部分。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-4DDATA-READ-0014` MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD observation and fuses the gener...
  - `EA-4DDATA-READ-0005` Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectori...
  - `EA-4DDATA-READ-0015` Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthe...
- Scientific memo preview: 《4D时空推理对数据的需求》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 4D时空推理对数据的需求 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 4D时空推理对数据的需求: 先看证据边界，再谈一个可传播的反常识洞察。

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
