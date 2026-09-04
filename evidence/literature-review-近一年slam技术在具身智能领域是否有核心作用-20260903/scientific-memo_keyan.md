# 近一年文献中 SLAM 在具身智能的角色：空间职能未被替代，系统形态正在迁移

## 研究边界

本备忘录回答一个研究决策问题：2025 年 9 月至 2026 年 9 月的文献，是否支持"SLAM 在具身智能领域具有核心作用"。综述为范围性设计：六维覆盖查询计划共注册 141 篇候选，48 篇恢复完整非 OCR 全文，39 篇经结构化精读与主张支撑审计进入证据层，投影为 224 条带定位器的证据事件。证据按职能聚簇为四组：视觉定位与建图 82 条、具身模型层 112 条、采集硬件与示教接口 25 条、4D 时空理解 5 条。

该设计能回答"文献呈现何种方向的一致证据"，不能回答三件事：仅见于经典机器人会议、未放预印本的文献覆盖有限；工业部署的实际渗透率没有独立证据源；一年窗口外的趋势不可外推。下文所有数字均出自上述 39 篇的精读证据。

## 中心判断

近一年证据既不支持"SLAM 正被端到端模型淘汰"，也不支持"SLAM 保持原有中心地位"。更准确的判断分三层。第一，在数据生产与评测基准两个环节，SLAM 的度量职能被更深而非更浅地消费：近一年主要的新具身数据设施与导航评测基准都以 SLAM 或视觉-惯性里程计的轨迹为度量骨架，且作者群体普遍把它当可替换商品而非研究焦点。第二，在在线决策回路中，SLAM 从显式中心模块退居为可组合输入；无图端到端路线在短时程、可控环境内拿到了真机证据，但长时程、大尺度、动态与安全关键场景没有任何替代证据，且这些路线自身隐性消费位姿流或几何基础模型。第三，SLAM 技术栈内部正在形态迁移：前端被几何基础模型改造，经典优化后端回归，地图从几何产物变成语言与任务可消费的接口。本判断可证伪：若后续文献显示无图路线在长时程大尺度动态环境下的成功率与度量一致性追平 SLAM 管线，且新一代具身数据设施不再依赖 SLAM 度量骨架，"职能核心"应修正为"职能退役"。

## 机制一：数据生产层——SLAM 已成度量底座，且被当商品消费

具身智能近一年最确定的变化发生在数据侧，而 SLAM 是这个变化的地基。[ActiveUMI](https://arxiv.org/abs/2510.01607) 把 Meta Quest 3 头显定位为整个采集框架的"高精度定位中枢"：头显内的 SLAM 系统同时追踪操作者头部与两只控制器的六自由度位姿，所有示教数据以绝对坐标记录在统一世界系中。位姿回放精度实验中，ActiveUMI 的相对位姿误差为 4.0 毫米，是被它替代的 UMI（10.1 毫米）的约四分之一。这不是孤例：[MobileEgo Anywhere](https://arxiv.org/abs/2605.05945) 用 iPhone 内置的 ARKit 视觉-惯性里程计采集了 200 小时、584 个会话的自我中心数据集，最长单会话 108 分钟；以 30 相机 Vicon 动捕为真值，十段序列中九段相对轨迹误差低于 1%，长时程漂移除全屋遍历（1.5 厘米）外均低于 1 厘米、低于轨迹总长的 0.1%。作者的技术形态判断同样值得记录：COLMAP 在小时级轨迹上计算不可行，特征点 SLAM 在弱纹理室内累积漂移，移动 AR 框架通过高频 IMU 与视觉关键帧融合成为唯一可行选项。[RoSHI](https://arxiv.org/abs/2604.07331) 的全身动捕套装走得更远——以自我中心 SLAM 锚定长时程运动、九个货架级 IMU 补充局部骨向，总硬件成本约 350 美元，而高端商用 IMU 动捕（约 4,500 至 14,000 美元）被作者明确指出"缺乏真正的全局定位"。[UMI-3D](https://arxiv.org/abs/2604.14089) 则证明这条路线的收益边界在扩张：LiDAR 中心的 SLAM 采集使原视觉 UMI 下难以可靠采集的大变形物体操作（窗帘拉动）达到 0.88 至 0.96 的归一化得分，论文将可扩展具身数据采集的瓶颈明确归位于位姿估计的可靠性。

两个限定条件必须同时陈述。其一，存在绕开 SLAM 的替代路线：[U-Arm](https://arxiv.org/abs/2509.02437) 的主从同构遥操作让训练数据的位姿真值直接来自从臂本体编码器，不经过任何外部位姿估计，单臂物料成本 50.5 美元。该路线在固定工位、单臂任务上成立，但难以迁移到 ActiveUMI 式的在野采集。其二，SLAM 保障的数据质量不能替代本体可行性：UMI-3D 的长时程任务成功率沿阶段急剧衰减（开门 97.5% 到抓杯 47.5% 再到放置 5.0%），其中 32.5% 的失败源于示教运动违反机器人逆运动学约束。数据层的小结是：SLAM 在这里的核心地位恰恰表现为"不被讨论"——它从研究问题变成了基础设施，而基础设施的标志就是可替换性：RoSHI 明确设计了把 Aria 眼镜换成"标准 RGB 相机加开源 SLAM 算法"的接口。

## 机制二：模型层——隐式空间能力划出无图可行区间，但未覆盖 SLAM 的职能空间

无图路线的真机证据是真实的。[WAM-Nav](https://arxiv.org/abs/2606.04907) 的潜在世界-动作模型完全不维护地图、定位或里程计模块，在 Unitree G1 人形机器人上跨四个室内外环境实现平均 85% 的任务成功率，全机载部署（RTX 4060 上 1 Hz 推理、MPC 50 Hz 跟踪）。[PanoNav](https://arxiv.org/abs/2511.06840) 以纯 RGB、无度量地图的设定在 HM3D 开放词汇目标导航上取得 43.5 的成功率，超过同设定基线。这类证据划出了无图路线的可行区间——但区间边界在论文自己的消融里写得很清楚。WAM-Nav 的非对称视距实验显示视觉前瞻为一帧时性能最优（50.2），前瞻视距越大单调退化（24 帧时降至 30.4）：短时程的近未来几何约束可靠，长自回归的视觉展开则误差累积。PanoNav 的成功率仍低于全部 RGB-D 输入的方法 6 个点以上；其死锁规避测试中，加入隐式文本记忆使成功率从 12 升至 48，但在高欺骗性场景下仍不足一半。

更大的图景是，基础模型的空间能力本身尚未达到接管该职能的门槛。[Theory of Space](https://arxiv.org/abs/2602.07055) 的认知地图评测给出三个系统性发现：主动-被动差距（要求模型自主采集信息而非消费预给轨迹时，GPT-5.2 平均分从 0.57 降至 0.46）；空间信念惯性（环境改变后重新探索，即便直接观测到新配置，视觉世界中 GPT-5.2 的朝向信念惯性达 68.9%）；以及模态差距（视觉世界的认知地图朝向正确率仅 20.2%，文本世界达 91.0%）。充分性测试提供了机制定位：把真值认知地图作为输入后模型升至约 95% 的近完美水平——瓶颈在于模型无法准确构建该地图，而非表征格式本身。[导航决策失败分析](https://arxiv.org/abs/2601.05529) 补充了安全侧证据：GPT-5 在部分可观测路径规划上 93% 的成功率伴随 7% 的被禁止对角移动；Gemini-2.0 Flash 与 GPT-4o 在完全信息地图任务上随复杂度从 100% 突变崩塌至 0%；Gemini-2.5 Flash 在紧急疏散测试中 32% 的试验把用户导向教授办公室而非逃生出口。世界模型路线同样未成熟：[Target-Bench](https://arxiv.org/abs/2511.17792) 上最强现成视频世界模型的加权总分仅 0.341，远低于真值视频的噪声底 0.862，且规划时域从 8 秒缩短到 4 秒时分数一致提升——长时域无图导航的可靠性尚未建立。VLA 的空间接地同样脆弱：[反事实评测](https://arxiv.org/abs/2602.17659) 中 π0.5 在原训练任务上偏置执行率高达 65.6%，在反事实指令下成功率仅 13.2%；三个相同物体仅靠空间语言区分时，π0.5 的接地率在 20% 至 60% 之间。

本文从这批证据中读出的关键结构性事实是：宣称"无图"的方法几乎都在隐性消费几何或位姿。[FutureNav](https://arxiv.org/abs/2606.30367) 的空间感知来自冻结的 VGGT 几何基础模型编码器，运行时既无地图也无里程计，但几何先验来自前馈几何模型而非凭空产生。[MG-Nav](https://arxiv.org/abs/2511.22609) 的稀疏记忆图几何骨架来自离线采集的带位姿示教游览，论文未讨论这些位姿在真实部署中的来源。[LAMP](https://arxiv.org/abs/2602.11862) 的隐式语言地图以相机位姿为输入域，问题定义显式假定机器人已充分遍历环境、位姿已解决。[VANDERER](https://arxiv.org/abs/2606.14879) 的无图探索用 MASt3R 做几何对应匹配，消融显示去掉该模块后探索面积从 12299 降至 11248。这些不是作弊，而是职能的转移支付：显式 SLAM 模块被移出系统图，其输出的消费者从规划器换成了特征编码器。另一条平行线是把位姿用作训练信号而非运行时模块：[Pose-VLA](https://arxiv.org/abs/2602.19710) 把约 155 万条轨迹的末端位姿统一到相机中心坐标系做预训练，在 RoboTwin 2.0 上超过 π0 约 12 至 14 个百分点，而推理时显式位姿估计的开销为零——空间先验被蒸馏进权重，在线估计被绕开而非被替代。

## 机制三：技术层——前端学习化、后端经典化、语义任务化

SLAM 社区自身的一年之变呈现清晰的三段式。第一段是混合架构的收敛。[ScaRF-SLAM](https://arxiv.org/abs/2606.00307) 的系统主张最具代表性：不用几何基础模型做状态估计，用经典视觉 SLAM 做鲁棒低延迟追踪、基础模型专用于稠密建图——其对照实验显示，正确初始化的 ORB-SLAM3 在 EuRoC 五个序列上的轨迹误差全部低于 MASt3R-SLAM 与 VGGT-SLAM2 等全基础模型系统；锚定 SLAM 位姿的建图在精确度上超全部对比方法 10% 至 20%，且输入批次从 11 降到 6 时精度仅降 1.60%（直接聚合基础模型预测降 8.03%）。[MASt3R-Fusion](https://arxiv.org/abs/2509.20757) 与 [FoundationSLAM](https://arxiv.org/abs/2512.25008) 从另一端收敛到同一结构：前者把前向点图回归与 IMU、GNSS 紧耦合，在 KITTI-360 公里级序列上按长度归一化的绝对轨迹误差为 0.05%，而 ORB-SLAM3 为 0.63%、纯视觉的 VGGT-Long 为 2.91% 且在洞穴序列上全部失败；后者把冻结的深度基础模型先验嵌入流式可微束调整，在 TUM 与 EuRoC 上取得对比系统中最优精度并在单卡上 18 FPS。反方向的证据同样在：[VGGT-SLAM++](https://arxiv.org/abs/2604.06830) 在未标定灰度 EuRoC 上误差 2.666 米，DROID-SLAM 为 0.027 米——学习前端的域差距被明确暴露。这些结果合成的判断是：学习几何的进展不必替换经典几何管线，而是通过系统级集成兑现。

第二段是失效边界的量化。[ScaleMaster](https://arxiv.org/abs/2602.18174) 基准显示，三个代表性深度单目 SLAM 系统在 884 米的全楼环游序列上出现灾难性尺度失效（DROID-SLAM 误差 89.35 米、MASt3R-SLAM 80.54 米）；更微妙的是"位姿准不等于地图对"——MASt3R-SLAM 在某图书馆序列上轨迹误差仅 0.12 米，但稠密地图近全图塌缩。[空间记忆综述](https://arxiv.org/abs/2604.16482) 则量化了部署侧的内存墙：SplaTAM 的运行时内存是持久地图的 55 倍（14 GB 对 254 MB），外推到 100 平方米公寓约需 200 GB，超过数据中心级 GPU；对照 ORB-SLAM3 以 55 MB 地图、单核 CPU 20 至 30 FPS 运行。决定部署可行性的不是范式标签，而是内存架构。

第三段是地图的语义化与任务化，即 SLAM 输出向具身任务接口的改造。[LEGO-SLAM](https://arxiv.org/abs/2511.16144) 复用建图阶段计算的语言特征做回环检测，在三个数据集上的轨迹误差均低于位置基线（Replica 0.22 对 0.28 厘米）；[SuperMap](https://arxiv.org/abs/2608.22896) 把 SLAM 时空地图定位为 VLM 空间接地的必要接口，其在线实例级分割大幅超越离线基线（椅子的检测精度 63.76 对 0 至 4.58），并在全板载硬件上实时运行；[GaussLite](https://arxiv.org/abs/2606.30809) 的建图密度以自然语言任务规格为条件；[RoboAtlas](https://arxiv.org/abs/2606.26046) 把视觉-语言推理直接集成进实时主动 SLAM 管线，用 7B 规模的模型在 GOAT-Bench 上取得 88.8% 成功率、超过全部用 GPT-4o 的基线——语义建图框架的信息价值高于底层模型规模。[OGScene3D](https://arxiv.org/abs/2603.16301) 则从需求侧确认了方向：开放词汇场景理解正被重新设计为 SLAM 式的增量在线形态，因为机器人任务必须在渐进探索中执行，而其在线位姿完全由 DROID-SLAM 提供。

## 机制四：评测层——替代路线的度量基础设施站在 SLAM 上

一个容易被忽略但结构性重要的事实：宣称替代或绕开 SLAM 的工作，其评测真值大多由 SLAM 生产。Target-Bench 的 450 个场景以四足机器人 SLAM 估计的轨迹为真值，[WorldMAP](https://arxiv.org/abs/2604.07957) 的评测闭环同样建立在 SLAM 轨迹的投影对齐上；ScaleMaster 的参考地图由 LiDAR 点云投影到 ARKit 轨迹构建；RoboAtlas 在 Habitat 中的大规模评测直接消费模拟器真值位姿，绕过了其真机栈中的 SLAM Toolbox；VANDERER 的探索覆盖率按仿真器全局真值俯视地图计算。这意味着"无图方法优于有图方法"的声明，目前多数由 SLAM 或仿真基础设施背书；在真实开放世界中不依赖外部真值的自评协议仍是空白。

## 条件与分歧

上述判断在四类条件下弱化或存在分歧。尺度条件：[空间智能体综述](https://arxiv.org/abs/2602.01644) 以传感约束划分三尺度，中观尺度（1 至 100 米）度量 SLAM 可解，宏观尺度（超 100 米）需外部感知——本文判断在中观尺度内有最强证据。场景条件：动态环境中轻地图反而更稳，MG-Nav 插入随机障碍后成功率仅从 73.53 降至 68.63，稠密地图方法 BSC-Nav 从 25.49 崩至 7.84；静态桌面操作不需要在线 SLAM，Pose-VLA 的全部验证在静态桌面设定内完成。方法论分歧：[SenseNova-SI](https://arxiv.org/abs/2511.13719) 主张空间智能是数据问题而非架构问题（其空间数据缩放至 850 万问答对），同时承认"单靠数据缩放不太可能达到人类水平"；[FALCON](https://arxiv.org/abs/2510.17439) 给出避开显式 3D 输入的结构性理由——大规模操作数据集缺乏对齐的 3D 标注、专用传感器难部署。产业侧参照：[具身算子白皮书](https://arxiv.org/abs/2607.03283) 把 SLAM 与导航列入近期优先建设的算子清单，其主张的分层部署架构中确定性规划器与控制器承担安全约束。这些分歧不改变职能判断，但决定了"哪个环节用哪种形态的 SLAM"。

## 可操作框架

| 环节 | SLAM 当前职能 | 替代路线的证据区间 | 决策参照 |
|---|---|---|---|
| 数据采集 | 世界系位姿流与度量骨架 | 主从同构的编码器真值（固定工位、单臂） | 在野采集、跨场景泛化、可变形任务选 SLAM 骨架 |
| 在线导航 | 全局度量一致性 | 短时程可控环境（人形真机 85%） | 长时程、回访、安全关键保留 SLAM；反应式短视距可端到端 |
| 操作策略 | 预训练空间先验（零推理开销） | 纯 RGB 前馈（深度注入有增量但模型对缺失鲁棒） | 显式 3D 推理在部署侧尚无收益证据 |
| 语义记忆 | 时空地图作为 VLM 接地接口 | 稀疏快照记忆（动态场景更稳） | 长时驻留环境选实例级时空图；动态频繁环境选轻记忆 |
| 评测 | 真值轨迹生产 | 动捕、仿真真值 | 无图方法的开放世界自评仍是空白 |

## 研究空白与下一步

本次 run 的覆盖缺口：邻接维度中产业部署与 SLAM 芯片化证据薄弱，事件相机仅一篇基准文献进入证据层。文献自身声明的缺口：跨会话尺度歧义（单段视频分三会话运行产生的地图碎片无法按统一尺度合并，被定位为长期建图的主要挑战）；统一空间表示（综述六大挑战之首，点云用于抓取、拓扑图用于导航、栅格用于地理分析的碎片现状）；长时程记忆评测（30 观测每秒下 128K 上下文在 90 分钟内耗尽，现行基准不评测数小时级任务）。下一步值得追踪的汇合点有二：几何基础模型作为 SLAM 前端的收敛设计（ScaRF-SLAM、MASt3R-Fusion、FoundationSLAM 已呈现同构性），以及具身模型消费结构化空间记忆的接口标准化（白皮书算子化路线与 SuperMap 类系统）。

## 结论

对"SLAM 是否在具身智能领域有核心作用"的回答是：空间职能核心、系统形态迁移。过去一年的证据里，SLAM 没有从任何环节退场——它从导航栈的中心变成了数据工厂的度量底座、评测基准的真值来源、语义记忆的几何骨架，以及无图路线背后被转移支付的几何先验。真正发生替代竞争的只有在线决策回路，而那里的证据边界清晰：短时程可控环境内端到端可行，长时程、大尺度、动态与安全关键场景仍是 SLAM 管线的领地，且技术栈自身正在通过混合架构与语义接口重塑。研究决策上，值得押注的方向不是"SLAM 与端到端二选一"，而是两者之间的接口：位姿流作为训练信号、时空地图作为模型接地接口、几何基础模型作为 SLAM 前端。

## References

1. [ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Teaching](https://arxiv.org/abs/2510.01607)
2. [MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data collection](https://arxiv.org/abs/2605.05945)
3. [RoSHI: A Versatile Robot-oriented Suit for Human Data In-the-Wild](https://arxiv.org/abs/2604.07331)
4. [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to LiDAR-empowered](https://arxiv.org/abs/2604.14089)
5. [U-ARM: Ultra low-cost general teleoperation interface for robot manipulation](https://arxiv.org/abs/2509.02437)
6. [WAM-Nav: Asymmetric Latent World-Action Modeling for Unified Visual Navigation](https://arxiv.org/abs/2606.04907)
7. [PanoNav: Mapless Zero-Shot Object Navigation with Panoramic Scene Parsing](https://arxiv.org/abs/2511.06840)
8. [Theory of Space: Can Foundation Models Construct Spatial Beliefs through Active Exploration?](https://arxiv.org/abs/2602.07055)
9. [Before We Trust Them: Decision-Making Failures in Navigation of Foundation Models](https://arxiv.org/abs/2601.05529)
10. [Target-Bench: Can Video World Models Achieve Mapless Path Planning with SLAM-Free Precision?](https://arxiv.org/abs/2511.17792)
11. [When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLA Models](https://arxiv.org/abs/2602.17659)
12. [FutureNav: Unified World-Action Modeling for Vision-and-Language Navigation](https://arxiv.org/abs/2606.30367)
13. [MG-Nav: Dual-Scale Visual Navigation via Sparse Spatial Memory](https://arxiv.org/abs/2511.22609)
14. [LAMP: Implicit Language Map for Robot Navigation](https://arxiv.org/abs/2602.11862)
15. [VANDERER: Map-Free Exploration using Future-Aware and Visual-Curiosity Policies](https://arxiv.org/abs/2606.14879)
16. [PoseVLA: Universal Pose Pretraining for Generalizable Vision-Language-Action Models](https://arxiv.org/abs/2602.19710)
17. [ScaRF-SLAM: Scale-Consistent Reconstruction with Feed-Forward Models and Classical SLAM](https://arxiv.org/abs/2606.00307)
18. [MASt3R-Fusion: Integrating Feed-Forward Visual Model with IMU, GNSS for Robust SLAM](https://arxiv.org/abs/2509.20757)
19. [FoundationSLAM: Unleashing the Power of Depth Foundation Models for Enhanced SLAM](https://arxiv.org/abs/2512.25008)
20. [VGGT-SLAM++: Spatially Corrected Back-End for Feed-Forward SLAM](https://arxiv.org/abs/2604.06830)
21. [Have We Mastered Scale in Deep Monocular Visual SLAM? The ScaleMaster Benchmark](https://arxiv.org/abs/2602.18174)
22. [A Survey of Spatial Memory Representations for Efficient Robot Navigation](https://arxiv.org/abs/2604.16482)
23. [LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM](https://arxiv.org/abs/2511.16144)
24. [SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation](https://arxiv.org/abs/2608.22896)
25. [GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Embodied Mapping](https://arxiv.org/abs/2606.30809)
26. [RoboAtlas: Contextual Active SLAM](https://arxiv.org/abs/2606.26046)
27. [OGScene3D: Incremental Open-Vocabulary 3D Gaussian Scene Graph Mapping](https://arxiv.org/abs/2603.16301)
28. [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction](https://arxiv.org/abs/2604.07957)
29. [From Perception to Action: Spatial AI Agents and World Models](https://arxiv.org/abs/2602.01644)
30. [Scaling Spatial Intelligence with Multimodal Foundation Models](https://arxiv.org/abs/2511.13719)
31. [From Spatial to Actions: Grounding Vision-Language-Action Model in Spatial Foundation Model](https://arxiv.org/abs/2510.17439)
32. [Embodied Operators and Benchmarking: Toward Reusable and Deployable Embodied AI](https://arxiv.org/abs/2607.03283)
