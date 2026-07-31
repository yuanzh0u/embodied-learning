# Query Plan: 近一年触觉数据与视觉数据联合训练的方法和进展

## Scope

- Knowledge IDs: EA-SENSOR, EA-MODEL, EA-DATA, EA-XEMBODIMENT
- Families: tactile-force, vla, world-model
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 192
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-visuotactile-joint-training | direct | `all:((visuo-tactile OR vision-tactile) AND (training OR learning)) AND all:(robot AND manipulation)` | Capture papers that explicitly train on visual and tactile streams rather than merely adding a touch sensor at deployment. |
| dynamic-visuotactile-world-model | mechanism | `all:((visuo-tactile OR vision-tactile) AND world AND model) AND all:(robot OR manipulation)` | Cover action-conditioned joint prediction of visual and contact futures. |
| dynamic-tactile-vla-grounding | policy-interface | `all:(tactile AND (VLA OR vision-language-action) AND (grounding OR action)) AND all:robot` | Find tactile supervision injected into VLA representations or action experts. |
| dynamic-tactile-distillation | transfer | `all:(tactile AND distillation AND (vision OR VLA)) AND all:(robot OR manipulation)` | Cover training-time tactile supervision that is distilled into a deployable visual policy. |
| dynamic-contact-gated-asymmetric-fusion | mechanism | `all:(tactile AND (gated OR asymmetric) AND fusion) AND all:(robot OR manipulation)` | Capture selective fusion intended to prevent tactile inputs from corrupting visual dynamics. |
| dynamic-visuotactile-reflex-control | deployment | `all:((visuo-tactile OR vision-tactile) AND (reflex OR high-frequency OR residual)) AND all:(robot AND control)` | Cover slow visual planning plus fast tactile residual correction in closed loop. |
| dynamic-visuotactile-benchmark-generalization | evaluation | `all:((visuo-tactile OR touch-vision) AND (benchmark OR dataset OR generalization)) AND all:robot` | Cover paired-data scale, contact-sequence leakage, held-out materials, and closed-loop evaluation boundaries. |
| dynamic-missing-tactile-negative-transfer | limitation | `all:(tactile AND (missing-modality OR negative-transfer OR contamination)) AND all:(robot AND manipulation)` | Search counterevidence on sensor absence, unstructured fusion, and deployment mismatch. |
| calibrated-representation-aligned-tactile-grounding | calibrated-term | `all:"representation-aligned tactile grounding"` | Names where future-touch supervision should enter a VLA. |
| calibrated-tactile-distillation | calibrated-term | `all:"tactile distillation"` | Names training-time touch transfer to a sensor-light deployment policy. |
| calibrated-visuo-tactile-world-model | calibrated-term | `all:"visuo-tactile world model"` | Names joint prediction of contact dynamics and visual evolution. |
| calibrated-contact-sequence-aware-split | calibrated-term | `all:"contact-sequence-aware split"` | Names a leakage-resistant evaluation unit for tactile representation datasets. |
| calibrated-representation-aligned-grounding | calibrated-query | `all:(representation AND tactile AND grounding) AND all:(robot AND manipulation)` | Search the new vocabulary for action-interface alignment. |
| calibrated-tactile-distillation | calibrated-query | `all:(tactile AND distillation AND vision) AND all:(robot OR manipulation)` | Search deployment-time sensor removal after multimodal training. |
| calibrated-contact-sequence-generalization | calibrated-query | `all:(tactile AND contact AND sequence AND generalization) AND all:robot` | Search data-split leakage and true material/sensor generalization. |
| tactile-force-tactile-manipulation | core | `all:tactile AND all:"robot manipulation"` | Find tactile sensing papers tied to manipulation policies or control. |
| tactile-force-force-torque | force | `all:force AND all:torque AND all:robot` | Cover force/torque observability and low-dimensional contact feedback. |
| tactile-force-slip-detection | contact-state | `all:"slip detection" AND all:robot` | Find tactile and force cues for grasp stability and material interaction. |
| tactile-force-contact-rich | task-family | `all:"contact-rich" AND all:manipulation` | Surface high-contact tasks where vision-only policies often fail. |
| tactile-force-sensor-fusion | fusion | `all:"sensor fusion" AND all:tactile AND all:robot` | Find multimodal policies combining tactile, force, vision, or proprioception. |
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
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-visuotactile-joint-training, dynamic-visuotactile-world-model, dynamic-tactile-distillation, dynamic-contact-gated-asymmetric-fusion, dynamic-visuotactile-reflex-control, dynamic-visuotactile-benchmark-generalization, calibrated-representation-aligned-tactile-grounding, calibrated-tactile-distillation, calibrated-visuo-tactile-world-model, calibrated-contact-sequence-aware-split, calibrated-representation-aligned-grounding, calibrated-tactile-distillation, calibrated-contact-sequence-generalization, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, world-model-video-prediction, world-model-planning, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-model-finetuning, ea-data-in-the-wild, ea-data-dataset-curation, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot |
| mechanisms-and-interfaces | 3 | dynamic-tactile-vla-grounding, ea-model-action-tokenization, ea-xembodiment-action-representation |
| limits-and-counterevidence | 3 | dynamic-missing-tactile-negative-transfer, vla-negative-transfer, world-model-contact, world-model-long-horizon, ea-sensor-occlusion |
| direct-topic | 3 | tactile-force-tactile-manipulation, vla-core, vla-named-models, world-model-robot, ea-sensor-multimodal-policy, ea-model-named-foundation, ea-data-robot-demonstrations, ea-data-demonstration-quality, ea-xembodiment-cross-embodiment |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-visuotactile-browser | `site:arxiv.org/abs (visuo-tactile OR vision-tactile) robot manipulation world model VLA` | Recover named methods missed by arXiv metadata wording. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-latest-visuotactile-calibration | llm | `site:arxiv.org/abs/2607 tactile vision robot manipulation` | Calibrate July 2026 terminology and check the end of the requested window. |
| web-calibrated-representation-aligned-tactile-grounding | arxiv | `"representation-aligned tactile grounding" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: representation-aligned tactile grounding. |
| web-calibrated-tactile-distillation | arxiv | `"tactile distillation" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: tactile distillation. |
| web-calibrated-visuo-tactile-world-model | arxiv | `"visuo-tactile world model" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: visuo-tactile world model. |
| web-calibrated-contact-sequence-aware-split | arxiv | `"contact-sequence-aware split" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: contact-sequence-aware split. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-visuotactile-joint-training | arxiv_api | llm | high | `all:((visuo-tactile OR vision-tactile) AND (training OR learning)) AND all:(robot AND manipulation)` | Capture papers that explicitly train on visual and tactile streams rather than merely adding a touch sensor at deployment. |
| dynamic-visuotactile-world-model | arxiv_api | llm | high | `all:((visuo-tactile OR vision-tactile) AND world AND model) AND all:(robot OR manipulation)` | Cover action-conditioned joint prediction of visual and contact futures. |
| dynamic-tactile-vla-grounding | arxiv_api | llm | high | `all:(tactile AND (VLA OR vision-language-action) AND (grounding OR action)) AND all:robot` | Find tactile supervision injected into VLA representations or action experts. |
| dynamic-tactile-distillation | arxiv_api | llm | high | `all:(tactile AND distillation AND (vision OR VLA)) AND all:(robot OR manipulation)` | Cover training-time tactile supervision that is distilled into a deployable visual policy. |
| dynamic-contact-gated-asymmetric-fusion | arxiv_api | llm | medium | `all:(tactile AND (gated OR asymmetric) AND fusion) AND all:(robot OR manipulation)` | Capture selective fusion intended to prevent tactile inputs from corrupting visual dynamics. |
| dynamic-visuotactile-reflex-control | arxiv_api | llm | medium | `all:((visuo-tactile OR vision-tactile) AND (reflex OR high-frequency OR residual)) AND all:(robot AND control)` | Cover slow visual planning plus fast tactile residual correction in closed loop. |
| dynamic-visuotactile-benchmark-generalization | arxiv_api | llm | high | `all:((visuo-tactile OR touch-vision) AND (benchmark OR dataset OR generalization)) AND all:robot` | Cover paired-data scale, contact-sequence leakage, held-out materials, and closed-loop evaluation boundaries. |
| dynamic-missing-tactile-negative-transfer | arxiv_api | llm | medium | `all:(tactile AND (missing-modality OR negative-transfer OR contamination)) AND all:(robot AND manipulation)` | Search counterevidence on sensor absence, unstructured fusion, and deployment mismatch. |
| dynamic-visuotactile-browser | browser_fallback | llm | high | `site:arxiv.org/abs (visuo-tactile OR vision-tactile) robot manipulation world model VLA` | Recover named methods missed by arXiv metadata wording. |
| dynamic-latest-visuotactile-calibration | web_calibration | llm | high | `site:arxiv.org/abs/2607 tactile vision robot manipulation` | Calibrate July 2026 terminology and check the end of the requested window. |

## Calibration Notes

- arxiv calibration (high): Representation-aligned tactile grounding applies future-touch supervision at intermediate action-expert features.
- arxiv calibration (high): HapticVLA distills training-time tactile information into a vision/state policy that does not require touch at deployment.
- arxiv calibration (high): OmniVTA combines a two-stream visuo-tactile world model with a contact-aware policy and a 60 Hz tactile reflex controller.
- arxiv calibration (high): RCT exposes contact-sequence leakage and held-out-material failure in touch-vision-language representation learning.

## Planner Notes

- llm dynamic expansion (high): The review is restricted to training or adapting robot representations, policies, and world models with paired visual and tactile/force data; pure tactile hardware and inference-only sensing are adjacent rather than direct evidence.
