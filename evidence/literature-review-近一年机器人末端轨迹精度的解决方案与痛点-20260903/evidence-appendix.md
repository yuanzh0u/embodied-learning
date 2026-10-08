# Evidence Appendix: 近一年机器人末端轨迹精度的解决方案与痛点

- Time range: 2025-09-01..2026-08-31
- Events: 169
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-TRAJACC-2026-0007

- Claim: 在含未知关节摩擦的Gazebo仿真（无外部扰动）中，自适应NT-STSM控制器在7-DOF Franka上取得全部控制器中最高的旋转跟踪精度（RMSE_ξ=2.25e-2 rad）、最平滑的控制输入（TV_τ=8.45e3 Nm最低），平移RMSE_p=1.76e-3 m与PD-high（1.54e-3 m）相当，同时平均控制力矩0.490 Nm低于PD-med（0.506）与PD-high（0.566 Nm）。
- Stance: `support` | Confidence: `direct`
- Paper: [2504.13056](https://arxiv.org/abs/2504.13056) Adaptive Task Space Nonsingular Terminal Super-Twisting Sliding Mode Control of a 7-DOF Robotic Manipulator
- Locator: B. Simulation Results, Table III
- Evidence: III-B原文：所提NT-STSM平移跟踪与PD-high相当、旋转精度全控制器最高、控制力矩水平低，且TV_τ全控制器最低（最平滑）；表III给出具体数值（RMSE_p 1.76e-3 m、RMSE_ξ 2.25e-2 rad、τ_avg 4.90e-1 Nm、TV_τ 8.45e3 Nm）。
- Quote: “As shown in Table III, the proposed NT-STSM controller achieved comparable translational tracking to the PD-high controller and the highest rotational tracking accuracy of all the controllers while maintaining a low level of control effort. The NT-STSM controller also provides the lowest TV τ among all controllers, indicating it has the smoothest control inputs.”
- Authors: lucas-wan; sean-smith; yajun-pan; et al.

### EA-TRAJACC-2026-0008

- Claim: 将[21]的关节空间NT-STSM（受κ2=1/4Γκ1严格增益比约束）原样用于任务空间后，RMSE_p较本文放松增益约束的方法增加71.3%、RMSE_ξ增加69.4%（6.13e-3 m、7.36e-2 rad vs 1.76e-3 m、2.25e-2 rad），表明稳定性证明强加的增益关系是该方案族此前的直接性能瓶颈。
- Stance: `support` | Confidence: `direct`
- Paper: [2504.13056](https://arxiv.org/abs/2504.13056) Adaptive Task Space Nonsingular Terminal Super-Twisting Sliding Mode Control of a 7-DOF Robotic Manipulator
- Locator: B. Simulation Results
- Evidence: III-B原文：把[21]的NT-STSM（原为关节空间设计、带κ1-κ2约束关系）用于任务空间导致RMSE_p增71.3%、RMSE_ξ增69.4%；作者结论是该稳定证明的严格增益关系限制控制器性能、不适合本应用；表III给出两者绝对值。
- Quote: “Applying the NT-STSM controller from [21], originally de- signed for the joint space, to the task space with its constrained relationship between κ 1 and κ 2 , resulted in a 71.3% increase in RMSE p , and a 69.4% increase in RMSE ξ , compared to our approach. This result indicates that the strict gain relationship required by the stability proof in [21] limits the controller performance and is not suitable for this application.”
- Authors: lucas-wan; sean-smith; yajun-pan; et al.

### EA-TRAJACC-2026-0009

- Claim: 同等控制力矩下，所提NT-STSM较PD-med使RMSE_p降低29.0%、RMSE_ξ降低27.6%；较PD-high跟踪性能相当但平均控制力矩低13.4%——即以更低能耗取得与强增益PD同级的任务空间跟踪精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2504.13056](https://arxiv.org/abs/2504.13056) Adaptive Task Space Nonsingular Terminal Super-Twisting Sliding Mode Control of a 7-DOF Robotic Manipulator
- Locator: B. Simulation Results, Table III
- Evidence: III-B原文给出与PD两档的百分比比较：对PD-med为29.0%/27.6%的RMSE降幅且控制力矩相近，对PD-high为跟踪相当但控制力矩低13.4%；表III显示PD-high以最高平均控制力矩（0.566 Nm）换取最好PD精度（1.54e-3 m），存在能耗与执行器上限风险。
- Quote: “Compared to the PD-med controller, the proposed NT-STSM controller reduced RMSE p by 29.0% and RMSE ξ by 27.6%, with similar control effort. Compared to the PD-high controller, the proposed NT-STSM controller achieved similar tracking performance with 13.4% lower control effort.”
- Authors: lucas-wan; sean-smith; yajun-pan; et al.

### EA-TRAJACC-2026-0034

- Claim: 在最佳正面HMD条件下静态跟踪精度高：F2条件、50 mm/s接近速度下8个静态位姿的平均误差仅2.1 mm（每位姿30次重复），且正面条件下更高接近速度普遍带来轻微改善；作者在讨论与结论中另总结最佳条件动态平均精度<2 mm、角度误差始终低于10°操作阈值——构成该商用方案族约2 mm级的量化精度锚点。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05391](https://arxiv.org/abs/2509.05391) Evaluating Magic Leap 2 Controller Tracking for Sensor Tool Guidance in AR-Based Industrial Inspections
- Locator: IV-A. Static Tracking Accuracy, Table III
- Evidence: IV-A原文：静态评估显示对视角与接近速度的清晰依赖，正面HMD位置下精度持续高——F2@50 mm/s全位姿平均误差仅2.1 mm、更高接近速度在最佳条件下普遍略有改善；表III F2(50)平均行Mean/Max/Repeat=2.1/4.3/0.8 mm核对一致；V-B首句与VI结论另报最佳条件动态平均精度<2 mm，IV-B3报角度误差始终显著低于10°阈值。
- Quote: “The static tracking evaluation revealed a clear dependency on the viewing angle and approach speed. Under optimal, frontal HMD positions, the system consistently achieved high accuracy. For instance, in the F2 condition at an approach speed of 50 mm/s, the mean error across all poses was only 2.1 mm. Higher approach speeds were generally associated with slight improvements in these optimal conditions.”
- Authors: christian-masuhr; julian-koch; thorsten-schppstuhl

### EA-TRAJACC-2026-0001

- Claim: 在双手相机人形机器人平台上，所提DET-MPH视觉伺服方法对M4-M8螺丝头槽对准任务达到93%-100%成功率与0.8-1.3mm平均收敛误差（每种规格100次物理试验）。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.04862](https://arxiv.org/abs/2503.04862) High-Precision Transformer-Based Visual Servoing for Humanoid Robots in Aligning Tiny Objects
- Locator: IV. CONCLUSIONS / B. Results and Discussion, Table II
- Evidence: 结论节原文总结：方法在M4-M8螺丝对准任务上展示平均0.8-1.3mm位置精度与93%-100%成功率，显著优于单感知头或传统CNN框架；表II给出分规格数值（M8 100%/1.3±0.6mm、M6 100%/1.0±0.4mm、M4 93%/0.8±0.5mm）。
- Quote: “The proposed method demonstrates an average positional precision of 0.8- 1.3 mm and a success rate of 93%-100% for the alignment tasks with M4-M8 screws, showing a significantly better performance than frameworks with either single perception head or traditional convolutional neural network.”
- Authors: jialong-xue; wei-gao; yu-wang; et al.

### EA-TRAJACC-2026-0002

- Claim: 同一硬件与任务设置下，DET-MPH较单感知头基线DET-SPH平均成功率高16%、精度好25%；较ResNet18+MLP基线平均成功率高47%、精度好54%。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.04862](https://arxiv.org/abs/2503.04862) High-Precision Transformer-Based Visual Servoing for Humanoid Robots in Aligning Tiny Objects
- Locator: B. Results and Discussion
- Evidence: III-B节原文给出与两个基线的相对比较：对DET-SPH为16%平均成功率提升与25%精度提升，对ResNet18+MLP为47%与54%；作者据此认为DET架构与MPH机制共同增强了视觉特征提取与控制精度。
- Quote: “They reveal that the proposed method achieves significantly better performance, with 16% higher average success rate and 25% better precision compared to the DET-SPH baseline, and 47% higher average success rate and 54% better precision compared to the ResNet18+MLP baseline. The results sub- stantiate the effectiveness of both the DET architecture and the MPH mechanism in enhancing visual feature extraction and control precision for tiny object alignment tasks.”
- Authors: jialong-xue; wei-gao; yu-wang; et al.

### EA-TRAJACC-2026-0003

- Claim: 该文识别的核心训练痛点是多距离训练中远距离样本主导损失从而压制近距离精度；其对策（MPH）是距离相关的输出缩放：每个感知头以距离区间相关的增益放大输出，使网络能提取对精确控制关键的精细位置差异特征。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.04862](https://arxiv.org/abs/2503.04862) High-Precision Transformer-Based Visual Servoing for Humanoid Robots in Aligning Tiny Objects
- Locator: B. Distance Estimation Transformer
- Evidence: II-B节原文：远距离RGB深度线索有限导致估计误差与损失量大，近距离损失小，形成压制效应降低近距精度——这对收敛后需要高精度的机器人应用是关键问题；为此实现距离相关的输出缩放以对抗远样本主导，使网络能提取对精确控制关键的精细位置差异特征。
- Quote: “like the tiny object alignment task discussed in this paper. To address this issue, distance-dependent output scaling is implemented to counteract the dominance of farther samples. This approach enables the network to extract refined features of positional discrepancy that are critical for precise control.”
- Authors: jialong-xue; wei-gao; yu-wang; et al.

### EA-TRAJACC-2026-0004

- Claim: 在小于0.016m的近距离训练样本上，DET-MPH仅需8个epoch即达到低于0.001m的估计误差，而DET-SPH需要近20个epoch才能达到同等水平，说明远距离样本的大损失贡献压制了SPH处理近距离样本的能力。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.04862](https://arxiv.org/abs/2503.04862) High-Precision Transformer-Based Visual Servoing for Humanoid Robots in Aligning Tiny Objects
- Locator: B. Results and Discussion
- Evidence: III-B节训练动态分析原文：DET-MPH对<0.016m样本的估计误差收敛显著快于DET-SPH，8 epoch内低于0.001m而SPH需近20 epoch；作者解释为SPH中远距离样本的更大损失贡献压制了近距样本处理能力，MPH实现全操作范围更均衡的训练。
- Quote: “the estimation error of DET-MPH converges significantly faster than that of DET-SPH for samples with distances less than 0.016m. Specifically, DET-MPH achieves an estimation error of below 0.001m within only 8 epochs during training for the close-range samples, whereas DET-SPH requires nearly 20 epochs to reach the same level of performance.”
- Authors: jialong-xue; wei-gao; yu-wang; et al.

### EA-TRAJACC-2026-0038

- Claim: 在高速动态跟踪消融中，把本框架的单步流策略换成 Diffusion Policy 后，推理时间超 128 ms、控制频率降至约 8 Hz，最大可跟踪速度被压制到 31 mm/s，重定位误差增大到 9.84 mm——即推理延迟通过控制频率直接封顶末端可跟踪速度与精度。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00983](https://arxiv.org/abs/2511.00983) Breaking the Latency Barrier: Synergistic Perception and Control for High-Frequency 3D Ultrasound Servoing
- Locator: IV. EXPERIMENTS / D. Ablation Studies and Comparative Analysis, Table IV
- Evidence: IV-D 消融在同一感知前端与同一动态跟踪任务上仅替换策略：Diffusion 变体 128.2 ms/8 Hz/30.98 mm/s/9.84 mm，本框架 16.2 ms/62 Hz/102.47 mm/s/1.52 mm（Table IV），正文明确将 31 mm/s 上限与 9.84 mm 误差归因于该延迟。
- Quote: “First, the Diffusion Policy variant revealed a severe latency bottleneck. Its inference time of over 128 ms corresponds to a sluggish control frequency of only 8 Hz, fundamentally limiting its dynamic response. This latency not only capped its tracking speed at 31 mm/s but also resulting in a large repositioning error of 9.84 mm.”
- Authors: yizhao-qian; yujie-zhu; jiayuan-luo; et al.

### EA-TRAJACC-2026-0039

- Claim: 本框架以 16.2 ms 端到端延迟实现 62 Hz 闭环控制，据此支持 >100 mm/s 的动态跟踪与 <1.6 mm 的终端收敛精度；作者论证该高性能是感知与控制紧耦合协同的涌现属性，而非任何单组件的贡献。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00983](https://arxiv.org/abs/2511.00983) Breaking the Latency Barrier: Synergistic Perception and Control for High-Frequency 3D Ultrasound Servoing
- Locator: IV. EXPERIMENTS / D. Ablation Studies and Comparative Analysis, Table II/IV
- Evidence: IV-D 结尾的对比总结与 Table II：高速动态跟踪中最大跟踪速度 102.47 mm/s、平均误差 6.124±0.386 mm、终端误差 1.629 mm、终端 NCC 0.9548；正文将高带宽明确表述为动态跟踪与精确收敛的前提，并称协同集成为涌现属性。
- Quote: “In stark contrast, our framework achieves a low 16.2 ms latency, enabling a 62 Hz control loop. This high bandwidth is the prerequisite for both its superior dynamic tracking (>100 mm/s) and its precise final convergence (<1.6 mm er- ror). These results demonstrate that high-performance robotic US is an emergent property that arises only from the tight, synergistic integration of perception and control.”
- Authors: yizhao-qian; yujie-zhu; jiayuan-luo; et al.

### EA-TRAJACC-2026-0042

- Claim: 借助解耦感知架构的归纳偏置，Sim-to-Real 只需 50 条真机专家轨迹微调（几何流大部分冻结、集中于域敏感的语义流微调）即可弥合现实差距，避免灾难性遗忘——该高频方案的真机数据成本条件显著低于从零采集。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00983](https://arxiv.org/abs/2511.00983) Breaking the Latency Barrier: Synergistic Perception and Control for High-Frequency 3D Ultrasound Servoing
- Locator: III. METHODOLOGY / E. Sample-Efficient Sim-to-Real Transfer
- Evidence: III-E 第三阶段明确：预训练模型仅用 50 条专家轨迹微调，冻结大部分域不变的几何流权重、集中微调域敏感的语义流，以针对性适配实现高效域迁移并防止灾难性遗忘；引言将其列为贡献（50 条轨迹快速收敛）。
- Quote: “Finally, to bridge the ”reality gap,” the pre-trained model is fine-tuned on a minimal dataset of just 50 expert trajecto- ries. This stage leverages the inductive biases of our decou- pled architecture for maximum sample efficiency. We freeze most weights of the largely domain-invariant geometric stream and concentrate fine-tuning on the domain-sensitive semantic stream.”
- Authors: yizhao-qian; yujie-zhu; jiayuan-luo; et al.

### EA-TRAJACC-2026-0043

- Claim: 在直线洛伦兹力执行器的多任务实验（参考命令每 10 次迭代顺序由 0.6 Hz 切至 0.7 Hz、再 0.8 Hz，共 30 次迭代）中，NN 增强 ILC 相对常规 ILC 在参考变化时的初始 MSE 显著更低且收敛更迅速（原文未报告具体数值）。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.11850](https://arxiv.org/abs/2511.11850) Neural Network-Augmented Iterative Learning Control for Friction Compensation of Motion Control Systems with Varying Disturbances
- Locator: V. EXPERIMENTAL TESTS AND RESULTS
- Evidence: V 节实验结果原文陈述初始 MSE 在参考变化时显著更低、收敛更快，并以 Fig. 10 的常规 ILC 与 NN 增强 ILC 收敛对比为依据。
- Quote: “Results show that the initial MSE upon reference changes is significantly lower with the proposed method, and convergence is achieved more rapidly. The reduced uncertainty levels contribute to improved robustness, demonstrating the effectiveness of neural network-augmented ILC in compensating nonlinear effects and enhancing performance in multi-task applications.”
- Authors: ali-mashhadireza; ali-sadighi

### EA-TRAJACC-2026-0045

- Claim: 方法核心机制：以参考轨迹的位置与速度为输入，训练神经网络预测收敛 ILC 努力中的非线性分量 u_n，使系统在多任务场景预先补偿非线性，从而减少 ILC 收敛所需迭代数。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.11850](https://arxiv.org/abs/2511.11850) Neural Network-Augmented Iterative Learning Control for Friction Compensation of Motion Control Systems with Varying Disturbances
- Locator: B. Incorporation of Neural Networks in ILC
- Evidence: II.B 节给出机制推导：收敛 ILC 努力分解为线性前馈分量与非线性分量，后者对每条参考唯一，训练 NN 按参考位置/速度预测之即可预先补偿并减少收敛迭代。
- Quote: “By training a neural network to predict u n based on position and velocity of the reference trajectory, the system can preemptively compensate nonlinearities, reducing the number of iterations needed for ILC convergence in multi-task scenarios.”
- Authors: ali-mashhadireza; ali-sadighi

### EA-TRAJACC-2026-0014

- Claim: 作者主张：对任意统计查询（SQ）型测试例程——无论基于Monte Carlo采样、重要性采样还是自适应重要性采样——施加轻量、参数化、自适应的修改（α量化+方差敏感终止），即可使其可证明地可重复，并同时给出精度与效率的保证界。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.08216](https://arxiv.org/abs/2505.08216) Rethink Repeatable Measures of Robot Performance With Statistical Query
- Locator: preamble / III. MAIN METHOD
- Evidence: 摘要明确陈述所提修改适用于任何SQ例程（三种采样机制通吃）并使可重复性可证明、精度与效率均有保证界；正文Thm.1-3分别落实精度保持、β可重复与方差敏感终止，且理论对固定与自适应q均成立。
- Quote: “We propose a lightweight, parameterized, and adaptive modification applicable to any SQ routine—whether based on Monte Carlo sampling, importance sampling, or adaptive importance sampling—that makes it provably repeatable, with guaranteed bounds on both accuracy and efficiency.”
- Authors: bowen-weng; linda-capito; guillermo-a-castillo; et al.

### EA-TRAJACC-2026-0015

- Claim: 在Unitree G1人形机器人定位重复性测试上，α量化算法经1次initiator基准与200次独立replicator执行取得98%可重复率（仅4次例外）；理论保证期望位移落在距（未知）真值0.195mm内（≥95%置信）且任意成对试验返回相同结果（≥90%概率）。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.08216](https://arxiv.org/abs/2505.08216) Rethink Repeatable Measures of Robot Performance With Statistical Query
- Locator: IV.A. Manipulation positioning tests / Fig. 2
- Evidence: IV.A节报告200次独立重复执行中98%返回同一量化结果（4次例外，符合β=0.1的≥90%保证）；同节明确设定γ=0.1、c=0.05、β=0.1、m=6mm后'expected displacement lies within 0.195 mm...with at least 95% probability'且'any pair of repeated trials yields the same outcome with at least 90% probability'。
- Quote: “The distribution of expected displacement values across these 200 replicated trials is shown in red in Fig. 2(a). The algorithm achieved a 98% repeatability rate, with only 4 exceptions out of 200 trials.”
- Authors: bowen-weng; linda-capito; guillermo-a-castillo; et al.

### EA-TRAJACC-2026-0017

- Claim: 在G1运动指令跟踪评测中，四种采样变体（Monte Carlo/重要性采样/两种batch大小的自适应重要性采样）共40次仿真试验全部收敛到同一最终跟踪性能估计≈0.47；最省样本的AIS变体（batch=30）仅需442次测试，而Monte Carlo最多需650次。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.08216](https://arxiv.org/abs/2505.08216) Rethink Repeatable Measures of Robot Performance With Statistical Query
- Locator: IV.C. Humanoid robot locomotive tracking performance tests / Fig. 6a
- Evidence: IV.C节报告四种α量化算法变体各执行10次（共40次），尽管采样行为不同全部收敛到同一估计≈0.47；样本需求差异显著：Monte Carlo最多650测试，AIS(d=30)仅442测试即达同一估计——可重复性与采样机制解耦，效率来自方差缩减。
- Quote: “Despite differences in sampling behavior, all 40 trials converged to the same final tracking performance estimate of approximately 0.47. However, as shown in Fig. 6a, the number of required samples varied significantly: Monte Carlo sampling used up to 650 tests, while the most efficient AIS variant (d = 30) achieved the same estimate with only 442 tests.”
- Authors: bowen-weng; linda-capito; guillermo-a-castillo; et al.

### EA-TRAJACC-2026-0018

- Claim: 同一RL运动策略的指令跟踪性能估计在仿真（40次试验均≈0.47）与真机（相隔7天的两次试验均为0.39）间存在明显差异（有界跟踪损失，真机更低）；所提框架以形式化保证（误差界0.078、95%置信、90%可重复）检测并量化该sim-to-real差异。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.08216](https://arxiv.org/abs/2505.08216) Rethink Repeatable Measures of Robot Performance With Statistical Query
- Locator: IV.C. Humanoid robot locomotive tracking performance tests
- Evidence: IV.C节报告真机两次试验（IS跨3天240测试、AIS单天222测试，相隔7天、动捕重新标定）均返回相同估计0.39，与仿真估计≈0.47形成清晰差异；正文明确两估计保证落在真值0.078内@95%置信、90%可重复，并称框架提供'principled and parameterized way to detect and quantify such discrepancies'。
- Quote: “According to Theorem 3 and the specified parameters, both the simulation and real-world estimates are guaranteed to lie within 0.078 of the ground-truth value with 95% confidence and are repeatable with 90% probability. Notably, the same locomotion algorithm exhibits a clear discrepancy in tracking performance between the simulator and the real world. The proposed testing framework offers a principled and parameter- ized way to detect and quantify such discrepancies, complete with formal guarant”
- Authors: bowen-weng; linda-capito; guillermo-a-castillo; et al.

### EA-TRAJACC-2026-0025

- Claim: 在四个配合量子任务（过盈-0.04mm至间隙+0.04mm、各50次真机试验）上，多教师蒸馏得到的单一鲁棒策略FVFC-MTRL-PD取得最高平均奖励22.1与最高平均成功率98.5%，优于恒参数力控FBCC（42.0%）、单任务RL基线MDRL（54.0%）与恒参数FVFC（61.0%），且与非鲁棒多任务策略FVFC-MTRL（97.0%）相当而无需任务编码。
- Stance: `support` | Confidence: `direct`
- Paper: [2508.12296](https://arxiv.org/abs/2508.12296) A Robust and Compliant Robotic Assembly Control Strategy for Batch Precision Assembly Task
- Locator: 4.3. Compliance and robustness verification / Table 3
- Evidence: 原文4.3节明确陈述FVFC-MTRL-PD在保持FVFC-MTRL高性能的同时获得跨子任务鲁棒性，取得最高平均奖励22.1与成功率98.5%；Table 3给出各基线平均成功率42.0%/54.0%/61.0%/97.0%。
- Quote: “As shown in Table 3, FVFC- MTRL demonstrates strong performance in each specific subtask, and FVFC-MTRL-PD further maintains the high performance of FVFC-MTRL while additionally achieving robustness across different subtasks. It outperforms all other methods, achieving the highest average reward of 22.1 and success rate of 98.5%.”
- Authors: bin-wang; jiwen-zhang; song-wang; et al.

### EA-TRAJACC-2026-0026

- Claim: 多任务RL训练框架（MTRL）使四个装配子任务的平均奖励在约50k步稳定收敛，样本效率比逐个独立训练（FVFC-STRL）提升50%以上。
- Stance: `support` | Confidence: `direct`
- Paper: [2508.12296](https://arxiv.org/abs/2508.12296) A Robust and Compliant Robotic Assembly Control Strategy for Batch Precision Assembly Task
- Locator: 4.2. Training process / Fig. 7
- Evidence: 原文4.2节陈述FVFC-MTRL平均奖励稳定增长并在约50k步收敛，而FVFC-STRL奖励波动且增长缓慢，并明确'样本效率提升超过50%'的结论。
- Quote: “The average reward across four subtasks in FVFC-MTRL increases steadily and converges at approximately 50k steps. However, the reward of FVFC-STRL fluctuates and increases slowly. It is verified that the proposed MTRL training framework effectively leverages the similarities among subtasks to enhance sample efficiency by more than 50%.”
- Authors: bin-wang; jiwen-zhang; song-wang; et al.

### EA-TRAJACC-2026-0027

- Claim: 批量验证的8组元件中，无倒角孔+制造变形销的两个困难组（G7/G8）上，按最相似子任务部署的MDRL成功率为0%，而FVFC-MTRL-PD仍达约90%（Table 6中G7为92%、G8为88%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2508.12296](https://arxiv.org/abs/2508.12296) A Robust and Compliant Robotic Assembly Control Strategy for Batch Precision Assembly Task
- Locator: 4.4. Batch precision assembly verification / Table 6
- Evidence: 原文4.4节明确陈述G7/G8为故意设计的更困难场景（孔无倒角、销有制造变形），MDRL完全失败（0%）而所提方法仍约90%；Table 6给出92%/88%的具体值。
- Quote: “Furthermore, Groups G7 and G8 represent two intentionally designed, more challenging assembly scenarios, featuring hole with non-chamfered edges and pegs with manufacturing-induced deformations. For these groups, the MDRL approach failed completely (0% success rate), whereas the proposed method still achieved success rates of approximately 90%.”
- Authors: bin-wang; jiwen-zhang; song-wang; et al.

### EA-TRAJACC-2026-0028

- Claim: 在四子任务各50次成功装配的力柔顺评测中，FVFC-MTRL-PD的最大接触力/力矩与控制步数在所有评估策略中最优：子任务T4最大轴向力Fz为0.202N，而FBCC为1.818N、MDRL为1.394N、恒参数FVFC为0.468N。
- Stance: `support` | Confidence: `direct`
- Paper: [2508.12296](https://arxiv.org/abs/2508.12296) A Robust and Compliant Robotic Assembly Control Strategy for Batch Precision Assembly Task
- Locator: 4.3. Compliance and robustness verification / Table 5
- Evidence: 原文4.3节明确陈述FVFC-MTRL-PD取得最佳装配力柔顺与最高装配效率；Table 5（子任务T4）给出各方法最大力/力矩与控制步数，本文方法Fz=0.202N为最低。
- Quote: “To quantitatively evaluate the assembly compliance, the maximum forces/moments, and the number of control steps are recorded for each successful assembly over 50 trials per subtask. The average values for subtasks T 2 and T 4 are reported in Tables 4 and 5, respectively. It is verified that FVFC-MTRL-PD achieves the best assembly force compliance and the highest assembly efficiency among all evaluated strategies.”
- Authors: bin-wang; jiwen-zhang; song-wang; et al.

### EA-TRAJACC-2026-0050

- Claim: REMAC 通过掩码动作分块在预训练策略上学习修正性调整（使策略在'意图动作与实际执行失配'下保持鲁棒），并用前缀保留采样强化块间连续性，整体不引入任何额外推理延迟（LoRA 训练后合并进主干）。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: Abstract; 4 Methodology (4.1-4.3)
- Evidence: 摘要声明 REMAC 学习对预训练策略的修正（掩码动作分块）并引入前缀保留采样强化块间连续性，且不产生额外延迟；4 节给出三组件（前缀掩码 m_d=1[τ≥d]、自条件课程、残差对齐 L_Δ）与式 7 的保留重叠段采样，4.3 节说明 LoRA 训练后合并故推理零开销。
- Quote: “To address this, we propose REMAC, which learns corrective adjustments on the pretrained policy through masked action chunking, enabling the policy to remain resilient under mismatches between intended ac- tions and actual execution during asynchronous inference. In addition, we intro- duce a prefix-preserved sampling procedure to reinforce inter-chunk continuity. Overall, our method delivers more reliable policies without incurring additional latency.”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0051

- Claim: Kinetix 12 任务组件消融（延迟 d=0-4）证明增益来自掩码分块训练范式而非参数增加：仅加 LoRA 无性能增益（d=4 时 0.428 甚至低于朴素异步的 0.451），逐级加入前缀掩码（0.636）、自条件课程（0.710）后完整 REMAC 达 0.779；且 REMAC 在全部延迟设置上超过朴素异步、BID 与 RTC，延迟越大优势越大。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: 5.1 Kinetix Environment, Table 1
- Evidence: 5.1 节 Table 1 报告组件逐加消融：Naive 0.828/0.702/0.639/0.525/0.451（d=0..4），+LoRA 0.825/0.710/0.630/0.510/0.428，+前缀掩码 0.863/0.825/0.752/0.729/0.636，+课程 0.848/0.837/0.805/0.762/0.710，完整方法 0.888/0.879/0.859/0.817/0.779；正文明确 LoRA-only 无增益说明有效性不能归因于参数增加。
- Quote: “Table 1 reports the contribution of each component in our method. First, adding LoRA alone—without modifying the training paradigm—yields no performance gain, indicating that the effectiveness of our approach cannot be attributed merely to the increase in parameters. In contrast, progressively incorporating the components described in Sec. 4.1 leads to consistent improvements, with the full method achieving the highest overall success rate.”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0052

- Claim: Franka 真机（π_0 骨干、夹爪开口收窄强制精细控制、15Hz、端到端延迟 d=2-3）三难度抓放任务上，REMAC 完成度全部最高：Grasp-Easy 0.903（次优 0.825）、Grasp-Medium 0.943（次优 TE 0.868）、Grasp-Hard 0.812（次优 RTC 0.753）；定性上同步推理频繁停顿导致掉落与定位不准，朴素异步/TE 易过早或过晚抓放，RTC 受自身额外延迟拖累。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: 5.2 Real-World Environment, Table 3
- Evidence: 5.2 节 Table 3 报告四基线与本文方法的平均完成进度（阶段制四步得分）：Sync 0.805/0.718/0.670，Naive 0.825/0.825/0.460，TE 0.825/0.868/0.717，RTC 0.823/0.848/0.753，Ours 0.903/0.943/0.812；正文给出各基线失败模式的定性归因。
- Quote: “Results. Table 3 reports the average completion progress for each task, showing that our method achieves higher completion rates across all tasks. During execution, synchronous inference produces frequent pauses, often leading to unintended object drops and inaccurate localization. Asynchronous baselines generate smoother trajectories without pronounced jerkiness. However, Naive Async and Temporal Ensembling remain prone to premature or delayed grasping and placement. In contrast, RTC suffers fr”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0053

- Claim: 运动学平滑度证据：150ms 注入延迟下对 15 次成功回合的平均速度与加速度分析显示，同步推理产生突发性、周期性的运动学变化，异步推理方法整体更平滑，其中 REMAC 动力学最稳定、突发变化最少，同时任务完成更快——即训练侧延迟适配不仅提升完成度也直接改善末端运动的平稳性。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: 5.2 Real-World Environment, Figure 5
- Evidence: 5.2 节 Figure 5 在 Grasp-Hard、150ms 注入延迟、全部策略成功的回合上对比任务进度与平均运动学：同步推理呈周期性突变，异步方法平滑，本文方法最稳定且完成更快。
- Quote: “Quantitatively, analysis of average robot velocity and acceleration over 15 trials shows that synchronous inference produces abrupt, periodic kinematic changes, whereas asynchronous inference methods yield smoother trajectories. Among these, our method achieves the most stable dynamics with fewer abrupt changes, highlighting both speed and stability.”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0054

- Claim: 延迟鲁棒性：注入额外 75ms/150ms 延迟（模拟慢硬件/慢网络部署，总有效延迟 d=3-5）后，REMAC 仍持续超过所有基线，显示训练侧延迟适配对延迟水平变化的鲁棒性。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: 5.2 Real-World Environment, Figure 4
- Evidence: 5.2 节 Figure 4 在 Grasp-Hard 上报告 +0/+75/+150ms 注入延迟的结果：REMAC 在总延迟 3-5 下仍全胜；紧随其后正文进一步给出机制性反转——延迟增大时朴素异步相对变好（更长执行时域减少块切换）、RTC 显著退化（见 C10 卡）。附录 Table 7 显示噪声/尖峰延迟下 REMAC 仍超过准确延迟下的 RTC。
- Quote: “Figure 4 reports results with additional latency injections of 75ms and 150ms, simulating deploy- ment under slower hardware and network conditions. Even with total inference delays of 3 − 5, our method consistently outperforms all baselines, demonstrating robustness to varying delay levels.”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0055

- Claim: REMAC 与测试时方法正交可组合：因其只修改骨干策略，可与 BID/RTC 叠加且在高延迟下进一步增益（d=4 时 0.779→+RTC 0.791），证明训练侧适配与测试时修正是互补而非竞争关系，REMAC 可作为异步执行的更强骨干。
- Stance: `support` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: 5.1 Kinetix Environment, Table 2
- Evidence: 5.1 节 Table 2 报告组合结果：Ours 0.888/0.879/0.859/0.817/0.779，+BID 0.888/0.880/0.862/0.821/0.781，+RTC 0.888/0.879/0.864/0.826/0.791；正文说明增益虽小但一致，高延迟下更大。
- Quote: “Our method can further be integrated with other test-time approaches such as BID and RTC, since it only modifies the backbone policy. Table 2 shows that, although the improvements are modest, integration consistently provides additional performance gains across delay settings, with larger improvements observed under higher delays. This demonstrates both the compatibility of our approach with existing test-time strategies and its potential as a plug-and-play method.”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0057

- Claim: 该文将人形loco-manipulation末端精度退化的根源定位于本体中心坐标系指令表述：既有方法在body-centric系中表述命令，无法内在校正腿式行走诱发的世界系累积漂移；HiWET据此把问题重构为世界系末端执行器跟踪，用分层RL解耦全局推理与动态执行。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06341](https://arxiv.org/abs/2602.06341) HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation
- Locator: preamble (Abstract); I. INTRODUCTION; II-B Related Works
- Evidence: 摘要原文指出既有方法通常在body-centric系中表述命令、无法内在校正腿式行走诱发的世界系累积漂移，并提出把问题重构为world-frame end-effector tracking、以分层RL解耦全局推理与动态执行；引言进一步指出任务轨迹超出静态可达空间时机器人须主动搬运基座，body-centric表述不显式处理该协调；II-B小结指出command-driven方法在body-centric系中无法保持世界系一致性。
- Quote: “Existing approaches typically formulate commands in body-centric frames, fail to inherently correct cumulative world-frame drift induced by legged locomotion. We reformulate the problem as world-frame end-effector tracking and propose HiWET, a hierarchical reinforcement learning framework that decouples global reasoning from dynamic execution.”
- Authors: zhanxiang-cao; liyun-yan; yang-zhang; et al.

### EA-TRAJACC-2026-0058

- Claim: HiWET在物理人形平台验证中实现仿真12.4mm世界系末端跟踪误差，并在多样肢体构型下实现鲁棒零样本sim-to-real迁移。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06341](https://arxiv.org/abs/2602.06341) HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation
- Locator: I. INTRODUCTION, Table I
- Evidence: 贡献列表原文宣称在物理人形平台上的广泛验证达到12.4mm世界系跟踪误差（仿真）与跨多样肢体构型的鲁棒零样本sim-to-real；表I给出EE位置误差12.4±2.4mm（同时基座线速度误差0.157±0.003m/s、身高误差0.018±0.012m）；真机表II圆/方轨迹RMSE 0.012±0.005/0.015±0.007m与之量级一致。
- Quote: “We perform extensive validation on a physical humanoid platform, demonstrating 12.4 mm world-frame tracking error in simulation and robust zero-shot sim-to-real transfer across diverse limb configurations.”
- Authors: zhanxiang-cao; liyun-yan; yang-zhang; et al.

### EA-TRAJACC-2026-0059

- Claim: HiWET的核心精度机制是运动学流形先验（KMP）+残差动作空间：KMP把操作流形经残差学习嵌入动作空间，降低探索维度并缓解运动学无效行为；具体为上身关节命令=冻结KMP的运动学一致参考+策略残差修正，下身保持绝对关节目标。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06341](https://arxiv.org/abs/2602.06341) HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation
- Locator: preamble (Abstract); IV-A. Hybrid Action Space; IV-B. Network Architecture Overview; IV-D. Kinematic Manifold Prior Learning
- Evidence: 摘要原文定义KMP经残差学习把操作流形嵌入动作空间、降低探索维度并缓解运动学无效行为；IV-A式(5)给出具体形式q_des_t,up = q̂_t,up + Δq_t,up并说明该残差表述使控制器能在保持流形有效性的同时做细微动态调整，下身保持绝对关节目标；IV-B说明KMP离线预训练并在策略优化中冻结、使策略学残差修正而非绝对关节目标；IV-D说明KMP训练数据由PyRoki约束优化IK生成、约1000万样本。
- Quote: “We introduce a Kinematic Manifold Prior (KMP) that embeds the manipulation manifold into the action space via residual learning, reducing exploration dimensionality and mitigating kinematically invalid behaviors.”
- Authors: zhanxiang-cao; liyun-yan; yang-zhang; et al.

### EA-TRAJACC-2026-0060

- Claim: 消融显示KMP与状态估计是EE跟踪精度的两大关键：去掉KMP参考后手部误差翻倍（12.4→25.2mm）且方差增大约5倍，证明无运动学引导直接学笛卡尔任务显著更难；去掉State Estimator后跟踪退化近10mm（23.0mm），证明准确的末端反馈对补偿行走诱发振荡必要。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06341](https://arxiv.org/abs/2602.06341) HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation
- Locator: VI-B. Ablation Studies and Precision Improvements, Table I
- Evidence: VI-B消融原文：去KMP导致最显著退化——手部误差翻倍至25.2mm、方差5×，确认无运动学引导学笛卡尔任务显著更难；去State Estimator退化近10mm，准确EE反馈对补偿行走诱发振荡必要；表I完整数值为HiWET 12.4±2.4、w/o IS 16.1±5.3、w/o State Est. 23.0±7.2、w/o KMP 25.2±12.8mm，真机表II消融方向一致（w/o KMP圆/方RMSE 0.032/0.039m）。
- Quote: “HiWET w/o KMP: Removing the KMP reference causes the most significant drop—hand error doubles (25.2 mm) with 5× higher variance—confirming that learning Carte- sian tasks without kinematic guidance is significantly more challenging. • HiWET w/o State Est.: Without the state estimator, tracking degrades by nearly 10 mm, indicating that accu- rate end-effector feedback is essential for compensating locomotion-induced oscillations.”
- Authors: zhanxiang-cao; liyun-yan; yang-zhang; et al.

### EA-TRAJACC-2026-0061

- Claim: HiWET真机世界系跟踪依赖LiDAR定位链路（头部Livox Mid-360+IMU经Fast-LIO2、基座位姿10Hz正运动学更新）；在圆/方轨迹任务10次重复中达到最低跟踪误差：圆RMSE 12mm、方RMSE 15mm，消融变体（固定α、去状态估计、去KMP）误差依次增大。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06341](https://arxiv.org/abs/2602.06341) HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation
- Locator: VI-E. Real-world Hardware Experiments, Table II
- Evidence: VI-E原文：世界系位姿由头部Livox Mid-360 LiDAR+IMU经Fast-LIO2估计、基座位姿10Hz经正运动学更新；圆/方任务10次重复对比消融变体，HiWET最低（圆12mm、方15mm）；表II完整数值：w/ Fixed α 0.018/0.019m、w/o State Est. 0.024/0.028m、w/o KMP 0.032/0.039m；低层策略机载50Hz零样本部署。
- Quote: “To enable world-frame tracking, global pose is estimated using a head-mounted Livox Mid-360 LiDAR and IMU via Fast-LIO2 [ 39 ], with base position updated at 10 Hz through forward kinematics. In the circle and square trajectory tasks (Fig. 1(e,f)), we compare HiWET against ablated variants over 10 repetitions. As shown in Table II, HiWET achieves the lowest tracking errors (12 mm for circles, 15 mm for squares).”
- Authors: zhanxiang-cao; liyun-yan; yang-zhang; et al.

### EA-TRAJACC-2026-0062

- Claim: KMP以精度换速度实现实时运动学参考：较PyRoki优化求解器（5次最大迭代配置）在单样本推理上加速超过5倍（批4000时保持毫秒级延迟），使其可无缝嵌入RL训练回路提供高频运动学参考；其重构精度（AMASS重定向测试集中位位置误差<15mm、姿态误差<5度）虽逊于近精确的迭代求解器，仍足以作为双臂协调的高效运动学先验。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06341](https://arxiv.org/abs/2602.06341) HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation
- Locator: VI-D. Kinematic Manifold Prior Benchmarking, Fig. 6
- Evidence: VI-D推理效率原文：较5次最大迭代配置的PyRoki，KMP-L单样本推理加速超过5倍，并行执行下差距进一步拉大（批4000时毫秒级延迟）；重构精度原文：PyRoki因迭代本性最精确，KMP-L在AMASS重定向G1测试集上中位位置误差<15mm、姿态误差<5度，IS训练显著优于均匀采样；KMP-S为1.39M、KMP-L为7.38M参数。
- Quote: “Compared to the PyRoki solver configured with 5 maximum iterations, KMP-L exhibits over 5× speedup at a single-sample inference level.”
- Authors: zhanxiang-cao; liyun-yan; yang-zhang; et al.

### EA-TRAJACC-2026-0019

- Claim: 在7名不同手型受试者、3种手指运动×6次重复的手部跟踪评测中，最优权重标定使指尖位置MAE显著下降：食指指尖取得最大平均降幅71.5%（约35.5→10.1mm）、拇指指尖降34.8%（约15.8→10.3mm）；作者认为该收益支撑标定对外骨骼末端（指尖）表征精度的提升，对精密操作任务尤其相关。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.23592](https://arxiv.org/abs/2507.23592) Human-Exoskeleton Kinematic Calibration to Improve Hand Tracking for Dexterous Teleoperation
- Locator: IV.A. Quantitative Results / Table II, Fig. 7
- Evidence: IV.A节明确报告食指指尖取得最高平均误差降幅71.5%、拇指指尖较温和的34.8%，并把这归为对外骨骼末端表征（end-effector representation）的提升；Fig.7给出对应的绝对MAE（未标定拇指15.8mm/食指35.5mm→最优权重10.3/10.1mm），Table II给出逐受试者降幅。
- Quote: “Fingertip position accuracy improved similarly, with the index fingertip achieving the highest average error reduction (71.5%), while the thumb fingertip showed a more moderate improvement (34.8%). These gains support the calibration’s effectiveness in enhancing end-effector representation, which is especially relevant for precision manipulation tasks.”
- Authors: haiyun-zhang; stefano-dalla-gasperina; saad-n-yousaf; et al.

### EA-TRAJACC-2026-0020

- Claim: 仿真灵敏度分析：虚拟连杆参数±10%独立扰动下，近端参数（x1、y1）对指尖位置影响最强（造成高达30mm偏差），而远端参数（x3、y3）影响通常低于3-5mm——外骨骼-人体运动学失准（尤其近端虚拟连杆）是指尖跟踪误差的主要机理来源，构成标定必要性的一阶证据。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.23592](https://arxiv.org/abs/2507.23592) Human-Exoskeleton Kinematic Calibration to Improve Hand Tracking for Dexterous Teleoperation
- Locator: II.C. Kinematic Parameters Sensitivity Analysis / Fig. 3
- Evidence: II.C节对食指运动学模型的6个2D虚拟连杆坐标各做±10%独立扰动仿真：近端参数致高达30mm指尖偏差、远端参数<3-5mm；后续段落补充指尖跟踪对水平(x)扰动更敏感，与设备在手背的水平滑动一致——为优先标定近端参数与数据驱动权重提供机理依据。
- Quote: “The results, shown in Fig. 3, indicate that proximal param- eters, particularly x 1 and y 1 , exert the strongest influence on fingertip position, with 10% perturbations causing deviations of up to 30 mm. In contrast, distal parameters such as x 3 and y 3 had only minor effects, typically below 3–5 mm.”
- Authors: haiyun-zhang; stefano-dalla-gasperina; saad-n-yousaf; et al.

### EA-TRAJACC-2026-0021

- Claim: 数据驱动的最优权重标定在全部受试关节上一致取得最低MAE，均匀权重标定次之，未标定模型误差最高；平均而言最优权重带来更大误差降低（尤其在指尖层面，食指改善最一致）——每受试者500组随机权重以动捕真值搜索的权重调优是标定框架的关键组件。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.23592](https://arxiv.org/abs/2507.23592) Human-Exoskeleton Kinematic Calibration to Improve Hand Tracking for Dexterous Teleoperation
- Locator: IV.A. Quantitative Results / Fig. 6, Table II
- Evidence: IV.A节明确给出三条件排序（最优<均匀<未标定的MAE）；III.A规定每受试者随机采样500组权重（wk∈[0,10]）、以动捕真值选出最小化关节MAE的权重分布并跨受试者平均；Fig.6显示平均权重强调拇指MCP（w2/w8）与食指PIP（w3/w4）相关的第二运动环参数。
- Quote: “The optimal-weighted calibration consistently yielded the lowest MAE, followed by the even-weighted calibration, while the uncalibrated model exhibited the highest errors across all tested joints. On average, the optimal-weighted approach produced greater error reductions, particularly at the fingertip level, with the index finger showing the most consistent im- provements.”
- Authors: haiyun-zhang; stefano-dalla-gasperina; saad-n-yousaf; et al.

### EA-TRAJACC-2026-0065

- Claim: 在 LIBERO 基准上，SmoothVLA 的平滑度指标相较标准 RL 微调提升 13.8%、相较监督微调提升 4.5%。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13925](https://arxiv.org/abs/2603.13925) SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization
- Locator: 4.2 Main Results on Robotics Benchmarks
- Evidence: 4.2 节 Figure 5 的平滑度分析给出：与传统 SFT 相比平滑度指标提升 4.5%，与标准 RL 微调相比提升 13.8%，作者将其归因于混合奖励对任务成功与运动平滑的兼顾。
- Quote: “In the smoothness analysis of Figure 5, the SmoothVLA method significantly optimizes motion trajectory quality. Specifically, compared to traditional supervised fine-tuning methods, the smoothness metric improves by 4.5%; when compared to standard RL fine-tuning methods, the improve- ment reaches 13.8%.”
- Authors: jiashun-li; xiaoyu-shi; hong-xie; et al.

### EA-TRAJACC-2026-0066

- Claim: 在 LIBERO in-distribution 评测中，SmoothVLA-GRPO 平均成功率达 80.5%，比同数据微调的 Octo 基线（73.9%）高 6.6 个百分点；将轨迹平滑度评估作为插件叠加到 DPO/GRPO 等强化微调框架可再提升平均成功率 2.6%。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13925](https://arxiv.org/abs/2603.13925) SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization
- Locator: 4.2 Main Results on Robotics Benchmarks
- Evidence: 4.2 节 Results 段报告 Figure 4 的 in-distribution 结果：SmoothVLA-GRPO 80.5% 平均成功率、较 Octo +6.6 个百分点，并声明作为通用插件叠加 DPO/GRPO 后成功率再增 2.6%。
- Quote: “As shown in Figure 4, in the in-distribution benchmark evalua- tion, SmoothVLA-GRPO achieves an average success rate of 80.5%, representing a 6.6 percentage point improvement over the baseline method Octo (73.9%). This enhancement proves the effectiveness of SmoothVLA as a universal plugin—when applied to different reinforcement fine-tuning methods (DPO and GRPO) with the incorporation of trajectory smoothness evaluation, the average success rate is further increased by 2.6%”
- Authors: jiashun-li; xiaoyu-shi; hong-xie; et al.

### EA-TRAJACC-2026-0067

- Claim: 在 LIBERO-Plus 四类扰动（语言/光照/背景/布局）评测中，SmoothVLA 平均成功率领先 SFT 方法 24.2 个百分点（Table 2 中 SmoothVLA-GRPO 46.2 vs OpenVLA-SFT 22.0），GRPO/DPO 变体分别领先 7.0/5.6 个百分点，且扰动下性能降幅更小。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13925](https://arxiv.org/abs/2603.13925) SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization
- Locator: 4.2 Main Results on Robotics Benchmarks
- Evidence: 4.2 节 Table 2 的 LIBERO-Plus 鲁棒性评测显示 SmoothVLA 各变体在四类扰动下平均成功率均高于对应 OpenVLA 基线，正文总结为领先 SFT 24.2%、GRPO/DPO 变体领先 7%/5.6%，且降幅更小。
- Quote: “The robustness evaluation in Table 2 further confirms the superiority of the method. SmoothVLA leads super- vised fine-tuning methods by 24.2% in average success rate, with variants based on GRPO and DPO leading by 7% and 5.6%, respectively. More importantly, when facing out-of- distribution perturbations, SmoothVLA exhibits smaller per- formance degradation, indicating stronger generalization ca- pability and stability.”
- Authors: jiashun-li; xiaoyu-shi; hong-xie; et al.

### EA-TRAJACC-2026-0068

- Claim: 在 LIBERO-Spatial 奖励消融（每设置独立 5 次取平均）中，含 jerk 平滑项的完整奖励 R_smooth 在五个评估维度平均 54.1，优于纯二值奖励 R_binary（48.2，差 5.9）与随机噪声奖励 R_random（46.5，差 7.6），说明增益来自结构化物理先验而非任意密集奖励扰动。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.13925](https://arxiv.org/abs/2603.13925) SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization
- Locator: 4.3 Ablation Study of Reward Model
- Evidence: 4.3 节 Table 3 在保持训练超参一致、仅改奖励设计的对照下，R_smooth 五维平均 54.1 最高，R_binary 48.2、R_random 46.5；正文结论明确平滑奖励项显著优于二值与随机奖励配置。
- Quote: “The results indicate that: (1) incorporating the smooth- ness reward term R smooth significantly enhances overall per- formance compared to basic binary rewards and random re- ward perturbations; (2) all reward components contribute sub- stantially to model robustness across different perturbation types.”
- Authors: jiashun-li; xiaoyu-shi; hong-xie; et al.

### EA-TRAJACC-2026-0070

- Claim: 在 150±30 ms 模拟广域网时延下，Oracle 预测器上的 SPO 在 StackBlocks 与 InsertSquarePeg 均达 100% 任务成功率（Steps 518.8/291.4，墙钟 15.7s/11.0s，累计空闲 4.8s/2.7s），而同步阻塞 Blocking 与 K=1 投机缓存 T1-SC 因持续网络停顿成功率均为 0%；SPO 与静态满树缓存 NFTC(K=10) 墙钟时间几乎相同，K=10@50 Hz 提供 200 ms 时间自主性足以桥接 150 ms RTT。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19418](https://arxiv.org/abs/2603.19418) Speculative Policy Orchestration: A Latency-Resilient Framework for Cloud-Robotic Manipulation
- Locator: V-B. Results and Discussion, 1) Experiment Evaluation with Oracle Models / Table II
- Evidence: V-B.1 报告 Oracle 模型下 Table II 结果：两个简单任务上 SPO/NFTC 成功率 100%、Blocking/T1-SC 为 0%；两个投机方法都把视界饱和在 K=10，墙钟时间几乎一致。
- Quote: “Both SPO and NFTC saturate the speculative horizon at K = 10 (200 ms of temporal autonomy), achieving near- identical wall-clock times ( 15.7s for StackBlocks).”
- Authors: chanh-nguyen; shutong-jin; florian-t-pokorny; et al.

### EA-TRAJACC-2026-0071

- Claim: ϵ-tube 验证机制：边缘节点在每个控制步用逆方差加权距离度量 e_t=√((s_t−ŝ_t)ᵀW(s_t−ŝ_t)) 比对实际状态与缓存预测状态，偏差在一个控制周期内被检出；e_t≤ϵ_base 时缓存命中并执行缓存动作，否则缓存失效、发出零速保持命令安全停止机器人并请求云端同步重规划——该机制不依赖神经策略的概率置信度，规避了校准失准风险。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19418](https://arxiv.org/abs/2603.19418) Speculative Policy Orchestration: A Latency-Resilient Framework for Cloud-Robotic Manipulation
- Locator: IV-C Continuous-State ϵ-Tube Verification
- Evidence: IV-C 说明精确状态匹配在连续环境中因摩擦/驱动噪声/传感器方差不可用，故采用连续状态验证器：确定性 ϵ-tube 包住预测轨迹，每步验证、越界即失效+零速保持+同步重规划。
- Quote: “Safety is enforced via a deterministic ϵ-tube around the predicted trajectory in this normalized state space. Because verification occurs at every control step, deviations are de- tected within a single control cycle. If e t ≤ ϵ base (line 9–11), a Cache Hit is registered and the cached action a t is executed immediately. Otherwise, a Cache Miss occurs, the edge node invalidates the cached trajectory, issues a zero-velocity hold command to safely stop the robot, and requests synchronous replanni”
- Authors: chanh-nguyen; shutong-jin; florian-t-pokorny; et al.

### EA-TRAJACC-2026-0072

- Claim: 固定投机深度存在根本权衡：更大 K 改善时延掩蔽但放大模型误差，更小 K 减少开环暴露但重新引入网络阻塞；SPO 的 AHS 以 AIMD 规则自适应调节——缓存命中时加性扩张 K←min(K_max,K+β)，失配时按危险比 ρ=e_miss/ϵ_base 乘性收缩 K←max(K_min,⌊K/ρ⌋)——使带宽与缓存容量随物理不确定度线性 O(K) 增长而非指数。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19418](https://arxiv.org/abs/2603.19418) Speculative Policy Orchestration: A Latency-Resilient Framework for Cloud-Robotic Manipulation
- Locator: IV-B Adaptive Horizon Scaling (AHS) / III-B Cloud-Induced Delay and Open-Loop Vulnerability
- Evidence: III-B 指出静态深度的两难（深缓存无高频验证会在接触时灾难性不稳定；浅缓存无法掩蔽时延导致控制饥饿）；IV-B 给出 AIMD 规则定义与界：命中时线性增长至多 (K_max−K_min)/β 个周期达 K_max，失配时按误差严重度 ρ 乘性收缩。
- Quote: “A critical challenge in speculative orchestration is deter- mining the optimal pre-fetch horizon (K). Static pre-fetching methods that cache deep, multi-second velocity plans without high-frequency validation risk catastrophic instability upon physical contact. Conversely, caching too few steps fails to mask network latency, leading to control starvation.”
- Authors: chanh-nguyen; shutong-jin; florian-t-pokorny; et al.

### EA-TRAJACC-2026-0073

- Claim: 学习模型（3 层 MLP，精度有限）下，SPO 相对同步 Blocking 基线把网络空闲时间降低 60% 以上，同时比静态 NFTC(K=10) 基线少丢弃约 60% 的云端预测，是唯一同时最小化空闲时间与计算浪费的方法；即使学习策略与世界模型精度有限，SPO 框架仍保持稳健。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19418](https://arxiv.org/abs/2603.19418) Speculative Policy Orchestration: A Latency-Resilient Framework for Cloud-Robotic Manipulation
- Locator: V-B. Results and Discussion, 2) Experimental Evaluation with Learned Models / Figure 7
- Evidence: V-B.2 报告 InsertOntoSquarePeg（learned MLP）的 Figure 7 结果：空闲时间较 Blocking 降 60%+（Fig. 7a）、丢弃预测较 NFTC 少约 60%（Fig. 7b）、效率权衡图（Fig. 7c）中 SPO 是唯一同时最小化两者的方法。
- Quote: “As shown in Figure 7 for the InsertOntoSquarePeg task, SPO achieves near-optimal latency masking, reducing net- work idle time by over 60% compared to the Blocking baseline (Fig. 7a). Crucially, SPO achieves this efficiency while discarding approximately 60% fewer cloud predictions than the NFTC (K = 10) baseline (Fig. 7b).”
- Authors: chanh-nguyen; shutong-jin; florian-t-pokorny; et al.

### EA-TRAJACC-2026-0076

- Claim: 在 Quanser 2DSFMR 主连杆-关节子系统实验（正弦 40pi/180@0.2 Hz、方波 35pi/180@0.1 Hz、锯齿 35pi/180@0.2 Hz 三种参考轨迹，副连杆作集中质量）中，backstepping 输出反馈控制器相对 LQR+前馈取得更小的关节跟踪误差、更快的振动抑制、更小且更快收敛到零的末端跟踪误差（正文未给出数值）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.17477](https://arxiv.org/abs/2605.17477) Rapid Vibration Suppression and Trajectory Tracking of a Serial Manipulator with Multi-Flexible Links
- Locator: B. Trajectory Tracking on Primary Link of 2DSFMR
- Evidence: IV.B 节实验结果原文明确陈述三种参考轨迹下所提控制器的关节误差更小、振动抑制更快、末端误差更小且更快收敛，结论节重申相对 LQR+前馈基线的优越性。
- Quote: “As shown in the Fig. 3 a) and b), the proposed controller achieves a smaller joint tracking error and faster vibration suppression across all three reference trajectories compared to the LQR+feedforward approach. Fig. 3 c) shows that the proposed controller yields a smaller tip tracking error than the LQR approach, and moreover, it is obvious that the proposed controller achieves faster convergence of the tip tracking error to zero under the square and sawtooth trajectories. This indicates that”
- Authors: chengyi-wang; yilong-huang; ji-wang

### EA-TRAJACC-2026-0077

- Claim: 在整机 2DSFMR 极坐标轨迹跟踪实验（正弦/方波/锯齿 (r,phi) 轮廓）中，backstepping 方法的末端极径与极角跟踪误差均小于 LQR+前馈，且在方波与锯齿轨迹下末端跟踪误差更快收敛到零。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.17477](https://arxiv.org/abs/2605.17477) Rapid Vibration Suppression and Trajectory Tracking of a Serial Manipulator with Multi-Flexible Links
- Locator: C. Trajectory Tracking on 2DSFMR
- Evidence: IV.C 节整机实验结果陈述 backstepping 的末端极径与极角误差均更小，且方波/锯齿下末端误差更快收敛到零。
- Quote: “Additionally, both the tip polar radial and tip polar angle tracking errors under the backstepping is smaller than those of the LQR+Feedforward method, and furthermore, both proposed controllers achieve faster convergence to zero of the end-effector tracking error of 2DSFMR under the square and sawtooth trajectories.”
- Authors: chengyi-wang; yilong-huang; ji-wang

### EA-TRAJACC-2026-0078

- Claim: 观测器仅用边界测量重构未测分布状态：在三种植入大初始误差的参考轨迹下，横向位移斜率估计的最大误差约 0.013（源于注入的初始误差），RMSE 为 0.00013-0.00130、MAE 为 0.00009-0.00047（表 II，x*=0 与 0.5L*1 两位置）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.17477](https://arxiv.org/abs/2605.17477) Rapid Vibration Suppression and Trajectory Tracking of a Serial Manipulator with Multi-Flexible Links
- Locator: B. Trajectory Tracking on Primary Link of 2DSFMR
- Evidence: IV.B 节表 II 给出观测器在三种轨迹、两个空间位置上估计横向位移斜率的 ME/RMSE/MAE 统计：ME 约 0.013（注入初始误差所致），RMSE 与 MAE 保持在 1e-4 量级。
- Quote: “the state estimates of ϖ 1,x ∗ (x ∗ , t ∗ ), at x ∗ = 0 and x ∗ = 0.5L ∗ 1 , converge rapidly, despite the large initial estimation error and the abrupt signal variations in the square and sawtooth waves. The statistical results further confirm this behavior. Although the ME reaches 0.013 due to the injected initial error, both the MAE and RMSE remain very low, demonstrating the robustness and accuracy of the proposed estimation scheme.”
- Authors: chengyi-wang; yilong-huang; ji-wang

### EA-TRAJACC-2026-0079

- Claim: 机制主张：backstepping 边界控制仅用边界（关节级）执行即可等效注入沿整条柔性结构的分布式阻尼，区别于在特定位置注入阻尼的已有 PDE 方法；阻尼剖面可由设计参数调节，从而实现快速振动抑制与末端快速收敛。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.17477](https://arxiv.org/abs/2605.17477) Rapid Vibration Suppression and Trajectory Tracking of a Serial Manipulator with Multi-Flexible Links
- Locator: D. Main Contribution
- Evidence: 贡献 2 原文陈述所提 backstepping 控制用仅边界执行实现沿整个柔性结构注入等效分布式阻尼，阻尼剖面可由控制设计参数调节。
- Quote: “In contrast, the proposed backstepping-based control achieves an equivalent spatially distributed damping injected along the entire flexible structure using only boundary actuation. The damping profile can be tuned via control design parameters, leading to rapid vibration suppression and fast convergence of the end-effector to the desired trajectory.”
- Authors: chengyi-wang; yilong-huang; ji-wang

### EA-TRAJACC-2026-0083

- Claim: DWS 的核心机制是在不扩大动作空间的前提下实现隐式动作分块：策略保留标准 d 维输出，用 h 步执行窗口（确定性执行算子把参考动作变换为局部连贯运动）与同步价值窗口（窗口对齐 TD 目标）耦合，辅以时序正则，从而桥接时间抽象与逐步控制。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.19592](https://arxiv.org/abs/2605.19592) Implicit Action Chunking for Smooth Continuous Control
- Locator: 1. Introduction
- Evidence: 引言方案段落明确：DWS 保留标准 d 维动作输出以规避优化不稳定，通过执行算子把参考动作变换为局部连贯运动并用时序正则强化，同时用同步价值窗口对齐 critic 训练与 h 步执行承诺。
- Quote: “To address these challenges, we propose Dual-Window Smoothing (DWS), an implicit action chunking framework that bridges the gap between temporal abstraction and step- wise control by coupling an h-step execution window with a synchronized value window. Diverging from explicit tra- jectory prediction, DWS retains a standard d-dimensional action output to circumvent optimization instability, instead achieving smoothness via an execution operator that trans- forms reference actions into locally coh”
- Authors: bosun-liang; shuo-pei; zirui-chen; et al.

### EA-TRAJACC-2026-0084

- Claim: 在 DMC 精度类任务上，DWS 相对 vanilla 基线将平均波动率（AFR）降低超 80%（Reacher-Hard 从 0.56 降至 0.10），且在 Ball-in-Cup 等高动态环境中降低物理 jerk 的同时保留宏观反应性。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.19592](https://arxiv.org/abs/2605.19592) Implicit Action Chunking for Smooth Continuous Control
- Locator: 4.2. Case Study of DeepMind Control Suite
- Evidence: 4.2 节引用 Figure 6 的量化结果：精度任务 AFR 降低超 80%，Reacher-Hard 从 0.56 到 0.10；附录 Table 10 的 5-seed 数值（DWS-SAC AFR L2 0.01±0.00 vs Vanilla-TD3 0.56±0.65）与正文一致。
- Quote: “As quantified in Figure 6, DWS reduces the AFR by over 80% in precision tasks compared to vanilla baselines (e.g., AFR from 0.56 to 0.10 in Reacher-Hard). Importantly, this improvement preserves responsiveness. Even in highly dynamic environments such as Ball-in-Cup, DWS reduces physical jerk while preserving macroscopic reactivity for successful swing-up and recovery.”
- Authors: bosun-liang; shuo-pei; zirui-chen; et al.

### EA-TRAJACC-2026-0085

- Claim: 在 CARLA LCO 任务（NPC 5 m/s 最难设置）上，DWS 达到 100% 成功率且 0% 碰撞与出界，而全部基线成功率 ≤20%（SOTA 平滑基线 LipsNet++ 仅 20%）；DWS 较 LipsNet++ 降低转向执行抖动（ActSmooth）88.7%、横摆角速度振荡 78.5%。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.19592](https://arxiv.org/abs/2605.19592) Implicit Action Chunking for Smooth Continuous Control
- Locator: 4.4. Case Study of Autonomous Vehicle Task
- Evidence: 4.4 节 LCO 主结果（Table 2）：DWS 100%/0%/0%，LipsNet++ 20%，HG-TD3/L2C2/ActionChunk/SmODE 均 0%；正文给出 ActSmooth 与 yaw rate 相对 LipsNet++ 的降幅 88.7%/78.5%，附录 F.2.3 的速度扫描显示 DWS 在 0-5 m/s 全速度段保持 100%。
- Quote: “DWS achieves a 100% success rate with 0% collisions and boundary violations, exhibiting robust compliance with safety constraints. In stark contrast, all baselines struggle significantly; notably, LipsNet++ (2025), a state-of-the-art smooth-policy baseline, only attains a 20% success rate. DWS not only completes the task reliably but does so with superior stability, reducing steering actua- tion jitter (ActSmooth) by 88.7% and yaw rate oscillation by 78.5% compared to LipsNet++.”
- Authors: bosun-liang; shuo-pei; zirui-chen; et al.

### EA-TRAJACC-2026-0086

- Claim: 在 LCO 最难设置的组件消融中，各部分变体均优于 HG-TD3 骨干（仅执行窗口 SR 0.50、仅价值窗口 0.65、价值窗口+正则 0.80、仅正则 0.60，骨干 0.00），但只有完整 DWS 同时达到 100% 成功率、零碰撞与最优整体平滑度，说明平滑执行与价值对齐缺一不可。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.19592](https://arxiv.org/abs/2605.19592) Implicit Action Chunking for Smooth Continuous Control
- Locator: 4.7. Ablation Study
- Evidence: 4.7 节 Table 7 的组件消融显示强组件间依赖：执行窗口单独使用改善舒适度指标但成功率受限，价值窗口单独使用大幅提升成功率但仍不及完整框架，加正则进一步改善权衡，完整 DWS 唯一达到 100%/0%。
- Quote: “The results again reveal a strong interde- pendence among components. Each partial variant improves over the HG-TD3 backbone on either task success or mo- tion smoothness, but none matches the complete model. In particular, the execution window alone improves comfort- related metrics but remains limited in task success, while the value window alone substantially boosts success yet still falls short of the full framework.”
- Authors: bosun-liang; shuo-pei; zirui-chen; et al.

### EA-TRAJACC-2026-0089

- Claim: PACE 是训练无关的测试时执行方法：从预测动作块自身的速度剖面中识别低速转换点作为候选重规划边界来在线选择执行时域，仅使用预测块本身，即插即用，不需重训练、不需访问策略内部信号。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: Abstract; 3.3 Phase-Aware Execution Horizon Selection
- Evidence: 摘要与方法节声明 PACE 利用操作轨迹的相位依赖运动学结构（相位转换处减速），把预测速度剖面的低速谷作为候选重规划边界；因其只用预测动作块，无需重训练或策略内部访问。3.2/3.3 节给出速度剖面构建、平滑、显著度评分与演示校准阈值的具体流程。
- Quote: “We propose PACE (Phase-Aware Chunk Execution), a training-free test-time execution method that selects the execution horizon online from the predicted chunk itself. PACE exploits the phase-dependent kinematic structure of manipulation trajectories by identifying low-speed transition points in the predicted speed profile and using them as candidate replanning boundaries. Because PACE uses only the predicted action chunk, it is plug-and-play and requires no retraining or access to policy internals”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

### EA-TRAJACC-2026-0090

- Claim: 在 50 个 RoboTwin2.0 任务上（每任务-方法 900 episodes、每方法共 45,000 episodes），PACE 把平均成功率从最强全局固定基线 H=25 的 57.8% 提升到 64.2%（+6.4 个百分点），且六个代表性任务全部超过最强固定基线（+2.3~+9.6）；因所有方法共享同一训练 checkpoint，增益可归因于测试时执行规则。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: 4.1 Simulation Results, Table 1
- Evidence: 4.1 节 Table 1 显示固定基线 H=5/25/50 的 50 任务平均分别为 48.8/57.8/53.4，PACE 为 64.2（+6.4 over H=25）；Table 1 六个代表任务上 PACE 分别 +2.9/+2.3/+6.8/+7.9/+9.6/+6.9。正文明确该设计隔离执行规则的影响。
- Quote: “Table 1 shows that PACE achieves the best 50-task average success rate. Among the fixed-horizon baselines, H = 25 is the strongest global choice, reaching 57.8%. PACE improves this average to 64.2%, a gain of 6.4 points, without task-specific horizon sweeps or changes to the underlying policy. Because all methods share the same trained checkpoint within each task, the improvement is attributable to the test-time execution rule.”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

### EA-TRAJACC-2026-0091

- Claim: 真机实验（RoboChallenge ALOHA 双臂两任务各 30 trials + Franka 单臂放置任务族 100 trials）中，PACE 相对同 checkpoint 全块执行基线（H=50）三设置全部提升：平均任务 Score 从 60.7 升到 77.7、平均全完成率从 50.7% 升到 70.4%，其中 Franka place_object_on_plate 从 72.0% 提升到 88.0%（五物体变体全部 +10~+25 个百分点）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: 5.1 Real-Robot Results, Table 5
- Evidence: 5.1 节 Table 5 报告三真机设置的 Score/Succ.：stack_bowls 70.0%→90.0%、put_pen_into_pencil_case 10.0%→33.3%、place_object_on_plate 72.0%→88.0%；附录 E.5 Table 9 显示 Franka 五物体全部提升。基线与 PACE 共享同一微调 checkpoint，仅执行规则不同。
- Quote: “Table 5 compares PACE with the corresponding baseline under the same real-robot setup and metric. PACE improves all three evaluated settings. On the two RoboChallenge tasks, it increases both the partial-credit Score and the full-completion rate. On the Franka place_object_on_plate task family, where Score and Succ. are identical, PACE improves performance from 72.0% to 88.0%. Averaged over the three real-robot evaluations, PACE raises the Score from 60.7 to 77.7 and Succ. from 50.7% to 70.4%.”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

### EA-TRAJACC-2026-0092

- Claim: 匹配平均时域诊断表明 PACE 的增益来自重规划时机的位置而非查询频率：在全部六个代表任务上，PACE 超过按其平均执行长度匹配的固定调度（+1.6~+10.6 个百分点，如 Place A2B Right 54.6 vs 44.0），说明其收益是把重规划边界放在相位结构更合适的位置（低速转换附近），而非更频繁地查询策略。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: 4.4 PACE versus Fixed-Horizon Sweeps, Table 4
- Evidence: 4.4 节构造匹配时域基线：取 PACE 全评测的平均选中时域四舍五入为常数 H，从 seed-0 扫描读取该 H 的成功率。Table 4 显示六任务 PACE 全部胜出（+1.6/+2.6/+10.6/+4.3/+1.9/+7.2），控制平均查询频率后剩余差异是重规划边界的放置位置。
- Quote: “Since the matched fixed baseline executes a constant horizon chosen to match PACE’s average executed horizon, this comparison controls for average replanning frequency. The re- maining difference is the placement of replanning boundaries. These gains therefore indicate that PACE does not merely bene- fit from using a shorter or longer average horizon; it improves performance by choosing more appropriate replanning points within the rollout, using the predicted chunk’s phase structure.”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

### EA-TRAJACC-2026-0096

- Claim: 在工业计量检测系统晶圆台（x 方向、500 次点到点运动）的实验 D1 中，将速度/加速度/加加速度前馈与柔顺补偿四个参数全部纳入递归学习后，参数收敛后的伺服误差（以累积功率谱密度表征）改善因子为 7。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.03533](https://arxiv.org/abs/2606.03533) Recursive Learning of Feedforward and Compliance Compensation Parameters for Precision Motion Systems
- Locator: 5.2 Experimental results
- Evidence: 5.2 节实验结果原文明确陈述'all parameters are included'时伺服误差改善因子为 7，并以 Fig. 6 的收敛后累积功率谱密度对比为依据。
- Quote: “in terms of the cumulative power spectral density of the servo error for different parameter sets after parameter convergence. Observe that the servo error is improved by a factor of 7 when all parameters are included”
- Authors: m-wind; j-pierssens; r-beerens; et al.

### EA-TRAJACC-2026-0097

- Claim: 在同一实验 D1 中，学习收益的参数贡献分解为：速度前馈 92.5%、加速度前馈 6.5%、柔顺补偿 1%，加加速度前馈贡献可忽略（该设置下）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.03533](https://arxiv.org/abs/2606.03533) Recursive Learning of Feedforward and Compliance Compensation Parameters for Precision Motion Systems
- Locator: 5.2 Experimental results
- Evidence: 5.2 节给出各补偿参数的量化贡献占比（92.5%/6.5%/1%），并明确 jerk 前馈在该设置下贡献可忽略，原文限定'for the setting considered'。
- Quote: “in the learning framework. The individual contributions for the velocity, acceleration and compliance compensa- tion contribute to 92.5%, 6.5%, 1%, respectively, where the contribution of jerk feedforward is negligible for the setting considered.”
- Authors: m-wind; j-pierssens; r-beerens; et al.

### EA-TRAJACC-2026-0099

- Claim: 采用多变量回归同时估计四个参数可显著降低参数耦合，尤其是速度-加加速度耦合；加速度-柔顺耦合在仿真中明显、实验中较不显著，作者推测因自适应增益相对较高。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.03533](https://arxiv.org/abs/2606.03533) Recursive Learning of Feedforward and Compliance Compensation Parameters for Precision Motion Systems
- Locator: 5.2 Experimental results
- Evidence: 5.2 节实验 D2 与仿真 Ds 显示单变量回归下出现速度-加速度与加速度-柔顺耦合，改用多变量回归后耦合显著降低；结论节重申这一发现。
- Quote: “The coupling between acceleration and compliance compensa- tion is also clearly visible in Fig. 8, yet less prominent in Fig. 9, most likely due to relatively high adaptation gains. By adopting multivariate regression as proposed in (20) the coupling between parameters, especially seen in velocity and jerk coupling, has been significantly reduced.”
- Authors: m-wind; j-pierssens; r-beerens; et al.

### EA-TRAJACC-2026-0103

- Claim: 时间索引条件化的机制归因：在 held-out 轨迹集上移除时间索引仅轻微影响成功率（99.4→98.9），但使 Pos_1s 从 8.6 cm 增至 14.6 cm、Rot_1s 从 12.8° 增至 26.6°、速度误差同步增大——时间索引主要通过解决每个异步参考区间内的相位失配来抑制帧漂移。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25706](https://arxiv.org/abs/2606.25706) Learning Asynchronous Upper-body Task-space Trajectory Tracking Policy for Humanoid Robots
- Locator: VI-B. Effect of Asynchronous Sparse Trajectory Tracking, Table II
- Evidence: Table II 的受控消融显示时间索引对成功率影响小但对异步区间误差影响大；正文明确确认时间索引主要解决相位失配，并附带给策略推理时速度调制能力。
- Quote: “As shown in Table II, removing the time index only slightly affects success rate, but increases Pos 1s from 8.6 cm to 14.6 cm and Rot 1s from 12.8 ◦ to 26.6 ◦ . This confirms that the time index mainly helps resolve the phase mis- match within each asynchronous reference interval.”
- Authors: yumeng-liu; dongqi-wang; jiyu-yu; et al.

### EA-TRAJACC-2026-0104

- Claim: 局部跟踪精度与异步帧一致执行解离：解耦式基线（基座与上半身分模块控制）取得最低局部位置误差（Pos_loc 2.61 cm），但成功率仅 92.30% 且异步误差更差（Pos_1s 9.11 cm、Rot_1s 15.51°）——在异步稀疏参考下解耦控制不足，统一端到端异步建模（ASYNC-CA：99.60%、6.00 cm/6.43°）才能实现稳定的全身跟踪。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25706](https://arxiv.org/abs/2606.25706) Learning Asynchronous Upper-body Task-space Trajectory Tracking Policy for Humanoid Robots
- Locator: VI-C. Comparison of Base-augmented Tracking, Table I
- Evidence: Table I 最后三行对比解耦基线、无估计器与完整 ASYNC-CA；正文明确指出解耦基线的局部精度未转化为更好的异步跟踪与成功率，统一端到端建模更有效。
- Quote: “However, this local accuracy does not lead to better asyn- chronous tracking and a lower success rate of 92.30%. This indicates that decoupled control alone is insufficient under asynchronous sparse references, while our unified end-to-end asynchronous modeling is more effective for stable whole- body tracking.”
- Authors: yumeng-liu; dongqi-wang; jiyu-yu; et al.

### EA-TRAJACC-2026-0107

- Claim: 自引导正则的真机必要性：OOD 后训练中移除自引导不会立即降低（仿真）成功率，但由于稀疏头/手命令使下半身关节不受约束，策略在满足跟踪目标的同时下半身漂移到异常构型（足外翻、膝外翻），导致真机迁移差；启用自引导后下半身保持自然稳定并可靠迁移到 G1 硬件——末端跟踪精度目标之外的自由度需要运动先验正则约束。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25706](https://arxiv.org/abs/2606.25706) Learning Asynchronous Upper-body Task-space Trajectory Tracking Policy for Humanoid Robots
- Locator: VI-E. Real-world Hardware Experiments, Fig. 7
- Evidence: VI-E 真机实验第一项消融显示去自引导的失败模式是下半身异常构型而非跟踪失败（Fig. 7 足外翻示例），带自引导则可靠迁移；正文据此确认自引导对约束未观测下半身运动的必要性。
- Quote: “Removing self-guidance does not immediately drop the success rate; however, because the sparse head-and-hand commands leave lower-body joints unspecified, the policy can satisfy the tracking objective while the lower body drifts into unnatural configurations. As shown in Fig. 7, this leads to abnormal lower-body motions (foot eversion, knee valgus) and poor real-robot transfer.”
- Authors: yumeng-liu; dongqi-wang; jiyu-yu; et al.

### EA-TRAJACC-2026-0109

- Claim: 论文的核心立论：异步分块控制的主导误差是局部交接问题而非全局任务理解丢失——延迟下视觉与语言输入通常仍正确指定任务与粗规划，不可靠的只是从已执行运动的延续；这把延迟控制重新表述为块交接处的边界条件化问题。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: I. Introduction
- Evidence: 引言显式陈述主导误差为局部 handoff 问题的判断，并由此推出边界条件化的问题表述；这是 ACNet 只改动作头、冻结骨干的设计依据。
- Quote: “The dominant error in asynchronous chunked control is treated here as a local handoff problem rather than a global loss of task understanding. Under inference delay, the visual and language inputs can often still specify the task and coarse plan correctly, while the unreliable component is the continuation from the motion already being executed.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0110

- Claim: delay action 编码机制：已执行后缀保留、未观测未来位用可学习 token 填充（显式标记不可用槽位，避免零动作的歧义与噪声填充的人为变异），再经轻量 transformer 编码器与动作专家相同的终端时序池化得到条件向量。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: IV-A. Delay-Action Encoding
- Evidence: IV-A 节给出 delay action 的填充与编码设计：可学习 padding token 显式标记不可用槽位，编码后复用动作专家的终端池化以对齐其时序抽象。
- Quote: “where p j ∈ R d a denotes the padding token at future position j. Learnable padding explicitly marks unavailable slots, avoiding the ambiguity of zero actions and the artificial variation of noise padding. ACNet then applies a lightweight transformer encoder E ϕ to e a delay t , followed by the same terminal temporal pooling operator used in the action expert, yielding”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0111

- Claim: 残差注入机制：因预训练骨干已编码任务上下文，ACNet 仅把延迟上下文注入动作头，且注入为残差形式使原预测器保持默认模式——延迟线索无信息时侧分支可塌缩为零。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: IV-B. Residual Injection as Local Boundary Correction
- Evidence: IV-B 节开头说明注入设计原则：只注入动作头、残差形式保持原预测器为默认模式；式(11)后的说明指出该紧凑侧分支在延迟线索无信息时可塌缩为零。
- Quote: “Because the pretrained backbone already encodes the task context, ACNet injects the delay context only into the action head. The injection is residual so that the original predictor remains the default mode.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0112

- Claim: 一阶雅可比论证（式 12）：ACNet 只需产出一个残差方向，使其下游效应匹配期望的边界修正，而非从头重建整个动作块——支持把异步延迟当作局部边界条件化而非完整视觉运动重映射，也解释了为何只需在动作头层面做轻量修正。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: IV-B. Residual Injection as Local Boundary Correction
- Evidence: IV-B 节对式(12)的解读：对小块内下游映射 g_l 做一阶展开，残差 u_l 的下游效应近似为雅可比左乘，故只需匹配期望边界修正的残差方向即可。
- Quote: “Equation (12) provides a local intuition: to first order, ACNet only needs to produce a residual direction whose downstream effect matches the desired boundary correction, rather than reconstructing the entire chunk from scratch. This supports treating asyn- chronous delay as local boundary conditioning rather than full visuomotor remapping.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0113

- Claim: 训练效率机制：由于 ACNet 只挂在动作头，固定观测-指令对的视觉-语言潜变量对采样延迟不变，故缓存一次即可跨多个延迟条件复用，无需为每个采样延迟重复前向全骨干——这是 20% 参数适配成本低于全量延迟条件化重训练的关键。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: IV-C. Training Objective
- Evidence: IV-C 节说明训练目标的效率设计：潜变量缓存与跨延迟复用增加延迟覆盖同时摊销骨干计算。
- Quote: “Because ACNet is attached only to the action head, delay robustness can be learned without repeatedly forwarding the full backbone for every sampled delay. For a fixed observation-instruction pair, the visual-language latent pro- duced by B ω (o t , l) is invariant to the sampled delay. This latent is therefore cached once and reused across multiple delay conditions.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0114

- Claim: Kinetix 上延迟档（d>0）平均成功率 ACNet 0.79，接近 Training-RTC 的 0.80，高于 RTC 0.72 与 Naïve Async 0.61；该鲁棒性仅训练约 20% 的模型参数获得，而 Training-RTC 更新 100%——即以约 80% 更低的可训练参数比例获得相当鲁棒性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: V-C. Quantitative Results, Table I
- Evidence: V-C 节报告 Table I：ACNet 平均 0.79 vs Training-RTC 0.80/RTC 0.72/Naïve Async 0.61，可训练参数约 20% vs 100%；正文明确总结为约 80% 更低的可训练参数比例。
- Quote: “Table I reports Kinetix results. Averaged over delayed settings, ACNet reaches 0.79 success, compared with 0.72 for RTC and 0.61 for Naïve Async , while remaining close to Training-RTC at 0.80. This robustness is obtained while training only around 20% of all model parameters, whereas Training-RTC updates 100%.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0115

- Claim: Meta-World MT50 上 ACNet 平均成功率 0.74，超过 Naïve Async（0.70）与 RTC（0.71）并匹配 Training-RTC（0.74）；端到端延迟 91 ms、控制频率 11.0 Hz，优于 RTC（159 ms/6.28 Hz）与 Training-RTC（134 ms/7.46 Hz）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: V-C. Quantitative Results, Table II
- Evidence: V-C 节报告 Table II：ACNet 0.74 平均成功率、91 ms 延迟、11.0 Hz 频率，均优于或匹配三个基线；H=50、e=25、d∈{0,5,10,15}。
- Quote: “Table II shows the same trend on Meta- World MT50. ACNet achieves 0.74 average success, ex- ceeding Naïve Async and RTC and matching Training- RTC, while reducing latency to 91 ms versus 159 ms for RTC and 134 ms for Training-RTC. Its achieved control frequency is 11.0 Hz, compared with 6.28 Hz and 7.46 Hz”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0117

- Claim: 真机 SO-ARM101（50 条训练 rollout、10 epochs、2 任务各 10 trials、与仿真相同异步协议）：ACNet 总成功率 20/20（put cube into box 10/10、clean table 10/10），Naïve Async 17/20（9/10、8/10）。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: V-D. Real-World Experiments, Table III
- Evidence: V-D 节报告 Table III 真机结果：ACNet 两任务全成功 20/20，Naïve Async 17/20；定性 rollout 显示 Naïve Async 块转换附近振荡更大、ACNet 交接更平滑且接触更稳。
- Quote: “The real-world dataset contains 50 training rollouts. The model is optimized for 10 epochs and evaluated on put the blue cube into the box and clean the table over 10 trials per task under the same asynchronous protocol as simulation. The quantitative results are summarized in Table III. ACNet achieves 20/20 total successes across the two tasks, whereas Naïve Async achieves 17/20.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0119

- Claim: 消融（Meta-World MT50、Evo-1 骨干）支持两个核心设计选择：仅最后块注入的跨延迟鲁棒性最好，早期层注入（尤其层 0）损害鲁棒性；可学习填充 token 在每个测试延迟上均优于零填充与随机噪声填充。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: V-F. Ablation Study
- Evidence: V-F 节消融：层活动度分析（K=1000 流匹配步）显示最后块活动度最大；Fig. 7(a) 确认最后块条件化跨延迟最优；Fig. 7(b) 确认可学习填充优于零/噪声填充。
- Quote: “The injection ablation in Fig. 7(a) confirms this choice: final-block conditioning is best across delays, while early-layer injection, especially at layer 0, degrades robustness. This supports using the delay action as a local boundary cue rather than an early perturbation to the task representation. Fig. 7(b) shows that learnable padding tokens outperform zero and random-noise padding at every tested delay.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0133

- Claim: 在两架Crazyflie 2.1紧编队硬件实验（60次运行、每案例重复5次、指令间距0.3/0.4m）中，仅含下洗ROM的反馈线性化控制器（ROM-FBL）相对名义动力学基线平均降低RMSE 24%、最大垂直误差30%；叠加学习残差后（Learned-FBL）在ROM-FBL之上再降RMSE 29%、z_max 43%。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12275](https://arxiv.org/abs/2607.12275) Flatness-Preserving Residual Learning for Real-Time Tight Quadrotor Formation Flight
- Locator: 5.2 Physical Experiments
- Evidence: 5.2节硬件结果原文给出分层百分比：ROM-FBL较Nominal-FBL平均降RMSE 24%与z_max 30%，Learned-FBL在ROM-FBL之上再降29%与43%，并称Learned-FBL整体最优（平均RMSE 5cm、z_max 10cm），与摘要宣称的'相对名义基线平均降低31%跟踪误差'同源。
- Quote: “The ROM-FBL controller outperformed the Nominal-FBL baseline by an average of 24% in RMSE and 30% in maximum vertical error (z max ). By leveraging the combined physics-informed and learned frame- work, the Learned-FBL controller achieved additional improvements of 29% in RMSE and 43% in z max relative to ROM-FBL.”
- Authors: pei-an-hsieh; fengjun-yang; nikolai-matni; et al.

### EA-TRAJACC-2026-0134

- Claim: 在双四旋翼堆叠编队仿真中，所提平坦性反馈线性化控制器（加载同一学习残差模型）的跟踪性能与Acados实现（编译为C代码、实时迭代）的NMPC相当，而平均求解时间降低20倍（0.99-1.3ms对26.2-27.6ms）。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12275](https://arxiv.org/abs/2607.12275) Flatness-Preserving Residual Learning for Real-Time Tight Quadrotor Formation Flight
- Locator: 5.1 Simulation Experiments, Table 4 / 5.2 Physical Experiments
- Evidence: 5.1节末尾原文：平坦性控制器跟踪性能与NMPC持平；NMPC虽用Acados编译C代码并采用实时迭代，所提JIT编译PyTorch控制器仍实现20×求解时间降低；表4给出z=0.3/0.5m下Ours 0.99/1.3ms对NMPC 27.6/26.2ms。
- Quote: “Our flatness-based controller achieves tracking performance on par with the NMPC. Moreover, while the NMPC was implemented in Acados (Verschueren et al., 2022), compiled into C code, and utilized real-time iteration, our JIT-compiled PyTorch-based controller still achieved a 20× reduction in solve time. This efficiency suggests broader applicability for computationally constrained hardware.”
- Authors: pei-an-hsieh; fengjun-yang; nikolai-matni; et al.

### EA-TRAJACC-2026-0135

- Claim: 硬件实验中的残差模型仅用28秒（6,720个数据点）飞行数据训练（2层4神经元神经网络叠加在下洗ROM上，采集时用未加学习残差的FBL控制器），即在双Crazyflie紧编队中实现有效的气动补偿跟踪。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12275](https://arxiv.org/abs/2607.12275) Flatness-Preserving Residual Learning for Real-Time Tight Quadrotor Formation Flight
- Locator: 5.2 Physical Experiments
- Evidence: 5.2节设置原文明确：硬件训练集D为28秒（6,720点），采自静顶与堆叠编队0.4m间距、0.4m速度、未增广FBL控制器的轨迹段；摘要进一步宣称30秒内训练数据即可实现稳定紧编队飞行。
- Quote: “The training dataset D spans 28 seconds (6,720 points) collected from trajectory segments where the quadrotors fly in static and stacked formations at a 0.4 m separation and 0.4 m/s velocity under an FBL controller unaugmented by learned residual dynamics.”
- Authors: pei-an-hsieh; fengjun-yang; nikolai-matni; et al.

### EA-TRAJACC-2026-0136

- Claim: 该文的核心机制是：将学习残差参数化为仅依赖编队各机位置与速度，使增广联合动力学保持微分平坦性，从而可用计算高效且能用标准线性技术整定的平坦性控制器替代计算昂贵的NMPC。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12275](https://arxiv.org/abs/2607.12275) Flatness-Preserving Residual Learning for Real-Time Tight Quadrotor Formation Flight
- Locator: 2 Problem Formulation
- Evidence: Sec. 2原文：为捕获并拒绝未建模气动效应同时最小化计算负担，将残差参数化为只依赖各机位置与速度；该参数化使增广的编队联合动力学保持微分平坦，从而平坦性控制器既享计算优势又可用标准线性技术整定。
- Quote: “To capture and reject unmodeled aerodynamic effects while minimizing the computational burden, we parameterize ξ to depend only on the vehicles’ positions and velocities. Crucially, this parameterization renders the joint aug- mented dynamics of the quadrotor team differentially flat. This enables the use of flatness-based controllers that not only enjoy computational benefits but are also tunable with standard linear techniques (Sec. 3).”
- Authors: pei-an-hsieh; fengjun-yang; nikolai-matni; et al.

### EA-TRAJACC-2026-0121

- Claim: 动作分块 VLA 的核心痛点机制是'多峰分叉'：相邻动作块由独立高斯噪声潜变量生成，可收敛到不相容的轨迹模态（如一块从一侧接近物体、下一块改从另一侧），在块边界产生突变不连续；这是跨块不一致而非块内问题，源于流匹配策略用不同噪声样本表达多峰动作分布的固有特性。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Abstract; Preliminaries
- Evidence: 摘要与 Preliminaries 的 Multimodal action distributions 段给出定义：contact-rich 任务动作分布多峰（引 Shafiullah et al. 2022），流匹配把不同初始噪声映射到不同模态；相邻块独立采样 z_n, z_{n+1}∼N(0,I)，即使观测相近，重叠区预测仍可分歧，产生意图冲突（Mode C 反向）与位置间隙（Mode B 偏移）两类边界 artifact（Figure 1a）。
- Quote: “Vision-Language-Action (VLA) policies that execute fixed- length action chunks can exhibit multimodal bifurcation: a cross-chunk inconsistency in which adjacent chunks gener- ated from independent Gaussian latents can converge to in- compatible trajectory modes, producing abrupt discontinu- ities at chunk boundaries.”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0122

- Claim: 痛点量化定位：在 LIBERO-10 + π_0.5 上，基线策略的边界 jerk（0.195）超过内部 jerk（0.094）的两倍，说明运动不规则性集中在块边界而非沿轨迹均匀分布——块边界 artifact 是可被指标分离量化的独立痛点，而非整体轨迹质量问题的副产品。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Introduction; Table 2
- Evidence: Introduction 与 Table 2 报告同一测量：基线 BJ 0.195、IJ 0.094、CD 0.172、AV_b 0.165，在执行后处理动作序列上按 Eq.9-13 计算（边界集 B={t\|t mod K=0}），10 任务 × 130 episodes 平均。
- Quote: “On LIBERO-10 with π 0.5 , the baseline boundary jerk is more than twice its interior jerk (0.195 vs. 0.094), indicating that motion irregularity is concentrated at chunk boundaries rather than uniformly distributed across the tra- jectory.”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0123

- Claim: 既有跨块一致性补救分布在一个成本-平滑度谱上且各有代价：RTC 用 ΠGDM 梯度条件 inpainting，一致性强但需在每个 ODE 步对策略网络反向传播，显著增加去噪延迟；BID 靠拒绝采样提高推理成本；Legato 需重训练动作模型（ACT-TE 对不相容模态取平均会产生无效中间动作，见同段前文）——共同缺口是缺少计算轻量、免训练的解析一致性机制。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Introduction; Related Work
- Evidence: Introduction 与 Related Work 的作者刻画：段落前句给出 ACT-TE 时序集成的平均化缺陷（'can create invalid intermediate actions when adjacent chunks choose incompatible modes''cannot select between incompatible modes'），本卡引文聚焦 RTC（反传+延迟）、BID（拒绝采样成本）与 Legato（重训练）三条路径。
- Quote: “RTC (Black, Galliker, and Levine 2025) treats continuation as conditional inpaint- ing and applies ΠGDM gradients inside the denoising ODE; this strongly improves consistency, but the required policy- network backpropagation at each ODE step substantially in- creases denoising latency. BID (Liu et al. 2025) searches for consistent continuations by rejection sampling, increas- ing inference cost, while Legato (Liu et al. 2026) learns continuation-aware dynamics during training and therefore requi”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0124

- Claim: SEAM 核心机制：利用同步分块执行的结构——机器人执行完前缀后，前一块的未执行尾部已可用作解析一致性参照；VLS 从该尾部导出时间相关目标，并在每个 Euler 步后施加闭式修正，不需对策略网络反向传播、不需重训练、不加辅助网络。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Abstract; SEAM Method, VLS (Eq.3-8, Table 1)
- Evidence: 摘要概述与方法节细节：对齐先验 a_al 由尾部 a_tail=c_n[K+1:H] 以末动作重复填充到 H（Eq.3，保守填充不外推、不设终点路点）；目标 r_{i+1}=(1−t_{i+1})·a_al[1:M]（Eq.4）；每步 Euler 候选后对引导窗口施加闭式负梯度 g=−2(x̃[1:M]−r_{i+1})（Eq.6-7），更新 x[1:M]=x̃[1:M]+λ(1−t_{i+1})g（Eq.8），未引导位置保留候选；λ(1−t) 调度早期弱、近动作流形强，避免过度约束早期去噪状态。
- Quote: “We propose SEAM (Smooth Execution of Action- chunked Motion), a training-free inference-time method for flow matching VLAs. SEAM exploits a simple synchronous- execution insight: after the robot consumes the executed pre- fix, the previous chunk’s unexecuted tail is already avail- able as an analytic consistency reference. Its core mecha- nism, Velocity-guided Loss Steering (VLS), derives a time- dependent target from this tail and applies a closed-form cor- rection after each Euler step without”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0125

- Claim: 主结果：LIBERO-10 + π_0.5 上，SEAM 把边界 jerk 从 0.195 降到 0.141（−27.7%）、内部 jerk 0.094→0.074（−21.3%）、块转换不连续 0.172→0.126（−26.7%）、边界 jerk 方差 0.165→0.094（−43.0%），同时任务成功率保持基线水平（95.7% vs 94.8%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Main Results, Table 2
- Evidence: Main Results 正文与 Table 2：π_0.5 基线 BJ/IJ/CD/AV_b=0.195/0.094/0.172/0.165、成功率 94.8%；+SEAM=0.141/0.074/0.126/0.094、95.7%。摘要用四舍五入口径（28%/27%）；成功率差异在 130 episodes/任务的噪声范围内，宜表述为'保持'而非'提升'。
- Quote: “SEAM reduces boundary jerk by 27.7% (0.195 → 0.141), interior jerk by 21.3% (0.094 → 0.074), chunk transition discontinuity by 26.7% (0.172 → 0.126), and AV b by 43.0% (0.165 → 0.094), while preserving baseline-level task suc- cess (95.7% vs. 94.8%).”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0127

- Claim: SEAM 去掉反向传播后成本近基线：每 10 步块查询去噪循环仅增加 3.8ms，总延迟保持 1.01× 基线（286.0 vs 282.2ms，每步额外仅 0.371ms 对照 RTC 的 6.236ms），同时降低边界 artifact 并保持可比任务成功率——零反传闭式修正在延迟敏感部署中成本可行。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Main Results, Table 2
- Evidence: Main Results 正文与 Table 2 计时列：SEAM 每步额外 0.371ms、每 10 步块 286.0ms、D-Cost 1.01×；RTC 每步额外 6.236ms、344.6ms、1.22×；计时协议为 RTX 3090 上缓存前缀去噪循环（N=10 Euler 步）单独测量。
- Quote: “In contrast, SEAM removes the backward pass, adds only 3.8 ms to the denois- ing loop per 10-step chunk, and keeps denoising-loop latency at 1.01× the baseline while reducing boundary artifacts and preserving comparable task success.”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0130

- Claim: 引导维度选择影响效果：仅引导位置维度（pos-only）比全维度更保守但平滑效果更差——λ=0.1、M=20 下 pos-only 为 BJ 0.162、CD 0.143、成功率 94.0%，全维度为 BJ 0.141、CD 0.126、成功率 95.7%；主结果因此采用有界窗口全维度设置。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Ablation Study, Table 4
- Evidence: Ablation Study 的维度对比（Table 4 下半区 pos 行 vs 上半区 all 行，λ 与 M 匹配扫描）：pos 行在全部 λ 上成功率与平滑均劣于匹配的 all 行（如 pos 0.2: 88.2%）。
- Quote: “Restricting guidance to position dimensions (“pos-only”) is more con- servative but less effective at smoothing than the matched all-dimension setting. At λ=0.1 and M =20, pos-only guid- ance yields BJ 0.162 and CD 0.143 with 94.0% success, whereas all-dimension guidance yields BJ 0.141 and CD 0.126 while preserving task success at 95.7%, supporting the bounded-window all-dimension setting”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0131

- Claim: 引导窗口 M 主要充当平滑度旋钮：测试的全部 M∈{2,...,20} 都相对基线降低 BJ 与 CD，任务成功率稳定在 94.7%–96.3%；更大窗口对 CD 降低更强，M=20 平滑最强（BJ 0.141、CD 0.126）——窗口长度在测试范围内不构成成功率风险，与 λ 的敏感性形成对照。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Ablation Study, Table 5 / results
- Evidence: Ablation Study 的 M 全扫描（Table 5，全维度、λ=0.1）：M=2..20 的 BJ 0.147–0.156、CD 0.134–0.146 均低于基线 0.195/0.172，成功率 94.7%（M=16）至 96.3%（M=6）；段落尾部（提取文本中被 Figure 4 说明隔断的后续句）把 M 总结为 smoothness knob。
- Quote: “Window length controls boundary smoothing. The Ta- ble 5 shows that every tested M reduces BJ and CD relative to the baseline, while task success remains broadly stable from 94.7% to 96.3%. Larger windows tend to reduce CD more strongly, and M =20 gives the strongest smoothing (BJ 0.141, CD 0.126).”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0132

- Claim: T1 失败模式定性对比揭示各方法失败机理：未引导基线会切换意图并在搬运中掉落物体；ACT-TE 过度平滑接触时序导致准确抓取延迟；RTC 的强连续性约束会把早期失败抓取锁定延续；SEAM 用弱重叠一致性而非硬连续性，在改善跨块一致性的同时保留纠正自由度。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Ablation Study, Qualitative T1 Failure Patterns (Figure 4) / results
- Evidence: Ablation Study 的定性分析（Figure 4 代表性 T1 rollout）：与 Table 3 中 T1 的最大方法间差距一致（基线 91.5 / SEAM 99.2 / RTC 90.8 / ACT-TE 58.5）；该段前句说明 T1 是逐任务差距最大任务。
- Quote: “The unguided baseline can switch intent and drop the object during transfer; ACT-TE can over- smooth contact timing and delay accurate grasping; RTC can preserve a failed early grasp through its stronger continuation constraint. SEAM avoids these failure modes by using weak overlap consistency rather than hard continuation, preserv- ing corrective freedom while improving cross-chunk consis- tency.”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0145

- Claim: 在4缆硅胶锥形软体臂真机上跟踪两个平面快速Lissajous式轨迹时，基于缩减Cosserat动力学的MHE-NMPC相比静态模型基控制器SMBC（因未考虑模型速度/加速度、快速圆弧运动尤其吃力）将末端位置RMSE从e_y 1.044→0.064 cm、e_z 1.216→0.083 cm（Y-Z平面）和e_x 0.310→0.062 cm、e_z 0.596→0.047 cm（X-Z平面），降幅80–94%，AVME同步大幅下降。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24029](https://arxiv.org/abs/2607.24029) Moving-Horizon Estimation and Nonlinear Model Predictive Control of Cable-Driven Soft Manipulators
- Locator: VIII-B2) Trajectory tracking control, Table I
- Evidence: VIII-B2原文：SMBC控制器下软臂只能近似跟随指定轨迹、快速圆周运动尤其困难，因其未考虑模型速度与加速度；NMPC精度更高（表I的AVME与RMSE更低）。表I逐轴数值：Y-Z平面SMBC e_y/e_z RMSE 1.044/1.216 cm→NMPC 0.064/0.083 cm；X-Z平面SMBC e_x/e_z RMSE 0.310/0.596 cm→NMPC 0.062/0.047 cm；AVME相应2.274→0.108、2.352→0.115、0.771→0.095、1.419→0.086 cm。
- Quote: “Fig. 18 reveals that under the SMBC controller, the soft ma- nipulator only approximately follows the designated trajecto- ries, particularly struggling with rapid circular movements due to a failure to consider the model’s velocity and acceleration. In contrast, the proposed NMPC controller achieves improved trajectory-tracking accuracy, as reflected by the lower AVME and RMSE values reported in Table I.”
- Authors: lingxiao-xun; haihong-li; gang-zheng

### EA-TRAJACC-2026-0146

- Claim: 在16缆软体臂仿真中，仅用末端位姿与绳长量测（应变/臂干位形不可直接量测、绳张力不可测）的MHE观测器在0.5 s内将应变估计误差收敛到±0.001以内；3.8 s绳驱动突然停止引起构型突变后，误差保持在±0.01内并在1 s内重新收敛到±0.001。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24029](https://arxiv.org/abs/2607.24029) Moving-Horizon Estimation and Nonlinear Model Predictive Control of Cable-Driven Soft Manipulators
- Locator: VII-A2) Analysis of simulation result, Fig. 7(b)
- Evidence: VII-A2原文：观测器收敛迅速，0.5 s内应变误差收敛到±0.001以内；3.8 s扰动发生时应变误差保持在±0.01内并在1 s内重新收敛到±0.001。量测假设（仅末端位姿+绳长可测、张力不可测）见VII-A1场景定义。
- Quote: “The results indicate that the observer has rapid convergence. Within 0.5s, the strain error converges to within ±0.001. When the disturbance occurs at 3.8s, the strain error remains within ±0.01 and reconverges to within ±0.001 within 1s.”
- Authors: lingxiao-xun; haihong-li; gang-zheng

### EA-TRAJACC-2026-0147

- Claim: 在4缆真机上，MHE-NMPC框架的平均总计算时间为51.4 ms（轨迹跟踪：MHE 18.6 ms+NMPC 32.8 ms，平均SQP迭代2.2/3.5次）和60.4 ms（marker跟踪：MHE 19.2 ms+NMPC 41.2 ms，迭代2.3/3.7次），均低于0.1 s采样周期，可在线实时运行末端跟踪。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24029](https://arxiv.org/abs/2607.24029) Moving-Horizon Estimation and Nonlinear Model Predictive Control of Cable-Driven Soft Manipulators
- Locator: VIII-B4) Computational Performance, Table II
- Evidence: VIII-B4原文：采样周期0.1 s，记录全部控制迭代的MHE与NMPC模块计算时间；表II汇总轨迹跟踪平均总耗时约51.4 ms、marker跟踪60.4 ms，均低于采样周期，框架可在物理原型上在线实时执行末端跟踪。表II同时给出各模块时域与平均SQP迭代数。
- Quote: “The sampling period was set to 0.1 s, and the computation time of the MHE and NMPC modules was recorded over all control iterations. As summarized in Table II, the average total computation time is approximately 51.4 ms for trajectory tracking and 60.4 ms for marker tracking. Both are below the sampling period, indicating that the proposed framework can be executed online for real-time end-effector tracking on the physical prototype.”
- Authors: lingxiao-xun; haihong-li; gang-zheng

### EA-TRAJACC-2026-0150

- Claim: 该框架的核心机制是用含松弛变量λ的softplus函数光滑近似绳张力-松弛互补关系，从而把绳长（而非张力）作为控制输入纳入可微优化，实现无需张力传感的绳长控制，并据此构建基于缩减Cosserat动力学的MHE状态估计与绳长/绳速约束下的NMPC任务空间控制。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24029](https://arxiv.org/abs/2607.24029) Moving-Horizon Estimation and Nonlinear Model Predictive Control of Cable-Driven Soft Manipulators
- Locator: VI-C. Smooth Cable Driven Constraint (Eqs. 44-47); preamble
- Evidence: 摘要原文：提出基于缩减Cosserat动力学的MHE与NMPC框架；发展平滑绳长驱动建模，通过近似绳张力与绳松弛之间的互补关系，实现无需直接张力传感的绳长控制。机制细节在VI-C：T=E(λ)、l−l_c=E(−λ)，softplus E(λ)=(1/c)log(1+e^{cλ})，c→∞时收敛到max(0,λ)保证互补约束，把非线性互补问题替换为等式约束G(x,l,λ)=l−l_c−E(−λ)=0并重定义最优控制问题。
- Quote: “In this paper, we propose a moving-horizon esti- mation (MHE) and nonlinear model predictive control (NMPC) framework for cable-driven soft manipulators based on reduced Cosserat dynamics. A smooth cable-length-driven modeling for- mulation is developed by approximating the complementarity relationship between cable tension and cable slackness, enabling cable-length control without direct tension sensing.”
- Authors: lingxiao-xun; haihong-li; gang-zheng

### EA-TRAJACC-2026-0152

- Claim: 在 π0.5 骨干上，仅作训练期辅助正则的 Hermite 变体（Reg）以零推理开销把平均成功率从 95.9% 提升到 98.7%（标准 LIBERO）、85.7%→90.9%（LIBERO-plus 分布偏移）、63.4%→90.0%（四个真机任务）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.01265](https://arxiv.org/abs/2608.01265) Hermite Curves as Trajectory Priors for Vision-Language-Action Models
- Locator: 1 INTRODUCTION
- Evidence: 引言与摘要给出同一组主结果数字：Reg 在三个评测域上一致超过共享 π 系列基线，且 Reg 保留基线动作头与采样流程，未引入运行时开销。
- Quote: “Against the shared π-series baseline, the strongest vari- ant HERMITE-VLA Reg improves the average success rate from 95.9% to 98.7% on standard LIBERO, from 85.7% to 90.9% under the distribution shifts of LIBERO-plus, and from 63.4% to 90.0% on four real-robot tasks.”
- Authors: qi-lv; jianming-xing; zhao-yang; et al.

### EA-TRAJACC-2026-0153

- Claim: 在真机 30 Hz、W=20、T=50 的闭环重规划设置下，Hermite 正则把重规划交接处的位移不连续中位数降到 π0.5 基线的 0.72×（Task 2）与 0.48×（Task 3）。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.01265](https://arxiv.org/abs/2608.01265) Hermite Curves as Trajectory Priors for Vision-Language-Action Models
- Locator: 4.5 Smoothness and Trajectory-Quality Analysis
- Evidence: 4.5 节 seam 分析直接给出相对中位数：Reg 相对 π0.5 基线把 handover 跳变降到 0.72×/0.48×；原文同时说明该比值因内部步同时被平滑而保守低估绝对收益。
- Quote: “Second, Hermite regularization sub- stantially mitigates this handover jump, with HERMITE- VLA Reg reducing the relative seam median to 0.72× on Task 2 and 0.48× on Task 3 compared to π 0.5 baseline.”
- Authors: qi-lv; jianming-xing; zhao-yang; et al.

### EA-TRAJACC-2026-0157

- Claim: 论文的核心机制结论：显式结构化轨迹先验最有效的作用方式是作为学习阶段的归纳偏置而非运行时约束——训练期 Reg 变体在三个评测域上均超过把先验作为部署输出的 CH，同时保持原始推理管线。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.01265](https://arxiv.org/abs/2608.01265) Hermite Curves as Trajectory Priors for Vision-Language-Action Models
- Locator: preamble (Abstract)
- Evidence: 摘要的 Trajectory analyses 句与正文 4.3（Reg 90.0% > CH 81.7% 真机；98.7% > 97.7% LIBERO）共同支撑该论断；Reg 不引入运行时延迟的属性使其区别于 primitive-as-policy 架构。
- Quote: “Across simulation benchmarks and real-robot platforms, Hermite Regularization achieves superior performance among these three variants, improving π 0.5 baseline success rates from 95.9% to 98.7% on LIBERO, 85.7% to 90.9% on LIBERO-plus, and 63.4% to 90.0% across four real-robot tasks without additional inference overhead. Trajectory analyses reveal that explicitly structuring trajectory priors serves most effectively as a learning inductive bias rather than a runtime constraint.”
- Authors: qi-lv; jianming-xing; zhao-yang; et al.

### EA-TRAJACC-2026-0140

- Claim: LIBERO（π0.5，单模型覆盖 ∆=1-9）上，Jetson-PI 四子集平均成功率较 VLASH 与 RTC 分别高 14.8 与 3.9 个百分点；随 ∆ 增大与错位加剧，VLASH/RTC 显著退化而 Jetson-PI 保持稳定高精度，∆=9 时优势扩大到 45.6 与 7.0 个百分点，且相对同步推理消除块间停顿而精度损失可忽略。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12659](https://arxiv.org/abs/2607.12659) Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference
- Locator: 5.1 Simulation Experiments, Table 3
- Evidence: Table 3 给出四子集×9 个 ∆ 的完整成功率矩阵：+Sched 平均 97.4/98.6/96.8/92.5 vs VLASH 74.4/86.1/84.2/81.3 与 RTC 92.6/96.6/94.1/86.4；正文总结平均优势 14.8/3.9 个百分点与 ∆=9 时的 45.6/7.0 个百分点，及相对 Sync（97.3/99.6/96.7/93.5）的 negligible loss。
- Quote: “Main Results. The simulation results are shown in Table 3. On average over four sub-datasets and different ∆, our method outperforms VLASH and RTC by 14.8% and 3.9%. Notably, as ∆ increases and the perception-execution misalignment problem becomes more severe, both VLASH and RTC exhibit significant performance degradation. In contrast, Jetson-PI maintains consistently high accuracy, as it adaptively provides future environment information for action prediction across varying ∆. For ∆ = 9, Jetson”
- Authors: zebin-yang; qi-wang; yunhe-wang; et al.

### EA-TRAJACC-2026-0141

- Claim: 机载实时化效果：在 Jetson Orin 上以 π0.5 为负载，Jetson-PI 经置信度调度（免每次调 VLM）、CUDA 图复用、GPU 常驻缓冲与流匹配展开，把端到端延迟从 1420.8 ms 降至 412.9 ms、反应时间从 1420.8 ms 降至 165.1 ms、控制频率从 0.70 Hz 提升到 6.06 Hz（较朴素 PyTorch 8.66×，较 vla.cpp 的 893.0 ms 提升 5.41×）；Thor 上从 2.18 Hz 提升到 7.59 Hz（3.48×）。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12659](https://arxiv.org/abs/2607.12659) Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference
- Locator: 5.2 Latency Evaluation, Table 4
- Evidence: Table 4 逐项叠加给出 Orin/Thor 上的延迟分解与频率：调度使反应时间 2.11×/1.87× 下降、图复用 2.96×（Orin）、缓冲+展开使动作专家 1.50×/1.59× 加速，总频率提升 8.66×/3.48×；正文另给 vla.cpp 对比 5.41×。
- Quote: “Overall, we achieve 8.66× and 3.48× improvements in control frequency on two devices, enhancing the robot’s reaction speed and task performance. Compared with vla.cpp, which has a latency of 893.0ms on the Orin platform [31], Jetson-PI achieves a 5.41× improvement in control frequency through scheduling and system opti- mizations.”
- Authors: zebin-yang; qi-wang; yunhe-wang; et al.

### EA-TRAJACC-2026-0142

- Claim: 错位校正的核心机制与代价条件：未来校正模块不预测未来图像、不逐层修正 KV 缓存，而是以 t 时刻压缩后的 VLM 末层输出与已提交动作为输入，预测 t+∆ 时刻的压缩 VLM 末层状态，供动作专家直接从未来时间步起预测动作；模块仅 40M 参数（约占整个 VLA 的 1%），引入的额外延迟可忽略——错位校正的可行性依赖'在压缩潜空间以轻量模块外插'这一设计约束。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12659](https://arxiv.org/abs/2607.12659) Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference
- Locator: 4.1 Foresight-Aligned Asynchronous Correction
- Evidence: 4.1 节明确三项设计要求（动作条件预测、轻量、适配可变 ∆）并给出实现：压缩末层状态+已提交动作→未来压缩状态；参数量 40M、占比 1%、成本可忽略；训练中随机采样 ∆ 使单模型适配不同设备延迟。
- Quote: “To avoid intro- ducing excessive latency, we do not directly predict future images or correct the KV cache at each layer. Inspired by [48], we take the compressed final-layer output of the VLM at t and the committed actions, then pass them through future correction module that predicts the compressed VLM final- layer output at t + ∆. Then pass this lightweight correction item to action expert, enabling action expert to directly predict actions starting from t+∆. The parameter size of future corr”
- Authors: zebin-yang; qi-wang; yunhe-wang; et al.

### EA-TRAJACC-2026-0143

- Claim: 真机（X2-W 机器人，XR-1 模型 @ Jetson Orin，15 Hz 执行，折衣任务含抓取/折叠/放置三子任务各 10 次）：朴素异步在受限算力下任务能力崩溃（6/10、0/10、5/10），Jetson-PI 达 10/10、8/10、9/10，相对 RTX 4090 部署基线（10/10、7/10、10/10）几乎无精度损失——机载实时化不再以牺牲复杂任务能力为代价。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.12659](https://arxiv.org/abs/2607.12659) Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference
- Locator: 5.3 Real-world Experiments, Figure 7 / 5.1 Simulation Experiments
- Evidence: 5.3 节在 Jetson Orin 上部署 XR-1 模型执行折衣任务，Figure 7 给出三种部署的每子任务 10 次成功率；正文总结 Jetson-PI 几乎无相对 4090 的精度损失且显著优于朴素异步。
- Quote: “Method Picking Folding Placing RTX 4090 (Baseline) 10/10 7/10 10/10 Jetson Orin (Naive Async) 6/10 0/10 5/10 Jetson-PI (Ours) 10/10 8/10 9/10 Figure 7: Real-world results on 3 subtasks (pick- ing, folding, placing) on different deployments.”
- Authors: zebin-yang; qi-wang; yunhe-wang; et al.

### EA-TRAJACC-2026-0158

- Claim: 在该 10 Hz 双臂世界动作模型平台上，六策略统一比较的总结论：prefix 条件式训练方法取得最佳整体精度-平滑权衡；直接动作加权平滑但精度受限；推理期速度引导无法约束 delay region。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.01880](https://arxiv.org/abs/2608.01880) World Action Models in Real Time: An Empirical Study of Smooth Execution via Asynchronous Deployment
- Locator: 1 Introduction
- Evidence: 引言第三条贡献即此总结论，与 5.3 在线结果（train 三任务 96/70/96）和 5.2 离线结果（train 与 simple 的 delay region 近零误差、infer 显著更高）相互印证。
- Quote: “We find that prefix-conditioned methods achieve the best overall precision–smoothness balance, while direct action weighting provides a smooth but precision-limited baseline, and velocity-guided inference fails to constrain the delay region on our platform.”
- Authors: motubrain-team

### EA-TRAJACC-2026-0159

- Claim: 在动态任务（传送带移动目标）上，sync 与纯 async 都只得 20 分：sync 因推理窗口内完全无响应无法跟踪目标，async 因无混合的硬切换产生全场最高 jerk（8.427 m/s³）而无法完成抓取；async+blend 也仅 40 分。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.01880](https://arxiv.org/abs/2608.01880) World Action Models in Real Time: An Empirical Study of Smooth Execution via Asynchronous Deployment
- Locator: 5.3 Online Robot Evaluation
- Evidence: 5.3 节动态任务段落原文给出 sync/async 各 20 分的原因机制与 async 最高 jerk 的定量描述，async+blend 40 分说明对齐+最简插值只是最低前提。
- Quote: “sync achieves a completion score of only 20, failing to track the moving target because the robot is completely unresponsive during the inference window. async also scores 20 despite being responsive—the hard chunk-switch without any blending produces the highest jerk among all methods, severe enough to prevent successful picking.”
- Authors: motubrain-team

### EA-TRAJACC-2026-0160

- Claim: 在精细操作任务（块入槽）上，去噪中加权混合（simple）的激进插值使放置精度退化到 27.5 分（sync 72.5、train 70），证实混合引入精度-平滑权衡；train 比 sync 更快（12.13 s vs 19.4 s）且 jerk 更低。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.01880](https://arxiv.org/abs/2608.01880) World Action Models in Real Time: An Empirical Study of Smooth Execution via Asynchronous Deployment
- Locator: 5.3 Online Robot Evaluation
- Evidence: 5.3 节精细任务段落原文明确把 27.5 分归因于精度-平滑权衡，并给出 train 的速度与 jerk 优势数字，直接支撑该主张。
- Quote: “simple’s aggressive action interpolation degrades placement precision (score 27.5), confirming that blending during denoising introduces a precision–smoothness trade-off on contact-critical tasks. sync (score 72.5) and train (score 70) both achieve high completion scores; train additionally completes the task faster (12.13 s vs. 19.4 s for sync) and with lower jerk”
- Authors: motubrain-team

### EA-TRAJACC-2026-0164

- Claim: 在平面3-DOF三绳下肢康复机器人仿真的代表组合案例（1-5s同时+10%参数不确定、5-9s带限白噪声力矩外扰）中，有界残差DDPG使末端RMS笛卡尔误差从0.0221419 m降至0.0128462 m（约42%），IAE降63.5%、ISE降66.8%、峰值误差降19.4%——持续误差的压缩远大于瞬态峰值。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26739](https://arxiv.org/abs/2608.26739) Residual Deep Reinforcement Learning-Based Computed Torque Control for a Cable-Driven Lower-Limb Rehabilitation Robot under Disturbances and Parametric Uncertainties
- Locator: 6.2. Representative combined uncertainty/disturbance case, Table 11
- Evidence: 6.2节原文：代表后处理数据集上RMS笛卡尔误差从0.0221419 m降至0.0128462 m（41.9826%，约42%），peak/IAE/ISE分别降19.4%/63.5%/66.8%；表11同数值并列最小绳需求0→3.41445 N、关节限位样本61→0。
- Quote: “Table 11 is generated from the representative post-processing dataset. RMS Cartesian error decreases from 0.0221419 m to 0.0128462 m, a 41.9826% reduction, reported as approximately 42%. Peak error decreases by 19.4%, IAE by 63.5%, and ISE by 66.8%.”
- Authors: mohammad-hossein-fakouri; ali-keymasi-khalaji

### EA-TRAJACC-2026-0165

- Claim: 四情景配对比较（独立case-matrix数据集）中，残差DDPG的RMS笛卡尔误差降幅为：名义21.1%、仅不确定39.4%、仅外扰27.7%、组合41.6%；不确定情景增益最大，支持残差策略主要补偿名义模型失配的机制解释。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26739](https://arxiv.org/abs/2608.26739) Residual Deep Reinforcement Learning-Based Computed Torque Control for a Cable-Driven Lower-Limb Rehabilitation Robot under Disturbances and Parametric Uncertainties
- Locator: 6.3. Four-case comparison and dataset provenance, Table 12
- Evidence: 6.3节原文：残差DDDPG在名义/仅不确定/仅外扰/组合四情景分别降RMS误差21.1%/39.4%/27.7%/41.6%；作者解释不确定情景的更大增益支持'actor补偿名义模型失配'，且名义情景的非零改善可源于指令滤波、数值微分、离散化等未被理想CTC抵消的效应。表12给出绝对值（如组合0.022032→0.012863 m）。
- Quote: “Table 12 compares the four primary scenarios using an independently generated case-matrix file. Residual DDPG reduces RMS error by 21.1% in the nominal case, 39.4% with uncertainty only, 27.7% with disturbance only, and 41.6% in the combined case. The larger gains in the uncertainty-containing cases support the interpretation that the actor compensates for nominal-model mismatch.”
- Authors: mohammad-hossein-fakouri; ali-keymasi-khalaji

### EA-TRAJACC-2026-0166

- Claim: 组合情景经十个扰动种子重复：CTC均值RMS误差0.022945±0.000533 m，残差DDPG为0.012916±0.000082 m（均值降幅43.69±1.17%），且残差支路标准差约小6.5倍——改善跨扰动实现稳定并降低对扰动抽样的敏感性。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.26739](https://arxiv.org/abs/2608.26739) Residual Deep Reinforcement Learning-Based Computed Torque Control for a Cable-Driven Lower-Limb Rehabilitation Robot under Disturbances and Parametric Uncertainties
- Locator: 6.4. Ten-seed robustness and interval-wise behavior
- Evidence: 6.4节原文：扰动启用情景以十种子重复，组合案例CTC均值RMS 0.022945±0.000533 m、残差0.012916±0.000082 m、均值降幅43.69±1.17%；残差控制器更小的标准差表明跨测试扰动实现的敏感性降低；区间分析另给出不确定区间-81.84%、外扰区间-68.45%的最大增益。
- Quote: “Disturbance-enabled cases were repeated with ten seeds. For the combined case, mean RMS error is 0.022945 ± 0.000533 m for CTC and 0.012916±0.000082 m for CTC + residual DDPG, giving a mean reduction of 43.69±1.17%.”
- Authors: mohammad-hossein-fakouri; ali-keymasi-khalaji

### EA-TRAJACC-2026-0010

- Claim: 真机倾倒任务（0.5 kg钢球容器、t=18 s起负载非线性时变）中改进是轴依赖的：PD-med在y向RMSE更低（7.30e-3 vs 9.41e-3 m）且φy相当，但NT-STSM在负载最敏感的z向RMSE显著更低（2.74e-3 vs 7.23e-3 m，约2.6倍改善），负载变化时PD性能退化而NT-STSM维持跟踪，同时平均控制力矩低32%（0.883 vs 1.30 Nm）、TV_τ低约2.6倍（7.98e3 vs 2.07e4）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2504.13056](https://arxiv.org/abs/2504.13056) Adaptive Task Space Nonsingular Terminal Super-Twisting Sliding Mode Control of a 7-DOF Robotic Manipulator
- Locator: C. Experimental Results, Table V
- Evidence: IV-C原文明确承认PD在y向与ε_z姿态上误差更低，而NT-STSM在负载最敏感的z轴显著改善，t=18 s负载变化时PD退化而NT-STSM维持跟踪，控制输入显著更低；表V给出轴级数值（y：7.30e-3 vs 9.41e-3 m；z：7.23e-3 vs 2.74e-3 m；φy：2.74e-2 vs 2.79e-2 rad；τ_avg：1.30 vs 0.883 Nm；TV_τ：2.07e4 vs 7.98e3）。
- Quote: “While the PD controller achieves lower tracking error in the y direction and ϵ z orientation, the NT-STSM controller demonstrates significantly improved tracking along the z-axis, which is most sensitive to the payload. This is clear at t = 18 s, where the payload change degrades the PD controller’s performance while the NT-STSM controller maintains more accurate tracking.”
- Authors: lucas-wan; sean-smith; yajun-pan; et al.

### EA-TRAJACC-2026-0033

- Claim: 遮挡恢复能力高度依赖运动速度：10 mm/s低速下系统对5秒遮挡取得100%遮挡成功率（OSR）且重捕获时间可忽略（仅IR传感器被遮挡时3D 1σ误差0.79 mm、相机与IR同时被挡时1.11 mm），而50 mm/s高速下遮挡后无法恢复稳定跟踪、OSR降为0——高速遮挡失效是该方案族在视线频繁受遮挡的工业检测场景的硬边界。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.05391](https://arxiv.org/abs/2509.05391) Evaluating Magic Leap 2 Controller Tracking for Sensor Tool Guidance in AR-Based Industrial Inspections
- Locator: IV-B4) Robustness, Reliability, Stability / X Y Z 3D X Y Z 3D X Y Z 3D 3D
- Evidence: IV-B4原文：系统对遮挡的鲁棒性高度速度依赖——10 mm/s下100% OSR、5秒遮挡后重捕获时间可忽略、精度仅轻微退化（IR-only 1σ 0.79 mm、全遮挡1.11 mm）；50 mm/s下无法恢复稳定跟踪、OSR为0。讨论节补充：高速下维持清晰视线对防止跟踪失效至关重要。提取文本中IV-B4小节正文物理上位于表IV/Fig.6-7内容之后的表体节（节标题'X Y Z 3D...'），故定位器为复合形式。
- Quote: “The system’s robust- ness to occlusion was found to be highly velocity-dependent. At the lower speed of 10 mm/s, the system demonstrated a 100% Occlusion Success Rate (OSR), re-acquiring the track after a 5-second occlusion with a negligible Re-acquisition Time (ROT). During these 10 mm/s tests, a slight degradation in precision was noted. The tracking remained highly precise when only the IR sensors were occluded (3D 1-sigma error of 0.79 mm), with a more pronounced, yet still robust, decrease”
- Authors: christian-masuhr; julian-koch; thorsten-schppstuhl

### EA-TRAJACC-2026-0040

- Claim: 组件级速度不等于系统级敏捷：把感知前端换成计算上更快的 DCL-Net（自身仅 14 ms、系统 73 Hz），动态跟踪实验立即失稳无法收敛——因为其架构未与策略协同设计、无法提供策略所需的稳定状态估计；高频方案的适用条件是感知输出的稳定性而非单纯吞吐。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.00983](https://arxiv.org/abs/2511.00983) Breaking the Latency Barrier: Synergistic Perception and Control for High-Frequency 3D Ultrasound Servoing
- Locator: IV. EXPERIMENTS / D. Ablation Studies and Comparative Analysis, Table IV
- Evidence: IV-D 消融显示 DCL-Net + Flow 组合延迟 13.7 ms（73 Hz）反而高于本框架，但动态跟踪完全无法收敛（误差 6.508 mm）；作者把失败归因于感知架构未协同设计以提供稳定状态估计，II-A 亦给出'组件级速度不转化为系统级敏捷'的一般性论断。该节原文两段逐字：'Second, and more critically, the system with the DCL-Net front-end failed to converge in dynamic tracking experiment. While the DCL-Net module itself is computationally fast'（提取文本在此插入Fig.8图注与Table III后接）'(14 ms), its architecture is not co-designed to provide the stable state estimates required by the policy, leading to immediate instability.'；Table IV 行：'DCL-Net + Flow ≈ 13.7 73 Failed to Converge 6.508'。
- Quote: “(14 ms), its architecture is not co-designed to provide the stable state estimates required by the policy, leading to immediate instability.”
- Authors: yizhao-qian; yujie-zhu; jiayuan-luo; et al.

### EA-TRAJACC-2026-0046

- Claim: 实验中引入在线 Kalman 滤波后，Q 滤波器带宽可提高到 70 Hz 以提升稳态性能；为覆盖多参考命令，验证流程在初始任务后又重复了 29 条附加参考命令（每条引入新的持续不确定性）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.11850](https://arxiv.org/abs/2511.11850) Neural Network-Augmented Iterative Learning Control for Friction Compensation of Motion Control Systems with Varying Disturbances
- Locator: V. EXPERIMENTAL TESTS AND RESULTS
- Evidence: V 节报告 Kalman 滤波使 Q 滤波器带宽提升至 70 Hz 并改善稳态性能，同时说明多命令验证流程重复了 29 条附加参考命令。
- Quote: “Despite simplified model assumptions, such as constant force and structural rigidity, ILC effectively mitigates uncertainties. Using a Kalman filter allowed increasing the Q-filter bandwidth to 70 Hz, enhancing steady-state performance. The process was repeated for 29 additional reference commands, each introducing a new persistent uncertainty.”
- Authors: ali-mashhadireza; ali-sadighi

### EA-TRAJACC-2026-0047

- Claim: 稳定性条件：NN 输出有界是保持系统单调 trial-to-trial 收敛的前提（在误差动态与 Q/L 滤波器约束的收敛条件下成立）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.11850](https://arxiv.org/abs/2511.11850) Neural Network-Augmented Iterative Learning Control for Friction Compensation of Motion Control Systems with Varying Disturbances
- Locator: D. Stability Analysis
- Evidence: II.D 节推导误差动态与 trial-to-trial 收敛的充要条件后，明确陈述有界的 NN 输出保证系统保持单调收敛。
- Quote: “The stability of neural network-based ILC relies on the boundedness of the neural network output. Error dynamics can be expressed as: E j+1 = (R(z) − D)(1 − Q(z)) + Q(z)(1 − GL(z))E j (z) (9) and the necessary and sufficient condition for trial-to-trial con- vergence is: E ∞ (z) − E i+1 (z) E ∞ (z) − E i (z) = Q(z)(1 − LG(z)) (10) ensuring convergence as long as: sup \|z\|=1 \|1 − LG(z)\| < sup \|z\|=1 1 Q(z) (11) Thus, bounded neural network outputs guarantee that the monotonic trial-to-trial converg”
- Authors: ali-mashhadireza; ali-sadighi

### EA-TRAJACC-2026-0016

- Claim: 在G1定位重复性场景中，该方法并不内在降低样本量：200次试验的样本数稳定在598-601（仅比700样本的ISO 9283改编少约100），作者明示样本效率收益并非方法固有属性——位移误差对初始位置近乎均匀分布，任何重要性分布选择都无法显著加速收敛。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2505.08216](https://arxiv.org/abs/2505.08216) Rethink Repeatable Measures of Robot Performance With Statistical Query
- Locator: IV.A. Manipulation positioning tests
- Evidence: IV.A节在报告98%可重复率后明确声明'the proposed method does not inherently make the testing process more efficient in terms of sample reduction'，并归因于位移误差在初始位置空间近乎均匀分布、q选择无法加速收敛；效率收益依赖方差可缩减的问题结构（如NADE的稀疏风险事件）。
- Quote: “the number of samples collected across the 200 trials was not fixed, but consistently fell within the limited range of 598 to 601—nearly 100 fewer samples per trial than adopted by the ISO 9283 adaptation. It is important to note, however, that the proposed method does not inherently make the testing process more efficient in terms of sample reduction.”
- Authors: bowen-weng; linda-capito; guillermo-a-castillo; et al.

### EA-TRAJACC-2026-0024

- Claim: 绝对精度水平与适用条件：最优权重标定后平均指尖误差约10mm，与常超10-20mm的无标记视觉系统相当或更好；先前研究报道10-15mm指尖误差内不会感知性损失控制保真度——该精度水平对遥操作任务可行，但处于可容忍范围的下沿。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2507.23592](https://arxiv.org/abs/2507.23592) Human-Exoskeleton Kinematic Calibration to Improve Hand Tracking for Dexterous Teleoperation
- Locator: V. DISCUSSION
- Evidence: V. DISCUSSION把本方法约10mm的平均指尖误差与文献中无标记视觉系统（常超10-20mm）对比，并援引先前研究'10-15mm内不损失控制保真度'的容忍度作为遥操作可行性依据——这为标定收益的绝对水平提供了外部参照，同时划出精度边界。
- Quote: “In terms of performance, the proposed method achieves a mean absolute fingertip error of approximately 10 mm, comparable to or better than markerless vision-based systems that often exceed 10–20 mm [24]. Prior studies have reported tolerable fingertip errors up to 10-15 mm without perceptible loss of control fidelity [11], [25], supporting the feasibility of the proposed framework for teleoperation tasks.”
- Authors: haiyun-zhang; stefano-dalla-gasperina; saad-n-yousaf; et al.

### EA-TRAJACC-2026-0080

- Claim: 输出反馈实现的传感要求仅为两类边界测量——连杆基座应变与关节角——观测器据此重构控制器所需的未测分布状态，实验在实物 2DSFMR 平台上完成。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.17477](https://arxiv.org/abs/2605.17477) Rapid Vibration Suppression and Trajectory Tracking of a Serial Manipulator with Multi-Flexible Links
- Locator: V. CONCLUSION
- Evidence: 结论节明确陈述输出反馈通过设计观测器，仅从基座应变与关节角的边界测量重构未测状态，并在物理 2DSFMR 平台上完成验证。
- Quote: “This is subsequently extended to an output-feedback approach by designing an observer that reconstructs the unmeasured states from only boundary measurements of the base strain E bi (t) and the joint angle θ i (t). Finally, the experimental validation is conducted on a physical 2DSFMR platform.”
- Authors: chengyi-wang; yilong-huang; ji-wang

### EA-TRAJACC-2026-0093

- Claim: 相位剖面消融（全 50 任务）显示平滑是必要成分：平滑在关节与笛卡尔两个空间都提升成功率（笛卡尔 62.2→64.5、关节 60.4→64.2，均相对固定 H=25 基线 57.8），且平滑后两空间表现相当（差 0.3 点内）——PACE 捕捉的是跨运动学表示共享的相位结构，而非依赖特定运动空间；原始未平滑剖面因虚假局部谷导致过于频繁的重规划而损失成功率。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: 4.3 Ablation Analysis, Table 2 left
- Evidence: 4.3 节 Table 2 左对比关节/笛卡尔 × 原始/平滑四种剖面构造：平滑两空间分别 +6.7/+6.4，原始仅 +4.4/+2.6 且平均执行时域更短（11.3/16.7 vs 19.5/24.3），说明平滑去除了引发过频重规划的噪声谷；默认采用平滑关节空间剖面（免正向运动学计算）。
- Quote: “Table 2 left shows that smoothing improves success in both spaces and increases the selected execution horizon. This sug- gests that smoothing removes noisy valleys that would otherwise cause overly frequent replanning. After smoothing, Cartesian and joint-space profiles perform comparably, indicating that PACE captures a phase structure shared across kinematic repre- sentations rather than relying on a specific motion space.”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

### EA-TRAJACC-2026-0100

- Claim: 多变量回归相对单变量回归获得更优参数估计性质的代价是必须在线计算（4x4）矩阵逆。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.03533](https://arxiv.org/abs/2606.03533) Recursive Learning of Feedforward and Compliance Compensation Parameters for Precision Motion Systems
- Locator: 4.2 Multivariate regression
- Evidence: 4.2 节原文明确陈述多变量回归带来更优参数估计性质，代价是需在线计算矩阵逆，这是作者陈述的设计权衡。
- Quote: “By considering the linear combination of all regressors Φ simultaneously, parameter coupling is implicitly taken into account. This results in superior parameter estimation properties, at the cost of having to compute a matrix inverse online.”
- Authors: m-wind; j-pierssens; r-beerens; et al.

### EA-TRAJACC-2026-0105

- Claim: 适用条件（规划频率维度）：方法在全部测试重规划频率下保持稳定且不绑定特定控制器频率；更高的重规划频率降低位置与旋转误差，因为更短的执行区间缓解帧失配与误差累积——异步失配的代价随规划-控制频率比增大而增大，且该效应不依赖特定教师骨干（OmniH2O 与 SONIC 趋势一致）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.25706](https://arxiv.org/abs/2606.25706) Learning Asynchronous Upper-body Task-space Trajectory Tracking Policy for Humanoid Robots
- Locator: VI-B. Effect of Asynchronous Sparse Trajectory Tracking, Fig. 5(b)
- Evidence: VI-B 重规划频率扫描（Fig. 5b）在两种教师骨干上重复，均显示误差随重规划频率升高而下降；正文将机理归因于更短执行区间缓解帧失配与误差累积。
- Quote: “Higher re-planning frequencies reduce position and rotation errors because shorter execution intervals alleviate frame mismatch and error accumulation. The same trend appears with both OmniH2O- and SONIC-based [11] teachers, sug- gesting that this frequency effect is not specific to a particular teacher backbone.”
- Authors: yumeng-liu; dongqi-wang; jiyu-yu; et al.

### EA-TRAJACC-2026-0106

- Claim: 结构不完整的量化后果与 MPC 补全条件：仅用稀疏 3 点参考做 OOD 后训练时，稀疏目标对高维全身动作空间欠约束，策略出现关节限位超限（安全裕度为负）且异步区间漂移更大；MPC 补全的基座+上半身稠密约束使异步跟踪误差降低并把关节限位裕度变为正值——稀疏任务空间参考的方案必须补全全身约束才能安全后训练。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.25706](https://arxiv.org/abs/2606.25706) Learning Asynchronous Upper-body Task-space Trajectory Tracking Policy for Humanoid Robots
- Locator: VI-D. OOD Post-Training with MPC Completion, Fig. 4
- Evidence: VI-D 的 Fig. 4(c) 显示 ASYNC-3PT（无 MPC 补全）后训练后关节限位裕度为负，Fig. 4(b) 显示其区间旋转漂移显著大于 ASYNC-CA；正文把根因归为稀疏 3 点目标欠约束高维动作空间。
- Quote: “Moreover, Fig. 4(c) shows that ASYNC-3PT has a negative joint-limit margin, indicating unsafe joint-limit violations. Without MPC-completed motion guidance, the sparse 3- point objective under-constrains the high-dimensional whole- body action space, making post-training prone to unsafe joint configurations. In contrast, MPC-completed guidance provides denser base and upper-body constraints, leading to lower asynchronous tracking errors and a positive joint-limit margin.”
- Authors: yumeng-liu; dongqi-wang; jiyu-yu; et al.

### EA-TRAJACC-2026-0118

- Claim: 平滑度分析（nut-assembly-v3 与 plate-slide-back-v3，H=50、d=10 的代表性 rollout）：ACNet 的 jerk 轨迹在延迟区间与块替换事件处保持更平坦的分布，Naïve Async 表现出更强的转换诱发抖动——但证据形态仅为两任务的定性曲线，无跨任务聚合数值或统计检验。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: V-E. Trajectory Smoothness Analysis
- Evidence: V-E 节用 Eq. 17 定义的平移 jerk 分析两个任务的代表性 rollout，结论为 ACNet 在延迟区间与块替换事件处 jerk 更平坦、跨块延续更平滑，与 Table II 成功率增益一致。
- Quote: “To examine motion quality beyond success rate, represen- tative rollouts from nut-assembly-v3 and plate-slide-back-v3 with H = 50 and d = 10 are analyzed. The jerk traces in Fig. 4 show that ACNet maintains a flatter profile around delayed intervals and chunk replacement events. In both tasks, Naïve Async exhibits stronger transition-induced jitter, whereas ACNet produces smoother cross-chunk continua- tion, consistent with the success gains in Table II.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0126

- Claim: 跨方法权衡：RTC 平滑更强（边界 jerk −54% 至 0.090、块不连续 −48% 至 0.089、成功率 95.1%、AV_b 与 SEAM 相同 0.094）但 ΠGDM 每步自动微分反传使每块去噪延迟 282.2→344.6ms（1.22×）；ACT-TE 平滑最激进（BJ 0.031、−84%、AV_b 0.006）但每步查询下成功率掉至 82.7%。方法选择取决于延迟预算与平滑需求的权衡，SEAM 定位近基线成本而非最强平滑。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Main Results, Table 2; Figure 3
- Evidence: Main Results 正文与 Table 2/Figure 3 三方对比；ACT-TE 的 82.7% 部分归因于 every-step 查询下的过平滑接触时序（T1 定性分析 Figure 4：'ACT-TE can over- smooth contact timing and delay accurate grasping'）。
- Quote: “RTC reaches stronger boundary jerk reduction (−54%, to 0.090) and chunk discontinuity re- duction (−48%, to 0.089) with 95.1% success and the same AV b as SEAM (0.094), but its ΠGDM guidance requires one automatic-differentiation backward pass per ODE step and increases per-chunk denoising latency from 282.2 ms to 344.6 ms (1.22×). ACT-TE achieves the most aggressive smoothing (BJ 0.031, −84%, AV b 0.006) under its every-step query setting, but drops to 82.7% success.”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0129

- Claim: 引导强度 λ 存在可靠性-平滑度权衡：λ=0.1 是最佳平衡（成功率 95.7%、BJ 0.141、CD 0.126），增大强度只边际改善部分 jerk 指标却快速侵蚀任务成功率（λ=0.15→92.8%、λ=0.2→89.5%），支持用弱闭式修正而非激进地把去噪轨迹压向前一块。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Ablation Study, Table 4
- Evidence: Ablation Study 的 λ 扫描（固定 M=20，全维度/仅位置两设置）：λ=0.05 时 94.8%/BJ 0.162/CD 0.145；λ=0.15/0.2 的 92.8%/89.5% 见 Table 4 行（all 0.15 20 92.8；all 0.20 20 89.5）与表后句（'92.8% at λ=0.15 and 89.5% at λ=0.2. This supports using a weak closed-form correction rather than forcing the denois- ing trajectory toward the previous chunk too aggressively.'）。
- Quote: “We first sweep the guidance strength λ at fixed M =20 for both all-dimension and position-only guidance, with the results shown in Table 4. In the all-dimension rows, increasing λ generally strengthens smoothing but quickly erodes task reliability. λ=0.05 reaches 94.8% success with moderate smoothing, while the main λ=0.1 setting gives the best balance: 95.7% success with BJ 0.141 and CD 0.126.”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0148

- Claim: 16缆仿真轨迹跟踪中，预测时域仅0.01 s时软臂在部分点位偏离目标轨迹、末端段逐渐卷曲并采取不合理位姿（短时域使优化'短视'、陷入当前时刻局部最优）；时域扩展到0.06 s后卷曲消失、跟踪误差显著降低（图11误差幅度约从±2降至±0.02，单位rad或cm）——预测时域长度是NMPC轨迹跟踪精度的关键适用条件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.24029](https://arxiv.org/abs/2607.24029) Moving-Horizon Estimation and Nonlinear Model Predictive Control of Cable-Driven Soft Manipulators
- Locator: VII-C3) Influence of the duration of prediction horizon, Figs. 10-11
- Evidence: VII-C3原文：预测时域0.01秒时软臂在部分点偏离目标轨迹；短预测时域使其无法预判未来轨迹变化、无法调整当前位姿去适应未来目标轨迹，因而采取不合理位姿试图跟随目标位置。后文进一步说明0.06 s时域下该问题解决（可在整个预测窗内规划、平滑调整、远端卷曲不再出现），图11显示扩展时域显著降低跟踪误差。±2与±0.02读自图11(a)/(b)纵轴刻度。
- Quote: “When the prediction horizon is 0.01 seconds, the simulation results show that the soft manipulator deviates from the target trajectory at certain points. The short prediction horizon prevents the soft manip- ulator from anticipating future trajectory changes, making it unable to adjust its current pose to accommodate the future target trajectory. Consequently, the manipulator adopts an unreasonable pose in its attempt to follow the target position.”
- Authors: lingxiao-xun; haihong-li; gang-zheng

### EA-TRAJACC-2026-0149

- Claim: 在实时随机目标跟踪场景中，目标位置快速随机变化会使控制输入短时剧变、降低控制平滑性并使数值优化落入不良局部极值；同时步进电机转速/输出扭矩有限，过度快速收绳会产生显著摩擦、增大系统误差并降低鲁棒性——因此作者在控制优化中引入绳速约束（\|l̇\|≤2πr_d·w_max，r_d=1 cm、w_max=5 rps）以增强鲁棒性并满足硬件要求。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.24029](https://arxiv.org/abs/2607.24029) Moving-Horizon Estimation and Nonlinear Model Predictive Control of Cable-Driven Soft Manipulators
- Locator: VIII-B3) Real time marker tracking
- Evidence: VIII-B3原文：目标点位置随机快速变化使控制输入可能短时剧烈变化，该现象会降低控制平滑性并使数值优化解落入不良局部极值；此外系统硬件有性能限制（如步进电机的转速与输出扭矩）；而且过度收绳速度会产生显著摩擦、增大系统误差并降低鲁棒性；因此为增强控制鲁棒性并满足硬件要求，在控制优化问题中引入绳速约束。约束式与r_d、w_max数值见其后公式段。
- Quote: “This phenomenon can reduce the smoothness of control and cause the numerical optimization solution to fall into undesirable local extrema. Additionally, the system hardware has performance limits, such as the rotational speed and output torque of the stepper motors. Moreover, excessive cable contraction speed can generate substantial friction, increasing system error and reducing robustness.”
- Authors: lingxiao-xun; haihong-li; gang-zheng

### EA-TRAJACC-2026-0155

- Claim: 在 LIBERO-plus 外观类扰动（Light/Background/Noise）下，显式 scaffold 变体 CH 的成功率低于 π0.5 基线（总平均 85.0% vs 85.7%）；作者将此解释为：当预训练动作头已有效建模密集动作时，Hermite 结构更适合作为补充性监督。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.01265](https://arxiv.org/abs/2608.01265) Hermite Curves as Trajectory Priors for Vision-Language-Action Models
- Locator: 4.3 Main Results
- Evidence: 4.3.1 节 LIBERO-plus 分析与 Table 3 显示 CH 在几何类扰动领先但在三类外观扰动上低于基线，作者给出机制性解释，构成条件性结论而非单纯失败案例。
- Quote: “85.0% average SR, leading on geometric perturbations but falling below the baseline on Light, Background, and Noise. The comparison suggests that, when the pretrained action predictor already models dense actions effectively, Hermite structure is more beneficial as complementary supervision.”
- Authors: qi-lv; jianming-xing; zhao-yang; et al.

### EA-TRAJACC-2026-0011

- Claim: 在与所提控制器相同的自适应增益律和tanh平滑处理下，传统NTSM控制器在7-DOF任务空间复合运动中仍严重抖振导致失稳（被从对比中省略），STSM控制器在14 s起显著抖振至17 s才恢复稳定（RMSE_p=7.04e-3 m、TV_τ=1.45e5 Nm）——抖振与失稳是传统滑模方案用于高DOF真机复杂运动的结构性痛点。
- Stance: `limit` | Confidence: `direct`
- Paper: [2504.13056](https://arxiv.org/abs/2504.13056) Adaptive Task Space Nonsingular Terminal Super-Twisting Sliding Mode Control of a 7-DOF Robotic Manipulator
- Locator: B. Simulation Results, Table III
- Evidence: III-B原文：尽管采用了抖振消减技术（tanh替换sign），NTSM仍严重抖振致失稳而被省略；STSM在14 s（旋转扰动段）开始显著抖振直到17 s稳定；表III中STSM的RMSE_p=7.04e-3 m、RMSE_ξ=1.19e-1 rad、TV_τ=1.45e5 Nm均为差档；作者补充：调低κ1/κ2可减抖但会牺牲跟踪精度。
- Quote: “Despite chattering reduction techniques, the NTSM con- troller exhibited severe chattering, leading to instability, and is omitted. The STSM controller performed well until 14 s, when it began to chatter significantly until stabilizing at 17 s.”
- Authors: lucas-wan; sean-smith; yajun-pan; et al.

### EA-TRAJACC-2026-0012

- Claim: 作者自述局限：所提控制器需要手动整定多个参数，需要专门的调试操作时间，是该方法落地的成本痛点；作者计划以基于学习或优化的方法自动化参数选择作为未来工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2504.13056](https://arxiv.org/abs/2504.13056) Adaptive Task Space Nonsingular Terminal Super-Twisting Sliding Mode Control of a 7-DOF Robotic Manipulator
- Locator: V. CONCLUSION
- Evidence: V. CONCLUSION原文明确承认：尽管有诸多优势，一个局限是需要手动整定多个参数、需要专门操作时间；未来工作将聚焦用学习或优化方法自动化参数选择，并扩展到多机械臂与力反馈协同。
- Quote: “Despite its advantages, one limitation of the proposed con- troller is that it requires manual tuning of multiple parameters, which requires dedicated operation time. Future work will fo- cus on automating parameter selection through learning-based or optimization-based approaches.”
- Authors: lucas-wan; sean-smith; yajun-pan; et al.

### EA-TRAJACC-2026-0031

- Claim: 在45°侧向视角条件（S3）下的静态位姿测试中，ML2控制器在SP05、SP06两个位姿出现平均高达347 mm的粗大位置误差，且该误差与极佳的重复性（0.3-0.4 mm）并存——系统自信且一致地报告严重错误位置的系统失效，而非随机噪声；表III显示第二个侧向位置S4下SP05/SP06同样出现346.5-347.5 mm级误差。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05391](https://arxiv.org/abs/2509.05391) Evaluating Magic Leap 2 Controller Tracking for Sensor Tool Guidance in AR-Based Industrial Inspections
- Locator: IV-A. Static Tracking Accuracy, Table III
- Evidence: IV-A原文：S3侧向视角下SP05/SP06出现高达347 mm的平均偏差且与0.3-0.4 mm的极佳重复性耦合，作者判定为系统性失效（系统自信且一致地报告严重错误位置）；表III逐格核对S3(25 mm/s)下SP05=346.9/347.4/0.3、SP06=346.8/347.6/0.4，S4(25 mm/s)下SP05=347.5/348.1/0.3、SP06=346.5/347.5/0.4（带*剔除出均值）；讨论节假设根因为控制器SLAM环境特征不足导致稳定但错误的位姿。
- Quote: “Despite the generally robust performance, a critical failure mode observed under the angled viewing condition S3 signif- icantly diminished its reliability. While most poses remained accurate, SP05 and SP06 exhibited gross positional errors, with a mean deviation of up to 347 mm. The most significant finding is that this major error was coupled with excellent repeatability (0.3-0.4 mm) (see Table III). This indicates a sys- tematic failure where the system confidently and consistently reports a”
- Authors: christian-masuhr; julian-koch; thorsten-schppstuhl

### EA-TRAJACC-2026-0032

- Claim: 在32次动态轨迹试验中，末端跟踪的平均3D RMS误差强依赖运动模式：直线轨迹最低（2.70 mm），光栅扫描轨迹最高（16.27 mm，约为直线的6倍）——光栅路径与直线在空间上紧邻执行，说明这是特定于光栅运动模式的系统性路径偏离，而非位置环境或随机精度问题（光栅轨迹平均3D 1σ仅0.846 mm，高RMS由少数高幅离群驱动）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05391](https://arxiv.org/abs/2509.05391) Evaluating Magic Leap 2 Controller Tracking for Sensor Tool Guidance in AR-Based Industrial Inspections
- Locator: IV-B1) Accuracy Metrics: Absolute Accuracy (RMS Error), Table IV
- Evidence: IV-B1原文：直线平均3D RMS误差最低（2.70 mm）、光栅最高（16.27 mm），且光栅与直线紧邻执行仍大幅系统偏离、路径本身精度很高；表IV交叉核对Average行：line 3D RMS=2.696（1σ=0.555）、raster=16.268（1σ=0.846）、circle=3.513（1σ=1.384）、square=3.126（1σ=0.999）mm——raster的RMS-1σ差全类别最大。
- Quote: “Line trajectories consistently per- formed best, showing the lowest average 3D RMS error (2.70 mm). In contrast, raster trajectories were the least accurate, with a significantly higher average RMS error of 16.27 mm. This is particularly noteworthy as the raster paths were executed in close proximity to the line trajectories, which suggests a substantial systematic deviation from the intended path that is specific to the raster motion pattern, despite the high precision of the path itself.”
- Authors: christian-masuhr; julian-koch; thorsten-schppstuhl

### EA-TRAJACC-2026-0035

- Claim: 对氢泄漏检测这一安全关键任务，控制器在最佳正面视角下误差持续低于预设5 mm端到端要求，但该精度未能在全部配置中维持（特定非正面视角出现显著位置离群）；作者结论：ML2控制器不能被认为对该安全关键任务可靠，实际部署需要能检测这种'高精度失效模式'（高重复性+粗大误差）的失效安全机制，而这超越简单离群值过滤。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05391](https://arxiv.org/abs/2509.05391) Evaluating Magic Leap 2 Controller Tracking for Sensor Tool Guidance in AR-Based Industrial Inspections
- Locator: V-C. Implications for the Industrial Use Case
- Evidence: V-C原文：实验环境与参数按泄漏检测场景设计、结果可有意义地迁移到预期应用；正面视角下误差远低于5 mm要求，但并非所有配置都能维持、特定非正面视角出现显著位置离群；基于这些结果，ML2控制器不能被认为对该安全关键任务可靠；实际实现需要能检测这种特定高精度失效模式的失效安全机制，超越简单离群过滤。
- Quote: “For the hydrogen leak inspection task, the controller’s performance under optimal, frontal viewing conditions con- sistently yielded errors well below the predefined 5 mm re- quirement. However, this level of accuracy was not maintained across all configurations, with significant positional outliers occurring under specific non-frontal viewing angles. Based on these results, the ML2 controller cannot be considered reliable for this safety-critical task. A practical implementation would require a”
- Authors: christian-masuhr; julian-koch; thorsten-schppstuhl

### EA-TRAJACC-2026-0036

- Claim: 评测方法学痛点：同一慢速光栅轨迹以10 Hz采样测得3D 1σ误差1.34 mm、以50 Hz采样仅0.44 mm（约3倍差）——异步数据流（ML2约30 Hz vs OptiTrack 50 Hz）的时间不确定性在低采样率下更显著、可能是测量伪影，50 Hz数据才更准确代表系统真实精度；时间戳直接对齐（无插值）在50 mm/s下的最大理论位置误差为0.25 mm，落在OptiTrack约0.2 mm精度范围内、影响可忽略。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05391](https://arxiv.org/abs/2509.05391) Evaluating Magic Leap 2 Controller Tracking for Sensor Tool Guidance in AR-Based Industrial Inspections
- Locator: V-D. Limitations
- Evidence: V-D原文：ML2（约30 Hz）与OptiTrack（50 Hz）异步数据流用直接时间戳相关对齐（无插值），50 mm/s下最大理论位置误差0.25 mm、在OptiTrack精度范围内影响可忽略；但该时间不确定性在低采样率下更显著、可能是测量伪影——同一慢速轨迹10 Hz测得1σ=1.34 mm vs 50 Hz的0.44 mm，50 Hz数据更准确代表真实精度；表IV交叉核对T17（raster F2,10 mm/s,10 Hz）1σ=1.340、T21（同轨迹50 Hz）0.440。
- Quote: “However, the effect of this temporal uncertainty appears to be more pronounced at lower sampling rates, potentially indicating a measurement artifact. This was evident when an identical slow trajectory yielded a 3D 1-sigma error of 1.34 mm when measured at 10 Hz, versus 0.44 mm at 50 Hz (see Table IV). This discrepancy indicates that the 50 Hz data more accurately represents the system’s true precision.”
- Authors: christian-masuhr; julian-koch; thorsten-schppstuhl

### EA-TRAJACC-2026-0005

- Claim: 作者自述的根本局限：方法受平移与旋转变换固有耦合约束，必须假设工具与目标已旋转预对齐；该假设虽在当前实现中操作上必要，但在众多真实场景中难以实现，可能限制方法的实际适用性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2503.04862](https://arxiv.org/abs/2503.04862) High-Precision Transformer-Based Visual Servoing for Humanoid Robots in Aligning Tiny Objects
- Locator: IV. CONCLUSIONS
- Evidence: IV. CONCLUSIONS原文明确：平移-旋转耦合使方法必须假设预对齐存在；作者同时指出旋转误差在RGB图像中从某些方向难以辨识，3D点云可能更适合，未来工作将发展平移+旋转双域对准策略。
- Quote: “However, the method is fundamentally constrained by the inherent coupling between translational and rotational transformations, necessitating the assumption of pre-existing rotational alignment between tool and target. This assump- tion, though operationally necessary in our current imple- mentation, may be difficult to achieve in numerous real- world scenarios, potentially limiting the method’s practical applicability.”
- Authors: jialong-xue; wei-gao; yu-wang; et al.

### EA-TRAJACC-2026-0006

- Claim: 纯RGB双相机视觉伺服存在沿视线方向的深度歧义失败模式：当螺丝刀尖位于头部相机与螺槽中心连线上时，头部与躯干相机都近似看到尖端居中于螺头，导致网络误判已对准；MPH近距离高增益通过放大此类近距误差驱动网络辨识细微位置差异从而缓解该问题。
- Stance: `limit` | Confidence: `direct`
- Paper: [2503.04862](https://arxiv.org/abs/2503.04862) High-Precision Transformer-Based Visual Servoing for Humanoid Robots in Aligning Tiny Objects
- Locator: B. Results and Discussion
- Evidence: III-B节失败案例分析原文（图7）：DET-SPH实验中的典型失败是尖端处于头部相机与螺槽中心连线上，双相机都误判居中对准；DET-MPH架构在近距离的更高增益放大该近距误差，产生显著训练损失驱动网络辨识图像空间中的细微位置差异。
- Quote: “Fig. 7(a) illustrates a typical failure case observed in exper- iments with DET-SPH , where the screwdriver tip is on the line connecting the head camera and the screw head center. The head and torso cameras both perceive that the screw- driver tip has approximately centered over the screw head, causing the network to falsely conclude proper alignment.”
- Authors: jialong-xue; wei-gao; yu-wang; et al.

### EA-TRAJACC-2026-0037

- Claim: 论文论证（引用 Diffusion Policy 系工作）：Diffusion Policy 依赖迭代去噪推理造成根本性延迟瓶颈，控制频率被限制在 10-23 Hz，远低于超声探头 60 Hz 更新流，无法实时补偿生理运动——迭代式生成策略的推理延迟是高频末端跟踪的首要痛点。
- Stance: `limit` | Confidence: `citation-supported`
- Paper: [2511.00983](https://arxiv.org/abs/2511.00983) Breaking the Latency Barrier: Synergistic Perception and Control for High-Frequency 3D Ultrasound Servoing
- Locator: B. Learning-based Control: The Quest for High-Frequency Policies and Robust Generalization
- Evidence: 相关工作在综述 Diffusion Policy 主导的模仿学习方法后明确指出其迭代去噪推理的延迟瓶颈与 10-23 Hz 频率上限，并强调任何低于 60 Hz 帧率的控制环无法响应每一帧新信息。
- Quote: “The state-of-the-art is dominated by Diffusion Policies [15], but their reliance on an iterative denoising process for inference imposes a fundamental latency bottle- neck. This limits their control frequency to 10-23 Hz [15], [16], a rate far below the 60 Hz update stream from the US probe, making real-time compensation of physiological motion impossible.”
- Authors: yizhao-qian; yujie-zhu; jiayuan-luo; et al.

### EA-TRAJACC-2026-0041

- Claim: 方案的适用边界：系统对未建模的 Z 轴旋转扰动仅在 15° 偏置内保持稳定（15° 时误差 8.170±0.179 mm、NCC 0.937），20° 出现控制失稳（9.916 mm），25° 跟踪失败（NCC 0.696）；失效根因是感知网络的归纳偏置——把旋转剪切误读为平移运动。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.00983](https://arxiv.org/abs/2511.00983) Breaking the Latency Barrier: Synergistic Perception and Control for High-Frequency 3D Ultrasound Servoing
- Locator: IV. EXPERIMENTS / E. Robustness to Out-of-Plane Rotational Disturbances, Table V
- Evidence: IV-E 对螺旋跟踪施加 0-25° 旋转偏置扫描，Table V 给出各档误差/NCC/状态；作者将失效模式明确归因于感知前端训练时把视觉剪切解释为平移的归纳偏置，属可预期的感知模糊。
- Quote: “The framework remains stable up to a 15° offset, maintaining high image similarity and minimal positional error. Beyond this threshold, performance degrades rapidly, with control instability at 20° and tracking failure at 25°. This failure mode stems directly from our perception front-end’s inductive bias: the network is trained to interpret visual shearing as translational motion.”
- Authors: yizhao-qian; yujie-zhu; jiayuan-luo; et al.

### EA-TRAJACC-2026-0044

- Claim: 在含 LuGre 摩擦的仿真中，参考频率在第 10 次迭代后由 0.5 Hz 改为 0.6 Hz 时，MSE 因摩擦模式改变而升高，先前收敛的 ILC 努力变为次优，需要额外迭代才能适应新参考。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.11850](https://arxiv.org/abs/2511.11850) Neural Network-Augmented Iterative Learning Control for Friction Compensation of Motion Control Systems with Varying Disturbances
- Locator: IV. SIMULATION / A. LuGre Friction Model
- Evidence: IV 节仿真第二场景明确报告参考频率切换导致 MSE 上升，归因于摩擦模式变化，且收敛的 ILC 努力变为次优、需要额外迭代重新适应。提取文本中该段物理上位于 IV 节内 'A. LuGre Friction Model' 小节块（表II/Fig.5之后），故定位器为复合形式。
- Quote: “In a second scenario, the reference frequency is changed from 0.5 Hz to 0.6 Hz after 10 iterations. As shown in Fig. 6, this causes an increase in mean square error (MSE) due to the change in friction patterns. The previously converged ILC effort becomes suboptimal, requiring additional iterations to adapt to the new reference.”
- Authors: ali-mashhadireza; ali-sadighi

### EA-TRAJACC-2026-0029

- Claim: 非鲁棒策略跨任务迁移显著退化：将在E-(4)（大间隙配合）训练的FVFC-MTRL策略直接用于E-(1)（大过盈配合）时，平均成功率降至82%、平均控制步数增加25%。
- Stance: `limit` | Confidence: `direct`
- Paper: [2508.12296](https://arxiv.org/abs/2508.12296) A Robust and Compliant Robotic Assembly Control Strategy for Batch Precision Assembly Task
- Locator: 4.3. Compliance and robustness verification
- Evidence: 原文4.3节以FVFC-MTRL的跨子任务迁移为例说明非鲁棒策略缺乏跨任务泛化能力：E-(4)策略用于E-(1)时成功率降至82%、步数增加25%。
- Quote: “Non-robust policies typically lack cross-task generalization capability, exhibiting significant performance degradation when directly transferred to different task configurations. For example, when applying the FVFC-MTRL policy trained in E-(4) to subtask E-(1), the average success rate decreases to 82% and the average control steps increase by 25%.”
- Authors: bin-wang; jiwen-zhang; song-wang; et al.

### EA-TRAJACC-2026-0048

- Claim: VLA 分块策略的实时同步控制实际不可达：同步推理要求推理延迟小于控制周期（δ<Δt 即 d=0），而 50Hz 控制（Δt=20ms）下 π_0 仅动作生成就需 76ms（RTX 4090），真机 15Hz 下端到端延迟约 122-140ms（有效延迟 d=2 或 3）——同步推理因此产生块间急动转换与执行时间延长，这是异步推理范式的动机，也是末端轨迹不连续的系统性根源之一。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: 3 Preliminaries, synchronous inference paragraph
- Evidence: 3 节论证同步推理的实时条件 δ<Δt 不可达并给出 π_0 在 RTX 4090 上 76ms 的动作生成延迟；5.2 节给出真机 15Hz 下端到端延迟 122-140ms（VLA 76-80ms + 网络 34-40ms + 处理 10-20ms），对应有效延迟 d=2 或 3。
- Quote: “For synchronous inference to achieve real-time execution, the condition δ < ∆t (i.e., d = 0) must hold, which is practically unattainable. For example, with a 50 Hz control frequency (∆t = 20 ms) and π 0 (Black et al., 2024) as the VLA model, action generation alone requires 76 ms on an NVIDIA RTX 4090 GPU, with additional overhead from preprocessing, disk I/O, and network transmission further increasing latency.”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0049

- Claim: 论文识别出异步推理下被忽视的第二失败模式'块内不一致'：给定当前感知 o_t，最优执行块应对应 A_t，但在推理延迟 d 与执行时域 h 下，实际执行的前 d 个动作继承自上一块 A_{t-h}（基于旧观测 o_{t-h}），这些前缀动作对当前状态次优，在块内造成感知-动作失配——与块间不连续（跨块潜在模式切换跳变）共同构成异步执行的两大性能退化源。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: 3 Preliminaries, intra-chunk inconsistency definition
- Evidence: 3 节用 P=3, h=2, d=1 的示例形式化两个挑战：块间不连续源于连续块可能来自不同潜在专家模式；块内不一致源于延迟期间执行的前缀动作以 o_{t-h} 为条件，对基于 o_t 的当前状态次优。
- Quote: “Given perception o t , the optimal executed chunk should fully correspond to A t . However, under inference delay d with execution horizon h, the first d actions executed are instead taken from A t−h . This results in intra-chunk inconsistency, where these inherited prefix actions become suboptimal for the current state, because they were conditioned on o t−h rather than o t , creating a perception–action mismatch within the chunk.”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0056

- Claim: 作者自述两条局限：(1) 需预先指定最大推理延迟以保证优化覆盖全部可能延迟，实际执行延迟超过该界时可能发生意外失败；(2) 掩码微调可能需要可观的微调数据，在数据采集昂贵或受限的场景下限制实用性（尽管附录 E.3 显示 30 条轨迹已接近 200 条的性能）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.20130](https://arxiv.org/abs/2601.20130) Real-Time Robot Execution with Masked Action Chunking
- Locator: G Limitations
- Evidence: 附录 G 明确列出两条局限：最大推理延迟需预先设定（超界可能意外失败）与微调数据需求可能可观。附录 E.3 的低数据实验（Table 4：30 条轨迹 0.900/0.905/0.810 vs 200 条 0.910/0.936/0.820）部分缓解第二条，但正文与表格的演示数口径（10 vs 30）存在不一致。
- Quote: “Our method is not without limitations. First, it requires specifying a maximum inference delay in advance to ensure that the optimization process covers the full range of possible delays. If the actual delay during execution exceeds this bound, unexpected failure may occur. Second, the approach may demand a substantial amount of finetuning data for masked finetuning, which could limit practicality in settings where data collection is costly or constrained.”
- Authors: haoxuan-wang; gengyu-zhang; yan-yan; et al.

### EA-TRAJACC-2026-0063

- Claim: 作者自述四项局限：(1)世界系跟踪精度受LiDAR定位精度上界约束；(2)评测轨迹尺度相对较小；(3)双臂全局跟踪依赖目标可行性且高层实验仅单臂；(4)接触富操作（如抓取）未探索，未来工作将融入视觉感知与力控。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.06341](https://arxiv.org/abs/2602.06341) HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation
- Locator: VII. CONCLUSION AND LIMITATIONS
- Evidence: VII结论节原文列明四项局限并给出未来方向（视觉感知+力控的灵巧接触感知操作）；结合正文，定位链路为头部Livox Mid-360+IMU的Fast-LIO2（10Hz），真机定量仅圆/方平滑轨迹×10次重复，高层世界系实验仅右手单臂轨迹。
- Quote: “The current framework has limitations: (1) world-frame tracking precision is bounded by LiDAR-based localization accuracy; (2) evaluated trajectories are relatively small in scale; (3) bimanual global tracking depends on target feasibility, and high-level experiments involve only single-arm tracking; (4) contact-rich manipulation (e.g., grasping) remains unexplored.”
- Authors: zhanxiang-cao; liyun-yan; yang-zhang; et al.

### EA-TRAJACC-2026-0023

- Claim: 标定并未消除全部偏差：残留的关节角（结论处约10°）与指尖误差因模型失配、传感噪声与未建模柔性而持续存在，且在指尖处最明显（小关节偏差沿运动学链累积放大）；对更高精度灵巧任务需补充指尖级或任务级标定。
- Stance: `limit` | Confidence: `direct`
- Paper: [2507.23592](https://arxiv.org/abs/2507.23592) Human-Exoskeleton Kinematic Calibration to Improve Hand Tracking for Dexterous Teleoperation
- Locator: V. DISCUSSION / VI. CONCLUSION
- Evidence: V. DISCUSSION明确说明残留误差的三个来源（模型失配、传感噪声、未建模柔性）及其在指尖的累积放大效应，并建议指尖级/任务级标定作为补充；VI. CONCLUSION进一步量化'约10°关节角残差仍在'，同时声称仍可支持精密跟踪——残差与精密任务需求的张力构成本方案族的未解痛点。
- Quote: “Despite the promising results, the calibrated model does not remove all discrepancies: residual joint-angle and fin- gertip errors persist due to model mismatch, sensing noise, 8 IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED FEBRUARY, 2026 and unmodeled compliance, and are most noticeable at the fingertips, where small joint deviations accumulate along the kinematic chain. A complementary fingertip-based or task- level calibration can therefore be used to further refine finge”
- Authors: haiyun-zhang; stefano-dalla-gasperina; saad-n-yousaf; et al.

### EA-TRAJACC-2026-0064

- Claim: 在 LIBERO 仿真基准上，用稀疏二值奖励在线 RL 微调的 OpenVLA 生成的末端轨迹平均 jerk 为 0.402 m/s³，显著高于 SFT 版本的 0.374 m/s³，即 RL 探索以轨迹抖动为代价（探索-稳定性悖论的定量实证）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.13925](https://arxiv.org/abs/2603.13925) SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization
- Locator: 2.2 Quantitative Analysis: Jerk-based Metric
- Evidence: 论文 2.2 节在 LIBERO 任务套件上大规模计算末端轨迹平均 jerk，Table 1 显示 RL 微调版本四套件平均 0.402 高于 SFT 的 0.374，且正文明确将其归因于稀疏奖励在线 RL 的策略搜索随机性。
- Quote: “As shown in Table1, the Reinforcement- fine-tuned model produces trajectories with a significantly higher average jerk (0.402m/s³) than the Supervised-fine- tuned model (0.374m/s³). This provides strong physical evi- dence that existing online RL fine-tuning methods based on sparse rewards, while improving generalization, indeed intro- duce additional trajectory jitter and degrade motion smooth- ness.”
- Authors: jiashun-li; xiaoyu-shi; hong-xie; et al.

### EA-TRAJACC-2026-0074

- Claim: 痛点定位：动作分块虽然缓解命令饥饿，但把系统变成 chunk 播放期间的部分开环控制器；chunk 中途发生未建模扰动或接触事件时，本地缓存轨迹可能不再与真实状态演化物理一致，盲目执行过时轨迹穿过未预期碰撞会导致危险的力累积与任务失败。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.19418](https://arxiv.org/abs/2603.19418) Speculative Policy Orchestration: A Latency-Resilient Framework for Cloud-Robotic Manipulation
- Locator: III-B Cloud-Induced Delay and Open-Loop Vulnerability
- Evidence: III-B 形式化延迟反馈 a_t=π(s_{t−δ}) 后指出：分块执行（transmit action chunks for local buffered execution）在 chunk 播放期间构成部分开环控制器，引用 MT-ACT 的大静态块（H=40）性能退化作为佐证。
- Quote: “While chunking alle- viates command starvation, it transforms the system into a partially open-loop controller during chunk playback [38]. If unmodeled disturbances or contact events occur mid-chunk, the locally buffered trajectory may no longer be physically consistent with the true state evolution. Blindly executing this stale trajectory through unanticipated collisions can lead to dangerous force accumulations and task failure.”
- Authors: chanh-nguyen; shutong-jin; florian-t-pokorny; et al.

### EA-TRAJACC-2026-0075

- Claim: 真机部署局限：仿真中用于干净隔离空闲时间的严格零速保持（a_t=0）在物理机器人上会造成严重机械应力与接触中的 stick-slip 伪影，真实部署必须把该算法反射映射为 Tier-3 硬件安全停止（如带阻抗控制的 jerk 受限减速）以安全耗散动能；且全部实验仅在 RLBench 仿真完成，真机传感器噪声与 sim-to-real 差距明确留作未来工作。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.19418](https://arxiv.org/abs/2603.19418) Speculative Policy Orchestration: A Latency-Resilient Framework for Cloud-Robotic Manipulation
- Locator: V-B. Results and Discussion, 3) Deployment Guidelines, Remark on Hardware Deployment / VI. CONCLUSIONS
- Evidence: V-B.3 的 Remark on Hardware Deployment 明确区分仿真反射与真机安全语义；VI 节未来工作第一条即为物理平台部署与传感器噪声/sim-to-real 鲁棒性评估。
- Quote: “However, commanding instantaneous zero velocity on physical robots causes severe mechanical stress and stick-slip artifacts during contact. In real-world deployments, this algorithmic reflex must map to a Tier-3 hardware safe stop (e.g., jerk-limited deceleration with impedance control) to safely dissipate kinetic energy.”
- Authors: chanh-nguyen; shutong-jin; florian-t-pokorny; et al.

### EA-TRAJACC-2026-0082

- Claim: 论文论证显式动作分块存在三大结构性缺陷：(1) 开环块执行对执行级平滑保证有限，允许块内快速方差并在重规划边界诱导尖锐不连续；(2) 策略输出从 R^d 膨胀到 R^hd，随时域 h 增大加剧优化复杂度并损害探索效率与训练稳定；(3) 与标准逐步交互接口（actor-critic 骨干、经验回放、逐点安全覆盖）架构性不兼容。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.19592](https://arxiv.org/abs/2605.19592) Implicit Action Chunking for Smooth Continuous Control
- Locator: 1. Introduction
- Evidence: 引言在综述 Q-Chunking/Decoupled Q-Chunking 等显式分块 RL 工作后，明确归纳三个问题并指出开环执行是块内方差与边界不连续的来源（引用 Yang et al. 2025 支持边界不连续论断）。
- Quote: “This approach introduces three problems. (1) It offers limited guarantees on execution- level smoothness, the open-loop nature of chunk execution allows for rapid intra-chunk variance and induces sharp dis- continuities at replanning boundaries (Yang et al., 2025). (2) It exacerbates optimization complexity by expanding the policy output from R d to R hd , which can hamper ex- ploration efficiency and training stability as the horizon h grows.”
- Authors: bosun-liang; shuo-pei; zirui-chen; et al.

### EA-TRAJACC-2026-0088

- Claim: 对动作分块策略，固定执行时域 H 的选择对成功率影响强非单调且高度任务依赖：在 RoboTwin2.0 的 Click bell 任务上，成功率在 H≈6 附近达峰、H≈25 附近下降近 40 个百分点、H≈35 再现第二峰——任何单一固定时域都可能落入某些任务的性能陡降区，是不合格的部署默认值。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: 1 Introduction, Figure 1 left panel
- Evidence: 论文 1 节在三个 RoboTwin2.0 任务上把 H 从 1 扫到 50，观察到成功率对 H 强非单调、最优时域高度任务依赖；Click bell 呈峰-谷-第二峰形态，谷底比峰值低近 40 个百分点，据此论证执行时域必须在部署时在线决定而非预先固定。
- Quote: “The left panel of Fig. 1 shows that such an empirical choice is unreliable. Sweeping H from 1 to 50 on three RoboTwin2.0 tasks, we observe that the success rate is strongly non-monotonic in H and that the preferred horizon is highly task-dependent. On Click bell, for instance, the success rate peaks near H ≈ 6, drops by nearly 40 points around H ≈ 25, and rebounds to a second peak near H ≈ 35.”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

### EA-TRAJACC-2026-0094

- Claim: PACE 的能力边界：它只改善预测块的执行方式，不改变基策略的动作分布——当基策略无法生成完成所需子任务的动作时（如笔盒未被充分打开即插入笔的失败案例），更好的重规划时机无法挽回回合；PACE 应被定位为执行层而非修复策略能力缺失的机制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: 7 Limitations; 5.3 Failure Case
- Evidence: 7 节 Limitations 与 5.3 节失败案例一致陈述：PACE 缩短了插入阶段的时域（7/6 步）多次刷新块，但刷新的块仍由同一基策略生成，笔盒仍只部分打开，任务失败——重规划时机不能恢复策略分布中缺失的任务完成行为。
- Quote: “PACE improves how predicted action chunks are executed, but it does not change the action distribution of the under- lying policy. If the base policy fails to generate actions that complete a required subtask, better replanning timing alone cannot recover the rollout.”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

### EA-TRAJACC-2026-0095

- Claim: PACE 的信号假设构成其适用条件：它假设有用的重规划边界反映在预测块的运动学结构中（接触/抓取/释放/对齐等相位常见）；关键决策点不表现为低速谷的任务、或运动剖面噪声大的策略只能提供较弱信号；此外全部实验仅覆盖 π_0.5 单一 VLA 策略族，跨策略族通用性未验证。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: 7 Limitations
- Evidence: 7 节 Limitations 第二、三段：假设段声明边界信号来自运动学结构并列举弱信号情形；通用性段声明实验仅用 π_0.5，未来需在其他 VLA 架构、动作 tokenized 策略与世界-动作模型上验证。两者共同界定 PACE 的适用域。
- Quote: “PACE assumes that useful replanning boundaries are re- flected in the kinematic structure of the predicted chunk, as is common in manipulation phases involving contact, grasping, release, or alignment. However, tasks whose key decision points are not expressed as low-speed valleys, or policies with noisy motion profiles, may provide weaker signals.”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

### EA-TRAJACC-2026-0098

- Claim: 在实验中，在线柔顺补偿学习的额外收益有限：总体性能提升主要归因于速度前馈，原因是事先调定的 y 位置相关名义柔顺补偿已接近真实柔顺，限制了在线自适应可获得的额外改善。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.03533](https://arxiv.org/abs/2606.03533) Recursive Learning of Feedforward and Compliance Compensation Parameters for Precision Motion Systems
- Locator: 5.2 Experimental results
- Evidence: 作者在 5.2 节明确解释实验收益主要来自速度前馈，并归因于名义柔顺补偿已接近真实值，从而限制了在线自适应的额外改善空间。
- Quote: “In the experimental results D 1 , the over- all performance gain is primarily attributed to velocity feedforward. This can be explained by the fact that the a priori tuned y-position-dependent nominal compliance compensation ˆγ 0 (y) is already close to the true compliance, thereby limiting the additional improvement achievable through online adaptation.”
- Authors: m-wind; j-pierssens; r-beerens; et al.

### EA-TRAJACC-2026-0102

- Claim: 在 1 Hz 参考更新、50 Hz 控制的人形任务空间跟踪设置下，把同步稀疏跟踪器直接部署到异步参考更新会使成功率跌至 75.48%（同步评测下同型跟踪器为 98.58%）、异步区间误差达 14.64 cm/15.15°；其机制是缓存参考被反复当作当前控制帧的瞬时目标，使每个参考区间内的执行相对累积帧失配近似开环——时间异步是末端任务空间跟踪精度的结构性痛点，而 ASYNC-3PT 隐式对齐将其恢复到 99.50% 成功、6.90 cm/6.83°。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.25706](https://arxiv.org/abs/2606.25706) Learning Asynchronous Upper-body Task-space Trajectory Tracking Policy for Humanoid Robots
- Locator: VI-B. Effect of Asynchronous Sparse Trajectory Tracking, Table I
- Evidence: Table I 显示 Sync W.ASC 75.48% 成功、Pos_1s 14.64 cm、Rot_1s 15.15°，而同步评测的 Sync W.SC 为 98.58%、ASYNC-3PT 为 99.50%/6.90/6.83；正文把退化机制明确表述为缓存参考被当作瞬时目标导致区间内近似开环执行。
- Quote: “Directly deploying a synchronous tracker under asynchronous refer- ence updates also leads to clear degradation: Sync W.ASC achieves only 75.48% success rate, with larger asynchronous tracking errors of 14.64 cm and 15.15 ◦ . This is because the cached reference is repeatedly treated as an instantaneous target in the current control frame, making execution within each reference interval approximately open-loop with respect to the accumulated frame mismatch.”
- Authors: yumeng-liu; dongqi-wang; jiyu-yu; et al.

### EA-TRAJACC-2026-0108

- Claim: 异步执行下，新动作块仍基于过期观测生成，直接拼接连续块会在交接边界破坏连续性，表现为突发动作变化、振荡修正与轨迹抖动，在接触丰富或精度敏感操作中可累积为任务失败；现有补救（运行时 inpainting/插值）多为启发式且依赖架构。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: I. Introduction
- Evidence: 引言将异步分块执行的失效模式定性为 handoff 边界的不连续（突发动作变化、振荡修正、轨迹抖动），并指出运行时 inpainting/插值类补救是启发式且架构相关的。
- Quote: “and direct stitching of consecutive chunks can break conti- nuity at the handoff boundary. The resulting discontinuities often appear as abrupt action changes, oscillatory correc- tions, and trajectory jitter, and in contact-rich or precision- sensitive manipulation they can accumulate into outright task failure. Existing remedies alleviate this issue only partially. Runtime inpainting or interpolation can smooth local discontinuities, but such methods are often heuristic and architecture-depend”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0116

- Claim: 作者自我声明的关键限制：ACNet 的延迟优势（91 ms vs 134/159 ms）主要来自底层模型选择（轻量 Evo-1 骨干）而非 ACNet 侧分支本身更快——同骨干下 ACNet 反而会给标准前向增加小编码器与投影开销，只是该开销被 Evo-1 更低的端到端运行时抵消。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: V-C. Quantitative Results
- Evidence: V-C 节在报告 MT50 延迟结果后立即声明该优势源于模型选择而非 ACNet 分支，并说明同骨干下的额外开销与抵消逻辑。
- Quote: “This latency advantage is mainly due to the underlying model choice rather than the ACNet side branch being intrinsically faster than delay-conditioned training: RTC and Training-RTC are based on π 0 , whereas ACNet is built on the lightweight Evo-1 backbone. On the same backbone, the proposed ACNet would add a small encoder and projection overhead to a standard forward pass.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0137

- Claim: 在0.5m分布外垂直间距上，学习模型对角加速度的残差预测误差略高于仅用ROM的模型，作者将此归因于神经网络对近距离强湍流数据的轻微过拟合，即学习残差在低扰动大间距工况下的角动力学泛化受限。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.12275](https://arxiv.org/abs/2607.12275) Flatness-Preserving Residual Learning for Real-Time Tight Quadrotor Formation Flight
- Locator: 5.1 Simulation Experiments
- Evidence: 5.1节表1讨论原文：学习模型在分布内与更近距离（0.2m）表现良好，但在更大的0.5m间距上仅用ROM略优；作者推断网络可能对高湍流近距离数据轻微过拟合，弱化了对更大、扰动更小间距下角动力学的泛化。
- Quote: “however, at the larger 0.5m separation, just using the ROM slightly outperforms it. This suggests that the neural network may mildly overfit to the highly turbulent close-proximity data, thereby marginally weakening its generalization to angular dynamics at larger, less perturbed distances.”
- Authors: pei-an-hsieh; fengjun-yang; nikolai-matni; et al.

### EA-TRAJACC-2026-0128

- Claim: 逐任务成功率非均匀：SEAM 在 T1–T3、T5 上最强、T6 并列最佳，但在 T7–T10 上低于最佳对比方法（如 T7：SEAM 90.8% vs RTC 99.2%）；聚合成功率保持（95.7%）不等于逐任务改进，作者因此主张任务成功、平滑度与去噪循环成本应联合评估而非单指标排名。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.04609](https://arxiv.org/abs/2607.04609) SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies
- Locator: Main Results, Table 3
- Evidence: Main Results 的 Table 3 段（该句在提取文本中被 Figure 3 说明与 Table 3 隔断，引文取图后连续部分）与 Table 3 逐任务数值：T1 基线 91.5→SEAM 99.2（ACT-TE 58.5，最大差距任务）；T7 SEAM 90.8 vs RTC 99.2；T10 SEAM 93.8 vs RTC 95.4；Overall 94.8/95.7/95.1/82.7。
- Quote: “it is strongest on several tasks (T1–T3 and T5), ties the best comparison on T6, and remains below the best comparison method on some tasks (T7–T10). We therefore treat task success, smoothness, and denoising- loop cost jointly rather than as a single-metric ranking.”
- Authors: dijia-zhan; xuemiao-xu; jinyi-li; et al.

### EA-TRAJACC-2026-0151

- Claim: 真机平台因仅由4缆驱动、工作空间是轴向压缩应变可忽略形成的'厚度极小的曲面'，为避免目标轨迹越出可达工作空间，实验只控制末端3维位置中的2维（X、Y、Z中的两个坐标），真机验证不覆盖姿态控制与全3维位置跟踪。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.24029](https://arxiv.org/abs/2607.24029) Moving-Horizon Estimation and Nonlinear Model Predictive Control of Cable-Driven Soft Manipulators
- Locator: VIII-B2) Trajectory tracking control
- Evidence: VIII-B2原文：鉴于软体臂仅由4缆驱动，末端工作空间构成厚度极小的曲面，该有限厚度源于绳张紧时软臂经历的轴向压缩应变可忽略[45]；为防目标轨迹越出可用工作空间，只管理末端位置(X,Y,Z)三个空间坐标中的两个。结论future work亦承认需向更高维位姿调节扩展。
- Quote: “Given that the soft manipulator is actuated by only four cables, the workspace of the end-effector constitutes a surface with minimal thickness. This limited thickness is due to the negligible axial compression strain experienced by the soft manipulator when tensioned by the cables, as noted in [45]. To prevent the target trajectory from extending beyond the available workspace, we manage only two of the three spatial coordinates (X, Y, Z) of the end-effector’s position.”
- Authors: lingxiao-xun; haihong-li; gang-zheng

### EA-TRAJACC-2026-0154

- Claim: 作者自述：Hermite 正则把轨迹平滑建模为软性归纳偏置而非严格约束，以牺牲绝对轨迹连续性换取策略表达力，且先验独立于视觉表征与非平滑接触事件。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.01265](https://arxiv.org/abs/2608.01265) Hermite Curves as Trajectory Priors for Vision-Language-Action Models
- Locator: 5 LIMITATION AND FUTURE WORK
- Evidence: 限制与未来工作一节原文给出两条方法学权衡，直接界定该方案的适用边界，是方案族痛点的一手作者陈述。
- Quote: “Our study highlights two key methodological trade-offs. First, Hermite regularization models trajectory smoothness as a soft inductive bias rather than strict constraints, preserv- ing policy expressivity at the expense of absolute trajectory continuity. Second, the proposed prior focuses on action- sequence structure, operating independently of vision-side representations and of non-smooth contact events.”
- Authors: qi-lv; jianming-xing; zhao-yang; et al.

### EA-TRAJACC-2026-0139

- Claim: 异步 VLA 推理的感知-执行错位痛点：因环境在 VLA 为下一动作块推理期间持续演化，朴素异步与 RTC 的任务成功率随推理延迟 ∆ 增大而显著下降；VLASH 在低 ∆ 下保持高精度，但更长延迟下仅预测未来机器人状态不足以捕捉环境变化——错位随延迟增大而加剧，是机载（长延迟）部署区别于高端 GPU 部署的核心精度痛点。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.12659](https://arxiv.org/abs/2607.12659) Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference
- Locator: 3 When Asynchronous Inference Meets Onboard Computation, Figure 3(a)(b)
- Evidence: 第 3 节用 Fig. 3(a)(b)（π0、LIBERO-Spatial/Goal）量化错位-成功率关系：朴素异步与 RTC 随 ∆ 增大成功率下降，VLASH 低 ∆ 稳定但长延迟不足；机制表述为环境在推理期间相对输入图像已变化。
- Quote: “Perception-execution misalignment arises because the envi- ronment continues to evolve while the VLA model performs inference for the next action chunk. As shown in Figure 3(a)(b), for naive asynchronous and RTC, with VLA inference latency increases, perception-execution misalignment becomes more severe, leading to task success rate drop.”
- Authors: zebin-yang; qi-wang; yunhe-wang; et al.

### EA-TRAJACC-2026-0163

- Claim: 离线重叠区分析显示：推理期速度引导（infer）在所有关节的 delay region 上 MAE 与 max 误差都显著高于动作约束类方法（simple/train）；速度级引导只改变去噪方向而不对输出动作施加硬约束，因此不能保证块边界动作连续，位置跳变不可避免。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.01880](https://arxiv.org/abs/2608.01880) World Action Models in Real Time: An Empirical Study of Smooth Execution via Asynchronous Deployment
- Locator: 5.2 Offline Trajectory Analysis
- Evidence: 5.2 节关键观察 1 给出该结论及其机制解释（速度引导 vs 动作约束的区别），与在线动态任务 infer 仅 30 分的结果一致。
- Quote: “infer fails to constrain the delay region. Across all joints, infer shows substantially higher MAE and max error in the delay region compared to simple and train. Unlike action-constraining methods, velocity-level guidance steers the denoising trajectory without enforcing hard constraints on the output actions, and therefore cannot guarantee action continuity at chunk boundaries—position jumps remain unavoidable.”
- Authors: motubrain-team

### EA-TRAJACC-2026-0167

- Claim: 残差DDPG在降低跟踪误差的同时把最大logged代数绳需求从76.87 N提高到86.24 N（+12.2%）——存在跟踪精度-绳力需求权衡，且因F_max未定义该绳需求只是诊断量而非执行器饱和可行性证明。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.26739](https://arxiv.org/abs/2608.26739) Residual Deep Reinforcement Learning-Based Computed Torque Control for a Cable-Driven Lower-Limb Rehabilitation Robot under Disturbances and Parametric Uncertainties
- Locator: 6.2. Representative combined uncertainty/disturbance case, Table 11
- Evidence: 6.2节原文：残差控制器把最大logged代数绳需求从76.87 N提高到86.24 N同时降低跟踪误差，量化了跟踪-需求权衡，并提示在物理电机/线轴/绳/预紧/F_max规格定义后应把绳力裕度纳入奖励与分配层；表11标注+12.2% higher且logged分配值非负由构造保证。
- Quote: “The residual controller raises the maximum logged algebraic cable demand from 76.87 N to 86.24 N while reducing tracking error. This quantifies the associated tracking–demand tradeoff and motivates incorporating cable-force margin into the reward and allocation layers once physical motor, spool, cable, pretension, and 𝐹 𝑚𝑎𝑥 specifications are defined.”
- Authors: mohammad-hossein-fakouri; ali-keymasi-khalaji

### EA-TRAJACC-2026-0168

- Claim: 换轨迹（圆形路径、组合情景）迁移评估显示双面结果：残差DDPG把RMS笛卡尔误差从0.021738降至0.012052 m（轨迹特定44.56%降幅），但关节限位channel-samples从44增至101、两支路最小logged张力均为零——改进的笛卡尔跟踪可与轨迹依赖的关节限位违反共存。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.26739](https://arxiv.org/abs/2608.26739) Residual Deep Reinforcement Learning-Based Computed Torque Control for a Cable-Driven Lower-Limb Rehabilitation Robot under Disturbances and Parametric Uncertainties
- Locator: 6.6. Residual authority and alternate-trajectory diagnostic
- Evidence: 6.6节原文：圆形路径上残差DDPG降RMS误差44.56%（轨迹特定），但关节限位channel-samples为44（CTC）对101（残差支路），最小张力双零、最大推断张力230.42 N对162.58 N；结论是展示了笛卡尔跟踪性能的迁移并识别出应纳入后续约束感知训练的扩展关节坐标范围；7.结论再次明确'改进的笛卡尔跟踪可与轨迹依赖的关节限位违反共存'。
- Quote: “The alternate circular path evaluates trajectory transfer and the associated joint-coordinate coverage. Residual DDPG reduces RMS Cartesian error from 0.021738 to 0.012052 m (a trajectory-specific 44.56% reduction), while joint-limit channel-samples are 44 for CTC and 101 for the residual branch.”
- Authors: mohammad-hossein-fakouri; ali-keymasi-khalaji

### EA-TRAJACC-2026-0169

- Claim: 作者自述边界：结果支持有界残差学习作为该仿真模型的有效补偿层，但不建立形式稳定性、动力学绳力实现、执行器饱和可行性、临床收益或硬件安全；改进的笛卡尔跟踪可与轨迹依赖的关节限位违反共存。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.26739](https://arxiv.org/abs/2608.26739) Residual Deep Reinforcement Learning-Based Computed Torque Control for a Cable-Driven Lower-Limb Rehabilitation Robot under Disturbances and Parametric Uncertainties
- Locator: 7. Conclusion
- Evidence: 7. Conclusion原文明确列举不建立的四类主张（形式稳定性、动力学绳力实现、执行器饱和可行性、临床收益或硬件安全），并以圆形路径测试为例说明笛卡尔改善与关节限位违反可共存；未来工作需定义物理预紧与绳力界、实现带不可行指令处理的QP分配器、把约束量纳入学习与监控层，并需更广随机化训练/测试与硬件验证。
- Quote: “The results support bounded residual learning as a useful compensation layer for the evaluated simulation model. They do not establish formal stability, dynamic cable-force realization, actuator-saturation feasibility, clinical benefit, or hardware safety. The circular-path test further shows that improved Cartesian tracking can coexist with trajectory- dependent joint-limit violations.”
- Authors: mohammad-hossein-fakouri; ali-keymasi-khalaji

### EA-TRAJACC-2026-0013

- Claim: 按ISO 9283改编流程做定位重复性测试，UR10e三次独立试验平均位移0.017mm且方差可忽略（小数点后五位一致），而Unitree G1人形机器人三次试验的平均位移与方差均显著不一致——现行标准流程对智能/随机机器人产生不可重复的测量结果。
- Stance: `gap` | Confidence: `direct`
- Paper: [2505.08216](https://arxiv.org/abs/2505.08216) Rethink Repeatable Measures of Robot Performance With Statistical Query
- Locator: I. INTRODUCTION / Fig. 1a
- Evidence: 原文引言以UR10e与G1的真机对照实例说明传统'低方差=可重复'假设失效：UR10e结果高度一致（0.017mm、方差可忽略），G1的平均位移与方差跨试验显著变化；测试设备（0.001mm分辨率千分表）与流程在两机器人间保持一致，仅机器人不同。
- Quote: “Upon executing the complete testing procedure through three independent trials, the UR10e demonstrates remarkably consistent results, achieving an average positioning displacement of 0.017 mm with negligible variance (consistent up to the fifth decimal place) across all trials. In contrast, the humanoid robot G1 exhibits substantially varying aver- age displacements and notable differences in variance among the three trials”
- Authors: bowen-weng; linda-capito; guillermo-a-castillo; et al.

### EA-TRAJACC-2026-0030

- Claim: 作者判断：现有面向多形状鲁棒装配的RL研究通常只追求提升成功率而不评估装配过程中的接触力柔顺性，这对高精度工业任务并不充分。
- Stance: `gap` | Confidence: `direct`
- Paper: [2508.12296](https://arxiv.org/abs/2508.12296) A Robust and Compliant Robotic Assembly Control Strategy for Batch Precision Assembly Task
- Locator: 1. Introduction
- Evidence: 原文引言在综述低精度（0.5-2.0mm间隙）多形状鲁棒装配研究[23-26]后，明确指出这些研究通常只追求成功率而不评估装配力柔顺，不足以支撑高精度工业任务——为本论文双指标（成功率+力柔顺）动机。
- Quote: “different shapes, but numerous agents are trained separated, which is very inefficient. In summary, these researches usually only pursue improving the success rate without evaluating the contact force compliance during assembly, which is not sufficient for high-precision industrial tasks.”
- Authors: bin-wang; jiwen-zhang; song-wang; et al.

### EA-TRAJACC-2026-0022

- Claim: 作者承认本研究的评估只考察相对误差降低，未与其他设备或标定方法做基准对比，建立统一的精度标准是重要未来方向；且受试者手寸略低于人群均值，需要更广泛用户群验证。
- Stance: `gap` | Confidence: `direct`
- Paper: [2507.23592](https://arxiv.org/abs/2507.23592) Human-Exoskeleton Kinematic Calibration to Improve Hand Tracking for Dexterous Teleoperation
- Locator: V. DISCUSSION
- Evidence: V. DISCUSSION的局限清单明确列出：评估为相对误差降低而非对标其他设备或标定方法，统一精度标准是未来方向；受试者代表性（手寸低于人群均值）也需扩展——该卡的71.5%/34.8%等相对降幅因此缺少绝对水平的外部锚点。
- Quote: “Second, we acknowledge that the participants represent hand sizes slightly below the population mean, highlighting the need for validation across a broader and more diverse range of users. Third, the evaluation assessed relative error reduction rather than benchmarking against other devices or calibration methods; establishing unified accuracy standards will be an important direction for future work.”
- Authors: haiyun-zhang; stefano-dalla-gasperina; saad-n-yousaf; et al.

### EA-TRAJACC-2026-0069

- Claim: 论文全部实验限于 LIBERO/LIBERO-Plus 仿真；作者明确把真实机器人平台与长时序操作任务上的验证、任务自适应/感知感知的平滑目标、以及与基于模型控制或世界模型的结合列为未来工作。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.13925](https://arxiv.org/abs/2603.13925) SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization
- Locator: 6 Conclusion
- Evidence: 结论章节在'promising results'之后自述三个未来方向，第一条即扩展到更复杂真实机器人平台与长时序任务，说明当前证据边界为仿真桌面操作。
- Quote: “Despite the promising results, this work opens sev- eral directions for future research.First, we plan to extend SmoothVLA to more complex real-world robotic platforms and long-horizon manipulation tasks, where smoothness con- straints are even more critical for safety and stability.”
- Authors: jiashun-li; xiaoyu-shi; hong-xie; et al.

### EA-TRAJACC-2026-0081

- Claim: 未解痛点：当前框架缺乏自适应机制，无法处理突发负载不确定（如末端抓取引起），作者将引入自适应控制列为未来工作；同段结论强调相对 LQR+前馈基线在快速振动抑制与轨迹跟踪上的优越性。
- Stance: `gap` | Confidence: `direct`
- Paper: [2605.17477](https://arxiv.org/abs/2605.17477) Rapid Vibration Suppression and Trajectory Tracking of a Serial Manipulator with Multi-Flexible Links
- Locator: V. CONCLUSION
- Evidence: 结论节在陈述对 LQR+前馈的优越性之后，明确把'引入自适应控制处理突发负载不确定（如末端抓取）'列为未来工作，说明当前版本未解决该问题。
- Quote: “Comparative results against the baseline LQR+feedforward method demonstrate the su- perior capability of our proposed strategy in achieving fast vibration suppression and trajectory tracking. Future work will incorporate adaptive control to handle sud- den payload uncertainties (e.g., during end-effector grasping)”
- Authors: chengyi-wang; yilong-huang; ji-wang

### EA-TRAJACC-2026-0087

- Claim: 作者自述局限：固定执行时域引入结构性归纳偏置，在高动态环境中（尤其窗口内发生突变时）可能限制策略表达能力与适应性，未来需要状态相关或可学习的执行 profile、自适应窗口长度或混合方案来放松固定调度假设。
- Stance: `gap` | Confidence: `direct`
- Paper: [2605.19592](https://arxiv.org/abs/2605.19592) Implicit Action Chunking for Smooth Continuous Control
- Locator: 5. Conclusion
- Evidence: 结论章节在总结强经验表现后明确承认固定执行时域的归纳偏置风险，并把状态相关/可学习执行 profile 与自适应窗口长度列为未来工作。
- Quote: “While DWS demonstrates strong empirical performance across diverse domains, its fixed execution horizon intro- duces a structural inductive bias that may limit policy expres- siveness and adaptability in highly dynamic environments, especially when abrupt changes occur within a window.”
- Authors: bosun-liang; shuo-pei; zirui-chen; et al.

### EA-TRAJACC-2026-0101

- Claim: 无名义调参的柔顺补偿学习及其收敛性质被作者列为未来工作：当前框架仍依赖离线标定名义参数（含 y 位置相关柔顺查找表），该依赖带来的手工调参成本与未验证的收敛性是作者承认的开放问题。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.03533](https://arxiv.org/abs/2606.03533) Recursive Learning of Feedforward and Compliance Compensation Parameters for Precision Motion Systems
- Locator: 6. CONCLUSION
- Evidence: 结论节明确将'learning compliance compensation without nominal tuning to verify convergence properties, potentially reducing manual tuning effort'列为未来工作，说明当前版本未解决该问题。
- Quote: “Re- sults show that a multivariate regression reduces param- eter coupling, predominantly between velocity and jerk feedforward, and between acceleration feedforward and compliance compensation. Future work will focus on learn- ing compliance compensation without nominal tuning to verify convergence properties, potentially reducing manual tuning effort.”
- Authors: m-wind; j-pierssens; r-beerens; et al.

### EA-TRAJACC-2026-0120

- Claim: 作者将三项扩展列为未来工作：更丰富的延迟信号、更大与时变的延迟、更广类别的实时控制策略——即当前框架只验证了固定离散延迟档，时变延迟鲁棒性未解决；同时作者总结 ACNet 以显著低于全量延迟条件化重训练的适配成本改善延迟控制鲁棒性与轨迹平滑度。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.25985](https://arxiv.org/abs/2606.25985) Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models
- Locator: VI. Conclusion
- Evidence: 结论段总结贡献（更低适配成本下的鲁棒性与平滑度改善）并列出三项未来工作，其中'larger and time-varying delays'直接界定了当前验证范围。
- Quote: “Experiments on Kinetix, Meta-World MT50, and a real SO-ARM101 platform show that ACNet improves delayed-control robustness and trajectory smooth- ness with substantially lower adaptation cost than full delay-conditioned retraining. Future work will extend this boundary-conditioning framework to richer delay signals, larger and time-varying delays, and broader classes of real- time control policies.”
- Authors: tiecheng-guo; meng-guo

### EA-TRAJACC-2026-0138

- Claim: 作者自述的适用边界：平坦性保持残差的结构假设需要在未来放宽，且实验规模（双机）需要扩大，即当前结构化参数化与实验规模是该方法已知的未解限制。
- Stance: `gap` | Confidence: `direct`
- Paper: [2607.12275](https://arxiv.org/abs/2607.12275) Flatness-Preserving Residual Learning for Real-Time Tight Quadrotor Formation Flight
- Locator: 6 Conclusion
- Evidence: 结论节原文：未来工作包括放宽平坦性保持残差的结构假设与扩大实验规模；结合全文以双机Crazyflie为对象的事实，表明结构约束（残差仅依赖位置/速度）与规模（两机）是作者明确承认的边界。
- Quote: “we demonstrated that our method effectively handles complex multi- quadrotor proximity flight scenarios with significant performance gains over baseline controllers. Future work includes relaxing the structural assumptions of the flatness-preserving residuals and scaling up the experiments.”
- Authors: pei-an-hsieh; fengjun-yang; nikolai-matni; et al.

### EA-TRAJACC-2026-0156

- Claim: 在该真机设置下，所有策略变体（含 Hermite 变体）在重规划交接步的控制不连续度都显著高于块内部执行（交接/内部比 ρ 达 5.5–8.6），说明重规划边界不连续是闭环分块执行 VLA 的普遍结构性痛点。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.01265](https://arxiv.org/abs/2608.01265) Hermite Curves as Trajectory Priors for Vision-Language-Action Models
- Locator: 4.5 Smoothness and Trajectory-Quality Analysis
- Evidence: 4.5 节边界评估的第一条结论对所有被测连续策略成立，量化为 ρ 范围 5.5–8.6；该现象与仿真分析一致，构成与具体方案无关的结构性问题陈述。
- Quote: “every policy variant exhibits significantly higher control discontinuity at replan- ning handovers than during interior execution (ρ ranging from 5.5 to 8.6), which is consistent with the observation”
- Authors: qi-lv; jianming-xing; zhao-yang; et al.

### EA-TRAJACC-2026-0144

- Claim: 作者自述局限：机载平台在算力与带宽上相对 GPU 集群存在根本性受限，随着模型参数量与批量规模继续增大，Jetson-PI 的性能增益可能无法完全弥合与高端 GPU 部署的差距——机载实时化方案的适用条件受硬件资源上限与模型规模扩张的制约。
- Stance: `gap` | Confidence: `direct`
- Paper: [2607.12659](https://arxiv.org/abs/2607.12659) Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference
- Locator: 7 Limitations
- Evidence: 论文设有独立 Limitations 小节，明确承认机载平台算力/带宽的根本性约束，并指出模型参数量与批量继续增大时收益可能不足以闭合与高端 GPU 部署的差距，同时给出适用定位（功耗与便携性敏感的移动机器人应用）。
- Quote: “the onboard platform remains fundamentally constrained in compute and bandwidth relative to GPU clusters. As model parameter counts and batch sizes continue to scale, the performance gains of Jetson-PI may not fully close the gap with high-end GPU deployment.”
- Authors: zebin-yang; qi-wang; yunhe-wang; et al.

### EA-TRAJACC-2026-0161

- Claim: 作者主张：时间对齐（把每帧命令关联到正确观测时间戳）是关键且常被低估的工程前提，对齐不良造成的持续抖动无法被任何混合算法补偿。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.01880](https://arxiv.org/abs/2608.01880) World Action Models in Real Time: An Empirical Study of Smooth Execution via Asynchronous Deployment
- Locator: 1 Introduction
- Evidence: 引言贡献 1 与讨论的『Reliable async execution—accurate temporal alignment—is the prerequisite』相互印证，构成作者对该领域痛点的一手判断。
- Quote: “We show that temporal alignment—accurately associating each command frame with the correct obser- vation timestamp—is a critical and often underappreciated engineering requirement; poor alignment causes persistent jitter that no blending algorithm can compensate for.”
- Authors: motubrain-team

### EA-TRAJACC-2026-0162

- Claim: 作者自述开放问题：所有被比较方法都假设旧块前缀提供有用引导；环境突变（如突然出现的障碍物使 chunk n+1 大幅偏离旧轨迹）时 prefix 约束变得有害，平滑且具反应性的轨迹生成无解。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.01880](https://arxiv.org/abs/2608.01880) World Action Models in Real Time: An Empirical Study of Smooth Execution via Asynchronous Deployment
- Locator: 6 Discussion and Conclusion
- Evidence: 讨论节明确把该情形列为作者计划探索的开放问题，并配 Figure 6 图示障碍物场景，属于作者一手承认的边界。
- Quote: “all methods here assume the prior chunk provides useful guidance; this breaks down when the environment changes abruptly. As illustrated in Figure 6, a suddenly appearing obstacle drives chunk n+1 away from the prior trajectory, making the prefix constraint harmful rather than helpful. How to generate smooth yet reactive trajectories under such conditions is an open problem we plan to explore.”
- Authors: motubrain-team

## References

- `2503.04862` [High-Precision Transformer-Based Visual Servoing for Humanoid Robots in Aligning Tiny Objects](https://arxiv.org/abs/2503.04862) (2025-10-19)
- `2504.13056` [Adaptive Task Space Nonsingular Terminal Super-Twisting Sliding Mode Control of a 7-DOF Robotic Manipulator](https://arxiv.org/abs/2504.13056) (2025-09-16)
- `2505.08216` [Rethink Repeatable Measures of Robot Performance With Statistical Query](https://arxiv.org/abs/2505.08216) (2025-12-18)
- `2507.23592` [Human-Exoskeleton Kinematic Calibration to Improve Hand Tracking for Dexterous Teleoperation](https://arxiv.org/abs/2507.23592) (2026-03-02)
- `2508.12296` [A Robust and Compliant Robotic Assembly Control Strategy for Batch Precision Assembly Task](https://arxiv.org/abs/2508.12296) (2026-01-01)
- `2509.05391` [Evaluating Magic Leap 2 Controller Tracking for Sensor Tool Guidance in AR-Based Industrial Inspections](https://arxiv.org/abs/2509.05391) (2025-10-08)
- `2511.00983` [Breaking the Latency Barrier: Synergistic Perception and Control for High-Frequency 3D Ultrasound Servoing](https://arxiv.org/abs/2511.00983) (2025-11-02)
- `2511.11850` [Neural Network-Augmented Iterative Learning Control for Friction Compensation of Motion Control Systems with Varying Disturbances](https://arxiv.org/abs/2511.11850) (2025-11-14)
- `2601.20130` [Real-Time Robot Execution with Masked Action Chunking](https://arxiv.org/abs/2601.20130) (2026-01-27)
- `2602.06341` [HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation](https://arxiv.org/abs/2602.06341) (2026-02)
- `2603.13925` [SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization](https://arxiv.org/abs/2603.13925) (2026-03-14)
- `2603.19418` [Speculative Policy Orchestration: A Latency-Resilient Framework for Cloud-Robotic Manipulation](https://arxiv.org/abs/2603.19418) (2026-03-19)
- `2605.17477` [Rapid Vibration Suppression and Trajectory Tracking of a Serial Manipulator with Multi-Flexible Links](https://arxiv.org/abs/2605.17477) (2026-05-17)
- `2605.19592` [Implicit Action Chunking for Smooth Continuous Control](https://arxiv.org/abs/2605.19592) (2026-05-19)
- `2606.00537` [PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking](https://arxiv.org/abs/2606.00537) (2026-05-30)
- `2606.03533` [Recursive Learning of Feedforward and Compliance Compensation Parameters for Precision Motion Systems](https://arxiv.org/abs/2606.03533) (2026-06-02)
- `2606.25706` [Learning Asynchronous Upper-body Task-space Trajectory Tracking Policy for Humanoid Robots](https://arxiv.org/abs/2606.25706) (2026-06-24)
- `2606.25985` [Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models](https://arxiv.org/abs/2606.25985) (2026-06-24)
- `2607.04609` [SEAM: Smooth Execution of Action-Chunked Motion for Vision-Language-Action Policies](https://arxiv.org/abs/2607.04609) (2026-07-06)
- `2607.12275` [Flatness-Preserving Residual Learning for Real-Time Tight Quadrotor Formation Flight](https://arxiv.org/abs/2607.12275) (2026-07)
- `2607.12659` [Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference](https://arxiv.org/abs/2607.12659) (2026-08-03)
- `2607.24029` [Moving-Horizon Estimation and Nonlinear Model Predictive Control of Cable-Driven Soft Manipulators](https://arxiv.org/abs/2607.24029) (2026-07-27)
- `2608.01265` [Hermite Curves as Trajectory Priors for Vision-Language-Action Models](https://arxiv.org/abs/2608.01265) (2026-08-02)
- `2608.01880` [World Action Models in Real Time: An Empirical Study of Smooth Execution via Asynchronous Deployment](https://arxiv.org/abs/2608.01880) (2026-08-11)
- `2608.26739` [Residual Deep Reinforcement Learning-Based Computed Torque Control for a Cable-Driven Lower-Limb Rehabilitation Robot under Disturbances and Parametric Uncertainties](https://arxiv.org/abs/2608.26739) (2026-08-27)
