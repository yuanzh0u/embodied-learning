# 核心论文与系统对照表

建议按表中顺序阅读；①—⑧为重点，三篇评测/理解前序可先速读。版本固定为本次恢复与核验版本。首次提交早于 2024-09-27 的条目属于必要前序。入选依据为机制、证据边界和延伸价值，不以品牌或引用量排序。

| 顺序 | 工作、固定版本 | 首次提交 | 定位与入选理由 | 前后关系 / 阅读提醒 |
|---|---|---|---|---|
| 1 | [UniAD](https://arxiv.org/abs/2212.10156v2) · 2212.10156v2 | 2022-12-20 | 前序：建立非语言、规划导向共享表征参照 | 被 DiMA 使用；OpenDriveVLA 借鉴 3D 查询设计；均为正文明确关系 |
| 2 | [Rethinking Open-Loop Evaluation / AD-MLP](https://arxiv.org/abs/2305.10430v2) · 2305.10430v2 | 2023-05-17 | 评测前序：先理解开放环误判为何会发生 | 与 NAVSIM 构成评测边界链；本表不把先后发表当直接继承 |
| 3 | [NAVSIM](https://arxiv.org/abs/2406.15349v2) · 2406.15349v2 | 2024-06-21 | 评测前序：分清非反应式模拟和交互闭环 | DiffusionDrive、AutoVLA 明确采用其评测 |
| 4 | [LingoQA](https://arxiv.org/abs/2312.14115v4) · 2312.14115v4 | 2023-12-21 | 理解前序：驾驶视频问答、标注和语言评估器 | Wayve 理解侧入口；与 SimLingo 为作者交叉，不据此推断直接代码继承 |
| 5 | [DriveLM](https://arxiv.org/abs/2312.14150v3) · 2312.14150v3 | 2023-12-21 | 数据/方法前序：图式推理、驾驶语言数据 | DiMA 使用 QA；SimLingo 引用并使用 PDM-lite 数据体系 |
| 6 | [LMDrive](https://arxiv.org/abs/2312.07488v2) · 2312.07488v2 | 2023-12-12 | 闭环前序：语言指令到执行控制的早期完整链路 | 与后继 VLA 比较指令输入和 PID 接口；不直接比较 LangAuto 与 Bench2Drive 分数 |
| 7 | [DriveVLM / DriveVLM-Dual](https://arxiv.org/abs/2402.12289v5) · 2402.12289v5 | 2024-02-19 | 核心①：分层快慢系统和车载演示 | 与 EMMA/ORION 为机制对照，不是证明它们继承 Dual 架构 |
| 8 | [EMMA](https://arxiv.org/abs/2410.23262v3) · 2410.23262v3 | 2024-10-30 | 核心②：统一语言空间与多任务训练 | Waymo 工业 Foundation Model 另列案例；研究模型不能等同量产系统 |
| 9 | [ORION](https://arxiv.org/abs/2503.19755v1) · 2503.19755v1 | 2025-03-25 | 核心③：planning token 到连续轨迹的接口 | 后读 Orion-Lite 与 MindDrive；两个不同方向的扩展 |
| 10 | [SimLingo](https://arxiv.org/abs/2503.09594v1) · 2503.09594v1 | 2025-03-12 | 核心④：直接检验语言—动作对齐 | Action Dreaming；区分完整模型与无语言 leaderboard BASE |
| 11 | [AutoVLA](https://arxiv.org/abs/2506.13757v3) · 2506.13757v3 | 2025-06-16 | 核心⑤：物理动作 token 与自适应推理/后训练 | 与 Alpamayo 对比动作输出接口；与 nuVLA 为同研究群体延伸而非同权重继承 |
| 12 | [Alpamayo-R1](https://arxiv.org/abs/2511.00088v2) · 2511.00088v2 | 2025-10-30 | 核心⑥：因果链监督、连续动作专家和奖励一致性 | AR1 更名 Alpamayo1；FlashDrive 主实验基于1.5，不混版本 |
| 13 | [Orion-Lite](https://arxiv.org/abs/2604.08266v1) · 2604.08266v1 | 2026-04-09 | 核心⑦：教师能力能否留在无 LLM 学生 | 明确蒸馏 ORION；TU/e 外部团队，不归入小米作者团队 |
| 14 | [DiffusionDrive](https://arxiv.org/abs/2411.15139v3) · 2411.15139v3 | 2024-11-22 | 核心⑧：非语言生成式驾驶策略的强对照 | TransFuser/SparseDrive 条件表征；与 VLA 的动作头相似性不证明人员或技术继承 |
| 15 | [DiMA](https://arxiv.org/abs/2501.09757v1) · 2501.09757v1 | 2025-01-16 | 训练期语言延伸：共享编码器与辅助任务蒸馏 | VAD/UniAD 是底座；与 Orion-Lite 为不同训练机制 |
| 16 | [OpenDriveVLA](https://arxiv.org/abs/2503.23463v2) · 2503.23463v2 | 2025-03-30 | 结构化表征延伸：明确 scene/agent/map token 对齐 | 与 EMMA 数值文本输出及 ORION 连续头对照 |
| 17 | [MindDrive (Fu et al.)](https://arxiv.org/abs/2512.13636v4) · 2512.13636v4 | 2025-12-15 | 在线学习延伸：仿真交互回报进入语言决策 | ORION 合作团队、Chat-B2D 与 VAE+GRU 技术延伸；不是 arXiv:2512.04441 同名作品 |
| 18 | [nuReasoning / nuVLA](https://arxiv.org/abs/2605.31572v1) · 2605.31572v1 | 2026-05-29 | 数据/评测延伸：推理监督与开放环规划分开评估 | AutoVLA 团队及 Motional 合作；nuVLA 关闭在线文字推理 |
| 19 | [Is VLA Reasoning Faithful?](https://arxiv.org/abs/2605.17268v2) · 2605.17268v2 | 2026-05-17 | 反证延伸：说明—动作一致性的独立审视 | 测试 Alpamayo-R1-10B；限定单模型、小样本、关键词核验 |
| 20 | [FlashDrive](https://arxiv.org/abs/2608.12932v1) · 2608.12932v1 | 2026-08-13 | 部署延伸：缓存、解码、动作采样和量化的系统成本 | 明确优化 Alpamayo1.5；不拿其基线时延倒推 AR1 原始论文 |
| S1 | [Tesla driving foundation / end-to-end policy](https://www.tesla.com/hr_hr/event/tesla-x-cvpr-2026) | 2023 / 2026 披露 | 必选工业案例；非语言路线不能漏掉 | 2023 foundation 演讲、FSD v12/v13/v14 历程与 v14.3 更新分开；非单篇同名模型论文 |
| S2 | [Waymo Foundation Model](https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving/) | 2025-12 / 2026-08 披露 | 语言、共享表征、验证层与世界预测交叉的产业对照 | 不是把 EMMA 改名；Driver/Simulator/Critic 是披露中的不同用途 |

系统案例为企业公开披露，不计入 30 篇正式论文。完整作者、主张定位及版本可从 [论文笔记](paper-notes-index.md) 与 [补充来源](supplement-sources.md) 继续追溯。

## 理想专题：按问题连读

以下顺序服务于公司研究思路，不是按时间推断模型替代；领域原有八篇核心选择保留。U1、Streaming Intent、DIAL是专题主线，其余为对照和延伸。

| 专题顺序 | 论文/版本 | 初次发表 | 入选理由 | 前后关系与阅读问题 |
|---|---|---|---|---|
| L2 | [MindVLA-U1](https://arxiv.org/abs/2605.12624v2) · 2605.12624v2 | 2026-05-12 | 主线：共享计算、流式记忆、快慢路径 | 先读已有DriveVLM(L1)，比较外部接口与共享骨干；并非声称权重继承 |
| L3 | [Streaming Intent](https://arxiv.org/abs/2605.12622v2) · 2605.12622v2 | 2026-05-12 | 主线：语义意图控制连续动作 | 与U1同项目、互补机制；动作涌现结论以开放环与定性范围为限 |
| L4 | [DIAL](https://arxiv.org/abs/2605.12625v2) · 2605.12625v2 | 2026-05-12 | 主线：跨意图候选进入偏好RL | 明确基于U1；和SI连读解释候选支持范围为何重要 |
| L5 | [LinkVLA](https://arxiv.org/abs/2603.01441v1) · 2603.01441v1 | 2026-03-02 | 对照：动作理解＋语言生成双向对齐 | 离散词元和粗到细并行解码；不是U1的同义实现 |
| L6 | [ReflectDrive](https://arxiv.org/abs/2509.20109v1) · 2509.20109v1 | 2025-09-24 | 对照：外部安全约束与生成修补 | 推理时反馈与DIAL训练时反馈比较，不构造虚假继承 |
| L7 | [World4Drive](https://arxiv.org/abs/2507.00603v1) · 2507.00603v1 | 2025-07-01 | 延伸：基础模型先验与潜在世界规划 | 轨迹聚类意图不同于语言意图；世界模型用于选择动作 |
| L8 | [DrivingSphere](https://arxiv.org/abs/2411.11252v1) · 2411.11252v1 | 2024-11-18 | 延伸：生成仿真的交互反馈 | 世界模型用于环境观测；策略表现与模拟器真实性分开 |
| L9 | [AnyScene](https://arxiv.org/abs/2605.26113v1) · 2605.26113v1 | 2026-05-25 | 延伸：布局、占据、多视角可控数据 | 与DrivingSphere按功能比较；当前没有反应式交通 |
| L10 | [VLAFlow](https://arxiv.org/abs/2607.01586v2) · 2607.01586v2 | 2026-07-02 | 理论/机制延伸：受控比较预训练目标 | 机器人实验代表训练机制问题，不充当智驾验证 |
| L11 | [ME-VLM](https://arxiv.org/abs/2609.24526v2) · 2609.24526v2 | 2026-09-21 | 基础模型延伸：认知/代理专家与部署 | 驾驶理解和端侧优化，不等同驾驶控制策略 |
| S3 | [理想 AD Max / VLA 工业披露](https://ir.lixiang.com/static-files/7f0f559e-1e07-4509-9214-19c5dfc7de92) | 2026-04-10（2025年度报告） | 论文到产品连接的企业来源 | 确认公开方向；研究论文检查点到车型版本的映射仍缺失 |

未接受为论文证据的重建、机器人及工具候选见[专题筛选记录](liauto-project-selection.json)，不据标题推断技术细节。
