# Query Plan: 近一年具身感知与导航是否已解决

## Scope

- Knowledge IDs: EA-SENSOR, EA-EVAL, EA-MODEL
- Families: world-model, sim2real
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 100
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-embodied-perception-real-world | dynamic-association | `all:"embodied perception" AND (all:robot OR all:agent) AND (all:real-world OR all:benchmark)` | Capture work that evaluates perception as an embodied closed-loop capability rather than an isolated vision metric. |
| dynamic-open-vocabulary-3d-navigation | dynamic-association | `(all:"open-vocabulary" OR all:"open world") AND (all:"3D scene" OR all:"scene graph") AND all:navigation` | Cover semantic and geometric scene understanding used by navigation under unseen categories and environments. |
| dynamic-active-perception-navigation | dynamic-association | `all:"active perception" AND (all:navigation OR all:exploration) AND all:robot` | Perception in embodied systems is action-dependent; active sensing exposes whether passive perception is sufficient. |
| dynamic-vln-generalization | evaluation | `(all:"vision-language navigation" OR all:VLN) AND (all:generalization OR all:robustness OR all:"unseen environment")` | Capture recent claims and limits in language-conditioned navigation beyond seen simulators. |
| dynamic-objectgoal-zero-shot | evaluation | `(all:"object goal navigation" OR all:ObjectNav) AND (all:"zero-shot" OR all:"open-vocabulary" OR all:generalization)` | Cover target-driven navigation with unseen objects and categories. |
| dynamic-navigation-world-model-long-horizon | mechanism | `all:"robot navigation" AND (all:"world model" OR all:"video prediction") AND (all:"long horizon" OR all:planning)` | Test whether predictive models resolve long-horizon state estimation and planning, or merely improve rollout quality. |
| dynamic-navigation-dynamic-social | adjacent | `all:"robot navigation" AND (all:dynamic OR all:social OR all:human-aware) AND (all:real-world OR all:deployment)` | Static indoor benchmarks understate navigation difficulty around moving people and changing layouts. |
| dynamic-navigation-sim2real-robustness | limitation | `all:navigation AND all:robot AND (all:sim2real OR all:"sim-to-real") AND (all:failure OR all:robustness OR all:uncertainty)` | Cover transfer gaps hidden by simulator-only evaluation. |
| dynamic-navigation-deployment-recovery | deployment | `all:"mobile robot" AND all:navigation AND (all:deployment OR all:"long-term autonomy" OR all:recovery) AND (all:failure OR all:safety OR all:reliability)` | Search for sustained autonomy, recovery, and safety evidence needed to call navigation solved. |
| dynamic-navigation-benchmark-saturation | limitation | `(all:VLN OR all:ObjectNav OR all:"embodied navigation") AND (all:benchmark OR all:evaluation) AND (all:limitation OR all:bias OR all:failure)` | Find benchmark critiques and failure analyses that qualify headline scores. |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| sim2real-core | core | `(all:sim2real OR all:"sim-to-real") AND all:robot` | Find the main simulation-to-real transfer literature surface. |
| sim2real-real-validation | validation | `all:"real robot" AND all:validation AND all:simulation` | Find papers that verify simulation claims against real robot runs. |
| sim2real-synthetic-data | data-generation | `all:"synthetic data" AND all:"robot manipulation"` | Capture synthetic-data pipelines used to reduce real collection cost. |
| sim2real-domain-randomization | method | `all:"domain randomization" AND all:"robot manipulation"` | Find robustification methods for visual and physical sim-to-real gaps. |
| sim2real-correlation | evaluation | `all:"sim-real" AND all:correlation AND all:evaluation` | Surface work that measures whether simulation rankings predict real performance. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-embodied-perception-real-world, dynamic-open-vocabulary-3d-navigation, dynamic-active-perception-navigation, dynamic-vln-generalization, dynamic-objectgoal-zero-shot, dynamic-navigation-world-model-long-horizon, dynamic-navigation-dynamic-social, dynamic-navigation-deployment-recovery, world-model-video-prediction, world-model-planning, sim2real-synthetic-data, sim2real-correlation, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| limits-and-counterevidence | 3 | dynamic-navigation-sim2real-robustness, dynamic-navigation-benchmark-saturation, world-model-contact, world-model-long-horizon, ea-sensor-occlusion |
| direct-topic | 3 | world-model-robot, sim2real-core, ea-sensor-multimodal-policy, ea-eval-closed-loop, ea-model-vla, ea-model-named-foundation |
| evaluation-and-validation | 3 | sim2real-real-validation |
| mechanisms-and-interfaces | 3 | sim2real-domain-randomization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-navigation-real-world-browser | `site:arxiv.org/abs ("vision-language navigation" OR ObjectNav) real-world robot failure 2025 2026` | Find real-world evaluations and failure analyses if API recall is weak. |
| dynamic-perception-navigation-gap-browser | `site:arxiv.org/abs embodied perception navigation benchmark limitation robustness 2025 2026` | Calibrate recent vocabulary for unresolved perception-navigation interfaces. |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-navigation-calibration | llm | `embodied navigation real world benchmark 2025 2026 perception robustness` | Calibrate current task names and benchmark terminology. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-embodied-perception-real-world | arxiv_api | llm | high | `all:"embodied perception" AND (all:robot OR all:agent) AND (all:real-world OR all:benchmark)` | Capture work that evaluates perception as an embodied closed-loop capability rather than an isolated vision metric. |
| dynamic-open-vocabulary-3d-navigation | arxiv_api | llm | high | `(all:"open-vocabulary" OR all:"open world") AND (all:"3D scene" OR all:"scene graph") AND all:navigation` | Cover semantic and geometric scene understanding used by navigation under unseen categories and environments. |
| dynamic-active-perception-navigation | arxiv_api | llm | high | `all:"active perception" AND (all:navigation OR all:exploration) AND all:robot` | Perception in embodied systems is action-dependent; active sensing exposes whether passive perception is sufficient. |
| dynamic-vln-generalization | arxiv_api | llm | high | `(all:"vision-language navigation" OR all:VLN) AND (all:generalization OR all:robustness OR all:"unseen environment")` | Capture recent claims and limits in language-conditioned navigation beyond seen simulators. |
| dynamic-objectgoal-zero-shot | arxiv_api | llm | high | `(all:"object goal navigation" OR all:ObjectNav) AND (all:"zero-shot" OR all:"open-vocabulary" OR all:generalization)` | Cover target-driven navigation with unseen objects and categories. |
| dynamic-navigation-world-model-long-horizon | arxiv_api | llm | medium | `all:"robot navigation" AND (all:"world model" OR all:"video prediction") AND (all:"long horizon" OR all:planning)` | Test whether predictive models resolve long-horizon state estimation and planning, or merely improve rollout quality. |
| dynamic-navigation-dynamic-social | arxiv_api | llm | high | `all:"robot navigation" AND (all:dynamic OR all:social OR all:human-aware) AND (all:real-world OR all:deployment)` | Static indoor benchmarks understate navigation difficulty around moving people and changing layouts. |
| dynamic-navigation-sim2real-robustness | arxiv_api | llm | high | `all:navigation AND all:robot AND (all:sim2real OR all:"sim-to-real") AND (all:failure OR all:robustness OR all:uncertainty)` | Cover transfer gaps hidden by simulator-only evaluation. |
| dynamic-navigation-deployment-recovery | arxiv_api | llm | high | `all:"mobile robot" AND all:navigation AND (all:deployment OR all:"long-term autonomy" OR all:recovery) AND (all:failure OR all:safety OR all:reliability)` | Search for sustained autonomy, recovery, and safety evidence needed to call navigation solved. |
| dynamic-navigation-benchmark-saturation | arxiv_api | llm | high | `(all:VLN OR all:ObjectNav OR all:"embodied navigation") AND (all:benchmark OR all:evaluation) AND (all:limitation OR all:bias OR all:failure)` | Find benchmark critiques and failure analyses that qualify headline scores. |
| dynamic-navigation-real-world-browser | browser_fallback | llm | high | `site:arxiv.org/abs ("vision-language navigation" OR ObjectNav) real-world robot failure 2025 2026` | Find real-world evaluations and failure analyses if API recall is weak. |
| dynamic-perception-navigation-gap-browser | browser_fallback | llm | medium | `site:arxiv.org/abs embodied perception navigation benchmark limitation robustness 2025 2026` | Calibrate recent vocabulary for unresolved perception-navigation interfaces. |
| dynamic-navigation-calibration | web_calibration | llm | medium | `embodied navigation real world benchmark 2025 2026 perception robustness` | Calibrate current task names and benchmark terminology. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (high): The static taxonomy has perception and evaluation routes but no dedicated navigation family, so this run adds navigation task families and explicit limitation/deployment surfaces.
