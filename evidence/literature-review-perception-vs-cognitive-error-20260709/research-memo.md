# 具身数据感知误差与认知误差的区别：近半年论文研究备忘录

## 范围

- 时间范围：2026-01-09..2026-07-09，按当前工作区日期 2026-07-09 回看最近半年。
- 知识单元：EA-DATA、EA-SENSOR、EA-EVAL、EA-MODEL，辅以 ERR-PATTERN 的误差账本语言。
- 证据状态：感知误差部分复用本地 accepted evidence run `literature-review-perception-error-traceability-20260708`；认知误差部分使用本次 arXiv 浏览检索得到的 paper-level 候选，尚未全部升级为 evidence JSONL。
- 检索计划：`query-plan.md` 与 `query-plan.json` 已保存在同目录。

## 中心结论

在近半年具身智能论文里，“感知误差”和“认知误差”不是按模型模块粗暴切开，而是按**第一处可证伪偏离点**切开：

- 感知误差：世界状态没有被正确观测、对齐或记录。典型问题是 2D 视觉丢 3D 几何、接触/力/滑移不可见、多模态时间同步错误、动作-状态字段不一致、episode 质量差。
- 认知误差：可用状态已经足够，但系统对任务、约束、子目标、恢复阶段或未来后果的理解/规划错了。典型问题是语言指令 grounding 错、长程任务分解错、CoT 与动作耦合不稳、world model 对可执行未来判断错、failure mode 识别错。

一句话：**感知误差问“机器人看到/记录到的世界对不对”；认知误差问“基于这个世界表征，它理解和打算做的事对不对”。**

## 对照表

| 维度 | 感知误差 | 认知误差 |
|---|---|---|
| 误差对象 | 观测、状态估计、3D/触觉/力、同步、标定、schema | 任务理解、语义消歧、子目标分解、规划、恢复策略、未来预测 |
| 第一处偏离 | 原始世界到状态表征 | 状态表征到意图/计划/动作选择 |
| 典型表现 | 看错物体位姿、接触不可见、时间戳错位、动作-state 不一致 | 看对了但拿错、顺序错、忽略约束、恢复阶段判断错、长程计划不可行 |
| 论文关键词 | 3D geometry、tactile/force、visuotactile、data quality、teleoperation telemetry | VLA reasoning、embodied CoT、latent planning、failure recovery、world-model planning |
| 诊断指标 | 可见率、点云/位姿误差、接触检测、同步误差、丢帧、stall/smoothness | 子目标正确率、instruction following、plan feasibility、failure-mode accuracy、rollout consistency、恢复成功率 |
| 治理方式 | 多模态冗余、标定/同步审计、episode 级质量反馈、触觉/力补充 | reasoning supervision、latent planning、任务分解评测、failure-conditioned recovery、world-model 反事实评估 |

## 近半年证据脉络

### 1. 感知误差：从“视觉看错”扩展为“可观测性与数据记录缺口”

Lift3D-VLA 指出物理操作需要几何理解和空间推理，当前 3D 编码和数据可得性会带来空间信息损失；它用显式点云推理和未来几何演化预测改善动态操作。TACO 则把接触任务里的失败定位为视觉难以单独检测的局部接触扰动，并指出 vision-only world model 可能生成视觉合理但接触不一致的轨迹。HapTile、TacForeSight 进一步把触觉、力/力矩、同步 visuotactile 数据变成 contact-rich manipulation 的必要证据层。

这类论文把“感知误差”从 image perception failure 扩成 embodied observability failure：关键状态如果没有被传感器覆盖，后续再强的认知模块也只能在错误状态上推理。

### 2. 数据/episode 误差：感知误差常藏在示教质量和日志结构里

DQAF 说明遥操作 episode 不能只按成功/失败验收；任务进度、运动平滑性、停顿、关节极限等遥测信号可以解释为什么一条成功示教仍对训练有害。已有本地 evidence run 还显示，HapTile 强调 timestamp gaps、action-state consistency、episode-level split，tau0-WM 用 modality-specific supervision masks 区分机器人数据、UMI 数据和 egocentric video 的监督可靠性。

这说明“感知误差”有时不是传感器瞬时读错，而是数据链路把不同模态、动作字段或监督强度混成了伪真值。

### 3. 认知误差：从“想得更多”变成“推理必须接到可执行动作”

Fast-ThinkAct 把 VLA 推理建模为 latent planning，目标是在保持长程规划、few-shot adaptation 和 failure recovery 的同时降低显式 CoT 延迟。Revisiting Embodied CoT 则更关键：高层语义理解必须落到 end-effector motion、image-space trajectory 等具体动作指导，高层推理本身只带来有限收益；把显式 CoT 当 autoregressive action prefix 还会引入 compounding inference errors 和 reasoning-action coupling 不稳定。

这给“认知误差”一个清晰定义：不是不会描述场景，而是不能把语义、空间和任务进度稳定地转换成可执行控制信号。

### 4. failure recovery 是区分两类误差的实验场

ReCoVLA 把高层 failure understanding 与低层 corrective control 分开：外部 VLM 只推断 failure mode 和 recovery stage，并选择结构化 reward，而不是直接生成动作。ProbeAct 则同时用 VLA hidden-state probe 估计 3D 目标位置、用 gripper/end-effector 信号检测 grasp/transport/placement failures，再用控制屏障函数做最小动作修正。

这两篇很适合作为边界案例：如果 failure detector 依赖 3D 位置、gripper 信号、接触状态，那是感知/状态层；如果 VLM 把失败阶段、恢复目标或 reward component 选错，那是认知/任务层。

### 5. world model 位于感知与认知之间

World Model for Robot Learning 总结了 world model 在 policy learning、planning、simulation、evaluation、data generation 中的角色。GigaWorld-1 进一步指出，用 world model 评估机器人策略时，短期视觉真实感不如 long-horizon、action-faithful rollout consistency 重要。Path Planning in Physically Viable World Models 展示了另一类认知错误：旧地图感知本身可能没错，但如果规划没有考虑未来地形变化，路线会在执行时变成不可达或不安全。

因此 world model 既可能产生感知型错误（预测的物理状态不真实），也可能产生认知型错误（反事实评估或计划选择错）。

## 建议立题

可把题目定为：

**具身误差分层与可归因评测：区分观测缺口、数据链路缺陷与任务推理失败**

三个核心研究问题：

1. 当机器人失败时，第一处可证伪偏离发生在观测/记录、状态 grounding、任务理解、计划生成、控制执行，还是闭环恢复？
2. 哪些 episode 日志字段能把“感知失败”与“认知失败”分开，而不是只给一个成功率？
3. 触觉/力/3D/world model/reasoning trace 哪些证据真正提高闭环诊断和恢复，而不是只提升离线指标？

## 最小实验设计

1. 构造同一批任务的四类扰动：视觉遮挡/光照、接触滑移/力扰动、语言目标歧义、长程子目标顺序变化。
2. 对每次失败记录多层日志：RGB/3D/触觉/力、timestamp、action-state consistency、subgoal、reasoning trace、world-model rollout、控制器状态。
3. 做 error attribution label：perception/data、grounding、planning/cognition、control、mixed。
4. 评估诊断器是否能预测正确恢复动作，而不只是预测失败类别。

## 主要参考论文

- Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation, arXiv:2607.06564.
- TACO: TActile World Model as a Self-COrrector for Scalable VLA Post-Training, arXiv:2607.02840.
- Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection, arXiv:2605.26349.
- HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning, arXiv:2606.04825.
- TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation, arXiv:2606.11184.
- Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning, arXiv:2601.09708.
- Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation, arXiv:2606.03784.
- ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies, arXiv:2606.09630.
- ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models, arXiv:2606.09740.
- ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking, arXiv:2602.21161.
- World Model for Robot Learning: A Comprehensive Survey, arXiv:2605.00080.
- GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation, arXiv:2607.02642.
- Path Planning in Physically Viable World Models, arXiv:2607.00673.

