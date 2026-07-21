# Query Plan: 近半年力觉在具身机器人领域的发展

## Scope

- Knowledge IDs: EA-SENSOR, EA-EVAL
- Families: tactile-force, last-centimeter, industrial-deployment
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 128
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-force-torque-manipulation | dynamic-direct | `(all:"force torque" OR all:"force/torque") AND (all:robot OR all:robotic) AND (all:manipulation OR all:policy)` | 覆盖腕部六轴力/力矩传感器进入机器人操作策略的直接工作。 |
| dynamic-force-aware-policy-learning | dynamic-mechanism | `(all:"force-aware" OR all:"force-guided" OR all:"force-conditioned") AND (all:robot OR all:manipulation)` | 覆盖力觉作为策略条件、反馈或表征的学习方法。 |
| dynamic-visual-force-fusion | dynamic-mechanism | `(all:"visual force" OR all:"vision force" OR all:"visuo-force") AND (all:robot OR all:manipulation)` | 覆盖视觉与力觉融合，以及视觉不可观测接触状态的补充。 |
| dynamic-contact-force-estimation | dynamic-mechanism | `(all:"contact force estimation" OR all:"force estimation") AND (all:robot OR all:robotic) AND (all:contact OR all:tactile)` | 覆盖从触觉、视觉或本体信号估计接触力的工作。 |
| dynamic-joint-torque-contact | dynamic-adjacent | `(all:"joint torque" OR all:"motor current") AND (all:"contact detection" OR all:"contact estimation") AND all:robot` | 覆盖无外置六轴传感器的关节力矩/电流接触感知路线。 |
| dynamic-force-controlled-insertion-learning | dynamic-deployment | `(all:"force control" OR all:"force-controlled") AND (all:insertion OR all:assembly) AND (all:learning OR all:policy)` | 覆盖装配、插入等最后一厘米任务中的学习型力控。 |
| dynamic-force-safety-failure | dynamic-limitation | `(all:force OR all:wrench) AND (all:"robot manipulation" OR all:"contact-rich") AND (all:failure OR all:safety OR all:uncertainty)` | 补充力觉在过力、碰撞、安全和不确定性方面的负面与边界证据。 |
| dynamic-whole-body-force-feedback | dynamic-adjacent | `(all:"whole-body" OR all:humanoid OR all:quadruped) AND (all:"force feedback" OR all:"contact feedback" OR all:tactile) AND all:robot` | 覆盖力觉从末端操作扩展为全身接触与稳定控制变量的工作。 |
| tactile-force-tactile-manipulation | core | `all:tactile AND all:"robot manipulation"` | Find tactile sensing papers tied to manipulation policies or control. |
| tactile-force-force-torque | force | `all:force AND all:torque AND all:robot` | Cover force/torque observability and low-dimensional contact feedback. |
| tactile-force-slip-detection | contact-state | `all:"slip detection" AND all:robot` | Find tactile and force cues for grasp stability and material interaction. |
| tactile-force-contact-rich | task-family | `all:"contact-rich" AND all:manipulation` | Surface high-contact tasks where vision-only policies often fail. |
| tactile-force-sensor-fusion | fusion | `all:"sensor fusion" AND all:tactile AND all:robot` | Find multimodal policies combining tactile, force, vision, or proprioception. |
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
| adjacent-and-transfer | 3 | dynamic-force-torque-manipulation, dynamic-force-aware-policy-learning, dynamic-visual-force-fusion, dynamic-contact-force-estimation, dynamic-joint-torque-contact, dynamic-whole-body-force-feedback, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, last-centimeter-visual-servoing, last-centimeter-force-insertion, industrial-deployment-acceptance-testing, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| deployment-and-operations | 3 | dynamic-force-controlled-insertion-learning, last-centimeter-failure-recovery, last-centimeter-fixture, industrial-deployment-reliability, industrial-deployment-cycle-time, industrial-deployment-yield, industrial-deployment-roi |
| limits-and-counterevidence | 3 | dynamic-force-safety-failure, ea-sensor-occlusion |
| direct-topic | 3 | tactile-force-tactile-manipulation, last-centimeter-exact, industrial-deployment-core, ea-sensor-multimodal-policy, ea-eval-closed-loop |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-force-sense-browser | `site:arxiv.org 2026 robot force torque force-aware manipulation policy` | API 欠召回时补充力觉策略论文。 |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-force-sense-calibration | llm | `2026 embodied robot force sensing force torque tactile policy` | 校准近半年新方法名和术语。 |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-force-torque-manipulation | arxiv_api | llm | high | `(all:"force torque" OR all:"force/torque") AND (all:robot OR all:robotic) AND (all:manipulation OR all:policy)` | 覆盖腕部六轴力/力矩传感器进入机器人操作策略的直接工作。 |
| dynamic-force-aware-policy-learning | arxiv_api | llm | high | `(all:"force-aware" OR all:"force-guided" OR all:"force-conditioned") AND (all:robot OR all:manipulation)` | 覆盖力觉作为策略条件、反馈或表征的学习方法。 |
| dynamic-visual-force-fusion | arxiv_api | llm | high | `(all:"visual force" OR all:"vision force" OR all:"visuo-force") AND (all:robot OR all:manipulation)` | 覆盖视觉与力觉融合，以及视觉不可观测接触状态的补充。 |
| dynamic-contact-force-estimation | arxiv_api | llm | high | `(all:"contact force estimation" OR all:"force estimation") AND (all:robot OR all:robotic) AND (all:contact OR all:tactile)` | 覆盖从触觉、视觉或本体信号估计接触力的工作。 |
| dynamic-joint-torque-contact | arxiv_api | llm | medium | `(all:"joint torque" OR all:"motor current") AND (all:"contact detection" OR all:"contact estimation") AND all:robot` | 覆盖无外置六轴传感器的关节力矩/电流接触感知路线。 |
| dynamic-force-controlled-insertion-learning | arxiv_api | llm | high | `(all:"force control" OR all:"force-controlled") AND (all:insertion OR all:assembly) AND (all:learning OR all:policy)` | 覆盖装配、插入等最后一厘米任务中的学习型力控。 |
| dynamic-force-safety-failure | arxiv_api | llm | high | `(all:force OR all:wrench) AND (all:"robot manipulation" OR all:"contact-rich") AND (all:failure OR all:safety OR all:uncertainty)` | 补充力觉在过力、碰撞、安全和不确定性方面的负面与边界证据。 |
| dynamic-whole-body-force-feedback | arxiv_api | llm | medium | `(all:"whole-body" OR all:humanoid OR all:quadruped) AND (all:"force feedback" OR all:"contact feedback" OR all:tactile) AND all:robot` | 覆盖力觉从末端操作扩展为全身接触与稳定控制变量的工作。 |
| dynamic-force-sense-browser | browser_fallback | llm | medium | `site:arxiv.org 2026 robot force torque force-aware manipulation policy` | API 欠召回时补充力觉策略论文。 |
| dynamic-force-sense-calibration | web_calibration | llm | medium | `2026 embodied robot force sensing force torque tactile policy` | 校准近半年新方法名和术语。 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (high): 将中文‘力觉’拆分为六轴力/力矩、关节力矩/本体接触、触觉阵列的力分布估计，以及力信号进入策略、世界模型和闭环控制四个检索面。
