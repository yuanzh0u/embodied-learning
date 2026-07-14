# 语言稀疏性、动作连续性与稠密视觉造成的多模态对齐难题研究备忘录

## 摘要

本文综述一个正在 VLA / 机器人基础模型中变得清晰的问题：语言、视觉和动作并不是三种可直接拼接的 表征单元 流。语言通常以任务级或阶段级指令出现，语义稀疏、时间标注粗；图像/视频是高维稠密信号，容易主导训练；动作是连续、闭环、受本体和控制器约束的物理量。近六个月的论文显示，失败常不是某个 backbone 不够大，而是语言-动作、视觉-动作、动作-控制器三条接口没有被显式对齐。

## 研究边界

- 检索时间：2025-12-30至2026-06-30；另以经典论文作背景基线，不把旧论文当作最新发现。
- 知识路由：相关知识单元, 相关知识单元, 相关知识单元, 相关知识单元。
- 证据层：10 篇 arXiv HTML 正文级论文，10 条 evidence events，全部 `confidence: 直接证据`。
- 限制：本综述聚焦机器人/VLA，不覆盖一般多模态大模型的全量图文对齐文献；2026 年论文多为预印本，结论应按“当前证据”而非领域共识处理。

## 背景脉络

RT-1 把大规模真实机器人数据、语言指令和视觉观测接到 Transformer 控制策略上，提出机器人也可能走 scaling 路线。RT-2 进一步把 VLM/VQA 风格的互联网语义知识迁移到机器人动作输出。Open X-Embodiment / RT-X、Octo、OpenVLA 则把跨机器人数据、通用策略和开源 VLA 推向主流。

与此同时，Diffusion Policy 和 `π0` 代表了另一条线：用扩散或 flow matching 处理连续、高维、可多峰的动作分布。

这条历史脉络解释了为什么 2026 年的新论文开始集中处理“接口”问题：VLM 提供语义和视觉先验，但机器人动作不是语言 表征单元，也不是图像 patch；动作要通过本体、控制器、状态估计和接触反馈落到物理世界。

## 中心判断

### 语言稀疏

语言在机器人数据中常是每条轨迹一个任务描述，或每个阶段一个低频标签。它表达“目标、约束、子任务”，但很少逐帧标注“此刻为什么这么动”。LA4VLA 直接指出，标准 VLA 预训练中，密集的 视觉—动作 supervision 会压过相对稀疏的 语言—动作 signal，导致策略学到视觉捷径而不是语言如何约束动作（[相关研究](https://arxiv.org/abs/2606.27295)）。

这带来一个重要推论：如果语言只在输入端作为 prompt 出现，而没有阶段级、动作级或因果级监督，它很容易成为装饰性条件。ZR-0 的 dense embodied chain-of-thought 方向可以理解为把稀疏语言“加密”：把场景描述、任务进度、未来计划、原子子任务、目标框和离散动作 表征单元 作为 dense supervision，使高层认知过程更细粒度地对齐到动作专家（[相关研究](https://arxiv.org/abs/2606.30552)）。

### 动作连续

动作不是自然语言词表。离散 动作标记 对 autoregressive VLA 很友好，但会带来压缩和解码问题：同一个 表征单元 在不同关节状态、物体位姿、接触条件下不应解码成同一个连续控制量。SA-VLA 因此把机器人状态注入 动作标记izer，试图缩小离散 表征单元 到连续控制之间的 compression 空白（[相关研究](https://arxiv.org/abs/2606.30113)）。

另一类论文绕开“先离散再还原”的瓶颈，用 flow matching / diffusion 直接学习连续动作流。Learning Action Priors for Cross-embodiment Robot Manipulation 的关键判断是：VLA 从 VLM 继承了视觉和语言先验，但 action module 往往从零学习物理运动；

先用无视觉、无语言的动作轨迹预训练 运动先验，再把它迁移到 VLA 对齐阶段，可以减轻早期训练同时学习 temporal action dynamics 和 cross-modal alignment 的负担（[相关研究](https://arxiv.org/abs/2606.26095)）。

### 视觉稠密

图像/视频在 表征单元 数量和时序密度上天然强势。它们携带几何、纹理、遮挡、对象状态和背景相关性，但也容易让模型用 spurious visual correlation 代替语言条件。LA4VLA 把这个问题表述得很直接：视觉-动作监督时间上更稠密、更动态，而语言-动作监督语义变化少、缺少局部阶段对齐（[相关研究](https://arxiv.org/abs/2606.27295)）。

近期论文的一个共同策略不是“少用视觉”，而是让视觉变得更结构化、更动作相关。Sparse2Act 用 task-space end-effector actions 监督 sparse 3D 表征单元s，把视觉几何组织到可执行的工作空间运动上（[相关研究](https://arxiv.org/abs/2606.12759)）。

SSI-Policy 则构造 RGB-only structured scene interface，把 monocular depth、language-grounded object layout 和 instruction-conditioned 2D motion trajectory 放到中间层，再交给 diffusion action planner；这等于在视觉和控制之间加了一个可解释、任务对齐的空间接口（[相关研究](https://arxiv.org/abs/2606.26800)）。

### 物理闭环

真实机器人中的 action 不是抽象标签，而是控制器输入。SPACE 指出，不同机器人甚至同一型号不同硬件单元中，同一 action command 都可能产生不同 motion；因此它用 Cartesian state delta 做共享动作表示，再用 Action Adapter 转成具体机器人控制命令（[相关研究](https://arxiv.org/abs/2606.24049)）。

接触任务进一步暴露了视觉的边界。Transferring Contact, Not Just Motion 说明，灵巧操作中只对齐 motion 不够，稳定抓取还要对齐 contact loading 和 force feedback；视觉在手指自遮挡下恢复接触状态很弱，需要力/触觉/本体感受补充（[相关研究](https://arxiv.org/abs/2606.15516)）。

## 核心机制

### 1. 对齐难题本质上是粒度错配

语言粒度粗，视觉粒度细，动作粒度连续。把它们统一成 表征单元 后，表面上进入同一个模型，实际上仍有三个未解决的 mapping：语言目标如何落到动作阶段，视觉几何如何落到可执行位姿，连续控制如何适配本体和控制器。

当前论文的共同趋势是为每个 mapping 引入更强的中间约束，例如 dense ECoT、语言—动作 pretraining、state-aware 动作标记izer、action prior、structured scene interface、Cartesian state delta。

### 2. 视觉不是越稠密越好，关键是稠密信号是否被动作约束

图像 patch、视频帧和多视角输入可以提供大量信息，但也会制造捷径。Sparse2Act 和 SSI-Policy 的价值在于把视觉压缩成 action-aligned geometry 或 task-aligned scene interface，而不是让视觉 表征单元 自己决定什么重要。换句话说，机器人视觉表征的目标不只是识别对象，而是把对象、空间关系和动作可达性放到同一坐标系里。

### 3. 动作空间是 VLA 与普通 VLM 的最大分水岭

普通 VLM 可以用文本 表征单元 作为输出；VLA 的输出必须被控制器执行。动作可以被离散化，但离散 表征单元 最后仍要还原到连续控制；动作可以直接用 flow/diffusion 生成，但还要匹配本体、频率、延迟、坐标系和安全约束。SA-VLA、Action Prior、SPACE、Rethinking VLA Scaling 都在从不同角度回答同一个问题：动作表征应该以物理状态变化和控制可执行性为中心，而不是以模型输出便利性为中心。

### 4. 跨本体 scaling 的瓶颈不是数据量，而是数据兼容性

Open X-Embodiment/RT-X 让“跨机器人大数据”成为可能，但 2026 年的证据明显更谨慎。Rethinking VLA Scaling 指出，机器人数据在本体、传感器、频率和动作空间上异构，朴素混合可能负迁移；SPACE 进一步说明 action command 本身不是通用标签。由此可推断：未来的数据 scaling 需要 metadata、action adapter、坐标系统一、质量审计和任务族分层，而不是简单合并轨迹。

### 5. 接触状态是视觉-语言-动作三元组的盲区

对于开放空间抓放，RGB + language + action 可能足够；但对滑移、柔顺贴合、灵巧抓握、插入和易碎物，关键状态常在视觉遮挡后发生。Transferring Contact, Not Just Motion 的证据说明，motion 隐状态 或 pose retargeting 不能替代 force/contact 表示。EA-SENSOR 的主题卡判断也支持这一点：视觉负责全局语义和接触前规划，触觉/力负责接触后的局部闭环。

## 争议与条件

- Dense ECoT 和 语言—动作 pretraining 都试图增强语言监督，但前者保留视觉并增加 dense reasoning，后者刻意拿掉视觉以避免捷径；两者不是互斥，而是分别处理“语言太粗”和“视觉太强”。
- Action 表征单元izer 与 continuous action expert 不是简单优劣关系。表征单元izer 方便接入 LLM/VLM 的自回归范式，continuous expert 更贴近控制分布；关键取决于是否保留状态、接触和本体条件。
- Structured RGB interface 能缓解视觉对齐，但论文也报告失败来自感知噪声、单目深度不稳定和接触不足。因此它适合做 perception-control interface，不应被当作万能替代触觉/力控。
- 大数据混合只有在动作表示、坐标系、采样频率、质量和任务语义可比时才可能带来正迁移；否则扩数据会扩噪声。

## 对后续研究的启发

1. 数据采集应增加阶段级语言、关键动作片段、失败恢复、坐标系、控制频率、接触/力状态等元数据，减少“语言只在轨迹头部出现”的稀疏监督。
2. 模型结构上可考虑三层接口：语言/任务层负责 goal 与 subtask，结构化视觉层负责 object/geometry/affordance，动作层负责 continuous trajectory、controller adapter 和 safety constraint。

3. 评测不应只看 open-loop action prediction。需要闭环成功率、action-表征单元 解码误差、时序对齐误差、坐标系错误、模态 dropout、接触遮挡恢复、跨本体 transfer matrix。
4. 对工业或接触丰富任务，应把触觉/力控从“附加模态”提升为对齐对象：视觉看不见的接触状态必须有独立监督和闭环接口。

5. 未来 topic-card 可加入一条工作记忆：VLA 对齐难题主要来自信号粒度、物理动作空间和系统闭环接口不一致，而不是单纯缺少更大 VLM。

## 系统设计含义

把对齐问题视为接口问题后，模型可以分成三层。任务层把语言目标拆为阶段和约束；状态层从稠密视觉中提取对象、几何与可供性；控制层生成连续轨迹，并依据机器人本体、频率和接触状态完成适配。三层之间需要可测的中间变量，而不是只靠端到端损失隐式连接。

数据也应围绕接口补齐。语言不能只出现在轨迹开头，应标出阶段转换和失败原因；视觉应保存关键对象与空间参照；动作要携带坐标系、控制周期和执行状态；接触任务还要记录力与滑移。这样才能区分语义未落地、视觉未对齐和控制器未执行三种不同失败。

评测时可采用逐层替换：给定正确阶段标签测试状态接口，再给定真实状态测试动作生成，最后用正确动作测试控制器。若端到端失败而某一替换显著恢复性能，就能定位瓶颈。相比只比较最终成功率，这种干预更能指导架构与数据修改。

## References

近六个月正文级证据：LA4VLA ([2606.27295](https://arxiv.org/abs/2606.27295)); ZR-0 dense ECoT ([2606.30552](https://arxiv.org/abs/2606.30552)); Rethinking VLA Scaling ([2602.09722](https://arxiv.org/abs/2602.09722)); UR5 VLA deployment ([2606.30456](https://arxiv.org/abs/2606.30456)); SA-VLA ([2606.30113](https://arxiv.org/abs/2606.30113)); Sparse2Act ([2606.12759](https://arxiv.org/abs/2606.12759)); SSI-Policy ([2606.26800](https://arxiv.org/abs/2606.26800)); Transferring Contact, Not Just Motion ([2606.15516](https://arxiv.org/abs/2606.15516)); Learning Action Priors ([2606.26095](https://arxiv.org/abs/2606.26095)); SPACE ([2606.24049](https://arxiv.org/abs/2606.24049)).

背景基线：RT-1 (2212.06817); RT-2 (2307.15818); Open X-Embodiment / RT-X (2310.08864); Octo (2405.12213); OpenVLA (2406.09246); Diffusion Policy (2303.04137); `π0` (2410.24164).
