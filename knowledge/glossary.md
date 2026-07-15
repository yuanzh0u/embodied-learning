---
id: KB-GLOSSARY
title: 术语表
type: glossary
updated: 2026-07-15
tags: [glossary, embodied-ai, error-governance]
---

# 术语表

| 术语 | 工作定义 | 相关卡片 |
|---|---|---|
| 具身智能 | 智能体通过传感、行动和环境交互完成物理任务的能力体系。 | EA-* |
| 本体 | 机器人或采集设备的身体结构、自由度、末端执行器、传感器和控制接口。 | EA-XEMBODIMENT |
| 跨本体迁移 | 把一个本体上的数据、技能或策略迁移到另一个本体上。 | EA-XEMBODIMENT |
| Retargeting | 将人手或一种机器人动作映射到另一种机器人动作空间的过程。 | EA-XEMBODIMENT |
| 无目标机器人本体 | 尚未确定最终部署机器人，或无法长期占用目标机器人采集数据的项目阶段。 | EA-DATA, EA-FIELD |
| 无本体感觉数据 | 有外部观测但缺少关节角、力矩、触觉等 proprioception/action 记录的数据。 | EA-DATA, EA-SENSOR |
| L0 | 人类视频与任务语义层，用于覆盖任务、步骤、对象、成功/失败和视觉语言理解。 | EA-DATA, EA-FIELD |
| L1 | 机器人兼容示教层，用手持 gripper/tool 等采集接近机器人动作空间的数据。 | EA-DATA, EA-HARDWARE |
| L2 | 仿真与合成放大层，用于扩大覆盖、生成标注和构建评测。 | EA-DATA, EA-EVAL |
| L3 | 目标机器人锚点层，用少量真实机器人数据校准前面三层。 | EA-DATA, EA-XEMBODIMENT |
| Episode | 一次完整任务样本，包含开始条件、过程、结束条件、成功/失败和数据流。 | EA-DATA, EA-FIELD |
| 数据采集 Hub | 可长期稳定产出高价值具身数据、且支持试采和远程验收的现场或场站。 | EA-FIELD, EA-BIZ |
| Object-centric action | 以对象状态变化表达动作，而不是直接绑定机器人关节。 | EA-DATA, EA-XEMBODIMENT |
| End-effector-centric action | 以机器人末端位姿或 delta pose 表达动作。 | EA-DATA, EA-XEMBODIMENT |
| Anchor data | 少量目标机器人真实执行数据，用于校准和闭环验证跨本体或无本体采集数据。 | EA-DATA, EA-XEMBODIMENT |
| Ego-centric behavior data | 人类第一视角视频及从中恢复的手—物轨迹、视点运动和任务结构；主要提供行为先验，不天然包含完整机器人动作、接触和奖励监督。 | EA-DATA, EA-XEMBODIMENT, EA-MODEL, EA-SENSOR |
| 可执行监督 | 已核验坐标、尺度、动作接口、可达性、接触和动力学约束，可供目标机器人训练或闭环评测使用的监督。 | EA-DATA, EA-XEMBODIMENT |
| 目标条件效用 | 数据质量相对于目标任务、目标分布和目标策略的实际贡献；同一轨迹在不同目标下可能有不同质量排序。 | EA-DATA |
| 监督可靠性 | 一类数据对某个字段能否提供可信真值的等级，例如人类视频可监督任务结构但通常不能直接监督机器人控制命令。 | EA-DATA, EA-4D |
| Supervision mask | 显式标记每类异构数据哪些字段可参与监督、哪些字段缺失或不可信的掩码。 | EA-DATA, EA-4D |
| Candidate pool | 多轮检索、去重和初筛后的候选论文集合，用来描述覆盖范围，不代表已经全文阅读。 | KB-LIT-REVIEWS |
| Full-text eligible | 已取得完整、可解析、可定位原文上下文的非 OCR 全文；摘要、残缺 PDF 和扫描件不属于当前项目的可用全文。 | KB-LIT-REVIEWS |
| Paper note | 对单篇论文 map read / deep read 后形成的结构化精读记录，包含方法、结果、限制、适用边界和原文证据卡。 | KB-LIT-REVIEWS |
| Claim-support audit | 检查 paper note 中的主张是否被对应全文 locator 与 source context 支持的审计。 | KB-LIT-REVIEWS |
| Accepted evidence event | 从通过审计的 paper note 投影出的正式论文证据记录，具有当前有效 run 集合中全局唯一的 event ID。 | KB-LIT-REVIEWS |
| Review packet | 汇总综述范围、证据分布、共识、限制和缺口的中预算审计视图，不等同于读者成稿。 | KB-LIT-REVIEWS |
| Action semantics | 控制命令在坐标系、频率、归一化、控制器和机器人本体条件下对应的物理含义。 | EA-ALIGN, EA-XEMBODIMENT |
| 可观测性 | 系统能否从传感器中观察到完成任务所需的关键状态。 | EA-SENSOR |
| VPR | Visual Place Recognition，按图像外观与结构召回地点候选的定位前端；高召回不等于最终位姿可恢复。 | EA-VLOC, EA-SENSOR |
| 相机重定位 | 在已有地图或参考集合中估计相机 6DoF 位姿，通常需要候选召回、几何验证与位姿求解。 | EA-VLOC, EA-HARDWARE |
| 可恢复域 | 在给定初始化、地图覆盖和场景条件下，定位或位姿细化仍可可靠收敛的工作范围。 | EA-VLOC, EA-EVAL |
| 风险—覆盖 | 联合衡量已接受预测的错误风险和系统愿意给出预测的查询覆盖率，防止用全局拒识制造虚假的低风险。 | EA-VLOC, EA-EVAL |
| 触觉 | 指尖或接触表面的局部压力、剪切、滑移、形变、纹理等接触信息。 | EA-SENSOR |
| 力/力矩 | 通常指腕部或关节层面的低维全局受力信息。 | EA-SENSOR |
| 最后一厘米 | 机器人从视觉定位过渡到接触闭环的精细操作阶段。 | EA-BIZ, EA-SENSOR |
| 开放环评测 | 给定离线观测历史，评估模型预测动作是否接近专家动作。 | EA-EVAL |
| 闭环评测 | 让机器人真实或仿真执行动作，并评估执行后果。 | EA-EVAL |
| 世界模型 | 预测动作如何改变未来状态、视觉或物理环境的模型。 | EA-EVAL |
| 4D 时空推理 | 对三维世界中的对象、机器人、接触和关系如何随时间演化进行表征、预测与决策。 | EA-4D |
| Action fidelity | 世界模型或数据中的未来变化是否忠实响应给定动作，而不只是生成视觉上合理的结果。 | EA-4D, EA-EVAL |
| World-model admissibility | 世界模型是否具备作为策略评估、拒绝或安全裁决依据的可采信性，包括动作、物理、长程和失败响应验证。 | EA-EVAL, ERR-EMBODIED |
| 感知误差 | 第一处可证伪偏离发生在真实世界到状态表征之间，例如不可观测、错位、标定或记录错误。 | ERR-EMBODIED, EA-SENSOR |
| 认知误差 | 状态表征足够，但任务、约束、阶段、计划或未来后果判断发生错误。 | ERR-EMBODIED, EA-ALIGN |
| 第一处可证伪偏离点 | 世界→表征→计划→控制→后果链上最早能被证据证明偏离预期的环节。 | ERR-EMBODIED, ERR-PATTERN |
| 误差预算 | 将系统错误拆解到数据、传感器、模型、控制、工具、评测等环节。 | ERR-PATTERN |
| 冗余检核 | 使用多源证据、多个工具、独立检查点或人工复核验证关键结论。 | ERR-PATTERN |
| 残差分析 | 分析输出与观测、证据、约束或验收标准之间的偏离结构。 | ERR-PATTERN |
| 适用边界 | 系统在哪些任务、场景、精度和风险等级下可以使用。 | ERR-COMPARE, ERR-PATTERN |
