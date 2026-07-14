# Query Plan: 具身数据感知误差与认知误差区别

## Scope

- Knowledge IDs: EA-DATA, EA-SENSOR, EA-EVAL, EA-MODEL
- Families: vla, world-model, tactile-force
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 160
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-robot-perception-failure | limitation | `all:robot AND (all:"perception failure" OR all:"perception error" OR all:"perceptual uncertainty")` | 直接覆盖具身感知失败。 |
| dynamic-sensor-drift-calibration | limitation | `all:robot AND (all:"sensor drift" OR all:miscalibration OR all:"temporal misalignment")` | 覆盖漂移、标定与同步误差。 |
| dynamic-multimodal-fusion-failure | limitation | `all:robot AND all:"multimodal fusion" AND (all:failure OR all:robustness OR all:uncertainty)` | 覆盖模态融合污染和缺失模态。 |
| dynamic-failure-attribution | evaluation | `all:"robot manipulation" AND (all:"failure attribution" OR all:"failure diagnosis" OR all:"failure detection")` | 覆盖失败定位和可观测诊断信号。 |
| dynamic-vla-uncertainty-recovery | recovery | `(all:VLA OR all:"vision-language-action") AND (all:uncertainty OR all:"failure recovery" OR all:intervention)` | 覆盖策略不确定性与恢复。 |
| dynamic-perception-action-decoupling | evaluation | `all:robot AND (all:probing OR all:"action head") AND (all:perception OR all:representation) AND all:failure` | 覆盖表征正确但动作选择错误的解耦证据。 |
| dynamic-world-model-action-ranking | evaluation | `all:"world model" AND (all:"action ranking" OR all:admissibility OR all:"policy evaluation") AND all:robot` | 覆盖预测保真与认知决策有效性的边界。 |
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |
| vla-large-scale-robot-data | data-scaling | `all:"large-scale" AND all:"robot data"` | Surface scaling and dataset-layer discussions for robot foundation models. |
| vla-robot-foundation-action | foundation-model | `all:"robot foundation model" AND all:action` | Find broader foundation-model papers whose metadata may not use VLA. |
| vla-finetuning-policy | transfer | `all:"fine-tuning" AND all:"robot policy"` | Surface evidence about target-task adaptation and data requirements. |
| vla-data-mixture | data-mixture | `all:"data mixture" AND all:"robot foundation model"` | Find mixture and dataset composition papers that explain scaling behavior. |
| vla-negative-transfer | limitation | `all:"negative transfer" AND all:robot AND all:policy` | Search for failure cases where broad pretraining hurts target deployment. |
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
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| limits-and-counterevidence | 3 | dynamic-robot-perception-failure, dynamic-sensor-drift-calibration, dynamic-multimodal-fusion-failure, vla-negative-transfer, world-model-contact, world-model-long-horizon, ea-sensor-occlusion |
| adjacent-and-transfer | 3 | dynamic-failure-attribution, dynamic-perception-action-decoupling, dynamic-world-model-action-ranking, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, world-model-video-prediction, world-model-planning, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, ea-data-in-the-wild, ea-data-dataset-curation, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation, ea-model-finetuning |
| deployment-and-operations | 3 | dynamic-vla-uncertainty-recovery |
| direct-topic | 3 | vla-core, vla-named-models, world-model-robot, tactile-force-tactile-manipulation, ea-data-robot-demonstrations, ea-data-demonstration-quality, ea-sensor-multimodal-policy, ea-eval-closed-loop, ea-model-named-foundation |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization |

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

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-topic-calibration | web | `"具身数据感知误差与认知误差区别" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-robot-perception-failure | arxiv_api | llm | medium | `all:robot AND (all:"perception failure" OR all:"perception error" OR all:"perceptual uncertainty")` | 直接覆盖具身感知失败。 |
| dynamic-sensor-drift-calibration | arxiv_api | llm | medium | `all:robot AND (all:"sensor drift" OR all:miscalibration OR all:"temporal misalignment")` | 覆盖漂移、标定与同步误差。 |
| dynamic-multimodal-fusion-failure | arxiv_api | llm | medium | `all:robot AND all:"multimodal fusion" AND (all:failure OR all:robustness OR all:uncertainty)` | 覆盖模态融合污染和缺失模态。 |
| dynamic-failure-attribution | arxiv_api | llm | medium | `all:"robot manipulation" AND (all:"failure attribution" OR all:"failure diagnosis" OR all:"failure detection")` | 覆盖失败定位和可观测诊断信号。 |
| dynamic-vla-uncertainty-recovery | arxiv_api | llm | medium | `(all:VLA OR all:"vision-language-action") AND (all:uncertainty OR all:"failure recovery" OR all:intervention)` | 覆盖策略不确定性与恢复。 |
| dynamic-perception-action-decoupling | arxiv_api | llm | medium | `all:robot AND (all:probing OR all:"action head") AND (all:perception OR all:representation) AND all:failure` | 覆盖表征正确但动作选择错误的解耦证据。 |
| dynamic-world-model-action-ranking | arxiv_api | llm | medium | `all:"world model" AND (all:"action ranking" OR all:admissibility OR all:"policy evaluation") AND all:robot` | 覆盖预测保真与认知决策有效性的边界。 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (medium): 补足静态 taxonomy 中缺失的感知失败、误差归因和感知—认知解耦术语。
