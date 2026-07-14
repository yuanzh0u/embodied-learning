# Query Plan: 世界模型需要什么样的训练数据

## Scope

- Knowledge IDs: EA-DATA, EA-MODEL, EA-EVAL
- Families: world-model, sim2real
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 120
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-world-model-admissibility | evaluation | `all:"world model" AND (all:admissibility OR all:trustworthiness OR all:reliability) AND all:robot` | 覆盖世界模型能否承担策略评估的可采信性。 |
| dynamic-world-model-action-fidelity | evaluation | `all:"world model" AND (all:"action fidelity" OR all:"action following" OR all:"action-conditioned reliability") AND all:robot` | 覆盖动作响应而非仅视觉逼真。 |
| dynamic-world-model-policy-evaluation | evaluation | `all:"world model" AND all:"policy evaluation" AND all:robot` | 覆盖世界模型作为策略评测器。 |
| dynamic-physically-viable-world-model | limitation | `all:"world model" AND (all:"physical viability" OR all:"physics adherence" OR all:"physically viable") AND all:robot` | 覆盖物理约束与失败乐观偏差。 |
| dynamic-action-conditioned-training-data | quality | `all:"world model" AND all:"action-conditioned" AND (all:data OR all:dataset) AND all:robot` | 覆盖动作干预后的状态变化数据。 |
| dynamic-contact-world-model-data | quality | `all:"world model" AND (all:contact OR all:tactile OR all:force) AND all:"robot manipulation"` | 覆盖接触与不可观测物理状态。 |
| dynamic-failure-recovery-rollouts | limitation | `all:"world model" AND (all:failure OR all:recovery OR all:intervention) AND all:robot` | 覆盖失败、纠错和恢复轨迹。 |
| dynamic-key-event-world-model | quality | `all:"world model" AND (all:keyframe OR all:"key event" OR all:sparse) AND all:robot` | 覆盖关键事件保留与高效时序采样。 |
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
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
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
| adjacent-and-transfer | 3 | dynamic-world-model-admissibility, dynamic-world-model-action-fidelity, dynamic-world-model-policy-evaluation, world-model-video-prediction, world-model-planning, sim2real-synthetic-data, sim2real-correlation, ea-data-in-the-wild, ea-data-dataset-curation, ea-model-finetuning, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| limits-and-counterevidence | 3 | dynamic-physically-viable-world-model, dynamic-failure-recovery-rollouts, world-model-contact, world-model-long-horizon |
| direct-topic | 3 | dynamic-action-conditioned-training-data, dynamic-contact-world-model-data, dynamic-key-event-world-model, world-model-robot, sim2real-core, ea-data-robot-demonstrations, ea-data-demonstration-quality, ea-model-vla, ea-model-named-foundation, ea-eval-closed-loop |
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
| browser-sim2real-core | `site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot` | Find sim-to-real papers through web/arXiv pages when API search under-recovers variants. |
| browser-sim2real-synthetic-validation | `site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation` | Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots. |
| browser-sim2real-eval-gap | `site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot` | Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-topic-calibration | web | `"世界模型需要什么样的训练数据" "robot" "arXiv"` | Find paper-facing terminology for the requested topic. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-world-model-admissibility | arxiv_api | llm | medium | `all:"world model" AND (all:admissibility OR all:trustworthiness OR all:reliability) AND all:robot` | 覆盖世界模型能否承担策略评估的可采信性。 |
| dynamic-world-model-action-fidelity | arxiv_api | llm | medium | `all:"world model" AND (all:"action fidelity" OR all:"action following" OR all:"action-conditioned reliability") AND all:robot` | 覆盖动作响应而非仅视觉逼真。 |
| dynamic-world-model-policy-evaluation | arxiv_api | llm | medium | `all:"world model" AND all:"policy evaluation" AND all:robot` | 覆盖世界模型作为策略评测器。 |
| dynamic-physically-viable-world-model | arxiv_api | llm | medium | `all:"world model" AND (all:"physical viability" OR all:"physics adherence" OR all:"physically viable") AND all:robot` | 覆盖物理约束与失败乐观偏差。 |
| dynamic-action-conditioned-training-data | arxiv_api | llm | medium | `all:"world model" AND all:"action-conditioned" AND (all:data OR all:dataset) AND all:robot` | 覆盖动作干预后的状态变化数据。 |
| dynamic-contact-world-model-data | arxiv_api | llm | medium | `all:"world model" AND (all:contact OR all:tactile OR all:force) AND all:"robot manipulation"` | 覆盖接触与不可观测物理状态。 |
| dynamic-failure-recovery-rollouts | arxiv_api | llm | medium | `all:"world model" AND (all:failure OR all:recovery OR all:intervention) AND all:robot` | 覆盖失败、纠错和恢复轨迹。 |
| dynamic-key-event-world-model | arxiv_api | llm | medium | `all:"world model" AND (all:keyframe OR all:"key event" OR all:sparse) AND all:robot` | 覆盖关键事件保留与高效时序采样。 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (medium): 同时覆盖世界模型的训练数据、动作忠实、可采信性和策略评估用途。
