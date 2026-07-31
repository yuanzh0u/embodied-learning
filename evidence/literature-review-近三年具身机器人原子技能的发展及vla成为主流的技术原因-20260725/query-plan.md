# Query Plan: 近三年具身机器人原子技能的发展及VLA成为主流的技术原因

## Scope

- Knowledge IDs: EA-MODEL, EA-XEMBODIMENT, EA-EVAL
- Families: vla
- Suggested categories: cs.AI, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 144
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-atomic-skill-direct | core | `(all:"atomic skill" OR all:"atomic skills") AND (all:robot OR all:robotic)` | 直接覆盖近年以 atomic skill 命名的机器人方法。 |
| dynamic-skill-library | mechanism | `all:"skill library" AND (all:"robot manipulation" OR all:"embodied control")` | 覆盖可复用技能库的构建、检索、扩展与组合。 |
| dynamic-skill-chaining | mechanism | `(all:"skill chaining" OR all:"skill composition") AND all:robot` | 原子技能的技术价值取决于长时程组合与子任务依赖。 |
| dynamic-motor-primitives | adjacent | `(all:"motor primitive" OR all:"behavior primitive" OR all:"action primitive") AND (all:manipulation OR all:robot)` | 覆盖不使用 atomic skill 命名的相邻技术谱系。 |
| dynamic-hierarchical-policy | mechanism | `all:"hierarchical policy" AND (all:"robot manipulation" OR all:"long-horizon manipulation")` | 覆盖高层技能选择与低层连续控制的分层方法。 |
| dynamic-task-decomposition | mechanism | `(all:"task decomposition" OR all:"subtask decomposition") AND (all:robot OR all:embodied) AND all:manipulation` | 覆盖用语言模型或规划器将长任务拆成技能的路线。 |
| dynamic-skill-segmentation | mechanism | `(all:"skill segmentation" OR all:"skill discovery") AND (all:robot OR all:manipulation)` | 覆盖从演示中自动发现技能边界和潜变量的方法。 |
| dynamic-continual-skills | deployment | `(all:"continual skill learning" OR all:"lifelong robot learning") AND (all:manipulation OR all:control)` | 检验技能库在持续扩展、遗忘与新技能接入上的优势和成本。 |
| dynamic-skill-interface-limit | limitation | `(all:"skill library" OR all:"skill primitive") AND (all:limitation OR all:failure OR all:scalability) AND all:robot` | 寻找固定技能语义、接口脆弱、组合误差和扩展成本等反方证据。 |
| dynamic-skill-evaluation | evaluation | `(all:"skill composition" OR all:"hierarchical manipulation") AND (all:benchmark OR all:evaluation OR all:"real robot")` | 寻找对长时程组合、真机闭环和失败恢复的评测证据。 |
| dynamic-generalist-specialist | adjacent | `(all:generalist AND all:specialist) AND (all:"robot policy" OR all:"robot manipulation")` | 对照统一通才模型与专用技能专家的取舍。 |
| dynamic-vla-atomic-hybrid | adjacent | `(all:VLA OR all:"vision-language-action") AND (all:"atomic skill" OR all:"skill library" OR all:"mixture of experts")` | 直接寻找 VLA 与技能库、专家路由结合的融合路线。 |
| calibrated-skill-guided-mixture-of-experts | calibrated-term | `all:"skill-guided mixture-of-experts"` | 新近原子技能工作将技能专家路由与 VLA 联系起来。 |
| calibrated-continual-skill-acquisition | calibrated-term | `all:"continual skill acquisition"` | 技能库路线的一个主要差异化目标。 |
| calibrated-semantically-grounded-atomic-skill-library | calibrated-term | `all:"semantically grounded atomic skill library"` | 覆盖技能分段、语义一致性和可组合性。 |
| calibration-atomicvla-moe | calibrated-query | `(all:"skill-guided mixture-of-experts" OR all:"continual skill acquisition") AND all:robot` | 捕获 AtomicVLA 及相邻融合路线。 |
| calibration-semantic-atomic | calibrated-query | `all:"semantic atomic skill" OR all:"semantically grounded atomic skill"` | 捕获语义技能分段与组合路线。 |
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
| ea-xembodiment-cross-embodiment | core | `all:"cross-embodiment" AND all:"robot manipulation"` | Find work that explicitly transfers skills or data across robot bodies. |
| ea-xembodiment-retargeting-dexterous | retargeting | `all:retargeting AND all:"dexterous hand"` | Cover human hand to dexterous robot hand mapping and its limits. |
| ea-xembodiment-human-to-robot | transfer | `all:"human-to-robot" AND all:demonstration` | Find human demonstration transfer papers beyond exact robot teleoperation. |
| ea-xembodiment-action-representation | representation | `all:"action representation" AND all:embodiment AND all:robot` | Expose latent actions, adapters, and interfaces that mediate embodiment mismatch. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-atomic-skill-direct, vla-core, vla-named-models, ea-model-named-foundation, ea-xembodiment-cross-embodiment, ea-eval-closed-loop |
| adjacent-and-transfer | 3 | dynamic-skill-library, dynamic-skill-chaining, dynamic-motor-primitives, dynamic-hierarchical-policy, dynamic-task-decomposition, dynamic-skill-segmentation, dynamic-continual-skills, dynamic-skill-evaluation, dynamic-generalist-specialist, dynamic-vla-atomic-hybrid, calibrated-skill-guided-mixture-of-experts, calibrated-continual-skill-acquisition, calibrated-semantically-grounded-atomic-skill-library, calibration-atomicvla-moe, calibration-semantic-atomic, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, ea-model-finetuning, ea-xembodiment-retargeting-dexterous, ea-xembodiment-human-to-robot, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| limits-and-counterevidence | 3 | dynamic-skill-interface-limit, vla-negative-transfer |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization, ea-xembodiment-action-representation |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-atomic-skills | `site:arxiv.org/abs robot atomic skill library manipulation` | 补充 arXiv API 对新命名和短语的召回。 |
| browser-composable-skills | `site:arxiv.org/abs robot composable skills skill chaining long-horizon manipulation` | 补充组合技能和长时程语彙。 |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-calibrated-skill-guided-mixture-of-experts | arxiv | `"skill-guided mixture-of-experts" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: skill-guided mixture-of-experts. |
| web-calibrated-continual-skill-acquisition | arxiv | `"continual skill acquisition" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: continual skill acquisition. |
| web-calibrated-semantically-grounded-atomic-skill-library | arxiv | `"semantically grounded atomic skill library" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: semantically grounded atomic skill library. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-atomic-skill-direct | arxiv_api | llm | high | `(all:"atomic skill" OR all:"atomic skills") AND (all:robot OR all:robotic)` | 直接覆盖近年以 atomic skill 命名的机器人方法。 |
| dynamic-skill-library | arxiv_api | llm | high | `all:"skill library" AND (all:"robot manipulation" OR all:"embodied control")` | 覆盖可复用技能库的构建、检索、扩展与组合。 |
| dynamic-skill-chaining | arxiv_api | llm | high | `(all:"skill chaining" OR all:"skill composition") AND all:robot` | 原子技能的技术价值取决于长时程组合与子任务依赖。 |
| dynamic-motor-primitives | arxiv_api | llm | high | `(all:"motor primitive" OR all:"behavior primitive" OR all:"action primitive") AND (all:manipulation OR all:robot)` | 覆盖不使用 atomic skill 命名的相邻技术谱系。 |
| dynamic-hierarchical-policy | arxiv_api | llm | high | `all:"hierarchical policy" AND (all:"robot manipulation" OR all:"long-horizon manipulation")` | 覆盖高层技能选择与低层连续控制的分层方法。 |
| dynamic-task-decomposition | arxiv_api | llm | high | `(all:"task decomposition" OR all:"subtask decomposition") AND (all:robot OR all:embodied) AND all:manipulation` | 覆盖用语言模型或规划器将长任务拆成技能的路线。 |
| dynamic-skill-segmentation | arxiv_api | llm | high | `(all:"skill segmentation" OR all:"skill discovery") AND (all:robot OR all:manipulation)` | 覆盖从演示中自动发现技能边界和潜变量的方法。 |
| dynamic-continual-skills | arxiv_api | llm | high | `(all:"continual skill learning" OR all:"lifelong robot learning") AND (all:manipulation OR all:control)` | 检验技能库在持续扩展、遗忘与新技能接入上的优势和成本。 |
| dynamic-skill-interface-limit | arxiv_api | llm | high | `(all:"skill library" OR all:"skill primitive") AND (all:limitation OR all:failure OR all:scalability) AND all:robot` | 寻找固定技能语义、接口脆弱、组合误差和扩展成本等反方证据。 |
| dynamic-skill-evaluation | arxiv_api | llm | high | `(all:"skill composition" OR all:"hierarchical manipulation") AND (all:benchmark OR all:evaluation OR all:"real robot")` | 寻找对长时程组合、真机闭环和失败恢复的评测证据。 |
| dynamic-generalist-specialist | arxiv_api | llm | medium | `(all:generalist AND all:specialist) AND (all:"robot policy" OR all:"robot manipulation")` | 对照统一通才模型与专用技能专家的取舍。 |
| dynamic-vla-atomic-hybrid | arxiv_api | llm | high | `(all:VLA OR all:"vision-language-action") AND (all:"atomic skill" OR all:"skill library" OR all:"mixture of experts")` | 直接寻找 VLA 与技能库、专家路由结合的融合路线。 |
| browser-atomic-skills | browser_fallback | llm | high | `site:arxiv.org/abs robot atomic skill library manipulation` | 补充 arXiv API 对新命名和短语的召回。 |
| browser-composable-skills | browser_fallback | llm | high | `site:arxiv.org/abs robot composable skills skill chaining long-horizon manipulation` | 补充组合技能和长时程语彙。 |

## Calibration Notes

- arxiv calibration (high): AtomicVLA 将 atomic skill library、skill-guided mixture-of-experts、continual skill acquisition 和 long-horizon planning 绑定在同一语汇中。
- arxiv calibration (high): 论文使用 atomic skill library construction、dynamic update 与 VLA fine-tuning 词汇。
- arxiv calibration (high): LRLL 使用 composable and generalizable skills、skill abstractor 与 lifelong robot library learning 词汇。

## Planner Notes

- llm dynamic expansion (high): ‘原子技能’在论文中并非统一标签，需同时覆盖 atomic skill、skill primitive、motor primitive、skill library、skill chaining、hierarchical policy、option/behavior tree 以及长时程任务分解。
