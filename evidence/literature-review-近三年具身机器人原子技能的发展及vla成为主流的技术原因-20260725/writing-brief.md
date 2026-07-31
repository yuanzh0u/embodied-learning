# Writing Brief: 近三年具身机器人原子技能的发展及VLA成为主流的技术原因

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近三年具身机器人原子技能的发展及VLA成为主流的技术原因
- Time range: 2023-07-25..2026-07-25
- Knowledge IDs: `EA-MODEL`, `EA-ALIGN`, `EA-XEMBODIMENT`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 17

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-MODEL`: RT-X 消融显示，在其跨本体设置中，更大模型容量会增强跨机器人数据集的迁移，这为通用 VLA 的规模化路线提供了直接技术激励。 ([2310.08864](https://arxiv.org/abs/2310.08864) / [EA-ATOM-2026-0001](evidence-appendix.md#ea-atom-2026-0001)) ⟷ DeCo 暴露了原子技能路线的核心成本：即使技能库可以零样本组合新长任务，VLM 规划的状态幻觉和指令分布偏移仍会降低部分原子任务表现。 ([2505.00527](https://arxiv.org/abs/2505.00527) / [EA-ATOM-2026-0007](evidence-appendix.md#ea-atom-2026-0007))
- `EA-MODEL`: Octo 在 WidowX 消融中表明，宽跨本体数据混合、ViT 骨干和 diffusion action head 的组合优于窄数据或替代动作头，说明 VLA 路线能同时吸收数据规模与连续动作建模收益。 ([2405.12213](https://arxiv.org/abs/2405.12213) / [EA-ATOM-2026-0002](evidence-appendix.md#ea-atom-2026-0002)) ⟷ 技能组合的瓶颈不只是单技能准确率：该诊断显示快照状态下的 VLA skill competence 与链式执行的 chained-state robustness 存在缺口，需要类型化前后置条件、步级验证和恢复。 ([2607.06256](https://arxiv.org/abs/2607.06256) / [EA-ATOM-2026-0010](evidence-appendix.md#ea-atom-2026-0010))
- `EA-MODEL`: π0 将通用 VLM 骨干与专门的连续动作专家结合，并在 10,000 小时、7 种机器人配置和 68 个任务的混合数据上训练；这表明 VLA 主流架构已通过专家化动作头吸收部分‘技能专用化’思路。 ([2410.24164](https://arxiv.org/abs/2410.24164) / [EA-ATOM-2026-0004](evidence-appendix.md#ea-atom-2026-0004)) ⟷ A recorded robot action is not a universal supervision signal: the same command can produce different motions across co... ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- `EA-MODEL`: LiLo-VLA 在两个长时程仿真套件上以平均 69% 成功率超过 π0.5 的 28% 和 OpenVLA-OFT 的 2%；它通过几何搬运、物体中心局部 VLA、动态重规划和技能复用组合，而非让单一端到端策略直接承担全部长程责任。 ([2602.21531](https://arxiv.org/abs/2602.21531) / [EA-ATOM-2026-0008](evidence-appendix.md#ea-atom-2026-0008)) ⟷ Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back int... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- `EA-MODEL`: AtomicVLA 在 LIBERO-LONG 中表明，用语义原子技能路由专家的 SG-MoE 达到 95.2% 成功率，比 token-level MoE 高 6.6 个百分点；原子技能的新进展正是进入 VLA 内部成为专家路由单元。 ([2603.07648](https://arxiv.org/abs/2603.07648) / [EA-ATOM-2026-0009](evidence-appendix.md#ea-atom-2026-0009)) ⟷ Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, tem... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- `EA-MODEL`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-ALIGN-READ-0015](evidence-appendix.md#ea-align-read-0015)) ⟷ H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0003](evidence-appendix.md#ea-vlabreak-2026-0003))
- `EA-MODEL`: H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0001](evidence-appendix.md#ea-vlabreak-2026-0001)) ⟷ OpenVLA 表明，开源预训练 VLA 可作为新机器人的可复用初始化，但实用采用仍依赖 10–150 条目标任务演示的微调。 ([2406.09246](https://arxiv.org/abs/2406.09246) / [EA-ATOM-2026-0003](evidence-appendix.md#ea-atom-2026-0003))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-MODEL (17 events)
- [`support`] RT-X 消融显示，在其跨本体设置中，更大模型容量会增强跨机器人数据集的迁移，这为通用 VLA 的规模化路线提供了直接技术激励。 ([2310.08864](https://arxiv.org/abs/2310.08864) / [EA-ATOM-2026-0001](evidence-appendix.md#ea-atom-2026-0001))
- [`support`] Octo 在 WidowX 消融中表明，宽跨本体数据混合、ViT 骨干和 diffusion action head 的组合优于窄数据或替代动作头，说明 VLA 路线能同时吸收数据规模与连续动作建模收益。 ([2405.12213](https://arxiv.org/abs/2405.12213) / [EA-ATOM-2026-0002](evidence-appendix.md#ea-atom-2026-0002))
- [`support`] π0 将通用 VLM 骨干与专门的连续动作专家结合，并在 10,000 小时、7 种机器人配置和 68 个任务的混合数据上训练；这表明 VLA 主流架构已通过专家化动作头吸收部分‘技能专用化’思路。 ([2410.24164](https://arxiv.org/abs/2410.24164) / [EA-ATOM-2026-0004](evidence-appendix.md#ea-atom-2026-0004))
- [`support`] H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0001](evidence-appendix.md#ea-vlabreak-2026-0001))
- [`support`] LiLo-VLA 在两个长时程仿真套件上以平均 69% 成功率超过 π0.5 的 28% 和 OpenVLA-OFT 的 2%；它通过几何搬运、物体中心局部 VLA、动态重规划和技能复用组合，而非让单一端到端策略直接承担全部长程责任。 ([2602.21531](https://arxiv.org/abs/2602.21531) / [EA-ATOM-2026-0008](evidence-appendix.md#ea-atom-2026-0008))
- [`support`] AtomicVLA 在 LIBERO-LONG 中表明，用语义原子技能路由专家的 SG-MoE 达到 95.2% 成功率，比 token-level MoE 高 6.6 个百分点；原子技能的新进展正是进入 VLA 内部成为专家路由单元。 ([2603.07648](https://arxiv.org/abs/2603.07648) / [EA-ATOM-2026-0009](evidence-appendix.md#ea-atom-2026-0009))
- [`support`] 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-ALIGN-READ-0015](evidence-appendix.md#ea-align-read-0015))
- [`conditional`] DexSkills 证明了原子技能路线在接触丰富长任务中的价值：触觉与本体信号可将长演示分解为可复用 primitive skills，再由独立策略组合执行；但证据限于预定技能集和特定灵巧手。 ([2405.03476](https://arxiv.org/abs/2405.03476) / [EA-ATOM-2026-0005](evidence-appendix.md#ea-atom-2026-0005))
- [`conditional`] OpenVLA 表明，开源预训练 VLA 可作为新机器人的可复用初始化，但实用采用仍依赖 10–150 条目标任务演示的微调。 ([2406.09246](https://arxiv.org/abs/2406.09246) / [EA-ATOM-2026-0003](evidence-appendix.md#ea-atom-2026-0003))
- [`conditional`] 原子技能库的当代发展已与 VLA 紧密耦合：该方法用 VLP 分解任务、用 VLA 微调实现技能，而且原子技能的粒度直接取决于 VLA 的可塑性和适应性。 ([2501.15068](https://arxiv.org/abs/2501.15068) / [EA-ATOM-2026-0006](evidence-appendix.md#ea-atom-2026-0006))
- [`conditional`] 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0002](evidence-appendix.md#ea-vlabreak-2026-0002))
- [`limit`] DeCo 暴露了原子技能路线的核心成本：即使技能库可以零样本组合新长任务，VLM 规划的状态幻觉和指令分布偏移仍会降低部分原子任务表现。 ([2505.00527](https://arxiv.org/abs/2505.00527) / [EA-ATOM-2026-0007](evidence-appendix.md#ea-atom-2026-0007))
- [`limit`] H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0003](evidence-appendix.md#ea-vlabreak-2026-0003))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- [`limit`] Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- [`limit`] Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- [`limit`] 技能组合的瓶颈不只是单技能准确率：该诊断显示快照状态下的 VLA skill competence 与链式执行的 chained-state robustness 存在缺口，需要类型化前后置条件、步级验证和恢复。 ([2607.06256](https://arxiv.org/abs/2607.06256) / [EA-ATOM-2026-0010](evidence-appendix.md#ea-atom-2026-0010))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` DexSkills 证明了原子技能路线在接触丰富长任务中的价值：触觉与本体信号可将长演示分解为可复用 primitive skills，再由独立策略组合执行；但证据限于预定技能集和特定灵巧手。 ([2405.03476](https://arxiv.org/abs/2405.03476) / [EA-ATOM-2026-0005](evidence-appendix.md#ea-atom-2026-0005))
- `conditional` OpenVLA 表明，开源预训练 VLA 可作为新机器人的可复用初始化，但实用采用仍依赖 10–150 条目标任务演示的微调。 ([2406.09246](https://arxiv.org/abs/2406.09246) / [EA-ATOM-2026-0003](evidence-appendix.md#ea-atom-2026-0003))
- `conditional` 原子技能库的当代发展已与 VLA 紧密耦合：该方法用 VLP 分解任务、用 VLA 微调实现技能，而且原子技能的粒度直接取决于 VLA 的可塑性和适应性。 ([2501.15068](https://arxiv.org/abs/2501.15068) / [EA-ATOM-2026-0006](evidence-appendix.md#ea-atom-2026-0006))
- `conditional` 在五个 5-7 步 LIBERO-LoHo 任务上，双层逻辑+潜在视觉引导比仅逻辑引导高 16.4 个成功率百分点，也高于像素级生成引导。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0002](evidence-appendix.md#ea-vlabreak-2026-0002))
- `limit` DeCo 暴露了原子技能路线的核心成本：即使技能库可以零样本组合新长任务，VLM 规划的状态幻觉和指令分布偏移仍会降低部分原子任务表现。 ([2505.00527](https://arxiv.org/abs/2505.00527) / [EA-ATOM-2026-0007](evidence-appendix.md#ea-atom-2026-0007))
- `limit` H-WM 的分层收益以额外训练与系统复杂度、以及任务可被结构化逻辑表示为前提。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0003](evidence-appendix.md#ea-vlabreak-2026-0003))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- `limit` Discrete action tokenization is a compact interface for autoregressive VLA policies, but decoding fixed tokens back into continuous robot controls is a bottleneck when the same token must mean differ... ([2606.30113](https://arxiv.org/abs/2606.30113) / [EA-ALIGN-READ-0003](evidence-appendix.md#ea-align-read-0003))
- `limit` Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- `limit` 技能组合的瓶颈不只是单技能准确率：该诊断显示快照状态下的 VLA skill competence 与链式执行的 chained-state robustness 存在缺口，需要类型化前后置条件、步级验证和恢复。 ([2607.06256](https://arxiv.org/abs/2607.06256) / [EA-ATOM-2026-0010](evidence-appendix.md#ea-atom-2026-0010))

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
