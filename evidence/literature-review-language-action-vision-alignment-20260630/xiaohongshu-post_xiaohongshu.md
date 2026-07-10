# 语言、视觉与连续动作对齐：洞察短串

## Hook

语言、视觉与连续动作对齐 最容易被讲成一句口号，但真正值钱的信息藏在证据条件里。

## 证据约束洞察

1. In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and underdeveloped language... ([EA-ALIGN-2026-0008](evidence-appendix.md#ea-align-2026-0008); stance: `support`)
2. Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. ([EA-ALIGN-2026-0001](evidence-appendix.md#ea-align-2026-0001); stance: `support`)
3. Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixin... ([EA-ALIGN-2026-0007](evidence-appendix.md#ea-align-2026-0007); stance: `limit`)
4. Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset c... ([EA-ALIGN-2026-0002](evidence-appendix.md#ea-align-2026-0002); stance: `limit`)
5. Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same to... ([EA-ALIGN-2026-0004](evidence-appendix.md#ea-align-2026-0004); stance: `limit`)

## 边界提醒

- Strong hook is allowed; stance/confidence cannot be upgraded.
- Any `conditional`, `limit`, or `gap` claim must stay visible in the thread.

## 依据来源

- Time range: 2025-12-30..2026-06-30

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
