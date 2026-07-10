# Evidence Appendix: 近一年已发表论文中的具身智能数据质量

- Time range: 2025-07-08..2026-07-08
- Events: 12
- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。

### EA-DATA-2026-LY-0007

- Claim: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.01657](https://arxiv.org/abs/2509.01657) Data Retrieval with Importance Weights for Few-Shot Imitation Learning
- Locator: Abstract; 1 Introduction; 2 Related Work
- Evidence: IWR 将 retrieval-based imitation learning 的常用最近邻规则解释为目标数据分布 KDE 的极限，指出其高方差、易受噪声影响且不考虑 prior data distribution；方法用目标/先验分布概率比进行 importance-weighted retrieval，并在仿真和 Bridge 真实评估中改善现有检索方法。
- Quote: “susceptible to noise”
- Authors: amber-xie; rahul-chand; dorsa-sadigh; et al.

### EA-DATA-2026-LY-0011

- Claim: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.13100](https://arxiv.org/abs/2512.13100) OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning
- Locator: Abstract; 1 Introduction; 6 OXE-AugE: A Large Open-Source Robot Augmentation Dataset; Appendix A.2
- Evidence: 论文指出 OXE 聚合 60 多个机器人数据集，但 top four robot types 占超过 85% 真实数据，带来过拟合风险；OXE-AugE 用 9 种不同机器人本体扩增 16 个 OXE 子集，形成 4.4M trajectories，并研究扩增对 cross-embodiment learning 的影响。
- Quote: “top four robot types account”
- Authors: guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al.

### EA-DATA-2026-LY-0001

- Claim: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09056](https://arxiv.org/abs/2603.09056) Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning
- Locator: I INTRODUCTION; II-B Robot data curation; VI CONCLUSIONS
- Evidence: 论文指出人类遥操作会带来错误、操作约束、技能差异、噪声和次优行为；QoQ 用 influence functions 衡量训练 state-action 对验证示范的贡献，并在轨迹层聚合以降低噪声、保持覆盖，在仿真、真实机器人和 DROID in-the-wild 数据上改善策略成功率。
- Quote: “direct contribution to policy performance”
- Authors: haeone-lee; taywon-min; junsu-kim; et al.

### EA-DATA-2026-LY-0009

- Claim: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: II-A Performance and Usability Limitations; V DISCUSSION
- Evidence: 论文指出 UMI 示教虽快于遥操作但仍比手工慢、工具重量会造成疲劳并影响 demonstration；实验中改变 UMI gripper fingers 的力分布显著影响打开绷带包装表现，concentrated load grippers 优于 distributed load grippers，作者将其连接到 demonstration quality 和 learned robot control policies。
- Quote: “subtle hardware changes”
- Authors: gina-l-georgadarellis; natalija-beslic; seonhun-lee; et al.

### EA-DATA-2026-LY-0003

- Claim: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.01544](https://arxiv.org/abs/2605.01544) An Efficient Metric for Data Quality Measurement in Imitation Learning
- Locator: Abstract; I INTRODUCTION; V Experiments
- Evidence: 论文把 poor-quality end-user demonstrations 具体化为 excessive corrective motions、oscillations 和 abrupt adjustments，并提出基于 demonstration trajectories PSD 的自动排序指标；实验比较未筛选、oracle、现有排序和 jerk/path-length 等 baseline，研究 PSD 筛选对下游 IL 成功率和平滑性的影响。
- Quote: “excessive corrective motions, oscillations”
- Authors: noushad-sojib; momotaz-begum

### EA-DATA-2026-LY-0002

- Claim: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: I INTRODUCTION; Abstract; V-D Pilot Study Design; VI-B Pilot Study Results
- Evidence: DQAF 框架从 sub-task progress、motion smoothness、stalls、kinematic limits 抽取质量信号，生成结构化质量评估和自然语言纠正建议；pilot study 中即时反馈条件呈现更高任务完成度、更高 episode-level quality scores 和更少 detected suboptimalities 的趋势。
- Quote: “not only on task completion”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

### EA-DATA-2026-LY-0005

- Claim: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation
- Locator: 1 Introduction; 2 Related Work; Appendix C.4 Retention Balance, Single-Task Curation, and Real-Robot Failure Modes
- Evidence: ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。
- Quote: “not only on data scale”
- Authors: tao-xu; jiaxin-wang; runhao-zhang; et al.

### EA-DATA-2026-LY-0010

- Claim: VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.10618](https://arxiv.org/abs/2602.10618) From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks
- Locator: 1 Introduction; 2 Related Work; Abstract
- Evidence: 论文指出 VR 用于记录机器人学习示教时，visual fidelity 可能不如 user behavior 的 quality/reliability 重要；输入设备与可视化会影响工作负荷、运动效率、不必要动作和执行精度。实验发现 controller 与 motion-capture gloves 在 pick-and-place 与 manner-oriented tasks 上呈现不同轨迹策略和权衡。
- Quote: “quality and reliability of user behavior”
- Authors: robin-beierling; manuel-scheibl; jonas-dech; et al.

### EA-DATA-2026-LY-0008

- Claim: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: 1 Introduction; 3.3 Trajectory and Grasp Filtering via Simulation; Abstract
- Evidence: PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。
- Quote: “harmful to train the robot”
- Authors: albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al.

### EA-DATA-2026-LY-0004

- Claim: 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.11634](https://arxiv.org/abs/2603.11634) Diversity You Can Actually Measure: A Fast, Model-Free Diversity Metric for Robotics Datasets
- Locator: I Introduction; Abstract; IX Conclusion and Limitations
- Evidence: FAKTUAL 用 signature-kernel entropy 直接在 demonstration dataset 上度量多样性并选择高熵子集；作者在结论中明确说明该方法不像其他 data curation 策略那样保证只选高质量轨迹，若数据集中存在有害轨迹，最 diverse 子集可能反而有损。
- Quote: “does not guarantee the selection”
- Authors: sreevardhan-sirigiri; nathan-samuel-de-lara; christopher-agia; et al.

### EA-DATA-2026-LY-0012

- Claim: 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.12365](https://arxiv.org/abs/2606.12365) Ambient Diffusion Policy: Imitation Learning from Suboptimal Data in Robotics
- Locator: 1 Introduction; 2 Related Work; 10 Conclusion; Abstract
- Evidence: Ambient Diffusion Policy 指出高质量任务专用机器人数据昂贵，而 failures、不同质量轨迹、仿真、跨本体和 egocentric video 等 suboptimal/OOD sources 很丰富；作者认为过滤会浪费数据，常规 co-training 又会学习 harmful parts，因此提出 noise-dependent data usage，只在特定 diffusion times 让 suboptimal samples 贡献训练。
- Quote: “suboptimal data will continue to grow”
- Authors: adam-wei; nicholas-pfaff; thomas-cohn; et al.

### EA-DATA-2026-LY-0006

- Claim: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation
- Locator: 1 Introduction; Abstract; 2 Related Work
- Evidence: 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action chunks。
- Quote: “valuable recovery behaviors”
- Authors: justin-yu; andrew-goldberg; kavish-kondap; et al.

## References

- `2509.01657` [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657) (2025-09-01)
- `2512.13100` [OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning](https://arxiv.org/abs/2512.13100) (2025-12-15)
- `2602.10618` [From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks](https://arxiv.org/abs/2602.10618) (2026-02-11)
- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2603.09056` [Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056) (2026-03-10)
- `2603.11634` [Diversity You Can Actually Measure: A Fast, Model-Free Diversity Metric for Robotics Datasets](https://arxiv.org/abs/2603.11634) (2026-03-12)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17)
- `2605.01544` [An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544) (2026-05-02)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.12365` [Ambient Diffusion Policy: Imitation Learning from Suboptimal Data in Robotics](https://arxiv.org/abs/2606.12365) (2026-06-10)
- `2606.16208` [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208) (2026-06-15)
- `2606.28320` [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320) (2026-06-26)
