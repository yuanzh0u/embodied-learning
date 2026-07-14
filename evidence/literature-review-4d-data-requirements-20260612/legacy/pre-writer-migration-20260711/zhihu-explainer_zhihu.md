# 4D 时空推理对数据的需求：专家解释帖

## TL;DR

4D 时空推理对数据的需求 不能只看一个漂亮结论，要先看论文级证据、适用条件和失败模式。

## 检索范围

- Time range: 2025-12-12..2026-06-12
- Paper-level sources: 10 / 5
- Output type: expert-explainer

## 常见误区或争议

- 把候选论文、项目页或社交讨论当成正文级证据，会高估结论强度。
- 把 `conditional`、`limit`、`gap` 写成共识，会让综述失真。

## 证据与限制

### 共识/正向证据
- [EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001): 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。
- [EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005): 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。
- [EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008): 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。
- [EA-DATA-2026-4DDATA-0009](evidence-appendix.md#ea-data-2026-4ddata-0009): 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。
- [EA-DATA-2026-4DDATA-0017](evidence-appendix.md#ea-data-2026-4ddata-0017): 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。
- [EA-EVAL-2026-4DDATA-0011](evidence-appendix.md#ea-eval-2026-4ddata-0011): 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。
- [EA-MODEL-2026-4DDATA-0003](evidence-appendix.md#ea-model-2026-4ddata-0003): 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。
- [EA-SENSOR-2026-4DDATA-0015](evidence-appendix.md#ea-sensor-2026-4ddata-0015): 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。
### 条件成立
- [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004): 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。
- [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002): 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。
- [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006): 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。
- [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010): 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。
- [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018): 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。
- [EA-DATA-2026-4DDATA-0016](evidence-appendix.md#ea-data-2026-4ddata-0016): 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。
- [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014): 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。
### 限制与失败模式
- [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019): 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。
- [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007): 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。
### 开放问题
- [EA-DATA-2026-4DDATA-0020](evidence-appendix.md#ea-data-2026-4ddata-0020): 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。
- [EA-SENSOR-2026-4DDATA-0012](evidence-appendix.md#ea-sensor-2026-4ddata-0012): 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| [EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001) | EA-DATA | `support` | `direct` | 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 | 3PoinTr先从无动作人类视频学习非 embodiment 点的密集3D点轨迹，再用20条机器人动作示教训练闭环策略；论文报告真实任务平均成功率相对最强基线提高25.0个百分点。 (Abstract; 1 Introduction; 4.1 Data collection; 4.4 Results) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | [2603.08485](https://arxiv.org/abs/2603.08485) |
| [EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005) | EA-DATA | `support` | `direct` | 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 | Kinema4D用URDF/重建机器人经正逆运动学产生4D robot pointmap控制信号，再训练模型生成同步RGB和pointmap未来；其Robo4D-200k包含201,426个带高质量4D标注的交互episode。 (Abstract; 1 Introduction; 3.1 Kinematics Control; 3.2 4D Generative Modeling; 3.3 Robo4D-200k) | mutian-xu; tianbao-zhang; tianqi-liu | [2603.16669](https://arxiv.org/abs/2603.16669) |
| [EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008) | EA-DATA | `support` | `direct` | 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 | GEM-4D冻结几何基础模型，提取稠密几何表示作为correspondence teacher，并通过geometry flow把监督蒸馏进视频backbone；训练后几何分支丢弃，推理仍是单流视频生成。 (2.2 Feed-Forward 3D and 4D Geometry Models; 3.2.3 Correspondence Distillation via Geometry Flow; 5 Conclusion) | kaichen-zhou; yuzhen-chen; fangneng-zhan | [2605.22882](https://arxiv.org/abs/2605.22882) |
| [EA-DATA-2026-4DDATA-0009](evidence-appendix.md#ea-data-2026-4ddata-0009) | EA-DATA | `support` | `direct` | 可部署的4D世界-动作模型需要异构数据混合，而不是单一robot demo：真实机器人远程操作、UMI式交互、第一视角人类视频、rollout/失败轨迹分别提供不同监督。 | τ0-WM构建27.3K小时语料：17.8K小时真实机器人远程操作、6.5K小时UMI式示教、3.0K小时开源第一视角人类交互视频，并用rollout或失败轨迹训练任务进度/低质量结果评估。 (Abstract; III Data Sources for Predictive Robot Learning; A Training Configuration) | pengfei-zhou; shengcong-chen; di-chen | [2606.01027](https://arxiv.org/abs/2606.01027) |
| [EA-DATA-2026-4DDATA-0017](evidence-appendix.md#ea-data-2026-4ddata-0017) | EA-DATA | `support` | `direct` | 接触导向的4D数据集应同步记录语言目标、第三视角/腕部视觉、双指触觉、机器人状态和动作轨迹，并把触觉反馈接入示教过程。 | HapTile提供1,726条示教、38个任务、9类技能，15Hz同步语言、视觉、触觉、机器人状态和动作；其teleoperation平台还将触觉marker motion转成操作者侧haptic feedback。 (Abstract; 3.1 Dataset Statistics; 4 Data Collection Platform; 4.3 Haptic Feedback to the Operator) | amirhosein-alian; yongqiang-zhao; shiyi-gu | [2606.04825](https://arxiv.org/abs/2606.04825) |
| [EA-DATA-2026-4DDATA-0004](evidence-appendix.md#ea-data-2026-4ddata-0004) | EA-DATA | `conditional` | `direct` | 4D监督数据需要时间密集、度量空间对齐且有足够点密度；过少点、只给2D轨迹、目标点集或静态/稠密深度都不等价。 | Pri4R比较多种监督目标，认为3D点轨迹兼具时间密集、几何度量和空间稀疏；附录中1024个点优于256/512点，且没有当前点云输入会退化，因为模型必须凭空生成而非预测给定场景演化。 (IV-B Why 3D Point Tracks as Privileged Supervision; S.III-A Additional Analysis on input; S.III-C Additional Ablations) | jisoo-kim; jungbin-cho; sanghyeok-chu | [2603.01549](https://arxiv.org/abs/2603.01549) |
| [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002) | EA-DATA | `conditional` | `direct` | 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 | 论文用可见性mask保留部分遮挡轨迹并逐点逐时刻mask损失，认为这比丢弃含不可见点的轨迹能提供更多任务关键监督；附录说明真实视频需2D跟踪、深度提升到3D、SAM3分割人手并移除embodiment点。 (4.3 Results: 3D Point Track Prediction; Appendix D Data Collection Details; Appendix G Future Work) | adam-hung; bardienus-pieter-duisterhof; jeffrey-ichnowski | [2603.08485](https://arxiv.org/abs/2603.08485) |
| [EA-DATA-2026-4DDATA-0006](evidence-appendix.md#ea-data-2026-4ddata-0006) | EA-DATA | `conditional` | `direct` | 4D数据生产可以接受伪标注噪声，但要明确目标是学习相对空间约束和运动先验；同时应合成失败轨迹，让模型区分成功和近失误。 | Kinema4D补充材料说明ST-v2生成的4D伪标注未必达到绝对亚毫米真值，但足以学习相对几何；LIBERO数据生成中还从成功轨迹注入不同强度动作噪声，合成九种失败轨迹。 (Supplementary G.2 Dataset; Acquisition of LIBERO simulated data; The underlying logic behind 4D pseudo annotation) | mutian-xu; tianbao-zhang; tianqi-liu | [2603.16669](https://arxiv.org/abs/2603.16669) |
| [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010) | EA-DATA | `conditional` | `direct` | 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 | 论文把真实robot data、UMI-style data和egocentric videos划分为不同监督等级，并用modality-specific supervision masks让每条样本只参与其实际拥有的视觉、状态、动作和进度损失。 (I Introduction; III Data Sources for Predictive Robot Learning; Unified supervision; IV-C Join... | pengfei-zhou; shengcong-chen; di-chen | [2606.01027](https://arxiv.org/abs/2606.01027) |
| [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018) | EA-DATA | `conditional` | `direct` | 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 | HapTile说明所有模态通过机器人控制循环同步，检查空/损坏轨迹和timestamp gaps，验证action-state consistency；附录还要求episode-level split避免temporal leakage，并保留raw/rectified tactile images。 (3.2 Synchronization and Data Quality Control; A.1 Data Formatting;... | amirhosein-alian; yongqiang-zhao; shiyi-gu | [2606.04825](https://arxiv.org/abs/2606.04825) |
| [EA-DATA-2026-4DDATA-0016](evidence-appendix.md#ea-data-2026-4ddata-0016) | EA-DATA | `conditional` | `direct` | 触觉4D数据不仅要记录，还要有事件强度或等价的时序结构，帮助模型区分静默期与接触活跃期。 | Dream-Tac的contact gate直接从左右指尖触觉RGB的帧间平均绝对差得到，经过鲁棒归一化后在接触变化时提高触觉token注意力；附录统计显示大多数变化很小，较大变化对应关键交互事件。 (3.3 Contact-Aware Self Attention; A.6 Contact Gate Statistics) | yunfan-lou; yifan-ye; yankai-fu | [2606.08737](https://arxiv.org/abs/2606.08737) |
| [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014) | EA-DATA | `conditional` | `direct` | 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 | TacForeSight在perturbation-aware设置中额外收集恢复示教，让外部扰动发生在执行中并要求示教者重新建立稳定接触；完整模型在三个扰动任务上报告90%、85%、85%平均完成/成功分数。 (IV-B 2 Perturbation-Aware Evaluation; IV-C Main Results; Table I) | yujie-zang; yuhang-zheng; xian-nie | [2606.11184](https://arxiv.org/abs/2606.11184) |
| [EA-DATA-2026-4DDATA-0019](evidence-appendix.md#ea-data-2026-4ddata-0019) | EA-DATA | `limit` | `direct` | 示教数据质量受采集硬件的人体工学和接触力分布强烈影响；“更多UMI/手持夹爪示教”不自动等于更好的4D交互数据。 | 该研究在医用绷带打开任务中比较不同UMI夹爪条件和裸手，发现集中载荷夹爪优于分布载荷夹爪，但仍明显慢于手；作者强调力分布、刚度和人体工学会影响示教质量和工作负荷。 (Abstract; II-A Performance and Usability Limitations; V Discussion; VI Conclusion) | gina-l-georgadarellis; natalija-beslic; seonhun-lee | [2603.17189](https://arxiv.org/abs/2603.17189) |
| [EA-DATA-2026-4DDATA-0020](evidence-appendix.md#ea-data-2026-4ddata-0020) | EA-DATA | `gap` | `direct` | 面向4D时空推理的数据采集应把采集设备本身当成被优化对象：如果夹爪无法表达任务所需的接触和力，算法很难从示教中补回来。 | 作者指出UMI完整学习流程通常至少需要200条固定环境任务示教，手持夹爪仍可能比裸手慢；研究中的夹爪未集成完整传感/marker pipeline，后续需把传感和跟踪能力纳入完整示教到机器人流程评估。 (II-A Performance and Usability Limitations; V Discussion; VI Conclusion) | gina-l-georgadarellis; natalija-beslic; seonhun-lee | [2603.17189](https://arxiv.org/abs/2603.17189) |
| [EA-EVAL-2026-4DDATA-0011](evidence-appendix.md#ea-eval-2026-4ddata-0011) | EA-EVAL | `support` | `direct` | 用于评估、改进和规划的4D世界模型需要多视角视觉、机器人本体状态、动作chunk、历史/记忆状态，以及可在latent中评估的奖励/价值监督。 | WEAVER在DROID上预训练并在真实任务数据上微调，输入右侧外部相机和腕部相机、proprioceptive state、action plan、memory/history latents，并蒸馏奖励/critic头来快速评分候选动作。 (3 WEAVER; 3.1 Key Design Decisions; 3.3 Accurate and Efficient Value Estimation; 4 Experimental... | arnav-kumar-jain; yilin-wu; jesse-farebrother | [2606.13672](https://arxiv.org/abs/2606.13672) |
| [EA-MODEL-2026-4DDATA-0003](evidence-appendix.md#ea-model-2026-4ddata-0003) | EA-MODEL | `support` | `direct` | 动作标签本身不足以教会VLA“动作之后世界会怎样变”；4D时空推理需要与动作时域对齐的3D点轨迹作为训练期特权监督。 | Pri4R指出动作标签主要鼓励模仿示教动作，但不给出世界动态；它给VLA添加点轨迹头，监督未来3D位移，训练后丢弃辅助头而不增加推理输入和计算。 (I Introduction; IV Pri4R: Learning World Dynamics via Privileged 4D Representations; IV-C Construction of 3D Point Track Supervision) | jisoo-kim; jungbin-cho; sanghyeok-chu | [2603.01549](https://arxiv.org/abs/2603.01549) |
| [EA-MODEL-2026-4DDATA-0007](evidence-appendix.md#ea-model-2026-4ddata-0007) | EA-MODEL | `limit` | `direct` | 只用视频重建损失训练世界模型会让4D推理停留在“看起来像”，但机器人需要的是跨帧同一3D表面点的一致对应。 | GEM-4D指出像素或latent重建损失不能保证对应一致，可能出现接触漂移、深度不一致和非刚性变形；这些视觉上微妙的错误会破坏从视频rollout提取动作。 (Abstract; 1 Introduction; 3.1 Problem Formulation; 3.2.1 What Governs Inter-Frame Correspondence) | kaichen-zhou; yuzhen-chen; fangneng-zhan | [2605.22882](https://arxiv.org/abs/2605.22882) |
| [EA-SENSOR-2026-4DDATA-0015](evidence-appendix.md#ea-sensor-2026-4ddata-0015) | EA-SENSOR | `support` | `direct` | 对接触任务，世界-动作模型的数据目标应联合包含未来视觉、未来触觉和动作；只预测未来图像会丢掉触发式、稀疏且短暂的接触事件。 | Dream-Tac把当前视觉/触觉/语言作为条件，联合去噪未来视觉、未来触觉和动作chunk；其contact-aware self-attention用相邻触觉帧变化计算事件门控，强调接触发生、滑移或释放等时刻。 (Abstract; 3.1 Problem Formulation; 3.2 Dream-Tac Architecture; 3.3 Contact-Aware Self Attention) | yunfan-lou; yifan-ye; yankai-fu | [2606.08737](https://arxiv.org/abs/2606.08737) |
| [EA-SENSOR-2026-4DDATA-0013](evidence-appendix.md#ea-sensor-2026-4ddata-0013) | EA-SENSOR | `support` | `direct` | 接触丰富任务的4D推理需要把高频腕部力/力矩和双指触觉场作为时间序列数据，而不只是把触觉当作当前帧的被动反馈。 | TacForeSight训练force-conditioned tactile world model，用高频wrist force/torque条件预测短时未来触觉latent；作者报告wrist wrench条件在MSE、cosine similarity和KL上优于无条件、RGB和机器人状态条件。 (Abstract; III-A Force-conditioned Tactile World Model; IV-D 1 Wor... | yujie-zang; yuhang-zheng; xian-nie | [2606.11184](https://arxiv.org/abs/2606.11184) |
| [EA-SENSOR-2026-4DDATA-0012](evidence-appendix.md#ea-sensor-2026-4ddata-0012) | EA-SENSOR | `gap` | `direct` | 纯视觉4D世界模型在接触、抓取稳定性、力、被遮挡几何、形变和颗粒动态上状态不可观；数据扩展应补触觉、力矩、深度、更多embodiment和失败/奖励监督。 | WEAVER限制部分指出视觉只给部分物理状态，任务相关的接触、力和遮挡几何可能不可见；形变/动态物体、有限规划时域、DROID embodiment覆盖、以及reward labels噪声都是剩余瓶颈。 (A5 Limitations; A5.1 Partial Observability; A5.2 Complex Deformable and Dynamic Interactions; A5.4 Data Coverage and... | arnav-kumar-jain; yilin-wu; jesse-farebrother | [2606.13672](https://arxiv.org/abs/2606.13672) |

## 延伸阅读与可信度

- Evidence sufficiency: formal-ready
- Paper-level sources: 10 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## References

- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
