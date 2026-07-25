# Evidence Appendix: 近一年 loco-manipulation 研究进展

- Time range: 2025-07-19 至 2026-07-19
- Events: 21
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-LOCOMANIP-2026-0005

- Claim: In simulation, the NSDF-conditioned policy maintained 100% success for standard-mass cylinders, cuboids and spheres, while removing NSDF produced 0% across those shapes.
- Stance: `support` | Confidence: `direct`
- Paper: [2509.13534](https://arxiv.org/abs/2509.13534) Embracing Bulky Objects with Humanoid Robots: Whole-Body Manipulation with Reinforcement Learning
- Locator: IV-B Adaptability to Different Object Properties
- Evidence: The shape sweep directly contrasts the full method with the no-NSDF ablation.
- Quote: “First, when the NSDF module is incorporated, the policy achieves and maintains a 100% success rate across multiple object types, including cylinders, cuboids, and spheres, under standard mass (3 kg) and size conditions. This demonstrates strong sim-to-sim transfer performance. In contrast, the policy exhibits complete failure (0% success) across all shape categories without NSDF, highlighting the essential role of this module in capturing geometric and semantic attributes for stable manipulation”
- Authors: chunxin-zheng; kai-chen; zhihai-bi; et al.

### EA-LOCOMANIP-2026-0006

- Claim: Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the evaluated tasks.
- Stance: `support` | Confidence: `direct`
- Paper: [2512.11047](https://arxiv.org/abs/2512.11047) WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control
- Locator: 4.3 How does action-free videos contribute to loco–manipulation?
- Evidence: The ablation directly compares the full model with removal of unified latent learning.
- Quote: “As shown in Table 4.2 , the full model improves success rate by 38.7%, indicating that unified latent learning extracts useful priors from action-free human videos and enhances downstream policy learning.”
- Authors: haoran-jiang; jin-chen; qingwen-bu; et al.

### EA-LOCOMANIP-2026-0008

- Claim: In a 15-minute comparison, HuMI collected 62 episodes versus 28 for TWIST2, with 96.7% versus 64.3% acceptance; time per acceptable episode fell to 30.0% of TWIST2.
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06643](https://arxiv.org/abs/2602.06643) Humanoid Manipulation Interface: Humanoid Whole-Body Manipulation from Robot-Free Demonstrations
- Locator: VI Data Collection Efficiency
- Evidence: The timed comparison jointly reports quantity, quality and accepted-data cost.
- Quote: “HuMI yields substantially higher throughput, collecting 62 episodes versus 28 with TWIST2, while also achieving a higher acceptance rate ( 96.7% vs. 64.3% ). HuMI’s streamlined, robot-free workflow further reduces the average time per acceptable episode to 30.0% of that of TWIST2”
- Authors: ruiqian-nai; boyuan-zheng; junming-zhao; et al.

### EA-LOCOMANIP-2026-0009

- Claim: With 100 robot and 300 human demonstrations, co-training scored 78% versus 59% for robot-only in-domain, and 82% versus 31% under generalization.
- Stance: `support` | Confidence: `direct`
- Paper: [2602.10106](https://arxiv.org/abs/2602.10106) EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
- Locator: IV-B Will human data improve humanoid loco-manipulation?
- Evidence: The main comparison directly reports both in-domain and generalization gaps.
- Quote: “For in-domain evaluation, co-training achieves 78% average score versus 59% for robot-only. The gap widens remarkably in generalization settings: co-training reaches 82% compared to 31% for robot-only.”
- Authors: modi-shi; shijia-peng; jin-chen; et al.

### EA-LOCOMANIP-2026-0019

- Claim: On hardware, Sumo uprighted a 15 kg tire—heavier than Spot arm's stated 11 kg lifting capacity—in 10/10 trials, averaging 9.2±4.7 seconds.
- Stance: `support` | Confidence: `direct`
- Paper: [2604.08508](https://arxiv.org/abs/2604.08508) Sumo: Dynamic and Generalizable Whole-Body Loco-Manipulation
- Locator: page 8
- Evidence: The hardware case study reports object mass, nominal arm capacity, success and completion time.
- Quote: “Tire Upright:In Fig. 7 (a), the robot is tasked to upright a tire of15kg, which is heavier than the maximum lifting capacity of11kg of the Spot arm. Additionally, the rubber tire presents hard-to-model geometries and friction properties, causing a large sim-to-real gap. Using a combination of its arm, torso, and legs, Sumo enables the robot to complete the task10out of10trials with an average completion time of9.2±4.7s, Tab. II.”
- Authors: john-z-zhang; maks-sorokin; jan-brdigam; et al.

### EA-LOCOMANIP-2026-0011

- Claim: On real cupboard opening, WHOLE-MoMa succeeded in 17/25 trials (68%), versus 4/25 for its WBC generator and 8/25 for behavior cloning.
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12509](https://arxiv.org/abs/2604.12509) Whole-Body Mobile Manipulation using Offline Reinforcement Learning on Sub-optimal Controllers
- Locator: VI-B Real-World Results
- Evidence: The real-world table separates full success across the three methods.
- Quote: “WHOLE-MoMa achieves 17/25 (68%), demonstrating substantial sim-to-real transfer, with the highest grasping success (22/25) and articulation success (17/22 given grasping).”
- Authors: snehal-jauhri; vignesh-prasad; georgia-chalvatzaki

### EA-LOCOMANIP-2026-0012

- Claim: Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to 0.85.
- Stance: `support` | Confidence: `direct`
- Paper: [2604.27224](https://arxiv.org/abs/2604.27224) Learning Tactile-Aware Quadrupedal Loco-Manipulation Policies
- Locator: IV-B Experimental Results and Analyze
- Evidence: The paper compares variants with the same tactile-aware high level but different low-level tactile tracking.
- Quote: “Finally, comparing Baseline 3 (P3) with our full method demonstrates the benefit of incorporating tactile commands into the low-level policy: our method further increases the success rate from 0.70 to 0.85 on Task 1 insertion (+0.15), from 0.60 to 0.80 on Task 1 whole (+0.20), and from 0.80 to 0.85 on Task 2 (+0.05), and achieves 1.00 on Task 3 (compared to 0.20 for P1).”
- Authors: pokuang-zhou; yuhao-zhou; quan-khanh-luu; et al.

### EA-LOCOMANIP-2026-0013

- Claim: Across nine simulated tasks, data generated from one source demonstration raised average policy performance from 0.33 for DexMimicGen+ to 0.89 for HumanoidMimicGen.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.27724](https://arxiv.org/abs/2605.27724) HumanoidMimicGen: Data Generation for Loco-Manipulation via Whole-Body Planning
- Locator: 6.2 HumanoidMimicGen Capabilities
- Evidence: The main comparison reports downstream policy performance averaged over all nine tasks.
- Quote: “From Table 1 , HumanoidMimicGen improves policy performance over all baselines in all tasks. Averaged over nine tasks, data generated by HumanoidMimicGen from a single source human demonstration increases policy performance from 0.33 (DexMimicGen+) to 0.89”
- Authors: kevin-lin; ajay-mandlekar; caelan-reed-garrett; et al.

### EA-LOCOMANIP-2026-0014

- Claim: In a staged real long-horizon task, TA-WBC completed five consecutive bottle-pick, stair-climb, disposal and return runs without falls or stumbles.
- Stance: `support` | Confidence: `direct`
- Paper: [2605.31343](https://arxiv.org/abs/2605.31343) Learning Terrain-Aware Whole-Body Control for Perceptive Legged Loco-Manipulation
- Locator: IV-C 2 Long-Horizon Loco-Manipulation
- Evidence: The real-world section explicitly reports repeated completion of the full multi-stage route.
- Quote: “The result shows that the legged manipulator with TA-WBC can successfully finish this long-horizon challenging task 5 times in a row without any falls or stumbles, verifying the robustness of our framework.”
- Authors: sikai-guo; yudong-zhong; guoyang-zhao; et al.

### EA-LOCOMANIP-2026-0020

- Claim: On four tasks held out from whole-body teleoperation, stationary same-embodiment co-training raised average task progress from 33% to 87%, close to a 94% 12-task teleoperation oracle.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.22174](https://arxiv.org/abs/2606.22174) OpenHLM: An Empirical Recipe for Whole-Body Humanoid Loco-Manipulation
- Locator: 1 Introduction
- Evidence: The paper overview reports the held-out-task gain and the full-teleoperation oracle.
- Quote: “Quantitatively, OpenHLM reaches 89% average task progress on the 8 training tasks of our HLM-12 benchmark; on the remaining 4 held-out tasks that whole-body teleop never covers, co-training with cheaper data lifts task progress from 33% to 87%, closing most of the gap to a 12-task oracle (94%).”
- Authors: yingdong-hu; haodong-zhu; boyuan-zheng; et al.

### EA-LOCOMANIP-2026-0021

- Claim: In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper.
- Stance: `support` | Confidence: `direct`
- Paper: [2607.10132](https://arxiv.org/abs/2607.10132) TAC-LOCO: Unified Whole-Body Control for Quadrupedal TACtile-Informed LOCO-Manipulation
- Locator: 6.5 Baseline comparison
- Evidence: The hardware baseline comparison isolates learned grasp regulation under the same command set.
- Quote: “We conduct 10 hardware trials using the same set of loco-manipulation commands as in Sec. 6 . Table 4 compares the success rates of our policy and the baseline, showing that our tactile-informed policy achieves a substantially higher success rate. Figure 11 shows that the baseline suffers from gradual object slip during the task. Since the gripper width remains fixed, the policy cannot actively suppress slip once the external force changes. Table 4: Deployment success rate comparison with baseli”
- Authors: muqun-hu; yuhao-zhou; kabir-ray-malik; et al.

### EA-LOCOMANIP-2026-0002

- Claim: On two real-world tasks, the same controller achieved 98% and 100% success under teleoperation, versus 80% and 85% when driven by a diffusion policy.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2508.10538](https://arxiv.org/abs/2508.10538) MLM: Learning Multi-task Loco-Manipulation Whole-Body Control for Quadruped Robot with Arm
- Locator: IV-C Real-world Experiments
- Evidence: Table V directly separates low-level tracking results under teleoperation and diffusion-policy trajectory generation.
- Quote: “TABLE V: Real-world experiment results. (cm / radian / %) EE pos err EE rot err Success Rate Teleoperation unplug charger 1.39 0.054 98 open container 1.02 0.047 100 DP unplug charger 1.37 0.039 80 open container 1.24 0.036 85”
- Authors: xin-liu; bida-ma; chenkun-qi; et al.

### EA-LOCOMANIP-2026-0003

- Claim: For two-box pick-and-place, the solver found the first goal-satisfying feasible plan after 30 of 200 tree expansions, with an average solve time of 52.3 seconds.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2508.14099](https://arxiv.org/abs/2508.14099) Task and Motion Planning for Humanoid Loco-manipulation
- Locator: IV-C Example Solutions
- Evidence: The example-solution section reports both search effort and computation for the modeled task.
- Quote: “The two-box pick and place tree search was expanded 200 times with an average solve time of 52.3 seconds. Note that using an NLP solver that exploits the sparsity in time of trajectory optimization, such as the SQP solver in Acados [ 20 ] , could yield a significant speedup w.r.t. IPOPT. A variety of solutions were generated, with the first feasible solution satisfying the goal being found in 30 iterations.”
- Authors: michal-ciebielski; victor-dhdin; majid-khadiv

### EA-LOCOMANIP-2026-0018

- Claim: On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.03279](https://arxiv.org/abs/2603.03279) ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation
- Locator: V-E Real-World Deployment
- Evidence: The real-world table separates external-state and onboard egocentric control modes.
- Quote: “TABLE IV : Real-world success rates on the OMOMO subset using a Unitree G1 humanoid. Each task is evaluated over two trials. MoCap provides object pose tracking for non-egocentric control modes, while the egocentric setting relies only on onboard sensing. MoCap is used for success evaluation in all settings. Dense reference tracking is direction-agnostic and thus reported as a single success rate. Setting Vertical Lateral Dense Reference Tracking 73% (19/26) Sparse Goal Following (MoCap) 80% (8/”
- Authors: xialin-he; sirui-xu; xinyao-li; et al.

### EA-LOCOMANIP-2026-0010

- Claim: The study reports a depth-only mobile-manipulation policy whose risk sensitivity can be adjusted at runtime while retaining task performance comparable to risk-neutral methods in simulation.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.04579](https://arxiv.org/abs/2603.04579) Risk-Aware Reinforcement Learning for Mobile Manipulation
- Locator: VI Conclusion
- Evidence: The conclusion summarizes risk-aware student competence and transfer through imitation learning.
- Quote: “Our approach trains risk-aware visuomotor policies for mobile manipulation conditioned on egocentric depth observations with runtime-adjustable risk sensitivity, achieving comparable performance to risk-neutral methods, and we show learnt risk-aware behaviours can be successfully transferred through Imitation Learning.”
- Authors: michael-groom; james-wilson; nick-hawes; et al.

### EA-LOCOMANIP-2026-0015

- Claim: In zero-shot transfer, pick-and-place scored 9/10 in simulation and 8/10 on hardware; handover scored 10/10 in simulation and 8/10 on hardware.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08278](https://arxiv.org/abs/2606.08278) SIMPLE: Simulation-Based Policy Learning and Evaluation for Humanoid Loco-manipulation
- Locator: 4 Experiments
- Evidence: The transfer table reports paired simulation and real success counts; in the recovered HTML it is attached to the parent experiments section.
- Quote: “Task Sim Eval Real Eval Pick & Place 9/10 = 0.90 8/10 = 0.80 Handover 10/10 = 1.00 8/10 = 0.80 Table 5: Zero-Shot Sim-to-Real Transfer. Success rates of a single policy fine-tuned exclusively on simulation data, evaluated both in the simulator and directly in the real world.”
- Authors: songlin-wei; zhenhao-ni; jie-liu; et al.

### EA-LOCOMANIP-2026-0016

- Claim: Across three simulated BEHAVIOR-1K tasks, SERF achieved mean task progress of 63.5, 60.1 and 52.5, versus 40.7, 43.0 and 48.4 for the fine-tuned image-only PI0.5 baseline.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.12956](https://arxiv.org/abs/2606.12956) SERF: Spatiotemporal Environment and Robot Feature Map for Long-Horizon Mobile Manipulation
- Locator: 5 Long-Horizon Mobile Manipulation
- Evidence: The main table reports mean task progress for the full system and image-only baseline across three tasks.
- Quote: “The full SERF policy achieves the highest task progress on all three evaluated tasks.”
- Authors: sunghwan-kim; byeonghyun-pak; kehan-long; et al.

### EA-LOCOMANIP-2026-0017

- Claim: Under an unseen locked-joint fault at the most demanding placement height, FT-WBC retained 70% survival but only 45% task success, reflecting an explicit survival-first posture policy.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.24466](https://arxiv.org/abs/2606.24466) FT-WBC: Learning Fault-Tolerant Whole-Body Control for Legged Loco-Manipulation
- Locator: 4.3 Real-World Deployment
- Evidence: The real-world analysis directly attributes reduced completion to conservative posture limits that preserve the degraded support polygon.
- Quote: “At the extreme height, our framework still guarantees a 70% survival rate even under severe locked conditions, demonstrating strong adaptation to out-of-distribution actuator failures. While the task success rate drops to 45%, this occurs because the PAM conservatively restricts the extreme upward pitch to prevent the CoM from escaping the degraded support polygon.”
- Authors: yudong-zhong; pengfei-mai; sikai-guo; et al.

### EA-LOCOMANIP-2026-0001

- Claim: On the real curtain task, neither image policy completed any of 10 trials; retrieval reached the curtain in 2/10, while behavior cloning did not reach it.
- Stance: `limit` | Confidence: `direct`
- Paper: [2507.21796](https://arxiv.org/abs/2507.21796) MoDeSuite: Robot Learning Task Suite for Benchmarking Mobile Manipulation with Deformable Objects
- Locator: IV-C Deployment on Real Robot
- Evidence: The deployment paragraph contrasts simulation success with physical failure.
- Quote: “While the policies are successful in simulation, neither is able to complete the task in the real world. Specifically, the retrieval-based method managed to approach and make contact with the curtain in 2 out of 10 trials, whereas the behavior cloning (BC) policy failed to even reach the curtain.”
- Authors: yuying-zhang; kevin-sebastian-luck; francesco-verdoja; et al.

### EA-LOCOMANIP-2026-0004

- Claim: Kitchen-R's reported execution evaluation always uses the ground-truth plan to isolate execution from planning error, so its module results are not direct evidence of end-to-end autonomy.
- Stance: `limit` | Confidence: `direct`
- Paper: [2508.15663](https://arxiv.org/abs/2508.15663) Mind and Motion Aligned: A Joint Evaluation IsaacSim Benchmark for Task Planning and Low-Level Policies in Mobile Manipulation
- Locator: IV METRICS
- Evidence: The metrics section explicitly states that execution does not use the predicted plan.
- Quote: “to isolate planning errors from execution errors, the ground-truth plan is always used for execution.”
- Authors: nikita-kachaev; andrei-spiridonov; andrey-gorodetsky; et al.

### EA-LOCOMANIP-2026-0007

- Claim: Cross-simulator smoothness was not a reliable robustness signal: MuJoCo drifted under default friction, while near-zero stop error under tuned friction came from unrealistically high tangential impedance.
- Stance: `limit` | Confidence: `direct`
- Paper: [2512.18938](https://arxiv.org/abs/2512.18938) A Framework for Deploying Learning-based Quadruped Loco-Manipulation
- Locator: 4.1.3 MuJoCo (tuned friction)
- Evidence: The cross-simulator study attributes apparently improved MuJoCo results to contact-parameter tuning rather than policy quality.
- Quote: “When evaluated with artificially enlarged impulse ratio ( impratio=100 ), sliding was nearly eliminated and the neutral/stop phases reached near-zero error ( Table ˜ 2 ). This confirms that apparent smoothness reflects traction tuning rather than intrinsic robustness.”
- Authors: yadong-liu; jianwei-liu; he-liang; et al.

## References

- `2507.21796` [MoDeSuite: Robot Learning Task Suite for Benchmarking Mobile Manipulation with Deformable Objects](https://arxiv.org/abs/2507.21796) (2025-07-29T13:33:43Z)
- `2508.10538` [MLM: Learning Multi-task Loco-Manipulation Whole-Body Control for Quadruped Robot with Arm](https://arxiv.org/abs/2508.10538) (2025-08-14T11:18:32Z)
- `2508.14099` [Task and Motion Planning for Humanoid Loco-manipulation](https://arxiv.org/abs/2508.14099) (2025-08-16T06:45:32Z)
- `2508.15663` [Mind and Motion Aligned: A Joint Evaluation IsaacSim Benchmark for Task Planning and Low-Level Policies in Mobile Manipulation](https://arxiv.org/abs/2508.15663) (2025-08-21T15:48:51Z)
- `2509.13534` [Embracing Bulky Objects with Humanoid Robots: Whole-Body Manipulation with Reinforcement Learning](https://arxiv.org/abs/2509.13534) (2025-09-16T21:01:24Z)
- `2512.11047` [WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control](https://arxiv.org/abs/2512.11047) (2025-12-11T19:07:31Z)
- `2512.18938` [A Framework for Deploying Learning-based Quadruped Loco-Manipulation](https://arxiv.org/abs/2512.18938) (2025-12-22T01:19:26Z)
- `2602.06643` [Humanoid Manipulation Interface: Humanoid Whole-Body Manipulation from Robot-Free Demonstrations](https://arxiv.org/abs/2602.06643) (2026-02-06T12:10:47Z)
- `2602.10106` [EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration](https://arxiv.org/abs/2602.10106) (2026-02-10T18:59:03Z)
- `2603.03279` [ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation](https://arxiv.org/abs/2603.03279) (2026-03-03T18:59:29Z)
- `2603.04579` [Risk-Aware Reinforcement Learning for Mobile Manipulation](https://arxiv.org/abs/2603.04579) (2026-03-04T20:17:28Z)
- `2604.08508` [Sumo: Dynamic and Generalizable Whole-Body Loco-Manipulation](https://arxiv.org/abs/2604.08508) (2026-04-09T17:49:40Z)
- `2604.12509` [Whole-Body Mobile Manipulation using Offline Reinforcement Learning on Sub-optimal Controllers](https://arxiv.org/abs/2604.12509) (2026-04-14T09:32:24Z)
- `2604.27224` [Learning Tactile-Aware Quadrupedal Loco-Manipulation Policies](https://arxiv.org/abs/2604.27224) (2026-04-29T21:46:58Z)
- `2605.27724` [HumanoidMimicGen: Data Generation for Loco-Manipulation via Whole-Body Planning](https://arxiv.org/abs/2605.27724) (2026-05-26T21:57:11Z)
- `2605.31343` [Learning Terrain-Aware Whole-Body Control for Perceptive Legged Loco-Manipulation](https://arxiv.org/abs/2605.31343) (2026-05-29T14:22:10Z)
- `2606.08278` [SIMPLE: Simulation-Based Policy Learning and Evaluation for Humanoid Loco-manipulation](https://arxiv.org/abs/2606.08278) (2026-06-06T17:55:43Z)
- `2606.12956` [SERF: Spatiotemporal Environment and Robot Feature Map for Long-Horizon Mobile Manipulation](https://arxiv.org/abs/2606.12956) (2026-06-11T06:29:49Z)
- `2606.22174` [OpenHLM: An Empirical Recipe for Whole-Body Humanoid Loco-Manipulation](https://arxiv.org/abs/2606.22174) (2026-06-20T18:02:50Z)
- `2606.24466` [FT-WBC: Learning Fault-Tolerant Whole-Body Control for Legged Loco-Manipulation](https://arxiv.org/abs/2606.24466) (2026-06-23T11:58:45Z)
- `2607.10132` [TAC-LOCO: Unified Whole-Body Control for Quadrupedal TACtile-Informed LOCO-Manipulation](https://arxiv.org/abs/2607.10132) (2026-07-11T05:45:24Z)
