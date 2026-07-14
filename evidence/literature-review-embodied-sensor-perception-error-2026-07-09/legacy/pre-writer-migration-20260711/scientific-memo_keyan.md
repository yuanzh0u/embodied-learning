# 具身传感器感知误差研究备忘录

## 研究边界与证据范围

本备忘录只覆盖 2026-01-09 至 2026-07-09 半年内 arXiv 可访问 HTML 正文的论文。检索从 `EA-SENSOR` 出发，扩展到 `EA-DATA` 的数据/标定质量和 `EA-EVAL` 的闭环评测；106 篇候选中，12 篇被提升为 accepted evidence。证据充分性达到正式综述阈值，但结论仍是半年窗口内的论文趋势，不等价于长期共识。Trace: [EA-SENSOR-2026-0001](evidence-appendix.md#ea-sensor-2026-0001), [EA-EVAL-2026-0012](evidence-appendix.md#ea-eval-2026-0012).

中心判断是：具身传感器感知误差正在从“图像识别误差”扩展为“任务条件下的可观测性、时延、融合和评测误差”。视觉仍是语义和几何主干，但近半年的论文反复指出，接触状态、滑移、力不匹配、局部对齐误差、照明退化和分布外不确定性不能靠 RGB 单独兜住。[2607.07287](https://arxiv.org/abs/2607.07287), [2606.28899](https://arxiv.org/abs/2606.28899), [2606.29384](https://arxiv.org/abs/2606.29384). Trace: [EA-SENSOR-2026-0001](evidence-appendix.md#ea-sensor-2026-0001), [EA-SENSOR-2026-0006](evidence-appendix.md#ea-sensor-2026-0006), [EA-SENSOR-2026-0011](evidence-appendix.md#ea-sensor-2026-0011).

## Evidence Core

- Evidence sufficiency: `formal-ready`；12 篇论文级来源 / 最低门槛 5 篇。
- Accepted events: 12；覆盖 `support`、`conditional`、`limit` 与 `gap`。
- Traceability: 正文论文 ID 链接到 arXiv，事件 ID 链接到 [evidence-appendix.md](evidence-appendix.md)；候选论文不用于支撑结论。
- 主要限制：半年窗口、以作者报告的 benchmark/仿真/实机结果为主，不能外推为跨硬件长期共识。

## Claim Map

| 机制 | 论文信号 | Stance |
|---|---|---|
| 接触隐变量不可见 | 触觉/力觉揭示视觉不可直接观测的滑移、力、接触稳定性 | support |
| 遮挡和材料导致位姿失败 | 单次触觉接触可补充 6-DoF pose 估计 | support |
| VLA 置信度缺失 | 扰动或 velocity-field disagreement 可做失败检测 | support |
| 融合不是堆 token | 无约束触觉注入可能污染视觉世界模型 | conditional |
| 监控不能只看全局异常 | action-conditioned 局部执行走廊更接近任务风险 | limit |
| success-only 评测不足 | 需要 Safety Success、形变、滑移/掉落等过程指标 | limit |
| 世界模型不能直接当裁判 | 视觉逼真度不保证动作响应正确 | gap |

## 证据簇：四类误差机制

第一类误差是“接触后才出现的物理状态不可观测”。TouchWorld 将滑移、错位、不稳定抓取和力不匹配视为灵巧操作的局部误差，并把触觉用于高频残差修正；MuSe 也把 force、tactile、audio 视为图像外的 interaction state 来源。[2607.07287](https://arxiv.org/abs/2607.07287), [2606.30988](https://arxiv.org/abs/2606.30988). 这是对 `EA-SENSOR` 主题卡的强化：触觉不是视觉替代物，而是接触闭环里的局部状态传感器。Trace: [EA-SENSOR-2026-0001](evidence-appendix.md#ea-sensor-2026-0001), [EA-SENSOR-2026-0010](evidence-appendix.md#ea-sensor-2026-0010).

第二类误差是“视觉几何在边界条件下崩掉”。YOTO 直接把遮挡、弱光、反光和透明表面列为视觉位姿估计的失败条件，并用单次双触点触觉恢复 6-DoF pose；RGB-S 则把触觉传感器位置投影到图像域，用 force-modulated saliency 显式建模运动学和标定误差带来的空间不确定性。[2606.28899](https://arxiv.org/abs/2606.28899), [2606.08765](https://arxiv.org/abs/2606.08765). Trace: [EA-SENSOR-2026-0006](evidence-appendix.md#ea-sensor-2026-0006), [EA-SENSOR-2026-0002](evidence-appendix.md#ea-sensor-2026-0002).

第三类误差是“策略模型知道自己不知道的能力不足”。两篇 VLA 不确定性论文都把失败检测放在分布偏移场景：一篇用 hidden activation perturbation 估计 epistemic signal，另一篇用 velocity-field disagreement 量化 flow-based VLA 的不可靠性。[2606.20754](https://arxiv.org/abs/2606.20754), [2606.18043](https://arxiv.org/abs/2606.18043). 这说明传感器误差和模型误差在闭环中会耦合：同一个观测退化，既是输入质量问题，也是 action confidence 问题。Trace: [EA-SENSOR-2026-0003](evidence-appendix.md#ea-sensor-2026-0003), [EA-SENSOR-2026-0004](evidence-appendix.md#ea-sensor-2026-0004).

第四类误差是“多模态融合本身引入新失真”。Tactile-WAM 的关键 caveat 是，接触任务里 RGB 未来可能视觉上合理但物理上不完整；但把触觉 token 无约束注入视觉 dynamics model 又会产生 tactile pollution。[2606.26663](https://arxiv.org/abs/2606.26663). 因此多传感器路线的研究问题不是“加不加触觉”，而是“触觉何时进入、进入哪个 action horizon、是否污染原视觉先验”。Trace: [EA-SENSOR-2026-0008](evidence-appendix.md#ea-sensor-2026-0008).

第五类误差是“监控与评测错位”。PATCH 认为全局视觉异常、帧级变化和策略不确定性不够，要看异常是否落在当前 action chunk 的执行走廊；SoftVTBench 则显示只看 Goal Success 会高估策略，需要 Safety Success、无掉落和形变约束；世界模型评测论文进一步提醒，视觉逼真度不能证明仿真器会按动作正确响应。[2606.16690](https://arxiv.org/abs/2606.16690), [2607.04234](https://arxiv.org/abs/2607.04234), [2607.07196](https://arxiv.org/abs/2607.07196). Trace: [EA-SENSOR-2026-0005](evidence-appendix.md#ea-sensor-2026-0005), [EA-EVAL-2026-0007](evidence-appendix.md#ea-eval-2026-0007), [EA-EVAL-2026-0012](evidence-appendix.md#ea-eval-2026-0012).

## 对后续研究的启发

传感器误差可以拆成四层来研究：观测层看遮挡、照明、深度/位姿/标定噪声；接触层看滑移、力、形变和接触稳定性；融合层看模态同步、token 注入、标定投影和 missing modality；评测层看闭环成功、安全过程、恢复能力和 world-model admissibility。这是一个推论框架，来自上述事件的组合，而不是单篇论文直接给出的分类。Trace: [EA-SENSOR-2026-0002](evidence-appendix.md#ea-sensor-2026-0002), [EA-SENSOR-2026-0008](evidence-appendix.md#ea-sensor-2026-0008), [EA-EVAL-2026-0012](evidence-appendix.md#ea-eval-2026-0012).

对项目实践而言，优先做“任务族误差预算”而不是泛泛采购传感器：透明/反光/遮挡物体优先补触觉或多视角；接触丰富任务优先补力/触觉和高频残差控制；照明变化优先考虑事件流或视觉鲁棒性；柔性物必须把形变和安全过程纳入验收。[2606.29384](https://arxiv.org/abs/2606.29384), [2607.04234](https://arxiv.org/abs/2607.04234). Trace: [EA-SENSOR-2026-0011](evidence-appendix.md#ea-sensor-2026-0011), [EA-EVAL-2026-0007](evidence-appendix.md#ea-eval-2026-0007).

## 条件、限制与未解决问题

当前证据仍有三个缺口：第一，多数结果是 benchmark、仿真或作者报告的真实任务，缺少跨实验室复现；第二，传感器漂移、磨损、跨硬件实例泛化在本次窗口内没有形成统一字段标准；第三，世界模型能否作为具身策略评测裁判仍需要 admissibility 证据，而不是只看视频质量。[2607.07196](https://arxiv.org/abs/2607.07196). Trace: [EA-EVAL-2026-0012](evidence-appendix.md#ea-eval-2026-0012).

## References

- [2606.08765](https://arxiv.org/abs/2606.08765) RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation.
- [2606.16690](https://arxiv.org/abs/2606.16690) PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation.
- [2606.18043](https://arxiv.org/abs/2606.18043) Uncertainty Quantification for Flow-Based Vision-Language-Action Models.
- [2606.20754](https://arxiv.org/abs/2606.20754) Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models.
- [2606.26663](https://arxiv.org/abs/2606.26663) Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention.
- [2606.28899](https://arxiv.org/abs/2606.28899) You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact.
- [2606.29384](https://arxiv.org/abs/2606.29384) Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model.
- [2606.30988](https://arxiv.org/abs/2606.30988) Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force.
- [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training.
- [2607.04234](https://arxiv.org/abs/2607.04234) SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects.
- [2607.07196](https://arxiv.org/abs/2607.07196) Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators.
- [2607.07287](https://arxiv.org/abs/2607.07287) TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation.

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
