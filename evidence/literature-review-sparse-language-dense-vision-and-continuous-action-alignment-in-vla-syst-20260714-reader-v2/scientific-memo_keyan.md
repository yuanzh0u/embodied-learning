# 语言稀疏性、动作连续性与稠密视觉造成的多模态对齐难题研究备忘录

## 摘要

本文综述一个正在 VLA / 机器人基础模型中变得清晰的问题：语言、视觉和动作并不是三种可直接拼接的 token 流。语言通常以任务级或阶段级指令出现，语义稀疏、时间标注粗；图像/视频是高维稠密信号，容易主导训练；动作是连续、闭环、受本体和控制器约束的物理量。近六个月的论文显示，失败常不是某个 backbone 不够大，而是语言-动作、视觉-动作、动作-控制器三条接口没有被显式对齐。

## 研究边界

版本说明：本轮以 15 篇可获取完整正文的论文为论证主干，逐篇核对问题、方法、结果与限制；未能取得可读全文的论文不再承担正文结论。

- 检索时间：2026 年 1 月 14 日至 7 月 14 日；经典论文只作背景基线，不被包装成最新发现。
- 覆盖规模：924 条去重候选、131 篇可用全文、24 篇直接相关论文；检索覆盖语言—动作、视觉—动作、动作接口、跨本体迁移与接触边界。
- 停止条件：候选量、全文量、关键维度和连续两轮低新增率均已满足；核心引用保持克制，不等于只检索了文中出现的十余篇论文。
- 限制：本综述聚焦机器人/VLA，不覆盖一般多模态大模型的全量图文对齐文献；2026 年论文多为预印本，结论应按“当前证据”而非领域共识处理。

## 背景脉络

RT-1 把大规模真实机器人数据、语言指令和视觉观测接到 Transformer 控制策略上，提出机器人也可能走 scaling 路线。RT-2 进一步把 VLM/VQA 风格的互联网语义知识迁移到机器人动作输出。Open X-Embodiment / RT-X、Octo、OpenVLA 则把跨机器人数据、通用策略和开源 VLA 推向主流。

与此同时，Diffusion Policy 和 `π0` 代表了另一条线：用扩散或 flow matching 处理连续、高维、可多峰的动作分布。

这条历史脉络解释了为什么 2026 年的新论文开始集中处理“接口”问题：VLM 提供语义和视觉先验，但机器人动作不是语言 token，也不是图像 patch；动作要通过本体、控制器、状态估计和接触反馈落到物理世界。

## 中心判断

### 语言稀疏

这带来一个重要推论：如果语言只在输入端作为 prompt 出现，而没有阶段级、动作级或因果级监督，它很容易成为装饰性条件。ZR-0 的 dense embodied chain-of-thought 方向可以理解为把稀疏语言“加密”：把场景描述、任务进度、未来计划、原子子任务、目标框和离散动作 token 作为 dense supervision，使高层认知过程更细粒度地对齐到动作专家（[Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](https://arxiv.org/abs/2606.30552)）。

### 动作连续

动作不是自然语言词表。离散 action token 对 autoregressive VLA 很友好，但会带来压缩和解码问题：同一个 token 在不同关节状态、物体位姿、接触条件下不应解码成同一个连续控制量。SA-VLA 因此把机器人状态注入 action tokenizer，试图缩小离散 token 到连续控制之间的 compression 空白（[SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113)）。

另一类论文绕开“先离散再还原”的瓶颈，用 flow matching / diffusion 直接学习连续动作流。Learning Action Priors for Cross-embodiment Robot Manipulation 的关键判断是：VLA 从 VLM 继承了视觉和语言先验，但 action module 往往从零学习物理运动；

### 视觉稠密

SSI-Policy 则构造 RGB-only structured scene interface，把 monocular depth、language-grounded object layout 和 instruction-conditioned 2D motion trajectory 放到中间层，再交给 diffusion action planner；这等于在视觉和控制之间加了一个可解释、任务对齐的空间接口（[SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation](https://arxiv.org/abs/2606.26800)）。

### 物理闭环

真实机器人中的 action 不是抽象标签，而是控制器输入。SPACE 指出，不同机器人甚至同一型号不同硬件单元中，同一 action command 都可能产生不同 motion；因此它用 Cartesian state delta 做共享动作表示，再用 Action Adapter 转成具体机器人控制命令（[SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049)）。

## 核心机制

### 1. 对齐难题本质上是粒度错配

语言粒度粗，视觉粒度细，动作粒度连续。把它们统一成 token 后，表面上进入同一个模型，实际上仍有三个未解决的 mapping：语言目标如何落到动作阶段，视觉几何如何落到可执行位姿，连续控制如何适配本体和控制器。

当前论文的共同趋势是为每个 mapping 引入更强的中间约束，例如 dense ECoT、语言—动作 pretraining、state-aware action tokenizer、action prior、structured scene interface、Cartesian state delta。

### 2. 视觉不是越稠密越好，关键是稠密信号是否被动作约束

图像 patch、视频帧和多视角输入可以提供大量信息，但也会制造捷径。Sparse2Act 和 SSI-Policy 的价值在于把视觉压缩成 action-aligned geometry 或 task-aligned scene interface，而不是让视觉 token 自己决定什么重要。换句话说，机器人视觉表征的目标不只是识别对象，而是把对象、空间关系和动作可达性放到同一坐标系里。

### 3. 动作空间是 VLA 与普通 VLM 的最大分水岭

普通 VLM 可以用文本 token 作为输出；VLA 的输出必须被控制器执行。动作可以被离散化，但离散 token 最后仍要还原到连续控制；动作可以直接用 flow/diffusion 生成，但还要匹配本体、频率、延迟、坐标系和安全约束。SA-VLA、Action Prior、SPACE、Rethinking VLA Scaling 都在从不同角度回答同一个问题：动作表征应该以物理状态变化和控制可执行性为中心，而不是以模型输出便利性为中心。

### 4. 跨本体 scaling 的瓶颈不是数据量，而是数据兼容性

Open X-Embodiment/RT-X 让“跨机器人大数据”成为可能，但 2026 年的证据明显更谨慎。Rethinking VLA Scaling 指出，机器人数据在本体、传感器、频率和动作空间上异构，朴素混合可能负迁移；SPACE 进一步说明 action command 本身不是通用标签。由此可推断：未来的数据 scaling 需要 metadata、action adapter、坐标系统一、质量审计和任务族分层，而不是简单合并轨迹。

### 5. 接触状态是视觉-语言-动作三元组的盲区

对于开放空间抓放，RGB + language + action 可能足够；但对滑移、柔顺贴合、灵巧抓握、插入和易碎物，关键状态常在视觉遮挡后发生。Transferring Contact, Not Just Motion 的证据说明，motion 潜在状态 或 pose retargeting 不能替代 force/contact 表示。EA-SENSOR 的主题卡判断也支持这一点：视觉负责全局语义和接触前规划，触觉/力负责接触后的局部闭环。

## 争议与条件

- Dense ECoT 和 语言—动作 pretraining 都试图增强语言监督，但前者保留视觉并增加 dense reasoning，后者刻意拿掉视觉以避免捷径；两者不是互斥，而是分别处理“语言太粗”和“视觉太强”。
- Action tokenizer 与 continuous action expert 不是简单优劣关系。tokenizer 方便接入 LLM/VLM 的自回归范式，continuous expert 更贴近控制分布；关键取决于是否保留状态、接触和本体条件。
- Structured RGB interface 能缓解视觉对齐，但论文也报告失败来自感知噪声、单目深度不稳定和接触不足。因此它适合做 perception-control interface，不应被当作万能替代触觉/力控。
- 大数据混合只有在动作表示、坐标系、采样频率、质量和任务语义可比时才可能带来正迁移；否则扩数据会扩噪声。

## 对后续研究的启发

1. 数据采集应增加阶段级语言、关键动作片段、失败恢复、坐标系、控制频率、接触/力状态等元数据，减少“语言只在轨迹头部出现”的稀疏监督。
2. 模型结构上可考虑三层接口：语言/任务层负责 goal 与 subtask，结构化视觉层负责 object/geometry/affordance，动作层负责 continuous trajectory、controller adapter 和 safety constraint。

3. 评测不应只看 open-loop action prediction。需要闭环成功率、action-token 解码误差、时序对齐误差、坐标系错误、模态 dropout、接触遮挡恢复、跨本体 transfer matrix。
4. 对工业或接触丰富任务，应把触觉/力控从“附加模态”提升为对齐对象：视觉看不见的接触状态必须有独立监督和闭环接口。

5. 未来 topic-card 可加入一条工作记忆：VLA 对齐难题主要来自信号粒度、物理动作空间和系统闭环接口不一致，而不是单纯缺少更大 VLM。

## 系统设计含义

把对齐问题视为接口问题后，模型可以分成三层。任务层把语言目标拆为阶段和约束；状态层从稠密视觉中提取对象、几何与可供性；控制层生成连续轨迹，并依据机器人本体、频率和接触状态完成适配。三层之间需要可测的中间变量，而不是只靠端到端损失隐式连接。

这套分层的价值还在于允许逐层证伪。若给定正确阶段标签后动作仍错，问题不在语言稀疏；若给定真实三维状态后恢复，说明视觉接口是瓶颈；若给定正确轨迹仍执行失败，则应检查控制器、坐标系和频率。把这些干预写进实验设计，才能避免把所有增益都归功于更大的主干模型。

数据也应围绕接口补齐。语言不能只出现在轨迹开头，应标出阶段转换和失败原因；视觉应保存关键对象与空间参照；动作要携带坐标系、控制周期和执行状态；接触任务还要记录力与滑移。这样才能区分语义未落地、视觉未对齐和控制器未执行三种不同失败。

评测时可采用逐层替换：给定正确阶段标签测试状态接口，再给定真实状态测试动作生成，最后用正确动作测试控制器。若端到端失败而某一替换显著恢复性能，就能定位瓶颈。相比只比较最终成功率，这种干预更能指导架构与数据修改。

## 精读复核后的对齐框架

移出无法获得完整正文的论文后，论证仍然指向四个可分开验证的接口。第一，语言需要被翻译为动作相关中间量：[稠密具身 CoT](https://arxiv.org/abs/2606.30552) 和 [ERVLA](https://arxiv.org/abs/2606.03784) 都把高层语义与末端运动、图像空间轨迹等表示相连，后者还显示把长 CoT 当动作前缀会累积推理误差。

第二，连续动作不能被当成与状态无关的离散单词。[SA-VLA](https://arxiv.org/abs/2606.30113) 把问题定位为固定 action token 回解码到连续控制时的状态依赖；[SPACE](https://arxiv.org/abs/2606.24049) 则表明同一记录命令在不同本体上未必对应同一物理运动。因此，动作对齐必须包含坐标系、本体和时序语义。

第三，稠密视觉应被压缩为结构化、动作可查询的接口。[SSI-Policy](https://arxiv.org/abs/2606.26800) 将 RGB 的几何和任务 grounding 与运动轨迹分层，减轻了视觉 token 直接淹没控制信号的风险。第四，接触不能继续停留在 RGB 之外：[TACO](https://arxiv.org/abs/2607.02840) 把未来视频和力序列联合预测，再用失败附近状态生成纠正动作。这些结果共同将“多模态对齐”改写为四个不同频、不同粒度的接口设计问题。

## References
- [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](https://arxiv.org/abs/2606.30552)
- [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113)
- [SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation](https://arxiv.org/abs/2606.26800)
- [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049)
- [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](https://arxiv.org/abs/2606.03784)
- [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840)
