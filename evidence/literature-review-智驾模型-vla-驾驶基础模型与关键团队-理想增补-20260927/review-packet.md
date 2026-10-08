# Review Packet: 智驾模型与关键团队：VLA、驾驶基础模型及理想系列论文

## Scope

- Topic: 智驾模型与关键团队：VLA、驾驶基础模型及理想系列论文
- Time range: 2024-09-27..2026-09-27; classic antecedents allowed
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-ALIGN`, `EA-EVAL`
- Evidence events: 66
- Topic cards: 0
- Registered source IDs available: not loaded

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 66
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-AVMODEL-2026-0001`, `EA-AVMODEL-2026-0005`, `EA-AVMODEL-2026-0007`, `EA-AVMODEL-2026-0009`, `EA-AVMODEL-2026-0011`, `EA-AVMODEL-2026-0013`, `EA-AVMODEL-2026-0015`, `EA-LIAUTO-2026-0001`, `EA-AVMODEL-2026-0018`, `EA-AVMODEL-2026-0020`, `EA-AVMODEL-2026-0022`, `EA-AVMODEL-2026-0025`
- Registered sources: not loaded

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 30 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 48
- Structure mapped: 30
- Deep-read papers: 30
- Claim-verified papers: 30
- Accepted evidence papers: 30
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- No topic cards provided.

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 28 |
| `conditional` | 条件成立 | 18 |
| `limit` | 限制/负面 | 20 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2212.10156: Planning-oriented Autonomous Driving | 2022-12-20 | conditional, support | EA-AVMODEL-2026-0001; EA-AVMODEL-2026-0002 |
| 2305.10430: Rethinking the Open-Loop Evaluation of End-to-End Autonomous Driving in nuScenes | 2023-05-17 | limit | EA-AVMODEL-2026-0003; EA-AVMODEL-2026-0004 |
| 2312.07488: LMDrive: Closed-Loop End-to-End Driving with Large Language Models | 2023-12-12 | conditional, support | EA-AVMODEL-2026-0005; EA-AVMODEL-2026-0006 |
| 2312.14115: LingoQA: Visual Question Answering for Autonomous Driving | 2023-12-21 | conditional, support | EA-AVMODEL-2026-0007; EA-AVMODEL-2026-0008 |
| 2312.14150: DriveLM: Driving with Graph Visual Question Answering | 2023-12-21 | limit, support | EA-AVMODEL-2026-0009; EA-AVMODEL-2026-0010 |
| 2402.12289: DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models | 2024-02-19 | conditional, support | EA-AVMODEL-2026-0011; EA-AVMODEL-2026-0012 |
| 2406.15349: NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking | 2024-06-21 | limit, support | EA-AVMODEL-2026-0013; EA-AVMODEL-2026-0014 |
| 2410.23262: EMMA: End-to-End Multimodal Model for Autonomous Driving | 2024-10-30 | conditional, limit, support | EA-AVMODEL-2026-0015; EA-AVMODEL-2026-0016; EA-AVMODEL-2026-0017 |
| 2411.11252: DrivingSphere: Building a High-fidelity 4D World for Closed-loop Simulation | 2024-11-18 | limit, support | EA-LIAUTO-2026-0001; EA-LIAUTO-2026-0002 |
| 2411.15139: DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving | 2024-11-22 | conditional, support | EA-AVMODEL-2026-0018; EA-AVMODEL-2026-0019 |
| 2501.09757: Distilling Multi-modal Large Language Models for Autonomous Driving | 2025-01-16 | conditional, support | EA-AVMODEL-2026-0020; EA-AVMODEL-2026-0021 |
| 2503.09594: SimLingo: Vision-Only Closed-Loop Autonomous Driving with Language-Action Alignment | 2025-03-12 | conditional, limit, support | EA-AVMODEL-2026-0022; EA-AVMODEL-2026-0023; EA-AVMODEL-2026-0024 |
| 2503.19755: ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation | 2025-03-25 | conditional, limit, support | EA-AVMODEL-2026-0025; EA-AVMODEL-2026-0026; EA-AVMODEL-2026-0027 |
| 2503.23463: OpenDriveVLA: Towards End-to-end Autonomous Driving with Large Vision Language Action Model | 2025-03-30 | limit, support | EA-AVMODEL-2026-0028; EA-AVMODEL-2026-0029 |
| 2506.13757: AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fin... | 2025-06-16 | limit, support | EA-AVMODEL-2026-0030; EA-AVMODEL-2026-0031; EA-AVMODEL-2026-0032 |
| 2507.00603: World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model | 2025-07-01 | conditional, support | EA-LIAUTO-2026-0003; EA-LIAUTO-2026-0004 |
| 2509.20109: Discrete Diffusion for Reflective Vision-Language-Action Models in Autonomous Driving | 2025-09-24 | limit, support | EA-LIAUTO-2026-0005; EA-LIAUTO-2026-0006 |
| 2511.00088: Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail | 2025-10-30 | conditional, limit, support | EA-AVMODEL-2026-0033; EA-AVMODEL-2026-0034; EA-AVMODEL-2026-0035 |
| 2512.13636: MindDrive: A Vision-Language-Action Model for Autonomous Driving via Online Reinforcement Learning | 2025-12-15 | limit, support | EA-AVMODEL-2026-0036; EA-AVMODEL-2026-0037 |
| 2603.01441: Unifying Language-Action Understanding and Generation for Autonomous Driving | 2026-03-02 | conditional, support | EA-LIAUTO-2026-0007; EA-LIAUTO-2026-0008 |
| 2604.08266: Orion-Lite: Distilling LLM Reasoning into Efficient Vision-Only Driving Models | 2026-04-09 | conditional, limit, support | EA-AVMODEL-2026-0038; EA-AVMODEL-2026-0039; EA-AVMODEL-2026-0040 |
| 2605.12622: Action Emergence from Streaming Intent | 2026-05-12 | conditional, support | EA-LIAUTO-2026-0009; EA-LIAUTO-2026-0010 |
| 2605.12624: MindVLA-U1: VLA Beats VA with Unified Streaming Architecture for Autonomous Driving | 2026-05-12 | limit, support | EA-LIAUTO-2026-0011; EA-LIAUTO-2026-0012 |
| 2605.12625: Driving Intents Amplify Planning-Oriented Reinforcement Learning | 2026-05-12 | conditional, support | EA-LIAUTO-2026-0013; EA-LIAUTO-2026-0014 |
| 2605.17268: Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation in Autonomous Driving Models | 2026-05-17 | limit | EA-AVMODEL-2026-0041; EA-AVMODEL-2026-0042 |
| 2605.26113: AnyScene: Towards Highly Controllable Driving Scene Generation at Anywhere and Beyond | 2026-05-25 | limit, support | EA-LIAUTO-2026-0015; EA-LIAUTO-2026-0016 |
| 2605.31572: nuReasoning: A Reasoning-Centric Dataset and Benchmark for Long-Tail Autonomous Driving | 2026-05-29 | conditional, support | EA-AVMODEL-2026-0043; EA-AVMODEL-2026-0044 |
| 2607.01586: VLAFlow: A Unified Training Framework for Vision-Language-Action Models via Co-training and Future Latent Alignment | 2026-07-02 | conditional, support | EA-LIAUTO-2026-0017; EA-LIAUTO-2026-0018 |
| 2608.12932: FlashDrive: Flash Vision-Language-Action Inference for Autonomous Driving | 2026-08-13 | limit, support | EA-AVMODEL-2026-0045; EA-AVMODEL-2026-0046 |
| 2609.24526: ME-VLM: A Unified VLM for Embodied Cognition and Agent Coordination | 2026-09-21 | conditional, support | EA-LIAUTO-2026-0019; EA-LIAUTO-2026-0020 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-AVMODEL-2026-0001 | EA-MODEL | `support` | `direct` | UniAD 以任务 query 作为感知、预测和规划之间的可学习接口，并保留显式中间监督。 | 方法逐项给出数据流；共享表征不意味着仅靠最终动作损失训练。 (2 Methodology) | yihan-hu; jiazhi-yang; li-chen; et al. | 2212.10156 |
| EA-AVMODEL-2026-0005 | EA-MODEL | `support` | `direct` | LMDrive 将语言指令、相机和 LiDAR 特征映射为路点及指令完成标志，再由 PID 执行。 | 原文执行链明确不是语言 token 直接驱动转向执行器。 (4.2 LLM for instruction-following auto driving) | hao-shao; yuxuan-hu; letian-wang; et al. | 2312.07488 |
| EA-AVMODEL-2026-0007 | EA-MODEL | `support` | `direct` | LingoQA 的对象是驾驶视频问答，配套学习式 Lingo-Judge，而非执行驾驶动作。 | 问题、输出与评测对象均为 QA，没有控制输出证据。 (3 LingoQA Benchmark; 7 Conclusion) | ana-maria-marcu; long-chen; jan-hnermann; et al. | 2312.14115 |
| EA-AVMODEL-2026-0009 | EA-MODEL | `support` | `direct` | DriveLM 以有向 QA 图传递上下文，再将行为说明映射为离散轨迹 token。 | motion 使用独立 LoRA，不能把多阶段流程压成一次统一解码。 (3.1 Prompting with Context; 3.2 Trajectory Tokenization for Motion) | chonghao-sima; katrin-renz; kashyap-chitta; et al. | 2312.14150 |
| EA-AVMODEL-2026-0011 | EA-MODEL | `support` | `direct` | DriveVLM-Dual 将低频 VLM 轨迹交给传统规划器进行高频细化，两支异步协作。 | 该节明确给出优化式与神经规划器两种接入方式；结论只描述接口，不推断统一端到端训练。 (3.5 DriveVLM-Dual) | xiaoyu-tian; junru-gu; bailin-li; et al. | 2402.12289 |
| EA-AVMODEL-2026-0013 | EA-MODEL | `support` | `direct` | NAVSIM 仅在初始帧调用规划策略，随后固定计划进行非反应式模拟，没有环境反馈给策略。 | 协议直接排除了通常意义上的策略交互闭环。 (3 NAVSIM: Non-Reactive Autonomous Vehicle Simulation) | daniel-dauner; marcel-hallgarten; tianyu-li; et al. | 2406.15349 |
| EA-AVMODEL-2026-0015 | EA-MODEL | `support` | `direct` | EMMA 将驾驶任务的非传感器输入和输出统一为文本，允许规划、检测和路网任务联合训练。 | 方法节明确选择数值文本而非专门动作 token；多任务用途在 generalist 节得到说明。 (2 Method) | jyh-jing-hwang; runsheng-xu; hubert-lin; et al. | 2410.23262 |
| EA-LIAUTO-2026-0001 | EA-MODEL | `support` | `direct` | DrivingSphere 把可控占据、视觉渲染与交通主体状态更新接成仿真闭环，区别于只生成固定视频。 | 明确由环境代理和自车控制反馈更新位置，再生成观测。 (3.3) | tianyi-yan; dongming-wu; wencheng-han; et al. | 2411.11252 |
| EA-AVMODEL-2026-0018 | EA-MODEL | `support` | `direct` | DiffusionDrive 从带噪轨迹锚点出发进行截断去噪，并以学习置信度选择最终轨迹。 | 无需语言或视频未来生成即可学习多模式驾驶动作，构成非语言主线对照。 (3.3 Truncated Diffusion; 3.4 Architecture) | bencheng-liao; shaoyu-chen; haoran-yin; et al. | 2411.15139 |
| EA-AVMODEL-2026-0020 | EA-MODEL | `support` | `direct` | DiMA 通过共享场景编码器、辅助任务和特征蒸馏训练视觉规划器，默认推理无需 LLM。 | 主方法与结果均明确无 LLM 推理；Dual 是另一个可选配置。 (3.1 Vision-based Planner; 5 Experimental Results) | deepti-hegde; rajeev-yasarla; hong-cai; et al. | 2501.09757 |
| EA-AVMODEL-2026-0022 | EA-MODEL | `support` | `direct` | SimLingo 用同一视觉场景的多种指令—轨迹配对，迫使模型学习语言对动作的影响。 | Action Dreaming 部分解释了普通专家轨迹可由视觉猜出、从而忽略语言的混淆；多分支数据针对该问题。 (3.2 Datasets) | katrin-renz; long-chen; elahe-arani; et al. | 2503.09594 |
| EA-AVMODEL-2026-0025 | EA-MODEL | `support` | `direct` | ORION 用 LLM 的 planning token 条件化 VAE 轨迹分布，并以 GRU 解码轨迹。 | 原文明确 VAE 负责 reasoning/action 分布对齐，GRU 借鉴 GenAD；不是纯文本坐标生成。 (3.3 Generative Planner) | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | 2503.19755 |
| EA-AVMODEL-2026-0028 | EA-MODEL | `support` | `direct` | OpenDriveVLA 将 scene、agent、map 三类结构化视觉 token 对齐到语言空间，并联合优化轨迹生成。 | 阶段一明确对三类 token 设独立 projector，后续阶段三联合训练；不能仅称通用图文 VLM。 (III-B Stage 1 - Hierarchical Vision-Language Alignment) | xingcheng-zhou; xuyuan-han; feng-yang; et al. | 2503.23463 |
| EA-AVMODEL-2026-0030 | EA-MODEL | `support` | `direct` | AutoVLA 将驾驶运动码本扩展进 VLM 词表，以统一自回归过程生成推理和动作。 | 框架节给出 K-disk 码本和扩展 token 的机制；区别于文本数值及外接连续解码头。 (3.1 Framework) | zewei-zhou; tianhui-cai; seth-z-zhao; et al. | 2506.13757 |
| EA-LIAUTO-2026-0003 | EA-MODEL | `support` | `direct` | World4Drive 用动作条件未来潜变量及学习式选择器评价多模式轨迹；测试期不访问真实未来 latent。 | 已核对训练期监督与推理期 ScoreNet 分工，避免把未来真值误当部署输入。 (3.3.2) | yupeng-zheng; pengxuan-yang; zebin-xing; et al. | 2507.00603 |
| EA-LIAUTO-2026-0005 | EA-MODEL | `support` | `direct` | ReflectDrive 的反思由外部安全评分、本地搜索和离散扩散修补实现，不是自然语言反思文本。 | 原文定义安全判据并在坐标空间查找可行点，再由生成器补全轨迹。 (4.2) | pengxiang-li; yinan-zheng; yue-wang; et al. | 2509.20109 |
| EA-AVMODEL-2026-0033 | EA-MODEL | `support` | `direct` | Alpamayo-R1 在训练时使用离散动作 token，但推理轨迹由连续 flow-matching 动作专家解码。 | 方法节明确区分训练和推理的动作表示，不能将其描述为纯自回归坐标输出。 (5.1 Action Modality Injection) | nvidia; yan-wang; wenjie-luo; et al. | 2511.00088 |
| EA-AVMODEL-2026-0036 | EA-MODEL | `support` | `direct` | MindDrive 先学语言 meta-action 到轨迹的映射，再用 CARLA 交互回报及 PPO 优化决策专家。 | 方法及算法明确回报来自实际 simulator rollout，优化的是决策分支和价值网络。 (3.2 Language-Action Mapping; 3.3 Online RL for Action-Reasoning) | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | 2512.13636 |
| EA-LIAUTO-2026-0007 | EA-MODEL | `support` | `direct` | LinkVLA 增加动作到语言的理解目标，并用终点引导的粗到细动作生成连接语言与规划。 | 反向理解提供对齐监督，但不能仅凭可读说明认定推理忠实。 (1 Introduction; 3.2; 3.3) | xinyang-wang; qian-liu; wenjie-ding; et al. | 2603.01441 |
| EA-AVMODEL-2026-0038 | EA-MODEL | `support` | `direct` | Orion-Lite 在推理时移除文本提示和大型 LLM，以轻量 transformer 模仿教师的 planning-token 表征。 | 原文明确学生删除文本提示、替换 LLM；仍继承教师视觉与时间模块。 (3.2 State Embedding Extraction; 3.3 Lightweight Distillation Module) | jing-gu; niccol-cavagnero; gijs-dubbelman | 2604.08266 |
| EA-LIAUTO-2026-0009 | EA-MODEL | `support` | `direct` | Streaming Intent 将语言推理解析为有限意图类别，再以意图条件控制连续动作生成。 | 离散语义桥接与连续动作头承担不同职责，不等同全动作词元化。 (2.1) | pengfei-jing; victor-shea-jay-huang; hengtong-lu; et al. | 2605.12622 |
| EA-LIAUTO-2026-0011 | EA-MODEL | `support` | `direct` | MindVLA-U1 以共享 Transformer 和独立轻量输出头联合学习语言与连续动作，主实验的语言监督限于基础 VQA 和官方意图标签。 | 已逐项核对 token 路径和训练数据声明；并未把项目完整数据工具等同主实验。 (2.1; 3.1) | yuzhou-huang; benjin-zhu; hengtong-lu; et al. | 2605.12624 |
| EA-LIAUTO-2026-0013 | EA-MODEL | `support` | `direct` | DIAL 明确继承 MindVLA-U1，先通过意图形成候选模式，再在同场景的跨意图采样组内进行强化学习。 | 这是原文声明的实现继承，可画实线；无需推断同公司其他论文的权重继承。 (3 Method) | hengtong-lu; victor-shea-jay-huang; chengmin-yang; et al. | 2605.12625 |
| EA-LIAUTO-2026-0015 | EA-MODEL | `support` | `direct` | AnyScene 将占据几何作为可控视频生成的中间约束，目标是扩展驾驶场景与传感器视角。 | 方法链连接布局、占据和视频；不把图像逼真度等同物理交互真实性。 (Abstract; 3 Method) | haiming-zhang; junfei-zhou; feng-jiang; et al. | 2605.26113 |
| EA-AVMODEL-2026-0043 | EA-MODEL | `support` | `direct` | nuReasoning 的 nuVLA 在推理时关闭显式文字推理，训练期加入推理监督仍改善其开放环规划。 | 消融明确区分训练监督与推理输出，为语言参与阶段提供直接证据。 (5.3 Results on Planning Benchmark) | zhiyu-huang; johnson-liu; rui-song; et al. | 2605.31572 |
| EA-LIAUTO-2026-0018 | EA-MODEL | `support` | `direct` | VLAFlow 的语言目标主要作用于预训练，不能据此断言驾驶推理时必须生成语言。 | 训练与推理分工直接支持这一区分；智驾迁移仍是待验证假设。 (1 Introduction; 3.4) | guoyang-xia; fengfa-li; hongjin-ji; et al. | 2607.01586 |
| EA-AVMODEL-2026-0045 | EA-MODEL | `support` | `direct` | FlashDrive 分别处理视觉重复编码、KV 预填充、串行推理和迭代动作解码四类延迟。 | 这是对 Alpamayo1.5 的明确工程继承，而非新驾驶策略从零训练。 (3 Method) | zekai-li; yihao-liang; hongfei-zhang; et al. | 2608.12932 |
| EA-LIAUTO-2026-0019 | EA-MODEL | `support` | `direct` | ME-VLM 将具身与代理专家蒸馏到一个部署学生，推理期不是两个教师的集成。 | 训练组织与车端运行模块分开，避免把教师计算量当推理开销。 (4.3) | foundation-model; li-auto-inc | 2609.24526 |
| EA-AVMODEL-2026-0002 | EA-MODEL | `conditional` | `direct` | UniAD 预测轨迹后，在推理时使用占据地图执行额外避碰优化。 | 原文区分可学习路点与推理优化，因此不能称像素直接到执行器的单一网络。 (2.4 Planning) | yihan-hu; jiazhi-yang; li-chen; et al. | 2212.10156 |
| EA-AVMODEL-2026-0006 | EA-MODEL | `conditional` | `direct` | LMDrive 的连续多句指令比单句指令更困难，实验中的驾驶分数与路线完成率下降。 | 结论限制到 LangAuto-Sequential 的组合指令设置。 (6.2 Quantitative Results) | hao-shao; yuxuan-hu; letian-wang; et al. | 2312.07488 |
| EA-AVMODEL-2026-0008 | EA-MODEL | `conditional` | `direct` | LingoQA 研究发现多帧上下文有助区分动态交通、信号灯变化等单帧易错情形。 | 人工与模型帧数分析支持视频理解必要性；不推断闭环驾驶效果。 (5.2 Evaluation of SOTA Vision-Language Models) | ana-maria-marcu; long-chen; jan-hnermann; et al. | 2312.14115 |
| EA-AVMODEL-2026-0012 | EA-MODEL | `conditional` | `direct` | 论文报告双 OrinX 的车载部署；VLM 与高频驾驶系统在不同处理器运行。 | 部署节明确说明处理器分工和实车演示；不将演示当作无监督运营证明。 (6 Onboard Deployment and Testing) | xiaoyu-tian; junru-gu; bailin-li; et al. | 2402.12289 |
| EA-AVMODEL-2026-0016 | EA-MODEL | `conditional` | `direct` | EMMA 的内部数据消融中，场景描述对规划表现影响中性，而元决策和关键物体识别带来改善。 | 同一 CoT 消融直接比较组成部分；不泛化为所有语言描述均无效。 (3.3 End-to-End Motion Planning with Chain-of-Thought Reasoning on Internal Dataset) | jyh-jing-hwang; runsheng-xu; hubert-lin; et al. | 2410.23262 |
| EA-AVMODEL-2026-0019 | EA-MODEL | `conditional` | `direct` | DiffusionDrive 的主 NAVSIM 设置采用前向相机与栅格 LiDAR；nuScenes 实验采用另一骨干配置。 | 不同实验的骨干与传感输入不能混成统一模型规格。 (4.2 Implementation Detail; 4.7 Quantitative Comparison on nuScenes dataset) | bencheng-liao; shaoyu-chen; haoran-yin; et al. | 2411.15139 |
| EA-AVMODEL-2026-0021 | EA-MODEL | `conditional` | `direct` | DiMA 中仅把 VQA 和规划损失加到 BEV 特征上的朴素联合训练，收益并不一致。 | 作者逐步消融显示结构化 token、蒸馏和辅助任务的重要性，不可把效果全归于加入语言。 (5.1 Ablation study.) | deepti-hegde; rajeev-yasarla; hong-cai; et al. | 2501.09757 |
| EA-AVMODEL-2026-0024 | EA-MODEL | `conditional` | `direct` | 官方 CARLA Leaderboard 仅测试 SimLingo-BASE；完整 SimLingo 的闭环驾驶在本地 Bench2Drive 检验。 | 原文说明 leaderboard 关闭造成的提交差异，避免把 BASE 的无语言成绩标成 VLA 实证。 (4.2 Implementation Details) | katrin-renz; long-chen; elahe-arani; et al. | 2503.09594 |
| EA-AVMODEL-2026-0026 | EA-MODEL | `conditional` | `direct` | 在 ORION 的受控动作输出消融中，纯文本轨迹表现最弱；生成式轨迹接口优于相同骨干的 MLP 解码。 | 仅描述同一实验内的接口比较；不据此判定所有双系统或扩散方法失败。 (4.5 Ablation Study) | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | 2503.19755 |
| EA-LIAUTO-2026-0004 | EA-MODEL | `conditional` | `direct` | World4Drive 的意图不是语言推理，而是轨迹词表聚类；它仍使用专家轨迹监督。 | 这构成与 Streaming Intent 的方法相似点及实质差异，而非同一个意图接口。 (3.2.1; 3.4) | yupeng-zheng; pengxuan-yang; zebin-xing; et al. | 2507.00603 |
| EA-AVMODEL-2026-0035 | EA-MODEL | `conditional` | `direct` | AlpaSim 闭环中自车重新渲染并执行控制，其他交通参与者沿日志轨迹回放。 | 评测协议明示背景交通非反应式；该闭环有自车反馈但不是所有参与者可互动。 (6.1 Evaluation Protocol) | nvidia; yan-wang; wenjie-luo; et al. | 2511.00088 |
| EA-LIAUTO-2026-0008 | EA-MODEL | `conditional` | `direct` | LinkVLA 的驾驶实验含 Bench2Drive 仿真闭环；其时延报告必须区分轨迹阶段与文字推理。 | 已核对实验和速度定义；保留排除 CoT 的计算边界。 (4.1; 4.3) | xinyang-wang; qian-liu; wenjie-ding; et al. | 2603.01441 |
| EA-AVMODEL-2026-0039 | EA-MODEL | `conditional` | `direct` | 在 Bench2Drive 消融中，特征蒸馏与真值轨迹监督结合优于任一单独信号。 | 该节报告三种训练配置；结论限制在同教师、冻结视觉模块和该闭环基准。 (5.2 Ablation Study) | jing-gu; niccol-cavagnero; gijs-dubbelman | 2604.08266 |
| EA-LIAUTO-2026-0010 | EA-MODEL | `conditional` | `direct` | 推理标注教师使用过去和未来视频；这一标签生成条件不代表推理期车辆可以访问未来。 | 明确区分离线标注特权信息和在线模型观测，保留事后解释偏差风险。 (2.3) | pengfei-jing; victor-shea-jay-huang; hengtong-lu; et al. | 2605.12622 |
| EA-LIAUTO-2026-0014 | EA-MODEL | `conditional` | `direct` | DIAL 的强化学习比较使用小规模重新划分的 RFS 验证序列，论文报告不能当作独立实车测试。 | 结合完整切分与检查点选择说明审查结论范围，而非只取提升数字。 (4.1) | hengtong-lu; victor-shea-jay-huang; chengmin-yang; et al. | 2605.12625 |
| EA-AVMODEL-2026-0044 | EA-MODEL | `conditional` | `direct` | nuReasoning 先自动产生推理标注，再经人工检查和纠错；其验证仍以开放环为限。 | 数据质量流程和驾驶验证层级是不同维度，不能用人工审核推导实车安全。 (3.3 Reasoning Annotation; 6 Conclusions) | zhiyu-huang; johnson-liu; rui-song; et al. | 2605.31572 |
| EA-LIAUTO-2026-0017 | EA-MODEL | `conditional` | `direct` | VLAFlow 通过受控训练范式比较研究语言与未来表征对动作迁移的作用，正文验证对象为机器人任务。 | 动作单目标在部分迁移设置出现退化；不泛化为所有动作预训练无效。 (1 Introduction; 4.2) | guoyang-xia; fengfa-li; hongjin-ji; et al. | 2607.01586 |
| EA-LIAUTO-2026-0020 | EA-MODEL | `conditional` | `direct` | ME-VLM 的驾驶评测针对理解与问答；部署段的 W4A8 和预填充性能不证明完整驾驶策略闭环。 | 结合任务与输出定义限定结论，驾驶能力范围不由标题 foundation model 自动扩大。 (5; 6.3.1) | foundation-model; li-auto-inc | 2609.24526 |
| EA-AVMODEL-2026-0003 | EA-MODEL | `limit` | `direct` | 无视觉 AD-MLP 在 nuScenes 开放环能取得有竞争力的轨迹结果，暴露指标与真实驾驶能力的落差。 | 方法、结果和限制共同构成反证，不能将其当作量产方案。 (3.3 Main Results; 5 Conclusion and Limitations) | jiang-tian-zhai; ze-feng; jinhao-du; et al. | 2305.10430 |
| EA-AVMODEL-2026-0004 | EA-MODEL | `limit` | `direct` | 占据栅格离散化会使真实记录轨迹被误判碰撞，栅格尺寸影响结果。 | 该节比较不同栅格尺寸和实例，限定为所研究的碰撞指标实现。 (4.2 Collision in Ground Truth) | jiang-tian-zhai; ze-feng; jinhao-du; et al. | 2305.10430 |
| EA-AVMODEL-2026-0010 | EA-MODEL | `limit` | `direct` | DriveLM-Agent 的论文规划验证仍为开放环；作者将闭环列为后续方向。 | CARLA QA 数据与实际策略闭环验证是不同证据。 (6 Discussion) | chonghao-sima; katrin-renz; kashyap-chitta; et al. | 2312.14150 |
| EA-AVMODEL-2026-0014 | EA-MODEL | `limit` | `direct` | NAVSIM 作者指出，高 PDMS 并不总对应高闭环分数，建议配合 CARLA 等闭环评测。 | 作者限制节明确承认非反应性、错误累积和交通规则覆盖的不足。 (5 Discussion) | daniel-dauner; marcel-hallgarten; tianyu-li; et al. | 2406.15349 |
| EA-AVMODEL-2026-0017 | EA-MODEL | `limit` | `direct` | 作者明确指出，人可读的辅助输出和驾驶动作并不保证始终一致。 | 限制节直接否认输出一致性的保证，不能用解释流畅度替代动作忠实性。 (A.5 Limitations, Risks, and Mitigations) | jyh-jing-hwang; runsheng-xu; hubert-lin; et al. | 2410.23262 |
| EA-LIAUTO-2026-0002 | EA-MODEL | `limit` | `direct` | DrivingSphere 报告的 UniAD 交互仿真路线完成度仍低；逼真度提升不等于策略可靠或已完成实车迁移。 | 该数字只对应文中模拟路线与所测策略，不作跨仿真排行榜。 (4.4) | tianyi-yan; dongming-wu; wencheng-han; et al. | 2411.11252 |
| EA-AVMODEL-2026-0023 | EA-MODEL | `limit` | `direct` | SimLingo 的消融未观察到未对齐语言任务对驾驶的明确正负影响；CoT 的驾驶收益也未达统计显著。 | 结果节与限制节共同限定增益归因：语言任务成绩不能自动证明驾驶增强。 (5 Conclusion and Limitations; 4.3 Results) | katrin-renz; long-chen; elahe-arani; et al. | 2503.09594 |
| EA-AVMODEL-2026-0027 | EA-MODEL | `limit` | `direct` | ORION 作者将大 VLM 的计算复杂度列为实时驾驶部署限制。 | 结论直接承认实时部署问题，不能把仿真闭环分数等同车端可部署性。 (5 Conclusion) | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | 2503.19755 |
| EA-AVMODEL-2026-0029 | EA-MODEL | `limit` | `direct` | OpenDriveVLA 当前规划评测仅为开放环，作者警告这可能高估鲁棒性。 | 原文承认未捕捉交互反馈，问答与离线轨迹成绩不足以证明真实闭环能力。 (VIII-D 2 Current Limitations) | xingcheng-zhou; xuyuan-han; feng-yang; et al. | 2503.23463 |
| EA-AVMODEL-2026-0031 | EA-MODEL | `limit` | `direct` | AutoVLA 的 NAVSIM best-of-N 结果依赖 oracle 选择，必须与可直接部署的单次预测分开。 | 结果节明确说明六个候选的选择方式；这是评测可用信息差异，不是一般部署能力。 (4.2 Main Results) | zewei-zhou; tianhui-cai; seth-z-zhao; et al. | 2506.13757 |
| EA-AVMODEL-2026-0032 | EA-MODEL | `limit` | `direct` | AutoVLA 作者仍将 GPU 依赖、显存和计算成本列为实时应用限制。 | 结论说明近实时与实用车端部署仍有差距，不把模型规模直接当部署证明。 (5 Conclusions) | zewei-zhou; tianhui-cai; seth-z-zhao; et al. | 2506.13757 |
| EA-LIAUTO-2026-0006 | EA-MODEL | `limit` | `direct` | ReflectDrive 单列使用真实未来主体轨迹评分的版本；其结果必须与恒速近似版本区分。 | 特权环境信息会改变安全评分能力，不能并入相同部署输入的横向排名。 (5.1) | pengxiang-li; yinan-zheng; yue-wang; et al. | 2509.20109 |
| EA-AVMODEL-2026-0034 | EA-MODEL | `limit` | `direct` | 仅优化推理评分时，Alpamayo-R1 的 ADE 和推理—动作一致性会退化；联合一致性奖励改善这种取舍。 | 奖励消融明确报告反向变化，说明高语言评分本身不足以确保动作改善。 (6.3 Improvements of Reasoning, Consistency, and Safety via RL Post-Training) | nvidia; yan-wang; wenjie-luo; et al. | 2511.00088 |
| EA-AVMODEL-2026-0037 | EA-MODEL | `limit` | `direct` | MindDrive 在线 RL 的训练轮数与闭环性能并非单调关系，过多更新会降低表现。 | 消融直接观察退化；作者用灾难性遗忘解释，但该机制解释本身仍是推断。 (4.3 Ablation Studies) | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | 2512.13636 |
| EA-AVMODEL-2026-0040 | EA-MODEL | `limit` | `direct` | 移除 LLM 后，Orion-Lite 的主要推理瓶颈转移到重型视觉编码器。 | 限制节明确指出瓶颈迁移，模块加速不能等同整个系统同比加速。 (6 Limitations and Future Work) | jing-gu; niccol-cavagnero; gijs-dubbelman | 2604.08266 |
| EA-LIAUTO-2026-0012 | EA-MODEL | `limit` | `direct` | MindVLA-U1 的规划、GRPO 和人类偏好结论仅在日志开放环成立，尚不支持反应式闭环或实车安全结论。 | 作者明确限定 WOD-E2E 和 RFS；训练反馈并非在线交通交互。 (5.2 Limitations) | yuzhou-huang; benjin-zhu; hengtong-lu; et al. | 2605.12624 |
| EA-AVMODEL-2026-0041 | EA-MODEL | `limit` | `direct` | 该审计发现 Alpamayo-R1 样本中存在声明减速或停车而轨迹继续的说明—动作不一致。 | 只采纳实验观察，不将它当作所有 VLA 或量产系统的失败率。 (5.3 Reasoning-Action Consistency (Phase 2B)) | nicanor-mayumu; xiaoheng-deng; patrick-mukala | 2605.17268 |
| EA-AVMODEL-2026-0042 | EA-MODEL | `limit` | `direct` | 该审计使用确定性关键词抽取，作者承认它会漏掉同义表达。 | 方法局限使其精确百分比不宜脱离阈值和标注协议使用。 (7.1 Model and Dataset) | nicanor-mayumu; xiaoheng-deng; patrick-mukala | 2605.17268 |
| EA-LIAUTO-2026-0016 | EA-MODEL | `limit` | `direct` | AnyScene 明确不建模交通流或反应式主体，其生成代理受固定 BEV 布局控制。 | 这是排除完整交互世界模型结论的直接依据。 (5 Conclusion and Future Work) | haiming-zhang; junfei-zhou; feng-jiang; et al. | 2605.26113 |
| EA-AVMODEL-2026-0046 | EA-MODEL | `limit` | `direct` | FlashDrive 的 AlpaSim 评测并非所有指标均改善，其中 Wrong Lane 退化。 | 作者结果包含退化指标，因此只能说特定设置保留总体质量，不能宣布安全无损。 (4.4 Closed-loop Evaluation) | zekai-li; yihao-liang; hongfei-zhang; et al. | 2608.12932 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-AVMODEL-2026-0001 | yihan-hu; jiazhi-yang; li-chen; et al. | unlisted | `support` | UniAD 以任务 query 作为感知、预测和规划之间的可学习接口，并保留显式中间监督。 |
| EA-AVMODEL-2026-0005 | hao-shao; yuxuan-hu; letian-wang; et al. | unlisted | `support` | LMDrive 将语言指令、相机和 LiDAR 特征映射为路点及指令完成标志，再由 PID 执行。 |
| EA-AVMODEL-2026-0007 | ana-maria-marcu; long-chen; jan-hnermann; et al. | unlisted | `support` | LingoQA 的对象是驾驶视频问答，配套学习式 Lingo-Judge，而非执行驾驶动作。 |
| EA-AVMODEL-2026-0009 | chonghao-sima; katrin-renz; kashyap-chitta; et al. | unlisted | `support` | DriveLM 以有向 QA 图传递上下文，再将行为说明映射为离散轨迹 token。 |
| EA-AVMODEL-2026-0011 | xiaoyu-tian; junru-gu; bailin-li; et al. | unlisted | `support` | DriveVLM-Dual 将低频 VLM 轨迹交给传统规划器进行高频细化，两支异步协作。 |
| EA-AVMODEL-2026-0013 | daniel-dauner; marcel-hallgarten; tianyu-li; et al. | unlisted | `support` | NAVSIM 仅在初始帧调用规划策略，随后固定计划进行非反应式模拟，没有环境反馈给策略。 |
| EA-AVMODEL-2026-0015 | jyh-jing-hwang; runsheng-xu; hubert-lin; et al. | unlisted | `support` | EMMA 将驾驶任务的非传感器输入和输出统一为文本，允许规划、检测和路网任务联合训练。 |
| EA-LIAUTO-2026-0001 | tianyi-yan; dongming-wu; wencheng-han; et al. | unlisted | `support` | DrivingSphere 把可控占据、视觉渲染与交通主体状态更新接成仿真闭环，区别于只生成固定视频。 |
| EA-AVMODEL-2026-0018 | bencheng-liao; shaoyu-chen; haoran-yin; et al. | unlisted | `support` | DiffusionDrive 从带噪轨迹锚点出发进行截断去噪，并以学习置信度选择最终轨迹。 |
| EA-AVMODEL-2026-0020 | deepti-hegde; rajeev-yasarla; hong-cai; et al. | unlisted | `support` | DiMA 通过共享场景编码器、辅助任务和特征蒸馏训练视觉规划器，默认推理无需 LLM。 |
| EA-AVMODEL-2026-0022 | katrin-renz; long-chen; elahe-arani; et al. | unlisted | `support` | SimLingo 用同一视觉场景的多种指令—轨迹配对，迫使模型学习语言对动作的影响。 |
| EA-AVMODEL-2026-0025 | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | unlisted | `support` | ORION 用 LLM 的 planning token 条件化 VAE 轨迹分布，并以 GRU 解码轨迹。 |
| EA-AVMODEL-2026-0028 | xingcheng-zhou; xuyuan-han; feng-yang; et al. | unlisted | `support` | OpenDriveVLA 将 scene、agent、map 三类结构化视觉 token 对齐到语言空间，并联合优化轨迹生成。 |
| EA-AVMODEL-2026-0030 | zewei-zhou; tianhui-cai; seth-z-zhao; et al. | unlisted | `support` | AutoVLA 将驾驶运动码本扩展进 VLM 词表，以统一自回归过程生成推理和动作。 |
| EA-LIAUTO-2026-0003 | yupeng-zheng; pengxuan-yang; zebin-xing; et al. | unlisted | `support` | World4Drive 用动作条件未来潜变量及学习式选择器评价多模式轨迹；测试期不访问真实未来 latent。 |
| EA-LIAUTO-2026-0005 | pengxiang-li; yinan-zheng; yue-wang; et al. | unlisted | `support` | ReflectDrive 的反思由外部安全评分、本地搜索和离散扩散修补实现，不是自然语言反思文本。 |
| EA-AVMODEL-2026-0033 | nvidia; yan-wang; wenjie-luo; et al. | unlisted | `support` | Alpamayo-R1 在训练时使用离散动作 token，但推理轨迹由连续 flow-matching 动作专家解码。 |
| EA-AVMODEL-2026-0036 | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | unlisted | `support` | MindDrive 先学语言 meta-action 到轨迹的映射，再用 CARLA 交互回报及 PPO 优化决策专家。 |
| EA-LIAUTO-2026-0007 | xinyang-wang; qian-liu; wenjie-ding; et al. | unlisted | `support` | LinkVLA 增加动作到语言的理解目标，并用终点引导的粗到细动作生成连接语言与规划。 |
| EA-AVMODEL-2026-0038 | jing-gu; niccol-cavagnero; gijs-dubbelman | unlisted | `support` | Orion-Lite 在推理时移除文本提示和大型 LLM，以轻量 transformer 模仿教师的 planning-token 表征。 |
| EA-LIAUTO-2026-0009 | pengfei-jing; victor-shea-jay-huang; hengtong-lu; et al. | unlisted | `support` | Streaming Intent 将语言推理解析为有限意图类别，再以意图条件控制连续动作生成。 |
| EA-LIAUTO-2026-0011 | yuzhou-huang; benjin-zhu; hengtong-lu; et al. | unlisted | `support` | MindVLA-U1 以共享 Transformer 和独立轻量输出头联合学习语言与连续动作，主实验的语言监督限于基础 VQA 和官方意图标签。 |
| EA-LIAUTO-2026-0013 | hengtong-lu; victor-shea-jay-huang; chengmin-yang; et al. | unlisted | `support` | DIAL 明确继承 MindVLA-U1，先通过意图形成候选模式，再在同场景的跨意图采样组内进行强化学习。 |
| EA-LIAUTO-2026-0015 | haiming-zhang; junfei-zhou; feng-jiang; et al. | unlisted | `support` | AnyScene 将占据几何作为可控视频生成的中间约束，目标是扩展驾驶场景与传感器视角。 |
| EA-AVMODEL-2026-0043 | zhiyu-huang; johnson-liu; rui-song; et al. | unlisted | `support` | nuReasoning 的 nuVLA 在推理时关闭显式文字推理，训练期加入推理监督仍改善其开放环规划。 |
| EA-LIAUTO-2026-0018 | guoyang-xia; fengfa-li; hongjin-ji; et al. | unlisted | `support` | VLAFlow 的语言目标主要作用于预训练，不能据此断言驾驶推理时必须生成语言。 |
| EA-AVMODEL-2026-0045 | zekai-li; yihao-liang; hongfei-zhang; et al. | unlisted | `support` | FlashDrive 分别处理视觉重复编码、KV 预填充、串行推理和迭代动作解码四类延迟。 |
| EA-LIAUTO-2026-0019 | foundation-model; li-auto-inc | unlisted | `support` | ME-VLM 将具身与代理专家蒸馏到一个部署学生，推理期不是两个教师的集成。 |
| EA-AVMODEL-2026-0002 | yihan-hu; jiazhi-yang; li-chen; et al. | unlisted | `conditional` | UniAD 预测轨迹后，在推理时使用占据地图执行额外避碰优化。 |
| EA-AVMODEL-2026-0006 | hao-shao; yuxuan-hu; letian-wang; et al. | unlisted | `conditional` | LMDrive 的连续多句指令比单句指令更困难，实验中的驾驶分数与路线完成率下降。 |
| EA-AVMODEL-2026-0008 | ana-maria-marcu; long-chen; jan-hnermann; et al. | unlisted | `conditional` | LingoQA 研究发现多帧上下文有助区分动态交通、信号灯变化等单帧易错情形。 |
| EA-AVMODEL-2026-0012 | xiaoyu-tian; junru-gu; bailin-li; et al. | unlisted | `conditional` | 论文报告双 OrinX 的车载部署；VLM 与高频驾驶系统在不同处理器运行。 |
| EA-AVMODEL-2026-0016 | jyh-jing-hwang; runsheng-xu; hubert-lin; et al. | unlisted | `conditional` | EMMA 的内部数据消融中，场景描述对规划表现影响中性，而元决策和关键物体识别带来改善。 |
| EA-AVMODEL-2026-0019 | bencheng-liao; shaoyu-chen; haoran-yin; et al. | unlisted | `conditional` | DiffusionDrive 的主 NAVSIM 设置采用前向相机与栅格 LiDAR；nuScenes 实验采用另一骨干配置。 |
| EA-AVMODEL-2026-0021 | deepti-hegde; rajeev-yasarla; hong-cai; et al. | unlisted | `conditional` | DiMA 中仅把 VQA 和规划损失加到 BEV 特征上的朴素联合训练，收益并不一致。 |
| EA-AVMODEL-2026-0024 | katrin-renz; long-chen; elahe-arani; et al. | unlisted | `conditional` | 官方 CARLA Leaderboard 仅测试 SimLingo-BASE；完整 SimLingo 的闭环驾驶在本地 Bench2Drive 检验。 |
| EA-AVMODEL-2026-0026 | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | unlisted | `conditional` | 在 ORION 的受控动作输出消融中，纯文本轨迹表现最弱；生成式轨迹接口优于相同骨干的 MLP 解码。 |
| EA-LIAUTO-2026-0004 | yupeng-zheng; pengxuan-yang; zebin-xing; et al. | unlisted | `conditional` | World4Drive 的意图不是语言推理，而是轨迹词表聚类；它仍使用专家轨迹监督。 |
| EA-AVMODEL-2026-0035 | nvidia; yan-wang; wenjie-luo; et al. | unlisted | `conditional` | AlpaSim 闭环中自车重新渲染并执行控制，其他交通参与者沿日志轨迹回放。 |
| EA-LIAUTO-2026-0008 | xinyang-wang; qian-liu; wenjie-ding; et al. | unlisted | `conditional` | LinkVLA 的驾驶实验含 Bench2Drive 仿真闭环；其时延报告必须区分轨迹阶段与文字推理。 |
| EA-AVMODEL-2026-0039 | jing-gu; niccol-cavagnero; gijs-dubbelman | unlisted | `conditional` | 在 Bench2Drive 消融中，特征蒸馏与真值轨迹监督结合优于任一单独信号。 |
| EA-LIAUTO-2026-0010 | pengfei-jing; victor-shea-jay-huang; hengtong-lu; et al. | unlisted | `conditional` | 推理标注教师使用过去和未来视频；这一标签生成条件不代表推理期车辆可以访问未来。 |
| EA-LIAUTO-2026-0014 | hengtong-lu; victor-shea-jay-huang; chengmin-yang; et al. | unlisted | `conditional` | DIAL 的强化学习比较使用小规模重新划分的 RFS 验证序列，论文报告不能当作独立实车测试。 |
| EA-AVMODEL-2026-0044 | zhiyu-huang; johnson-liu; rui-song; et al. | unlisted | `conditional` | nuReasoning 先自动产生推理标注，再经人工检查和纠错；其验证仍以开放环为限。 |
| EA-LIAUTO-2026-0017 | guoyang-xia; fengfa-li; hongjin-ji; et al. | unlisted | `conditional` | VLAFlow 通过受控训练范式比较研究语言与未来表征对动作迁移的作用，正文验证对象为机器人任务。 |
| EA-LIAUTO-2026-0020 | foundation-model; li-auto-inc | unlisted | `conditional` | ME-VLM 的驾驶评测针对理解与问答；部署段的 W4A8 和预填充性能不证明完整驾驶策略闭环。 |
| EA-AVMODEL-2026-0003 | jiang-tian-zhai; ze-feng; jinhao-du; et al. | unlisted | `limit` | 无视觉 AD-MLP 在 nuScenes 开放环能取得有竞争力的轨迹结果，暴露指标与真实驾驶能力的落差。 |
| EA-AVMODEL-2026-0004 | jiang-tian-zhai; ze-feng; jinhao-du; et al. | unlisted | `limit` | 占据栅格离散化会使真实记录轨迹被误判碰撞，栅格尺寸影响结果。 |
| EA-AVMODEL-2026-0010 | chonghao-sima; katrin-renz; kashyap-chitta; et al. | unlisted | `limit` | DriveLM-Agent 的论文规划验证仍为开放环；作者将闭环列为后续方向。 |
| EA-AVMODEL-2026-0014 | daniel-dauner; marcel-hallgarten; tianyu-li; et al. | unlisted | `limit` | NAVSIM 作者指出，高 PDMS 并不总对应高闭环分数，建议配合 CARLA 等闭环评测。 |
| EA-AVMODEL-2026-0017 | jyh-jing-hwang; runsheng-xu; hubert-lin; et al. | unlisted | `limit` | 作者明确指出，人可读的辅助输出和驾驶动作并不保证始终一致。 |
| EA-LIAUTO-2026-0002 | tianyi-yan; dongming-wu; wencheng-han; et al. | unlisted | `limit` | DrivingSphere 报告的 UniAD 交互仿真路线完成度仍低；逼真度提升不等于策略可靠或已完成实车迁移。 |
| EA-AVMODEL-2026-0023 | katrin-renz; long-chen; elahe-arani; et al. | unlisted | `limit` | SimLingo 的消融未观察到未对齐语言任务对驾驶的明确正负影响；CoT 的驾驶收益也未达统计显著。 |
| EA-AVMODEL-2026-0027 | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | unlisted | `limit` | ORION 作者将大 VLM 的计算复杂度列为实时驾驶部署限制。 |
| EA-AVMODEL-2026-0029 | xingcheng-zhou; xuyuan-han; feng-yang; et al. | unlisted | `limit` | OpenDriveVLA 当前规划评测仅为开放环，作者警告这可能高估鲁棒性。 |
| EA-AVMODEL-2026-0031 | zewei-zhou; tianhui-cai; seth-z-zhao; et al. | unlisted | `limit` | AutoVLA 的 NAVSIM best-of-N 结果依赖 oracle 选择，必须与可直接部署的单次预测分开。 |
| EA-AVMODEL-2026-0032 | zewei-zhou; tianhui-cai; seth-z-zhao; et al. | unlisted | `limit` | AutoVLA 作者仍将 GPU 依赖、显存和计算成本列为实时应用限制。 |
| EA-LIAUTO-2026-0006 | pengxiang-li; yinan-zheng; yue-wang; et al. | unlisted | `limit` | ReflectDrive 单列使用真实未来主体轨迹评分的版本；其结果必须与恒速近似版本区分。 |
| EA-AVMODEL-2026-0034 | nvidia; yan-wang; wenjie-luo; et al. | unlisted | `limit` | 仅优化推理评分时，Alpamayo-R1 的 ADE 和推理—动作一致性会退化；联合一致性奖励改善这种取舍。 |
| EA-AVMODEL-2026-0037 | haoyu-fu; diankun-zhang; zongchuang-zhao; et al. | unlisted | `limit` | MindDrive 在线 RL 的训练轮数与闭环性能并非单调关系，过多更新会降低表现。 |
| EA-AVMODEL-2026-0040 | jing-gu; niccol-cavagnero; gijs-dubbelman | unlisted | `limit` | 移除 LLM 后，Orion-Lite 的主要推理瓶颈转移到重型视觉编码器。 |
| EA-LIAUTO-2026-0012 | yuzhou-huang; benjin-zhu; hengtong-lu; et al. | unlisted | `limit` | MindVLA-U1 的规划、GRPO 和人类偏好结论仅在日志开放环成立，尚不支持反应式闭环或实车安全结论。 |
| EA-AVMODEL-2026-0041 | nicanor-mayumu; xiaoheng-deng; patrick-mukala | unlisted | `limit` | 该审计发现 Alpamayo-R1 样本中存在声明减速或停车而轨迹继续的说明—动作不一致。 |
| EA-AVMODEL-2026-0042 | nicanor-mayumu; xiaoheng-deng; patrick-mukala | unlisted | `limit` | 该审计使用确定性关键词抽取，作者承认它会漏掉同义表达。 |
| EA-LIAUTO-2026-0016 | haiming-zhang; junfei-zhou; feng-jiang; et al. | unlisted | `limit` | AnyScene 明确不建模交通流或反应式主体，其生成代理受固定 BEV 布局控制。 |
| EA-AVMODEL-2026-0046 | zekai-li; yihao-liang; hongfei-zhang; et al. | unlisted | `limit` | FlashDrive 的 AlpaSim 评测并非所有指标均改善，其中 Wrong Lane 退化。 |

## Synthesis Slots

### 共识/正向证据
- `EA-AVMODEL-2026-0001`: UniAD 以任务 query 作为感知、预测和规划之间的可学习接口，并保留显式中间监督。
- `EA-AVMODEL-2026-0005`: LMDrive 将语言指令、相机和 LiDAR 特征映射为路点及指令完成标志，再由 PID 执行。
- `EA-AVMODEL-2026-0007`: LingoQA 的对象是驾驶视频问答，配套学习式 Lingo-Judge，而非执行驾驶动作。
- `EA-AVMODEL-2026-0009`: DriveLM 以有向 QA 图传递上下文，再将行为说明映射为离散轨迹 token。
- `EA-AVMODEL-2026-0011`: DriveVLM-Dual 将低频 VLM 轨迹交给传统规划器进行高频细化，两支异步协作。
- `EA-AVMODEL-2026-0013`: NAVSIM 仅在初始帧调用规划策略，随后固定计划进行非反应式模拟，没有环境反馈给策略。
- `EA-AVMODEL-2026-0015`: EMMA 将驾驶任务的非传感器输入和输出统一为文本，允许规划、检测和路网任务联合训练。
- `EA-LIAUTO-2026-0001`: DrivingSphere 把可控占据、视觉渲染与交通主体状态更新接成仿真闭环，区别于只生成固定视频。
### 条件成立
- `EA-AVMODEL-2026-0002`: UniAD 预测轨迹后，在推理时使用占据地图执行额外避碰优化。
- `EA-AVMODEL-2026-0006`: LMDrive 的连续多句指令比单句指令更困难，实验中的驾驶分数与路线完成率下降。
- `EA-AVMODEL-2026-0008`: LingoQA 研究发现多帧上下文有助区分动态交通、信号灯变化等单帧易错情形。
- `EA-AVMODEL-2026-0012`: 论文报告双 OrinX 的车载部署；VLM 与高频驾驶系统在不同处理器运行。
- `EA-AVMODEL-2026-0016`: EMMA 的内部数据消融中，场景描述对规划表现影响中性，而元决策和关键物体识别带来改善。
- `EA-AVMODEL-2026-0019`: DiffusionDrive 的主 NAVSIM 设置采用前向相机与栅格 LiDAR；nuScenes 实验采用另一骨干配置。
- `EA-AVMODEL-2026-0021`: DiMA 中仅把 VQA 和规划损失加到 BEV 特征上的朴素联合训练，收益并不一致。
- `EA-AVMODEL-2026-0024`: 官方 CARLA Leaderboard 仅测试 SimLingo-BASE；完整 SimLingo 的闭环驾驶在本地 Bench2Drive 检验。
### 限制与失败模式
- `EA-AVMODEL-2026-0003`: 无视觉 AD-MLP 在 nuScenes 开放环能取得有竞争力的轨迹结果，暴露指标与真实驾驶能力的落差。
- `EA-AVMODEL-2026-0004`: 占据栅格离散化会使真实记录轨迹被误判碰撞，栅格尺寸影响结果。
- `EA-AVMODEL-2026-0010`: DriveLM-Agent 的论文规划验证仍为开放环；作者将闭环列为后续方向。
- `EA-AVMODEL-2026-0014`: NAVSIM 作者指出，高 PDMS 并不总对应高闭环分数，建议配合 CARLA 等闭环评测。
- `EA-AVMODEL-2026-0017`: 作者明确指出，人可读的辅助输出和驾驶动作并不保证始终一致。
- `EA-LIAUTO-2026-0002`: DrivingSphere 报告的 UniAD 交互仿真路线完成度仍低；逼真度提升不等于策略可靠或已完成实车迁移。
- `EA-AVMODEL-2026-0023`: SimLingo 的消融未观察到未对齐语言任务对驾驶的明确正负影响；CoT 的驾驶收益也未达统计显著。
- `EA-AVMODEL-2026-0027`: ORION 作者将大 VLM 的计算复杂度列为实时驾驶部署限制。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 30 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-AVMODEL-2026-0001` UniAD 以任务 query 作为感知、预测和规划之间的可学习接口，并保留显式中间监督。
  - `EA-AVMODEL-2026-0005` LMDrive 将语言指令、相机和 LiDAR 特征映射为路点及指令完成标志，再由 PID 执行。
  - `EA-AVMODEL-2026-0007` LingoQA 的对象是驾驶视频问答，配套学习式 Lingo-Judge，而非执行驾驶动作。
- Scientific memo preview: 《智驾模型与关键团队：VLA、驾驶基础模型及理想系列论文》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 智驾模型与关键团队：VLA、驾驶基础模型及理想系列论文 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 智驾模型与关键团队：VLA、驾驶基础模型及理想系列论文: 先看证据边界，再谈一个可传播的反常识洞察。

## Draft Outline

1. 研究边界与证据范围
2. 概念与问题结构
3. 主要共识
4. 条件、限制与分歧
5. 未解决问题
6. 对后续研究/项目的启发

## Traceability Checklist

- Cite event IDs for paper-specific claims.
- Cite stable source IDs for topic-card background.
- Mark cross-event synthesis as `inference` with a short reason.
- Do not cite candidate-only papers as accepted evidence.
- Open raw sources before using exact wording.
