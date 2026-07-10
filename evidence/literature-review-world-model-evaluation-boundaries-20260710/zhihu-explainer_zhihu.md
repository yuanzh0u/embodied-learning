# 世界模型评测边界：专家解释帖

## TL;DR

世界模型评测边界 不能只看一个漂亮结论，要先看论文级证据、适用条件和失败模式。

## 检索范围

- Time range: 2025-12-11..2026-06-11
- Paper-level sources: 5 / 5
- Output type: expert-explainer

## 常见误区或争议

- 把候选论文、项目页或社交讨论当成正文级证据，会高估结论强度。
- 把 `conditional`、`limit`、`gap` 写成共识，会让综述失真。

## 证据与限制

### 条件成立
- [EA-EVAL-2026-SMOKE-0004](evidence-appendix.md#ea-eval-2026-smoke-0004): For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before execution.
- [EA-EVAL-2026-MEMO-0006](evidence-appendix.md#ea-eval-2026-memo-0006): Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic frame dropping can remove exactly the even...
- [EA-EVAL-2026-SMOKE-0003](evidence-appendix.md#ea-eval-2026-smoke-0003): A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action candidates.
### 限制与失败模式
- [EA-EVAL-2026-SMOKE-0005](evidence-appendix.md#ea-eval-2026-smoke-0005): External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometry-only checks do not verify dynamics or...
- [EA-EVAL-2026-SMOKE-0002](evidence-appendix.md#ea-eval-2026-smoke-0002): Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following do not establish robotic trustworthiness.
### 开放问题
- [EA-EVAL-2026-SMOKE-0001](evidence-appendix.md#ea-eval-2026-smoke-0001): Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| [EA-EVAL-2026-SMOKE-0004](evidence-appendix.md#ea-eval-2026-smoke-0004) | EA-EVAL | `conditional` | `direct` | For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking d... | VLM-DEWM validates each VLM decision against a persistent world model and uses discrepancy analysis for targeted recovery, with reported gains in state tracking and recovery success in long-horizon manufacturing tasks.... | guoqin-tang | [2602.15549](https://arxiv.org/abs/2602.15549) |
| [EA-EVAL-2026-MEMO-0006](evidence-appendix.md#ea-eval-2026-memo-0006) | EA-EVAL | `conditional` | `direct` | Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic fr... | The paper argues that pixel-space rollout is expensive, but indiscriminate frame dropping is misaligned with embodied manipulation because critical task events may involve only small visual changes and become unrecovera... | ziheng-he | [2606.00664](https://arxiv.org/abs/2606.00664) |
| [EA-EVAL-2026-SMOKE-0003](evidence-appendix.md#ea-eval-2026-smoke-0003) | EA-EVAL | `conditional` | `direct` | A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action candidates. | The paper presents a unified video-action world model that combines policy learning, video prediction, and action evaluation, using test-time sampling, ranking, and simulator-based rectification before execution. (Abstr... | pengfei-zhou | [2606.01027](https://arxiv.org/abs/2606.01027) |
| [EA-EVAL-2026-SMOKE-0005](evidence-appendix.md#ea-eval-2026-smoke-0005) | EA-EVAL | `limit` | `direct` | External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometr... | The limitations section identifies upstream perception errors, open-vocabulary failures under closed-world assumptions, and a dynamics gap in the physical verification scope. (4.4.2 Limitations and Failure Mode Analysis... | guoqin-tang | [2602.15549](https://arxiv.org/abs/2602.15549) |
| [EA-EVAL-2026-SMOKE-0002](evidence-appendix.md#ea-eval-2026-smoke-0002) | EA-EVAL | `limit` | `direct` | Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following d... | RoboTrustBench evaluates video world models with four scenario types and a six-dimensional protocol, reporting failures in constraint reasoning, counterfactual grounding, physical interaction, and unsafe-instruction sup... | huiqiong-li | [2606.01600](https://arxiv.org/abs/2606.01600) |
| [EA-EVAL-2026-SMOKE-0001](evidence-appendix.md#ea-eval-2026-smoke-0001) | EA-EVAL | `gap` | `direct` | Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias... | The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias. (Abstract... | tianzhuo-yang | [2605.29360](https://arxiv.org/abs/2605.29360) |

## 延伸阅读与可信度

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
