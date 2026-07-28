# LeWorldModel 技术谱系：从“潜空间可预测”到“闭环可规划”

## 研究边界

本文聚焦 LeWorldModel（LeWM）及其最直接的技术前序、后续修补和反例，而不把所有带有 world model 名称的工作混在一起。检索窗口为 2026 年 1 月 24 日至 7 月 24 日，并为理解技术来源纳入窗口外的 [V-JEPA 2](https://arxiv.org/abs/2506.09985) 与 [LeJEPA](https://arxiv.org/abs/2511.08544)。本轮共获得 193 篇去重候选、38 篇可读完整正文，最终以 24 篇逐篇精读论文支撑判断。

分析对象不是单一预测指标，而是从像素输入到真实动作之间的整条链：表征能否稳定联合训练，潜动态是否对动作敏感，多步滚动是否覆盖规划时域，潜空间代价是否对应真实可达性，规划与控制又能否在计算预算内改善任务结果。DINOv3 一类静态视觉基础表征只作为“冻结通用编码器”的对照边界；MoE、统一模型和一般 VLA 路线不承担本文核心论证。

## 中心判断

LeWM 的贡献不是简单地把世界模型做小，而是证明了一条极简链路可以工作：从像素联合训练编码器和动作条件预测器，用一个预测损失加一个防坍塌正则学习潜状态，再在该潜空间中以 CEM/MPC 搜索短动作序列。这使“自监督视觉表征—潜动态—规划控制”第一次以很少的训练部件连成一个可复现基线。

但 2026 年紧随其后的研究也给出更重要的结论：**稳定、可预测、动作敏感、可达、可搜索和闭环有效是六个不同命题。** LeWM 主要把前两三项接了起来，后续工作则逐层暴露并修补剩余接口。因此，评价这条路线不能只问 latent prediction loss 是否下降，也不能只看生成结果是否自然；必须检查每一层是否满足下一层所需的契约。

## 最短技术链：LeJEPA 的正则如何进入 LeWM

[LeJEPA](https://arxiv.org/abs/2511.08544) 的出发点是简化联合嵌入预测学习。它把多视图预测与 SIGReg 结合，移除 prototypes、teacher–student、EMA 和 stop-gradient 等常用防坍塌装置。SIGReg 将批量表征投影到多个随机一维方向，再用 Epps–Pulley 统计量把投影分布推向标准高斯；当投影方向足够多时，这相当于约束联合分布接近各向同性高斯。其价值首先是训练稳定和分布塑形，而不是控制本身。LeJEPA 的主要实验没有动作条件动力学、模型滚动或闭环规划，因此它只能解释 LeWM 的正则来源，不能替 LeWM 提供控制证据。

[LeWorldModel](https://arxiv.org/abs/2603.19312) 将这套思想放进离线动作轨迹。设像素观测经编码器得到 \(z_t=f_\theta(o_t)\)，动作条件预测器根据历史潜状态和动作给出下一状态 \(\hat z_{t+1}=g_\phi(z_{\le t},a_t)\)。训练目标可概括为

\[
\mathcal{L}=\mathcal{L}_{pred}+\lambda\mathcal{L}_{SIGReg}.
\]

动作通过 AdaLN 注入预测器每一层，预测器自回归推出候选动作序列下的未来潜状态。控制时，CEM 采样并迭代更新动作序列，最小化终端预测潜状态与目标图像潜状态的距离；系统只执行其中一段动作，获得新观测后重新规划。这种 receding-horizon 设计很关键：论文没有声称可以无限滚动，而是明确承认更长 rollout 同时增加计算和模型偏差。

在论文的模拟协议中，LeWM 在 Push-T 上比 PLDM 高 18 个百分点，固定规划配置完成一次完整规划少于一秒；三训练种子的对照也显示 PLDM 的成功率方差更大。不过，LeWM 并非在所有环境领先。简单的 Two-Room 反而表现较差，作者推测低数据多样性、低内在状态维度与高维各向同性先验存在冲突。这说明 SIGReg 是一种带数据条件的正则，不是“潜空间越高斯越适合所有控制任务”的普遍定律。

## 速度分支：Fast-LeWM 并行的是动力学查询，不是整个规划器

[Fast-LeWorldModel](https://arxiv.org/abs/2606.26217) 针对 LeWM 规划时必须顺序调用一步 predictor 的瓶颈，引入因果 action-prefix encoder：把同一个已观测状态作为锚点，一次处理多个动作前缀，并行预测不同未来时域的潜状态；训练时对每个前缀提供稠密目标。视觉编码器与 SIGReg 仍被保留，因此它主要改写的是动力学查询方式，而不是换掉表征目标、终端潜距离或 CEM。

在该论文的同协议四任务汇总中，平均成功率由 LeWM 的 85.8% 提升到 Fast-LeWM 的 90.5%，再加 self-conditioning 后为 92.0%，但主表没有跨种子误差条。Two-Room、同一 CEM 预算和单张 RTX 4090 的计时显示，动力学部分由 31.4 秒降到 8.0 秒，完整 CEM 则由 54.4 秒降到 28.3 秒。这个分账说明加速确实来自把五次顺序动力学调用合为一次 prefix pass，同时也说明模型前向之外的采样、精英筛选和分布更新仍占大量时间；28.3 秒的绝对延迟也不能称为实时控制。这里的协议与 LeWM 原论文“少于一秒”的配置不同，数字不能横向直接相减。超过单个最大 prefix window 的更长时间点仍要组合两次预测，而 naive 的长动作输入若缺少稠密前缀监督和 state token，并不能保持同样质量。

## 第一份独立契约：预测必须对动作敏感

动作作为网络输入，并不保证网络真正使用动作。若相邻帧变化平滑，模型可能主要靠当前状态预测下一状态，同时把不同动作造成的差异压在很小的潜位移里。这样的模型可以有较低预测误差，却会让 CEM 难以区分候选动作。

[Delta-JEPA](https://arxiv.org/abs/2606.31232) 对此给出直接修补：除预测未来潜状态外，再要求仅从潜状态差分 \(z_{t+1}-z_t\) 恢复已执行动作。这个 latent-difference action decoding 迫使局部转移几何携带动作信息。固定训练和规划协议后，它在四个模拟环境都优于从两个端点拼接后解码动作的版本；可视化也显示，当起始历史不变而只改变动作时，Delta-JEPA 的预测响应按动作分开，LeWM 的响应则更集中、更重叠。

然而动作敏感仍不是任务充分性。[Predictive Objectives Discard Exogenous Control-Relevant Features](https://arxiv.org/abs/2606.30068) 构造了一个受控反例：若某个与奖励相关的状态特征在时间上不可预测，纯粹的无奖励潜预测目标没有理由保留它。增加潜容量不能自动补回这个信号；逆动力学只有在行为策略的动作与该特征相关时才可能间接保留它。这个结果来自小型合成环境，不能直接宣布大型机器人模型也会失败，但它明确否定了一个常见推理——“把所有可预测因素建模好，就等于保留了控制所需的一切”。

## 第二份独立契约：潜距离必须对应有限预算内的可达性

LeWM 的默认规划接口把终端潜状态到目标潜状态的欧氏距离当作代价。这个选择计算简单，却暗含很强的几何假设：潜空间中的近邻，必须在动力学约束和剩余步数下也容易到达。

[Beyond Euclidean Proximity](https://arxiv.org/abs/2605.22164) 用 Two-Room 给出醒目的反例。只替换终端 selector、保持世界模型不变，full-horizon trajectory reachability metric 就把 LeWM 的平均成功率从 7.0% 提升到 97.0%。更有解释力的是，和二维位置相关的一个低维 rowspace 只贡献了终端—目标潜均方误差的 0.5%–0.7%，却能让规划成功率达到 90.8%；剩余的大部分潜误差几乎不帮助穿过门洞。这表明“潜空间中占能量最多的方向”与“规划中最重要的方向”可能完全不同。

[RC-aux](https://arxiv.org/abs/2605.07278) 进一步把时间和方向纳入接口。它一方面训练多时域开放环预测，缩小单步训练与多步规划的错配；另一方面学习预算条件、方向敏感的轨迹可达性，并在测试时把它作为搜索信号。在 Wall 任务中，匹配比较的成功率由 50.4% 提升到 83.6%。但它的可达性标签仍来自数据轨迹，只是现实可行性的代理；未观察到的捷径、不确定性和完整约束还没有解决。

这两项工作把问题从“表征是否好”改写为“表征向规划器暴露了什么代价”。它们也解释了为什么仅比较预测损失常常无法预测控制结果：损失平均了所有潜维度，而规划依赖的可能只是少数方向、特定时域和有向可达关系。

## 第三份独立契约：更快的规划仍要保留闭环含义

[Latent Geometry Beyond Search](https://arxiv.org/abs/2605.08732) 尝试把 LeWM 上反复运行的 CEM 摊销掉。它冻结 LeWM，用离线轨迹训练目标条件逆动力学模型，根据当前潜状态、目标潜状态和剩余时域直接输出下一动作；执行后重新编码真实观测，因此仍是闭环控制。在论文八个“环境—协议”单元中，它有七个达到或超过 CEM，Push-T 是例外。

这不是无成本地消除规划，而是把重复在线搜索换成环境内离线监督。论文关于“各向同性 LeWM 几何让逆映射更好学”的理论解释也明确带条件：作者没有验证 LeWM 完全满足所列几何假设，也没有设置 non-isotropic 对照。Push-T 的成功率还会在测试预算从 25 步增至 100 步时由 93.0% 降至 75.0%，与超出训练范围后的 horizon clamp 一致。对于不可逆的多步决策，局部逆映射不能显式比较长期后果，仍可能需要偶发搜索或其他纠错机制。

## 第四份独立契约：层级结构不能自动制造长程能力

短时域模型自然会引出“增加高层子目标”的方案。但 [Mind the Gap](https://arxiv.org/abs/2607.12547) 表明，oracle 轨迹中的中间目标可执行，不代表模型生成的子目标同样可靠。生成 subgoal 可能时间错位，也可能落到低层控制器没有见过的支持分布之外。论文中的经验宏动作 CEM 通过从训练轨迹的 macro-action bank 采样锚点、只在其附近优化 residual，能改善部分设置；收益却依赖时间尺度和执行方式，最长 Push-T 时域中在线受约束重规划优于 staged execution。

因此，长程能力至少要分别评估子目标质量、低层可执行性、高层搜索支持和执行期纠偏。只报告 oracle subgoal 或只增加 hierarchy 层数，会把不同问题折叠成一个看似漂亮的总体成功率。

## 条件、分歧与评测边界

潜表征的另一个分歧是“重建细节”与“任务语义”的权衡。[Reconstruction or Semantics?](https://arxiv.org/abs/2605.06388) 在固定数据、动作条件转移和训练协议下比较两类冻结编码器。在 Bridge V2 的家族级统计中，语义潜空间相对重建潜空间的 VLA 成功率高 9.8 个百分点、OOD 成功率高 13.6 个百分点，一步 CEM 动作误差也更低。与此同时，语义潜变量可能损失精细几何和接触信息，压缩适配器还会在扩散易训练与细粒度控制之间产生取舍。结论应当是“视觉锐利不是控制效用的充分代理”，而不是某个通用视觉模型在所有机器人任务中必然更优。

评测也必须从模型内部指标走到动作后果。[MiraBench](https://arxiv.org/abs/2605.29360) 强调动作跟随、物理遵循与乐观偏差；长 rollout 还需要时间一致性和足够低的决策延迟。真实机器人、接触丰富任务、视角变化和分布外恢复目前仍是 LeWM 主线的薄弱处。V-JEPA 2-AC 虽然提供跨两座实验室的真实部署证据，但其无动作视频预训练不直接包含动作因果，控制来自随后少量机器人数据上的动作条件训练；约 16 秒的已验证时域、人工子目标和相机位置选择也限制了外推。

## 结论与下一步

LeWM 最值得学习的，不是某个单独的速度或成功率数字，而是一条极简、可拆解的研究基线。它把像素、JEPA、动作条件动态和 latent MPC 放进同一个系统，使后续研究可以逐层问出更精确的问题：

1. SIGReg 是否在当前数据分布中既防坍塌又不扭曲任务几何？
2. 固定历史、改变动作时，潜状态位移是否可分辨？
3. 训练时域是否覆盖规划时域，多步误差是否按关键事件而非平均帧统计？
4. 终端代价是否预测有向、预算条件的真实可达性？
5. 加速来自减少模型计算、压缩 rollout，还是把在线搜索摊销成额外离线监督？
6. 改进是否在真实闭环、接触任务、OOD 与失败恢复中仍成立？

下一步最有价值的复现不是简单跑通 LeWM，而是在同一数据和 planner 预算下做分层消融：记录坍塌指标、动作可分性、多时域误差、可达性校准、CEM 搜索效率和闭环成功率，再逐个加入 Delta-JEPA、TRM/RC-aux 或 GC-IDM。这样才能知道收益来自表征、动力学、代价还是控制器，而不是把所有改善归到一个含义过宽的“world model”上。

## References

- [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/abs/2506.09985)
- [LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics](https://arxiv.org/abs/2511.08544)
- [LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels](https://arxiv.org/abs/2603.19312)
- [Fast LeWorldModel](https://arxiv.org/abs/2606.26217)
- [Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding](https://arxiv.org/abs/2606.31232)
- [Predictive Objectives Discard Exogenous Control-Relevant Features](https://arxiv.org/abs/2606.30068)
- [Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics](https://arxiv.org/abs/2605.22164)
- [Predictive but Not Plannable: RC-aux for Latent World Models](https://arxiv.org/abs/2605.07278)
- [Latent Geometry Beyond Search: Amortizing Planning in World Models](https://arxiv.org/abs/2605.08732)
- [Mind the Gap: Promises and Pitfalls of Hierarchical Planning in LeWorldModel](https://arxiv.org/abs/2607.12547)
- [Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models](https://arxiv.org/abs/2605.06388)
- [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360)
