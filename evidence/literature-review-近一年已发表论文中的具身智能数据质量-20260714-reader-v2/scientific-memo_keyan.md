# 近一年已发表论文中的具身智能数据质量：科研备忘录

## 研究边界

版本说明：本轮以 15 篇可获取完整正文的论文为论证主干，逐篇核对问题、方法、结果与限制；未能取得可读全文的论文不再承担正文结论。

本备忘录覆盖 2025 年 7 月 14 日至 2026 年 7 月 14 日公开论文，主题限定在具身智能数据质量，重点落在机器人示教、VLA 微调、跨本体数据、遥操作采集、人类视频迁移和模仿学习数据筛选。本次范围综述从 851 条去重候选中核验 90 篇可用全文，并以 36 篇直接相关论文形成判断。它仍是公开论文的阶段性样本，不是仅限同行评审论文的完整普查。

## 中心判断

近一年论文的共同转向是：具身智能的数据质量不再等同于“清洗坏轨迹”或“采更多轨迹”，而是在目标任务、采集接口、数据分布、轨迹片段和训练过程之间建立闭环。换言之，高质量数据是 target-conditioned utility，而不是全局静态属性。QoQ 直接把质量定义为训练样本对验证示范和策略性能的贡献 [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056)，IWR 把外部数据质量绑定到目标任务分布相关性 [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657)，ATHENA 则显示多任务 VLA 中还必须防止任务覆盖坍缩 [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208)。

## 证据覆盖与限制

证据覆盖三类高信号问题：质量定义和度量（influence functions、PSD、trajectory entropy、importance weighting）；采集端质量塑形（遥操作反馈、UMI gripper 设计、VR 输入模态）；异构或弱质量数据如何进入训练（human video 仿真过滤、suboptimal data 选择性利用、OXE 跨本体扩增）。候选量、全文量、关键维度和连续低新增轮次均已满足停止条件。

## 核心机制

**1. 质量首先是对目标策略有用。** QoQ 反对只用专家相似度、互信息或人工启发式做代理指标，主张用样本对验证示范 loss 降低和策略性能提升的影响来评估轨迹 [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056)。IWR 给出相邻视角：当用外部大规模数据增强少样本任务时，数据是否“好”取决于目标分布与先验分布的概率比，而不是最近邻相似度本身 [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657)。两篇合起来说明，机器人数据质量需要以目标任务和目标策略为参照系，而不是以数据集内部几何为唯一参照。

因此，数据质量的核心不是“效用优先”或“多样性优先”二选一，而是目标效用、任务覆盖和坏轨迹风险之间的约束优化。

**3. 质量从采集工具开始，而不是采完以后再补救。** DQAF 把遥操作 episode 的质量信号拆成任务进度、运动平滑性、停顿、关节极限，并把自然语言反馈闭环给采集员 [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349)。UMI gripper 研究显示，力分布、重量和人体工学会改变示教表现与操作者负担 [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)。VR 研究进一步显示，输入设备和可视化会改变轨迹效率、不必要动作和执行精度，且不同任务偏好不同模态 [From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks](https://arxiv.org/abs/2602.10618)。三项研究共同把质量控制点前移到采集硬件、交互模态、采集员反馈和任务分解，而不只是离线筛选器。

**4. 质量粒度正在从 episode 下探到 segment/chunk。** PSD metric 将低质量 end-user 示教具体化为过度纠正、振荡和突兀调整，提供无需 推演 或专家标签的快速排序 [An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544)。WARP-RM 指出长程遥操作里的次优 episode 往往同时包含停顿、失误和高价值恢复片段，整条丢弃会浪费有用数据，因此需要 frame/chunk 级 progress signal [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320)。

由此可见，episode 级质量分数适合采集员反馈和粗筛，训练阶段则需要更细粒度的片段价值估计。

**5. 异构数据不是“能不能用”，而是“以什么条件进入训练”。** PSI 说明人类视频虽然能扩大数据来源，但必须通过仿真过滤排除位姿估计错误、机器人不可达和 grasp 不兼容轨迹 [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197)。OXE-AugE 把跨本体质量问题表述为 robot/gripper 分布不均衡，指出 OXE 中 top four robot types 占超过 85% 真实数据会带来过拟合风险 [OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning](https://arxiv.org/abs/2512.13100)。

## 五层质量栈

一个可操作的数据质量栈可以分成五层。第一层是 collection interface quality，检验采集硬件、VR 输入方式、遥操作 UI 和采集员反馈是否改变了轨迹质量 [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349), [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189), [From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks](https://arxiv.org/abs/2602.10618)。第二层是 trajectory health，检查平滑性、纠正动作、振荡、停顿和关节极限等可直接从轨迹或遥测中计算的信号 [An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544)。

第三层是 target-conditioned utility，用 validation demonstrations、目标任务分布或 influence/retrieval 权重衡量数据对目标策略是否真正有用 [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056), [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657)。第四层是 coverage and balance，防止高分筛选导致任务、本体、夹爪或场景覆盖坍缩 [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208), [OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning](https://arxiv.org/abs/2512.13100)。

## 条件与分歧

现有结果主要来自特定机器人、任务集和训练配方，因此某种筛选信号在一个项目中有效，不代表它能跨本体、跨任务复用。开放空间抓放可能更看重轨迹平滑与几何覆盖，接触密集任务则更依赖力、触觉和恢复片段。这些差异不应被压缩成一个全局分数。

## 未解决问题

本轮证据尚未给出跨任务通用的质量基准，也缺少能把采集成本、人工复核、训练算力和真机收益放入同一账本的长期实验。另一个缺口是可追溯性：当策略退化时，现有管线很少能反推到具体数据版本、筛选规则和训练阶段。这是本轮检索的证据边界。

## 对后续研究的启发

后续实验应将“删除哪些数据”改写为“哪类数据在哪个训练阶段产生多大边际收益”。最小可行对照应同时报告数据量、覆盖变化、训练成本与真实闭环结果，并保留失败和恢复片段的独立统计。

## 工程落点

把上述证据转成工程动作，最重要的变化是取消单一质量分。采集端记录操作者负担、停顿、过度纠正和关节极限；训练前评估任务相关性、覆盖均衡与可执行性；训练后再用闭环成功率、恢复能力和分布外表现反校准筛选规则。这样才能区分“轨迹看起来整洁”与“轨迹确实改善目标策略”。

这套分层也给出了反例：某条轨迹可能动作不够平滑，却包含稀有失败恢复；某个数据子集与目标任务相似，却让少数任务完全失去覆盖；某种采集设备能提高速度，却增加接触损伤。质量治理的对象因此不是单条样本，而是样本进入特定训练阶段后产生的边际作用。

## 精读复核后的新证据

在移出两个无法取得完整正文的引用后，数据筛选的结论从“识别多样性”进一步收窄到“保留可复用结构与任务覆盖”。[SIEVE](https://arxiv.org/abs/2607.06442) 按原语组合和转换接口分配选择预算，再保留稳定、中心的轨迹；论文报告用一半示教和一半训练步数可优于全量训练。这与 [ATHENA](https://arxiv.org/abs/2606.16208) 对任务覆盖的要求相互补充：数据治理不能只做一个全局高分排名，还要防止小任务被整体淘汰。

同时，[TACO](https://arxiv.org/abs/2607.02840) 把数据质量推进到失败后的纠正片段：触觉感知世界模型联合预测视频与力，再为失败附近状态标注纠正动作。这说明“高质量数据”不只是干净的成功示教，还包括可定位、可恢复的失败边界。

对工程管线而言，这意味着筛选器要同时输出样本效用、任务覆盖和失败可恢复性，而不是只给一个不可解释的总分。只有这三类信号一起进入版本比较，数据质量才能被持续治理。

## References
- [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056)
- [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657)
- [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208)
- [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349)
- [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)
- [From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks](https://arxiv.org/abs/2602.10618)
- [An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544)
- [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320)
- [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197)
- [OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning](https://arxiv.org/abs/2512.13100)
- [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442)
- [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840)
