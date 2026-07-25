# 具身数据污染：从样本脏点到训练—评测—生成链的系统性失真

## 研究边界

本文考察 2025 年 7 月 15 日至 2026 年 7 月 15 日公开的具身智能论文，问题是：数据污染如何进入具身学习管道、怎样扭曲训练或评测，以及现有工作能提供哪些检测和治理手段。检索覆盖 964 篇候选论文，49 篇取得完整非 OCR 正文，最终有 15 篇通过逐篇阅读与论断支持审计。

这里的“污染”采用一个工作定义：任何进入训练、适配、生成或评测证据链，并使模型能力估计或行为机制发生非预期偏移的数据问题。它既包括恶意投毒，也包括训练—评测泄漏、重复样本造成的虚假规模、时间同步错误、低质量示范和任务覆盖坍缩。普通分布偏移、传感噪声或自然失败并不自动属于污染；只有当它们被固化进数据资产、切分或评价流程，才进入本文范围。

这个定义是本文对分散文献的综合，而非领域已有的统一术语。本次 15 篇精读样本中，9 篇集中于后门与恶意投毒，说明“显式污染”的安全研究已经形成明显支线；但对跨数据集近重复、基础模型预训练暴露和真实训练—测试交叉重合，近一年具身论文仍缺少同等成熟的量化审计。

## 中心判断

具身数据污染的本质不是“某些样本不干净”，而是**数据来源、时间结构、任务边界和模型供应链之间的对应关系被破坏**。具身模型输出连续动作，训练数据又常被切成 episode、chunk、frame，并经过基础模型、微调、世界模型扩增和闭环评测；污染因此可以藏在任何一层，并在后续环节才被激活。单看数据量、平均成功率或干净任务表现，都不足以证明数据与模型没有被污染。这个判断可以被证伪：如果未来研究表明，跨来源审计、时间一致性检查、结构化切分和触发压力测试均不能比普通随机抽检更早发现异常，那么本文提出的“关系失真”框架就需要修正。

## 一、评测污染首先表现为“模型见过了问题的结构”

具身评测的危险不只在于训练集和测试集出现完全相同的图像。更常见的情况是任务布局、物体关系、指令—动作映射或场景结构高度相似，使模型可以依赖记忆而非真正泛化。[LIBERO-PRO](https://arxiv.org/abs/2510.03827) 对标准 LIBERO 协议施加受控扰动后发现，固定布局和动作映射会让常规成功率高估模型的稳健泛化。这类问题即使没有字节级重复，也会形成“语义泄漏”。

训练语料内部的重复则制造另一种假象。[OSCAR](https://arxiv.org/abs/2606.04463) 指出，机器人和第一视角视频会在同一物理场景中反复记录高度相似任务，原始片段数增长，却几乎没有增加场景多样性。它采用先做视觉聚类、再用轨迹相似性核验的两阶段去重，恰好说明具身重复不能只靠单帧相似度判定：同一场景里动作轨迹不同的样本仍可能有价值。

两篇工作合在一起，给出一个重要区分：**训练语料去重解决的是有效覆盖，训练—评测隔离解决的是证据独立性**。前者做得好，不代表后者自然成立。实际治理应同时维护来源 episode、场景、操作者、任务、对象、时间和基础模型版本等谱系字段，并在视觉、语言、状态与轨迹四种表征上做交集审计。

## 二、连续控制让污染从“样本级”下沉到动作窗和时间轴

在图像分类里，错误标签通常对应单个样本；在 VLA 中，一个 episode 可能同时包含有效操作、停顿、误动作和恢复行为。粗粒度地保留或丢弃整条轨迹，会把这些差异抹平。[WARP-RM](https://arxiv.org/abs/2606.28320) 的出发点正是：次优长程示范中仍可能含有高价值恢复片段，因此质量控制需要下探到 frame 或 chunk 级进展信号。[SIEVE](https://arxiv.org/abs/2607.06442) 则按可复用动作原语的组合与转换接口分配选择预算，说明“看起来稳定的多数轨迹”未必覆盖任务真正需要的结构。

恶意研究把这一问题展示得更尖锐。[DropVLA](https://arxiv.org/abs/2510.10932) 表明，后门可以只在关键短时窗覆写夹爪等低层动作；episode 级总体分数仍可能掩盖动作级异常。[SilentDrift](https://arxiv.org/abs/2601.14323) 进一步利用 action chunking 与 delta-pose 积分，让每一步都平滑、微小的偏差在开环执行窗内累积成失败。因此，“轨迹平滑”“绝大多数帧正常”“整条任务偶尔成功”都不是充分的安全证据。

时间同步本身也是污染入口。[HapTile](https://arxiv.org/abs/2606.04825) 在数据管道中同步视觉、触觉、状态和动作，检查空轨迹、损坏轨迹、时间戳缺口及动作—状态一致性。它提示我们：多模态具身数据的质量单位不是独立传感器帧，而是同一控制时刻上可以因果对齐的观测—动作—结果关系。

由此得到的治理结论是：数据审计必须至少保留 episode、chunk、关键事件和控制 tick 四级视图。训练和评测报告也应补充接触前后、夹爪开合、恢复动作、动作窗末端等局部指标，而不是只报 episode 平均成功率。

## 三、污染会沿模型供应链潜伏，并在后续环节二次激活

近一年最强的证据来自后门研究。[`!Imperio, smolVLA`](https://arxiv.org/abs/2607.04146) 在真实拾放实验中，仅将 3 条投毒 episode 混入 320 条干净 episode，就能在触发词出现时造成完全拒绝服务；干净提示下的行为却可保持正常。[State Backdoor](https://arxiv.org/abs/2601.04266) 把触发从图像或文本移到真实示教的初始关节状态，显示仅依赖视觉预处理无法覆盖状态空间污染。[AttackVLA](https://arxiv.org/abs/2511.12149) 还展示了触发后执行攻击者指定长程动作序列的可能性，说明风险不止是“机器人失败”，还可能是“机器人按另一套目标成功”。

更麻烦的是，干净微调不等于清洗。[Inject Once, Survive Later](https://arxiv.org/abs/2602.00500) 将后门植入对下游微调不敏感的模块，使基模型污染能够穿过用户端的干净适配。换句话说，数据治理不能只检查企业自己新增的示范，还必须追踪基础模型权重、预训练数据声明、适配模块和检查点继承关系。

[Targeting World Models to Compromise Robot Learning Pipelines](https://arxiv.org/abs/2606.09499) 又增加了一层：表面安全的遥操视频可以先通过数据集级检查，却在世界模型生成合成轨迹时转化为危险行为，再污染下游政策。污染由此变成“二次激活”——原始样本、生成器输出和最终政策之间不能分开验收。凡是使用世界模型扩增、重标注或反事实生成的管道，都需要对生成前后分别建立可信 canary 集与行为差异审计。

## 四、检测、定位和恢复必须分账，数据选择也不能只做全局排序

现有防御开始从简单图像净化转向内部机制监控。[When Attention Betrays](https://arxiv.org/abs/2602.03153) 利用深层注意力和潜特征异常定位视觉后门，再重建视觉 token；但与场景语义自然融合的触发物仍是明显盲点。[TrustVLA](https://arxiv.org/abs/2607.12571) 强调用干净校准数据建立内部机制基线，并把检测、因果定位和恢复分开评价。二者都不能证明对状态触发、语义触发或自适应攻击普遍有效，因此防御结果必须明确触发类型和威胁模型。

非恶意数据治理也存在类似的“单指标失灵”。[ATHENA](https://arxiv.org/abs/2606.16208) 显示，多任务 VLA 数据若只做单一全局效用排序，某些任务可能被几乎淘汰，形成任务覆盖坍缩。由此可见，清洗不是越多越好：重复、损坏或有害样本应删除，但罕见任务、失败恢复和结构边界样本可能恰恰是长尾能力的来源。质量分、结构覆盖与任务最低配额需要共同约束。

## 可操作治理框架

| 环节 | 最小审计单位 | 主要风险 | 建议的证据 |
|---|---|---|---|
| 采集与入库 | 控制 tick、事件、episode | 时间错位、空/坏轨迹、动作—状态不一致 | 同步日志、哈希、设备与操作者谱系、因果一致性检查 |
| 合并与选择 | 场景、轨迹、任务、来源 | 近重复、虚假规模、任务覆盖坍缩 | 多模态相似簇、跨库交集、任务最低覆盖、保留/删除理由 |
| 训练与适配 | 基模型、模块、检查点 | 预训练暴露、持久后门、干净微调假安全 | 模型卡、权重继承、模块变化、可信 canary 与触发压力测试 |
| 生成与扩增 | 原始样本—生成轨迹对 | 世界模型二次激活、错误放大 | 生成前后差分、危险动作规则、人工复核抽样 |
| 闭环评测 | episode 与关键动作窗 | 记忆式高分、动作级异常被平均 | 结构扰动集、触发 ASR、干净成功率、局部动作与恢复指标 |

这个框架要求分开报告四类结果：干净任务成功率、触发或扰动条件下的攻击/失效率、检测的误报漏报、恢复后的能力损失。任何单项指标都不能独立支持“无污染”结论。

## 条件、分歧与研究空白

第一，后门论文通常采用明确攻击权限和特定触发器，部分实验仍以仿真或白盒设置为主；它们证明攻击面存在，不直接给出现实供应链中的发生率。第二，本次精读样本对恶意污染覆盖强，对无意的跨数据集重合、互联网视频预训练暴露和基础模型记忆覆盖弱。这是本次文献库与公开研究共同呈现的缺口，不能被表述为“领域不存在这些问题”。第三，去重和数据选择论文多以训练效率或平均性能为目标，尚未统一报告污染率、覆盖损失和评测独立性。

下一步最有价值的研究不是再提出一个总质量分，而是建立可复现的具身污染基准：公开数据谱系；构造精确重复、语义近重复、时间错位、低质片段、任务覆盖坍缩、状态/视觉/语言触发和世界模型二次激活等可控污染；同时报告清洁性能、污染条件性能、检出率、误报率、恢复代价和跨模型迁移。只有这样，“数据清洗”才能从经验工程变成可比较的科学问题。

## 结论

近一年的证据改变了一个常见直觉：具身数据污染不是入库前做一次清洗就能解决的静态问题。它贯穿采集、切分、合并、基础模型、微调、生成和闭环评测，并且常在动作窗、状态空间或下游生成阶段才显现。真正可靠的治理对象不是单个样本，而是样本与来源、时间、任务、模型版本及评测条件之间的关系。能追溯这些关系，并用结构扰动和触发测试验证它们，才接近“没有被污染”的可审计证据。

## References

1. [State Backdoor: Towards Stealthy Real-world Poisoning Attack on Vision-Language-Action Model in State Space](https://arxiv.org/abs/2601.04266)
2. [!Imperio, smolVLA: The Implications of Data Poisoning on Open Source Robotics](https://arxiv.org/abs/2607.04146)
3. [DropVLA: An Action-Level Backdoor Attack on Vision-Language-Action Models](https://arxiv.org/abs/2510.10932)
4. [SilentDrift: Exploiting Action Chunking for Stealthy Backdoor Attacks on Vision-Language-Action Models](https://arxiv.org/abs/2601.14323)
5. [When Attention Betrays: Erasing Backdoor Attacks in Robotic Policies by Reconstructing Visual Tokens](https://arxiv.org/abs/2602.03153)
6. [Targeting World Models to Compromise Robot Learning Pipelines](https://arxiv.org/abs/2606.09499)
7. [LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization](https://arxiv.org/abs/2510.03827)
8. [TrustVLA: Mechanism-Guided Inference-Time Defense Against Vision-Language-Action Backdoors](https://arxiv.org/abs/2607.12571)
9. [AttackVLA: Benchmarking Adversarial and Backdoor Attacks on Vision-Language-Action Models](https://arxiv.org/abs/2511.12149)
10. [Inject Once Survive Later: Backdooring Vision-Language-Action Models to Persist Through Downstream Fine-tuning](https://arxiv.org/abs/2602.00500)
11. [OSCAR: Omni-Embodiment Action-Conditioned World Model for Robotics](https://arxiv.org/abs/2606.04463)
12. [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825)
13. [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208)
14. [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320)
15. [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442)
