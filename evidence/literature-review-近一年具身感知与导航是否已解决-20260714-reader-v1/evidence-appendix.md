# Evidence Appendix: 近一年具身感知与导航是否已解决

- Time range: 2025-07-14..2026-07-14
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-PNAV-2026-0002

- Claim: 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.08325](https://arxiv.org/abs/2601.08325) ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation
- Locator: 4.1 Experimental Results
- Evidence: 结果段在报告总体领先的同时明确指出最难L4任务性能下降。
- Quote: “Although performance decreases on the most difficult L4 tasks (1.2%), ActiveVLA still demonstrates promising long-horizon reasoning and strong 3D perception for precise manipulation.”
- Authors: zhenyang-liu

### EA-PNAV-2026-0011

- Claim: ReaDy-Go支持环境特定的动态sim-to-real路线，但作者仍要求扩大训练环境，并引入安全学习以应对更密集、多样和激进的动态主体。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.11575](https://arxiv.org/abs/2602.11575) ReaDy-Go: Real-to-Sim Dynamic 3D Gaussian Splatting Simulation for Environment-Specific Visual Navigation with Moving Obstacles
- Locator: V Conclusion
- Evidence: 结论把泛化潜力与后续扩环境、处理复杂动态体的必要性并列。
- Quote: “Future work includes expanding training environments to strengthen generalization and integrating safe reinforcement learning methods to handle more challenging scenarios involving diverse dynamic agents beyond humans, dense dynamic obstacle settings, and aggressive human motions.”
- Authors: seungyeon-yoo

### EA-PNAV-2026-0003

- Claim: OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.11072](https://arxiv.org/abs/2603.11072) OA-NBV: Occlusion-Aware Next-Best-View Planning for Human-Centered Active Perception on Mobile Robots
- Locator: V-B Limitations and future work.
- Evidence: 限制段直接划定即时单步观测与完整多视图任务之间的边界。
- Quote: “Finally, OA-NBV targets single-step viewpoint selection for immediate observation quality, rather than multi-view reconstruction.”
- Authors: boxun-hu

### EA-PNAV-2026-0012

- Claim: 真实VLN鲁棒性依赖显式结构先验、异常检测和重规划；没有这些机制的基线在目标式指令或阻塞下会出现灾难性退化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.12696](https://arxiv.org/abs/2603.12696) HaltNav: Reactive Visual Halting over Lightweight Topological Priors for Robust Vision-Language Navigation
- Locator: IV-C Real-World Evaluation Results
- Evidence: 实机结果段直接比较基线在目标式和障碍注入条件下的崩溃。
- Quote: “The real world dramatically amplifies both failure modes observed in simulation. Under goal-only instructions (L2-B), InternVLA-N1 collapses to 0% SR and StreamVLN to 13.33%, far below their simulation counterparts. Under obstacle injection, both baselines drop to 0% SR across all conditions—even StreamVLN, which retained 37.50% in simulation.”
- Authors: zihui-yu

### EA-PNAV-2026-0004

- Claim: 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.14801](https://arxiv.org/abs/2605.14801) Exploring Bottlenecks in VLM-LLM Navigation: How 3D Scene Understanding Capability Impacts Zero-Shot VLN
- Locator: IV CONCLUSIONS
- Evidence: 结论直接同时报告感知饱和和两类仍关键的误差。
- Quote: “Our analysis also revealed that false positives and distorted bounding box aspect ratios are critical factors affecting navigation performance, and that a small set of core navigation-relevant object categories is sufficient for successful navigation.”
- Authors: ziyi-xia

### EA-PNAV-2026-0015

- Claim: 开放世界航空ObjectNav远未解决：基准中所有方法的碰撞率都超过真实部署可接受水平，语义探索尚未转化为安全控制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2508.00288](https://arxiv.org/abs/2508.00288) UAV-ON: A Benchmark for Open-World Object Goal Navigation with Aerial Agents
- Locator: 6.2 Results
- Evidence: 结果段直接指出所有方法的高碰撞率和真实部署不可接受性。
- Quote: “Notably, all methods exhibit collision rates exceeding 30%, which would be unacceptable in real-world UAV deployments where safety is critical. Such high collision rates pose serious risks in physical environments, where hardware damage and human safety must be considered.”
- Authors: jianqiang-xiao

### EA-PNAV-2026-0009

- Claim: 真实社会导航的进步仍依赖受限的人体状态表征；论文明确指出机器人缺少专家可用的人类意图线索，并受到感知延迟影响。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.17204](https://arxiv.org/abs/2509.17204) Ratatouille: Imitation Learning Ingredients for Real-world Social Robot Navigation
- Locator: VI Limitations and Future Work
- Evidence: 限制段直接比较专家与机器人可见信息，说明剩余感知鸿沟。
- Quote: “The expert can infer human intent from subtle body cues and benefits from perfect perception without delays, whereas the robot only observes human positions.”
- Authors: james-r-han

### EA-PNAV-2026-0010

- Claim: 当前VLM导航仍存在显著人类差距，且目标定位是主导失败模式；这说明基础视觉语言能力尚未等价为可靠空间行动。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.26909](https://arxiv.org/abs/2510.26909) NaviTrace: Evaluating Embodied Navigation of Vision-Language Models
- Locator: IV-D Summary of Key Findings
- Evidence: 关键发现段同时报告人类差距和目标定位主导失败。
- Quote: “(1) Large human performance gap. Across all four embodiments and task categories, VLM scores are substantially worse than both human and oracle-like baselines, highlighting significant room for improvement (see Fig. ˜ 4 and Table ˜ III ). (2) Goal localization is the dominant failure mode. When models predict only the goal location and we connect it with a straight line, scores are similar to full-trace predictions.”
- Authors: tim-windecker

### EA-PNAV-2026-0001

- Claim: MSGNav的结果不能说明零样本导航已解决：作者明确指出VFM/VLM延迟阻碍实时部署，且最后一公里仅被缓解而未被彻底解决。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.10376](https://arxiv.org/abs/2511.10376) MSGNav: Unleashing the Power of Multi-modal 3D Scene Graph for Zero-Shot Embodied Navigation
- Locator: 5 Conclusion
- Evidence: 结论段直接给出两项残余问题，构成对榜单增益的部署边界。
- Quote: “Despite these advantages of MSGNav , scene graph-based methods still face low inference efficiency due to the latency of VFMs and VLMs, suggesting future work on faster graph construction and inference for real‑time deployment. Additionally, while the “last-mile” problem has been mitigated by the VVD module, it is not fully resolved.”
- Authors: xun-huang

### EA-PNAV-2026-0007

- Claim: 现有VLN的高层推理并未克服物理执行：即使CoT改善理想化传送设置，严格物理条件下性能仍低，碰撞是主要瓶颈。
- Stance: `limit` | Confidence: `direct`
- Paper: [2512.19021](https://arxiv.org/abs/2512.19021) VLNVerse: A Benchmark for Vision-Language Navigation with Versatile, Embodied, Realistic Simulation and Evaluation
- Locator: 5.3 Zero-shot Performance on VLNVerse
- Evidence: 零样本实验把同一代理放入传送和严格物理设置，直接暴露碰撞导致的退化。
- Quote: “Strikingly, when we introduce CoT prompting, performance in the Tel-Hop setting improves further, yet performance in the Strict setting remains low. This result strongly confirms that physical collision is the primary bottleneck.”
- Authors: sihao-lin

### EA-PNAV-2026-0008

- Claim: CausalNav说明动态语义图可显著推进户外长距离导航，但作者仍把扩展性、极端光照天气和长时一致性列为未解决限制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.01872](https://arxiv.org/abs/2601.01872) CausalNav: A Long-term Embodied Navigation System for Autonomous Mobile Robots in Dynamic Outdoor Scenarios
- Locator: V Conclusion and Future Work
- Evidence: 结论的限制句直接界定了方法在真实动态场景之外的缺口。
- Quote: “While effective in dynamic scenes, CausalNav still faces limitations in scalability, robustness under extreme lighting or weather, and long-horizon consistency.”
- Authors: hongbo-duan

### EA-PNAV-2026-0005

- Claim: 当前LMM的连续空间行动仍远未解决：失败跨越几何感知、跨视角理解、动作后果想象和长期记忆，而非单一视觉分类误差。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.07973](https://arxiv.org/abs/2604.07973) How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace
- Locator: 7. Conclusion
- Evidence: 结论把关键决策分叉后的发散归结为四类相互耦合的能力缺口。
- Quote: “By examining navigation completion progress curves, we identify a critical decision bifurcation (CDB) phenomenon, in which navigation errors of LMMs do not grow gradually but instead deviate after a pivotal decision point. From the CDB viewpoint, we derive that LMMs exhibit emerging reasoning and action capabilities but still suffer from four key limitations: insufficient geometric perception, limited cross-view understanding, lack of spatial imagination about action consequences, and weak long-”
- Authors: baining-zhao

### EA-PNAV-2026-0013

- Claim: 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.10348](https://arxiv.org/abs/2606.10348) Rethinking Embodied Navigation via Relational Inductive Bias
- Locator: Abstract > first paragraph
- Evidence: 引言直接描述视觉相似、静态先验和缺少动作验证导致的持续污染。
- Quote: “visual similarity can induce false positives, static priors are difficult to update once contradicted, and the lack of embodied verification may lead to repeated failed exploration, continuously contaminating map updates and navigation decisions.”
- Authors: weitao-an

### EA-PNAV-2026-0014

- Claim: 端侧VLM可显著降低导航推理延迟，但基于场景图的ObjectNav仍无法原生表示瞬态组合语义，动态线索可能在稀疏查询间丢失。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.27871](https://arxiv.org/abs/2606.27871) LocalNav: Distilling Frontier VLMs and Embodied RL for On-Device Object Goal Navigation
- Locator: 5 Conclusion
- Evidence: 结论的限制段直接说明场景图的时空语义缺口。
- Quote: “Limitations SG -based ObjectNav approaches are spatio-temporally limited. While the SG updates between VLM queries, the SG cannot inherently bind transient, compositional semantics (e.g., distinguishing a generic ”chair” from a ”chair with a person on it” ).”
- Authors: nicolas-baumann

### EA-PNAV-2026-0006

- Claim: 缺乏标准化、可扩展的sim-to-real基准本身就是关键瓶颈，因此模拟榜单分数不足以宣告感知或导航已经解决。
- Stance: `gap` | Confidence: `direct`
- Paper: [2508.11117](https://arxiv.org/abs/2508.11117) Robot Policy Evaluation for Sim-to-Real Transfer: A Benchmarking Perspective
- Locator: I Introduction
- Evidence: 引言直接把标准化sim-real可迁移性基准的缺失称为关键瓶颈。
- Quote: “The absence of a standardized, scalable robotic benchmark for sim-to-real transferability presents a critical bottleneck for visual policy for robotics.”
- Authors: xuning-yang

## References

- `2508.00288` [UAV-ON: A Benchmark for Open-World Object Goal Navigation with Aerial Agents](https://arxiv.org/abs/2508.00288) (2025-08-01)
- `2508.11117` [Robot Policy Evaluation for Sim-to-Real Transfer: A Benchmarking Perspective](https://arxiv.org/abs/2508.11117) (2025-08-14)
- `2509.17204` [Ratatouille: Imitation Learning Ingredients for Real-world Social Robot Navigation](https://arxiv.org/abs/2509.17204) (2025-09-21)
- `2510.26909` [NaviTrace: Evaluating Embodied Navigation of Vision-Language Models](https://arxiv.org/abs/2510.26909) (2025-10-30)
- `2511.10376` [MSGNav: Unleashing the Power of Multi-modal 3D Scene Graph for Zero-Shot Embodied Navigation](https://arxiv.org/abs/2511.10376) (2025-11-13)
- `2512.19021` [VLNVerse: A Benchmark for Vision-Language Navigation with Versatile, Embodied, Realistic Simulation and Evaluation](https://arxiv.org/abs/2512.19021) (2025-12-22)
- `2601.01872` [CausalNav: A Long-term Embodied Navigation System for Autonomous Mobile Robots in Dynamic Outdoor Scenarios](https://arxiv.org/abs/2601.01872) (2026-01-05)
- `2601.08325` [ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation](https://arxiv.org/abs/2601.08325) (2026-01-13)
- `2602.11575` [ReaDy-Go: Real-to-Sim Dynamic 3D Gaussian Splatting Simulation for Environment-Specific Visual Navigation with Moving Obstacles](https://arxiv.org/abs/2602.11575) (2026-02-12)
- `2603.11072` [OA-NBV: Occlusion-Aware Next-Best-View Planning for Human-Centered Active Perception on Mobile Robots](https://arxiv.org/abs/2603.11072) (2026-03-10)
- `2603.12696` [HaltNav: Reactive Visual Halting over Lightweight Topological Priors for Robust Vision-Language Navigation](https://arxiv.org/abs/2603.12696) (2026-03-13)
- `2604.07973` [How Far Are Large Multimodal Models from Human-Level Spatial Action? A Benchmark for Goal-Oriented Embodied Navigation in Urban Airspace](https://arxiv.org/abs/2604.07973) (2026-04-09)
- `2605.14801` [Exploring Bottlenecks in VLM-LLM Navigation: How 3D Scene Understanding Capability Impacts Zero-Shot VLN](https://arxiv.org/abs/2605.14801) (2026-05-14)
- `2606.10348` [Rethinking Embodied Navigation via Relational Inductive Bias](https://arxiv.org/abs/2606.10348) (2026-06-09)
- `2606.27871` [LocalNav: Distilling Frontier VLMs and Embodied RL for On-Device Object Goal Navigation](https://arxiv.org/abs/2606.27871) (2026-06-26)
