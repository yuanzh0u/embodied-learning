# Evidence Appendix

> **Run**: literature-review-近一年allocentric-representation在具身领域的应用-20260813
> **Total evidence events**: 43 (ALLO-0001 to ALLO-0043)
> **Accepted papers**: 15
> **Date**: 2026-08-13

---

## Evidence Event Index

### ALLO-3DVLA: 3D Representation in VLA (16 events)

| Event ID | Paper | Stance | Confidence | Claim Summary |
|----------|-------|--------|------------|---------------|
| ALLO-0001 | GeoVLA (2508.09071) | gap | direct | 当前VLA依赖2D输入，忽略3D几何信息 |
| ALLO-0002 | GeoVLA (2508.09071) | support | direct | 点云嵌入+3D Action Expert，LIBERO/ManiSkill2 SOTA |
| ALLO-0003 | GeoVLA (2508.09071) | support | direct | 3D表征带来高度/尺度/视角鲁棒性 |
| ALLO-0004 | SpatialActor (2511.09555) | gap | direct | 点云稀疏采样和图像法各有缺陷 |
| ALLO-0005 | SpatialActor (2511.09555) | support | direct | 语义-几何解耦，RLBench 87.4%，噪声+13.9-19.4% |
| ALLO-0006 | SpatialActor (2511.09555) | support | direct | 解耦表征增强少样本泛化 |
| ALLO-0007 | Spatial Forcing (2510.12276) | limit | direct | 显式3D传感器面临噪声/异构性/覆盖问题 |
| ALLO-0008 | Spatial Forcing (2510.12276) | support | direct | 隐式对齐超越2D和3D VLA，3.8倍加速 |
| ALLO-0009 | Spatial Forcing (2510.12276) | conditional | inference | 隐式对齐降低3D部署门槛 |
| ALLO-0013 | 3D-VLA (2403.09631) | gap | direct | 2D VLA缺乏3D世界整合 |
| ALLO-0014 | 3D-VLA (2403.09631) | support | direct | 3D-VLA统一感知推理动作的世界模型 |
| ALLO-0015 | DP3 (2403.03954) | support | direct | DP3稀疏点云+diffusion policy的泛化优势 |
| ALLO-0028 | ActiveVLA (CVPR2026) | support | direct | 主动感知注入VLA提升3D操作精度 |
| ALLO-0029 | ActiveVLA (CVPR2026) | conditional | inference | 主动视角调整突破视角不变性瓶颈 |
| ALLO-0038 | GeoVLA (2508.09071) | support | inference | allocentric表征编码视角无关几何不变性 |
| ALLO-0039 | SpatialActor (2511.09555) | support | inference | 鲁棒性源于表征解耦非信息增加 |
| ALLO-0040 | Spatial Forcing (2510.12276) | conditional | inference | 关键在对齐质量非传感器数据 |

### ALLO-OBJCENT: Object-Centric Representation (4 events)

| Event ID | Paper | Stance | Confidence | Claim Summary |
|----------|-------|--------|------------|---------------|
| ALLO-0010 | OmniManip (2501.03841) | gap | direct | VLM缺乏细粒度3D空间理解 |
| ALLO-0011 | OmniManip (2501.03841) | support | direct | canonical space+交互原语，零样本泛化 |
| ALLO-0012 | OmniManip (2501.03841) | support | direct | 双闭环架构确保约束精确落地 |
| ALLO-0041 | OmniManip (2501.03841) | support | inference | canonical space天然携带任务语义 |

### ALLO-SPATREASON: VLM Spatial Reasoning (12 events)

| Event ID | Paper | Stance | Confidence | Claim Summary |
|----------|-------|--------|------------|---------------|
| ALLO-0016 | SpatialVLM (2401.12168) | support | direct | 链式推理+空间数据预训练赋予VLM空间能力 |
| ALLO-0017 | SpatialVLM (2401.12168) | gap | direct | VLM原生空间推理不足 |
| ALLO-0018 | SpatialRGPT (NeurIPS2024) | support | direct | 深度感知+区域级空间推理 |
| ALLO-0022 | GCoT (CVPR2026) | gap | direct | VLM空间推理存在幻觉 |
| ALLO-0023 | GCoT (CVPR2026) | limit | direct | 对抗条件下Grounding-Acc<5% |
| ALLO-0024 | HandVQA (CVPR2026) | gap | direct | 基础VLM细粒度空间推理接近随机 |
| ALLO-0025 | HandVQA (CVPR2026) | support | direct | 微调后50%→90%+，可迁移 |
| ALLO-0026 | GCA (CVPR2026) | gap | direct | VLM语义推理与几何计算不匹配 |
| ALLO-0027 | GCA (CVPR2026) | support | direct | GCA语义分析器+任务求解器解耦 |
| ALLO-0043 | GCoT (CVPR2026) | support | direct | Grounded CoT范式最有效 |

### ALLO-EGOALLOC: Ego-Allocentric Transformation (7 events)

| Event ID | Paper | Stance | Confidence | Claim Summary |
|----------|-------|--------|------------|---------------|
| ALLO-0019 | SymPL (CVPR2026) | gap | direct | VLM在allocentric视角下断崖式下降 |
| ALLO-0020 | SymPL (CVPR2026) | support | direct | 四步免训练法，COMFORT#多个方向>90% |
| ALLO-0021 | SymPL (CVPR2026) | limit | direct | 依赖VLM方向感知准确性 |
| ALLO-0030 | VSI-Bench (2024-12) | gap | direct | ego-allocentric转换是空间智能关键维度 |
| ALLO-0031 | VSI-Bench (2024-12) | gap | inference | allocentric是基础能力缺口 |
| ALLO-0034 | Ego2Robot (2026-08) | support | direct | allocentric表征在跨embodiment迁移中起桥梁作用 |
| ALLO-0035 | Ego2Robot (2026-08) | conditional | inference | allocentric提供坐标系无关中间表示 |
| ALLO-0042 | SymPL (CVPR2026) | conditional | inference | 投影+符号化是效率vs保真度折中 |

### ALLO-SURVEY: Survey & Taxonomy (4 events)

| Event ID | Paper | Stance | Confidence | Claim Summary |
|----------|-------|--------|------------|---------------|
| ALLO-0032 | SpatialSurvey (2025-10) | support | direct | 综述识别allocentric推理为关键挑战 |
| ALLO-0033 | SpatialSurvey (2025-10) | gap | direct | allocentric视角缺乏统一表征框架 |
| ALLO-0036 | ObjCentSurvey (2025) | support | direct | object-centric表征已有系统研究脉络 |
| ALLO-0037 | ObjCentSurvey (2025) | gap | direct | 与端到端VLA集成处于早期 |

---

## Article-to-Evidence Trace Map

### Scientific Memo (scientific-memo_keyan.md)

| Article Section | Primary Evidence Events |
|----------------|------------------------|
| Introduction | ALLO-0001, ALLO-0013, ALLO-0019 |
| Background | ALLO-0015, ALLO-0016, ALLO-0017, ALLO-0018, ALLO-0014 |
| 显式3D注入 | ALLO-0002, ALLO-0003, ALLO-0004, ALLO-0005, ALLO-0006, ALLO-0038, ALLO-0039 |
| 隐式3D对齐 | ALLO-0007, ALLO-0008, ALLO-0009, ALLO-0028, ALLO-0029, ALLO-0040 |
| 符号化工具化 | ALLO-0010, ALLO-0011, ALLO-0012, ALLO-0026, ALLO-0027, ALLO-0041 |
| VLM推理局限 | ALLO-0019, ALLO-0022, ALLO-0023, ALLO-0024, ALLO-0030, ALLO-0031 |
| Ego-Allocentric转换 | ALLO-0030, ALLO-0034, ALLO-0035, ALLO-0042 |
| Open Problems | ALLO-0033, ALLO-0037, ALLO-0023 |

### Zhihu Explainer (zhihu-explainer_zhihu.md)

| Article Section | Primary Evidence Events |
|----------------|------------------------|
| TL;DR | ALLO-0002, ALLO-0008, ALLO-0011, ALLO-0022 |
| 第一条路线 | ALLO-0001, ALLO-0002, ALLO-0003, ALLO-0004, ALLO-0005, ALLO-0006 |
| 第二条路线 | ALLO-0007, ALLO-0008, ALLO-0009, ALLO-0028, ALLO-0040 |
| 第三条路线 | ALLO-0011, ALLO-0019, ALLO-0020, ALLO-0027, ALLO-0041 |
| VLM推理幻觉 | ALLO-0022, ALLO-0023, ALLO-0024, ALLO-0025 |
| 边界声明 | ALLO-0033, ALLO-0037 |

### Xiaohongshu Post (xiaohongshu-post_xiaohongshu.md)

| Article Section | Primary Evidence Events |
|----------------|------------------------|
| 痛点 | ALLO-0001, ALLO-0013 |
| 突破一 | ALLO-0002, ALLO-0005 |
| 突破二 | ALLO-0008 |
| 突破三 | ALLO-0019, ALLO-0020 |
| 警示 | ALLO-0022, ALLO-0023, ALLO-0025 |
| 展望 | ALLO-0033, ALLO-0037 |
