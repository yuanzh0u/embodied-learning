# 过去一年，具身智能的数据质量为什么变成核心矛盾？

## TL;DR

如果只看一句话：机器人数据质量已经从“多采一点、脏数据删掉”变成“哪些数据、在什么任务上、以什么粒度、通过什么采集接口、怎样进入训练”的系统问题。近一年几篇论文分别从 influence functions、遥操作反馈、轨迹 PSD、多样性、跨本体均衡、人类视频过滤和 suboptimal data 利用切入，合起来指向同一个结论：数据质量不是数据集自带的标签，而是数据和目标策略之间的关系 [相关研究](https://arxiv.org/abs/2603.09056), 相关研究, 相关研究。

## 检索范围

- 时间范围：2025-07-08至2026-07-08。
- 证据规模：12 篇论文、12 条 已接纳证据，达到正式解释稿门槛。
- 边界：arXiv/public-paper snapshot，不是同行评审论文普查；完整事件立场、置信度和定位见 随附证据附录。

## 真实机制

### 误区一：成功轨迹就是好轨迹

遥操作采集里，很多 episode 是“任务成功但学习上很差”：动作绕、停顿多、反复纠正、接近关节极限。DQAF 这篇论文直接反对只按成功/失败验收，它把 episode 质量拆成任务进度、平滑性、停顿和 kinematic 限制s，并把反馈即时给采集员 [相关研究](https://arxiv.org/abs/2605.26349)。PSD metric 论文也把低质量 end-user 示教落到轨迹频域上：过多纠正、振荡和突兀调整会伤害 imitation learning，可以用 PSD 做快速排序 相关研究。

### 误区二：数据多样性越高越好

多样性当然重要，但不能单独等于质量。FAKTUAL 用 trajectory-kernel entropy 度量机器人数据集多样性，并用高熵子集做 curation，但作者也明确说，这个方法不保证只选择高质量轨迹；如果数据里有有害或病态轨迹，单纯最大化 diversity 可能出问题 [相关研究](https://arxiv.org/abs/2603.11634)。ATHENA 从 VLA 微调角度补了另一半：如果只按全局效用排序，某些任务会被几乎删光，所以质量筛选还要守住任务覆盖 相关研究。

### 误区三：坏数据只能删

长程示教很微妙，一条看起来次优的轨迹里可能有停顿、失误，也可能有宝贵的恢复动作。WARP-RM 的核心思路就是别只做 episode-level keep/drop，而是学习 frame/chunk 级 progress signal，把高价值 动作片段s 权重提上来 [相关研究](https://arxiv.org/abs/2606.28320)。

Ambient Diffusion Policy 更激进：suboptimal data 会一直伴随机器人数据扩张，过滤全部坏数据既浪费，普通 co-training 又会学到 harmful parts，所以要控制 suboptimal samples 在训练过程中何时贡献 相关研究。

### 更底层的问题：质量从采集工具就开始了

UMI gripper 论文很有启发：同样是采示教，手持 gripper 的力分布、重量和人体工学会影响操作者表现，最后影响学到的策略 [相关研究](https://arxiv.org/abs/2603.17189)。VR 示教论文也类似，它发现输入设备和可视化会改变轨迹效率、不必要动作和精度，而且不同任务偏好不同交互方式 相关研究。这意味着数据团队不能把质量部门放在采集之后，采集工具本身就是数据质量的一部分。

### 人类视频和跨本体数据：便宜，但不是免费午餐

人类视频很诱人，因为规模大，但 PSI 论文指出，人类视频中的物体轨迹要先通过仿真过滤，排除 pose estimation error、机器人不可达轨迹和 grasp 不兼容，否则这些数据可能伤害机器人学习 [相关研究](https://arxiv.org/abs/2602.13197)。跨本体数据也类似，OXE-AugE 论文指出 OXE 的真实数据高度集中在少数 robot types，top four robot types 超过 85%，这会带来 robot-scene 过拟合风险，所以跨本体质量还包括本体和夹爪分布是否均衡 相关研究。

## 一个更实用的定义

可以把具身智能数据质量理解成五层：采集接口是否让人产生好示教，轨迹是否健康，数据是否对目标任务有用，覆盖是否均衡，坏数据是否被正确过滤、降权或分阶段利用。

这个定义不是某一篇论文的原话，而是对近一年证据的综合推论：QoQ/IWR 负责“目标有用性”，DQAF/PSD/UMI/VR 负责“采集和轨迹健康”，ATHENA/OXE-AugE 负责“覆盖均衡”，PSI/WARP-RM/Ambient Diffusion Policy 负责“异构和弱质量数据如何进入训练” [相关研究](https://arxiv.org/abs/2603.09056), 相关研究, 相关研究, 相关研究, 相关研究。

## 边界与可信度

过去一年最值得注意的变化，是大家不再相信“更大数据集自动带来更好机器人”。更准确的说法是：机器人需要更可用的数据资产，而可用性来自采集端、筛选端、覆盖端、训练端和闭环评估端共同控制。这里的 caveat 是，当前论文大多仍在特定任务、数据集或模型上验证，还没有一个跨任务统一质量 基准测试；所以最稳妥的工程路线，是先把质量指标拆开记录，再用目标策略闭环收益校准 [相关研究](https://arxiv.org/abs/2605.01544), 相关研究, 相关研究。

## 一个反例：最高分数据也可能让系统退化

假设筛选器偏爱动作平滑、任务常见的轨迹，它会持续选中容易任务，却把少数困难任务和恢复动作排除。整体训练损失可能下降，真实部署一遇到长尾状态就失效。质量因此必须同时考虑目标效用和覆盖，不能只看单条轨迹分数。

## 边界：质量排序会随目标变化

同一条示教对某个机器人、某项任务很有用，换本体或控制器后可能不再兼容。任何质量结论都应绑定目标策略和数据版本，并用闭环复测更新；离开这些条件，没有永久有效的“黄金数据”。

## References

- [2509.01657](https://arxiv.org/abs/2509.01657) Data Retrieval with Importance Weights for Few-Shot Imitation Learning.
- [2512.13100](https://arxiv.org/abs/2512.13100) OXE-AugE.
- [2602.10618](https://arxiv.org/abs/2602.10618) From Interaction to Demonstration Quality in Virtual Reality.
- [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works.
- [2603.09056](https://arxiv.org/abs/2603.09056) Quality over Quantity.
- [2603.11634](https://arxiv.org/abs/2603.11634) Diversity You Can Actually Measure.
- [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality.
- [2605.01544](https://arxiv.org/abs/2605.01544) An Efficient Metric for Data Quality Measurement in Imitation Learning.
- [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation.
- [2606.12365](https://arxiv.org/abs/2606.12365) Ambient Diffusion Policy.
- [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA.
- [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM.
