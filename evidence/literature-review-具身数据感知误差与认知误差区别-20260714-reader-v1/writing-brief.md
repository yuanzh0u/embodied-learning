# Writing Brief: 具身数据感知误差与认知误差区别

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 具身数据感知误差与认知误差区别
- Time range: 2026-01-14..2026-07-14
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `EA-MODEL`, `ERR-EMBODIED`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-READ-0008](evidence-appendix.md#ea-data-read-0008)) ⟷ TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))
- `EA-DATA`: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009)) ⟷ A recorded robot action is not a universal supervision signal: the same command can produce different motions across co... ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007))
- `EA-DATA`: 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 ([2605.00080](https://arxiv.org/abs/2605.00080) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010)) ⟷ ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))
- `EA-DATA`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011)) ⟷ HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003))
- `EA-DATA`: ProbeAct 的探针实验表明，扰动下 VLA 视觉骨干仍保留目标物空间表示，而失败集中在动作头回落到记忆的训练轨迹。 ([2606.09740](https://arxiv.org/abs/2606.09740) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004))
- `EA-DATA`: 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 ([2607.00673](https://arxiv.org/abs/2607.00673) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013)) ⟷ ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005))
- `EA-DATA`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014)) ⟷ τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- `EA-DATA`: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-READ-0015](evidence-appendix.md#ea-data-read-0015)) ⟷ TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (15 events)
- [`support`] 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009))
- [`support`] 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 ([2605.00080](https://arxiv.org/abs/2605.00080) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))
- [`support`] DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-READ-0008](evidence-appendix.md#ea-data-read-0008))
- [`support`] 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- [`support`] ProbeAct 的探针实验表明，扰动下 VLA 视觉骨干仍保留目标物空间表示，而失败集中在动作头回落到记忆的训练轨迹。 ([2606.09740](https://arxiv.org/abs/2606.09740) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012))
- [`support`] 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 ([2607.00673](https://arxiv.org/abs/2607.00673) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013))
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014))
- [`support`] Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-READ-0015](evidence-appendix.md#ea-data-read-0015))
- [`conditional`] ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005))
- [`conditional`] τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- [`conditional`] ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005))
- `conditional` τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- `conditional` ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007))
- `limit` TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))

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
