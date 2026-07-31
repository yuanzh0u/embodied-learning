# VLA 为什么成为主流，而原子技能没有消失：2023—2026 年具身机器人技术路线复盘

## 摘要

本文研究 2023 年 7 月至 2026 年 7 月间具身机器人“原子技能”与视觉—语言—动作模型（Vision-Language-Action, VLA）的技术演进。检索覆盖 atomic skill、primitive、skill library、hierarchical policy、task decomposition、skill chaining 等异名概念；在 612 篇候选中恢复 56 篇全文，最终以完整非 OCR 全文、结构化论文笔记和主张支持审计为门槛纳入 15 篇。中心判断是：**主流并非在 VLA 与原子技能之间二选一，而是选择 VLA 作为可规模化的共享表征与预训练底座，同时把原子技能下沉为专家路由、局部策略、层级接口和执行契约。** 早期独立技能库没有成为统一主线，主要因为它必须预先承担技能边界、语义本体、终止条件、跨技能状态和失败恢复等接口成本；VLA 则先利用视觉语言预训练、跨机器人数据混合和统一微调接口获得规模收益。随着任务转向长时程、真实闭环和跨本体部署，单体 VLA 的局限又推动系统重新引入技能化结构。因此，更准确的趋势不是“VLA 取代原子技能”，而是“VLA 基座化，技能模块化，执行契约显式化”。

## 1. 研究边界：什么才算原子技能

“原子技能”在近三年论文中并不是稳定术语。同一类对象可能被称为 primitive、motor primitive、option、skill policy、skill library、subtask 或 action expert。本文将它操作化为：**一个可复用、有限时域、闭环执行的策略单元，具有参数化目标，并至少隐含前置条件、完成/终止判据以及失败语义。** 这一定义排除了仅为提高训练效率而切出的任意动作片段，也不把每个离散动作 token 自动视为技能。

这个口径很重要。若只统计标题含 atomic skill 的论文，会低估技能化研究；若把所有 action chunk 都算作技能，又会把原子技能概念稀释到失去解释力。本文因此同时检索直接命名和相邻技术路线，并把“为何 VLA 成为主流”视为跨论文的机制性推断，而不是某一篇论文可以单独证明的事实。

## 2. 中心判断：为什么 VLA 先赢得了主流资源

### 2.1 VLA 给出了更清晰的规模化路径

Open X-Embodiment/RT-X 把多机构、跨机器人数据汇入统一训练框架，并在其跨本体消融中观察到更大的模型容量带来更好的跨数据集迁移。这给研究社区一个非常明确的工程信号：数据集可以合并、模型可以扩容、迁移效果可以用统一基准观察 [Open X-Embodiment](https://arxiv.org/abs/2310.08864)。Octo 随后进一步显示，在其 WidowX 实验中，宽跨本体数据混合、ViT 骨干与 diffusion action head 的组合优于窄数据或替代动作头，说明视觉表征、数据规模与连续动作生成可以在同一训练配方内共同优化 [Octo](https://arxiv.org/abs/2405.12213)。

相比之下，独立技能库在增加数据之前，往往先要回答“切成什么技能”“不同机器人是否共享同一技能语义”“技能何时完成”“上一个技能留下的状态是否满足下一个技能的输入条件”。这些问题并非不能解决，但它们使新增数据不再是简单追加样本，而要同步维护技能本体和接口。技术路线因此呈现不对称：VLA 首先把复杂性吸收到大规模联合建模中，原子技能路线则较早暴露了结构设计成本。

### 2.2 VLA 建立了统一的复用与适配接口

OpenVLA 把开源预训练模型、通用输入形式和下游微调流程组合起来，表明一个预训练 VLA 可以作为新机器人的可复用初始化；但其部署仍需约 10—150 条目标任务演示，说明“通用底座”并不等于零成本落地 [OpenVLA](https://arxiv.org/abs/2406.09246)。π0 则把通用视觉语言骨干与专门处理连续动作的 flow-matching action expert 结合，在 10,000 小时、7 类机器人配置和 68 个任务的混合数据上训练 [π0](https://arxiv.org/abs/2410.24164)。这一步尤其关键：它说明 VLA 不必保持完全同质的端到端结构，也可以在共享表征之上容纳动作专家。

因此，VLA 赢得主流并不意味着研究者认定“技能没有价值”，而是它提供了更低摩擦的公共入口：相同的视觉语言先验、相似的数据格式、可发布的权重和可复现的微调范式。对实验室而言，这比先设计一套只能在特定机器人上成立的技能目录更容易形成累积效应。

### 2.3 论文与基准更容易奖励端到端规模收益

这是本文基于证据分布作出的推断：跨本体预训练、平均成功率和统一基准能形成醒目的横向比较；而原子技能的主要价值——可诊断性、局部替换、明确交接与故障隔离——通常要到长任务或真实部署中才显现，评价成本更高，也更依赖系统定义。换言之，VLA 更容易展示“能力边界向外扩张”，技能化架构更擅长解决“能力如何可靠拼接”。前者天然更适合形成基础模型主线，后者则更像运行时和系统工程问题。

## 3. 原子技能路线其实一直在发展

2024 年的 DexSkills 利用触觉与本体信号把接触丰富的长演示分割为可复用 primitive skills，再以独立策略组合执行，证明技能分解在灵巧操作中具有明确价值；但其证据限于预定技能集合与特定灵巧手 [DexSkills](https://arxiv.org/abs/2405.03476)。2025 年的原子技能库工作更直接地把视觉语言规划器用于任务分解，再微调 VLA 实现具体技能；技能粒度因此取决于 VLA 本身的可塑性，而非独立于 VLA 的固定目录 [Atomic Skill Library](https://arxiv.org/abs/2501.15068)。

DeCo 展示了技能组合对未见长任务的价值，同时也暴露了它的两类脆弱点：高层 VLM 可能产生状态幻觉，原子指令与训练分布偏移也会降低部分单技能表现 [DeCo](https://arxiv.org/abs/2505.00527)。这说明“拥有一组会做的技能”不等于“能稳定完成技能链”。2026 年关于语义交接失败的诊断进一步区分了快照状态下的 skill competence 与链式执行中的 chained-state robustness：如果前置/后置条件、步级验证和恢复机制没有显式化，单技能成功率并不能推出长任务成功率 [Semantic Handoff Failures](https://arxiv.org/abs/2607.06256)。

这些工作共同解释了原子技能为何没有单独统治主流：它不是一个只靠增加技能数量就能扩展的平面库，而是一套必须处理边界、状态迁移和恢复的协议系统。技能越多，潜在交接关系越多；如果没有类型化接口，组合错误会随任务长度累积。

## 4. 真正的新趋势：原子技能迁入 VLA 内部

近期结果已经把“VLA 对原子技能”这个二分法拆掉。AtomicVLA 用语义原子技能路由混合专家，在 LIBERO-LONG 上报告 95.2% 成功率，比 token-level MoE 高 6.6 个百分点 [AtomicVLA](https://arxiv.org/abs/2603.07648)。这里的原子技能不是 VLA 外部的手工控制器，而是模型内部决定专家分工的语义单位。

LiLo-VLA 采用另一种混合方式：几何搬运负责可解析运动，物体中心局部 VLA 处理需要语义感知的局部操作，再加动态重规划、恢复与技能复用。在论文的两个长时程仿真套件上，它的平均成功率为 69%，对比 π0.5 的 28% 和 OpenVLA-OFT 的 2% [LiLo-VLA](https://arxiv.org/abs/2602.21531)。该结果不能直接外推到所有真实机器人，但它清楚表明：当评价对象从单段反应式操作变成长时程任务时，把所有责任压给一个全局端到端策略未必最优。

H-WM 进一步把低频符号逻辑、潜在视觉子目标与高频 VLA 动作块连接起来。在五个 5—7 步 LIBERO-LoHo 任务上，双层逻辑与视觉引导的平均成功率比仅逻辑引导高 16.4 个百分点；代价是额外训练、系统复杂度，以及任务必须能够被有意义地表示为结构化逻辑状态 [H-WM](https://arxiv.org/abs/2602.11291)。ReCoVLA 则把失败类型与恢复阶段的判断交给 VLM，把具体纠正留给 residual policy，展示了认知层和控制层可分离的恢复结构；与此同时，VLM 的失败分类本身又成为独立错误源 [ReCoVLA](https://arxiv.org/abs/2606.09630)。

由此看，原子技能没有退出技术发展，而是发生了三种迁移：从手工技能目录迁到语义专家路由，从完整任务控制器迁到局部策略，从隐式动作片段迁到带验证和恢复的执行契约。

## 5. 为什么单体 VLA 仍不足以成为最终系统

跨本体动作并不是天然通用的监督信号。同一控制命令在不同控制器、机器人形态、硬件个体和部署动力学下可能产生不同运动 [SPACE](https://arxiv.org/abs/2606.24049)。离散动作 token 虽然为自回归 VLA 提供紧凑接口，但固定 token 在不同关节状态和接触条件下需要解码成不同连续控制，这也是 SA-VLA 试图用本体状态条件化解码解决的问题 [SA-VLA](https://arxiv.org/abs/2606.30113)。真实 UR5 实验还指出，离线指标并不会自动转化为稳定闭环行为；动作语义、坐标系、模态时间对齐、图像预处理和数据覆盖需要同时受控 [UR5 VLA study](https://arxiv.org/abs/2606.30456)。

这些限制意味着未来系统更可能形成五层结构：共享 VLA 负责语义与视觉先验；层级规划器或世界模型维持长程状态；技能/动作专家承担局部闭环；本体适配器处理坐标、控制与动力学差异；执行管理器显式检查前后置条件、完成信号和恢复路径。这里的“原子性”不是越细越好，而是要以能否独立验证、复用和恢复为准。

## 6. 结论、边界与可证伪条件

近三年的主流选择可以概括为：**先用 VLA 解决共享表征、数据聚合和通用初始化，再用技能化结构解决长时程可靠性、专家分工和系统可维护性。** 原子技能作为独立品牌显得边缘，是因为技能本体与组合协议难以跨机器人统一，也因为其收益在现有基准中不如规模曲线醒目；但在技术内核上，它正以更成熟的形式回归。

这一判断仍有三个边界。第一，纳入证据以 arXiv 和公开全文为主，2026 年论文多处于预印本阶段。第二，不同论文的机器人、任务和成功率不可直接横比，本文仅在论文自己的对照设置内引用数值。第三，“主流关注”的解释包含对研究生态的推断，不是因果实验。

它也可以被证伪：如果一种固定或自动发现的原子技能架构，在匹配数据、算力和本体范围后，能够不依赖共享 VLA 底座，仍达到相当的跨任务、跨本体扩展性，并且无需高昂的技能本体与接口维护成本，那么“VLA 是更优公共底座”的判断就应被削弱。当前证据更支持的不是路线淘汰，而是层次分工。

## References

1. Open X-Embodiment Collaboration. [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864), 2023.
2. Octo Model Team. [Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213), 2024.
3. Kim et al. [OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246), 2024.
4. Black et al. [π0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164), 2024.
5. Davchev et al. [DexSkills: Skill Segmentation Using Haptic Data for Learning Autonomous Long-Horizon Robotic Manipulation Tasks](https://arxiv.org/abs/2405.03476), 2024.
6. [Learning an Atomic Skill Library for Long-Term Robotic Tasks](https://arxiv.org/abs/2501.15068), 2025.
7. [DeCo: Skill Decomposition and Composition for Zero-Shot Generalization in Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2505.00527), 2025.
8. [LiLo-VLA: Reusable Skill Learning for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2602.21531), 2026.
9. [AtomicVLA: Semantic Skill Routing for Vision-Language-Action Models](https://arxiv.org/abs/2603.07648), 2026.
10. [Semantic Handoff Failures in Chained Vision-Language-Action Skills](https://arxiv.org/abs/2607.06256), 2026.
11. Huang et al. [H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model](https://arxiv.org/abs/2602.11291), 2026.
12. Hu et al. [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630), 2026.
13. [SPACE: State-Change-Aware Cross-Embodiment Action Representation](https://arxiv.org/abs/2606.24049), 2026.
14. Jiang et al. [SA-VLA: State-aware Tokenizer for Improving Vision-Language-Action Models' Performance](https://arxiv.org/abs/2606.30113), 2026.
15. Hochedel and Lalonde. [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456), 2026.
