# Query Plan: 具身传感器感知误差

## Scope

- Knowledge IDs: EA-SENSOR, EA-DATA, EA-EVAL
- Families: tactile-force, last-centimeter, sim2real
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Minimum candidate count: 20

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-sensor-noise-robot-perception | dynamic-association | `(all:"sensor noise" OR all:"perception error" OR all:"calibration error") AND (all:robot OR all:"robot manipulation")` | Directly targets papers that frame embodied perception as sensor or calibration error. |
| dynamic-uncertainty-state-estimation-manipulation | dynamic-association | `(all:uncertainty OR all:"state estimation") AND all:"robot manipulation" AND (all:vision OR all:tactile OR all:force)` | Captures uncertainty-aware perception and state-estimation errors in manipulation. |
| dynamic-occlusion-depth-pose-error | dynamic-association | `(all:occlusion OR all:"depth noise" OR all:"pose error") AND all:"robot manipulation"` | Targets visual and 3D perception failure modes that affect embodied control. |
| dynamic-slip-contact-error | dynamic-association | `(all:slip OR all:"contact state" OR all:"contact estimation") AND (all:tactile OR all:force) AND all:robot` | Targets contact-rich perception errors that RGB cannot directly observe. |
| dynamic-multimodal-robustness-sensor-failure | dynamic-association | `(all:"sensor fusion" OR all:multimodal) AND (all:robustness OR all:"sensor failure" OR all:"missing modality") AND all:robot` | Covers multimodal robustness and degradation under unreliable or missing sensor inputs. |
| tactile-force-tactile-manipulation | core | `all:tactile AND all:"robot manipulation"` | Find tactile sensing papers tied to manipulation policies or control. |
| tactile-force-force-torque | force | `all:force AND all:torque AND all:robot` | Cover force/torque observability and low-dimensional contact feedback. |
| tactile-force-slip-detection | contact-state | `all:"slip detection" AND all:robot` | Find tactile and force cues for grasp stability and material interaction. |
| tactile-force-contact-rich | task-family | `all:"contact-rich" AND all:manipulation` | Surface high-contact tasks where vision-only policies often fail. |
| tactile-force-sensor-fusion | fusion | `all:"sensor fusion" AND all:tactile AND all:robot` | Find multimodal policies combining tactile, force, vision, or proprioception. |
| last-centimeter-exact | core | `all:"last centimeter" AND all:robot` | Catch papers that explicitly name the deployment bottleneck. |
| last-centimeter-visual-servoing | pre-contact | `all:"visual servoing" AND all:"robot manipulation"` | Find close-range pose correction before contact closure. |
| last-centimeter-force-insertion | contact | `all:"force control" AND all:insertion AND all:robot` | Surface insertion and compliant-contact methods for final alignment. |
| last-centimeter-failure-recovery | recovery | `all:"failure recovery" AND all:"robot manipulation"` | Find retry, recovery, and takeover strategies after near-goal failures. |
| last-centimeter-fixture | deployment-adjacent | `(all:fixture OR all:fixturing) AND all:robot AND all:insertion` | Capture fixture and workcell design that reduces contact uncertainty. |
| sim2real-core | core | `(all:sim2real OR all:"sim-to-real") AND all:robot` | Find the main simulation-to-real transfer literature surface. |
| sim2real-real-validation | validation | `all:"real robot" AND all:validation AND all:simulation` | Find papers that verify simulation claims against real robot runs. |
| sim2real-synthetic-data | data-generation | `all:"synthetic data" AND all:"robot manipulation"` | Capture synthetic-data pipelines used to reduce real collection cost. |
| sim2real-domain-randomization | method | `all:"domain randomization" AND all:"robot manipulation"` | Find robustification methods for visual and physical sim-to-real gaps. |
| sim2real-correlation | evaluation | `all:"sim-real" AND all:correlation AND all:evaluation` | Surface work that measures whether simulation rankings predict real performance. |
| ea-sensor-multimodal-policy | core | `all:multimodal AND all:"robot manipulation" AND all:policy` | Find policy papers where sensor fusion affects manipulation behavior. |
| ea-sensor-tactile-force | contact | `all:tactile AND all:force AND all:"robot manipulation"` | Cover physical observability beyond RGB, especially contact and force cues. |
| ea-sensor-point-cloud | geometry | `all:"point cloud" AND all:"robot manipulation"` | Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks. |
| ea-sensor-occlusion | limitation | `all:occlusion AND all:"robot perception" AND all:manipulation` | Expose perception failure cases where single-view RGB is insufficient. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-browser-sensor-perception-error | `site:arxiv.org/abs robot manipulation sensor perception error tactile force occlusion 2026` | Fallback discovery if API recall is weak for the combined framing. |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-web-sensor-error-terms | agent | `"robot manipulation" "sensor noise" "tactile" "uncertainty"` | Calibrate current wording around embodied sensor error discussions. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-sensor-noise-robot-perception | arxiv_api | agent | medium | `(all:"sensor noise" OR all:"perception error" OR all:"calibration error") AND (all:robot OR all:"robot manipulation")` | Directly targets papers that frame embodied perception as sensor or calibration error. |
| dynamic-uncertainty-state-estimation-manipulation | arxiv_api | agent | medium | `(all:uncertainty OR all:"state estimation") AND all:"robot manipulation" AND (all:vision OR all:tactile OR all:force)` | Captures uncertainty-aware perception and state-estimation errors in manipulation. |
| dynamic-occlusion-depth-pose-error | arxiv_api | agent | medium | `(all:occlusion OR all:"depth noise" OR all:"pose error") AND all:"robot manipulation"` | Targets visual and 3D perception failure modes that affect embodied control. |
| dynamic-slip-contact-error | arxiv_api | agent | medium | `(all:slip OR all:"contact state" OR all:"contact estimation") AND (all:tactile OR all:force) AND all:robot` | Targets contact-rich perception errors that RGB cannot directly observe. |
| dynamic-multimodal-robustness-sensor-failure | arxiv_api | agent | medium | `(all:"sensor fusion" OR all:multimodal) AND (all:robustness OR all:"sensor failure" OR all:"missing modality") AND all:robot` | Covers multimodal robustness and degradation under unreliable or missing sensor inputs. |
| dynamic-browser-sensor-perception-error | browser_fallback | agent | medium | `site:arxiv.org/abs robot manipulation sensor perception error tactile force occlusion 2026` | Fallback discovery if API recall is weak for the combined framing. |
| dynamic-web-sensor-error-terms | web_calibration | agent | medium | `"robot manipulation" "sensor noise" "tactile" "uncertainty"` | Calibrate current wording around embodied sensor error discussions. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- agent dynamic expansion (medium): The user topic combines embodied sensor perception with error analysis; static EA-SENSOR/tactile-force terms need added recall for noise, uncertainty, calibration, occlusion, drift, and closed-loop state estimation failure.
