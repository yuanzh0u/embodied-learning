# 来源登记草案（未自动合并）

> 状态：`draft-only / pending-owner-review`
>
> 本文件只为后续人工维护 `knowledge/sources.md` 与文献综述目录提供登记文本；尚未写入来源总表、主题卡或正式证据目录。合并前应由知识库 owner 决定最终 ID、存储位置和状态字段。

## 建议的来源角色分层

这两项来源不能互相替代：

1. 用户给定的访谈摘要属于 `industry observation`，用于记录行业关注点、模型名称和检索起点，不用于单独证明技术事实。
2. 当前 LeWorldModel 文献 run 属于 `primary-paper synthesis`，技术 claim 应回到其中已审核的 paper-level event。

若二者表述冲突，以完整论文和通过审核的 evidence event 为技术判断依据；访谈摘要保留为“行业观察到什么”的来源。

## 建议条目 A：S-LI-WEI-MENTIONED-MODELS-20260724

- 候选状态：`external-local`；`pending-owner-review`，未自动合并
- 来源角色：`industry observation`
- 本地来源：`D:\Worksapce\hunter\docs\summaries\2026-07-24-li-wei-mentioned-models.md`
- 类型：用户提供的访谈摘要 / 行业观察 / 模型线索清单
- 日期：2026-07-24
- 范围：
  - 李威访谈或交流摘要中提到的模型、研究方向与技术关键词
  - 用于确定 LeWorldModel、JEPA、潜空间世界模型、规划与控制等检索入口
  - 不视为逐字采访记录，也不视为论文结论、性能数字或模型优劣的正式证据
- 建议使用规则：
  - 可支持“行业讨论提到了哪些方向”或“为什么启动该轮调研”。
  - 不可单独支持架构细节、实验结果、发布日期、性能排名或因果结论。
  - 技术性转述必须由下方 `primary-paper synthesis` 中的已审核事件补证。
- 可追溯路径：上述外部本地文件；后续若迁移进仓库，应保留原路径、迁移日期与内容哈希。

## 建议条目 B：LR-LEWORLDMODEL-LINEAGE-20260724

- 候选状态：`active-settled-run`；`pending-owner-review`，未自动合并
- 来源角色：`primary-paper synthesis`
- 稳定目录：`evidence/literature-review-leworldmodel-技术谱系-jepa-潜空间世界模型到规划控制-20260724/`
- 直接证据入口：
  - 已接纳事件：`evidence/literature-review-leworldmodel-技术谱系-jepa-潜空间世界模型到规划控制-20260724/evidence.jsonl`
  - 逐篇笔记：`evidence/literature-review-leworldmodel-技术谱系-jepa-潜空间世界模型到规划控制-20260724/paper-notes/`
  - 原文支持审计：`evidence/literature-review-leworldmodel-技术谱系-jepa-潜空间世界模型到规划控制-20260724/claim-support-audits/`
- 类型：完整非 OCR 论文精读 / claim-support 审核 / 跨论文技术谱系综合
- 执行日期：2026-07-24 至 2026-07-25
- 覆盖论文发布日期：2025-06-11 至 2026-07-14
- 已审核规模：
  - 24 篇不重复论文
  - 76 条 evidence event
  - 其中 63 条来自本轮 `evidence-new`，13 条来自明确选择的 `reused-evidence`
- 主题范围：
  - JEPA/LeJEPA 的表征目标、SIGReg 与 LeWorldModel 的端到端动作条件潜动力学
  - 从“可预测”到“可规划”的潜空间几何：动作敏感性、可达性、终端度量、逆动力学与搜索
  - 无动作视频预训练与机器人 action-conditioned post-training 的阶段边界
  - semantic latent 与 reconstruction-aligned latent 对视觉质量、动作恢复、规划和策略评估的不同影响
  - 长时程 rollout、层级 subgoal、支持约束搜索、接触/几何信息与真实部署限制
  - 世界模型评估从视觉保真扩展到动作忠实、物理一致、长程一致、策略效用与计算效率
- 建议使用规则：
  - 用于 EA-MODEL、EA-EVAL、EA-4D 的技术 claim 时，必须同时记录具体 event ID。
  - 家族级、跨论文或机制链综合应标记为 `inference`，并保留任务、本体、数据集与评估代理边界。
  - 不将模拟任务结论直接外推到真实机器人，不将生成 rollout 内的 VLA 成功率直接等同于真实闭环成功。
  - 不把 Web-DINO 等单个受测编码器扩展成 DINOv3 或其他视觉基础模型的通用优劣结论。
- 可追溯路径：
  - 每条技术 claim：对应 JSONL 中的 `event_id`
  - 每条事件的论文、locator、摘要与 verification：同一 JSONL 事件对象
  - 精确原文上下文：对应 `paper-notes/<arxiv-id>.json` 与 `claim-support-audits/<arxiv-id>.json`

## 合并位置提示

当前 `knowledge/sources.md` 的约定说明论文级证据与文献 run 通常由 `evidence/` 和 `knowledge/literature-review-catalog.md` 管理。因此建议人工合并时：

- 将条目 A 作为 `industry observation` 登记到 `knowledge/sources.md`；
- 将条目 B 的稳定入口优先登记到文献综述目录，并在需要统一来源角色时再从 `knowledge/sources.md` 建立指向该 run 的轻量引用。

本提示不执行任何合并。
