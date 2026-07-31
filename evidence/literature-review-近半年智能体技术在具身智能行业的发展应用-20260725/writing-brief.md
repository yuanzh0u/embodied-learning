# Writing Brief: 近半年智能体技术在具身智能行业的发展应用

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近半年智能体技术在具身智能行业的发展应用
- Time range: 2026-01-25..2026-07-25
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-BIZ`
- Review mode: scoping
- Paper-level sources: 32 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 47

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-4D-READ-0013](evidence-appendix.md#ea-4d-read-0013)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `EA-DATA`: A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-tra... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-WMDATA-READ-0007](evidence-appendix.md#ea-wmdata-read-0007)) ⟷ 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- `EA-DATA`: Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow ta... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-WMDATA-READ-0008](evidence-appendix.md#ea-wmdata-read-0008)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `EA-DATA`: World-model training and post-training data should include dense corrective trajectories around failure-prone states, n... ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-WMDATA-READ-0009](evidence-appendix.md#ea-wmdata-read-0009)) ⟷ 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- `EA-EVAL`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-WMEVAL-READ-0001](evidence-appendix.md#ea-wmeval-read-0001)) ⟷ A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neura... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-WMEVAL-READ-0014](evidence-appendix.md#ea-wmeval-read-0014))
- `EA-EVAL`: Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, c... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-WMEVAL-READ-0003](evidence-appendix.md#ea-wmeval-read-0003)) ⟷ PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and pos... ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-WMEVAL-READ-0008](evidence-appendix.md#ea-wmeval-read-0008))
- `EA-EVAL`: GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulatio... ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-WMEVAL-READ-0005](evidence-appendix.md#ea-wmeval-read-0005)) ⟷ Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should ex... ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-WMEVAL-READ-0013](evidence-appendix.md#ea-wmeval-read-0013))
- `EA-EVAL`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinem... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-WMEVAL-READ-0007](evidence-appendix.md#ea-wmeval-read-0007)) ⟷ World-model training and post-training objectives should be tied to downstream action quality rather than intermediate... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMEVAL-READ-0015](evidence-appendix.md#ea-wmeval-read-0015))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (6 events)
- [`support`] A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horiz... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-WMDATA-READ-0007](evidence-appendix.md#ea-wmdata-read-0007))
- [`support`] World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-WMDATA-READ-0009](evidence-appendix.md#ea-wmdata-read-0009))
- [`support`] Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon futur... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-WMDATA-READ-0008](evidence-appendix.md#ea-wmdata-read-0008))
- [`support`] Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-4D-READ-0013](evidence-appendix.md#ea-4d-read-0013))
- [`conditional`] 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))

### EA-EVAL (12 events)
- [`support`] Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-WMEVAL-READ-0007](evidence-appendix.md#ea-wmeval-read-0007))
- [`support`] GEM-4D supports geometry-feature distillation as a way to make video world models more actionable for robot manipulation without adding inference-time cost. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-WMEVAL-READ-0005](evidence-appendix.md#ea-wmeval-read-0005))
- [`support`] Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information do... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-WMEVAL-READ-0003](evidence-appendix.md#ea-wmeval-read-0003))
- [`support`] τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-WMEVAL-READ-0001](evidence-appendix.md#ea-wmeval-read-0001))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-WMEVAL-READ-0010](evidence-appendix.md#ea-wmeval-read-0010))
- [`conditional`] A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-WMEVAL-READ-0014](evidence-appendix.md#ea-wmeval-read-0014))
- [`conditional`] Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-WMEVAL-READ-0011](evidence-appendix.md#ea-wmeval-read-0011))
- [`limit`] PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-WMEVAL-READ-0008](evidence-appendix.md#ea-wmeval-read-0008))
- [`limit`] World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMEVAL-READ-0015](evidence-appendix.md#ea-wmeval-read-0015))
- [`limit`] Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-WMEVAL-READ-0013](evidence-appendix.md#ea-wmeval-read-0013))
- [`gap`] Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-WMEVAL-READ-0006](evidence-appendix.md#ea-wmeval-read-0006))
- [`gap`] Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection. ([2605.29360](https://arxiv.org/abs/2605.29360) / [EA-WMEVAL-READ-0004](evidence-appendix.md#ea-wmeval-read-0004))

### EA-MODEL (29 events)
- [`support`] ALRM 将高层规划、执行与机器人 API 分层，并通过动作结果回传形成可修订计划的闭环。 ([2601.19510](https://arxiv.org/abs/2601.19510) / [EA-AGENT-2026-0001](evidence-appendix.md#ea-agent-2026-0001))
- [`support`] H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0001](evidence-appendix.md#ea-vlabreak-2026-0001))
- [`support`] 同一高层循环在真实 Mobipick 上运行，并在约一天内通过更换提示与技能绑定迁移到 Valdemar 仿真场景。 ([2602.13081](https://arxiv.org/abs/2602.13081) / [EA-AGENT-2026-0005](evidence-appendix.md#ea-agent-2026-0005))
- [`support`] RACAS 在三类差异显著的机器人上复用同一控制逻辑；适配只需更换机器人、动作和环境的提示配置。 ([2603.05621](https://arxiv.org/abs/2603.05621) / [EA-AGENT-2026-0011](evidence-appendix.md#ea-agent-2026-0011))
- [`support`] StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。 ([2603.12553](https://arxiv.org/abs/2603.12553) / [EA-VLABREAK-2026-0004](evidence-appendix.md#ea-vlabreak-2026-0004))
- [`support`] 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-ALIGN-READ-0015](evidence-appendix.md#ea-align-read-0015))
- [`support`] 具身智能体记忆可显式连接持久对象、场景状态、动作转移和可执行技能，并用前置条件与预期后果约束技能选择。 ([2606.29774](https://arxiv.org/abs/2606.29774) / [EA-AGENT-2026-0014](evidence-appendix.md#ea-agent-2026-0014))
- [`support`] 在五个真实桌面记忆任务上，结构化记忆相对关键帧检索把平均成功率从 56% 提至 84%，检索准确率从 68% 提至 98%，检索努力从 4.5 降至 1.3。 ([2606.29774](https://arxiv.org/abs/2606.29774) / [EA-AGENT-2026-0015](evidence-appendix.md#ea-agent-2026-0015))
- [`conditional`] 在该 56 指令仿真基准上，Claude-4.1-Opus 的 TaP 成功率为 93.5%，CaP 为 92.6%，但平均延迟由 33.44 秒增至 82.60 秒。 ([2601.19510](https://arxiv.org/abs/2601.19510) / [EA-AGENT-2026-0002](evidence-appendix.md#ea-agent-2026-0002))
- [`conditional`] 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0002](evidence-appendix.md#ea-vlabreak-2026-0002))
- [`conditional`] 该架构把 LLM 限制在高层决策和技能调用；真实部署的前提是平台已有完整低层栈、语义状态快照及结构化成功/失败信号。 ([2602.13081](https://arxiv.org/abs/2602.13081) / [EA-AGENT-2026-0004](evidence-appendix.md#ea-agent-2026-0004))
- [`conditional`] 在该实验中，情景记忆对任务成功率的作用因模型和任务而异，结论不确定；较稳定的收益是减少工具调用。 ([2603.03148](https://arxiv.org/abs/2603.03148) / [EA-AGENT-2026-0009](evidence-appendix.md#ea-agent-2026-0009))
- [`conditional`] 模型可在占位空间、已占用位置等工具失败后自行重规划，但恢复过程仍可能受幻觉影响而产生新的失败。 ([2603.03148](https://arxiv.org/abs/2603.03148) / [EA-AGENT-2026-0010](evidence-appendix.md#ea-agent-2026-0010))
- [`conditional`] 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 ([2603.12553](https://arxiv.org/abs/2603.12553) / [EA-VLABREAK-2026-0005](evidence-appendix.md#ea-vlabreak-2026-0005))
- [`conditional`] ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-ALIGN-READ-0006](evidence-appendix.md#ea-align-read-0006))
- [`limit`] 该研究不能证明真实机器人部署可靠性，因为主要评测使用占位位姿和动作序列代理，作者也把真实机器人与感知整合列为后续工作。 ([2601.19510](https://arxiv.org/abs/2601.19510) / [EA-AGENT-2026-0003](evidence-appendix.md#ea-agent-2026-0003))
- [`limit`] H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0003](evidence-appendix.md#ea-vlabreak-2026-0003))
- [`limit`] 长时执行仍会出现陈旧世界状态、提示约束违背、非确定性选择和不规则事件检查，因此灵活性没有转化为可预测可靠性。 ([2602.13081](https://arxiv.org/abs/2602.13081) / [EA-AGENT-2026-0006](evidence-appendix.md#ea-agent-2026-0006))
- [`limit`] 基于轮询的事件检测无法在长动作中即时抢占；物理安全需要并发监控、可取消技能或把动作切成可中断检查点。 ([2602.13081](https://arxiv.org/abs/2602.13081) / [EA-AGENT-2026-0007](evidence-appendix.md#ea-agent-2026-0007))
- [`limit`] LLM 机器人智能体会在任务未真实完成时相信自己成功；这种误报会直接污染以自报结果标注的情景记忆。 ([2603.03148](https://arxiv.org/abs/2603.03148) / [EA-AGENT-2026-0008](evidence-appendix.md#ea-agent-2026-0008))
- [`limit`] 当前系统约每 5–10 秒才执行一个动作；作者认为这种逐步推理成本让长时接触操作实验慢到不可行。 ([2603.05621](https://arxiv.org/abs/2603.05621) / [EA-AGENT-2026-0012](evidence-appendix.md#ea-agent-2026-0012))
- [`limit`] 缺少显式深度使 VLM 对碰撞风险的判断过度或不足自信，说明自然语言视觉接口不能替代安全几何感知。 ([2603.05621](https://arxiv.org/abs/2603.05621) / [EA-AGENT-2026-0013](evidence-appendix.md#ea-agent-2026-0013))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- [`limit`] 该记忆路线尚未证明可变形物和强感知/状态漂移下的鲁棒性，模板库覆盖是重要边界。 ([2606.29774](https://arxiv.org/abs/2606.29774) / [EA-AGENT-2026-0016](evidence-appendix.md#ea-agent-2026-0016))
- [`limit`] Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- [`limit`] Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-ALIGN-READ-0009](evidence-appendix.md#ea-align-read-0009))
- [`limit`] 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0006](evidence-appendix.md#ea-vlabreak-2026-0006))
- [`limit`] 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4D-READ-0011](evidence-appendix.md#ea-4d-read-0011))
- `conditional` A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-WMEVAL-READ-0014](evidence-appendix.md#ea-wmeval-read-0014))
- `conditional` Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-WMEVAL-READ-0011](evidence-appendix.md#ea-wmeval-read-0011))
- `limit` PredictiveGraphs is bounded by simplified independence assumptions, perception ambiguity among similar objects, and possible LLM hallucinations during verification and planning. ([2605.00121](https://arxiv.org/abs/2605.00121) / [EA-WMEVAL-READ-0008](evidence-appendix.md#ea-wmeval-read-0008))
- `limit` World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-WMEVAL-READ-0015](evidence-appendix.md#ea-wmeval-read-0015))
- `limit` Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-WMEVAL-READ-0013](evidence-appendix.md#ea-wmeval-read-0013))
- `gap` Pri4R leaves open whether 4D point-track supervision should be used at larger pretraining scale or with explicit test-time geometric inputs. ([2603.01549](https://arxiv.org/abs/2603.01549) / [EA-WMEVAL-READ-0006](evidence-appendix.md#ea-wmeval-read-0006))
- `gap` Robotic world-model evaluation should move beyond visual fidelity toward action-conditioned reliability, including physical adherence, action-following fidelity, and optimism-bias detection. ([2605.29360](https://arxiv.org/abs/2605.29360) / [EA-WMEVAL-READ-0004](evidence-appendix.md#ea-wmeval-read-0004))
- `conditional` 在该 56 指令仿真基准上，Claude-4.1-Opus 的 TaP 成功率为 93.5%，CaP 为 92.6%，但平均延迟由 33.44 秒增至 82.60 秒。 ([2601.19510](https://arxiv.org/abs/2601.19510) / [EA-AGENT-2026-0002](evidence-appendix.md#ea-agent-2026-0002))
- `conditional` 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0002](evidence-appendix.md#ea-vlabreak-2026-0002))
- `conditional` 该架构把 LLM 限制在高层决策和技能调用；真实部署的前提是平台已有完整低层栈、语义状态快照及结构化成功/失败信号。 ([2602.13081](https://arxiv.org/abs/2602.13081) / [EA-AGENT-2026-0004](evidence-appendix.md#ea-agent-2026-0004))
- `conditional` 在该实验中，情景记忆对任务成功率的作用因模型和任务而异，结论不确定；较稳定的收益是减少工具调用。 ([2603.03148](https://arxiv.org/abs/2603.03148) / [EA-AGENT-2026-0009](evidence-appendix.md#ea-agent-2026-0009))
- `conditional` 模型可在占位空间、已占用位置等工具失败后自行重规划，但恢复过程仍可能受幻觉影响而产生新的失败。 ([2603.03148](https://arxiv.org/abs/2603.03148) / [EA-AGENT-2026-0010](evidence-appendix.md#ea-agent-2026-0010))
- `conditional` 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 ([2603.12553](https://arxiv.org/abs/2603.12553) / [EA-VLABREAK-2026-0005](evidence-appendix.md#ea-vlabreak-2026-0005))
- `conditional` ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-ALIGN-READ-0006](evidence-appendix.md#ea-align-read-0006))
- `limit` 该研究不能证明真实机器人部署可靠性，因为主要评测使用占位位姿和动作序列代理，作者也把真实机器人与感知整合列为后续工作。 ([2601.19510](https://arxiv.org/abs/2601.19510) / [EA-AGENT-2026-0003](evidence-appendix.md#ea-agent-2026-0003))
- `limit` H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0003](evidence-appendix.md#ea-vlabreak-2026-0003))
- `limit` 长时执行仍会出现陈旧世界状态、提示约束违背、非确定性选择和不规则事件检查，因此灵活性没有转化为可预测可靠性。 ([2602.13081](https://arxiv.org/abs/2602.13081) / [EA-AGENT-2026-0006](evidence-appendix.md#ea-agent-2026-0006))
- `limit` 基于轮询的事件检测无法在长动作中即时抢占；物理安全需要并发监控、可取消技能或把动作切成可中断检查点。 ([2602.13081](https://arxiv.org/abs/2602.13081) / [EA-AGENT-2026-0007](evidence-appendix.md#ea-agent-2026-0007))
- `limit` LLM 机器人智能体会在任务未真实完成时相信自己成功；这种误报会直接污染以自报结果标注的情景记忆。 ([2603.03148](https://arxiv.org/abs/2603.03148) / [EA-AGENT-2026-0008](evidence-appendix.md#ea-agent-2026-0008))
- `limit` 当前系统约每 5–10 秒才执行一个动作；作者认为这种逐步推理成本让长时接触操作实验慢到不可行。 ([2603.05621](https://arxiv.org/abs/2603.05621) / [EA-AGENT-2026-0012](evidence-appendix.md#ea-agent-2026-0012))
- `limit` 缺少显式深度使 VLM 对碰撞风险的判断过度或不足自信，说明自然语言视觉接口不能替代安全几何感知。 ([2603.05621](https://arxiv.org/abs/2603.05621) / [EA-AGENT-2026-0013](evidence-appendix.md#ea-agent-2026-0013))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- `limit` 该记忆路线尚未证明可变形物和强感知/状态漂移下的鲁棒性，模板库覆盖是重要边界。 ([2606.29774](https://arxiv.org/abs/2606.29774) / [EA-AGENT-2026-0016](evidence-appendix.md#ea-agent-2026-0016))
- `limit` Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- `limit` Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- `limit` TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-ALIGN-READ-0009](evidence-appendix.md#ea-align-read-0009))
- `limit` 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0006](evidence-appendix.md#ea-vlabreak-2026-0006))
- `limit` 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))

## Writer handoff

- Use `$embodied-ai-review-writer` with this brief, the accepted evidence JSONL, and `evidence-appendix.md`.
- The writer loads only the requested style reference and drafts each style independently from this evidence model.
- Generate `trace-map.json`, then pass the writer's editorial quality audit before settlement.

## 引用速查

- **正文引用 = arXiv 论文链接**:`[2606.13877](https://arxiv.org/abs/2606.13877)` 或 `[SIEVE](https://arxiv.org/abs/2607.06442)`。读者点开即达论文。
- 事件级溯源留给 appendix:成稿正文不放 `evidence-appendix.md#...` 事件锚点;需要精确定位(章节/立场/置信)时,读者从 References 或 appendix 查。
- 本简报中每条证据给出 `论文链接 / 事件链接` 对:写作时**取前者入正文**,后者供你核对 locator 与 stance。
- Citation density and visible source format are style-specific; do not force a full bibliography into Xiaohongshu prose.
- 完整证据条目在 [evidence-appendix.md](evidence-appendix.md);事件映射由 `trace-map.json` 保存。
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`
