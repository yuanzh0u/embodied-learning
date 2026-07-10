# Evidence Appendix: 世界模型评测边界

- Time range: 2025-12-11..2026-06-11
- Events: 6
- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。

### EA-EVAL-2026-SMOKE-0004

- Claim: For dynamic manufacturing, an external queryable world model can make VLM planning more verifiable by separating persistent state management from semantic reasoning and checking decisions before execution.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.15549](https://arxiv.org/abs/2602.15549) VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing
- Locator: Abstract; 1 Introduction; Methodology
- Evidence: VLM-DEWM validates each VLM decision against a persistent world model and uses discrepancy analysis for targeted recovery, with reported gains in state tracking and recovery success in long-horizon manufacturing tasks.
- Authors: guoqin-tang

### EA-EVAL-2026-MEMO-0006

- Claim: Efficient embodied world-model rollouts must preserve sparse task-relevant manipulation events such as approach, contact, grasp, and release; reducing inference cost by generic frame dropping can remove exactly the events downstream policies need.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.00664](https://arxiv.org/abs/2606.00664) SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models
- Locator: Abstract; 1 Introduction
- Evidence: The paper argues that pixel-space rollout is expensive, but indiscriminate frame dropping is misaligned with embodied manipulation because critical task events may involve only small visual changes and become unrecoverable if omitted.
- Authors: ziheng-he

### EA-EVAL-2026-SMOKE-0003

- Claim: A video-action world model can support pre-execution action evaluation by imagining candidate futures, scoring task progress, and rectifying low-quality action candidates.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) τ0-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract; I Introduction
- Evidence: The paper presents a unified video-action world model that combines policy learning, video prediction, and action evaluation, using test-time sampling, ranking, and simulator-based rectification before execution.
- Authors: pengfei-zhou

### EA-EVAL-2026-SMOKE-0005

- Claim: External world-model verification has explicit deployment boundaries: corrupted perception can pollute the world model, closed-world assumptions fail on novel objects, and geometry-only checks do not verify dynamics or kinematics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.15549](https://arxiv.org/abs/2602.15549) VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing
- Locator: 4.4.2 Limitations and Failure Mode Analysis; Scope of Physical Verification (Dynamics Gap)
- Evidence: The limitations section identifies upstream perception errors, open-vocabulary failures under closed-world assumptions, and a dynamics gap in the physical verification scope.
- Authors: guoqin-tang

### EA-EVAL-2026-SMOKE-0002

- Claim: Trustworthy robotic video world-model evaluation needs constraint-sensitive, counterfactual, and adversarial scenarios because visual coherence and surface instruction following do not establish robotic trustworthiness.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.01600](https://arxiv.org/abs/2606.01600) RoboTrustBench: Benchmarking the Trustworthiness of Video World Models for Robotic Manipulation
- Locator: Abstract; Evaluation Dimensions; Analysis of Trustworthiness Failures
- Evidence: RoboTrustBench evaluates video world models with four scenario types and a six-dimensional protocol, reporting failures in constraint reasoning, counterfactual grounding, physical interaction, and unsafe-instruction suppression.
- Authors: huiqiong-li

### EA-EVAL-2026-SMOKE-0001

- Claim: Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection.
- Stance: `gap` | Confidence: `direct`
- Paper: [2605.29360](https://arxiv.org/abs/2605.29360) MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models
- Locator: Abstract; Problem Formulation; Design of MIRABENCH
- Evidence: The paper frames existing evaluations as weak evidence for whether action-conditioned predictions are reliable, then defines MiraBench around physics adherence, action fidelity, and failure-case optimism bias.
- Authors: tianzhuo-yang

## References

- `2602.15549` [VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing](https://arxiv.org/abs/2602.15549) (2026-02-17)
- `2605.29360` [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360) (2026-05-28)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [τ0-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.01600` [RoboTrustBench: Benchmarking the Trustworthiness of Video World Models for Robotic Manipulation](https://arxiv.org/abs/2606.01600) (2026-06-01)
