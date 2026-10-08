# 智驾模型中的语言、动作与基础模型：核心论文、技术接口和团队

## 研究边界

本次调研面向需要选择研究切入点、理解技术栈并定位相关团队的研究者。重点时间为 2024-09-27 至 2026-09-27，补充必要前序；20 篇论文经过完整非 OCR 全文恢复、问题驱动阅读和主张审计，其中选择 8 篇核心工作。Tesla 与 Waymo 的工业系统另按官方披露记录，不计入论文数量。本次未运行模型复现实验，也不构造跨评测协议的性能榜单。

## 中心判断

**中心判断：当前证据支持把语言看作可放在不同训练阶段和系统接口上的能力，而不能仅凭“VLA”标签判断驾驶能力或部署形态。** 有用的比较单位是：什么数据进入共享表征，哪些监督改变规划，语言是否实际参与车端决策，动作如何生成，以及错误能否在环境反馈中被发现。本文据此推断，语言收益更可能来自与驾驶动作相关的约束和监督，而非单纯增加文字输出。若在匹配数据、算力、骨干和闭环协议的实验中，通用场景描述能稳定获得与动作对齐监督相同的收益，这个判断应被修正。

配套材料为[核心论文与系统表](core-papers-systems.md)、[技术栈表](technology-stack.md)、[组织人员表](organization-people.md)及[关系图](relationships.md)。具体来源、版本和缺项均保留在这些表及证据附录中。

## 语言在驾驶链条中的位置，比模型名称更有解释力

驾驶理解、决策和动作输出首先应分开。LingoQA 研究视频问答；DriveLM 用图式问答组织感知、预测和规划语义，其动作实验仍主要是开放环；这些工作可以说明模型理解了什么，却不能据此推导车辆能够稳定执行。LMDrive 则把相机、LiDAR 和指令映射为路点，再由 PID 控制，已经具有语言到执行的接口，但连续复杂指令仍比单句困难。[LingoQA](https://arxiv.org/abs/2312.14115)、[DriveLM](https://arxiv.org/abs/2312.14150)、[LMDrive](https://arxiv.org/abs/2312.07488)

核心工作 DriveVLM 与 EMMA 给出两种重要组织方式。DriveVLM-Dual 把低频 VLM 产生的计划交给高频驾驶系统细化，论文报告双 OrinX 的实车部署；它展示了语言语义如何进入既有驾驶栈，并不要求所有模块统一为一个语言模型。EMMA 则在 Gemini 基础上把非传感器输入输出统一为文本，通过共同训练连接规划、检测和路网任务。前者强调接口和频率分工，后者强调表示与任务共享，两者都不能直接简化为“一个模型从像素控制车辆”。[DriveVLM](https://arxiv.org/abs/2402.12289)、[EMMA](https://arxiv.org/abs/2410.23262)

语言参与训练也值得纳入主线。DiMA 通过共享场景编码器、结构化辅助任务和蒸馏改善视觉规划器，默认部署可以不运行 LLM；朴素地把问答与规划损失相加，收益却不一致。nuReasoning 的 nuVLA 在训练时接受推理监督，推理时关闭显式文字推理，仍报告开放环规划改善。这些结果说明应分别登记“语言训练来源”和“车端运行模块”，不能将部署时不说话误判为训练中没有语言贡献。[DiMA](https://arxiv.org/abs/2501.09757)、[nuReasoning](https://arxiv.org/abs/2605.31572)

## 关键问题是语义怎样约束动作，以及约束是否有效

ORION、AutoVLA 和 Alpamayo-R1 是理解动作接口的三篇核心论文。ORION 用 LLM 的 planning token 条件化轨迹分布，再通过 VAE 与 GRU 生成轨迹；AutoVLA 把离散驾驶运动码本加入 VLM 词表，用同一自回归过程生成推理和动作；Alpamayo-R1 在训练阶段注入离散动作 token，但推理时由读取 VLM 缓存的连续 flow-matching 动作专家生成控制量，再积分为轨迹。因此，“VLA 输出动作”至少覆盖隐表征接口、离散动作词表和连续动作专家三种不同实现，训练目标与延迟来源也随之不同。[ORION](https://arxiv.org/abs/2503.19755)、[AutoVLA](https://arxiv.org/abs/2506.13757)、[Alpamayo-R1](https://arxiv.org/abs/2511.00088)

SimLingo 是检验语言独立贡献的关键工作。它用同一视觉场景下不同指令与轨迹的配对，迫使模型学习指令如何改变驾驶行为。其消融没有发现未对齐语言任务对驾驶的明确影响，思维链收益也未达统计显著。EMMA 的消融同样显示，普通场景描述影响中性，关键物体和元决策更有帮助。两者共同支持“监督内容与动作相关性”这个判断，但还不足以证明语言在所有长尾情形中都无益或必不可少。[SimLingo](https://arxiv.org/abs/2503.09594)、[EMMA](https://arxiv.org/abs/2410.23262)

后训练还必须区分反馈来源。AutoVLA 以组相对优化结合驾驶目标和推理长度约束；Alpamayo-R1 同时奖励推理质量、推理与动作一致性及轨迹表现，单独奖励推理可能损害轨迹指标和一致性。MindDrive 则在 CARLA 中收集交互回报，用 PPO 更新决策专家，动作专家在该阶段保持固定。离线候选轨迹评分与环境交互强化学习解决的问题不同，不能仅因都使用“RL”便认作同一种学习机制。[AutoVLA](https://arxiv.org/abs/2506.13757)、[Alpamayo-R1](https://arxiv.org/abs/2511.00088)、[MindDrive](https://arxiv.org/abs/2512.13636)

文字解释也不是行为证据。《Is VLA Reasoning Faithful?》 对小规模样本做关键词、运动学谓词及图像干预，发现解释与动作不一致的情形，可作为失败分析入口；其样本、判定规则与干预方式不足以支持对整个系统安全率或真实因果机制的概括。研究设计应直接检查“看到障碍—选择停车—实际减速”是否一致，而不只检查解释是否流畅。[《Is VLA Reasoning Faithful?》](https://arxiv.org/abs/2605.17268)

## 非语言策略与部署压缩，决定比较是否公平

DiffusionDrive 是本次保留的非语言核心对照。它从带噪轨迹锚点出发进行少步去噪，再以学习得到的置信度选择轨迹。它证明动作分布建模可以独立于语言进行研究，也为评估 VLA 增益提供更有力的对照。经典前序 UniAD 则通过任务 query 连接感知、预测与规划，并保留中间监督和推理期避碰优化；端到端训练并不意味着没有结构化模块或运行时约束。[DiffusionDrive](https://arxiv.org/abs/2411.15139)、[UniAD](https://arxiv.org/abs/2212.10156)

Orion-Lite 直接蒸馏 ORION 的 planning-token 表征，推理时以轻量 transformer 替换大型 LLM，并移除文本提示。这个结果支持压缩语言教师带来的表征，却不能证明教师在训练中无用；论文的模块加速也不能换算成整车同倍数加速，视觉编码仍可能占据主要延迟。另一延伸 FlashDrive 对 Alpamayo 1.5 的视觉编码、预填充、串行解码和动作生成分别优化，说明部署瓶颈需按组件定位，其硬件与模型版本不能同 Alpamayo-R1 的原始延迟直接排名。[Orion-Lite](https://arxiv.org/abs/2604.08266)、[FlashDrive](https://arxiv.org/abs/2608.12932)

对项目而言，应先固定传感器、历史窗口、导航输入、训练样本和评测协议，再比较纯视觉动作头、训练期语言教师与在线语言推理。否则更大预训练数据、不同轨迹选择规则或更多推理算力，都可能被误记为“语言增益”。AutoVLA 的部分离线结果采用多个样本的 oracle 选择，CARLA 又采用不同训练配置，尤其不能把各表最佳结果拼成一个部署方案。[AutoVLA](https://arxiv.org/abs/2506.13757)

## Tesla 与 Waymo：企业公开披露中的驾驶基础模型

**本节属于企业公开披露，未经本文独立性能验证，也不属于论文主张审计。** Tesla 必须作为核心系统案例保留，但现有来源不足以把“Tesla foundation model”落实为一篇固定架构、完整开放训练配方的论文。CVPR 2023 议程可以核实 Phil Duan 的报告题目与当时职衔；它本身不能证明模型层数、动作接口或损失函数。[CVPR 2023 原始议程](https://opendrivelab.com/cvpr2023/workshop/)

Tesla 的 CVPR 2026 官方页面分别列出 Ashok Elluswamy 的 pixels-to-actuation 多模态模型报告、Phil Duan 的端到端 driving policy 与车队数据筛选报告，并将视频生成展示单列。Q1 2026 更新另披露 FSD v14.3 的强化学习阶段、视觉编码器及运行时调整。可以据此把 Tesla 置于车队数据驱动的驾驶策略演进主线；不能进一步认定其属于某种公开 VLA、推定语言是否完全缺席，或把视频生成组件当成已证实运行在驾驶控制链上的世界模型。[Tesla CVPR 2026](https://www.tesla.com/hr_hr/event/tesla-x-cvpr-2026)、[Q1 2026 更新，第 8 页](https://ir.tesla.com/_flysystem/s3/sec/000162828026026551/tsla-20260422-gen.pdf)

Waymo 的官方技术文章更明确地描述了快速传感器融合、较慢的驾驶 VLM、world decoder，以及共享基础模型对 Driver、Simulator、Critic 的支持，还描述教师学生、车端轨迹验证与数据反馈循环。这是类别交叉的实例：同一系统可以同时包含语言语义、世界预测和动作策略。EMMA 可以帮助理解统一文本接口，但不能替代量产 Driver 的技术说明，更不能把其论文作者表当成整个工业系统的责任名单。[Waymo 2025 技术披露](https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving/)、[Waymo 2026 技术总结](https://waymo.com/blog/2026/08/10ailessons/)

Tesla 原始演讲已保留视频入口，但本次未恢复可审计的完整逐字稿，未据此生成时间戳主张。具体骨干、动作编码、奖励设计和未公开的数据规模均保持缺项；官方议程摘要不会被当作完整技术报告。

## 验证边界与团队地图决定后续怎么读

开放环轨迹拟合、非反应式仿真、持续反馈闭环和实车测试分别回答不同问题。Rethinking the Open-Loop Evaluation 展示了仅使用自车状态的方法也能在常用开放环指标上表现良好。NAVSIM 则在起始帧调用策略后固定计划进行非反应式模拟，不能替代交互驾驶；AlpaSim 中自车反馈与背景车辆日志回放也应分别记录。SimLingo 官方榜单测试的是 BASE 版本，完整语言模型的本地闭环结果另有协议。因此报告把验证配置写在模型版本旁，避免将“有驾驶数据”误读为“有闭环驾驶证据”。[开放环评测反思](https://arxiv.org/abs/2305.10430)、[NAVSIM](https://arxiv.org/abs/2406.15349)、[SimLingo](https://arxiv.org/abs/2503.09594)、[Alpamayo-R1](https://arxiv.org/abs/2511.00088)

组织地图按署名关系而非声望排列：DriveVLM 连接清华与理想；EMMA 为 Waymo；ORION、MindDrive 连接华中科技大学与小米汽车；AutoVLA、nuReasoning 涉及 UCLA 及相应合作团队；Alpamayo-R1 的附录明确列出项目与模块贡献角色；Orion-Lite 则来自独立的 TU/e 团队，不是 ORION 原班团队。详细人员与出处见[组织人员表](organization-people.md)和[发表时身份记录](publication-identities.json)。

当前任职另行核对至 2026-09-27。例如 Zhiyu Huang 的主页已列出 2026 年 8 月赴 NC State 任助理教授，而 AutoVLA 的发表机构仍保留 UCLA；Katrin Renz 的主页记录博士毕业后加入 physical AI 初创公司，未公开公司名便不补猜。Tesla 的报告人、论文作者、公开技术负责人分别保留；Phil Duan 本人对 FSD v12/v13/v14 职责的叙述只按公开自述记录。[Zhiyu Huang](https://mczhi.github.io/)、[Katrin Renz](https://www.katrinrenz.de/)、[Phil Duan](https://www.philduan.com/)

## 下一步：阅读顺序与有判别力的实验

建议的阅读主线是 DriveVLM → EMMA → ORION → SimLingo → AutoVLA → Alpamayo-R1 → Orion-Lite → DiffusionDrive，并把 Tesla 放在系统技术栈一侧并行阅读。需要强化学习时接 MindDrive，需要低延迟时接 FlashDrive，需要训练期语言时接 DiMA 与 nuReasoning，需要判断结果可信度时先读开放环评测反思与 NAVSIM。本文仍缺少同数据同算力的跨路线实车比较，也无法还原闭源车队的数据筛选与训练配方；这些是下一步应索取的证据，而非可以从模型标签推导的事实。

后续研究最有判别力的实验，是在固定动作头与数据条件下分别加入场景文字、动作对齐语言和在线推理，同时记录闭环成功、干预、语义—动作一致性与端到端延迟。这样才能回答：语言带来的能力是否必须在车端保留，以及哪个训练接口真正值得投入。

## References

以下固定版本构成本次论文证据集合；企业与人员来源另见[补充来源记录](supplement-sources.md)。

1. Yihan Hu et al. (2022). [Planning-oriented Autonomous Driving](https://arxiv.org/abs/2212.10156v2). arXiv:2212.10156v2.

2. Jiang-Tian Zhai et al. (2023). [Rethinking the Open-Loop Evaluation of End-to-End Autonomous Driving in nuScenes](https://arxiv.org/abs/2305.10430v2). arXiv:2305.10430v2.

3. Hao Shao et al. (2023). [LMDrive: Closed-Loop End-to-End Driving with Large Language Models](https://arxiv.org/abs/2312.07488v2). arXiv:2312.07488v2.

4. Ana-Maria Marcu et al. (2023). [LingoQA: Visual Question Answering for Autonomous Driving](https://arxiv.org/abs/2312.14115v4). arXiv:2312.14115v4.

5. Chonghao Sima et al. (2023). [DriveLM: Driving with Graph Visual Question Answering](https://arxiv.org/abs/2312.14150v3). arXiv:2312.14150v3.

6. Xiaoyu Tian et al. (2024). [DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models](https://arxiv.org/abs/2402.12289v5). arXiv:2402.12289v5.

7. Daniel Dauner et al. (2024). [NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking](https://arxiv.org/abs/2406.15349v2). arXiv:2406.15349v2.

8. Jyh-Jing Hwang et al. (2024). [EMMA: End-to-End Multimodal Model for Autonomous Driving](https://arxiv.org/abs/2410.23262v3). arXiv:2410.23262v3.

9. Bencheng Liao et al. (2024). [DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving](https://arxiv.org/abs/2411.15139v3). arXiv:2411.15139v3.

10. Deepti Hegde et al. (2025). [Distilling Multi-modal Large Language Models for Autonomous Driving](https://arxiv.org/abs/2501.09757v1). arXiv:2501.09757v1.

11. Katrin Renz et al. (2025). [SimLingo: Vision-Only Closed-Loop Autonomous Driving with Language-Action Alignment](https://arxiv.org/abs/2503.09594v1). arXiv:2503.09594v1.

12. Haoyu Fu et al. (2025). [ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation](https://arxiv.org/abs/2503.19755v1). arXiv:2503.19755v1.

13. Xingcheng Zhou et al. (2025). [OpenDriveVLA: Towards End-to-end Autonomous Driving with Large Vision Language Action Model](https://arxiv.org/abs/2503.23463v2). arXiv:2503.23463v2.

14. Zewei Zhou et al. (2025). [AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning](https://arxiv.org/abs/2506.13757v3). arXiv:2506.13757v3.

15. NVIDIA et al. (2025). [Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail](https://arxiv.org/abs/2511.00088v2). arXiv:2511.00088v2.

16. Haoyu Fu et al. (2025). [MindDrive: A Vision-Language-Action Model for Autonomous Driving via Online Reinforcement Learning](https://arxiv.org/abs/2512.13636v4). arXiv:2512.13636v4.

17. Jing Gu et al. (2026). [Orion-Lite: Distilling LLM Reasoning into Efficient Vision-Only Driving Models](https://arxiv.org/abs/2604.08266v1). arXiv:2604.08266v1.

18. Nicanor Mayumu et al. (2026). [Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation in Autonomous Driving Models](https://arxiv.org/abs/2605.17268v2). arXiv:2605.17268v2.

19. Zhiyu Huang et al. (2026). [nuReasoning: A Reasoning-Centric Dataset and Benchmark for Long-Tail Autonomous Driving](https://arxiv.org/abs/2605.31572v1). arXiv:2605.31572v1.

20. Zekai Li et al. (2026). [FlashDrive: Flash Vision-Language-Action Inference for Autonomous Driving](https://arxiv.org/abs/2608.12932v1). arXiv:2608.12932v1.
