# Evidence Appendix: 近一年鱼眼镜头在具身领域的应用

- Time range: 2025-09-09 to 2026-09-09
- Events: 746
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### LR-FISHEYE-2026-0447

- Claim: exUMI 保留 UMI 的腕装 GoPro 鱼眼镜头作为主视觉输入，并把相机安装位置前移（跟随 FastUMI 的设置）以获得更宽且更清晰的视野、消除采集者身体对视野的遮挡从而增强向机器人迁移性；部署侧策略评估同样仅使用该 GoPro 相机作为视觉输入。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 14, Appendix A.1 Visual Input
- Evidence: 附录 A.1 Visual Input 说明与 UMI 相同采用带鱼眼镜头的 GoPro 作为主视觉输入，相机前移跟随 FastUMI 以获得更宽更清晰视野并消除身体遮挡；正文 Section 5.2 说明真机评估用 GoPro 作为唯一视觉输入。
- Quote: “Visual Input. Same as the UMI [1], we employ a GoPro camera with a fisheye lens as our primary visual input. We move the camera forward, following FastUMI [32] for a wider and clearer view. The camera positioning eliminates body occlusion in the field of view to enhance transferability.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0449

- Claim: 以 AR MoCap+磁编码器替代视觉 SLAM/ArUco 跟踪后，exUMI 的数据采集处理管线显著简化且更稳健，数据处理成功率接近 100%，而 vanilla UMI 不到 60%。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 5, Section 3.2 Data Processing
- Evidence: Section 3.2 末段总结：经过精心设计，exUMI 能稳健采集带准确 6D 位姿与夹爪宽度的演示数据，采集处理管线显著简化且更稳健，数据处理成功率接近 100%，相比之下 vanilla UMI 不到 60%。
- Quote: “Our data collection pipeline is significantly simplified and more robust, leading to a nearly 100% data processing success rate compared to less than 60% of vanilla UMI.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0450

- Claim: 部署侧评估配置：Flexiv Rizon 4 机械臂 + Flexiv Grav 自适应夹爪，GoPro 相机为唯一视觉输入，采用 diffusion policy（ViT 图像骨干）+多模态直接特征拼接，每任务评估 20 trials，控制频率 10 Hz。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 7, Section 5.2 Experiment Settings for Imitation Learning
- Evidence: Section 5.2 说明评估平台与策略结构：Flexiv Rizon 4 + Flexiv Grav、GoPro 唯一视觉输入、diffusion policy+ViT 骨干、直接特征拼接、20 trials；附录 C 说明 RTX 4070 主机 10 Hz 控制与 pipe-clamp 支架复刻 exUMI 末端传感器布局。
- Quote: “We evaluate our learning system on a Flexiv Rizon 4 robot arm with a Flexiv Grav adaptive gripper, and use a GoPro camera as the only visual input. We adopt diffusion policy [47] with a ViT image backbone model, and direct feature concatenation for multimodal inputs. We evaluate our policy for 20 trials.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0452

- Claim: 触觉输入与 TPP 预训练的增益集中在力敏感阶段：Pull Drawer（随机 50-1000g 石头）成功率 40%（vision-only）→50%（vision+tactile）→95%（+TPP），Peg in Hole Insert 阶段 50%→60%→80%；而无需触觉的阶段（Pull Drawer Empty、Peg Grasp）三种策略均达 100%。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 8, Table 3
- Evidence: Table 3 报告触觉任务三级对比：Put Ball 70/70/85、Open Bottle 20/50/60、Pull Drawer Empty 100/100/100、Random 40/50/95、Peg Grasp 100/100/100、Insert 50/60/80；正文指出力敏感阶段触觉策略持续带来改进，TPP 把两者分别提升至 95% 与 80%。
- Quote: “Input Representation Put Ball Open Bottle Pull Drawer Peg in Hole Empty Random Grasp Insert Vision Only 70% 20% 100% 40% 100% 50% Vision & Tactile 70% 50% 100% 50% 100% 60% Vision & Tactile w/ TPP (Ours) 85% 60% 100% 95% 100% 80%”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0453

- Claim: TPP 输入消融显示多模态条件化单调降低触觉预测误差：验证集 MSE 从仅以 RGB 图像为输入的 0.0298 降至触觉历史 0.0132、触觉+RGB 0.0125、触觉+动作 0.0117，全输入（触觉历史+动作+RGB）最优 0.0099——动作感知是误差最大的单项改善来源之一。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 6, Table 1
- Evidence: Table 1 对触觉预测预训练做输入设置消融：五种输入组合的验证集 MSE 表明视觉与动作序列的多模态条件化都能降低触觉预测误差，其中动作感知预测取得最佳性能。
- Quote: “Tactile History Action Input RGB Image MSE Error ✗ ✓ ✓ 0.0298 ✓ ✗ ✗ 0.0132 ✓ ✗ ✓ 0.0125 ✓ ✓ ✗ 0.0117 ✓ ✓ ✓ 0.0099”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0454

- Claim: 触觉表征学习算法对比中，TPP 在两个任务上均最优：Put Ball 85%、Peg in Hole 80%，优于 BYOL 空间自监督（80%/50%）与直接多模态模仿（70%/60%）、vision-only（70%/50%）；BYOL 在 Peg in Hole 上（50%）甚至不优于 vision-only。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 18, Table 6
- Evidence: 附录 D.2 按作者采集数据重训 direct 学习与 BYOL（按 MimicTouch）作对比，Table 6 显示 TPP 在 Put Ball 与 Peg in Hole 上取得最佳成功率。
- Quote: “Modality V V+T V+T V+T Tactile Learning / Direct BYOL TPP (Ours) Put Ball 70% 70% 80% 85% Peg in Hole 50% 60% 50% 80%”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0455

- Claim: exUMI 的 play 数据采集在接触密度与效率上均大幅优于常规采集：自采数据有效触觉帧占比超 60%（常规采集数据不足 10%），480K 触觉帧仅需 5 小时人机交互（遥操作系统需 10 倍时间），总计 1M 帧对齐图像-触觉-动作数据。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 5, Section 4.2 Action-aware Tactile Data Collection
- Evidence: Section 4.2 说明采集者随机操作 10 个真实环境、300+ 物体，共采 1M 帧对齐图像-触觉-动作数据；有效触觉帧超 60% 对比常规采集 <10%；480K 触觉帧仅 5 小时人机交互完成，遥操作需 10 倍时间。
- Quote: “Our data has rich contacts with over 60% active tactile frames, compared to less than 10% of regular data collection [12]. The contact richness further enhances our collec- tion efficiency, and the 480 K tactile frames are collected from just 5 hours of human interaction, which would take 10× the time for a teleoperation system.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0456

- Claim: exUMI 数据集的原始触觉帧规模（480.9K）显著超过既有真实世界触觉数据集：此前最大规模的 TVL 为 43.7K 帧，Touch2Touch 32.3K、Touch and Go 13.9K、VisGel 12.0K，exUMI 约为 TVL 的 11 倍，且是少数以人类手持采集（而非机器人采集）的数据集之一。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 17, Table 5
- Evidence: 附录 B 的 Table 5 对比 11 个真实世界触觉数据集的规模、传感器、本体感知与采集来源：exUMI 以 480.9K 原始帧居首（9DTact+，人类采集），TVL 43.7K（DIGIT，机器人采集）次之。
- Quote: “TVL [12] 43.7 K DIGIT ✓ Robot Touch2Touch [52] 32.3 K Multiple ✓ Robot X-Capture [43] 3.0 K DIGIT ✗ Human Ours 480.9 K (raw frames) 9DTact+ ✓ Human”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0457

- Claim: 对简单 pick-and-place 任务，采集者用 exUMI 可在 20 分钟内完成 100 条演示，达到 100% 数据可用率，且行为克隆策略取得超 70% 任务成功率。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 2, Section 1 Introduction
- Evidence: 引言以 pick-and-place 为例给出效率数字：20 分钟 100 条演示、100% 数据可用率、行为克隆超 70% 成功率；Table 2 逐任务采集时长（26-79 分钟/任务）与之相容。
- Quote: “For a simple pick-and-place task, a user could collect 100 demonstrations in 20 minutes to achieve 100% data usability and over 70% task success rate by behavior cloning.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0460

- Claim: exUMI 整机默认配置成本 698 美元，其中 GoPro 11+配件（298 美元）为最大单项（约 43%）；作者指出可通过替换为其它鱼眼相机进一步降成本（目标降至 500 美元以下）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 14, Table 4 and Appendix A.1 Cost and Accessibility
- Evidence: 附录 A.1 成本小节与 Table 4 BOM：默认配置 698 美元（GoPro 298、Meta Quest 299、Orange Pi 35、触觉传感器 30 等），可用替代鱼眼相机进一步降低；Broader Impact 提及正推进到 500 美元以下。
- Quote: “Our system is low-cost with a minimal configuration starting at $ 698, which can be further reduced by substituting the GoPro with alternative fisheye cameras.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0461

- Claim: 替代鱼眼视觉跟踪的 AR MoCap 方案精度受控验证：把 AR 控制器装在机器人末端并遥操作运动（50 cm 范围内），相对真值轨迹的平均位置误差为三轴 5.4/2.3/1.7 mm，旋转误差低于 1 度；x 轴（深度轴）误差最大达 20 mm。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 15, Appendix A.3 System Evaluation
- Evidence: 附录 A.3 系统评估：AR 控制器安装于机器人末端、遥操作机器人在 50 cm 范围内运动获取真值与估计轨迹，6D 位姿差显示三轴平均位置误差 5.4/2.3/1.7 mm、旋转误差低于 1 度，x 轴为深度轴误差最大 20 mm。
- Quote: “The system demonstrates remarkable accuracy, achieving mean position errors of 5.4 / 2.3 / 1.7 mm at each axis. The rotation errors are below 1 degree (notably small due to the robot’s limited rotation range). The x-axis error reaches a maximum of 20 mm since it is the depth axis in the Flexiv coordinate system and inherently presents greater measurement challenges.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-1116

- Claim: 领域定位与核心主张：全向视觉（以 360° 视觉理解环境）在机器人、工业巡检、环境监测等域的重要性持续上升；相对传统针孔视觉提供整体环境感知、显著提升场景感知完整性与决策可靠性；其基础研究历史上落后于针孔视觉，当前在具身 AI 时代因工业需求与学术兴趣而快速发展——本文（AAAI 2026 talk 论文，作者含 Insta360 工业方）提出由四个子系统构成的全景系统架构 PANORAMA。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 1, Abstract
- Evidence: 摘要陈述：omnidirectional vision 跨域重要性、相对 pinhole 的整体感知优势、历史滞后、具身 AI 时代快速发展、生成/感知/理解/数据集四线突破、PANORAMA 四子系统架构。
- Quote: “has become increasingly critical across do- mains like robotics, industrial inspection, and environmental monitoring. Compared to traditional pinhole vision, omnidi- rectional vision provides holistic environmental awareness, significantly enhancing the completeness of scene perception and the reliability of decision-making. However, foundational research in this area has historically lagged behind traditional pinhole vision. This talk presents an emerging trend in the embodied AI era: the rapid”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1120

- Claim: 生成侧进展：早期以 GAN 方法为主（Dream360 以两阶段策略——codebook 全景外扩+频率感知细化——从选定 viewport 生成高质量高分辨率全景）；扩散模型成为主流后相关研究渐起：PanoDiffusion 以双分支扩散结构允许训练时输入 RGB-D 数据、向生成模型注入更多空间信息以提升全景质量，OmniDrag 以轨迹控制全景生成、增强用户友好性。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 2, Recent Technical Advances: Omnidirectional Generation
- Evidence: Recent Technical Advances 生成节：Dream360 两阶段外扩、PanoDiffusion 双分支 RGB-D 条件扩散、OmniDrag 轨迹控制。
- Quote: “Researchers focus on the generative adversarial network- based methods for omnidirectional generation at the early stage (Ai et al. 2024; Chen, Wang, and Liu 2022; Cheng et al. 2022; Wang et al. 2022; Oh et al. 2022). Typically, through a two-stage strategy, including both codebook- based panorama outpainting and frequency-aware refine- ment, Dream360 (Ai et al. 2024) successfully generates high-quality and high-resolution panorama images based on selected viewports. As diffusion models have bec”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1121

- Claim: 感知侧域适应路线：针对全景数据瓶颈，域适应成为让模型用无标注全景数据的主流方案，现有策略分三类——对抗学习（判别器迫使跨域难区分特征）、伪标签（GoodSAM/GoodSAM++ 用 SAM 精化伪标签、OmniSAM 动态伪标签更新提升可信度）、原型对齐（360SFUDA++/OmniSAM 以畸变匹配+原型语义抽象对齐源/目标域中心，yielding significant improvements）。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 2, Recent Technical Advances: Omnidirectional Perception
- Evidence: Recent Technical Advances 感知节：三类域适应策略与代表工作（GoodSAM/GoodSAM++/OmniSAM/360SFUDA++）。
- Quote: “Considering the data bottleneck problems of omnidirec- tional vision, the domain adaptation technique has become a popular solution that enables models to deal with panoramic images with unlabeled data (Zheng et al. 2024). The existing strategies can be primarily classified into three types: ad- versarial learning-based strategy, pseudo-label-based strat- egy, and prototype-based strategy (Zhong et al. 2025). Ad- versarial learning-based strategies introduce a discrimina- tor to force the model”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1122

- Claim: 理解侧进展与瓶颈：现有多模态大模型经普通（尤其针孔）图像训练、从未见过全景图像故难以理解；数据侧以构建全景理解数据集/基准为主（OSR-bench 提出认知地图概念分块标注、OmniVQA 以 agent 协作高效标注）；模型侧多用 GRPO 等技术在既有 VQA 数据上直接微调，而 ERP-RoPE 尝试探索全景图像内部特征以进一步增强理解。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 2, Recent Technical Advances: Omnidirectional Understanding
- Evidence: Recent Technical Advances 理解节：MLLM 针孔训练局限、OSR-bench/OmniVQA 数据路线、GRPO 微调与 ERP-RoPE 模型路线。
- Quote: “Current multi-modal large language models tend to be trained through normal images, especially the pinhole im- ages. Consequently, these models struggle to understand panoramic images, having never encountered them be- fore. From the perspective of data, recent works focus on building omnidirectional understanding datasets and bench- marks (Dongfang et al. 2025; Zhang, Ye, and Zheng 2025; Song et al. 2024; Zhou et al. 2025; Chou et al. 2020). Es- pecially, OSR-bench (Dongfang et al. 2025) create”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1123

- Claim: 数据集版图（Table 1）：按 Indoor/Outdoor/UAV（Flight）× Real/Synthetic 分类盘点 23 个代表性数据集——室内真实侧 ZInD 71K 全景/1.5K 住宅、Matterport3D 10.8K 图像/90 栋、Stanford 2D-3D-S 70K 图像；户外真实侧 StreetLearn 143K 图像、360VOT 120 序列/113K 帧、Dense360 160K 全景+5M 实体级 caption、360Loc 多设备定位测试床；QA 侧 OSR-Bench 153,000+ 问答对；UAV 侧最薄（真实仅 UAV-ERP 2.3K 已标注图像，合成仅 AirSim-360）——室内数据密语义、户外/飞行数据重空间覆盖。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 3, Table 1 与其后总结段
- Evidence: Table 1 以 Scene/Source/Dataset/Year/Annotations/Scale 六列盘点 23 个数据集；正文总结 common modalities、granularity 差异（室内密语义 vs 户外重覆盖）与 identify 23 representative datasets 的口径。
- Quote: “Scene Source Dataset Year Annotations Scale Indoor Real PanoContext (Dong et al. 2024) 2014 Layouts, object 3D bounding boxes 700 full-view panoramas Stanford 2D-3D-S (Armeni et al. 2017) 2017 RGB, depth, semantics 70,000 images Matterport3D (Chang et al. 2017) 2017 RGB-D panoramas, 2D/3D semantics & poses 10.8 K images, 90 buildings ZInD (Cruz et al. 2021) 2021 360 ◦ panoramas, 3D layouts, floorplans 71 K panoramas, 1.5 K homes HM3D (Ramakrishnan et al. 2021) 2021 Textured 3D mesh reconstructi”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1125

- Claim: PANORAMA 理想系统架构（应用方式蓝图）：四子系统——(1) 数据采集与预处理：ERP 或 multi-fisheye lens rigs 相机+IMU/深度等互补传感器，负责数据采集、格式转换（ERP↔Cubemap 按下游需求动态切换）、多/多模态传感器同步与标定；(2) 感知：面向球面几何适配的深度模型（Spherical CNN/Transformer）提取特征，共享骨干同时做语义分割/目标检测/深度估计；(3) 应用：消费结构化感知输出服务导航与 SLAM、人机交互、数字孪生与 3D 重建等具身任务；(4) 加速与部署：量化/剪枝平衡精度-延迟-功耗，边缘平台（NVIDIA Jetson、SOPHGO SE9）落地——四者构成从原始传感器到具身应用的一体化管线。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 4, PANORAMA System Architecture: Key Subsystems 与 Workflow（Fig. 2）
- Evidence: PANORAMA System Architecture 节给出四子系统（数据采集与预处理/感知/应用/加速与部署）的职责、硬件与代表技术，及一体化 Workflow。
- Quote: “data and converting it into a format suitable for compu- tational processing. It primarily consists of hardware like cameras (e.g., those utilizing equirectangular projection or multi-fisheye lens rigs) and complementary sensors (e.g., IMUs, depth sensors). Its core functions include: • Data Capture: Acquiring high-resolution omnidirec- tional images and videos. • Format Conversion: Dynamically transforming data be- tween different representations (e.g., ERP, Cubemap) to suit the needs of downst”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1126

- Claim: 六阶段路线图：Stage 1 数据集整合（统一投影/标准划分/一致重标注/灵活重投影工具保证 ERP 与 cubemap 公平比较）；Stage 2 多模态扩展（同步 RGB/深度/LiDAR/音频/IMU、标准化 rig 与标定协议、公共多传感器语料、real-synthetic 混合采集控成本）；Stage 3 推理与具身数据（grounded VQA/指令跟随/导航/抓取，模板+LLM+人验的混合问题生成，仿真环境供动态场景）；Stage 4 统一模型预训练（联合 360° 几何+语义+同步传感器流的多任务编码器，跨投影表示/多目标损失/域混合课程）；Stage 5 评测与基准（标准划分、投影一致重投影工具、逐任务精度+跨投影一致性+具身任务成功率、OOD 划分/校准/不确定性/效率目标）；Stage 6 部署与泛化（跨域迁移/持续学习/真实条件鲁棒性、部署套件与压力测试数据集）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 5, Stages 1-5（Stage 6 起于 page 5 末、续于 page 6；Fig. 3 同页）
- Evidence: Emerging Trends & Future Roadmap 节与 Fig. 3 给出六阶段（Dataset Integration/Multi-Modal Expansion/Reasoning and Embodied Data/Unified Model Pretraining/Evaluation and Benchmarking/Deployment and Generalization）及各阶段关键交付物。
- Quote: “Stage 1: Dataset Integration In the first stage, the focus is on bringing together existing datasets into a single, consis- tent framework for projections, along with standardized test splits. The data will be re-annotated with consistent labels, and flexible re-projection tools will help ensure fair compar- isons of model performance across different formats, like ERP and cubemap. This stage will result in a well-organized benchmark suite, with careful human checks to reduce errors in the annot”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1127

- Claim: 跨社区获益面（定性）：(1) 机器人与自主导航——全向感知是完整态势感知的基石，消除盲点使密集动态环境（如拥挤公共场所）导航更准确更安全，并提供多角度上下文；(2) 人机交互——配全向相机的机器人可同时追踪多个个体、解读群组对话、理解来自任意方向的社会线索，促成更自然无缝可信的 HRI；(3) 认知 AI 与虚拟代理——全向视觉提供本质上更接近人类 ego 视觉的稠密信息流，支撑空间推理、长程任务规划与环境物理常识等高级认知能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 6, Cross-Community Impacts & Open Challenges（前三 bullet）
- Evidence: Cross-Community Impacts 节列出三类社区的获益机制（均以引用支撑的定性论断）。
- Quote: “In today’s era of embodied AI, the maturity of omnidirec- tional vision no longer merely refers to the gradual up- date of technology but rather its emergence as a fundamen- tal enabling technology, promoting cross-community break- throughs in practical application domains. The impact of omnidirectional vision, especially the PANORAMA system, in the current era extends far beyond a single community, providing cross-community impacts for researchers from di- verse fields: • Robotics & Autonomous”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1130

- Claim: 终局主张与三方分工：具身智能时代要求从'狭窄前视'到'球面理解世界'的范式转移，拥抱全向视觉可共同解锁具身 AI 下一前沿（造出不仅看见而且理解并与环境整体交互的 agent）——'具身 AI 的未来是全向的'；并呼吁三方分工：数据集创建者发布覆盖室内外/通用/具身场景的大规模多任务全景数据集、算法研究者超越针孔模型的简单适配创造带全向信息的新架构与动态学习范式、应用工程师在真实机器人与交互系统中展示全向感知收益以弥合实验室与实践。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 6, Conclusion（In summary 段）
- Evidence: 结论段：范式转移表述、三方呼吁（Dataset Creators/Algorithm Researchers/Application Engineers）与终局句 The embodied AI's future is omnidirectional。
- Quote: “In summary, the process towards achieving truly embodied intelligence is a collective effort. In the field of omnidirec- tional vision, we call upon researchers to: • For Dataset Creators: Plan and publish large-scale multi-task omnidirectional datasets that encompass the complexity of real-world scenes, including both indoor and outdoor scenarios, general scenarios, and embodied intelligent scenarios. • For Algorithm Researchers: Go beyond simple adapta- tions based on pinhole models and create”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1206

- Claim: 内窥镜鱼眼的应用动机与处理路线：内窥镜因鱼眼效应（fisheye effect）获得增大的视场（increased field of view）；管线在探索前做棋盘格标定获取 SLAM 所需相机参数，随后按 DROID-SLAM 原实现对相机流去畸变（undistort），围绕图像中心裁剪以去除内窥镜视野周围的黑边，再缩放到 SLAM 模型输入尺寸；重建逆投影使用标定所得、对应去畸变图像的矫正相机矩阵（rectified camera matrix）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 5-6, Section 3.3 Real time 3D Reconstruction
- Evidence: page 5-6 Section 3.3：checkerboard 标定→undistort（following the original DROID-SLAM implementation）→中心裁剪去黑边→缩放→rectified camera matrix 逆投影；跨页 5→6 断行（"fisheye effect" 在 page 5 末、"for an increased field of view" 在 page 6 首）。
- Quote: “We perform a checkerboard calibration before explorations to obtain the camera parameters required by the SLAM framework. Since the endoscope has a fisheye effect 5 ## page 6 for an increased field of view, following the original DROID-SLAM implementation, we undistort the camera stream. We crop the images around the image center to remove the black mask around the endoscope view. Then, we scale these preprocessed images to match SLAM’s model input size. During the reconstruction, for the invers”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1207

- Claim: 管线全程在针孔模型空间运行且不依赖深度相机硬件：DROID-SLAM 把修正后的逐像素深度经逆投影函数+针孔相机模型映射为 3D 点云；为增强单目视频，作者集成定制 in-domain MDE 模型为 SLAM 创建先验，构成伪 RGB-D 管线（称 RGB-D SLAM），免去笨重昂贵的深度相机；DROID-SLAM 权重取自原作不做额外训练，以检验重建算法的泛化能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 5, Section 3.3 Real time 3D Reconstruction
- Evidence: page 5 Section 3.3：pinhole camera model 逆投影、pseudo-RGB-D（without the bulky and expensive depth cameras）、DROID-SLAM 权重无再训练。
- Quote: “The corrected depth values are later mapped to a point cloud in 3D using an inverse projection function and the pinhole camera model. DROID-SLAM supports multiple input modes, such as RGB- D or stereo. To augment our monocular video, we integrate our customized in-domain MDE model to create priors for the SLAM algorithm. This results in a pseudo-RGB-D pipeline (referred to as RGB-D SLAM), without the bulky and expensive depth cam- eras. We use the DROID-SLAM model weights from [28] without addit”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1208

- Claim: 临床动机：NOTES（经自然孔道手术）经口、尿道、肛门或阴道等自然孔道操作、免额外切口，但以增加复杂性为代价——可视化、空间定向、深度感知与解剖识别的困难使这类手术具有挑战性、抑制专业掌握与实用推广；这些限制显示了对更好场景理解（引导外科医生与自动化）的显著需求。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 2, Section 1 Introduction
- Evidence: page 2 Section 1 Introduction：NOTES 自然孔道列表 + 四类困难（visualization, spatial orientation, depth perception, anatomy recognition）+ 场景理解需求。
- Quote: “NOTES allow operating through natural orifices such as the mouth, urethra, anus, or vagina, without additional inci- sions; however, at the cost of increasing complexity. Difficulties in visualization, spatial orientation, depth perception, and anatomy recognition make these procedures chal- lenging, throttling expertise and practical applicability [2]. These limitations show the significant need for better scene understanding to guide surgeons and automation.”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1210

- Claim: CAO 重建定量结果：RGB-D SLAM 距离指标全面优于或持平 SfM——中位最近点距离 0.53±0.32 vs 0.63±0.13 mm、单侧 Chamfer 0.66±0.40 vs 0.90±0.17 mm、单侧 Hausdorff 6.92±2.24 vs 100.96±127.29 mm；速度优势巨大：post-BA 每帧 0.46±0.07 s vs SfM 6.39±1.98 s（pre-BA 0.29±0.02 s）；RGB SLAM 为 0.52±0.23 / 0.67±0.30 / 15.10±5.27 mm、post-BA 0.42±0.07 s——实时化同时提升精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 7, Table 1 (Central Airway Obstruction)
- Evidence: page 7 Table 1 CAO 块全行：MCP/CD/HD/Pre-BA/Post-BA 时间、分割精度、点数、覆盖；SfM 基线为 DISK+LightGlue（HLoc，同口径去畸变+裁剪预处理）。
- Quote: “Central Airway Obstruction SfM RGB SLAM RGB-D SLAM Median Closest Point Dist. (mm) ↓ 0.63 ± 0.13 0.52 ± 0.23 0.53 ± 0.32 One-sided Chamfer Dist. (mm) ↓ 0.90 ± 0.17 0.67 ± 0.30 0.66 ± 0.40 One-Sided Hausdorff Dist. (mm) ↓ 100.96 ± 127.29 15.10 ± 5.27 6.92 ± 2.24 Pre-BA Time Per Frame (sec) ↓ - 0.26 ± 0.02 0.29 ± 0.02 Post-BA Time Per Frame (sec) ↓ 6.39 ± 1.98 0.42 ± 0.07 0.46 ± 0.07 Segmentation Precision (%) ↑ 96.69 ± 1.59 85.48 ± 5.09 88.07 ± 2.56 # Reconstruct. Points (x1000) ↑ 121.6 ± 44.6 10”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1211

- Claim: BPH 跨解剖定量结果：RGB-D SLAM 中位最近点 0.52±0.15 vs SfM 1.86±0.30 mm、单侧 Chamfer 0.65±0.19 vs 2.25±0.40 mm、单侧 Hausdorff 9.95±1.78 vs 31.63±13.95 mm；post-BA 每帧 0.28±0.05 s vs SfM 16.76±8.70 s；RGB SLAM 为 0.63±0.19 / 0.89±0.19 / 21.25±14.61 mm、0.26±0.05 s——换解剖（气管→前列腺尿道）后仍维持亚毫米级 Chamfer 精度与实时速度。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 7, Table 1 (Benign Prostatic Hyperplasia)
- Evidence: page 7 Table 1 BPH 块全行；与 CAO 块趋势一致（"In both the CAO and the BPH cases, error metrics show similar trends"，page 9）。
- Quote: “Benign Prostatic Hyperplasia SfM RGB SLAM RGB-D SLAM Median Closest Point Dist. (mm) ↓ 1.86 ± 0.30 0.63 ± 0.19 0.52 ± 0.15 One-sided Chamfer Dist. (mm) ↓ 2.25 ± 0.40 0.89 ± 0.19 0.65 ± 0.19 One-Sided Hausdorff Dist. (mm) ↓ 31.63 ± 13.95 21.25 ± 14.61 9.95 ± 1.78 Pre-BA Time Per Frame (sec) ↓ - 0.21 ± 0.05 0.23 ± 0.05 Post-BA Time Per Frame (sec) ↓ 16.76 ± 8.70 0.26 ± 0.05 0.28 ± 0.05 Segmentation Precision (%) ↑ 96.23 ± 2.64 89.71 ± 5.18 90.87 ± 5.40 # Reconstruct. Points (x1000) ↑ 84.3 ± 50.7 4”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1212

- Claim: 尺度配准方法：尽管 MDE 输出绝对深度，其不完美仍会造成单目重建的尺度差，而正确尺度是自动化与测量类应用的必要条件。作者用相机运动的机器人运动学数据克服尺度模糊并配准估计地图到手术场景：读取机械臂位姿并施加 eye-in-hand 标定获得机器人持镜位姿读数，用 Umeyama 算法把 SLAM（后 bundle adjustment）估计相机位姿的平移分量配准到机器人持镜位姿——两条独立获取的位姿链配准免除了前作所需的 fiducials，可即时缩放对齐分割 3D 地图到物理场景；该方法可通过光学跟踪器等手段推广到非机器人应用。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 6, Section 3.5 Registration and Scaling the Reconstruction
- Evidence: page 6 Section 3.5：MDE 不完美→尺度差动机；robot kinematics + eye-in-hand + Umeyama（平移分量）配准；免 fiducials；光学跟踪器推广路径。
- Quote: “Although we use an MDE model that outputs absolute depth estimation, imperfec- tions in this model can still cause scale differences in the monocular reconstruction. While these reconstructions are still useful as a 3D map, correct scale is required for applications such as automation and measurements. To overcome the scale ambigu- ity and register the estimated map onto the surgical scene, we use robot kinematics data of the camera motion. By reading the robot arm poses and applying an eye- in-”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1213

- Claim: 配准与尺度精度：Central Airway（中央气道）尺度比 98.17±3.49%、位姿 RMSE 0.67 mm；Prostate（前列腺）尺度比 98.23±5.88%、位姿 RMSE 1.12 mm——尺度估计误差约在 2% 以内，位姿配准残差为毫米级（摘要口径：平均位姿配准 RMSE 0.9 mm、估计尺度在真值 2% 以内）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 9, Table 2; Section 4.2 Registration Accuracy
- Evidence: page 9 Table 2：两解剖的 Scale Ratio 与 Pose RMSE；测量协议见 page 9 Section 4.2（机器人持镜位姿 vs 配准后估计位姿的 RMSE；5 对烧灼点 caliper 实测 vs 估计距离的尺度比）。
- Quote: “Table 2 Evaluation of registration and scaling accuracy. Scale Ratio (%) Pose RMSE (mm) Central Airway 98.17 ± 3.49 0.67 Prostate 98.23 ± 5.88 1.12”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1219

- Claim: 评估载体与金标准：CAO 用羊pluck+鸡胸制备模拟人类解剖的体模（切小鸡胸块造成气管约 50% 阻塞、经小切口置入并用超级胶固定）；BPH 用最初为手术训练开发的水凝胶体模（按患者 CT 扫描建模、反映人类解剖的视觉与材料特性）；用 Virtuoso Surgical 内窥镜系统在两类体模上录制单目视频；并对体模做 CT 扫描、手工分割解剖结构，作为感知管线评估的金标准几何。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 4, Section 3.1 Phantom Production and Data Collection
- Evidence: page 4 Section 3.1：羊pluck/鸡胸 CAO 体模（~50% 阻塞）、患者 CT 建模水凝胶 BPH 体模、Virtuoso Surgical 系统、CT 扫描+手工分割金标准。
- Quote: “For the CAO case, following our previous work [3], we prepare phantoms using sheep pluck and chicken breast to mimic human anatomy. We separate the trachea from the rest of the pluck for easier handling. We cut small pieces of chicken breast that cause around 50% occlusion in the trachea, place them inside the airway through small incisions, and secure them with super glue (Fig. 2b). For our BPH experiments, we use hydrogel phantoms developed originally for sur- gical training [19]. These phanto”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1220

- Claim: MDE 三阶段框架解决内窥镜缺乏 GT 深度：(1) 渲染数据生成——在 Unity 中用 CAO/BPH 扫描的 3D CT 分割产生绝对深度图；(2) 渲染与真实内窥镜数据间的无监督域适应——渲染图像被转换为真实内窥镜场景的视觉风格以缩小域间隙；(3) 深度预测——用第 (2) 步配对的转换渲染图像与深度图微调 DepthAnythingV2 模型，实现准确的深度估计；CAO 与 BPH 分别训练了独立模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 5, Section 3.2 Segmentation and Monocular Depth Estimation
- Evidence: page 5 Section 3.2 末段：MDE 三阶段（Unity 渲染绝对深度→无监督域适应→DepthAnythingV2 微调）；CAO/BPH 独立模型。
- Quote: “To address the lack of ground truth depth in endoscopic images, we use an MDE framework [24] that integrates 3D CT data and 2D endoscopic video data. Our MDE consists of three main stages: (1) Rendered data generation in Unity using 3D CT segmentations of CAO and BPH scans to produce absolute depth maps [25]; (2) Unsupervised domain adaptation [26] between rendered and real endoscopy data, where rendered images are translated into the visual style of real endoscopic scenes to reduce the domain g”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1233

- Claim: Omni-LIVO 的核心应用方式是紧耦合多相机 LiDAR-惯性-视觉里程计：以多视角观测全面利用大范围空间中的 LiDAR 几何信息，引入 Cross-View 直接对齐策略在非重叠视角间维持光度一致性，并以带多视角更新与自适应协方差的 ESIKF 完成状态估计——系统为 FAST-LIVO2 的多相机扩展。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 1, Abstract and Section I Introduction
- Evidence: 摘要陈述系统定位（tightly coupled multi-camera LIVO）、两项核心机制（Cross-View direct alignment；multi-view updates + adaptive covariance 的 ESIKF 扩展）与评测结论；引言明确系统 extends FAST-LIVO2 with multi-view photometric constraints。
- Quote: “We present Omni-LIVO, a tightly coupled multi-camera LIVO system that leverages multi-view observations to comprehensively utilize LiDAR geometric information across extended spatial regions. Omni-LIVO introduces a Cross-View direct alignment strategy that maintains photometric consistency across non- overlapping views, and extends the Error-State Iterated Kalman Filter (ESIKF) with multi-view updates and adaptive covariance.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1234

- Claim: 作者把多相机方案的动机锚定在单相机 LIVO 的结构性限制上：既有 LIVO 普遍依赖单相机，无法充分利用 LiDAR 导出深度做光度对齐与场景着色；多相机配置带来扩展空间覆盖、更丰富几何约束、更高可观测性以及遮挡/光照变化下的鲁棒性。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 1, Abstract and Section I Introduction
- Evidence: 摘要指出现有 LIVO 单相机限制；引言'Realizing these advantages'段列举多相机四项优势；该动机由后文相机数量消融与遮挡/光照场景结果验证。
- Quote: “Multi-camera configurations offer significant advantages for LIVO systems through extended spatial coverage, enabling comprehensive utilization of LiDAR-derived depth for pho- tometric alignment, richer geometric constraints, improved observability, and enhanced robustness under occlusion and illumination changes.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1235

- Claim: 非重叠环视多相机配置存在区别于立体相机的两类核心挑战：其一，patch 在相机间切换时光度连续性必须通过时间 patch 迁移维持；其二，各视角异构测量可靠性需要自适应协方差建模——这两项挑战分别对应本文两项贡献（Cross-View temporal migration、自适应多视角 ESIKF）的问题定义。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 1, Section I Introduction
- Evidence: 引言'Realizing these advantages requires addressing key technical challenges'段给出两类挑战及其解法对应关系；III-C 与 III-E 分别给出机制细节，消融实验分别验证。
- Quote: “Unlike stereo systems that use overlapping views for feature matching, non-overlapping multi-camera configurations require different approaches. First, photometric continuity must be maintained through temporal patch migra- tion as patches transition between cameras. Second, adaptive covariance modeling is needed to handle heterogeneous mea- surement reliability across different views”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1237

- Claim: Cross-View temporal migration 的核心机制：当地图点从相机 i 迁移到相机 j 时，参考 patch 动态切换——优先采用当前相机（j）的观测，或选择光度误差最小的 patch（式(5) 对点 p 全部观测集合 O(p) 最小化成对 patch 强度差）；迁移事件由迁移指示子 M(p,i→j)（式(4)：参考相机≠当前相机、点仅在新相机可见且跨帧迁移）判定，从而在非重叠相机交接处维持直接光度约束。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 2-3, Section III-C. Cross-View Direct Method
- Evidence: III-C 给出迁移指示子式(4) 与参考 patch 动态切换式(5)；图 3 示意点 p2 从前相机迁移到左相机，图 4 示意转弯时 intra-camera（绿）与迁移（红）patch 关联。
- Quote: “When camera migration occurs, the reference patch is dynamically switched by prioritizing observations from the current camera, or selecting the patch with minimum pho- tometric error:”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1238

- Claim: 跨相机光度一致性的工程代价清单：各相机图像需先经渐晕多项式归一化（式(6)-(7)，系数逐相机离线标定），曝光差异由逐相机逆曝光时间参数 τ_c 处理并在 ESIKF 框架中联合优化（雅可比扩展至 R^{m×(6+N_c)}，无需估计相机间相对曝光因子）；跨相机 patch warp 在局部平面假设下由相对变换诱导的单应 H_{i→j}(p)（式(8)-(9)）完成。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 3-4, Section III-C. Cross-View Direct Method
- Evidence: III-C 给出渐晕归一化、逐相机曝光参数联合优化与单应 warp 的完整公式链；III-E 说明雅可比扩展维度；双向耦合雅可比（式(12)）同时约束两相机几何与光度。
- Quote: “Exposure variations across cameras are handled through per- camera inverse exposure time parameters τ c jointly optimized in the ESIKF framework, ensuring photometric consistency without requiring relative exposure factor estimation.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1239

- Claim: 自适应协方差把多相机异构测量质量纳入滤波权重：光度协方差矩阵 R_img 依据实时光度误差自适应缩放（缩放因子由上一帧平均光度误差经线性映射与时间平滑得到，σ_min/σ_max=100.0/1000.0、e_max=100.0、平滑系数 λ=0.3），对高光度误差相机（如运动模糊、遮挡）降权、对可靠观测加权，从而在不利条件下提升鲁棒性。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 4-5, Section III-E. Iterative Multi-Camera State Estimation with ESIKF
- Evidence: III-E 给出式(17)-(18) 的协方差缩放与时间平滑公式及全部超参数；IV-E 讨论与 Lower Gallery 2 消融（C10）验证光照变化下的鲁棒性增益。
- Quote: “This adaptive weighting down-weights cameras with high photometric errors (e.g., motion blur, occlusion) and up-weights reliable observations, improving robustness in adverse conditions.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1240

- Claim: 总体量化效果：在 Hilti 2022/2023 与 Newer College 共 27 条序列上，Omni-LIVO 变体在 25/27 序列取得最低误差且全部完成评测；相对 FAST-LIVO2 全部 27 序列平均误差降低 30%，Lower Gallery 序列最高降低 82%（Table II：FAST-LIVO2 0.033→Ours 0.006 m）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 6, Section IV-B and Table II
- Evidence: IV-B 汇报 25/27、平均 30% 降幅与 82% 单序列最高降幅；Table II 给出 27 序列 × 10 配置的完整 ATE RMSE 矩阵；Lower Gallery 行 FAST-LIVO2 0.033、Ours 0.006 与 82% 陈述一致。
- Quote: “Omni-LIVO vari- ants achieve the lowest error in 25 out of 27 sequences and suc- cessfully complete all evaluated tracks, outperforming FAST- LIVO2, R 3 LIVE, FAST-LIO2, and OpenMAVIS across diverse environments including construction sites, indoor corridors, and underground scenarios. Compared to FAST-LIVO2, our system achieves an average 30% error reduction across all 27 sequences, with improvements up to 82% on Lower Gallery.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1241

- Claim: 消融量化 Cross-View temporal migration 的增益条件：大视点变化序列获益显著——Hilti 2022 Cupola 2 上完整系统 0.098 m vs 关闭迁移（w/o cvtm）0.146 m（降低 32.9%）；跨视角光度连续性在视点剧烈变化（如转弯）时是环视多相机系统的精度关键。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 6, Section IV-B and Table II
- Evidence: IV-B 消融分析给出 Cupola 2 的 cvtm 对比；Table II Cupola 2 行 Ours 0.098、w/o cvtm 0.146；图 4 示意转弯时 intra-camera（绿）与迁移（红）patch 关联。
- Quote: “Ablation analysis demonstrates that Cross-View Temporal Migration improves accuracy in sequences with large view- point changes (Cupola 2: 0.098 m vs. 0.146 m w/o cvtm), while Adaptive Covariance enhances robustness under illumination variations (Lower Gallery 2: 0.083 m vs. 0.109 m w/o ac).”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1242

- Claim: 消融量化自适应协方差的增益条件：光照变化场景获益显著——Hilti 2022 Lower Gallery 2 上完整系统 0.083 m vs 关闭自适应协方差（w/o ac）0.109 m（降低 23.9%）；误差驱动的协方差缩放在光照变化的画廊环境提供鲁棒性增益。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 6, Section IV-B and Table II
- Evidence: IV-B 消融分析给出 Lower Gallery 2 的 ac 对比；Table II Lower Gallery 2 行 Ours 0.083、w/o ac 0.109；IV-E 讨论复述该结论。
- Quote: “while Adaptive Covariance enhances robustness under illumination variations (Lower Gallery 2: 0.083 m vs. 0.109 m w/o ac).”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1243

- Claim: 相机数量消融显示 1-Cam→2-Cam→3-Cam 渐进增益且几何复杂场景增益最大：Newer College Underground hard 从 1-Cam 0.096 m 到 3-Cam（Ours）0.055 m（降低 42.7%）、Construction Upper 2 从 0.037 到 0.009 m；作者据此判断多相机融合在几何挑战场景提供更大收益。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 6, Section IV-B and Table II
- Evidence: IV-B 相机数量对比给出 Underground hard 0.096→0.055 与趋势判断；Table II 各序列 1-Cam/2-Cam/Ours 三列支持渐进增益模式。
- Quote: “Camera number comparison shows progressive gains from 1- Cam to 3-Cam (Ours), with the largest improvements in com- plex environments (Underground hard: 0.096 m to 0.055 m). This trend indicates that multi-camera fusion provides greater benefits in geometrically challenging scenarios.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1245

- Claim: 多相机配置带来稠密着色建图增益：Omni-LIVO 产生的 RGB 着色点数全面超过对比方法，复杂环境提升最显著——自定义 basement3 序列 33,513,608 vs FAST-LIVO2 9,519,125（3.5×）；stairs 14,184,500 vs 5,539,700、classroom 4,484,889 vs 3,111,504、corridor 8,715,790 vs 4,863,001。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 7-8, Section IV-D and Table IV
- Evidence: IV-D 定性结果引用 Table IV 着色点数统计；Table IV 给出 4 序列 × 4 方法的着色点数；图 7 展示 Cupola 2 与 Underground Hard 的多相机着色建图质量。
- Quote: “more RGB-colored points than competing methods, with par- ticularly significant improvements in complex environments (3.5× more than FAST-LIVO2 in basement3).”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1246

- Claim: 多视角约束提升可观测性与全局一致性：楼梯序列回环对比中 Omni-LIVO 起止点精确对齐而 FAST-LIVO2 出现可见漂移，作者将一致性改善归因于多视角约束增强的可观测性——在未集成在线回环闭合的条件下由里程计本身维持全局一致性。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 6-7, Section IV-D, Fig. 8
- Evidence: IV-D 定性结果（Fig. 8）给出回环起止对齐对比与可观测性归因；结论章 future work 确认当前无在线回环。
- Quote: “Fig. 8 validates the system’s ability to maintain global consistency and achieve precise loop closure, with Omni-LIVO showing superior align- ment compared to FAST-LIVO2’s visible drift. The improved consistency is attributed to enhanced observability from multi- view constraints.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1248

- Claim: 应用形态（传感 rig）：Omni-LIVO 自定义数据集采用 LIVOX MID360 LiDAR（360° 水平 FoV、10Hz）+ 四台 1024×768@10Hz 相机十字交叉（cross-pattern）布局，在手持与机器人两种平台上采集；各相机通道外部触发保证同时曝光——以'360° LiDAR + 多相机非重叠环视'组合实现全向感知。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 5, Section IV-A; page 2, Section III-B
- Evidence: IV-A 数据集描述给出 rig 配置与两种平台（Fig. 6）；III-B 式(3) 说明各相机通道外部触发确保同时曝光。
- Quote: “We additionally col- lected a custom dataset comprising multiple sequences using LIVOX MID360 LiDAR (360° horizontal FoV, 10Hz) and four cameras (1024×768, 10Hz) in cross-pattern configuration with handheld and robotic platforms (Fig. 6).”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1289

- Claim: Multi-LVI-SAM 的核心应用方式是把多台鱼眼相机的视觉特征统一投影到以全景模型中心为球心的归一化球面上，构成单一全景视觉特征模型：该模型作为全局几何优化框架整合多视角约束、支撑无缝回环与全局位姿优化，同时降低系统复杂度（避免逐相机冗余处理）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 1, Section I Introduction
- Evidence: 引言说明为避免独立融合每个鱼眼视角带来的显著计算开销，构建全景视觉特征模型统一多相机观测：各相机特征投影到归一化球面（球心即全景模型中心），模型作为全局几何优化框架整合多视角约束。
- Quote: “Visual features from each camera are projected onto a normalized sphere, where the center of the sphere is the center of the panoramic model. This model serves as a global geometric optimization framework that consolidates multi-view constraints, enabling seamless loop closure and global pose optimization while reducing system complexity.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1290

- Claim: 作者把多相机（鱼眼）方案的动机锚定在单目 LVIO 的窄视场上：既有 LVIO 系统多用单目相机，FoV 受限导致两类限制——快速视点变化时环境感知不足、无纹理或重复场景特征跟踪失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 1, Section I Introduction
- Evidence: 引言指出 VINS-Mono/OpenVINS、LIO-SAM/FAST-LIO2 各自受限于单传感器弱点后，明确单目 LVIO 的两类 FoV 限制；后文以 Stairs（低纹理楼梯）等实验验证该动机。
- Quote: “However, most existing LVIO systems utilize monocular cameras, which have limited FoV, leading to two major limitations: (1) inadequate environmental perception during rapid viewpoint”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1292

- Claim: 在无纹理与几何重复环境（Newer College Stairs）中多鱼眼配置获益显著：FAST-LIO2 因窄空间点云退化发散、FAST-LIVO2 因单目视场与特征提取能力限制无法在低纹理楼梯面获得足够视觉约束，两者均定位失效；本文通过多相机协同观测在几何重复、纹理稀缺的楼梯间维持稳定特征跟踪与位姿估计，Stairs RMSE 0.451100 m（w/ loop）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 5-6, Section IV-A and Table II
- Evidence: Section IV-A 给出 Stairs 场景失效机制归因与本文方法对比结论；Table II 给出 Stairs 序列各方法 RMSE（FAST-LIO2/FAST-LIVO2/LVI-SAM 均 fail，本文 w/loop 0.451100、w/o loop 0.701162、Ours-LIO 3.032322）。
- Quote: “In the challenging Stairs scenario, both FAST-LIO2 and FAST-LIVO2 experience localization failures: FAST-LIO2 diverges due to point cloud degradation in narrow spaces, while FAST-LIVO2 is limited by the field of view and feature extraction capability of a monocular camera, unable to obtain sufficient visual constraints on low-texture stair surfaces. In contrast, the proposed method, through the collaborative observation of the multi-camera system, maintains stable feature tracking and pose estim”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1295

- Claim: 在含动态物体的室内场景（M2DGR room-01/02）中多鱼眼配置获益：FAST-LIVO2、R2Live、LVI-SAM 均失效，本文分别取得 0.135218/0.127308 m RMSE；作者归因于动态物体破坏视觉特征连续性使单目/单相机系统难以维持帧间匹配、单目尺度不确定性导致误差持续累积发散，而多视角观测可滤除动态干扰特征并增强跟踪冗余。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 6, Section IV-B and Table III
- Evidence: Section IV-B 报告 M2DGR room-01/02 上 FAST-LIVO2 与 R2Live 轨迹大幅漂移、LVI-SAM fail，本文 w/loop 0.135218/0.127308 m；归因动态物体+单目尺度不确定性；多相机多视角观测滤除干扰特征。
- Quote: “the presence of dynamic objects (such as moving pedestri- ans) in the scene disrupts the continuity of visual features, making it difficult for monocular or single-camera systems to maintain stable inter-frame feature matching. Second, during prolonged operation, the inherent scale uncertainty of monocular systems leads to continuously accumulating errors, ultimately causing the entire system to diverge.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1297

- Claim: 外参补偿的量化效果：Newer College Stairs 序列因 LiDAR 点云特征退化而更依赖视觉特征三角化深度，补偿前精度因多相机中心与全景模型中心偏移而显著恶化，补偿后 RMSE 由 0.759511 降至 0.451100（降低 40.6%）；Hilti'2022 全部 4 序列补偿一致优于无补偿。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 6-7, Section IV-C and Table IV
- Evidence: Section IV-C 以 Stairs 为例说明补偿机制并给出 40.6% RMSE 降幅；Table IV 给出有/无补偿在 Newer College、M2DGR、Hilti'2022 各序列的完整对比，补偿侧全部占优。
- Quote: “Taking the Newer College Stairs sequence as an example, because the degradation of LiDAR point cloud features increases the need for accurate triangulation results of visual features to provide accurate depth, the accuracy significantly dete- riorates due to the offset between the multi-camera center and the panoramic model center. After implementing our compensation mechanism, the RMSE is reduced by 40.6%, fully validating the effectiveness of the proposed method.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1298

- Claim: 单鱼眼相机配置在复杂动态场景下完全失效而多相机融合恢复稳定：M2DGR walk-01（动态车辆、行人与密集植被挑战特征跟踪）中仅靠 mid-right 相机时里程计系统完全失效，四相机融合利用互补视角补偿单相机跟踪失败，显著增强整体鲁棒性（全配置 0.076371 m，四种单相机中 midright fail、其余 0.076557-0.076897 m）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 6-7, Section IV-C and Table IV
- Evidence: Section IV-C 消融显示 walk-01 序列 mid-right 单相机配置完全失效，多相机融合通过互补视角补偿个体相机跟踪失败；Table IV 该行给出四种单相机与全配置的 RMSE 对比。
- Quote: “in the M2DGR walk-01 test sequence (as shown in Figure 8), dynamic vehicles, moving pedestrians, and dense vegetation pose significant challenges to visual feature track- ing. When relying solely on the mid-right camera, the odom- etry system experiences complete failure.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1299

- Claim: Hilti'2022 消融证实无任何单相机配置通过全部测试、全配置+补偿全部完成且精度最优：Construction Upper Level 3 四种单相机全部 fail（全配置 w/补偿 0.165085 m）；Corridor Lower Gallery 2 单相机两台 fail、全配置 0.517772 m 优于所有单相机（0.839022-1.084816 m）；作者总结没有单相机成功通过全部测试，多相机融合在单相机缺乏特征信息时保证鲁棒性。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 6-7, Section IV-C and Table IV
- Evidence: Section IV-C 用 Hilti'2022（工地、画廊、地下室，含长走廊、楼梯、无纹理、光照不足、LiDAR 平面约束不足）做额外消融；Table IV 给出四种单相机/LIO/有无补偿全配置对比；作者明确 no single camera successfully passed all tests。
- Quote: “Construction Upper Level 3 fail fail fail 0.550198 fail 0.171185 0.165085 Basement 2 0.692945 0.178062 0.294170 0.242493 fail 0.187401 0.166250 Attic to Upper Gallery 2 0.892412 0.868133 1.094798 1.442255 3.918399 0.917128 0.655462 Corridor Lower Gallery 2 0.839022 0.977379 1.084816 fail fail 0.689255 0.517772”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-0465

- Claim: ActiveUMI 为每个 VR 控制器加装一枚腕装鱼眼相机，安装位置以最大化视野为目标，捕捉机器人即时操作环境的全面视觉信息；该腕视图作为头戴相机第一视角的补充进入下游策略。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 3, Section 3.1 Data Collection System for ActiveUMI
- Evidence: Section 3.1 夹爪驱动段说明为丰富数据流，每个控制器加装鱼眼相机；该腕装相机位置以最大化 FoV，为下游策略模型提供丰富视觉上下文，腕视图作为头戴第一视角的补充。
- Quote: “To enrich the data stream, we augment each controller with a fisheye camera. This wrist-mounted camera is po- sitioned to maximize its field of view, capturing compre- hensive visual information of the robot’s immediate oper- ational environment. This provides the downstream pol- icy model with rich visual context, and the resulting “wrist view” serves as a valuable complement to the first-person perspective from the head-mounted camera.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0467

- Claim: 真机部署设置：测试台由三台 6-DoF ARX R5 机械臂构成，两臂各配一枚鱼眼腕装相机构成双臂操作系统，第三臂提供主动移动视角、其相机源为人类操作者 VR 头显以模拟 egocentric 头相机；全部传感器与机器人数据以 30Hz 采集，策略用 π0 微调 50k iterations，默认每实验 10 trials。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 6, Section 4.1 Implementation Details and Task Descriptions
- Evidence: Section 4.1 说明实验平台（三台 ARX R5、两臂各配鱼眼腕装相机、第三臂主动视角源为操作者 VR 头显）、30Hz 采集、π0 微调 50k iterations 与 10 trials 协议。
- Quote: “Our real-world experiments are conducted on a testbed con- sisting of three 6-DoF ARX R5 robotic arms. Two arms, each equipped with a fisheye wrist-mounted camera, form a bimanual manipulation system. The third arm provides an active, mobile viewpoint, with its camera feed sourced from a human operator’s VR headset to simulate an egocentric head camera. All sensor and robot data is collected at a fre- quency of 30Hz.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0468

- Claim: 三相机配置受控对比（同 π0 基座，in-domain 五任务）：仅双鱼眼腕相机的 UMI 设置平均成功率 26%（bottle placing 60%、rope boxing 20%、shirt folding 10%、block disassembly 0%、take drink from bag 40%），加静态顶视头相机升至 42%，ActiveUMI 主动头视角达 70%（对应 90%/70%/80%/30%/80%）——腕鱼眼-only 是三种配置中最弱的。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 7, Table 1
- Evidence: Table 1 报告三配置在五个 in-domain 任务上的成功率与均值；表注明确 wrist-camera-only 配置对应 UMI 设置；正文指出主动感知在全部任务上显著优于两个对照，且固定顶视相机可靠优于腕-only，说明第三人称视角提供互补信息。
- Quote: “Table 1. We compare our active perception approach to two variants: a fixed top-down camera and a wrist-camera-only setup. The wrist- camera-only configuration corresponds to the UMI setting. Camera View Tasks (In-Domain) Bottle placing Rope boxing Shirt folding Block disassembly Take Drink from Bag Average UMI 60% 20% 10% 0% 40% 26% UMI w/ Fixed Head Camera 60% 40% 40% 20% 50% 42% ActiveUMI 90% 70% 80% 30% 80% 70%”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0470

- Claim: 作者报告：纯 ActiveUMI 数据训练的策略在全部任务上取得平均 70% 成功率，相对非主动感知对照（腕中心视角策略与静态第三人称相机策略）平均成功率分别提升 44% 与 38%；在新物体与新环境测试中保持 56% 平均成功率（摘要口径：70% in-distribution、56% 泛化保持）。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 2, Section 1 Introduction
- Evidence: 引言概述实验结论：纯 ActiveUMI 数据训练的策略平均 70% 成功率，相对腕中心视角与静态第三人称相机分别提升 44% 与 38%；新物体新环境保持 56%。
- Quote: “By training policies trained purely on ActiveUMI demonstrations, they attain an average 70% success rate on all tasks. Relative to non-active perception counterparts (i.e., policies trained from wrist-centric views or static third-person cameras), ActiveUMI improves aver- age success by 44% and 38%, respectively. Furthermore, when evaluated with novel objects and scenes, learned poli- cies retain 56% of the average success rate, indicating a meaningful generalization from in-wild data.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0471

- Claim: 数据混合实验（shirt folding，每实验 20 trials）：纯 ActiveUMI 数据成功率 80%，混入 10% 遥操作数据升至 90%，混入仅 1% 遥操作数据最优达 95%——大规模低成本 ActiveUMI 数据配合极少量真机遥操作数据即可显著提升策略。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 7, Table 3
- Evidence: Table 3 报告三种遥操作数据占比（10%/1%/0%）下的平均成功率（90%/95%/80%）；正文指出最优策略是混入仅 1% 遥操作数据，与'大规模数据+少量真实演示'的先前结论一致。
- Quote: “Table 3. Data Mixing Ratio Experiments. We conducted experi- ments on the shirt folding task to find the optimal data mixture for maximizing model performance. Teleoperated Data Ratio 10% 1% 0% Avg. Success Rate 90% 95% 80%”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0472

- Claim: 采集吞吐：对两个长程任务，ActiveUMI 采集耗时为直接人手演示的 1.49-2.06 倍（shirt folding 1.49×、rope boxing 2.06×），而常规真机遥操作为 2.63-3.27 倍（2.63×、3.27×）——ActiveUMI 是介于裸手效率与遥操作之间的实用折中。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 8, Section 4.5 Data Collection Throughput and Accuracy
- Evidence: Section 4.5 报告 rope boxing 与 shirt folding 两任务在三种采集方式下的耗时对比（Figure 6(d)）：ActiveUMI 分别为裸手的 2.06× 与 1.49×，遥操作为 3.27× 与 2.63×。
- Quote: “As shown in Figure 6(d), ActiveUMI significantly speeds up data collection compared to teleoperation. For the rope boxing task, ActiveUMI was 2.06x slower than a direct human demonstration, while conventional teleoper- ation was 3.27x slower. Similarly, for shirt folding, Ac- tiveUMI was 1.49x slower, compared to 2.63x for teleop- eration.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0473

- Claim: 采集精度：以卷尺标称距离（100cm 递减 10cm 至 10cm，十档十次）为真值测得的相对位姿误差（RPE），ActiveUMI 为 4.0mm，UMI 为 10.1mm——VR 控制器跟踪的数据精度约为 UMI 视觉管线的 2.5 倍。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 7, Figure 6(e)
- Evidence: Figure 6(e) 报告 RPE 对比：UMI 10.1mm、ActiveUMI 4.0mm；正文叙述两系统 RPE 相差 2.5 倍（原文表述存在笔误，图形数字为准）。
- Quote: “RPE(mm) UMI 10.1 ActiveUMI (Ours) 4.0 (e) Relative Pose Error (RPE) Comparison Rope boxing Shirt folding Rope boxing Rope boxing Shirt folding Figure 6. Data Collection Comparison. (a)-(d) We utilize efficiency comparison among ActivateUMI, bare hand, and teleoperation in two tasks: rope boxing and shirt folding.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0474

- Claim: 主动感知机制：系统显式记录操作者头戴显示器（HMD）的实时 6-DoF 位姿作为策略额外输入，使模型学习操作者头动（即视觉注意）与手部动作的关键关联；部署时策略为机器人头部预测 6-DoF 位姿，由低层控制器执行，使机器人能动态调整视角、克服遮挡。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 4, Section 3.2 Active Perception for Policy Learning
- Evidence: Section 3.2 说明 ActiveUMI 通过显式记录 HMD 6-DoF 位姿作为策略输入学习头动-动作关联；部署时策略预测头部 6-DoF 位姿并由低层控制器执行，实现动态视角调整与遮挡克服。
- Quote: “the real-time 6-DoF pose of the operator’s Head-Mounted Display (HMD) as an additional input to the policy. This allows the model to learn the crucial correlation between an operator’s head movements (i.e., their visual attention) and their corresponding hand actions.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0475

- Claim: 固定顶视头相机可靠地优于仅腕相机配置，表明第三人称视角为复杂双臂任务提供互补信息；作者将主动感知增益归因于两点：主动相机让策略把演示者的头/身运动补偿掉而非当作观测噪声，以及主动视角选择使策略按需获取任务关键信息（如确认抓取）。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 6, Section 4.2 How Important is the Egocentric Active Perception?
- Evidence: Section 4.2 末段给出两点解释与固定相机优于腕-only 的结论：演示者头/身运动在主动相机下可被补偿；主动视角选择按需获取任务关键信息；固定顶视相机可靠优于腕-only，说明第三人称视角提供互补信息。
- Quote: “We hypothesize two drivers of the improvements: (i) during in-the-wild data collection, demonstrators move their head and body; an active camera lets the policy com- pensate for this motion rather than treat it as observation noise; and (ii) active viewpoint selection enables the pol- icy to acquire task-critical information (e.g., verifying a grasp) on demand. Finally, the fixed top-down camera re- liably outperforms wrist-only, indicating that a third-person view adds complementary information”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0476

- Claim: 论文结论主张：主动感知数据管线显著优于缺乏主动感知的基线，证实'学习如何看与学习做什么同等重要'；腕装动作中心相机限制复杂、长程或遮挡任务性能是现有机器人学习系统的关键缺陷。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 8, Section 5 Conclusions
- Evidence: 结论指出当前数据采集方法忽视主动 egocentric 感知是关键缺陷，多数系统依赖动作中心的腕装相机限制复杂/长程/遮挡任务；实验证实主动视角控制高度有效（70% 成功率），learning how to look 与 learning what to do 同等重要。
- Quote: “In conclusion, we identified a critical limitation in current robot data collection methods: the neglect of active, egocen- tric perception. While humans naturally move their heads to understand and interact with the world, most robot learn- ing systems rely on action-centric, wrist-mounted cameras that limit performance on complex, long-horizon, or oc- cluded tasks.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0483

- Claim: FastUMI-100K 是 UMI 系大规模多模态演示数据集：包含 100K+ 演示轨迹，覆盖代表性家庭环境、54 类任务与数百种物体；多模态流包括末端状态、多视角腕装鱼眼图像与文本标注，每条轨迹 120-500 帧。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 1, Abstract
- Evidence: 摘要逐字给出 100K+ 轨迹、54 任务、数百物体、三类模态（end-effector states、multi-view wrist-mounted fisheye images、textual annotations）与 120-500 帧轨迹长度；正文补充折合 600 小时交互数据、5 个标准化环境（Introduction，page 1）。
- Quote: “Specifically, FastUMI-100K contains over 100K+ demonstration trajectories collected across representative household environ- ments, covering 54 tasks and hundreds of object types. Our dataset integrates multimodal streams, including end-effector states, multi-view wrist-mounted fisheye images and textual annotations.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0484

- Claim: FastUMI-100K 采集硬件延续 FastUMI 协议：轨迹跟踪由 RealSense T265 承担，高分辨率、广角鱼眼 RGB 图像由 GoPro 鱼眼相机采集——跟踪与视觉职能在硬件层分离，鱼眼相机仅承担视觉观察职能。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 3, Section III.A Hardware Design
- Evidence: Section III.A 首句给出 T265 tracking 与 GoPro fisheye cameras 的分工；同节后文给出双臂系统配置（两枚 T265+两枚 GoPro 鱼眼集成于两夹爪末端，20Hz 同步记录）。
- Quote: “Following the protocols established in FastUMI, we use the RealSense T265 for trajectory tracking, while high- resolution, wide-angle fisheye RGB images are captured using GoPro fisheye cameras.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0485

- Claim: 作者核心主张：在九个短程任务上用 FastUMI-100K 微调 π0-base 后，每种操作类型都取得高成功率，表明鱼眼视角与现有数据集中常用的常规 RGB 图像同样能捕捉物体空间状态与更丰富的上下文信息；该结论与 FastUMI 先行工作一致（末端安装的鱼眼镜头与多视角相机设置性能相当）。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 7, Section V.C Fine-tuning on VLA Large Models (Table III)
- Evidence: Section V.C 先陈述九个短程任务的实验设置，再给出'equally capable'主张与 FastUMI 结论对齐；Table III（page 7）报告各任务成功率：Open Drawer 80.00%、Open Roaster 86.67%、Open Container 73.33%、Rearrange Coke 93.33%、Unplug Charger 93.33%、Pick Bear/Lid/Cup 80.00/80.00/93.33%、Hotdog in Roaster 80.00%。
- Quote: “As shown in Table III, we first selected nine short-horizon tasks from different manipulation types for experimentation. Each type of task achieved a high success rate, indicating that the fisheye perspective is equally capable of capturing the spatial state of objects and richer contextual information as compared to the commonly used RGB images in existing datasets. This aligns with the findings in FastUMI, where fisheye lenses installed on the end-effector and multi-view camera setups demonstr”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0488

- Claim: 跨平台迁移设置：单任务 Diffusion Policy 模型迁移到两个品牌与结构均不同的机器人平台（Xarm6、Flexiv Rizon4）执行相同任务时，不对目标机器人做任何额外微调，仅调整末端坐标系的映射。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 7, Section V.B Cross-platform Deployment
- Evidence: Section V.B 描述跨本体评估实验设计：同一 DP 模型迁移至 Xarm6 与 Flexiv Rizon4，无额外微调、仅末端坐标系映射；Table I 双平台列给出迁移后成功率（如开微波炉门双平台同为 66.67%）。
- Quote: “During the transfer process, no additional fine-tuning is applied to the target robots, with only the coordinate system mapping of the end-effector being adjusted.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0490

- Claim: 采集效率：同一操作任务的采集耗时仅为遥操作式采集方法的 1/5；衣物折叠任务在 AgiBot（遥操作）中耗时 50 秒，FastUMI 仅 10 秒——手持直接操作的效率红利使 100K 级采集在人力上可行。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 5, Section IV.C Diversity of Task Horizon
- Evidence: Section IV.C 给出 1/5 总体倍率与衣物折叠案例（AgiBot 50s vs FastUMI 10s）；同节报告轨迹时长 6-25 秒（120-500 帧），并主张因消除动作延迟与冗余指令传输，信息密度高于遥操作数据。
- Quote: “For the same manipulation task, the time required for this scheme is only one-fifth of that using the teleoperation-based collection method. For example, the time spent on the clothes folding task in AgiBot [11] is 50 seconds, while FastUMI completes the same task in only 10 seconds.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0491

- Claim: 标注语言受鱼眼第一人称视角约束：因第一人称视角视频使用自中心（self-centered）坐标系，子任务级标注主要描述目标位置（如 move towards the cup）而非相对位置关系（如 move left towards the cup），以降低标注歧义——鱼眼第一人称特性从图像层级联到文本标注层，塑造了数据集的标注规范。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 4, Section III.D.1 Subtask-Level Annotation
- Evidence: Section III.D.1 说明子任务级标注的坐标系适配策略；同节末尾报告双层标注体系共提供 15,000 条文本标注（GPT-4o 预标注+人工分割交叉校验；运动级标注基于 RT-H 范式）。
- Quote: “Because the first-person perspective video uses a self- centered coordinate system, the subtask-level annotations primarily focus on describing the target position (e.g., move towards the cup) rather than relative position relation- ships (e.g., move left towards the cup) to reduce ambiguity in the annotations.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0492

- Claim: 多传感器时间对齐：最大对齐误差设为 GoPro 采样周期的一半（1/120 秒）；每个夹爪的视频帧均匀降采样至 20Hz 并与时间上最接近的 T265 位姿数据匹配；该方案最终实现双臂多传感器数据的亚毫秒级对齐精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 4, Section III.C Multi-Device Multi-Sensor Alignment
- Evidence: Section III.C（跨 page 3-4）描述对齐策略：ROS 统一时钟+近似时间同步器，四传感器（两 GoPro 60Hz+两 T265 200Hz，page 3），RGB 话题按时间戳近似同步、视频帧降采样 20Hz 匹配最近位姿，最终亚毫秒精度。
- Quote: “The maximum alignment error is set to half the GoPro sampling period (i.e., 1/120 seconds). Simultaneously, video frames from each gripper are uniformly downsampled to 20Hz and matched with the closest T265 pose data in time. This approach ultimately achieves sub-millisecond precision in the alignment of dual- arm multi-sensor data, providing a stable and synchronized dataset for downstream learning tasks.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0493

- Claim: 采集过程质量监控以鱼眼图像为主通道：GoPro 鱼眼图像与 T265 相机轨迹的实时可视化显示在计算机上，使操作者能监控丢帧与轨迹漂移等潜在问题——腕装鱼眼流兼任采集质量保障的人机接口，而不仅是策略训练数据。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 3, Section III.B.2 During Data Collection
- Evidence: Section III.B.2（During Data Collection）描述实时可视化监控；同节 III.B.3（Post-Data Collection）补充自动化过滤：通过计算相邻轨迹点间线速度与角速度识别可能导致 SLAM 漂移的操作异常，异常轨迹自动标记无效并删除。
- Quote: “In parallel, real-time visualization of the GoPro fisheye images and T265 camera trajectories is displayed on the computer, enabling the operator to monitor potential issues such as frame drops or trajectory drift during data collection.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0497

- Claim: UMI 系范式定位：Fast-UMI 通过把手持硬件与机器人末端解耦、保留腕部鱼眼视角（retaining the wrist fisheye view）、用 RealSense T265 直接记录 6-DoF 末端位姿，来提升采集吞吐与跨本体迁移，避免重型离线 SLAM 与固定动作捕捉设施。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 2, Section II.A Sensor-enhanced Interface Dataset
- Evidence: Related Work II.A 描述 Fast-UMI（同组先前工作，引文 [21]）的设计要点；II.B 把 UMI 系手持数据集的互补优势总结为保留部署腕视角、平滑低延迟末端状态与硬件解耦带来的复用潜力。
- Quote: “Building on this paradigm, Fast-UMI in- creases throughput and cross-embodiment transfer by decou- pling handheld hardware from robot end-effectors, retaining the wrist fisheye view, and directly logging 6-DoF end- effector poses with RealSense T265—avoiding heavy offline SLAM or fixed motion-capture infrastructure”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0041

- Claim: 在 PANDORA 全景目标检测上，不做旋转增强训练时，把 YOLOv11 的平面层替换为球面层可使模型对随机测试旋转鲁棒：球面模型 mAP@10 在无旋转测试与随机旋转测试下基本持平（29.54% vs 29.59%），而平面模型从 39.65% 崩塌至 12.71%（随机旋转条件下球面比平面高约 16.9 点 mAP@10）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 7, Table 3
- Evidence: 表 3 给出相同训练协议（无旋转增强）下 planar 与 spherical YOLOv11 的 NR/RR 测试结果：spherical 的 RR 测试 mAP@10（29.59%）与 NR 测试（29.54%）几乎一致，planar 则从 39.65% 掉到 12.71%，说明旋转鲁棒性来自架构等变偏置而非数据增强。
- Quote: “Planar YOLOv11[22] NR 39.65% 24.41% 12.71% 4.66% RR 27.76% 9.99% 28.01% 10.24% Spherical YOLOv11 NR 29.54% 11.41% 29.59% 7.90% Table 3.Object Detection Results on PANDORA Dataset.”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0043

- Claim: 在 Stanford 2D-3D-S 语义分割（仅 RGB 输入）上，无旋转增强训练的球面 DeepLab v3 对随机测试旋转鲁棒（mIoU 28.78%→28.09%，-0.7 点），而平面 DeepLab v3 从 35.01% 崩塌至 12.11%；随机旋转条件下球面模型比平面高约 16 点 mIoU。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 7, Table 4
- Evidence: 表 4 报告 NR 训练下 NR/RR 测试的 mIoU：planar DeepLab v3 从 35.01%（NR）崩塌到 12.11%（RR），spherical DeepLab v3 仅从 28.78% 到 28.09%；同一表格显示该模式对 UNet 与 YOLOv11 backbone 也成立。
- Quote: “Planar DeepLab v3[5] NR 35.01% 58.30% 12.11% 22.50% RR 32.29% 52.89% 38.30% 53.99% Planar UNet[26] NR 33.33% 55.48% 12.91% 23.40% RR 33.75% 51.13% 35.91% 51.52% Planar YOLOv11[22] NR 28.32% 48.09% 8.17% 16.43% RR 28.53% 44.39% 30.62% 45.13% Spherical DeepLab v3 NR 28.78% 45.27% 28.09% 41.18% RR 30.55% 44.58% 32.59% 45.38% Spherical UNet NR 25.72% 42.20% 22.99% 35.29% RR 25.07% 40.85% 27.83% 41.81% Spherical YOLOv11 NR 24.29% 40.59% 15.61% 28.08% RR 21.52% 38.88% 24.05% 38.98% Table 4.Semantic Se”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0537

- Claim: 环视鱼眼相机系统相对多针孔系统的三项结构性部署优势：重叠 FoV 提供物理级冗余（同一物体被多视角捕获以增强可靠性，不依赖算法级鲁棒性）；超广 FoV 适合空间受限或成本敏感的部署场景（室内机器人、监控）；同等覆盖下针孔系统通常需要更多相机（nuScenes 用六个、Tesla autopilot 用八个）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 1, Section Introduction, advantages paragraph
- Evidence: Introduction 逐字给出三项优势；同页还有监管预装优势（2018 美国 rear-view 法规使量产车已广泛预装、可直接复用免针孔系统改造费用），因该句被论文脚注块截断未纳入摘录，见 relation 与 note。
- Quote: “Second, com- pared to methods (Ge et al. 2023; Yan et al. 2023; Xie et al. 2025) that rely on algorithms to improve robustness against sensor failures, a surround-view fisheye system in- herently provides physical redundancy via overlapping FoV . As shown in Figure 1 (Right), this overlap captures the same object from multiple viewpoints to enhance reliability. Fi- nally, the ultra-wide FoV suits scenarios with constrained space or cost-sensitive deployment, such as indoor robotics or surveillan”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0540

- Claim: Fisheye3DOD 基准设计：CARLA 合成的 144 条驾驶序列（城市/郊区；白天正午/日落/夜间三种光照 × 晴/云/雨三种天气），每条以 10Hz 采集 50 秒共 500 帧时间对齐传感数据；同一场景同步配置六个环视针孔相机与四个 220° FoV 广角鱼眼相机，均附 3D 边界框标注——双成像模型同场景配对使针孔/鱼眼可直接公平比较。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 3, Section Fisheye3DOD Dataset, Data Collection
- Evidence: Data Collection 段另述 LiDAR/语义 LiDAR/自车轨迹同步采集；CARLA 无原生鱼眼传感器，畸变由 Kannala-Brandt 投影数学建模（见 C15）。
- Quote: “To address the existing gap in fisheye 3D object detection datasets, we developed Fisheye3DOD, a synthetic bench- mark created through the CARLA simulator (Dosovitskiy et al. 2017). This dataset comprises 144 driving sequences covering urban and suburban environments, spanning di- verse illumination conditions (daytime noon, sunset, night) and weather patterns (clear, cloudy, rainy). Each scenario contains temporally aligned sensor data captured at 10Hz over 50-second episodes, yielding a total”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0543

- Claim: RQ2 答案：在特征层端到端建模鱼眼几何（投影到球面等距柱面表示）优于图像级矫正——FisheyeBEVDet 与 FisheyePETR 的等距柱面版相对透视矫正基线 FDS 分别提升 4.5 与 6.2 点，相对柱面对应版再高 0.9 与 2.9 点；作者把优势归因于特征级建模保留更丰富的空间与语义信息，以及等距柱面更均匀的角度采样（特别是垂直方向）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 6, Section Experiments, RQ2
- Evidence: 摘要的 up to 6.2% 即 FisheyePETR 的这一增益；与 C06 表内数字一致（0.470−0.408=6.2 点、0.485−0.440=4.5 点）。
- Quote: “In particular, FisheyeBEVDet and FisheyePETR with equirectangular representation improve FDS by 4.5 and 6.2 points over the perspective-rectified baseline. This improvement stems from end-to-end mod- eling of fisheye geometry at the feature level, which pre- serves richer spatial and semantic information than image- level rectification. Moreover, they outperform their cylindri- cal counterparts by 0.9 and 2.9 points, respectively. This may be due to their more uniform angular sampling, particula”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0545

- Claim: RF1 传感器失效鲁棒性：多鱼眼系统依靠广泛 FoV 重叠天然缓解传感器失效——在前后相机均被移除的配置下，鱼眼方法的 FDS 降幅远小于针孔对应配置，因为针孔设置在这些极端条件下产生盲区，而多鱼眼设置保持全覆盖。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 6, Section Additional Analysis, RF1 and Table 3
- Evidence: Table 3 数字：BEVDet 4×P (w/o ↕) FDS 0.370/mAP 0.206 vs FisheyeBEVDet 2×F (↔) 0.431/0.315；PETR 4×P (w/o ↕) 0.321/0.142 vs FisheyePETR 2×F (↔) 0.382/0.244——两个鱼眼残缺配置均反超针孔残缺配置。
- Quote: “To validate this, Table 3 compares pin- hole and fisheye configurations both missing front and rear cameras: specifically, BEVDet with four pinhole cameras without front-rear sensors (4 × P (w/o ↕)) versus Fisheye- BEVDet with two fisheye cameras arranged left-right (2 × F (↔)). Similar comparisons are made for PETR variants. Results show that fisheye methods experience much smaller drops in FDS than pinhole counterparts when front and rear cameras are removed. This is because pinhole setups dev”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0546

- Claim: RF2 布局效应：前后（front-rear）传感器布局优于左右（left-right）布局——FDS 高 2-4%，因为交通参与者多聚集于车辆纵轴、减少径向畸变可更好保持目标形状，而左右布局把物体推向图像边缘、加剧像素压缩与检测难度；全环视（full surround）布局再比前后布局高 3-5%，取得最高精度，源于多相机协同（前后优化纵向覆盖，全环视以互补边缘细节缓解侧向畸变）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 6, Section Additional Analysis, RF2 and Table 3
- Evidence: Table 3 数字：FisheyeBEVDet 2×F (↕) 0.454 > 2×F (↔) 0.431 < 4×F 0.485；FisheyePETR 2×F (↕) 0.421 > (↔) 0.382 < 4×F 0.470。
- Quote: “RF2 (Sensor Layout Impact): Front-rear sensor lay- outs outperform lateral ones, with full surround achiev- ing the best results.To assess the effect of sensor placement in multi-fisheye systems, we compare three multi-fisheye layouts: front-rear, left-right, and full surround. As shown in Table 3, front-rear yields 2-4% higher FDS than left-right, since most traffic participants (e.g., cars, vans) cluster along the vehicle’s longitudinal axis, allowing better shape preser- vation by reducing ra”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0547

- Claim: RF3 近场对齐：鱼眼相机能力与近场感知对齐——鱼眼变体在 0-30m 段达到 0.586 FDS，与针孔系统 0-48m 段的 0.563 FDS 相当，而 0-30m 恰是覆盖 60km/h 车速下制动距离的关键范围；作者据此主张鱼眼相机特别适合低速场景：自动泊车系统、仓储机器人、人行道配送机器人。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 7, Section Additional Analysis, RF3 and Table 4
- Evidence: 同段引 F2BEV（16m）与 FisheyeBEVSeg（25m）为近场鱼眼先例；Table 4 另给同段对比（0-30m：针孔 0.673 vs 鱼眼 0.586，鱼眼同段仍低约 0.09 FDS）。
- Quote: “Our experiments in Table 4 validate this, showing fisheye variants achieve 0.586 FDS at 0-30m, comparable to pinhole systems’ 0.563 FDS at 0-48m — a critical range covering the under-30m braking distance at 60 km/h (Hosseinlou, Ahadi, and Hema- tian 2012). This capability makes fisheye cameras especially suitable for low-speed scenarios such as automated parking systems, warehouse robots, and sidewalk delivery robots.”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0549

- Claim: 定性观察：稀疏交通下鱼眼变体对正面远距目标（≈45m 范围）达到与针孔标准版距离等变（distance-equivariant）的检测性能；重度交通多车遮挡下所有检测器对远距目标退化、鱼眼变体降幅略大（密集遮挡放大像素压缩影响）；但在这些挑战条件下鱼眼变体仍保持与针孔模型相当的近场检测精度——作者据此定位其为近距感知的互补传感器。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 7, Section Qualitative Analysis and Fig. 5
- Evidence: Fig. 5 在 LiDAR 点云中可视化稀疏/密集两种交通密度下多检测器的预测对比（BEVDet/PETR/FisheyeBEVDet/FisheyePETR vs 真值）。
- Quote: “In the light traf- fic scenario, fisheye variants achieve distance-equivariant detection performance to their standard pinhole counter- parts for frontally distant objects (≈ 45m range), even with their inherent radial distortion and pixel compression. Under heavy traffic with multi-vehicle occlusion, all detectors ex- hibit performance degradation on distant objects, with fish- eye variants showing a slightly greater decline. This ob- served discrepancy may be due to the amplified impact of pix”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0550

- Claim: 方法路线：为公平回答 RQ2，作者放弃附加技巧（bells and whistles），以端到端『白板』（tabula rasa）方式在两大主流检测范式中原生引入鱼眼几何——BEV 型与 query 型两个方法均以球面坐标建模 3D 空间，并通过反向投影建立图像到空间的对应关系。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 4, Section Our Detector, Spherical Feature Representation
- Evidence: 后续段落给出实现：2D 特征经标定鱼眼投影函数可微扭转到等距柱面表示；FisheyeBEVDet 用同心球面壳层替代 LSS 平行平面分层、沿单位射线预测深度分布；FisheyePETR 用球面截锥点（二次递增深度间隔）做位置编码（page 4-5）。
- Quote: “To fairly answerRQ2, we forgo the “bells and whistles” but instead pursue an end-to-end “tabula rasa” approach to in- vestigate two distinct 3D detection paradigms: BEV-based and query-based. Both methods model 3D space in spherical coordinates and perform back-projection to establish image- to-space correspondence.”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0600

- Claim: OneOcc 的应用方式：以单全景环形镜头（PAL，鱼眼族）相机作为唯一视觉传感器，为足式/人形机器人做 360° 语义占据预测；选型理由是单全景相机提供紧凑的真实 360° 覆盖，但代价是引入环形畸变与展开后的接缝伪影——透视相机 SSC 管线无法直接处理，需要专用设计。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 1, Section 1 Introduction
- Evidence: 引言'Panoramic SSC with a single sensor'段说明单全景相机提供紧凑真实 360° 覆盖但引入环形畸变与展开接缝伪影，透视相机 SSC 管线处理不佳，因此需要保留原始全景线索同时利用网格友好投影的设计。
- Quote: “A single panoramic camera provides compact, true 360 ◦ coverage but intro- duces annular distortions and seam artifacts after unwrap- ping [36]—issues poorly handled by perspective-camera SSC pipelines. This motivates a design that preserves raw panoramic cues while exploiting grid-friendly projections.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0601

- Claim: 平台动机：直接迁移现有 SSC 到足式/人形平台不平凡——敏捷步态引起机身抖动、破坏证据与时间相干性；这类平台在杂乱不平地形需要全向 360° 态势感知；且紧的载荷/功耗预算偏好轻量、单传感器、低延迟方案——三个约束共同指向单全景相机方案。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 1, Section 1 Introduction
- Evidence: 引言'Why legged and humanoid platforms are different'段列举三重差异：步态抖动 corrupts evidence and breaks temporal coherence、需要 full 360° situational awareness in cluttered uneven terrain、tight payload/power budgets favor lightweight single-sensor low-latency solutions。
- Quote: “Di- rectly transferring SSC is non-trivial: agile gaits cause body jitter that corrupts evidence and breaks temporal coher- ence; these platforms require full 360 ◦ situational aware- ness in cluttered, uneven terrain; and tight payload/power budgets favor lightweight, single-sensor, low-latency solu- tions.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0602

- Claim: QuadOcc 基准定义：真实四足机器人第一人称 360° 数据集——PAL 全景相机与多帧 LiDAR 聚合+Grounded-SAM 初始化+定向人工修正的半自动 GT；10 场景 24K 帧，day/dusk/night 标准化覆盖，6 语义类训练，占据用 0.4m 体素在 64×64×8 网格（作者以'具身算力与低于汽车的速度'论证该分辨率）；采集端 Livox Mid-360 LiDAR（含 IMU）与 PAL 相机硬件触发+软件时间戳同步。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 2, Section 1 Benchmarks paragraph; page 22, Section 9.1
- Evidence: 引言 Benchmarks 段定义 QuadOcc 的规模（10 场景/24K 帧/6 类/0.4m 体素 64×64×8）、光照覆盖与半自动 GT 管线；补充材料 9.1 节给出传感器套件（Livox Mid-360+PAL，硬件触发同步）。
- Quote: “QuadOcc is a real first-person 360 ◦ dataset on a quadruped within a cam- pus domain, with standardized day/dusk/night coverage and semi-automatic ground truth (multi-frame LiDAR aggrega- tion, Grounded-SAM [37] initialization, targeted manual fixes). It contains 10 scenes and 24K frames, uses 6 se- mantic categories for training. The occupancy uses 0.4 m voxels on a 64 × 64 × 8 grid—reflecting embodied com- pute and lower speed than cars.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0603

- Claim: QuadOcc 主结果（作者重训全部基线）：OneOcc 以单全景相机输入达 20.56 mIoU，超过最佳 LiDAR 基线 LMSCNet（18.44）与最强视觉基线 MonoScene（19.19）；借助 LiDAR 的 SGN† 取得视觉组最高几何 IoU 49.16，但相机-only 的 OneOcc 仍是视觉组最佳 mIoU——作者结论：任务对齐的全景融合使相机-only 管线在该距离/分辨率下可与乃至超越流行 LiDAR 栈。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 7, Section 4.2 Quantitatively Comparisons (Table 2, page 5)
- Evidence: Section 4.2 报告 QuadOcc 验证集对比：OneOcc 20.56 mIoU 超 LMSCNet 18.44 与 MonoScene 19.19；SGN†（P+L）以 LiDAR 取得最高几何 IoU 但相机-only OneOcc 拿下视觉组最佳 mIoU；相关工作的动机句指出 LiDAR 栈对受限平台重且耗电。
- Quote: “OneOcc attains 20.56 mIoU, surpassing the best LiDAR baseline LMSC- Net (18.44) and the strongest vision baseline MonoScene (19.19). SGN † (P+L) achieves the highest geometry IoU (49.16) among vision entries by leveraging LiDAR, yet camera-only OneOcc delivers the best mIoU (20.56) among vision methods. Task-aligned panoramic fusion (DP-ER, BGV, AMoE-3D, with GDC on legged data) enables a camera-only pipeline to rival and even surpass popular Li- DAR stacks at this range/resolution.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0604

- Claim: H3O 泛化结果：同域（HOMO）OneOcc 37.29 mIoU（+3.83 vs MonoScene），跨城（HETER）32.23 mIoU（+8.08）；跨城分布偏移下优势更大——作者归因于 DP-ER 与 AMoE-3D 跨地图/光照/天气迁移、畸变感知先验缓解全景混叠，使相机-only mIoU 在分布偏移下达 SOTA（摘要口径：+3.83 within-city、+8.08 cross-city，up to +33.5% 相对）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 7, Section 4.2 (Table 3, page 6)
- Evidence: Section 4.2 报告 H3O 同域/跨城结果与更大跨城边际的解释；摘要与引言给出 +3.83/+8.08（up to +33.5% relative）口径。
- Quote: “On H3O-Homo OneOcc reaches 37.29 mIoU (+3.83 vs. MonoScene), while on H3O-Heter it attains 32.23 mIoU (+8.08). The larger margin under heterogeneous cross-city shifts highlights OneOcc’s strong distribution ro- bustness: DP-ER and AMoE-3D transfer across maps and lighting/weather, and their distortion-aware priors mitigate panoramic aliasing, yielding state-of-the-art camera-only mIoU under distribution shift.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0605

- Claim: FoV 价值量化（train-once、test-with-crops，H3O-Heter）：OneOcc 的 mIoU 随水平 FoV 近单调上升——90° 7.35、180° 17.27、270° 24.28、360° 32.23（90°→360° 总增 +24.88 mIoU、+77.2% 相对；MonoScene 总增 +19.50）；最后 270°→360° 增量 +7.95 大于 MonoScene 的 +5.95，作者称之为环向连续性补全时的非线性'闭环效应'——对基线的绝对优势也随 FoV 扩大（+2.70/+3.53/+6.08/+8.08）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 14, Section 6.2 Horizontal Field-of-View and Table 7
- Evidence: 补充材料 6.2 节以 360° 训练、评测时前向中心裁剪（不微调）的协议量化 FoV 缩放：OneOcc 各 FoV mIoU、总增 +24.88/+77.2%、闭环效应 +7.95 vs +5.95、绝对边际随 FoV 增大；并论证具身智能体需要绕自我中心的全向占据网格（原地转向/回退/身后侧向操作常见）。
- Quote: “For OneOcc, mIoU scales near-monotonically with FoV: +9.92 (90→180), +7.01 (180→270), and +7.95 (270→360), totaling +24.88 from 90 ◦ to 360 ◦ (+77.2% rel.). MonoScene also improves but less (+19.50 total). This indicates that surround cues translate into long-range context, with stronger returns when the azimuthal ring is closed.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0609

- Claim: 步态补偿消融（QuadOcc）：从 ER-only 单网格无 GDC 的 Q0 基线（19.19 mIoU）逐加模块——+GDC 19.58（+0.39）、+DP-ER 19.89（+0.31）、+BGV 20.30（+0.41）、+AMoE-3D 20.56（+0.26），增益可加；GDC 在特征提升前以零初始化头回归 2D 位移修正采样坐标，无需额外传感器（无 IMU/里程计），其作用是把步态冲击的相位误差在体素量化前路由回 2D 修正——针对足式平台抖动的全景相机专用机制。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 7, Section 4.3 and Table 4 (GDC design: page 5, Section 3.5)
- Evidence: Section 4.3 报告四模块逐加消融与增益解释（GDC stabilizes sampling、DP-ER complementary cues、BGV reduces discretization bias、AMoE-3D sharpens edges/contacts）；Section 3.5 定义 GDC 为提升前的 2D 位移回归（零初始化、即插即用、无额外传感器）。
- Quote: “Start- ing from Q0 (ER-only, no GDC, single-grid, no AMoE-3D; 19.19 mIoU), we add: +GDC → 19.58 (+0.39), +DP-ER → 19.89 (+0.31), +BGV → 20.30 (+0.41), +AMoE-3D (full) → 20.56 (+0.26). Gains are additive: GDC stabi- lizes sampling; DP-ER provides complementary cues; BGV reduces discretization bias; AMoE-3D sharpens edges/con- tacts without over-smoothing flats.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0610

- Claim: 端侧可部署性（Jetson AGX Orin 64GB 实测，QuadOcc 全景输入 1×3×370×1220，2D 编解码 INT8 TensorRT + 几何模块 FP16）：OneOcc 总时延 73.32 ms（13.64 FPS），MonoScene 98.01 ms（10.20 FPS），端侧整体加速约 1.34×——增益主要来自更轻的 2D 分支（53.86 vs 61.97 ms）与 3D 解码器（14.57 vs 33.58 ms），额外的笛卡尔→极坐标重采样仅 2.40 ms；桌面侧 RTX 4090 FP32 69.93 ms（14.30 FPS）、101.76M 参数、1.82GB 峰值（FP16 52.84 ms/18.92 FPS/1.49GB）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 21, Section 8.3 and Table 15 (page 22); page 8, Section 4.5
- Evidence: 补充材料 8.3 节在 Jetson AGX Orin 64GB（MAX 功耗模式）上以 INT8 TensorRT（2D）+FP16（几何模块）实测分阶段时延（5 次预热+100 次平均）；主文 4.5 节给出 RTX 4090 指标。
- Quote: “OneOcc achieves a total latency of 73.32 ms (13.64 FPS), compared with 98.01 ms (10.20 FPS) for MonoScene [50], corresponding to an overall speedup of approximately 1.34× on the embedded plat- form. Notably, this gain is achieved despite the additional Cart2Polar Samp. stage, which is absent in MonoScene.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0614

- Claim: 距离分箱安全分析：把非空体素限制在以智能体为中心的三个嵌套范围（Far ±12.8m/Mid ±6.4m/Near ±3.2m）后，OneOcc 对 MonoScene 的 mIoU 增益在所有距离箱均为正且近场仍保持——QuadOcc：Far 19.19→20.56、Mid 23.32→24.47、Near 24.29→24.95（+0.66）；H3O-Heter：Far 24.15→32.23、Mid 30.17→37.11、Near 30.69→37.35（+6.66）——增益并非只来自远场连续性或全景伪影抑制，在与短时避障、落脚点选择和局部可通行性最相关的近场同样成立。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 40, Section 12.3 Range-wise Safety Analysis and Figure 18
- Evidence: 补充材料 12.3 节报告距离分箱 mIoU 对比（Figure 18）：两基准三个距离箱全部为正增益，且从 Far 到 Near 两方法均改善（更小范围的长程歧义/遮挡更少、证据更密）。
- Quote: “On QuadOcc, the mIoU improves from 19.19 to 20.56 in the Far range, from 23.32 to 24.47 in the Mid range, and from 24.29 to 24.95 in the Near range. On H3O-Heter, the corresponding gains are larger: 24.15 → 32.23 (Far), 30.17 → 37.11 (Mid), and 30.69 → 37.35 (Near).”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0762

- Claim: OmniTrack++ 论文主张：对四足机器人与双足轮腿机器人等小型移动平台，全景（360°）成像提供了一种紧凑而有效的全场景态势感知手段，无需多传感器即可实现，从而降低负载。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 1, Section 1 Introduction
- Evidence: 作者在引言中明确将全景成像定位为小型具身平台的传感器选型优势：紧凑、全场景覆盖、减少多传感器负载。
- Quote: “In particular, for small-scale mobile platforms such as quadrupedal robots and bipedal wheel-legged robots, panoramic imaging offers a compact yet effective means to achieve full-scene situational awareness without the need for multiple sensors, thus reduc- ing payload”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0763

- Claim: 现有主要面向针孔相机的 MOT 算法难以泛化到全景设置，根源是图像展开为等距柱状格式后的分辨率退化、几何畸变与非均匀光照；论文引用先前工作称这些因素可导致 IDSW 增加高达 40%。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 2, Section 1 Introduction
- Evidence: 作者以引用文献（Shen and Yang 2024）支撑全景设置下 IDSW 最高增加 40% 的量化冲击；针孔 MOT 泛化失败由作者陈述，40% 数字本身依赖被引工作。
- Quote: “Ex- isting MOT algorithms Chen et al (2024b); Lv et al (2024), primarily designed for pinhole camera inputs, often fail to generalize well to panoramic settings due to intrinsic chal- lenges, e.g., , resolution degradation, geometric distortions, and non-uniform illumination when the images are unfolded into an equirectangular format Lin et al (2025). These fac- tors frequently lead to degraded performance—for instance, causing up to a 40% increase in IDSWs Shen and Yang (2024)—thus constraining”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0764

- Claim: 在四足机器人 PAL 全景数据 QuadTrack 测试集上，OmniTrack++ E2E 变体取得 34.90 HOTA 与 41.21 IDF1，较前作 OmniTrack E2E（19.87 HOTA / 19.47 IDF1）分别提升 +15.03 HOTA 与 +11.74 IDF1；TBD 变体达 36.08 HOTA / 42.76 IDF1。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 14, Section 5.2.1 + Table 3
- Evidence: QuadTrack 上对前作的绝对提升量级（+15 HOTA）远大于 JRDB 上（+3.94），说明具身运动扰动场景下专门组件收益更大。
- Quote: “On QuadTrack, OmniTrack++ E2E attains a HOTA of 34.90, yielding an absolute improvement of +15.03 points (from 19.87 to 34.90) compared to the orig- inal OmniTrack, while OmniTrack++ DA further elevates the score to 36.08.”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0765

- Claim: 在 JRDB 测试集（轮式平台多镜头拼接全景）上，OmniTrack++ E2E 达 25.50 HOTA / 28.00 IDF1，较 OmniTrack E2E（21.56/22.87）提升 +3.94 HOTA / +5.13 IDF1；TBD 变体 27.03 HOTA 与 0.81 OSPA 为该表最佳。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 14, Section 5.2.2 + Table 4
- Evidence: JRDB 上 E2E 增益（+3.94）仅为 QuadTrack（+15.03）的四分之一，暗示运动扰动强度影响专门设计的边际收益。
- Quote: “Notably, OmniTrack++ E2E demonstrates substantial improvements over the original OmniTrack E2E , achieving a HOTA score of 25.50 and an IDF1 of 28.00, representing absolute improvements of +3.94 and +5.13 points, respectively.”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0767

- Claim: EmboTrack 基准由两种具身平台的全景成像构成：QuadTrack 用四足机器人搭载 PAL 全景环形镜头（360°×70° FoV、2048×2048 分辨率、最高 40.5 FPS），BipTrack 用轮腿机器人搭载 Insta360 全景相机（双鱼眼拼接、最高 3840×1920、100 FPS、约 170° 单镜头 FoV）；合计 44 序列、26,400+ 标注帧、600+ 轨迹，跨两城市五校区采集。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 11, Sections 4.1-4.2
- Evidence: 数据集硬件规格完整覆盖两类宽 FoV 成像模态（PAL vs 双鱼眼拼接）与两类具身本体（四足 vs 轮腿），为综述硬件维度提供直接参照。
- Quote: “The PAL camera provides a 360 ◦ ×70 ◦ panoramic FoV at 2048×2048 resolution and up to 40.5 FPS, ensuring wide- area scene coverage. Mounted at the top of the quadruped, the camera delivers an unobstructed perspective, enabling panoramic data acquisition in unconstrained outdoor envi- ronments. The dataset spans multiple times of day—from morning to evening—across five campuses in the cities of Changsha and Hangzhou”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0768

- Claim: JRDB 验证集 5-epoch 组件消融显示：DynamicSSM Block（隐式畸变/光度校准）单独带来 +1.04 HOTA（27.30→28.34）与 +1.10 IDF1，是单独贡献最大的组件；与 ExpertTrack Memory 组合达 28.47 HOTA（+1.17）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 15, Table 7 + Section 5.3.1
- Evidence: 消融表显示畸变校准组件（DSSM）贡献约为长期记忆组件（ETM +0.31）的 3 倍以上，指向畸变本身是全景 MOT 的主要瓶颈。
- Quote: “Exp. DSSM ETM HOTA↑ IDF1↑ OSPA↓ MOTA↑ 1 - - 27.30 31.19 0.8958 27.34 2 ✓ 27.61 31.21 0.8610 11.99 3 ✓ 28.34 32.29 0.8786 29.86 4 ✓ ✓ 28.47 32.68 0.8552 22.20”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0775

- Claim: EmboTrack 的设计意图是捕捉具身平台特有的运动扰动：四足平台的周期性步态导致俯仰/横滚波动、垂直体振荡与速度突变，轮腿平台的复合运动引入俯仰波动、横向倾斜与间歇步态扰动；论文以图像平面归一化 Y 轴位移曲线（Fig. 7）显示 JRDB 轮式平台位移平滑、QuadTrack/BipTrack 振荡明显——平台运动扰动被作为基准的核心难度来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 10, Section 4 EmboTrack
- Evidence: 该基准首次把步态/轮腿运动扰动作为全景 MOT 的系统性变量（Table 1 显示既有 360° 基准均为轮式平台），界定了具身全景感知区别于自动驾驶的评测条件。
- Quote: “(i) BipTrack: Recorded with a wheeled-legged robot equipped with an Insta360 panoramic camera (Fig. 6 (a)), it introduces hybrid loco- motion dynamics. This platform combines wheel-based mo- bility with articulated leg joints, producing distinctive motion characteristics such as pitch variations, lateral tilting, and oc- casional gait-like steps. These motions induce complex scene deformations and non-uniform perspective transitions, com- plicating object detection and association. (ii) QuadTrac”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0776

- Claim: JRDB 验证集 E2E 对比中，OmniTrack++ 以 70.05M 参数（前作 63.13M，约 +11% 增量）取得 30.84 HOTA / 35.66 IDF1（前作 25.12/27.42，+5.72/+8.24），超过参数量 50.36M 的 MeMOTR（29.51/33.64）与 TrackFormer、MOTR、MOTRv2。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 15, Table 6 + Section 5.2.4
- Evidence: 约 7M 参数的 MoE 记忆与畸变模块增量换来 JRDB 验证集上 +5.72 HOTA，同时压过更强的通用 E2E 基线。
- Quote: “MeMOTR Gao and Wang (2023) 50.36M 29.51 33.64 0.891 OmniTrack E2E (ours) 63.13M 25.12 27.42 0.925 OmniTrack++ E2E (ours) 70.05M 30.84 35.66 0.879”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-1191

- Claim: 路线主张与任务定义：作者主张"机器人操控世界之前必须先掌握感知动作"，与其移动整个机身，更优雅高效的方案是移动"眼睛"；据此定义语言引导主动视觉感知任务——给定 PTZ 相机拍的单张 RGB 图像与自然语言指令，预测 pan(Δθ1)/tilt(Δθ2)/zoom(Δz) 三值，重定位并重缩放视场使任务相关细节居中放大；与操控不同，该动作空间直接控制观测过程、作用于真实 PTZ 执行器。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 2, I Introduction
- Evidence: page 2 Introduction：move the "eyes" 主张 + 任务形式化（三元组定义、reposition and rescale the field of view、directly controls the observation process on real PTZ actuators）。
- Quote: “In contrast, we argue that before a robot can manipulate the world, it must first master perceptual action. Instead of moving the entire robot body, a more elegant and efficient solution is to move the “eyes.” To this end, we define the task of language-guided active visual perception: given a single RGB image captured by a PTZ (pan-tilt- zoom) camera and a natural language instruction describing the information need (e.g., “What is the brand of the pen?”), the system must predict three values—p”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1192

- Claim: EyeVLA 系统构成与推理形态：硬件平台 Robotic EyeBall（REB）= 两轴 pan-tilt 云台 + 变焦相机；算法管线适配 Qwen2.5-VL（7B）做感知与相机控制联合建模。推理时接收初始宽视场（wide-field）图像+指令，预测紧凑动作三元组，单次前向（single forward pass）驱动物理执行器获取放大后的任务相关视图，无需迭代搜索或人工干预。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 3, III-A Overall Approach
- Evidence: page 3 Section 3.1 Overall Approach：系统构成（REB 硬件+Qwen2.5-VL 7B 适配）与推理流程（单次前向、无迭代搜索）。
- Quote: “The system consists of a hardware platform, the Robotic EyeBall (REB) comprising a two-axis pan-tilt mount and a zoomable camera, and an algorithmic pipeline that adapts Qwen2.5-VL (7B) for joint perception and camera control (see Figure 2). At inference time, the system receives an initial wide-field image together with a natural language instruction, predicts a compact action triplet a, and drives the physical actuators to acquire a zoomed-in, task- relevant view in a single forward pass, with”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1193

- Claim: 层级动作编码的 token 效率：设计三优势（每位内 token 数理论最优；常数时间编解码；高位对应粗调、低位对应细调的物理结构对齐）；500 真实样本经验分析显示 98.6% 的动作幅度落在 ±29° 内、最多两档十进制位即可表示，平均 token 长度 2.3，显著优于逐度均匀离散化（平均 12.7）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 4, III-B Hierarchical Action Encoding
- Evidence: page 4 Section 3.2 末段：三优势列表 + 经验统计（98.6% within ±29°、average token length 2.3 vs uniform discretization 12.7）。
- Quote: “This design offers three key advantages: (1) theoretical optimality in token usage within each digit; (2) constant-time encoding and decoding; and (3) structural alignment with physical camera control, where higher digits correspond to coarse adjustments and lower digits to fine tuning. Empirical analysis on 500 real-world samples shows that 98.6% of actions fall within ±29 ◦ , requiring at most two digit levels and achieving an average token length of 2.3, which is significantly more efficient”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1195

- Claim: 数据效率设定：自建机器人眼系统共采集 500 条真实演示样本（跨物体类别与室内环境），切分为 450 训练 + 50 held-out 测试、无场景重叠；另补 5 万条来自 Rexverse-2M grounding 数据集的伪标签合成样本扩充训练数据——且合成数据仅用于 SFT 预训练阶段，RL 后训练只在 450 条真实演示上进行（任务完成奖励修正残余偏差、提升真机鲁棒性）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 6, IV-A Dataset
- Evidence: page 6 Section 4.1 Dataset：500/450/50 切分、no scene overlap、50,000 pseudo-labeled from Rexverse-2M、synthetic 仅 SFT / RL 仅 450 真实演示的阶段隔离。
- Quote: “We have developed a robotic eye system comprising a two-axis pan-tilt mount and a zoomable camera. We collected a total of 500 real-world demonstration samples spanning diverse object categories and indoor environments. These are split into a training set of 450 scenes and a held-out test set of 50 scenes, with no scene overlap between splits. Each sample represents a complete task instance paired with a natural language instruction, recorded under varied spatial configurations and viewing condi”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1196

- Claim: 主结果：EyeVLA(RL3) 在三个动作维度全部取得最低 MAE（θ1: 2.04°、θ2: 1.68°、Zoom: 65.37）与最高平均任务完成率 96%，大幅超过 ML 基线（CR 36%）与全部 SFT-only 变体；且 SFT1 已在 θ2 与 Zoom 的 MAE 上超过 ML 基线，显示 VLM 底座的泛化能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 7, Table 1; IV-B Main Results
- Evidence: page 7 Table 1 及 4.2 正文：RL3 三维度最低 MAE + 96% CR；ML 基线 36%；SFT1 已超 ML（θ2/Zoom MAE）。
- Quote: “As shown in Table 1, EyeVLA (RL3) achieves the lowest MAE across all three action dimensions (𝜃 1 : 2.04°, 𝜃 2 : 1.68°, Zoom: 65.37) and the highest average task completion rate (96%), substantially outperforming both the ML baseline (CR: 36%) and the SFT-only variants.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1197

- Claim: 现成 VLM 基线对照：直接提示 Qwen2.5-VL 预测 PTZ 动作（无 grounding）仅 12% CR——表明现成 VLM 缺乏物理相机控制推理能力；加 grounding+硬编码几何映射升到 70%，但仍显著低于端到端学习的 EyeVLA（96%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 7, Table 2; IV-B Main Results
- Evidence: page 7 Table 2 及正文：Direct 12%、Grounding 70%（θ1 3.87/θ2 2.34/Zoom 109.46）、EyeVLA(RL3) 96%。
- Quote: “Directly prompting the VLM to predict PTZ actions without any grounding yields only 12% CR, indicating that off- the-shelf VLMs lack the ability to reason about physical camera control. When augmented with grounding followed by a hard- coded geometric mapping, the completion rate rises to 70%, but still falls significantly short of EyeVLA (96%), demonstrating the advantage of our end-to-end learned approach.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1199

- Claim: IoU 过滤消融：去掉 IoU 过滤（SFT2(N) vs SFT2(Y)）导致全部指标急剧退化——θ1 MAE 从 3.97° 升至 4.91°、CR 从 72% 跌至 56%（SFT3 阶段同型），表明未过滤的低质量伪标签引入噪声损害训练；IoU 是伪标签质量的有效代理指标，滤掉低空间对齐样本是迭代精炼成功的关键。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 8, IV-D Ablation Study; page 7, Table 1
- Evidence: page 8 Section 4.4 IoU-Controlled Data Filtering：SFT2(Y)→SFT2(N) θ1 3.97°→4.91°、CR 72%→56%；Table 1 同口径。
- Quote: “As reported in Table 1, removing IoU filtering (SFT2(N) vs. SFT2(Y)) leads to a sharp degradation across all metrics: 𝜃 1 MAE rises from 3.97° to 4.91° and CR drops from 72% to 56%, indicating that low- quality pseudo-labels without IoU filtering introduce noise that harms training.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1200

- Claim: RL 消融：尽管 SFT3 已有竞争力 MAE，RL3 进一步把 θ1 误差从 2.94° 降至 2.04°、平均 CR 从 92% 提至 96%；RL 在两个阶段一致提升预测 bbox 的平均 IoU（SFT2→RL2：0.68→0.75；SFT3→RL3：0.91→0.93）。作者假设：SFT 令模型过拟合伪标签分布、动作预测偶尔塌缩到窄区间，RL 用真机奖励惩罚系统性偏差、产生更多样且物理落地的动作输出（zoom 轴尤为明显）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 8, IV-D Ablation Study; page 9, Table 3
- Evidence: page 8 Section 4.4 Reinforcement Learning + page 9 Table 3（SFT2/RL2/SFT3/RL3 平均 IoU 0.68/0.75/0.91/0.93）。
- Quote: “Despite SFT3 already achieving competitive MAE scores, RL3 further re- duces 𝜃 1 error from 2.94° to 2.04° and improves the average CR from 92% to 96%. As shown in Table 3, RL consistently improves the mean IoU of predicted bounding boxes at both stages (SFT2→RL2: 0.68→0.75; SFT3→RL3: 0.91→0.93).”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1202

- Claim: ML 基线的"不公平优势"仍失败：随机森林基线以 GT bbox 作为输入特征（EyeVLA 不可得的优势）仍只达 36% CR——凸显学习式方法的必要性，即从 bbox 几何特征到相机动作的浅层映射不足以完成该任务。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 7-8, IV-B Main Results; Figure 6
- Evidence: page 7-8 Section 4.2 与 Figure 6 标题：RF baseline provided with GT bounding boxes as input features（advantage not available to EyeVLA）yet only 36% CR。
- Quote: “We note that the ML 7 ## page 8 Figure 6: The fitting performance of the Random Forest baseline is provided with ground-truth bounding boxes as input features (an advantage not available to EyeVLA), yet it still achieves only 36% CR, highlighting the necessity of our learned approach.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1251

- Claim: 360DVO 的应用方式定位：第一个基于深度学习的单目全景视觉里程计框架，用抗畸变球面特征提取器 DAS-Feat 从 360° 图像学习抗畸变特征，再以稀疏特征 patch 建立全景可微捆绑调整 ODBA 的位姿估计约束。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 1, Abstract and I. Introduction
- Evidence: 摘要与贡献列表声明'first deep learning-based OVO framework'与 DAS-Feat/ODBA 两模块划分；引言与 III 节展开两模块设计。
- Quote: “we present 360DVO, the first deep learning-based OVO framework. Our approach introduces a distortion-aware spherical feature ex- tractor (DAS-Feat) that adaptively learns distortion-resistant features from 360-degree images.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1252

- Claim: 全景相机的任务动机：单目 OVO 系统用 360° 相机克服透视 VO 的 FoV 限制；但既有方法依赖手工特征或光度目标，在剧烈运动与光照变化等挑战场景缺乏鲁棒性——本文以此为问题定义。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 1, Abstract
- Evidence: 摘要开头两句话完整给出动机与缺口；引言进一步列举光照变化、低帧率、运动模糊等现实挑战。
- Quote: “Monocular omnidirectional visual odometry (OVO) systems leverage 360-degree cameras to overcome field-of-view limitations of perspective VO systems. However, existing methods, reliant on handcrafted features or photometric objectives, often lack robustness in challenging scenarios, such as aggressive motion and varying illumination.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1254

- Claim: DAS-Feat 的核心设计 SphereResNet：球面卷积模块把全景图像逆投影到单位球，7×7 球面卷积核在球切平面采样像素再投回全景图像，配合两对 32/64 维残差块；由此获得抗畸变特征，patch 可不经 warp 直接从特征图裁切。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 3, Section III-A
- Evidence: III-A 节逐句描述 SphereResNet 结构与 7×7 核采样机制；残差块作用（缓解梯度消失）与消融 #2（SphereNet 无残差训练崩溃）互证。
- Quote: “Each input I i is fed into the spherical convolution module that inversely projects the omnidirectional image onto a unit sphere. A 7 × 7 spherical convolution kernel samples pixels on the sphere’s tangent plane and then projects those samples back onto the omnidirectional image.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1255

- Claim: ODBA 全景可微捆绑调整：以球面重投影约束联合优化相机位姿与 3D 点深度，最小化预测 patch 与重投影 patch 的坐标误差，Gauss-Newton 求解、Schur 补分块更新位姿与深度，不依赖外部初始化。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 3, Section III-B
- Evidence: III-B 节给出完整优化链路（式(6)-(10)）；相关工作节对比 SC-OmniGS（需 SfM/VO 前端初始化）强调本文无需外部初始化。
- Quote: “ODBA jointly optimizes camera poses and 3D point depths by minimizing the coordinate error between the predicted and reprojected patches.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1256

- Claim: 新真实世界 OVO 基准：20 条序列（平均约 1k 帧）按轨迹复杂度与环境动态分为 Easy/Hard 各 10 条；伪真值用 Agisoft Metashape 生成——在 TartanAirV2 上验证 Metashape 轨迹 ATE-RMSE 仅 0.027（接近真值），而 COLMAP 达 2.535，故选 Metashape。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 4, Section IV
- Evidence: IV 节给出数据来源三分（360VOTS 3 条/互联网 15 条/香港电车 2 条）、Easy/Hard 划分标准与伪真值工具选型验证实验。
- Quote: “The results show that Agisoft Metashape consistently produces trajectories with negligible ATE-RMSE (i.e., 0.027), which closely matches the provided ground truth, whereas COLMAP yields larger errors and drift (i.e., 2.535).”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1257

- Claim: 总体效果声明：在自建真实基准与公开合成数据集（TartanAirV2、360VO）上，360DVO 超越 SOTA 基线（含 360VO 与 OpenVSLAM），鲁棒性提升 50%、精度提升 37.5%。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 1, Abstract
- Evidence: 摘要总结性声明；正文 V-B 各表给出分项支撑（成功率 100% vs 43-92%；ATE 降幅见 C08-C10、C18 卡）。
- Quote: “Extensive experiments on this benchmark and public synthetic datasets (TartanAir V2 and 360VO) demonstrate that 360DVO surpasses state-of-the-art baselines (including 360VO and OpenVSLAM), improving robustness by 50% and accuracy by 37.5%.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1258

- Claim: 合成易场景（360VO 数据集）结果：360DVO 在全部指标上优于 OpenVSLAM 与 360VO，ATE 相对 360VO 降低 10%（1.11 vs 1.24 m；RPE(t) 0.235 vs 0.291；RPE(r) 0.440 vs 0.455）。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 5, Section V-B and Table II
- Evidence: V-B 360VO Dataset 段 + Table II 三方法三指标完整数值。
- Quote: “As shown in Tab. II, 360DVO achieves better per- formance on all metrics than both OpenVSLAM and 360VO, reducing the ATE by 10% compared with 360VO.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1259

- Claim: 合成难场景（TartanAirV2 评测集）结果：360DVO 默认配置取得最高成功率与精度（100% 成功，平均 ATE 0.038 m），而 OpenVSLAM（53%）与 360VO（27%）在全部 Hard 序列几乎失效；在 TartanAir 训练的学习型针孔方法表现尚可但在 Hard 序列挣扎，凸显全景 FoV 对 VO 的收益。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 5, Section V-B and Table I
- Evidence: V-B TartanAirV2 段 + Table I：360DVO 8/8 序列最优，成功率 100%；Droid-SLAM/DPVO/DPV-SLAM 100% 但平均 ATE 1.951/1.668/0.168。
- Quote: “As Tab. I shows, our 360DVO with default settings attains the highest success rate and accuracy, whereas OpenVSLAM and 360VO nearly fail on all hard sequences. Learning-based pinhole methods [7], [8], [37], trained on TartanAir [32], perform reasonably well but struggle on the Hard sequences, highlighting the benefit of omnidirectional FOVs for visual odometry.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1260

- Claim: FoV 解耦实验（本综述问题最直接证据）：为把宽 FoV 收益与算法性能分离，从全景图像虚拟裁切 90° FoV、640×640 的针孔序列跑针孔 SOTA。结论：窄 FoV 使挑战场景更难——增加 feature leave-view 事件、缩短长期共视；OVO 方法整体比针孔方法更稳更优，360DVO 相对 DPV-SLAM 在 Easy 降 ATE 56.2%、相对 DPVO 在 Hard 提升 37.1%。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 5, Section V-B and Table III
- Evidence: V-B 360DVO Dataset 段描述解耦设计与归因；Table III 给出 20 序列完整矩阵（Easy 平均：360DVO 3.31 vs DPV-SLAM 7.56；Hard：360DVO fast 3.68 vs DPVO 6.92）。
- Quote: “Narrow FOVs make challenging scenes harder by increas- ing feature leave-view events and shortening long-term co- visibility. Overall, OVO methods demonstrate more stable and higher performance than pinhole methods shown in Tab. III, revealing the inherent value of 360-degree coverage. 360DVO reduces ATE over DPV-SLAM by 56.2% on Easy and outperforms DPVO with 37.1% improvement on Hard.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1262

- Claim: 从针孔到全景的消融（特征网络必要性）：把 DPVO 的 BA 换成 ODBA 即可处理 360° 图像，但沿用经典 CNN（ResNet）特征时性能反而退化（avg ATE 7.37→9.99，Hard 12.7）——为 360° 图像设计专用特征网络是必要的。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 6-7, Section V-C and Table IV
- Evidence: V-C From Pinhole to Omnidirection 段 + Table IV：DPVO(pinhole,ResNet,DBA) 7.83/6.92/7.37 vs #1(360°,ResNet,ODBA) 7.33/12.7/9.99。
- Quote: “Replacing the BA module of DPVO [8] with the novel omnidirectional differentiable bundle adjustment (ODBA) module enables 360-degree cam- era pose optimization. However, although the modification allows 360-degree image processing, the method relying on classic CNN features has degraded performance as reported”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1268

- Claim: 真实基准上的全景方法内部对比：360DVO 相对 OpenVSLAM 在 Easy 降 27.6%、Hard 提升 43.4%（OpenVSLAM Easy 4.57 尚可、Hard 7.69 明显劣化）；直接法 360VO 在大量序列失败，平均成功率仅 43%，远低于 360DVO 的 100%。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 5, Section V-B and Table III
- Evidence: V-B 360DVO Dataset 段数值陈述；Table III 成功率列 360VO 42%（正文写 43%，四舍五入口径差异）、OpenVSLAM 94%(Easy)/92%(Hard)。
- Quote: “On the omnidirectional side, 360DVO surpasses OpenVSLAM by 27.6% on Easy and 43.4% on Hard. OpenVSLAM is competitive on Easy (i.e., 4.57) but underperforms on Hard (i.e., 7.69). Direct method 360VO fails on many sequences, with an average success rate of 43%, far below 360DVO’s 100%.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-0377

- Claim: 渲染采用混合方案：静态背景环境用 3D Gaussian Splatting（3DGS）渲染保证真实感，动态物体与机械臂用高质量 mesh 模型渲染（Isaac Sim 5.1，path-tracing 引擎着色）；每个时间步把动态渲染的机器人与物体叠加到静态 3DGS 背景上。作者称该方案"不仅保证真实感，还支持从任意视角和任意本体进行灵活的图像编辑"。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 7, Section 3.3.2 Robot Data Rendering
- Evidence: "Any View"的机制载体：3DGS 背景 + mesh 动态前景的混合渲染 + 任意视角重渲染；跨本体（UR5/ToRA/Franka/Unitree G1 等）同理由替换 mesh 实现。
- Quote: “we employ a hybrid rendering scheme in Isaac Sim 5.1, where the static background environment is rendered using 3D Gaussian Splatting (3DGS) for photorealism, while dynamic objects and robotic manipulators are rendered using high-quality mesh models. The entire rendering environment’s coordinate system is aligned with the robot base frame. Specifically, at each time step t, the joint angles of the robot arms are computed using an inverse kinematics (IK) solver based on the target pose matrices p”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0378

- Claim: 3DGS 重建经闭式相似变换与真实环境达到公制对齐后，导出为 USD 资产导入 Isaac Sim 作为动态渲染的静态背景；作者称此步骤"保证几何与光度一致性，从而减小视觉观测中的域差距"。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 6, Section 3.3.1 Scene Reconstruction
- Evidence: Real→Sim 几何桥梁：metric alignment 协议（承自 Re3SIM）保证渲染视角变化时场景几何不漂移，是"任意视角"成立的几何基础。
- Quote: “This closed-form solution ensures metric alignment between real and virtual environments. Once aligned, the 3DGS model is exported as a Universal Scene Description (USD) asset and imported into Isaac Sim, serving as the static background for dynamic rendering. This step guarantees geometric and photometric consistency, thereby reducing the domain gap in visual observations.”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0379

- Claim: 重投影验证显示：重投影的触觉接触点持续与可见的指-物交互区域重合（如指尖按压杯柄或工具表面），且渲染力的幅值与观察到的形变或握持强度相关；作者称这种跨模态一致性证实了多模态数据管线的时间同步与几何精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 8, Section 4.1 Simulation Evaluation
- Evidence: 仿真端验证方式：把估计的 3D 手套/物体/触觉点用相机内外参重投影回 RGB 帧做一致性检查；结论为主观检查级别而非量化指标。
- Quote: “Crucially, the reprojected tactile contact points consistently coincide with visible regions of finger-object interaction (e.g., fingertips pressing against a mug handle or tool surface), and the magnitude of the rendered force correlates with observed deformation or grip intensity. This cross-modal consistency confirms the temporal synchronization and geometric accuracy of our multimodal data pipeline, establishing a reliable foundation for subsequent retargeting and simulation.”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0380

- Claim: Dex-Tactile 重定向精度：在 Isaac Sim 中重放 10 个不同形状物体的重定向操作，把原手套触觉接触点经解剖对应映射到灵巧手后，与灵巧手表面实际模拟接触位置的欧氏距离平均误差为 3.86 mm。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 8, Section 4.1, Figure 4(b)
- Evidence: 重定向保真度量化：10 物体 Isaac Sim 重放、映射触觉点 vs 实际模拟接触位置的欧氏距离。
- Quote: “We then calculate the Euclidean distance between these mapped points and the actual simulated contact locations on the dex-hand surface. The results over 10 diverse objects are reported in Fig.4 (b). The average error of tactile contact points is 3.86 mm.”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0381

- Claim: 真机重放：按重定向轨迹与关节角驱动 UR5 + Paxini DexH13 执行 10 个物体的操作任务（每物体 10 次独立试验），平均成功率 84%；几何简单、接触模式稳定的物体（椰子水瓶、柔顺剂瓶）成功率 90–100，较复杂物体（塑料杯、相机）成功率仍高于 80。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 9, Section 4.2 Real-World Evaluation, Figure 4(c)
- Evidence: 真机重放量化结果：UR5+DexH13、10 物体 × 10 试验、平均 84%；复杂度分层（简单几何 90–100 vs 复杂 >80）。
- Quote: “We conduct replay experiments on UR5 equipped with the Paxini DexH13 dex-hand. For each of the retargeted demonstration, UR5 end-effector is driven according to the retargeted trajectory and dex-hand is driven according to the retargeted joint angles. The object is placed at the same position when human demonstration data collected, ensuring consistent starting conditions. We perform 10 independent trials per object. A trial is considered successful if the robot completes the intended manipulati”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0382

- Claim: VLA 下游配平对比（两数据源演示数量相等、任务相同、训练超参相同）：在三个代表性任务（pick-and-place、push cuboid、pour bottle）上，遥操作数据训练的 Pi0.5 达 100% 成功率，仅用生成（Real-Sim-Real）数据训练的 Pi0.5 达 80%；作者称"仅存在 20% 的成功率下降"，并据此主张该管线可作为遥操作的可扩展、低成本替代。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 9, Table 1 + Section 4.2
- Evidence: 数据源配平对比主结果：Tele 100% vs Paint 80%（Pi0.5，含腕相机）；"可替代遥操作"主张的直接依据。
- Quote: “To comprehensively evaluate the efficacy of our Real-Sim-Real data pipeline for robot skill learning, we conduct a comparative study by training Vision-Language-Action (VLA) policies using two distinct sources of demonstration data: (1) synthetic data generated through our proposed pipeline (referred to as Real- Sim-Real data), and (2) real-world teleoperation demonstrations collected via direct human control of the robot (referred to as Tele. data). To ensure a rigorously fair comparison and is”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0388

- Claim: 采集效率：在 6 个不同难度任务上各收集 100 条成功演示序列的双方法对比中，人类演示采集一致快于遥操作——pick-and-place 任务遥操作耗时为人类采集的 2.57×，多阶段的 table bussing 与 fold clothes 任务上人类采集约只需遥操作五分之一的时间（最高 5.33× 加速），且任务越复杂差距越大。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 10, Table 2 + Section 4.3
- Evidence: 成本量化：6 任务 × 100 条成功演示；效率倍率随任务复杂度上升（2.57×→5.33×）；table bussing/fold clothes 需双手协调与精细力控时加速最大。
- Quote: “To quantify this, we collected 100 successful demonstration sequences across 6 tasks of varying difficulty using both methods. All trials were conducted by trained operators, where a demonstration is defined as successful if the task is completed without object drops or resets. As summarized in Table 2, human demonstration consistently outperforms teleoperation across all tasks. For the basic pick-and-place task, teleoperation requires 2.57× the time relative to human collection. This gap widens”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0001

- Claim: 在 MuJoCo 模拟的六个操作任务的平均成功率上，单个腕戴鱼眼相机训练的 state-free 策略在特征贫乏背景下为 0.57、特征丰富背景下为 0.66，均高于单个腕戴针孔相机的 0.31 与 0.34。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 7, Table 1
- Evidence: Table 1 的单相机四行显示，鱼眼单相机在 poor/rich 两种背景下的六任务平均成功率（0.57/0.66）均高于针孔单相机（0.31/0.34）。
- Quote: “Pinhole(Single) Poor 0.40 0.52 0.36 0.04 0.14 0.40 0.31 Pinhole(Single) Rich 0.48(+0.08)0.56(+0.04)0.34(-0.02)0.18(+0.14)0.12(-0.02)0.38(-0.02)0.34(+0.03) Fisheye(Single) Poor 0.68 0.800.800.30 0.24 0.58 0.57 Fisheye(Single) Rich0.74(+0.06)0.84(+0.04)0.76(-0.04)0.56(+0.26)0.48(+0.24)0.60(+0.02)0.66(+0.09)”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0003

- Claim: 以本体感觉预测为代理任务探测编码器隐式空间感知时，三个真实任务上特征丰富背景下鱼眼相机训练的编码器均取得最低平移与旋转误差（Pick Cup 2.362 cm / 3.394°，Fold Towel 2.908 cm / 2.952°，Hang Chinese Knot 5.143 cm / 4.887°），远低于针孔相机在特征贫乏背景下的误差（Pick Cup 12.309 cm / 15.345°）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 7, Table 2
- Evidence: Table 2 显示每个任务的 Fisheye-Rich 行都是该任务四行中平移/旋转误差最低的，而 Pinhole-Poor 行误差最高；探针方法在表注中说明。
- Quote: “Table 2. Quantitative probing of visual encoder spatial awareness using proprioception prediction as a proxy task (RQ1). We eval- uate the quality of learned spatial representations by fine-tuning a lightweight MLP head on the pre-trained visual encoder to predict the robot’s proprioceptive state in three real-world tasks. Task Camera Feature Trans. Err(cm)↓Rot. Err( ◦)↓ Pick Cup Pinhole Poor 12.309 15.345 Pinhole Rich 5.367 7.612 Fisheye Poor 3.369 3.677 Fisheye Rich2.362 3.394 Fold Towel Pinho”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0004

- Claim: 在真实世界场景多样性实验中，仅用 8 个不同背景场景训练的鱼眼策略在完全未见场景上的零样本成功率迅速超过 95%；同一实验观察到鱼眼相机比常规（针孔）相机显著更大的场景多样性扩展潜力。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 7, Section 4.2
- Evidence: Section 4.2 报告真实世界设置下八个多样训练场景即可使鱼眼策略在未见环境的零样本成功率超过 95%，并观察到鱼眼相对常规相机更大的 scaling 潜力。
- Quote: “The results, presented in Fig. 8, strongly support our hy- pothesis. We observe that the fisheye camera exhibits sig- nificantly greater scaling potential compared to the conven- tional camera. Notably, in the real-world setup, the fish- eye policy’s zero-shot success rate on unseen environments (a) 5 unseen test scenes in simulation(b) 4 unseen test scenes in the real-world Figure 7. The unseen scenes for evaluation in (a) simulation and (b) real-world experiments (RQ2). rapidly exceeds95%when”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0007

- Claim: 在同一跨相机设置中，加入 Random Scale Augmentation 训练的策略在全部五个未见相机配置上保持更高成功率，作者据此支持'学习相对尺度是跨相机鲁棒性关键'的假设。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 8, Figure 10
- Evidence: Figure 10 的对比显示 RSA 训练的策略在所有未见相机参数上保持更高成功率，正文将其解读为相对尺度学习的证据。
- Quote: “In contrast, the policy trained with our RSA maintains higher success rates across all configu- rations, demonstrating robust generalization. This strongly supports our hypothesis that learning relative scale is the key to cross-camera robustness.”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0008

- Claim: 在模拟六任务平均成功率上，单个腕戴鱼眼相机的配置（特征贫乏 0.57、特征丰富 0.66）超过两个腕戴针孔相机的配置（0.38、0.45），即在 Table 1 的设置内更宽 FoV 的单相机优于双针孔。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 7, Table 1
- Evidence: Table 1 的单鱼眼行与双针孔行的 Average 列直接比较显示单鱼眼均值在两种背景复杂度下均更高。
- Quote: “Pinhole(Single) Poor 0.40 0.52 0.36 0.04 0.14 0.40 0.31 Pinhole(Single) Rich 0.48(+0.08)0.56(+0.04)0.34(-0.02)0.18(+0.14)0.12(-0.02)0.38(-0.02)0.34(+0.03) Fisheye(Single) Poor 0.68 0.800.800.30 0.24 0.58 0.57 Fisheye(Single) Rich0.74(+0.06)0.84(+0.04)0.76(-0.04)0.56(+0.26)0.48(+0.24)0.60(+0.02)0.66(+0.09) Pinhole(Double) Poor 0.50 0.44 0.26 0.22 0.44 0.40 0.38 Pinhole(Double) Rich 0.70(+0.20)0.34(-0.10)0.36(+0.10)0.38(+0.16)0.34(-0.10)0.56(+0.16)0.45(+0.07) Fisheye(Double) Poor 0.86 0.84 0.740.6”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0324

- Claim: OmniDP 的应用方式：端到端 LiDAR 驱动 3D 视动策略——金字塔卷积点云编码器（增强时间感知注意力）把全景点云编码为含空间结构与时间上下文的紧凑全局特征，条件化 Diffusion Policy 解码器迭代去噪生成协调动作序列，直接从全向观察映射动作、无中间状态估计；采用全景 LiDAR 在每个时间步捕获完整 360° 点云，提供对周围的全空间感知，使机器人不移动即可触及并操作身体周围任意位置的物体，并通过持续感知周围障碍在杂乱环境中支持无碰撞双臂协调。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 3, Section III-B, OmniDP
- Evidence: Sec. III-B 两段：Architecture of OmniDP 段给出编码器-解码器组成与端到端声明；Omnidirectional Perception 段给出 360° 点云、无需移动即可操作周围物体与无碰撞双臂协调的设计意图。
- Quote: “OmniDP comprises a percep- tion encoder and an action decoder. The encoder processes panoramic point clouds using a pyramid convolutional en- coder [6] enhanced with time-aware attention, producing a compact global feature that captures both spatial structure and temporal context. This feature conditions a Diffusion Policy [4] decoder, which iteratively denoises random noise into coordinated action sequences. The end-to-end frame- work directly maps omnidirectional observations to whole- body ac”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0325

- Claim: 传感硬件：头装 Livox MID-360 全景 LiDAR 提供 360° 水平、−7° 到 52° 垂直视场，10 Hz 下每秒最多生成 200k 点；宽 FoV 与非重复扫描模式在短时间窗内改善空间覆盖、增强杂乱室内环境的几何一致性；系统不依赖多相机融合或结构光深度传感器，直接以原始 LiDAR 点云作为主要视觉输入模态。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 3, Section III-C, Panoramic Lidar Perception
- Evidence: Sec. III-C Panoramic Lidar Perception 段给出 MID-360 的 FoV、点率、非重复扫描与“原始点云为唯一视觉输入”的声明；仿真侧 LiDAR 技术栈基于 DISCOVERSE（同段末句，已核对）。
- Quote: “Our perception system centers on a head-mounted Livox MID-360 LiDAR, rigidly installed to align with the operator’s egocentric viewpoint and provide panoramic 3D observations. The LiDAR pro- vides a 360 ◦ horizontal and −7 ◦ to 52 ◦ vertical field-of- view (FoV), generating up to 200k points per second at 10 Hz. The wide FoV and non-repetitive scanning pattern improve spatial coverage within short temporal windows, which enhances geometric consistency in cluttered indoor environments. Instead of”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0328

- Claim: 六任务（2 仿真 + 4 真机，每任务 20 次试验）总成功率：OmniDP 82/120，相机基线 iDP3 25/120、DP3 22/120、DP 18/120；四个视野外（OV）任务上三个基线全部 0/20，OmniDP 达仿真 Pour 12/20、真机 Hand Over 12/20、Pour 11/20、Wipe 16/20；视野内 Pick & Place 上仿真 16/20（iDP3 14/20）、真机 15/20（iDP3 11/20）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 5, Table I
- Evidence: Tab. I 逐格给出四方法 × 六任务成功率与 Total 列；OV 任务基线全 0/20 的解释见 page 6 Sec. IV-A（all baselines largely fail due to their limited perceptual coverage，已核对）。
- Quote: “TABLE I: Performance comparison. Our method consistently outperforms existing RGB-based and depth-to-point-cloud baselines across all simulated and real-world tasks, with particularly significant advantages in scenarios where target objects lie outside the camera’s field of view. Simulation Real World Method Pick & Place Pour (OV) Pick & Place Hand Over (OV) Pour (OV) Wipe (OV) Total DP 10/20 0/20 8/20 0/20 0/20 0/20 18/120 DP3 13/20 0/20 9/20 0/20 0/20 0/20 22/120 iDP3 14/20 0/20 11/20 0/20 0/2”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0330

- Claim: 杂乱环境避碰评估（物理障碍置于机器人操作路径上、处于头装 RGB-D 相机视野之外，page 6 Sec. IV-B）：OmniDP 任务成功 14/20、碰撞率 5/20；三个相机基线任务成功均为 0/20、碰撞率 DP 20/20、DP3 18/20、iDP3 18/20——基线因无法感知相机视野外的障碍而频繁碰撞。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 6, Table II and Section IV-B
- Evidence: Tab. II 逐格给出四方法的成功率与碰撞率；障碍置于相机 FOV 外的实验设置逐字位于 page 6 Sec. IV-B（place a physical obstacle along the robot’s manipulation path, positioned outside the field of view of the head-mounted RGB-D camera，已核对）。
- Quote: “TABLE II: Collision-free manipulation evaluation. Results demonstrate that OmniDP achieves robust omnidirectional obstacle avoidance in cluttered environments. Method Success Rate ↑ Collision Rate ↓ DP 0/20 20/20 DP3 0/20 18/20 iDP3 0/20 18/20 Ours 14/20 5/20”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0332

- Claim: Hand Over 任务消融（Tab. IV）：完整 OmniDP 成功率 12/20；移除全景观察（w/o Omni. Obs.，即仅依赖自体深度相机点云，page 6 Sec. IV-D）导致完全任务失败 0/20——作者称之为凸显 360° 场景理解对此类任务的关键作用；移除时间感知注意力池化（w/o TAP）降至 9/20，表明历史点云上的注意力时间平滑贡献更稳定的策略执行。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 7, Table IV; page 6, Section IV-D
- Evidence: Tab. IV（page 7）给出三行成功率；消融叙述（removing the panoramic LiDAR input (i.e., relying solely on egocentric depth-based point clouds) leads to complete task failure；disabling TAP results in a noticeable decrease）逐字位于 page 6 Sec. IV-D（已核对）。
- Quote: “TABLE IV: Ablation study. The results confirm the neces- sity of the designed components. Ablation Success Rate OmniDP 12/20 w/o Omni. Obs. 0/20 w/o TAP 9/20”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0339

- Claim: 作者观察到：在固定相机配置上微调的 VLA 对相机-机器人硬件排布的轻微偏移极度敏感——仅 3 cm 的腕相机偏移就可使任务成功率减半；即使小偏移也需要在修改后的设置下重新采集演示并微调整个模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 1, Section I, Introduction
- Evidence: 引言以作者自身观察量化视角敏感性：minor variations 下 performance degrades significantly，3 cm 腕相机偏移即可 halve the success rate；并由 VLA 端到端特性推出重采数据+全模型微调的必要性。
- Quote: “We mainly focus on deviations of hardware arrangement between the camera and the robot, where minor shifts are unavoidable in everyday unstructured environ- ments, such as homes or offices. Even under minor varia- tions, the performance degrades significantly. For example, we observed that a 3 cm shift in the wrist camera can halve the success rate. The inherent end-to-end nature of VLAs necessitates acquiring demo trajectories in the modified setup and fine-tuning the entire model even after sm”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0340

- Claim: 据本文引用的 LIBERO-Plus 与 VLATest 评测，VLA 在相机扰动下出现大幅性能退化，成功率从超过 90% 跌至 30% 以下（LIBERO-Plus 数字）——相机视角敏感性被视为非结构化环境部署的关键障碍。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 2, Section II-A, Vision-Language-Action Models
- Evidence: 相关工作节引用 LIBERO-Plus [10] 与 VLATest [11] 的评测结果：success rates dropping from over 90% to below 30% [10]，并称 camera viewpoint sensitivity 为 real-world deployment 的 critical barrier。
- Quote: “Recent evaluations on LIBERO-Plus [10] and VLATest [11] reveal substantial performance degradation under camera perturbations, with success rates dropping from over 90% to below 30% [10]. This camera viewpoint sensitivity poses a critical barrier to real-world deployment in unstructured environments where camera placements differ from trained environments.”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0341

- Claim: 相机适配模块以 LVSM（前馈新视角合成，decoder-only）实现，实时运行不构成控制瓶颈：模块约 30 FPS，而典型 VLA 约 10 Hz；LVSM 在 RTX 4090（BF16）上以 36.55 ms 从 2 个输入视图合成 2 个 256×256 新视图（约 27 FPS）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 3, Section III-B
- Evidence: 方法节给出控制回路四步（采集→虚拟合成训练视角→冻结策略推理→执行）与实时性论证：approximately 30 FPS vs typical VLAs ~10 Hz；LVSM 具体延迟 36.55 ms（2 视图→2 视图，256×256，RTX 4090，BF16，27 FPS）。
- Quote: “Since the camera adaptation module operates at approximately 30 FPS while typical VLAs run at around 10 Hz [4], [5], [6], our frame- work introduces negligible computational overhead and does not become a bottleneck in the control loop. Specifically, LVSM [24] achieves a latency of 36.55 ms for synthesizing 2 novel views from 2 input views at 256×256 resolution on an NVIDIA RTX 4090 GPU with BF16 mixed precision, corresponding to 27 FPS.”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0343

- Claim: 在 LIBERO 四套件的 agent 相机（三档 S/M/L）扰动评估中（Table I）：本方法在所有套件与扰动档位上取得最佳成绩——Ours-π 全套件平均成功率 94.5%、Ours-OV 85.6%，均超过数据增广微调基线 π*0.5（87.2%）、表征中心基线 GeoAwareVLA（86.1%）与未适配基线（π0.5 平均 67.9%、OpenVLA-OFT 62.1%）；未适配基线随扰动档位急剧退化（OpenVLA-OFT 85.2%→46.2%，π0.5 92.4%→39.9%，small→large）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 4, Table I and Section IV-A.2
- Evidence: Table I 报告 agent 相机扰动（wrist 固定）下六方法×四套件×三档成功率；正文总结 Our methods consistently achieve the best performance across all suites and perturbation levels，并给出基线退化数字（85.2→46.2、92.4→39.9）与 Ours-π 94.5%。
- Quote: “Our methods consistently achieve the best performance across all suites and perturbation levels, demon- strating robust viewpoint generalization. While base policies experience drastic performance degradation as camera vari- ation increases—for instance, OpenVLA-OFT drops from 85.2% (small) to 46.2% (large) and π 0.5 from 92.4% to 39.9%—our view adaptation method provides significant im- provements for both base policies. Notably, Ours-π achieves 94.5% average success rate, while maintaining con”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0344

- Claim: 在 LIBERO-Long 的腕相机扰动评估中（agent 相机固定，Table II）：Ours-π 平均成功率 88.6%（S/M/L：91.8/89.6/84.4），高于数据增广基线 π*0.5（83.1%）与未适配 π0.5（28.6%）；GeoAwareVLA 平均仅 5.2%、全档低于 10%——尽管它在 agent 相机扰动下可达 86.1%（Table I）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 4, Table II and Section IV-A.2
- Evidence: Table II 报告 LIBERO-Long 腕相机三档扰动成功率；正文总结本方法 88.6% 平均、超过数据增广与 GeoAwareVLA，并指出 GeoAwareVLA 从 agent 扰动下的 86.1% 崩溃到腕扰动下的 <10%。
- Quote: “As shown in Table II, our method achieves 88.6% average success rate, outperforming both data augmentation and GeoAwareVLA. Interestingly, GeoAwareVLA shows a dramatic performance collapse un- der wrist camera perturbations, dropping to below 10% across all perturbation levels despite achieving competitive performance (86.1%) on agent camera perturbations in Ta- ble I.”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0349

- Claim: 真机实验（Franka Panda + π0.5 LoRA 微调，4 个桌面任务，测试时把训练用 ZED2 相机之一换成另一位置的 ZED2）：基线策略在所有任务的新视角上成功率一致下降（末端执行器能移到目标附近但无法精确抓取/放置）；本方法维持与训练视角相当的任务成功率（进度与二值两种口径），证明零样本相机适配在真实操作场景中对新视角有效。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 7, Section IV-B.2 and Fig. 6
- Evidence: IV-B.2 节报告 Fig. 6 的真机新视角结果：基线一致下降、本方法维持训练视角水平；评估协议为每任务执行 10 次（page 6）、指标为 Task Success Rate（Progress 分阶段部分得分 / Binary 二值）。
- Quote: “even a slight change in viewpoint is sufficient to degrade task performance. In contrast, our method maintains task success rates comparable to those achieved with the training viewpoint, demonstrating that our zero-shot camera adapta- tion framework effectively generalizes to novel viewpoints in real-world manipulation scenarios.”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0618

- Claim: PanoMMOcc 是首个面向四足机器人的真实世界全景多模态语义占据数据集（四传感模态、多样场景），配套提出 VoxelHound 框架（含 VJC 垂直抖动补偿与 MIPF 多模态信息 prompt 融合），在其基准上取得 SOTA，mIoU 提升 +4.16。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 1, Abstract; page 2, Section I and Table II (page 7)
- Evidence: 摘要声明 first real-world panoramic multimodal occupancy dataset for quadruped robots、四个传感模态、VJC/MIPF 两模块与 +4.16 mIoU SOTA；正文 page 2 与 Table II 给出 23.34 vs 19.18 的完整数字。
- Quote: “we introduce PanoMMOcc, the first real-world panoramic multimodal occu- pancy dataset for quadruped robots, comprising four sensing modalities collected across diverse scenes. We further propose VoxelHound, a panoramic multimodal occupancy perception framework tailored to legged locomotion and spherical imaging. VoxelHound incorporates a Vertical Jitter Compensation (VJC) module to mitigate severe viewpoint perturbations caused by body pitch and roll during locomotion, enabling more consistent s”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0619

- Claim: PanoMMOcc 采集平台以 Unitree Go2 四足机器人为载体：全景输入来自一台 PAL（Panoramic Annular Lens）相机，360°×70° FoV、最高 40 FPS、2048×2048 分辨率；另在机器人背部搭载 MID-360 LiDAR 采集点云。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 3, Section III Sensor suite
- Evidence: 第 III 节 Sensor suite 列出 rig 组成：(1) Unitree Go2 平台；(2) PAL 相机 360°×70° FoV@40FPS、2048×2048；(3) 背载 MID-360 LiDAR；热/偏振相机参数在 page 4（Guide Infrared N-Driver P302B 640×512@25FPS；LUCID TRI050S-QC 1224×1024）。
- Quote: “Sensor suite. We develop a panoramic multimodal data ac- quisition platform mounted on a quadruped robot, as shown in Fig. 2. (1) Quadruped platform. A Unitree Go2 robot is employed for data collection, and its agile locomotion enables traversal of complex outdoor environments. (2) Panoramic camera. A Panoramic Annular Lens (PAL) camera provides a 360 ◦ × 70 ◦ FoV at up to 40 FPS with a resolution of 2048 × 2048. (3) LiDAR. A MID-360 LiDAR mounted on the robot’s back captures accurate 3D point”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0620

- Claim: VoxelHound 全模态（C+L+T+P）在 PanoMMOcc 上达 23.34 mIoU SOTA：超最佳 camera-only MonoScene（8.94）+14.40，超最佳多模态 EFFOcc-T（19.18）+4.16（+21.7%）；同 C+L 设定下 22.87 亦超 EFFOcc-T +3.69——作者将热/偏振增益解读为互补信息。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 2, Section I; page 8, Section V-B-1 and Table II (page 7)
- Evidence: page 2 引言末段给出三个数字（23.34/8.94/+14.40/19.18/+4.16/+21.7%）；page 8 V-B-1 补充同 C+L 设定 22.87 vs 19.18（+3.69）与热偏振互补性解读。
- Quote: “Extensive experiments on PanoMMOcc show that VoxelHound achieves state-of-the-art performance at 23.34 mIoU, surpass- ing the best camera-only MonoScene (8.94; +14.40) and the best multimodal EFFOcc-T (19.18; +4.16, +21.7%).”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0623

- Claim: VJC 动机：与轮式平台不同，四足运动使机体沿垂直轴振荡，在采集图像中引入垂直抖动；这种步态扰动造成空间特征表示错位并降低 BEV 变换稳定性——VJC 是插入图像编码器与 2D-to-BEV 视角变换之间的轻量补偿模块。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 6, Section IV-D Vertical Jitter Compensation
- Evidence: 第 IV-D 节动机段逐字；模块细节（宽度平均→Conv 编码器→回归头→归一化 Δh→grid sample 双线性补偿）在公式 (4)-(6)。
- Quote: “Unlike wheeled autonomous driving platforms, our dataset is collected using a quadruped robot. Due to legged locomo- tion, body oscillation along the vertical axis introduces vertical jitter in the captured images. This gait-induced perturbation causes misalignment in spatial feature representation and de- grades the stability of the BEV transformation. To mitigate this issue, we propose a lightweight Vertical Jitter Compensation (VJC) module, which is inserted between the image encoder and the”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0624

- Claim: VJC/MIPF 模块消融增益有限：基线 22.74 mIoU（IoU 46.03），仅 VJC 22.97、仅 MIPF 22.88，两者并用 23.34（IoU 46.08）——合计 +0.60 mIoU，说明基准上的性能主要来自多模态输入与基线架构，两个专用模块是边际改进。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 7, Table IV; page 8-9, Section V-C
- Evidence: Table IV 四行（1/2/3/Ours）逐字；page 9 正文补充 combining both further increases it to 23.34 mIoU 与互补性结论。
- Quote: “TABLE IV ABLATION ON DIFFERENT COMPONENTS IN VOXELHOUND. # VJC MIPF IoU↑ mIoU↑ 1 46.03 22.74 2 ! 45.96 22.97 3 ! 46.06 22.88 Ours ! ! 46.08 23.34”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0625

- Claim: MIPF 采用非对称融合：直接拼接/相加对所有模态一视同仁会稀释几何一致性并引入模态干扰；MIPF 以 LiDAR 为几何基底，图像模态（RGB/热/偏振）压缩为语义 prompt，经残差 sigmoid 调制自适应增强而非覆盖 LiDAR 特征——保证几何结构作为主表示基。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 6, Section IV-E Multimodal Information Prompt Fusion
- Evidence: 第 IV-E 节开头动机段逐字（Direct concatenation...geometric basis）；公式 (7)-(10) 给出 prompt 生成、几何引导注意力与残差调制。
- Quote: “Direct concatenation or addition treats all sensor modalities equally, although they provide different types of information. In practice, heterogeneous sensors contribute fundamentally different information: LiDAR directly measures 3D geometry, while RGB, thermal, and polarization modalities provide com- plementary semantic and appearance cues. Blindly blending these features may dilute geometric consistency and introduce modality interference. Thus, MIPF adopts asymmetric fusion, using LiDAR as”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0626

- Claim: FOV 感知评测（剔除 pedestrian，因采集操作员总在平台后方、对前置热/偏振相机不可见）：C+T、C+P 分别提升 matched-FOV mIoU 3.8% 与 5.8%，C+T+P 在 union FOV 上提升 19.7%，且方位角扇区一致改善——有限 FOV 的多模态线索也能惠及直接观测区域之外的占据预测。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 8, Section V-B-2 and Fig. 7
- Evidence: 第 V-B-2 节整段逐字，含 pedestrian 剔除理由、三个增益数字与方位角扇区结论；Fig. 7(a)(b)(c) 对应图示。
- Quote: “Beyond-FOV Benefits of Multimodal Perception: For fair FOV-specific evaluation, the pedestrian class is excluded be- cause the data-collection operator consistently appears behind the platform and is therefore invisible to the forward-facing thermal and polarization cameras. As shown in Fig. 7(a), C+T and C+P improve the matched-FOV mIoU by 3.8% and 5.8%, respectively, while C+T+P yields a larger gain of 19.7% over the union FOV. Fig. 7(b) and (c) further show consistent improvements across azim”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0631

- Claim: 标定管线：全景/热/偏振相机分别用棋盘格独立标内参——热与偏振相机用带径向/切向畸变的标准针孔模型，PAL 全景相机用通用 Taylor（OCam）模型处理其强非线性全景投影；内参通过最小化棋盘格角点重投影误差估计并全数据集固定。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 11-12, Appendix A-C Calibration
- Evidence: 附录 A-C Camera Intrinsic Calibration 段逐字；LiDAR-相机外参用白板四角手动标注+重投影误差优化（公式 16-17，page 12），标定可视化 Fig. A.1。
- Quote: “Camera Intrinsic Calibration. We independently calibrate the panoramic, thermal, and polarization cameras using checkerboard patterns captured from diverse viewpoints. For thermal and polarization cameras, we adopt the standard pinhole model with radial and tangential distortion. For the Panoramic Annular Lens (PAL) camera, we use the generic Taylor (OCam) model [95] to handle its strong nonlinear om- nidirectional projection. All intrinsic parameters are estimated by minimizing the reprojection”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0708

- Claim: Fisheye3R 论文主张：在大规模透视图像上训练的前馈多视图 3D 重建基础模型在鱼眼图像上性能退化，根因是非线性投影模型改变了 3D 点到 2D 图像平面的映射、导致像素空间排布变化（而非单纯的数据分布未见）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 1, Abstract
- Evidence: 摘要把退化原因从'训练数据没见过鱼眼'具体化为非线性投影引起的像素空间重排，为'在模型侧适配鱼眼几何'而非'收集更多鱼眼数据'的路线提供依据。
- Quote: “Feed-forward foundation models for multi-view 3-dimensional (3D) reconstruction have been trained on large-scale datasets of perspec- tive images; when tested on wide field-of-view images, e.g., from a fish- eye camera, their performance degrades. This degradation arises from changes in spatial arrangements of pixels induced by the non-linear pro- jection model that maps 3D points onto the 2D image plane.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0709

- Claim: 作者主张：鱼眼相机因大场景覆盖带来的态势感知优势被广泛应用于从机器人到 AR/VR 的空间应用；许多平台部署宽 FoV 或同时含透视与鱼眼的混合相机系统，而透视训练的 3D 基础模型此前无法直接集成进这类商用系统。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 2, Section 1 Introduction
- Evidence: 引言把鱼眼在具身系统的存在感（态势感知、混合 rig、商用集成缺口）作为研究动机直接陈述，是'鱼眼镜头在具身领域应用方式'的一手动机证据。
- Quote: “As many spatial applications are deployed on platforms with wide field-of-view (FoV) cameras or mixed-camera systems, e.g., comprising both perspective and fisheye cameras, these foundation models have been unsuitable for direct integration into these commercial systems.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0711

- Claim: Fisheye3R 的核心机制是在模型潜空间（而非图像空间）重校准鱼眼特征：向每个 transformer 层（图像编码器前 L0 层除外）插入 K 个可学习校准 token 调制高层特征，使鱼眼特征对齐到透视特征表示。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 6, Section 3.2 Model Adaptation with Calibration Tokens
- Evidence: 方法节明确 token 插入位置（编码器除前 L0 层外的所有层 + 注意力层）与目的（对齐鱼眼与透视特征表示）；训练时仅校准 token 被学习、主干完全冻结（page 7，Sec 3.2 末）。
- Quote: “To bridge this gap, we align fisheye feature representations with those of per- spective images by introducing K learnable calibration tokens into each trans- former layer. As illustrated in Fig. 2, these tokens are inserted into all the encoder layers except the initial L 0 layers to modulate the high-level features.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0712

- Claim: 针对鱼眼真值数据稀缺，作者提出三档数据灵活性的学习方案：(i) SSL——仅有无标注透视 RGB 图像时，用模型自身在原始透视序列上的预测作伪标签进行自监督（配合合成畸变）；(ii) SL——有标注透视数据直接监督；(iii) SL+——透视+鱼眼标注数据监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 7, Section 3.3 Learning
- Evidence: Sec 3.3 按数据可得性给出三种监督方案并给出损失形式（式 11-13）；SSL 的伪标签机制（原始模型对未畸变序列的预测）直接决定其收益上限受基线质量约束。
- Quote: “We propose three supervision schemes according to the types of data available. Self-supervised learning with perspective images (SSL). If only perspec- tive RGB images I p are available with no ground truth, we generate pseudo- labels using the original model’s predictions for self-supervision.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0713

- Claim: 在 3 个基础模型（VGGT/π³/MapAnything）× 3 个鱼眼测试集 × 15 指标共 135 项测试中：仅用无标注透视图像的 SSL 即在 26/135 项取得 >50% 提升；加入透视标注（SL）后为 37/135；加入鱼眼标注（SL+）后达 77/135——收益随监督强度单调扩大。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 11, Section 4.2 Results (Table 1 on page 9)
- Evidence: 结果节用 135 项测试的 >50% 改善计数刻画三方案收益阶梯，同时说明框架在数据受限 regime 有效且随监督扩展高效扩展。
- Quote: “Remarkably, even self-supervised learn- ing using only unlabeled perspective RGB images boosts performance on fisheye data by a large margin, achieving a 50%+ improvement in 26/135 tests across all models and metrics. This highlights our framework’s potential to scale with larger corpora of unlabeled data for further enhancement. The introduction of annotated perspective data further strengthens these results, with 37/135 met- rics showing improvements exceeding 50%. Performance ultimately peaks”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0714

- Claim: 在户外驾驶数据集 KITTI360 上，MapAnything+Fisheye3R（SL+）相对未适配基线大幅提升：位姿 AUC 0.428→0.917、ATE 1.215→0.152、深度 δ1 0.607→0.922、点云 CD 1.301→0.575、FoV AUC 0.259→0.805。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 9, Table 1
- Evidence: Table 1 的 KITTI360/MapAnything 块给出基线与三种方案的 15 指标完整数值；户外场景 SL+ 收益幅度显著大于室内，说明真实鱼眼标注对户外域差的关键作用。
- Quote: “MapAnything [20] 0.818 0.947 0.428 1.215 3.023 20.568 0.258 5.775 0.607 1.097 1.505 1.301 18.034 6.642 0.259 w/ SSL 0.906 0.989 0.540 0.707 2.152 15.528 0.156 4.294 0.809 0.933 1.098 1.015 15.739 6.025 0.291 w/ SL 0.906 0.982 0.538 0.682 2.141 15.342 0.153 4.458 0.814 0.938 1.094 1.016 15.750 5.998 0.295 w/ SL+ 1.000 0.992 0.917 0.152 0.350 1.565 0.091 3.282 0.922 0.549 0.601 0.575 2.963 1.938 0.805”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0716

- Claim: 混合相机序列需要门控机制：在纯鱼眼序列上训练的校准 token 会因参数漂移使透视图像性能退化；在混合序列上训练可保留透视精度但削弱鱼眼适配；提出的掩码注意力（按帧相机类型屏蔽 token 对透视帧的影响）在所有透视比例上最稳健，并保证透视向后兼容与混合序列推理。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 12, Section 4.2 Performance on hybrid inputs (Fig. 5)
- Evidence: 作者在混合序列分析（Fig.5）中报告了三种训练策略随透视比例变化的权衡，并给出掩码注意力同时保住两侧性能的结论；这构成混合 rig 部署的设计约束证据。
- Quote: “Fig. 5 shows that while calibration tokens excel at optimizing pure fisheye sequences, they suffer from parameter drift caused by specialized training on fisheye images, leading to per- formance degradation on perspective images. Conversely, while training tokens on mixed-camera sequences preserves perspective accuracy, it weakens adapta- tion to fisheye data.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0717

- Claim: 混合相机能力的具身落地示例：自动驾驶车辆配备左/右鱼眼+前视透视相机时，该方法利用前视透视相机桥接两侧鱼眼视图，从混合传感器重建出单一几何一致的全景场景。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 12, Section 4.2 (Fig. 6)
- Evidence: 作者把 KITTI360 异构 rig 作为'实际部署场景'展示：透视相机桥接两侧鱼眼视图形成单一全景重建；Fig.6 caption 进一步指出没有异构相机处理能力时两个鱼眼视图的重建将保持断裂。
- Quote: “The reconstructions in Fig. 6 illustrate a practical deployment scenario of our mixed-camera model for autonomous driving, where a vehicle is equipped with heterogeneous cameras. Leveraging the forward-facing perspective camera to connect the left and right fisheye views, our method recon- structs a single, geometrically consistent panoramic scene from hybrid sensors.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0718

- Claim: 适配参数开销极小：向图像编码器后 12 层与帧级/全局注意力层（E/F/G 模块）各插入 K=8 校准 token 共需 344,064 可训练参数，而达到相近深度/点图精度的 LoRA 对照需 1,032,192（r=4）至 8,257,536（r=32）参数——r=32 约为校准 token 的 24 倍。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 22, Table 4
- Evidence: Table 4 给出各模块组合与 LoRA 各秩的可训练参数量与 9 项重建指标；正文指出 LoRA r=32 参数量为校准 token 的 24 倍、两者深度/点图相当而校准 token 在位姿与 FoV 上最优（page 24）。
- Quote: “E F G 344,064 35.24 0.134 4.370 0.171 0.810 0.058 0.045 3.264 2.074 LoRA r = 4 1,032,192 34.85 0.142 4.603 0.178 0.804 0.060 0.046 3.668 2.394 r = 8 2,064,384 34.86 0.142 4.560 0.173 0.808 0.059 0.046 3.454 2.242 r = 16 4,128,768 34.88 0.139 4.494 0.172 0.808 0.058 0.046 3.380 2.177 r = 32 8,257,536 34.93 0.137 4.410 0.170 0.810 0.057 0.045 3.398 2.198 Table 4: Ablation study of calibration tokens (C.T.) inserted to different modules and comparison to LoRA (with different ranks r). Reconstructio”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0719

- Claim: 推理开销近乎为零：加入校准 token 后 MapAnything 推理速度与显存完全不变（31.1 FPS、14.72 GiB）；掩码注意力仅在相机类型未知/混合序列时引入，代价为 29.1 FPS（约 -6%）与 15.26 GiB（约 +4%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 23, Table 5
- Evidence: Table 5 在 A6000 上测量基线/+token/+token+掩码注意力的 FPS 与峰值显存；caption 明确 6%/4% 开销仅在未知或混合相机类型序列中出现，纯鱼眼序列适配完全零成本。
- Quote: “Baseline 31.1 14.72 + Calibration Tokens 31.1 14.72 + Calibration Tokens + Masked Attention 29.1 15.26 Table 5: Average inference frames per second (FPS) and peak GPU memory across the test sequences with MapAnything model and an A6000 GPU. The inference overhead is mainly from masked attention (6% in runtime and 4% in memory), which is only introduced when the test sequences have unknown and potentially mixed camera types.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0720

- Claim: 投影模型泛化：仅用 Kannala-Brandt 模型合成畸变训练的校准 token，在 Stanford2D3DS 上使 π³ 的重建 CD 在 7 种投影模型下全部大幅下降——KB(OOD) 0.230→0.116、Fisheye624 0.228→0.117、MEI 0.264→0.095、Equidistant 0.219→0.107、Stereographic 0.211→0.088、Equiangular 0.241→0.116、Orthographic 0.375→0.182（改善 48.5%-64.1%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 14, Table 2
- Evidence: Table 2 用 Stanford2D3DS 渲染 7 种投影模型做受控对比，剥离数据集混淆因素；改善幅度 48.5%-64.1% 说明校准 token 学到的是投影域差的一般性校正而非 KB 特定拟合。
- Quote: “π 3 CD↓ 0.230 0.228 0.264 0.219 0.211 0.241 0.375 +Ours 0.116 0.117 0.095 0.107 0.088 0.116 0.182 Improvement 49.7% 48.5% 64.1% 51.1% 58.1% 52.0% 51.5%”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0721

- Claim: 相机模型泛化超出鱼眼：在 Matterport3D 全景图像上训练的校准 token 可迁移到 Stanford2D3DS 的 360° 全景图像多视图重建，作者据此主张校准 token 能泛化到鱼眼以外的相机模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 14, Section 4.2 Generalization to panoramic images (Fig. 9)
- Evidence: 作者以 Matterport3D 训练、Stanford2D3DS 测试的跨数据集全景重建实验（Fig.9）说明校准 token 的相机模型泛化潜力，但仅此一组定性实验，未给全景任务的定量指标。
- Quote: “Figure 9 presents multi-view reconstructions from 360 ◦ im- ages, where calibration tokens are trained on Matterport3D [5] and tested on Stanford2D3DS [2]. The result implies that calibration tokens can be general- ized to camera models beyond fisheye.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0781

- Claim: OccTrack360 提供 174~2234 帧的长时序多样序列（论文称显著长于既有占据跟踪基准），并配以原则性体素可见性标注：覆盖全方向的遮挡掩码与基于 MEI 统一投影模型的鱼眼 FoV 掩码。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 1, Abstract
- Evidence: 摘要明确给出序列长度区间与两类掩码；长时序（最长 2234 帧）是评估时序一致性与长时程跟踪行为的前提。
- Quote: “OccTrack360 provides substantially longer and more diverse sequences (174∼2234 frames) than prior benchmarks, together with principled voxel visibility annotations, including an all- direction occlusion mask and an MEI-based fisheye field-of-view mask.”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0782

- Claim: 在占据与鱼眼感知数据集对比表中，OccTrack360 以 18 个语义类别、128×128×16 体素空间并提供实例级标注，与 TrackOcc-Waymo（2025，14 类、200×200×16、实例级）同列，而 SemanticKITTI/Occ3D/nuScenes-Occupancy/OpenOcc/SSCBench-KITTI360 系列均无实例级标注——鱼眼占据跟踪基准进入'实例级'时代但体素空间反而小于针孔路线。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 2, Fig. 2(a)
- Evidence: Fig. 2(a) 对比表：OccTrack360 行为 2026/18 类/128×128×16/实例级 ✓；WoodScape/SynWoodScape 为鱼眼但无体素标注；TrackOcc-Waymo 是唯一此前有实例级的占据跟踪基准。
- Quote: “TrackOcc-Waymo [13] 2025 14 200×200×16 ✓ OccTrack360 (Ours) 2026 18 128×128×16 ✓”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0785

- Claim: 配备 MEI 球面几何提升（FEL）的 FoSOcc 直接以原始鱼眼为输入取得 OccSQ 总体 14.37 / OccSTQ 14.38，较同输入设置下针孔提升的 TrackOcc（1.59/1.67）提升 +12.78/+12.71——在提升模块内建模鱼眼几何（而非矫正图像）使原始鱼眼输入达到甚至超过 all 输入设置的水平。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 7, Table II
- Evidence: Table II Fisheyes 行：FoSOcc 14.37/14.38 vs TrackOcc 1.59/1.67；page 1 Fig. 1 亦标注 +12.78（SQ overall F 列），交叉一致。Fisheyes 设置的 14.37 甚至高于 all 设置的 14.20。
- Quote: “TrackOcc Fisheyes 1.59 1.02 4.37 0.34 0.03 1.76 2.16 0.74 0.14 1.67 FoSOcc (Ours) 14.37 6.33 33.75 3.73 12.95 14.40 17.63 6.64 1.69 14.38”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0786

- Claim: 在 all 输入设置下，FoSOcc 将 OccSQ 总体从 12.90 提升至 14.20（OccSTQ 14.84→15.82），增益集中出现在此前近乎为零的几何规则类别：parking 0→7.56、fence 0.85→2.90——鱼眼感知的收益分布不均，几何规则小类获益最大。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 7, Table II
- Evidence: Table II all 行两组数字逐类对比；parking 从 0 到 7.56 与 fence 从 0.85 到 2.90 是增益主体，Fig. 1 亦标注 +1.30/+7.56/+2.05 三组差值（overall/parking/fence），交叉一致。
- Quote: “TrackOcc all 12.90 0 29.87 0.85 7.02 17.07 20.69 8.38 3.40 14.84 FoSOcc (Ours) 14.20 7.56 25.09 2.90 12.70 17.61 21.53 9.87 5.03 15.82”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0788

- Claim: 在针孔基准 Occ3D-Waymo 上，FoSOcc（CFM）取得 OccSQ 总体 30.8（基线 TrackOcc 29.4）、OccSTQ 20.9（20.0）；作者报告相对 SQ 提升 sign +11.1%、general objects +20.7%、cyclist AQ +26.1%——中心聚焦监督在针孔标准设置下也带来小尺度类别增益，说明其收益不专属鱼眼畸变。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 7, Table I + Section V-C
- Evidence: Table I：FoSOcc 30.8/15.3(sign)/44.9(building)/40.8(vegetation)/11.1(G.O.)/14.2(AQ)/20.9(STQ) vs TrackOcc 29.4/13.6/43.2/40.0/9.2/13.5/20.0；正文 V-C 给出三个相对提升百分比。
- Quote: “Our proposed CFM significantly outperforms the baseline, achieving relative SQ improvements of 11.1% for traffic signs and 20.7% for general objects. Furthermore, a substan- tial AQ gain of 26.1% is observed in the cyclist category.”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0789

- Claim: CFM 的核心机制主张：六方向偏移乘积构成的 focus feature 在实例几何中心自然达到最大并向边界衰减，该 center-peaked 分布作为类高斯软约束，比硬边界偏移对鱼眼畸变导致的空间抖动耐受得多——把监督焦点从易受扰动的边界转移到稳定中心是畸变鲁棒的关键设计。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 6, Section IV-B.2
- Evidence: 作者在 IV-B.2 论证 δp 的中心峰值性质并以实例级归一化保证尺度不变；Fig. 9 的 SFF 热图可视化提供定性支撑。
- Quote: “This “center-peaked” distribution acts as a Gaussian-like soft constraint, which is far more tolerant to the spatial jitter caused by fisheye distortion than hard boundary offsets.”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0791

- Claim: FEL 把 LSS 式 2D-to-3D 提升从针孔假设改写为 MEI 统一投影模型下的球面过程：引入镜面参数 ξ 显式建模到偏移单位球的投影，为宽 FoV 占据预测提供更有表达力的几何基础——代表'在提升模块内原生建模鱼眼几何'而非'先矫正图像'的技术路线。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 6, Section IV-C
- Evidence: IV-C 陈述针孔提升模型的失效与 FEL 的改写方式；式(3)-(6) 给出从归一化图像坐标到单位球向量的完整推导链；其效果由 Table II 的 Fisheyes 对照（C06）支撑。
- Quote: “To bridge this geometric gap, we propose Fisheye-based Enhanced Lifting (FEL), which reformulates the lifting process using the Unified Projection Model (MEI) [7]. By incorporating a mirror parameter ξ, FEL explicitly models the projection onto a displaced unit sphere, providing a more expressive geometric foundation for wide-FoV occupancy prediction.”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0793

- Claim: CFM 组件消融（Occ3D-Waymo，12/24 epochs 控制）：实例级归一化（A）单独把 OccSQ 总体从 29.99 提至 30.16，加监督 focus feature（B）提至 30.67，全量训练 30.80；B 组件对 general objects 增益最大（15.51→17.88→20.15，full-train 19.62），construction cones 在 full-train 达 14.18——两组件互补，监督 focus feature 是小尺度类别增益的主要来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 8, Table III
- Evidence: Table III 四行消融配置（✗✗/✓✗/✓✓/full-train）逐列给出；12 epochs 控制使组件归因不被训练量差异混淆（full-train 行单独标注）。
- Quote: “✗ ✗ 29.99 14.96 44.00 40.46 11.78 15.51 10.62 14.02 2.68 5.43 ✓ ✗ 30.16 14.27 44.27 40.03 12.57 17.88 11.21 14.89 2.71 4.91 ✓ ✓ 30.67 16.22 45.12 40.71 12.92 20.15 10.65 14.06 2.72 5.73 full-train 30.80 15.28 44.87 40.79 11.13 19.62 14.18 18.90 3.19 5.79”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0901

- Claim: 作者动机：360° 成像单次拍摄即可捕获完整球面环境，支持整体场景理解，应用指向虚拟现实与自主系统（autonomous systems）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 1, Section 1 Introduction
- Evidence: 引言开篇句给出 360° 成像的能力定位（单拍完整球面环境）与应用方向（VR 与自主系统）。
- Quote: “Unlike traditional perspective images, 360 ∘ imagery captures a complete spherical environment in a single shot, enabling holistic scene understanding and broad applications in virtual reality and autonomous systems.”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0902

- Claim: 方法设计：RePer-360 把全景适配重构为畸变感知自调制——不做互补投影特征的直接融合，而是通过对齐跨域特征分布的归一化调制来适配全景畸变，同时避免覆写或破坏预训练透视先验。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 3, Section 3 Methodology (overview)
- Evidence: 第 3 节方法论开篇明确 Rather than performing direct feature fusion 的设计转向：归一化调制 + 先验保留。
- Quote: “To this end, we propose RePer-360, a distortion-aware self-modulation framework for panoramic monocular depth estimation. Rather than perform- ing direct feature fusion, RePer-360 aligns cross-domain feature distributions via normalization-based modulation, thereby adapting to panoramic distortions while avoiding overwriting or damaging pretrained perspective priors.”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0903

- Claim: 数据效率：RePer-360 仅用先前方法约 1% 的训练数据（1k 对 120k 图像对）即超越此前 state of the art；在同等训练数据规模下，RMSE 相对改进最高达 22.4%。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 3, Section 1 Introduction (contributions)
- Evidence: 引言贡献段给出两个量化锚点：1k vs 120k（约 1%）与同规模下 RMSE 最高 22.4% 相对改进。
- Quote: “RePer-360 achieves high data efficiency and superior accuracy: using only ∼1% of the training data of prior methods (1k vs. 120k image pairs), it surpasses the previous state of the art; under the same training data scale, it improves RMSE by up to 22.4% relatively.”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0904

- Claim: Matterport3D in-domain 主表：RePer-360 达 Abs Rel 0.0691 / RMSE 0.3164，优于直接 in-domain 训练的 PanDA-L（0.0788 / 0.3827）与『120K 半监督预训练 + in-domain 微调』协议的 PanDA-L*（0.0717 / 0.3305）；表注明确训练协议不同，Δ 行给出对 PanDA-L 公平对比的相对改进：Abs Rel 12.3%、Sq Rel 32.2%、RMSE 17.3%。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 11, Table 1 (Matterport3D block)
- Evidence: Table 1 Matterport3D 区块 + 表注：PanDA-L*/PanDA-L/Ours 三行与 Δ 行逐值给出；表注说明协议差异，正文的 fair comparison 段给出 12.3%/17.3%。
- Quote: “Note that the training protocols differ: PanDA-L* was first pre-trained using semi-supervised learning on 120K panoramic images and then fine-tuned on in-domain data, whereas our method and all other baselines were trained directly on in-domain data only. Dataset Method Abs Rel ↓ Sq Rel ↓ RMSE ↓ 𝛿 1 ↑ 𝛿 2 ↑ 𝛿 3 ↑ Matterport3D [7] BiFuse [25] 0.2048 - 0.6259 84.52 93.19 96.32 UniFuse [14] 0.1063 - 0.4941 88.97 96.23 98.31 BiFuse++ [26] - - 0.5190 87.90 95.17 97.72 PanoFormer [23] - - 0.3635 91”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0905

- Claim: Stanford2D3D in-domain 主表：RePer-360 达 Abs Rel 0.0580 / RMSE 0.2474，优于 PanDA-L（0.0881 / 0.3185）与 PanDA-L*（0.0609 / 0.2540）；Δ 行对 PanDA-L 公平对比的相对改进为 Abs Rel 34.2%、Sq Rel 30.5%、RMSE 22.3%。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 11, Table 1 (Stanford2D3D block)
- Evidence: Table 1 Stanford2D3D 区块：PanDA-L*/PanDA-L/Ours 三行与 Δ 行逐值给出。
- Quote: “PanDA-L* [6] 0.0609 - 0.2540 96.82 99.05 99.52 PanDA-L 0.0881 0.0550 0.3185 93.42 98.26 99.33 RePer-360 (Ours) 0.0580 0.0382 0.2474 97.37 98.89 99.35 𝛥 34.2% 30.5% 22.3% 4.22% 0.64% 0.02%”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0906

- Claim: 零样本泛化：仅用合成数据（Structured3D + Deep360）训练时，RePer-360 在 Stanford2D3D 上 Abs Rel 改进 42.3%、RMSE 改进 14.0%（相对 PanDA-L）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 10, Section 4.2 Quantitative Results
- Evidence: 第 4.2 节正文给出零样本设定（合成数据训练）与 S2D3D 上 42.3%/14.0% 的相对改进。
- Quote: “The zero-shot generalization results in Table 2 further validate our advantages under the same synthetic-data training regime (Structured3D and Deep360 only), with improvements of 42.3% in Abs Rel and 14.0% in RMSE on Stanford2D3D.”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0908

- Claim: 架构消融（Matterport3D 统一训练配置）：完整几何感知调制（Index d，SCAdaLN + GAG 引导）RMSE 0.3164 最优；显式交互设计显著更差——cross-attention 变体 0.4549、无条件退化基线 0.3846/0.4638；用 UniFuse CEE 替换 GAG 为 0.3244；完全融合设计（UniFuse 无调制）大幅跌至 0.6032——多分支融合不足以弥合投影域差。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 14, Table 3
- Evidence: Table 3 架构消融全表：a-d 四种条件 + ECCLoss/注意力/融合变体行，统一冻结 backbone、数据与优化策略。
- Quote: “- ✗ None None ✗ 0.3846 0.0915 0.0525 92.25 98.53 a ✗ GAG PanoAttn ✓ 0.4638 0.1158 0.0790 86.80 96.80 b ✗ GAG CrossAttn ✓ 0.4549 0.1168 0.0763 87.15 97.17 c ✓ ERP PanoAttn ✓ 0.3206 0.0698 0.0390 95.66 99.03 c ✓ CP PanoAttn ✓ 0.3227 0.0692 0.0388 95.58 99.03 d ✓ GAG PanoAttn ✓ 0.3164 0.0691 0.0388 95.67 99.07 - ✓ GAG PanoAttn ✗ 0.3249 0.0716 0.0396 95.17 99.04 - ✓ GAG NormalAttn ✓ 0.3209 0.0725 0.0393 95.43 99.01 - ✓ UniFuse PanoAttn ✓ 0.3244 0.0731 0.0412 94.93 99.04 - ✗ UniFuse None ✓ 0.6032 0.1”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0909

- Claim: 损失消融（补充材料 Table 8）：去一致性损失 Abs Rel 0.0716 / RMSE 0.3249；随机 patch 采样的 EPNL 为 0.0731 / 0.3180（Abs Rel 反而略差于无一致性损失）；结构化的 cubemap 域 ECCLoss 最优 0.0691 / 0.3164——结构化、几何一致的监督优于随机局部约束。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 23, Table 8 (Supplementary B.4)
- Evidence: Table 8 损失策略对比：三行数值完整给出 EPNL 混合结果（RMSE/δ 改善但 Abs Rel 略差）与 ECCLoss 全优。
- Quote: “w/o Consistency Loss 0.0716 0.3249 0.9517 w/ EPNL [6] 0.0731 0.3180 0.9548 w/ ECCLoss (Ours) 0.0691 0.3164 0.9567”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0914

- Claim: 真实世界定性验证：作者用 DJI Osmo 360 消费级全景相机自采基准外的多样室内外场景（含夜间），RePer-360 比 PanDA-L 产生更连贯的深度预测、更好保持结构布局与更清晰边界；样例无 GT，仅为定性结果。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 25, Section B.7 and Figure 13 (Supplementary)
- Evidence: 补充材料 B.7：自采样例说明与定性结论；图 13 展示室内外与夜间对比。
- Quote: “We further present qualitative results on self-collected panoramic images captured using a DJI Osmo 360 camera. These samples are collected outside the benchmark datasets and cover diverse real-world indoor and outdoor scenes. As shown in Fig. 13, RePer-360 produces more coherent depth predictions than PanDA-L across diverse scenes. It better preserves structural layout and clearer boundaries in both indoor and outdoor environments, including challenging nighttime cases.”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0937

- Claim: 方法设计：PanoAffordanceNet 端到端框架，以畸变感知谱调制器（DASM）做纬度依赖的校准、以全环球面稠密化头（OSDH）从稀疏激活恢复拓扑连续，并通过像素级、分布级、区域—文本对比三级约束，在低监督下有效抑制语义漂移。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 1, Abstract
- Evidence: 摘要方法段：DASM 纬度校准、OSDH 拓扑连续恢复、三级约束抑制语义漂移。
- Quote: “We propose PanoAffordanceNet, an end-to-end framework featuring a Distortion-Aware Spectral Modulator (DASM) for latitude- dependent calibration and an Omni-Spherical Densification Head (OSDH) to restore topological continuity from sparse activations. By integrating multi-level constraints comprising pixel-wise, distributional, and region-text contrastive objectives, our framework effectively suppresses semantic drift under low supervision.”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0938

- Claim: 数据集贡献：作者构建 360-AGD——首个带精确交互区域标注的全景 affordance grounding 数据集，此前无公开基准支持全景室内场景的交互 affordance 接地。Easy Split 约 800 张（源自 360-Indoor 与 Gibson，原始分辨率约 512×1024，相对干净简单室内场景），Hard Split 约 1,200 张（源自 PanoContext 与 Sun360，最高 4552×9104，视觉复杂度与保真度更高）；标注覆盖 19 个 affordance 类，采用关键点监督策略——标注者在所有有效（非遮挡）交互区域内布点，经高斯核生成每类概率热图，重度遮挡且边界模糊的区域被忽略。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 5, Section IV (360-AGD: Established Dataset)
- Evidence: 第 IV 节全段：首个数据集声明 + Easy/Hard 双分裂来源与规模（约 800/约 1,200）+ 19 类 + 关键点—高斯核软监督 + 遮挡忽略规则。
- Quote: “Existing affordance datasets [13, 23] mainly target standard-view 2D images or 3D point clouds, and no public benchmark currently supports interactive affordance ground- ing in panoramic indoor scenes. To bridge this gap, we introduce 360-AGD, the first dataset with precise annotations of interaction regions in panoramic images. This benchmark is designed to evaluate model generalization and robustness across indoor environments of diverse complexity. Data Collection. To build a benchmark capabl”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0940

- Claim: 机制（DASM 纬度自适应补偿）：针对 ERP 引起的频率失衡——赤道附近保留锐利边缘、极区结构被拉伸——对高/低频两支路做定向补偿：高频增强模块（HFEM）锐化赤道区域的交互边界同时抑制极区被放大的伪影；低频稳定模块（LFSM）在极区附近维持全局结构一致性以缓解拉伸造成的语义碎片化。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 4, Section III-C (Distortion-Aware Spectral Modulator)
- Evidence: 第 III-C 节：ERP 频率失衡描述 + HFEM/LFSM 分支职责。
- Quote: “To address ERP-induced frequency imbalance, where sharp edges are preserved near the equator but structures are stretched at the poles, we apply targeted compensation to each branch: the High-Frequency Enhancement Module (HFEM, Fig. 2(c)) sharpens the interaction boundaries in equatorial regions while suppressing artifacts amplified at the poles; the Low-Frequency Stabilization Module (LFSM, Fig. 2(d)) maintains global structural consistency near the poles to mitigate semantic fragmentation from”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0941

- Claim: 机制（OSDH 球面稠密化）：为在球面流形上恢复拓扑连续，OSDH 以视觉自相似性为结构归纳偏置——将精化视觉特征投影到单位超球面构建余弦亲和矩阵，经 top-k 选高置信种子、置信图噪声抑制后，以种子传播式 A_refined = A_init + α·max_j(S_ij·C_j)（α 为可学习残差标量）把稀疏激活稠密化为完整连贯的功能区域。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 4, Section III-D (Spherical-Aware Hierarchical Decoder) and Figure 3
- Evidence: 第 III-D 节 OSDH 段 + 式(5)-(7)：球面投影、亲和矩阵、种子传播公式与可学习残差标量。
- Quote: “visual self-similarity as a structural inductive bias (detailed in Fig. 3). Specifically, we project the refined visual features F ′′ v onto the unit hypersphere and construct a symmetric affinity matrix S ∈ R L×L via cosine similarity: S ij = (f ′′ v,i · f ′′ v,j )/(∥f ′′ v,i ∥∥f ′′ v,j ∥). (5) Simultaneously, high-confidence seeds K are selected via top-k. Spurious noise is suppressed with a confidence map: C = Sigmoid((A init − μ A )/(σ A /T )) , (6) Max Pool Spherical Projection B”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0942

- Claim: 主结果（360-AGD，one-shot，指标 KLD↓/SIM↑/NSS↑）：Easy Split 上 Ours 1.270/0.506/4.490 vs OOAL 2.868/0.117/1.267、OS-AGDO 2.853/0.124/1.299；Hard Split 上 Ours 1.306/0.474/4.398 vs OOAL 3.067/0.097/1.484、OS-AGDO 2.965/0.115/1.484——KLD 约降一半以上，SIM 约 4 倍，NSS 约 3 倍，两个难度分裂上全指标一致领先。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 6, Table I (a)
- Evidence: Table I(a) 全量数值：两基线 + Ours 在 Easy/Hard 两分裂上的三元组指标。
- Quote: “TABLE I: Quantitative comparison across different domains. Top: Performance on our proposed 360-AGD dataset. Bottom: Generalization results on the perspective AGD20K dataset [13]. (a) Evaluation on the Proposed 360-AGD Dataset Method Supervision Easy Split Hard Split KLD↓ SIM↑ NSS↑ KLD↓ SIM↑ NSS↑ OOAL [9] One-shot 2.868 0.117 1.267 3.067 0.097 1.484 OS-AGDO [35] One-shot 2.853 0.124 1.299 2.965 0.115 1.484 Ours One-shot 1.270 0.506 4.490 1.306 0.474 4.398”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0944

- Claim: 组件消融（360-AGD Hard Split）：各组件提供渐进且可区分的收益——LoRA 参数高效适配带来初始性能提升（任务特定特征调优的必要性）；DASM 的集成为几何扭曲提供关键修正、显著降低 KLD 误差；OSDH 补充精化空间一致性、从稀疏激活恢复拓扑连续；完整模型取得最佳整体表现（1.306 KLD、0.474 SIM），印证模块化设计针对全景 affordance 预测的独特挑战有效。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 6, Section V-D (Effects of Model Components) and Table II
- Evidence: 第 V-D 节 Effects of Model Components 段 + Table II：三组件各自职责 + 完整模型最佳数值。
- Quote: “Effects of Model Components. As shown in Table II, each component provides incremental but distinct gains. The introduction of LoRA-based parameter-efficient adaptation yields an initial performance boost, demonstrating the neces- sity of task-specific feature tuning. Notably, the integration of Distortion-Aware Spectral Modulator (DASM) provides a critical correction for geometric warping, significantly reducing the KLD error. Furthermore, Omni-Spherical Den- sification Head (OSDH) complements”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0945

- Claim: 损失消融（360-AGD Hard Split，Table III）：单项损失配置最弱（1.596 KLD/0.395 SIM/3.891 NSS）；两项损失配置居中（1.430–1.459 KLD）；完整三级损失（像素级 BCE + 分布级 KL + 区域—文本对比 RTC）取得最强配置 1.306/0.474/4.398——像素、分布、语义三层监督的协同效应得到验证。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 6, Table III and Section V-D (Effects of Training Objectives)
- Evidence: Table III 五行损失配置数值 + 第 V-D 节 Effects of Training Objectives 叙述（BCE 基线难从稀疏标注捕获功能形状、KL 引入分布级监督、RTC 消歧特征）。
- Quote: “TABLE III: Ablation study of loss components on the 360-AGD Hard Split. We investigate the impact of the L KL , L RTC and L BCE . L KL L RTC L BCE KLD ↓ SIM ↑ NSS ↑ ✓ 1.596 0.395 3.891 ✓ ✓ 1.459 0.442 4.374 ✓ ✓ 1.430 0.450 4.041 ✓ ✓ 1.331 0.493 4.361 ✓ ✓ ✓ 1.306 0.474 4.398”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0947

- Claim: 超参鲁棒性（OSDH top-k，Table V）：方法在 top-k∈[5, 20] 宽区间内高度稳定——KLD 仅波动 0.006（1.306→1.312），SIM 近乎恒定；鲁棒性源于 OSDH 以球面自相似为结构先验并配合置信引导噪声抑制，无需精细调种子阈值即可从稀疏激活可靠恢复拓扑连续功能区——显著提升真实部署实用性。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 7, Table V and Section V-E (Robustness to Top-k Selection)
- Evidence: 第 V-E 节 Robustness to Top-k Selection 段：区间稳定性数值 + 机制归因 + 部署实用性结论。
- Quote: “Robustness to Top-k Selection. We further examine the sensitivity of the OSDH module to the top-k value. Table V shows that our method exhibits remarkable stability across a wide range of top-k ∈ [5, 20]: KLD fluctuates by only 0.006 (from 1.306 to 1.312), while SIM remains nearly constant. This robustness stems from OSDH’s integration of spherical self-similarity as a structural prior, coupled with a confidence-guided noise suppression mechanism, enabling reliable recovery of topologically cont”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0948

- Claim: 真实具身场景（可穿戴 360° egocentric）：作者构建可穿戴采集系统——将 Insta360 X4 全景相机安装在头戴帽上，模拟具身智能体的 360° egocentric 视角；在复杂办公与家居场景中，模型在光照变化与严重几何畸变下仍准确局部化关键功能区域（如 sit 与 display），为服务机器人的全局决策与任务规划提供可靠功能先验。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: pages 7-8, Section V-F (Performance in Real-World Scenarios) and Figure 6
- Evidence: 第 V-F 节 + Fig 6：可穿戴采集设定（Insta360 X4 + 头戴帽）+ 办公/家居定性结果 + 服务机器人动机。
- Quote: “we build a wearable data collection system by mounting an Insta360 X4 panoramic camera on a head- mounted cap to simulate the 360 ◦ egocentric perspective ## page 8 display sit (a) (b) Fig. 6: Real-world evaluation. (a) Wearable data collection setup. (b) Qualitative grounding results. of an embodied agent. In complex office and domestic scenarios, our model accurately localizes key functional regions (e.g., sit and display), despite varying illumination conditions and severe geometric disto”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0950

- Claim: 实现细节与全景特定增强：视觉编码器用 ImageNet 预训练的 DINOv2-Base，文本编码器用预训练 CLIP；AdamW（初始 lr 1e-5、余弦退火）、2×NVIDIA A6000、20k 迭代、batch size 4；全景输入统一 resize 到 560×1120。增强除常规翻转/颜色抖动外，引入全景特定增强——±3° 随机旋转、±5% 随机缩放、水平环绕平移（horizontal wraparound shifts），以强化 360° 拓扑固有的旋转不变性；训练时对二值标注掩码施加高斯模糊得到软监督热图。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 5, Section V-A (Experimental Setup, Implementation Details)
- Evidence: 第 V-A 节 Implementation Details：骨干/优化器/算力/分辨率 + 全景特定增强清单。
- Quote: “Implementation Details The visual encoder adopts a DINOv2-Base model [27] pre-trained on ImageNet, while the text encoder uses a pre-trained CLIP model [29]. The model is trained end-to-end using the AdamW optimizer with an initial learning rate of 1e−5 and a cosine annealing schedule. Training is performed on two NVIDIA A6000 GPUs for a total of 20k iterations with a batch size of 4. All panoramic inputs are uniformly resized to a resolution of 560×1120. To enhance robustness, in addition to st”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-1134

- Claim: OmniVLN 的多模态感知模块通过融合旋转 LiDAR 与全景鱼眼相机（panoramic fisheye cameras）的数据实现 360° 时空一致的感知，生成跨机器人平台的高保真语义点云，作为其空中与地面 VLN 框架的感知前端。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 3, Fig. 2 caption, Section III
- Evidence: 框架总览图（Fig. 2）说明多模态感知模块融合旋转 LiDAR 与全景鱼眼相机数据实现 360° 时空一致性，生成跨平台高保真语义点云；引言与贡献 1 同样以旋转 LiDAR+全景相机为跨平台全向感知前端。
- Quote: “The Multimodal Perception module (left) achieves 360 ◦ spatio-temporal consistency by fusing data from a rotating LiDAR and panoramic fisheye cameras, enabling the generation of high-fidelity semantic point clouds across robotic platforms.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1135

- Claim: 作者指出，窄视场感知在实际中每步只暴露局部场景，受限视角设置常导致重复旋转、侧方或后方目标发现延迟、以及探索搜索中的拓扑理解碎片化——这是本文引入全向感知的直接动机。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 1, I Introduction
- Evidence: 引言第一挑战：现有 VLN 系统基于窄 FoV 观测，受限视角导致重复旋转、侧/后方目标发现延迟与拓扑碎片化，在杂乱遮挡室内更严重并跨房间累积误差。
- Quote: “In practice, this limited-view setting often causes repeated rotations, delayed discovery of side- or rear-located targets, and fragmented topological understanding during exploration and search.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1137

- Claim: 全景语义的获取方式：640×1920 全景流经 Grounded SAM 与 SAM2 提取开放词汇分割 mask，3D 点经等距柱状（equirectangular）投影映射到全景像素坐标并查询 mask 获得标签，从而把全景图像语义与 LiDAR 几何耦合为 DSG 构建的输入。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 3, III-A, Fig. 3
- Evidence: III-A 说明全向语义感知使用 640×1920 全景流，Open-vocabulary mask 由 Grounded SAM/SAM2 提取，3D 点经 equirectangular 投影到全景像素坐标 (u,v) 查询 mask 标签。
- Quote: “For omnidirectional semantic awareness, we utilize a 640 × 1920 panoramic stream I t . Open-vocabulary masks M t are extracted via Grounded SAM [22] and SAM2. As shown in Fig. 3, each point P t = (x, y, z) ∈ P map is mapped to panoramic pixel coordinates (u, v) through equirectangular projection:”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1138

- Claim: 在真实三房间 IoT 实验室 44 个测试对象的指称表达生成（REG）任务上，分层 DSG 表示相对非分层平铺对象列表将整体准确率从 77.27% 提升至 93.18%（+15.91 个百分点），其中视角相关（VD）空间关系推理从 68.18% 提升至 90.91%（+22.73 个百分点）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 5, Table I, Section IV-A.2
- Evidence: Table I：Non-Hierarchical (Uniform Flat) VI 86.36%/VD 68.18%/Overall 77.27%；Hierarchical (Ours) VI 95.45%/VD 90.91%/Overall 93.18%；Improvement +9.09%/+22.73%/+15.91%。作者归因于 DSG 剪枝搜索空间、消除平铺基线的跨房间空间幻觉。
- Quote: “Non-Hierarchical (Uniform Flat) 86.36% 68.18% 77.27% Hierarchical (Ours) 95.45% 90.91% 93.18% Improvement +9.09% +22.73% +15.91%”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1139

- Claim: 在 50 对象的全局记忆层合成场景 D9 中，基于 DSG 的分层摘要将累积 token 消耗从 3555.98 降至 1067.62（缩减 69.98%），作者称该缩减通过防止上下文溢出同时保持必要拓扑感知来支撑建筑级可扩展性。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 6, Section IV-B.2; page 7, Table II
- Evidence: IV-B.2：50 对象密度下基线需 3555.98 token，DSG 摘要仅 1067.62 token，69.98% 缩减；Table II 显示九个数据集全部缩减且随密度增大（D1 0.25% 到 D9 69.98%）。
- Quote: “At a density of 50 objects, the baseline requires 3555.98 tokens, whereas our DSG-based summary uses only 1067.62 tokens. This 69.98% reduction facilitates building-scale scalability by preventing context overflow while preserving essential topological awareness.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1140

- Claim: 在全局记忆层最高密度合成场景 D9 中，平铺列表基线的导航成功率退化至 16%，而分层方法通过把远端房间摘要为拓扑节点保持 80% 的 SR；周边层（D4-D6）两种方法均达 100%，中央层（D1-D3）分层方法 100% vs 基线 D3 降至 80%。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 6, Section IV-B.3, Fig. 7
- Evidence: IV-B.3 与 Fig. 7：foveal tier 分层 100% vs 基线 D3 80%；peripheral tier 两者 100%；global memory tier 差距最大，D9 平铺基线 16% vs 分层 80%，作者归因于长坐标列表消歧复杂性。
- Quote: “The global memory tier (D7-D9) exhibits the largest performance gap. The flat-list baseline degrades to 16 percent SR in D9 due to the complexity of disambiguating long co- ordinate lists. By summarizing distant rooms into topological nodes, our method maintains an 80% SR in D9, validating hierarchical abstraction as a reliable cognitive heuristic for long-horizon navigation.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1141

- Claim: 在高密度场景的实证测试中，多分辨率提示把平均单步决策响应时间从 12.4s 降至 3.8s（作者称约 3 倍加速），并称该加速对四足部署至关重要——过慢的推理会导致里程计漂移与安全风险。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 6, Section IV-B.4
- Evidence: IV-B.4：把空间排序交给 10ms 内零 token 的 Python 几何引擎后，高密度场景平均响应时间从 12.4s 降到 3.8s，约 3 倍加速，对四足部署（延迟致里程计漂移与安全风险）关键。
- Quote: “Empirical tests in high-density scenarios demonstrate a reduction in average response time from 12.4s to 3.8s per decision compared to the flat-prompt baseline. This 3x speedup is critical for quadruped deployment, where excessive latency causes odometry drift and safety hazards.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1142

- Claim: 作者强调：octant 表示构建自全向感知与持久 DSG 记忆而非单一窄 FoV 图像，因此邻近的侧向与后方候选对象无需重复探索性旋转即可持续供规划器使用。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 4, Section III-C.1
- Evidence: III-C.1 说明 octant 表示基于全向感知+持久 DSG 记忆而非单张窄 FoV 图像，侧/后方候选无需重复探索旋转即可供规划器使用；近处节点保留实例级细节，远处压缩为房间/功能组摘要。
- Quote: “Importantly, the octant representation is built from omnidi- rectional perception and persistent DSG memory rather than a single narrow-FoV image, so nearby side and rear candidates remain available to the planner without requiring repeated ex- ploratory rotations.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1143

- Claim: 在同一机器人轨迹、环境与语义建图管线下，旋转 LiDAR 配置在语义图中实例化 85 个对象节点，固定 LiDAR 配置仅 61 个；作者将差距归因于旋转扫描对侧向与部分遮挡区域覆盖的改善，并确认全向主动扫描缓解感知滞后、减少有限传感器视场导致的拓扑碎片化。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 7, Section IV-D, Fig. 9
- Evidence: IV-D：同一轨迹/环境/管线对比旋转 vs 固定 LiDAR，85 vs 61 对象节点；Fig. 9 显示旋转配置在侧向与部分遮挡区域覆盖显著改善；作者据此确认全向主动扫描缓解感知滞后与拓扑碎片化。
- Quote: “Under the same robot trajectory, environment, and semantic mapping pipeline, the rotating LiDAR configuration provides substantially more complete omnidirectional observa- tions than the fixed LiDAR setting. Specifically, the rotating system instantiates 85 object nodes in the resulting semantic map, whereas the fixed LiDAR configuration identifies only 61 object nodes along the same path.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1144

- Claim: 该框架在空中与地面机器人上验证：定位使用 FAST-LIO，机载模块负责感知与 DSG 构建，而 LLM 推理经 WiFi 离机（offboard）进行——全向感知与建图在机载，重推理在云端。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 6, Section IV-C
- Evidence: IV-C 开头说明验证设置：FAST-LIO 定位覆盖空中与地面机器人，机载模块管理感知与 DSG 构建，LLM 推理经 WiFi 离机处理，分层提示传输给远端模型、返回命令解析为平台特定 setpoint。
- Quote: “OmniVLN validation uses FAST-LIO [28] for localization across aerial [29] and ground robots. Onboard modules man- age perception and DSG construction, while LLM reasoning is handled offboard via WiFi.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1145

- Claim: 空中平台集成 PX4 自驾仪与 MINCO 轨迹优化器，四足平台使用 Unitree SDK 与 FAR 局部规划器做避碰运动；两个平台共享统一推理管线，平台特定修改仅限于低层控制与局部规划模块。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 7, Section IV-C
- Evidence: IV-C 平台细节：PX4+MINCO（空中）、Unitree SDK+FAR（四足），共享统一推理管线，平台差异限于低层控制与局部规划；作者称此模块化设计使异构机器人以最小改动复用推理栈。
- Quote: “The aerial platform integrates the PX4 autopilot [30], and MINCO [31] trajectory optimizer. The quadruped uses the Unitree SDK and FAR local planner [32] for collision-aware motion. Both systems share a unified reasoning pipeline, with platform-specific modifications limited to low-level control and local planning modules.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-0121

- Claim: 在自建的 PAP-12K 全景可供性基准上，免训练的 PAP 管线取得 gIoU 71.56、cIoU 62.30、P@50 75.49、P@50:95 64.97（推理约 10 秒），对次优基线 A4-Agent 的绝对提升为 +9.01 gIoU 与 +12.33 cIoU。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 10, Section 5.2 Overall Performance; Table 2 (page 8)
- Evidence: 正文 S5.2 逐字给出 PAP 四项指标与相对 A4-Agent 的 gIoU/cIoU 绝对增益；page 8 Table 2 给出全部方法完整数值与推理时间，两者互相印证。
- Quote: “Specifically, PAP achieves a gIoU of 71.56% and a cIoU of 62.30%, surpassing the second-best method, A4-Agent, by absolute margins of 9.01% and 12.33%, respectively.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0124

- Claim: 在集中体现全景特有难点的 Hard 子集（掩码占全图 >30% 或 <0.1%、或被 ERP 左右边界截断，约占 30% 样本）上，PAP 对 A4-Agent 的优势进一步扩大：gIoU 60.35 vs 42.75（+17.60）、cIoU 52.59 vs 36.42（+16.17）、P@50:95 52.17 vs 30.38（+21.79）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 10, Table 3; Section 5.2 Performance on Different Difficulty Levels
- Evidence: Table 3 Hard/Normal 分层显示 PAP 的优势在 Hard 子集最大；正文给出四项绝对增益，说明方法确实针对全景特有难点而非平均情况。
- Quote: “Notably, in theHardsubset, our method exhibits an even more pronounced advantage, outperforming the second-best method (A4-Agent) by absolute margins of 17.60% and 16.17% in terms of gIoU and cIoU.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0125

- Claim: 消融显示自适应注视（球面到透视重投影）是无训练域适配的关键：去掉 AG、直接在裁剪 ERP 区域上运行 OVD+SAM 时，gIoU 从 72.69 降到 64.99（-7.70）、cIoU 从 63.85 降到 55.43（-8.42）；作者据此论证 ERP 空间畸变对 2D 基础模型先验构成严重域偏移。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 11, Table 5; Section 5.3 Impact of Adaptive Gaze
- Evidence: Table 5 的 w/o AG 与 w/ AG 对比直接量化了畸变域偏移的代价与重投影的收益，是"如何用全景相机"这一应用方式问题的核心机制证据。
- Quote: “w/o AG 64.99 55.43 68.43 56.37 w/ AG 72.69 63.85 76.29 66.13 ∆ 7.70 8.42 7.77 9.76”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0129

- Claim: 论文转引的证据表明 360° 视觉对多种具身任务有益：导航/SLAM 中无需频繁重定向即可稳定跟踪路标并建图（360ORB-SLAM 等）、操作任务能力显著增强（Eye-Robot, Kerr et al. 2025）、精确定位（360Loc）、以及与 MLLM 结合的全向空间推理问答（360-R1 等），达到针孔系统无法匹敌的环境完整性。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 3, Section 2 Related Work, Panoramic Vision paragraph
- Evidence: Related Work 的 Panoramic Vision 段集中转述了全景输入在四类具身任务上的既有收益证据，为综述的跨任务获益判断提供文献线索。
- Quote: “In Embodied Intelligence, this omnidirectional capability effectively eliminates blind spots. For autonomous navigation and SLAM, it allows agents to maintain stable tracking of landmarks and build consistent maps without frequent reorientation (Chen et al., 2024; Wang et al., 2025b). Beyond navigation, 360◦ visual inputs significantly enhance an agent’s ability in manipulation tasks (Kerr et al., 2025) and facilitate precise localization (Huang et al., 2024a).”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0130

- Claim: PAP-12K 全部全景图由 Insta360-X5 原生 360° 相机实拍（非多视拼接或合成渲染）：三脚架稳定加延时拍摄消除人体遮挡，随机改变三脚架高度使不同仰角物体呈现不同程度的赤道畸变以模拟真实机器人视点，每场景以不同角度/高度/物体布局拍摄 2–4 张。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 5, Section 3.3 Dataset Construction, Panoramic Image Collection
- Evidence: S3.3 详述采集协议：设备型号、稳定与去人手段、随机高度带来的畸变多样性，是综述中"全景相机如何进入具身数据生产"的硬件侧证据。
- Quote: “All panoramic images were captured using the Insta360-X5, a state-of-the- art professional high-resolution panoramic camera that can capture images at 12K resolution. To ensure high fidelity and simulate realistic robot viewpoints, we employed a professional tripod for stabilization and utilized delayed shooting to eliminate human obstruction from the field of view.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0131

- Claim: PAP-12K 是首个"全景+可供性"数据集：1,003 张 12K（11904×5952）全景图、6,103 个标注实例、13,493 条可供性问答，覆盖 12 类室内场景；Table 1 显示现有可供性数据集全部为针孔成像（FoV 约 30–70°），现有全景数据集则多来自多视拼接或合成渲染且无可供性标注。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 5, Section 3.2 Dataset Statistics; Table 1 (page 4)
- Evidence: S3.2 给出数据集规模与场景分布，Table 1 系统对比既有可供性/全景数据集，确立 PAP-12K 的"原生 360° 相机+可供性标注"独特定位。
- Quote: “In total, the dataset comprises 1,003 ultra-high-resolution panoramic images, 6,103 annotated object instances, and 13,493 affordance-related questions.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0021

- Claim: 在同一冻结 DINOv2-B backbone 的受控消融中，把位置编码换为 FishRoPE (θ,φ) 使 WoodScape 鱼眼 2D 检测达到 54.2 mAP，高于 2D Axial RoPE 的 52.5 mAP 与学习式绝对 PE 的 51.8 mAP。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 6, Table 3
- Evidence: Table 3 在同 backbone 下对比五种位置编码，FishRoPE (θ,φ) 在检测列取得最高 mAP，几何适配的增益独立于 backbone 选择。
- Quote: “Learned absolute PE 51.8 59.2 Sinusoidal 2D PE 52.1 59.6 2D Axial RoPE [5] 52.5 61.4 FishRoPE (θonly) 53.6 64.7 FishRoPE (θ, ϕ)54.2 65.1”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0022

- Claim: 在 SynWoodScapes BEV 语义分割上，FishRoPE (DINOv2-B + FishRoPE) 达到 65.1 mIoU，高于同 backbone 下 2D RoPE 变体的 61.4 mIoU，也超过使用更大 DINOv2-L backbone 的 FishBEV 的 64.22 mIoU。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 6, Table 2
- Evidence: Table 2 显示 FishRoPE 完整方法在 SynWoodScapes 上为 65.1 mIoU，对比同表内 F2BEV 53.39、FishBEV 64.22 与自身 2D RoPE 变体 61.4。
- Quote: “F2BEV [20] R-18 53.39 † FishBEV [1] DINOv2-L 64.22 § FishRoPE (R-18 + FishRoPE) R-18 56.8 FishRoPE (DINOv2-B + 2D RoPE) DINOv2-B 61.4 FishRoPE (DINOv2-B + FishRoPE) DINOv2-B65.1”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0023

- Claim: 消融显示 θ-only 变体已捕获鱼眼径向结构的绝大部分，加入方位角 φ 通过编码方位关系再带来 +0.6 mAP（检测）与 +0.4 mIoU（BEV 分割）的增益。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 6, Section 4.4
- Evidence: Section 4.4 正文对 Table 3 的解读：θ-only 捕获大部分径向结构，加 φ 带来进一步小幅增益。
- Quote: “The θ-only variant captures most of the radial structure; adding ϕ provides a further +0.6 mAP / +0.4 mIoU by encoding azimuthal relationships.”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0024

- Claim: 同用 FishRoPE 时，冻结 DINOv2-B（可训练 LoRA+头约 12.4M 参数）在两个任务上均超过常规训练的 Swin-T（29M 参数）：检测 54.2 vs 52.9 mAP，BEV 分割 65.1 vs 59.8 mIoU，作者据此认为冻结 VFM + LoRA 为鱼眼感知提供强于常规 backbone 的特征。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 6, Table 4
- Evidence: Table 4 的 backbone 消融显示 DINOv2-B 在两任务上均为最优，且以更少可训练参数超过 Swin-T。
- Quote: “Backbone Params mAP↑mIoU↑ Swin-T [15] 29M 52.9 59.8 DINOv2-S ∗ [16] 8.1M 53.4 62.7 DINOv2-B ∗ [16] 12.4M54.2 65.1 ∗Frozen; params = trainable LoRA + head only.”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0081

- Claim: UMI-3D 沿用 UMI 的腕装鱼眼相机方案并把视场进一步加宽到约 185°（M12 镜头系统），并直接使用未经去畸变的原始鱼眼图像作为策略观察输入，以在腕部快速运动与视角持续变化下扩大可观察区域，同时保留中心分辨率、紧凑编码周边上下文。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 5, Section III-A, design principle HD2
- Evidence: 硬件设计原则 HD2 明确说明：UMI-3D 跟随 UMI 已验证的宽 FoV 鱼眼成像方案，采用更宽的约 185° 鱼眼相机与 M12 镜头，并像 UMI 一样直接使用原始鱼眼图像（不去畸变），在扩大可观察区域的同时保留中心分辨率并紧凑编码周边上下文。
- Quote: “In UMI-3D, we further extend this approach by using a wider FoV fisheye camera (approximately 185°) through an M12 lens system, expanding the observable region (see Fig. 2). As in UMI, we directly use raw fisheye im- ages without undistortion, preserving central resolution while compactly encoding peripheral context.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0082

- Claim: UMI-3D 的宽 FoV 鱼眼设计使相机视场与腕装 LiDAR 视场大幅重叠，确保视觉与几何观测对应于工作区的重叠区域，从而为一致的 LiDAR-相机多模态感知提供基础。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 5, Section III-A, design principle HD2
- Evidence: 作者把“与 LiDAR 视场大幅重叠”列为宽 FoV 设计的直接收益之一：视觉与几何观测覆盖重叠的工作区区域，为一致多模态感知（LiDAR-相机融合）奠定基础。
- Quote: “Beyond improving visual coverage, the wide-FoV design also enables substantial overlap with the LiDAR field of view, providing a foundation for consistent multimodal perception by ensuring that visual and geometric observations correspond to overlapping regions of the workspace.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0085

- Claim: 在三个对视觉 SLAM 高度挑战的代表性场景（无纹理白墙、强光照变化下的可变形窗帘、含铰接物体与动态遮挡的长时序操作）中，UMI-3D 的 LiDAR-centric SLAM 在全部场景下保持稳定、抗漂移的位姿估计并产生一致的 3D 地图重建（论文为定性展示，未报告相对真值或视觉 SLAM 的定位误差定量对比）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 12, Section V, Robust SLAM for Reliable Data Collection
- Evidence: 作者用 Fig. 10 的三个场景定性评估 SLAM 鲁棒性，声明在所有场景中保持稳定与抗漂移的位姿估计及一致地图重建；正文未给出定位误差数值，也未与视觉 SLAM 做定量对照。
- Quote: “As shown in Fig. 10, we evaluate SLAM performance in three representative challenging scenarios: a textureless white wall, a deformable curtain under strong lighting variation, and a long-horizon manipulation task in- volving articulated objects and dynamic occlusions. These conditions are known to be highly challenging for vision- based SLAM due to lack of texture, large non-rigid motion, and drastic illumination changes. Across all scenarios, UMI- 3D maintains stable and drift-resistant pose e”
- Authors: ziming-wang

### LR-FISHEYE-2026-0086

- Claim: 在拉窗帘任务（大型可变形物体；769 条 UMI-3D 演示训练的扩散策略，DINOv2 ViT-L/14 编码器；评估覆盖强光照与背光条件）上，策略在三种窗帘类型上分别取得 0.88、0.90、0.96 的归一化分数（共 120 次评估 trials），并在显著的光照与外观变化下保持稳健的抓取与拉拽行为。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 13, Section V-B, Performance (Fig. 12)
- Evidence: Fig. 12 及正文给出三种窗帘的归一化分数 0.88/0.90/0.96 与稳健性结论。作者在 Discussion（page 13）进一步说明：该任务中腕装相机视野大部分被动态、低纹理的窗帘运动与强光照变化占据，使纯视觉 SLAM 的位姿估计不可行，而学到的策略在训练与部署时都只依赖视觉输入。
- Quote: “As shown in Fig. 12, the policy achieves strong performance across all curtain types, with normalized scores of 0.88, 0.90, and 0.96, respectively. The system remains robust under significant variations in lighting and appearance, demonstrating reliable grasping and pulling be- haviors for deformable objects.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0087

- Claim: 在杯碟摆放任务（3,500 条 UMI-3D 演示；评估全部在未见环境，8 杯×8 碟共 64 个物体组合、每组合 10 trials、共 640 次评估）上，已见物体对的平均归一化分数为 0.863，部分未见（杯或碟未见）降至 0.788，完全未见组合为 0.736，呈平缓的性能退化。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 13, Section V-A, Generalization Performance (Fig. 11)
- Evidence: 作者报告了按物体组合可见性分层的泛化结果：seen 0.863、partially unseen 0.788、fully unseen 0.736，并据此认为策略泛化超出对特定物体实例的记忆。
- Quote: “For seen object pairs, the average normalized score reaches 0.863. Under partial distribution shift (either cup or saucer unseen), performance decreases moderately to 0.788, and further to 0.736 in fully unseen scenarios.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0091

- Claim: 用原始 UMI 系统训练的预训练策略（来自数据 scaling laws 的先前工作）未经任何微调直接部署到 UMI-3D 硬件上，在未见环境的 4 鼠标×4 鼠标垫共 16 个物体组合、每组合 5 trials（共 80 trials）上取得 0.73–1.00 的归一化分数。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 14, Section V-D, Cross-Embodiment Performance (Fig. 14)
- Evidence: Fig. 14 及正文给出 0.73–1.00 的分数范围。紧接着的句子（跨 page 14-15）说明：尽管硬件配置与传感模态不同，策略在未见环境保持稳定的抓取与放置；作者在 page 15 Discussion 据此认为 UMI-3D 与原 UMI 保持紧密对齐的视觉观察空间，并推测两代数据可联合训练以通过数据 scaling 提升策略性能。
- Quote: “the policy achieves consistently strong performance across all object combinations, with normalized scores ranging from 0.73 to 1.00.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0093

- Claim: UMI-3D 的宽 FoV 鱼眼设计直接沿袭 UMI 及其引用的鱼眼相机经验研究（arXiv:2603.02139）——两者被引证为“宽 FoV 鱼眼成像能在操作中维持任务相关观测”的设计依据。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 5, Section III-A, design principle HD2
- Evidence: 该引用关系表明 UMI 生态中“腕装宽 FoV 鱼眼”已成为被显式经验研究支撑的设计惯例，UMI-3D 是其延续与加宽（185°）。
- Quote: “Following UMI, which demonstrates the effectiveness of wide-FoV fisheye imaging for maintaining task-relevant observations during manipulation [4, 33], we adopt a similar design.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0094

- Claim: UMI-3D 为腕装 LiDAR-鱼眼多模态感知开发了专门的 LiDAR-相机外参标定模块 livox2cam，其设计（扫描模式无关的边缘提取、补偿光斑边缘膨胀的椭圆拟合、多帧联合优化）被作者称为应对固态 LiDAR 不规则采样与鱼眼光学强非线性畸变的关键。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 6, Section III-B, SP2.2
- Evidence: 该标定模块基于带四个圆孔与基准标记的标定板提取跨模态 3D-3D 对应，SVD 闭式解外参；鱼眼内参另用 equidistant 投影模型标定（page 6, SP2.1），支撑像素-射线映射、ArUco 检测与空间一致裁剪。
- Quote: “To further improve robustness under practical sensing con- ditions, the proposedlivox2cammodule incorporates (i) scan- pattern-agnostic edge extraction for sparse and non-repetitive LiDAR measurements, (ii) ellipse-based fitting to compensate for spot-induced edge dilation, and (iii) multi-frame joint optimization for enhanced geometric consistency. These de- signs are critical for handling the irregular sampling of solid- state LiDAR (Fig. 5C(ii)) and the strong nonlinear distortion introduced”
- Authors: ziming-wang

### LR-FISHEYE-2026-0286

- Claim: 在 robomimic 仿真三任务（square/can/lift）上，用多相机伪演示训练显著优于单相机训练（所有 N=10/25/50 设置一致）：例如 can 任务 N=10 时，单视角成功率 0.18，五视角（base 动作空间）0.32（78%↑）、相机动作空间 0.37（105%↑）；square N=25 从 0.26 升至 0.42（base，62%↑）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 5, Table I
- Evidence: Tab. I 报告了三种视角数量（1/3/5）×三种动作空间下全部设置的成功率，正文总结“multi-camera training significantly outperforms single-camera training in all the scenarios, even achieving double success rates in some settings”。
- Quote: “TABLE I: Camera View Scaling-Up Results in Simulation Environments. Training View Space Square Can Lift N = 10 N = 25 N = 50 N = 10 N = 25 N = 50 N = 10 Cam F Base 0.14 0.26 0.42 0.18 0.54 0.72 0.69 Cam F , Cam F L , Cam F R Base 0.16 (14%↑) 0.31 (19%↑) 0.47 (12%↑) 0.27 (50%↑) 0.63 (17%↑) 0.78 (8%↑) 0.79 (14%↑) Camera 0.17 (21%↑) 0.29 (12%↑) 0.47 (12%↑) 0.30 (67%↑) 0.68 (26%↑) 0.83 (15%↑) 0.76 (10%↑) Cam F , Cam F L , Cam F R Cam F U , Cam F D Base 0.18 (29%↑) 0.42 (62%↑) 0.55 (31%↑) 0.32 (78%↑)”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-0287

- Claim: 作者报告在大多数情况下，用五个相机训练比用三个相机取得明显更好的性能，反映了继续增加相机视角的扩展收益。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 4, Section IV-B, Q1
- Evidence: Q1 段的结论句：training with five cameras achieves notably better performance than training with three cameras in most cases，与 Tab. I 中 5 视角行普遍高于 3 视角行一致。
- Quote: “Additionally, training with five cameras achieves notably better performance than training with three cameras in most cases. This further reflects the benefits of scaling up camera views in imitation learning.”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-0289

- Claim: 用五视角伪演示训练的策略可自然泛化到推理期不同相机视角：can 任务上五视角训练的策略在 Cam_F/Cam_F_L/Cam_F_U 推理视角下分别得 0.37/0.68、0.30/0.66、0.37/0.77（N=10/25）；而单视角训练策略换到 Cam_F_L/Cam_F_U 时崩溃至 0.00/0.07 与 0.01/0.05。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 6, Table IV
- Evidence: Tab. IV 对比五视角训练与单视角训练策略在三种推理视角下的成功率；正文总结 our policy achieves stable performance over several different camera view inputs, which allows more flexibility in the camera setup in the deployment。
- Quote: “TABLE IV: Camera View Generalization in the Inference. Training View Inference View Can N = 10 N = 25 Five Views Cam F 0.37 0.68 Cam F L 0.30 0.66 Cam F U 0.37 0.77 Single View Cam F 0.18 0.54 Cam F L 0.00 0.07 Cam F U 0.01 0.05”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-0290

- Claim: 单视角策略可在推理期通过多视角动作聚合免费获益：can 任务 N=10 时，三视角训练+三视角聚合推理达 0.39，高于三视角训练+单视角推理的 0.30 与单视角基线的 0.18；square N=25 从 0.29 升至 0.33。各视角输入独立并行处理，聚合在 GPU 上高度并行，额外延迟低。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 7, Table V
- Evidence: Tab. V 给出三种训练/推理组合在 square/can 六个设置下的成功率；正文指出 using three views in the deployment can improve the model performance compared with using a single fixed view，且并行处理降低聚合延迟。
- Quote: “TABLE V: Multiview Composition with Single-View Policy. Training View Inference View Square Can N = 10 N = 25 N = 50 N = 10 N = 25 N = 50 Cam F Cam F 0.14 0.26 0.42 0.18 0.54 0.72 Cam F , Cam F L , Cam F R Cam F 0.17 0.29 0.47 0.30 0.68 0.83 Cam F , Cam F L , Cam F R 0.18 0.33 0.51 0.39 0.73 0.85”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-0295

- Claim: 视角扩展在演示采集阶段几乎零额外人工：每条专家演示仍只需一次执行，多台相机同步录制即可把每条演示扩展为 V 个伪演示（N·V 训练样本）；推理可保持单相机部署。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 3, Section III-B
- Evidence: 方法节声明 scaling up camera views adds negligible extra effort in expert demonstration collection process since each expert demonstration still requires only a single execution；部署节声明模型面向单视角输入、无需多相机部署。
- Quote: “It is worth mentioning that scaling up camera views adds negligible extra effort in expert demonstration collection process since each expert demonstration still requires only a single execution.”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-1044

- Claim: RobotPan 的应用方式：在人形平台 Tiangong 3.0 上用六台相机的环视 rig（而非多鱼眼全景 rig）实现 360° 视觉；作者明确说明因硬件约束六相机光学中心无法共置，经典多鱼眼拼接管线不适用，必须用几何感知的视图合成来获得环视画面。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 1, Section 1 Introduction
- Evidence: 引言指出多鱼眼全景 rig 近似单一光心故可拼接，而本系统相机受硬件约束无法共置，经典图像拼接管线不可用，需要有原理的几何感知视图合成。
- Quote: “Unlike multi-fisheye panoramic rigs that approximate a sin- gle optical center, our cameras cannot be co-located due to hardware constraints, which makes classical image-stitching pipelines inapplicable and requires principled geometry- aware view synthesis. Meanwhile”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1045

- Claim: 具身人机回路（遥操作、数据采集、紧急接管）中窄视场前视相机的问题陈述：受限视场降低态势感知，操作者需以不舒服的身体/头部旋转去“搜索”视点；机器人传感布局与人眼差异导致 HMD 视图不稳定并引发模拟器眩晕。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 1, Section 1 Introduction
- Evidence: 引言逐条列出前视相机受限视场的三个实际问题：态势感知受限、需要不舒服的体位搜索视点、多相机切换打断工作流；摘要同时指出运动诱发抖动导致 HMD 模拟器眩晕。
- Quote: “First, the limited field of view of a forward-facing camera restricts situational awareness: operators cannot reliably perceive surrounding obstacles or affordances, which constrains safe motion and often requires uncomfortable body/head rota- tions to “search” for viewpoints.”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1046

- Claim: 环视 rig 硬件配置：六台向外 RGB 相机均匀分布在半径 89 mm 的圆环上，方位角 0°/±60°/±120°/180°，每台相机水平视场 118°、垂直视场 92°；配合头顶 40 线激光雷达（水平 360°、垂直 59°）提供多模态数据。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 6, Section 3.1 Experimental Setup (Fig. 4/5; 40-beam LiDAR 描述延续至 page 7 首段)
- Evidence: 3.1 节传感器布局段给出圆环半径、六个方位角、每相机 118°×92° 视场与 40 线 LiDAR 覆盖，并称该几何保证稳健的多视重叠。
- Quote: “they are positioned at 0 ◦ (front), ±60 ◦ (front- left/right), ±120 ◦ (back-left/right), and 180 ◦ (rear). Cou- pled with each camera’s wide horizontal field of view of 118 ◦ and vertical field of view of 92 ◦ , this geometry guar- antees robust, multi-view visual overlap.”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1047

- Claim: RobotPan 数据集规模与构成：339 个同步片段、每片段 200 帧，六 RGB 相机 + 一台 LiDAR 联合标定同步采集，覆盖室内（办公/家庭/展厅/厂房）与室外（街区/园区/道路）场景，约 80% 片段含动态/非刚性内容，RGB 分辨率 1920×1536（训练下采样到 518×406），按 80/10/10 划分。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 7, Section 3.1 RobotPan dataset
- Evidence: 3.1 节数据集段给出片段数、帧数、场景类型、动态占比、分辨率与划分比例。
- Quote: “Our dataset contains 339 synchronized clips, each with 200 frames, captured with a calibrated rig consisting of six RGB cameras and one LiDAR. The sequences cover diverse indoor environments (office build- ings, households, exhibition halls, and factories) and outdoor environments (urban blocks, industrial parks, and roads). All sensors are time-synchronized and jointly calibrated, enabling consistent multi-view and multi-sensor geometry. The RGB cameras record at a resolution of 1920×1536, and”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1048

- Claim: 在 RobotPan 自建数据集 4 视角稀疏新视图合成上，ROBOTPAN 以 327K 高斯取得最佳三项渲染指标（PSNR 24.70、SSIM 0.811、LPIPS 0.197），高斯数比每像素一高斯方法少 3.86×、比 pixelSplat（多高斯每像素，3,783K）少 11.57×；最佳前基线 DepthSplat 为 1,261K/22.97/0.787/0.200。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 8, Table 3 与 Section 3.3 Comparison 段
- Evidence: Table 3 与正文给出本方法与 pixelSplat/MVSplat/FLARE/DepthSplat 的对比及 3.86×/11.57× 紧凑性倍数。
- Quote: “DepthSplat [34] Pixel-wise 1,261K 22.97 0.787 0.200 Ours Spherical voxel-wise 327K 24.70 0.811 0.197 TABLE 4 Quantitative comparison with state-of-the-art novel view synthesis methods on the DL3DV-Benchmarks and RealEstate10K datasets. Method DL3DV-Benchmarks RealEstate10K PSNR↑ SSIM↑ LPIPS↓ PSNR↑ SSIM↑ LPIPS↓ pixelSplat [26] 16.55 0.456 0.480 25.89 0.858 0.142 MVSplat [27] 18.13 0.559 0.393 26.39 0.869 0.128 FLARE [12] 18.89 0.591 0.352 27.39 0.873 0.107 DepthSplat [34] 19.24 0.620 0.322 27.47”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1051

- Claim: 流式新视图合成：在 10 个动态子场景（每场景 200 帧 × 6 视角=1,200 图像）上，流式变体取得 28.59 dB PSNR、每帧更新仅 0.47 s、渲染 230 FPS、存储 7.2 MB，全面优于在线基线（IGS 27.75 dB/3.65 s/204 FPS/6.5 MB；3DGStream 26.11 dB/12.25 s/215 FPS/7.8 MB）与离线基线（Spacetime-GS 25.41 dB）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 9, Table 5 与 Section 3.4 Comparison 段（26×/33×/7.8× 训练加速表述在 page 10）
- Evidence: Table 5 与正文报告与离线（K-Planes/4DGS/Spacetime-GS）和在线（StreamRF/3DGStream/IGS）方法的 PSNR/训练时间/渲染速度/存储对比。
- Quote: “Ours (Streaming) 28.59 0.47 230 7.2 Metrics and baselines. Following prior work [64], we report PSNR, Storage usage, Training time, and Rendering speed for comparison with previous approaches. For online training methods, the first-frame observations are used to initialize the scene representation, and the subsequent frames are in- corporated incrementally through per-frame updates. In this setting, we compare against StreamRF [63], 3DGStream [54], and IGS [64]. For offline training methods, all”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1052

- Claim: 高斯预测范式消融：球面体素式预测把表征从像素式的 1,261K 高斯/378 MB 压缩到 327K/97 MB，同时把 PSNR/SSIM/LPIPS 从 21.43/0.713/0.341 提升到 24.70/0.811/0.197；笛卡尔体素式居中（439K/130 MB/23.12/0.791/0.236）——球面近细远粗层级与机器人中心场景几何最匹配。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 10, Table 6 与 Section 3.5 Ablation 段（约 70% 存储削减的表述在 page 4, Section 2.3）
- Evidence: Table 6 对比像素式/体素式/球面体素式三种高斯预测范式；正文明确给出 1261K→327K、378 MB→97 MB 与指标提升。
- Quote: “Pixel-wise 1261K 378 21.43 0.713 0.341 Voxel-wise 439K 130 23.12 0.791 0.236 Spherical voxel-wise 327K 97 24.70 0.811 0.197 TABLE 7 Ablation study of key design choices on the proposed dataset for streaming novel view synthesis over 200 evaluation frames. Configuration #Gaussians Storage (MB)↓ PSNR↑ SSIM↑ LPIPS↓ Naive Concatenation (w/o MLP) 65,400K 19,400 24.66 0.806 0.201 w/o Range-Image Fusion 3,094K 1,371 24.71 0.812 0.213 w/o Tiny-MLP Refinement 3,023K 872 24.32 0.739 0.241 Full Model 3,023”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1053

- Claim: 流式融合消融：朴素拼接跨帧预测会在 200 帧评测中把表征膨胀到 65,400K 高斯、19,400 MB 存储，尽管渲染质量尚可（PSNR 24.66）但对长序列不可行；完整模型为 3,023K/1,296 MB/25.12/0.832/0.184；去掉距离图像融合（3,094K/1,371/24.71/0.812/0.213）或去掉 tiny-MLP 精修（3,023K/872/24.32/0.739/0.241）均降低质量。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 10, Table 7 与 Section 3.5 Streaming fusion 段
- Evidence: Table 7 报告朴素拼接/去距离图像融合/去 tiny-MLP/完整模型四配置的高斯数、存储与渲染指标；正文明确称朴素拼接 impractical。
- Quote: “Naive Concatenation (w/o MLP) 65,400K 19,400 24.66 0.806 0.201 w/o Range-Image Fusion 3,094K 1,371 24.71 0.812 0.213 w/o Tiny-MLP Refinement 3,023K 872 24.32 0.739 0.241 Full Model 3,023K 1,296 25.12 0.832 0.184 tion scheme, the scene representation allocates Gaussians more efficiently across space, allowing us to model the scene with a smaller number of Gaussians while preserving reconstruction fidelity. This compact representation further reduces computational rendering overhead and contribut”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1057

- Claim: 度量一致性的实现方式：为满足 SLAM 与闭环控制等下游任务对度量一致场景的要求，作者用 LiDAR 监督微调几何预测器，把预测点图对齐到每个相机坐标系下的 LiDAR 度量几何；训练损失含 LiDAR 稀疏尺度感知点损失与 π3 伪法线损失。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 4, Section 2.2 末段（训练损失细节在 page 5, Section 2.5）
- Evidence: 2.2 节末与 2.5 节说明 LiDAR 监督微调与四项训练目标（MSE/LPIPS 渲染损失+LiDAR 点损失+法线损失）。
- Quote: “Finally, to ensure metric consistency, we fine- tune the geometry predictor with LiDAR supervision, align- ing the predicted point maps to LiDAR-derived metric ge- ometry in each camera frame; training details are provided in Sec. 2.5.”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1058

- Claim: 数据采集协议：训练/评估数据由人佩戴与机器人同构的头戴式采集系统采集（操作者平均身高约 160 cm 以匹配人形平台传感器高度），并加颈部稳定器抑制头部诱发运动、执行保守运动剖面——步速限制 ≤1.2 m/s、转向速度 ≤0.4 rad/s 以保证数据一致性。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 7, Section 3.1 Data collection 段（Fig. 5 在 page 6）
- Evidence: 3.1 节数据采集段给出穿戴 rig、身高匹配、颈部稳定器与限速协议。
- Quote: “Data are recorded by human operators (average height ∼160 cm) wearing the rig on the head to match the sensor height of the target humanoid platform. We further add a neck stabilizer to reduce head- induced motion and enforce conservative motion profiles during capture: walking speed is limited to ≤ 1.2 m/s and turning speed to ≤ 0.4 rad/s for data consistency.”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1170

- Claim: 作者定位：鱼眼镜头因超宽视场（>90°，常见 120° 或 180°）与少量采集即可高效覆盖场景，是自动驾驶、机器人与沉浸式 VR 的基石输入；但其严重径向畸变与非线性投影违反原始 3DGS 的针孔假设，直接套用会产生伪影与性能退化。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 2, Section 1 Introduction
- Evidence: 引言：3DGS 擅长针孔相机，直接用于鱼眼图像面临关键限制；鱼眼是自动驾驶、机器人、沉浸式 VR 的基石（超宽 FoV>90°，常见 120°/180°，少量采集高效覆盖）；严重径向畸变与非线性投影违反针孔假设，naive 应用产生伪影与性能退化。
- Quote: “its direct application to fisheye images-a cor- nerstone of autonomous driving, robotics, and immersive VR due to ultra-wide FOV ( >90°, the common ones are 120° or 180°) and efficient scene coverage with fewer cap- tures—faces critical limitations. Fisheye lenses’ severe ra- dial distortion and nonlinear projection violate pinhole as- sumptions of the original 3DGS, causing artifacts and per- formance degradation when naively applied.”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1172

- Claim: DirectFisheye-GS 将 Kannala-Brandt 鱼眼投影模型嵌入 3DGS 管线，实现原生鱼眼图像直接训练、无需去畸变预处理，同时保持栅格化渲染效率、与现有 3DGS viewer 和商业工具的完全兼容，并保留相邻光线间的原始空间关系（多视图一致性约束的必要条件）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 2, Section 1 Introduction
- Evidence: 引言方法段：整合 KB [14] 投影模型消除 undistortion 预处理、保持栅格化效率；确保与现有 3DGS viewer/商业工具完全兼容；保留相邻光线空间关系。page 3 Section 2.2 指出 3DGUT 虽平衡精度与泛化但破坏 3DGS 完全显式架构、训练结果与现有 viewer 和商业管线不兼容；page 6 Section 5.1 确认本文结果可用原始 SIBR Viewer 查看。
- Quote: “We integrate the Kannala-Brandt [14] fisheye projection model into the 3DGS pipeline, eliminating the need for undistortion pre- processing and preserving the efficiency of rasterization- based rendering. This not only ensures full compatibility with existing 3DGS viewers and commercial tools, but also retains the original spatial relationships among neighbor- ing rays—an essential condition for multi-view consistency constraints.”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1174

- Claim: 机理与玩具实验（附录 C）：大畸变（大入射角）区域的投影 Jacobian 呈强视图依赖的各向异性，导致跨视图梯度不平衡；图像中心处 Jacobian 平滑退化为针孔情形、优化更稳定且近各向同性。三个等半径球用三个高斯拟合多视图鱼眼图像的玩具实验中，中心高斯在优化中保持各向同性尺度，外周（蓝色）高斯被非线性视图依赖梯度拉成不稳定极端形变。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 13, Appendix Section C, Fig. 7
- Evidence: 附录 C：反传中 3D 协方差梯度 ∇Σ=(WJθ)ᵀ(∇Σ2D)(WJθ) 被鱼眼模型的非线性 Jacobian 直接调制（式 7 的 Jθ 是相机坐标高度非线性函数，含 θd、θ′d 与径向距离/深度高阶项，已核对）；大入射角区强视图依赖各向异性→不平衡梯度，中心平滑退化为针孔；Fig. 7 玩具实验给出中心 vs 外周高斯的对照。
- Quote: “In regions with large distortion (i.e., large incident angles), the Jacobian exhibits strong view-dependent anisotropy, leading to unbalanced gradients across views. In contrast, near the image center the Jacobian smoothly degenerates toward the pinhole case, resulting in more stable and nearly isotropic optimization. We further illustrate this effect with a toy experiment (Fig. 7). Three spheres with identical radii are rendered into multiple fisheye images and fitted using three Gaus- sian pri”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1175

- Claim: CVO 设计：利用 3DGS 初始化所依赖的 COLMAP SfM 稀疏点云天然编码的跨图像特征对应——Step 1 按共享 SIFT 特征数为每张图像排序近邻相机、构建特征重叠关联图；Step 2 对图中每对相机计算位姿角度差并降序排序（max angle association graph）；训练时每次迭代随机选主视图并从图中取其 top-(batchsize−1) 关联相机——该策略同时平衡特征重叠与角度多样性。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 5, Section 3.3 Cross-View Joint Optimization
- Evidence: Section 3.3 两步实现（SIFT 共享特征数 + 位姿角度差降序）与逐迭代主视图+top-(N-1) 采样；Algorithm 1（page 6）给出 L1+SSIM 损失累计回传伪代码；batchsize=2（page 6 Section 4.3）；设计目标是 Shared Gaussian Optimization 与 Multi-View Consistency（page 4-5）；不依赖 COLMAP 本身（page 12 Section B 声明可换 VGGT）。
- Quote: “Step 1: Camera Association. Construct a feature-overlap graph for each image, ranking neighboring cameras by shared SIFT feature counts (→ camera association graph) . Step 2: Angular Divergence Sorting. For each camera pair in the camera association graph , compute their pose angular difference and sort them in descending order (→ max angle association graph). During training, we iteratively sample a primary view and select its top-batchsize−1 correlated cameras from the graph. This strategy bal”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1176

- Claim: FisheyeNeRF 数据集（train view）六场景平均：原始 3DGS 把鱼眼当针孔直接训练全面崩溃（SSIM 0.6124/PSNR 18.8454/LPIPS 0.5228）；DirectFisheye-GS 达 SSIM 0.8284/PSNR 26.2522/LPIPS 0.2295，超过去畸变输入+鱼眼渲染的 3DGS*（0.8240/25.5382/0.2431）、Fisheye-GS**（0.8183/25.1783/0.2658）与 3DGUT（0.8020/25.2837/0.3290）——原生输入优于去畸变管线，作者据此说明相机建模正确且 undistortion 不可避免丢失场景信息。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 7, Table 1
- Evidence: Table 1（train view）六场景平均行：3DGS 0.6124/18.8454/0.5228（各场景最低）→ 3DGS* 0.8240/25.5382/0.2431 → Fisheye-GS** 0.8183/25.1783/0.2658 → 3DGUT 0.8020/25.2837/0.3290 → Self-Cali-GS 0.7460/24.0084/0.4507 → Ours 0.8284/26.2522/0.2295；page 6 Section 5.1 正文：3DGS 无法处理鱼眼图像每格最低，undistortion 后训练再鱼眼渲染 'our method achieves superior or comparable results in all cases'，证明 undistortion 不可避免丢失信息。
- Quote: “3DGS 0.6355 19.8407 0.5273 0.5306 18.0784 0.5122 0.6491 19.3742 0.5388 0.5412 18.1212 0.5362 0.6842 19.8638 0.5045 0.6338 17.7938 0.5179 0.6124 18.8454 0.5228 3DGS* 0.8587 26.9129 0.2223 0.8108 26.6751 0.2129 0.8356 26.4027 0.2502 0.8187 24.5977 0.2140 0.8163 25.6968 0.2666 0.8036 22.9437 0.2924 0.8240 25.5382 0.2431 Fisheye-GS** 0.8593 26.9145 0.2245 0.8230 26.8117 0.2242 0.8384 26.9748 0.2604 0.8022 24.4500 0.2285 0.8223 24.9219 0.2888 0.7643 20.9969 0.3681 0.8183 25.1783 0.2658 3DGUT 0.8200 2”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1179

- Claim: Den-SOFT 大尺度真实场景：户外无界场景 Ruziniu 上 DirectFisheye-GS 显著领先——train view SSIM/PSNR/LPIPS 0.8225/24.0154/0.2140 vs 3DGUT 0.7500/22.2100/0.3400（PSNR +1.81dB）；test view 0.8006/22.7404/0.2222 vs 3DGUT 0.5230/19.8780/0.4380（PSNR +2.86dB，且 3DGUT test SSIM 崩至 0.5230）；室内 Coffee 场景同样最优（train PSNR 27.3528 vs 3DGUT 25.7450）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 8, Table 3
- Evidence: Table 3（Den-SOFT train+test）：Ours 在 Ruziniu/Coffee 全部口径最优；3DGUT 在 Ruziniu test SSIM 0.5230 接近崩溃、Fisheye-GS** train SSIM 仅 0.5965/0.5843、Self-Cali-GS 全面落后；page 6 Section 5.1 正文：无界户外场景光照剧变、细节丰富使其他方法局限更严重，'on an outdoor scene like Ruziniu, our method significantly outperforms others'（已核对）。
- Quote: “3DGUT 0.7500 22.2100 0.3400 0.8830 25.7450 0.3310 Self-Cali-GS 0.5224 19.7540 0.5969 0.8873 22.9550 0.2460 Ours 0.8225 24.0154 0.2140 0.9105 27.3528 0.2181 Test View SSIM↑ PSNR↑ LPIPS↓ SSIM↑ PSNR↑ LPIPS↓ 3DGS* 0.7403 19.6615 0.2754 0.8740 24.0067 0.2488 Fisheye-GS** 0.5843 19.9809 0.4523 0.8664 24.6196 0.2731 3DGUT 0.5230 19.8780 0.4380 0.8770 24.9090 0.3390 Self-Cali-GS 0.5072 19.5411 0.6024 0.8629 21.4954 0.2729 Ours 0.8006 22.7404 0.2222 0.8815 24.9305 0.2299”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1180

- Claim: 鱼眼图像边界区（正文 Section 5.2 界定为超过 60° FoV 的边缘区域）PSNR（Den-SOFT）：加 CVO 后 Ruziniu 从 23.0033 升至 23.7625、Coffee 从 26.2492 升至 27.3819，均超过 3DGUT（Ruziniu 22.2242、Coffee 25.8105）——CVO 在畸变最重的鱼眼边缘区有效且反超 SOTA。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 8, Table 4
- Evidence: Table 4（图像边界区 PSNR，Den-SOFT）：Ruziniu w/o CVO 23.0033 / w/ CVO 23.7625 / 3DGUT 22.2242；Coffee 26.2492 / 27.3819 / 25.8105；page 7 Section 5.2 正文：'CVO improves PSNR at the boundary (beyond 60° FOV) and outperforms 3DGUT'，强化鱼眼模型与 CVO 对图像边缘高斯的作用（已核对）。
- Quote: “Scene w/o CVO w/ CVO 3DGUT Ruziniu 23.0033 23.7625 22.2242 Coffee 26.2492 27.3819 25.8105”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1181

- Claim: CVO 迁移到针孔相机管线有效：Square2 场景 3DGS+CVO PSNR 30.9500/SSIM 0.9403/LPIPS 0.1420（原始 3DGS 30.5345/0.9354/0.1505；3DGS+random select 30.6498/0.9355/0.1491），Coffee 场景 27.5138/0.9033/0.2172（vs 27.2348 与 random select 反降至 26.2880）——跨视图联合优化不依赖鱼眼输入，对针孔 3DGS 同样改善且优于随机多视图采样。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 8, Table 7
- Evidence: Table 7（自采集针孔场景 Square2/Coffee）：3DGS → +random select → +CVO 的 SSIM/PSNR/LPIPS 对比，Coffee random select PSNR 反降（26.2880）；page 8 Section 5.2 正文：'This strategy can also be seamlessly integrated into the pinhole camera–based GS pipeline'、CVO 一致改善并超 random-selection；page 14 Supp Table 9（Tanks&Temples：drjohnson/playroom/train/truck 四场景同趋势，已核对）。
- Quote: “Method SSIM↑ PSNR↑ LPIPS↓ SSIM↑ PSNR↑ LPIPS↓ 3DGS 0.9354 30.5345 0.1505 0.9013 27.2348 0.2237 3DGS + random select 0.9355 30.6498 0.1491 0.8936 26.2880 0.2370 3DGS + CVO 0.9403 30.9500 0.1420 0.9033 27.5138 0.2172”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1183

- Claim: 计算成本（ScanNet++ 8d563fc2cc 场景，单张 NVIDIA A100）：DirectFisheye-GS 训练 0.395 小时、渲染 77 FPS——训练成本与 3DGUT（0.404 小时）相当，渲染更快（3DGUT 55 FPS），远优于 Self-Cali-GS（3.333 小时/31 FPS）；作者据此称在支持原生鱼眼输入的方法中同时取得最优重建质量与计算效率。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 14, Table 11, Appendix Section F
- Evidence: Table 11 对比三个支持原生鱼眼输入的方法（其余方法需预处理）；Section F：以 ScanNet++ 8d563fc2cc 场景为例，本方法同时取得最优重建质量（引 Table 2）与计算效率。
- Quote: “Method Ours 3DGUT Self-Cali-GS Training-Time (h) 0.395 0.404 3.333 Rendering-Speed (FPS) 77 55 31”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1270

- Claim: PanoAir 的应用方式：面向无人机的全景视觉惯性 SLAM——ERP 全景相机+IMU 输入，通过全景特征提取（混合特征+畸变感知加权）与全景优化、全景回环实现鲁棒、精确、全局一致的位姿估计，并在嵌入式平台部署验证实用性。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 1, Abstract and I. Introduction
- Evidence: 摘要与贡献列表给出框架三模块与 PC+嵌入式双平台验证声明；IV 节展开各模块设计。
- Quote: “To achieve accurate and robust pose estimation under such challenging UAV scenarios, we propose a panoramic VI- SLAM framework that exploits the omnidirectional FoV via the proposed panoramic feature extraction and panoramic loop closure, enhancing feature constraints and ensuring global con- sistency.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1271

- Claim: 任务动机与缺口：既有 VI-SLAM 主要依赖有限 FoV 传感器，在复杂 UAV 场景会导致漂移甚至失效；全景相机虽提供全向感知提升鲁棒性，但全景 VI-SLAM 与对应的真实 UAV 数据集仍欠探索。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 1, Abstract
- Evidence: 摘要问题定义段；引言进一步给出既有全景方法'或无度量尺度或无完整 SLAM'的两类缺口。
- Quote: “However, existing VI-SLAM methods mainly rely on sensors with limited fields of view (FoV), which can lead to drift and even failure in complex UAV scenarios. Although panoramic cameras provide omnidirectional perception to improve robustness, panoramic VI-SLAM and corresponding real-world datasets for UAVs remain underexplored.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1272

- Claim: 全景相机的硬件构成路径：多相机拼接配置采用少量超广角 FoV 鱼眼镜头（常背靠背布置），经等距柱状投影（ERP）实现全向 FoV，同时保持紧凑轻量设计——但基于该拼接配置的既有方法或无度量尺度或无完整 SLAM（不能校正长期累积误差），限制实际应用。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 1, Section I Introduction
- Evidence: 引言对全景硬件方案的分类描述；Table I 横向对比既有全景基准佐证数据缺口。
- Quote: “multi- camera stitching [14] configuration employ a small number of ultra-wide FOV fisheye lenses, often configured back-to-back, enabling an omnidirectional FOV through equirectangular pro- jection (ERP), while maintaining a compact and lightweight design”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1273

- Claim: 宽 FoV 视觉 SLAM 的三路径分类：单宽 FoV 相机（鱼眼/环形镜头，可超 180° 但无法全向覆盖）；多相机系统（重叠或非重叠 FoV 组合，但引入冗余传感器并需复杂标定）；紧凑全景相机（直接拍摄 ERP，实现 360°×180° 全向覆盖）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 2, Section II-A
- Evidence: II-A 节开头的三分法陈述；本文选择第三条路径的理由（全向覆盖+免多传感器标定）与另两路径缺点并列给出。
- Quote: “(a) Single wide-FoV cameras, such as fisheye cameras [1], [2], [31] and annular lenses [32], [33], can provide a FoV exceeding 180 ◦ . However, they still fail to offer full omnidirectional coverage.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1274

- Claim: 数据集规模与构成：17 条序列、累计 15.8 km、总时长 45 min，覆盖云/晴/夜三种光照（从光照充足到极暗），每种光照下含多种轨迹长度、飞行速度与机动模式（急速偏航、高度变化、飞行抖动）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 3, Section III-A
- Evidence: III-A 节数据统计；Table III 逐序列给出速度 2.9-10.0 m/s、长度 257-1901 m、时长 87-234 s。
- Quote: “Our dataset consists of a total of 17 sequences, covering a cumulative distance of 15.8 km with a total 45 minutes duration.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1275

- Claim: 采集硬件配置：Insta360 X3 全景相机安装于 DJI Matrice 300 RTK 无人机，以 30 fps 同步采集全景、前/后视鱼眼与针孔图像；内置 IMU 提供 1000 Hz 惯性测量；真值轨迹由 DJI D-RTK2 站以 5 Hz 记录（水平 1cm+1ppm RMS）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 3, Section III-B and Table II
- Evidence: III-B 节硬件与标定描述；Table II 汇总传感器参数（含加计/陀螺噪声密度与随机游走）。
- Quote: “Our dataset is collected using an Insta360 X3 [49] panoramic camera mounted on a DJI Matrice 300 RTK [50] UAV, capturing panoramic, front- and back-view fisheye, and pinhole images at 30 fps”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1277

- Claim: ERP 畸变的显式处理：ERP 投影在图像顶/底边界附近存在严重拉伸、易引入误匹配；本文基于 ERP 投影机制为每个特征推导畸变感知权重 σ=cos((v/IH−1/2)π)/η^l，特征越接近上下边界权重越低，显式降低畸变影响；该权重同时进入优化协方差矩阵。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 4, Section IV-A
- Evidence: IV-A-2 特征提取段给出式(3)与机制解释；IV-B-1 式(6)将 σ 进入协方差。
- Quote: “a distortion-aware weighting function is derived based on the ERP projection mechanism (Eq. (1)) for each feature”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1278

- Claim: UAV 基准总体效果：PanoAir 在自建 17 序列上取得 100% 成功率与全部条件最佳精度（平均 ATE 0.739 m），且提供度量尺度位姿；对比基线成功率：ORB-SLAM3 83%、VINS-Mono 59%、Droid-SLAM 76%、OpenVSLAM 94%（尺度对齐）、360DVO 100%（尺度对齐，平均 ATE 1.398 m）、360-VIO 59%、OpenVINS 88%。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 6, Section V-B and Table IV
- Evidence: Table IV 完整 17 序列×8 方法 ATE 矩阵+成功率列；正文 V-B-1 声明 100% 与 best accuracy。
- Quote: “Our method achieves a 100% success rate and achieves the best accuracy across all sequences, while provid- ing poses with metric scale.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1279

- Claim: 夜间低光+高机动场景归因：Night 条件低光与高机动（Seq12/14/16）下部分方法初始化失败或跟踪丢失；作者将 PanoAir 的稳定归因于全景相机的全向 FoV 提供更丰富的视觉信息与更多路标观测（相对鱼眼或针孔方法如 ORB-SLAM3 与 Droid-SLAM）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 6, Section V-B and Table IV
- Evidence: V-B-1 Night 场景分析段；Table IV Night 列显示 VINS-Mono/360-VIO 多序列失败、Ours 全部成功。
- Quote: “It can be attributed to the omnidirectional FOV of panoramic camera providing richer visual information with more landmark observed compared to the fisheye or pinhole method like ORB-SLAM3 and Droid-SLAM.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1281

- Claim: 公开基准（360-VIO 手持数据集）效果：为与视觉惯性里程计公平对比（关闭回环），PanoAir 在三条室内手持序列上取得最高成功率与精度——平均 ATE 0.145 m/RPE 0.073 m，优于 360DVO（0.307/0.068）、360-VIO（0.493/0.089）、ORB-SLAM3（0.209/0.087）；OpenVSLAM 与 VINS-Mono 在 Hard 序列失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 6, Section V-B and Table V
- Evidence: V-B-1 末段 + Table V 完整数值（部分基线结果引自原文）。
- Quote: “The results show that our method achieves the highest success rate and accuracy across three indoor handheld sequences.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1282

- Claim: 全景 FoV 的独占能力（反向回环）：得益于全向 FoV，全景回环不仅能从相同视角方向（Loop 2）检测回环，也能从相反方向（Loop 1）检测——这是针孔或鱼眼相机无法实现的；5.5 km 户外手持序列上该能力使系统能重新对齐起点与终点，实现全局一致估计。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 7, Section V-B and Fig. 4
- Evidence: V-B-2 定性结果段 + Fig.4 下部（Loop 1/Loop 2 标注）；Table VI 端点数值佐证回环校正效果。
- Quote: “Notably, benefit from the omnidirectional FoV, our panoramic loop closure detects loops not only from the same viewing direction (Loop 2), but also from opposite directions (Loop 1), which is not achievable with pinhole or fisheye cameras.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1283

- Claim: 大尺度场景对比（5.5 km 手持）：端到端学习方法 DROID-SLAM 显存溢出（GPU OOM）；ORB-SLAM3 与 360-VIO 明显漂移；OpenVSLAM 即使开启回环检测也无法校正单目尺度变化引起的漂移；PanoAir 无回环时漂移已最小，开启回环后成功对齐起点与终点。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 7, Section V-B
- Evidence: V-B-2 大尺度手持段 + Fig.4 下部轨迹对比。
- Quote: “The end-to- end learning-based method DROID-SLAM run out of GPU memory. ORB-SLAM3 and 360-VIO exhibit noticeable drift, while OpenVSLAM, even with loop detection enabled, fails to correct drift induced by monocular scale variations.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1284

- Claim: 回环校正的量化效果（手持对齐序列端点误差）：户外 5.5 km 序列起点终点对齐场景，无回环端点误差 (-9.92, -49.37, -28.43) m，开启全景回环后降至 (-1.39, -0.08, 0.36) m；室内 330 m 序列从 (-1.52, -0.53, -0.74) 降至 (-0.01, 0.00, 0.01) m。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 7, Section V-B and Table VI
- Evidence: Table VI 端点数值表；正文引述该表说明回环有效校正累积漂移。
- Quote: “Ours(Without Loop) -1.52, -0.53, -0.74 -9.92, -49.37, -28.43 Ours(With Loop) -0.01, 0.00, 0.01 -1.39, -0.08, 0.36”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1285

- Claim: 嵌入式部署效果：Jetson Orin NX 上以帧步进 3（10 Hz）运行，总跟踪耗时 114.2 ms（约 9 fps）vs PC 24.9 ms（40 fps）；平均 ATE 0.772 m vs PC 0.739 m，精度与 PC 相当；实际部署中高频位姿输出可由 IMU 积分+SLAM 校正融合获得，适配 UAV 与资源受限平台。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 7-8, Section V-C and Tables VII-VIII
- Evidence: V-C 嵌入式部署段 + Table VII（分模块运行时）+ Table VIII（PC vs Jetson ATE）+ Fig.5（箱线图）。
- Quote: “Our method achieves high-accuracy pose estimation on the edge device in real time (10 Hz frame rate), while maintaining accuracy comparable to PC implementation.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1286

- Claim: 全景回环的消融验证：去除全景回环后总体轨迹精度最差（平均 ATE 0.578→1.223 m，Cloudy 0.805→2.170、Sunny 0.566→1.087、Night 0.789→1.517），表明全景回环有效校正漂移；去畸变权重（0.709）与单一特征分支也有不同程度劣化。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 8, Section V-D and Table IX
- Evidence: V-D 消融段 + Table IX 四变体×四场景完整数值。
- Quote: “Among the ablated variants, w/o panoramic loop closure exhibits worse overall trajectory accuracy, indicating that panoramic loop closure effectively corrects drift.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1288

- Claim: 混合特征的必要性消融：仅手工特征（w/o learned feature）在 Indoor 序列失败；仅学习特征（w/o hand-crafted feature）在 Night 序列失败——两分支特征约束互补，单一来源在特定退化条件下不足；ERP 特征提取需手工+学习混合。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 8, Section V-D and Table IX
- Evidence: V-D 消融段 + Table IX 前两行（含失败标记）。
- Quote: “The w/o learned feature and w/o hand-crafted feature variants suffer from insufficient feature constraints, leading to tracking fail- ures or degraded accuracy.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-0267

- Claim: FastUMI Pro 手持采集平台的视觉核心是腕装鱼眼：主鱼眼相机居中安装在夹爪爪面上方，提供约 180° 对角视场的宽角 RGB 局部工作空间观测；两侧辅以两台辅助鱼眼相机与机载深度相机构成四目视觉系统，在中央视图被爪指遮挡或弱纹理时保持鲁棒跟踪；末端位姿由 Vive Tracker 与机载视觉惯性 SLAM 双流融合恢复，精度约 3mm。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 5, Section 3.1 UMI Hardware for Cross-embodiment Data Collection
- Evidence: Section 3.1 描述 FastUMI Pro 传感套件：主鱼眼相机 + 双辅助鱼眼 + 深度相机构成 quad-ocular 系统；Vive Tracker 6-DoF + VI-SLAM 双流融合位姿达亚厘米精度（~3mm）；观测为左右两腕装鱼眼视图、无外部主视图或第三人称相机。
- Quote: “main fisheye camera is mounted centrally above the gripper jaws, providing a wide-angle (≈180 ◦ diagonal field of view) RGB observation of the local workspace. Flanking the main camera are two auxiliary fisheye cameras that together with an onboard depth camera constitute a quad-ocular visual system; this redundancy maintains robust visual tracking even when the central view is occluded by the gripper fingers or suffers from texture-poor regions. End-effector pose is recovered by fusing two inde”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0272

- Claim: 为对齐鱼眼域，作者构建 UMI-VQA——据其所知首个面向腕装鱼眼观测的大规模视觉-语言数据集：8M 问答对基于同一鱼眼视觉域，覆盖场景理解、交互接地与空间推理；通过与动作数据协同训练 VLM 骨干，把视觉表征对齐到腕装鱼眼固有的畸变几何与局部第一人称视角，而非强制从头微调。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 2, Section 1 Introduction
- Evidence: Introduction 与 Method 3.2：UMI-VQA 由真实 UMI 腕装鱼眼帧（5 能力子集，page 7 Figure 3：物体接地 842K/场景理解 406K/描述 103K/交互接地 894K/空间推理 824K，共 3M）与 RefSpatial 鱼眼化补充（5M）构成 8M 样本。
- Quote: “we construct UMI-VQA, which is, to our knowledge, the first large-scale vision-language dataset tailored to wrist-mounted fisheye observations. UMI-VQA contains 8M question-answer pairs grounded in the same fisheye visual regime, covering scene understanding, interaction grounding, and spatial reasoning. By co-training the VLM backbone on UMI-VQA alongside action data, we align its visual representations to the distorted geometry and local first-person perspective inherent in wrist-mounted fishe”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0274

- Claim: 辅助 VQA 监督的视角域必须与动作数据观测域匹配：在 π0.5 + 受控 UMI 子集上（同动作数据/观测/训练预算），鱼眼域 UMI-VQA 协同训练把三任务聚合成功率从 45.0% 提到 55.0%（+10.0pp），而标准视图 VQA 反而降到 31.7%（比 action-only 低 13.3pp）——全局规则透视观测下的 VQA 监督会把共享骨干的表征学习带离腕装鱼眼动作预测所需的视觉线索。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 14, Section 4.2, Table 3
- Evidence: Table 3 报告三种训练设定的真机成功率（每任务 20 trials，三任务：Center Cube 上叠方块/叠纸杯/叠笔筒）；正文解释标准视图 VQA 有害的机理假设（分布失配偏置表征学习）与 UMI-VQA 最优的结果。
- Quote: “As shown in Table 3, standard-view VQA achieves a lower aggregate success rate than action-only training. This result suggests that auxiliary VQA supervision is not universally beneficial in co-training.”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0277

- Claim: 在同批重采集腕装鱼眼演示上训练的仿真对比中，VISTA 系统性最强：RoboTwin-UMI 0.683 vs 最强基线 π0.5 的 0.594（+8.9pp），LIBERO-UMI 0.943 vs 0.922，平均 0.813——超 π0.5 5.5 点、LingBot-VLA 15.5 点、Wall-X 38.7 点，证明显式鱼眼域适配+物理验证数据的有效性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 15, Section 4.3, Table 6
- Evidence: Table 6 报告四方法在 RoboTwin-UMI/LIBERO-UMI 的成功率（LingBot-VLA 0.499/0.817/0.658、Wall-X 0.152/0.700/0.426、π0.5 0.594/0.922/0.758、VISTA 0.683/0.943/0.813）；全部方法同批腕装鱼眼演示训练，隔离模型差异。
- Quote: “On RoboTwin-UMI, VISTA improves the success rate from 0.594 to 0.683 over the strongest baseline π 0.5 . On LIBERO-UMI, VISTA further improves from 0.922 to 0.943. Overall, VISTA obtains an average success rate of 0.813, outperforming π 0.5 by 5.5 points, LingBot-VLA by 15.5 points, and Wall-X by 38.7 points.”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0278

- Claim: 真机 20 个 UMI 采集操作任务（同验证数据集、同平台与物体配置，每任务 20 trials）上，VISTA 平均成功率 0.598，超 π0.5 的 0.528（+7.0pp 绝对增益），大幅超 LingBot-VLA 的 0.313（+28.5pp）——鱼眼域感知对齐、局部交互理解与物理可执行监督的收益迁移到真机部署。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 16, Section 4.3, Table 7
- Evidence: Table 7 报告三方法 20 任务平均成功率（LingBot-VLA 0.313、π0.5 0.528、VISTA 0.598）；正文给出 7.0 点绝对增益与 28.5 点领先；逐任务结果在 Table 11（page 33）。
- Quote: “Policy Avg. Success Rate LingBot-VLA 0.313 π 0.5 0.528 VISTA 0.598”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0280

- Claim: 跨本体部署以相机配置匹配为前提：作者在三台双臂平台（RealMan、AC one、Galaxea R1 Pro）上安装与手持设备相同的腕装相机配置与末端执行器，末端相机与手持设备完全相同以保证部署观测分布匹配训练分布；各平台机械适配夹爪爪件但保持相同指尖几何与相机外参，使手持数据训练的策略无需重新标定视觉系即可迁移。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 5, Section 3.1 UMI Hardware
- Evidence: Section 3.1 末段说明部署侧方案：三平台安装同款腕装相机与末端执行器，机械适配爪件但保持 fingertip geometry 与 camera extrinsics 一致，实现免视觉系重标定的迁移；配合任何满足 UMI 端执行器安装规范的新臂只需实现笛卡尔空间控制接口（page 22 附录 A）。
- Quote: “For downstream policy execution we mount the same wrist-camera configuration and end-effectors on distinct dual-arm embodiments: RealMan, AC one, and Galaxea R1 Pro (Fig. 2, right). The end-effector cameras are identical to those on the handheld device, ensuring that the visual observation distribution at deployment matches the training distribution. The gripper jaws on the robot side are mechanically adapted to each platform while preserving the same fingertip geometry and camera extrinsics, so”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0501

- Claim: BifrostUMI 的每个手持操作接口都集成一个鱼眼相机与电机驱动 rack-and-pinion 夹爪机构，手柄带 PICO 控制器专用卡槽，使稳定抓取与腕视图视觉观测、夹爪开度测量同步进行。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 3, Section III.A Robot-free Data Collection System, Data-collection hardware
- Evidence: Sec. III.A hardware 段逐字描述每个接口集成鱼眼相机+电机驱动夹爪+控制器卡槽的设计，鱼眼与夹爪机构物理一体化。
- Quote: “Each interface integrates a fisheye camera and a motor-driven rack- and-pinion gripper mechanism, together with a handle that includes a dedicated mounting slot for a PICO controller. This design enables stable grasping while simultaneously capturing wrist-view visual observations and gripper width measurements.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0502

- Claim: 采集平台由 PICO 动捕（双脚+腰部 tracker）与两个各带一个鱼眼相机的仪表化夹爪组成，系统同步记录鱼眼腕视图图像、PICO SDK 人体关键点状态与电机编码器夹爪开度三路多模态观测。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 3, Fig. 2 BifrostUMI Data Acquisition System caption
- Evidence: Fig. 2 caption 明确两个仪表化夹爪各配一个鱼眼相机，且系统同步记录腕视图图像（来自鱼眼相机）、关键点状态（PICO SDK）与夹爪开度（电机编码器）。
- Quote: “The data acquisition platform consists of a PICO-based motion capture setup, including two foot-mounted trackers and one waist-mounted tracker, together with two instrumented grippers, each equipped with a fisheye camera. The system synchronously records multimodal observations, including wrist-view images from the fisheye cameras, human keypoint states obtained via the PICO SDK, and gripper aperture measurements derived from motor encoder readings.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0503

- Claim: 高层策略的唯一视觉条件是一对同步的 224×224 左右腕视图 RGB 图像，辅以 15 维下肢本体感知向量（12 腿关节+3 腰关节）的三帧历史；腕视图（鱼眼采集）是策略全部视觉输入。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 4, Section III.B High-Level: Diffusion Policy, Observation
- Evidence: Sec. III.B Observation 段明确策略条件为一对同步 224×224 左右腕视图 RGB + 15 维下肢本体感知三帧历史；上肢关节被省略因操作意图由 TCP 关键点表达。
- Quote: “The policy is conditioned on one synchro- nized pair of 224×224 left/right wrist-view RGB images and a three-frame history of a 15-D lower-body proprioceptive vector, including 12 leg joints and 3 waist joints.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0504

- Claim: 腕视图 RGB 图像由 DINOv2 编码，与下肢本体感知及 diffusion 步数融合为全局条件，diffusion 模型据此预测 TCP 与身体支撑关键点的动作轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 4, Fig. 4 Conditional diffusion policy architecture caption
- Evidence: Fig. 4 caption 描述条件 diffusion 策略架构：腕视图 RGB→DINOv2→与本体感知/diffusion 步融合→预测关键点动作轨迹。
- Quote: “Wrist-view RGB images are encoded by DINOv2 and fused with lower-body proprioception and the diffusion step as the global condition. The diffusion model predicts action trajectories for TCPs and body-support keypoints.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0506

- Claim: 10 分钟窗口内 BifrostUMI 的有效演示吞吐量在全部操作员×任务组合上高于 TWIST2 遥操作：非行走任务平均加速约 2.2×，行走咖啡递送上差距悬殊（novice 61 vs 1，61.0×）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 7, Table I and Section IV.C
- Evidence: Table I 报告六组操作员-任务对的 10 分钟有效轨迹数与 speedup（2.2×/2.5×/61.0×/1.8×/2.3×/12.4×），正文总结非行走任务平均 ~2.2×。
- Quote: “As shown in Table I, BifrostUMI consistently achieves higher valid demonstration throughput than TWIST2 across all operators and tasks, yielding an average speedup of approximately 2.2× on the two non-locomotion tasks and a much larger gain on walking coffee delivery.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0507

- Claim: 基于鱼眼腕视图观测训练的策略在三个真实任务（杂乱桌面抓放、双臂蔬菜收集、动态投掷）上把免机器人人类演示迁移为物理人形执行：完成视觉定位、抓取、转移与放置/释放，说明学习到的策略超出慢速末端到达。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 6, Section IV.A, Fig. 6
- Evidence: Sec. IV.A 定性结论：Fig. 6 显示三任务全部完成闭环；具体成功率数值仅在图中，正文为定性表述。
- Quote: “The qualitative results in Fig. 6 show that BifrostUMI transfers robot-free human demonstrations to physical hu- manoid execution across all three tasks. The robot completes visual localization, grasping, transfer, and placement in the cluttered scene; switches between two arms for sequential bimanual collection; and generates a coordinated wind-up and release motion for dynamic ball throwing, indicating that the learned policy extends beyond slow end-effector reaching.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0508

- Claim: 把空间关键点重定向（SKR）替换为 GMR 会大幅降低前两个操作任务的成功率：人形部署需要 SKR 做尺度自适应同时保留任务相关关键点的空间结构，无空间锚定的重定向下上层视觉策略仅能偶尔靠闭环视觉反馈恢复且补偿脆弱。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 6, Section IV.A, Fig. 6 ablation
- Evidence: Sec. IV.A 消融结论：SKR→GMR 替换大幅降低成功率；闭环视觉反馈的补偿被描述为 brittle and unstable。
- Quote: “For the first two tasks, replacing Spatial Keypoint Retargeting with GMR [25] substantially reduces success. This confirms that humanoid deployment requires SKR to perform scale adaptation while preserving the spatial structure of task-relevant keypoints. Without this spatially grounded retargeting, the upper-level visual policy may occasionally recover through closed-loop visual feedback, but such compensation is brittle and unsta- ble.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0509

- Claim: 强腰腿参与的任务需要膝关键点：膝关键点消融显示其对恢复正确下肢运动（尤其屈膝与降低身体）至关重要，缺少时下肢姿态欠约束、全身执行可靠性下降；全身任务（桌下垃圾处置、行走咖啡递送）在七关键点变体下于物理 G1 上完成。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 7, Section IV.B and Fig. 7
- Evidence: Sec. IV.B 报告 Fig. 7 两全身任务定性完成与膝关键点消融结论（欠约束→可靠性下降）。
- Quote: “The qualitative results in Fig. 7 show that BifrostUMI completes both task sequences on the physical Unitree G1 robot. Under-table waste disposal demonstrates that sparse keypoints can encode whole-body posture changes needed to reach targets outside the arm-only workspace, while walking coffee delivery shows that the same framework supports locomotion-manipulation”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0799

- Claim: 数据集对比显示 WideDepth 基准的 GT 精度数量级领先：Precision@10m 为 ±1mm，而 KITTI-360/WoodScape/其训练集为 ±20mm、Oxford RobotCar 为 ±30mm；HFOV 覆盖 120..195°，且是唯一同时提供水平+垂直立体、针孔配对与稠密深度图的鱼眼数据集，训练集为首个垂直立体设置。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 2, Table I
- Evidence: Table I 逐列对比 7 个数据集：Real/Synthetic、Domain、分辨率、HFOV、精度、立体/针孔/稠密深度图配置；WideDepth benchmark 行唯一为 Indoor+±1mm+全配置。
- Quote: “Precision@10m - - ±30 mm ±20 mm ±20 mm ±20 mm ±1 mm Horizontal Stereo ✓ ✗ ✗ ✗ ✗ ✗ ✓ Vertical Stereo ✗ ✗ ✗ ✗ ✗ ✓ ✓ Pinhole ✗ ✗ ✓ ✓ ✗ ✗ ✓ Dense depth map ✓ ✓ ✗ ✗ ✗ ✗ ✓”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0800

- Claim: 基准设计显式面向具身应用：场景按任务策展（操作任务取孤立物体、导航取走廊/办公室/厨房等杂乱环境）；采集高度按部署平台分层——1.65m 对应 AR/人形机器人、2.5m 对应 CCTV、0.5m 对应移动平台；较高视角强调大平面、较低视角捕捉椅腿与线缆等细节。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 4, Section IV-A
- Evidence: IV-A 阐述基准设计原则：与自动驾驶数据集的近重复采样不同，按细粒度细节/几何复杂度/光照/深度用例策展；三种高度直接对应三类机器人部署眼高。
- Quote: “For manipulation, isolated objects are key, while navigation benefits from corridors, offices, and cluttered environments (e.g., kitchens). Captured indoors, our benchmark includes the following lighting categories: natural light, office lamps, and mixed conditions. To enhance diversity, we varied capture heights: 1.65m for AR/humanoid robots, 2.5m for CCTV, and 0.5m for mobile platforms. Higher viewpoints emphasize large planes, while lower ones capture finer details like chair legs and wires.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0801

- Claim: WideDepth 提出 CUDA 加速的生成管线：基于 Double Sphere 模型从高分辨率 LiDAR 扫描生成鱼眼立体 RGB/深度/视差真值（无需存储大体积全景中间产物），并借此让针孔训练的立体模型免重训适配鱼眼图像——'复用针孔模型生态 + 投影层适配'而非重训专用架构。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 1, Contributions
- Evidence: 贡献 2 原文：CUDA-accelerated pipeline、Double Sphere model、scalable benchmark creation without storing large panoramas、adapting pinhole-trained models to fisheye without retraining；配套的 Disparity2Depth 转换在 Helvipad 上以 CREStereo 验证（MAE=1.92、RMSE=3.40，与原报告相当）。
- Quote: “We propose a CUDA-accelerated pipeline that gener- ates stereo fisheye RGB, depth, and disparity ground truth from high-resolution LiDAR scans using the Dou- ble Sphere model. This enables scalable benchmark creation without storing large panoramas and allows adapting pinhole-trained models to fisheye without retraining.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0802

- Claim: 投影对照实验（同一 CREStereo 立体模型，差异仅来自投影）：等距柱状投影全面优于 cubemap——EPE 1.065 vs 4.500、EPE_Q95 3.056 vs 13.743、bad-1 28.27% vs 78.93%、bad-3 5.16% vs 51.13%；cubemap 保留局部细节但面边界不连续带来深度一致性问题，误差在边界处增大。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 4, Table II + Section III-C
- Evidence: Table II 六项指标等距柱状全优；Fig. 3 误差差值图显示 cubemap 误差在边界增大；III-C 正文明确同模型设计确保差异仅来自投影方法本身。
- Quote: “Cubemap 4.500 3.111 13.743 78.93 62.92 51.13 Equirectangular 1.065 0.351 3.056 28.27 10.37 5.16”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0807

- Claim: 与单目深度随 FOV 退化相反，经等距柱状适配后的立体匹配性能随 FOV 增大而一致改善：StereoBase 在全部五种基线上 FOV 120→195° 的 RelEPE 均下降（如 20mm 行 0.083→0.067、65mm 行 0.074→0.061）——宽 FoV 对（适配后的）鱼眼立体深度是净收益，支持其在室内广覆盖感知中的价值。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 6, Section V-B + Fig. 8 (page 7)
- Evidence: V-B 原文：higher FOV consistently enhances performance, reinforcing the importance of wide angles for capturing broader indoor environments；Fig. 8 每一行从左到右（FOV 增大）数值递减提供逐行验证。
- Quote: “We also analyzed the impact of baseline and FOV on StereoBase, finding that baseline variations affect perfor- mance more significantly than FOV. A 65 mm baseline yields optimal metrics, while larger baselines degrade quality due to disparity distribution shift. Conversely, higher FOV con- sistently enhances performance, reinforcing the importance of wide angles for capturing broader indoor environments.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0808

- Claim: 轻量 BGNet（19ms、面向 Jetson Orin 嵌入式实时推理）在 WideDepth 训练集上微调 15 epochs 后：EPE 3.411→1.767（−48%）、EPE_Q50 −57%、EPE_Q95 −58%、bad-1 53.30→27.63（−48%）、bad-3 24.34→9.29（−62%），延迟不变，超过 FADNet++/GMStereo 并接近 IGEV/StereoBase/CREStereo——小规模鱼眼域适应可用轻量模型追平重型模型（摘要的'最高 62% 提升'即 bad-3 −62% 口径）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 7, Table IV + Section V-B
- Evidence: Table IV 微调行括号内百分比与原始行对照；微调协议（15 epochs、batch 8、AdaBelief、one-cycle 5e-5、50% 非对称色彩增强）在 V-B 报告；摘要 up to a 62% performance boost 与 bad-3 −62% 一致。
- Quote: “BGNet [28] 19 3.411 1.410 13.595 53.30 33.32 24.34 BGNet [28] (fine-tuned) 19 1.767 (-48%) 0.606 (-57%) 5.736 (-58%) 27.63 (-48%) 13.76 (-59%) 9.29 (-62%)”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0809

- Claim: 经等距柱状投影适配后，6 个立体模型在鱼眼输入上的排名与针孔基准排名高度一致——鱼眼立体性能可从针孔排名推断；对宽角应用 StereoBase 最理想但代价是高延迟，而 Fig. 7 的相对误差图显示其错误集中于半透明/反射面等通用立体难点、无鱼眼特有问题——投影适配路线未引入鱼眼专属误差模式。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 6, Section V-B (+ Fig. 7, page 7)
- Evidence: V-B 原文：model rankings closely match pinhole benchmarks, suggesting that fisheye stereo performance can be inferred from pinhole-based ratings；StereoBase proves ideal, though at the cost of high latency；Fig. 7 错误图分析（common stereo matching errors without fisheye-specific issues）。
- Quote: “Quantitative results in Table IV show that model rankings closely match pinhole benchmarks, suggesting that fisheye stereo performance can be inferred from pinhole-based rat- ings. For wide-angle applications, StereoBase proves ideal, though at the cost of high latency.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-1080

- Claim: 应用方式与动机：主流透视图像范式的 MLLM 继承人眼式感知的窄瞬时视场，而导航、机器人搜索与 3D 场景理解等任务受益于 360° 全景'超感知'（supersensing）——一次捕获整个周围环境；但现有 MLLM 管线通常把全景分解为多个透视视图，使等距柱面投影（ERP）的球面结构基本保持隐式；本文提出 pano-native 理解：要求 MLLM 把 ERP 全景当作连续的观察者中心空间直接推理，并定义语义锚定、球面定位、参考系变换、深度感知 3D 空间推理四项关键能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 1, Abstract
- Evidence: page 1 摘要陈述窄视场问题、360° 超感知动机、既有管线分解全景致球面结构隐式，以及 pano-native 四能力定义。
- Quote: “Multimodal large language models (MLLMs) still struggle with spatial understand- ing under the dominant perspective-image paradigm, which inherits the narrow field of view of human-like perception. For navigation, robotic search, and 3D scene understanding, 360 ◦ panoramic sensing offers a form of supersensing by capturing the entire surrounding environment at once. However, existing MLLM pipelines typically decompose panoramas into multiple perspective views, leav- ing the spherical structure”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1081

- Claim: 能力分类法：pano-native 理解被分解为四个能力族并作为监督设计与基准构建的共同基础——(1) 语义锚定：把语言锚定到 ERP 中的视觉实体（身份、属性、场景内容与全局场景拓扑语义）；(2) 球面定位：在以 yaw/pitch 参数化的观察者中心球面上定位实体（从粗方向分类到细粒度 BFOV 式角度接地），而非仅平面图像网格；(3) 参考系变换：推理观察者旋转或以物体为条件的重定向下空间关系如何变化（含角度关系与接缝感知的环绕连续性）；(4) 深度感知 3D 空间推理（定义在 page 5 开头）：把球面观测连接到周围 3D 结构（深度、相对距离与观察者中心关系）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 4, Section 3.2 Capability Taxonomy（Depth-aware 3D 一族定义在 page 5 开头）
- Evidence: Section 3.2 给出语义锚定/球面定位/参考系变换三族定义并声明该分类法是监督设计与基准构建的基础；第四族（深度感知 3D）在 page 5 开头定义。
- Quote: “We decompose pano-native understanding into four capability families that together define the core requirements for reasoning over ERP panoramas. This taxonomy serves as the foundation for both supervision design and benchmark construction. Semantic anchoring. The model must ground language to visual entities in ERP panoramas, covering object identity, attributes, scene contents, and global scene-topology semantics such as environment and layout structure. This forms the semantic basis for subse”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1082

- Claim: 数据规模与构成：ERP 语料库含 570,321 张全环绕全景，室内（297,476 张，52.2%）与室外（272,845 张，47.8%）近似均衡——作者认为该均衡对 pano-native 学习重要（室内提供物体丰富的局部布局与深度关系，室外引入更大尺度结构、长程可见性与多样全景拓扑）；来源混合：Realsee3D 合成 273,451 张（47.9%，最大单一来源）、API 采集 117,261、户外网络爬取 76,643、街景爬取 63,651、Realsee3D 真实 24,025、360+X 15,290；发布前将做隐私过滤（遮蔽可识别内容、排除敏感场景）并只发布与源许可兼容的资产。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 15, Appendix A.1 与 Table 9
- Evidence: Appendix A.1 与 Table 9 报告语料总量、室内外均衡及其学习意义、六类来源构成；同页给出许可与隐私处理承诺。
- Quote: “Our ERP corpus contains 570,321 full-surround panoramas collected from mixed sources. The corpus is approximately balanced between indoor and outdoor scenes, with 297,476 indoor panoramas and 272,845 outdoor panoramas. This balance is important for pano-native spatial learning, since indoor scenes provide object-rich local layouts and depth relations, while outdoor scenes introduce larger-scale structures, long-range visibility, and diverse panoramic topology.”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1083

- Claim: 可验证元数据管线与指令规模：每张全景投影为 120° FoV、60° yaw 步长（相邻视图约 60° 重叠）的透视视图，用 WeDetect-Large 开放世界检测器（置信阈值 0.3、视图级 NMS IoU 0.5）检测后重投影回 ERP 坐标并跨视图合并（两框 ERP IoU 超 0.6 视为几何一致）；用 Qwen3-VL-32B 生成类别/属性/描述/判别性指代短语，再以 WeDetect-Ref-4B 做描述引导复检（原始提议与复检框 IoU 超 0.7 才保留实体）；深度取源数据对齐深度或全景深度模型伪深度；最终从验证后元数据图实例化 7.65M 候选指令样本、采样 2,997,516 条规范训练集（平均每张全景 5.26 条指令）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 15, Appendix A.2 与 A.3（Table 10 指令分布在 page 16）
- Evidence: Appendix A.2-A.3 给出管线实现参数（投影 FoV/步长、检测/复检阈值、模型选择）与候选/规范指令两级规模。
- Quote: “We provide additional implementation details for the metadata construction pipeline in Sec. 3.3. For each ERP panorama, we render overlapping perspective views with a 120 ◦ FoV and a 60 ◦ yaw stride, resulting in approximately 60 ◦ overlap between adjacent views. We use WeDetect-Large [ 13] as the open-world detector, with a confidence threshold of 0.3 and a view-level NMS IoU threshold of 0.5. The detected boxes are reprojected to ERP coordinates and merged across overlapping views; two boxe”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1084

- Claim: 模型设计：PanoWorld 以 Qwen3.5-VL 为底座并扩展 pano-aware 模块——Spherical Spatial Cross-Attention（SSCA）适配器插入 patch embedding 之后：对每个 ERP patch 计算其图像坐标中心 (u,v) 并映射到球面方向 (λ,φ)，经固定正弦球面编码 γ 后由 MLP 投影为球面空间 token S；视觉 token H(0) 通过交叉注意力（Q=LN(H(0))、K=V=LN(S)）检索几何信息，所得几何感知信号经门控残差更新 H̃(0)=H(0)+α⊙A 融合回视觉流再送入其余视觉块（α 为小值初始化的可学习门，说明接排 page 7）——预训练主干保持不变，球面几何经视觉内容与观察者中心空间 token 的自适应交互注入，以弥合'同一像素位移在不同纬度对应不同角度变化、左右边界在真实场景相邻'的 ERP 与平面栅格错配。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 6, Section 3.4 Pano-aware MLLM Adaptation（公式 (7)-(10)；α 门说明在 page 7 开头）
- Evidence: Section 3.4 给出 SSCA 的插入位置、球面 token 构造（公式 7-8）、交叉注意力融合（公式 9）与门控残差更新（公式 10），并陈述主干不变的设计意图。
- Quote: “We adopt Qwen3.5-VL as the backbone and extend it with a pano-aware module that injects spherical geometry into the visual stream. Since the native visual encoder operates on a planar raster, it does not explicitly account for the spherical structure of ERP images, where the same pixel displacement may correspond to different angular changes at different latitudes and the left and right image borders are adjacent in the real scene. To address this mismatch, we introduce Spherical Spatial Cross-A”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1085

- Claim: 主基准结果：pano-native 训练把 Qwen3.5 基线在 PanoSpace-Bench 上从 overall 30.8 提升到 56.5，且增益是跨类别而非类别特定的——绝对方向 25.2→93.7、BFOV mIoU 1.41→73.3、球面关系均值 26.1→47.4、3D 空间均值 36.9→49.8、接缝推理 41.2→65.5；作者结论：稳健的全景理解需要 pano-native 空间学习，而不是把 ERP 当作一张宽 2D 图像或仅依赖提示级的坐标描述。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 8, Section 4.2（Table 2 在 page 7）
- Evidence: Section 4.2 正文汇总 Table 2 的主对比：基线 30.8→PanoWorld 56.5 及五类增益数字，并给出中心结论。
- Quote: “Our pano-native model achieves the best overall performance, improving the Qwen3.5 baseline from 30.8 to 56.5. The gains are broad rather than category-specific: absolute direction rises from 25.2 to 93.7, BFOV mIoU from 1.41 to 73.3, spherical relation average from 26.1 to 47.4, 3D spatial average from 36.9 to 49.8, and seam reasoning from 41.2 to 65.5. These results support the central claim of the paper: robust panoramic understanding requires pano-native spatial learning rather than treating”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1088

- Claim: 零样本迁移到外部人形搜索基准：H*Bench 原协议为透视视图迭代探索，本模型直接以 ERP 全景为输入一步预测方向——PanoWorld 零样本达 overall 56.1（HOS 61.8/HPS 47.5），大幅超过最强已报告透视视图基线 HVS-3B*（38.4），也高于 GPT-4o（21.3）与 Gemini-2.5-Pro（32.3）；作者据此说明 pano-native 监督学到的表示可迁移到下游全景搜索而非过拟合 PanoSpace-Bench。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 8, Section 4.2 H*Bench 零样本段（Table 3(a) 同页）
- Evidence: Section 4.2 报告 Table 3(a) 对比：零样本 ERP 输入 56.1 vs 最强透视视图基线 38.4，并给出泛化性解释。
- Quote: “Table 3(a) compares the conventional perspective-view protocol with direct ERP input. Our zero-shot model reaches 56.10 overall, substantially outperforming the strongest reported perspective-view baseline (38.40). This shows that the representation learned from pano-native supervision transfers to downstream panoramic search rather than overfitting to PanoSpace-Bench alone.”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1089

- Claim: VLN 迁移：R2R-CE Val-Unseen 上仅以 ERP 全景为输入（区别于用全景采样候选透视图做视点选择的既有用法），PanoWorld-VLN 达 54.3 SR/52.1 SPL，较 waypoint 范式的 GridMM +5.3 SR/+11.1 SPL，较 RGB-only 的 StreamVLN +4.1 SR/+5.0 SPL——且在与近期 RGB-only VLN 相同的 R2R/RxR 训练设定下仅用 80% 训练数据；作者结论：直接全景理解为 VLN 提供高效可迁移范式，从碎片化局部视图探索转向统一全环绕空间推理。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 8, Section 4.2 VLN 段（Table 4 在 page 9）
- Evidence: Section 4.2 VLN 段报告直接 ERP 输入的 R2R-CE 结果与两类范式（waypoint/RGB-only）对比及 80% 数据设定。
- Quote: “Quantitative comparison on VLN. We further evaluate transfer on R2R-CE Val-Unseen using only ERP panorama as input, which is different from methods that use panoramas to sample candidate perspective views for viewpoint selection. As shown in Table 4, PanoWorld achieves 54.3 SR and 52.1 SPL using only panorama input. Compared with methods that rely on waypoint predictors or use panoramas mainly for candidate-view selection, PanoWorld directly consumes the ERP panorama as a unified full-surround o”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1090

- Claim: 数据质量消融：两级元数据验证对可靠 ERP 监督重要——从无验证 baseline 出发，检测验证（滤除几何不稳定提议与接地目标）把 overall 从 38.8 提到 46.4，语义验证（去除语义不一致问答对）提到 48.0，两者结合得最佳 55.1 且定位/方向/3D/接缝全面增益——作者确认数据质量是 pano-native 学习的一个主要因素。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 9, Section 4.3 Metadata verification 段（Table 6 在 page 10）
- Evidence: Section 4.3 Metadata verification 段报告 Table 6 的四档管线消融与结论。
- Quote: “Metadata verification. Table 6 shows that both verification modules are important for reliable ERP supervision. Starting from the unverified baseline, detection verification improves overall accuracy from 38.8 to 46.4 by filtering geometrically unstable proposals, while semantic verification raises it to 48.0 by removing inconsistent language-region pairs. Combining both yields the best result of 55.1, with gains across localization, directional reasoning, 3D reasoning, and seam continuity. This”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1091

- Claim: 架构消融：比较残差融合与交叉注意力在 patch/merge/output 三种插入位置——patch 级交叉注意力整体最佳，把准确率从 0.484 提升到 0.551 并取得最强球面关系均值（0.460）与 3D 空间均值（0.488）；残差融合在部分设定（尤其接缝连续性）有帮助但在关系密集类别上不一致——支持 SSCA 设计结论：球面几何在早期（patch 级）经与视觉 token 的内容依赖交互注入最有效。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 9, Section 4.3 Architecture ablation 段（Table 7 在 page 10）
- Evidence: Section 4.3 Architecture ablation 段报告 Table 7 的融合机制×插入位置消融与 SSCA 设计结论。
- Quote: “Architecture ablation. Table 7 compares residual fusion and cross-attention at different insertion positions. Patch-level cross-attention performs best overall, improving accuracy from 0.484 to 0.551 and yielding the strongest spherical relation average (0.460) and 3D spatial average (0.488). Residual fusion also helps in some settings, especially seam continuity, but is less consistent on relation-heavy categories. These results support the proposed SSCA design: geometry is most effective when”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1092

- Claim: 推理效率：H* 任务上直接 ERP 推理仅需 1 步/1 次模型调用/16.5k 有效输入 token 并维持完整 360° 空间覆盖；透视视图旋转范式平均需 3.58-6.34 次交互步与 18.7k-29.9k 有效输入 token，对应 1.13-1.81× 于直接 ERP 推理的成本，且旋转法每步只观察局部 FoV——直接全景推理以单次前向把迭代局部视图搜索替换为统一高效的全环绕推理范式。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 22, Appendix D Efficiency Study 与 Table 14
- Evidence: Appendix D 与 Table 14 报告视角旋转 vs 直接 ERP 的交互步/调用数/有效输入 token/相对成本对比。
- Quote: “As shown in Table 14, perspective-view rotation requires 3.58–6.34 interaction steps on average, leading to 18.7K–29.9K effective input tokens. This corresponds to 1.13–1.81× the cost of direct ERP inference. Our method requires only one step and one model call, with 16.5K effective input tokens, while maintaining full 360 ◦ spatial coverage. This demonstrates that pano-native spatial learning replaces iterative local-view search with a unified and efficient full-surround inference paradigm.”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-0101

- Claim: 1001 DEMOS 用超广角鱼眼相机做 eye-in-hand 数据采集，以在相同采集视角数下最大化演示的视觉覆盖；作者同时指出：虽然这大幅扩展了观察视场，但该非标准相机配置要求把 3D Gaussian Splatting 公式扩展为在渲染步骤引入鱼眼 ray sampler。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 2, Section 1, key designs (third bullet)
- Evidence: 这是论文三条关键设计中的第三条：鱼眼超广角的选择服务于“让每条演示的视觉覆盖最大化”，但非标准成像模型迫使作者改造 3DGS 渲染管线（Fisheye-3DGS）。
- Quote: “To maximize visual coverage during data collection, our system uses an ultra-wide fish-eye cam- era. However, while this drastically increases the field-of-view of the observations, this non- standard camera configuration requires us to extend the 3D Gaussian Splatting formulation by introducing a fisheye ray sampler in the rendering step.”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0102

- Claim: Fisheye-3DGS 把 3DGS 的针孔 ray sampler 替换为基于 KB8 相机模型的鱼眼 ray sampler，并将 tile 分配从针孔 ray 重分配到鱼眼 ray、按原 256-ray-per-tile 布局分区，从而在精确建模鱼眼畸变的同时保留 CUDA block-thread 结构以实现快速光栅化。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 4, Section 3.1, Fisheye 3D Gaussians (Fig. 3)
- Evidence: KB8（Kannala-Brandt 通用相机模型）为每个鱼眼像素计算射线方向，再经针孔内参映射到 splat 位置；该设计是“鱼眼 + 3DGS 可编辑渲染”的核心使能组件。
- Quote: “we replace the original ray sampler with a KB8-based [36] fisheye ray sampler. As shown in Fig.3, for each fisheye pixel (u, v), compute its ray di- rection rd = KB8( u, v) [36], then project rd through the camera intrinsics K to obtain the pinhole coordinates (up, vp) = K rd, thus associating each fisheye ray with its 3D-Gaussian splat location on the 2D image plane. We redistribute tile assignments from pinhole to fisheye rays, partition fisheye rays into the original 256-ray-per- tile layout”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0103

- Claim: 在 RoboMimic square 任务（Franka Panda 方螺母插杆）的仿真评估中——为匹配 eye-in-hand 数据格式，腕相机针孔图像被转换为 GoPro 鱼眼镜头 155° FoV 的鱼眼图像——在同等原始专家演示量下，free-space 动作-视角增广相比无增广训练平均提升 56% 任务成功率，并紧贴真值渲染 oracle 上界（低数据域差距 8%、高数据域差距 11%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 8, Section 4.1
- Evidence: 仿真对照包含 No Aug、GT-rendering oracle（仅仿真可得）、Aug Action Only 与 SPARTN；策略在各演示子集 {30,50,100,150,200} 上训练并在 1000 个测试初始构型上评估。
- Quote: “Figure 5(b) shows that, with the same amount of original expert demonstrations, our action-view augmentation closely tracks the perfect GT-rendering upper bound, with a performance gap of 8% in the low-data regime and 11% in the high-data regime. Compared to policies trained without aug- mentation, our free space augmentation provides an average of 56% task success rate improvement.”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0104

- Claim: 在真机杯具服务任务上，以同等数量的人类演示为基础，free-space 增广相比无增广训练提供 55% 的性能提升。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 8, Section 4.1
- Evidence: 真机基础数据为 89 条单演示者 UMI 采集 episodes；从人工筛选的 50 条 episodes 生成 7245 条 free-space 增广 episodes（page 7）。
- Quote: “In the real-world experiment shown in Fig 6, we find that, with the same amount of human demon- strations, our free space augmentation provides a performance boost of 55% over policies trained without augmentation.”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0105

- Claim: 在真机障碍物场景评估（每策略 20 个评估 episodes）中，加入障碍规避增广数据的策略（Obstacle Aug）以 100% 成功率完成任务，显著超过 FreeSpace Aug（10%）与 No Aug（5%）——避障行为在原始人类演示中不存在，由增广数据习得。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 8, Section 4.1
- Evidence: 原始演示全部在无障碍场景采集；障碍规避增广把 Objaverse 障碍物集成进原场景的 Fisheye-3DGS 并生成绕障轨迹（page 7）。
- Quote: “We find that our full Obstalce Aug is able to complete the task with a 100% success rate, significantly outperforming FreeSpace Aug with 10% and No Aug with 5% success rates, respectively.”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0106

- Claim: 在更具挑战性的障碍设置（更难的障碍放置、更大且几何形状更多样的障碍物；10 组不同障碍集各 10 trials）中，Obstacle Aug 策略完成 10/10 trials，而 No Aug 与 FreeSpace Aug 均未完成任何 trial。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 13, Appendix A.2, Table A1
- Evidence: 附录 A.2 的挑战性障碍实验与正文共用同一三个策略；Table A1 报告 No Aug 0%、FreeSpace Aug 0%、Obstacle Aug 100%。
- Quote: “we conducted 10 trials on 10 different obstacle sets as shown in Fig. A2, on the same three policies No Aug, FreeSpace Aug, Obstacle Aug, as tested in real world experiments for Free Space and Obstacle as reported in manuscript, and found that ours Obstalce Aug was able to complete 10/10 trials, while No Aug and FreeSpace Aug both fail complete any trials.”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0110

- Claim: action-only 增广（Aug Action Only）在第三人称视角下对小范围机器人状态扰动有效，但在 eye-in-hand 观察下失效——微小的末端执行器位姿变化会产生剧烈的视觉变化；定量上该基线相比 No Aug 平均提升 29%（峰值 56%），而 1001 DEMOS 在高数据域最多超出 Aug Action Only 35%。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 8, Section 4.2
- Evidence: 该对比揭示了观察模式（第三人称 vs eye-in-hand）决定增广方式的适用性：视觉-动作耦合越强，越需要视觉端的联合增广。
- Quote: “While effective for small, local robot state variations under third-person views, it breaks down with eye-in-hand observations, where minor end-effector pose changes produce drastic visual shifts. We replicate this baseline by applying free-space aug- mentation in the end-effector and gripper actions, but using the original visual observations. As Fig. 5 shows, Aug Action Only boosts the average success rate by 29% over No Aug – peaking at 56%. In turn, Ours outperforms Aug Action Only by up to”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0111

- Claim: 与单步增广基线 SPARTN（NeRF 重建视觉场景、单步扰动视觉-动作）相比：SPARTN 相比 No Aug 提升 41%，但其单步增广无法产生平滑的轨迹级避障行为、更容易使策略进入无恢复行为的未见构型；1001 DEMOS 做轨迹级动作-视角增广，平均成功率再超出 SPARTN 15%（峰值提升 18%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 8, Section 4.2
- Evidence: 该对比把“增广粒度”从单步提升到整条轨迹，作者归因于轨迹级增广能提供 OOD 状态下的恢复行为。
- Quote: “Single-step action-view augmentation using SPARTN improves policies’ performance for OOD camera views, as shown in Fig. 5 with a performance gain of 41% over No Aug. However, SPARTN’s single-step augmentation cannot produce smooth, trajectory-level collision-avoidance behaviors, more easily causing policies to enter unseen configurations for which no recovery behav- iors exist in the training data. By comparison, 1001 D EMOS performs trajectory-level action-view augmentation. We observe that Our”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0113

- Claim: 为与 eye-in-hand 数据格式一致，仿真评估把 RoboMimic 腕相机的针孔图像观察用 GoPro 鱼眼镜头（155° FoV）的内参与畸变参数转换为鱼眼图像。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 6, Section 4, Simulation Evaluation
- Evidence: 该转换保证仿真/真机数据格式一致，也说明鱼眼格式是该框架的一等公民而非可选项；同时 50° 增广锥、155° 鱼眼转换共同定义了评估的视角扰动范围。
- Quote: “To follow the same data format as in §3.1, we convert the pinhole image observations from the wrist camera into Fisheye images using intrinsic & distortion parameters of a GoPro Fisheye lens with a 155 ◦ FoV .”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0430

- Claim: ICWM 的部署机制是两阶段免更新推理：任务执行前，机器人在安全工作空间内采样随机目标位姿并执行任务无关探测动作，记录 (o_s, a, o_e) 转移构成交互上下文 T；该协议无需梯度更新、免先验标定、无需目标环境知识，且探测工作空间设计为避开任务相关物体以不扰动任务初始状态。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 5, Section 4.2
- Evidence: 方法设计卡：Active Probing Phase 的完整描述（随机目标位姿、空间多样性、避开任务物体）与两阶段协议声明。
- Quote: “At deployment, ICWM enables task-specific demonstration-free adaptation to novel system configurations through a two-phase inference protocol that requires no gradient updates, prior calibration, or knowledge of the target environment. Active Probing Phase. Before task execution, the robot collects the interaction context T = { ( o s i , a i , o e i ) } N i=1 by performing N task-agnostic probing actions. For each step i ∈ {1, . . . , N }, a random target pose is sampled within the robot’s safe”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0431

- Claim: 仿真跨视角协议下的平均增益：LIBERO 上 ICWM 相对多视角行为克隆（MV，同架构同数据但无上下文）提升 OOD 成功率 13.0%，相对注入真值相机角度文本的显式配置基线（EXP）再提升 9.5%——隐式交互上下文系统辨识优于显式角度标注；作者同时强调多视角数据扩展仍留有『几何外推』这一标准模仿学习无法解决的开放难题。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 6, Section 5.2, Figure 4
- Evidence: 5.2 节两条关键观察的原文数值：+13.0% vs MV、+9.5% vs EXP；图 4 AVERAGE 标注 +8.1%/+13.0%。
- Quote: “ICWM demonstrates significantly stronger resilience, im- proving the OOD success rate by 13.0% over the Multi-View BC baseline. This confirms that while multi-view training expands spatial data, geometric extrapolation remains an open challenge that standard imitation learning struggles to resolve without test-time adaptation. (2) Implicit identification outperforms explicit specification. ICWM improves OOD success rate by 9.5% over Explicit Configuration.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0432

- Claim: 长时程任务获益最大：LIBERO-Long 上 ICWM 相对 MV 提升 29.9%（seen）与 26.3%（unseen），为全部套件中最大相对增益；作者归因于长时程任务会放大视角偏移造成的小空间误差、在基线中引发级联失败，而 ICWM 通过持续把动作锚定在系统动力学上来缓解。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 6, Section 5.2
- Evidence: 5.2 节第 (3) 条观察：+29.9%（seen）/ +26.3%（unseen），最大相对增益；表 4 Long OOD 平均 MV 19.8 / ICWM 25.0（page 16/19 核对）。
- Quote: “On LIBERO-Long, ICWM surpasses MV by 29.9% (seen) and 26.3% (unseen), the largest relative margins across all suites.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0435

- Claim: 探测运动模式不敏感：四种探测策略（Random / XY-only / Z-only / R-only）在 OOD 视角上全部超过多视角基线 15–27%，作者据此判定收益来自交互格式本身而非特定运动模式；随机采样平均 25.0 为最佳（MV 19.8），且无单一策略在所有视角占优——不同运动轴暴露局部动力学流形的不同侧面。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 8, Section 6.2, Table 2
- Evidence: 6.2 节 + 表 2 数值：Random 25.0 / R-only 23.4 / Z-only 22.8 / XY-only 24.9 对 MV 19.8；'by 15 27%' 为提取文本中破折号丢失形态（原文 15–27%）。
- Quote: “As shown in Tab. 2, all four strategies consistently outperform the multi-view baseline by 15 27%, confirming that the benefit of ICWM stems from the interaction format itself rather than any partic- ular movement pattern. Performance differences across strategies suggest that different axes expose different aspects of the local dynamics manifold, with no single strategy dominating across all viewpoints.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0438

- Claim: 形态学（运动学）外推上优势随不确定度扩大：WindowX 平台把连杆长度缩放为 {100%, 90%, 80%, 70%}，训练只用两个边界构型（100% 与 70%）、零样本评测两个插值 OOD 构型（90% 与 80%）；连杆偏移从 10% 增至 20% 时，MV 平均成功率塌缩过半（57%→28%），ICWM 优雅退化（77%→62%），对 MV 的优势从 20 分扩大到 34 分；垫片实验显示同样模式（ΔL=80mm 处 MV 5.6、ICWM 14.4）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 9, Section 6.3, Figure 9
- Evidence: 6.3 节 WindowX 插值外推协议与 57→28 / 77→62 / 20→34 分数值；垫片 ΔL=80mm 数值在同节前句。
- Quote: “We further validate this on a WindowX platform with system- atically varied link lengths ({100%, 90%, 80%, 70%} of the orig- inal), training on two boundary configurations (100% and 70% link length) and evaluating zero-shot on two interpolated OOD configurations (90% and 80%). As the link-length offset increases from 10% to 20%, MV’s average success rate collapses by more than half (57% → 28%), while ICWM degrades far more grace- fully (77% → 62%), widening its margin over MV from 20 to 34 point”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0636

- Claim: Humanoid-OmniOcc 是首个面向人形机器人的全景双目（panoramic stereo-based）占据数据集：Unitree G1 头部 4 组双目相机实现完整 360° 视觉覆盖、15 类室内语义密集标注、15 个仿真场景+5 个真实环境，机器人本体不依赖 LiDAR。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 3, Contributions (bullet 1); page 3, Table 1
- Evidence: 贡献第一条逐字声明 first panoramic stereo-based occupancy dataset for humanoid robots、full 360° visual coverage、15 indoor categories、15 simulated scenes and 5 real-world environments、without relying on LiDAR；Table 1（page 3）给出 155K 帧/[44,384,384]/0.04m 的对比行。
- Quote: “• We present Humanoid-OmniOcc, the first panoramic stereo-based occupancy dataset for humanoid robots, offering full 360 ◦ visual coverage with dense semantic labels over 15 indoor categories, spanning 15 simulated scenes and 5 real-world environments, without relying on LiDAR.”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0637

- Claim: 环视双目硬件配置：Unitree G1 头部前/后/左/右各装一组双目模块（共 4 组），构成全景立体感知系统，每组经视差计算做深度估计以保证 360° 空间覆盖；相机分辨率 1280×1080、基线 6cm、焦距 596.81px；原始（畸变）图像 FOV 约 106°(H)×86°(V)（±3°），立体校正后收缩为 93°(H)×83°(V)（±3°）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 5, Section 3.3 Omnidirectional Stereo Configuration and Fig. 3
- Evidence: Section 3.3 逐字给出 rig 构成（front/rear/left/right 四方向）、分辨率/基线/焦距与 raw→rectified FOV 数字；全文无鱼眼/OCam 模型字样，相机按常规内外参标定（同段末句）。
- Quote: “As shown in Fig. 3, four stereo camera modules are mounted on the Unitree G1’s head facing the front, rear, left, and right directions, form- ing a panoramic stereo perception system. Each stereo pair performs depth estimation through disparity computation, ensuring 360 ◦ spatial coverage. In our setup, we employ stereo cam- eras with a resolution of 1280×1080, a baseline of 6 cm, and a focal length of 596.81 pixels. The field of view (FOV) of the raw distorted images is approximately 106 ◦ ho”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0638

- Claim: 动机：现有具身/室内占据数据集（如 HumanoidOcc）以单目为主——存在深度歧义与弱跨域泛化——或依赖 LiDAR——对人形头戴平台准确但昂贵且笨重；两条既有范式在几何可靠性或硬件成本上受限。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 1, Section 1 Introduction (second-to-last paragraph)
- Evidence: 引言第二段逐字：embodied/indoor occupancy datasets ... predominantly monocular—prone to depth ambiguity and weak cross-domain generalization—or rely on LiDAR, which is accurate but costly and cumbersome for head-mounted humanoid platforms；page 2 首段把两种范式概括为 struggle with geometric reliability or incur prohibitive hardware costs（已核对，在 C04 context 内）。
- Quote: “More recently, embodied/indoor occupancy datasets have begun to emerge (e.g., HumanoidOcc Cui et al. (2025)), yet they are predominantly monocular—prone to depth ambiguity and weak cross- domain generalization—or rely on LiDAR, which is accurate but costly and cumbersome for head- mounted humanoid platforms.”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0640

- Claim: Real2Sim2Real 闭环范式：(i) Real→Sim——Unitree G1 的立体相机内外参、基线（6cm）、FOV 与安装几何被精确复刻进 NVIDIA Isaac Sim，配校准材质与光照的 PBR 光度真实渲染以缩小视觉域差；(ii) Sim——以传感器精确数字孪生产出像素级密集标注（厘米级占据 GT、15 类逐体素语义、度量深度图），15 个室内场景共 155K+ 样本；(iii) Sim→Real——纯仿真训练的模型直接部署到同一 Unitree G1 平台的 5 个真实环境（Bar/Corridor/Office/Apartment）评测并量化 sim-to-real 差距。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 4, Section 3.1 Real2Sim2Real Design Philosophy
- Evidence: Section 3.1 三段（Real→Sim / Sim / Sim→Real）逐字；闭环失败模式反馈句在 page 5 开头（已核对，见 C15）；Abstract 与 Contributions 第二条复述同一范式。
- Quote: “Real→Sim. The physical sensor configuration of the Unitree G1 robot—including stereo camera intrinsics, extrinsics, baseline (6 cm), field of view, and mounting geometry—is precisely replicated in NVIDIA Isaac Sim. Photorealistic physically-based rendering (PBR) with calibrated material prop- erties and lighting further minimizes the visual domain gap, ensuring that the simulated observations closely match real sensor outputs. Sim (Data Generation). With the sensor-accurate digital twin in place”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0641

- Claim: 测试集主结果：环视双目 HS²Occ 在未见仿真测试场景上取得 29.67 IoU / 11.69 mIoU 的最佳总体表现，超过最强单目基线 FB-Occ（28.59 IoU / 5.11 mIoU）——几何 IoU 差距小（+1.08）而语义 mIoU 差距大（11.69 vs 5.11，约 2.3 倍），作者归因于室内长尾类别上显著更好的语义完整性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 8, Section 5.3 Main Results and Table 2
- Evidence: Section 5.3 逐字给出 29.67/11.69/28.59/5.11 四个数字与 best overall performance、semantic completeness 结论；Table 2（page 8）行数据一致（FB-Occ Mono 28.59 5.11；HS²Occ Stereo 29.67 11.69）。
- Quote: “On the test set, our stereo-based HS 2 Occ achieves the best overall performance with 29.67 IoU and 11.69 mIoU, outperforming the strongest monocular baseline (FB-Occ: 28.59 IoU / 5.11 mIoU), indicating notably better semantic completeness on indoor long-tail categories.”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0642

- Claim: 真实世界（sim-to-real）主结果：纯仿真训练的 HS²Occ 在真实场景达 35.45 IoU / 19.26 mIoU，大幅超过最佳单目结果（best IoU 15.39 / best mIoU 5.34）——域移下环视双目优势比测试集更显著（真实 IoU 差距 20.06 vs 测试集 1.08），且真实 IoU（35.45）高于测试集（29.67）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 8, Section 5.3 Main Results and Table 2
- Evidence: Section 5.3 逐字给出 35.45/19.26/15.39/5.34；Table 2 真实世界行（FlashOcc 15.39 IoU；GaussianFormer 5.30 mIoU——正文写 5.34，存在文本/表格 0.04 不一致，引用以表格 5.30 为准）；『20.06 vs 1.08』为两表差值的直接算术。
- Quote: “generalizes strongly to real-world scenes under the Real2Sim2Real protocol, reaching 35.45 IoU and 19.26 mIoU, which exceeds the best monocular results (best IoU: 15.39, best mIoU: 5.34).”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0643

- Claim: 逐类分析：立体深度先验显著改善交互相关语义与细薄结构——测试集上 HS²Occ 的 floor 50.85、door 12.97、cabinet 16.71，且在单目方法常崩溃的目标中心类别上保持非平凡 IoU；真实评测中 chair/table/sofa/bed 达 22.31/22.43/34.74/34.93，验证域移下稳健的 2D-to-3D 提升。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 8, Section 5.3 Per-class results and Table 2
- Evidence: Section 5.3 逐类段落逐字给出全部七个数字与 collapse/robust lifting 结论；Table 2 对应列一致（real: chair 22.31/table 22.43/sofa 34.74/bed 34.93）。
- Quote: “Per-class results further show that stereo depth priors substantially improve interaction-relevant semantics and thin structures: on the test set, HS 2 Occ boosts floor (50.85), door (12.97), and cabinet (16.71), while maintaining non-trivial IoUs for object-centric classes where monocular methods often collapse; in real-world evaluation, HS 2 Occ achieves strong recognition for chair/table/sofa/bed (22.31/22.43/34.74/34.93), validating robust 2D-to-3D lifting under domain shift.”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0645

- Claim: 视差→深度公式消融：把视差代价体转换为深度向代价体（SDN）相对 DDVM 一致提升——测试集 IoU/mIoU 28.04/10.07 → 29.67/11.69，真实世界 32.80/17.03 → 35.45/19.26；动机是视差代价体存在深度敏感不均（同样视差位移在更远距离对应更大深度变化），深度向公式保证不同距离段的同等对待。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 8, Section 5.4 Ablation Study on Disparity-to-Depth Formulation and Table 4 (page 9); page 6, Section 4.3
- Evidence: Section 5.4 消融句逐字给出四组数字；动机句在 Section 4.3（page 6，已核对：Disparity-based cost volumes suffer from non-uniform depth sensitivity...ensuring equal treatment across different distance ranges）；Table 4（page 9）行数据一致。
- Quote: “Ablation Study on Disparity-to-Depth Formulation. As shown in Tab. 4, compared with DDVM, SDN consistently improves occupancy on both the test set (IoU/mIoU: 28.04/10.07 → 29.67/11.69) and real-world data (32.80/17.03 → 35.45/19.26).”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0647

- Claim: 数据规模与生产成本：Humanoid-OmniOcc 共 155,753 个样本（每个样本含全向视点采集的 4 组双目对），来自 15 个仿真室内环境（公寓/工作室/卧室/餐厅/厨房/休息室/客厅/办公室/庭院等房型）；另在 5 个真实室内环境采集 sim-to-real 评测数据；整个数据构建与 PBR 渲染过程消耗约 4,000 GPU 小时（NVIDIA L20 集群），涵盖全局光照仿真、立体渲染与体素级占据 GT 生成。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 13, Appendix A.1 Overview and Table 5; page 3, Table 1
- Evidence: Appendix A.1 逐字给出 155,753/15/5/4,000 GPU hours/L20 与房型列表；Table 5（page 13）给出逐场景帧数分布（最大 Nooks 19,851）；Table 1（page 3）给出与 HumanoidOcc 40K、EmbodiedOcc 674 的规模对比（已核对）。
- Quote: “As summarized in Table 5, Humanoid-OmniOcc dataset comprises a total of 155,753 samples, each containing four stereo pairs captured from omnidirectional viewpoints. The data are collected from fifteen simulated indoor environments, each featuring distinct spatial layouts and aesthetic styles, covering diverse room types including apartments, studios, bedrooms, dining rooms, kitchens, lounges, living rooms, offices, and patios. In addition, five real-world indoor environments (Bar, Corridor, Offi”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0649

- Claim: 规模分析：训练帧数从 15K 增至 59K 时 IoU/Precision/Recall 一致提升——更大场景覆盖带来更好的空间泛化与完整性；测试帧数从 1K 增至 9K 时各指标几乎不变（波动仅 1–2%）——学习到的表示跨测试场景泛化良好，不依赖场景特定先验或时序偏差。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 14, Appendix A.4 More Analysis and Figure 6
- Evidence: Appendix A.4 逐字；注意正文文字（15K→59K、IoU/Precision/Recall）与 Figure 6 轴标（15K/52K/104K/146K）及图例（IoU/mIoU）存在不一致——引用时以定性方向（训练扩规模有效、测试规模不敏感）为准。
- Quote: “Figure 6 (Left) illustrates the influence of training data scale on occupancy prediction performance. As the number of training frames increases from 15K to 59K, all three metrics—IoU, Precision, and Recall—consistently improve, indicating that larger scene coverage leads to better spatial generalization and completeness. We also analyze the robustness of HS 2 Occ under varying testing frame scales, as shown in Figure 6 (Right). When the number of testing frames increases from 1K to 9K, all thre”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0672

- Claim: OneCanvas 的核心表征：把来自全部视角的 patch 特征按其深度与相机位姿提升到 3D 世界坐标，再按该点相对画布原点的连续经纬度放置到单一等距柱状（equirectangular）全景画布上，不做栅格化、不做跨视图聚合；3D 位置嵌入把 patch 的度量坐标加回特征，以弥补世界位置折叠到角坐标时丢失的深度；预训练 VLM 像消费普通图像一样消费该表示，骨干无融合器、无重大架构修改。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 1, Abstract
- Evidence: 摘要与引言给出机制四要素：深度+位姿提升、连续经纬度放置（无栅格化）、3D 位置嵌入恢复度量信息、VLM 原样消费。
- Quote: “Instead, OneCanvas aggregates patch fea- tures from all views onto a single equirectangular panoramic canvas. Namely, each patch is unprojected to a 3D world coordinate using its depth and camera pose, then placed on the canvas at the continuous longitude and latitude of that point as seen from the canvas origin, with no rasterization or aggregation across overlapping views. A 3D position embedding of the patch’s metric coordinates is added to its feature, restoring the depth lost when collapsin”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0673

- Claim: 为恢复 ERP 全景折叠丢失的度量信息，OneCanvas 为每个 patch 编码画布系下的度量偏移：逐轴正弦（x/y/z 各 16 个对数间隔频率）+ 径向原语（范数与水平径距各 8 个频率）+ 单位射线方向直通，共 136 通道，经 2 层 MLP 投影后以可学习标量门加到 patch 特征上；作者强调以特征空间注入而非新增 RoPE 维度，以保持 3D-RoPE 预训练的角/时语义不变。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 5, Section 3.2, 3D position embedding
- Evidence: Sec 3.2 的 3D position embedding 段：136 通道编码 = 逐轴正弦（16 频率）+ 径向原语（8 频率）+ 单位方向直通，2 层 MLP + 学习标量门注入特征。
- Quote: “3D position embedding. A 2D VLM picks up only a class-conditioned scale prior from pix- els, not a metric reading of the actual layout. We supply explicit per-patch metric position by encoding the canvas-frame offset q i = (q x , q y , q z ) as the concatenation of (i) per-axis sinusoids {sin(ω k q a ), cos(ω k q a ), q a } for a ∈ {x, y, z} at 16 log-spaced frequencies ω k ∈ [0.1, 100] rad/m, (ii) the same form on the radial primitives ∥q i ∥ and r xz = p q 2 x + q 2 z at 8 log-spaced f”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0674

- Claim: 作者声称：由于全景画布可以以任意感兴趣的位姿为原点，同一表征直接支持从特定视角出发的情境推理（situated reasoning）——这是机器人与具身智能的常见需求；摘要亦把机器人、AR 助手、自主代理的空间问答动机作为 3D 场景理解的目标场景。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 1, Abstract
- Evidence: 摘要明确 canvas 可中心化于任意 pose of interest、直接支持 situated reasoning、是 robotics and embodied AI 的 common requirement；引言列举机器人/AR/自主代理的空间问题需求。
- Quote: “Because the canvas can be centered on any pose of interest, the same representation directly supports situated reasoning from a specific viewpoint, a common requirement in robotics and embodied AI.”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0675

- Claim: 作者给出采用全景表征的动机：全景图像表征提供 360° 视场，天然保持长程空间关系，该性质已被场景理解与近期的 3D 视觉定位工作利用。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 4, Section 2, Unified scene representations
- Evidence: 相关工作『Unified scene representations』段首句：panoramic representations offer a 360° field of view that naturally preserves long-range spatial relationships。
- Quote: “Unified scene representations. Panoramic image representations offer a 360 ◦ field of view that nat- urally preserves long-range spatial relationships, a property exploited for scene understanding Zheng et al. [2025c] and recently for 3D visual grounding.”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0677

- Claim: 在 SQA3D（3D 情境问答）上 OneCanvas 取得 65.3 EM@1，比此前最佳方法高 2.3 个百分点，为该基准新 SOTA。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 3, Section 1, Introduction
- Evidence: 引言结果句：state of the art on SQA3D (65.3 EM@1, 2.3 points above the previous best)；Table 1 中此前最佳为 Ross3D 63.0 EM@1。
- Quote: “OneCanvas reaches state of the art on SQA3D Ma et al. [2023] (65.3 EM@1, 2.3 points above the previous best),”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0678

- Claim: OneCanvas 同时在 VSI-Bench 取得 70.1 平均分、在 SPBench 零样本取得 72.1 总分（高于次佳 4.8 个百分点），并且训练计算量比最强竞争方法低一个数量级（作者归一化口径：290 vs 最高 27,648 A100 等效 GPU 小时）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 3, Section 1, Introduction
- Evidence: 引言结果句给出 VSI-Bench 70.1 average、SPBench 72.1 zero-shot overall（+4.8）、order of magnitude less training compute；Appendix B Table 7 归一化计算量 290 A100-equiv GPU-h。
- Quote: “VSI-Bench Yang et al. [2025a] (70.1 average), and SPBench Li et al. [2026] (72.1 zero-shot overall, 4.8 points above the next best method), while using an order of magnitude less training compute than the strongest competing methods (Figure 2,”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0679

- Claim: SQA3D 分题型结果（Table 1）：OneCanvas 总体 65.3 EM@1 / 68.4 EM@R1，超过最强基线 Ross3D（63.0 / 65.7）；最直接检验情境推理的题型上优势最大——Which 74.4（Ross3D 60.1）、Can 75.4（70.4）、Others 70.5（60.1）；正文指出剩余差距集中在依赖文本先验的 Is（是/否）与 How（计数）题型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 8, Table 1 and Section 4.2 (page 7)
- Evidence: Table 1 行：OneCanvas 62.1/76.2/61.1/75.4/74.4/70.5 \| 65.3 \| 68.4 对 Ross3D 56.0/79.8/60.6/70.4/55.3/60.1 \| 63.0 \| 65.7；Sec 4.2 叙述 best on Which/Can/Others、gap 集中在 Is/How。
- Quote: “Ross3D Wang et al. [2025a] 56.0 79.8 60.6 70.4 55.3 60.1 63.0 65.7 OneCanvas (Ours) 62.1 76.2 61.1 75.4 74.4 70.5 65.3 68.4”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0680

- Claim: SPBench 零样本评测（Table 2）：OneCanvas 总分 72.1、多视角子集平均 81.5（数值题 79.0、多选题 91.8），超过次佳 SpaceMind（总分 67.3、多视角 73.8）；单图子集平均 62.8 亦居首（SpaceMind 59.7）。正文将多选题上的最大增益归因于单一全景画布给多视角问题统一参考系、免于 VLM 逐视图拼接。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 8, Table 2 and Section 4.2 (page 7)
- Evidence: Table 2 行：OneCanvas 72.1 \| 79.0 91.8 81.5 \| 62.8 62.7 62.8 对 SpaceMind 67.3 \| 76.2 70.5 73.8 \| 66.3 53.2 59.7；Sec 4.2 归因于 unified frame of reference。
- Quote: “SpaceMind Zhao et al. [2025] 67.3 76.2 70.5 73.8 66.3 53.2 59.7 OneCanvas (Ours) 72.1 79.0 91.8 81.5 62.8 62.7 62.8”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0681

- Claim: VSI-Bench 八子任务（Table 3）：OneCanvas 总平均 70.1 居首；优势最大的是路径规划（Route）59.8（表内次佳 SenseNova-SI 48.5）；房间大小 76.5 领先；相对距离 71.0、相对方向 84.8 居第二；但物体计数 68.4 明显低于 SpaceMind 73.3 与基础 VLM 基线 71.3。正文称路径规划最直接检验统一全景画布上的多步推理。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 8, Table 3 and Section 4.2 (page 7)
- Evidence: Table 3 行：OneCanvas 70.1 \| 68.4 59.5 75.4 76.5 \| 71.0 84.8 59.8 65.7；SpaceMind 69.6 \| 73.3 ...；SenseNova-SI 68.8 ... 48.5；Base VLM Obj.Cnt 71.3 来自 Table 4（page 9）。
- Quote: “Cambrian-S Yang et al. [2026] 67.5 73.2 50.5 74.9 72.2 71.1 76.2 41.8 80.1 SenseNova-SI Cai et al. [2026] 68.8 72.0 53.5 76.8 72.8 69.6 80.8 48.5 76.4 SpaceMind Zhao et al. [2025] 69.6 73.3 61.4 77.3 74.2 67.2 88.4 44.3 70.6 OneCanvas (Ours) 70.1 68.4 59.5 75.4 76.5 71.0 84.8 59.8 65.7”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0682

- Claim: 训练算力对比（Table 7，作者 A100 等效归一化）：OneCanvas 两阶段合计约 72.5 小时 × 8×A6000（580 原始 GPU 时）= 290 A100 等效 GPU 时；对比 VLM-3R 240、ViCA 1,320（4.6 倍）、SpaceMind 4,800（17 倍）、SenseNova-SI 27,648（95 倍）；作者并披露归一化仅按峰值 TFLOPS、偏向低估对手算力（对己方不利），且带带宽约束的保守换算下数量级结论不变。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 14, Appendix B, Table 7
- Evidence: Appendix B Table 7/9：OneCanvas 290 A100-equiv GPU-h；ViCA 1,320（4.6×）、SpaceMind 4,800（17×）、SenseNova-SI 27,648（95×）；GPU 归一化方法与保守性讨论在 Table 8 与正文。
- Quote: “OneCanvas (Ours) A6000 8 ≈72.5 h 580 290 VLM-3R Fan et al. [2026] H200 16 5 h 80 240 ViCA Feng [2025] H100 8 55 h 440 1,320 SpaceMind Zhao et al. [2025] H100 64 25 h 1,600 4,800 SenseNova-SI Cai et al. [2026] H100 † 128 72 h 9,216 27,648”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0683

- Claim: 组件消融（Table 4，VSI-Bench）：完整模型 70.1；去掉 3D 位置嵌入降至 69.0（房间大小 76.5→69.8，降幅集中于度量型子任务）；再去掉 stage-1 空间预训练（仅 Panorama+3D PE）降至 66.6（路径规划 59.8→46.4）；仅全景画布（Panorama only）63.7；基础 VLM 多视角输入 63.5。归因：空间预训练课程主要支撑路径规划，3D 位置嵌入主要支撑度量读数，统一全景表征对跨场景关系任务（相对方向提升最大）贡献显著。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 9, Section 4.3 and Table 4
- Evidence: Table 4：Full 70.1 / w/o 3D PE 69.0 / Panorama+3D PE 66.6 / Panorama only 63.7 / Base VLM 63.5；正文归因 route 由 stage-1 支撑、room size 由 3D PE 支撑、相对方向提升来自统一全景。
- Quote: “Full model (ours) 70.1 68.4 59.5 75.4 76.5 71.0 84.8 59.8 65.7 Full w/o 3D PE 69.0 68.5 55.9 75.3 69.8 68.9 86.2 63.4 63.8 Panorama + 3D PE 66.6 67.6 53.7 75.6 71.5 70.4 85.9 46.4 61.3 Panorama only 63.7 67.3 52.1 75.8 56.2 69.3 83.6 44.3 60.4 Base VLM (multi-view) 63.5 71.3 50.3 74.8 66.0 67.9 72.2 41.8 63.4”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0685

- Claim: 画布原点消融（Table 5，SQA3D 同一检查点）：以智能体位姿（位置+朝向）为原点得 65.3 EM@1；场景中心 61.2、随机相机 61.4、场景外 59.8。视角依赖题型差距最大——Which 在智能体位姿下 74.4，对场景中心 58.7、随机相机 57.5、场景外 53.0；正文指出 Is/How 等视角无关题型不受原点策略影响，场景外原点则一致变差。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 9, Section 4.3 and Table 5
- Evidence: Table 5：Agent pose 65.3 EM@1（Which 74.4）对 Scene center 61.2（58.7）、Random camera 61.4（57.5）、Outside scene 59.8（53.0）；Sec 4.3 叙述 agent-pose centering 驱动 Which 题型的大部分增益。
- Quote: “Agent pose 62.1 76.2 61.1 75.4 74.4 70.5 65.3 68.4 Scene center 60.3 76.1 60.4 68.9 58.7 62.4 61.2 64.3 Random camera 61.1 76.2 61.9 68.9 57.5 62.6 61.4 64.6 Outside scene 59.5 75.3 60.6 68.3 53.0 59.1 59.8 62.7”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-1400

- Claim: Sphere-VIO 的应用方式：面向异构多相机系统的轻量滤波式 VIO——以统一球面表示管理多相机（含鱼眼/超广角）图像，CPU-only 实时状态估计，面向资源受限机器人。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 1, Abstract and I. Introduction
- Evidence: 摘要声明三模块（USPM/HOFA/ESKF）与'accuracy, robustness, efficiency, and cross-camera generality'折衷；III 节展开设计。
- Quote: “To address these issues, we present Sphere-VIO, a lightweight filter-based VIO framework with unified spherical representation for heterogeneous multi- camera systems.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1401

- Claim: USPM 统一球面全景模型：支持所有标准相机模型（Kalibr 兼容：pinhole、MEI 等），实现多相机图像与共享球面空间的双向快速映射，无需顺序拼接——简化跨相机特征管理并提升三角化效率。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 1, Abstract and I. Introduction
- Evidence: 摘要声明 USPM 能力；III-A 节式(1)-(9) 给出双向映射公式链与 Kalibr 兼容物理投影算子。
- Quote: “Specifically, we first propose a Unified Spherical Panorama Model (USPM) that supports all standard camera models and enables bidirectional fast mapping between multi- camera images and a shared spherical space without sequential stitching, simplifying cross-camera feature management and improving triangulation efficiency.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1402

- Claim: USPM 的通用性边界宽松：面向任意多相机 rig 设计（不要求全 360° 覆盖，窄 FoV 前视双目也可工作），把所有相机图像统一到单一球面——统一表示不强制全景硬件。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 2, Section III-A
- Evidence: III-A 开篇明确 USPM 灵活性声明；这解释了 EuRoC/TUM-VI 针孔双目数据集上的可运行性。
- Quote: “We propose the USPM for arbitrary multi-camera rigs, unifying all camera images onto a single spherical surface. USPM is flexible: it does not require full 360° coverage and even works with narrow-FOV forward stereo rigs.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1405

- Claim: HOFA 分层全向特征对齐的任务自适应策略：新特征做跨相机深度估计+范围过滤（FOV-极线约束推导的可行逆深度集合），预三角化特征直接复用可靠深度——两种深度源共同支撑全景级半直接 patch 匹配。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 3, Section III-B
- Evidence: III-B 首段给出策略；式(10)-(11) 为对齐与逆深度优化、式(12)-(14) 为可行深度集合推导、Vogiatzis 滤波收敛（page 3-4）。
- Quote: “Building on SVO 2.0 [15], we propose the HOFA frame- work for USPM. It adopts a task-adaptive strategy: new features undergo cross-camera depth estimation with range filtering, while pre-triangulated features directly reuse their re- liable depth.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1406

- Claim: 全景上的轻量化特征选择：沿用 PAN-SLAM 在完整全景上提取全局特征的思路，但改用轻量 FAST 关键点替代 ORB 以最小化计算开销——宽 FoV 表示的计算代价被显式管理。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 3, Section III-A
- Evidence: III-A 末段说明全景特征提取策略；同段前句为 USPM 并行重映射（Parallel Unit 1）降低全景合成延迟。
- Quote: “Follow- ing PAN-SLAM [4], we extract global features on the full panorama, but adopt lightweight FAST keypoints instead of ORB to minimize computational overhead.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1407

- Claim: ESKF 后端核心设计：以 3D 球面 bearing 残差替换 SchurVINS 的 2D 透视重投影残差，避免全景投影下直接像素误差的强非线性；其他全景 SLAM 系统（[4] PAN-SLAM、[7] ROVINS）虽也用球面残差但依赖重量级图优化——本文保留 Schur 补管线以控制 3D 残差的额外计算。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 4, Section III-C
- Evidence: III-C 残差构造段（式(16) 残差定义、式(17) 雅可比、式(19) Schur 补 ESKF 更新）；[4]/[7] 身份见 References。
- Quote: “We replace SchurVINS’ 2D perspective reprojection resid- ual with a 3D spherical bearing vector residual tailored to USPM (Fig. 4), avoiding the strong nonlinearity of direct pixel error for omnidirectional projections [10]. While other panoramic SLAM systems [4], [7] also use spherical residuals, they rely on heavy graph optimization.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1409

- Claim: 长走廊/大范围运动鲁棒性收益：TUM-VI 平均 ATE 0.1518 m——优于滤波式 SchurVINS 48.8%（0.2965）、图优化 VINS-Fusion 63.6%（0.4171）；框架无图优化与全局建图，统一球面公式在立体方案剧烈漂移的长走廊环境带来显著鲁棒性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 5-6, Section IV-B and Table II
- Evidence: IV-B 段落给出 0.1518 与两个百分比；Table II（page 6）给出 11 序列明细（走廊 c1-c5 漂移最重）。
- Quote: “On the TUM-VI dataset, our method obtains an ATE RMSE of 0.1518 m. It outperforms the filter-based SchurVINS by 48.8% and surpasses the graph-optimized VINS-Fusion by 63.6%. Notably, our framework operates without graph optimization or global mapping, and our unified spherical formulation brings prominent robustness for long-corridor environments where stereo-based alternatives suffer drastic drift.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1410

- Claim: 恶劣条件基准的稳定收益：HILTI 2022（稀疏纹理+密集运动+不均匀光照）平均 ATE 0.1821 m 总排名第二、仅次 MAVIS（0.0980）；优于 VINS-Fusion/ORB-SLAM3/SchurVINS 达 35.3%/39.7%/55.7%——多相机球面建模在恶劣条件下稳定跟踪，而窄 FoV 立体管线严重漂移。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 5-6, Section IV-B and Table III
- Evidence: IV-B 段落给出 0.1821 与三个百分比；Table III（page 6）给出 6 实验明细（SchurVINS 0.4110、VINS-Fusion 0.2813、ORB-SLAM3 0.3022）。
- Quote: “On HILTI 2022, Sphere-VIO ranks second overall with 0.1821 m ATE RMSE only inferior to MAVIS, outperforming VINS-Fusion, ORB-SLAM3 and SchurVINS by 35.3%, 39.7% and 55.7% respectively, as multi-camera spherical modeling ensures sta- ble tracking under harsh conditions while narrow-FOV stereo pipelines suffer severe drift.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1412

- Claim: 异构超广角硬件是现成 SLAM 的能力边界：自建四目 206° 鱼眼+IMU 数据集（OptiTrack 真值）上全部 4 个基线失败——ORB-SLAM3/MAVIS 的 pinhole/Kannala-Brandt 模型无法适配 >180° FoV；VINS-Fusion/SchurVINS 虽用 206° 能力的 MEI 模型，仍因发散朝向+部分重叠下的跨相机匹配挑战失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 5-6, Section IV-C1 and Table IV
- Evidence: IV-C1 段落给出全败与两层归因；Table IV（page 6）基线行全部为'-'（No valid results available, due to tracking loss, or camera model incompatibility）。
- Quote: “As shown in Table IV, all baselines fail: ORB-SLAM3 and MAVIS cannot adapt to over 180° FOV due to their pinhole or Kannala-Brandt models, while VINS-Fusion and SchurVINS, despite using 206° FOV- capable MEI models, fail due to cross-camera matching chal- lenges from divergent orientations and partial overlaps.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1413

- Claim: 多相机重叠覆盖的精度增益与嵌入式可行性：同一自建数据集上 Sphere-VIO 立体变体 0.1797 m、多相机变体提升至 0.1230 m（利用重叠覆盖）；Intel NUC 13 嵌入式平台仅轻微退化至 0.1341 m——多相机宽 FoV 配置与资源受限部署同时可行。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 5, Section IV-C1 and Table IV
- Evidence: IV-C1 段落三个数；Table IV 明细（SV stereo/MC/NUC 三行）；Table VI 给出对应每帧时间。
- Quote: “In contrast, Sphere-VIO tracks stably on all sequences: the stereo variant achieves 0.1797 m average ATE RMSE, while the multi-camera version improves to 0.1230 m by leveraging overlapping coverage. On Intel NUC 13, performance degrades slightly to 0.1341 m, confirming resource-constrained deploy- ment feasibility.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1414

- Claim: 宽 FoV 收益的初始化级机制证据：立体配置的静态三角化仅覆盖中央 90° 水平 FoV（全向全景的 1/4），区域外特征无法静态初始化、只能依赖 VIO 跟踪期深度估计引入不确定性并降低精度；四相机配置实现 360° 均匀全覆盖三角化，提供更鲁棒的初始化基础——直接解释系统级性能差距的根因。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 7, Section IV-C2 and Fig. 7
- Evidence: IV-C2 段落 + Fig. 7（page 7）四配置三角化可视化（Seeker 全向/HILTI/Seeker 立体/TUM-VI 立体）；同段确认 HILTI/TUM-VI 一致结果支撑泛化。
- Quote: “stereo configuration achieves valid static triangulation only in the central 90° horizontal FOV, covering just one-quarter of the full omnidirectional panorama, while features outside this region cannot be statically initialized and rely on depth estimation during VIO tracking, introducing uncertainty and degrading accuracy. In contrast, the four-camera configuration achieves uniform 360° full-coverage triangulation, providing a more robust initialization foundation.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1415

- Claim: 多相机宽 FoV 的 CPU 实时效率：HILTI 2022（40 Hz 相机，实时阈值 0.025 s/帧）上 SV 多相机（同时处理四路流+CLAHE 预处理）平均仅 0.0122 s/帧（约阈值一半）；立体 VINS-Fusion 0.0257 s 超限，SchurVINS 0.0036 s——宽 FoV 多相机不以牺牲实时性为代价（效率源于三并行单元线程池）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 7, Section IV-D and Table V
- Evidence: IV-D 段落给出阈值/三方法数值与并行单元归因；Table V（page 7）给出 6 实验逐项时间。
- Quote: “With 40 Hz cameras, HILTI 2022 requires per-frame latency ≤ 0.025 s for real-time operation. As shown in Table V, stereo VINS-Fusion (0.0257 s) exceeds this limit, while SchurVINS and Sphere-VIO run in real time. Our multi- camera Sphere-VIO, processing four streams with CLAHE preprocessing, averages only 0.0122 s per frame, nearly half the threshold.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1416

- Claim: 嵌入式部署效率：自建 20 Hz 数据集（实时阈值 0.05 s/帧）上 SV 笔记本 0.0138 s、Intel NUC 13 嵌入式 0.0180 s——均远低于阈值，验证资源受限平台实际部署可行性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 7, Section IV-D and Table VI
- Evidence: IV-D 末句给出双平台数与结论；Table VI（page 8）给出 5 序列逐项时间。
- Quote: “Then as listed in Table VI, on our 20 Hz self-made dataset (latency limit 0.05 s, Section IV-C1), Sphere-VIO achieves 0.0138 s on a laptop and 0.0180 s on Intel NUC 13. Both are well within the limit, verifying practical deployment feasibility.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-0520

- Claim: HiFi-UMI 的核心 FoV 升级：每手搭载两个非平行鱼眼相机（上下布置），实现约 200° 的水平与垂直覆盖；该超广视图减少遮挡并改善夹爪周围的可观测性，与头部立体对合计整机六相机。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 8, Section 3.1.3 Cameras and Sensors
- Evidence: Sec. 3.1.3 逐字给出每手两个非平行鱼眼、~200° 水平/垂直覆盖、减少遮挡改善可观测性的设计陈述。
- Quote: “Each hand carries two non-parallel fisheye cameras, yielding about 200 ◦ of horizontal and vertical coverage. This ultra-wide view reduces occlusion and improves observability around the gripper. Together with the stereo head cameras, the complete device integrates six cameras.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0521

- Claim: Table 1 对八款免机器人采集系统的横比中，HiFi-UMI 是唯一达到微秒级 GPIO 硬件触发同步与最宽双腕覆盖（6 视图 / 200°）的系统：UMI 原版为 2 视图 / 155° + ~6ms 软件同步，FastUMI Pro 为 2 视图 / 180°。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 9, Table 1 and caption
- Evidence: Table 1 横比 pose 采集/精度/同步/视图-FoV/相对位姿/夹爪形态/便携性八轴；caption 总结 HiFi-UMI 优势为 ~3mm 精度、GPIO 微秒同步、最宽双腕覆盖与免基站便携。
- Quote: “Together, these choices yield HiFi-UMI’s main advantages over prior systems: millimeter-level end-effector accuracy (∼3 mm) obtained from head-mounted offline stereo-inertial SLAM without external tracking infrastructure; the tightest, microsecond-level synchronization via a GPIO hardware trigger; the widest sensing coverage at both hands; and greater ease of use—fully portable with no external base stations, and operated through a full-palm glove rather than a trigger for more natural manipulat”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0522

- Claim: 整机传感集成：六相机（头部立体对+每手双非平行鱼眼）+ 头/双手 IMU + 夹爪高精度编码器，全部传感器由单一统一 GPIO 外部触发驱动，实现跨所有相机、IMU 与编码器的微秒级时间同步，取代先前系统的软件/无线对齐并消除一类动作标签噪声。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 8, Section 3.1.3 Cameras and Sensors
- Evidence: Sec. 3.1.3 逐字描述六相机+IMU+编码器由单一 GPIO 外部触发做微秒级同步，并声明其取代软件对齐消除动作标签噪声。
- Quote: “Together with the stereo head cameras, the complete device integrates six cameras. It further carries IMUs on the head and both hands—for pose estimation and motion-state monitoring—and high-precision encoders on the grippers to measure opening angle. Critically, every sensor is driven by a single, unified GPIO external trigger [53], providing microsecond-level temporal synchronization across all cameras, IMUs, and encoders.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0523

- Claim: 策略的全部视觉观测固定取自采集装置的四个腕视图（每手两个鱼眼视图），对每个 backbone 与每个训练条件一致；头部立体对只用于采集期轨迹重建、从不作为策略输入——腕部鱼眼多视图是策略学习的唯一视觉接口。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 13, Section 5 Baselines and Training Setup
- Evidence: Sec. 5 接口约定逐字声明视觉观测取自四腕视图、头部立体对从不进策略，且 UMI 与 teleop 变体用相同相机选择/时间偏移/张量布局。
- Quote: “The visual observation o (m) t is drawn from the four wrist views of the capture rig—two per hand—for every backbone and every condition; the head-mounted stereo pair is used only for trajectory reconstruction during capture and is never provided as input to the policy.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0524

- Claim: 全部真机实验使用双七关节 Tianji Robotics Marvin M6 力控臂的固定双臂平台，其搭载与采集装置同款的夹爪与四个腕相机（Sec. 3.1）；头部立体对仅用于离线采集重建并在部署中被排除，策略只接收录制视图的严格子集——采集与部署的接触和观测接口物理同一。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 17, Section 6.1.1 Evaluation Benchmark
- Evidence: Sec. 6.1.1 逐字声明实验平台（Tianji Robotics Marvin M6 双臂）匹配 HiFi-UMI 末端（同夹爪+四腕相机）、头部对仅离线重建且部署排除、策略接收录制视图严格子集、采集与部署接触/观测接口物理同一；『残余差距限于臂运动学』一句位于下一页，未纳入本卡摘录。
- Quote: “All real-robot experiments use a stationary bimanual platform with two seven-joint Tianji Robotics Marvin M6 force-controlled arms. At deployment, the platform matches the HiFi-UMI end effector: it carries the same gripper and four wrist cameras described in Sec. 3.1. The head stereo pair is used only for offline capture reconstruction and excluded from deployment, so the policy receives a strict subset of the recorded views. Capture and deployment thus have physically identical contact and obse”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0525

- Claim: 端到端数据保真度：处理管线交付 3mm 末端执行器精度（~2m 工作区内对基站跟踪真值的平均平移误差）、<40μs 跨传感器时序偏移、每小时少于两帧丢帧、98% 轨迹重建成功率与 <0.1° 夹爪开角误差——作者据此主张其轨迹精度/时序/夹爪重建与真机遥操作同级。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 12, Section 3.4 and Table 2
- Evidence: Sec. 3.4 + Table 2 报告五项端到端保真度指标；3mm 精度对基站真值测量（仅用于精度评估）。
- Quote: “The pipeline delivers 3 mm end-effector accuracy, cross-sensor timing offsets below 40 μs, fewer than two dropped frames per hour of capture, a 98% trajectory- reconstruction success rate, and gripper-state error below 0.1 ◦”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0526

- Claim: 零机器人 post-training 的聚合结论：三个 backbone（两 VLA + 一 WAM）上仅用 HiFi-UMI 演示 post-training 与同域遥操作匹配，差异为 -2.5、+3.1、-0.6 个百分点，双向且均在协议采样噪声内——免机器人鱼眼腕视图数据可独立承载部署级 post-training。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 4, Section 1 and page 20, Section 6.2
- Evidence: Sec. 1 与 Sec. 6.2 一致报告三 backbone 差异数字；960 rollouts、冻结基准、双操作员分离协议。
- Quote: “On three backbones spanning both the vision-language- action (VLA) and world-action-model (WAM) families, HiFi-UMI-only post-training matches in-domain tele- operation: the differences are −2.5, +3.1, and −0.6 percentage points, of both signs and each within the sampling noise of our protocol.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0527

- Claim: VLA 轨道任务级数字：StarVLA-QwenPI 上 UMI post-training 51.3%（82/160）vs 遥操作 53.8%（86/160）；OpenPI-π0.5 上 UMI 77.5%（124/160）vs 遥操作 74.4%（119/160），其中 UMI 在 Remote Insertion 达 85.0%——teleop 数据在评估场景内采集而 UMI 零轨迹在该场景。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 20-21, Section 6.2.1 and Fig. 9
- Evidence: Sec. 6.2.1 聚合比较段给出两 VLA backbone 的四任务汇总数字；Remote Insertion 85.0% 见任务级对比与 Fig. 9。
- Quote: “On StarVLA-QwenPI, the UMI-post-trained policy achieves 51.3% success (82/160), compared with 53.8% (86/160) for its teleoperation-trained counterpart, corresponding to a difference of only 2.5 percentage points. On OpenPI-π 0.5 , UMI post-training achieves 77.5% success (124/160), exceeding teleoperation post-training at 74.4% (119/160) by 3.1 percentage points.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0528

- Claim: 腕视图策略的纯 UMI 数据量-性能曲线：Remote Insertion 上 400 条演示 37.5% → 800 条 65.0% → 1,600 条 70.0% → 3,200 条 85.0%，6,400 条 82.5% 饱和——部署级性能可通过规模化免机器人鱼眼腕视图数据获得，无需真机锚点。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 22, Section 6.2.1 and Fig. 10a
- Evidence: Sec. 6.2.1 data-scaling 研究：OpenPI-π0.5 五档数据量各 40 rollouts；低数据区增益陡峭，~3,200 条后平台化。
- Quote: “The success rate improves from 37.5% with 400 demonstrations to 65.0% with 800 demonstrations, indicating that additional UMI trajectories rapidly improve the policy’s ability to acquire the basic manipulation skill. Further scaling to 1,600 and 3,200 demonstrations continues to improve performance, reaching 70.0% and 85.0% success rates, respectively.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0529

- Claim: 同源大规模预训练的下游增益：4,000 小时 HiFi-UMI 预训练在架构与 post-training 配方固定的对照下使 StarVLA-QwenPI 聚合真机成功率 +18.1 个百分点（擦拭/折叠/插入增益最强），且 800 条任务数据即超过 4× 数据的 scratch 基线——鱼眼腕视图语料的预训练先验同时改善数据效率与性能上限。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 27, Section 6.3 and Fig. 15 / Fig. 10b
- Evidence: Sec. 6.3：C1 vs C7 初始化对照（同 3,200 episodes post-training，仅换初始化）；+18.1pp 见 Fig. 15 与正文；800-episode 超基线见 Fig. 10b。
- Quote: “UMI pre-training raises aggregate StarVLA-QwenPI success by 18.1 percentage points, with particularly strong gains on wiping, folding, and insertion. Because the architecture and post-training recipe are fixed, this improvement can be attributed to the visual-motor initialization rather than additional task-specific supervision.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0726

- Claim: 论文主张：现代具身系统普遍依赖多相机 3D 感知——机器人策略常用工作区相机+腕戴相机组合捕捉任务级上下文与局部操作细节，自动驾驶与导航系统用环视 rig 做大范围感知、占据推理与规划；此类系统常混合不同视点、分辨率与 FoV 的相机，其中窄/标准 FoV 针孔相机保留远处细节，宽 FoV 或鱼眼相机提供近场与周边覆盖。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 2, Section 1 Introduction
- Evidence: 引言把'异构多相机 rig'定位为具身系统常态而非例外：鱼眼负责近场/周边、针孔负责远距细节的分工是异构深度问题的出发点；紧随其后指出针孔中心假设的现有深度/3D 基础模型在此设置下失效。
- Quote: “In modern embodied systems, these requirements are commonly supported by multi-camera 3D perception. Multiple views expand spatial coverage, reduce occlusion, and provide complementary geometric cues for scene understanding. Robot poli- cies commonly combine workspace and wrist-mounted cameras to capture both task-level context and local manipulation details [7, 29, 49], while autonomous driving and navigation systems use surround-view rigs for wide-area perception, oc- cupancy reasoning, and pl”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0727

- Claim: X-Lens 用通用反投影映射 G 替换针孔内参来抽象异构相机：G 把连续像素坐标映射为后投影单位射线，吸收逐相机标定（焦距、主点、畸变系数）与显式相机类型指示符 τ∈{pinhole, fisheye}；网络内所有下游几何推理在射线空间而非像素坐标空间进行；无闭式投影模型的相机用训练时采样的表格化径向轮廓实现 G，从而同一网络无需任何架构修改即可直接吸收 pinhole、鱼眼与 360° 相机的异构混合。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 4, Section 3.1 Formulation and Design Principles
- Evidence: 通用相机表示是 X-Lens 异构能力的根基：把相机差异全部归一化到射线空间，使下游模块（注意力偏置、位置编码、尺度池化）与具体投影模型解耦，这解释了为何同一模型可覆盖 pinhole/鱼眼/360° 混合而无需架构改动。
- Quote: “To handle multi- view heterogeneous configurations, X-Lens abstracts cameras away from specific projection models and replaces the pinhole intrinsic with a generic unprojection map G. Each view s is formally specified as: r s,p = G(p; ξ s , τ s )R s , r s,p ∈ S 2 , p ∈ [0, W ] × [0, H], (1) where G maps a continuous pixel coordinate p to a back-projected unit ray. It absorbs both the per-camera calibration ξ s , including focal lengths, principal point, and distortion coefficients, and an expl”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0728

- Claim: X-Lens 的多视图校准 token 机制：引入按 Transformer 层、相机类型、token 数、维度索引的可学习校准 token 张量，逐层执行'注入-参与注意力-丢弃'（inject-attend-drop）过程，切片注入每一层（含跨视图层）；跨视图层内注意力掩码使 token 只注意自己所在视图、不向全局度量融合添加相机类型信号；token 仅对鱼眼视图注入（针孔通路不变）且零初始化、从恒等起点渐进学习；与单目校准 token 前作 [15] 的区别在于 token 按层与相机类型特化、经掩码保持视图局部，把镜头校正限制在各视图内以保护异构设置依赖的跨视图度量融合。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 6, Section 3.2 Multi-View Calibration Tokens
- Evidence: 该设计把'鱼眼镜头校正'与'跨视图度量融合'解耦：token 只在视图内吸收镜头畸变、不进入全局融合；仅鱼眼注入意味着针孔通路与性能不受适配影响——这是与 Fisheye3R（token 全局参与注意力）不同的工程取舍。
- Quote: “Heterogeneous inputs carry distinct per-lens distortion patterns. To keep these from being absorbed indiscriminately by the shared visual tokens, we introduce a learnable calibration-token tensor Θ ∈ R N L ×T ×K×C indexed by Transformer layer N L , camera type T , token count K, and dimension C. At each layer i, the type-specific slice Θ[i, τ s ] is appended to view s’s token sequence, attends, and is then dropped before the next layer re-injects a fresh slice, forming an inject-attend-drop proc”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0729

- Claim: 跨视图几何兼容通过 Jacobian 畸变偏置注入全局注意力：作者指出校准 token 提供视图局部镜头适配，而可靠的异构匹配还需跨视图几何兼容性，这在鱼眼-针孔跨视图交互中尤为重要——因非线性投影，视觉对应的区域可能占据差异极大的图像平面邻域；偏置作用于跨视图层的全部 patch token，从逐 patch 射线与反投影 Jacobian J=[∂r/∂u, ∂r/∂v]（patch 网格上有限差分估计）构造 9 维相对描述符（角一致性/射线点积、相对局部尺度/log 范数差、射线位移、Jacobian 相关），经轻量逐头 MLP 转为 Softmax 归一化前的加性偏置，促使跨视图注意力偏向 3D 射线几何与局部投影结构兼容的 patch 对，而非仅依赖畸变图像坐标中的外观相似性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 6, Section 3.2 Jacobian Distortion Bias
- Evidence: 机制要点是把'局部投影变化'量化为 Jacobian 并转为注意力偏置：外观相似的 patch 若射线几何不兼容将被降权；这是对'鱼眼-针孔对应难'的几何先验式解法，消融（C10）证明其在全部相机设置有效。
- Quote: “Jacobian Distortion Bias Calibration tokens provide view-local adaptation for lens-specific distortions, whereas reliable heterogeneous matching also requires cross-view geometric compatibility. This is particularly important for fisheye–pinhole cross-view interactions, where visually corresponding regions can occupy very different image-plane neighborhoods due to non-linear projection. We therefore introduce the Jacobian Distortion Bias in the cross-view attention layers L g . The bias is appl”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0730

- Claim: 鱼眼视图的周边区域径向压缩、倾向携带更大几何不确定性，直接池化所有空间特征回归度量尺度会使预测偏向低可靠的畸变区域；为此 X-Lens 引入 Scale Attention 置信度引导池化：用预测置信图选取空间可靠区域，丢弃置信最低的 25% 像素，对剩余核心集做置信度加权池化来回归全局度量尺度，以降低对鱼眼边界伪影的敏感性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 7, Section 3.2 Geometric Rotary Position Embedding and Scale Attention
- Evidence: 该卡同时携带限制证据（鱼眼周边低可靠、会污染尺度回归）与方法证据（置信引导池化规避）；周边区低置信也解释了模型为何需要显式置信输出通道，与 Fig.9 偏置集中在鱼眼边界区（C11）互为印证。
- Quote: “In fisheye views, peripheral regions are radially compressed and tend to carry larger geometric uncertainty. Directly pooling all spatial features to regress the metric scale ˆm can therefore bias the prediction toward distorted regions with low reliability. For robust metric scale estimation, we introduce Scale Attention, a confidence guided pooling mechanism that uses the predicted confidence map ˆ C to select spatially reliable regions. The lowest confidence 25% of pixels are discarded, and”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0731

- Claim: X-Lens 采用渐进三阶段训练：先用多视图针孔数据训练基础网络学习尺度感知几何表示（校准 token 与 Jacobian 偏置禁用）；再冻结主干、射线编码器与预测头，仅更新校准 token 做鱼眼适配，把径向压缩与非线性镜头效应限制在专用 token 通路、不覆写 Stage-1 学到的针孔表示；最后激活 Jacobian 畸变偏置，在鱼眼-针孔混合多视图数据与 Stage-1 纯针孔数据上联合微调，训练跨视图注意力在统一射线空间表示下调和异构图像平面畸变——该调度先隔离镜头适配再做联合训练，减少针孔先验与鱼眼畸变建模之间的干扰。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 7, Section 3.3 Multi-Stage Heterogeneous Training Strategy
- Evidence: 三阶段的动机是防止鱼眼适配覆写针孔几何先验；Stage-3 混入纯针孔数据回放是因为 OmniScene 两个针孔视图几乎无重叠——附录 B.2 消融（Table 7）验证回放以近零异构/鱼眼代价恢复针孔性能。
- Quote: “X-Lens is trained with a progressive three-stage pipeline that moves from homogeneous pinhole geometry to fisheye adap- tation and finally to heterogeneous multi-camera optimization. This schedule isolates lens-specific adaptation before joint training, reducing interference between pinhole priors and fisheye distortion modeling. The goal is to first obtain a stable multi-view geometric backbone, then introduce fisheye-specific parameters under a controlled optimization regime, and only afterwar”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0732

- Claim: 为弥合多相机几何感知数据缺口，作者发布 OmniScene 大规模合成数据集：用标定六相机 rig（四鱼眼+两针孔）渲染，针对现有资源的两个缺口——多样宽 FoV 鱼眼数据稀缺、缺带稠密度量真值的同步异构基准；覆盖住宅、办公、商场、仓库、城市、科幻综合体与风格化时代室内等室内外场景（Kujiale 与 Unreal Engine 资产）；含 103 个复杂场景、564 条随机运动序列、约 266K 多视图帧（六相机 rig 超过 1.7M 张图像），每帧配稠密无噪声度量真值；四鱼眼相机围绕平台中心排列、重叠 FoV 捕捉水平环视上下文，遵循 Kannala-Brandt 投影模型、提供 180° FoV；前后两针孔相机补足远距细节；全部相机 504×798 同步渲染并提供 OpenCV 约定内外参，模型可直接使用标定几何而无需去畸变或手工校正。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 8, Section 4 The OmniScene Dataset
- Evidence: OmniScene 是论文异构评测的支柱；其鱼眼设定（KB 模型、180° FoV）划定了方法验证过的投影空间，也是作者自述'极端 FOV 镜头存在 sim-to-real gap'（C14）的成因之一；真实异构 rig 定量评测的缺位由此数据集的合成性质引出（C15）。
- Quote: “To bridge the gap in multi-camera geometric perception, we introduce OmniScene, a large-scale synthetic dataset for multi-view metric depth estimation with heterogeneous cameras. It is rendered with a calibrated six-camera rig containing four fisheye and two pinhole views. It targets two key limitations in existing resources: (i) the scarcity of diverse wide-FOV fisheye data, and (ii) the lack of synchronized heterogeneous benchmarks with dense metric ground truth. Unlike driving-centric dataset”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0733

- Claim: 同构鱼眼设置下 X-Lens（0.04B）保持强度量精度与最高速度：单目 KITTI360 上取得所有对比方法中最佳 Scale AbsRel（0.0955）、AbsRel（0.2110）、RMSE（4.1961）同时 41 FPS（基线 4-8 FPS）；用两个时序分离的 KITTI360 帧作输入时进一步超过单目变体，Scale AbsRel 再降 12.9%、RMSE 降 3.6%，说明跨视图约束提供了单目推理之外的几何证据；OmniScene-Single 上最佳 Scale AbsRel/AbsRel/RMSE；四视图 OmniScene-Quad 上在所有报告精度指标上一致超过 MapAnything（1.23B）、DepthAnyCamera、UniDAC 并保持 24 FPS，参数比 MapAnything 少 96.7%。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 11, Table 1 and Section 5.1 Fisheye Cameras
- Evidence: Table 1 显示加第二个时序帧的跨视图增益（KITTI360 −12.9% Scale AbsRel）；四鱼眼 24 FPS 接近实时；鱼眼设置对比的多为单目/通用相机模型，MapAnything 是唯一多视图基线且 Scale AbsRel 严重失准（OmniScene-Quad 1.0455）。
- Quote: “Table 1. Fisheye evaluation on monocular KITTI360 [37], monocular OmniScene-Single, and four-view OmniScene-Quad. FPS is reported at the native evaluation resolution of each dataset. The best result on each dataset is highlighted in bold. Dataset Views Method Params Scale AbsRel ↓ AbsRel ↓ RMSE ↓ δ 1 ↑ τ 1.03 ↑ FPS ↑ KITTI360 [37] 1 UniDepthv2-Small [54] 0.03B 0.1597 0.2597 7.4067 0.6931 0.1803 7 UniDepthv2-Large [54] 0.35B 0.1787 0.2718 8.0432 0.7091 0.1860 5 Metric3Dv2-Small [19] 0.03B 0.263”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0734

- Claim: 异构六视图（4 鱼眼+2 针孔）OmniScene-Full 上 X-Lens 取得全部报告指标最佳：Scale AbsRel 0.1181、AbsRel 0.1021、RMSE 1.5993、δ1 0.8982、τ1.03 0.3724，22 FPS；对比 MapAnything 1.23B（0.3701/0.1746/2.1834/0.7357/0.1647，5 FPS）Scale AbsRel 降低 68.1%、参数少 96.7%、速度快四倍以上；对比 AbsRel 最强基线 UniDAC 0.36B（AbsRel 0.1368）AbsRel 降低 25.4%、参数少 88.9%（与摘要口径一致）。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 13, Table 3 and Section 5.2 Heterogeneous Cameras
- Evidence: 25.4%/88.9% 由 Table 3 行直接可算（UniDAC AbsRel 0.1368→0.1021；参数 0.36B→0.04B），摘要同口径陈述；作者据此主张显式异构建模是混合 rig 实时度量感知的实用路径。注意该基准为自建合成集（见 C15 的外推边界）。
- Quote: “Table 3. Heterogeneous-camera evaluation OmniScene-Full with six input views (4 fisheye + 2 pinhole). FPS is measured at 504 × 798 resolution. The best result is highlighted in bold. Dataset Views Method Params Scale AbsRel ↓ AbsRel ↓ RMSE ↓ δ 1 ↑ τ 1.03 ↑ FPS ↑ OmniScene-Full 6 MapAnything [28] 1.23B 0.3701 0.1746 2.1834 0.7357 0.1647 5 DepthAnyCamera [92] 0.06B 0.2571 0.2066 2.3981 0.7653 0.2411 1 UniDAC [14] 0.36B 0.2506 0.1368 2.6125 0.8156 0.2511 1 Ours 0.04B 0.1181 0.1021 1.5993 0.8982 0”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0735

- Claim: 消融显示每个训练阶段与 Jacobian 偏置均必要：仅 Stage-1（纯针孔训练）在混合相机下表现差（异构 AbsRel 0.7563）——针孔-only 训练无法处理鱼眼畸变；仅 Stage-2 改善稠密深度但缺异构联合优化仍受限（0.3952）；Stage-3 冻结主干也次优（0.2333），说明共享表示必须适应混合相机几何；去掉 Jacobian 畸变偏置在全部评测相机设置退化（异构 AbsRel 0.1021→0.1912、Scale AbsRel 0.1181→0.1801；针孔 OmniOcc Scale AbsRel 0.0670→0.5631），证明偏置改善跨视图几何对齐并在异构与针孔数据混合训练时正则化泛化；完整模型（三阶段+校准 token+Jacobian 偏置）在三个设置的完整结果中取得最佳。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 15, Table 4 and Section 6 Ablation Study
- Evidence: Stage-1-only 0.7563 为'针孔/透视中心模型对鱼眼的域差'提供第三个独立量化数据点（与 Fisheye3R 未适配基线退化一致）；w/o Jacobian bias 在纯针孔设置也大幅退化（0.5631）略反直觉，作者归因于偏置对混合训练的正则化作用而非纯几何 necessity。
- Quote: “Table 4. Ablation of training stages and geometry modules. The heterogeneous setting uses OmniScene-Full with four fisheye and two pinhole cameras. The fisheye-only setting uses fisheye cameras. The pinhole-only setting uses six-view OmniOcc. Cameras Views Variant Scale AbsRel ↓ AbsRel ↓ RMSE ↓ δ 1 ↑ τ 1.03 ↑ Heterogeneous 6 Stage-1 only 0.3026 0.7563 2.4716 0.4811 0.1156 Stage-2 only 0.3308 0.3952 2.2159 0.6264 0.1331 Stage-3 frozen 0.2886 0.2333 2.6006 0.7436 0.1743 w/o Jacobian bias 0.1801”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0736

- Claim: 偏置修正幅度的可视化（Fig. 9）显示：鱼眼视图在高畸变边界区域需要更大幅度的修正，而针孔视图呈现更平滑、空间更均匀的修正——反映针孔近似线性投影不需要修正场的快速空间变化。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 14, Figure 9
- Evidence: 与 Scale Attention 丢弃低置信周边像素（C05）互补：几何修正需求也集中在鱼眼边界；两条证据共同界定鱼眼图像'中心可靠、周边难'的结构，对综述'鱼眼哪些区域受限'给出跨论文一致答案。
- Quote: “Figure 9. Visualization of the bias-correction magnitude from B in Equation (4). Fisheye views require larger corrections in highly distorted boundary regions, while pinhole views show smoother and more spatially uniform corrections, reflecting their approximately linear projection, which does not require rapid spatial changes in the correction field.”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0738

- Claim: 具身下游初步证据：在 RoboTwin2 Scan-Object (Easy) 任务上，X-Lens 视觉表征结合 VO-DPP 策略框架的任务成功率（TSR）为 72%，超过 DINOv3-Base（50%）、DINOv3-Large（55%）与 VGGT（67%）——四种编码器在同一 VO-DPP 框架、相同训练配置（300 epoch、lr 1e-5）下的对照。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 21, Table 5 (Appendix A.2)
- Evidence: 附录 A 说明集成方式：不喂刚体重建点云或显式深度图（量化误差+丢语义），而是直接路由灵活的自注意力 token，保留任务语义与空间先验；但作者自述为单任务初步案例研究（preliminary case study），且对照基线 VO-DPP 算法当时未公开发布，结论外推需谨慎。
- Quote: “Table 5. Preliminary case study of different visual representation algorithms combined with VO-DPP on RoboTwin2 Scan-Object (Easy) downstream task success rate. Variant visual encoder epoch learning rate TSR(%) With dinov3-base training 300 1e-5 50 With dinov3-large training 300 1e-5 55 With VGGT training 300 1e-5 67 With Ours training 300 1e-5 72”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0919

- Claim: 方法设计：RayTun3R 冻结预训练网络主干，仅适配与 token 位置和相机几何绑定的轻量组件——学习对绝对与旋转位置编码（PE/RoPE）的参数高效残差修正，配合免参数的 tokenization 与预测网格坐标修正以移除残余针孔假设；适配器仅含 10,752 个可训练参数，可从短时段片段用几何损失学得，适配后无额外推理开销地迁移到序列其余帧。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 1, Abstract
- Evidence: 摘要方法段完整给出：冻结主干 + PE/RoPE 残差 + 免参数修正 + 10,752 参数 + 短时段几何损失 + 零推理开销。
- Quote: “It keeps the pretrained network fixed and adapts only lightweight components tied to token position and camera geometry. RayTun3R learns parameter-efficient residual corrections to absolute and rotary positional encodings, together with parameter-free tokenization and corrections to prediction- grid coordinates that remove residual pinhole assumptions. The resulting adapter contains only 10,752 trainable parameters and can be learned from a short temporal segment using geometric losses. Once ada”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0920

- Claim: 头条效果：在视场角 110°–200° 的多样鱼眼数据集上，适配器相对未适配模型将旋转误差降低 2–12×，以约 14× 更少的可训练参数胜过 LoRA，位姿优于免适配基线且避免其多视图推理成本，深度精度保持有竞争力。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 1, Abstract
- Evidence: 摘要末句集中给出四个量化锚点：2–12× 旋转误差、~14× 参数优势、位姿优于免适配基线、深度竞争力。
- Quote: “Across diverse fisheye datasets with fields of view from 110 ◦ to 200 ◦ , our adapter reduces rotation error by 2–12× relative to the unadapted model, out- performs LoRA while using ∼ 14× fewer trainable parameters, improves pose over adaptation-free baselines while avoiding their multi-view inference cost, and remains competitive on depth accuracy.”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0921

- Claim: 机制证据（pinhole bias 定位）：作者测量 DA3 各规模（Small/Base/Large/Giant）绝对位置编码的局部 Jacobian（以最大奇异值 σ1 与面积元刻画），发现预训练 PE 关于归一化半径几乎平坦——与针孔相机的位置无关结构一致；在 KITTI-360 上拟合适配器后，同样曲线向解析鱼眼参考弯曲。这把『鱼眼失配』定位到位置编码而非通用特征处理。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 4, Section 3 (On pinhole bias) and Figure 2
- Evidence: 第 3 节末段 + Fig 2：PE Jacobian 测量的实证描述——预训练平坦（pinhole-like），适配后弯向鱼眼参考。
- Quote: “Using Depth Anything 3 [5], we verify this bias by measuring the local Jacobian of the absolute positional embedding, J PE = ∂P A /∂(u, v) ∈ R C×2 , and summarizing it by its largest singular value σ 1 and local area element q det(J ⊤ PE J PE ) in Fig. 2. These quantities capture the strongest local variation and local scale of the embedding. Across all frozen model sizes, both are nearly flat as a function of normalized radius ρ (cf . Fig. 2a,b), matching the position-independent structure of”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0922

- Claim: 方法细节：RayTun3R 修改四类与 token 位置—几何相关的组件——绝对 PE、（存在时的）RoPE、预测网格坐标、patch tokenization；唯一可学习参数是小型 PE/RoPE 查找表修正，所有注意力块、MLP、预测头与 DPT 权重保持冻结；极坐标 (ρ,θ) 参数化的径向+角向 PE 残差零初始化，DPT 网格与分词修正是免参数的。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: pages 4-5, Sections 4-4.2
- Evidence: 第 4 节方法总览 + 4.1 问题设定 + 4.2 适配细节：四组件清单、唯一可学习部分、冻结范围、极坐标残差与零初始化。
- Quote: “Our goal is to adapt a pretrained pinhole 3D foundation model to fisheye input while keeping the pretrained model frozen. Fisheye optics change the mapping between token locations in the image and viewing rays, so the spatial structure learned during pinhole pretraining no longer matches the input camera. Motivated by the PE Jacobian analysis, we therefore modify the components that encode how token locations in the image relate to geometry: Absolute positional embeddings, rotary positional enco”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0923

- Claim: 评测覆盖（应用场景谱）：五个鱼眼数据集覆盖室外驾驶（KITTI-360，185° FOV）、手持双鱼眼视频（TUM-VI，195°）、带位姿 DSLR 鱼眼扫描（ScanNet++，115°）、多相机采集（ETH3D，110°）与室内外双鱼眼（FIORD，200°）；全部提供参考位姿，ETH3D 与 ScanNet++ 另提供稠密深度——对应车辆、手持、室内扫描等具身平台语境。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 6, Section 5 (Datasets)
- Evidence: 第 5 节数据集段给出五数据集的 FOV 与平台属性；Sec H 给出机器人/自主系统应用动机。
- Quote: “Datasets. Fisheye datasets with reliable pose or depth ground truth remain less common than standard pinhole reconstruction benchmarks. We evaluate on five datasets covering out- door driving (KITTI-360 [48], 185 ◦ FOV), handheld dual-fisheye video (TUM-VI [49], 195 ◦ ), (a) Center-PH (b) Multi-PH Figure 3: Adaptation-free baselines. posed DSLR fisheye scans (ScanNet++ [50], 115 ◦ ), multi-camera captures (ETH3D [51], 110 ◦ ), and dual- fisheye indoor/outdoor scenes (FIORD [52], 200 ◦ ). All da”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0924

- Claim: 主结果（Table 1，DA3-Small，五数据集，指标 R°/t°/d_reproj）：RayTun3R 在全部五个数据集上取得最低平移方向误差，在 ETH3D/TUM-VI/ScanNet++/FIORD 上取得最低旋转误差。ETH3D：0.70/4.48/5.82，显著优于 Vanilla 8.59/15.16/15.98、LoRA 2.18/10.74/9.02、CalTok 2.48/13.21/11.94；ScanNet++：1.11/5.78/4.16 vs Vanilla 10.21/30.26/23.82；FIORD：4.10/5.40/9.00 vs Vanilla 18.20/29.50/75.30。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 7, Table 1 and Section 5.1
- Evidence: Table 1 五行全量数值 + Section 5.1 首句的『全数据集最低平移、四数据集最低旋转』总结。
- Quote: “Dataset Vanilla Center-PH Multi-PH LoRA CalTok RayTun3R (ours) ETH3D 8.59 15.16 15.98 3.46 13.70 10.92 3.31 13.68 13.48 2.18 10.74 9.02 2.48 13.21 11.94 0.70 4.48 5.82 KITTI-360 1.69 12.81 11.64 0.79 4.17 3.10 1.71 9.75 4.72 1.37 8.49 5.56 1.66 10.05 5.83 0.84 2.92 3.88 TUM-VI 10.41 23.23 57.01 3.33 29.24 3.22 2.99 25.60 4.92 3.38 13.63 3.83 3.84 16.17 9.61 2.41 13.23 3.81 ScanNet++ 10.21 30.26 23.82 3.27 22.77 2.21 1.66 10.43 1.63 3.68 17.66 4.98 4.51 23.20 7.02 1.11 5.78 4.16 FIORD 18.20 29.5”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0927

- Claim: 推理开销（Table 4b，DA3-Small，504×504，RTX A4000，1000 帧平均）：RayTun3R 约 100 ms/帧、开销约 0%、可训练参数 10.8K；对照 LoRA 约 110 ms（+10%、147.5K 参数）、CalTok 约 105 ms（+5%、18.4K 参数）、Multi-PH 约 400 ms（+300%）、Center-PH 约 105 ms（+5%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 9, Table 4 (b)
- Evidence: Table 4b 六行开销表 + 表注测量条件（504×504、A4000、1000 帧平均）。
- Quote: “(b) Inference cost on DA3-Small, measured per fisheye frame at 504×504 on one NVIDIA RTX A4000 and averaged over 1000 frames. Trainable parameter counts account for the DA3-Small backbone width, with token size C = 384. (a) Component ablation on KITTI-360. Configuration R ◦ ↓ t ◦ ↓ d reproj ↓ Patch undistortion (no learnable PE) 1.397 6.66 8.96 Naive remap of PE 0.810 12.93 11.53 Radial PE only 1.154 5.48 3.70 Radial + angular PE 1.038 4.21 3.39 RayTun3R w/o border token 1.061 4.45 3.17 RayTu”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0928

- Claim: 组件消融（Table 4a，KITTI-360 cam02 185°，30 帧训练、前 500 帧评测）：完整模型重投影误差最低（1.183/4.81/3.03）；最大增益来自学习型 PE 残差（仅径向 PE 已 1.154/5.48/3.70，加角向 1.038/4.21/3.39）；直接对预训练 PE 表做几何重索引（Naive remap of PE）失败——旋转 0.810 但平移 12.93、深度 11.53；仅免参数的 patch 去畸变 1.397/6.66/8.96 远低于学习适配器。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 9, Table 4 (a) and Section 5.2
- Evidence: Table 4a 八行消融 + Section 5.2 首段归因（largest gain from learned PE residual；naive remap 失败原因）。
- Quote: “Table 4: Component ablation and inference cost. (a) Component ablation on KITTI-360 (drive 0000, cam02, 185 ◦ fisheye), trained on 30 frames and evaluated on the first 500 frames. (b) Inference cost on DA3-Small, measured per fisheye frame at 504×504 on one NVIDIA RTX A4000 and averaged over 1000 frames. Trainable parameter counts account for the DA3-Small backbone width, with token size C = 384. (a) Component ablation on KITTI-360. Configuration R ◦ ↓ t ◦ ↓ d reproj ↓ Patch undistortion (no”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0929

- Claim: 机制拆分（Table 7b + Table 8，ETH3D terrains / FIORD Kitchen）：绝对 PE 是主要学习组件——仅 RoPE 适配几乎无效（19.52/7.8/9.6，接近未适配 Vanilla 19.87/8.2/10.7），仅绝对 PE 已 0.68/0.9/1.6 近全模型（0.48）；去掉角向 bin 明显退化（径向 only 2.82/3.3/3.6）；免参数修正单独使用收益小且在 FIORD 上反而退化（39.04/36.3/19.2 vs Vanilla 28.09/20.7/14.2），仅学习组件 4.64/4.1/5.8，组合最优 3.10/2.5/5.5——剩余失配含方向依赖成分，不只径向。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 15, Tables 7 (b) and 8 (Supplementary G)
- Evidence: Table 7b（PE/RoPE 拆分与 bin 敏感性）+ Table 8（学习 vs 免参数），两表连续位于附录 G。
- Quote: “Absolute PE only (no RoPE) 0.68 0.9 1.6 RoPE only (no Absolute PE) 19.52 7.8 9.6 Both (full) 0.48 0.9 1.6 N r =10, N θ =8 0.72 0.9 1.7 N r =20, N θ =8 (default) 0.48 0.9 1.6 N r =40, N θ =8 0.47 0.9 1.5 N r =20, N θ =0 (radial only) 2.82 3.3 3.6 Table 8: Learned positional residuals vs. parameter-free camera-model corrections. We report pose rotation error R ◦ , translation-direction error t ◦ , and reprojection error d reproj on ETH3D terrains and FIORD Kitchen. Lower is better for all”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0932

- Claim: 跨 backbone 泛化（Table 6，ETH3D 场景均值）：RayTun3R 在全部五个冻结 backbone（DA3-Small/Base/Large、π³、VGGT）上取得最低平均旋转与平移误差——DA3-Small 0.70/4.48 vs Baseline 8.59/15.16、Center-PH 3.46/13.70；DA3-Base 0.54/3.26 vs 8.27/12.24；DA3-Large 0.51/2.96 vs 6.36/13.94；π³ 0.66/2.48 vs 2.66/11.30；VGGT 0.96/4.82 vs 3.19/11.52；Center-PH 深度有竞争力但位姿始终更高。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 14, Table 6 and Section E (Supplementary)
- Evidence: Table 6 五 backbone × 三方法均值表 + Sec E 正文总结（lowest mean rotation and translation error for every backbone）。
- Quote: “Method DA3-Small DA3-Base DA3-Large π 3 VGGT R t AbsRel δ R t AbsRel δ R t AbsRel δ R t AbsRel δ R t AbsRel δ Baseline 8.59 15.16 0.178 0.751 8.27 12.24 0.147 0.794 6.36 13.94 0.135 0.828 2.66 11.30 0.250 0.642 3.19 11.52 0.285 0.557 Center-PH 3.46 13.70 0.111 0.867 1.85 9.36 0.082 0.911 1.56 9.32 0.075 0.941 1.08 10.46 0.156 0.772 1.17 8.98 0.228 0.623 RayTun3R (ours) 0.70 4.48 0.107 0.884 0.54 3.26 0.089 0.910 0.51 2.96 0.083 0.925 0.66 2.48 0.175 0.863 0.96 4.82 0.139 0.834”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-1152

- Claim: 作者指出：配备大视场（FoV）鱼眼镜头的多鱼眼相机系统广泛用于移动机器人与数据采集平台，在状态估计与深度预测等任务中提升感知性能——这是本文多鱼眼标定研究的应用背景。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 1, I Introduction
- Evidence: 引言首句说明大 FoV 多鱼眼系统广泛用于移动机器人（引 DJI、Skydio）与数据采集平台（引 WoodScape、Ant3D），在状态估计（引 VINS-Mono）与深度预测（引 Omnidirectional Stereo、Omnividar）等任务中提升感知性能。
- Quote: “ULTI-FISHEYE camera systems equipped with large- field-of-view (FoV) lenses are widely used in mo- bile robots [1], [2] and data collection platforms [3], [4], where they improve perception performance in tasks such as state estimation [5] and depth prediction [6], [7].”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1155

- Claim: 成功与失败试验的观测分布无系统差异：全部 16 设置中观测计数差 D_qty 低于 0.30%（中位 0.15%、均值 0.17%），空间分布差 D_sp 与随机标签基线 D_rand 几乎一致（Δ_sp 至多 0.13 个百分点）——图像平面观测数量与分布不足以解释初始化失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 4, Table III, Section III-D
- Evidence: Table III 对每配置比较成功/失败组的 D_qty/D_sp/D_rand/Δ_sp：D_qty 全部 <0.30%，D_sp 与 D_rand 匹配、Δ_sp≤0.13pp，成功/失败分割的空间分离度不高于随机分割。
- Quote: “Table III confirms that the point-count difference is neg- ligible: D qty remains below 0.30% in all settings, with a median of 0.15% and a mean of 0.17%. Moreover, D sp closely matches D rand , and ∆ sp is at most 0.13 percentage points.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1156

- Claim: 失败案例沿内参初始化路径的条件数一致高于成功案例：以 Schur 消去标靶位姿后的规范化相机参数信息块定义条件数轨迹，失败试验诱导更病态的内参更新——失败与局部参数可分性差相关，而非仅缺检测或空间不平衡。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 4, Section III-E, Fig. 3
- Evidence: Fig. 3 比较成功/失败试验沿初始化路径的 conditioning score（γ_k=log10 κ(S̃_c)）：失败案例一致更大，表明在优化器遇到的当前线性化点处诱导更病态的内参更新。
- Quote: “Fig. 3 compares the conditioning scores of successful and failed trials along the initialization path. Failed cases consis- tently exhibit larger γ k values than successful cases, indicating that they induce more ill-conditioned intrinsic updates at the current linearization points encountered by the optimizer.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1157

- Claim: 作者的核心机制结论：与针孔标定不同，鱼眼标定在内参初始化中引入更强的焦距尺度与投影形状参数耦合；当观测只占据窄径向范围时，两组参数可产生几乎相同的残差变化而难以可靠估计——失败的核心是内参参数方向可分性差。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 5, Section III-F Key Findings
- Evidence: III-F Key Findings：低召回与空间不平衡可观察但均非主要失败机制；核心问题是初始化中内参参数方向可分性差；鱼眼（相对针孔）引入更强焦距-投影耦合，窄径向范围观测使参数产生相似残差变化、难以可靠估计。
- Quote: “the core issue is the poor separability of intrinsic parameter directions during initializa- tion. Unlike pinhole calibration, fisheye calibration introduces stronger coupling between focal scale and projection-shape parameters, and when observations occupy only a narrow radial range, these parameters can produce similar residual changes and become difficult to estimate reliably.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1158

- Claim: 径向覆盖实验（Fig. 4）：中心、中径、边缘三类单带径向剖面的焦距-投影耦合一致强于径向覆盖剖面，且该结论在 Omni、EUCM、Double-Sphere 三个鱼眼投影族上一致——稳定内参初始化要求观测跨越宽径向范围。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 5, Fig. 4, Section III-E
- Evidence: Fig. 4 对比 C/M/E/R 四类径向剖面的焦距-投影耦合度量（式 12 的 C_fη=log10 κ(G_fη)）：单带剖面耦合一致更强，径向覆盖剖面在三投影族上耦合最低。
- Quote: “Fig. 4 compares central (C), middle-radius (M), edge (E), and radially covered (R) profiles. Single-band profiles consis- tently produce stronger coupling, while radial coverage yields the lowest coupling across all three fisheye families.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1159

- Claim: 学习型标靶检测器在四档 FoV（180-240°）上召回率 0.9255-0.9344，几何检测法仅 0.6838-0.7085（240° 时差距最大：0.9263 vs 0.6838），且平均定位误差也更低（0.7841-0.8277 px vs 0.8304-0.8553 px）——学习检测显著提升严重鱼眼畸变下的检测召回与精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 6, Table IV, Section V-B
- Evidence: Table IV 对比学习检测器与几何检测器在 180/200/220/240° FoV 下的 Recall/Mean Error：学习法召回稳定在 0.93 上下且误差略低；几何法召回随 FoV 增大降至 0.68。
- Quote: “180 0.9330 / 0.7841 0.7085 / 0.8377 200 0.9344 / 0.7944 0.7049 / 0.8380 220 0.9255 / 0.7941 0.7077 / 0.8304 240 0.9263 / 0.8277 0.6838 / 0.8553”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1160

- Claim: 在 16 个合成配置的总体结果上，CO-Calib 把标定成功率从 Kalibr 的 68.1% 提升到 99.3%，并把总体外参误差从 0.54mm/0.029° 降到 0.18mm/0.021°（平移/旋转）。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 6, Section V-C; page 7, Table VI
- Evidence: V-C 与 Table VI：CO-Calib 在各 FoV/配置一致提升成功率，总体 68.1%→99.3%，外参误差 0.54/0.029→0.18/0.021（mm/deg，strict-success 试验平均）。
- Quote: “In particular, the overall success rate increases from 68.1% with Kalibr to 99.3% with CO-Calib. Meanwhile, CO-Calib also reduces the overall extrinsic calibration error from 0.54/0.029 to 0.18/0.021 in translation and rotation, respectively.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1161

- Claim: 在最宽的 FoV240 档，Kalibr 成功率仅 12%-41%（依 stereo 相对旋转 0/60/90/120° 配置），CO-Calib 达到 98%-100%——宽 FoV 是现有管线最痛、CO-Calib 增益最大的区间。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 7, Table V
- Evidence: Table V FoV240 四配置：Kalibr SR 12%/41%/25%/23%，CO-Calib 98%/98%/98%/100%；外参误差 CO-Calib 也普遍更低（如 0/0.005 vs 0.24/0.006）。
- Quote: “Kalibr 12% 3.56/0.099 0.24/0.006 41% 3.40/0.089 0.54/0.032 25% 3.37/0.099 0.64/0.078 23% 3.41/0.108 0.82/0.058 CO-Calib 98% 3.35/0.076 0.18/0.005 98% 3.07/0.056 0.14/0.009 98% 2.97/0.059 0.17/0.027 100% 3.03/0.067 0.22/0.015”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1162

- Claim: 帧选择消融：对每个被选择序列构造同规模随机子集并跑同一标定管线，总体成功率从 99.3% 暴跌到 30.9%——CO-Calib 的收益来自按覆盖与可观测性选择帧，而非单纯减少帧数。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 6, Section V-C
- Evidence: V-C 消融：same-size random subset 使总体成功率从 99.3% 降至 30.9%，确认改进不是来自减少帧数而是来自选择覆盖/可观测性更好的帧。
- Quote: “For each selected sequence, we construct a same-size random subset and run the same calibration pipeline. The random subsets lead to a much lower overall success rate, dropping from 99.3% to 30.9%.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1163

- Claim: 初始化必要性消融：把标准三阶段管线改为去掉初始化的 BA-only 两阶段管线后，总体成功率降至 13.5%——可靠的（线性化）初始化对鲁棒标定不可绕过，最终联合优化无法补偿病态初始化。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 6, Section V-C; page 7, Table V
- Evidence: V-C 消融：BA-only two-stage（去初始化）总体成功率 13.5%，Table V 各配置普遍个位数至两成（FoV240 低至 1%），证明初始化阶段的关键性。
- Quote: “Finally, we evaluate the effect of removing the initialization stage by comparing the standard three-stage pipeline with a BA-only two-stage pipeline. Without initialization, the overall success rate decreases to 13.5%, demonstrating that a reliable”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1164

- Claim: 真实挑战案例：在六相机 Hex-Fisheye 系统上，Kalibr 在全部 10 个序列上标定失败（0/10），而 CO-Calib 全部 10 个试验成功并保持高外参一致性（Table VII：0.97mm/0.048°）——超多相机鱼眼 rig 是现有工具链的失败边界，CO-Calib 将其变为可用。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 7, Section V-C; page 8, Table VII
- Evidence: V-C 真实实验：Hex-Fisheye 数据集上 Kalibr 全序列失败，CO-Calib 10/10 成功且外参一致性高；Table VII 给出 CO-Calib Hex-Fisheye Ext. Std. 0.97/0.048（mm/deg），Basalt 51.23/6.626 且仅 4/10。
- Quote: “More importantly, on the challeng- ing Hex-Fisheye dataset, Kalibr fails on all sequences, while CO-Calib succeeds on all 10 trials and maintains high extrinsic consistency.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1165

- Claim: 真实评估方法与 stereo 结果：因真实数据无相机参数与位姿真值，作者用重复标定序列间的外参一致性（基线长度与相对旋转角的标准差）作代理指标；在 5 种标准 stereo 鱼眼配置上 CO-Calib 全部 5/5 成功，外参一致性与 Kalibr 相当（平移差异典型在亚毫米级、旋转在小数度以内）。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 7, Section V-C; page 8, Table VII
- Evidence: V-C：真实无 GT 故用外参一致性代理；Table VII 显示 5 种 stereo 配置（Rot-0/30/60/90/120）CO-Calib 与 Kalibr 均 5/5 成功，CO-Calib 一致性数值互有胜负（如 Rot-90 0.43 vs 0.71mm 更好、Rot-60 0.33 vs 0.17mm 略差），Basalt 一致性显著更差。
- Quote: “Since ground-truth camera parameters and camera poses are unavail- able in real-world data, we use extrinsic consistency across repeated calibration sequences as a proxy metric. Specifically, lower standard deviations of the estimated baseline length and relative rotation angle indicate more stable calibration results.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-0249

- Claim: UCAG-P 把操作表示为相机可观测的锚点运动而非本体专属控制：共享动作空间用语义锚点对在相机坐标系中的运动描述任务进度，使机器人臂、人形机械手和人手演示成为同一动作模式的不同 embodiment。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 9, Section 4.2 Camera-Centric Action Space
- Evidence: Section 4.2 开篇定义共享空间 G：跨机器人臂、人形与人手演示，任务进度通过腕/末端与抓取中心在相机视野中的运动显现，这些量与 VLA 使用的视觉证据绑定而不与特定关节布局或控制器绑定。
- Quote: “The shared space G describes manipulation through camera-observable geometry rather than embodiment- specific controls, as presented in Figure 5. Across robot arms, humanoid manipulators, and human demon- strations, task progress is visible through the motion of the acting wrist or end effector and the grasp center in the camera view.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0250

- Claim: 预训练语料共 6373.586 小时、1,020,672 条轨迹，其中 VITRA/EgoDex/EgoVerse 三个人类手部第一视角演示数据集贡献 2,339.727 小时（占具身语料 36.71%，341,132 条），仿真占 59.11%、真机仅 4.18%——人类演示是与机器人/仿真同量级的最大数据族之一。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 6, Section 3.1 Embodied Corpus Composition, Table 1
- Evidence: Table 1 给出语料构成（含 Human-hand subtotal 341,132 条 / 2339.727 小时 / 36.71% 与 Total 6373.586 小时）；正文 Egocentric human demonstrations 段给出 2,339.727 小时与 36.71% 占比。
- Quote: “Egocentric human demonstrations. VITRA, EgoDex, and EgoVerse contribute 2,339.727 hours of egocentric manipulation video, or 36.71% of the embodied corpus.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0251

- Claim: 人类手部演示不含机器人命令：作者检测腕部和抓取中心锚点，把其运动转换为相机中心伪动作，使人类与机器人行为在同一几何动作空间中表达，为机器人轨迹补充多样化的物体交互与 embodiment 无关的运动线索。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 7, Section 3.1 Embodied Corpus Composition (continuation)
- Evidence: Section 3.1 末段说明 egoistic 视频无机器人命令，故检测腕/抓取中心锚点并转换为相机中心伪动作；该表示补充多样化物体交互与 embodiment 无关运动线索，同时把人类与机器人行为表达在同一几何动作空间。
- Quote: “detect wrist and grasp-center anchors and convert their motion into camera-centric pseudo-actions. This representation supplements robot trajectories with diverse object interactions and embodiment-independent motion cues while expressing human and robot behavior in the same geometric action space.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0252

- Claim: 锚点语义跨本体固定：人类手部演示中 p0 取自腕部关键点、p1 取拇指尖与食指尖的中点；机器人 embodiment 中 p0 来自模拟器状态或正向运动学提供的腕/末端坐标系、p1 由夹爪或手部几何计算。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 9, Section 4.2 Camera-Centric Action Space
- Evidence: Section 4.2 给出锚点对实例化：人类手部由 hand keypoints 提供锚点对；同段前文给出机器人 embodiment 的 p0/p0 计算来源（腕/末端坐标系、夹爪几何），锚点语义角色固定而物理实例随本体变化。
- Quote: “For human-hand demonstrations, hand keypoints provide the corresponding anchor pair, with p 0 obtained from the wrist keypoint and p 1 defined as the midpoint between the thumb tip and index fingertip.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0256

- Claim: 单一统一检查点（无任何基准专属微调）在四个仿真基准上达到 LIBERO 98.3%（四子套件 98.8/98.6/99.2/96.4）、RoboTwin Easy 88.66%、RoboTwin Hard 89.20%、RoboCasa GR-1 62.0%，并在全部评测数据集上超过通用基线 Qwen-VLA（Instruct 97.9/86.1/87.2/56.7）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 12, Section 5.2, Table 3
- Evidence: Section 5.2 叙述 LIBERO 98.3% 与四子套件分数、RoboTwin 88.66%/89.20%；Table 3 给出 UCAG-P Generalist 行（98.3/88.7/89.2/62.0）与 Qwen-VLA-Instruct 行（97.9/86.1/87.2/56.7），并声明全部结果来自单一检查点、无基准专属后训练。
- Quote: “On LIBERO, UCAG-P reaches 98.3%, within one point of the strongest reported result, with 98.8%, 98.6%, 99.2%, and 96.4% on LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long, respectively (see Section B.3). On RoboTwin, it reaches 88.66% on Easy and 89.20% on Hard, remaining competitive with recent specialist and generalist policies.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0257

- Claim: 真机受控对比（同演示预算、观测设置、控制器，Piper 机器人，每任务 100 演示×20 闭环试验）中，UCAG-P 初始化在人-机迁移任务上大幅领先：面包抓取 60% vs π0.5 的 20%，开抽屉 90% vs 85%，双臂叠碗 75% vs 65%；面包任务的监督来自 MediaPipe 手部关键点转换的相机中心锚点。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 13, Section 5.2b, Figure 7
- Evidence: Figure 7 报告真机三任务成功率（60/90/75 vs π0.5 的 20/85/65）；正文强调对比在相同演示预算、观测设置与控制器下进行；page 24 A.5 说明面包 pickup 通过 MediaPipe 手部关键点转相机中心锚点测试 human-to-robot 迁移，page 28 C.1 给出转换细节。
- Quote: “UCAG-P achieves 60%, 90%, and 75% success on bread grasping, drawer opening, and bowl stacking, respectively, compared with 20%, 85%, and 65% for π 0.5 . These controlled comparisons show that the UCAG-P initialization improves real-robot adaptation under the same demonstration budget, observation setup, and controller.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0259

- Claim: 几何条件化翻译器把相机坐标预测转为可执行命令时，显式条件于相机-基座变换 T_base←cam、当前状态局部雅可比与编码本体结构（活跃操纵臂、命令槽位）的几何 token——即每台目标机器人都需要相机-基座标定才能执行共享几何预测。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 10, Section 4.3 UCAG-P Architecture
- Evidence: Section 4.3 说明翻译器接收预测几何块、本体状态与几何上下文（camera-to-base transform、局部 Jacobian、几何 token）；camera-to-base 变换把相机帧中预测的方向与位移对齐到机器人本体坐标系，雅可比提供关节变化与末端运动的局部关系。
- Quote: “The camera-to-base transform aligns directions and displacements predicted in the camera frame with the robot body frame.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0260

- Claim: 输入侧的相机异构处理：所有 RGB 统一缩放到 224×224 并做轻量颜色增广；因相机数量因数据源而异，观测被打包进固定数量的视图槽（view slots），缺失视图零填充并用视图有效性指示符禁用。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 7, Section 3.2 Data Curation and Preprocessing, Stage 2
- Evidence: Section 3.2 Stage 2 描述视觉与语言标准化：统一分辨率 224×224、轻量颜色增广缩小仿真/真机/egoistic 演示的外观差距；相机数量差异通过固定视图槽与 view-validity indicators 处理。
- Quote: “Because camera counts differ across sources, observations are packed into a fixed number of view slots. Missing views are zero-filled and disabled by view-validity indicators.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0303

- Claim: 该移动双臂平台的视觉传感套件由一台顶装 360° 全景相机与三台局部 RGB 相机（一台前视 + 两台腕装）组成；平台为轮式双臂构型（RANGER MINI 3 移动底盘 + 两台 6-DoF Agilex PIPER 臂 + 平行夹爪），底盘支持自旋、阿克曼转向与斜向平移三种模式。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 3, Section III-A, Robot embodiment
- Evidence: Robot embodiment 段给出传感配置：顶装 360° 全景相机负责周围环境观察，三台局部 RGB 覆盖机器人前方场景与末端操作区。图 1（page 3）将全景相机标注为 Insta X5 360 Camera、局部相机标注为 3 × RGB Camera。
- Quote: “As shown on the right side of Fig. 1, the robot is a wheeled bimanual platform comprising a RANGER MINI 3 mobile base, two 6-DoF Agilex PIPER arms, and parallel grippers. Its visual sensing suite consists of a top-mounted 360-degree panoramic camera and three local RGB cameras: one front-facing camera and two wrist- mounted cameras.”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0307

- Claim: PanoVLA 数据集规模：四任务各采集 200 条遥操作轨迹共 800 条，总计约 5.5 小时、约 500k 同步帧（25 Hz，每条轨迹约 20-30 秒）；采集时全景相机、局部相机、本体态与全身动作以共享时间戳同步录制。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 3, Section III-B, Data Collection Protocol and Dataset
- Evidence: Data Collection Protocol 段给出采集协议与规模数字；page 4（Data Modalities）进一步说明全景观察由顶装 360° 相机采集并转为 ERP 存储与局部/腕视图同步。
- Quote: “Using the teleoperation system above, we collect 200 demonstration trajectories for each of the four real-world mobile manipulation tasks, yielding 800 trajectories in to- tal. During each demonstration, the system synchronously records visual observations from all cameras, robot propri- oceptive states, and whole-body actions with shared times- tamps. The trajectories span approximately 5.5 hours in total. Each trajectory lasts about 20–30 seconds and is recorded at 25 Hz, yielding roughly 500k”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0308

- Claim: PanoVLA 把全景观测作为 VLA 的独立专家模态接入 π0.5 骨干：VLM 专家从局部观察、指令与本体态计算 KV cache；并行地全景编码器把全景观察编码为 token，全景专家在与 VLM cache 的联合自注意力中处理全景 token 并产出全景 cache；动作专家基于拼接 cache [C_vlm; C_pano] 预测动作块，从而同时利用局部观察的精细操作线索与全景观察的机器人中心全局上下文。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 5, Section IV-B, PanoVLA (fusion interface)
- Evidence: Fusion 接口设计段给出 KV cache 融合机制；page 4 末句说明 PanoVLA instantiated from the dual-expert π0.5 backbone by inserting the panorama expert between its VLM and action experts（三专家 MoT）。
- Quote: “We adopt the transformer key–value (KV) cache as the fusion interface. For an L-layer expert, a cache is the layer-wise collection C = {(K ℓ , V ℓ )} L ℓ=1 generated from its context tokens and reused by subsequent tokens during attention. At time t, the VLM expert computes the VLM cache C vlm t from I loc t , l, and s t . In parallel, the panorama encoder encodes I pano t into tokens Z pano t . The panorama expert then performs joint self-attention with C vlm t while processing Z pano t , and p”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0309

- Claim: 全景编码管线以双目鱼眼原始观察为输入：同步双目鱼眼视图先经球面重投影映射到公共观察球，并光栅化为等距柱状投影（ERP）图像，得到连续的机器人中心全景；再送入全景视觉编码器 MTPano（全景基础模型，密集场景解析），提取其分割与深度分支的中间特征作为语义与几何两组密集特征，按通道维拼接为统一密集全景表征；最后经自适应平均池化压缩到固定空间分辨率并用轻量 MLP 映射到全景专家隐维，产出与全景分辨率无关的固定数量全景 token。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 5, Section IV-B, Panorama Encoder
- Evidence: Panorama Encoder 段描述三阶段管线（球面投影、全景特征提取、token 适配）与 MTPano 双分支特征；token adapter 段说明池化+MLP 适配使 token 数与全景分辨率无关。
- Quote: “Given synchronized dual- fisheye observations, we first apply spherical reprojection to map the two fisheye views onto a common viewing sphere and rasterize the spherical representation as an equirectan- gular projection (ERP) image, yielding a continuous, robot- centric panorama of the surroundings. This ERP image is then fed into a panoramic visual encoder E p . We instantiate E p with MTPano [35], a panoramic foundation model for dense scene parsing. Specifically, we extract intermediate feat”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0310

- Claim: 四任务闭环真机评估（每任务 15 次试验）中，PanoVLA 平均阶段完成率 SCR 91.3%、端到端成功率 SR 73.4%，显著超过仅用局部视角的 π0.5 基线（58.6%/30.0%）；分任务看 Move Block 收益最大（SR 20.0%→93.3%），Open Curtain 26.7%→66.7%，Wipe Table 26.7%→46.7%，Move Pen 46.7%→86.7%；raw ERP 附加图像基线平均 80.8%/56.7%，透视拼接基线 70.4%/38.3%。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 6, Table II and Section V-B
- Evidence: Table II 汇报四方法在四任务上的 SCR/SR 与平均值；正文（page 6）总结 PanoVLA achieves the best average results 并归因 SCR 增益来自目标搜索、移动接近与物理操作等中间阶段。
- Quote: “TABLE II REAL-WORLD CLOSED-LOOP EVALUATION. SCR DENOTES STAGE COMPLETION RATE AND SR DENOTES END-TO-END SUCCESS RATE; AVG. IS AVERAGED OVER THE FOUR TASKS, WITH 15 TRIALS PER TASK. THE BEST RESULTS ARE HIGHLIGHTED IN BOLD. Method Move Pen Move Block Open Curtain Wipe Table Avg. SCR SR SCR SR SCR SR SCR SR SCR SR π 0.5 71.1% 46.7% 35.0% 20.0% 61.7% 26.7% 66.7% 26.7% 58.6% 30.0% π 0.5 w/ Pano 95.6% 86.7% 80.0% 73.3% 73.3% 46.7% 74.4% 20.0% 80.8% 56.7% π 0.5 w/ Stacked Pano 82.2% 60.0% 70.0% 40.0%”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0314

- Claim: 全景编码器选择对闭环性能影响显著：用基础 VLM 自带的视觉编码器 SigLIP（透视图像预训练）编码 ERP 全景仅得 75.6% SCR / 40.0% SR，用全景基础模型 MTPano 达 95.6% / 86.7%（Move Pen 消融，每变体 15 次闭环真机试验）；作者归因于 SigLIP 难以捕捉等距柱状观察的水平连续性与全局布局，而 MTPano 专为全景空间结构设计、为全景专家构建机器人中心空间上下文提供更有效线索。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 7, Section V-C, Panorama visual encoder and Table III
- Evidence: V-C 消融：Panorama visual encoder 对比 SigLIP 与 MTPano（同为 100M 全景专家）；Tab. III 给出数值，正文给出归因分析。
- Quote: “Using SigLIP yields only 75.6% SCR and 40.0% SR, substantially lower than the 95.6% and 86.7% achieved with MTPano. Because SigLIP is pretrained primarily on perspective images, it may be less effective at capturing the horizontal continuity and global layout of equirectangular observations. In contrast, MTPano is designed to model panorama-specific spatial structure, providing the panorama expert with more informa- tive cues for constructing robot-centric spatial context.”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0357

- Claim: 作者动机性观察：在固定相机位姿上训练的 VLA 策略一旦部署时相机移动就趋于崩溃——在最差的 LIBERO 套件上，成功率从 92.4% 跌至 9.3%（无规范化处理时）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 4, Section 3.1, Motivation
- Evidence: 方法动机节以具体数字量化视角脆弱性：in our worst LIBERO suite, the success rate decreases from 92.4% to 9.3%；摘要层表述为 about 90% to about 10% in the worst case（page 1）。
- Quote: “A VLA policy trained at a fixed camera pose tends to collapse once the camera moves at deployment; in our worst LIBERO suite, the success rate decreases from 92.4% to 9.3%.”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0358

- Claim: 核心概念贡献（Locality 归约）：实际部署中相机变化通常很小（相对工作区仅几至几十厘米）；在该有界扰动前提下，视角变化只影响图像的有限部分，大部分像素可经深度信息与相机参数几何恢复，学习只需处理狭窄缺失区域（可视为 inpainting 问题）；因此视角规范化不是完整的新视角合成问题，而是基本独立于场景与策略的局部适配问题。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 2, Section 1, Introduction
- Evidence: 引言正式化 Locality：perturbations are often small relative to the workspace, typically amounting to only a few to a few tens of centimeters；viewpoint changes affect only a limited portion of the image, while most pixels remain geometrically recoverable；viewpoint canonicalization is not a full novel-view-synthesis problem, but a simpler local adaptation problem that is largely independent of the scene and policy；紧随其后声明 We treat Locality as an empirically testable assumption（后续 A.1 形式化、A.2 验证）。
- Quote: “In practice, these perturbations are often small relative to the workspace, typically amounting to only a few to a few tens of centimeters. We refer to this practical property as Locality. Under this assumption, viewpoint changes affect only a limited portion of the image, while most pixels remain geometrically recoverable. Specifically, most of the visual content can be mapped to the canonical view using depth information and camera parameters. This means that learning is mainly needed for a na”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0359

- Claim: 规范化器架构：对称 U-Net 以 [RGB∥深度] 通道拼接为输入、经位姿对 FiLM 嵌入调制，逐源像素预测 14 维高斯描述子（位置残差、各向异性 log 尺度、朝向四元数、不透明度、颜色残差）；全部头零初始化使模块恰从几何扭曲起步，高斯中心锚定在世界空间反投影点、残差位移钳制在局部深度 10% 内；每源像素一个高斯，经 gsplat 可微 α-blending 在规范位姿光栅化，遮挡由深度排序解决，α-blender 自身填充剥离带，无需独立 inpainting 头。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 5, Section 3.3, Pixel-aligned 3D-Gaussian architecture
- Evidence: Section 3.3 给出完整架构：FiLM-modulated symmetric U-Net（输入 [Is∥Ds]）、14-dimensional Gaussian descriptor（∆μ/log s/q/α/∆c 五分量）、All heads are zero-initialized so that fϕ starts exactly at the geometric warp、center clamp caps displacement at 10% of local depth（式(5) c∆µ=0.1）、gsplat differentiable α-blender 在规范位姿光栅化、Occlusion is resolved by depth-sorting、the α-blender itself fills the disocclusion band。
- Quote: “A symmetric U-Net takes the channel-wise concatenation [I s ∥ D s ] as input and is FiLM-modulated [24] by a pose-pair embedding, which is formulated as z pose = MLP(C s , C ⋆ ) ∈ R 128 . At every source pixel, the decoder predicts a 14-dimensional Gaussian descriptor consisting of a position residual (∆μ), an anisotropic log-scale (log s), an orientation quaternion (q), an opacity (α), and a color residual (∆c). All heads are zero-initialized so that f ϕ starts exactly at the geometric warp. Th”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0360

- Claim: 与并发工作 AnyCamVLA 的对比定位（作者口径）：AnyCamVLA 同样冻结策略，但依赖 LVSM 合成器与双视图输入，其评估局限于较窄的扰动范围；本文以 Locality 归约把模块参数量相对 AnyCamVLA 减少 42×。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 3, Section 2, Camera-Robust Robot Learning
- Evidence: 相关工作 Camera-Robust Robot Learning 段：The concurrent AnyCamVLA [10] similarly froze the policy but relied on LVSM [12] synthesizer with dual-view inputs, with evaluation limited to narrow perturbations；we introduce a Locality-based reformulation that reduces the number of parameters by 42× compared with AnyCamVLA（本文模块 4M；AnyCamVLA 的 LVSM 模块 171M，数字见两文各自规格）。
- Quote: “The concurrent AnyCamVLA [10] similarly froze the policy but relied on LVSM [12] synthesizer with dual-view inputs, with evaluation limited to narrow perturbations. On the other hand, we introduce a Locality-based reformulation that reduces the number of parameters by 42× compared with AnyCamVLA.”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0361

- Claim: 跨策略泛化（单一 checkpoint，εt=100cm，500 episodes）：XVLA（spatial）1.4%→81.0%（+79.6pp）；OpenVLA-OFT 7B（object）19.8%→81.6%（+61.8pp）；RynnVLA-002（spatial）25.8%→78.6%（+52.8pp）；π0.5 3.4B（spatial）42.6%→86.8%（+44.2pp）——每个冻结策略均无微调获益，作者观察获益幅度与策略自身鲁棒性反相关。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 7, Table 1(a)
- Evidence: Table 1(a) 四行完整数字（No canon/Fwd-warp/GS-VLA/∆，Fwd-warp 分别为 19.7/30.5/37.8/56.5）；page 6 正文补充 the magnitude of the benefit anti-correlates with the policy’s intrinsic robustness。
- Quote: “XVLA spatial 1.4 19.7 81.0 +79.6 OpenVLA-OFT (7 B) object 19.8 30.5 81.6 +61.8 RynnVLA-002 spatial 25.8 37.8 78.6 +52.8 π 0.5 (3.4 B) spatial 42.6 56.5 86.8 +44.2”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0362

- Claim: 跨套件零样本迁移：模块只依赖轮廓-深度几何而不依赖任务语义，可零样本迁移到未见环境；最显著增益在长程 libero_10 套件——π0.5 从 9.3% 提升到 72.1%（+62.8pp）；作者把长程套件的大幅提升归因于误差累积的减少：每步保持小的 inpainting 区域限制了帧间漂移、防止误差随时间复合。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 6, Section 4.2
- Evidence: Cross-suite generalization 段：our module transfers zero-shot to unseen environments；the most striking gain occurs on the long-horizon libero_10 suite, boosting π0.5 from 9.3% to 72.1% (+62.8 pp)；归因 reduced error accumulation over long trajectories（Table 1(b) 规格：1000 episodes，page 7）。
- Quote: “Because the scene structure depends only on silhouette ge- ometry and not on task semantics, our module transfers zero-shot to unseen environments. As shown in Table 1(b), the most striking gain occurs on the long-horizon libero_10 suite, boosting π 0.5 from 9.3% to 72.1% (+62.8 pp). We attribute this especially large improvement to reduced error accumulation over long trajectories: by keeping the inpainted region small at each step, the locality property limits frame-to-frame drift and prevents”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0363

- Claim: 扰动尺度扫描（π0.5×libero_spatial，εt∈{5,15,30,50,100,200}cm）：未保护基线跨扫描下降 49.5pp（85.2%→35.7%），GS-VLA 仅下降 9.5pp（88.0%→78.5%）；增益 ∆ 随 εt 增长（+2.8pp@5cm、+13.7pp@50cm、+44.2pp@100cm、+42.8pp@200cm），在 Locality 界内近似线性增长。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 7, Table 2
- Evidence: Table 2 标题与数据：The baseline drops 49.5 pp across the sweep; GS-VLA drops only 9.5 pp；No canon 85.2/82.7/80.6/73.5/42.6/35.7，GS-VLA 88.0/88.6/87.6/87.2/86.8/78.5，∆ +2.8/+5.9/+7.0/+13.7/+44.2/+42.8；线性性讨论见 Section 4.3（∆ grows approximately linear in εt within the Locality bound）。
- Quote: “The baseline drops 49.5 pp across the sweep; GS- VLA drops only 9.5 pp. Term ∆ grows approximately linearly in ε t within the Locality bound, matching Appendix A.1; the largest cell (ε t =100 cm) is in bold. Method \ ε t (cm) 5 15 30 50 100 200 No canon 85.2 82.7 80.6 73.5 42.6 35.7 GS-VLA (ours) 88.0 88.6 87.6 87.2 86.8 78.5 ∆ (pp) +2.8 +5.9 +7.0 +13.7 +44.2 +42.8”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0370

- Claim: 机制级验证支持 Locality 归约：新暴露区域比例 η(ρ) 在 ρ≤0.5 内对平移/旋转/联合扰动均线性（R²≥0.99），每个（模式×套件）格斜率 η(ρ)/ρ∈[0.27,1.09]，符合 Proposition A.1 的双边界；旋转贡献斜率跨套件几乎不变（spatial 1.084 vs object 1.089，差 0.4%）而平移贡献斜率变化约 60%（按轮廓长度预测的比值误差在 11% 内），印证"旋转项只依赖图像周长、平移项依赖轮廓长度"的场景分解；剥离像素紧贴深度边缘（距最近深度边缘 5–7px，对比均匀随机的 27–33px，约 5× 更紧）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 14, Appendix A.2
- Evidence: A.2 Empirical validation：η(ρ) is linear with R²≥0.99 for ρ≤0.5 across translation, rotation, and joint perturbation modes；η(ρ)/ρ ∈ [0.27, 1.09]；The rotation slope is essentially the same on both suites (1.084 on spatial vs. 1.089 on object, a 0.4% discrepancy), while the translation slope varies by about 60%；Occluded pixels lie 5–7 px from the nearest depth edge... against 27–33 px for uniform-random pixels — a roughly 5× tighter localization（斜率表见 page 15 Table 5）。
- Quote: “We find η(ρ) is linear with R 2 ≥ 0.99 for ρ ≤ 0.5 across translation, rotation, and joint perturbation modes, and across both spatial and object. On every (mode, suite) cell the slope satisfies η(ρ)/ρ ∈ [0.27, 1.09], which confirms the two-sided bound of Proposition A.1. Departure from linearity begins around ρ ≈ 0.5, well inside the validity range the proposition predicts. Scene decomposition. A second, sharper prediction comes from Corollary A.1: the rotation contri- bution to η depends only”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0393

- Claim: 在 LIBERO-Plus 相机扰动轨道上，跨视角动作流一致性训练达到 87.2±0.4%（3 个训练种子），比同配对数据的 FM-only 对照（79.8±0.8%）高 7.4pp、比朴素混合相机 SFT 高 12.5pp，同时保持名义相机 ID 性能 95.0%（两种子方差 ±0.8 vs ±4.3）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 6, Section 4.2, Table 1
- Evidence: Table 1 与正文给出主结果：两配对变体共享数据仅差 λ_CV，间隙跨种子一致；ID 均值相同但提出方法种子方差更低。
- Quote: “The proposed method reaches 87.2±0.4% on the camera track, with +7.4pp over the FM-only same-data control (79.8±0.8%) and +12.5pp over naive mixed-camera SFT.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0394

- Claim: 仅用名义相机数据微调的 π0.5 式 VLA 在腕部相机全程遮蔽、仅单场景 RGB 推理时对场景相机扰动近乎崩溃：相机扰动轨道成功率 16.8%（C1 距离/尺度 1.1%、C2 球面位置 13.2%、C3 端点朝向 45.7%），而 ID 名义相机成功率 85.8%。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 6, Table 1
- Evidence: Table 1 名义相机基线行量化固定相机脆弱性：ID 85.8 对相机轨道 16.8，其中 C1 类（距离与尺度）几乎归零（1.1）。
- Quote: “Nominal-only baseline nominal LIBERO, FM only 85.8 16.8 1.1 13.2 45.7”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0396

- Claim: 提出方法的相机轨道增益在三类扰动上均为正但幅度不均：C1（相机距离/尺度）+9.2pp、C2（球面位置）+8.0pp、C3（端点朝向）+3.4pp（90.6±0.9% 对 FM-only 87.2±0.7%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 6, Section 4.2
- Evidence: 正文按类别拆分增益，C3 上控制本身已较强（87.2%），提出方法提升至 90.6%。
- Quote: “The camera-track gains are largest on C1 (+9.2pp) and C2 (+8.0pp), and remain positive on C3 (+3.4pp), where the proposed method reaches 90.6±0.9% compared with 87.2±0.7% for FM-only.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0397

- Claim: 真机部署于从未用于数据采集的相机摆放时，跨视角一致性训练把聚合成功率从 FM-only 多视角训练的 53.3%（48/90）提高到 74.4%（67/90）（描述性两比例检验 p<0.005），而 seen 相机条件下两者相当（80/90 对 79/90）——同数据对照分离出一致性项的真实 held-out 增益。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 7, Section 4.4 (Table 7 on page 14)
- Evidence: 真机协议为 3 seen + 3 held-out 摆放、每 cell 10 rollouts；两方法共享同一多相机示范数据与预算，仅差跨视角项。
- Quote: “On held-out cameras, FM-only multi-view training reaches 48/90 aggregate successes, while the proposed objective reaches 67/90 (descriptive two-proportion test, p < 0.005; we treat per-task/per- placement counts as primary).”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0403

- Claim: 方法定位为训练期配方而非推理接口改造：与相机条件化（需外参/Plücker ray/相机标签）、相机坐标动作（需外参标定）、测试时视角合成/表征再校准、3D/几何输入（深度/点云/RGB-D）等家族相比，本文推理仅用单场景 RGB+语言+本体感知，跨视角配对只存在于训练损失中，与上述家族原则上可组合。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 3, Section 2 Related Work (contract comparison: page 18, Table 9)
- Evidence: 相关工作节声明现有补救改变感知或推理契约而本方法只改训练目标；附录 H Table 9 给出逐家族推理需求对比。
- Quote: “These remedies modify the infer- ence contract; ours acts only on the training objective and leaves the single-scene-RGB, calibration- free interface unchanged, so it is largely orthogonal to and combinable with them.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0404

- Claim: 仿真配对数据规模为 338,575 对同状态配对（由 libero spatial、libero object、libero goal、libero 100 的原始示范经 MuJoCo 状态重置 + 名义/扰动双相机重渲染构造），扰动相机采自 LIBERO-Plus C1/C2/C3 分布族且与评估基准切分不相交。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 5, Section 4.1 (Appendix A.1: page 12)
- Evidence: 4.1 节给出配对构造流程与规模；附录 A.2 说明训练/评估分离（无评估相机姿态、任务初始状态或动作标签进入训练）。
- Quote: “We generate 338,575 same-state pairs from libero spatial , libero object, libero goal, and libero 100”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0411

- Claim: 在 LIBERO-Plus 相机轨道的 carve-and-hold-out 协议下，仅约束不变块的选择性跨视角一致性（SCVC）在 held-out 轨道视角外推区把闭环成功率比同数据匹配对照提高 12.2 点（95% CI [7.4, 17.0]；独立第二训练种子下 +15.5，CI [11.7, 19.4]），效应被另外两个相机轴复现；而训练包络内的插值区两种子均零增益（−1.2 与 −4.3 点），分布内能力保持（−0.6 与 −0.2 点）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 1, Abstract; page 6-7, Section VI-D, Table II
- Evidence: 摘要主结果句给出全部关键量级：外推 +12.2/+15.5、两轴复现、插值零增益、ID 保持；桶级明细见 Table II（C02）。
- Quote: “On held-out orbital viewpoints beyond the training envelope, SCVC improves closed-loop success over the matched control by 12.2 points (95% CI [7.4, 17.0]; +15.5, CI [11.7, 19.4], under an independent second training seed)—an effect two further camera axes replicate—while interpolation within the envelope shows no gain in either seed (−1.2 and −4.3 points) and in- distribution competence is preserved (−0.6, −0.2).”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0412

- Claim: 桶级明细（第一训练种子，每任务 10 trials）：C2 方位角分布内桶 84.0→88.5（+4.52 [+2.65,+6.39]）、插值桶 86.3→85.1（−1.22 [−4.29,+1.84]，跨零）、外推桶 63.8→76.0（+12.20 [+7.40,+17.00]）；C1 dolly 外推 67.0→71.2（+4.24 [+0.71,+7.88]）而插值 null；C2 仰角外推（386 任务）54.9→63.7（+8.76 [+6.40,+11.11]）；C3 端点朝向轴插值/外推均 null（−0.97/−0.58）；四套件 ID 92.3→91.7（−0.60）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 7, Table II
- Evidence: Table II 给出预注册比较全表：两臂唯一差异是一致性权重；分布内桶为分布匹配上限而非 OOD 主张；外推桶是真正未见视角。
- Quote: “C2 azimuth in-dist 294 84.0 88.5 +4.52 (+2.65, +6.39) interp 49 86.3 85.1 −1.22 (−4.29, +1.84) extrap 100 63.8 76.0 +12.20 (+7.40, +17.00) C1 dolly in-dist 168 91.5 91.3 −0.18 (−1.90, +1.67) interp 46 88.7 89.6 +0.87 (−1.96, +3.91) extrap 99 67.0 71.2 +4.24 (+0.71, +7.88) C2 elevation extrap 386 54.9 63.7 +8.76 (+6.40, +11.11) C3 endpoint interp 62 92.6 91.6 −0.97 (−3.71, +1.61) extrap 226 88.6 88.0 −0.58 (−2.12, +1.02) ID (4 suites, 500 eps/suite) 92.3 91.7 −0.60”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0414

- Claim: 腕部相机混杂遮蔽审计（每条件 1,200 rollouts）：对发布腕部版 Cosmos 策略，遮蔽场景相机（被相机基准扰动的传感器）仅使成功率从 80.5%（Wilson 95% CI [78.2, 82.6]）降至 66.6%（[63.9, 69.2]，噪声填充 69.7%），遮蔽腕部相机则塌缩至 0.2%（[0.1, 0.7]）——策略在完全没有场景视图时仍解决三分之二相机扰动任务，而无腕部则完全无助；名义任务小型试点同构（140/180 场景遮蔽 vs 37/180 腕部遮蔽，填充类型间至多 5 点变化），公开 π0.5 LIBERO 策略同样场景遮蔽无碍而腕部遮蔽完全失效。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 5, Section VI-B, Figure 3
- Evidence: 遮蔽审计以'无输入仍成功证明输入不必要'的方向性论证隔离混杂；场景遮蔽仅掉 14 点而腕部遮蔽归零说明相机轨道分数由腕部视图承载。
- Quote: “Figure 3 presents a masking audit of the released wrist- enabled Cosmos policy run directly on the camera-perturbed tasks (1,200 rollouts per condition). Blacking out the scene camera, the very sensor the camera benchmark perturbs, lowers success only from 80.5% (unmasked, Wilson 95% CI [78.2, 82.6]) to 66.6% ([63.9, 69.2]), with a scene-noise fill at 69.7% ([67.0, 72.2]); blacking out the wrist collapses it to 0.2% ([0.1, 0.7]). The policy thus still solves two- thirds of camera-perturbed tasks”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0415

- Claim: 腕部混杂对基准数字的后果（Table I）：发布腕部版检查点 ID 98.5%/相机轨道 79.5%/掉点 19.0，而匹配的场景-only 参照 ID 93.2%/相机轨道 26.0%/掉点 67.2——ID 差约 5 点而相机掉点差近 50 点；官方排行榜独立模型家族 corroborate（OpenVLA-OFT 去 wrist 输入相机分从 56.4 掉至 10.4）；场景视图对腕部版策略仍有信息量（遮蔽它聚合掉 14 点，从 spatial 增益到 goal 大掉），但腕部视图是测量场景视角不变性的混杂因子。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 6, Table I
- Evidence: Table I 把遮蔽审计转化为基准后果：同一基准上腕部版与场景-only 的 ID 差 5 点、相机掉点差近 50 点；OFT 排行榜数字为独立家族佐证。
- Quote: “Policy ID Camera Drop Released ckpt (wrist) 98.5 79.5 19.0 Scene-only reference 93.2 26.0 67.2 OFT (wrist / none) – 56.4 / 10.4 – input from OpenVLA-OFT drops its camera score from 56.4 to 10.4 [4]. The scene view still informs wrist-equipped policies—masking it costs 14 points aggregate, ranging from a gain on spatial to a large drop on goal—and the audit shows the wrist view is a confound for measuring scene- view invariance, the quantity a camera benchmark intends to measure.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0416

- Claim: 场景-only 参照的零样本脆弱性量级：分布内 93.2% 而全相机轨道仅 26.0%，且掉点轴间不均——dolly 7.5%、轨道视角变化 21.4%、原地端点再定向 61.3%——轨道轴贡献基准大部分相机实例，是零样本差距的主要所在。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 6, Section VI-C
- Evidence: VI-C 以冻结场景-only 参照量化零样本差距并按轴分解，作为方法要解决的失效定位。
- Quote: “The scene-only reference reaches 93.2% in distribution yet 26.0% on the full camera track, and the drop is un- even across axes: 7.5% under dolly, 21.4% under orbital viewpoint change, 61.3% under in-place reorientation. This is the zero-shot gap the method addresses, and the orbital axis, which contributes the majority of the benchmark’s camera instances, is where most of it lives.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0421

- Claim: 对照设计的因果分离：两模型在同一 carve 配对 manifest、同一场景-only 基础检查点上训练——λ_CV=0 的对照与 λ_CV=2.0 的 SCVC；因对照的两支均接收监督损失，它是相机增广基线，方法-对照差在相同数据、初始化与预算下隔离出一致性项本身的效应。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 5, Section V-C
- Evidence: 对照看到与 SCVC 完全相同的扰动相机配对；外推增益因此可归因一致性项而非数据暴露。
- Quote: “Two models are trained on the identical carved manifest from the same scene-only base checkpoint: a control with λ CV = 0 and the method (SCVC) with λ CV = 2.0. Because the control receives the supervised loss on both branches, it is a camera-augmented baseline, and the method- minus-control difference isolates the consistency term under identical data, initialization, and budget.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-1098

- Claim: 应用方式：固定服务机器人以机顶 360° 全景相机（egocentric panoptic 360° 图像）为唯一视觉传感器，在 9 个真实环境、跨 3 个月共 20 天的部署中采集 in-the-wild 人机交互预期数据集 HUI360（多天/多环境/自然发生行为），并配套开放任意 360° 等距柱面视频的自动交互标注管线与人工修正接口；原始 360° 全景图像按 GDPR 按需开放（仅限研究用途）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 1, Abstract
- Evidence: 摘要给出：最大 in-the-wild HRI 预期数据集、移动机器人多天多环境采集、任意 360° equirectangular 视频的自动标注管线、1M 预处理标注与原始 panoptic 360° ego 图像（GDPR 按需）。
- Quote: “we introduce HUI360, the largest dataset for human-robot interaction anticipation in the wild and its set of baselines. The dataset was collected from a mobile robot, in the wild, over multiple days within a 3-month period, and in several environments, capturing natural, spontaneous behaviors from both passersby and users, and encompassing a diverse range of individuals. This variety enables evaluating and improving the generalization capabilities of interaction anticipation models. We designed”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1099

- Claim: 全景 FoV 与规模的组合缺口被填补：在 Table I 所列 9 个 HRI 预期相关数据集中，HUI360 是唯一同时具备 360° FoV、612K 帧、4310 tracks、375 次交互、开放 2D poses、视频与 9 个场景的 in-the-wild 数据集；既有 360° 数据集要么无 tracks/poses（SSUP-HRI 1.4M 帧 0 tracks）、要么规模小（ATC 33K 帧 4 tracks），而具细粒度标注的多为窄 FoV Kinect 数据（90°-100°）——Ours+SSUP-A 合计 1.8M 帧、32,008 tracks、794 交互。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 2, Table I（图 1 概览同页）
- Evidence: Table I 以 #Frames/#Tracks/#Interaction/Available/Curated/FOV/Poses/Video/#Scenes/ITW 十维对比 9 个数据集；Ours 行 612K/4310/375/360/2D/9，Ours+SSUP-A 行 1.8M/32,008/794。
- Quote: “Ours 612K 4310 375 ✓ ✓ 360 2D ✓ 9 ✓ Ours+SSUP-A 1.8M 2 32 008 794 ✓ ✓ 360 2D ✓ 9 + Mobile”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1100

- Claim: 全景图像的处理代价与解法：直接把 ERP 全景图喂给未在全景图上训练的模型有负面影响，故检测/过滤/分割/跟踪全部改在 region-images（全景图的裁剪区域）上进行——检测用 4 个带 wrap-around 的重叠固定区域（各 W/2×H、仅保留中心半区避免重复），跟踪/分割用围绕目标的移动区域逐帧推进，过滤基于 box 尺寸、mask 尺寸与有效关键点数。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 4, Section III-C.1 与 Fig. 2/Fig. 3（Algorithm 1 见 page 15）
- Evidence: Section III-C.1 与 Fig. 2/3 说明 region-images 缓解 panoptic 图像对未训练模型的负面效应、4 个 wrap-around 重叠固定区域与中心半区去重、Algorithm 1（page 10/15）给出形式化流程。
- Quote: “In practice, we performed the steps of detection, filtering, segmentation and tracking using region-images (crops of the panoptic image) to mitigate the negative effects of directly using panoptic images on models that have not been trained with them. The full process is briefly illustrated in Figure 2 (detection and filtering) in Figure 3 (tracking and segmentation) and is detailed in the supplementary materials (Algorithm 1). Fig. 2. Detection and filtering process in equirectangular images: t”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1101

- Claim: 交互的自动标注以几何判据完成：只认与平台的物理交互（拿取/放置/投掷），把交互区（HUI360 为机器人托盘、SSUP-A 为垃圾桶顶）与人分割掩码的相交作为交互判据；HUI360 相机固定故交互区在画面中位置固定、判定直接；SSUP-A 相机随垃圾桶移动且自稳定导致交互区在画面中漂移，需逐帧用 SAM2 跟踪交互区并取 Convex Hull 再求交——方法适用于任意固定或移动交互区（要求凸形状）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 4, Section III-C.2 Automatic detection of interactions
- Evidence: Section III-C.2 定义物理交互与交互区判据，说明 HUI360（固定区）与 SSUP-A（移动区+Convex Hull）两种情形及凸形状适用条件。
- Quote: “We adopt a precise definition of an interaction where we only consider physical interaction with the platform. In practice, we define an interaction zone (the trashcans in SSUP-A and the plate of the robot in HUI360) and consider that someone is interacting when their segmentation mask intersects with this zone. Doing so is straightforward in HUI360, as the interaction zone occupies a fix place in the camera frame, but the mounting of the camera on the trashcans of SSUP makes that they move and”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1102

- Claim: 姿态提取采用互补双模型：ViTPose-B（17 COCO 关键点，256×192 稳健）与 Sapiens-0.6B-Pose-308（308 关键点含 242 面部，1024×768 高精度）；全景图中人像尺度分布为 26% 框高<256、73% 在 [256,1024]、0.4%>1024，多数人像对 ViTPose 下采样、对 Sapiens 上采样，最终 73% 的 ViTPose 与 62% 的 Sapiens 关键点（面部 64%、其余 55%）有效（score c>0.5）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 5, Section III-C.3 Automatic extraction of pose
- Evidence: Section III-C.3 报告两种姿态模型的分辨率互补性与全数据集关键点有效率统计（按 ×1.25 框扩张口径）。
- Quote: “Two methods were used because they appear to be com- plementary. Indeed, ViTPose operates reliably and robustly at reasonable working resolutions (256×192), whereas Sapiens works at much higher resolutions (1024×768) but provides a very precise estimation with keypoints on the face and hands. In our dataset 26% of the boxes have and height h < 256, 73% have h ∈ [256, 1024] and 0.4% have h > 1024 (after ×1.25 expansion as used for those methods). Meaning that most of the persons images are downsc”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1103

- Claim: 跨域扩展 SSUP-A：为检验跨机器人平台迁移，把自动管线加标注到既有 SSUP-HRI 数据（纽约公共广场、2 个 field sessions 相隔一年、2 台移动垃圾桶机器人配 360 相机、Wizard-of-Oz 操作），共平均每帧 5.5 人、总计 1.15M 帧的检测/跟踪/标注——移动平台+视角偏移+截然不同的行为域使其成为迁移性基准，并与 HUI360 共享同质标注协议。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 3, Section III-B.2 SSUP-A: Extension to other domains
- Evidence: Section III-B.2 说明 SSUP-A 的来源（2 sessions×5 days、公共广场、2 mobile trash barrels with 360 cameras、Wizard of Oz）与标注规模（average of 5.5 persons per frame、total of 1.15M frames）。
- Quote: “To push even further the diversity of environments, we annotated the SSUP-HRI dataset [1], which was collected in the wild during 2 field sessions of 5 days each, one year apart, on public squares of New York using 2 mobile trash barrels equipped with 360 cameras and operated in a Wizard of Oz fashion. The videos exhibit a full range of passerbys and users all around, with individual and group interactions. The different nature of behaviors, the shift in viewpoint, as well as the use of a mobile”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1104

- Claim: 质量控制靠人工策展：全套视频人工观看，可整集作废（异常行为归因于机器人新鲜感、操作员在场执行技术任务、不可恢复的跟踪失败、伦理协议与 GDPR 撤回）、可删/拆/并 track、可修正交互标签（SSUP-A 的假阴性投掷与凸包假阳性）；掩码与关键点不做逐点修正、失败即整 track 作废——最终 15% 的 episodes 被标记且不导出。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 5, Section III-D Manual curation
- Evidence: Section III-D 说明策展动作类型（作废/删/拆/并/改标签）与原因类别，给出 15% episodes flagged 未导出的量化结果。
- Quote: “To ensure the quality of the data we share, we proceeded to manual curation using specifically designed user interfaces. Our curation consisted in (1) flagging full episodes as invalid for reason such as: multiple abnormal behaviors attributed to the novelty of the robot’s presence, presence of the operator for technical task (launching/stopping recording, maintaining the robot), multiple and non recoverable tracking issues, removal request in compliance with our ethics protocol and GDPR, (2) co”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1105

- Claim: 主基线效果：以 mask 面积（距离代理）+框位置+ViTPose 关键点为特征（D3）、T_ADV=15（提前 1s），LSTM 在 HUI360 留出环境上 AUC 0.91（MLP 0.86、RF 0.81）；跨数据集零样本（换机器人平台）LSTM 为 HUI360→SSUP-A 0.84、SSUP-A→HUI360 0.84、SSUP-A 原生 0.88——LSTM 全面优于 MLP/RF，平台变化带来可见但非毁灭性的 AUC 下降。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 7, Table III 与 Section IV-C.1
- Evidence: Section IV-C.1 Transfer capabilities 与 Table III 报告 RF/MLP/LSTM 在两数据集 native 训练下的 in-dataset 与 cross-dataset AUC。
- Quote: “As reported in Table III, the LSTM model outperforms the MLP and Random Forest in all scenarios. As expected, a change in the robotic platform results in a noticeable drop in performance under cross-dataset evaluation. These findings establish an initial baseline emphasizing generalization for robots operating in unseen, in-the-wild environments. TABLE III AUC OF MLP, RF AND LSTM. EACH MODEL IS TRAINED ON ITS NATIVE DATASET, AND SUBSEQUENTLY EVALUATED IN A CROSS-DOMAIN TRANSFER SCENARIO. HUI360”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1107

- Claim: 前瞻时域退化平缓：观测窗离交互起点越近越易判对，AUC 随 T_ADV（5→30 帧，即 0.33→2.0s）呈近似规律下降——LSTM 0.97/0.94/0.89/0.87/0.84/0.77、MLP 0.96/0.92/0.89/0.86/0.84/0.76、RF 0.90/0.84/0.81/0.78/0.73/0.71；MLP 与 LSTM 优于 RF 且退化更缓——2 秒前瞻仍有 0.77 的排序能力，但可靠预警窗口实质在 1s 内（≥0.89）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 7, Table V 与 Section IV-C.1
- Evidence: Section IV-C.1 Forecasting capabilities 与 Table V 报告六档 T_ADV 下三基线 AUC（仅用足够长的 track 以支持 30 帧采样）。
- Quote: “Forecasting capabilities On Table V, we provide the baseline of our proposed models. Unsurprisingly, the closer the observation window is to the onset of the interaction, the easier it becomes to correctly classify the anticipation. Moreover, the decrease in performance follows a fairly regular trend. It can also be observed that the MLP and LSTM outperforms the Random Forest and exhibit a more gradual degradation in performance as T ADV increases. Classifiers and trained and evaluated with the”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-0654

- Claim: Spheriverse 的采集平台由一台球面相机（DuxCam M4，图像分辨率 5188×1979）与一台 Hesai OT128 128 线 LiDAR 构成，以 LiDAR 坐标系为参考标定相机内参与外参；数据集含 644 条序列、覆盖 13 个地理与视觉多样的区域。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 4, Section 3 and Section 3.1, Data Collection
- Evidence: 第 3.1 节数据采集披露传感器配置（DuxCam M4 5188×1979 + Hesai OT128 128 线 LiDAR、Zhang 内参标定、以 LiDAR 为参考标外参、PTP 时钟对齐）；第 3 节开头给出 644 序列/13 区域规模。
- Quote: “introduce Spheriverse, a real-world spherical dataset with rich semantic annotations, comprising 644 sequences from 13 geographically and visually diverse regions. Equipped with a high-quality spherical camera and a 128-beam Li- DAR, Spheriverse provides dense observations to support research on spherical 3D perception. TABLE 2 Data distribution across four daily time periods for 644 sequences: night (20:00–05:00), dawn (05:00–07:00), daytime (07:00–18:00), and evening (18:00–20:00). Density den”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0655

- Claim: 作者把球面 3D 感知的核心挑战归结为跨空间表示差异：球面观测编码在角域而目标表征位于稠密度量体素空间，这一分歧引发物体外观、几何与空间关系上的一系列投影诱导畸变。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 2, Section 1, Introduction
- Evidence: 引言指出 angular observations 与 metric voxels 的分歧造成 cross-space representation gap 与 projection-induced distortions；SphereOcc 的 CSRR/SER 两模块即为弥合该差异而设计。
- Quote: “This divergence creates a cross-space representation gap between angular observa- tions and metric voxels, giving rise to a range of projection- induced distortions in object appearance, geometry, and spatial relationships.”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0656

- Claim: 在 Spheriverse 语义占据预测基准上（Table 3，统一协议），SphereOcc 达 13.91% mIoU 与 24.65% GeoIoU，超过此前最强方法 TPVFormer（12.21% mIoU）与 SurroundOcc（22.55% GeoIoU），绝对增益 1.70 与 2.10 个百分点（相对提升 13.9% 与 9.3%）；并在全部五类场景子集的两个指标上均排名第一，九类语义中七类 class-wise IoU 最佳。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 9, Table 3 and Section 5.1.1, Results and Analyses
- Evidence: Table 3 总体结果与正文分析：SphereOcc 13.91/24.65 对 TPVFormer 12.21（mIoU 最强先前）与 SurroundOcc 22.55（GeoIoU 最强先前），+1.70/+2.10pp，五场景全第一、七类 IoU 最佳。
- Quote: “As shown in Table 3, SphereOcc achieves the best overall performance, reaching 13.91% mIoU and 24.65% GeoIoU. For mIoU, SphereOcc surpasses TPVFormer [18], the strongest prior method for this met- ric (13.91% vs. 12.21%). For GeoIoU, it outperforms Sur- roundOcc [19], the strongest prior method for this metric (24.65% vs. 22.55%). These results correspond to absolute gains of 1.70 and 2.10 percentage points, or relative im- provements of 13.9% and 9.3%, respectively. SphereOcc also ranks first i”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0658

- Claim: 组件消融（SurroundOcc 基线逐步加模块）：把 ResNet 换成预训练 InternImage-T 骨干使 mIoU 从 12.05% 升至 12.14%、GeoIoU 从 22.55% 升至 23.35%；再加 CSRR 升至 12.71%/23.50%（增益 0.57/0.15pp）；SER 贡献最大增量，把 mIoU 与 GeoIoU 提升至 13.91% 与 24.65%。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 11, Section 6.1 and Table 6 (page 13)
- Evidence: Table 6 消融：骨干升级 +0.09 mIoU、CSRR +0.57、SER 最大增量至 13.91/24.65；作者明确 SER produces the largest incremental improvement。
- Quote: “As shown in Table 6, replacing ResNet [105] with the pretrained InternImage- T [104] improves mIoU from 12.05% to 12.14% and GeoIoU from 22.55% to 23.35%, confirming the effectiveness of the stronger backbone. Adding CSRR further increases mIoU to 12.71% and GeoIoU to 23.50%, with gains of 0.57 and 0.15 percentage points, respectively. By incorporating range–azimuth relations into the lifted voxel features, CSRR strengthens their correspondence with spherical geometry before occupancy decoding.”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0662

- Claim: 在 BEV 语义制图基准上，专为球面观测设计的 OneBEV 取得最高整体 mIoU（22.66%），超过第二名 HDMapNet（20.71%）1.95 个百分点，并在全部五类场景子集排名第一，在结构受限场景优势最大（23.15% vs 20.28%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 10, Section 5.2 and Table 4 (page 11)
- Evidence: Table 4 十方法对比：OneBEV 22.66% mIoU 第一、HDMapNet 20.71% 第二；OneBEV 五场景全第一、结构受限场景 23.15% vs 20.28% 优势最大。
- Quote: “For semantic mapping, Table 4 shows that OneBEV [35], which is specifically designed for spherical observations, achieves the highest overall mIoU and outperforms the second-ranked HDMapNet [81] by 1.95 percentage points (22.66% vs. 20.71%). OneBEV also ranks first across all five scene subsets, with its largest ad- vantage observed in structurally constrained scenes (23.15% vs. 20.28%).”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0664

- Claim: 作者给出纯相机球面感知的动机：引入 LiDAR 带来额外传感器负载、功耗与车载计算开销，对紧凑具身平台构成相当大约束；因此 SphereOcc 选择相机路线，以解决角域与笛卡尔体素空间之间的跨空间表示差异。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 4, Section 2.2, Semantic Occupancy Prediction
- Evidence: 相关工作节（Sec 2.2）指出 LiDAR-assisted 方法的传感器负载/功耗/算力代价对 compact embodied platforms 的约束，并据此提出 camera-based spherical 3D perception 路线。
- Quote: “LiDAR entails additional sensor payload, power consump- tion, and onboard computational overhead, imposing con- siderable constraints on compact embodied platforms. In this work, we propose SphereOcc for camera-based spher- ical 3D perception to address a cross-space representation gap between the angular domain and Cartesian voxel space.”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-1062

- Claim: 应用方式：超低空无人机机载平台上，把四路硬件同步鱼眼视频流实时拼成开放的 1280×640 等距柱面全景（ERP）接口，作为下游感知/定位任务的统一可复用视觉接口；机载计算为 Jetson Orin NX，整机为定制碳纤维机架（相机+计算+飞控+GNSS 一体）。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 1, Abstract 与 Section I Introduction（Fig. 1）
- Evidence: 摘要与前言给出系统概念：四路同步鱼眼流→开放 ERP 接口→下游目标检测与定位；ERP 使角覆盖成为显式操作选择。
- Quote: “Abstract—Ultra-low-altitude unmanned aerial vehicles (UAVs) require surround vision near buildings, vegetation, and other obstacles. We present a parallax-aware onboard platform that converts four synchronized fisheye streams into an open 1280 × 640 equirectangular panorama (ERP) interface.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1063

- Claim: 多鱼眼环视的核心挑战与方案分界：四相机各自有不同光心，近处与远处内容需要不同投影深度（视差）；封闭消费级全景相机隐藏原始视图与标定，开放 rig 则把同步、标定、拼接与运行时控制转移给机器人——本文选开放 rig 并按相邻相机重叠区独立选择投影深度（离散半径库 R={1,2,4,12,30} m，page 4）来处理视差。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 1, Section I Introduction；半径库 R={1,2,4,12,30} m 见 page 4, Section IV-A
- Evidence: 前言'Angular coverage is the first requirement'段说明四相机不同光心导致近/远内容需要不同投影深度、封闭全景相机隐藏原始视图与标定、开放 rig 把同步/标定/拼接/运行时控制转移给机器人。
- Quote: “Angular coverage is the first requirement. Four cameras have different optical centres, so near and far content require different projection depths. A mount or camera-order change can invalidate calibration, while independent exposure control produces visible colour layers. Closed consumer panoramic cameras hide the raw views and calibration. Open rigs expose them, but transfer synchronization, calibration, panorama formation, and runtime control to the robot.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1064

- Claim: 平台硬件规格：定制碳纤维四旋翼 28×28×13.3 cm、含 4000 mAh 电池重 1002.3 g（不含 693.2 g）、辅助载荷上限 500 g、推重比 4.2:1、25 W 模式无载荷续航 9 min；四路硬件同步全局快门鱼眼相机 1088×1280@20 Hz、标称 200° FoV、USB 3.0；Jetson Orin NX 16 GB 在 25 W 模式形成 1280×640 ERP，目标每 20 Hz 输入组发布一帧全景。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 3, Section III-A 与 Table II（Table II 跨 page 3-4）
- Evidence: Section III-A 与 Table II 给出整机尺寸/重量/推重比/续航、相机分辨率/帧率/FoV/接口与板载计算配置。
- Quote: “The platform measures 28 × 28 × 13.3 cm and has a measured mass of 1002.3 g with a 4000 mAh battery and 693.2 g without it. It supports up to 500 g auxiliary payload and has a 4.2:1 thrust-to-weight ratio. With no auxiliary payload and the Jetson configured in 25 W mode, the measured endurance is 9 min. The integrated sensing assembly provides four hardware-synchronized global-shutter streams at 1088×1280, 20 Hz, and nominal 200 ◦ FOV through USB 3.0.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1065

- Claim: 评测数据集：真实飞行采集 18 条完整序列、>50,000 个有效四视图组、覆盖 7 个场地（Court/Farmland/Lake/North Playground/North Square/South Playground/South Square），含白天与夜间重访及 teach-repeat 飞行；另有一条近场序列作近距离结构压力测试；全景评测采用按序列或场地不相交的划分以避免相邻帧泄漏。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 4, Section III-C Field data for evaluation（Fig. 3 在 page 5）
- Evidence: Section III-C 描述采集范围：自然与人工场地、teach-repeat、昼夜重访；按 sequence/site 划分避免泄漏。
- Quote: “The collection spans natural and built sites, teach–repeat flights, and daytime and night-time revisits recorded as syn- chronized four-view data (Fig. 3). The curated field record contains 18 complete sequences and more than 50,000 valid four-view groups across seven field sites: Court, Farmland, Lake, North Playground, North Square, South Playground, and South Square. South Playground and South Square include both daytime and night-time revisits. An additional near-field sequence provides a cl”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1066

- Claim: 拼接几何效果：远场样本中 Ours 的特征错位 Med./P90 为 3.81/5.82 像素，优于 Fixed Depth 的 5.66/9.97（P90 相对削减 41.6%，摘要口径）与 Adaptive Seam 的 3.99/6.02；近场样本中 Ours 取得最佳 Med./P90（2.32/10.33 像素）并与 Adaptive Seam 并列最佳接缝 RGB 中位数（8.50），Fixed Depth 近场中位错位 10.12 像素、Adaptive Seam 近场 P90 18.27 像素。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 7, Section V-A 与 Table III（41.6% 表述在 page 1 Abstract）
- Evidence: Section V-A 文字与 Table III 报告远/近场各 60 帧条件下的 AKAZE 特征错位中位数/P90 与接缝 RGB 中位数（评估特征与选择特征的 SIFT 相互独立）。
- Quote: “In the far-field sample, Ours achieved median/P90 mis- alignment of 3.81/5.82 pixels, compared with 5.66/9.97 pixels for Fixed Depth and 3.99/6.02 pixels for Adaptive Seam. In the near-field sample, Ours achieved the best median/P90 misalignment (2.32/10.33 pixels) and tied Adaptive Seam for the best seam RGB median (8.50).”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1067

- Claim: 跨场地持续泛化（held-out）：在预留的 Lake 与 South-Square teach/repeat 片段上，Ours 取得 Med./P90/最差重叠 P90 为 5.23/8.95/9.98 像素、CIEDE2000 色差 2.403，均优于 Global Radius 的 5.42/9.29/10.20 与 2.406——在 held-out 场地上聚合几何误差最低，但相对最优基线的边际很小（<0.2 像素/0.003 色差）。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 7, Section V-A 末段（Table IV 在 page 8）
- Evidence: Section V-A 末段与 Table IV 报告 held-out lake/south-square 连续片段的错位与色差，所有方法均产出完整 ERP；作者注明帧间相关故只做描述性汇报。
- Quote: “Ours achieved median, P90, and worst-overlap P90 errors of 5.23, 8.95, and 9.98 pixels in Table IV. The corresponding Global Radius values were 5.42, 9.29, and 10.20 pixels. Ours tied the best seam RGB median at 3.33 and achieved CIEDE2000 colour consistency of 2.403, compared with 2.406 for Global Radius.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1069

- Claim: 下游检测接口收益：用冻结 YOLOv10-N 在匹配的起飞后远场全景上评测，八扇区 ERP 采样把人员响应覆盖从单前向扇区的 6.9% 提升到 55.1%，高于直接 ERP 推理的 39.4% 与四扇区的 46.4%——环视接口相对前视的覆盖增益约 48 个百分点（6.9%→55.1%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 7, Section V-A object-detection interface validation（Fig. 5(b) 在 page 8）
- Evidence: Fig. 5(b) 与正文报告前向扇区、直接 ERP、四扇区、八扇区四种采样的人员响应覆盖率，含 95% bootstrap 置信区间；作者注明该指标不度量检测器再训练或真值检测精度。
- Quote: “Using frozen YOLOv10-N, Fig. 5(b) evaluates the exported ERP represen- tations of Ours on matched post-takeoff far-field panoramas. Eight sectors increased response coverage from 6.9% for the forward sector to 55.1%, compared with 39.4% for direct ERP inference and 46.4% for four sectors.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1075

- Claim: 开放接口对比（Table I）：在所列研究级 aerial 系统与消费级 360 相机中，只有本平台同时开放硬件、软件、数据、ERP 输出与鱼眼原始输出五项（Ours 全 ✓）；PanoAir/RflyPano 硬件不开放；OmniNxt 数据不开放且无 ERP 输出；Omni-Swarm 无 ERP 输出；Insta360 X5/DJI Osmo 360 消费全景相机仅 ERP 输出、其余均不开放——开放原始视图与标定是把多鱼眼感知交还给机器人侧研发的关键接口属性。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 2, Table I 与 Section II-A 末段
- Evidence: Table I 以 ✓/– 列出各系统的硬件/软件/数据开放性与 ERP/鱼眼输出接口；正文总结这些接口级差异。
- Quote: “TABLE I PUBLIC AVAILABILITY AND OUTPUT INTERFACES OF RESEARCH AERIAL SYSTEMS AND COMMERCIAL 360 CAMERAS. ✓: PUBLICLY RELEASED; –: NOT RELEASED OR NOT STATED IN THE CITED SOURCE. System/product Hardware open Software open Data open ERP out. Fisheye out. PanoAir [3] – ✓ ✓ ✓ ✓ RflyPano [4] – ✓ ✓ ✓ ✓ OmniNxt [10] ✓ ✓ – – ✓ Omni-Swarm [11] – ✓ ✓ – ✓ Insta360 X5/DJI Osmo 360 [12], [13] – – – ✓ – Ours ✓ ✓ ✓ ✓ ✓”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-0451

- Claim: 在腕装鱼眼 GoPro 为唯一视觉输入的 vision-only 扩散策略下，成功率呈清晰任务梯度：简单 pick-and-place 超过 80%（Table 2 中 pick cube 85%、pick carrot 80%），精度类任务 60-65%，而需要触觉推理的复杂任务显著退化——pull drawer 仅 40%（多数失败源于在错误方向施加过大力）、peg in hole 仅靠视觉常无法对准、open bottle vision-only 仅 20%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 8, Section 5.3 Real World Evaluation Result (numbers in Table 2 page 7 and Table 3)
- Evidence: Section 5.3 非触觉评估：策略在简单 pick-and-place 上超 80%（展示充分空间演示质量），pick broccoli 因滑腻表面与不规则几何降至 60%，精度类仍超 60%；复杂任务退化——pull drawer 仅 40% 且多数失败为错误方向过度施力，peg in hole 常无法仅凭视觉对准；Table 2/3 给出 open bottle vision-only 20%。
- Quote: “The success rate of “pick broccoli” task slightly drops to 60% due to the slippery surface and irregular geometry. Tasks involving precision manipulation (“stack” and “insert”) are more challenging, but we still reach over 60% due to the accurate robot proprioception of exUMI. Complex tasks requiring reasoning with tactile feedback show performance degradation. “Pull drawer” achieves merely a 40% success rate, and the majority of failures occur when the policy applies excessive force in incorrec”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-1214

- Claim: MDE 深度先验的密度-精度权衡：SLAM 依赖深度估计的稠密重建特性把覆盖扩展到观测次数更少的区域并增加重建点数；两种 SLAM 的重建密度与覆盖均高于 SfM；但 RGB-D SLAM 相对 RGB SLAM 的平均重建点数与覆盖率下降，作者将其归因于 RGB-D 重建中更低的噪声——该噪声水平差异用 Hausdorff 距离指标可以更好理解。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 9, Section 5 Discussion; page 7, Table 1
- Evidence: page 9 Section 5 Discussion：dense reconstruction 扩覆盖增点数；RGB-D vs RGB 点数/覆盖下降归因 lower noise；Hausdorff 更好理解噪声差异。Table 1 数字见 page 7。
- Quote: “The dense reconstruction nature of the SLAM algorithm, which relies on depth esti- mation, helps extend coverage to areas with a smaller number of observations and increases the number of reconstructed points. While both SLAM methods have higher reconstruction density and coverage compared to SfM algorithm, a decrease in average number of reconstruction points and coverage in the RGB-D SLAM compared to the RGB SLAM can be attributed to lower noise in the RGB-D reconstruction. This lower noise le”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1244

- Claim: 多相机扩展的计算代价可控且有嵌入式实测：相对 FAST-LIVO2，Omni-LIVO 在 Hilti（3 相机）引入 1.16× 开销（60.3 vs 52.1 ms/帧）、自定义序列（4 相机）1.21×（40.6 vs 33.6 ms/帧），主因跨相机约束计算；在 NVIDIA Jetson AGX Orin（12 核 ARM 2.2GHz、64GB）上维持 10Hz 实时，内存 2906 MB（Hilti）/2359 MB（Custom）——宽 FoV 多相机的部署收益以约 1.2× 计算开销为条件，在 10Hz 数据率下嵌入式可行。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 6-7, Section IV-C and Table III
- Evidence: IV-C 给出复杂度 O((N_p+N_cross)·P·L)、Jetson 平台参数与 1.16×/1.21× 结论；Table III 给出逐序列时间/内存（Hilti 3 相机平均 60.3 ms、Custom 4 相机平均 40.6 ms）。
- Quote: “Compared to FAST-LIVO2, Omni-LIVO introduces 1.16× overhead on Hilti (60.3 ms vs. 52.1 ms, 3 cameras) and 1.21× on custom sequences (40.6 ms vs. 33.6 ms, 4 cameras), primarily due to cross-camera constraint computation, while maintaining real-time 10Hz performance with 2906 MB (Hilti) and 2359 MB (Custom) memory consumption, demonstrating practical viability for embedded platforms.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1249

- Claim: 本文环视宽覆盖的实现路径是多台非重叠 90° FoV 相机的拼接而非鱼眼单机光学：图 3 以 Left/Front/Right 三台 90° FoV 相机示意跨视角迁移，方法章未使用鱼眼投影模型或畸变处理（全文 fisheye 仅出现于相关工作对 BAMF-SLAM 的描述及该参考文献标题）——该证据限定：Omni-LIVO 属于综述问题中'环视/多相机宽 FoV'维度的证据，不能作为鱼眼光学（畸变建模）维度的证据。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 3, Fig. 3; page 2, Section II-C
- Evidence: 图 3 图注给出三台 90° FoV 相机的跨视角迁移示意；全文 fisheye 检索仅 2 处（II-C 对 BAMF-SLAM 的描述、参考文献 [19] 标题）；方法章投影函数为通用 π_c(·)。
- Quote: “maintaining photometric continuity across non-overlapping 90 ◦ FoVs through Cross-View residuals.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1250

- Claim: 唯一多相机基线 OpenMAVIS（多相机视觉-惯性、无 LiDAR）呈现两极表现：部分序列优于单目 LIVO 基线（Hilti 2022 Attic to Upper Gallery 0.103 m vs FAST-LIVO2 0.150 m），但在几何退化场景大幅劣化（Construction Multilevel 0.933 m vs Ours 0.020 m；Outside Building 0.425 m vs 0.016 m）——多相机宽 FoV 视觉约束在缺少 LiDAR 几何支撑时场景依赖性强，与 LiDAR 融合互补。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 6, Table II
- Evidence: Table II OpenMAVIS 列 27 序列数值：Hilti 2022 上多数序列 0.08-0.26 m 但 Multilevel 0.933、Outside Building 0.425 波动大；Newer College 上 0.084-0.255 m 居中偏弱。
- Quote: “Construction Multilevel 0.155 0.020 0.021 0.038 0.933 0.021 0.020 0.022 0.020 0.020”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1293

- Claim: Newer College 整体格局是条件性的：运动较平滑序列（Quad-Easy 0.068595、Math-Easy 0.080021、Cloister 0.080777 等）本文定位精度与稳定性最优，Cloister 显著优于 FAST-LIVO2（0.080777 vs 0.277620）；但剧烈运动序列本文回退（Quad-Hard 0.089189 劣于 FAST-LIVO2 0.070212，Math-Hard w/loop 0.88219 劣于 FAST-LIO2 0.067132），Ours-LIO 在 6/8 序列 fail。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 6, Table II
- Evidence: Table II 汇总 Newer College 8 序列 6 种配置的 ATE RMSE：本文 w/loop 在 Quad-Easy/Math-Easy/Math-Medium/Undermine-Hard/Stairs/Cloister 最优或并列最优，Quad-Hard/Math-Hard 劣于最优基线；LVI-SAM 全部 8 序列 fail，Ours-LIO 仅 Quad-Easy 完成。
- Quote: “Sequence FAST-LIO2 Ours-LIO FAST-LIVO2 LVI-SAM (w/ loop) Multi-LVI-SAM (w/o loop) Ours (w/ loop) Quad-Easy 0.070734 0.072749 0.070027 fail 0.071064 0.068595 Quad-Hard 0.080453 fail 0.070212 fail 0.089902 0.089189 Math-Easy 0.111047 0.080668 0.131684 fail 0.080243 0.080021 Math-Medium 0.118592 fail 0.128942 fail 0.110313 0.107045 Math-Hard 0.067132 fail 0.103742 fail 0.089415 0.88219 Undermine-Hard 0.057463 fail 0.149832 fail 0.077561 0.077231 Stairs fail 3.032322 fail fail 0.701162 0.451100 Cloi”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1300

- Claim: 多鱼眼全景化的计算代价可控但不为零：四相机配置平均每帧处理时间是单相机配置的 2.15 倍（三数据集平均 98.042750 ms vs 45.555879 ms；Newer College 111.345361 ms、M2DGR 128.731194 ms、Hilti'2022 54.051696 ms），作者称全景特征模型与高效多相机特征融合机制使相机数增至四倍仅带来 2.15 倍计算开销。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 7, Section IV-D and Table V
- Evidence: Section IV-D 对比三个数据集上单相机与四相机配置的平均每帧处理时间；Table V 给出全部数值；作者据此主张全景模型的多视角感知计算效率。
- Quote: “As shown in Table V, the average processing time of the four-camera system is only 2.15 times that of the single-camera sys- tem.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-0487

- Claim: DP 基线在 7 个子任务、两个平台上的成功率为 33.33%-66.67%：铰接类开微波炉门（双平台 66.67%）与旋转类倒水（66.67%，Xarm6）最高，柔性物体放衣入洗衣机（33.33%，Flexiv）与放叉入筷笼（33.33%，Xarm6）最低——鱼眼采集数据在基础扩散策略下达到中等可用水平，任务类型调制收益。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 6, Table I
- Evidence: Table I 报告 DP 在 Make Sandwich（两子任务）、Place Tableware、Heat Food、Pour Water、Storage Shoes、Wash Clothes 上的双平台成功率；正文（page 6 V.A）说明因 DP 长程能力受限将长程任务拆为独立子任务验证，并称'即使最基础的基线模型，数据依然可靠'。
- Quote: “Task Sub-Task Description Manipulation Type Platform Successful Rate of DP Make Sandwich Place the lettuce leaves on the plate Pick-Place & Rotation Flexiv Rizon4 60.00% Xarm6 53.33% Place the bread slices on the plate Pick-Place & Rotation Flexiv Rizon4 60.00% Xarm6 60.00% Place Tableware Place the fork into the chopstick holder Pick-Place & Rotation Flexiv Rizon4 40.00% Xarm6 33.33% Heat Food Open the microwave door Hinged Flexiv Rizon4 66.67% Xarm6 66.67% Pour Water Pour the water from the bo”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0494

- Claim: 动作表征对比（Table II，数据源自 FastUMI 先行工作）：TCP（工具中心点）位姿表征的 ACT 变体显著优于关节空间 ACT——Pick Bear 从 20.00%（ACT）升至 80.00%（PoseACT 绝对），Sweep Trash 从 6.67% 升至 60.00%（PoseACT 相对）。
- Stance: `conditional` | Confidence: `citation-supported`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 6, Table II
- Evidence: Table II 给出四变体两任务成功率（ACT/Smooth-ACT/PoseACT 绝对/相对）；page 7 V.A 说明该表源自 FastUMI 先行工作 [21]，并解读 TCP 位姿对轨迹形状与动态特征的稳健捕捉、UMI 系数据（独立于机器人本体、使用末端状态）允许更细致表征真实操作的灵巧性与类人运动特征。
- Quote: “Joint TCP Task ACT Smooth-ACT PoseACT (Absolute) PoseACT (Relative) Pick Bear 20.00% 60.00% 80.00% 73.33% Sweep Trash 6.67% 26.67% 53.33% 60.00%”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0045

- Claim: 球面等变收益取决于卷积核设计：在 Spherical MNIST 上（训练不含随机旋转），distance-only 球面核在随机旋转测试下保持 85.43%-91.50% 准确率（PWC×3 为 85.43%、6 级傅里叶嵌入 MLP 为 91.50%），而引入方向分量的 distance×direction 核从无旋转 98.28% 降至随机旋转 43.54%，与平面 CNN 的旋转崩塌（98.45%→41.08%）相当。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 6, Table 2
- Evidence: 表 2 的核参数化消融显示径向核保持旋转一致性、方向核在无旋转下匹配平面精度但旋转下崩塌到平面水平；正文将此解释为方向核牺牲了等变性以捕获朝向敏感线索（如区分 6 与 9）。
- Quote: “Model NR↑RR↑ Planar 98.45% 41.08% S2CNN [6] 96% 94% SO(3) CNN [11] 98.7% 98.1% (1) Spherical Dis PWC×3 87.18% 85.43% (2) Spherical Dis MLP [8, 8],L= 0 67.01% 65.74% (3) Spherical Dis MLP [8, 8],L= 6 92.13% 91.50% (4) Spherical Dis×Dir MLP [16, 16],L= 898.28% 43.54% Table 2.MNIST Classification Results.All models are trained without random rotation.Ldenotes embedding levels.”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0046

- Claim: 旋转等变的实现还依赖位置采样的空间均匀性：在 Stanford 2D-3D-S 分割（无旋转训练）上，只有 icosahedron 采样 + 3 段离散核在随机旋转测试下保持 mIoU 28.09%（无旋转 28.78%），而 Fibonacci、HEALPix、quasi-random、equirectangular 采样在随机旋转下 mIoU 崩塌至 12.60%、13.87%、8.70%、12.87%，icosahedron 增加距离段数（4-6 段）也降至 21.39%-23.50%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 8, Table 6
- Evidence: 表 6 消融显示 icosahedron-3 是唯一在 RR 下基本持平的配置；作者总结非均匀采样引入空间偏置破坏等变性，更多段数则因每段样本减少而过拟合。
- Quote: “Location Sampler Distance Bins NR RR mIoU↑mAcc↑mIoU↑mAcc↑ Icosahedron 3 28.78% 45.27% 28.09% 41.18% Icosahedron 4 27.99% 45.52% 23.50% 35.57% Icosahedron 5 29.66% 45.36% 22.82% 34.69% Icosahedron 6 29.02% 45.95% 21.39% 33.40% Fibonacci 3 31.69% 47.63% 12.60% 22.79% HEALPix 3 29.59% 46.98% 13.87% 25.20% Quasi-random 3 29.85% 48.06% 8.70% 17.73% Octahedron 3 28.96% 44.12% 14.05% 24.57% Hexahedron 3 29.25% 45.41% 18.06% 29.27% Equirectangular 3 30.25% 46.69% 12.87% 23.48% Table 6.Ablation Study on”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0047

- Claim: 在单 batch 过拟合、禁用随机旋转的零样本镜头迁移设置下，球面 DeepLab v3 从针孔训练迁移到全景测试的 mIoU 为 35.62%，明显高于平面模型的 19.57%（+16.05 点），说明球面表示在大 FoV 差异方向上的跨镜头一致性更好。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 8, Table 5
- Evidence: 表 5 的迁移矩阵 pinhole 训练行显示球面模型在 panoramic 测试列（35.62%）远高于平面（19.57%）；作者解释球面模型跨镜头表现更一致，尤其当源/目标镜头 FoV 覆盖相似时，但 FoV 差异悬殊时降级更明显。
- Quote: “mIoU↑mAcc↑mIoU↑mAcc↑mIoU↑mAcc↑ Planar DeepLab v3[5] Pinhole53.75% 59.70%33.47%45.73%19.57%36.40% Fisheye67.95% 81.58% 68.54% 82.70%57.46%77.46% Panoramic51.56%62.24%55.57%67.91% 71.20% 92.12% Spherical DeepLab v3 Pinhole48.71% 62.21%36.51%62.07%35.62%61.05% Fisheye40.27%45.45% 54.65% 66.21% 48.04% 63.85% Panoramic36.54%42.38% 58.52% 69.75% 65.71% 90.44% Table 5.Zero-shot Lens Generalizability Test.Overfitted and tested on the same batch. Random rotation is disabled.”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0050

- Claim: USF 的镜头无关性以每相机已知标定为前提：方法要求输入图像带有任意相机模型下的已标定内参，由其导出逐像素单位射线向量（lens normal map）并定义图像坐标与球面坐标的双射。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 3, 3.1 Spherical Projection and Resampling
- Evidence: 3.1 节方法定义以 calibrated intrinsics 为输入前提，lens normal map 是整个投影管线的基础；全文没有未标定输入或标定噪声鲁棒性实验。
- Quote: “Given an input image with calibrated intrinsics under any camera model (e.g., pinhole, fisheye, or panoramic), we derive the per-pixel geometry as unit-norm R3 vectors. Col- lectively, they form alens normal map 2, which defines a bijectivemapping between image coordinates and spherical coordinates.”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0611

- Claim: 双投影成本收益（真 PAL 部署，QuadOcc）：Dual（原始环形+等距柱面双编码器）取得最佳占据质量 20.56 mIoU，优于 ER-only 20.03 与 Raw-only 19.76（+0.53/+0.80）——原始环形流单独用不足以取得最佳体素质量；但代价是相对 ER-only 参数 +86.5%（189.83M vs 101.76M）、峰值显存 +25.1%（2.14 vs 1.71 GB）、吞吐 -14.8%（15.46 vs 18.15 FPS），Raw-only 最快（25.18 FPS）最省显存（1.55GB）但牺牲召回与 IoU——在原生等距柱面输入（H3O）上 ER-only 才是实用选择，Dual 仅在'最后一丝精度'关键时启用。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 17, Section 6.4 and Table 9
- Evidence: 补充材料 6.4 节在同一骨干/训练计划下仅变投影路径：Dual 20.56 最好，ER-only 20.03，Raw-only 19.76；成本分析给出参数/显存/吞吐三维权衡与'enable Dual only when the last bit of precision is critical'结论。
- Quote: “Dual achieves the best overall occupancy quality, improving over ER-only by +0.45 IoU and +0.53 mIoU (48.92/20.56 vs. 48.47/20.03), with higher precision (66.69 vs. 65.77) at essentially unchanged recall (64.74 vs. 64.81). Raw- only is weaker on IoU/mIoU (47.70/19.76), indicating that using the raw annulus alone is insufficient for best voxel quality.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0766

- Claim: 在新建的轮腿机器人双鱼眼拼接基准 BipTrack 上，OmniTrack++ E2E/TBD 分别达 44.63/44.96 HOTA，超过最强通用基线 ByteTrack（44.10）与 MeMOTR（43.17），但相对 MeMOTR 的领先仅约 1.5 HOTA，远小于 QuadTrack 上的领先幅度。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 14, Table 3
- Evidence: BipTrack 上 MeMOTR（43.17 HOTA）几乎追平 OmniTrack++（44.63），提示在运动扰动较温和的数据上通用方法即可接近专用框架。
- Quote: “BipTrack Dataset E2E MOTRv2 Zhang et al (2023) 39.29 0.78 38.60 2.72 MeMOTR Gao and Wang (2023) 43.17 0.82 46.22 27.85 OmniTrack E2E (ours) 35.70 0.89 33.91 -16.30 OmniTrack++ E2E (ours) 44.63 0.84 46.81 21.63 TBD SORT Bewley et al (2016) 42.67 0.86 44.96 28.27 DeepSORT Wojke et al (2017) 41.15 0.90 38.56 22.61 ByteTrack Zhang et al (2022) 44.10 0.84 46.25 20.61”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0771

- Claim: 把跟踪输出反馈回检测器的机制移植到第三方 TBD 管线（OmniTrack++_Det 检测 + ByteTrack/HybridSORT 跟踪）时，JRDB 验证集上 ByteTrack 的 HOTA/IDF1 各提升 +0.48，HybridSORT 的 HOTA 提升 +0.28、IDF1 提升 +0.68——反馈机制的跨管线移植增益存在但幅度小（<1 点）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 14-15, Section 5.2.3 + Table 5
- Evidence: 反馈机制的外部有效性在小范围内成立（+0.28~+0.68），远小于框架整体的提升幅度，提示反馈只是全景 MOT 收益的一部分。
- Quote: “the com- parison between the third and fifth rows shows that incor- porating the feedback mechanism consistently improves tracking performance: within the OmniTrack++ framework, HOTA and IDF1 on ByteTrack increase by +0.48 and +0.48 points, respectively, while on HybridSORT, HOTA improves”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-1194

- Claim: 连续回归路线失败：把动作预测当作直接连续回归（输出原始 (Δθ1, Δθ2, Δz)、不做离散化）训练的模型严重过拟合训练分布，在留出测试集上任务完成率接近零——证实层级离散 token 表示对泛化是必要的。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 8, IV-B Analysis of Action Encoding
- Evidence: page 8 Section 4.2 Analysis of Action Encoding：direct continuous regression → severely overfit → near-zero task completion on held-out test set。
- Quote: “We also experimented with treating action prediction as direct continuous regression, training the model to output raw (Δ𝜃 1 , Δ𝜃 2 , Δ𝑧) values without discretiza- tion. The resulting model severely overfit to the training distribution and achieved near-zero task completion on the held-out test set, confirming that the hierarchical discrete token representation is essential for generalization.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1267

- Claim: 全景与鱼眼的路径定位：既有工作用鱼眼相机扩展 FoV、并为间接/直接 VO-SLAM 流水线适配投影模型，但这些方法仍是为鱼眼相机定制的扩展，未完全适配全景场景；要达到 360° FoV，ROVO 采用宽基线多鱼眼相机系统；与之相对，OpenVSLAM 支持便携 360° 相机捕获的全景输入。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 2, Section II
- Evidence: II. Related Works Omnidirectional Visual Odometry 段的领域地图式陈述；为作者对引用工作的定性，非实验结果。
- Quote: “Prior works [14], [15], [16] expand the field of view by employing fisheye cam- eras and adapting indirect and direct VO/SLAM pipelines [17], [4], [18] with appropriate projection models [19], [20]. Al- though these methods broaden the field of view, they re- main extensions tailored to fisheye cameras, not fully ac- commodating omnidirectional scenarios.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1269

- Claim: 分辨率-速度-精度三方权衡：默认 3840×1920 桌面 8 FPS；降到 1920×960 提速到 17 FPS 但平均 ATE 恶化 21.6%，960×480 到 22 FPS 但恶化 41.0%——全景图像的高分辨率既是精度来源也是主要算力负担，低分辨率反而靠减少像素位移与模糊稳定剧烈运动。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 7, Section V-C and Table V
- Evidence: V-C Hyperparameters 段 + Table V #R0/#R1 行；与 C16 瓶颈陈述、C15 边缘部署互证。
- Quote: “Downscaling the default resolution to 1920 × 960 (#R0) and 960 × 480 (#R1) raises FPS from 8 to 17 and 22, while worsening average ATE by 21.6% and 41.0%.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-0375

- Claim: RoboPaint 用专用数据采集房的多相机阵列采集人类演示：每间房配备由高分辨率 RGB 相机与标定过的 RGB-D 传感器（Intel RealSense D455）组成的多相机阵列，相机刚性安装并预标定到桌面世界坐标，以支持精确 3D 重建与操作轨迹的跨视角对齐。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 3, Section 3.1 Human Data Acquisition
- Evidence: 采集端硬件形态：固定多相机阵列 + 刚性安装 + 桌面世界坐标预标定，是"数据房式"环视采集的代表配置；全文相机均为常规透视机型。
- Quote: “we have constructed many dedicated Data-Acquisition-Rooms, each equipped with a multi-camera array comprising both high-resolution RGB cameras and calibrated RGB-D sensors (Intel RealSense D455). All cameras are rigidly mounted and pre-calibrated with respect to the table world coordinate, enabling accurate 3D reconstruction and cross-view alignment of manipulation trajectories.”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0376

- Claim: 该采集系统同步记录 11 路 RGB 视觉信号（每路 1200×1920）、3 路 RGB-D 多模态信号（每路 720×1280）、15 通道触觉信号（总分辨率 3465×3）与 29 通道本体感知关节信号（29×1）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 2, Section 1, contributions bullet 1
- Evidence: 采集系统通道规格：视觉（RGB/RGB-D）、触觉、本体感知三类信号的同步通道数与分辨率；注意摘要/贡献/正文三处触觉与关节数字口径不一（见 reader_inferred）。
- Quote: “We developed a high-fidelity multimodal data acquisition system capable of synchronously recording 11 channels of RGB visual signals (each has the resolution of 1200 × 1920), 3 channels of RGB-D multi-modal signals (each has the resolution of 720 × 1280), 15 channels of tactile signals (in total resolution of 3465 × 3), and 29 channels of proprioceptive joint signals (in total of 29 × 1).”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0389

- Claim: 作者报告（部署行为定性对比，Fig.6）：Real-Sim-Real 数据训练的模型部署执行更平滑、更稳定，而遥操作数据训练的模型表现出明显抖动。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 13, Section 6.2 Model Deployment Results
- Evidence: 定性观察：作者将抖动归因于遥操作需经中间控制器（操纵杆/动捕服）传递意图、跟踪误差与延迟累积（归因见 page 13-14 原文）；对比条件未严格对齐（见 author_stated）。
- Quote: “As shown in Fig.6, models trained on our Real- Sim-Real data exhibit smoother and more stable execution during deployment, whereas those trained on teleoperation data display noticeable jitter.”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0002

- Claim: 在真实世界三个操作任务上，将训练与评测背景从特征贫乏改为特征丰富带来的平均归一化得分增益，腕戴鱼眼相机为 +0.39，高于针孔相机的 +0.18，即鱼眼的定位收益以环境视觉复杂度为条件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 6, Figure 6
- Evidence: 正文对 Figure 6 的解读直接给出真实世界平均增益 +0.39（鱼眼）vs +0.18（针孔），并把更强的场景复杂度依赖归因于 CLIP 编码器与真实纹理对宽 FoV 的利用。
- Quote: “Crucially, Fig. 6 shows this performance gain ismore significant for the fisheye camerain the real world (average gain+0.39vs. +0.18for pinhole) than in simulation. We attribute this to the stronger CLIP [33] encoder and complex real-world tex- tures, which the fisheye’s FoV fully exploits.”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0005

- Claim: 模拟中的场景多样性扩展曲线明显较缓；作者将其归因于两点：模拟使用非预训练 ResNet-18 而真实世界使用预训练 CLIP 编码器，以及模拟背景图像的视觉复杂度相对更低。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 7, Section 4.2
- Evidence: 作者明确指出模拟扩展曲线较缓并给出两点归因，说明鱼眼场景泛化收益依赖编码器预训练与背景视觉复杂度。
- Quote: “In contrast, the scaling curve in simulation is less steep. We attribute this discrepancy to two primary differ- ences: 1) the variation in visual encoders (a non-pre-trained ResNet-18 [16] in simulation vs. the pre-trained CLIP [33] in the real world), and 2) the comparatively lower visual complexity of simulated background imagery (see Fig. 5 and the supplementary file).”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0322

- Claim: 作者的核心条件判断：在物理约束阻止机器人重新定位自身的场景中，保持全向感知（omnidirectional awareness）远比颜色或语义信息更关键。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 1, Abstract
- Evidence: 摘要第二句给出该判断；page 1 引言以“viewpoint-limited”案例重申（target objects may remain undetected by conventional RGB-D cameras, thereby limiting the effective workspace）。引言版本已核对。
- Quote: “In scenarios where physical constraints prevent the robot from repositioning itself, maintaining om- nidirectional awareness becomes far more critical than color or semantic information.”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0329

- Claim: 收益分层：对目标位于相机视野外的任务（OV），所有相机基线因感知覆盖受限基本失败（Tab. I 中全部 0/20），OmniDP 借全向 360° 感知实现大工作区操作、在保持全环境感知的同时触及周围任意位置物体；对视野内任务（如 Pick & Place），OmniDP 也超过基线（仿真 16/20 vs 14/20、真机 15/20 vs 11/20），作者归因于全景感知提供全面场景上下文利于避障与空间推理、时间感知编码通过缓解瞬态传感器噪声增强时间稳定性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 6, Section IV-A; values from page 5, Table I
- Evidence: Sec. IV-A 分析段给出 OV 基线失败归因与视野内任务的两条增益机制；具体数值见 Tab. I（page 5，已核对）。
- Quote: “For tasks where target objects are located outside the camera’s field of view (denoted OV), all baselines largely fail due to their limited perceptual coverage. In contrast, OmniDP leverages its omnidirectional 360° perception to achieve robust large-workspace manipulation, reaching ob- jects anywhere in the surroundings while maintaining full environmental awareness. For in-view tasks such as Pick & Place, OmniDP also outperforms the baselines, benefit- ing from panoramic perception that provid”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0331

- Claim: 泛化评估（在基线表现最好的视野内 Pick & Place 任务上引入三类变化）：OmniDP 在物体实例、光照、杂乱场景变体下分别保持 13/20、15/20、12/20，高于最强基线 iDP3 的 12/20、12/20、10/20，但差距仅 1-3 次成功（每变体 20 次试验）；DP 为 3/20、4/20、2/20，DP3 为 7/20、8/20、7/20；作者归因于全景场景理解提供全面空间上下文、天然较少受光照变化与局部杂乱影响。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 6, Table III and Section IV-C
- Evidence: Tab. III 逐格给出四方法 × 三变体成功率；归因句（panoramic scene understanding...inherently less affected by lighting changes or local clutter）逐字位于 page 6 Sec. IV-C（已核对）。
- Quote: “TABLE III: Generalization capability evaluation. Results demonstrate that OmniDP maintains consistently high suc- cess rates across varying object instances, lighting condi- tions, and cluttered scenes. Method Instance Lighting Scene DP 3/20 4/20 2/20 DP3 7/20 8/20 7/20 iDP3 12/20 12/20 10/20 Ours 13/20 15/20 12/20”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0342

- Claim: 方法的部署前提是训练与测试相机参数（外参+内参）均已知且表达在同一坐标系：作者认为这在实际部署中合理，因为相机标定可在系统搭建时完成一次。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 3, Section III-A, Problem Setup
- Evidence: 问题设定节明确假设：both C train and C test are known and expressed in the same coordinate frame，理由是 camera calibration can be performed once during system setup。
- Quote: “that both C train and C test are known and expressed in the same coordinate frame, which is a reasonable assumption in practical deployment scenarios where camera calibration can be performed once during system setup.”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0347

- Claim: 视角适配方法消融（LIBERO-Long，Table III）：LVSM 域适应微调后平均成功率 88.6%、PSNR 23.20 dB，接近原视角 92.4%；深度重投影（真值深度点云重投影+Telea 修补）81.1%、PSNR 18.27 dB；单应变换 31.7%、14.72 dB；无适配 49.0%、13.64 dB；未经域适应微调的 LVSM 仅 33.2%、16.54 dB——几何正确但非真实感的重投影在大视角偏移下的伪影会限制 VLA 的视觉理解。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 5, Table III
- Evidence: Table III 对比四种适配方法（无适配/单应/深度重投影/LVSM±微调）的成功率与 PSNR；正文（page 6）指出深度重投影虽几何正确但非真实感伪影限制 VLA 视觉理解，本方法维持接近原视角性能（88.6% vs 92.4%）。
- Quote: “TABLE III SUCCESS RATE (%) AND IMAGE QUALITY ON VIEWPOINT ADAPTATION ABLATION. Success Rate (%) PSNR (dB) Method Small Medium Large Average Average π 0.5 (original view) – 92.4 – π 0.5 (no adaptation) 85.6 46.8 14.6 49.0 13.64 Homography 74.6 9.6 10.8 31.7 14.72 Depth 85.2 84.6 73.4 81.1 18.27 Ours-π (w/o FT) 65.4 20.0 14.2 33.2 16.54 Ours-π 91.0 88.6 86.2 88.6 23.20”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0348

- Claim: 仿真域的"零样本"部署依赖一次 LVSM 域适应微调（在 491 场景、64 视角/场景、无动作标签的自建多视角数据上），但作者论证其成本远低于 VLA 微调：LVSM 仅 171M 参数（OpenVLA-OFT 7B、π0.5 3.3B），且只需多视角图像、无需机器人动作标签，数据采集便宜一个数量级；真机 agent 相机部署则直接使用 RealEstate10K 原始 checkpoint（零样本）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 6, Section IV-A.4 (efficiency paragraph)
- Evidence: page 4 说明 LVSM 在自建 491 场景仿真多视角数据（LIBERO-Plus 资产替换物体/纹理）上微调以弥合域差；page 6 论证一次性微调效率（171M vs 7B/3.3B、无需动作标签），并注明真机 agent 相机用原始 LVSM。
- Quote: “While our primary approach is zero-shot adaptation with frozen policies, we note that the one-time LVSM fine-tuning for domain adaptation is significantly more efficient than VLA fine-tuning. First, LVSM is substantially smaller (171M parameters) compared to VLAs (7B for OpenVLA-OFT, 3.3B for π 0.5 ), requiring less computational resources. More importantly, LVSM fine-tuning only requires multi-view im- ages without any robot action labels, making data collection orders of magnitude easier and c”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0350

- Claim: 在额外的手持相机实验中，三台不同相机（ZED2 立体相机、Intel RealSense D435、iPhone 17 Pro）被手持并在策略执行中自由移动，位姿由工作台上的 ArUco 标记估计；作者称该方法可实时成功运行，泛化到相机外参变化之外的内参与跨相机型号图像特性变化——但该实验仅提供补充视频中的定性结果，无成功率数字。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 7, Section IV-B.3
- Evidence: IV-B.3 节描述手持实验设置（三相机、ArUco 位姿估计）与泛化声明（外参+内参+图像特性跨型号），定性结果在补充视频。
- Quote: “To further demonstrate the robustness of our method, we conduct an additional experiment where, unlike the fixed-camera setup in the previous evaluation, three different cameras (a ZED2 stereo camera, an Intel RealSense D435, and an iPhone 17 Pro) are held by hand and moved freely while the policy is being executed, as illustrated in Figure 1. The pose of each handheld camera is estimated using ArUco markers [50] attached to the work table. This experiment demonstrates that our method can succes”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0622

- Claim: 日夜分解（Table III）：C 6.47/3.46、C+T+P 6.85/4.07、C+L 22.56/19.17、C+L+T+P 23.34/18.68（日/夜）——夜间全模态（18.68）反而略低于 C+L（19.17，差 0.49），热+偏振的夜间收益只体现在纯相机配置（3.46→4.07）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 7, Table III; page 8, Section V-B-1
- Evidence: Table III 四行两列数字逐字；page 8 正文仅说按日夜评估鲁棒性，未展开讨论夜间 C+L+T+P<C+L 的细节——该 0.49 差值是读者对表格的直接算术，作者未在正文解释。
- Quote: “RESULTS ON DIFFERENT LIGHTING CONDITIONS ON PANOMMOCC. # Modality Day Night mIoU↑ VoxelHound C 6.47 3.46 C+T+P 6.85 4.07 C+L 22.56 19.17 C+L+T+P 23.34 18.68”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0632

- Claim: 作者动机定位：四足平台相比轮式平台视点低、频繁自遮挡、步态动力学引起强自运动；全景相机缓解视角受限，但仅依赖 RGB 模态在光照变化、低纹理区域与远距离感知场景下仍然脆弱——这是本文转向多模态的直接理由。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 1, Section I; page 2, Section II-B
- Evidence: 第 I 节倒数第二段逐字；相关工作中将四足占据路线定位为 camera-only（OneOcc vision-only panoramic；QuadOcc 仅 RGB），确立本文的 multimodal 增量定位。
- Quote: “Deploying panoramic occupancy perception on real robotic platforms introduces significant challenges, particularly for quadruped robots. Compared with wheeled platforms (Fig. 1a), quadruped platforms (Fig. 1b) have low sensor viewpoints, fre- quent self-occlusions, and strong ego-motion induced by gait dynamics [10], [24]. Although panoramic cameras mitigate view limitations, relying solely on the RGB modality remains fragile under illumination variations, low-texture regions, and long-range per”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0715

- Claim: 户外 KITTI360 上收益高度依赖真实鱼眼标注：无鱼眼标注的 SSL/SL 仅把 MapAnything 位姿 AUC 从 0.428 提至 0.540/0.538（深度 δ1 0.607→0.809/0.814），而含真实鱼眼数据的 SL+ 达 0.917/0.922——纯合成畸变训练不足以完全弥合真实户外鱼眼域差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 9, Table 1
- Evidence: Table 1 显示 KITTI360 上 SSL 与 SL 几乎无差别且远低于 SL+，而室内数据集（ScanNet++/ADT）上 SSL 已接近全监督；说明合成畸变的域覆盖在户外不足，SL+ 的训练集中含 ASE+KITTI360 真实鱼眼数据。
- Quote: “MapAnything [20] 0.818 0.947 0.428 1.215 3.023 20.568 0.258 5.775 0.607 1.097 1.505 1.301 18.034 6.642 0.259 w/ SSL 0.906 0.989 0.540 0.707 2.152 15.528 0.156 4.294 0.809 0.933 1.098 1.015 15.739 6.025 0.291 w/ SL 0.906 0.982 0.538 0.682 2.141 15.342 0.153 4.458 0.814 0.938 1.094 1.016 15.750 5.998 0.295 w/ SL+ 1.000 0.992 0.917 0.152 0.350 1.565 0.091 3.282 0.922 0.549 0.601 0.575 2.963 1.938 0.805”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0912

- Claim: backbone 规模边界（Table 6）：ViT-S 上 RePer-360（Abs Rel 0.0875 / RMSE 0.4073，M3D）对 PanDA-S（0.0884 / 0.4160）增益收窄；ViT-B 上 M3D Abs Rel 0.0799 反而略差于 PanDA-B 的 0.0773（但 RMSE 0.3577 更优、S2D3D 两指标均更优）；作者归因：小 backbone 特征提取能力弱，限制 CP 引导信号的质量——增益随 backbone 能力增强而更明显。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 22, Table 6 (Supplementary B.2)
- Evidence: Table 6 跨 backbone 对比：ViT-S/ViT-B 两档 PanDA 与 RePer-360 的 M3D/S2D3D 数值；正文给出能力-增益相关性解释。
- Quote: “PanDA-S [6] ViT-S 0.0884 0.4160 0.0865 0.3219 RePer-360 (Ours) ViT-S 0.0875 0.4073 0.0801 0.3130 PanDA-B [6] ViT-B 0.0773 0.3710 0.0796 0.3013 RePer-360 (Ours) ViT-B 0.0799 0.3577 0.0672 0.2752”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0913

- Claim: 与多视角流水线 ST²360D 的零样本对比是条件性的：其小变体单帧 5.9 s 对 PanDA-Small 0.06 s（约 98× 开销）；VDA-Large 变体报告 M3D 0.1153 Abs Rel / 0.4284 RMSE、S2D3D 0.1005 / 0.2986，而 RePer-360 为 0.1033 / 0.4534 与 0.0630 / 0.2849——RePer 在 S2D3D 更优、M3D 上 Abs Rel 更低，但 ST²360D 的 M3D RMSE 更低。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 23, Section B.3 (comparison with ST²360D)
- Evidence: 补充材料 B.3 引用 ST²360D 报告数字（未公开实现）与本方法数字的逐项对比，并给出算力开销对比。
- Quote: “also improves zero-shot depth estimation through a multi-view pipeline, but with higher runtime. Under the reported single-A40 setting, its small variant requires 5.9 s, compared with 0.06 s for PanDA-Small, corresponding to an approximately 98× overhead. Since larger variants are generally not faster than smaller ones, this suggests the high computational cost of multi-view inference. As ST 2 360D is not publicly available and reports only zero-shot results, we cite its reported numbers. Using”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0943

- Claim: 跨域泛化（透视 AGD20K）：Seen Split 上 Ours 0.739/0.616/1.750 与 OOAL 0.740/0.577/1.745 基本持平（KLD 略好、SIM/NSS 更好）；Unseen Split 上 Ours 1.185/0.475/1.419 vs OOAL 1.070/0.461/1.503——SIM 略好但 KLD 与 NSS 劣于 OOAL。两个分裂上均优于弱监督基线 LOCATE/WSMA/LoopTrans 的对应值（如 Seen KLD 1.226/1.176/1.088 vs 0.739）。全景化设计迁移到透视域时呈『分布更平滑』的交换：部分点敏感指标受损。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 6, Table I (b) and Section V-B
- Evidence: Table I(b) 全量数值：弱监督三基线 + 两个 one-shot 方法在 Seen/Unseen 的三元组指标。
- Quote: “(b) Generalization Results on the Perspective AGD20K Dataset Method Supervision Seen Split Unseen Split KLD↓ SIM↑ NSS↑ KLD↓ SIM↑ NSS↑ LOCATE [7] Weakly 1.226 0.401 1.177 1.405 0.372 1.157 WSMA [18] Weakly 1.176 0.416 1.247 1.335 0.382 1.220 LoopTrans [36] Weakly 1.088 0.445 1.322 1.247 0.403 1.315 OS-AGDO [35] One-shot 1.320 0.390 1.021 1.398 0.382 1.174 OOAL [9] One-shot 0.740 0.577 1.745 1.070 0.461 1.503 Ours One-shot 0.739 0.616 1.750 1.185 0.475 1.419”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0946

- Claim: 超参边界（LoRA rank r，Table IV）：性能随 r 增大呈近似倒 U 型——低秩（r=4, 8）表征容量不足以捕获 ERP 投影引入的复杂非线性几何畸变，跨域对齐次优；过高秩（r≥24）出现明显性能退化（r=32 时 KLD 升至 1.403），提示过参数化可能在稀缺 one-shot 样本上过拟合或破坏预训练 DINOv2 的鲁棒语义先验；r=16 取得适配灵活性与语义保存的最优平衡（1.306/0.474/4.398），为作者默认配置。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 7, Table IV and Section V-E (Impact of LoRA Adaptation Rank)
- Evidence: 第 V-E 节 Impact of LoRA Adaptation Rank 段：倒 U 趋势、低/高秩失效归因、r=16 最优。
- Quote: “Impact of LoRA Adaptation Rank r. As shown in Table IV , model performance exhibits an approximately inverted-U trend as r increases. When the rank is low (r = 4, 8), the representation capacity is insufficient to capture the complex nonlinear geometric distortions introduced by ERP projection, leading to suboptimal cross-domain alignment. Conversely, excessively high ranks (r ≥ 24) result in notice- able performance degradation (e.g., KLD rises to 1.403 at r = 32). This suggests that over-param”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-1136

- Claim: 作者指出：感知扩展到全向 3D 建图后，更密集的语义地图、更多候选对象与更多长程空间关系若被直接文本化供 LLM 规划，会迅速导致 token 爆炸——穷举对象列表或稠密地图描述会超出 prompt 预算、降低推理稳定性并增加推理延迟。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 2, I Introduction
- Evidence: 引言第二挑战：更丰富的观测改善全局态势感知的同时产生更密集语义地图/更多候选对象/长程关系，直接文本化会 token 爆炸、超出 prompt 预算、降低推理稳定性、增加推理延迟。
- Quote: “semantic maps, more candidate objects, and more long-range spatial relations that must be reasoned over during naviga- tion. Directly verbalizing such information for LLM-based planning quickly leads to a token explosion problem, where exhaustive object lists or dense semantic map descriptions exceed the prompt budget, reduce reasoning stability, and increase inference latency [3], [6].”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-0126

- Claim: 递归视觉路由（RVR）的增益集中在困难样本：Hard 子集 cIoU +12.30、gIoU +5.03，而 Normal 子集仅 cIoU +4.50、gIoU +0.78——递归放大主要解决全景中的亚尺度目标定位，对常规尺度目标增益有限。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 11, Table 6; Section 5.3 Impact of Recursive Visual Routing
- Evidence: Table 6 按 All/Hard/Normal 分块对比递归路由与单步网格路由，显示增益几乎全部来自 Hard 子集，界定了该机制的实际适用条件。
- Quote: “the performance gains are significantly more pronounced on the “Hard” subset, where cIoU and gIoU surge by 12.30% and 5.03%, respectively, compared to the modest increases of 4.50% and 0.78% on the “Normal” subset.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0132

- Claim: PAP 性能随 VLM 骨干能力提升而提升：Gemini-3-Flash 达 74.03 gIoU（超默认 Qwen3-VL-32B 的 72.69），更小的 Qwen3-VL-8B/4B 与 Qwen2.5-VL-7B 分别降至 68.93/66.28/65.47——免训练管线的上限受 VLM 推理能力约束，作者将其表述为灵活性（可换闭源模型做离线数据生成、换轻量模型平衡推理成本）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 18, Table 10; Section A.2 Analysis of Different VLM backbones
- Evidence: Table 10 覆盖 5 个 VLM 骨干，显示性能与骨干能力强正相关，并支撑作者"离线数据生成引擎 vs 轻量在线推理"的双用途定位。
- Quote: “Gemini-3-Flash 74.03 67.65 77.74 67.20 2 Qwen-3-VL-32B72.69 63.85 76.29 66.13 3 Qwen-3-VL-8B 68.93 55.57 72.43 62.34 4 Qwen-3-VL-4B 66.28 52.79 70.15 59.94 5 Qwen-2.5-VL-7B 65.47 52.12 68.08 57.35”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0133

- Claim: 在粗到细路由范式下，向 VLM 输入 2000×1000 的降采样全景已足够：4000×2000 仅带来边际 gIoU 提升（73.32 vs 72.69）且 cIoU 反降（58.98 vs 63.85），同时图像 token 数与推理延迟翻倍；1000×500 则掉至 66.46 gIoU。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 18, Table 11; Section A.3 Analysis of Different Resolution (page 19)
- Evidence: Table 11 的三档分辨率对比显示收益递减与延迟代价，说明该范式的分辨率需求由路由结构而非传感器原始分辨率决定。
- Quote: “4000×200073.3258.9876.81 67.30 2 2000×1000 72.69 63.85 76.29 66.13 3 1000×500 66.46 56.45 70.78 59.18”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0089

- Claim: 在长时序任务（顺序完成滑门开启、柜内取杯、放置到碟；340 条 UMI-3D 演示、40 trials）上，门开阶段成功率达 97.5%（表明策略可可靠学习铰接物体交互），但错误沿阶段累积：杯抓取成功率 47.5%，最终放置仅 5.0%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 14, Section V-C, Performance and Failure Propagation (Fig. 13)
- Evidence: Fig. 13 的 Sankey 图展示失败传播：门开 97.5%、杯抓取 47.5%、放置 5.0%。作者在 Discussion 中指出多阶段任务还需数据分布、机器人具身与控制可行性之间的一致性。
- Quote: “As shown in Fig. 13, the door opening stage achieves a high success rate of 97.5%, indicating that the policy reliably learns articulated object interaction. However, performance decreases in subsequent stages, with cup grasping success at 47.5% and final placement success at only 5.0%.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0285

- Claim: 该论文的“相机视角扩展”使用常规透视 RGB 相机（单个前视 Cam_F，另四个相机仅绕工作区中心向左/右/上/下各旋转 15° 得到 Cam_F_L、Cam_F_R、Cam_F_U、Cam_F_D），采集时同步录制、推理默认只用前视 Cam_F——即通过多台窄视角常规相机获得视角多样性，而非鱼眼/全景/超广角光学。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 4, Section IV-A, c) Camera Views
- Evidence: 实验设置 c) Camera Views 明确给出相机布置：默认前视相机加 15° 旋转得到的四个附加视角；全文未出现鱼眼、全景或超广角相机。该卡用于固定本文证据的传感边界。
- Quote: “c) Camera Views: Unless otherwise specified, we consider a camera with its perspective view directed to the front of the robot arm, denoted as Cam F . We ro- tate the camera around the workspace center by 15 ◦ towards the left, right, upper, and down sides sepa- rately, deriving four additional camera views denoted as Cam F L , Cam F R , Cam F U , Cam F D respectively. All these cameras will record the expert demonstration for imitation learning policy training. During inference, unless otherwis”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-0293

- Claim: 真机实验受硬件限制只有两个相机视角（左视/右视），作者自述两视角训练带来的性能增益不显著；但推理期多视角聚合仍能在真机上提升单视角推理性能（Tab. VI：N=25 时单视角 0.45、双视角训练 0.50、双视角训练+聚合 0.75；N=50 时 0.70/0.85/0.85）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 6-7, Section IV-B Q6 and Table VI
- Evidence: Q6 段给出真机设置（FANUC CRX-10iA 倒水任务、50 条演示、双固定相机）与结果解读：双视角联合训练略优但 gain not very significant，多视角聚合则验证了 Alg. 1 的有效性；Tab. VI 给出三个数值行。
- Quote: “However, due to hardware limitations, we only have two camera views in total. As a result, the performance gain from two-view training is not very significant. Afterwards, we further study whether multiview composition in the inference stage can better improve the visual policy performance. The results are also revealed in Tab. VI. Multiview composition can help improve model performance over single-view inference, which verifies the effectiveness of our algorithm in Alg. 1 in the real-world set”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-0294

- Claim: 作者在结论中明确限定：该框架聚焦固定场景内的视角多样性，未来工作才探索把视角扩展与环境随机化、跨具身数据或大规模基础模型结合以进一步增强泛化——即视角多样性不等于环境/场景多样性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 6, Section V Conclusion
- Evidence: 结论段的范围声明：While our framework focuses on viewpoint diversity within a fixed scene, future work may explore combining view scaling with environment randomization, cross-embodiment data, or large-scale foundation models。
- Quote: “While our framework focuses on viewpoint diversity within a fixed scene, future work may explore combining view scaling with environment randomization, cross-embodiment data, or large-scale foundation models to further enhance generaliza- tion.”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-1050

- Claim: 在公共重建基准上结果互有胜负而非全面领先：DTU 上 Overall 3.0251 略优于 Pi3 的 3.0785（但 Acc. 3.3049/Comp. 2.2424 均劣于 Pi3 的 3.0213/2.1322）；ETH3D 上 Overall 0.1841 劣于 Pi3 的 0.1672（Acc. 0.1132 优、Comp. 0.1240 劣）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 7, Table 2（Section 3.2）
- Evidence: Table 2 报告 DTU/ETH3D 上与 Dust3R/MASt3R/Spann3R/VGGT/Pi3 的对比，本方法与 Pi3 各有胜负。
- Quote: “Pi3 [13] 3.0213 2.1322 3.0785 0.1341 0.1169 0.1672 Ours 3.3049 2.2424 3.0251 0.1132 0.1240 0.1841”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1056

- Claim: 跨数据集泛化的条件性：在 DL3DV-Benchmarks 上本方法 PSNR 20.13 与 LPIPS 0.318 均最佳（DepthSplat 19.24/0.322）；在 RealEstate10K 上 SSIM 0.896 最佳但 PSNR 27.43 略低于 DepthSplat 的 27.47，作者自述“其余指标保持有竞争力”。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 8, Table 4 与 Section 3.3 跨数据集段（best SSIM 表述延续至 page 9 首段）
- Evidence: Table 4 报告 DL3DV 与 RealEstate10K 上的 PSNR/SSIM/LPIPS 对比；正文明确承认 RealEstate10K 上 PSNR 非最佳。
- Quote: “DepthSplat [34] 19.24 0.620 0.322 27.47 0.889 0.114 Ours 20.13 0.616 0.318 27.43 0.896 0.109 3.3 Generalized Novel View Synthesis Datasets. We evaluate generalized novel view synthe- sis on both our proposed surround-view robotic dataset and two public benchmarks, DL3DV-Benchmarks [58] and RealEstate10K [59]. Our proposed dataset is designed for sparse-view robotic perception with large viewpoint changes and limited overlap across input cameras, making view synthesis substantially more challengi”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1177

- Claim: ScanNet++ 数据集（test view）六场景平均：DirectFisheye-GS SSIM 0.8972/PSNR 28.3683/LPIPS 0.1863，与 3DGUT（SSIM 0.9042/PSNR 28.4178/LPIPS 0.2563）相比 SSIM/PSNR 略低但 LPIPS 明显更优（低 0.070），同时超过 Fisheye-GS**（0.8970/27.8600/0.1950）与 3DGS*（0.8651/25.8754/0.2223）——常规室内场景上与 SOTA 互有胜负而非全面领先。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 8, Table 2
- Evidence: Table 2（test view）平均行：3DGUT 0.9042/28.4178/0.2563、Self-Cali-GS 0.8251/23.2996/0.2442、Ours 0.8972/28.3683/0.1863；Fisheye-GS** 0.8970/27.8600/0.1950 与 3DGS* 0.8651/25.8754/0.2223 出自同表（已核对）；LPIPS 差距 0.2563-0.1863=0.070。
- Quote: “3DGUT 0.9300 29.7930 0.2290 0.9010 25.7450 0.2520 0.9340 30.4110 0.2470 0.8650 27.4000 0.2630 0.9510 32.2130 0.2570 0.8440 24.9450 0.2900 0.9042 28.4178 0.2563 Self-Cali-GS 0.8549 22.7834 0.1985 0.8422 21.1700 0.2316 0.8747 25.6795 0.2055 0.7259 21.9833 0.3383 0.9081 28.1148 0.1481 0.7447 20.0664 0.3431 0.8251 23.2996 0.2442 Ours 0.9191 28.7369 0.1511 0.8984 25.9518 0.1715 0.9296 30.6031 0.1783 0.8499 27.1832 0.2127 0.9473 32.7372 0.1849 0.8390 24.9978 0.2194 0.8972 28.3683 0.1863”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1178

- Claim: 作者对比分析：在与 3DGUT 相同的六个 ScanNet++ 场景上，两个紧凑高反射室内场景（ID 0a5c013435、d415cc449b）3DGUT 略优于本方法——与其光线追踪式建模对局部光照与镜面效应更鲁棒一致（且非本文重点）；其余场景与数据集上本方法一致取得更高重建质量。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 13, Appendix Section D
- Evidence: 附录 D：3DGUT 是性能最接近的方法；两反射场景略优归因于 ray-based formulation 对局部光照/镜面更鲁棒且'is not the primary focus of this work'；其余场景/数据集本方法一致更高；同节还分析 3DGUT 的七 sigma 点 UT 采样在强畸变边界产生马赛克伪影（Fig. 5/8/9 与视频）。
- Quote: “On two compact and highly reflective indoor scenes (IDs: 0a5c013435 and d415cc449b), 3DGUT slightly out- performs our method, which is consistent with its ray-based formulation that is more robust to localized lighting and specular effects and is not the primary focus of this work. In the other scenes and datasets, however, our method con- sistently achieves higher reconstruction quality.”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1280

- Claim: 跨论文评测张力（360DVO 在 UAV 语境的相对表现）：本文化用 UAV 数据集评测 360DVO，承认其仅用单目里程计即取得较高精度与鲁棒性（100% 成功），但在部分序列上劣于 OpenVSLAM——与 360DVO 原文（arXiv:2601.02309）自报在其基准上全面超越 OpenVSLAM 形成评测语境对照。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 6, Section V-B and Table IV
- Evidence: V-B-1 对 360DVO 的定性评价 + Table IV 中 360DVO 行（avg 1.398）与 OpenVSLAM 行（多序列更低 ATE 但有失败）。
- Quote: “360DVO achieves relatively high accuracy and ro- bustness even with only monocular odometry. However, it still underperforms compared to OpenVSLAM on some se- quences.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-0271

- Claim: 视场三方对照（RoboTwin，π0.5）：把标准'主视图+腕视图'换成窄视场腕装透视相机使成功率暴跌至 13.1%；换成 UMI 式广角鱼眼恢复部分丢失的上下文（59.4%），但仍明显低于标准视图（82.0%）——广角鱼眼信息量优于窄视场腕相机，但策略仍须依赖带径向畸变的局部 gripper-centric 视图而非全局组织的主视图。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 12, Section 4.1 Diagnostic Validation
- Evidence: Section 4.1 第一个诊断实验：RoboTwin 上把标准观测换成 wrist-only 透视相机使 π0.5 掉到 13.1%（窄视场上下文不足）；扩展为 UMI 式广角鱼眼恢复部分上下文但仍留差距（Table 1：RoboTwin 腕装鱼眼 59.4 vs 标准 82.0）。
- Quote: “On RoboTwin (Chen et al., 2025), replacing the standard main-view-plus-wrist observation setup with wrist-only perspective cameras causes a severe drop in π 0.5 success rate to 13.1%, indicating that narrow-FOV wrist views alone provide insufficient scene context. Expanding the wrist cameras to UMI-style wide-angle fisheye observations recovers part of this lost context, but still leaves a clear gap to the standard-view setting, as shown in Table 1. This suggests that UMI-style wrist-fisheye obs”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0273

- Claim: 透视→鱼眼数据合成的边界条件：当目标鱼眼 FoV 超出原始图像可见范围（≈180° 对角 FoV 镜头正是如此），经典几何 warp（纯像素重映射）不可避免产生拉伸边界、非自然外推或周边内容缺失，因为几何变换无法合成原始视锥之外的可信场景结构；作者改用扩散图像编辑模型 FLUX.2-dev 做语义感知的图像到图像翻译——不仅施加几何畸变，还以全局场景语义为条件幻觉出物理可信的周边内容，得到带自然压缩边缘的鱼眼风格视图。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 7, Section 3.2 UMI-VQA for Perception Alignment
- Evidence: Section 3.2 论证 RefSpatial 透视图像必须带入鱼眼域时，经典多项式畸变 warp 的失效机理（视锥外内容无法几何合成），以及 FLUX.2-dev 语义感知翻译的替代方案与'更接近真实鱼眼镜头光学特性'的主张。
- Quote: “produces stretched boundaries, unnatural extrapolation, or missing content in the periphery, because geometric transforms cannot synthesize plausible scene structure beyond the original viewing frustum. In contrast, we employ a diffusion-based image-editing model (i.e., FLUX.2-dev (Labs, 2025)) to perform semantic-aware image-to-image translation. The model not only applies geometric distortion but also hallucinates physically plausible peripheral content conditioned on global scene semantics, y”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0276

- Claim: 轨迹可执行性是本体条件化的：同一批在 RealMan 上低分的数据在 R1Pro 上获得更高分数并可成功部署——RealMan 低分子集策略在 R1Pro 上 OSR 0.80、PSR 1.00（在 RealMan/AC one 上 OSR 0.00），支持按目标本体条件化过滤：同一 UMI 数据对一台机器人危险、对另一台合适。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 17, Table 5
- Evidence: Fig. 7 显示同一子集在三本体上分数分布不同；Table 5 报告跨本体部署：低分子集策略在 RealMan/ACone 上 OSR 0.00/0.00，在 R1Pro 上 GSR 0.80、OSR 0.80、PSR 1.00；正文据此支持 embodiment-conditioned filtering。
- Quote: “Training Data #Demos RealMan ACone R1Pro GSR OSR PSR GSR OSR PSR GSR OSR PSR Low-score subset 50 0.55 0.00 0.00 0.60 0.00 0.00 0.80 0.80 1.00 High-score subset 50 0.65 0.65 1.00 0.60 0.55 0.92 0.75 0.75 1.00”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0281

- Claim: 仿真基准的'腕装鱼眼'数据是合成畸变而非真实鱼眼镜头：RoboTwin 用垂直 FoV 150° 的宽角腕相机（渲染分辨率 680×680）采集后，在 HDF5→LeRobot 转换时对每帧施加固定重映射网格的鱼眼风格变换（fisheye strength s=1.8，源半径 ρ_src=tan(ρ·arctan(s))/s，单位圆外像素填黑边），再缩放到 224×224；LIBERO 保留单腕相机（700×700）共享同一畸变参数。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 31, Appendix D, Implementation Details
- Evidence: Appendix D 说明仿真腕装鱼眼数据生成两段式流水线：宽角相机采集（150° vFoV）+ 转换期固定 remap 网格鱼眼化（s=1.8、双线性插值、黑边填充）；这是理解 Table 6 仿真结果光学保真度的关键边界条件。
- Quote: “For RoboTwin, we first collect demonstrations using wide-angle wrist cameras whose vertical field of view is 150 ◦ and whose rendered resolution is 680 × 680.”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0505

- Claim: 对时序敏感任务，BifrostUMI 沿用 UMI 的延迟匹配流程，校准并补偿腕视图观测、夹爪状态测量、高层策略推理与机器人控制之间的相对延迟——鱼眼腕视图要支撑定时敏感行为需显式时序校准。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 3, Section III.A, Latency matching
- Evidence: Sec. III.A Latency matching 段声明遵循 UMI [9] 的延迟匹配程序校准四路延迟；与 C10 消融（移除后动态投掷退化）互证。
- Quote: “For timing-sensitive tasks, we follow the latency-matching procedure of UMI [9] to calibrate and compensate for the relative delays among wrist-view observations, gripper-state measurements, high-level policy inference, and robot control.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0804

- Claim: UniK3D（显式相机通用设计）在中等鱼眼区间（120-140°）达到最高精度并超过其他受测单目模型，是'宽而非极端 FOV'应用的最可靠单目选择；但在极端 FOV（≥165°）且无内参的 camera-free 模式下仍退化——相机通用设计部分缓解但不能消除极端鱼眼的单目深度退化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 6, Section V-A
- Evidence: V-A 原文：UniK3D explicitly designed to be camera-universal、highest accuracy at moderate fisheye ranges (120–140°)、surpasses other tested monocular models in this regime、decline at extreme FoVs (≥165°) in camera-free mode without intrinsics。
- Quote: “Since UniK3D was explicitly designed to be camera-universal, it achieves its highest accuracy at moderate fisheye ranges (120–140 ◦ ) and surpasses other tested monocular models in this regime. This makes it the most reliable choice for applications targeting wide yet not extreme FOVs. However, even this model shows decline at extreme FoVs (≥ 165 ◦ ) when operated in camera-free mode without intrinsics.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0805

- Claim: 深度补全模型受宽 FOV 影响明显小于单目模型：FOV 120→195° 下 NLSPN AbsRel 仅 +5.92%、CompletionFormer +6.73%（两者 MAE/RMSE 部分指标反而改善），轻量 CostDCNet +38.5%——但所有补全模型在 AbsRel 这一关键指标上仍显著退化，注意力机制的大模型相对更能解读宽视角场景。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 6, Table III + Section V-A
- Evidence: Table III 补全三行与单目五行的百分比对照；V-A 原文：depth completion models are less affected by wide angles but still show significant declines in the AbsRel metric；归因于复杂模型（注意力+高容量）更善于解读宽视角。
- Quote: “In summary, even robust, large-scale models like Depth Anything V2-Large degrade in performance on fisheye im- ages as FOV increases. As expected, depth completion mod- els are less affected by wide angles but still show significant declines in the AbsRel metric, one of the most important indicators, even among high-performing SOTA models with attention mechanisms.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-1087

- Claim: 提示工程与朴素微调的边界（条件性）：H*Bench 上通用 Qwen3.5 直接 ERP 推理仅 19.4 overall，文本提示提升到 38.5、视觉提示 40.4——显式坐标指令有帮助但不能解决 pano-native 推理；对 H*Bench 做朴素 ERP 微调反而更差（17.8），说明底座模型缺乏全景空间先验时目标任务监督本身不足；相比之下 pano-native 模型零样本 56.10、H* 微调后 70.00——pano-native 学习提供了从提示工程或朴素任务监督不可恢复的可迁移空间初始化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 8, Section 4.2 H*Bench 段（Table 3(b) 同页）
- Evidence: Section 4.2 H*Bench 段报告 prompt-only 变体、naive SFT 与 pano-native 模型的三路对比及结论句。
- Quote: “Table 3(b) shows that direct ERP inference with a generic Qwen3.5 model reaches only 19.4 over- all, and prompt engineering improves it to 38.5– 40.4, suggesting that explicit coordinate instruc- tions help but do not solve pano-native reasoning. Naive H ∗ Bench fine-tuning with ERP input per- forms even worse (17.8 overall), indicating that target-task supervision alone is insufficient when the base model lacks panoramic spatial priors. In contrast, our model reaches 56.10 zero-shot and 70.00 a”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-0107

- Claim: 增广旋转范围消融（50 条 RoboMimic square 鱼眼 eye-in-hand 演示、每条生成 20 个增广 episodes、旋转界 {20°,30°,40°,50°,60°}）：更大的旋转界在视角覆盖有限时会损害渲染质量，成功率在 50° 处饱和，作者据此在所有其他实验采用 50°。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 8, Section 4.3 (Fig. A1 on page 13)
- Evidence: 该权衡由 3DGS 的视角分布外渲染退化决定：作者在轨迹优化中用 Lrender 损失把生成位姿约束在原演示/扫描视角分布附近（page 5），消融确认 50° 是质量-多样性平衡点。
- Quote: “While larger rotation bounds increase diversity, they can harm rendering quality under limited viewpoint coverage. To quantify this trade-off, we trained visuomotor policies on 50 RoboMimic “square” export demonstrations (fisheye, eye-in-hand), augmenting each with rotation bounds of {20◦, 30◦, 40◦, 50◦, 60◦}, generating 20 augmented episodessamples per demo. We then evaluated on a held-outout test set shown in Fig 5. As shown in Fig A1, success rates plateaued at 50◦, which we therefore adopt f”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0436

- Claim: 上下文内系统辨识能力不能从标准模仿训练中自发获得：未经上下文监督训练的 BC 策略，在同样前置交互 token 的条件下成功率塌缩到近零（<1%）（结论句跨页接续于 page 8：该能力必须在训练期显式激励，而非从模仿学习中自然涌现）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 7, Section 6.1
- Evidence: 6.1 节第二问的受控检查：无上下文监督的 BC + 同样交互前缀 → 近零；显式激励必要性结论在 page 8 首段。
- Quote: “Is in-context capability an emergent property of specialized training? To determine whether in-context adaptation arises from standard sequence modeling, we evaluate a BC policy trained without in-context supervision under the same interaction context. Performance collapses to near-zero (< 1%) when interaction”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0437

- Claim: 语义扰动的增益明显温和于视角增益：干扰物场景 35.0 vs 27.5（ICWM vs MV）、新桌面纹理 41.2 vs 37.5；作者把更温和的增益归因于当前数据集中场景-配置多样性稀缺，而非机制本身的根本限制。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 8, Section 6.3
- Evidence: 6.3 节语义扰动数值与作者自归因（数据稀缺而非机制上限）。
- Quote: “Semantic perturbations. As shown in (Fig. 8a), ICWM maintains a consistent margin over MV under both distractor objects (35.0 vs. 27.5) and novel table textures (41.2 vs. 37.5). The more moderate gains relative to viewpoint generalization likely reflect the scarcity of diverse scene-configuration data in current datasets rather than a fundamental limitation of the mechanism.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0441

- Claim: 真机感知配置为 12 相机环视阵列：相机布设在变化的高度与方位角上，『确保工作空间全覆盖的同时引入显著透视诱导的空间畸变』；12 相机被划分为 6 训练 / 6 保留测试，强制成功依赖功能系统辨识而非对特定相机-机器人几何的记忆；每任务收集约 100–150 条遥操作人类示范。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 19, Section C.1
- Evidence: C.1 节感知与泛化协议描述：12 相机、变高度/方位角、6/6 划分、每任务 100–150 示范。
- Quote: “To create a challenging multi-view sensing environment, we deploy an array of 12 cameras strategically positioned at varying elevations and azimuthal angles. This setup ensures com- prehensive coverage of the workspace while introducing significant perspective-induced spatial distortions. Generalization Protocol and Data Collection. To rigorously evaluate zero-shot adaptation, we partition the 12-camera system into two distinct subsets: 6 cameras are designated for training, while the remaining”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0644

- Claim: 立体骨干消融（固定占据头与 2D-to-3D 提升管线，仅换立体骨干）：测试集上 LStereo-L 取最高 IoU 35.11（FoundationStereo 29.67），但 mIoU 仅 8.09 vs FDS 11.69；真实世界 FDS 35.45 IoU / 19.26 mIoU 大幅领先 LStereo-L 33.66 / 9.78——占据质量对立体深度可靠性高度敏感，作者据此选 FoundationStereo 为默认骨干。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 9, Table 3 Ablation Study on Stereo module; page 8, Section 5.4
- Evidence: Table 3 全部十行（5 骨干×test/real）逐字；page 8 Section 5.4 的解释句（occupancy quality is highly sensitive to stereo depth reliability / a stronger stereo model can significantly enhance semantic completeness and real-world generalization）在 C09 的 summary 与 relation 中转述（已核对，见 page 8 原文）。
- Quote: “Test Set LStereo-S Guo et al. (2025a) 33.46 6.55 39.33 6.06 0.00 6.31 12.37 3.40 6.44 0.21 5.37 0.14 1.64 3.87 0.00 LStereo-L Guo et al. (2025a) 35.11 8.09 42.73 6.62 0.08 7.26 15.21 4.49 9.25 0.03 6.51 0.88 8.54 3.57 0.00 COEX Bangunharcana et al. (2021) 31.17 5.20 43.24 2.49 0.01 5.14 7.40 0.54 1.88 0.02 3.46 0.31 0.57 2.51 0.00 IGEV Xu et al. (2023a) 27.59 5.59 36.01 2.98 0.02 6.56 10.88 2.52 0.47 0.07 2.97 0.09 6.58 3.57 0.00 FDS Wen et al. (2025) 29.67 11.69 50.85 4.50 12.97 5.17 6.95 9.57”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0676

- Claim: 作者指出：已有研究（PanoEnv）表明 ERP 图像的几何畸变对现成 VLM 仍是挑战；OneCanvas 的应对是投影特征而非原始像素——把 lift-then-project 原则（BEV 方法的既有范式）迁移到 VLM 3D 场景理解，畸变被投影几何吸收而不强加给 VLM 的感知；画布原点可自由选择以同时支持场景中心与位姿中心的情境推理。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 4, Section 2, Unified scene representations
- Evidence: 相关工作段：PanoEnv 证明 ERP 畸变对 off-the-shelf VLMs 是挑战；BEV 的 unproject-then-reproject 范式被迁移；we project features rather than raw pixels 使畸变被投影几何吸收。
- Quote: “Our work brings this principle to VLM-based 3D scene understanding: per-view features are lifted with metric depth and camera poses, projected once onto a panoramic canvas, and consumed directly by the VLM, with the canvas origin chosen freely to support both scene-centered and pose-centered situated reasoning. Because we project features rather than raw pixels, the distortion that PanoEnv documents is absorbed by the projection geometry rather than forced onto the VLM’s perception.”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-1408

- Claim: 针孔基准上的精度代价（宽 FoV 统一表示的反向证据）：EuRoC 平均 ATE 0.1072 m——胜 VINS-Fusion 48.3% 但落后 SchurVINS（Table I：SchurVINS 0.0779、ORB-SLAM3 0.0400、MAVIS 0.0475）；作者归因：球面 bearing 残差面向宽 FoV 多相机而非针孔场景最优。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 5-6, Section IV-B and Table I
- Evidence: IV-B 段落给出 0.1072 与归因；Table I（page 6）给出四基线 EuRoC 全序列数值。
- Quote: “Our filter-driven Sphere-VIO yields an average ATE RMSE of 0.1072 m on EuRoC, surpassing VINS-Fusion by 48.3% but trailing SchurVINS, as our spherical bearing residual targets wide-FOV multi-camera setups rather than pinhole scenarios optimized by conventional planar reprojection residuals.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1411

- Claim: 精度天花板对照：跨全部公共基准，MAVIS（图优化多相机）总体精度顶级——Sphere-VIO 的定位是精度-效率-通用性折衷而非精度第一；宽 FoV 收益不等于全面超越图优化多相机基线。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 5, Section IV-B
- Evidence: IV-B 开篇的跨基准总评；与 Table I-III 中 MAVIS 各项第一（EuRoC 0.0475 次于 ORB-SLAM3、TUM-VI 0.0769、HILTI 0.0980）一致。
- Quote: “Across all bench- marks, MAVIS obtain overall top-tier localization accuracy.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-0737

- Claim: 同构针孔设置下 X-Lens 的收益是条件性的：以 0.04B 参数直接预测全局尺度项，在 ETH3D 与 OmniOcc 上取得最佳 Scale AbsRel、ScanNet++V2 上具竞争力，参数比若干稠密深度指标上最强的针孔基线 DA3-Giant（1.36B）少 97.1%，速度大幅领先（两视图针孔 39 FPS、六视图 OmniOcc 26 FPS，多数大型前馈几何基线更快）；但作者承认大型几何基础模型在部分稠密深度指标上仍更强——Table 2 中 ETH3D AbsRel 0.0445 落后 MapAnything 0.0228 与 DA3-Giant 0.0113，OmniOcc AbsRel 0.0656 落后 MapAnything 0.0553，ScanNet++V2 的 AbsRel/RMSE/δ1 亦未领先（0.0549/0.1621/0.9626 vs MapAnything 0.0548/0.1542/0.9773）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 12, Table 2 and Section 5.1 Pinhole Cameras
- Evidence: 作者把该权衡明示为设计目标（解耦深度感知与完整重建以获得可实时部署的紧凑模型）；对综述的意义：紧凑异构模型不必在单相机设置全面领先，选型时应按'尺度+速度 vs 稠密精度'权衡。
- Quote: “Table 2. Multi-view pinhole evaluation on ETH3D [59], ScanNet++V2 [88], and OmniOcc six-view dataset. The best result on each dataset is highlighted in bold. A red cross indicates that the corresponding baseline does not explicitly predict a global scale term. Dataset Views Method Params Scale AbsRel ↓ AbsRel ↓ RMSE ↓ δ 1 ↑ τ 1.03 ↑ FPS ↑ ETH3D [59] 2 VGGT [70] 1.26B × 0.0184 0.4073 0.9974 0.8693 15 VGGT-Omega [71] 1.14B × 0.0055 0.1465 0.9994 0.8693 12 DA3-Small [38] 0.03B × 0.0454 0.7438 0.9”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0925

- Claim: 路线权衡（裁剪 vs 适配）：Center-PH（单 110° 虚拟针孔裁剪）在深度上保持强竞争力，因为它产出接近主干预训练分布的透视图像；但它丢弃鱼眼外围内容，位姿明显更差——ScanNet++ 上 RayTun3R 把 Center-PH 的旋转误差从 3.27° 降到 1.11°、平移方向误差从 22.77° 降到 5.78°。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 8, Section 5.1 (Dense depth evaluation)
- Evidence: 第 5.1 节 Dense depth evaluation 段：裁剪路线深度优势的归因 + ScanNet++ 位姿对比数字。
- Quote: “Dense depth evaluation. For ETH3D and ScanNet++, which provide ground-truth depth, we report AbsRel and δ 1.25 in Tab. 3 (left). RayTun3R improves over the vanilla model and lightweight adaptation baselines on both datasets. Center-PH remains strong on depth because it produces perspective images close to the backbone’s pretraining distribution. However, Center-PH discards the peripheral fisheye content, yielding less accurate pose estimates: On ScanNet++, RayTun3R reduces Center-PH rotation fr”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0926

- Claim: 稠密深度（Table 3 左，DA3-Small）：ETH3D 上 RayTun3R AbsRel 0.107 / δ1.25 0.884 为全表最优（含 Center-PH 0.111/0.867、LoRA 0.166/0.814、CalTok4 0.175/0.793、Vanilla 0.178/0.751）；ScanNet++ 上 Center-PH 深度更优（0.066/0.961 vs RayTun3R 0.108/0.886），但 RayTun3R 仍明显优于 Vanilla（0.282/0.601）与两个适配基线（LoRA 0.175/0.760、CalTok4 0.168/0.769）——深度获益是数据集条件性的。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 8, Table 3 (left)
- Evidence: Table 3 左半：两数据集五方法 AbsRel/δ1.25 全量数值。
- Quote: “ETH3D ScanNet++ Method AbsRel ↓ δ 1.25 ↑ AbsRel ↓ δ 1.25 ↑ Center-PH 0.111 0.867 0.066 0.961 LoRA 0.166 0.814 0.175 0.760 CalTok4 0.175 0.793 0.168 0.769 Vanilla 0.178 0.751 0.282 0.601 RayTun3R (ours) 0.107 0.884 0.108 0.886”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0930

- Claim: 标定敏感性（Table 5，DA3-Small，每数据集一条代表序列）：用 AnyCalib 单图预测标定替换 GT 标定后，RayTun3R 误差增大但仍显著优于 LoRA/CalTok——ETH3D terrains 从 0.48/0.9/1.7（GT）到 1.02/2.3/2.6（AnyCalib），而 CalTok+AnyCalib 在 ScanNet++ 达 4.44/24.7/5.5、FIORD Kitchen 达 30.3/59.9/10.6——适配有效性以『可用相机参数（GT 或预测）』为前提条件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 13, Table 5 and Section B (Supplementary)
- Evidence: Table 5 六行（三方法 × GT/AnyCalib）+ Sec B 正文结论（remains useful under approximate camera calibration）。
- Quote: “RayTun3R (ours) (GT) 0.48 0.9 1.7 0.69 2.4 2.9 1.94 11.2 3.6 0.40 2.2 1.7 3.1 2.5 5.5 RayTun3R (ours) (AnyCalib) 1.02 2.3 2.6 1.14 2.5 3.1 1.16 7.0 4.4 0.75 4.6 3.1 4.9 3.0 5.2 LoRA (GT) 3.62 3.4 4.0 0.61 2.8 4.6 2.96 12.6 2.8 4.22 23.0 2.9 7.7 14.6 10.1 LoRA (AnyCalib) 2.30 4.7 3.2 2.32 2.8 4.8 6.60 20.4 16.6 3.52 17.5 4.9 10.2 14.2 10.8 CalTok (GT) 3.41 4.8 4.5 1.09 3.1 4.4 3.79 14.9 4.6 3.09 20.0 4.4 15.8 15.5 9.0 CalTok (AnyCalib) 2.15 4.4 3.4 1.90 8.5 5.8 7.21 42.0 38.1 4.44 24.7 5.5 30.3 5”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0306

- Claim: 四个评估任务刻意设计为任务相关区域不被局部相机同时覆盖：任务组合变化目标放置、双侧交互与空间范围——Move Pen 与 Move Block 改变目标相对机器人的方向，Open Curtain 需要与两侧顺序交互，Wipe Table 沿长桌延展操作后才归还抹布；因此需要跨视角空间推理与多阶段状态跟踪。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 4, Section III-B, Task Taxonomy
- Evidence: Task Taxonomy 段总结四任务的空间设置（Table I：Move Pen front/left/right、Move Block left/right/both sides、Open Curtain left/right、Wipe Table along a long table），并明确 task-relevant regions are not simultaneously covered by the local cameras。
- Quote: “The task suite varies target placement, bilateral interaction, and spatial extent: Move Pen and Move Block change the target direction relative to the robot, Open Curtain requires sequential interaction with both sides, and Wipe Table extends manipulation over a long table before returning the cloth. In these tasks, task- relevant regions are not simultaneously covered by the local cameras, creating a need for cross-view spatial reasoning and multi-stage state tracking.”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0311

- Claim: 在以单目标定位与短程抓放为主的 Move Pen 任务上，把 ERP 全景直接作为附加图像输入的 π0.5 w/ Pano 基线与 PanoVLA 成绩持平（Tab. II：两者 SCR/SR 均为 95.6%/86.7%）；作者解释为等距柱状全景已给 π0.5 提供足够空间信息、显式全景建模的边际收益减小——PanoVLA 的优势在需要多阶段状态跟踪与长程空间一致性的任务上才变得明显。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 7, Section V-B (Move Pen analysis; sentence starts on page 6)
- Evidence: V-B 分析段：π0.5 w/ Pano matches PanoVLA on Move Pen，因 ERP 已提供充分空间信息；The PanoVLA advantage becomes more apparent in tasks that require multistage state tracking and long-range spatial consistency。持平的具体数值见 Tab. II（page 6）。
- Quote: “The equirectangular panorama already pro- vides sufficient spatial information to π 0.5 , reducing the benefit of explicitly modeling panoramic information with panorama expert. The PanoVLA advantage becomes more apparent in tasks that require multistage state tracking - and long-range spatial consistency.”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0312

- Claim: 在需要多阶段状态跟踪的 Wipe Table 任务上，raw panorama 基线（π0.5 w/ Pano）在最后"归还抹布"阶段仅 26.7% 的试验完成，导致 SCR 74.4% 但端到端 SR 仅 20.0%；PanoVLA 该阶段完成 73.3%、SR 46.7%——差距表明全景专家在跨操作阶段跟踪任务状态转换、保持全局空间一致性（可靠重新定位抹布并归位）上更有效。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 7, Section V-B and Fig. 4
- Evidence: V-B 分析段结合 Fig. 4 的 stage-wise 曲线解释 raw panorama 基线在 Wipe Table 最后阶段的崩溃与 PanoVLA 的优势来源。
- Quote: “Although the raw panorama input baseline performs well on Move Pen, its Wipe Table profile in Fig. 4 drops at the final stage. It completes this stage in only 26.7% of trials, resulting in an SCR of 74.4% but an end-to-end SR of only 20.0%, whereas PanoVLA achieves 73.3% stage completion and 46.7% SR.”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0364

- Claim: 联合平移×旋转漂移（ε∈{100,200}cm × yaw∈{10°,20°}，Table 3）：增益保持在 [+21, +42]pp 区间；两个趋势——更大平移反而拉大 ∆（无保护基线衰减快于规范化器，差距随幅度扩大），更大旋转收窄 ∆（作者归因于训练时大旋转采样不足，可完全在数据侧解决而无需改架构）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 8, Section 4.4, Table 3
- Evidence: Section 4.4：∆ stays in the [+21, +42] pp range across all four cells；First, larger ε actually widens ∆... Second, larger θ narrows ∆, which we attribute to undersampling of large rotations at training time；Table 3 给出四格数字（最大格 ε=200cm/θ=10°：35.8→78.0，+42.2pp）。
- Quote: “So far, we mainly varied translation and kept rotation small. To check that the picture survives once translation and rotation move together, we cross ε ∈ {100, 200} cm with yaw θ ∈ {10 ◦ , 20 ◦ } in Table 3. ∆ stays in the [+21, +42] pp range across all four cells. Two trends are visible. First, larger ε actually widens ∆: the baseline drops faster than the canonicalizer, so the gap between them grows. Second, larger θ narrows ∆, which we attribute to undersampling of large rotations at trainin”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0365

- Claim: 部署标定现实性：外参位姿标定误差在约 3cm/3° 内规范化器保持稳定（三套件均值下降至多 5pp，与普通相机重装公差相当）；推到 5cm/5° 时长程 libero_10 开始受损（−23.8pp），是可吸收标定噪声的实际极限；内参（焦距）噪声远不如此致命——全程焦距扫描内 \|∆\|≤2.8pp，针孔内参误差的重要性远低于外参位姿误差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 8, Section 4.5, Table 4
- Evidence: Section 4.5：Within roughly 3 cm and 3° of calibration error, the canonicalizer remains stable, with a three-suite mean drop of at most 5 pp — comparable to ordinary camera re-mounting tolerances；Pushed to 5 cm and 5°, the long-horizon libero_10 suite begins to suffer (−23.8 pp)... practical limit；Intrinsics noise is far less damaging... \|∆\| stays within 2.8 pp（焦距 ±5%/±10% 扫描规格见 Table 15，page 20）。
- Quote: “The canonicalizer assumes that the deployment pose is known. In practice, it is only known up to calibration error, so we ask how much error is tolerated. To answer this, we inject (T cm, R ◦ ) of pose noise on top of ε=100 cm, applied only to the pose seen by the canonicalizer (Table 4). Within roughly 3 cm and 3 ◦ of calibration error, the canonicalizer remains stable, with a three-suite mean drop of at most 5 pp — comparable to ordinary camera re-mounting tolerances. Pushed to 5 cm and 5 ◦ ,”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0395

- Claim: 跨视角一致性的增益依赖动作等价配对而非通用平滑：在保持每视图流匹配标签正确的前提下，把跨视角损失中的配对应打乱（跨不同物理状态比较速度预测）后，相机轨道成功率从 84.9% 塌缩至 50.4%（K=1）、从 87.2% 塌缩至 25.8%（K=2）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 6, Section 4.3, Figure 3c, Table 2
- Evidence: shuffle 控制只破坏 L_CV 内的配对身份；匹配配方越强（双边 K=2）在错误配对下塌缩越狠，排除通用速度场平滑解释。
- Quote: “Performance collapses from 84.9% to 50.4% at K = 1, and from 87.2% to 25.8% at K = 2 (Figure 3c).”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0405

- Claim: 评估协议以腕部相机全程遮蔽为因果控制：腕部视图不随场景相机扰动而变化，允许策略使用它将引入未受扰动的视觉捷径、混淆场景相机归因；该选择隔离了场景相机归因，但使绝对成功率与保留腕部视图的标准 LIBERO-Plus 数字不可比，所有对比均在单场景 RGB 协议内进行。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 5, Section 4 (also page 12, Appendix A.2)
- Evidence: 4 节开头与 A.2 说明遮蔽动机与可比性警告；该控制与 2608.21402 的腕部遮蔽审计形成同一测量学问题的两条证据线。
- Quote: “In all experiments, the wrist-camera stream is masked during both training and evaluation: the wrist view is not subject to the scene-camera perturbation, so allowing the policy to use it would introduce an unperturbed visual shortcut that confounds the causal interpretation of scene-camera robustness.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0407

- Claim: 停止梯度（教师-学生式单向耦合）变体达到最高 ID 成功率 96.7%，但相机轨道仅 84.3%，比双边梯度配方低 2.9pp——锚定单分支是较弱的跨视角耦合形式，双边梯度与多流样本 averaging 是完整配方的必要组成。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 7, Table 2
- Evidence: Table 2 消融行给出停止梯度配置的 ID/相机数字与解读；注意该行同时改变梯度结构与流时间分布，作者声明不能单因素归因。
- Quote: “A stop-gradient teacher–student variant achieves the highest in-distribution success (96.7%) but only 84.3% on the camera track, 2.9pp below the bilateral recipe.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0417

- Claim: 保真-控制解离：在轨道轴上，闭环动作成功率跨严重度从 53% 崩溃至 3%，而相对 excess-FID 保持平坦（全部级别介于 −0.07 与 +0.16 之间）；dolly 轴上预测保真与控制共同退化。视频先验恰在控制失效最重的轴上存活（呼应他处观察到的 foresight-action 失配）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 6, Section VI-C, Figure 4
- Evidence: excess-FID 扣除同相机真值重放的 oracle 地板后衡量分布保真；作者自认其严格弱于语义计划正确性，仅作动机证据。
- Quote: “On the orbital axis, action success collapses from 53% to 3% across severity levels while relative excess-FID stays flat (between −0.07 and +0.16 across all levels). On the dolly axis, in contrast, prediction fidelity co-degrades with control. The video prior thus survives precisely on the axis where control fails hardest, echoing foresight-action misalignment observed elsewhere [9], and marking the orbital axis as the natural primary target for an action-side repair.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0419

- Claim: 收益-代价交换不对称（作者总结）：训练包络内该目标不买任何东西、还可能对近天花板对照损失几点；包络外（对照跌至 55–67% 处）它在三个轴、两个种子上回报 +4 到 +16 点。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 7, Section VII
- Evidence: VII 节结尾以不对称交换刻画方法边界，与 Table II/第二种子数字一致。
- Quote: “The exchange the objective offers is asymmetric: inside the envelope it buys nothing and can cost a few points against a near-ceiling control; beyond the envelope, where the control falls to 55–67%, it returns +4 to +16 points across three axes and two seeds.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0420

- Claim: 独立第二种子（双臂同协议重训）复现层级结构：外推 +15.50（CI [+11.70,+19.40]）、dolly +4.44（[+0.61,+8.49]）、仰角 +4.84（[+3.11,+6.58]）、分布匹配方位角区 +3.40（[+1.77,+4.93]）、ID 保持 −0.2、两个复合桶转正（+5.16/+16.36）；其插值 cell 读 −4.29（CI [−7.56,−1.22]）。跨种子看，方法臂插值成功数移动 3/490 trials（85.1%→85.7%）而对照臂移动 18（86.3%→90.0%），其中 14 个落在单一长程任务的五个插值视图上，goal 套件对照两种子均 100% 解插值 trials（方法臂 95.6%/90.0%）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 7, Section VI-D
- Evidence: 第二种子全套数字与跨种子插值移动分析显示方法臂稳定性高于对照臂，但插值结论不可下。
- Quote: “A second seed, both arms retrained under the identical protocol, reproduces the hierarchy: extrapolation +15.50 (CI [+11.70, +19.40]), dolly +4.44 ([+0.61, +8.49]), el- evation +4.84 ([+3.11, +6.58]), the distribution-matched azimuth region +3.40 ([+1.77, +4.93]), ID preservation −0.2, and both compound buckets now positive (+5.16, [+0.78, +9.69]; +16.36, [+12.73, +20.20]). Its interpola- tion cell reads −4.29 ([−7.56, −1.22]). Across seeds the method’s interpolation successes move by 3 trials i”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0422

- Claim: 分析计划在评估前固定（预注册）：主终点为方位角插值与外推桶，以配对任务 bootstrap 95% CI 比较；其余单轴桶为次级；分布内桶不携带 OOD 语言；结果按测量值报告，包括 null 结果。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 5, Section V-C
- Evidence: 预注册+null 报告与 carve-and-hold-out 协议共同构成评估契约；V-A 节另披露分布匹配契约的局限（每个被评估姿态都被训练过则无 OOD 空间）。
- Quote: “Our analysis plan was fixed before evaluation: the primary endpoints are the azimuth interpolation and extrapolation buckets, compared by paired task bootstrap with 95% confidence intervals; the remaining single-axis buckets are secondary; in-distribution buckets carry no OOD language. We report the plan’s out- come as measured, including null results.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-1108

- Claim: 低帧率部署边界：固定 2s 观测窗、输入降采样至 15/5/3/1 Hz 时 AUC 为 LSTM 0.91/0.87/0.85/0.78、MLP 0.87/0.87/0.85/0.75、RF 0.81/0.80/0.80/0.73——5Hz 与 3Hz 基本保持（LSTM 各降 4/6 个点），但 1Hz 出现明显坍塌（再降 7 个点至 0.78），作者将其定位为机载算力受限下预期系统对时间分辨率敏感性的基线。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 8, Table VI 与 Section IV-C.1
- Evidence: Section IV-C.1 Input frequency robustness 与 Table VI 报告四档子采样率下三基线 AUC（T_org=30 保持 2 秒窗）。
- Quote: “degrades as the input framerate decreases (cf. VI), with a pronounced collapse when the rate drops to a critical value of one frame per second. The results presented here serve as an additional baseline, highlighting the sensitivity of antic- ipation systems to temporal resolution under computational constraints. TABLE VI AUC OF RF AND MLP WITH DIFFERENT SUBSAMPLING RATE s. FOR ALL BASELINES WE KEEP T org = 30 (2 SEC). s / Freq. 1 / 15Hz 3 / 5Hz 5 / 3Hz 15 / 1Hz RF 0.81 0.80 0.80 0.73 MLP 0.87”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1109

- Claim: 特征消融的边际收益递减：加入姿态关键点显著提升（仅 mask 的 D1：LSTM 0.79→D3 含 ViTPose 0.91；MLP 0.81→0.87），但更细的 Sapiens-308 关键点与 242 面部关键点（D4/D5）相对 D3 无实质增益（MLP 0.88/0.88、LSTM 0.88/0.90 vs 0.91），不含框位置的 D7（MLP 0.89）与头肩耳眼手工子集 D6（LSTM 0.90）同样持平——作者结论：Sapiens 关键点与 ViTPose 结果相近 despite being much more detailed。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 8, Table VII 与 Section IV-C.2
- Evidence: Section IV-C.2 定义 D1-D7 特征集并给出 Table VII 消融；正文明确 Sapiens 与 ViTPose 结果相近。
- Quote: “The results presented in Table VII suggest that the key points provided by Sapiens yield results similar to those of ViTPose for the reference databases tested, despite being much more detailed. TABLE VII ABLATION STUDY OF FEATURE SETS FOR RF, MLP AND LSTM CLASSIFIERS. BEST RESULT FOR EACH CLASSIFIER IN BOLD. D 1 D 2 D 3 D 4 D 5 D 6 D 7 RF 0.78 0.80 0.81 0.81 0.81 0.81 0.80 MLP 0.81 0.83 0.87 0.88 0.88 0.87 0.89 LSTM 0.79 0.81 0.91 0.88 0.90 0.90 0.89”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1112

- Claim: 全景单目的距离信息缺口：系统无距离传感器输入，用分割 mask 尺寸作人到机器人距离的代理（负样本 T0 取 mask 最大时刻），补充实验以额外 RGBD 相机测量验证 mask 尺寸（全 360 图内）与距离的明显相关；框尺寸同样相关但 less stable（受位置与运动偏置，mask 尺寸除严重遮挡外稳定，而遮挡样本在采样时已被过滤）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 12, Supplementary Section XI（Fig. 13 在 page 13）
- Evidence: 补充材料 Section XI 说明 mask 尺寸作为距离代理的动机与 RGBD 验证（Fig. 13）、框尺寸的相对不稳定性与遮挡过滤。
- Quote: “We used the mask size as a proxy for distance when align- ing the negative tracks during sampling, for those tracks T 0 is define as the moment where they appear with the biggest mask size. We show in 13 the obvious correlation between mask size (in the full 360 image) and distance (measured with an additional RGBD camera), we also compare it to the box size. The box size also appears correlated to the distance but we found it to be less stable (more subject to bias depending on position and mov”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-0659

- Claim: 在逐步遮蔽输入图像的球面 FoV 鲁棒性实验中：水平 FoV 缩减时所有方法都随可用角度覆盖减少而退化；在最受限的 120° 水平 FoV 下 SphereOcc 仍达 8.98% mIoU 与 17.42% GeoIoU，超过对应第二名（8.34% 与 17.09%）——但相对其 360° 完整 FoV 下的 13.91% mIoU 已大幅下降。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 12, Section 6.3 and Table 8 (page 14)
- Evidence: Table 8 水平 FoV 360/300/240/180/120 度扫描：所有方法随覆盖减少退化；120° 下 SphereOcc 8.98/17.42 仍为最佳但远低于其 360° 结果。
- Quote: “Under horizontal FoV reduction, all methods exhibit per- formance degradation as the available angular coverage decreases. At the most restrictive 120 ◦ FoV, SphereOcc still achieves 8.98% mIoU and 17.42% GeoIoU, outperforming the corresponding second-best results of 8.34% and 17.09%.”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0660

- Claim: 垂直 FoV 从 136.70° 缩到 76.70°（自上而下遮蔽、保留下半球面图像）时，SphereOcc 的 mIoU 仅从 13.91% 降至 13.80%、GeoIoU 从 24.65% 降至 24.48%，仍高于所有对比方法在完整 FoV 下的最佳结果（13.80% vs 12.21% mIoU、24.48% vs 22.55% GeoIoU）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 12, Section 6.3 and Table 8 (page 14)
- Evidence: Table 8 垂直 FoV 扫描：136.70→76.70° 时 SphereOcc mIoU 13.91→13.80、GeoIoU 24.65→24.48，仍超对比方法完整 FoV 最佳（12.21/22.55）；作者称 greater stability under vertical FoV reduction。
- Quote: “SphereOcc exhibits greater stability under vertical FoV re- duction. When the vertical FoV is reduced from 136.70 ◦ to 76.70 ◦ , its mIoU decreases only from 13.91% to 13.80%, while its GeoIoU decreases from 24.65% to 24.48%. Notably, these results remain higher than the best full-FoV results of all competing methods, with 13.80% versus 12.21% mIoU and 24.48% versus 22.55% GeoIoU.”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0666

- Claim: 数据集径向统计显示：随距自车距离增加，前景交通参与者占比递减——车辆从 15.78% 降至 0.60%、行人从 0.05% 降至 0.01%、骑行者从 0.20% 降至 0.08%；植被从 22.74% 升至 47.95%、建筑先升到约 29% 后保持稳定。作者将前景参与者的递减与远距更强的遮挡和更低的可观测性相关联。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 6, Section 3.2, Semantic Statistics and Fig. 4
- Evidence: Sec 3.2 语义统计（Fig. 4 右面板，0–70m 分七个 10m 径向仓）：前景类占比随距离骤降，作者解释为 stronger occlusion and reduced observability at longer ranges。
- Quote: “Across radial bins, foreground traffic participants become progressively less prevalent, consis- tent with stronger occlusion and reduced observability at longer ranges. Specifically, the vehicle proportion decreases from 15.78% to 0.60%, while pedestrian and cyclist pro- portions show overall decreases from 0.05% to 0.01% and from 0.20% to 0.08%, respectively. Conversely, vegetation increases from 22.74% to 47.95%, while buildings rise from 12.75% to approximately 29% and then remain sta- ble a”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-1070

- Claim: VPR 定位的条件性结果：冻结 CosPlace 跨飞行视觉位置识别中，白天 ERP 八扇区最强（R@1 74.9%、R@5 90.8%、误差 17.2 m，优于原始鱼眼 4V 的 69.3/85.8 与 ERP 4V 的 66.7/83.6），但描述子调用翻倍；跨光照（South-Square 昼→夜）原始鱼眼 4V 最佳（9.5 vs ERP8V 23.8）；同照度夜→夜（South-Playground）ERP 4V 最佳（77.8）而 ERP 8V 最差（63.0）——最优扇区密度随条件与算力预算变化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 9, Section V-D 与 Table VII
- Evidence: Table VII 与正文报告四种表示（raw fisheye 4V/rectified 4V/ERP 4V/ERP 8V）在白天、昼→夜、夜→夜协议下的 CosPlace 召回与 GNSS 误差。
- Quote: “ERP 8V gives the strongest daytime result (74.9% Recall@1, 90.8% Recall@5, and 17.2 m error), but doubles descriptor calls relative to ERP 4V. ERP 8V gives the highest South- Square day-to-night Recall@5 (23.8%), whereas ERP 4V gives the highest South-Playground night-to-night Recall@5 (77.8%); the preferred sector density is therefore condition- and budget- dependent.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1071

- Claim: 冻结检测器接口的条件性：八视 ERP 角度目标匹配上 Ours 取得最高均值置信度 0.809 与 AP@10° 88.0%，与 Adaptive Seam 并列覆盖率 49.7%、精确率 96.1%、召回 89.1%；但作者明确这些角度目标指标是下游接口代理而非边界框 IoU 精度，且 YOLOv10-N 与 CosPlace 均未针对 ERP 适配或微调，结果不能分离 ERP 图像的内在下游优势。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 7, Table III 右三列与 Section V-A（'interface proxies' 声明）
- Evidence: Table III 右三列与正文报告 YOLO 8V 响应指标；作者两次声明角度目标指标非 IoU 精度、模型未适配 ERP。
- Quote: “Ours achieved the highest mean confidence (0.809) and AP@10 ◦ (88.0%). Ours and Adaptive Seam tied on coverage (49.7%), precision (96.1%), and recall (89.1%). These angular target metrics are downstream interface proxies, not bounding-box IoU accuracy.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-0448

- Claim: vanilla UMI 的夹爪状态估计依赖 ArUco 标记，该视觉方案受遮挡与严重鱼眼畸变影响，贡献了约 10% 的数据预处理失败与明显误差；exUMI 因此改用低成本 AS5600 磁旋转编码器做夹爪开合跟踪。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 4, Section 3.1 Hardware Design
- Evidence: Section 3.1 指出原 UMI 设计的夹爪状态估计依赖 ArUco 标记，受遮挡与严重鱼眼畸变之害，贡献约 10% 数据预处理失败与显著误差；为此提出 AS5600 磁旋转编码器方案。
- Quote: “The gripper state estimation in the original UMI design relies on ArUco markers, which suffer from occlusion and severe fisheye distortion, contributing to approximately 10% of data preprocessing failures and notable errors. To achieve accurate and robust gripper width tracking, we propose a low-cost AS5600 magnetic rotary encoder solution.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0458

- Claim: 作者自认算法限制：交互与运动信息受低动作维度与有限相机视角的限制，导致触觉预测性能不完美；计划通过集成力矩测量与多视角视觉输入解决。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 9, Section 7 Limitations (Algorithm Limitations)
- Evidence: Section 7 Algorithm Limitations：预测式交互表征学习框架存在固有约束，低动作维度与有限相机视角限制了交互与运动信息，触觉预测性能不完美；未来计划集成力矩测量与多视角视觉输入。
- Quote: “The interaction and movement information is limited due to low action dimen- sion and limited camera angle, resulting in imperfect tactile prediction performance. We plan to address these by integrating force-torque measurements and multi-view vision inputs in the future.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-0459

- Claim: 作者自认硬件限制：AR 头显式运动捕捉虽有稳健性，但用户反馈指出热不适与颈部疲劳两项人机工程问题；替代跟踪方案（如 HTC Vive Tracker）依赖外部基站、与便携性目标冲突；同时 9DTact 触觉传感器的耐久性与一致性仍是关键关切。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.14688](https://arxiv.org/abs/2509.14688) exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Locator: page 9, Section 7 Limitations (Hardware Limitations)
- Evidence: Section 7 Hardware Limitations 列出两条：AR 头显的热不适与颈部疲劳（考虑过 HTC Vive Tracker 但其依赖外部基站、与便携采集目标冲突）；9DTact 耐久性与一致性虽经改进仍有提升空间。
- Quote: “Hardware Limitations. (1) Although our AR headset-based motion capture system demonstrates robustness, user feedback highlights two ergonomic concerns of thermal discomfort and neck strain. While we considered alternative tracking solutions (e.g , dedicated motion capture trackers like HTC Vive Tracker), these trackers usually rely on external base stations for more accurate tracking, which conflicts with our design goal of maintaining portability for in-situ AR-assisted data acqui- sition.”
- Authors: yue-xu; litao-wei; pengyu-an; et al.

### LR-FISHEYE-2026-1117

- Claim: 模型能力差距（核心局限）：多数预训练模型通过卷积/池化等操作编码针孔图像适用的归纳偏置（如平移不变性），无法理解全景图像的畸变特性，直接迁移到全景图像时性能显著下降——如何在模型层面高效弥合数据域差距是全景视觉研究的关键问题。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 2, Motivation & Problem Space（Model Capabilities 段，句子起点在 page 1 末）
- Evidence: 问题空间'模型能力'段：预训练模型的针孔归纳偏置（translation invariance via convolution/pooling）、对全景畸变特性不理解、直接迁移性能显著下降、域差距弥合为关键问题。
- Quote: “tion characteristics of panoramic images, leading to a signif- icant decline in performance when the models are directly transferred to deal with panoramic images. Thus, how to ef- ficiently bridge the domain gap of data at the model level has become a key issue in the research on panoramic vi- sion (Coors, Condurache, and Geiger 2018; Shen et al. 2022; Su and Grauman 2019; Yun et al. 2023), especially in the era of embodied AI.”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1118

- Claim: 数据瓶颈（核心局限）：全景图像因 ERP 投影畸变且典型以高分辨率采集，人工标注成本高于针孔等图像类型；投影固有的几何畸变使常规为针孔图像设计的自动标注工具失效——二者显著阻碍大规模高质量数据集的发展，构成全向视觉在具身 AI 领域推进的数据瓶颈。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 1, Motivation & Problem Space（Data Bottlenecks 段）
- Evidence: 问题空间'数据瓶颈'段：ERP 畸变+高分辨率→人工标注贵、自动标注工具失效、阻碍大规模高质量数据集。
- Quote: “Data Bottlenecks: Panoramic images, which are often dis- torted due to equirectangular projection (ERP) and typically captured at high resolutions, are more costly to annotate manually compared to other image types, such as pinhole images. The geometric distortions inherent in these projec- tions make conventional automated annotation tools, typi- cally designed for pinhole images, ineffective. These chal- lenges significantly hinder the development of large-scale, high-quality datasets (Li et a”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1128

- Claim: 开放挑战（作者明示的局限）：(1) 泛化与鲁棒性——多数模型仍聚焦特定场景或投影方法，跨全景传感器规格/场景/投影的泛化仍非平凡，需投影无关表示与自监督学习；(2) 动态畸变处理——现有方法把畸变当帧独立的静态几何问题，而真实场景中畸变本质是动态的，需显式考虑全景视频序列中畸变的时间一致性与演化；(3) 行动感知表示学习——终极目标不止'看得更好'而是'行动更有效'，需把全景视觉特征整合进下游控制策略；(4) 可扩展统一架构——超越任务特定模型的低效，需要预训练于大规模全景数据、可快速特化到多任务的全向基础模型。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 6, Cross-Community Impacts & Open Challenges（Open Challenges 四 bullet）
- Evidence: Open Challenges 节四 bullet：Generalization and Robustness、Dynamic Distortion Handling、Action-Aware Representation Learning、Scalable and Unified Architectures。
- Quote: “Despite the positive cross-community impacts of omnidirec- tional vision in the embodied AI era, several open challenges remain, providing new directions for future research. • Generalization and Robustness: Most current models still focus on specific scenarios or projection methods (Ai et al. 2022). Developing models that generalize across diverse panoramic sensor specifications, application sce- narios, and projection methods remains non-trivial (Ai, Cao, and Wang 2025). It is necessary for fu”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1129

- Claim: 当前方法现状短板：尽管近期进展（含早期视觉-语言多模态模型），多数方法仍任务特定、在投影歧义上挣扎、缺乏大规模多模态预训练资源——这些局限阻碍模型泛化并对具身 AI 的更广发展构成显著挑战（作者以此为由提出 PANORAMA 与分阶段路线图）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 4, Emerging Trends & Future Roadmap 引言段
- Evidence: Emerging Trends 段：recent advancements 后的转折——task-specific、projection ambiguities、lack of large-scale multi-modal pretraining resources、hinder model generalization。
- Quote: “Additionally, early multi-modal models have emerged that integrate vision and language for more com- prehensive task understanding. Despite these advancements, many approaches remain task-specific, struggle with projec- tion ambiguities, and lack large-scale multi-modal pretrain- ing resources. These limitations hinder model generaliza- tion and pose significant challenges to the broader develop- ment of embodied AI (He et al. 2022”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1215

- Claim: 分割投影精度的实时代价：SfM 基线在两个解剖上分割精度均最高——CAO 96.69±1.59% vs RGB SLAM 85.48±5.09%、RGB-D SLAM 88.07±2.56%；BPH 96.23±2.64% vs 89.71±5.18%、90.87±5.40%——实时 SLAM 管线的分割投影精度系统性低于离线 SfM（作者归因：未做前作 [3] 中加权不同 mask 等修改的实时 mask 投影导致精度下降，page 9）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 7, Table 1; page 9, Section 5 Discussion
- Evidence: page 7 Table 1 两块 Segmentation Precision 行 + page 9 Discussion 归因句（"real-time projection of segmentation masks without additional modification, such as weighting different masks as in [3], causes a lower segmentation precision"）。
- Quote: “Table 1 Average quantitative evaluation results for 3D reconstruction methods. ↑ indicates higher is better, ↓ indicates lower is better. Best results in the category are given bold and the second best is underlined. SLAM processing times are reported before and after bundle adjustment (BA). Central Airway Obstruction SfM RGB SLAM RGB-D SLAM Median Closest Point Dist. (mm) ↓ 0.63 ± 0.13 0.52 ± 0.23 0.53 ± 0.32 One-sided Chamfer Dist. (mm) ↓ 0.90 ± 0.17 0.67 ± 0.30 0.66 ± 0.40 One-Sided Hausdorff”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1216

- Claim: 学习组件依赖与域间隙：管线性能重度依赖其学习组件；水下场景中深度模型降低噪声（更小 Hausdorff 距离），但因水下视图受空气-水域图像域间隙影响，MDE 的使用导致更大 Chamfer 距离、不一定改善重建；整体管线可容易适配不同场景或术式，并在 cadaver 实验中无任何修改即显示有前景的表现；DROID-SLAM 对内窥镜案例显示良好泛化，但通过 SLAM 管线内网络的 in-domain 训练与更好的深度估计模型，重建质量还可提升。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 10, Section 5 Discussion
- Evidence: page 10 Section 5 Discussion 第一段：heavily dependent on learning-based components；水下 domain gap；cadaver without any modifications；DROID-SLAM 泛化 + in-domain 训练可改进。
- Quote: “The performance of this pipeline is heavily dependent on its learning-based com- ponents. For the underwater scenario (Fig. 5), the depth model decreases the noise, leading to a smaller Hausdorff distance. However, since the underwater views are affected by the domain gap between images in air and water, the use of MDE results in larger Chamfer Distance and does not necessarily improve the reconstructions. Nonetheless, the overall pipeline can be easily adapted to different scenarios or pro- ced”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1217

- Claim: 实时恢复鲁棒性局限：具有离线性质的 SfM 对暂时遮挡或其他可致跟踪重初始化的因素更鲁棒，实时 SLAM 的恢复更困难，这也可能影响分割精度与重建精度；尽管 SLAM 算法能够在 SfM 失败的场景中重建（Fig. 5 水下两段），临床场景中血液或碎屑等更明显的因素可能需要对实时重建管线的修改。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 10, Section 5 Discussion
- Evidence: page 10 Section 5 Discussion 第二段：SfM offline 更鲁棒 vs SLAM real-time recovery 更难；blood/debris 临床因素；SLAM 在 SfM 失败场景可重建（Fig. 5）。
- Quote: “While SfM, with its offline nature, is more robust to temporary occlusions or other factors that can cause tracking to reinitialize, recovery in real-time for SLAM is more challenging. This can also affect the segmentation precision and reconstruction accuracy. Even though the SLAM algorithm is able to reconstruct in the scenarios SfM failed (Fig. 5), modifications to real-time reconstruction pipeline may be needed in the clinical scenario where factors such as blood or debris are more apparent.”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1218

- Claim: 形变建模缺失（作者自述核心局限）：管线未将场景形变纳入考虑，且随手术进行手术场景显著变化，因此需用中间重建更新场景表示（如 Fig. 6b 切除一叶后的术中重建）；该限制在 CAO 中因气管的刚性而较不明显，且如前作 [3] 所示手术自动化仍然可能；未来工作包括以形变建模改进感知以及超声等其他模态的集成。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 10, Section 5 Discussion
- Evidence: page 10 Section 5 Discussion 第三段："Finally, as a limitation, this pipeline does not take the scene deformations into account"；CAO 刚性缓解；未来工作形变建模+超声。
- Quote: “Finally, as a limitation, this pipeline does not take the scene deformations into account and as the operation progresses, surgical scenes change significantly. There- fore, intermediate reconstructions can be used to update the scene representations (e.g. in Fig. 6b). This limitation is less apparent in CAO due to the rigid nature of the trachea and as can be seen in our previous work [3], surgical automation is still pos- sible. Our future work includes improving the perception with deformatio”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1247

- Claim: 作者自认的系统边界：系统尚未集成在线回环闭合（当前全局一致性仅靠里程计与多视角约束），多传感器标定精化列为未来工作；实验讨论将计算开销定性为适度（moderate computational overhead），其主因是跨相机约束计算。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 8, Section V Conclusions; page 6-7, Sections IV-C and IV-E
- Evidence: 结论章 future work 列出在线回环与标定精化两项；Discussion（IV-E）与 IV-C 陈述 moderate overhead 及其来源。
- Quote: “Future work will explore online loop closure and investigate multi-sensor calibration refinement.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-1291

- Claim: 全景统一表示引入鱼眼多相机系统特有的三角化代价：鱼眼相机中心与全景球心不重合的平移偏移使基于球心的三角化得到错误 3D 点估计、导致状态估计退化；作者为此提出基于严格几何推导的外参补偿方法，以改善视角间特征一致性并显著降低三角化与优化误差。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 1, Section I Introduction; page 3-4, Section III-B.2
- Evidence: 引言指出全景模型三角化因相机中心与球心偏移而不准确，外参补偿方法改善视角间特征一致性、显著降低三角化与优化误差；III-B.2 给出共面几何推导（法向量、交线向量、深度残差修正）。
- Quote: “Due to the offset between the fisheye camera center and the center of the panoramic model, triangulation based on the panoramic model can lead to inaccurate 3D point estimates. To address this problem, we introduce an extrinsic com- pensation method based on rigorous geometric deduction. This method improves inter-view feature consistency and significantly reduces triangulation and optimization errors, resulting in more accurate long-term pose estimation.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1294

- Claim: 作者自认剧烈运动局限：快速姿态变化或剧烈设备晃动（Hard 系列）序列中，本文 LiDAR 子系统性能显著退化；由于视觉子系统依赖 LiDAR 点云提供深度信息，整体系统精度受连带影响——多鱼眼视觉无法独立弥补 LiDAR 退化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 5-6, Section IV-A
- Evidence: Section IV-A 指出 Hard 系列中 LiDAR 子系统退化且视觉子系统因依赖 LiDAR 深度而受影响；后文补充 FAST-LIO2（同为 FAST-LIVO2 的 LIO 子系统）基于平面特征的点到面关联比本文 LIO 的点到线关联提供更有效约束。
- Quote: “However, in sequences with rapid orientation changes or severe device shaking (Hard series), the performance of our LiDAR subsystem degrades considerably. Since the visual subsystem relies on accurate LiDAR point clouds”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1296

- Claim: 作者自认透明材质场景局限：M2DGR hall-05、door-02 序列中大面积玻璃墙干扰 LiDAR 点云深度信息，进而影响视觉特征的深度关联、降低系统精度——视觉特征深度依赖 LiDAR 的链路在玻璃幕墙环境受限（hall-05 本文 RMSE 仍达 0.992787 m）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 6, Section IV-B and Table III
- Evidence: Section IV-B 指出玻璃墙干扰 LiDAR 点云深度、影响深度关联并降低精度；Table III 中 hall-05 各方法 RMSE 均在 0.87-1.37 m 量级（本文 w/loop 0.992787 最优但绝对精度差），佐证该场景整体困难。
- Quote: “However, in the sequences such as hall-05 and door-02, the presence of large glass wall interferes with the depth information from LiDAR point clouds, which in turn affects the depth association of visual features and reduces the system’s accuracy.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1301

- Claim: 现成单目 LVIO 直接用于鱼眼数据会双重受损：LVI-SAM 的后端优化采用归一化平面，无法利用数据集中鱼眼相机的宽 FoV；鱼眼图像外围区域的严重畸变常导致视觉-LiDAR 数据融合时与点云错位——LVI-SAM 在 Newer College 全部 8 条序列失效。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 6, Section IV-A and Table II
- Evidence: Section IV-A 分析 LVI-SAM 失效原因：归一化平面后端无法利用宽 FoV，外围畸变导致融合错位；Table II 中 LVI-SAM 在全部 8 条 Newer College 序列 fail；本文全景视觉特征模型针对性解决。
- Quote: “LVI-SAM employs a normalized plane in its backend optimization, which fails to fully leverage the wide FOV of fisheye cameras in the dataset. Furthermore, severe distortion in the peripheral regions of fisheye images often leads to misalignment with point clouds during visual-lidar data fusion.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1302

- Claim: 作者自认两项待改进方向界定了当前系统的边界：相邻相机重叠观测区尚未被利用（当前仅按 FoV 归属单台相机处理重叠区深度点），系统在暗环境中的鲁棒性有待提升。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 8, Section V Conclusions; page 4, Section III-B.3
- Evidence: 结论章 future work 指出相邻相机重叠观测区利用与暗环境鲁棒性改进两个方向；重叠区当前处理方式见 III-B.3（深度点投影到 FoV 最可能包含该点云的相机图像）。
- Quote: “The future work will focus on how to take advantage of the overlapping observation areas of neighboring cameras and the improvement of the robustness of the system in dark environments.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-1303

- Claim: 极端光照是实测受限场景：Hilti'2022 评估中，强户外曝光与楼梯间极暗条件对基于视觉的方法构成重大挑战；同时这些场景 LiDAR 平面约束不足，单靠 LiDAR 难以准确鲁棒定位（工地与楼梯间尤甚），多相机融合正是在视觉与 LiDAR 双重退化的组合场景中提供足够约束。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05740](https://arxiv.org/abs/2509.05740) Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras
- Locator: page 7, Section IV-C
- Evidence: Section IV-C 描述 Hilti'2022 场景挑战：长走廊、楼梯、无纹理、光照不足、LiDAR 平面约束不足；强曝光与极暗楼梯间挑战视觉方法；多相机融合为 LiDAR 失效漂移提供约束补足。
- Quote: “Additionally, strong outdoor exposure and extremely dark conditions in stairwells pose significant challenges for vision- based methods.”
- Authors: xinyu-zhang; kai-huang; junqiao-zhao; et al.

### LR-FISHEYE-2026-0466

- Claim: 论文核心论断：现有手持接口主要依赖腕装相机，而人类靠移动头部管理遮挡、获取上下文；即使具备宽视野，末端中心（腕装）视角仍不足以服务长程任务与精细操作，并与使用头装相机的平台不对齐——腕装相机视角受操作需求而非感知目标约束。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 2, Section 1 Introduction
- Evidence: 引言指出多数现有接口忽视主动 egocentric 感知：人类移动头部管理遮挡与收集上下文，而现有 rig 主要依赖腕装相机；即使有宽 FoV，末端中心视角仍 underserve 长程任务与精细操作，且与头装相机平台不对齐。Section 3.2 重申：腕装相机随臂移动，视角受操作需求而非感知目标约束，难以处理视觉遮挡、可变形物体操作或需要大幅视角转换的任务。
- Quote: “Yet most current inter- faces overlook active, egocentric perception: humans move their heads to manage occlusion and gather context, while existing rigs rely primarily on wrist-mounted cameras. Even with a wide field-of-view, an end-effector–centric view underserves long-horizon tasks and fine manipula- tion and misaligns with platforms that use head-mounted cameras.”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0469

- Claim: 新环境同任务复测下腕装鱼眼-only 策略近乎全崩：UMI（仅双鱼眼腕相机）平均成功率从 in-domain 的 26% 跌至 6%（rope boxing/shirt folding/block disassembly/take drink from bag 四任务均为 0%），固定头相机 16%，ActiveUMI 保持 56%——腕装鱼眼-only 配置对视觉分布偏移最脆弱，主动视角的相对优势在新环境下扩大。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: page 7, Table 2
- Evidence: Table 2 在新环境下复测 Table 1 同任务集：UMI 30/0/0/0/0 均值 6%，固定头相机 30/10/20/0/20 均值 16%，ActiveUMI 70/50/80/30/50 均值 56%；正文指出依赖静态或受限视角的策略在环境改变时无法适应，而主动控制视角使策略对视觉偏移更有韧性。
- Quote: “Table 2. We compare our active perception approach to two variants in a new environment under the same task as Table 1. Camera View Tasks (New Environment) Bottle placing Rope boxing Shirt folding Block disassembly Take Drink from Bag Average UMI 30% 0% 0% 0% 0% 6% UMI w/ Fixed Head Camera 30% 10% 20% 0% 20% 16% ActiveUMI 70% 50% 80% 30% 50% 56%”
- Authors: qiyuan-zeng; chengmeng-li; jude-st-john; et al.

### LR-FISHEYE-2026-0486

- Claim: 长程任务失效模式：Heat Food 任务第一阶段成功率很高（开微波炉门 100.00%），但过渡到第二阶段时模型在相似观测之间发生局部失败（推微波炉门 vs 抓面包），导致剩余动作全部无法执行（放入面包 0.00%、关门 0.00%）；作者归因：数据集不提供固定第三人称视角的全局状态信息，轨迹不同阶段的相似视觉观测会影响模型推断，对依赖第一人称腕视角的模型影响尤甚。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 7, Section V.C Fine-tuning on VLA Large Models (Table IV)
- Evidence: Section V.C 报告 Heat Food 三阶段 staged 成功率并给出失效机理（相似观测局部失败+无第三人称全局视角）；Table IV 逐字给出 100.00%/0.00%/0.00%；作者预期纳入更丰富历史与时序信息的未来 VLA 可克服该局限。
- Quote: “Interestingly, for the Heat Food task, the success rate is high in the first stage. However, during the transition to the second stage, the model encounter a local failure between similar observations, such as pushing the microwave door open and grabbing the bread. As a result, the model is unable to proceed with the remaining actions. Since the dataset does not provide a fixed third-person perspective for global state information, the presence of similar visual observations across different sta”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0489

- Claim: 跨本体硬边界：由于 FastUMI 数据不受特定机器人本体物理限制约束，人手采集的轨迹可能超出小工作空间机械臂的可达范围；Wash Clothes 任务完全超出 Xarm6 平台工作空间导致无法执行；缓解方案是按目标机器人额定工作空间构建三维边界盒，过滤主体越界的轨迹。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 7, Section V.B Cross-platform Deployment
- Evidence: Section V.B 报告跨平台实验中发现的工作空间失配问题、边界盒过滤方案与 Wash Clothes 完全越界案例；Table I 显示 Wash Clothes 仅在 Flexiv Rizon4 上评测（33.33%），Xarm6 缺席与此一致。
- Quote: “We found that since data collected by FastUMI is not constrained by the physical limitations of any specific robotic embodiment, human-collected data may exceed the manipulation range of robotic arms with smaller workspaces. To address this issue, when filtering data, a three-dimensional bounding box can be constructed based on the rated workspace of the target robot. If the main part of a trajectory exceeds the predefined bounding box, it is considered outside the physical reach of the robotic”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0495

- Claim: 长程任务的阶段间衰减：Make Sandwich 与 Wash Clothes 任务第一阶段成功率高，第二阶段因推理错误累积出现精度下降（Table IV：Make Sandwich 100.00%→73.33%，Wash Clothes 93.33%→60.00%）——与 Heat Food 的骤降（C04）构成两种长程失效形态。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 7, Section V.C Fine-tuning on VLA Large Models (Table IV)
- Evidence: Section V.C 报告两任务的 staged 成功率衰减并归因于推理错误累积；Table IV 逐字给出 Make Sandwich（放生菜 100.00%、放面包 73.33%）与 Wash Clothes（抓衣入机 93.33%、关门 60.00%）的分阶段数字。
- Quote: “As shown in Table IV, for the tasks Make Sandwich and Wash Clothes, the first stage shows high success rates, followed by a slight decline in accuracy during the second stage due to the accumulation of inference errors.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0042

- Claim: 球面化以无旋转条件下的峰值检测精度为代价：同一无旋转训练/测试条件下，球面 YOLOv11 的 mAP@10 为 29.54%，低于平面 YOLOv11 的 39.65%（约 -10.1 点）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 7, Table 3
- Evidence: 表 3 的 NR/NR 条件显示球面 YOLOv11（29.54%）明显低于平面 YOLOv11（39.65%）；正文讨论将此类差距归因于离散径向权重的表达力受限。
- Quote: “Planar YOLOv11[22] NR 39.65% 24.41% 12.71% 4.66% RR 27.76% 9.99% 28.01% 10.24% Spherical YOLOv11 NR 29.54% 11.41% 29.59% 7.90% Table 3.Object Detection Results on PANDORA Dataset.”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0044

- Claim: 分割任务上球面化同样带来峰值精度代价：无旋转训练/测试条件下，球面 DeepLab v3 / UNet / YOLOv11 的 mIoU 分别为 28.78% / 25.72% / 24.29%，均低于对应平面模型的 35.01% / 33.33% / 28.32%（三个 backbone 均低约 4-7.6 点）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 7, Table 4
- Evidence: 表 4 的 NR/NR 条件下三个 backbone 的球面变体 mIoU 全部低于平面变体，差距从 YOLOv11 的 4.0 点到 DeepLab v3 的 6.2 点不等，与作者归因于离散径向核表达力受限的说明一致。
- Quote: “Planar DeepLab v3[5] NR 35.01% 58.30% 12.11% 22.50% RR 32.29% 52.89% 38.30% 53.99% Planar UNet[26] NR 33.33% 55.48% 12.91% 23.40% RR 33.75% 51.13% 35.91% 51.52% Planar YOLOv11[22] NR 28.32% 48.09% 8.17% 16.43% RR 28.53% 44.39% 30.62% 45.13% Spherical DeepLab v3 NR 28.78% 45.27% 28.09% 41.18% RR 30.55% 44.58% 32.59% 45.38% Spherical UNet NR 25.72% 42.20% 22.99% 35.29% RR 25.07% 40.85% 27.83% 41.81% Spherical YOLOv11 NR 24.29% 40.59% 15.61% 28.08% RR 21.52% 38.88% 24.05% 38.98% Table 4.Semantic Se”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0048

- Claim: 同一零样本跨镜头实验中球面优势是方向性的：从鱼眼训练迁移到针孔测试时球面 DeepLab v3 mIoU 为 40.27%，低于平面的 67.95%；从全景训练迁移到针孔测试时球面为 36.54%，也低于平面的 51.56%——向小 FoV 镜头迁移时平面模型反而更优。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 8, Table 5
- Evidence: 表 5 迁移矩阵的两个方向（fisheye→pinhole、panoramic→pinhole）显示球面模型低于平面模型；作者也承认两类模型都无法在所有镜头组合上完美，FoV 差异悬殊时降级更明显。
- Quote: “mIoU↑mAcc↑mIoU↑mAcc↑mIoU↑mAcc↑ Planar DeepLab v3[5] Pinhole53.75% 59.70%33.47%45.73%19.57%36.40% Fisheye67.95% 81.58% 68.54% 82.70%57.46%77.46% Panoramic51.56%62.24%55.57%67.91% 71.20% 92.12% Spherical DeepLab v3 Pinhole48.71% 62.21%36.51%62.07%35.62%61.05% Fisheye40.27%45.45% 54.65% 66.21% 48.04% 63.85% Panoramic36.54%42.38% 58.52% 69.75% 65.71% 90.44% Table 5.Zero-shot Lens Generalizability Test.Overfitted and tested on the same batch. Random rotation is disabled.”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0049

- Claim: 作者明确承认：使用离散径向权重保证等变但限制了方向敏感性；且角度偏移、包围框朝向等预测目标本质上是 gauge-dependent 的，无法仅靠旋转等变模型在全局旋转下保持，捕获这类方向线索需要带数据增强的方向性核或估计局部坐标架的 gauge-等变架构。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 7, 4.2.2 Results and Discussion
- Evidence: 4.2.2 讨论在解释球面检测模型 RR 下 mAP@50 下降（11.41%→7.90%）的语境下，作者陈述了径向核的方向敏感性损失与 gauge-dependent 目标的不可保持性，并指出需要方向核+增强或 gauge-等变架构。
- Quote: “reduction in raw accuracy due to limited expressiveness. The same trade-off recurs here: using discrete radial weights en- sures equivariance but restricts directional sensitivity, which is often important for capturing orientation-specific patterns. It is also worth noting that certain prediction targets, such as angular offsets or bounding box orientation, are inherently gauge-dependent and cannot be preserved under global ro- tation simply by a rotation-equivariant model. Capturing such direc”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0539

- Claim: 鱼眼成像的核心机制性代价是像素压缩：非线性投影把广角场景压进有限图像区域，Fisheye3DOD 中鱼眼视图物体的像素面积仅约为针孔对应物的 15%；由此造成空间分辨率与视觉细节的显著损失，且该成像期信息熵损失不可逆——无法通过鱼眼矫正（rectification）恢复。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 3, Section Challenges of Fisheye Images and Fig. 3
- Evidence: Fig. 3 Right 给出直观例子：同一物体针孔约 70×80 像素、鱼眼仅约 22×26 像素，鱼眼像素面积约为针孔的 0.1 倍（page 3 caption）。
- Quote: “The Figure 3 highlights a key challenge in fisheye im- agery: pixel compression. Fisheye projection nonlinearly compresses wide-angle scenes into limited image regions, resulting in significantly fewer pixels per object compared to pinhole projection. In our dataset, objects in fisheye views occupy only about 15% of the pixel area of their counterparts in pinhole images, as shown in Figure 3 (Left). This leads to a substantial loss of spatial resolution and visual detail, mak- ing reliable detec”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0541

- Claim: RQ1 答案：把代表性针孔 3D 检测器（BEVDet、PETR）经标准透视或柱面矫正迁移到鱼眼数据后，尽管有预处理，两模型相对各自 6 相机针孔原配置的 FDS 均下降超过 12 点，其余指标同步明显退化；作者把退化归因于鱼眼成像的固有限制——非线性投影压缩使有效像素密度骤降、信息损失不可逆，矫正无法弥补。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 5, Section Experiments, RQ1
- Evidence: 同段把根因指回像素压缩（~15% 像素面积，见 C03）；Table 2 具体数字见 C06。
- Quote: “RQ1: How much accuracy is lost when transfer- ring pinhole-based detectors to fisheye images? Table 2 presents the performance of representative pinhole-based 3D object detectors applied to fisheye data after standard recti- fication using perspective or cylindrical projection. Despite this preprocessing, both BEVDet and PETR suffer substan- tial accuracy drops compared to their original configurations on 6-camera pinhole images. Specifically, FDS decreases by over 12 points for both models, and”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0542

- Claim: Table 2 全量数字：BEVDet 从 6×针孔（FDS 0.563 / mAP 0.506）迁到 4×鱼眼后，透视矫正降至 0.440/0.304、柱面矫正 0.453/0.322，FisheyeBEVDet（等距柱面）恢复至 0.485/0.382；PETR 从 0.553/0.482 降至 0.408/0.274（透视）/0.411/0.285（柱面），FisheyePETR 恢复至 0.470/0.374——包括本文方法在内的全部鱼眼变体均未回到各自针孔基线水平。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 6, Table 2
- Evidence: 表中 mATE/mASE/mAOE 同步给出（如 PETR 针孔 mATE 0.580 → 鱼眼透视 0.783，FisheyePETR 降到 0.727；FisheyeBEVDet 恢复后 mASE 0.162 已优于针孔基线 0.161 附近）。
- Quote: “BEVDet 6 × P − 0.563 0.506 0.458 0.161 0.520 BEVDet 4 × F Perspective 0.440 0.304 0.588 0.177 0.505 BEVDet 4 × F Cylindrical 0.453 0.322 0.591 0.178 0.478 FisheyeBEVDet 4 × F Cylindrical 0.476 0.361 0.581 0.162 0.482 FisheyeBEVDet 4 × F Equirectangular 0.485 0.382 0.591 0.164 0.480 PETR 6 × P − 0.553 0.482 0.580 0.120 0.430 PETR 4 × F Perspective 0.408 0.274 0.783 0.161 0.433 PETR 4 × F Cylindrical 0.411 0.285 0.773 0.169 0.447 FisheyePETR 4 × F Cylindrical 0.441 0.330 0.758 0.159 0.425 FisheyeP”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0544

- Claim: 作者明确承认的天花板：即便有球面建模改进，鱼眼方法仍落后于针孔检测器；在本数据集中针孔图像为物体提供近十倍的有效像素面积，因此在空间证据显著更少的前提下，期待鱼眼检测器达到可比精度是不现实的。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 6, Section Experiments, RQ2
- Evidence: 这是作者自己给出的 limitation 声明（RQ2 段末承认段），与 C06 的表内差距一致。
- Quote: “It should be acknowledged that, despite these improve- ments, fisheye-based methods still lag behind pinhole detec- tors due to intrinsic imaging challenges. In our dataset, pin- hole images provide nearly ten times the effective pixel area of fisheye images for objects. It is therefore unrealistic to ex- pect fisheye-based detectors to achieve comparable accuracy while operating with significantly less spatial evidence.”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0548

- Claim: RF4 失败模式：从针孔输入切换到鱼眼输入时，小目标类别（Pedestrian、Cyclist）遭受最显著的性能下降——可能因固有尺寸小，鱼眼像素压缩下保留的视觉线索更少；且在仿真环境中该问题因纹理丰富度有限而进一步加剧。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 7, Section Additional Analysis, RF4 and Fig. 6
- Evidence: Fig. 6 逐类 AP 同时显示鱼眼模型在所有类别上均显著优于柱面矫正基线；作者建议借助小目标检测的洞察缓解。
- Quote: “RF4 (Failure Modes and Limitations): Small-footprint objects exacerbate challenges under fisheye distortion. Figure 6 compares per-class AP between our fisheye mod- els, cylindrical rectified baselines, and their pinhole coun- terparts. We observe that small-footprint classes, such as Pedestrian and Cyclist, suffer the most significant perfor- mance drop when shifting input from pinhole to fisheye. This may be due to their inherently small size, which results in fewer visual cues being preserved”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0551

- Claim: （读者推断）本基准的全部鱼眼证据是仿真级的：CARLA 缺乏原生鱼眼传感器支持，鱼眼畸变由 Kannala-Brandt 投影数学建模生成——即全部定量结论（迁移损失、恢复幅度、布局/距离/类别效应）建立在合成鱼眼图像上；全文无任何真实鱼眼传感器或真实场景验证，作者亦自述仿真纹理有限会加剧小目标问题——结论向真实鱼眼硬件与真实机器人场景的外推未经检验。
- Stance: `limit` | Confidence: `inference`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 3, Section Fisheye3DOD Dataset, Data Collection and page 7, RF4
- Evidence: 推断依据有三：CARLA 无原生鱼眼（本卡 context）；RF4 仿真纹理自述（page 7）；全文实验均在 Fisheye3DOD 上、无 real-world 实验（通读观察）。
- Quote: “Noting that CARLA lacks native fisheye sensor sup- port (Dosovitskiy et al. 2017), we mathematically model fisheye distortion via the Kannala-Brandt projection (Kan- nala and Brandt 2006).”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-0606

- Claim: 光照边界（QuadOcc）：OneOcc 在 day（21.15 vs 18.58）与 dusk（19.86 vs 15.14）领先最佳视觉基线，但 night mIoU 13.50 落后 MonoScene 14.20（精度更高，作者归因视锥伪影抑制）——全景相机方案在低光下不占优；LiDAR 基线则呈 dusk 常优于 day（近红外太阳背景更弱）、night 因回波统计改变与低反照率/镜面稀疏回波而下降的趋势。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 7, Section 4.2 and Table 5
- Evidence: Section 4.2 Robustness to Lighting Conditions（Table 5）报告 day/dusk/night 分层：OneOcc day 21.15/dusk 19.86/night 13.50，MonoScene 18.58/15.14/14.20；正文明确 night 落后但精度更高，并给出 LiDAR 的光照趋势解释。
- Quote: “OneOcc leads the best vision baseline in day (21.15 vs. 18.58) and dusk (19.86 vs. 15.14); at night its mIoU (13.50) trails MonoScene (14.20) but shows higher precision, likely from frustum-artifact suppression (cf. Fig. 4). LiDAR trend. Dusk often exceeds day due to weaker solar background in near-IR, while night drops with altered return statistics and sparser echoes on low- albedo/specular surfaces, hurting long-range completion.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0607

- Claim: 分辨率/任务边界（作者自述）：64×64×8@0.4m 体素对导航、落脚点选择与路径规划足够，但对需要精细接触推理的任务不理想——精确抓取、物体整理、杂乱货架操作；该尺度下小物体与细结构常只占几个体素，放大标签噪声且难以亚体素精度捕捉几何。提高分辨率（128×128×16 同边界）反而因优化难度降低 mIoU（32.23→21.16）、吞吐降约 3×（14.30→5.01 FPS）、显存增约 5.9×（1.82→10.71 GB）——粗网格是具身算力下的被迫最优而非自由选择。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 38, Section 12.1; page 18, Section 6.5 and Table 10
- Evidence: 补充材料 12.1 Limitations 首条：0.4m 体素对导航/落脚点/路径规划足够但对精细接触推理（精确抓取/物体整理/杂乱货架操作）不理想；6.5 节分辨率研究给出 128×128×16 的精度反降与 3× FPS/5.9× 显存代价。
- Quote: “Our se- mantic occupancy is defined on a 64×64×8 grid with 0.4 m voxels around the ego, which is sufficient for navigation, foothold selection, and path planning on legged/humanoid platforms with moderate speed and limited payload com- pared to intelligent vehicles. However, this resolution is not ideal for tasks that require fine-grained contact reasoning, such as precise grasping, object re-arrangement, or manip- ulation in cluttered shelves. At this scale, small objects and thin structures ar”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0608

- Claim: 标定敏感性边界：OneOcc 假设标定准确且漂移有界（作者在结论限制中明示）；受控标定噪声实验（H3O-Heter）显示联合内外参 1%/2%/5% 噪声下 mIoU 为 27.26/23.67/16.75（干净 32.23），仍优于 MonoScene（+5.27/+4.09/+2.79）但 5% 噪声下近乎减半；5% 噪声增强重训可把退化曲线拉平（5% 噪声下 22.84 几乎不降）但代价是干净性能从 32.23 降至 23.00——鱼眼/全景相机的精密标定是部署硬约束，鲁棒性-精度存在权衡。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 8, Section 5 Limitations & Outlook; page 19, Section 6.6 and Table 11
- Evidence: 结论 Limitations & Outlook 明示标定假设；补充材料 6.6 节注入受控内外参标定噪声（确定性、固定种子）并报告 1/2/5% 三档 mIoU 与噪声增强重训变体：OneOcc 27.26/23.67/16.75，增强变体近乎恒定 22.97/23.03/22.84 但干净降至 23.00。
- Quote: “With joint intrinsic+extrinsic noise, OneOcc achieves 27.26/23.67/16.75 mIoU at 1%/2%/5%, outperforming MonoScene by +5.27/+4.09/+2.79, respectively. This indicates that the proposed dual-projection lifting and 3D reasoning pipeline retains stronger geometric consistency under imperfect calibration.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0612

- Claim: 数据覆盖与 sim-to-real 边界（作者自述）：QuadOcc 中等规模且限于校园域环境，H3O 纯仿真；该组合对研究跨域鲁棒性与机器人形态变化有用，但未覆盖真实人形部署场景的多样性（如密集室内办公、家庭、高动态人群）——人形式评估当前依赖仿真占据标签，继承仿真器与渲染栈偏差，对带全景相机的真人形机器人存在不可避免的 sim-to-real gap。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 38-39, Section 12.1 Dataset coverage and sim-to-real gap
- Evidence: 补充材料 12.1 Limitations 第二条明确数据覆盖范围与仿真依赖，并给出缓解方向（更大规模真实 360° 占据数据集+sim-to-real 适配技术）。
- Quote: “QuadOcc is moderate-scale and rooted in a campus-like environment, and Human360Occ (H3O) is purely simulated. While this pairing is useful for studying cross-domain robustness and robot morphology changes, it does not fully cover the diver- sity of real humanoid deployment scenarios (e.g., dense in- door offices, homes, or highly dynamic crowds).”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0613

- Claim: 单帧设计边界（作者自述）：当前公式从单帧全景预测占据——避免对机器人运动模型的硬假设、简化部署并已由 GDC 吸收步态抖动，但限制了随时间累积证据、显式推理动态目标与利用长期时序上下文的能力；特别是快速移动主体（行人、车辆、其他机器人）在每帧被当作静态处理，任何时序一致性只能从训练数据隐式涌现。轻量时序实验佐证：3 帧 GT 位姿特征平均把 QuadOcc-val 20.56→20.92、H3O-Heter 32.23→33.74（BEVFormer 式注意力 21.18/34.25 但时延 69.93→78.60 ms、显存 1.82→2.35 GB），且 GT 位姿对齐不可部署，单帧仍是默认。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.03571](https://arxiv.org/abs/2511.03571) OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera
- Locator: page 39, Section 12.1 Single-frame design; page 19, Section 6.7 and Table 12
- Evidence: 补充材料 12.1 Limitations 第三条说明单帧设计的取舍与动态目标限制；6.7 节时序聚合实验给出两种 3 帧变体的精度收益与时延/显存代价及单帧默认的理由。
- Quote: “In particular, fast-moving agents (pedes- trians, vehicles, other robots) are treated as static at each frame, and any temporal consistency emerges only implic- itly from the training data.”
- Authors: hao-shi; ze-wang; shangwei-guo; et al.

### LR-FISHEYE-2026-0769

- Claim: 引入 ExpertTrack Memory 使 MOTA 从 27.34（无组件基线）降至 22.20（完整模型），作者解释记忆机制对假阳性更敏感；该组件单独的 HOTA 增益仅 +0.31，且与 DSSM 组合时增益低于两者单独增益之和的叠加预期。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 15, Section 5.3.1 + Table 7
- Evidence: MoE 记忆模块并非纯增益组件：MOTA 下降约 5 个点，HOTA 边际贡献小（+0.31），说明长时程身份保持与假阳性抑制存在张力。
- Quote: “When both com- ponents are combined, the improvements increase further to +1.17 points in HOTA and +1.49 points in IDF1, confirming that DSSM and ETM complement each other and jointly con- tribute to more robust and accurate temporal associations. It is worth noting that while the introduction of ETM leads to a decrease in the MOTA score (from 27.34 to 22.20 in the full model)—a common trade-off since memory mechanisms can”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0770

- Claim: FlexiTrack 实例训练构成消融显示：仅用反馈生成的 FlexiTrack 实例（I_ft）训练时 E2E 跟踪几乎失效（HOTA 4.39，MOTA 崩溃至 -1112.10）；仅用 GT 去噪实例（I_dn）为 14.64 HOTA；两者结合才达 28.47 HOTA——轨迹反馈信号自身不足以支撑端到端关联学习，必须依赖 GT 扰动信号的配合。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 16, Section 5.3.2 + Table 8
- Evidence: 反馈机制并非自足：无 GT 去噪实例时训练崩溃级别的失败表明反馈线索需要监督信号锚定，限制了该方法在无标注场景的直接迁移。
- Quote: “In Exp. 2 , using only I f t during training yields a modest HOTA of 4.39, indicating that while feed- back provides some informative signals, establishing accurate associations remains challenging and prone to overfitting. In contrast, Exp. 3 , which utilizes only I dn in training, achieves a substantial improvement to 14.64 in HOTA, reflecting the strong association cues inherited from GT-based information that effectively guide the network in linking simple targets. Finally, incorporating bot”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0772

- Claim: 推理效率对比：单张 RTX 3090、4160×480 输入下，YOLO26 检测器基线管线达 50.7-55.3 FPS，而 OmniTrack/OmniTrack++ 完整跟踪系统为 10.96-16.62 FPS——全景反馈式感知管线的推理成本约为纯检测器基线的 1/4~1/5。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 15, Table 5
- Evidence: 反馈闭环+全景处理的代价是 4-5 倍的帧率损失，且论文未提供机载嵌入式平台上的运行数据，具身部署的实时性存疑。
- Quote: “The Baseline employs YOLO26 as the detector with a standard Tracking-By-Detection (TBD) pipeline. Vanilla TBD replaces the detector with our OmniTrack Det or OmniTrack++ Det , enabling panoramic-aware detection while keeping the same TBD tracker. OmniTrack++ DA builds upon OmniTrack++ Det by incorporating our proposed feedback mechanism, where tracking outputs are fed back to the detector to refine future predictions. The numbers represent the improvement relative to the baseline method. The FPS”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0773

- Claim: 在 JRDB 测试集 TBD 范式上，OmniTrack++ DA 的 IDF1（29.52，前作 30.26）与 MOTA（25.05，前作 26.60）均较原 OmniTrack DA 回退；作者承认 OmniTrack++ 设计以 E2E 跟踪为主，数据关联集成仅受较少针对性优化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 14, Section 5.2.2 + Table 4
- Evidence: 长程记忆与反馈设计在 E2E 范式获益，但同一框架的 TBD 变体在关联与检测综合指标上反而回退，说明增益绑定于特定跟踪范式。
- Quote: “Under the TBD paradigm, while OmniTrack++ DA experiences a slight drop in IDF1 and MOTA compared to OmniTrack DA , it still achieves state-of- the-art HOTA (27.03) and OSPA (0.81) on the JRDB dataset. This minor trade-off in specific metrics is expected, as the de- sign of OmniTrack++ primarily focuses on optimizing E2E tracking; consequently, certain aspects of data-association in- tegration receive less targeted refinement.”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-0774

- Claim: 作者自述失败模式：在重度遮挡、密集人群或突然相机运动的复杂场景中，OmniTrack++ 仍会产生碎片轨迹或临时身份切换，当多个行人重叠或近距离移动时尤其明显；作者据此指出显式时序推理与遮挡感知建模是未来方向。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.00510](https://arxiv.org/abs/2511.00510) OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback
- Locator: page 19, Section 5.5 Failure Case Analysis
- Evidence: 全景相机解决的是'目标出视野'，但密集人群的重叠遮挡与运动歧义仍破坏身份关联，是该方法明确声明的残余挑战。
- Quote: “As illustrated in Fig. 12, our method occasionally struggles in complex real-world scenarios involving heavy occlusion, dense crowds, or abrupt camera motion. Specifically, our tracker may produce fragmented trajectories or temporary identity switches when multiple pedestrians overlap or move in close proximity. These issues mainly arise from severe occlusion and motion ambiguity, which can disrupt stable target association.”
- Authors: kai-luo; hao-shi; kunyu-peng; et al.

### LR-FISHEYE-2026-1188

- Claim: EyeVLA 作者断言：具身 AI 中视觉感知应当是主动的——系统必须决定看哪里、以什么尺度感知，才能在像素与空间预算约束下获取最大信息量；而现有视觉模型与固定 RGB-D 相机的组合"根本无法兼顾宽域覆盖与细粒度细节获取"，严重限制其在开放世界机器人应用中的效能。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 1, Abstract
- Evidence: page 1 Abstract 原文：感知应主动（decide where to look and at what scale to sense under pixel and spatial budget constraints）+ 固定 RGB-D 相机与宽域覆盖/细粒度获取不可兼得（fundamentally fail to reconcile）。
- Quote: “In embodied AI, visual perception should be active rather than passive: the system must decide where to look and at what scale to sense to acquire maximally informative data under pixel and spatial budget constraints. Existing vision models coupled with fixed RGB-D cameras fundamentally fail to reconcile wide-area cov- erage with fine-grained detail acquisition, severely limiting their efficacy in open-world robotic applications.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1189

- Claim: 具体受限任务与替代代价：机器人常需感知远处细粒度细节——读药瓶上的小字、识别特定工具连接器、确认微型拨动开关状态——才能做出决策；靠物理移动（locomotion）接近这些目标在时间、能量与路径规划开销上高度低效。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 2, I Introduction
- Evidence: page 2 Introduction 第二段：三个任务实例（medicine bottle 小字 / tool connector / toggle switch）+ locomotion 三类代价（time, energy, and path planning overhead）。
- Quote: “Robots frequently need to perceive distant, fine- grained details—such as reading small text on a medicine bottle, identifying a specific tool connector, or verifying the state of a tiny toggle switch—to make informed decisions. Relying on phys- ical locomotion to approach these targets is highly inefficient in terms of time, energy, and path planning overhead.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1190

- Claim: 固定单目/RGB-D 相机即使配强大 VLM 底座，也固有地把信息冗余（大块低价值背景区域）与关键细节缺失交织在一起：不牺牲宽域覆盖就无法解析远处文本或小型任务决定性结构；因此传统 VLM 管线在精度敏感任务上表现不佳，尽管擅长全局场景摘要。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 2, I Introduction
- Evidence: page 2 Introduction：interleave information redundancy (large low-value background areas) with critical detail omissions；cannot resolve distant text or small task-decisive structures without sacrificing wide-area coverage；underperform on precision-sensitive tasks。
- Quote: “Yet fixed monocular or RGB-D cameras—even when coupled with powerful VLM backbones—inherently interleave information redundancy (large low-value background areas) with critical detail omissions. They cannot resolve distant text or small task-decisive structures without sacrificing wide-area coverage. As a result, conventional VLM-based pipelines underperform on precision-sensitive tasks, despite excelling at global scene summarization.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1201

- Claim: 评估协议边界：Zoom 误差以原始 zoom 单位计（约 90 单位≈1× zoom）；任务完成率 CR 在物理机器人眼系统上对 50 个 held-out 真实场景做 5 次独立运行，成功判据为目标物体占据结果帧中"清晰可辨且居中"的区域——由人工评价（human evaluation）判定，报告 5 次运行的平均完成率。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 6, IV-A Metrics
- Evidence: page 6 Section 4.1 Metrics：(A) MAE 定义含 zoom 原始单位换算（90≈1×）；(B) CR 定义含 5 次运行、人工判据。
- Quote: “For zoom (Δ𝑧), errors are measured in raw zoom units; a change of approximately 90 units corresponds to 1× zoom in the real-world scene. (B) Task Completion Rate (CR). We deploy each model on the physical robotic eye system and evaluate it over five independent runs on the 50 held-out real-world scenes. A trial is considered successful if the target object occupies a clearly recognizable and centered region of the resulting frame, as judged by human evalua- tion. We report the mean task completi”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-1253

- Claim: 全景图像的根本光学困难：等距柱状投影造成强非线性畸变，在大规模透视图像上训练的深度特征提取器隐式假设线性采样，从全景图像产出不可靠特征、降低位姿估计稳定性与精度；且非线性区域的计算被浪费、拖慢运行速度。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 1, Section I Introduction
- Evidence: 引言明确列出畸变对深度特征的两重伤害（特征不可靠+算力浪费）；后文消融（#1 ResNet 退化、#2 SphereNet 训练崩溃）对该论断提供实验支撑。
- Quote: “Most deep feature extractors [5], [6], [7], [8], [9], [10] trained on large-scale perspective images implicitly assume linear sampling, which produces unreliable features from omnidirectional images, degrading the stability and accuracy of pose estimation. Additionally, computational power would be wasted in the non-linear region, reducing the running speed.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1261

- Claim: 宽 FoV 的反向边界（动态物体反例）：Hard-06 拥挤桥面序列上针孔方法反超全景方法——针孔裁切主要包含静态桥体结构，而全景图像纳入大量动态物体，降低特征匹配性能。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 5, Section V-B and Table III
- Evidence: V-B 明确的反例陈述；Table III Hard-06 列显示针孔方法（Droid-SLAM 12.9、DPVO 19.3、DPV-SLAM 17.7）对 360DVO 默认 23.1/fast 22.7 的反超格局（绝对值仍大，但相对排名反转）。
- Quote: “Notably, the pinhole methods outperform the OVO methods on Hard-06 captured on a crowded bridge. The pinhole crops predominantly contain static bridge structures, whereas the omnidirectional images include many dynamic objects, which degrades feature matching performance.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1263

- Claim: 球面卷积直接替换的失败（limit 消融）：用 SphereNet 替换经典 CNN 后模型训练中梯度爆炸（尽管做了梯度裁剪与学习率调参），最终完全无法估计任何相机位姿；SphereResNet（加残差块）才稳定训练并取得最佳精度——说明畸变适配网络本身有稳定性门槛。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 7, Section V-C and Table IV
- Evidence: V-C Distortion-Aware Spherical Features 段 + Table IV #2 行（'-' 表示失败）；Fig. 5 给 ResNet 45% vs SphereResNet 90% patch 跟踪精度的直观对比。
- Quote: “However, when re- placing the classic CNN with a spherical feature extractor, SphereNet [11], the model suffers gradient explosions despite clipping gradient and tuning learning-rate during training. It fails to estimate any camera poses consequently, shown in Tab. IV (#2).”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1264

- Claim: 重复纹理失败模式（limit）：Hard-04 序列（天空/草地/植被等重复纹理主导）上，高分辨率默认配置劣于经典与学习方法（含 OpenVSLAM、DPVO），而 fast 配置取得最佳结果 0.190 m——高分辨率梯度选择纳入大量歧义 patch，导致新关键帧对应不稳定；低 patch 数与低分辨率的 fast 配置隐式正则化了问题。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 6, Section V-B and Table III
- Evidence: V-B 末段详细分析该失败模式；Table III Hard-04 列：默认 5.10 vs fast 0.19 vs OpenVSLAM 0.28、DPVO 0.61。
- Quote: “On sequence Hard-04, 360DVO (default) underperforms both classical and learning-based methods (e.g., OpenVSLAM [1], DPVO [8]), while 360DVO (fast) achieves the best result (i.e., 0.190). This sequence is dominated by repetitive textures (e.g., sky, grass, foliage). High-resolution gradient-based selection admits many ambiguous patches, yielding unstable correspon- dences in new keyframes.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1265

- Claim: 边缘部署算力边界：Jetson Orin 上 360DVO 默认版最准但最慢（2 FPS，avg ATE 3.98），fast 版恢复约 5 FPS 且精度仍有竞争力（5.07 vs OpenVSLAM 6.38）；作者承认计算上比常规 OVO 方法略贵，认为精度与鲁棒性收益抵消开销。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 7, Section V-D and Table VI
- Evidence: V-D Edge Deployment 段 + Table VI（OpenVSLAM 3-7 FPS / 360DVO default 2 FPS / fast 5 FPS）。
- Quote: “As shown in Tab. VI, 360DVO (default) is the most ac- curate but also the slowest. 360DVO (fast) recovers efficiency (≈ 5 FPS) while remaining competitive in accuracy, outper- forming OpenVSLAM (5.07 vs. 6.38). Although computation- ally slightly more expensive than conventional OVO methods, 360DVO achieves noticeably higher accuracy and more robust tracking.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-1266

- Claim: 作者自述瓶颈与未来工作：高分辨率特征图上的模块构成主要计算瓶颈；降低输入分辨率或提升硬件算力可提速，但要在嵌入式平台实时运行必须开发更轻量且有效的特征提取器（列为有前景的未来方向）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.02309](https://arxiv.org/abs/2601.02309) 360DVO: Deep Visual Odometry for Monocular 360-Degree Camera
- Locator: page 8, Section V-D
- Evidence: V-D 末段结论性陈述；与 Table V 分辨率-FPS-ATE 三元权衡（8→17→22 FPS，ATE +21.6%/+41.0%）互证。
- Quote: “Modules operating on high-resolution feature maps constitute the principal bottle- neck. While reducing input resolution or increasing hardware compute capacity can improve inference speed, developing a more lightweight yet effective feature extractor is necessary for enabling real-time operation on embedded platforms, which is a promising direction for future work.”
- Authors: xiaopeng-guo; yinzhe-xu; huajian-huang; et al.

### LR-FISHEYE-2026-0383

- Claim: 腕相机通道是折损的关键放大器：去掉腕相机后，生成数据训练的 Pi0.5 三任务平均成功率降为 46.6%（pick-and-place 40.0%、push cuboid 70.0%、pour bottle 30.0%），同配置遥操作数据为 83.3%——与遥操作的差距从有腕相机时的 20.0 个百分点（80.0% vs 100.0%）扩大到 36.7 个百分点（83.3%−46.6%）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 9, Table 1
- Evidence: 通道依赖量化：Pi0.5 无腕相机 Paint 46.6% vs Tele 83.3%；pour 任务 Paint 仅 30.0%。差距 36.7pp 为 83.3−46.6 的简单算术。
- Quote: “Table 1 Real-world experimental results on different models using different data. Task DP Pi05 (w/ wrist camera) Pi05 (w/o wrist camera) Tele Paint Tele Paint Tele Paint Pick and place 90.0% 40.0% 100.0% 70.0% 90.0% 40.0% Push cuboid 100.0% 100.0% 100.0% 100.0% 90.0% 70.0% Pour bottle 40.0% 10.0% 100.0% 70.0% 70.0% 30.0% Avg. 76.6% 50.0% 100.0% 80.0% 83.3% 46.6%”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0384

- Claim: 折损幅度依赖策略架构：生成数据训练的 DP 策略三任务平均成功率 50.0%（pick-and-place 40.0%、push cuboid 100.0%、pour bottle 10.0%），同数据源遥操作为 76.6%，降幅 26.6 个百分点，大于 Pi0.5 的 20.0 个百分点降幅；且 DP 的遥操作基线本身 pour 任务仅 40.0%。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 9, Table 1
- Evidence: 架构依赖量化：DP Paint 50.0% vs Tele 76.6%；对比 Pi0.5 Paint 80.0% vs Tele 100.0%。降幅 26.6/20.0 pp 为表值减法（76.6−50.0、100.0−80.0）。
- Quote: “Table 1 Real-world experimental results on different models using different data. Task DP Pi05 (w/ wrist camera) Pi05 (w/o wrist camera) Tele Paint Tele Paint Tele Paint Pick and place 90.0% 40.0% 100.0% 70.0% 90.0% 40.0% Push cuboid 100.0% 100.0% 100.0% 100.0% 90.0% 70.0% Pour bottle 40.0% 10.0% 100.0% 70.0% 70.0% 30.0% Avg. 76.6% 50.0% 100.0% 80.0% 83.3% 46.6%”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0385

- Claim: 作者承认生成（"painted"）的腕相机图像存在伪影：腕相机距 3DGS 点云过近，导致相关 3D 点被渲染器剔除；作者表示将优化 3DGS 重建算法以提升重建质量。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 16, Figure 8 caption
- Evidence: 作者自述渲染边界：近距 3DGS 点云剔除 → painted 腕视图伪影；这是"任意视角"主张在近距机位上的显式例外。
- Quote: “Note that the "painted" wrist images exhibit some artifacts. This is because the wrist camera is too close to the 3DGS point cloud, causing the relevant 3D points to be culled by the renderer. We will optimize the 3DGS reconstruction algorithm to improve the quality of the 3DGS reconstruction.”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0006

- Claim: 在模拟六个任务的平均成功率上，使用常规增强训练的鱼眼策略零样本迁移到具有不同畸变与 FoV 参数的未见鱼眼镜头时出现严重性能下降（如 Param 3、Param 4 配置）；该实验主要在模拟中进行，真实世界验证被置于补充材料。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 8, Figure 10
- Evidence: Section 4.3 与 Figure 10 报告 baseline 策略在未见镜头上严重掉点；作者同时说明由于真实世界评估成本高，实验主要在模拟完成。
- Quote: “To verify this hypothesis, we conduct extensive experi- ments in simulation, as evaluating numerous hardware con- figurations in the real world is costly (see supplementary for real-world verification). We train policies on a sin- gle camera configuration (“Seen Param”) and evaluate their zero-shot transfer performance on fiveunseenconfigura- tions with varying distortion and FoV parameters (see sup- plementary for more details). The results in Fig. 10 are conclusive. The baseline pol- icy, trai”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0321

- Claim: 作者的问题定义：常规 RGB-D 方案受窄视场（FOV）与自遮挡限制，迫使机器人频繁移动基座，带来运动不确定性与安全风险；现有扩展感知的方案（主动视觉系统与第三视角相机）引入机械复杂度、标定依赖与延迟，阻碍可靠的实时性能。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 1, Abstract
- Evidence: 摘要逐句给出 RGB-D 窄 FOV 与自遮挡、频繁基座移动的运动不确定性与安全风险，以及主动视觉/第三视角相机的机械复杂度、标定依赖、延迟三项成本。
- Quote: “conventional RGB-D solutions suffer from narrow fields of view (FOV) and self-occlusion, requiring frequent base move- ments that introduce motion uncertainty and safety risks. Existing approaches to expanding perception, including active vision systems and third-view cameras, introduce mechanical complexity, calibration dependencies, and latency that hinder reliable real-time performance.”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0326

- Claim: 点云预处理以臂可达为界：原始全景 LiDAR 点云密度非均匀（传感器附近密集、远处稀疏）；为保证机械臂可达范围内的点密度与实时推理效率，系统裁剪 LiDAR 1.3 米以外的点（基于臂可达先验，远距稀疏采样对操作任务效用有限），剩余点均匀降采样至每帧 4096 点——全景覆盖下的有效操作工作区实际以约 1.3 米臂尺度为界。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 3, Section III-B, Point Cloud Processing
- Evidence: Sec. III-B Point Cloud Processing 段给出非均匀密度动机、1.3 m 裁剪（arm reachability prior）与 4096 点/帧降采样。
- Quote: “Raw panoramic LiDAR point clouds exhibit non-uniform density, with points densely distributed near the sensor and sparse at a distance. To ensure sufficient point density for nearby objects within the robot’s manipulation range while maintaining real-time inference efficiency, we design a lightweight preprocessing pipeline. Specifically, we crop out points beyond 1.3 meters from the Lidar sensor based on the robot’s arm reachability prior, where the sparse sampling provides limited utility for m”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0327

- Claim: 策略输入输出分解：模型输入为覆盖人形全部关节的 43 维关节状态（本体感知）加头装 LiDAR 全景点云；监督目标仅为上肢 28 维关节角（臂+灵巧手）；部署时学习到的策略只生成上肢关节命令，下肢与腰由预训练 HOMIE 算法控制以保持稳定行走；点云表示在 LiDAR 自体系中，部署时无需外参标定并增强跨环境适应性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 3, Section III-B, Learning and Deployment
- Evidence: Sec. III-B Learning and Deployment 段给出 43 维输入、28 维监督、部署分工与自体系免标定声明；全身自主列为未来工作（page 7，已核对）。
- Quote: “We train OmniDP using human demonstration data collected via the whole-body teleoperation system described in Sec. III-C. To achieve coor- dinated whole-body control, the model takes as input the 43- dimensional joint states covering all joints of the humanoid as proprioceptive information, together with panoramic point clouds from the head-mounted LiDAR as visual perception. The supervision target is the 28-dimensional joint angles of the upper body, including arms and dexterous hands. During d”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0333

- Claim: 作者未来工作声明暴露的系统边界：当前 OmniDP 为纯 LiDAR 几何路线——计划通过整合 LiDAR 几何、RGB 语义与触觉反馈引入多模态感知；全身自主（利用 LiDAR 感知相机视野外目标并用移动主动获取视角）、扩散策略+强化学习的动作精化、以及未见物体/布局/任务的零样本泛化均列为未来方向。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 7, Section V, Future Work
- Evidence: Conclusion/Future Work 段逐句列出四项未来方向；摘要中“全向感知比颜色/语义更关键”的判断（C02）与该多模态整合计划共同构成当前系统几何单模态的证据。
- Quote: “Future work will extend the system toward whole-body autonomy, leveraging LiDAR to perceive targets beyond the camera’s field of view and using locomotion for active viewpoint acquisition. We also plan to incorpo- rate multi-modal sensing by integrating LiDAR geometry, RGB semantics, and tactile feedback. On the control side, augmenting diffusion policy with reinforcement learning represents a promising direction to improve action refinement and adaptability. Strengthening the policy’s generaliz”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0345

- Claim: 对 GeoAwareVLA 在腕相机扰动下崩溃（而 agent 相机扰动下正常）的不对称行为，作者提出的解释是假设性的：若 VLA 训练中主要依赖腕相机特征，VGGT 提取的 3D 表征可能隐式锚定在腕相机坐标系——agent 相机变化时腕中心表征仍有效（功能正常），腕相机被扰动时整个几何参考系错位、3D 特征失去一致性，导致策略完全失效。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 5, Section IV-A.2 (hypothesis paragraph)
- Evidence: 作者以 We hypothesize 引出对 GeoAwareVLA 不对称崩溃的机制解释（3D 表征隐式锚定腕相机坐标系）；对比基线退化（π0.5 腕 28.6% vs agent 49.0%）作为"策略依赖腕相机特征"的证据。
- Quote: “as relative camera transformations, depth, and multi-view correspondences. However, if the VLA learns to predom- inantly rely on wrist camera features during training as evidenced by the base policy behavior, the 3D geometric representations may become implicitly anchored to the wrist camera coordinate frame. In this case, when the agent camera viewpoint changes, the wrist-centric 3D representation re- mains valid, allowing GeoAwareVLA to function reasonably well. However, when the wrist camera”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0346

- Claim: 视角增广数据微调路线存在两个根本困难（Fig. 3，LIBERO-Long agent 视角变化）：(1) 仅用 1 个任务的增广演示微调反而降低其余 9 个任务在新视角上的成功率——单任务学到的视角泛化不迁移；(2) 所有微调配置（1/5/10 任务）在原始视角上的性能随训练持续下降（灾难性遗忘），即使覆盖全部 10 个任务也无法避免。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 5, Section IV-A.3 and Fig. 3
- Evidence: IV-A.3 节在 LIBERO-Long 上以 1/5/10 任务覆盖度扫描 π0.5 微调：单任务微调降低其他任务新视角性能；原视角性能在所有配置下持续下降；10 任务也不能阻止遗忘。
- Quote: “As shown in Figure 3, fine-tuning with only 1 task actually decreases performance on novel viewpoints for the other 9 tasks. This reveals a critical limitation: viewpoint generalization learned from a single task does not transfer to other tasks, likely due to the task-specific visual patterns and object configurations. Furthermore, we observe a consistent decline in performance on the original viewpoint across all fine-tuning configurations as training progresses. This degradation indicates cat”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0351

- Claim: 作者自述限制：(1) 新视角合成重建质量退化时方法会失败——如源视图仅单台相机且目标视角相距远、或输入存在大遮挡区域；(2) 前馈新视角合成引入约 30 ms/帧延迟，在极端动态场景可能构成挑战，且推理需要额外 GPU 显存；(3) 当训练相机配置在各演示间不一致时，目标视角的选择仍是开放挑战。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05868](https://arxiv.org/abs/2603.05868) AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models
- Locator: page 7, Section V, Conclusion
- Evidence: 结论节以 Despite its effectiveness, our method has limitations 列出三类限制：NVS 退化场景、~30 ms/帧延迟与 GPU 显存、跨演示训练相机不一致时的目标视角选择。
- Quote: “Despite its effectiveness, our method has limitations. Our method can fail in cases when the reconstruction quality of novel view synthesis degrades, for instance, when the source view is limited to a single camera and the target viewpoint is far from the source view, or large occluded regions are present in the input images. Also, feed-forward novel view synthesis introduces a latency of approximately 30 ms per frame, which may pose challenges in extremely dynamic scenarios, and requires additi”
- Authors: hyeongjun-heo; seungyeon-woo; sang-min-kim; et al.

### LR-FISHEYE-2026-0621

- Claim: 同架构模态消融显示全景相机-only 路线在该基准上很弱：纯相机 C 仅 5.53 mIoU，加入全部成像模态（C+T+P）也仅 6.14，而引入 LiDAR（C+L）即跳至 22.87、全模态 23.34——几何信息主要来自 LiDAR，全景 RGB 及其与热/偏振的组合远逊于含 LiDAR 配置。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 7, Table II
- Evidence: Table II 中 VoxelHound 的六行模态配置（C 5.53/C+T 5.91/C+P 5.95/C+T+P 6.14/C+L 22.87/C+L+T+P 23.34）是同一架构下的受控消融；LiDAR-only 基线（EFFOcc-L 18.77、OccFusion-L 17.48、LiCROcc-L 17.95）也都大幅超过相机-only 变体。
- Quote: “C 5.53 1.34 6.35 0.00 21.03 18.26 2.59 6.91 8.09 0.45 1.03 0.09 0.17 C+T 5.91 3.31 11.09 0.00 19.95 16.80 1.11 8.48 8.28 0.34 1.26 0.30 0.02 C+P 5.95 1.12 4.19 0.00 20.13 19.59 3.86 9.56 9.68 0.45 2.48 0.14 0.19 C+T+P 6.14 1.51 8.25 0.03 20.83 18.17 4.47 7.78 8.96 0.08 3.26 0.08 0.21 C+L 22.87 26.86 22.11 0.00 48.99 34.56 6.46 23.38 34.16 37.70 16.49 7.14 16.54 VoxelHound (Ours) C+L+T+P 23.34 26.69 21.77 0.00 49.53 34.97 8.59 24.61 34.41 37.35 18.67 4.71 18.76”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0627

- Claim: 场景分解：VoxelHound 在相对结构化场景（尤其 residential/campus）表现最好，在 green spaces/forest/rural 等自然场景性能下降，原因是 irregular terrain、dense vegetation 与 ambiguous boundaries；Table A.1 中全模态 mIoU 为 campus 26.50、residential 20.30 vs forest 13.10、green spaces 15.35、rural 15.48（相机-only 各场景仅 3.39–4.97）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 12, Table A.1; page 12-13, Appendix B-A
- Evidence: 附录 B-A 定性句 + Table A.1 六场景两行（C 与 C+L+T+P）逐字数字；正文 page 8 未做场景分解，完整数据在附录。
- Quote: “performance drops in natural scenes such as green spaces, forests, and rural areas due to irregular terrain, dense vege- tation, and ambiguous boundaries.”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0628

- Claim: 体素分辨率权衡：在固定感知范围下把体素从 0.4m 细化到 0.2m（64×64×16→128×128×32）反而使 mIoU 从 23.34 降至 18.28，同时 GFLOPs 84.47→130.62、FPS 11.03→10.57、显存 386.97→393.99MB——更高体素分辨率并不必然提升占据预测（预测空间扩大增加优化难度）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 13, Appendix B-B and Table B.1
- Evidence: 附录 B-B 整段逐字（含全部五个指标数字与结论句）；Table B.1 两行对应。
- Quote: “We further study the effect of voxel resolution while keeping the perception range, evaluation protocol, model architecture, and training hyperparameters unchanged. Specifically, we re- fine the voxel size from 0.4m to 0.2m, corresponding to changing the voxel grid from (64×64×16) to (128×128×32). We report mIoU, Params, GFLOPs, FPS, and peak GPU memory measured on a single RTX 3090 with batch size 1. As shown in Tab. B.1, the finer 128 × 128 × 32 setting in- creases the computational cost from”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0629

- Claim: 极暗夜间失败案例：预测占据在场景边界（尤其远端区域）稀疏，主因 Livox MID-360 LiDAR 远距离点密度下降（距离越远观测越稀疏）；尽管如此多模态框架仍保持场景整体几何结构。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 14, Appendix C-B and Fig. C.1
- Evidence: 附录 C-B 首段逐字；同节后续对比 EFFOcc(C+L) 语义错误与 MonoScene 纯视觉失效（在 context 之外的后续句子，已核对：EFFOcc not only suffers from sparse predictions but also produces incorrect semantic categories / MonoScene fails to recover meaningful geometric structures）。
- Quote: “Fig.C.1 presents a representative failure case in an extremely dark nighttime environment. The predicted occupancy is sparse near scene boundaries, especially in distant regions. This phenomenon is mainly caused by the reduced LiDAR point density at long ranges, as the Livox MID-360 LiDAR produces increasingly sparse observations as distance increases. Despite this limitation, our multimodal framework is still able to preserve the overall geometric structure of the scene.”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0630

- Claim: 作者自述局限：(1) PanoMMOcc 虽覆盖多样环境，但整体规模相对大规模车载感知数据集仍有限，需更多序列/环境/天气条件；(2) 室内场景覆盖不足，可能限制部分机器人感知任务的适用性；未来工作包括噪声/缺失传感器下的鲁棒融合与时序线索。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.13108](https://arxiv.org/abs/2603.13108) Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots
- Locator: page 14, Appendix C-A; page 9, Section VI
- Evidence: 附录 C-A Limitations 整段逐字；future work 句与第 VI 节结论一致（robust and efficient multimodal fusion under noisy or missing sensor inputs、temporal cues）。
- Quote: “Despite the advantages of the proposed dataset and percep- tion framework, several limitations remain. Although PanoM- MOcc covers a diverse set of environments, the overall dataset scale is still relatively limited compared with large-scale vehicle-based perception datasets. Expanding the dataset with more sequences, environments, and weather conditions would further improve its representativeness for real-world robotic applications. In addition, indoor scenes are not extensively covered, which”
- Authors: guoqiang-zhao; zhe-yang; sheng-wu; et al.

### LR-FISHEYE-2026-0710

- Claim: 常规鱼眼矫正（rectification）前处理路线存在结构性代价：裁剪到矩形针孔视口会损失周边覆盖（这恰是选用宽 FoV 相机的初衷）；保留原始 FoV 则产生极端重采样伪影并使图像偏离下游模型的训练分布。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 2, Section 1 Introduction
- Evidence: 引言对矫正路线给出三重代价（覆盖损失/重采样伪影/分布偏移），另指出矫正引入延迟且依赖精确标定、误差会累积传播；这是对'最省事路线'的系统性否定论证。
- Quote: “Yet, this comes with a significant loss of peripheral coverage (due to cropping), which was the precise advantage that motivated the use of wide FoV cameras in the first place. On the other hand, retaining the original fisheye FoV in perspective images results in images with extreme resampling artifacts.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0722

- Claim: 作者自述局限：(1) 方法依赖 token 式适配，仅适用于 transformer 架构；(2) 自监督适配的保真度依赖原模型自身性能；(3) 对缺乏现成标注的任务，自监督路线可能受限（监督设定下可用真值部分缓解）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.28896](https://arxiv.org/abs/2603.28896) Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses
- Locator: page 15, Section 5 Limitations
- Evidence: 局限节简短但明确：transformer-only 约束排除了非 token 化感知模型；SSL 上限绑定基线模型质量；无标注任务上自监督受限。三者均未被实验进一步量化。
- Quote: “The proposed method is limited to transformer architectures due to its dependency on token-based adaptation. The fidelity of self-supervised adaptation also depends on the original model’s performance. While this is par- tially mitigated by the use of ground truth in the supervised setting, one may be limited for tasks that do not have annotations readily available.”
- Authors: ruxiao-duan; erin-hong; dongxu-zhao; et al.

### LR-FISHEYE-2026-0783

- Claim: 在 OccTrack360 上，采用针孔式 2D-to-3D 提升的 TrackOcc 基线直接以原始鱼眼图像为输入时近乎崩溃：OccSQ 总体仅 1.59、OccSTQ 1.67（对比 all 输入设置的 12.90/14.84）——针孔占据跟踪管线不经鱼眼几何适配无法处理未矫正鱼眼输入。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 7, Table II
- Evidence: Table II 的 Fisheyes 行：TrackOcc 1.59（OccSQ overall）/1.67（OccSTQ），各分项亦全面低下（parking 1.02、building 4.37、fence 0.34、OccAQ overall 2.16）。
- Quote: “TrackOcc Fisheyes 1.59 1.02 4.37 0.34 0.03 1.76 2.16 0.74 0.14 1.67 FoSOcc (Ours) 14.37 6.33 33.75 3.73 12.95 14.40 17.63 6.64 1.69 14.38”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0784

- Claim: 将鱼眼图像矫正为透视视图再输入针孔管线可部分恢复性能（TrackOcc OccSQ 10.15，高于原始鱼眼的 1.59 但低于 all 输入的 12.90），且作者明确指出矫正过程固有地限制 FoV 并降低覆盖——'先矫正后推理'是鱼眼部署中 FoV 换可用性的次优路线。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 7, Table II + Section V-D
- Evidence: Table II 的 Rectified Fisheyes 行给出 10.15；正文 V-D 节明确陈述矫正限制 FoV 并降低覆盖，FoSOcc 直接处理原始鱼眼以保持更完整感知范围。
- Quote: “Notably, while TrackOcc [13] relies on rectifying fisheye images into perspective views—a process that inherently limits the field-of-view (FoV) and degrades coverage—our FoSOcc framework processes raw fisheye inputs directly, thereby preserving a more comprehensive sensing range.”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0787

- Claim: 同一 all 输入设置下，大尺度结构类出现回退：building 类 OccSQ 从 TrackOcc 的 29.87 降至 FoSOcc 的 25.09（−4.78）；Fisheyes 设置下 FoSOcc 的 OccAQ Car（6.64）与 Truck（1.69）也低于 all 设置（9.87/5.03）——鱼眼球面提升的收益集中于小尺度几何规则类，对大尺度/远距结构类存在几何代价。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 7, Table II
- Evidence: Table II 中 all 行 building 列 29.87→25.09；Fisheyes 行 Car 6.64/Truck 1.69 对比 all 行 9.87/5.03。正文未单独讨论该回退（作者局限部分亦未提及），该模式由表格数字直接呈现。
- Quote: “TrackOcc all 12.90 0 29.87 0.85 7.02 17.07 20.69 8.38 3.40 14.84 FoSOcc (Ours) 14.20 7.56 25.09 2.90 12.70 17.61 21.53 9.87 5.03 15.82”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0790

- Claim: 作者指出鱼眼光学使既有体素偏移（boundary offset）监督失效的机制：外围区域严重切向畸变与不均匀分辨率导致 2D-to-3D 深度提升的必然误差，单个体素的深度错位即可令损失函数以最大可能误差惩罚模型并产生不稳定梯度——鱼眼畸变通过深度提升误差直接破坏边界监督信号。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 6, Section IV-B.1
- Evidence: IV-B.1 列举边界偏移监督的两个缺陷，第一缺陷的因果链完整：外围切向畸变→深度提升误差→单 voxel 错位→最大误差惩罚→不稳定梯度；第二缺陷为全局归一化的物理含义模糊。
- Quote: “In fisheye optics, peripheral regions suffer from severe tangential distortion and non-uniform resolution, leading to inevitable errors in 2D-to-3D depth lifting. Even a single-voxel misalignment in depth can cause the loss function to penalize the model with the maximum possible error”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0792

- Claim: 由于 GPU 显存限制，OccTrack360 上的实验将水平有效范围从基准设计的 [−25.6m, 25.6m] 压缩到 [−12.8m, 12.8m]——环视感知范围仅兑现一半，12.8m 以远的占据预测能力未被评估，'360° 环视'的实际评测范围与宣称覆盖之间存在落差。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 6, Section V-A
- Evidence: V-A 节明确写出设计覆盖与实验有效范围的差异及原因（limited GPU memory）；z 轴 [−2.0m,4.4m] 与 0.2m 体素分辨率未受影响。
- Quote: “In the proposed OccTrack360, the spatial coverage is defined over [−25.6m, 25.6m] in both the forward-backward and left-right directions, and [−2.0m, 4.4m] along the z (vertical) axis. Each voxel has a finer resolution of 0.2m×0.2m×0.2m, and the input data are also provided at 2Hz. To accommodate limited GPU memory, however, we restrict the effective range in our experiments to [−12.8m, 12.8m] in the horizontal plane.”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0794

- Claim: OccTrack360 后向体素补全对 ego/实例位姿变换做 XY 平面投影并用 SVD 归一化，作者承认该操作在抑制误差的同时'不可避免地忽略了 z 轴方向的真实变化'——变换式标签构造在高度维度存在系统性信息损失，构成该类鱼眼占据基准的标签质量边界。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 4, Section III Object Completion
- Evidence: III 节 Object Completion 段承认 SVD 归一化的 z 轴代价；page 3 Fig. 4 另记录 z+ error 现象（KITTI360 外参高度平移 z_w 与坡道语义不一致），两者共同构成高度维度的标签风险。
- Quote: “Singular Value Decomposition (SVD) is then performed for normalization, which suppresses errors but inevitably disregards genuine variations along the z-axis.”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0900

- Claim: 作者报告：在透视图像上训练的深度基础模型（如 Depth Anything Models）虽在透视域性能强劲，但在 360° 全景图像上泛化很差，归因于透视域与全景域之间的显著几何差异；且完全微调这类模型通常需要大量全景数据。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 1, Abstract
- Evidence: 摘要首句直接陈述问题：透视基础模型在 360° 输入上 generalize poorly，原因（作者归因）是两域几何差异，且完全微调数据需求大。
- Quote: “Recent depth foundation models trained on perspective im- agery achieve strong performance, yet generalize poorly to 360 ∘ images due to the substantial geometric discrepancy between perspective and panoramic domains. Moreover, fully fine-tuning these models typically requires large amounts of panoramic data.”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0907

- Claim: 零样本量化对照（Table 2）：未适配的 DAM v2（ViT-L）在全景输入上 RMSE 为 0.5522（Matterport3D）/ 0.4884（Stanford2D3D），明显差于全景适配方法 PanDA-L（0.4539 / 0.3314）与 RePer-360（0.4534 / 0.2849）——透视基础模型在 360° 输入上的退化有具体数值。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 12, Table 2
- Evidence: Table 2 零样本对比：DAM v2 / PanDA-L / RePer-360 三行 RMSE 数值。
- Quote: “DAM v2 [36] ViT-L - 0.5522 - 0.4884 PanDA-L [6] ViT-L 0.1036 0.4539 0.1092 0.3314 RePer-360 (Ours) ViT-L 0.1033 0.4534 0.0630 0.2849”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0910

- Claim: 复杂度对比（ViT-L，单卡 RTX A4000）：RePer-360 参数量 359M、推理 1.30 FPS，参数比 PanDA-L（336M、2.59 FPS）多 23M（约 +6.8%），推理速度低于单分支 PanDA-L；同时远快于 patch 融合的 MoGe-2（326M、0.02 FPS）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 23, Table 7 (Supplementary B.3)
- Evidence: Table 7 复杂度对比：参数量与 FPS 三行；正文 B.3 说明速度下降源于 ERP→CP 投影与双分支特征提取，并给出 65×/98× 的路线级对比。
- Quote: “Method Parameters (M) FPS PanDA-L [6] 336 2.59 MoGe-2 [33] 326 0.02 RePer-360 (Ours) 359 1.30”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0911

- Claim: 作者自述限制：双分支架构带来额外计算开销、导致推理速度下降；较小 backbone 上观察到性能增益减弱。未来工作将提升架构效率，并把机制扩展到能处理多样成像模型（如鱼眼相机）等更一般框架——即当前方法不覆盖鱼眼相机。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05999](https://arxiv.org/abs/2603.05999) RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation
- Locator: page 25, Section C Limitation and Future Work
- Evidence: 补充材料 Section C Limitation and Future Work 原文逐字给出两条限制与未来工作方向。
- Quote: “Despite the additional computational overhead introduced by the dual-branch architecture, which leads to reduced inference speed, and the diminished per- formance gains observed with smaller backbones, RePer-360 demonstrates the potential of a guidance-based domain adaptation framework. Future work will focus on improving architectural efficiency and extending this mechanism toward a more general framework capable of handling diverse imaging models (e.g., fisheye cameras) and other cross-domain”
- Authors: cheng-guan; chunyu-lin; zhijie-shen; et al.

### LR-FISHEYE-2026-0939

- Claim: 负结果（透视范式直迁全景失败）：作者的比较视觉分析显示，常规 2D 透视范式（OOAL、OS-AGDO）直接应用于 360° 等距柱状输入时发生灾难性的空间推理崩溃——热图呈混乱、碎片化激活，普遍缺乏结构连贯性，频繁出现严重语义漂移（高响应区域系统性偏离真值功能区）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 6, Section V-C (Performance Analysis) and Figure 5
- Evidence: 第 V-C 节 + Fig 5：对 OOAL/OS-AGDO 热图的定性失效分析——碎片化激活、结构失连、语义漂移。
- Quote: “perspective-based paradigms undergo a catastrophic break- down of spatial reasoning when directly applied to 360- degree equirectangular inputs. The heatmaps generated by OOAL [9] and OS-AGDO [35] are characterized by er- ratic, fragmented activations and a pervasive lack of struc- tural coherence, frequently exhibiting severe semantic drift TABLE III: Ablation study of loss components on the 360-AGD Hard Split. We investigate the impact of the L KL , L RTC and L BCE . L KL L RTC L BCE KLD ↓”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0949

- Claim: 作者自述边界（结论 future work）：当前工作为具身智能体在真实 360° 环境提供基础，但未来研究才将探索动态场景的时序推理与 3D 空间表征的跨模态协同——即本框架不覆盖动态场景时序建模，也未与 3D 空间表征集成。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 8, Section VI (Conclusion)
- Evidence: 第 VI 节结论末句：两条 future work 方向隐含当前方法的覆盖边界。
- Quote: “We believe this work provides a solid foundation for embodied agents in real-world 360 ◦ environments. Future research will explore temporal reasoning for dynamic scenes and cross-modal synergy with 3D spatial representations.”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-1146

- Claim: 作者把扩展到动态环境（将实时行人跟踪与预测纳入场景图层级）与空地协作多智能体系统列为未来工作，表明当前 OmniVLN 框架与评估不覆盖动态行人场景。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 8, V Conclusion
- Evidence: 结论节未来工作：扩展 OmniVLN 到动态环境（实时行人跟踪与预测进入场景图层级），并研究共享表示支撑的空地协作多智能体系统。
- Quote: “Future research will extend OmniVLN to dynamic environ- ments by incorporating real-time pedestrian tracking and pre- diction into the scene graph hierarchy. Furthermore, we aim to investigate collaborative air-ground multi-agent systems where shared representations facilitate decentralized exploration and coordinated task allocation.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-1147

- Claim: 导航成功率与 token 消耗的定量评估使用作者自建的合成场景生成器（九个数据集 D1-D9、可控空间条件），理由是 MP3D 等现有基准的对象密度固定不适用；真实机器人上的导航仅为定性演示，论文未报告真实环境的定量导航成功率。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.17351](https://arxiv.org/abs/2603.17351) OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms
- Locator: page 6, Section IV-B.1; page 7, Section IV-C
- Evidence: IV-B.1：因 MP3D 等基准对象密度固定，作者开发合成场景生成器产出九个数据集（D1-D9）做可控空间条件评估；IV-C 的真实部署验证为 Fig. 8 定性演示（'go to the nearest chair' 命令的执行与场景图同步）。
- Quote: “Since existing benchmarks like MP3D [18] often feature fixed object den- sities, we developed a synthetic scene generator to produce nine distinct datasets (D 1 to D 9 ) with controllable spatial con- ditions.”
- Authors: zhongyuang-liu; min-he; shaonan-yu; et al.

### LR-FISHEYE-2026-0122

- Claim: 为针孔/透视图像设计的 SoTA 可供性与开放词汇分割方法在 PAP-12K 全景输入上严重退化：AffordanceVLM 仅 9.66 gIoU、LISA 15.21、OV-Seg 29.48，最强的 A4-Agent 也只有 62.55 gIoU，而 PAP 为 71.56 gIoU。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 8, Table 2
- Evidence: Table 2 完整列出 6 个透视基线在 PAP-12K 上的四项指标：最弱方法 gIoU 不足 10，与 PAP 差距极大，验证全景输入对针孔方法的域间隙。
- Quote: “OV-Seg (Liang et al., 2023) 29.48 17.85 32.00 18.80∼8s LISA (Lai et al., 2024) 15.21 16.34 13.66 8.30 ∼7s VisionReasoner (Liu et al., 2025) 49.33 44.64 51.06 38.06∼12s AffordanceVLM (Wu et al., 2025) 9.66 13.11 8.96 5.41 ∼7.8s Affordance-R1 (Wang et al., 2025a) 51.80 50.32 55.47 40.70∼10.4s A4-Agent (Zhang et al., 2025c) 62.55 49.97 67.09 54.28 ∼11.8s PAP (Ours) 71.56 62.30 75.49 64.97∼10s”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0123

- Claim: 作者前置实验显示：把全分辨率全景图直接输入在标准透视图像上训练的基线（Affordance-R1、AffordanceVLM、VisionReasoner、LISA、OV-Seg）会导致接近完全失败、指标接近零，因此论文报告的基线成绩均为把全景图缩放到各方法训练分辨率后的结果。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 22, Section C.3 Details of the Implementation of Baseline Methods
- Evidence: 附录 C.3 说明基线适配协议：全景输入必须缩放到训练分辨率才能得到有意义的评测，否则接近全失败；这是理解 Table 2 中基线成绩的前提。
- Quote: “In our preliminary experiments, directly feeding them full-resolution panoramic images resulted in near-complete failure, yielding performance metrics close to zero. To ensure meaningful evaluations, we resize the panoramic input images to match the respective training resolutions of each method before testing.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0127

- Claim: PAP 默认配置（Qwen3-VL-32B 骨干）单次全景可供性查询推理约 10 秒，作者自评延迟"可接受但不亮眼"；换 Qwen3-VL-4B 骨干可把延迟压到 2–3 秒，但性能下降约 8%；作者将其定位为高层规划可接受的延迟，并计划用 PAP 做离线数据生成以蒸馏更小的端到端模型。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 19, Section B.1 Acceptable but Unimpressive Latency
- Evidence: 附录 B.1 是作者对部署侧限制的直接陈述：约 10 秒延迟、轻量骨干的精度-延迟权衡，以及离线蒸馏的后续路线。
- Quote: “As demonstrated in Table 2 in the main text, our PAP significantly outperforms other baselines while main- taining comparable inference latency(∼10 seconds). However, for real-world robotic deployment, minimizing latency is always desirable.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0134

- Claim: （读者推断）PAP 的全部定量证据限于静态三脚架全景图上的离线 2D 掩码指标（gIoU/cIoU/P@50/P@50:95）：论文未报告任何机器人闭环、移动相机视点或下游操作成功率实验，"全景感知有利于具身智能"在机器人侧仍是动机层面论证。
- Stance: `limit` | Confidence: `inference`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 9, Section 5.1 Evaluation Metrics
- Evidence: 前提：评测协议只有四项 2D 掩码指标（S5.1）；采集为三脚架静态拍摄（S3.3）；全文（含附录 A-G）无机器人实验章节。结论：具身侧收益未被实验证明。
- Quote: “we adopt four complementary metrics to comprehensively assess prediction quality, including:1) gIoU (Generalized IoU):The average Intersection-over-Union across all test samples, measuring the overall segmentation quality of the predicted affordance regions.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0135

- Claim: 作者承认解耦管线的级联误差风险与端到端 ERP 原生模型的缺位：物体小部分跨网格边界时 RVR 可能漏输出其中一个网格（作者以约 10° 的 FoV 冗余缓解）；且能原生理解 ERP、高效推理可供性的端到端模型对下游应用价值更大，PAP 被定位为零样本数据生成引擎与后续端到端模型的基石。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 19, Section B.2 End-to-End Model v.s. Decoupled Pipeline; Section B.3 (pages 19-20)
- Evidence: 附录 B.2/B.3 是作者对方法边界的直接讨论：解耦架构的级联误差来源与缓解手段，以及对端到端 ERP 原生模型的期待。
- Quote: “Nevertheless, we recognize the significant potential of end-to-end models for this task. While we have introduced several tailored designs to bridge the domain gap between panoramic and conventional camera imaging, a model capable of natively understanding Equirectangular Projection (ERP) images and efficiently inferring affordances would offer even greater value for downstream applications.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0025

- Claim: 作者论证：对 FoV 超过 180° 的宽角相机，把鱼眼图像矫正为针孔等效视图本质上有损——丢弃针孔 FoV 之外不可恢复的边缘内容，且重映射压缩边缘区域所需的重采样会引入插值伪影、降低目标本已很小的有效分辨率；这是选择在原生鱼眼图像上操作并让模型几何表征适配非线性投影的理由。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 3, Section 3.1
- Evidence: Section 3.1 以矫正的有损性论证原生鱼眼操作动机：边缘内容丢失与插值伪影两级代价。
- Quote: “However, rectification is fundamentally lossy for wide-angle cameras (FOV>180 ◦): it discards periph- eral content beyond the recoverable pinhole FOV , and the resampling required to remap compressed peripheral regions introduces interpolation artifacts that degrade effective reso- lution where objects are already small [10, 28].”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0026

- Claim: BEV 提升模块假设平坦地面作为世界-相机对应；该假设适合典型驾驶场景的道路表面，但对高架结构（如天桥标志、立交桥上的车辆）与非平面地形会退化，作者提出多平面表示作为讨论过的扩展方向。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 5, Section 3.4
- Evidence: Section 3.4 明确写出平地假设及其在高架结构/非平面地形下的退化。
- Quote: “We note that the BEV lifting module assumes a flat ground plane for the world-to-camera correspondence. While this assumption is well-suited to road surfaces in typ- ical driving scenarios, it degrades for elevated structures (e.g., overhead signs, overpass vehicles) and non-planar ter- rain.”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0027

- Claim: 作者声明的限制：FishRoPE 的逆投影需要已知的相机内参，端到端内参估计被列为未来工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 6, Limitations
- Evidence: 结论后明确给出 Limitations 段：需要已知内参做逆投影。
- Quote: “Limitations.FishRoPE requires known camera intrinsics for the inverse projection; end-to-end intrinsic estimation is future work.”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0083

- Claim: 作者明确声明宽 FoV 成像本身不提供显式、可靠的深度或运动估计，并以此作为引入直接几何传感（LiDAR）的动机。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 5, Section III-A, design principles HD2-HD3
- Evidence: 这是对鱼眼超广角观察的关键能力边界声明：宽 FoV 提高视觉覆盖但不提供深度/运动估计。结合 HD3（page 5）：UMI 用侧镜构造隐式立体深度，UMI-3D 改用 LiDAR 直接几何感知获得度量尺度深度与鲁棒 SE(3) 状态估计。
- Quote: “However, wide-FoV imaging alone does not provide explicit and reliable depth or motion estimation, motivating the use of direct geometric sensing.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0084

- Claim: 原始 UMI 依赖单目视觉 SLAM：原始工作自述需要视觉特征足够丰富的环境、在白墙/弱光等弱纹理区域可能失败；后续大规模 UMI 数据收集研究进一步表明视觉 SLAM 对遮挡与动态场景变化高度敏感——开门/抽屉等大物体部分或完全遮挡相机视野的任务会使 SLAM 误判运动甚至完全丢失跟踪，从而限制可采集的任务范围。
- Stance: `limit` | Confidence: `citation-supported`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 2, Section I
- Evidence: 论文在引言中综述了 UMI 视觉 SLAM 的两类失败模式：弱纹理环境（引原始 UMI [4]）与遮挡/动态场景（引大规模 UMI 数据收集研究 [15]），并指出这些限制使数据采集偏向对视觉 SLAM 友好的场景。
- Quote: “As acknowledged in the original work, the system requires environments with sufficiently rich visual features to maintain stable tracking, and may fail in textureless regions such as blank walls or poorly lit scenes [4]. More critically, subsequent empirical studies on large-scale UMI data collection further reveal that visual SLAM is highly sensitive to occlusions and dynamic scene changes. For instance, during the ma- nipulation of large objects that partially or fully block the camera view, s”
- Authors: ziming-wang

### LR-FISHEYE-2026-0088

- Claim: 杯碟摆放的失败分析显示：低对比度且偏离训练分布的棕色碟子持续取得最低分——策略在多数情况下能成功抓杯并到达正确放置区域，却犹豫释放物体或将杯子放到碟外；作者将此归因于视觉歧义，并在讨论中总结精确放置仍从根本上受感知质量限制、需要更几何感知或多模态的表示。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 13, Section V-A, Failure Analysis and Discussion
- Evidence: 该失败模式表明系统瓶颈转移到了推理时的 2D 视觉感知：抓取与接近动作正确，但放置目标定位受低对比度影响；作者据此提出需要 geometry-aware 或多模态表示。
- Quote: “A notable failure mode is observed for the brown saucer (seventh row in Fig. 11), which consistently yields the lowest scores. In many cases, the policy successfully grasps the cup and reaches the correct placement region, but hesitates to release the object or places it outside the saucer. We attribute this behavior to visual ambiguity. The brown saucer exhibits low contrast with the surrounding environment and deviates from the training data distribution, making it difficult for the policy to”
- Authors: ziming-wang

### LR-FISHEYE-2026-0090

- Claim: 同一长时序任务中，32.5% 的 trials 成功完成门开与取杯、却在放置阶段因违反机器人逆运动学约束而失败；作者认为这是演示动作与机器人可行构型空间不匹配的表现，需要更严格的运动学过滤或具身感知的策略约束。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 14, Section V-C, Failure Analysis
- Evidence: 这是感知之外的主要失败来源：演示动作超出机器人可行构型空间，属于数据-具身不匹配而非感知失败；与第二失败来源（训练数据少导致的抓取成功率低）并列。
- Quote: “First, a significant portion (32.5%) of trials successfully complete door opening and cup grasping but fail during place- ment due to violations of the robot’s inverse kinematics con- straints. This suggests a mismatch between the demonstrated motions and the robot’s feasible configuration space, indicating the need for stricter kinematic filtering or embodiment-aware policy constraints.”
- Authors: ziming-wang

### LR-FISHEYE-2026-0288

- Claim: 视角选择强烈影响扩展收益：加入与部署视角分布差异大的训练视角几乎无益——在 square 任务上，Cam_F+侧视+顶视三相机训练仅得 0.17/0.24/0.40（N=10/25/50），与单视角 0.14/0.26/0.42 基本持平甚至更低；相机间夹角从 15° 增大到 30° 时增益也明显小于默认设置。作者归因于这些分布外视角数据不能改善固定 Cam_F 推理输入下的模型性能。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 5, Section IV-B, Q3 and Table III
- Evidence: Tab. III 对比了四种训练视角组合：默认 15° 邻近视角、30° 夹角、前+侧+顶完全不同视角。Q3 正文明确：setting 1) 中多视角伪演示 hardly improves performance，setting 2) 增益 less significant，均归因于视角分布差异。
- Quote: “In setting 1), exploiting pseudo-demonstrations from multiple views hardly improves the performance of imitation learning. Since only Cam F is used during inference, the ad- ditional side-view and top-view cameras used during training capture perspectives that have distinct distributions. Despite their diversity, these out-of-distribution data may not help to improve the model performance with Cam F inputs during inference. In setting 2), a performance gain is also observed, but it is less signi”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-0291

- Claim: 动作空间与视角扩展强耦合：EEF 动作空间在有无多视角训练时都显著差于 base/camera 空间（square 单视角 EEF 0.06/0.25/0.32 vs base 0.14/0.26/0.42；五视角下 EEF 0.09/0.27/0.41 vs base 0.18/0.42/0.55），作者归因于 EEF 坐标系原点移动大幅增加策略学习难度；base 与 camera 动作空间都能从多视角训练显著获益。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 5, Table II
- Evidence: Tab. II 单独对比 base 与 EEF 动作空间在单视角/五视角下的成功率；正文（page 4）指出 EEF 显著更差且归因于移动原点，base/camera 空间则均能获益，显示视角扩展对动作空间的鲁棒性与例外。
- Quote: “TABLE II: Effect of Action Space. Training View Space Square N = 10 N = 25 N = 50 Cam F Base 0.14 0.26 0.42 EEF 0.06 0.25 0.32 Cam F , Cam F L , Cam F R Cam F U , Cam F D Base 0.18 0.42 0.55 EEF 0.09 0.27 0.41”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-0292

- Claim: 相机动作空间虽在多数情况下性能更好，但需要多相机标定、带来额外人工；作者明确称在 base 与 camera 动作空间之间选择是性能与劳动强度的权衡。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00557](https://arxiv.org/abs/2604.00557) Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning
- Locator: page 5, Section IV-B, Q2
- Evidence: Q2 段末的权衡声明：camera action space requires multiview camera calibration, which incorporates extra human labor; it is a trade-off between performance and labor intensiveness。
- Quote: “However, it is also worth mentioning that camera action space requires multiview camera calibration, which incorporates extra human labor. Therefore, it is a trade-off between performance and labor intensiveness to select the action spaces between base and camera spaces.”
- Authors: yichen-xie; yixiao-wang; shuqi-zhao; et al.

### LR-FISHEYE-2026-1049

- Claim: 点图重建结果的条件性：在自建环绕数据集上，已知相机位姿时本方法 Overall Chamfer 0.268 优于最佳基线 Pi3 的 0.332（Comp. 0.126 vs 0.221）；但在无位姿设定下 Acc. 0.612 与 Overall 0.482 反而劣于 Pi3 的 0.580/0.460——本方法的优势依赖已知标定/位姿条件。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 7, Table 1（Section 3.2）
- Evidence: Table 1 按 w/o pose 与 w/ pose 两设定报告 Acc./Comp./Overall，本方法仅在有位姿列全面领先，无位姿列 Acc./Overall 落后 Pi3。
- Quote: “Pi3 [13] 0.580 0.440 0.353 0.221 0.460 0.332 Ours 0.612 0.409 0.350 0.126 0.482 0.268”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1054

- Claim: 存储并非最优的作者承认：离线方法 4DGS 在存储上更紧凑（Table 5 中 0.3 MB vs 本方法 7.2 MB），但需全序列联合优化、不适合机器人低延迟流式；在线方法 IGS 的内存占用也略小于本方法（6.5 vs 7.2 MB），作者以更好渲染质量与更快渲染作为补偿论据。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 10, Section 3.4 Comparison 末段（4DGS 0.3 MB 数据在 page 9, Table 5）
- Evidence: 正文承认 offline 方法（如 4DGS）storage 更紧凑、IGS slightly more compact，并给出适用性论辩。
- Quote: “Although offline methods such as 4DGS are more compact in storage, they require sequence-level optimiza- tion over the entire scene and therefore are not suitable for practical low-latency streaming applications in robotics.”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-1171

- Claim: 对鱼眼图像先去畸变再训练 3DGS 的通行做法引入两类问题：(1) 图像边缘黑边造成信息丢失，抵消鱼眼大 FoV 优势；(2) 拉伸-插值重采样把每像素值摊到更大区域、稀释细节密度，导致 3DGS 过拟合这些低频区，产生模糊与漂浮伪影。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 1, Abstract
- Evidence: 摘要列出 undistortion 两个问题：黑边信息损失 negate 大 FoV 优势；stretch-and-interpolate 重采样稀释细节密度导致 3DGS 过拟合低频区、产生 blur 与 floating artifacts；page 2 引言以 'irreversible compromises' 复述并归为现有鱼眼 3DGS 工作（3DGS/Fisheye-GS）的共同前置。
- Quote: “1) Black borders at image edges cause information loss and negate the fish- eye’s large FOV advantage; 2) Undistortion’s stretch-and- interpolate resampling spreads each pixel’s value over a larger area, diluting detail density— causes 3DGS overfit- ting these low-frequency zones, producing blur and float- ing artifacts.”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1173

- Claim: 作者观察：即使鱼眼相机模型建模正确，重建场景在图像边缘仍出现漂浮物——畸变向周边增大，而 3DGS 原始的逐迭代随机单视图选择优化忽略同一高斯的跨视图相关性，导致极端形状（如过大或拉长）从而降低重建质量。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 1, Abstract
- Evidence: 摘要：'Despite correct modeling' 后描述边缘 floaters 现象与两个成因（畸变向周边增大 + 随机单视图选择忽略跨视图相关性→极端形状）；page 4 Section 3.3 展开：独立逐迭代优化对同一高斯产生跨视图不一致的几何/光度参数，边缘（畸变最大处）最严重，VR 头动时 floaters/flickering 降低沉浸感。
- Quote: “Despite correct modeling, we observed that the recon- structed scenes still exhibit floaters at image edges: Dis- tortion increases toward the periphery, and 3DGS’s orig- inal per-iteration random-selecting-view optimization ig- nores the cross-view correlations of a Gaussian, leading to extreme shapes (e.g., oversized or elongated) that de- grade reconstruction quality.”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1182

- Claim: CVO batch-size 权衡（Ruziniu，30k 迭代）：N=1→2 增益最大（PSNR 23.7717→24.0154，ΔPSNR/ΔTime 1.0344%）但训练时间从 38.87 分钟增至 62.43 分钟（+60.5%）；N≥3 边际收益递减（ΔPSNR/ΔTime 0.1711%-0.5215%），N=5 时 PSNR 24.2896 需 160.92 分钟（约 4.1 倍单视图时间）——作者指出最显著改善发生在 N=1→2（从单目到立体监督的转变），概念上重要。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 14, Table 10, Appendix Section E
- Evidence: Table 10：N=1-5 的 PSNR/LPIPS/Time/ΔPSNR/ΔTime（1: 23.7717/0.2232/38.87min/-；2: 24.0154/0.2139/62.43/1.0344%；3: 24.1583/0.2102/89.83/0.5215%；4: 24.2262/0.2077/129.52/0.1711%；5: 24.2896/0.2051/160.92/0.2019%）；Section E：N=2 为默认设置；N=训练图像数时视图选择策略无关紧要；'most significant improvement happens when moving from N=1→2—shifting from monocular to stereo supervision. This transition is conceptually important.'
- Quote: “Batchsize PSNR LPIPS Time (min) ∆PSNR/∆Time 1 23.7717 0.2232 38.87 - 2 24.0154 0.2139 62.43 1.0344% 3 24.1583 0.2102 89.83 0.5215% 4 24.2262 0.2077 129.52 0.1711% 5 24.2896 0.2051 160.92 0.2019% variance updates under large distortion. Combined with the CVO strategy, our method achieves sharper edges, smoother α-blending, and better cross-view geometric consistency, showing generality and effectiveness even in dataset like Den-SOFT (Table 3, Fig. 9), which exhibits more severe distortion, larger”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1184

- Claim: 作者自述局限：CVO 的性能增益在复杂光照条件下不显著——它有利于同一高斯的视图相关属性（SH）优化，但 Splat 范式下仍需进一步建模反射/折射等复杂效应（更精确的复杂反射率与各向异性、光照反射方向建模是有价值的未来工作）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00648](https://arxiv.org/abs/2604.00648) DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization
- Locator: page 14, Appendix Section G
- Evidence: 附录 G Limitations Discussion 首条：复杂光照下 CVO 增益不显著；Splat 范式需反射/折射建模；同节另指出超挑战区域（弱纹理等）对 3DGS 本身已困难、需更好表示与语义约束（future work），且 CVO 用 COLMAP 特征对应分组在稀疏纹理区不降低性能（无量化消融）。
- Quote: “A primary limitation is that CVO’s performance gain is not significant under complex lighting conditions. While it ben- efits optimization of view-dependent attributes (SH) of the same Gaussian, further modeling of complex effects like re- flection and refraction is needed under the Splat-paradigm.”
- Authors: zhengxian-yang; fei-xie; xutao-xue; et al.

### LR-FISHEYE-2026-1276

- Claim: 拼接全景图像的标定限制：由于拼接后的全景图像不对应任何物理相机，其相对 IMU 的外参通过定义虚拟相机中心（前后鱼眼光心中点）来近似——双鱼眼拼接结构的固有限制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 3, Section III-B
- Evidence: III-B 标定段明确陈述该近似；前后鱼眼各自外参用 Kalibr 标定，仅全景外参取中点。
- Quote: “Since the stitched panoramic image does not correspond to a physical camera, its extrinsic transformation with respect to the IMU is approximated by defining a virtual camera center as the midpoint between the optical centers of the front and back fisheye cameras.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-1287

- Claim: 作者自述局限：其一，整体框架可进一步加速以更好利用现代边缘设备的 GPU 资源；其二，虽然全向 FoV 提升了对遮挡和动态物体的鲁棒性，但这些因素未被显式建模，大规模遮挡或高度动态场景仍可能导致错误的位姿估计与建图。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.00852](https://arxiv.org/abs/2604.00852) PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset
- Locator: page 8, Section VI Conclusion
- Evidence: VI 结论末段两条局限陈述与未来工作方向。
- Quote: “Nevertheless, our method still has several limitations. First, the overall framework can be further accelerated to better exploit the abundant GPU resources available on modern edge devices [61]. Second, although the omnidirectional FoV improves robustness to occlusions and dynamic objects, these factors are not explicitly modeled, and large-scale occlusions or highly dynamic scenes may still cause erroneous pose estimation and mapping.”
- Authors: yiyang-wu; xiaohu-zhang; yanjin-du; et al.

### LR-FISHEYE-2026-0268

- Claim: 作者论证鱼眼投影对 VLM 接地的双重伤害：鱼眼引入强径向畸变与高度非均匀空间分辨率（图像中心保留细节、周边区域被重度压缩），叠加腕装位置带来的夹爪/手臂频繁自遮挡——几何扭曲+gripper-centric 视角偏移使 UMI 观测偏离 VLM 预训练与 VLA 协同训练中常见的视觉分布，对现有视觉表征构成事实上的分布外（out-of-distribution）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 2, Section 1 Introduction, visual grounding mismatch
- Evidence: Introduction 双失配框架的第一轴（visual grounding）：UMI/FastUMI 用腕装鱼眼（如 180° FoV 相机）采集，观测局部、gripper-centric、与全局/主视图监督根本不同；鱼眼投影的几何扭曲+腕装视角偏移共同把 UMI 观测推出 VLM 预训练分布。
- Quote: “fisheye projection introduces severe radial distortion and highly non-uniform spatial resolution: the image center preserves fine detail while peripheral regions are heavily compressed. Moreover, wrist-mounted placement introduces frequent self- occlusion from the gripper or robot arm. Together, the geometric warping induced by fisheye projection and the wrist-only, gripper-centric viewpoint shift UMI observations away from the visual distributions commonly seen during VLM pretraining and VLA co”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0269

- Claim: 从标准视图训练切换到腕装鱼眼训练使三个强 VLA 的平均成功率一致下降：π0.5 在 LIBERO 96.3→92.2、RoboTwin 82.0→59.4（平均降 13.4 点），LingBot-VLA 平均降 15.7 点，Wall-X 平均降 2.2 点——腕装鱼眼观测对 VLA 策略学习构成真实感知瓶颈。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 12, Table 1
- Evidence: Table 1 报告三模型在 LIBERO/RoboTwin 上标准视图 vs 腕装鱼眼（分别微调）的成功率与 Avg. Drop；正文说明切换观测域使三模型平均性能全部下降，π0.5 与 LingBot-VLA 降幅尤深（13.4/15.7 点，page 13）。
- Quote: “Model LIBERO RoboTwin Avg. Drop Standard View Wrist-Fisheye Standard View Wrist-Fisheye π 0.5 96.3 92.2 82.0 59.4 13.4 Wall-X 74.6 70.0 14.9 15.2 2.2 LingBot-VLA 85.3 81.7 77.6 49.9 15.7”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0270

- Claim: 鱼眼变换使 5 个通用与机器人专用 VLM 在 4 个空间推理基准上一致退化：平均绝对降 4.0 点（8.6% 相对降幅），单模型降幅 4.5%-13.7%——预训练 VLM 不会在畸变、局部、腕装鱼眼域下自动保持物体与空间理解。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 13, Section 4.1, Table 2
- Evidence: Table 2 报告 Qwen2.5VL-3B/Qwen3VL-4B/Embodied-R1/RoboBrain2.5/VLASER 在 Where2Place/RefSpatial/ERQA/EmbSpatial 上原始 vs 鱼眼变换图像的分数；正文给出平均绝对降 4.0 点（8.6% 相对）与单模型 4.5%-13.7% 区间，并确认该结果直接动机化感知对齐 VQA。
- Quote: “fisheye transformation causes a consistent mean absolute drop of 4.0 points (8.6% relative degradation) across all models, with individual model drops ranging from 4.5% to 13.7%. This confirms that pretrained VLMs do not automatically preserve object and spatial understanding under the distorted, local, wrist-mounted fisheye regime, directly motivating the need for perception-aligned VQA.”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0275

- Claim: 物理验证分数强预测部署成功：同规模（各 50 demos）的低分子集（平均分 35.50，主要由执行保真 39.35 拖累）训练的策略在 RealMan 订书机放置上 OSR 0.00（能抓 0.55 但放置全败），高分子集（平均分 99.21）OSR 0.65、PSR 1.00——低分数据教出'语义合理但物理上难以执行'的动作模式。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 15, Section 4.2, Table 4
- Evidence: Table 4 报告分数控制子集的打分（连续性 100/100、碰撞 94.69/100、保真 39.35/99.21）与部署结果（GSR 0.55/0.65，OSR 0.00/0.65，PSR 0.00/1.00）；Fig. 8/9（page 16）显示低分策略抓取后大位姿偏差导致放置失败。
- Quote: “Traj. Type #Traj. Continuity Collision Fidelity Avg. Score GSR OSR PSR Low-score subset 50 100.00 94.69 39.35 35.50 0.55 0.00 0.00 High-score subset 50 100.00 100.00 99.21 99.21 0.65 0.65 1.00”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0279

- Claim: 真机逐任务收益非均匀：VISTA 在部分任务上落后于 π0.5——Pick Target Fruits from Bowl 0.25 vs 0.35、Pour Chips from Bowl to Plate 0.70 vs 0.85；多数任务领先（如叠碗 0.92 vs 0.25、开微波炉 0.62 vs 0.40），整体 0.598 vs 0.528——平均增益掩盖了任务级波动（VISTA 自身任务间 0.25-0.85）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.04708](https://arxiv.org/abs/2606.04708) VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
- Locator: page 33, Table 11
- Evidence: Table 11 报告 20 任务逐任务成功率（LingBot-VLA/π0.5/VISTA 三列）：VISTA 在 Pick Target Fruits（0.25 vs 0.35）与 Pour Chips（0.70 vs 0.85）落后，在 stack_bowls_two（0.92 vs 0.25）、open_microwave（0.62 vs 0.40）等大幅领先，Overall 0.313/0.528/0.598。
- Quote: “Pick Target Fruits from Bowl 0.35 0.35 0.25 Put Doll into Drawer and Close 0.45 0.90 0.80 Open Drawer 0.00 0.40 0.55 Organize Dolls 0.55 0.80 0.80 Place Bun into Rice Cooker and Close 0.35 0.60 0.65 Arrange Flowers 0.55 0.75 0.55 Place Drink into Box 0.00 0.25 0.40 Hang Mug on Rack 0.00 0.60 0.50 Stack Pen Holders 0.00 0.40 0.55 Pour Chips from Bowl to Plate 0.80 0.85 0.70 Pick Plum from Cluttered Fruits 0.00 0.65 0.85 Stack Paper Cups 0.10 0.35 0.45 Place Fruits 0.60 0.40 0.65 Overall 0.313 0.5”
- Authors: siyuan-yang; linzheng-guo; ouyang-lu; et al.

### LR-FISHEYE-2026-0510

- Claim: 移除延迟匹配会降低动态投掷任务性能：感知、夹爪状态与机器人执行间的精确同步对定时敏感释放至关重要——鱼眼腕视图链路的时序校准是该类任务的必要组件而非可选优化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 6, Section IV.A, Fig. 6 ablation
- Evidence: Sec. IV.A 消融：移除延迟匹配→动态投掷退化；同步被表述为 timing-sensitive release 的关键。
- Quote: “For dynamic ball throwing, removing latency matching also degrades performance, showing that precise synchro- nization among sensing, gripper state, and robot actuation is critical for timing-sensitive release.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0511

- Claim: （读者推断）论文未披露鱼眼相机型号、FoV 度数与畸变校正策略，策略以 224×224 原始腕视图 RGB 直接消费鱼眼图像；『鱼眼腕视图足以支撑人形全身技能』的结论不能区分鱼眼大 FoV 的具体贡献与等效针孔腕相机的贡献，径向畸变对精细视觉定位的影响未被隔离测量。
- Stance: `limit` | Confidence: `inference`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 3, Section III.A (fisheye mentions) and page 4, Section III.B Observation
- Evidence: 全文 fisheye 仅 Fig. 2 caption 与 Sec. III.A hardware 两处，均为配置描述；无任何 FoV/型号/校正/对照实验信息，故该边界为读者基于文本缺失的推断。
- Quote: “In parallel, the handheld grippers record synchronized wrist- view images using fisheye cameras. The gripper width is measured by the magnetic encoder of the motor drive, providing gripper-state annotations for policy learning.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0512

- Claim: （读者推断）策略视觉输入仅腕部双视图，无全局/环视视野：任务空间定位依赖腕视图局部 grounding 与关键点几何接口，本框架的验证域不含需要场景级感知（避障、桌面外目标搜索、大空间导航）的任务。
- Stance: `limit` | Confidence: `inference`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 4, Section III.B Observation
- Evidence: Observation 段明确唯一视觉条件是左右腕视图对+下肢本体感知；五任务均为桌面/近场操作，无场景级感知任务。
- Quote: “The policy is conditioned on one synchro- nized pair of 224×224 left/right wrist-view RGB images and a three-frame history of a 15-D lower-body proprioceptive vector, including 12 leg joints and 3 waist joints. Upper-body joints are omitted because the policy expresses manipulation intent through task-space TCP keypoints, with joint config- urations resolved downstream by SKR and control.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0513

- Claim: （读者推断）全部任务成功率为 20-trial 条形图数值、正文零百分比数字：BifrostUMI 操作效果的定量强度不可从文本核验，其『可部署』结论在文本层面仅为定性主张，仅吞吐量（Table I）可复算。
- Stance: `limit` | Confidence: `inference`
- Paper: [2605.03452](https://arxiv.org/abs/2605.03452) BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: page 6, Fig. 6 caption and page 7, Fig. 7 caption, Table I
- Evidence: Fig. 6/7 caption 声明 20 trials 成功率条形图，正文以『substantially reduces』『degrades』等定性词描述消融，无任何百分比；Table I 是唯一文本化数字表。
- Quote: “The left-side bar plots report success rates over 20 independent trials for the corresponding ablations: the first two tasks evaluate the effect of spatial keypoint retargeting (SKR), while the dynamic ball-throwing task evaluates latency matching.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### LR-FISHEYE-2026-0803

- Claim: 单目度量深度模型随 FOV 从 120° 扩大到 195° 系统性退化（Table III 百分比变化）：DepthAnythingV2 AbsRel +166%、δ1.25 −86.8%；PatchFusion +160%/−87.4%；UniK3D +97.3%/−73.7%；ZoeDepth +60.1%/−51.7%；最稳的 DepthPro 也 +9.0%/−4.1%——宽 FoV 的畸变几何与域偏移使现成单目模型在鱼眼输入上大面积失效。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 6, Table III + Section V-A + Fig. 6
- Evidence: Table III 给出 195° vs 120° 的指标百分比变化；Fig. 6 显示 AbsRel 随 FOV 的渐变曲线（90-195°），针孔（90°）上各模型表现良好、随 FOV 扩大恶化；正文归因为 domain shift and distorted geometry。
- Quote: “DepthAnythingV2 [18] +166% +126% +106% -86.8% -81.5% -53.9% PatchFusion [19] +160% +123% +91.3% -87.4% -68% -27.9% UniK3D [22] +97.3% +147.2% +119.6% -73.7% -56.2% -38.9% ZoeDepth [20] +60.1% +47.3% +21.3% -51.7% -25% -6.5% DepthPro [21] +9.0% +3.3% +8.3% -4.1% -4.5% -2.31%”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0806

- Claim: StereoBase 的基线×FOV 网格分析（RelEPE，低优）：基线错配的伤害显著大于高 FOV——65mm 基线全程最优（0.061-0.074），20mm 次之（0.067-0.083），120mm 0.081-0.094，200mm 0.12-0.13，300mm 恒定 0.16 最差；大基线因视差分布偏移而退化——鱼眼立体部署中基线与训练分布的匹配是比 FOV 更关键的风险因子。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 7, Fig. 8 + Section V-B
- Evidence: Fig. 8 五基线×四 FOV 的 RelEPE 矩阵与正文 V-B 的结论（baseline variations affect performance more significantly than FOV；65mm optimal；larger baselines degrade due to disparity distribution shift）。
- Quote: “120 140 165 195 FOV (degrees) 20 65 120 200 300 Baseline (mm) 0.083 0.078 0.074 0.067 0.074 0.068 0.066 0.061 0.094 0.088 0.086 0.081 0.13 0.13 0.12 0.12 0.16 0.16 0.16 0.16 0.08 0.10 0.12 0.14 0.16 Fig. 8. Impact of baseline and FOV variations on RelEPE (lower is better) using StereoBase model. Results indicate much greater sensitivity to unfamiliar baselines than high FOVs, demonstrating our approach’s effectiveness for fisheye stereo.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0810

- Claim: 作者自述局限：LiDAR 扫描难以准确捕捉透明与反射表面，基准中这些区域被掩码处理——玻璃/镜面等对室内机器人感知高频出现的困难场景在 WideDepth 中系统性缺席（被标为零深度或清理掉），留作未来工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 7, Section VI Limitations and Future Work
- Evidence: VI 节首句即承认 LiDAR 对透明/反射表面的捕捉缺陷与掩码处理；IV-C 亦提及窗户/镜子半手工清理、反射面零深度掩码的实现细节。
- Quote: “LiDAR scanning struggles to accurately capture transpar- ent and reflective surfaces, so we masked these areas in our benchmark. However, these challenging cases present valuable research opportunities, and we aim to address depth estimation in such conditions in future work.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0811

- Claim: 作者自述局限：GPU 算力约束使域适应微调仅限于轻量架构（BGNet），域适应对更大模型（处理畸变几何）的效果不确定——62%/48% 级别的微调增益不能外推到重型立体模型。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 7, Section VI Limitations and Future Work
- Evidence: VI 节明确 GPU constraints restricted fine-tuning to lightweight architectures，larger models with distorted geometry 的域适应效果 uncertain；与 C11 的收益证据共同界定适用范围。
- Quote: “Regarding the experiments, our GPU constraints restricted fine-tuning to lightweight architectures, leaving the effect of domain adaptation on larger models with distorted geometry uncertain.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-0812

- Claim: 基准深度分布以中距为主体：2-5m 占 74.7%、0-1m 仅 6.9%、5-10m 9.6%、10+m 1.7%（长右尾来自走廊）——尽管动机强调操作任务需要亚厘米级近场精度，近场区间在基准中的证据密度最薄，'鱼眼深度支撑近场操作'的量化依据受限。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 4, Section IV-A + Fig. 4
- Evidence: Fig. 4 深度分布统计为报告数字；'动机与分布错位'的判断依据是 Section II-B 的 manipulation tasks demand sub-centimeter accuracy 陈述（page 2）与该分布的对照。
- Quote: “Figure 4 presents key dataset statistics. The depth range histogram shows a long right tail, which can challenge near- range indoor models. Overall, the primary depth bins are: 0–1 m (6.9%), 2–5 m (74.7%), 5–10 m (9.6%), and 10+ m (1.7%), aligning with typical indoor datasets.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-1086

- Claim: 通用 MLLM 直读 ERP 的能力受限：Table 2 中商用与开源通用 MLLM 在 pano-native 空间推理上整体偏弱（GPT-4o 31.8、Mimo-v2.5 37.2、Qwen3.5-9B 30.8 overall），性能在 BFOV 接地、参考系变换与观察者中心 3D 推理上下滑最明显，而基本物体识别相对较强——主要挑战不在物体语义而在把 ERP 全景当作连续观察者中心表示来推理；提示增强（视觉提示 36.4）只改善粗定位，在球面关系与 3D 空间推理上收益仍然有限（各通用基线 BFOV mIoU 仅 0.7-4.9）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 7, Section 4.2 与 Table 2
- Evidence: Section 4.2 开头段总结 Table 2：通用模型弱、下滑集中在 BFOV/参考系/3D；视觉提示只救粗定位。
- Quote: “Table 2 shows that general-purpose MLLMs remain weak on pano-native spatial reasoning. Across both proprietary and open-source models, performance drops most clearly on BFOV grounding, reference-frame transformation, and viewer-centered 3D reasoning, even when basic object recogni- tion is relatively strong. This gap indicates that the main challenge is not object semantics alone, but reasoning over the ERP panorama as a continuous observer-centered representation. Prompt enhancement improves di”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-1093

- Claim: 作者自述限制：(1) 元数据构建管线依赖自动开放世界检测、MLLM 语义标注、指代复检与全景深度估计——尽管引入两级验证提升可靠性，这些组件的错误仍可能传播到最终元数据图；(2) PanoSpace-Bench 定位为观察者中心 ERP 空间推理的诊断性基准，因此不覆盖所有全景任务，如长时程具身交互、动态场景或多智能体导航；作者据此提出未来方向：更可靠的全景感知模块与更强跨模态验证（数据侧），以及把 pano-native 基准从静态 ERP 推理扩展到交互导航、时序全景视频与动态 3D 环境（评测侧）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 22, Appendix F Limitations
- Evidence: Appendix F Limitations 给出元数据噪声传播与基准诊断范围两项限制及对应未来方向。
- Quote: “While PanoWorld demonstrates strong pano-native spatial reasoning, several limitations remain. First, our metadata construction pipeline relies on automatic open-world detection, MLLM-based semantic annotation, referring re-detection, and panoramic depth estimation. Although we introduce two-level verification to improve reliability, errors from these components may still propagate to the final metadata graph. Second, PanoSpace-Bench is designed as a diagnostic benchmark for observer-centered ER”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-0108

- Claim: 作者声明：仅有单个 eye-in-hand 移动相机时，演示阶段的视角覆盖不足以做动态场景重建、也不足以生成远离原视角的新视角，因此当前把 1001 DEMOS 管线限制在接触前或接触后的静态场景；提出的补救方向包括多相机 rig、ToF 传感器或需要更少训练视角的动态重建方法。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 9, Section 6, Limitations & Future Work
- Evidence: 这同时解释了为什么增广只在接触事件之前进行（接触后阶段原样保留原演示）以及为什么旋转范围有 50° 上限（C07）。
- Quote: “With only a single eye-in-hand moving camera, the view coverage of the demonstration stage is inadequate for dynamic scene reconstruction or for generating novel views far from the original viewpoints. As a result, we currently restrict the 1001 D EMOS pipeline to static scenes before or after contact.”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0109

- Claim: 新视角生成模块继承 3DGS 的多视角不一致性：对训练视角分布之外的生成视角会产生浮点伪影；作者建议采用 2DGS 等内在视角一致的表示来缓解。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 9, Section 6, Limitations & Future Work
- Evidence: 这是 C07 中“更大旋转界损害渲染质量”的机理根源：渲染退化以浮点伪影形式出现，作者以 2DGS 为候选修复方向。
- Quote: “Our novel-view generation module inherits 3DGS’s multi-view inconsistent nature, yielding float- ing artifacts for generated viewpoints outside of the training viewpoint distribution. This could be alleviated by adopting inherently view-consistent representations like 2DGS [45].”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0429

- Claim: 真机视角外移造成标准 VLA 断崖式退化：UR5e 12 相机平台（6 训练视角 / 6 保留测试视角）上，标准（多视角混合训练）VLA 的成功率从训练视角 68% 跌至新视角 17%；论文据此判定『多视角混训本身无法在测试时弥合新配置差距』，并称引入 ICWM 后无需参数更新或任务示范即有效缓解该退化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 7, Section 5.3, Figure 5
- Evidence: 作者在 5.3 节以 68%→17% 定量刻画视角外移退化，并把 ICWM 的价值定位为免参数更新的缓解；相对增益数字见图 5 轴标签。
- Quote: “As shown in Fig. 5, standard VLA performance drops sharply from 68% to 17% upon viewpoint shift, confirming that standard mix-training alone cannot bridge the gap to novel configurations at test time.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0433

- Claim: OOD 视角 135° 对包括 ICWM 在内的所有方法失效：作者归因为该视角特有的几何约束——物体遮挡与模型可见有效工作空间缩减，操作目标可能在执行中移出视野；这是一个方法无关的感知层共享限制，而非 ICWM 特有失败。表 4 中 135° 列各方法成功率 0.0–3.2%（如 Long 套件 MV 1.2 / EXP 1.0 / ICWM 2.2）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 16, Section B.2
- Evidence: B.2 节明确承认 135° 为全方法失效点并给出遮挡/视野归因；具体数值取自表 4（page 19）。
- Quote: “We also observe that certain OOD viewpoints, particularly 135°, pose challenges for all methods, including ICWM. We attribute this to viewpoint-specific geometric constraints: at 135°, the camera angle may introduce a certain degree of object occlusion and reduce the effective workspace visible to the model, which can cause manipulation targets to occasionally exit the field of view during execution. This suggests a perceptual limitation shared across methods, rather than a failure specific to I”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0434

- Claim: 上下文内容错误时是主动误导而非被忽略：使用 180° 偏移视角采集的错误上下文使 OOD 平均成功率（18.9）低于完全无上下文（22.0），负迁移幅度与正确上下文的增益（13.6%）对称——证明模型真实地以上下文内容为条件做配置推断；同节表 1 显示去掉图像 token 造成最大崩塌（平均 −56.4%），模型会把探测动作误当作任务示范去模仿。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 7, Section 6.1, Table 1
- Evidence: 6.1 节消融的关键定量：false context 18.9 < no context 22.0；增益 13.6% 对称；w/o images 平均 −56.4% 最大崩塌。
- Quote: “Critically, false context performs worse than no context at all (18.9 vs. 22.0), indicating that misaligned context actively misleads the policy’s world model rather than being pas- sively ignored. This negative transfer, symmetric in magnitude to the gains from correct context (13.6%), confirms that the model genuinely conditions on context content for configuration inference.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0439

- Claim: 推理开销定量边界：单张 RTX 4090 上基线 VLA 每步 0.112s；带 N=3 / N=5 上下文片段分别增至 0.165s / 0.185s（每步 +47% / +65%），作者称不破坏控制环稳定性；缓解依赖 KV 缓存，但其前提被明确表述为『交互上下文在固定配置下静态』——即部署期相机/系统配置不得变化；真机探测阶段另需一次性执行 20 个探测动作、约 5–6 秒（App. D）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 9, Section 6.4, Figure 10
- Evidence: 6.4 节延迟数值与 KV 缓存前提；App. D 的 20 步 / 5–6 秒探测开销。
- Quote: “While the baseline VLA requires 0.112s per inference step, our ICWM-enhanced model with N = 3 and N = 5 context clips incurs a latency of 0.165s and 0.185s respectively, without compromising control loop stability (Fig. 10). Fur- thermore, since the interaction context T ψ is static under a fixed configuration, its hidden states can be pre-computed and reused via KV caching, effectively reducing per-step inference cost back to near-baseline levels.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0442

- Claim: 『OOD 视角』实为训练方位角之间的角度插值而非包络外外推：6 个测试角中 45°/255°/285°/315° 分别落在相邻训练角的窄间隔内（(30,60)、(240,270)、(270,300)、(300,330)），135°/225° 落在最大训练间隔 (120,240) 内部；论文未区分插值与外推桶、未做 carve-and-hold-out 式包络控制（对照 2608.21402 的协议），故其『OOD 增益』证据不能等同于训练包络外视角外推，且最难视角 135° 恰位于最大间隔内部，提示纯角度插值本身即可失败。
- Stance: `limit` | Confidence: `inference`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 15, Section B.1
- Evidence: 推断卡：基于 B.1 角度分配的几何关系与表 4 中 135° 全方法崩塌的交叉引用；协议原文不含插值/外推区分。
- Quote: “We distribute 14 discrete azimuthal angles around the workspace cen- ter. We designate 8 In-Domain (ID) angles for training: ψ train ∈ {30 ◦ , 60 ◦ , 90 ◦ , 120 ◦ , 240 ◦ , 270 ◦ , 300 ◦ , 330 ◦ }, while withholding 6 Out-of-Domain (OOD) angles: ψ test ∈ {45 ◦ , 135 ◦ , 225 ◦ , 255 ◦ , 285 ◦ , 315 ◦ } exclusively for evaluation.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0443

- Claim: 长时程套件上预训练基线完全失效：π-FAST 与 NORA 在全部 6 个 OOD 视角均为 0.0（平均 0.0），π0.5 平均 0.1，而同条件下 MV 19.8 / EXP 20.2 / ICWM 25.0——经单视角微调的大规模预训练 VLA 的跨视角能力接近于零；作者在基线设置中明示这些预训练模型仅作上下文参照、用于论证『开箱即用泛化即使在大规模预训练下仍是未解难题』。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 19, Table 4
- Evidence: 表 4 Long 套件整块数值 + 5.1 节基线定位声明。
- Quote: “Long π-FAST 0.0 0.0 0.0 0.0 0.0 0.0 0.0 π 0.5 0.4 0.0 0.0 0.0 0.0 0.4 0.1 NORA 0.0 0.0 0.0 0.0 0.0 0.0 0.0 MV 30.4 1.2 2.8 24.0 32.8 27.6 19.8 EXP 29.8 1.0 6.4 24.0 27.8 32.2 20.2 ICWM (ours) 36.6 2.2 8.8 28.4 36.6 37.6 25.0”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0646

- Claim: 基线适配协议披露：FB-Occ、FlashOcc、SurroundOcc 原为 nuScenes 6 环视相机设计，被适配为 4 视图输入设定——仅使用每个双目对的左图；即单目基线看到 4 个视角，双目模型额外利用右图与视差信息。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 7, Section 5.1 Implementation Details
- Evidence: Section 5.1 实现细节逐字；GaussianFormer 为原生的 4 适配之一？——正文仅列 FB-Occ/FlashOcc/SurroundOcc 三个适配对象（GaussianFormer 未在该句中，已核对）；Table 2 中四个单目基线均以 Mono 输入标注。
- Quote: “We adapt FB-Occ Li et al. (2023b), FlashOcc Yu et al. (2023), and SurroundOcc Wei et al. (2023) (originally designed for nuScenes with 6 surround-view cameras) to a 4-view input setting using the left images from each stereo pair.”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0648

- Claim: 真实世界 GT 生产依赖外部传感与人工：真实占据监督基于 LiDAR 点云生成——融合稠密点云先经预处理消除无效点/外点/噪声，再变换到统一 baselink 坐标系并离散化到预定义体素空间，含 LiDAR 点的体素标为占据（代表实际物理观测支撑的区域）；未观测/遮挡区域经 FoV 约束可见性评估+3D Bresenham 射线追踪标记为未知而非误标自由，语义标签最终人工标注。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 13, Appendix A.3 Ground Truth Generation in the Real World (continued on page 14)
- Evidence: Appendix A.3 首段逐字覆盖 LiDAR 点云→预处理→baselink→体素离散化→占据标记；Bresenham 可见性与人工语义标注句在同节 page 14 后文（已核对：we employ the 3D Bresenham ray-tracing algorithm ... semantic labels are manually annotated to obtain semantic occupancy supervision）。
- Quote: “We generate 3D occupancy supervision ground truth based on LiDAR point clouds. First, the fused dense point clouds undergo a preprocessing stage to eliminate invalid points, extreme outliers, and significant noise, thereby mitigating the impact of artifacts on voxel labeling. Subsequently, the point clouds are transformed into a unified baselink coordinate system using sensor calibration parameters, and a predefined 3D voxel space is constructed around the robotic. Each point coordinate is discr”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0650

- Claim: sim-to-real 域差失败模式（作者承认）：真实世界评测揭示领域特定失败模式——光照差异（lighting discrepancies）与材质反射率不匹配（material reflectance mismatch）——这些失败模式反过来指导仿真器参数的迭代精化，以闭合 Real2Sim2Real 环；该闭环设计确保基准不是一次性仿真产物。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 5, Section 3.1 Real2Sim2Real Design Philosophy (Sim→Real paragraph, continued from page 4)
- Evidence: page 5（Section 3.1 Sim→Real 段落的跨页续文）逐字；Abstract 与 Contributions 的 closes the loop 表述一致；正文其余部分无自述局限（Conclusion 亦无），该判断基于全文结构核查。
- Quote: “reveals domain-specific failure modes (e.g., lighting discrepancies, material reflectance mismatch), which in turn inform iterative refinement of the simulation parameters—closing the Real2Sim2Real loop. This closed-loop design ensures that the benchmark is not a one-off simulation artifact but a continu- ously improvable pipeline tightly coupled with real-world deployment requirements.”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-0684

- Claim: 消融中的反例是物体计数：基础 VLM（多视角原始输入）保持小幅领先（Table 4 中 71.3 对 OneCanvas 68.4），作者怀疑这反映了较小的重投影误差会把画布上的实例碎片化或合并——即全景重投影管线在逐实例精细任务上有精度代价。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 9, Section 4.3 (Table 4)
- Evidence: Sec 4.3 消融讨论：object counting 是唯一 base VLM 领先的子任务（71.3 vs 68.4，Table 4 page 9）；作者归因 suspected small reprojection inaccuracies。
- Quote: “The exception is object counting, where the base VLM retains a small lead, which we suspect reflects small reprojection inaccuracies that can fragment or merge instances on the canvas.”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-0686

- Claim: 作者自述限制：OneCanvas 需要深度与相机位姿（纯 RGB 方法可避免这一依赖），且位姿估计失败仍会使画布退化（前馈度量重建正在缩小该差距）；单一全局全景以精细空间精度换取紧凑性（跨页续文：可能限制非常大或室外场景）；课程为手工设计、新增空间技能需编写新任务生成器；方法假设骨干至少有 2D 位置编码承载经纬度（Qwen3-VL 类多轴 RoPE 成立、1D 位置模型不成立）；全部实验仅用 Qwen3-VL-8B。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19253](https://arxiv.org/abs/2606.19253) OneCanvas: 3D Scene Understanding via Panoramic Reprojection
- Locator: page 9, Section 5, Limitations
- Evidence: 结论节 Limitations 段：深度+位姿依赖、位姿失败退化画布、全局全景换精度、手工课程、2D 位置编码骨干假设、单骨干实验；续文在 page 10 开头。
- Quote: “Limitations. OneCanvas requires depth and camera poses, which pure RGB methods avoid, and pose-estimation failures can still degrade the canvas, though feed-forward metric reconstruction is narrowing this gap. The single global panorama trades fine spatial precision for compactness and”
- Authors: bartomiej-baranowski; dave-zhenyu-chen; matthias-niener

### LR-FISHEYE-2026-1404

- Claim: 单镜头全景相机的结构性局限（本文定位）：提供全 FoV 但缺乏基线约束做可靠尺度估计，被迫依赖噪声 IMU 尺度线索，导致尺度不稳与长期漂移——与多相机 rig 的基线约束形成路线级对比。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 1, Section I. Introduction
- Evidence: Introduction 对 single-lens panoramic cameras 的直接评述；[9] 即本批 PanoAir（2604.00852），其自报 UAV 基准带度量尺度 100% 成功——构成对照。
- Quote: “Single-lens panoramic cameras [9], [10], [11] provide full FOV but lack baseline constraints for reliable scale estimation, forcing reliance on noisy IMU scale cues and leading to un- stable scale and long-term drift.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1417

- Claim: 作者自述核心局限：作为纯 VIO 系统无回环，存在长期漂移；未来工作引入轻量回环扩展为完整 SLAM，同时保持 CPU-only 效率与多相机适应性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 8, Section V
- Evidence: V. Conclusion and Future Work 末句直接自述；与 IV-A 评测协议（基线回环全关、SE(3) 对齐）互证。
- Quote: “As a pure VIO system, it lacks loop closure and suffers from long-term drift. Future work will incorporate lightweight loop closure to extend it to a complete SLAM system while preserving its CPU-only efficiency and multi-camera adaptability.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-1418

- Claim: 作者自述自建数据集的硬件局限：ATE 略高于公共数据集的两个原因——5 cm 立体基线（标准数据集的一半）降低三角化精度；偶发重复 IMU 时间戳引入噪声。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 5, Section IV-C1
- Evidence: IV-C1 末段硬件限制说明；同段'Despite these challenges, our method outperforms all baselines'。
- Quote: “SE(3)-aligned ATE RMSE is slightly higher than on public datasets due to two hardware limitations: a 5 cm stereo baseline, half that of standard datasets, degrading triangulation accuracy, and occasional duplicate IMU times- tamps introducing noise.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-0519

- Claim: 本文在 Introduction 中明确列举 UMI 原版手持采集的保真度缺陷（本卡摘录覆盖其中三项）：跨相机共视重建的双手相对位姿在协调任务上引入误差、软件/无线时间对齐、以及每手单个 155° 腕鱼眼留下盲区与弱深度线索——单鱼眼窄 FoV 被作者列为待修复缺陷而非可接受配置。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 2, Section 1 Introduction
- Evidence: Introduction 列举现行手持采集的保真度缺陷链（完整列表另含页 1 的视觉(-惯性) SLAM 位姿漂移项，不在本摘录内），本摘录覆盖共视重建相对位姿、软件时间对齐与单 155° 腕鱼眼盲区三项，末项直指 one 155° wrist fisheye per hand 的盲区与深度线索问题。
- Quote: “is reconstructed from cross-camera co-visibility rather than measured natively, introducing error precisely on the coordinated tasks where it matters most; sensor streams use software or wireless alignment rather than hardware triggers; and one 155 ◦ wrist fisheye per hand leaves blind spots and weak depth cues [6, 9].”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0530

- Claim: 作者明确声明保真度整体验证未分解：轨迹精度、双手相对位姿、同步与 FoV 作为联合设计原则实现，未通过受控降解隔离各因素；结果只证明高保真充分、不说明部署级策略需要每项属性多少——FoV（含 200° 双鱼眼配置）的边际贡献未被量化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 29, Section 7 Limitations, Fidelity is validated as a whole, not decomposed
- Evidence: Sec. 7 Limitations 第三条：fidelity as a design principle / no controlled degradation / high fidelity suffices but not how much of each property。
- Quote: “We treat fidelity as a design principle realized jointly by trajectory accuracy, inter-gripper relative pose, synchronization, and field of view, and we do not isolate these factors through controlled degradation.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0531

- Claim: 作者明确声明 parity 对比非样本匹配：无预训练时 UMI-only post-training 使用约十倍于遥操作基线的演示量，结论是实用数据生产管线对比而非每轨迹数据效率——鱼眼腕视图的平价结论应在此口径下引用。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 29, Section 7 Limitations, Data efficiency and transfer across post-training sources
- Evidence: Sec. 7 Limitations 第四条：not sample-matched / roughly ten times as many demonstrations / practical data-production pipelines。
- Quote: “Our parity comparison is not sample- matched: without pre-training, UMI-only post-training uses roughly ten times as many demonstrations as the teleoperation baseline, so the result compares practical data-production pipelines rather than per-trajectory efficiency.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0532

- Claim: 作者明确声明评估范围限制：零机器人 post-training 证据仅覆盖四个桌面双臂任务与三个 backbone（场景级分布偏移下），对其他任务、本体与偏移的普适性未测试；预训练证据更窄，仅在 StarVLA-QwenPI 上测量。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 28, Section 7 Limitations, Evaluation scope and generality
- Evidence: Sec. 7 Limitations 第一条：four tabletop bimanual tasks and three backbones / generality remains untested / pre-training evidence narrower。
- Quote: “Our zero-robot post-training evidence covers four tabletop bimanual tasks and three backbones under scene-level distribution shift; its generality to other tasks, embodiments, and shifts remains untested. The pre-training evidence is narrower: scaling and downstream gains are measured only on StarVLA-QwenPI.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0533

- Claim: （读者推断）『每手双非平行鱼眼 200°』的 FoV 主张缺三个可核验细节：鱼眼相机型号/分辨率/畸变模型未披露、图像进入策略前的几何预处理（是否去畸变/如何标定）未描述、且没有任何 FoV 变量消融——超广角配置对策略性能的净贡献与轨迹精度/同步/样本量不可分离，论文自己也承认不知道每项属性需要多少。
- Stance: `limit` | Confidence: `inference`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: page 8, Section 3.1.3 and page 29, Section 7 Limitations
- Evidence: Sec. 3.1.3 仅有覆盖度数描述；全文无相机型号/内参/去畸变流程；作者在 Sec. 7 自认 fidelity 未分解——三项缺失均为文本直接观察，联合推断已标注为读者推断。
- Quote: “Our results thus show that high fidelity suffices, but not how much of each property a deployable policy requires. A systematic ablation—selectively degrading each factor while holding sample count and scene coverage fixed—would quantify its marginal contribution and turn “high fidelity helps” into an actionable specification of the fidelity required for deployment.”
- Authors: yuteng-wei; jinming-ma; jiawei-wang; et al.

### LR-FISHEYE-2026-0739

- Claim: 作者自述局限：(1) X-Lens 动态接受任意内外参作为几何输入，但严格依赖真值标定、缺乏在线联合预测这些相机配置的能力；(2) 泛化方面，系统虽能跨多样相机设置泛化，但底层合成训练数据只覆盖有界的相机内参变化范围，遇到偏离训练分布的极端 FOV 未见鱼眼镜头模型时存在明显 sim-to-real gap、性能轻微退化；未来工作将扩大真实数据与内参多样性、增加时序聚合，并探索 X-Lens 作为世界模型、SLAM 与机器人 loco-manipulation 的几何先验。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 15, Section 7 Conclusion (Limitations)
- Evidence: 标定依赖与 Fisheye3R 的假设一致（两者都把内外参当输入而非输出），说明这是当前鱼眼适配/异构建模路线的共同前提而非 X-Lens 独有缺陷；极端 FOV sim-to-real gap 与训练构成（Stage-2/3 主要依赖合成 OmniScene）互为因果。
- Quote: “Limitations. X-Lens dynamically accepts arbitrary intrinsic and extrinsic parameters as geometric inputs; however, it strictly relies on ground-truth calibration and lacks the capability to jointly predict these configurations online. Regarding generalization, while the system generalizes across diverse camera setups, the underlying synthetic training data inherently covers a bounded range of camera intrinsic variations. Consequently, when encountering unseen fisheye lens models with extreme FOV”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0918

- Claim: 作者问题陈述：DUSt3R/MASt3R/VGGT/π³/DA3 等 3D 基础模型在针孔（pinhole）图像上可前馈产出强深度与位姿估计，但在鱼眼几何下急剧退化；作者将此失败部分归因于预训练位置编码中的针孔相机偏置（pinhole bias）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 1, Abstract
- Evidence: 摘要开篇陈述问题与归因：pinhole imagery 上强、fisheye geometry 下急剧退化，原因之一是位置编码的 pinhole bias。
- Quote: “Recent 3D foundation models, such as DUSt3R, MASt3R, VGGT, π 3 , and Depth Anything 3, provide strong feed-forward depth and pose estimates on pinhole imagery, but degrade sharply under fisheye camera geometry. We show that this failure is partly caused by a pinhole camera bias in the positional encodings of pretrained 3D foundation models, and propose RayTun3R,”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-0931

- Claim: 作者自述限制（五条）：(i) 计算的是相机特定修正，换鱼眼相机或畸变档案需重新适配；(ii) 假设主点与以径向为主的畸变，不显式覆盖强切向/非径向光学；(iii) 需要相机参数（AnyCalib 预测标定可用但精度受限）；(iv) 只针对鱼眼图像，全景/equirectangular 输入留作未来工作；(v) 训练集需要足够帧间位移，小/退化运动下自监督约束变弱。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.02711](https://arxiv.org/abs/2607.02711) RayTun3R: Online Camera Adaptation in 3D Foundation Models
- Locator: page 9, Section 6 Conclusion and Limitations
- Evidence: Section 6 Limitations 原文逐字给出五条编号限制。
- Quote: “Limitations. (i) RayTun3R computes a camera-specific correction; a different fisheye camera or distortion profile requires new adaptation. (ii) RayTun3R assumes a principal point and mostly radial distortion; it does not explicitly cover strong tangential or non-radial optics. (iii) RayTun3R requires camera parameters, although Sec. B shows that predicted calibration from off-the-shelf networks such as AnyCalib [23] remains accurate. (iv) Our work focuses on fisheye images. Panoramic or equirect”
- Authors: daniil-sinitsyn; nikita-araslanov; daniel-cremers

### LR-FISHEYE-2026-1153

- Claim: 在受控合成实验中，标定失败率随 FoV 增大骤增：180° 时仅 0-3%，220° 时 36-67%，240° 时 59-88%（依 stereo 相对旋转配置而异）；且失败时几乎全部（75-100%）可归因于内参初始化阶段而非后续联合优化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 3, Table I, Section III-B
- Evidence: Table I 报告 16 配置（4 相对旋转×4 FoV）的失败率与失败中内参初始化占比：FoV180 0-3%/0-100%；FoV220 36-67%/98.5-100%；FoV240 59-88%/98.9-100%；正文总结窄 FoV 失败罕见、宽 FoV 骤增、几乎全部失败源自内参初始化。
- Quote: “Failures are rare at narrower FoVs but increase sharply for wide-FoV settings; when calibration fails, almost all failed trials originate from intrinsic initialization.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1154

- Claim: 反直觉对照实验：把检测到的标靶点替换为完整真值（GT）观测后重跑同一标定管线，总成功率反而从 68.1% 降到 53.7%、多数宽 FoV 配置更不稳定——说明多鱼眼标定失败不能由低检测召回或外周观测不足解释，完整观测反而暴露底层优化不稳定性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 3, Table II, Section III-C
- Evidence: Table II 对比几何检测观测与全 GT 观测的成功率（每格 geometry/GT）：总体 68.1%/53.7%，宽 FoV 配置 GT 下更差（如 FoV240-0：12%/2%）；正文解释失败不能仅由低召回或外周样本不足解释。
- Quote: “Table II shows the opposite: the success rate drops from 68.1% to 53.7%, and most wide-FoV settings become less stable. Thus, calibration failure cannot be explained by low recall or insufficient peripheral sample count alone; full observations can instead expose the underlying optimization instability.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-1166

- Claim: 方法代价（作者承认）：在 FoV180-220 的若干配置上 CO-Calib 的位姿估计误差（ATE）略高于 Kalibr，作者归因于选择策略使用更少帧做优化、可能减少相机位姿估计可用的轨迹覆盖——帧选择的鲁棒性收益以部分位姿估计精度为代价。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.05777](https://arxiv.org/abs/2607.05777) Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis
- Locator: page 6, Section V-C; page 7, Table V
- Evidence: V-C：FoV180-220 若干配置 CO-Calib 的 ATE 略高（Table V 如 FoV180-0：4.30 vs 3.14），作者解释为选择策略用更少帧、减少位姿估计的轨迹覆盖；同时选中帧提供更好几何约束使外参更准。
- Quote: “For several configurations from FoV180 to FoV220, CO-Calib shows a slightly higher pose estimation error than Kalibr. This is mainly because the proposed selection strategy uses fewer frames for optimization, which may reduce the trajectory coverage available for camera pose estimation.”
- Authors: peize-liu; zhe-tong; chen-feng; et al.

### LR-FISHEYE-2026-0253

- Claim: 相机中心几何监督以每数据源的相机标定和度量深度为前提：当度量深度或相机标定信息不可用时，相应的相机坐标分量被标记为不可用而非被当作有效几何目标（经 loss mask 旁路）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 9, Section 4.2 Camera-Centric Action Space
- Evidence: Section 4.2 明确写出不可用分量的处理策略：marked unavailable rather than treated as valid geometric targets；这与 method 假设（标定+深度可得）和作者限制（标定误差传播）构成同一约束链。
- Quote: “When metric depth or camera calibration information is unavailable, the corresponding camera-frame components are marked unavailable rather than treated as valid geometric targets.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0254

- Claim: 作者明确声明：相机标定、深度估计、本体运动学或 MediaPipe 手部关键点定位的误差会传播进相机中心目标和下游翻译器——几何信息必须被可靠估计或标定是该方法的刚性依赖。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 14, Section 6 Conclusion and Limitations
- Evidence: Section 6 Limitations 第一条：UCAG-P relies on geometric information that must be estimated or calibrated reliably；附录 D（page 30）重复该限制并把失败案例归因于锚点检测、轨迹预测与动作翻译错误。
- Quote: “Errors in camera calibration, depth estimation, embodiment kinematics, or MediaPipe hand-keypoint localization can propagate into the camera-centric target and the downstream translator.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0255

- Claim: 在 LIBERO-Plus 七类分布偏移下，相机偏移是相机中心策略的最弱类别：UCAG-P 零样本相机扰动成功率 51.2%，远低于机器人状态 92.8%、光照 98.9%、背景 98.0%（语言 83.5%、噪声 75.2%、布局 74.3%，总均分 82.0%）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 13, Table 4
- Evidence: Table 4 报告 UCAG-P 零样本七类扰动成功率（Camera 51.2 / Robot 92.8 / Lang. 83.5 / Light 98.9 / Bkg. 98.0 / Noise 75.2 / Layout 74.3 / Avg. 82.0）；正文说明其对 robot-state、lighting、background 扰动尤其鲁棒，而 camera、sensor-noise、object-layout 更具挑战。
- Quote: “UCAG-P Zero-shot 51.2 92.8 83.5 98.9 98.0 75.2 74.3 82.0”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0258

- Claim: 直接本体替换（RoboTwin 中 ALOHA→ARX，固定场景/物体布局/扰动种子/相机外参，IK 对齐初始末端位姿）后 UCAG-P 零样本成功率 35.0%，远低于源本体 ALOHA 的 88.66%（Easy）/89.20%（Hard）——相机中心运动本身不能消除形态学与运动学失配。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 13, Section 5.2b
- Evidence: Section 5.2b 报告 ARX 替换实验：35.0% 成功率、显著低于源本体性能但仍是零样本直接替换迁移；Table B.1（page 25）给出对照数字 88.66/89.20/35.0；作者据此说明 camera-centric motion 提供可迁移中间目标但形态学/运动学失配仍是开放挑战。
- Quote: “UCAG-P achieves 35.0% success, which is substantially below the source-embodiment performance, but it is still zero-shot transfer under a direct embodiment replacement. The result suggests that camera-centric motion provides a transferable intermediate target, while also showing that morphology and kinematic mismatch remain open challenges.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0261

- Claim: 作者声明真机评估是刻意受控且规模有限的：实验支持 human-to-robot 迁移和数据高效 SFT 适配，但更广泛的真机鲁棒性需要跨更多机器人、相机设置、物体类别和长程任务的评估。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.26058](https://arxiv.org/abs/2608.26058) One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation
- Locator: page 14, Section 6 Conclusion and Limitations
- Evidence: Section 6 Limitations 第三条：real-world evaluation is intentionally controlled and limited in scale；附录 D（page 30）复述同一条并强调需评估更多相机设置。
- Quote: “Our real-world evaluation is intentionally controlled and limited in scale. The experiments support human-to-robot transfer and data-efficient SFT adaptation, but broader real-world robustness requires evaluation across more robots, camera setups, object categories, and long-horizon tasks.”
- Authors: shaoqing-xu; fang-li; guozhi-zhan; et al.

### LR-FISHEYE-2026-0304

- Claim: 作者论证局部观察的根本局限：前视与腕装相机虽提供高分辨率操作线索，但视场天然受限；在长程移动操作任务中，底盘平移与旋转叠加机械臂自遮挡，会频繁导致目标物体、地标或目标区域从局部视野中消失——这是引入全景观测的核心动机。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 1, Section I, Introduction (second challenge)
- Evidence: 引言第二个挑战段：conventional local observations 受限视场 + 基座运动与自遮挡使目标频繁离开局部视野；作者据此主张用全景成像提供环境全向观察。
- Quote: “The second challenge lies in achieving robust visual perception during robot motion. Conventional local obser- vations, such as front-facing and wrist-mounted cameras, provide high-resolution manipulation cues but are inherently constrained by limited fields of view. In long-horizon mobile manipulation tasks, base translation and rotation, together with self-occlusion from the robot arms, can frequently cause target objects, landmarks, or goal regions to disappear from these local views.”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0305

- Claim: 全景图像具有独特的非透视畸变，与常规预训练视觉编码器形成显著域差距：直接套用标准视觉表征往往导致特征质量退化与语义信息保留不足——这促使作者开发专门的 panorama-aware 表征与融合架构，把全景观测与多模态输入整合并显式建模机器人中心全局上下文。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 1, Section I, Introduction
- Evidence: 引言段：panoramic images exhibit distinctive non-perspective distortions，与 pretraining conventional visual encoders 的域差距使直接套用标准表征导致 degraded feature quality and limited preservation of semantic information，因此 motivating panorama-aware representation and fusion architecture。
- Quote: “Nevertheless, panoramic images exhibit distinctive non-perspective distortions, creating a significant domain gap using the pretraining conventional visual encoders. As a result, directly applying standard visual representations often leads to degraded feature quality and limited preservation of semantic information. This motivates us to develop a panorama-aware representation and fusion architecture that integrates panoramic observations with mul- timodal inputs and explicitly models robot-cent”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0313

- Claim: 把全景重投影为多个透视视图再拼接（stacked-panorama：3 个光学轴按偏航 120° 均匀间隔的透视图拼接为复合图，page 5 基线定义）是另一种折中：它部分缓解 ERP 与透视图像编码器的不匹配，在 Wipe Table 上 SR 40.0% 高于 raw panorama 的 20.0%（透视重投影有利于操作密集阶段）；但在其余任务上低于 raw panorama 基线（平均 SCR 70.4% vs 80.8%，Tab. II），作者归因于透视裁剪可能削弱有利于机器人中心理解的跨视角连续性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 7, Section V-B (stacked-panorama analysis)
- Evidence: V-B 分析段讨论 stacked-panorama 基线的不同折中：manipulation-heavy 阶段受益于透视重投影，其余任务上透视裁剪削弱 cross-view continuity。
- Quote: “Reprojecting the panorama into perspective views intro- duces a different trade-off. The stacked-panorama baseline partially alleviates the mismatch between equirectangular panoramas and perspective-image encoders by decomposing the panorama into multiple perspective views. On Wipe Table, its observed SR is 40.0%, compared with 20.0% for raw panorama input, indicating that perspective reprojection can benefit manipulation-heavy stages. However, it under- performs the raw panorama baseline on the”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0315

- Claim: 全景专家容量在有限微调数据下存在甜点：50M 参数不足以捕捉跨视角依赖与目标方向线索（84.4% SCR / 60.0% SR）；100M 最优（95.6% / 86.7%）；超过 100M 不再带来一致的闭环改进（200M 93.3%/86.7%，300M 降至 91.1%/73.3%）；作者据此采用 100M 专家作为表征容量与数据高效微调之间的经验折中。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 7, Section V-C, Panorama expert scale and Table III
- Evidence: V-C 消融：Panorama expert scale 在 50M/100M/200M/300M 上扫描（Tab. III），结论是 100M 为最优折中。
- Quote: “TABLE III EFFECT OF EXPERT SIZE AND PANORAMA ENCODER SELECTION. Variant Expert Size SCR SR Expert size PanoVLA w/ MTPano 50M 84.4% 60.0% PanoVLA w/ MTPano 100M 95.6% 86.7% PanoVLA w/ MTPano 200M 93.3% 86.7% PanoVLA w/ MTPano 300M 91.1% 73.3% Panorama encoder PanoVLA w/ SigLIP 100M 75.6% 40.0% PanoVLA w/ MTPano 100M 95.6% 86.7% Panorama expert scale. We investigate the impact of panorama expert capacity by varying the parameter count as shown in Table III. These results suggest that the 50M exper”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0366

- Claim: 度量深度依赖（结构性限制）：主实验使用校准的度量深度（取自传感器或预校准估计器）；换成零样本 DepthAnything V2 即使做逐图像解析 scale/shift 标定也只得 44.5% SR——几何基底不再度量对齐，逐帧标定无法恢复式(5)所需的绝对尺度；在 50k LIBERO 帧上微调深度骨干（3 epochs）可弥合大部分差距至 71.7% SR（距 GT 深度上限 86.8% 仍差 15.1pp，比仅标定高 27.2pp）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 9, Section 5 (Depth substitution), Table 16
- Evidence: Section 5 Depth substitution：zero-shot DepthAnything V2 + per-image analytical scale/shift calibration → yields only 44.5% SR；A short fine-tune of the depth backbone on 50 k LIBERO frames (3 epochs) bridges most of this gap, reaching 71.7% SR (−15.1 pp from the GT-depth ceiling at 86.8% and +27.2 pp over calibration alone)；Table 16（page 20）显示更大编码器/精修头/端到端梯度均无法进一步改善。
- Quote: “GS-VLA depends on calibrated metric depth, taken from a sensor or pre- calibrated estimator in our main experiments. Replacing this with zero-shot DepthAnything V2 [36], even with per-image analytical scale/shift calibration, yields only 44.5% SR — the geometric base is no longer metric-aligned and per-frame calibration cannot recover the absolute scale required by (5). A short fine-tune of the depth backbone on 50 k LIBERO frames (3 epochs) bridges most of this gap, reaching 71.7% SR (−15.1 pp”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0367

- Claim: 作者自述限制（单视图输入）：规范化器只消费单源帧及其校准深度，源相机完全未观测的场景内容无法被 inpainter 恢复；作者预期多视图扩展（如融合腕装相机或前一帧）可在不改变底层 Locality 归约的前提下抬升该上限，留作未来工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 9, Section 6, Limitation (Single-view input)
- Evidence: Section 6 第一条限制：The canonicalizer in this paper consumes a single source frame and its calibrated depth, so any scene content that the source camera does not observe at all cannot be recovered by the in-painter；multi-view extension — for example, fusing a wrist-mounted camera or a previous-step frame — to lift this ceiling。
- Quote: “The canonicalizer in this paper consumes a single source frame and its calibrated depth, so any scene content that the source camera does not observe at all cannot be recovered by the in-painter. We expect a multi-view extension — for example, fusing a wrist-mounted camera or a previous-step frame — to lift this ceiling without changing the underlying Locality reduction, and we leave that direction to future work.”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0368

- Claim: 作者自述限制（旋转的 Locality 边界）：默认平移预算已很大（εt=100cm 相对约 0.7m 工作区），在其上叠加有意义的旋转常使相机整体转出工作区，因此无法在 Table 3 联合格之外做干净的旋转扫描；失败案例检查发现相当比例的采样相机视锥根本不含工作区——这标示的是所用扰动分布的实际天花板，而非规范化器本身的性质。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 9, Section 6, Limitation (Locality boundary on rotation)
- Evidence: Section 6 第二条限制：The translation budget in our default setting is already large (εt=100 cm relative to a ∼0.7 m workspace)... frequently rotates the camera off the workspace entirely；We could not run a clean rotation sweep beyond the joint (εt, θ) cells reported in Table 3；a non-trivial fraction of the sampled cameras do not contain the workspace inside their frustum at all... practical ceiling of the perturbation distribution we used rather than a property of the canonicalizer itself。
- Quote: “The translation budget in our default setting is already large (ε t =100 cm relative to a ∼ 0.7 m workspace), and adding meaningful rotation on top of such translations frequently rotates the camera off the workspace entirely. We could not run a clean rotation sweep beyond the joint (ε t , θ) cells reported in Table 3 for this reason. Inspecting the failure-case rollouts, we found that a non-trivial fraction of the sampled cameras do not contain the workspace inside their frustum at all, which m”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0369

- Claim: 作者自述限制（无真机验证）：本文全部实验在 LIBERO 仿真器内完成；真机验证需要外部度量深度源（承前一条）与搭建物理装置的工程投入，在项目资源与人力约束内无法完成；作者因此将仿真结果定位为"强但终究是初步的信号"，把真机复现视为自然的后续工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 9, Section 6, Limitation (Real-world evaluation)
- Evidence: Section 6 第三条限制：All experiments in this paper are run inside the LIBERO simulator；Validating GS-VLA on a real robot requires both an external metric-depth source... and the engineering effort to instrument a physical rig, neither of which we were able to put in place within the resource and personnel constraints；a strong but ultimately preliminary signal。
- Quote: “All experiments in this paper are run inside the LIBERO simulator. Val- idating GS-VLA on a real robot requires both an external metric-depth source (per the previous point) and the engineering effort to instrument a physical rig, neither of which we were able to put in place within the resource and personnel constraints of this project. We therefore report the simulator results as a strong but ultimately preliminary signal, and treat a real-robot replication as the natural follow-up.”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0371

- Claim: 读者推断（对鱼眼综述的适用边界）：该方法的形式化以针孔相机为前提——内参被定义为编码焦距与主点的 3×3 针孔矩阵 K，规范化器输入为单帧 RGB、逐像素度量深度、源/规范位姿与该针孔内参；结合 Locality 前提（扰动限于有界邻域、失配退化为 O(ρ) 薄带），把鱼眼/全景/超广角相机接入针孔训练视角不属于该方法已验证或声称的范围——FOV 跃变与径向畸变既不在针孔 K 的表达内，也会把"薄带剥离"变成大面积未观测/不可几何映射区域，超出 Locality 归约的前提。
- Stance: `limit` | Confidence: `inference`
- Paper: [2608.19066](https://arxiv.org/abs/2608.19066) GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting
- Locator: page 4, Section 3.2, Problem definition
- Evidence: 推断依据：page 4 问题定义逐字将内参限定为 pinhole matrix K（encodes the focal lengths and principal point），输入接口为 (Is, Ds, Cs, C*, K)；page 2 Locality 前提把有界邻域外的大视角变化排除（C02 已立卡）；全文无畸变模型/球面投影处理环节，光栅化配置为 45° 垂直 FOV（page 16, Table 9）。
- Quote: “The camera intrinsics are given by the pinhole matrix K ∈ R 3×3 , which encodes the focal lengths and principal point.”
- Authors: yechan-park; hyunjin-kim

### LR-FISHEYE-2026-0398

- Claim: 真机 held-out 增益的任务异质性显著：合笔记本盖任务在提出目标下近乎无损（30/30 held-out 成功），电池入箱从 17/30 提高到 23/30，而取耳机任务最差（FM-only 5/30 对提出方法 14/30），且增益随摆放几何激进程度增长（跨任务聚合差 H0 +4、H1 +6、H2 +9 个 rollout）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 7-8, Section 4.4 (per-placement detail: page 14, Section D.3)
- Evidence: 逐任务与逐摆放拆分显示增益集中在几何最激进的 held-out 摆放与最远视角，但耳机任务的失败模式（细带被遮挡、接近角小误差导致抓空）属于单 RGB 可观测性限制。
- Quote: “the Laptop lid task transfers nearly losslessly under the proposed objective (30/30 held-out), the Battery box task improves from 17/30 to 23/30, and the Headphone stand task carries the largest absolute gap, 5/30 to 14/30.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0399

- Claim: 作者明确声明方法存在配对数据刚性需求：真动作等价配对只能由仿真 MuJoCo 状态重置重渲染或硬件同步多相机获得，这排除大多数现有单相机机器人数据集（不同视图来自不同 rollout）；近似配对（独立采集轨迹）不安全——非等价状态间施加一致性会把逐状态速度预测拉向状态边缘均值并对抗监督流匹配信号（塌缩至 25.8% 实证确认）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 8, Section 5 Limitations (Paired training data)
- Evidence: 限制章节第一条说明配对需求与近似配对风险，并以 shuffle 塌缩作为机制证据；减少该需求被列为未来工作。
- Quote: “The method requires true action-equivalent pairs: in simulation by resetting MuJoCo states and rerendering, on hardware by synchronized cameras observing the same physical state at the same timestamp. This requirement excludes most existing single-camera robot datasets”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0400

- Claim: 作者明确声明单 RGB 可观测性上限：跨视角一致性只能改进同一状态跨视图的动作一致性，无法恢复输入 RGB 中不存在的视觉信息——当 held-out 相机遮挡任务关键几何或压缩接触附近的深度线索时，目标无锚可依；且部署契约刻意不含深度、点云、RGB-D 或触觉。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 8, Section 5 Limitations (Observability under single RGB)
- Evidence: 限制章节第二条明确把残留失败（耳机任务 16/30）归因于遮挡与深度歧义，并把与深度/点云/RGB-D/触觉的组合列为直接扩展方向。
- Quote: “Cross-view consistency improves action agreement across views of the same state but cannot recover information not visually present in the input RGB; when held- out cameras occlude task-critical geometry or compress depth cues near contact, the objective has nothing to anchor against.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0401

- Claim: 作者明确声明评估范围：真机研究刻意受控（3 个桌面任务、静态外置场景相机、3 seen + 3 held-out 摆放、每任务-摆放 cell 10 rollouts），不建立 LIBERO-Plus C1/C2/C3 之外、移动相机、光照变化、杂乱、透明/可变形物体或移动底盘操作的鲁棒性；向离散 token VLA 骨干与其他动作头族的迁移留作未来工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 8, Section 5 Limitations (Scope of evaluation); page 19, Appendix I
- Evidence: 限制章节第三条列出不覆盖条件；附录 I 补充跨 VLA 族迁移为未验证方向。
- Quote: “The hardware study is intentionally controlled: three tabletop tasks, static ex- ternal scene cameras, three seen and three held-out placements, and 10 rollouts per task—placement cell. It does not establish robustness beyond LIBERO-Plus C1/C2/C3 shifts, moving cameras, light- ing changes, clutter, transparent/deformable objects, or mobile-base manipulation.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0406

- Claim: 作者报告的探索性特征级替代方案全部失败：注入 VGGT 视图稳定 canonical token 的 corrected 版本仅达 15.3% 相机轨道成功率（与名义基线地板相当或更低），硬动作路径瓶颈变体 67.4% 低于同数据标准流匹配策略的 71.4%——视图不变特征不保证动作不变，一致性必须放在策略自己的动作流输出上。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 18, Appendix G
- Evidence: 附录 G 记录三次特征级尝试（canonical-token 注入、canonical 残差锚、动作路径瓶颈）及失败数字，并说明设计含义。
- Quote: “The cor- rected canonical-token injection run reached 15.3% camera-track success, comparable to or below the nominal-only floor.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0413

- Claim: 错误坐标一致性（把跨视角一致性施加于协变未来场景块）的危害被定量验证：受控共享主干去噪器收敛训练下，held-out 配对的归一化视图差比率在 λ∈{0.1,0.5,2.0} 测得 0.715/0.337/0.116，对 Proposition 1 预测值 0.714/0.333/0.111 相差在 10% 以内且随 λ 单调；2B WAM 上 2k 步错误坐标臂（除一致性额外加在协变未来场景块外与选择性运行全同）的 held-out 跨视角未来场景比塌缩至 0.18 并向 Proposition 1 渐近下降，而选择性运行与 λ=0 控制均保持约 0.98。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 4, Section IV-C, Figure 2
- Evidence: 收缩定律三层验证中的两层：受控合成实验（共享网络训练到达逐对最优）与 2B 模型 on-model 短程检查；作者声明 2B 模型上的全定量测量超出范围。
- Quote: “The measured ratios are 0.715, 0.337, and 0.116 at λ ∈ {0.1, 0.5, 2.0}, against predicted values 0.714, 0.333, and 0.111: within ten percent everywhere and monotone in λ. Shared-network training reaches the per-pair optimum here, so wrong-coordinate consistency collapses covariant content exactly as the algebra says. A full quantitative measurement of the law on the 2B model is out of scope; as a quali- tative on-model check we trained a short (2k-step) wrong- coordinate arm on the WAM itself, i”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0418

- Claim: 套件级异质性：主外推桶内部 spatial 套件提升 40.8 点而 object 套件回归 11.6 点；在预注册终点之外的复合极端方位角+仰角位移下 object 套件回归 40.4 点——没有任何单轴桶接近该失败量级。作者解读：不变块上的跨视角一致性约束末端执行器去向，而 object 中心套件强调的精细抓取几何在其 reach 之外，复合位移回归显示该交换可以为负。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 7, Section VII
- Evidence: VII 节如实报告桶内套件异质性与非预注册复合位移的负回归，并给出机制解读（抓取精度分量在目标 reach 外）。
- Quote: “The heterogeneity inside the primary extrapolation bucket is sharper—spatial improves by 40.8 points while object regresses by 11.6—and under a compound extreme azimuth-and-elevation shift outside the pre-registered endpoints the object suite regresses by 40.4 points, a failure no single-axis bucket approaches. The pattern admits a consistent reading: cross-view agreement on the invariant block constrains where the end-effector should go, while the fine grasp geometry that the object-centric sui”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0423

- Claim: 作者声明的数据前提限制：方法需要同状态跨视角配对——仿真中通过状态重置渲染很廉价，但真实世界需要同步多相机 rig 或配对数据集；扩展到近似匹配配对是未来工作（Proposition 2 背后的协方差分解提示一条路线）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 7, Section VIII Limitations (first paragraph)
- Evidence: 限制章节第一条：配对需求与近似配对开放性；仿真廉价性与真世界成本形成对照。
- Quote: “The method requires same-state cross-view pairs, which are cheap in simulation through state-reset rendering but demand synchronized multi-camera rigs or paired datasets in the real world; extending the analysis to approximately matched pairs is future work, and the covariance decom- position behind Proposition 2 suggests a route.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0424

- Claim: 作者声明的证据范围限制：本文全部闭环证据均为仿真（在公认公开基准上按披露协议）；同一一致性机制的流 VLA 实例化已迁移到真机 [7]、说明机制可迁移性，但 WAM 实例化的真机证据保持开放。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 8, Section VIII Limitations
- Evidence: 限制章节第二条：仿真闭环+流 VLA 真机间接证据+WAM 真机开放的三段式声明。
- Quote: “loop evidence in this paper is likewise simulated, on a recognized public benchmark under a disclosed protocol; the flow-VLA instantiation of the same consistency mech- anism has transferred to a real robot [7], which speaks to the mechanism’s transferability; real-robot evidence for the WAM instantiation remains open.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-1106

- Claim: AUC 表象下的精度崩塌：跨数据集 AP/F1 大幅下降——HUI360 训练的 LSTM 在 HUI360 Test 上 AP 0.60/F1 0.61，零样本到 SSUP-A Test 后 AP 仅 0.16、F1 0.23；SSUP-A 训练的 LSTM 原生 SSUP-A Test 为 AP 0.24/F1 0.26、零样本到 HUI360 Test 反而 AP 0.50/F1 0.50；作者指出类别不平衡（尤其 SSUP-A）使该影响在 AP/F1 上比 AUC 更可见——跨平台交互预期的正类查准率仍接近不可用水平。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 7, Table IV（不平衡比例 0.19/0.03 见 page 6, Section IV-A）
- Evidence: Section IV-A（page 6）说明 AP/F1 报告动机与类别不平衡；Table IV 给出三基线 AP 与 F1@0.5 的 in/cross-dataset 全矩阵。
- Quote: “TABLE IV AVERAGE PRECISION AND F1-SCORE (AT 0.5) OF MLP, RF AND LSTM IN IN-DATASET AND CROSS-DATASET EVALUATION HUI360 Test SSUP-A Test RF MLP LSTM RF MLP LSTM AP HUI360 Train 0.48 0.53 0.60 0.14 0.12 0.16 SSUP-A Train 0.33 0.49 0.50 0.16 0.21 0.24 F1-Score HUI360 Train 0.45 0.57 0.61 0.06 0.20 0.23 SSUP-A Train 0.39 0.44 0.50 0.23 0.24 0.26”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1110

- Claim: 作者自述定义局限：以'与平台物理接触'为操作化交互定义只覆盖 HRI 行为谱的子集，未显式建模前接触社会信号（gaze、hesitation、verbal engagement、approach-and-stop）——这是可扩展性与语义丰富度的权衡：客观可自动测量的判据换来大规模可复现标注，但限制了可捕捉的交互范围；作者将 HUI360 定位为 foundation 而非完整定义。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 8, Section V Conclusion 末两段
- Evidence: 结论末段明确操作化定义的子集性质、未建模的前接触信号与可扩展性-语义丰富度权衡。
- Quote: “We acknowledge that the operational definition of inter- action adopted in HUI360, based on physical contact with the platform, captures only a subset of the rich spectrum of human-robot interaction behaviors. In particular, it does not explicitly model pre-contact social signals such as gaze, hes- itation, verbal engagement, or approach-and-stop behaviors, which may also convey interaction intent. This design choice reflects a trade-off between scalability and semantic richness. While objective”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-1111

- Claim: 基线与全景表示均未充分开发：作者自述当前基线 architecturally basic（RF/MLP/LSTM），把'利用 equirectangular 图像的特有性质'、更丰富的时空建模与社交/群体动态列为未来方向——即全景输入目前只被当普通特征源处理，其角坐标/环绕几何尚未转化为模型归纳偏置，全景 ego 数据的独特价值未被基线兑现。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.11051](https://arxiv.org/abs/2608.11051) HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation
- Locator: page 8, Section V Conclusion
- Evidence: 结论段：baselines architecturally basic；leveraging the specific characteristics of equirectangular imagery 列为 open direction。
- Quote: “While the current baselines are architecturally basic, they open promising directions whether it is exploring richer temporal and spatial modeling, leveraging the specific char- acteristics of equirectangular imagery, or incorporating social and group dynamics. In this sense, HUI360 represents not only a significant step toward practical and generalizable human-robot interaction anticipation, but also an important resource for future research in socially aware robotics and anticipatory perceptio”
- Authors: raphael-lorenzo-louis; fabio-amadio; bertrand-luvison; et al.

### LR-FISHEYE-2026-0657

- Claim: 在 class-wise IoU 上，SphereOcc 在 Person 与 Bike 两类不排名第一（Person 3.02%、Bike 7.50%），虽较 SurroundOcc（1.65%、5.16%）分别相对提升 83.0% 与 45.3%，但绝对 IoU 水平仍然很低。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 9, Table 3 and Section 5.1.1
- Evidence: Table 3 class-wise 结果：Person 最优为 TPVFormer 4.07、Bike 最优为 TPVFormer 8.54（表中数值），SphereOcc 3.02/7.50 未夺冠；正文明确 does not rank first for Person and Bike 并给出相对 SurroundOcc 的提升。
- Quote: “Although it does not rank first for Person and Bike, it improves their IoUs over SurroundOcc by 83.0% (3.02% vs. 1.65%) and 45.3% (7.50% vs. 5.16%), respectively.”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0661

- Claim: 按垂直体素高度分层的评估（Table 7）：全部方法在最上分层（12–15，top）与最下分层（0–3，bottom）的性能远低于中间层——SphereOcc 顶层 mIoU 3.20/GeoIoU 12.63、底层 mIoU 3.85/GeoIoU 6.99，而中间两层（8–11、4–7）mIoU 为 14.18 与 13.57；对比方法（TPVFormer/SurroundOcc/MonoScene/QuadricFormer）在顶层 mIoU 仅 2.49–2.97、底层 1.19–3.06。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 14, Table 7
- Evidence: Table 7 垂直分区：12–15（top）/8–11/4–7/0–3（bottom）四层五方法对比；top/bottom 层 mIoU 全部低于 3.2/3.9，与中间层差距一个数量级；page 12 Sec 6.2 称这些为 sparsely observed top and bottom regions。
- Quote: “Vertical 12–15 mIoU 2.56 2.97 2.49 2.83 3.20 GeoIoU 10.41 11.73 10.25 8.93 12.63 8–11 mIoU 12.88 12.27 11.87 11.23 14.18 GeoIoU 20.56 20.67 19.74 18.89 22.48 4–7 mIoU 11.28 11.50 10.38 10.98 13.57 GeoIoU 30.00 30.51 29.68 28.87 33.14 0–3 mIoU 1.71 3.06 1.19 2.57 3.85 GeoIoU 2.28 5.67 1.69 4.47 6.99”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0663

- Claim: 在 3D 目标检测基准上，最优方法 SparseBEV 的整体 mAP 仅 0.1689、NDS 仅 0.1221；检测性能在五类场景间变化显著（结构受限场景更高、功能性与乡村场景更低），对比方法频繁出现漏检或定位不准；作者据此指出球面 3D 目标检测仍对场景结构与物体分布敏感，从角坐标球面观测恢复度量笛卡尔 3D 空间中的物体位置依然困难。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 10, Section 5.2 and Table 5 (page 12)
- Evidence: Table 5 九方法对比：SparseBEV mAP 0.1689/NDS 0.1221 最佳；场景间差异大（Struc. mAP 0.3175 vs Funct. 0.0531，Table 5/page 12）；正文结论 spherical 3D object detection remains sensitive to scene structure and object distribution。
- Quote: “For 3D object detec- tion, Table 5 shows that SparseBEV [91] achieves the best overall performance, with an mAP of 0.1689 and an NDS of 0.1221, followed by PolarBEVDet [99]. SparseBEV also performs best in expressway, rural, structurally constrained, and urban scenes, whereas PD-BEV [101] performs best in functional scenes. Performance varies substantially across the five scene categories, with higher detection accuracy in structurally constrained scenes and lower accuracy in functional and rura”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0665

- Claim: 作者列举 Spheriverse 中的代表性挑战场景：车辆伪装与罕见乡村内容（温室、牲畜）引入语义歧义与长尾外观变化；曲面/高架/多层结构使角观测与度量 3D 空间的几何对应复杂化；低光照、高 ISO 增益、局部曝光变化与镜头污染在球面图像上造成空间非均匀退化——这些因素常同时出现，对语义识别与几何重建构成复合挑战。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 13, Section 6.4 and Fig. 8
- Evidence: Sec 6.4 与 Fig. 8 归纳五类挑战（伪装、乡村温室/牲畜、低光高 ISO、复杂几何、局部光照与镜头污染），并强调 compound challenges。
- Quote: “First, vehicle camouflage and uncommon rural content, such as greenhouses and live- stock, introduce substantial semantic ambiguity and long- tail appearance variations. Second, curved, overhead, and multi-level structures complicate the geometric correspon- dence between angular observations and metric 3D space. Third, low illumination, high ISO gain, local exposure variations, and lens contamination cause spatially non- uniform degradation across spherical images. These factors frequently occu”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-1068

- Claim: 嵌入式代价（质量-效率权衡的限制面）：在严格 20 Hz 四鱼眼输入下 Ours 维持 19.99 frames/s、0.026% 定时丢帧，但 P50/P95 延迟为 42.32/71.88 ms、50 ms 及时输出率仅 71.04%、平均模块输入功率 13.29 W——相对 Global Radius 功率从 12.31 W 增至 13.29 W、P95 延迟从 29.40 ms 增至 71.88 ms；而 Fixed Depth 为 20.54/24.73 ms、100% 及时、10.92 W。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 9, Section V-C 与 Table VI
- Evidence: Section V-C 与 Table VI 报告四配置在 Jetson Orin NX 上的完整路径延迟/吞吐/及时率/丢帧/功率/内存（每条件 3 次重复、轮换顺序、剔除前 10 s）。
- Quote: “Relative to Global Radius, Ours increases mean module-input power from 12.31 to 13.29 W and P95 latency from 29.40 to 71.88 ms. Both retain 19.99 frames/s with 0.026% cross- condition timed drops, but their 50 ms timely-output rates are 99.92% and 71.04%, respectively. The maximum measured junction temperature is 59.3 ◦ C. Together, output rate and the separate 50 ms timely-output metric define the verified quality– efficiency operating point.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1072

- Claim: 时间策略与结构连续性的权衡：相对 Immediate，Ours 的半径状态切换数在近/远场分别减少 69.4%/68.4%（49→15、19→6 次）；但近场线结构连续性上 Default（Ours）为 50.8%，低于 Two-confirmation 的 51.8%（-0.99 pp）与固定方法（Fixed Depth 55.8%、Global Radius 56.1%），仅高于 Immediate 的 50.6%（+0.25 pp）和 Fixed Feather 的 27.4%——自适应时间策略以小幅结构连续性损失换取状态响应性，固定深度方法在该指标上反而更高。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 8, Table V 与 Fig. 5(a)（正文 '50.8%/51.8%/27.4%' 段在 page 7）
- Evidence: Section V-B 与 Table V 报告时间策略单变量消融的切换数与结构连续性差值；Fig. 5(a) 标签给出各方法近场结构保持率与每帧保留段数。
- Quote: “27.4% \| 2.82/frame 55.8% \| 6.92/frame 56.1% \| 6.75/frame 51.8% \| 5.94/frame 50.6% \| 5.85/frame 50.8% \| 5.76/frame”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1073

- Claim: 作者自述限制：当前公式对每个重叠区只建模一个主导深度，在混合深度内容与实时资源约束下仍然受限——这两点边界促使其提出更丰富的局部场景模型（同时保持开放原始视图与标定接口）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 9, Section VI Conclusion 末段
- Evidence: 结论段明确 one dominant depth per overlap 与 mixed-depth content、real-time resource constraints 两项限制。
- Quote: “The present formulation models one dominant depth per overlap and remains limited by mixed-depth content and real-time resource constraints. These boundaries motivate richer local scene models that preserve the open raw-view and calibration interfaces while extending downstream aerial perception and localization.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1074

- Claim: 作者自述的下游证据边界：冻结检测与 VPR 在未适配 ERP 的常规图像训练模型下只提供互补的接口证据，不能确立检测器精度、通用表示排序或 ERP 图像的内在下游优势；结果同时揭示质量-效率权衡（扇区密度、时间自适应与嵌入式成本应按任务与算力预算选择）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 9, Section VI Conclusion
- Evidence: 结论段两处限定：frozen 下游证据的 scope 与 quality–efficiency trade-off 的任务依赖性。
- Quote: “Frozen detection and VPR provide complementary interface evidence under conventional-image-trained models that were not adapted to ERP inputs. They do not establish detector accuracy, a universal representation ranking, or an intrinsic downstream advantage of ERP imagery.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

### LR-FISHEYE-2026-1119

- Claim: 应用空白：新传感器（360 相机）遇上新时代（具身 AI），工业等原场景将迎来技术迭代，但不同场景特性与优先级各异、催生大量场景特异性子领域；因跨学科人才缺乏与既有全景数据/模型不足，全景生产安全巡检、全景森林火情检测等子领域目前缺乏充分探索。
- Stance: `gap` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 2, Motivation & Problem Space（Application Blanks 段）
- Evidence: 问题空间'应用空白'段：场景特异性子领域、跨学科人才缺乏、全景生产安全巡检与森林火情检测缺乏探索。
- Quote: “Application Blanks: When new sensors (360 cameras) meet a new era (embodied AI), many original scenarios, such as industrial scenarios, are likely to experience new technological iterations. However, different application sce- narios exhibit distinct characteristics and priorities, which have spawned numerous scenario-specific research sub- fields. This has given rise to numerous sub-fields of re- search that are scenario-specific. Due to the lack of interdis- ciplinary talents and the insuffici”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1124

- Claim: 数据集层面的两个缺口：近期数据集渐把几何真值与下游任务结合（Matterport3D/ReplicaPano/HM3D 配实例或任务级标签），时间性与具身采集也在变多；但完全同步的多传感器全景采集（全景 RGB+LiDAR+空间音频+行为轨迹）仍然罕见；QA 式全景推理基准刚开始出现（OSR-Bench/OmniVQA），推理导向的全景评测资源仍处初生阶段——同时社区已开始关注投影诱导畸变并用畸变感知方法/损失缓解纬度/极点伪影。
- Stance: `gap` | Confidence: `direct`
- Paper: [2509.12989](https://arxiv.org/abs/2509.12989) PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era
- Locator: page 3, Table 1 后总结段
- Evidence: Table 1 后总结段：几何真值+下游任务结合、时间/具身采集渐多、多传感器同步全景采集罕见、畸变感知方法出现、QA 式基准初生（nascent）。
- Quote: “Recent datasets increasingly combine geometric ground truth with downstream tasks. For example, Matter- port3D (Chang et al. 2017), ReplicaPano (Dong et al. 2024), and HM3D (Ramakrishnan et al. 2021) illustrate datasets that pair panoramas/depth/layouts with instance or task-level labels. Temporal and embodied captures are be- coming more common (Xia et al. 2018). However, fully synchronized multi-sensor panoptic collections that com- bine panoramic RGB, LiDAR, spatial audio, and behav- ioral tr”
- Authors: xu-zheng; chenfei-liao; ziqiao-weng; et al.

### LR-FISHEYE-2026-1209

- Claim: 空白定位：Semantic-SuPer 等把深度估计、语义分割与工具位姿信息结合创建分割手术场景的方法只在开集（open access）腹腔镜设置测试、未实现于内窥镜；本文把实时 3D 重建与深度学习模型获取的语义目标信息结合，实现内窥镜手术中快速准确的场景理解、支撑手术自动化等下游任务；据作者所知，本研究是首个将实时 SLAM 方法用于 CAO（中央气道阻塞）与 BPH（良性前列腺增生）的工作。
- Stance: `gap` | Confidence: `direct`
- Paper: [2509.13541](https://arxiv.org/abs/2509.13541) PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM
- Locator: page 3, Section 2 Background and Related Work
- Evidence: page 3 Section 2 末段：Semantic-SuPer 仅 open access laparoscopy 未用于 endoscopy；"the first to use real-time SLAM methods for CAO and BPH"。
- Quote: “Methods such as Semantic-SuPer bring together information from depth estimation, semantic segmentation, and tool poses to create segmented surgical scenes [18]. This method is tested only on an open access laparoscopy setup and not implemented for endoscopy. In this study, we combine the real-time 3D reconstructions with semantic target information acquired from a deep learning model. This allows fast and accurate scene understanding in endoscopic surgeries, enabling downstream tasks such as sur”
- Authors: ayberk-acar; fangjie-li; susheela-sharma-stern; et al.

### LR-FISHEYE-2026-1236

- Claim: 作者明确指出领域空白：多相机系统虽已在视觉 SLAM 中被探索（MIMC-VINS、多鱼眼的 BAMF-SLAM、LF-VIO/LF-VISLAM、MAVIS 等），但其与 LiDAR 和惯性数据的紧耦合集成在 LIVO 系统中仍未被充分研究——Omni-LIVO 即为填补该空白的工作；相关工作进一步说明既有 VI 域多相机系统不利用 LiDAR 几何结构、既有 LIVO 普遍采用单相机配置限制宽 FoV LiDAR 几何的全面利用。
- Stance: `gap` | Confidence: `direct`
- Paper: [2509.15673](https://arxiv.org/abs/2509.15673) Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion
- Locator: page 1, Section I Introduction; page 2, Sections II-B and II-C
- Evidence: 引言与相关工作（II-B/II-C）分别陈述 LIVO 侧单相机现状与 VI 侧多相机现状，构成本文的问题定位与贡献声明依据。
- Quote: “While multi-camera systems have been explored in visual SLAM [9], [10], their tight integration with LiDAR and inertial data in LIVO systems remains underexplored.”
- Authors: yinong-cao; chenyang-zhang; xin-he; et al.

### LR-FISHEYE-2026-0496

- Claim: 规格披露缺口（读者推断）：论文对鱼眼相机的全部描述仅为'高分辨率、广角鱼眼 RGB 图像（GoPro 鱼眼相机）'与'多视角腕装鱼眼图像'，未披露视场角数值、分辨率、畸变模型或去畸变处理流程；全文 9 页无任何鱼眼畸变处理或相机标定细节——无法判断策略消费的是原始畸变图像还是校正图像，也无法与其它鱼眼系统（UMI/exUMI/ActiveUMI）做光学层定量比较。
- Stance: `gap` | Confidence: `inference`
- Paper: [2510.08022](https://arxiv.org/abs/2510.08022) FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
- Locator: page 2, Figure 1 caption; page 3, Section III.A Hardware Design
- Evidence: 以 page 2 Fig. 1 caption 与 page 3 III.A 的全部相机描述为证据基础：两处描述均无量化规格；'未披露规格/无畸变处理讨论'是对全文的缺失性观察（absence-in-source），'无法定量比较'为读者推断。
- Quote: “FastUMI-100K integrates multimodal data streams, including single-arm and dual-arm trajectories, multi-view wrist-mounted fisheye image, and fine-grained textual annotations.”
- Authors: kehui-liu; zhongjie-jia; yang-li; et al.

### LR-FISHEYE-2026-0051

- Claim: （读者推断）USF 的全部实证评估只覆盖 MNIST 数字分类、全景目标检测与跨镜头语义分割三类 2D 视觉基准及超参消融，未包含任何机器人本体上的实验；其对具身智能（导航/操作/VLA）任务的价值属于作者定位声明而非实验结论。
- Stance: `gap` | Confidence: `inference`
- Paper: [2511.18174](https://arxiv.org/abs/2511.18174) Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera
- Locator: page 2, 1 Introduction 末段（contributions 之前的评估范围声明）
- Evidence: 前提一：作者自述评估任务为'MNIST digit classification, object detection on panoramic images, and semantic segmentation across lenses'（page 2）；前提二：实验章节 4.1-4.4 与全部表格均无机器人本体或闭环任务。二者合并得出'无机器人实验'的否定性结论；结论章仅以'practical foundation for ... robotics, AR/VR/MR/XR'作定位声明。若后续版本补充机器人实验，该 gap 消失。
- Quote: “We evaluate USF on a wide range of vision tasks: MNIST digit classification, object detection on panoramic images, and semantic segmentation across lenses. Our results show that USF maintains competitive performance while demon- strating superior robustness to rotation and zero-shot gener- alization across unseen wide-FoV lenses.”
- Authors: mukai-yu; mosam-dabhi; liuyue-xie; et al.

### LR-FISHEYE-2026-0538

- Claim: 环视鱼眼相机可用四个 >180° FoV 的超广角镜头无缝捕获全向环境，为自动驾驶车辆与各类机器人提供紧凑多相机 360° 感知；但已有鱼眼工作集中于深度估计与分割，对动态避障至关重要的 3D 目标检测（3DOD）在本文之前仍是空白。
- Stance: `gap` | Confidence: `direct`
- Paper: [2511.18695](https://arxiv.org/abs/2511.18695) Exploring Surround-View Fisheye Camera 3D Object Detection
- Locator: page 1, Section Introduction, first paragraph
- Evidence: Introduction 首段；『首个系统量化研究』的定位见 page 2 贡献列表（To our knowledge, the first systematic and quantitative study）。
- Quote: “Reliable 360◦ perception is vital for autonomous systems like self-driving vehicles and various robots. Surround-view fisheye cameras enable this via a compact multi-camera setup, as shown in Figure 1 (Right), where four ultra-wide lenses (each exceeding 180◦ field of view (FoV)) capture the full surroundings seamlessly. Existing fisheye-based works focus on depth estimation (Won, Ryu, and Lim 2020; Xie, Wang, and Liu 2023) and segmentation (Deng et al. 2019; Playout et al. 2021), but 3DOD—a cru”
- Authors: changcai-li; wenwei-lin; zuoxun-hou; et al.

### LR-FISHEYE-2026-1198

- Claim: 任务空白与对比不可行：语言引导 PTZ 相机控制是本文提出的任务，作者称据其所知没有既有模型直接解决；现有 VLA 模型（如 OpenVLA）面向机器人操控、缺 PTZ 控制接口，直接对比不可行；主动视觉搜索方法（如 Active-O3）纯软件运行、对静态图像裁剪区域，不能接入物理 PTZ 执行器或产生真机相机控制信号。
- Stance: `gap` | Confidence: `direct`
- Paper: [2511.15279](https://arxiv.org/abs/2511.15279) Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception
- Locator: page 6, IV-A Baseline and Comparison Scope
- Evidence: page 6 Section 4.1 Baseline and Comparison Scope：no existing model directly addresses this problem；OpenVLA lacks PTZ control interfaces；Active-O3 purely software by cropping static images。
- Quote: “Language-guided PTZ camera control is a task introduced by this work; to our knowledge, no ex- isting model directly addresses this problem. Existing VLA models (e.g., OpenVLA [12]) target robotic manipulation and lack PTZ con- trol interfaces, making direct comparison infeasible. Active visual search methods (e.g., Active-O3 [30]) operate purely in software by cropping regions of a static image, and thus cannot interface with physical PTZ actuators or produce real-world camera control signals.”
- Authors: jiashu-yang; yifan-han; yucheng-xie; et al.

### LR-FISHEYE-2026-0386

- Claim: 本管线采集端的相机配置全部为常规透视机型：多相机阵列由高分辨率 RGB 相机与标定过的 Intel RealSense D455 RGB-D 传感器组成；经全文（含补充材料）检索，未出现鱼眼、全景、超广角相机配置或畸变投影建模的相关内容。
- Stance: `gap` | Confidence: `direct`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 3, Section 3.1 Human Data Acquisition
- Evidence: 证据边界界定卡：设备配置为作者陈述（常规透视机型），缺席声明（无鱼眼/全景/超广角/畸变内容）经 17 页全文词表检索验证，界定本文对鱼眼综述的可用范围。
- Quote: “we have constructed many dedicated Data-Acquisition-Rooms, each equipped with a multi-camera array comprising both high-resolution RGB cameras and calibrated RGB-D sensors (Intel RealSense D455). All cameras are rigidly mounted and pre-calibrated with respect to the table world coordinate, enabling accurate 3D reconstruction and cross-view alignment of manipulation trajectories.”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0387

- Claim: 尽管"任意视角渲染"是标题级主张，下游评测并未隔离验证视角自由性的价值：三个评测任务部署时均使用固定相机配置，每策略在 10 个随机采样的初始物体位置上评测（各 10 次试验）；论文没有视角或相机配置变化的受控实验。
- Stance: `gap` | Confidence: `inference`
- Paper: [2602.05325](https://arxiv.org/abs/2602.05325) RoboPaint: From Human Demonstration to Any Robot and Any View
- Locator: page 9, Section 4.2 Real-World Evaluation
- Evidence: 读者推断：评测协议（3 任务 × 10 随机初始位置、固定主相机+腕相机）未包含视角/FOV 变化条件；"固定相机配置"与"无视角变化实验"为全文阅读确认的缺席事实，非作者原文陈述。
- Quote: “During deployment, each policy is evaluated on 10 randomly sampled initial object positions within the robot’s workspace. A trial is considered successful if the robot completes the task without human intervention and achieves the desired physical outcome, i.e., the target object is placed in the goal region, the cube is pushed to the designated location, and the bottle is tilted by nearly 90 degrees.”
- Authors: jiacheng-fan; zhiyue-zhao; yiqian-zhang; et al.

### LR-FISHEYE-2026-0009

- Claim: 作者指出：隔离鱼眼特定光学特性对策略学习定量影响的系统分析此前缺失，且现有鱼眼数据集缺乏机器人操作任务、主流机器人 benchmark 缺少鱼眼视频流。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.02139](https://arxiv.org/abs/2603.02139) Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation
- Locator: page 2, Related Work
- Evidence: Related Work 中作者明确陈述该空白并以此定位本文贡献。
- Quote: “However, a systematic analysis isolating the quantitative impact of specific optical properties on policy learning re- mains absent. This gap is reflected in the current bench- marking landscape: existing fisheye datasets [42, 43, 56] lack robotic manipulation tasks, while popular robotics benchmarks [19, 21, 28, 31] omit fisheye streams.”
- Authors: han-xue; nan-min; xiaotong-liu; et al.

### LR-FISHEYE-2026-0323

- Claim: 全景传感器（包括 360° 相机与 LiDAR）无需机械运动即可提供宽水平视场，已在自动驾驶、导航与腿式运动中展现潜力，但其在人形机器人端到端视动操作中的应用仍探索不足——这是本文识别并填补的空白。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 2, Section I (final paragraph)
- Evidence: 引言末段（page 2 开头）逐句给出全景传感器的无机械运动宽视场、AD/导航/运动中的既有进展（引文 [21][22][23]-[25][26]）与人形端到端视动操作的 under-explored 空白；[22] 为鱼眼环视相机 BEV 分割、[23] 为背对背鱼眼相机 SLAM，均为全景相机路线的被引代表。
- Quote: “Panoramic sensors, including 360 ◦ cameras and LiDAR, provide wide horizontal fields of view without mechanical motion. Al- though they have shown promise in autonomous driving [21], [22], navigation [23]–[25], and locomotion [26], their use in end-to-end visuomotor manipulation for humanoid robots remains under-explored, representing a gap in enabling large- workspace manipulation tasks [25], [27], [28].”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0334

- Claim: 本文的基线集合仅含三个共享扩散策略骨干、视觉输入各异的窄视场相机方法（DP 用 240×424 RGB、DP3 用第三视角深度点云、iDP3 用自体深度点云），且作者明示该对比旨在检验“FOV 限制”的影响而非证明算法优越性；全部评估（Tab. I-IV）中不存在任何鱼眼/全景相机基线或同等预算多相机对照——全景 LiDAR 相对全景相机（360°/环视鱼眼）方案的优劣在本文中未被检验。
- Stance: `gap` | Confidence: `inference`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 5, Section IV, Baselines
- Evidence: Baselines 段逐字列出三个基线与对比目的声明；基线输入模态差异逐字位于 page 5-6 Sec. IV-A（已核对）；“无全景相机基线”为对 page 1-8 全部基线/任务/表格的穷尽检索结论（已核对：全文无 fisheye/panoramic camera 基线或附加相机对照实验）。
- Quote: “We evaluate our approach against three diffusion-based manipulation policies: DP [4], DP3 [5], and iDP3 [6]. These methods share a common diffusion-policy Out of Vie Pick and Plac Handove Pou Wip Fig. 5: Real-world experiments and snapshots. We further validate OmniDP on four real-world tasks, confirming its robust performance in real-world environments and out-of- view manipulation scenarios. backbone but differ in their visual observation modalities and encoder architectures. By benchmarking u”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0335

- Claim: 评估协议：所有方法主要以任务成功率评估，每任务在一致初始条件下运行 20 次并报告成功试验数；杂乱环境避碰任务额外报告碰撞率（执行中与周围障碍发生物理接触的试验比例）；全文（page 1-8）未报告试验种子、方差或显著性检验，20 次试验下以 5% 为分辨率的单值计数使方法间小差距（如泛化 13/20 vs 12/20）的统计稳健性无法判定。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.05355](https://arxiv.org/abs/2603.05355) OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception
- Locator: page 6, Section IV, Evaluation Metrics
- Evidence: Evaluation Metrics 段逐字给出 20 次/任务、成功率与碰撞率定义；全文无种子/方差/显著性报告（已通读 page 1-8 提取文本核对）。
- Quote: “Evaluation Metrics. We evaluate all methods primarily by task success rate. For each task, we run each model 20 times under consistent initial conditions and report the number of successful trials. For collision-free manipulation tasks conducted in cluttered environments, we additionally report the collision rate, defined as the proportion of trials where the robot makes physical contact with surrounding obstacles during execution. This metric captures the robot’s ability to leverage environment”
- Authors: pei-qu; zheng-li; yufei-jia; et al.

### LR-FISHEYE-2026-0780

- Claim: OccTrack360 论文主张：截至该文（2026），既有占据/占据跟踪基准主要面向针孔相机设置、受限 FoV 或较短序列，不能同时提供宽 FoV 鱼眼观测、时序一致的实例级体素标注和原则性可见性约束，因此不足以评估长期环视动态理解——这是环视鱼眼 4D 占据跟踪的基准空白。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.08521](https://arxiv.org/abs/2603.08521) OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras
- Locator: page 1, Section I Introduction
- Evidence: 作者在引言中列举既有基准（Occ3D、SSCBench 等）的三个联合缺失项：宽 FoV 鱼眼观测、时序一致实例级体素标注、原则性可见性约束。
- Quote: “Existing occupancy datasets and benchmarks [5], [6] pri- marily focus on pinhole-camera setups, limited Fields of View (FoV), or relatively short sequences, which makes them insufficient for evaluating long-term, surround-view dynamic understanding. In particular, they do not jointly provide: (1) wide-FoV fisheye observations, (2) temporally consistent instance-level voxel annotations, and (3) principled visibility constraints for occupancy tracking.”
- Authors: yongzhi-lin; kai-luo; yuanfan-zheng; et al.

### LR-FISHEYE-2026-0936

- Claim: 作者任务缺口陈述：360° 空间的全局感知对具身智能体必不可少，但当前 affordance grounding（功能可供性接地）研究仍以物体为中心、局限于透视视图；作者据此提出新任务『360° 室内环境的整体 affordance grounding』，其三大挑战为 ERP 等距柱状投影的严重几何畸变、语义分散、跨尺度对齐困难。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.09760](https://arxiv.org/abs/2603.09760) PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments
- Locator: page 1, Abstract
- Evidence: 摘要开篇：全局感知必要性 + 现状局限（object-centric、perspective views）+ 新任务三挑战（ERP 畸变、语义分散、跨尺度对齐）。
- Quote: “Global perception is essential for embodied agents in 360° spaces, yet current affordance grounding remains largely object-centric and restricted to perspective views. To bridge this gap, we introduce a novel task: Holistic Affor- dance Grounding in 360° Indoor Environments. This task faces unique challenges, including severe geometric distor- tions from Equirectangular Projection (ERP), semantic dis- persion, and cross-scale alignment difficulties.”
- Authors: guoliang-zhu; wanjun-jia; caoyang-shao; et al.

### LR-FISHEYE-2026-0128

- Claim: 论文声明：尽管全景视觉在具身智能（导航、SLAM、场景理解等"看"的任务）已有应用，其用于"行动"侧的可供性推理潜力此前基本未被探索，本文是对全景可供性预测任务的首个探索。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.15558](https://arxiv.org/abs/2603.15558) Panoramic Affordance Prediction
- Locator: page 3, Section 2 Related Work, final paragraph
- Evidence: Related Work 末段明确指出全景视觉在 affordance reasoning 上的空白，是本文立题依据；"首个"声明来自作者，为综述提供了任务层面的时间锚点。
- Quote: “Despite the promising applications of panoramic vision in embodied intelligence, its potential for affordance reasoning remains largely unexplored.”
- Authors: zixin-zhang; chenfei-liao; hongfei-zhang; et al.

### LR-FISHEYE-2026-0028

- Claim: 评估范围被作者明确限定为环视车载鱼眼上的两个任务；公式化对任何已知投影模型的相机的通用性是作者声明，catadioptric 与 360° 镜头的扩展被列为有前景的未来工作。
- Stance: `gap` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 6, Section 5
- Evidence: 结论部分明确区分'已评估的两个车载任务'与'声称通用但未验证的公式化范围'。
- Quote: “While our evaluation covers two tasks on surround-view automotive fisheye, the formulation is general to any camera with a known projection model, and we see extension to catadioptric and360 ◦ lenses as promising future work.”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0029

- Claim: 作者指出：大规模鱼眼标注比 nuScenes/KITTI 等透视基准稀缺多个数量级，使从头重训基础模型不现实；现有鱼眼方法因此依赖 ImageNet 预训练 ResNet，放弃了视觉基础模型可泛化、抗畸变的表征。
- Stance: `gap` | Confidence: `direct`
- Paper: [2604.10391](https://arxiv.org/abs/2604.10391) FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception
- Locator: page 1, Introduction
- Evidence: Introduction 中作者把鱼眼方法学落后的原因总结为标注稀缺与几何失配的双重障碍。
- Quote: “The barrier is twofold.First, large-scale fisheye annota- tions are orders of magnitude scarce than perspective bench- marks like nuScenes or KITTI, making it impractical to re- train foundation models from scratch. Existing fisheye meth- ods [9, 18, 20, 26] therefore rely on ImageNet-pretrained ResNet, forfeiting the generalizable, distortion-robust repre- sentations that VFMs provide.”
- Authors: rahul-ahuja; mudit-jain; bala-murali-manoghar-sai-sudhakar; et al.

### LR-FISHEYE-2026-0092

- Claim: 作者承认本文训练的策略在推理时主要依赖视觉观察，系统在演示中同步采集的 3D 几何信息（物体结构、空间关系、交互动态）未被纳入策略学习；将 3D 信息直接引入策略学习被列为重要未来方向。
- Stance: `gap` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: page 15, Section VI, Limitations and Future Work
- Evidence: 限制章节明确区分了 LiDAR 在数据采集（SLAM 鲁棒性/数据质量）中的作用与策略推理（纯视觉）的现状，并把 geometry-aware manipulation 列为未来方向。
- Quote: “While LiDAR plays a critical role in improving SLAM robust- ness and data quality, the learned policies in this work rely primarily on visual observations at inference time. However, the system inherently captures synchronized 3D geometric information during demonstrations, including object structure, spatial relationships, and interaction dynamics.”
- Authors: ziming-wang

### LR-FISHEYE-2026-1055

- Claim: 动机-证据缺口：论文以“运动诱发抖动导致 HMD 模拟器眩晕”与窄视场/多相机切换打断操作者工作流作为系统动机，但全文实验只覆盖点图重建、稀疏/流式新视图合成等代理指标，未报告任何操作者实验（如模拟器眩晕量表、态势感知或遥操作绩效）来直接验证这些动机收益。
- Stance: `gap` | Confidence: `inference`
- Paper: [2604.13476](https://arxiv.org/abs/2604.13476) RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception
- Locator: page 1, Abstract（动机陈述）；page 7-10, Sections 3.2-3.5（实验全部为重建/NVS 指标，无人因实验）
- Evidence: 摘要与引言提出 HMD 模拟器眩晕、工作流打断等动机；但 Section 3 实验全部为重建/NVS 指标（Table 1-7），Section 4 结论也未报告操作者研究。
- Quote: “However, current robotic visual interfaces are often limited to narrow forward-facing views, or, when multiple on-board cameras are available, require cumbersome manual switching that interrupts the operator’s workflow. Both configurations suffer from motion-induced jitter that causes simulator sickness in head-mounted displays.”
- Authors: jiahao-ma; qiang-zhang; peiran-liu; et al.

### LR-FISHEYE-2026-0798

- Claim: WideDepth 论文主张：鱼眼相机在机器人的近场操作、导航与沉浸式感知中被日益采用，但带精确真值的室内深度基准仍然缺失——既有数据集多为合成或户外、缺真实室内数据；WideDepth 作为首个室内鱼眼深度估计数据集填补该空白（101 场景、5K 高分辨率立体对、毫米级 GT 深度与视差）。
- Stance: `gap` | Confidence: `direct`
- Paper: [2605.24074](https://arxiv.org/abs/2605.24074) WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation
- Locator: page 1, Abstract + Section I Introduction
- Evidence: 摘要首句即陈述机器人采用趋势与基准缺失；引言指出既有数据集 synthetic or outdoor、lacking real indoor data；贡献 1 自述首个室内毫米精度鱼眼深度基准。
- Quote: “Fisheye cameras are increasingly adopted in robotics for near-field manipulation, navigation, and immersive perception, yet indoor depth benchmarks with accurate ground truth are still missing. To address this, we introduce WideDepth — the first indoor dataset for fisheye depth estimation, featuring 101 scenes containing 5K high-resolution stereo pairs labeled with millimeter-level ground truth depth and disparity.”
- Authors: ilia-indyk; ignat-penshin; ivan-sosin; et al.

### LR-FISHEYE-2026-1094

- Claim: 具身部署证据缺口：论文动机与任务叙事面向导航/机器人搜索等具身场景，但全部具身评测止于静态 ERP 全景上的问答与搜索（PanoSpace-Bench 2,000 题、H*Bench 静态全景一步方向预测）以及 R2R-CE 协议下的导航评测——无实体机器人、机载部署或真实环境闭环实验；且 ERP 全景输入被假定为上游已提供（训练与评测直接消费 Realsee3D/360+X/网络/街景 API 等既有全景数据），鱼眼/全景传感端的获取管线（相机阵列、拼接、标定）在本文中不可见。
- Stance: `gap` | Confidence: `inference`
- Paper: [2605.13169](https://arxiv.org/abs/2605.13169) PanoWorld: Towards Spatial Supersensing in 360° Panorama World
- Locator: page 20, Appendix B.3 R2R-CE 评测协议段（实验范围核对：page 7-10 主实验与 page 18-21 附录；语料来源 page 15 Table 9）
- Evidence: Appendix B.3 确认 R2R-CE 评测为直接全景输入的离线协议；主实验（page 7-10）与附录（page 15-22）范围内无实机实验与传感端描述；训练语料来源见 page 15 Table 9。
- Quote: “We further evaluate transfer to embodied navigation on R2R-CE Val-Unseen. Unlike conventional VLN methods that often use panoramas to construct candidate perspective views or rely on additional observations such as odometry, depth, or single-view RGB streams, our model directly takes the ERP panorama as the visual observation and predicts the navigation direction from the full-surround input.”
- Authors: changpeng-wang; xin-lin; junhan-liu; et al.

### LR-FISHEYE-2026-0112

- Claim: 与 UMI 类似，数据采集时下游部署机器人的运动学限制未知，生成的演示轨迹未考虑这些限制；作者通过限制初始位姿采样范围与障碍物放置，保证生成轨迹落在部署机器人的任务空间内，并把在轨迹优化中纳入下游机器人运动学约束（任务空间与构型空间）列为扩展方向。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.19586](https://arxiv.org/abs/2606.19586) One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies
- Locator: page 9, Section 6, Limitations & Future Work
- Evidence: 作者认为该扩展可实现 embodiment-aware 策略学习框架，把语义与物理有效但硬件不可行的动作迁移到不同机器人具身。
- Quote: “Similar to UMI [7], since the kinematic limits of the downstream deployment robots are unknown at the time of data collection, the generated demonstration trajectories do not account for kinematic limits of the downstream deployment robots. We carefully bound both, the sampling range for ini- tial poses and the placement of obstacles, to ensure that the generated trajectories lie within the task space of the deployment robot.”
- Authors: chuer-pan; litian-liang; dominik-bauer; et al.

### LR-FISHEYE-2026-0440

- Claim: 评测轴仅为方位角刚体旋转：仿真协议把 14 个离散方位角中的 8 个用于训练（ψ_train∈{30°,60°,90°,120°,240°,270°,300°,330°}）、6 个保留为 OOD 评测（ψ_test∈{45°,135°,225°,255°,285°,315°}）；全文实验均使用常规 RGB 相机，扰动类型限于视角旋转、真机安装位置差与形态学改变，未测试鱼眼径向畸变、FOV/焦距变化或全景拼接等光学域偏移——ICWM 证据对『相机光学特性改变』的外推未建立。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.26025](https://arxiv.org/abs/2606.26025) In-Context World Modeling for Robotic Control
- Locator: page 15, Section B.1
- Evidence: 协议卡：B.1 节完整角度分配表；全文（含 App. C 真机 12 相机描述）无任何鱼眼/广角/畸变实验，此为全文级核对后的缺失声明。
- Quote: “We distribute 14 discrete azimuthal angles around the workspace cen- ter. We designate 8 In-Domain (ID) angles for training: ψ train ∈ {30 ◦ , 60 ◦ , 90 ◦ , 120 ◦ , 240 ◦ , 270 ◦ , 300 ◦ , 330 ◦ }, while withholding 6 Out-of-Domain (OOD) angles: ψ test ∈ {45 ◦ , 135 ◦ , 225 ◦ , 255 ◦ , 285 ◦ , 315 ◦ } exclusively for evaluation.”
- Authors: siyin-wang; junhao-shi; senyu-fei; et al.

### LR-FISHEYE-2026-0639

- Claim: 立体中间路线与数据集空白：对近场感知，立体在 arm's reach 距离提供度量接地的稠密深度，成本更低且更易部署；但作者所知此前不存在与人形机器人 360° 自我中心室内感知对齐的环视-双目（surround-stereo）占据数据集。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.22971](https://arxiv.org/abs/2606.22971) Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI
- Locator: page 2, Section 1 (stereo-centric approach paragraph); page 4, Section 2.3
- Evidence: page 2 逐字给出 stereo 中间路线的三条属性（metrically grounded dense depth at arm's reach / lower cost / easier deployment）与 no surround-stereo occupancy dataset exists 的空白声明；Related Work 2.3 末句确认已有立体占据方法 limited to front-view stereo settings（已核对，page 4）。
- Quote: “struggle with geometric reliability or incur prohibitive hardware costs. To break this bottleneck at both the data and algorithmic levels, we advocate for a stereo-centric approach. For near-field perception, stereo offers a pragmatic middle ground: metrically grounded dense depth at arm’s reach with lower cost and easier deployment. Meanwhile, stereo depth estimation Guo et al. (2023, 2024, 2025a) has matured to a degree that makes it a strong source of depth priors. However, to our knowledge,”
- Authors: xianda-guo; bohao-zhang; chenwei-huang; et al.

### LR-FISHEYE-2026-1403

- Claim: 领域缺口（本文定位）：采用全景表示的近期工作（含 PAN-SLAM [4]、Multi-LVI-SAM [12]）仍局限于特定刚性相机配置、忽略异构模块几何一致性、依赖昂贵拼接或优化后端，导致实时性差——异构通用+轻量实时是多相机 VIO 的未解缺口。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.29910](https://arxiv.org/abs/2606.29910) Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems
- Locator: page 1, Section I. Introduction
- Evidence: Introduction 末段对近期全景表示工作的定位性评述；[12] 即本批综述第一篇 Multi-LVI-SAM（2509.05740），[4] 为 PAN-SLAM。
- Quote: “Recent works [4], [12] adopt panoramic representations, a special full-field variant of gen- eral spherical representations, but remain confined to specific rigid setups, ignore geometric consistency for heterogeneous modules, and depend on expensive stitching or optimization backends, resulting in poor real-time performance.”
- Authors: yueteng-yang; yusen-xie; hao-wei; et al.

### LR-FISHEYE-2026-0740

- Claim: 评测协议层面：论文定量评测中鱼眼与异构评测使用 OmniScene held-out 测试场景（OmniScene-Full/Quad/Single）与 KITTI360，针孔评测使用 ETH3D、ScanNet++ v2 与真实世界 OmniOcc 基准，而 OmniOcc 的硬件是四个立体相机对（共 8 个同步 RGB 视图）+ 共配准 LiDAR 的纯针孔环视设置——因此异构（鱼眼+针孔混合）设置的定量结果全部来自 OmniScene（作者自建合成数据集，见 Sec 4/C07），不存在真实世界混合鱼眼+针孔 rig 的定量评测基准；'异构收益'（如 AbsRel −25.4%）向真实世界混合 rig 的外推缺乏直接定量证据。
- Stance: `gap` | Confidence: `inference`
- Paper: [2607.12993](https://arxiv.org/abs/2607.12993) X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras
- Locator: page 22, Appendix C and D
- Evidence: 该缺口由评测协议枚举直接推出：附录 D 明确鱼眼与异构评测只用 OmniScene 测试场景与 KITTI360、针孔评测用 ETH3D/ScanNet++/OmniOcc；附录 C 说明 OmniOcc 为立体对 RGB（针孔）硬件；全文表格（Table 1-5）无真实异构基准，Fig.6/10/11 的真实场景结果仅为定性。
- Quote: “C. OmniOcc: Real-world Surround-view Benchmark To assess our model’s robustness in real-world data, we curate OmniOcc, a real-world indoor dataset for multi-view geometric parsing. The hardware setup consists of four stereo camera pairs cam 0 –cam 3 , each providing a left and a right view for 8 synchronized RGB views in total at 1280 × 1088 resolution, together with a co-registered LiDAR sensor, establishing omnidirectional coverage under a shared metric coordinate frame. OmniOcc spans 25 diver”
- Authors: heng-zhou; shuhong-liu; yonghao-he; et al.

### LR-FISHEYE-2026-0316

- Claim: 评估协议为每方法每任务 15 次闭环真机试验、每试验单次不间断 rollout、失败阶段不做人工重置；全文（page 1-8）未报告试验种子、方差或显著性检验，各方法间的数字差距（如 Wipe Table SR 46.7% vs 40.0% vs 20.0%）在 15 次试验下的统计稳健性无法从报告数据判定。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.02257](https://arxiv.org/abs/2608.02257) Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation
- Locator: page 5, Section V-A, Evaluation Protocol and Metrics
- Evidence: Evaluation Protocol 段逐字给出 15 trials/task、single uninterrupted rollout、no manual resets；全文无种子/方差/显著性报告（已通读 page 1-8 提取文本核对）。
- Quote: “To enable fine-grained failure analysis, we decompose each task into multiple stages and evaluate each method with 15 closed- loop real-robot trials per task. Every trial is conducted as a single uninterrupted rollout, with all actions generated by the policy and no manual resets of failed stages.”
- Authors: donglin-yang; haoran-chen; xingyu-chen; et al.

### LR-FISHEYE-2026-0402

- Claim: 真机部署相机为 Intel RealSense D435i 常规 RGB 相机（640×480@15fps）、训练用三台同步外置场景相机 C0/C1/C2——全研究不含鱼眼/全景/超广角成像；评估的相机变化全部是外参级（距离、方位、高度/俯仰）摆放变化。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.06965](https://arxiv.org/abs/2608.06965) Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies
- Locator: page 14, Table 6
- Evidence: Table 6 记录硬件与相机型号；扰动族定义（C1 距离/尺度、C2 球面位置、C3 端点朝向）全部为外参变化，无镜头模型变量。
- Quote: “Image preprocessing Intel RealSense D435i cameras; RGB images are captured at 640 × 480 resolution and 15 fps.”
- Authors: bingqi-huang; bingchuan-wei; xuan-wang; et al.

### LR-FISHEYE-2026-0425

- Claim: 本文评估的相机变化轴全部为透视相机外参级四轴：LIBERO-Plus 枚举的 1,599 个相机扰动任务实例的参数覆盖轨道方位角（水平 ±75°）、仰角（垂直 {0, 15}）、dolly 距离（尺度 100 到 200）与相机端点原地再定向（±10）；训练配对采样同轴并匹配基准边缘分布——全文不存在镜头模型/畸变级别的相机变量。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.21402](https://arxiv.org/abs/2608.21402) Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information
- Locator: page 5, Section V-B
- Evidence: 轴枚举出自 V-B 节；'全文无镜头模型变量'为读者对 9 页全文的检索事实，仅支撑 gap 立场而非性能断言。
- Quote: “LIBERO-Plus enumerates 1,599 camera-perturbed task instances whose parameters span four axes: orbital azimuth (horizon, ±75 ◦ ), elevation (vertical, {0, 15}), dolly distance (scale, 100 to 200), and in-place reorientation of the camera endpoint (±10) [4]. Our training pairs sample the same axes with density matched to the benchmark marginal, after which we remove held-out regions.”
- Authors: bingqi-huang; bingchuan-wei; yingkai-cai; et al.

### LR-FISHEYE-2026-0667

- Claim: 作者定位研究空白：球面观测的全 FoV 覆盖特性与具身智能对整体 3D 空间感知的增长需求高度契合，但现有研究大多聚焦透视相机或 2D 球面场景理解，球面视觉用于 3D 空间感知的潜力基本未被探索。
- Stance: `gap` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 1, Section 1, Introduction
- Evidence: 引言开头：spherical observations 的连续 360° 水平覆盖与具身智能需求高度对齐（引 [7][8][9]），但 3D 空间感知方向的球面视觉潜力 largely unexplored。
- Quote: “property is highly aligned with the growing demand for em- bodied intelligence for holistic 3D spatial perception [7], [8], [9]. However, existing studies have largely focused on per- spective cameras or 2D spherical scene understanding [10], [11], [12], [13], leaving the potential of spherical vision for 3D spatial perception largely unexplored.”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-0668

- Claim: 全景环形相机（panoramic annular camera）的固有结构设计把垂直 FoV 限制在约 45°；已有占据预测工作（OneOcc、PanoMMOcc）基于此类相机，而宽 FoV 的球面占据预测在此前未被探索。
- Stance: `gap` | Confidence: `direct`
- Paper: [2609.09012](https://arxiv.org/abs/2609.09012) Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild
- Locator: page 4, Section 2.2, Semantic Occupancy Prediction
- Evidence: Sec 2.2 指出 OneOcc/PanoMMOcc 的环形相机垂直 FoV 约 45°（page 3 Sec 2.1 亦称其仅水平观测、限制可捕捉场景范围），wide-FoV spherical occupancy unexplored。
- Quote: “OneOcc [43] and PanoMMOcc [78] have studied semantic occupancy prediction from panoramic annular cameras [1], their vertical field of view is limited to approximately 45 ◦ , leaving wide-FoV spherical occupancy unexplored.”
- Authors: fei-teng; sheng-wu; mengfei-duan; et al.

### LR-FISHEYE-2026-1076

- Claim: 动机-证据缺口：论文动机是超低空 UAV 在建筑物/植被/人群附近穿行时需要环视以避免前视相机在转弯中丢失地标并把感知方向耦合到避障决策，但全文评测止于拼接几何/光度质量、Jetson 嵌入式运行时与冻结检测/VPR 接口代理，未报告任何闭环避障、航迹控制或飞行任务级收益实验。
- Stance: `gap` | Confidence: `inference`
- Paper: [2609.02319](https://arxiv.org/abs/2609.02319) From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs
- Locator: page 1, Section I Introduction（动机）；page 7-9, Sections V-A–V-D（实验范围，无闭环避障/飞行控制实验）
- Evidence: page 1 引言给出避障耦合与环视动机；page 7-9 全部实验（Tables III-VII、Figs. 5-6）为拼接质量、运行时与冻结模型接口评测；page 9 结论亦未提飞行任务实验。
- Quote: “Ultra-low-altitude unmanned aerial vehicles (UAVs) move be- tween open views and cluttered areas near buildings, vegetation, and people. A forward camera can lose landmarks or objects during turns, whereas panoramic vision preserves surround- view context.”
- Authors: dun-dai; ze-lu; cheng-he; et al.

## References

- `2509.05740` [Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras](https://arxiv.org/abs/2509.05740) (2025-09)
- `2509.12989` [PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era](https://arxiv.org/abs/2509.12989) (2025-09)
- `2509.13541` [PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM](https://arxiv.org/abs/2509.13541) (2025-09)
- `2509.14688` [exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation](https://arxiv.org/abs/2509.14688) (2025-09)
- `2509.15673` [Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry via Photometric Migration and ESIKF Fusion](https://arxiv.org/abs/2509.15673) (2025-09)
- `2510.01607` [ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations](https://arxiv.org/abs/2510.01607) (2025-10)
- `2510.08022` [FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset](https://arxiv.org/abs/2510.08022) (2025-10)
- `2511.00510` [OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback](https://arxiv.org/abs/2511.00510) (2025-11)
- `2511.03571` [OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera](https://arxiv.org/abs/2511.03571) (2025-11)
- `2511.15279` [Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception](https://arxiv.org/abs/2511.15279) (2025-11)
- `2511.18174` [Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera](https://arxiv.org/abs/2511.18174) (2025-11)
- `2511.18695` [Exploring Surround-View Fisheye Camera 3D Object Detection](https://arxiv.org/abs/2511.18695) (2025-11)
- `2601.02309` [360DVO: Deep Visual Odometry for Monocular 360-Degree Camera](https://arxiv.org/abs/2601.02309) (2026-01)
- `2602.05325` [RoboPaint: From Human Demonstration to Any Robot and Any View](https://arxiv.org/abs/2602.05325) (2026-02)
- `2603.02139` [Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation](https://arxiv.org/abs/2603.02139) (2026-03)
- `2603.05355` [OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception](https://arxiv.org/abs/2603.05355) (2026-03)
- `2603.05868` [AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models](https://arxiv.org/abs/2603.05868) (2026-03)
- `2603.05999` [RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation](https://arxiv.org/abs/2603.05999) (2026-03)
- `2603.08521` [OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras](https://arxiv.org/abs/2603.08521) (2026-03)
- `2603.09760` [PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments](https://arxiv.org/abs/2603.09760) (2026-03)
- `2603.13108` [Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots](https://arxiv.org/abs/2603.13108) (2026-03)
- `2603.15558` [Panoramic Affordance Prediction](https://arxiv.org/abs/2603.15558) (2026-03-14)
- `2603.17351` [OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms](https://arxiv.org/abs/2603.17351) (2026-03)
- `2603.28896` [Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses](https://arxiv.org/abs/2603.28896) (2026-03)
- `2604.00557` [Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning](https://arxiv.org/abs/2604.00557) (2026-04)
- `2604.00648` [DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting with Cross-View Joint Optimization](https://arxiv.org/abs/2604.00648) (2026-04)
- `2604.00852` [PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset](https://arxiv.org/abs/2604.00852) (2026-04)
- `2604.10391` [FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception](https://arxiv.org/abs/2604.10391) (2026-04)
- `2604.13476` [RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception](https://arxiv.org/abs/2604.13476) (2026-04)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089) (2026-04)
- `2605.03452` [BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation](https://arxiv.org/abs/2605.03452) (2026-05)
- `2605.13169` [PanoWorld: Towards Spatial Supersensing in 360° Panorama World](https://arxiv.org/abs/2605.13169) (2026-05)
- `2605.24074` [WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation](https://arxiv.org/abs/2605.24074) (2026-05)
- `2606.04708` [VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training](https://arxiv.org/abs/2606.04708) (2026-05)
- `2606.19253` [OneCanvas: 3D Scene Understanding via Panoramic Reprojection](https://arxiv.org/abs/2606.19253) (2026-06)
- `2606.19586` [One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies](https://arxiv.org/abs/2606.19586) (2026-06)
- `2606.22971` [Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI](https://arxiv.org/abs/2606.22971) (2026-06)
- `2606.26025` [In-Context World Modeling for Robotic Control](https://arxiv.org/abs/2606.26025) (2026-06)
- `2606.29910` [Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems](https://arxiv.org/abs/2606.29910) (2026-06)
- `2607.02711` [RayTun3R: Online Camera Adaptation in 3D Foundation Models](https://arxiv.org/abs/2607.02711) (2026-07)
- `2607.05777` [Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis](https://arxiv.org/abs/2607.05777) (2026-07)
- `2607.12993` [X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras](https://arxiv.org/abs/2607.12993) (2026-07)
- `2607.25895` [HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone](https://arxiv.org/abs/2607.25895) (2026-07)
- `2608.02257` [Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation](https://arxiv.org/abs/2608.02257) (2026-08)
- `2608.06965` [Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies](https://arxiv.org/abs/2608.06965) (2026-08)
- `2608.11051` [HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation](https://arxiv.org/abs/2608.11051) (2026-08)
- `2608.19066` [GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting](https://arxiv.org/abs/2608.19066) (2026-08)
- `2608.21402` [Selective Cross-View Consistency for World Action Models: Held-Out Viewpoint Robustness Without Test-Time Camera Information](https://arxiv.org/abs/2608.21402) (2026-08)
- `2608.26058` [One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training for Heterogeneous Embodied Manipulation](https://arxiv.org/abs/2608.26058) (2026-08)
- `2609.02319` [From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs](https://arxiv.org/abs/2609.02319) (2026-09)
- `2609.09012` [Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild](https://arxiv.org/abs/2609.09012) (2026-09)
