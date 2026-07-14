# Writing Brief: 具身数据感知误差溯源

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 具身数据感知误差溯源
- Time range: 2025-07-08..2026-07-08
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `ERR-PATTERN`
- Paper-level sources: 15 / 5 (formal-ready)
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002)) ⟷ VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- `EA-DATA`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001)) ⟷ 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `EA-DATA`: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002)) ⟷ 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `EA-DATA`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `EA-DATA`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DATA-2026-LY-0007](evidence-appendix.md#ea-data-2026-ly-0007)) ⟷ 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (12 events)
- [`support`] 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DATA-2026-LY-0007](evidence-appendix.md#ea-data-2026-ly-0007))
- [`support`] 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001))
- [`support`] 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003))
- [`support`] 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002))
- [`support`] 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- [`conditional`] 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- [`conditional`] 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- [`conditional`] 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- [`conditional`] 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))
- [`limit`] VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))

### EA-EVAL (1 events)
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004))

### EA-SENSOR (1 events)
- [`limit`] 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))

### EA-XEMBODIMENT (1 events)
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- `conditional` 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `conditional` 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `conditional` 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `conditional` 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))
- `limit` VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- `limit` 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

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
