# 从"预训练技巧"到"跨视角研究范式"：Ego-Exo 后继工作的十年演进

> **研究备忘录** | 主题：第三人称→第一人称视觉表征迁移的演进 | 证据基础：11 篇全文精读论文，20 条经验证证据事件 | 综述模式：scoping
>
> 本备忘录基于经过完整全文提取与 claim-support audit 的论文级证据，所有主张可追溯到具体论文。事件级溯源见 `evidence-appendix.md` 与 `trace-map.json`。

## 1. 研究边界与问题界定

本文回答一个具体问题：Ego-Exo（Li et al., CVPR 2021）提出的"从第三人称视频迁移视觉表征到第一人称"思路，其后继工作如何演进，形成了哪些子方向与数据/方法范式？

证据池由引文分析确定：以 Ego-Exo 为根节点，经 Semantic Scholar 引文图向下游扩展并人工复核，选出 11 篇真正属于 ego-exo / third-person / exo 领域的后继论文，全部完成非 OCR 全文提取与六遍式精读，投影出 20 条证据事件。需要说明：这是一个引文图派生的候选集，不是关键词全量检索，因此不声称覆盖该领域全部工作，也不把"被引影响力"等同于"方法正确性"。

## 2. 中心判断

Ego-Exo 的真正贡献不是某一个模型，而是把一个直觉——"第三人称视频里藏着能被蒸馏到第一人称模型的 egocentric 信号"——变成了一个可复用的**迁移范式**。十年间，这个范式沿三条路线展开：**(1) 数据/基准化**（把视角迁移固化为大规模同步或异步 ego-exo 数据集）；**(2) 任务化**（把"迁移"落到 affordance 定位、对象对应、时序动作分割、视频描述等具体下游任务）；**(3) 前置放松**（从"无需配对/标注 ego 视频"进一步到"无需同步""无需配对""用语言/gaze 桥接"）。

贯穿这三条路线的核心张力是：**难点从来不在"要不要迁移"，而在"用什么信号桥接视角差距"**。Ego-Exo 用自动伪标签，后续工作依次验证了时间同步、gaze、语言对齐、无标注同步视频对作为桥接信号的有效性；而一旦桥接信号缺失或过弱，迁移就退化——这是所有工作共同的边界。

## 3. 核心机制：迁移范式如何层层演进

### 3.1 起点：把 egocentric 信号"蒸馏"进 exo 预训练

[Ego-Exo](https://arxiv.org/abs/2104.07905) 在标准 third-person 视频动作分类预训练之外，用离线 egocentric 模型为 Kinetics 视频生成三类伪标签——egocentricity 分数（Ego-Score）、被操纵物体（Object-Score）、手-物交互时空图（Interaction-Map）——以知识蒸馏损失注入视频模型。关键前置是**不依赖配对或带动作标注的 ego 视频**。结果在 Charades-Ego 上较 Kinetics 预训练基线高 +3.26 mAP，EPIC-Kitchens-100 达当时 SOTA。这个设定定义了后续所有工作的共同问题：在 ego 数据稀缺/无标注约束下，如何把 exo 的知识搬过来。

### 3.2 路线一：从"方法"到"数据集与基准"

Ego-Exo 之后，最显著的一步是把视角迁移**基础设施化**。[Ego-Exo4D](https://arxiv.org/abs/2311.18259)（Grauman 领衔）发布 1286 小时、740 名参与者、8 领域的时间同步第一+第三人称视频，并首次把 ego-exo relation（对象对应 correspondence、视角翻译 translation）形式化为可评测基准任务。这意味着"跨视角迁移"从一个论文技巧变成了一组有标准指标、有 leaderboard 的公共任务。[EgoExoLearn](https://arxiv.org/abs/2403.16182) 更进一步，把设定推进到**异步、异环境**的 demo-following——个体观看 exo 演示后在佩戴 gaze 设备的情况下于不同环境复现程序性任务。[EgoExo-Fitness](https://arxiv.org/abs/2406.08877) 则把双视角延伸到全身健身动作与"做得多好"的可解释动作评判。三者合起来，把 Ego-Exo 的"迁移"补全为"what / when / how well"三个维度的可评测问题。

### 3.3 路线二：桥接信号的迁移谱系

最实质的方法演进集中在"用什么桥接"。这一谱系清晰地显示了一条**信号从强到弱、从前置苛刻到宽松**的路线：

- **时间同步**：[Synchronization is All You Need](https://arxiv.org/abs/2312.02638) 证明，仅用带标注 exo 视频 + 无标注的同步 exo-ego 视频对做知识蒸馏，就能把时序动作分割模型从 exo 迁移到 ego，edit 分数 28.59，与监督式 ego-oracle（26.42）相当，远超仅用 exo 数据的基线（12.60）。同步是强信号，但需要采集同步对。
- **无配对时序对齐**：[AE2](https://arxiv.org/abs/2306.05526)（Xue & Grauman）把前置进一步放松到 unpaired：用 DTW 时序对齐作自监督目标、object-centric 编码器关注手与主动物体、反转帧作负样本，从无配对 ego-exo 视频学到细粒度视角不变表征（Break Eggs 动作相位分类 F1 66.23，超过最佳基线 GTA 的 56.86）。
- **语言/伪配对**：[EgoInstructor](https://arxiv.org/abs/2401.00789) 用 caption 语言对齐自动挖掘 ego-exo 对，EgoExoNCE 损失把跨视角视频特征对齐到共享文本语义，检索 third-person 教学视频作参考增强 egocentric 描述（InternVideo 在 CharadesEgo 上 Ego2Exo/Exo2Ego 分别提升 15.9%/7.7%）。
- **gaze**：[EgoExoLearn](https://arxiv.org/abs/2403.16182) 的基准显示 gaze 是弥合视角差距的有效信号。

### 3.4 路线三：把"迁移"落成具体任务

在静态图像侧，一条独立的 affordance grounding 分支把 exo→ego 迁移做深做实。[Learning Affordance Grounding from Exocentric Images](https://arxiv.org/abs/2203.09905) 提出从第三人称人-物交互图像学可供性知识并迁移到 egocentric 图像（AGD20K，seen 设定 KLD 提升 17.2%），其期刊版 [Grounded Affordance from Exocentric View](https://arxiv.org/abs/2208.13196) 用 CFT 密集匹配显式建模"交互偏差"。[LOCATE](https://arxiv.org/abs/2303.09665) 把迁移细化到部件级，unseen 设定 KLD 提升 20.4%。[ObjectRelator](https://arxiv.org/abs/2411.19083) 则在 Ego-Exo4D 的对象对应任务上用多模态条件 + 跨视角对齐取得 SOTA（IoU Ego2Exo 39.7→44.3）。这条分支的共同教训是：迁移的精度取决于**能不能把 exo 交互中"与任务相关的那部分"（部件、对象、可供性）单独拎出来**，而不是全局搬特征。

## 4. 条件与分歧

1. **桥接信号决定迁移上限，也决定适用边界。** 同步、gaze、语言配对各有效，但都对应不同的采集成本与前置；没有哪种信号是普适的。[EgoExoLearn](https://arxiv.org/abs/2403.16182) 是这条边界的直接证据：即使 co-training ego+exo 并使用 gaze，跨视角关联准确率最高也只到约 55.3%（Exo2Ego test），异步跨视角桥接仍是显著未解决的 gap。
2. **迁移精度受任务粒度制约。** 全局特征蒸馏（Ego-Exo 原版）足够支撑动作识别，但 affordance 定位与对象对应需要部件级/对象级的显式对齐，说明"迁移"不是一个统一操作，而是随任务粒度的变化而分层。
3. **证据面偏斜。** 本池 20 条事件中绝大多数是 support，limit/conditional 证据稀缺，这更多是候选选择（引文派生的"有影响力后继"天然偏正向）所致，而非该领域没有失败；异步关联的 gap 是唯一显式负向信号。

## 5. 可操作框架

| 场景 | 可用桥接信号 | 参考工作 |
|---|---|---|
| 已有同步 ego-exo 视频对 | 时间同步 | Synchronization / EgoExo-Fitness |
| 只有无配对 ego+exo 视频 | 时序对齐 / 伪配对 | AE2 / EgoInstructor |
| 只有 exo 交互图像 + ego 物体图像 | 部件/可供性定位 | Affordance / LOCATE |
| 需评估动作质量 | 专家评判 + gaze | EgoExo-Fitness / EgoExoLearn |

## 6. 研究空白与下一步

- **异步跨视角的稳定桥接仍未解决**（EgoExoLearn 的 55.3% 上限）——这是当前最明确的开放问题。
- 现有工作多在单任务验证，缺乏跨任务统一的"视角不变表征"判据；AE2 提出的是时序对齐代理，EgoInstructor 提出的是语言对齐代理，二者如何统一尚无答案。
- 引文池本身有边界：本 run 未覆盖关键词检索的全量候选，也未纳入 ego-only 的下游工作，因此"演进全貌"仍需一轮 planner 驱动的检索来补全。

## 7. 结论

Ego-Exo 的"第三人称→第一人称迁移"已从一个预训练技巧，长成了一个有数据、有基准、有任务谱系的研究范式。它留下的最有用的遗产不是某个蒸馏损失，而是一个判断：**跨视角迁移的难点在桥接信号，不在迁移本身**。谁能为"异步、无配对、弱监督"的真实场景找到更便宜、更稳的桥接信号，谁就掌握了这条线的下一程。

## References

- [Ego-Exo](https://arxiv.org/abs/2104.07905) — Li, Nagarajan, Xiong, Grauman. CVPR 2021.（根论文）
- [Ego-Exo4D](https://arxiv.org/abs/2311.18259) — Grauman et al. CVPR 2024.
- [EgoExoLearn](https://arxiv.org/abs/2403.16182) — Huang et al. CVPR 2024.
- [Learning Affordance Grounding from Exocentric Images](https://arxiv.org/abs/2203.09905) — Luo et al. CVPR 2022.
- [Grounded Affordance from Exocentric View](https://arxiv.org/abs/2208.13196) — Luo et al. IJCV 2022.
- [LOCATE](https://arxiv.org/abs/2303.09665) — Li et al. CVPR 2023.
- [AE2](https://arxiv.org/abs/2306.05526) — Xue & Grauman. NeurIPS 2023.
- [Synchronization is All You Need](https://arxiv.org/abs/2312.02638) — Quattrocchi et al. ECCV 2024.
- [EgoInstructor](https://arxiv.org/abs/2401.00789) — Xu et al. CVPR 2024.
- [ObjectRelator](https://arxiv.org/abs/2411.19083) — Fu et al. ICCV 2025.
- [EgoExo-Fitness](https://arxiv.org/abs/2406.08877) — Li et al. ECCV 2024.
