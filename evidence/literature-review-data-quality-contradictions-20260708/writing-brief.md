# Writing Brief: 具身智能数据质量的主要矛盾

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 具身智能数据质量的主要矛盾
- Time range: 2026-01-08..2026-07-08
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-XEMBODIMENT`, `EA-MODEL`, `EA-EVAL`
- Paper-level sources: 34 / 5 (formal-ready)
- Accepted events: 54

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002)) ⟷ VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- `EA-DATA`: 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001)) ⟷ 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- `EA-DATA`: 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005)) ⟷ 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-2026-DQ-0003](evidence-appendix.md#ea-data-2026-dq-0003))
- `EA-DATA`: 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008)) ⟷ 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `EA-DATA`: 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0009](evidence-appendix.md#ea-data-2026-4ddata-0009)) ⟷ 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- `EA-DATA`: 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0017](evidence-appendix.md#ea-data-2026-4ddata-0017)) ⟷ 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006))
- `EA-DATA`: 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。 ([2603.19201](https://arxiv.org/abs/2603.19201) / [EA-TWM-2026-0005](evidence-appendix.md#ea-twm-2026-0005)) ⟷ 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `EA-DATA`: 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-2026-0013](evidence-appendix.md#ea-twm-2026-0013)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (21 events)
- [`support`] 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001))
- [`support`] 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005))
- [`support`] 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。 ([2603.19201](https://arxiv.org/abs/2603.19201) / [EA-TWM-2026-0005](evidence-appendix.md#ea-twm-2026-0005))
- [`support`] 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。 ([2604.07335](https://arxiv.org/abs/2604.07335) / [EA-TWM-2026-0014](evidence-appendix.md#ea-twm-2026-0014))
- [`support`] 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008))
- [`support`] 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0009](evidence-appendix.md#ea-data-2026-4ddata-0009))
- [`support`] 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0017](evidence-appendix.md#ea-data-2026-4ddata-0017))
- [`support`] 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-2026-0013](evidence-appendix.md#ea-twm-2026-0013))
- [`support`] 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002))
- [`conditional`] 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0004](evidence-appendix.md#ea-twm-2026-0004))
- [`conditional`] 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- [`conditional`] 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- [`conditional`] 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006))
- [`conditional`] 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- [`conditional`] 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- [`conditional`] 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-DATA-2026-4DDATA-0016](evidence-appendix.md#ea-data-2026-4ddata-0016))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- [`conditional`] 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-2026-DQ-0003](evidence-appendix.md#ea-data-2026-dq-0003))
- [`limit`] 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- [`limit`] VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- [`gap`] 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0020](evidence-appendix.md#ea-data-2026-4ddata-0020))

### EA-EVAL (8 events)
- [`support`] 触觉世界模型必须在扰动与恢复数据上评估，否则会高估接触丰富任务的稳定性。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-2026-0008](evidence-appendix.md#ea-twm-2026-0008))
- [`support`] 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。 ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-EVAL-2026-4DDATA-0011](evidence-appendix.md#ea-eval-2026-4ddata-0011))
- [`support`] 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-2026-0001](evidence-appendix.md#ea-twm-2026-0001))
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004))
- [`conditional`] 在触觉世界动作模型中，触觉融合需要对接触事件做门控，否则会把稀疏、事件驱动的触觉信号当作持续视觉信号处理。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-2026-0010](evidence-appendix.md#ea-twm-2026-0010))
- [`conditional`] 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-2026-0002](evidence-appendix.md#ea-twm-2026-0002))
- [`limit`] 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-2026-0012](evidence-appendix.md#ea-twm-2026-0012))
- [`gap`] 触觉表征评测正在扩展到大规模全手触觉和自我中心视觉，但多数评测仍停留在表征层，不能直接证明下游机器人性能。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TWM-2026-0015](evidence-appendix.md#ea-twm-2026-0015))

### EA-MODEL (14 events)
- [`support`] 把触觉作为接触 grounding 信号注入世界模型，可以改善被遮挡或视觉混淆场景中的物体持续性、物理一致性和零样本接触规划。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0003](evidence-appendix.md#ea-twm-2026-0003))
- [`support`] 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-MODEL-2026-4DDATA-0003](evidence-appendix.md#ea-model-2026-4ddata-0003))
- [`support`] 触觉世界模型的落地形态正在从被动观测转向预测接触演化并驱动快速反射式控制。 ([2603.19201](https://arxiv.org/abs/2603.19201) / [EA-TWM-2026-0006](evidence-appendix.md#ea-twm-2026-0006))
- [`support`] 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-2026-0009](evidence-appendix.md#ea-twm-2026-0009))
- [`support`] 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-2026-0007](evidence-appendix.md#ea-twm-2026-0007))
- [`support`] 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-2026-0011](evidence-appendix.md#ea-twm-2026-0011))
- [`support`] In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and underdeveloped language-action grounding. ([2606.27295](https://arxiv.org/abs/2606.27295) / [EA-ALIGN-2026-0008](evidence-appendix.md#ea-align-2026-0008))
- [`support`] Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. ([2606.30552](https://arxiv.org/abs/2606.30552) / [EA-ALIGN-2026-0001](evidence-appendix.md#ea-align-2026-0001))
- [`conditional`] 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。 ([2603.15257](https://arxiv.org/abs/2603.15257) / [EA-TWM-2026-0017](evidence-appendix.md#ea-twm-2026-0017))
- [`conditional`] 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-2026-0016](evidence-appendix.md#ea-twm-2026-0016))
- [`limit`] Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixing can cause negative... ([2602.09722](https://arxiv.org/abs/2602.09722) / [EA-ALIGN-2026-0007](evidence-appendix.md#ea-align-2026-0007))
- [`limit`] 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007))
- [`limit`] Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-2026-0002](evidence-appendix.md#ea-align-2026-0002))
- [`limit`] Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-2026-0004](evidence-appendix.md#ea-align-2026-0004))

### EA-SENSOR (9 events)
- [`support`] 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-2026-0018](evidence-appendix.md#ea-twm-2026-0018))
- [`support`] 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-SENSOR-2026-4DDATA-0015](evidence-appendix.md#ea-sensor-2026-4ddata-0015))
- [`support`] 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-SENSOR-2026-4DDATA-0013](evidence-appendix.md#ea-sensor-2026-4ddata-0013))
- [`support`] Dense or sparse visual geometry becomes more useful for manipulation when it is explicitly aligned to task-space actions rather than learned only through downstream policy losses. ([2606.12759](https://arxiv.org/abs/2606.12759) / [EA-ALIGN-2026-0005](evidence-appendix.md#ea-align-2026-0005))
- [`support`] 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 ([2607.05390](https://arxiv.org/abs/2607.05390) / [EA-SENSOR-2026-DQ-0005](evidence-appendix.md#ea-sensor-2026-dq-0005))
- [`conditional`] A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-2026-0006](evidence-appendix.md#ea-align-2026-0006))
- [`limit`] For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self-occluded. ([2606.15516](https://arxiv.org/abs/2606.15516) / [EA-ALIGN-2026-0009](evidence-appendix.md#ea-align-2026-0009))
- [`limit`] 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))
- [`gap`] 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-SENSOR-2026-4DDATA-0012](evidence-appendix.md#ea-sensor-2026-4ddata-0012))

### EA-XEMBODIMENT (2 events)
- [`support`] A VLA that inherits visual and linguistic priors from a VLM still lacks an explicit physical motion prior; pretraining the action module on unconditioned trajectories can reduce the burden of learnin... ([2606.26095](https://arxiv.org/abs/2606.26095) / [EA-ALIGN-2026-0003](evidence-appendix.md#ea-align-2026-0003))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0004](evidence-appendix.md#ea-twm-2026-0004))
- `conditional` 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- `conditional` 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `conditional` 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006))
- `conditional` 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `conditional` 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- `conditional` 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-DATA-2026-4DDATA-0016](evidence-appendix.md#ea-data-2026-4ddata-0016))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `conditional` 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-2026-DQ-0003](evidence-appendix.md#ea-data-2026-dq-0003))
- `limit` 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- `limit` VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- `gap` 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0020](evidence-appendix.md#ea-data-2026-4ddata-0020))
- `conditional` 在触觉世界动作模型中，触觉融合需要对接触事件做门控，否则会把稀疏、事件驱动的触觉信号当作持续视觉信号处理。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-2026-0010](evidence-appendix.md#ea-twm-2026-0010))
- `conditional` 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-2026-0002](evidence-appendix.md#ea-twm-2026-0002))
- `limit` 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-2026-0012](evidence-appendix.md#ea-twm-2026-0012))
- `gap` 触觉表征评测正在扩展到大规模全手触觉和自我中心视觉，但多数评测仍停留在表征层，不能直接证明下游机器人性能。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TWM-2026-0015](evidence-appendix.md#ea-twm-2026-0015))
- `conditional` 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。 ([2603.15257](https://arxiv.org/abs/2603.15257) / [EA-TWM-2026-0017](evidence-appendix.md#ea-twm-2026-0017))
- `conditional` 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-2026-0016](evidence-appendix.md#ea-twm-2026-0016))
- `limit` Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixing can cause negative... ([2602.09722](https://arxiv.org/abs/2602.09722) / [EA-ALIGN-2026-0007](evidence-appendix.md#ea-align-2026-0007))
- `limit` 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007))
- `limit` Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-2026-0002](evidence-appendix.md#ea-align-2026-0002))
- `limit` Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-2026-0004](evidence-appendix.md#ea-align-2026-0004))
- `conditional` A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-2026-0006](evidence-appendix.md#ea-align-2026-0006))
- `limit` For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self-occluded. ([2606.15516](https://arxiv.org/abs/2606.15516) / [EA-ALIGN-2026-0009](evidence-appendix.md#ea-align-2026-0009))
- `limit` 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))
- `gap` 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-SENSOR-2026-4DDATA-0012](evidence-appendix.md#ea-sensor-2026-4ddata-0012))
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
