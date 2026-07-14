# 具身机器人为什么总在“最后一厘米”翻车？近半年论文给了一个答案：它没真的看见接触

## TL;DR

很多人把机器人感知误差理解成“摄像头识别错了”。近半年具身智能论文里更有意思的趋势是：真正难的不是识别杯子，而是闭环控制中那些 RGB 看不见、模型又没把握的状态，比如滑移、接触法向、力不匹配、透明/反光表面的位姿、照明退化和动作执行过程中的局部扰动。, . [相关研究](https://arxiv.org/abs/2607.07287), 相关研究.

## 检索范围

- 时间范围：2026-01-09至2026-07-09。
- 证据规模：12 篇论文、12 条 已接纳证据，达到正式解释稿门槛。
- 证据边界：arXiv HTML 正文快照；完整事件立场、置信度和定位见 随附证据附录。

## 真实机制

### 误区一：视觉强了，传感器问题就结束了

视觉确实是机器人通用语义能力的底座，但它不是物理接触的全知传感器。TouchWorld 这类工作把失败直接写成滑移、错位、不稳定抓取和力不匹配；MuSe 也指出 force、tactile、audio 会揭示图像不可直接观测的 interaction states。, . 也就是说，机器人“看见了物体”不等于“知道手指和物体之间正在发生什么”。 [相关研究](https://arxiv.org/abs/2607.07287), 相关研究.

遮挡、弱光、反光和透明表面会把这个问题进一步放大。YOTO 的 6-DoF pose 论文把这些条件列为视觉位姿估计的失败场景，并展示单次双触点触觉可以在视觉不可靠时补位；Event-VLA 则从另一端处理照明变化，用事件流补充 RGB-centric VLA 的可见性退化。, . [相关研究](https://arxiv.org/abs/2606.28899), 相关研究.

### 误区二：多加传感器就能解决

更准确的说法是：加传感器只解决“可观测性”，不自动解决“融合误差”。RGB-S 的做法很典型：它不是把触觉粗暴拼到视觉 表征单元 里，而是用机器人运动学和相机标定把触觉位置投影到图像平面，并显式处理运动学和标定误差带来的空间不确定性。. [相关研究](https://arxiv.org/abs/2606.08765).

Tactile-WAM 甚至给了一个反例：接触任务里的视觉未来可能看起来合理，但物理上不完整；可如果无约束注入触觉 表征单元，又可能产生 tactile pollution，让视频和动作预测都退化。. 所以多模态不是“越多越好”，而是要回答三个工程问题：什么时候读、读到哪个控制层、怎么防止它污染原来的视觉先验。 [相关研究](https://arxiv.org/abs/2606.26663).

### 误区三：模型失败就是输出错了

VLA 的麻烦在于，它可能没有一个好用的“我不确定”信号。两篇 2026 年 6 月论文分别从 hidden activation perturbation 和 velocity-field disagreement 出发，把不确定性变成失败检测和主动微调信号。, . 这对部署很关键：如果机器人不知道自己正在分布外，就很难决定停下、求助、重试还是进入恢复策略。 [相关研究](https://arxiv.org/abs/2606.20754), 相关研究.

PATCH 进一步提醒，光有全局异常分数也不够。一个路人进入画面、背景移动、手边目标被遮挡，视觉上都可能“异常”，但不一定影响当前动作；关键是异常是否落在 动作片段 将要使用的执行走廊里。. [相关研究](https://arxiv.org/abs/2606.16690).

### 误区四：成功率够高就说明感知够可靠

SoftVTBench 的观点很适合拿来泼冷水：柔性物操作不能只看 Goal Success，还要看有没有滑移、掉落、过度形变。一个策略把东西送到目标位置，但过程中捏坏了、拉变形了，在真实生产里并不是成功。. [相关研究](https://arxiv.org/abs/2607.04234).

世界模型评测也有类似问题。看起来很真的视频，不代表它会按机器人的动作正确演化；如果把这种生成式世界模型当 test oracle，就要先验证它的 admissibility，而不是只看视觉质量。. [相关研究](https://arxiv.org/abs/2607.07196).

## 一个更实用的框架

可以把具身传感器感知误差拆成四层：观测层，处理遮挡、照明、反光、深度和位姿；接触层，处理滑移、力、形变和稳定性；融合层，处理标定、同步、表征单元 注入和模态污染；评测层，处理闭环成功、安全过程和世界模型可信度。这是对 12 条证据的综合推论，不是单篇论文的原话。 [相关研究](https://arxiv.org/abs/2606.08765), 相关研究, 相关研究.

## 边界与可信度

这组证据不支持“所有任务都必须上触觉”。它支持的是按任务建立误差预算：先确认不可观测状态和失败后果，再决定补视觉、触觉、力觉、事件流，或补动作条件监控。多数证据仍来自特定 基准测试、仿真或作者报告的实机设置，跨实验室复现、长期漂移和跨传感器实例泛化仍不足（inference；综合 [相关研究](https://arxiv.org/abs/2606.26663), 相关研究, 相关研究）。

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

完整证据条目见 随附证据附录。
