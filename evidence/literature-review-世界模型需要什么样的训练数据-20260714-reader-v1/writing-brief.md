# Writing Brief: 世界模型需要什么样的训练数据

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 世界模型需要什么样的训练数据
- Time range: 2026-01-14..2026-07-14
- Knowledge IDs: `EA-DATA`, `EA-MODEL`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001)) ⟷ World-model training and post-training objectives should be tied to downstream action quality rather than intermediate... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- `EA-DATA`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulatio... ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002)) ⟷ PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and pos... ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013))
- `EA-DATA`: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, c... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003)) ⟷ DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storag... ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014))
- `EA-DATA`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-tra... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007)) ⟷ Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004))
- `EA-DATA`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow ta... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-DATA-READ-0008](evidence-appendix.md#ea-data-read-0008)) ⟷ A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neura... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005))
- `EA-DATA`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, n... ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009)) ⟷ For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persis... ([2602.15549](https://arxiv.org/abs/2602.15549) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- `EA-DATA`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinem... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012)) ⟷ World-model training and post-training objectives should be tied to downstream action quality rather than intermediate... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- `EA-DATA`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency o... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-DATA-READ-0015](evidence-appendix.md#ea-data-read-0015)) ⟷ PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and pos... ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (15 events)
- [`support`] A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horiz... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007))
- [`support`] Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012))
- [`support`] World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009))
- [`support`] GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))
- [`support`] Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon futur... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-DATA-READ-0008](evidence-appendix.md#ea-data-read-0008))
- [`support`] Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information do... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003))
- [`support`] τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-DATA-READ-0015](evidence-appendix.md#ea-data-read-0015))
- [`conditional`] For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before exec... ([2602.15549](https://arxiv.org/abs/2602.15549) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- [`conditional`] A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005))
- [`conditional`] Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004))
- [`limit`] PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013))
- [`limit`] World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- [`limit`] DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014))
- [`gap`] Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before exec... ([2602.15549](https://arxiv.org/abs/2602.15549) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- `conditional` A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005))
- `conditional` Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004))
- `limit` PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013))
- `limit` World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- `limit` DGSG-Mind still depends on pose quality for initial reconstruction and faces scalability limits from 3D Gaussian storage and GPU memory. ([2605.29879](https://arxiv.org/abs/2605.29879) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014))
- `gap` Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))

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
