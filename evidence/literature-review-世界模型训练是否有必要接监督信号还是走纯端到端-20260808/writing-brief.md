# Writing Brief: 世界模型训练是否有必要接监督信号还是走纯端到端

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 世界模型训练是否有必要接监督信号还是走纯端到端
- Time range: 2026-02-09..2026-08-09
- Knowledge IDs: `EA-EVAL`, `EA-MODEL`, `EA-4D`
- Review mode: scoping
- Paper-level sources: 12 / 15 floor (not a cap)
- Coverage and saturation gate: blocked
- Writing readiness: preliminary
- Unresolved checks: coverage-report-missing
- Accepted events: 18

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-WMDATA-READ-0001](evidence-appendix.md#ea-wmdata-read-0001)) ⟷ World-model training and post-training objectives should be tied to downstream action quality rather than intermediate... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMDATA-READ-0006](evidence-appendix.md#ea-wmdata-read-0006))
- `EA-DATA`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulatio... ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-WMDATA-READ-0002](evidence-appendix.md#ea-wmdata-read-0002)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `EA-DATA`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-tra... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-WMDATA-READ-0007](evidence-appendix.md#ea-wmdata-read-0007)) ⟷ World-model training and post-training objectives should be tied to downstream action quality rather than intermediate... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMDATA-READ-0006](evidence-appendix.md#ea-wmdata-read-0006))
- `EA-DATA`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow ta... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-WMDATA-READ-0008](evidence-appendix.md#ea-wmdata-read-0008)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `EA-DATA`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, n... ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-WMDATA-READ-0009](evidence-appendix.md#ea-wmdata-read-0009)) ⟷ World-model training and post-training objectives should be tied to downstream action quality rather than intermediate... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMDATA-READ-0006](evidence-appendix.md#ea-wmdata-read-0006))
- `EA-DATA`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency o... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-WMDATA-READ-0015](evidence-appendix.md#ea-wmdata-read-0015)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `EA-DATA`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency o... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-4D-READ-0003](evidence-appendix.md#ea-4d-read-0003)) ⟷ World-model training and post-training objectives should be tied to downstream action quality rather than intermediate... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMDATA-READ-0006](evidence-appendix.md#ea-wmdata-read-0006))
- `EA-DATA`: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-4D-READ-0013](evidence-appendix.md#ea-4d-read-0013)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (12 events)
- [`support`] A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horiz... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-WMDATA-READ-0007](evidence-appendix.md#ea-wmdata-read-0007))
- [`support`] World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-WMDATA-READ-0009](evidence-appendix.md#ea-wmdata-read-0009))
- [`support`] GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-WMDATA-READ-0002](evidence-appendix.md#ea-wmdata-read-0002))
- [`support`] Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon futur... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-WMDATA-READ-0008](evidence-appendix.md#ea-wmdata-read-0008))
- [`support`] τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-WMDATA-READ-0001](evidence-appendix.md#ea-wmdata-read-0001))
- [`support`] Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-4D-READ-0013](evidence-appendix.md#ea-4d-read-0013))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-4D-READ-0003](evidence-appendix.md#ea-4d-read-0003))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-WMDATA-READ-0015](evidence-appendix.md#ea-wmdata-read-0015))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- [`limit`] World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMDATA-READ-0006](evidence-appendix.md#ea-wmdata-read-0006))
- [`gap`] Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-4D-READ-0001](evidence-appendix.md#ea-4d-read-0001))
- [`gap`] Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-WMDATA-READ-0010](evidence-appendix.md#ea-wmdata-read-0010))

### EA-EVAL (4 events)
- [`support`] GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-WMEVAL-READ-0005](evidence-appendix.md#ea-wmeval-read-0005))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-WMEVAL-READ-0010](evidence-appendix.md#ea-wmeval-read-0010))
- [`limit`] World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMEVAL-READ-0015](evidence-appendix.md#ea-wmeval-read-0015))
- [`gap`] Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection. ([2605.29360](https://arxiv.org/abs/2605.29360) / [EA-WMEVAL-READ-0004](evidence-appendix.md#ea-wmeval-read-0004))

### EA-MODEL (2 events)
- [`limit`] 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0006](evidence-appendix.md#ea-vlabreak-2026-0006))
- [`limit`] 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `limit` World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMDATA-READ-0006](evidence-appendix.md#ea-wmdata-read-0006))
- `gap` Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-4D-READ-0001](evidence-appendix.md#ea-4d-read-0001))
- `gap` Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-WMDATA-READ-0010](evidence-appendix.md#ea-wmdata-read-0010))
- `limit` World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMEVAL-READ-0015](evidence-appendix.md#ea-wmeval-read-0015))
- `gap` Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection. ([2605.29360](https://arxiv.org/abs/2605.29360) / [EA-WMEVAL-READ-0004](evidence-appendix.md#ea-wmeval-read-0004))
- `limit` 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0006](evidence-appendix.md#ea-vlabreak-2026-0006))
- `limit` 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))

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
