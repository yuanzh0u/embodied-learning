# Query Plan: Jim Fan research trajectory: generalist agents, embodied AI, foundation models, and open-world learning

## Scope

- Knowledge IDs: EA-MODEL, EA-EVAL, EA-DATA
- Families: vla, world-model, sim2real, droid-ego4d
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 200
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-author-linxi-fan | core | `au:"Linxi Fan"` | Primary arXiv author spelling established by the author's homepage and paper records. |
| dynamic-author-jim-fan | identity-variant | `all:"Jim Fan" AND (all:agent OR all:robot OR all:reinforcement)` | Checks the public name variant while constraining same-name noise. |
| dynamic-early-scale-lineage | named-method | `all:("Deep Speech 2" OR "Ladder Network" OR "World of Bits" OR SURREAL OR SECANT)` | Covers the early sequence from large-scale learning systems to visual-agent generalization. |
| dynamic-generalist-control-lineage | named-method | `all:(MetaMorph OR MineDojo OR VIMA) AND (all:agent OR all:robot OR all:control)` | Covers morphology-general control, open-ended environments, and multimodal robot prompting. |
| dynamic-llm-agent-lineage | named-method | `all:(Voyager OR Eureka OR DrEureka) AND (all:agent OR all:robot OR all:reward)` | Covers LLM-written skills, curricula, rewards, and sim-to-real transfer. |
| dynamic-physical-ai-lineage | named-method | `all:(GR00T OR DreamGen OR DexUMI OR HumanoidMimicGen OR "Sim-and-Real Co-Training" OR "CaP-X")` | Covers later physical-AI, humanoid, data-generation, and code-as-policy work associated with Linxi Fan. |
| dynamic-open-ended-agents-mechanism | mechanism | `all:"open-ended" AND all:(embodied OR agent) AND all:(knowledge OR lifelong OR curriculum)` | Captures the mechanism surface linking MineDojo and Voyager rather than only their names. |
| dynamic-foundation-policy-mechanism | mechanism | `all:("foundation model" OR multimodal OR language) AND all:(robot OR embodied) AND all:(policy OR action OR control)` | Captures the transition from multimodal prompting to action-producing foundation policies. |
| dynamic-video-world-model-robot | mechanism | `all:"video world model" AND all:(robot OR manipulation OR humanoid) AND all:(policy OR data OR control)` | Covers the later use of generative video/world models for robot data and policy learning. |
| dynamic-external-minecraft-evaluation | evaluation | `all:(Minecraft OR MineDojo OR Voyager) AND all:(benchmark OR evaluation OR generalization OR ablation)` | Finds independent or comparative evaluation of open-world agent claims. |
| dynamic-external-robot-prompt-evaluation | evaluation | `all:(VIMA OR "multimodal prompt" OR "code as policy") AND all:robot AND all:(benchmark OR evaluation OR limitation)` | Finds comparison and boundary evidence for prompted robot agents. |
| dynamic-external-reward-code-limit | limitation | `all:("language model" OR LLM) AND all:(reward OR code) AND all:(robot OR embodied) AND all:(failure OR limitation OR robustness OR safety)` | Targets counter-evidence and transfer limits for LLM-generated rewards or control code. |
| dynamic-humanoid-foundation-evaluation | evaluation | `all:(humanoid OR "generalist robot") AND all:(foundation OR pretraining) AND all:(benchmark OR real-world OR evaluation OR generalization)` | Finds evidence needed to evaluate later physical-AI scaling claims outside project announcements. |
| dynamic-physical-ai-deployment | deployment | `all:(humanoid OR "robot foundation model") AND all:(deployment OR reliability OR recovery OR latency OR safety)` | Prevents engineering demos and industrial readiness from being conflated. |
| calibrated-linxi-fan | calibrated-term | `all:"Linxi Fan"` | Primary publication author spelling. |
| calibrated-linxi-jim-fan | calibrated-term | `all:"Linxi "Jim" Fan"` | Self-declared full public name variant. |
| calibrated-generally-capable-agents | calibrated-term | `all:"generally capable agents"` | Self-described mission spanning physical and virtual worlds; framing context, not a scientific result. |
| calibrated-training-and-deploying-visual-agents-at-scale | calibrated-term | `all:"Training and Deploying Visual Agents at Scale"` | Dissertation title provides a stable bridge between earlier systems/scaling work and later generalist-agent work. |
| calibrated-minedojo | calibrated-term | `all:MineDojo` | Officially linked project name. |
| calibration-thesis-lineage | calibrated-query | `all:"Training and Deploying Visual Agents at Scale" OR (au:"Linxi Fan" AND all:"visual agent")` | Finds the thesis record or linked research lineage. |
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
| sim2real-core | core | `(all:sim2real OR all:"sim-to-real") AND all:robot` | Find the main simulation-to-real transfer literature surface. |
| sim2real-real-validation | validation | `all:"real robot" AND all:validation AND all:simulation` | Find papers that verify simulation claims against real robot runs. |
| sim2real-synthetic-data | data-generation | `all:"synthetic data" AND all:"robot manipulation"` | Capture synthetic-data pipelines used to reduce real collection cost. |
| sim2real-domain-randomization | method | `all:"domain randomization" AND all:"robot manipulation"` | Find robustification methods for visual and physical sim-to-real gaps. |
| sim2real-correlation | evaluation | `all:"sim-real" AND all:correlation AND all:evaluation` | Surface work that measures whether simulation rankings predict real performance. |
| droid-robot-manipulation | named-dataset | `all:DROID AND all:"robot manipulation"` | Find DROID robot data papers and reuse discussions. |
| ego4d-robot-learning | named-dataset | `all:Ego4D AND all:"robot learning"` | Catch robot-learning papers that draw on egocentric human video data. |
| droid-ego-egocentric-video | adjacent-data | `all:"egocentric video" AND all:"robot learning"` | Find human-observation data papers near Ego4D even when the dataset is not named. |
| droid-ego-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot demonstration"` | Capture natural-environment data collection and scaling constraints. |
| droid-ego-data-mixture | data-mixture | `all:"data mixture" AND all:"robot learning"` | Find cross-dataset mixture papers that discuss data compatibility and noise. |
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
| direct-topic | 3 | dynamic-author-linxi-fan, dynamic-early-scale-lineage, dynamic-generalist-control-lineage, dynamic-llm-agent-lineage, dynamic-physical-ai-lineage, vla-core, vla-named-models, world-model-robot, sim2real-core, droid-robot-manipulation, ego4d-robot-learning, ea-model-named-foundation, ea-eval-closed-loop |
| adjacent-and-transfer | 3 | dynamic-author-jim-fan, dynamic-open-ended-agents-mechanism, dynamic-foundation-policy-mechanism, dynamic-video-world-model-robot, dynamic-external-minecraft-evaluation, dynamic-external-robot-prompt-evaluation, dynamic-humanoid-foundation-evaluation, dynamic-physical-ai-deployment, calibrated-linxi-fan, calibrated-linxi-jim-fan, calibrated-generally-capable-agents, calibrated-training-and-deploying-visual-agents-at-scale, calibrated-minedojo, calibration-thesis-lineage, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, world-model-video-prediction, world-model-planning, sim2real-synthetic-data, sim2real-correlation, droid-ego-egocentric-video, droid-ego-in-the-wild, droid-ego-data-mixture, ea-model-finetuning, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| limits-and-counterevidence | 3 | dynamic-external-reward-code-limit, vla-negative-transfer, world-model-contact, world-model-long-horizon |
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
| dynamic-author-browser | `site:arxiv.org/abs "Linxi Fan"` | Recover author papers if the arXiv API under-recovers. |
| dynamic-project-browser | `site:arxiv.org/abs (MineDojo OR VIMA OR Voyager OR Eureka OR DrEureka OR GR00T OR DreamGen) robot agent` | Recover named-project records and follow-ups. |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-official-identity | llm | `Jim Fan official NVIDIA homepage publications` | Confirm identity, public name variants, and official project vocabulary. |
| dynamic-current-projects | llm | `site:research.nvidia.com "Linxi Fan" robotics agent` | Calibrate current NVIDIA project and lab vocabulary without accepting claims from snippets. |
| web-calibrated-linxi-fan | author-homepage | `"Linxi Fan" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: Linxi Fan. |
| web-calibrated-linxi-jim-fan | author-homepage | `"Linxi "Jim" Fan" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: Linxi "Jim" Fan. |
| web-calibrated-generally-capable-agents | author-homepage | `"generally capable agents" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: generally capable agents. |
| web-calibrated-training-and-deploying-visual-agents-at-scale | stanford-thesis-record | `"Training and Deploying Visual Agents at Scale" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: Training and Deploying Visual Agents at Scale. |
| web-calibrated-minedojo | official-nvidia-lab-page | `"MineDojo" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: MineDojo. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-author-linxi-fan | arxiv_api | llm | high | `au:"Linxi Fan"` | Primary arXiv author spelling established by the author's homepage and paper records. |
| dynamic-author-jim-fan | arxiv_api | llm | medium | `all:"Jim Fan" AND (all:agent OR all:robot OR all:reinforcement)` | Checks the public name variant while constraining same-name noise. |
| dynamic-early-scale-lineage | arxiv_api | llm | high | `all:("Deep Speech 2" OR "Ladder Network" OR "World of Bits" OR SURREAL OR SECANT)` | Covers the early sequence from large-scale learning systems to visual-agent generalization. |
| dynamic-generalist-control-lineage | arxiv_api | llm | high | `all:(MetaMorph OR MineDojo OR VIMA) AND (all:agent OR all:robot OR all:control)` | Covers morphology-general control, open-ended environments, and multimodal robot prompting. |
| dynamic-llm-agent-lineage | arxiv_api | llm | high | `all:(Voyager OR Eureka OR DrEureka) AND (all:agent OR all:robot OR all:reward)` | Covers LLM-written skills, curricula, rewards, and sim-to-real transfer. |
| dynamic-physical-ai-lineage | arxiv_api | llm | medium | `all:(GR00T OR DreamGen OR DexUMI OR HumanoidMimicGen OR "Sim-and-Real Co-Training" OR "CaP-X")` | Covers later physical-AI, humanoid, data-generation, and code-as-policy work associated with Linxi Fan. |
| dynamic-open-ended-agents-mechanism | arxiv_api | llm | medium | `all:"open-ended" AND all:(embodied OR agent) AND all:(knowledge OR lifelong OR curriculum)` | Captures the mechanism surface linking MineDojo and Voyager rather than only their names. |
| dynamic-foundation-policy-mechanism | arxiv_api | llm | medium | `all:("foundation model" OR multimodal OR language) AND all:(robot OR embodied) AND all:(policy OR action OR control)` | Captures the transition from multimodal prompting to action-producing foundation policies. |
| dynamic-video-world-model-robot | arxiv_api | llm | medium | `all:"video world model" AND all:(robot OR manipulation OR humanoid) AND all:(policy OR data OR control)` | Covers the later use of generative video/world models for robot data and policy learning. |
| dynamic-external-minecraft-evaluation | arxiv_api | llm | medium | `all:(Minecraft OR MineDojo OR Voyager) AND all:(benchmark OR evaluation OR generalization OR ablation)` | Finds independent or comparative evaluation of open-world agent claims. |
| dynamic-external-robot-prompt-evaluation | arxiv_api | llm | medium | `all:(VIMA OR "multimodal prompt" OR "code as policy") AND all:robot AND all:(benchmark OR evaluation OR limitation)` | Finds comparison and boundary evidence for prompted robot agents. |
| dynamic-external-reward-code-limit | arxiv_api | llm | medium | `all:("language model" OR LLM) AND all:(reward OR code) AND all:(robot OR embodied) AND all:(failure OR limitation OR robustness OR safety)` | Targets counter-evidence and transfer limits for LLM-generated rewards or control code. |
| dynamic-humanoid-foundation-evaluation | arxiv_api | llm | medium | `all:(humanoid OR "generalist robot") AND all:(foundation OR pretraining) AND all:(benchmark OR real-world OR evaluation OR generalization)` | Finds evidence needed to evaluate later physical-AI scaling claims outside project announcements. |
| dynamic-physical-ai-deployment | arxiv_api | llm | medium | `all:(humanoid OR "robot foundation model") AND all:(deployment OR reliability OR recovery OR latency OR safety)` | Prevents engineering demos and industrial readiness from being conflated. |
| dynamic-author-browser | browser_fallback | llm | high | `site:arxiv.org/abs "Linxi Fan"` | Recover author papers if the arXiv API under-recovers. |
| dynamic-project-browser | browser_fallback | llm | medium | `site:arxiv.org/abs (MineDojo OR VIMA OR Voyager OR Eureka OR DrEureka OR GR00T OR DreamGen) robot agent` | Recover named-project records and follow-ups. |
| dynamic-official-identity | web_calibration | llm | high | `Jim Fan official NVIDIA homepage publications` | Confirm identity, public name variants, and official project vocabulary. |
| dynamic-current-projects | web_calibration | llm | medium | `site:research.nvidia.com "Linxi Fan" robotics agent` | Calibrate current NVIDIA project and lab vocabulary without accepting claims from snippets. |

## Calibration Notes

- author-homepage calibration (high): Self-authored identity and research framing; accessed 2026-07-21. Uses Linxi "Jim" Fan and highlights VIMA, MineDojo, Voyager, and Eureka. The publication list appears stale after 2022, so it is not treated as comprehensive.
- official-nvidia-lab-page calibration (high): Official NVIDIA page confirms Jim Fan, NVIDIA, and Robotics interest; accessed 2026-07-21. It does not state a current job title.
- official-nvidia-lab-page calibration (high): Official NVIDIA Seattle Robotics Lab page links Jim Fan to MineDojo; accessed 2026-07-21.
- stanford-thesis-record calibration (high): Institutional record for Linxi Fan's dissertation, Training and Deploying Visual Agents at Scale.

## Planner Notes

- llm dynamic expansion (high): Person-centred review requires author-identity, named-project, lineage, limitation, evaluation, and adjacent follow-up queries beyond the static embodied-AI taxonomy.
