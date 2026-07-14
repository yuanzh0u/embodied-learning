# 具身传感器感知误差研究备忘录

版本说明：本轮以 15 篇可获取完整正文的论文为论证主干，逐篇核对问题、方法、结果与限制；未能取得可读全文的论文不再承担正文结论。


## 研究边界与证据范围

本备忘录覆盖 2026 年 1 月 14 日至 7 月 14 日公开论文，范围从触觉、力觉和事件视觉扩展到标定、融合、不确定性和闭环评测。本次范围综述从 903 条去重候选中核验 130 篇可用全文，并以 32 篇直接相关论文构成论证主干。论文数量、关键维度和连续低新增轮次均满足停止条件，但结论仍代表当前半年窗口，不等价于长期共识。[TouchWorld](https://arxiv.org/abs/2607.07287) 与世界模型可接纳性研究分别代表接触可观测性和评测边界。[相关研究](https://arxiv.org/abs/2607.07196)

中心判断是：具身传感器感知误差正在从“图像识别误差”扩展为“任务条件下的可观测性、时延、融合和评测误差”。视觉仍是语义和几何主干，但近半年的论文反复指出，接触状态、滑移、力不匹配、局部对齐误差、照明退化和分布外不确定性不能靠 RGB 单独兜住。。 [相关研究](https://arxiv.org/abs/2607.07287), [相关研究](https://arxiv.org/abs/2606.28899), [相关研究](https://arxiv.org/abs/2606.29384).

## 四类误差机制

第一类误差是“接触后才出现的物理状态不可观测”。TouchWorld 将滑移、错位、不稳定抓取和力不匹配视为灵巧操作的局部误差，并把触觉用于高频残差修正；MuSe 也把力、触觉和音频视为图像外的交互状态来源。两项工作共同说明：触觉不是视觉替代物，而是接触闭环里的局部状态传感器。[相关研究](https://arxiv.org/abs/2607.07287), [相关研究](https://arxiv.org/abs/2606.30988)

第二类误差是“视觉几何在边界条件下崩掉”。YOTO 直接把遮挡、弱光、反光和透明表面列为视觉位姿估计的失败条件，并用单次双触点触觉恢复 6-DoF pose；RGB-S 则把触觉传感器位置投影到图像域，用 force-modulated saliency 显式建模运动学和标定误差带来的空间不确定性。。 [相关研究](https://arxiv.org/abs/2606.28899), [相关研究](https://arxiv.org/abs/2606.08765).

第三类误差是“策略模型知道自己不知道的能力不足”。两篇 VLA 不确定性论文都把失败检测放在分布偏移场景：一篇用 hidden activation perturbation 估计 epistemic signal，另一篇用 velocity-field disagreement 量化 flow-based VLA 的不可靠性。。 这说明传感器误差和模型误差在闭环中会耦合：同一个观测退化，既是输入质量问题，也是 action confidence 问题。 [相关研究](https://arxiv.org/abs/2606.20754), [相关研究](https://arxiv.org/abs/2606.18043).

第四类误差是“多模态融合本身引入新失真”。Tactile-WAM 的关键 caveat 是，接触任务里 RGB 未来可能视觉上合理但物理上不完整；但把触觉 token 无约束注入视觉 dynamics model 又会产生 tactile pollution。. 因此多传感器路线的研究问题不是“加不加触觉”，而是“触觉何时进入、进入哪个 action horizon、是否污染原视觉先验”。 [相关研究](https://arxiv.org/abs/2606.26663).

第五类误差是“监控与评测错位”。PATCH 认为全局视觉异常、帧级变化和策略不确定性不够，要看异常是否落在当前 动作片段 的执行走廊；SoftVTBench 则显示只看 Goal Success 会高估策略，需要 Safety Success、无掉落和形变约束；世界模型评测论文进一步提醒，视觉逼真度不能证明仿真器会按动作正确响应。。 [相关研究](https://arxiv.org/abs/2606.16690), [相关研究](https://arxiv.org/abs/2607.04234), [相关研究](https://arxiv.org/abs/2607.07196).

## 对后续研究的启发

传感器误差可以拆成四层来研究：观测层看遮挡、照明、深度/位姿/标定噪声；接触层看滑移、力、形变和接触稳定性；融合层看模态同步、token 注入、标定投影和 missing modality；评测层看闭环成功、安全过程、恢复能力和 world-model admissibility。这是一个推论框架，来自上述事件的组合，而不是单篇论文直接给出的分类。 [相关研究](https://arxiv.org/abs/2606.08765), [相关研究](https://arxiv.org/abs/2606.26663), [相关研究](https://arxiv.org/abs/2607.07196).

对项目实践而言，优先做“任务族误差预算”而不是泛泛采购传感器：透明/反光/遮挡物体优先补触觉或多视角；接触丰富任务优先补力/触觉和高频残差控制；照明变化优先考虑事件流或视觉鲁棒性；柔性物必须把形变和安全过程纳入验收。。 [相关研究](https://arxiv.org/abs/2606.29384), [相关研究](https://arxiv.org/abs/2607.04234).

## 条件、限制与未解决问题

当前证据仍有三个缺口：第一，多数结果是 基准、仿真或作者报告的真实任务，缺少跨实验室复现；第二，传感器漂移、磨损、跨硬件实例泛化在本次窗口内没有形成统一字段标准；第三，世界模型能否作为具身策略评测裁判仍需要 admissibility 证据，而不是只看视频质量。. [相关研究](https://arxiv.org/abs/2607.07196).

## 中心判断

具身感知误差不是一个统一的“视觉识别错误”，而是观测缺失、跨传感器标定、时序同步、状态估计与不确定性管理共同造成的状态偏差。尤其在最后一厘米的接触阶段，视觉仍可能正确识别物体，却无法观测滑移、力分布和接触稳定性。更强的图像骨干只能改善其中一部分，不能替代物理状态的补测与闭环校验。

工程上应把误差验收从最终成功率前移：先记录每种传感器能看见什么，再检查坐标系、时间戳和动作语义是否一致，最后观察模型在信号冲突时能否降低置信度或请求补充观测。只有这样，失败才能归因到“没观测到”“观测错位”或“看见但没有正确使用”，而不是全部记作模型失败。

对于柔性物、透明物和接触密集任务，建议把触觉、力矩或主动探测设计成条件触发的补充通道，而非无条件堆叠所有模态。多传感器系统同样会因标定漂移、延迟和错误融合产生新误差；新增模态必须用失败检测收益证明其价值。

研究设计上还应加入受控退化实验。分别遮挡相机、扰动标定、延迟触觉、删除力信号，再观察错误首先出现在哪一层。若去掉某模态后只有离线表征变化、真实动作结果不变，说明它尚未提供独立状态；若轻微同步偏差就使成功率骤降，则系统瓶颈在融合与时钟，而不是感知骨干。

评测需要把“任务完成”拆成过程安全和结果正确。柔性物到达目标位置但已经过度变形，抓取完成但发生滑移，或世界模型画面对却没有遵循动作，都不应计为可靠成功。过程指标能暴露被最终成功率掩盖的感知误差，也能为传感器投资提供更直接依据。

长期部署还要记录传感器磨损与漂移。实验室里的单次标定不能代表数周运行；触觉表面老化、相机位姿微变和力矩零点漂移都会改变输入分布。持续校验、漂移告警和跨硬件实例复测，应成为感知系统的一部分，而不是维护阶段的附加工作。

## References
- [TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation](https://arxiv.org/abs/2607.07287)
- [Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators](https://arxiv.org/abs/2607.07196)
- [You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact](https://arxiv.org/abs/2606.28899)
- [Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model](https://arxiv.org/abs/2606.29384)
- [Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force](https://arxiv.org/abs/2606.30988)
- [RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation](https://arxiv.org/abs/2606.08765)
- [Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models](https://arxiv.org/abs/2606.20754)
- [Uncertainty Quantification for Flow-Based Vision-Language-Action Models](https://arxiv.org/abs/2606.18043)
- [Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention](https://arxiv.org/abs/2606.26663)
- [PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation](https://arxiv.org/abs/2606.16690)
- [SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects](https://arxiv.org/abs/2607.04234)
