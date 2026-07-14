# Writing Brief: Sparse language, dense vision, and continuous action alignment in VLA systems

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: Sparse language, dense vision, and continuous action alignment in VLA systems
- Time range: 2026-01-14..2026-07-14
- Knowledge IDs: `EA-MODEL`, `EA-SENSOR`, `EA-XEMBODIMENT`, `EA-ALIGN`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-MODEL`: Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platfo... ([2606.30552](https://arxiv.org/abs/2606.30552) / [EA-ALIGN-READ-0005](evidence-appendix.md#ea-align-read-0005)) ⟷ A recorded robot action is not a universal supervision signal: the same command can produce different motions across co... ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- `EA-MODEL`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-ALIGN-READ-0012](evidence-appendix.md#ea-align-read-0012)) ⟷ Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back int... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- `EA-MODEL`: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-ALIGN-READ-0013](evidence-appendix.md#ea-align-read-0013)) ⟷ Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, tem... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- `EA-MODEL`: 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 ([2605.00080](https://arxiv.org/abs/2605.00080) / [EA-ALIGN-READ-0014](evidence-appendix.md#ea-align-read-0014)) ⟷ TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-ALIGN-READ-0009](evidence-appendix.md#ea-align-read-0009))
- `EA-MODEL`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-ALIGN-READ-0015](evidence-appendix.md#ea-align-read-0015)) ⟷ A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task groun... ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-READ-0002](evidence-appendix.md#ea-align-read-0002))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-MODEL (15 events)
- [`support`] 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-ALIGN-READ-0013](evidence-appendix.md#ea-align-read-0013))
- [`support`] 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 ([2605.00080](https://arxiv.org/abs/2605.00080) / [EA-ALIGN-READ-0014](evidence-appendix.md#ea-align-read-0014))
- [`support`] DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-ALIGN-READ-0012](evidence-appendix.md#ea-align-read-0012))
- [`support`] 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-ALIGN-READ-0015](evidence-appendix.md#ea-align-read-0015))
- [`support`] Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. ([2606.30552](https://arxiv.org/abs/2606.30552) / [EA-ALIGN-READ-0005](evidence-appendix.md#ea-align-read-0005))
- [`conditional`] ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-ALIGN-READ-0010](evidence-appendix.md#ea-align-read-0010))
- [`conditional`] τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-ALIGN-READ-0011](evidence-appendix.md#ea-align-read-0011))
- [`conditional`] ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-ALIGN-READ-0006](evidence-appendix.md#ea-align-read-0006))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-ALIGN-READ-0007](evidence-appendix.md#ea-align-read-0007))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-ALIGN-READ-0008](evidence-appendix.md#ea-align-read-0008))
- [`conditional`] A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-READ-0002](evidence-appendix.md#ea-align-read-0002))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- [`limit`] Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- [`limit`] Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-ALIGN-READ-0009](evidence-appendix.md#ea-align-read-0009))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-ALIGN-READ-0010](evidence-appendix.md#ea-align-read-0010))
- `conditional` τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-ALIGN-READ-0011](evidence-appendix.md#ea-align-read-0011))
- `conditional` ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-ALIGN-READ-0006](evidence-appendix.md#ea-align-read-0006))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-ALIGN-READ-0007](evidence-appendix.md#ea-align-read-0007))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-ALIGN-READ-0008](evidence-appendix.md#ea-align-read-0008))
- `conditional` A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-READ-0002](evidence-appendix.md#ea-align-read-0002))
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
- Registered sources: not loaded
