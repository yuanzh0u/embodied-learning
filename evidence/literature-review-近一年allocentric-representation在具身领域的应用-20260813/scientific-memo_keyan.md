# Allocentric Representation 在具身领域的应用：2025-2026 年范围性综述

> 文献综述 | 2025-08 至 2026-08 | 43 条证据事件 | 17 篇论文

## 摘要

Allocentric（物体中心/世界中心）表征是指以外部参照系（如物体、场景坐标系）而非自我中心视角来描述空间信息的表示方式。在具身智能领域，近一年的研究经历了从"可选增强模块"到"核心空间能力"的范式转变。本综述基于 43 条证据事件的分析表明，allocentric 表征在 VLA（视觉-语言-动作）模型和 VLM（视觉-语言模型）中的应用已分化为三条技术路线：显式 3D 注入（以 [GeoVLA](https://arxiv.org/abs/2508.09071) 和 [SpatialActor](https://arxiv.org/abs/2511.09555) 为代表）、隐式 3D 对齐（以 [Spatial Forcing](https://arxiv.org/abs/2510.12276) 为代表）和符号化工具化（以 [OmniManip](https://arxiv.org/abs/2501.03841) 和 SymPL 为代表）。与此同时，VLM 在 allocentric 空间推理上暴露出系统性短板：egocentric 推理能力强但 allocentric 推理显著退化，且存在"答案正确但推理幻觉"的现象。三条路线在表征质量、工程实用性和泛化能力上各有取舍，当前缺乏统一评估框架和直接的跨路线消融实验。

---

## 1 引言

### 1.1 Allocentric 表征的定义与范畴

在认知科学中，allocentric 表征是指以环境或物体为参照系的空间表示，与 egocentric（自我中心）表征相对。在具身 AI 领域，allocentric 表征涵盖三个相互关联但可区分的子方向：（1）3D 几何表征，如点云、深度图、体素等，提供视角无关的几何信息；（2）object-centric 表征，以物体规范空间（canonical space）为参照系，携带功能语义；（3）ego-allocentric 转换，即在自我中心视角和物体/世界中心视角之间转换的能力。

近一年（2025-08 至 2026-08），allocentric 表征在具身 AI 中的地位发生了显著变化。以 [3D-VLA](https://arxiv.org/abs/2403.09631) 和 [3D Diffusion Policy](https://arxiv.org/abs/2403.03954) 为代表的基础工作确立了 3D 表征对机器人操作的增益，而 2025-2026 年的研究则深入探索了如何更有效地将 allocentric 信息融入 VLA 模型和 VLM 的推理过程。

### 1.2 问题动机

当前 VLA 模型主要依赖 2D 视觉输入，缺乏对 3D 物理世界的几何感知。[GeoVLA](https://arxiv.org/abs/2508.09071) 指出，2D 视觉输入忽略了 3D 物理世界中丰富的几何信息，限制了机器人的空间感知和适应能力（ALLO-0001）。[3D-VLA](https://arxiv.org/abs/2403.09631) 进一步指出，现有 VLA 通过学习从感知到行动的直接映射，忽略了世界的动态变化以及动作与动态之间的关系（ALLO-0013）。[OmniManip](https://arxiv.org/abs/2501.03841) 则从 VLM 的角度指出，VLM 虽擅长高层常识推理，但缺乏精确操作所需的细粒度 3D 空间理解能力（ALLO-0010）。

### 1.3 综述范围与方法

本综述覆盖 2025-08 至 2026-08 期间的文献，同时纳入少量 2024 年的基础工作作为背景。检索通过多轮 web 搜索完成（arXiv API 受限），覆盖关键词包括 "allocentric representation"、"3D representation VLA"、"spatial reasoning VLM"、"object-centric manipulation" 等。共筛选 18 篇候选论文，其中 15 篇被接纳为证据来源。

---

## 2 背景工作

### 2.1 3D 表征在机器人策略中的早期应用

[3D Diffusion Policy (DP3)](https://arxiv.org/abs/2403.03954)（RSS 2024）是将 3D 视觉表征融入机器人策略学习的奠基性工作。该方法利用紧凑的 3D 点云表征，通过高效的点编码器从稀疏点云中提取视觉表示，并融入扩散策略（diffusion policy）框架。DP3 的核心贡献在于证明了简单 3D 表征即可显著提升视觉运动策略的泛化能力（ALLO-0015）。

[3D-VLA](https://arxiv.org/abs/2403.09631) 在此基础上进一步整合了 3D 感知、推理和动作。该模型基于 3D 大语言模型构建，引入交互令牌（interaction tokens）与具身环境交互，并通过具身扩散模型生成目标图像和点云。3D-VLA 策划了大规模 3D 具身指令数据集，证明了 3D 表征与语言-动作的联合训练可以提升推理、多模态生成和规划能力（ALLO-0014）。

### 2.2 VLM 空间推理的早期探索

[SpatialVLM](https://arxiv.org/abs/2401.12168) 首次系统性地赋予 VLM 空间推理能力。该工作通过互联网规模的空间数据预训练和思维链推理，使 VLM 能够理解距离、大小和物体间关系等空间概念（ALLO-0016）。SpatialRGPT（NeurIPS 2024）进一步引入了深度感知视觉编码器和区域级空间推理，并提出了覆盖室内、室外和模拟环境的 SpatialRGPT-Bench（ALLO-0017, ALLO-0018）。这两项工作为后续 allocentric 空间推理研究奠定了基础。

---

## 3 VLA 中的 Allocentric 3D 表征：三条技术路线

### 3.1 显式 3D 注入路线

显式 3D 注入路线的核心思想是将深度图、点云等 3D 传感器数据直接编码并融入 VLA 模型的表征空间。

**GeoVLA** ([arXiv:2508.09071](https://arxiv.org/abs/2508.09071)) 提出了一种并行处理 2D 视觉-语言信息和 3D 几何信息的框架。它将深度图转换为点云，使用定制的点嵌入网络（Point Embedding Network）独立生成 3D 几何嵌入，再与 VLM 提取的视觉-语言嵌入拼接，通过空间感知动作专家（3D-enhanced Action Expert）融合不同传感器模态的信息以产生精确动作序列。GeoVLA 在 LIBERO 和 ManiSkill2 仿真基准上取得 SOTA 结果，并在真实世界任务中展现出对高度适应性、尺度感知和视角不变性的显著鲁棒性（ALLO-0002, ALLO-0003）。

**SpatialActor** ([arXiv:2511.09555](https://arxiv.org/abs/2511.09555), AAAI 2026 Oral) 深入分析了显式 3D 注入路线的两大痛点：基于点的方法因稀疏采样导致细粒度语义丢失；基于图像的方法将语义和几何耦合在 2D 主干网络中，对深度噪声敏感。SpatialActor 提出语义-几何解耦框架：语义引导几何模块（Semantic-guided Geometric Module）自适应地融合来自噪声深度和语义引导专家先验的两种互补几何信息；空间变换器（Spatial Transformer）利用低层次空间线索实现精确的 2D-3D 映射。SpatialActor 在 RLBench 上达到 87.4%，在噪声条件下提升 13.9-19.4%，并显著增强了对新任务的少样本泛化能力（ALLO-0005, ALLO-0006, ALLO-0039）。

显式路线的共同优势在于直接获取几何信息，表征质量高；但面临传感器噪声、硬件异构性和数据集中深度覆盖不完整的工程瓶颈（ALLO-0007）。

### 3.2 隐式 3D 对齐路线

隐式 3D 对齐路线不依赖显式 3D 传感器输入，而是通过训练策略让模型从 2D 输入中隐式学习 3D 空间理解。

**Spatial Forcing (SF)** ([arXiv:2510.12276](https://arxiv.org/abs/2510.12276)) 是这一路线的代表。SF 的核心洞察是：现有 VLA 基于仅在 2D 数据上预训练的 VLM，缺乏准确的空间感知。显式 3D 方案面临传感器噪声、硬件异构性和深度覆盖不完整的挑战，而从 2D 图像估计 3D 信息的方法又受限于深度估计器的性能。SF 提出一种隐式对齐策略：将 VLA 的中间视觉嵌入与预训练 3D 基础模型产生的几何表征进行对齐，在中间层强制 VLA 编码更丰富的空间表征以增强动作精度。SF 在仿真和真实世界环境中均超越 2D 和 3D 方案，训练加速达 3.8 倍，并提升了数据效率（ALLO-0008, ALLO-0009, ALLO-0040）。

**ActiveVLA**（2026-01）从另一角度补充了隐式路线：通过将主动感知注入 VLA 模型，使机器人能够主动调整视角以获取更优的 3D 理解，从而在精准 3D 机器人操作任务中提升性能（ALLO-0028, ALLO-0029）。

隐式路线的吸引力在于降低了部署门槛——不需要额外的 3D 传感器即可获得空间理解能力。但当前仅 Spatial Forcing 一篇论文的实证支持，其表征上限和泛化边界仍有待验证。

### 3.3 符号化/工具化路线

符号化路线不修改 VLM 内部表征，而是通过外部工具或符号化重构将 3D 空间信息转化为 VLM 擅长的推理形式。

**OmniManip** ([arXiv:2501.03841](https://arxiv.org/abs/2501.03841), CVPR 2025) 提出以物体的规范空间（canonical space）为 allocentric 参照系。规范空间由物体的功能可供性（functional affordances）定义，提供了一种结构化且语义有意义的方式来描述交互原语（如点和方向）。这些原语作为桥梁，将 VLM 的常识推理转化为可操作的 3D 空间约束。OmniManip 设计了双闭环系统：高层规划通过原语重采样、交互渲染和 VLM 检查完成；低层执行通过 6D 位姿追踪实现。该方法在无需 VLM 微调的情况下实现了跨多种操作任务的零样本泛化（ALLO-0011, ALLO-0041）。

**SymPL**（CVPR 2026）直接针对 VLM 的 allocentric 推理短板。其核心发现是：VLM 在 egocentric 视角的空间推理上表现尚可，但切换到 allocentric 视角时性能显著下降，这源于训练数据中视角分布的偏差。SymPL 通过投影、抽象、二分和定位四个步骤，将复杂的 allocentric 空间推理转化为结构化符号布局问题，让 VLM 利用其内在的结构化推理能力而非直接处理 3D 几何。该方法在 COMFORT# 数据集上，closer 方向达 97.33%，visibility 达 91.41%，facing 达 91.50%（ALLO-0020）。但 SymPL 最频繁的错误来源是参考观察者面向方向向量的估计错误，说明符号化方法仍依赖上游感知精度（ALLO-0021）。

**GCA**（Geometrically-Constrained Agent, CVPR 2026）将 VLM 角色解耦为语义分析师和任务求解器两阶段。第一阶段将模糊自然语言查询形式化为几何任务约束（参考帧约束 + 客观约束），第二阶段在约束边界内调用工具箱（物体检测、方向估计、3D 重建、BEV 分析等）执行几何计算，并通过知识增强代码生成（KACG）输出推理结论。GCA 的核心洞察是：VLM 推理发生在有损的语义空间中，与高保真几何计算不对齐，因此需要将语义推理与几何计算解耦（ALLO-0027）。

### 3.4 三条路线的对比分析

| 维度 | 显式 3D 注入 | 隐式 3D 对齐 | 符号化/工具化 |
|------|-------------|-------------|-------------|
| 代表方法 | GeoVLA, SpatialActor | Spatial Forcing | OmniManip, SymPL, GCA |
| 3D 信息来源 | 传感器（深度/点云） | 3D 基础模型对齐 | 工具箱/符号重构 |
| 是否需要额外传感器 | 是 | 否 | 否 |
| 表征质量 | 高（直接几何） | 中（隐式编码） | 依赖工具精度 |
| 工程复杂度 | 高 | 低 | 中 |
| 训练需求 | 端到端训练 | 对齐训练 | 免训练/少训练 |
| 泛化能力 | 视角不变性好 | 有待验证 | 零样本泛化 |
| 主要局限 | 噪声/覆盖/异构 | 单篇论文支持 | 依赖上游感知 |

---

## 4 VLM 中的 Allocentric 空间推理：能力边界

### 4.1 能力缺失诊断

近一年的研究揭示了 VLM 在 allocentric 空间推理上的系统性短板。SymPL 发现 VLM 在 egocentric 推理上表现尚可，但切换到 allocentric 视角时性能显著下降（ALLO-0019）。这一差距不是"性能稍差"，而是"能力缺失"——训练数据中视角分布的偏差导致模型在 allocentric 推理上存在结构性盲区。

**HandVQA**（CVPR 2026）从细粒度角度进一步确认了这一发现。该工作构建了 160 万+多选题的基准，覆盖角度、距离和相对位置三个维度。结果显示，基础 VLM 在角度和距离推理上接近随机水平（ALLO-0024）。经 HandVQA 微调后，相对位置准确率从约 50%（随机水平）提升至 90% 以上，且学到的空间知识可迁移到下游任务（ALLO-0025）。这表明 allocentric 空间推理能力可以通过结构化训练习得，但基础 VLM 普遍缺失这一能力。

### 4.2 推理幻觉

**GCoT**（Grounded Chain-of-Thought, CVPR 2026）从更深层面诊断了 VLM 空间推理的可信度问题。GCoT 设计了三种推理范式进行对比：Answer-First（先答后定位）、Grounding-First（先定位后作答）和 Grounded CoT（逐步定位逐步推理）。实验结果令人警醒：LLaVA-13B 取得最高答案准确率 69.7%，但一致性指标仅 13.3%——意味着它能答对不少题目，但推理过程定位的视觉区域根本不在正确位置（ALLO-0022）。

更极端的是，在对抗鲁棒性实验中，所有模型的定位准确率普遍低于 5%，一致性指标几乎全部低于 5%（ALLO-0023）。这表明当前 VLM 的空间推理存在系统性而非偶发的视觉幻觉。值得注意的是，模型幻觉程度与参数量和通用 benchmark 性能无直接相关性——大型强模型同样存在严重一致性问题。

### 4.3 解决路径

针对 allocentric 推理短板，近一年的研究提出了三条解决路径：

1. **微调路径**：HandVQA 证明了通过结构化空间推理任务微调，可使 VLM 获得细粒度 3D 空间推理能力（ALLO-0025）。
2. **工具化路径**：GCA 和 SymPL 通过工具箱调用和符号化重构，绕过 VLM 的几何计算短板（ALLO-0027, ALLO-0020）。
3. **预训练路径**：SpatialVLM 和 SpatialRGPT 从预训练阶段注入空间知识（ALLO-0016, ALLO-0018）。

三条路径的交汇点在于：allocentric 推理的瓶颈不在于模型容量，而在于训练数据的空间分布偏差和推理过程中的几何信息损失。

---

## 5 Ego-Allocentric 转换与跨 Embodiment 迁移

### 5.1 VSI-Bench：评估 ego-allocentric 转换

Thinking in Space / VSI-Bench 是首个系统评估多模态大模型视觉-空间智能的基准。其评估维度之一即为 ego-allocentric 转换——在自我中心视角和环境中心视角之间转换的能力（ALLO-0030, ALLO-0031）。VSI-Bench 的设计表明，ego-allocentric 转换不仅是具身操作的工程需求，更是空间智能的核心维度。

### 5.2 Ego2Robot：工程实现

Ego2Robot（2026-08）展示了从自我中心人类视频到机器人训练数据的规模化合成。该方法将约 1,940 小时人类中心操作视频通过动作对齐转化为机器人数据，其中涉及 3D 空间对齐以实现 ego-to-robot 迁移（ALLO-0034, ALLO-0035）。allocentric 表征在此过程中提供了坐标系无关的中间表示，使不同视角和本体之间的迁移成为可能。

### 5.3 跨 Embodiment 迁移中的桥梁作用

SymPL 的 allocentric 推理和 OmniManip 的 canonical space 共同表明，allocentric 表征在跨 embodiment 迁移中起桥梁作用：它提供了不受特定视角或本体约束的空间表示，使得从一个本体到另一个本体的技能迁移有了一个共享的"空间语言"（ALLO-0042）。

---

## 6 开放问题

### 6.1 统一评估框架缺失

当前三条技术路线各自使用不同的评估基准（LIBERO/ManiSkill2、RLBench、COMFORT#），缺乏统一的 allocentric 表征评估框架。这导致跨路线比较困难，无法直接回答"哪条路线在什么场景下最优"（ALLO-0033）。

### 6.2 端到端融合的可行性

当前符号化路线依赖外部工具箱，增加了延迟和错误传播风险。将 allocentric 表征完全融入端到端 VLA 训练是否可行，仍是一个开放问题。Spatial Forcing 的隐式对齐策略提供了一种可能的端到端方案，但需要更多实证支持（ALLO-0037）。

### 6.3 对抗鲁棒性

GCoT 的发现表明，VLM 空间推理在对抗条件下近乎崩溃（G-Acc < 5%）。这对于需要高可信度的具身部署场景是重大隐患。当前三条路线均未系统评估对抗鲁棒性（ALLO-0023）。

### 6.4 长时程任务中的表征一致性

现有工作主要在短时程单步任务上验证，allocentric 表征在长时程多步任务中的一致性维持尚未被系统研究。

### 6.5 缺乏跨路线直接消融实验

当前没有论文直接比较显式 3D 注入、隐式对齐和符号化工具化三条路线在相同任务上的表现，这是最重要的实证空白。

---

## 6A 研究边界与范围声明

本综述的覆盖范围受以下边界约束：

1. **时间范围**：核心覆盖 2025-08 至 2026-08，少量 2024 年基础工作作为背景纳入。2024 年以前的工作（如 NeRF-based manipulation、早期 point cloud policy）未系统覆盖。
2. **检索方法**：因 arXiv API 受限，主要依赖 web 搜索发现论文，可能遗漏未被中文或英文技术博客覆盖的论文。候选池规模（18 篇）低于 scoping 模式的候选下限（100 篇），结论为初步性质。
3. **证据类型**：部分论文（SymPL、GCoT、HandVQA、GCA、ActiveVLA）因无法获取全文，证据基于 arXiv 摘要和公开技术解读提取，置信度标注为 inference 的证据占一定比例。
4. **主题边界**：本综述聚焦 allocentric 表征在 VLA 和 VLM 中的应用，不覆盖自动驾驶 BEV 感知、SLAM 建图等非具身操纵/导航领域的 allocentric 表征工作。
5. **跨 run 复用**：前一个 run（exocentric 人类数据发展）中涉及 3D 重建、深度感知的证据未直接复用，因两者关注点不同。

---

## 7 中心论点与结论

### 7.1 中心论点

本综述的中心论点是：**allocentric 表征已从具身 AI 的可选增强模块演变为 VLA 和 VLM 空间推理的核心能力，但技术路线的三路分化（显式注入、隐式对齐、符号化工具化）和评估碎片化阻碍了统一框架的形成。** 三条路线分别信任传感器、表征对齐和工具化推理，各自在表征质量、工程实用性和泛化能力上有明确取舍，但当前缺乏跨路线的直接消融实验和统一评估基准。

### 7.2 结论

本综述揭示了 allocentric 表征在具身 AI 中从背景概念到核心能力的转变。三条技术路线的分化反映了不同研究团队对"如何让机器理解 3D 空间"这一根本问题的不同回答：显式路线信任传感器，隐式路线信任表征对齐，符号化路线信任工具化推理。

VLM allocentric 推理的系统性短板（能力缺失、推理幻觉、对抗脆弱性）不仅是技术挑战，更触及 AI 可信度的核心。未来研究的交汇点可能在于：将隐式对齐的端到端优势与符号化的免训练灵活性结合，同时通过结构化训练修复 allocentric 推理的能力缺失。

但在此之前，领域亟需统一评估框架和跨路线直接消融实验，以建立可比较的实证基础。

---

## References

- [GeoVLA: Empowering 3D Representations in Vision-Language-Action Models](https://arxiv.org/abs/2508.09071)
- [SpatialActor: Exploring Disentangled Spatial Representations for Robust Robotic Manipulation](https://arxiv.org/abs/2511.09555)
- [Spatial Forcing: Implicit Spatial Representation Alignment for Vision-language-action Model](https://arxiv.org/abs/2510.12276)
- [OmniManip: Towards General Robotic Manipulation via Object-Centric Interaction Primitives as Spatial Constraints](https://arxiv.org/abs/2501.03841)
- [3D-VLA: A 3D Vision-Language-Action Generative World Model](https://arxiv.org/abs/2403.09631)
- [3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations](https://arxiv.org/abs/2403.03954)
- [SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning Capabilities](https://arxiv.org/abs/2401.12168)
- SpatialRGPT: Grounded Spatial Reasoning in Vision-Language Models (NeurIPS 2024)
- Keep it SymPL: Symbolic Projective Layout for Allocentric Spatial Reasoning in Vision-Language Models (CVPR 2026)
- Grounded Chain-of-Thought for Multimodal Large Language Models (CVPR 2026)
- HandVQA: Diagnosing and Improving Fine-Grained Spatial Reasoning about Hands in Vision-Language Models (CVPR 2026)
- Geometrically-Constrained Agent for Spatial Reasoning (CVPR 2026)
- ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation (2026)
- Thinking in Space: How Multimodal Large Language Models Learn to Reason Spatially Through Video (VSI-Bench, 2024)
- Multimodal Spatial Reasoning in the Large Model Era: A Survey and Benchmarks (2025)
- Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data (2026)
- A Survey of Embodied Learning for Object-centric Robotic Manipulation (2025)
