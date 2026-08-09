# Review Packet

> Topic: 具身端到端模型除动作监督外还需要哪些监督信号
> Mode: scoping | Events: 127 | Papers: 94 | Time: 2025-08 to 2026-08

## Core Finding

具身端到端模型除动作监督外至少需要七类非动作监督信号：触觉/力觉、几何/3D、物理、语义/中间表征、奖励/RL、对比/表征学习、安全/纠正。这些信号具有维度互补性，遵循特权范式（训练时注入、推理时丢弃），且生命周期依赖（不同阶段需要不同类型）。

## Evidence Structure

| 监督类型 | 新论文 | 可复用论文 | 核心发现 |
|---------|--------|----------|---------|
| 触觉/力觉 | 9 | 8 | 最普遍需求；力觉盲是视觉策略核心缺陷 |
| 几何/3D | 6 | 10 | 空间推理和视图泛化的刚需 |
| 物理 | 3 | 5 | 三种注入时机：训练时/后训练时/推理时 |
| 语义/中间表征 | 1 | 4 | 密集标注解决"知道做什么但不知道为什么" |
| 奖励/RL | 1 | 6 | 仿真RL + 真实辅助损失防止遗忘 |
| 对比/表征 | 2 | 3 | 跨模态对齐但通用外部特征可能有害 |
| 安全/纠正 | 1 | 3 | 防止信用分配偏差和失败传播 |

## Key Papers

- [2606.09337] TORL-VLA: wrench prediction + intervention-censored critic
- [2607.18231] FM-VLA: force memory VAE (25.9% + 40.7% → 83.3%)
- [2603.13315] Bi-HIL: force supervision 0% → 80% on peg-in-hole
- [2606.13886] PhysVLA: inference-time physics gate (+17% without retraining)
- [2607.14609] Rep-Aligned Tactile: supervision position matters (74% vs 58%)
- [2606.27504] ReWorld: external pretrained features can be harmful
- [2605.22882] GEM-4D: geometry distillation 61% → 81%
- [2607.06564] Lift3D-VLA: GC-MAE point cloud + future geometry prediction
- [2603.10871] FG-CLTP: quantitative tactile tokenization (MAE -52.6%)
- [2603.23376] ABot-PhysWorld: physics-aware DPO post-training
