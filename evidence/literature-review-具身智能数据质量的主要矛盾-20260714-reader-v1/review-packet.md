# Review Packet: 具身智能数据质量的主要矛盾

## Scope

- Topic: 具身智能数据质量的主要矛盾
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-XEMBODIMENT`, `EA-MODEL`, `EA-EVAL`
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
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-READ-0008`, `EA-DATA-READ-0003`, `EA-DATA-READ-0007`, `EA-DATA-READ-0004`, `EA-DATA-READ-0005`, `EA-DATA-READ-0006`, `EA-DATA-READ-0013`, `EA-DATA-READ-0014`, `EA-DATA-READ-0009`, `EA-DATA-READ-0010`, `EA-DATA-READ-0015`, `EA-DATA-READ-0012`
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
| `support` | 支持 | 6 |
| `conditional` | 条件成立 | 6 |
| `limit` | 限制/负面 | 3 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.10618: From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation... | 2026-02-11 | conditional | EA-DATA-READ-0013 |
| 2602.13197: Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos | 2026-02-13 | conditional | EA-DATA-READ-0014 |
| 2603.17189: Influence of Gripper Design on Human Demonstration Quality for Robot Learning | 2026-03-17 | support | EA-DATA-READ-0008 |
| 2605.22882: GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | 2026-05-20 | support | EA-DATA-READ-0003 |
| 2606.01027: τ0-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | support | EA-DATA-READ-0007 |
| 2606.02577: RoboDream: Compositional World Models for Scalable Robot Data Synthesis | 2026-06-01 | conditional | EA-DATA-READ-0009 |
| 2606.12072: World Model Self-Distillation: Training World Models to Solve General Tasks | 2026-06-10 | conditional | EA-DATA-READ-0010 |
| 2606.12403: World Pilot: Steering Vision-Language-Action Models with World-Action Priors | 2026-06-10 | limit | EA-DATA-READ-0011 |
| 2606.28320: WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation | 2026-06-26 | conditional | EA-DATA-READ-0015 |
| 2607.02642: GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | support | EA-DATA-READ-0004 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-DATA-READ-0001 |
| 2607.05390: Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | support | EA-DATA-READ-0005 |
| 2607.06442: SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | limit | EA-DATA-READ-0002 |
| 2607.06558: RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | conditional | EA-DATA-READ-0012 |
| 2607.06564: Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | support | EA-DATA-READ-0006 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-READ-0008 | EA-DATA | `support` | `direct` | 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 | 论文指出 UMI 示教虽快于遥操作但仍比手工慢、工具重量会造成疲劳并影响 demonstration；实验中改变 UMI gripper fingers 的力分布显著影响打开绷带包装表现，concentrated load grippers 优于 distributed load grippers，作者将其连接到 demonstration quality 和 learned robot control policies。 (V DI... | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | 2603.17189 |
| EA-DATA-READ-0003 | EA-DATA | `support` | `direct` | World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions. | GEM-4D injects dense 4D correspondence supervision from a geometry foundation model into a video generative backbone during training, arguing that correspondence consistency makes future rollouts more reliable for actio... | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | 2605.22882 |
| EA-DATA-READ-0007 | EA-DATA | `support` | `direct` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 | 摘要直接报告了异构数据组成与 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-DATA-READ-0004 | EA-DATA | `support` | `direct` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-trai... | gigaworld-team; angyuan-ma; boyuan-wang; et al. | 2607.02642 |
| EA-DATA-READ-0005 | EA-DATA | `support` | `direct` | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | 论文认为形变物体有高维状态和复杂材料属性，接触诱发的局部形变常被末端执行器或物体遮挡；已有数据集常缺对象多样性、依赖合成数据，或缺高保真标注与接触形变。Deform360 采集 198 个日常物体、1,980 个交互序列、215 小时以上数据、41 个环视相机和双臂触觉 UMI gripper，并用 markerless 3D tracking 提取稠密几何与运动。 (Abstract (full-text section)) | hongyu-li; wanjia-fu; xiaoyan-cong; et al. | 2607.05390 |
| EA-DATA-READ-0006 | EA-DATA | `support` | `direct` | Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 | 引言将操作需求归结为显式 3D 结构与时间一致性，并说明纯 2D 管线及有损的跨模态变换会削弱这些约束。 (I Introduction) | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | 2607.06564 |
| EA-DATA-READ-0013 | EA-DATA | `conditional` | `direct` | VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 | 论文指出 VR 用于记录机器人学习示教时，visual fidelity 可能不如 user behavior 的 quality/reliability 重要；输入设备与可视化会影响工作负荷、运动效率、不必要动作和执行精度。实验发现 controller 与 motion-capture gloves 在 pick-and-place 与 manner-oriented tasks 上呈现不同轨迹策略和权衡。 (1 Introduc... | robin-beierling; manuel-scheibl; jonas-dech; et al. | 2602.10618 |
| EA-DATA-READ-0014 | EA-DATA | `conditional` | `direct` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 | PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。 (3.3 Trajectory and Gr... | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | 2602.13197 |
| EA-DATA-READ-0009 | EA-DATA | `conditional` | `direct` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel object... | RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost... | junjie-ye; rong-xue; basile-van-hoorick; et al. | 2606.02577 |
| EA-DATA-READ-0010 | EA-DATA | `conditional` | `direct` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and... | WMSD frames supervised fine-tuning on paired task-execution videos as costly, then proposes self-distillation and reinforcement learning where a VLM generates tasks/solutions from unlabeled scene images and feedback ver... | sebastian-stapf; pablo-acuaviva-huertos; aram-davtyan; et al. | 2606.12072 |
| EA-DATA-READ-0015 | EA-DATA | `conditional` | `direct` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 | 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action... | justin-yu; andrew-goldberg; kavish-kondap; et al. | 2606.28320 |
| EA-DATA-READ-0012 | EA-DATA | `conditional` | `direct` | RynnWorld-Teleop将数字遥操作作为生成式数据引擎，但论文明确限定了它对精细流体动力学、高形变物体和跨机器人平台扩展的能力。 | 结论的限制段指出，模型在精细流体和高形变操作上仍会失败，而当前跨本体迁移仍要求每个平台单独微调。 (6 Conclusion) | haoyu-zhao; xingyue-zhao; hangyu-li; et al. | 2607.06558 |
| EA-DATA-READ-0011 | EA-DATA | `limit` | `direct` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. | World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy. (Abstract... | zefu-lin; rongxu-cui; junjia-xu; et al. | 2606.12403 |
| EA-DATA-READ-0001 | EA-DATA | `limit` | `direct` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 | 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。 (5 Conclusion and Limitations) | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |
| EA-DATA-READ-0002 | EA-DATA | `limit` | `direct` | SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 | 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。 (Introduction) | changti-wu; bin-yu; zhaolong-shen; et al. | 2607.06442 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-READ-0008 | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | unlisted | `support` | 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 |
| EA-DATA-READ-0003 | kaichen-zhou; yuzhen-chen; fangneng-zhan; et al. | unlisted | `support` | World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable r... |
| EA-DATA-READ-0007 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `support` | τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 |
| EA-DATA-READ-0004 | gigaworld-team; angyuan-ma; boyuan-wang; et al. | unlisted | `support` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 |
| EA-DATA-READ-0005 | hongyu-li; wanjia-fu; xiaoyan-cong; et al. | unlisted | `support` | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 |
| EA-DATA-READ-0006 | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | unlisted | `support` | Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 |
| EA-DATA-READ-0013 | robin-beierling; manuel-scheibl; jonas-dech; et al. | unlisted | `conditional` | VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 |
| EA-DATA-READ-0014 | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | unlisted | `conditional` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 |
| EA-DATA-READ-0009 | junjie-ye; rong-xue; basile-van-hoorick; et al. | unlisted | `conditional` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrat... |
| EA-DATA-READ-0010 | sebastian-stapf; pablo-acuaviva-huertos; aram-davtyan; et al. | unlisted | `conditional` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM... |
| EA-DATA-READ-0015 | justin-yu; andrew-goldberg; kavish-kondap; et al. | unlisted | `conditional` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 |
| EA-DATA-READ-0012 | haoyu-zhao; xingyue-zhao; hangyu-li; et al. | unlisted | `conditional` | RynnWorld-Teleop将数字遥操作作为生成式数据引擎，但论文明确限定了它对精细流体动力学、高形变物体和跨机器人平台扩展的能力。 |
| EA-DATA-READ-0011 | zefu-lin; rongxu-cui; junjia-xu; et al. | unlisted | `limit` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution... |
| EA-DATA-READ-0001 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 |
| EA-DATA-READ-0002 | changti-wu; bin-yu; zhaolong-shen; et al. | unlisted | `limit` | SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-READ-0008`: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
- `EA-DATA-READ-0003`: World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions.
- `EA-DATA-READ-0007`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- `EA-DATA-READ-0004`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- `EA-DATA-READ-0005`: 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。
- `EA-DATA-READ-0006`: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。
### 条件成立
- `EA-DATA-READ-0013`: VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。
- `EA-DATA-READ-0014`: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- `EA-DATA-READ-0009`: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing...
- `EA-DATA-READ-0010`: Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM feedback as weak ver...
- `EA-DATA-READ-0015`: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- `EA-DATA-READ-0012`: RynnWorld-Teleop将数字遥操作作为生成式数据引擎，但论文明确限定了它对精细流体动力学、高形变物体和跨机器人平台扩展的能力。
### 限制与失败模式
- `EA-DATA-READ-0011`: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- `EA-DATA-READ-0001`: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
- `EA-DATA-READ-0002`: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DATA-READ-0008` 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
  - `EA-DATA-READ-0003` World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield ex...
  - `EA-DATA-READ-0007` τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- Scientific memo preview: 《具身智能数据质量的主要矛盾》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 具身智能数据质量的主要矛盾 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 具身智能数据质量的主要矛盾: 先看证据边界，再谈一个可传播的反常识洞察。

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
