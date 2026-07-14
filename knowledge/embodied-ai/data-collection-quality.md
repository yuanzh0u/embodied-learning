---
id: EA-DATA
title: 数据采集与数据质量
type: topic-card
domain: embodied-ai
updated: 2026-07-14
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §一 数据采集与数据质量(Q1-Q3)
  - id: S-EMBODIED-DATA-FRAMEWORK
    status: external-local
    locator: docs/knowledge/data-collection-framework.md; docs/knowledge/data-schema-quality-compliance.md
  - id: RUN-DATA-QUALITY-20260714
    file: ../../evidence/literature-review-近一年已发表论文中的具身智能数据质量-20260714-reader-v2/evidence.jsonl
    locator: EA-DQ-YEAR-READ-0001..0015
  - id: RUN-DATA-CONTRADICTIONS-20260714
    file: ../../evidence/literature-review-具身智能数据质量的主要矛盾-20260714-reader-v2/evidence.jsonl
    locator: EA-DQ-CONTRA-READ-0001..0015
  - id: RUN-WMDATA-20260714
    file: ../../evidence/literature-review-世界模型需要什么样的训练数据-20260714-reader-v2/evidence.jsonl
    locator: EA-WMDATA-READ-0001..0015
  - id: RUN-UMI-QUALITY-20260714
    file: ../../evidence/literature-review-近半年-umi-数据质量-20260714-reader-v2/evidence.jsonl
    locator: EA-UMI-READ-0001..0015
tags: [embodied-ai, data, collection, quality, scaling, umi, droid, ego4d, occlusion, l0-l3, episode, schema, target-conditioned, recovery]
aliases: [数据采集, 数据质量, UMI, DROID, Ego, Scaling Law, 遮挡率, L0-L3, 无本体采集, episode, 目标条件效用, 监督可靠性]
load_when:
  - 问题涉及机器人数据采集、轨迹质量、采集员规范、数据多样性或遮挡评估
  - 问题比较 UMI、Ego、DROID、遥操作、自然场景采集和实验室采集
  - 问题涉及无目标机器人本体阶段、L0/L1/L2/L3 数据金字塔、episode schema、标注质量或合规
  - 问题涉及轨迹筛选、质量分、坏数据利用、任务覆盖、失败恢复或异构数据监督
confidence: working
---

# 数据采集与数据质量

## Agent Load Hints

- Usually pair with: EA-HARDWARE, EA-SENSOR, EA-EVAL, EA-FIELD.
- Raw source needed when: 需要 1-18 个具体 Q&A、L0-L3 90 天路线、原始 schema 或合规条款的完整论述。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 区分候选池、可读全文和 accepted evidence；不要把 15 篇精读上限误解为检索池规模。

## 30 秒摘要

数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；高分筛选还必须保留任务、本体、场景和长尾覆盖。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。所有异构数据都应声明其可信监督字段，并以真实闭环收益作为最终验收。

## 关键判断

- VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
- 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
- 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
- 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
- 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- 数据质量最终要通过目标策略闭环收益验证，而不是只看数据是否“丰富”。
- 同一轨迹对不同目标任务可能有不同价值；质量排序应同时考虑目标效用、任务覆盖和有害轨迹风险。
- 质量粒度应从 episode 下探到 segment、action chunk、primitive 和 contact event；次优长轨迹中可能包含高价值恢复片段。
- 人类视频、UMI、真实机器人、仿真和生成数据能监督的字段不同，必须记录 supervision mask 或字段白名单。
- 数据集不能只收成功示教，还应系统记录 near-miss、失败、人工接管、恢复、进度和奖励信号。
- 世界模型训练数据必须暴露动作干预后的状态变化；静态图文或视觉重建不能替代动作忠实和接触动力学。
- 无目标机器人本体时，优先用 L0 人类视频覆盖任务语义，用 L1 手持 gripper/tool 采接近动作空间的轨迹，用 L2 仿真/合成放大覆盖和标注，用 L3 少量真实机器人数据做锚点校准。
- 动作表达在机器人形态未定时应优先采用 object-centric 或 end-effector-centric，不要过早绑定具体关节空间。
- 每条 episode 至少应能 join 任务、对象、场景、操作人、传感器、轨迹、标注、成功/失败和授权范围。
- 缺失 proprioception、关节状态或力控数据时应显式标为 missing 或 inferred，不应伪造成精确机器人状态。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 数据健康 | 时间同步误差、丢帧率、状态缺失、异常力、轨迹截断 |
| 多样性 | 任务数、场景数、物体数、初始位姿覆盖、操作者覆盖 |
| 动作一致性 | 动作分歧、速度范围、路径长度、夹爪开合时机 |
| 遮挡 | 关键对象可见率、关键点可见率、连续遮挡帧、关键阶段遮挡率 |
| 策略收益 | 少样本成功率、失败恢复率、跨场景成功率、负迁移检查 |
| 目标效用 | validation influence、目标分布相关性、样本移除后的闭环性能变化 |
| 覆盖均衡 | 任务/本体/夹爪/场景覆盖、coverage collapse、长尾占比 |
| 片段质量 | progress、停顿、振荡、过度纠正、primitive/transition 覆盖 |
| 监督可靠性 | 字段白名单、visibility/supervision mask、不可达率、仿真过滤通过率 |
| Schema 完整性 | `episode_id` join、相机内外参、轨迹字段、step segments、quality_score、授权字段 |
| 可重定向性 | 工作空间约束、速度/加速度约束、夹爪状态、接触事件、目标机器人锚点误差 |
| 合规 | consent、usage_scope、脱敏状态、商用许可、撤回机制、访问分权 |

## 适用边界

- 通用预训练：优先任务、场景、物体和语言描述多样性。
- 工业单任务：优先高精度、失败恢复、边界工况、目标工位真实数据。
- 单视角 RGB 可起步，但不宜单独支撑高可靠、接触丰富或遮挡严重任务。
- L0 纯视频适合任务库、步骤切分、affordance 和失败库，不适合直接当低层控制数据。
- L1 手持采集器适合早期高性价比示教，但仍需标定、动作表示和少量目标机器人锚点校准。
- 不存在跨任务通用的单一质量分；PSD、多样性、influence 或相似度都只能覆盖部分质量维度。
- 合成和世界模型数据可扩覆盖，但必须通过几何、动作、接触和真实闭环相关性验收。

## 证据锚点

- S-EA-QUESTIONS:1-6 覆盖采集范式、UMI/Ego/DROID、实验室与自然场景。
- S-EA-QUESTIONS:7-13 覆盖数据 scaling、多样性、一致性和采集员规范。
- S-EA-QUESTIONS:14-18 覆盖异构数据、遮挡量化和单视角限制。
- S-EMBODIED-DATA-FRAMEWORK:§数据采集框架卡 覆盖无目标机器人本体、L0-L3 数据金字塔、技术路线优先级和规模参考。
- S-EMBODIED-DATA-FRAMEWORK:§数据 Schema、质量与合规卡 覆盖最小 episode 字段、存储原则、必标字段、质量指标和合规边界。
- RUN-DATA-QUALITY-20260714：`EA-DQ-YEAR-READ-0001..0010`, `0015` 覆盖采集硬件塑形、任务条件效用、轨迹/chunk 质量、跨本体均衡、任务覆盖和组合式筛选。
- RUN-DATA-CONTRADICTIONS-20260714：`EA-DQ-CONTRA-READ-0001..0015` 共同支持规模—效用、视觉—可观测性、异构监督—字段可靠性、生成扩展—具身锚定和 episode—片段价值等矛盾；矛盾分类为跨事件 `inference`。
- RUN-WMDATA-20260714：`EA-WMDATA-READ-0001..0010`, `0015` 覆盖异构交互、监督掩码、关键事件、具身锚定合成数据、几何未来、失败修正和长程动作忠实。
- RUN-UMI-QUALITY-20260714：`EA-UMI-READ-0001..0004`, `0007..0015` 覆盖人体工学、多物理模态、3D tracking、数字遥操作边界、轨迹筛选和闭环质量定义。

## 待补问题

- 为不同任务族建立“有效轨迹成本”估算模板。
- 把遮挡率从像素级指标进一步连接到策略失败类型。
- 将 LeRobot/RLDS 兼容 episode schema 细化成字段模板。
- 为 L0/L1/L2/L3 建立不同任务族的采集量级和锚点比例建议。
- 建立跨任务、跨本体、跨采集设备的数据质量 benchmark。
- 将单个 `quality_score` 扩展为接口、健康、效用、覆盖、可执行性、训练利用和闭环收益字段。
