# Writing Brief: 具身智能数据质量的主要矛盾

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 具身智能数据质量的主要矛盾
- Time range: 2026-01-14..2026-07-14
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-XEMBODIMENT`, `EA-MODEL`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D corres... ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003)) ⟷ TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))
- `EA-DATA`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004)) ⟷ SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))
- `EA-DATA`: 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 ([2607.05390](https://arxiv.org/abs/2607.05390) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005)) ⟷ Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should ex... ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- `EA-DATA`: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006)) ⟷ Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009))
- `EA-DATA`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007)) ⟷ Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervis... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))
- `EA-DATA`: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-READ-0008](evidence-appendix.md#ea-data-read-0008)) ⟷ RynnWorld-Teleop将数字遥操作作为生成式数据引擎，但论文明确限定了它对精细流体动力学、高形变物体和跨机器人平台扩展的能力。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (15 events)
- [`support`] 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-READ-0008](evidence-appendix.md#ea-data-read-0008))
- [`support`] World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-DATA-READ-0003](evidence-appendix.md#ea-data-read-0003))
- [`support`] τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-READ-0007](evidence-appendix.md#ea-data-read-0007))
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-DATA-READ-0004](evidence-appendix.md#ea-data-read-0004))
- [`support`] 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 ([2607.05390](https://arxiv.org/abs/2607.05390) / [EA-DATA-READ-0005](evidence-appendix.md#ea-data-read-0005))
- [`support`] Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-READ-0006](evidence-appendix.md#ea-data-read-0006))
- [`conditional`] VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([2602.10618](https://arxiv.org/abs/2602.10618) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014))
- [`conditional`] Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009))
- [`conditional`] Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))
- [`conditional`] 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-READ-0015](evidence-appendix.md#ea-data-read-0015))
- [`conditional`] RynnWorld-Teleop将数字遥操作作为生成式数据引擎，但论文明确限定了它对精细流体动力学、高形变物体和跨机器人平台扩展的能力。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012))
- [`limit`] Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))
- [`limit`] SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([2602.10618](https://arxiv.org/abs/2602.10618) / [EA-DATA-READ-0013](evidence-appendix.md#ea-data-read-0013))
- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-READ-0014](evidence-appendix.md#ea-data-read-0014))
- `conditional` Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-READ-0009](evidence-appendix.md#ea-data-read-0009))
- `conditional` Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DATA-READ-0010](evidence-appendix.md#ea-data-read-0010))
- `conditional` 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-READ-0015](evidence-appendix.md#ea-data-read-0015))
- `conditional` RynnWorld-Teleop将数字遥操作作为生成式数据引擎，但论文明确限定了它对精细流体动力学、高形变物体和跨机器人平台扩展的能力。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-READ-0012](evidence-appendix.md#ea-data-read-0012))
- `limit` Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-READ-0011](evidence-appendix.md#ea-data-read-0011))
- `limit` TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DATA-READ-0001](evidence-appendix.md#ea-data-read-0001))
- `limit` SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-READ-0002](evidence-appendix.md#ea-data-read-0002))

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
- Registered sources: not loaded
