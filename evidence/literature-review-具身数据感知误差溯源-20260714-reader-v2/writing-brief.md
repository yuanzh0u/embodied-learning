# Writing Brief: 具身数据感知误差溯源

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 具身数据感知误差溯源
- Time range: 2025-07-14..2026-07-14
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `ERR-PATTERN`, `ERR-EMBODIED`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [ERR-TRACE-READ-0010](evidence-appendix.md#err-trace-read-0010)) ⟷ TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [ERR-TRACE-READ-0001](evidence-appendix.md#err-trace-read-0001))
- `EA-DATA`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [ERR-TRACE-READ-0011](evidence-appendix.md#err-trace-read-0011)) ⟷ SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [ERR-TRACE-READ-0004](evidence-appendix.md#err-trace-read-0004))
- `EA-DATA`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [ERR-TRACE-READ-0012](evidence-appendix.md#err-trace-read-0012)) ⟷ A recorded robot action is not a universal supervision signal: the same command can produce different motions across co... ([2606.24049](https://arxiv.org/abs/2606.24049) / [ERR-TRACE-READ-0009](evidence-appendix.md#err-trace-read-0009))
- `EA-DATA`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [ERR-TRACE-READ-0013](evidence-appendix.md#err-trace-read-0013)) ⟷ 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [ERR-TRACE-READ-0015](evidence-appendix.md#err-trace-read-0015))
- `EA-DATA`: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [ERR-TRACE-READ-0014](evidence-appendix.md#err-trace-read-0014)) ⟷ HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [ERR-TRACE-READ-0002](evidence-appendix.md#err-trace-read-0002))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (15 events)
- [`support`] 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [ERR-TRACE-READ-0010](evidence-appendix.md#err-trace-read-0010))
- [`support`] 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [ERR-TRACE-READ-0011](evidence-appendix.md#err-trace-read-0011))
- [`support`] DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [ERR-TRACE-READ-0012](evidence-appendix.md#err-trace-read-0012))
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [ERR-TRACE-READ-0013](evidence-appendix.md#err-trace-read-0013))
- [`support`] Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [ERR-TRACE-READ-0014](evidence-appendix.md#err-trace-read-0014))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [ERR-TRACE-READ-0005](evidence-appendix.md#err-trace-read-0005))
- [`conditional`] 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [ERR-TRACE-READ-0007](evidence-appendix.md#err-trace-read-0007))
- [`conditional`] τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [ERR-TRACE-READ-0008](evidence-appendix.md#err-trace-read-0008))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [ERR-TRACE-READ-0002](evidence-appendix.md#err-trace-read-0002))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [ERR-TRACE-READ-0003](evidence-appendix.md#err-trace-read-0003))
- [`conditional`] 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [ERR-TRACE-READ-0006](evidence-appendix.md#err-trace-read-0006))
- [`limit`] 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [ERR-TRACE-READ-0015](evidence-appendix.md#err-trace-read-0015))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [ERR-TRACE-READ-0009](evidence-appendix.md#err-trace-read-0009))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [ERR-TRACE-READ-0001](evidence-appendix.md#err-trace-read-0001))
- [`limit`] SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [ERR-TRACE-READ-0004](evidence-appendix.md#err-trace-read-0004))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [ERR-TRACE-READ-0005](evidence-appendix.md#err-trace-read-0005))
- `conditional` 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [ERR-TRACE-READ-0007](evidence-appendix.md#err-trace-read-0007))
- `conditional` τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [ERR-TRACE-READ-0008](evidence-appendix.md#err-trace-read-0008))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [ERR-TRACE-READ-0002](evidence-appendix.md#err-trace-read-0002))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [ERR-TRACE-READ-0003](evidence-appendix.md#err-trace-read-0003))
- `conditional` 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [ERR-TRACE-READ-0006](evidence-appendix.md#err-trace-read-0006))
- `limit` 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [ERR-TRACE-READ-0015](evidence-appendix.md#err-trace-read-0015))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [ERR-TRACE-READ-0009](evidence-appendix.md#err-trace-read-0009))
- `limit` TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [ERR-TRACE-READ-0001](evidence-appendix.md#err-trace-read-0001))
- `limit` SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [ERR-TRACE-READ-0004](evidence-appendix.md#err-trace-read-0004))

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
