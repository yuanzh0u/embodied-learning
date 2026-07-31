# Evidence Appendix: 近一年 ego-centric 数据中手部检测与追踪的问题和难点

- Time range: 2025-07-29 至 2026-07-29
- Events: 29
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-EGOHAND-2026-0007

- Claim: 第一视角的相机坐标会把头部抖动与物体运动混合，稳定 HOI 追踪需要世界坐标锚定。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.01050](https://arxiv.org/abs/2601.01050) EgoGrasp: World-Space Hand-Object Interaction Estimation from Egocentric Videos
- Locator: 1 Introduction
- Evidence: 原文直接描述相机自运动与物体运动的坐标耦合。
- Quote: “In egocentric scenarios, high-frequency camera jitter is entangled with object movement in local views.”
- Authors: hongming-fu; wenjia-wang; xiaozhen-qiao; et al.

### EA-EGOHAND-2026-0009

- Claim: Egocentric 手指自遮挡是高频现象：跨四个数据集，超过 20% 帧至少有一根手指高度遮挡。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.15516](https://arxiv.org/abs/2601.15516) DeltaDorsal: Enhancing Hand Pose Estimation with Dorsal Features in Egocentric Views
- Locator: 3.2. Occlusion Prevalence in Egocentric Data
- Evidence: 原文在四数据集分析中直接报告遮挡比例。
- Quote: “As shown in Figure 3 a, more than 20% of frames across all evaluated datasets exhibit at least one occluded finger, with over 5% containing two or more occluded fingers.”
- Authors: william-huang; siyou-pei; leyi-zou; et al.

### EA-EGOHAND-2026-0018

- Claim: 单目头戴相机中，绝对 3D 手追踪同时受深度–尺度歧义、自遮挡与宽 FOV/鱼眼变形限制。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.12498](https://arxiv.org/abs/2605.12498) EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera
- Locator: 1. Introduction
- Evidence: 原文在问题定义中直接并列了绝对 3D 手追踪的三个主要视觉/几何难点。
- Quote: “However, achieving this from a single egocentric camera is challenging due to depth–scale ambiguity, frequent self-occlusions, and the strong distortions introduced by wide-FOV and fisheye optics (Millerdurai et al. , 2024a , 2025 ) .”
- Authors: christen-millerdurai; shaoxiang-wang; yaxu-xie; et al.

### EA-EGOHAND-2026-0020

- Claim: Ego 双手追踪的观测质量具有左/右手与腕部/手指两个轴的异质性，不能用单一置信度概括。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.18553](https://arxiv.org/abs/2605.18553) StableHand: Quality-Aware Flow Matching for World-Space Dual-Hand Motion Estimation from Egocentric Video
- Locator: 1 Introduction
- Evidence: 原文直接给出单一质量分数会混淆的两类异质性。
- Quote: “A single scalar quality per hand would average wrist global drift with finger articulation error and ignore asymmetric bimanual occlusion, informing our four-channel signal indexed by hand and component.”
- Authors: huajian-zeng; chaohua-yao; yuantai-zhang; et al.

### EA-EGOHAND-2026-0026

- Claim: Egocentric 4D 手重建同时受移动相机、严重自遮挡、有限视角、快速手动与双手交互影响。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19156](https://arxiv.org/abs/2606.19156) Hand-4DGS: Feed-Forward 3D Gaussian Splatting for 4D Hand Reconstruction from Egocentric Videos
- Locator: 1 Introduction
- Evidence: 原文在问题定义中直接列出了移动相机、遮挡、视角、快速运动和双手交互等耦合困难。
- Quote: “Body reconstruction methods typically assume a static camera observing a single person, whereas egocentric scenarios involve a moving camera, severe self-occlusions, limited viewpoints, rapid hand motion, and interactions between two hands.”
- Authors: jeongmin-bae; seoha-kim; marc-pollefeys; et al.

### EA-EGOHAND-2026-0004

- Claim: 在真实环境中获得精确 3D 手真值仍依赖多相机、同步、标定和重型移动采集硬件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.02601](https://arxiv.org/abs/2510.02601) Ego-Exo 3D Hand Tracking in the Wild with a Mobile Multi-Camera Rig
- Locator: 3.1 Mobile Capture Rig
- Evidence: 原文的硬件章节表明高精度真值来自多视图、MoCap、硬同步和标定的组合。
- Quote: “All ten monochrome cameras and the five MoCap cameras are hardware-synchronized and precisely calibrated into a shared three-dimensional reference frame.”
- Authors: patrick-rim; kun-he; kevin-harris; et al.

### EA-EGOHAND-2026-0008

- Claim: 开放词表世界坐标 HOI 恢复的精度目前以重型离线管线为代价，不等于可实时部署。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.01050](https://arxiv.org/abs/2601.01050) EgoGrasp: World-Space Hand-Object Interaction Estimation from Egocentric Videos
- Locator: 4.1 Implementation Details & Metrics
- Evidence: 推理设置明确使用 200 步扩散采样，且前文还有多步测试时优化。
- Quote: “For inference, we applied DDIM [ song2020denoising ] sampling with 200 steps, and downsampled sequences by 3 at preprocessing stage.”
- Authors: hongming-fu; wenjia-wang; xiaozhen-qiao; et al.

### EA-EGOHAND-2026-0010

- Claim: 手背皮肤形变只是条件性遮挡补充信号；手背不可见、低分辨率或快速运动会削弱其价值。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.15516](https://arxiv.org/abs/2601.15516) DeltaDorsal: Enhancing Hand Pose Estimation with Dorsal Features in Egocentric Views
- Locator: 8. Discussion
- Evidence: 作者在泛化讨论中明确限定手背特征的可见性条件。
- Quote: “Secondly, we acknowledge that our approach leveraging purely dorsal features for pose estimation is only applicable for a portion of in-the-wild scenarios where the dorsum of the hand is visible.”
- Authors: william-huang; siyou-pei; leyi-zou; et al.

### EA-EGOHAND-2026-0012

- Claim: 当前纯合成数据不能替代真实 egocentric HOI 数据；它主要是少标签和域适应下的补充资源。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.29733](https://arxiv.org/abs/2603.29733) Leveraging Synthetic Data for Enhancing Egocentric Hand-Object Interaction Detection
- Locator: 5 Discussion
- Evidence: 讨论章直接给出纯合成方案的边界。
- Quote: “Currently, synthetic data alone cannot fully replace real-world data for egocentric HOI detection.”
- Authors: rosario-leonardi; antonino-furnari; francesco-ragusa; et al.

### EA-EGOHAND-2026-0015

- Claim: TouchMoment 的自动训练标注与手工标签平均相差 1.94 帧，这与严格评测容差处于同一量级。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.12343](https://arxiv.org/abs/2604.12343) Detecting Precise Hand Touch Moments in Egocentric Video
- Locator: 3.2 Touch Annotation
- Evidence: 原文给出自动工具相对手工标注的帧级差异。
- Quote: “On a held-out subset with full manual annotation, this automatic tool differs from manual labels by an average of 1.94 frames, demonstrating sufficient accuracy for large-scale training data.”
- Authors: huy-anh-nguyen; feras-dayoub; minh-hoai

### EA-EGOHAND-2026-0017

- Claim: 双目事件的几何增益以更高硬件、标定和算力成本为代价，超低功耗部署仍需压缩。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.12297](https://arxiv.org/abs/2605.12297) EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras
- Locator: V-I Limitations
- Evidence: 作者在限制章明确承认当前架构对超低功耗部署仍有额外工程需求。
- Quote: “To facilitate deployment on ultra-low-power wearable devices with stringent power budgets, such overhead can be further mitigated through model compression or quantization techniques.”
- Authors: luming-wang; hao-shi; jiajun-zhai; et al.

### EA-EGOHAND-2026-0022

- Claim: 视觉与 6-DoF IMU 的互补只有在准确同步下成立：视觉锚定全局位置，IMU 补足遮挡下的高频指部运动。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.21714](https://arxiv.org/abs/2605.21714) AVI-HT: Adaptive Vision-IMU Fusion for 3D Hand Tracking
- Locator: 1 Introduction
- Evidence: 该句在上下文中明确指向视觉全局锚点与 IMU 局部动力学的互补。
- Quote: “Therefore, fusing the two recovers what each modality alone cannot.”
- Authors: ziyi-kou; ankit-kumar; mia-huang; et al.

### EA-EGOHAND-2026-0001

- Claim: 事件手追踪存在显著视角域差：第三视角模型直接用于第一视角时性能会严重下降。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.13883](https://arxiv.org/abs/2509.13883) EvHand-FPV: Efficient Event-Based 3D Hand Tracking from First-Person View
- Locator: IV-B Comparison with Prior Work
- Evidence: 原文在同一表中报告了 EventHands 直接跨视角迁移的下降。
- Quote: “However, when applied to our first-person perspective (egocentric) task, its performance drops dramatically to only 0.12 2D-AUCp on real data and 0.17 3D-AUC on synthetic data, demonstrating the significant domain gap between viewpoints and the necessity of EvHand-FPV.”
- Authors: zhen-xu; guorui-lu; chang-gao; et al.

### EA-EGOHAND-2026-0003

- Claim: 受控数据上训练的 3D 手追踪器不能保证野外泛化；在 EgoExo-Hands 上的 MKPE 从域内约 9–11 mm 上升到 16.28 mm。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.02601](https://arxiv.org/abs/2510.02601) Ego-Exo 3D Hand Tracking in the Wild with a Mobile Multi-Camera Rig
- Locator: 3.3 Quantitative Evaluation
- Evidence: 该结论由同节 Table 2 的域内和跨域 MKPE 直接支持。
- Quote: “Models trained on existing datasets, UmeTrack [ 9 ] and HOT3D [ 2 ] , generalize significantly worse to EgoExo-Hands, highlighting the increased difficulty of our in-the-wild data.”
- Authors: patrick-rim; kun-he; kevin-harris; et al.

### EA-EGOHAND-2026-0005

- Claim: 流式手追踪/预测中，素朴时序记忆可能比无记忆更差，因为背景 token 会检索并放大历史队列中的自回归误差。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18127](https://arxiv.org/abs/2511.18127) SFHand: Learning Embodied Manipulation by Streaming Egocentric 3D Hand Forecasting
- Locator: 5.3.2 Ablation on ROI-enhanced memory
- Evidence: 该句由同节 Table 4 的 ADE/FDE 消融数据直接支持。
- Quote: “The vanilla memory without ROI enhancement performs even worse than the no-memory baseline.”
- Authors: ruicong-liu; yifei-huang; liangyang-ouyang; et al.

### EA-EGOHAND-2026-0006

- Claim: 自回归追踪/预测必须显式管理自身误差累积；被存入的错误可以被后续时刻再次检索并放大。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.18127](https://arxiv.org/abs/2511.18127) SFHand: Learning Embodied Manipulation by Streaming Egocentric 3D Hand Forecasting
- Locator: 5.3.2 Ablation on ROI-enhanced memory
- Evidence: 作者在消融解释中直接给出了记忆导致误差放大的机制。
- Quote: “This can amplify error, as autoregressive prediction errors stored in the memory queue ( ) are retrieved and propagated by non-salient parts of the current query ( ).”
- Authors: ruicong-liu; yifei-huang; liangyang-ouyang; et al.

### EA-EGOHAND-2026-0011

- Claim: 裸手预训练的视觉手追踪器在传感手套上存在大幅外观域差，每种新手套都可能需要新的适配数据。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.05159](https://arxiv.org/abs/2602.05159) AirGlove: Exploring Egocentric 3D Hand Tracking and Appearance Generalization for Sensing Gloves
- Locator: 5 Evaluation
- Evidence: 原文在四类手套评测表后直接总结了裸手到手套的性能下降。
- Quote: “We observe that both MEgATrack and UmeTrack show substantially degraded performance on sensing gloves compared to bare-hands.”
- Authors: wenhui-cui; ziyi-kou; chuan-qin; et al.

### EA-EGOHAND-2026-0013

- Claim: HOI-Synth 的证据是单帧检测证据，不包含轨迹连续性或时序追踪能力。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.29733](https://arxiv.org/abs/2603.29733) Leveraging Synthetic Data for Enhancing Egocentric Hand-Object Interaction Detection
- Locator: 5.1 Limitations and future work
- Evidence: 限制章明确声明不使用时序信息。
- Quote: “Our analysis is restricted to frame-level HOS detection and does not exploit temporal information.”
- Authors: rosario-leonardi; antonino-furnari; francesco-ragusa; et al.

### EA-EGOHAND-2026-0014

- Claim: 精确触碰时刻检测不是普通手检测；它还需区分强自运动、近距遮挡和视觉上几乎相同的近接触帧。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.12343](https://arxiv.org/abs/2604.12343) Detecting Precise Hand Touch Moments in Egocentric Video
- Locator: 1 Introduction
- Evidence: 原文直接列出了接触时刻定位中的第一视角特有干扰。
- Quote: “Rapid head motion introduces strong egomotion, while approaching hands often create severe occlusions and perspective distortions at close range.”
- Authors: huy-anh-nguyen; feras-dayoub; minh-hoai

### EA-EGOHAND-2026-0016

- Claim: 事件相机不会自动消除 egocentric 干扰：头部运动生成的背景事件会与手运动信号耦合。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.12297](https://arxiv.org/abs/2605.12297) EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras
- Locator: I Introduction
- Evidence: 原文直接描述了头部自运动对事件流的混入机制。
- Quote: “However, processing such asynchronous event video streams in egocentric settings is fundamentally challenged by ego-motion noise: continuous head movements induce background events that couple with hand-generated signals and severely complicate feature decoupling [ 22 , 34 ] .”
- Authors: luming-wang; hao-shi; jiajun-zhai; et al.

### EA-EGOHAND-2026-0019

- Claim: 跨镜头单网络仍依赖已标定 3D 训练数据和相机内参，不等于无标定野外泛化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.12498](https://arxiv.org/abs/2605.12498) EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera
- Locator: 5. Limitations
- Evidence: 作者在限制章明确把已标定 3D 训练依赖与野外泛化不足联系起来。
- Quote: “It relies on calibrated 3D datasets for training, preventing the use of large 2D hand datasets common in root-relative methods (Pavlakos et al. , 2024 ; Potamias et al. , 2024 ) and limiting generalization to in-the-wild imagery.”
- Authors: christen-millerdurai; shaoxiang-wang; yaxu-xie; et al.

### EA-EGOHAND-2026-0021

- Claim: 当上游视觉完全没有可靠观测锚点时，生成恢复只能产生合理先验，可能形成错误轨迹。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.18553](https://arxiv.org/abs/2605.18553) StableHand: Quality-Aware Flow Matching for World-Space Dual-Hand Motion Estimation from Egocentric Video
- Locator: Appendix H Additional Qualitative Results
- Evidence: 作者在失败案例中明确区分了“合理”与“正确”。
- Quote: “In both cases the generative process synthesizes a plausible but incorrect trajectory from the prior alone, illustrating the limit of our method when the upstream visual stream provides no observation to anchor a channel.”
- Authors: huajian-zeng; chaohua-yao; yuantai-zhang; et al.

### EA-EGOHAND-2026-0023

- Claim: 手套型多模态追踪会引入新的外观域差，且对不同手套布局和 IMU 规格的泛化尚未验证。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.21714](https://arxiv.org/abs/2605.21714) AVI-HT: Adaptive Vision-IMU Fusion for 3D Hand Tracking
- Locator: 6 Conclusion
- Evidence: 原文在结论的限制段明确将跨手套泛化列为未验证问题。
- Quote: “In addition, since our experiments use a specific type of data sensing glove, the generalization to other gloves with different sensor layouts, form factors, or IMU specifications remains to be validated.”
- Authors: ziyi-kou; ankit-kumar; mia-huang; et al.

### EA-EGOHAND-2026-0024

- Claim: 事件手检测的精度仍受慢变信号不可见与将事件流重新帧化的处理低效限制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.10790](https://arxiv.org/abs/2606.10790) A Multimodal RGB and Events Dataset for Hand Detection in First-Person View
- Locator: I Introduction
- Evidence: 原文直接列出了事件传感器与处理表示两类瓶颈。
- Quote: “But event-based approaches currently face limitations in accuracy due to two main factors: the sensors’ inability to detect slowly changing signals and the inefficiency of existing processing techniques that transform event streams into frame- based formats for analysis using convolutional neural networks [ 31 , 22 , 1 ] .”
- Authors: bharghav-kota; yulia-sandamirskaya

### EA-EGOHAND-2026-0027

- Claim: Hand-4DGS 的定量结果排除了手大部分出框或上游无法正确检测双手的帧，因而不能外推到最难丢检场景。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19156](https://arxiv.org/abs/2606.19156) Hand-4DGS: Feed-Forward 3D Gaussian Splatting for 4D Hand Reconstruction from Egocentric Videos
- Locator: C.2 Training Setup and Model Architecture
- Evidence: 数据处理细节明确列出了两类被排除的高难样本。
- Quote: “We perform training and evaluation only when both hands are sufficiently visible in the image. Specifically, we exclude instances where more than half of a bounding box area is outside the image or when HaMeR fails to detect both hands correctly.”
- Authors: jeongmin-bae; seoha-kim; marc-pollefeys; et al.

### EA-EGOHAND-2026-0029

- Claim: 将中心帧的接触标注传播到整个 clip 会受手边别错误和相机跳变污染，需保留每帧置信度。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.30598](https://arxiv.org/abs/2606.30598) Towards in-the-wild Egocentric 3D Hand-Object Pose Estimation
- Locator: 10 Limitations and Future Directions
- Evidence: 作者在限制中明确列出了标签传播的两类时序噪声。
- Quote: “Additionally, we propagate manually-verified ground-truth from a single frame to a clip. Propagation can be noisy due to errors in hand pose estimates from WiLoR [ Potamias_2025_CVPR_wilor ] (hand-side errors or camera placement jumps).”
- Authors: siddhant-bansal; zhifan-zhu; shashank-tripathi; et al.

### EA-EGOHAND-2026-0002

- Claim: 真实事件数据缺少 3D 真值，导致该方法的真实 3D 指标无法被直接验证。
- Stance: `gap` | Confidence: `direct`
- Paper: [2509.13883](https://arxiv.org/abs/2509.13883) EvHand-FPV: Efficient Event-Based 3D Hand Tracking from First-Person View
- Locator: IV-A2 3D Metric
- Evidence: 原文明确将 3D 评测限定在合成数据。
- Quote: “However, due to the inherent difficulties in obtaining 3D annotations for real-world data, our evaluation of this metric is limited to synthetic data.”
- Authors: zhen-xu; guorui-lu; chang-gao; et al.

### EA-EGOHAND-2026-0025

- Claim: 现有 EventEgoHands 仍缺少光照、肤色和活动多样性，真实数据覆盖是未解问题。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.10790](https://arxiv.org/abs/2606.10790) A Multimodal RGB and Events Dataset for Hand Detection in First-Person View
- Locator: V conclusion and further work
- Evidence: 未来工作明确列出了数据人群与场景多样性边界。
- Quote: “Future work includes creating an event-based Hands dataset in first-person view with more variation in lighting conditions, skin tones and activity being performed.”
- Authors: bharghav-kota; yulia-sandamirskaya

### EA-EGOHAND-2026-0028

- Claim: 野外 egocentric 手物 3D 估计的主要数据瓶颈是重遮挡与接触歧义下缺少便宜、可扩展的 3D 监督。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.30598](https://arxiv.org/abs/2606.30598) Towards in-the-wild Egocentric 3D Hand-Object Pose Estimation
- Locator: 1 Introduction
- Evidence: 该句所在段落将野外遮挡/接触歧义与 MoCap 成本、环境空洞联系起来。
- Quote: “A central bottleneck is the availability of supervision.”
- Authors: siddhant-bansal; zhifan-zhu; shashank-tripathi; et al.

## References

- `2509.13883` [EvHand-FPV: Efficient Event-Based 3D Hand Tracking from First-Person View](https://arxiv.org/abs/2509.13883) (2025-09-17)
- `2510.02601` [Ego-Exo 3D Hand Tracking in the Wild with a Mobile Multi-Camera Rig](https://arxiv.org/abs/2510.02601) (2025-10-02)
- `2511.18127` [SFHand: Learning Embodied Manipulation by Streaming Egocentric 3D Hand Forecasting](https://arxiv.org/abs/2511.18127) (2025-11-22)
- `2601.01050` [EgoGrasp: World-Space Hand-Object Interaction Estimation from Egocentric Videos](https://arxiv.org/abs/2601.01050) (2026-01-03)
- `2601.15516` [DeltaDorsal: Enhancing Hand Pose Estimation with Dorsal Features in Egocentric Views](https://arxiv.org/abs/2601.15516) (2026-01-21)
- `2602.05159` [AirGlove: Exploring Egocentric 3D Hand Tracking and Appearance Generalization for Sensing Gloves](https://arxiv.org/abs/2602.05159) (2026-02-05)
- `2603.29733` [Leveraging Synthetic Data for Enhancing Egocentric Hand-Object Interaction Detection](https://arxiv.org/abs/2603.29733) (2026-03-31)
- `2604.12343` [Detecting Precise Hand Touch Moments in Egocentric Video](https://arxiv.org/abs/2604.12343) (2026-04-14)
- `2605.12297` [EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras](https://arxiv.org/abs/2605.12297) (2026-05-12)
- `2605.12498` [EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera](https://arxiv.org/abs/2605.12498) (2026-05-12)
- `2605.18553` [StableHand: Quality-Aware Flow Matching for World-Space Dual-Hand Motion Estimation from Egocentric Video](https://arxiv.org/abs/2605.18553) (2026-05-18)
- `2605.21714` [AVI-HT: Adaptive Vision-IMU Fusion for 3D Hand Tracking](https://arxiv.org/abs/2605.21714) (2026-05-20)
- `2606.10790` [A Multimodal RGB and Events Dataset for Hand Detection in First-Person View](https://arxiv.org/abs/2606.10790) (2026-06-09)
- `2606.19156` [Hand-4DGS: Feed-Forward 3D Gaussian Splatting for 4D Hand Reconstruction from Egocentric Videos](https://arxiv.org/abs/2606.19156) (2026-06-17)
- `2606.30598` [Towards in-the-wild Egocentric 3D Hand-Object Pose Estimation](https://arxiv.org/abs/2606.30598) (2026-06-29)
