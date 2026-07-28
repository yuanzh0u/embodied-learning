# Query Plan: EgoVerse ecosystem: egocentric human data, human-to-robot transfer, evaluation, and industry collaboration

## Scope

- Knowledge IDs: EA-DATA, EA-XEMBODIMENT, EA-EVAL, EA-MODEL, EA-BIZ
- Families: droid-ego4d, retargeting, teleoperation-demo-quality, vla
- Suggested categories: cs.AI, cs.CV, cs.HC, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 200
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-egoverse-core | named-project | `all:EgoVerse` | Recover the core paper and follow-on work that explicitly names the living dataset ecosystem. |
| dynamic-danfei-egocentric-lineage | author-lineage | `au:"Danfei Xu" AND all:(egocentric OR human-to-robot OR cross-embodiment)` | Cover the direct research lineage without using the author as evidence by authority. |
| dynamic-named-lineage | named-method | `all:(EgoMimic OR EgoBridge OR EMMA OR EgoScale) AND all:(robot OR manipulation)` | Recover the capture, alignment, mobile-manipulation, and dexterous-scaling lineage around EgoVerse. |
| dynamic-emergent-human-robot-transfer | mechanism | `all:"human to robot transfer" AND all:(VLA OR "vision-language-action" OR pretraining)` | Test the hypothesis that diverse robot pretraining creates embodiment-agnostic transfer from human data. |
| dynamic-egocentric-action-supervision | mechanism | `all:"egocentric human data" AND all:(action OR trajectory OR retargeting OR policy)` | Find how human video is converted into robot-action supervision rather than used only for perception pretraining. |
| dynamic-dataset-composition-alignment | data-quality | `all:"dataset composition" AND all:(robot OR manipulation) AND all:(alignment OR diversity OR retrieval)` | Cover target relevance and diversity composition instead of treating hours as a sufficient quality measure. |
| dynamic-cross-lab-evaluation | evaluation | `all:("cross-lab" OR "multiple labs" OR reproducible) AND all:(robot learning OR manipulation) AND all:evaluation` | Find multi-site evaluation designs and limits relevant to EgoVerse's consortium-scale study. |
| dynamic-human-data-negative-transfer | limitation | `all:("human video" OR "human data") AND all:robot AND all:("negative transfer" OR limitation OR failure OR mismatch)` | Actively search for counterevidence and transfer failures. |
| dynamic-egocentric-contact-limit | limitation | `all:egocentric AND all:robot AND all:(contact OR tactile OR occlusion) AND all:(transfer OR imitation)` | Cover states that vision/pose-only human data may not observe reliably. |
| dynamic-data-governance-license | deployment-governance | `all:(robotics OR egocentric) AND all:dataset AND all:(license OR privacy OR provenance OR versioning)` | Cover governance and reproducibility limits of living, multi-provider datasets. |
| dynamic-rss26-adjacent | adjacent-venue | `all:("robot-free egocentric" OR "human demonstrations" OR "cross-embodiment transfer") AND all:(manipulation OR imitation)` | Recover RSS 2026-adjacent routes without using venue acceptance as scientific evidence. |
| calibrated-human-to-robot-transfer | calibrated-term | `all:"human-to-robot transfer"` | Canonical scientific outcome used by the paper and related lineage. |
| calibrated-data-centric-robotics | calibrated-term | `all:"data-centric robotics"` | Umbrella framing for source, composition, quality, evaluation, and flywheel questions. |
| calibrated-training-validated-data | calibrated-term | `all:"training-validated data"` | Current ecosystem claim that requires a scientific operational definition. |
| calibrated-living-dataset | calibrated-term | `all:"living dataset"` | Signals versioning, contribution, governance, and reproducibility questions. |
| calibration-data-centric-robotics | calibrated-query | `all:"data-centric robotics" OR (all:"dataset composition" AND all:robot)` | Translate workshop framing into paper-search vocabulary. |
| calibration-living-dataset | calibrated-query | `all:"living dataset" AND all:(robot OR egocentric)` | Find work on continuously growing datasets and versioned ecosystems. |
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
| teleop-imitation-learning | core | `all:teleoperation AND all:"imitation learning" AND all:robot` | Find the main literature surface connecting teleoperation to robot policy learning. |
| teleop-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface trace consistency, operator skill, and data acceptance criteria. |
| teleop-operator-burden | human-factor | `all:operator AND all:burden AND all:teleoperation` | Find papers about human workload and collection throughput. |
| teleop-latency | system-limitation | `all:latency AND all:teleoperation AND all:robot` | Capture delay and synchronization limits that affect demonstration fidelity. |
| teleop-action-interface | policy-interface | `all:"action interface" AND all:robot AND all:demonstration` | Find work where action-space choices determine whether demonstrations transfer. |
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |
| vla-large-scale-robot-data | data-scaling | `all:"large-scale" AND all:"robot data"` | Surface scaling and dataset-layer discussions for robot foundation models. |
| vla-robot-foundation-action | foundation-model | `all:"robot foundation model" AND all:action` | Find broader foundation-model papers whose metadata may not use VLA. |
| vla-finetuning-policy | transfer | `all:"fine-tuning" AND all:"robot policy"` | Surface evidence about target-task adaptation and data requirements. |
| vla-data-mixture | data-mixture | `all:"data mixture" AND all:"robot foundation model"` | Find mixture and dataset composition papers that explain scaling behavior. |
| vla-negative-transfer | limitation | `all:"negative transfer" AND all:robot AND all:policy` | Search for failure cases where broad pretraining hurts target deployment. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-egoverse-core, dynamic-named-lineage, droid-robot-manipulation, ego4d-robot-learning, retargeting-robot-manipulation, teleop-imitation-learning, teleop-demonstration-quality, vla-core, vla-named-models, ea-data-robot-demonstrations, ea-xembodiment-cross-embodiment, ea-eval-closed-loop |
| adjacent-and-transfer | 3 | dynamic-danfei-egocentric-lineage, dynamic-emergent-human-robot-transfer, dynamic-egocentric-action-supervision, dynamic-dataset-composition-alignment, dynamic-cross-lab-evaluation, dynamic-rss26-adjacent, calibrated-human-to-robot-transfer, calibrated-data-centric-robotics, calibrated-training-validated-data, calibrated-living-dataset, calibration-data-centric-robotics, calibration-living-dataset, droid-ego-egocentric-video, droid-ego-in-the-wild, droid-ego-data-mixture, retargeting-human-to-robot-mapping, retargeting-dexterous-hand, retargeting-gripper-demonstration, teleop-operator-burden, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, ea-data-in-the-wild, ea-data-dataset-curation, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot, ea-eval-open-loop-benchmark, ea-eval-world-model |
| limits-and-counterevidence | 3 | dynamic-human-data-negative-transfer, dynamic-egocentric-contact-limit, retargeting-morphology-gap, teleop-latency, vla-negative-transfer |
| deployment-and-operations | 3 | dynamic-data-governance-license |
| mechanisms-and-interfaces | 3 | teleop-action-interface, ea-xembodiment-action-representation |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-egoverse-browser | `site:arxiv.org/abs EgoVerse egocentric human robot transfer` | Recover the core paper and explicit follow-ons if API metadata lags. |
| dynamic-lineage-browser | `site:arxiv.org/abs (EgoMimic OR EgoBridge OR EMMA OR EgoScale) robot` | Recover named lineage papers and their identifiers. |
| dynamic-counterevidence-browser | `site:arxiv.org/abs egocentric human data robot (failure OR limitation OR negative transfer)` | Find limiting or contradictory evidence that may be under-indexed. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-rss-calibration | agent | `site:roboticsconference.org 2026 EgoVerse human data imitation learning` | Calibrate official venue terminology and adjacent session names. |
| web-calibrated-egoverse | rss-official | `"EgoVerse" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: EgoVerse. |
| web-calibrated-human-to-robot-transfer | rss-official | `"human-to-robot transfer" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: human-to-robot transfer. |
| web-calibrated-data-centric-robotics | rss-workshop-official | `"data-centric robotics" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: data-centric robotics. |
| web-calibrated-training-validated-data | social-calibration | `"training-validated data" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: training-validated data. |
| web-calibrated-living-dataset | project-page | `"living dataset" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: living dataset. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-egoverse-core | arxiv_api | agent | high | `all:EgoVerse` | Recover the core paper and follow-on work that explicitly names the living dataset ecosystem. |
| dynamic-danfei-egocentric-lineage | arxiv_api | agent | high | `au:"Danfei Xu" AND all:(egocentric OR human-to-robot OR cross-embodiment)` | Cover the direct research lineage without using the author as evidence by authority. |
| dynamic-named-lineage | arxiv_api | agent | high | `all:(EgoMimic OR EgoBridge OR EMMA OR EgoScale) AND all:(robot OR manipulation)` | Recover the capture, alignment, mobile-manipulation, and dexterous-scaling lineage around EgoVerse. |
| dynamic-emergent-human-robot-transfer | arxiv_api | agent | high | `all:"human to robot transfer" AND all:(VLA OR "vision-language-action" OR pretraining)` | Test the hypothesis that diverse robot pretraining creates embodiment-agnostic transfer from human data. |
| dynamic-egocentric-action-supervision | arxiv_api | agent | high | `all:"egocentric human data" AND all:(action OR trajectory OR retargeting OR policy)` | Find how human video is converted into robot-action supervision rather than used only for perception pretraining. |
| dynamic-dataset-composition-alignment | arxiv_api | agent | high | `all:"dataset composition" AND all:(robot OR manipulation) AND all:(alignment OR diversity OR retrieval)` | Cover target relevance and diversity composition instead of treating hours as a sufficient quality measure. |
| dynamic-cross-lab-evaluation | arxiv_api | agent | medium | `all:("cross-lab" OR "multiple labs" OR reproducible) AND all:(robot learning OR manipulation) AND all:evaluation` | Find multi-site evaluation designs and limits relevant to EgoVerse's consortium-scale study. |
| dynamic-human-data-negative-transfer | arxiv_api | agent | high | `all:("human video" OR "human data") AND all:robot AND all:("negative transfer" OR limitation OR failure OR mismatch)` | Actively search for counterevidence and transfer failures. |
| dynamic-egocentric-contact-limit | arxiv_api | agent | medium | `all:egocentric AND all:robot AND all:(contact OR tactile OR occlusion) AND all:(transfer OR imitation)` | Cover states that vision/pose-only human data may not observe reliably. |
| dynamic-data-governance-license | arxiv_api | agent | medium | `all:(robotics OR egocentric) AND all:dataset AND all:(license OR privacy OR provenance OR versioning)` | Cover governance and reproducibility limits of living, multi-provider datasets. |
| dynamic-rss26-adjacent | arxiv_api | agent | medium | `all:("robot-free egocentric" OR "human demonstrations" OR "cross-embodiment transfer") AND all:(manipulation OR imitation)` | Recover RSS 2026-adjacent routes without using venue acceptance as scientific evidence. |
| dynamic-egoverse-browser | browser_fallback | agent | high | `site:arxiv.org/abs EgoVerse egocentric human robot transfer` | Recover the core paper and explicit follow-ons if API metadata lags. |
| dynamic-lineage-browser | browser_fallback | agent | high | `site:arxiv.org/abs (EgoMimic OR EgoBridge OR EMMA OR EgoScale) robot` | Recover named lineage papers and their identifiers. |
| dynamic-counterevidence-browser | browser_fallback | agent | medium | `site:arxiv.org/abs egocentric human data robot (failure OR limitation OR negative transfer)` | Find limiting or contradictory evidence that may be under-indexed. |
| dynamic-rss-calibration | web_calibration | agent | high | `site:roboticsconference.org 2026 EgoVerse human data imitation learning` | Calibrate official venue terminology and adjacent session names. |

## Calibration Notes

- rss-official calibration (high): Confirms EgoVerse as RSS 2026 Paper 92 in Datasets and Benchmarks.
- rss-workshop-official calibration (high): Calibrates data-centric robotics terms: sources, quality versus scale, composition, evaluation, and data flywheels.
- project-page calibration (medium): Confirms living dataset/ecosystem vocabulary and current partner list.
- author-homepage calibration (medium): Confirms named lineage: EgoMimic, EgoBridge, EMMA, Emergence, and EgoVerse.
- social-calibration calibration (low): Used only to discover new partner names and current ecosystem vocabulary.

## Planner Notes

- agent dynamic expansion (high): Expansion derived from the EgoVerse paper, official project pages, RSS 2026 program, and the repository seed survey.
