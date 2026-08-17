# Evidence Appendix: Ego-Exo 相机配置与视角对齐

- Time range: 2021-12-15..2026-08-14（覆盖 EgoBody 到最新对齐方法）
- Events: 18
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-CAMALIGN-2026-0001

- Claim: Ego-Exo4D 的第三人称（exo）相机配置由一套低成本、便携、自动时间同步的采集 rig 初始化：1 台 Aria 眼镜（ego）+ 4 台固定在三脚架上的 GoPro（exo），全套（不含 Aria/手机/笔记本）成本低于 3000 美元。
- Stance: `support` | Confidence: `direct`
- Paper: [2311.18259](https://arxiv.org/abs/2311.18259) Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person Perspectives
- Locator: 3.1 Ego-exo camera rig
- Evidence: 3.1 直接列出 rig 的组成与成本，说明 exo 相机为固定于三脚架的 4 台 GoPro。
- Quote: "Our solution consists of 1 Aria ..., 4 GoPros ..., 1 GoPro Remote, 4 Tripods ... The total cost excluding the Aria/phone/laptop is under $3,000."
- Authors: kristen-grauman; andrew-westbury; lorenzo-torresani

### EA-CAMALIGN-2026-0002

- Claim: exo（GoPro）相机的几何初始化分两步：Aria 用 VIO+SLAM 构建公共度量、重力对齐的坐标地图；每台静态 GoPro 先在实验室手工标定一台以获得默认内参，再用 P4P（PnP）算法配合 RANSAC 在该 SLAM 地图上估计其 6DoF 位姿并重新估计焦距，从而把所有 exo 相机注册进同一世界坐标系。
- Stance: `support` | Confidence: `direct`
- Paper: [2311.18259](https://arxiv.org/abs/2311.18259) Ego-Exo4D
- Locator: 3.1.2 Precomputed 3D spatial signals
- Evidence: 3.1.2 详述 Aria MPS 的标定、Aria 6DoF 定位与 GoPro 6DoF 定位流程。
- Quote: "manually calibrated one device in the lab to obtain default parameters, and then use the P4P ... algorithm (with RANSAC to reject matching outliers) to estimate the 6 DoF pose, as well as re-estimate the focal length."
- Authors: kristen-grauman; andrew-westbury; lorenzo-torresani

### EA-CAMALIGN-2026-0003

- Claim: exo 相机的时间同步用一段 29fps 的预渲染 QR 码视频编码墙钟时间，逐台相机播放并利用帧率差细同步，最终人工校验每台 GoPro 与 Aria RGB 相机的同步误差在 1 帧以内（±16.66ms，亚帧级）。
- Stance: `support` | Confidence: `direct`
- Paper: [2311.18259](https://arxiv.org/abs/2311.18259) Ego-Exo4D
- Locator: 7.1 Time sync
- Evidence: 7.1 详述 QR 码视频同步机制与 ±1 帧校验精度，并说明 70% 自动达到帧级同步、其余 30% 靠人工对齐恢复。
- Quote: "we employ a pre-rendered sequence of QR Codes ... to finely sync the cameras. ... each GoPro camera was within 1 frame (+-16.66ms) of the Aria RGB camera."
- Authors: kristen-grauman; andrew-westbury; lorenzo-torresani

### EA-CAMALIGN-2026-0004

- Claim: EgoBody 的多台第三人称相机（3–5 台固定的 Azure Kinect RGB-D）+ 1 台 HoloLens2（ego）通过两步完成空间对齐：先用棋盘格标定得到初始内/外参，再用 ICP 刚性配准（场景点云）细化 Kinect–Kinect 与 Kinect–HoloLens2；Cam1 定义世界坐标系原点，HoloLens2 靠内置头部跟踪器在其世界原点下被持续跟踪。
- Stance: `support` | Confidence: `direct`
- Paper: [2112.07642](https://arxiv.org/abs/2112.07642) EgoBody: Human Body Shape and Motion of Interacting People from Head-Mounted Devices
- Locator: 3.2 Data Acquisition Setup
- Evidence: 3.2 与 0.A.1 Calibration 详述多相机空间标定流程与世界原点定义。
- Quote: "Kinect-Kinect and Kinect-HoloLens2 cameras are spatially calibrated using a checkerboard and refined by rigid alignment steps (ICP). ... We use Cam1 to define our world coordinate frame origin."
- Authors: siwei-zhang; qianli-ma; yan-zhang

### EA-CAMALIGN-2026-0005

- Claim: 第一↔第三人称视角对齐的一条表征路线：AE2 在无配对（unpaired）设定下，用 object-centric 编码器关注手与主动物体、以 DTW 时序对齐作自监督目标、反转帧作负样本，学到细粒度视角不变表征，从而在不需要几何标定的情况下对齐 ego-exo 视角。
- Stance: `support` | Confidence: `direct`
- Paper: [2306.05526](https://arxiv.org/abs/2306.05526) Learning Fine-grained View-Invariant Representations from Unpaired Ego-Exo Videos via Temporal Alignment
- Locator: 1 Introduction
- Evidence: 1 Introduction 与 Method 直接陈述三个关键设计；被纳入既有 ego-exo 综述（EA-EGOEXO-2026-0011/0012）。
- Quote: "unpaired data. In the unpaired setting, we know which human activity occurs ... but they need not be collected simultaneously or in the same environment."
- Authors: zihui-xue; kristen-grauman

### EA-CAMALIGN-2026-0006

- Claim: 第一↔第三人称视角对齐落到对象级对应任务：ObjectRelator 用 MCFuse 融合文本描述与视觉掩码、XObjAlign 做自监督跨视角对象对齐，在 Ego-Exo4D 对象对应基准上取得 SOTA（IoU Ego2Exo 39.7→44.3，Exo2Ego 44.1→49.2）。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.19083](https://arxiv.org/abs/2411.19083) ObjectRelator: Enabling Cross-View Object Relation Understanding Across Ego-Centric and Exo-Centric Perspectives
- Locator: 4.1 Main Results on Ego-Exo4D
- Evidence: Abstract 与 4.1 直接陈述方法与 Ego-Exo4D 上相对 PSALM 的 IoU 提升；被纳入既有综述（EA-EGOEXO-2026-0013/0014）。
- Quote: "improves the PSALM from 39.7 to 44.3 on Ego2Exo and from 44.1 to 49.2 on Exo2Ego."
- Authors: yu-fu; runze-wang; bin-ren

### EA-CAMALIGN-2026-0007

- Claim: LM-EEC 把 ego-exo 对象对应形式化为：给定同步的 ego-exo 视频对与某一视角的目标掩码，在另一视角逐帧分割同一对象（Ego2Exo / Exo2Ego），并以基于 SAM 2 的双记忆库 + Memory-View 混合专家（MoE）模块解决极端视角变化、遮挡与小目标问题，在 EgoExo4D 上取得 SOTA。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.11417](https://arxiv.org/abs/2510.11417) Robust Ego-Exo Correspondence with Long-Term Memory
- Locator: 3.1 Task definition
- Evidence: 3.1 与 3.3 直接陈述任务定义与双记忆/MoE 架构。
- Quote: "Given a pair of synchronized ego-exo videos and a sequence of query masks for an object ... identify the corresponding masks of the same object in each synchronized frame of the other view."
- Authors: zijian-he

### EA-CAMALIGN-2026-0008

- Claim: Exo2Ego 提出生成式第一↔第三人称视角对齐：把 exo→ego 跨视角翻译解耦为高层结构变换（显式鼓励跨视角对应）与基于扩散的像素级幻觉（引入手部布局先验），在最小化对相机参数/几何结构假设的前提下生成第一人称视角。
- Stance: `support` | Confidence: `direct`
- Paper: [2403.06351](https://arxiv.org/abs/2403.06351) Put Myself in Your Shoes: Lifting the Egocentric Perspective from Exocentric Videos
- Locator: 3.1 Problem Formulation
- Evidence: Abstract 与 3.1 直接陈述两阶段解耦与无几何假设的概率化设定。
- Quote: "we propose a generative framework called Exo2Ego that decouples the translation process into two stages: high-level structure transformation ... and a diffusion-based pixel-level hallucination."
- Authors: mi-luo

### EA-CAMALIGN-2026-0009

- Claim: BYOV 用掩码 ego-exo 建模在无配对设定下学视角不变表征：self-view masking 重构自视角帧以捕获时序依赖、cross-view masking 预测对方视角的隐变量以学跨视角对齐，从而在不需同步/配对的前提下对齐 ego-exo 视角。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.19706](https://arxiv.org/abs/2503.19706) Bootstrap Your Own Views: Masked Ego-Exo Modeling for Fine-grained View-invariant Representation Learning
- Locator: 3.1 Overview of BYOV
- Evidence: Abstract 与 3.1 直接陈述两种掩码建模目标。
- Quote: "masked self-view modeling reconstructs frame-level token embeddings from the own view ... masked cross-view modeling learns view-invariant temporal features by predicting the different view's latents."
- Authors: jungin-park

### EA-CAMALIGN-2026-0010

- Claim: SAVA-X 把第一↔第三人称对齐用于跨视角模仿错误检测：给定异步、长度不匹配的 exo 演示与 ego 模仿视频，用 Align–Fuse–Detect 框架（视角条件自适应采样、场景自适应视角嵌入、双向交叉注意力融合）定位 ego 时间线上的步骤并判断正误。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.12764](https://arxiv.org/abs/2603.12764) SAVA-X: Ego-to-Exo Imitation Error Detection via Scene-Adaptive View Alignment
- Locator: 3.1 Problem Formulation
- Evidence: Abstract 与 3.1 直接陈述任务定义与三大组件。
- Quote: "we propose SAVA-X, an Align-Fuse-Detect framework with (i) view-conditioned adaptive sampling, (ii) scene-adaptive view embeddings, and (iii) bidirectional cross-attention fusion."
- Authors: jia-li

### EA-CAMALIGN-2026-0011

- Claim: SUM-L 处理无配对多视角（含多台第三人称相机）对齐：先用 LLM 编码视频文本叙述挖掘跨视角伪配对，再做语义感知的跨视角对比对齐 + 视频-文本模态对齐，从而在没有同步/配对多视角数据的情况下对齐第一与第三人称视角。
- Stance: `support` | Confidence: `direct`
- Paper: [2308.11489](https://arxiv.org/abs/2308.11489) Learning from Semantic Alignment between Unpaired Multiviews for Egocentric Video Recognition
- Locator: 3.3 Semantics-based Multiview Learning
- Evidence: Abstract、3.1 与 3.3 直接陈述伪配对挖掘与语义感知对齐。
- Quote: "we propose ... Semantics-based Unpaired Multiview Learning ... build cross-view pseudo-pairs and do view-invariant alignment by leveraging the semantic information of videos."
- Authors: qitong-wang

### EA-CAMALIGN-2026-0012

- Claim: 第一↔第三人称对齐的同步蒸馏路线：仅用带标注 exo 视频 + 无标注的同步 exo-ego 视频对做知识蒸馏，即可把时序动作分割模型从 exo 迁移到 ego（edit 28.59，与监督 ego-oracle 26.42 相当），同步是强桥接信号但需采集同步对。
- Stance: `support` | Confidence: `direct`
- Paper: [2312.02638](https://arxiv.org/abs/2312.02638) Synchronization is All You Need: Exocentric-to-Egocentric Transfer for Temporal Action Segmentation with Unlabeled Synchronized Video Pairs
- Locator: 5.1 Performance of the Proposed Approach
- Evidence: Abstract 与 5.1 直接陈述该设定与 edit 分数对比；被纳入既有综述（EA-EGOEXO-2026-0017/0018）。
- Quote: "28.59 ... 26.42 ... 12.60"
- Authors: camillo-quattrocchi; antonino-furnari

### EA-CAMALIGN-2026-0013

- Claim: YOWO 把多台第三人称（天花板安装）相机的对齐形式化为场景建图加相机位姿注册：让佩戴头戴 RGB-D 相机的移动 agent 遍历场景一次，用 ICP/SLAM 建出场景点云与 ego 轨迹；天花板相机通过观察该 agent 的运动关键点用增量 SfM 估计相对位姿，再用时空重平衡配准与因子图联合优化，把所有天花板相机 6DoF 位姿注册进同一世界坐标系。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.16521](https://arxiv.org/abs/2511.16521) YOWO: You Only Walk Once to Jointly Map an Indoor Scene and Register Ceiling Cameras
- Locator: III Approach
- Evidence: III Approach 与 III-C Collaborative Processing 直接陈述三条处理管线与联合注册机制。
- Quote: "a mobile agent with a head-mounted RGB-D camera to traverse the entire scene once ... registering CMC six-degrees-of-freedom (6-DoF) poses to the scene layout."
- Authors: yowo

### EA-CAMALIGN-2026-0014

- Claim: 对于没有共视重叠的孤立第三人称相机，YOWO 先完成场景建图与非孤立相机注册，再用 RANSAC 加 PnP 从已优化的 3D 移动关键点初始化其 6DoF 位姿，随后融合场景静态关键点与移动关键点的 2D-3D 匹配细化位姿——即先建图、后 PnP 定位，把无法共视的相机也注册进场景。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.16521](https://arxiv.org/abs/2511.16521) YOWO
- Locator: III-D Register 6-DoF Poses for Isolated CMCs
- Evidence: III-D 直接陈述孤立相机的 PnP 初始化与细化流程。
- Quote: "Employing RANSAC and PnP ... we initialize the 6-DoF pose of the isolated CMC ... incorporate the 2D-3D matches ... to refine the isolated CMC 6-DoF pose."
- Authors: yowo

### EA-CAMALIGN-2026-0015

- Claim: H2O 用 5 台 Azure Kinect RGB-D 相机（4 静态 + 1 头戴）采集同步多视角；外参标定不使用棋盘格，而是用 9 个 IR 反射球——每球在所有相机中可见，从深度图定位其 3D 坐标后用 PnP 求解相机位姿；相机间用物理线缆同步，帧间延迟小于 0.74ms。
- Stance: `support` | Confidence: `direct`
- Paper: [2104.11181](https://arxiv.org/abs/2104.11181) H2O: Two Hands Manipulating Objects for First Person Interaction Recognition
- Locator: 3.1 Camera Calibration
- Evidence: 3.1 与 4.1 直接陈述 IR 反射球标定与线缆同步机制。
- Quote: "We place nine IR reflective spheres ... solve for camera pose via PnP ... To ensure synchronization between multiple cameras, we use physical cables."
- Authors: taein-kwon

### EA-CAMALIGN-2026-0016

- Claim: Nymeria 的采集配置由 mocap 服、Aria 眼镜、miniAria 腕带与同步设备组成；同步设备为所有设备提供统一时间戳（可选从无线服务器接收），达亚毫秒级精度，XSens 与 Aria 的对齐误差在 1 个运动帧内即 4.2ms。
- Stance: `support` | Confidence: `direct`
- Paper: [2406.09905](https://arxiv.org/abs/2406.09905) Nymeria: A Massive Collection of Multimodal Egocentric Daily Motion in the Wild
- Locator: 3.1 Data collection setup (Synchronization)
- Evidence: Synchronization 小节直接陈述同步设备与精度。
- Quote: "A synchronization device is developed to supply the timestamps for all devices ... sub-millisecond accuracy. The alignment between XSens and Aria is within 1 motion frame i.e. 4.2 ms."
- Authors: lingni-ma

### EA-CAMALIGN-2026-0017

- Claim: Nymeria 用 Project Aria MPS 的 VIO、SLAM 与建图算法，把同一地点多设备录制的数据先各自跑 SLAM，再回环闭合并做视觉惯性 bundle adjustment 联合优化，全局对齐进单一度量 3D 世界，输出 1kHz 高精度轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2406.09905](https://arxiv.org/abs/2406.09905) Nymeria
- Locator: 3.2 6DoF localization and mapping with global alignment
- Evidence: 3.2 直接陈述多设备全局对齐流程。
- Quote: "first SLAM is run for each individual recording independently. Subsequently, the resulting maps are loop-closed and jointly optimized via visual-inertial bundle adjustment."
- Authors: lingni-ma

### EA-CAMALIGN-2026-0018

- Claim: EgoHumans 用异构多相机系统（多副 Aria 眼镜作 ego + 8–15 台 GoPro 作 secondary/exo，全部同步，便携体积可移动）在野外采集多人 3D 人体；每帧标注每台相机的标定与位姿，并把 secondary 与 ego 相机对齐进世界坐标系。
- Stance: `support` | Confidence: `direct`
- Paper: [2305.16487](https://arxiv.org/abs/2305.16487) EgoHumans: An Egocentric 3D Multi-Human Benchmark
- Locator: 3 EgoHumans Dataset
- Evidence: Data Collection 直接陈述异构相机系统、同步与逐帧标定位姿标注。
- Quote: "a flexible and simple multi-view system with heterogeneous sensors, including multiple Aria glasses and GoPros for the egocentric and secondary views ... All cameras are synchronized."
- Authors: rawal-khirodkar

## References

- `2311.18259` [Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person Perspectives](https://arxiv.org/abs/2311.18259) (2023-11-30)
- `2112.07642` [EgoBody: Human Body Shape and Motion of Interacting People from Head-Mounted Devices](https://arxiv.org/abs/2112.07642) (2021-12-15)
- `2306.05526` [Learning Fine-grained View-Invariant Representations from Unpaired Ego-Exo Videos via Temporal Alignment](https://arxiv.org/abs/2306.05526) (2023-06-10)
- `2411.19083` [ObjectRelator: Enabling Cross-View Object Relation Understanding Across Ego-Centric and Exo-Centric Perspectives](https://arxiv.org/abs/2411.19083) (2024-11-28)
- `2510.11417` [Robust Ego-Exo Correspondence with Long-Term Memory](https://arxiv.org/abs/2510.11417) (2025-10-13)
- `2403.06351` [Put Myself in Your Shoes: Lifting the Egocentric Perspective from Exocentric Videos](https://arxiv.org/abs/2403.06351) (2024-03-11)
- `2503.19706` [Bootstrap Your Own Views: Masked Ego-Exo Modeling for Fine-grained View-invariant Representation Learning](https://arxiv.org/abs/2503.19706) (2025-03-24)
- `2603.12764` [SAVA-X: Ego-to-Exo Imitation Error Detection via Scene-Adaptive View Alignment](https://arxiv.org/abs/2603.12764) (2026-03-16)
- `2308.11489` [Learning from Semantic Alignment between Unpaired Multiviews for Egocentric Video Recognition](https://arxiv.org/abs/2308.11489) (2023-08-22)
- `2312.02638` [Synchronization is All You Need: Exocentric-to-Egocentric Transfer for Temporal Action Segmentation with Unlabeled Synchronized Video Pairs](https://arxiv.org/abs/2312.02638) (2023-12-05)
- `2511.16521` [YOWO: You Only Walk Once to Jointly Map an Indoor Scene and Register Ceiling Cameras](https://arxiv.org/abs/2511.16521) (2025-11)
- `2104.11181` [H2O: Two Hands Manipulating Objects for First Person Interaction Recognition](https://arxiv.org/abs/2104.11181) (2021-04-22)
- `2406.09905` [Nymeria: A Massive Collection of Multimodal Egocentric Daily Motion in the Wild](https://arxiv.org/abs/2406.09905) (2024-06-14)
- `2305.16487` [EgoHumans: An Egocentric 3D Multi-Human Benchmark](https://arxiv.org/abs/2305.16487) (2023-05-25)
