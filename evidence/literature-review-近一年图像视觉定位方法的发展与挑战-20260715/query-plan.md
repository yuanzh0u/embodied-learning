# Query Plan: 近一年图像视觉定位方法的发展与挑战

## Scope

- Knowledge IDs: EA-HARDWARE, EA-SENSOR, EA-EVAL
- Families: none
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 128
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-visual-localization-core | core | `all:"visual localization" AND (all:image OR all:camera)` | Capture papers using the canonical field name. |
| dynamic-camera-relocalization | core | `(all:"camera relocalization" OR all:"camera localization") AND all:image` | Cover metric 6-DoF relocalization terminology used outside the exact visual-localization phrase. |
| dynamic-structure-based-localization | mechanism | `(all:"2D-3D matching" OR all:"structure-based localization" OR all:"image-to-point") AND all:localization` | Cover retrieval-plus-correspondence and explicit 3D-map pipelines. |
| dynamic-scene-coordinate-regression | mechanism | `(all:"scene coordinate regression" OR all:"scene coordinates") AND (all:localization OR all:relocalization)` | Cover dense coordinate regression and differentiable pose-estimation lineages. |
| dynamic-pose-regression | mechanism | `(all:"absolute pose regression" OR all:"camera pose regression") AND all:image` | Cover direct and transformer-based pose-regression methods and their accuracy limits. |
| dynamic-place-recognition | adjacent | `(all:"visual place recognition" OR all:"place recognition") AND (all:robot OR all:localization)` | Cover the retrieval/coarse-localization stage that increasingly uses foundation features and sequence context. |
| dynamic-map-free-localization | mechanism | `(all:"map-free localization" OR all:"map free localization" OR all:"SfM-free localization")` | Cover localization without a prebuilt metric reconstruction and relative-pose alternatives. |
| dynamic-neural-scene-localization | mechanism | `(all:NeRF OR all:"3D Gaussian Splatting" OR all:"neural scene representation") AND (all:localization OR all:relocalization OR all:"camera pose")` | Cover implicit and radiance-field/3DGS scene representations used as localization maps. |
| dynamic-foundation-features-localization | mechanism | `(all:"foundation model" OR all:"vision foundation model" OR all:DINOv2 OR all:CLIP) AND (all:"visual localization" OR all:"place recognition")` | Test the shift from task-specific local descriptors to pretrained semantic and geometric features. |
| dynamic-long-term-localization | limitation | `(all:"long-term localization" OR all:"lifelong localization" OR all:"cross-season localization" OR all:"appearance change") AND all:visual` | Capture appearance, illumination, seasonal, and map-aging challenges. |
| dynamic-dynamic-scene-localization | limitation | `(all:"dynamic scene" OR all:"scene change" OR all:occlusion) AND (all:"visual localization" OR all:"camera relocalization")` | Cover localization failures caused by moving objects, structural changes, and occlusions. |
| dynamic-localization-uncertainty | evaluation | `(all:uncertainty OR all:calibration OR all:confidence) AND (all:"visual localization" OR all:"camera pose estimation")` | Cover reliability, confidence calibration, rejection, and failure prediction. |
| dynamic-localization-benchmark-robustness | evaluation | `(all:benchmark OR all:robustness OR all:evaluation) AND (all:"visual localization" OR all:"camera relocalization")` | Capture benchmark revisions, robustness analysis, and protocol critiques. |
| dynamic-localization-efficiency | deployment | `(all:efficient OR all:real-time OR all:mobile OR all:edge OR all:compression) AND (all:"visual localization" OR all:"visual place recognition")` | Cover map memory, latency, compute, bandwidth, and on-device deployment constraints. |
| dynamic-robot-localization-deployment | deployment | `(all:robot OR all:autonomous OR all:embodied) AND (all:"visual localization" OR all:"camera relocalization") AND (all:deployment OR all:"real-world" OR all:navigation)` | Capture closed-loop and real-system evidence beyond image-only benchmarks. |
| calibrated-gsff | calibrated-term | `all:GSFF` | Named 3DGS feature-field localization method. |
| calibrated-gsvisloc | calibrated-term | `all:GSVisLoc` | Named generalizable 3DGS localization method. |
| calibrated-lavpr | calibrated-term | `all:LaVPR` | Named language-vision place-recognition benchmark. |
| calibrated-fol | calibrated-term | `all:FoL++` | Named region-aware VPR method. |
| calibrated-displace | calibrated-term | `all:DisPlace` | Named multi-reference VPR fusion method. |
| calibrated-megaloc | calibrated-term | `all:MegaLoc` | Foundation-model-driven global descriptor family highlighted by recent evaluation. |
| calibrated-depth-aware-distillation | calibrated-term | `all:"depth-aware distillation"` | Recent geometry injection mechanism for VPR. |
| calibrated-geographic-imbalance | calibrated-term | `all:"geographic imbalance"` | Recent benchmark and data-distribution failure surface. |
| calibration-named-3dgs-localization | calibrated-query | `all:GSFF OR all:GSVisLoc OR all:"Gaussian Splatting Feature Fields"` | Recover recent named 3DGS localization methods and nearby follow-ups. |
| calibration-named-vpr-methods | calibrated-query | `all:LaVPR OR all:"FoL++" OR all:DisPlace OR all:MegaLoc` | Recover recent named VPR methods and benchmark papers. |
| calibration-vpr-geometry-language-data | calibrated-query | `all:"visual place recognition" AND (all:"depth-aware" OR all:language OR all:"geographic imbalance")` | Cover emerging multimodal and dataset-governance directions. |
| ea-hardware-teleop-device | core | `all:teleoperation AND all:"data collection" AND all:robot` | Find hardware routes used to collect robot demonstrations. |
| ea-hardware-slam-demonstration | tracking | `all:SLAM AND all:"robot manipulation" AND all:demonstration` | Capture tracking and reconstruction limitations in collection devices. |
| ea-hardware-arkit-tracking | tracking | `all:ARKit AND all:robot AND all:tracking` | Find low-cost pose-tracking and VIO routes relevant to data capture. |
| ea-hardware-handheld-gripper | device-language | `(all:"handheld gripper" OR all:"hand-held gripper") AND all:robot` | Catch UMI-like collection devices that may not use UMI in metadata. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-visual-localization-core, dynamic-camera-relocalization, ea-hardware-teleop-device, ea-sensor-multimodal-policy |
| adjacent-and-transfer | 3 | dynamic-structure-based-localization, dynamic-scene-coordinate-regression, dynamic-pose-regression, dynamic-place-recognition, dynamic-map-free-localization, dynamic-neural-scene-localization, dynamic-foundation-features-localization, dynamic-localization-uncertainty, dynamic-localization-benchmark-robustness, dynamic-localization-efficiency, dynamic-robot-localization-deployment, calibrated-gsff, calibrated-gsvisloc, calibrated-lavpr, calibrated-fol, calibrated-displace, calibrated-megaloc, calibrated-depth-aware-distillation, calibrated-geographic-imbalance, calibration-named-3dgs-localization, calibration-named-vpr-methods, calibration-vpr-geometry-language-data, ea-hardware-slam-demonstration, ea-hardware-arkit-tracking, ea-hardware-handheld-gripper, ea-sensor-tactile-force |
| limits-and-counterevidence | 3 | dynamic-long-term-localization, dynamic-dynamic-scene-localization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-visual-localization-browser | `site:arxiv.org visual localization camera relocalization 2025 2026` | Fallback discovery for recent papers missed or delayed by the arXiv API. |
| dynamic-visual-localization-benchmark-browser | `site:arxiv.org visual localization benchmark robustness 2025 2026` | Fallback discovery focused on evaluation and negative evidence. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-visual-localization-web-calibration | llm | `visual localization camera relocalization latest methods 2025 2026` | Calibrate recent terminology and named method lineages before finalizing search rounds. |
| web-calibrated-gsff | arxiv | `"GSFF" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: GSFF. |
| web-calibrated-gsvisloc | arxiv | `"GSVisLoc" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: GSVisLoc. |
| web-calibrated-lavpr | arxiv | `"LaVPR" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: LaVPR. |
| web-calibrated-fol | arxiv | `"FoL++" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: FoL++. |
| web-calibrated-displace | arxiv | `"DisPlace" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: DisPlace. |
| web-calibrated-megaloc | arxiv | `"MegaLoc" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: MegaLoc. |
| web-calibrated-depth-aware-distillation | arxiv | `"depth-aware distillation" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: depth-aware distillation. |
| web-calibrated-geographic-imbalance | arxiv | `"geographic imbalance" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: geographic imbalance. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-visual-localization-core | arxiv_api | llm | high | `all:"visual localization" AND (all:image OR all:camera)` | Capture papers using the canonical field name. |
| dynamic-camera-relocalization | arxiv_api | llm | high | `(all:"camera relocalization" OR all:"camera localization") AND all:image` | Cover metric 6-DoF relocalization terminology used outside the exact visual-localization phrase. |
| dynamic-structure-based-localization | arxiv_api | llm | high | `(all:"2D-3D matching" OR all:"structure-based localization" OR all:"image-to-point") AND all:localization` | Cover retrieval-plus-correspondence and explicit 3D-map pipelines. |
| dynamic-scene-coordinate-regression | arxiv_api | llm | high | `(all:"scene coordinate regression" OR all:"scene coordinates") AND (all:localization OR all:relocalization)` | Cover dense coordinate regression and differentiable pose-estimation lineages. |
| dynamic-pose-regression | arxiv_api | llm | high | `(all:"absolute pose regression" OR all:"camera pose regression") AND all:image` | Cover direct and transformer-based pose-regression methods and their accuracy limits. |
| dynamic-place-recognition | arxiv_api | llm | high | `(all:"visual place recognition" OR all:"place recognition") AND (all:robot OR all:localization)` | Cover the retrieval/coarse-localization stage that increasingly uses foundation features and sequence context. |
| dynamic-map-free-localization | arxiv_api | llm | high | `(all:"map-free localization" OR all:"map free localization" OR all:"SfM-free localization")` | Cover localization without a prebuilt metric reconstruction and relative-pose alternatives. |
| dynamic-neural-scene-localization | arxiv_api | llm | high | `(all:NeRF OR all:"3D Gaussian Splatting" OR all:"neural scene representation") AND (all:localization OR all:relocalization OR all:"camera pose")` | Cover implicit and radiance-field/3DGS scene representations used as localization maps. |
| dynamic-foundation-features-localization | arxiv_api | llm | medium | `(all:"foundation model" OR all:"vision foundation model" OR all:DINOv2 OR all:CLIP) AND (all:"visual localization" OR all:"place recognition")` | Test the shift from task-specific local descriptors to pretrained semantic and geometric features. |
| dynamic-long-term-localization | arxiv_api | llm | high | `(all:"long-term localization" OR all:"lifelong localization" OR all:"cross-season localization" OR all:"appearance change") AND all:visual` | Capture appearance, illumination, seasonal, and map-aging challenges. |
| dynamic-dynamic-scene-localization | arxiv_api | llm | high | `(all:"dynamic scene" OR all:"scene change" OR all:occlusion) AND (all:"visual localization" OR all:"camera relocalization")` | Cover localization failures caused by moving objects, structural changes, and occlusions. |
| dynamic-localization-uncertainty | arxiv_api | llm | high | `(all:uncertainty OR all:calibration OR all:confidence) AND (all:"visual localization" OR all:"camera pose estimation")` | Cover reliability, confidence calibration, rejection, and failure prediction. |
| dynamic-localization-benchmark-robustness | arxiv_api | llm | high | `(all:benchmark OR all:robustness OR all:evaluation) AND (all:"visual localization" OR all:"camera relocalization")` | Capture benchmark revisions, robustness analysis, and protocol critiques. |
| dynamic-localization-efficiency | arxiv_api | llm | high | `(all:efficient OR all:real-time OR all:mobile OR all:edge OR all:compression) AND (all:"visual localization" OR all:"visual place recognition")` | Cover map memory, latency, compute, bandwidth, and on-device deployment constraints. |
| dynamic-robot-localization-deployment | arxiv_api | llm | high | `(all:robot OR all:autonomous OR all:embodied) AND (all:"visual localization" OR all:"camera relocalization") AND (all:deployment OR all:"real-world" OR all:navigation)` | Capture closed-loop and real-system evidence beyond image-only benchmarks. |
| dynamic-visual-localization-browser | browser_fallback | llm | medium | `site:arxiv.org visual localization camera relocalization 2025 2026` | Fallback discovery for recent papers missed or delayed by the arXiv API. |
| dynamic-visual-localization-benchmark-browser | browser_fallback | llm | medium | `site:arxiv.org visual localization benchmark robustness 2025 2026` | Fallback discovery focused on evaluation and negative evidence. |
| dynamic-visual-localization-web-calibration | web_calibration | llm | medium | `visual localization camera relocalization latest methods 2025 2026` | Calibrate recent terminology and named method lineages before finalizing search rounds. |

## Calibration Notes

- arxiv calibration (high): Introduces Gaussian Splatting Feature Fields (GSFF) for privacy-preserving visual localization.
- arxiv calibration (high): Introduces GSVisLoc for generalizable localization directly against 3D Gaussian Splatting scene representations.
- arxiv calibration (high): Introduces LaVPR and language-vision place recognition under visual degradation.
- arxiv calibration (high): Uses VPR as an image-pair retrieval front-end and compares AnyLoc, SALAD, and MegaLoc with older descriptor families.
- arxiv calibration (high): FoL++ emphasizes region reliability, occlusion resistance, adaptive re-ranking, and efficiency.
- arxiv calibration (high): DisPlace uses multiple reference traversals to separate place identity from condition and viewpoint variation.
- arxiv calibration (high): Depth-aware distillation augments DINOv2 VPR in repetitive forest environments.
- arxiv calibration (high): DAPR identifies geographic long-tail imbalance in urban VPR benchmarks.

## Planner Notes

- llm dynamic expansion (high): The static embodied-AI taxonomy has no dedicated visual-localization family, so this run expands to the major metric camera-localization lineages and their deployment failure surfaces.
