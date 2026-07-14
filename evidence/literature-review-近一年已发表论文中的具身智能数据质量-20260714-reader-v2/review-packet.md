# Review Packet: 近一年已发表论文中的具身智能数据质量

## Scope

- Topic: 近一年已发表论文中的具身智能数据质量
- Time range: 2025-07-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-MODEL`, `EA-EVAL`
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
- Trace IDs: `EA-DQ-YEAR-READ-0008`, `EA-DQ-YEAR-READ-0009`, `EA-DQ-YEAR-READ-0005`, `EA-DQ-YEAR-READ-0001`, `EA-DQ-YEAR-READ-0006`, `EA-DQ-YEAR-READ-0007`, `EA-DQ-YEAR-READ-0010`, `EA-DQ-YEAR-READ-0002`, `EA-DQ-YEAR-READ-0003`, `EA-DQ-YEAR-READ-0011`, `EA-DQ-YEAR-READ-0012`, `EA-DQ-YEAR-READ-0004`
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
| `conditional` | 条件成立 | 5 |
| `limit` | 限制/负面 | 3 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2509.01657: Data Retrieval with Importance Weights for Few-Shot Imitation Learning | 2025-09-01 | support | EA-DQ-YEAR-READ-0008 |
| 2512.13100: OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning | 2025-12-15 | support | EA-DQ-YEAR-READ-0009 |
| 2602.10618: From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation... | 2026-02-11 | conditional | EA-DQ-YEAR-READ-0002 |
| 2602.13197: Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos | 2026-02-13 | conditional | EA-DQ-YEAR-READ-0003 |
| 2603.09056: Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning | 2026-03-10 | support | EA-DQ-YEAR-READ-0005 |
| 2603.17189: Influence of Gripper Design on Human Demonstration Quality for Robot Learning | 2026-03-17 | support | EA-DQ-YEAR-READ-0001 |
| 2605.01544: An Efficient Metric for Data Quality Measurement in Imitation Learning | 2026-05-02 | support | EA-DQ-YEAR-READ-0006 |
| 2605.26349: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Co... | 2026-05-25 | support | EA-DQ-YEAR-READ-0007 |
| 2606.02577: RoboDream: Compositional World Models for Scalable Robot Data Synthesis | 2026-06-01 | conditional | EA-DQ-YEAR-READ-0011 |
| 2606.12072: World Model Self-Distillation: Training World Models to Solve General Tasks | 2026-06-10 | conditional | EA-DQ-YEAR-READ-0012 |
| 2606.12403: World Pilot: Steering Vision-Language-Action Models with World-Action Priors | 2026-06-10 | limit | EA-DQ-YEAR-READ-0013 |
| 2606.16208: ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation | 2026-06-15 | support | EA-DQ-YEAR-READ-0010 |
| 2606.28320: WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation | 2026-06-26 | conditional | EA-DQ-YEAR-READ-0004 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-DQ-YEAR-READ-0014 |
| 2607.06442: SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | limit | EA-DQ-YEAR-READ-0015 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DQ-YEAR-READ-0008 | EA-DATA | `support` | `direct` | 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 | IWR 将 retrieval-based imitation learning 的常用最近邻规则解释为目标数据分布 KDE 的极限，指出其高方差、易受噪声影响且不考虑 prior data distribution；方法用目标/先验分布概率比进行 importance-weighted retrieval，并在仿真和 Bridge 真实评估中改善现有检索方法。 (Abstract (full-text section)) | amber-xie; rahul-chand; dorsa-sadigh; et al. | 2509.01657 |
| EA-DQ-YEAR-READ-0009 | EA-DATA | `support` | `direct` | 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 | 论文指出 OXE 聚合 60 多个机器人数据集，但 top four robot types 占超过 85% 真实数据，带来过拟合风险；OXE-AugE 用 9 种不同机器人本体扩增 16 个 OXE 子集，形成 4.4M trajectories，并研究扩增对 cross-embodiment learning 的影响。 (Abstract (full-text section)) | guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al. | 2512.13100 |
| EA-DQ-YEAR-READ-0005 | EA-DATA | `support` | `direct` | 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 | 论文指出人类遥操作会带来错误、操作约束、技能差异、噪声和次优行为；QoQ 用 influence functions 衡量训练 state-action 对验证示范的贡献，并在轨迹层聚合以降低噪声、保持覆盖，在仿真、真实机器人和 DROID in-the-wild 数据上改善策略成功率。 (VI CONCLUSIONS) | haeone-lee; taywon-min; junsu-kim; et al. | 2603.09056 |
| EA-DQ-YEAR-READ-0001 | EA-DATA | `support` | `direct` | 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 | 论文指出 UMI 示教虽快于遥操作但仍比手工慢、工具重量会造成疲劳并影响 demonstration；实验中改变 UMI gripper fingers 的力分布显著影响打开绷带包装表现，concentrated load grippers 优于 distributed load grippers，作者将其连接到 demonstration quality 和 learned robot control policies。 (V DI... | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | 2603.17189 |
| EA-DQ-YEAR-READ-0006 | EA-DATA | `support` | `direct` | 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 | 论文把 poor-quality end-user demonstrations 具体化为 excessive corrective motions、oscillations 和 abrupt adjustments，并提出基于 demonstration trajectories PSD 的自动排序指标；实验比较未筛选、oracle、现有排序和 jerk/path-length 等 baseline，研究 PSD 筛选对下游 IL... | noushad-sojib; momotaz-begum | 2605.01544 |
| EA-DQ-YEAR-READ-0007 | EA-DATA | `support` | `direct` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 | 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。 (Abstract (full-text section)) | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | 2605.26349 |
| EA-DQ-YEAR-READ-0010 | EA-DATA | `support` | `direct` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 | ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。 (C.4 Retention Balan... | tao-xu; jiaxin-wang; runhao-zhang; et al. | 2606.16208 |
| EA-DQ-YEAR-READ-0002 | EA-DATA | `conditional` | `direct` | VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 | 论文指出 VR 用于记录机器人学习示教时，visual fidelity 可能不如 user behavior 的 quality/reliability 重要；输入设备与可视化会影响工作负荷、运动效率、不必要动作和执行精度。实验发现 controller 与 motion-capture gloves 在 pick-and-place 与 manner-oriented tasks 上呈现不同轨迹策略和权衡。 (1 Introduc... | robin-beierling; manuel-scheibl; jonas-dech; et al. | 2602.10618 |
| EA-DQ-YEAR-READ-0003 | EA-DATA | `conditional` | `direct` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 | PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。 (3.3 Trajectory and Gr... | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | 2602.13197 |
| EA-DQ-YEAR-READ-0011 | EA-DATA | `conditional` | `direct` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel object... | RoboDream anchors generation to rendered robot motion, conditions on scene/object priors, and introduces retrieval-and-rebirth plus prop-free teleoperation to generate demonstrations and reduce real data collection cost... | junjie-ye; rong-xue; basile-van-hoorick; et al. | 2606.02577 |
| EA-DQ-YEAR-READ-0012 | EA-DATA | `conditional` | `direct` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and... | WMSD frames supervised fine-tuning on paired task-execution videos as costly, then proposes self-distillation and reinforcement learning where a VLM generates tasks/solutions from unlabeled scene images and feedback ver... | sebastian-stapf | 2606.12072 |
| EA-DQ-YEAR-READ-0004 | EA-DATA | `conditional` | `direct` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 | 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action... | justin-yu; andrew-goldberg; kavish-kondap; et al. | 2606.28320 |
| EA-DQ-YEAR-READ-0013 | EA-DATA | `limit` | `direct` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. | World Pilot argues that VLA semantic grounding from static image-text pairs cannot capture continuous contact-rich dynamics, and uses WAM-derived scene-evolution and trajectory priors to complement the policy. (Abstract... | world-pilot-authors | 2606.12403 |
| EA-DQ-YEAR-READ-0014 | EA-DATA | `limit` | `direct` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 | 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。 (5 Conclusion and Limitations) | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |
| EA-DQ-YEAR-READ-0015 | EA-DATA | `limit` | `direct` | SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 | 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。 (Introduction) | changti-wu; bin-yu; zhaolong-shen; et al. | 2607.06442 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DQ-YEAR-READ-0008 | amber-xie; rahul-chand; dorsa-sadigh; et al. | unlisted | `support` | 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 |
| EA-DQ-YEAR-READ-0009 | guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al. | unlisted | `support` | 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 |
| EA-DQ-YEAR-READ-0005 | haeone-lee; taywon-min; junsu-kim; et al. | unlisted | `support` | 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 |
| EA-DQ-YEAR-READ-0001 | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | unlisted | `support` | 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 |
| EA-DQ-YEAR-READ-0006 | noushad-sojib; momotaz-begum | unlisted | `support` | 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 |
| EA-DQ-YEAR-READ-0007 | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | unlisted | `support` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 |
| EA-DQ-YEAR-READ-0010 | tao-xu; jiaxin-wang; runhao-zhang; et al. | unlisted | `support` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 |
| EA-DQ-YEAR-READ-0002 | robin-beierling; manuel-scheibl; jonas-dech; et al. | unlisted | `conditional` | VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 |
| EA-DQ-YEAR-READ-0003 | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | unlisted | `conditional` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 |
| EA-DQ-YEAR-READ-0011 | junjie-ye; rong-xue; basile-van-hoorick; et al. | unlisted | `conditional` | Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrat... |
| EA-DQ-YEAR-READ-0012 | sebastian-stapf | unlisted | `conditional` | Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM... |
| EA-DQ-YEAR-READ-0004 | justin-yu; andrew-goldberg; kavish-kondap; et al. | unlisted | `conditional` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 |
| EA-DQ-YEAR-READ-0013 | world-pilot-authors | unlisted | `limit` | Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution... |
| EA-DQ-YEAR-READ-0014 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 |
| EA-DQ-YEAR-READ-0015 | changti-wu; bin-yu; zhaolong-shen; et al. | unlisted | `limit` | SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DQ-YEAR-READ-0008`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
- `EA-DQ-YEAR-READ-0009`: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
- `EA-DQ-YEAR-READ-0005`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
- `EA-DQ-YEAR-READ-0001`: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
- `EA-DQ-YEAR-READ-0006`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。
- `EA-DQ-YEAR-READ-0007`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- `EA-DQ-YEAR-READ-0010`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
### 条件成立
- `EA-DQ-YEAR-READ-0002`: VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。
- `EA-DQ-YEAR-READ-0003`: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- `EA-DQ-YEAR-READ-0011`: Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewpoints while reducing...
- `EA-DQ-YEAR-READ-0012`: Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM feedback as weak ver...
- `EA-DQ-YEAR-READ-0004`: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
### 限制与失败模式
- `EA-DQ-YEAR-READ-0013`: Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics.
- `EA-DQ-YEAR-READ-0014`: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。
- `EA-DQ-YEAR-READ-0015`: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DQ-YEAR-READ-0008` 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
  - `EA-DQ-YEAR-READ-0009` 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
  - `EA-DQ-YEAR-READ-0005` 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
- Scientific memo preview: 《近一年已发表论文中的具身智能数据质量》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年已发表论文中的具身智能数据质量 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年已发表论文中的具身智能数据质量: 先看证据边界，再谈一个可传播的反常识洞察。

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
