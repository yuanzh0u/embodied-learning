# Writing Brief: 近半年 UMI 数据质量

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近半年 UMI 数据质量
- Time range: 2025-12-06..2026-06-06
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-XEMBODIMENT`
- Paper-level sources: 5 / 5 (formal-ready)
- Accepted events: 5

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- 证据中没有明显的 stance 张力;考虑以共识+边界作为组织轴。

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (2 events)
- [`conditional`] UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only dat... ([2601.09988](https://arxiv.org/abs/2601.09988) / [UMI-6M-001](evidence-appendix.md#umi-6m-001))
- [`limit`] UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefulness. ([2603.17189](https://arxiv.org/abs/2603.17189) / [UMI-6M-002](evidence-appendix.md#umi-6m-002))

### EA-SENSOR (2 events)
- [`conditional`] UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data. ([2604.10647](https://arxiv.org/abs/2604.10647) / [UMI-6M-003](evidence-appendix.md#umi-6m-003))
- [`limit`] Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [UMI-6M-004](evidence-appendix.md#umi-6m-004))

### EA-XEMBODIMENT (1 events)
- [`support`] For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action space, avoiding retargeting and embodimen... ([2606.06033](https://arxiv.org/abs/2606.06033) / [UMI-6M-005](evidence-appendix.md#umi-6m-005))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only dat... ([2601.09988](https://arxiv.org/abs/2601.09988) / [UMI-6M-001](evidence-appendix.md#umi-6m-001))
- `limit` UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefulness. ([2603.17189](https://arxiv.org/abs/2603.17189) / [UMI-6M-002](evidence-appendix.md#umi-6m-002))
- `conditional` UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data. ([2604.10647](https://arxiv.org/abs/2604.10647) / [UMI-6M-003](evidence-appendix.md#umi-6m-003))
- `limit` Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [UMI-6M-004](evidence-appendix.md#umi-6m-004))

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
