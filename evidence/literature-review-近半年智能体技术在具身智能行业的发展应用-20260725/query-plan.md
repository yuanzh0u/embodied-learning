# Query Plan: 近半年智能体技术在具身智能行业的发展应用

## Scope

- Knowledge IDs: EA-MODEL, EA-BIZ, EA-EVAL
- Families: vla, world-model, industrial-deployment
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 160
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-agentic-robot-control | core | `all:"agentic AI" AND (all:robot OR all:robotics)` | 直接覆盖以智能体为上层控制器的机器人系统。 |
| dynamic-embodied-reasoning-tool-use | mechanism | `all:"embodied reasoning" AND (all:"tool use" OR all:"tool calling" OR all:planning)` | 覆盖高层推理、工具调用和技能选择。 |
| dynamic-robot-skill-graph-agent-os | mechanism | `(all:"skill graph" OR all:"agent OS" OR all:orchestration) AND (all:robot OR all:embodied)` | 覆盖技能图、运行时编排和资源调度。 |
| dynamic-embodied-agent-memory | mechanism | `all:"embodied agent" AND (all:"episodic memory" OR all:"spatial memory" OR all:"working memory")` | 覆盖长时任务中的经历记忆、空间记忆和工作记忆。 |
| dynamic-success-detection-replanning | evaluation | `(all:"success detection" OR all:"failure detection") AND (all:robot OR all:embodied) AND (all:replanning OR all:retry)` | 智能体闭环的关键不是计划生成，而是执行后判定、重试和重规划。 |
| dynamic-multi-agent-robot-collaboration | adjacent | `(all:"multi-agent" OR all:"multi-robot") AND (all:"embodied intelligence" OR all:"robot manipulation") AND all:collaboration` | 覆盖多个物理智能体的协作、分工和无显式通信协调。 |
| dynamic-agentic-robot-fragility | limitation | `(all:agentic OR all:"LLM agent") AND all:robot AND (all:fragile OR all:hallucination OR all:failure OR all:safety)` | 主动寻找幻觉、误判成功、脆弱性和安全限制。 |
| dynamic-agentic-industrial-deployment | deployment | `(all:agentic OR all:"physical agent") AND all:robot AND (all:industrial OR all:warehouse OR all:manufacturing) AND (all:deployment OR all:production)` | 覆盖工厂、仓储和制造业中的智能体化机器人部署。 |
| calibrated-agentic-robot-control | calibrated-term | `all:"agentic robot control"` | 直接描述智能体控制机器人。 |
| calibrated-embodied-agentos | calibrated-term | `all:"Embodied AgentOS"` | 描述将任务转为技能图并闭环监控的运行时。 |
| calibrated-3d-spatial-memory | calibrated-term | `all:"3D spatial memory"` | 支撑跨时段空间一致性与任务恢复。 |
| calibrated-success-detection | calibrated-term | `all:"success detection"` | 产业高层模型把成功判定作为重试/推进门控。 |
| calibrated-semantic-reasoning | calibrated-term | `all:"semantic reasoning"` | 产业系统将长时任务语义推理与低层动作分层。 |
| calibration-agentic-robot-control | calibrated-query | `all:"agentic robot control" OR (all:agentic AND all:robot AND all:control)` | 复现直接词与宽松组合。 |
| calibration-embodied-agent-os | calibrated-query | `all:"Embodied AgentOS" OR (all:"embodied agent" AND all:"skill graph")` | 覆盖新出现的运行时/技能图架构。 |
| calibration-success-detection | calibrated-query | `all:"success detection" AND (all:robot OR all:embodied)` | 检验学术文献是否采用产业模型的同一术语。 |
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
| industrial-deployment-core | core | `all:"industrial robot" AND all:deployment` | Find deployment papers in manufacturing or production contexts. |
| industrial-deployment-reliability | reliability | `all:reliability AND all:robot AND all:deployment` | Capture uptime, fault tolerance, and long-run operational evidence. |
| industrial-deployment-cycle-time | production | `all:"cycle time" AND all:automation AND all:robot` | Find throughput constraints that affect ToB feasibility. |
| industrial-deployment-yield | production-quality | `all:yield AND all:robot AND all:manufacturing` | Surface quality and yield discussions beyond one-off success rate. |
| industrial-deployment-acceptance-testing | evaluation | `all:"acceptance testing" AND all:robot` | Find validation and acceptance language for production handoff. |
| industrial-deployment-roi | business-adjacent | `all:ROI AND all:robot AND all:automation` | Search for cost or return-on-investment framing when present in technical metadata. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |
| ea-biz-industrial-deployment | core | `all:"industrial deployment" AND all:robot` | Find papers that discuss moving robot systems beyond lab demonstrations. |
| ea-biz-reliability | deployment | `all:reliability AND all:"robot manipulation" AND all:deployment` | Capture reliability, uptime, and operational risk discussions. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-agentic-robot-control, vla-core, vla-named-models, world-model-robot, industrial-deployment-core, ea-model-named-foundation, ea-biz-industrial-deployment |
| adjacent-and-transfer | 3 | dynamic-embodied-reasoning-tool-use, dynamic-robot-skill-graph-agent-os, dynamic-embodied-agent-memory, dynamic-success-detection-replanning, dynamic-multi-agent-robot-collaboration, dynamic-agentic-industrial-deployment, calibrated-agentic-robot-control, calibrated-embodied-agentos, calibrated-3d-spatial-memory, calibrated-success-detection, calibrated-semantic-reasoning, calibration-agentic-robot-control, calibration-embodied-agent-os, calibration-success-detection, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, world-model-video-prediction, world-model-planning, industrial-deployment-acceptance-testing, ea-model-finetuning, ea-biz-reliability |
| limits-and-counterevidence | 3 | dynamic-agentic-robot-fragility, vla-negative-transfer, world-model-contact, world-model-long-horizon |
| deployment-and-operations | 3 | industrial-deployment-reliability, industrial-deployment-cycle-time, industrial-deployment-yield, industrial-deployment-roi |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-agentic-robotics-browser | `site:arxiv.org/abs 2026 (agentic OR embodied reasoning) robot planning memory` | API 欠召回时发现 agentic robotics 新论文。 |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-physical-agent-industry-web | llm | `2026 physical agent embodied reasoning robot deployment official` | 校准产业界对 physical agent 与 embodied reasoning 的实际用法。 |
| web-calibrated-agentic-robot-control | arxiv | `"agentic robot control" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: agentic robot control. |
| web-calibrated-embodied-agentos | arxiv | `"Embodied AgentOS" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: Embodied AgentOS. |
| web-calibrated-3d-spatial-memory | arxiv | `"3D spatial memory" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: 3D spatial memory. |
| web-calibrated-success-detection | project-page | `"success detection" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: success detection. |
| web-calibrated-semantic-reasoning | company-page | `"semantic reasoning" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: semantic reasoning. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-agentic-robot-control | arxiv_api | llm | high | `all:"agentic AI" AND (all:robot OR all:robotics)` | 直接覆盖以智能体为上层控制器的机器人系统。 |
| dynamic-embodied-reasoning-tool-use | arxiv_api | llm | high | `all:"embodied reasoning" AND (all:"tool use" OR all:"tool calling" OR all:planning)` | 覆盖高层推理、工具调用和技能选择。 |
| dynamic-robot-skill-graph-agent-os | arxiv_api | llm | medium | `(all:"skill graph" OR all:"agent OS" OR all:orchestration) AND (all:robot OR all:embodied)` | 覆盖技能图、运行时编排和资源调度。 |
| dynamic-embodied-agent-memory | arxiv_api | llm | high | `all:"embodied agent" AND (all:"episodic memory" OR all:"spatial memory" OR all:"working memory")` | 覆盖长时任务中的经历记忆、空间记忆和工作记忆。 |
| dynamic-success-detection-replanning | arxiv_api | llm | high | `(all:"success detection" OR all:"failure detection") AND (all:robot OR all:embodied) AND (all:replanning OR all:retry)` | 智能体闭环的关键不是计划生成，而是执行后判定、重试和重规划。 |
| dynamic-multi-agent-robot-collaboration | arxiv_api | llm | medium | `(all:"multi-agent" OR all:"multi-robot") AND (all:"embodied intelligence" OR all:"robot manipulation") AND all:collaboration` | 覆盖多个物理智能体的协作、分工和无显式通信协调。 |
| dynamic-agentic-robot-fragility | arxiv_api | llm | high | `(all:agentic OR all:"LLM agent") AND all:robot AND (all:fragile OR all:hallucination OR all:failure OR all:safety)` | 主动寻找幻觉、误判成功、脆弱性和安全限制。 |
| dynamic-agentic-industrial-deployment | arxiv_api | llm | high | `(all:agentic OR all:"physical agent") AND all:robot AND (all:industrial OR all:warehouse OR all:manufacturing) AND (all:deployment OR all:production)` | 覆盖工厂、仓储和制造业中的智能体化机器人部署。 |
| dynamic-agentic-robotics-browser | browser_fallback | llm | medium | `site:arxiv.org/abs 2026 (agentic OR embodied reasoning) robot planning memory` | API 欠召回时发现 agentic robotics 新论文。 |
| dynamic-physical-agent-industry-web | web_calibration | llm | medium | `2026 physical agent embodied reasoning robot deployment official` | 校准产业界对 physical agent 与 embodied reasoning 的实际用法。 |

## Calibration Notes

- arxiv calibration (high): 论文标题直接采用 Agentic AI for Robot Control。
- arxiv calibration (high): 论文采用 Embodied AgentOS、3D spatial memory 和 executable skill graphs。
- project-page calibration (medium): 产业模型采用 embodied reasoning、tool calling 与 success detection。
- company-page calibration (medium): 产业系统采用 semantic reasoning、long-horizon autonomy 与 full-body control。

## Planner Notes

- llm dynamic expansion (medium): 智能体在具身系统中的新近表述分散在 agentic control、embodied reasoning、skill graph、memory、success detection 与 multi-agent collaboration，需要跨词族检索。
