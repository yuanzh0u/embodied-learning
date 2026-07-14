# 世界模型评测边界：洞察短串

## Hook

世界模型评测边界 最容易被讲成一句口号，但真正值钱的信息藏在证据条件里。

## 证据约束洞察

1. For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking d... ([EA-EVAL-2026-SMOKE-0004](evidence-appendix.md#ea-eval-2026-smoke-0004); stance: `conditional`)
2. Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic fr... ([EA-EVAL-2026-MEMO-0006](evidence-appendix.md#ea-eval-2026-memo-0006); stance: `conditional`)
3. A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action candidates. ([EA-EVAL-2026-SMOKE-0003](evidence-appendix.md#ea-eval-2026-smoke-0003); stance: `conditional`)
4. External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometr... ([EA-EVAL-2026-SMOKE-0005](evidence-appendix.md#ea-eval-2026-smoke-0005); stance: `limit`)
5. Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following d... ([EA-EVAL-2026-SMOKE-0002](evidence-appendix.md#ea-eval-2026-smoke-0002); stance: `limit`)

## 边界提醒

- Strong hook is allowed; stance/confidence cannot be upgraded.
- Any `conditional`, `limit`, or `gap` claim must stay visible in the thread.

## 依据来源

- Time range: 2025-12-11..2026-06-11

- Evidence sufficiency: formal-ready
- Paper-level sources: 5 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

- No immediate source gaps detected from loaded packet inputs.

## References

- `2602.15549` [VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing](https://arxiv.org/abs/2602.15549) (2026-02-17)
- `2605.29360` [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360) (2026-05-28)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [τ0-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.01600` [RoboTrustBench: Benchmarking the Trustworthiness of Video World Models for Robotic Manipulation](https://arxiv.org/abs/2606.01600) (2026-06-01)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
