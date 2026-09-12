# Query Plan: 近一年鱼眼镜头在具身领域的应用

## Scope

- Knowledge IDs: EA-SENSOR, EA-HARDWARE
- Families: none
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 100
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-fisheye-robot-broad | dynamic-direct | `all:fisheye AND all:robot` | Broadest recall for fisheye lenses used in any robotic context; downstream screening separates embodied applications from ADAS surround-view. |
| dynamic-fisheye-manipulation | dynamic-direct | `all:fisheye AND all:manipulation` | Direct: fisheye wrist/body cameras in manipulation policies (e.g. Rethinking Camera Choice, Give Human a Robot Hand). |
| dynamic-fisheye-vla | dynamic-direct | `all:fisheye AND (all:"vision-language-action" OR all:VLA)` | Direct: VLA policies trained on or adapted to fisheye observations (VISTA, PanoVLA family). |
| dynamic-panorama-vla-mobile | dynamic-direct | `all:panorama AND all:"robot manipulation"` | Panorama-aware VLA for mobile manipulation is a 2026 direct-topic family (PanoVLA). |
| dynamic-wide-fov-robot | dynamic-mechanism | `all:"wide field of view" AND all:robot` | Mechanism: wide-FoV benefits (spatial localization, context) phrased without the word fisheye. |
| dynamic-fisheye-distortion-policy | dynamic-mechanism | `all:fisheye AND all:distortion` | Mechanism: radial distortion modeling, rectification, and their interaction with learned policies. |
| dynamic-cross-camera-generalization | dynamic-limit | `all:"camera generalization" AND all:robot` | Limit surface: policies that overfit to one camera model (pinhole vs fisheye); AnyCamVLA/ICWM family. |
| dynamic-camera-adaptation-robot | dynamic-limit | `all:"camera adaptation" AND all:robot` | Limit surface: zero-shot camera/viewpoint adaptation as the response to fisheye-vs-pinhole domain gaps. |
| dynamic-fisheye-benchmark | dynamic-eval | `all:fisheye AND all:benchmark` | Evaluation: benchmarks and datasets that include fisheye sensors for robot perception (RoboSense-style). |
| dynamic-omnidirectional-navigation | dynamic-eval | `all:omnidirectional AND all:navigation AND all:robot` | Evaluation/deployment: omnidirectional-camera navigation systems (SysNav 360-camera object navigation). |
| dynamic-fisheye-humanoid | dynamic-deploy | `all:fisheye AND all:humanoid` | Deployment: humanoid platforms shipping fisheye cameras (AGIBOT G2, NICO stereo fisheye). |
| dynamic-surround-view-robot | dynamic-deploy | `all:"surround view" AND all:robot AND all:perception` | Deployment: 360 surround-view vision systems on embodied platforms (RobotPan on Tiangong humanoid). |
| dynamic-360-camera-robot | dynamic-deploy | `all:"360 camera" AND all:robot` | Deployment: 360-degree panoramic cameras as robot input or teleoperation interface. |
| dynamic-fisheye-slam | dynamic-adjacent | `all:fisheye AND all:SLAM` | Adjacent: fisheye/omnidirectional SLAM underpins embodied localization (ODGS-SLAM, multi-fisheye VIO); screen for robot context. |
| dynamic-panoramic-teleop-data | dynamic-adjacent | `all:panoramic AND all:teleoperation` | Adjacent: panoramic cameras in whole-body teleoperation and demonstration data collection. |
| dynamic-fisheye-detection | dynamic-adjacent | `all:fisheye AND (all:detection OR all:segmentation) AND all:robot` | Adjacent: fisheye perception modules (detection/segmentation) consumed by robot stacks. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-hardware-teleop-device | core | `all:teleoperation AND all:"data collection" AND all:robot` | Find hardware routes used to collect robot demonstrations. |
| ea-hardware-slam-demonstration | tracking | `all:SLAM AND all:"robot manipulation" AND all:demonstration` | Capture tracking and reconstruction limitations in collection devices. |
| ea-hardware-arkit-tracking | tracking | `all:ARKit AND all:robot AND all:tracking` | Find low-cost pose-tracking and VIO routes relevant to data capture. |
| ea-hardware-handheld-gripper | device-language | `(all:"handheld gripper" OR all:"hand-held gripper") AND all:robot` | Catch UMI-like collection devices that may not use UMI in metadata. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-fisheye-robot-broad, dynamic-fisheye-manipulation, dynamic-fisheye-vla, dynamic-panorama-vla-mobile, dynamic-wide-fov-robot, dynamic-fisheye-distortion-policy, dynamic-fisheye-slam, dynamic-panoramic-teleop-data, dynamic-fisheye-detection, ea-sensor-tactile-force, ea-sensor-point-cloud, ea-hardware-handheld-gripper |
| limits-and-counterevidence | 3 | dynamic-cross-camera-generalization, dynamic-camera-adaptation-robot, ea-sensor-occlusion |
| evaluation-and-validation | 3 | dynamic-fisheye-benchmark, dynamic-omnidirectional-navigation |
| deployment-and-operations | 3 | dynamic-fisheye-humanoid, dynamic-surround-view-robot, dynamic-360-camera-robot |
| direct-topic | 3 | ea-sensor-multimodal-policy, ea-hardware-teleop-device |
| mechanisms-and-interfaces | 3 | ea-hardware-slam-demonstration, ea-hardware-arkit-tracking |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-fisheye-embodied-browser | `fisheye camera "vision-language-action" OR manipulation site:arxiv.org 2026` | Recover papers whose abstracts use fisheye-adjacent wording missed by API field search. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-fisheye-vlm-robustness-web | web-calibration | `fisheye distortion VLM robustness robot 2026 arXiv` | Check whether VLM-on-fisheye robustness studies form a distinct 2026 paper family. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-fisheye-robot-broad | arxiv_api | web-calibration | high | `all:fisheye AND all:robot` | Broadest recall for fisheye lenses used in any robotic context; downstream screening separates embodied applications from ADAS surround-view. |
| dynamic-fisheye-manipulation | arxiv_api | web-calibration | high | `all:fisheye AND all:manipulation` | Direct: fisheye wrist/body cameras in manipulation policies (e.g. Rethinking Camera Choice, Give Human a Robot Hand). |
| dynamic-fisheye-vla | arxiv_api | web-calibration | high | `all:fisheye AND (all:"vision-language-action" OR all:VLA)` | Direct: VLA policies trained on or adapted to fisheye observations (VISTA, PanoVLA family). |
| dynamic-panorama-vla-mobile | arxiv_api | web-calibration | medium | `all:panorama AND all:"robot manipulation"` | Panorama-aware VLA for mobile manipulation is a 2026 direct-topic family (PanoVLA). |
| dynamic-wide-fov-robot | arxiv_api | web-calibration | medium | `all:"wide field of view" AND all:robot` | Mechanism: wide-FoV benefits (spatial localization, context) phrased without the word fisheye. |
| dynamic-fisheye-distortion-policy | arxiv_api | web-calibration | high | `all:fisheye AND all:distortion` | Mechanism: radial distortion modeling, rectification, and their interaction with learned policies. |
| dynamic-cross-camera-generalization | arxiv_api | web-calibration | medium | `all:"camera generalization" AND all:robot` | Limit surface: policies that overfit to one camera model (pinhole vs fisheye); AnyCamVLA/ICWM family. |
| dynamic-camera-adaptation-robot | arxiv_api | web-calibration | medium | `all:"camera adaptation" AND all:robot` | Limit surface: zero-shot camera/viewpoint adaptation as the response to fisheye-vs-pinhole domain gaps. |
| dynamic-fisheye-benchmark | arxiv_api | web-calibration | medium | `all:fisheye AND all:benchmark` | Evaluation: benchmarks and datasets that include fisheye sensors for robot perception (RoboSense-style). |
| dynamic-omnidirectional-navigation | arxiv_api | web-calibration | medium | `all:omnidirectional AND all:navigation AND all:robot` | Evaluation/deployment: omnidirectional-camera navigation systems (SysNav 360-camera object navigation). |
| dynamic-fisheye-humanoid | arxiv_api | web-calibration | medium | `all:fisheye AND all:humanoid` | Deployment: humanoid platforms shipping fisheye cameras (AGIBOT G2, NICO stereo fisheye). |
| dynamic-surround-view-robot | arxiv_api | web-calibration | medium | `all:"surround view" AND all:robot AND all:perception` | Deployment: 360 surround-view vision systems on embodied platforms (RobotPan on Tiangong humanoid). |
| dynamic-360-camera-robot | arxiv_api | web-calibration | medium | `all:"360 camera" AND all:robot` | Deployment: 360-degree panoramic cameras as robot input or teleoperation interface. |
| dynamic-fisheye-slam | arxiv_api | web-calibration | medium | `all:fisheye AND all:SLAM` | Adjacent: fisheye/omnidirectional SLAM underpins embodied localization (ODGS-SLAM, multi-fisheye VIO); screen for robot context. |
| dynamic-panoramic-teleop-data | arxiv_api | web-calibration | medium | `all:panoramic AND all:teleoperation` | Adjacent: panoramic cameras in whole-body teleoperation and demonstration data collection. |
| dynamic-fisheye-detection | arxiv_api | web-calibration | medium | `all:fisheye AND (all:detection OR all:segmentation) AND all:robot` | Adjacent: fisheye perception modules (detection/segmentation) consumed by robot stacks. |
| dynamic-fisheye-embodied-browser | browser_fallback | web-calibration | medium | `fisheye camera "vision-language-action" OR manipulation site:arxiv.org 2026` | Recover papers whose abstracts use fisheye-adjacent wording missed by API field search. |
| dynamic-fisheye-vlm-robustness-web | web_calibration | web-calibration | medium | `fisheye distortion VLM robustness robot 2026 arXiv` | Check whether VLM-on-fisheye robustness studies form a distinct 2026 paper family. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- web-calibration dynamic expansion (high): Web calibration on 2026-09-09 found direct-topic papers (arXiv:2603.02139 fisheye camera choice in robotic manipulation; arXiv:2608.02257 panorama-aware VLA; arXiv:2604.13476 RobotPan surround-view; arXiv:2606.04708 VISTA fisheye UMI adaptation; arXiv:2603.05868 AnyCamVLA zero-shot camera adaptation), plus industrial signals (AGIBOT G2 humanoid ships fisheye cameras) and adjacent families (ODGS-SLAM omnidirectional GS-SLAM, SysNav 360-camera navigation, RoboSense fisheye-equipped dataset).
