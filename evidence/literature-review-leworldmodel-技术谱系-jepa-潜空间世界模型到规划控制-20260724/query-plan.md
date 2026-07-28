# Query Plan: LeWorldModel 技术谱系：JEPA 潜空间世界模型到规划控制

## Scope

- Knowledge IDs: EA-MODEL, EA-EVAL
- Families: world-model
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 140
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-lewm-exact | named-method | `all:"LeWorldModel" OR all:"LeWM"` | Recover the focal paper, direct variants, follow-ups, and papers that evaluate or reuse LeWM. |
| dynamic-fast-lewm | named-variant | `all:"Fast LeWorldModel" OR all:"Fast-LeWM"` | Capture the direct multi-horizon/prefix-prediction response to LeWM rollout cost and error accumulation. |
| dynamic-lewm-amortized-planning | named-variant | `all:"Latent Geometry Beyond Search" OR (all:"LeWorldModel" AND all:"inverse dynamics")` | Capture learned inverse-dynamics planning that replaces online search in a pretrained LeWM latent space. |
| dynamic-lejepa-sigreg | mechanism | `all:"LeJEPA" OR all:"Sketched Isotropic Gaussian Regularization" OR all:"SIGReg"` | Recover the anti-collapse theory and regularizer inherited by LeWM. |
| dynamic-end-to-end-jepa-world-model | mechanism | `(all:JEPA OR all:"joint embedding predictive") AND all:"world model" AND (all:"end-to-end" OR all:pixels)` | Find end-to-end predictive-embedding world models and alternatives to frozen foundation encoders. |
| dynamic-jepa-collapse-limit | limitation | `(all:JEPA OR all:"joint embedding") AND (all:collapse OR all:stability OR all:regularization) AND (all:dynamics OR all:video)` | Find collapse, stability, and geometry critiques relevant to LeWM's core training claim. |
| dynamic-latent-planning-mpc | planning | `all:"latent world model" AND (all:planning OR all:MPC OR all:"cross entropy method") AND (all:pixel OR all:visual)` | Map the planning mechanism and comparable latent-space planners. |
| dynamic-latent-rollout-error | limitation | `all:"latent dynamics" AND (all:"error accumulation" OR all:"multi-step" OR all:"long horizon") AND (all:planning OR all:control)` | Recover evidence on autoregressive rollout drift and multi-step alternatives. |
| dynamic-latent-cost-alignment | evaluation | `all:"latent distance" AND (all:goal OR all:cost) AND (all:planning OR all:control)` | Test when distance in a learned latent space is aligned with task progress and control utility. |
| dynamic-action-fidelity-jepa | evaluation | `(all:JEPA OR all:"predictive embedding") AND all:action AND (all:fidelity OR all:counterfactual OR all:control)` | Cover action sensitivity, counterfactual futures, and decision utility rather than visual prediction alone. |
| dynamic-dino-wm-pldm | named-baseline | `all:"DINO-WM" OR all:"planning with latent dynamics models" OR all:PLDM` | Recover LeWM's frozen-backbone and prior end-to-end planning baselines. |
| dynamic-vjepa-robot-planning | adjacent | `(all:"V-JEPA 2" OR all:"V-JEPA") AND (all:robot OR all:planning OR all:control)` | Provide the video-JEPA predecessor and its action-conditioned robotics bridge. |
| dynamic-latent-world-model-efficiency | deployment | `all:"latent world model" AND (all:efficient OR all:lightweight OR all:"real-time") AND (all:planning OR all:control)` | Audit LeWM's efficiency and deployment-relevance claims under comparable planning budgets. |
| calibrated-leworldmodel | calibrated-term | `all:LeWorldModel` | Canonical focal method name. |
| calibrated-lewm | calibrated-term | `all:LeWM` | Canonical abbreviation used by the focal paper and follow-ups. |
| calibrated-fast-lewm | calibrated-term | `all:"Fast-LeWM"` | Direct LeWM variant addressing autoregressive rollout cost and accumulated latent error. |
| calibrated-action-prefix-prediction | calibrated-term | `all:"action-prefix prediction"` | Mechanism name used by Fast-LeWM. |
| calibrated-gc-idm | calibrated-term | `all:"GC-IDM"` | Goal-conditioned inverse-dynamics controller used to amortize planning over a pretrained LeWM. |
| calibrated-sigreg | calibrated-term | `all:SIGReg` | Sketched Isotropic Gaussian Regularization is the anti-collapse mechanism central to LeJEPA and LeWM. |
| calibration-lewm-family | calibrated-query | `all:"LeWorldModel" OR all:"LeWM" OR all:"Fast-LeWM"` | Exact family-name recovery. |
| calibration-lewm-planning | calibrated-query | `all:"LeWorldModel" AND (all:"GC-IDM" OR all:"inverse dynamics" OR all:"action-prefix")` | Recover direct planning and rollout extensions. |
| calibration-sigreg | calibrated-query | `all:"SIGReg" OR all:"Sketched Isotropic Gaussian Regularization"` | Recover the inherited representation-regularization mechanism and critiques. |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
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
| direct-topic | 3 | dynamic-lewm-exact, dynamic-fast-lewm, dynamic-lewm-amortized-planning, dynamic-dino-wm-pldm, world-model-robot, ea-model-vla, ea-model-named-foundation, ea-eval-closed-loop |
| adjacent-and-transfer | 3 | dynamic-lejepa-sigreg, dynamic-end-to-end-jepa-world-model, dynamic-latent-planning-mpc, dynamic-latent-cost-alignment, dynamic-action-fidelity-jepa, dynamic-vjepa-robot-planning, dynamic-latent-world-model-efficiency, calibrated-leworldmodel, calibrated-lewm, calibrated-fast-lewm, calibrated-action-prefix-prediction, calibrated-gc-idm, calibrated-sigreg, calibration-lewm-family, calibration-lewm-planning, calibration-sigreg, world-model-video-prediction, world-model-planning, ea-model-finetuning, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| limits-and-counterevidence | 3 | dynamic-jepa-collapse-limit, dynamic-latent-rollout-error, world-model-contact, world-model-long-horizon |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-lewm-browser | `site:arxiv.org/abs ("LeWorldModel" OR "Fast-LeWM" OR "Latent Geometry Beyond Search")` | Exact-family fallback if arXiv API tokenization under-recovers the LeWM name. |
| dynamic-lewm-limit-browser | `site:arxiv.org/abs LeWorldModel (limitation OR collapse OR rollout OR planning)` | Discover direct critiques, evaluations, and extensions of the focal model. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-lewm-calibration | llm | `"LeWorldModel" JEPA SIGReg latent planning` | Confirm exact method, mechanism, and follow-up terminology. |
| web-calibrated-leworldmodel | arxiv | `"LeWorldModel" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: LeWorldModel. |
| web-calibrated-lewm | arxiv | `"LeWM" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: LeWM. |
| web-calibrated-fast-lewm | arxiv | `"Fast-LeWM" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: Fast-LeWM. |
| web-calibrated-action-prefix-prediction | arxiv | `"action-prefix prediction" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: action-prefix prediction. |
| web-calibrated-gc-idm | arxiv | `"GC-IDM" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: GC-IDM. |
| web-calibrated-sigreg | arxiv | `"SIGReg" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: SIGReg. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-lewm-exact | arxiv_api | llm | high | `all:"LeWorldModel" OR all:"LeWM"` | Recover the focal paper, direct variants, follow-ups, and papers that evaluate or reuse LeWM. |
| dynamic-fast-lewm | arxiv_api | llm | high | `all:"Fast LeWorldModel" OR all:"Fast-LeWM"` | Capture the direct multi-horizon/prefix-prediction response to LeWM rollout cost and error accumulation. |
| dynamic-lewm-amortized-planning | arxiv_api | llm | high | `all:"Latent Geometry Beyond Search" OR (all:"LeWorldModel" AND all:"inverse dynamics")` | Capture learned inverse-dynamics planning that replaces online search in a pretrained LeWM latent space. |
| dynamic-lejepa-sigreg | arxiv_api | llm | high | `all:"LeJEPA" OR all:"Sketched Isotropic Gaussian Regularization" OR all:"SIGReg"` | Recover the anti-collapse theory and regularizer inherited by LeWM. |
| dynamic-end-to-end-jepa-world-model | arxiv_api | llm | high | `(all:JEPA OR all:"joint embedding predictive") AND all:"world model" AND (all:"end-to-end" OR all:pixels)` | Find end-to-end predictive-embedding world models and alternatives to frozen foundation encoders. |
| dynamic-jepa-collapse-limit | arxiv_api | llm | high | `(all:JEPA OR all:"joint embedding") AND (all:collapse OR all:stability OR all:regularization) AND (all:dynamics OR all:video)` | Find collapse, stability, and geometry critiques relevant to LeWM's core training claim. |
| dynamic-latent-planning-mpc | arxiv_api | llm | high | `all:"latent world model" AND (all:planning OR all:MPC OR all:"cross entropy method") AND (all:pixel OR all:visual)` | Map the planning mechanism and comparable latent-space planners. |
| dynamic-latent-rollout-error | arxiv_api | llm | high | `all:"latent dynamics" AND (all:"error accumulation" OR all:"multi-step" OR all:"long horizon") AND (all:planning OR all:control)` | Recover evidence on autoregressive rollout drift and multi-step alternatives. |
| dynamic-latent-cost-alignment | arxiv_api | llm | medium | `all:"latent distance" AND (all:goal OR all:cost) AND (all:planning OR all:control)` | Test when distance in a learned latent space is aligned with task progress and control utility. |
| dynamic-action-fidelity-jepa | arxiv_api | llm | medium | `(all:JEPA OR all:"predictive embedding") AND all:action AND (all:fidelity OR all:counterfactual OR all:control)` | Cover action sensitivity, counterfactual futures, and decision utility rather than visual prediction alone. |
| dynamic-dino-wm-pldm | arxiv_api | llm | high | `all:"DINO-WM" OR all:"planning with latent dynamics models" OR all:PLDM` | Recover LeWM's frozen-backbone and prior end-to-end planning baselines. |
| dynamic-vjepa-robot-planning | arxiv_api | llm | high | `(all:"V-JEPA 2" OR all:"V-JEPA") AND (all:robot OR all:planning OR all:control)` | Provide the video-JEPA predecessor and its action-conditioned robotics bridge. |
| dynamic-latent-world-model-efficiency | arxiv_api | llm | medium | `all:"latent world model" AND (all:efficient OR all:lightweight OR all:"real-time") AND (all:planning OR all:control)` | Audit LeWM's efficiency and deployment-relevance claims under comparable planning budgets. |
| dynamic-lewm-browser | browser_fallback | llm | high | `site:arxiv.org/abs ("LeWorldModel" OR "Fast-LeWM" OR "Latent Geometry Beyond Search")` | Exact-family fallback if arXiv API tokenization under-recovers the LeWM name. |
| dynamic-lewm-limit-browser | browser_fallback | llm | medium | `site:arxiv.org/abs LeWorldModel (limitation OR collapse OR rollout OR planning)` | Discover direct critiques, evaluations, and extensions of the focal model. |
| dynamic-lewm-calibration | web_calibration | llm | high | `"LeWorldModel" JEPA SIGReg latent planning` | Confirm exact method, mechanism, and follow-up terminology. |

## Calibration Notes

- arxiv calibration (high): Official arXiv record confirms LeWorldModel, LeWM, end-to-end JEPA, and the stable-from-pixels framing.
- arxiv calibration (high): Official arXiv record confirms Fast LeWorldModel / Fast-LeWM and action-prefix prediction.
- arxiv calibration (high): Official arXiv record confirms the direct LeWM planning follow-up and the Goal-Conditioned Inverse Dynamics Model (GC-IDM) term.
- arxiv calibration (high): Official arXiv record confirms LeJEPA and Sketched Isotropic Gaussian Regularization (SIGReg), the anti-collapse mechanism used by LeWM.

## Planner Notes

- llm dynamic expansion (high): The user narrowed the review to the LeWorldModel lineage. Static world-model taxonomy needs exact LeWM names, its anti-collapse mechanism, direct planning follow-ups, and negative/evaluation surfaces.
