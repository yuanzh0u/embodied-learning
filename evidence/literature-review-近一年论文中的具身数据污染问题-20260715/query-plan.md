# Query Plan: 近一年论文中的具身数据污染问题

## Scope

- Knowledge IDs: EA-DATA, EA-EVAL, EA-MODEL
- Families: vla, world-model, droid-ego4d
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 160
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-direct-data-contamination | core | `(all:"data contamination" OR all:"benchmark contamination") AND (all:robot OR all:embodied)` | 直接检索具身/机器人语境中的数据与基准污染。 |
| dynamic-direct-train-test-leakage | core | `(all:"data leakage" OR all:"train-test leakage" OR all:"test leakage") AND (all:"robot learning" OR all:"embodied AI")` | 捕获划分、时间和轨迹级训练—测试泄漏。 |
| dynamic-overlap-near-duplicate | quality | `(all:"dataset overlap" OR all:"train-test overlap" OR all:"near-duplicate" OR all:deduplication) AND (all:robot OR all:embodied OR all:egocentric)` | 检索跨数据集重叠、近重复和去重管道。 |
| dynamic-benchmark-exposure-vla | evaluation | `(all:"benchmark exposure" OR all:"benchmark leakage" OR all:memorization) AND (all:VLA OR all:"vision-language-action" OR all:"embodied agent")` | 检索基础 VLM/LLM 或 VLA 对评测任务的预训练曝光和记忆效应。 |
| dynamic-shortcut-overfit-embodied-benchmark | evaluation | `(all:shortcut OR all:overfit OR all:memorization) AND (all:"robot benchmark" OR all:"embodied reasoning" OR all:"robotic benchmark")` | 寻找被静态协议或传感运动先验掩盖的基准过拟合。 |
| dynamic-poisoning-vla-policy | limitation | `(all:poisoning OR all:poisoned OR all:backdoor) AND (all:"robot policy" OR all:"robot learning" OR all:"vision-language-action")` | 检索示教、预训练 VLA 和下游策略中的恶意污染。 |
| dynamic-world-model-poisoning | system-limitation | `all:"world model" AND (all:poisoning OR all:backdoor) AND (all:robot OR all:robotic)` | 检索世界模型生成数据供应链的潜伏式污染。 |
| dynamic-label-noise-pseudolabel-robot | quality | `(all:"label noise" OR all:"pseudo-label noise" OR all:"noisy demonstrations") AND (all:"robot learning" OR all:"robot manipulation")` | 检索错误标注、伪标签和混合质量示教如何进入训练集。 |
| dynamic-synthetic-feedback-contamination | adjacent | `(all:"synthetic data" OR all:"generated data") AND (all:contamination OR all:"model collapse" OR all:"feedback loop") AND (all:robot OR all:embodied)` | 检索生成数据反馈回训造成的系统性污染；仅作邻接证据面。 |
| dynamic-governance-provenance-dedup | deployment | `(all:provenance OR all:deduplication OR all:"data governance") AND (all:"robot dataset" OR all:"robot learning")` | 寻找可追溯、去重和污染防控工程方案。 |
| calibrated-static-evaluation-overfit | calibrated-term | `all:"static evaluation overfit"` | 用于发现不直接自称 contamination，但可能暴露评测与训练分布过度耶合的工作。 |
| calibrated-robot-learning-supply-chain | calibrated-term | `all:"robot learning supply chain"` | 世界模型投毒工作使用的系统边界词。 |
| calibrated-visual-token-backdoor | calibrated-term | `all:"visual-token backdoor"` | VLA 预训练污染与防御论文的具体机制词。 |
| calibration-static-eval-overfit | calibrated-query | `all:"static evaluation" AND (all:overfit OR all:shortcut) AND (all:VLA OR all:robot)` | 补足非显式 contamination 术语的评测污染候选。 |
| calibration-supply-chain-poisoning | calibrated-query | `all:"robot learning supply chain" AND (all:poisoning OR all:backdoor)` | 定向回收生成数据供应链攻击工作。 |
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
| droid-robot-manipulation | named-dataset | `all:DROID AND all:"robot manipulation"` | Find DROID robot data papers and reuse discussions. |
| ego4d-robot-learning | named-dataset | `all:Ego4D AND all:"robot learning"` | Catch robot-learning papers that draw on egocentric human video data. |
| droid-ego-egocentric-video | adjacent-data | `all:"egocentric video" AND all:"robot learning"` | Find human-observation data papers near Ego4D even when the dataset is not named. |
| droid-ego-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot demonstration"` | Capture natural-environment data collection and scaling constraints. |
| droid-ego-data-mixture | data-mixture | `all:"data mixture" AND all:"robot learning"` | Find cross-dataset mixture papers that discuss data compatibility and noise. |
| ea-data-robot-demonstrations | core | `all:"robot demonstration" AND all:data` | Find papers that treat demonstrations as reusable robot-learning data. |
| ea-data-demonstration-quality | quality | `all:"demonstration quality" AND all:"robot learning"` | Surface work that audits operator traces, consistency, and usable trajectory quality. |
| ea-data-in-the-wild | collection-setting | `all:"in-the-wild" AND all:"robot manipulation"` | Capture natural-scene collection papers and their generalization tradeoffs. |
| ea-data-dataset-curation | adjacent | `all:"dataset curation" AND all:"robot learning"` | Find dataset organization, filtering, metadata, and quality-control discussions. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dynamic-direct-data-contamination, dynamic-direct-train-test-leakage, dynamic-overlap-near-duplicate, dynamic-label-noise-pseudolabel-robot, vla-core, vla-named-models, world-model-robot, droid-robot-manipulation, ego4d-robot-learning, ea-data-robot-demonstrations, ea-data-demonstration-quality, ea-eval-closed-loop |
| adjacent-and-transfer | 3 | dynamic-benchmark-exposure-vla, dynamic-shortcut-overfit-embodied-benchmark, dynamic-synthetic-feedback-contamination, dynamic-governance-provenance-dedup, calibrated-static-evaluation-overfit, calibrated-robot-learning-supply-chain, calibrated-visual-token-backdoor, calibration-static-eval-overfit, calibration-supply-chain-poisoning, vla-open-x-embodiment, vla-large-scale-robot-data, vla-robot-foundation-action, vla-finetuning-policy, vla-data-mixture, world-model-video-prediction, world-model-planning, droid-ego-egocentric-video, droid-ego-in-the-wild, droid-ego-data-mixture, ea-data-in-the-wild, ea-data-dataset-curation, ea-eval-open-loop-benchmark, ea-eval-world-model |
| limits-and-counterevidence | 3 | dynamic-poisoning-vla-policy, dynamic-world-model-poisoning, vla-negative-transfer, world-model-contact, world-model-long-horizon |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-browser-embodied-contamination | `site:arxiv.org/abs ("data contamination" OR "train-test leakage" OR "dataset overlap") (robot OR embodied OR VLA)` | arXiv API 低召回时用于发现候选论文。 |
| dynamic-browser-robot-poisoning | `site:arxiv.org/abs (poisoning OR backdoor) ("robot learning" OR "robot policy" OR VLA OR "world model")` | 定向发现机器人数据投毒与后门工作。 |
| browser-vla-named-models | `site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot` | Find VLA and named robot foundation model papers when acronym or model names are sparse in API results. |
| browser-vla-data-mixtures | `site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")` | Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits. |
| browser-vla-transfer-limits | `site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")` | Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-calibrate-contamination-terms | llm | `embodied AI robot learning data contamination benchmark leakage dataset overlap backdoor poisoning` | 检查领域是否已形成新的固定术语或方法名。 |
| web-calibrated-static-evaluation-overfit | arxiv-web-search | `"static evaluation overfit" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: static evaluation overfit. |
| web-calibrated-robot-learning-supply-chain | arxiv-web-search | `"robot learning supply chain" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: robot learning supply chain. |
| web-calibrated-visual-token-backdoor | arxiv-web-search | `"visual-token backdoor" robot manipulation arxiv` | Check whether calibrated term appears in paper-facing web surfaces: visual-token backdoor. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-direct-data-contamination | arxiv_api | llm | medium | `(all:"data contamination" OR all:"benchmark contamination") AND (all:robot OR all:embodied)` | 直接检索具身/机器人语境中的数据与基准污染。 |
| dynamic-direct-train-test-leakage | arxiv_api | llm | medium | `(all:"data leakage" OR all:"train-test leakage" OR all:"test leakage") AND (all:"robot learning" OR all:"embodied AI")` | 捕获划分、时间和轨迹级训练—测试泄漏。 |
| dynamic-overlap-near-duplicate | arxiv_api | llm | medium | `(all:"dataset overlap" OR all:"train-test overlap" OR all:"near-duplicate" OR all:deduplication) AND (all:robot OR all:embodied OR all:egocentric)` | 检索跨数据集重叠、近重复和去重管道。 |
| dynamic-benchmark-exposure-vla | arxiv_api | llm | medium | `(all:"benchmark exposure" OR all:"benchmark leakage" OR all:memorization) AND (all:VLA OR all:"vision-language-action" OR all:"embodied agent")` | 检索基础 VLM/LLM 或 VLA 对评测任务的预训练曝光和记忆效应。 |
| dynamic-shortcut-overfit-embodied-benchmark | arxiv_api | llm | medium | `(all:shortcut OR all:overfit OR all:memorization) AND (all:"robot benchmark" OR all:"embodied reasoning" OR all:"robotic benchmark")` | 寻找被静态协议或传感运动先验掩盖的基准过拟合。 |
| dynamic-poisoning-vla-policy | arxiv_api | llm | medium | `(all:poisoning OR all:poisoned OR all:backdoor) AND (all:"robot policy" OR all:"robot learning" OR all:"vision-language-action")` | 检索示教、预训练 VLA 和下游策略中的恶意污染。 |
| dynamic-world-model-poisoning | arxiv_api | llm | medium | `all:"world model" AND (all:poisoning OR all:backdoor) AND (all:robot OR all:robotic)` | 检索世界模型生成数据供应链的潜伏式污染。 |
| dynamic-label-noise-pseudolabel-robot | arxiv_api | llm | medium | `(all:"label noise" OR all:"pseudo-label noise" OR all:"noisy demonstrations") AND (all:"robot learning" OR all:"robot manipulation")` | 检索错误标注、伪标签和混合质量示教如何进入训练集。 |
| dynamic-synthetic-feedback-contamination | arxiv_api | llm | low | `(all:"synthetic data" OR all:"generated data") AND (all:contamination OR all:"model collapse" OR all:"feedback loop") AND (all:robot OR all:embodied)` | 检索生成数据反馈回训造成的系统性污染；仅作邻接证据面。 |
| dynamic-governance-provenance-dedup | arxiv_api | llm | medium | `(all:provenance OR all:deduplication OR all:"data governance") AND (all:"robot dataset" OR all:"robot learning")` | 寻找可追溯、去重和污染防控工程方案。 |
| dynamic-browser-embodied-contamination | browser_fallback | llm | medium | `site:arxiv.org/abs ("data contamination" OR "train-test leakage" OR "dataset overlap") (robot OR embodied OR VLA)` | arXiv API 低召回时用于发现候选论文。 |
| dynamic-browser-robot-poisoning | browser_fallback | llm | medium | `site:arxiv.org/abs (poisoning OR backdoor) ("robot learning" OR "robot policy" OR VLA OR "world model")` | 定向发现机器人数据投毒与后门工作。 |
| dynamic-calibrate-contamination-terms | web_calibration | llm | medium | `embodied AI robot learning data contamination benchmark leakage dataset overlap backdoor poisoning` | 检查领域是否已形成新的固定术语或方法名。 |

## Calibration Notes

- arxiv-web-search calibration (high): 命中具身评测中的 shortcut、overfit 和 static evaluation 术语，仅用于校准查询。
- arxiv-web-search calibration (high): 既有候选池显示 robotic policy/VLA 论文使用 backdoor、poisoned data、visual token 等词。
- arxiv-web-search calibration (high): 既有候选池显示 world-model data poisoning、robot learning supply chain 是有效检索词。
- web-search-error calibration (low): 第二轮实时搜索发生网络错误；保留离线动态扩展并转入 arXiv API 检索。

## Planner Notes

- llm dynamic expansion (medium): ‘具身数据污染’尚无稳定统一术语；本轮将偶发的训练—评测泄漏、重复/近重复、预训练基准曝光、错误监督扩散和恶意投毒分开检索。
