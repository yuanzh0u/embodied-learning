# Query Plan: 近一年具身智能预训练模型对数据源多样性及相机分辨率帧率码率FOV机位的要求

## Scope

- Knowledge IDs: EA-DATA, EA-HARDWARE, EA-SENSOR, EA-MODEL, EA-XEMBODIMENT
- Families: vla, droid-ego4d, teleoperation-demo-quality, retargeting, sim2real
- Suggested categories: cs.AI, cs.CV, cs.HC, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 160
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-heterogeneous-vla-pretraining | dynamic-association | `(all:"vision-language-action" OR all:"robot foundation model") AND (all:heterogeneous OR all:"data mixture" OR all:"multi-embodiment")` | Find recent VLA work that explicitly studies heterogeneous source mixtures and cross-embodiment pretraining. |
| dynamic-capture-parameters | dynamic-association | `(all:"robot learning" OR all:"robot dataset") AND (all:"camera resolution" OR all:"frame rate" OR all:"field of view")` | Recover dataset and system papers that disclose capture resolution, temporal rate, FOV, and camera placement. |
| dynamic-viewpoint-camera-domain | dynamic-association | `(all:"robot pretraining" OR all:"vision-language-action") AND (all:viewpoint OR all:"camera domain" OR all:egocentric OR all:wrist-camera)` | Test whether viewpoint and camera-domain diversity are learned as invariances or require explicit alignment. |
| dynamic-negative-transfer-diversity | dynamic-association | `(all:"robot manipulation" OR all:"vision-language-action") AND (all:"negative transfer" OR all:"expert diversity" OR all:"embodiment gap" OR all:"action mismatch")` | Find counterevidence to the intuition that every additional source or collection setup improves pretraining. |
| calibrated-reliability-aware-heterogeneous-pretraining | calibrated-term | `all:"reliability-aware heterogeneous pretraining"` | Separates source diversity from supervision reliability. |
| calibrated-camera-space-actions | calibrated-term | `all:"camera-space actions"` | A current interface for aligning human and robot visual-action data. |
| calibrated-viewpoint-action | calibrated-term | `all:"viewpoint action"` | Captures the fact that camera motion may be policy-relevant behavior. |
| calibrated-motion-transfer | calibrated-term | `all:"motion transfer"` | Current terminology for exploiting heterogeneous multi-embodiment data. |
| calibration-reliability-aware-heterogeneous | calibrated-query | `all:"reliability-aware" AND (all:egocentric OR all:"vision-language-action")` | Find methods that explicitly weight heterogeneous pseudo-action supervision by reliability. |
| calibration-viewpoint-action | calibrated-query | `all:"viewpoint action" OR (all:"active perception" AND all:egocentric AND all:robot)` | Find pretraining approaches that model camera motion as behavior. |
| calibration-motion-transfer | calibrated-query | `all:"motion transfer" AND (all:"multi-embodiment" OR all:"vision-language-action")` | Find current heterogeneous robot-data alignment mechanisms. |
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
| retargeting-robot-manipulation | core | `all:retargeting AND all:"robot manipulation"` | Find the broad retargeting literature for manipulation tasks. |
| retargeting-human-to-robot-mapping | transfer | `all:"human-to-robot" AND all:mapping` | Capture human motion or hand data mapped onto robot embodiments. |
| retargeting-dexterous-hand | embodiment | `all:"dexterous hand" AND all:retargeting` | Find fine-grained human hand to dexterous hand transfer papers. |
| retargeting-gripper-demonstration | embodiment | `all:gripper AND all:"human demonstration" AND all:robot` | Search for lower-DOF gripper abstractions of human demonstrations. |
| retargeting-morphology-gap | limitation | `all:"morphology gap" AND all:robot` | Find papers that name embodiment mismatch as a transfer limit. |
| sim2real-core | core | `(all:sim2real OR all:"sim-to-real") AND all:robot` | Find the main simulation-to-real transfer literature surface. |
| sim2real-real-validation | validation | `all:"real robot" AND all:validation AND all:simulation` | Find papers that verify simulation claims against real robot runs. |
| sim2real-synthetic-data | data-generation | `all:"synthetic data" AND all:"robot manipulation"` | Capture synthetic-data pipelines used to reduce real collection cost. |
| sim2real-domain-randomization | method | `all:"domain randomization" AND all:"robot manipulation"` | Find robustification methods for visual and physical sim-to-real gaps. |
| sim2real-correlation | evaluation | `all:"sim-real" AND all:correlation AND all:evaluation` | Surface work that measures whether simulation rankings predict real performance. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-heterogeneous-vla-pretraining, dynamic-capture-parameters, dynamic-viewpoint-camera-domain, dynamic-negative-transfer-diversity, calibrated-reliability-aware-heterogeneous-pretraining, calibrated-camera-space-actions, calibrated-viewpoint-action, calibrated-motion-transfer, calibration-reliability-aware-heterogeneous, calibration-viewpoint-action, calibration-motion-transfer, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, droid-ego-egocentric-video, droid-ego-in-the-wild, droid-ego-data-mixture, teleop-operator-burden, retargeting-human-to-robot-mapping, retargeting-dexterous-hand, retargeting-gripper-demonstration, sim2real-synthetic-data, sim2real-correlation |
| direct-topic | 3 | vla-core, vla-named-models, droid-robot-manipulation, ego4d-robot-learning, teleop-imitation-learning, teleop-demonstration-quality, retargeting-robot-manipulation, sim2real-core, ea-data-robot-demonstrations |
| limits-and-counterevidence | 3 | vla-negative-transfer, teleop-latency, retargeting-morphology-gap |
| mechanisms-and-interfaces | 3 | teleop-action-interface, sim2real-domain-randomization |
| evaluation-and-validation | 3 | sim2real-real-validation |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-specs-browser | `site:arxiv.org/abs robot dataset camera resolution fps FOV wrist camera VLA 2025 2026` | Search full paper records for capture specifications that may be absent from metadata. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-current-data-mixtures-web | llm | `site:arxiv.org/abs 2026 VLA heterogeneous data sources egocentric robot simulation pretraining` | Calibrate current terminology for mixed-source VLA pretraining. |
| web-calibrated-reliability-aware-heterogeneous-pretraining | arxiv | `"reliability-aware heterogeneous pretraining" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: reliability-aware heterogeneous pretraining. |
| web-calibrated-camera-space-actions | arxiv | `"camera-space actions" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: camera-space actions. |
| web-calibrated-viewpoint-action | arxiv | `"viewpoint action" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: viewpoint action. |
| web-calibrated-motion-transfer | arxiv | `"motion transfer" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: motion transfer. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-heterogeneous-vla-pretraining | arxiv_api | llm | medium | `(all:"vision-language-action" OR all:"robot foundation model") AND (all:heterogeneous OR all:"data mixture" OR all:"multi-embodiment")` | Find recent VLA work that explicitly studies heterogeneous source mixtures and cross-embodiment pretraining. |
| dynamic-capture-parameters | arxiv_api | llm | medium | `(all:"robot learning" OR all:"robot dataset") AND (all:"camera resolution" OR all:"frame rate" OR all:"field of view")` | Recover dataset and system papers that disclose capture resolution, temporal rate, FOV, and camera placement. |
| dynamic-viewpoint-camera-domain | arxiv_api | llm | medium | `(all:"robot pretraining" OR all:"vision-language-action") AND (all:viewpoint OR all:"camera domain" OR all:egocentric OR all:wrist-camera)` | Test whether viewpoint and camera-domain diversity are learned as invariances or require explicit alignment. |
| dynamic-negative-transfer-diversity | arxiv_api | llm | medium | `(all:"robot manipulation" OR all:"vision-language-action") AND (all:"negative transfer" OR all:"expert diversity" OR all:"embodiment gap" OR all:"action mismatch")` | Find counterevidence to the intuition that every additional source or collection setup improves pretraining. |
| dynamic-specs-browser | browser_fallback | llm | medium | `site:arxiv.org/abs robot dataset camera resolution fps FOV wrist camera VLA 2025 2026` | Search full paper records for capture specifications that may be absent from metadata. |
| dynamic-current-data-mixtures-web | web_calibration | llm | medium | `site:arxiv.org/abs 2026 VLA heterogeneous data sources egocentric robot simulation pretraining` | Calibrate current terminology for mixed-source VLA pretraining. |

## Calibration Notes

- arxiv calibration (high): ACE-Ego-0 uses the current terms reliability-aware weighting, camera-space actions, morphology conditioning, and time-aligned action chunking for heterogeneous human/robot/simulation pretraining.
- arxiv calibration (high): ActiveMimic treats egocentric camera motion as a viewpoint action rather than nuisance noise.
- arxiv calibration (high): HumanEgo foregrounds entity-level hand-object interaction and transfer across novel robots, cameras, and environments.
- arxiv calibration (high): Gemini Robotics 1.5 uses motion transfer terminology for heterogeneous multi-embodiment robot data.

## Planner Notes

- llm dynamic expansion (medium): The review needs to connect model-level heterogeneous pretraining with capture-device, viewpoint, temporal, codec, and embodiment-interface constraints.
