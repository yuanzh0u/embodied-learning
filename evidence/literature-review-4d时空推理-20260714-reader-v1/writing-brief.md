# Writing Brief: 4D时空推理

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 4D时空推理
- Time range: 2026-01-14..2026-07-14
- Knowledge IDs: `EA-DATA`, `EA-EVAL`, `EA-MODEL`, `EA-SENSOR`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency o... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003)) ⟷ PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and pos... ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- `EA-DATA`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulatio... ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004)) ⟷ DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storag... ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007))
- `EA-DATA`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinem... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005)) ⟷ τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))
- `EA-DATA`: GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic oc... ([2605.17682](https://arxiv.org/abs/2605.17682) / [EA-DATA-READ-0008](evidence-appendix.md#ea-data-read-0008)) ⟷ HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))
- `EA-DATA`: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- `EA-DATA`: MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD o... ([2602.09878](https://arxiv.org/abs/2602.09878) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014)) ⟷ 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012))
- `EA-DATA`: Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a... ([2605.01799](https://arxiv.org/abs/2605.01799) / [EA-DATA-READ-0015](evidence-appendix.md#ea-data-read-0015)) ⟷ PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and pos... ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (15 events)
- [`support`] MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD observation and fuses the generated views into a more complete 3D structure over... ([2602.09878](https://arxiv.org/abs/2602.09878) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014))
- [`support`] Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005))
- [`support`] Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data. ([2605.01799](https://arxiv.org/abs/2605.01799) / [EA-DATA-READ-0015](evidence-appendix.md#ea-data-read-0015))
- [`support`] GEM represents future driving scenes as explicit continuous 4D Gaussian primitives, enabling arbitrary-time semantic occupancy queries and motion planning without fixed-step autoregressive rollout. ([2605.17682](https://arxiv.org/abs/2605.17682) / [EA-DATA-READ-0008](evidence-appendix.md#ea-data-read-0008))
- [`support`] GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004))
- [`support`] Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003))
- [`conditional`] 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012))
- [`conditional`] τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- [`limit`] PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- [`limit`] DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007))
- [`gap`] Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))
- [`gap`] UMI 夹爪手指的力分布会显著改变操作者的任务表现和示教质量，说明数据采集硬件本身是学习管线需要优化的一部分。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012))
- `conditional` τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- `limit` PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- `limit` DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007))
- `gap` Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))
- `gap` UMI 夹爪手指的力分布会显著改变操作者的任务表现和示教质量，说明数据采集硬件本身是学习管线需要优化的一部分。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009))

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
