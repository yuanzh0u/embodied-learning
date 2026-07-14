# Query Plan: 近半年 UMI 数据质量

## Scope

- Knowledge IDs: EA-DATA, EA-SENSOR, EA-HARDWARE, EA-XEMBODIMENT
- Families: umi, teleoperation-demo-quality
- Suggested categories: cs.AI, cs.CV, cs.HC, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 104
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| umi-exact-lineage | exact-lineage | `all:"Universal Manipulation Interface"` | Find the original UMI lineage and papers spelling out the full method name. |
| umi-abbrev-robot-data | exact-lineage | `all:UMI AND all:robot AND all:data` | Catch metadata that uses the UMI acronym without the expanded phrase. |
| umi-named-variants | named-variant | `(all:"UMI-3D" OR all:"UMI 3D" OR all:DexUMI OR all:RealDexUMI)` | Find named variants that expose 3D, dexterity, and wearable-data limitations. |
| umi-force-torque | sensor-extension | `all:UMI AND all:force AND all:torque` | Find UMI extensions for contact-rich or force-aware data collection. |
| umi-handheld-gripper-language | device-language | `(all:"handheld gripper" OR all:"hand-held gripper") AND all:demonstration` | Catch UMI-like handheld interfaces that may not mention the acronym. |
| umi-usability-limitations | limitation | `all:usability AND all:gripper AND all:"robot learning"` | Find papers that critique operator burden, gripper design, and data usability. |
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
| ea-hardware-teleop-device | core | `all:teleoperation AND all:"data collection" AND all:robot` | Find hardware routes used to collect robot demonstrations. |
| ea-hardware-slam-demonstration | tracking | `all:SLAM AND all:"robot manipulation" AND all:demonstration` | Capture tracking and reconstruction limitations in collection devices. |
| ea-hardware-arkit-tracking | tracking | `all:ARKit AND all:robot AND all:tracking` | Find low-cost pose-tracking and VIO routes relevant to data capture. |
| ea-hardware-handheld-gripper | device-language | `(all:"handheld gripper" OR all:"hand-held gripper") AND all:robot` | Catch UMI-like collection devices that may not use UMI in metadata. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | umi-exact-lineage, umi-abbrev-robot-data, umi-named-variants, teleop-imitation-learning, teleop-demonstration-quality, ea-data-robot-demonstrations, ea-sensor-multimodal-policy, ea-hardware-teleop-device, ea-xembodiment-cross-embodiment |
| mechanisms-and-interfaces | 3 | umi-force-torque, teleop-action-interface, ea-xembodiment-action-representation |
| adjacent-and-transfer | 3 | umi-handheld-gripper-language, teleop-operator-burden, ea-data-in-the-wild, ea-data-dataset-curation, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-hardware-slam-demonstration, ea-hardware-arkit-tracking, ea-hardware-handheld-gripper, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot |
| limits-and-counterevidence | 3 | umi-usability-limitations, teleop-latency, ea-sensor-occlusion |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-umi-named-lineage | `site:arxiv.org/abs ("Universal Manipulation Interface" OR "UMI-FT" OR "UMI-3D" OR DexUMI OR RealDexUMI) robot manipulation` | Find UMI lineage and named variants through arXiv pages when API metadata search misses exact names. |
| browser-umi-usability-quality | `site:arxiv.org/abs (UMI OR "handheld gripper" OR "hand-held gripper") ("demonstration quality" OR usability OR ergonomics) "robot learning"` | Find negative or conditional UMI data-usability discussions around gripper design and operator burden. |
| browser-umi-sensing-transfer-limits | `site:arxiv.org/abs (UMI OR "Universal Manipulation Interface") (SLAM OR occlusion OR tactile OR force OR retargeting OR dexterous)` | Find UMI-adjacent limitation papers about sensing, tracking, force, tactile feedback, or embodiment transfer. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-topic-calibration | web | `"近半年 UMI 数据质量" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.
