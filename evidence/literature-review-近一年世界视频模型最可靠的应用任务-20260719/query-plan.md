# Query Plan: 近一年世界视频模型最可靠的应用任务

## Scope

- Knowledge IDs: EA-MODEL, EA-EVAL
- Families: world-model, vla, sim2real, tactile-force
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 100
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-world-model-policy-evaluation | evaluation | `all:"world model" AND all:"policy evaluation" AND all:robot` | Test whether policy ranking and scalable evaluation have the strongest sim-real evidence. |
| dynamic-world-model-data-synthesis | mechanism | `all:"world model" AND (all:"data synthesis" OR all:"synthetic demonstrations") AND all:robot` | Cover training-time generation and augmentation, where model errors are filtered before deployment. |
| dynamic-world-model-post-training-recovery | mechanism | `all:"world model" AND (all:"post-training" OR all:recovery OR all:"self-correction") AND all:robot` | Cover failure-adjacent correction and policy post-training rather than unconstrained generation. |
| dynamic-world-model-planning-control | deployment | `all:"video world model" AND (all:planning OR all:control) AND all:robot` | Find direct planning/control evidence and its deployment constraints. |
| dynamic-world-model-admissibility | limitation | `all:"world model" AND (all:"action fidelity" OR all:"physics adherence" OR all:"failure optimism") AND all:robot` | Test whether visual realism is insufficient for decision use. |
| dynamic-world-model-long-horizon-efficiency | limitation | `all:"world model" AND all:robot AND (all:"long-horizon" OR all:latency OR all:efficiency)` | Cover compounding rollout error and online inference cost. |
| dynamic-world-model-geometry-distillation | mechanism | `all:"world model" AND (all:4D OR all:geometry OR all:"point track") AND all:"robot manipulation"` | Cover training-time geometry supervision and distillation that may improve policies without online rollout cost. |
| dynamic-world-action-model-contact | limitation | `(all:"world action model" OR all:"video world model") AND (all:contact OR all:tactile OR all:force) AND all:robot` | Check reliability boundaries for contact-rich manipulation and partially observed physics. |
| calibrated-neural-simulator-for-policy-evaluation | calibrated-term | `all:"neural simulator for policy evaluation"` | Names the most directly validated offline application surface. |
| calibrated-task-progress-aware-scoring | calibrated-term | `all:"task-progress-aware scoring"` | Separates generating a rollout from scoring policy progress. |
| calibrated-world-action-model | calibrated-term | `all:"world action model"` | Captures joint prediction-and-control systems that may not use video world model in metadata. |
| calibrated-persistent-rollout | calibrated-term | `all:"persistent rollout"` | Captures long-horizon stabilization and compounding-error work. |
| calibration-neural-simulator-policy-evaluation | calibrated-query | `all:"neural simulator" AND all:"policy evaluation" AND all:robot` | Find evaluator-oriented video world models. |
| calibration-task-progress-world-model | calibrated-query | `all:"task progress" AND all:"world model" AND all:robot` | Find world-model rollouts paired with task-progress or reward scoring. |
| calibration-world-action-model | calibrated-query | `(all:"world action model" OR all:"world-action model") AND all:robot` | Find joint video-action and direct-control work. |
| calibration-persistent-world-model-rollout | calibrated-query | `all:persistent AND all:"world model" AND all:rollout AND all:robot` | Find long-horizon rollout stabilization studies. |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-world-model-policy-evaluation, dynamic-world-model-data-synthesis, dynamic-world-model-post-training-recovery, dynamic-world-model-planning-control, dynamic-world-model-geometry-distillation, calibrated-neural-simulator-for-policy-evaluation, calibrated-task-progress-aware-scoring, calibrated-world-action-model, calibrated-persistent-rollout, calibration-neural-simulator-policy-evaluation, calibration-task-progress-world-model, calibration-world-action-model, calibration-persistent-world-model-rollout, world-model-video-prediction, world-model-planning, vla-open-x-embodiment |
| limits-and-counterevidence | 3 | dynamic-world-model-admissibility, dynamic-world-model-long-horizon-efficiency, dynamic-world-action-model-contact, world-model-contact, world-model-long-horizon |
| direct-topic | 3 | world-model-robot, vla-core, vla-named-models |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-reliable-world-model-tasks-browser | `site:arxiv.org/abs 2026 robot video world model policy evaluation data synthesis recovery planning` | Discover newly submitted task-oriented papers if the API under-recovers. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-world-model-neural-simulator-web | llm | `site:arxiv.org/abs 2026 robot neural simulator world model policy evaluation` | Calibrate current naming around video-world-model evaluators. |
| web-calibrated-neural-simulator-for-policy-evaluation | arxiv | `"neural simulator for policy evaluation" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: neural simulator for policy evaluation. |
| web-calibrated-task-progress-aware-scoring | arxiv | `"task-progress-aware scoring" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: task-progress-aware scoring. |
| web-calibrated-world-action-model | arxiv | `"world action model" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: world action model. |
| web-calibrated-persistent-rollout | arxiv | `"persistent rollout" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: persistent rollout. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-world-model-policy-evaluation | arxiv_api | llm | high | `all:"world model" AND all:"policy evaluation" AND all:robot` | Test whether policy ranking and scalable evaluation have the strongest sim-real evidence. |
| dynamic-world-model-data-synthesis | arxiv_api | llm | high | `all:"world model" AND (all:"data synthesis" OR all:"synthetic demonstrations") AND all:robot` | Cover training-time generation and augmentation, where model errors are filtered before deployment. |
| dynamic-world-model-post-training-recovery | arxiv_api | llm | high | `all:"world model" AND (all:"post-training" OR all:recovery OR all:"self-correction") AND all:robot` | Cover failure-adjacent correction and policy post-training rather than unconstrained generation. |
| dynamic-world-model-planning-control | arxiv_api | llm | high | `all:"video world model" AND (all:planning OR all:control) AND all:robot` | Find direct planning/control evidence and its deployment constraints. |
| dynamic-world-model-admissibility | arxiv_api | llm | high | `all:"world model" AND (all:"action fidelity" OR all:"physics adherence" OR all:"failure optimism") AND all:robot` | Test whether visual realism is insufficient for decision use. |
| dynamic-world-model-long-horizon-efficiency | arxiv_api | llm | high | `all:"world model" AND all:robot AND (all:"long-horizon" OR all:latency OR all:efficiency)` | Cover compounding rollout error and online inference cost. |
| dynamic-world-model-geometry-distillation | arxiv_api | llm | high | `all:"world model" AND (all:4D OR all:geometry OR all:"point track") AND all:"robot manipulation"` | Cover training-time geometry supervision and distillation that may improve policies without online rollout cost. |
| dynamic-world-action-model-contact | arxiv_api | llm | high | `(all:"world action model" OR all:"video world model") AND (all:contact OR all:tactile OR all:force) AND all:robot` | Check reliability boundaries for contact-rich manipulation and partially observed physics. |
| dynamic-reliable-world-model-tasks-browser | browser_fallback | llm | medium | `site:arxiv.org/abs 2026 robot video world model policy evaluation data synthesis recovery planning` | Discover newly submitted task-oriented papers if the API under-recovers. |
| dynamic-world-model-neural-simulator-web | web_calibration | llm | medium | `site:arxiv.org/abs 2026 robot neural simulator world model policy evaluation` | Calibrate current naming around video-world-model evaluators. |

## Calibration Notes

- arxiv calibration (high): RoboWorld uses neural simulator, policy evaluation, Step Forcing, task-progress-aware scoring, and sim-real rank alignment.
- arxiv calibration (high): Qwen-RobotWorld groups current applications into synthetic data generation, virtual policy evaluation, and language-guided planning signals.
- arxiv calibration (high): MotuBrain uses the current term world action model for joint video-action prediction and real-time control.
- arxiv calibration (high): Persistent Robot World Models foregrounds autoregressive rollout drift and rollout-stabilizing post-training.

## Planner Notes

- llm dynamic expansion (high): The review asks which application tasks are reliable, so discovery must separate training-time/offline assistance, policy evaluation, recovery, planning, and direct control, and must include counterevidence on action fidelity, physical adherence, long-horizon drift, and latency.
