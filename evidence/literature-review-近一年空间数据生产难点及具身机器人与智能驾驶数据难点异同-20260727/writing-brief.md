# Writing Brief: 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同
- Time range: 2025-07-27..2026-07-27
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-4D`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 17 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 19

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a... ([2605.01799](https://arxiv.org/abs/2605.01799) / [EA-4DDATA-READ-0015](evidence-appendix.md#ea-4ddata-read-0015)) ⟷ Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or... ([2604.14089](https://arxiv.org/abs/2604.14089) / [EA-UMI-READ-0004](evidence-appendix.md#ea-umi-read-0004))
- `EA-DATA`: Production-grade HD-map ground truth is a multi-source and multi-pass QA product: occlusion-free aerial data and onboar... ([2606.02956](https://arxiv.org/abs/2606.02956) / [EA-SPATIAL-2026-0003](evidence-appendix.md#ea-spatial-2026-0003)) ⟷ Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- `EA-DATA`: Fleet-grade spatial truth requires an explicit pose-and-time production stack: urban GNSS degradation is mitigated with... ([2606.17080](https://arxiv.org/abs/2606.17080) / [EA-SPATIAL-2026-0005](evidence-appendix.md#ea-spatial-2026-0005)) ⟷ 4D radar auto-labeling remains bounded by the quality of the cross-modal teacher and correspondence: severe occlusion o... ([2601.21454](https://arxiv.org/abs/2601.21454) / [EA-SPATIAL-2026-0001](evidence-appendix.md#ea-spatial-2026-0001))
- `EA-DATA`: Vector HD-map ground truth is built on a globally registered dense 3D map and still requires expert geometry/topology a... ([2606.17080](https://arxiv.org/abs/2606.17080) / [EA-SPATIAL-2026-0006](evidence-appendix.md#ea-spatial-2026-0006)) ⟷ Synthetic occupancy generation does not escape the ground-truth bottleneck: OccSim reports that semantic occupancy stil... ([2603.28887](https://arxiv.org/abs/2603.28887) / [EA-SPATIAL-2026-0002](evidence-appendix.md#ea-spatial-2026-0002))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (17 events)
- [`support`] Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data. ([2605.01799](https://arxiv.org/abs/2605.01799) / [EA-4DDATA-READ-0015](evidence-appendix.md#ea-4ddata-read-0015))
- [`support`] Production-grade HD-map ground truth is a multi-source and multi-pass QA product: occlusion-free aerial data and onboard 3D sensing must be fused, map changes checked, geometry and topology manually... ([2606.02956](https://arxiv.org/abs/2606.02956) / [EA-SPATIAL-2026-0003](evidence-appendix.md#ea-spatial-2026-0003))
- [`support`] Fleet-grade spatial truth requires an explicit pose-and-time production stack: urban GNSS degradation is mitigated with LiDAR-inertial and INS fusion, cameras and LiDAR are disciplined to a master cl... ([2606.17080](https://arxiv.org/abs/2606.17080) / [EA-SPATIAL-2026-0005](evidence-appendix.md#ea-spatial-2026-0005))
- [`support`] Vector HD-map ground truth is built on a globally registered dense 3D map and still requires expert geometry/topology annotation plus visual verification; high-quality coordinates alone do not supply... ([2606.17080](https://arxiv.org/abs/2606.17080) / [EA-SPATIAL-2026-0006](evidence-appendix.md#ea-spatial-2026-0006))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- [`conditional`] 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4DDATA-READ-0009](evidence-appendix.md#ea-4ddata-read-0009))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-4DDATA-READ-0007](evidence-appendix.md#ea-4ddata-read-0007))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4DDATA-READ-0008](evidence-appendix.md#ea-4ddata-read-0008))
- [`conditional`] 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- [`limit`] 4D radar auto-labeling remains bounded by the quality of the cross-modal teacher and correspondence: severe occlusion or lighting can degrade visual segmentation, while image-plane overlap makes rada... ([2601.21454](https://arxiv.org/abs/2601.21454) / [EA-SPATIAL-2026-0001](evidence-appendix.md#ea-spatial-2026-0001))
- [`limit`] Synthetic occupancy generation does not escape the ground-truth bottleneck: OccSim reports that semantic occupancy still requires manual semantic annotation, leaving fewer than 100,000 training frame... ([2603.28887](https://arxiv.org/abs/2603.28887) / [EA-SPATIAL-2026-0002](evidence-appendix.md#ea-spatial-2026-0002))
- [`limit`] Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [EA-UMI-READ-0004](evidence-appendix.md#ea-umi-read-0004))
- [`limit`] Driving-data fragmentation is itself a production bottleneck: dataset-specific file formats, APIs, calibration conventions and modality coverage make preprocessing repeatedly reimplemented and cross-... ([2606.04271](https://arxiv.org/abs/2606.04271) / [EA-SPATIAL-2026-0004](evidence-appendix.md#ea-spatial-2026-0004))
- [`limit`] Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- [`limit`] Synthetic driving corner cases still require human or programmatic validation: even with explicit collision zones and CARLA execution, the LLM may fail under multiple constraints and only 29.4% of ge... ([2607.07601](https://arxiv.org/abs/2607.07601) / [EA-SPATIAL-2026-0007](evidence-appendix.md#ea-spatial-2026-0007))
- [`limit`] Safety-critical driving data is hard to produce because the desired distribution conflicts with natural occurrence: geographic coverage is narrow, routine safe interactions dominate, and raw trajecto... ([2607.16943](https://arxiv.org/abs/2607.16943) / [EA-SPATIAL-2026-0008](evidence-appendix.md#ea-spatial-2026-0008))
- [`limit`] Rule-generated risk labels remain provisional ground truth because they inherit errors from trajectories, maps and signal binding; auditability does not substitute for manual accuracy and threshold-s... ([2607.16943](https://arxiv.org/abs/2607.16943) / [EA-SPATIAL-2026-0009](evidence-appendix.md#ea-spatial-2026-0009))

### EA-MODEL (1 events)
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))

### EA-SENSOR (1 events)
- [`support`] 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0001](evidence-appendix.md#ea-tactile-2026-0001))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- `conditional` 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4DDATA-READ-0009](evidence-appendix.md#ea-4ddata-read-0009))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-4DDATA-READ-0007](evidence-appendix.md#ea-4ddata-read-0007))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-4DDATA-READ-0008](evidence-appendix.md#ea-4ddata-read-0008))
- `conditional` 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- `limit` 4D radar auto-labeling remains bounded by the quality of the cross-modal teacher and correspondence: severe occlusion or lighting can degrade visual segmentation, while image-plane overlap makes rada... ([2601.21454](https://arxiv.org/abs/2601.21454) / [EA-SPATIAL-2026-0001](evidence-appendix.md#ea-spatial-2026-0001))
- `limit` Synthetic occupancy generation does not escape the ground-truth bottleneck: OccSim reports that semantic occupancy still requires manual semantic annotation, leaving fewer than 100,000 training frame... ([2603.28887](https://arxiv.org/abs/2603.28887) / [EA-SPATIAL-2026-0002](evidence-appendix.md#ea-spatial-2026-0002))
- `limit` Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [EA-UMI-READ-0004](evidence-appendix.md#ea-umi-read-0004))
- `limit` Driving-data fragmentation is itself a production bottleneck: dataset-specific file formats, APIs, calibration conventions and modality coverage make preprocessing repeatedly reimplemented and cross-... ([2606.04271](https://arxiv.org/abs/2606.04271) / [EA-SPATIAL-2026-0004](evidence-appendix.md#ea-spatial-2026-0004))
- `limit` Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- `limit` Synthetic driving corner cases still require human or programmatic validation: even with explicit collision zones and CARLA execution, the LLM may fail under multiple constraints and only 29.4% of ge... ([2607.07601](https://arxiv.org/abs/2607.07601) / [EA-SPATIAL-2026-0007](evidence-appendix.md#ea-spatial-2026-0007))
- `limit` Safety-critical driving data is hard to produce because the desired distribution conflicts with natural occurrence: geographic coverage is narrow, routine safe interactions dominate, and raw trajecto... ([2607.16943](https://arxiv.org/abs/2607.16943) / [EA-SPATIAL-2026-0008](evidence-appendix.md#ea-spatial-2026-0008))
- `limit` Rule-generated risk labels remain provisional ground truth because they inherit errors from trajectories, maps and signal binding; auditability does not substitute for manual accuracy and threshold-s... ([2607.16943](https://arxiv.org/abs/2607.16943) / [EA-SPATIAL-2026-0009](evidence-appendix.md#ea-spatial-2026-0009))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))

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
