# Query Plan: Sparse language, dense vision, and continuous action alignment in VLA systems

## Scope

- Knowledge IDs: EA-MODEL, EA-SENSOR, EA-XEMBODIMENT
- Families: vla, retargeting
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 112
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-language-action-grounding | mechanism | `(all:VLA OR all:"vision-language-action") AND (all:"language-action" OR all:"instruction grounding")` | 覆盖语言到动作的显式约束。 |
| dynamic-continuous-action-expert | policy-interface | `(all:VLA OR all:"vision-language-action") AND (all:"continuous action" OR all:"action expert" OR all:"flow matching")` | 覆盖连续动作专家和运动先验。 |
| dynamic-action-tokenizer | policy-interface | `all:robot AND (all:"action tokenizer" OR all:"action tokenization")` | 覆盖离散动作表示及解码边界。 |
| dynamic-vision-action-geometry | representation | `all:"robot manipulation" AND (all:"action-aligned" OR all:"task-space") AND (all:vision OR all:3D)` | 覆盖视觉几何到可执行动作的接口。 |
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |
| vla-large-scale-robot-data | data-scaling | `all:"large-scale" AND all:"robot data"` | Surface scaling and dataset-layer discussions for robot foundation models. |
| vla-robot-foundation-action | foundation-model | `all:"robot foundation model" AND all:action` | Find broader foundation-model papers whose metadata may not use VLA. |
| vla-finetuning-policy | transfer | `all:"fine-tuning" AND all:"robot policy"` | Surface evidence about target-task adaptation and data requirements. |
| vla-data-mixture | data-mixture | `all:"data mixture" AND all:"robot foundation model"` | Find mixture and dataset composition papers that explain scaling behavior. |
| vla-negative-transfer | limitation | `all:"negative transfer" AND all:robot AND all:policy` | Search for failure cases where broad pretraining hurts target deployment. |
| retargeting-robot-manipulation | core | `all:retargeting AND all:"robot manipulation"` | Find the broad retargeting literature for manipulation tasks. |
| retargeting-human-to-robot-mapping | transfer | `all:"human-to-robot" AND all:mapping` | Capture human motion or hand data mapped onto robot embodiments. |
| retargeting-dexterous-hand | embodiment | `all:"dexterous hand" AND all:retargeting` | Find fine-grained human hand to dexterous hand transfer papers. |
| retargeting-gripper-demonstration | embodiment | `all:gripper AND all:"human demonstration" AND all:robot` | Search for lower-DOF gripper abstractions of human demonstrations. |
| retargeting-morphology-gap | limitation | `all:"morphology gap" AND all:robot` | Find papers that name embodiment mismatch as a transfer limit. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-language-action-grounding, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, retargeting-human-to-robot-mapping, retargeting-dexterous-hand, retargeting-gripper-demonstration, ea-model-finetuning, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot |
| mechanisms-and-interfaces | 3 | dynamic-continuous-action-expert, dynamic-action-tokenizer, dynamic-vision-action-geometry, ea-model-action-tokenization, ea-xembodiment-action-representation |
| direct-topic | 3 | vla-core, vla-named-models, retargeting-robot-manipulation, ea-model-named-foundation, ea-sensor-multimodal-policy, ea-xembodiment-cross-embodiment |
| limits-and-counterevidence | 3 | vla-negative-transfer, retargeting-morphology-gap, ea-sensor-occlusion |

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
| web-topic-calibration | web | `"Sparse language, dense vision, and continuous action alignment in VLA systems" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-language-action-grounding | arxiv_api | llm | medium | `(all:VLA OR all:"vision-language-action") AND (all:"language-action" OR all:"instruction grounding")` | 覆盖语言到动作的显式约束。 |
| dynamic-continuous-action-expert | arxiv_api | llm | medium | `(all:VLA OR all:"vision-language-action") AND (all:"continuous action" OR all:"action expert" OR all:"flow matching")` | 覆盖连续动作专家和运动先验。 |
| dynamic-action-tokenizer | arxiv_api | llm | medium | `all:robot AND (all:"action tokenizer" OR all:"action tokenization")` | 覆盖离散动作表示及解码边界。 |
| dynamic-vision-action-geometry | arxiv_api | llm | medium | `all:"robot manipulation" AND (all:"action-aligned" OR all:"task-space") AND (all:vision OR all:3D)` | 覆盖视觉几何到可执行动作的接口。 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (medium): 补足语言稀疏、视觉几何与连续动作接口的检索面。
