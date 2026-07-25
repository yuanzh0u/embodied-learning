# Query Plan: 近半年VLA在具身领域最大的技术突破

## Scope

- Knowledge IDs: EA-MODEL, EA-EVAL
- Families: vla
- Suggested categories: cs.AI, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 100
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-vla-world-model-planning | dynamic-association | `(all:"vision language action" OR all:VLA) AND (all:"world model" OR all:"world action model") AND (all:planning OR all:foresight OR all:rollout)` | 捕捉从直接动作预测转向动作条件后果预演的核心路线。 |
| dynamic-structured-hierarchical-vla | dynamic-association | `(all:VLA OR all:"robot policy") AND (all:structured OR all:hierarchical OR all:symbolic) AND (all:planning OR all:"world model")` | 检索结构化里程碑、分层世界模型与长时程任务—运动规划。 |
| dynamic-geometry-dynamics-vla | dynamic-association | `(all:VLA OR all:"world action model") AND (all:4D OR all:geometry OR all:pointmap OR all:"point track") AND (all:robot OR all:manipulation)` | 检索用 4D/几何动态给 VLA 提供可执行物理表征的路线。 |
| dynamic-vla-correction-recovery | dynamic-association | `(all:VLA OR all:"world action model") AND (all:recovery OR all:correction OR all:"self-correct" OR all:failure)` | 检索失败检测、接触纠错、自我恢复和后训练。 |
| dynamic-vla-world-model-limits | dynamic-association | `(all:VLA OR all:"world action model") AND (all:failure OR all:drift OR all:attack OR all:admissibility OR all:benchmark)` | 主动检索世界模型路线的失效、攻击、可采信性与闭环评测反证。 |
| calibrated-structured-planner | calibrated-term | `all:"structured planner"` | 将稠密视频预测压缩为动力学相关的稀疏里程碑。 |
| calibrated-kinematic-grounding | calibrated-term | `all:"kinematic grounding"` | 区分视觉可能未来与可执行运动计划。 |
| calibrated-hierarchical-world-model | calibrated-term | `all:"hierarchical world model"` | 连接高层逻辑转移与低层视觉动态。 |
| calibration-structured-planner | calibrated-query | `all:"structured planner" AND (all:robot OR all:VLA)` | 定向回收结构化世界模型规划工作。 |
| calibration-hierarchical-world-model | calibrated-query | `all:"hierarchical world model" AND all:robot` | 定向回收分层世界模型。 |
| vla-core | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that directly model robot actions from vision and language. |
| vla-named-models | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"` | Catch named robot foundation model families and comparative work. |
| vla-open-x-embodiment | data-source | `(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot` | Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids. |
| vla-large-scale-robot-data | data-scaling | `all:"large-scale" AND all:"robot data"` | Surface scaling and dataset-layer discussions for robot foundation models. |
| vla-robot-foundation-action | foundation-model | `all:"robot foundation model" AND all:action` | Find broader foundation-model papers whose metadata may not use VLA. |
| vla-finetuning-policy | transfer | `all:"fine-tuning" AND all:"robot policy"` | Surface evidence about target-task adaptation and data requirements. |
| vla-data-mixture | data-mixture | `all:"data mixture" AND all:"robot foundation model"` | Find mixture and dataset composition papers that explain scaling behavior. |
| vla-negative-transfer | limitation | `all:"negative transfer" AND all:robot AND all:policy` | Search for failure cases where broad pretraining hurts target deployment. |
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
| adjacent-and-transfer | 3 | dynamic-vla-world-model-planning, dynamic-structured-hierarchical-vla, dynamic-geometry-dynamics-vla, dynamic-vla-correction-recovery, dynamic-vla-world-model-limits, calibrated-structured-planner, calibrated-kinematic-grounding, calibrated-hierarchical-world-model, calibration-structured-planner, calibration-hierarchical-world-model, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, ea-model-finetuning, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| direct-topic | 3 | vla-core, vla-named-models, ea-model-named-foundation, ea-eval-closed-loop |
| limits-and-counterevidence | 3 | vla-negative-transfer |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-vla-breakthrough-browser | `site:arxiv.org VLA world model structured planning robot manipulation 2026` | 官方 API 漏检时补充新方法名称。 |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-vla-breakthrough-web | llm | `site:arxiv.org/abs/2607 VLA robot world model planning` | 校准 2026 年 7 月最新术语。 |
| web-calibrated-structured-planner | arxiv-web | `"structured planner" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: structured planner. |
| web-calibrated-kinematic-grounding | arxiv-web | `"kinematic grounding" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: kinematic grounding. |
| web-calibrated-hierarchical-world-model | arxiv-web | `"hierarchical world model" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: hierarchical world model. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-vla-world-model-planning | arxiv_api | llm | high | `(all:"vision language action" OR all:VLA) AND (all:"world model" OR all:"world action model") AND (all:planning OR all:foresight OR all:rollout)` | 捕捉从直接动作预测转向动作条件后果预演的核心路线。 |
| dynamic-structured-hierarchical-vla | arxiv_api | llm | high | `(all:VLA OR all:"robot policy") AND (all:structured OR all:hierarchical OR all:symbolic) AND (all:planning OR all:"world model")` | 检索结构化里程碑、分层世界模型与长时程任务—运动规划。 |
| dynamic-geometry-dynamics-vla | arxiv_api | llm | high | `(all:VLA OR all:"world action model") AND (all:4D OR all:geometry OR all:pointmap OR all:"point track") AND (all:robot OR all:manipulation)` | 检索用 4D/几何动态给 VLA 提供可执行物理表征的路线。 |
| dynamic-vla-correction-recovery | arxiv_api | llm | high | `(all:VLA OR all:"world action model") AND (all:recovery OR all:correction OR all:"self-correct" OR all:failure)` | 检索失败检测、接触纠错、自我恢复和后训练。 |
| dynamic-vla-world-model-limits | arxiv_api | llm | high | `(all:VLA OR all:"world action model") AND (all:failure OR all:drift OR all:attack OR all:admissibility OR all:benchmark)` | 主动检索世界模型路线的失效、攻击、可采信性与闭环评测反证。 |
| dynamic-vla-breakthrough-browser | browser_fallback | llm | medium | `site:arxiv.org VLA world model structured planning robot manipulation 2026` | 官方 API 漏检时补充新方法名称。 |
| dynamic-vla-breakthrough-web | web_calibration | llm | medium | `site:arxiv.org/abs/2607 VLA robot world model planning` | 校准 2026 年 7 月最新术语。 |

## Calibration Notes

- arxiv-web calibration (high): StructVLA 使用 structured planner / structured frames / kinematic grounding 描述稀疏可执行预见。
- arxiv-web calibration (high): H-WM 使用 hierarchical world model / logical and visual state transitions 描述分层长时程规划。

## Planner Notes

- llm dynamic expansion (high): ‘最大技术突破’需要比较反应式 VLA、分层规划、世界模型后果预演、4D/几何动态、触觉纠错与闭环评测路线，并为每条路线检索反证。
