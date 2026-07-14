# Writing Brief: 4D时空推理

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 4D时空推理
- Time range: 2026-01-14..2026-07-14
- Knowledge IDs: `EA-4D`, `EA-DATA`, `EA-EVAL`, `EA-MODEL`, `EA-SENSOR`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 40

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001)) ⟷ 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- `EA-DATA`: 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005)) ⟷ Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4D-0007](evidence-appendix.md#ea-data-2026-4d-0007))
- `EA-DATA`: 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008)) ⟷ τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demo... ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4D-0011](evidence-appendix.md#ea-data-2026-4d-0011))
- `EA-DATA`: 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0009](evidence-appendix.md#ea-data-2026-4ddata-0009)) ⟷ 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `EA-DATA`: 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0017](evidence-appendix.md#ea-data-2026-4ddata-0017)) ⟷ 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- `EA-EVAL`: Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-... ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-EVAL-2026-4D-0004](evidence-appendix.md#ea-eval-2026-4d-0004)) ⟷ τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but... ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-EVAL-2026-4D-0012](evidence-appendix.md#ea-eval-2026-4d-0012))
- `EA-EVAL`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinem... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-EVAL-2026-4D-0006](evidence-appendix.md#ea-eval-2026-4d-0006)) ⟷ WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable a... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-EVAL-2026-4D-0014](evidence-appendix.md#ea-eval-2026-4d-0014))
- `EA-EVAL`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency o... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-EVAL-2026-4D-0013](evidence-appendix.md#ea-eval-2026-4d-0013)) ⟷ ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real... ([2603.13788](https://arxiv.org/abs/2603.13788) / [EA-EVAL-2026-4D-0002](evidence-appendix.md#ea-eval-2026-4d-0002))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (16 events)
- [`support`] 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001))
- [`support`] 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005))
- [`support`] 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008))
- [`support`] 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0009](evidence-appendix.md#ea-data-2026-4ddata-0009))
- [`support`] 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0017](evidence-appendix.md#ea-data-2026-4ddata-0017))
- [`conditional`] 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- [`conditional`] 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- [`conditional`] Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial constraints and motion p... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4D-0007](evidence-appendix.md#ea-data-2026-4d-0007))
- [`conditional`] 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006))
- [`conditional`] τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding. ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4D-0011](evidence-appendix.md#ea-data-2026-4d-0011))
- [`conditional`] 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- [`conditional`] 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- [`conditional`] 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-DATA-2026-4DDATA-0016](evidence-appendix.md#ea-data-2026-4ddata-0016))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- [`limit`] 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- [`gap`] 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0020](evidence-appendix.md#ea-data-2026-4ddata-0020))

### EA-EVAL (8 events)
- [`support`] Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only prediction, or dense depth... ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-EVAL-2026-4D-0004](evidence-appendix.md#ea-eval-2026-4d-0004))
- [`support`] Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-EVAL-2026-4D-0006](evidence-appendix.md#ea-eval-2026-4d-0006))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-EVAL-2026-4D-0013](evidence-appendix.md#ea-eval-2026-4d-0013))
- [`support`] 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。 ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-EVAL-2026-4DDATA-0011](evidence-appendix.md#ea-eval-2026-4ddata-0011))
- [`conditional`] ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset, masking pipeline,... ([2603.13788](https://arxiv.org/abs/2603.13788) / [EA-EVAL-2026-4D-0002](evidence-appendix.md#ea-eval-2026-4d-0002))
- [`conditional`] τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensing, uncertainty estimation, longer horiz... ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-EVAL-2026-4D-0012](evidence-appendix.md#ea-eval-2026-4d-0012))
- [`limit`] WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, data coverage, and nois... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-EVAL-2026-4D-0014](evidence-appendix.md#ea-eval-2026-4d-0014))
- [`gap`] EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual scenes. ([2603.15467](https://arxiv.org/abs/2603.15467) / [EA-EVAL-2026-4D-0020](evidence-appendix.md#ea-eval-2026-4d-0020))

### EA-MODEL (8 events)
- [`support`] Pri4R treats 4D geometry as a training-time privileged signal: VLA backbones learn future 3D point tracks so their action representations encode how scene geometry evolves over time. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-MODEL-2026-4D-0003](evidence-appendix.md#ea-model-2026-4d-0003))
- [`support`] 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-MODEL-2026-4DDATA-0003](evidence-appendix.md#ea-model-2026-4ddata-0003))
- [`support`] ST-VLA frames 4D spatiotemporal reasoning as a bridge between high-level VLA semantics and continuous robot control by lifting 2D guidance into 3D trajectories and 4D temporal context. ([2603.13788](https://arxiv.org/abs/2603.13788) / [EA-MODEL-2026-4D-0001](evidence-appendix.md#ea-model-2026-4d-0001))
- [`support`] GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4D-0009](evidence-appendix.md#ea-model-2026-4d-0009))
- [`support`] τ0-WM treats 4D-style predictive reasoning as a deployment-time loop: propose executable action chunks, imagine action-conditioned futures, score progress, then revise low-quality candidates before e... ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-MODEL-2026-4D-0010](evidence-appendix.md#ea-model-2026-4d-0010))
- [`limit`] GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences over time. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4D-0008](evidence-appendix.md#ea-model-2026-4d-0008))
- [`limit`] 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007))
- [`gap`] Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-MODEL-2026-4D-0005](evidence-appendix.md#ea-model-2026-4d-0005))

### EA-SENSOR (8 events)
- [`support`] PredictiveGraphs shows a relational route to 4D reasoning: embed temporal persistence filters in a 3D scene graph so robots can query likely future object-receptacle states and plan navigation accord... ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-SENSOR-2026-4D-0015](evidence-appendix.md#ea-sensor-2026-4d-0015))
- [`support`] GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autoregressive rollout. ([2605.17682](https://arxiv.org/abs/2605.17682) / [EA-SENSOR-2026-4D-0019](evidence-appendix.md#ea-sensor-2026-4d-0019))
- [`support`] DGSG-Mind combines dynamic 3D Gaussian mapping with scene graphs so that embodied agents can update object-level topology and reason over spatial-semantic relations in changing environments. ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-SENSOR-2026-4D-0017](evidence-appendix.md#ea-sensor-2026-4d-0017))
- [`support`] 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-SENSOR-2026-4DDATA-0015](evidence-appendix.md#ea-sensor-2026-4ddata-0015))
- [`support`] 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-SENSOR-2026-4DDATA-0013](evidence-appendix.md#ea-sensor-2026-4ddata-0013))
- [`limit`] PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-SENSOR-2026-4D-0016](evidence-appendix.md#ea-sensor-2026-4d-0016))
- [`limit`] DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-SENSOR-2026-4D-0018](evidence-appendix.md#ea-sensor-2026-4d-0018))
- [`gap`] 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-SENSOR-2026-4DDATA-0012](evidence-appendix.md#ea-sensor-2026-4ddata-0012))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004))
- `conditional` 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `conditional` Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial constraints and motion p... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4D-0007](evidence-appendix.md#ea-data-2026-4d-0007))
- `conditional` 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006))
- `conditional` τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding. ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4D-0011](evidence-appendix.md#ea-data-2026-4d-0011))
- `conditional` 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `conditional` 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- `conditional` 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-DATA-2026-4DDATA-0016](evidence-appendix.md#ea-data-2026-4ddata-0016))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `limit` 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019))
- `gap` 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-4DDATA-0020](evidence-appendix.md#ea-data-2026-4ddata-0020))
- `conditional` ST-VLA reports material manipulation gains from 3D-4D reasoning, including higher zero-shot success in RLBench and real-world manipulation, but its evidence is tied to its dataset, masking pipeline,... ([2603.13788](https://arxiv.org/abs/2603.13788) / [EA-EVAL-2026-4D-0002](evidence-appendix.md#ea-eval-2026-4d-0002))
- `conditional` τ0-WM reports that heterogeneous pretraining and test-time world-model computation improve real-robot manipulation, but the paper also identifies tactile sensing, uncertainty estimation, longer horiz... ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-EVAL-2026-4D-0012](evidence-appendix.md#ea-eval-2026-4d-0012))
- `limit` WEAVER's authors explicitly limit visual world models: partial observability, missing contact/force state, deformable and granular dynamics, latency-limited planning horizons, data coverage, and nois... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-EVAL-2026-4D-0014](evidence-appendix.md#ea-eval-2026-4d-0014))
- `gap` EscapeCraft-4D shows that 4D reasoning evaluation should include transient evidence, irreversible timing constraints, and cross-modal active perception, not only static 3D visual scenes. ([2603.15467](https://arxiv.org/abs/2603.15467) / [EA-EVAL-2026-4D-0020](evidence-appendix.md#ea-eval-2026-4d-0020))
- `limit` GEM-4D identifies a core failure mode of video world models for robots: visually plausible futures can still be unusable when they do not preserve consistent 3D correspondences over time. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4D-0008](evidence-appendix.md#ea-model-2026-4d-0008))
- `limit` 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007))
- `gap` Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-MODEL-2026-4D-0005](evidence-appendix.md#ea-model-2026-4d-0005))
- `limit` PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-SENSOR-2026-4D-0016](evidence-appendix.md#ea-sensor-2026-4d-0016))
- `limit` DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-SENSOR-2026-4D-0018](evidence-appendix.md#ea-sensor-2026-4d-0018))
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
