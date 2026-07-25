# Writing Brief: 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进
- Time range: 2025-07-20..2026-07-20
- Knowledge IDs: `EA-SENSOR`, `EA-MODEL`, `EA-ALIGN`, `EA-XEMBODIMENT`, `EA-DATA`
- Review mode: scoping
- Paper-level sources: 42 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 56

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0007](evidence-appendix.md#ea-ego-2026-0007)) ⟷ 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- `EA-DATA`: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-READ-0002](evidence-appendix.md#ea-twm-read-0002)) ⟷ Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- `EA-DATA`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-READ-0003](evidence-appendix.md#ea-twm-read-0003)) ⟷ Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- `EA-DATA`: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-READ-0004](evidence-appendix.md#ea-twm-read-0004)) ⟷ Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- `EA-DATA`: 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-READ-0005](evidence-appendix.md#ea-twm-read-0005)) ⟷ Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。 ([2607.03828](https://arxiv.org/abs/2607.03828) / [EA-EGO-2026-0019](evidence-appendix.md#ea-ego-2026-0019))
- `EA-DATA`: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-READ-0006](evidence-appendix.md#ea-twm-read-0006)) ⟷ 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-TWM-READ-0009](evidence-appendix.md#ea-twm-read-0009))
- `EA-DATA`: TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 ([2604.07335](https://arxiv.org/abs/2604.07335) / [EA-TWM-READ-0008](evidence-appendix.md#ea-twm-read-0008)) ⟷ 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))
- `EA-DATA`: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 ([2606.18043](https://arxiv.org/abs/2606.18043) / [EA-TWM-READ-0015](evidence-appendix.md#ea-twm-read-0015)) ⟷ 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0008](evidence-appendix.md#ea-ego-2026-0008))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (25 events)
- [`support`] 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0007](evidence-appendix.md#ea-ego-2026-0007))
- [`support`] TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 ([2604.07335](https://arxiv.org/abs/2604.07335) / [EA-TWM-READ-0008](evidence-appendix.md#ea-twm-read-0008))
- [`support`] 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-READ-0005](evidence-appendix.md#ea-twm-read-0005))
- [`support`] 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-READ-0002](evidence-appendix.md#ea-twm-read-0002))
- [`support`] 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-READ-0006](evidence-appendix.md#ea-twm-read-0006))
- [`support`] 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-READ-0003](evidence-appendix.md#ea-twm-read-0003))
- [`support`] 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-READ-0004](evidence-appendix.md#ea-twm-read-0004))
- [`support`] Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 ([2606.18043](https://arxiv.org/abs/2606.18043) / [EA-TWM-READ-0015](evidence-appendix.md#ea-twm-read-0015))
- [`conditional`] VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-READ-0001](evidence-appendix.md#ea-twm-read-0001))
- [`conditional`] 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0008](evidence-appendix.md#ea-ego-2026-0008))
- [`conditional`] 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-READ-0007](evidence-appendix.md#ea-twm-read-0007))
- [`conditional`] 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0017](evidence-appendix.md#ea-ego-2026-0017))
- [`conditional`] 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0018](evidence-appendix.md#ea-ego-2026-0018))
- [`conditional`] 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-TWM-READ-0014](evidence-appendix.md#ea-twm-read-0014))
- [`conditional`] 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-TWM-READ-0010](evidence-appendix.md#ea-twm-read-0010))
- [`conditional`] 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-TWM-READ-0011](evidence-appendix.md#ea-twm-read-0011))
- [`conditional`] 显式 contact geometry 在该系统中显著减少滑移并提高成功率，说明接触结构是 Ego-centric 数据转成可执行监督的独立质量维度。 ([2607.03828](https://arxiv.org/abs/2607.03828) / [EA-EGO-2026-0020](evidence-appendix.md#ea-ego-2026-0020))
- [`limit`] 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- [`limit`] Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- [`limit`] Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- [`limit`] Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- [`limit`] 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-TWM-READ-0009](evidence-appendix.md#ea-twm-read-0009))
- [`limit`] Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。 ([2607.03828](https://arxiv.org/abs/2607.03828) / [EA-EGO-2026-0019](evidence-appendix.md#ea-ego-2026-0019))
- [`limit`] 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))
- [`gap`] 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 ([2607.07196](https://arxiv.org/abs/2607.07196) / [EA-TWM-READ-0013](evidence-appendix.md#ea-twm-read-0013))

### EA-MODEL (26 events)
- [`support`] Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the evaluated tasks. ([2512.11047](https://arxiv.org/abs/2512.11047) / [EA-LOCOMANIP-2026-0006](evidence-appendix.md#ea-locomanip-2026-0006))
- [`support`] 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-ALIGN-READ-0013](evidence-appendix.md#ea-align-read-0013))
- [`support`] H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0001](evidence-appendix.md#ea-vlabreak-2026-0001))
- [`support`] StructVLA 把稠密视频未来压缩成由夹爪转换和运动转折点定义的稀疏结构化帧，再将这种规划表征迁移到低层动作生成。 ([2603.12553](https://arxiv.org/abs/2603.12553) / [EA-VLABREAK-2026-0004](evidence-appendix.md#ea-vlabreak-2026-0004))
- [`support`] Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to 0.85. ([2604.27224](https://arxiv.org/abs/2604.27224) / [EA-LOCOMANIP-2026-0012](evidence-appendix.md#ea-locomanip-2026-0012))
- [`support`] 纯反应式 VLA 在复杂物理环境中仍受长时程推理、时序归因和误差累积限制，这构成引入显式预测结构的主要动机。 ([2605.00080](https://arxiv.org/abs/2605.00080) / [EA-ALIGN-READ-0014](evidence-appendix.md#ea-align-read-0014))
- [`support`] DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-ALIGN-READ-0012](evidence-appendix.md#ea-align-read-0012))
- [`support`] 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-ALIGN-READ-0015](evidence-appendix.md#ea-align-read-0015))
- [`support`] Cross-embodiment VLA alignment is difficult partly because shared high-level task cognition must be connected to platform-specific low-level state and action spaces. ([2606.30552](https://arxiv.org/abs/2606.30552) / [EA-ALIGN-READ-0005](evidence-appendix.md#ea-align-read-0005))
- [`support`] In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. ([2607.10132](https://arxiv.org/abs/2607.10132) / [EA-LOCOMANIP-2026-0021](evidence-appendix.md#ea-locomanip-2026-0021))
- [`conditional`] 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0002](evidence-appendix.md#ea-vlabreak-2026-0002))
- [`conditional`] ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-ALIGN-READ-0010](evidence-appendix.md#ea-align-read-0010))
- [`conditional`] On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively. ([2603.03279](https://arxiv.org/abs/2603.03279) / [EA-LOCOMANIP-2026-0018](evidence-appendix.md#ea-locomanip-2026-0018))
- [`conditional`] 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 ([2603.12553](https://arxiv.org/abs/2603.12553) / [EA-VLABREAK-2026-0005](evidence-appendix.md#ea-vlabreak-2026-0005))
- [`conditional`] τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-ALIGN-READ-0011](evidence-appendix.md#ea-align-read-0011))
- [`conditional`] ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-ALIGN-READ-0006](evidence-appendix.md#ea-align-read-0006))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-ALIGN-READ-0007](evidence-appendix.md#ea-align-read-0007))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-ALIGN-READ-0008](evidence-appendix.md#ea-align-read-0008))
- [`conditional`] A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-READ-0002](evidence-appendix.md#ea-align-read-0002))
- [`limit`] H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0003](evidence-appendix.md#ea-vlabreak-2026-0003))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- [`limit`] Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- [`limit`] Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-ALIGN-READ-0009](evidence-appendix.md#ea-align-read-0009))
- [`limit`] 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0006](evidence-appendix.md#ea-vlabreak-2026-0006))
- [`limit`] 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))

### EA-SENSOR (5 events)
- [`support`] 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 ([2606.28899](https://arxiv.org/abs/2606.28899) / [EA-SENSORERR-READ-0010](evidence-appendix.md#ea-sensorerr-read-0010))
- [`support`] RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 ([2606.29384](https://arxiv.org/abs/2606.29384) / [EA-SENSORERR-READ-0011](evidence-appendix.md#ea-sensorerr-read-0011))
- [`support`] 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 ([2607.07287](https://arxiv.org/abs/2607.07287) / [EA-SENSORERR-READ-0012](evidence-appendix.md#ea-sensorerr-read-0012))
- [`conditional`] 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-SENSORERR-READ-0007](evidence-appendix.md#ea-sensorerr-read-0007))
- [`conditional`] 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-SENSORERR-READ-0004](evidence-appendix.md#ea-sensorerr-read-0004))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-READ-0001](evidence-appendix.md#ea-twm-read-0001))
- `conditional` 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0008](evidence-appendix.md#ea-ego-2026-0008))
- `conditional` 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-READ-0007](evidence-appendix.md#ea-twm-read-0007))
- `conditional` 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0017](evidence-appendix.md#ea-ego-2026-0017))
- `conditional` 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0018](evidence-appendix.md#ea-ego-2026-0018))
- `conditional` 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-TWM-READ-0014](evidence-appendix.md#ea-twm-read-0014))
- `conditional` 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-TWM-READ-0010](evidence-appendix.md#ea-twm-read-0010))
- `conditional` 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-TWM-READ-0011](evidence-appendix.md#ea-twm-read-0011))
- `conditional` 显式 contact geometry 在该系统中显著减少滑移并提高成功率，说明接触结构是 Ego-centric 数据转成可执行监督的独立质量维度。 ([2607.03828](https://arxiv.org/abs/2607.03828) / [EA-EGO-2026-0020](evidence-appendix.md#ea-ego-2026-0020))
- `limit` 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- `limit` Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- `limit` Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- `limit` Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- `limit` 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-TWM-READ-0009](evidence-appendix.md#ea-twm-read-0009))
- `limit` Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。 ([2607.03828](https://arxiv.org/abs/2607.03828) / [EA-EGO-2026-0019](evidence-appendix.md#ea-ego-2026-0019))
- `limit` 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))
- `gap` 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 ([2607.07196](https://arxiv.org/abs/2607.07196) / [EA-TWM-READ-0013](evidence-appendix.md#ea-twm-read-0013))
- `conditional` 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0002](evidence-appendix.md#ea-vlabreak-2026-0002))
- `conditional` ActionReasoning假设感知已由视觉算法可靠提供，将 LLM 的任务收窄为 3D 动作推理；作者认为这种解耦可降低端到端训练的数据需求。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-ALIGN-READ-0010](evidence-appendix.md#ea-align-read-0010))
- `conditional` On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively. ([2603.03279](https://arxiv.org/abs/2603.03279) / [EA-LOCOMANIP-2026-0018](evidence-appendix.md#ea-locomanip-2026-0018))
- `conditional` 在论文覆盖的设置中，StructVLA 的长时程改进同时出现在 LIBERO-Long 和 Franka 实机 tidy-up，但证据范围仍限于少量夹爪操作任务。 ([2603.12553](https://arxiv.org/abs/2603.12553) / [EA-VLABREAK-2026-0005](evidence-appendix.md#ea-vlabreak-2026-0005))
- `conditional` τ0-WM 把真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹合并训练，并用按模态的监督掩码处理各数据源的标注缺失。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-ALIGN-READ-0011](evidence-appendix.md#ea-align-read-0011))
- `conditional` ERVLA 的大规模实验表明，有效的具身 CoT 需要落到末端执行器运动或图像空间轨迹等动作相关表示，而将显式 CoT 作为自回归动作前缀会在推理时累积误差。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-ALIGN-READ-0006](evidence-appendix.md#ea-align-read-0006))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-ALIGN-READ-0007](evidence-appendix.md#ea-align-read-0007))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-ALIGN-READ-0008](evidence-appendix.md#ea-align-read-0008))
- `conditional` A structured intermediate visual interface can reduce the alignment burden by separating RGB-based geometric/task grounding from embodiment-specific action control. ([2606.26800](https://arxiv.org/abs/2606.26800) / [EA-ALIGN-READ-0002](evidence-appendix.md#ea-align-read-0002))
- `limit` H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0003](evidence-appendix.md#ea-vlabreak-2026-0003))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- `limit` Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- `limit` Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- `limit` TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-ALIGN-READ-0009](evidence-appendix.md#ea-align-read-0009))
- `limit` 在完整 LIBERO 闭环扫描中，BadWAM 的黑盒动作攻击将高成功率 WAM 从 96.5% 降至 43.1%，且失败对空间与长时程任务尤为严重。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0006](evidence-appendix.md#ea-vlabreak-2026-0006))
- `limit` 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))
- `conditional` 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-SENSORERR-READ-0007](evidence-appendix.md#ea-sensorerr-read-0007))
- `conditional` 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-SENSORERR-READ-0004](evidence-appendix.md#ea-sensorerr-read-0004))

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
