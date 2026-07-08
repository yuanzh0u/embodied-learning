# Query Plan: 触觉世界模型

## Scope

- Knowledge IDs: EA-SENSOR, EA-DATA, EA-MODEL, EA-EVAL
- Families: tactile-force, world-model, vla, last-centimeter
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Minimum candidate count: 20

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-tactile-world-model | dynamic-association | `all:"tactile world model" AND all:"robot"` | Direct query for tactile world model papers. |
| dynamic-visuotactile-world-model | dynamic-association | `(all:"visuo-tactile" OR all:"visuotactile") AND all:"world model"` | Many papers spell the topic as visuo-tactile or visuotactile world modeling. |
| dynamic-tactile-world-action-model | dynamic-association | `all:"tactile" AND all:"world action model"` | Recent robotics papers may frame tactile prediction as a world-action model. |
| dynamic-force-conditioned-tactile-dynamics | dynamic-association | `all:"force" AND all:"tactile" AND all:"dynamics" AND all:"manipulation"` | Force/torque signals often condition future tactile dynamics in contact-rich manipulation. |
| dynamic-future-tactile-prediction | dynamic-association | `all:"future tactile" AND all:"robot"` | Tactile world models may be described as future tactile prediction or tactile foresight. |
| dynamic-contact-rich-world-model | dynamic-association | `all:"contact-rich" AND all:"world model" AND all:"robot"` | Contact-rich manipulation is the main task family where tactile world models matter. |
| dynamic-tactile-vla-world | dynamic-association | `all:"tactile" AND (all:"vision-language-action" OR all:"VLA") AND all:"world"` | Tactile information may be integrated into VLA or world-action models rather than named as world models. |
| dynamic-tactile-dataset-action | dynamic-association | `all:"tactile" AND all:"dataset" AND all:"action" AND all:"manipulation"` | Review needs data and benchmark evidence for tactile world modeling. |
| dynamic-haptic-tactile-language-action | dynamic-association | `all:"haptic" AND all:"tactile" AND all:"language" AND all:"action"` | Haptic-informed VTLA datasets can supply tactile world-model training data. |
| dynamic-tactile-recovery | dynamic-association | `all:"tactile" AND all:"recovery" AND all:"contact" AND all:"robot"` | Recovery and perturbation handling are important downstream claims for tactile world models. |
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
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |
| vla-large-scale-robot-data | data-scaling | `all:"large-scale" AND all:"robot data"` | Surface scaling and dataset-layer discussions for robot foundation models. |
| vla-robot-foundation-action | foundation-model | `all:"robot foundation model" AND all:action` | Find broader foundation-model papers whose metadata may not use VLA. |
| vla-finetuning-policy | transfer | `all:"fine-tuning" AND all:"robot policy"` | Surface evidence about target-task adaptation and data requirements. |
| vla-data-mixture | data-mixture | `all:"data mixture" AND all:"robot foundation model"` | Find mixture and dataset composition papers that explain scaling behavior. |
| vla-negative-transfer | limitation | `all:"negative transfer" AND all:robot AND all:policy` | Search for failure cases where broad pretraining hurts target deployment. |
| last-centimeter-exact | core | `all:"last centimeter" AND all:robot` | Catch papers that explicitly name the deployment bottleneck. |
| last-centimeter-visual-servoing | pre-contact | `all:"visual servoing" AND all:"robot manipulation"` | Find close-range pose correction before contact closure. |
| last-centimeter-force-insertion | contact | `all:"force control" AND all:insertion AND all:robot` | Surface insertion and compliant-contact methods for final alignment. |
| last-centimeter-failure-recovery | recovery | `all:"failure recovery" AND all:"robot manipulation"` | Find retry, recovery, and takeover strategies after near-goal failures. |
| last-centimeter-fixture | deployment-adjacent | `(all:fixture OR all:fixturing) AND all:robot AND all:insertion` | Capture fixture and workcell design that reduces contact uncertainty. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-tactile-world-model-browser | `"tactile world model" robot manipulation arxiv` | Fallback discovery for exact phrase. |
| dynamic-dream-tac-browser | `"Dream-Tac" tactile world action model` | Known recent naming pattern for tactile world-action modeling. |
| dynamic-tacforesight-browser | `"TacForeSight" tactile world model` | Known recent naming pattern for tactile foresight/world modeling. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-tactile-world-model-web | llm | `"tactile world model" "contact-rich manipulation"` | Calibrate phrase variants outside arXiv metadata. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-tactile-world-model | arxiv_api | llm | medium | `all:"tactile world model" AND all:"robot"` | Direct query for tactile world model papers. |
| dynamic-visuotactile-world-model | arxiv_api | llm | medium | `(all:"visuo-tactile" OR all:"visuotactile") AND all:"world model"` | Many papers spell the topic as visuo-tactile or visuotactile world modeling. |
| dynamic-tactile-world-action-model | arxiv_api | llm | medium | `all:"tactile" AND all:"world action model"` | Recent robotics papers may frame tactile prediction as a world-action model. |
| dynamic-force-conditioned-tactile-dynamics | arxiv_api | llm | medium | `all:"force" AND all:"tactile" AND all:"dynamics" AND all:"manipulation"` | Force/torque signals often condition future tactile dynamics in contact-rich manipulation. |
| dynamic-future-tactile-prediction | arxiv_api | llm | medium | `all:"future tactile" AND all:"robot"` | Tactile world models may be described as future tactile prediction or tactile foresight. |
| dynamic-contact-rich-world-model | arxiv_api | llm | medium | `all:"contact-rich" AND all:"world model" AND all:"robot"` | Contact-rich manipulation is the main task family where tactile world models matter. |
| dynamic-tactile-vla-world | arxiv_api | llm | medium | `all:"tactile" AND (all:"vision-language-action" OR all:"VLA") AND all:"world"` | Tactile information may be integrated into VLA or world-action models rather than named as world models. |
| dynamic-tactile-dataset-action | arxiv_api | llm | medium | `all:"tactile" AND all:"dataset" AND all:"action" AND all:"manipulation"` | Review needs data and benchmark evidence for tactile world modeling. |
| dynamic-haptic-tactile-language-action | arxiv_api | llm | medium | `all:"haptic" AND all:"tactile" AND all:"language" AND all:"action"` | Haptic-informed VTLA datasets can supply tactile world-model training data. |
| dynamic-tactile-recovery | arxiv_api | llm | medium | `all:"tactile" AND all:"recovery" AND all:"contact" AND all:"robot"` | Recovery and perturbation handling are important downstream claims for tactile world models. |
| dynamic-tactile-world-model-browser | browser_fallback | llm | medium | `"tactile world model" robot manipulation arxiv` | Fallback discovery for exact phrase. |
| dynamic-dream-tac-browser | browser_fallback | llm | medium | `"Dream-Tac" tactile world action model` | Known recent naming pattern for tactile world-action modeling. |
| dynamic-tacforesight-browser | browser_fallback | llm | medium | `"TacForeSight" tactile world model` | Known recent naming pattern for tactile foresight/world modeling. |
| dynamic-tactile-world-model-web | web_calibration | llm | medium | `"tactile world model" "contact-rich manipulation"` | Calibrate phrase variants outside arXiv metadata. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (medium): Agent expanded tactile world model into visuo-tactile world/action models, force-conditioned tactile dynamics, contact-rich manipulation, tactile datasets, and last-centimeter recovery.
