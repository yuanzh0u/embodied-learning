# Writing Brief

> Topic: 具身端到端模型除动作监督外还需要哪些监督信号
> Audience: three independent deliverables sharing the same evidence base

## Central Thesis

具身端到端模型至少需要七类非动作监督信号，每类解决动作监督无法覆盖的特定失败模式。监督信号具有维度互补性、特权范式特征和生命周期依赖性。

## Seven Supervision Types

1. **触觉/力觉监督** — 最普遍需求（9/20 新论文），解决力觉盲
2. **几何/3D 监督** — 空间推理和视图泛化刚需
3. **物理监督** — 三种注入时机，弥补物理无知
4. **语义/中间表征监督** — 结构化任务理解
5. **奖励/RL 监督** — 超越静态演示的闭环优化
6. **对比/表征学习监督** — 跨模态对齐，但通用外部特征可能有害
7. **安全/纠正监督** — 防止信用分配偏差

## Key Quantitative Evidence

- Bi-HIL: peg-in-hole 0% → 80% with force [2603.13315]
- FM-VLA: force+state 25.9%+40.7% → 83.3% [2607.18231]
- GEM-4D: 61% → 81% with geometry [2605.22882]
- ManiVID-3D: +40.6% under viewpoint variation [2509.11125]
- PhysVLA: +17% without retraining [2606.13886]
- Rep-Aligned: 74% vs 58% by position [2607.14609]
- FG-CLTP: MAE -52.6% [2603.10871]
- RL-Co: +24% real-world [2602.12628]

## Writing Strategy

- Scientific memo: 按七类监督组织，每类含机制、证据、限制
- Zhihu: 以"直觉错误"开头，七类监督各给一个最亮数据点
- Xiaohongshu: 关键数据点 + 误解澄清 + 边界声明

## Limitations to Acknowledge

- 仿真和实验室环境为主，真实部署未验证
- 不同任务最小监督组合不同
- 监督获取成本和标注质量是实际瓶颈
- 外部监督的迁移条件尚不明确
