# Review Packet: 近一年 Allocentric Representation 在具身领域的应用

> **Run**: literature-review-近一年allocentric-representation在具身领域的应用-20260813
> **时间范围**: 2025-08-13 .. 2026-08-13
> **候选论文**: 18 篇（已接受 17 篇，候选 1 篇）
> **证据事件**: 43 条（ALLO-0001 至 ALLO-0043）
> **生成日期**: 2026-08-13

---

## 一、Evidence Core（证据核心摘要）

### 1.1 证据全景

本次综述从 17 篇已接受论文中提取了 43 条证据事件，覆盖 6 个知识单元：

| 知识单元 | 证据数 | 核心论文 | 支撑/限制/条件/空白 |
|----------|--------|----------|---------------------|
| ALLO-3DVLA（3D表征在VLA中的应用） | 16 | GeoVLA, SpatialActor, Spatial Forcing, 3D-VLA, DP3, ActiveVLA | 9 support / 2 limit / 4 conditional / 1 gap |
| ALLO-OBJCENT（Object-centric操作表征） | 4 | OmniManip | 4 support |
| ALLO-SPATREASON（VLM中的allocentric空间推理） | 9 | SpatialVLM, SpatialRGPT, GCoT, HandVQA, GCA | 4 support / 2 limit / 3 gap |
| ALLO-EGOALLOC（Ego-allocentric转换） | 8 | SymPL, VSI-Bench, Ego2Robot | 1 support / 1 limit / 4 gap / 2 conditional |
| ALLO-SURVEY（综述级观察） | 4 | 空间推理综述, Object-centric操作综述 | 2 support / 2 gap |
| 总计 | 43 | — | 21 support / 5 limit / 6 conditional / 11 gap |

### 1.2 核心发现

**发现一：allocentric 3D表征已成为VLA的核心差异化能力。**
GeoVLA（[arXiv:2508.09071](https://arxiv.org/abs/2508.09071)）、SpatialActor（[arXiv:2511.09555](https://arxiv.org/abs/2511.09555)）、Spatial Forcing（[arXiv:2510.12276](https://arxiv.org/abs/2510.12276)）三篇近一年核心论文均以不同方式将3D几何表征引入VLA，且各自在LIBERO、RLBench等基准上取得SOTA。关键分歧在于**显式3D输入 vs 隐式3D对齐**：GeoVLA和SpatialActor走显式路径（点云/深度），Spatial Forcing走隐式路径（对齐3D基础模型表征），后者以3.8倍训练加速和无需额外传感器的优势挑战了显式路径的必要性。（ALLO-0002, ALLO-0005, ALLO-0008, ALLO-0040）

**发现二：VLM在allocentric空间推理上存在系统性短板。**
SymPL（CVPR 2026）直接指出VLM在egocentric空间推理上表现良好但在allocentric视角下表现很差（ALLO-0019）。GCoT（CVPR 2026）进一步揭示VLM空间推理的"幻觉"问题——对抗条件下所有模型Grounding-Acc <5%（ALLO-0023）。HandVQA（CVPR 2026）显示基础VLM在角度/距离推理上接近随机（ALLO-0024）。三篇CVPR 2026论文从不同角度确认：**allocentric空间推理不是性能差距问题，而是能力缺失问题**。

**发现三：allocentric表征的引入路径正在分化为三条技术路线。**
- **路线A（显式3D传感器注入）**：GeoVLA → 点云嵌入；SpatialActor → 深度+语义融合；3D-VLA → 3D LLM。优势是表征保真度高，瓶颈是传感器噪声和硬件异构性。（ALLO-0007）
- **路线B（隐式3D对齐）**：Spatial Forcing → 对齐3D基础模型表征。优势是无需额外硬件、训练高效，但表征质量受限于基础模型。（ALLO-0008, ALLO-0040）
- **路线C（符号化/工具化）**：SymPL → 投影+符号化；GCA → 工具箱+代码生成；OmniManip → canonical space+原语。优势是可解释、免训练，但依赖上游感知精度。（ALLO-0020, ALLO-0027, ALLO-0041）

**发现四：ego-allocentric转换是连接感知与操作的关键桥梁。**
VSI-Bench将ego-allocentric转换作为评估MLLM空间智能的关键维度（ALLO-0030），Ego2Robot在ego-to-robot数据迁移中依赖3D空间对齐（ALLO-0034）。这表明allocentric表征不仅是推理问题，更是**跨embodiment、跨视角数据迁移的基础设施**。

**发现五：object-centric allocentric表征天然携带任务语义。**
OmniManip以功能可供性定义canonical space（ALLO-0041），使allocentric表征区别于纯几何3D表征。Object-centric操作综述（ALLO-0036）确认了这一研究脉络的系统性，但同时指出与端到端VLA的集成仍处于早期阶段（ALLO-0037）。

---

## 二、Claim Map（关键主张图谱）

### 主题一：Allocentric 3D表征在VLA中的技术路线分化

| 主张 | 立场 | 证据 | 来源 |
|------|------|------|------|
| 当前VLA依赖2D输入，忽略3D几何信息，限制空间感知 | gap | ALLO-0001 | GeoVLA |
| 显式3D点云嵌入可达到SOTA并增强视角不变性 | support | ALLO-0002, ALLO-0003, ALLO-0038 | GeoVLA |
| 点云方法稀疏采样丢语义，图像方法语义几何纠缠 | gap | ALLO-0004 | SpatialActor |
| 语义-几何解耦在噪声下优势放大（+13.9-19.4%） | support | ALLO-0005, ALLO-0006, ALLO-0039 | SpatialActor |
| 显式3D传感器面临噪声、硬件异构、覆盖不完整 | limit | ALLO-0007 | Spatial Forcing |
| 隐式对齐3D基础模型可超越显式3D输入，3.8倍加速 | support | ALLO-0008, ALLO-0040 | Spatial Forcing |
| 隐式对齐降低3D表征部署门槛 | conditional | ALLO-0009 | Spatial Forcing |
| 2D VLA缺乏3D物理世界整合，忽略世界动态 | gap | ALLO-0013 | 3D-VLA |
| 3D LLM+交互token+扩散模型链接感知推理动作 | support | ALLO-0014 | 3D-VLA |
| 紧凑3D点云表征证明3D泛化优势 | support | ALLO-0015 | DP3 |
| 主动感知可动态提升allocentric表征质量 | support | ALLO-0028, ALLO-0029 | ActiveVLA |

**主题总结**：显式 vs 隐式 vs 符号化三条路线尚未收敛。显式路线在表征保真度上领先但受硬件限制；隐式路线在工程实用性上领先但表征上限受制于基础模型；符号化路线可解释性强但依赖上游感知。2025-2026年的趋势是从"是否需要3D"转向"如何高效获取3D理解"。

### 主题二：VLM Allocentric空间推理的能力边界与幻觉

| 主张 | 立场 | 证据 | 来源 |
|------|------|------|------|
| VLM egocentric推理好但allocentric推理差 | gap | ALLO-0019 | SymPL |
| 免训练符号化方法可实现allocentric推理（closer 97.33%） | support | ALLO-0020 | SymPL |
| 符号化方法依赖VLM方向感知准确性 | limit | ALLO-0021, ALLO-0042 | SymPL |
| VLM空间推理存在幻觉，答案正确≠推理正确 | gap | ALLO-0022 | GCoT |
| 对抗条件下所有模型G-Acc <5%, Consist. <5% | limit | ALLO-0023 | GCoT |
| Grounded CoT范式最有效缓解空间推理幻觉 | support | ALLO-0043 | GCoT |
| 基础VLM在角度/距离推理上接近随机 | gap | ALLO-0024 | HandVQA |
| 微调后相对位置准确率>90%，空间知识可迁移 | support | ALLO-0025 | HandVQA |
| VLM在有损语义空间推理，与几何计算不匹配 | gap | ALLO-0026 | GCA |
| 语义-几何解耦+工具箱+代码生成实现几何约束推理 | support | ALLO-0027 | GCA |
| VLM原生空间推理不足，需显式预训练和推理链 | gap | ALLO-0017 | SpatialVLM |
| 深度感知编码器+区域级推理增强VLM空间能力 | support | ALLO-0016, ALLO-0018 | SpatialVLM, SpatialRGPT |

**主题总结**：VLM的allocentric空间推理存在三重困境——(1) 能力缺失（egocentric强allocentric弱）；(2) 推理幻觉（答案正确但过程错误）；(3) 对抗脆弱性（<5%准确率）。解决路径正在分化为"微调"（HandVQA）和"工具化"（GCA/SymPL）两条路线，但前者需要大规模数据、后者依赖上游感知精度。

### 主题三：Ego-Allocentric转换与跨Embodiment迁移

| 主张 | 立场 | 证据 | 来源 |
|------|------|------|------|
| ego-allocentric转换是MLLM空间智能关键维度 | gap | ALLO-0030, ALLO-0031 | VSI-Bench |
| MLLM尚未达到人类水平空间智能 | gap | ALLO-0030 | VSI-Bench |
| 3D空间对齐是ego-to-robot迁移的关键 | support | ALLO-0034 | Ego2Robot |
| allocentric表征为跨embodiment迁移提供坐标系无关中间表示 | conditional | ALLO-0035 | Ego2Robot |
| 投影+符号化将3D allocentric推理降维为2D符号操作 | conditional | ALLO-0042 | SymPL |

**主题总结**：ego-allocentric转换既是评估维度（VSI-Bench），也是工程需求（Ego2Robot）。allocentric表征的坐标系无关性使其成为跨embodiment数据迁移的天然桥梁，但当前方法在转换精度和泛化性上仍有显著差距。

### 主题四：Object-Centric Allocentric表征与操作

| 主张 | 立场 | 证据 | 来源 |
|------|------|------|------|
| VLM缺乏细粒度3D空间理解，无法支撑精确操作 | gap | ALLO-0010 | OmniManip |
| 功能可供性定义的canonical space实现零样本泛化 | support | ALLO-0011, ALLO-0041 | OmniManip |
| 双闭环架构确保allocentric约束从推理到执行落地 | support | ALLO-0012 | OmniManip |
| object-centric表征在泛化性和可组合性上优势明显 | support | ALLO-0036 | Object-centric综述 |
| object-centric表征与端到端VLA集成仍处早期 | gap | ALLO-0037 | Object-centric综述 |

**主题总结**：OmniManip代表了一种将allocentric表征与任务语义绑定的范式——canonical space以功能可供性定义，使表征天然携带操作意图。这一路线的零样本泛化能力突出，但与端到端VLA的深度融合仍是未解问题。

### 主题五：综述视角下的Allocentric挑战定位

| 主张 | 立场 | 证据 | 来源 |
|------|------|------|------|
| allocentric空间推理被识别为大模型时代关键挑战 | support | ALLO-0032 | 空间推理综述 |
| allocentric推理缺乏统一表征框架 | gap | ALLO-0033 | 空间推理综述 |
| object-centric表征在具身操作中已有系统研究脉络 | support | ALLO-0036 | Object-centric综述 |
| allocentric表征与大规模预训练融合是未解问题 | gap | ALLO-0037 | Object-centric综述 |

**主题总结**：两篇综述从不同角度确认了allocentric表征的重要性——空间推理综述将其定位为大模型时代的关键挑战，Object-centric操作综述确认了其在具身操作中的系统性研究脉络。但两篇综述也共同指出：**allocentric表征缺乏统一框架，且与大规模预训练的融合尚未解决**。

---

## 三、Source Gaps（来源空白与局限）

### 3.1 证据覆盖空白

| 空白类型 | 描述 | 影响 |
|----------|------|------|
| **全文不可得** | 12篇论文中仅5篇有arXiv ID且全文可获取（GeoVLA, SpatialActor, Spatial Forcing, OmniManip, 3D-VLA, DP3, SpatialVLM），其余8篇为会议论文/项目页面，无法进行claim-support审计 | 部分证据基于摘要和用户提供的研究笔记，confidence标注为direct但未经全文验证 |
| **时间范围边缘** | 3D-VLA（2024-03）、DP3（2024-03）、SpatialVLM（2024-01）、SpatialRGPT（2024-10）发表于时间范围外，但作为基础工作被纳入 | 这些论文的引入为理解2025-2026年工作提供了必要上下文，但不属于"近一年"严格范围 |
| **arXiv ID缺失** | SymPL, GCoT, HandVQA, GCA, ActiveVLA, VSI-Bench, 空间推理综述, Ego2Robot, Object-centric综述共9篇缺少arXiv ID | 无法通过arXiv API验证，引用链接使用项目页面或会议页面 |
| **定量数据不完整** | ActiveVLA、VSI-Bench、Ego2Robot、两篇综述缺少详细定量结果 | 部分evidence的claim基于定性描述，无法提供精确数字 |

### 3.2 研究主题空白

| 空白类型 | 描述 | 相关证据 |
|----------|------|----------|
| **统一表征框架缺失** | 综述（ALLO-0033）和Object-centric综述（ALLO-0037）均指出allocentric表征缺乏统一框架，当前三条技术路线（显式/隐式/符号化）各自为政 | ALLO-0033, ALLO-0037 |
| **VLA与allocentric推理的端到端融合** | Object-centric综述明确指出allocentric表征与端到端VLA的集成仍处于早期阶段（ALLO-0037）；OmniManip选择双闭环而非端到端，间接印证了这一gap | ALLO-0037, ALLO-0012 |
| **对抗鲁棒性** | GCoT揭示VLM在对抗条件下allocentric推理接近崩溃（G-Acc <5%），但VLA侧尚无对抗鲁棒性评估 | ALLO-0023 |
| **跨embodiment泛化** | Ego2Robot展示了ego-to-robot迁移中的3D空间对齐（ALLO-0034），但allocentric表征在不同机器人形态间的泛化能力未被系统评估 | ALLO-0034, ALLO-0035 |
| **真实世界部署** | 多数VLA论文在仿真基准（LIBERO, RLBench, ManiSkill2）上评估，真实世界部署的allocentric表征质量评估缺失 | ALLO-0002, ALLO-0005 |
| **长时程任务** | 当前工作主要关注单步或短时程操作，allocentric表征在长时程、多步骤任务中的持续维护和更新未被研究 | 全部证据 |
| **多物体关系推理** | OmniManip关注单物体canonical space，多物体间allocentric关系推理（如物体A相对于物体B的位置）未被系统研究 | ALLO-0011 |
| **计算效率与表征质量的权衡** | Spatial Forcing的隐式对齐带来3.8倍加速（ALLO-0008），但隐式表征的质量上限和退化边界未被量化 | ALLO-0008, ALLO-0040 |

### 3.3 方法论局限

| 局限 | 描述 | 涉及论文 |
|------|------|----------|
| **基准碎片化** | VLA论文使用LIBERO/RLBench/ManiSkill2，VLM推理论文使用COMFORT#/SpatialRGPT-Bench/VSI-Bench，两套基准无法互通 | GeoVLA, SpatialActor, SymPL, GCoT等 |
| **allocentric定义不统一** | 不同论文对"allocentric"的理解不同：3D-VLA/GeoVLA指向3D几何表征，SymPL指向物体中心视角推理，OmniManip指向object-centric canonical space | 全部论文 |
| **评估维度单一** | 多数论文仅评估成功率，缺少对allocentric表征质量（如几何精度、视角不变性程度）的直接度量 | GeoVLA, SpatialActor, Spatial Forcing |

### 3.4 候选论文未接受说明

| 论文 | 状态 | 原因 |
|------|------|------|
| GreenVLA (arXiv:2602.00919) | candidate | VLA with potential 3D representation aspects，需要进一步验证其与allocentric表征的关联度 |

---

## 四、证据溯源索引

### 按知识单元

- **ALLO-3DVLA**: ALLO-0001 ~ ALLO-0009, ALLO-0013 ~ ALLO-0015, ALLO-0028, ALLO-0029, ALLO-0038 ~ ALLO-0040
- **ALLO-OBJCENT**: ALLO-0010 ~ ALLO-0012, ALLO-0041
- **ALLO-SPATREASON**: ALLO-0016 ~ ALLO-0018, ALLO-0022 ~ ALLO-0027, ALLO-0043
- **ALLO-EGOALLOC**: ALLO-0019 ~ ALLO-0021, ALLO-0030, ALLO-0031, ALLO-0034, ALLO-0035, ALLO-0042
- **ALLO-SURVEY**: ALLO-0032, ALLO-0033, ALLO-0036, ALLO-0037

### 按论文

| 论文 | arXiv | 证据ID |
|------|-------|--------|
| GeoVLA | [2508.09071](https://arxiv.org/abs/2508.09071) | ALLO-0001, ALLO-0002, ALLO-0003, ALLO-0038 |
| SpatialActor | [2511.09555](https://arxiv.org/abs/2511.09555) | ALLO-0004, ALLO-0005, ALLO-0006, ALLO-0039 |
| Spatial Forcing | [2510.12276](https://arxiv.org/abs/2510.12276) | ALLO-0007, ALLO-0008, ALLO-0009, ALLO-0040 |
| OmniManip | [2501.03841](https://arxiv.org/abs/2501.03841) | ALLO-0010, ALLO-0011, ALLO-0012, ALLO-0041 |
| 3D-VLA | [2403.09631](https://arxiv.org/abs/2403.09631) | ALLO-0013, ALLO-0014 |
| DP3 | [2403.03954](https://arxiv.org/abs/2403.03954) | ALLO-0015 |
| SpatialVLM | [2401.12168](https://arxiv.org/abs/2401.12168) | ALLO-0016, ALLO-0017 |
| SpatialRGPT | [NeurIPS 2024](https://www.anjiecheng.me/assets/SpatialRGPT/Spatial_RGPT.pdf) | ALLO-0018 |
| SymPL | [CVPR 2026](https://airlabkhu.github.io/SymPL/) | ALLO-0019, ALLO-0020, ALLO-0021, ALLO-0042 |
| GCoT | CVPR 2026 | ALLO-0022, ALLO-0023, ALLO-0043 |
| HandVQA | [CVPR 2026](https://kcsayem.github.io/handvqa/) | ALLO-0024, ALLO-0025 |
| GCA | CVPR 2026 | ALLO-0026, ALLO-0027 |
| ActiveVLA | 2026-01 | ALLO-0028, ALLO-0029 |
| VSI-Bench | 2024-12 | ALLO-0030, ALLO-0031 |
| 空间推理综述 | 2025-10 | ALLO-0032, ALLO-0033 |
| Ego2Robot | 2026-08 | ALLO-0034, ALLO-0035 |
| Object-centric操作综述 | 2025 | ALLO-0036, ALLO-0037 |
