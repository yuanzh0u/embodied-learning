# Evidence Appendix: 具身数据感知误差与认知误差区别

- Time range: 2026-01-09..2026-07-09
- Events: 15
- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。

### EA-DATA-2026-LY-0002

- Claim: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: I INTRODUCTION; Abstract; V-D Pilot Study Design; VI-B Pilot Study Results
- Evidence: DQAF 框架从 sub-task progress、motion smoothness、stalls、kinematic limits 抽取质量信号，生成结构化质量评估和自然语言纠正建议；pilot study 中即时反馈条件呈现更高任务完成度、更高 episode-level quality scores 和更少 detected suboptimalities 的趋势。
- Quote: “not only on task completion”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

### EA-DATA-2026-DQ-0002

- Claim: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06564](https://arxiv.org/abs/2607.06564) Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation
- Locator: Abstract; I Introduction; IV-C Geometry-Centric Masked Autoencoding; V-B Multi-Task on MetaWorld and RLBench
- Evidence: 论文将 2D VLA 的困难归因于几何理解和空间推理不足、3D 数据和强 3D encoder 稀缺、跨模态 lifting/projection 损失几何 fidelity；其 GC-MAE 用伪点云监督当前点云重建和未来几何演化，并在仿真与真实任务中提升成功率。
- Authors: jiaming-liu; qingpo-wuwu; nuowei-han; et al.

### EA-DATA-2026-4DDATA-0010

- Claim: 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: I Introduction; III Data Sources for Predictive Robot Learning; Unified supervision; IV-C Joint Flow-Matching Objective
- Evidence: 论文把真实robot data、UMI-style data和egocentric videos划分为不同监督等级，并用modality-specific supervision masks让每条样本只参与其实际拥有的视觉、状态、动作和进度损失。
- Authors: pengfei-zhou; shengcong-chen; di-chen

### EA-DATA-2026-4DDATA-0018

- Claim: 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control; A.1 Data Formatting; A.2 Tactile Sensor Data Processing
- Evidence: HapTile说明所有模态通过机器人控制循环同步，检查空/损坏轨迹和timestamp gaps，验证action-state consistency；附录还要求episode-level split避免temporal leakage，并保留raw/rectified tactile images。
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu

### EA-DATA-2026-4DDATA-0014

- Claim: 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: IV-B 2 Perturbation-Aware Evaluation; IV-C Main Results; Table I
- Evidence: TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。
- Authors: yujie-zang; yuhang-zheng; xian-nie

### EA-EVAL-2026-DQ-0004

- Claim: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02642](https://arxiv.org/abs/2607.02642) GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation
- Locator: Abstract; 1 Introduction; 4.2 Evaluation Protocol; 5.2 How Do Pretraining and Training Data Matter?; 7 Discussion and Conclusion
- Evidence: 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-training 共同决定。
- Authors: gigaworld-team; angyuan-ma; boyuan-wang; et al.

### EA-PVC-2026-0001

- Claim: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.09708](https://arxiv.org/abs/2601.09708) Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning
- Locator: Abstract; 1 Introduction; 5 Conclusion
- Evidence: 论文指出 VLA 靠动作监督擅长基本技能,但在长程规划、失败自我纠正、新场景适应上泛化差;Fast-ThinkAct 用 preference-guided 蒸馏把冗长文本推理压缩为紧凑 latent CoT,在保持 long-horizon planning、few-shot adaptation 和 failure recovery 的同时推理延迟最多降 89.3%。
- Authors: chi-pin-huang; yunze-man; zhiding-yu; et al.

### EA-PVC-2026-0006

- Claim: 纯反应式 VLA 的长程推理、时序 credit assignment 与误差复合问题源于缺少显式预测结构;世界模型既可作决策期评估器(认知层验证),其像素级 rollout 的长程误差积累又是自身的感知型缺陷,需符号结构缓解。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.00080](https://arxiv.org/abs/2605.00080) World Model for Robot Learning: A Comprehensive Survey
- Locator: 1 Introduction; 4.2 World Model for Evaluation; 8.5 Symbolic Structure Integration
- Evidence: 综述指出 reactive VLA 在复杂物理环境中受限于 long-horizon reasoning、temporal credit assignment 与 compounding errors,归因于缺少对世界演化的显式预测结构;世界模型作为 evaluator 可对候选动作做 rollout 排序/拒绝/安全过滤(GPC、IRASim、World-in-World);8.5 节指出 pixel-based rollout 的长程误差积累可用符号/混合世界模型缓解,但符号化依赖感知 grounding。
- Authors: bohan-hou; gen-li; jindou-jia; et al.

### EA-PVC-2026-0003

- Claim: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09630](https://arxiv.org/abs/2606.09630) ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies
- Locator: 1 Introduction; 6 Limitations
- Evidence: ReCoVLA 用外部 VLM 只推断 failure type、recovery stage、active entities、confidence 和 reward mask,不直接生成动作;确定性 reward compiler 做实体 grounding 与 stage gates,residual policy 在冻结 VLA latents 上学纠正。Limitations 明确列出 VLM failure-classification mistakes 与 perception errors、sim-to-real mismatch 并列为失败来源。
- Authors: haodi-hu; chung-ta-huang; jing-liu; et al.

### EA-PVC-2026-0004

- Claim: 感知正确不等于执行正确:VLA 的视觉骨干在扰动场景下仍保持准确空间表征,失败瓶颈在动作头塌缩到记忆轨迹——即 latent perception 与 motor execution 解耦,这是可与感知误差区分的下游错误。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09740](https://arxiv.org/abs/2606.09740) ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models
- Locator: 1 Introduction; 2 Related Work; 3 Method
- Evidence: 论文用 probing 实验证明扰动下 VLA 视觉骨干维持目标物体的准确空间表征,失败仅在 action head:过拟合映射使网络塌缩回训练分布的名义轨迹(memory trap);ProbeAct 从内部 hidden states 提取 3D 目标位置、用运动学状态机检测失败、以 CBF 做最小动作修正,全程无需外部 3D 传感。
- Authors: fan-zhang; seongbin-park; baharan-mirzasoleiman; et al.

### EA-PVC-2026-0007

- Claim: 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.00673](https://arxiv.org/abs/2607.00673) Path Planning in Physically Viable World Models
- Locator: Abstract; 1 Introduction; 2 Related Work
- Evidence: 论文指出多数路径规划假设地图不变,只问 which path is best 而不问 mission 是否在指定物理变化下仍可行;PVWM 用 Gaussian splat 重建加 MPM 物理仿真生成 query-conditioned 修改场景,真实野外场地的洪水多严重度实验显示:仅在原始重建上规划看不到的长程路线失败与改线行为被暴露出来。
- Authors: su-ann-low; cheng-hsi-hsiao; xingjian-li; et al.

### EA-PVC-2026-0005

- Claim: 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.21161](https://arxiv.org/abs/2602.21161) ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking
- Locator: I Introduction; II-B LLM/VLM Based Robotic Operation; IV-D 2 Single-Agent ablation
- Evidence: 论文主张解耦视觉组件:由成熟视觉管线提供准确 3D 状态,LLM 只做 physical reasoning 并直接在 SE(3) 输出分阶段动作;single-agent 消融显示缺少阶段间验证时早期错误传播,前四块砖放置误差显著增大并频繁碰塌墙体,支持多阶段推理与角色分工的必要性。
- Authors: guangming-wang; qizhen-ying; yixiong-jing; et al.

### EA-PVC-2026-0002

- Claim: 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.03784](https://arxiv.org/abs/2606.03784) Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation
- Locator: 1 Introduction; 3.1 Exploring Effective Embodied Chain-of-Thought Signals; Appendix E Limitations and Future Work
- Evidence: 论文明确写到 enhanced perception and broader semantic coverage do not inherently guarantee better action generation;系统研究显示推理信号必须落到 end-effector motion、image-space trajectory 等动作相关表示;reasoning-as-prefix 慢且脆,长推理链在推理期误差复合;附录指出语言字段稳但欠规格、稠密 grounding 字段更可执行却更易受 detector error、calibration bias、occlusion 影响。
- Authors: nan-sun; yuan-zhang; yongkun-yang; et al.

### EA-SENSOR-2026-DQ-0006

- Claim: 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02840](https://arxiv.org/abs/2607.02840) TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training
- Locator: Abstract; 1 Introduction; 2 Related Work; 3 Method; 5 Conclusion and Limitations
- Evidence: 论文指出 VLA 在接触丰富任务中会因轻微接触扰动产生不可恢复失败，这些失败难以从视觉单独检测；TACO 用 tactile-aware world model 将真实 rollout 中的失败邻近状态转成想象的视触觉纠正片段和可执行纠正动作，在真实接触任务中相对 base policy 提升 44 个百分点成功率。
- Authors: shengbang-liu; yueru-jia; yuyang-yan; et al.

### EA-ALIGN-2026-0010

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: Abstract; Section 1 Introduction; Section 3.2 Inconsistency of Control Commands across Robots; Section 4 SPACE
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Authors: haeone-lee

## References

- `2601.09708` [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](https://arxiv.org/abs/2601.09708) (2026-01-14)
- `2602.21161` [ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking](https://arxiv.org/abs/2602.21161) (2026-02-24)
- `2605.00080` [World Model for Robot Learning: A Comprehensive Survey](https://arxiv.org/abs/2605.00080) (2026-04-30)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.03784` [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](https://arxiv.org/abs/2606.03784) (2026-06-02)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.09630` [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630) (2026-06-08)
- `2606.09740` [ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models](https://arxiv.org/abs/2606.09740) (2026-06-08)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2607.00673` [Path Planning in Physically Viable World Models](https://arxiv.org/abs/2607.00673) (2026-07-01)
- `2607.02642` [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.06564` [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07)
