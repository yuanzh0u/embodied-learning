# Writing Brief: 近一年具身智能预训练模型对数据源与采集参数的要求

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年具身智能预训练模型对数据源与采集参数的要求
- Time range: 2025-07-26..2026-07-26
- Knowledge IDs: `EA-DATA`, `EA-HARDWARE`, `EA-SENSOR`, `EA-MODEL`, `EA-XEMBODIMENT`
- Review mode: scoping
- Paper-level sources: 20 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 33

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DQ-YEAR-READ-0008](evidence-appendix.md#ea-dq-year-read-0008)) ⟷ SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DQ-YEAR-READ-0015](evidence-appendix.md#ea-dq-year-read-0015))
- `EA-DATA`: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([2512.13100](https://arxiv.org/abs/2512.13100) / [EA-DQ-YEAR-READ-0009](evidence-appendix.md#ea-dq-year-read-0009)) ⟷ 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- `EA-DATA`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-DQ-YEAR-READ-0010](evidence-appendix.md#ea-dq-year-read-0010)) ⟷ Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- `EA-DATA`: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0007](evidence-appendix.md#ea-ego-2026-0007)) ⟷ 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0005](evidence-appendix.md#ea-ego-2026-0005))
- `EA-DATA`: 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0002](evidence-appendix.md#ea-pretrain-data-2026-0002)) ⟷ 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0006](evidence-appendix.md#ea-ego-2026-0006))
- `EA-DATA`: 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。 ([2606.16253](https://arxiv.org/abs/2606.16253) / [EA-PRETRAIN-DATA-2026-0003](evidence-appendix.md#ea-pretrain-data-2026-0003)) ⟷ Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- `EA-MODEL`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-ALIGN-READ-0012](evidence-appendix.md#ea-align-read-0012)) ⟷ A recorded robot action is not a universal supervision signal: the same command can produce different motions across co... ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- `EA-SENSOR`: 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0001](evidence-appendix.md#ea-tactile-2026-0001)) ⟷ HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0002](evidence-appendix.md#ea-tactile-2026-0002))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (29 events)
- [`support`] 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DQ-YEAR-READ-0008](evidence-appendix.md#ea-dq-year-read-0008))
- [`support`] 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([2512.13100](https://arxiv.org/abs/2512.13100) / [EA-DQ-YEAR-READ-0009](evidence-appendix.md#ea-dq-year-read-0009))
- [`support`] 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0007](evidence-appendix.md#ea-ego-2026-0007))
- [`support`] 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-DQ-YEAR-READ-0010](evidence-appendix.md#ea-dq-year-read-0010))
- [`support`] 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。 ([2606.16253](https://arxiv.org/abs/2606.16253) / [EA-PRETRAIN-DATA-2026-0003](evidence-appendix.md#ea-pretrain-data-2026-0003))
- [`support`] 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0002](evidence-appendix.md#ea-pretrain-data-2026-0002))
- [`conditional`] VLA 对压缩往往呈‘轻压缩稳定、越过任务特定转折后骤降’，因此码率验收应看闭环成功曲线，不应只看人眼画质。 ([2512.11612](https://arxiv.org/abs/2512.11612) / [EA-PRETRAIN-DATA-2026-0005](evidence-appendix.md#ea-pretrain-data-2026-0005))
- [`conditional`] 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。 ([2512.11612](https://arxiv.org/abs/2512.11612) / [EA-PRETRAIN-DATA-2026-0006](evidence-appendix.md#ea-pretrain-data-2026-0006))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- [`conditional`] 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0008](evidence-appendix.md#ea-ego-2026-0008))
- [`conditional`] Retargeted ego-human 数据只能部分替代目标机器人示范：在论文的 Make Coffee co-training 实验中，没有 robot data 时成功始终接近 0。 ([2603.22264](https://arxiv.org/abs/2603.22264) / [EA-EGO-2026-0011](evidence-appendix.md#ea-ego-2026-0011))
- [`conditional`] UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data. ([2604.10647](https://arxiv.org/abs/2604.10647) / [EA-UMI-READ-0003](evidence-appendix.md#ea-umi-read-0003))
- [`conditional`] Physics refiner 和 interaction reward 是把 Ego-centric 视频数据变成可执行技能的必要中间层；只跟踪运动会在接触任务中失败。 ([2605.20373](https://arxiv.org/abs/2605.20373) / [EA-EGO-2026-0013](evidence-appendix.md#ea-ego-2026-0013))
- [`conditional`] 缩小 human/robot 图像外观差距并不足以让 ego 数据可训练；Water Flowers 消融中 visual-only 最高约 32.5%，显式 hand-object 6DoF ICT 才带来大幅闭环提升。 ([2605.24934](https://arxiv.org/abs/2605.24934) / [EA-EGO-2026-0014](evidence-appendix.md#ea-ego-2026-0014))
- [`conditional`] 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0017](evidence-appendix.md#ea-ego-2026-0017))
- [`conditional`] 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0018](evidence-appendix.md#ea-ego-2026-0018))
- [`conditional`] 带宽要求必须在目标 VLA 和任务上用闭环成功率标定，感知画质或单一固定 bpp 不能替代。 ([2606.16253](https://arxiv.org/abs/2606.16253) / [EA-PRETRAIN-DATA-2026-0004](evidence-appendix.md#ea-pretrain-data-2026-0004))
- [`conditional`] 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- [`limit`] 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- [`limit`] Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- [`limit`] 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0005](evidence-appendix.md#ea-ego-2026-0005))
- [`limit`] 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0006](evidence-appendix.md#ea-ego-2026-0006))
- [`limit`] Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- [`limit`] 将 egocentric hand trajectories 转为机器人可执行数据仍需 human-in-the-loop retargeting：基础坐标/形态偏差和 contact-rich 片段要人工校准。 ([2603.22264](https://arxiv.org/abs/2603.22264) / [EA-EGO-2026-0010](evidence-appendix.md#ea-ego-2026-0010))
- [`limit`] Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [EA-UMI-READ-0004](evidence-appendix.md#ea-umi-read-0004))
- [`limit`] 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。 ([2605.20373](https://arxiv.org/abs/2605.20373) / [EA-EGO-2026-0012](evidence-appendix.md#ea-ego-2026-0012))
- [`limit`] HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。 ([2605.24934](https://arxiv.org/abs/2605.24934) / [EA-EGO-2026-0015](evidence-appendix.md#ea-ego-2026-0015))
- [`limit`] Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- [`limit`] SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DQ-YEAR-READ-0015](evidence-appendix.md#ea-dq-year-read-0015))

### EA-MODEL (2 events)
- [`support`] DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-ALIGN-READ-0012](evidence-appendix.md#ea-align-read-0012))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))

### EA-SENSOR (2 events)
- [`support`] 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0001](evidence-appendix.md#ea-tactile-2026-0001))
- [`limit`] HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0002](evidence-appendix.md#ea-tactile-2026-0002))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` VLA 对压缩往往呈‘轻压缩稳定、越过任务特定转折后骤降’，因此码率验收应看闭环成功曲线，不应只看人眼画质。 ([2512.11612](https://arxiv.org/abs/2512.11612) / [EA-PRETRAIN-DATA-2026-0005](evidence-appendix.md#ea-pretrain-data-2026-0005))
- `conditional` 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。 ([2512.11612](https://arxiv.org/abs/2512.11612) / [EA-PRETRAIN-DATA-2026-0006](evidence-appendix.md#ea-pretrain-data-2026-0006))
- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- `conditional` 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0008](evidence-appendix.md#ea-ego-2026-0008))
- `conditional` Retargeted ego-human 数据只能部分替代目标机器人示范：在论文的 Make Coffee co-training 实验中，没有 robot data 时成功始终接近 0。 ([2603.22264](https://arxiv.org/abs/2603.22264) / [EA-EGO-2026-0011](evidence-appendix.md#ea-ego-2026-0011))
- `conditional` UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data. ([2604.10647](https://arxiv.org/abs/2604.10647) / [EA-UMI-READ-0003](evidence-appendix.md#ea-umi-read-0003))
- `conditional` Physics refiner 和 interaction reward 是把 Ego-centric 视频数据变成可执行技能的必要中间层；只跟踪运动会在接触任务中失败。 ([2605.20373](https://arxiv.org/abs/2605.20373) / [EA-EGO-2026-0013](evidence-appendix.md#ea-ego-2026-0013))
- `conditional` 缩小 human/robot 图像外观差距并不足以让 ego 数据可训练；Water Flowers 消融中 visual-only 最高约 32.5%，显式 hand-object 6DoF ICT 才带来大幅闭环提升。 ([2605.24934](https://arxiv.org/abs/2605.24934) / [EA-EGO-2026-0014](evidence-appendix.md#ea-ego-2026-0014))
- `conditional` 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0017](evidence-appendix.md#ea-ego-2026-0017))
- `conditional` 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0018](evidence-appendix.md#ea-ego-2026-0018))
- `conditional` 带宽要求必须在目标 VLA 和任务上用闭环成功率标定，感知画质或单一固定 bpp 不能替代。 ([2606.16253](https://arxiv.org/abs/2606.16253) / [EA-PRETRAIN-DATA-2026-0004](evidence-appendix.md#ea-pretrain-data-2026-0004))
- `conditional` 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- `limit` 从 egocentric 视频恢复的 object trajectory 不是完整机器人动作：该路线无法获得 gripper state，只能把动作表示为 9D 物体位姿增量。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0003](evidence-appendix.md#ea-ego-2026-0003))
- `limit` Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- `limit` 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0005](evidence-appendix.md#ea-ego-2026-0005))
- `limit` 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0006](evidence-appendix.md#ea-ego-2026-0006))
- `limit` Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- `limit` 将 egocentric hand trajectories 转为机器人可执行数据仍需 human-in-the-loop retargeting：基础坐标/形态偏差和 contact-rich 片段要人工校准。 ([2603.22264](https://arxiv.org/abs/2603.22264) / [EA-EGO-2026-0010](evidence-appendix.md#ea-ego-2026-0010))
- `limit` Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [EA-UMI-READ-0004](evidence-appendix.md#ea-umi-read-0004))
- `limit` 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。 ([2605.20373](https://arxiv.org/abs/2605.20373) / [EA-EGO-2026-0012](evidence-appendix.md#ea-ego-2026-0012))
- `limit` HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。 ([2605.24934](https://arxiv.org/abs/2605.24934) / [EA-EGO-2026-0015](evidence-appendix.md#ea-ego-2026-0015))
- `limit` Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- `limit` SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DQ-YEAR-READ-0015](evidence-appendix.md#ea-dq-year-read-0015))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))
- `limit` HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0002](evidence-appendix.md#ea-tactile-2026-0002))

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
