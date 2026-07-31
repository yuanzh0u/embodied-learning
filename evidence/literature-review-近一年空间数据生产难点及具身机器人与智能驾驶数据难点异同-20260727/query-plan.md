# Query Plan: 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同

## Scope

- Knowledge IDs: EA-DATA, EA-SENSOR, EA-EVAL
- Families: teleoperation-demo-quality, tactile-force, world-model, sim2real
- Suggested categories: cs.AI, cs.CV, cs.HC, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 200
- Full-text floor: 40
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-robot-spatial-data-4d | core | `(all:"robot manipulation" OR all:"embodied AI") AND (all:"4D data" OR all:"3D point tracks" OR all:"spatiotemporal data")` | Find papers that make geometry and temporal correspondence explicit in robot data. |
| dynamic-robot-spatial-calibration | quality | `all:robot AND (all:"hand-eye calibration" OR all:"sensor calibration" OR all:"time synchronization") AND (all:dataset OR all:demonstration)` | Cover coordinate-frame and synchronization failures during robot dataset production. |
| dynamic-robot-occlusion-contact-data | limitation | `all:"robot manipulation" AND (all:occlusion OR all:contact OR all:deformable) AND (all:dataset OR all:data OR all:demonstration)` | Cover spatial state that vision cannot directly observe during contact-rich manipulation. |
| dynamic-robot-auto-annotation-3d | production | `all:robot AND (all:"automatic annotation" OR all:"pseudo label" OR all:"data engine") AND (all:3D OR all:spatial)` | Find scalable robot spatial labeling and its error modes. |
| dynamic-driving-spatial-data-core | core | `(all:"autonomous driving" OR all:"self-driving") AND (all:"spatial data" OR all:"3D data" OR all:"4D data") AND (all:dataset OR all:annotation OR all:generation)` | Direct autonomous-driving spatial-data production surface. |
| dynamic-driving-occupancy-data | representation | `all:"autonomous driving" AND (all:"3D occupancy" OR all:"4D occupancy" OR all:"occupancy flow") AND (all:dataset OR all:label OR all:benchmark)` | Occupancy is a major spatial representation whose ground truth is difficult to produce under occlusion. |
| dynamic-driving-hd-map-production | production | `all:"autonomous driving" AND (all:"HD map" OR all:"online mapping" OR all:"map update") AND (all:dataset OR all:annotation OR all:construction)` | Cover map creation, freshness, localization, and update costs. |
| dynamic-driving-calibration-sync | quality | `all:"autonomous driving" AND (all:"sensor calibration" OR all:"time synchronization" OR all:"multi-sensor dataset")` | Cover fleet-scale multi-sensor alignment and drift. |
| dynamic-driving-auto-labeling | production | `all:"autonomous driving" AND (all:"automatic annotation" OR all:"auto-labeling" OR all:"pseudo label") AND (all:3D OR all:LiDAR OR all:occupancy)` | Cover scalable 3D labeling and teacher/model bias. |
| dynamic-driving-long-tail-mining | limitation | `all:"autonomous driving" AND (all:"long tail" OR all:"rare scenario" OR all:"corner case") AND (all:dataset OR all:"data mining")` | Cover event rarity and log-selection difficulty rather than average road coverage. |
| dynamic-driving-generative-simulation | sim-real | `all:"autonomous driving" AND (all:"world model" OR all:"generative simulation" OR all:"synthetic data") AND (all:evaluation OR all:closed-loop OR all:sim2real)` | Cover generated spatial data, controllability, realism, and closed-loop validity. |
| dynamic-driving-adverse-weather-data | deployment | `all:"autonomous driving" AND (all:"adverse weather" OR all:night OR all:"sensor degradation") AND (all:dataset OR all:data)` | Cover environmental domain gaps and sensor failure regimes. |
| dynamic-cross-domain-spatial-ground-truth | evaluation | `(all:robotics OR all:"autonomous driving") AND (all:"spatial ground truth" OR all:"ground truth quality" OR all:"label uncertainty")` | Find methods and critiques about imperfect spatial ground truth across both domains. |
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
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| sim2real-core | core | `(all:sim2real OR all:"sim-to-real") AND all:robot` | Find the main simulation-to-real transfer literature surface. |
| sim2real-real-validation | validation | `all:"real robot" AND all:validation AND all:simulation` | Find papers that verify simulation claims against real robot runs. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-robot-spatial-data-4d, dynamic-robot-spatial-calibration, dynamic-driving-spatial-data-core, dynamic-driving-calibration-sync, teleop-imitation-learning, teleop-demonstration-quality, tactile-force-tactile-manipulation, world-model-robot, sim2real-core |
| limits-and-counterevidence | 3 | dynamic-robot-occlusion-contact-data, dynamic-driving-long-tail-mining, teleop-latency, world-model-contact, world-model-long-horizon |
| deployment-and-operations | 3 | dynamic-robot-auto-annotation-3d, dynamic-driving-hd-map-production, dynamic-driving-auto-labeling |
| mechanisms-and-interfaces | 3 | dynamic-driving-occupancy-data, teleop-action-interface |
| adjacent-and-transfer | 3 | dynamic-driving-generative-simulation, dynamic-driving-adverse-weather-data, dynamic-cross-domain-spatial-ground-truth, teleop-operator-burden, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, world-model-video-prediction, world-model-planning |
| evaluation-and-validation | 3 | sim2real-real-validation |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-driving-spatial-data-browser | `site:arxiv.org autonomous driving spatial data production occupancy auto labeling dataset 2025 2026` | Fallback discovery for driving papers under vocabulary missed by API queries. |
| dynamic-robot-spatial-data-browser | `site:arxiv.org robot manipulation 4D spatial data collection calibration contact dataset 2025 2026` | Fallback discovery for embodied spatial-data production papers. |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-topic-calibration | web | `"近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-robot-spatial-data-4d | arxiv_api | llm | high | `(all:"robot manipulation" OR all:"embodied AI") AND (all:"4D data" OR all:"3D point tracks" OR all:"spatiotemporal data")` | Find papers that make geometry and temporal correspondence explicit in robot data. |
| dynamic-robot-spatial-calibration | arxiv_api | llm | high | `all:robot AND (all:"hand-eye calibration" OR all:"sensor calibration" OR all:"time synchronization") AND (all:dataset OR all:demonstration)` | Cover coordinate-frame and synchronization failures during robot dataset production. |
| dynamic-robot-occlusion-contact-data | arxiv_api | llm | high | `all:"robot manipulation" AND (all:occlusion OR all:contact OR all:deformable) AND (all:dataset OR all:data OR all:demonstration)` | Cover spatial state that vision cannot directly observe during contact-rich manipulation. |
| dynamic-robot-auto-annotation-3d | arxiv_api | llm | medium | `all:robot AND (all:"automatic annotation" OR all:"pseudo label" OR all:"data engine") AND (all:3D OR all:spatial)` | Find scalable robot spatial labeling and its error modes. |
| dynamic-driving-spatial-data-core | arxiv_api | llm | high | `(all:"autonomous driving" OR all:"self-driving") AND (all:"spatial data" OR all:"3D data" OR all:"4D data") AND (all:dataset OR all:annotation OR all:generation)` | Direct autonomous-driving spatial-data production surface. |
| dynamic-driving-occupancy-data | arxiv_api | llm | high | `all:"autonomous driving" AND (all:"3D occupancy" OR all:"4D occupancy" OR all:"occupancy flow") AND (all:dataset OR all:label OR all:benchmark)` | Occupancy is a major spatial representation whose ground truth is difficult to produce under occlusion. |
| dynamic-driving-hd-map-production | arxiv_api | llm | high | `all:"autonomous driving" AND (all:"HD map" OR all:"online mapping" OR all:"map update") AND (all:dataset OR all:annotation OR all:construction)` | Cover map creation, freshness, localization, and update costs. |
| dynamic-driving-calibration-sync | arxiv_api | llm | high | `all:"autonomous driving" AND (all:"sensor calibration" OR all:"time synchronization" OR all:"multi-sensor dataset")` | Cover fleet-scale multi-sensor alignment and drift. |
| dynamic-driving-auto-labeling | arxiv_api | llm | high | `all:"autonomous driving" AND (all:"automatic annotation" OR all:"auto-labeling" OR all:"pseudo label") AND (all:3D OR all:LiDAR OR all:occupancy)` | Cover scalable 3D labeling and teacher/model bias. |
| dynamic-driving-long-tail-mining | arxiv_api | llm | high | `all:"autonomous driving" AND (all:"long tail" OR all:"rare scenario" OR all:"corner case") AND (all:dataset OR all:"data mining")` | Cover event rarity and log-selection difficulty rather than average road coverage. |
| dynamic-driving-generative-simulation | arxiv_api | llm | high | `all:"autonomous driving" AND (all:"world model" OR all:"generative simulation" OR all:"synthetic data") AND (all:evaluation OR all:closed-loop OR all:sim2real)` | Cover generated spatial data, controllability, realism, and closed-loop validity. |
| dynamic-driving-adverse-weather-data | arxiv_api | llm | high | `all:"autonomous driving" AND (all:"adverse weather" OR all:night OR all:"sensor degradation") AND (all:dataset OR all:data)` | Cover environmental domain gaps and sensor failure regimes. |
| dynamic-cross-domain-spatial-ground-truth | arxiv_api | llm | high | `(all:robotics OR all:"autonomous driving") AND (all:"spatial ground truth" OR all:"ground truth quality" OR all:"label uncertainty")` | Find methods and critiques about imperfect spatial ground truth across both domains. |
| dynamic-driving-spatial-data-browser | browser_fallback | llm | high | `site:arxiv.org autonomous driving spatial data production occupancy auto labeling dataset 2025 2026` | Fallback discovery for driving papers under vocabulary missed by API queries. |
| dynamic-robot-spatial-data-browser | browser_fallback | llm | high | `site:arxiv.org robot manipulation 4D spatial data collection calibration contact dataset 2025 2026` | Fallback discovery for embodied spatial-data production papers. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (high): The static embodied-AI taxonomy lacks autonomous-driving spatial-data production, so this expansion creates balanced robot and driving evidence surfaces.
