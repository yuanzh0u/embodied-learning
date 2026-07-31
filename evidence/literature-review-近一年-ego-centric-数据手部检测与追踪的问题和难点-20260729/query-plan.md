# Query Plan: 近一年 Ego-centric 数据手部检测与追踪的问题和难点

## Scope

- Knowledge IDs: EA-DATA, EA-SENSOR, EA-HARDWARE
- Families: droid-ego4d, retargeting
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 112
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-egocentric-hand-detection | core | `all:egocentric AND (all:"hand detection" OR all:"hand segmentation")` | Directly retrieves first-person hand localization and segmentation work. |
| dynamic-egocentric-hand-pose | core | `all:egocentric AND (all:"3D hand pose" OR all:"hand pose estimation" OR all:"hand mesh")` | Covers joint and mesh estimation, which are the dominant technical meanings of hand tracking in recent work. |
| dynamic-first-person-hand-tracking | tracking | `(all:"first-person" OR all:egocentric) AND all:hand AND (all:tracking OR all:temporal)` | Finds explicit temporal tracking and sequence-consistency work. |
| dynamic-egocentric-hand-object | mechanism | `all:egocentric AND (all:"hand-object interaction" OR all:"hand object") AND (all:pose OR all:tracking OR all:detection)` | Interaction is the main source of self/object occlusion and contact ambiguity. |
| dynamic-hand-occlusion-motion-blur | limitation | `all:egocentric AND all:hand AND (all:occlusion OR all:"motion blur" OR all:truncation OR all:"ego-motion")` | Targets the dominant failure conditions rather than only successful methods. |
| dynamic-bimanual-identity | limitation | `all:egocentric AND (all:bimanual OR all:"two hands") AND (all:tracking OR all:pose OR all:identity)` | Bimanual overlap and left/right identity swaps are a distinct tracking failure mode. |
| dynamic-hand-tracking-benchmark | evaluation | `all:egocentric AND all:hand AND (all:benchmark OR all:dataset OR all:evaluation) AND (all:pose OR all:tracking)` | Retrieves datasets and evaluation protocols needed to audit annotation and metric gaps. |
| dynamic-ego-exo-hand-ground-truth | evaluation | `(all:"ego-exo" OR all:multiview) AND all:hand AND (all:"ground truth" OR all:annotation OR all:tracking)` | Multi-view capture is the main route to accurate in-the-wild 3D hand ground truth. |
| dynamic-event-camera-hand-pose | adjacent | `all:egocentric AND all:hand AND (all:event OR all:stereo) AND (all:pose OR all:tracking)` | Event/stereo sensing directly addresses blur, dynamic range, and depth ambiguity. |
| dynamic-realtime-hoi-industrial | deployment | `all:egocentric AND all:hand AND (all:"real-time" OR all:streaming OR all:industrial) AND (all:detection OR all:tracking OR all:interaction)` | Surfaces latency, compute, and cascade-error trade-offs in deployable systems. |
| calibrated-egoev-handpose | calibrated-term | `all:"EgoEV-HandPose"` | Named 2026 event-camera method and dataset. |
| calibrated-ego-exo-3d-hand-tracking | calibrated-term | `all:"ego-exo 3D hand tracking"` | Named 2025 annotation route. |
| calibrated-bimanual-occlusion | calibrated-term | `all:"bimanual occlusion"` | Explicit recent failure condition. |
| calibrated-ego-motion-interference | calibrated-term | `all:"ego-motion interference"` | Explicit recent sensing limitation. |
| calibration-ego-event-hand | calibrated-query | `all:EgoEV-HandPose OR (all:egocentric AND all:event AND all:"hand pose")` | Recover the method and adjacent event-camera papers. |
| calibration-ego-exo-hand | calibrated-query | `all:"ego-exo" AND all:"hand tracking"` | Recover the mobile multi-camera ground-truth lineage. |
| droid-robot-manipulation | named-dataset | `all:DROID AND all:"robot manipulation"` | Find DROID robot data papers and reuse discussions. |
| ego4d-robot-learning | named-dataset | `all:Ego4D AND all:"robot learning"` | Catch robot-learning papers that draw on egocentric human video data. |
| droid-ego-egocentric-video | adjacent-data | `all:"egocentric video" AND all:"robot learning"` | Find human-observation data papers near Ego4D even when the dataset is not named. |
| droid-ego-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot demonstration"` | Capture natural-environment data collection and scaling constraints. |
| droid-ego-data-mixture | data-mixture | `all:"data mixture" AND all:"robot learning"` | Find cross-dataset mixture papers that discuss data compatibility and noise. |
| retargeting-robot-manipulation | core | `all:retargeting AND all:"robot manipulation"` | Find the broad retargeting literature for manipulation tasks. |
| retargeting-human-to-robot-mapping | transfer | `all:"human-to-robot" AND all:mapping` | Capture human motion or hand data mapped onto robot embodiments. |
| retargeting-dexterous-hand | embodiment | `all:"dexterous hand" AND all:retargeting` | Find fine-grained human hand to dexterous hand transfer papers. |
| retargeting-gripper-demonstration | embodiment | `all:gripper AND all:"human demonstration" AND all:robot` | Search for lower-DOF gripper abstractions of human demonstrations. |
| retargeting-morphology-gap | limitation | `all:"morphology gap" AND all:robot` | Find papers that name embodiment mismatch as a transfer limit. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-egocentric-hand-detection, dynamic-egocentric-hand-pose, droid-robot-manipulation, ego4d-robot-learning, retargeting-robot-manipulation, ea-data-robot-demonstrations, ea-data-demonstration-quality |
| adjacent-and-transfer | 3 | dynamic-first-person-hand-tracking, dynamic-egocentric-hand-object, dynamic-hand-tracking-benchmark, dynamic-ego-exo-hand-ground-truth, dynamic-event-camera-hand-pose, dynamic-realtime-hoi-industrial, calibrated-egoev-handpose, calibrated-ego-exo-3d-hand-tracking, calibrated-bimanual-occlusion, calibrated-ego-motion-interference, calibration-ego-event-hand, calibration-ego-exo-hand, droid-ego-egocentric-video, droid-ego-in-the-wild, droid-ego-data-mixture, retargeting-human-to-robot-mapping, retargeting-dexterous-hand, retargeting-gripper-demonstration |
| limits-and-counterevidence | 3 | dynamic-hand-occlusion-motion-blur, dynamic-bimanual-identity, retargeting-morphology-gap |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-browser-egocentric-hand-2025 | `site:arxiv.org egocentric hand pose tracking occlusion 2025 2026` | Fallback for current papers poorly indexed by the arXiv API. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-web-egocentric-hand | llm | `egocentric hand tracking benchmark 2025 2026` | Discover current dataset and method names. |
| web-calibrated-egoev-handpose | arxiv-search | `"EgoEV-HandPose" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: EgoEV-HandPose. |
| web-calibrated-ego-exo-3d-hand-tracking | arxiv-search | `"ego-exo 3D hand tracking" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: ego-exo 3D hand tracking. |
| web-calibrated-bimanual-occlusion | arxiv-search | `"bimanual occlusion" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: bimanual occlusion. |
| web-calibrated-ego-motion-interference | arxiv-search | `"ego-motion interference" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: ego-motion interference. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-egocentric-hand-detection | arxiv_api | llm | high | `all:egocentric AND (all:"hand detection" OR all:"hand segmentation")` | Directly retrieves first-person hand localization and segmentation work. |
| dynamic-egocentric-hand-pose | arxiv_api | llm | high | `all:egocentric AND (all:"3D hand pose" OR all:"hand pose estimation" OR all:"hand mesh")` | Covers joint and mesh estimation, which are the dominant technical meanings of hand tracking in recent work. |
| dynamic-first-person-hand-tracking | arxiv_api | llm | high | `(all:"first-person" OR all:egocentric) AND all:hand AND (all:tracking OR all:temporal)` | Finds explicit temporal tracking and sequence-consistency work. |
| dynamic-egocentric-hand-object | arxiv_api | llm | high | `all:egocentric AND (all:"hand-object interaction" OR all:"hand object") AND (all:pose OR all:tracking OR all:detection)` | Interaction is the main source of self/object occlusion and contact ambiguity. |
| dynamic-hand-occlusion-motion-blur | arxiv_api | llm | high | `all:egocentric AND all:hand AND (all:occlusion OR all:"motion blur" OR all:truncation OR all:"ego-motion")` | Targets the dominant failure conditions rather than only successful methods. |
| dynamic-bimanual-identity | arxiv_api | llm | medium | `all:egocentric AND (all:bimanual OR all:"two hands") AND (all:tracking OR all:pose OR all:identity)` | Bimanual overlap and left/right identity swaps are a distinct tracking failure mode. |
| dynamic-hand-tracking-benchmark | arxiv_api | llm | high | `all:egocentric AND all:hand AND (all:benchmark OR all:dataset OR all:evaluation) AND (all:pose OR all:tracking)` | Retrieves datasets and evaluation protocols needed to audit annotation and metric gaps. |
| dynamic-ego-exo-hand-ground-truth | arxiv_api | llm | high | `(all:"ego-exo" OR all:multiview) AND all:hand AND (all:"ground truth" OR all:annotation OR all:tracking)` | Multi-view capture is the main route to accurate in-the-wild 3D hand ground truth. |
| dynamic-event-camera-hand-pose | arxiv_api | llm | medium | `all:egocentric AND all:hand AND (all:event OR all:stereo) AND (all:pose OR all:tracking)` | Event/stereo sensing directly addresses blur, dynamic range, and depth ambiguity. |
| dynamic-realtime-hoi-industrial | arxiv_api | llm | high | `all:egocentric AND all:hand AND (all:"real-time" OR all:streaming OR all:industrial) AND (all:detection OR all:tracking OR all:interaction)` | Surfaces latency, compute, and cascade-error trade-offs in deployable systems. |
| dynamic-browser-egocentric-hand-2025 | browser_fallback | llm | high | `site:arxiv.org egocentric hand pose tracking occlusion 2025 2026` | Fallback for current papers poorly indexed by the arXiv API. |
| dynamic-web-egocentric-hand | web_calibration | llm | high | `egocentric hand tracking benchmark 2025 2026` | Discover current dataset and method names. |

## Calibration Notes

- arxiv-search calibration (high): Recent terminology includes stereo event streams, KeypointBEV, bimanual occlusion, and ego-motion interference.
- arxiv-search calibration (high): Recent data terminology includes ego-exo 3D hand tracking, mobile multi-camera rig, in-the-wild, and marker-less ground truth.
- arxiv-search calibration (high): Deployment terminology includes streaming egocentric vision, active object detection, cascaded architecture, and real-time industrial domains.

## Planner Notes

- llm dynamic expansion (high): The static embodied-AI taxonomy under-specifies egocentric hand detection, hand mesh recovery, temporal identity tracking, and hand-object occlusion.
