# Query Plan: 具身智能数据质量的主要矛盾

## Scope

- Knowledge IDs: EA-DATA, EA-SENSOR, EA-HARDWARE, EA-XEMBODIMENT, EA-MODEL, EA-EVAL
- Families: teleoperation-demo-quality, vla, sim2real, world-model, tactile-force, retargeting
- Suggested categories: cs.AI, cs.CV, cs.HC, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 200
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-robot-data-quality | quality | `all:"robot data quality" OR all:"robotics data quality"` | 直接覆盖数据质量命名。 |
| dynamic-robot-data-curation | quality | `all:robot AND (all:"data curation" OR all:"data selection" OR all:"influence function")` | 覆盖训练效用与数据选择机制。 |
| dynamic-demonstration-assessment | evaluation | `all:"robot demonstration" AND (all:quality OR all:assessment OR all:feedback)` | 覆盖示教质量和采集反馈。 |
| dynamic-failure-recovery-data | limitation | `all:robot AND (all:"failure recovery" OR all:near-miss OR all:intervention) AND (all:data OR all:demonstration)` | 覆盖失败、接管和恢复样本。 |
| dynamic-supervision-reliability | limitation | `all:"robot learning" AND (all:"weak supervision" OR all:"noisy demonstrations" OR all:"suboptimal data")` | 覆盖异构监督与次优数据边界。 |
| teleop-imitation-learning | core | `all:teleoperation AND all:"imitation learning" AND all:robot` | Find the main literature surface connecting teleoperation to robot policy learning. |
| teleop-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface trace consistency, operator skill, and data acceptance criteria. |
| teleop-operator-burden | human-factor | `all:operator AND all:burden AND all:teleoperation` | Find papers about human workload and collection throughput. |
| teleop-latency | system-limitation | `all:latency AND all:teleoperation AND all:robot` | Capture delay and synchronization limits that affect demonstration fidelity. |
| teleop-action-interface | policy-interface | `all:"action interface" AND all:robot AND all:demonstration` | Find work where action-space choices determine whether demonstrations transfer. |
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |
| vla-large-scale-robot-data | data-scaling | `all:"large-scale" AND all:"robot data"` | Surface scaling and dataset-layer discussions for robot foundation models. |
| vla-robot-foundation-action | foundation-model | `all:"robot foundation model" AND all:action` | Find broader foundation-model papers whose metadata may not use VLA. |
| vla-finetuning-policy | transfer | `all:"fine-tuning" AND all:"robot policy"` | Surface evidence about target-task adaptation and data requirements. |
| vla-data-mixture | data-mixture | `all:"data mixture" AND all:"robot foundation model"` | Find mixture and dataset composition papers that explain scaling behavior. |
| vla-negative-transfer | limitation | `all:"negative transfer" AND all:robot AND all:policy` | Search for failure cases where broad pretraining hurts target deployment. |
| sim2real-core | core | `(all:sim2real OR all:"sim-to-real") AND all:robot` | Find the main simulation-to-real transfer literature surface. |
| sim2real-real-validation | validation | `all:"real robot" AND all:validation AND all:simulation` | Find papers that verify simulation claims against real robot runs. |
| sim2real-synthetic-data | data-generation | `all:"synthetic data" AND all:"robot manipulation"` | Capture synthetic-data pipelines used to reduce real collection cost. |
| sim2real-domain-randomization | method | `all:"domain randomization" AND all:"robot manipulation"` | Find robustification methods for visual and physical sim-to-real gaps. |
| sim2real-correlation | evaluation | `all:"sim-real" AND all:correlation AND all:evaluation` | Surface work that measures whether simulation rankings predict real performance. |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| tactile-force-tactile-manipulation | core | `all:tactile AND all:"robot manipulation"` | Find tactile sensing papers tied to manipulation policies or control. |
| tactile-force-force-torque | force | `all:force AND all:torque AND all:robot` | Cover force/torque observability and low-dimensional contact feedback. |
| tactile-force-slip-detection | contact-state | `all:"slip detection" AND all:robot` | Find tactile and force cues for grasp stability and material interaction. |
| tactile-force-contact-rich | task-family | `all:"contact-rich" AND all:manipulation` | Surface high-contact tasks where vision-only policies often fail. |
| tactile-force-sensor-fusion | fusion | `all:"sensor fusion" AND all:tactile AND all:robot` | Find multimodal policies combining tactile, force, vision, or proprioception. |
| retargeting-robot-manipulation | core | `all:retargeting AND all:"robot manipulation"` | Find the broad retargeting literature for manipulation tasks. |
| retargeting-human-to-robot-mapping | transfer | `all:"human-to-robot" AND all:mapping` | Capture human motion or hand data mapped onto robot embodiments. |
| retargeting-dexterous-hand | embodiment | `all:"dexterous hand" AND all:retargeting` | Find fine-grained human hand to dexterous hand transfer papers. |
| retargeting-gripper-demonstration | embodiment | `all:gripper AND all:"human demonstration" AND all:robot` | Search for lower-DOF gripper abstractions of human demonstrations. |
| retargeting-morphology-gap | limitation | `all:"morphology gap" AND all:robot` | Find papers that name embodiment mismatch as a transfer limit. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-hardware-teleop-device | core | `all:teleoperation AND all:"data collection" AND all:robot` | Find hardware routes used to collect robot demonstrations. |
| ea-hardware-slam-demonstration | tracking | `all:SLAM AND all:"robot manipulation" AND all:demonstration` | Capture tracking and reconstruction limitations in collection devices. |
| ea-hardware-arkit-tracking | tracking | `all:ARKit AND all:robot AND all:tracking` | Find low-cost pose-tracking and VIO routes relevant to data capture. |
| ea-hardware-handheld-gripper | device-language | `(all:"handheld gripper" OR all:"hand-held gripper") AND all:robot` | Catch UMI-like collection devices that may not use UMI in metadata. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-robot-data-quality, dynamic-robot-data-curation, teleop-imitation-learning, teleop-demonstration-quality, vla-core, vla-named-models, sim2real-core, world-model-robot, tactile-force-tactile-manipulation, retargeting-robot-manipulation, ea-data-robot-demonstrations, ea-sensor-multimodal-policy, ea-hardware-teleop-device, ea-xembodiment-cross-embodiment |
| adjacent-and-transfer | 3 | dynamic-demonstration-assessment, teleop-operator-burden, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, sim2real-synthetic-data, sim2real-correlation, world-model-video-prediction, world-model-planning, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, retargeting-human-to-robot-mapping, retargeting-dexterous-hand, retargeting-gripper-demonstration, ea-data-in-the-wild, ea-data-dataset-curation, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-hardware-slam-demonstration, ea-hardware-arkit-tracking, ea-hardware-handheld-gripper |
| limits-and-counterevidence | 3 | dynamic-failure-recovery-data, dynamic-supervision-reliability, teleop-latency, vla-negative-transfer, world-model-contact, world-model-long-horizon, retargeting-morphology-gap, ea-sensor-occlusion |
| mechanisms-and-interfaces | 3 | teleop-action-interface, sim2real-domain-randomization |
| evaluation-and-validation | 3 | sim2real-real-validation |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-topic-calibration | web | `"具身智能数据质量的主要矛盾" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-robot-data-quality | arxiv_api | llm | medium | `all:"robot data quality" OR all:"robotics data quality"` | 直接覆盖数据质量命名。 |
| dynamic-robot-data-curation | arxiv_api | llm | medium | `all:robot AND (all:"data curation" OR all:"data selection" OR all:"influence function")` | 覆盖训练效用与数据选择机制。 |
| dynamic-demonstration-assessment | arxiv_api | llm | medium | `all:"robot demonstration" AND (all:quality OR all:assessment OR all:feedback)` | 覆盖示教质量和采集反馈。 |
| dynamic-failure-recovery-data | arxiv_api | llm | medium | `all:robot AND (all:"failure recovery" OR all:near-miss OR all:intervention) AND (all:data OR all:demonstration)` | 覆盖失败、接管和恢复样本。 |
| dynamic-supervision-reliability | arxiv_api | llm | medium | `all:"robot learning" AND (all:"weak supervision" OR all:"noisy demonstrations" OR all:"suboptimal data")` | 覆盖异构监督与次优数据边界。 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (medium): 把数据质量从静态清洁度扩展到目标效用、覆盖、失败恢复和监督可靠性。
