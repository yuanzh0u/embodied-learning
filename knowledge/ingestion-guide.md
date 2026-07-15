---
id: KB-INGEST
title: 新素材入库规范
type: workflow
updated: 2026-07-15
tags: [ingestion, workflow, agent-process]
---

# 新素材入库规范

新增论文、报告、访谈、网页、产品信息或项目经验时，按以下流程处理。

## 1. 登记来源

在 [sources.md](sources.md) 记录：

- source id
- 文件或链接
- 类型：论文、报告、访谈、产品页、会议纪要、项目经验
- 时间范围或发布日期
- 可信等级：primary、secondary、industry-observation、inference
- 可复核链接或本地路径

## 2. 抽取主题

判断素材属于哪些主题卡：

- 数据采集与质量：EA-DATA
- 传感器与感知：EA-SENSOR
- 采集硬件：EA-HARDWARE
- 图像视觉定位、VPR、相机重定位与定位地图：EA-VLOC
- 跨本体迁移：EA-XEMBODIMENT
- 模型与预训练：EA-MODEL
- 评测与世界模型：EA-EVAL
- 4D 时空推理、世界动态、跨帧几何：EA-4D
- VLA 语言—视觉—动作接口：EA-ALIGN
- 商业化：EA-BIZ
- 误差治理：ERR-COMPARE / ERR-PATTERN
- 具身失败归因、感知/认知/控制误差：ERR-EMBODIED

如果没有合适主题，复制 [templates/topic-card.md](templates/topic-card.md) 创建新卡。

## 3. 更新主题卡

每次更新尽量只添加高信噪比内容：

- 新增关键判断
- 新增证据锚点
- 新增指标或评估方法
- 新增适用边界
- 新增待复核问题

避免把整段论文摘要直接粘进主题卡。长摘要应放到单独 source note 或保留在原文。

论文级材料优先结算到 `evidence/literature-review-<topic>-<date>/`；主题卡的 `source` 可直接登记 run 路径与 event locator，不在 `sources.md` 重复登记论文。

## 3.1 论文综述的四层证据漏斗

文献综述不得把“最终精读/引用论文数”当作“相关论文总数”。每个正式 run 至少区分：

1. `candidate-registry.json`：多轮检索和去重后的候选池。
2. `coverage-report.json`：候选规模、维度覆盖、全文可得性与停止条件。
3. `paper-note-index.json`：取得完整全文并完成 map read / deep read 的论文。
4. `evidence.jsonl`：通过 claim-support audit 后投影出的正式证据事件。

候选论文可以达到数百篇；精读论文数由 review mode、覆盖维度、论证需要和边际饱和度决定，不是固定上限。

## 3.2 全文恢复与阅读闸门

- 优先读取 arXiv HTML；不可得时下载 arXiv PDF 并做文本层提取。
- arXiv PDF 仍不可用时，可回退到出版方、作者主页或公开仓库中的同版本全文。
- 当前项目不使用 OCR，也不纳入只能通过扫描图像恢复正文的论文。
- 摘要、搜索片段、残缺 PDF 或无法确认完整性的文本只能留在 candidate/lead 层，不能生成 accepted evidence。
- 每篇 accepted 论文必须有 paper note、原文 locator/source context 和通过状态的 claim-support audit。
- 新事件 ID 必须在当前有效 run 中全局唯一；run manifest 应登记独立 `event_id_prefix`。

## 3.3 综述成果结算与知识卡同步

- 正式结算前检查科研备忘录、知乎解释稿、小红书稿、evidence appendix 和 trace map。
- 新版本使用新的 append-only run 目录；旧 run 保留，不原地覆盖。
- 主题卡 `source.file` 指向当前有效 run，并用实际存在的 event ID 或区间作为 locator。
- 更新 [literature-review-catalog.md](literature-review-catalog.md)，登记综述范围、候选池、全文数、精读数、知识卡映射和审计入口。
- 文章是面向读者的表达层，不是独立证据源；知识卡主张最终仍应回到 paper note、audit 和 evidence event。

## 4. 更新索引

新增主题卡后必须更新：

- [index.md](index.md) 的主题卡路由
- 对应领域的 `index.md`
- [literature-review-catalog.md](literature-review-catalog.md)，如果新增或升级文献综述 run
- [glossary.md](glossary.md)，如果引入新术语

## 5. 标记不确定性

快速变化信息必须写明日期，例如模型版本、产品规格、行业规模、政策、benchmark 排名。判断来自推断时，在卡片中标记 `inference`。
