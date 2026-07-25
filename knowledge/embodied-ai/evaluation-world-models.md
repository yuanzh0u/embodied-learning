---
id: EA-EVAL
title: 评测体系与世界模型
type: topic-card
domain: embodied-ai
updated: 2026-07-20
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §六 评测体系与世界模型(Q16-Q17)
  - id: RUN-WMEVAL-20260714
    file: ../../evidence/literature-review-世界模型评测边界-20260714-reader-v2/evidence.jsonl
    locator: EA-WMEVAL-READ-0001..0015
  - id: RUN-WMDATA-20260714
    file: ../../evidence/literature-review-世界模型需要什么样的训练数据-20260714-reader-v2/evidence.jsonl
    locator: EA-WMDATA-READ-0001..0015
  - id: RUN-SENSOR-ERROR-20260714
    file: ../../evidence/literature-review-具身传感器感知误差-20260714-reader-v2/evidence.jsonl
    locator: EA-SENSORERR-READ-0001..0015
  - id: RUN-VLOC-20260715
    file: ../../evidence/literature-review-近一年图像视觉定位方法的发展与挑战-20260715/evidence.jsonl
    locator: EA-VLOC-2026-0004; EA-VLOC-2026-0006; EA-VLOC-2026-0008..0011; EA-VLOC-2026-0015
  - id: RUN-DATA-CONTAMINATION-20260715
    file: ../../evidence/literature-review-近一年论文中的具身数据污染问题-20260715/evidence.jsonl
    locator: EA-CONTAM-2026-0003..0010; EA-CONTAM-2026-0012
  - id: RUN-VLA-WM-SHIFT-20260717
    file: ../../evidence/literature-review-近一年为何说反应式vla已死世界模型当立-20260717/evidence.jsonl
    locator: EA-CONTAM-2026-0007; EA-WMEVAL-READ-0001; EA-WMEVAL-READ-0003..0008; EA-WMEVAL-READ-0010..0011; EA-WMEVAL-READ-0013..0015
  - id: RUN-LOCOMANIP-20260719
    file: ../../evidence/literature-review-近一年-loco-manipulation-研究进展-20260719/evidence.jsonl
    locator: EA-LOCOMANIP-2026-0001; EA-LOCOMANIP-2026-0004; EA-LOCOMANIP-2026-0007; EA-LOCOMANIP-2026-0010; EA-LOCOMANIP-2026-0015..0018
  - id: RUN-WM-TASKS-20260719
    file: ../../evidence/literature-review-近一年世界视频模型最可靠的应用任务-20260719/evidence.jsonl
    locator: EA-WMTASK-2026-0001..0002; ERR-PVC-READ-0013..0014; EA-WMEVAL-READ-0004; EA-WMEVAL-READ-0010; EA-WMEVAL-READ-0013; EA-WMEVAL-READ-0015
  - id: RUN-VLA-BREAKTHROUGH-20260719
    file: ../../evidence/literature-review-近半年vla在具身领域最大的技术突破-20260719/evidence.jsonl
    locator: EA-VLABREAK-2026-0006..0007; EA-WMEVAL-READ-0004; EA-WMEVAL-READ-0010; EA-WMEVAL-READ-0015
tags: [embodied-ai, evaluation, benchmark, closed-loop, world-model, world-model-authority, action-conditioned-reliability, candidate-ranking, failure-optimism, sim-real, admissibility, action-fidelity, contamination, semantic-leakage, backdoor, risk-coverage, visual-localization]
aliases: [评测体系, 闭环评测, 开放环评测, 世界模型, 世界模型权限阶梯, Action-conditioned reliability, 后果预演, 候选动作排序, 策略淘汰, 失败乐观偏差, Benchmark, Sim2Real, 数据污染评测, 语义泄漏, 触发测试, 动作忠实, 世界模型可采信性, 风险覆盖, 定位评测]
load_when:
  - 问题涉及具身智能评测、benchmark、开放环/闭环、世界模型或长程规划
  - 问题涉及 world-model admissibility、动作忠实、反事实、乐观偏差或策略评估器可信度
  - 问题涉及训练评测泄漏、数据投毒、VLA 后门、触发测试、检测恢复或世界模型二次激活
  - 问题涉及世界模型是否能参与规划、候选动作排序、后果拒识或“世界模型当立”的评测证据
  - 问题涉及世界模型可靠应用、权限晋级、同分布策略排序、BadWAM 或动作—想象同步
confidence: working
---

# 评测体系与世界模型

## Agent Load Hints

- Usually pair with: EA-MODEL, EA-DATA, EA-BIZ, EA-4D, ERR-PATTERN, ERR-EMBODIED.
- Raw source needed when: 需要具体 benchmark 和世界模型论文引用。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 进入世界模型相关 run；评测裁决需要同时读取 limit/gap 事件，不能只加载支持性论文。

## 30 秒摘要

开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。当前最可靠的应用位于权限阶梯低端：训练期 4D/几何教师、离线策略排序与淘汰、有本体锚定的数据/后训练，以及明确物理变量下的 what-if 检查；在线预演、直接控制和安全裁决需要逐级更强的真实闭环证据。

## 关键判断

- 机器人策略最终必须在真实或高保真仿真闭环中验证。
- 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
- 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
- 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
- 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。
- 世界模型评测应覆盖 action-following fidelity、physics adherence、failure optimism、反事实和对抗约束。
- 稀疏的 approach、contact、grasp、release 等关键事件必须保留，普通视频抽帧会删除动作所需信号。
- Goal Success 会高估柔性物和接触任务，应同时记录 Safety Success、形变、滑移、掉落和过力。
- 外部世界模型验证也会被上游感知污染，并受封闭词表和动力学验证能力限制。
- 预测保真属于感知账本，候选动作排序、拒绝和 what-if 规划属于认知账本。
- 视觉定位的 Recall@K 只评估候选前端；最终验收还要覆盖几何验证、位姿误差、可恢复域、连续失定位和恢复能力。
- 定位拒识必须用风险—覆盖曲线评估；固定地理半径真值也要与视觉重叠、地形高度和任务可达性做一致性审计。
- 训练与评测在场景布局、任务逻辑或指令—动作映射上过近时，常规成功率会把记忆误判为泛化；结构扰动集应成为评测独立性检查的一部分。
- Episode 成功率会漏掉关键短时窗的动作覆写和平滑累积漂移，评测需要局部动作、接触前后与 chunk 末端指标。
- 后门防御必须分别报告检测、因果定位、恢复、误报和恢复后能力损失，并限定视觉、状态、语言或自适应触发范围。
- 世界模型扩增需要联合验收原始样本、生成轨迹和最终政策；生成前安全不能推出生成后安全。
- 世界模型取得规划权必须同时满足真实结果保真、长时程一致和足够低的推理成本，并证明候选排序与真实闭环结果相关。
- “能生成未来”不是可采信性证据；系统还应对不可执行未来拒识、不过度乐观地预测失败，并在相同预算下优于不预演的基线。
- Loco-manipulation benchmark 必须区分模块诊断与端到端自治：执行 ground-truth plan、依赖动捕/marker、或只在两个短任务上做真机迁移时，不能把模块高分外推为开放环境可靠性。
- Sim-to-real 应同时报告成功、接触/滑移、状态估计来源、失败阶段和多次真实试验；柔性物与视觉域偏移可能让仿真成功在真机上归零。
- 世界模型权限应按错误可拦截性分配：训练期教师和离线筛选允许人工/真实系统复核，直接控制与安全裁决的错误难以拦截，验收门槛必须更高。
- 同分布策略排序可以条件性复现真机榜单顺序，但必须同时报告 rank correlation、错误淘汰、分布外退化与真实闭环复验，不能据此授予直接控制权。
- RoboWorld 暴露了接触后物体破碎、变形和视觉不一致；这类错误限制高接触策略评测，即使接触前场景与运动看起来合理。
- WAM 安全不能只判断 imagined future 是否合理，还要核对实际执行动作与想象条件是否同步；BadWAM 说明 action mismatch 可在“想象正确”时大幅压低任务成功。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 开放环 | 动作误差、trajectory likelihood、阶段预测、数据分布内外表现 |
| 闭环 | 成功率、平均完成时间、失败恢复率、人工接管、连续运行小时 |
| 安全 | 碰撞次数、过力次数、急停、越界、人机距离违规 |
| 稳定性 | MTBF、重试次数、成功率方差、标定频率 |
| 世界模型 | 多步预测一致性、物体永久性、几何/接触一致、action fidelity、sim-real ranking |
| 可采信性 | physics adherence、failure optimism、反事实、对抗约束、排序相关性 |
| 过程安全 | Safety Success、滑移/掉落、形变、过力、碰撞、接管 |
| 效率 | 关键事件保留、rollout 延迟、在线规划预算、恢复耗时 |
| 视觉定位 | 分条件 Recall@K、PnP/细化成功率、6DoF 误差、风险—覆盖、连续失定位时长、恢复率 |
| 污染压力测试 | 结构扰动集、训练—评测重合率、触发 ASR/失效率、clean success、关键动作窗异常、跨触发面迁移 |
| 防御与恢复 | 检出率、误报率、因果定位准确率、恢复成功率、恢复后能力损失、持续性复测 |
| 决策价值 | 候选动作排序相关性、拒识准确率、failure optimism、规划闭环增益、rollout 延迟与单位成功成本 |
| 权限晋级 | 排名相关性、风险—覆盖、错误淘汰率、分布外退化、在线增益、直接控制安全事件 |
| 动作—想象同步 | action trace 一致性、控制/观测延迟、接触后状态一致、imagined/actual divergence |

## 适用边界

- 仿真适合算法 ablation、危险动作过滤、失败模式预筛和控制器调参。
- 高接触、柔性物、透明/反光物、复杂摩擦和触觉任务必须做真实验证。
- 世界模型近期更适合作离线评估、候选动作筛选和数据生成工具。
- 未通过真实闭环或可靠 sim-real ranking 的世界模型，不应单独承担上线验收或安全裁决。
- 视觉一致但接触、动作或奖励响应错误的模型不具备策略评估 admissibility。
- 允许拒识的定位安全结论只适用于系统可以停机、重定位或切换传感器的场景；必须持续输出位姿时，低覆盖会转化为任务风险。
- 后门 benchmark 的攻击权限与触发器定义决定结论边界；攻击成功证明风险面存在，不等于现实供应链中的污染发生率。
- 未证明动作条件可靠性、sim-real 排序和真实闭环增益的生成模型，只能作为数据/分析工具，不能单独承担规划或安全裁决。
- RoboWorld 的策略排序结论依赖 DROID/RoboArena 等同分布设置；跨本体、跨环境和高接触 OOD 场景必须重新校准。
- BadWAM 证明动作—想象不同步是安全攻击面，但其成功率下降来自特定设置，不能直接外推现实系统发生率。

## 证据锚点

- S-EA-QUESTIONS:67-70 覆盖具身智能评测。
- S-EA-QUESTIONS:71-75 覆盖世界模型。
- RUN-WMEVAL-20260714：`EA-WMEVAL-READ-0001..0015` 覆盖异构监督、外部可查询状态、关键事件保留、动作/物理忠实、长程效率、具身锚定合成数据和下游动作质量目标。
- RUN-WMDATA-20260714：`EA-WMDATA-READ-0003..0007`, `0015` 支持关键事件、具身锚定合成数据、sim-real 对齐、动作质量目标和长程 rollout 可用性。
- RUN-SENSOR-ERROR-20260714：`EA-SENSORERR-READ-0002`, `0005..0009` 支持局部执行走廊、Safety Success、world-model admissibility 和部署置信度。
- RUN-VLOC-20260715：`EA-VLOC-2026-0004`, `0006`, `0008..0011`, `0015` 支持不确定性拒识、真值协议、初始化/几何失败、风险—覆盖和地理长尾评测边界。
- RUN-DATA-CONTAMINATION-20260715：`EA-CONTAM-2026-0003..0010`, `0012` 支持动作窗污染、chunk 漂移、检测—定位—恢复分账、世界模型二次激活、训练评测语义泄漏和控制环同步审计；这些事件原始投影归入 EA-DATA，本卡结论属于有明确锚点的跨卡 synthesis。
- RUN-VLA-WM-SHIFT-20260717：`EA-WMEVAL-READ-0001`, `0003..0008`, `0010..0011`, `0013..0015` 与 `EA-CONTAM-2026-0007` 共同覆盖异构监督、关键事件、4D/几何增强、物理/动作忠实、长程效率、具身锚定和评测泄漏；“规划权门槛”是综合 run 的跨事件 `inference`。
- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0001`, `0004`, `0007`, `0015` 对照了真实柔性物失败、ground-truth-plan 评测边界、摩擦调参假鲁棒与窄任务零样本迁移；`0010`, `0016..0018` 补充风险、长时序记忆、故障下 safety–completion 分账和动捕—机载深度差距。
- RUN-WM-TASKS-20260719：`EA-WMTASK-2026-0001..0002`, `ERR-PVC-READ-0013..0014`, `EA-WMEVAL-READ-0004`, `0010`, `0013`, `0015` 支持低权限任务、同分布策略排序、接触后失真与可采信门槛；“权限阶梯”为跨事件 `inference`。
- RUN-VLA-BREAKTHROUGH-20260719：`EA-VLABREAK-2026-0006..0007` 与复用的世界模型评测事件支持动作—想象同步门禁；BadWAM 的反例不能由视觉合理性指标替代。

## 待补问题

- 建立任务族评测模板。
- 补充 PoC、实验室 benchmark、工业验收之间的指标映射。
- 整理世界模型可落地用法与不可替代真实验证的边界。
- 建立预测保真、决策有效和安全裁决三套分账指标。
- 建立贯通 VPR、几何验证、最终位姿和任务恢复的定位评测模板。
- 建立同时报告 clean performance、污染条件性能、检出/误报、恢复代价和跨模型迁移的具身污染评测协议。
- 建立相同动作候选、计算预算与真机数据下，有/无后果预演层的闭环评测协议。
- 建立训练期教师、离线排序、在线预演、直接控制和安全裁决的五级权限晋级表。
- 建立 imagined action、实际控制命令、机器人状态和接触后果的端到端同步审计协议。
