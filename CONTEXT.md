---
id: PROJECT-CONTEXT
title: 项目上下文词表
type: glossary
updated: 2026-07-17
tags: [context, glossary, embodied-ai, query-planning]
---

# 项目上下文词表

本文只定义本项目共享语言，不写 Skill implementation spec。更细的证据、来源与主题知识仍按 `knowledge/` 路由加载。

| 术语 | 工作定义 |
|---|---|
| query plan | 围绕一个研究问题形成的结构化检索策略，说明 topic mapping、query tier、query channel 和每条 query 的 rationale。它是检索前的计划，不是论文证据。 |
| arXiv API query | 面向官方 arXiv API 元数据检索的 query 字符串。它应使用 API 可理解的论文检索表达，不混入 `site:`、Browser 搜索语法或社交平台线索。 |
| browser fallback query | 当 arXiv API 结果过少、受限或需要补充候选线索时，用 Browser/web search 执行的 fallback query。它用于发现候选论文、项目页或作者页入口，不能直接提升为 evidence。 |
| web calibration | 用 arXiv 页面、项目页、作者页、实验室页面等 web sources 校准关键词、别名、方法族和社区新词的过程。它只调整 query wording 与覆盖面，不替代正文证据。 |
| social calibration | 用 Reddit、X/Twitter 等社交讨论观察研究者或用户实际使用的说法、抱怨和新词。它属于 noisy signal，默认只作为低置信 query 线索。 |
| specialized family | 一组可复用的具身智能专项检索族，例如 UMI、VLA、Sim2Real、retargeting、tactile/force 等，用于把 broad topic 展开到命名方法、邻接任务和常见 failure surface。 |
| query tier | query plan 中表达召回层级和意图的标签，如 direct、adjacent、family、limitation、negative 或 calibration。tier 解释这条 query 预计捕获哪类材料。 |
| low-confidence calibration | 来自社交平台、非正式网页或其他噪声较高来源的校准记录。它可以提示新 query 或别名，但必须保留低置信标记，不能当作 accepted claim 或 source evidence。 |
| candidate pool | 多轮检索、去重和初筛后形成的相关论文候选集合。它用于证明覆盖范围，不等于已阅读全文或最终引用数。 |
| full-text eligible | 已取得完整、可解析且可定位原文上下文的非 OCR 全文。摘要、搜索片段、残缺 PDF 和扫描件不属于本项目的可用全文。 |
| paper note | 对单篇完整论文进行 map read / deep read 后形成的结构化记录，包含研究问题、方法、结果、限制和带原文上下文的 evidence cards。 |
| claim-support audit | 检查 paper note 中每个主张是否被对应全文上下文支持的审计。只有通过审计的主张才能投影为 accepted evidence。 |
| accepted evidence event | 从通过审计的 paper note 投影出的论文级证据记录，具有当前有效 run 集合中全局唯一的 event ID。 |
| review packet | 面向研究者的中预算审计视图，汇总综述范围、证据分布、共识、限制和缺口；它不是读者成稿。 |
| reader-facing articles | 科研备忘录、知乎解释稿和小红书稿三类表达层。它们共享 accepted evidence，但必须按各自读者和文体独立组织。 |
| active review run | 由 [文献综述成果目录](knowledge/literature-review-catalog.md) 声明为当前知识卡证据入口的 append-only run；历史 run 保留但不默认加载。 |
| reactive VLA | 狭义指主要通过行为克隆，把当前观测与语言指令直接映射为下一步或下一段动作、但不显式预测和检验动作后果的 VLA 策略；它不等同于全部 VLA 架构。 |
| VLA–world-model fusion stack | 知识库对近期跨论文证据的 synthesis：VLA 提供语义理解、任务分解与动作先验，动作条件世界模型负责后果预演、候选排序与失败识别，本体适配器和底层控制器负责可执行落地。 |
| action-conditioned reliability | 世界模型在给定动作条件下，对真实后果、物理约束、长时一致、失败状态和候选排序保持可靠，并能在可用延迟内支持闭环决策的联合要求。 |
| embodied data contamination | 具身数据中的来源、时间、任务、动作、模型版本或评测边界关系失真；既包括近重复、同步错位和训练—评测泄漏，也包括投毒、持久后门及生成扩增中的二次激活。它不是只在入库前发生的样本级脏数据。 |
| semantic leakage | 训练与评测在场景、任务逻辑、对象布局或指令—动作映射上过度相似，使模型依赖记忆取得高分；即使不存在字节级重复，也会破坏泛化证据的独立性。 |
| supply-chain persistence | 污染或后门进入基础模型、适配模块或检查点后继续穿过下游干净微调的现象；因此只审计本地新增示教不能证明模型链路无污染。 |
| secondary activation | 原始数据在入库时看似安全，但经世界模型生成、轨迹扩增或重标注后转化为危险行为并污染下游策略的现象。 |
| ego-centric behavior data | 人类第一视角视频及其恢复出的手—物轨迹、视点运动和任务结构。它适合提供高覆盖行为先验，但默认不等于机器人控制监督；具体边界见 EA-DATA、EA-XEMBODIMENT 和 EA-MODEL。 |
| executable supervision | 已对坐标系、尺度、动作接口、运动学可达性、接触结构和动力学可行性做过核验，可被目标机器人训练或闭环评测消费的监督信号。 |
| visual localization stack | 从地点候选检索，经视觉/几何验证，到 6DoF 位姿估计或局部细化，再到拒识与恢复的完整定位链；不能用单一 Recall@K 代替整链结果。 |
| recoverability domain | 给定地图、参考覆盖、初始化误差和场景条件时，定位或位姿细化仍能可靠收敛的工作域。超出该域时应拒识、重定位或切换传感器。 |
| risk–coverage | 同时报告被系统接受的查询覆盖率与这些已接受结果的错误风险；低风险但接近零覆盖不代表系统具备可用定位能力。 |
