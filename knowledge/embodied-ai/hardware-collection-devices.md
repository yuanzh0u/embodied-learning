---
id: EA-HARDWARE
title: 采集硬件与设备路线
type: topic-card
domain: embodied-ai
updated: 2026-06-05
source:
  - id: S-EA-QUESTIONS
    file: ../../具身智能研究问题清单.md
    locator: lines 170-244
tags: [embodied-ai, hardware, monocular, stereo, arkit, slam, tracking, umi, glove]
aliases: [采集硬件, 单目, 双目, ARKit, SLAM, Tracking, UMI, 指套, 手套]
load_when:
  - 问题涉及采集设备选型、单目双目、ARKit、SLAM、VR tracking、UMI 或指套式设备
confidence: working
---

# 采集硬件与设备路线

## Agent Load Hints

- Usually pair with: EA-DATA, EA-SENSOR.
- Raw source needed when: 需要具体设备路线的完整问答或参考资料。

## 30 秒摘要

采集硬件不会收敛到单一设备，而会收敛到少数数据协议和接口范式。单目方案因成本、标定和维护优势适合规模化起步；双目/多目适合几何精度、插入、堆叠和遮挡严重任务；ARKit/SLAM/Tracking 设备适合低成本位姿与遥操作输入，但不能当工业真值。UMI 类设备的价值来自硬件约束下的软件化数据闭环，指套/手套适合人手技能和灵巧操作数据。

## 关键判断

- 具身采集不必须双目，关键看任务是否依赖稳定几何、相对深度和遮挡恢复。
- 行业偏好单目来自工程经济性：便宜、易标定、低带宽、易维护、适配视觉预训练。
- 双目落地瓶颈是标定同步、弱纹理/反光匹配失败、深度噪声融合和系统成本。
- ARKit 可用于低成本 VIO、位姿跟踪和快速原型，但不适合作唯一计量真值。
- VR/AR tracking 是低成本人机输入，需记录置信度、丢踪事件和时间戳质量。
- UMI 的核心价值是把自然场景人类示教转成机器人可学习的数据闭环。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 单目/双目 | 标定维护时间、深度有效率、关键阶段遮挡率、单位有效轨迹成本 |
| ARKit/SLAM | 轨迹漂移、重定位次数、低纹理失败率、时间同步误差 |
| Tracking | 抖动、延迟、丢踪率、姿态跳变、操作者负担 |
| UMI/指套 | 轨迹重建质量、动作表示可迁移性、佩戴漂移、接触事件可观测性 |

## 适用边界

- 单目适合低成本、大规模、开放空间任务。
- 双目/多目适合孔位、薄片、插入、堆叠、狭窄空间和局部 3D 重建。
- 指套/手套适合采人手细粒度技能，但最终仍需机器人本体数据校准。

## 证据锚点

- S-EA-QUESTIONS:30-33 覆盖单目、双目和空间感知。
- S-EA-QUESTIONS:34-37 覆盖 ARKit、SLAM、全景相机。
- S-EA-QUESTIONS:38-40 覆盖 Tracking 设备。
- S-EA-QUESTIONS:41-45 覆盖 UMI 和指套式设备。

## 待补问题

- 建立采集硬件选型矩阵。
- 补充不同设备的单位有效轨迹成本模型。
- 明确设备数据协议：pose、timestamp、confidence、frame、calibration metadata。
