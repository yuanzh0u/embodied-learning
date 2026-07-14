# 近一年已发表论文中的具身智能数据质量：科研备忘录

## 研究边界

本备忘录覆盖 2025 年 7 月 14 日至 2026 年 7 月 14 日公开论文，主题限定在具身智能数据质量，重点落在机器人示教、VLA 微调、跨本体数据、遥操作采集、人类视频迁移和模仿学习数据筛选。本次范围综述从 851 条去重候选中核验 90 篇可用全文，并以 36 篇直接相关论文形成判断。它仍是公开论文的阶段性样本，不是仅限同行评审论文的完整普查。

## 中心判断

近一年论文的共同转向是：具身智能的数据质量不再等同于“清洗坏轨迹”或“采更多轨迹”，而是在目标任务、采集接口、数据分布、轨迹片段和训练过程之间建立闭环。换言之，高质量数据是 target-conditioned utility，而不是全局静态属性。QoQ 直接把质量定义为训练样本对验证示范和策略性能的贡献 [相关研究](https://arxiv.org/abs/2603.09056)，IWR 把外部数据质量绑定到目标任务分布相关性 [相关研究](https://arxiv.org/abs/2509.01657)，ATHENA 则显示多任务 VLA 中还必须防止任务覆盖坍缩 [相关研究](https://arxiv.org/abs/2606.16208)。

## 证据覆盖与限制

证据覆盖三类高信号问题：质量定义和度量（influence functions、PSD、trajectory entropy、importance weighting）；采集端质量塑形（遥操作反馈、UMI gripper 设计、VR 输入模态）；异构或弱质量数据如何进入训练（human video 仿真过滤、suboptimal data 选择性利用、OXE 跨本体扩增）。候选量、全文量、关键维度和连续低新增轮次均已满足停止条件。

这个覆盖足以支持“数据质量是闭环工程”的中心论点，但还不足以给出统一 基准 或跨任务通用阈值，这是本轮文献中的明显空白 [相关研究](https://arxiv.org/abs/2605.01544), [相关研究](https://arxiv.org/abs/2603.11634), [相关研究](https://arxiv.org/abs/2606.12365)。

## 核心机制

**1. 质量首先是对目标策略有用。** QoQ 反对只用专家相似度、互信息或人工启发式做代理指标，主张用样本对验证示范 loss 降低和策略性能提升的影响来评估轨迹 [相关研究](https://arxiv.org/abs/2603.09056)。IWR 给出相邻视角：当用外部大规模数据增强少样本任务时，数据是否“好”取决于目标分布与先验分布的概率比，而不是最近邻相似度本身 [相关研究](https://arxiv.org/abs/2509.01657)。两篇合起来说明，机器人数据质量需要以目标任务和目标策略为参照系，而不是以数据集内部几何为唯一参照。

**2. 质量还必须保留覆盖，而不是只取高分样本。** ATHENA 证明在多任务 VLA 微调中，单一全局 influence 排序会把某些任务几乎淘汰，造成任务级 coverage collapse，因此需要把 task-local utility 与 cross-task utility 放在同一个质量函数中 [相关研究](https://arxiv.org/abs/2606.16208)。FAKTUAL 则从反方向给出边界：多样性是质量的一部分，但 diversity maximization 不能保证排除有害轨迹 [相关研究](https://arxiv.org/abs/2603.11634)。

因此，数据质量的核心不是“效用优先”或“多样性优先”二选一，而是目标效用、任务覆盖和坏轨迹风险之间的约束优化。

**3. 质量从采集工具开始，而不是采完以后再补救。** DQAF 把遥操作 episode 的质量信号拆成任务进度、运动平滑性、停顿、关节极限，并把自然语言反馈闭环给采集员 [相关研究](https://arxiv.org/abs/2605.26349)。UMI gripper 研究显示，力分布、重量和人体工学会改变示教表现与操作者负担 [相关研究](https://arxiv.org/abs/2603.17189)。VR 研究进一步显示，输入设备和可视化会改变轨迹效率、不必要动作和执行精度，且不同任务偏好不同模态 [相关研究](https://arxiv.org/abs/2602.10618)。三项研究共同把质量控制点前移到采集硬件、交互模态、采集员反馈和任务分解，而不只是离线筛选器。

**4. 质量粒度正在从 episode 下探到 segment/chunk。** PSD metric 将低质量 end-user 示教具体化为过度纠正、振荡和突兀调整，提供无需 推演 或专家标签的快速排序 [相关研究](https://arxiv.org/abs/2605.01544)。WARP-RM 指出长程遥操作里的次优 episode 往往同时包含停顿、失误和高价值恢复片段，整条丢弃会浪费有用数据，因此需要 frame/chunk 级 progress signal [相关研究](https://arxiv.org/abs/2606.28320)。

由此可见，episode 级质量分数适合采集员反馈和粗筛，训练阶段则需要更细粒度的片段价值估计。

**5. 异构数据不是“能不能用”，而是“以什么条件进入训练”。** PSI 说明人类视频虽然能扩大数据来源，但必须通过仿真过滤排除位姿估计错误、机器人不可达和 grasp 不兼容轨迹 [相关研究](https://arxiv.org/abs/2602.13197)。OXE-AugE 把跨本体质量问题表述为 robot/gripper 分布不均衡，指出 OXE 中 top four robot types 占超过 85% 真实数据会带来过拟合风险 [相关研究](https://arxiv.org/abs/2512.13100)。

Ambient Diffusion Policy 更进一步：suboptimal/OOD data 会随着规模化持续增长，质量治理应决定它们在训练过程中的贡献方式，而不只是过滤掉 [相关研究](https://arxiv.org/abs/2606.12365)。

## 五层质量栈

一个可操作的数据质量栈可以分成五层。第一层是 collection interface quality，检验采集硬件、VR 输入方式、遥操作 UI 和采集员反馈是否改变了轨迹质量 [相关研究](https://arxiv.org/abs/2605.26349), [相关研究](https://arxiv.org/abs/2603.17189), [相关研究](https://arxiv.org/abs/2602.10618)。第二层是 trajectory health，检查平滑性、纠正动作、振荡、停顿和关节极限等可直接从轨迹或遥测中计算的信号 [相关研究](https://arxiv.org/abs/2605.01544)。

第三层是 target-conditioned utility，用 validation demonstrations、目标任务分布或 influence/retrieval 权重衡量数据对目标策略是否真正有用 [相关研究](https://arxiv.org/abs/2603.09056), [相关研究](https://arxiv.org/abs/2509.01657)。第四层是 coverage and balance，防止高分筛选导致任务、本体、夹爪或场景覆盖坍缩 [相关研究](https://arxiv.org/abs/2606.16208), [相关研究](https://arxiv.org/abs/2512.13100)。

第五层是 training-time utilization，决定低质量、suboptimal 或 OOD 数据是被丢弃、降权、分阶段利用，还是拆成可用 chunk [相关研究](https://arxiv.org/abs/2606.28320), [相关研究](https://arxiv.org/abs/2606.12365)。

## 条件与分歧

论文并不支持一个统一的“质量分数”。PSD 适合快速筛出抖动和纠正动作，但它不是任务可执行性或目标分布相关性的完整代理 [相关研究](https://arxiv.org/abs/2605.01544)。FAKTUAL 的多样性指标能改善或匹配全量数据表现，但作者明确承认它不保证只选高质量轨迹 [相关研究](https://arxiv.org/abs/2603.11634)。VR 和 UMI 论文也提醒，采集模态对不同任务的影响不一致，不能把某个硬件或交互方案泛化为全场景最优 [相关研究](https://arxiv.org/abs/2603.17189), [相关研究](https://arxiv.org/abs/2602.10618)。

## 未解决问题

本轮文献的缺口有三类。第一，缺少跨任务、跨本体、跨采集设备的统一数据质量 基准，现有工作多在特定数据集、特定任务或特定模型上验证 [相关研究](https://arxiv.org/abs/2605.01544), [相关研究](https://arxiv.org/abs/2606.16208)。第二，许多方法仍依赖验证示范、目标任务分布或任务成功定义，一旦目标任务变化，质量排序可能重排 [相关研究](https://arxiv.org/abs/2603.09056), [相关研究](https://arxiv.org/abs/2509.01657)。第三，对“坏数据中的好片段”已有 WARP-RM 和 Ambient Diffusion Policy 这类方向，但还没有统一回答何时过滤、何时降权、何时分阶段训练 [相关研究](https://arxiv.org/abs/2606.28320), [相关研究](https://arxiv.org/abs/2606.12365)。

## 对后续研究的启发

对具身智能数据工程来说，建议把数据质量表从单个 `quality_score` 扩展成多列：采集接口质量、轨迹健康度、目标相关性、覆盖均衡度、可执行性过滤、训练利用策略和闭环收益。这个建议是对 12 篇论文的综合推论，不是任一论文的单独结论；它由 QoQ/IWR 的目标效用、DQAF/PSD 的轨迹健康、ATHENA/OXE-AugE 的覆盖均衡、PSI/ADP/WARP-RM 的条件利用共同支撑 [相关研究](https://arxiv.org/abs/2603.09056), [相关研究](https://arxiv.org/abs/2605.26349), [相关研究](https://arxiv.org/abs/2606.16208), [相关研究](https://arxiv.org/abs/2602.13197), [相关研究](https://arxiv.org/abs/2606.12365)。

## 工程落点

把上述证据转成工程动作，最重要的变化是取消单一质量分。采集端记录操作者负担、停顿、过度纠正和关节极限；训练前评估任务相关性、覆盖均衡与可执行性；训练后再用闭环成功率、恢复能力和分布外表现反校准筛选规则。这样才能区分“轨迹看起来整洁”与“轨迹确实改善目标策略”。

这套分层也给出了反例：某条轨迹可能动作不够平滑，却包含稀有失败恢复；某个数据子集与目标任务相似，却让少数任务完全失去覆盖；某种采集设备能提高速度，却增加接触损伤。质量治理的对象因此不是单条样本，而是样本进入特定训练阶段后产生的边际作用。

## References

- [2509.01657](https://arxiv.org/abs/2509.01657) Data Retrieval with Importance Weights for Few-Shot Imitation Learning.
- [2512.13100](https://arxiv.org/abs/2512.13100) OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning.
- [2602.10618](https://arxiv.org/abs/2602.10618) From Interaction to Demonstration Quality in Virtual Reality.
- [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos.
- [2603.09056](https://arxiv.org/abs/2603.09056) Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning.
- [2603.11634](https://arxiv.org/abs/2603.11634) Diversity You Can Actually Measure.
- [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning.
- [2605.01544](https://arxiv.org/abs/2605.01544) An Efficient Metric for Data Quality Measurement in Imitation Learning.
- [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation.
- [2606.12365](https://arxiv.org/abs/2606.12365) Ambient Diffusion Policy.
- [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA.
- [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM.
