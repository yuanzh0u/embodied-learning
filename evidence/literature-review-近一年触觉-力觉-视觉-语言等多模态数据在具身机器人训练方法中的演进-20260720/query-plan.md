# Query Plan: 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进

## Scope

- Knowledge IDs: EA-SENSOR, EA-MODEL, EA-XEMBODIMENT, EA-DATA
- Families: tactile-force, vla, world-model, retargeting
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 128
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-vision-language-tactile-action | dynamic-association | `all:(vision AND language AND tactile AND action) AND all:robot` | Capture explicit extensions from VLA to vision-language-tactile-action policies. |
| dynamic-force-conditioned-tactile-foresight | mechanism | `all:(force AND tactile AND prediction) AND all:(robot AND manipulation)` | Find methods that separate global force signals from local tactile dynamics and use them predictively. |
| dynamic-representation-aligned-tactile-grounding | mechanism | `all:(tactile AND representation AND grounding) AND all:(robot AND action)` | Test whether tactile supervision is moving from raw-input fusion to selected action-representation layers. |
| dynamic-tactile-distillation | transfer | `all:(tactile AND distillation) AND all:(robot OR manipulation)` | Cover training-time touch or force supervision that is distilled away at deployment. |
| dynamic-contact-gated-multimodal-fusion | policy-interface | `all:(contact AND gated AND multimodal AND fusion) AND all:robot` | Capture sparse/event-driven fusion that activates physical modalities only around contact. |
| dynamic-multisensory-continual-adaptation | transfer | `all:(multisensory AND continual AND learning) AND all:(robot AND force)` | Find post-training routes that adapt pretrained visual policies to force or touch without full retraining. |
| dynamic-missing-modality-robustness | limitation | `all:(missing AND modality AND robustness) AND all:(robot AND manipulation)` | Cover sensor-dropout and deployment-time modality-mismatch counterevidence. |
| dynamic-tactile-vla-post-training | deployment | `all:(tactile AND VLA AND post-training) AND all:robot` | Capture tactile self-correction and policy steering methods applied after VLA pretraining. |
| calibrated-representation-aligned-tactile-grounding | calibrated-term | `all:"representation-aligned tactile grounding"` | Recent vocabulary for choosing the internal policy layer at which future-touch supervision is applied. |
| calibrated-force-guided-tactile-foresight | calibrated-term | `all:"force-guided tactile foresight"` | Distinguishes global wrist force/torque conditioning from local tactile prediction. |
| calibrated-cross-modal-representation-compatibility | calibrated-term | `all:"cross-modal representation compatibility"` | Names the emerging finding that structured compatible representations matter more than adding more modalities. |
| calibrated-tactile-distillation | calibrated-term | `all:"tactile distillation"` | Covers training-time physical sensing that is removed from the deployment sensor stack. |
| calibration-representation-aligned-tactile | calibrated-query | `all:(representation AND tactile AND grounding) AND all:(robot AND manipulation)` | Search the calibrated terminology in arXiv metadata. |
| calibration-tactile-distillation-vla | calibrated-query | `all:(tactile AND distillation AND VLA) AND all:robot` | Search training-time touch transfer into deployable VLA policies. |
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
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-vision-language-tactile-action, dynamic-force-conditioned-tactile-foresight, dynamic-representation-aligned-tactile-grounding, dynamic-tactile-distillation, dynamic-multisensory-continual-adaptation, dynamic-tactile-vla-post-training, calibrated-representation-aligned-tactile-grounding, calibrated-force-guided-tactile-foresight, calibrated-cross-modal-representation-compatibility, calibrated-tactile-distillation, calibration-representation-aligned-tactile, calibration-tactile-distillation-vla, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, world-model-video-prediction, world-model-planning |
| mechanisms-and-interfaces | 3 | dynamic-contact-gated-multimodal-fusion |
| limits-and-counterevidence | 3 | dynamic-missing-modality-robustness, vla-negative-transfer, world-model-contact, world-model-long-horizon |
| direct-topic | 3 | tactile-force-tactile-manipulation, vla-core, vla-named-models, world-model-robot |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-vlta-browser | `site:arxiv.org/abs (tactile OR force) (VLA OR vision-language-action) robot manipulation` | Recover named VLTA/VLA tactile variants missed by metadata wording. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-alignment-calibration | llm | `site:arxiv.org/abs tactile representation alignment action expert robot` | Calibrate recent wording around where tactile supervision is injected. |
| web-calibrated-representation-aligned-tactile-grounding | arxiv | `"representation-aligned tactile grounding" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: representation-aligned tactile grounding. |
| web-calibrated-force-guided-tactile-foresight | arxiv | `"force-guided tactile foresight" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: force-guided tactile foresight. |
| web-calibrated-cross-modal-representation-compatibility | arxiv | `"cross-modal representation compatibility" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: cross-modal representation compatibility. |
| web-calibrated-tactile-distillation | arxiv | `"tactile distillation" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: tactile distillation. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-vision-language-tactile-action | arxiv_api | llm | medium | `all:(vision AND language AND tactile AND action) AND all:robot` | Capture explicit extensions from VLA to vision-language-tactile-action policies. |
| dynamic-force-conditioned-tactile-foresight | arxiv_api | llm | medium | `all:(force AND tactile AND prediction) AND all:(robot AND manipulation)` | Find methods that separate global force signals from local tactile dynamics and use them predictively. |
| dynamic-representation-aligned-tactile-grounding | arxiv_api | llm | medium | `all:(tactile AND representation AND grounding) AND all:(robot AND action)` | Test whether tactile supervision is moving from raw-input fusion to selected action-representation layers. |
| dynamic-tactile-distillation | arxiv_api | llm | medium | `all:(tactile AND distillation) AND all:(robot OR manipulation)` | Cover training-time touch or force supervision that is distilled away at deployment. |
| dynamic-contact-gated-multimodal-fusion | arxiv_api | llm | medium | `all:(contact AND gated AND multimodal AND fusion) AND all:robot` | Capture sparse/event-driven fusion that activates physical modalities only around contact. |
| dynamic-multisensory-continual-adaptation | arxiv_api | llm | medium | `all:(multisensory AND continual AND learning) AND all:(robot AND force)` | Find post-training routes that adapt pretrained visual policies to force or touch without full retraining. |
| dynamic-missing-modality-robustness | arxiv_api | llm | medium | `all:(missing AND modality AND robustness) AND all:(robot AND manipulation)` | Cover sensor-dropout and deployment-time modality-mismatch counterevidence. |
| dynamic-tactile-vla-post-training | arxiv_api | llm | medium | `all:(tactile AND VLA AND post-training) AND all:robot` | Capture tactile self-correction and policy steering methods applied after VLA pretraining. |
| dynamic-vlta-browser | browser_fallback | llm | medium | `site:arxiv.org/abs (tactile OR force) (VLA OR vision-language-action) robot manipulation` | Recover named VLTA/VLA tactile variants missed by metadata wording. |
| dynamic-alignment-calibration | web_calibration | llm | medium | `site:arxiv.org/abs tactile representation alignment action expert robot` | Calibrate recent wording around where tactile supervision is injected. |

## Calibration Notes

- arxiv calibration (high): Uses representation-aligned tactile grounding and future tactile prediction at intermediate action-expert features.
- arxiv calibration (high): Uses force-guided tactile foresight, compact latent prediction, and tactile-guided gating.
- arxiv calibration (high): Frames multimodal training as representation compatibility rather than modality scaling.
- arxiv calibration (high): Uses tactile distillation to train a policy that does not require tactile input at inference time.

## Planner Notes

- llm dynamic expansion (medium): The review question spans modality roles, fusion timing, representation alignment, post-training, and deployment-time sensor availability; these interfaces are wider than the static tactile-force and VLA families alone.
