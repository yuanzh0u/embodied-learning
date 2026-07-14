# Writing Brief: Sparse language, dense vision, and continuous action alignment in VLA systems

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: Sparse language, dense vision, and continuous action alignment in VLA systems
- Time range: 2025-12-30..2026-06-30
- Knowledge IDs: `EA-MODEL`, `EA-SENSOR`, `EA-XEMBODIMENT`
- Paper-level sources: 10 / 5 (formal-ready)
- Accepted events: 10

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-MODEL`: Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platfo... ([2606.30552](https://arxiv.org/abs/2606.30552) / [EA-ALIGN-2026-0001](evidence-appendix.md#ea-align-2026-0001)) ⟷ Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, tem... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-2026-0002](evidence-appendix.md#ea-align-2026-0002))
- `EA-MODEL`: In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action sign... ([2606.27295](https://arxiv.org/abs/2606.27295) / [EA-ALIGN-2026-0008](evidence-appendix.md#ea-align-2026-0008)) ⟷ Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back int... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-2026-0004](evidence-appendix.md#ea-align-2026-0004))
- `EA-SENSOR`: Dense or sparse visual geometry becomes more useful for manipulation when it is explicitly aligned to task-space action... ([2606.12759](https://arxiv.org/abs/2606.12759) / [EA-ALIGN-2026-0005](evidence-appendix.md#ea-align-2026-0005)) ⟷ For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comp... ([2606.15516](https://arxiv.org/abs/2606.15516) / [EA-ALIGN-2026-0009](evidence-appendix.md#ea-align-2026-0009))
- `EA-XEMBODIMENT`: A VLA that inherits visual and linguistic priors from a VLM still lacks an explicit physical motion prior; pretraining... ([2606.26095](https://arxiv.org/abs/2606.26095) / [EA-ALIGN-2026-0003](evidence-appendix.md#ea-align-2026-0003)) ⟷ A recorded robot action is not a universal supervision signal: the same command can produce different motions across co... ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-MODEL (5 events)
- [`support`] In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and underdeveloped language-action grounding. ([2606.27295](https://arxiv.org/abs/2606.27295) / [EA-ALIGN-2026-0008](evidence-appendix.md#ea-align-2026-0008))
- [`support`] Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. ([2606.30552](https://arxiv.org/abs/2606.30552) / [EA-ALIGN-2026-0001](evidence-appendix.md#ea-align-2026-0001))
- [`limit`] Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixing can cause negative... ([2602.09722](https://arxiv.org/abs/2602.09722) / [EA-ALIGN-2026-0007](evidence-appendix.md#ea-align-2026-0007))
- [`limit`] Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-2026-0002](evidence-appendix.md#ea-align-2026-0002))
- [`limit`] Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-2026-0004](evidence-appendix.md#ea-align-2026-0004))

### EA-SENSOR (3 events)
- [`support`] Dense or sparse visual geometry becomes more useful for manipulation when it is explicitly aligned to task-space actions rather than learned only through downstream policy losses. ([2606.12759](https://arxiv.org/abs/2606.12759) / [EA-ALIGN-2026-0005](evidence-appendix.md#ea-align-2026-0005))
- [`conditional`] A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-2026-0006](evidence-appendix.md#ea-align-2026-0006))
- [`limit`] For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self-occluded. ([2606.15516](https://arxiv.org/abs/2606.15516) / [EA-ALIGN-2026-0009](evidence-appendix.md#ea-align-2026-0009))

### EA-XEMBODIMENT (2 events)
- [`support`] A VLA that inherits visual and linguistic priors from a VLM still lacks an explicit physical motion prior; pretraining the action module on unconditioned trajectories can reduce the burden of learnin... ([2606.26095](https://arxiv.org/abs/2606.26095) / [EA-ALIGN-2026-0003](evidence-appendix.md#ea-align-2026-0003))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `limit` Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixing can cause negative... ([2602.09722](https://arxiv.org/abs/2602.09722) / [EA-ALIGN-2026-0007](evidence-appendix.md#ea-align-2026-0007))
- `limit` Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-2026-0002](evidence-appendix.md#ea-align-2026-0002))
- `limit` Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-2026-0004](evidence-appendix.md#ea-align-2026-0004))
- `conditional` A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-2026-0006](evidence-appendix.md#ea-align-2026-0006))
- `limit` For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self-occluded. ([2606.15516](https://arxiv.org/abs/2606.15516) / [EA-ALIGN-2026-0009](evidence-appendix.md#ea-align-2026-0009))
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
