---
id: EA-SENSOR
title: 传感器与多模态感知
type: topic-card
domain: embodied-ai
updated: 2026-07-26
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §二 传感器与多模态感知(Q4-Q5)
  - id: RUN-TACTILE-WM-20260714
    file: ../../evidence/literature-review-触觉世界模型-20260714-reader-v2/evidence.jsonl
    locator: EA-TWM-READ-0001..0015
  - id: RUN-SENSOR-ERROR-20260714
    file: ../../evidence/literature-review-具身传感器感知误差-20260714-reader-v2/evidence.jsonl
    locator: EA-SENSORERR-READ-0001..0015
  - id: RUN-UMI-QUALITY-20260714
    file: ../../evidence/literature-review-近半年-umi-数据质量-20260714-reader-v2/evidence.jsonl
    locator: EA-UMI-READ-0001..0015
  - id: RUN-EGO-DATA-20260715
    file: ../../evidence/literature-review-ego-centric-数据在具身模型训练中的问题与困难-20260715/evidence.jsonl
    locator: EA-EGO-2026-0005..0006; EA-EGO-2026-0015..0018; EA-EGO-2026-0020
  - id: RUN-VLOC-20260715
    file: ../../evidence/literature-review-近一年图像视觉定位方法的发展与挑战-20260715/evidence.jsonl
    locator: EA-VLOC-2026-0011..0013; EA-VLOC-2026-0015
  - id: RUN-LOCOMANIP-20260719
    file: ../../evidence/literature-review-近一年-loco-manipulation-研究进展-20260719/evidence.jsonl
    locator: EA-LOCOMANIP-2026-0012; EA-LOCOMANIP-2026-0014; EA-LOCOMANIP-2026-0017..0018; EA-LOCOMANIP-2026-0021
  - id: RUN-MULTIMODAL-TRAINING-20260720
    file: ../../evidence/literature-review-近一年触觉-力觉-视觉-语言等多模态数据在具身机器人训练方法中的演进-20260720/evidence.jsonl
    locator: EA-TWM-READ-0001..0014; EA-SENSORERR-READ-0004; EA-SENSORERR-READ-0007; EA-SENSORERR-READ-0010..0012; EA-LOCOMANIP-2026-0012; EA-LOCOMANIP-2026-0021
  - id: RUN-TACTILE-YEAR-20260720
    file: ../../evidence/literature-review-近一年触觉在具身机器人领域的发展-20260720/evidence.jsonl
    locator: EA-TACTILE-2026-0001..0002; EA-TWM-READ-0001..0015; EA-SENSORERR-READ-0001; EA-SENSORERR-READ-0010; EA-SENSORERR-READ-0012; EA-LOCOMANIP-2026-0012; EA-LOCOMANIP-2026-0021; EA-UMI-READ-0002; EA-UMI-READ-0015
  - id: RUN-FORCE-SENSE-20260720
    file: ../../evidence/literature-review-近半年力觉在具身机器人领域的发展-20260720/evidence.jsonl
    locator: EA-TWM-READ-0001..0008; EA-TWM-READ-0010..0012; EA-TWM-READ-0014; EA-SENSORERR-READ-0001; EA-SENSORERR-READ-0010; EA-SENSORERR-READ-0012; EA-LOCOMANIP-2026-0012; EA-LOCOMANIP-2026-0021
  - id: RUN-PRETRAIN-DATA-SOURCES-20260726
    file: ../../evidence/literature-review-近一年具身智能预训练模型对数据源与采集参数的要求-20260726/evidence.jsonl
    locator: EA-PRETRAIN-DATA-2026-0003..0006; EA-EGO-2026-0014..0018; EA-UMI-READ-0004; EA-TACTILE-2026-0001..0002
tags: [embodied-ai, sensors, multimodal, function-rate-alignment, rgb, point-cloud, tactile, force, force-torque, proprioception, perception-error, tactile-world-model, contact-execution-stack, ego-centric, visual-localization]
aliases: [传感器, 多模态感知, 功能—时标对齐融合, 触觉, 力觉, 力控, 六维力力矩, 接触执行栈, 点云, 3D, RGB, 触觉世界模型, 感知误差, 第一视角感知, VPR]
load_when:
  - 问题涉及 RGB、深度、点云、触觉、力/力矩、接触状态、材料属性或传感器组合
  - 问题涉及传感器感知误差、模态融合污染、触觉未来预测、漂移磨损或世界模型接触状态
  - 问题涉及第一视角相机自运动、手物轨迹恢复、视觉地点识别或几何先验
  - 问题涉及触觉/力觉训练方法、HT-Bench、接触事件、选择性融合、高低频控制或跨传感器泛化
confidence: working
---

# 传感器与多模态感知

## Agent Load Hints

- Usually pair with: EA-DATA, EA-HARDWARE, EA-BIZ, EA-4D, ERR-EMBODIED.
- Raw source needed when: 需要触觉标准化、触觉任务清单或具体论文编号。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 进入触觉、传感器误差或 UMI run，再按任务选择 paper note，避免默认加载全部多模态论文。

## 30 秒摘要

视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；腕部六维力/力矩提供低维全局载荷，触觉提供高维局部接触场，两者不能互换。最新综合更支持按功能和时标选择性耦合：视觉/语言负责慢速全局语义与计划，触觉/力觉进入快速接触反馈，动作条件世界模型负责预测与验证。目标不是堆传感器，而是形成“同步数据—接触表征—动作条件预测—高频纠偏—安全过程评测”的接触执行栈，并证明每个模态在闭环中产生可验证收益且不污染已有先验。

## 关键判断

- RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
- 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
- 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
- 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
- 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- 触觉数据集要把磨损、漂移、换件和跨实例泛化当作数据集的一部分。
- 传感器误差应分为观测、接触、融合和评测四层，并记录每层的残差与版本信息。
- 触觉是稀疏、事件驱动信号；接触门控、时间同步和 action horizon 决定融合是否有效。
- 无约束触觉注入可能污染视觉 dynamics model，多模态不是无条件增益。
- 全局异常检测不足以代表任务风险；监控应关注当前 action chunk 的局部执行走廊。
- 触觉世界模型只有进入 MPC、动作验证、anticipatory prior 或反射控制，才证明闭环价值。
- Ego-centric wrist trajectory 与相机自运动天然耦合；不统一参考系和置信度时，视点变化会被误写成动作监督。
- RGB-only 手腕/手物标签存在 fidelity ceiling，自动恢复结果应携带不确定性，并经过遮挡、深度、接触和物理可行性过滤。
- VPR 相似度不足以单独处理感知别名；深度/共视几何能提供补充，但安全拒识必须与接受覆盖一起报告。
- 动态 loco-manipulation 中，触觉可从操作侧附加观测升级为全身控制变量：它应同时影响夹爪调节、手臂轨迹和身体稳定，而不只在高层做接触分类。
- 地形、目标物体、机器人自身空间状态和执行器故障都属于全身操作的任务状态；只看 RGB 与本体状态会遗漏支撑面、滑移和退化可达域。
- 多模态训练的基本单元应从“同时间戳帧”提升为 approach、contact、slip、release、recovery 等接触事件链；同步只是底线，功能与控制频率决定如何融合。
- 多模态融合应有方向性：触觉可以约束动作和接触预测，但无约束地反向注入视觉 dynamics 可能造成模态污染；contact gate、非对称注意力和快慢层级需要独立消融。
- 腕部六维力/力矩适合表达全局载荷和先行条件，局部触觉力场适合表达接触位置、滑移与形变；两者应在空间标定与时间角色上分别建模。
- HT-Bench 把全手触觉—第一视角配对数据扩展到约 1,000 万 RGB 帧、780 万触觉帧和 226 项任务，但当前只证明表征评测价值，不能外推为真实机器人闭环收益。
- 触觉/力觉接入部署系统时，应贯通动作条件预测、候选动作验证和失败附近纠偏；只提高触觉重建或分类分数不构成控制价值证据。
- 跨数据源可使用不同视觉/深度采样率，但必须保存实际采样时间、时钟源、丢帧/抖动和跨模态对齐误差；训练 action chunk 应按物理时长对齐，不按固定帧数假设同速。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 3D 感知 | 深度噪声、位姿误差、遮挡恢复率、空间任务成功率 |
| 触觉 | 接触检测延迟、滑移检测率、压力分布稳定性、跨传感器实例性能 |
| 力/力矩 | 过力次数、接触阈值误报、力控稳定性、异常碰撞检测 |
| 多模态融合 | 模态 dropout 鲁棒性、缺失模态退化、闭环成功率提升 |
| 对齐与融合 | 时钟残差、标定投影误差、接触事件完整率、contact gate、模态污染消融 |
| 过程安全 | Safety Success、滑移/掉落、形变、过力、恢复率 |
| 长期维护 | 漂移曲线、磨损、换件重标定、跨传感器实例退化 |
| 接触表征 | 空间接触结构、跨模态对齐、时间动态、任务级 OOD、跨硬件单元退化 |
| 第一视角轨迹 | 参考系残差、wrist/object pose recovery、遮挡通过率、深度/接触一致性 |
| 视觉定位前端 | 分条件 Recall@K、视觉重叠、感知别名率、风险—覆盖、连续失定位时长 |

## 适用边界

- 开放空间、刚体、视觉可见任务：视觉模型可能已足够形成可用策略。
- 透明/反光/遮挡/软物/精密插入/易碎物：需要 3D、触觉、力控或柔顺执行补充。
- 多模态方案必须按任务收益验证，否则会增加标定、带宽、同步和维护成本。
- 触觉或力觉结果通常硬件特定，不能从单一传感器和小规模任务直接外推为通用能力。
- 世界模型预测视觉逼真不等于接触和动作响应正确，必须经过 admissibility 与真实闭环验证。
- Ego 标签恢复和 VPR 拒识的结论依赖相机、场景重复度与参考覆盖；跨环境部署需要重新校准阈值和可恢复域。
- HT-Bench 目前不覆盖指尖光学触觉、腕部力/力矩、皮肤 taxel 和非手部本体，也没有真实机器人闭环操作；不能将其表征分数解释为通用触觉控制能力。
- 力觉与触觉结论高度依赖传感器形态、安装位置、标定和控制频率；跨硬件迁移必须重新验收同步、空间映射和维护漂移。

## 证据锚点

- S-EA-QUESTIONS:19-22 覆盖 RGB、3D、点云和物理模态。
- S-EA-QUESTIONS:23-29 覆盖触觉与视觉、力、pose 的关系，以及触觉标准化。
- RUN-TACTILE-WM-20260714：`EA-TWM-READ-0001..0008`, `0010..0015` 覆盖同步多模态序列、视觉—触觉—动作未来、显式接触几何、力/力矩先验、高低频控制分层和推理期动作验证。
- RUN-SENSOR-ERROR-20260714：`EA-SENSORERR-READ-0001..0012`, `0014..0015` 覆盖触觉失败修正、局部风险走廊、融合污染、安全过程、admissibility、空间对齐、置信度和恢复数据。
- RUN-UMI-QUALITY-20260714：`EA-UMI-READ-0001..0005`, `0015` 支持人体工学、力/触觉/深度/位姿、LiDAR-centric 3D sensing 和软物体多视角可观测性。
- RUN-EGO-DATA-20260715：`EA-EGO-2026-0005..0006`, `0015..0018`, `0020` 支持单目几何与遮挡边界、相机—手腕参考系解耦、自动标签 fidelity、主动视点条件和接触结构过滤。
- RUN-VLOC-20260715：`EA-VLOC-2026-0011..0013`, `0015` 支持风险—覆盖、参考分布条件、深度几何蒸馏和地理长尾不等于视觉难度。
- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0012`, `0021` 支持触觉命令跟踪和触觉驱动全身抓持调节；`0014` 支持地形感知与接触面相对目标；`0017..0018` 显示故障状态与机载深度相对动捕的真机性能差距。
- RUN-MULTIMODAL-TRAINING-20260720：`EA-TWM-READ-0001..0014`, `EA-SENSORERR-READ-0004`, `0007`, `0010..0012` 与 `EA-LOCOMANIP-2026-0012`, `0021` 共同支持按功能/时标选择性耦合、接触事件、模态污染和快慢反馈分层；这些结论属于跨 run synthesis。
- RUN-TACTILE-YEAR-20260720：`EA-TACTILE-2026-0001..0002` 支持 HT-Bench 的数据规模、空间/跨模态/时间/OOD 评测与“表征不等于闭环”的边界；其余事件复用已审计触觉世界模型、传感器误差、Loco 与 UMI run。
- RUN-FORCE-SENSE-20260720：`EA-TWM-READ-0004`, `0006..0007`, `0014`, `EA-SENSORERR-READ-0001`, `0012`, `EA-LOCOMANIP-2026-0012`, `0021` 支持六维载荷—局部接触分工、动作验证、高频纠偏和全身低层反馈；该 run 没有新增论文级 event。

## 待补问题

- 建立不同任务族的最小传感器组合建议。
- 补一份触觉数据标准字段表。
- 把“最后一厘米”拆成视觉、力控、触觉、末端执行器和柔顺控制的接口规范。
- 建立跨传感器实例、磨损和维护周期的长期基准。
- 建立贯通 Ego 标签恢复置信度、VPR 可恢复域与机器人闭环失败的联合校准协议。
- 建立接触事件 schema、硬件 ID、时钟、标定和换件维护的统一记录规范。
- 建立触觉/力觉表征提升到策略排序、快速纠偏和真实闭环收益的逐级验收基准。
