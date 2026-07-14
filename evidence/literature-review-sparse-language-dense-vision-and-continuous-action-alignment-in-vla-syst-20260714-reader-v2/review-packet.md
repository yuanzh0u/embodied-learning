# Review Packet: Sparse language, dense vision, and continuous action alignment in VLA systems

## Scope

- Topic: Sparse language, dense vision, and continuous action alignment in VLA systems
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-SENSOR`, `EA-XEMBODIMENT`, `EA-ALIGN`
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
- Trace IDs: `EA-ALIGN-READ-0013`, `EA-ALIGN-READ-0014`, `EA-ALIGN-READ-0012`, `EA-ALIGN-READ-0015`, `EA-ALIGN-READ-0005`, `EA-ALIGN-READ-0010`, `EA-ALIGN-READ-0011`, `EA-ALIGN-READ-0006`, `EA-ALIGN-READ-0007`, `EA-ALIGN-READ-0008`, `EA-ALIGN-READ-0002`, `EA-ALIGN-READ-0001`
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
| `conditional` | 条件成立 | 6 |
| `limit` | 限制/负面 | 4 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2601.09708: Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning | 2026-01-14 | support | EA-ALIGN-READ-0013 |
| 2602.21161: ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking | 2026-02-24 | conditional | EA-ALIGN-READ-0010 |
| 2605.00080: World Model for Robot Learning: A Comprehensive Survey | 2026-04-30 | support | EA-ALIGN-READ-0014 |
| 2605.26349: Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Co... | 2026-05-25 | support | EA-ALIGN-READ-0012 |
| 2606.01027: $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation | 2026-05-31 | conditional | EA-ALIGN-READ-0011 |
| 2606.03784: Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation | 2026-06-02 | conditional | EA-ALIGN-READ-0006 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional | EA-ALIGN-READ-0007 |
| 2606.09630: ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies | 2026-06-08 | support | EA-ALIGN-READ-0015 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | conditional | EA-ALIGN-READ-0008 |
| 2606.24049: SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies | 2026-06-23 | limit | EA-ALIGN-READ-0001 |
| 2606.26800: SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation | 2026-06-25 | conditional | EA-ALIGN-READ-0002 |
| 2606.30113: SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance | 2026-06-29 | limit | EA-ALIGN-READ-0003 |
| 2606.30456: Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform | 2026-06-29 | limit | EA-ALIGN-READ-0004 |
| 2606.30552: Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision | 2026-06-29 | support | EA-ALIGN-READ-0005 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | limit | EA-ALIGN-READ-0009 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-ALIGN-READ-0013 | EA-MODEL | `support` | `direct` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 | 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。 (5 Conclusion) | chi-pin-huang; yunze-man; zhiding-yu; et al. | 2601.09708 |
| EA-ALIGN-READ-0014 | EA-MODEL | `support` | `direct` | 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 | 引言直接将纯反应 VLA 的三类困难列为长时程推理、temporal credit assignment 与 compounding errors。 (1 Introduction) | bohan-hou; gen-li; jindou-jia; et al. | 2605.00080 |
| EA-ALIGN-READ-0012 | EA-MODEL | `support` | `direct` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 | 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。 (Abstract (full-text section)) | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | 2605.26349 |
| EA-ALIGN-READ-0015 | EA-MODEL | `support` | `direct` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 | ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classifi... | haodi-hu; chung-ta-huang; jing-liu; et al. | 2606.09630 |
| EA-ALIGN-READ-0005 | EA-MODEL | `support` | `direct` | Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. | The paper frames low-level state/action heterogeneity as a core cross-embodiment challenge, then uses dense embodied chain-of-thought supervision in the VLM stream and a flow-matching action expert that outputs continuo... | haoyang-li; guanlin-li; youhe-feng; et al. | 2606.30552 |
| EA-ALIGN-READ-0010 | EA-MODEL | `conditional` | `direct` | ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 | 相关工作段明确提出解耦视觉部件，让 LLM 在已知感知状态上做 3D 物理与动作推理。 (II-B LLM/VLM Based Robotic Operation) | guangming-wang; qizhen-ying; yixiong-jing; et al. | 2602.21161 |
| EA-ALIGN-READ-0011 | EA-MODEL | `conditional` | `direct` | τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 | 摘要直接列出四类交互数据和 modality-specific supervision masks。 (Abstract (full-text section)) | pengfei-zhou; shengcong-chen; di-chen; et al. | 2606.01027 |
| EA-ALIGN-READ-0006 | EA-MODEL | `conditional` | `direct` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 | 摘要同时给出了动作相关 grounding 的有效性与 autoregressive action prefix 的 compounding-error 限制。 (Abstract (full-text section)) | nan-sun; yuan-zhang; yongkun-yang; et al. | 2606.03784 |
| EA-ALIGN-READ-0007 | EA-MODEL | `conditional` | `direct` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 | 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。 (3.2 Synchronization and Data Quality Control) | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-ALIGN-READ-0008 | EA-MODEL | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-ALIGN-READ-0002 | EA-MODEL | `conditional` | `direct` | A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. | SSI-Policy builds an RGB-only structured scene interface encoding monocular depth features, language-grounded layouts, and instruction-conditioned 2D motion trajectories; it reports few-shot gains but notes failures fro... | kaijun-wang; zikai-ouyang; xuping-wu; et al. | 2606.26800 |
| EA-ALIGN-READ-0001 | EA-MODEL | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-ALIGN-READ-0003 | EA-MODEL | `limit` | `direct` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same to... | SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines. (Abstract (full-text section)) | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | 2606.30113 |
| EA-ALIGN-READ-0004 | EA-MODEL | `limit` | `direct` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset c... | The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone. (Abstract (full-text section... | mathilde-hochedel; marc-lalonde | 2606.30456 |
| EA-ALIGN-READ-0009 | EA-MODEL | `limit` | `direct` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 | 结论的 Recognize–Imagine–Label 回路明确连接了真实失败、视频—力联合想象与纠正动作标注。 (5 Conclusion and Limitations) | shengbang-liu; yueru-jia; yuyang-yan; et al. | 2607.02840 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-ALIGN-READ-0013 | chi-pin-huang; yunze-man; zhiding-yu; et al. | unlisted | `support` | 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 |
| EA-ALIGN-READ-0014 | bohan-hou; gen-li; jindou-jia; et al. | unlisted | `support` | 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 |
| EA-ALIGN-READ-0012 | gokul-narayanan; yash-shahapurkar; melih-erdogan; et al. | unlisted | `support` | DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 |
| EA-ALIGN-READ-0015 | haodi-hu; chung-ta-huang; jing-liu; et al. | unlisted | `support` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 |
| EA-ALIGN-READ-0005 | haoyang-li; guanlin-li; youhe-feng; et al. | unlisted | `support` | Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action s... |
| EA-ALIGN-READ-0010 | guangming-wang; qizhen-ying; yixiong-jing; et al. | unlisted | `conditional` | ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 |
| EA-ALIGN-READ-0011 | pengfei-zhou; shengcong-chen; di-chen; et al. | unlisted | `conditional` | τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 |
| EA-ALIGN-READ-0006 | nan-sun; yuan-zhang; yongkun-yang; et al. | unlisted | `conditional` | ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 |
| EA-ALIGN-READ-0007 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `conditional` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 |
| EA-ALIGN-READ-0008 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `conditional` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 |
| EA-ALIGN-READ-0002 | kaijun-wang; zikai-ouyang; xuping-wu; et al. | unlisted | `conditional` | A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action con... |
| EA-ALIGN-READ-0001 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-ALIGN-READ-0003 | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | unlisted | `limit` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottlen... |
| EA-ALIGN-READ-0004 | mathilde-hochedel; marc-lalonde | unlisted | `limit` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preproce... |
| EA-ALIGN-READ-0009 | shengbang-liu; yueru-jia; yuyang-yan; et al. | unlisted | `limit` | TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 |

## Synthesis Slots

### 共识/正向证据
- `EA-ALIGN-READ-0013`: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
- `EA-ALIGN-READ-0014`: 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。
- `EA-ALIGN-READ-0012`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- `EA-ALIGN-READ-0015`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- `EA-ALIGN-READ-0005`: Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces.
### 条件成立
- `EA-ALIGN-READ-0010`: ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。
- `EA-ALIGN-READ-0011`: τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。
- `EA-ALIGN-READ-0006`: ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。
- `EA-ALIGN-READ-0007`: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- `EA-ALIGN-READ-0008`: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- `EA-ALIGN-READ-0002`: A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control.
### 限制与失败模式
- `EA-ALIGN-READ-0001`: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- `EA-ALIGN-READ-0003`: Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under d...
- `EA-ALIGN-READ-0004`: Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- `EA-ALIGN-READ-0009`: TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-ALIGN-READ-0013` 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
  - `EA-ALIGN-READ-0014` 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。
  - `EA-ALIGN-READ-0012` DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- Scientific memo preview: 《Sparse language, dense vision, and continuous action alignment in VLA systems》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: Sparse language, dense vision, and continuous action alignment in VLA systems 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: Sparse language, dense vision, and continuous action alignment in VLA systems: 先看证据边界，再谈一个可传播的反常识洞察。

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
