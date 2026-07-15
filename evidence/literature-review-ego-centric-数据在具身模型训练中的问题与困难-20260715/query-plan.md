# Query Plan: Ego-centric 数据在具身模型训练中的问题与困难

## Scope

- Knowledge IDs: EA-DATA, EA-XEMBODIMENT, EA-MODEL, EA-SENSOR
- Families: droid-ego4d, retargeting, vla, teleoperation-demo-quality
- Suggested categories: cs.AI, cs.CV, cs.HC, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 200
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-egocentric-robot-learning | dynamic-association | `all:"egocentric video" AND (all:"robot learning" OR all:"robot manipulation")` | 直接覆盖第一视角视频用于机器人学习。 |
| dynamic-first-person-demonstration | dynamic-association | `all:"first-person video" AND (all:robot OR all:manipulation)` | 补充不使用 egocentric 术语的第一视角论文。 |
| dynamic-human-video-policy | dynamic-association | `all:"human video" AND (all:"robot policy" OR all:"imitation learning")` | 覆盖从人类视频学习机器人策略的主线。 |
| dynamic-ego-to-robot | transfer | `(all:"ego-to-robot" OR all:"human-to-robot") AND (all:video OR all:demonstration)` | 覆盖跨本体迁移与 embodiment gap。 |
| dynamic-hand-object-interface | representation | `all:"hand-object interaction" AND (all:robot OR all:policy)` | 手—物交互是将人类第一视角视频转成机器人可执行表征的常见接口。 |
| dynamic-latent-pseudo-action | policy-interface | `(all:"latent action" OR all:"pseudo action") AND (all:"human video" OR all:egocentric) AND all:robot` | 覆盖无原生机器人动作标签时的替代监督。 |
| dynamic-egocentric-trajectory-extraction | quality | `all:egocentric AND (all:"6DoF trajectory" OR all:"object trajectory" OR all:"hand pose") AND all:robot` | 覆盖从原始第一视角视频恢复运动轨迹及其噪声问题。 |
| dynamic-egocentric-observability-limit | limitation | `all:egocentric AND (all:occlusion OR all:contact OR all:"camera motion" OR all:visibility) AND (all:robot OR all:manipulation)` | 覆盖遮挡、接触不可观测和相机自运动等数据缺陷。 |
| dynamic-egocentric-vla-pretraining | named-method | `all:egocentric AND (all:VLA OR all:"vision language action") AND (all:pretraining OR all:"pre-training")` | 覆盖第一视角视频用于 VLA 预训练的直接证据。 |
| calibrated-entity-level-hand-object-interaction | calibrated-term | `all:"entity-level hand-object interaction"` | HumanEgo 用于缩小视觉外观与运动学本体差距。 |
| calibrated-6dof-object-manipulation-trajectories | calibrated-term | `all:"6DoF object manipulation trajectories"` | EgoScaler 将原始 ego 视频转成 VLA 可用轨迹。 |
| calibrated-noisy-or-incomplete-trajectories | calibrated-term | `all:"noisy or incomplete trajectories"` | 直接指向轨迹恢复和质量控制问题。 |
| calibration-humanego-interface | calibrated-query | `all:"hand-object interaction" AND all:egocentric AND all:robot` | 回收 HumanEgo 及相邻实体级接口论文。 |
| calibration-egoscaler-trajectories | calibrated-query | `all:"6DoF object manipulation trajectories" OR (all:EgoScaler AND all:robot)` | 回收原始 egocentric 视频到动作轨迹的直接论文。 |
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
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |
| vla-large-scale-robot-data | data-scaling | `all:"large-scale" AND all:"robot data"` | Surface scaling and dataset-layer discussions for robot foundation models. |
| vla-robot-foundation-action | foundation-model | `all:"robot foundation model" AND all:action` | Find broader foundation-model papers whose metadata may not use VLA. |
| vla-finetuning-policy | transfer | `all:"fine-tuning" AND all:"robot policy"` | Surface evidence about target-task adaptation and data requirements. |
| vla-data-mixture | data-mixture | `all:"data mixture" AND all:"robot foundation model"` | Find mixture and dataset composition papers that explain scaling behavior. |
| vla-negative-transfer | limitation | `all:"negative transfer" AND all:robot AND all:policy` | Search for failure cases where broad pretraining hurts target deployment. |
| teleop-imitation-learning | core | `all:teleoperation AND all:"imitation learning" AND all:robot` | Find the main literature surface connecting teleoperation to robot policy learning. |
| teleop-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface trace consistency, operator skill, and data acceptance criteria. |
| teleop-operator-burden | human-factor | `all:operator AND all:burden AND all:teleoperation` | Find papers about human workload and collection throughput. |
| teleop-latency | system-limitation | `all:latency AND all:teleoperation AND all:robot` | Capture delay and synchronization limits that affect demonstration fidelity. |
| teleop-action-interface | policy-interface | `all:"action interface" AND all:robot AND all:demonstration` | Find work where action-space choices determine whether demonstrations transfer. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-egocentric-robot-learning, dynamic-first-person-demonstration, dynamic-human-video-policy, dynamic-ego-to-robot, calibrated-entity-level-hand-object-interaction, calibrated-6dof-object-manipulation-trajectories, calibrated-noisy-or-incomplete-trajectories, calibration-humanego-interface, calibration-egoscaler-trajectories, droid-ego-egocentric-video, droid-ego-in-the-wild, droid-ego-data-mixture, retargeting-human-to-robot-mapping, retargeting-dexterous-hand, retargeting-gripper-demonstration, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, teleop-operator-burden, ea-data-in-the-wild, ea-data-dataset-curation, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot, ea-model-finetuning, ea-sensor-tactile-force, ea-sensor-point-cloud |
| mechanisms-and-interfaces | 3 | dynamic-hand-object-interface, dynamic-latent-pseudo-action, teleop-action-interface, ea-xembodiment-action-representation, ea-model-action-tokenization |
| direct-topic | 3 | dynamic-egocentric-trajectory-extraction, dynamic-egocentric-vla-pretraining, droid-robot-manipulation, ego4d-robot-learning, retargeting-robot-manipulation, vla-core, vla-named-models, teleop-imitation-learning, teleop-demonstration-quality, ea-data-robot-demonstrations, ea-xembodiment-cross-embodiment, ea-model-named-foundation, ea-sensor-multimodal-policy |
| limits-and-counterevidence | 3 | dynamic-egocentric-observability-limit, retargeting-morphology-gap, vla-negative-transfer, teleop-latency |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-egocentric-training-challenges-browser | `site:arxiv.org/abs (egocentric OR first-person) human video robot learning embodiment gap action labels occlusion` | 发现 API 元数据可能漏掉的挑战型论文。 |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-egocentric-robot-terms-web | llm | `site:arxiv.org/abs egocentric human video robot policy 2025 2026` | 校准近一年方法名与数据处理术语。 |
| web-calibrated-entity-level-hand-object-interaction | arxiv | `"entity-level hand-object interaction" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: entity-level hand-object interaction. |
| web-calibrated-6dof-object-manipulation-trajectories | arxiv | `"6DoF object manipulation trajectories" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: 6DoF object manipulation trajectories. |
| web-calibrated-noisy-or-incomplete-trajectories | arxiv | `"noisy or incomplete trajectories" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: noisy or incomplete trajectories. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-egocentric-robot-learning | arxiv_api | llm | medium | `all:"egocentric video" AND (all:"robot learning" OR all:"robot manipulation")` | 直接覆盖第一视角视频用于机器人学习。 |
| dynamic-first-person-demonstration | arxiv_api | llm | medium | `all:"first-person video" AND (all:robot OR all:manipulation)` | 补充不使用 egocentric 术语的第一视角论文。 |
| dynamic-human-video-policy | arxiv_api | llm | medium | `all:"human video" AND (all:"robot policy" OR all:"imitation learning")` | 覆盖从人类视频学习机器人策略的主线。 |
| dynamic-ego-to-robot | arxiv_api | llm | medium | `(all:"ego-to-robot" OR all:"human-to-robot") AND (all:video OR all:demonstration)` | 覆盖跨本体迁移与 embodiment gap。 |
| dynamic-hand-object-interface | arxiv_api | llm | medium | `all:"hand-object interaction" AND (all:robot OR all:policy)` | 手—物交互是将人类第一视角视频转成机器人可执行表征的常见接口。 |
| dynamic-latent-pseudo-action | arxiv_api | llm | medium | `(all:"latent action" OR all:"pseudo action") AND (all:"human video" OR all:egocentric) AND all:robot` | 覆盖无原生机器人动作标签时的替代监督。 |
| dynamic-egocentric-trajectory-extraction | arxiv_api | llm | medium | `all:egocentric AND (all:"6DoF trajectory" OR all:"object trajectory" OR all:"hand pose") AND all:robot` | 覆盖从原始第一视角视频恢复运动轨迹及其噪声问题。 |
| dynamic-egocentric-observability-limit | arxiv_api | llm | medium | `all:egocentric AND (all:occlusion OR all:contact OR all:"camera motion" OR all:visibility) AND (all:robot OR all:manipulation)` | 覆盖遮挡、接触不可观测和相机自运动等数据缺陷。 |
| dynamic-egocentric-vla-pretraining | arxiv_api | llm | medium | `all:egocentric AND (all:VLA OR all:"vision language action") AND (all:pretraining OR all:"pre-training")` | 覆盖第一视角视频用于 VLA 预训练的直接证据。 |
| dynamic-egocentric-training-challenges-browser | browser_fallback | llm | medium | `site:arxiv.org/abs (egocentric OR first-person) human video robot learning embodiment gap action labels occlusion` | 发现 API 元数据可能漏掉的挑战型论文。 |
| dynamic-egocentric-robot-terms-web | web_calibration | llm | medium | `site:arxiv.org/abs egocentric human video robot policy 2025 2026` | 校准近一年方法名与数据处理术语。 |

## Calibration Notes

- arxiv calibration (high): HumanEgo 使用 entity-level hand-object interaction 与 dense auxiliary objectives 描述 ego-to-robot transfer。
- arxiv calibration (high): EgoScaler 使用 6DoF object manipulation trajectories、raw egocentric videos、noisy or incomplete trajectories 与 VLA pre-training。

## Planner Notes

- llm dynamic expansion (medium): 第一视角人类视频进入具身训练时，还会以 human video、first-person demonstration、hand-object interaction、pseudo-action、latent action 和 ego-to-robot 等术语出现。
