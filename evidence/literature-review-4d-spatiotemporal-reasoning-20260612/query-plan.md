# Query Plan: 4D时空推理

## Scope

- Knowledge IDs: EA-SENSOR, EA-MODEL, EA-EVAL
- Families: world-model
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Minimum candidate count: 12

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-4d-spatiotemporal-reasoning | dynamic-association | `all:"4D" AND all:"spatio-temporal reasoning"` | Direct phrase-level recall for papers using 4D and spatio-temporal reasoning language. |
| dynamic-4d-scene-graph | dynamic-association | `all:"4D scene graph" OR all:"spatio-temporal scene graph"` | Scene graphs often encode object relations over time, a natural substrate for 4D reasoning. |
| dynamic-dynamic-3d-scene-understanding | dynamic-association | `all:"dynamic 3D scene" AND (all:reasoning OR all:planning OR all:understanding)` | Many 4D papers use dynamic 3D scene wording rather than the exact term 4D. |
| dynamic-4d-representation-robot | dynamic-association | `all:"4D representation" AND (all:robot OR all:embodied OR all:manipulation)` | Tie 4D representation papers back to embodied AI and robotics relevance. |
| dynamic-scene-flow-robot-reasoning | dynamic-association | `all:"scene flow" AND (all:robot OR all:embodied) AND (all:reasoning OR all:planning)` | Scene flow is a core motion-field representation for temporal 3D reasoning. |
| dynamic-occupancy-forecasting-embodied | dynamic-association | `all:"occupancy forecasting" AND (all:embodied OR all:robot OR all:planning)` | Occupancy forecasting captures future spatial states for navigation and planning. |
| dynamic-video-world-model-3d-planning | dynamic-association | `all:"video world model" AND (all:"3D" OR all:"4D" OR all:planning)` | Video/world-model papers often discuss temporal physical prediction even without 4D wording. |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-4d-spatiotemporal-reasoning-arxiv | `site:arxiv.org 4D spatiotemporal reasoning embodied AI robot` | Fallback candidate discovery when arXiv API under-recovers exact 4D wording. |
| browser-4d-scene-graph-arxiv | `site:arxiv.org "4D scene graph" robot reasoning` | Fallback candidate discovery for temporal relational scene representations. |
| browser-dynamic-3d-world-model-arxiv | `site:arxiv.org dynamic 3D scene world model robot planning` | Fallback candidate discovery for world-model and planning papers with dynamic 3D wording. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-4d-spatiotemporal-terms | agent | `"4D" "spatio-temporal reasoning" robot` | Calibrate whether the exact phrase is common or whether adjacent terms dominate. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-4d-spatiotemporal-reasoning | arxiv_api | agent | medium | `all:"4D" AND all:"spatio-temporal reasoning"` | Direct phrase-level recall for papers using 4D and spatio-temporal reasoning language. |
| dynamic-4d-scene-graph | arxiv_api | agent | medium | `all:"4D scene graph" OR all:"spatio-temporal scene graph"` | Scene graphs often encode object relations over time, a natural substrate for 4D reasoning. |
| dynamic-dynamic-3d-scene-understanding | arxiv_api | agent | medium | `all:"dynamic 3D scene" AND (all:reasoning OR all:planning OR all:understanding)` | Many 4D papers use dynamic 3D scene wording rather than the exact term 4D. |
| dynamic-4d-representation-robot | arxiv_api | agent | medium | `all:"4D representation" AND (all:robot OR all:embodied OR all:manipulation)` | Tie 4D representation papers back to embodied AI and robotics relevance. |
| dynamic-scene-flow-robot-reasoning | arxiv_api | agent | medium | `all:"scene flow" AND (all:robot OR all:embodied) AND (all:reasoning OR all:planning)` | Scene flow is a core motion-field representation for temporal 3D reasoning. |
| dynamic-occupancy-forecasting-embodied | arxiv_api | agent | medium | `all:"occupancy forecasting" AND (all:embodied OR all:robot OR all:planning)` | Occupancy forecasting captures future spatial states for navigation and planning. |
| dynamic-video-world-model-3d-planning | arxiv_api | agent | medium | `all:"video world model" AND (all:"3D" OR all:"4D" OR all:planning)` | Video/world-model papers often discuss temporal physical prediction even without 4D wording. |
| browser-4d-spatiotemporal-reasoning-arxiv | browser_fallback | agent | medium | `site:arxiv.org 4D spatiotemporal reasoning embodied AI robot` | Fallback candidate discovery when arXiv API under-recovers exact 4D wording. |
| browser-4d-scene-graph-arxiv | browser_fallback | agent | medium | `site:arxiv.org "4D scene graph" robot reasoning` | Fallback candidate discovery for temporal relational scene representations. |
| browser-dynamic-3d-world-model-arxiv | browser_fallback | agent | medium | `site:arxiv.org dynamic 3D scene world model robot planning` | Fallback candidate discovery for world-model and planning papers with dynamic 3D wording. |
| web-4d-spatiotemporal-terms | web_calibration | agent | medium | `"4D" "spatio-temporal reasoning" robot` | Calibrate whether the exact phrase is common or whether adjacent terms dominate. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- agent dynamic expansion (medium): 4D spatiotemporal reasoning is not a static taxonomy family; expand from embodied world models into dynamic 3D/4D scene representations, scene graphs, scene flow, occupancy forecasting, and video/world-model planning.
