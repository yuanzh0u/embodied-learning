# Review Packet: 近三年具身机器人原子技能的发展及VLA成为主流的技术原因

## Scope

- Topic: 近三年具身机器人原子技能的发展及VLA成为主流的技术原因
- Time range: 2023-07-25..2026-07-25
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-ALIGN`, `EA-XEMBODIMENT`, `EA-EVAL`
- Evidence events: 17
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 17
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-ATOM-2026-0001`, `EA-ATOM-2026-0002`, `EA-ATOM-2026-0004`, `EA-VLABREAK-2026-0001`, `EA-ATOM-2026-0008`, `EA-ATOM-2026-0009`, `EA-ALIGN-READ-0015`, `EA-ATOM-2026-0005`, `EA-ATOM-2026-0003`, `EA-ATOM-2026-0006`, `EA-VLABREAK-2026-0002`, `EA-ATOM-2026-0007`
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

- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型、本体适配器与底层控制器组成的融合栈。近期突破不只是生成更长视频，而是把未来压缩成低频逻辑步骤、稀疏视觉子目标或结构化状态，并验证它与真实动作同步；BadWAM 说明“想象合理、动作错误”足以让系统失效。世界模型应先承担训练期教师、离线排序等低权限任务，再逐级争取在线规划权。Loco-manipulation 与多模态证据还表明，完整动作接口及按功能/时标分层的接触反馈会限制能力上限。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-ALIGN` VLA 多模态与动作对齐: VLA 对齐的核心不是把语言、视觉和动作都变成 token，而是处理多种信号的粒度、功能、频率和物理语义错配：语言通常任务级且稀疏，视觉高维稠密，动作连续且受本体/控制器约束，触觉与力觉则在接触后进入更快的反馈环。可靠系统需要把低频逻辑与视觉子目标、高频 VLA 执行、机器人特定控制器和接触反馈分层连接，并用动作条件状态变化作为共享接口。动作表示应以物理状态变化和可执行性为中心，而不是以模型输出方便为中心。
  - 稠密 visual-action 监督可能压过稀疏 language-action 信号，使语言退化为装饰性条件。
  - 阶段级语言、dense reasoning 或独立 language-action pretraining 可以增强语言对动作的约束，但会引入新的标注和误差传播问题。
  - 视觉不是越稠密越好；应通过 task-space action、结构化场景接口、affordance 或轨迹监督组织成动作相关表示。
  - 离散 action token 便于接入自回归模型，但解码到连续控制时必须条件化机器人状态、本体、接触和控制器。
  - VLA 可以继承视觉与语言先验，却不会自动继承连续运动先验；action prior 或 flow/diffusion action expert 可独立预训练。
- `EA-XEMBODIMENT` 跨本体与数据迁移: 跨本体迁移的核心不是复制姿态、控制命令或传感器 token，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。语言/视觉语义、对象状态变化和粗运动先验较易共享；局部接触载荷、传感器频率、硬件标定和控制接口更依赖目标平台。更稳健的路线是共享 Cartesian/object state delta 或接触目标，再由机器人和传感器特定 adapter、少量目标硬件数据与真实闭环校准落地。
  - 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
  - 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
  - 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
  - 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
  - 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。当前最可靠的应用位于权限阶梯低端：训练期 4D/几何教师、离线策略排序与淘汰、有本体锚定的数据/后训练，以及明确物理变量下的 what-if 检查；在线预演、直接控制和安全裁决需要逐级更强的真实闭环证据。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 7 |
| `conditional` | 条件成立 | 4 |
| `limit` | 限制/负面 | 6 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2310.08864: Open X-Embodiment: Robotic Learning Datasets and RT-X Models | 2023-10-13T05:20:40Z | support | EA-ATOM-2026-0001 |
| 2405.03476: DexSkills: Skill Segmentation Using Haptic Data for Learning Autonomous Long-Horizon Robotic Manipulation Tasks | 2024-05-06T13:51:02Z | conditional | EA-ATOM-2026-0005 |
| 2405.12213: Octo: An Open-Source Generalist Robot Policy | 2024-05-20T17:57:01Z | support | EA-ATOM-2026-0002 |
| 2406.09246: OpenVLA: An Open-Source Vision-Language-Action Model | 2024-06-13T15:46:55Z | conditional | EA-ATOM-2026-0003 |
| 2410.24164: $π_0$: A Vision-Language-Action Flow Model for General Robot Control | 2024-10-31T17:22:30Z | support | EA-ATOM-2026-0004 |
| 2501.15068: An Atomic Skill Library Construction Method for Data-Efficient Embodied Manipulation | 2025-01-25T04:19:33Z | conditional | EA-ATOM-2026-0006 |
| 2505.00527: DeCo: Task Decomposition and Skill Composition for Zero-Shot Generalization in Long-Horizon 3D Manipulation | 2025-05-01T13:52:19Z | limit | EA-ATOM-2026-0007 |
| 2602.11291: H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model | 2026-02-11T19:08:36Z | conditional, limit, support | EA-VLABREAK-2026-0001; EA-VLABREAK-2026-0002; EA-VLABREAK-2026-0003 |
| 2602.21531: LiLo-VLA: Compositional Long-Horizon Manipulation via Linked Object-Centric Policies | 2026-02-25T03:33:39Z | support | EA-ATOM-2026-0008 |
| 2603.07648: AtomicVLA: Unlocking the Potential of Atomic Skill Learning in Robots | 2026-03-08T14:18:56Z | support | EA-ATOM-2026-0009 |
| 2606.09630: ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies | 2026-06-08 | support | EA-ALIGN-READ-0015 |
| 2606.24049: SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies | 2026-06-23 | limit | EA-ALIGN-READ-0001 |
| 2606.30113: SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance | 2026-06-29 | limit | EA-ALIGN-READ-0003 |
| 2606.30456: Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform | 2026-06-29 | limit | EA-ALIGN-READ-0004 |
| 2607.06256: Diagnosing Semantic Handoff Failures in Agent-Orchestrated Vision-Language-Action Skill Composition | 2026-07-07T13:24:37Z | limit | EA-ATOM-2026-0010 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-ATOM-2026-0001 | EA-MODEL | `support` | `direct` | RT-X 消融显示，在其跨本体设置中，更大模型容量会增强跨机器人数据集的迁移，这为通用 VLA 的规模化路线提供了直接技术激励。 | 论文在 RT-2-X 设计消融中将更高模型容量与更强跨数据集迁移相联系。 (V-C Design decisions) | open-x-embodiment-collaboration; abby-o-neill; abdul-rehman; et al. | 2310.08864 |
| EA-ATOM-2026-0002 | EA-MODEL | `support` | `direct` | Octo 在 WidowX 消融中表明，宽跨本体数据混合、ViT 骨干和 diffusion action head 的组合优于窄数据或替代动作头，说明 VLA 路线能同时吸收数据规模与连续动作建模收益。 | 论文在同一机器人与任务上消融数据、动作头和视觉架构。 (Appendix F > F-B Model Ablations) | octo-model-team; dibya-ghosh; homer-walke; et al. | 2405.12213 |
| EA-ATOM-2026-0004 | EA-MODEL | `support` | `direct` | π0 将通用 VLM 骨干与专门的连续动作专家结合，并在 10,000 小时、7 种机器人配置和 68 个任务的混合数据上训练；这表明 VLA 主流架构已通过专家化动作头吸收部分‘技能专用化’思路。 | 论文讨论节明确给出数据规模、本体数和任务数，并描述 VLM 与 flow action expert 分工。 (VII Discussion, Limitations, and Future Work) | kevin-black; noah-brown; danny-driess; et al. | 2410.24164 |
| EA-VLABREAK-2026-0001 | EA-MODEL | `support` | `direct` | H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 | 方法定义了逻辑世界模型、视觉世界模型、低层 VLA 和子任务完成检测的两时间尺度接口。 (IV-C Hierarchical World Model Guidance for VLA) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-ATOM-2026-0008 | EA-MODEL | `support` | `direct` | LiLo-VLA 在两个长时程仿真套件上以平均 69% 成功率超过 π0.5 的 28% 和 OpenVLA-OFT 的 2%；它通过几何搬运、物体中心局部 VLA、动态重规划和技能复用组合，而非让单一端到端策略直接承担全部长程责任。 | 主结果表在视觉干扰与最多 16 技能扩展下对比 LiLo-VLA 与两个强 VLA 基线。 (IV-B Main Results: Zero-Shot Compositionality and Scalability) | yue-yang; shuo-cheng; yu-fang; et al. | 2602.21531 |
| EA-ATOM-2026-0009 | EA-MODEL | `support` | `direct` | AtomicVLA 在 LIBERO-LONG 中表明，用语义原子技能路由专家的 SG-MoE 达到 95.2% 成功率，比 token-level MoE 高 6.6 个百分点；原子技能的新进展正是进入 VLA 内部成为专家路由单元。 | 同一 LIBERO-LONG 消融将 skill-guided routing 与 token-level 和 timestep routing 对照。 (4.4 Ablation Study) | likui-zhang; tao-tang; zhihao-zhan; et al. | 2603.07648 |
| EA-ALIGN-READ-0015 | EA-MODEL | `support` | `direct` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 | ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classifi... | haodi-hu; chung-ta-huang; jing-liu; et al. | 2606.09630 |
| EA-ATOM-2026-0005 | EA-MODEL | `conditional` | `direct` | DexSkills 证明了原子技能路线在接触丰富长任务中的价值：触觉与本体信号可将长演示分解为可复用 primitive skills，再由独立策略组合执行；但证据限于预定技能集和特定灵巧手。 | 结论直接将框架概括为从人类演示分解并学习可复用 primitive skills。 (VII Conclusion) | xiaofeng-mao; gabriele-giudici; claudio-coppola; et al. | 2405.03476 |
| EA-ATOM-2026-0003 | EA-MODEL | `conditional` | `direct` | OpenVLA 表明，开源预训练 VLA 可作为新机器人的可复用初始化，但实用采用仍依赖 10–150 条目标任务演示的微调。 | 论文将 10–150 条目标演示的全参数微调设为广泛采用的关键实验。 (5.2 Data-Efficient Adaptation to New Robot Setups) | moo-jin-kim; karl-pertsch; siddharth-karamcheti; et al. | 2406.09246 |
| EA-ATOM-2026-0006 | EA-MODEL | `conditional` | `direct` | 原子技能库的当代发展已与 VLA 紧密耦合：该方法用 VLP 分解任务、用 VLA 微调实现技能，而且原子技能的粒度直接取决于 VLA 的可塑性和适应性。 | VLA Wheel 将技能粒度明确绑定到 VLA 可塑性与适应性。 (3.3 VLA Wheel) | dongjiang-li; bo-peng; chang-li; et al. | 2501.15068 |
| EA-VLABREAK-2026-0002 | EA-MODEL | `conditional` | `direct` | 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 | H-WM 为 64.8%，logic-only 为 48.4%，H-WM-Stable-Diffusion 为 54.4%。 (VI Results) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-ATOM-2026-0007 | EA-MODEL | `limit` | `direct` | DeCo 暴露了原子技能路线的核心成本：即使技能库可以零样本组合新长任务，VLM 规划的状态幻觉和指令分布偏移仍会降低部分原子任务表现。 | 原子任务表中部分任务下降，作者将其归因于 VLM 计划不稳定。 (V-B Generalization Performance on DeCoBench) | zixuan-chen; junhui-yin; yangtao-chen; et al. | 2505.00527 |
| EA-VLABREAK-2026-0003 | EA-MODEL | `limit` | `direct` | H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 | 结论明确列出额外组件/训练阶段的代价，以及对符号化状态的依赖。 (VII Conclusion) | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | 2602.11291 |
| EA-ALIGN-READ-0001 | EA-MODEL | `limit` | `direct` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time... | SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness. (... | haeone-lee | 2606.24049 |
| EA-ALIGN-READ-0003 | EA-MODEL | `limit` | `direct` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same to... | SA-VLA conditions action-token decoding on proprioceptive state via adapters or cross-attention, reporting improved RoboTwin and zero-shot sim-to-real success over tokenizer baselines. (Abstract (full-text section)) | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | 2606.30113 |
| EA-ALIGN-READ-0004 | EA-MODEL | `limit` | `direct` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset c... | The UR5 study reports a gap between offline indicators and unstable closed-loop physical behavior, attributing it to data-model-control pipeline consistency rather than model capacity alone. (Abstract (full-text section... | mathilde-hochedel; marc-lalonde | 2606.30456 |
| EA-ATOM-2026-0010 | EA-MODEL | `limit` | `direct` | 技能组合的瓶颈不只是单技能准确率：该诊断显示快照状态下的 VLA skill competence 与链式执行的 chained-state robustness 存在缺口，需要类型化前后置条件、步级验证和恢复。 | 结论直接概括快照能力与组合状态稳健性之间的诊断差距。 (VII Conclusion) | ke-rui; yushen-zuo; jiawei-wang; et al. | 2607.06256 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-ATOM-2026-0001 | open-x-embodiment-collaboration; abby-o-neill; abdul-rehman; et al. | unlisted | `support` | RT-X 消融显示，在其跨本体设置中，更大模型容量会增强跨机器人数据集的迁移，这为通用 VLA 的规模化路线提供了直接技术激励。 |
| EA-ATOM-2026-0002 | octo-model-team; dibya-ghosh; homer-walke; et al. | unlisted | `support` | Octo 在 WidowX 消融中表明，宽跨本体数据混合、ViT 骨干和 diffusion action head 的组合优于窄数据或替代动作头，说明 VLA 路线能同时吸收数据规模与连续动作建模收益。 |
| EA-ATOM-2026-0004 | kevin-black; noah-brown; danny-driess; et al. | unlisted | `support` | π0 将通用 VLM 骨干与专门的连续动作专家结合，并在 10,000 小时、7 种机器人配置和 68 个任务的混合数据上训练；这表明 VLA 主流架构已通过专家化动作头吸收部分‘技能专用化’思路。 |
| EA-VLABREAK-2026-0001 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `support` | H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 |
| EA-ATOM-2026-0008 | yue-yang; shuo-cheng; yu-fang; et al. | unlisted | `support` | LiLo-VLA 在两个长时程仿真套件上以平均 69% 成功率超过 π0.5 的 28% 和 OpenVLA-OFT 的 2%；它通过几何搬运、物体中心局部 VLA、动态重规划和技能复用组合，而非让单一端到端策略直接承担全部长程责任。 |
| EA-ATOM-2026-0009 | likui-zhang; tao-tang; zhihao-zhan; et al. | unlisted | `support` | AtomicVLA 在 LIBERO-LONG 中表明，用语义原子技能路由专家的 SG-MoE 达到 95.2% 成功率，比 token-level MoE 高 6.6 个百分点；原子技能的新进展正是进入 VLA 内部成为专家路由单元。 |
| EA-ALIGN-READ-0015 | haodi-hu; chung-ta-huang; jing-liu; et al. | unlisted | `support` | 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 |
| EA-ATOM-2026-0005 | xiaofeng-mao; gabriele-giudici; claudio-coppola; et al. | unlisted | `conditional` | DexSkills 证明了原子技能路线在接触丰富长任务中的价值：触觉与本体信号可将长演示分解为可复用 primitive skills，再由独立策略组合执行；但证据限于预定技能集和特定灵巧手。 |
| EA-ATOM-2026-0003 | moo-jin-kim; karl-pertsch; siddharth-karamcheti; et al. | unlisted | `conditional` | OpenVLA 表明，开源预训练 VLA 可作为新机器人的可复用初始化，但实用采用仍依赖 10–150 条目标任务演示的微调。 |
| EA-ATOM-2026-0006 | dongjiang-li; bo-peng; chang-li; et al. | unlisted | `conditional` | 原子技能库的当代发展已与 VLA 紧密耦合：该方法用 VLP 分解任务、用 VLA 微调实现技能，而且原子技能的粒度直接取决于 VLA 的可塑性和适应性。 |
| EA-VLABREAK-2026-0002 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `conditional` | 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 |
| EA-ATOM-2026-0007 | zixuan-chen; junhui-yin; yangtao-chen; et al. | unlisted | `limit` | DeCo 暴露了原子技能路线的核心成本：即使技能库可以零样本组合新长任务，VLM 规划的状态幻觉和指令分布偏移仍会降低部分原子任务表现。 |
| EA-VLABREAK-2026-0003 | jinbang-huang; wenyuan-chen; zhiyuan-li; et al. | unlisted | `limit` | H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 |
| EA-ALIGN-READ-0001 | haeone-lee | unlisted | `limit` | A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units,... |
| EA-ALIGN-READ-0003 | tengyue-jiang; chunpu-xu; jiayue-kang; et al. | unlisted | `limit` | Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottlen... |
| EA-ALIGN-READ-0004 | mathilde-hochedel; marc-lalonde | unlisted | `limit` | Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preproce... |
| EA-ATOM-2026-0010 | ke-rui; yushen-zuo; jiawei-wang; et al. | unlisted | `limit` | 技能组合的瓶颈不只是单技能准确率：该诊断显示快照状态下的 VLA skill competence 与链式执行的 chained-state robustness 存在缺口，需要类型化前后置条件、步级验证和恢复。 |

## Synthesis Slots

### 共识/正向证据
- `EA-ATOM-2026-0001`: RT-X 消融显示，在其跨本体设置中，更大模型容量会增强跨机器人数据集的迁移，这为通用 VLA 的规模化路线提供了直接技术激励。
- `EA-ATOM-2026-0002`: Octo 在 WidowX 消融中表明，宽跨本体数据混合、ViT 骨干和 diffusion action head 的组合优于窄数据或替代动作头，说明 VLA 路线能同时吸收数据规模与连续动作建模收益。
- `EA-ATOM-2026-0004`: π0 将通用 VLM 骨干与专门的连续动作专家结合，并在 10,000 小时、7 种机器人配置和 68 个任务的混合数据上训练；这表明 VLA 主流架构已通过专家化动作头吸收部分‘技能专用化’思路。
- `EA-VLABREAK-2026-0001`: H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。
- `EA-ATOM-2026-0008`: LiLo-VLA 在两个长时程仿真套件上以平均 69% 成功率超过 π0.5 的 28% 和 OpenVLA-OFT 的 2%；它通过几何搬运、物体中心局部 VLA、动态重规划和技能复用组合，而非让单一端到端策略直接承担全部长程责任。
- `EA-ATOM-2026-0009`: AtomicVLA 在 LIBERO-LONG 中表明，用语义原子技能路由专家的 SG-MoE 达到 95.2% 成功率，比 token-level MoE 高 6.6 个百分点；原子技能的新进展正是进入 VLA 内部成为专家路由单元。
- `EA-ALIGN-READ-0015`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
### 条件成立
- `EA-ATOM-2026-0005`: DexSkills 证明了原子技能路线在接触丰富长任务中的价值：触觉与本体信号可将长演示分解为可复用 primitive skills，再由独立策略组合执行；但证据限于预定技能集和特定灵巧手。
- `EA-ATOM-2026-0003`: OpenVLA 表明，开源预训练 VLA 可作为新机器人的可复用初始化，但实用采用仍依赖 10–150 条目标任务演示的微调。
- `EA-ATOM-2026-0006`: 原子技能库的当代发展已与 VLA 紧密耦合：该方法用 VLP 分解任务、用 VLA 微调实现技能，而且原子技能的粒度直接取决于 VLA 的可塑性和适应性。
- `EA-VLABREAK-2026-0002`: 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。
### 限制与失败模式
- `EA-ATOM-2026-0007`: DeCo 暴露了原子技能路线的核心成本：即使技能库可以零样本组合新长任务，VLM 规划的状态幻觉和指令分布偏移仍会降低部分原子任务表现。
- `EA-VLABREAK-2026-0003`: H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。
- `EA-ALIGN-READ-0001`: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- `EA-ALIGN-READ-0003`: Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean different controls under d...
- `EA-ALIGN-READ-0004`: Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not controlled together.
- `EA-ATOM-2026-0010`: 技能组合的瓶颈不只是单技能准确率：该诊断显示快照状态下的 VLA skill competence 与链式执行的 chained-state robustness 存在缺口，需要类型化前后置条件、步级验证和恢复。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-ATOM-2026-0001` RT-X 消融显示，在其跨本体设置中，更大模型容量会增强跨机器人数据集的迁移，这为通用 VLA 的规模化路线提供了直接技术激励。
  - `EA-ATOM-2026-0002` Octo 在 WidowX 消融中表明，宽跨本体数据混合、ViT 骨干和 diffusion action head 的组合优于窄数据或替代动作头，说明 VLA 路线能同时吸收数据规模与连续动作建模收益。
  - `EA-ATOM-2026-0004` π0 将通用 VLM 骨干与专门的连续动作专家结合，并在 10,000 小时、7 种机器人配置和 68 个任务的混合数据上训练；这表明 VLA 主流架构已通过专家化动作头吸收部分‘技能专用化’思路。
- Scientific memo preview: 《近三年具身机器人原子技能的发展及VLA成为主流的技术原因》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近三年具身机器人原子技能的发展及VLA成为主流的技术原因 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近三年具身机器人原子技能的发展及VLA成为主流的技术原因: 先看证据边界，再谈一个可传播的反常识洞察。

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
