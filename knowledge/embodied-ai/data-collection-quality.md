---
id: EA-DATA
title: 数据采集与数据质量
type: topic-card
domain: embodied-ai
updated: 2026-07-27
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
  - id: RUN-EGO-DATA-20260715
    file: ../../evidence/literature-review-ego-centric-数据在具身模型训练中的问题与困难-20260715/evidence.jsonl
    locator: EA-EGO-2026-0001..0020; 6 reused reader-v2 events
  - id: RUN-DATA-CONTAMINATION-20260715
    file: ../../evidence/literature-review-近一年论文中的具身数据污染问题-20260715/evidence.jsonl
    locator: EA-CONTAM-2026-0001..0015
  - id: RUN-MULTIMODAL-TRAINING-20260720
    file: ../../evidence/literature-review-近一年触觉-力觉-视觉-语言等多模态数据在具身机器人训练方法中的演进-20260720/evidence.jsonl
    locator: EA-ALIGN-READ-0007..0008; EA-ALIGN-READ-0011..0012; EA-EGO-2026-0003..0004; EA-EGO-2026-0007..0009; EA-EGO-2026-0016..0020; EA-TWM-READ-0001; EA-TWM-READ-0005..0006; EA-TWM-READ-0008; EA-TWM-READ-0012
  - id: RUN-TACTILE-YEAR-20260720
    file: ../../evidence/literature-review-近一年触觉在具身机器人领域的发展-20260720/evidence.jsonl
    locator: EA-TACTILE-2026-0001..0002; EA-TWM-READ-0001; EA-UMI-READ-0002; EA-UMI-READ-0015
  - id: RUN-PRETRAIN-DATA-SOURCES-20260726
    file: ../../evidence/literature-review-近一年具身智能预训练模型对数据源与采集参数的要求-20260726/evidence.jsonl
    locator: EA-PRETRAIN-DATA-2026-0001..0006; EA-DQ-YEAR-READ-0003; EA-DQ-YEAR-READ-0008..0010; EA-DQ-YEAR-READ-0015; EA-EGO-2026-0007..0009; EA-UMI-READ-0004
  - id: RUN-SPATIAL-DATA-ROBOT-AV-20260727
    file: ../../evidence/literature-review-近一年空间数据生产难点及具身机器人与智能驾驶数据难点异同-20260727/evidence.jsonl
    locator: EA-SPATIAL-2026-0001..0009; 10 reused reader-backed events
tags: [embodied-ai, data, collection, quality, multimodal, contact-event, hardware-provenance, synchronization, contamination, poisoning, backdoor, provenance, deduplication, scaling, umi, droid, ego4d, occlusion, l0-l3, episode, schema, target-conditioned, recovery, spatial-data, autonomous-driving, closed-loop]
aliases: [数据采集, 数据质量, 多模态数据, 接触事件, 硬件谱系, 数据污染, 数据投毒, 后门, 数据谱系, 语义泄漏, UMI, DROID, Ego, Scaling Law, 遮挡率, L0-L3, 无本体采集, episode, 目标条件效用, 监督可靠性, 空间数据, 智能驾驶数据]
load_when:
  - 问题涉及机器人数据采集、轨迹质量、采集员规范、数据多样性或遮挡评估
  - 问题比较 UMI、Ego、DROID、遥操作、自然场景采集和实验室采集
  - 问题涉及无目标机器人本体阶段、L0/L1/L2/L3 数据金字塔、episode schema、标注质量或合规
  - 问题涉及轨迹筛选、质量分、坏数据利用、任务覆盖、失败恢复或异构数据监督
  - 问题涉及数据污染、近重复、时间错位、训练评测泄漏、VLA 后门、模型供应链或生成扩增风险
  - 问题涉及视觉—触觉—力觉同步、接触事件切分、传感器硬件 ID、标定版本或跨实例维护
  - 问题比较具身机器人与智能驾驶的空间数据生产、长尾覆盖、闭环验收或合成数据边界
confidence: working
---

# 数据采集与数据质量

## Agent Load Hints

- Usually pair with: EA-HARDWARE, EA-SENSOR, EA-EVAL, EA-FIELD.
- Raw source needed when: 需要 1-18 个具体 Q&A、L0-L3 90 天路线、原始 schema 或合规条款的完整论述。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 区分候选池、可读全文和 accepted evidence；不要把 15 篇精读上限误解为检索池规模。

## 30 秒摘要

数据采集不是单纯堆轨迹，而是硬件、同步、标定、动作语义、元数据、采集员反馈和质量审计组成的工程体系。数据质量不是样本的全局静态属性，而是相对目标任务和目标策略的效用；数据污染则是来源、时间、任务、模型版本和评测边界的关系失真，治理必须贯穿采集、训练、生成和闭环评测。无目标机器人本体阶段可用 L0-L3 数据金字塔积累语义、可重定向轨迹、仿真覆盖和失败库，但最终仍需少量目标机器人数据校准可执行性。对视觉—触觉—力觉数据，同时间戳帧只是最低层记录，真正的训练单元还应保留 approach、contact、slip、release、recovery 等事件链，并记录传感器/硬件 ID、时钟、标定和换件历史。所有异构数据都应声明可信监督字段，以动作条件状态变化和真实闭环收益验收；规模化触觉数据不自动等于跨硬件通用性或控制收益。

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
- Ego-centric 视频的主要数据损失发生在“行为观测→可执行监督”转换：相机自运动、遮挡与尺度会污染轨迹，视频又通常缺失 gripper、force、contact 和 reward。
- Ego-centric 规模收益以动作接口和目标本体锚定为条件；只扩大 raw video 而不控制伪标签与可执行性，可能出现数据增多、真实机器人性能下降。
- 接触几何与物理可行性应作为独立质量闸门，不能用视觉相似度或自由空间姿态误差替代。
- 具身去重应把视觉场景相似与轨迹相似分开核验；片段数增长不等于场景、任务或动作覆盖增长。
- 训练语料去重与训练—评测隔离是两项不同治理任务；无字节级重复也可能因场景、布局和指令—动作映射过近产生语义泄漏。
- 污染审计至少需要 episode、action chunk、关键事件和控制 tick 四级视图，并在多模态数据上验证时间同步与动作—状态一致性。
- 污染会沿基础模型、适配模块、检查点与世界模型生成链路持续或二次激活；下游只使用干净数据微调不能单独证明链路无污染。
- 后门防御应把检测、因果定位和恢复后的能力损失分开计账，并明确覆盖的触发面与威胁模型。
- 多模态数据切分应同时保留物理事件和控制阶段；仅按固定帧数抽样会丢失接触、滑移、释放和恢复等稀疏高价值信号。
- 每条多模态 episode 应记录传感器型号/序列号、安装位置、量程、采样率、时钟源、内外参/力标定、固件和换件维护，避免把硬件漂移误当任务变化。
- 成功示范不足以训练接触纠错；near-miss、过力、滑移、物体变形、人工接管和恢复轨迹应作为独立事件与监督字段入库。
- HT-Bench 的大规模同步视觉—触觉数据证明了表征规模化可行性，但跨实例、长期维护和真实机器人闭环仍需目标硬件数据与独立验收。
- 通用预训练的多样性应投向任务、场景、物体、视点、行为和本体覆盖；一致性应投向坐标、时间、动作语义、机位、标定和监督可靠性等数据契约。
- 采集设备和原生规格可以异构，但应保留小而高保真的目标机器人锚点集，用对齐观测几何、动作接口和真实闭环校准广泛数据池。
- 空间数据的稀缺不是像素或点云总量不足，而是缺少可用于决策的时空真值：坐标与时间可追溯、任务关键隐状态可观、动作/意图/拓扑语义正确、失败长尾充分且后果可闭环复验。
- 具身机器人最难生产的是本体相关的“执行真值”，包括接触、力、滑移、形变、动作可执行性和失败恢复；智能驾驶最难生产的是 ODD 相关的“覆盖真值”，包括地图拓扑与更新、地理/天气覆盖、稀有多体风险和可反应闭环。

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
| 污染与谱系 | 来源/版本哈希、场景—轨迹近重复、跨库交集、时间戳缺口、动作—状态一致性、训练—评测结构重合 |
| 投毒与恢复 | clean success、触发 ASR/失效率、检出率、误报率、恢复后能力损失、跨检查点持久性 |
| 多模态同步 | 跨模态时间残差、丢帧、接触事件完整率、动作—状态因果顺序、时钟漂移 |
| 硬件谱系 | 传感器/固件/标定版本、换件次数、跨实例退化、重标定工时、长期漂移 |
| 空间真值有效性 | 坐标/时间残差、关键隐状态可观率、语义/动作字段正确率、风险或恢复事件密度、闭环可复验率 |

## 适用边界

- 通用预训练：优先任务、场景、物体和语言描述多样性。
- 工业单任务：优先高精度、失败恢复、边界工况、目标工位真实数据。
- 单视角 RGB 可起步，但不宜单独支撑高可靠、接触丰富或遮挡严重任务。
- L0 纯视频适合任务库、步骤切分、affordance 和失败库，不适合直接当低层控制数据。
- L1 手持采集器适合早期高性价比示教，但仍需标定、动作表示和少量目标机器人锚点校准。
- 不存在跨任务通用的单一质量分；PSD、多样性、influence 或相似度都只能覆盖部分质量维度。
- 合成和世界模型数据可扩覆盖，但必须通过几何、动作、接触和真实闭环相关性验收。
- 当前后门论文证明的是多种攻击面在特定权限、触发器与实验设置下成立，不能据此外推现实数据供应链中的发生率。
- 入库前清洗不能替代基础模型、微调模块、生成轨迹和最终政策的端到端复验。
- 大规模同步数据不等于跨传感器通用化；硬件实例、标定、磨损和维护分布变化必须单独报告。
- 表征 benchmark 的提升不能外推为闭环操作收益，除非同一数据/模型在策略排序、纠偏或真实执行中通过验收。
- 机器人与智驾可共享对齐、谱系、遮挡、长尾和闭环质量框架，但不能共享一个无条件的质量分：机器人数据须绑定本体与控制器，智驾数据须绑定 ODD、地图版本与交通交互分布。

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
- RUN-EGO-DATA-20260715：`EA-EGO-2026-0001..0020` 覆盖动作标签不完备、相机运动与遮挡、跨本体重定向、接触/物理可行性、规模—噪声冲突和目标机器人锚定；“六层可执行监督数据栈”是基于这些事件的跨论文 `inference`。
- RUN-DATA-CONTAMINATION-20260715：`EA-CONTAM-2026-0001..0010` 覆盖状态/视觉/语言/动作窗后门、持久污染、防御边界与世界模型二次激活；`0011..0015` 覆盖视觉—轨迹联合去重、同步与动作—状态检核、任务覆盖、片段级价值和结构化选择。
- RUN-MULTIMODAL-TRAINING-20260720：`EA-ALIGN-READ-0007..0008`, `0011..0012`, `EA-EGO-2026-0003..0004`, `0007..0009`, `0016..0020`, `EA-TWM-READ-0001`, `0005..0006`, `0008`, `0012` 支持接触事件、同步、监督掩码、硬件/本体锚定和失败数据；结论为跨 run synthesis。
- RUN-TACTILE-YEAR-20260720：`EA-TACTILE-2026-0001..0002` 支持约 1,000 万 RGB 帧、780 万触觉帧、226 项任务的同步数据规模和“表征不等于闭环”边界；复用事件补充多物理模态与长期维护条件。
- RUN-SPATIAL-DATA-ROBOT-AV-20260727：`EA-SPATIAL-2026-0001..0009` 支持智驾中的跨模态自动标注、占用生成、地图生产/维护、数据格式碎片、危险场景合成与风险语义长尾；同 run 的 10 条复用事件支持机器人中的坐标/本体对齐、遮挡/接触可观性、失败恢复和稀疏视角 4D 数据生成。机器人“执行真值”与智驾“覆盖真值”的二分是跨论文 `inference`。

## 待补问题

- 为不同任务族建立“有效轨迹成本”估算模板。
- 把遮挡率从像素级指标进一步连接到策略失败类型。
- 将 LeRobot/RLDS 兼容 episode schema 细化成字段模板。
- 为 L0/L1/L2/L3 建立不同任务族的采集量级和锚点比例建议。
- 建立跨任务、跨本体、跨采集设备的数据质量 benchmark。
- 将单个 `quality_score` 扩展为接口、健康、效用、覆盖、可执行性、训练利用和闭环收益字段。
- 建立 Ego-centric 数据的有效小时指标，显式计入自动标签通过率、人工重定向工时、物理过滤损耗和目标机器人示教替代率。
- 建立可控污染 benchmark，覆盖精确/语义近重复、时间错位、任务覆盖坍缩、多触发面后门和世界模型二次激活，并统一报告检出、误报、恢复与闭环代价。
- 将接触事件、硬件身份、时钟、标定、换件和维护历史补入 episode schema。
- 建立触觉/力觉数据从表征、策略排序到快速纠偏与真实闭环的逐级价值审计。
