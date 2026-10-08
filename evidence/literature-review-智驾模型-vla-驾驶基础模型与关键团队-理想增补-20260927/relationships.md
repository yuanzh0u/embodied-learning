# 技术关系与组织关系图

实线表示明确使用、蒸馏或评测关系；虚线仅表示本综述的方法比较。不是影响力排名或人员师承图。每条技术边的主张、类型和定位见 [relations.json](relations.json)；原始引用边独立保留在 [citation-graph.json](citation-graph.json)。

```mermaid
flowchart LR
  U[UniAD] -->|REL-01 编码器使用| D[DiMA]
  O[ORION] -->|REL-02 教师蒸馏| OL[Orion-Lite]
  O -.->|REL-03 同机构协作与接口比较| M[MindDrive]
  A15[Alpamayo 1.5] -->|REL-04 实现基础| F[FlashDrive]
  AR[Alpamayo-R1] -->|REL-05 被测模型| FA[推理忠实性分析]
  N[NAVSIM] -->|REL-06 评测协议| DD[DiffusionDrive]
  N -->|REL-07 评测协议之一| AV[AutoVLA]
  DV[DriveVLM] -.->|REL-08 快慢接口比较| W[Waymo 官方快慢架构]
```

下图的连线表示发表时机构、明确公开角色或企业披露归属，不推断所有作者的个人贡献。人员对应关系、当前任职及日期见 [organization-people.json](organization-people.json)，发表时原文对应见 [publication-identities.json](publication-identities.json)。

```mermaid
flowchart TD
  TH[清华 / 理想] -->|PUB-2402.12289| DV[DriveVLM]
  WM[Waymo] -->|PUB-2410.23262| EM[EMMA]
  XM[华中科技大学 / 小米汽车] -->|PUB-2503.19755| OR[ORION]
  XM -->|PUB-2512.13636| MI[MindDrive]
  UC[UCLA] -->|PUB-2506.13757| AU[AutoVLA]
  NV[NVIDIA] -->|PUB-2511.00088 附录角色| AL[Alpamayo-R1]
  TU[TU/e MPS] -->|PUB-2604.08266| OL[Orion-Lite]
  TV[图宾根 / Wayve] -->|PUB-2503.09594| SI[SimLingo]
  TE[Tesla] -->|IND-TESLA-2023 / 2026| PH[Phil Duan：报告与公开工程角色]
  TE -->|IND-TESLA-2026| AS[Ashok Elluswamy：报告与公开职衔]
```

Tesla 的 2023 foundation-model 报告、2026 driving-policy 报告与 FSD v14.3 更新属于按日期串联的公开披露。这里不绘制未被公开资料支持的具体模型继承边。Alpamayo-R1 与当前 Alpamayo 1/1.5 发布命名见补充来源 CODE-ALPAMAYO，也不能直接视作同一评测权重。

## 理想专题：机制连接与证据边界

实线仅用于明确实现继承；下图其余虚线为同项目互补或本报告的机制比较。边记录为relations.json中的REL-LI-09至REL-LI-17，不能解释为内部产品依赖图。

```mermaid
flowchart LR
  DV[DriveVLM 语义辅助] -.->|REL-LI-11 问题延伸| LK[LinkVLA 离散双向接口]
  LK -.->|REL-LI-12 并行接口比较| U[U1 共享骨干与连续动作]
  SI[Streaming Intent 语义意图] -.->|REL-LI-10 同项目互补| U
  U -->|REL-LI-09 明确基于| D[DIAL 多意图偏好学习]
  R[ReflectDrive 外部约束修补] -.->|REL-LI-15 训练与推理反馈比较| D
  W[World4Drive 潜在世界选轨迹] -.->|REL-LI-13 意图定义不同| SI
  DS[DrivingSphere 生成交互仿真] -.->|REL-LI-14 功能比较| AS[AnyScene 固定布局场景生成]
  VF[VLAFlow 机器人训练比较] -.->|REL-LI-16 驾驶迁移待验证| U
  ME[ME-VLM 驾驶理解与端侧部署] -.->|REL-LI-17 权重映射未公开| P[理想量产VLA披露]
```

组织层可以确认联合发表：Mind-Omni论文连接理想、清华与港中文；LinkVLA连接理想与浙大；DrivingSphere连接理想、澳门大学与北理工；World4Drive连接中科院自动化所、理想、鹏城实验室、新加坡国立与清华；VLAFlow连接理想、北邮与港中文深圳。它们不是统一汇报线。ME-VLM项目领导、模型与部署贡献组按§9单独记录。各个人机构与版本以组织人员表为准。

原有citation-graph保留前一轮引文扩展；本轮新增的原文关系检查另见[理想引文与继承检查](liauto-citation-checks.json)，不把研究者画出的虚线当作论文引用。
