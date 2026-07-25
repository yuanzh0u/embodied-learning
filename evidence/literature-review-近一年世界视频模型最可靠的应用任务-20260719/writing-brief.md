# Writing Brief: 近一年世界视频模型最可靠的应用任务

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年世界视频模型最可靠的应用任务
- Time range: 2025-07-19..2026-07-19
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-4D`
- Review mode: scoping
- Paper-level sources: 30 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 31

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-4D-READ-0013](evidence-appendix.md#ea-4d-read-0013)) ⟷ LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 ([2510.03827](https://arxiv.org/abs/2510.03827) / [EA-CONTAM-2026-0007](evidence-appendix.md#ea-contam-2026-0007))
- `EA-DATA`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-tra... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-WMDATA-READ-0007](evidence-appendix.md#ea-wmdata-read-0007)) ⟷ 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- `EA-DATA`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow ta... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-WMDATA-READ-0008](evidence-appendix.md#ea-wmdata-read-0008)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `EA-DATA`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, n... ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-WMDATA-READ-0009](evidence-appendix.md#ea-wmdata-read-0009)) ⟷ 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- `EA-DATA`: 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 ([2607.00673](https://arxiv.org/abs/2607.00673) / [ERR-PVC-READ-0013](evidence-appendix.md#err-pvc-read-0013)) ⟷ LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 ([2510.03827](https://arxiv.org/abs/2510.03827) / [EA-CONTAM-2026-0007](evidence-appendix.md#ea-contam-2026-0007))
- `EA-DATA`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [ERR-PVC-READ-0014](evidence-appendix.md#err-pvc-read-0014)) ⟷ 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- `EA-EVAL`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-WMEVAL-READ-0001](evidence-appendix.md#ea-wmeval-read-0001)) ⟷ In the DROID/RoboArena setting, a closed-loop video-world-model evaluator produced a policy ranking that closely matche... ([2607.01060](https://arxiv.org/abs/2607.01060) / [EA-WMTASK-2026-0001](evidence-appendix.md#ea-wmtask-2026-0001))
- `EA-EVAL`: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, c... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-WMEVAL-READ-0003](evidence-appendix.md#ea-wmeval-read-0003)) ⟷ PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and pos... ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-WMEVAL-READ-0008](evidence-appendix.md#ea-wmeval-read-0008))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (10 events)
- [`support`] A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horiz... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-WMDATA-READ-0007](evidence-appendix.md#ea-wmdata-read-0007))
- [`support`] World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-WMDATA-READ-0009](evidence-appendix.md#ea-wmdata-read-0009))
- [`support`] Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon futur... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-WMDATA-READ-0008](evidence-appendix.md#ea-wmdata-read-0008))
- [`support`] Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-4D-READ-0013](evidence-appendix.md#ea-4d-read-0013))
- [`support`] 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 ([2607.00673](https://arxiv.org/abs/2607.00673) / [ERR-PVC-READ-0013](evidence-appendix.md#err-pvc-read-0013))
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [ERR-PVC-READ-0014](evidence-appendix.md#err-pvc-read-0014))
- [`conditional`] 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- [`limit`] 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- [`limit`] LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 ([2510.03827](https://arxiv.org/abs/2510.03827) / [EA-CONTAM-2026-0007](evidence-appendix.md#ea-contam-2026-0007))

### EA-EVAL (14 events)
- [`support`] Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-WMEVAL-READ-0007](evidence-appendix.md#ea-wmeval-read-0007))
- [`support`] GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-WMEVAL-READ-0005](evidence-appendix.md#ea-wmeval-read-0005))
- [`support`] Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information do... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-WMEVAL-READ-0003](evidence-appendix.md#ea-wmeval-read-0003))
- [`support`] τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-WMEVAL-READ-0001](evidence-appendix.md#ea-wmeval-read-0001))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-WMEVAL-READ-0010](evidence-appendix.md#ea-wmeval-read-0010))
- [`conditional`] A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-WMEVAL-READ-0014](evidence-appendix.md#ea-wmeval-read-0014))
- [`conditional`] Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-WMEVAL-READ-0011](evidence-appendix.md#ea-wmeval-read-0011))
- [`conditional`] In the DROID/RoboArena setting, a closed-loop video-world-model evaluator produced a policy ranking that closely matched the real-robot leaderboard across the evaluated policies, supporting policy ra... ([2607.01060](https://arxiv.org/abs/2607.01060) / [EA-WMTASK-2026-0001](evidence-appendix.md#ea-wmtask-2026-0001))
- [`limit`] PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-WMEVAL-READ-0008](evidence-appendix.md#ea-wmeval-read-0008))
- [`limit`] World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMEVAL-READ-0015](evidence-appendix.md#ea-wmeval-read-0015))
- [`limit`] Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-WMEVAL-READ-0013](evidence-appendix.md#ea-wmeval-read-0013))
- [`limit`] RoboWorld's principal qualitative failures occur after object contact, when manipulated objects may disintegrate, morph unrealistically, or become visually inconsistent, limiting contact-rich manipul... ([2607.01060](https://arxiv.org/abs/2607.01060) / [EA-WMTASK-2026-0002](evidence-appendix.md#ea-wmtask-2026-0002))
- [`gap`] Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-WMEVAL-READ-0006](evidence-appendix.md#ea-wmeval-read-0006))
- [`gap`] Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection. ([2605.29360](https://arxiv.org/abs/2605.29360) / [EA-WMEVAL-READ-0004](evidence-appendix.md#ea-wmeval-read-0004))

### EA-MODEL (7 events)
- [`support`] 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-ALIGN-READ-0013](evidence-appendix.md#ea-align-read-0013))
- [`support`] 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-ALIGN-READ-0015](evidence-appendix.md#ea-align-read-0015))
- [`conditional`] ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-ALIGN-READ-0006](evidence-appendix.md#ea-align-read-0006))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- [`limit`] Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- [`limit`] Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-ALIGN-READ-0009](evidence-appendix.md#ea-align-read-0009))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `limit` 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- `limit` LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 ([2510.03827](https://arxiv.org/abs/2510.03827) / [EA-CONTAM-2026-0007](evidence-appendix.md#ea-contam-2026-0007))
- `conditional` A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-WMEVAL-READ-0014](evidence-appendix.md#ea-wmeval-read-0014))
- `conditional` Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-WMEVAL-READ-0011](evidence-appendix.md#ea-wmeval-read-0011))
- `conditional` In the DROID/RoboArena setting, a closed-loop video-world-model evaluator produced a policy ranking that closely matched the real-robot leaderboard across the evaluated policies, supporting policy ra... ([2607.01060](https://arxiv.org/abs/2607.01060) / [EA-WMTASK-2026-0001](evidence-appendix.md#ea-wmtask-2026-0001))
- `limit` PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-WMEVAL-READ-0008](evidence-appendix.md#ea-wmeval-read-0008))
- `limit` World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMEVAL-READ-0015](evidence-appendix.md#ea-wmeval-read-0015))
- `limit` Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-WMEVAL-READ-0013](evidence-appendix.md#ea-wmeval-read-0013))
- `limit` RoboWorld's principal qualitative failures occur after object contact, when manipulated objects may disintegrate, morph unrealistically, or become visually inconsistent, limiting contact-rich manipul... ([2607.01060](https://arxiv.org/abs/2607.01060) / [EA-WMTASK-2026-0002](evidence-appendix.md#ea-wmtask-2026-0002))
- `gap` Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-WMEVAL-READ-0006](evidence-appendix.md#ea-wmeval-read-0006))
- `gap` Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection. ([2605.29360](https://arxiv.org/abs/2605.29360) / [EA-WMEVAL-READ-0004](evidence-appendix.md#ea-wmeval-read-0004))
- `conditional` ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-ALIGN-READ-0006](evidence-appendix.md#ea-align-read-0006))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- `limit` Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- `limit` Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- `limit` TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-ALIGN-READ-0009](evidence-appendix.md#ea-align-read-0009))

## Writer handoff

- Use `$embodied-ai-review-writer` with this brief, the accepted evidence JSONL, and `evidence-appendix.md`.
- The writer loads only the requested style reference and drafts each style independently from this evidence model.
- Generate `trace-map.json`, then pass the writer's editorial quality audit before settlement.

## 引用速查

- **正文引用 = arXiv 论文链接**:`[2606.13877](https://arxiv.org/abs/2606.13877)` 或 `[SIEVE](https://arxiv.org/abs/2607.06442)`。读者点开即达论文。
- 事件级溯源留给 appendix:成稿正文不放 `evidence-appendix.md#...` 事件锚点;需要精确定位(章节/立场/置信)时,读者从 References 或 appendix 查。
- 本简报中每条证据给出 `论文链接 / 事件链接` 对:写作时**取前者入正文**,后者供你核对 locator 与 stance。
- Citation density and visible source format are style-specific; do not force a full bibliography into Xiaohongshu prose.
- 完整证据条目在 [evidence-appendix.md](evidence-appendix.md);事件映射由 `trace-map.json` 保存。
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`
