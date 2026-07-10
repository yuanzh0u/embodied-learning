# Source Entry Draft: 具身传感器感知误差

Draft entries for later merge into `knowledge/sources.md`. Retrieved 2026-07-09. Evidence events live in `evidence/literature-review-embodied-sensor-perception-error-2026-07-09/evidence.jsonl`.

## S-ARXIV-2606.08765

- 文件/链接：[RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation](https://arxiv.org/abs/2606.08765)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-07; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：视觉遮挡/退化下触觉接触投影、标定误差与空间不确定性；见 EA-SENSOR-2026-0002。
- 适用：需要复核 RGB-S、触觉-视觉对齐、标定误差或 occluded manipulation 论点时读取。

## S-ARXIV-2606.16690

- 文件/链接：[PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation](https://arxiv.org/abs/2606.16690)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-15; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：部署期局部视觉异常、action chunk 执行走廊、runtime monitor；见 EA-SENSOR-2026-0005。
- 适用：需要复核全局异常分数为何不足、局部扰动监控或 occlusion/disturbance 风险时读取。

## S-ARXIV-2606.18043

- 文件/链接：[Uncertainty Quantification for Flow-Based Vision-Language-Action Models](https://arxiv.org/abs/2606.18043)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-16; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：flow-based VLA epistemic uncertainty、velocity-field disagreement、失败检测；见 EA-SENSOR-2026-0004。
- 适用：需要复核 VLA 置信度、分布外失败和主动微调相关论点时读取。

## S-ARXIV-2606.20754

- 文件/链接：[Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models](https://arxiv.org/abs/2606.20754)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-18; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：hidden activation perturbation、VLA failure detection、distribution shift；见 EA-SENSOR-2026-0003。
- 适用：需要复核 VLA 不确定性估计和失败检测论点时读取。

## S-ARXIV-2606.26663

- 文件/链接：[Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention](https://arxiv.org/abs/2606.26663)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-25; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：contact-rich WAM、tactile pollution、触觉 token 融合 caveat；见 EA-SENSOR-2026-0008。
- 适用：需要复核多模态融合为何可能引入新误差时读取。

## S-ARXIV-2606.28899

- 文件/链接：[You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact](https://arxiv.org/abs/2606.28899)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-27; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：遮挡/弱光/反光/透明表面下视觉位姿估计失败，触觉 6-DoF pose 补充；见 EA-SENSOR-2026-0006。
- 适用：需要复核触觉 pose estimation 与视觉失败边界时读取。

## S-ARXIV-2606.29384

- 文件/链接：[Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model](https://arxiv.org/abs/2606.29384)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-28; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：illumination shift、degraded RGB observation、event stream for robust VLA；见 EA-SENSOR-2026-0011。
- 适用：需要复核事件相机/事件流如何补偿 RGB 可见性退化时读取。

## S-ARXIV-2606.30988

- 文件/链接：[Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force](https://arxiv.org/abs/2606.30988)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-29; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：force/tactile/audio 交互状态、硬件任务依赖、多传感持续学习；见 EA-SENSOR-2026-0010。
- 适用：需要复核视觉策略如何增量适配 force-torque 等新模态时读取。

## S-ARXIV-2607.02840

- 文件/链接：[TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840)
- 类型：论文 / arXiv
- 时间标记：published 2026-07-03; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：contact-rich VLA failure、tactile-aware world model、局部纠错片段；见 EA-SENSOR-2026-0009。
- 适用：需要复核触觉世界模型和接触失败恢复时读取。

## S-ARXIV-2607.04234

- 文件/链接：[SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects](https://arxiv.org/abs/2607.04234)
- 类型：论文 / arXiv
- 时间标记：published 2026-07-05; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-EVAL：Goal Success vs Safety Success、滑移/掉落/形变、柔性物安全评测；见 EA-EVAL-2026-0007。
- 适用：需要复核 success-only 评测为什么高估策略可靠性时读取。

## S-ARXIV-2607.07196

- 文件/链接：[Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators](https://arxiv.org/abs/2607.07196)
- 类型：论文 / arXiv
- 时间标记：published 2026-07-08; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-EVAL：world-model simulator admissibility、视觉逼真度与动作响应正确性的断裂；见 EA-EVAL-2026-0012。
- 适用：需要复核世界模型是否可作为闭环评测裁判时读取。

## S-ARXIV-2607.07287

- 文件/链接：[TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation](https://arxiv.org/abs/2607.07287)
- 类型：论文 / arXiv
- 时间标记：published 2026-07-08; retrieved 2026-07-09
- 可信等级：primary
- 主题范围：
  - EA-SENSOR：滑移、力不匹配、接触稳定性、触觉高频残差修正；见 EA-SENSOR-2026-0001。
- 适用：需要复核触觉作为接触隐变量和局部误差反馈通道的论点时读取。
