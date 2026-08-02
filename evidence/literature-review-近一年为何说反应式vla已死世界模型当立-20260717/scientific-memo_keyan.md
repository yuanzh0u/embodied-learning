# 反应式 VLA 已死？近一年论文中从“直接出动作”到“预演后行动”的范式转移

## 研究边界

本备忘录检视 2025 年 7 月 15 日至 2026 年 7 月 17 日公开的具身智能论文。候选池含 1,547 篇论文，175 篇获得可读全文；本次综合使用其中 28 篇完成全文精读和主张支持审计的论文。证据集中包含支持、限制、条件性结果和明示缺口，而非只选“世界模型有效”的正例。

这一范围能回答的是研究重心如何迁移，不能证明 VLA 会作为模型类别消失，也不能将预印本的局部结果外推为工业系统已经成熟。

## 中心判断

“VLA 已死”只在一个严格限定下成立：如果 VLA 指的是一个从当前图像和语言指令直接回归下一段动作、主要靠行为克隆训练、不显式检验动作后果的反应式策略，那么近一年的论文正在系统性地拆掉它的前提。它在跨本体动作语义、长时程归因、失败恢复、接触可观测性和真实闭环评测上都遇到结构性瓶颈。

但“世界模型当立”也不是用视频生成器替代策略模型。证据更支持一个融合架构：VLA 保留语义理解、任务分解和动作先验；动作条件世界模型负责预测后果、比较候选、识别失败和产生纠错信号；本体适配器与底层控制器负责把意图变成可执行运动。所谓范式转移，是从“动作预测就是全部”转向“策略、动态与控制分账而联合”。

## 一、VLA 的第一道死穴：动作 token 没有通用的物理语义

统一 token 形式容易制造一种错觉：只要不同机器人的动作都能编码，它们就可以直接混合学习。[SPACE](https://arxiv.org/abs/2606.24049) 指出，同一记录控制命令在不同控制器、机械本体、硬件个体和部署动态中可以产生不同运动。[SA-VLA](https://arxiv.org/abs/2606.30113) 则把问题收窄到离散动作 token 的解码端：一个固定 token 在不同机器人状态和接触情境下，未必对应同一连续控制量。

这不是编码器再大一点就会自动消失的问题。它要求模型把“语义上想做什么”、“世界会怎么变”和“这台机器人怎么动”分成不同接口。一项 UR5 真机实验也表明，离线 VLA 指标很好，仍可能因坐标系、模态时间对齐、图像预处理和动作语义不一致而无法稳定转成真实行为（[UR5 实验](https://arxiv.org/abs/2606.30456)）。

结论是：跨本体不应优先共享原始 command，而应优先共享任务阶段、空间状态变化、可达性和后果，再由本体适配器落地到具体控制器。

## 二、VLA 的第二道死穴：预测下一步，却不判断下一步会造成什么

反应式策略的根本缺口不是不会产生动作，而是它通常没有一个可查询的“假如执行这个动作，世界会变成什么”模块。在短时程、轨迹密集覆盖的模仿任务中，这个缺口可以被数据局部掩盖；在长任务、干扰和不可逆接触中，小偏差会沿动作块累积，而且策略不知道何时已经进入不可恢复状态。

近期 VLA 研究其实已在承认这一点。[ERVLA](https://arxiv.org/abs/2606.03784) 显示，有效的具身思维链必须落到末端执行器运动或图像空间轨迹等动作相关表示，把显式文本思维链当作自回归动作前缀反而会累积误差。[Fast-ThinkAct](https://arxiv.org/abs/2601.09708) 尝试把长程规划和失败自纠正压缩成隐变量推理；[ReCoVLA](https://arxiv.org/abs/2606.09630) 则将失败类型判断、恢复阶段和 reward 选择与底层 residual 纠错分开。这些工作不是在证明 VLA 没用，而是在把一个单一端到端函数拆回认知、动态与控制三层。

## 三、为什么世界模型正在成为新的中心层

世界模型的价值不在于多生成一段视频，而在于同时改变训练目标、规划接口和评测方式。

第一，它把监督从“专家当时做了什么”扩展到“动作使世界如何变化”。[$\tau_0$-WM](https://arxiv.org/abs/2606.01027) 将真实遥操、UMI 式交互、人类第一视角视频与 rollout/失败轨迹放入统一视频—动作模型，用模态监督掩码处理异构标注缺失。[GEM-4D](https://arxiv.org/abs/2605.22882) 通过几何特征蒸馏提升视频世界模型的操作相关性，而不增加推理时几何负担。[3PoinTr](https://arxiv.org/abs/2603.08485) 进一步说明，遮挡期间的物体点身份不应因暂时不可见而被整段丢掉。

第二，它使候选动作可以在执行前被比较。[World Pilot](https://arxiv.org/abs/2606.12403) 的核心动机正是：静态图文预训练无法为接触丰富操作提供充分信号，策略需要看到动作条件场景演化。[Interactive World Simulator](https://arxiv.org/abs/2603.08546) 表明，中等规模的机器人交互数据可以训练世界模型并生成策略训练示例，但前提是长时程交互一致性与 sim-real 排序相关性成立。

第三，它能把失败附近变成可学习的数据，而不是将失败 episode 整体丢弃。[Hi-WM](https://arxiv.org/abs/2604.21741) 强调失败高发状态周围的密集纠正轨迹；[TACO](https://arxiv.org/abs/2607.02840) 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于 VLA 后训练。[Dream-Tac](https://arxiv.org/abs/2606.08737) 把动作块、未来视觉和未来触觉放入同一目标，就是因为纯视觉未来无法完整观测接触成败。

## 四、基准高分为什么不能挽救旧范式

近一年最关键的变化之一，是“什么算做对了”正在被重写。[LIBERO-PRO](https://arxiv.org/abs/2510.03827) 指出，LIBERO 标准协议中的训练与测试任务过度接近，固定布局和指令—动作映射的记忆可被误认为泛化。[EgoVLA](https://arxiv.org/abs/2507.12440) 提供了另一个冷静例子：人类第一视角视频预训练不会直接消除本体差距；在缺少机器人微调时，其仿真 humanoid 任务成功率为 0%。这不否定人类视频预训练的价值，但否定了“视觉语义规模自动等于物理可执行性”。

世界模型也面临同样的评测重构。[MiraBench](https://arxiv.org/abs/2605.29360) 把缺口概括为动作条件可靠性：不只看视觉保真，还要看物理约束、动作跟随忠实度和失败乐观偏差。[WEAVER](https://arxiv.org/abs/2606.13672) 进一步要求结果保真、长时一致与足够高的规划效率同时成立。[SANTS](https://arxiv.org/abs/2605.27947) 则直接提醒：后期去噪即使让视频更好看，也可能更不动作相关或更不符合物理。

因此，世界模型不是凭“能生成”就取得系统权力。它必须证明自己能正确排序候选动作、对不可执行未来拒识、对失败不过度乐观，并且在真实闭环中产生稳定增益。

## 五、范式转移的可操作形态

| 系统层 | 应保留的能力 | 应新增的验收门槛 |
|---|---|---|
| 语义与任务层 | VLA/VLM 的指令理解、子任务分解、开放词汇 | 指令置换敏感性、阶段判断、失败类型准确率 |
| 动态与评估层 | 动作条件世界模型的未来预演、候选排序、失败检测 | action fidelity、physics adherence、failure optimism、sim-real 排序相关性 |
| 动作接口层 | 连续 action expert、本体 adapter、状态条件解码 | 不可达率、坐标系/频率一致性、接触负载、时延 |
| 真实执行层 | 底层控制、传感反馈、急停与恢复 | 闭环成功、滑移/掉落/过力、恢复率、接管次数、连续运行时间 |

对数据工程的直接含义是，从只收成功示教转向收集干预、失败附近、恢复、接触、力/触觉和几何对应。[SKIP](https://arxiv.org/abs/2606.00664) 说明 approach、contact、grasp、release 等稀疏关键事件不能被普通抽帧删除；[TacForeSight](https://arxiv.org/abs/2606.11184) 表明，如果目标包含扰动恢复，数据就必须显式包含正常示教和 recovery interaction，不能指望模型从成功轨迹自行猜出如何重建接触。

## 条件、分歧与可证伪性

第一，世界模型还未取得普遍的规划可采信性。[Pri4R](https://arxiv.org/abs/2603.01549) 仍将 4D point-track 监督能否扩大到更大预训练、是否需要在推理时显式引入几何观测留作未解问题。可变形物、强遮挡、精细摩擦与长时接触仍是高风险区。

第二，本文不主张删除 VLA。如果未来一个没有预测性训练目标、没有外部动态评估器的纯反应式 VLA，能在未见环境、跨本体、长时程和接触干扰任务上，以相同计算与真机数据预算，在动作忠实度、失败恢复和真实闭环成功率上稳定追平或超过融合系统，那么“反应式 VLA 已进入死胡同”的判断就被证伪。

## 结论

近一年论文没有宣告 VLA 寿终正寝。它们做的事更具体：拒绝把视觉语义、连续物理、本体控制和失败恢复压成一个无差别的 next-action 函数。“世界模型当立”的实质，是为机器人引入能被验证的后果预演层，让系统在行动前可以比较，在失败时可以归因，在接触中可以利用非视觉信号。最可能胜出的不是“世界模型 vs. VLA”，而是“带世界模型的 VLA 系统 vs. 只会反应的 VLA”。

## References

- [EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos](https://arxiv.org/abs/2507.12440)
- [LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization](https://arxiv.org/abs/2510.03827)
- [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](https://arxiv.org/abs/2601.09708)
- [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549)
- [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485)
- [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546)
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](https://arxiv.org/abs/2604.21741)
- [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882)
- [SANTS: A State-Adaptive Scheduler for World Action Models](https://arxiv.org/abs/2605.27947)
- [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360)
- [$\tau_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027)
- [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664)
- [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](https://arxiv.org/abs/2606.03784)
- [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737)
- [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630)
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184)
- [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403)
- [WEAVER, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672)
- [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049)
- [SA-VLA: State-aware Tokenizer for Improving Vision-Language-Action Models' Performance](https://arxiv.org/abs/2606.30113)
- [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456)
- [TACO: TActile World Model as a Self-COrrector for Scalable VLA Post-Training](https://arxiv.org/abs/2607.02840)
