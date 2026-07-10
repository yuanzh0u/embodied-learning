# Evidence Appendix: 语言、视觉与连续动作对齐

- Time range: 2025-12-30..2026-06-30
- Events: 10
- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。

### EA-ALIGN-2026-0008

- Claim: In standard VLA pretraining, dense visual-action supervision can dominate the comparatively sparse language-action signal, encouraging visual shortcuts and underdeveloped language-action grounding.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.27295](https://arxiv.org/abs/2606.27295) LA4VLA: Learning to Act without Seeing via Language-Action Pretraining
- Locator: Abstract; Section 1 Introduction; Section 4 LA4VLA Dataset Construction; Section 5 LA4VLA Pretraining
- Evidence: LA4VLA removes visual observations during pretraining and pairs atomic action segments with low-level language descriptions to strengthen language-conditioned action priors before or alongside VLA training.
- Authors: tao-lin

### EA-ALIGN-2026-0001

- Claim: Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.30552](https://arxiv.org/abs/2606.30552) Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision
- Locator: Abstract; Introduction; Section 3.1 Model Architecture
- Evidence: The paper frames low-level state/action heterogeneity as a core cross-embodiment challenge, then uses dense embodied chain-of-thought supervision in the VLM stream and a flow-matching action expert that outputs continuous action chunks.
- Authors: haoyang-li

### EA-ALIGN-2026-0007

- Claim: Scaling VLA data is not analogous to scaling text/image data because robot datasets are heterogeneous in embodiment, sensing, control frequency, and action space; naive data mixing can cause negative transfer.
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.09722](https://arxiv.org/abs/2602.09722) Rethinking Visual-Language-Action Model Scaling: Alignment, Mixture, and Regularization
- Locator: Abstract; Section I Introduction; Section V Experiments
- Evidence: The paper reports that unified end-effector-relative action representation is critical for cross-embodiment transfer, while indiscriminate pooling of heterogeneous robot datasets can degrade performance.
- Authors: ye-wang

### EA-ALIGN-2026-0002

- Claim: Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30456](https://arxiv.org/abs/2606.30456) Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform
- Locator: Abstract; Section 1.1 Project Motivation; Section 2.1 Background
- Evidence: The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone.
- Authors: mathilde-hochedel

### EA-ALIGN-2026-0004

- Claim: Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under different robot states and contacts.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30113](https://arxiv.org/abs/2606.30113) SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance
- Locator: Abstract; Section 1 Introduction; Section 2.2 Discrete Action Tokenizers
- Evidence: SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines.
- Authors: tengyue-jiang

### EA-ALIGN-2026-0005

- Claim: Dense or sparse visual geometry becomes more useful for manipulation when it is explicitly aligned to task-space actions rather than learned only through downstream policy losses.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.12759](https://arxiv.org/abs/2606.12759) Sparse2Act: Learning Action-Aligned Sparse 3D Representations for Cross-Domain Robot Manipulation
- Locator: Abstract; Figure 1 caption; Section 1 Introduction
- Evidence: Sparse2Act uses task-space end-effector actions as geometric supervision for masked sparse 3D tokens, arguing that point-cloud observations and motions share a metric workspace.
- Authors: yu-guo

### EA-ALIGN-2026-0006

- Claim: A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26800](https://arxiv.org/abs/2606.26800) SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation
- Locator: Abstract; Section III-B Framework Overview; Section IV-H Failure Cases; Section V Conclusion
- Evidence: SSI-Policy builds an RGB-only structured scene interface encoding monocular depth features, language-grounded layouts, and instruction-conditioned 2D motion trajectories; it reports few-shot gains but notes failures from perception noise and contact limitations.
- Authors: kaijun-wang

### EA-ALIGN-2026-0009

- Claim: For dexterous manipulation, aligning motion alone is insufficient; contact loading and force feedback must be made comparable across hands, especially when visual evidence is self-occluded.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.15516](https://arxiv.org/abs/2606.15516) Transferring Contact, Not Just Motion: Compliant Grasping Across Dexterous Hands
- Locator: Abstract; Section 1 Introduction; Contributions list
- Evidence: The paper introduces a force-position interface that maps hand-specific effort signals into calibrated torques, fingertip forces, and load descriptors, and trains a mask-aware flow-matching policy to rely on force/proprioception when vision is occluded.
- Authors: soofiyan-atar

### EA-ALIGN-2026-0003

- Claim: A VLA that inherits visual and linguistic priors from a VLM still lacks an explicit physical motion prior; pretraining the action module on unconditioned trajectories can reduce the burden of learning temporal action dynamics and cross-modal alignment simultaneously.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26095](https://arxiv.org/abs/2606.26095) Learning Action Priors for Cross-embodiment Robot Manipulation
- Locator: Abstract; Section III Learning Action Prior; Section III-D VLA Training with Action Prior Distillation
- Evidence: The method first trains a flow-matching encoder-decoder action module on action trajectories without visual/language tokens, then transfers this prior into VLA training through decoder reuse and latent distillation.
- Authors: dong-jing

### EA-ALIGN-2026-0010

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: Abstract; Section 1 Introduction; Section 3.2 Inconsistency of Control Commands across Robots; Section 4 SPACE
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Authors: haeone-lee

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
