# Review Packet: 近一年具身导航问题是否已有效解决

## Scope

- Topic: 近一年具身导航问题是否已有效解决
- Time range: 2025-07-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-EVAL`, `EA-SENSOR`, `EA-4D`
- Evidence events: 15
- Topic cards: 3
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> full-text evidence -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval, HTML/PDF/OCR recovery, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 15
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-PVC-2026-0007`, `EA-PNAV-2026-0011`, `EA-PNAV-2026-0003`, `EA-PNAV-2026-0012`, `EA-PNAV-2026-0004`, `EA-PNAV-2026-0015`, `EA-PNAV-2026-0009`, `EA-PNAV-2026-0010`, `EA-PNAV-2026-0001`, `EA-PNAV-2026-0007`, `EA-PNAV-2026-0008`, `EA-PNAV-2026-0005`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

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
- `ERR-EMBODIED` 具身智能误差分层与溯源: 具身错误不应按“哪个模型模块报错”粗分，而应寻找第一处可证伪偏离点。感知误差发生在真实世界到状态表征：关键状态没被看到、对齐或记录；认知误差发生在状态表征到意图、计划或动作选择：可用状态足够，但任务、约束、阶段或未来后果判断错误。动作转译、控制执行和硬件响应还应单独记账。可靠归因依赖 probing、episode 遥测、对照实验和闭环结果，不能从失败表象直接猜测。
  - “看对了但做错了”可以通过 probing 证明：视觉骨干保持空间表征，而动作头塌缩回记忆轨迹。
  - 动作语义、坐标系、控制频率和本体 adapter 错配常伪装成感知误差。
  - 接触不可见、标定/同步偏差和缺失模态属于感知链问题；失败阶段判断、计划不可行和 what-if 推理缺失属于认知链问题。
  - 失败恢复是最适合分层诊断的实验场：依次检查状态可见、恢复数据存在、失败阶段判断和纠正动作可执行。
  - 世界模型横跨两层：未来状态预测保真属于感知型问题，候选动作排序与拒绝属于认知型问题。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 1 |
| `conditional` | 条件成立 | 4 |
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
| 2602.11575: ReaDy-Go: Real-to-Sim Dynamic 3D Gaussian Splatting Simulation for Environment-Specific Visual Navigation with Moving O... | 2026-02-12 | conditional | EA-PNAV-2026-0011 |
| 2603.11072: OA-NBV: Occlusion-Aware Next-Best-View Planning for Human-Centered Active Perception on Mobile Robots | 2026-03-10 | conditional | EA-PNAV-2026-0003 |
| 2603.12696: HaltNav: Reactive Visual Halting over Lightweight Topological Priors for Robust Vision-Language Navigation | 2026-03-13 | conditional | EA-PNAV-2026-0012 |
| 2604.07973: How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation... | 2026-04-09 | limit | EA-PNAV-2026-0005 |
| 2605.14801: Exploring Bottlenecks in VLM-LLM Navigation: How 3D Scene Understanding Capability Impacts Zero-Shot VLN | 2026-05-14 | conditional | EA-PNAV-2026-0004 |
| 2606.10348: Rethinking Embodied Navigation via Relational Inductive Bias | 2026-06-09 | limit | EA-PNAV-2026-0013 |
| 2606.27871: LocalNav: Distilling Frontier VLMs and Embodied RL for On-Device Object Goal Navigation | 2026-06-26 | limit | EA-PNAV-2026-0014 |
| 2607.00673: Path Planning in Physically Viable World Models | 2026-07-01 | support | EA-PVC-2026-0007 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-PVC-2026-0007 | EA-MODEL | `support` | `direct` | 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。 | 论文指出多数路径规划假设地图不变,只问 which path is best 而不问 mission 是否在指定物理变化下仍可行;PVWM 用 Gaussian splat 重建加 MPM 物理仿真生成 query-conditioned 修改场景,真实野外场地的洪水多严重度实验显示:仅在原始重建上规划看不到的长程路线失败与改线行为被暴露出来。 (Abstract; 1 Introduction; 2 Related Work) | su-ann-low; cheng-hsi-hsiao; xingjian-li; et al. | 2607.00673 |
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
| EA-PVC-2026-0007 | su-ann-low; cheng-hsi-hsiao; xingjian-li; et al. | unlisted | `support` | 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。 |
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

### 共识/正向证据
- `EA-PVC-2026-0007`: 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。
### 条件成立
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
  - `EA-PVC-2026-0007` 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。
  - `EA-PNAV-2026-0011` ReaDy-Go支持环境特定的动态sim-to-real路线，但作者仍要求扩大训练环境，并引入安全学习以应对更密集、多样和激进的动态主体。
  - `EA-PNAV-2026-0003` OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。
- Scientific memo preview: 《近一年具身导航问题是否已有效解决》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年具身导航问题是否已有效解决 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年具身导航问题是否已有效解决: 先看证据边界，再谈一个可传播的反常识洞察。

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
