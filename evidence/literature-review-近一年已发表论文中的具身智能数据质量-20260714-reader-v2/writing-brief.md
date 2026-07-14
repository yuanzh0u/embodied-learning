# Writing Brief: 近一年已发表论文中的具身智能数据质量

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年已发表论文中的具身智能数据质量
- Time range: 2025-07-14..2026-07-14
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-MODEL`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DQ-YEAR-READ-0001](evidence-appendix.md#ea-dq-year-read-0001)) ⟷ Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should ex... ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DQ-YEAR-READ-0013](evidence-appendix.md#ea-dq-year-read-0013))
- `EA-DATA`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [EA-DQ-YEAR-READ-0005](evidence-appendix.md#ea-dq-year-read-0005)) ⟷ TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DQ-YEAR-READ-0014](evidence-appendix.md#ea-dq-year-read-0014))
- `EA-DATA`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [EA-DQ-YEAR-READ-0006](evidence-appendix.md#ea-dq-year-read-0006)) ⟷ SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DQ-YEAR-READ-0015](evidence-appendix.md#ea-dq-year-read-0015))
- `EA-DATA`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DQ-YEAR-READ-0007](evidence-appendix.md#ea-dq-year-read-0007)) ⟷ VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([2602.10618](https://arxiv.org/abs/2602.10618) / [EA-DQ-YEAR-READ-0002](evidence-appendix.md#ea-dq-year-read-0002))
- `EA-DATA`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DQ-YEAR-READ-0008](evidence-appendix.md#ea-dq-year-read-0008)) ⟷ 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- `EA-DATA`: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([2512.13100](https://arxiv.org/abs/2512.13100) / [EA-DQ-YEAR-READ-0009](evidence-appendix.md#ea-dq-year-read-0009)) ⟷ 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DQ-YEAR-READ-0004](evidence-appendix.md#ea-dq-year-read-0004))
- `EA-DATA`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-DQ-YEAR-READ-0010](evidence-appendix.md#ea-dq-year-read-0010)) ⟷ Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DQ-YEAR-READ-0011](evidence-appendix.md#ea-dq-year-read-0011))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (15 events)
- [`support`] 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DQ-YEAR-READ-0008](evidence-appendix.md#ea-dq-year-read-0008))
- [`support`] 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([2512.13100](https://arxiv.org/abs/2512.13100) / [EA-DQ-YEAR-READ-0009](evidence-appendix.md#ea-dq-year-read-0009))
- [`support`] 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [EA-DQ-YEAR-READ-0005](evidence-appendix.md#ea-dq-year-read-0005))
- [`support`] 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DQ-YEAR-READ-0001](evidence-appendix.md#ea-dq-year-read-0001))
- [`support`] 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [EA-DQ-YEAR-READ-0006](evidence-appendix.md#ea-dq-year-read-0006))
- [`support`] DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DQ-YEAR-READ-0007](evidence-appendix.md#ea-dq-year-read-0007))
- [`support`] 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-DQ-YEAR-READ-0010](evidence-appendix.md#ea-dq-year-read-0010))
- [`conditional`] VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([2602.10618](https://arxiv.org/abs/2602.10618) / [EA-DQ-YEAR-READ-0002](evidence-appendix.md#ea-dq-year-read-0002))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- [`conditional`] Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DQ-YEAR-READ-0011](evidence-appendix.md#ea-dq-year-read-0011))
- [`conditional`] Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DQ-YEAR-READ-0012](evidence-appendix.md#ea-dq-year-read-0012))
- [`conditional`] 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DQ-YEAR-READ-0004](evidence-appendix.md#ea-dq-year-read-0004))
- [`limit`] Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DQ-YEAR-READ-0013](evidence-appendix.md#ea-dq-year-read-0013))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DQ-YEAR-READ-0014](evidence-appendix.md#ea-dq-year-read-0014))
- [`limit`] SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DQ-YEAR-READ-0015](evidence-appendix.md#ea-dq-year-read-0015))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([2602.10618](https://arxiv.org/abs/2602.10618) / [EA-DQ-YEAR-READ-0002](evidence-appendix.md#ea-dq-year-read-0002))
- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- `conditional` Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DQ-YEAR-READ-0011](evidence-appendix.md#ea-dq-year-read-0011))
- `conditional` Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DQ-YEAR-READ-0012](evidence-appendix.md#ea-dq-year-read-0012))
- `conditional` 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DQ-YEAR-READ-0004](evidence-appendix.md#ea-dq-year-read-0004))
- `limit` Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DQ-YEAR-READ-0013](evidence-appendix.md#ea-dq-year-read-0013))
- `limit` TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-DQ-YEAR-READ-0014](evidence-appendix.md#ea-dq-year-read-0014))
- `limit` SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DQ-YEAR-READ-0015](evidence-appendix.md#ea-dq-year-read-0015))

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
