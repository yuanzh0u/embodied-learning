# Writing Brief: 近一年具身导航问题是否已有效解决

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年具身导航问题是否已有效解决
- Time range: 2025-07-14..2026-07-14
- Knowledge IDs: `EA-EVAL`, `EA-SENSOR`, `EA-4D`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- 证据中没有明显的 stance 张力;考虑以共识+边界作为组织轴。

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (1 events)
- [`support`] 对依赖历史地图的导航，感知重建本身可以正确，但地形物理变化仍会使原路线失效；物理可行世界模型通过介入前的 what-if 修改场景暴露这类长时程规划失败。 ([2607.00673](https://arxiv.org/abs/2607.00673) / [ERR-PVC-READ-0013](evidence-appendix.md#err-pvc-read-0013))

### EA-SENSOR (14 events)
- [`conditional`] ReaDy-Go支持环境特定的动态sim-to-real路线，但作者仍要求扩大训练环境，并引入安全学习以应对更密集、多样和激进的动态主体。 ([2602.11575](https://arxiv.org/abs/2602.11575) / [EA-PNAV-2026-0011](evidence-appendix.md#ea-pnav-2026-0011))
- [`conditional`] OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 ([2603.11072](https://arxiv.org/abs/2603.11072) / [EA-PNAV-2026-0003](evidence-appendix.md#ea-pnav-2026-0003))
- [`conditional`] 真实VLN鲁棒性依赖显式结构先验、异常检测和重规划；没有这些机制的基线在目标式指令或阻塞下会出现灾难性退化。 ([2603.12696](https://arxiv.org/abs/2603.12696) / [EA-PNAV-2026-0012](evidence-appendix.md#ea-pnav-2026-0012))
- [`conditional`] 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 ([2605.14801](https://arxiv.org/abs/2605.14801) / [EA-PNAV-2026-0004](evidence-appendix.md#ea-pnav-2026-0004))
- [`limit`] 开放世界航空ObjectNav远未解决：基准中所有方法的碰撞率都超过真实部署可接受水平，语义探索尚未转化为安全控制。 ([2508.00288](https://arxiv.org/abs/2508.00288) / [EA-PNAV-2026-0015](evidence-appendix.md#ea-pnav-2026-0015))
- [`limit`] 真实社会导航的进步仍依赖受限的人体状态表征；论文明确指出机器人缺少专家可用的人类意图线索，并受到感知延迟影响。 ([2509.17204](https://arxiv.org/abs/2509.17204) / [EA-PNAV-2026-0009](evidence-appendix.md#ea-pnav-2026-0009))
- [`limit`] 当前VLM导航仍存在显著人类差距，且目标定位是主导失败模式；这说明基础视觉语言能力尚未等价为可靠空间行动。 ([2510.26909](https://arxiv.org/abs/2510.26909) / [EA-PNAV-2026-0010](evidence-appendix.md#ea-pnav-2026-0010))
- [`limit`] MSGNav的结果不能说明零样本导航已解决：作者明确指出VFM/VLM延迟阻碍实时部署，且最后一公里仅被缓解而未被彻底解决。 ([2511.10376](https://arxiv.org/abs/2511.10376) / [EA-PNAV-2026-0001](evidence-appendix.md#ea-pnav-2026-0001))
- [`limit`] 现有VLN的高层推理并未克服物理执行：即使CoT改善理想化传送设置，严格物理条件下性能仍低，碰撞是主要瓶颈。 ([2512.19021](https://arxiv.org/abs/2512.19021) / [EA-PNAV-2026-0007](evidence-appendix.md#ea-pnav-2026-0007))
- [`limit`] CausalNav说明动态语义图可显著推进户外长距离导航，但作者仍把扩展性、极端光照天气和长时一致性列为未解决限制。 ([2601.01872](https://arxiv.org/abs/2601.01872) / [EA-PNAV-2026-0008](evidence-appendix.md#ea-pnav-2026-0008))
- [`limit`] 当前LMM的连续空间行动仍远未解决：失败跨越几何感知、跨视角理解、动作后果想象和长期记忆，而非单一视觉分类误差。 ([2604.07973](https://arxiv.org/abs/2604.07973) / [EA-PNAV-2026-0005](evidence-appendix.md#ea-pnav-2026-0005))
- [`limit`] 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。 ([2606.10348](https://arxiv.org/abs/2606.10348) / [EA-PNAV-2026-0013](evidence-appendix.md#ea-pnav-2026-0013))
- [`limit`] 端侧VLM可显著降低导航推理延迟，但基于场景图的ObjectNav仍无法原生表示瞬态组合语义，动态线索可能在稀疏查询间丢失。 ([2606.27871](https://arxiv.org/abs/2606.27871) / [EA-PNAV-2026-0014](evidence-appendix.md#ea-pnav-2026-0014))
- [`gap`] 缺乏标准化、可扩展的sim-to-real基准本身就是关键瓶颈，因此模拟榜单分数不足以宣告感知或导航已经解决。 ([2508.11117](https://arxiv.org/abs/2508.11117) / [EA-PNAV-2026-0006](evidence-appendix.md#ea-pnav-2026-0006))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` ReaDy-Go支持环境特定的动态sim-to-real路线，但作者仍要求扩大训练环境，并引入安全学习以应对更密集、多样和激进的动态主体。 ([2602.11575](https://arxiv.org/abs/2602.11575) / [EA-PNAV-2026-0011](evidence-appendix.md#ea-pnav-2026-0011))
- `conditional` OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 ([2603.11072](https://arxiv.org/abs/2603.11072) / [EA-PNAV-2026-0003](evidence-appendix.md#ea-pnav-2026-0003))
- `conditional` 真实VLN鲁棒性依赖显式结构先验、异常检测和重规划；没有这些机制的基线在目标式指令或阻塞下会出现灾难性退化。 ([2603.12696](https://arxiv.org/abs/2603.12696) / [EA-PNAV-2026-0012](evidence-appendix.md#ea-pnav-2026-0012))
- `conditional` 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 ([2605.14801](https://arxiv.org/abs/2605.14801) / [EA-PNAV-2026-0004](evidence-appendix.md#ea-pnav-2026-0004))
- `limit` 开放世界航空ObjectNav远未解决：基准中所有方法的碰撞率都超过真实部署可接受水平，语义探索尚未转化为安全控制。 ([2508.00288](https://arxiv.org/abs/2508.00288) / [EA-PNAV-2026-0015](evidence-appendix.md#ea-pnav-2026-0015))
- `limit` 真实社会导航的进步仍依赖受限的人体状态表征；论文明确指出机器人缺少专家可用的人类意图线索，并受到感知延迟影响。 ([2509.17204](https://arxiv.org/abs/2509.17204) / [EA-PNAV-2026-0009](evidence-appendix.md#ea-pnav-2026-0009))
- `limit` 当前VLM导航仍存在显著人类差距，且目标定位是主导失败模式；这说明基础视觉语言能力尚未等价为可靠空间行动。 ([2510.26909](https://arxiv.org/abs/2510.26909) / [EA-PNAV-2026-0010](evidence-appendix.md#ea-pnav-2026-0010))
- `limit` MSGNav的结果不能说明零样本导航已解决：作者明确指出VFM/VLM延迟阻碍实时部署，且最后一公里仅被缓解而未被彻底解决。 ([2511.10376](https://arxiv.org/abs/2511.10376) / [EA-PNAV-2026-0001](evidence-appendix.md#ea-pnav-2026-0001))
- `limit` 现有VLN的高层推理并未克服物理执行：即使CoT改善理想化传送设置，严格物理条件下性能仍低，碰撞是主要瓶颈。 ([2512.19021](https://arxiv.org/abs/2512.19021) / [EA-PNAV-2026-0007](evidence-appendix.md#ea-pnav-2026-0007))
- `limit` CausalNav说明动态语义图可显著推进户外长距离导航，但作者仍把扩展性、极端光照天气和长时一致性列为未解决限制。 ([2601.01872](https://arxiv.org/abs/2601.01872) / [EA-PNAV-2026-0008](evidence-appendix.md#ea-pnav-2026-0008))
- `limit` 当前LMM的连续空间行动仍远未解决：失败跨越几何感知、跨视角理解、动作后果想象和长期记忆，而非单一视觉分类误差。 ([2604.07973](https://arxiv.org/abs/2604.07973) / [EA-PNAV-2026-0005](evidence-appendix.md#ea-pnav-2026-0005))
- `limit` 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。 ([2606.10348](https://arxiv.org/abs/2606.10348) / [EA-PNAV-2026-0013](evidence-appendix.md#ea-pnav-2026-0013))
- `limit` 端侧VLM可显著降低导航推理延迟，但基于场景图的ObjectNav仍无法原生表示瞬态组合语义，动态线索可能在稀疏查询间丢失。 ([2606.27871](https://arxiv.org/abs/2606.27871) / [EA-PNAV-2026-0014](evidence-appendix.md#ea-pnav-2026-0014))
- `gap` 缺乏标准化、可扩展的sim-to-real基准本身就是关键瓶颈，因此模拟榜单分数不足以宣告感知或导航已经解决。 ([2508.11117](https://arxiv.org/abs/2508.11117) / [EA-PNAV-2026-0006](evidence-appendix.md#ea-pnav-2026-0006))

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
