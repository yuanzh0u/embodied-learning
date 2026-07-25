# 近一年视频世界模型最可靠的应用任务：排序、边界与部署门槛

## 研究边界

本文将“世界视频模型”界定为：从观测历史和动作条件中预测未来视觉或潜在状态、用于机器人学习与决策的 video world model，而非通用文生视频模型。时间窗口是 2025-07-19 至 2026-07-19。检索池包含 1,589 篇候选论文，175 篇具备可读全文；本结论层使用 30 篇完成全文精读、主张支持审计的论文。

“可靠”不指画面逼真，而指一项任务在明确边界内同时具备：对真实结果有预测或排序价值、对动作条件忠实、在所需时域内不崩溃、错误可被检出或拒绝，且计算成本允许它进入实际流程。这一口径与 [GigaWorld-1](https://arxiv.org/abs/2607.02642)、[MiraBench](https://arxiv.org/abs/2605.29360) 和 [WEAVER](https://arxiv.org/abs/2606.13672) 的评测方向一致。

## 中心判断

近一年最稳健的应用不是“让视频模型直接开机器人”，而是让它担任低权限、可复核、可被真实数据锚定的中间任务。按当前证据强度排序，第一梯队是同分布下的策略离线评估与排序；第二梯队是带真实本体锚定的数据合成、后训练与失败附近纠错，以及训练期的 4D/几何动态监督；有明确物理变量的 what-if 可行性检查已有可用实例，但尚不能推广到开放式长时程规划。直接闭环控制、高接触操作和安全验收目前不应列入“可靠任务”。

这个排序的核心不是模型大小，而是错误能否被系统容纳：结果只用于排序候选方案、合成数据还要经过下游过滤，风险可控；一旦模型拥有直接执行权或安全裁决权，接触动力学、长程漂移和乐观预测就会从“可被筛掉的噪声”变成真实事故。

## 一、策略评估与候选排序：目前证据最强

视频世界模型最清晰的价值，是把原本需要真机、场地和人工监督的大量策略 rollout，前移为低成本筛选。[RoboWorld](https://arxiv.org/abs/2607.01060) 在 DROID/RoboArena 设置中让同一批策略完全在模型内闭环执行，得到的策略排名与真机榜单高度一致。[GigaWorld-1](https://arxiv.org/abs/2607.02642) 则把问题扩展到多个视频世界模型、动作表示和大规模模拟 rollout，指向同一个结论：评估器价值由长时程、动作忠实的结果一致性决定，不是短视频的观感。

但“最强”仍然是有条件的。RoboWorld 验证的是同一数据生态和动作接口下的相对排序，不是每个 episode 的绝对因果保真，更不是安全认证。它还借助任务进度评分器把策略已完成的有效操作与后续的生成伪影分开。因此，当前最合适的产品定位是“大批量淘汰和排名”，由少量真机试验完成最后验收。

## 二、数据生成与后训练：比直接控制更容易可靠

第二类成熟用法是让世界模型生产训练材料，而不是生产最终动作。[Interactive World Simulator](https://arxiv.org/abs/2603.08546) 表明，适量机器人交互数据可以训练可互动模拟器，用来生成策略训练示范；[Hi-WM](https://arxiv.org/abs/2604.21741) 强调在容易失败的状态周围生成密集纠错轨迹，而非继续堆叠成功示范。两者都把生成轨迹放在后训练环节，它们的错误仍可以被质量过滤、策略对照和真机小样本复验拦截。

可扩展不等于无条件。[RoboDream](https://arxiv.org/abs/2606.02577) 通过渲染的机器人运动、场景和物体先验锚定本体，以减少“看起来像机器人，动起来却不可执行”的生成幻觉；[ComSim](https://arxiv.org/abs/2604.11386) 用少量真实数据对齐经典仿真和神经仿真。因而，可靠的不是“纯生成数据”，而是一条有本体约束、真实样本锚定和下游闭环消融的数据管线。

## 三、训练期几何与动态教师：低权限、高价值

第三类值得优先投资的任务，是把视频世界模型当作表征学习和训练期特权教师。[GEM-4D](https://arxiv.org/abs/2605.22882) 把稠密 4D 对应监督蒸馏进视频骨干，推理时可去掉几何分支；这种设计避免在每一个控制步骤里生成完整视频，却保留了身份、运动和几何一致性。[Pri4R](https://arxiv.org/abs/2603.01549) 也支持用 4D point tracks 组织动态监督，但大规模预训练和测试时是否需要显式几何输入仍是开放问题。

这条路线的优势是错误不会立即转化为执行动作，可以通过真机策略对照来判断表征是否真正提高下游动作质量。它同时提醒评测者：不要把视频重建损失当成最终目标。[SANTS](https://arxiv.org/abs/2605.27947) 表明，更充分的去噪并不总能提供更好的动作条件，后期视频可以更精致却更不物理。

## 四、受约束的 what-if 检查与失败恢复：有用，但边界要窄

世界模型参与规划最有说服力的场景，不是从像素中自由幻想所有未来，而是针对明确物理介入问“原方案还能不能执行”。[Path Planning in Physically Viable World Models](https://arxiv.org/abs/2607.00673) 用场景重建与物理修改暴露历史地图上不可见的长程路线失效。这类任务的可靠性来自查询变量、物理模型和拒绝条件都比较明确。

失败恢复也适合采用分层结构：高层识别失败模式、回复阶段和奖励，底层控制器执行 residual 修正。[ReCoVLA](https://arxiv.org/abs/2606.09630) 支持这种“认知判断—控制纠错”分账。但如果训练数据没有真实的扰动与恢复轨迹，模型不会凭空学会重建接触；[TacForeSight](https://arxiv.org/abs/2606.11184) 的证据正好显示恢复任务需要 nominal demonstration 之外的 recovery interaction data。

## 五、为什么直接控制与安全裁决仍不可靠

第一个硬边界是接触。RoboWorld 的失败分析发现，画面在接触前通常稳定，操作开始后物体却可能解体、变形或失去一致性。[Dream-Tac](https://arxiv.org/abs/2606.08737) 之所以同时预测未来视觉和触觉，正因为 RGB 历史无法充分恢复局部接触状态。在柔性物、滑移、摩擦和遮挡任务中，这不是调大模型就会自动消失的问题。

第二个边界是动作接口。[SPACE](https://arxiv.org/abs/2606.24049) 指出，同一条命令在不同控制器、硬件和部署动力学下可以产生不同运动。因此，视频模型看懂了“会发生什么”，也不等于它掌握了目标机器人“应该发什么控制量”。

第三个边界是评测泄漏。[LIBERO-PRO](https://arxiv.org/abs/2510.03827) 显示，在标准 benchmark 上的高分模型，面对物体位置或小幅任务修改时可以几乎崩溃。世界模型如果与策略共享近重复的场景、任务逻辑或动作映射，就可能把记忆当成因果理解。

## 六、任务优先级与最低验收门槛

| 任务 | 当前判断 | 可靠的原因 | 最低验收门槛 |
|---|---|---|---|
| 同分布策略评估、排序与淘汰 | A，最值得优先落地 | 直接对照真机策略排名，错误不直接执行 | 真机排序相关、多场景覆盖、失败不过度乐观、允许拒识 |
| 合成训练数据、策略后训练和失败附近纠错 | A-/B+，条件可靠 | 生成错误可被下游过滤和真机消融拦截 | 本体锚定、生成/真实混合消融、策略闭环增益、负迁移检查 |
| 训练期 4D/几何动态监督与蒸馏 | B+，低权限高价值 | 保留物体身份和跨帧几何，无须授予生成器执行权 | 真机成功率或样本效率增益，不只看视频指标 |
| 明确物理变量下的 what-if 可行性检查、失败恢复建议 | B，边界化可用 | 查询、模型和拒绝条件可明确定义 | 物理参数校准、真实失败/恢复数据、不确定性与拒识 |
| 在线候选动作预演与 test-time planning | C+，有前景但尚在证明 | 可用结果预演补足纯反应策略 | 同计算预算闭环对照、动作忠实、长程稳定、延迟预算 |
| 长时程高接触直接控制、安全认证或上线验收 | D，当前不可交付 | 接触不可观、自回归漂移和本体接口误差会直接转成事故 | 必须保留真机或高保真物理验收，世界模型不得单独裁决 |

## 研究空白与下一步

第一，目前最好的策略评估证据仍高度集中在同本体、同数据生态。需要盲测的跨机器人、跨控制器 sim-real 排序实验。第二，策略级排名相关不等于 episode 级安全可采信；评测应加入失败乐观偏差、对抗动作和风险—覆盖曲线。第三，需要在相同数据、算力、动作候选和真机预算下，直接对照“训练期教师”、“离线评估器”、“在线预演器”三种权限级别，才能确定世界模型的边际价值。

本文的排序可被证伪：如果直接控制型视频世界模型在未见场景、多本体、长时程接触和干扰恢复上，以相同计算与真机数据预算稳定超过“策略 + 离线评估/预演 + 底层控制器”的分层系统，且能识别自己不知道的未来，那么“低权限任务最可靠”就应被修正。

## 结论

近一年的证据已经足以把视频世界模型从“演示未来”推向“影响研发流程”，但还不足以让它单独接管机器人。最合理的落地顺序是：先做策略排序和淘汰，再做有本体锚定的数据/后训练，然后尝试训练期几何教师与受约束 what-if 检查；将在线长程控制与安全验收保留给真实闭环。世界模型当下最值钱的能力，不是替现实做决定，而是在真实试错之前更快地缩小选择空间。

## References

- [RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation](https://arxiv.org/abs/2607.01060)
- [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642)
- [MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models](https://arxiv.org/abs/2605.29360)
- [WEAVER, Better, Faster, Longer](https://arxiv.org/abs/2606.13672)
- [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546)
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](https://arxiv.org/abs/2604.21741)
- [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](https://arxiv.org/abs/2606.02577)
- [ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation](https://arxiv.org/abs/2604.11386)
- [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882)
- [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549)
- [SANTS: A State-Adaptive Scheduler for World Action Models](https://arxiv.org/abs/2605.27947)
- [Path Planning in Physically Viable World Models](https://arxiv.org/abs/2607.00673)
- [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery](https://arxiv.org/abs/2606.09630)
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184)
- [Dream-Tac: A Unified Tactile World Action Model](https://arxiv.org/abs/2606.08737)
- [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049)
- [LIBERO-PRO: Robust and Fair VLA Evaluation Beyond Memorization](https://arxiv.org/abs/2510.03827)
