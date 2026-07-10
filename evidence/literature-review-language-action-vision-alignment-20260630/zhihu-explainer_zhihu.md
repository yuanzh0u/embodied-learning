# 语言、视觉与连续动作对齐：专家解释帖

## TL;DR

语言、视觉与连续动作对齐 不能只看一个漂亮结论，要先看论文级证据、适用条件和失败模式。

## 检索范围

- Time range: 2025-12-30..2026-06-30
- Paper-level sources: 10 / 5
- Output type: expert-explainer

## 常见误区或争议

- 把候选论文、项目页或社交讨论当成正文级证据，会高估结论强度。
- 把 `conditional`、`limit`、`gap` 写成共识，会让综述失真。

## 证据与限制

### 共识/正向证据
- [EA-ALIGN-2026-0008](evidence-appendix.md#ea-align-2026-0008): In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and underdeveloped language-action grounding.
- [EA-ALIGN-2026-0001](evidence-appendix.md#ea-align-2026-0001): Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces.
- [EA-ALIGN-2026-0005](evidence-appendix.md#ea-align-2026-0005): Dense or sparse visual geometry becomes more useful for manipulation when it is explicitly aligned to task-space actions rather than learned only through downstream policy losses.
- [EA-ALIGN-2026-0003](evidence-appendix.md#ea-align-2026-0003): A VLA that inherits visual and linguistic priors from a VLM still lacks an explicit physical motion prior; pretraining the action module on unconditioned trajectories can reduce the burden of learning temporal action dy...
### 条件成立
- [EA-ALIGN-2026-0006](evidence-appendix.md#ea-align-2026-0006): A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control.
### 限制与失败模式
- [EA-ALIGN-2026-0007](evidence-appendix.md#ea-align-2026-0007): Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixing can cause negative transfer.
- [EA-ALIGN-2026-0002](evidence-appendix.md#ea-align-2026-0002): Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- [EA-ALIGN-2026-0004](evidence-appendix.md#ea-align-2026-0004): Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under d...
- [EA-ALIGN-2026-0009](evidence-appendix.md#ea-align-2026-0009): For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self-occluded.
- [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010): A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| [EA-ALIGN-2026-0008](evidence-appendix.md#ea-align-2026-0008) | EA-MODEL | `support` | `direct` | In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and underdeveloped language... | LA4VLA removes visual observations during pretraining and pairs atomic action segments with low-level language descriptions to strengthen language-conditioned action priors before or alongside VLA training. (Abstract; S... | tao-lin | [2606.27295](https://arxiv.org/abs/2606.27295) |
| [EA-ALIGN-2026-0001](evidence-appendix.md#ea-align-2026-0001) | EA-MODEL | `support` | `direct` | Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. | The paper frames low-level state/action heterogeneity as a core cross-embodiment challenge, then uses dense embodied chain-of-thought supervision in the VLM stream and a flow-matching action expert that outputs continuo... | haoyang-li | [2606.30552](https://arxiv.org/abs/2606.30552) |
| [EA-ALIGN-2026-0007](evidence-appendix.md#ea-align-2026-0007) | EA-MODEL | `limit` | `direct` | Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixin... | The paper reports that unified end-effector-relative action representation is critical for cross-embodiment transfer, while indiscriminate pooling of heterogeneous robot datasets can degrade performance. (Abstract; Sect... | ye-wang | [2602.09722](https://arxiv.org/abs/2602.09722) |
| [EA-ALIGN-2026-0002](evidence-appendix.md#ea-align-2026-0002) | EA-MODEL | `limit` | `direct` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset c... | The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone. (Abstract; Section 1.1 Proje... | mathilde-hochedel | [2606.30456](https://arxiv.org/abs/2606.30456) |
| [EA-ALIGN-2026-0004](evidence-appendix.md#ea-align-2026-0004) | EA-MODEL | `limit` | `direct` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same to... | SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines. (Abstract; Section 1 Introduction;... | tengyue-jiang | [2606.30113](https://arxiv.org/abs/2606.30113) |
| [EA-ALIGN-2026-0005](evidence-appendix.md#ea-align-2026-0005) | EA-SENSOR | `support` | `direct` | Dense or sparse visual geometry becomes more useful for manipulation when it is explicitly aligned to task-space actions rather than learned only through downstream policy losses. | Sparse2Act uses task-space end-effector actions as geometric supervision for masked sparse 3D tokens, arguing that point-cloud observations and motions share a metric workspace. (Abstract; Figure 1 caption; Section 1 In... | yu-guo | [2606.12759](https://arxiv.org/abs/2606.12759) |
| [EA-ALIGN-2026-0006](evidence-appendix.md#ea-align-2026-0006) | EA-SENSOR | `conditional` | `direct` | A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. | SSI-Policy builds an RGB-only structured scene interface encoding monocular depth features, language-grounded layouts, and instruction-conditioned 2D motion trajectories; it reports few-shot gains but notes failures fro... | kaijun-wang | [2606.26800](https://arxiv.org/abs/2606.26800) |
| [EA-ALIGN-2026-0009](evidence-appendix.md#ea-align-2026-0009) | EA-SENSOR | `limit` | `direct` | For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self... | The paper introduces a force-position interface that maps hand-specific effort signals into calibrated torques, fingertip forces, and load descriptors, and trains a mask-aware flow-matching policy to rely on force/propr... | soofiyan-atar | [2606.15516](https://arxiv.org/abs/2606.15516) |
| [EA-ALIGN-2026-0003](evidence-appendix.md#ea-align-2026-0003) | EA-XEMBODIMENT | `support` | `direct` | A VLA that inherits visual and linguistic priors from a VLM still lacks an explicit physical motion prior; pretraining the action module on unconditioned trajectories can reduce t... | The method first trains a flow-matching encoder-decoder action module on action trajectories without visual/language tokens, then transfers this prior into VLA training through decoder reuse and latent distillation. (Ab... | dong-jing | [2606.26095](https://arxiv.org/abs/2606.26095) |
| [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010) | EA-XEMBODIMENT | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | [2606.24049](https://arxiv.org/abs/2606.24049) |

## 延伸阅读与可信度

- Evidence sufficiency: formal-ready
- Paper-level sources: 10 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## References

- `2602.09722` [Rethinking Visual-Language-Action Model Scaling: Alignment, Mixture, and Regularization](https://arxiv.org/abs/2602.09722) (2026-02-10)
- `2606.12759` [Sparse2Act: Learning Action-Aligned Sparse 3D Representations for Cross-Domain Robot Manipulation](https://arxiv.org/abs/2606.12759) (2026-06-10)
- `2606.15516` [Transferring Contact, Not Just Motion: Compliant Grasping Across Dexterous Hands](https://arxiv.org/abs/2606.15516) (2026-06-17)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2606.26095` [Learning Action Priors for Cross-embodiment Robot Manipulation](https://arxiv.org/abs/2606.26095) (2026-06-24)
- `2606.26800` [SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation](https://arxiv.org/abs/2606.26800) (2026-06-25)
- `2606.27295` [LA4VLA: Learning to Act without Seeing via Language-Action Pretraining](https://arxiv.org/abs/2606.27295) (2026-06-25)
- `2606.30113` [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113) (2026-06-29)
- `2606.30456` [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456) (2026-06-29)
- `2606.30552` [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](https://arxiv.org/abs/2606.30552) (2026-06-29)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
