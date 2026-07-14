# 具身机器人为什么总在“最后一厘米”翻车？近半年论文给了一个答案：它没真的看见接触

## TL;DR

这一版不只核对摘要，而是对 15 篇入选论文逐篇阅读方法、结果与局限。下文只保留能在完整正文中重新定位的判断。

很多人把机器人感知误差理解成“摄像头识别错了”。近半年具身智能论文里更有意思的趋势是：真正难的不是识别杯子，而是闭环控制中那些 RGB 看不见、模型又没把握的状态，比如滑移、接触法向、力不匹配、透明/反光表面的位姿、照明退化和动作执行过程中的局部扰动。。 [相关研究](https://arxiv.org/abs/2607.07287), 相关研究.

## 这篇回答讨论什么

这里讨论的是 2026 年上半年公开论文呈现出的机制：感知误差如何从相机观测一路传播到接触、融合、动作置信度和闭环评测。它不是一份传感器采购榜，也不把预印本中的局部结果当成跨实验室共识。

## 真实机制

### 误区一：视觉强了，传感器问题就结束了

视觉确实是机器人通用语义能力的底座，但它不是物理接触的全知传感器。TouchWorld 这类工作把失败直接写成滑移、错位、不稳定抓取和力不匹配；MuSe 也指出 force、tactile、audio 会揭示图像不可直接观测的 interaction states。。 也就是说，机器人“看见了物体”不等于“知道手指和物体之间正在发生什么”。 [相关研究](https://arxiv.org/abs/2607.07287), 相关研究.

遮挡、弱光、反光和透明表面会把这个问题进一步放大。YOTO 的 6-DoF pose 论文把这些条件列为视觉位姿估计的失败场景，并展示单次双触点触觉可以在视觉不可靠时补位；Event-VLA 则从另一端处理照明变化，用事件流补充 RGB-centric VLA 的可见性退化。。 [相关研究](https://arxiv.org/abs/2606.28899), 相关研究.

### 误区二：多加传感器就能解决

更准确的说法是：加传感器只解决“可观测性”，不自动解决“融合误差”。RGB-S 的做法很典型：它不是把触觉粗暴拼到视觉 token 里，而是用机器人运动学和相机标定把触觉位置投影到图像平面，并显式处理运动学和标定误差带来的空间不确定性。. [相关研究](https://arxiv.org/abs/2606.08765).

Tactile-WAM 甚至给了一个反例：接触任务里的视觉未来可能看起来合理，但物理上不完整；可如果无约束注入触觉 token，又可能产生 tactile pollution，让视频和动作预测都退化。. 所以多模态不是“越多越好”，而是要回答三个工程问题：什么时候读、读到哪个控制层、怎么防止它污染原来的视觉先验。 [相关研究](https://arxiv.org/abs/2606.26663).

### 误区三：模型失败就是输出错了

VLA 的麻烦在于，它可能没有一个好用的“我不确定”信号。两篇 2026 年 6 月论文分别从 hidden activation perturbation 和 velocity-field disagreement 出发，把不确定性变成失败检测和主动微调信号。。 这对部署很关键：如果机器人不知道自己正在分布外，就很难决定停下、求助、重试还是进入恢复策略。 [相关研究](https://arxiv.org/abs/2606.20754), 相关研究.

PATCH 进一步提醒，光有全局异常分数也不够。一个路人进入画面、背景移动、手边目标被遮挡，视觉上都可能“异常”，但不一定影响当前动作；关键是异常是否落在 动作片段 将要使用的执行走廊里。. [相关研究](https://arxiv.org/abs/2606.16690).

### 误区四：成功率够高就说明感知够可靠

SoftVTBench 的观点很适合拿来泼冷水：柔性物操作不能只看 Goal Success，还要看有没有滑移、掉落、过度形变。一个策略把东西送到目标位置，但过程中捏坏了、拉变形了，在真实生产里并不是成功。. [相关研究](https://arxiv.org/abs/2607.04234).

世界模型评测也有类似问题。看起来很真的视频，不代表它会按机器人的动作正确演化；如果把这种生成式世界模型当 test oracle，就要先验证它的 admissibility，而不是只看视觉质量。. [相关研究](https://arxiv.org/abs/2607.07196).

## 一个更实用的框架

可以把具身传感器感知误差拆成四层：观测层，处理遮挡、照明、反光、深度和位姿；接触层，处理滑移、力、形变和稳定性；融合层，处理标定、同步、token 注入和模态污染；评测层，处理闭环成功、安全过程和世界模型可信度。这是多篇论文共同支持的分析框架，不是单篇论文的原话。[相关研究](https://arxiv.org/abs/2606.08765)

## 边界与可信度

这组证据不支持“所有任务都必须上触觉”。它支持的是按任务建立误差预算：先确认不可观测状态和失败后果，再决定补视觉、触觉、力觉、事件流，或补动作条件监控。多数证据仍来自特定 基准、仿真或作者报告的实机设置，跨实验室复现、长期漂移和跨传感器实例泛化仍不足（综合 [相关研究](https://arxiv.org/abs/2606.26663), 相关研究, 相关研究）。

## 延伸阅读
- [TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation](https://arxiv.org/abs/2607.07287)
- [You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact](https://arxiv.org/abs/2606.28899)
- [RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation](https://arxiv.org/abs/2606.08765)
- [Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention](https://arxiv.org/abs/2606.26663)
- [Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models](https://arxiv.org/abs/2606.20754)
- [PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation](https://arxiv.org/abs/2606.16690)
- [SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objects](https://arxiv.org/abs/2607.04234)
- [Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators](https://arxiv.org/abs/2607.07196)
