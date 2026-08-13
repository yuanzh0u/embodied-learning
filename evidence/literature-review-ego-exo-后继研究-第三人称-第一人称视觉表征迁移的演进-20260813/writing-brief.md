# Writing Brief: Ego-Exo 后继研究：第三人称→第一人称视觉表征迁移的演进

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: Ego-Exo 后继研究：第三人称→第一人称视觉表征迁移的演进
- Time range: 2026-02-13..2026-08-13
- Knowledge IDs: `EA-XEMBODIMENT`, `EA-MODEL`, `EA-DATA`
- Review mode: scoping
- Paper-level sources: 11 / 15 floor (not a cap)
- Coverage and saturation gate: blocked
- Writing readiness: preliminary
- Unresolved checks: coverage-report-missing, paper-reading-accepted-floor:0/15, paper-reading-ledger-mismatch:accepted-0<event-papers-11
- Accepted events: 20

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- 证据中没有明显的 stance 张力;考虑以共识+边界作为组织轴。

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-XEMBODIMENT (20 events)
- [`support`] Ego-Exo 从大规模第三人称视频中挖掘 Ego-Score、Object-Score、Interaction-Map 三类 egocentric 信号，并以知识蒸馏损失在预训练时注入视频模型，从而无需配对或动作标注的 ego 视频。 ([2104.07905](https://arxiv.org/abs/2104.07905) / [EA-EGOEXO-2026-0001](evidence-appendix.md#ea-egoexo-2026-0001))
- [`support`] Ego-Exo 在 Charades-Ego 上较 Kinetics 预训练基线提升 +3.26 mAP，并在 EPIC-Kitchens-100 取得当时 SOTA。 ([2104.07905](https://arxiv.org/abs/2104.07905) / [EA-EGOEXO-2026-0002](evidence-appendix.md#ea-egoexo-2026-0002))
- [`support`] 该工作提出从 exocentric 视角的 affordance grounding：从第三人称人-物交互图像学习可供性知识并迁移到 egocentric 物体图像，仅用 affordance 标签监督，并构建 AGD20K 数据集。 ([2203.09905](https://arxiv.org/abs/2203.09905) / [EA-EGOEXO-2026-0007](evidence-appendix.md#ea-egoexo-2026-0007))
- [`support`] 在 seen 设定下，该方法 KLD 较最佳 saliency 模型提升 17.2%，较 affordance grounding 模型提升 13.3%。 ([2203.09905](https://arxiv.org/abs/2203.09905) / [EA-EGOEXO-2026-0008](evidence-appendix.md#ea-egoexo-2026-0008))
- [`support`] 该期刊版在会议版基础上引入 Cross-view Feature Transfer（CFT）模块，通过密集匹配显式建模人与人之间的 interaction bias，扩展 AGD20K 至 26,117 图像。 ([2208.13196](https://arxiv.org/abs/2208.13196) / [EA-EGOEXO-2026-0016](evidence-appendix.md#ea-egoexo-2026-0016))
- [`support`] LOCATE 提出部件级知识迁移：定位 exo 交互区域、用 PartSelect 选出物体部件原型，再以此监督 egocentric affordance grounding，仅用图像级标签弱监督。 ([2303.09665](https://arxiv.org/abs/2303.09665) / [EA-EGOEXO-2026-0009](evidence-appendix.md#ea-egoexo-2026-0009))
- [`support`] 在 unseen 设定下，LOCATE 较 SOTA 方法 Cross-view-AG+ 提升 KLD 20.4%、SIM 33.3%、NSS 31.2%。 ([2303.09665](https://arxiv.org/abs/2303.09665) / [EA-EGOEXO-2026-0010](evidence-appendix.md#ea-egoexo-2026-0010))
- [`support`] AE2 从 unpaired 的 ego-exo 视频学习细粒度视角不变表征：用 object-centric 编码器关注手与主动物体，以 DTW 时序对齐作自监督目标，并用反转帧作负样本对比正则。 ([2306.05526](https://arxiv.org/abs/2306.05526) / [EA-EGOEXO-2026-0011](evidence-appendix.md#ea-egoexo-2026-0011))
- [`support`] AE2 在四个数据集、regular 与 cross-view 设定上全面超越 SOTA（如 Break Eggs 动作相位分类 F1 66.23 vs 最佳基线 GTA 56.86）。 ([2306.05526](https://arxiv.org/abs/2306.05526) / [EA-EGOEXO-2026-0012](evidence-appendix.md#ea-egoexo-2026-0012))
- [`support`] Ego-Exo4D 是迄今最大的时间同步第一+第三人称视频数据集，共 1286 小时、740 名参与者、覆盖 8 个领域技能活动，并配多模态与专家评论等语言标注。 ([2311.18259](https://arxiv.org/abs/2311.18259) / [EA-EGOEXO-2026-0003](evidence-appendix.md#ea-egoexo-2026-0003))
- [`support`] Ego-Exo4D 首次形式化 ego-exo relation 任务族（对象级对应 correspondence 与视角翻译 translation），使 first↔third-person 视角迁移成为可评测的基准任务。 ([2311.18259](https://arxiv.org/abs/2311.18259) / [EA-EGOEXO-2026-0004](evidence-appendix.md#ea-egoexo-2026-0004))
- [`support`] 该工作用无标注的同步 exo-ego 视频对做知识蒸馏，把时序动作分割模型从 exo 迁移到 ego，无需任何 ego 标签，并在 Assembly101 与 EgoExo4D 上验证。 ([2312.02638](https://arxiv.org/abs/2312.02638) / [EA-EGOEXO-2026-0017](evidence-appendix.md#ea-egoexo-2026-0017))
- [`support`] 同步蒸馏最佳模型在 Assembly101 上与监督式 ego-oracle 相当（edit 28.59 vs 26.42），远超仅用 exo 数据的基线（edit 12.60）。 ([2312.02638](https://arxiv.org/abs/2312.02638) / [EA-EGOEXO-2026-0018](evidence-appendix.md#ea-egoexo-2026-0018))
- [`support`] EgoInstructor 用自动挖掘的 ego-exo 视频对训练跨视角检索模块，检索语义相关的第三人称教学视频作参考，增强 egocentric 视频描述。 ([2401.00789](https://arxiv.org/abs/2401.00789) / [EA-EGOEXO-2026-0019](evidence-appendix.md#ea-egoexo-2026-0019))
- [`support`] EgoInstructor 的跨视角检索模块在 7 个 benchmark 上一致提升，如 InternVideo 在 CharadesEgo 上 Ego2Exo/Exo2Ego 分别提升 15.9% 与 7.7%。 ([2401.00789](https://arxiv.org/abs/2401.00789) / [EA-EGOEXO-2026-0020](evidence-appendix.md#ea-egoexo-2026-0020))
- [`support`] EgoExoLearn 将 ego-exo 迁移推进到异步、异环境的演示跟随（demo-following）设定：个体观看 exo 演示后在佩戴 gaze 设备的情况下于不同环境复现程序性任务，共 120 小时。 ([2403.16182](https://arxiv.org/abs/2403.16182) / [EA-EGOEXO-2026-0005](evidence-appendix.md#ea-egoexo-2026-0005))
- [`support`] EgoExo-Fitness 提供 32 小时、1276 段同步 egocentric+exocentric 全身健身动作数据集，并引入技术关键点核验、自然语言评语、质量分等可解释动作评判标注。 ([2406.08877](https://arxiv.org/abs/2406.08877) / [EA-EGOEXO-2026-0015](evidence-appendix.md#ea-egoexo-2026-0015))
- [`support`] ObjectRelator 针对 ego-exo 对象对应任务，用 MCFuse 融合文本描述与视觉掩码、XObjAlign 做自监督跨视角对象对齐，在 Ego-Exo4D 上取得 SOTA。 ([2411.19083](https://arxiv.org/abs/2411.19083) / [EA-EGOEXO-2026-0013](evidence-appendix.md#ea-egoexo-2026-0013))
- [`support`] ObjectRelator 在 Ego-Exo4D 对象对应任务上较 PSALM 提升 IoU：Ego2Exo 39.7→44.3，Exo2Ego 44.1→49.2。 ([2411.19083](https://arxiv.org/abs/2411.19083) / [EA-EGOEXO-2026-0014](evidence-appendix.md#ea-egoexo-2026-0014))
- [`gap`] EgoExoLearn 的 cross-view association 基准显示，即使 co-training ego+exo 并使用 gaze，模型跨视角关联能力仍有限（Exo2Ego test 最高约 55.3% top-1），暴露出桥接异步 ego-exo 活动的显著 gap。 ([2403.16182](https://arxiv.org/abs/2403.16182) / [EA-EGOEXO-2026-0006](evidence-appendix.md#ea-egoexo-2026-0006))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `gap` EgoExoLearn 的 cross-view association 基准显示，即使 co-training ego+exo 并使用 gaze，模型跨视角关联能力仍有限（Exo2Ego test 最高约 55.3% top-1），暴露出桥接异步 ego-exo 活动的显著 gap。 ([2403.16182](https://arxiv.org/abs/2403.16182) / [EA-EGOEXO-2026-0006](evidence-appendix.md#ea-egoexo-2026-0006))

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
