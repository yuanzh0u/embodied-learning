# Review Packet: 近一年具身感知与导航是否已解决

## Scope

- Topic: 近一年具身感知与导航是否已解决
- Time range: 2025-07-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-SENSOR`, `EA-EVAL`, `ERR-EMBODIED`
- Evidence events: 15
- Topic cards: 3
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 15
- Stance labels: `conditional`, `gap`, `limit`
- Confidence labels: `direct`
- Trace IDs: `EA-PNAV-2026-0002`, `EA-PNAV-2026-0011`, `EA-PNAV-2026-0003`, `EA-PNAV-2026-0012`, `EA-PNAV-2026-0004`, `EA-PNAV-2026-0015`, `EA-PNAV-2026-0009`, `EA-PNAV-2026-0010`, `EA-PNAV-2026-0001`, `EA-PNAV-2026-0007`, `EA-PNAV-2026-0008`, `EA-PNAV-2026-0005`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 15
- Structure mapped: 15
- Deep-read papers: 15
- Claim-verified papers: 15
- Accepted evidence papers: 15
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；腕部六维力/力矩提供低维全局载荷，触觉提供高维局部接触场，两者不能互换。最新综合更支持按功能和时标选择性耦合：视觉/语言负责慢速全局语义与计划，触觉/力觉进入快速接触反馈，动作条件世界模型负责预测与验证。目标不是堆传感器，而是形成“同步数据—接触表征—动作条件预测—高频纠偏—安全过程评测”的接触执行栈，并证明每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。当前最可靠的应用位于权限阶梯低端：训练期 4D/几何教师、离线策略排序与淘汰、有本体锚定的数据/后训练，以及明确物理变量下的 what-if 检查；在线预演、直接控制和安全裁决需要逐级更强的真实闭环证据。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- `ERR-EMBODIED` 具身智能误差分层与溯源: 具身错误不应按“哪个模型模块报错”粗分，而应寻找第一处可证伪偏离点。感知误差发生在真实世界到状态表征：关键状态没被看到、对齐或记录；认知误差发生在状态表征到意图、计划或动作选择：可用状态足够，但任务、约束、阶段或未来后果判断错误。动作转译、控制执行和硬件响应还应单独记账。可靠归因依赖 probing、episode 遥测、对照实验和闭环结果，不能从失败表象直接猜测。
  - “看对了但做错了”可以通过 probing 证明：视觉骨干保持空间表征，而动作头塌缩回记忆轨迹。
  - 动作语义、坐标系、控制频率和本体 adapter 错配常伪装成感知误差。
  - 接触不可见、标定/同步偏差和缺失模态属于感知链问题；失败阶段判断、计划不可行和 what-if 推理缺失属于认知链问题。
  - 失败恢复是最适合分层诊断的实验场：依次检查状态可见、恢复数据存在、失败阶段判断和纠正动作可执行。
  - 世界模型横跨两层：未来状态预测保真属于感知型问题，候选动作排序与拒绝属于认知型问题。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `conditional` | 条件成立 | 5 |
| `limit` | 限制/负面 | 9 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2508.00288: UAV-ON: A Benchmark for Open-World Object Goal Navigation with Aerial Agents | 2025-08-01 | limit | EA-PNAV-2026-0015 |
| 2508.11117: Robot Policy Evaluation for Sim-to-Real Transfer: A Benchmarking Perspective | 2025-08-14 | gap | EA-PNAV-2026-0006 |
| 2509.17204: Ratatouille: Imitation Learning Ingredients for Real-world Social Robot Navigation | 2025-09-21 | limit | EA-PNAV-2026-0009 |
| 2510.26909: NaviTrace: Evaluating Embodied Navigation of Vision-Language Models | 2025-10-30 | limit | EA-PNAV-2026-0010 |
| 2511.10376: MSGNav: Unleashing the Power of Multi-modal 3D Scene Graph for Zero-Shot Embodied Navigation | 2025-11-13 | limit | EA-PNAV-2026-0001 |
| 2512.19021: VLNVerse: A Benchmark for Vision-Language Navigation with Versatile, Embodied, Realistic Simulation and Evaluation | 2025-12-22 | limit | EA-PNAV-2026-0007 |
| 2601.01872: CausalNav: A Long-term Embodied Navigation System for Autonomous Mobile Robots in Dynamic Outdoor Scenarios | 2026-01-05 | limit | EA-PNAV-2026-0008 |
| 2601.08325: ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation | 2026-01-13 | conditional | EA-PNAV-2026-0002 |
| 2602.11575: ReaDy-Go: Real-to-Sim Dynamic 3D Gaussian Splatting Simulation for Environment-Specific Visual Navigation with Moving O... | 2026-02-12 | conditional | EA-PNAV-2026-0011 |
| 2603.11072: OA-NBV: Occlusion-Aware Next-Best-View Planning for Human-Centered Active Perception on Mobile Robots | 2026-03-10 | conditional | EA-PNAV-2026-0003 |
| 2603.12696: HaltNav: Reactive Visual Halting over Lightweight Topological Priors for Robust Vision-Language Navigation | 2026-03-13 | conditional | EA-PNAV-2026-0012 |
| 2604.07973: How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation... | 2026-04-09 | limit | EA-PNAV-2026-0005 |
| 2605.14801: Exploring Bottlenecks in VLM-LLM Navigation: How 3D Scene Understanding Capability Impacts Zero-Shot VLN | 2026-05-14 | conditional | EA-PNAV-2026-0004 |
| 2606.10348: Rethinking Embodied Navigation via Relational Inductive Bias | 2026-06-09 | limit | EA-PNAV-2026-0013 |
| 2606.27871: LocalNav: Distilling Frontier VLMs and Embodied RL for On-Device Object Goal Navigation | 2026-06-26 | limit | EA-PNAV-2026-0014 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-PNAV-2026-0002 | EA-SENSOR | `conditional` | `direct` | 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。 | 结果段在报告总体领先的同时明确指出最难L4任务性能下降。 (4.1 Experimental Results) | zhenyang-liu | 2601.08325 |
| EA-PNAV-2026-0011 | EA-SENSOR | `conditional` | `direct` | ReaDy-Go支持环境特定的动态sim-to-real路线，但作者仍要求扩大训练环境，并引入安全学习以应对更密集、多样和激进的动态主体。 | 结论把泛化潜力与后续扩环境、处理复杂动态体的必要性并列。 (V Conclusion) | seungyeon-yoo | 2602.11575 |
| EA-PNAV-2026-0003 | EA-SENSOR | `conditional` | `direct` | OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 | 限制段直接划定即时单步观测与完整多视图任务之间的边界。 (V-B Limitations and future work.) | boxun-hu | 2603.11072 |
| EA-PNAV-2026-0012 | EA-SENSOR | `conditional` | `direct` | 真实VLN鲁棒性依赖显式结构先验、异常检测和重规划；没有这些机制的基线在目标式指令或阻塞下会出现灾难性退化。 | 实机结果段直接比较基线在目标式和障碍注入条件下的崩溃。 (IV-C Real-World Evaluation Results) | zihui-yu | 2603.12696 |
| EA-PNAV-2026-0004 | EA-SENSOR | `conditional` | `direct` | 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 | 结论直接同时报告感知饱和和两类仍关键的误差。 (IV CONCLUSIONS) | ziyi-xia | 2605.14801 |
| EA-PNAV-2026-0015 | EA-SENSOR | `limit` | `direct` | 开放世界航空ObjectNav远未解决：基准中所有方法的碰撞率都超过真实部署可接受水平，语义探索尚未转化为安全控制。 | 结果段直接指出所有方法的高碰撞率和真实部署不可接受性。 (6.2 Results) | jianqiang-xiao | 2508.00288 |
| EA-PNAV-2026-0009 | EA-SENSOR | `limit` | `direct` | 真实社会导航的进步仍依赖受限的人体状态表征；论文明确指出机器人缺少专家可用的人类意图线索，并受到感知延迟影响。 | 限制段直接比较专家与机器人可见信息，说明剩余感知鸿沟。 (VI Limitations and Future Work) | james-r-han | 2509.17204 |
| EA-PNAV-2026-0010 | EA-SENSOR | `limit` | `direct` | 当前VLM导航仍存在显著人类差距，且目标定位是主导失败模式；这说明基础视觉语言能力尚未等价为可靠空间行动。 | 关键发现段同时报告人类差距和目标定位主导失败。 (IV-D Summary of Key Findings) | tim-windecker | 2510.26909 |
| EA-PNAV-2026-0001 | EA-SENSOR | `limit` | `direct` | MSGNav的结果不能说明零样本导航已解决：作者明确指出VFM/VLM延迟阻碍实时部署，且最后一公里仅被缓解而未被彻底解决。 | 结论段直接给出两项残余问题，构成对榜单增益的部署边界。 (5 Conclusion) | xun-huang | 2511.10376 |
| EA-PNAV-2026-0007 | EA-SENSOR | `limit` | `direct` | 现有VLN的高层推理并未克服物理执行：即使CoT改善理想化传送设置，严格物理条件下性能仍低，碰撞是主要瓶颈。 | 零样本实验把同一代理放入传送和严格物理设置，直接暴露碰撞导致的退化。 (5.3 Zero-shot Performance on VLNVerse) | sihao-lin | 2512.19021 |
| EA-PNAV-2026-0008 | EA-SENSOR | `limit` | `direct` | CausalNav说明动态语义图可显著推进户外长距离导航，但作者仍把扩展性、极端光照天气和长时一致性列为未解决限制。 | 结论的限制句直接界定了方法在真实动态场景之外的缺口。 (V Conclusion and Future Work) | hongbo-duan | 2601.01872 |
| EA-PNAV-2026-0005 | EA-SENSOR | `limit` | `direct` | 当前LMM的连续空间行动仍远未解决：失败跨越几何感知、跨视角理解、动作后果想象和长期记忆，而非单一视觉分类误差。 | 结论把关键决策分叉后的发散归结为四类相互耦合的能力缺口。 (7. Conclusion) | baining-zhao | 2604.07973 |
| EA-PNAV-2026-0013 | EA-SENSOR | `limit` | `direct` | 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。 | 引言直接描述视觉相似、静态先验和缺少动作验证导致的持续污染。 (Abstract > first paragraph) | weitao-an | 2606.10348 |
| EA-PNAV-2026-0014 | EA-SENSOR | `limit` | `direct` | 端侧VLM可显著降低导航推理延迟，但基于场景图的ObjectNav仍无法原生表示瞬态组合语义，动态线索可能在稀疏查询间丢失。 | 结论的限制段直接说明场景图的时空语义缺口。 (5 Conclusion) | nicolas-baumann | 2606.27871 |
| EA-PNAV-2026-0006 | EA-SENSOR | `gap` | `direct` | 缺乏标准化、可扩展的sim-to-real基准本身就是关键瓶颈，因此模拟榜单分数不足以宣告感知或导航已经解决。 | 引言直接把标准化sim-real可迁移性基准的缺失称为关键瓶颈。 (I Introduction) | xuning-yang | 2508.11117 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-PNAV-2026-0002 | zhenyang-liu | unlisted | `conditional` | 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。 |
| EA-PNAV-2026-0011 | seungyeon-yoo | unlisted | `conditional` | ReaDy-Go支持环境特定的动态sim-to-real路线，但作者仍要求扩大训练环境，并引入安全学习以应对更密集、多样和激进的动态主体。 |
| EA-PNAV-2026-0003 | boxun-hu | unlisted | `conditional` | OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 |
| EA-PNAV-2026-0012 | zihui-yu | unlisted | `conditional` | 真实VLN鲁棒性依赖显式结构先验、异常检测和重规划；没有这些机制的基线在目标式指令或阻塞下会出现灾难性退化。 |
| EA-PNAV-2026-0004 | ziyi-xia | unlisted | `conditional` | 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 |
| EA-PNAV-2026-0015 | jianqiang-xiao | unlisted | `limit` | 开放世界航空ObjectNav远未解决：基准中所有方法的碰撞率都超过真实部署可接受水平，语义探索尚未转化为安全控制。 |
| EA-PNAV-2026-0009 | james-r-han | unlisted | `limit` | 真实社会导航的进步仍依赖受限的人体状态表征；论文明确指出机器人缺少专家可用的人类意图线索，并受到感知延迟影响。 |
| EA-PNAV-2026-0010 | tim-windecker | unlisted | `limit` | 当前VLM导航仍存在显著人类差距，且目标定位是主导失败模式；这说明基础视觉语言能力尚未等价为可靠空间行动。 |
| EA-PNAV-2026-0001 | xun-huang | unlisted | `limit` | MSGNav的结果不能说明零样本导航已解决：作者明确指出VFM/VLM延迟阻碍实时部署，且最后一公里仅被缓解而未被彻底解决。 |
| EA-PNAV-2026-0007 | sihao-lin | unlisted | `limit` | 现有VLN的高层推理并未克服物理执行：即使CoT改善理想化传送设置，严格物理条件下性能仍低，碰撞是主要瓶颈。 |
| EA-PNAV-2026-0008 | hongbo-duan | unlisted | `limit` | CausalNav说明动态语义图可显著推进户外长距离导航，但作者仍把扩展性、极端光照天气和长时一致性列为未解决限制。 |
| EA-PNAV-2026-0005 | baining-zhao | unlisted | `limit` | 当前LMM的连续空间行动仍远未解决：失败跨越几何感知、跨视角理解、动作后果想象和长期记忆，而非单一视觉分类误差。 |
| EA-PNAV-2026-0013 | weitao-an | unlisted | `limit` | 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。 |
| EA-PNAV-2026-0014 | nicolas-baumann | unlisted | `limit` | 端侧VLM可显著降低导航推理延迟，但基于场景图的ObjectNav仍无法原生表示瞬态组合语义，动态线索可能在稀疏查询间丢失。 |
| EA-PNAV-2026-0006 | xuning-yang | unlisted | `gap` | 缺乏标准化、可扩展的sim-to-real基准本身就是关键瓶颈，因此模拟榜单分数不足以宣告感知或导航已经解决。 |

## Synthesis Slots

### 条件成立
- `EA-PNAV-2026-0002`: 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。
- `EA-PNAV-2026-0011`: ReaDy-Go支持环境特定的动态sim-to-real路线，但作者仍要求扩大训练环境，并引入安全学习以应对更密集、多样和激进的动态主体。
- `EA-PNAV-2026-0003`: OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。
- `EA-PNAV-2026-0012`: 真实VLN鲁棒性依赖显式结构先验、异常检测和重规划；没有这些机制的基线在目标式指令或阻塞下会出现灾难性退化。
- `EA-PNAV-2026-0004`: 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。
### 限制与失败模式
- `EA-PNAV-2026-0015`: 开放世界航空ObjectNav远未解决：基准中所有方法的碰撞率都超过真实部署可接受水平，语义探索尚未转化为安全控制。
- `EA-PNAV-2026-0009`: 真实社会导航的进步仍依赖受限的人体状态表征；论文明确指出机器人缺少专家可用的人类意图线索，并受到感知延迟影响。
- `EA-PNAV-2026-0010`: 当前VLM导航仍存在显著人类差距，且目标定位是主导失败模式；这说明基础视觉语言能力尚未等价为可靠空间行动。
- `EA-PNAV-2026-0001`: MSGNav的结果不能说明零样本导航已解决：作者明确指出VFM/VLM延迟阻碍实时部署，且最后一公里仅被缓解而未被彻底解决。
- `EA-PNAV-2026-0007`: 现有VLN的高层推理并未克服物理执行：即使CoT改善理想化传送设置，严格物理条件下性能仍低，碰撞是主要瓶颈。
- `EA-PNAV-2026-0008`: CausalNav说明动态语义图可显著推进户外长距离导航，但作者仍把扩展性、极端光照天气和长时一致性列为未解决限制。
- `EA-PNAV-2026-0005`: 当前LMM的连续空间行动仍远未解决：失败跨越几何感知、跨视角理解、动作后果想象和长期记忆，而非单一视觉分类误差。
- `EA-PNAV-2026-0013`: 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。
### 开放问题
- `EA-PNAV-2026-0006`: 缺乏标准化、可扩展的sim-to-real基准本身就是关键瓶颈，因此模拟榜单分数不足以宣告感知或导航已经解决。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-PNAV-2026-0002` 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。
  - `EA-PNAV-2026-0011` ReaDy-Go支持环境特定的动态sim-to-real路线，但作者仍要求扩大训练环境，并引入安全学习以应对更密集、多样和激进的动态主体。
  - `EA-PNAV-2026-0003` OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。
- Scientific memo preview: 《近一年具身感知与导航是否已解决》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年具身感知与导航是否已解决 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年具身感知与导航是否已解决: 先看证据边界，再谈一个可传播的反常识洞察。

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
