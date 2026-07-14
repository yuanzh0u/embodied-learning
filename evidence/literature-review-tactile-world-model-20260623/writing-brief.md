# Writing Brief: 触觉世界模型

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 触觉世界模型
- Time range: 2025-12-23..2026-06-23
- Knowledge IDs: `EA-DATA`, `EA-EVAL`, `EA-MODEL`, `EA-SENSOR`
- Paper-level sources: 11 / 5 (formal-ready)
- Accepted events: 18

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。 ([2603.19201](https://arxiv.org/abs/2603.19201) / [EA-TWM-2026-0005](evidence-appendix.md#ea-twm-2026-0005)) ⟷ 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0004](evidence-appendix.md#ea-twm-2026-0004))
- `EA-DATA`: 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-2026-0013](evidence-appendix.md#ea-twm-2026-0013)) ⟷ 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0004](evidence-appendix.md#ea-twm-2026-0004))
- `EA-DATA`: 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。 ([2604.07335](https://arxiv.org/abs/2604.07335) / [EA-TWM-2026-0014](evidence-appendix.md#ea-twm-2026-0014)) ⟷ 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0004](evidence-appendix.md#ea-twm-2026-0004))
- `EA-EVAL`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-2026-0001](evidence-appendix.md#ea-twm-2026-0001)) ⟷ 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-2026-0012](evidence-appendix.md#ea-twm-2026-0012))
- `EA-EVAL`: 触觉世界模型必须在扰动与恢复数据上评估，否则会高估接触丰富任务的稳定性。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-2026-0008](evidence-appendix.md#ea-twm-2026-0008)) ⟷ 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-2026-0002](evidence-appendix.md#ea-twm-2026-0002))
- `EA-MODEL`: 把触觉作为接触 grounding 信号注入世界模型，可以改善被遮挡或视觉混淆场景中的物体持续性、物理一致性和零样本接触规划。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0003](evidence-appendix.md#ea-twm-2026-0003)) ⟷ 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。 ([2603.15257](https://arxiv.org/abs/2603.15257) / [EA-TWM-2026-0017](evidence-appendix.md#ea-twm-2026-0017))
- `EA-MODEL`: 触觉世界模型的落地形态正在从被动观测转向预测接触演化并驱动快速反射式控制。 ([2603.19201](https://arxiv.org/abs/2603.19201) / [EA-TWM-2026-0006](evidence-appendix.md#ea-twm-2026-0006)) ⟷ 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-2026-0016](evidence-appendix.md#ea-twm-2026-0016))
- `EA-MODEL`: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-2026-0007](evidence-appendix.md#ea-twm-2026-0007)) ⟷ 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。 ([2603.15257](https://arxiv.org/abs/2603.15257) / [EA-TWM-2026-0017](evidence-appendix.md#ea-twm-2026-0017))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (4 events)
- [`support`] 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。 ([2603.19201](https://arxiv.org/abs/2603.19201) / [EA-TWM-2026-0005](evidence-appendix.md#ea-twm-2026-0005))
- [`support`] 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。 ([2604.07335](https://arxiv.org/abs/2604.07335) / [EA-TWM-2026-0014](evidence-appendix.md#ea-twm-2026-0014))
- [`support`] 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-2026-0013](evidence-appendix.md#ea-twm-2026-0013))
- [`conditional`] 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0004](evidence-appendix.md#ea-twm-2026-0004))

### EA-EVAL (6 events)
- [`support`] 触觉世界模型必须在扰动与恢复数据上评估，否则会高估接触丰富任务的稳定性。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-2026-0008](evidence-appendix.md#ea-twm-2026-0008))
- [`support`] 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-2026-0001](evidence-appendix.md#ea-twm-2026-0001))
- [`conditional`] 在触觉世界动作模型中，触觉融合需要对接触事件做门控，否则会把稀疏、事件驱动的触觉信号当作持续视觉信号处理。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-2026-0010](evidence-appendix.md#ea-twm-2026-0010))
- [`conditional`] 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-2026-0002](evidence-appendix.md#ea-twm-2026-0002))
- [`limit`] 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-2026-0012](evidence-appendix.md#ea-twm-2026-0012))
- [`gap`] 触觉表征评测正在扩展到大规模全手触觉和自我中心视觉，但多数评测仍停留在表征层，不能直接证明下游机器人性能。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TWM-2026-0015](evidence-appendix.md#ea-twm-2026-0015))

### EA-MODEL (7 events)
- [`support`] 把触觉作为接触 grounding 信号注入世界模型，可以改善被遮挡或视觉混淆场景中的物体持续性、物理一致性和零样本接触规划。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0003](evidence-appendix.md#ea-twm-2026-0003))
- [`support`] 触觉世界模型的落地形态正在从被动观测转向预测接触演化并驱动快速反射式控制。 ([2603.19201](https://arxiv.org/abs/2603.19201) / [EA-TWM-2026-0006](evidence-appendix.md#ea-twm-2026-0006))
- [`support`] 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-2026-0009](evidence-appendix.md#ea-twm-2026-0009))
- [`support`] 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-2026-0007](evidence-appendix.md#ea-twm-2026-0007))
- [`support`] 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-2026-0011](evidence-appendix.md#ea-twm-2026-0011))
- [`conditional`] 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。 ([2603.15257](https://arxiv.org/abs/2603.15257) / [EA-TWM-2026-0017](evidence-appendix.md#ea-twm-2026-0017))
- [`conditional`] 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-2026-0016](evidence-appendix.md#ea-twm-2026-0016))

### EA-SENSOR (1 events)
- [`support`] 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-2026-0018](evidence-appendix.md#ea-twm-2026-0018))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-2026-0004](evidence-appendix.md#ea-twm-2026-0004))
- `conditional` 在触觉世界动作模型中，触觉融合需要对接触事件做门控，否则会把稀疏、事件驱动的触觉信号当作持续视觉信号处理。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-2026-0010](evidence-appendix.md#ea-twm-2026-0010))
- `conditional` 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-2026-0002](evidence-appendix.md#ea-twm-2026-0002))
- `limit` 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-2026-0012](evidence-appendix.md#ea-twm-2026-0012))
- `gap` 触觉表征评测正在扩展到大规模全手触觉和自我中心视觉，但多数评测仍停留在表征层，不能直接证明下游机器人性能。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TWM-2026-0015](evidence-appendix.md#ea-twm-2026-0015))
- `conditional` 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。 ([2603.15257](https://arxiv.org/abs/2603.15257) / [EA-TWM-2026-0017](evidence-appendix.md#ea-twm-2026-0017))
- `conditional` 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-2026-0016](evidence-appendix.md#ea-twm-2026-0016))

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
