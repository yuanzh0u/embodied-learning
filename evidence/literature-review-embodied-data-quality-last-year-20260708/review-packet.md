# Review Packet: 近一年已发表论文中的具身智能数据质量

## Scope

- Topic: 近一年已发表论文中的具身智能数据质量
- Time range: 2025-07-08..2026-07-08
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-MODEL`, `EA-EVAL`
- Evidence events: 12
- Topic cards: 1
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: planner -> hub -> review packet -> style menu.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for retrieval, HTML mining, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 12
- Stance labels: `conditional`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-2026-LY-0007`, `EA-DATA-2026-LY-0011`, `EA-DATA-2026-LY-0001`, `EA-DATA-2026-LY-0009`, `EA-DATA-2026-LY-0003`, `EA-DATA-2026-LY-0002`, `EA-DATA-2026-LY-0005`, `EA-DATA-2026-LY-0010`, `EA-DATA-2026-LY-0008`, `EA-DATA-2026-LY-0004`, `EA-DATA-2026-LY-0012`, `EA-DATA-2026-LY-0006`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Paper-level sources: 12 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、时间同步、标定、动作表示、元数据、采集员规范和质量审计组成的工程体系。UMI 更接近可学控制数据，Ego/Ego4D 更接近感知与任务先验，DROID 展示了自然场景大规模机器人数据的组织难度。无目标机器人本体阶段仍可积累任务、视觉、语义、可重定向轨迹和失败库，但不能直接等价为可部署策略数据，最终需要少量目标机器人锚点闭环校准。泛化任务优先任务/场景多样性，工业单任务优先数据精度、边界工况和失败恢复。遮挡、异构数据有效性和单视角限制必须用任务相关指标验证。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 7 |
| `conditional` | 条件成立 | 5 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2509.01657: Data Retrieval with Importance Weights for Few-Shot Imitation Learning | 2025-09-01 | support | EA-DATA-2026-LY-0007 |
| 2512.13100: OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning | 2025-12-15 | support | EA-DATA-2026-LY-0011 |
| 2602.10618: From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation... | 2026-02-11 | conditional | EA-DATA-2026-LY-0010 |
| 2602.13197: Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos | 2026-02-13 | conditional | EA-DATA-2026-LY-0008 |
| 2603.09056: Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning | 2026-03-10 | support | EA-DATA-2026-LY-0001 |
| 2603.11634: Diversity You Can Actually Measure: A Fast, Model-Free Diversity Metric for Robotics Datasets | 2026-03-12 | conditional | EA-DATA-2026-LY-0004 |
| 2603.17189: Influence of Gripper Design on Human Demonstration Quality for Robot Learning | 2026-03-17 | support | EA-DATA-2026-LY-0009 |
| 2605.01544: An Efficient Metric for Data Quality Measurement in Imitation Learning | 2026-05-02 | support | EA-DATA-2026-LY-0003 |
| 2605.26349: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Co... | 2026-05-25 | support | EA-DATA-2026-LY-0002 |
| 2606.12365: Ambient Diffusion Policy: Imitation Learning from Suboptimal Data in Robotics | 2026-06-10 | conditional | EA-DATA-2026-LY-0012 |
| 2606.16208: ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation | 2026-06-15 | support | EA-DATA-2026-LY-0005 |
| 2606.28320: WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation | 2026-06-26 | conditional | EA-DATA-2026-LY-0006 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-2026-LY-0007 | EA-DATA | `support` | `direct` | 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 | IWR 将 retrieval-based imitation learning 的常用最近邻规则解释为目标数据分布 KDE 的极限，指出其高方差、易受噪声影响且不考虑 prior data distribution；方法用目标/先验分布概率比进行 importance-weighted retrieval，并在仿真和 Bridge 真实评估中改善现有检索方法。 (Abstract; 1 Introduction; 2 Related... | amber-xie; rahul-chand; dorsa-sadigh; et al. | 2509.01657 |
| EA-DATA-2026-LY-0011 | EA-DATA | `support` | `direct` | 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 | 论文指出 OXE 聚合 60 多个机器人数据集，但 top four robot types 占超过 85% 真实数据，带来过拟合风险；OXE-AugE 用 9 种不同机器人本体扩增 16 个 OXE 子集，形成 4.4M trajectories，并研究扩增对 cross-embodiment learning 的影响。 (Abstract; 1 Introduction; 6 OXE-AugE: A Large Open-Sour... | guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al. | 2512.13100 |
| EA-DATA-2026-LY-0001 | EA-DATA | `support` | `direct` | 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 | 论文指出人类遥操作会带来错误、操作约束、技能差异、噪声和次优行为；QoQ 用 influence functions 衡量训练 state-action 对验证示范的贡献，并在轨迹层聚合以降低噪声、保持覆盖，在仿真、真实机器人和 DROID in-the-wild 数据上改善策略成功率。 (I INTRODUCTION; II-B Robot data curation; VI CONCLUSIONS) | haeone-lee; taywon-min; junsu-kim; et al. | 2603.09056 |
| EA-DATA-2026-LY-0009 | EA-DATA | `support` | `direct` | 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 | 论文指出 UMI 示教虽快于遥操作但仍比手工慢、工具重量会造成疲劳并影响 demonstration；实验中改变 UMI gripper fingers 的力分布显著影响打开绷带包装表现，concentrated load grippers 优于 distributed load grippers，作者将其连接到 demonstration quality 和 learned robot control policies。 (II-A... | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | 2603.17189 |
| EA-DATA-2026-LY-0003 | EA-DATA | `support` | `direct` | 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 | 论文把 poor-quality end-user demonstrations 具体化为 excessive corrective motions、oscillations 和 abrupt adjustments，并提出基于 demonstration trajectories PSD 的自动排序指标；实验比较未筛选、oracle、现有排序和 jerk/path-length 等 baseline，研究 PSD 筛选对下游 IL... | noushad-sojib; momotaz-begum | 2605.01544 |
| EA-DATA-2026-LY-0002 | EA-DATA | `support` | `direct` | 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 | DQAF 框架从 sub-task progress、motion smoothness、stalls、kinematic limits 抽取质量信号，生成结构化质量评估和自然语言纠正建议；pilot study 中即时反馈条件呈现更高任务完成度、更高 episode-level quality scores 和更少 detected suboptimalities 的趋势。 (I INTRODUCTION; Abstract; V-... | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | 2605.26349 |
| EA-DATA-2026-LY-0005 | EA-DATA | `support` | `direct` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 | ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。 (1 Introduction; 2 R... | tao-xu; jiaxin-wang; runhao-zhang; et al. | 2606.16208 |
| EA-DATA-2026-LY-0010 | EA-DATA | `conditional` | `direct` | VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 | 论文指出 VR 用于记录机器人学习示教时，visual fidelity 可能不如 user behavior 的 quality/reliability 重要；输入设备与可视化会影响工作负荷、运动效率、不必要动作和执行精度。实验发现 controller 与 motion-capture gloves 在 pick-and-place 与 manner-oriented tasks 上呈现不同轨迹策略和权衡。 (1 Introduc... | robin-beierling; manuel-scheibl; jonas-dech; et al. | 2602.10618 |
| EA-DATA-2026-LY-0008 | EA-DATA | `conditional` | `direct` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 | PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。 (1 Introduction; 3.3 T... | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | 2602.13197 |
| EA-DATA-2026-LY-0004 | EA-DATA | `conditional` | `direct` | 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 | FAKTUAL 用 signature-kernel entropy 直接在 demonstration dataset 上度量多样性并选择高熵子集；作者在结论中明确说明该方法不像其他 data curation 策略那样保证只选高质量轨迹，若数据集中存在有害轨迹，最 diverse 子集可能反而有损。 (I Introduction; Abstract; IX Conclusion and Limitations) | sreevardhan-sirigiri; nathan-samuel-de-lara; christopher-agia; et al. | 2603.11634 |
| EA-DATA-2026-LY-0012 | EA-DATA | `conditional` | `direct` | 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 | Ambient Diffusion Policy 指出高质量任务专用机器人数据昂贵，而 failures、不同质量轨迹、仿真、跨本体和 egocentric video 等 suboptimal/OOD sources 很丰富；作者认为过滤会浪费数据，常规 co-training 又会学习 harmful parts，因此提出 noise-dependent data usage，只在特定 diffusion times 让 subo... | adam-wei; nicholas-pfaff; thomas-cohn; et al. | 2606.12365 |
| EA-DATA-2026-LY-0006 | EA-DATA | `conditional` | `direct` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 | 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action... | justin-yu; andrew-goldberg; kavish-kondap; et al. | 2606.28320 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-2026-LY-0007 | amber-xie; rahul-chand; dorsa-sadigh; et al. | unlisted | `support` | 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 |
| EA-DATA-2026-LY-0011 | guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al. | unlisted | `support` | 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 |
| EA-DATA-2026-LY-0001 | haeone-lee; taywon-min; junsu-kim; et al. | unlisted | `support` | 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 |
| EA-DATA-2026-LY-0009 | gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al. | unlisted | `support` | 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 |
| EA-DATA-2026-LY-0003 | noushad-sojib; momotaz-begum | unlisted | `support` | 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 |
| EA-DATA-2026-LY-0002 | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | unlisted | `support` | 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 |
| EA-DATA-2026-LY-0005 | tao-xu; jiaxin-wang; runhao-zhang; et al. | unlisted | `support` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 |
| EA-DATA-2026-LY-0010 | robin-beierling; manuel-scheibl; jonas-dech; et al. | unlisted | `conditional` | VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 |
| EA-DATA-2026-LY-0008 | albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al. | unlisted | `conditional` | 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 |
| EA-DATA-2026-LY-0004 | sreevardhan-sirigiri; nathan-samuel-de-lara; christopher-agia; et al. | unlisted | `conditional` | 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 |
| EA-DATA-2026-LY-0012 | adam-wei; nicholas-pfaff; thomas-cohn; et al. | unlisted | `conditional` | 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 |
| EA-DATA-2026-LY-0006 | justin-yu; andrew-goldberg; kavish-kondap; et al. | unlisted | `conditional` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-2026-LY-0007`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
- `EA-DATA-2026-LY-0011`: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
- `EA-DATA-2026-LY-0001`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
- `EA-DATA-2026-LY-0009`: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
- `EA-DATA-2026-LY-0003`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。
- `EA-DATA-2026-LY-0002`: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。
- `EA-DATA-2026-LY-0005`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
### 条件成立
- `EA-DATA-2026-LY-0010`: VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。
- `EA-DATA-2026-LY-0008`: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- `EA-DATA-2026-LY-0004`: 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。
- `EA-DATA-2026-LY-0012`: 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。
- `EA-DATA-2026-LY-0006`: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 12 / 5
- Recommended default: all
- Core claims:
  - `EA-DATA-2026-LY-0007` 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
  - `EA-DATA-2026-LY-0011` 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
  - `EA-DATA-2026-LY-0001` 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
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
