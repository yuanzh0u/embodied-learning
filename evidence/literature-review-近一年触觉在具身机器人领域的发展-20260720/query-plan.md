# Query Plan: 近一年触觉在具身机器人领域的发展

## Scope

- Knowledge IDs: EA-SENSOR, EA-DATA, EA-MODEL, EA-EVAL
- Families: tactile-force, world-model, industrial-deployment
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 160
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-tactile-foundation-representation | dynamic-association | `(all:tactile OR all:haptic) AND (all:"foundation model" OR all:pretraining OR all:representation) AND all:robot` | Capture tactile encoders, pretrained representations, and generalist tactile models. |
| dynamic-tactile-vla-policy | dynamic-association | `(all:tactile OR all:touch OR all:haptic) AND (all:"vision language action" OR all:VLA OR all:policy) AND all:robot` | Capture tactile injection into VLA and visuomotor policy stacks. |
| dynamic-tactile-world-action-model | dynamic-association | `(all:tactile OR all:touch) AND (all:"world model" OR all:"world action model" OR all:prediction) AND all:manipulation` | Capture predictive contact models and inference-time action verification. |
| dynamic-tactile-dexterous-soft | dynamic-association | `(all:tactile OR all:touch) AND (all:dexterous OR all:"deformable object" OR all:insertion OR all:assembly) AND all:robot` | Capture contact-rich dexterous, deformable, insertion, and assembly task evidence. |
| dynamic-robot-skin-whole-body | dynamic-association | `(all:"robot skin" OR all:e-skin OR all:"whole-body tactile" OR all:"foot contact") AND (all:humanoid OR all:robot)` | Capture large-area tactile skin, humanoid body contact, and locomotion-contact sensing. |
| dynamic-tactile-dataset-benchmark | dynamic-association | `(all:tactile OR all:visuotactile) AND (all:dataset OR all:benchmark OR all:evaluation) AND all:robot` | Capture datasets, benchmarks, cross-sensor evaluation, and safety metrics. |
| dynamic-tactile-calibration-drift | dynamic-association | `(all:tactile OR all:force) AND (all:calibration OR all:drift OR all:wear OR all:"cross-sensor") AND all:robot` | Capture sensor-instance transfer, calibration, drift, wear, and maintenance limitations. |
| dynamic-tactile-negative-evidence | dynamic-association | `(all:tactile OR all:haptic) AND (all:failure OR all:limitation OR all:latency OR all:noise) AND all:"robot manipulation"` | Capture explicit negative results and deployment constraints. |
| calibrated-touchworld | calibrated-term | `all:TouchWorld` | Recent tactile foundation model alias. |
| calibrated-taco | calibrated-term | `all:TacO` | Recent task-driven tactile sensor benchmark alias. |
| calibrated-ht-bench | calibrated-term | `all:"HT-Bench"` | Recent full-hand tactile representation benchmark alias. |
| calibrated-handtouch | calibrated-term | `all:HandTouch` | Recent vision-tactile encoder alias. |
| calibrated-tactidex | calibrated-term | `all:TactiDex` | Recent tactile-guided dexterous benchmark alias. |
| calibrated-contact-level-human-likeness | calibrated-term | `all:"contact-level human-likeness"` | Evaluation framing beyond kinematic imitation. |
| calibration-touchworld | calibrated-query | `all:TouchWorld OR all:"predictive reactive tactile"` | Recover the TouchWorld lineage and adjacent predictive/reactive tactile policies. |
| calibration-tactile-benchmarks | calibrated-query | `all:TacO OR all:TactiDex OR all:"HT-Bench" OR all:HandTouch` | Recover recent tactile sensor, representation, and dexterous transfer benchmarks. |
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
| industrial-deployment-core | core | `all:"industrial robot" AND all:deployment` | Find deployment papers in manufacturing or production contexts. |
| industrial-deployment-reliability | reliability | `all:reliability AND all:robot AND all:deployment` | Capture uptime, fault tolerance, and long-run operational evidence. |
| industrial-deployment-cycle-time | production | `all:"cycle time" AND all:automation AND all:robot` | Find throughput constraints that affect ToB feasibility. |
| industrial-deployment-yield | production-quality | `all:yield AND all:robot AND all:manufacturing` | Surface quality and yield discussions beyond one-off success rate. |
| industrial-deployment-acceptance-testing | evaluation | `all:"acceptance testing" AND all:robot` | Find validation and acceptance language for production handoff. |
| industrial-deployment-roi | business-adjacent | `all:ROI AND all:robot AND all:automation` | Search for cost or return-on-investment framing when present in technical metadata. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-tactile-foundation-representation, dynamic-tactile-vla-policy, dynamic-tactile-world-action-model, dynamic-tactile-dexterous-soft, dynamic-robot-skin-whole-body, dynamic-tactile-dataset-benchmark, dynamic-tactile-calibration-drift, dynamic-tactile-negative-evidence, calibrated-touchworld, calibrated-taco, calibrated-ht-bench, calibrated-handtouch, calibrated-tactidex, calibrated-contact-level-human-likeness, calibration-touchworld, calibration-tactile-benchmarks, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, world-model-video-prediction, world-model-planning, industrial-deployment-acceptance-testing, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-data-in-the-wild, ea-data-dataset-curation |
| direct-topic | 3 | tactile-force-tactile-manipulation, world-model-robot, industrial-deployment-core, ea-sensor-multimodal-policy, ea-data-robot-demonstrations, ea-data-demonstration-quality |
| limits-and-counterevidence | 3 | world-model-contact, world-model-long-horizon, ea-sensor-occlusion |
| deployment-and-operations | 3 | industrial-deployment-reliability, industrial-deployment-cycle-time, industrial-deployment-yield, industrial-deployment-roi |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-tactile-robotics-browser | `site:arxiv.org/abs (tactile OR visuotactile OR haptic) robot manipulation 2025 2026` | Browser fallback for broad recent tactile robotics discovery. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-tactile-calibration-web | llm | `tactile robotics 2026 dataset world model VLA robot skin` | Find fresh method aliases and benchmark names before finalizing search terms. |
| web-calibrated-touchworld | arxiv-web | `"TouchWorld" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: TouchWorld. |
| web-calibrated-taco | arxiv-web | `"TacO" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: TacO. |
| web-calibrated-ht-bench | arxiv-web | `"HT-Bench" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: HT-Bench. |
| web-calibrated-handtouch | arxiv-web | `"HandTouch" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: HandTouch. |
| web-calibrated-tactidex | arxiv-web | `"TactiDex" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: TactiDex. |
| web-calibrated-contact-level-human-likeness | arxiv-web | `"contact-level human-likeness" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: contact-level human-likeness. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-tactile-foundation-representation | arxiv_api | llm | medium | `(all:tactile OR all:haptic) AND (all:"foundation model" OR all:pretraining OR all:representation) AND all:robot` | Capture tactile encoders, pretrained representations, and generalist tactile models. |
| dynamic-tactile-vla-policy | arxiv_api | llm | medium | `(all:tactile OR all:touch OR all:haptic) AND (all:"vision language action" OR all:VLA OR all:policy) AND all:robot` | Capture tactile injection into VLA and visuomotor policy stacks. |
| dynamic-tactile-world-action-model | arxiv_api | llm | medium | `(all:tactile OR all:touch) AND (all:"world model" OR all:"world action model" OR all:prediction) AND all:manipulation` | Capture predictive contact models and inference-time action verification. |
| dynamic-tactile-dexterous-soft | arxiv_api | llm | medium | `(all:tactile OR all:touch) AND (all:dexterous OR all:"deformable object" OR all:insertion OR all:assembly) AND all:robot` | Capture contact-rich dexterous, deformable, insertion, and assembly task evidence. |
| dynamic-robot-skin-whole-body | arxiv_api | llm | medium | `(all:"robot skin" OR all:e-skin OR all:"whole-body tactile" OR all:"foot contact") AND (all:humanoid OR all:robot)` | Capture large-area tactile skin, humanoid body contact, and locomotion-contact sensing. |
| dynamic-tactile-dataset-benchmark | arxiv_api | llm | medium | `(all:tactile OR all:visuotactile) AND (all:dataset OR all:benchmark OR all:evaluation) AND all:robot` | Capture datasets, benchmarks, cross-sensor evaluation, and safety metrics. |
| dynamic-tactile-calibration-drift | arxiv_api | llm | medium | `(all:tactile OR all:force) AND (all:calibration OR all:drift OR all:wear OR all:"cross-sensor") AND all:robot` | Capture sensor-instance transfer, calibration, drift, wear, and maintenance limitations. |
| dynamic-tactile-negative-evidence | arxiv_api | llm | medium | `(all:tactile OR all:haptic) AND (all:failure OR all:limitation OR all:latency OR all:noise) AND all:"robot manipulation"` | Capture explicit negative results and deployment constraints. |
| dynamic-tactile-robotics-browser | browser_fallback | llm | medium | `site:arxiv.org/abs (tactile OR visuotactile OR haptic) robot manipulation 2025 2026` | Browser fallback for broad recent tactile robotics discovery. |
| dynamic-tactile-calibration-web | web_calibration | llm | medium | `tactile robotics 2026 dataset world model VLA robot skin` | Find fresh method aliases and benchmark names before finalizing search terms. |

## Calibration Notes

- arxiv-web calibration (high): TouchWorld uses predictive-and-reactive tactile foundation model terminology.
- arxiv-web calibration (high): TacO frames task-driven cross-modality tactile sensor benchmarking.
- arxiv-web calibration (high): HT-Bench introduces full-hand tactile representation learning with egocentric vision.
- arxiv-web calibration (high): TactiDex uses contact-level human-likeness and tactile-guided transfer terminology.

## Planner Notes

- llm dynamic expansion (medium): Broad tactile-in-embodied-robotics framing requires sensor, representation, policy, whole-body, evaluation, and deployment surfaces beyond the static tactile-force family.
