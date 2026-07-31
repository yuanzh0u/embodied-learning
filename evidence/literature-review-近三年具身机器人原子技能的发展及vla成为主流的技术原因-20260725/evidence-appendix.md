# Evidence Appendix: 近三年具身机器人原子技能的发展及VLA成为主流的技术原因

- Time range: 2023-07-25..2026-07-25
- Events: 17
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-ATOM-2026-0001

- Claim: RT-X 消融显示，在其跨本体设置中，更大模型容量会增强跨机器人数据集的迁移，这为通用 VLA 的规模化路线提供了直接技术激励。
- Stance: `support` | Confidence: `direct`
- Paper: [2310.08864](https://arxiv.org/abs/2310.08864) Open X-Embodiment: Robotic Learning Datasets and RT-X Models
- Locator: V-C Design decisions
- Evidence: 论文在 RT-2-X 设计消融中将更高模型容量与更强跨数据集迁移相联系。
- Quote: “higher model capacity enables higher degree of transfer across robotic datasets.”
- Authors: open-x-embodiment-collaboration; abby-o-neill; abdul-rehman; et al.

### EA-ATOM-2026-0002

- Claim: Octo 在 WidowX 消融中表明，宽跨本体数据混合、ViT 骨干和 diffusion action head 的组合优于窄数据或替代动作头，说明 VLA 路线能同时吸收数据规模与连续动作建模收益。
- Stance: `support` | Confidence: `direct`
- Paper: [2405.12213](https://arxiv.org/abs/2405.12213) Octo: An Open-Source Generalist Robot Policy
- Locator: Appendix F > F-B Model Ablations
- Evidence: 论文在同一机器人与任务上消融数据、动作头和视觉架构。
- Quote: “We achieve best performance when using the ViT architecture, diffusion action head, and wide training data mixture.”
- Authors: octo-model-team; dibya-ghosh; homer-walke; et al.

### EA-ATOM-2026-0004

- Claim: π0 将通用 VLM 骨干与专门的连续动作专家结合，并在 10,000 小时、7 种机器人配置和 68 个任务的混合数据上训练；这表明 VLA 主流架构已通过专家化动作头吸收部分‘技能专用化’思路。
- Stance: `support` | Confidence: `direct`
- Paper: [2410.24164](https://arxiv.org/abs/2410.24164) $π_0$: A Vision-Language-Action Flow Model for General Robot Control
- Locator: VII Discussion, Limitations, and Future Work
- Evidence: 论文讨论节明确给出数据规模、本体数和任务数，并描述 VLM 与 flow action expert 分工。
- Quote: “Our pre-training mixture consists of 10,000 hours of dexterous manipulation data from 7 different robot configurations and 68 tasks”
- Authors: kevin-black; noah-brown; danny-driess; et al.

### EA-VLABREAK-2026-0001

- Claim: H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: IV-C Hierarchical World Model Guidance for VLA
- Evidence: 方法定义了逻辑世界模型、视觉世界模型、低层 VLA 和子任务完成检测的两时间尺度接口。
- Quote: “The hierarchical information at multiple abstraction level enables the VLA to maintain consistency with long-horizon task structure while remaining responsive to local visual feedback.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-ATOM-2026-0008

- Claim: LiLo-VLA 在两个长时程仿真套件上以平均 69% 成功率超过 π0.5 的 28% 和 OpenVLA-OFT 的 2%；它通过几何搬运、物体中心局部 VLA、动态重规划和技能复用组合，而非让单一端到端策略直接承担全部长程责任。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.21531](https://arxiv.org/abs/2602.21531) LiLo-VLA: Compositional Long-Horizon Manipulation via Linked Object-Centric Policies
- Locator: IV-B Main Results: Zero-Shot Compositionality and Scalability
- Evidence: 主结果表在视觉干扰与最多 16 技能扩展下对比 LiLo-VLA 与两个强 VLA 基线。
- Quote: “This substantial performance gap highlights the limitations of monolithic policies”
- Authors: yue-yang; shuo-cheng; yu-fang; et al.

### EA-ATOM-2026-0009

- Claim: AtomicVLA 在 LIBERO-LONG 中表明，用语义原子技能路由专家的 SG-MoE 达到 95.2% 成功率，比 token-level MoE 高 6.6 个百分点；原子技能的新进展正是进入 VLA 内部成为专家路由单元。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.07648](https://arxiv.org/abs/2603.07648) AtomicVLA: Unlocking the Potential of Atomic Skill Learning in Robots
- Locator: 4.4 Ablation Study
- Evidence: 同一 LIBERO-LONG 消融将 skill-guided routing 与 token-level 和 timestep routing 对照。
- Quote: “AtomicVLA achieves a success rate of 95.2%, outperforming the MoE baseline by 6.6%”
- Authors: likui-zhang; tao-tang; zhihao-zhan; et al.

### EA-ALIGN-READ-0015

- Claim: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09630](https://arxiv.org/abs/2606.09630) ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies
- Locator: 1 Introduction
- Evidence: ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classification mistakes 与 perception errors、sim-to-real mismatch 并列为失败来源。
- Quote: “Instead, it produces a structured recovery descriptor containing the failure type, recovery stage, active entities, confidence, and reward mask.”
- Authors: haodi-hu; chung-ta-huang; jing-liu; et al.

### EA-ATOM-2026-0005

- Claim: DexSkills 证明了原子技能路线在接触丰富长任务中的价值：触觉与本体信号可将长演示分解为可复用 primitive skills，再由独立策略组合执行；但证据限于预定技能集和特定灵巧手。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2405.03476](https://arxiv.org/abs/2405.03476) DexSkills: Skill Segmentation Using Haptic Data for Learning Autonomous Long-Horizon Robotic Manipulation Tasks
- Locator: VII Conclusion
- Evidence: 结论直接将框架概括为从人类演示分解并学习可复用 primitive skills。
- Quote: “decomposing them into reusable primitive skills, trained from human demonstrations.”
- Authors: xiaofeng-mao; gabriele-giudici; claudio-coppola; et al.

### EA-ATOM-2026-0003

- Claim: OpenVLA 表明，开源预训练 VLA 可作为新机器人的可复用初始化，但实用采用仍依赖 10–150 条目标任务演示的微调。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2406.09246](https://arxiv.org/abs/2406.09246) OpenVLA: An Open-Source Vision-Language-Action Model
- Locator: 5.2 Data-Efficient Adaptation to New Robot Setups
- Evidence: 论文将 10–150 条目标演示的全参数微调设为广泛采用的关键实验。
- Quote: “full fine-tuning of all model parameters, using small datasets with 10–150 demonstrations of a target task”
- Authors: moo-jin-kim; karl-pertsch; siddharth-karamcheti; et al.

### EA-ATOM-2026-0006

- Claim: 原子技能库的当代发展已与 VLA 紧密耦合：该方法用 VLP 分解任务、用 VLA 微调实现技能，而且原子技能的粒度直接取决于 VLA 的可塑性和适应性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2501.15068](https://arxiv.org/abs/2501.15068) An Atomic Skill Library Construction Method for Data-Efficient Embodied Manipulation
- Locator: 3.3 VLA Wheel
- Evidence: VLA Wheel 将技能粒度明确绑定到 VLA 可塑性与适应性。
- Quote: “The granularity of atomic skills is determined by the performance of VLA models”
- Authors: dongjiang-li; bo-peng; chang-li; et al.

### EA-VLABREAK-2026-0002

- Claim: 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: VI Results
- Evidence: H-WM 为 64.8%，logic-only 为 48.4%，H-WM-Stable-Diffusion 为 54.4%。
- Quote: “Incorporating visual guidance yields consistent additional gains, providing more than 10% further improvement in Q-score and 17% in success rate.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-ATOM-2026-0007

- Claim: DeCo 暴露了原子技能路线的核心成本：即使技能库可以零样本组合新长任务，VLM 规划的状态幻觉和指令分布偏移仍会降低部分原子任务表现。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.00527](https://arxiv.org/abs/2505.00527) DeCo: Task Decomposition and Skill Composition for Zero-Shot Generalization in Long-Horizon 3D Manipulation
- Locator: V-B Generalization Performance on DeCoBench
- Evidence: 原子任务表中部分任务下降，作者将其归因于 VLM 计划不稳定。
- Quote: “This drop primarily stems from VLM visual-semantic grounding errors:”
- Authors: zixuan-chen; junhui-yin; yangtao-chen; et al.

### EA-VLABREAK-2026-0003

- Claim: H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.11291](https://arxiv.org/abs/2602.11291) H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
- Locator: VII Conclusion
- Evidence: 结论明确列出额外组件/训练阶段的代价，以及对符号化状态的依赖。
- Quote: “The logical world model depends on structured logical state representations, which assume that the task can be meaningfully formulated in a symbolic logical space.”
- Authors: jinbang-huang; wenyuan-chen; zhiyuan-li; et al.

### EA-ALIGN-READ-0001

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: 3.2 Inconsistency of Control Commands across Robots
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Quote: “Recent work has scaled robot learning by training policies on data from multiple embodiments [ 27 , 23 , 32 ] , often using the Cartesian delta action space [ 23 , 32 ] since it is less dependent on robot-specific kinematics and invariant to base-frame translation [ 18 , 14 ] . In practice, this is typically realized by predicting Cartesian delta control commands that are fed to the underlying robot controller [ 23 , 32 ] . Figure 2: Different robots (e.g., UR5 vs. Franka Research 3) require dif”
- Authors: haeone-lee

### EA-ALIGN-READ-0003

- Claim: Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under different robot states and contacts.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30113](https://arxiv.org/abs/2606.30113) SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance
- Locator: Abstract (full-text section)
- Evidence: SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines.
- Quote: “Abstract Discrete action tokenization provides a compact interface for autoregressive VLA policies, but accurately recovering continuous robot actions from discrete codes remains challenging. Existing tokenizers typically map each discrete code to a fixed continuous action prototype, ignoring the robot’s current proprioceptive state. This limitation is particularly pronounced in manipulation, where the same action token may require different continuous controls under different joint configuratio”
- Authors: tengyue-jiang; chunpu-xu; jiayue-kang; et al.

### EA-ALIGN-READ-0004

- Claim: Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30456](https://arxiv.org/abs/2606.30456) Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform
- Locator: Abstract (full-text section)
- Evidence: The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone.
- Quote: “Instead, it is strongly influenced by a combination of factors, including action semantics, coordinate frame conventions, temporal alignment between modalities, image preprocessing consistency, and dataset coverage and quality. These observations lead to a key interpretation: the successful deployment of VLA systems in real-world settings depends less on incremental improvements in model capacity and more on precise control of the entire data–model–control pipeline.”
- Authors: mathilde-hochedel; marc-lalonde

### EA-ATOM-2026-0010

- Claim: 技能组合的瓶颈不只是单技能准确率：该诊断显示快照状态下的 VLA skill competence 与链式执行的 chained-state robustness 存在缺口，需要类型化前后置条件、步级验证和恢复。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06256](https://arxiv.org/abs/2607.06256) Diagnosing Semantic Handoff Failures in Agent-Orchestrated Vision-Language-Action Skill Composition
- Locator: VII Conclusion
- Evidence: 结论直接概括快照能力与组合状态稳健性之间的诊断差距。
- Quote: “a gap between snapshot skill competence and chained-state robustness.”
- Authors: ke-rui; yushen-zuo; jiawei-wang; et al.

## References

- `2310.08864` [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864) (2023-10-13T05:20:40Z)
- `2405.03476` [DexSkills: Skill Segmentation Using Haptic Data for Learning Autonomous Long-Horizon Robotic Manipulation Tasks](https://arxiv.org/abs/2405.03476) (2024-05-06T13:51:02Z)
- `2405.12213` [Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213) (2024-05-20T17:57:01Z)
- `2406.09246` [OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246) (2024-06-13T15:46:55Z)
- `2410.24164` [$π_0$: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164) (2024-10-31T17:22:30Z)
- `2501.15068` [An Atomic Skill Library Construction Method for Data-Efficient Embodied Manipulation](https://arxiv.org/abs/2501.15068) (2025-01-25T04:19:33Z)
- `2505.00527` [DeCo: Task Decomposition and Skill Composition for Zero-Shot Generalization in Long-Horizon 3D Manipulation](https://arxiv.org/abs/2505.00527) (2025-05-01T13:52:19Z)
- `2602.11291` [H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model](https://arxiv.org/abs/2602.11291) (2026-02-11T19:08:36Z)
- `2602.21531` [LiLo-VLA: Compositional Long-Horizon Manipulation via Linked Object-Centric Policies](https://arxiv.org/abs/2602.21531) (2026-02-25T03:33:39Z)
- `2603.07648` [AtomicVLA: Unlocking the Potential of Atomic Skill Learning in Robots](https://arxiv.org/abs/2603.07648) (2026-03-08T14:18:56Z)
- `2606.09630` [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630) (2026-06-08)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2606.30113` [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113) (2026-06-29)
- `2606.30456` [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456) (2026-06-29)
- `2607.06256` [Diagnosing Semantic Handoff Failures in Agent-Orchestrated Vision-Language-Action Skill Composition](https://arxiv.org/abs/2607.06256) (2026-07-07T13:24:37Z)
