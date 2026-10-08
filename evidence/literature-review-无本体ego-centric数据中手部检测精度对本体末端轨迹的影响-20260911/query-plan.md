# Query Plan: 无本体ego-centric数据中手部检测精度对本体末端轨迹的影响

## Scope

- Knowledge IDs: EA-DATA, EA-XEMBODIMENT, EA-SENSOR, EA-MODEL
- Families: none
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 144
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-ego-hand-robot-core | dynamic-direct | `all:egocentric AND all:"hand pose" AND all:robot` | Core intersection: egocentric hand pose used for robot learning. |
| dynamic-ego-video-imitation-hand | dynamic-direct | `all:"egocentric video" AND all:"imitation learning" AND all:hand` | Direct: imitation from egocentric human video via hand signals (EgoVLA/EgoMimic family). |
| dynamic-hand-pose-retarget | dynamic-direct | `all:"hand pose" AND all:retargeting AND all:robot` | Direct: hand-pose-to-robot retargeting pipelines and their error behavior. |
| dynamic-human-video-wrist-trajectory | dynamic-direct | `all:"human video" AND all:"wrist trajectory" AND all:robot` | Direct: wrist/end-effector trajectory recovery from human video. |
| dynamic-egodex-egovla-titles | dynamic-direct | `ti:EgoDex OR ti:EgoVLA OR ti:EgoMimic` | Title anchors for the three flagship ego-video-to-robot systems. |
| dynamic-world-space-hand-recon | dynamic-method | `all:"world-space" AND all:"hand" AND all:reconstruction AND all:egocentric` | Method: world-space hand reconstruction (HaWoR family) as the ego-video action-labeling front end. |
| dynamic-hand-object-4d-policy | dynamic-method | `all:"hand-object" AND all:trajectory AND all:policy AND all:video` | Method: 4D hand-object trajectory reconstruction feeding manipulation policies (VideoManip). |
| dynamic-embodiment-agnostic-rep | dynamic-method | `all:"embodiment-agnostic" AND all:"human video"` | Method: embodiment-agnostic intermediate representations that bypass or buffer hand-pose error (LUCID, 3PoinTr). |
| dynamic-point-track-action | dynamic-method | `all:"point tracks" AND all:robot AND all:manipulation` | Method/alternative: point-track action representations that avoid explicit hand pose (ATM, Track2Act, 3PoinTr). |
| dynamic-pose-noise-robust-policy | dynamic-limit | `all:noisy AND all:demonstrations AND all:policy AND all:robot` | Limit: robustness of imitation policies to noisy action labels/trajectories. |
| dynamic-hand-tracking-noise | dynamic-limit | `all:"hand tracking" AND (all:noise OR all:error OR all:accuracy) AND all:robot` | Limit: hand tracking noise/error/accuracy in robot data pipelines. |
| dynamic-label-noise-imitation | dynamic-limit | `all:"label noise" AND all:"imitation learning" AND all:manipulation` | Limit: action-label noise in imitation learning for manipulation. |
| dynamic-hand-pose-benchmark-eval | dynamic-eval | `all:"hand pose estimation" AND all:benchmark AND all:egocentric` | Eval: egocentric hand pose benchmarks/metrics (MPJPE/MKPE) that quantify the upstream error budget. |
| dynamic-retarget-eval-dexterous | dynamic-eval | `all:retargeting AND all:evaluation AND all:"dexterous manipulation"` | Eval: retargeting objective ablations and error metrics for dexterous manipulation (mingrui-yu study, PKDA). |
| dynamic-human-video-success-rate | dynamic-eval | `all:"human videos" AND all:"success rate" AND all:robot AND all:manipulation` | Eval: downstream policy success rates from human-video-derived trajectories. |
| dynamic-umi-tracking-deploy | dynamic-deploy | `all:UMI AND all:tracking AND all:manipulation` | Deploy: device-based tracking (UMI/FastUMI/DexUMI) as the accuracy contrast to visual hand detection. |
| dynamic-teleop-hand-tracking-deploy | dynamic-deploy | `all:teleoperation AND all:"hand tracking" AND all:robot` | Deploy: teleoperation hand tracking accuracy/latency (Vision Pro class) as deployed baseline. |
| dynamic-wearable-data-collection | dynamic-adjacent | `all:wearable AND all:"data collection" AND all:manipulation AND all:hand` | Adjacent: wearable ego data collection where hand signal quality is the bottleneck. |
| dynamic-egoexo-robot-transfer | dynamic-adjacent | `all:EgoExo4D OR (all:ego-exo AND all:robot)` | Adjacent: Ego-Exo datasets/benchmarks feeding robot learning. |
| dynamic-motion-retarget-humanoid-adjacent | dynamic-adjacent | `all:"motion retargeting" AND all:humanoid AND all:video` | Adjacent: human-video motion retargeting to humanoid whole bodies (GenMimic family) — wrist trajectory error tolerance. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-ego-hand-robot-core, dynamic-ego-video-imitation-hand, dynamic-hand-pose-retarget, dynamic-human-video-wrist-trajectory, dynamic-egodex-egovla-titles, dynamic-wearable-data-collection, dynamic-egoexo-robot-transfer, dynamic-motion-retarget-humanoid-adjacent, ea-data-in-the-wild, ea-data-dataset-curation, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-model-finetuning |
| mechanisms-and-interfaces | 3 | dynamic-world-space-hand-recon, dynamic-hand-object-4d-policy, dynamic-embodiment-agnostic-rep, dynamic-point-track-action, ea-xembodiment-action-representation, ea-model-action-tokenization |
| limits-and-counterevidence | 3 | dynamic-pose-noise-robust-policy, dynamic-hand-tracking-noise, dynamic-label-noise-imitation, ea-sensor-occlusion |
| evaluation-and-validation | 3 | dynamic-hand-pose-benchmark-eval, dynamic-retarget-eval-dexterous, dynamic-human-video-success-rate |
| deployment-and-operations | 3 | dynamic-umi-tracking-deploy, dynamic-teleop-hand-tracking-deploy |
| direct-topic | 3 | ea-data-robot-demonstrations, ea-data-demonstration-quality, ea-xembodiment-cross-embodiment, ea-sensor-multimodal-policy, ea-model-vla, ea-model-named-foundation |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-topic-arxiv | `site:arxiv.org/abs "无本体ego-centric数据中手部检测精度对本体末端轨迹的影响" "robot"` | Fallback candidate discovery on arXiv pages when API metadata search under-recovers. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-topic-calibration | web | `"无本体ego-centric数据中手部检测精度对本体末端轨迹的影响" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-ego-hand-robot-core | arxiv_api | web-calibration | high | `all:egocentric AND all:"hand pose" AND all:robot` | Core intersection: egocentric hand pose used for robot learning. |
| dynamic-ego-video-imitation-hand | arxiv_api | web-calibration | high | `all:"egocentric video" AND all:"imitation learning" AND all:hand` | Direct: imitation from egocentric human video via hand signals (EgoVLA/EgoMimic family). |
| dynamic-hand-pose-retarget | arxiv_api | web-calibration | high | `all:"hand pose" AND all:retargeting AND all:robot` | Direct: hand-pose-to-robot retargeting pipelines and their error behavior. |
| dynamic-human-video-wrist-trajectory | arxiv_api | web-calibration | high | `all:"human video" AND all:"wrist trajectory" AND all:robot` | Direct: wrist/end-effector trajectory recovery from human video. |
| dynamic-egodex-egovla-titles | arxiv_api | web-calibration | high | `ti:EgoDex OR ti:EgoVLA OR ti:EgoMimic` | Title anchors for the three flagship ego-video-to-robot systems. |
| dynamic-world-space-hand-recon | arxiv_api | web-calibration | high | `all:"world-space" AND all:"hand" AND all:reconstruction AND all:egocentric` | Method: world-space hand reconstruction (HaWoR family) as the ego-video action-labeling front end. |
| dynamic-hand-object-4d-policy | arxiv_api | web-calibration | high | `all:"hand-object" AND all:trajectory AND all:policy AND all:video` | Method: 4D hand-object trajectory reconstruction feeding manipulation policies (VideoManip). |
| dynamic-embodiment-agnostic-rep | arxiv_api | web-calibration | high | `all:"embodiment-agnostic" AND all:"human video"` | Method: embodiment-agnostic intermediate representations that bypass or buffer hand-pose error (LUCID, 3PoinTr). |
| dynamic-point-track-action | arxiv_api | web-calibration | high | `all:"point tracks" AND all:robot AND all:manipulation` | Method/alternative: point-track action representations that avoid explicit hand pose (ATM, Track2Act, 3PoinTr). |
| dynamic-pose-noise-robust-policy | arxiv_api | web-calibration | high | `all:noisy AND all:demonstrations AND all:policy AND all:robot` | Limit: robustness of imitation policies to noisy action labels/trajectories. |
| dynamic-hand-tracking-noise | arxiv_api | web-calibration | high | `all:"hand tracking" AND (all:noise OR all:error OR all:accuracy) AND all:robot` | Limit: hand tracking noise/error/accuracy in robot data pipelines. |
| dynamic-label-noise-imitation | arxiv_api | web-calibration | medium | `all:"label noise" AND all:"imitation learning" AND all:manipulation` | Limit: action-label noise in imitation learning for manipulation. |
| dynamic-hand-pose-benchmark-eval | arxiv_api | web-calibration | high | `all:"hand pose estimation" AND all:benchmark AND all:egocentric` | Eval: egocentric hand pose benchmarks/metrics (MPJPE/MKPE) that quantify the upstream error budget. |
| dynamic-retarget-eval-dexterous | arxiv_api | web-calibration | high | `all:retargeting AND all:evaluation AND all:"dexterous manipulation"` | Eval: retargeting objective ablations and error metrics for dexterous manipulation (mingrui-yu study, PKDA). |
| dynamic-human-video-success-rate | arxiv_api | web-calibration | medium | `all:"human videos" AND all:"success rate" AND all:robot AND all:manipulation` | Eval: downstream policy success rates from human-video-derived trajectories. |
| dynamic-umi-tracking-deploy | arxiv_api | web-calibration | high | `all:UMI AND all:tracking AND all:manipulation` | Deploy: device-based tracking (UMI/FastUMI/DexUMI) as the accuracy contrast to visual hand detection. |
| dynamic-teleop-hand-tracking-deploy | arxiv_api | web-calibration | medium | `all:teleoperation AND all:"hand tracking" AND all:robot` | Deploy: teleoperation hand tracking accuracy/latency (Vision Pro class) as deployed baseline. |
| dynamic-wearable-data-collection | arxiv_api | web-calibration | medium | `all:wearable AND all:"data collection" AND all:manipulation AND all:hand` | Adjacent: wearable ego data collection where hand signal quality is the bottleneck. |
| dynamic-egoexo-robot-transfer | arxiv_api | web-calibration | medium | `all:EgoExo4D OR (all:ego-exo AND all:robot)` | Adjacent: Ego-Exo datasets/benchmarks feeding robot learning. |
| dynamic-motion-retarget-humanoid-adjacent | arxiv_api | web-calibration | medium | `all:"motion retargeting" AND all:humanoid AND all:video` | Adjacent: human-video motion retargeting to humanoid whole bodies (GenMimic family) — wrist trajectory error tolerance. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- web-calibration dynamic expansion (high): Web calibration on 2026-09-11 identified the hand-detection-to-trajectory pipeline family: EgoVLA (arXiv:2507.12440, wrist/hand actions from ego video -> IK retargeting), EgoDex (Apple, 829h AVP device-tracked 3D hand), VideoManip (arXiv:2602.09013, 4D hand-object trajectory -> DP3 policy 62.86%), AoE (arXiv:2602.23893, HaWoR hand reconstruction pipeline), Video2Sim2Real (arXiv:2606.08828, HaMeR keypoints -> Mink retargeting), LUCID (embodiment-agnostic intent: object flow + palm pose), 3PoinTr (arXiv:2603.08485, 3D point tracks as embodiment-agnostic representation), MobileEgo Anywhere (arXiv:2605.05945). Retargeting-error analyses: mingrui-yu key-objectives retargeting study, Vision-Based Hand Shadowing (arXiv:2603.11383, failures stem exclusively from landmark detection issues), HumDex (arXiv:2603.12260), PKDA (arXiv:2511.10987). Device-tracked contrast family: FastUMI / ActiveUMI (arXiv:2510.01607) / UMI-3D / DexUMI. Prior run LR-EGO-HAND (20260729) quantified ego hand-tracking accuracy itself (in-domain MKPE 9-11mm -> 16.28mm in the wild); this run targets the downstream propagation into end-effector trajectory and policy success.
