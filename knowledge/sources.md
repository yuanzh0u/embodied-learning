---
id: KB-SOURCES
title: 原始材料登记表
type: source-index
updated: 2026-07-08
tags: [sources, provenance]
---

# 原始材料登记表

登记规则:`status: active` 的来源存在于工作树;`status: external-local` 的来源来自本机其他项目路径,已被本知识库卡片吸收但原文不在当前工作树;`status: retired` 的来源已从工作树移除,唯一存档是 git 历史,用登记的 `archive` 命令恢复(见 [ADR-0002](../docs/adr/0002-retire-raw-sources-promote-evidence-layer.md))。锚点一律使用章节标题或编号(语义锚),不使用行号。

论文级证据与文献 run 成品不在本表登记,见 [../evidence/README.md](../evidence/README.md)。

## S-EMBODIED-DATA-FRAMEWORK

- 状态:external-local(2026-07-08 从 `/Users/ryan/Documents/具身数据` 迁移登记;源项目当前无 git commit)
- 本地来源:
  - 压缩卡:`/Users/ryan/Documents/具身数据/docs/knowledge/data-collection-framework.md`
  - 压缩卡:`/Users/ryan/Documents/具身数据/docs/knowledge/data-schema-quality-compliance.md`
  - 原始长文:`/Users/ryan/Documents/具身数据/materials/source/embodied_robot_no_body_data_collection_research.md`
- 类型:项目研究长文 / 数据采集框架 / 数据 schema 与合规规范
- 时间标记:原始素材登记日期 2026-06-01;迁移日期 2026-07-08
- 主题范围(章节锚):
  - 无目标机器人本体与无本体感觉数据:§数据采集框架卡/两种“无本体”含义
  - L0-L3 数据金字塔:§数据采集框架卡/L0-L3 数据金字塔
  - 技术路线优先级与规模参考:§数据采集框架卡/技术路线优先级、§快速规模参考
  - episode schema、存储、标注、质量、合规:§数据 Schema、质量与合规卡
- 适用:需要设计无目标机器人本体阶段的数据资产、episode schema、标注质量、授权合规或 L0/L1/L2/L3 路线时读取。

## S-LOGISTICS-HUB-SURVEY

- 状态:external-local(2026-07-08 从 `/Users/ryan/Documents/具身数据` 迁移登记;源项目当前无 git commit)
- 本地来源:
  - 压缩卡:`/Users/ryan/Documents/具身数据/docs/knowledge/logistics-hub-survey.md`
  - 压缩卡:`/Users/ryan/Documents/具身数据/docs/knowledge/field-evidence-checklist.md`
  - 压缩卡:`/Users/ryan/Documents/具身数据/docs/knowledge/scoring-and-acceptance.md`
  - 原始长文:`/Users/ryan/Documents/具身数据/materials/source/logistics_sorting_factory_embodied_data_survey_sop.md`
  - 交付表:`/Users/ryan/Documents/具身数据/deliverables/物流分拣工厂具身数据采集考察填写表.xlsx`
  - 演示版:`/Users/ryan/Documents/具身数据/deliverables/物流分拣工厂具身数据采集Hub考察SOP.pptx`
- 类型:现场考察 SOP / 项目经验 / 交付模板
- 时间标记:原始素材登记日期 2026-06-02;迁移日期 2026-07-08
- 主题范围(章节锚):
  - 物流 Hub 考察目标、必拍区域、岗位编号、考察节奏、当天交付:§物流 Hub 考察卡
  - 六类视频、访谈对象、尺寸测量、补拍触发、文件命名:§现场证据检查卡
  - 远程验收、Hub 条件评分、一票否决、岗位机器人替代优先级:§评分与验收卡
  - 完整执行细节、口播模板、最终报告模板:原始长文对应章节
- 适用:需要规划物流分拣现场考察、审核现场证据、给 Hub 或岗位评分、写考察报告或设计试采时读取。

## S-EA-QUESTIONS

- 状态:retired(2026-07-08 退役,git 存档)
- 存档:`git show 081e898:具身智能研究问题清单.md`
- 类型:研究问题清单 / 主题综述
- 时间标记:文中注明部分回答基于截至 2026-05-30 的公开资料
- 主题范围(章节锚):
  - 数据采集与数据质量:§一(Q1 数据采集范式、Q2 数据多样性与 Scaling Law、Q3 数据质量评估)
  - 传感器与多模态感知:§二(Q4 RGB/深度/点云/物理信息、Q5 触觉感知)
  - 采集硬件与设备路线:§三(Q6 单目/双目与空间感知、Q7 ARKit/SLAM 与视觉定位、Q8 Tracking 设备、Q9 UMI 与新型采集设备)
  - 跨本体与数据迁移:§四(Q10 人手数据迁移、Q11 跨本体预训练、Q12 Retargeting)
  - 模型与预训练:§五(Q13 Unified Model、Q14 开源模型与泛化、Q15 预训练评估)
  - 评测体系与世界模型:§六(Q16 具身智能评测、Q17 世界模型)
  - 产业落地与商业化:§七(Q18 ToB 落地)
  - 参考资料:§参考资料
- 适用:需要具身智能各议题的完整论述、问题列表、参考论文链接时,从 git 存档读取。

## S-ERR-COMPARE

- 状态:retired(2026-07-08 退役,git 存档)
- 存档:`git show 081e898:测绘误差观与大模型误差治理比较.md`
- 类型:跨学科对照 / 工程治理框架
- 主题范围(章节锚):
  - 核心结论:§核心结论
  - 学术角度差异:§一(误差对象/真值基础/理论框架/误差分布假设/学术目标)
  - 实践角度差异:§二(处理链路对比、错误定位、验收方式)、§三 核心对照表
  - 互补与迁移方法:§四-§六(误差预算、冗余检核、精度分级、误差传播、残差分析;大模型反哺测绘)
  - 红利与边界:§七 可能产生的红利、§八 不能机械照搬、§九 最终判断
  - 参考资料:§参考资料
- 适用:需要比较测绘误差理论和大模型误差治理、提炼可信系统方法时,从 git 存档读取。

## S-PROJECT-CONTEXT

- 状态:retired(2026-07-08 退役,git 存档)
- 存档:`git show 081e898:项目背景信息.md`
- 类型:项目背景 / 研究主线
- 适用:需要理解本项目为什么关注具身智能、误差治理和工程可信系统时,从 git 存档读取。项目当前共享语言见 [../CONTEXT.md](../CONTEXT.md)。
