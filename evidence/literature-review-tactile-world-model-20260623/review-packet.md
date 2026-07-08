# Review Packet: 触觉世界模型

## Scope

- Topic: 触觉世界模型
- Resolved time range: 2025-12-23 to 2026-06-23
- Knowledge routes: `EA-SENSOR`, `EA-DATA`, `EA-MODEL`, `EA-EVAL`
- Search artifacts: `query-plan.json`, `query-plan.md`, `arxiv-candidates.json`
- Evidence artifacts: `source-entry-draft.md`, `evidence.jsonl`

## Sufficiency

- Paper-level sources promoted: 11 / 5 required
- Evidence events: 18
- Stance coverage: support, conditional, limit, gap
- Formal review status: formal-ready

## Synthesis Frame

触觉世界模型不是“给机器人多接一个触觉传感器”。本轮证据显示，它更像一个接触动力学建模问题：模型需要从视觉、触觉、力/力矩、动作、语言和机器人状态中预测未来接触，并把预测接到规划、策略修正或快速反射控制上。

## Evidence Clusters

1. 表征与预测：ContactWorld、Visuo-Tactile World Models、OmniVTA、TacForeSight、Dream-Tac 直接支持“触觉世界模型需要空间结构、时间连续性、动作条件、接触门控和 force-conditioned tactile latent dynamics”。
2. 数据供给：Visuo-Tactile World Models、OmniVTA、HapTile、TAMEn 支持“数据必须同步多模态、覆盖成功/失败/恢复、包含触觉原始图像与接触几何派生信号，并通过可执行性或闭环收益验证”。
3. 使用接口：OmniVTA、TacForeSight、Dream-Tac、ViTaL、AT-VLA 表明触觉世界模型可用于 MPC、anticipatory contact priors、world-action generation、inference-time steering 和 slow-fast policy injection。
4. 评测缺口：ContactWorld、TacForeSight、HT-Bench、ViTaL 指向长期规划、扰动恢复、表征到下游性能、预测误差累积等评测短板。

## Main Claim Map

| Claim | Trace | Stance | Confidence |
|---|---|---|---|
| 触觉世界模型的核心变量是接触，而不是触觉图像本身。 | `EA-SENSOR`; `EA-TWM-2026-0003`; `EA-TWM-2026-0007` | support | direct/topic-card-source |
| 表征的空间结构、时间连续性和跨模态兼容性决定长期规划表现。 | `EA-TWM-2026-0001`; `EA-TWM-2026-0002` | support/conditional | direct |
| 数据需求至少包括同步视觉、触觉、动作、proprioception、语言/任务条件、成功失败与恢复片段。 | `EA-TWM-2026-0004`; `EA-TWM-2026-0005`; `EA-TWM-2026-0013`; `EA-TWM-2026-0014` | support/conditional | direct |
| 力/力矩与触觉不是冗余模态；全局 force 可能先于局部触觉变化。 | `EA-TWM-2026-0007`; `EA-SENSOR` | support | direct/topic-card-source |
| 闭环落地需要高频触觉路径或反射控制，不能只依赖低频大模型推理。 | `EA-TWM-2026-0006`; `EA-TWM-2026-0016` | support/conditional | direct |
| 当前触觉世界模型仍存在传感器迁移、预训练规模、预测误差累积和下游评测不足。 | `EA-TWM-2026-0002`; `EA-TWM-2026-0012`; `EA-TWM-2026-0015` | limit/gap | direct |

## Topic Card Update Suggestions

- Add to `EA-SENSOR`: 触觉数据应区分原始 tactile image、力/力矩、tactile depth/force-field、marker displacement 等派生接触几何；不同表示与视觉表征的兼容性会影响世界模型规划收益。 Source: `EA-TWM-2026-0001`, `EA-TWM-2026-0018`.
- Add to `EA-DATA`: 接触丰富世界模型数据需要成功、失败、扰动恢复、可执行性检查和多频率同步，单纯成功演示会漏掉临界接触状态。 Source: `EA-TWM-2026-0004`, `EA-TWM-2026-0013`, `EA-TWM-2026-0014`.
- Add to `EA-EVAL`: 触觉世界模型评测应覆盖长期规划、扰动恢复、跨传感器/跨对象泛化，以及表征级指标到真实下游任务成功率的关联。 Source: `EA-TWM-2026-0002`, `EA-TWM-2026-0008`, `EA-TWM-2026-0015`.
