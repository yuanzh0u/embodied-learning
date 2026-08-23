# Evidence Appendix: 第三视角视频数据对ego数据采集和预训练的帮助

- Time range: 2025-08-12..2026-08-12
- Events: 48
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-EXO-EGO-2026-0001

- Claim: 第三人称(exocentric)视频可转化为第一人称(egocentric)视角,为机器人和AR/VR领域的模仿、推理和交互提供关键的第一人称感知能力
- Stance: `support` | Confidence: `direct`
- Paper: [2512.08269](https://arxiv.org/abs/2512.08269) EgoX: Egocentric Video Generation from a Single Exocentric Video
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0002

- Claim: exocentric视频的latent特征为egocentric视频生成提供更广泛的场景上下文,弥补ego先验渲染中缺失的场景信息
- Stance: `support` | Confidence: `direct`
- Paper: [2512.08269](https://arxiv.org/abs/2512.08269) EgoX: Egocentric Video Generation from a Single Exocentric Video
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0003

- Claim: 利用预训练大规模视频扩散模型的时空知识,通过轻量LoRA适配即可从单个exocentric视频生成高质量egocentric视频,并对未见场景具有强泛化能力
- Stance: `support` | Confidence: `direct`
- Paper: [2512.08269](https://arxiv.org/abs/2512.08269) EgoX: Egocentric Video Generation from a Single Exocentric Video
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0006

- Claim: egocentric人类视频提供可大规模采集的替代数据源,相比机器人遥操作可在多样化物体、环境和任务变体中大规模收集手部交互数据
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02580](https://arxiv.org/abs/2608.02580) Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0007

- Claim: 在ego2robot合成数据与机器人数据上联合预训练,持续提升OOD泛化性能,增益在视觉外观、具身形态和语义扰动下最为显著,表明ego数据主要提升不变性和跨分布鲁棒性
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02580](https://arxiv.org/abs/2608.02580) Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0009

- Claim: 在15种形态的Ego2R数据基础上加入原始ego视频数据,性能从33.5%跃升至37.3%,原始ego数据有效充当第16种'形态',通过略微不同的视觉外观和动作分布进一步丰富预训练多样性
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02580](https://arxiv.org/abs/2608.02580) Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0012

- Claim: Egocentric视频预训练为VLA提供跨本体知识（cross-embodiment knowledge），完全丢弃人类数据会浪费预训练获得的跨本体知识和对真实世界部署的泛化能力。这间接支持了人类视频数据（包括潜在的第三视角数据）对ego预训练的价值。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.04196](https://arxiv.org/abs/2608.04196) SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0015

- Claim: 第三视角视频与第一视角视频互补：第一视角保留动作执行视角，暴露接触动力学、手-物体关系、时间意图和运动决策的视觉后果；第三视角补充全身运动、姿态、交互上下文、周围智能体和场景级动态，使这些信息更易观察。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.06747](https://arxiv.org/abs/2605.06747) HumanNet: Human-centric Video Dataset for Robot Learning
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0016

- Claim: HumanNet将视角多样性作为四大设计原则之一——第一视角和第三视角来源均被保留并显式索引，使模型能学习互补的执行者中心和观察者中心线索。数据管线在采集阶段就将第一视角和第三视角材料分流处理。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.06747](https://arxiv.org/abs/2605.06747) HumanNet: Human-centric Video Dataset for Robot Learning
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0017

- Claim: 结合第一和第三视角支持运动感知表示学习：第三视角视频对全身运动、移动、姿态和多人动态特别有价值，第一视角对双手、接触和执行者中心意图特别有价值。两者结合支持对齐外观、语言和运动的表示，而非将视频视为独立帧序列。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.06747](https://arxiv.org/abs/2605.06747) HumanNet: Human-centric Video Dataset for Robot Learning
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0005

- Claim: EgoX框架需要egocentric相机位姿作为输入,在野外场景中需手动确定相机外参,这限制了从exocentric视频全自动生成ego数据的能力
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.08269](https://arxiv.org/abs/2512.08269) EgoX: Egocentric Video Generation from a Single Exocentric Video
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0008

- Claim: 当评估相机视角更接近egocentric视角时(如EBench的高位相机),ego数据预训练的增益被放大:3:1比例在EBench上达到最佳(51.7%,较robot-only提升12.1%),表明视角匹配度影响预训练效果
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.02580](https://arxiv.org/abs/2608.02580) Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0013

- Claim: SiMDex重新挖掘预训练所用的同一egocentric语料库进行任务感知的后训练选择，使大规模ego采集'两次获益'（广度和精度）。然而该方法仅限于egocentric数据，未探索第三视角数据是否能增强挖掘的相似性信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.04196](https://arxiv.org/abs/2608.04196) SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0004

- Claim: 此前的exo-to-ego方法需要额外ego输入或多视角exo视频:EgoExo-Gen需要第一帧ego图像,Exo2Ego-V需要四个同步exocentric摄像机视角,限制了从第三视角视频采集ego数据的实用性
- Stance: `limit` | Confidence: `direct`
- Paper: [2512.08269](https://arxiv.org/abs/2512.08269) EgoX: Egocentric Video Generation from a Single Exocentric Video
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0010

- Claim: 视觉对齐依赖inpainting和深度感知合成,在严重遮挡或复杂光照下可能产生伪影;retargeting将手部姿态映射到平行夹爪会丢失精细手指关节信息,限制了ego数据转化为训练数据的质量
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.02580](https://arxiv.org/abs/2608.02580) Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0014

- Claim: SiMDex的收益根本上取决于人类数据池的覆盖度——当池中缺乏与目标技能相似的高质量演示时，检索无信号可利用，甚至可能在机器人数据充足时注入方差。该限制暗示第三视角数据可能通过提供互补的运动模式来弥补ego数据池的覆盖盲区。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.04196](https://arxiv.org/abs/2608.04196) SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0019

- Claim: HumanNet承认开放世界人类视频存在视角不平衡（viewpoint imbalance）问题：大规模数据可能制造普遍性的幻觉，而实际上对特定地理区域、相机视角、体型、日常活动等存在显著偏倚。同时指出人类行为不等于机器人行为，存在本体差距。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.06747](https://arxiv.org/abs/2605.06747) HumanNet: Human-centric Video Dataset for Robot Learning
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0011

- Claim: SiMDex仅在Related Works中将Ego-Exo4D作为'rich foundation'提及，但实际人类数据池完全来自EgoDex（纯egocentric视频），未使用任何第三视角数据来辅助ego数据的选择或预训练。论文未探索第三视角视频能否增强egocentric数据挖掘的效果。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.04196](https://arxiv.org/abs/2608.04196) SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-EXO-EGO-2026-0018

- Claim: HumanNet的VLA后训练验证实验仅使用1000小时egocentric视频作为预训练源（对比100小时真实机器人数据和20000小时基线），未测试加入第三视角视频是否改善预训练效果。第三视角对ego预训练的增量贡献未被实验验证。
- Stance: `gap` | Confidence: `direct`
- Paper: [2605.06747](https://arxiv.org/abs/2605.06747) HumanNet: Human-centric Video Dataset for Robot Learning
- Locator: not recorded
- Evidence: 
- Authors: unlisted

### EA-DQ-YEAR-READ-0008

- Claim: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.01657](https://arxiv.org/abs/2509.01657) Data Retrieval with Importance Weights for Few-Shot Imitation Learning
- Locator: Abstract (full-text section)
- Evidence: IWR 将 retrieval-based imitation learning 的常用最近邻规则解释为目标数据分布 KDE 的极限，指出其高方差、易受噪声影响且不考虑 prior data distribution；方法用目标/先验分布概率比进行 importance-weighted retrieval，并在仿真和 Bridge 真实评估中改善现有检索方法。
- Quote: “Abstract While large-scale robot datasets have propelled recent progress in imitation learning, learning from smaller task specific datasets remains critical for deployment in new environments and unseen tasks. One such approach to few-shot imitation learning is retrieval-based imitation learning, which extracts relevant samples from large, widely available prior datasets to augment a limited demonstration dataset. To determine the relevant data from prior datasets, retrieval-based approaches mo”
- Authors: amber-xie; rahul-chand; dorsa-sadigh; et al.

### EA-DQ-YEAR-READ-0009

- Claim: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.13100](https://arxiv.org/abs/2512.13100) OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning
- Locator: Abstract (full-text section)
- Evidence: 论文指出 OXE 聚合 60 多个机器人数据集，但 top four robot types 占超过 85% 真实数据，带来过拟合风险；OXE-AugE 用 9 种不同机器人本体扩增 16 个 OXE 子集，形成 4.4M trajectories，并研究扩增对 cross-embodiment learning 的影响。
- Quote: “Abstract Large and diverse datasets are needed for training generalist robot policies that have potential to control a variety of robot embodiments—robot arm and gripper combinations—across diverse tasks and environments. As re-collecting demonstrations and retraining for each new hardware platform are prohibitively costly, we show that existing robot data can be augmented for transfer and generalization. The Open X-Embodiment (OXE) dataset, which aggregates demonstrations from over 60 robot dat”
- Authors: guanhua-ji; harsha-polavaram; lawrence-yunliang-chen; et al.

### EA-EGO-2026-0007

- Claim: 在 EgoScale 的测量区间内，egocentric human action pretraining 确有规模收益：1K 到 20K 小时使真实机器人平均任务完成度从 0.30 升到 0.71。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.3 Policy Performance Scales with Pretraining Data Size
- Evidence: 五个数据规模的同架构实验报告单调提升，并限制结论不外推到测量区间之外。
- Quote: “Average task completion rises monotonically from 0.30 at 1k hours to 0.71 at 20k hours”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-WMDATA-READ-0001

- Claim: τ0-WM 使用真实机器人遥操作、UMI 式交互、人类第一视角视频与 rollout/失败轨迹的异构语料，并用按模态的监督掩码训练统一视频—动作世界模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.01027](https://arxiv.org/abs/2606.01027) $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
- Locator: Abstract (full-text section)
- Evidence: 摘要直接报告了异构数据组成与 modality-specific supervision masks。
- Quote: “Abstract Robotic manipulation requires models that generate executable actions while anticipating and evaluating their future consequences before physical execution. We present -World Model ( -WM), a unified video-action world model that integrates policy learning, video prediction, and action evaluation within a single future-predictive framework. Built on a shared video diffusion backbone, -WM provides two complementary interfaces. First, a video action model jointly predicts future visual lat”
- Authors: pengfei-zhou; shengcong-chen; di-chen; et al.

### EA-DQ-YEAR-READ-0010

- Claim: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation
- Locator: C.4 Retention Balance, Single-Task Curation, and Real-Robot Failure Modes
- Evidence: ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。
- Quote: “To further ablate the role of Multitask Influence Interaction (MII), we visualize the retained task distributions after data curation in Fig. 8 . We consider the six-task real-robot setting with 120 demonstrations per task and an overall retention ratio of 66.7%. Without MII, naively ranking demonstrations with a single global influence score results in a highly skewed retained set: Pick Fruits, Shelf Retrieval, and Wipe Board retain 115, 113, and 104 demonstrations, respectively, whereas Stack”
- Authors: tao-xu; jiaxin-wang; runhao-zhang; et al.

### EA-PRETRAIN-DATA-2026-0003

- Claim: 多相机 VLA 不应把码率在机位和画面区域间均分；应优先保留对当前动作有用的视图和区域。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16253](https://arxiv.org/abs/2606.16253) SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models
- Locator: 1 Introduction and 3 Method
- Evidence: 论文指出不同机位和图像区域对控制的价值不均匀，SPARC 通过时序 mask 自适应分配比特。
- Quote: “Uniform bitrate allocation across cameras and image regions is therefore fundamentally inefficient.”
- Authors: sangyun-chung; mincheol-shin; jihyun-kim; et al.

### EA-PRETRAIN-DATA-2026-0002

- Claim: 任务匹配的人类 egocentric 视频能补齐少量机器人示范的动作覆盖空洞，但收益是在对齐与质量加权管线中实现的。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.17200](https://arxiv.org/abs/2606.17200) ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining
- Locator: 5.3 Human Data for Augmented Fine-Tuning, Figure 6
- Evidence: 419 条人类视频的工作空间覆盖是 34 条机器人示范的 4.8 倍，联合微调将 10 试验成功率从 10% 提高到 40%。
- Quote: “The 419 episodes of task-matched human video spread across 0.296 m 2 , 4.8 broader coverage”
- Authors: hao-li; ganlong-zhao; yufei-liu; et al.

### EA-PRETRAIN-DATA-2026-0006

- Claim: 当动作学习依赖多视图时，数据包应同步保存机位标识、视频、机器人状态和动作；10 Hz 是该 UR5 系统实例，不是预训练的通用帧率。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.11612](https://arxiv.org/abs/2512.11612) Embodied Image Compression: Towards Codec for Robotic Visual Systems
- Locator: Appendix C Subjective Data Collection
- Evidence: 真实管线同步记录腕部与第三人称 RealSense、关节角和末端增量动作，频率为 10 Hz。
- Quote: “Joint angles, two camera streams (wrist view and third-person view, captured by two Intel realsense cameras), and actions”
- Authors: zhenghao-chen; zijie-yue; haozhe-li; et al.

### EA-UMI-READ-0002

- Claim: UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only data is insufficient for force-sensitive tasks.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.09988](https://arxiv.org/abs/2601.09988) In-the-Wild Compliant Manipulation with UMI-FT
- Locator: Abstract (full-text section)
- Evidence: The HTML full text reports that UMI-FT mounts compact six-axis force/torque sensors on each finger, uses multimodal demonstrations to train adaptive compliance policies, and shows diverse in-the-wild data outperforming limited scene-diversity data in a skewer task.
- Quote: “Abstract Many manipulation tasks require careful force modulation. With insufficient force the task may fail, while excessive force could cause damage. The high cost, bulky size and fragility of commercial force/torque (F/T) sensors have limited large-scale, force-aware policy learning. We introduce UMI-FT, a handheld data-collection platform that mounts compact, six-axis force/torque sensors on each finger, enabling finger-level wrench measurements alongside RGB, depth, and pose. Using the mult”
- Authors: hojung-choi; yifan-hou; chuer-pan; et al.

### EA-DQ-YEAR-READ-0003

- Claim: 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.13197](https://arxiv.org/abs/2602.13197) Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos
- Locator: 3.3 Trajectory and Grasp Filtering via Simulation
- Evidence: PSI 将人类演示转换为 6DoF object pose trajectories 后在仿真中执行，用于过滤不适合机器人学习的数据；不适合原因包括 pose estimation errors 和机器人 physically unachievable trajectories，并生成 grasp suitability labels 以学习 task-oriented grasping。
- Quote: “Now that we have converted the human demonstrations into 6 DoF object pose trajectories, the next step is to execute them on a robot in simulation. This serves two purposes. One is to filter out those that may not be suitable for robot learning. There are two main reasons a trajectory may be unsuitable. First, pose estimation errors can lead to inaccurate trajectories. Second, the extracted trajectory may not be physically achievable by the robot. In either case, it would be harmful to train the”
- Authors: albert-j-zhai; kuo-hao-zeng; jiasen-lu; et al.

### EA-EGO-2026-0008

- Claim: 大规模 human pretraining 仍需少量精确 aligned human-robot mid-training 才能最好地落到可执行控制；规模和本体对齐是互补条件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.2 Large-Scale Human Pretraining Is Key to Strong Dexterous Manipulation Policy Performance
- Evidence: 四类 checkpoint 的消融中，pretrain+midtrain 最好；human pretraining 提供结构，mid-training 负责控制锚定。
- Quote: “combining human pretraining with a small amount of aligned mid-training yields the best overall performance”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-UMI-READ-0003

- Claim: UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.10647](https://arxiv.org/abs/2604.10647) OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction
- Locator: Abstract (full-text section)
- Evidence: The HTML full text repeatedly identifies limited physical interaction signals as a bottleneck of existing UMI-like systems and proposes synchronized RGB, depth, trajectory, tactile sensing, internal grasping force, and external wrench data to improve contact-rich policy learning.
- Quote: “Abstract UMI-style interfaces enable scalable robot learning, but existing systems remain largely visuomotor, relying primarily on RGB observations and trajectory while providing only limited access to physical interaction signals. This becomes a fundamental limitation in contact-rich manipulation, where success depends on contact dynamics such as tactile interaction, internal grasping force, and external interaction wrench that are difficult to infer from vision alone. We present OmniUMI, a uni”
- Authors: shaqi-luo; yuanyuan-li; youhao-hu; et al.

### EA-EGO-2026-0017

- Claim: 自动 RGB-only ego 标签存在明显 fidelity ceiling：严格阈值下左右 wrist pose recovery 仅约 66% 和 62%，规模化以噪声为代价。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 4.3 Egocentric Video Yields Effective Pretraining Labels
- Evidence: HOT3D ground truth 上的 10% sample 验证给出 head/wrist 三类严格阈值 recovery rate。
- Quote: “Under the strict tier ( , rot6d L2 ), head recovery reaches 78.82%, with left and right wrist recovery at 65.93% and 61.72%, respectively;”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-EGO-2026-0018

- Claim: 把 camera motion 当作 viewpoint action 可提供真实的 active-perception prior，但能力必须在有 head-camera/robot fine-tuning 的系统中承接。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 4.4 The Head Camera Enables Pretrained Active Perception
- Evidence: Restocking 中 egocentric-pretrained model 的 placement 为 24/27，SFT-only 为 6/27；移除 head camera 降到 1/27。
- Quote: “ActiveMimic scores 24 out of 27 on placement, whereas ActiveMimic sft-only achieves only 6 out of 27”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-PRETRAIN-DATA-2026-0001

- Claim: 异构来源应扩大，但在联合预训练前必须将空间坐标、本体形态、物理时间和标签可靠性显式对齐或条件化；否则会降低动作学习性能。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.17200](https://arxiv.org/abs/2606.17200) ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining
- Locator: 5.2 Ablation Studies, Figure 5(b)
- Evidence: 三项组件消融均降低 RoboCasa 成功率，其中去掉人类伪动作可靠性加权的降幅最大。
- Quote: “Removing morphology tokens makes the success rate drop from 72.8% to 70.9%”
- Authors: hao-li; ganlong-zhao; yufei-liu; et al.

### EA-EGO-2026-0004

- Claim: Ego-centric 轨迹构建存在规模—质量冲突：保留更多疑似背景/错误轨迹会显著降低真实机器人表现。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: IV-C Ablation Study
- Evidence: BGTS=1.0 保留 86,427 episodes 但真实机器人分数低于 BGTS=0.7 的 45,157 episodes。
- Quote: “Setting an appropriate curation threshold is crucial to balancing the scale and quality of our dataset”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGO-2026-0005

- Claim: 单目 RGB 人类视频恢复出的 hand-object 轨迹常不具物理可执行性；对象几何、手尺度/姿态误差会形成穿模、无效接触和抓取失败。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.09013](https://arxiv.org/abs/2602.09013) Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
- Locator: III-B Dexterous Grasp and Manipulation Learning
- Evidence: 方法段明确说明重建运动正确时，机器人—对象交互仍可能因几何误差而无效。
- Quote: “the resulting robot–object interactions are not always physically feasible due to reconstruction errors”
- Authors: hongyi-chen; tony-dong; tiancheng-wu; et al.

### EA-EGO-2026-0006

- Claim: 当前 VideoManip 依赖静态或近静态相机，并在真实闭环中用固定 hand-object 相对位姿绕过手部遮挡，限制了动态第一视角数据的可用范围。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.09013](https://arxiv.org/abs/2602.09013) Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
- Locator: V Conclusion, Limitations, and Future Work
- Evidence: 作者在限制段明确列出 dynamic camera 未覆盖；实验段说明对象点云被 LEAP Hand 遮挡时采用固定相对位姿近似。
- Quote: “The current framework assumes static or approximately static camera setups”
- Authors: hongyi-chen; tony-dong; tiancheng-wu; et al.

### EA-EGO-2026-0009

- Claim: Ego-centric 数据的动作接口会决定训练成败：wrist-only 缺失手指/接触时序，小 fingertip 误差又会映射成不合理关节和接触丢失。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.6 Hand Action Space Design for Human Pretraining
- Evidence: 动作空间消融中 wrist-only 普遍较差，fingertip mapping 在 Cards/Bottle 等接触敏感任务不稳定。
- Quote: “Small errors in fingertip pose often lead to implausible joint configurations after mapping”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-UMI-READ-0004

- Claim: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible task distribution.
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: Abstract (full-text section)
- Evidence: The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration data quality under challenging real-world conditions.
- Quote: “Abstract We present UMI-3D, a multimodal extension of the Universal Manipulation Interface (UMI) for robust and scalable data collection in embodied manipulation. While UMI enables portable, wrist-mounted data acquisition, its reliance on monocular visual SLAM makes it vulnerable to occlusions, dynamic scenes, and tracking failures, limiting its applicability in real-world environments. UMI-3D addresses these limitations by introducing a lightweight and low-cost LiDAR sensor tightly integrated i”
- Authors: ziming-wang

### EA-EGO-2026-0012

- Claim: 从人类视频恢复的 motion prior 会因遮挡、接触伪影和 retargeting 误差而物理不合理，不能直接当作 humanoid policy 的示范。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.20373](https://arxiv.org/abs/2605.20373) SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework
- Locator: 1 Introduction
- Evidence: 引言直接列出三类误差并说明它们使数据 unsuitable for direct policy learning。
- Quote: “Severe occlusion, contact artifacts, and retargeting errors render this data physically implausible for direct imitation”
- Authors: tianshu-wu; xiangqi-kong; yue-chen; et al.

### EA-EGO-2026-0015

- Claim: HumanEgo 的高成功率依赖强 hand/object tracking 前端；单目绝对深度、动态遮挡、模块级联误差和亚厘米接触精度仍是未解决困难。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.24934](https://arxiv.org/abs/2605.24934) HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos
- Locator: 5 Conclusion
- Evidence: 作者在 limitation 段逐项列出 stereo hand tracking、occlusion-robust tracking、cascading failures 和 1 cm plateau。
- Quote: “monocular substitutes drop real-world success sharply”
- Authors: zhi-wang; botao-he; kelin-yu; et al.

### EA-EGO-2026-0016

- Claim: Ego-centric wrist trajectory 与相机自运动天然耦合；若不统一参考系，动作监督会把 camera rotation/translation 错算为 hand motion。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.06194](https://arxiv.org/abs/2606.06194) ActiveMimic: Egocentric Video Pretraining with Active Perception
- Locator: 3 Method
- Evidence: 方法段明确说明 current-frame wrist pose 与 first-frame camera path 的坐标差异会混合两类位移。
- Quote: “using these wrist poses directly as action supervision would therefore conflate wrist movement with camera motion”
- Authors: xingyao-lin; guojin-zhong; tianyi-lu; et al.

### EA-EGO-2026-0019

- Claim: Ego-human motion 的 pose/joint 对齐只能保证自由空间几何相似；不显式建模 hand-object contact，就难以保持持续接触、物体交换和多阶段操作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.03828](https://arxiv.org/abs/2607.03828) ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Modeling
- Locator: II-B Human-to-Robot Motion Retargeting
- Evidence: 相关工作和引言都指出现有方法多假设 object-free/weak-contact，忽略手臂与手的不同功能。
- Quote: “most methods assume object-free or weak-contact settings and focus on geometric consistency or joint error minimization”
- Authors: yuanchuan-lai; qing-gao; ziyan-liang; et al.

### EA-DQ-YEAR-READ-0015

- Claim: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06442](https://arxiv.org/abs/2607.06442) SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: Introduction
- Evidence: 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。
- Quote: “Our contributions are as follows: • We propose a primitive-compositional view of trajectory utility, realized by Primitive Discovery and Structural Exposure Allocation, which allocate selection budgets according to reuse-aware primitive and transition exposure under diminishing returns. • We introduce Learning-Friendly Trajectory Selection, which selects medoid trajectories within each composition-pattern bucket to favor central, stable, and predictable realizations for behavior cloning. • We pr”
- Authors: changti-wu; bin-yu; zhaolong-shen; et al.

### EA-ALIGN-READ-0012

- Claim: DQAF 不用成功/失败二值标签代替数据质量，而是联合子任务进度、动作平滑度、停顿和运动学极限生成 episode 级评估与给操作者的纠正反馈。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.26349](https://arxiv.org/abs/2605.26349) Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection
- Locator: Abstract (full-text section)
- Evidence: 摘要明确列出了质量信号、结构化评估和可执行的自然语言反馈。
- Quote: “Abstract Industrial automation is at a pivotal moment, as Physical AI is driving a transition from rigid, hand-engineered automation systems toward more flexible and adaptive systems. This shift has created a growing demand for large-scale, real-world robot demonstration data, making teleoperation an increasingly important mechanism for data collection. However, high-quality teleoperated demonstrations remain difficult to obtain in practice, as novice operators often produce episodes that are ta”
- Authors: gokul-narayanan; yash-shahapurkar; melih-erdogan; et al.

### EA-ALIGN-READ-0001

- Claim: A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics.
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.24049](https://arxiv.org/abs/2606.24049) SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies
- Locator: 3.2 Inconsistency of Control Commands across Robots
- Evidence: SPACE predicts Cartesian state deltas as a shared end-effector-space representation and uses an action adapter to convert them into robot-specific control commands, improving cross-robot and dynamics-shift robustness.
- Quote: “Recent work has scaled robot learning by training policies on data from multiple embodiments [ 27 , 23 , 32 ] , often using the Cartesian delta action space [ 23 , 32 ] since it is less dependent on robot-specific kinematics and invariant to base-frame translation [ 18 , 14 ] . In practice, this is typically realized by predicting Cartesian delta control commands that are fed to the underlying robot controller [ 23 , 32 ] . Figure 2: Different robots (e.g., UR5 vs. Franka Research 3) require dif”
- Authors: haeone-lee

### EA-TACTILE-2026-0001

- Claim: 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19161](https://arxiv.org/abs/2606.19161) HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision
- Locator: Abstract; 3 HT-Bench: A Multi-Task Tactile Evaluation Benchmark
- Evidence: 摘要和基准设计章节直接给出数据规模、四项评测任务与任务级 OOD 划分。
- Quote: “comprising 10M RGB frames and 7.8M tactile frames collected across 226 tasks.”
- Authors: yuzhe-huang; jiaping-wu; jiaming-jiang; et al.

### EA-TACTILE-2026-0002

- Claim: HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19161](https://arxiv.org/abs/2606.19161) HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision
- Locator: 6 Limitations and Future Work
- Evidence: 作者在限制章节明确列出硬件/本体覆盖和闭环下游评测缺失。
- Quote: “While these tasks assess structural, cross-modal, and temporal understanding, they do not directly measure downstream robotic performance.”
- Authors: yuzhe-huang; jiaping-wu; jiaming-jiang; et al.

## References

- `2509.01657` [Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657) (2025-09-01)
- `2509.21986` [Developing Vision-Language-Action Model from Egocentric Videos](https://arxiv.org/abs/2509.21986) (2025-09-26T07:09:33Z)
- `2512.08269` [EgoX: Egocentric Video Generation from a Single Exocentric Video](https://arxiv.org/abs/2512.08269)
- `2512.11612` [Embodied Image Compression: Towards Codec for Robotic Visual Systems](https://arxiv.org/abs/2512.11612) (2025-12-12T18:59:07Z)
- `2512.13100` [OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning](https://arxiv.org/abs/2512.13100) (2025-12-15)
- `2601.09988` [In-the-Wild Compliant Manipulation with UMI-FT](https://arxiv.org/abs/2601.09988) (2026-01-15)
- `2602.09013` [Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction](https://arxiv.org/abs/2602.09013) (2026-02-09T18:56:02Z)
- `2602.13197` [Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197) (2026-02-13)
- `2602.16710` [EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data](https://arxiv.org/abs/2602.16710) (2026-02-18T18:59:05Z)
- `2604.10647` [OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction](https://arxiv.org/abs/2604.10647) (2026-04-12)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089) (2026-04-15)
- `2605.06747` [HumanNet: Human-centric Video Dataset for Robot Learning](https://arxiv.org/abs/2605.06747)
- `2605.20373` [SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework](https://arxiv.org/abs/2605.20373) (2026-05-19T18:24:05Z)
- `2605.24934` [HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos](https://arxiv.org/abs/2605.24934) (2026-05-24T08:26:41Z)
- `2605.26349` [Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349) (2026-05-25)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.06194` [ActiveMimic: Egocentric Video Pretraining with Active Perception](https://arxiv.org/abs/2606.06194) (2026-06-04T14:01:01Z)
- `2606.16208` [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208) (2026-06-15)
- `2606.16253` [SPARC: Spatially Adaptive Rate Control for Vision-Language-Action Models](https://arxiv.org/abs/2606.16253) (2026-06-15T03:38:29Z)
- `2606.17200` [ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining](https://arxiv.org/abs/2606.17200) (2026-06-15T18:40:18Z)
- `2606.19161` [HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision](https://arxiv.org/abs/2606.19161) (2026-06-17)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2607.03828` [ObjRetarget: An Object-Aware Motion Retargeting Framework with Anthropomorphic Arm Constraints and Polyhedral Hand Modeling](https://arxiv.org/abs/2607.03828) (2026-07-04T11:31:23Z)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
- `2608.02580` [Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data](https://arxiv.org/abs/2608.02580)
- `2608.04196` [SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation](https://arxiv.org/abs/2608.04196)
