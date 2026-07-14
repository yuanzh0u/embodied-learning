# Review Packet: 具身数据感知误差与认知误差区别

## Scope

- Topic: 具身数据感知误差与认知误差区别
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `EA-MODEL`, `ERR-EMBODIED`
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
- Trace IDs: `EA-DATA-READ-0009`, `EA-DATA-READ-0010`, `EA-DATA-READ-0008`, `EA-DATA-READ-0011`, `EA-DATA-READ-0012`, `EA-DATA-READ-0013`, `EA-DATA-READ-0014`, `EA-DATA-READ-0015`, `EA-DATA-READ-0005`, `EA-DATA-READ-0006`, `EA-DATA-READ-0002`, `EA-DATA-READ-0003`
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
| `conditional` | 条件成立 | 5 |
| `limit` | 限制/负面 | 2 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2601.09708: Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning | 2026-01-14 | support | EA-DATA-READ-0009 |
| 2602.21161: ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking | 2026-02-24 | conditional | EA-DATA-READ-0005 |
| 2605.00080: World Model for Robot Learning: A Comprehensive Survey | 2026-04-30 | support | EA-DATA-READ-0010 |
| 2605.26349: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Co... | 2026-05-25 | support | EA-DATA-READ-0008 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional | EA-DATA-READ-0006 |
| 2606.03784: Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation | 2026-06-02 | conditional | EA-DATA-READ-0002 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional | EA-DATA-READ-0003 |
| 2606.09630: ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies | 2026-06-08 | support | EA-DATA-READ-0011 |
| 2606.09740: ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models | 2026-06-08 | support | EA-DATA-READ-0012 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional | EA-DATA-READ-0004 |
| 2606.24049: SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies | 2026-06-23 | limit | EA-DATA-READ-0007 |
| 2607.00673: Path Planning in Physically Viable World Models | 2026-07-01 | support | EA-DATA-READ-0013 |
| 2607.02642: GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | support | EA-DATA-READ-0014 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-DATA-READ-0001 |
| 2607.06564: Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | support | EA-DATA-READ-0015 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-READ-0009 | EA-DATA | `support` | `direct` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 | 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。 (5 Conclusion) | chi-pin-huang; yunze-man; zhiding-yu; et al. | 2601.09708 |
| EA-DATA-READ-0010 | EA-DATA | `support` | `direct` | 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 | 引言直接将纯反应 VLA 的三类困难列为长时程推理、temporal credit assignment 与 compounding errors。 (1 Introduction) | bohan-hou; gen-li; jindou-jia; et al. | 2605.00080 |
| EA-DATA-READ-0008 | EA-DATA | `support` | `direct` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 | 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。 (Abstract (full-text section)) | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | 2605.26349 |
| EA-DATA-READ-0011 | EA-DATA | `support` | `direct` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 | ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classifi... | haodi-hu; chung-ta-huang; jing-liu; et al. | 2606.09630 |
| EA-DATA-READ-0012 | EA-DATA | `support` | `direct` | ProbeAct 的探针实验表明，扰动下 VLA 视觉骨干仍保留目标物空间表示，而失败集中在动作头回落到记忆的训练轨迹。 | 引言将该失败定义为 latent perception 与 motor execution 的解耦，并把瓶颈定位到过拟合的 action head。 (1 Introduction) | fan-zhang; seongbin-park; baharan-mirzasoleiman; et al. | 2606.09740 |
| EA-DATA-READ-0013 | EA-DATA | `support` | `direct` | 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 | 摘要对比了原始重建环境与物理修改场景下的路线可行性，并报告后者能揭示前者不可见的失败。 (Abstract (full-text section)) | su-ann-low; cheng-hsi-hsiao; xingjian-li; et al. | 2607.00673 |
| EA-DATA-READ-0014 | EA-DATA | `support` | `direct` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-trai... | gigaworld-team; angyuan-ma; boyuan-wang; et al. | 2607.02642 |
| EA-DATA-READ-0015 | EA-DATA | `support` | `direct` | Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 | 引言将操作需求归结为显式 3D 结构与时间一致性，并说明纯 2D 管线及有损的跨模态变换会削弱这些约束。 (I Introduction) | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | 2607.06564 |
| EA-DATA-READ-0005 | EA-DATA | `conditional` | `direct` | ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 | 相关工作段明确提出解耦视觉部件，让 LLM 在已知感知状态上做 3D 物理与动作推理。 (II-B LLM/VLM Based Robotic Operation) | guangming-wang; qizhen-ying; yixiong-jing; et al. | 2602.21161 |
| EA-DATA-READ-0006 | EA-DATA | `conditional` | `direct` | τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 | 摘要直接列出四类交互数据和 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-DATA-READ-0002 | EA-DATA | `conditional` | `direct` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 | 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。 (Abstract (full-text section)) | nan-sun; yuan-zhang; yongkun-yang; et al. | 2606.03784 |
| EA-DATA-READ-0003 | EA-DATA | `conditional` | `direct` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 | 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。 (3.2 Synchronization and Data Quality Control) | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-DATA-READ-0004 | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-DATA-READ-0007 | EA-DATA | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-DATA-READ-0001 | EA-DATA | `limit` | `direct` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 | 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。 (5 Conclusion and Limitations) | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-READ-0009 | chi-pin-huang; yunze-man; zhiding-yu; et al. | unlisted | `support` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 |
| EA-DATA-READ-0010 | bohan-hou; gen-li; jindou-jia; et al. | unlisted | `support` | 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 |
| EA-DATA-READ-0008 | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | unlisted | `support` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 |
| EA-DATA-READ-0011 | haodi-hu; chung-ta-huang; jing-liu; et al. | unlisted | `support` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 |
| EA-DATA-READ-0012 | fan-zhang; seongbin-park; baharan-mirzasoleiman; et al. | unlisted | `support` | ProbeAct 的探针实验表明，扰动下 VLA 视觉骨干仍保留目标物空间表示，而失败集中在动作头回落到记忆的训练轨迹。 |
| EA-DATA-READ-0013 | su-ann-low; cheng-hsi-hsiao; xingjian-li; et al. | unlisted | `support` | 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 |
| EA-DATA-READ-0014 | gigaworld-team; angyuan-ma; boyuan-wang; et al. | unlisted | `support` | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 |
| EA-DATA-READ-0015 | jiaming-liu; qingpo-wuwu; nuowei-han; et al. | unlisted | `support` | Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 |
| EA-DATA-READ-0005 | guangming-wang; qizhen-ying; yixiong-jing; et al. | unlisted | `conditional` | ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 |
| EA-DATA-READ-0006 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `conditional` | τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 |
| EA-DATA-READ-0002 | nan-sun; yuan-zhang; yongkun-yang; et al. | unlisted | `conditional` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 |
| EA-DATA-READ-0003 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `conditional` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 |
| EA-DATA-READ-0004 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-DATA-READ-0007 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-DATA-READ-0001 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-READ-0009`: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
- `EA-DATA-READ-0010`: 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。
- `EA-DATA-READ-0008`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- `EA-DATA-READ-0011`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- `EA-DATA-READ-0012`: ProbeAct 的探针实验表明，扰动下 VLA 视觉骨干仍保留目标物空间表示，而失败集中在动作头回落到记忆的训练轨迹。
- `EA-DATA-READ-0013`: 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。
- `EA-DATA-READ-0014`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- `EA-DATA-READ-0015`: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。
### 条件成立
- `EA-DATA-READ-0005`: ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。
- `EA-DATA-READ-0006`: τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。
- `EA-DATA-READ-0002`: ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。
- `EA-DATA-READ-0003`: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- `EA-DATA-READ-0004`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
### 限制与失败模式
- `EA-DATA-READ-0007`: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- `EA-DATA-READ-0001`: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DATA-READ-0009` 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
  - `EA-DATA-READ-0010` 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。
  - `EA-DATA-READ-0008` DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- Scientific memo preview: 《具身数据感知误差与认知误差区别》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 具身数据感知误差与认知误差区别 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 具身数据感知误差与认知误差区别: 先看证据边界，再谈一个可传播的反常识洞察。

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
