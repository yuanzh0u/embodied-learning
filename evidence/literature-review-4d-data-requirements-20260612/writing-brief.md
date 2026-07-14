# Writing Brief: 4D时空推理对数据的需求

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 4D时空推理对数据的需求
- Time range: 2025-12-12..2026-06-12
- Knowledge IDs: `EA-DATA`, `EA-EVAL`, `EA-MODEL`, `EA-SENSOR`
- Paper-level sources: 10 / 5 (formal-ready)
- Accepted events: 20

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001)) ⟷ 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- `EA-DATA`: 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005)) ⟷ 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `EA-DATA`: 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008)) ⟷ 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- `EA-DATA`: 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0009](evidence-appendix.md#ea-data-2026-4ddata-0009)) ⟷ 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006))
- `EA-DATA`: 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0017](evidence-appendix.md#ea-data-2026-4ddata-0017)) ⟷ 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `EA-MODEL`: 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-MODEL-2026-4DDATA-0003](evidence-appendix.md#ea-model-2026-4ddata-0003)) ⟷ 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (14 events)
- [`support`] 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001))
- [`support`] 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005))
- [`support`] 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008))
- [`support`] 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0009](evidence-appendix.md#ea-data-2026-4ddata-0009))
- [`support`] 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0017](evidence-appendix.md#ea-data-2026-4ddata-0017))
- [`conditional`] 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- [`conditional`] 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- [`conditional`] 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006))
- [`conditional`] 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- [`conditional`] 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- [`conditional`] 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-DATA-2026-4DDATA-0016](evidence-appendix.md#ea-data-2026-4ddata-0016))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- [`limit`] 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- [`gap`] 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0020](evidence-appendix.md#ea-data-2026-4ddata-0020))

### EA-EVAL (1 events)
- [`support`] 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。 ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-EVAL-2026-4DDATA-0011](evidence-appendix.md#ea-eval-2026-4ddata-0011))

### EA-MODEL (2 events)
- [`support`] 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-MODEL-2026-4DDATA-0003](evidence-appendix.md#ea-model-2026-4ddata-0003))
- [`limit`] 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007))

### EA-SENSOR (3 events)
- [`support`] 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-SENSOR-2026-4DDATA-0015](evidence-appendix.md#ea-sensor-2026-4ddata-0015))
- [`support`] 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-SENSOR-2026-4DDATA-0013](evidence-appendix.md#ea-sensor-2026-4ddata-0013))
- [`gap`] 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-SENSOR-2026-4DDATA-0012](evidence-appendix.md#ea-sensor-2026-4ddata-0012))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- `conditional` 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `conditional` 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006))
- `conditional` 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `conditional` 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- `conditional` 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-DATA-2026-4DDATA-0016](evidence-appendix.md#ea-data-2026-4ddata-0016))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `limit` 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- `gap` 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0020](evidence-appendix.md#ea-data-2026-4ddata-0020))
- `limit` 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007))
- `gap` 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-SENSOR-2026-4DDATA-0012](evidence-appendix.md#ea-sensor-2026-4ddata-0012))

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
