# Writing Brief: 第三视角视频数据对ego数据采集和预训练的帮助

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 第三视角视频数据对ego数据采集和预训练的帮助
- Time range: 2025-08-12..2026-08-12
- Knowledge IDs: `EA-DATA`, `EA-MODEL`, `EA-XEMBODIMENT`, `EA-SENSOR`
- Review mode: scoping
- Paper-level sources: 26 / 15 floor (not a cap)
- Coverage and saturation gate: blocked
- Writing readiness: preliminary
- Unresolved checks: candidate_floor, full_text_floor, coverage_dimensions, saturation
- Accepted events: 48

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DQ-YEAR-READ-0008](evidence-appendix.md#ea-dq-year-read-0008)) ⟷ SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DQ-YEAR-READ-0015](evidence-appendix.md#ea-dq-year-read-0015))
- `EA-DATA`: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([2512.13100](https://arxiv.org/abs/2512.13100) / [EA-DQ-YEAR-READ-0009](evidence-appendix.md#ea-dq-year-read-0009)) ⟷ Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- `EA-DATA`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-DQ-YEAR-READ-0010](evidence-appendix.md#ea-dq-year-read-0010)) ⟷ 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0005](evidence-appendix.md#ea-ego-2026-0005))
- `EA-DATA`: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0007](evidence-appendix.md#ea-ego-2026-0007)) ⟷ 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0006](evidence-appendix.md#ea-ego-2026-0006))
- `EA-DATA`: 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0002](evidence-appendix.md#ea-pretrain-data-2026-0002)) ⟷ Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- `EA-DATA`: 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。 ([2606.16253](https://arxiv.org/abs/2606.16253) / [EA-PRETRAIN-DATA-2026-0003](evidence-appendix.md#ea-pretrain-data-2026-0003)) ⟷ 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。 ([2605.20373](https://arxiv.org/abs/2605.20373) / [EA-EGO-2026-0012](evidence-appendix.md#ea-ego-2026-0012))
- `EA-DATA`: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-WMDATA-READ-0001](evidence-appendix.md#ea-wmdata-read-0001)) ⟷ HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。 ([2605.24934](https://arxiv.org/abs/2605.24934) / [EA-EGO-2026-0015](evidence-appendix.md#ea-ego-2026-0015))
- `EA-MODEL`: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-ALIGN-READ-0012](evidence-appendix.md#ea-align-read-0012)) ⟷ A recorded robot action is not a universal supervision signal: the same command can produce different motions across co... ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (25 events)
- [`support`] 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DQ-YEAR-READ-0008](evidence-appendix.md#ea-dq-year-read-0008))
- [`support`] 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([2512.13100](https://arxiv.org/abs/2512.13100) / [EA-DQ-YEAR-READ-0009](evidence-appendix.md#ea-dq-year-read-0009))
- [`support`] 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0007](evidence-appendix.md#ea-ego-2026-0007))
- [`support`] τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-WMDATA-READ-0001](evidence-appendix.md#ea-wmdata-read-0001))
- [`support`] 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-DQ-YEAR-READ-0010](evidence-appendix.md#ea-dq-year-read-0010))
- [`support`] 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。 ([2606.16253](https://arxiv.org/abs/2606.16253) / [EA-PRETRAIN-DATA-2026-0003](evidence-appendix.md#ea-pretrain-data-2026-0003))
- [`support`] 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0002](evidence-appendix.md#ea-pretrain-data-2026-0002))
- [`conditional`] 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。 ([2512.11612](https://arxiv.org/abs/2512.11612) / [EA-PRETRAIN-DATA-2026-0006](evidence-appendix.md#ea-pretrain-data-2026-0006))
- [`conditional`] UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only dat... ([2601.09988](https://arxiv.org/abs/2601.09988) / [EA-UMI-READ-0002](evidence-appendix.md#ea-umi-read-0002))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- [`conditional`] 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0008](evidence-appendix.md#ea-ego-2026-0008))
- [`conditional`] UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data. ([2604.10647](https://arxiv.org/abs/2604.10647) / [EA-UMI-READ-0003](evidence-appendix.md#ea-umi-read-0003))
- [`conditional`] 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0017](evidence-appendix.md#ea-ego-2026-0017))
- [`conditional`] 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0018](evidence-appendix.md#ea-ego-2026-0018))
- [`conditional`] 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- [`limit`] Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- [`limit`] 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0005](evidence-appendix.md#ea-ego-2026-0005))
- [`limit`] 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0006](evidence-appendix.md#ea-ego-2026-0006))
- [`limit`] Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- [`limit`] Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [EA-UMI-READ-0004](evidence-appendix.md#ea-umi-read-0004))
- [`limit`] 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。 ([2605.20373](https://arxiv.org/abs/2605.20373) / [EA-EGO-2026-0012](evidence-appendix.md#ea-ego-2026-0012))
- [`limit`] HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。 ([2605.24934](https://arxiv.org/abs/2605.24934) / [EA-EGO-2026-0015](evidence-appendix.md#ea-ego-2026-0015))
- [`limit`] Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- [`limit`] Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。 ([2607.03828](https://arxiv.org/abs/2607.03828) / [EA-EGO-2026-0019](evidence-appendix.md#ea-ego-2026-0019))
- [`limit`] SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DQ-YEAR-READ-0015](evidence-appendix.md#ea-dq-year-read-0015))

### EA-MODEL (2 events)
- [`support`] DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-ALIGN-READ-0012](evidence-appendix.md#ea-align-read-0012))
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-READ-0001](evidence-appendix.md#ea-align-read-0001))

### EA-SENSOR (2 events)
- [`support`] 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0001](evidence-appendix.md#ea-tactile-2026-0001))
- [`limit`] HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0002](evidence-appendix.md#ea-tactile-2026-0002))

### unknown (19 events)
- [`support`] 第三人称(exocentric)视频可转化为第一人称(egocentric)视角,为机器人和AR/VR领域的模仿、推理和交互提供关键的第一人称感知能力 ([2512.08269](https://arxiv.org/abs/2512.08269) / [EA-EXO-EGO-2026-0001](evidence-appendix.md#ea-exo-ego-2026-0001))
- [`support`] exocentric视频的latent特征为egocentric视频生成提供更广泛的场景上下文,弥补ego先验渲染中缺失的场景信息 ([2512.08269](https://arxiv.org/abs/2512.08269) / [EA-EXO-EGO-2026-0002](evidence-appendix.md#ea-exo-ego-2026-0002))
- [`support`] 利用预训练大规模视频扩散模型的时空知识,通过轻量LoRA适配即可从单个exocentric视频生成高质量egocentric视频,并对未见场景具有强泛化能力 ([2512.08269](https://arxiv.org/abs/2512.08269) / [EA-EXO-EGO-2026-0003](evidence-appendix.md#ea-exo-ego-2026-0003))
- [`support`] egocentric人类视频提供可大规模采集的替代数据源,相比机器人遥操作可在多样化物体、环境和任务变体中大规模收集手部交互数据 ([2608.02580](https://arxiv.org/abs/2608.02580) / [EA-EXO-EGO-2026-0006](evidence-appendix.md#ea-exo-ego-2026-0006))
- [`support`] 在ego2robot合成数据与机器人数据上联合预训练,持续提升OOD泛化性能,增益在视觉外观、具身形态和语义扰动下最为显著,表明ego数据主要提升不变性和跨分布鲁棒性 ([2608.02580](https://arxiv.org/abs/2608.02580) / [EA-EXO-EGO-2026-0007](evidence-appendix.md#ea-exo-ego-2026-0007))
- [`support`] 在15种形态的Ego2R数据基础上加入原始ego视频数据,性能从33.5%跃升至37.3%,原始ego数据有效充当第16种'形态',通过略微不同的视觉外观和动作分布进一步丰富预训练多样性 ([2608.02580](https://arxiv.org/abs/2608.02580) / [EA-EXO-EGO-2026-0009](evidence-appendix.md#ea-exo-ego-2026-0009))
- [`support`] Egocentric视频预训练为VLA提供跨本体知识（cross-embodiment knowledge），完全丢弃人类数据会浪费预训练获得的跨本体知识和对真实世界部署的泛化能力。这间接支持了人类视频数据（包括潜在的第三视角数据）对ego预训练的价值。 ([2608.04196](https://arxiv.org/abs/2608.04196) / [EA-EXO-EGO-2026-0012](evidence-appendix.md#ea-exo-ego-2026-0012))
- [`support`] 第三视角视频与第一视角视频互补：第一视角保留动作执行视角，暴露接触动力学、手-物体关系、时间意图和运动决策的视觉后果；第三视角补充全身运动、姿态、交互上下文、周围智能体和场景级动态，使这些信息更易观察。 ([2605.06747](https://arxiv.org/abs/2605.06747) / [EA-EXO-EGO-2026-0015](evidence-appendix.md#ea-exo-ego-2026-0015))
- [`support`] HumanNet将视角多样性作为四大设计原则之一——第一视角和第三视角来源均被保留并显式索引，使模型能学习互补的执行者中心和观察者中心线索。数据管线在采集阶段就将第一视角和第三视角材料分流处理。 ([2605.06747](https://arxiv.org/abs/2605.06747) / [EA-EXO-EGO-2026-0016](evidence-appendix.md#ea-exo-ego-2026-0016))
- [`support`] 结合第一和第三视角支持运动感知表示学习：第三视角视频对全身运动、移动、姿态和多人动态特别有价值，第一视角对双手、接触和执行者中心意图特别有价值。两者结合支持对齐外观、语言和运动的表示，而非将视频视为独立帧序列。 ([2605.06747](https://arxiv.org/abs/2605.06747) / [EA-EXO-EGO-2026-0017](evidence-appendix.md#ea-exo-ego-2026-0017))
- [`conditional`] EgoX框架需要egocentric相机位姿作为输入,在野外场景中需手动确定相机外参,这限制了从exocentric视频全自动生成ego数据的能力 ([2512.08269](https://arxiv.org/abs/2512.08269) / [EA-EXO-EGO-2026-0005](evidence-appendix.md#ea-exo-ego-2026-0005))
- [`conditional`] 当评估相机视角更接近egocentric视角时(如EBench的高位相机),ego数据预训练的增益被放大:3:1比例在EBench上达到最佳(51.7%,较robot-only提升12.1%),表明视角匹配度影响预训练效果 ([2608.02580](https://arxiv.org/abs/2608.02580) / [EA-EXO-EGO-2026-0008](evidence-appendix.md#ea-exo-ego-2026-0008))
- [`conditional`] SiMDex重新挖掘预训练所用的同一egocentric语料库进行任务感知的后训练选择，使大规模ego采集'两次获益'（广度和精度）。然而该方法仅限于egocentric数据，未探索第三视角数据是否能增强挖掘的相似性信号。 ([2608.04196](https://arxiv.org/abs/2608.04196) / [EA-EXO-EGO-2026-0013](evidence-appendix.md#ea-exo-ego-2026-0013))
- [`limit`] 此前的exo-to-ego方法需要额外ego输入或多视角exo视频:EgoExo-Gen需要第一帧ego图像,Exo2Ego-V需要四个同步exocentric摄像机视角,限制了从第三视角视频采集ego数据的实用性 ([2512.08269](https://arxiv.org/abs/2512.08269) / [EA-EXO-EGO-2026-0004](evidence-appendix.md#ea-exo-ego-2026-0004))
- [`limit`] 视觉对齐依赖inpainting和深度感知合成,在严重遮挡或复杂光照下可能产生伪影;retargeting将手部姿态映射到平行夹爪会丢失精细手指关节信息,限制了ego数据转化为训练数据的质量 ([2608.02580](https://arxiv.org/abs/2608.02580) / [EA-EXO-EGO-2026-0010](evidence-appendix.md#ea-exo-ego-2026-0010))
- [`limit`] SiMDex的收益根本上取决于人类数据池的覆盖度——当池中缺乏与目标技能相似的高质量演示时，检索无信号可利用，甚至可能在机器人数据充足时注入方差。该限制暗示第三视角数据可能通过提供互补的运动模式来弥补ego数据池的覆盖盲区。 ([2608.04196](https://arxiv.org/abs/2608.04196) / [EA-EXO-EGO-2026-0014](evidence-appendix.md#ea-exo-ego-2026-0014))
- [`limit`] HumanNet承认开放世界人类视频存在视角不平衡（viewpoint imbalance）问题：大规模数据可能制造普遍性的幻觉，而实际上对特定地理区域、相机视角、体型、日常活动等存在显著偏倚。同时指出人类行为不等于机器人行为，存在本体差距。 ([2605.06747](https://arxiv.org/abs/2605.06747) / [EA-EXO-EGO-2026-0019](evidence-appendix.md#ea-exo-ego-2026-0019))
- [`gap`] SiMDex仅在Related Works中将Ego-Exo4D作为'rich foundation'提及，但实际人类数据池完全来自EgoDex（纯egocentric视频），未使用任何第三视角数据来辅助ego数据的选择或预训练。论文未探索第三视角视频能否增强egocentric数据挖掘的效果。 ([2608.04196](https://arxiv.org/abs/2608.04196) / [EA-EXO-EGO-2026-0011](evidence-appendix.md#ea-exo-ego-2026-0011))
- [`gap`] HumanNet的VLA后训练验证实验仅使用1000小时egocentric视频作为预训练源（对比100小时真实机器人数据和20000小时基线），未测试加入第三视角视频是否改善预训练效果。第三视角对ego预训练的增量贡献未被实验验证。 ([2605.06747](https://arxiv.org/abs/2605.06747) / [EA-EXO-EGO-2026-0018](evidence-appendix.md#ea-exo-ego-2026-0018))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` EgoX框架需要egocentric相机位姿作为输入,在野外场景中需手动确定相机外参,这限制了从exocentric视频全自动生成ego数据的能力 ([2512.08269](https://arxiv.org/abs/2512.08269) / [EA-EXO-EGO-2026-0005](evidence-appendix.md#ea-exo-ego-2026-0005))
- `conditional` 当评估相机视角更接近egocentric视角时(如EBench的高位相机),ego数据预训练的增益被放大:3:1比例在EBench上达到最佳(51.7%,较robot-only提升12.1%),表明视角匹配度影响预训练效果 ([2608.02580](https://arxiv.org/abs/2608.02580) / [EA-EXO-EGO-2026-0008](evidence-appendix.md#ea-exo-ego-2026-0008))
- `conditional` SiMDex重新挖掘预训练所用的同一egocentric语料库进行任务感知的后训练选择，使大规模ego采集'两次获益'（广度和精度）。然而该方法仅限于egocentric数据，未探索第三视角数据是否能增强挖掘的相似性信号。 ([2608.04196](https://arxiv.org/abs/2608.04196) / [EA-EXO-EGO-2026-0013](evidence-appendix.md#ea-exo-ego-2026-0013))
- `limit` 此前的exo-to-ego方法需要额外ego输入或多视角exo视频:EgoExo-Gen需要第一帧ego图像,Exo2Ego-V需要四个同步exocentric摄像机视角,限制了从第三视角视频采集ego数据的实用性 ([2512.08269](https://arxiv.org/abs/2512.08269) / [EA-EXO-EGO-2026-0004](evidence-appendix.md#ea-exo-ego-2026-0004))
- `limit` 视觉对齐依赖inpainting和深度感知合成,在严重遮挡或复杂光照下可能产生伪影;retargeting将手部姿态映射到平行夹爪会丢失精细手指关节信息,限制了ego数据转化为训练数据的质量 ([2608.02580](https://arxiv.org/abs/2608.02580) / [EA-EXO-EGO-2026-0010](evidence-appendix.md#ea-exo-ego-2026-0010))
- `limit` SiMDex的收益根本上取决于人类数据池的覆盖度——当池中缺乏与目标技能相似的高质量演示时，检索无信号可利用，甚至可能在机器人数据充足时注入方差。该限制暗示第三视角数据可能通过提供互补的运动模式来弥补ego数据池的覆盖盲区。 ([2608.04196](https://arxiv.org/abs/2608.04196) / [EA-EXO-EGO-2026-0014](evidence-appendix.md#ea-exo-ego-2026-0014))
- `limit` HumanNet承认开放世界人类视频存在视角不平衡（viewpoint imbalance）问题：大规模数据可能制造普遍性的幻觉，而实际上对特定地理区域、相机视角、体型、日常活动等存在显著偏倚。同时指出人类行为不等于机器人行为，存在本体差距。 ([2605.06747](https://arxiv.org/abs/2605.06747) / [EA-EXO-EGO-2026-0019](evidence-appendix.md#ea-exo-ego-2026-0019))
- `gap` SiMDex仅在Related Works中将Ego-Exo4D作为'rich foundation'提及，但实际人类数据池完全来自EgoDex（纯egocentric视频），未使用任何第三视角数据来辅助ego数据的选择或预训练。论文未探索第三视角视频能否增强egocentric数据挖掘的效果。 ([2608.04196](https://arxiv.org/abs/2608.04196) / [EA-EXO-EGO-2026-0011](evidence-appendix.md#ea-exo-ego-2026-0011))
- `gap` HumanNet的VLA后训练验证实验仅使用1000小时egocentric视频作为预训练源（对比100小时真实机器人数据和20000小时基线），未测试加入第三视角视频是否改善预训练效果。第三视角对ego预训练的增量贡献未被实验验证。 ([2605.06747](https://arxiv.org/abs/2605.06747) / [EA-EXO-EGO-2026-0018](evidence-appendix.md#ea-exo-ego-2026-0018))
- `conditional` 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。 ([2512.11612](https://arxiv.org/abs/2512.11612) / [EA-PRETRAIN-DATA-2026-0006](evidence-appendix.md#ea-pretrain-data-2026-0006))
- `conditional` UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only dat... ([2601.09988](https://arxiv.org/abs/2601.09988) / [EA-UMI-READ-0002](evidence-appendix.md#ea-umi-read-0002))
- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DQ-YEAR-READ-0003](evidence-appendix.md#ea-dq-year-read-0003))
- `conditional` 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0008](evidence-appendix.md#ea-ego-2026-0008))
- `conditional` UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data. ([2604.10647](https://arxiv.org/abs/2604.10647) / [EA-UMI-READ-0003](evidence-appendix.md#ea-umi-read-0003))
- `conditional` 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0017](evidence-appendix.md#ea-ego-2026-0017))
- `conditional` 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0018](evidence-appendix.md#ea-ego-2026-0018))
- `conditional` 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。 ([2606.17200](https://arxiv.org/abs/2606.17200) / [EA-PRETRAIN-DATA-2026-0001](evidence-appendix.md#ea-pretrain-data-2026-0001))
- `limit` Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。 ([2509.21986](https://arxiv.org/abs/2509.21986) / [EA-EGO-2026-0004](evidence-appendix.md#ea-ego-2026-0004))
- `limit` 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0005](evidence-appendix.md#ea-ego-2026-0005))
- `limit` 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。 ([2602.09013](https://arxiv.org/abs/2602.09013) / [EA-EGO-2026-0006](evidence-appendix.md#ea-ego-2026-0006))
- `limit` Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。 ([2602.16710](https://arxiv.org/abs/2602.16710) / [EA-EGO-2026-0009](evidence-appendix.md#ea-ego-2026-0009))
- `limit` Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [EA-UMI-READ-0004](evidence-appendix.md#ea-umi-read-0004))
- `limit` 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。 ([2605.20373](https://arxiv.org/abs/2605.20373) / [EA-EGO-2026-0012](evidence-appendix.md#ea-ego-2026-0012))
- `limit` HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。 ([2605.24934](https://arxiv.org/abs/2605.24934) / [EA-EGO-2026-0015](evidence-appendix.md#ea-ego-2026-0015))
- `limit` Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。 ([2606.06194](https://arxiv.org/abs/2606.06194) / [EA-EGO-2026-0016](evidence-appendix.md#ea-ego-2026-0016))
- `limit` Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。 ([2607.03828](https://arxiv.org/abs/2607.03828) / [EA-EGO-2026-0019](evidence-appendix.md#ea-ego-2026-0019))
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
