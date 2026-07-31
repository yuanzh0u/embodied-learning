---
id: EA-HARDWARE
title: 采集硬件与设备路线
type: topic-card
domain: embodied-ai
updated: 2026-07-26
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §三 采集硬件与设备路线(Q6-Q9)
  - id: RUN-UMI-QUALITY-20260714
    file: ../../evidence/literature-review-近半年-umi-数据质量-20260714-reader-v2/evidence.jsonl
    locator: EA-UMI-READ-0001..0015
  - id: RUN-VLOC-20260715
    file: ../../evidence/literature-review-近一年图像视觉定位方法的发展与挑战-20260715/evidence.jsonl
    locator: EA-VLOC-2026-0001..0010; EA-VLOC-2026-0014
  - id: RUN-PRETRAIN-DATA-SOURCES-20260726
    file: ../../evidence/literature-review-近一年具身智能预训练模型对数据源与采集参数的要求-20260726/evidence.jsonl
    locator: EA-PRETRAIN-DATA-2026-0003..0006; EA-EGO-2026-0014..0018; EA-UMI-READ-0004
tags: [embodied-ai, hardware, monocular, stereo, arkit, slam, tracking, umi, glove, visual-localization, localization-map]
aliases: [采集硬件, 单目, 双目, ARKit, SLAM, Tracking, UMI, 指套, 手套, 定位地图, SCR, 3DGS]
load_when:
  - 问题涉及采集设备选型、单目双目、ARKit、SLAM、VR tracking、UMI 或指套式设备
confidence: working
---

# 采集硬件与设备路线

## Agent Load Hints

- Usually pair with: EA-DATA, EA-SENSOR.
- Raw source needed when: 需要具体设备路线的完整问答或参考资料。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 进入 UMI run；设备选型要同时核验采集质量、人体工学和闭环收益。

## 30 秒摘要

采集硬件不会收敛到单一设备，而会收敛到少数数据协议和接口范式。单目适合规模化起步，双目/多目和 LiDAR 适合几何、遮挡、动态或弱纹理场景；ARKit/SLAM/Tracking 可作低成本位姿输入但不能当工业真值。视觉定位还需要把点云、SCR、3DGS 或参考图像集合视为有构建、存储、更新、隐私和可恢复域成本的“地图硬件”。UMI 的数据质量从采集器设计开始：人体工学、力分布、重量、刚度、传感器组合和部署端同构程度会直接改变示教速度、损伤、负担和可执行性。

## 关键判断

- 具身采集不必须双目，关键看任务是否依赖稳定几何、相对深度和遮挡恢复。
- 行业偏好单目来自工程经济性：便宜、易标定、低带宽、易维护、适配视觉预训练。
- 双目落地瓶颈是标定同步、弱纹理/反光匹配失败、深度噪声融合和系统成本。
- ARKit 可用于低成本 VIO、位姿跟踪和快速原型，但不适合作唯一计量真值。
- VR/AR tracking 是低成本人机输入，需记录置信度、丢踪事件和时间戳质量。
- UMI 的核心价值是把自然场景人类示教转成机器人可学习的数据闭环。
- 视觉/轨迹型 UMI 对接触丰富任务通常缺力、触觉、内部抓力和外部 wrench，应按任务补充物理模态。
- 单目 SLAM 型 UMI 在遮挡、动态、弱纹理和 tracking failure 场景风险高，LiDAR-centric 3D sensing 可扩展可采任务分布。
- 灵巧操作若采集端和部署端共享末端、传感器与动作空间，可减少 retargeting 失真。
- 3DGS/SCR 等神经地图可以降低某些建图或查询成本，但渲染质量不等于几何可定位性，地图表示必须按对应唯一性和位姿可恢复性验收。
- 3DGS 位姿细化通常是局部优化，前端 Top-K 召回、初始位姿和局部几何质量仍是系统级依赖。
- 近一年预训练证据不支持单一摄像头分辨率、帧率、码率、FOV 或机位标准；设备可异构，但要保证关键交互可见、硬件时间对齐、机位角色与内外参可追溯。
- 原始采集规格、传输/预处理规格和模型输入规格应分层记录；224×224、256×256 或 240×320 等模型输入不能倒推为采集硬件上限。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 单目/双目 | 标定维护时间、深度有效率、关键阶段遮挡率、单位有效轨迹成本 |
| ARKit/SLAM | 轨迹漂移、重定位次数、低纹理失败率、时间同步误差 |
| Tracking | 抖动、延迟、丢踪率、姿态跳变、操作者负担 |
| UMI/指套 | 轨迹重建质量、动作表示可迁移性、佩戴漂移、接触事件可观测性 |
| 人体工学 | 任务时间、操作者负担、损伤率、握持力分布、连续采集时长 |
| 物理模态 | force/torque、抓力、触觉、深度、外部 wrench 的同步完整性 |
| 定位地图 | 构建时间、存储、更新延迟、对应内点率、可恢复域、隐私攻击面 |

## 适用边界

- 单目适合低成本、大规模、开放空间任务。
- 双目/多目适合孔位、薄片、插入、堆叠、狭窄空间和局部 3D 重建。
- 指套/手套适合采人手细粒度技能，但最终仍需机器人本体数据校准。
- 增加传感器会提高标定、同步、重量和维护成本，必须以单位有效轨迹收益验证。
- 当前神经定位地图证据多来自已知静态场景和路线复访，不能直接替代开放世界长期地图维护与多传感器恢复。

## 证据锚点

- S-EA-QUESTIONS:30-33 覆盖单目、双目和空间感知。
- S-EA-QUESTIONS:34-37 覆盖 ARKit、SLAM、全景相机。
- S-EA-QUESTIONS:38-40 覆盖 Tracking 设备。
- S-EA-QUESTIONS:41-45 覆盖 UMI 和指套式设备。
- RUN-UMI-QUALITY-20260714：`EA-UMI-READ-0001..0004` 覆盖采集器人体工学、力/触觉/深度/位姿与 LiDAR-centric 3D sensing；`0007..0008` 记录数字遥操作边界和任务条件化 VR 配置。
- RUN-VLOC-20260715：`EA-VLOC-2026-0001..0010`, `0014` 覆盖 3DGS/SCR/前馈地图、初值与几何依赖、评测真值、地图隐私和局部细化边界。

## 待补问题

- 建立采集硬件选型矩阵。
- 补充不同设备的单位有效轨迹成本模型。
- 明确设备数据协议：pose、timestamp、confidence、frame、calibration metadata。
- 将人体工学和连续采集负担纳入采集器验收，而不是只看位姿精度。
- 建立点云、SCR、3DGS 和多参考图像地图的全生命周期成本—精度—隐私对照。
