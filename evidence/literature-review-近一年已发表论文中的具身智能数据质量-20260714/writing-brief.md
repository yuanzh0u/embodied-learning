# Writing Brief: 近一年已发表论文中的具身智能数据质量

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年已发表论文中的具身智能数据质量
- Time range: 2025-07-14..2026-07-14
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-MODEL`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 36 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 37

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002)) ⟷ VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- `EA-DATA`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001)) ⟷ Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should ex... ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011))
- `EA-DATA`: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002)) ⟷ UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration... ([2603.17189](https://arxiv.org/abs/2603.17189) / [UMI-6M-002](evidence-appendix.md#umi-6m-002))
- `EA-DATA`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003)) ⟷ 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-2026-DQ-0003](evidence-appendix.md#ea-data-2026-dq-0003))
- `EA-DATA`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-DATA-2026-LY-0005](evidence-appendix.md#ea-data-2026-ly-0005)) ⟷ 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 ([2603.11634](https://arxiv.org/abs/2603.11634) / [EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004))
- `EA-DATA`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DATA-2026-LY-0007](evidence-appendix.md#ea-data-2026-ly-0007)) ⟷ 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))
- `EA-DATA`: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-LY-0009](evidence-appendix.md#ea-data-2026-ly-0009)) ⟷ 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- `EA-DATA`: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([2512.13100](https://arxiv.org/abs/2512.13100) / [EA-DATA-2026-LY-0011](evidence-appendix.md#ea-data-2026-ly-0011)) ⟷ VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([2602.10618](https://arxiv.org/abs/2602.10618) / [EA-DATA-2026-LY-0010](evidence-appendix.md#ea-data-2026-ly-0010))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (26 events)
- [`support`] 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([2509.01657](https://arxiv.org/abs/2509.01657) / [EA-DATA-2026-LY-0007](evidence-appendix.md#ea-data-2026-ly-0007))
- [`support`] 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([2512.13100](https://arxiv.org/abs/2512.13100) / [EA-DATA-2026-LY-0011](evidence-appendix.md#ea-data-2026-ly-0011))
- [`support`] A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-consistent long-horiz... ([2603.08546](https://arxiv.org/abs/2603.08546) / [EA-DATA-2026-WMDATA-0001](evidence-appendix.md#ea-data-2026-wmdata-0001))
- [`support`] 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001))
- [`support`] 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 ([2603.17189](https://arxiv.org/abs/2603.17189) / [EA-DATA-2026-LY-0009](evidence-appendix.md#ea-data-2026-ly-0009))
- [`support`] World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. ([2604.21741](https://arxiv.org/abs/2604.21741) / [EA-DATA-2026-WMDATA-0003](evidence-appendix.md#ea-data-2026-wmdata-0003))
- [`support`] 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003))
- [`support`] 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002))
- [`support`] A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under intervention, with modalities beyond RGB... ([2606.00113](https://arxiv.org/abs/2606.00113) / [EA-DATA-2026-WMDATA-0014](evidence-appendix.md#ea-data-2026-wmdata-0014))
- [`support`] Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations, broad egocentric human videos, and roll... ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-WMDATA-0002](evidence-appendix.md#ea-data-2026-wmdata-0002))
- [`support`] 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([2606.16208](https://arxiv.org/abs/2606.16208) / [EA-DATA-2026-LY-0005](evidence-appendix.md#ea-data-2026-ly-0005))
- [`support`] 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002))
- [`conditional`] UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only dat... ([2601.09988](https://arxiv.org/abs/2601.09988) / [UMI-6M-001](evidence-appendix.md#umi-6m-001))
- [`conditional`] Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation demonstrations, because off-the-shelf generative models can hallucinate robot bodi... ([2512.11797](https://arxiv.org/abs/2512.11797) / [EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005))
- [`conditional`] VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([2602.10618](https://arxiv.org/abs/2602.10618) / [EA-DATA-2026-LY-0010](evidence-appendix.md#ea-data-2026-ly-0010))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- [`conditional`] 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 ([2603.11634](https://arxiv.org/abs/2603.11634) / [EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004))
- [`conditional`] A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-DATA-2026-WMDATA-0006](evidence-appendix.md#ea-data-2026-wmdata-0006))
- [`conditional`] Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-2026-WMDATA-0004](evidence-appendix.md#ea-data-2026-wmdata-0004))
- [`conditional`] 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 ([2606.12365](https://arxiv.org/abs/2606.12365) / [EA-DATA-2026-LY-0012](evidence-appendix.md#ea-data-2026-ly-0012))
- [`conditional`] Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DATA-2026-WMDATA-0012](evidence-appendix.md#ea-data-2026-wmdata-0012))
- [`conditional`] 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))
- [`conditional`] 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-2026-DQ-0003](evidence-appendix.md#ea-data-2026-dq-0003))
- [`limit`] UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefulness. ([2603.17189](https://arxiv.org/abs/2603.17189) / [UMI-6M-002](evidence-appendix.md#umi-6m-002))
- [`limit`] Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011))
- [`limit`] VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))

### EA-EVAL (2 events)
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004))
- [`limit`] World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-EVAL-2026-WMDATA-0013](evidence-appendix.md#ea-eval-2026-wmdata-0013))

### EA-MODEL (4 events)
- [`support`] World-model training data needs geometry-consistency supervision, because photorealistic video without stable 4D correspondences can fail to yield executable robot actions. ([2605.22882](https://arxiv.org/abs/2605.22882) / [EA-MODEL-2026-WMDATA-0008](evidence-appendix.md#ea-model-2026-wmdata-0008))
- [`support`] Robot videos can be converted into richer world-model supervision by pairing RGB with depth and pseudo 3D scene-flow targets, training models to represent current 3D structure and short-horizon futur... ([2605.20752](https://arxiv.org/abs/2605.20752) / [EA-MODEL-2026-WMDATA-0009](evidence-appendix.md#ea-model-2026-wmdata-0009))
- [`support`] Training data for efficient embodied world-model rollouts must preserve sparse task-relevant events such as approach, contact, grasp, and release; generic frame dropping can remove the information do... ([2606.00664](https://arxiv.org/abs/2606.00664) / [EA-MODEL-2026-WMDATA-0007](evidence-appendix.md#ea-model-2026-wmdata-0007))
- [`limit`] World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to task-relevant interac... ([2606.12217](https://arxiv.org/abs/2606.12217) / [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010))

### EA-SENSOR (4 events)
- [`support`] 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 ([2607.05390](https://arxiv.org/abs/2607.05390) / [EA-SENSOR-2026-DQ-0005](evidence-appendix.md#ea-sensor-2026-dq-0005))
- [`conditional`] UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data. ([2604.10647](https://arxiv.org/abs/2604.10647) / [UMI-6M-003](evidence-appendix.md#umi-6m-003))
- [`limit`] Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [UMI-6M-004](evidence-appendix.md#umi-6m-004))
- [`limit`] 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))

### EA-XEMBODIMENT (1 events)
- [`support`] For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action space, avoiding retargeting and embodimen... ([2606.06033](https://arxiv.org/abs/2606.06033) / [UMI-6M-005](evidence-appendix.md#umi-6m-005))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only dat... ([2601.09988](https://arxiv.org/abs/2601.09988) / [UMI-6M-001](evidence-appendix.md#umi-6m-001))
- `conditional` Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation demonstrations, because off-the-shelf generative models can hallucinate robot bodi... ([2512.11797](https://arxiv.org/abs/2512.11797) / [EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005))
- `conditional` VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([2602.10618](https://arxiv.org/abs/2602.10618) / [EA-DATA-2026-LY-0010](evidence-appendix.md#ea-data-2026-ly-0010))
- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- `conditional` 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 ([2603.11634](https://arxiv.org/abs/2603.11634) / [EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004))
- `conditional` A scalable world-model data pipeline can use a small amount of real-world data to align classical simulation with neural simulation, generating action-video pairs that preserve real-world consistency... ([2604.11386](https://arxiv.org/abs/2604.11386) / [EA-DATA-2026-WMDATA-0006](evidence-appendix.md#ea-data-2026-wmdata-0006))
- `conditional` Synthetic world-model data for robot learning needs embodiment anchoring: rendered robot motion plus explicit scene and object priors can synthesize demonstrations in novel objects, scenes, and viewp... ([2606.02577](https://arxiv.org/abs/2606.02577) / [EA-DATA-2026-WMDATA-0004](evidence-appendix.md#ea-data-2026-wmdata-0004))
- `conditional` 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 ([2606.12365](https://arxiv.org/abs/2606.12365) / [EA-DATA-2026-LY-0012](evidence-appendix.md#ea-data-2026-ly-0012))
- `conditional` Paired task-execution videos are useful but costly; self-distillation can partially replace curated task-video supervision by using unlabeled scene images, VLM-generated tasks and solutions, and VLM... ([2606.12072](https://arxiv.org/abs/2606.12072) / [EA-DATA-2026-WMDATA-0012](evidence-appendix.md#ea-data-2026-wmdata-0012))
- `conditional` 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))
- `conditional` 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DATA-2026-DQ-0003](evidence-appendix.md#ea-data-2026-dq-0003))
- `limit` UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefulness. ([2603.17189](https://arxiv.org/abs/2603.17189) / [UMI-6M-002](evidence-appendix.md#umi-6m-002))
- `limit` Static image-text pretraining is insufficient training signal for contact-rich manipulation; world-model data should expose action-conditioned scene evolution and contact dynamics. ([2606.12403](https://arxiv.org/abs/2606.12403) / [EA-DATA-2026-WMDATA-0011](evidence-appendix.md#ea-data-2026-wmdata-0011))
- `limit` VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- `limit` World-model training and post-training objectives should be tied to downstream action quality rather than intermediate video fidelity, because later denoising can become less action-relevant or physi... ([2605.27947](https://arxiv.org/abs/2605.27947) / [EA-EVAL-2026-WMDATA-0013](evidence-appendix.md#ea-eval-2026-wmdata-0013))
- `limit` World-action training cannot optimize only visual reconstruction: hidden states that make plausible futures may still be poorly organized for low-level control unless aligned to task-relevant interac... ([2606.12217](https://arxiv.org/abs/2606.12217) / [EA-MODEL-2026-WMDATA-0010](evidence-appendix.md#ea-model-2026-wmdata-0010))
- `conditional` UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data. ([2604.10647](https://arxiv.org/abs/2604.10647) / [UMI-6M-003](evidence-appendix.md#umi-6m-003))
- `limit` Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and exp... ([2604.14089](https://arxiv.org/abs/2604.14089) / [UMI-6M-004](evidence-appendix.md#umi-6m-004))
- `limit` 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))

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
