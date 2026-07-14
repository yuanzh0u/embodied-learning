# 4D时空推理对数据的需求：专家解释帖

## TL;DR

这一版不只核对摘要，而是对 15 篇入选论文逐篇阅读方法、结果与局限。下文只保留能在完整正文中重新定位的判断。

4D时空推理不是给机器人多看视频就会自然出现的能力。它需要的数据，是一套能把“3D空间中的对象运动、机器人动作、接触状态、失败恢复”对齐到同一时间轴上的监督系统。

最简洁的回答是：要有4D几何轨迹，要有真实机器人动作 grounding，要有触觉/力等接触传感，要有失败与恢复数据，还要有严格的数据同步和质量治理。

## 误区：为什么“更多视频”不够

普通视频只告诉模型画面怎么变，但机器人要知道的是：同一个杯沿、抽屉把手、柔性布料或工具尖端在3D空间里怎么移动，机器人末端执行器该怎样跟上，以及接触有没有成功。

GEM-4D把这个问题讲得很清楚：视频可以看起来逼真，但跨帧3D对应关系错了，动作提取就会失败（[相关研究](https://arxiv.org/abs/2605.22882)）。所以4D数据首先要补的不是审美质量，而是物理对应一致性。

## 真实机制

第一层是几何时序监督。3PoinTr、Pri4R、Kinema4D和GEM-4D都在用不同形式表达同一个需求：3D point tracks、robot pointmaps、geometry teacher features、跨帧correspondence。这些数据告诉模型“世界中的点随时间怎么动”（[相关研究](https://arxiv.org/abs/2603.08485), 相关研究, 相关研究, 相关研究）。

第二层是可执行动作。人类视频能提供丰富物体动态，但没有机器人可直接执行的动作。τ0-WM把数据分成真实机器人远程操作、UMI式交互、第一视角人类视频、失败推演，并用不同mask控制每类数据能监督什么（, [τ_0-WM](https://arxiv.org/abs/2606.01027)）。这就是关键：不能把所有数据都当成同一种真值。

第三层是接触传感。很多4D推理失败不发生在“看见物体”阶段，而发生在接触、滑移、插入、擦拭、形变、抓取稳定性这些视觉不可靠的瞬间。TacForeSight用腕部力/力矩预测未来触觉潜在状态，Dream-Tac联合预测未来视觉、未来触觉和动作，HapTile则从数据集层面同步记录语言、视觉、触觉、状态和动作（[相关研究](https://arxiv.org/abs/2606.11184), 相关研究, 相关研究）。

第四层是失败和恢复。世界模型如果只能生成成功案例，就很难做动作筛选和修正。Kinema4D合成失败轨迹，TacForeSight显式收集扰动恢复示教，WEAVER和τ0-WM都把候选动作的评估/进度/奖励纳入部署逻辑（[相关研究](https://arxiv.org/abs/2603.16669), 相关研究, 相关研究）。

第五层是数据质量。HapTile强调同步、timestamp 空白、动作-状态一致性、episode-level split和触觉标记跟踪；UMI示教质量研究提醒我们，采集硬件本身会决定示教是否可学（[相关研究](https://arxiv.org/abs/2606.04825), 相关研究）。

## 一个容易忽略的分歧

4D监督不一定要在推理时输入。Pri4R和GEM-4D都展示了一种路线：训练期用点轨迹或几何教师把时空结构蒸馏进模型，推理期不增加额外输入或计算（[相关研究](https://arxiv.org/abs/2603.01549), 相关研究）。

这对数据建设很重要：我们可以先把复杂标注用于训练期，而不是要求部署端永远带着昂贵的完整4D传感栈。

## 最小可行数据规范

如果要为4D时空推理设计一个新数据集，我会把最低要求写成六项：

1. 同步多视角RGB或RGB-D，并保留相机/时间戳信息。
2. 机器人状态、动作chunk、末端执行器轨迹必须与视频对齐。
3. 至少提供一种4D几何监督：点轨迹、pointmap、scene flow、geometry-teacher feature或可复现伪标注。
4. 对接触任务，记录触觉、腕部力/力矩或等价接触事件信号。
5. 收集失败、近失误、扰动恢复和任务进度/奖励标签。

6. 明确每类数据的监督权限：robot demo监督动作，人类视频监督视觉动态，UMI式数据只能作为较弱动作式信号。

## 可信度与边界

较稳妥的结论是：4D数据需求已经从“视频规模”转向“多层监督结构”。但许多结果仍是论文内评测，尤其触觉世界模型和4D生成式仿真还需要跨平台、跨任务、跨实验室复现。读者不应把本文列出的数据层直接理解成一张通用采购清单；具体任务仍要先判断哪些状态不可观、哪些动作必须闭环验证。

## 延伸阅读
- [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882)
- [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485)
- [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027)
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184)
- [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669)
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825)
- [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549)
