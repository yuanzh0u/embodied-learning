# 数据时空一致性正在从“同步指标”变成具身智能的系统契约

## 研究边界

本文考察 2025 年 7 月 27 日至 2026 年 7 月 27 日的具身智能论文，问题不是“哪些方法显式使用了 spatiotemporal consistency 这个词”，而是：论文在什么位置讨论数据的时间、空间、动作与物理后果必须彼此一致。检索池包含 1,401 篇候选论文，52 篇具有完整可读的非 OCR 全文；本文从中接纳 20 篇完成全文阅读与论据核验的论文，覆盖数据采集、多模态感知、4D 世界模型、第一视角迁移和 VLA 部署。

这一范围可以支持机制归纳，但不能给出跨任务统一的同步误差、帧率或标定精度阈值。多数论文报告的是特定机器人、传感器和任务下的实现与消融；例如 10 Hz、6 FPS 或快慢流频率比都是系统实例，不是行业标准。

## 中心判断

近一年的变化不是出现了一个新的“时空一致性分数”，而是研究共同把一致性从采集端的一次性检查，推进为贯穿数据、模型与闭环执行的五层契约：共同物理时间、共同空间参考、跨视角/跨模态对应、动作—状态因果匹配，以及长序列中的对象身份与接触连续性。时间戳相同只能证明记录层对齐；只有当同一动作在同一坐标语义下对应同一段物理状态变化，并在预测和真实执行中保持同步，数据才对策略学习真正一致。

这是本文的跨论文推断。它会被以下结果证伪：只做时间戳与外参对齐、无需动作语义、接触事件和长程后果检核的数据，在跨本体与真实闭环中仍能稳定达到同等性能。现有证据恰好指向相反方向：异构数据若不同时处理空间、形态、物理时间和标签可靠性，会损害动作学习；离线指标也可能在数据—模型—控制接口不一致时无法转化为稳定真机行为。[ACE-Ego-0](https://arxiv.org/abs/2606.17200) 与一项 [UR5 实机研究](https://arxiv.org/abs/2606.30456) 分别从预训练消融和部署观察给出了这一边界。

## 一、时间一致性：统一的不是帧号，而是物理事件

最底层的要求仍然是硬件同步。HapTile 在机器人控制环内同步视觉、触觉、语言、状态和动作，并检查时间戳缺口、损坏轨迹与动作—状态一致性；[Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) 则先用时间戳对齐腕部位姿、关节、外部视觉和双指触觉视频，再降采样训练。这些工作说明，模型输入频率可以降，但原始物理时间与对齐过程不能丢。[HapTile](https://arxiv.org/abs/2606.04825) 的价值也不只是“多一种触觉数据”，而是把多个模态放回同一控制事件中。

更重要的变化是多速率建模。视觉和语言承担较慢的场景理解与任务约束，触觉在接触后进入更快的纠偏回路；[AT-VLA](https://arxiv.org/abs/2605.07308) 因此把慢速视觉—语言流和快速触觉流分开。[H-WM](https://arxiv.org/abs/2602.11291) 也用低频逻辑状态维持长任务顺序，用视觉子目标连接感知，再让高频 VLA 执行动作块。这里的“一致”不再等于所有通道采相同 FPS，而是不同频率的信号能被映射到同一段物理过程：接近、接触、滑移、释放和恢复。

因此，按固定帧数切 action chunk 是危险的。不同来源即使都提供 16 帧，实际覆盖的物理时长、控制延迟和接触阶段也可能不同。[Embodied Image Compression](https://arxiv.org/abs/2512.11612) 的 10 Hz 多视角管线只是一个 UR5 实例；合理的数据契约应保存实际采样时刻、时钟源、丢帧与抖动，再按物理时长或事件边界生成训练窗口。

## 二、空间一致性：共同坐标比更多视角更优先

空间一致性首先是参考系问题。第一视角视频中的相机与手腕同时运动；[ActiveMimic](https://arxiv.org/abs/2606.06194) 明确指出，直接把腕部轨迹当动作监督，会把相机平移和旋转混入手部运动。类似问题也出现在跨本体预训练：同一个数值向量可能分别表示相机坐标下位移、末端绝对位姿或关节命令。没有坐标图、单位、动作语义和形态条件，“数值接近”并不代表物理动作一致。

第二层是跨视角几何对应。[MVISTA-4D](https://arxiv.org/abs/2602.09878) 从单视角 RGBD 生成几何一致的任意视角，再把它们反投影、融合成随时间变化的 3D 结构；[Embody4D](https://arxiv.org/abs/2605.01799) 则把固定或稀疏机位导致的局部观测，转化为新视角视频与 3D 感知的数据扩增问题。这两条路线扩展了观测面，但也隐含一个质量闸门：新视角必须保持对象身份、相机几何和时间连续，不能仅靠单帧视觉逼真验收。

第三层是可见性与标定不确定性。[3PoinTr](https://arxiv.org/abs/2603.08485) 不因关键点短暂遮挡就删除整条轨迹，而是只屏蔽不可见的点—时刻损失，从而保留跨帧对象运动监督。[RGB-S](https://arxiv.org/abs/2606.08765) 将触觉接触投影到图像域时，还用空间分布显式表达运动学和标定误差。它们共同说明：空间对齐不应伪装成无误差真值，而要同时记录对应关系、可见性和残差。

## 三、跨模态一致性：同一时刻不等于同一物理含义

接触任务最能暴露“同时间戳帧”的不足。相机可能仍看到夹爪覆盖物体，却无法判断摩擦、滑移和局部形变；触觉或力信号虽然时间上对齐，也可能因安装位置和表示空间不同而无法直接融合。[ContactWorld](https://arxiv.org/abs/2606.13877) 的比较显示，稳定长程规划依赖空间结构、时间连续性和跨模态兼容性同时成立；在其 12 个接触任务上，点云与触觉力场的组合优于单纯腕部或前视图，但论文没有把“增加模态”本身当作充分条件。

[Dream-Tac](https://arxiv.org/abs/2606.08737) 把动作块、未来视觉和未来触觉置于同一预测目标中，实际上把跨模态对齐改写为“动作之后，各模态应如何共同变化”。[HT-Bench](https://arxiv.org/abs/2606.19161) 则把规模推进到约 1,000 万 RGB 帧、780 万触觉帧和 226 项任务，并评估接触结构、跨模态对应和时间动态。大规模配对数据使表征研究成为可能，但仍不能自动外推为真实机器人闭环收益。

多模态带宽也应服从动作效用。[SPARC](https://arxiv.org/abs/2606.16253) 指出，多机位数据不应把码率均匀分给每个视图和区域，而应保留对当前动作有用的内容。[Event-VLA](https://arxiv.org/abs/2606.29384) 以事件流补充光照变化下退化的 RGB，进一步说明模态价值来自它是否补足特定不可观测状态，而非传感器数量。

## 四、因果一致性：动作必须与状态变化成对

真正决定数据能否训练控制策略的，是动作与后果是否匹配。[Kinema4D](https://arxiv.org/abs/2603.16669) 把机器人控制表示为运动学正确的 4D 轨迹，再让生成模型预测环境响应；这比仅以低维动作向量条件化视频更明确地绑定了“机器人如何运动”和“世界如何变化”。HapTile 的动作—状态检核、Dream-Tac 的动作—视觉—触觉联合预测，都是同一方向：数据单元应是一次干预及其后果，而非彼此松散的帧和标签。

这一层也给出了最强反例。[BadWAM](https://arxiv.org/abs/2607.15207) 表明，世界—动作模型可以“想象得合理却执行得错误”；安全属性不应只检查生成未来是否逼真，而要验证想象未来与实际将执行动作是否同步。这使“动作—想象一致性”成为世界模型数据和评测的新要求。若预测视频与真实动作解绑，再好的时空画面也不能作为可靠控制证据。

## 五、长程一致性：要保持身份、接触和任务进度

长序列误差并不只来自画面漂移。对象身份交换、遮挡后重现错误、接触关系中断、动作延迟累积和任务阶段错位，都会让局部合理的预测在几秒后失去物理意义。[WEAVER](https://arxiv.org/abs/2606.13672) 将有效机器人世界模型概括为结果保真、长程时间一致和计算效率三者同时满足；缺少其中任何一项，都难以用于策略评估、改进或规划。

这也解释了为什么 H-WM 的多时间尺度结构有意义：低频逻辑维持全局任务顺序，高频控制吸收局部变化。但该路线仍有边界。稀疏子目标可能漏掉接触瞬态，长程一致的视觉计划也可能与真实执行动作不同步。因而部署验收必须同时检查任务进度、对象/接触连续性和动作忠实，而不能只看终帧或视频质量。

## 可操作的数据契约

| 层级 | 入库必须保留 | 建议检核 |
|---|---|---|
| 物理时间 | 原始时间戳、时钟源、采样率、丢帧/抖动、控制延迟 | 跨模态时间残差、事件顺序、物理窗口长度 |
| 空间参考 | 坐标图、单位、内外参、标定版本、机位/硬件 ID | 重投影残差、参考系闭环、遮挡与可见性 |
| 模态对应 | 视觉、深度、触觉、力、本体状态的字段白名单与缺失标记 | 对应完整率、模态污染消融、跨实例退化 |
| 动作因果 | 动作语义、控制频率、执行延迟、动作前后状态、接触事件 | 动作—状态残差、接触因果顺序、不可达率 |
| 长程动态 | 对象/点轨迹、阶段、失败、接管、恢复、奖励或进度 | 身份保持、长程漂移、动作—想象同步、闭环成功率 |

这张表的含义不是强迫所有数据源提供全部字段。人类视频、机器人示教、触觉序列和合成 4D 数据可以各自缺字段，但缺失必须显式标注，训练时按可靠监督字段使用。异构可以扩大内容覆盖，一致性则应集中在数据契约和目标机器人锚点上。

## 条件、分歧与研究空白

第一，目前没有证据支持统一帧率、码率或同步误差阈值。任务时域、控制频率、传感器延迟和接触速度不同，阈值必须通过目标策略的闭环曲线标定。

第二，生成式新视角和 4D 伪标注能扩大数据覆盖，但仍缺少跨方法统一的几何—动作—接触联合验收。视觉一致不能替代物理一致，表征分数也不能替代闭环控制。

第三，多速率系统缺少统一的端到端延迟预算。慢速语义、视觉子目标、动作块和快速触觉纠偏如何在同一时间轴上对账，仍是工程与研究共同空白。

第四，硬件长期漂移、换件和重标定尚未被多数数据集作为核心变量。空间一致性若只在采集首日成立，就不能支撑长期部署。

## 结论

近一年论文给出的最重要变化，是把数据时空一致性从“传感器同步是否成功”推进到“数据能否忠实描述一次物理干预及其后果”。可靠的数据不必同构，也不必同频；但它必须回答五个问题：何时发生、在什么坐标中发生、哪些观测对应同一状态、哪个动作导致了什么变化，以及这种关系能否跨遮挡、接触和长任务保持。对具身数据工程而言，下一步不应再寻找一个全局一致性分数，而应建立可分层审计、可在真实闭环中证伪的数据契约。

## References

- [ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining](https://arxiv.org/abs/2606.17200)
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825)
- [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001)
- [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](https://arxiv.org/abs/2605.07308)
- [ActiveMimic: Egocentric Video Pretraining with Active Perception](https://arxiv.org/abs/2606.06194)
- [MVISTA-4D: View-Consistent 4D World Model with Test-Time Action Inference for Robotic Manipulation](https://arxiv.org/abs/2602.09878)
- [Embody4D: A Generalist Data Engine for Embodied 4D World Modeling](https://arxiv.org/abs/2605.01799)
- [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485)
- [RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation](https://arxiv.org/abs/2606.08765)
- [ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13877)
- [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737)
- [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669)
- [H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model](https://arxiv.org/abs/2602.11291)
- [WEAVER, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672)
- [BadWAM: When World-Action Models Dream Right but Act Wrong](https://arxiv.org/abs/2607.15207)
- [SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models](https://arxiv.org/abs/2606.16253)
- [HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision](https://arxiv.org/abs/2606.19161)
- [Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model](https://arxiv.org/abs/2606.29384)
- [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456)
