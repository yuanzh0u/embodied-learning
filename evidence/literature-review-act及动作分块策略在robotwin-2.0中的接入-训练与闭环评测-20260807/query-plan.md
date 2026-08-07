# Query Plan: ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测

## Scope

- Knowledge IDs: EA-MODEL, EA-EVAL
- Families: none
- Suggested categories: cs.AI, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 100
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-robotwin-act-direct | core | `all:RoboTwin AND all:"Action Chunking Transformer"` | 捕获直接同时使用 ACT 与 RoboTwin 的研究。 |
| dynamic-robotwin-action-chunk | mechanism | `all:RoboTwin AND all:"action chunk"` | 覆盖在 RoboTwin 上研究动作块预测或执行的方法。 |
| dynamic-action-chunking-mechanism | mechanism | `all:"action chunking" AND all:"robot manipulation"` | 建立动作分块的机制、表达能力和误差累积证据。 |
| dynamic-adaptive-replanning | limitation | `(all:"adaptive action chunking" OR all:"execution horizon" OR all:replanning) AND all:"robot policy"` | 覆盖固定执行窗的反例、自适应重规划和响应性—连续性权衡。 |
| dynamic-temporal-aggregation | policy-interface | `(all:"temporal aggregation" OR all:"temporal ensembling") AND all:"robot manipulation"` | 覆盖 ACT 部署中跨动作块融合和平滑执行的核心接口。 |
| dynamic-multitask-bimanual-act | named-variant | `(all:"Action Chunking Transformer" OR all:"MoE-ACT") AND all:"multi-task" AND all:bimanual` | 覆盖 ACT 的多任务、语言条件和双臂变体。 |
| dynamic-robotwin-bimanual-benchmark | evaluation | `all:"RoboTwin 2.0" AND all:bimanual AND (all:benchmark OR all:evaluation)` | 补齐 RoboTwin 2.0 任务、域随机化和评测边界。 |
| dynamic-robotwin-policy-adapter | deployment | `all:RoboTwin AND (all:deployment OR all:adapter OR all:interface) AND all:policy` | 寻找策略包装器、观测编码和动作交付的工程证据。 |
| dynamic-robotwin-domain-randomization | evaluation | `all:RoboTwin AND all:"domain randomization" AND all:policy` | 捕获干净设置与困难随机化设置之间的鲁棒性落差。 |
| dynamic-action-chunk-runtime-monitor | deployment | `all:"action chunk" AND (all:monitor OR all:failure OR all:intervention) AND all:robot` | 覆盖动作块执行时的失败检测、插手和闭环安全。 |
| calibrated-phase-aware-chunk-execution | calibrated-term | `all:"phase-aware chunk execution"` | Fresh label for adaptive execution horizons on RoboTwin 2.0. |
| calibrated-denoising-variance-adaptive-chunking | calibrated-term | `all:"denoising-variance adaptive chunking"` | Fresh label for policy-internal replanning cues. |
| calibrated-implicit-ensembling | calibrated-term | `all:"implicit ensembling"` | Fresh mechanism hypothesis for why action chunking works. |
| calibration-pace | calibrated-query | `all:"phase-aware chunk execution" OR all:PACE` | Recover the PACE paper and related mentions. |
| calibration-dvac | calibrated-query | `all:"denoising-variance adaptive chunking" OR all:DVAC` | Recover DVAC and related action-chunk execution research. |
| calibration-chunk-mechanism | calibrated-query | `all:"implicit ensembling" AND all:"action chunking"` | Recover the recent mechanism-focused action chunking study. |
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
| direct-topic | 3 | dynamic-robotwin-act-direct, dynamic-multitask-bimanual-act, ea-model-vla, ea-model-named-foundation, ea-eval-closed-loop |
| adjacent-and-transfer | 3 | dynamic-robotwin-action-chunk, dynamic-action-chunking-mechanism, dynamic-robotwin-bimanual-benchmark, dynamic-robotwin-policy-adapter, dynamic-robotwin-domain-randomization, dynamic-action-chunk-runtime-monitor, calibrated-phase-aware-chunk-execution, calibrated-denoising-variance-adaptive-chunking, calibrated-implicit-ensembling, calibration-pace, calibration-dvac, calibration-chunk-mechanism, ea-model-finetuning, ea-eval-open-loop-benchmark, ea-eval-world-model, ea-eval-sim-real-correlation |
| limits-and-counterevidence | 3 | dynamic-adaptive-replanning |
| mechanisms-and-interfaces | 3 | dynamic-temporal-aggregation, ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-robotwin-act-browser | `site:arxiv.org/abs RoboTwin ACT action chunking robot` | API 检索不足时捕获直接交叉论文。 |
| dynamic-action-chunking-browser | `site:arxiv.org/abs adaptive action chunk execution replanning robot` | 捕获新的动作块执行别名和方法。 |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| web-calibrated-phase-aware-chunk-execution | arxiv | `"phase-aware chunk execution" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: phase-aware chunk execution. |
| web-calibrated-denoising-variance-adaptive-chunking | arxiv | `"denoising-variance adaptive chunking" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: denoising-variance adaptive chunking. |
| web-calibrated-implicit-ensembling | arxiv | `"implicit ensembling" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: implicit ensembling. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-robotwin-act-direct | arxiv_api | llm | high | `all:RoboTwin AND all:"Action Chunking Transformer"` | 捕获直接同时使用 ACT 与 RoboTwin 的研究。 |
| dynamic-robotwin-action-chunk | arxiv_api | llm | high | `all:RoboTwin AND all:"action chunk"` | 覆盖在 RoboTwin 上研究动作块预测或执行的方法。 |
| dynamic-action-chunking-mechanism | arxiv_api | llm | high | `all:"action chunking" AND all:"robot manipulation"` | 建立动作分块的机制、表达能力和误差累积证据。 |
| dynamic-adaptive-replanning | arxiv_api | llm | high | `(all:"adaptive action chunking" OR all:"execution horizon" OR all:replanning) AND all:"robot policy"` | 覆盖固定执行窗的反例、自适应重规划和响应性—连续性权衡。 |
| dynamic-temporal-aggregation | arxiv_api | llm | high | `(all:"temporal aggregation" OR all:"temporal ensembling") AND all:"robot manipulation"` | 覆盖 ACT 部署中跨动作块融合和平滑执行的核心接口。 |
| dynamic-multitask-bimanual-act | arxiv_api | llm | high | `(all:"Action Chunking Transformer" OR all:"MoE-ACT") AND all:"multi-task" AND all:bimanual` | 覆盖 ACT 的多任务、语言条件和双臂变体。 |
| dynamic-robotwin-bimanual-benchmark | arxiv_api | llm | high | `all:"RoboTwin 2.0" AND all:bimanual AND (all:benchmark OR all:evaluation)` | 补齐 RoboTwin 2.0 任务、域随机化和评测边界。 |
| dynamic-robotwin-policy-adapter | arxiv_api | llm | medium | `all:RoboTwin AND (all:deployment OR all:adapter OR all:interface) AND all:policy` | 寻找策略包装器、观测编码和动作交付的工程证据。 |
| dynamic-robotwin-domain-randomization | arxiv_api | llm | high | `all:RoboTwin AND all:"domain randomization" AND all:policy` | 捕获干净设置与困难随机化设置之间的鲁棒性落差。 |
| dynamic-action-chunk-runtime-monitor | arxiv_api | llm | medium | `all:"action chunk" AND (all:monitor OR all:failure OR all:intervention) AND all:robot` | 覆盖动作块执行时的失败检测、插手和闭环安全。 |
| dynamic-robotwin-act-browser | browser_fallback | llm | high | `site:arxiv.org/abs RoboTwin ACT action chunking robot` | API 检索不足时捕获直接交叉论文。 |
| dynamic-action-chunking-browser | browser_fallback | llm | high | `site:arxiv.org/abs adaptive action chunk execution replanning robot` | 捕获新的动作块执行别名和方法。 |

## Calibration Notes

- arxiv calibration (high): DVAC uses denoising variance to adapt the executed prefix and replanning point.
- arxiv calibration (high): PACE uses phase-aware chunk execution and evaluates on 50 RoboTwin 2.0 tasks.
- arxiv calibration (high): AAC uses action entropy for inference-time adaptive chunk sizing.
- arxiv calibration (high): Recent mechanism study frames implicit ensembling and non-Markovian expressivity as chunking benefits.
- official-context calibration (medium): RoboTwin's current terminology is ACT data preprocessing, policy training, evaluation, and temporal aggregation.

## Planner Notes

- llm dynamic expansion (high): ACT–RoboTwin 是窄方法与特定基准的交叉问题，需要显式扩展到动作分块、执行调度、多任务双臂操作和域随机化评测。
