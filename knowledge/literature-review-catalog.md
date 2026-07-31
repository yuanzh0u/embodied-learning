---
id: KB-LIT-REVIEWS
title: 文献综述成果目录
type: evidence-routing-index
updated: 2026-07-29
tags: [literature-review, evidence-routing, paper-reading, provenance]
---

# 文献综述成果目录

本目录连接主题卡与论文级证据，不重复存放论文摘要。当前有效版本包含 17 个 paper-reader-backed 基础 run 与 11 个跨 run 主题综合；`reader-v1` 保留为历史产物，但其事件编号命名空间存在跨 run 冲突，不作为知识卡的当前证据入口。

## 批次概况

- Review mode：17 项基础 run 均为 `scoping`。
- 检索池：基础 run 每项 172–1,409 篇候选论文。
- 全文层：基础 run 每项 48–162 篇具有可读全文。
- 精读层：除 loco-manipulation run 按论证覆盖选取 21 篇外，其余 16 项基础 run 每项选取 15 篇核心论文，均完成 paper note 与 claim-support audit。
- 基础 run 总量：261 个任务—论文精读实例，143 篇不重复论文，280 条全局唯一正式证据事件（286 条事件出现中有 6 条由 Ego run 复用）。
- 跨 run 综合：11 项。前 8 项包括“反应式 VLA—世界模型融合栈”、“视频世界模型可靠应用任务”、“近半年 VLA 最大技术突破”、“近半年智能体技术产业应用”、“近一年多模态训练方法演进”、“近一年触觉发展”、“近半年力觉发展”与“近三年原子技能与 VLA 主流化”；“预训练数据源与采集参数”综合在 1,398 篇候选、40 篇可读全文中接纳 20 篇；“数据时空一致性”综合在 1,401 篇候选、52 篇可读全文中接纳 20 篇；本次“空间数据生产与机器人—智驾比较”综合在 225 篇候选、44 篇完整全文中接纳 17 篇已审计论文，聚焦时空真值、不可观状态、长尾生产与闭环验收。
- 全文边界：只接收完整、可解析的非 OCR 全文；扫描论文不在当前探索范围。
- 成稿：每项均包含科研备忘录、知乎解释稿和小红书稿，三者共享证据层但独立组织表达。

## 17 项成果

“规模”依次表示候选池 / 可读全文 / 精读并接纳论文数。

| ID | 综述主题 | 主要知识卡 | 规模 | 审计入口 |
|---|---|---|---:|---|
| LR-4D | 4D 时空推理 | EA-4D, EA-MODEL, EA-EVAL | 915 / 128 / 15 | [run](../evidence/literature-review-4d时空推理-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-4d时空推理-20260714-reader-v2/review-packet.md) |
| LR-4D-DATA | 4D 时空推理对数据的需求 | EA-4D, EA-DATA, EA-SENSOR | 915 / 128 / 15 | [run](../evidence/literature-review-4d时空推理对数据的需求-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-4d时空推理对数据的需求-20260714-reader-v2/review-packet.md) |
| LR-VLA-ALIGN | VLA 中稀疏语言、稠密视觉与连续动作对齐 | EA-ALIGN, EA-MODEL, EA-XEMBODIMENT | 924 / 131 / 15 | [run](../evidence/literature-review-sparse-language-dense-vision-and-continuous-action-alignment-in-vla-syst-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-sparse-language-dense-vision-and-continuous-action-alignment-in-vla-syst-20260714-reader-v2/review-packet.md) |
| LR-WM-EVAL | 世界模型评测边界 | EA-EVAL, EA-4D | 885 / 130 / 15 | [run](../evidence/literature-review-世界模型评测边界-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-世界模型评测边界-20260714-reader-v2/review-packet.md) |
| LR-WM-DATA | 世界模型需要什么样的训练数据 | EA-DATA, EA-MODEL, EA-EVAL | 885 / 130 / 15 | [run](../evidence/literature-review-世界模型需要什么样的训练数据-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-世界模型需要什么样的训练数据-20260714-reader-v2/review-packet.md) |
| LR-SENSOR-ERROR | 具身传感器感知误差 | EA-SENSOR, ERR-EMBODIED | 903 / 130 / 15 | [run](../evidence/literature-review-具身传感器感知误差-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-具身传感器感知误差-20260714-reader-v2/review-packet.md) |
| LR-PVC | 感知误差与认知误差的区别 | ERR-EMBODIED, ERR-PATTERN | 936 / 130 / 15 | [run](../evidence/literature-review-具身数据感知误差与认知误差区别-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-具身数据感知误差与认知误差区别-20260714-reader-v2/review-packet.md) |
| LR-TRACE | 具身数据感知误差溯源 | ERR-EMBODIED, ERR-PATTERN, EA-DATA | 936 / 130 / 15 | [run](../evidence/literature-review-具身数据感知误差溯源-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-具身数据感知误差溯源-20260714-reader-v2/review-packet.md) |
| LR-DQ-CONTRA | 具身智能数据质量的主要矛盾 | EA-DATA, EA-SENSOR, EA-EVAL | 822 / 124 / 15 | [run](../evidence/literature-review-具身智能数据质量的主要矛盾-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-具身智能数据质量的主要矛盾-20260714-reader-v2/review-packet.md) |
| LR-TWM | 触觉世界模型 | EA-SENSOR, EA-MODEL, EA-EVAL | 867 / 124 / 15 | [run](../evidence/literature-review-触觉世界模型-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-触觉世界模型-20260714-reader-v2/review-packet.md) |
| LR-DQ-YEAR | 近一年论文中的具身智能数据质量 | EA-DATA, EA-XEMBODIMENT | 851 / 90 / 15 | [run](../evidence/literature-review-近一年已发表论文中的具身智能数据质量-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-近一年已发表论文中的具身智能数据质量-20260714-reader-v2/review-packet.md) |
| LR-UMI | 近半年 UMI 数据质量 | EA-DATA, EA-HARDWARE, EA-SENSOR | 862 / 122 / 15 | [run](../evidence/literature-review-近半年-umi-数据质量-20260714-reader-v2/run.json) · [packet](../evidence/literature-review-近半年-umi-数据质量-20260714-reader-v2/review-packet.md) |
| LR-EGO-DATA | 近一年 Ego-centric 数据用于具身模型训练的问题与困难 | EA-DATA, EA-XEMBODIMENT, EA-MODEL, EA-SENSOR | 1,409 / 162 / 15 | [run](../evidence/literature-review-ego-centric-数据在具身模型训练中的问题与困难-20260715/run.json) · [packet](../evidence/literature-review-ego-centric-数据在具身模型训练中的问题与困难-20260715/review-packet.md) |
| LR-EGO-HAND | 近一年 Ego-centric 数据手部检测与追踪的问题和难点 | EA-DATA, EA-SENSOR, EA-HARDWARE, EA-4D | 172 / 48 / 15 | [run](../evidence/literature-review-近一年-ego-centric-数据手部检测与追踪的问题和难点-20260729/run.json) · [packet](../evidence/literature-review-近一年-ego-centric-数据手部检测与追踪的问题和难点-20260729/review-packet.md) |
| LR-VLOC | 近一年图像视觉定位方法的发展与挑战 | EA-VLOC, EA-SENSOR, EA-EVAL, EA-HARDWARE | 321 / 53 / 15 | [run](../evidence/literature-review-近一年图像视觉定位方法的发展与挑战-20260715/run.json) · [packet](../evidence/literature-review-近一年图像视觉定位方法的发展与挑战-20260715/review-packet.md) |
| LR-CONTAM | 近一年论文中的具身数据污染问题 | EA-DATA, EA-EVAL, EA-MODEL | 964 / 49 / 15 | [run](../evidence/literature-review-近一年论文中的具身数据污染问题-20260715/run.json) · [packet](../evidence/literature-review-近一年论文中的具身数据污染问题-20260715/review-packet.md) |
| LR-LOCOMANIP | 近一年 loco-manipulation 研究进展 | EA-LOCOMANIP, EA-MODEL, EA-EVAL, EA-XEMBODIMENT, EA-SENSOR | 556 / 76 / 21 | [run](../evidence/literature-review-近一年-loco-manipulation-研究进展-20260719/run.json) · [packet](../evidence/literature-review-近一年-loco-manipulation-研究进展-20260719/review-packet.md) |

## 跨 run 综合专题

| ID | 综合问题 | 主要知识卡 | 规模 | 审计入口 |
|---|---|---|---:|---|
| LR-VLA-WM-SHIFT | 近一年为何说反应式 VLA 已死、世界模型当立 | EA-MODEL, EA-EVAL, EA-4D, EA-ALIGN | 1,547 / 175 / 28 | [run](../evidence/literature-review-近一年为何说反应式vla已死世界模型当立-20260717/run.json) · [packet](../evidence/literature-review-近一年为何说反应式vla已死世界模型当立-20260717/review-packet.md) |
| LR-WM-TASKS | 近一年世界视频模型最可靠的应用任务 | EA-MODEL, EA-EVAL, EA-4D | 1,589 / 175 / 30 | [run](../evidence/literature-review-近一年世界视频模型最可靠的应用任务-20260719/run.json) · [packet](../evidence/literature-review-近一年世界视频模型最可靠的应用任务-20260719/review-packet.md) |
| LR-VLA-BREAKTHROUGH-HY1 | 近半年 VLA 在具身领域最大的技术突破 | EA-MODEL, EA-EVAL, EA-4D, EA-ALIGN | 1,246 / 161 / 27 | [run](../evidence/literature-review-近半年vla在具身领域最大的技术突破-20260719/run.json) · [packet](../evidence/literature-review-近半年vla在具身领域最大的技术突破-20260719/review-packet.md) |
| LR-MULTIMODAL-TRAINING-YEAR | 近一年触觉、力觉、视觉、语言等多模态数据在具身机器人训练方法中的演进 | EA-SENSOR, EA-MODEL, EA-ALIGN, EA-XEMBODIMENT, EA-DATA | 1,789 / 247 / 42 | [run](../evidence/literature-review-近一年触觉-力觉-视觉-语言等多模态数据在具身机器人训练方法中的演进-20260720/run.json) · [packet](../evidence/literature-review-近一年触觉-力觉-视觉-语言等多模态数据在具身机器人训练方法中的演进-20260720/review-packet.md) |
| LR-TACTILE-YEAR | 近一年触觉在具身机器人领域的发展 | EA-SENSOR, EA-DATA, EA-MODEL, EA-EVAL | 867 / 124 / 23 | [run](../evidence/literature-review-近一年触觉在具身机器人领域的发展-20260720/run.json) · [packet](../evidence/literature-review-近一年触觉在具身机器人领域的发展-20260720/review-packet.md) |
| LR-FORCE-SENSE-HY1 | 近半年力觉在具身机器人领域的发展 | EA-SENSOR, EA-MODEL, EA-EVAL | 176 / 46 / 17 | [run](../evidence/literature-review-近半年力觉在具身机器人领域的发展-20260720/run.json) · [packet](../evidence/literature-review-近半年力觉在具身机器人领域的发展-20260720/review-packet.md) |
| LR-AGENTIC-INDUSTRY-HY1 | 近半年智能体技术在具身智能行业的发展应用 | EA-MODEL, EA-EVAL, EA-BIZ | 1,250 / 161 / 32 | [run](../evidence/literature-review-近半年智能体技术在具身智能行业的发展应用-20260725/run.json) · [packet](../evidence/literature-review-近半年智能体技术在具身智能行业的发展应用-20260725/review-packet.md) |
| LR-ATOMIC-SKILLS-3Y | 近三年具身机器人原子技能的发展及 VLA 成为主流的技术原因 | EA-MODEL, EA-ALIGN, EA-XEMBODIMENT, EA-EVAL | 612 / 56 / 15 | [run](../evidence/literature-review-近三年具身机器人原子技能的发展及vla成为主流的技术原因-20260725/run.json) · [packet](../evidence/literature-review-近三年具身机器人原子技能的发展及vla成为主流的技术原因-20260725/review-packet.md) |
| LR-PRETRAIN-DATA-SOURCES-YEAR | 近一年具身智能预训练模型对数据源与采集参数的要求 | EA-DATA, EA-HARDWARE, EA-SENSOR, EA-MODEL, EA-XEMBODIMENT | 1,398 / 40 / 20 | [run](../evidence/literature-review-近一年具身智能预训练模型对数据源与采集参数的要求-20260726/run.json) · [packet](../evidence/literature-review-近一年具身智能预训练模型对数据源与采集参数的要求-20260726/review-packet.md) |
| LR-SPATIOTEMP-CONSISTENCY-YEAR | 近一年具身智能论文中的数据时空一致性 | EA-DATA, EA-SENSOR, EA-4D, EA-ALIGN | 1,401 / 52 / 20 | [run](../evidence/literature-review-近一年具身智能论文中的数据时空一致性-20260727/run.json) · [packet](../evidence/literature-review-近一年具身智能论文中的数据时空一致性-20260727/review-packet.md) |
| LR-SPATIAL-DATA-ROBOT-AV-YEAR | 近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同 | EA-DATA, EA-SENSOR, EA-4D | 225 / 44 / 17 | [run](../evidence/literature-review-近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同-20260727/run.json) · [packet](../evidence/literature-review-近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同-20260727/review-packet.md) |

## 按上下文预算加载

| 预算 | 加载内容 | 用途 |
|---|---|---|
| 低 | 主索引 + 1 张主题卡 | 获取压缩判断、指标与适用边界 |
| 中 | 主题卡 + 对应 `review-packet.md` | 查看证据范围、共识、限制和论文分布 |
| 高 | `paper-note-index.json` → 单篇 paper note → claim-support audit | 核验论文结构、原文上下文和主张支持关系 |
| 写作 | `writing-brief.md` + `evidence-appendix.md` + 目标文体成稿 | 复用论证结构并保持引用可追溯 |

不要默认整读 `candidate-registry.json` 或全部论文笔记。候选池用于证明覆盖，主题判断以通过审计的 accepted evidence 为准。

## 共同结论

- 具身数据质量是相对于目标任务、目标策略和闭环结果的条件效用，不是单一静态分数。
- 从视频或图文走向世界模型，需要补齐动作干预、几何对应、接触状态、失败恢复和监督可靠性。
- VLA 的主要接口矛盾是语言、视觉与动作的粒度和物理语义错配，不能靠统一 token 形式自动消除。
- 世界模型只有同时满足结果保真、长程一致、动作忠实和计算可用，才可能成为策略评估或规划工具。
- 机器人失败应按第一处可证伪偏离点分账，区分感知、认知、动作转译、控制执行和评测错误。
- 触觉、力、3D 与事件视觉的价值取决于是否补足当前任务的不可观测状态，并在真实闭环中产生可验证增益。
- Ego-centric 数据提供的是高覆盖行为先验，不是完整机器人控制监督；规模收益以坐标解耦、动作/接触恢复、本体转换、可执行性过滤和目标机器人锚定为条件。
- Ego-centric 手部追踪的瓶颈已从可见帧单帧精度转向观测断裂管理：头部自运动、遮挡/出框、深度歧义和时序误差会耦合；时序或多模态先验只能在仍有可靠观测锚点时提高稳定性，评测应保留丢检、身份续接、重获取和世界轨迹漂移。
- 图像视觉定位正在从单一检索精度转向地图几何、可恢复域、风险—覆盖和评测真值的联合治理；神经表示与高相似度都不能替代几何验证和失败拒识。
- 具身数据污染是来源、时间结构、任务边界和模型供应链之间的关系失真；治理必须覆盖语义泄漏、场景/轨迹近重复、动作窗异常、持久后门与世界模型二次激活，不能只做入库前样本清洗。
- “反应式 VLA 已死”只对不显式检验后果的狭义策略成立；当前证据更支持 VLA 语义/动作先验、世界模型后果预演和本体控制联合的融合栈，而不是用视频生成器替代 VLA。
- 近半年 VLA 最大的技术突破是“后果可校验”的策略融合栈：用结构化世界状态或分层世界模型预演动作后果，再以失败诊断、恢复和低层控制闭环约束执行；BadWAM 等反例同时表明，视觉上合理的想象不等于动作忠实或安全。
- Loco-manipulation 正从上肢/下肢解耦转向任务意图—全身执行分层；统一动作接口、异构数据分工、地形/触觉/故障反馈已有真机证据，但开放世界瓶颈已上移到状态估计、长时序记忆、规划可执行性和失败恢复。
- 视频世界模型当前最可靠的是低权限、可复核的中间任务：同分布策略排序与淘汰、有本体锚定的数据/后训练、训练期 4D/几何监督，以及明确物理变量下的 what-if 检查；长时程高接触直接控制与安全裁决仍必须保留真实闭环。
- 近一年多模态训练的主线不是增加输入通道，而是按功能和频率分层：语言约束任务，视觉提供全局语义/几何，触觉与力/力矩预测和纠正接触，动作条件世界模型检查后果，平台适配器完成执行；无约束融合可能污染视觉动力学，视觉逼真的未来也不能替代动作忠实与真实闭环。
- 近一年触觉研究的主线是从附加观测升级为接触执行栈：同步数据和全手表征构成底座，触觉世界模型预测并验证动作，高频触觉纠正滑移与力不匹配，全身控制与安全过程评测提供闭环证据；通用化仍受硬件异构、同步标定、跨实例迁移和长期维护约束。
- 近半年力觉研究正从附加传感器路线转向“接触表征—动作条件预测—高频纠偏”的分层闭环；六维力/力矩、局部触觉力场与全身接触反馈分别承担不同尺度的状态，但收益以同步、标定、接触门控、控制层级和安全过程评测为条件。
- 近半年具身智能体的主线是形成“高层任务推理与记忆—技能/VLA 执行—实时控制与独立安全”的分层闭环，并把数据、仿真、评测和部署流程变成研发智能体可编排的工具；产业公开证据以 L1 演示和 L2 客户验证为主，持续商业运行仍集中于仓储搬运等窄任务。
- 原子技能没有被 VLA 淘汰：VLA 因跨机器人数据聚合、视觉语言先验和统一微调接口成为共享底座，技能化结构则迁入语义专家路由、局部闭环、层级规划与显式交接/恢复协议；长任务可靠性取决于二者的分层组合，而非单一路线替代。
- 具身预训练数据应实行“多样内容、受控契约、目标锚点”：设备与来源可异构，坐标/时间/动作/机位/标定/可靠性必须可解释；相机分辨率、帧率、码率与 FOV 没有跨任务通用门槛，应用有效可见性、物理时间同步和目标 VLA 闭环成功曲线验收。
- 数据时空一致性不是单一同步分数，而是物理时间、空间参考、跨视角/跨模态对应、动作—状态因果匹配和长程对象/接触连续性的五层契约；时间戳与外参对齐只是入场条件，最终应以动作—后果同步和真实闭环收益验收。
- 空间数据生产的共同瓶颈是把不完全、异步、有遮挡的观测变成可对动作后果负责的时空真值；具身机器人最终锚定本体相关的接触与执行真值，智能驾驶最终锚定 ODD 相关的地图拓扑、地理覆盖、稀有交互与闭环安全真值。

这些结论来自 17 项基础综述与 11 项跨 run 主题综合，属于知识库层面的 synthesis；具体论文支持应回到相应主题卡的证据锚点和 paper-reader-backed evidence event。
