# Writing Brief: 世界模型评测边界

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 世界模型评测边界
- Time range: 2025-12-11..2026-06-11
- Knowledge IDs: `EA-EVAL`
- Paper-level sources: 5 / 5 (formal-ready)
- Accepted events: 6

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- 证据中没有明显的 stance 张力;考虑以共识+边界作为组织轴。

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-EVAL (6 events)
- [`conditional`] For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before exec... ([2602.15549](https://arxiv.org/abs/2602.15549) / [EA-EVAL-2026-SMOKE-0004](evidence-appendix.md#ea-eval-2026-smoke-0004))
- [`conditional`] Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic frame dropping can rem... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-EVAL-2026-MEMO-0006](evidence-appendix.md#ea-eval-2026-memo-0006))
- [`conditional`] A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action candidates. ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-EVAL-2026-SMOKE-0003](evidence-appendix.md#ea-eval-2026-smoke-0003))
- [`limit`] External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometry-only checks do not... ([2602.15549](https://arxiv.org/abs/2602.15549) / [EA-EVAL-2026-SMOKE-0005](evidence-appendix.md#ea-eval-2026-smoke-0005))
- [`limit`] Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following do not establish robo... ([2606.01600](https://arxiv.org/abs/2606.01600) / [EA-EVAL-2026-SMOKE-0002](evidence-appendix.md#ea-eval-2026-smoke-0002))
- [`gap`] Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection. ([2605.29360](https://arxiv.org/abs/2605.29360) / [EA-EVAL-2026-SMOKE-0001](evidence-appendix.md#ea-eval-2026-smoke-0001))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before exec... ([2602.15549](https://arxiv.org/abs/2602.15549) / [EA-EVAL-2026-SMOKE-0004](evidence-appendix.md#ea-eval-2026-smoke-0004))
- `conditional` Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic frame dropping can rem... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-EVAL-2026-MEMO-0006](evidence-appendix.md#ea-eval-2026-memo-0006))
- `conditional` A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action candidates. ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-EVAL-2026-SMOKE-0003](evidence-appendix.md#ea-eval-2026-smoke-0003))
- `limit` External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometry-only checks do not... ([2602.15549](https://arxiv.org/abs/2602.15549) / [EA-EVAL-2026-SMOKE-0005](evidence-appendix.md#ea-eval-2026-smoke-0005))
- `limit` Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following do not establish robo... ([2606.01600](https://arxiv.org/abs/2606.01600) / [EA-EVAL-2026-SMOKE-0002](evidence-appendix.md#ea-eval-2026-smoke-0002))
- `gap` Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection. ([2605.29360](https://arxiv.org/abs/2605.29360) / [EA-EVAL-2026-SMOKE-0001](evidence-appendix.md#ea-eval-2026-smoke-0001))

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
