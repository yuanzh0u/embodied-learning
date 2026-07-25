# Writing Brief: 近一年论文中的具身数据污染问题

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年论文中的具身数据污染问题
- Time range: 2025-07-15..2026-07-15
- Knowledge IDs: `EA-DATA`, `EA-EVAL`, `EA-MODEL`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 具身视频语料的重复不能只按片段数理解：同一场景中的相似任务会膨胀数据规模却几乎不增加场景多样性，因此去重应同时检查视觉与轨迹冗余。 ([2606.04463](https://arxiv.org/abs/2606.04463) / [EA-CONTAM-2026-0011](evidence-appendix.md#ea-contam-2026-0011)) ⟷ 具身污染不只能藏在图像或文本中：污染真实示教里的初始关节状态可形成隐蔽 VLA 后门，并绕过视觉预处理防御。 ([2601.04266](https://arxiv.org/abs/2601.04266) / [EA-CONTAM-2026-0001](evidence-appendix.md#ea-contam-2026-0001))
- `EA-DATA`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-CONTAM-2026-0013](evidence-appendix.md#ea-contam-2026-0013)) ⟷ 开源机器人数据供应链对极小比例的 episode 级投毒很敏感：在该真实拾放实验中，3 条投毒 episode 混入 320 条干净 episode 即实现触发式完全拒绝服务。 ([2607.04146](https://arxiv.org/abs/2607.04146) / [EA-CONTAM-2026-0002](evidence-appendix.md#ea-contam-2026-0002))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (15 events)
- [`support`] 具身视频语料的重复不能只按片段数理解：同一场景中的相似任务会膨胀数据规模却几乎不增加场景多样性，因此去重应同时检查视觉与轨迹冗余。 ([2606.04463](https://arxiv.org/abs/2606.04463) / [EA-CONTAM-2026-0011](evidence-appendix.md#ea-contam-2026-0011))
- [`support`] 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-CONTAM-2026-0013](evidence-appendix.md#ea-contam-2026-0013))
- [`conditional`] 视觉后门可通过深层注意力和潜特征异常做推理时定位，但与场景语义自然融合的触发物依然是明显盲点。 ([2602.03153](https://arxiv.org/abs/2602.03153) / [EA-CONTAM-2026-0005](evidence-appendix.md#ea-contam-2026-0005))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-CONTAM-2026-0012](evidence-appendix.md#ea-contam-2026-0012))
- [`conditional`] 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-CONTAM-2026-0014](evidence-appendix.md#ea-contam-2026-0014))
- [`conditional`] 后门防御应把检测、因果定位和恢复分开计账；干净校准的内部机制监控对视觉触发有效，但不覆盖状态、语义或自适应后门。 ([2607.12571](https://arxiv.org/abs/2607.12571) / [EA-CONTAM-2026-0008](evidence-appendix.md#ea-contam-2026-0008))
- [`limit`] LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 ([2510.03827](https://arxiv.org/abs/2510.03827) / [EA-CONTAM-2026-0007](evidence-appendix.md#ea-contam-2026-0007))
- [`limit`] 仅看 episode 成功率会漏掉动作级污染：后门可在关键短时窗覆写夹爪等可复用低层动作，即使整体任务表现仍显得正常。 ([2510.10932](https://arxiv.org/abs/2510.10932) / [EA-CONTAM-2026-0003](evidence-appendix.md#ea-contam-2026-0003))
- [`limit`] 污染后门可以不只让机器人“失败”，而是在触发时执行攻击者指定的长程动作序列；真机已显示可行性，但强度低于仿真。 ([2511.12149](https://arxiv.org/abs/2511.12149) / [EA-CONTAM-2026-0009](evidence-appendix.md#ea-contam-2026-0009))
- [`limit`] 具身污染不只能藏在图像或文本中：污染真实示教里的初始关节状态可形成隐蔽 VLA 后门，并绕过视觉预处理防御。 ([2601.04266](https://arxiv.org/abs/2601.04266) / [EA-CONTAM-2026-0001](evidence-appendix.md#ea-contam-2026-0001))
- [`limit`] Action chunking 与 delta-pose 积分会把平滑、微小的污染偏差在开环执行窗内积累成失败，使“轨迹看起来平滑”不再是安全证据。 ([2601.14323](https://arxiv.org/abs/2601.14323) / [EA-CONTAM-2026-0004](evidence-appendix.md#ea-contam-2026-0004))
- [`limit`] 下游只用干净数据微调不能证明 VLA 已经没有污染；植入微调不敏感模块的基模型后门可穿过用户端的干净适配。 ([2602.00500](https://arxiv.org/abs/2602.00500) / [EA-CONTAM-2026-0010](evidence-appendix.md#ea-contam-2026-0010))
- [`limit`] 世界模型使数据污染变成“二次激活”问题：表面安全的遥操数据可在生成扩增时转化为危险轨迹，并污染下游政策。 ([2606.09499](https://arxiv.org/abs/2606.09499) / [EA-CONTAM-2026-0006](evidence-appendix.md#ea-contam-2026-0006))
- [`limit`] 开源机器人数据供应链对极小比例的 episode 级投毒很敏感：在该真实拾放实验中，3 条投毒 episode 混入 320 条干净 episode 即实现触发式完全拒绝服务。 ([2607.04146](https://arxiv.org/abs/2607.04146) / [EA-CONTAM-2026-0002](evidence-appendix.md#ea-contam-2026-0002))
- [`limit`] SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-CONTAM-2026-0015](evidence-appendix.md#ea-contam-2026-0015))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 视觉后门可通过深层注意力和潜特征异常做推理时定位，但与场景语义自然融合的触发物依然是明显盲点。 ([2602.03153](https://arxiv.org/abs/2602.03153) / [EA-CONTAM-2026-0005](evidence-appendix.md#ea-contam-2026-0005))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-CONTAM-2026-0012](evidence-appendix.md#ea-contam-2026-0012))
- `conditional` 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-CONTAM-2026-0014](evidence-appendix.md#ea-contam-2026-0014))
- `conditional` 后门防御应把检测、因果定位和恢复分开计账；干净校准的内部机制监控对视觉触发有效，但不覆盖状态、语义或自适应后门。 ([2607.12571](https://arxiv.org/abs/2607.12571) / [EA-CONTAM-2026-0008](evidence-appendix.md#ea-contam-2026-0008))
- `limit` LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 ([2510.03827](https://arxiv.org/abs/2510.03827) / [EA-CONTAM-2026-0007](evidence-appendix.md#ea-contam-2026-0007))
- `limit` 仅看 episode 成功率会漏掉动作级污染：后门可在关键短时窗覆写夹爪等可复用低层动作，即使整体任务表现仍显得正常。 ([2510.10932](https://arxiv.org/abs/2510.10932) / [EA-CONTAM-2026-0003](evidence-appendix.md#ea-contam-2026-0003))
- `limit` 污染后门可以不只让机器人“失败”，而是在触发时执行攻击者指定的长程动作序列；真机已显示可行性，但强度低于仿真。 ([2511.12149](https://arxiv.org/abs/2511.12149) / [EA-CONTAM-2026-0009](evidence-appendix.md#ea-contam-2026-0009))
- `limit` 具身污染不只能藏在图像或文本中：污染真实示教里的初始关节状态可形成隐蔽 VLA 后门，并绕过视觉预处理防御。 ([2601.04266](https://arxiv.org/abs/2601.04266) / [EA-CONTAM-2026-0001](evidence-appendix.md#ea-contam-2026-0001))
- `limit` Action chunking 与 delta-pose 积分会把平滑、微小的污染偏差在开环执行窗内积累成失败，使“轨迹看起来平滑”不再是安全证据。 ([2601.14323](https://arxiv.org/abs/2601.14323) / [EA-CONTAM-2026-0004](evidence-appendix.md#ea-contam-2026-0004))
- `limit` 下游只用干净数据微调不能证明 VLA 已经没有污染；植入微调不敏感模块的基模型后门可穿过用户端的干净适配。 ([2602.00500](https://arxiv.org/abs/2602.00500) / [EA-CONTAM-2026-0010](evidence-appendix.md#ea-contam-2026-0010))
- `limit` 世界模型使数据污染变成“二次激活”问题：表面安全的遥操数据可在生成扩增时转化为危险轨迹，并污染下游政策。 ([2606.09499](https://arxiv.org/abs/2606.09499) / [EA-CONTAM-2026-0006](evidence-appendix.md#ea-contam-2026-0006))
- `limit` 开源机器人数据供应链对极小比例的 episode 级投毒很敏感：在该真实拾放实验中，3 条投毒 episode 混入 320 条干净 episode 即实现触发式完全拒绝服务。 ([2607.04146](https://arxiv.org/abs/2607.04146) / [EA-CONTAM-2026-0002](evidence-appendix.md#ea-contam-2026-0002))
- `limit` SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-CONTAM-2026-0015](evidence-appendix.md#ea-contam-2026-0015))

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
