# Writing Brief: 近一年具身智能论文中的数据时空一致性

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年具身智能论文中的数据时空一致性
- Time range: 2025-07-27..2026-07-27
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-4D`, `EA-ALIGN`
- Review mode: scoping
- Paper-level sources: 20 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 20

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-READ-0003](evidence-appendix.md#ea-twm-read-0003)) ⟷ Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- `EA-DATA`: MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD o... ([2602.09878](https://arxiv.org/abs/2602.09878) / [EA-4D-READ-0014](evidence-appendix.md#ea-4d-read-0014)) ⟷ 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- `EA-DATA`: Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a... ([2605.01799](https://arxiv.org/abs/2605.01799) / [EA-4D-READ-0015](evidence-appendix.md#ea-4d-read-0015)) ⟷ HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-4D-READ-0010](evidence-appendix.md#ea-4d-read-0010))
- `EA-DATA`: Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinem... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-4D-READ-0005](evidence-appendix.md#ea-4d-read-0005)) ⟷ VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-READ-0001](evidence-appendix.md#ea-twm-read-0001))
- `EA-DATA`: WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency o... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-4D-READ-0003](evidence-appendix.md#ea-4d-read-0003)) ⟷ 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-READ-0007](evidence-appendix.md#ea-twm-read-0007))
- `EA-DATA`: 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。 ([2606.16253](https://arxiv.org/abs/2606.16253) / [EA-PRETRAIN-DATA-2026-0003](evidence-appendix.md#ea-pretrain-data-2026-0003)) ⟷ 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-TWM-READ-0014](evidence-appendix.md#ea-twm-read-0014))
- `EA-DATA`: Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-4D-READ-0013](evidence-appendix.md#ea-4d-read-0013)) ⟷ 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- `EA-MODEL`: H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0001](evidence-appendix.md#ea-vlabreak-2026-0001)) ⟷ 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (15 events)
- [`support`] MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD generation from a single-view RGBD observation and fuses the generated views into a more complete 3D structure over... ([2602.09878](https://arxiv.org/abs/2602.09878) / [EA-4D-READ-0014](evidence-appendix.md#ea-4d-read-0014))
- [`support`] Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model predicts environment... ([2603.16669](https://arxiv.org/abs/2603.16669) / [EA-4D-READ-0005](evidence-appendix.md#ea-4d-read-0005))
- [`support`] Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view video transformation and a 3D-aware compositional synthesis pipeline for training data. ([2605.01799](https://arxiv.org/abs/2605.01799) / [EA-4D-READ-0015](evidence-appendix.md#ea-4d-read-0015))
- [`support`] Dream-Tac将动作块、未来视觉和未来触觉放进同一世界动作建模目标，以弥补单纯视觉未来对接触互动线索的不足。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-4D-READ-0013](evidence-appendix.md#ea-4d-read-0013))
- [`support`] WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, improvement, and planni... ([2606.13672](https://arxiv.org/abs/2606.13672) / [EA-4D-READ-0003](evidence-appendix.md#ea-4d-read-0003))
- [`support`] 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-READ-0003](evidence-appendix.md#ea-twm-read-0003))
- [`support`] 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。 ([2606.16253](https://arxiv.org/abs/2606.16253) / [EA-PRETRAIN-DATA-2026-0003](evidence-appendix.md#ea-pretrain-data-2026-0003))
- [`conditional`] 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。 ([2512.11612](https://arxiv.org/abs/2512.11612) / [EA-PRETRAIN-DATA-2026-0006](evidence-appendix.md#ea-pretrain-data-2026-0006))
- [`conditional`] VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-READ-0001](evidence-appendix.md#ea-twm-read-0001))
- [`conditional`] 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- [`conditional`] 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-READ-0007](evidence-appendix.md#ea-twm-read-0007))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-4D-READ-0010](evidence-appendix.md#ea-4d-read-0010))
- [`conditional`] 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-TWM-READ-0014](evidence-appendix.md#ea-twm-read-0014))
- [`conditional`] 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- [`limit`] Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))

### EA-MODEL (3 events)
- [`support`] H-WM 用低频符号逻辑转移维持全局顺序，用潜在视觉子目标把逻辑状态落到感知空间，再由高频 VLA 执行动作 chunk。 ([2602.11291](https://arxiv.org/abs/2602.11291) / [EA-VLABREAK-2026-0001](evidence-appendix.md#ea-vlabreak-2026-0001))
- [`limit`] Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- [`limit`] 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))

### EA-SENSOR (2 events)
- [`support`] 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0001](evidence-appendix.md#ea-tactile-2026-0001))
- [`support`] RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 ([2606.29384](https://arxiv.org/abs/2606.29384) / [EA-SENSORERR-READ-0011](evidence-appendix.md#ea-sensorerr-read-0011))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。 ([2512.11612](https://arxiv.org/abs/2512.11612) / [EA-PRETRAIN-DATA-2026-0006](evidence-appendix.md#ea-pretrain-data-2026-0006))
- `conditional` VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-READ-0001](evidence-appendix.md#ea-twm-read-0001))
- `conditional` 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- `conditional` 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-READ-0007](evidence-appendix.md#ea-twm-read-0007))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-4D-READ-0010](evidence-appendix.md#ea-4d-read-0010))
- `conditional` 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-TWM-READ-0014](evidence-appendix.md#ea-twm-read-0014))
- `conditional` 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- `limit` Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- `limit` Offline VLA indicators can fail to transfer to stable real-robot behavior when action semantics, coordinate frames, temporal modality alignment, image preprocessing, and dataset coverage are not cont... ([2606.30456](https://arxiv.org/abs/2606.30456) / [EA-ALIGN-READ-0004](evidence-appendix.md#ea-align-read-0004))
- `limit` 对 WAM 的安全监测不能只检查‘想象的未来是否看起来合理’，还必须验证未来与实际执行动作在闭环中是否同步。 ([2607.15207](https://arxiv.org/abs/2607.15207) / [EA-VLABREAK-2026-0007](evidence-appendix.md#ea-vlabreak-2026-0007))

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
