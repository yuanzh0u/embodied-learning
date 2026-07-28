# Review Packet: Jim Fan research trajectory: general agents, embodied intelligence, foundation models, and open-world learning

## 第一阶段结论

这条研究路线最稳定的主线，不是某个单一模型名称，而是把“可扩展训练—跨分布泛化—开放世界任务生成—技能/奖励接口—真实机器人闭环”逐步接起来。2015 年的工作首先体现为大规模训练系统与严格消融；2019—2021 年转向分布式强化学习、交互式仿真和视觉鲁棒性；2022 年集中探索跨任务、跨形态和多模态提示接口；2023—2024 年把 LLM 用作课程、程序技能、奖励和 domain randomization 的生成器；2025—2026 年则汇入 VLA、异构数据、世界模型和真实机器人系统。

这个阶段划分是本综述根据论文问题与方法之间的继承关系做出的 **inference**，不是 Jim Fan 本人公开给出的分期。论文能确认的是合作团队在各自实验边界内报告了相应结果；不能确认的是作者名单中每个人的具体贡献、技术传播度等同于有效性、以及演示系统已经具备跨场景通用物理智能。

本轮的证据结构为：15 篇 Jim Fan 署名论文 + 2 篇外部限制/反证文献；全部使用完整非 OCR 全文，17/17 通过 paper-note validation 与 claim-support audit。候选池为 471 篇，完整全文恢复 47 篇，五个覆盖维度与两轮饱和检查均通过。

## 身份消歧与归属边界

- **confirmed**：论文作者的规范姓名是 `Linxi Fan`；本人主页使用 `Linxi "Jim" Fan`。本轮将 Jim Fan、Linxi Fan、Linxi "Jim" Fan 视为同一研究者。依据是[本人主页](https://jimfan.me/)、[NVIDIA 官方研究页面](https://research.nvidia.com/labs/lpr/author/jim-fan/)和论文作者记录，核验日为 2026-07-21。
- **confirmed**：截至核验日，官方 NVIDIA 页面确认其 NVIDIA 归属及 Robotics 研究方向；[Stanford 学位记录](https://searchworks.stanford.edu/view/14300918)确认论文题目为 *Training and Deploying Visual Agents at Scale*。
- **disputed / unresolved**：本人主页、较新的活动介绍和其他自维护页面使用了 Senior Research Scientist、Lead of AI Agents、Director 或 Distinguished Research Scientist 等不同表述；NVIDIA 官方研究页没有给出可裁决的当前职称。因此本综述只写“在 NVIDIA 从事机器人/智能体研究”，不指定唯一当前头衔。
- **confirmed but narrow**：作者顺序只能证明署名。SECANT 和 MineDojo 中 Linxi Fan 为第一作者；GR00T N1 的 arXiv 备注明确写明作者按字母排序、项目负责人为 Linxi "Jim" Fan 与 Yuke Zhu。除此之外，不从作者顺序推断个人负责的模块。
- **evidence gap**：大多数论文没有可用于本轮审计的个人贡献声明；因此“Jim Fan 发明了某系统/独立提出某方法”一类表达不被接纳，统一写成“Jim Fan 参与署名的团队工作”或“该论文报告”。

## 人物—项目—论文时间线

| 阶段 | 问题意识 | 代表论文/项目 | 本轮可确认的贡献 | 主要边界 |
|---|---|---|---|---|
| 2015：规模化深度学习与机制拆解 | 模型为何有效；数据、计算、训练吞吐与部署如何共同决定进展 | Ladder Network ablation；Deep Speech 2 | 组件贡献不等；大数据、大模型、HPC 与服务系统共同构成研究系统（[0001](evidence-appendix.md#ea-jimfan-read-0001), [0002](evidence-appendix.md#ea-jimfan-read-0002)） | 图像分类与语音识别，不是具身智能证据 |
| 2019—2021：可扩展 RL、仿真与视觉泛化 | 如何让交互学习可复现、可扩展，并对视觉分布偏移更稳健 | SURREAL-System；iGibson 1.0；SECANT | 分布式 RL 去瓶颈、交互式家庭仿真、强弱增强分阶段的 zero-shot visual generalization（[0003](evidence-appendix.md#ea-jimfan-read-0003), [0004](evidence-appendix.md#ea-jimfan-read-0004), [0005](evidence-appendix.md#ea-jimfan-read-0005)） | 吞吐不等于泛化；iGibson 的实机证据仅为匹配公寓中的 LiDAR PointGoal；SECANT 主要处理外观变化 |
| 2022：通用控制接口与开放世界基座 | 能否共享 transformer 表征，并跨任务、形态和多模态提示组合泛化 | Pre-Trained LMs for Interactive Decision-Making；MetaMorph；MineDojo；VIMA | 顺序结构与预训练初始化、形态条件控制、Minecraft 任务/知识/奖励基座、多模态提示策略（[0006](evidence-appendix.md#ea-jimfan-read-0006)–[0009](evidence-appendix.md#ea-jimfan-read-0009)） | 多数证据来自模拟环境；自然语言语义并非所有增益的唯一来源；VIMA 在 novel-task L4 仍明显退化 |
| 2023—2024：LLM 作为课程、技能与奖励设计器 | 如何在没有固定任务列表和手工密集奖励时持续探索、积累技能并自动设计训练目标 | Voyager；Eureka；DrEureka | 自动课程 + 程序技能库 + 执行反馈；进化式 reward code；reward-aware domain randomization（[0010](evidence-appendix.md#ea-jimfan-read-0010)–[0012](evidence-appendix.md#ea-jimfan-read-0012)） | Voyager 依赖 Minecraft 与高层 API；Eureka 的强证据在仿真；DrEureka 只在两个实机任务族验证，且 plain Eureka 实机行走失败 |
| 2025—2026：物理 AI 基础模型栈 | 如何组合 VLM 推理、连续动作专家、异构数据和世界模型，并进入真实机器人闭环 | GR00T N1；DreamDojo；CaP-X | 双系统 VLA、真实/人类视频/合成数据混合、latent-action world model、对 coding-agent 脚手架的系统评测（[0014](evidence-appendix.md#ea-jimfan-read-0014)–[0016](evidence-appendix.md#ea-jimfan-read-0016)） | GR00T N1 的实机结果是两项短时桌面任务；DreamDojo 下游验证集中于水果装袋；CaP-X 表明高层 primitive 会掩盖低层能力缺口 |

两篇外部限制证据不属于 Jim Fan 的论文序列：BadRobot 说明具身 LLM 的文本对齐不能自动保证物理动作安全，且两种防御仍不充分（[0013](evidence-appendix.md#ea-jimfan-read-0013)）；*Robots Need More than VLA and World Models* 则提出数据、跨本体、物理后果、奖励和部署反馈接口仍是缺口（[0017](evidence-appendix.md#ea-jimfan-read-0017)）。后者是 position paper，应当作为待检验框架，而非经验性反驳。

## 按主张组织的 Claim Map

### C1. 规模不是“模型参数更多”，而是完整实验系统的规模

- **支持**：Deep Speech 2 和 SURREAL-System 把训练吞吐、资源调度、网络通信和部署成本纳入方法系统（0002、0003）。
- **限制**：系统吞吐只提高实验能力，不直接证明更强泛化或真实可靠性。
- **与知识单元关系**：对应 `EA-MODEL` 的“预训练价值最终以闭环结果验收”，也与 `EA-DATA` 的数据工程观点一致。

### C2. 通用化首先表现为显式接口，而不是一个模型直接控制所有环境

- **支持**：MetaMorph 用 morphology condition；VIMA 用多模态 prompt 与 object token；GR00T N1 用 VLM System 2 + diffusion-action System 1（0007、0009、0014）。
- **限制/反面**：VIMA 的最难 novel-task 设置仍显著退化；CaP-X 发现高层 primitive 能抬高成功率但掩盖低层几何和控制缺口（0016）。
- **推断**：这些工作共同指向“共享骨干 + 结构化接口 + 专用动作模块”，与 `EA-MODEL`、`EA-ALIGN` 当前判断一致；这不是任何单篇论文直接证明的统一架构定律。

### C3. 开放世界学习依赖课程、记忆、可执行技能和反馈闭环的组合

- **支持**：MineDojo 提供任务、互联网知识和 learned reward；Voyager 把自动课程、代码技能库、执行反馈和自验证结合起来（0008、0010）。
- **限制**：Minecraft 的程序接口、可逆试错成本和离散反馈远好于真实机器人环境；不能把“游戏内持续发现物品”直接改写为物理世界终身学习。
- **evidence gap**：缺少跨环境、跨低层控制器、长时间真实运行和遗忘/恢复审计。

### C4. LLM 可以自动化奖励与仿真参数设计，但仿真成功不是实机成功

- **支持**：Eureka 在 29 个仿真环境中生成 reward code，并通过迭代反思改善；DrEureka 将 reward-aware prior 用于 domain randomization（0011、0012）。
- **关键反面结果**：plain Eureka policy 在真实四足行走中失败；这直接否定“仿真奖励好即可自然跨越 sim-to-real”的强表述。
- **适用边界**：DrEureka 的实机结果来自两个任务族，且作者承认无视觉输入、静态 DR、无法自动选择真实策略。

### C5. 物理 AI 的下一步从策略模型扩展为数据—动作—世界模型—反馈栈

- **支持**：GR00T N1 混合真实机器人、人类视频和合成数据；DreamDojo 用 44k 小时第一视角视频与 latent action 预训练 world model（0014、0015）。
- **限制**：前者的实机验证小且短时；后者的 policy-evaluation 高相关性只在 20 个水果装袋场景中测得，并存在乐观仿真、罕见快速动作、多视角和长期保持缺口。
- **外部 gap**：0017 将物理数据自动标注、跨本体 retargeting、physics-grounded consequences、reward inference 和 self-improving deployment 视为仍缺失的接口。

### C6. 传播力、引用量与技术有效性必须分账

- **confirmed**：本轮只能确认论文在各自任务、指标和硬件上的报告结果。
- **not established**：本轮没有把引用量、社交媒体传播、项目演示或公司叙事作为有效性证据。
- **下一阶段所需证据**：独立复现、下游系统采用、跨平台迁移、真实闭环寿命、失败恢复、安全与成本数据。

## 来源分级与使用规则

1. **Tier A — accepted paper evidence**：17 篇完整非 OCR 全文、paper note、claim-support audit 和 evidence event。只有这一层可以支持论文结论与定量/机制主张。
2. **Tier B — official context**：本人主页、NVIDIA 官方研究页、Stanford 学位记录。只用于姓名、机构、学位题目和本人公开研究表述；快速变化字段注明 2026-07-21 核验日。
3. **Tier C — project pages / talks / interviews**：可用于项目动机、愿景和本人观点，但必须与论文结果分开。本轮未用其替代任何论文证据。
4. **Tier D — secondary coverage / social media**：只能提供线索或传播背景，不进入 accepted evidence。本轮没有用二手报道裁决任职、个人贡献或技术有效性。

## 下一阶段最值得深入的五个问题

1. MineDojo、VIMA、Voyager、Eureka/DrEureka 的**独立复现和下游采用链**是什么？哪些后续工作真正继承其机制，哪些只继承叙事或 benchmark？
2. 从 VIMA/GR00T N1/CaP-X 出发，如何建立统一的**接口抽象度 × 跨任务 × 跨本体 × 实机闭环**评测，分离 foundation model 能力与人工 API/控制器脚手架？
3. GR00T N1 与 DreamDojo 中真实机器人、人类视频和合成数据各自贡献多少？是否存在经过公平预算控制的**数据混合消融与负迁移检查**？
4. DreamDojo 类 world model 何时可被视为策略评估器？需要怎样的 **action fidelity、接触/力学、failure optimism、反事实和 sim-real ranking** 门槛？
5. 能否通过贡献声明、代码责任、项目记录和可核验访谈建立更细的**个人—团队贡献图**，而不依赖作者顺序或媒体标签？

## Scope

- Topic: Jim Fan research trajectory: general agents, embodied intelligence, foundation models, and open-world learning
- Time range: 2010-01-01..2026-07-21
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-4D`, `EA-ALIGN`, `EA-DATA`
- Evidence events: 17
- Topic cards: 5
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 17
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: [EA-JIMFAN-READ-0015](evidence-appendix.md#ea-jimfan-read-0015), [EA-JIMFAN-READ-0013](evidence-appendix.md#ea-jimfan-read-0013), [EA-JIMFAN-READ-0008](evidence-appendix.md#ea-jimfan-read-0008), [EA-JIMFAN-READ-0004](evidence-appendix.md#ea-jimfan-read-0004), [EA-JIMFAN-READ-0001](evidence-appendix.md#ea-jimfan-read-0001), [EA-JIMFAN-READ-0002](evidence-appendix.md#ea-jimfan-read-0002), [EA-JIMFAN-READ-0003](evidence-appendix.md#ea-jimfan-read-0003), [EA-JIMFAN-READ-0010](evidence-appendix.md#ea-jimfan-read-0010), [EA-JIMFAN-READ-0005](evidence-appendix.md#ea-jimfan-read-0005), [EA-JIMFAN-READ-0006](evidence-appendix.md#ea-jimfan-read-0006), [EA-JIMFAN-READ-0007](evidence-appendix.md#ea-jimfan-read-0007), [EA-JIMFAN-READ-0009](evidence-appendix.md#ea-jimfan-read-0009)
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 17 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 17
- Structure mapped: 17
- Deep-read papers: 17
- Claim-verified papers: 17
- Accepted evidence papers: 17
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- Fallback sources are review-packet context, not Hub evidence JSONL.

### official-context
- Linxi Jim Fan — personal research homepage - https://jimfan.me/
- NVIDIA Learning and Perception Research — Jim Fan - https://research.nvidia.com/labs/lpr/author/jim-fan/
- NVIDIA Seattle Robotics Lab — Jim Fan - https://research.nvidia.com/labs/srl/authors/jim-fan/
- Stanford SearchWorks — Training and Deploying Visual Agents at Scale - https://searchworks.stanford.edu/view/14300918

## Topic Card Context

- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。VLA 可以继承视觉和语言先验，却不会自动继承运动、接触和控制器先验；语言—视觉—动作接口需要显式对齐。4D 和世界模型可以提供几何动态监督、未来想象和动作筛选，但训练目标必须面向动作质量而非只追求视觉重建。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测应分开记录预测保真与决策有效，防止“视频更真实”掩盖错误动作响应。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- `EA-4D` 4D 时空推理与世界动态: 具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。
  - 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
  - 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
  - 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
  - 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
  - 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。
- `EA-ALIGN` VLA 多模态与动作对齐: VLA 对齐的核心不是把语言、视觉和动作都变成 token，而是处理三种信号的粒度与物理语义错配：语言通常任务级且稀疏，视觉高维稠密并容易形成捷径，动作连续、闭环且受本体和控制器约束。可靠系统需要显式连接语言到任务阶段、视觉几何到可执行动作、共享状态变化到机器人特定控制器。动作表示应以物理状态变化和可执行性为中心，而不是以模型输出方便为中心。
  - 稠密 visual-action 监督可能压过稀疏 language-action 信号，使语言退化为装饰性条件。
  - 阶段级语言、dense reasoning 或独立 language-action pretraining 可以增强语言对动作的约束，但会引入新的标注和误差传播问题。
  - 视觉不是越稠密越好；应通过 task-space action、结构化场景接口、affordance 或轨迹监督组织成动作相关表示。
  - 离散 action token 便于接入自回归模型，但解码到连续控制时必须条件化机器人状态、本体、接触和控制器。
  - VLA 可以继承视觉与语言先验，却不会自动继承连续运动先验；action prior 或 flow/diffusion action expert 可独立预训练。
- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；高分筛选还必须保留任务、本体、场景和长尾覆盖。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。所有异构数据都应声明其可信监督字段，并以真实闭环收益作为最终验收。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 5 |
| `conditional` | 条件成立 | 9 |
| `limit` | 限制/负面 | 2 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 1511.06430: Deconstructing the Ladder Network Architecture | 2015-11-19 | support | [EA-JIMFAN-READ-0001](evidence-appendix.md#ea-jimfan-read-0001) |
| 1512.02595: Deep Speech 2: End-to-End Speech Recognition in English and Mandarin | 2015-12-08 | support | [EA-JIMFAN-READ-0002](evidence-appendix.md#ea-jimfan-read-0002) |
| 1909.12989: SURREAL-System: Fully-Integrated Stack for Distributed Deep Reinforcement Learning | 2019-09-27 | support | [EA-JIMFAN-READ-0003](evidence-appendix.md#ea-jimfan-read-0003) |
| 2012.02924: iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes | 2020-12-05 | conditional | [EA-JIMFAN-READ-0004](evidence-appendix.md#ea-jimfan-read-0004) |
| 2106.09678: SECANT: Self-Expert Cloning for Zero-Shot Generalization of Visual Policies | 2021-06-17 | conditional | [EA-JIMFAN-READ-0005](evidence-appendix.md#ea-jimfan-read-0005) |
| 2202.01771: Pre-Trained Language Models for Interactive Decision-Making | 2022-02-03 | conditional | [EA-JIMFAN-READ-0006](evidence-appendix.md#ea-jimfan-read-0006) |
| 2203.11931: MetaMorph: Learning Universal Controllers with Transformers | 2022-03-22 | conditional | [EA-JIMFAN-READ-0007](evidence-appendix.md#ea-jimfan-read-0007) |
| 2206.08853: MineDojo: Building Open-Ended Embodied Agents with Internet-Scale Knowledge | 2022-06-17 | support | [EA-JIMFAN-READ-0008](evidence-appendix.md#ea-jimfan-read-0008) |
| 2210.03094: VIMA: General Robot Manipulation with Multimodal Prompts | 2022-10-06 | conditional | [EA-JIMFAN-READ-0009](evidence-appendix.md#ea-jimfan-read-0009) |
| 2305.16291: Voyager: An Open-Ended Embodied Agent with Large Language Models | 2023-05-25 | support | [EA-JIMFAN-READ-0010](evidence-appendix.md#ea-jimfan-read-0010) |
| 2310.12931: Eureka: Human-Level Reward Design via Coding Large Language Models | 2023-10-19 | conditional | [EA-JIMFAN-READ-0011](evidence-appendix.md#ea-jimfan-read-0011) |
| 2406.01967: DrEureka: Language Model Guided Sim-To-Real Transfer | 2024-06-04 | conditional | [EA-JIMFAN-READ-0012](evidence-appendix.md#ea-jimfan-read-0012) |
| 2407.20242: BadRobot: Jailbreaking Embodied LLM Agents in the Physical World | 2024-07-16 | limit | [EA-JIMFAN-READ-0013](evidence-appendix.md#ea-jimfan-read-0013) |
| 2503.14734: GR00T N1: An Open Foundation Model for Generalist Humanoid Robots | 2025-03-18 | conditional | [EA-JIMFAN-READ-0014](evidence-appendix.md#ea-jimfan-read-0014) |
| 2602.06949: DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos | 2026-02-06 | conditional | [EA-JIMFAN-READ-0015](evidence-appendix.md#ea-jimfan-read-0015) |
| 2603.22435: CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation | 2026-03-23 | limit | [EA-JIMFAN-READ-0016](evidence-appendix.md#ea-jimfan-read-0016) |
| 2606.06556: Robots Need More than VLA and World Models | 2026-06-04 | gap | [EA-JIMFAN-READ-0017](evidence-appendix.md#ea-jimfan-read-0017) |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| [EA-JIMFAN-READ-0015](evidence-appendix.md#ea-jimfan-read-0015) | EA-4D | `conditional` | `direct` | DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and planning benefits after... | Its policy-evaluation correlation is measured on 20 fruit-packing scenes; the paper also acknowledges optimistic simulation and coverage limitations. (4.7 Downstream Applications) | shenyuan-gao; william-liang; kaiyuan-zheng; et al. | 2602.06949 |
| [EA-JIMFAN-READ-0013](evidence-appendix.md#ea-jimfan-read-0013) | EA-ALIGN | `limit` | `direct` | BadRobot demonstrates that embodied LLM systems can be jailbroken into unsafe actions and that two tested defenses only partially mitigate the attacks. | The paper evaluates attacks in embodied-agent simulators and on physical robot setups; defense effects vary across attacks. (5 Mitigation, Challenges and Implications) | hangtao-zhang; chenyu-zhu; xianlong-wang; et al. | 2407.20242 |
| [EA-JIMFAN-READ-0008](evidence-appendix.md#ea-jimfan-read-0008) | EA-DATA | `support` | `direct` | MineDojo combines a large Minecraft task suite, internet-derived multimodal knowledge, and MineCLIP reward learning to support open-ended agent research. | MineCLIP is reported as competitive with manual rewards on selected programmatic tasks and more robust than vanilla CLIP under visual shifts. (Page 9) | linxi-fan; guanzhi-wang; yunfan-jiang; et al. | 2206.08853 |
| [EA-JIMFAN-READ-0004](evidence-appendix.md#ea-jimfan-read-0004) | EA-EVAL | `conditional` | `direct` | iGibson provides interactive household simulation, sensor generation, domain randomization, planning, and demonstration tools, with a bounded LiDAR sim-to-real navigation result. | The platform broadens the experimental substrate for interactive embodied tasks, but its real-transfer evidence is narrow and materially below simulated success. (Page 6) | bokui-shen; fei-xia; chengshu-li; et al. | 2012.02924 |
| [EA-JIMFAN-READ-0001](evidence-appendix.md#ea-jimfan-read-0001) | EA-MODEL | `support` | `direct` | The Ladder Network ablation shows that its components contribute unequally: lateral connections and reconstruction are especially important in the tested semi-supervised setting. | This early work establishes an ablation-centered habit: unpack a successful architecture rather than treating the whole recipe as one indivisible advance. (Page 8) | mohammad-pezeshki; linxi-fan; philemon-brakel; et al. | 1511.06430 |
| [EA-JIMFAN-READ-0002](evidence-appendix.md#ea-jimfan-read-0002) | EA-MODEL | `support` | `direct` | Deep Speech 2 links model progress to joint scaling of data, model size, high-performance training, and deployable inference rather than to architecture alone. | The paper's importance for the trajectory is systems thinking: research throughput and serving constraints are treated as part of the learning system. (Page 23) | dario-amodei; rishita-anubhai; eric-battenberg; et al. | 1512.02595 |
| [EA-JIMFAN-READ-0003](evidence-appendix.md#ea-jimfan-read-0003) | EA-MODEL | `support` | `direct` | SURREAL-System treats distributed-RL infrastructure as an experimental variable: replay sharding and actor batching remove concrete throughput bottlenecks. | The work connects scalable infrastructure, reproducibility, and robotics-suite evaluation in the transition from general ML systems to embodied learning. (Page 8) | linxi-fan; yuke-zhu; jiren-zhu; et al. | 1909.12989 |
| [EA-JIMFAN-READ-0010](evidence-appendix.md#ea-jimfan-read-0010) | EA-MODEL | `support` | `direct` | Voyager's automatic curriculum, executable skill library, and iterative environment feedback jointly support sustained in-context exploration in Minecraft. | The system continues discovering items and transfers stored programs, while ablations show that curriculum, skills, feedback, and the chosen LLM all matter. (3.3 Evaluation Results) | guanzhi-wang; yuqi-xie; yunfan-jiang; et al. | 2305.16291 |
| [EA-JIMFAN-READ-0005](evidence-appendix.md#ea-jimfan-read-0005) | EA-MODEL | `conditional` | `direct` | SECANT decouples policy optimization from robust visual representation learning by cloning a weakly augmented RL expert into a strongly augmented student. | The method targets appearance shift across four domains and makes the expert/student separation the mechanism for zero-shot visual robustness. (Page 1) | linxi-fan; guanzhi-wang; de-an-huang; et al. | 2106.09678 |
| [EA-JIMFAN-READ-0006](evidence-appendix.md#ea-jimfan-read-0006) | EA-MODEL | `conditional` | `direct` | For the tested interactive tasks, sequential representation and pretrained transformer initialization matter more than whether the input sequence uses natural-language semantics. | This qualifies a language-centric reading of the work: much of the transfer can come from sequential structure and pretrained weights. (Page 9) | shuang-li; xavier-puig; chris-paxton; et al. | 2202.01771 |
| [EA-JIMFAN-READ-0007](evidence-appendix.md#ea-jimfan-read-0007) | EA-MODEL | `conditional` | `direct` | MetaMorph shows that conditioning a transformer controller on morphology can support zero-shot transfer within a modular robot design space. | The work moves from one-policy-per-robot toward a morphology-conditioned controller, while keeping the evidence inside simulated modular designs. (Page 7) | agrim-gupta; linxi-fan; surya-ganguli; et al. | 2203.11931 |
| [EA-JIMFAN-READ-0009](evidence-appendix.md#ea-jimfan-read-0009) | EA-MODEL | `conditional` | `direct` | VIMA's multimodal-prompt policy and object-centric tokenization improve data efficiency and progressive generalization on its simulated tabletop benchmark. | The experiments support multimodal prompting and object-centric structure, but all methods still degrade on novel-task Level 4. (Page 7) | yunfan-jiang; agrim-gupta; zichen-zhang; et al. | 2210.03094 |
| [EA-JIMFAN-READ-0011](evidence-appendix.md#ea-jimfan-read-0011) | EA-MODEL | `conditional` | `direct` | Eureka's evolutionary search over LLM-generated reward code reaches or exceeds human-designed rewards on most tasks in its simulated suites. | Iterative reward reflection improves generated rewards beyond one-shot sampling, supporting an LLM-as-reward-engineer mechanism in simulation. (4.3 Results) | yecheng-jason-ma; william-liang; guanzhi-wang; et al. | 2310.12931 |
| [EA-JIMFAN-READ-0012](evidence-appendix.md#ea-jimfan-read-0012) | EA-MODEL | `conditional` | `direct` | DrEureka automates both reward and domain-randomization design for two real-robot settings, while plain Eureka fails the real locomotion transfer. | The negative plain-Eureka result is crucial: a reward adequate for simulation is not sufficient for sim-to-real transfer. (VI-A Comparison to Pre-Existing Sim-to-Real Configurations) | yecheng-jason-ma; william-liang; hung-ju-wang; et al. | 2406.01967 |
| [EA-JIMFAN-READ-0014](evidence-appendix.md#ea-jimfan-read-0014) | EA-MODEL | `conditional` | `direct` | GR00T N1 combines a vision-language System 2 with a diffusion-action System 1 and heterogeneous data, with bounded real humanoid manipulation results. | The model is evaluated on two GR-1 bimanual settings using five objects and three trials per object, alongside broader simulated benchmarks. (4.4 Quantitative Results) | nvidia; johan-bjorck; fernando-castaeda; et al. | 2503.14734 |
| [EA-JIMFAN-READ-0016](evidence-appendix.md#ea-jimfan-read-0016) | EA-MODEL | `limit` | `direct` | CaP-X shows that high-level robot primitives can inflate coding-agent success while masking failures in lower-level perception, geometry, and control reasoning. | Performance rises with abstraction, but expressivity narrows; multi-turn execution feedback recovers part of the low-level performance gap. (3.3 Discussion) | letian-fu; justin-yu; karim-el-refai; et al. | 2603.22435 |
| [EA-JIMFAN-READ-0017](evidence-appendix.md#ea-jimfan-read-0017) | EA-MODEL | `gap` | `direct` | A 2026 position paper argues that VLAs and world models remain incomplete without interfaces for physical data, cross-embodiment retargeting, grounded consequences, rewards, and d... | This is counterevidence at the level of field framing, not an empirical falsification of any single Jim Fan paper. (3 The Missing Components for Physical Intelligence) | elis-karcini; faisal-mehrban; quang-nguyen; et al. | 2606.06556 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| [EA-JIMFAN-READ-0015](evidence-appendix.md#ea-jimfan-read-0015) | shenyuan-gao; william-liang; kaiyuan-zheng; et al. | unlisted | `conditional` | DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and pla... |
| [EA-JIMFAN-READ-0013](evidence-appendix.md#ea-jimfan-read-0013) | hangtao-zhang; chenyu-zhu; xianlong-wang; et al. | unlisted | `limit` | BadRobot demonstrates that embodied LLM systems can be jailbroken into unsafe actions and that two tested defenses only partially mitigate the attacks. |
| [EA-JIMFAN-READ-0008](evidence-appendix.md#ea-jimfan-read-0008) | linxi-fan; guanzhi-wang; yunfan-jiang; et al. | unlisted | `support` | MineDojo combines a large Minecraft task suite, internet-derived multimodal knowledge, and MineCLIP reward learning to support open-ended agent research. |
| [EA-JIMFAN-READ-0004](evidence-appendix.md#ea-jimfan-read-0004) | bokui-shen; fei-xia; chengshu-li; et al. | unlisted | `conditional` | iGibson provides interactive household simulation, sensor generation, domain randomization, planning, and demonstration tools, with a bounded LiDAR sim-to-real... |
| [EA-JIMFAN-READ-0001](evidence-appendix.md#ea-jimfan-read-0001) | mohammad-pezeshki; linxi-fan; philemon-brakel; et al. | unlisted | `support` | The Ladder Network ablation shows that its components contribute unequally: lateral connections and reconstruction are especially important in the tested semi-... |
| [EA-JIMFAN-READ-0002](evidence-appendix.md#ea-jimfan-read-0002) | dario-amodei; rishita-anubhai; eric-battenberg; et al. | unlisted | `support` | Deep Speech 2 links model progress to joint scaling of data, model size, high-performance training, and deployable inference rather than to architecture alone. |
| [EA-JIMFAN-READ-0003](evidence-appendix.md#ea-jimfan-read-0003) | linxi-fan; yuke-zhu; jiren-zhu; et al. | unlisted | `support` | SURREAL-System treats distributed-RL infrastructure as an experimental variable: replay sharding and actor batching remove concrete throughput bottlenecks. |
| [EA-JIMFAN-READ-0010](evidence-appendix.md#ea-jimfan-read-0010) | guanzhi-wang; yuqi-xie; yunfan-jiang; et al. | unlisted | `support` | Voyager's automatic curriculum, executable skill library, and iterative environment feedback jointly support sustained in-context exploration in Minecraft. |
| [EA-JIMFAN-READ-0005](evidence-appendix.md#ea-jimfan-read-0005) | linxi-fan; guanzhi-wang; de-an-huang; et al. | unlisted | `conditional` | SECANT decouples policy optimization from robust visual representation learning by cloning a weakly augmented RL expert into a strongly augmented student. |
| [EA-JIMFAN-READ-0006](evidence-appendix.md#ea-jimfan-read-0006) | shuang-li; xavier-puig; chris-paxton; et al. | unlisted | `conditional` | For the tested interactive tasks, sequential representation and pretrained transformer initialization matter more than whether the input sequence uses natural-... |
| [EA-JIMFAN-READ-0007](evidence-appendix.md#ea-jimfan-read-0007) | agrim-gupta; linxi-fan; surya-ganguli; et al. | unlisted | `conditional` | MetaMorph shows that conditioning a transformer controller on morphology can support zero-shot transfer within a modular robot design space. |
| [EA-JIMFAN-READ-0009](evidence-appendix.md#ea-jimfan-read-0009) | yunfan-jiang; agrim-gupta; zichen-zhang; et al. | unlisted | `conditional` | VIMA's multimodal-prompt policy and object-centric tokenization improve data efficiency and progressive generalization on its simulated tabletop benchmark. |
| [EA-JIMFAN-READ-0011](evidence-appendix.md#ea-jimfan-read-0011) | yecheng-jason-ma; william-liang; guanzhi-wang; et al. | unlisted | `conditional` | Eureka's evolutionary search over LLM-generated reward code reaches or exceeds human-designed rewards on most tasks in its simulated suites. |
| [EA-JIMFAN-READ-0012](evidence-appendix.md#ea-jimfan-read-0012) | yecheng-jason-ma; william-liang; hung-ju-wang; et al. | unlisted | `conditional` | DrEureka automates both reward and domain-randomization design for two real-robot settings, while plain Eureka fails the real locomotion transfer. |
| [EA-JIMFAN-READ-0014](evidence-appendix.md#ea-jimfan-read-0014) | nvidia; johan-bjorck; fernando-castaeda; et al. | unlisted | `conditional` | GR00T N1 combines a vision-language System 2 with a diffusion-action System 1 and heterogeneous data, with bounded real humanoid manipulation results. |
| [EA-JIMFAN-READ-0016](evidence-appendix.md#ea-jimfan-read-0016) | letian-fu; justin-yu; karim-el-refai; et al. | unlisted | `limit` | CaP-X shows that high-level robot primitives can inflate coding-agent success while masking failures in lower-level perception, geometry, and control reasoning. |
| [EA-JIMFAN-READ-0017](evidence-appendix.md#ea-jimfan-read-0017) | elis-karcini; faisal-mehrban; quang-nguyen; et al. | unlisted | `gap` | A 2026 position paper argues that VLAs and world models remain incomplete without interfaces for physical data, cross-embodiment retargeting, grounded conseque... |

## Synthesis Slots

### 共识/正向证据
- [EA-JIMFAN-READ-0008](evidence-appendix.md#ea-jimfan-read-0008): MineDojo combines a large Minecraft task suite, internet-derived multimodal knowledge, and MineCLIP reward learning to support open-ended agent research.
- [EA-JIMFAN-READ-0001](evidence-appendix.md#ea-jimfan-read-0001): The Ladder Network ablation shows that its components contribute unequally: lateral connections and reconstruction are especially important in the tested semi-supervised setting.
- [EA-JIMFAN-READ-0002](evidence-appendix.md#ea-jimfan-read-0002): Deep Speech 2 links model progress to joint scaling of data, model size, high-performance training, and deployable inference rather than to architecture alone.
- [EA-JIMFAN-READ-0003](evidence-appendix.md#ea-jimfan-read-0003): SURREAL-System treats distributed-RL infrastructure as an experimental variable: replay sharding and actor batching remove concrete throughput bottlenecks.
- [EA-JIMFAN-READ-0010](evidence-appendix.md#ea-jimfan-read-0010): Voyager's automatic curriculum, executable skill library, and iterative environment feedback jointly support sustained in-context exploration in Minecraft.
### 条件成立
- [EA-JIMFAN-READ-0015](evidence-appendix.md#ea-jimfan-read-0015): DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and planning benefits after robot post-training.
- [EA-JIMFAN-READ-0004](evidence-appendix.md#ea-jimfan-read-0004): iGibson provides interactive household simulation, sensor generation, domain randomization, planning, and demonstration tools, with a bounded LiDAR sim-to-real navigation result.
- [EA-JIMFAN-READ-0005](evidence-appendix.md#ea-jimfan-read-0005): SECANT decouples policy optimization from robust visual representation learning by cloning a weakly augmented RL expert into a strongly augmented student.
- [EA-JIMFAN-READ-0006](evidence-appendix.md#ea-jimfan-read-0006): For the tested interactive tasks, sequential representation and pretrained transformer initialization matter more than whether the input sequence uses natural-language semantics.
- [EA-JIMFAN-READ-0007](evidence-appendix.md#ea-jimfan-read-0007): MetaMorph shows that conditioning a transformer controller on morphology can support zero-shot transfer within a modular robot design space.
- [EA-JIMFAN-READ-0009](evidence-appendix.md#ea-jimfan-read-0009): VIMA's multimodal-prompt policy and object-centric tokenization improve data efficiency and progressive generalization on its simulated tabletop benchmark.
- [EA-JIMFAN-READ-0011](evidence-appendix.md#ea-jimfan-read-0011): Eureka's evolutionary search over LLM-generated reward code reaches or exceeds human-designed rewards on most tasks in its simulated suites.
- [EA-JIMFAN-READ-0012](evidence-appendix.md#ea-jimfan-read-0012): DrEureka automates both reward and domain-randomization design for two real-robot settings, while plain Eureka fails the real locomotion transfer.
### 限制与失败模式
- [EA-JIMFAN-READ-0013](evidence-appendix.md#ea-jimfan-read-0013): BadRobot demonstrates that embodied LLM systems can be jailbroken into unsafe actions and that two tested defenses only partially mitigate the attacks.
- [EA-JIMFAN-READ-0016](evidence-appendix.md#ea-jimfan-read-0016): CaP-X shows that high-level robot primitives can inflate coding-agent success while masking failures in lower-level perception, geometry, and control reasoning.
### 开放问题
- [EA-JIMFAN-READ-0017](evidence-appendix.md#ea-jimfan-read-0017): A 2026 position paper argues that VLAs and world models remain incomplete without interfaces for physical data, cross-embodiment retargeting, grounded consequences, rewards, and deployment feedback.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 17 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - [EA-JIMFAN-READ-0015](evidence-appendix.md#ea-jimfan-read-0015) DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluati...
  - [EA-JIMFAN-READ-0013](evidence-appendix.md#ea-jimfan-read-0013) BadRobot demonstrates that embodied LLM systems can be jailbroken into unsafe actions and that two tested defenses only partially mitigate the attack...
  - [EA-JIMFAN-READ-0008](evidence-appendix.md#ea-jimfan-read-0008) MineDojo combines a large Minecraft task suite, internet-derived multimodal knowledge, and MineCLIP reward learning to support open-ended agent resea...
- Scientific memo preview: 《Jim Fan research trajectory: general agents, embodied intelligence, foundation models, and open-world learning》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: Jim Fan research trajectory: general agents, embodied intelligence, foundation models, and open-world learning 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: Jim Fan research trajectory: general agents, embodied intelligence, foundation models, and open-world learning: 先看证据边界，再谈一个可传播的反常识洞察。

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
