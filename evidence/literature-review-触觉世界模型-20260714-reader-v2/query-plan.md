# Query Plan: 触觉世界模型

## Scope

- Knowledge IDs: EA-DATA, EA-EVAL, EA-MODEL, EA-SENSOR
- Families: tactile-force, world-model
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 120
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-visuotactile-world-model | core | `(all:"visuo-tactile" OR all:visuotactile) AND all:"world model" AND all:robot` | 直接覆盖视觉—触觉世界模型。 |
| dynamic-tactile-action-model | mechanism | `all:tactile AND (all:"world action model" OR all:"action-conditioned") AND all:robot` | 覆盖动作条件的触觉未来。 |
| dynamic-contact-prediction | mechanism | `all:"robot manipulation" AND (all:"contact prediction" OR all:"force prediction" OR all:"slip prediction")` | 覆盖接触状态和物理结果预测。 |
| dynamic-tactile-foundation | adjacent | `all:tactile AND (all:"foundation model" OR all:pretraining) AND all:robot` | 覆盖大规模触觉表征与迁移。 |
| tactile-force-tactile-manipulation | core | `all:tactile AND all:"robot manipulation"` | Find tactile sensing papers tied to manipulation policies or control. |
| tactile-force-force-torque | force | `all:force AND all:torque AND all:robot` | Cover force/torque observability and low-dimensional contact feedback. |
| tactile-force-slip-detection | contact-state | `all:"slip detection" AND all:robot` | Find tactile and force cues for grasp stability and material interaction. |
| tactile-force-contact-rich | task-family | `all:"contact-rich" AND all:manipulation` | Surface high-contact tasks where vision-only policies often fail. |
| tactile-force-sensor-fusion | fusion | `all:"sensor fusion" AND all:tactile AND all:robot` | Find multimodal policies combining tactile, force, vision, or proprioception. |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-visuotactile-world-model, tactile-force-tactile-manipulation, world-model-robot, ea-data-robot-demonstrations, ea-data-demonstration-quality, ea-eval-closed-loop, ea-model-vla, ea-model-named-foundation, ea-sensor-multimodal-policy |
| adjacent-and-transfer | 3 | dynamic-tactile-action-model, dynamic-contact-prediction, dynamic-tactile-foundation, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, world-model-video-prediction, world-model-planning, ea-data-in-the-wild, ea-data-dataset-curation, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation, ea-model-finetuning, ea-sensor-tactile-force, ea-sensor-point-cloud |
| limits-and-counterevidence | 3 | world-model-contact, world-model-long-horizon, ea-sensor-occlusion |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-topic-arxiv | `site:arxiv.org/abs "触觉世界模型" "robot"` | Fallback candidate discovery on arXiv pages when API metadata search under-recovers. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-topic-calibration | web | `"触觉世界模型" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-visuotactile-world-model | arxiv_api | llm | medium | `(all:"visuo-tactile" OR all:visuotactile) AND all:"world model" AND all:robot` | 直接覆盖视觉—触觉世界模型。 |
| dynamic-tactile-action-model | arxiv_api | llm | medium | `all:tactile AND (all:"world action model" OR all:"action-conditioned") AND all:robot` | 覆盖动作条件的触觉未来。 |
| dynamic-contact-prediction | arxiv_api | llm | medium | `all:"robot manipulation" AND (all:"contact prediction" OR all:"force prediction" OR all:"slip prediction")` | 覆盖接触状态和物理结果预测。 |
| dynamic-tactile-foundation | arxiv_api | llm | medium | `all:tactile AND (all:"foundation model" OR all:pretraining) AND all:robot` | 覆盖大规模触觉表征与迁移。 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (medium): 区分触觉表征、触觉未来预测和闭环动作使用。
