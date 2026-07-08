# Query Plan: 4D时空推理对数据的需求

## Scope

- Knowledge IDs: EA-DATA, EA-SENSOR, EA-MODEL, EA-EVAL
- Families: world-model, vla, droid-ego4d, teleoperation-demo-quality, tactile-force
- Suggested categories: cs.AI, cs.CV, cs.HC, cs.LG, cs.RO, eess.SY
- Minimum candidate count: 20

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-4d-data-requirements | dynamic-association | `all:"4D" AND (all:data OR all:dataset OR all:annotation OR all:supervision) AND (all:robot OR all:embodied)` | Directly target papers discussing data, datasets, annotations, or supervision for 4D embodied reasoning. |
| dynamic-4d-point-track-supervision | dynamic-association | `all:"3D point tracks" AND (all:VLA OR all:robot OR all:manipulation)` | 3D point tracks are a recurring data/supervision format for learning 4D world dynamics. |
| dynamic-4d-pseudo-annotation | dynamic-association | `(all:"4D annotation" OR all:"4D pseudo" OR all:"pseudo annotation") AND (all:robot OR all:embodied OR all:manipulation)` | Surface papers that discuss scalable 4D labels and pseudo-label quality tradeoffs. |
| dynamic-4d-human-robot-data | dynamic-association | `(all:"human video" OR all:egocentric OR all:UMI OR all:DROID) AND (all:"world model" OR all:"4D" OR all:"video-action")` | 4D reasoning systems often combine human videos, egocentric video, UMI-style data, and robot demonstrations. |
| dynamic-failure-recovery-world-model-data | dynamic-association | `(all:failure OR all:recovery OR all:negative) AND all:"world model" AND all:robot` | World models used for action evaluation need failed rollouts and recovery trajectories, not only successful demonstrations. |
| dynamic-geometry-teacher-data | dynamic-association | `(all:"geometry foundation model" OR all:VGGT OR all:"pointmap") AND (all:"world model" OR all:robot OR all:"4D")` | Some 4D world models use geometry foundation models as teachers or pseudo-label sources. |
| dynamic-tactile-force-world-model-data | dynamic-association | `(all:tactile OR all:"force feedback" OR all:"force-torque") AND all:"world model" AND all:manipulation` | Contact-rich 4D reasoning may require tactile or force data beyond vision. |
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
| droid-robot-manipulation | named-dataset | `all:DROID AND all:"robot manipulation"` | Find DROID robot data papers and reuse discussions. |
| ego4d-robot-learning | named-dataset | `all:Ego4D AND all:"robot learning"` | Catch robot-learning papers that draw on egocentric human video data. |
| droid-ego-egocentric-video | adjacent-data | `all:"egocentric video" AND all:"robot learning"` | Find human-observation data papers near Ego4D even when the dataset is not named. |
| droid-ego-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot demonstration"` | Capture natural-environment data collection and scaling constraints. |
| droid-ego-data-mixture | data-mixture | `all:"data mixture" AND all:"robot learning"` | Find cross-dataset mixture papers that discuss data compatibility and noise. |
| teleop-imitation-learning | core | `all:teleoperation AND all:"imitation learning" AND all:robot` | Find the main literature surface connecting teleoperation to robot policy learning. |
| teleop-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface trace consistency, operator skill, and data acceptance criteria. |
| teleop-operator-burden | human-factor | `all:operator AND all:burden AND all:teleoperation` | Find papers about human workload and collection throughput. |
| teleop-latency | system-limitation | `all:latency AND all:teleoperation AND all:robot` | Capture delay and synchronization limits that affect demonstration fidelity. |
| teleop-action-interface | policy-interface | `all:"action interface" AND all:robot AND all:demonstration` | Find work where action-space choices determine whether demonstrations transfer. |
| tactile-force-tactile-manipulation | core | `all:tactile AND all:"robot manipulation"` | Find tactile sensing papers tied to manipulation policies or control. |
| tactile-force-force-torque | force | `all:force AND all:torque AND all:robot` | Cover force/torque observability and low-dimensional contact feedback. |
| tactile-force-slip-detection | contact-state | `all:"slip detection" AND all:robot` | Find tactile and force cues for grasp stability and material interaction. |
| tactile-force-contact-rich | task-family | `all:"contact-rich" AND all:manipulation` | Surface high-contact tasks where vision-only policies often fail. |
| tactile-force-sensor-fusion | fusion | `all:"sensor fusion" AND all:tactile AND all:robot` | Find multimodal policies combining tactile, force, vision, or proprioception. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-4d-data-requirements-arxiv | `site:arxiv.org 4D robot dataset annotation supervision world model` | Fallback discovery for data/annotation-heavy 4D papers. |
| browser-4d-point-track-vla-arxiv | `site:arxiv.org "3D point tracks" VLA robot world dynamics` | Fallback discovery for 3D point-track supervision papers. |
| browser-video-action-world-model-data-arxiv | `site:arxiv.org video-action world model robot heterogeneous data failure trajectories` | Fallback discovery for video-action world model data mixtures. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-4d-data-requirements-terms | agent | `"4D" robot "dataset" "world model" annotation` | Calibrate terms for data requirements around 4D embodied reasoning. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-4d-data-requirements | arxiv_api | agent | medium | `all:"4D" AND (all:data OR all:dataset OR all:annotation OR all:supervision) AND (all:robot OR all:embodied)` | Directly target papers discussing data, datasets, annotations, or supervision for 4D embodied reasoning. |
| dynamic-4d-point-track-supervision | arxiv_api | agent | medium | `all:"3D point tracks" AND (all:VLA OR all:robot OR all:manipulation)` | 3D point tracks are a recurring data/supervision format for learning 4D world dynamics. |
| dynamic-4d-pseudo-annotation | arxiv_api | agent | medium | `(all:"4D annotation" OR all:"4D pseudo" OR all:"pseudo annotation") AND (all:robot OR all:embodied OR all:manipulation)` | Surface papers that discuss scalable 4D labels and pseudo-label quality tradeoffs. |
| dynamic-4d-human-robot-data | arxiv_api | agent | medium | `(all:"human video" OR all:egocentric OR all:UMI OR all:DROID) AND (all:"world model" OR all:"4D" OR all:"video-action")` | 4D reasoning systems often combine human videos, egocentric video, UMI-style data, and robot demonstrations. |
| dynamic-failure-recovery-world-model-data | arxiv_api | agent | medium | `(all:failure OR all:recovery OR all:negative) AND all:"world model" AND all:robot` | World models used for action evaluation need failed rollouts and recovery trajectories, not only successful demonstrations. |
| dynamic-geometry-teacher-data | arxiv_api | agent | medium | `(all:"geometry foundation model" OR all:VGGT OR all:"pointmap") AND (all:"world model" OR all:robot OR all:"4D")` | Some 4D world models use geometry foundation models as teachers or pseudo-label sources. |
| dynamic-tactile-force-world-model-data | arxiv_api | agent | medium | `(all:tactile OR all:"force feedback" OR all:"force-torque") AND all:"world model" AND all:manipulation` | Contact-rich 4D reasoning may require tactile or force data beyond vision. |
| browser-4d-data-requirements-arxiv | browser_fallback | agent | medium | `site:arxiv.org 4D robot dataset annotation supervision world model` | Fallback discovery for data/annotation-heavy 4D papers. |
| browser-4d-point-track-vla-arxiv | browser_fallback | agent | medium | `site:arxiv.org "3D point tracks" VLA robot world dynamics` | Fallback discovery for 3D point-track supervision papers. |
| browser-video-action-world-model-data-arxiv | browser_fallback | agent | medium | `site:arxiv.org video-action world model robot heterogeneous data failure trajectories` | Fallback discovery for video-action world model data mixtures. |
| web-4d-data-requirements-terms | web_calibration | agent | medium | `"4D" robot "dataset" "world model" annotation` | Calibrate terms for data requirements around 4D embodied reasoning. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- agent dynamic expansion (medium): The topic asks for data requirements behind 4D spatiotemporal reasoning, so expand from 4D/world-model/VLA terms into datasets, annotation, privileged supervision, pseudo labels, heterogeneous video-action data, failure/recovery data, and contact-sensing data.
