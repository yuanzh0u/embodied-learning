# 具身数据感知误差与认知误差的区别

## 研究范围

- 时间范围:2026-01-09..2026-07-09(近半年)。
- 证据范围:15 条正文级 evidence events——7 条本次晋升的认知误差侧论文(EA-PVC 系列事件),8 条复用自感知误差溯源 run 的感知侧证据。
- 覆盖知识单元:`EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `EA-MODEL`;误差账本语言来自 `ERR-PATTERN`。
- 完整证据条目见 [evidence-appendix.md](evidence-appendix.md);检索计划与晋升 digest 存于同名 work/ 目录。

## 中心判断

近半年论文对"感知误差 vs 认知误差"给出的最有解释力的切分,不是按模型模块(视觉编码器 vs 语言头),而是按**第一处可证伪偏离点**:

- **感知误差**:世界状态没有被正确观测、对齐或记录——2D 丢 3D 几何([Lift3D-VLA](https://arxiv.org/abs/2607.06564))、接触不可见([TACO](https://arxiv.org/abs/2607.02840))、时间戳与动作-状态错位([HapTile](https://arxiv.org/abs/2606.04825))、episode 遥测缺失([DQAF](https://arxiv.org/abs/2605.26349))。
- **认知误差**:可用状态已经足够,但系统对任务、约束、恢复阶段或未来后果的理解/规划错了——CoT 与动作耦合不稳([Revisiting ECoT](https://arxiv.org/abs/2606.03784))、失败模式判断错([ReCoVLA](https://arxiv.org/abs/2606.09630))、对未来世界状态不做 what-if 推理([PVWM](https://arxiv.org/abs/2607.00673))。

一句话:**感知误差问"机器人看到/记录到的世界对不对";认知误差问"基于这个世界表征,它理解和打算做的事对不对"。**

这个切分之所以成立,是因为近半年出现了能把两层**实验性分开**的证据——最典型的是 [ProbeAct](https://arxiv.org/abs/2606.09740):probing 实验显示扰动场景下 VLA 的视觉骨干仍保持准确的空间表征,失败瓶颈只在动作头塌缩回记忆轨迹。感知对了、行为错了,两层解耦从推测变成了可测量的事实(inference;综合 [EA-PVC-2026-0004](evidence-appendix.md#ea-pvc-2026-0004) 与 [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))。

## 四个派生张力

### 1. 感知增强 vs 动作生成:更好的"看"不自动带来更好的"做"

[Revisiting ECoT](https://arxiv.org/abs/2606.03784) 系统研究的第一句结论就是:enhanced perception and broader semantic coverage do not inherently guarantee better action generation。高层语义推理必须转译成 end-effector motion、image-space trajectory 等动作相关表示才有用;把显式 CoT 当动作前缀会引入 compounding errors。同一方向上,[Fast-ThinkAct](https://arxiv.org/abs/2601.09708) 证明认知处理可以压缩为 latent 推理而保持长程规划与失败恢复——说明"认知层"是一个可独立优化、可压缩的处理阶段,而不是感知的附属品。

结论:感知与认知之间存在一个**转译界面**(语义→动作表示),大量"认知误差"实际发生在这个界面上,而不是理解本身。

### 2. 感知对了 vs 执行错了:解耦的直接证据

[ProbeAct](https://arxiv.org/abs/2606.09740) 的 probing 证据是本次证据集里对两类误差最锋利的区分:视觉骨干维持准确空间表征、动作头塌缩(memory trap)。它的工程含义同样清晰——既然内部感知没坏,恢复就不需要外部 3D 传感器,从 hidden states 提取几何参照 + 最小动作修正即可。反过来,[Revisiting ECoT](https://arxiv.org/abs/2606.03784) 的附录提醒:dense grounding 字段(boxes、gripper 位置)本身受 detector error、calibration bias、occlusion 污染——**认知层的输入质量仍受感知层制约**,两层可区分但不独立。

结论:诊断顺序应当是"先用 probing/遥测确认感知层是否保真,再归因认知层",而不是从表象猜。

### 3. 失败恢复:两类误差最好的实验场

恢复任务天然要求区分"哪里错了"。[ReCoVLA](https://arxiv.org/abs/2606.09630) 把认知层(VLM 只推断 failure mode、recovery stage、reward 选择)与控制层(residual 纠正)显式分开,其 Limitations 把 VLM failure-classification mistakes 与 perception errors 并列为独立失败来源——认知误差第一次在系统设计里有了自己的"账户"。[ActionReasoning](https://arxiv.org/abs/2602.21161) 从反方向补充:假设感知已准确、让 LLM 专注 3D 动作推理确实可行且省数据,但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。感知侧证据同样支持这个实验场定位:[TacForeSight](https://arxiv.org/abs/2606.11184) 表明学恢复必须显式采集 recovery interaction data——**数据里没有恢复,认知层就无从学习恢复**。

结论:恢复失败的归因链是"感知层(状态可见吗)→ 数据层(恢复数据存在吗)→ 认知层(失败阶段判对了吗)→ 控制层(纠正可执行吗)",四层各有独立的证据字段。

### 4. 世界模型横跨两层:预测误差是感知型,评估误差是认知型

[世界模型综述](https://arxiv.org/abs/2605.00080) 把 reactive VLA 的长程推理与误差复合问题归因于缺少显式预测结构,并把世界模型的 evaluator 角色(候选动作 rollout 排序/拒绝/安全过滤)单列一节——这属于认知层验证。但同一综述也指出 pixel-based rollout 的长程误差积累是世界模型自身的感知型缺陷。[GigaWorld-1](https://arxiv.org/abs/2607.02642) 给出评估侧的判据:evaluator 可靠性取决于长程动作忠实的 rollout 一致性,不是视觉真实感。[PVWM](https://arxiv.org/abs/2607.00673) 展示了纯认知型规划误差的干净样本:重建地图没错,但不对"洪水后地形"做 what-if 推理,路线在执行时不可达——感知无过错,规划有责任。

结论:评估世界模型时要分别记账——预测保真度(感知型)与决策有效性(认知型)各自有指标,混在一个分数里会掩盖问题来源。

## 误差账本:两类误差的可操作区分

| 判据 | 感知误差 | 认知误差 |
|---|---|---|
| 第一处偏离 | 原始世界 → 状态表征 | 状态表征 → 意图/计划/动作选择 |
| 典型证据字段 | 关键点可见率、接触事件、时间同步误差、action-state 一致性、episode 遥测 | probing 保真度、failure-mode 分类正确率、子目标/阶段判断、plan feasibility、rollout 一致性 |
| 快速检验 | 换传感器/补模态后失败是否消失 | 感知输入不变、换推理/规划头后失败是否消失 |
| 治理手段 | 多模态冗余、同步标定审计、episode 质量反馈([DQAF](https://arxiv.org/abs/2605.26349))、监督可靠性分级([tau0-WM](https://arxiv.org/abs/2606.01027)) | 推理-动作转译监督([Revisiting ECoT](https://arxiv.org/abs/2606.03784))、阶段验证([ActionReasoning](https://arxiv.org/abs/2602.21161))、失败条件化恢复([ReCoVLA](https://arxiv.org/abs/2606.09630))、what-if 评估([PVWM](https://arxiv.org/abs/2607.00673)) |
| 跨本体附注 | 传感器配置差异 | 动作语义差异([SPACE](https://arxiv.org/abs/2606.24049)):recorded action 不是通用监督信号,错配会伪装成任一类误差 |

## 最短结论

感知误差与认知误差的区别,不在"哪个模块出错",而在**第一处可证伪偏离发生在世界→表征,还是表征→行动**。近半年文献的实质进展是让这条边界可测量:probing 能证明感知保真时行为仍错([ProbeAct](https://arxiv.org/abs/2606.09740)),恢复系统能把失败判断与纠正执行分账([ReCoVLA](https://arxiv.org/abs/2606.09630)),世界模型评估能把预测保真与决策有效分账([GigaWorld-1](https://arxiv.org/abs/2607.02642))。对数据工作的含义:误差账本要同时记录两层的证据字段,并保留"感知输入不变、只换认知头"这类对照实验的可能性——否则所有失败都会被记到最显眼的那一层。

## References

- [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07) — 证据: [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002)
- [TACO: TActile World Model as a Self-COrrector for Scalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03) — 证据: [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006)
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09) — 证据: [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014)
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset](https://arxiv.org/abs/2606.04825) (2026-06-04) — 证据: [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018)
- [Closing the Loop in Teleoperation (DQAF)](https://arxiv.org/abs/2605.26349) (2026-05-27) — 证据: [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002)
- [tau0-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31) — 证据: [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010)
- [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23) — 证据: [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010)
- [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02) — 证据: [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004)
- [Fast-ThinkAct: Efficient VLA Reasoning via Verbalizable Latent Planning](https://arxiv.org/abs/2601.09708) (2026-01-14) — 证据: [EA-PVC-2026-0001](evidence-appendix.md#ea-pvc-2026-0001)
- [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](https://arxiv.org/abs/2606.03784) (2026-06-02) — 证据: [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002)
- [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in VLA Policies](https://arxiv.org/abs/2606.09630) (2026-06-08) — 证据: [EA-PVC-2026-0003](evidence-appendix.md#ea-pvc-2026-0003)
- [ProbeAct: Probe-Guided Training-Free Failure Recovery in VLA Models](https://arxiv.org/abs/2606.09740) (2026-06-08) — 证据: [EA-PVC-2026-0004](evidence-appendix.md#ea-pvc-2026-0004)
- [ActionReasoning: Robot Action Reasoning in 3D Space with LLM](https://arxiv.org/abs/2602.21161) (2026-02-24) — 证据: [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005)
- [World Model for Robot Learning: A Comprehensive Survey](https://arxiv.org/abs/2605.00080) (2026-04-30) — 证据: [EA-PVC-2026-0006](evidence-appendix.md#ea-pvc-2026-0006)
- [Path Planning in Physically Viable World Models](https://arxiv.org/abs/2607.00673) (2026-07-01) — 证据: [EA-PVC-2026-0007](evidence-appendix.md#ea-pvc-2026-0007)
