# Query Plan: 第三视角视频数据对ego数据采集和预训练的帮助

## Scope

- Knowledge IDs: EA-DATA, EA-MODEL, EA-XEMBODIMENT, EA-SENSOR
- Families: droid-ego4d
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 124
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-exocentric-video-robot | dynamic-association | `all:exocentric AND all:"robot learning"` | Exocentric (third-person) video is the core term for this topic but is absent from the static taxonomy. |
| dynamic-ego-exo4d | named-dataset | `all:"Ego-Exo4D"` | Ego-Exo4D is the primary paired ego-exo dataset; papers using it directly address the topic. |
| dynamic-ego-exo-paired | dynamic-association | `all:"ego-exo" AND all:robot` | Ego-exo paired data is the specific data paradigm this topic investigates. |
| dynamic-third-person-camera-robot | dynamic-association | `all:"third-person" AND all:"robot" AND all:camera` | Third-person camera is the common phrasing for exocentric view in robot learning. |
| dynamic-multi-view-manipulation | dynamic-association | `all:"multi-view" AND all:"robot manipulation"` | Multi-view setups combining ego and exo perspectives are directly relevant to the topic. |
| dynamic-external-camera-learning | dynamic-association | `all:"external camera" AND all:"robot learning"` | External camera is another term for third-person view in robot data collection. |
| dynamic-third-person-pretrain | dynamic-association | `all:"third-person" AND all:"pretraining" AND all:robot` | Directly targets pretraining with third-person video data for robot learning. |
| dynamic-multi-camera-vla | dynamic-association | `all:"multi-camera" AND all:"vision-language-action"` | Multi-camera VLA papers discuss view selection and ego-exo complementarity. |
| dynamic-ego-centric-pretrain | dynamic-association | `all:"egocentric" AND all:"pretraining" AND all:robot` | Egocentric pretraining is the downstream consumer of third-person data augmentation. |
| dynamic-hand-object-reconstruction-multi-view | dynamic-association | `all:"hand-object" AND all:"multi-view" AND all:reconstruction` | Multi-view hand-object reconstruction is a key mechanism by which third-person data helps ego data. |
| droid-robot-manipulation | named-dataset | `all:DROID AND all:"robot manipulation"` | Find DROID robot data papers and reuse discussions. |
| ego4d-robot-learning | named-dataset | `all:Ego4D AND all:"robot learning"` | Catch robot-learning papers that draw on egocentric human video data. |
| droid-ego-egocentric-video | adjacent-data | `all:"egocentric video" AND all:"robot learning"` | Find human-observation data papers near Ego4D even when the dataset is not named. |
| droid-ego-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot demonstration"` | Capture natural-environment data collection and scaling constraints. |
| droid-ego-data-mixture | data-mixture | `all:"data mixture" AND all:"robot learning"` | Find cross-dataset mixture papers that discuss data compatibility and noise. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-exocentric-video-robot, dynamic-ego-exo-paired, dynamic-third-person-camera-robot, dynamic-multi-view-manipulation, dynamic-external-camera-learning, dynamic-third-person-pretrain, dynamic-multi-camera-vla, dynamic-ego-centric-pretrain, dynamic-hand-object-reconstruction-multi-view, droid-ego-egocentric-video, droid-ego-in-the-wild, droid-ego-data-mixture, ea-data-in-the-wild, ea-data-dataset-curation, ea-model-finetuning, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot, ea-sensor-tactile-force, ea-sensor-point-cloud |
| direct-topic | 3 | dynamic-ego-exo4d, droid-robot-manipulation, ego4d-robot-learning, ea-data-robot-demonstrations, ea-data-demonstration-quality, ea-model-vla, ea-model-named-foundation, ea-xembodiment-cross-embodiment, ea-sensor-multimodal-policy |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization, ea-xembodiment-action-representation |
| limits-and-counterevidence | 3 | ea-sensor-occlusion |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-exo-ego-browser | `"exocentric" "egocentric" "robot" "pretraining" site:arxiv.org` | Browser fallback for ego-exo paired pretraining papers that may not appear in API metadata. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-exo-ego-web | llm | `"ego-exo" "robot learning" "pretraining" 2025 2026` | Calibrate current terminology for ego-exo paired data in robot learning. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-exocentric-video-robot | arxiv_api | llm | high | `all:exocentric AND all:"robot learning"` | Exocentric (third-person) video is the core term for this topic but is absent from the static taxonomy. |
| dynamic-ego-exo4d | arxiv_api | llm | high | `all:"Ego-Exo4D"` | Ego-Exo4D is the primary paired ego-exo dataset; papers using it directly address the topic. |
| dynamic-ego-exo-paired | arxiv_api | llm | high | `all:"ego-exo" AND all:robot` | Ego-exo paired data is the specific data paradigm this topic investigates. |
| dynamic-third-person-camera-robot | arxiv_api | llm | high | `all:"third-person" AND all:"robot" AND all:camera` | Third-person camera is the common phrasing for exocentric view in robot learning. |
| dynamic-multi-view-manipulation | arxiv_api | llm | medium | `all:"multi-view" AND all:"robot manipulation"` | Multi-view setups combining ego and exo perspectives are directly relevant to the topic. |
| dynamic-external-camera-learning | arxiv_api | llm | medium | `all:"external camera" AND all:"robot learning"` | External camera is another term for third-person view in robot data collection. |
| dynamic-third-person-pretrain | arxiv_api | llm | high | `all:"third-person" AND all:"pretraining" AND all:robot` | Directly targets pretraining with third-person video data for robot learning. |
| dynamic-multi-camera-vla | arxiv_api | llm | medium | `all:"multi-camera" AND all:"vision-language-action"` | Multi-camera VLA papers discuss view selection and ego-exo complementarity. |
| dynamic-ego-centric-pretrain | arxiv_api | llm | high | `all:"egocentric" AND all:"pretraining" AND all:robot` | Egocentric pretraining is the downstream consumer of third-person data augmentation. |
| dynamic-hand-object-reconstruction-multi-view | arxiv_api | llm | medium | `all:"hand-object" AND all:"multi-view" AND all:reconstruction` | Multi-view hand-object reconstruction is a key mechanism by which third-person data helps ego data. |
| dynamic-exo-ego-browser | browser_fallback | llm | medium | `"exocentric" "egocentric" "robot" "pretraining" site:arxiv.org` | Browser fallback for ego-exo paired pretraining papers that may not appear in API metadata. |
| dynamic-exo-ego-web | web_calibration | llm | medium | `"ego-exo" "robot learning" "pretraining" 2025 2026` | Calibrate current terminology for ego-exo paired data in robot learning. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (high): Static taxonomy lacks exocentric/third-person/Ego-Exo4D terms that are central to this topic.
