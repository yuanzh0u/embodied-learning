---
id: KB-LIT-REVIEWS
title: 文献综述成果目录
type: evidence-routing-index
updated: 2026-07-15
tags: [literature-review, evidence-routing, paper-reading, provenance]
---

# 文献综述成果目录

本目录连接主题卡与论文级证据，不重复存放论文摘要。当前有效版本是 15 个 paper-reader-backed run；`reader-v1` 保留为历史产物，但其事件编号命名空间存在跨 run 冲突，不作为知识卡的当前证据入口。

## 批次概况

- Review mode：15 项均为 `scoping`。
- 检索池：每项 321–1,409 篇候选论文。
- 全文层：每项 49–162 篇具有可读全文。
- 精读层：每项选取 15 篇核心论文，完成 paper note 与 claim-support audit。
- 总量：225 个任务—论文精读实例，107 篇不重复论文，230 条全局唯一正式证据事件。
- 全文边界：只接收完整、可解析的非 OCR 全文；扫描论文不在当前探索范围。
- 成稿：每项均包含科研备忘录、知乎解释稿和小红书稿，三者共享证据层但独立组织表达。

## 15 项成果

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
| LR-VLOC | 近一年图像视觉定位方法的发展与挑战 | EA-VLOC, EA-SENSOR, EA-EVAL, EA-HARDWARE | 321 / 53 / 15 | [run](../evidence/literature-review-近一年图像视觉定位方法的发展与挑战-20260715/run.json) · [packet](../evidence/literature-review-近一年图像视觉定位方法的发展与挑战-20260715/review-packet.md) |
| LR-CONTAM | 近一年论文中的具身数据污染问题 | EA-DATA, EA-EVAL, EA-MODEL | 964 / 49 / 15 | [run](../evidence/literature-review-近一年论文中的具身数据污染问题-20260715/run.json) · [packet](../evidence/literature-review-近一年论文中的具身数据污染问题-20260715/review-packet.md) |

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
- 图像视觉定位正在从单一检索精度转向地图几何、可恢复域、风险—覆盖和评测真值的联合治理；神经表示与高相似度都不能替代几何验证和失败拒识。
- 具身数据污染是来源、时间结构、任务边界和模型供应链之间的关系失真；治理必须覆盖语义泄漏、场景/轨迹近重复、动作窗异常、持久后门与世界模型二次激活，不能只做入库前样本清洗。

这些结论是对 15 项综述的跨 run 综合，属于知识库层面的 synthesis；具体论文支持应回到相应主题卡的证据锚点和 paper-reader-backed evidence event。
