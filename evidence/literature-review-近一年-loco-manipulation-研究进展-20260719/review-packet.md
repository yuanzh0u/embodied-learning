# Review Packet: 近一年 loco-manipulation 研究进展

## Scope

- Topic: 近一年 loco-manipulation 研究进展
- Time range: 2025-07-19 至 2026-07-19
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-XEMBODIMENT`, `EA-SENSOR`
- Evidence events: 21
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 21
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-LOCOMANIP-2026-0005`, `EA-LOCOMANIP-2026-0006`, `EA-LOCOMANIP-2026-0008`, `EA-LOCOMANIP-2026-0009`, `EA-LOCOMANIP-2026-0019`, `EA-LOCOMANIP-2026-0011`, `EA-LOCOMANIP-2026-0012`, `EA-LOCOMANIP-2026-0013`, `EA-LOCOMANIP-2026-0014`, `EA-LOCOMANIP-2026-0020`, `EA-LOCOMANIP-2026-0021`, `EA-LOCOMANIP-2026-0002`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 21 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 21
- Structure mapped: 21
- Deep-read papers: 21
- Claim-verified papers: 21
- Accepted evidence papers: 21
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型后果预演、本体适配器与底层控制器组成的融合栈。Ego-centric 人类视频可扩展行为与视点先验，但只有经过动作恢复、本体对齐和目标机器人锚定后，才可能转成可执行控制。基础模型、适配模块与检查点还构成需要独立审计的供应链。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测还要审计训练—测试结构独立性，并把干净性能、触发/扰动风险、检测误报与恢复代价分开记录，防止记忆式高分或 episode 平均值掩盖动作窗风险。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- `EA-XEMBODIMENT` 跨本体与数据迁移: 跨本体迁移的核心不是复制姿态或控制命令，而是保留任务相关的状态变化与接触功能。人手数据映射到灵巧手或夹爪时，应优先抽象抓取意图、对象轨迹、接触区域和 affordance。不同机器人即使记录相同 action command，也可能产生不同运动；更稳健的路线是共享 Cartesian state delta、对象状态变化或接触目标，再由机器人特定 adapter 和真实闭环校准落地。
  - 灵巧手可保留指尖轨迹、掌心 pose、关键关节和接触关系，再做优化或学习式映射。
  - 双指夹爪应抽象抓取点、夹爪宽度、接近方向和物体接触区域。
  - 错误映射会让策略学到机器人不可执行或接触不稳定的动作。
  - 跨本体中间表征可包括物体轨迹、末端 6D pose、接触 patch、力闭合、skill token、latent action。
  - 动力学与触觉差异在真实接触任务中比运动学差异更容易造成长期失败。
- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。第一视角视频尤其要分开相机自运动、手物运动与主动视点动作；视觉定位也要把外观召回、几何可恢复性和拒识覆盖分账。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；触觉世界模型应预测动作条件下的接触演化，而不只是重建触觉图像。多模态建模的目标不是堆传感器，而是让每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 11 |
| `conditional` | 条件成立 | 7 |
| `limit` | 限制/负面 | 3 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2507.21796: MoDeSuite: Robot Learning Task Suite for Benchmarking Mobile Manipulation with Deformable Objects | 2025-07-29T13:33:43Z | limit | EA-LOCOMANIP-2026-0001 |
| 2508.10538: MLM: Learning Multi-task Loco-Manipulation Whole-Body Control for Quadruped Robot with Arm | 2025-08-14T11:18:32Z | conditional | EA-LOCOMANIP-2026-0002 |
| 2508.14099: Task and Motion Planning for Humanoid Loco-manipulation | 2025-08-16T06:45:32Z | conditional | EA-LOCOMANIP-2026-0003 |
| 2508.15663: Mind and Motion Aligned: A Joint Evaluation IsaacSim Benchmark for Task Planning and Low-Level Policies in Mobile Manip... | 2025-08-21T15:48:51Z | limit | EA-LOCOMANIP-2026-0004 |
| 2509.13534: Embracing Bulky Objects with Humanoid Robots: Whole-Body Manipulation with Reinforcement Learning | 2025-09-16T21:01:24Z | support | EA-LOCOMANIP-2026-0005 |
| 2512.11047: WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control | 2025-12-11T19:07:31Z | support | EA-LOCOMANIP-2026-0006 |
| 2512.18938: A Framework for Deploying Learning-based Quadruped Loco-Manipulation | 2025-12-22T01:19:26Z | limit | EA-LOCOMANIP-2026-0007 |
| 2602.06643: Humanoid Manipulation Interface: Humanoid Whole-Body Manipulation from Robot-Free Demonstrations | 2026-02-06T12:10:47Z | support | EA-LOCOMANIP-2026-0008 |
| 2602.10106: EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration | 2026-02-10T18:59:03Z | support | EA-LOCOMANIP-2026-0009 |
| 2603.03279: ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation | 2026-03-03T18:59:29Z | conditional | EA-LOCOMANIP-2026-0018 |
| 2603.04579: Risk-Aware Reinforcement Learning for Mobile Manipulation | 2026-03-04T20:17:28Z | conditional | EA-LOCOMANIP-2026-0010 |
| 2604.08508: Sumo: Dynamic and Generalizable Whole-Body Loco-Manipulation | 2026-04-09T17:49:40Z | support | EA-LOCOMANIP-2026-0019 |
| 2604.12509: Whole-Body Mobile Manipulation using Offline Reinforcement Learning on Sub-optimal Controllers | 2026-04-14T09:32:24Z | support | EA-LOCOMANIP-2026-0011 |
| 2604.27224: Learning Tactile-Aware Quadrupedal Loco-Manipulation Policies | 2026-04-29T21:46:58Z | support | EA-LOCOMANIP-2026-0012 |
| 2605.27724: HumanoidMimicGen: Data Generation for Loco-Manipulation via Whole-Body Planning | 2026-05-26T21:57:11Z | support | EA-LOCOMANIP-2026-0013 |
| 2605.31343: Learning Terrain-Aware Whole-Body Control for Perceptive Legged Loco-Manipulation | 2026-05-29T14:22:10Z | support | EA-LOCOMANIP-2026-0014 |
| 2606.08278: SIMPLE: Simulation-Based Policy Learning and Evaluation for Humanoid Loco-manipulation | 2026-06-06T17:55:43Z | conditional | EA-LOCOMANIP-2026-0015 |
| 2606.12956: SERF: Spatiotemporal Environment and Robot Feature Map for Long-Horizon Mobile Manipulation | 2026-06-11T06:29:49Z | conditional | EA-LOCOMANIP-2026-0016 |
| 2606.22174: OpenHLM: An Empirical Recipe for Whole-Body Humanoid Loco-Manipulation | 2026-06-20T18:02:50Z | support | EA-LOCOMANIP-2026-0020 |
| 2606.24466: FT-WBC: Learning Fault-Tolerant Whole-Body Control for Legged Loco-Manipulation | 2026-06-23T11:58:45Z | conditional | EA-LOCOMANIP-2026-0017 |
| 2607.10132: TAC-LOCO: Unified Whole-Body Control for Quadrupedal TACtile-Informed LOCO-Manipulation | 2026-07-11T05:45:24Z | support | EA-LOCOMANIP-2026-0021 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-LOCOMANIP-2026-0005 | EA-MODEL | `support` | `direct` | In simulation, the NSDF-conditioned policy maintained 100% success for standard-mass cylinders, cuboids and spheres, while removing NSDF produced 0% across those shapes. | The shape sweep directly contrasts the full method with the no-NSDF ablation. (IV-B Adaptability to Different Object Properties) | chunxin-zheng; kai-chen; zhihai-bi; et al. | 2509.13534 |
| EA-LOCOMANIP-2026-0006 | EA-MODEL | `support` | `direct` | Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the evaluated tasks. | The ablation directly compares the full model with removal of unified latent learning. (4.3 How does action-free videos contribute to loco–manipulation?) | haoran-jiang; jin-chen; qingwen-bu; et al. | 2512.11047 |
| EA-LOCOMANIP-2026-0008 | EA-MODEL | `support` | `direct` | In a 15-minute comparison, HuMI collected 62 episodes versus 28 for TWIST2, with 96.7% versus 64.3% acceptance; time per acceptable episode fell to 30.0% of TWIST2. | The timed comparison jointly reports quantity, quality and accepted-data cost. (VI Data Collection Efficiency) | ruiqian-nai; boyuan-zheng; junming-zhao; et al. | 2602.06643 |
| EA-LOCOMANIP-2026-0009 | EA-MODEL | `support` | `direct` | With 100 robot and 300 human demonstrations, co-training scored 78% versus 59% for robot-only in-domain, and 82% versus 31% under generalization. | The main comparison directly reports both in-domain and generalization gaps. (IV-B Will human data improve humanoid loco-manipulation?) | modi-shi; shijia-peng; jin-chen; et al. | 2602.10106 |
| EA-LOCOMANIP-2026-0019 | EA-MODEL | `support` | `direct` | On hardware, Sumo uprighted a 15 kg tire—heavier than Spot arm's stated 11 kg lifting capacity—in 10/10 trials, averaging 9.2±4.7 seconds. | The hardware case study reports object mass, nominal arm capacity, success and completion time. (page 8) | john-z-zhang; maks-sorokin; jan-brdigam; et al. | 2604.08508 |
| EA-LOCOMANIP-2026-0011 | EA-MODEL | `support` | `direct` | On real cupboard opening, WHOLE-MoMa succeeded in 17/25 trials (68%), versus 4/25 for its WBC generator and 8/25 for behavior cloning. | The real-world table separates full success across the three methods. (VI-B Real-World Results) | snehal-jauhri; vignesh-prasad; georgia-chalvatzaki | 2604.12509 |
| EA-LOCOMANIP-2026-0012 | EA-MODEL | `support` | `direct` | Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to... | The paper compares variants with the same tactile-aware high level but different low-level tactile tracking. (IV-B Experimental Results and Analyze) | pokuang-zhou; yuhao-zhou; quan-khanh-luu; et al. | 2604.27224 |
| EA-LOCOMANIP-2026-0013 | EA-MODEL | `support` | `direct` | Across nine simulated tasks, data generated from one source demonstration raised average policy performance from 0.33 for DexMimicGen+ to 0.89 for HumanoidMimicGen. | The main comparison reports downstream policy performance averaged over all nine tasks. (6.2 HumanoidMimicGen Capabilities) | kevin-lin; ajay-mandlekar; caelan-reed-garrett; et al. | 2605.27724 |
| EA-LOCOMANIP-2026-0014 | EA-MODEL | `support` | `direct` | In a staged real long-horizon task, TA-WBC completed five consecutive bottle-pick, stair-climb, disposal and return runs without falls or stumbles. | The real-world section explicitly reports repeated completion of the full multi-stage route. (IV-C 2 Long-Horizon Loco-Manipulation) | sikai-guo; yudong-zhong; guoyang-zhao; et al. | 2605.31343 |
| EA-LOCOMANIP-2026-0020 | EA-MODEL | `support` | `direct` | On four tasks held out from whole-body teleoperation, stationary same-embodiment co-training raised average task progress from 33% to 87%, close to a 94% 12-task teleoperation ora... | The paper overview reports the held-out-task gain and the full-teleoperation oracle. (1 Introduction) | yingdong-hu; haodong-zhu; boyuan-zheng; et al. | 2606.22174 |
| EA-LOCOMANIP-2026-0021 | EA-MODEL | `support` | `direct` | In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. | The hardware baseline comparison isolates learned grasp regulation under the same command set. (6.5 Baseline comparison) | muqun-hu; yuhao-zhou; kabir-ray-malik; et al. | 2607.10132 |
| EA-LOCOMANIP-2026-0002 | EA-MODEL | `conditional` | `direct` | On two real-world tasks, the same controller achieved 98% and 100% success under teleoperation, versus 80% and 85% when driven by a diffusion policy. | Table V directly separates low-level tracking results under teleoperation and diffusion-policy trajectory generation. (IV-C Real-world Experiments) | xin-liu; bida-ma; chenkun-qi; et al. | 2508.10538 |
| EA-LOCOMANIP-2026-0003 | EA-MODEL | `conditional` | `direct` | For two-box pick-and-place, the solver found the first goal-satisfying feasible plan after 30 of 200 tree expansions, with an average solve time of 52.3 seconds. | The example-solution section reports both search effort and computation for the modeled task. (IV-C Example Solutions) | michal-ciebielski; victor-dhdin; majid-khadiv | 2508.14099 |
| EA-LOCOMANIP-2026-0018 | EA-MODEL | `conditional` | `direct` | On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively. | The real-world table separates external-state and onboard egocentric control modes. (V-E Real-World Deployment) | xialin-he; sirui-xu; xinyao-li; et al. | 2603.03279 |
| EA-LOCOMANIP-2026-0010 | EA-MODEL | `conditional` | `direct` | The study reports a depth-only mobile-manipulation policy whose risk sensitivity can be adjusted at runtime while retaining task performance comparable to risk-neutral methods in... | The conclusion summarizes risk-aware student competence and transfer through imitation learning. (VI Conclusion) | michael-groom; james-wilson; nick-hawes; et al. | 2603.04579 |
| EA-LOCOMANIP-2026-0015 | EA-MODEL | `conditional` | `direct` | In zero-shot transfer, pick-and-place scored 9/10 in simulation and 8/10 on hardware; handover scored 10/10 in simulation and 8/10 on hardware. | The transfer table reports paired simulation and real success counts; in the recovered HTML it is attached to the parent experiments section. (4 Experiments) | songlin-wei; zhenhao-ni; jie-liu; et al. | 2606.08278 |
| EA-LOCOMANIP-2026-0016 | EA-MODEL | `conditional` | `direct` | Across three simulated BEHAVIOR-1K tasks, SERF achieved mean task progress of 63.5, 60.1 and 52.5, versus 40.7, 43.0 and 48.4 for the fine-tuned image-only PI0.5 baseline. | The main table reports mean task progress for the full system and image-only baseline across three tasks. (5 Long-Horizon Mobile Manipulation) | sunghwan-kim; byeonghyun-pak; kehan-long; et al. | 2606.12956 |
| EA-LOCOMANIP-2026-0017 | EA-MODEL | `conditional` | `direct` | Under an unseen locked-joint fault at the most demanding placement height, FT-WBC retained 70% survival but only 45% task success, reflecting an explicit survival-first posture po... | The real-world analysis directly attributes reduced completion to conservative posture limits that preserve the degraded support polygon. (4.3 Real-World Deployment) | yudong-zhong; pengfei-mai; sikai-guo; et al. | 2606.24466 |
| EA-LOCOMANIP-2026-0001 | EA-MODEL | `limit` | `direct` | On the real curtain task, neither image policy completed any of 10 trials; retrieval reached the curtain in 2/10, while behavior cloning did not reach it. | The deployment paragraph contrasts simulation success with physical failure. (IV-C Deployment on Real Robot) | yuying-zhang; kevin-sebastian-luck; francesco-verdoja; et al. | 2507.21796 |
| EA-LOCOMANIP-2026-0004 | EA-MODEL | `limit` | `direct` | Kitchen-R's reported execution evaluation always uses the ground-truth plan to isolate execution from planning error, so its module results are not direct evidence of end-to-end a... | The metrics section explicitly states that execution does not use the predicted plan. (IV METRICS) | nikita-kachaev; andrei-spiridonov; andrey-gorodetsky; et al. | 2508.15663 |
| EA-LOCOMANIP-2026-0007 | EA-MODEL | `limit` | `direct` | Cross-simulator smoothness was not a reliable robustness signal: MuJoCo drifted under default friction, while near-zero stop error under tuned friction came from unrealistically h... | The cross-simulator study attributes apparently improved MuJoCo results to contact-parameter tuning rather than policy quality. (4.1.3 MuJoCo (tuned friction)) | yadong-liu; jianwei-liu; he-liang; et al. | 2512.18938 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-LOCOMANIP-2026-0005 | chunxin-zheng; kai-chen; zhihai-bi; et al. | unlisted | `support` | In simulation, the NSDF-conditioned policy maintained 100% success for standard-mass cylinders, cuboids and spheres, while removing NSDF produced 0% across tho... |
| EA-LOCOMANIP-2026-0006 | haoran-jiang; jin-chen; qingwen-bu; et al. | unlisted | `support` | Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the ev... |
| EA-LOCOMANIP-2026-0008 | ruiqian-nai; boyuan-zheng; junming-zhao; et al. | unlisted | `support` | In a 15-minute comparison, HuMI collected 62 episodes versus 28 for TWIST2, with 96.7% versus 64.3% acceptance; time per acceptable episode fell to 30.0% of TW... |
| EA-LOCOMANIP-2026-0009 | modi-shi; shijia-peng; jin-chen; et al. | unlisted | `support` | With 100 robot and 300 human demonstrations, co-training scored 78% versus 59% for robot-only in-domain, and 82% versus 31% under generalization. |
| EA-LOCOMANIP-2026-0019 | john-z-zhang; maks-sorokin; jan-brdigam; et al. | unlisted | `support` | On hardware, Sumo uprighted a 15 kg tire—heavier than Spot arm's stated 11 kg lifting capacity—in 10/10 trials, averaging 9.2±4.7 seconds. |
| EA-LOCOMANIP-2026-0011 | snehal-jauhri; vignesh-prasad; georgia-chalvatzaki | unlisted | `support` | On real cupboard opening, WHOLE-MoMa succeeded in 17/25 trials (68%), versus 4/25 for its WBC generator and 8/25 for behavior cloning. |
| EA-LOCOMANIP-2026-0012 | pokuang-zhou; yuhao-zhou; quan-khanh-luu; et al. | unlisted | `support` | Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tig... |
| EA-LOCOMANIP-2026-0013 | kevin-lin; ajay-mandlekar; caelan-reed-garrett; et al. | unlisted | `support` | Across nine simulated tasks, data generated from one source demonstration raised average policy performance from 0.33 for DexMimicGen+ to 0.89 for HumanoidMimi... |
| EA-LOCOMANIP-2026-0014 | sikai-guo; yudong-zhong; guoyang-zhao; et al. | unlisted | `support` | In a staged real long-horizon task, TA-WBC completed five consecutive bottle-pick, stair-climb, disposal and return runs without falls or stumbles. |
| EA-LOCOMANIP-2026-0020 | yingdong-hu; haodong-zhu; boyuan-zheng; et al. | unlisted | `support` | On four tasks held out from whole-body teleoperation, stationary same-embodiment co-training raised average task progress from 33% to 87%, close to a 94% 12-ta... |
| EA-LOCOMANIP-2026-0021 | muqun-hu; yuhao-zhou; kabir-ray-malik; et al. | unlisted | `support` | In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. |
| EA-LOCOMANIP-2026-0002 | xin-liu; bida-ma; chenkun-qi; et al. | unlisted | `conditional` | On two real-world tasks, the same controller achieved 98% and 100% success under teleoperation, versus 80% and 85% when driven by a diffusion policy. |
| EA-LOCOMANIP-2026-0003 | michal-ciebielski; victor-dhdin; majid-khadiv | unlisted | `conditional` | For two-box pick-and-place, the solver found the first goal-satisfying feasible plan after 30 of 200 tree expansions, with an average solve time of 52.3 second... |
| EA-LOCOMANIP-2026-0018 | xialin-he; sirui-xu; xinyao-li; et al. | unlisted | `conditional` | On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively. |
| EA-LOCOMANIP-2026-0010 | michael-groom; james-wilson; nick-hawes; et al. | unlisted | `conditional` | The study reports a depth-only mobile-manipulation policy whose risk sensitivity can be adjusted at runtime while retaining task performance comparable to risk... |
| EA-LOCOMANIP-2026-0015 | songlin-wei; zhenhao-ni; jie-liu; et al. | unlisted | `conditional` | In zero-shot transfer, pick-and-place scored 9/10 in simulation and 8/10 on hardware; handover scored 10/10 in simulation and 8/10 on hardware. |
| EA-LOCOMANIP-2026-0016 | sunghwan-kim; byeonghyun-pak; kehan-long; et al. | unlisted | `conditional` | Across three simulated BEHAVIOR-1K tasks, SERF achieved mean task progress of 63.5, 60.1 and 52.5, versus 40.7, 43.0 and 48.4 for the fine-tuned image-only PI0... |
| EA-LOCOMANIP-2026-0017 | yudong-zhong; pengfei-mai; sikai-guo; et al. | unlisted | `conditional` | Under an unseen locked-joint fault at the most demanding placement height, FT-WBC retained 70% survival but only 45% task success, reflecting an explicit survi... |
| EA-LOCOMANIP-2026-0001 | yuying-zhang; kevin-sebastian-luck; francesco-verdoja; et al. | unlisted | `limit` | On the real curtain task, neither image policy completed any of 10 trials; retrieval reached the curtain in 2/10, while behavior cloning did not reach it. |
| EA-LOCOMANIP-2026-0004 | nikita-kachaev; andrei-spiridonov; andrey-gorodetsky; et al. | unlisted | `limit` | Kitchen-R's reported execution evaluation always uses the ground-truth plan to isolate execution from planning error, so its module results are not direct evid... |
| EA-LOCOMANIP-2026-0007 | yadong-liu; jianwei-liu; he-liang; et al. | unlisted | `limit` | Cross-simulator smoothness was not a reliable robustness signal: MuJoCo drifted under default friction, while near-zero stop error under tuned friction came fr... |

## Synthesis Slots

### 共识/正向证据
- `EA-LOCOMANIP-2026-0005`: In simulation, the NSDF-conditioned policy maintained 100% success for standard-mass cylinders, cuboids and spheres, while removing NSDF produced 0% across those shapes.
- `EA-LOCOMANIP-2026-0006`: Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the evaluated tasks.
- `EA-LOCOMANIP-2026-0008`: In a 15-minute comparison, HuMI collected 62 episodes versus 28 for TWIST2, with 96.7% versus 64.3% acceptance; time per acceptable episode fell to 30.0% of TWIST2.
- `EA-LOCOMANIP-2026-0009`: With 100 robot and 300 human demonstrations, co-training scored 78% versus 59% for robot-only in-domain, and 82% versus 31% under generalization.
- `EA-LOCOMANIP-2026-0019`: On hardware, Sumo uprighted a 15 kg tire—heavier than Spot arm's stated 11 kg lifting capacity—in 10/10 trials, averaging 9.2±4.7 seconds.
- `EA-LOCOMANIP-2026-0011`: On real cupboard opening, WHOLE-MoMa succeeded in 17/25 trials (68%), versus 4/25 for its WBC generator and 8/25 for behavior cloning.
- `EA-LOCOMANIP-2026-0012`: Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to 0.85.
- `EA-LOCOMANIP-2026-0013`: Across nine simulated tasks, data generated from one source demonstration raised average policy performance from 0.33 for DexMimicGen+ to 0.89 for HumanoidMimicGen.
### 条件成立
- `EA-LOCOMANIP-2026-0002`: On two real-world tasks, the same controller achieved 98% and 100% success under teleoperation, versus 80% and 85% when driven by a diffusion policy.
- `EA-LOCOMANIP-2026-0003`: For two-box pick-and-place, the solver found the first goal-satisfying feasible plan after 30 of 200 tree expansions, with an average solve time of 52.3 seconds.
- `EA-LOCOMANIP-2026-0018`: On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively.
- `EA-LOCOMANIP-2026-0010`: The study reports a depth-only mobile-manipulation policy whose risk sensitivity can be adjusted at runtime while retaining task performance comparable to risk-neutral methods in simulation.
- `EA-LOCOMANIP-2026-0015`: In zero-shot transfer, pick-and-place scored 9/10 in simulation and 8/10 on hardware; handover scored 10/10 in simulation and 8/10 on hardware.
- `EA-LOCOMANIP-2026-0016`: Across three simulated BEHAVIOR-1K tasks, SERF achieved mean task progress of 63.5, 60.1 and 52.5, versus 40.7, 43.0 and 48.4 for the fine-tuned image-only PI0.5 baseline.
- `EA-LOCOMANIP-2026-0017`: Under an unseen locked-joint fault at the most demanding placement height, FT-WBC retained 70% survival but only 45% task success, reflecting an explicit survival-first posture policy.
### 限制与失败模式
- `EA-LOCOMANIP-2026-0001`: On the real curtain task, neither image policy completed any of 10 trials; retrieval reached the curtain in 2/10, while behavior cloning did not reach it.
- `EA-LOCOMANIP-2026-0004`: Kitchen-R's reported execution evaluation always uses the ground-truth plan to isolate execution from planning error, so its module results are not direct evidence of end-to-end autonomy.
- `EA-LOCOMANIP-2026-0007`: Cross-simulator smoothness was not a reliable robustness signal: MuJoCo drifted under default friction, while near-zero stop error under tuned friction came from unrealistically high tangential impedance.

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 21 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-LOCOMANIP-2026-0005` In simulation, the NSDF-conditioned policy maintained 100% success for standard-mass cylinders, cuboids and spheres, while removing NSDF produced 0%...
  - `EA-LOCOMANIP-2026-0006` Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors...
  - `EA-LOCOMANIP-2026-0008` In a 15-minute comparison, HuMI collected 62 episodes versus 28 for TWIST2, with 96.7% versus 64.3% acceptance; time per acceptable episode fell to 3...
- Scientific memo preview: 《近一年 loco-manipulation 研究进展》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年 loco-manipulation 研究进展 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年 loco-manipulation 研究进展: 先看证据边界，再谈一个可传播的反常识洞察。

## Draft Outline

1. 研究边界与证据范围
2. 概念与问题结构
3. 主要共识
4. 条件、限制与分歧
5. 未解决问题
6. 对后续研究/项目的启发

## Traceability Checklist

- Cite event IDs for paper-specific claims.
- Cite stable source IDs for topic-card background.
- Mark cross-event synthesis as `inference` with a short reason.
- Do not cite candidate-only papers as accepted evidence.
- Open raw sources before using exact wording.
