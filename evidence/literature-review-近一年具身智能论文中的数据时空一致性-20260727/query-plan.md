# Query Plan: 近一年具身智能论文中的数据时空一致性

## Scope

- Knowledge IDs: EA-DATA, EA-SENSOR, EA-EVAL
- Families: world-model, tactile-force, vla, teleoperation-demo-quality
- Suggested categories: cs.AI, cs.CV, cs.HC, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 176
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-clock-sensor-synchronization | quality | `(all:robot OR all:embodied) AND (all:"sensor synchronization" OR all:"time synchronization" OR all:"timestamp alignment")` | 覆盖多传感器硬件时钟、时间戳、延迟和抖动讨论。 |
| dynamic-multimodal-temporal-alignment | representation | `all:"robot manipulation" AND (all:"temporal alignment" OR all:"cross-modal alignment") AND (all:tactile OR all:force OR all:vision)` | 覆盖视觉、触觉、力觉与机器人状态的跨模态时间对齐。 |
| dynamic-spatial-calibration-coordinate-frame | quality | `all:robot AND (all:"coordinate frame" OR all:"spatial calibration" OR all:extrinsic) AND (all:dataset OR all:demonstration OR all:multimodal)` | 覆盖相机—机器人—物体参考系、外参和空间标定。 |
| dynamic-view-consistent-4d-data | representation | `(all:"view-consistent" OR all:"multi-view consistency") AND (all:4D OR all:"world model") AND all:robot` | 覆盖跨视角几何一致和任意视角时空生成。 |
| dynamic-point-tracks-correspondence | representation | `(all:"3D point tracks" OR all:"spatiotemporal correspondence") AND (all:manipulation OR all:embodied)` | 覆盖跨帧点身份、遮挡可见性与度量几何监督。 |
| dynamic-action-state-consistency | evaluation | `all:robot AND (all:"action-state consistency" OR all:"action observation alignment" OR all:"action-conditioned state")` | 覆盖动作、观测和状态变化之间的对齐与检核。 |
| dynamic-action-fidelity-long-horizon | limitation | `all:"robot world model" AND (all:"action fidelity" OR all:"long-horizon consistency" OR all:"temporal consistency")` | 覆盖长程预测漂移、动作忠实和视频逼真但物理不一致的反例。 |
| dynamic-contact-event-alignment | limitation | `all:"contact-rich manipulation" AND (all:"contact event" OR all:"contact-aware" OR all:"event-driven") AND (all:tactile OR all:force)` | 覆盖稀疏接触事件、固定帧采样失真和接触门控。 |
| dynamic-physical-time-action-chunk | policy-interface | `(all:VLA OR all:"vision-language-action") AND (all:"action chunk" OR all:"control frequency") AND (all:latency OR all:asynchronous OR all:alignment)` | 覆盖动作块按物理时长而非固定帧数对齐、控制频率和延迟。 |
| dynamic-spatiotemporal-data-quality | quality | `(all:robot OR all:embodied) AND all:"spatiotemporal consistency" AND (all:data OR all:dataset OR all:trajectory)` | 直接捕捉明确使用时空一致性术语的数据论文。 |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| tactile-force-tactile-manipulation | core | `all:tactile AND all:"robot manipulation"` | Find tactile sensing papers tied to manipulation policies or control. |
| tactile-force-force-torque | force | `all:force AND all:torque AND all:robot` | Cover force/torque observability and low-dimensional contact feedback. |
| tactile-force-slip-detection | contact-state | `all:"slip detection" AND all:robot` | Find tactile and force cues for grasp stability and material interaction. |
| tactile-force-contact-rich | task-family | `all:"contact-rich" AND all:manipulation` | Surface high-contact tasks where vision-only policies often fail. |
| tactile-force-sensor-fusion | fusion | `all:"sensor fusion" AND all:tactile AND all:robot` | Find multimodal policies combining tactile, force, vision, or proprioception. |
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
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-clock-sensor-synchronization, dynamic-spatial-calibration-coordinate-frame, dynamic-spatiotemporal-data-quality, world-model-robot, tactile-force-tactile-manipulation, vla-core, vla-named-models, teleop-imitation-learning, teleop-demonstration-quality, ea-data-robot-demonstrations, ea-sensor-multimodal-policy, ea-eval-closed-loop |
| mechanisms-and-interfaces | 3 | dynamic-multimodal-temporal-alignment, dynamic-view-consistent-4d-data, dynamic-point-tracks-correspondence, dynamic-physical-time-action-chunk, teleop-action-interface |
| adjacent-and-transfer | 3 | dynamic-action-state-consistency, world-model-video-prediction, world-model-planning, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, teleop-operator-burden, ea-data-in-the-wild, ea-data-dataset-curation, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| limits-and-counterevidence | 3 | dynamic-action-fidelity-long-horizon, dynamic-contact-event-alignment, world-model-contact, world-model-long-horizon, vla-negative-transfer, teleop-latency, ea-sensor-occlusion |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-browser-spatiotemporal-data | `site:arxiv.org robot data spatiotemporal consistency synchronization calibration action-state` | API 术语过严时补获相邻论文。 |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-web-physical-time | llm | `robot dataset physical time alignment sensor clock action chunk` | 校准论文对物理时间、控制频率和同步误差的实际用词。 |
| dynamic-web-spatial-contract | llm | `robot learning dataset coordinate frame calibration provenance multimodal` | 校准空间契约、标定谱系和参考系残差术语。 |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-clock-sensor-synchronization | arxiv_api | llm | high | `(all:robot OR all:embodied) AND (all:"sensor synchronization" OR all:"time synchronization" OR all:"timestamp alignment")` | 覆盖多传感器硬件时钟、时间戳、延迟和抖动讨论。 |
| dynamic-multimodal-temporal-alignment | arxiv_api | llm | high | `all:"robot manipulation" AND (all:"temporal alignment" OR all:"cross-modal alignment") AND (all:tactile OR all:force OR all:vision)` | 覆盖视觉、触觉、力觉与机器人状态的跨模态时间对齐。 |
| dynamic-spatial-calibration-coordinate-frame | arxiv_api | llm | high | `all:robot AND (all:"coordinate frame" OR all:"spatial calibration" OR all:extrinsic) AND (all:dataset OR all:demonstration OR all:multimodal)` | 覆盖相机—机器人—物体参考系、外参和空间标定。 |
| dynamic-view-consistent-4d-data | arxiv_api | llm | high | `(all:"view-consistent" OR all:"multi-view consistency") AND (all:4D OR all:"world model") AND all:robot` | 覆盖跨视角几何一致和任意视角时空生成。 |
| dynamic-point-tracks-correspondence | arxiv_api | llm | high | `(all:"3D point tracks" OR all:"spatiotemporal correspondence") AND (all:manipulation OR all:embodied)` | 覆盖跨帧点身份、遮挡可见性与度量几何监督。 |
| dynamic-action-state-consistency | arxiv_api | llm | high | `all:robot AND (all:"action-state consistency" OR all:"action observation alignment" OR all:"action-conditioned state")` | 覆盖动作、观测和状态变化之间的对齐与检核。 |
| dynamic-action-fidelity-long-horizon | arxiv_api | llm | high | `all:"robot world model" AND (all:"action fidelity" OR all:"long-horizon consistency" OR all:"temporal consistency")` | 覆盖长程预测漂移、动作忠实和视频逼真但物理不一致的反例。 |
| dynamic-contact-event-alignment | arxiv_api | llm | high | `all:"contact-rich manipulation" AND (all:"contact event" OR all:"contact-aware" OR all:"event-driven") AND (all:tactile OR all:force)` | 覆盖稀疏接触事件、固定帧采样失真和接触门控。 |
| dynamic-physical-time-action-chunk | arxiv_api | llm | medium | `(all:VLA OR all:"vision-language-action") AND (all:"action chunk" OR all:"control frequency") AND (all:latency OR all:asynchronous OR all:alignment)` | 覆盖动作块按物理时长而非固定帧数对齐、控制频率和延迟。 |
| dynamic-spatiotemporal-data-quality | arxiv_api | llm | medium | `(all:robot OR all:embodied) AND all:"spatiotemporal consistency" AND (all:data OR all:dataset OR all:trajectory)` | 直接捕捉明确使用时空一致性术语的数据论文。 |
| dynamic-browser-spatiotemporal-data | browser_fallback | llm | medium | `site:arxiv.org robot data spatiotemporal consistency synchronization calibration action-state` | API 术语过严时补获相邻论文。 |
| dynamic-web-physical-time | web_calibration | llm | medium | `robot dataset physical time alignment sensor clock action chunk` | 校准论文对物理时间、控制频率和同步误差的实际用词。 |
| dynamic-web-spatial-contract | web_calibration | llm | medium | `robot learning dataset coordinate frame calibration provenance multimodal` | 校准空间契约、标定谱系和参考系残差术语。 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (high): 将具身数据时空一致性拆为时钟/采样、坐标/标定、跨视角/跨模态对应、动作—状态因果对齐、长程物理连续性五层；这些术语不会稳定同时出现在论文标题或摘要中。
