# Evidence Appendix: 无本体ego-centric数据中手部检测精度对本体末端轨迹的影响

- Time range: 2025-09-01..2026-08-31
- Events: 357
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-EGOPREC-2026-0016

- Claim: 以点轨作为本体无关中间表征的预测模型（Track2Act）可直接在含 ego-centric 人类视频（EpicKitchens）的网络视频混合语料上训练，且在 held-out 视频上的点轨预测精度（∆=0.67-0.77）显著优于 flow 基线（0.21-0.42）与先生成视频再追踪的基线（0.17-0.30），说明绕开显式手部姿态估计、改用点轨从人类视频中学习运动计划是可行的。
- Stance: `support` | Confidence: `direct`
- Paper: [2405.01527](https://arxiv.org/abs/2405.01527) Track2Act: Predicting Point Tracks from Internet Videos enables Generalizable Robot Manipulation
- Locator: 5.1 Point Track Prediction Results, Table 1
- Evidence: Table 1 在 EpicKitchens、SmthSmthv2（人类视频）与 BridgeData、RT1（机器人视频）四个 held-out 集上报告单一模型的 ∆ 指标，Ours 行 0.67/0.70/0.77/0.75，均大幅高于 Flow 与 Video 基线；4.3 与附录 6.5 确认训练混合了 EpicKitchens ego-centric 片段。
- Quote: “Table 1: Evaluation of track prediction performance on held-out videos from different datasets on the web. EpicKitchens [10] and SmthSmthv2 [21] are datsets of human videos, and BridgeData [61] and RT1 data [8] are datasets of robot videos. Note that we train a single model that we evaluate on these different datasets. The metric ∆ is defined in section 4.1. Higher is better and the range is from 0 to 1. EpicKitchens [10] SmthSmthv2 [21] BridgeData [61] RT1 Data [8] Flow [67] 0.21 0.27 0.42 0.38”
- Authors: homanga-bharadhwaj; roozbeh-mottaghi; abhinav-gupta; et al.

### EA-EGOPREC-2026-0019

- Claim: 在利用 ego-centric 人类视频（EpicKitchens）构建训练数据时，作者以'片段画面中可见人手'作为筛选标准（将长视频切成 4-5 秒片段并保留手部可见者），以此近似保证片段内发生了物体操作；即在该点轨管线中，手部检测只作为数据清洗信号，而非姿态监督来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2405.01527](https://arxiv.org/abs/2405.01527) Track2Act: Predicting Point Tracks from Internet Videos enables Generalizable Robot Manipulation
- Locator: Appendix, 6.5 Training Data for Track Prediction
- Evidence: 附录 6.5 逐字说明 EpicKitchens 片段筛选标准；全文方法（3.2）不含任何手部姿态估计模块，与'仅作筛选信号'的表述一致。
- Quote: “Epic- Kitchens contains ego-centric videos of humans in different locations performing diverse tasks in kitchens. Since these videos are long (≥ 20 min each), we choose clips of duration 4-5 seconds by cutting the long videos, and choosing clips where a human hand is visible in the scene (so as to have clips where an object is being manipulated, instead of a person just moving around).”
- Authors: homanga-bharadhwaj; roozbeh-mottaghi; abhinav-gupta; et al.

### EA-EGOPREC-2026-0477

- Claim: 在相同 Vision Pro 手部追踪源与相同双臂硬件下，Bunny-VisionPro 的重定向+运动控制优化使 6 个自建双臂任务中手臂关节位置变化（∆Qpos）较 AnyTeleop+ 低约 43%，AnyTeleop+ 在复杂轨迹与大末端位姿变化下出现激进、不可预测且可能不安全的关节运动。
- Stance: `support` | Confidence: `direct`
- Paper: [2407.03162](https://arxiv.org/abs/2407.03162) Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning
- Locator: 4.2 Real Robot Teleoperation Experiments, Table 3
- Evidence: 4.2 正文报告 AnyTeleop+ 手臂关节位置变化高 43% 并描述其激进运动；Table 3 给出各任务 ∆Qpos 原始值（如 Grasp Toy 0.35 vs 0.77）。
- Quote: “In contrast, AnyTeleop+ struggles with complex trajectories and large end-effector pose changes, often leading to aggressive joint movements and unpredictable, potentially unsafe robot control, as evidenced by a 43% increase in arm joint position changes during tasks.”
- Authors: runyu-ding; yuzhe-qin; jiyue-zhu; et al.

### EA-EGOPREC-2026-0478

- Claim: 用 Bunny-VisionPro 采集的演示训练 ACT/Diffusion Policy/DP3，平均成功率较 AnyTeleop+ 演示高 22%；泛化上空间新位置 +14% SR-SG、未见物体 +26% SR-U，作者据此认为高质量、轨迹一致的演示显著提升模仿学习泛化。
- Stance: `support` | Confidence: `direct`
- Paper: [2407.03162](https://arxiv.org/abs/2407.03162) Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning
- Locator: 5 Imitation Learning, Table 4
- Evidence: 5.1 正文给出 22%/14%/26% 三个数值与轨迹一致性解释；Table 4 提供三任务×三策略的逐格成功率。
- Quote: “As shown in Tab. 4, Bunny-VisoinPro significantly outperforms AnyTeleop+ by an average of 22% success rate across three tasks using three different policies. This showcases the superior quality of the demonstrations collected by our system.”
- Authors: runyu-ding; yuzhe-qin; jiyue-zhu; et al.

### EA-EGOPREC-2026-0479

- Claim: Bunny-VisionPro 的手部重定向（含 loop joint）单帧耗时 3.43ms、含奇异与碰撞规避的完整运动控制 15.93ms，系统在 CPU 上整体 >60Hz 实时运行；loop joint 降维求解较等式约束法（34.98ms）提速约 10.2 倍，使全自由度灵巧重定向不成为延迟来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2407.03162](https://arxiv.org/abs/2407.03162) Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning
- Locator: 4.2 Real Robot Teleoperation Experiments, Table 1
- Evidence: Table 1 剖析各模块毫秒级耗时；4.1 正文确认 >60Hz；3.2 报告 10.2 倍提速；引言指出延迟→不精确运动。
- Quote: “CPU i7-12700KF Module Time (ms) Retargeting (w/o loop joints) 2.54 Retargeting (loop joints as Cons.) 34.98 Retargeting (loop joints ours) 3.43 Motion Control (IK only) 0.74 Motion Control (+ Coll.) 7.85 Motion Control (+ Sing.) 10.42 Motion Control (+ Coll. + Sing.) 15.93 Haptic Feedback (PWM) 0.04”
- Authors: runyu-ding; yuzhe-qin; jiyue-zhu; et al.

### EA-EGOPREC-2026-0481

- Claim: Bunny-VisionPro 的手部重定向目标函数显式包含时序平滑项 β\|\|∆q\|\|²，对相邻帧间大幅关节位置变化施加惩罚，从算法层面抑制逐帧手部追踪噪声向机器人关节命令的传导。
- Stance: `support` | Confidence: `direct`
- Paper: [2407.03162](https://arxiv.org/abs/2407.03162) Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning
- Locator: 3.2 Robot Hand Motion Retargeting
- Evidence: 3.2 式(1)第二项逐字说明对连续帧间 ∆q 的惩罚；该项与关键点向量误差项共同构成重定向目标。
- Quote: “The second term enforces temporal smoothness by penal- izing large joint position changes ∆q between consecutive frames, with weight β.”
- Authors: runyu-ding; yuzhe-qin; jiyue-zhu; et al.

### EA-EGOPREC-2026-0001

- Claim: 在 HO3D 逐帧 4D 重建中，WiLoR 的帧间抖动指标 MPFJE 0.762(×100)、Jitter 5.92、手腕根位移误差 RTE 0.07，显著低于 HaMeR 的 1.768、20.43、2.92；RTE 度量手腕跨帧位移，作者将无时序模块下的低抖动归因于检测的稳健性。
- Stance: `support` | Confidence: `direct`
- Paper: [2409.12259](https://arxiv.org/abs/2409.12259) WiLoR: End-to-end 3D Hand Localization and Reconstruction in-the-wild
- Locator: 5.3. Evaluation of Dynamic Reconstruction, Table 6
- Evidence: Table 6 逐行报告各方法 MPFVE/MPFJE/Jitter/RTE，表后正文给出 RTE 的手腕位移定义与对检测稳定性的归因。
- Quote: “HaMeR [63] 10.60 1.768 20.43 2.92 Proposed 4.43 0.762 5.92 0.07 Table 6. Reconstruction of dynamic 3D Hands. We evaluate the temporal coherence and the jittering of the reconstruction for the proposed and the baseline methods on the HO3D dataset. similar to [77], we measure the jerk (Jitter) of the 3D hand joints motion along with the global Root Translation Error (RTE) that measures the displacement of the wrist across frames. In Tab. 6, we report the reconstruction results for the best perform”
- Authors: rolandos-alexandros-potamias; zhang-jinglei; jiankang-deng; et al.

### EA-EGOPREC-2026-0002

- Claim: 在手-物交互基准 HO3Dv2 上，WiLoR 达到 PA-MPJPE 7.5mm、PA-MPVPE 7.7mm、AUC_J 0.851，优于 HaMeR 的 7.7mm/7.9mm/0.846，代表当前单帧相机系手部重建的 SOTA 精度水平。
- Stance: `support` | Confidence: `direct`
- Paper: [2409.12259](https://arxiv.org/abs/2409.12259) WiLoR: End-to-end 3D Hand Localization and Reconstruction in-the-wild
- Locator: 5.2. Evaluation of 3D Hand Pose Estimation, Table 4
- Evidence: Table 4 在 HO3Dv2 协议下逐行报告 AUC/PA-MPJPE/PA-MPVPE，WiLoR 全部指标最优；表注确认单位为 mm。
- Quote: “HaMeR 0.846 7.7 0.841 7.9 0.635 0.980 Proposed 0.851 7.5 0.846 7.7 0.646 0.983 Table 4. Comparison with the state-of-the-art on the HO3D dataset [25]. We use the HO3Dv2 protocol and report metrics that evaluate accuracy of the estimated 3D joints and 3D mesh. PA-MPVPE and PA-MPJPE numbers are in mm.”
- Authors: rolandos-alexandros-potamias; zhang-jinglei; jiankang-deng; et al.

### EA-EGOPREC-2026-0085

- Claim: EgoMimic 将人-机器人末端位姿分布差异部分归因于两侧的测量精度差异，并以逐源高斯归一化对齐动作分布；Object-in-Bowl 消融中去除动作归一化导致任务得分下降 38%（128→79 分），说明该对齐是人体手部追踪数据可用性的关键前提。
- Stance: `support` | Confidence: `direct`
- Paper: [2410.24221](https://arxiv.org/abs/2410.24221) EgoMimic: Scaling Imitation Learning via Egocentric Video
- Locator: B. Results; B. Data Processing and Domain Alignment
- Evidence: III-B 明确列出 'measurement precision disparities between human and robotic systems' 作为分布差异来源之一；IV-B/Table IV 报告去除归一化的 -38% 消融。
- Quote: “First, removing action normalization results in a 38% drop in task score.”
- Authors: simar-kareer; dhruv-patel; ryan-punamiya; et al.

### EA-EGOPREC-2026-0086

- Claim: 在 Object-in-Bowl 上，EgoMimic 用 2 小时机器人数据+1 小时 Aria 手部追踪人体数据（128 分）显著优于 3 小时纯机器人数据训练的 ACT（74 分）；1 小时人体数据产出 1400 条演示而机器人 1 小时仅约 135 条。
- Stance: `support` | Confidence: `direct`
- Paper: [2410.24221](https://arxiv.org/abs/2410.24221) EgoMimic: Scaling Imitation Learning via Egocentric Video
- Locator: B. Results
- Evidence: IV-B scaling 段落给出 128 vs 74 分对比与每小时演示数对比；对照 ACT 使用更多机器人数据。
- Quote: “EgoMimic trained on 2 hours of robot data and 1 hour of human data significantly outperforms ACT trained on 3 hours of robot data (128 vs 74”
- Authors: simar-kareer; dhruv-patel; ryan-punamiya; et al.

### EA-EGOPREC-2026-0007

- Claim: 遮挡率升高显著退化相机系手部姿态精度：DexYCB 上 WiLoR 的 PA-MPJPE 从全部帧 5.01mm 升至 75-100% 遮挡帧 5.68mm（AUC 90.0→88.7），HaWoR 凭借时序图像/姿态先验从 4.76mm 仅升至 5.07mm（AUC 90.5→89.9）；作者同时指出 ego 视频有限视场导致的手部边界截断会显著恶化姿态估计框架性能。
- Stance: `support` | Confidence: `direct`
- Paper: [2501.02973](https://arxiv.org/abs/2501.02973) HaWoR: World-Space Hand Motion Reconstruction from Egocentric Videos
- Locator: 4.1. Camera-frame 3D Hand Motion / Methods (Table 1)
- Evidence: Table 1 按遮挡比例分三档报告 PA-MPJPE/AUC；3.1 节明确将边界截断列为恶化姿态估计的挑战。
- Quote: “WiLoR [32] 5.01 90.0 5.42 89.2 5.68 88.7 temporal S 2 HAND(V) [39] 7.27 85.5 7.71 84.6 7.87 84.3 VIBE [21] 6.43 87.1 6.84 86.4 7.06 85.8 TCMR [10] 6.28 87.5 6.58 86.8 6.95 86.1 Deformer [14] 5.22 89.6 5.70 88.6 6.34 87.3 Proposed 4.76 90.5 5.03 89.9 5.07 89.9 Table 1. Quantitative camera-frame comparison of state-of-the- art hand pose estimation methods on the DexYCB test dataset. We compare PA-MPJPE and AUC results, especially the split un- der large occlusion proportion (50%-75% and 75%-100%)”
- Authors: jinglei-zhang; jiankang-deng; chao-ma; et al.

### EA-EGOPREC-2026-0355

- Claim: 用估计手部姿态生成动作标签、inpainting 人臂并叠加渲染机器人的 Hand Inpaint(Phantom)在 5 个场内任务达 0.40-0.92 成功率(Pick/Place Book 0.92)，OOD 场景 0.64-0.84；而不做视觉对齐的 Vanilla 与 Red Line 编辑在所有任务上成功率为 0。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.00779](https://arxiv.org/abs/2503.00779) Phantom: Training Robots Without Robots Using Only Human Videos
- Locator: 4.2 In-distribution Scene, Table 1
- Evidence: Table 1/Table 2 报告 Hand Inpaint 各任务成功率与 Vanilla/Red Line 全零结果。
- Quote: “Hand Inpaint (Phantom) 0.92 0.72 0.64 0.72 0.88 0.80 0.72 0.40 Hand Mask 0.92 0.52 0.60 0.76 0.75 0.75 0.72 0.68 Red Line 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 Vanilla 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 Table 1: In-distribution scene results: Both Hand Inpaint and Hand Mask achieve high success rates across all tasks. The Red Line strategy fails to achieve success on any task, as does the Vanilla baseline.”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0502

- Claim: 将少量动觉示教数据与 VR 遥操作数据混合训练，最优模型平均成功率比任一单模态数据高 20%；在 Flip Glass 上 100 条混合示教达 75% 成功率，比 100 条纯动觉示教的最优模型高 5 个百分点。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.07017](https://arxiv.org/abs/2503.07017) How to Train Your Robots? The Impact of Demonstration Modality on Imitation Learning
- Locator: V. RESULTS
- Evidence: 结果节直接给出 20% 平均提升与 Flip Glass 75%（+5%）两个数字，对应图 10 与图 11。
- Quote: “We see that the best-performing models with mixed data outperform single-modality baseline by 20% on average. In Flip Glass, the model trained with a total of 100 mixed demonstrations achieves 75% success rate, outperforming (+5%) the best model using all 100 kinesthetic demonstrations (Fig. 5).”
- Authors: haozhuo-li; yuchen-cui; dorsa-sadigh

### EA-EGOPREC-2026-0503

- Claim: 采集模态决定数据的轨迹统计特征：动觉示教在无接触力任务上动作方差与最大 jerkiness 最低，而遥操作数据空间散布更广、状态多样性更高；Push Sanitizer 上动觉示教反而动作方差与 jerkiness 最高。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.07017](https://arxiv.org/abs/2503.07017) How to Train Your Robots? The Impact of Demonstration Modality on Imitation Learning
- Locator: V. RESULTS
- Evidence: 结果节数据分析段直接报告各模态轨迹散布与动作方差/jerkiness 的相对关系；图 9 配文总结动觉示教动作方差与最大 jerkiness 更低（除接触力任务）。
- Quote: “We observe that kinesthetic teaching leads to data with relatively low action variance in the two tasks without contact force, but high action variance and jerkiness in the Push Sanitizer task.”
- Authors: haozhuo-li; yuchen-cui; dorsa-sadigh

### EA-EGOPREC-2026-0320

- Claim: 在 8 个仿真灵巧任务上，MAPLE 以 31.9%±1.2 的平均成功率超过全部通用与操作专用基线（次优 DINO 28.8%±1.2），领先幅度超过两个标准差；在真实 ORCA 灵巧手三任务上 MAPLE 成功率均为最高且是唯一未触发安全 abort 的方法。
- Stance: `support` | Confidence: `direct`
- Paper: [2504.06084](https://arxiv.org/abs/2504.06084) MAPLE: Encoding Dexterous Robotic Manipulation Priors Learned From Egocentric Videos
- Locator: 4.2. Evaluation in Simulation Environments
- Evidence: 4.2 主结果段与 Table 2 给出均值与标准差比较；4.3 失效分析给出真实任务最高成功率与零 abort。
- Quote: “MAPLE achieves the best overall performance among all methods, exceeding the second-best approach by more than two standard deviations”
- Authors: alexey-gavryushin; xi-wang; robert-j-s-malate; et al.

### EA-EGOPREC-2026-0084

- Claim: 以 ARKit 采集时追踪为真值的 EgoDex 基准上，SOTA 模仿策略预测双手 48 维腕部+指尖轨迹的平均 3D 关键点误差约 4.4-4.5 cm（2 秒 horizon，K=1）；预测 horizon 加长误差增大（H=1s/2s/3s 时 Dec+BC 平均距离分别为 0.031/0.045/0.053 m）。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.11709](https://arxiv.org/abs/2505.11709) EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video
- Locator: Section 5 Experiments, Tables 2-3 (extraction block: background)
- Evidence: 表 2 给出各模型 2s horizon 的 Avg/Final Distance，表 3 给出 horizon 消融数值；指标定义为 12 个 3D 关键点（双腕+双手指尖）的欧氏距离。
- Quote: “Results for models trained and evaluated with different prediction horizons. As expected, accuracy falls as the prediction horizon increases.”
- Authors: ryan-hoque; peide-huang; david-j-yoon; et al.

### EA-EGOPREC-2026-0364

- Claim: 仅用 Aria 智能眼镜采集的人类演示(每任务 100 条、约 20 分钟采集、零机器人数据)训练的闭环策略，在 7 个操作任务上取得 13/15、11/15、9/15、11/15、11/15、10/15、9/15 的零样本成功率(平均约 70%)；图像策略基线全部 0/15。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.20290](https://arxiv.org/abs/2505.20290) EgoZero: Robot Learning from Smart Glasses
- Locator: Method, Table 1
- Evidence: Table 1 给出 EGOZERO 逐任务成功率与基线对比；摘要报告 70% 平均成功率与 20 分钟/任务采集量。
- Quote: “EGOZERO 13/15 11/15 9/15 11/15 11/15 10/15 9/15 Table 1: Success rates for all baselines and ablations. All models were trained on the same 100 demonstrations per task, and evaluated on zero-shot object poses (unseen from training), cameras (iPhone vs Aria), and environment (robot workspace vs in-the-wild).”
- Authors: vincent-liu; ademi-adeniji; haotian-zhan; et al.

### EA-EGOPREC-2026-0431

- Claim: DexUMI 用外骨骼关节编码器直接读取关节动作，其明确设计动机是消除视觉指尖追踪带来的不准确性——即作者判断视觉手部追踪误差大到需要以硬件传感替代。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.21864](https://arxiv.org/abs/2505.21864) DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation
- Locator: 1 Introduction
- Evidence: Introduction 列举硬件适配四点收益，其中'Capturing precise joint action'一条逐字声明编码器直读可消除视觉指尖追踪的不准确性。
- Quote: “Capturing precise joint action: Unlike retargeting methods, our exoskeleton reads precise joint angles directly from encoders, eliminating inaccuracies due to visual fingertip tracking.”
- Authors: mengda-xu; han-zhang; yifan-hou; et al.

### EA-EGOPREC-2026-0033

- Claim: 移除指尖 pinch 目标项（A1）后，机器人手无法在真实捏取任务中闭合拇指与食指尖间隙，导致涉及 pinch 的任务失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2506.09384](https://arxiv.org/abs/2506.09384) Analyzing Key Objectives in Human-to-Robot Retargeting for Dexterous Manipulation
- Locator: B. Analysis of Results
- Evidence: B 节结果分析报告：A1 在真实世界操作中导致 pinch 类任务失败，原因是无法闭合拇指与食指尖间隙；运动学上 A1 同时显著抬高指尖位置与相对拇指位置误差。
- Quote: “in real-world manipulations, removing the pinch term in A1 leads to failure in tasks involving pinch motions, as it cannot close the gap between thumb and index fingertips (A1 in Task 3, Fig. 4).”
- Authors: xin-chendong; mingrui-yu; yongpeng-jiang; et al.

### EA-EGOPREC-2026-0516

- Claim: 将人类采集数据集 DexYCB 与 ARCTIC 经'重定向人类示教到机器人轨迹+加噪'的管线转为机器人示教后，仅有 62% 和 64% 的轨迹在仿真中成功达成任务目标——人类采集数据经重定向路线进入机器人训练时存在约三分之一的验收损耗。
- Stance: `support` | Confidence: `direct`
- Paper: [2506.17198](https://arxiv.org/abs/2506.17198) Dex1B: Learning with 1B Demonstrations for Dexterous Manipulation
- Locator: V. EXPERIMENTS / B. Dataset Analysis
- Evidence: V-B Dataset Comparison 段报告：遵循既有工作将 DexYCB/ARCTIC 重定向为机器人示教并加噪扩增后，收集到 62%/64% 成功达成任务目标的轨迹。
- Quote: “We collected 62% and 64% of all trajectories from the DexYCB and ARCTIC datasets, respectively, that successfully achieve task goals.”
- Authors: jianglong-ye; keyi-wang; chengjing-yuan; et al.

### EA-EGOPREC-2026-0517

- Claim: 人类采集的 DexYCB/ARCTIC 数据集中关节值分布经常集中于关节极限处，而 Dex1B 通过去偏与关节限位正则化使分布更均匀、集中于均值附近——人类采集路线的示教数据存在结构性分布偏差。
- Stance: `support` | Confidence: `direct`
- Paper: [2506.17198](https://arxiv.org/abs/2506.17198) Dex1B: Learning with 1B Demonstrations for Dexterous Manipulation
- Locator: V. EXPERIMENTS / B. Dataset Analysis
- Evidence: V-B Dataset Comparison 段与图 6 配文：DexYCB/ARCTIC 关节值常集中于关节极限，Dex1B 经去偏与正则化分布更均匀。
- Quote: “Unlike DexYCB and ARCTIC, which often have joint values concetrate at the limits, the distribution of Dex1B is more evenly spread, centering around the mean joint values.”
- Authors: jianglong-ye; keyi-wang; chengjing-yuan; et al.

### EA-EGOPREC-2026-0077

- Claim: 在预训练数据混合消融中，尽管 HoloAssist 手部标注有噪声、HOT3D 缺语言标签、TACO 视觉多样性有限，加入这些源仍带来正向迁移，未见噪声标注导致负迁移。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.12440](https://arxiv.org/abs/2507.12440) EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
- Locator: 5.2 Humanoid Robot Evaluation
- Evidence: Fig. 7 显示数据多样性增加持续提升 Unseen 短程任务的 SR 与 PSR；正文明确将 HoloAssist 标注噪声列为仍获正迁移的瑕疵之一。
- Quote: “we still observe positive transfer, highlighting the robustness of our approach to dataset imperfections.”
- Authors: ruihan-yang; qinxi-yu; yecheng-wu; et al.

### EA-EGOPREC-2026-0078

- Claim: EgoVLA 的人-机手部表示重定向（MANO 拟合+MLP）引入的平均指尖位置误差为 5×10^-5 m，且经该管线回放原始演示仍保持任务有效性，作者据此判断重定向误差对控制性能影响不显著。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.12440](https://arxiv.org/abs/2507.12440) EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
- Locator: 3.3 Transferring EgoVLA to Humanoid Robot
- Evidence: 3.3 节给出指尖拟合误差数值与回放有效性检验；附录 3.3 给出重定向 MLP 结构。
- Quote: “replaying raw demonstrations through this retargeting pipeline preserves task validity, indicating that the small errors introduced during retargeting do not significantly affect control performance.”
- Authors: ruihan-yang; qinxi-yu; yecheng-wu; et al.

### EA-EGOPREC-2026-0079

- Claim: EgoVLA 在人类视频评估集上预测未来腕部平移的平均误差约 8 cm（2D 归一化误差约 0.13），与 HOI-forecast 报告的 SOTA 相当；该量级误差经机器人微调后仍得到 77.78% 的短程任务平均成功率。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.12440](https://arxiv.org/abs/2507.12440) EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
- Locator: 5.1 Human Manipulation Modeling
- Evidence: 5.1 节给出腕部预测误差数值；5.2 节表 1 给出 Seen 配置短程任务平均 SR=77.78%。两者是同一系统的上游预测精度与下游成功率。
- Quote: “the average future prediction error for the human wrist translation is approximately 8, cm. When projected onto the 2D image plane, the normalized error is around 0.13”
- Authors: ruihan-yang; qinxi-yu; yecheng-wu; et al.

### EA-EGOPREC-2026-0359

- Claim: 在 Stack Pots 任务 OOD 场景，共训练所用编辑人类视频比例从 0%/10%/50%/100% 递增时，策略成功率分别为 2%/26%/47%/68%(各 25 次 rollout)：即便标签只是带噪的 2D 手部关键点，编辑后人类视频量的增加仍单调提升机器人策略性能。
- Stance: `support` | Confidence: `direct`
- Paper: [2508.09976](https://arxiv.org/abs/2508.09976) Masquerade: Learning from In-the-wild Human Videos using Data-Editing
- Locator: F. Does increasing the amount of in-the-wild data improve, Fig. 6
- Evidence: Fig. 6 数据规模实验正文报告 2/26/47/68% 四档成功率。
- Quote: “success rates rise steadily with more human-video data: 0% → 2%, 10% → 26%, 50% → 47%, and 100% → 68% (25 rollouts each). This clear upward trend demonstrates that increasing the amount of in-the-wild human videos directly boosts robot performance and suggests further gains could be realized by scaling beyond the current dataset size.”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0368

- Claim: 固定 1 小时静态机器人操作数据，人类移动操作数据从 15 分钟增至 1 小时时 EMMA 成功率从 0.36 升至 0.82；同任务 Mobile ALOHA 的机器人遥操作数据同等增长仅从 0.26 升至 0.52——人类 ego-centric 数据的规模收益持续高于等量采集时间的移动遥操作数据(差距从 10pp 扩到 30pp)。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.04443](https://arxiv.org/abs/2509.04443) EMMA: Scaling Mobile Manipulation via Egocentric Human Data
- Locator: Ablation Study
- Evidence: H3 段与 Fig. 8(b) 报告两条规模曲线的端点数值；正文另述 Handover Wine 1h 人类替换 1h 遥操作 82% vs 52%。
- Quote: “Keeping one hour of static robot manipulation data fixed, EMMA’s success rate climbs steadily from 0.36 to 0.82 as we increase human mobile manipulation data from 15 minutes to one hour (Fig. 8 (b)). Mobile ALOHA also improves from 0.26 to 0.52 when its robot teleoperation data grows from 15 minutes to one hour, but remains consistently below EMMA.”
- Authors: lawrence-y-zhu; pranav-kuppili; ryan-punamiya; et al.

### EA-EGOPREC-2026-0101

- Claim: 本文的从视频恢复手部/腕部轨迹的检测器栈是三级级联：MediaPipe 逐帧定位并裁剪手部 → FrankMocap 的 SMPL-X 回归器输出局部腕部坐标系下 21 个手部关节的 3D 位置 → 关节投影到深度图并解 PnP 恢复相机系腕部 6D 位姿；作者明确判定单目估计的腕部平移空间精度不足——为提升空间精度，用 RGBD 相机深度数据导出的腕部点替代 FrankMocap 估计的腕部平移，腕部方向则由 PnP 精化，且离线视频用绝对位置重定向、实时遥操作用更稳定的深度腕部+向量重定向。这构成'单目手部姿态估计的腕部平移分量是已知精度短板、需以深度传感替代'的工程证据。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.10952](https://arxiv.org/abs/2509.10952) ImMimic: Cross-Domain Imitation from Human Videos via Mapping and Interpolation
- Locator: 3.1 Hand Pose Retargeting System; Appendix
- Evidence: 3.1 描述 MediaPipe→FrankMocap→深度投影+PnP 的完整检测链；Appendix B 明确以深度腕部点替代 FrankMocap 估计的腕部平移以提升空间精度，并区分离线位置重定向与在线向量重定向两种模式。
- Quote: “To improve spatial accuracy, particularly important for teleoperation, we replace FrankMocap’s es- timated wrist translation with a wrist point derived from depth data captured by an RGBD camera.”
- Authors: yangcen-liu; woo-chul-shin; yunhai-han; et al.

### EA-EGOPREC-2026-0102

- Claim: 本文用三级时序手段吸收手部关键点检测噪声：(1) 重定向优化目标含 β·‖q_t−q_{t−1}‖² 时序平滑项与关节限位约束（α、β 平衡尺度与时序平滑）；(2) 实时遥操作侧对关键点施加平滑系数 0.2 的低通滤波以抑制突发关键点波动，使约束优化在 10ms 内求解并实现 30Hz 稳定控制与记录；(3) 推理端对重叠预测做带衰减权重的 temporal ensembling 以保证动作平滑。检测噪声在此路线中被当作需持续抑制的既有条件而非可消除变量。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.10952](https://arxiv.org/abs/2509.10952) ImMimic: Cross-Domain Imitation from Human Videos via Mapping and Interpolation
- Locator: 3.1 Hand Pose Retargeting System; 3.4 Inference; Appendix
- Evidence: 3.1 给出含 β 时序平滑项的重定向优化（式 1）；Appendix B 报告 10ms/帧求解、0.2 低通滤波抑制关键点突变、30Hz 稳定控制；3.4 报告推理端 temporal ensembling。
- Quote: “We solve this constrained optimization problem in under 10 ms per frame. To further reduce latency and improve motion continuity, we apply a low- pass filter with a smoothing parameter of 0.2 to suppress sudden keypoint fluctuations. This enables stable control and recording at 30 Hz.”
- Authors: yangcen-liu; woo-chul-shin; yunhai-han; et al.

### EA-EGOPREC-2026-0103

- Claim: 人机动作差距被量化为 DTW 对齐后的动作距离（AD，平移 L1+手姿 L1+旋转角距的加权和）：两只灵巧手的平均 AD（Allegro 0.078、Ability 0.075）反而大于两只平行夹爪（Robotiq 0.066、FR 0.065），即更类人的末端不一定更接近机器人可执行动作——作者归因于安装方式与臂运动学同手部设计共同影响重定向；且策略从人类视频获益的幅度与 AD 负相关：AD 越小获益越大，与机械结构是否类人无关。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.10952](https://arxiv.org/abs/2509.10952) ImMimic: Cross-Domain Imitation from Human Videos via Mapping and Interpolation
- Locator: 5 Core Results
- Evidence: 5 Core Results 报告四本体平均 AD（0.065-0.078）与'AD 小→获益大'的经验律及对反直觉结果的归因；Appendix Table E.3 给出 4 任务 × 4 本体的 AD 明细并注明夹爪动作差距总体小于灵巧手。
- Quote: “Average AD (Action Distance) shows that two dexterous hands demonstrate larger action distances (Allegro: 0.078, Ability: 0.075) compared to the two grippers (Robotiq: 0.066, FR: 0.065). Moreover, Tab. 1 show that policies benefit more from human videos when the action distance is smaller, regardless of its mechanical structure.”
- Authors: yangcen-liu; woo-chul-shin; yunhai-han; et al.

### EA-EGOPREC-2026-0104

- Claim: 动作空间映射显著优于视觉特征映射：在 Pick and Place/Flip × Robotiq/Ability 对照中，动作映射 ImMimic-A 四项成功率全为 1.00，视觉映射 ImMimic-V 低至 0.50，随机映射最低 0.40；作者报告视觉映射弱时策略在原位打转失效，并解释经运动学约束重定向的人类动作在结构上比视觉特征更接近机器人动作。独立的长原始视频检索任务复验了该结论：视觉干扰下视觉映射 mIoU 从 0.52 跌至 0.41（↓0.11）、Acc@0.5 从 66.7 跌至 33.3，而动作映射仅从 0.70 跌至 0.67（↓0.03）、Acc@0.5 66.7 不变量级（66.7→66.7）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.10952](https://arxiv.org/abs/2509.10952) ImMimic: Cross-Domain Imitation from Human Videos via Mapping and Interpolation
- Locator: 5 Core Results
- Evidence: 5 Core Results 的 Tab.2 报告六种设置在两本体两任务的成功率，正文报告视觉映射弱导致原地打转并给出结构性解释；Appendix C 的 Tab.C.1 报告三条件下视觉/动作映射的 mIoU 与 Acc@0.5。
- Quote: “Random Mapping 0.40 0.50 0.80 0.50 ImMimic-V 1.00 0.50 0.90 0.70 ImMimic-A 1.00 1.00 1.00 1.00 Table 2: Comparison of success rate across two em- bodiments (Robotiq, Ability) and two tasks (Pick and Place, Flip), with 5 robot demos and 100 hu- man demos.”
- Authors: yangcen-liu; woo-chul-shin; yunhai-han; et al.

### EA-EGOPREC-2026-0315

- Claim: 为弥合人机域差，EgoBridge 在数据侧叠加三重对齐：机器人佩戴同款 Aria 眼镜并模拟成年人类手眼配置以消除相机设备差；人机动作统一投影到 ego 相机（设备）伪参考系的 SE(3) 空间并按本体做 z-score 归一化；训练侧再用 DTW 距离吸收人机 2-3 倍的执行速度差与共享 SE(3) 空间内的残余运动学差异。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.19626](https://arxiv.org/abs/2509.19626) EgoBridge: Domain Adaptation for Generalizable Imitation from Egocentric Human Data
- Locator: 4.2 Designing OT Cost Function for Action-Aware Joint Adaptation
- Evidence: 4.2 给出 2-3 倍速度差与共享 SE(3) 下残余运动学差异的表述；4.3 给出同款眼镜模拟手眼配置；附录 F 给出每本体 z-score 归一化。
- Quote: “humans might be 2-3 times faster than teleoperated robots, and kinematic variations, where even within a shared SE(3) end-effector action space and hand-eye alignment through an egocentric coordinate frame (Sec. 4.3), minor kinematic differences exist.”
- Authors: ryan-punamiya; dhruv-patel; patcharapong-aphiwetsa; et al.

### EA-EGOPREC-2026-0316

- Claim: 在三个真实单臂/双臂任务上，EgoBridge 较人类数据增强跨本体基线最高提升 44% 绝对成功率；在机器人数据从未覆盖的 Drawer 第四象限（行为仅见于人类数据），EgoBridge 取得 33% 成功率而所有基线完全失败（0%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.19626](https://arxiv.org/abs/2509.19626) EgoBridge: Domain Adaptation for Generalizable Imitation from Egocentric Human Data
- Locator: 5.3 Results
- Evidence: 摘要与 5.3 分别给出 44% 与 33%/0% 数字；Table 1 中 Drawer 行为泛化列基线全部为 0%。
- Quote: “find that EgoBridge is able to generalize to these locations with a success rate of 33%, whereas most methods fail entirely (Tab. 1)”
- Authors: ryan-punamiya; dhruv-patel; patcharapong-aphiwetsa; et al.

### EA-EGOPREC-2026-0327

- Claim: 作者将无本体 ego 视频轨迹提取的误差显式归因于三类来源：物体检测误差、点云配准误差、相邻帧深度不一致造成的平移抖动；并分别用背景轨迹相似度（BGTS）阈值、行程距离阈值和五帧均值平滑予以缓解。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: B. Pre-training Dataset Construction
- Evidence: Data Curation 小节原话指出不准确轨迹主要来自检测与配准误差，并描述两条对应过滤器；随后一段说明深度不一致导致抖动并用五帧窗口平滑。
- Quote: “We found that EgoScaler some- times produces inaccurate trajectories, mainly due to object detection and point cloud registration errors. To remove them automatically, we apply two rule-based filters: a travel distance threshold for registration errors and a background track similarity threshold for detection errors. For the travel distance threshold (δ DT ), we define the travel distance D of a trajectory as the cumulative displace- ment of its positional component, D = P T −1 t=1 ∥p t+1 −”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGOPREC-2026-0328

- Claim: 轨迹提取质量与数据规模存在可量化的权衡：不过滤检测误差（δ_BGTS=1.0，86,427 条）时真机成功率降至 38.8±4.3，而 δ_BGTS=0.7（45,157 条）达 55.0±6.1，即约 2 倍含噪数据反而使成功率下降约 16 个百分点；过严过滤（0.5，28,719 条）为 53.8±5.2。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: B. Results; C. Ablation Study
- Evidence: Table III 给出三个阈值下的 episode 数与两环境成功率；消融段落解释为较低阈值去噪但缩量、较高阈值留噪而性能下降，0.7 为最佳折中。
- Quote: “TABLE III: Performance comparison across different background track similarity thresholds (BGTS). δ BGTS #Episodes SIMPLER [20] Real Robot 0.5 28,719 25.8 ±5.4 53.8 ±5.2 0.7 45,157 26.0 ±5.9 55.0 ±6.1 1.0 86,427 22.5 ±4.8 38.8 ±4.3”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGOPREC-2026-0329

- Claim: 用物体中心 ego 轨迹预训练的 π0 在真机搬运任务上达到 21/40，与真实机器人遥操作数据集相当（BC-Z 19/40、BridgeData V2 17/40、Fractal 22/40），与 BridgeData V2 混合后达 27/40；同设置下从头训练成功率为 0%。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: B. Results
- Evidence: Table II 报告四个预训练数据集在相同后训练协议下的真机成功率；正文确认 scratch 真机 0% 且混合数据集进一步增益。
- Quote: “TABLE II: Comparison with robot datasets. Successes out of 10 rollouts are reported for each task, with the final column showing the total. Dataset Carrot -Pot Carrot -Bowl Onion -Pot Onion -Bowl Total BridgeData V2 [27] 4/10 3/10 6/10 4/10 17/40 BC-Z [26] 5/10 5/10 4/10 5/10 19/40 Fractal [3] 7/10 4/10 7/10 4/10 22/40 Ours 4/10 6/10 7/10 4/10 21/40 Ours + [27] 7/10 7/10 7/10 6/10 27/40 As shown in Fig. 5, our method outperforms the scratch base- line in real-robot tasks, while achieving small”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGOPREC-2026-0442

- Claim: 在卷尺回放协议（标称距离 100→10cm 共 10 点、10 次试验取平均）下，ActiveUMI 采集轨迹经真实机器人回放的相对位姿误差为 4.0mm，显著低于 UMI 的 10.1mm（约 2.5 倍），作者把该差距归因于 VR 追踪系统优势——为'采集接口位姿追踪精度→机器人末端回放轨迹精度'提供直接定量证据。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: 4.5. Data Collection Throughput and Accuracy, Fig. 6(e)
- Evidence: 4.5 定义 RPE 协议（式 1-2：以标称距离为真值计算回放距离的绝对/相对误差）并报告十次试验平均；数值逐字取自 Fig. 6(e) 图块标注文本（'RPE(mm) UMI 10.1 / ActiveUMI (Ours) 4.0'，该图块在抽取文本中物理位于 4.3 与 4.5 之间）；正文 '2.5x smaller' 与 10.1/4.0≈2.53 一致。注意正文存在笔误：'the RPE of UMI is 2.5x smaller than UMI' 按图注数据主语应为 ActiveUMI；且式 2 将 RPE 定义为百分比而图注以 mm 标注。
- Quote: “We can observe that the RPE of UMI is 2.5x smaller than UMI. This low error is naturally comes from the advantange of the VR system”
- Authors: qiyuan-zeng; chengmeng-li; j-drummond-john; et al.

### EA-EGOPREC-2026-0445

- Claim: 在相同 pi0 后端与相同训练流程下，具备主动 ego 感知的 ActiveUMI 策略在六个双臂任务上平均成功率 70%，显著高于固定顶视相机变体（42%）与纯腕摄 UMI 配置（26%）；在新环境中三者分别为 56%、16%、6%——头部视点可控性对遮挡与视角变化场景的鲁棒性贡献大于单纯增加固定第三视角。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: 4.2. How Important is the Egocentric Active Per-; 4.3. Mixed Training with Teleoperated Data, Table 1
- Evidence: Table 1 给出 in-domain 五任务逐任务与平均成功率（UMI 26% / 固定头 42% / ActiveUMI 70%）；Table 2 给出新环境对应数字（6% / 16% / 56%），其图块文本在抽取中物理位于 4.3 节内，4.4 正文复述 56%/16%/6%；4.2 正文给出两驱动假设（补偿演示者头体运动、按需获取任务关键信息）。
- Quote: “UMI 60% 20% 10% 0% 40% 26% UMI w/ Fixed Head Camera 60% 40% 40% 20% 50% 42% ActiveUMI 90% 70% 80% 30% 80% 70%”
- Authors: qiyuan-zeng; chengmeng-li; j-drummond-john; et al.

### EA-EGOPREC-2026-0332

- Claim: 在 robot-free ego 采集系统中，末端追踪误差为毫米级且因方案而异：UMI 8.855±3.228 mm、AirExo-2 1.737±1.713 mm、EgoMI（VR 手柄）2.126±1.216 mm；作者指出 robot-free 采集下数据质量直接取决于示教设备保真度（而 on-embodiment 采集由机器人传感反馈记录，对示教设备精度不敏感）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00153](https://arxiv.org/abs/2511.00153) EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations
- Locator: C. Policy learning with Active Vision
- Evidence: Table I 列出各系统 Error (mm, avg±std) 与是否 robot-free/头部追踪/真夹爪；表注明确阐述 robot-free 与 on-embodiment 对示教设备精度依赖的差异。
- Quote: “TABLE I: Comparison of teleoperation systems and their features. For on-embodiment data collection, teaching device accuracy is less critical since the robot records data from sensor feedback rather than depending on the fidelity of the teaching device itself. Our proposed method, EgoMI, is the only system that simultaneously captures head and hand trajectories, supports true gripper actions, and enables whole-body retargeting, bridging the embodiment gap between human demonstrations and robotic”
- Authors: justin-yu; yide-shentu; di-wu; et al.

### EA-EGOPREC-2026-0333

- Claim: EgoMI 的 robot-free 轨迹净化与标定管线包括：视频时序检查与 SE(3) 平移/旋转增量平滑阈值过滤低质轨迹；按首帧头部水平位置与双手前向方向（circular mean yaw）把 VR 世界系重定向到机器人规范坐标系；再经 VR 手柄→机器人法兰→TCP 的固定标定链，将全部轨迹表达到机器人中心坐标系以缩小本体感知差距。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00153](https://arxiv.org/abs/2511.00153) EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations
- Locator: C. Data Reformatting and Cleaning
- Evidence: C 节完整描述过滤（timing checks、SE(3) deltas 平滑阈值）与四步变换（前向估计、base origin、VR-to-base、calibration/offsets），并声明目的是最小化 proprioceptive gap。
- Quote: “We develop a high-throughput conversion pipeline that discovers and validates trajectory episodes, filtering out low-quality or corrupted data via video timing checks, and trajectory smoothness thresholds (SE(3) translation/rotation deltas). A key step is applying transforms that re-orient the raw data to minimize the proprioceptive gap between the capture system and the target robot. Because demonstrations are collected in a VR system with its own arbitrary world frame, we align all poses to th”
- Authors: justin-yu; yide-shentu; di-wu; et al.

### EA-EGOPREC-2026-0334

- Claim: 重定向环节用可微 IK（Pyroki）替代解析 IK：把不可达位姿作为加权代价最小化问题处理，实现 graceful degradation——尽可能接近演示位姿而非执行报错，从而无需手工轨迹过滤或重训即可把不受约束的人类演示迁移到不同运动学极限的机器人。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00153](https://arxiv.org/abs/2511.00153) EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations
- Locator: D. Policy Deployment
- Evidence: D. Policy Deployment 原段对比解析 IK 与可微 IK 在不可达位姿上的行为，并声明无需 manual trajectory filtering or retraining。
- Quote: “Unlike analytical IK, which fails or returns nulls on unreachable poses, a differentiable approach treats IK as a weighted cost-minimization problem. By op- timizing for end-effector pose error alongside posture regularization, the system achieves ”graceful degradation” reaching as close as physically possible to the demonstrated pose rather than experiencing execution errors. This ensures robust transfer of unconstrained human demonstrations to robot embodiments with varying kinematic limits wi”
- Authors: justin-yu; yide-shentu; di-wu; et al.

### EA-EGOPREC-2026-0038

- Claim: SPIDER 展示从单 RGB 视频（Trellis 重建 + HaMeR 手部姿态估计 + FoundationPose 物体 6D 位姿跟踪）出发的重定向：因遮挡与分辨率限制，人与物体运动比数据集更 noisy，经物理 grounding 修正噪声、伪影与穿透后，轨迹可直接在物理机器人上执行（倒杯、装螺栓）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.09484](https://arxiv.org/abs/2511.09484) SPIDER: Scalable Physics-Informed Dexterous Retargeting
- Locator: 4.1 Retargeting from Single RGB Camera
- Evidence: 4.1 节描述完整管线与结论：单 RGB 输入运动更 noisy，需要更强物理 grounding；作者报告噪声/伪影/穿透被修正且轨迹直接真机执行。结果为定性展示（figure 9），无数值指标。
- Quote: “The pipeline consists of: (1) 3D mesh reconstruction with Trellis (Xiang et al., 2025), (2) hand pose estimation with HAMER (Pavlakos et al., 2024) to obtain MANO parameters, and (3) object pose tracking with FoundationPose (Wen et al., 2024) for 6D trajectories. Due to the occlu- sion and limited resolution, the human and object motion are more noisy than the dataset, which requires more robust physics grounding. As shown in figure 9, we validate on single-hand manipula- tion tasks like pouring”
- Authors: chaoyi-pan; changhao-wang; haozhi-qi; et al.

### EA-EGOPREC-2026-0039

- Claim: 在 Oakink 7 个双手任务与 GigaHands 3 条轨迹（5 种灵巧手、5 个种子）上，纯运动学重定向（指尖 IK）成功率仅 0.0-0.13，普通采样 0.23-0.64，退火核采样 0.43-1.00，退火核+虚拟接触引导达 0.45-1.00，比仅退火核平均高约 18%。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.09484](https://arxiv.org/abs/2511.09484) SPIDER: Scalable Physics-Informed Dexterous Retargeting
- Locator: 3.2 Ablation Study
- Evidence: 3.2 节 Table 1 给出四档方法在 10 个机器人-数据集组合上的成功率（运动学 0.0-0.13，全方法 0.45-1.00），Key Findings 报告全方法在所有组合上最高、比仅退火核高 ~18%。
- Quote: “Key results are presented in table 1, where sampling equipped with an annealed kernel and virtual contact guidance consistently achieves the highest success rates across all robot–dataset combinations, outperforming the annealed-kernel-only version by ∼ 18%.”
- Authors: chaoyi-pan; changhao-wang; haozhi-qi; et al.

### EA-EGOPREC-2026-0371

- Claim: In-N-On 把人类与机器人数据统一映射到以人为中心的状态-动作空间：头姿 SE(3) 为基变换、双腕姿相对头姿、手指运动建模为 3×5 指尖关键点(优化式手指重定向算法的直接输入)、夹爪开合映射为拇指-食指指尖距离；配套 Pinocchio IK/FK 套件在机器人关节空间与该空间之间双向转换。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.15704](https://arxiv.org/abs/2511.15704) In-N-On: Scaling Egocentric Manipulation with in-the-wild and on-task Data
- Locator: 3.1. PH
- Evidence: 3.1 节统一空间四条定义与套件功能声明，逐字支撑。
- Quote: “we model finger motions as fingertip keypoints, as all well-established optimization- based finger retargeting algorithms [11, 21, 41] directly use fingertip keypoints with scaling factors.”
- Authors: xiongyi-cai; ri-zhao-qiu; geng-chen; et al.

### EA-EGOPREC-2026-0303

- Claim: 在统一动作空间下以指尖轨迹（而非关节角）为预测目标，METIS 无需修改即可迁移到 22-DoF SharpaWave 灵巧手，在 Grasp Apple into Basket 与 Tool Use 上分别取得 85.0% 与 70.0% 成功率。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.17366](https://arxiv.org/abs/2511.17366) METIS: Multi-Source Egocentric Training for Integrated Dexterous Vision-Language-Action Model
- Locator: 5.4. Generalization
- Evidence: 5.4 跨本体实验报告两任务成功率并归因于指尖空间预测。
- Quote: “As METIS predicts fingertip trajectories rather than direct joint angles, the policy is naturally transferable and remains unaffected by variations in hand kinematics.”
- Authors: yankai-fu; ning-chen; junkai-zhao; et al.

### EA-EGOPREC-2026-0532

- Claim: 仅用视觉隐状态预测损失训练世界模型不足以捕捉灵巧动态，因为手部只占图像很小区域；作者据此引入从预测隐状态解码指尖/手腕热图的手部一致性损失作为局部监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.13644](https://arxiv.org/abs/2512.13644) World Models for Learning Dexterous Hand-Object Interactions from Human Videos
- Locator: 3.3 Hand Consistency Training Loss
- Evidence: 3.3 节作者明确观察到单靠 L_state 不足以捕捉灵巧动态所需的细粒度细节，原因是手部在图像中占比小，因此加入手部一致性损失。
- Quote: “insufficient for capturing the fine-grained details necessary for modeling dexterous dynamics, as the hands occupy only a small region of the image.”
- Authors: raktim-gautam-goswami; amir-bar; david-fan; et al.

### EA-EGOPREC-2026-0533

- Claim: 在 EgoDex 开环预测上，加入手部一致性损失使 4 秒预测的 PCK@20 从 26 提升至 60（+34 个百分点），embedding L2 误差同时从 0.85 降到 0.66，说明手部特异性监督显著改善了世界模型对手部位形的建模。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.13644](https://arxiv.org/abs/2512.13644) World Models for Learning Dexterous Hand-Object Interactions from Human Videos
- Locator: 4.2 Ablation Studies
- Evidence: 4.2 节表 2：无 HC 损失 PCK@20@4s=26、L2=0.85；有 HC 损失 PCK@20@4s=60、L2=0.66；正文复述 +34pp。
- Quote: “adding hand consistency loss yields up to a 34% increase in PCK@20 at 4 seconds prediction.”
- Authors: raktim-gautam-goswami; amir-bar; david-fan; et al.

### EA-EGOPREC-2026-0535

- Claim: 在 DexWM 训练组合中加入 EgoDex 人类 ego 视频后，RoboCasa 下游开环预测改善：embedding L2 从 1.3/0.96 降到 0.79/0.57（4s/平均），PCK@20 从 2/12 升到 7/17，说明带手部关键点标注的人类视频对跨本体动力学学习有可测收益。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.13644](https://arxiv.org/abs/2512.13644) World Models for Learning Dexterous Hand-Object Interactions from Human Videos
- Locator: 3.4 Robot Task Planning; 4.2 Ablation Studies
- Evidence: 表 1（位于 3.4 节版面内）对比 EgoDex+DROID 与仅 DROID 训练在 RoboCasa Lift 开环评估的 L2 与 PCK@20；4.2 节正文确认加入 EgoDex 显著提升 RoboCasa 表现。
- Quote: “adding EgoDex on top of DROID significantly boosts performance on RoboCasa, while preserving performance on EgoDex.”
- Authors: raktim-gautam-goswami; amir-bar; david-fan; et al.

### EA-EGOPREC-2026-0536

- Claim: DexWM 在真机 Franka+Allegro 上零样本抓取 12 次试验成功 10 次（≈83%），而 Diffusion Policy 与无人类视频预训练的 DexWM 真机成功率为 0；仿真 reach/place/grasp 成功率 72%/28%/58%。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.13644](https://arxiv.org/abs/2512.13644) World Models for Learning Dexterous Hand-Object Interactions from Human Videos
- Locator: 4.5 Human Video To Robot Transfer
- Evidence: 4.5 节与表 4：真机抓取 10/12≈83%；仿真三任务 72/28/58；DP 与无预训练变体真机均为 0。
- Quote: “Without any finetuning on real robot data, DexWM achieves 10 successes out of 12 trials (≈ 83% success rate)”
- Authors: raktim-gautam-goswami; amir-bar; david-fan; et al.

### EA-EGOPREC-2026-0540

- Claim: E2E-3M 的质量验收口径是语言规则而非几何真值：确定性规则校验器执行证据落地（所有被提及的动作、手和接触状态必须得到 clip 帧支持）、ego 一致性与模式时序逻辑；典型生成失败包括引用不可见的手、时序错乱与欠约束占位符。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.16793](https://arxiv.org/abs/2512.16793) PhysBrain: Human Egocentric Data as a Bridge from Vision Language Models to Physical Intelligence
- Locator: 3.1 Egocentric2Embodiment Translation Pipeline
- Evidence: 3.1.3 节列出三类校验约束与常见失败（references to non-visible hands 等），不合格样本回炉重生成。
- Quote: “Evidence grounding requires that all mentioned actions, hands, and contact states are supported by the clip frames.”
- Authors: xiaopeng-lin; shijie-lian; bin-yu; et al.

### EA-EGOPREC-2026-0541

- Claim: 以 PhysBrain 为 VLM 骨干的 PhysGR00T 仅用 OXE 两个子集（Bridge、Fractal）微调即在 SimplerEnv 四任务取得平均 53.9% 成功率，超过用更大规模机器人数据训练的 VLA 基线（最高 53.1%），并比同管线微调的第二名 VLM 基线高 8.8 个百分点、比 RoboBrain 高 16.1 个百分点。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.16793](https://arxiv.org/abs/2512.16793) PhysBrain: Human Egocentric Data as a Bridge from Vision Language Models to Physical Intelligence
- Locator: 5.2 VLA Simulation Evaluation
- Evidence: 5.2 节表 2 与正文：PhysBrain 平均 53.9%，VLA 基线最高 VideoVLA 53.1%；VLM 基线第二名 Spatial-SSRL 45.1%（+8.8pp），RoboBrain 37.8%（+16.1pp）。
- Quote: “our VLA model achieves an average success rate of 53.9%, outperforming VLA baselines trained on substantially larger robot datasets”
- Authors: xiaopeng-lin; shijie-lian; bin-yu; et al.

### EA-EGOPREC-2026-0542

- Claim: 在 EgoThink 基准上，PhysBrain 的 Planning 维度得分 64.5，超过 GPT-4 的 35.5，平均分 64.3 低于 GPT-4 的 67.4；提升最大维度是 Planning。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.16793](https://arxiv.org/abs/2512.16793) PhysBrain: Human Egocentric Data as a Bridge from Vision Language Models to Physical Intelligence
- Locator: 5.1 VLM Egocentric Evaluation; Method
- Evidence: 5.1 节表 1：PhysBrain Planning 64.5 vs GPT-4 35.5；平均 64.3 vs 67.4；正文称 Planning 提升最显著且超过 GPT-4。
- Quote: “PhysBrain (ours) 70 53.5 77 65.3 64.5 58 64.3”
- Authors: xiaopeng-lin; shijie-lian; bin-yu; et al.

### EA-EGOPREC-2026-0527

- Claim: WIYH 对手部动作标注质量采用可操作的验收口径：将 H-Gloves 的 3D 手部骨架投影到胸戴相机视角，与分割得到的手部掩膜计算相交评分，低于预设阈值的样本被标记并经人工复核后过滤。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.24310](https://arxiv.org/abs/2512.24310) World In Your Hands: A Large-Scale and Open-source Ecosystem for Learning Human-centric Manipulation in the Wild
- Locator: 2.2 Data Validation System
- Evidence: 2.2 节描述了投影相交质检流程：手部掩膜与骨架投影求交，低分样本进入人工复核与过滤，图 3 图注复述该阈值-复核机制。
- Quote: “We compute an intersection score and flag samples whose score falls below a predefined threshold; these cases are then manually reviewed and filtered to ensure data quality.”
- Authors: tars-robotics; yupeng-zheng; jichao-peng; et al.

### EA-EGOPREC-2026-0528

- Claim: 在多物体杂乱场景的灵巧抓取任务中，仅用机器人数据训练的策略成功率最高 8%，混入 800 条重定向人类中心数据后成功率升至 60%（+52 个百分点）；单物体场景同样观察到 +13.4 个百分点的提升。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.24310](https://arxiv.org/abs/2512.24310) World In Your Hands: A Large-Scale and Open-source Ecosystem for Learning Human-centric Manipulation in the Wild
- Locator: 5.2 Results and In-depth Discussion
- Evidence: 5.2 节与表 5 报告：杂乱场景 500 条机器人数据成功率 8.0%，加 800 条人类数据后 60.0%（+52.0）；单物体场景 43.3%→56.7%（+13.4）。
- Quote: “Simply increasing data quantity from 200 clips to 500 clips yields marginal performance improvement from 0% to 8%. However, after co-training with human-centric data, the success rate increases by 52%.”
- Authors: tars-robotics; yupeng-zheng; jichao-peng; et al.

### EA-EGOPREC-2026-0406

- Claim: 在纯 ego（头戴）相机、无腕部相机的采集中，手部被物体或环境遮挡会使手部追踪质量显著退化，产生缺失或错误的动作标签；作者因此要求演示者调整接近角度与操作方式以保持手部全程可见（即使偏离自然行为）。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.10106](https://arxiv.org/abs/2602.10106) EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
- Locator: B. Practical Guidelines for Data Collection
- Evidence: 附录 B 手部可见性准则明确指出遮挡→追踪退化→缺失/错误动作标签的因果链。
- Quote: “Hand Visibility Maintenance. Reliable hand pose estimation requires minimizing occlusion during manipulation, particularly when ego-centric (head) cameras are used only without wrist cameras. When hands are obscured by manipulated objects or environmental elements, tracking quality degrades substantially, resulting in missing or inaccurate action labels.”
- Authors: modi-shi; shijia-peng; jin-chen; et al.

### EA-EGOPREC-2026-0407

- Claim: 由于动作表示采用 delta 末端位姿，微小的腕部旋转即可在视觉几乎相同的操作场景中产生截然不同的动作标签；此类不一致会给训练数据引入显著噪声——近似相同的视觉观测配上了冲突的动作目标，最终降低策略学习效果。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.10106](https://arxiv.org/abs/2602.10106) EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
- Locator: B. Practical Guidelines for Data Collection
- Evidence: 附录 B 腕-手一致性准则直接陈述小腕部旋转→动作标签剧变→观测-动作冲突→策略退化。
- Quote: “Since our action representation uses delta end-effector poses, small wrist rotations can produce dramatically different action labels even for visually similar manipulation scenarios. Such inconsistencies introduce significant noise into the training data, as nearly identical visual observations become paired with conflicting action targets, ultimately degrading policy learning effectiveness.”
- Authors: modi-shi; shijia-peng; jin-chen; et al.

### EA-EGOPREC-2026-0410

- Claim: 为抑制追踪噪声，管线将腕部位姿表达到骨盆坐标系、用 Savitzky-Golay 滤波平滑平移、在 SO(3) 切空间以 log/exp 映射滤波旋转；抓取状态则经低通+SG 平滑后按指级曲率阈值化为二值标签，作者称该曲率表示可缓解噪声并实现可靠的监督提取。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.10106](https://arxiv.org/abs/2602.10106) EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
- Locator: C. Human-to-Humanoid Alignment
- Evidence: III.C 动作对齐与 Gripper 段落给出完整滤波/平滑/阈值化链。
- Quote: “Explicitly, we express human wrist poses in a pelvis-centric frame, then smooth translations with a Savitzky-Golay filter [52]. For rotations, we filter in the SO(3) tangent space using log/exp maps to prevent quaternion interpolation ambiguities.”
- Authors: modi-shi; shijia-peng; jin-chen; et al.

### EA-EGOPREC-2026-0389

- Claim: 重建误差（物体几何、手部 mesh 尺度/形状/姿态不准）会导致抓握穿透物体表面或接触缺失；用 ContactOpt 做可微接触优化后，20 物体平均抓握成功率从 30.7% 提升到 63.75%，即接触级后处理可吸收大部分重建误差。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.09013](https://arxiv.org/abs/2602.09013) Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
- Locator: A. Grasping Experiments
- Evidence: IV-A 消融：同一 DRO 抓握模型分别在未优化/优化抓握上训练。
- Quote: “We further ablate the effect of grasp optimization using ContactOpt [47] by retraining the DRO grasping model on all objects with unoptimized grasps, which yields only a 30.7% average success rate across 20 objects, compared to 63.75% when using optimized grasps, as shown in Fig. 3(a). As shown in Fig. 5(b), unoptimized grasps often penetrate object surfaces or fail to establish contact due to reconstruction errors, whereas optimized grasps achieve more accurate hand–object contact, which is ref”
- Authors: hongyi-chen; tony-dong; tiancheng-wu; et al.

### EA-EGOPREC-2026-0391

- Claim: in-the-wild 视频不做重力对齐时 Pour Tea 成功率为 0%，对齐后与有外参标定的 in-scene 视频无显著差异，说明坐标系级误差（相机姿态未知）对重定向轨迹是灾难性的，但可用单目重力估计（GeoCalib）有效校正。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.09013](https://arxiv.org/abs/2602.09013) Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
- Locator: B. Manipulation Experiments
- Evidence: IV-B A4 的重力对齐消融。
- Quote: “Table II shows no significant performance dif- ference between the two video sources; however, without applying gra R cam for the in-the-wild Pour Tea task, the success rate drops to 0%, highlighting the importance of gravity-alignment calibration”
- Authors: hongyi-chen; tony-dong; tiancheng-wu; et al.

### EA-EGOPREC-2026-0392

- Claim: HaMeR 的弱透视相机模型存在固有深度歧义并对焦距误差敏感；VIDEOMANIP 复用 MoGe-2 度量深度（与物体位姿估计同一深度参照），取 HaMeR 2D 关键点处的度量深度均值作为校正后的手部深度，使手与物体共享同一 3D 坐标系。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.09013](https://arxiv.org/abs/2602.09013) Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
- Locator: III. METHOD
- Evidence: III-A 手部 mesh 估计段的误差机制与校正设计。
- Quote: “HaMeR uses a weak-perspective camera model, which is inherently depth-ambiguous and sensitive to focal length errors. To align the reconstructed hand mesh H within a joint coordinate space with the object, we reuse the metric depth maps predicted by MoGe-2, which are consistent with those used for object pose estimation, to ensure that H and O share the same depth reference. We then compute the corrected hand depth t ′ z by averaging the metric depths at the 2D keypoints predicted by HaMeR”
- Authors: hongyi-chen; tony-dong; tiancheng-wu; et al.

### EA-EGOPREC-2026-0401

- Claim: EasyMimic 的无本体管线完全以单目 HaMeR 模型从普通 RGB 视频重建的 3D 手部信息（21 关键点 + 778 网格顶点，相机坐标系）作为后续动作/视觉对齐的唯一手部轨迹来源。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11464](https://arxiv.org/abs/2602.11464) EasyMimic: A Low-Cost Framework for Robot Imitation Learning from Human Videos
- Locator: A. Data Collection Systems and Hardware Design
- Evidence: 方法 III.A 明确说明用 HaMeR 从单目输入重建每帧手部形态，提供 21 关键点与 778 顶点于相机坐标系，作为对齐流程基础。
- Quote: “To process human videos, we leverage the advanced HaMeR model [44] to extract 3D hand information from monocular inputs. We utilize this model to precisely reconstruct the hand morphology for each video frame, providing 21 hand keypoint coordinates X C t and 778 hand mesh vertex coordinates V C t in the camera coordinate frame C.”
- Authors: tao-zhang; song-xia; ye-wang; et al.

### EA-EGOPREC-2026-0402

- Claim: 作者指出以手腕或指尖中点为重定向锚点会偏离真实交互中心——手腕离物体太远、精细操作时指尖相互运动导致锚点不稳——因此改用拇指 PIP 与食指 MCP 中点（大鱼际中心）作为抓取中相对稳定的锚点。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11464](https://arxiv.org/abs/2602.11464) EasyMimic: A Low-Cost Framework for Robot Imitation Learning from Human Videos
- Locator: B. Physical Alignment
- Evidence: III.B 位置对齐段落论证手腕/指尖锚点的不稳定性并给出大鱼际锚点设计。
- Quote: “Prior works often use the wrist [10] or the midpoint of the fingertips [27] as an anchor point, but these can deviate from the true center of interaction during complex manipulations. For example, the wrist is too far from the object, while fingertips move relative to each other during fine manipulation, leading to an unstable anchor.”
- Authors: tao-zhang; song-xia; ye-wang; et al.

### EA-EGOPREC-2026-0403

- Claim: 消融动作空间对齐（人类数据不做 AA 直接共同训练）后，平均任务得分从 0.87 降至 0.60（-0.27），且在需要精确手部旋转的 pick/stack 类任务中退化最明显。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.11464](https://arxiv.org/abs/2602.11464) EasyMimic: A Low-Cost Framework for Robot Imitation Learning from Human Videos
- Locator: C. Further Analysis
- Evidence: Table III 与正文：去除 AA 平均降 0.27 分；作者明确指出需要精确手部旋转的任务退化尤其明显。
- Quote: “AA leads to a significant performance drop, with an average decrease of 0.27 points across tasks. The performance degra- dation is particularly pronounced in tasks such as pick-and- stack, which require precise hand rotation.”
- Authors: tao-zhang; song-xia; ye-wang; et al.

### EA-EGOPREC-2026-0306

- Claim: 为补偿大规模噪声监督，EgoScale 混入 829 小时 EgoDex 数据（Apple Vision Pro 采集、腕部与手部追踪准确、覆盖 194 个桌面任务），作为更高精度的运动学信号『锚定』预训练，同时保持可扩展性。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 2.2. Human Data Sources and Processing
- Evidence: 2.2 原文描述 EgoDex 子集的精度定位与锚定作用。
- Quote: “To complement this large-scale but noisy supervision, we additionally incorporate 829 hours of EgoDex dataset [8], collected using Apple Vision Pro with accurate wrist and hand tracking. EgoDex covers 194 tabletop manipulation tasks involving everyday objects and provides higher-precision kinematic signals that help anchor pretraining while preserving scalability.”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-EGOPREC-2026-0307

- Claim: Stage II 对齐中训数据（约 50 小时人类+4 小时机器人、344 个桌面任务）的人类手部运动用与机器人遥操作完全相同的动捕栈采集——Vive tracker 提供腕部 3D 位姿、Manus 手套记录 25 关节变换，且人机视角匹配、相机内参标定、信号与视频同步。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 2.2. Human Data Sources and Processing
- Evidence: 2.2 Stage II 段落逐句描述采集配置；图 2a 说明确认与机器人同传感设置。
- Quote: “Human hand motion is captured using the same motion-capture stack as in robot teleoperation: Vive trackers provide wrist pose (3D position and orientation), while Manus gloves record full in-hand pose as 25 joint transforms. All motion signals are synchronized with the video stream.”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-EGOPREC-2026-0309

- Claim: 在 1k-20k 小时扫描内，人类预训练数据量与手部动作预测验证损失呈对数线性关系（L=0.024-0.003·ln(D)，R²=0.9983），且下游真机平均完成度从 1k 小时的 0.30 单调升至 20k 小时的 0.71、无饱和迹象——尽管这些人类示教是噪声的、无约束的、且不做任务对齐。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.3. Policy Performance Scales with Pretraining Data Size
- Evidence: 3.3 报告规模律拟合与真机完成度-数据量曲线，两者均基于同一批含噪声手部监督的预训练检查点。
- Quote: “Average task completion rises monotonically from 0.30 at 1k hours to 0.71 at 20k hours, with no signs of saturation in the explored regime. These results indicate that large-scale human data provides increasingly strong priors for dexterous manipulation, even though the human demonstrations are noisy, unconstrained, and not task-aligned.”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-EGOPREC-2026-0472

- Claim: AoE 云端管线的手部重建精度报告为 PA-MPJPE 3.7-7.4mm、MPJPE 8.9-11.9mm、AUC 0.90-0.93（Ego4D/EgoDex 测试集，含 w/o 与 w/ depth 配置）；EgoDex 上的较大误差被归因于数据集固有的运动模糊与错位，作者用 AR 眼镜硬件追踪做配对验证以支持其管线精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.23893](https://arxiv.org/abs/2602.23893) AoE: Always-on Egocentric Human Video Collection for Embodied AI
- Locator: 4.1. Precision of the AoE System
- Evidence: Figure 5f Table 1 给出两数据集 PA-MPJPE/MPJPE/AUC 数值（扁平文本为 3.7/7.4 与 8.9/11.9）；4.1 正文给出运动模糊与错位的归因及 AR 眼镜配对验证。
- Quote: “While larger errors on EgoDex stem primarily from dataset-inherent motion blur and misalignment (Figure 5 d), validation against hardware-tracked AR glasses confirms our model’s precision (Figure 5 c).”
- Authors: bowen-yang; zishuo-li; yang-sun; et al.

### EA-EGOPREC-2026-0473

- Claim: AoE 报告相机轨迹在 7-DoF 对齐后 ATE 全数据集 <5mm，但弱纹理背景使 EgoDex 的尺度无关 ATE-S 退化至 16.2mm；手机工厂内参（Camera2 API）与离线靶标标定的偏差 <1%（均值 0.64%、标准差 0.21%），作者据此免除逐设备标定。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.23893](https://arxiv.org/abs/2602.23893) AoE: Always-on Egocentric Human Video Collection for Embodied AI
- Locator: 4.1. Precision of the AoE System
- Evidence: 4.1 给出 ATE<5mm、ATE-S 16.2mm（EgoDex 弱纹理）与标定偏差 <1%（0.64%±0.21%）；3.2 说明手部 MANO 输出经 SLAM 位姿变换到世界系。
- Quote: “Post 7-DoF alignment, the Absolute Trajectory Error (ATE) remains < 5 mm across all datasets (Table 2 of Figure 5 f). Although texture-less backgrounds in EgoDex degrade ATE-S (16.2 mm), our method maintains centimeter-level accuracy even with monocular RGB input”
- Authors: bowen-yang; zishuo-li; yang-sun; et al.

### EA-EGOPREC-2026-0474

- Claim: AoE 的质量控制设定显式数值门限：自动过滤运动学离群（关节速度 >3σ）与高重投影误差（>5px）的样本，5% 人工抽检用于管线自适应调整，失败样本进入难负样本池重标注；端侧另丢弃时长不足的片段。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.23893](https://arxiv.org/abs/2602.23893) AoE: Always-on Egocentric Human Video Collection for Embodied AI
- Locator: 3.2. Automated Annotation and Quality Filtering Pipeline
- Evidence: 3.2 Quality Control 段给出 >3σ/>5px 门限、5% 抽检与难负样本池机制；3.1 与附录 7.2 给出端侧时长过滤。
- Quote: “We automatically filter kinematic outliers (> 3𝜎 joint velocities) and high reprojection errors (> 5px).”
- Authors: bowen-yang; zishuo-li; yang-sun; et al.

### EA-EGOPREC-2026-0412

- Claim: HoMMI 的无本体采集接口（iPhone ARKit）经与动捕真值对比，平均追踪误差在 5.0mm 位置 / 0.8° 旋转以内；该精度级别的手部（夹爪）轨迹支撑了三个长时程任务 80-90% 的成功率。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.03243](https://arxiv.org/abs/2603.03243) HoMMI: Learning Whole-Body Mobile Manipulation from Human Demonstrations
- Locator: A. Depth quality sensitivity
- Evidence: 附录 IV.C 报告 ARKit 对动捕真值的平均追踪误差 ≤5.0mm/0.8°；主结果 90/85/80% 成功率在该数据精度下获得。
- Quote: “C. iPhone-ARKit tracking error. We measure the average tracking error against ground truth obtained from Motion Capture. The error is within 5.0 mm position / 0.8° rotation.”
- Authors: xiaomeng-xu; jisang-park; han-zhang; et al.

### EA-EGOPREC-2026-0413

- Claim: 对深度注入高斯噪声的敏感性测试显示：std ≤1cm 时 Laundry 成功率不变（90%），std=20mm 时降至 50%——即 ego 3D 观测的几何噪声存在约 1cm 的容忍阈值，超过后性能显著退化。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.03243](https://arxiv.org/abs/2603.03243) HoMMI: Learning Whole-Body Mobile Manipulation from Human Demonstrations
- Locator: A. Depth quality sensitivity
- Evidence: 附录 IV.A Table II：noise std 0/2/10/20mm 对应成功率 90/90/90/50。
- Quote: “We inject additional Gaussian noise into depth and evaluate the Laundry task under 3 noise levels (10 rollouts each). As shown in Tab. II, performance remains unchanged up to 1 cm standard deviation noise and degrades only under substantially larger perturbations. noise std (mm) 0 2 10 20 success (%) 90 90 90 50”
- Authors: xiaomeng-xu; jisang-park; han-zhang; et al.

### EA-EGOPREC-2026-0415

- Claim: HoMMI 将头部 look-at 点从全身 IK 目标中排除、单独控制，以避免干扰双臂末端 SE(3) 追踪；即通过动作表示层面的头-手解耦保护末端轨迹精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.03243](https://arxiv.org/abs/2603.03243) HoMMI: Learning Whole-Body Mobile Manipulation from Human Demonstrations
- Locator: B. Constraint-Aware Whole-body Controller
- Evidence: VI.B 明确说明 look-at 点独立于全身 IK 目标以避免干扰双臂 EE 追踪；与 V.B look-at 表示设计呼应。
- Quote: “Importantly, the look- at point is controlled separately from the whole-body IK and is excluded from the IK objective to avoid interfering with bimanual EEF tracking.”
- Authors: xiaomeng-xu; jisang-park; han-zhang; et al.

### EA-EGOPREC-2026-0496

- Claim: CDF-Glove 的绳驱-编码器手部关节传感在食指 DIP 关节重复定位实验中达到标准差 <0.4°（3 次重复：接触角均值 63.15°、标准差 0.29°），作者称 MCP/PIP 关节同类测试标准差同样低于 0.4°，表明其手部追踪一致性在亚度量级。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05804](https://arxiv.org/abs/2603.05804) CDF-Glove: A Cable-Driven Force Feedback Glove for Dexterous Teleoperation
- Locator: A. CDF-Glove Performance Validation
- Evidence: V.A.3 逐字报告 DIP 三次重复的均值/标准差与 <0.4° 结论，并声称 MCP/PIP 同类结果。
- Quote: “This process repeats three times. We calculate the mean and standard deviation of the contact angle, resulting in an average value of 63.15°, with standard deviations of 0.29°, respectively. As shown in Fig. 9, the standard deviation of repeated positioning for the index finger distal joint (DIP) using CDF-Glove is less than 0.4°, indicating high accuracy and stability.”
- Authors: huayue-liang; ruochong-li; yaodong-yang; et al.

### EA-EGOPREC-2026-0020

- Claim: 在真实操作数据中，可见性感知的 3D 点轨预测（对暂时遮挡点保留监督、仅屏蔽对应点-时刻的损失）使 3D 轨迹误差较 General Flow 基线平均降低 28%（ADE）与 44%（5% ADE，任务关键运动点）；General Flow 因预处理时丢弃任何含不可见点-时刻的轨迹，在 Throw Away Paper 等遮挡严重任务上完全失去对被操作物体的监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.3 Results: 3D Point Track Prediction, Table 1 (extraction section '20 Robot Demos')
- Evidence: Table 1 给出四个真实任务的毫米级 ADE/5% ADE，3PoinTr 全部优于 General Flow；正文明确归因于可见性掩码保留暂时遮挡点的监督（Throw Away Paper 中所有纸点末帧不可见，General Flow 因而无纸运动监督）。
- Quote: “Open Drawer 2.54 16.37 2.18 13.19 Right Glass 3.34 30.38 2.29 18.55 Throw Away Paper 2.40 22.87 1.47 8.17 Fold Sock 1.56 10.09 1.14 4.68”
- Authors: adam-hung; bardienus-p-duisterhof; jeffrey-ichnowski

### EA-EGOPREC-2026-0021

- Claim: 以 3D 点轨（剔除人臂 embodiment 点）为中间表征、仅用 20 条机器人演示与每任务 50 段非约束人类视频，3PoinTr 在四个真实任务上成功率 20/20、20/20、18/20、17/20，平均比最强基线 DP3 高 25.0 个百分点；逐步重预测点轨的 ATM 基线受人类-机器人分布偏移与执行时遮挡影响，在夹爪遮挡物体的 Throw Away Paper 上成功率为 0/20。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: 4.4 Results: Sample-Efficient Policy Learning, Table 3 (extraction section '20 Robot Demos')
- Evidence: Table 3 报告四个真实任务 20 次 rollout 的成功数；正文明确指出 ATM 的 per-step 重预测在遮挡点丢失表征，Throw Away Paper 0% 成功；+25.0pp 为作者陈述的平均差距。
- Quote: “Task ATM [4] DP3 [17] 3PoinTr Open Drawer 6/20 14/20 20/20 Right Glass 3/20 18/20 20/20 Throw Away Paper 0/20 9/20 18/20 Fold Sock 7/20 14/20 17/20”
- Authors: adam-hung; bardienus-p-duisterhof; jeffrey-ichnowski

### EA-EGOPREC-2026-0015

- Claim: 同一 ego 手部检测驱动 IK 重定向管线，在结构化实验室环境取得 86.7%±4.2% 抓取成功率（150 episode），而在非结构化野外环境（杂货店/药店）75 次尝试仅成功 7 次（9.3%）：首要失效模式是周围物体从 ego 相机视角遮挡手部，导致 MediaPipe 丢失拇指/食指 landmark，夹爪角与 IK 目标位置都无法计算；即便结构化环境也有 17.1% 的帧无手部检测。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.11383](https://arxiv.org/abs/2603.11383) Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics
- Locator: VI-B. Pick-and-Place Success Rates / VI-D. In-the-Wild Evaluation
- Evidence: VI-B 给出 86.7%±4.2%；VI-D 给出 7/75=9.3%、遮挡失效机制与 17.1% 无检测率的引用。
- Quote: “Over 75 grasp attempts across both locations, only 7 suc- ceeded, yielding a success rate of 9.3%. The primary failure mode is hand occlusion by surrounding objects: in a cluttered shelf environment, the operator’s hand is frequently occluded by adjacent products, shelf edges, and price tags from the egocentric camera’s perspective. This causes MediaPipe to lose track of the thumb and index finger landmarks, preventing both the gripper angle computation and the IK target position calculation. Ou”
- Authors: hendrik-chiche; antoine-jamme; trevor-rigoberto-martinez; et al.

### EA-EGOPREC-2026-0028

- Claim: 结构化实验室 ego 录制中，MediaPipe 手部检测的可用性远非完备：503 帧里右手检出率仅 77.3%，5.6% 被误判为左手，17.1% 完全无检测；EMA 换手纠正能把误判降到 2.8%，但无检测帧无法用启发式恢复（手不可见即信息为零）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.11383](https://arxiv.org/abs/2603.11383) Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics
- Locator: VI-J. Hand Detection Reliability
- Evidence: VI-J 逐帧统计：77.3% 检出/5.6% 误判/17.1% 无检测；换手纠正 5.6%→2.8%，无检测率不变。
- Quote: “Over 503 frames of a representative pick-and-place record- ing, MediaPipe detected the right hand in 77.3% of frames, with 5.6% erroneously classified as left-hand detections and 17.1% yielding no detection. After applying an EMA-based hand-swap correction heuristic, erroneous left-hand classifica- tions were reduced from 5.6% to 2.8%, while the no-detection rate remained at 17.1% (since no heuristic can recover frames where no hand is visible).”
- Authors: hendrik-chiche; antoine-jamme; trevor-rigoberto-martinez; et al.

### EA-EGOPREC-2026-0460

- Claim: 在 14 人四任务用户研究中，基于视觉追踪的遥操作（TeleDex）在接触/精度要求高的任务上显著劣于编码器外骨骼：剪刀剪切成功率 0.00（DexEXO 0.79、DexUMI 0.00），叠杯 0.33（DexEXO 0.82），钢琴 0.60（DexEXO 0.96）；作者将遥操作的失败归因于精度、响应与力反馈不足。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17323](https://arxiv.org/abs/2603.17323) DexEXO: A Wearability-First Dexterous Exoskeleton for Operator-Agnostic Demonstration and Learning
- Locator: B. Demonstration User Studies, Table I
- Evidence: Table I 给出三设备四任务成功率；V-B 正文明确视觉遥操作剪刀任务失败归因于精度/响应/力反馈，且钢琴任务 DexEXO 比 DexUMI 高 54.5%。
- Quote: “Tele- operation failed at the same task due to a lack of precision, responsiveness, and force feedback.”
- Authors: alvin-zhu; mingzhang-zhu; beomdo-kim; et al.

### EA-EGOPREC-2026-0461

- Claim: 视觉手部追踪系统的失效模式是视线遮挡与接触丰富交互中的追踪不稳定；无物理约束的数据手套则会产生对目标机器人运动学不可行的轨迹（correspondence problem）。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2603.17323](https://arxiv.org/abs/2603.17323) DexEXO: A Wearability-First Dexterous Exoskeleton for Operator-Agnostic Demonstration and Learning
- Locator: A. Teleoperation for Dexterous Manipulation
- Evidence: II-A 明确陈述两类失效并引 [15,24,34]（视觉遮挡）与 [36-38]（手套 correspondence problem）；属作者对文献的归因性陈述。
- Quote: “Vision-based systems provide an unencumbered user experience, yet they are fundamentally limited by line-of-sight occlusion and tracking instability during contact-rich interactions”
- Authors: alvin-zhu; mingzhang-zhu; beomdo-kim; et al.

### EA-EGOPREC-2026-0464

- Claim: 在 DexViTac 数据中，视觉手部追踪（RTMPose）在手-物互遮挡与自遮挡下失效：抓取 1.5-5 s 段出现显著高频抖动、阶跃式突变与物理穿插；IMU 动捕手套输出全程平滑连续、满足物理约束的关节轨迹。该对比为曲线级定性证据，无关节误差数值。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17851](https://arxiv.org/abs/2603.17851) DexViTac: Collecting Human Visuo-Tactile-Kinematic Demonstrations for Contact-Rich Dexterous Manipulation
- Locator: D. Hand Pose Tracking Quality
- Evidence: IV-D 与图 8-9 描述 RTMPose 在遮挡下的抖动/跳变/穿插及手套方案的平滑连续；作者自述『quantitatively analyzed』但仅给出时段定位（1.5-5 s），无误差数值。
- Quote: “It is observed that between 1.5 s and 5 s, the vision- based baseline RTMPose exhibits significant high-frequency jitter and sudden step-like mutations.”
- Authors: xitong-chen; yifeng-pan; min-li; et al.

### EA-EGOPREC-2026-0465

- Claim: 在四任务各 30 次的真机评测中，完整多模态方法平均成功率 85.8%，而仅视觉 ACT 基线仅 17.5%；在视觉遮挡（pipetting 6.7%）与力反馈依赖（erasing 16.7%）任务上仅视觉方案近乎失效。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17851](https://arxiv.org/abs/2603.17851) DexViTac: Collecting Human Visuo-Tactile-Kinematic Demonstrations for Contact-Rich Dexterous Manipulation
- Locator: B. Task-Level Deployment and Generalization, Table I
- Evidence: Table I 给出四任务四方法成功率；IV-B 正文将 B1 的失败归于视觉遮挡与力反馈缺失。
- Quote: “In tasks characterized by visual occlusion (pipetting) or a heavy reliance on force feedback (erasing), the vision- only scheme (B1) yields success rates of only 6.7% and 16.7%.”
- Authors: xitong-chen; yifeng-pan; min-li; et al.

### EA-EGOPREC-2026-0487

- Claim: TeleDex 作者指出：AnyTeleop 类依赖固定外置相机的视觉手部姿态估计对遮挡、视角变化与深度歧义敏感（按其自身 limitation），且其腕部位姿由图像深度线索推断而非直接 6-DoF 传感，在快速运动与接触密集交互中会引入噪声。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2603.17065](https://arxiv.org/abs/2603.17065) TeleDex: Accessible Dexterous Teleoperation
- Locator: C. Dexterous Hand Teleoperation
- Evidence: II.C 段先引 AnyTeleop 自身 limitation 说明固定外置相机方案的三种敏感性，再以作者分析指出腕部位姿来自深度线索的噪声风险。
- Quote: “While effective, such approaches rely on camera- based hand pose estimation from a fixed external viewpoint, making them sensitive to occlusions, viewpoint changes, and depth ambiguity as outlined in their limitations. Moreover, wrist pose is inferred from image-based depth cues rather than direct 6-DoF sensing, which can introduce noise during fast motions and contact-rich interactions.”
- Authors: omar-rayyan; maximilian-gilles; yuchen-cui

### EA-EGOPREC-2026-0488

- Claim: TeleDex 的腕戴式设计将手机前置相机刚性固定在操作者手臂上，相机随手部一起移动，使操作者无需保持手部处于固定相机视野内，从而缓解固定外置相机方案的视野约束与遮挡问题。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.17065](https://arxiv.org/abs/2603.17065) TeleDex: Accessible Dexterous Teleoperation
- Locator: B. Wrist-Mounted Setting
- Evidence: III.B 段逐字对比固定外置相机方案（手须保持在视野内、位姿由深度线索推断）与腕戴共动方案的自由活动能力。
- Quote: “Unlike external camera-based approaches, where the user must ensure their hand remains within the field of view of a fixed camera since the pose is inferred from image-based depth cues, the arm-mounted configuration allows the operator to move freely because the camera moves together with the hand.”
- Authors: omar-rayyan; maximilian-gilles; yuchen-cui

### EA-EGOPREC-2026-0089

- Claim: UniDex 把手部姿态估计偏差显式列为 ego 人体数据转机器人轨迹时的系统性误差来源之一：其重定向在机器人基座前插入 6-DoF dummy base 偏移，并通过对每个人体数据集×每种灵巧手做一次基础交互式标定来选择该偏移，以吸收坐标系差异与手部姿态估计偏差；接触密集片段再人工微调少量帧，作者报告该基础标定即可覆盖绝大多数轨迹，使管线能以 modest 人工量扩展到大规模 ego 数据集。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.22264](https://arxiv.org/abs/2603.22264) UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos
- Locator: 3.2. Human-Robot Transformation
- Evidence: 3.2.1 说明指尖 IK + dummy base 的两阶段人机回环流程，并明确 dummy 偏移用于处理跨数据集系统性差异（含 hand-pose estimation bias）与手型形态差异；同段报告基础标定覆盖绝大多数轨迹。
- Quote: “we per- form a basic interactive calibration to select dummy base offsets to handle systematic differences across datasets (e.g., coordinate frames/ hand-pose estimation bias) and hand morphology differences”
- Authors: gu-zhang; qicheng-xu; haozhe-zhang; et al.

### EA-EGOPREC-2026-0456

- Claim: 以陆上 UMI-Aquatic 手持示教训练的深度 affordance 模型为零样本感知接口时，水下抓取策略在 ID 设置达 85%（RGB 基线 65%），在未见背景 OOD 下保持 80% 而 RGB 基线与 RGB 添加消融均崩溃到 0%，在仅陆上出现的新物体上零样本达 75%（RGB 基线 50%），每方法-条件 20 次试验。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.27012](https://arxiv.org/abs/2603.27012) UMI-Underwater: Learning Underwater Manipulation without Underwater Teleoperation
- Locator: B. Methods Compared; D. OOD Visual Generalization Under Unseen Backgrounds
- Evidence: Tables I-III 分别报告 ID 85/65、OOD 背景 80/0/0、新物体 75/50；IV-D 正文确认背景偏移下 RGB 策略崩溃且加入 RGB 的消融同样归零。
- Quote: “Table II shows that under background shift, RGB-based policies fail catastrophically.”
- Authors: hao-li; long-yin-chung; jack-goler; et al.

### EA-EGOPREC-2026-0061

- Claim: 在以单目相机采集的人手关键点为输入的仿真 Wuji 手遥操作中，Kilohertz-Safe 的 QP+约束管线平均逐帧计算延迟 9.05ms（std 2.29ms，99%ile 13.42ms），85.82% 控制步满足 100Hz；同设置下 Dex-Retargeting 为 15.59ms/34.41%，GeoRT 为 34.49ms/0.19%。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.29213](https://arxiv.org/abs/2603.29213) Kilohertz-Safe: A Scalable Framework for Constrained Dexterous Retargeting
- Locator: A. Experimental Setup, Table I
- Evidence: Table I 直接在相同仿真平台上列出三种方法的延迟均值/标准差/99 分位与 RT@100Hz，本文方法全面最优；实验设置（IV-A）说明仿真输入来自单目相机关键点。
- Quote: “Ours 9.05 2.29 13.42 85.82 Dex-Retargeting 15.59 12.50 32.82 34.41 GeoRT 34.49 4.28 49.90 0.19”
- Authors: yinxiao-tian; ziyi-yang; zinan-zhao; et al.

### EA-EGOPREC-2026-0386

- Claim: WARPED 的重定向把误差来源按时相分流：接触前末端位姿由拇指-食指关节映射（手部姿态质量主导），接触期间 EE 位姿由物体相对接触帧的运动刚性推出（物体位姿跟踪质量 1:1 主导末端轨迹）。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.10809](https://arxiv.org/abs/2604.10809) WARPED: Wrist-Aligned Rendering for Robot Policy Learning from Egocentric Human Demonstrations
- Locator: E. Retargeting and Rendering
- Evidence: III-E 与公式 (15)：接触前 hand-pose 映射，接触期 EE 刚性跟随物体。
- Quote: “the end-effector pose is mapped from the human-hand pose using the thumb and index joints, as shown in Fig. 4(b) and discussed in more detail in Appendix F. Following Pan et al. [70], we apply pre- contact trajectory optimization to prevent unintended gripper- object collisions. The optimization is formulated as min T ee t<ts λ funnel L funnel + λ col L col + λ smooth L smooth (14) where L funnel constrains trajectories to remain close to the orig- inal motion, L col prevents gripper-object”
- Authors: harry-freeman; chung-hee-kim; george-kantor

### EA-EGOPREC-2026-0387

- Claim: HAMER 单帧手部姿态估计被作者明确指出噪声大且时序不一致（无帧间时序信息），WARPED 用两阶段优化（先固定关节只优化全局旋转/平移/形状的 2D 重投影+时序平滑，再加入深度监督细化关节）作为手部检测误差的吸收手段。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.10809](https://arxiv.org/abs/2604.10809) WARPED: Wrist-Aligned Rendering for Robot Policy Learning from Egocentric Human Demonstrations
- Locator: C. Hand Pose Initialization
- Evidence: Appendix C 描述 HAMER 噪声与两阶段细化。
- Quote: “The 3D hand pose estimates (Sec. III-C2) produced by HAMER [74] are often noisy and temporally inconsistent, as HAMER does not use temporal information between frames”
- Authors: harry-freeman; chung-hee-kim; george-kantor

### EA-EGOPREC-2026-0505

- Claim: 在 LfHV 领域共识中，接近动作的迁移路线的典型失效模式是 mis-grounding：从人类视频提取的轨迹、接触线索或潜动作在视频中看似合理，但违反目标机器人的运动学、控制频率、碰撞约束或接触动力学。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.27621](https://arxiv.org/abs/2604.27621) Robot Learning from Human Videos: A Survey
- Locator: 30 Journal Title XX(X)
- Evidence: 3.5 节作者对文献失效模式的综合：远离动作的路线失效于 under-grounding，接近动作的路线失效于 mis-grounding，观测路线失效于 false visual equivalence。
- Quote: “Methods close to actions usually fail through mis-grounding: the extracted trajectory, contact cue, or latent action appears plausible in the human video but violates the target robot’s kinematics, control frequency, collision constraints, or contact dynamics.”
- Authors: ma-et-al-shanghai-jiao-tong-university-university-of-cambridge-corresponding-hesheng-wang

### EA-EGOPREC-2026-0507

- Claim: 手部重建工具链的演进反映了已知误差模式：HaMeR 的端到端回归存在固有的 misalignment 与错误位姿；WiLoR 通过 mesh 对齐多尺度特征的精修层缓解；HaWoR 进一步面向自我中心视频做世界系手部运动重建（解耦相机系手部恢复与世界系相机轨迹估计，并对出画帧做 motion infilling），产出时序连贯的全局手部轨迹。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2604.27621](https://arxiv.org/abs/2604.27621) Robot Learning from Human Videos: A Survey
- Locator: 14 Journal Title XX(X)
- Evidence: 综述转述 Pavlakos et al. 2024 (HaMeR)、Potamias et al. 2025 (WiLoR)、Zhang et al. 2025d (HaWoR) 的方法定位与动机；这些是对被引工作的描述而非综述作者的实验。
- Quote: “To address the inherent misalignments and incorrect poses of HaMeR’s end-to-end regression, WiLoR (Potamias et al. 2025) introduces an additional refinement layer that deforms hand pose using mesh- aligned multi-scale features. It supports efficient multi-hand reconstruction and smooth monocular video tracking”
- Authors: ma-et-al-shanghai-jiao-tong-university-university-of-cambridge-corresponding-hesheng-wang

### EA-EGOPREC-2026-0508

- Claim: 在综述统计的动作导向迁移代表工作中，52% 使用纯自我中心视频、41% 使用纯外部视角视频；作者分析指出越接近可执行动作，保留交互几何与时序精确的操作线索越重要，自我中心视频因此在该家族占主导。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.27621](https://arxiv.org/abs/2604.27621) Robot Learning from Human Videos: A Survey
- Locator: 28 Journal Title XX(X)
- Evidence: Tab.7 及 3.4.1 节给出 52%/41% 统计与'closer observations of hand-object interactions and manipulation timings'的机制解释。
- Quote: “The egocentric tendency becomes even more pronounced in action-oriented transfer, where egocentric and exocentric sources account for 52% and 41% of the reviewed works, respectively.”
- Authors: ma-et-al-shanghai-jiao-tong-university-university-of-cambridge-corresponding-hesheng-wang

### EA-EGOPREC-2026-0509

- Claim: 综述的数据集趋势分析指出：近期数据集越来越重视细粒度手部位姿与关节标注，反映了'准确的手部运动建模对将 HOI 知识迁移到机器人操作至关重要'这一日益增强的共识；智能眼镜（Vision Pro、Aria）的内置追踪使手部位姿可免额外标注管线直接获取。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.27621](https://arxiv.org/abs/2604.27621) Robot Learning from Human Videos: A Survey
- Locator: 32 Journal Title XX(X)
- Evidence: 4.1 节趋势第 4 条原文表述；Tab.10 的 Pose annot. 列（Mocap/Device tracking/RGB/RGB(-D)+opt.）为标注协议差异提供结构化佐证。
- Quote: “This trend reflects the growing recognition that accurate hand motion modeling is critical for transferring HOI knowledge to robot manipulation. Besides, with the development of smart glasses (e.g., Vision Pro and Aria), hand poses can be efficiently captured with built-in tracking algorithms, without requiring additional annotation pipelines”
- Authors: ma-et-al-shanghai-jiao-tong-university-university-of-cambridge-corresponding-hesheng-wang

### EA-EGOPREC-2026-0510

- Claim: 综述总结：尽管 affordance 迁移快速发展，其有效性仍严重依赖可靠的 HOI 分析、准确的空间定位与鲁棒的重定向；这一依赖在复杂操作任务、尤其是严重遮挡、大视角变化、物体与末端类别多样的开放世界设定下尤其受到挑战。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.27621](https://arxiv.org/abs/2604.27621) Robot Learning from Human Videos: A Survey
- Locator: 24 Journal Title XX(X)
- Evidence: 3.3.1(f) affordance 家族结论段的作者综合判断，与 Tab.9 失效条件互证。
- Quote: “Despite the rapid development of affordance-based transfer, its effectiveness still depends heavily on reliable HOI analysis, accurate spatial grounding, and robust retargeting. This is particularly challenged in complex manipulation tasks, especially in open-world settings with severe occlusion, large viewpoint variation, and diverse object and effector categories.”
- Authors: ma-et-al-shanghai-jiao-tong-university-university-of-cambridge-corresponding-hesheng-wang

### EA-EGOPREC-2026-0256

- Claim: 在受控 ego 采集的中心帧手部 crop 上，22-DoF 手部关节角回归的精度地板为：手部专用 WiLoR 平均 MAE 4.7°（gesture/user/both 划分 3.9°/5.6°/5.7°），最佳通用骨干 ResNet-152 为 5.1°；所有视觉模型在跨被试（user/both）划分上误差一致高于跨手势划分。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05712](https://arxiv.org/abs/2605.05712) EgoEMG: A Multimodal Egocentric Dataset with Bilateral EMG and Vision for Hand Pose Estimation
- Locator: 5.2 Vision-to-Pose Results (Table 3)
- Evidence: Table 3 视觉行给出 WiLoR 3.9/5.6/5.7/4.7 与 ResNet-152 4.3/6.1/6.1/5.1；正文确认 WiLoR 最强视觉基线与跨被试更难。
- Quote: “Input Method Params Gesture User Both Avg ResNet-based comparison Vision V-RN18 11.5M 5.1 ±1.3 6.8 ±1.7 6.8 ±0.9 5.9 EMG+Vision F-RN18+S 15.5M 4.6 ±1.3 6.4 ±1.4 6.4 ±0.8 5.4 ViT-based comparison Vision V-ViT-S 21.9M 5.0 ±1.3 7.3 ±2.4 7.2 ±0.5 6.0 EMG+Vision F-ViT-S+S 25.9M 4.5 ±1.3 6.8 ±1.2 6.8 ±0.6 5.5 Additional vision-only backbones Vision V-RN50 23.5M 4.5 ±1.3 6.2 ±2.2 6.2 ±0.7 5.3 Vision V-RN152 58.2M 4.3 ±1.2 6.1 ±2.3 6.1 ±0.7 5.1 Vision V-ViT-B 86.2M 4.8 ±1.3 7.0 ±2.3”
- Authors: ziheng-xi; jiayi-yu; yitao-wang; et al.

### EA-EGOPREC-2026-0258

- Claim: 动捕到手部姿态真值的重建管线自身带误差地板：EgoEMG 的 learning-based markers2mano 管线无效帧率 3.6%（EMG2Pose 逐帧 IK 求解器为 12.7%，降低 3.5 倍），重建 MANO 网格的平均 marker-to-mesh 对齐误差为 4.3mm（InterHand2.6M 子集 3.2mm）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05712](https://arxiv.org/abs/2605.05712) EgoEMG: A Multimodal Egocentric Dataset with Bilateral EMG and Vision for Hand Pose Estimation
- Locator: 3.2 Pose Label Reconstruction
- Evidence: 3.2 节给出 12.7%→3.6%（3.5×）与 4.3mm/3.2mm 两组数字。
- Quote: “Compared with the per-frame inverse-kinematics solver used by EMG2Pose, which has a reported 12.7% invalid-frame rate, our learning-based reconstruction reduces the invalid-frame rate to 3.6%, a 3 Single-hand Symmetric bimanual Asymmetric bimanual Gesture Type GT Hand Pose Left-Hand EMG Right-Hand EMG Egocentric View Exeternal View (RGB-D) Figure 2: Representative synchronized samples from EgoEMG. Each row (3.9 s window) shows GT hand pose, bilateral EMG, egocentric RGB at window center, an”
- Authors: ziheng-xi; jiayi-yu; yitao-wang; et al.

### EA-EGOPREC-2026-0546

- Claim: 长时 ego 采集的追踪漂移经 ArUco 标记回访实测：六类环境中除全屋遍历（会话末 1.5cm）外漂移均低于 1cm，且所有情况下低于轨迹长度的 0.1%。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: IV. DATA QUALITY VALIDATION
- Evidence: IV-A2 表 III：六环境回访漂移 0.1-1.5cm；正文给出 <1cm（除全屋遍历）与 <0.1% 轨迹长度两个汇总口径。
- Quote: “drift is below 1 cm in all but the whole-house traversal (1.5 cm end-of-session) and below 0.1% of trajectory length in all cases”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathor; et al.

### EA-EGOPREC-2026-0548

- Claim: 在无法获得手部几何真值的条件下，MobileEgo 用三项无真值一致性指标验收手部标注：20 根 MANO 骨长的中位变异系数 1.27%（左）/1.43%（右）（典型 7-8cm 骨上约 1mm 稳定性）、15 个屈曲关节角 99.99% 落在已发表生物力学界限内、腕部速度/加速度分布无瞬移级不连续；小指末节因骨长约 2cm 放大了固定绝对噪声，CV 升至约 7.5%。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: APPENDIX
- Evidence: 附录 VIII：骨长 CV 1.27%/1.43%（约 1mm/7-8cm），剔除小指末节后双手 pooled CV<1%；关节角 99.99% 合法；小指末节 CV 约 7.5% 的原因分析；腕部中位速度 0.34/0.27 m/s。
- Quote: “Median coefficient of variation (CV) of the 20 MANO bone lengths is 1.27% (left hand) and 1.43% (right), indicating stability to within roughly 1 mm on a typical 7–8 cm bone”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathor; et al.

### EA-EGOPREC-2026-0012

- Claim: 在自建 ego 双目事件数据集 EgoEVHands 上，EgoEV-HandPose 的绝对 3D 手部姿态误差为 MPJPE 22.03mm（HOMO 同分布）/ 30.54mm（HETER 跨被试）；传感模态是低光与运动模糊场景的误差量级决定因素——RGB 双目基线 HandMvNet 低光下 82.43mm，而事件流方法 29.50mm，事件单目双手基线 Ev2Hands 整体达 115.13mm。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.12297](https://arxiv.org/abs/2605.12297) EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras
- Locator: V-C. Main Results and Scenario Analysis (Table II)
- Evidence: V-C 正文给出 22.03/30.54mm 双协议数字；V-D 正文给出低光 82.43→29.50mm 与 Ev2Hands 115.1mm 对比，均与 Table II 行值一致。
- Quote: “Ours (KeypointBEV) w/o action cls. – E-B-1 11.48 22.03 18.96 22.31 21.90 22.04 21.99 21.65 22.09 22.13 5.88 19.86 HETER (Heterogeneous Distribution) HandMvNet † [13] VISAPP’25 F-B-1/3 38.41 71.87 34.83 62.16 82.43 68.31 72.62 69.98 73.97 73.64 85.9 87.7 Ev2Hands † [12] CVPR’24 E-M-3 68.90 115.13 82.30 118.39 111.66 120.46 114.05 115.34 112.69 114.30 4.50 21.50 EvHandPose † [11] CVPR’24 E-M-3 28.15 60.20 26.00 58.49 62.06 60.20 – – – – 47.4 3.69 EventEgo3D † [9] CVPR’23 E-M-1 42.10 72.76 36.5”
- Authors: luming-wang; hao-shi; jiajun-zhai; et al.

### EA-EGOPREC-2026-0014

- Claim: 重投影引导的迭代精化显著压缩 3D 误差与离群点：三角化初始化为 52.72mm，首轮迭代即降 26.1%，最终（Iter 2）达 30.54mm；PCK 曲线下面积从初始三角化的 0.436 提升到融合模型的 0.589（阈值 0-50mm），作者将收益归因于遮挡区域大误差离群点的削减。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.12297](https://arxiv.org/abs/2605.12297) EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras
- Locator: V-F. Ablation Study (Fig 9 / Fig 10)
- Evidence: V-F 正文给出 52.72→30.54mm 与 26.1% 首轮降幅；Fig 10 说明文字给出 AUC 0.589 vs 0.436，正文明确‘particularly in occluded regions’。
- Quote: “To isolate the contributions of the proposed components, specifically the KeypointBEV module, we analyze the per- formance evolution from the initial coarse stage to the final iteration (see Fig. 9). The initial coarse stage (heatmap + triangulation) yields higher errors (an MPJPE of 52.72 mm), while the final refined output (Iter 2) achieves the best MPJPE. By applying reprojection-guided visual feedback, the MPJPE drops by 26.1% after the first iteration and reaches 30.54 mm finally. This prog”
- Authors: luming-wang; hao-shi; jiajun-zhai; et al.

### EA-EGOPREC-2026-0043

- Claim: 真机扭转实验中，误差沿时间轴增大的机制被归因于输入侧视觉追踪退化：部分指尖遮挡、重抓与累积姿态失配偏置视觉人手意图估计；以 ArUco 物转为参照，DexTwist 转角跟踪 RMSE 14.3°/MAE 11.9°/Corr 0.96，优于向量重定向的 23.2°/15.6°/0.83；以视觉估计的人手意图为参照时两者误差均大幅升高（33.7°/25.9°/0.67 vs 40.3°/32.8°/0.60），且 DexTwist 的稳定正则项可使执行轨迹比含噪意图估计更接近实测物转。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.12182](https://arxiv.org/abs/2605.12182) DexTwist: Dexterous Hand Retargeting for Twist Motion via Mixed Reality-based Teleoperation
- Locator: C. Experimental Results
- Evidence: IV-C 真机结果段：五种试验聚合；Table II 双参照数值（ArUco：23.2/15.6/0.83 vs 14.3/11.9/0.96；意图：40.3/32.8/0.60 vs 33.7/25.9/0.67）；同段明确归因'Late-phase errors can increase due to partial fingertip occlusion, re-grasping, and accumulated orientation mismatch, which bias the visual estimate of human intent'。
- Quote: “Late-phase errors can increase due to partial fingertip occlusion, re-grasping, and accumulated orientation mismatch, which bias the visual estimate of human intent. Although DexTwist tracks Human Intent as its reference, the stability regularizers can yield closer alignment with measured object rotation than with the noisy intent estimate.”
- Authors: dongmyoung-lee; chengxi-li; dongheui-lee

### EA-EGOPREC-2026-0010

- Claim: 在四个基准（ARCTIC/HOT3D/H2O/HO3D）上，手部姿态的对齐精度（PS-MJE 5.6-9.9mm）与绝对相机系定位精度严重脱节：最好的绝对方法（EgoForce）CS-MJE 仍达 43.9mm（HOT3D）与 49.5mm（ARCTIC），而 SOTA root-relative 方法 HaMeR 经单目深度提升到相机系（HaMeR_D）后误差达 4493.7mm（HOT3D）与 2067.3mm（ARCTIC）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.12498](https://arxiv.org/abs/2605.12498) EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera
- Locator: 4.1 Results, Table 1
- Evidence: Table 1 同表并列 CS-MJE 与 PS-MJE 两列：PS-MJE 全方法 5.6-9.9mm，而 CS-MJE 从 EgoForce 的 25.0-49.5mm 到 HaMeR_D 的 561.5-4493.7mm 跨越三个数量级。
- Quote: “Method ARCTIC HOT3D H2O HO3D CS-MJE ↓ PS-MJE ↓ CS-MJE ↓ PS-MJE ↓ CS-MJE ↓ PS-MJE ↓ CS-MJE ↓ PS-MJE ↓ HaMeR D 2067.3 9.2 4493.7 8.3 631.6 6.3 561.5 7.7 MobRecon 81.5 9.6 116.3 8.0 49.1 6.2 121.7 9.2 HandOccNet 256.3 8.0 284.8 6.6 62.1 5.3 156.4 9.1 HandDGP 51.7 9.9 61.3 8.6 29.9 6.3 50.3 9.3 EgoForce (Ours) 49.5 8.0 43.9 6.6 25.0 5.6 49.5 9.0”
- Authors: christen-millerdurai; shaoxiang-wang; yaxu-xie; et al.

### EA-EGOPREC-2026-0054

- Claim: 对单目视频提取的人体关键点做纯几何重定向（GR）会把视频噪声直接传导为物理不可用的机器人轨迹：GR 的接触序列错误率最高达 32.12%（squat），各动作均高于或远高于 DDR（0%-13.71%）；作者明确归因——GR 缺少动态接触模型且纯依赖带噪专家示教，导致预期接触相出现滑移伪影，而动力学一致性约束（IDR/DDR）能强制接触点静止从而缓解这些伪影。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.23762](https://arxiv.org/abs/2605.23762) Direct Dynamic Retargeting for Humanoid Imitation Learning from Videos
- Locator: B. Retargeted trajectories
- Evidence: Table III 报告五动作 GR/IDR/DDR 接触序列错误率（对手工标注真值）；IV-B 第 3 小节明确将 GR 滑移伪影归因于缺少动态接触模型与依赖带噪示教，并称动态一致性约束缓解之。
- Quote: “Movement GR IDR DDR (ours) Squat 32.12% 0.00% 0.00% Kung fu 10.53% 13.03% 4.23% One-foot Balance 21.37% 24.72% 13.71% Pistol Squat 15.00% 9.13% 5.35% Balancing Stick 8.19% 20.73% 7.86%”
- Authors: constant-roux; ludovic-de-mattes; armand-jordana; et al.

### EA-EGOPREC-2026-0055

- Claim: 参考轨迹的物理质量沿'参考→RL 监督'通道传播为学习效率差距：用 DDR 参考训练的 RL 策略在几乎所有动作上 final reward 最高、收敛最快（pistol squat 383.7/79.6k 步 vs GR 200.7/128.4k 步；one-foot balance 360.0/76.3k vs GR 253.7/219.9k），而 GR 参考因物理不可行使 RL 智能体陷入跟踪与物理定律的持续冲突；IDR 虽可行但因 GR 初始化的运动学偏差在 balancing stick 上未能收敛（Table VI 记为 '-'）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.23762](https://arxiv.org/abs/2605.23762) Direct Dynamic Retargeting for Humanoid Imitation Learning from Videos
- Locator: C. Imitation Policies
- Evidence: Table VI 报告三方法五动作的 final reward 与 90% 收敛步数；IV-C 正文解释 GR 参考物理不可行导致 RL 冲突、IDR 被 GR 初始化偏差锚定。
- Quote: “Movement GR IDR DDR (Ours) Final 90% Final 90% Final 90% Squat 307.0 41.3k 374.8 38.2k 363.2 21.1k Kung fu 322.7 91.1k 366.8 95.6k 398.4 71.6k One-foot Bal. 253.7 219.9k 301.6 57.3k 360.0 76.3k Pistol Squat 200.7 128.4k 340.8 93.5k 383.7 79.6k Bal. Stick 252.6 103.2k - - 364.5 78.9k”
- Authors: constant-roux; ludovic-de-mattes; armand-jordana; et al.

### EA-EGOPREC-2026-0056

- Claim: DDR 的作者声称：把参考生成问题直接 formulation 在任务空间并采用 Laplacian 图距离，能有效缓解从视频中提取的人体数据的噪声与漂移影响；该 Laplacian 相对形状度量显式保持示教的局部结构形状，且对全局平移与旋转不变，采样式 CEM 求解器同时内在地处理带噪视频数据中接触识别的歧义。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.23762](https://arxiv.org/abs/2605.23762) Direct Dynamic Retargeting for Humanoid Imitation Learning from Videos
- Locator: V. CONCLUSION
- Evidence: V. CONCLUSION 明确陈述 Laplacian 任务空间距离缓解视频噪声与漂移；III-D 说明该度量对全局平移旋转不变；I. INTRODUCTION 说明 CEM 采样内在处理带噪视频接触识别歧义。
- Quote: “ing. By formulating the reference generation problem di- rectly in the task space using a Laplacian graph distance, our approach effectively mitigates the impact of noisy and drifting human data extracted from videos. Furthermore, by employing a sampling-based solver directly within a physics simulator, DDR inherently optimizes over complex contact sequences while guaranteeing the physical viability of the resulting motions.”
- Authors: constant-roux; ludovic-de-mattes; armand-jordana; et al.

### EA-EGOPREC-2026-0072

- Claim: 仅使用单 RGB-D 相机（MediaPipe 检测 + 深度恢复腕部 3D + 在线 MANO 拟合 + 高斯平滑）采集的低成本演示，经重定向与演示引导 RL 后，在 3 种灵巧手 × 3 种关节物体共 9 个跨本体组合上取得平均 36.5% 成功率，部分任务最高 93.3%。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.03268](https://arxiv.org/abs/2606.03268) EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations
- Locator: 1 Introduction
- Evidence: 引言与 4.2 一致报告 36.5% 平均成功率与 93.3% 上限；采集管线细节（MediaPipe、深度腕部恢复、在线 MANO、高斯平滑）见 3.1。
- Quote: “Under low-cost demonstration conditions, EaDex achieves an average success rate of 36.5% across nine cross-embodiment manipulation tasks, corresponding to a 55.3% relative improvement over the baseline without demonstration annealing, and in some tasks, EaDex achieves a success rate of up to 93.3%.”
- Authors: qian-zhao-217607; xin-tong; chengdong-wu; et al.

### EA-EGOPREC-2026-0075

- Claim: 作者明确指出 RGB-D 感知与在线 MANO 拟合会给手部运动序列引入高频时序噪声，并在重定向与策略学习之前沿时间轴施加高斯平滑以提升运动序列的时序连续性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.03268](https://arxiv.org/abs/2606.03268) EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations
- Locator: 3.1 Dataset Construction
- Evidence: 3.1 原文说明噪声来源（RGB-D 感知、在线 MANO 拟合）与高斯平滑（式 3）的处理位置；该处理在数据进入重定向与 RL 之前完成。
- Quote: “To further reduce high-frequency temporal noise introduced by RGB-D perception and online MANO fitting, we apply Gaussian smoothing along the temporal axis”
- Authors: qian-zhao-217607; xin-tong; chengdong-wu; et al.

### EA-EGOPREC-2026-0373

- Claim: 手部姿态质量对共训练迁移呈因果剂量-响应：以三角测量手部为基准注入拟合 TriHands-HaWoR 误差分布的标定高斯噪声，迁移成功率从 0.0× 噪声的 48.3±19.6% 单调降至 0.5× 的 30.0±13.1% 与 1.0× 的 20.0±6.5%；参照系中 SOTA 单目估计器 HaWoR 相对三角测量真值的世界系误差 W-MPJPE 达 161.85mm，且 1 秒预测视界内的手部关节平移常被深度值噪声主导。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.06627](https://arxiv.org/abs/2606.06627) What Matters When Cotraining Robot Manipulation Policies on Everyday Human Videos?
- Locator: 6 Results
- Evidence: 6 Results 手部质量段 + Tab. 3(HaWoR 四误差指标) + Tab. 4(三档噪声成功率) + 深度噪声主导机制句。
- Quote: “Given the metrics in Table 3, it is unsur- prising the monocular transfer is worse — the hand joint translations in our 1-second prediction horizon can often be dominated by the noise in the depth val- ues. Table 4 shows that transfer degrades monotoni- cally with noise level, further confirming that higher quality hands lead to greater transfer.”
- Authors: richard-li; aditya-prakash; andrew-wen; et al.

### EA-EGOPREC-2026-0439

- Claim: 动作标签保真度显著影响可部署性：8 任务平均全任务成功率从可执行手命令标签的 88.75% 降到 state-as-action（以测量手部状态作标签）的 51.25%，去触觉变体为 70.00%；差距在需要维持/恢复接触的任务上最大。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.06033](https://arxiv.org/abs/2606.06033) RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning
- Locator: 5.1 Policies Learned from RealDexUMI Demonstrations (Table 2)
- Evidence: Table 2 给出三行完整消融（88.75/70.00/51.25），5.1 正文解释 state-as-action 在维持/恢复接触任务上恶化最明显。
- Quote: “RealDexUMI 1.00 1.00 0.85 1.00 0.80 0.85 0.70 0.90 88.75% w/o tactile 0.90 1.00 0.45 0.80 0.55 0.70 0.60 0.60 70.00% State-as-action 0.65 0.85 0.30 0.35 0.20 0.45 0.60 0.70 51.25%”
- Authors: chaoyi-xu; yixuan-jiang; jiahui-huan; et al.

### EA-EGOPREC-2026-0377

- Claim: 自适应接触优化（对手部全局平移与指尖局部几何的有界修正）将物体平移误差从 1.36cm 降到 0.82cm、指尖误差从 2.18cm 降到 1.65cm、成功率从 36.2% 提升到 49.5%，表明手部姿态估计误差引起的指尖悬空/穿透可被几何级后处理部分吸收。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08057](https://arxiv.org/abs/2606.08057) EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets
- Locator: 3 Egocentric Demonstration Data Collection and Quality Assessment (Table 2)
- Evidence: w/o Adaptive Contact Optimization 与完整 EgoAERO 两行消融差值即为接触优化的贡献。
- Quote: “EgoDex-R Only Hand Pose 28.6 4.72 3.35 2.48 9.8 EgoDex-R w/o Adaptive Contact Optimization 15.4 1.36 2.93 2.18 36.2 EgoDex-R EgoAERO 9.7 0.82 2.48 1.65 49.5”
- Authors: yichen-niu; haoran-lv; xinrui-zhang; et al.

### EA-EGOPREC-2026-0378

- Claim: 单目手部姿态估计存在全局深度偏差，EgoAERO 用 RGB-D 深度图对手部全局平移做基于鲁棒残差的校正（只校正全局平移、不动关节），这是对手部检测误差在源头端的补偿。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08057](https://arxiv.org/abs/2606.08057) EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets
- Locator: 2.1 Asset-free Egocentric Hand-Object Reconstruction
- Evidence: 2.1.3 节陈述深度偏差机制与校正设计。
- Quote: “Since monocular hand pose estimation may suffer from global depth bias, EgoAERO further uses the RGB-D depth map to correct the global translation of the whole hand. Specifically, the system projects MANO vertices onto the RGB-D image, queries RGB-aligned depth values in local neigh- borhoods, and estimates a translation correction ∆p C t from the robust residuals between the visible 3D hand surface observations and the predicted vertices. This correction is applied only to the global hand tran”
- Authors: yichen-niu; haoran-lv; xinrui-zhang; et al.

### EA-EGOPREC-2026-0379

- Claim: 在 ego 视角下头部运动会混入手腕轨迹（静止物体出现虚假漂移、手腕轨迹含有与操作无关的相机运动），EgoAERO 以 RGB-D SLAM 将所有帧变换到固定桌面坐标系并对手部像素降权，以分离相机运动与手部运动。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08057](https://arxiv.org/abs/2606.08057) EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets
- Locator: 2.1 Asset-free Egocentric Hand-Object Reconstruction
- Evidence: 2.1.4 节陈述 ego motion 混淆机制与 SLAM 补偿。
- Quote: “Since the egocentric camera is mounted on the head, head motion is mixed into the hand-object tra- jectories expressed in the camera frame: static objects may exhibit spurious drift, and the hand wrist trajectory may contain camera motion unrelated to manipulation”
- Authors: yichen-niu; haoran-lv; xinrui-zhang; et al.

### EA-EGOPREC-2026-0381

- Claim: EgoAERO 将 ego 数据可接受阈值操作化为有界可恢复性：只有能靠小幅、局部、可解释的修正（不修改物体轨迹、不重解手部关节）恢复稳定接触的序列才判为可用，并输出 accept / repairable accept / recapture 三档采集决策。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08057](https://arxiv.org/abs/2606.08057) EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets
- Locator: 3 Egocentric Demonstration Data Collection and Quality Assessment
- Evidence: 第 3 节在线质量评估机制。
- Quote: “The online assessment is based on bounded recoverability: a sequence is considered use- ful if stable hand-object contact can be recov- ered through small, local, and interpretable corrections, without modifying the object trajectory or re-solving hand articulation. EgoAERO evaluates tracking stability, contact consistency, residual penetration, and temporal jitter from the reconstructed hand state, object pose, and object geometry. It outputs three collection decisions: accept, repairable accep”
- Authors: yichen-niu; haoran-lv; xinrui-zhang; et al.

### EA-EGOPREC-2026-0382

- Claim: 该管线判定重定向 rollout 成功的默认阈值为物体旋转误差 <30°、物体平移误差 <3cm、手部关节误差 <8cm、指尖误差 <6cm，给出了仿真重放场景下末端轨迹可用性的一组显式容差。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08057](https://arxiv.org/abs/2606.08057) EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets
- Locator: References (Appendix H Definitions of Evaluation Metrics)
- Evidence: Appendix H 给出默认成功阈值。
- Quote: “By default, we set τ r = 30 ◦ , τ t = 3 cm, τ j = 8 cm, and τ f t = 6 cm”
- Authors: yichen-niu; haoran-lv; xinrui-zhang; et al.

### EA-EGOPREC-2026-0418

- Claim: 对象中心关键帧细化是一种不依赖手部轨迹精度的缓解机制：从物体运动中检测接触/交互/脱离关键帧，用仿真器中的物体几何与位姿优化这些帧的机器人构型，再以锚点插值修正原始重定向轨迹——即把可信来源从'含噪的手部估计'换成'仿真回环中的物体信息'。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08828](https://arxiv.org/abs/2606.08828) Video2Sim2Real: Full-Stack Autonomous Dexterous Skill Acquisition from a Single Human Video
- Locator: 4.2 Refinement Modules
- Evidence: 4.2 正文明确'Rather than treating the extracted robot motion as a reliable reference'，关键帧构型由物体信息优化后作为锚点插值修正重定向轨迹；附录 A.2.2 进一步说明接触帧位姿'carries perception, reconstruction, and retargeting error'故需几何校正+抓取搜索。
- Quote: “The refinement module aims to improve the retargeted robot trajectory. In this work, we propose an object-centric keyframe refinement method. Rather than learning to refine the trajectory directly, our method identifies key manipulation frames and uses the object configurations at these frames to optimize the desired robot configurations. These optimized configurations then serve as anchor points for interpolating and correcting the retargeted trajectory.”
- Authors: yunhai-han; jianuo-qiu; linhao-bai; et al.

### EA-EGOPREC-2026-0419

- Claim: 解耦 sim-to-real 策略（IL 从点云蒸馏关键帧手部姿态处理几何误差 + 残差 RL 做手指级物理适应）在真实世界物体位姿扰动下取得 95.7% 平均成功率；而依赖预训练 6D 位姿估计（FoundationPose）直接校正机器人姿态的路线仅 15.7%——部署时策略蒸馏比信赖检测/位姿估计模型的精度更鲁棒。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08828](https://arxiv.org/abs/2606.08828) Video2Sim2Real: Full-Stack Autonomous Dexterous Skill Acquisition from a Single Human Video
- Locator: 5.3 Evaluation of Sim-to-Real Transfer
- Evidence: Table 2：FoundationPose 0/10,0/10,1/10,0/10,0/10,0/10,10/10（15.7%）vs Ours 10/10,9/10,10/10,8/10,10/10,10/10,10/10（95.7%），两法共用同一手指残差 RL 策略；附录 E.5 Table 11 补充 Pure-IL 5.7%、Pure-RL(finger) 45.7%、Pure-RL(arm+finger) 3.0%。
- Quote: “Table 2: Real-world task success rate under object pose variations. Method Apple Peach Steak Toy Tissue Book Tray Avg. FoundationPose 0/10 0/10 1/10 0/10 0/10 0/10 10/10 15.7% Ours 10/10 9/10 10/10 8/10 10/10 10/10 10/10 95.7%”
- Authors: yunhai-han; jianuo-qiu; linhao-bai; et al.

### EA-EGOPREC-2026-0026

- Claim: 以腕+五指尖六关键点为统一观测-动作表征，Dexterous Point Policy 仅用人类视频训练（零机器人示教）即在 8 个真机灵巧任务上达 75.0% 平均成功率，远高于同样仅用人类数据的 Point Policy（3.7%）与 VITRA（1.0%）；去掉互联网规模预训练降至 67.5%（Pick and Place），去掉自回归降至 37.5%。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.10614](https://arxiv.org/abs/2606.10614) Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations
- Locator: 4.1 Experimental Setup, Table 1 (Dexterous manipulation results; float 在抽取文本中位于 4.1 标题之下)
- Evidence: Table 1 给出 8 任务逐任务成功率与三方法对比；Table 3 给出 w/o AR（37.5%）与 w/o Pretrain（67.5%）消融；所有方法共享人类演示数据与（对 VITRA）同一 IK 管线。
- Quote: “Method Bottle Box Ball Towel Teddy Open Brush Spray Avg. Point Policy 0.0 0.0 4.2 12.5 4.2 8.4 0.0 0.0 3.7 VITRA 0.0 0.0 0.0 4.2 0.0 4.2 0.0 0.0 1.0 DPP (Ours) 95.8 75.0 70.8 87.5 79.2 87.5 62.5 41.7 75.0”
- Authors: beomjun-kim; seong-hyeon-park; seunghoon-sim; et al.

### EA-EGOPREC-2026-0091

- Claim: 手部轨迹重建环节的检测层误差来源被作者明确识别为三类：(i) 单帧 WiLoR 预测对噪声与遮挡敏感；(ii) 严格双目三角化在任一视图缺检时失败；(iii) 现有基础手部重建器不能准确估计全局腕部变换。对应的缓解设计是：不直接使用 WiLoR 全局根，而把重建的 MANO 关节重投影到两个像平面做 DLT 三角化获得标定世界系下的米制 3D 腕部位置、旋转平均融合双视图朝向；对缺失帧做平移线性插值与旋转球面插值；再在 SE(3) 李群上以 IEKF-RTS 平滑器（过程噪声 Q=1e-5 I6、量测噪声 R=1e-2 I6，首尾有效位姿固定为锚）抑制逐帧噪声与高频抖动，得到时间一致的腕部轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.10743](https://arxiv.org/abs/2606.10743) Hand-centric Human-to-Robot Trajectory Transfer from Video Demonstrations via Open-World Contact Localization
- Locator: 3.1 Hand Trajectory Reconstruction; Appendix A Robust hand motion recovery; References
- Evidence: 3.1 陈述 WiLoR 单帧噪声/遮挡敏感与双目三角化缺检失败，并给出插值+IEKF-RTS 平滑方案；Appendix A 进一步声明基础重建器全局腕部变换不准、改用 MANO 关节 DLT 三角化，并给出 Q/R 协方差与首尾锚定细节。
- Quote: “Since single-frame WiLoR predictions are sensitive to noise and occlusions [4], and strict stereo triangulation fails when either view lacks a valid detection, we complete missing frames by temporal interpolation and further refine the wrist trajectory using an SE(3) Iterative Extended Kalman Filter with a Rauch–Tung–Striebel smoother (IEKF–RTS) [46].”
- Authors: yitian-shi; di-wen; zhengqi-han; et al.

### EA-EGOPREC-2026-0092

- Claim: 重定向的传播路径：接触建立后采用刚体耦合假设，腕部相对抓取变换在同一段内保持恒定（g_t = T_w(t) T_w(s_k)^{-1} g_0），因此腕部轨迹的残余误差会被原样传导为平行夹爪末端轨迹误差；作者明确承认 3.1 的手部位姿估计仍含残余漂移、经分段抓取传播后会被放大，且抓取传播会因手部位姿估计误差引入小的 onset 错位。缓解手段是 LTE 接触对齐细化：从 HOGraspFlow 抓取条件接触图与 DA3 首帧双目点云估计平移校正量，只编辑抓取起始控制位姿、固定段终点，在不改变示教运动趋势的前提下改善接触对齐，并借同一 LTE 机制做碰撞感知增广（间隙半径 0.05 m、N_max=30）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.10743](https://arxiv.org/abs/2606.10743) Hand-centric Human-to-Robot Trajectory Transfer from Video Demonstrations via Open-World Contact Localization
- Locator: 3.3 Cross-Embodiment Trajectory Retargeting; Appendix D Trajectory refinement and augmentation; References
- Evidence: 3.3 给出刚体耦合传播方程与 onset 错位陈述及 LTE 细化方案；Appendix D 补充'手部位姿估计残余漂移经分段抓取传播被放大'与 LTE 目标函数（四项：拉普拉斯形状保持、起始位姿校正、终点固定、轨迹贴近）及碰撞拒绝参数。
- Quote: “Since grasp propagation may introduce small onset misalignments due to hand pose estimation errors, we apply Laplacian Trajectory Editing (LTE) [45] to the propagated segment-wise PJ trajectories for contact-aware refinement.”
- Authors: yitian-shi; di-wen; zhengqi-han; et al.

### EA-EGOPREC-2026-0093

- Claim: 下游可用性量化与失败归因：HOWTransfer 真机回放总体成功率 86%，比共享同一接触段的模板抓取基线高 23 个百分点（water 92% vs 30%、disassemble 78% vs 0%）；长时程任务（Pot Cooking、Breakfast）因多接触转移与累积执行误差成功率下降。失败分析进一步将大多数失败归因于手部重定向或轨迹增广误差在物理执行中累积：擦拭类任务失败主要因轨迹略低或抓取过深导致与白板碰撞；工具/受约束物体任务对抓取朝向与功能对齐敏感，不准确的刀具/锅铲/盖子抓取会使被操作物撞上目标或周围结构；倾倒类失败源于杯/壶口方向未对准目标。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.10743](https://arxiv.org/abs/2606.10743) Hand-centric Human-to-Robot Trajectory Transfer from Video Demonstrations via Open-World Contact Localization
- Locator: 4.2 Trajectory Reconstruction Quality; Appendix G Failure analysis; References
- Evidence: 4.2 报告 86% 总体回放成功率与 23pp 差距及 per-task 对照；Appendix G 给出失败模式的任务分类归因；模板基线与本文共享接触段，隔离抓取重定向贡献。
- Quote: “HOWTransfer achieves an overall replay success rate of 86%, outperforming the template-based baseline by 23 percentage points. The gains are especially clear on tasks requiring task-specific grasp selection and contact alignment, such as water (92% vs. 30%) and disassemble (78% vs. 0%).”
- Authors: yitian-shi; di-wen; zhengqi-han; et al.

### EA-EGOPREC-2026-0094

- Claim: 接触时序定位精度是抓取重定向时间锚的上游质量瓶颈：在 110 视频基准上本文方法总体 MAE 11.787 帧、SR(3)=0.491、SR(10)=0.736、IoU=0.816，远优于 EgoLoc（MAE 27.264、SR(3)=0.075）与拇指-食指闭合阈值基线（SR(3)=0.364）；作者明确判定拇指-食指闭合是真实接触的不可靠代理（高 MoF=0.784 但 Precision 仅 0.508、IoU 仅 0.465），且接触段正是 PJ 抓取初始化与轨迹传播的时间锚（onset 帧作抓取重定向关键帧）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.10743](https://arxiv.org/abs/2606.10743) Hand-centric Human-to-Robot Trajectory Transfer from Video Demonstrations via Open-World Contact Localization
- Locator: 4 Experiments, Table 1; 4.1 Temporal Contact Localization
- Evidence: Table 1 报告四方法八指标总体接触定位结果；4.1 正文给出拇指-食指闭合不可靠与 EgoLoc 不适合非 ego 多阶段设置的判定；3.3 明确 onset 帧作为抓取重定向关键帧。
- Quote: “Threshold 0.364 0.423 0.508 30.195 0.784 0.465 0.508 0.584 EgoLoc 0.075 0.127 0.207 27.264 0.456 0.382 0.653 0.495 Ours (w/o DA3) 0.495 0.579 0.687 11.805 0.790 0.766 0.963 0.851 Ours 0.491 0.581 0.736 11.787 0.872 0.816 0.932 0.891”
- Authors: yitian-shi; di-wen; zhengqi-han; et al.

### EA-EGOPREC-2026-0088

- Claim: EgoEngine 在真机 Aria 任务的动作优化中显式把 ego 视频估计的参考信号视为含噪并给出具体容差：因物体轨迹取自第一视角视频（含重建、追踪与标定误差）而非仿真真值，优化采用放宽的物体轨迹可行阈值（位置 0.08 m、旋转 2.5 rad）以避免过拟合噪声参考，同时将 human-mimic 关节奖励权重设为 0.0，避免被含噪的重定向手指运动过度约束。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.12604](https://arxiv.org/abs/2606.12604) EgoEngine: From Egocentric Human Videos to High-Fidelity Dexterous Robot Demonstrations
- Locator: Appendix
- Evidence: 附录 C.2 说明 Aria 真机任务的物体轨迹来自 ego 视频、含重建/追踪/标定误差，因此采用放宽阈值（位置 0.08 m、旋转 2.5 rad）防止过拟合噪声参考；同段给出关节奖励权重 0.0 以避免过度约束含噪重定向手指运动。
- Quote: “we use looser feasibility thresholds, including an object position thresh- old of 0.08 m and an object rotation threshold of 2.5 rad, so that the optimizer can tolerate imperfect object-trajectory estimates instead of overfitting to noisy references”
- Authors: yangcen-liu; shuo-cheng; xi-yin; et al.

### EA-EGOPREC-2026-0398

- Claim: 在同一 sensorimotor 策略下，闭环重查询意图的 LUCID 在三个 web 监督真实任务上平均成功率 73%，显著高于开环视频生成 planner 的 28%；开环在执行偏离（如 misgrasp 后勺子移位）时因陈旧参考使策略混乱失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.11628](https://arxiv.org/abs/2606.11628) LUCID: Learning Embodiment-Agnostic Intent Models from Unstructured Human Videos for Scalable Dexterous Robot Skill Acquisition
- Locator: 1 Introduction
- Evidence: 1 Introduction 报告 73% vs 28%；4.1 描述开环基线在 misgrasp 后陈旧参考导致策略混乱，LUCID 在抓取偏差或物体移位时重查询场景并重定向策略。
- Quote: “Closed-loop LUCID achieves 73% average success on the web-supervised tasks vs 28% for an open-loop baseline, and the same intent model drives both embodiments with comparable success (63%) on the smartphone-collected tasks.”
- Authors: harsh-gupta; guanya-shi; wenzhen-yuan

### EA-EGOPREC-2026-0499

- Claim: 该框架的作者基于实验观察指出：可穿戴手部接口对手部尺寸与佩戴对齐高度敏感——即使微小差异也会在估计的手部运动学中产生可察觉误差并直接影响遥操作精度；当机械/传感设计无法实现手型不变性时，必须引入显式标定或自适应追踪（其实践为被试特异性标定，对齐外骨骼关节空间与解剖手部构型）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.15434](https://arxiv.org/abs/2606.15434) A Bilateral Teleoperation Framework for Dexterous Manipulation
- Locator: A. Hand Morphology and Donning Effects
- Evidence: IV.A 逐字给出佩戴敏感→系统误差→精度影响的因果陈述，与因佩戴敏感而采用定制标定程序的工程回应。
- Quote: “In our experiments, even minor variations in hand size or device alignment produced noticeable errors in estimated hand kinematics, directly affecting teleoperation precision. When hand-size invariance cannot be achieved through mechanical or sensing design alone, explicit calibration or adaptive tracking becomes necessary. Because the kinematic mapping of the Maestro exoskeleton is sensitive to donning conditions, we therefore employ a custom calibration proce- dure to align the sensed exoskele”
- Authors: stefano-dalla-gasperina; dong-ho-kang; haiyun-zhang; et al.

### EA-EGOPREC-2026-0500

- Claim: 该框架的作者明确枚举遥操作的残余误差来源为四项：不完善的手部追踪、重定向不准、延迟与人差异，并承认即使仔细的系统设计也无法完全消除这些误差、其对操作者形成持续认知负担；其经验是共享控制（任务相关约束增强操作者指令）可在无需全自主的前提下显著缓解残余人误，同时保留操作者意图。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.15434](https://arxiv.org/abs/2606.15434) A Bilateral Teleoperation Framework for Dexterous Manipulation
- Locator: D. Shared Control for Human Error Mitigation
- Evidence: IV.D 首两句逐字给出四元误差枚举与不可消除性承认，随后给出共享控制缓解的关键经验。
- Quote: “Teleoperation inevitably involves residual errors arising from imperfect hand tracking, retargeting inaccuracies, latency, and human variability. Our experiments confirmed that even with careful system design, these errors cannot be fully elimi- nated and place a continuous cognitive burden on the operator. A key lesson learned is that shared control can meaningfully mitigate residual human error without requiring full autonomy.”
- Authors: stefano-dalla-gasperina; dong-ho-kang; haiyun-zhang; et al.

### EA-EGOPREC-2026-0338

- Claim: 单目 2D 观察固有的深度歧义与遮挡使独立的手部/物体估计器频繁产生空间不一致，表现为物体穿插或不真实悬空等物理不可行交互，并会直接损害下游策略训练。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: 1 Introduction
- Evidence: 引言陈述该机制并以 [12,13,14]（手物估计器）与 [15]（ContactOpt）支撑；相关工作节再次引用 [37,38,39] 重申独立估计导致空间差异与穿插。
- Quote: “Independent hand and object estimators [12, 13, 14] frequently suffer from spatial inconsistencies, primarily due to the inherent depth am- biguity and occlusion in 2D observations. These perceptual inaccuracies lead to physically im- plausible interactions such as interpenetration or unrealistic hovering [15], which are detrimental to downstream policy training.”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0339

- Claim: 对单目逐帧深度/内参估计的时序不一致，管线取全局平均内参 K̄ 为规范内参，并对每帧深度图做重映射 D_cor(u)=D(u)·‖K̄⁻¹u‖/‖K_t⁻¹u‖，以强制整段序列的空间一致性，再用校正深度把物体分割反投影为 3D 坐标。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: 3.1 Unified Perception and Object Reconstruction
- Evidence: 3.1 节给出规范内参与深度重映射公式及其目的（空间一致性）。
- Quote: “To mitigate temporal inconsistencies inherent in per-frame intrinsic estimation, we establish a canonical intrinsic matrix by computing the global average, ¯ K = 1 N P N i=1 K i . The depth maps are then refined through a remapping operation, D cor t (u) = D t (u) · ∥ ¯ K −1 u∥ 2 ∥K −1 t u∥ 2 , which en- sures spatial consistency across the sequence.”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0340

- Claim: 绝对尺度恢复不追求完美度量精度：点云聚类去离群后以物体最长轴为目标尺度 s，SAM3D 网格按 s 缩放得到度量一致的数字孪生；作者明确声明深度有偏时系统仍能在缩放虚拟空间中追踪轨迹，保留内部运动结构与物理可行性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: K. To ensure the fidelity of the reconstructed
- Evidence: 该段（html-flat 从 3.1 断出的续段）给出尺度 s 定义、SAM3D 缩放与'不严格依赖度量精度'的原话声明。
- Quote: “To ensure the fidelity of the reconstructed point clouds, spatial clustering is applied to filter out outliers, from which the absolute physical di- mensions are estimated. Specifically, the length of the object’s longest axis is defined as the target scale s. To recover the complete geometry, we employ SAM3D [66] to generate a coherent mesh from monocular views, which is then uniformly scaled to match s, yielding a metric-consistent digital twin M obj . Notably, while the estimation of absolut”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0341

- Claim: 检测器选型针对失败模式互补：物体侧 FoundationPose 在严重遮挡或快速运动下常出现追踪漂移与位姿跳变（内部打分不可靠），故引入 SpatialTracker 的像素级时序对应来正则化并稳定轨迹；手部侧用鲁棒追踪器回归 MANO 形状 β 与姿态 θ，并恢复腕部全局旋转与平移作为运动学先验。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: 3.2 Pose estimation and Optimization
- Evidence: 3.2 Object-Hand Tracking 小节分别描述 FoundationPose 的失败模式、SpatialTracker 的补偿作用与 MANO 手部状态 τ_h=(θ,β,R_h,t_h) 的构成。
- Quote: “However, under severe oc- clusions or rapid motions, FoundationPose often suffers from tracking drift and abrupt pose jumps due to unreliable internal scoring metrics. To mitigate these tracking failures, our system incorpo- rates SpatialTracker [67] to extract robust, pixel-level temporal correspondences, which regularize and stabilize the trajectory estimation, where a more comprehensive architectural description can be found in Appendix A.2. To capture the hand’s kinematic state, we employ a”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0342

- Claim: 在 TACO ego-centric 视频上，融合 2D+3D 追踪与细化的管线达到 CD 1.447cm、ADD-S 80.52%、失败率 7.27%、SI 0.535，全面优于 FoundationPose（1.685cm/76.98%/10.52%/0.529）与 SpatialTracker（1.829cm/63.65%/28.45%/0.532）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: 4.1 Object Pose Estimation
- Evidence: 4.1 节正文与 Table 1 完整给出三种方法六个指标；正文另述定性结论（FoundationPose 重度遮挡下频繁跟丢）。
- Quote: “Table 1: Performance Comparison on the TACO Dataset Pose Accuracy Robustness Temporal Smoothness Method CD (cm) ↓ ADD-S (%) ↑ FR (%) ↓ RTE (cm) ↓ RRE (rad) ↓ SI ↑ FoundationPose 1.685 76.98 10.52 0.926 0.052 0.529 SpatialTracker 1.829 63.65 28.45 0.765 0.085 0.532 Ours 1.447 80.52 7.27 0.897 0.053 0.535”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0343

- Claim: 几何/物理两阶段细化对策略可用性呈剂量效应：去除几何约束 C1 后 8 个任务成功率全部归零（多数任务无法初始化）；去除物理约束 C2 后平均成功率 54.4%；完整管线 79.3%。高精度任务对物理约束最敏感（锤击 7%→51%，用牙刷 14%→33%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: 4.3 Ablation Study
- Evidence: Table 3 给出 8 任务×4 条件的逐格成功率与平均行；4.3 正文解释 C1 建立手物协调的空间基础（缺则多数任务无法初始化）、C2 对高精度场景必不可少。
- Quote: “As shown in Table 3, the baseline models lacking these constraints exhibit significant performance degradation. The results indicate that C 1 establishes the necessary spatial foundation for hand-object coordination, without which most tasks fail to initialize. Furthermore, the inclusion of C 2 is essential for refining complex interactions, particularly in high-precision scenarios. The full V2P framework consistently achieves the highest average success rate (79.3%) on XHand, validating that”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0345

- Claim: OakInk 策略学习上，本文方法 SR 0.483、右手相对平移误差 0.00647m，优于 ManipTrans 的 0.417 与 0.00869m；相对旋转误差 0.182rad vs 0.197rad（右手）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: 4.2 Policy Learning Evaluation
- Evidence: Table 2 给出两方法在 SR/E_rR/E_rT/E_lR/E_lT 五项指标上的数值；4.2 正文称本文在多数关键指标上持续优于基线。
- Quote: “Table 2: Quantitative Evaluation on the OakInk Benchmark. E R and E T denote relative rotation and translation errors, where subscripts r and l represent the right and left hands, respectively. Method SR ↑ E rR (rad) ↓ E rT (m) ↓ E lR (rad) ↓ E lT (m) ↓ ManipTrans 0.417 0.197 0.00869 0.277 0.0139 Ours 0.483 0.182 0.00647 0.283 0.0117”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0393

- Claim: 在噪声重建的人-物参考轨迹上，dynamics-aware 重定向基线（SPIDER 式退火采样）成功率仅 25%，加入 warmup steps、随机力扰动与 transition reward 三项针对噪声的组件后升至 71%；同一管线在干净 MoCap 参考（OakInk2）上从 72% 升至 81%，即重建噪声使重定向成功率比干净参考低约 10 个百分点。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.19333](https://arxiv.org/abs/2606.19333) Do as I Do: Dexterous Manipulation Data from Everyday Human Videos
- Locator: Table 3: Retargeting Results; 4.3 Retargeting Results
- Evidence: Table 3 在 655 条重建参考上报告 Annealed Sampling 0.25 → +Warmup 0.66 → +Perturbation 0.67 → +Transition Reward 0.71；OakInk2 上 0.72 → 0.81。正文 4.3 明确 warmup 是主贡献（发现比噪声首帧更稳定的初态）。
- Quote: “On our reconstructed in-the-wild data, DO AS I DO reaches a 71% success rate, significantly improving over the baseline of 25%. The main differentiator is warmup, which discovers initial states that are much more stable and natural than the noisy initial frame, thereby leading to successful tracking in subsequent timesteps.”
- Authors: bhawna-paliwal; haritheja-etukuru; william-liang; et al.

### EA-EGOPREC-2026-0035

- Claim: 在 ContactPose 25 个抓取上，TopoRetarget 取得最低接触精度误差 7.71 mm 与接触对齐误差 15.67°，最大穿透 1.07 mm，平均求解低于 5 ms/帧；作者将残差归因于人手-灵巧手形态差距与源侧 ContactPose 穿透。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16272](https://arxiv.org/abs/2606.16272) TopoRetarget: Interaction-Preserving Retargeting for Dexterous Manipulation
- Locator: 5.1 Interaction-Preserving Retargeting Quality
- Evidence: 5.1 节报告 Table 1 结果：接触精度/对齐/穿透全面优于 OmniRetarget、Mink、DexPilot、GeoRT，并说明残差来源包括源侧 ContactPose 穿透。
- Quote: “Table 1 shows that TopoRetarget achieves the lowest contact precision and contact alignment er- rors, with 7.71 mm and 15.67 ◦ , respectively. The residual is attributable to the human-dexterous embodiment gap and source-side ContactPose interpenetration. TopoRetarget also keeps penetra- tion small, with a maximum penetration of 1.07 mm, and avoids the severe interpenetration observed in several baselines, indicating that the method better preserves local contact geometry. Moreover, the average”
- Authors: jielin-wu; shenzhe-yao; guanqi-he; et al.

### EA-EGOPREC-2026-0036

- Claim: 在相同 PPO 设置下，TopoRetarget 生成的参考使下游 RL 跟踪策略在 MoCap Pen-Spin 数据集上取得 87.5% (28/32) 成功率，比所有基线高 40 个百分点以上（最优基线 46.9%），Ho-cap 上 84.4% 对最优基线 75.0%。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16272](https://arxiv.org/abs/2606.16272) TopoRetarget: Interaction-Preserving Retargeting for Dexterous Manipulation
- Locator: 5.2 Downstream Tracking Policy Performance
- Evidence: 5.2 节与 Table 2 报告：Pen-Spin 上 TopoRetarget 87.5% 对 OmniRetarget 46.9%、Mink 21.9%、DexPilot 40.6%、GeoRT 31.2%，且位置/旋转误差最低；作者指出快速运动与频繁非指尖接触转换要求高质量参考。
- Quote: “As shown in Table 2, TopoRetarget achieves the highest success rate at 84.4% and the lowest po- sition error at 0.87 cm on the Ho-cap Dataset, while rotation errors remain comparable across meth- ods because the trajectories are primarily grasp-centric. On the MoCap Pen-Spin Dataset, rapid motion and frequent non-tip contact transitions demand high-quality reference motion; TopoRetar- get reaches 87.5% success, over 40 percentage points above all baselines, with the lowest position and rotation”
- Authors: jielin-wu; shenzhe-yao; guanqi-he; et al.

### EA-EGOPREC-2026-0448

- Claim: 对 timing-sensitive 任务，HumanoidUMI 遵循 UMI 的延迟匹配协议校准并补偿腕视观测、夹爪状态、高层策略推理与机器人控制之间的相对延迟；动态投球消融显示去除延迟匹配会使性能下降，说明传感-控制同步精度是动态任务中独立于空间追踪精度的轨迹可用性决定因素。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.27239](https://arxiv.org/abs/2606.27239) HumanoidUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: A. Robot-free Data Collection System; A. Effectiveness of the robot-free data collection and train-
- Evidence: III-A 'Latency matching' 段声明沿用 UMI[9] 协议校准补偿；IV-A 报告动态投球任务对释放时机高度敏感、去除延迟匹配的消融性能下降（Fig. 6 柱状图，20 次试验/变体，文本无数值）。
- Quote: “For timing-sensitive tasks, we follow the latency-matching procedure of UMI [9] to calibrate and compensate for the relative delays among wrist-view observations, gripper-state measurements, high-level policy inference, and robot control.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### EA-EGOPREC-2026-0096

- Claim: 作者明确把手部估计噪声识别为人类数据迁移的核心误差来源：人类动作通常由手部姿态估计器提取，即使经参数化约束或重定向，提取的动作仍不可避免地带噪；其中腕部旋转因预测器误差尤其不可靠，且手指与平行夹爪接触模式的本质差异使腕部旋转与操作语义解耦；直接把提取的人类 6DoF 腕部动作回放到机器人经常产生扭曲行为。据此作者提出动作空间降维的缓解手段：只共享头相机系下的相对腕部平移（translation-only bridging action），该表示被声称对带噪旋转估计鲁棒、构造上本体无关。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.28133](https://arxiv.org/abs/2606.28133) Translation as a Bridging Action: Transferring Manipulation Skills from Humans to Robots
- Locator: 4.1 Motion Bridging Action Representation; 1 Introduction
- Evidence: 1 Introduction 给出'提取动作不可避免地带噪'的总述；4.1 列出两条 sub-optimal 理由（旋转噪声、接触模式解耦）与直接回放扭曲的经验观察，并给出 bridging action 定义与其鲁棒/本体无关的三条性质。
- Quote: “we argue this is sub-optimal: 1) the wrist rotations for human data are noisy due to predictor errors [54], and 2) the distinct contact patterns between fingers and parallel grippers decouple wrist rotation from the semantic manipulation behavior. Empirically, we find that directly replaying the extracted human 6DoF wrist actions on robots often leads to distorted behaviors.”
- Authors: sijin-chen; kaixuan-jiang; haixin-shi; et al.

### EA-EGOPREC-2026-0097

- Claim: 检测噪声对迁移的下游量化对照：从头共训时，用 6DoF 人类腕部动作（含带噪旋转）总体成功率仅 12.50%、平均进度 34.67%，而用 translation-only bridging 动作达 22.50% 与 44.58%；定性上 6DoF 共训使机器人产生扭曲、偏离目标的腕部位姿，bridging 动作产生与微波炉把手自然对齐的位姿。两组模型共享架构、数据与训练量，唯一变量是人类动作表示。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.28133](https://arxiv.org/abs/2606.28133) Translation as a Bridging Action: Transferring Manipulation Skills from Humans to Robots
- Locator: 5.3 Why translation-only instead of 6DoF human wrist actions?, Table 2
- Evidence: 5.3 正文报告 6DoF 共训导致 noisy and twisted behaviors、bridging 共训更稳定；Tab.2 报告两种人类动作表示在四任务组与总体的进度/成功率（12.50% vs 22.50% overall success）。
- Quote: “25.00 4.17 55.00 31.25 28.13 0.00 49.17 33.33 34.67 12.50 a 3D-wrist 38.02 25.00 49.06 31.25 48.13 3.13 50.00 37.50 44.58 22.50”
- Authors: sijin-chen; kaixuan-jiang; haixin-shi; et al.

### EA-EGOPREC-2026-0098

- Claim: 上界实验提供了动作噪声代价的间接量化：把任务机器人示教（100 轨迹/任务）按人类目标转成 translation-only 动作——此时无观测 gap 且动作噪声远低——总体成功率 55.83%、进度 73.54%，显著高于默认人类数据共训的 38.33%/59.75%；作者据此判断迁移效率随视觉 gap 与动作噪声的减小而提升，bridging 表示本身是有效的迁移媒介。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.28133](https://arxiv.org/abs/2606.28133) Translation as a Bridging Action: Transferring Manipulation Skills from Humans to Robots
- Locator: 5.8 The upper bound of the bridging objective, Table 5
- Evidence: 5.8 描述上界实验设计（机器人数据伪装人类数据，no observation gap and far less action noise）；Tab.5 报告 Default 38.33% vs Upper Bound 55.83% 总体成功率；正文据此判断迁移效率随 gap 与噪声减小而提升。
- Quote: “Default (Ours) 64.58 45.83 56.88 43.75 52.50 15.63 61.67 50.00 59.75 38.33 Upper Bound 68.75 54.17 75.94 62.50 81.25 53.13 71.25 58.33 73.54 55.83”
- Authors: sijin-chen; kaixuan-jiang; haixin-shi; et al.

### EA-EGOPREC-2026-0111

- Claim: 单视角人类演示的感知误差具有结构性：手部关键点与物体位姿会抖动、漂移，并在接触时刻被遮挡——作者逐字指出 'The demonstrated reference is therefore inaccurate exactly where it matters most'（演示参考恰恰在最要紧处不准）；该感知问题与逐路点 IK 可行性问题耦合，必须联合求解。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.09519](https://arxiv.org/abs/2607.09519) DemoBridge: A Simulation-in-the-Loop Toolkit for Single-View Human Demonstration Retargeting
- Locator: I. INTRODUCTION
- Evidence: I. INTRODUCTION 逐字给出两类耦合困难（运动学、感知）与 'jitter, drift, and are occluded at the moment of contact' 的误差源刻画；属问题框定型主张，无量化分解，按作者主张收录。
- Quote: “The second is perceptual. From a single view, hand keypoints and object poses jitter, drift, and are occluded at the moment of contact. The demonstrated reference is therefore inaccurate exactly where it matters most.”
- Authors: zehao-wang; fabien-despinoy; sergey-zakharov; et al.

### EA-EGOPREC-2026-0112

- Claim: 单视角 2D 手部关键点经深度图提升为 3D 时，凡被操作物体前景遮挡手部的位置，深度错误导致提升关节同步出错（'the depth is wrong, and so is the lifted joint'）；缓解手段为：遮挡间隙插值+中值滤波去毛刺+Savitzky-Golay 平滑的噪声滤波链，再以 MANO 手模型拟合关键点并从摆好姿态的网格重读解剖一致的关节（含指尖），接触事件则从手-物运动共现（同动才判持物）读出。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.09519](https://arxiv.org/abs/2607.09519) DemoBridge: A Simulation-in-the-Loop Toolkit for Single-View Human Demonstration Retargeting
- Locator: A. Event extraction
- Evidence: V-A Event extraction 逐字描述噪声滤波三件套（插值/中值/SG）、深度提升在前景遮挡处出错的机制、MANO 拟合重读与运动共现接触判定；IV. DESIGN CHOICES 补充手部后端（MediaPipe/HaMeR）与 2D→米制 3D 提升路径。
- Quote: “noise filter: occlusion gaps are interpolated, spikes are removed with a median filter, and the hand keypoints and wrist pose are smoothed (Savitzky–Golay filter [15]). Single-view keypoints are lifted to 3D through the depth map. Wherever the manipulated object foreground- occludes the hand, the depth is wrong, and so is the lifted joint. We denoise these by fitting a MANO hand model to the keypoints and re-reading clean, anatomically consistent joints (fingertips included) from the posed mesh.”
- Authors: zehao-wang; fabien-despinoy; sergey-zakharov; et al.

### EA-EGOPREC-2026-0113

- Claim: 单视角参考位姿仅精确到数毫米（'accurate only to a few millimeters'）；当物体接近夹爪开口宽度时，该偏移足以漏抓——可接受阈值因此由任务几何（物体宽 vs 夹爪开口）决定而非固定数值。全管线在三个真实演示任务上 place 阶段成功 6/10（mug-on-plate）、7/10（cup-stack）、7/10（pour-milk），grasp 8-9/10；人工补给 grasp timing 的重实现基线 YOTO†/RoboWheel† 大多止步于 grasp 之前（place 0-2/10），且一旦 grasp 成功，transport 从未失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.09519](https://arxiv.org/abs/2607.09519) DemoBridge: A Simulation-in-the-Loop Toolkit for Single-View Human Demonstration Retargeting
- Locator: B. Real demonstrations
- Evidence: VI-B-d 逐字给出 'few millimeters' 与 'nearly as wide as the gripper opening, that offset is enough to miss the grasp' 的阈值论断及 'Transport never fails once a rollout has grasped' 的观察；Table II 给出三任务四阶段累积成功率（Ours place 6-7/10，基线 0-2/10）。
- Quote: “Grasp timing is necessary but far from sufficient. We supply the baselines with the grasp timing they cannot reliably extract, yet both clear only the reach stage and rarely grasp. The reference pose is the deeper problem. From a single view it is accurate only to a few millimeters.”
- Authors: zehao-wang; fabien-despinoy; sergey-zakharov; et al.

### EA-EGOPREC-2026-0482

- Claim: 在同一 NOKOV 动捕追踪接口与相同硬件下，TELEDEXTER 在 7 个灵巧任务上达 75.2% 平均 SR / 87.1% 平均 TP，而纯运动学重定向基线（DexRT 5.7/37.6、GeoRT 0.0/28.5）与生成式先验基线（DexGen 0.0/25.0）近乎全败，失败集中于首个接触密集的 in-hand 重定向/手指步态阶段。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.11481](https://arxiv.org/abs/2607.11481) Towards Human-level Dexterous Teleoperation
- Locator: 4.2 Dexterous Teleoperation Evaluation, Tab. 1
- Evidence: 4.2 正文给出 75.2/87.1 与基线近乎全败的对比；Tab. 1 逐格列出各方法 SR/TP；阶段分析指出基线在首个接触密集阶段崩溃。
- Quote: “As shown in Tab. 1, TELEDEXTER achieves 75.2% average SR and 87.1% average TP across all seven tasks, while all baselines near-uniformly fail. On the reorienta- tion tasks, TELEDEXTER achieves 66.7–80.0% SR by executing dynamic in-hand reorientation through learned contact strategies. In contrast, kinematic retargeting methods (DexRT, GeoRT) rarely progress beyond the initial pick-up stage, as they lack the dynamics prior needed for contact- rich in-hand manipulation.”
- Authors: puhao-li; zeyuan-chen; yingying-wu; et al.

### EA-EGOPREC-2026-0484

- Claim: TELEDEXTER 训练时向观测注入指尖位置 ±5mm、物体位置 ±5mm、物体姿态 ±2° 的均匀噪声与 2 帧观测延迟队列（采样概率 0.5），并随机化关节位置高斯噪声 σ=0.1；在此噪声预算下训练的控制器零样本迁移到真实遥操作，给出了一组可复现的『追踪/感知噪声可接受阈值』参考值。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.11481](https://arxiv.org/abs/2607.11481) Towards Human-level Dexterous Teleoperation
- Locator: References (Appendix C.7 Domain Randomization, Tab. 9)
- Evidence: 附录 Tab. 9 逐项列出 sensing noise 与 observation latency 的随机化范围；C.7 说明其目的是容忍 sim-to-real 感知差距。
- Quote: “Sensing noise joint position q t additive Gaussian σ = 0.1 fingertip position additive uniform ±5 mm object position additive uniform ±5 mm object orientation additive uniform ±2 ◦ Observation latency queue size constant 2 frames queue sampling probability constant 0.5”
- Authors: puhao-li; zeyuan-chen; yingying-wu; et al.

### EA-EGOPREC-2026-0485

- Claim: 即使在动捕采集端，TELEDEXTER 的几何感知重定向仍需引入 Curobo 时序平滑能量项（对关节速度/加速度/加加速度惩罚）来抑制采集抖动（capture jitter），说明采集噪声沿参考轨迹传导、必须在重定向阶段显式压制。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.11481](https://arxiv.org/abs/2607.11481) Towards Human-level Dexterous Teleoperation
- Locator: 3.2 Hand-Object Reference Motion Construction
- Evidence: 3.2 末段逐字说明 L_smooth 采用 Curobo 时序平滑能量以抑制 capture jitter；C.5 给出该能量项的构成（速度 log-cosh + 加速度/加加速度 ℓ2）。
- Quote: “L smooth applies the Curobo [40] temporal smoothness energy on q 1:T to suppress capture jitter.”
- Authors: puhao-li; zeyuan-chen; yingying-wu; et al.

### EA-EGOPREC-2026-0520

- Claim: Open-AoE 在归档前执行三门质量检验：完整率门保留手部重建有效帧率足够高的片段，正确率门保留向 28-DoF 关节空间重定向时 IK 失败率保持低水平的片段（以保护下游可用性），一致性门保留相机轨迹平滑连续的片段，另加随机人工抽检剔除严重遮挡与极端光照边缘案例——数据验收标准被显式定义为下游重定向可用性的代理。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.14183](https://arxiv.org/abs/2607.14183) Open-AoE: An Open Egocentric Manipulation Dataset and Toolchain for Embodied Learning
- Locator: 4. Quality Inspection / 3.5 Quality Inspection & Data Delivery
- Evidence: 3.5 节逐句给出三门定义与人工抽检；'which preserves downstream usability'明确正确率门的设计动机是下游可用性。
- Quote: “The completeness gate retains Parts whose hand-reconstruction valid-frame ratio is high enough for reliable pose annotation; the correctness gate retains those whose inverse-kinematics failure rate stays low when retargeting to the 28-DoF joint space, which preserves downstream usability; and the consistency gate retains Parts with smooth, continuous camera trajectories free of abrupt jumps between adjacent frames.”
- Authors: zishuo-li; bowen-yang; changtao-miao; et al.

### EA-EGOPREC-2026-0521

- Claim: 在约 100 小时评测子集上，Open-AoE 的手部信号可用性为 98.93% 条目至少一只手有效、98.02% 条目双手均有效；bbox 100% 有效、98.39% 完全处于图像边界内、均值置信度 0.947；历史-未来训练窗口保留率达理论上限的 97.8%——消费级手机 ego 采集经其管线后可达到接近完备的手部信号覆盖。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.14183](https://arxiv.org/abs/2607.14183) Open-AoE: An Open Egocentric Manipulation Dataset and Toolchain for Embodied Learning
- Locator: 5.4. Training-Window Retention and Multimodal Completeness
- Evidence: 5.4 节与图 9：98.93%/98.02% 手部信号可用率、约 1,760 窗/小时（97.8% 上限）、bbox 100% 有效与 0.947 均值置信度，均基于发布的 validity 信息统计。
- Quote: “Open-AoE also exhibits substantially higher native hand-signal availability than OpenEgo, with 98.93% of evaluated entries containing at least one valid hand signal and 98.02% containing valid signals for both hands.”
- Authors: zishuo-li; bowen-yang; changtao-miao; et al.

### EA-EGOPREC-2026-0107

- Claim: 作者将 ego-centric 手部姿态预测的两类结构性误差源明确归因于：(1) 视野受限——头戴设备只覆盖主体前方有限区域，导致手部/物体外观截断等上下文线索不足，显著影响手-物交互理解与手部关键点预测；(2) 高动态——自由移动的 ego 相机叠加快速手部动作，产生高度动态背景与复杂的手-背景相对运动，使当前与未来手部运动模式难以准确捕捉。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.15890](https://arxiv.org/abs/2607.15890) Exo2EgoPose: Leveraging Exocentric Demonstrations for Vision-Language guided Egocentric 3D Hand Pose Forecasting
- Locator: 1 Introduction
- Evidence: Introduction 逐字给出两类挑战（limited field-of-view / highly dynamic motions）及其对手部关键点预测与运动模式捕捉的影响机制，Figure 1 亦以此立论；属问题框定型主张，无单独实验隔离，故按作者主张收录。
- Quote: “on the one hand, Ego videos are recorded by head-mounted devices and only cover limited regions in front of the subject, resulting in in- sufficient contextual cues like truncated hand or object appearances, which remarkably affect the understanding of hand-object interac- tion and prediction of hand keypoints. On the other hand, freely moving Ego cameras coupled with rapid hand maneuvers lead to highly dynamic backgrounds and complex hand-background rela- tive motions. Such dynamics make it dif”
- Authors: zhaofeng-shi; heqian-qiu; lanxiao-wang; et al.

### EA-EGOPREC-2026-0108

- Claim: 在 AssemblyHands val 上，完整 Exo2EgoPose 的 MPJPE/MPJVE 为 25.37/6.29mm；在移除 GLMM 但保留双层 Exo 重建监督的变体（30.11/7.76）基础上，完全移除 Exo 演示进一步劣化至 39.70/8.87mm——作者表述为 9.59 MPJPE 与 1.11 MPJVE 的严重劣化；视频级（VER）与分块帧级（CFER）Exo 重建各自再贡献约 2.83 与 3.11 MPJPE。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.15890](https://arxiv.org/abs/2607.15890) Exo2EgoPose: Leveraging Exocentric Demonstrations for Vision-Language guided Egocentric 3D Hand Pose Forecasting
- Locator: 4.3 Ablation Study
- Evidence: Table 2 八行消融给出全模型 25.37/6.29、无 GLMM 30.11/7.76、全去 Exo 39.70/8.87；正文逐字报告 +9.59/+1.11（相对第五行）与 +2.83/+3.11（VER/CFER）的劣化值。
- Quote: “Moreover, we completely remove Exo demonstrations in the last row, which causes severe degradation of 9.59 in MPJPE and 1.11 in MPJVE. It further em- phasizes the effectiveness of Exo demonstrations, which facilitate modeling complex spatial contexts and temporal dynamics.”
- Authors: zhaofeng-shi; heqian-qiu; lanxiao-wang; et al.

### EA-EGOPREC-2026-0110

- Claim: 作者将 ego 3D 手部姿态视为桥接人-机动作的自然显式统一表征，以预训练 Exo2EgoPose 为教师网络、向 GR-1 学生策略做中间表征蒸馏，并在 CALVIN 基准 ABC→D（训练于 A/B/C 场景、评测未见场景 D）零样本长时程设定下评测人-机迁移能力（Table 4，指标为 Avg.L 平均成功长度与 Avg.R 平均成功率）；摘要声明该迁移有效并在 CALVIN 上取得提升。全文核对的定量结果为 Avg.L 3.38、Avg.R 67.5%，超第二名 AR-VRM（3.29/65.9%）0.09 长度与 1.6% 成功率，但因抽取结构限制（见 verification）本卡仅作定性收录。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.15890](https://arxiv.org/abs/2607.15890) Exo2EgoPose: Leveraging Exocentric Demonstrations for Vision-Language guided Egocentric 3D Hand Pose Forecasting
- Locator: Abstract; 4.4 In-depth Analysis, Table 4 caption (Table 4 数值区在抽取文本中位于第二个 'Methods' 标题之下，因去重不可定位)
- Evidence: Abstract 逐字声明 'effective human-to-robot transfer capability' 与 CALVIN 提升；Table 4 caption（位于 4.4 节表面）给出 ABC→D 设定与 Avg.L/Avg.R 定义；4.4.5 正文给出教师蒸馏机制。定量数值经全文核对（Exo2EgoPose 3.38/67.5% vs AR-VRM 3.29/65.9%），但 Table 4 数值区与 4.4.5 段落在抽取文本中位于第二个 'Methods' 标题之下，审计的章节表面匹配只取首个同名标题，该区域不可定位，故本卡 quantitative=false 作定性收录，数值保留在 findings 与 tables。
- Quote: “Moreover, it demonstrates an effective human-to-robot transfer capability and yields improvements on the CALVIN dataset.”
- Authors: zhaofeng-shi; heqian-qiu; lanxiao-wang; et al.

### EA-EGOPREC-2026-0468

- Claim: EgoRecovery 用 HaWoR 从第一视角视频重建双手 MANO 并提取腕部 6-DoF 位姿与指尖距离夹爪代理组成 14D 人体状态流，但该重建轨迹仅用于人类解码器辅助训练与矫正意图目标构建，明确不作为机器人坐标系的动作监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.19745](https://arxiv.org/abs/2607.19745) EgoRecovery: Acquiring Failure Recovery Ability Through Human Recovery Demonstration
- Locator: Appendix F Motion Reconstruction and Data Preprocessing; References (extraction 将附录 A-H 并入 References surface)
- Evidence: Appendix F 描述 HaWoR→MANO→腕部 6-DoF + 夹爪代理的 14D 流，并明确声明不用于机器人动作监督；3.2 说明意图目标仅描述矫正幅值包络。
- Quote: “This reconstructed pose stream is used as the human embodiment trajectory for the auxiliary human decoder and for corrective intent target construction. It is not used as robot frame action supervision.”
- Authors: zuhao-ge; yu-chen-zhou; weitao-zhou; et al.

### EA-EGOPREC-2026-0469

- Claim: EgoRecovery 对 HaWoR 重建轨迹设定显式质量门：腕部位置帧间跳变超过 30mm 或欧拉角跳变超过 20° 的帧由邻近有效帧插值替换，再经中值滤波与 Savitzky-Golay 平滑；清洗后仍不可靠的段被拒绝或掩码剔除；人类示教集还按可靠双手追踪、无严重遮挡与传感丢帧逐集过滤。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.19745](https://arxiv.org/abs/2607.19745) EgoRecovery: Acquiring Failure Recovery Ability Through Human Recovery Demonstration
- Locator: Appendix F Motion Reconstruction and Data Preprocessing; Appendix E Data Collection and Annotation; References (extraction 将附录 A-H 并入 References surface)
- Evidence: Appendix F 给出 30mm/20° 跳变插值与平滑流程及不可靠段剔除；Appendix E 给出集级过滤标准（可靠双手追踪、无严重遮挡或丢帧）。
- Quote: “Frames with wrist position jumps above 30 mm or Euler-angle jumps above 20 ◦ are replaced by interpolation from neighboring valid frames.”
- Authors: zuhao-ge; yu-chen-zhou; weitao-zhou; et al.

### EA-EGOPREC-2026-0470

- Claim: EgoRecovery 将未来窗口的归一化末端位移投影到 K=4 低频 DCT 基上并取空间范数，得到只对矫正幅值包络敏感的 4D 意图目标；该设计刻意使目标对小的时序或接触差异不敏感，并辅以峰峰位移低于 0.01m 的近静止段掩码，从而在表示层容忍手部重建噪声。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.19745](https://arxiv.org/abs/2607.19745) EgoRecovery: Acquiring Failure Recovery Ability Through Human Recovery Demonstration
- Locator: 3.2 Corrective Intent for Human to Robot Recovery Learning; G Corrective Intent Target
- Evidence: 3.2 与 Eq.1 描述 DCT 幅值包络及其『对小差异不敏感』的设计动机；Appendix G 给出 K=4、L=16 相位点与 0.01m 近静止掩码。
- Quote: “To make the envelope compact and less sensitive to small timing or contact differences, we project the normalized future motion onto a low-frequency discrete cosine transform (DCT) basis”
- Authors: zuhao-ge; yu-chen-zhou; weitao-zhou; et al.

### EA-EGOPREC-2026-0471

- Claim: 在四任务闭环消融中，去除矫正段掩码（不再区分恢复段与名义/无效段）使平均 Recovery SR 从 85.0 降至 55.0，降幅大于去除意图损失本身（65.0）；恢复边界 t_rec 由运动能量曲线自动生成候选再经人工对照同步视频确认，同一遍标注记录质量标志与是否废弃。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.19745](https://arxiv.org/abs/2607.19745) EgoRecovery: Acquiring Failure Recovery Ability Through Human Recovery Demonstration
- Locator: 4.4 Ablation Study, Table 2; E Data Collection and Annotation
- Evidence: Table 2 消融给出 85.0→55.0（去掩码）与 85.0→65.0（去意图损失）；Appendix E 描述 t_rec 半自动标注流程与质量标志。
- Quote: “Removing the intent loss reduces average Recovery SR to 65.0, and removing the corrective segment mask degrades it further to 55.0.”
- Authors: zuhao-ge; yu-chen-zhou; weitao-zhou; et al.

### EA-EGOPREC-2026-0451

- Claim: HiFi-UMI 的头戴离线双目惯性 SLAM + 标记块手部定位管线在约 2 m 累积头轨迹工作空间内达到 3 mm 平均末端平移误差（以基站追踪为真值、仅用于精度评测），跨传感器时间偏差 <40 μs，轨迹重建通过率 98%，夹爪开合角误差 <0.1°。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: 3.4 Processed-Data Quality, Table 2
- Evidence: Sec 3.4 与 Table 2 直接报告端到端保真度五项指标，并说明 3 mm 是在约 2 m 工作空间内对基站真值的平均平移误差。
- Quote: “Tab. 2 reports the end-to-end fidelity of the processed data. The pipeline delivers 3 mm end-effector accuracy, cross-sensor timing offsets below 40 μs, fewer than two dropped frames per hour of capture, a 98% trajectory- reconstruction success rate, and gripper-state error below 0.1”
- Authors: simple-ai; unknown-author; yuteng-wei; et al.

### EA-EGOPREC-2026-0452

- Claim: 在三种 backbone（StarVLA-QwenPI、OpenPI-π0.5、LingBot-VA）上，仅用 HiFi-UMI 无本体数据后训练的策略与同场景遥操作后训练相比，聚合成功率差分别为 -2.5、+3.1、-0.6 个百分点，方向不一致且在 40 次/任务-策略的抽样噪声内；UMI 数据全部采自非评测场景，处于场景偏移的不利位置。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: 6.2 Can UMI-Only Post-Training Match Teleoperation-Based Post-Training?
- Evidence: Sec 6.2 三个组内受控对比（VLA 轨道 640 次 + WAM 轨道 320 次 rollout）报告了聚合成功率差；作者明确差异在抽样噪声内且比较非样本匹配（每任务约 3200 条 UMI vs 300 条遥操作）。
- Quote: “On StarVLA-QwenPI, the UMI-post-trained policy achieves 51.3% success (82/160), compared with 53.8% (86/160) for its teleoperation-trained counterpart, corresponding to a difference of only 2.5 percentage points.”
- Authors: simple-ai; unknown-author; yuteng-wei; et al.

### EA-EGOPREC-2026-0455

- Claim: 在 LingBot-VA 的真值未来视频诊断下（隔离视频生成误差），UMI 后训练策略在真实机器人 held-out 观测上的整段 12 步双臂 XYZ 轨迹 RMSE 为 24.33 mm，接近遥操作后训练的 21.64 mm；UMI→Real 与 UMI→UMI 的跨域差仅 3.20 mm 平移、0.23° 旋转，表明 UMI 动作标签训练出的解码器跨观测域退化很小。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: 6.2 Can UMI-Only Post-Training Match Teleoperation-Based Post-Training?, Figure 12
- Evidence: Sec 6.2.2 Figure 12 及正文给出 Real→Real 21.64 mm、UMI→Real 24.33 mm、UMI→UMI 21.13 mm，并报告跨域差 3.20 mm/0.23°；真随机参考约 117-124 mm 提供尺度。
- Quote: “resulting in cross-domain differences of only 3.20 mm in translation and 0.23”
- Authors: simple-ai; unknown-author; yuteng-wei; et al.

### EA-EGOPREC-2026-0523

- Claim: DexDirect 将低 setup 采集系统（视觉/位姿追踪类）演示性能受损归因于追踪闭环的四类因素：追踪延迟、位姿估计误差、工作空间失配、以及维持操作者-机器人坐标映射的认知负担——即手部/腕部位姿估计误差经'人动-机器人跟随'的追踪控制环路传播为机器人末端轨迹误差与演示失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.27784](https://arxiv.org/abs/2607.27784) DexDirect: Direct Kinesthetic Arm Guidance for Efficient Dexterous Demonstration Collection
- Locator: I. INTRODUCTION（追踪闭环归因段） / 6 DOF（extraction 图题被解析为伪节，引言该段实际落入此节面）
- Evidence: 引言在引出'避免代理环路的自然方式是直接引导机器人'之前，逐句列出低setup系统演示性能受影响的四类因素。
- Quote: “Consequently, demonstration performance is affected by factors such as tracking latency, pose estimation error, workspace mismatch, and the cognitive burden of maintain- ing a coordinate mapping between the operator and the robot.”
- Authors: beom-jun-kim; shiu-jen-wang; jonathan-liu; et al.

### EA-EGOPREC-2026-0524

- Claim: DexDirect 的缓解路线是让被直接拖动的物理机器人记录臂部轨迹：采集期完全不需要臂侧位姿估计、重定向、IK 求解器或笛卡尔运动生成器，所录每个构型都是机器人在关节与控制器限内的物理可达状态；与此互补，视觉通路被收缩为仅提供手局部坐标系下的手指构型，显式不使用单目 webcam 估计的全局腕部位姿。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.27784](https://arxiv.org/abs/2607.27784) DexDirect: Direct Kinesthetic Arm Guidance for Efficient Dexterous Demonstration Collection
- Locator: B. Direct Kinesthetic Arm Guidance / C. Vision-Based Finger Retargeting
- Evidence: III-B 给出'编码器直录+正运动学、采集期无估计/重定向/IK'的完整陈述；III-C 给出'不使用 webcam 全局腕部位姿、视觉管线限于手局部手指构型'的设计声明。
- Quote: “effector poses are obtained through forward kinematics. No arm-side pose estimation, retargeting, inverse-kinematics solver, or Cartesian motion generator is required during col- lection. Each recorded configuration therefore corresponds to a state physically attained by the robot, subject to its joint and controller limits.”
- Authors: beom-jun-kim; shiu-jen-wang; jonathan-liu; et al.

### EA-EGOPREC-2026-0525

- Claim: 在 10 名参与者 × 5 任务、同时间预算的被试内对照中，纯视觉追踪方案 AnyTeleop 仅产出 28 条成功演示（DexDirect 481 条、TeleDex 151 条，对应 17.2× 与 3.2× 吞吐差距），逐任务成功率 AnyTeleop 0–0.50 且在白板擦拭与键盘打字两任务上 0 成功——视频复盘将白板任务失败归因于操作者无法调节末端法向深度导致接触不足/不稳，即视觉追踪质量不足时演示可用性坍缩为任务级失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.27784](https://arxiv.org/abs/2607.27784) DexDirect: Direct Kinesthetic Arm Guidance for Efficient Dexterous Demonstration Collection
- Locator: C. Demonstration Throughput and Task Performance
- Evidence: IV-C 给出 481/151/28 吞吐、17.2×/3.2× 倍数、三方法逐任务成功率区间（0.71–0.96 / 0.32–0.85 / 0–0.50）、AnyTeleop 白板与键盘 0 成功及视频复盘的深度调节失败归因。
- Quote: “Under the same time budget per-condition, DexDirect col- lected 481 successful demonstrations across participants and tasks, compared with 151 for TeleDex and 28 for AnyTeleop. This corresponds to 3.2× the successful-demonstration throughput of TeleDex and 17.2× that of AnyTeleop. As summarized in Table I, DexDirect achieved the highest success rate on every task. Its success rate ranged from 0.71 on keyboard typing to 0.96 on Lazy Susan rotation and pick- and-place, whereas TeleDex ranged from”
- Authors: beom-jun-kim; shiu-jen-wang; jonathan-liu; et al.

### EA-EGOPREC-2026-0312

- Claim: 在三个真实灵巧任务上，用三级管线挖掘的任务相关人类样本（约 1.49M，不足池的 5%）训练 VLA，将总体成功率从等量随机采样的 47.7% 提升至 61.1%（+13.4）；在机器人数据 0.5×-2× 区间维持约 57-58% 的稳定下限，0.5× 时相对基线 +17.2。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.04196](https://arxiv.org/abs/2608.04196) SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation
- Locator: 4.3 Main Results
- Evidence: 4.3 主结果与 4.4 规模消融原文给出全部数字。
- Quote: “Mining task-relevant human data lifts the overall success rate from 47.7% to 61.1% (+13.4), using only ∼1.49M retrieved samples—under 5% of the human pool—which shows that targeted retrieval outperforms random sampling of the same size.”
- Authors: nie-lin; takehiko-ohkawa; sijin-chen; et al.

### EA-EGOPREC-2026-0045

- Claim: 跨帧接触一致性是端到端性能的最大单项贡献：消融中以逐帧接触观测替代跨帧接触一致性（w/o CC）时，轨迹成功率在 DexYCB 上从 57.78% 跌至 17.78%、在 TACO 上从 26.67% 跌至 10.00%（宽松口径），跌回最强基线水平；去掉 Laplacian 交互保持同样造成大幅下跌（DexYCB 降至 26.67%、TACO 降至 13.33%），而去稳定接触损失在宽松口径影响较小、严格旋转口径一致退化。成功判据为物体轨迹 ATE-Position≤0.10 m 且 ATE-Rotation≤1.00 rad（宽松）/0.50 rad（严格），不完整或非法轨迹计为失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.07045](https://arxiv.org/abs/2608.07045) C2Dex: Contact-Consistent Reconstruction and Retargeting for Dexterous Manipulation from Monocular Video
- Locator: Method (mangled table-header block holding the Table IV ablation results paragraph)
- Evidence: IV-E 消融段（提取文本中落入表格表头混杂块）报告：w/o CC 使成功率从 57.78%→17.78%（DexYCB）、26.67%→10.00%（TACO 宽松）；w/o Lap 跌至 26.67%/13.33%；w/o CPL 宽松口径 55.56%/23.33%、严格口径 44.44%/13.33%。阈值定义核对于 IV-A（ATE-P≤0.10 m，ATE-R≤1.00/0.50 rad，非法轨迹计失败）。
- Quote: “Table IV shows that cross-frame contact consistency is essential to end-to-end performance: removing it drops the success rate from 57.78% to 17.78% on DexYCB and from 26.67% to 10.00% (relaxed) on TACO.”
- Authors: jie-ren; zhehao-jiang; yinhong-yang; et al.

### EA-EGOPREC-2026-0511

- Claim: HandEdit 的 200M 规模 pseudo-GT 数据管线对分割、背景修复、手部重定向、IK 与虚拟基座放置、渲染/合成、和谐化每个阶段的中间输出施加自动检查与人工筛查，未通过阶段标准的样本被剔除，只有保留的和谐化输出才作为评测参考集——ego 视频→机器人数据管线的误差控制是分阶段设闸而非末端总检。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.12122](https://arxiv.org/abs/2608.12122) HandEdit: A Unified Benchmark for Egocentric Human-to-Robot Dexterous Hand Image Editing
- Locator: Abstract / Section 3.1 Data Curation Pipeline
- Evidence: Section 3.1 末段明确描述六个阶段的中间输出均经自动检查与人工筛查，失败者剔除，保留的和谐化输出构成评测用 pseudo-GT 参考集；附录 B 进一步给出各阶段具体标准。
- Quote: “Automatic checks and human screening are applied to intermediate outputs from segmentation, background restoration, retargeting, IK and virtual-base placement, rendering/compositing, and harmonization. Samples that fail the stage-specific criteria are excluded, and the retained harmonized outputs constitute the pseudo-GT reference set used for similarity-based evaluation.”
- Authors: zhenjie-yang; xingyu-jiao; guopeng-zhong; et al.

### EA-EGOPREC-2026-0513

- Claim: 在 11 个代表性编辑模型的 Hand-only 评测中，人手可移除性（removal 0.904-0.955）显著高于交互保持（interaction 0.266-0.703），结构保真与身份保真的模型间差距也更大；最强基线 GPT-Image-2 的 interaction 也仅 0.703——ego 人手画面转机器人画面时，保持物理可信的手物交互比去掉人手难得多。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.12122](https://arxiv.org/abs/2608.12122) HandEdit: A Unified Benchmark for Egocentric Human-to-Robot Dexterous Hand Image Editing
- Locator: Background / Section 4.2 Benchmark Results and In-depth Analysis
- Evidence: Section 4.2 关键观察原文+Table 4 数值：Hand-only 赛道 11 模型 removal 列 0.904-0.955、interaction 列 0.266-0.703；作者概括为'移除源人手相对容易，生成本体并保持交互是基准的主要难点'。
- Quote: “Most models obtain relatively high human-hand removal scores, suggesting that removing the source human hand is comparatively easier. In contrast, structural fidelity, ID fidelity, and interaction preservation show larger performance gaps across models.”
- Authors: zhenjie-yang; xingyu-jiao; guopeng-zhong; et al.

### EA-EGOPREC-2026-0069

- Claim: OmniShare 的人类演示采集使用配备 29 个磁旋转编码器的数据手套，实现亚度级（sub-degree）手部运动学测量，并以微秒级同步套件记录手部运动、接触与多视角场景观测。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.14028](https://arxiv.org/abs/2608.14028) AdvDex: Learning Dexterous Manipulation from Human Demonstrations via Joint-Aligned Actions and Adversarial Learning
- Locator: 3.1 OmniShare Dataset
- Evidence: 3.1.2 数据采集系统原文描述 29 编码器手套与亚度级运动学；该采集精度是论文宣称的“high-quality kinematic supervision”的物理基础。
- Quote: “The operator wears a data glove equipped with 29 magnetic rotary encoders for sub-degree hand kinematics”
- Authors: zhiyue-zhao; jing-wu; hairuo-liu; et al.

### EA-EGOPREC-2026-0046

- Claim: 在相同人类示教参考轨迹下，纯运动学重定向的直接回放在纸杯抓取上产生最高力追踪误差（侧抓 0.309±0.006 N、顶抓 0.736±0.000 N，各 5 次试验），而执行端力感知残差修正（REFORCE）将误差降至 0.247±0.036 N 与 0.474±0.049 N；作者同时指出运动学重定向忽略几何与接触动力学，输出仅为 coarse motion match。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.15560](https://arxiv.org/abs/2608.15560) ReForce: Learning Force-aware Retargeting for Dexterous Manipulation
- Locator: 4.1 Real-World Evaluation; 1 Introduction
- Evidence: Table 1 报告同一记录参考轨迹下三种执行方式的力追踪误差（牛顿，5 次试验均值±标准差），replay 最高、REFORCE 最低；1 Introduction 明确指出运动学重定向忽略接触动力学、输出为 coarse motion match。
- Quote: “Grasp Replay Admittance REFORCE Side 0.309 ± 0.006 0.280 ± 0.013 0.247 ± 0.036 Top 0.736 ± 0.000 0.619 ± 0.048 0.474 ± 0.049”
- Authors: yuhang-wu; lingqi-zeng; changwei-jing; et al.

### EA-EGOPREC-2026-0048

- Claim: 通过训练期结构化增强让控制器接触'参考失真'情形（reference-stall 冻结部分参考分量模拟停滞参考、pose-drift 从低力状态向关节限位扰动模拟位姿漂移），并向策略输入显式误差特征，可在仿真 held-out 14,605 episodes 上把力追踪误差从 Base+状态/力目标输入的 0.0601±0.0002 N 降到组合增强+误差特征的 0.0379±0.0006 N；仅加入位姿参考输入即可在各训练分布上降低约 32-35% 误差。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.15560](https://arxiv.org/abs/2608.15560) ReForce: Learning Force-aware Retargeting for Dexterous Manipulation
- Locator: 4.2 Simulation Ablation of Training Data and Policy Inputs; 4.1 Real-World Evaluation
- Evidence: 4.2 节描述两种结构化增强的构造与训练混合比例，Table 3 报告 4 种训练分布 × 3 种输入的力追踪误差（3 种子），正文给出 32-35% 与最优 0.0379±0.0006 N 的结论。
- Quote: “Base 0.0601 ± 0.0002 0.0400 ± 0.0013 0.0388 ± 0.0015 Base + Reference-stall aug. 0.0592 ± 0.0012 0.0401 ± 0.0025 0.0381 ± 0.0005 Base + Pose-drift aug. 0.0609 ± 0.0006 0.0396 ± 0.0010 0.0385 ± 0.0013 Base + Both aug. 0.0590 ± 0.0012 0.0396 ± 0.0030 0.0379 ± 0.0006”
- Authors: yuhang-wu; lingqi-zeng; changwei-jing; et al.

### EA-EGOPREC-2026-0491

- Claim: ViHaTeleop 在腕戴鱼眼相机上加装 LED 补光后，MediaPipe 手部关键点的帧间抖动（frame-to-frame landmark jitter）在直射眩光下平均降低 39.6%、在低光下降低 21.3%，低光检测率从 98.3% 升至 100%（单人 4 手势×4 光照条件×10 次=160 试次）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.16572](https://arxiv.org/abs/2608.16572) ViHaTeleop: A Low-Cost, Lightweight Visual-Haptic Teleoperation System for Dexterous Manipulation Learning
- Locator: B. Pose Estimation
- Evidence: III.B 逐字给出 160 试次 LED 开/关消融的抖动降幅与检测率提升四个数字。
- Quote: “comprising four gestures, four lighting/LED conditions, and ten repetitions each (160 trials), LEDs reduced mean frame- to-frame landmark jitter by 39.6% under direct glare and 21.3% in low light, while increasing low-light detection from 98.3% to 100%.”
- Authors: fucai-zhu; yanhou-lai; paul-maestre; et al.

### EA-EGOPREC-2026-0492

- Claim: ViHaTeleop 作者指出 ACE 移动版因浮动基座未被追踪而存在末端执行器映射失稳问题，并据此以 SLAM 追踪替代外骨骼，为遥操作提供固定原点参考系，使腕部→末端映射更直观稳定。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.16572](https://arxiv.org/abs/2608.16572) ViHaTeleop: A Low-Cost, Lightweight Visual-Haptic Teleoperation System for Dexterous Manipulation Learning
- Locator: A. Dexterous Teleoperation
- Evidence: II.A 段先指认 ACE 移动版非追踪浮动基座导致 unstable end-effector mapping，再给出本系统的固定原点 SLAM 替代方案。
- Quote: “while ACE’s exoskeleton adds considerable weight, and its mobile version suffers from unstable end-effector mapping due to a non-tracked floating base. We adopt ACE’s hand- tracking approach but replace the exoskeleton with SLAM- based tracking, providing a fixed-origin reference frame for more intuitive and stable mapping.”
- Authors: fucai-zhu; yanhou-lai; paul-maestre; et al.

### EA-EGOPREC-2026-0493

- Claim: ViHaTeleop 在腕部位姿→末端控制链上设置了两级轨迹保护：目标平移被钳制在机器人基座坐标系的预定义工作空间盒内；IK 求解失败或违反关节限时保持最后一条有效指令，以避免末端轨迹不连续。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.16572](https://arxiv.org/abs/2608.16572) ViHaTeleop: A Low-Cost, Lightweight Visual-Haptic Teleoperation System for Dexterous Manipulation Learning
- Locator: C. Robot Arm Control
- Evidence: III.C 逐字描述相对位姿映射、工作空间钳制与 IK 失败时 hold the last valid command 的防不连续策略。
- Quote: “The target pose is executed through inverse kinematics with joint limits; if IK fails or violates limits, we hold the last valid command to avoid discontinuities.”
- Authors: fucai-zhu; yanhou-lai; paul-maestre; et al.

### EA-EGOPREC-2026-0494

- Claim: ViHaTeleop 指认 DexPilot 重定向中距离依赖投影的突变阈值会造成中间抓握构型不连续（『snapping』），并以随拇指-手指距离平滑插值的自适应函数（投影距离 η(d) 与重定向权重 w(d)）替代硬阈值，消除该重定向引入的轨迹伪影。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.16572](https://arxiv.org/abs/2608.16572) ViHaTeleop: A Low-Cost, Lightweight Visual-Haptic Teleoperation System for Dexterous Manipulation Learning
- Locator: D. Robot Hand Motion Retargeting
- Evidence: III.D 先指出 abrupt thresholding 导致 snapping，再给出 η(d)/w(d) 平滑插值公式与 LEAP Hand 超参数。
- Quote: “We smooth this schedule because abrupt thresholding can cause discontinuous intermediate grasp configurations (“snapping”).”
- Authors: fucai-zhu; yanhou-lai; paul-maestre; et al.

### EA-EGOPREC-2026-0049

- Claim: 在离线（无人在环）人类示教设置中，重定向误差无人吸收、被直接放大：不精确的重定向（全身相似性与末端跟踪此消彼长）或不一致的重定向（相似人姿映射到不同关节配置）都会把重定向误差变成策略的监督误差，小误差即可导致回放失败。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29940](https://arxiv.org/abs/2606.29940) WARP: Whole-Body Retargeting for Learning from Offline Human Demonstrations
- Locator: 1 Introduction
- Evidence: 1 Introduction 系统陈述离线设置缺少遥操作的在线修正，重定向轨迹即监督，并列出 imprecision 与 inconsistency 两类失败模式；Fig 1 说明小误差导致回放失败。
- Quote: “Either case turns retargeting error into supervision er- ror. Second, the solution may be inconsistent: because humanoids are highly redundant, nearly identical human poses can map to different configurations depending on solver initialization or local tradeoffs. Similar observations would be paired with divergent actions, which impedes learning.”
- Authors: zhenyang-chen; chuizheng-kong; chuye-zhang; et al.

### EA-EGOPREC-2026-0050

- Claim: 闭式 SEW 求解+掌部硬约束把重定向环节的掌位误差压到机器精度量级：WARP（JL off）掌位均值误差 0.0046 mm、P95 0.046 mm、掌朝向误差 8.74e-6 deg，较优化式末端软目标基线 MINK-EF（0.701 mm / 1.853 mm / 0.0107 deg）降低 150 倍以上，且无约束 SEW-M 达 178.979 mm；评估覆盖 514 条人类示教、135,896 帧。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29940](https://arxiv.org/abs/2606.29940) WARP: Whole-Body Retargeting for Learning from Offline Human Demonstrations
- Locator: 4.1 Evaluation on Retargeting Motion Quality
- Evidence: Fig 5 表格给出四种方法 JL on/off 的掌位/朝向误差等指标，正文陈述 150× 与机器精度结论；C.2.1 给出 514 motions、135,896 frames 规模。
- Quote: “SEW-M off 178.979 201.056 7.89e-6 0.000 0.0126 0.243 0.488 1.20e-25 6.83e-14 MINK-EF off 0.701 1.853 0.0107 0.625 0.1610 0.977 0.368 173.49 3.117 MINK-TE off 18.557 73.980 0.157 0.027 0.0852 0.640 1.026 1119.11 6.106 WARP off 0.0046 0.046 8.74e-6 0.000 0.0047 0.163 0.289 1.14e-25 6.66e-14”
- Authors: zhenyang-chen; chuizheng-kong; chuye-zhang; et al.

### EA-EGOPREC-2026-0051

- Claim: 重定向质量差异在开环回放成功率上几乎不可见（DexMimicGen 三任务平均 WARP 80.0% vs MINK 79.5%），但传导到策略学习后显著放大：相同策略在 WARP 数据上平均成功率 71% vs MINK 数据 59%（+12%）；真实世界 rotate-box 上同样回放接近而策略 65% vs 40%。作者据此断言'replay 持平掩盖重定向差异，运动质量而非回放完成度决定下游成败'。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29940](https://arxiv.org/abs/2606.29940) WARP: Whole-Body Retargeting for Learning from Offline Human Demonstrations
- Locator: 4.2 Simulation Evaluation; 4.3 Real-World Evaluation
- Evidence: Table 1 报告三任务 replay/policy 成功率矩阵，4.2 正文给出'replay parity understates the difference'与'decisive downstream'结论；4.3 Finding Summary 给出真实世界 65% vs 40%。
- Quote: “MINK 99.5% 94% 88.5% 74% 50.5% 8% 79.5% 59% WARP 98.5% 100% 90.5% 78% 51.0% 34% 80.0% 71% Table 1: Replay and policy rollout re- sult (%) on DexMimicGen tasks. WARP achieves 12% higher success rate for policy.”
- Authors: zhenyang-chen; chuizheng-kong; chuye-zhang; et al.

### EA-EGOPREC-2026-0053

- Claim: 为吸收人侧运动的小幅抖动与晃动，WARP 在移动底座上采用死区+二阶滤波（deadband δxy=0.05 m、δθ=0.1 rad、阻尼比 ζ=1、自然频率 fn≈1.5 Hz）：死区内弹簧力为零、底座仅靠阻尼滑行静止，jitter 与小晃动永不传到轮子；躯干吸收细调节、底座只处理真实搬移。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.29940](https://arxiv.org/abs/2606.29940) WARP: Whole-Body Retargeting for Learning from Offline Human Demonstrations
- Locator: Appendix B.5 Lazy Mobile-Base Filter; References
- Evidence: 附录 B.5 给出死区滤波器公式（Eq. 6-7）与全部参数取值，并陈述死区内抖动不达轮子的设计目标；3 Method 的 Lazy Mobile-Base Tracking 段给出躯干吸收细调节的机制说明。
- Quote: “Inside the deadband the spring force vanishes and the base coasts to rest under damping alone, so jitter and small sway never reach the wheels; outside it, the spring smoothly draws the base toward the target. We use ζ = 1 for non-overshooting tracking, f n ≈ 1.5 Hz, and deadband radii δ xy = 0.05 m and δ θ = 0.1 rad.”
- Authors: zhenyang-chen; chuizheng-kong; chuye-zhang; et al.

### EA-EGOPREC-2026-0422

- Claim: 真实部署中机器人腕部轨迹相对仿真参考的平均 sim-to-real 追踪误差为 2.83cm，且随任务阶段递增：approach 1.1cm、grasp 2.7cm、lift 3.8cm；z 向存在约 5.7mm 系统性抬高，跨 episode 重复性标准差仅 0.46-0.82cm。作者将残差归因于臂阻抗控制器稳态顺应偏移、≤1cm 物体摆放变化与相机外参标定误差，而非学习到的运动本身——且在此误差水平下 cube picking 仍达 93% 成功率。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.07747](https://arxiv.org/abs/2609.07747) Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction
- Locator: Appendix
- Evidence: 附录 B Fig.7：mean sim-to-real tracking error 2.83cm、cross-episode std 0.46-0.82cm、阶段分解 1.1→2.7→3.8cm、z 向 +5.7mm；真实成功率 28/30 出自 4.4。
- Quote: “The sim-to-real discrepancy exhibits structured patterns across spatial axes and task phases. The dominant deviation occurs along the x-axis, which corresponds to the forward load-bearing direc- tion, while the y- and z-trajectories remain more closely aligned. Temporally, the discrepancy in- creases from 1.1 cm during approach to 2.7 cm during grasp and 3.8 cm during lift. This pattern is consistent with a steady-state compliance offset of the arm impedance controller under increasing payload,”
- Authors: ruoqu-chen; feixiang-ruan; liu-cao; et al.

### EA-EGOPREC-2026-0423

- Claim: 单目视频手部轨迹在使用前经三级净化链：WiLoR 逐帧初始估计→MANO 参数模型对检测 2D 关键点的投影拟合→全序列时间一致性精修与手-物穿透约束联合优化；重定向环节再以两阶段优化（先臂-腕后臂-手联合）并对拇指/食指/远端关键点加大权重——检测误差在重建与重定向两个阶段被显式抑制而非直接传导。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.07747](https://arxiv.org/abs/2609.07747) Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction
- Locator: 3.2 Motion Prior Data Extraction with Spatial Augmentation
- Evidence: 3.2 正文：WiLoR 初始估计+MANO 时间一致性与手-物穿透约束精修；两阶段重定向'using larger weights for the thumb, index finger, and distal keypoints'；附录 C 给出 L_hand/L_batch/L_joint 目标，附录 D 给出手指权重表（拇指25/食指15/中指10/环7/小5，Tip 1.0→Proximal 0.3）。
- Quote: “the hand-object motion at 30 Hz. Object poses are estimated using FoundationPose [41], while hand poses are estimated using WiLoR [42] and further refined with MANO-based temporal consistency and hand-object penetration constraints.”
- Authors: ruoqu-chen; feixiang-ruan; liu-cao; et al.

### EA-EGOPREC-2026-0424

- Claim: 重定向环节设显式可用性硬阈值：空间增强后的每个演示变体计算全轨迹平均末端位置追踪误差，超过 8cm 即标记不可达并排除出策略训练——防止检测/重定向质量过差的轨迹污染后续学习。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.07747](https://arxiv.org/abs/2609.07747) Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction
- Locator: Appendix
- Evidence: 附录 D：'we compute the mean end-effector position tracking error over the trajectory. Augmented variants whose mean error exceeds 8 cm are marked unreachable and excluded from policy training'；该过滤作用于 ±5cm/±10° 空间增强变体。
- Quote: “tion, we compute the mean end-effector position tracking error over the trajectory. Augmented variants whose mean error exceeds 8 cm are marked unreachable and excluded from policy training.”
- Authors: ruoqu-chen; feixiang-ruan; liu-cao; et al.

### EA-EGOPREC-2026-0425

- Claim: 真实世界 cube picking 模态消融（同一教师蒸馏）：完整视觉-触觉策略 28/30（93.3%），移除视觉降至 14/30，移除触觉降至 11/30，仅本体感知 8/30；失败集中于抓取未命中与接触后脱手——触觉反馈与视觉检测形成近半数的独立互补贡献，可补偿视觉/检测链的不足。
- Stance: `support` | Confidence: `direct`
- Paper: [2609.07747](https://arxiv.org/abs/2609.07747) Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction
- Locator: 4.3 Q2: The Role of Scene and Tactile Representations
- Evidence: 4.3 正文：full 28/30、no vision 14/30、no tactile 11/30、proprioception only 8/30，变体均蒸馏自同一教师；失败模式为 missing the object during grasp acquisition 与 losing the object after contact。
- Quote: “The full visual-tactile policy achieves 28/30 success, while removing vision or tac- tile feedback reduces success to 14/30 and 11/30, respectively; using proprioception alone further reduces success to 8/30.”
- Authors: ruoqu-chen; feixiang-ruan; liu-cao; et al.

### EA-EGOPREC-2026-0017

- Claim: 由 2D 点轨预测经初始帧深度+刚体变换优化（PnP）提升得到的开环 3D 末端执行器轨迹，真机成功率仅 25-35%（MG/G/CG/TG 四级），主要失败于抓取位置不准与无法从中间失败恢复；叠加用约 400 条本体遥操作示教训练的闭环残差策略后成功率升至 40-70%，说明预测/提升误差会直接传导到末端轨迹并降低可用性，但可被少量本体数据的残差校正部分缓解。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2405.01527](https://arxiv.org/abs/2405.01527) Track2Act: Predicting Point Tracks from Internet Videos enables Generalizable Robot Manipulation
- Locator: 5.2 Robot Manipulation Results, Table 2
- Evidence: Table 2 报告 Ours (Open-Loop) 35/25/30/25% vs Ours（残差闭环）70/60/55/40%；3.4 节说明开环失败源于预测小误差与缺乏接触推理；5.3 节列出失败模式。残差策略训练数据约 400 条轨迹见 4.3 与附录 6.6。
- Quote: “MG G CG TG Behavior Cloning (BC) 60% 20% 0% 0% Affordance-Conditioned 65% 30% 10% 5% Video-Conditioned 60% 25% 0% 0% Hand-Object Mask-Conditioned 70% 40% 25% 20% Ours (Open-Loop) 35% 25% 30% 25% Ours (Ablation; actions not residuals) 70% 45% 30% 30% Ours 70% 60% 55% 40%”
- Authors: homanga-bharadhwaj; roozbeh-mottaghi; abhinav-gupta; et al.

### EA-EGOPREC-2026-0480

- Claim: 在 5 名未受训操作者的用户研究中，低成本 ERM 触觉反馈在 10 组比较中的 9 组维持或提高任务成功率，并加快对形变小的球的移球任务；操作者报告视觉部分受阻时触觉反馈加快了物体定位并增强遥操作信心。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2407.03162](https://arxiv.org/abs/2407.03162) Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning
- Locator: 4.3 User Study of Haptic Feedback
- Evidence: 4.3 用户研究报告 9/10 比较维持或提高成功率、移球任务更快，以及操作者在视觉受阻时借助触觉定位的主观报告。
- Quote: “As shown in Fig. 4, haptic feedback maintains or improves suc- cess rates in 9 out of 10 comparisons. This boost is attributed to enhanced interaction awareness between the robot and the object, which prevents abnormal current generation in robot arms due to excessive pressure, thus promoting safer operations.”
- Authors: runyu-ding; yuzhe-qin; jiyue-zhu; et al.

### EA-EGOPREC-2026-0003

- Claim: 手部检测精度强依赖训练数据规模与分布：同一检测器训练图像从 0.25M 增至 2M 时 OxfordHands mAP 由 26.69 升至 48.98；改用仅在 OxfordHands 上训练时 WHIM mAP 降至 35.29，而 WHIM 全量训练达 53.79。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2409.12259](https://arxiv.org/abs/2409.12259) WiLoR: End-to-end 3D Hand Localization and Reconstruction in-the-wild
- Locator: 5.1. Evaluation of Hand Detection and Localization, Table 2
- Evidence: Table 2 消融逐行列出训练数据量（0.25M/0.5M/1M/2M）与训练集组合（仅 OxfordHands vs WHIM）下的 AP0.5/mAP。
- Quote: “Proposed-w. 0.25M - - 49.15 26.69 75.75 38.48 Proposed-w. 0.5M - - 58.32 35.15 83.03 42.11 Proposed-w. 1M - - 69.21 43.04 88.37 47.92 Proposed-w.OxfordHands - - 68.15 40.34 70.14 35.29 Proposed-w. ResNet50 118 34 74.13 47.34 95.43 51.85 Proposed-w. HRNet 132 30 84.82 49.83 97.23 54.12 Proposed-w/o Augmentations - - 70.76 42.17 91.13 49.93 Proposed-w/o Landmark Loss - - 72.57 45.96 92.43 51.44 Proposed-M 25 (↓ 5×) 138 (↑ 4×) 82.64 48.98 96.06 53.79”
- Authors: rolandos-alexandros-potamias; zhang-jinglei; jiankang-deng; et al.

### EA-EGOPREC-2026-0426

- Claim: FastUMI 手持设备以 RealSense T265 提供末端位姿真值，对照光学动捕真值的平均定位误差随视觉遮挡加剧而上升：低遮挡 Pick Cup 为 10.5mm，部分遮挡 Open Container 升至 17.7mm，强遮挡 Rearrange Coke 进一步劣化（Table I 单轨迹 19-36mm）；替代传感器 RoboBaton MINI 低遮挡下 15.2mm 略差，但部分遮挡下 11.2mm 更稳定。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2409.19499](https://arxiv.org/abs/2409.19499) FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset
- Locator: VI-A. Data Quality, Table I
- Evidence: 作者将 4 个反光标记贴于手持设备，以光学动捕系统轨迹为真值，用 evo 工具包计算 T265 与 MINI 在 3 个遮挡递增任务上的定位误差，每任务 10 条轨迹；正文明确给出 10.5/17.7/15.2/11.2mm 四个均值并指出 Rearrange Coke 中 T265 进一步劣化。
- Quote: “In the “Pick Cup” scenario, where occlusion is minimal, T265 achieves an average positioning error of 10.5 mm, while MINI’s error averages 15.2 mm. In the “Open Container,” T265’s error increases to 17.7 mm, reflecting the partial obstruction of its field of view, whereas MINI’s error decreases to 11.2 mm.”
- Authors: zhaxizhuoma; liu-kehui; guan-chuyue; et al.

### EA-EGOPREC-2026-0427

- Claim: T265 的 VIO 误差沿演示轨迹呈非均匀时间分布：轨迹首尾误差低、中段显著增大，夹爪靠近桌面遮挡视觉特征时出现两个明显误差峰，回到初始视角后回环闭合机制将追踪精度恢复至接近初始水平。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2409.19499](https://arxiv.org/abs/2409.19499) FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset
- Locator: VI-A. Data Quality, Fig. 11
- Evidence: VI-A 正文明确描述该时间模式并以 Fig. 11 展示 Pick Cup 任务中 T265 误差曲线：近桌面遮挡产生两个误差峰，返回初始视角后回环恢复精度。
- Quote: “We also observe that the VIO error typically remains low at the beginning and end of each trajectory but grows noticeably in the middle. Fig. 11 illustrates this pattern for T265 during the “Pick Cup” task: as the gripper moves closer to the table, occlusion reduces visible features and causes two pronounced error peaks.”
- Authors: zhaxizhuoma; liu-kehui; guan-chuyue; et al.

### EA-EGOPREC-2026-0428

- Claim: FastUMI 的采集端质量控制依赖 T265 四级置信度（Failed/Low/Medium/High）门控：环境需满足至少 95% 采样位姿为 High 才开录；录制中低置信度位姿被剔除并用邻帧插值保持连续；光照不足会显著降低置信度并加剧漂移。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2409.19499](https://arxiv.org/abs/2409.19499) FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset
- Locator: III-B. Raw Data Quality Assessment
- Evidence: III-B 描述置信度门控、环境验证阈值、低置信度位姿剔除插值与光照敏感性；III-A 另给出重初始化与蓝色参考槽回环两种漂移校正策略。
- Quote: “Our tests indicate that lighting conditions notably affect the T265’s performance, with dim or low-light environments often leading to reduced confidence levels and increased drift. During actual recordings, any low-confidence pose is excluded and interpolated from neighboring frames to maintain continuity.”
- Authors: zhaxizhuoma; liu-kehui; guan-chuyue; et al.

### EA-EGOPREC-2026-0006

- Claim: 在 HOT3D ego-centric 世界系评测中，HaWoR 全模型达到 W-MPJPE 33.20mm、WA-MPJPE 11.27mm、RTE 0.78%、Accel 5.41 m/s²；消融显示去除预训练 WiLoR ViT 骨干特征后 W-MPJPE 恶化至 86.80mm（PA-MPJPE 7.59），去除时序图像与姿态先验（IAM&PAM）后恶化至 44.60mm。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2501.02973](https://arxiv.org/abs/2501.02973) HaWoR: World-Space Hand Motion Reconstruction from Egocentric Videos
- Locator: 4.3. Ablation / Table 4(a)
- Evidence: Table 4(a) 逐行报告全模型与三个消融配置的世界系指标；33.20mm 与正文 Table 3 的 Proposed 行一致（见 findings），消融行直接显示组件移除对世界系误差的影响。
- Quote: “Method PA-MPJPE W-MPJPE WA-MPJPE RTE Accel w/o Pretrained ViT 7.59 86.80 19.46 1.26 9.09 w/o IAM & PAM 5.07 44.60 13.85 0.93 8.42 w/o PAM 4.80 36.32 12.40 0.88 6.03 Proposed 4.79 33.20 11.27 0.78 5.41 (a) Hand motion components. Here is the ablation results without IAM (Image Attention Module), PAM (Pose Attention Module) or pretrained ViT.”
- Authors: jinglei-zhang; jiankang-deng; chao-ma; et al.

### EA-EGOPREC-2026-0008

- Claim: 手部出视野帧是 ego 视频世界系轨迹的主要误差来源：HOT3D 不可见序列上，朴素 Last Pose 补全 W-MPJPE 116.79mm、LERP 插值 75.01mm，HaWoR 学习型 infiller 降至 66.25mm，但仍约为可见帧全管线世界误差（33.20mm）的两倍。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2501.02973](https://arxiv.org/abs/2501.02973) HaWoR: World-Space Hand Motion Reconstruction from Egocentric Videos
- Locator: 4.3. Ablation, Table 4(b)
- Evidence: Table 4(b) 在 HOT3D 不可见序列上比较三种补全策略的 FID/PA-MPJPE/W-MPJPE/WA-MPJPE/RTE；33.20mm 来自同论文 Table 3 的 Proposed 行。
- Quote: “Method FID PA-MPJPE W-MPJPE WA-MPJPE RTE Last Pose 1.52 7.83 116.79 78.78 13.04 LERP 1.42 6.33 75.01 49.16 9.39 Proposed 0.57 6.22 66.25 37.22 7.41 (b) Motion Infiller. We experiment on the invisible sequences of HOT3D [4] validation dataset.”
- Authors: jinglei-zhang; jiankang-deng; chao-ma; et al.

### EA-EGOPREC-2026-0351

- Claim: 在 Phantom 管线中，单目手部姿态估计器 HaMeR 虽能准确重建手型，但无法可靠估计绝对 3D 姿态；作者用 SAM2 分割+深度图构造手部点云，再以 ICP 将 HaMeR 网格对齐到点云来修正绝对位姿，进而生成机器人末端位置/姿态/夹爪开合动作标签。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2503.00779](https://arxiv.org/abs/2503.00779) Phantom: Training Robots Without Robots Using Only Human Videos
- Locator: 3.2 Action Labeling of Human Videos
- Evidence: 3.2 节明确写出 HaMeR 因单目依赖难以估计绝对 3D 姿态，并用深度+ICP 精修；动作标签(p_t, R_t, g_t)全部由精修后关键点定义。
- Quote: “While HaMeR accurately captures hand shape, it struggles to estimate the absolute 3D pose due to its reliance on a monocular image. To refine this estimate, we incorporate depth data.”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0352

- Claim: HaMeR 对 RGB 中被遮挡的手部关键点估计困难，抓取时尤为严重，常预测出不符合解剖学的手指构型；Phantom 通过将拇指与食指末两关节约束为单自由度、限制在解剖可行范围内来缓解该误差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2503.00779](https://arxiv.org/abs/2503.00779) Phantom: Training Robots Without Robots Using Only Human Videos
- Locator: 3.2 Action Labeling of Human Videos
- Evidence: 3.2 节明确指出遮挡下关键点失真在抓取时加剧、球关节模型产生不真实手指构型，并以单自由度约束应对。
- Quote: “HaMeR also struggles with keypoints that are occluded in the RGB image—an issue exacer- bated during grasping. Since HaMeR models all hand joints as ball joints, it often predicts unrealistic finger configurations under occlu- sion. To address this, we constrain the last two joints of the thumb and index fingers to a sin- gle degree of freedom, limiting their movement to anatomically feasible ranges. This ensures more accurate finger pose estimation when oc- clusions occur.”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0354

- Claim: 在 Kinova 单场景扫描任务上，训练数据规模相同时人手视频演示训练的策略成功率低于遥操作机器人演示：50 条时 0.44 vs 0.52(p=0.778)，100 条时 0.64 vs 0.88(p=0.095)；将人手演示扩到 300 条成功率升至 0.84。作者将该精度差距归因于 RGBD 视频中手部姿态估计的不确定性，并指出人手数据易采集、可用规模弥补单条精度。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2503.00779](https://arxiv.org/abs/2503.00779) Phantom: Training Robots Without Robots Using Only Human Videos
- Locator: 6.3 Evaluating the Benefits of Co-training with Diverse Human Data, Table 6
- Evidence: Appendix 6.4 及 Table 6 报告三种数据规模下人手 vs 机器人演示的成功率与 Fisher 精确检验，并明确归因于手部姿态估计不确定性。
- Quote: “While our approach significantly reduces the cost of scaling data collection across diverse environ- ments, it introduces a tradeoff: human video demonstrations provide scalability at the expense of some precision, due to uncertainty in hand pose estimation from RGBD videos. To investigate how much precision is lost, we compare policies trained on teleoperated robot demonstrations (collected using an Oculus controller) against those trained on human video demonstrations for the Kinova sweeping t”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0501

- Claim: 接触力存在时，replay 记录的末端位姿无法恢复示教动作；作者采用的误差补偿启发式虽能在第二次 replay 完成任务，但引入高 jerkiness，导致动觉示教数据在需强接触力的 Push Sanitizer 任务上训练的扩散策略性能不及遥操作数据。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2503.07017](https://arxiv.org/abs/2503.07017) How to Train Your Robots? The Impact of Demonstration Modality on Imitation Learning
- Locator: V. RESULTS
- Evidence: 结果节明确报告 Push Sanitizer 中 replay 首次失败、误差项导致动作高 jerkiness；图 5 显示该任务上动觉示教策略欠优；设计节描述无力传感器时只能用补偿启发式。
- Quote: “However, in Push Sanitizer (requiring high contact force), kinesthetic teaching falls short since replaying recorded end-effector poses did not succeed at this task in the first try. The error term we introduced in Section IV induces high jerkiness in actions despite successfully completing the task on the second iteration.”
- Authors: haozhuo-li; yuchen-cui; dorsa-sadigh

### EA-EGOPREC-2026-0318

- Claim: MAPLE 的监督信号完全来自现成检测器链而非人工标注或真值动捕：VISOR-HOS 接触分割定位接触帧、HaMeR 逐帧重建 MANO 手部姿态、SAM-PT 点追踪回投影接触点；管线施加多重质量门控（HOS 置信度 ≥0.9 且恰好单只右手接触、物体掩码腐蚀、指尖投影距离比落在 0.3-1.7 之外则弃用、45 帧内找不到预测帧则弃用），从约 1,590 小时 Ego4D 子集仅产出约 82,100 个训练样本。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2504.06084](https://arxiv.org/abs/2504.06084) MAPLE: Encoding Dexterous Robotic Manipulation Priors Learned From Egocentric Videos
- Locator: 3.2. Manipulation Supervision Extraction
- Evidence: 3.2 给出 HaMeR/SAM-PT 提取链；S6 给出置信度、距离比与超时三道门控；3. MAPLE 给出 82,100 样本规模。
- Quote: “For each contact frame, we use the pre- trained hand pose estimation model HaMeR [49] to extract the MANO [57] pose vector”
- Authors: alexey-gavryushin; xi-wang; robert-j-s-malate; et al.

### EA-EGOPREC-2026-0321

- Claim: 手部姿态监督的粒度需要工程收窄才可用：作者把 MANO 姿态用 Memcodes tokenizer 离散为 8 个 codebook×1024 类的分类任务，以规避直接回归面临的解剖约束与自穿透问题；消融显示 tokenizer 版在 DAPG 四任务均值 38.3%，高于直接回归手部姿态的 36.7%、去掉接触损失的 36.0% 与去掉手部姿态损失的 35.6%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2504.06084](https://arxiv.org/abs/2504.06084) MAPLE: Encoding Dexterous Robotic Manipulation Priors Learned From Egocentric Videos
- Locator: 4.2. Evaluation in Simulation Environments / T. Success rates are averages
- Evidence: 3.2 给出 tokenizer 设计动机；Table 3 给出四配置消融均值；4.2 分析段确认 tokenizer 一致更优。
- Quote: “training the model with a hand pose tokenizer leads to a higher performance than letting it reconstruct hand poses from scratch”
- Authors: alexey-gavryushin; xi-wang; robert-j-s-malate; et al.

### EA-EGOPREC-2026-0083

- Claim: EgoDex 的手部标注在采集时由 Vision Pro 的多相机、已知内外参与生产级手部预测网络共同产生；作者论证事后手部预测网络（如 HaMeR 用于网络视频）在缺少多视角与时刻相机外参时预测质量会受损。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2505.11709](https://arxiv.org/abs/2505.11709) EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video
- Locator: Section 2.3 Learning from Human Video (extraction block: background)
- Evidence: 2.3 节对比两种标注路径并给出设计理由；abstract 与 3.1 节确认 ARKit/on-device SLAM 来源。
- Quote: “quality of these networks can suffer without multiple viewpoints and detailed knowledge of the camera extrinsics at all times, usually unavailable with raw Internet video. In contrast, the EgoDex dataset includes 3D head and hand tracking at the time of collection, where multiple cameras on the Vision Pro, known intrinsics and extrinsics, and a production-grade hand prediction network all contribute to precise annotation.”
- Authors: ryan-hoque; peide-huang; david-j-yoon; et al.

### EA-EGOPREC-2026-0361

- Claim: EgoZero 发现 HaMeR 在相机坐标系下的末端预测不准确，但其手坐标系内的局部预测更可靠；因此用 Aria MPS 的 6DoF 手姿(H_t)校正 HaMeR 构建的掌心坐标系，即把 HaMeR 的局部手部形变与 Aria 的 ego-centric 手部定位组合成最终动作标签。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2505.20290](https://arxiv.org/abs/2505.20290) EgoZero: Robot Learning from Smart Glasses
- Locator: 3.1 Human-Robot Domain Unification
- Evidence: 3.1 节明确写出 HaMeR 相机系不准、手系可靠，并以 H_t 校正掌心帧的组合方案(式 1)。
- Quote: “Though HaMeR’s end-effector predictions in camera frame are inaccurate, its pre- dictions localized in hand frame are more reliable. Therefore, we compose local hand deformation from HaMeR with egocentric hand information from Aria.”
- Authors: vincent-liu; ademi-adeniji; haotian-zhan; et al.

### EA-EGOPREC-2026-0435

- Claim: 在 DexUMI 的 4 任务×2 手评估中，相对（relative）手指动作表示的阶段累计成功率一致高于绝对表示：同为触觉+Inpaint 配置下，Cube 1.00 vs 0.10、Tea-leaf（XHand）0.85 vs 0.00、Kitchen-salt 0.75 vs 0.00；作者据此认为相对轨迹对噪声与硬件缺陷更鲁棒。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2505.21864](https://arxiv.org/abs/2505.21864) DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation
- Locator: 5 Evaluation (Table 1)
- Evidence: Table 1 给出 Rel/Abs×触觉×视觉适配的完整消融矩阵，5.1 明确相对轨迹一致更优并给出分布简单性与反应式累积行为两点解释。
- Quote: “Rel Yes Inpaint 1.00 0.85 1.00 0.85 1.00 0.85 0.95 0.95 0.75 Abs Yes Inpaint 0.10 0.35 0.80 0.00 1.00 0.25 0.50 0.45 0.00”
- Authors: mengda-xu; han-zhang; yifan-hou; et al.

### EA-EGOPREC-2026-0436

- Claim: DexUMI 要求逐传感器延迟标定以维持观测-动作时间对齐：相机/iPhone 延迟用滚动 QR 码测量（沿用 UMI 方案），编码器延迟通过与回放机器人手图像的 overlay 对比调准——延迟设高则机器人手指在 overlay 中领先（执行未来动作），设低则滞后，需调至完全对齐后再做线性插值与 3 倍降采样。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2505.21864](https://arxiv.org/abs/2505.21864) DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation
- Locator: Appendix (E.2 Training Data Latency Management)
- Evidence: 附录 E.2 给出 t_capture = t_receive − l_sensor 的校正公式、QR 码测延迟法与编码器延迟的 overlay 调参判据。
- Quote: “If the encoder latency is set too low, the robot hand fingers will lag behind the exoskeleton fingers in the overlay image. We tune the encoder latency until the exoskeleton fingers and robot fingers are perfectly aligned.”
- Authors: mengda-xu; han-zhang; yifan-hou; et al.

### EA-EGOPREC-2026-0031

- Claim: 作者主张在多数灵巧操作任务中精确跟踪全局手腕位姿并非必要、且可能降低指尖位置精度；其重定向目标因此允许调整手腕位姿以换取更高的指尖精度。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2506.09384](https://arxiv.org/abs/2506.09384) Analyzing Key Objectives in Human-to-Robot Retargeting for Dexterous Manipulation
- Locator: II. METHOD
- Evidence: 方法节明确给出设计动机：形态差异下精确手腕追踪会与指尖相对位置/方向冲突，因此用拇指尖位置项替代手腕位置项，仅对手腕旋转加小权重正则；消融 A5（正文 B 节）报告该选择显著降低指尖全局位置误差。
- Quote: “However, accurate tracking of global wrist pose is not necessary in most dexterous manipulation tasks and may reduce accuracy in fingertip positions. Due to different hand morphologies between the human and robot, the fingertip positions relative to the wrist may conflict with the relative positions between fingertips and fingertip orientations. As a result, it can be better to allow adjustment of the wrist pose in exchange for higher fingertip accuracy.”
- Authors: xin-chendong; mingrui-yu; yongpeng-jiang; et al.

### EA-EGOPREC-2026-0032

- Claim: 重定向目标的 pinch 项将估计的拇指-主指尖距离在 [ε2, ε1] = [1×10^-2 m, 1×10^-1 m] 区间内线性重缩放到 [0, ε1]，并把低于 ε2 的距离截断为 0，使足够小的估计指尖距离被当作已闭合的捏取。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2506.09384](https://arxiv.org/abs/2506.09384) Analyzing Key Objectives in Human-to-Robot Retargeting for Dexterous Manipulation
- Locator: II. METHOD
- Evidence: 方法节给出 pinch 项的连续切换权重与分段线性距离重缩放公式，并明确 ε1=1×10^-1 m、ε2=1×10^-2 m；附录说明该设计针对 Vision Pro 在手指接触时仍输出小的正距离并抖动的现象（该段位于 extraction 图表碎片标题之后，故此处仅按方法节表述设计本身）。
- Quote: “fingertip distance within pinching range [ϵ 2 , ϵ 1 ] is lin- early rescaled into [0, ϵ 1 ]. This ensures a continuous transition in the pinching range and avoids sudden changes around the threshold ϵ 1 . In practice we set ϵ 1 = 1 × 10 −1 m and ϵ 2 = 1 × 10 −2 m.”
- Authors: xin-chendong; mingrui-yu; yongpeng-jiang; et al.

### EA-EGOPREC-2026-0518

- Claim: 在仿真基准中，Dex1B 上训练的模型在两种评测分布、两种方法、train/test 各 split 上一致优于在人类标注的 DexYCB/ARCTIC 上训练的模型（lifting 任务 DexSimple：DexYCB 测试集 53.02 vs 21.21；articulation 任务：ARCTIC 测试集 73.49 vs 23.08）；但该对比中数据集规模相差约五个数量级，优势混合了规模、多样性与质量效应，不能单独归因于数据质量。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2506.17198](https://arxiv.org/abs/2506.17198) Dex1B: Learning with 1B Demonstrations for Dexterous Manipulation
- Locator: V. EXPERIMENTS / B. Dataset Analysis
- Evidence: Table III 与 V-B Benchmarks 段：跨任务/基线/split 一致优势；原文表述 'the former outperforms the latter across tasks, baselines and splits'。
- Quote: “When comparing models trained on Dex1B to those trained on DexYCB/ARCTIC, we consistently find that the former outperforms the latter across tasks, baselines and splits.”
- Authors: jianglong-ye; keyi-wang; chengjing-yuan; et al.

### EA-EGOPREC-2026-0076

- Claim: 在 EgoVLA 的 ego 视频预训练混合中，手部姿态标注较噪的 HoloAssist 被刻意下采样至 1/10，以避免噪声标注源过度代表；即标注噪声通过降权而非清洗来缓解。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2507.12440](https://arxiv.org/abs/2507.12440) EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
- Locator: 3.1 Ego-Centric Human Manipulation Dataset
- Evidence: 作者在数据集构建中明确说明 HoloAssist 手部标注更噪，并因此均匀下采样至 1/10 以平衡任务与来源。
- Quote: “To avoid overrepresentation of HoloAssist, which has noisier labels, we uniformly sampled 1/10 of it to balance tasks and sources.”
- Authors: ruihan-yang; qinxi-yu; yecheng-wu; et al.

### EA-EGOPREC-2026-0081

- Claim: 针对 ego 视频连续相机运动这一误差源，EgoVLA 利用世界系相机位姿将未来腕部位置投影到当前相机系进行监督，以保证监督信号一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2507.12440](https://arxiv.org/abs/2507.12440) EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
- Locator: 3.1 Ego-Centric Human Manipulation Dataset
- Evidence: 3.1 节 Data Processing 段落明确描述该补偿及其动机。
- Quote: “Egocentric videos introduce challenges for learning due to continuous camera motion. To mitigate this, we use world-frame camera poses to project future wrist positions into the current camera frame, ensuring consistent supervision.”
- Authors: ruihan-yang; qinxi-yu; yecheng-wu; et al.

### EA-EGOPREC-2026-0356

- Claim: 在 Masquerade 中，HaMeR 可可靠恢复手型与 2D 关键点位置，但单目输入排除了准确的绝对 3D 姿态估计；由于大规模 in-the-wild 视频没有深度数据(无法像 Phantom 那样用深度精修)，作者只把 2D 关键点位置用作视觉模型的辅助监督标签，而不直接纳入策略学习。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2508.09976](https://arxiv.org/abs/2508.09976) Masquerade: Learning from In-the-wild Human Videos using Data-Editing
- Locator: B. Data processing of in-the-wild egocentric videos
- Evidence: III-B2 明确对比 Phantom 的深度精修，指出无深度时仅将 2D 关键点作辅助损失，不直接进策略学习。
- Quote: “HaMeR reliably recovers hand shape and 2D keypoint locations, its monocular input precludes accurate absolute 3D pose estimation. Unlike [13], which refines HaMeR with depth, our large-scale human videos lack depth data. Therefore, we use the 2D keypoint locations as supervisory labels for an auxiliary loss in our vision model, without in- corporating them directly into policy learning.”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0357

- Claim: Masquerade 通过显式过滤与填补规则控制手部追踪误差进入训练集：丢弃相机运动超过每步 5cm 平移或 0.5rad 旋转的帧及因关键点错误或运动学限制导致动作无效的帧；单手被遮挡或出画时复用该手最后可见帧的动作，全程不可见的手赋予固定'出画'标签，双手均缺失的帧直接丢弃。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2508.09976](https://arxiv.org/abs/2508.09976) Masquerade: Learning from In-the-wild Human Videos using Data-Editing
- Locator: B. Data processing of in-the-wild egocentric videos; C. Additional data-editing details
- Evidence: III-B3 给出无效动作/相机运动过滤原则，Appendix C 给出 5cm/0.5rad 阈值与遮挡复用/丢弃规则。
- Quote: “remove all frames where the estimated camera motion exceeds 5 cm in translation or 0.5 rad in rotation per timestep. To preserve all possible actions and maintain temporal consistency, if a single hand becomes occluded or leaves the frame, its action from the last visible frame in the episode is reused for all subsequent frames. If a hand is invisible for the entire episode, it is assigned a fixed “out-of-frame” action label. Frames in which both hands are missing are discarded.”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0360

- Claim: Masquerade 的重定向管线无法处理 in-the-wild 视频中的所有灵巧抓取，且缺少深度数据使其无法正确处理遮挡(有时机器人像素错误地覆盖在场景物体上)；尽管如此，这些不完美的 overlay 相比完全不用 overlay 仍能大幅提升性能，粗糙的视觉对齐即可显著收益于跨本体迁移。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2508.09976](https://arxiv.org/abs/2508.09976) Masquerade: Learning from In-the-wild Human Videos using Data-Editing
- Locator: B. Data processing of in-the-wild egocentric videos
- Evidence: III-B 末段承认重定向与遮挡处理缺陷，同时声明 imperfect overlay 远优于无 overlay；IV-D 消融证实无 overlay 性能骤降。
- Quote: “While this filtering removes the most problematic cases, many overlays remain imperfect. Our retargeting pipeline cannot handle all dexterous grasps seen in in-the-wild videos, and the absence of depth data prevents correct handling of occlusions, sometimes causing robot pixels to erroneously appear over scene objects. Nevertheless, we show that these imperfect overlays dramatically improve performance compared to using no overlays at all —highlighting how even rough visual alignment can strongl”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0366

- Claim: EMMA 用 Aria MPS 估计的双手 3D 手姿与 3D 头姿(SLAM 世界系)作为人类侧动作数据源；为对齐人与机器人操作动作，先将两者的上身动作块统一变换到观测时刻的相机参考系(人类用 SLAM 估计、机器人用手眼标定)，再承认生物力学与传感器造成的持续分布差距，对变换后的位姿与动作数据按各自数据源独立做 Z-score 归一化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.04443](https://arxiv.org/abs/2509.04443) EMMA: Scaling Mobile Manipulation via Egocentric Human Data
- Locator: A. Data Retargeting and Alignment
- Evidence: III 节确认 MPS 双手 SE(3) 数据源；IV-A 'Aligning Manipulation Action Data' 给出相机系变换与逐源 Z-score 归一化两步。
- Quote: “Aligning Manipulation Action Data. For manipulation, we address mismatches between human hand data (H p ) and robot end-effector data (R p ). Inspired by prior work like EgoMimic [2], we first unify coordinate frames by transform- ing all upper-body action chunks (both human and robot) into the reference frame of the camera at the time of observation, using SLAM estimates for human data and hand-eye cali- bration for robot data. This makes predictions relative to the current view. Second, acknow”
- Authors: lawrence-y-zhu; pranav-kuppili; ryan-punamiya; et al.

### EA-EGOPREC-2026-0367

- Claim: 在 Handover Wine 消融中：去掉运动学重定向(直接执行原始人类导航路径点)成功率下降 30 个百分点，因机器人在执行运动学不可行轨迹时频繁丢失递交对象；去掉相位识别则导致任务完全失败(抓取时基座误动、导航时手臂误动，引发碰撞与掉落)。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.04443](https://arxiv.org/abs/2509.04443) EMMA: Scaling Mobile Manipulation via Egocentric Human Data
- Locator: A. Main Results
- Evidence: Main Results 消融段报告去重定向 -30pp 与去相位完全失败及失败模式；Fig. 9 与之对应。
- Quote: “Without kinematic retargeting, the success rate drops by 30%, as the robot frequently loses track of the human recipient when executing kinematically infeasible trajectories. The phase identification mechanism proves equally crucial—its removal causes complete task failure due to unintended base movements during grasping and unnecessary arm motions during navigation, resulting in collisions and dropped objects.”
- Authors: lawrence-y-zhu; pranav-kuppili; ryan-punamiya; et al.

### EA-EGOPREC-2026-0369

- Claim: EMMA 的无监督相位识别以手部速度/头部速度比为核心信号(阈值 τ_ratio=2.0、τ_head=0.4m/s)，对 10% 人工标注段验证四任务 MoF 均 ≥0.92；部署时的相位感知调制去除了操作阶段头部运动引入的基座动作噪声，保证两相位平滑切换。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.04443](https://arxiv.org/abs/2509.04443) EMMA: Scaling Mobile Manipulation via Egocentric Human Data
- Locator: C. Auxiliary Phase Identification and Control Modulation
- Evidence: IV-C 给出相位算法、阈值选择与 MoF≥0.92 验证，以及相位调制去除 base action noise 的声明。
- Quote: “We empirically selected τ ratio = 2.0, τ head = 0.4m/s, and τ duration = 30 based on the Table Service task. Consistently high MoF scores across tasks (all ≥ 0.92) confirm the system’s robustness to these specific threshold choices.”
- Authors: lawrence-y-zhu; pranav-kuppili; ryan-punamiya; et al.

### EA-EGOPREC-2026-0322

- Claim: RynnVLA-001 的人类轨迹监督不来自视频手部检测器，而来自 EgoDex 数据集中 Apple Vision Pro 设备采集的上肢关节轨迹，且只取腕部关键点（作者明确以其近似末端执行器位置）；模型不回归原始坐标，而是预测由人体专用 ActionVAE 压缩的轨迹块潜嵌入，当前腕部关键点位置另以状态嵌入形式逐帧输入。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.15212](https://arxiv.org/abs/2509.15212) RynnVLA-001: Using Human Demonstrations to Improve Robot Manipulation
- Locator: 3.2 Human-Centric Trajectory-Aware Video Modeling
- Evidence: 3.2 给出 EgoDex/AVP 来源、仅取腕部关键点近似末端位置、预测 ActionVAE 潜嵌入而非原始坐标、腕部状态嵌入四点。
- Quote: “To this end, we adopt the EgoDex dataset (Hoque et al., 2025), which provides trajectories of all upper-body joints captured via Apple Vision Pro devices. Among these, we selectively use only the wrist keypoints, as they approximate end-effector positions.”
- Authors: yuming-jiang; siteng-huang; shengke-xue; et al.

### EA-EGOPREC-2026-0323

- Claim: RynnVLA-001 的 12M ego 视频语料用现成全身姿态估计模型（Yang et al., 2023）逐帧提取面部、躯干与手部关键点（腕、肘、手指），并以两条二元规则过滤：含面部关键点的视频按第三视角线索丢弃，仅保留手腕与手部关键点可见的帧；全程无检测置信度阈值或轨迹级质量门控。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.15212](https://arxiv.org/abs/2509.15212) RynnVLA-001: Using Human Demonstrations to Improve Robot Manipulation
- Locator: 5 EXPERIMENTS / 4 Ego-Centric Video Data Curation Pipeline
- Evidence: 第 4 节数据清洗管线（extraction 并入 5 EXPERIMENTS 表面）给出关键点检测与两条 ego 过滤规则。
- Quote: “For each frame in the video, we apply a pose estimation model (Yang et al., 2023) to extract human keypoints, including facial landmarks, torso joints, and hand-related keypoints (e.g., wrists, elbows, fingers). Ego-centric Filtering. We apply two key filtering criteria to retain only high-quality ego-centric manipulation videos: 1) No facial keypoints: Videos containing facial landmarks are discarded. The appearance of a human face strongly suggests a third-person perspective, which is not suit”
- Authors: yuming-jiang; siteng-huang; shengke-xue; et al.

### EA-EGOPREC-2026-0324

- Claim: 面对『人手轨迹与机器人手臂运动学实质不同』，RynnVLA-001 的域差处理是表征级的：训练两个域专属 ActionVAE（Stage 2 压缩人类轨迹、Stage 3 压缩机器人动作），且 Stage 3 直接丢弃 Stage 2 预训练的人类动作头、重新初始化单层线性头来预测机器人动作嵌入。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.15212](https://arxiv.org/abs/2509.15212) RynnVLA-001: Using Human Demonstrations to Improve Robot Manipulation
- Locator: 3.4 Robot-Centric Vision-Language Action Modeling
- Evidence: 3.4 给出两个域专属 ActionVAE 与丢弃人类动作头两处设计。
- Quote: “Since human hand trajectories differ substantially from robot arm kinematics, the action head pretrained in Stage 2 is discarded.”
- Authors: yuming-jiang; siteng-huang; shengke-xue; et al.

### EA-EGOPREC-2026-0314

- Claim: EgoBridge 的人类动作监督完全来自 Aria MPS 云端服务返回的设备系双手 3D 位置追踪（非自训练检测器、无人工标注）；且由于人类数据只有 3D 位置，BC 损失对人类样本做掩码、仅监督预测中的 3D 位置分量——手部追踪信号对机器人末端姿态与夹爪精度没有直接贡献。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.19626](https://arxiv.org/abs/2509.19626) EgoBridge: Domain Adaptation for Generalizable Imitation from Egocentric Human Data
- Locator: References / Appendix E Embodied human data
- Evidence: 附录 E 描述 MPS 返回设备系双手 3D 位置；附录 B.1.2 描述人类数据仅有 3D 位置故使用掩码损失。（extraction 将附录 A-H 并入 References 区段表面，故用复合定位器。）
- Quote: “The service returns device pose estimated using the SLAM camera, hand tracking relative to the device frame, a semi-dense point-cloud of the environment and eye gaze estimation.”
- Authors: ryan-punamiya; dhruv-patel; patcharapong-aphiwetsa; et al.

### EA-EGOPREC-2026-0326

- Claim: 存在一条不经过手部检测的路线：用 EgoScaler 从纯 RGB ego 视频提取被操纵物体的 6DoF 轨迹（质心+旋转），并将其近似为机器人末端执行器状态（不含夹爪）用于 VLA 预训练，从而完全绕开手部姿态标注对专用硬件的依赖。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: I. INTRODUCTION
- Evidence: 引言明确写出 EgoScaler 轨迹中每个位姿表示被操纵物体质心与旋转、近似为末端执行器状态（排除夹爪），并将该框架应用于 Ego4D/Ego-Exo4D/HD-EPIC/Nymeria 四个数据集。
- Quote: “Each pose in a trajectory rep- resents the centroid and rotation of the manipulated object, approximated as the end-effector states of a robot, excluding the gripper. We apply this framework to four large egocentric video datasets, including Ego4D [22], Ego-Exo4D [23], HD- EPIC [24], and Nymeria [25].”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGOPREC-2026-0443

- Claim: ActiveUMI 以初始标定建立的统一世界坐标系记录绝对坐标位姿，并用三种操作化标定手段保证每次采集的一致初始状态：B 键 in-situ 零点重置（头显内实时渲染坐标轴对齐物理工作区）、夹爪 placeholder 坞站（就位时相对距离与位姿固定为预定义状态，按键即时标定虚拟坐标系原点与朝向）、以及 3cm 零点触觉反馈（接近基座原点时高频振动提示）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: 3.3. Calibrating End-Effector for Precise Data Col-
- Evidence: 3.3 陈述绝对坐标记录与统一世界坐标系（'All data is recorded in absolute co- ordinates relative to a unified world coordinate system that is established during an initial calibration phase'，该句含抽取断词故未用作引文），并依次描述零点重置、坞站与触觉反馈三手段；4.5 的 RPE 结果为其间接效果证据。
- Quote: “This jig can be placed anywhere in the workspace to establish a consistent starting point.”
- Authors: qiyuan-zeng; chengmeng-li; j-drummond-john; et al.

### EA-EGOPREC-2026-0444

- Claim: ActiveUMI 的追踪硬件路径是 Quest 3s 头显 inside-out 追踪：头显 onboard 相机通过追踪控制器集成的红外 LED 图案实时三角测量其 6-DoF 位姿，HMD 的 SLAM 系统同时提供稳定世界坐标系并追踪头部与控制器；控制器刚性挂载到机器人同款夹爪后其位姿直接代表机器人末端位姿，无需 UMI 式的视觉 SLAM 离线重建。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.01607](https://arxiv.org/abs/2510.01607) ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Locator: 3.1. Data Collection System for ActiveUMI
- Evidence: 3.1 'VR gripper controller' 段描述 inside-out 三角测量与刚性挂载代表机器人位姿，并声明误差分析见 4.5；'Head-mounted display (HMD)' 段声明 SLAM 提供稳定世界坐标系并同时追踪头部与控制器（该句在抽取文本中被图 3 文本插断，故未并入引文）。
- Quote: “The headset’s onboard cameras continuously triangulate the controller’s pose in real-time by tracking a unique pattern of integrated infrared (IR) LEDs.”
- Authors: qiyuan-zeng; chengmeng-li; j-drummond-john; et al.

### EA-EGOPREC-2026-0335

- Claim: 在宽域搜索任务上，仅用手部 SE(3)+腕相机的 20D 策略显著落后于加入头部 SE(3) 与头部相机的 29D 策略：桌面任务 29/40 vs 36/40；保留头部图像但固定头部目标时骤降至 2/20；货架任务 0/40 vs 35/40。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.00153](https://arxiv.org/abs/2511.00153) EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations
- Locator: B. Searching Tasks
- Evidence: B. Searching Tasks 报告三组对照的 rollout 计数，并解释 20D 因腕视角场景上下文不完整而在跨工作区协调上失败。
- Quote: “On the tabletop task, the 29D policy achieves a success rate of 36/40, outperforming the 20D wrist camera-only policy, which achieves 29/40. Failure analysis shows that the 20D policy struggles primarily in wide-spanning scenarios requiring hand transfers, often failing to coordinate across the workspace due to incomplete scene context within only the wrist-views. By contrast, the 29D policy leverages the operator’s natural pre-attentive head motion: as operators look toward the placement locati”
- Authors: justin-yu; yide-shentu; di-wu; et al.

### EA-EGOPREC-2026-0337

- Claim: 无显式眼动追踪时，作者用注视点 reticle 约束操作者将目标置于视野中心；定性观察显示无 reticle 训练的策略经常完全失败，作者归因于自由视线漂移使轨迹与观察在部署时出离演示分布。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.00153](https://arxiv.org/abs/2511.00153) EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations
- Locator: B. Operator Gaze and Active Vision Data
- Evidence: B. Operator Gaze and Active Vision Data 末尾报告无 reticle 策略经常完全失败的定性观察及其归因。
- Quote: “Qualitatively, we observe that policies trained without the reticle often fail completely, likely due to free gaze variability and weak head–gaze correlation, which caused trajectories and observations to drift out of the demonstration distribution at deployment.”
- Authors: justin-yu; yide-shentu; di-wu; et al.

### EA-EGOPREC-2026-0400

- Claim: 在双目标定相机下用 HaMeR 检测 2D 手关键点并三角化为末端位姿（抓取点=拇指食指指尖均值）的人演示，朴素协同训练会使扩散策略学到机器人动力学不可行的动作（如侧向抓取），几乎无提升甚至低于纯机器人基线；IK 重放后约 50% 人演示因运动学/动力学失败被人工丢弃；X-DIFFUSION 仅在加噪后人-机动作不可区分的扩散步（分类器判机器人概率≥50% 的最早步 k*）纳入人动作，在 5 个真实任务上平均成功率较跨本体基线高 16% 且超过人工过滤。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.04671](https://arxiv.org/abs/2511.04671) X-Diffusion: Training Diffusion Policies on Cross-Embodiment Human Demonstrations
- Locator: I. INTRODUCTION; III. PROBLEM FORMULATION AND BACKGROUND; V. EXPERIMENTS
- Evidence: III 描述 HaMeR 双目三角化与抓取点定义；V 报告 naive co-training 退化（Point Policy 低于 robot-only）、约 50% 人演示 IK 重放失败被丢弃、FILTERED 优于 NAIVE 而 X-DIFFUSION 全面超过 FILTERED；I 报告较跨本体基线平均 +16%。
- Quote: “While prior approaches that naively co-train on human data may generate infeasible robot actions, selectively training on human actions at high-noise levels improves upon naive co-training and even surpasses manual data filtering. X-DIFFUSION outperforms a range of cross-embodiment learning baselines by an average of 16% in task success.”
- Authors: maximus-a-pace; prithwish-dan; chuanruo-ning; et al.

### EA-EGOPREC-2026-0037

- Claim: 为抵御含噪/不稳定接触的演示，SPIDER 用接触过滤器检测不稳定交互：接触持续时间短于 t_c,min 或接触点漂移超过 d_c,max 时判定为不稳定并禁用对应虚拟约束，使只有可靠接触参与引导，防止含噪演示带偏优化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.09484](https://arxiv.org/abs/2511.09484) SPIDER: Scalable Physics-Informed Dexterous Retargeting
- Locator: 2.3 Virtual Contact Guidance
- Evidence: 2.3 节'Robustness against imperfect reference contact'明确：虚拟约束应选择性松弛，接触过滤器按时长阈值 t_c,min 与漂移阈值 d_c,max 判定不稳定接触并禁用其约束。
- Quote: “contact filter that detects unstable interactions: if a contact duration is shorter than t c,min or if the contact point drifts more than d c,max during that period, the contact is classified as unstable and the corresponding virtual constraint is disabled. 5 This implementation ensures that only reliable contacts contribute to guidance, thereby preventing noisy demonstrations from biasing the optimization process.”
- Authors: chaoyi-pan; changhao-wang; haozhi-qi; et al.

### EA-EGOPREC-2026-0370

- Claim: In-N-On 的 on-task 数据采集刻意选用商用级设备(Apple Vision Pro 与 Meta Aria Glass)，明确理由是'确保 on-task 数据集中的高质量手部姿态'；两款设备均提供头姿、腕姿与稠密指尖关键点预测。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.15704](https://arxiv.org/abs/2511.15704) In-N-On: Scaling Egocentric Manipulation with in-the-wild and on-task Data
- Locator: 3.1. PH
- Evidence: 3.1 节 Data for Post-training 段直述设备选择动机与三款信号(头/腕/指尖)。
- Quote: “To ensure high-quality hand poses in our on-task datasets, we use commercial-grade data collection devices, including Apple Vision Pro and the Meta Aria Glass. Both Vision Pro and Meta Aria glass provide head poses, wrist poses and dense fingertip key- point predictions.”
- Authors: xiongyi-cai; ri-zhao-qiu; geng-chen; et al.

### EA-EGOPREC-2026-0372

- Claim: 朴素人-机数据混合训练的中间特征可被简单 MLP 探针以 100% 成功率区分人类/机器人来源(模型'作弊'式过拟合本体线索)；引入 GRL 域对抗判别器后线性探测降至约 50% 随机水平，且单条机器人演示的 pouring few-shot 组合成功率从 15% 升至 25%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.15704](https://arxiv.org/abs/2511.15704) In-N-On: Scaling Egocentric Manipulation with in-the-wild and on-task Data
- Locator: 3.2. Human; 4.2. Evaluation
- Evidence: 3.2.4 节探针 100% 声明与 Fig. 7 约 50% 结果；Tab. 2 给出 15%/25% 组合成功率。
- Quote: “Tab. 2 demonstrates improved few-shot learning capability. Without a domain discriminator, the model quickly overfits to the single humanoid demonstra- tion.”
- Authors: xiongyi-cai; ri-zhao-qiu; geng-chen; et al.

### EA-EGOPREC-2026-0301

- Claim: METIS/EgoAtlas 的手部与腕部轨迹监督不依赖对 ego 视频的视觉手部检测，而来自传感式动捕管线：自采数据用 Manus Quantum 手套记录每手 25 个关键点 3D 位置、VIVE Tracker 提供 6-DoF 腕部位姿，其余来源为多目光学动捕、VR 设备 SLAM 与遥操作机器人数据；作者明确将『对遮挡与视觉歧义鲁棒』列为自采传感数据的首要收益。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.17366](https://arxiv.org/abs/2511.17366) METIS: Multi-Source Egocentric Training for Integrated Dexterous Vision-Language-Action Model
- Locator: 3.1. Wearable System for Enhanced Human Data
- Evidence: 3.1 描述手套+tracker 采集系统并批评视觉/多目方案的视角依赖与遮挡；3.2 列出四类来源并把鲁棒性列为增强数据第一项收益。
- Quote: “We use Manus Quantum Metagloves to record precise 3D positions of hand keypoints, with 25 keypoints per hand. A VIVE Tracker mounted on each glove provides the 6-DoF wrist pose,”
- Authors: yankai-fu; ning-chen; junkai-zhao; et al.

### EA-EGOPREC-2026-0302

- Claim: 为跨本体统一动作空间，METIS 将腕部位姿（18D：3D 位置+6D 旋转）统一表达到 ego 相机坐标系、将手部（30D）表达为腕坐标系下的指尖 3D 位置；推理时策略预测指尖目标再经 IK 回到关节角，人与机器人腕系通过标定对齐，因此 ego 相机-腕部外参标定是轨迹从人传到机器人的必经误差环节。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.17366](https://arxiv.org/abs/2511.17366) METIS: Multi-Source Egocentric Training for Integrated Dexterous Vision-Language-Action Model
- Locator: 3.3. Data Processing
- Evidence: 3.3 逐句描述统一动作空间构造与 FK/IK 互转；附录 A 给出三 tracker 标定流程。
- Quote: “we construct a unified action space that bridges the gap between human and robot motion representations. For the wrist pose (18 dim), we unify all representations into the ego-camera coordinate frame, which consists of a 3D position and a 6D rotation vector. For the hand (30 dim), we calibrate the motion to the wrist coordinate frame, using the 3D positions of each fingertip. Dexterous hand’s joint angles can be mapped to fingertip positions through forward kinematics (FK).”
- Authors: yankai-fu; ning-chen; junkai-zhao; et al.

### EA-EGOPREC-2026-0538

- Claim: DexWM 的手部动作监督完全建立在 ego 数据集自带的自动标注之上：EgoDex 提供每只手 25 个 3D 关键点、相机内外参与全部姿态估计的置信度分数，论文未报告额外人工校正或按置信度过滤。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.13644](https://arxiv.org/abs/2512.13644) World Models for Learning Dexterous Hand-Object Interactions from Human Videos
- Locator: Appendix
- Evidence: 附录 C.2 说明 EgoDex 标注构成（3D 骨架、25 关键点/手、置信度）；3.1 节说明多数 ego 数据集已含手部关键点标注，DexWM 直接使用。
- Quote: “EgoDex provides rich multimodal annotations, in- cluding 3D skeletal poses for the upper body and 25 keypoints per hand, camera intrinsics and extrinsics, and confidence scores for all pose estimates.”
- Authors: raktim-gautam-goswami; amir-bar; david-fan; et al.

### EA-EGOPREC-2026-0539

- Claim: PhysBrain 的 ego→物理桥梁不依赖显式手部 3D 姿态或腕部轨迹标注：监督来自把 ego 视频翻译为 7 种 schema 模式（temporal/spatial/attribute/mechanics/reasoning/summary/trajectory）的语言化 VQA，姿态与接触信息以语言形式承载。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.16793](https://arxiv.org/abs/2512.16793) PhysBrain: Human Egocentric Data as a Bridge from Vision Language Models to Physical Intelligence
- Locator: 3.1 Egocentric2Embodiment Translation Pipeline
- Evidence: 3.1.2 节明确每个 clip 按 7 种互补 VQA 模式之一标注；全管线无 3D 姿态/关键点监督的使用，4 节动作专家仅从 VLM hidden states 条件化。
- Quote: “Each clip is labeled with one of seven complementary VQA modes, including temporal, spatial, attribute, mechanics, reasoning, summary, and trajectory.”
- Authors: xiaopeng-lin; shijie-lian; bin-yu; et al.

### EA-EGOPREC-2026-0544

- Claim: 仅用 E2E ego 语言监督做 SFT（不含任何 SAT 任务样本）即可把 VST 的 SAT 总分从 45.33 提升到 59.33、Egocentric Movement 子项从 26.09 提升到 91.30，但 Object Movement 子项反而从 39.13 降到 34.78，增益集中在 ego 运动与动态空间推理而非均匀提升。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.16793](https://arxiv.org/abs/2512.16793) PhysBrain: Human Egocentric Data as a Bridge from Vision Language Models to Physical Intelligence
- Locator: 5.1 VLM Egocentric Evaluation; Method
- Evidence: 5.1.2 节 SAT 互补评估：E2E-only SFT 后总分 45.33→59.33、Egocentric Movement 26.09→91.30、Action Consequence 54.05→64.86、Perspective 39.39→48.48，而 Object Movement 39.13→34.78、Goal Aim 不变。
- Quote: “After fine-tuning on E2E dataset, overall accuracy increases to 59.33, while Egocentric Movement improves markedly to 91.30.”
- Authors: xiaopeng-lin; shijie-lian; bin-yu; et al.

### EA-EGOPREC-2026-0526

- Claim: WIYH 的 Oracle Suite 自动标注管线（IR+RGB+IMU 融合）输出的手腕轨迹在动捕室受控验证中取得平均约 5mm 的位置误差，作者以此作为数据集动作标注的精度验收依据。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.24310](https://arxiv.org/abs/2512.24310) World In Your Hands: A Large-Scale and Open-source Ecosystem for Learning Human-centric Manipulation in the Wild
- Locator: 2.2 Data Validation System
- Evidence: 2.2 节明确给出动捕室对比测试：Oracle Suite 轨迹与动捕轨迹的平均位置误差 5mm；图 3 说明此为受控实验室环境下的平均平移误差。
- Quote: “Our Oracle Suite achieves an average position error of 5 mm in the motion capture room environment.”
- Authors: tars-robotics; yupeng-zheng; jichao-peng; et al.

### EA-EGOPREC-2026-0529

- Claim: 作者明确指出人类中心数据的运动精度是有限的，其下游收益来自动作分布的多样性而非精度：多样性增强了策略对未见初始状态的泛化能力。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2512.24310](https://arxiv.org/abs/2512.24310) World In Your Hands: A Large-Scale and Open-source Ecosystem for Learning Human-centric Manipulation in the Wild
- Locator: 5.2 Results and In-depth Discussion
- Evidence: 5.2 节结果讨论中作者直接陈述：尽管人类中心数据运动精度有限，其多样动作分布增强了对未见初始状态的泛化。
- Quote: “Although the motion precision in the human-centric data is limited, its diverse action distribution en- hances the policy’s generalization capability to unseen initial states.”
- Authors: tars-robotics; yupeng-zheng; jichao-peng; et al.

### EA-EGOPREC-2026-0411

- Claim: 作者指出：对于手部被遮挡的随机人体运动或高速运动变化，需要更高级的传感配置——如触觉与 SLAM 技术——来补偿估计误差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.10106](https://arxiv.org/abs/2602.10106) EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
- Locator: A. Motivating Questions
- Evidence: 附录 A Q5 局限讨论中提出触觉+SLAM 补偿估计误差的方向。
- Quote: “Random human motion with occluded hands or high-speed motion changes would require more advanced sensor setups, such as tactile and SLAM techniques, to compensate for the estimation error.”
- Authors: modi-shi; shijia-peng; jin-chen; et al.

### EA-EGOPREC-2026-0390

- Claim: 抓握失败主要源于物体位姿估计误差（如 Pan 的手柄被人手严重遮挡）与力闭合缺失；为每个失败物体追加 2 条不同视角/抓握风格的视频后，5 个失败物体成功率从 8.6% 升至 40.8%，总体从 63.75% 升至 70.25%，说明遮挡引起的重建失败可用多视角数据多样性部分对冲。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.09013](https://arxiv.org/abs/2602.09013) Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
- Locator: A. Grasping Experiments
- Evidence: IV-A 失败归因 + Table I 多视频消融。
- Quote: “These failures pri- marily stem from object pose estimation errors, for example in the Pan case where heavy occlusion of the handle by the human hand leads to inaccurate pose estimation, and from a lack of force awareness, in which grasps for the Glasses Case and Hand Bag are kinematically plausible but fail to achieve force closure, resulting in instability. To mitigate these issues, we examine whether incorporating grasping videos with diverse viewpoints and grasp styles improves performance.”
- Authors: hongyi-chen; tony-dong; tiancheng-wu; et al.

### EA-EGOPREC-2026-0404

- Claim: 以 HaMeR 单目手部轨迹共同训练 + 仅 10-20 条机器人遥操作轨迹即可达到 0.88 平均得分，远超纯机器人 10 条 (0.26) 与 20 条 (0.51) 基线。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.11464](https://arxiv.org/abs/2602.11464) EasyMimic: A Low-Cost Framework for Robot Imitation Learning from Human Videos
- Locator: B. Main Results
- Evidence: Table II 与正文：EasyMimic 平均 0.88，Robot-Only 10/20 条分别 0.26/0.51；数据规模分析显示 50 条人类视频 + 10-20 条机器人轨迹即足够。
- Quote: “Our EasyMimic framework achieves the best performance across all tasks, with an average score of 0.88, surpassing the Pretrain-Finetune method by 0.13 points and the Robot- only (10 trajectories) baseline by 0.62 points.”
- Authors: tao-zhang; song-xia; ye-wang; et al.

### EA-EGOPREC-2026-0305

- Claim: EgoScale Stage I 的腕部与手部轨迹监督直接来自对 20,854 小时 in-the-wild ego 视频施加的现成 SLAM 与手部姿态估计管线，作者明确承认这些估计因无约束采集而是噪声的，但主张数据规模与多样性仍提供有效监督，且下游性能随数据量持续提升。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 2.2. Human Data Sources and Processing
- Evidence: 2.2 原文逐句给出估计管线来源、噪声坦承与规模补偿主张；3.3 规模律实验为该主张提供结果支持。
- Quote: “We apply off-the-shelf SLAM and hand-pose estimation pipelines to recover camera motion and human hand trajectories. Although these estimates are noisy due to unconstrained data collection, the scale and diversity of the data provide effective supervision”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-EGOPREC-2026-0308

- Claim: 预训练手部动作表示消融显示：wrist-only 表示在所有任务上表现差（尤其在需要精细手指关节与接触时序的任务）；指尖 SE(3) 表示虽提供更丰富几何监督但不一致——指尖姿态的小误差经 MLP 映射后常产生不可行的关节配置，导致 Card/Bottle 等接触敏感任务中抓取不稳或接触丢失；经优化重定向（关节限位+运动学约束+指数平滑）的关节空间表示在所有任务上最一致。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.16710](https://arxiv.org/abs/2602.16710) EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
- Locator: 3.6. Hand Action Space Design for Human Pretraining
- Evidence: 3.6 逐句描述三种表示的对比结果与指尖误差→不可行关节配置的失败模式；附录 D 描述优化重定向与指数平滑。
- Quote: “Small errors in fingertip pose often lead to implausible joint configurations after mapping, causing unstable grasps or contact loss in contact-sensitive tasks such as Cards and Bottle. In contrast, pretraining with retargeted joint-space hand actions yields the most consistent performance across all tasks.”
- Authors: ruijie-zheng; dantong-niu; yuqi-xie; et al.

### EA-EGOPREC-2026-0475

- Claim: 在 Unitree G1 人形真机上，50 条遥操作加 200 条 AoE 人类视频使 Close Laptop 成功率 45%→95%、Push Bowl & Pour Seeds 0%→20%（PSR 30%→48%）、Pick&Place 45%→75%；但 Fold Scarf 维持 10% 不变，作者归因于硬件时延阻碍可形变物体所需的高频反应控制。策略学习走 FLARE 未来潜变量对齐，不使用重建轨迹作动作标签。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.23893](https://arxiv.org/abs/2602.23893) AoE: Always-on Egocentric Human Video Collection for Embodied AI
- Locator: 4.3. Real-World Evaluation on Humanoid Hardware; 7.4. Experiment Setups
- Evidence: Table 2 与 4.3.1 给出四任务 SR/PSR 对比与 Fold Scarf 归因；7.4 说明 FLARE 训练只用未来潜变量对齐损失 + 遥操作动作流匹配损失。
- Quote: “Notably, in Close Laptop, adding AoE data boosts SR from 45.0% to 95.0%. In the challenging Push Bowl & Pour Seeds task, where the baseline fails (0% SR), AoE inclusion enables a 20.0% SR and increases PSR from 30.0% to 48.0%.”
- Authors: bowen-yang; zishuo-li; yang-sun; et al.

### EA-EGOPREC-2026-0497

- Claim: CDF-Glove 的绳驱力反馈响应时间约 200ms，作者将其归因于 RS485 串行通信瓶颈与绳驱伺服的机械响应时间，并明确划定可接受边界：该延迟对高速交互偏高，但对数据集内的准静态操作任务是足够的。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.05804](https://arxiv.org/abs/2603.05804) CDF-Glove: A Cable-Driven Force Feedback Glove for Dexterous Teleoperation
- Locator: A. CDF-Glove Performance Validation
- Evidence: V.A.2 逐字给出 200ms 测量值、RS485+伺服的归因与『高速偏高/准静态足够』的边界陈述。
- Quote: “The experimental results indicate that the response time for cable-driven force feedback, based on current information from the RY-H1, is nearly 200 ms. The 200 ms force-feedback latency is primarily attributed to the serial communication bottleneck (RS485) and the mechanical response time of the cable-driven servos. While relatively high for high-speed interactions, it proved sufficient for the quasi-static manipulation tasks in our datasets.”
- Authors: huayue-liang; ruochong-li; yaodong-yang; et al.

### EA-EGOPREC-2026-0022

- Claim: 在相同仿真设定（20 条演示/任务、每任务 200 次 rollout）下，将 3D 点轨替换为 2D 点轨（并换用 2D 图像编码器）使平均成功率从 64.9% 降至 35.8%，逐任务为 35.0/26.5/44.0/37.5% vs 66.0/51.0/67.5/75.0%，说明带深度的 3D 提升对点轨表征的下游策略效用有实质贡献。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: Appendix F Additional Ablation Results, Table 5 (extraction section '20 Robot Demos')
- Evidence: Figure 4 报告消融平均成功率（2D Point Tracks 35.8 vs 3PoinTr 64.9），Appendix F Table 5 给出逐任务数值；消融同时更换了图像编码器（DP 的 2D encoder 替代 DP3 的 3D encoder）。
- Quote: “Task 2D Point Tracks No Perceiver-IO No U-Net Xattn No Extra Videos 3PoinTr Block Stack 35.0 24.5 56.0 69.0 66.0 Right Glass 26.5 25.0 41.0 19.5 51.0 Pot Lid 44.0 55.5 62.5 57.5 67.5 Open Microwave 37.5 29.0 70.0 60.0 75.0”
- Authors: adam-hung; bardienus-p-duisterhof; jeffrey-ichnowski

### EA-EGOPREC-2026-0029

- Claim: 把检测器从 MediaPipe 换成 WiLoR 只能部分缓解遮挡失效：347 帧结构化 ego 录制上，检出率 62.8%→67.7%（+7.8%），无检测率 37.2%→32.3%，有效 IK 目标率 59.9%→64.8%（+8.2%），仅 3.5% 的帧被 WiLoR 挽回；两个检测器在'检出→有效 IK 目标'的转换率上都超过 95%（95.4%/95.7%），作者据此确认瓶颈是手部检测本身而非 IK 目标计算。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.11383](https://arxiv.org/abs/2603.11383) Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics
- Locator: VI-L. Occlusion Mitigation via WiLoR
- Evidence: Table VII 给出两检测器的检出/有效目标/无检测三行与 +7.8%/+8.2%/3.5%；VI-L 正文给出 95%+ 转换率与瓶颈归因。
- Quote: “Metric MediaPipe WiLoR Hand detected 218 (62.8%) 235 (67.7%) Valid IK target 208 (59.9%) 225 (64.8%) No detection 129 (37.2%) 112 (32.3%) Recovery (WiLoR found, MP missed) 12 frames (3.5%) Detection improvement +7.8% Valid target improvement +8.2%”
- Authors: hendrik-chiche; antoine-jamme; trevor-rigoberto-martinez; et al.

### EA-EGOPREC-2026-0030

- Claim: 该管线的 IK 解算环节引入的末端位置误差为均值 36.4mm（std 2.5mm、max 43.3mm，N=125 帧），约为 SO-ARM101 臂展（约 300mm）的 12%，作者判定对 50×50mm 方块的抓取任务可接受；姿态误差高达 163.4°，但源于 5-DOF 机械臂无法满足 6-DOF 目标的结构性折中（解算优先保位置），而非追踪噪声。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.11383](https://arxiv.org/abs/2603.11383) Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics
- Locator: VI-E. IK Solver Accuracy
- Evidence: VI-E 给出 36.4mm（std 2.5/max 43.3，分轴 X18.4/Y18.2/Z22.7）与 163.4° 及 5-DOF 约束解释；作者给出 12% 臂展与可接受性判断。
- Quote: “The mean position error ∥FK(q ∗ ) − p target ∥ is 36.4 mm (std 2.5 mm, max 43.3 mm), distributed approximately equally across axes (X: 18.4 mm, Y: 18.2 mm, Z: 22.7 mm). The mean orientation error is 163.4 ◦ (std 5.6 ◦ ), reflecting the fundamental constraint of a 5-DOF kinematic chain attempting to reach a 6-DOF target: because only 5 arm joints contribute to end-effector positioning, the solver cannot independently satisfy both position and orientation and must compromise, prioritising positio”
- Authors: hendrik-chiche; antoine-jamme; trevor-rigoberto-martinez; et al.

### EA-EGOPREC-2026-0462

- Claim: DexEXO 的 pose-tolerant 拇指耦合给外骨骼相对手掌留出四维自运动流形，捏取姿态下实测 wiggle space 拟合椭球半轴达 66.12/49.19/21.14 mm：操作者手与外骨骼之间可发生厘米级相对运动而不改变被动手（即被编码器测量并重定向的手）的姿态。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.17323](https://arxiv.org/abs/2603.17323) DexEXO: A Wearability-First Dexterous Exoskeleton for Operator-Agnostic Demonstration and Learning
- Locator: A. Experimental Validation of Thumb Wiggle Space
- Evidence: III-D 推导两连杆耦合只施加两个标量约束、残余四维自运动；V-A 用动捕约 25 s 采样拟合出三半轴长度。
- Quote: “The fitted ellipsoid has semi-axis lengths of 66.12 mm, 49.19 mm, and 21.14 mm.”
- Authors: alvin-zhu; mingzhang-zhu; beomdo-kim; et al.

### EA-EGOPREC-2026-0463

- Claim: DexEXO 的手指数据链为六个模拟编码器 1 kHz 采样、刚性防 backlash 结构，并经同姿态逐点采样的分段线性插值映射到 ROHand 执行器；末端 6 自由度位姿由 iPhone ARKit 采集重采样至 60 Hz，各模态以视频时间戳做最近邻软件对齐。全文未报告 ARKit 位姿精度或时间对齐误差数值。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.17323](https://arxiv.org/abs/2603.17323) DexEXO: A Wearability-First Dexterous Exoskeleton for Operator-Agnostic Demonstration and Learning
- Locator: A. Data Collection
- Evidence: IV-A 逐项描述编码器 1 kHz、ARKit 60 Hz 重采样与最近邻时间对齐；III-B 描述防漂移刚性结构；全文检索无 ARKit 精度或同步误差数值。
- Quote: “Asynchronous encoder and pose measurements are matched via nearest-neighbor association.”
- Authors: alvin-zhu; mingzhang-zhu; beomdo-kim; et al.

### EA-EGOPREC-2026-0467

- Claim: DexViTac 的采集效率超过 248 条/小时（四任务平均 14.5 s/条），显著高于传统遥操作的 84 条/小时（112.3 s/条），接近自然人手的 275 条/小时（13.1 s/条）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.17851](https://arxiv.org/abs/2603.17851) DexViTac: Collecting Human Visuo-Tactile-Kinematic Demonstrations for Contact-Rich Dexterous Manipulation
- Locator: C. Data Collection Efficiency
- Evidence: IV-C 与图 7 给出三方案每示教时长与吞吐对比；结论节另写『exceeding 100 demos/hour』与摘要/正文不一致，按正文 248 为准。
- Quote: “the data collection efficiency of our system ex- ceeds 248 demos/hour, which is significantly higher than the 84 demos/hour of teleoperation and approaches the 275 demos/hour efficiency of natural human hands”
- Authors: xitong-chen; yifeng-pan; min-li; et al.

### EA-EGOPREC-2026-0489

- Claim: 用 TeleDex 采集的 120 条仿真演示训练无任务特定修改的 vanilla CNN+MLP 行为克隆策略，在水果顺序抓放任务上 20 次评估达 80%（16/20）成功率，作者据此认为 TeleDex 演示质量足以支持模仿学习。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.17065](https://arxiv.org/abs/2603.17065) TeleDex: Accessible Dexterous Teleoperation
- Locator: E. Policy Training
- Evidence: IV.E 报告 120 条演示、RGB+本体感知观测、vanilla CNN+MLP、80%（16/20）成功率及作者的充分性结论。
- Quote: “The trained policy achieves a success rate of 80% (16/20) over 20 evaluation episodes, demonstrating that demonstrations collected with TeleDex are of sufficient quality to enable effective imitation learning, even with a simple baseline model and a relatively modest dataset size.”
- Authors: omar-rayyan; maximilian-gilles; yuchen-cui

### EA-EGOPREC-2026-0457

- Claim: UMI-Aquatic 的自动标注链以 AprilTag 追踪估计夹爪开合宽度，用滑窗变点检测（陡降后平台）确定闭合时刻 t*，再从闭合帧用 CoTracker3 点追踪向早期帧回追夹爪-物体接触像素，生成每帧 affordance 关键点监督；该标签质量完全依赖闭合时刻检测与点追踪的准确性，但论文未对标注链精度作任何量化评估。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.27012](https://arxiv.org/abs/2603.27012) UMI-Underwater: Learning Underwater Manipulation without Underwater Teleoperation
- Locator: C. Goal-Conditioned Data Preprocessing and Training
- Evidence: III-C-b 与 Fig. 6 描述标注链：AprilTag 宽度信号→滑窗检测 t*→CoTracker3 回追接触像素 (u_t, v_t)；全文未报告检测或回追的误差率。
- Quote: “we use an AprilTag-based gripper tracking pipeline (Fig. 6) to estimate gripper openness/width and to determine the grasp/contact timing in the camera frame.”
- Authors: hao-li; long-yin-chung; jack-goler; et al.

### EA-EGOPREC-2026-0062

- Claim: 在帧对齐跟踪相机采集的人手输入下，启用 CBF 安全约束时超过 95% 的控制步碰撞安全分数高于 0.8（阈值 D_safe=0.01m，激活距离 0.011m），仅个别帧因离散控制与系统时延出现毫米级阈值违例；去除安全项的消融中安全分数频繁跌破阈值。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.29213](https://arxiv.org/abs/2603.29213) Kilohertz-Safe: A Scalable Framework for Constrained Dexterous Retargeting
- Locator: B. Simulation Evaluation
- Evidence: IV-B 安全分析段落与 Fig.5 消融说明直接给出 >95%/0.8 的定量结论、毫米级违例归因（离散控制与时延）以及 0.01m/0.011m 的参数设定。
- Quote: “Quantitatively, more than 95% of control steps achieve a safety score above 0.8, indicating sustained collision clearance without sacrificing real-time performance or motion fidelity.”
- Authors: yinxiao-tian; ziyi-yang; zinan-zhao; et al.

### EA-EGOPREC-2026-0384

- Claim: 仅用单目 RGB ego 人类视频，经手-物联合优化与手腕对齐渲染训练的扩散策略在 5 个桌面任务上达到与遥操作相当的成功率（如 Rotate Box 20/20 vs 16/20），而没有准确手-物几何的 Alter 基线全面失败（0-8/20），说明手-物轨迹/几何重建精度是此类管线政策可用性的决定因素。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.10809](https://arxiv.org/abs/2604.10809) WARPED: Wrist-Aligned Rendering for Robot Policy Learning from Egocentric Human Demonstrations
- Locator: D. Results (Table I)
- Evidence: Table I 真机成功率；正文明确指出 Alter 失败是因为缺少准确手-物几何。
- Quote: “Teleoperation 16/20 19/20 16/20 15/20 19/20 Alter (Heng et al.) 7/20 3/20 0/20 0/20 8/20 WARPED (no augmentation) 0/20 17/20 0/20 0/20 8/20 WARPED (background distractors) 18/20 15/20 17/20 9/20 17/20 WARPED 20/20 18/20 17/20 11/20 17/20 Teleoperation + WARPED 19/20 20/20 17/20 11/20 20/20”
- Authors: harry-freeman; chung-hee-kim; george-kantor

### EA-EGOPREC-2026-0506

- Claim: 综述的路线选择指南指出：affordance 迁移在 HOI 解析不可靠时失效——原因包括遮挡、相机运动、物体重建误差与严重形态失配；并且在力、柔顺性或接触稳定性无法仅从视觉推断时同样吃力。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.27621](https://arxiv.org/abs/2604.27621) Robot Learning from Human Videos: A Survey
- Locator: 32 Journal Title XX(X)
- Evidence: Tab.9 中 affordance-based action transfer 行的'When it tends to fail'栏明确列出上述条件。
- Quote: “It fails when HOI parsing is unreliable because of occlusion, camera motion, object reconstruc- tion errors, or severe morphology mismatch. It also struggles when force, compliance, or contact stability cannot be inferred from vision alone.”
- Authors: ma-et-al-shanghai-jiao-tong-university-university-of-cambridge-corresponding-hesheng-wang

### EA-EGOPREC-2026-0257

- Claim: 残差 EMG+vision 融合在全部匹配轻量视觉基线上一致降低关节角误差（RN18 5.9→5.4°、ViT-S 6.0→5.5° avg），且遮挡分级分析显示手部自遮挡程度与融合增益正相关；但当前融合仅超过轻量通用骨干——手部专用 WiLoR 纯视觉（4.7°）仍强于全部融合基线，EMG 能否增益专用视觉模型是作者明示的开放问题。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.05712](https://arxiv.org/abs/2605.05712) EgoEMG: A Multimodal Egocentric Dataset with Bilateral EMG and Vision for Hand Pose Estimation
- Locator: 5.2 Vision-to-Pose Results
- Evidence: Table 3 融合行 vs 匹配视觉行；5.2 正文给出'consistently improves'、遮挡-增益正相关与 WiLoR 仍更强三要点。
- Quote: “Fusion consistently improves over matched lightweight generic vision-only baselines across all backbone families and splits. The improvement is largest on the gesture split, while user-split gains are smaller, suggesting that EMG is particularly informative for fine articulation but remains affected by inter-subject variability. At the same time, V-WiLoR remains stronger than the current lightweight fusion baselines, indicating that the next benchmark milestone is to test whether EMG also improv”
- Authors: ziheng-xi; jiayi-yu; yitao-wang; et al.

### EA-EGOPREC-2026-0545

- Claim: 消费级 iPhone Pro 的 ARKit 视觉惯性里程计对 30 相机 Vicon 动捕真值的轨迹精度为：9/10 序列相对 ATE 低于 1%、平移 RPE 全程低于 5cm、旋转 RPE 低于 4°，唯一例外是快速旋转序列；作者据此判断其足以锚定世界系手部姿态。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: IV. DATA QUALITY VALIDATION
- Evidence: IV-A1 表 II 报告 10 条序列的 ATE RMSE/相对 ATE/RPE；正文总结 9/10 相对 ATE<1%、平移 RPE<5cm、旋转 RPE<4°，快速旋转序列例外。
- Quote: “Relative ATE stays below 1% for nine of the ten sequences and rotational RPE below 4”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathor; et al.

### EA-EGOPREC-2026-0549

- Claim: MobileEgo 数据作为训练信号的下游验证：VITRA-VLA-3B mid-training 后 held-out 手部动作预测损失从 0.265 降到 0.214（-19%），降幅集中在手指关节（-24%）而非腕根（-14%）；未训练模型因尺度失配 best-of-10 腕部误差 554mm，mid-training 校准到 70mm。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: V. TRAINING SIGNAL VALIDATION
- Evidence: V 节：held-out 损失单调降 0.265→0.214；手指 -24%、腕根 -14%；未训练 554mm→mid-trained 70mm（best-of-10，100 held-out clips）。
- Quote: “its predictions are mis-scaled, giving a best-of-10 wrist error of 554 mm, whereas mid-training calibrates it to our distribution (70 mm; Fig. 3b)”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathor; et al.

### EA-EGOPREC-2026-0013

- Claim: 固定同一 2D 骨干时，2D 检测到 3D 姿态的融合/提升（lifting）策略独立决定最终 3D 误差：朴素三角化 79.21mm，引入相机内外参的参数调制类方法 53.49-121.74mm，跨视角交叉注意力匹配 42.98mm，几何感知 BEV 融合（KeypointBEV）30.54mm——最好与最差策略相差 4 倍，且任何仅在 2D 域融合的方法都无法突破 42.98mm。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.12297](https://arxiv.org/abs/2605.12297) EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras
- Locator: V-F. Ablation Study, Table III
- Evidence: Table III 七种融合实现同表对比；V-F 正文解释 PM 类受深度歧义约束、CM 类缺几何约束的失效机制。
- Quote: “Method Input Implementation M-3D↓ Baseline 2D Coord. Triangulation 79.21 Direct-3D Heat. + I/E Params. PM → Absolute 3D 121.74 Coarse-3D (H) Heat. + I/E Params. PM → Relative 3D 112.62 Coarse-3D (F) Feat. + I/E Params. PM → Relative 3D 87.68 Fine-2D Feat. + I/E Params. PM → 2D Residual 53.49 Fine-2D Cross-attn. Feat. (Stereo) CM (No Params.) 42.98 KeypointBEV BEV Feat. Geo-aware Fusion 30.54”
- Authors: luming-wang; hao-shi; jiajun-zhai; et al.

### EA-EGOPREC-2026-0042

- Claim: 在接触丰富的扭转任务中，小的运动学误差在人-机器人本体差距下会被放大为功能失效：直接姿态模仿产生沿物体表面的切向指尖滑动而非绕预期轴的旋转，表现为螺丝轴漂移、接触滑移与三指稳定性丧失。DexTwist 的缓解是把目标从几何相似换成功能保持：捏合激活后估计操作者螺丝轴与累积扭转意图，用定义在机器人三指几何上的虚拟物目标（转角跟踪+指尖闭合+轴一致+质心稳定四项正则）做实时有界残差关节精修。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.12182](https://arxiv.org/abs/2605.12182) DexTwist: Dexterous Hand Retargeting for Twist Motion via Mixed Reality-based Teleoperation
- Locator: B. Hand Functional Retargeting
- Evidence: III-B 开篇明确：常规重定向目标强调几何相似，接触扭转中小运动学误差在本体差距下表现为切向滑移、轴漂移与三指失稳；同节给出功能化替代：迟滞门激活、螺丝轴（式 5）与累积转角（式 6）估计、虚拟物目标（式 8）与每周期 5 次有限差分迭代的有界残差精修。
- Quote: “Conventional hand retargeting objectives emphasize geo- metric similarity (e.g., joint angles or fingertip positions). For contact-rich twisting, however, small kinematic errors under embodiment mismatch often manifest as tangential slip, axis drift, and loss of tripod stability.”
- Authors: dongmyoung-lee; chengxi-li; dongheui-lee

### EA-EGOPREC-2026-0011

- Claim: 将 root-relative 手部姿态提升到相机系的方式决定绝对轨迹误差：同一 HALO 预测经朴素深度提升到 H2O/HOT3D 产生 530.5/1851.9mm 误差与 41.9/180.4 m/s² 加速度误差，经 DGP 为 25.0/115.6mm，经射线空间求解（RSS）为 25.0/45.8mm，RSS+Kalman 滤波进一步将 CS-ACC 从 23.5 降至 14.0 m/s²。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.12498](https://arxiv.org/abs/2605.12498) EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera
- Locator: 9.2 Ablations, Table 9
- Evidence: Table 9 消融四种提升方式；9.2 正文明确朴素深度提升在单目尺度歧义下失效并给出全部数值。
- Quote: “The naïve depth-based lifting, similar to HaMeR D ’s metric- depth formulation, fails under monocular scale ambiguity, yielding large translation errors (530.5/1851.9 𝑚𝑚) and correspondingly high acceleration errors (41.9/180.4 𝑚/𝑠 2 ). On H2O, our Ray Space Solver (RSS) and DGP from Valassakis and Garcia-Hernando [2024] achieve the same CS-MJE of 25 𝑚𝑚 with nearly identical CS-ACC (7.4 𝑚/𝑠 2 ), indicating that both correctly exploit the pinhole projection con- straints. On HOT3D, however, DGP r”
- Authors: christen-millerdurai; shaoxiang-wang; yaxu-xie; et al.

### EA-EGOPREC-2026-0073

- Claim: 固定演示权重会被低成本演示中的噪声带偏：在相同数据、奖励、预算与 PPO 配置下，接触奖励驱动的动态演示退火将平均成功率从 23.5% 提升到 36.5%（相对 +55.3%）；作者明确归因于“固定演示权重易受低成本演示噪声影响”。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.03268](https://arxiv.org/abs/2606.03268) EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations
- Locator: 4.3 Ablation Study on Dynamic Demonstration Annealing
- Evidence: 4.3 消融原文同时给出 23.5%→36.5%（+55.3%）的定量对比与“fixed demonstration weights are prone to being affected by noise in low-cost demonstrations”的机理归因。
- Quote: “Compared to the fixed-weight setting, our method increases the average success rate from 23.5% to 36.5%, a relative improvement of 55.3%. This demonstrates that fixed demonstration weights are prone to being affected by noise in low-cost demonstrations, whereas dynamic annealing retains demonstration guidance during early training and gradually re- leases it as the policy achieves stable contact behaviors, thereby improving task success rates.”
- Authors: qian-zhao-217607; xin-tong; chengdong-wu; et al.

### EA-EGOPREC-2026-0374

- Claim: 当前 SOTA 单目手部估计器(HaWoR)的标签虽已越过'有迁移'门槛但远未追平高质量标签：同 532 条视频上 HaWoR 单目手部共训练均值 24.7±16.9%，仍高于纯机器人训练 11.9%，却显著低于三角测量手部的 41.5±12.1%——手部质量差距在该设置下对应约 17pp 的成功率差。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06627](https://arxiv.org/abs/2606.06627) What Matters When Cotraining Robot Manipulation Policies on Everyday Human Videos?
- Locator: 6 Results
- Evidence: 6 Results 'Hand quality matters' 段逐字给出 24.7% vs 11.9% 对比与'even noisy hand labels provide some benefit'判断；41.5% 来自 Tab. 1 Ours 行。
- Quote: “However, the mean success rate for HaWoR is still higher than Robot Only (24.7% vs 11.9%) (Table 2). This indicates even noisy hand labels provide some benefit across certain tasks but greater improvements in hand pose estimation quality will unlock better transfer across other tasks.”
- Authors: richard-li; aditya-prakash; andrew-wen; et al.

### EA-EGOPREC-2026-0375

- Claim: 即使手部标签达到三角测量级质量，自然动作鸿沟下实验室共训练设计仍失效：CLS-token 图像瓶颈均值仅 14.7±18.6%、PiZero 式共享动作编解码器 17.5±6.0%、EgoBridge 动作相似性对齐 16.6±10.7%，而 token 级融合+本体专属动作编解码器配方达 41.5±12.1%；作者论证大动作鸿沟下共享确定性解码器'必然失败'，本体特化权重是必要条件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06627](https://arxiv.org/abs/2606.06627) What Matters When Cotraining Robot Manipulation Policies on Everyday Human Videos?
- Locator: 6 Results
- Evidence: 4.4 节'guaranteed to fail'论证 + 6 Results 架构消融段与 Tab. 1(CLS 14.7/PiZero 17.5/EgoBridge 16.6 vs Ours 41.5)。
- Quote: “Additionally, untying the action encoders and decoders leads to large improvements in 5 out of 6 tasks, for a similar reason.”
- Authors: richard-li; aditya-prakash; andrew-wen; et al.

### EA-EGOPREC-2026-0437

- Claim: RealDexUMI 把 6-DoF 追踪位姿仅用于构造 hand-frame 相对动作标签（∆T_{t,k}=T_t^{-1}T_{t+k}），绝对位姿不进入策略观测，使策略从局部视觉、触觉与手部状态预测末端运动，而非记忆采集特定的全局位姿——从设计上放宽了对全局追踪帧精度与采集-部署坐标对齐的要求。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.06033](https://arxiv.org/abs/2606.06033) RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning
- Locator: 4.1 Policy Interface
- Evidence: 4.1 明确绝对位姿不进观测、仅用 T_t 构造相对标签，并给出不记忆全局位姿的动机；附录 B.1 确认 6-DoF 位姿流（100Hz）仅作动作标签。
- Quote: “only to construct hand-frame relative action labels, so the policy predicts end-effector motion from local visual, tactile, and hand-state cues rather than memorizing a collection-specific global pose.”
- Authors: chaoyi-xu; yixuan-jiang; jiahui-huan; et al.

### EA-EGOPREC-2026-0376

- Claim: 在 ego 视频重定向的灵巧操作中，仅使用重建的人手运动（无物体状态与接触监督）成功率仅 9.8%，加入物体 6-DoF 状态后升至 36.2%，完整管线达 49.5%，说明手部轨迹必须辅以物体状态与接触信息才能支撑可执行的末端轨迹。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08057](https://arxiv.org/abs/2606.08057) EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets
- Locator: 3 Egocentric Demonstration Data Collection and Quality Assessment (Table 2); 4.2 Simulation Experiment Results
- Evidence: Table 2（EgoDex-R 100 序列）三消融成功率对比。
- Quote: “EgoDex-R Only Hand Pose 28.6 4.72 3.35 2.48 9.8 EgoDex-R w/o Adaptive Contact Optimization 15.4 1.36 2.93 2.18 36.2 EgoDex-R EgoAERO 9.7 0.82 2.48 1.65 49.5”
- Authors: yichen-niu; haoran-lv; xinrui-zhang; et al.

### EA-EGOPREC-2026-0380

- Claim: 即便经过前述校正，ego 遮挡与手部姿态估计误差仍会导致指尖悬空、接触缺失或局部穿透；EgoAERO 将其形式化为保守的几何级接触修正（不动物体姿态与 MANO 关节，仅有界调整全局平移与局部指尖几何）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08057](https://arxiv.org/abs/2606.08057) EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets
- Locator: 2.1 Asset-free Egocentric Hand-Object Reconstruction
- Evidence: 2.1.5 节陈述接触失真问题与修正公式化。
- Quote: “Due to egocentric occlusions and hand pose estimation errors, fingertip float- ing, missing contacts, or local penetra- tions may still occur during grasping. EgoAERO formulates this problem as a conservative geometry-level contact cor- rection: it keeps the object pose, ob- ject mesh, and MANO articulation un- changed, and only applies bounded cor- rections to the global hand translation and vertices in local contact regions”
- Authors: yichen-niu; haoran-lv; xinrui-zhang; et al.

### EA-EGOPREC-2026-0420

- Claim: 该系统为'可接受误差范围'提供了一个操作化锚点：IL 蒸馏策略在物体位姿局部随机化（平面 ±5 cm、朝向 ±10°）下训练，使机器人对检测与重建误差在该局部范围内保持鲁棒；超出局部范围则需改用碰撞感知运动规划，而规划路点约 1-2 cm 的末端位姿偏差即可导致精密任务失败。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08828](https://arxiv.org/abs/2606.08828) Video2Sim2Real: Full-Stack Autonomous Dexterous Skill Acquisition from a Single Human Video
- Locator: 4.3 Sim-to-Real Transfer Modules
- Evidence: 4.3.1 给出 ±5cm/±10° 训练随机化范围（附录 A.3.1 同为 ±5cm/±10°，测试扰动 0.5-5cm 见 Table 9/10）；附录 A.4 报告规划 EE 位姿与期望接触位姿典型偏差约 1cm 需短视界 IK 精修，附录 G.2 报告约 2cm 路点误差导致 Apple/Toy replay 失败。
- Quote: “Randomization: In training, we randomize the object position and orientation within a local range (e.g., ±5 cm and ±10 ◦ , respectively) and collect pairs of point cloud and the corresponding robot hand poses in the table frame.”
- Authors: yunhai-han; jianuo-qiu; linhao-bai; et al.

### EA-EGOPREC-2026-0024

- Claim: 在 ego-centric 视频上，现成手部追踪器 HaWoR 虽能准确追踪手部姿态，但对形状/尺度的逐帧推理不一致——单条视频内手部尺度变化超过 10%（正文附录称 >10cm），并在深度轴引入 >30Hz 的高频噪声（尺度-深度歧义：大手被推断为更远、小手更近）；将形状参数改为以 HaMeR 平均 β 为输入的尺度一致推理后，关键点轨迹稳定性明显改善。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.10614](https://arxiv.org/abs/2606.10614) Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations
- Locator: Appendix F Scale-Consistent HaWoR (extraction heading 'References'), Figure 6
- Evidence: Appendix F 逐字报告单条 egocentric 视频内 >10cm 尺度变化、>30Hz 深度噪声与成因解释，Figure 6 caption 报告 >10% 尺度不一致；3.2 节声明修改后 'noticeable improvement in the stability of the keypoint trajectory'。改善幅度未定量，claim 保持定性。
- Quote: “However, as shown in Figure 6a, even within a single egocentric video, the hand scale varies notably, i.e., > 10cm. In other words, the model inconsistently infers that larger hands are farther away and smaller hands are closer than the ground truth. To verify this, in Figure 6b, we visualize the depth noise amplitude, i.e., > 30Hz signal which is definitely noise from the human action within a single sequence.”
- Authors: beomjun-kim; seong-hyeon-park; seunghoon-sim; et al.

### EA-EGOPREC-2026-0025

- Claim: 对手部关键点标注的精度需求随训练阶段不同：互联网规模预训练可直接使用 VITRA 语料中精度较低的 HaWoR 预计算关键点（作者称 'the less accurate keypoint labels are benign for training'），而任务微调集的关键点直接刻画任务操作过程、必须准确（'need to be accurate to successfully represent the process of the task'），因此微调集额外做了尺度一致化处理。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.10614](https://arxiv.org/abs/2606.10614) Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations
- Locator: 3.2 Data
- Evidence: 3.2 Data 节逐字给出两阶段精度需求的对比陈述，并说明这是引入尺度一致 HaWoR 的动机；该论断为作者经验性主张，无单独消融，故 stance 取 conditional。
- Quote: “For the pretraining corpus we use VITRA’s pre-computed HaWoR [37] hand keypoints directly. Since the purpose of the pretraining is to coarsely train general dexterous hand manipulation, the less accurate keypoint labels are benign for training. On the other hand, keypoints of the fine-tuning dataset are directly related to the task manipulation, which need to be accurate to successfully represent the process of the task.”
- Authors: beomjun-kim; seong-hyeon-park; seunghoon-sim; et al.

### EA-EGOPREC-2026-0399

- Claim: LUCID 有意将手部重建降级为'粗略 palm pose'：WiLoR 的 MANO 手网格逐帧刚体拟合到深度得到 palm pose，与物体 flow 共同构成短视野意图参考，精细手指构型与接触被显式丢弃并委托给仿真 RL 策略；作者承认该有损接口即使在意图准确时也缺失完整复现人类演示所需线索。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11628](https://arxiv.org/abs/2606.11628) LUCID: Learning Embodiment-Agnostic Intent Models from Unstructured Human Videos for Scalable Dexterous Robot Skill Acquisition
- Locator: 3.1 Intent Model
- Evidence: 3.1 定义 intent 为 'object motion and rough palm pose' 并描述 WiLoR→刚体拟合→palm pose 链路；5 Limitations (3) 自述接口丢弃 finger configuration and fine contact、即使意图准确也缺失复现线索。
- Quote: “We define manipulation intent as a short-horizon prediction of object motion and rough palm pose, shared across embodiments; the joint-level commands that realize it are delegated to a separate sensorimotor policy.”
- Authors: harsh-gupta; guanya-shi; wenzhen-yuan

### EA-EGOPREC-2026-0344

- Claim: 同一套视频提取的运动先验在不同灵巧手上的迁移性能差异显著：Arti-MANO 82.4%（拟人结构贴近 MANO）最高，Inspire 78.8%、Shadow 61.6%、Allegro 52.0% 最低；作者将 Allegro 低分归因于粗大指尖导致的自碰撞与网格穿插触发提前终止。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: 4.4 Generalization and Visualization Results
- Evidence: Table 4 给出 4 本体×5 任务成功率与平均；4.4 正文解释 Arti-MANO 的拟人优势与 Allegro 的几何干扰-提前终止机制。
- Quote: “The Arti-MANO achieves the highest overall success rate (82.4%) largely due to its anthropomorphic design; its link proportions and joint hierarchies closely align with the human MANO model used in our trajectory optimization, facilitating a natural mapping of dex- terous poses in contact-rich tasks. In contrast, the high-dimensional configurations of the Shadow and Allegro hands introduce significant complexity, as their increased degrees of freedom expand 7 Brush the mug Pour water with cup”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0394

- Claim: DO AS I DO 将成功重定向轨迹定义为平均位置误差 E_pos < 0.1 m 且平均旋转误差 E_rot < 0.5 rad，并在此阈值下对 655 条噪声重建参考达到 71% 成功率、最终平均位置误差 0.05 m / 旋转误差 0.28 rad，给出了人视频重定向末端轨迹的一条可接受精度参考线。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.19333](https://arxiv.org/abs/2606.19333) Do as I Do: Dexterous Manipulation Data from Everyday Human Videos
- Locator: 4.1 Experimental Setup; Table 3: Retargeting Results
- Evidence: 4.1 Experimental Setup 明确阈值定义；Table 3 完整管线（+Transition Reward 行）报告 Reconstruction 列 Pos 0.05 / Rot 0.28。阈值沿用近期文献 [15, 59, 60] 口径。
- Quote: “Following the recent literature [15, 59, 60], we evaluate successful trajectories as those with mean position error E pos < 0.1 m and mean rotation error E rot < 0.5 rad.”
- Authors: bhawna-paliwal; haritheja-etukuru; william-liang; et al.

### EA-EGOPREC-2026-0446

- Claim: HumanoidUMI 的高层策略以稀疏关键点（默认 pelvis+双 TCP+双足，下肢密集任务加双膝）为动作空间，且所有关键点以 query 时刻 pelvis 帧表示、未来位姿相对其 query 时刻位姿构造相对标签（式 1），部署时再用当前机器人前向运动学解码（式 2）——手部（TCP）追踪误差经此相对化与根帧绑定被部分隔离，而非直接进入全局帧绝对轨迹标签。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.27239](https://arxiv.org/abs/2606.27239) HumanoidUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: B. High-Level: Diffusion Policy
- Evidence: III-B 明确动作空间构造（5×9+2=47 维）、pelvis 帧表示与式 1-2 的编码/解码；III-A 说明关键点来自 PICO SDK 手柄位姿与 SMPL 身体表示的坐标变换。
- Quote: “All keypoint poses are expressed in the pelvis frame at the query time t.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### EA-EGOPREC-2026-0447

- Claim: SKR 把人体-机器人形态差异的补偿显式集中在两处：对腿相关关键点仅施加 pelvis 局部垂直缩放（λ_leg=0.75，其余关键点坐标不变），以及对所有关键点施加固定标定偏移以吸收追踪人体关键点与机器人连杆帧之间的差异；随后两阶段约束加权 IK（先足支撑一致性、后 pelvis/TCP 精修）生成时间连贯的机器人原生参考。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.27239](https://arxiv.org/abs/2606.27239) HumanoidUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
- Locator: C. Bridge: Keypoint Retargeting System
- Evidence: III-C 给出 λ_leg=0.75 的取值与动机（演示者与 G1 腿长差）、'Fixed calibrated offsets are applied...' 的偏移声明、式 5 的加权 IK 与两阶段流程；Fig. 5 说明 SKR 保留关键点间度量空间关系。
- Quote: “Fixed calibrated offsets are applied to account for differences between the tracked human keypoints and robot link frames.”
- Authors: hongwu-wang; chenhao-yu; youhao-hu; et al.

### EA-EGOPREC-2026-0040

- Claim: 在捏取等精细接触任务中，上游手部测量误差会被直接放大为任务级失败：抓取小物体时即使很小的位置误差也会导致任务失败；由于传感器限制与潜在电磁干扰，即使操作者明确做出指尖接触，测得的手部姿态仍可能显著偏离真实手势、无法捕捉捏取的几何特征。AnyDexRT 的缓解是不再仅依赖（含噪的）指尖位置映射推断精细接触，而是训练接触分类器从拇指-他指指尖位置对识别捏取模式；推理时检测到人际指尖接触即在对应映射机器人位置的邻域搜索机器人捏取姿态以保证稳定抓取。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.08341](https://arxiv.org/abs/2607.08341) AnyDexRT: Calibration-Free Dexterous Hand Retargeting with Few-Shot Human Guidance
- Locator: 6 DoF 7 DoF (mangled extraction heading spanning Sections 1-4.1 Setup, passage in 3.4 Pinch Pose Refinement using Contact Classifier)
- Evidence: 3.4 节明确：小物体抓取对重定向精度要求高、小位置误差即可致任务失败；因传感器限制与电磁干扰，测量手姿可显著偏离真实手势、丢失捏取几何特征；为此训练接触分类器 f_c 识别接触模式（式 5，BCE 损失），推理时检测到接触即在映射位置邻域搜索机器人捏取姿态。
- Quote: “Grasping tiny objects requires higher retargeting accuracy, as even small positional errors can lead to task failure. This is especially critical for pinch motions, where precise fingertip contact is re- quired. As shown in Fig. 4, due to sensor limitations and poten- tial electromagnetic interference, the measured hand pose may still deviate significantly from the actual hand gesture, even when the operator makes clear fingertip contact. As a result, the measured pose may fail to capture the ge”
- Authors: chenxi-wang; ying-feng; hongjie-fang; et al.

### EA-EGOPREC-2026-0064

- Claim: 以单条人类演示经交互保持重定向 + 残差 RL 训练的策略可零样本迁移到真机：作者报告其方法在四个手-任务设置中的三个（LEAP-Scissors、LEAP-Screwdriver、WUJI-Screwdriver）上可靠迁移，而第四个（WUJI-Scissors）未成功。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.11874](https://arxiv.org/abs/2607.11874) A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation
- Locator: 4.2 Results / Method
- Evidence: 4.2 (Q3) 原文明确列出三个可靠迁移任务；第四任务 WUJI-Scissors 的失败由同段后文与 limitations 归因于非回驱电机与不准的剪刀网格。
- Quote: “(Q3) Sim-to-real transfer. We deploy the RL policies that achieve reasonable performance in simu- lation to the real world and show the performance in Table 2. Our method transfers reliably on three of the four tasks: LEAP-Scissors, LEAP-Screwdriver, and WUJI-Screwdriver.”
- Authors: yunhai-feng; natalie-leung; jiaxuan-wang; et al.

### EA-EGOPREC-2026-0065

- Claim: 在相同 RL 设置下，重定向参考质量的差异直接决定下游策略可用性：交互保持重定向使仿真成功率达 98.7-99.8%（物体关键点误差 5.3-6.5mm），而纯运动学 IK 重定向基线（Mink IK+RL、DexMachina、SPIDER）因手-物穿透等物理不可行参考在多数任务上成功率为 0-22.3%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.11874](https://arxiv.org/abs/2607.11874) A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation
- Locator: 4.2 Results / Method, Table 1
- Evidence: Table 1 行给出四方法在四任务上的误差与成功率对比；4.2 (Q1) 原文说明 IK 基线产生大量手-物穿透并导致 RL 初始化不稳定。
- Quote: “REGRIND (Ours) 5.6±6.4 99.8±0.3% 5.4±5.8 99.7±0.0% 5.3±13.1 98.7±1.3% 6.5±15.5 98.8±1.3% SPIDER 176.2±1.6 0.0±0.0% 134.5±78.9 0.0±0.0% 119.0±32.7 0.0±0.0% 116.9±16.1 0.0±0.0% DexMachina 10.1±9.5 22.3±17.7% 8.3±6.7 99.7±0.1% 67.2±31.8 0.0±0.0% 5.9±9.7 99.3±0.1% Mink IK + RL 12.6±21.4 2.0±2.9% 17.5±4.5 0.0±0.0% 38.9±29.1 0.0±0.0% 10.0±12.0 3.1±1.3%”
- Authors: yunhai-feng; natalie-leung; jiaxuan-wang; et al.

### EA-EGOPREC-2026-0067

- Claim: REGRIND 的迁移配方在 RL 训练中对策略观测注入均匀噪声（位置 ±2mm、旋转 ±0.02rad、关节 ±0.02rad），并施加 0-2 控制步的连续观测时延以建模真机系统延迟（系统辨识测得真机响应滞后约 1-2 步、30-60ms）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.11874](https://arxiv.org/abs/2607.11874) A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation
- Locator: References / App. B.4
- Evidence: 附录 B.4 原文给出观测噪声与时延注入量级；附录 E 系统辨识给出 1-2 步（30-60ms）实测延迟，二者共同定义了该管线所针对的感知噪声包络。
- Quote: “Observation noise. We apply uniform noise on policy observations at every timestep (position ±2, mm, orientation ±0.02, rad, joints ±0.02, rad). We also apply continuous observation lag to model the delay in the real-world system (uniformly sampled in [0, 2] control steps per reset, with shared lag within object state, wrist pose, and hand joints).”
- Authors: yunhai-feng; natalie-leung; jiaxuan-wang; et al.

### EA-EGOPREC-2026-0486

- Claim: any-to-any 重定位压力测试以物体位置误差 <2cm 且旋转误差 <20° 作为目标到达判据；部署后的控制器在该判据下于 Cylinder 上连续到达 41.1 个随机目标、per-target 成功率 97.6%（Cuboid 为 12.1 个、92.3%）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.11481](https://arxiv.org/abs/2607.11481) Towards Human-level Dexterous Teleoperation
- Locator: References (Appendix A.1 Any-to-Any Reposition Evaluation, Tab. 6)
- Evidence: 附录 A.1 给出判据（2cm/20° 同时满足）、15 次/物体协议与结果（41.1/97.6% vs 12.1/92.3%），并归因于物体几何差异。
- Quote: “A target is counted as reached when the object position error falls below 2 cm and the object rotation error falls below 20 ◦ simultaneously. A trial terminates when (i) the object slips out of the hand, or (ii) the active target has not been reached for 20 s.”
- Authors: puhao-li; zeyuan-chen; yingying-wu; et al.

### EA-EGOPREC-2026-0522

- Claim: Open-AoE 的 110D 密集 MANO 动作表示在当前相机帧系下表达腕部平移与有限差分速度，作者明确声明该速度同时包含手部运动与相机自运动，而非纯惯性系腕部运动——ego 视频的载体自运动会混入以相机帧表示的手部轨迹量，是 ego-centric 路线特有的轨迹污染来源。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.14183](https://arxiv.org/abs/2607.14183) Open-AoE: An Open Egocentric Manipulation Dataset and Toolchain for Embodied Learning
- Locator: 4.3. AoE-Training-Ready
- Evidence: 4.3 节 110D 表示定义段：平移与速度以米/米每秒在当前帧 OpenCV 相机坐标表达；作者附注速度含手运动+相机自运动。Table 2 显示 48D wrist-fingertip 与 62D/20D 接口改用 SLAM 世界帧。
- Quote: “because this frame moves with the wearer, the velocity contains both hand motion and camera ego-motion rather than purely inertial wrist motion.”
- Authors: zishuo-li; bowen-yang; changtao-miao; et al.

### EA-EGOPREC-2026-0109

- Claim: 为从无人工 3D 标注的 ego 视频构建基准（EgoMe-pose），作者采用自动标注+双级阈值过滤管线：先用置信度阈值 σ_d≥0.5 的现成手部检测器提取手部包围框，再用 InterHand 估计相对 3D 手部姿态、RootNet 预测手根绝对深度并做相对-绝对坐标仿射变换，最后仅保留手部置信度 σ_d≥0.6 且整集超过 95% 帧有效标注的样本；最终整理出 6067/1344/2648 个训练/验证/测试集。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.15890](https://arxiv.org/abs/2607.15890) Exo2EgoPose: Leveraging Exocentric Demonstrations for Vision-Language guided Egocentric 3D Hand Pose Forecasting
- Locator: 4.1 Experimental Settings, 4.1.1 Benchmarks (EgoMe-pose 标注管线; float Table 1 使该段落在抽取文本中位于 'Methods' 标题之下)
- Evidence: 4.1.1 EgoMe-pose 构建管线逐字给出 (2) 检测阈值 σ_d≥0.5、(3) InterHand+RootNet 相对-绝对变换、(4) 过滤条件 σ_d≥0.6 且 >95% 帧有效，以及 6067/1344/2648 的划分规模。
- Quote: “(2) Hand detection: Before 3D hand pose labeling, we first utilize an on-the-shelf hand detector with a threshold 𝜎 𝑑 ≥ 0.5 to extract bounding boxes of hand(s) in the video frames. (3) Hand pose labeling: We employ InterHand [45] to estimate the relative 3D hand poses. Then, we adopt RootNet [44] to predict the absolute depth of the hand roots. Furthermore, we perform the relative-to-absolute affine transformation of the coordinate system. (4) Annotation filtering: To ensure the accuracy of aut”
- Authors: zhaofeng-shi; heqian-qiu; lanxiao-wang; et al.

### EA-EGOPREC-2026-0454

- Claim: 腕部相机 VIO 的视野会被手或被操作物体经常性遮挡，使轨迹易受追踪失败与累积漂移影响；HiFi-UMI 据此改用头戴视点（头运动远小于手运动）加标记块相对定位，并以源轨迹有效性检查剔除 SLAM 追踪失败、丢帧、时间戳不连续、严重手部位姿离群与动作尖峰等片段。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: 3.1 HiFi-UMI Capture Device
- Evidence: Sec 3.1.1 陈述腕部 VIO 的遮挡/漂移失效模式与头戴方案动机；Sec 5.5 列出训练前的源轨迹剔除规则，覆盖 SLAM 失败与手部位姿离群。
- Quote: “Wrist-camera VIO is cheaper and lighter than either, yet its view is routinely occluded by the hand or the manipulated object, leaving trajectories vulnerable to tracking failure and accumulated drift.”
- Authors: simple-ai; unknown-author; yuteng-wei; et al.

### EA-EGOPREC-2026-0310

- Claim: SiMDex 的人类轨迹来自 EgoDex 的追踪腕部与指尖变换；进入重定向前先变换到身体中心系去除 ego 运动、按手部可见性与速度过滤、并施加时序平滑——即在数据生产端对追踪质量做了显式门控，但未报告过滤阈值或追踪误差幅度。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.04196](https://arxiv.org/abs/2608.04196) SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation
- Locator: 3.1 Unified Morphology-Agnostic Representation
- Evidence: 3.1 Sources 段逐句描述人类样本的追踪来源与三项预处理。
- Quote: “Human demonstrations are drawn from EgoDex [19], an egocentric video dataset with tracked wrist and fingertip transforms; we transform trajectories into a body-centered frame to remove ego-motion, filter by hand visibility and velocity, and apply temporal smoothing before the same retargeting.”
- Authors: nie-lin; takehiko-ohkawa; sijin-chen; et al.

### EA-EGOPREC-2026-0044

- Claim: 单目管线的逐帧手部检测噪声首先表现为接触观测不稳定：从单帧独立提取的接触对位姿噪声、遮挡与单目深度歧义敏感；C2Dex 的关键观察是在局部稳定接触期内同一手顶点应保持关联物体表面的同一局部区域，因此把逐帧接触观测聚合到规范物体空间（去除物体刚体运动后可比），经法向一致性过滤、按时序稳定性分段、段内 DBSCAN 聚类并取主导簇 medoid 得到稳定接触，再以接触一致性损失把稳定接触作为轨迹级约束回灌 HOI 优化，减少接触抖动、伪接触切换与穿透。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.07045](https://arxiv.org/abs/2608.07045) C2Dex: Contact-Consistent Reconstruction and Retargeting for Dexterous Manipulation from Monocular Video
- Locator: A. Contact-Consistent HOI Reconstruction
- Evidence: III-A-b 明确：逐帧独立提取的接触对位姿噪声/遮挡/单目深度歧义敏感；核心观察是局部稳定接触期内手顶点关联同一物体局部区域；故在规范物体空间聚合逐帧观测。同节给出法向一致性过滤（w_n>γ_n）、ε_θ 分段、DBSCAN 主导簇 medoid（式 1）与接触一致性损失（式 2）；III-A-c 与图 1 陈述其减少接触抖动/伪切换/穿透的作用。
- Quote: “b) Cross-Frame Contact Stabilization.: Contacts ex- tracted independently from individual frames are sensitive to pose noise, occlusion, and monocular depth ambiguity. Our key observation is that, within a locally stable contact phase, a hand vertex should remain associated with the same local region of the object surface. We therefore aggregate frame- wise contact observations in the canonical object space.”
- Authors: jie-ren; zhehao-jiang; yinhong-yang; et al.

### EA-EGOPREC-2026-0512

- Claim: 实体机器人基座在 ego-centric 人类视频中不可观测，HandEdit 因此对每个源序列×目标本体定义相机相对的虚拟基座并在整段序列保持固定；候选基座经 IK 可行性、关节限位、碰撞与轨迹质量评估，人工从前三名有效序列级方案中挑选，全部不可信时整段序列被剔除——基座不可观性是 ego 视频重定向到臂手系统时特有的结构性误差源。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.12122](https://arxiv.org/abs/2608.12122) HandEdit: A Unified Benchmark for Egocentric Human-to-Robot Dexterous Hand Image Editing
- Locator: Abstract / Section 3.1 Data Curation Pipeline
- Evidence: Section 3.1 臂手段：基座不可观测→定义相机相对虚拟基座并整段固定；候选经 IK 可行性/关节限位/碰撞/轨迹质量评估；人工选前三名之一，全不可信则剔除序列。
- Quote: “Because the physical robot base is not observable in egocentric human videos, we define a camera-relative virtual base for each source sequence and target embodiment and keep it fixed throughout the sequence.”
- Authors: zhenjie-yang; xingyu-jiao; guopeng-zhong; et al.

### EA-EGOPREC-2026-0514

- Claim: 由于渲染的机器人前景与修复的背景分开处理，初始合成图在颜色、光照、对比度、纹理或边界外观上可能不匹配，使插入的机器人在视觉上脱离环境；HandEdit 因此在管线末端追加轻量和谐化模块（约 20MB 的 Harmonizer，在 1 万张自然 ego 手部图像上自监督训练）——重定向+渲染链路即使几何正确，仍残留外观层误差，需要专门后处理。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.12122](https://arxiv.org/abs/2608.12122) HandEdit: A Unified Benchmark for Egocentric Human-to-Robot Dexterous Hand Image Editing
- Locator: Background / Section 3.5 Harmonization Post-processing
- Evidence: Section 3.5 首段给出前景/背景分治导致外观失配的机制描述，随后给出 Harmonizer 的训练与推理设置（1 万张自监督、推理时用机器人 mask 定位细化区域、不改变关节构型/腕姿态/物体状态/交互几何）。
- Quote: “Because the foreground and background are processed separately, the initial composite may contain mismatches in color, illumination, contrast, texture, or boundary appearance, making the inserted robot look visually detached from its surroundings.”
- Authors: zhenjie-yang; xingyu-jiao; guopeng-zhong; et al.

### EA-EGOPREC-2026-0068

- Claim: 在 ego-centric 域偏移（HOI4D：手外观、相机、环境均变化）下，AdvDex 的手部动作预测误差为 d_h-o 10.5mm、MPJPE 7.2mm、MWTE 6.1mm，约为同采集域（OmniShare-Unseen：3.2/2.8/2.5mm）的 2.5-3 倍；去掉域对抗模块（w/o Adv）HOI4D 误差升至 13.9/13.3/10.8mm，VITRA 基线为 16.3/13.7/11.5mm。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.14028](https://arxiv.org/abs/2608.14028) AdvDex: Learning Dexterous Manipulation from Human Demonstrations via Joint-Aligned Actions and Adversarial Learning
- Locator: Method, Table 2
- Evidence: Table 2 四行数值直接给出两裂、三指标的对比；4.2 原文说明 HOI4D 裂引入手外观/相机/环境偏移，且 w/o Adv 与 Ours 的差异支持域对抗的有效性。
- Quote: “VITRA [73] 20.1 16.2 14.8 16.3 13.7 11.5 w/o OmniShare 19.8 15.7 14.2 15.6 14.1 11.3 w/o Adv 6.4 4.9 4.2 13.9 13.3 10.8 Ours 3.2 2.8 2.5 10.5 7.2 6.1”
- Authors: zhiyue-zhao; jing-wu; hairuo-liu; et al.

### EA-EGOPREC-2026-0070

- Claim: 从预训练中去掉手套采集的 OmniShare 人类演示后，真机策略在 unseen 物体列成功率从 50.0% 降到 25.0%、unseen 环境列从 60.0% 降到 20.0%；去掉域对抗模块则分别降到 15.0% 与 30.0%，完整模型为 50.0%/60.0%。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.14028](https://arxiv.org/abs/2608.14028) AdvDex: Learning Dexterous Manipulation from Human Demonstrations via Joint-Aligned Actions and Adversarial Learning
- Locator: Ablations, Table 3
- Evidence: Table 3 消融行直接给出四种配置在 5 个 seen 任务 + unseen 物体/环境两列的成功率；unseen 两列的跌幅最大，符合作者“larger drops on unseen objects and environments”的原文结论。
- Quote: “w/o OmniShare 75.0 55.0 45.0 85.0 65.0 25.0 20.0 w/o Adv 70.0 60.0 40.0 80.0 50.0 15.0 30.0 Ours 80.0 70.0 55.0 90.0 70.0 50.0 60.0”
- Authors: zhiyue-zhao; jing-wu; hairuo-liu; et al.

### EA-EGOPREC-2026-0047

- Claim: 当参考由学习的 ACT 策略（约 30-40 条人类示教训练）生成时，执行端力反馈修正对接触保持的收益是任务依赖的：纸杯任务 force-safe success 从参考策略单独的 30.0% 提升到 REFORCE 的 70%，严重失接触从 7/10 降为 0/10，追踪误差从 0.812 降到 0.124 N；但夹子任务上 admittance（90.0%、0.419 N）优于 REFORCE（54.5%、0.441 N，4/11 过力试验）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.15560](https://arxiv.org/abs/2608.15560) ReForce: Learning Force-aware Retargeting for Dexterous Manipulation
- Locator: 4.1 Real-World Evaluation
- Evidence: Table 2 完整报告两任务三种执行配置的 force-safe success、追踪误差、过力与严重失接触计数；正文 4.1.2 明确承认 REFORCE 对 admittance 的力追踪优势是任务依赖的。
- Quote: “Task Method Force-safe success ↑ Tracking error ↓ Over-force ↓ Severe missing contact ↓ Active fingers ↑ Paper cup Reference policy 30.0% 0.812 0/10 7/10 0.17 Paper cup Reference policy + Admittance 60.0% 0.683 4/10 1/10 1.26 Paper cup Reference policy + REFORCE 70% 0.124 2/10 0/10 2.61 Tongs Reference policy 50.0% 0.454 0/10 5/10 0.94 Tongs Reference policy + Admittance 90.0% 0.419 0/10 1/10 1.34”
- Authors: yuhang-wu; lingqi-zeng; changwei-jing; et al.

### EA-EGOPREC-2026-0018

- Claim: 该管线的点轨监督与评估均以 Co-Tracker 自动追踪输出为 ground truth（训练时用 Co-Tracker 在 40 万片段上生成监督轨迹，评估时同样以 Co-Tracker 输出为参照），因此报告的点轨精度是相对于该现成追踪器的一致性，其绝对精度上限受追踪器误差约束，且评估存在同源循环。
- Stance: `limit` | Confidence: `direct`
- Paper: [2405.01527](https://arxiv.org/abs/2405.01527) Track2Act: Predicting Point Tracks from Internet Videos enables Generalizable Robot Manipulation
- Locator: 4.1 Evaluation Details
- Evidence: 4.1 节明确'we consider the output of Co-Tracker to be the ground-truth'；附录 6.5 明确训练监督来自对 400,000 个片段运行 Co-Tracker。两处均为作者直接陈述的设计事实。
- Quote: “For evaluation videos, we consider the output of Co-Tracker [29] to be the ground- truth and compare the difference with respect to the predictions, based on the δ x t metric.”
- Authors: homanga-bharadhwaj; roozbeh-mottaghi; abhinav-gupta; et al.

### EA-EGOPREC-2026-0476

- Claim: Bunny-VisionPro 作者明确承认：Apple Vision Pro 的手部追踪在手指自遮挡时不准确，直接导致机器人控制命令抖动；作者提出融合可穿戴设备数据作为缓解方向。
- Stance: `limit` | Confidence: `direct`
- Paper: [2407.03162](https://arxiv.org/abs/2407.03162) Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning
- Locator: 6 Conclusion and Limitation
- Evidence: 第 6 节 limitation 第一句逐字给出自遮挡→追踪不准→命令抖动的因果陈述与可穿戴融合的缓解建议。
- Quote: “Limitation. Our system has two main limitations: (i) Vision Pro’s hand tracking is inaccurate when fingers are self-occluded, causing jerky control commands. This issue could be mitigated by fusing data from wearable devices with Vision Pro.”
- Authors: runyu-ding; yuzhe-qin; jiyue-zhu; et al.

### EA-EGOPREC-2026-0004

- Claim: WiLoR 在相机系中估计 3D 手姿，作者承认这可能导致对整体 3D 场景的不准确假设，需要接入 3D metric 基础模型才能实现世界系重建。
- Stance: `limit` | Confidence: `direct`
- Paper: [2409.12259](https://arxiv.org/abs/2409.12259) WiLoR: End-to-end 3D Hand Localization and Reconstruction in-the-wild
- Locator: 9. Limitations
- Evidence: Limitations 节明确陈述相机系估计局限并给出补救方向（3D metric 基础模型）。
- Quote: “Finally, WiLoR estimates 3D hand poses in cam- era space, which may lead to inaccurate assumptions about the overall 3D scene. Adapting WiLoR with a 3D metric foundational model [96, 99] could enable more accurate 3D reconstruction in world space.”
- Authors: rolandos-alexandros-potamias; zhang-jinglei; jiankang-deng; et al.

### EA-EGOPREC-2026-0005

- Claim: 即使以 2M 图像训练，WiLoR 仍在极端手指姿态与拥挤环境下检测/重建失败，且 bottom-up 逐手重建无法充分捕捉双手交互与接触。
- Stance: `limit` | Confidence: `direct`
- Paper: [2409.12259](https://arxiv.org/abs/2409.12259) WiLoR: End-to-end 3D Hand Localization and Reconstruction in-the-wild
- Locator: 9. Limitations
- Evidence: Limitations 节给出失效模式并呼应 Figure 7 failure cases。
- Quote: “As can be seen in Fig. 7 WiLoR can fail under extreme finger poses and can also fail to detect hands in crowded environments. Creating a synthetic dataset with diverse hand poses and photorealistic hands could help mitigate these issues [67]. Additionally, since WiLoR employs a bottom-up recon- struction strategy, interactions and contacts between hands may not be adequately captured in 3D space.”
- Authors: rolandos-alexandros-potamias; zhang-jinglei; jiankang-deng; et al.

### EA-EGOPREC-2026-0429

- Claim: 非平行夹爪造成系统性末端轨迹偏差：xArm Gripper 全开-全闭间有效长度变化约 1 厘米，使手持演示迁移到机载执行时相机视角与 TCP 错位，FastUMI 因此需要在推理时运行动态误差补偿算法（按夹爪开度沿 TCP 局部 Z 轴反向修正指令位姿）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2409.19499](https://arxiv.org/abs/2409.19499) FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset
- Locator: II-C. Robot-Mounted Device Design, Fig. 4
- Evidence: II-C 给出 xArm Gripper 有效长度变化约 1cm 的事实与迁移错位问题，IV-E 给出两阶段动态误差补偿公式（补偿距离 d(i) 与位姿修正 p'ee = pee - d(i)·z_axis）。
- Quote: “For example, the xArm Gripper’s effective length changes by approximately 1 centimeter as it moves between fully open and closed positions (see Fig. 4). This discrepancy in gripper motion can create mismatches in the observed camera view, especially when transferring demonstrations collected on the handheld device to different robot-mounted setups.”
- Authors: zhaxizhuoma; liu-kehui; guan-chuyue; et al.

### EA-EGOPREC-2026-0430

- Claim: 作者实验观察到原 UMI 系统基于 GoPro 的 VIO 加开源 SLAM 配置在铰链操作等涉及长时间遮挡的任务中难以维持鲁棒运行，视觉信号间歇丢失导致数据质量下降、削弱后续学习效用；且 VIO 对参数化敏感、需复杂标定与多次坐标变换。
- Stance: `limit` | Confidence: `direct`
- Paper: [2409.19499](https://arxiv.org/abs/2409.19499) FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset
- Locator: I. INTRODUCTION
- Evidence: I. INTRODUCTION 明确记录作者对 UMI 系统的实验评估观察（prolonged occlusions 下追踪困难）及 VIO 标定复杂性，作为 FastUMI 重设计动机。
- Quote: “Through experimental evaluation, we observe that the UMI system encounters difficulties in tasks that involve prolonged occlusions, such as hinged operations. As a result, the UMI software configuration struggles to maintain robust operation when visual signals are intermittently lost, thereby diminishing data quality and reducing its utility for subsequent learning tasks.”
- Authors: zhaxizhuoma; liu-kehui; guan-chuyue; et al.

### EA-EGOPREC-2026-0087

- Claim: 尽管机器人末端位姿在语义上比关节位置更接近人手位姿，EgoMimic 发现 6-DoF ViperX 臂因解冗余度低，用末端位姿经笛卡尔控制器（如微分 IK）驱动时常遇到奇异或不平滑解，因此被迫改用关节空间控制、位姿空间预测仅用于学习人-机共享表征。
- Stance: `limit` | Confidence: `direct`
- Paper: [2410.24221](https://arxiv.org/abs/2410.24221) EgoMimic: Scaling Imitation Learning via Egocentric Video
- Locator: C. Training Human-Robot Joint Policies
- Evidence: III-C 明确说明末端位姿控制因 6-DoF 低冗余而遭遇奇异/不平滑解，故采用关节空间控制、位姿预测仅服务于共享表征。
- Quote: “While the robot end-effector poses are more semantically similar to human hand pose than robot-joint positions, it is difficult to control our robot with end-effector poses via a cartesian-based controller”
- Authors: simar-kareer; dhruv-patel; ryan-punamiya; et al.

### EA-EGOPREC-2026-0009

- Claim: HaWoR 作者自述管线依赖外部手部检测/跟踪输出，错误检测——尤其左右手身份跟踪失败——会传播为世界系重建错误；且双手独立建模在交互时产生自穿透。
- Stance: `limit` | Confidence: `direct`
- Paper: [2501.02973](https://arxiv.org/abs/2501.02973) HaWoR: World-Space Hand Motion Reconstruction from Egocentric Videos
- Locator: 9. Limitations
- Evidence: 补充材料 Limitations 节明确陈述检测误差传播与双手独立建模两类失效机制，并以 Figure 9 佐证。
- Quote: “One limitation of our approach is its reliance on hand- tracking outputs from an off-the-shelf method [32], which can propagate erroneous detections to HaWoR, particularly in cases of tracking identity failures. As illustrated in Fig. 9, such issues can lead to reconstruction errors, for example, when left/right hand tracking is incorrect. It is also important to note that HaWoR models each hand independently, without any inter-penetration con- strains. This can cause self-penetrations when the”
- Authors: jinglei-zhang; jiankang-deng; chao-ma; et al.

### EA-EGOPREC-2026-0353

- Claim: Phantom 作者明确承认：该方法的整体性能受限于现有手部姿态估计器的性能，因为演示视频的目标动作完全由估计器产生；由于手部姿态估计器目前仍在遮挡下表现困难，该方法同样如此。
- Stance: `limit` | Confidence: `direct`
- Paper: [2503.00779](https://arxiv.org/abs/2503.00779) Phantom: Training Robots Without Robots Using Only Human Videos
- Locator: 6 Limitations
- Evidence: Limitations 节第一条即将手部姿态估计器性能列为方法性能上限，并指出遮挡是共同弱点。
- Quote: “First, its performance is limited by the performance of exist- ing hand pose estimators since it relies on them to obtain the target actions from a demonstration video. Because hand pose estimators currently still struggle with occlusions, our method does too. However, this also means that our method will get better as hand pose estimators improve.”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0319

- Claim: 作者显式承认检测器伪标签存在三类残余误差并给出下游影响假设：self-contact（HOS 把手与身体/衣物的接触误判为手-物接触，可能给编码器引入对人体衣物的偏置）、premature contact（接近中即被误判接触，无深度信息下难排除，会把特征焦点移向背景）、premature tracking termination（HOS 漏检导致预测帧仍处接触状态，接触点预测退化为指尖位置回归、特征信息量减少）；这些误差源于 VISOR-HOS 的大量误报，管线过滤只能『大部分消除』。
- Stance: `limit` | Confidence: `direct`
- Paper: [2504.06084](https://arxiv.org/abs/2504.06084) MAPLE: Encoding Dexterous Robotic Manipulation Priors Learned From Egocentric Videos
- Locator: 3.2. Manipulation Supervision Extraction
- Evidence: 3.2 声明残余错误与 VISOR-HOS 误报来源；S6.1/S6.2 逐类给出误差定义与下游影响假设。
- Quote: “These residual errors reflect the large number of false posi- tives generated by [11], which are largely eliminated by fil- tering in our pipeline”
- Authors: alexey-gavryushin; xi-wang; robert-j-s-malate; et al.

### EA-EGOPREC-2026-0082

- Claim: 即使是 Apple Vision Pro/ARKit 生产级采集时追踪，其灵巧手部标注在重度遮挡（如叠毛巾）或非常高速的运动下也会不完美，因为标注本身是模型预测。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.11709](https://arxiv.org/abs/2505.11709) EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video
- Locator: Section 7 Conclusion (extraction block: background)
- Evidence: 作者在结论局限段明确承认标注在重度遮挡与高速运动下 imperfect，并指出标注是模型预测。
- Quote: “The dexterous annotations can also be imperfect, especially during heavy occlusion (e.g., towel folding) or very high speed motions, as they are themselves model predictions.”
- Authors: ryan-hoque; peide-huang; david-j-yoon; et al.

### EA-EGOPREC-2026-0362

- Claim: EgoZero 作者量化承认：Aria 手姿并不总是预测手上同一位置，HaMeR 对手部的旋转与平移分量预测不稳定；即使仔细调整动作组合公式(式 1)，最终动作标签仍含 1-2cm 误差，使策略无法解决高精度任务。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.20290](https://arxiv.org/abs/2505.20290) EgoZero: Robot Learning from Smart Glasses
- Locator: 4.5 Limitations
- Evidence: 4.5 Limitations of hand models 逐句给出 Aria/HaMeR 误差来源与 1-2cm 标签误差及其对高精度任务的阻断。
- Quote: “Aria’s hand pose does not always predict the same location on the hand and [54] predicts inconsistently incorrect rotational and translational components on the hand. Even when carefully Equation 1 is tuned, the action labels contain 1- 2cm error, preventing the policy from solving high-precision tasks.”
- Authors: vincent-liu; ademi-adeniji; haotian-zhan; et al.

### EA-EGOPREC-2026-0363

- Claim: 在 ego-centric 无深度传感器设定下，最优单目度量深度模型即使经场景中多个 Aruco 标签标定仍产生 >5cm 的深度误差，用估计深度替代三角化训练的策略在全部 7 个任务上无一例外地失败(0/15)；EgoZero 因此改用 CoTracker3 追踪+沿相机轨迹三角化来恢复物体 3D 状态。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.20290](https://arxiv.org/abs/2505.20290) EgoZero: Robot Learning from Smart Glasses
- Locator: 4.3 Ablations; Method, Table 1
- Evidence: 4.3 消融报告 >5cm 深度误差与'All policies trained with estimated depth fail unequivocally'；Table 1 中 EGOZERO - triangulated depth 行 7 任务全 0/15。
- Quote: “We observe that the best metric depth models, even when grounded with many Aruco tags in the scene, produce depth measurements of >5cm error. This suggests that the depth maps are warped unevenly, potentially by the distortion caused by Aria’s fisheye. All policies trained with estimated depth fail unequivocally.”
- Authors: vincent-liu; ademi-adeniji; haotian-zhan; et al.

### EA-EGOPREC-2026-0433

- Claim: 部署侧机器人手的回差与摩擦造成电机-指尖映射迟滞：Inspire Hand 指尖到达同一电机目标值的位置随运动方向不同而不同，编码器-电机回归模型只能保证单一方向（开或闭）精确，并给 inpainting 与动作映射带入细微偏差；XHand 的电机-指尖映射还随时间推移与每次重启轻微变化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.21864](https://arxiv.org/abs/2505.21864) DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation
- Locator: 7 Limitation and Future Work
- Evidence: Limitation 章'Precision'条目报告两种手的回差/摩擦迟滞现象、单方向精确结论及 XHand 的时间/重启漂移。
- Quote: “Consequently, when fitting regression models between encoder and hand motor values, we can typically ensure precision in only “one direction”—either when closing the hand or opening it. This inevitably causes minor discrepancies in the inpainting and action mapping processes.”
- Authors: mengda-xu; han-zhang; yifan-hou; et al.

### EA-EGOPREC-2026-0434

- Claim: DexUMI 的关节真值存在机械失效模式：3D 打印外骨骼在人手操作力作用下会发生形变，此时编码器无法捕获该形变，导致机器人手指位置与外骨骼实际手指位置不对齐。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.21864](https://arxiv.org/abs/2505.21864) DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation
- Locator: 7 Limitation and Future Work
- Evidence: Limitation 章 Material Limitations 条目与附录 A.1 均报告：人手力使 3D 打印外骨骼形变、编码器读数不含形变、机器人手指位置与外骨骼实际位置错位。
- Quote: “we sometimes found that encoders cannot precisely capture human motion due to 3D printing material strength limitations; occasionally, the human hand slightly distorts the exoskeleton linkage when manipulating objects. In such cases, encoders are unable to capture this distortion.”
- Authors: mengda-xu; han-zhang; yifan-hou; et al.

### EA-EGOPREC-2026-0080

- Claim: 仅在 ego 人类视频上预训练的 EgoVLA，不经机器人数据微调直接部署时，在基准全部任务上成功率为 0%；失败源于外观、感知与运动学失配。
- Stance: `limit` | Confidence: `direct`
- Paper: [2507.12440](https://arxiv.org/abs/2507.12440) EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
- Locator: 5.2 Humanoid Robot Evaluation
- Evidence: 5.2 节 zero-shot 段落明确报告 0% 成功率与失配归因。
- Quote: “zero-shot deployment on humanoid robots without fine-tuning on robot data results in 0% success across all tasks.”
- Authors: ruihan-yang; qinxi-yu; yecheng-wu; et al.

### EA-EGOPREC-2026-0358

- Claim: 作者明确承认：其方法依赖单目手部姿态估计器对齐机器人 overlay，而这些模型在快速运动或重度遮挡的帧上表现差，这类帧必须从训练数据集中丢弃；overlay 质量随手部估计器进步而提升。
- Stance: `limit` | Confidence: `direct`
- Paper: [2508.09976](https://arxiv.org/abs/2508.09976) Masquerade: Learning from In-the-wild Human Videos using Data-Editing
- Locator: V. LIMITATIONS AND FUTURE WORK
- Evidence: Limitations 第一条即手部姿态估计器在快运动/重遮挡失效且帧须丢弃。
- Quote: “First, our method relies on hand-pose estimators to align robot overlays from monocular images. These models perform poorly on frames with fast motions or heavy occlusions, and such frames must be discarded from our training dataset. However, this also means that as hand-pose estimators improve, our overlays will too.”
- Authors: marion-lepert; jiaying-fang; jeannette-bohg

### EA-EGOPREC-2026-0090

- Claim: OpenEgo 虽把六个 ego 数据集统一为 MANO-21 相机系手部轨迹，但手部 3D 标注精度随来源混合：无原生灵巧标注的 CaptainCook4D 全靠 2D 关键点检测+RGB-D 深度反投影重建，HOI4D 缺姿态帧亦回退此法，作者明确声明此类来源的 3D 关节质量取决于关键点估计器与深度传感；遮挡/缺失关节仅以二值可见性掩码标记并在训练中屏蔽，数据集不提供逐来源的精度区分。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05513](https://arxiv.org/abs/2509.05513) OpenEgo: A Large-Scale Multimodal Egocentric Dataset for Dexterous Manipulation
- Locator: 3 OpenEgo Dataset; 5 Conclusion
- Evidence: Sec 3 逐源管线：CaptainCook4D 'no native hand pose; detect 2D landmarks and back-project with depth'，HOI4D 缺帧 'fall back to landmark detection and depth back-projection'；Sec 5 局限(3) '3D joint quality depends on the landmark estimator and depth sensing'；Sec 3 末可见性掩码仅标记遮挡/缺失。
- Quote: “For sources lacking dexterous labels, 3D joint quality depends on the landmark estimator and depth sensing”
- Authors: ahad-jawaid; yu-xiang

### EA-EGOPREC-2026-0105

- Claim: 缓解的边界：即便检测噪声经三级吸收、域差经映射+MixUp 桥接，残余失败仍集中在硬件/接触层面——Robotiq 薄指尖致 Push 轨迹不稳、掌心间隙致锅铲夹持失效，Ability 短拇指致抓取错位、锤击任务 0.0 SR，Allegro 大手握不稳锅铲（Flip ≤0.2 SR）；作者自述更大域差（本体与人类平均动作距离差异显著或视觉外观差异大）下性能仍退化，且各本体收益幅度不一致。检测链治理到位后，末端可用性的瓶颈转移到本体机械结构与接触交互。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.10952](https://arxiv.org/abs/2509.10952) ImMimic: Cross-Domain Imitation from Human Videos via Mapping and Interpolation
- Locator: 7 Limitations
- Evidence: 5 Core Results 与 Appendix E.5 按本体归纳失败案例（薄指尖、掌心间隙、短拇指、大手）；7 Limitations 自述大域差退化与收益不一致两条局限；Tab.1 中 Hammer-Ability 0.0、Flip-Allegro 0.2 与失败归因互证。
- Quote: “though ImMimic outperforms baselines across embodiments in most of the tasks, its performance is still degraded under even larger domain gaps, such as significant differences in average action dis- tances between embodiments and humans, or major visual appearance differences.”
- Authors: yangcen-liu; woo-chul-shin; yunhai-han; et al.

### EA-EGOPREC-2026-0325

- Claim: 三个模型的单试次成功率（SR@1）均明显低于其平均成功率：RynnVLA-001 平均 90.6% 而 SR@1 仅 56.7%，Pi0 70.4%/56.3%，GR00T N1.5 55.6%/37.2%；作者自述较低的 SR@1 表明物体定位精度距可靠单次成功仍有较大提升空间。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.15212](https://arxiv.org/abs/2509.15212) RynnVLA-001: Using Human Demonstrations to Improve Robot Manipulation
- Locator: 5.2 Comparison with SoTA methods / Method, Table 1
- Evidence: Table 1 给出三模型任务成功率、平均成功率与 SR@1；5.2 正文自述 SR@1 偏低指向定位精度瓶颈。（extraction 将 Table 1 表体切到第一个 'Method' 表面，5.2 正文亦在其中，故用复合定位器。）
- Quote: “The relatively low SR@1 values for all three models suggest that there is still a large zoom for improving object localization accuracy to achieve reliable single-trial success.”
- Authors: yuming-jiang; siteng-huang; shengke-xue; et al.

### EA-EGOPREC-2026-0317

- Claim: 轨迹相似性度量的精度直接决定迁移性能：把 DTW 伪配对换成简单 MSE 后，Drawer 分布内成功率从 47% 降至 14%（正文行文写 47%→17%，与表 2 的 14% 存在内部不一致）、行为泛化从 33% 降至 17%，是三项消融中分布内降幅最大者；作者另定性指出 DTW 在轨迹跨阶段与极端视角偏移下会误配。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.19626](https://arxiv.org/abs/2509.19626) EgoBridge: Domain Adaptation for Generalizable Imitation from Egocentric Human Data
- Locator: 5.3 Results
- Evidence: Table 2 给出四行消融数字；5.3 消融段给出最大降幅归因；附录 I 给出 DTW 失效模式。
- Quote: “replacing the cost function with MSE leads to the largest performance drop for in- distribution policy success rate from 47% to 17%, seen in Tab. 2, which emphasizes the importance of creating semantically similar pseudo-pairs”
- Authors: ryan-punamiya; dhruv-patel; patcharapong-aphiwetsa; et al.

### EA-EGOPREC-2026-0330

- Claim: 该管线的监督信号止于刚体物体层面：夹爪状态无法从 ego 视频获得，动作被截断为 9 维（6DoF 位移、不含夹爪），因此无法监督抓取闭合与手指级控制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: C. Policy Training
- Evidence: Action Representation 小节原话说明因 III-B 无法获得夹爪状态，每个动作为 9 维向量；问题定义节也说明预训练中状态与动作均在无夹爪的末端执行器空间近似。
- Quote: “Action Representation. During pre-training on our dataset, an action is represented as the displacement of the 6DoF 0 9 18 27 36 45 27 26 18 21 23 Scratch LAPA (Sthv2) LAPA (Ours) Ours Ours + BridgeData V2 (b)SIMPLER Average 0 20 40 60 80 68 60 707070 55 45 70 60 45 38 20 35 45 50 34 30 353535 00000 AverageCarrot - Pot Carrot - Bowl Onion - Pot Onion - Bowl (a) Real Robot Tasks % Success Rate Fig. 5: Performance of baselines and our dataset across manipulation tasks. “ObjectA – ObjectB” denote”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGOPREC-2026-0331

- Claim: 单目 ego 视频的 3D 轨迹恢复依赖相机内参：Ego4D 不提供 EgoScaler 所需内参，需先用 COLMAP 估计，找不到满足特征匹配与几何约束（最小内点数、最大重投影误差）的初始图像对时，该样本被直接剔除。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.21986](https://arxiv.org/abs/2509.21986) Developing Vision-Language-Action Model from Egocentric Videos
- Locator: B. Pre-training Dataset Construction
- Evidence: Egocentric Video Resources 小节说明 Ego4D 无内参、用 COLMAP 预估计、无有效初始对则剔除样本。
- Quote: “Unlike the other datasets, Ego4D does not provide camera intrinsics required by EgoScaler to reconstruct 3D trajectories. We therefore estimate them in advance using COLMAP [53], [54]. COLMAP searches for an initial image pair that satisfies predefined feature- matching and geometric constraints, such as a minimum number of inliers and a maximum re-projection error. If no valid pair is found, we exclude the corresponding instance from our dataset.”
- Authors: tomoya-yoshida; shuhei-kurita; taichi-nishimura; et al.

### EA-EGOPREC-2026-0336

- Claim: 作者自述三类局限：系统沉重不利于长时间采集；机器人主动头运动范围可超出人体自然范围、重定向可能因此受限；SPARKS 为固定启发式、不能自适应更新记忆。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.00153](https://arxiv.org/abs/2511.00153) EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations
- Locator: VI. CONCLUSION
- Evidence: VI. CONCLUSION 开头连续陈述三点局限。
- Quote: “While EgoMI significantly narrows the embodiment gap, several limitations remain. The system is heavy and difficult to use for long durations for certain users. Physical embodiment mismatches also persist: for example, the robot’s actuated head can move beyond natural human ranges, so retargeting may constrain performance. SPARKS, though effective, uses a fixed scoring heuristic and does not adaptively update memory; more intelligent conditioning mechanisms could further improve performance.”
- Authors: justin-yu; yide-shentu; di-wu; et al.

### EA-EGOPREC-2026-0534

- Claim: 更低的整体感知相似度误差（embedding L2）并不意味着手部位置建模更准：PEVA* 的 L2 略优于 DexWM（0.62/0.49 vs 0.67/0.51），但 PCK@20 更低（56/63 vs 60/68），DexWM 平均 PCK@20 高出 5 个百分点以上。
- Stance: `limit` | Confidence: `direct`
- Paper: [2512.13644](https://arxiv.org/abs/2512.13644) World Models for Learning Dexterous Hand-Object Interactions from Human Videos
- Locator: 4.2 Ablation Studies
- Evidence: 表 3 给出三模型 L2 与 PCK@20 对照，表注与 4.4 节正文均指出 L2 更低不等于手部位置更准。
- Quote: “We find that lower perceptual similarity score (Embedding L2 Error) does not always reflect more accurate hand location, which is reliably captured by estimating the hands position, measured by percentage of correct keypoints (PCK).”
- Authors: raktim-gautam-goswami; amir-bar; david-fan; et al.

### EA-EGOPREC-2026-0537

- Claim: DexWM 规划失败模式分解显示：grasp 任务失败中 20% 为 Last cm 末端误差（到达目标区域但差最后几厘米）、18% 为隐状态漂移（世界模型状态预测随时间逐渐漂移）；reach 任务 Last cm 占 24%。
- Stance: `limit` | Confidence: `direct`
- Paper: [2512.13644](https://arxiv.org/abs/2512.13644) World Models for Learning Dexterous Hand-Object Interactions from Human Videos
- Locator: Appendix
- Evidence: 附录 C.6 表 6 将失败分为接触动态/掉落/Last cm/状态漂移四类并给出各任务百分比；正文定义了 Last cm 与 State Drift 的失效机理。
- Quote: “Last cm errors occur when the robot reaches the target region but fails due to small inaccuracies in the final few centimeters. State Drift denotes failures where the world model’s state prediction gradually drifts over time.”
- Authors: raktim-gautam-goswami; amir-bar; david-fan; et al.

### EA-EGOPREC-2026-0543

- Claim: 作者明确将人类 ego 数据定位为机器人数据的互补而非替代：机器人 ego 监督对物理落地仍然关键，与该方向结合可进一步提升性能上限。
- Stance: `limit` | Confidence: `direct`
- Paper: [2512.16793](https://arxiv.org/abs/2512.16793) PhysBrain: Human Egocentric Data as a Bridge from Vision Language Models to Physical Intelligence
- Locator: 1 Introduction
- Evidence: 1 Introduction 贡献段前的定位声明：该方向是互补而非替代，机器人 ego 监督对 physical grounding 仍关键。
- Quote: “This direction is complementary rather than a replacement for robot data: robot egocentric supervision remains critical for physical grounding and can further raise the performance ceiling when combined with our approach.”
- Authors: xiaopeng-lin; shijie-lian; bin-yu; et al.

### EA-EGOPREC-2026-0530

- Claim: 在采集范式对比中，基于 VR 的手部追踪只提供 2D 手部骨架且受视觉遮挡影响，而融合 IMU/IR/鱼眼视觉的 Oracle Suite 在遮挡下仍能提供准确的 3D 手部骨架。
- Stance: `limit` | Confidence: `direct`
- Paper: [2512.24310](https://arxiv.org/abs/2512.24310) World In Your Hands: A Large-Scale and Open-source Ecosystem for Learning Human-centric Manipulation in the Wild
- Locator: Appendix
- Evidence: 附录 A.2 质量对比：VR 手部追踪仅 2D 骨架且受遮挡影响；Oracle Suite 提供遮挡下准确的 3D 骨架。
- Quote: “Quality: VR-based hand tracking only provides 2D hand skeletons and suffers from visual occlusion. In contrast. In comparison, the Oracle Suite provides accurate 3D hand skeletons, even if under visual occlusion.”
- Authors: tars-robotics; yupeng-zheng; jichao-peng; et al.

### EA-EGOPREC-2026-0408

- Claim: 迁移有效性随操作精度要求上升而下降：在精度关键子步 Cart Stowing s2，Human-only 仅 5%，低于 Robot-only 的 15%；共同训练达 60%，说明人类数据提供的有用先验需与机器人演示结合才在精密阶段生效。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.10106](https://arxiv.org/abs/2602.10106) EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
- Locator: C. Which subskill benefits most from the data transfer?
- Evidence: IV.C 正文给出 5%/15%/60% 三个数字，Table I 同行数据一致。
- Quote: “However, for precision-critical phases such as Cart Stowing s2, Human-only achieves only 5% versus Robot-only’s 15%. Notably, Co-training reaches 60% on this subtask, indicating that human data provides useful priors that become effective when combined with robot demos.”
- Authors: modi-shi; shijia-peng; jin-chen; et al.

### EA-EGOPREC-2026-0409

- Claim: 作者自述 delta 末端位姿的根本局限：人手朝向与机器人夹爪朝向的对应关系有歧义、难以仅凭视觉观测推断；无本体感知输入时精确旋转迁移仍然困难，策略无法从 ego 图像可靠区分期望末端朝向，限制精细旋转控制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.10106](https://arxiv.org/abs/2602.10106) EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
- Locator: V. DISCUSSIONS
- Evidence: Sec V Action Representation 段落与 Sec VI 局限均明确陈述朝向歧义问题。
- Quote: “However, delta end-effector poses present a fundamental limitation: the correspondence between human hand orien- tation and robot gripper orientation is ambiguous. While we define explicit pose correspondences, these mappings are difficult to infer from visual observations alone. Consequently, without proprioceptive input, precise rotation transfer remains challenging—the policy cannot reliably disambiguate intended end-effector orientations from egocentric images, limiting fine- grained rotatio”
- Authors: modi-shi; shijia-peng; jin-chen; et al.

### EA-EGOPREC-2026-0414

- Claim: 朴素地将头部 RGB 直接输入策略并回归 6-DoF 头部动作，在两个任务上成功率为 0%；作者归因于视角/外观失配造成 OOD，并指出同时追踪 6-DoF 头部与手部轨迹常导致大追踪误差并违反机器人运动学约束。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.03243](https://arxiv.org/abs/2603.03243) HoMMI: Learning Whole-Body Mobile Manipulation from Human Demonstrations
- Locator: D. Findings Summary
- Evidence: F3 结论与 VII.A/VII.C 基线结果一致（RGB-Only 0%/45%/0%）。
- Quote: “Directly feeding the head RGB to the policy and regressing the head motion leads to brittle grasping and unstable motions, yielding a 0% success rate on two tasks, indicating a significant OOD shift due to viewpoint/appearance mismatch. Tracking 6-DoF head and hand trajectories together often leads to large tracking errors and violates the robot’s kinematic constraints (Fig. 5).”
- Authors: xiaomeng-xu; jisang-park; han-zhang; et al.

### EA-EGOPREC-2026-0498

- Claim: CDF-Glove 作者明确承认其手部传感链存在编码器信号漂移与零偏波动、PCB 引起的控制延迟等误差来源，并将『集成绳驱控制策略以进一步降低追踪误差』列为在途工作——即手套式直接传感的追踪误差并未被消除，而是以漂移/零偏/延迟形态持续存在。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.05804](https://arxiv.org/abs/2603.05804) CDF-Glove: A Cable-Driven Force Feedback Glove for Dexterous Teleoperation
- Locator: VI. CONCLUSION AND FUTURE WORK
- Evidence: VI 章 limitation 段逐字列出编码器信号漂移、零偏波动、PCB 控制延迟，并给出以降低追踪误差为目标的后续工作。
- Quote: “Current limitations include restricted force output, lack of complex haptic feed- back, encoder signal drift and zero-offset fluctuation, as well as PCB-induced control latency. Ongoing work will focus on enhancing the force output, optimizing the PCB design to minimize latency, and integrating cable-driven control strategies [25] to further reduce tracking errors.”
- Authors: huayue-liang; ruochong-li; yaodong-yang; et al.

### EA-EGOPREC-2026-0023

- Claim: 3PoinTr 的真实世界 3D 点轨监督来自全自动伪标签管线：CoTracker3 提取 2D 点轨迹与可见性掩码，FoundationStereo 立体深度将 2D 轨迹提升为 3D，SAM3 以文本提示 'human arm' 分割并剔除人臂点；作者承认该方法在数据采集时依赖准确的 2D 点追踪，而追踪在透明物体、遮挡物体、反光物体与阴影条件下会失败。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.08485](https://arxiv.org/abs/2603.08485) 3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos
- Locator: Appendix G Future Work (extraction section '20 Robot Demos')
- Evidence: Appendix D 逐字描述三步伪标签管线；Appendix G 逐字陈述对准确 2D 追踪的依赖及四类失败条件。两处的组合（管线构成+失败条件）均为作者直接陈述。
- Quote: “3PoinTr also relies on accurate 2D point tracking at data collection time, which can fail under certain conditions such as transparent objects, occluded objects, reflective objects, and shadows.”
- Authors: adam-hung; bardienus-p-duisterhof; jeffrey-ichnowski

### EA-EGOPREC-2026-0458

- Claim: 陆上 RGB 输入的 affordance 模型向水下迁移很差（严重外观偏移），故系统改用单目深度作为 affordance 输入；水下成像的波长相关衰减、散射/后向散射、浊度与快速变化的光照和焦散会使同一环境内的外观发生显著漂移。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.27012](https://arxiv.org/abs/2603.27012) UMI-Underwater: Learning Underwater Manipulation without Underwater Teleoperation
- Locator: I. INTRODUCTION
- Evidence: III-C 声明 RGB affordance 跨域差是改用深度的直接原因；I. INTRODUCTION 列举水下感知退化因子；IV-D 的 0% 崩溃提供实证。
- Quote: “wavelength-dependent attenuation, scattering/backscatter, tur- bidity, and rapidly changing illumination and caustics”
- Authors: hao-li; long-yin-chung; jack-goler; et al.

### EA-EGOPREC-2026-0459

- Claim: 部署期存在 overshoot 诱发的目标切换失效：ROV 过冲使目标部分出画或与 goal 规格错位，affordance 模型转而对保持可见的干扰物给出高置信度，把策略引向错误物体；该失效还会使恢复策略反向重追到干扰物而非原目标。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.27012](https://arxiv.org/abs/2603.27012) UMI-Underwater: Learning Underwater Manipulation without Underwater Teleoperation
- Locator: E. Novel-Object Generalization via On-Land Pretraining
- Evidence: IV-E 后段 Failure mode 明确描述该失效链及其对恢复策略的破坏，并给出低层控制改进与时序一致性两处缓解方向。
- Quote: “an overshoot-induced target switch can cause recovery to re-approach the distractor rather than returning to the original goal.”
- Authors: hao-li; long-yin-chung; jack-goler; et al.

### EA-EGOPREC-2026-0385

- Claim: 在 Can on Plate 任务上，作者将 WARPED 略低于 UMI 的成功率归因于物体位姿跟踪噪声给演示引入的轻微不一致，说明即使整体管线可用，跟踪噪声仍会作为残余误差进入重定向后的末端轨迹数据。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.10809](https://arxiv.org/abs/2604.10809) WARPED: Wrist-Aligned Rendering for Robot Policy Learning from Egocentric Human Demonstrations
- Locator: D. Results
- Evidence: IV-D 中 WARPED 与 UMI 对比段的作者归因。
- Quote: “In contrast, WARPED exhibits a slightly lower success, possibly as a result of the noise in object pose tracking which introduces minor variability in the demonstrations.”
- Authors: harry-freeman; chung-hee-kim; george-kantor

### EA-EGOPREC-2026-0388

- Claim: WARPED 在两个失效模式上暴露了估计精度的下限：小且平贴桌面的物体使位姿估计与重定向更困难（Wipe Brush 11/20，低于遥操作 15/20），物体被完全遮挡时管线直接失败。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.10809](https://arxiv.org/abs/2604.10809) WARPED: Wrist-Aligned Rendering for Robot Policy Learning from Egocentric Human Demonstrations
- Locator: D. Results; V. DISCUSSION AND LIMITATIONS
- Evidence: IV-D 结果与 V 局限分别给出两个失效条件。
- Quote: “Additionally, the pipeline fails when the manipulated object becomes fully occluded, which is also a limitation of state-of-the-art object tracking methods”
- Authors: harry-freeman; chung-hee-kim; george-kantor

### EA-EGOPREC-2026-0547

- Claim: 在 98 会话（1.19M 帧、25.2 小时）上，WiLoR 手部检测仅覆盖 86.2% 的帧（平均置信度 0.73），另有 0.02% 帧因 LiDAR 零深度返回被阈值过滤丢弃。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: APPENDIX
- Evidence: 附录 VIII 首段：检测成功率 86.2%、平均 WiLoR 置信度 0.73；247 帧（0.02%）零深度经 z>0.01m 阈值丢弃。
- Quote: “Hand de- tection succeeds on 86.2% of frames (mean WiLoR confidence 0.73); 247 frames with zero LiDAR depth returns (0.02%) are discarded via a z > 0.01 m threshold before computing metrics”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathor; et al.

### EA-EGOPREC-2026-0550

- Claim: 作者明确声明下游验证的边界：训练信号实验是开环的（held-out 手部动作预测、无闭环机器人 rollout），证明的是可训练性而非策略级任务成功率；且管线依赖 iPhone Pro，Android/ARCore 的 VIO 精度更低且缺 LiDAR 深度。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.05945](https://arxiv.org/abs/2605.05945) MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
- Locator: VI. LIMITATIONS
- Evidence: VI. LIMITATIONS：开环验证声明与平台依赖声明（ARCore VIO 精度更低、无 LiDAR）。
- Quote: “Our training-signal experiment is open-loop (we evaluate held-out hand-action prediction and perform no closed-loop robot rollout), so it demonstrates trainability rather than policy-level task success”
- Authors: senthil-palanisamy; abhishek-anand; satpal-singh-rathor; et al.

### EA-EGOPREC-2026-0074

- Claim: 单 RGB-D 相机采集在手势被遮挡时关键点检测可能不完整；作者采用的缓解手段（控制腕部时采用参考姿态+局部偏移、让手掌尽量朝向相机）以减少遮挡，但承认这会轻微限制腕部动作的灵活性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.03268](https://arxiv.org/abs/2606.03268) EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations
- Locator: 5 Conclusion and Limitations
- Evidence: 第 5 节 Limitations 原文完整陈述遮挡问题、缓解手段及其代价；与未来工作（多相机融合）呼应。
- Quote: “Our method uses a single RGB-D camera to capture hand motions. When gestures are occluded, keypoint detection may be incomplete. To mitigate this issue, we adopt a reference pose with local offsets when controlling the wrist, ensuring the palm faces the camera as much as possible, which reduces occlusion. However, this approach can slightly limit the dexterity of wrist motions.”
- Authors: qian-zhao-217607; xin-tong; chengdong-wu; et al.

### EA-EGOPREC-2026-0438

- Claim: RealDexUMI 作者指认 FastUMI-100k 与 TouchGuide 等先前系统通过启发式坐标对齐把演示轨迹映射到机器人执行帧，认为该做法把演示硬编码到预定义结构化工作空间、并把采集绑定到部署时的机器人基座帧，与非结构化场景下的 robot-free 采集不兼容。
- Stance: `limit` | Confidence: `citation-supported`
- Paper: [2606.06033](https://arxiv.org/abs/2606.06033) RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning
- Locator: 4.1 Policy Interface
- Evidence: 4.1 在论证相对标签动机时点名 FastUMI[25]（即 FastUMI-100k）与 TouchGuide[50] 的启发式坐标对齐并给出三点批评；该陈述是对他文的概括，需结合被引原文核实。
- Quote: “Prior systems such as FastUMI [25] and TouchGuide [50] map demonstration trajectories into robot execution frames through heuristic coordinate alignment. This alignment hard-codes demonstrations to a predefined structured workspace and ties data collection to a deployment-time robot base frame.”
- Authors: chaoyi-xu; yixuan-jiang; jiahui-huan; et al.

### EA-EGOPREC-2026-0440

- Claim: 在采集端接口对比中，Manus 手套重定向基线在 cap twisting 上成功，但在依赖精确指尖捏取的 tea picking（用镊子）上表现急剧下降；作者据此指出：丰富的人手运动本身在必须重定向到机器人手时并不充分。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.06033](https://arxiv.org/abs/2606.06033) RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning
- Locator: 5.3 Collection-Time Dexterity
- Evidence: 5.3 报告 Manus 基线两任务的反差表现并给出'must be retargeted to a robot hand'的归因；Fig. 8 给出逐方法成功次数（同操作者、10 分钟练习后评估）。
- Quote: “However, its performance drops sharply on tea picking, where tweezer use depends on precise fingertip pinching. This contrast shows that rich human-hand motion alone is insufficient when it must be retargeted to a robot hand.”
- Authors: chaoyi-xu; yixuan-jiang; jiahui-huan; et al.

### EA-EGOPREC-2026-0383

- Claim: 作者承认该管线在严重遮挡、反光物体、快速运动或手部/分割估计不准确时性能退化，即手部检测精度仍是系统性能的前置条件而非已被后处理完全解决的问题。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.08057](https://arxiv.org/abs/2606.08057) EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets
- Locator: 6 Limitations
- Evidence: Limitations 一节明确列出退化条件。
- Quote: “Its current pipeline mainly targets single-hand manipulation, and performance can degrade under severe occlusion, reflective objects, fast motion, or inaccurate hand/segmentation estimates”
- Authors: yichen-niu; haoran-lv; xinrui-zhang; et al.

### EA-EGOPREC-2026-0416

- Claim: 在无本体人类操作视频管线中，严重的手部自遮挡与手-物遮挡会显著降低手部运动估计精度；作者将其列为直接迁移的两大首要障碍之一，并在附录逐任务展示 HaMeR 估计的遮挡实例以解释重定向轨迹偏离演示意图。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.08828](https://arxiv.org/abs/2606.08828) Video2Sim2Real: Full-Stack Autonomous Dexterous Skill Acquisition from a Single Human Video
- Locator: 1 Introduction
- Evidence: 引言明确将'severe hand self-occlusion and hand-object occlusion→motion estimation accuracy 显著退化'列为第一挑战；附录 D.1 Fig.6 为七个任务逐一标注遮挡类型（self-occlusion / hand-object occlusion / 两者叠加）并说明其解释了重定向轨迹的偏离。
- Quote: “lenges hinder direct transfer. First, severe hand self-occlusion and hand–object occlusion during manipulation can significantly degrade motion estimation accuracy. Second, a substantial embod-”
- Authors: yunhai-han; jianuo-qiu; linhao-bai; et al.

### EA-EGOPREC-2026-0417

- Claim: 跨七任务仿真细化评测显示：对含噪重定向轨迹依赖越强的细化策略整体越差——Residual RL 成功率 49.5/52.9%、DeepMimic RL 19.5/24.3%、Pre-Contact Init 6.2/19.5%、Opt-Pre-Contact Init 1.9/14.3%、Object-only 9.5/15.7%，而本文对象中心关键帧锚定法达 91.4% 且安全率 100%；作者据此结论：直接细化重定向人类运动受限于含噪/不准的运动先验。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.08828](https://arxiv.org/abs/2606.08828) Video2Sim2Real: Full-Stack Autonomous Dexterous Skill Acquisition from a Single Human Video
- Locator: 5.1 Experiment Design
- Evidence: Table 1 跨任务均值：Success 行 RRL-F 49.5±47.7 / RRL-A 52.9±49.8 / DM-F 19.5 / DM-A 24.3 / PCI-F 6.2 / PCI-A 19.5 / OPCI-F 1.9 / OPCI-A 14.3 / Obj-F 9.5 / Obj-A 15.7 / Ours 91.4±22.7；Safety 行 Ours 100.0。5.2 正文'RL-based baselines can be limited by noisy retargeted trajectories or high-dimensional state spaces'与附录 D.1 Steak Seasoning 案例共同支撑归因。
- Quote: “Metric RRL-F RRL-A DM-F DM-A PCI-F PCI-A OPCI-F OPCI-A Obj-F Obj-A Ours Success ↑ 49.5±47.7 52.9±49.8 19.5±33.4 24.3±41.5 6.2±12.5 19.5±37.5 1.9±2.6 14.3±26.2 9.5±25.2 15.7±26.9 91.4±22.7”
- Authors: yunhai-han; jianuo-qiu; linhao-bai; et al.

### EA-EGOPREC-2026-0027

- Claim: 即使关键点表征松弛了人-机耦合，预测的腕/指尖轨迹仍有一部分在部署机器人上运动学不可行并引入非平凡 IK 误差；真机剩余失败以低层运动问题为主（动作定位不精确与接触力不足），且整条管线继承 VLM、分割、深度与手部追踪模型的失败模式。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.10614](https://arxiv.org/abs/2606.10614) Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations
- Locator: 5 Conclusion
- Evidence: 5 节 Limitations 逐字给出 IK 误差与继承视觉模型失败模式两条；4.2 节逐字给出剩余失败以低层运动问题为主的观察。
- Quote: “Limitations. Several limitations remain. First, although the keypoint representation loosens the coupling between human and robot hand actions, some predicted trajectories are still kinematically infeasible on the deployment robot and induce non-trivial IK error.”
- Authors: beomjun-kim; seong-hyeon-park; seunghoon-sim; et al.

### EA-EGOPREC-2026-0397

- Claim: LUCID 的人视频监督依赖四级提取链（ViPE 深度/相机、SAM 3.1 分割、DenseTrack3Dv2 物体点追踪、WiLoR 手部 MANO 网格拟合），作者自述每一级都是数据提取与部署时的故障点，in-hand occlusion 与无纹理物体等感知故障会沿链传播到 sensorimotor 策略。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.11628](https://arxiv.org/abs/2606.11628) LUCID: Learning Embodiment-Agnostic Intent Models from Unstructured Human Videos for Scalable Dexterous Robot Skill Acquisition
- Locator: 5 Limitations
- Evidence: 5 Limitations (1) 逐项命名四个组件并称各自引入故障点，明确'Perception faults like in-hand occlusion or textureless objects propagate down the chain to the sensorimotor policy'；3.1 详述四级管线职责。
- Quote: “(1) Pipeline brittleness. The system is over-modularized; SAM 3.1, DenseTrack3Dv2, ViPE, and WiLoR each introduce a failure point during data extraction and at deployment. Perception faults like in-hand occlusion or textureless objects propagate down the chain to the sensorimotor policy.”
- Authors: harsh-gupta; guanya-shi; wenzhen-yuan

### EA-EGOPREC-2026-0346

- Claim: 作者自述两项局限：方法仅适配刚体物体，铰接/可变形体未覆盖；仿真采用浮动基座假设、省略具体机械臂形态，关节可达性需依赖外部 IK 求解器，端到端全身可行性留作未来工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.16436](https://arxiv.org/abs/2606.16436) V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
- Locator: 5 Limitations
- Evidence: 5 Limitations 整节两条局限与 claim 对应。
- Quote: “While our framework successfully facilitates dexterous manipulation learning from monocular videos, certain constraints remain. Currently, our methodology is tailored for rigid-body objects; extending it to articulated or deformable entities remains unexplored due to their high degrees of freedom and complex contact physics. Furthermore, the simulation enforces a floating-base as- sumption that omits specific robot arm morphologies, requiring external inverse kinematics solvers to manage joint r”
- Authors: kaihan-chen; yanming-shao; haifeng-ji; et al.

### EA-EGOPREC-2026-0395

- Claim: 对 100DOH 采样的 2,000 条 10 秒片段，仅 187 条（9%）存在有意义手-物交互，最终 83 条（4%）通过重建质检：41 条因手或物体出画、29 条因无活动或跨镜头、14 条因相机运动、10 条因 SAM 3D 失败；作者估计不做适当预处理过滤将承受约 20× 的数据惩罚。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19333](https://arxiv.org/abs/2606.19333) Do as I Do: Dexterous Manipulation Data from Everyday Human Videos
- Locator: 4.5 Human Data Filtering Playbook
- Evidence: 4.5 playbook 逐类给出过滤漏斗数字：2000→187（有意义交互）→扣除出画 41、跨镜头 29、相机运动 14、SAM 3D 失败 10、其他 10→83（4%）。
- Quote: “Out of the 2,000 videos sampled from 100DOH, only 83 (4%) survive our quality check for the reconstruction pass. Even in the best case, we foresee 107 clips, or roughly 5% of the data, being directly relevant for learning dexterous manipulation, implying a 20× penalty in not properly preprocessing and filtering internet videos for robot learning.”
- Authors: bhawna-paliwal; haritheja-etukuru; william-liang; et al.

### EA-EGOPREC-2026-0396

- Claim: 作者自述该管线假设刚性物体与半准确米制单目深度，且单目观测存在真实手-物距离歧义、难以区分物理接触与视觉遮挡；重建仅覆盖手与单个物体，无法推理环境约束，仿真器近似为真实世界表现设定上界。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.19333](https://arxiv.org/abs/2606.19333) Do as I Do: Dexterous Manipulation Data from Everyday Human Videos
- Locator: 5 Conclusion (Limitations)
- Evidence: 5 Conclusion 的 Limitations 段逐项列出刚性物体、米制深度、手-物距离歧义、接触 vs 遮挡、单物体场景、仿真器近似六条局限。
- Quote: “Our approach assumes rigid objects and semi-accurate metric depth predictions from monocular RGB, and may fail when either assumption doesn’t hold. Monocular observations also suffer from ambiguity in the true hand-object distance, making it difficult to distinguish physical contact from mere visual occlusion.”
- Authors: bhawna-paliwal; haritheja-etukuru; william-liang; et al.

### EA-EGOPREC-2026-0034

- Claim: TopoRetarget 依赖上游人类参考运动的质量：它能处理源运动穿透造成的接触失真，但对 virtual contact（手指意图与物体交互但未实际触碰物体表面）效果差，作者将纠正此类缺失接触列为未来工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.16272](https://arxiv.org/abs/2606.16272) TopoRetarget: Interaction-Preserving Retargeting for Dexterous Manipulation
- Locator: 7 Limitations and Future Work
- Evidence: 局限性节明确承认方法依赖上游参考质量，并区分两类源误差：穿透型接触失真可处理，而 virtual contact（缺失接触）不可处理。
- Quote: “TopoRetarget depends on the quality of the upstream human reference motion. Our method can handle contact distortion caused by penetration in the source motion, but it is less effective for virtual contacts, where the source finger is intended to interact with the object but does not actually touch the object surface.”
- Authors: jielin-wu; shenzhe-yao; guanqi-he; et al.

### EA-EGOPREC-2026-0099

- Claim: 缓解手段的代价边界：丢弃人类旋转监督使失败集中于接触中需要精确末端构型的任务——'插吸管'与'开抽屉'中策略表现出明确任务意图，但在抓稳吸管或转动腕部建立有效拉拽接触等关键步骤失败；作者明确承认这些失败与丢弃旋转监督的设计选择一致，并指出引入有限但可靠的旋转线索是未来方向；此外共训后机器人难以抓取薄物体，归因于观测/本体 gap 与人类动作中不可避免的噪声。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.28133](https://arxiv.org/abs/2606.28133) Translation as a Bridging Action: Transferring Manipulation Skills from Humans to Robots
- Locator: 5.9 Failure Case Analysis; 6 Conclusions
- Evidence: 5.9 报告失败集中于插吸管/开抽屉的精确末端构型步骤，并明示与丢弃旋转监督一致；6 Conclusions 自述局限并报告薄物体抓取困难的双因素归因。
- Quote: “These failures are consistent with our design choice of discarding rotational supervision from human data, and point to incorporating limited, reliable rotation cues as a promising direction for future work.”
- Authors: sijin-chen; kaixuan-jiang; haixin-shi; et al.

### EA-EGOPREC-2026-0041

- Claim: 在全局手基坐标系中施加运动方向一致性的重定向目标（如 GeoRT）隐含假设指尖测量已良好标定；实践中手套传感器标定误差会在测量与真实指尖位置之间引入平移或旋转差异，使全局测量的运动方向失准，即标定/坐标系对齐误差经全局方向目标直接传播为重定向运动失真。AnyDexRT 改为在局部坐标系中保持运动方向（局部运动损失，与 partial Chamfer、距离保持联合训练），作者陈述这使重定向行为对标定误差更不敏感、更符合操作者意图。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.08341](https://arxiv.org/abs/2607.08341) AnyDexRT: Calibration-Free Dexterous Hand Retargeting with Few-Shot Human Guidance
- Locator: 6 DoF 7 DoF (mangled extraction heading spanning Sections 1-4.1 Setup, passage in 3.2 Local Motion Preservation)
- Evidence: 3.2 节 Local Motion Preservation：GeoRT 在全局手基系施加方向一致性、隐含假设指尖测量良好标定；手套标定误差引入平移/旋转差异使全局方向失准（该句因分页在提取文本中被图 3 噪声截断，前后两半均已核对）；本节末句陈述局部运动损失使重定向对标定误差更不敏感。4.1 节 Fig 5 的 ±45°/±90° 旋转扰动实验为该机制提供实证（见 findings，定位器不可解析）。
- Quote: “Local Motion Preservation Partial correspondence aligns fingertip spaces, but does not guarantee that local motion directions are preserved. GeoRT [55] imposes directional consistency in the global hand-base frame, implicitly assuming well-calibrated fingertip measurements.”
- Authors: chenxi-wang; ying-feng; hongjie-fang; et al.

### EA-EGOPREC-2026-0114

- Claim: 作者自述主要限制为物体追踪：实际使用中手部在操作过程中部分遮挡物体，逐帧 6D 位姿追踪常因此丢失，进而污染参考轨迹与抽取的事件——即物体追踪误差沿'位姿丢失→参考轨迹污染→事件抽取错误'的路径传入重定向；次要限制为仅支持单臂（双臂事件抽取已可靠但双臂运动规划未纳入）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.09519](https://arxiv.org/abs/2607.09519) DemoBridge: A Simulation-in-the-Loop Toolkit for Single-View Human Demonstration Retargeting
- Locator: VII. LIMITATIONS
- Evidence: VII. LIMITATIONS 逐字给出物体追踪丢失→污染参考轨迹与事件的因果链及单臂限制；VI-B Fig. 3C 给出物体位姿翻转的具体实例（该 rollout 仍成功），并声明本文演示中追踪保持在任务容差内。
- Quote: “The main limitation is object tracking. In real use the hand partially occludes the object during manipulation, and the per- frame 6D pose tracker then often loses track of it. This corrupts the reference trajectory and the extracted events. A second limitation is bimanual support. The solver currently supports a single arm.”
- Authors: zehao-wang; fabien-despinoy; sergey-zakharov; et al.

### EA-EGOPREC-2026-0483

- Claim: 作者明确承认 TELEDEXTER 的真实部署依赖动捕系统进行实时手-物位姿估计，并将『替换为无标记视觉追踪系统』列为降低部署门槛、扩大适用性的未来方向，而非已验证能力。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.11481](https://arxiv.org/abs/2607.11481) Towards Human-level Dexterous Teleoperation
- Locator: 6 Limitations
- Evidence: 第 6 节 Limitations 第二段逐字陈述对动捕的依赖与无标记视觉追踪作为未来方向。
- Quote: “Our real-world deployment relies on a motion-capture system for real-time hand and object pose estimation. Replacing this with a markerless, vision-based tracking system would significantly lower the barrier to deployment and broaden the practical applicability of the framework.”
- Authors: puhao-li; zeyuan-chen; yingying-wu; et al.

### EA-EGOPREC-2026-0311

- Claim: SiMDex 的 Stage III 再排序用稠密光流聚合为 clip 级描述子对候选重打分，提供一个『独立于重定向精度』的跨本体验证信号；作者同时承认纯运动学相似性（腕部 6D 位姿+指尖位置）不含接触力、物体状态与交互语义，会产生如『手几乎不动的 drilling 片段』之类的错配，需光流纠正且算力代价非平凡。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.04196](https://arxiv.org/abs/2608.04196) SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation
- Locator: 3.2 Similarity-Based Data Mining
- Evidence: 3.2 Stage III 原文给出『independent of retargeting accuracy』的设计动机；第 6 节局限给出运动学错配实例与光流纠正代价。
- Quote: “into a clip-level descriptor and re-score by descriptor similarity, yielding a verification signal independent of retargeting accuracy.”
- Authors: nie-lin; takehiko-ohkawa; sijin-chen; et al.

### EA-EGOPREC-2026-0313

- Claim: 挖掘收益的边界：当人类池中缺乏与目标技能相似的高质量示教时（Drill 案例），检索在机器人数据稀缺时仍有帮助（0.25× 时 +8.9、0.5× 时 +13.4），但一旦机器人示教充足（1×、2×），少量被挖掘到的 drilling 样本引入的是方差而非信号，SiMDex 反而落后基线。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.04196](https://arxiv.org/abs/2608.04196) SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation
- Locator: 6 Limitations and Future Work
- Evidence: 4.4 per-task 分析与第 6 节局限共同支持该反转及其归因。
- Quote: “to the target skill, retrieval has little relevant signal to exploit and may even inject variance once robot data is sufficient.”
- Authors: nie-lin; takehiko-ohkawa; sijin-chen; et al.

### EA-EGOPREC-2026-0071

- Claim: 作者明确指出：尽管动作空间已跨本体对齐，硬件差异仍限制精细操作技能的迁移，且人类模仿数据单独可能无法捕捉高精度控制所需的本体特异策略；共享动作表示不显式建模本体特异动力学或接触约束。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.14028](https://arxiv.org/abs/2608.14028) AdvDex: Learning Dexterous Manipulation from Human Demonstrations via Joint-Aligned Actions and Adversarial Learning
- Locator: 6 Limitations and Future Work
- Evidence: 第 6 节局限性原文陈述上述两点；与 4.3 需 1000 条目标本体遥操作轨迹后训练的事实一致。
- Quote: “Although AdvDex aligns actions across embodiments, hardware differences still limit the transfer of fine-grained manipulation skills. Human imitation data alone may not capture the embodiment-specific strategies required for high-precision control.”
- Authors: zhiyue-zhao; jing-wu; hairuo-liu; et al.

### EA-EGOPREC-2026-0052

- Claim: 作者自述：人侧采集设备（Quest 头显 inside-out 追踪）本身引入运动误差与 jerkiness——尤其在快速运动、遮挡或异常体态下的 jitter、drift、不连续与肢体估计不准；由于管线是离线的，这些伪影可直接传播进重定向后的机器人轨迹，再进入策略监督。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.29940](https://arxiv.org/abs/2606.29940) WARP: Whole-Body Retargeting for Learning from Offline Human Demonstrations
- Locator: Appendix D.1 Limitations; References
- Evidence: 附录 D.1 'Human data quality' 段明确把部分重定向轨迹误差归因于采集设备，描述噪声形态（jitter/drift/discontinuities/inaccurate limb estimates）及其在离线管线中的直接传播。
- Quote: “in the retargeted trajectories can originate from the collection device itself. Inside-out tracking may introduce jitter, drift, discontinuities, or inaccurate limb estimates, especially during fast motion, occlusion, or unusual body poses. Since our pipeline is offline, these artifacts can propagate directly into the robot trajectory and then into the policy supervision.”
- Authors: zhenyang-chen; chuizheng-kong; chuye-zhang; et al.

### EA-EGOPREC-2026-0421

- Claim: 对单目人类视频重建并经两阶段优化的重定向轨迹，开环运动学回放几乎不可用：六类灵巧任务仿真平均成功率仅 5.2%，而同一参考经触觉感知 RL 学习的 DEX-X 达 65.9%（ManipTrans 式模仿 21.9%）——从含噪手部检测得到的重定向轨迹必须经物理交互学习才能转化为可用技能。
- Stance: `limit` | Confidence: `direct`
- Paper: [2609.07747](https://arxiv.org/abs/2609.07747) Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction
- Locator: 4.2 Q1: Multi-Task Dexterous Manipulation in Simulation
- Evidence: 4.2 正文：DEX-X 65.9% vs ManipTrans 21.9% vs kinematic retargeting 5.2%；DAPG 评估的五类单手任务上 61.7% vs 40.6%。Table 1 显示 Kin. Retarget 在插销、手内旋转/平移上为 0%。
- Quote: “success rate of 65.9%, compared with 21.9% for ManipTrans and 5.2% for kinematic retargeting. On the five single-hand categories evaluated by DAPG, DEX-X achieves 61.7% average success compared with 40.6% for DAPG.”
- Authors: ruoqu-chen; feixiang-ruan; liu-cao; et al.

### EA-EGOPREC-2026-0504

- Claim: 该模态对比中即便是最接近'手到机器人'映射的 VR 遥操作，其手部轨迹也来自 Oculus 手柄 IMU 位姿而非视觉手部检测；因此本研究不能量化视觉手部检测误差的传播，无本体 ego-centric 视频模态不在其评测空间内。
- Stance: `gap` | Confidence: `inference`
- Paper: [2503.07017](https://arxiv.org/abs/2503.07017) How to Train Your Robots? The Impact of Demonstration Modality on Imitation Learning
- Locator: I. INTRODUCTION
- Evidence: 前提：引言描述 VR 遥操作手柄轨迹直接映射为机器人轨迹；相关工作指出 VR 手柄由 IMU 追踪；实验节确认用 Oculus Quest 手柄位姿。推断：全文无视觉手部估计环节，故对综述问题的核心链路无直接测量。削弱条件：若其手柄位姿被视为手部检测的上界替代，则结论仅提供乐观边界。
- Quote: “With VR teleoperation, the demonstrator only needs to have a rough estimate of how their motion scales to the robot’s motion and their hand trajectory can then directly translate to robot trajectory.”
- Authors: haozhuo-li; yuchen-cui; dorsa-sadigh

### EA-EGOPREC-2026-0365

- Claim: 作者综述指出：从单目视觉输入预测手部关键点的手部姿态估计模型(如 HaMeR 一类)虽在简单场景有效，但对遮挡脆弱、时序不一致、且对背景干扰物缺乏鲁棒性。
- Stance: `gap` | Confidence: `citation-supported`
- Paper: [2505.20290](https://arxiv.org/abs/2505.20290) EgoZero: Robot Learning from Smart Glasses
- Locator: 2 Related Work
- Evidence: Related Work 末段对手部姿态估计模型[54-57]的总体评价；依赖被引工作，属作者综合判断。
- Quote: “These models are trained with imitation learning to predict hand keypoints [58] from monocular visual input. Although effective in many simple domains, these models are brittle to occlusions, temporally inconsistent, and lack robustness to background distractors.”
- Authors: vincent-liu; ademi-adeniji; haotian-zhan; et al.

### EA-EGOPREC-2026-0432

- Claim: DexUMI 的腕部（末端）6DoF 位姿由 iPhone ARKit 提供，且该追踪设备仅用于数据采集、部署端不再需要；但全文未报告 ARKit 位姿精度的任何定量评估或与独立真值的对比。
- Stance: `gap` | Confidence: `direct`
- Paper: [2505.21864](https://arxiv.org/abs/2505.21864) DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation
- Locator: 3.2 Sensor Integration; Background
- Evidence: 3.2 S.2 声明用 iPhone ARKit 捕获 6DoF 腕部位姿、仅采集需要；通读全文（含附录 D/E 传感器与采集细节）未见任何 ARKit 精度数字或真值对照实验。
- Quote: “We use iPhone ARKit to capture the 6DoF wrist pose, as smartphones represent the most accessible devices capable of providing precise spatial tracking. This tracking device is only needed for data collection, not for robot deployment.”
- Authors: mengda-xu; han-zhang; yifan-hou; et al.

### EA-EGOPREC-2026-0519

- Claim: 该数据集工作的动机断言是'人类标注昂贵且不精确'，但全文未量化人类标注的具体误差水平；其数据验收机制是仿真成功过滤而非轨迹几何误差阈值，绕开了视觉手部检测问题，因此不能为 ego 视频管线的检测精度阈值提供直接证据。
- Stance: `gap` | Confidence: `inference`
- Paper: [2506.17198](https://arxiv.org/abs/2506.17198) Dex1B: Learning with 1B Demonstrations for Dexterous Manipulation
- Locator: I. INTRODUCTION
- Evidence: 前提 1：引言将 human annotation is costly and imprecise 作为动机且全文无误差量化。前提 2：III/V 节显示验收依赖 ManiSkill/SAPIEN 仿真过滤成功轨迹。推断：本文不能回答检测精度阈值问题。削弱条件：若把仿真成功视为轨迹质量的终极代理，则其过滤机制提供了另一种验收范式。
- Quote: “they each have limitations: human annotation is costly and imprecise, optimization-based methods are slow and sensitive to initialization, and RL-based techniques lack data diversity.”
- Authors: jianglong-ye; keyi-wang; chengjing-yuan; et al.

### EA-EGOPREC-2026-0106

- Claim: 缺口：本文完整披露了手部检测-重定向管线组件，却全程未量化检测精度——无 2D/3D 关键点误差、无腕部 6DoF 位姿误差、无深度替代前后的精度对照、无检测噪声注入消融；'单目腕部平移不准'仅以工程替代决策隐式表达。且人类视频为固定第三人称 agent-view RealSense 采集（与机器人同相机同工作空间），非 ego-centric：无头动、自遮挡、出框等 ego 噪声源。因此从本文无法推出手部检测误差的可接受阈值，也不能将其噪声吸收结论外推至 ego-centric 检测条件。
- Stance: `gap` | Confidence: `inference`
- Paper: [2509.10952](https://arxiv.org/abs/2509.10952) ImMimic: Cross-Domain Imitation from Human Videos via Mapping and Interpolation
- Locator: 3.1 Hand Pose Retargeting System
- Evidence: 3.1 与 Appendix B 仅列管线组件与替代决策；4 Experiment Setups 的指标（SR/SPARC/AD）全部作用于重定向之后，无任何检测精度度量；Appendix A 明确固定 agent-view、同相机同工作空间的受控采集。
- Quote: “We use MediaPipe [51] to localize and crop the human hand in each frame. Each patch is fed into FrankMocap [52], whose SMPL-X regressor produces precise 3D positions for 21 hand joints in the local wrist frame. By projecting these joints into the depth map and solving a Perspective-n-Point problem, we recover the wrist 6D pose in camera frame.”
- Authors: yangcen-liu; woo-chul-shin; yunhai-han; et al.

### EA-EGOPREC-2026-0304

- Claim: 论文未提供任何手部/腕部姿态估计噪声或检测精度对下游轨迹与成功率影响的消融：作者自述局限只涉及单一 ego 视角的观测限制与缺第三人称预训练数据，手部轨迹精度被默认由动捕级传感保障，视觉手部检测误差→重定向末端轨迹精度这一因果链在该系统中仍未被检验。
- Stance: `gap` | Confidence: `inference`
- Paper: [2511.17366](https://arxiv.org/abs/2511.17366) METIS: Multi-Source Egocentric Training for Integrated Dexterous Vision-Language-Action Model
- Locator: 6. Conclusions and Limitations
- Evidence: 通读全文（含 5.5 消融与第 6 节局限）后确认：两项消融分别针对预训练数据组成与运动动力学表示，均无姿态噪声变量；局限节未提手部检测精度。前提：全文已覆盖方法、实验、附录 A/F 的标定细节；削弱条件：作者后续补充噪声消融。
- Quote: “several limitations remain. First, our model relies solely on egocentric observations, which may restrict its ability to perceive complete object geometry and fine interaction details.”
- Authors: yankai-fu; ning-chen; junkai-zhao; et al.

### EA-EGOPREC-2026-0531

- Claim: 在部分灵巧操作任务上所有方法的成功率持续偏低，作者将“进一步提高人类数据的采集精度”与“设计更好的人机知识迁移算法”并列为关键未来方向，即承认当前采集精度是部分任务的瓶颈之一。
- Stance: `gap` | Confidence: `direct`
- Paper: [2512.24310](https://arxiv.org/abs/2512.24310) World In Your Hands: A Large-Scale and Open-source Ecosystem for Learning Human-centric Manipulation in the Wild
- Locator: Appendix
- Evidence: 附录 D 在分析各任务成功率与失败原因后指出：部分任务所有方法成功率持续偏低，未来需提高人类数据采集精度并改进迁移算法。
- Quote: “the consistently low success rates across all methods in certain tasks highlight important directions for future research: how to further improve the collection precision of human data and how to design efficient algorithms that can better transfer knowledge from human data to dexterous manipulation tasks.”
- Authors: tars-robotics; yupeng-zheng; jichao-peng; et al.

### EA-EGOPREC-2026-0405

- Claim: 该论文未量化 HaMeR 手部姿态估计误差，也未建立检测误差→末端轨迹误差的传播或阈值分析：唯一失败分析（Fig. 5）把失败归因于策略的空间关系理解而非手部检测质量。
- Stance: `gap` | Confidence: `inference`
- Paper: [2602.11464](https://arxiv.org/abs/2602.11464) EasyMimic: A Low-Cost Framework for Robot Imitation Learning from Human Videos
- Locator: C. Further Analysis
- Evidence: 通读全文，方法与实验均未报告任何关键点/轨迹级误差指标；失败案例仅归结为空间理解不足。
- Quote: “Figure 5 illus- trates representative examples of common failure modes: In pick and place tasks, the robot occasionally releases the gripper before reaching the target location, often due to an insufficient understanding of spatial relationships.”
- Authors: tao-zhang; song-xia; ye-wang; et al.

### EA-EGOPREC-2026-0466

- Claim: DexViTac 的全局腕部轨迹由 RealSense T265 内置 VIO 输出（带置信度、无需外部标定）经自定义误差补偿与 R_c2b 自动标定后增量重定向到机器人基座；作者声明该设置可稳定精确追踪腕部轨迹，但全文未报告全局轨迹的定量精度或漂移数值。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.17851](https://arxiv.org/abs/2603.17851) DexViTac: Collecting Human Visuo-Tactile-Kinematic Demonstrations for Contact-Rich Dexterous Manipulation
- Locator: A. Hardware Design; C. Data Preprocessing
- Evidence: III-A-4 描述 T265 VIO + 误差补偿；III-C-2 给出增量重定向公式与 R_c2b 标定流程；全文检索无任何毫米/度数级轨迹精度数值。
- Quote: “Combined with a custom error- compensation algorithm, this setup enables stable and precise tracking of wrist trajectories.”
- Authors: xitong-chen; yifeng-pan; min-li; et al.

### EA-EGOPREC-2026-0490

- Claim: TeleDex 全文未提供手部关键点或腕部位姿追踪的定量精度/延迟/丢帧测量：动态任务（接物、守门、绕线）仅以『无可见追踪漂移或失控』的定性观察作为追踪质量证据。
- Stance: `gap` | Confidence: `inference`
- Paper: [2603.17065](https://arxiv.org/abs/2603.17065) TeleDex: Accessible Dexterous Teleoperation
- Locator: D. Complex Manipulation Experiments
- Evidence: IV.D 的定性声称是全文最接近追踪质量的陈述；通读 IV 全部小节与 V，所有定量指标均为任务耗时/成功率，无位姿误差、追踪频率或丢帧统计。
- Quote: “Across all scenarios, operators were able to successfully complete the tasks via performing fine-grained corrective motions in real time, without observable tracking drift or loss of control.”
- Authors: omar-rayyan; maximilian-gilles; yuchen-cui

### EA-EGOPREC-2026-0063

- Claim: 该框架的一阶线性化建立在 Remark 1 的假设上：视觉追踪/数据手套能以高频率可靠获取人手运动，使相邻步关节变化足够小；论文未对检测噪声、遮挡或低帧率输入做扰动实验，实机验证仅为定性，检测精度到重定向轨迹误差的传播未被量化。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.29213](https://arxiv.org/abs/2603.29213) Kilohertz-Safe: A Scalable Framework for Constrained Dexterous Retargeting
- Locator: A. Quadratic Programming Formulation of Hand Pose Re-; C. Real-World Evaluation
- Evidence: Remark 1 原文将“高频可靠获取人手运动”作为高频率闭环与小步长线性化的前提；C 节实机实验自述为定性评估，全文无输入噪声敏感性分析。
- Quote: “Remark 1: With the availability of virtual reality inter- faces, vision-based tracking, and data gloves, human hand motion can now be acquired reliably at high frequency. This enables dexterous-hand teleoperation to be executed within a high-rate control loop, where the variation in joint configurations between consecutive time steps is inherently small.”
- Authors: yinxiao-tian; ziyi-yang; zinan-zhao; et al.

### EA-EGOPREC-2026-0441

- Claim: RealDexUMI 的末端位姿真值来源未被精度标定：一个刚性安装于手模块的 6-DoF 追踪器经固定外参转换到预定义 hand 参考系（100Hz 记录，仅用于构造相对动作标签），但全文未给出追踪器型号、绝对精度或与独立真值的对比。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.06033](https://arxiv.org/abs/2606.06033) RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning
- Locator: 4.1 Policy Interface
- Evidence: 4.1 说明追踪器刚性安装与固定外参转换；附录 B.1 给出 100Hz 记录与仅作标签的用途；通读全文（含附录 A 手套、B 同步、D 训练）未见追踪器型号或精度数据。
- Quote: “The 6-DoF tracker is rigidly mounted to the hand module, and its pose is converted to a predefined hand reference frame through a fixed transform.”
- Authors: chaoyi-xu; yixuan-jiang; jiahui-huan; et al.

### EA-EGOPREC-2026-0095

- Claim: 缺口：本文从未对手部/腕部轨迹重建的空间精度做直接定量评估——全文没有对真值的平移/旋转误差、没有 MPJPE 类指标，轨迹质量的验证设计只包含任务成功率与盲测偏好两项下游代理；因此无法从本文推出手部检测/追踪精度到重定向末端轨迹误差的可接受阈值，其'噪声吸收'证据全部停留在任务层面。
- Stance: `gap` | Confidence: `inference`
- Paper: [2606.10743](https://arxiv.org/abs/2606.10743) Hand-centric Human-to-Robot Trajectory Transfer from Video Demonstrations via Open-World Contact Localization
- Locator: 4.2 Trajectory Reconstruction Quality
- Evidence: 4.2 的评估设计仅列 (i) 任务成功率与 (ii) 盲测偏好研究；通读全文（含附录 A-J）未发现任何腕部/手部轨迹对真值的空间误差测量，唯一的空间度量是接触定位的帧级 MAE 与碰撞增广的间隙参数。
- Quote: “To validate the fidelity of our transferred trajectories, we conducted a series of qualitative and quan- titative experiments, including: (i) an evaluation of retargeting task success rates on our hardware setups and (ii) a blinded pairwise-comparison preference study comparing trajectories generated by HOWTransfer against those collected through teleoperation.”
- Authors: yitian-shi; di-wen; zhengqi-han; et al.

### EA-EGOPREC-2026-0100

- Claim: 缺口：本文把'手部姿态估计噪声'作为核心立论却全程未量化它——未命名具体估计器、未报告腕部平移/旋转的误差幅度或分布、未描述任何滤波/异常剔除管线；'noisy'的全部证据是下游行为对照（6DoF 扭曲 vs 3DoF 稳定）与上界差距，且 6DoF 基线把旋转噪声与接触模式失配捆绑在同一变量中；因此从本文无法推出手部检测/追踪误差的可接受阈值或噪声-误差的传递函数。
- Stance: `gap` | Confidence: `inference`
- Paper: [2606.28133](https://arxiv.org/abs/2606.28133) Translation as a Bridging Action: Transferring Manipulation Skills from Humans to Robots
- Locator: 1 Introduction; 4.1 Motion Bridging Action Representation
- Evidence: 1 Introduction 与 4.1 对噪声仅有定性陈述（inevitably noisy / noisy due to predictor errors）；通读全文（含全部实验节）未发现估计器名称、误差幅值或噪声处理管线；Tab.2 的对照同时移除旋转噪声与接触失配两个机制。
- Quote: “Human actions are typically derived from hand pose estimators [13, 26, 27, 62]. Though human hands can be constrained by parameterization [37, 38, 41, 45, 62] or re-targeting [66], the extracted actions are inevitably noisy.”
- Authors: sijin-chen; kaixuan-jiang; haixin-shi; et al.

### EA-EGOPREC-2026-0066

- Claim: 作者在部署时刻意绕过感知误差：直接向策略喂入动捕物体位姿“以最小化感知误差、防止其成为混杂因素”，并在局限性中承认对动捕的依赖；因此该管线对（如 ego-centric 视频中）噪声化手部/物体位姿估计的容忍度未被表征。
- Stance: `gap` | Confidence: `direct`
- Paper: [2607.11874](https://arxiv.org/abs/2607.11874) A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation
- Locator: 4.1 Experiment Setup; 5 Limitations
- Evidence: 4.1 原文明确以 mocap 排除感知混杂；5 Limitations 承认部署依赖动捕；全文（含附录）无对演示或部署感知噪声的敏感性实验。
- Quote: “To isolate the dynamics gap in sim-to-real transfer, we feed object poses from a motion capture system directly to the policy at deployment time, which minimizes perception errors and prevents them from acting as a confounder.”
- Authors: yunhai-feng; natalie-leung; jiaxuan-wang; et al.

### EA-EGOPREC-2026-0453

- Claim: HiFi-UMI 将保真度（轨迹精度、双臂相对位姿、同步、视场）作为整体设计原则验证，但未做受控退化消融，因此其结果只证明高保真充分，未回答可部署策略对每项保真度因子的具体需求阈值。
- Stance: `gap` | Confidence: `direct`
- Paper: [2607.25895](https://arxiv.org/abs/2607.25895) HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone
- Locator: 7 Discussion
- Evidence: Sec 7 作者自述『Fidelity is validated as a whole, not decomposed』，并提出需要选择性退化各因子的系统消融才能给出可操作的保真度规格。
- Quote: “Fidelity is validated as a whole, not decomposed. We treat fidelity as a design principle realized jointly by trajectory accuracy, inter-gripper relative pose, synchronization, and field of view, and we do not isolate these factors through controlled degradation. Our results thus show that high fidelity suffices, but not how much of each property a deployable policy requires.”
- Authors: simple-ai; unknown-author; yuteng-wei; et al.

### EA-EGOPREC-2026-0515

- Claim: HandEdit 的重定向以源数据集的 MANO 或 3D 手部姿态估计为输入，其 pseudo-GT 轨迹精度继承上游手部姿态估计的残差；管线的阶段 QC 只剔除超限的灾难性失败，未报告保留样本的残余腕部/指尖误差分布，因此该基准不能回答'可接受阈值内的残余手部检测误差如何影响最终轨迹精度'。
- Stance: `gap` | Confidence: `inference`
- Paper: [2608.12122](https://arxiv.org/abs/2608.12122) HandEdit: A Unified Benchmark for Egocentric Human-to-Robot Dexterous Hand Image Editing
- Locator: Abstract / Section 3.1 Data Curation Pipeline
- Evidence: 前提 1：Section 3.1 以 MANO/3D hand pose 为重定向输入，其精度取决于上游数据集标注链。前提 2：附录 B.2 明示 Table S5 只描述被拒帧、不度量保留样本残余误差。推断：保留集残余轨迹误差未知，阈值内的精度-可用性关系不在本文评测空间。削弱条件：若上游数据集（如 HO-Cap 的 MoCap 级标注）姿态误差可忽略，则该缺口对高标注质量子集不成立。
- Quote: “For dexterous hands, we convert the MANO [66] or 3D hand pose into robot joint states”
- Authors: zhenjie-yang; xingyu-jiao; guopeng-zhong; et al.

### EA-EGOPREC-2026-0495

- Claim: ViHaTeleop 作者明确承认：全系统没有对追踪器（Vive Ultimate）或相机（MediaPipe 手部检测）精度的外部 ground-truth 基准测量；腕部 SLAM 追踪的精度声明依赖第三方文献 [28] 的评估而非本文实测。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.16572](https://arxiv.org/abs/2608.16572) ViHaTeleop: A Low-Cost, Lightweight Visual-Haptic Teleoperation System for Dexterous Manipulation Learning
- Locator: F. Discussion
- Evidence: IV.F limitation 段逐字列出无 ground-truth 基准；II.A 对 Vive Ultimate 精度的唯一支撑是引用 Kulozik & Jarrassé 的第三方评估。
- Quote: “Remaining limitations include no external ground-truth benchmark of tracker or camera accu- racy, single-participant LED evaluation, a small parallelism- constraint ablation, and a limited user-study sample (n = 9).”
- Authors: fucai-zhu; yanhou-lai; paul-maestre; et al.

## References

- `2405.01527` [Track2Act: Predicting Point Tracks from Internet Videos enables Generalizable Robot Manipulation](https://arxiv.org/abs/2405.01527) (2024-05-02)
- `2407.03162` [Bunny-VisionPro: Real-Time Bimanual Dexterous Teleoperation for Imitation Learning](https://arxiv.org/abs/2407.03162) (2024-07-03)
- `2409.12259` [WiLoR: End-to-end 3D Hand Localization and Reconstruction in-the-wild](https://arxiv.org/abs/2409.12259) (2024-09-18)
- `2409.19499` [FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset](https://arxiv.org/abs/2409.19499) (2024-09-29)
- `2410.24221` [EgoMimic: Scaling Imitation Learning via Egocentric Video](https://arxiv.org/abs/2410.24221) (2024-10-31)
- `2501.02973` [HaWoR: World-Space Hand Motion Reconstruction from Egocentric Videos](https://arxiv.org/abs/2501.02973) (2025-01-06)
- `2503.00779` [Phantom: Training Robots Without Robots Using Only Human Videos](https://arxiv.org/abs/2503.00779) (2025-03-02)
- `2503.07017` [How to Train Your Robots? The Impact of Demonstration Modality on Imitation Learning](https://arxiv.org/abs/2503.07017) (2025-03-10)
- `2504.06084` [MAPLE: Encoding Dexterous Robotic Manipulation Priors Learned From Egocentric Videos](https://arxiv.org/abs/2504.06084) (2025-04-08)
- `2505.11709` [EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video](https://arxiv.org/abs/2505.11709) (2025-05-16)
- `2505.20290` [EgoZero: Robot Learning from Smart Glasses](https://arxiv.org/abs/2505.20290) (2025-05-27)
- `2505.21864` [DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation](https://arxiv.org/abs/2505.21864) (2025-05-27)
- `2506.09384` [Analyzing Key Objectives in Human-to-Robot Retargeting for Dexterous Manipulation](https://arxiv.org/abs/2506.09384) (2025-06-11)
- `2506.17198` [Dex1B: Learning with 1B Demonstrations for Dexterous Manipulation](https://arxiv.org/abs/2506.17198) (2025-06-20)
- `2507.12440` [EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos](https://arxiv.org/abs/2507.12440) (2025-07-16)
- `2508.09976` [Masquerade: Learning from In-the-wild Human Videos using Data-Editing](https://arxiv.org/abs/2508.09976) (2025-08-13)
- `2509.04443` [EMMA: Scaling Mobile Manipulation via Egocentric Human Data](https://arxiv.org/abs/2509.04443) (2025-09-04)
- `2509.05513` [OpenEgo: A Large-Scale Multimodal Egocentric Dataset for Dexterous Manipulation](https://arxiv.org/abs/2509.05513) (2025-09-05)
- `2509.10952` [ImMimic: Cross-Domain Imitation from Human Videos via Mapping and Interpolation](https://arxiv.org/abs/2509.10952) (2025-09-13)
- `2509.15212` [RynnVLA-001: Using Human Demonstrations to Improve Robot Manipulation](https://arxiv.org/abs/2509.15212) (2025-09-18)
- `2509.19626` [EgoBridge: Domain Adaptation for Generalizable Imitation from Egocentric Human Data](https://arxiv.org/abs/2509.19626) (2025-09-23)
- `2509.21986` [Developing Vision-Language-Action Model from Egocentric Videos](https://arxiv.org/abs/2509.21986) (2025-09-26)
- `2510.01607` [ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations](https://arxiv.org/abs/2510.01607) (2025-10-02)
- `2511.00153` [EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations](https://arxiv.org/abs/2511.00153) (2025-10-31)
- `2511.04671` [X-Diffusion: Training Diffusion Policies on Cross-Embodiment Human Demonstrations](https://arxiv.org/abs/2511.04671) (2025-11-06)
- `2511.09484` [SPIDER: Scalable Physics-Informed Dexterous Retargeting](https://arxiv.org/abs/2511.09484) (2025-11-12)
- `2511.15704` [In-N-On: Scaling Egocentric Manipulation with in-the-wild and on-task Data](https://arxiv.org/abs/2511.15704) (2025-11-19)
- `2511.17366` [METIS: Multi-Source Egocentric Training for Integrated Dexterous Vision-Language-Action Model](https://arxiv.org/abs/2511.17366) (2025-11-21)
- `2512.13644` [World Models for Learning Dexterous Hand-Object Interactions from Human Videos](https://arxiv.org/abs/2512.13644) (2025-12-15)
- `2512.16793` [PhysBrain: Human Egocentric Data as a Bridge from Vision Language Models to Physical Intelligence](https://arxiv.org/abs/2512.16793) (2025-12-19)
- `2512.24310` [World In Your Hands: A Large-Scale and Open-source Ecosystem for Learning Human-centric Manipulation in the Wild](https://arxiv.org/abs/2512.24310) (2025-12-30)
- `2602.09013` [Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction](https://arxiv.org/abs/2602.09013) (2026-02-11)
- `2602.10106` [EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration](https://arxiv.org/abs/2602.10106) (2026-02-10)
- `2602.11464` [EasyMimic: A Low-Cost Framework for Robot Imitation Learning from Human Videos](https://arxiv.org/abs/2602.11464) (2026-02-12)
- `2602.16710` [EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data](https://arxiv.org/abs/2602.16710) (2026-02-18)
- `2602.23893` [AoE: Always-on Egocentric Human Video Collection for Embodied AI](https://arxiv.org/abs/2602.23893) (2026-02-27)
- `2603.03243` [HoMMI: Learning Whole-Body Mobile Manipulation from Human Demonstrations](https://arxiv.org/abs/2603.03243) (2026-03-05)
- `2603.05804` [CDF-Glove: A Cable-Driven Force Feedback Glove for Dexterous Teleoperation](https://arxiv.org/abs/2603.05804) (2026-03-06)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.11383` [Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics](https://arxiv.org/abs/2603.11383) (2026-03-11)
- `2603.17065` [TeleDex: Accessible Dexterous Teleoperation](https://arxiv.org/abs/2603.17065) (2026-03-20)
- `2603.17323` [DexEXO: A Wearability-First Dexterous Exoskeleton for Operator-Agnostic Demonstration and Learning](https://arxiv.org/abs/2603.17323) (2026-03-18)
- `2603.17851` [DexViTac: Collecting Human Visuo-Tactile-Kinematic Demonstrations for Contact-Rich Dexterous Manipulation](https://arxiv.org/abs/2603.17851) (2026-03-18)
- `2603.22264` [UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos](https://arxiv.org/abs/2603.22264) (2026-03-23)
- `2603.27012` [UMI-Underwater: Learning Underwater Manipulation without Underwater Teleoperation](https://arxiv.org/abs/2603.27012) (2026-03-27)
- `2603.29213` [Kilohertz-Safe: A Scalable Framework for Constrained Dexterous Retargeting](https://arxiv.org/abs/2603.29213) (2026-03-31)
- `2604.10809` [WARPED: Wrist-Aligned Rendering for Robot Policy Learning from Egocentric Human Demonstrations](https://arxiv.org/abs/2604.10809) (2026-04-12)
- `2604.27621` [Robot Learning from Human Videos: A Survey](https://arxiv.org/abs/2604.27621) (2026-04-30)
- `2605.05712` [EgoEMG: A Multimodal Egocentric Dataset with Bilateral EMG and Vision for Hand Pose Estimation](https://arxiv.org/abs/2605.05712) (2026-05-07)
- `2605.05945` [MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware](https://arxiv.org/abs/2605.05945) (2026-05-07)
- `2605.12182` [DexTwist: Dexterous Hand Retargeting for Twist Motion via Mixed Reality-based Teleoperation](https://arxiv.org/abs/2605.12182) (2026-05-12)
- `2605.12297` [EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras](https://arxiv.org/abs/2605.12297) (2026-05-12)
- `2605.12498` [EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera](https://arxiv.org/abs/2605.12498) (2026-05-13)
- `2605.23762` [Direct Dynamic Retargeting for Humanoid Imitation Learning from Videos](https://arxiv.org/abs/2605.23762) (2026-05-22)
- `2606.03268` [EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations](https://arxiv.org/abs/2606.03268) (2026-06-02)
- `2606.06033` [RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning](https://arxiv.org/abs/2606.06033) (2026-06-04)
- `2606.06627` [What Matters When Cotraining Robot Manipulation Policies on Everyday Human Videos?](https://arxiv.org/abs/2606.06627) (2026-06-04)
- `2606.08057` [EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets](https://arxiv.org/abs/2606.08057) (2026-06-06)
- `2606.08828` [Video2Sim2Real: Full-Stack Autonomous Dexterous Skill Acquisition from a Single Human Video](https://arxiv.org/abs/2606.08828) (2026-06-07)
- `2606.10614` [Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations](https://arxiv.org/abs/2606.10614) (2026-06-09)
- `2606.10743` [Hand-centric Human-to-Robot Trajectory Transfer from Video Demonstrations via Open-World Contact Localization](https://arxiv.org/abs/2606.10743) (2026-06-09)
- `2606.11628` [LUCID: Learning Embodiment-Agnostic Intent Models from Unstructured Human Videos for Scalable Dexterous Robot Skill Acquisition](https://arxiv.org/abs/2606.11628) (2026-06-10)
- `2606.12604` [EgoEngine: From Egocentric Human Videos to High-Fidelity Dexterous Robot Demonstrations](https://arxiv.org/abs/2606.12604) (2026-06-10)
- `2606.15434` [A Bilateral Teleoperation Framework for Dexterous Manipulation](https://arxiv.org/abs/2606.15434) (2026-06-13)
- `2606.16272` [TopoRetarget: Interaction-Preserving Retargeting for Dexterous Manipulation](https://arxiv.org/abs/2606.16272) (2026-06-19)
- `2606.16436` [V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos](https://arxiv.org/abs/2606.16436) (2026-06-15)
- `2606.19333` [Do as I Do: Dexterous Manipulation Data from Everyday Human Videos](https://arxiv.org/abs/2606.19333) (2026-06-17)
- `2606.27239` [HumanoidUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation](https://arxiv.org/abs/2606.27239) (2026-06-25)
- `2606.28133` [Translation as a Bridging Action: Transferring Manipulation Skills from Humans to Robots](https://arxiv.org/abs/2606.28133) (2026-06-26)
- `2606.29940` [WARP: Whole-Body Retargeting for Learning from Offline Human Demonstrations](https://arxiv.org/abs/2606.29940) (2026-08-19)
- `2607.08341` [AnyDexRT: Calibration-Free Dexterous Hand Retargeting with Few-Shot Human Guidance](https://arxiv.org/abs/2607.08341) (2026-07-09)
- `2607.09519` [DemoBridge: A Simulation-in-the-Loop Toolkit for Single-View Human Demonstration Retargeting](https://arxiv.org/abs/2607.09519) (2026-07-10)
- `2607.11481` [Towards Human-level Dexterous Teleoperation](https://arxiv.org/abs/2607.11481) (2026-07-13)
- `2607.11874` [A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation](https://arxiv.org/abs/2607.11874) (2026-07-13)
- `2607.14183` [Open-AoE: An Open Egocentric Manipulation Dataset and Toolchain for Embodied Learning](https://arxiv.org/abs/2607.14183) (2026-07-15)
- `2607.15890` [Exo2EgoPose: Leveraging Exocentric Demonstrations for Vision-Language guided Egocentric 3D Hand Pose Forecasting](https://arxiv.org/abs/2607.15890) (2026-07-17)
- `2607.19745` [EgoRecovery: Acquiring Failure Recovery Ability Through Human Recovery Demonstration](https://arxiv.org/abs/2607.19745) (2026-07-22)
- `2607.25895` [HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone](https://arxiv.org/abs/2607.25895) (2026-07-28)
- `2607.27784` [DexDirect: Direct Kinesthetic Arm Guidance for Efficient Dexterous Demonstration Collection](https://arxiv.org/abs/2607.27784) (2026-07-30)
- `2608.04196` [SiMDex: Mining Similar Egocentric Videos for Cross-Embodiment Dexterous Manipulation](https://arxiv.org/abs/2608.04196) (2026-08-04)
- `2608.07045` [C2Dex: Contact-Consistent Reconstruction and Retargeting for Dexterous Manipulation from Monocular Video](https://arxiv.org/abs/2608.07045) (2026-08-10)
- `2608.12122` [HandEdit: A Unified Benchmark for Egocentric Human-to-Robot Dexterous Hand Image Editing](https://arxiv.org/abs/2608.12122) (2026-08-12)
- `2608.14028` [AdvDex: Learning Dexterous Manipulation from Human Demonstrations via Joint-Aligned Actions and Adversarial Learning](https://arxiv.org/abs/2608.14028) (2026-08-14)
- `2608.15560` [ReForce: Learning Force-aware Retargeting for Dexterous Manipulation](https://arxiv.org/abs/2608.15560) (2026-08-16)
- `2608.16572` [ViHaTeleop: A Low-Cost, Lightweight Visual-Haptic Teleoperation System for Dexterous Manipulation Learning](https://arxiv.org/abs/2608.16572) (2026-08-17)
- `2609.07747` [Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction](https://arxiv.org/abs/2609.07747) (2026-09-07)
