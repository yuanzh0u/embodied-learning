# Writing Brief: 世界模型需要什么样的训练数据

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 世界模型需要什么样的训练数据
- Time range: 2025-12-11..2026-06-11
- Knowledge IDs: `EA-DATA`, `EA-MODEL`, `EA-EVAL`
- Paper-level sources: 14 / 5 (formal-ready)
- Accepted events: 14

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-tra... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-DATA-2026-WMDATA-0001](evidence-appendix.md#ea-data-2026-wmdata-0001)) ⟷ Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should ex... ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011))
- `EA-DATA`: Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleopera... ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-WMDATA-0002](evidence-appendix.md#ea-data-2026-wmdata-0002)) ⟷ Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-2026-WMDATA-0004](evidence-appendix.md#ea-data-2026-wmdata-0004))
- `EA-DATA`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, n... ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-DATA-2026-WMDATA-0003](evidence-appendix.md#ea-data-2026-wmdata-0003)) ⟷ Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation de... ([2512.11797](https://arxiv.org/abs/2512.11797) / [EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005))
- `EA-DATA`: A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, c... ([2606.00113](https://arxiv.org/abs/2606.00113) / [EA-DATA-2026-WMDATA-0014](evidence-appendix.md#ea-data-2026-wmdata-0014)) ⟷ A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neura... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-DATA-2026-WMDATA-0006](evidence-appendix.md#ea-data-2026-wmdata-0006))
- `EA-MODEL`: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, c... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-MODEL-2026-WMDATA-0007](evidence-appendix.md#ea-model-2026-wmdata-0007)) ⟷ World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still b... ([2606.12217](https://arxiv.org/abs/2606.12217) / [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010))
- `EA-MODEL`: World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D corres... ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-WMDATA-0008](evidence-appendix.md#ea-model-2026-wmdata-0008)) ⟷ World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still b... ([2606.12217](https://arxiv.org/abs/2606.12217) / [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010))
- `EA-MODEL`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow ta... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-MODEL-2026-WMDATA-0009](evidence-appendix.md#ea-model-2026-wmdata-0009)) ⟷ World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still b... ([2606.12217](https://arxiv.org/abs/2606.12217) / [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (9 events)
- [`support`] A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horiz... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-DATA-2026-WMDATA-0001](evidence-appendix.md#ea-data-2026-wmdata-0001))
- [`support`] World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-DATA-2026-WMDATA-0003](evidence-appendix.md#ea-data-2026-wmdata-0003))
- [`support`] A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under intervention, with modalities beyond RGB... ([2606.00113](https://arxiv.org/abs/2606.00113) / [EA-DATA-2026-WMDATA-0014](evidence-appendix.md#ea-data-2026-wmdata-0014))
- [`support`] Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations, broad egocentric human videos, and roll... ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-WMDATA-0002](evidence-appendix.md#ea-data-2026-wmdata-0002))
- [`conditional`] Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation demonstrations, because off-the-shelf generative models can hallucinate robot bodi... ([2512.11797](https://arxiv.org/abs/2512.11797) / [EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005))
- [`conditional`] A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-DATA-2026-WMDATA-0006](evidence-appendix.md#ea-data-2026-wmdata-0006))
- [`conditional`] Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-2026-WMDATA-0004](evidence-appendix.md#ea-data-2026-wmdata-0004))
- [`conditional`] Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DATA-2026-WMDATA-0012](evidence-appendix.md#ea-data-2026-wmdata-0012))
- [`limit`] Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011))

### EA-EVAL (1 events)
- [`limit`] World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-EVAL-2026-WMDATA-0013](evidence-appendix.md#ea-eval-2026-wmdata-0013))

### EA-MODEL (4 events)
- [`support`] World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-WMDATA-0008](evidence-appendix.md#ea-model-2026-wmdata-0008))
- [`support`] Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon futur... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-MODEL-2026-WMDATA-0009](evidence-appendix.md#ea-model-2026-wmdata-0009))
- [`support`] Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information do... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-MODEL-2026-WMDATA-0007](evidence-appendix.md#ea-model-2026-wmdata-0007))
- [`limit`] World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to task-relevant interac... ([2606.12217](https://arxiv.org/abs/2606.12217) / [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation demonstrations, because off-the-shelf generative models can hallucinate robot bodi... ([2512.11797](https://arxiv.org/abs/2512.11797) / [EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005))
- `conditional` A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-DATA-2026-WMDATA-0006](evidence-appendix.md#ea-data-2026-wmdata-0006))
- `conditional` Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-2026-WMDATA-0004](evidence-appendix.md#ea-data-2026-wmdata-0004))
- `conditional` Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DATA-2026-WMDATA-0012](evidence-appendix.md#ea-data-2026-wmdata-0012))
- `limit` Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011))
- `limit` World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-EVAL-2026-WMDATA-0013](evidence-appendix.md#ea-eval-2026-wmdata-0013))
- `limit` World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to task-relevant interac... ([2606.12217](https://arxiv.org/abs/2606.12217) / [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010))

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
