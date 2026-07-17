# Query Plan: 近一年为何说反应式VLA已死世界模型当立

## Scope

- Knowledge IDs: EA-MODEL, EA-EVAL
- Families: vla, sim2real, tactile-force, world-model
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 168
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-reactive-vla-limit | limitation | `(all:VLA OR all:"vision-language-action") AND (all:reactive OR all:"error accumulation" OR all:recovery) AND all:robot` | Test the narrow claim that reactive next-action policies break on long-horizon execution and recovery. |
| dynamic-vla-world-model-fusion | mechanism | `(all:VLA OR all:"vision-language-action") AND all:"world model" AND all:robot` | Look for fusion rather than replacement between VLA policies and world models. |
| dynamic-world-action-model | mechanism | `(all:"world action model" OR all:"world-action model") AND all:robot` | Capture models that jointly represent actions and predicted futures. |
| dynamic-world-model-action-reliability | evaluation | `all:"world model" AND (all:"action fidelity" OR all:"physics adherence" OR all:"failure optimism") AND all:robot` | Distinguish useful predictive models from visually plausible but decision-invalid video generators. |
| dynamic-world-model-contact-recovery | limitation | `all:"world model" AND (all:tactile OR all:force OR all:contact) AND (all:recovery OR all:correction) AND all:robot` | Cover contact-rich tasks where RGB-only futures are partially observable. |
| dynamic-vla-benchmark-memorization | evaluation | `(all:VLA OR all:"vision-language-action") AND (all:memorization OR all:"benchmark leakage" OR all:overfit)` | Check whether standard benchmark gains overstate physical generalization. |
| calibrated-world-language-action | calibrated-term | `all:"world-language-action"` | Recent naming for architectures that combine language reasoning, predictive world modeling, and action synthesis. |
| calibrated-world-model-preference-reward | calibrated-term | `all:"world-model preference reward"` | Captures world models used as critics for VLA post-training. |
| calibrated-unified-vla-and-world-model | calibrated-term | `all:"unified VLA and world model"` | Captures explicit evidence against a simple replacement narrative. |
| calibration-world-language-action | calibrated-query | `all:"world-language-action" OR all:"world language action"` | Find WLA-family papers. |
| calibration-world-model-preference-vla | calibrated-query | `all:"world model" AND all:preference AND (all:VLA OR all:"vision-language-action")` | Find world-model critics used for VLA improvement. |
| calibration-unified-vla-world-model | calibrated-query | `all:unified AND all:"world model" AND (all:VLA OR all:"vision-language-action")` | Find joint rather than replacement architectures. |
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |
| vla-large-scale-robot-data | data-scaling | `all:"large-scale" AND all:"robot data"` | Surface scaling and dataset-layer discussions for robot foundation models. |
| vla-robot-foundation-action | foundation-model | `all:"robot foundation model" AND all:action` | Find broader foundation-model papers whose metadata may not use VLA. |
| vla-finetuning-policy | transfer | `all:"fine-tuning" AND all:"robot policy"` | Surface evidence about target-task adaptation and data requirements. |
| vla-data-mixture | data-mixture | `all:"data mixture" AND all:"robot foundation model"` | Find mixture and dataset composition papers that explain scaling behavior. |
| vla-negative-transfer | limitation | `all:"negative transfer" AND all:robot AND all:policy` | Search for failure cases where broad pretraining hurts target deployment. |
| sim2real-core | core | `(all:sim2real OR all:"sim-to-real") AND all:robot` | Find the main simulation-to-real transfer literature surface. |
| sim2real-real-validation | validation | `all:"real robot" AND all:validation AND all:simulation` | Find papers that verify simulation claims against real robot runs. |
| sim2real-synthetic-data | data-generation | `all:"synthetic data" AND all:"robot manipulation"` | Capture synthetic-data pipelines used to reduce real collection cost. |
| sim2real-domain-randomization | method | `all:"domain randomization" AND all:"robot manipulation"` | Find robustification methods for visual and physical sim-to-real gaps. |
| sim2real-correlation | evaluation | `all:"sim-real" AND all:correlation AND all:evaluation` | Surface work that measures whether simulation rankings predict real performance. |
| tactile-force-tactile-manipulation | core | `all:tactile AND all:"robot manipulation"` | Find tactile sensing papers tied to manipulation policies or control. |
| tactile-force-force-torque | force | `all:force AND all:torque AND all:robot` | Cover force/torque observability and low-dimensional contact feedback. |
| tactile-force-slip-detection | contact-state | `all:"slip detection" AND all:robot` | Find tactile and force cues for grasp stability and material interaction. |
| tactile-force-contact-rich | task-family | `all:"contact-rich" AND all:manipulation` | Surface high-contact tasks where vision-only policies often fail. |
| tactile-force-sensor-fusion | fusion | `all:"sensor fusion" AND all:tactile AND all:robot` | Find multimodal policies combining tactile, force, vision, or proprioception. |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| limits-and-counterevidence | 3 | dynamic-reactive-vla-limit, dynamic-world-model-contact-recovery, vla-negative-transfer, world-model-contact, world-model-long-horizon |
| adjacent-and-transfer | 3 | dynamic-vla-world-model-fusion, dynamic-world-action-model, dynamic-world-model-action-reliability, dynamic-vla-benchmark-memorization, calibrated-world-language-action, calibrated-world-model-preference-reward, calibrated-unified-vla-and-world-model, calibration-world-language-action, calibration-world-model-preference-vla, calibration-unified-vla-world-model, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, sim2real-synthetic-data, sim2real-correlation, tactile-force-force-torque, tactile-force-slip-detection, tactile-force-contact-rich, tactile-force-sensor-fusion, world-model-video-prediction, world-model-planning, ea-model-finetuning, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| direct-topic | 3 | vla-core, vla-named-models, sim2real-core, tactile-force-tactile-manipulation, world-model-robot, ea-model-named-foundation, ea-eval-closed-loop |
| evaluation-and-validation | 3 | sim2real-real-validation |
| mechanisms-and-interfaces | 3 | sim2real-domain-randomization, ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-vla-world-model-browser | `site:arxiv.org/abs VLA world model robot action fidelity recovery` | Fallback discovery for newly submitted fusion and evaluation papers. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-world-language-action-web | llm | `site:arxiv.org/abs world-language-action robot` | Calibrate the emerging WLA naming used by recent papers. |
| web-calibrated-world-language-action | arxiv | `"world-language-action" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: world-language-action. |
| web-calibrated-world-model-preference-reward | arxiv | `"world-model preference reward" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: world-model preference reward. |
| web-calibrated-unified-vla-and-world-model | arxiv | `"unified VLA and world model" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: unified VLA and world model. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-reactive-vla-limit | arxiv_api | llm | high | `(all:VLA OR all:"vision-language-action") AND (all:reactive OR all:"error accumulation" OR all:recovery) AND all:robot` | Test the narrow claim that reactive next-action policies break on long-horizon execution and recovery. |
| dynamic-vla-world-model-fusion | arxiv_api | llm | high | `(all:VLA OR all:"vision-language-action") AND all:"world model" AND all:robot` | Look for fusion rather than replacement between VLA policies and world models. |
| dynamic-world-action-model | arxiv_api | llm | high | `(all:"world action model" OR all:"world-action model") AND all:robot` | Capture models that jointly represent actions and predicted futures. |
| dynamic-world-model-action-reliability | arxiv_api | llm | high | `all:"world model" AND (all:"action fidelity" OR all:"physics adherence" OR all:"failure optimism") AND all:robot` | Distinguish useful predictive models from visually plausible but decision-invalid video generators. |
| dynamic-world-model-contact-recovery | arxiv_api | llm | high | `all:"world model" AND (all:tactile OR all:force OR all:contact) AND (all:recovery OR all:correction) AND all:robot` | Cover contact-rich tasks where RGB-only futures are partially observable. |
| dynamic-vla-benchmark-memorization | arxiv_api | llm | high | `(all:VLA OR all:"vision-language-action") AND (all:memorization OR all:"benchmark leakage" OR all:overfit)` | Check whether standard benchmark gains overstate physical generalization. |
| dynamic-vla-world-model-browser | browser_fallback | llm | medium | `site:arxiv.org/abs VLA world model robot action fidelity recovery` | Fallback discovery for newly submitted fusion and evaluation papers. |
| dynamic-world-language-action-web | web_calibration | llm | medium | `site:arxiv.org/abs world-language-action robot` | Calibrate the emerging WLA naming used by recent papers. |

## Calibration Notes

- arxiv calibration (high): RynnVLA-002 uses the phrase unified vision-language-action and world model.
- arxiv calibration (high): NORA-1.5 uses world-model- and action-based preference rewards for VLA post-training.
- arxiv calibration (high): WLA-0 introduces the term world-language-action model.

## Planner Notes

- llm dynamic expansion (high): The claim contrasts reactive VLA policies with predictive, action-conditioned models; search must cover failure/recovery, physical admissibility, 4D/contact dynamics, and VLA-world-model fusion.
