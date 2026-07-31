---
id: EA-MODEL
title: 模型与预训练
type: topic-card
domain: embodied-ai
updated: 2026-07-26
source:
  - id: S-EA-QUESTIONS
    status: retired
    archive: "git show 081e898:具身智能研究问题清单.md"
    locator: §五 模型与预训练(Q13-Q15)
  - id: RUN-VLA-ALIGN-20260714
    file: ../../evidence/literature-review-sparse-language-dense-vision-and-continuous-action-alignment-in-vla-syst-20260714-reader-v2/evidence.jsonl
    locator: EA-ALIGN-READ-0001..0015
  - id: RUN-WMDATA-20260714
    file: ../../evidence/literature-review-世界模型需要什么样的训练数据-20260714-reader-v2/evidence.jsonl
    locator: EA-WMDATA-READ-0001..0015
  - id: RUN-4D-REASONING-20260714
    file: ../../evidence/literature-review-4d时空推理-20260714-reader-v2/evidence.jsonl
    locator: EA-4D-READ-0001..0015
  - id: RUN-EGO-DATA-20260715
    file: ../../evidence/literature-review-ego-centric-数据在具身模型训练中的问题与困难-20260715/evidence.jsonl
    locator: EA-EGO-2026-0001..0002; EA-EGO-2026-0007..0008; EA-EGO-2026-0011; EA-EGO-2026-0014; EA-EGO-2026-0018
  - id: RUN-DATA-CONTAMINATION-20260715
    file: ../../evidence/literature-review-近一年论文中的具身数据污染问题-20260715/evidence.jsonl
    locator: EA-CONTAM-2026-0001..0010
  - id: RUN-VLA-WM-SHIFT-20260717
    file: ../../evidence/literature-review-近一年为何说反应式vla已死世界模型当立-20260717/evidence.jsonl
    locator: EA-ALIGN-READ-0001; EA-ALIGN-READ-0003..0004; EA-ALIGN-READ-0006; EA-ALIGN-READ-0009; EA-ALIGN-READ-0013; EA-ALIGN-READ-0015; EA-CONTAM-2026-0007; EA-EGO-2026-0001; EA-EGO-2026-0003; EA-WMDATA-READ-0009; EA-WMEVAL-READ-0004; EA-WMEVAL-READ-0010; EA-WMEVAL-READ-0013; EA-WMEVAL-READ-0015
  - id: RUN-LOCOMANIP-20260719
    file: ../../evidence/literature-review-近一年-loco-manipulation-研究进展-20260719/evidence.jsonl
    locator: EA-LOCOMANIP-2026-0002..0003; EA-LOCOMANIP-2026-0006; EA-LOCOMANIP-2026-0008..0009; EA-LOCOMANIP-2026-0013; EA-LOCOMANIP-2026-0016; EA-LOCOMANIP-2026-0018..0020
  - id: RUN-WM-TASKS-20260719
    file: ../../evidence/literature-review-近一年世界视频模型最可靠的应用任务-20260719/evidence.jsonl
    locator: EA-WMTASK-2026-0001..0002; EA-WMDATA-READ-0007; EA-WMEVAL-READ-0005; EA-WMEVAL-READ-0011; EA-WMEVAL-READ-0014
  - id: RUN-VLA-BREAKTHROUGH-20260719
    file: ../../evidence/literature-review-近半年vla在具身领域最大的技术突破-20260719/evidence.jsonl
    locator: EA-VLABREAK-2026-0001..0007; EA-ALIGN-READ-0001; EA-ALIGN-READ-0003..0004; EA-ALIGN-READ-0006; EA-ALIGN-READ-0009; EA-ALIGN-READ-0015; EA-WMDATA-READ-0009; EA-WMEVAL-READ-0004; EA-WMEVAL-READ-0010; EA-WMEVAL-READ-0015
  - id: RUN-MULTIMODAL-TRAINING-20260720
    file: ../../evidence/literature-review-近一年触觉-力觉-视觉-语言等多模态数据在具身机器人训练方法中的演进-20260720/evidence.jsonl
    locator: EA-TWM-READ-0001..0014; EA-ALIGN-READ-0001..0015; EA-VLABREAK-2026-0001..0007
  - id: RUN-PRETRAIN-DATA-SOURCES-20260726
    file: ../../evidence/literature-review-近一年具身智能预训练模型对数据源与采集参数的要求-20260726/evidence.jsonl
    locator: EA-PRETRAIN-DATA-2026-0001..0006; EA-EGO-2026-0007..0009; EA-DQ-YEAR-READ-0009
tags: [embodied-ai, model, pretraining, vla, reactive-vla, world-model, hierarchical-world-model, sparse-future, latent-planning, action-fidelity, rt-x, octo, openvla, sim2real, ego-centric, contamination, poisoning, backdoor, supply-chain]
aliases: [机器人基础模型, Unified Model, VLA, 反应式VLA, VLA—世界模型融合栈, 分层世界模型, 稀疏未来, 世界模型权限阶梯, latent planning, Octo, OpenVLA, RT-X, 预训练, 微调, 模型供应链, 持久后门, 数据投毒, Ego-centric预训练]
load_when:
  - 问题涉及统一机器人模型、VLA、开源模型泛化、预训练有效性或 Sim2Real
  - 问题涉及基模型污染、VLA 后门、干净微调能否清除污染、检查点继承或世界模型生成风险
  - 问题涉及“VLA 已死”、反应式策略、世界模型当立、动作后果预演或策略—动态—控制分层
  - 问题涉及 H-WM、StructVLA、BadWAM、稀疏未来、动作—想象同步或世界模型权限分配
confidence: working
---

# 模型与预训练

## Agent Load Hints

- Usually pair with: EA-DATA, EA-XEMBODIMENT, EA-EVAL, EA-ALIGN, EA-4D.
- Raw source needed when: 需要具体模型或论文引用编号。
- Evidence route: 先从 [文献综述成果目录](../literature-review-catalog.md) 选择 run；中预算读 review packet，高预算按 paper-note index 核验。

## 30 秒摘要

机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型、本体适配器与底层控制器组成的融合栈。近期突破不只是生成更长视频，而是把未来压缩成低频逻辑步骤、稀疏视觉子目标或结构化状态，并验证它与真实动作同步；BadWAM 说明“想象合理、动作错误”足以让系统失效。世界模型应先承担训练期教师、离线排序等低权限任务，再逐级争取在线规划权。Loco-manipulation 与多模态证据还表明，完整动作接口及按功能/时标分层的接触反馈会限制能力上限。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。

## 关键判断

- VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
- Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
- Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
- 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
- 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- 仿真可降低筛选成本，但真实机器人评测仍是最终证据。
- 语言、视觉和动作的主要矛盾是粒度与物理接口错配，不是简单缺少更大的 VLM。
- action module 可通过 motion prior、flow/diffusion 或状态条件 tokenizer 独立学习连续动作结构。
- 4D point tracks 和几何 correspondence 可作为训练期监督，提高动作相关世界动态而不一定增加推理成本。
- 世界动作模型不能只优化视频重建；内部表示还应与接触、轨迹和任务相关区域对齐。
- Ego-centric 预训练存在实测规模收益，但规模与本体对齐是互补条件；没有机器人微调或 aligned human-robot 中间训练时，收益不能直接落到目标控制。
- 缩小 human/robot 视觉外观差距不等于解决动作接口；hand-object 6DoF、接触结构和目标机器人数据仍决定闭环可执行性。
- 基模型后门可能植入对下游微调不敏感的模块并穿过干净适配；模型卡必须追踪预训练来源、模块变化与检查点继承。
- VLA 的污染触发面覆盖视觉、语言、初始状态和关键动作窗，单一图像预处理或单一触发测试不能支持整体安全结论。
- Action chunking 与 delta-pose 积分会放大平滑小偏差，模型审计应覆盖 chunk 内累积和执行窗末端误差。
- 世界模型生成可以把表面安全的数据转成危险轨迹，生成器与下游策略必须共享 canary、差分和闭环复验链路。
- 近期证据支持的范式转移不是“世界模型替代 VLA”，而是把语义/规划、后果评估和本体控制分账后联合；这是跨论文 synthesis，不是单篇论文的直接结论。
- 具身推理只有落到末端运动、图像空间轨迹或其他动作相关表示才有控制价值；显式文本 CoT 作为动作前缀会增加延迟，并可能累积误差。
- 失败恢复可拆为认知层的 failure mode / recovery stage / reward 判断与控制层 residual 纠正，使分类错误和执行错误能够独立归因。
- 原生全身动作接口先于模型规模决定可表达能力；若采集接口不允许深蹲、脚部操作或腰腿协同，VLA 无法从后续规模化中补回缺失动作。
- Loco-manipulation 的异构共训应让少量目标本体全身数据负责动作锚定，同形态静态操作补新动作，人类/robot-free 数据扩展物体、语言与场景；各数据源不能无条件互换。
- 近期 VLA 技术增量更集中在结构化、稀疏和多时间尺度未来：低频逻辑顺序或视觉里程碑负责规划，高频 VLA 与控制器负责闭环执行，而不是把长段稠密视频直接当控制计划。
- 夹爪状态转换和运动转折点可把视频未来压缩为可迁移到低层动作的稀疏规划表征，但现有真机和长程证据仍来自较窄任务。
- 世界动作模型必须同时验证想象与实际动作的同步；BadWAM 将评测成功率从 96.5% 降至 43.1%，表明视觉上合理的未来不能替代 action fidelity。
- 世界模型权限应按错误可拦截性逐级开放：训练期几何/4D 教师和离线策略排序优先，在线预演次之，直接控制与安全裁决最后。
- 多模态 backbone 不应无条件融合全部传感器；语言/视觉、触觉/力觉与控制状态应按功能和频率选择性耦合，并以动作条件状态变化作为共享接口。
- 异构预训练的稳定收益来自“多源覆盖 + 显式对齐”：相机坐标系、本体形态、物理时间和标签可靠性应分别条件化，有噪声人类伪动作不应与传感器记录动作等权。

## 指标与检核

| 关注点 | 可用指标 |
|---|---|
| 离线预训练 | action prediction loss、next state prediction、任务阶段分类、OOD 距离 |
| 迁移价值 | 目标演示数下降、少样本成功率、transfer matrix、负迁移检查 |
| 真实泛化 | 跨物体/场景/任务成功率、失败恢复率、人工接管次数 |
| 系统问题定位 | 开放环误差、闭环失败分类、控制延迟、标定偏差 |
| Sim2Real | sim-real correlation、真实噪声注入、延迟建模、少量真实验证 |
| 多模态对齐 | 语言消融、action-grounded attention、动作解码误差、阶段一致性 |
| 世界动态 | 3D correspondence、action fidelity、长程 rollout、未来评分相关性 |
| Ego 预训练 | 有效视频小时、自动标签通过率、robot-anchor 比例、预训练/中间训练/微调消融、真实闭环增益 |
| 模型供应链 | 基模型/模块/检查点谱系、clean/trigger success、跨微调持久性、触发面覆盖、恢复后能力损失 |
| 融合系统价值 | 同预算纯反应式/融合系统对照、候选动作排序、失败识别、恢复率、闭环增益、额外推理延迟 |
| 结构化未来 | 子目标可达率、里程碑/转折点覆盖、长程任务进度、结构化未来到动作的迁移增益 |
| 权限晋级 | 离线排序相关性、拒绝/风险覆盖、在线规划增益、action fidelity、真实闭环安全门禁 |

## 适用边界

- 当前统一模型更适合作为初始化、表征模型、高层 planner 或 action prior。
- 工业部署必须结合目标本体数据、动作接口校准、底层控制器和闭环评测。
- 高接触、柔性物、透明/反光物和长程任务对预训练泛化要求更高，风险也更大。
- 现有 Ego-centric 规模曲线来自特定灵巧操作和主动感知设置，不能外推为 raw video 对所有机器人任务都遵循同一 scaling law。
- 现有后门研究多基于明确攻击权限和特定触发器，只能说明供应链攻击面与防御盲点，不能推断现实基础模型的污染率。
- 本卡不主张删除 VLA；若纯反应式 VLA 在相同计算与真机数据预算下，能在未见环境、跨本体、长时程和接触扰动任务上稳定追平融合系统，该范式转移判断即被证伪。
- 当前分层世界模型与稀疏未来结果集中在少量 5–7 步或特定夹爪任务，不能据此证明开放世界长程规划已经解决。
- 同分布策略排序只适合作为条件性筛选证据；接触后破碎、变形和视觉不一致仍限制高接触评测与直接控制。

## 证据锚点

- S-EA-QUESTIONS:56-58 覆盖 Unified Model 和 scaling 挑战。
- S-EA-QUESTIONS:59-62 覆盖 benchmark 与真实泛化问题。
- S-EA-QUESTIONS:63-66 覆盖预训练评估和 Sim2Real。
- RUN-VLA-ALIGN-20260714：`EA-ALIGN-READ-0001..0006`, `0013..0015` 覆盖动作语义、结构化接口、跨本体适配以及长程推理与恢复。
- RUN-WMDATA-20260714：`EA-WMDATA-READ-0001..0010` 覆盖异构视频—动作数据、关键事件、具身锚定合成数据、几何未来和失败附近纠正轨迹。
- RUN-4D-REASONING-20260714：`EA-4D-READ-0001..0005`, `0008`, `0014..0015` 覆盖 4D 监督、几何增强 rollout、连续 4D 表征和多视角训练数据。
- RUN-EGO-DATA-20260715：`EA-EGO-2026-0001..0002`, `0007..0008`, `0011`, `0014`, `0018` 支持 Ego 规模收益、本体/动作接口边界、aligned mid-training、目标机器人数据不可缺以及主动视点先验的条件性。
- RUN-DATA-CONTAMINATION-20260715：`EA-CONTAM-2026-0001..0010` 覆盖状态/视觉/语言/动作窗触发、极低比例 episode 投毒、chunk 漂移、持久后门、检测恢复边界和世界模型二次激活；这些事件原始投影归入 EA-DATA，本卡结论属于有明确锚点的跨卡 synthesis。
- RUN-VLA-WM-SHIFT-20260717：`EA-ALIGN-READ-0001`, `0003..0004`, `0006`, `0009`, `0013`, `0015` 支持动作语义、动作相关/latent 推理与恢复分层；`EA-EGO-2026-0001`, `0003` 与 `EA-CONTAM-2026-0007` 限定本体迁移和泛化证据；`EA-WMDATA-READ-0009`、`EA-WMEVAL-READ-0004`, `0010`, `0013`, `0015` 支持后果评估、失败数据和世界模型可用性要求。“VLA—世界模型融合栈”是跨事件 `inference`，未新增论文级 event。
- RUN-LOCOMANIP-20260719：`EA-LOCOMANIP-2026-0002..0003`, `0006`, `0016`, `0018..0020` 支持全身执行、在线规划、显式记忆、稀疏目标控制和原生全身 VLA；`0008..0009`, `0013`, `0020` 支持 robot-free、人类视频、生成数据与同形态静态数据的条件性分工。
- RUN-WM-TASKS-20260719：`EA-WMTASK-2026-0001..0002`, `EA-WMDATA-READ-0007`, `EA-WMEVAL-READ-0005`, `0011`, `0014` 支持低权限世界模型任务、同分布策略排序与接触后失真边界；“权限阶梯”是跨事件 `inference`。
- RUN-VLA-BREAKTHROUGH-20260719：`EA-VLABREAK-2026-0001..0005` 支持低频逻辑、潜在视觉子目标和稀疏里程碑未来；`0006..0007` 支持 action fidelity 安全边界。其余复用事件将结构化未来与 VLA—世界模型融合栈连接起来。
- RUN-MULTIMODAL-TRAINING-20260720：`EA-TWM-READ-0001..0014`, `EA-ALIGN-READ-0001..0015`, `EA-VLABREAK-2026-0001..0007` 支持按功能/时标分层的多模态模型接口；该结论为跨 run synthesis，并未新增论文级 event。

## 待补问题

- 建立公开 VLA 模型比较表。
- 把模型失败拆成数据、模型、控制、硬件和任务定义五类。
- 补充企业内部复验预训练价值的实验设计模板。
- 建立 action prior、离散 tokenizer 和 continuous expert 的统一对照。
- 建立 Ego-human、aligned human-robot 与目标机器人数据的混合比例和边际收益曲线。
- 建立基础模型—适配模块—检查点—生成器—策略的供应链谱系和分阶段 canary 复验模板。
- 建立相同数据、计算和控制预算下纯反应式 VLA 与融合栈的可证伪对照实验。
- 建立训练期教师、离线排序、在线预演、直接控制和安全裁决的世界模型权限晋级门禁。
- 建立结构化/稀疏未来相对稠密视频 rollout 的规划价值、延迟与动作忠实对照。
