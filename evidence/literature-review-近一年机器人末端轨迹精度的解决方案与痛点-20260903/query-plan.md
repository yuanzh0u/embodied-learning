# Query Plan: 近一年机器人末端轨迹精度的解决方案与痛点

## Scope

- Knowledge IDs: EA-MODEL, EA-SENSOR, EA-EVAL, EA-BIZ
- Families: last-centimeter, industrial-deployment, sim2real
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 200
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-trajectory-tracking-control | dynamic-direct | `all:"trajectory tracking" AND all:robot` | 末端轨迹精度的直接文献用语是 trajectory tracking，控制类论文标题高频。 |
| dynamic-end-effector-accuracy | dynamic-direct | `all:"end-effector" AND all:accuracy` | 直接命中以末端执行器精度为题的论文。 |
| dynamic-positioning-accuracy-compensation | dynamic-direct | `all:"positioning accuracy" AND all:compensation AND all:robot` | 工业机器人绝对定位精度补偿是解决方案主文献线。 |
| dynamic-kinematic-calibration | dynamic-mechanism | `all:"kinematic calibration" AND all:robot` | 运动学标定是提升末端精度的经典机制层方案。 |
| dynamic-dynamic-parameter-identification | dynamic-mechanism | `all:"dynamic parameter identification" AND all:robot` | 动力学参数辨识支撑模型基控制补偿。 |
| dynamic-friction-compensation | dynamic-mechanism | `all:"friction compensation" AND all:robot` | 摩擦是轨迹跟踪误差的高频来源，补偿文献密集。 |
| dynamic-mpc-robot | dynamic-mechanism | `all:"model predictive control" AND all:manipulator` | MPC 是近年轨迹级精度控制主流方案之一。 |
| dynamic-disturbance-observer | dynamic-mechanism | `all:"disturbance observer" AND all:robot AND all:manipulator` | 扰动观测器针对未建模动态造成的跟踪误差。 |
| dynamic-iterative-learning-control | dynamic-mechanism | `all:"iterative learning control" AND all:robot` | ILC 面向重复轨迹任务消除跟踪误差。 |
| dynamic-residual-dynamics-learning | dynamic-mechanism | `all:"residual dynamics" AND all:learning AND all:robot` | 学习残差动力学再叠加模型控制是近年混合方案主线。 |
| dynamic-vibration-suppression | dynamic-mechanism | `all:"vibration suppression" AND all:robot` | 柔性/振动直接破坏末端轨迹精度。 |
| elastic-joint-control | dynamic-mechanism | `all:"elastic joints" AND all:manipulator` | 谐波减速器弹性关节是跟踪误差的机制层痛点。 |
| dynamic-learning-tracking-error | dynamic-limit | `all:"tracking error" AND all:"neural network" AND all:robot` | 学习法消除跟踪误差的论文与痛点的实证来源。 |
| dynamic-action-chunking-smoothness | dynamic-limit | `all:"action chunking" AND (all:smooth OR all:jerk OR all:oscillation)` | VLA/ACT 动作分块带来的末端抖动是学习侧轨迹精度痛点。 |
| dynamic-lowlevel-control-vla | dynamic-adjacent | `all:"low-level control" AND (all:"vision-language-action" OR all:VLA)` | VLA 与底层轨迹控制器的接口是近年精度讨论热点。 |
| dynamic-diffusion-policy-tracking | dynamic-adjacent | `all:"diffusion policy" AND all:tracking` | 扩散策略输出轨迹与跟踪控制器组合的精度证据。 |
| dynamic-whole-body-control | dynamic-adjacent | `all:"whole-body control" AND (all:humanoid OR all:manipulator)` | 全身控制把任务空间轨迹精度下沉到全身关节。 |
| dynamic-visual-servoing-precision | dynamic-deployment | `all:"visual servoing" AND all:precision` | 视觉伺服用感知闭环补偿末端轨迹偏差。 |
| dynamic-iso9283-path-accuracy | dynamic-evaluation | `all:ISO AND all:9283` | ISO 9283 规定轨迹精度/重复性的评测口径。 |
| dynamic-sim2real-tracking | dynamic-evaluation | `all:"sim-to-real" AND all:"tracking control" AND all:robot` | sim-to-real 控制差距以跟踪精度为度量的证据。 |
| dynamic-backlash-gear | dynamic-limit | `all:backlash AND all:robot AND all:joint` | 传动间隙是精度痛点的硬件层语言。 |
| dynamic-rl-tracking-control | dynamic-adjacent | `all:"reinforcement learning" AND all:"tracking control" AND all:robot` | RL 直接学习跟踪控制器近年证据线。 |
| last-centimeter-exact | core | `all:"last centimeter" AND all:robot` | Catch papers that explicitly name the deployment bottleneck. |
| last-centimeter-visual-servoing | pre-contact | `all:"visual servoing" AND all:"robot manipulation"` | Find close-range pose correction before contact closure. |
| last-centimeter-force-insertion | contact | `all:"force control" AND all:insertion AND all:robot` | Surface insertion and compliant-contact methods for final alignment. |
| last-centimeter-failure-recovery | recovery | `all:"failure recovery" AND all:"robot manipulation"` | Find retry, recovery, and takeover strategies after near-goal failures. |
| last-centimeter-fixture | deployment-adjacent | `(all:fixture OR all:fixturing) AND all:robot AND all:insertion` | Capture fixture and workcell design that reduces contact uncertainty. |
| industrial-deployment-core | core | `all:"industrial robot" AND all:deployment` | Find deployment papers in manufacturing or production contexts. |
| industrial-deployment-reliability | reliability | `all:reliability AND all:robot AND all:deployment` | Capture uptime, fault tolerance, and long-run operational evidence. |
| industrial-deployment-cycle-time | production | `all:"cycle time" AND all:automation AND all:robot` | Find throughput constraints that affect ToB feasibility. |
| industrial-deployment-yield | production-quality | `all:yield AND all:robot AND all:manufacturing` | Surface quality and yield discussions beyond one-off success rate. |
| industrial-deployment-acceptance-testing | evaluation | `all:"acceptance testing" AND all:robot` | Find validation and acceptance language for production handoff. |
| industrial-deployment-roi | business-adjacent | `all:ROI AND all:robot AND all:automation` | Search for cost or return-on-investment framing when present in technical metadata. |
| sim2real-core | core | `(all:sim2real OR all:"sim-to-real") AND all:robot` | Find the main simulation-to-real transfer literature surface. |
| sim2real-real-validation | validation | `all:"real robot" AND all:validation AND all:simulation` | Find papers that verify simulation claims against real robot runs. |
| sim2real-synthetic-data | data-generation | `all:"synthetic data" AND all:"robot manipulation"` | Capture synthetic-data pipelines used to reduce real collection cost. |
| sim2real-domain-randomization | method | `all:"domain randomization" AND all:"robot manipulation"` | Find robustification methods for visual and physical sim-to-real gaps. |
| sim2real-correlation | evaluation | `all:"sim-real" AND all:correlation AND all:evaluation` | Surface work that measures whether simulation rankings predict real performance. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-trajectory-tracking-control, dynamic-end-effector-accuracy, dynamic-positioning-accuracy-compensation, dynamic-kinematic-calibration, dynamic-dynamic-parameter-identification, dynamic-friction-compensation, dynamic-mpc-robot, dynamic-disturbance-observer, dynamic-iterative-learning-control, dynamic-residual-dynamics-learning, dynamic-vibration-suppression, elastic-joint-control, dynamic-lowlevel-control-vla, dynamic-diffusion-policy-tracking, dynamic-whole-body-control, dynamic-rl-tracking-control, last-centimeter-visual-servoing, last-centimeter-force-insertion, industrial-deployment-reliability, sim2real-synthetic-data, ea-model-finetuning, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-eval-world-model |
| limits-and-counterevidence | 3 | dynamic-learning-tracking-error, dynamic-action-chunking-smoothness, dynamic-backlash-gear, ea-sensor-occlusion |
| deployment-and-operations | 3 | dynamic-visual-servoing-precision, last-centimeter-failure-recovery, last-centimeter-fixture, industrial-deployment-cycle-time, industrial-deployment-yield, industrial-deployment-roi |
| evaluation-and-validation | 3 | dynamic-iso9283-path-accuracy, dynamic-sim2real-tracking, industrial-deployment-acceptance-testing, sim2real-real-validation, sim2real-correlation, ea-eval-open-loop-benchmark, ea-eval-sim-real-correlation |
| direct-topic | 3 | last-centimeter-exact, industrial-deployment-core, sim2real-core, ea-model-vla, ea-model-named-foundation, ea-sensor-multimodal-policy, ea-eval-closed-loop |
| mechanisms-and-interfaces | 3 | sim2real-domain-randomization, ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-trajectory-precision-browser | `robot end-effector trajectory accuracy solutions 2026` | 检查 arXiv 元数据之外是否有工业侧讨论。 |
| dynamic-vla-jitter-browser | `VLA action chunking jitter smoothing low-level control 2026` | 学习侧末端抖动痛点的社区讨论校准。 |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-trajectory-accuracy-terms | llm | `"trajectory tracking accuracy" robot manipulator compensation survey` | 校准轨迹精度领域当前术语。 |
| dynamic-absolute-accuracy-repeatability | llm | `industrial robot "absolute accuracy" repeatability gap` | 确认绝对精度 vs 重复性术语仍在使用。 |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-trajectory-tracking-control | arxiv_api | llm | high | `all:"trajectory tracking" AND all:robot` | 末端轨迹精度的直接文献用语是 trajectory tracking，控制类论文标题高频。 |
| dynamic-end-effector-accuracy | arxiv_api | llm | high | `all:"end-effector" AND all:accuracy` | 直接命中以末端执行器精度为题的论文。 |
| dynamic-positioning-accuracy-compensation | arxiv_api | llm | high | `all:"positioning accuracy" AND all:compensation AND all:robot` | 工业机器人绝对定位精度补偿是解决方案主文献线。 |
| dynamic-kinematic-calibration | arxiv_api | llm | high | `all:"kinematic calibration" AND all:robot` | 运动学标定是提升末端精度的经典机制层方案。 |
| dynamic-dynamic-parameter-identification | arxiv_api | llm | high | `all:"dynamic parameter identification" AND all:robot` | 动力学参数辨识支撑模型基控制补偿。 |
| dynamic-friction-compensation | arxiv_api | llm | high | `all:"friction compensation" AND all:robot` | 摩擦是轨迹跟踪误差的高频来源，补偿文献密集。 |
| dynamic-mpc-robot | arxiv_api | llm | high | `all:"model predictive control" AND all:manipulator` | MPC 是近年轨迹级精度控制主流方案之一。 |
| dynamic-disturbance-observer | arxiv_api | llm | medium | `all:"disturbance observer" AND all:robot AND all:manipulator` | 扰动观测器针对未建模动态造成的跟踪误差。 |
| dynamic-iterative-learning-control | arxiv_api | llm | high | `all:"iterative learning control" AND all:robot` | ILC 面向重复轨迹任务消除跟踪误差。 |
| dynamic-residual-dynamics-learning | arxiv_api | llm | high | `all:"residual dynamics" AND all:learning AND all:robot` | 学习残差动力学再叠加模型控制是近年混合方案主线。 |
| dynamic-vibration-suppression | arxiv_api | llm | high | `all:"vibration suppression" AND all:robot` | 柔性/振动直接破坏末端轨迹精度。 |
| elastic-joint-control | arxiv_api | llm | medium | `all:"elastic joints" AND all:manipulator` | 谐波减速器弹性关节是跟踪误差的机制层痛点。 |
| dynamic-learning-tracking-error | arxiv_api | llm | medium | `all:"tracking error" AND all:"neural network" AND all:robot` | 学习法消除跟踪误差的论文与痛点的实证来源。 |
| dynamic-action-chunking-smoothness | arxiv_api | llm | high | `all:"action chunking" AND (all:smooth OR all:jerk OR all:oscillation)` | VLA/ACT 动作分块带来的末端抖动是学习侧轨迹精度痛点。 |
| dynamic-lowlevel-control-vla | arxiv_api | llm | high | `all:"low-level control" AND (all:"vision-language-action" OR all:VLA)` | VLA 与底层轨迹控制器的接口是近年精度讨论热点。 |
| dynamic-diffusion-policy-tracking | arxiv_api | llm | medium | `all:"diffusion policy" AND all:tracking` | 扩散策略输出轨迹与跟踪控制器组合的精度证据。 |
| dynamic-whole-body-control | arxiv_api | llm | medium | `all:"whole-body control" AND (all:humanoid OR all:manipulator)` | 全身控制把任务空间轨迹精度下沉到全身关节。 |
| dynamic-visual-servoing-precision | arxiv_api | llm | medium | `all:"visual servoing" AND all:precision` | 视觉伺服用感知闭环补偿末端轨迹偏差。 |
| dynamic-iso9283-path-accuracy | arxiv_api | llm | medium | `all:ISO AND all:9283` | ISO 9283 规定轨迹精度/重复性的评测口径。 |
| dynamic-sim2real-tracking | arxiv_api | llm | medium | `all:"sim-to-real" AND all:"tracking control" AND all:robot` | sim-to-real 控制差距以跟踪精度为度量的证据。 |
| dynamic-backlash-gear | arxiv_api | llm | medium | `all:backlash AND all:robot AND all:joint` | 传动间隙是精度痛点的硬件层语言。 |
| dynamic-rl-tracking-control | arxiv_api | llm | medium | `all:"reinforcement learning" AND all:"tracking control" AND all:robot` | RL 直接学习跟踪控制器近年证据线。 |
| dynamic-trajectory-precision-browser | browser_fallback | llm | low | `robot end-effector trajectory accuracy solutions 2026` | 检查 arXiv 元数据之外是否有工业侧讨论。 |
| dynamic-vla-jitter-browser | browser_fallback | llm | low | `VLA action chunking jitter smoothing low-level control 2026` | 学习侧末端抖动痛点的社区讨论校准。 |
| dynamic-trajectory-accuracy-terms | web_calibration | llm | medium | `"trajectory tracking accuracy" robot manipulator compensation survey` | 校准轨迹精度领域当前术语。 |
| dynamic-absolute-accuracy-repeatability | web_calibration | llm | medium | `industrial robot "absolute accuracy" repeatability gap` | 确认绝对精度 vs 重复性术语仍在使用。 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (medium): 末端轨迹精度是控制/标定/学习三条线的交叉词，静态分类法（last-centimeter 偏最后接近段）覆盖不足；Agent 依据机器人学控制文献常规术语推断动态扩展。
