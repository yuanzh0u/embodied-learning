# Query Plan: 近一年exocentric人类数据的发展

## Scope

- Knowledge IDs: EA-DATA, EA-XEMBODIMENT, EA-MODEL, EA-SENSOR
- Families: none
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 100
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |
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
| direct-topic | 3 | ea-data-robot-demonstrations, ea-data-demonstration-quality, ea-xembodiment-cross-embodiment, ea-model-vla, ea-model-named-foundation, ea-sensor-multimodal-policy |
| adjacent-and-transfer | 3 | ea-data-in-the-wild, ea-data-dataset-curation, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot, ea-model-finetuning, ea-sensor-tactile-force, ea-sensor-point-cloud |
| mechanisms-and-interfaces | 3 | ea-xembodiment-action-representation, ea-model-action-tokenization |
| limits-and-counterevidence | 3 | ea-sensor-occlusion |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-topic-arxiv | `site:arxiv.org/abs "近一年exocentric人类数据的发展" "robot"` | Fallback candidate discovery on arXiv pages when API metadata search under-recovers. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-topic-calibration | web | `"近一年exocentric人类数据的发展" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.
