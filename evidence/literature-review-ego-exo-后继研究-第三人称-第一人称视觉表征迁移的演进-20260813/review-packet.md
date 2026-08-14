# Review Packet: Ego-Exo 后继研究：第三人称→第一人称视觉表征迁移的演进

## Scope

- Topic: Ego-Exo 后继研究：第三人称→第一人称视觉表征迁移的演进
- Time range: 2026-02-13..2026-08-13
- Review style: `survey`
- Knowledge IDs: `EA-XEMBODIMENT`, `EA-MODEL`, `EA-DATA`
- Evidence events: 20
- Topic cards: 0
- Registered source IDs available: not loaded

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 20
- Stance labels: `gap`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-EGOEXO-2026-0001`, `EA-EGOEXO-2026-0002`, `EA-EGOEXO-2026-0007`, `EA-EGOEXO-2026-0008`, `EA-EGOEXO-2026-0016`, `EA-EGOEXO-2026-0009`, `EA-EGOEXO-2026-0010`, `EA-EGOEXO-2026-0011`, `EA-EGOEXO-2026-0012`, `EA-EGOEXO-2026-0003`, `EA-EGOEXO-2026-0004`, `EA-EGOEXO-2026-0017`
- Registered sources: not loaded

## Evidence Sufficiency

- Evidence sufficiency: preliminary
- Review mode: scoping
- Paper-level sources: 11 / 15 floor (not a cap)
- Coverage and saturation gate: blocked
- Full text recovered: 11
- Structure mapped: 11
- Deep-read papers: 11
- Claim-verified papers: 11
- Accepted evidence papers: 0
- Paper-reading gate: blocked
- Formal outputs are blocked until the paper floor and every coverage/saturation check pass.
- Unresolved checks: coverage-report-missing, paper-reading-accepted-floor:0/15, paper-reading-ledger-mismatch:accepted-0<event-papers-11

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- No topic cards provided.

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 19 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2104.07905: Ego-Exo: Transferring Visual Representations from Third-person to First-person Videos | 2021-04-16 | support | EA-EGOEXO-2026-0001; EA-EGOEXO-2026-0002 |
| 2203.09905: Learning Affordance Grounding from Exocentric Images | 2022-03-18 | support | EA-EGOEXO-2026-0007; EA-EGOEXO-2026-0008 |
| 2208.13196: Grounded Affordance from Exocentric View | 2022-08-28 | support | EA-EGOEXO-2026-0016 |
| 2303.09665: LOCATE: Localize and Transfer Object Parts for Weakly Supervised Affordance Grounding | 2023-03-17 | support | EA-EGOEXO-2026-0009; EA-EGOEXO-2026-0010 |
| 2306.05526: Learning Fine-grained View-Invariant Representations from Unpaired Ego-Exo Videos via Temporal Alignment | 2023-06-10 | support | EA-EGOEXO-2026-0011; EA-EGOEXO-2026-0012 |
| 2311.18259: Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person Perspectives | 2023-11-30 | support | EA-EGOEXO-2026-0003; EA-EGOEXO-2026-0004 |
| 2312.02638: Synchronization is All You Need: Exocentric-to-Egocentric Transfer for Temporal Action Segmentation with Unlabeled Sync... | 2023-12-05 | support | EA-EGOEXO-2026-0017; EA-EGOEXO-2026-0018 |
| 2401.00789: EgoInstructor: Retrieval-Augmented Egocentric Video Captioning | 2024-01-01 | support | EA-EGOEXO-2026-0019; EA-EGOEXO-2026-0020 |
| 2403.16182: EgoExoLearn: A Dataset for Bridging Asynchronous Ego- and Exo-centric View of Procedural Activities in Real World | 2024-03-25 | gap, support | EA-EGOEXO-2026-0005; EA-EGOEXO-2026-0006 |
| 2406.08877: EgoExo-Fitness: Towards Egocentric and Exocentric Full-Body Action Understanding | 2024-06-13 | support | EA-EGOEXO-2026-0015 |
| 2411.19083: ObjectRelator: Enabling Cross-View Object Relation Understanding Across Ego-Centric and Exo-Centric Perspectives | 2024-11-28 | support | EA-EGOEXO-2026-0013; EA-EGOEXO-2026-0014 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-EGOEXO-2026-0001 | EA-XEMBODIMENT | `support` | `direct` | Ego-Exo 从大规模第三人称视频中挖掘 Ego-Score、Object-Score、Interaction-Map 三类 egocentric 信号，并以知识蒸馏损失在预训练时注入视频模型，从而无需配对或动作标注的 ego 视频。 | 摘要与方法部分直接陈述该核心思想与三类辅助任务。 (Abstract (full-text section)) | yanghao-li; tushar-nagarajan; bo-xiong; et al. | 2104.07905 |
| EA-EGOEXO-2026-0002 | EA-XEMBODIMENT | `support` | `direct` | Ego-Exo 在 Charades-Ego 上较 Kinetics 预训练基线提升 +3.26 mAP，并在 EPIC-Kitchens-100 取得当时 SOTA。 | 实验部分报告了相对标准预训练基线的提升幅度。 (1 Introduction) | yanghao-li; tushar-nagarajan; bo-xiong; et al. | 2104.07905 |
| EA-EGOEXO-2026-0007 | EA-XEMBODIMENT | `support` | `direct` | 该工作提出从 exocentric 视角的 affordance grounding：从第三人称人-物交互图像学习可供性知识并迁移到 egocentric 物体图像，仅用 affordance 标签监督，并构建 AGD20K 数据集。 | 摘要直接陈述该任务设定与数据集。 (Abstract (full-text section)) | hongcheng-luo; wei-zhai; jing-zhang; et al. | 2203.09905 |
| EA-EGOEXO-2026-0008 | EA-XEMBODIMENT | `support` | `direct` | 在 seen 设定下，该方法 KLD 较最佳 saliency 模型提升 17.2%，较 affordance grounding 模型提升 13.3%。 | 实验部分报告相对各基线的提升幅度。 (5.2 Quantitative and Qualitative Comparisons) | hongcheng-luo; wei-zhai; jing-zhang; et al. | 2203.09905 |
| EA-EGOEXO-2026-0016 | EA-XEMBODIMENT | `support` | `direct` | 该期刊版在会议版基础上引入 Cross-view Feature Transfer（CFT）模块，通过密集匹配显式建模人与人之间的 interaction bias，扩展 AGD20K 至 26,117 图像。 | 引言与摘要陈述 CFT 模块与 interaction bias 建模。 (Abstract (full-text section)) | hongcheng-luo; wei-zhai; jing-zhang; et al. | 2208.13196 |
| EA-EGOEXO-2026-0009 | EA-XEMBODIMENT | `support` | `direct` | LOCATE 提出部件级知识迁移：定位 exo 交互区域、用 PartSelect 选出物体部件原型，再以此监督 egocentric affordance grounding，仅用图像级标签弱监督。 | 摘要与方法部分直接陈述部件级迁移机制。 (Abstract (full-text section)) | gen-li; varun-jampani; deqing-sun; et al. | 2303.09665 |
| EA-EGOEXO-2026-0010 | EA-XEMBODIMENT | `support` | `direct` | 在 unseen 设定下，LOCATE 较 SOTA 方法 Cross-view-AG+ 提升 KLD 20.4%、SIM 33.3%、NSS 31.2%。 | 实验部分报告相对 Cross-view-AG+ 的提升。 (4.2 Comparison to State-of-the-Art) | gen-li; varun-jampani; deqing-sun; et al. | 2303.09665 |
| EA-EGOEXO-2026-0011 | EA-XEMBODIMENT | `support` | `direct` | AE2 从 unpaired 的 ego-exo 视频学习细粒度视角不变表征：用 object-centric 编码器关注手与主动物体，以 DTW 时序对齐作自监督目标，并用反转帧作负样本对比正则。 | 摘要与方法部分直接陈述三个关键设计。 (1 Introduction) | zihui-xue; kristen-grauman | 2306.05526 |
| EA-EGOEXO-2026-0012 | EA-XEMBODIMENT | `support` | `direct` | AE2 在四个数据集、regular 与 cross-view 设定上全面超越 SOTA（如 Break Eggs 动作相位分类 F1 66.23 vs 最佳基线 GTA 56.86）。 | 实验表 1 报告各数据集分类/检索指标。 (5 Experiments) | zihui-xue; kristen-grauman | 2306.05526 |
| EA-EGOEXO-2026-0003 | EA-XEMBODIMENT | `support` | `direct` | Ego-Exo4D 是迄今最大的时间同步第一+第三人称视频数据集，共 1286 小时、740 名参与者、覆盖 8 个领域技能活动，并配多模态与专家评论等语言标注。 | 摘要与数据集部分直接报告规模与模态。 (Abstract (full-text section)) | kristen-grauman; andrew-westbury; lorenzo-torresani; et al. | 2311.18259 |
| EA-EGOEXO-2026-0004 | EA-XEMBODIMENT | `support` | `direct` | Ego-Exo4D 首次形式化 ego-exo relation 任务族（对象级对应 correspondence 与视角翻译 translation），使 first↔third-person 视角迁移成为可评测的基准任务。 | 基准任务部分定义 ego-exo relation 家族。 (1 Introduction) | kristen-grauman; andrew-westbury; lorenzo-torresani; et al. | 2311.18259 |
| EA-EGOEXO-2026-0017 | EA-XEMBODIMENT | `support` | `direct` | 该工作用无标注的同步 exo-ego 视频对做知识蒸馏，把时序动作分割模型从 exo 迁移到 ego，无需任何 ego 标签，并在 Assembly101 与 EgoExo4D 上验证。 | 摘要与方法部分直接陈述该设定与方法。 (Abstract (full-text section)) | camillo-quattrocchi; antonino-furnari; daniele-di-mauro; et al. | 2312.02638 |
| EA-EGOEXO-2026-0018 | EA-XEMBODIMENT | `support` | `direct` | 同步蒸馏最佳模型在 Assembly101 上与监督式 ego-oracle 相当（edit 28.59 vs 26.42），远超仅用 exo 数据的基线（edit 12.60）。 | 实验表 1 报告 edit 分数对比。 (5.1 Performance of the Proposed Approach) | camillo-quattrocchi; antonino-furnari; daniele-di-mauro; et al. | 2312.02638 |
| EA-EGOEXO-2026-0019 | EA-XEMBODIMENT | `support` | `direct` | EgoInstructor 用自动挖掘的 ego-exo 视频对训练跨视角检索模块，检索语义相关的第三人称教学视频作参考，增强 egocentric 视频描述。 | 摘要直接陈述检索增强框架。 (Abstract (full-text section)) | jilan-xu; yifei-huang; junlin-hou; et al. | 2401.00789 |
| EA-EGOEXO-2026-0020 | EA-XEMBODIMENT | `support` | `direct` | EgoInstructor 的跨视角检索模块在 7 个 benchmark 上一致提升，如 InternVideo 在 CharadesEgo 上 Ego2Exo/Exo2Ego 分别提升 15.9% 与 7.7%。 | 实验部分报告跨视角检索提升幅度。 (4.2.1 Results on Cross-view Retrieval) | jilan-xu; yifei-huang; junlin-hou; et al. | 2401.00789 |
| EA-EGOEXO-2026-0005 | EA-XEMBODIMENT | `support` | `direct` | EgoExoLearn 将 ego-exo 迁移推进到异步、异环境的演示跟随（demo-following）设定：个体观看 exo 演示后在佩戴 gaze 设备的情况下于不同环境复现程序性任务，共 120 小时。 | 摘要与数据收集部分直接描述该设定与规模。 (Abstract (full-text section)) | yifei-huang; guo-chen; jilan-xu; et al. | 2403.16182 |
| EA-EGOEXO-2026-0015 | EA-XEMBODIMENT | `support` | `direct` | EgoExo-Fitness 提供 32 小时、1276 段同步 egocentric+exocentric 全身健身动作数据集，并引入技术关键点核验、自然语言评语、质量分等可解释动作评判标注。 | 摘要直接陈述数据集规模与标注。 (1 Introduction) | yuan-ming-li; wei-jin-huang; an-lan-wang; et al. | 2406.08877 |
| EA-EGOEXO-2026-0013 | EA-XEMBODIMENT | `support` | `direct` | ObjectRelator 针对 ego-exo 对象对应任务，用 MCFuse 融合文本描述与视觉掩码、XObjAlign 做自监督跨视角对象对齐，在 Ego-Exo4D 上取得 SOTA。 | 摘要与引言直接陈述方法与任务。 (Abstract (full-text section)) | yu-fu; runze-wang; bin-ren; et al. | 2411.19083 |
| EA-EGOEXO-2026-0014 | EA-XEMBODIMENT | `support` | `direct` | ObjectRelator 在 Ego-Exo4D 对象对应任务上较 PSALM 提升 IoU：Ego2Exo 39.7→44.3，Exo2Ego 44.1→49.2。 | 主结果表 2 报告 IoU 对比。 (4.1 Main Results on Ego-Exo4D) | yu-fu; runze-wang; bin-ren; et al. | 2411.19083 |
| EA-EGOEXO-2026-0006 | EA-XEMBODIMENT | `gap` | `direct` | EgoExoLearn 的 cross-view association 基准显示，即使 co-training ego+exo 并使用 gaze，模型跨视角关联能力仍有限（Exo2Ego test 最高约 55.3% top-1），暴露出桥接异步 ego-exo 活动的显著 gap。 | 实验结果部分报告该基准的准确率并据此指出模型局限。 (4.2.1 Cross-view association) | yifei-huang; guo-chen; jilan-xu; et al. | 2403.16182 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-EGOEXO-2026-0001 | yanghao-li; tushar-nagarajan; bo-xiong; et al. | unlisted | `support` | Ego-Exo 从大规模第三人称视频中挖掘 Ego-Score、Object-Score、Interaction-Map 三类 egocentric 信号，并以知识蒸馏损失在预训练时注入视频模型，从而无需配对或动作标注的 ego 视频。 |
| EA-EGOEXO-2026-0002 | yanghao-li; tushar-nagarajan; bo-xiong; et al. | unlisted | `support` | Ego-Exo 在 Charades-Ego 上较 Kinetics 预训练基线提升 +3.26 mAP，并在 EPIC-Kitchens-100 取得当时 SOTA。 |
| EA-EGOEXO-2026-0007 | hongcheng-luo; wei-zhai; jing-zhang; et al. | unlisted | `support` | 该工作提出从 exocentric 视角的 affordance grounding：从第三人称人-物交互图像学习可供性知识并迁移到 egocentric 物体图像，仅用 affordance 标签监督，并构建 AGD20K 数据集。 |
| EA-EGOEXO-2026-0008 | hongcheng-luo; wei-zhai; jing-zhang; et al. | unlisted | `support` | 在 seen 设定下，该方法 KLD 较最佳 saliency 模型提升 17.2%，较 affordance grounding 模型提升 13.3%。 |
| EA-EGOEXO-2026-0016 | hongcheng-luo; wei-zhai; jing-zhang; et al. | unlisted | `support` | 该期刊版在会议版基础上引入 Cross-view Feature Transfer（CFT）模块，通过密集匹配显式建模人与人之间的 interaction bias，扩展 AGD20K 至 26,117 图像。 |
| EA-EGOEXO-2026-0009 | gen-li; varun-jampani; deqing-sun; et al. | unlisted | `support` | LOCATE 提出部件级知识迁移：定位 exo 交互区域、用 PartSelect 选出物体部件原型，再以此监督 egocentric affordance grounding，仅用图像级标签弱监督。 |
| EA-EGOEXO-2026-0010 | gen-li; varun-jampani; deqing-sun; et al. | unlisted | `support` | 在 unseen 设定下，LOCATE 较 SOTA 方法 Cross-view-AG+ 提升 KLD 20.4%、SIM 33.3%、NSS 31.2%。 |
| EA-EGOEXO-2026-0011 | zihui-xue; kristen-grauman | unlisted | `support` | AE2 从 unpaired 的 ego-exo 视频学习细粒度视角不变表征：用 object-centric 编码器关注手与主动物体，以 DTW 时序对齐作自监督目标，并用反转帧作负样本对比正则。 |
| EA-EGOEXO-2026-0012 | zihui-xue; kristen-grauman | unlisted | `support` | AE2 在四个数据集、regular 与 cross-view 设定上全面超越 SOTA（如 Break Eggs 动作相位分类 F1 66.23 vs 最佳基线 GTA 56.86）。 |
| EA-EGOEXO-2026-0003 | kristen-grauman; andrew-westbury; lorenzo-torresani; et al. | unlisted | `support` | Ego-Exo4D 是迄今最大的时间同步第一+第三人称视频数据集，共 1286 小时、740 名参与者、覆盖 8 个领域技能活动，并配多模态与专家评论等语言标注。 |
| EA-EGOEXO-2026-0004 | kristen-grauman; andrew-westbury; lorenzo-torresani; et al. | unlisted | `support` | Ego-Exo4D 首次形式化 ego-exo relation 任务族（对象级对应 correspondence 与视角翻译 translation），使 first↔third-person 视角迁移成为可评测的基准任务。 |
| EA-EGOEXO-2026-0017 | camillo-quattrocchi; antonino-furnari; daniele-di-mauro; et al. | unlisted | `support` | 该工作用无标注的同步 exo-ego 视频对做知识蒸馏，把时序动作分割模型从 exo 迁移到 ego，无需任何 ego 标签，并在 Assembly101 与 EgoExo4D 上验证。 |
| EA-EGOEXO-2026-0018 | camillo-quattrocchi; antonino-furnari; daniele-di-mauro; et al. | unlisted | `support` | 同步蒸馏最佳模型在 Assembly101 上与监督式 ego-oracle 相当（edit 28.59 vs 26.42），远超仅用 exo 数据的基线（edit 12.60）。 |
| EA-EGOEXO-2026-0019 | jilan-xu; yifei-huang; junlin-hou; et al. | unlisted | `support` | EgoInstructor 用自动挖掘的 ego-exo 视频对训练跨视角检索模块，检索语义相关的第三人称教学视频作参考，增强 egocentric 视频描述。 |
| EA-EGOEXO-2026-0020 | jilan-xu; yifei-huang; junlin-hou; et al. | unlisted | `support` | EgoInstructor 的跨视角检索模块在 7 个 benchmark 上一致提升，如 InternVideo 在 CharadesEgo 上 Ego2Exo/Exo2Ego 分别提升 15.9% 与 7.7%。 |
| EA-EGOEXO-2026-0005 | yifei-huang; guo-chen; jilan-xu; et al. | unlisted | `support` | EgoExoLearn 将 ego-exo 迁移推进到异步、异环境的演示跟随（demo-following）设定：个体观看 exo 演示后在佩戴 gaze 设备的情况下于不同环境复现程序性任务，共 120 小时。 |
| EA-EGOEXO-2026-0015 | yuan-ming-li; wei-jin-huang; an-lan-wang; et al. | unlisted | `support` | EgoExo-Fitness 提供 32 小时、1276 段同步 egocentric+exocentric 全身健身动作数据集，并引入技术关键点核验、自然语言评语、质量分等可解释动作评判标注。 |
| EA-EGOEXO-2026-0013 | yu-fu; runze-wang; bin-ren; et al. | unlisted | `support` | ObjectRelator 针对 ego-exo 对象对应任务，用 MCFuse 融合文本描述与视觉掩码、XObjAlign 做自监督跨视角对象对齐，在 Ego-Exo4D 上取得 SOTA。 |
| EA-EGOEXO-2026-0014 | yu-fu; runze-wang; bin-ren; et al. | unlisted | `support` | ObjectRelator 在 Ego-Exo4D 对象对应任务上较 PSALM 提升 IoU：Ego2Exo 39.7→44.3，Exo2Ego 44.1→49.2。 |
| EA-EGOEXO-2026-0006 | yifei-huang; guo-chen; jilan-xu; et al. | unlisted | `gap` | EgoExoLearn 的 cross-view association 基准显示，即使 co-training ego+exo 并使用 gaze，模型跨视角关联能力仍有限（Exo2Ego test 最高约 55.3% top-1），暴露出桥接异步 ego-exo 活动的显著 gap。 |

## Synthesis Slots

### 共识/正向证据
- `EA-EGOEXO-2026-0001`: Ego-Exo 从大规模第三人称视频中挖掘 Ego-Score、Object-Score、Interaction-Map 三类 egocentric 信号，并以知识蒸馏损失在预训练时注入视频模型，从而无需配对或动作标注的 ego 视频。
- `EA-EGOEXO-2026-0002`: Ego-Exo 在 Charades-Ego 上较 Kinetics 预训练基线提升 +3.26 mAP，并在 EPIC-Kitchens-100 取得当时 SOTA。
- `EA-EGOEXO-2026-0007`: 该工作提出从 exocentric 视角的 affordance grounding：从第三人称人-物交互图像学习可供性知识并迁移到 egocentric 物体图像，仅用 affordance 标签监督，并构建 AGD20K 数据集。
- `EA-EGOEXO-2026-0008`: 在 seen 设定下，该方法 KLD 较最佳 saliency 模型提升 17.2%，较 affordance grounding 模型提升 13.3%。
- `EA-EGOEXO-2026-0016`: 该期刊版在会议版基础上引入 Cross-view Feature Transfer（CFT）模块，通过密集匹配显式建模人与人之间的 interaction bias，扩展 AGD20K 至 26,117 图像。
- `EA-EGOEXO-2026-0009`: LOCATE 提出部件级知识迁移：定位 exo 交互区域、用 PartSelect 选出物体部件原型，再以此监督 egocentric affordance grounding，仅用图像级标签弱监督。
- `EA-EGOEXO-2026-0010`: 在 unseen 设定下，LOCATE 较 SOTA 方法 Cross-view-AG+ 提升 KLD 20.4%、SIM 33.3%、NSS 31.2%。
- `EA-EGOEXO-2026-0011`: AE2 从 unpaired 的 ego-exo 视频学习细粒度视角不变表征：用 object-centric 编码器关注手与主动物体，以 DTW 时序对齐作自监督目标，并用反转帧作负样本对比正则。
### 开放问题
- `EA-EGOEXO-2026-0006`: EgoExoLearn 的 cross-view association 基准显示，即使 co-training ego+exo 并使用 gaze，模型跨视角关联能力仍有限（Exo2Ego test 最高约 55.3% top-1），暴露出桥接异步 ego-exo 活动的显著 gap。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: preliminary
- Paper-level sources: 11 / 15 floor (not a cap)
- Recommended default: preliminary-packet
- Core claims:
  - `EA-EGOEXO-2026-0001` Ego-Exo 从大规模第三人称视频中挖掘 Ego-Score、Object-Score、Interaction-Map 三类 egocentric 信号，并以知识蒸馏损失在预训练时注入视频模型，从而无需配对或动作标注的 ego 视频。
  - `EA-EGOEXO-2026-0002` Ego-Exo 在 Charades-Ego 上较 Kinetics 预训练基线提升 +3.26 mAP，并在 EPIC-Kitchens-100 取得当时 SOTA。
  - `EA-EGOEXO-2026-0007` 该工作提出从 exocentric 视角的 affordance grounding：从第三人称人-物交互图像学习可供性知识并迁移到 egocentric 物体图像，仅用 affordance 标签监督，并构建 AGD20K 数据集。
- Scientific memo preview: 《Ego-Exo 后继研究：第三人称→第一人称视觉表征迁移的演进》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: Ego-Exo 后继研究：第三人称→第一人称视觉表征迁移的演进 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: Ego-Exo 后继研究：第三人称→第一人称视觉表征迁移的演进: 先看证据边界，再谈一个可传播的反常识洞察。

## Draft Outline

1. 研究边界与证据范围
2. 概念与问题结构
3. 主要共识
4. 条件、限制与分歧
5. 未解决问题
6. 对后续研究/项目的启发

## Traceability Checklist

- Cite event IDs for paper-specific claims.
- Cite stable source IDs for topic-card background.
- Mark cross-event synthesis as `inference` with a short reason.
- Do not cite candidate-only papers as accepted evidence.
- Open raw sources before using exact wording.
