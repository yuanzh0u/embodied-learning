# Evidence Appendix: 近一年类脑模型的发展

- Time range: 2025-08 至 2026-08
- Events: 121
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-BRAIN-2026-0080

- Claim: 该文提出面向人类神经类器官的世界模型训练课程:三个渐进复杂度的闭环虚拟环境——条件回避(静态状态-动作偶然性)、一维捕食者-猎物(目标导向交互)、Pong 复刻(动态连续时间系统)——并完整形式化状态/动作空间、感觉编码、运动解码与奖惩反馈协议。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.04633](https://arxiv.org/abs/2509.04633) The Physical Basis of Prediction: World Model Formation in Neural Organoids via an LLM-Generated Curriculum
- Locator: 1 Introduction
- Evidence: 引言明确三项主要贡献,第一项即三环境课程;4.1-4.3 给出各协议细节。
- Quote: “We make three primary contributions. First, we introduce a curriculum of three distinct environments, each designed to probe a different facet of decision-making and world modeling, ranging from simple state avoidance to dynamic, long-horizon interception tasks.”
- Authors: brennen-hill

### EA-BRAIN-2026-0081

- Claim: 学习机制设计把 RL 奖惩转译为预测编码信号:奖励实现为可预测、低熵电刺激(如全网一致低频正弦波,或 UV 解笼锁多巴胺),惩罚实现为不可预测、高熵白噪声刺激(随机幅频、随机电极子集),以预测误差驱动突触可塑性,作为自由能原理的直接检验。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.04633](https://arxiv.org/abs/2509.04633) The Physical Basis of Prediction: World Model Formation in Neural Organoids via an LLM-Generated Curriculum
- Locator: 3.3 Inducing world model formation via predictive coding and reinforcement
- Evidence: 3.3 节给出奖惩两种实现(电刺激与多巴胺解笼锁)及白噪声惩罚设计。
- Quote: “In our framework, we leverage this concept by designing feedback signals to be either highly predictable (low surprise) or highly unpredictable (high surprise), serving as functional proxies for positive and negative reinforcement, respectively.”
- Authors: brennen-hill

### EA-BRAIN-2026-0082

- Claim: 评估设计主张超越行为指标、直接度量学习的物理相关物:以 fEPSP 斜率作突触强度代理(训练后持续上升为 LTP、下降为 LTD,可用 100 Hz 强直或 1 Hz 低频刺激主动诱导),辅以 GCaMP 双光子钙成像纵向追踪单个神经元与事后 AMPA/NMDA 受体免疫组化。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.04633](https://arxiv.org/abs/2509.04633) The Physical Basis of Prediction: World Model Formation in Neural Organoids via an LLM-Generated Curriculum
- Locator: 3.4 Evaluating the embodied world model: From task performance to synaptic correlates
- Evidence: 3.4 节给出电生理/光学/分子三层评估设计,各层指标均为神经科学成熟度量。
- Quote: “A sustained increase in this slope post-training is the canonical electrophysiological signature of long-term potentiation (LTP), while a decrease signifies long-term depression (LTD).”
- Authors: brennen-hill

### EA-BRAIN-2026-0083

- Claim: 提出 LLM 驱动的生成式课程设计:LLM 作为元控制器/AI Dungeon Master 自动生成与优化实验协议,包括为 FinalSpark Neuroplatform 生成含状态编码、动作解码、反馈与终止条件的完整 Python 脚本,把环境与课程设计变成高通量元学习循环。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.04633](https://arxiv.org/abs/2509.04633) The Physical Basis of Prediction: World Model Formation in Neural Organoids via an LLM-Generated Curriculum
- Locator: 4.4 Generative models for world generation: LLM-driven automated curriculum design
- Evidence: 4.4 节定义元控制器角色与元学习循环,并给出 Neuroplatform API 脚本生成提示示例。
- Quote: “To overcome the limitations of manual experimental design and to systematically explore the vast parameter space of environments and training protocols, we propose an automated framework where an LLM functions as a meta-controller or AI Dungeon Master.”
- Authors: brennen-hill

### EA-BRAIN-2026-0001

- Claim: SpikingBrain 是首个在非 NVIDIA(国产 MetaX)平台上大规模训练类脑大模型的公开工作,在数百卡集群上实现 76B 参数规模的稳定训练,为脉冲大模型的算力自主路线提供了端到端工程验证。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05276](https://arxiv.org/abs/2509.05276) SpikingBrain: Spiking Brain-inspired Large Models
- Locator: 1 Introduction
- Evidence: 引言明确声明首个非 NVIDIA 平台大规模类脑 LLM 训练并达到 76B 稳定训练。
- Quote: “This work represents, to our knowledge, the first large-scale training of brain-inspired LLMs on a non-NVIDIA platform, achieving stable training at 76B parameters.”
- Authors: yuqi-pan; yupeng-feng; jinghao-zhuang; et al.

### EA-BRAIN-2026-0002

- Claim: 经转换式持续预训练(150B/160B token,少于从头训练 2% 算力)后,SpikingBrain-7B 在下游基准恢复基座约 90% 性能(MMLU 65.84 vs Qwen2.5 的 74.21),76B 混合 MoE 模型基本闭合差距(MMLU 73.58,超过 Llama2-70B 的 69.57 与 Mixtral-8x7B 的 71.23)。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05276](https://arxiv.org/abs/2509.05276) SpikingBrain: Spiking Brain-inspired Large Models
- Locator: 5.1 Downstream Performance
- Evidence: 5.1 节正文与表 1/表 2 给出两模型与基线的完整对比,明确 ~90% 恢复与差距基本闭合。
- Quote: “As shown in Table 1 , our SpikingBrain-7B linear model recovers nearly 90% of the base model’s performance across benchmarks, reaching a level comparable to advanced Transformer models such as Mistral-7B and Llama3-8B.”
- Authors: yuqi-pan; yupeng-feng; jinghao-zhuang; et al.

### EA-BRAIN-2026-0003

- Claim: 长上下文推理:1M token 输入下 TTFT 相对全注意力基线实测加速 26.5×(H100,10 次平均);4M token 为按拟合曲线的保守外推估计 >100×,基线在该长度因资源限制无法实测。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05276](https://arxiv.org/abs/2509.05276) SpikingBrain: Spiking Brain-inspired Large Models
- Locator: 5.2 Long-context Efficiency
- Evidence: 5.2 节报告实测 26.5× 与明确标注的估计值 >100×。
- Quote: “at an input length of 1M tokens, the SpikingBrain-7B model achieves a 26.5× speedup in TTFT (Time to First Token) compared with the Qwen2.5 baseline using full attention and all-to-all communication.”
- Authors: yuqi-pan; yupeng-feng; jinghao-zhuang; et al.

### EA-BRAIN-2026-0004

- Claim: CPU 端部署:1B 压缩 SpikingBrain 线性模型经 llama.cpp 量化部署,在 64k/128k/256k 序列长度分别取得 4.04×/7.52×/15.39× 解码加速,且吞吐随输出长度保持恒定。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05276](https://arxiv.org/abs/2509.05276) SpikingBrain: Spiking Brain-inspired Large Models
- Locator: 5.3 CPU-side Inference
- Evidence: 5.3 节报告三级序列长度的 CPU 加速比与恒定开销特性。
- Quote: “Overall, SpikingBrain-1B achieves speedups of 4.04×, 7.52×, and 15.39× at sequence lengths of 64k, 128k, and 256k, respectively.”
- Authors: yuqi-pan; yupeng-feng; jinghao-zhuang; et al.

### EA-BRAIN-2026-0005

- Claim: 国产算力训练效率:MetaX C550 集群上 SpikingBrain-7B 训练达到 1558 TGS 与 23.4% MFU(8 路 DP+4 路 PP),与同配置 NVIDIA A800 的 25.8% 相当;训练连续运行超两周无中断。
- Stance: `support` | Confidence: `direct`
- Paper: [2509.05276](https://arxiv.org/abs/2509.05276) SpikingBrain: Spiking Brain-inspired Large Models
- Locator: 5.4 Performance on the MetaX Cluster
- Evidence: 5.4 节报告 TGS/MFU 数字、A800 对比与两周稳定性监控结论。
- Quote: “we achieve a TGS (Token Per Second) of 1558 and an MFU (Model FLOPs Utilization) of 23.4% (8-way DP, 4-way PP, PP micro-batch size 2, global batch size 512), reflecting high computational efficiency and effective resource utilization. This result is comparable to the measured MFU of 25.8% on an NVIDIA A800 80GB GPU cluster under the same parallel configuration, despite the use of older software versions on MetaX due to compatibility constraints.”
- Authors: yuqi-pan; yupeng-feng; jinghao-zhuang; et al.

### EA-BRAIN-2026-0014

- Claim: 作者提出首个面向深层 SNN 的 QIF 神经元离散化,据其所知是首个基于 QIF 的深层 SNN 演示,能表达 LIF 不具备的阈下振荡与输入变化敏感性,并证明可稳定训练。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.05168](https://arxiv.org/abs/2510.05168) Discretized Quadratic Integrate-and-Fire Neuron Model for Deep Spiking Neural Networks
- Locator: 1 Introduction
- Evidence: 引言明确 first 声明与动力学优势;4.2 节给出稳定性分析支撑'可稳定训练'。
- Quote: “To the best of our knowledge, this is the first demonstration of deep SNNs based on QIF neurons.”
- Authors: eric-jahns; davi-moreno; milan-stojkov; et al.

### EA-BRAIN-2026-0015

- Claim: 在 CIFAR-10/CIFAR-100(ResNet-19)上,该 QIF 离散化配合 TET 损失以 4 时间步分别达 96.86%(±0.13)与 80.62%(±0.24),2 时间步达 96.70/80.31,超过表内此前最佳直接训练方法(如 Surrogate Module 的 96.82%、Ternary Spike 的 80.20%)。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.05168](https://arxiv.org/abs/2510.05168) Discretized Quadratic Integrate-and-Fire Neuron Model for Deep Spiking Neural Networks
- Locator: 5.1 Comparison to Recent Works
- Evidence: 表 1 给出 QIF 与 QIF+TET 在 2/4 时间步下的三数据集结果及标准差。
- Quote: “QIF (Ours) + TET Neuron Model 4 / 4 / 4 96.86 0.13% 80.62 0.24% 70.38% 2 / 2 / 96.70 0.08% 80.31 0.27%”
- Authors: eric-jahns; davi-moreno; milan-stojkov; et al.

### EA-BRAIN-2026-0017

- Claim: CIFAR-10 DVS 上,该 QIF 离散化以 VGGSNN 架构 10 时间步达 83.00%(±0.50),超过 LSG(77.90%)等专注神经元模型改进的方法,但仍低于 TEBN 的 84.90%;ResNet-19 上达 80.70%(±0.10),超过 Ternary Spike 的 79.84%。
- Stance: `support` | Confidence: `direct`
- Paper: [2510.05168](https://arxiv.org/abs/2510.05168) Discretized Quadratic Integrate-and-Fire Neuron Model for Deep Spiking Neural Networks
- Locator: 5.1 Comparison to Recent Works
- Evidence: 表 2 汇总 DVS 上各方法准确率,正文说明 TEBN 因无法折叠归一化参数而引入推理开销。
- Quote: “QIF (Ours) Neuron Model VGGSNN 10 83.00 0.50% ResNet-19 10 80.70 0.10%”
- Authors: eric-jahns; davi-moreno; milan-stojkov; et al.

### EA-BRAIN-2026-0104

- Claim: 该综述主张:深度学习的既有成功建立在四项脑启发原则之上,而把脑机制移植进 AI 的失败案例往往反映的是对生物计算理解本身的局限,因此需要持续将神经科学新发现转化为人工智能模型,并以此反过来检验脑功能理论。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.04455](https://arxiv.org/abs/2511.04455) The brain as a blueprint: a survey of brain-inspired approaches to learning in artificial intelligence
- Locator: 1 Introduction
- Evidence: 引言中作者把移植失败归因于对生物计算的理解局限,并据此提出双向检验(翻译神经科学进 AI、用 AI 测脑理论)的纲领。
- Quote: “In parallel, this also suggests that failures to implement aspects of the brain into AI models often reflects limits in our understanding of biological computations.”
- Authors: guillaume-etter

### EA-BRAIN-2026-0105

- Claim: 综述转述被引工作:放宽反向传播的严格权重对称性后学习仍然有效——仅共享权重符号的 sign symmetry 网络在 ImageNet 等数据集上已接近反向传播的精度,说明精确权重传输并非深度网络学习的必要条件。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2511.04455](https://arxiv.org/abs/2511.04455) The brain as a blueprint: a survey of brain-inspired approaches to learning in artificial intelligence
- Locator: 2.2.3 Sign symmetry
- Evidence: 2.2.3 节转述 sign symmetry 在 ImageNet 上接近 BP 精度,并连同 feedback alignment 说明权重对称可放宽。
- Quote: “Interestingly, networks trained with sign symmetry have also demonstrated promising performance on challenging datasets like ImageNet, approaching the accuracy of backpropagation in some cases.”
- Authors: guillaume-etter

### EA-BRAIN-2026-0106

- Claim: 综述转述被引工作:固定反馈权重的 FW-DTP 无需学习反馈通路即可向隐层传递有效目标,显著降低训练计算成本,并在多个图像分类数据集上常取得高于标准 DTP 的测试性能——说明层间目标重构的训练并非目标传播有效性的必要条件。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2511.04455](https://arxiv.org/abs/2511.04455) The brain as a blueprint: a survey of brain-inspired approaches to learning in artificial intelligence
- Locator: 2.2.7 Fixed-weight difference target propagation
- Evidence: 2.2.7 节描述 FW-DTP 固定反馈权重带来的成本下降与性能改进,并据此质疑反馈权重学习的必要性。
- Quote: “FW-DTP can achieve improved stability during training and often exhibits higher test performance compared to standard DTP on various image classification datasets.”
- Authors: guillaume-etter

### EA-BRAIN-2026-0038

- Claim: NeuronSpark-0.9B(874M 参数)从随机初始化、无 Transformer 蒸馏完成训练:85,000 步预训练(约 1.4B token)损失降至 3.6(曲线从 9.0 降到 3.5),6,500 步 SFT 后损失 2.1,8×RTX 4090 上吞吐 960 tokens/sec,并展示基础中文多轮对话。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16148](https://arxiv.org/abs/2603.16148) NeuronSpark: A Spiking Neural Network Language Model with Selective State Space Dynamics
- Locator: 5.2 Results
- Evidence: 表 2 给出完整训练指标,正文补充损失曲线范围、吞吐与两个定性对话示例。
- Quote: “Table 2: Training results for NeuronSpark -0.9B. Metric Pretrain SFT Training loss 3.6 2.1 Parameters 874M Training steps 85,000 6,500 Tokens seen 1.4B 0.4B Hardware 8 NVIDIA RTX 4090”
- Authors: zhengzheng-tang

### EA-BRAIN-2026-0039

- Claim: 与既有 SNN 语言模型对照,NeuronSpark-0.9B(874M)是唯一同时满足从零训练、核心脉冲计算、通用生成、对话四项的模型;SpkGPT(216M)缺对话能力,SpkBERT/SpkBERT-110M(110M)依赖蒸馏且无通用生成;参数规模约为此前上限的 4 倍。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16148](https://arxiv.org/abs/2603.16148) NeuronSpark: A Spiking Neural Network Language Model with Selective State Space Dynamics
- Locator: 5.4 Comparison with Existing SNN Language Models
- Evidence: 表 4 以 From/Core/Gen/Dia 四列勾选对比四个模型;Related Work 给出此前规模上限 216M 的依据。
- Quote: “Table 4: Comparison with existing SNN language models. Model Par. From Core Gen. Dia. SpkBERT-110M 110M ✗ ✓ ✗ ✗ SpkBERT 110M ✗ ✓ ✗ ✗ SpkGPT 216M ✓ ✓ ✓ ✗ NeuronSpark -0.9B 874M ✓ ✓ ✓ ✓”
- Authors: zhengzheng-tang

### EA-BRAIN-2026-0040

- Claim: 训练稳定性消融:7 个替代架构变体(各训练 1K-12K 步)损失全部停滞在 7.0 以上(如去除跨层均衡的 MPD-AGL 变体 7.21、E[K] 下限变体 7.47),仅最终完整架构在 85K 步达到 3.5,说明稳定化组件是该规模下可训练的必要条件。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16148](https://arxiv.org/abs/2603.16148) NeuronSpark: A Spiking Neural Network Language Model with Selective State Space Dynamics
- Locator: Architecture Ablation via Training Stability
- Evidence: 表 3 列出 7 个变体的步数与损失;正文明确所有变体损失>7.0、仅最终架构到 3.5。
- Quote: “Table 3: Ablation variants. All stagnated above loss 7.0; only the final architecture reached 3.5. Variant Steps Loss What Changed Final V1 85K 3.5 Full architecture MPD-AGL + no Phase 2 4.8K 7.21 Adaptive surrogate gradient, removed cross-layer equalization”
- Authors: zhengzheng-tang

### EA-BRAIN-2026-0041

- Claim: 训练后可解释性分析(40 句中文、541 token)显示计算分配由结构/句法角色而非预测难度驱动:排除 BOS 哨兵 token 后 surprisal 与 E[K] 相关性降至近零,mean E[K] 在所有 surprisal 区间平坦(7.4-7.9);功能词/标点比内容词少约 0.7 步;学习到的神经元 67.3% 为快时间常数、32.7% 为慢。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.16148](https://arxiv.org/abs/2603.16148) NeuronSpark: A Spiking Neural Network Language Model with Selective State Space Dynamics
- Locator: 5.5 Biological Interpretability Analysis
- Evidence: 图 4/图 5 及正文给出 E[K] 分层分布、BOS 混混杂控制后的相关性与快慢神经元占比。
- Quote: “Excluding BOS tokens, the correlation drops to (near zero), and binned analysis confirms that mean E[K] is essentially flat ( 7.4–7.9) across all surprisal ranges. This reveals that PonderNet’s computation budget is governed by structural/syntactic role rather than predictive difficulty”
- Authors: zhengzheng-tang

### EA-BRAIN-2026-0008

- Claim: SDLLM 是首个完全消除矩阵乘法、仅以稀疏加法执行的脉冲驱动大语言模型,在 LLaMA2-7B/13B、LLaMA3-8B、Qwen2.5-14B 多个基座上实现,并将 SNN 与低位量化边缘方案首次系统对比。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.16475](https://arxiv.org/abs/2604.16475) Spike-driven Large Language Model
- Locator: 7 Conclusion
- Evidence: 结论首句明确 first 声明与多基座覆盖。
- Quote: “In this work, we present the first spike-driven LLM that eliminates matrix multiplication entirely by leveraging sparse addition, built upon multiple LLM architectures, addressing the issues of insufficient spiking representation and sparsity at the LLM level.”
- Authors: han-xu; xuerui-qiu; baiyu-chen; et al.

### EA-BRAIN-2026-0009

- Claim: 在 LLaMA-2-7B/13B 上,SDLLM 相比 SpikeLLM 任务性能分别提升 5.69% 与 4.23%,同时 FLOPs 降低 1.4×、能耗降低 7×;摘要汇总称对既有脉冲 LLM 能耗降低 7×、精度提升 4.2%。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.16475](https://arxiv.org/abs/2604.16475) Spike-driven Large Language Model
- Locator: 5.1 Main Results
- Evidence: 5.1 节给出对 SpikeLLM 的具体对比数字;摘要给出对既有脉冲 LLM 的 7×/4.2% 汇总。
- Quote: “Experimental results show that, on the LLaMA-2-7B and LLaMA-2-13B models, SDLLM achieves higher task performance by 5.69% and 4.23%, respectively, compared to SpikeLLM. Additionally, SDLLM reduces FLOPs by 1.4 , and energy consumption by 7 , outperforming SpikeLLM in both accuracy and efficiency.”
- Authors: han-xu; xuerui-qiu; baiyu-chen; et al.

### EA-BRAIN-2026-0010

- Claim: LLaMA2-7B 上 SDLLM(4bit 权重-1.58bit 脉冲)零样本 QA 平均 61.09、功率 0.67J,超过最佳低位基线 DuQuant 的 60.57(3.97J),相对全精度 63.72(31.77J)仍低约 2.6 个百分点。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.16475](https://arxiv.org/abs/2604.16475) Spike-driven Large Language Model
- Locator: 5 Experiments
- Evidence: 表 5 完整给出 SDLLM、全精度与七种低位基线的精度/FLOPs/功率。
- Quote: “Our core focus is to explore whether LLMs at the tens-of-billions scale can be constructed as spike-driven SNNs that replace dense matrix multiplications with sparse additions through spike encoding.”
- Authors: han-xu; xuerui-qiu; baiyu-chen; et al.

### EA-BRAIN-2026-0011

- Claim: 在更新的 Qwen2.5-14B 上,4bit 权重-1.58bit 脉冲编码平均 72.51,大幅高于同位宽 RTN 的 39.35 与 GPTQ 的 36.73,表明脉冲语义量化对更强基座的退化远小于常规量化。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.16475](https://arxiv.org/abs/2604.16475) Spike-driven Large Language Model
- Locator: 5 Experiments
- Evidence: 表 6 给出 Qwen2.5-14B 下脉冲方案与 RTN/GPTQ/SmoothQuant 对比。
- Quote: “We apply the SDLLM method (our -SQP two-step spike encoding with symmetric quantization–based bidirectional encoding and segmented membrane potentials as sparse components, which replaces dense matrix multiplications with spike-driven sparse additions) to LLaMA2-7B, LLaMA2-13B, and LLaMA3-8B, as well as the newer LLM Qwen2.5-14B, and systematically evaluate performance on commonsense question answering (PIQA, ARC-easy, ARC-challenge, HellaSwag, and WinoGrande) and more complex language generatio”
- Authors: han-xu; xuerui-qiu; baiyu-chen; et al.

### EA-BRAIN-2026-0013

- Claim: 与低位量化边缘方案相比,SDLLM 在保持竞争精度的同时最多实现 13× 能耗降低,首次给出 SNN 可与低位边缘方案在精度与能效上抗衡的证据。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.16475](https://arxiv.org/abs/2604.16475) Spike-driven Large Language Model
- Locator: 7 Conclusion
- Evidence: 结论原句给出 up to 13×。
- Quote: “Our results show that, compared to low-bit edge solutions, SDLLM achieves competitive accuracy while reducing energy consumption by up to 13 . This work provides the first compelling evidence that SNNs are not only feasible for LLMs but also have the potential to rival low-bit edge solutions in both accuracy and energy efficiency”
- Authors: han-xu; xuerui-qiu; baiyu-chen; et al.

### EA-BRAIN-2026-0092

- Claim: SpikeMLLM 是首个面向多模态大模型(MLLM)的脉冲框架,统一既有 ANN 量化方法于脉冲表示空间,并把脉冲 LLM 路线从单模态文本扩展到多模态。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.18610](https://arxiv.org/abs/2604.18610) SpikeMLLM: Spike-based Multimodal Large Language Models via Modality-Specific Temporal Scales and Temporal Compression
- Locator: 1. Introduction
- Evidence: 引言明确自述 the first spike-based framework for MLLMs(注意介词 within 与摘要版 in 略有差异,以引言版为准)。
- Quote: “To address these challenges, we propose SpikeMLLM , the first spike-based framework for MLLMs, which unifies existing ANN quantization methods within the spiking representation space.”
- Authors: han-xu; zhiyong-qin; di-shang; et al.

### EA-BRAIN-2026-0093

- Claim: 在激进时间步压缩(15→2)下,SpikeMLLM 对 FP16 基线的五基准平均性能差距仅 1.03%(Qwen2VL-7B)与 0.72%(InternVL2-8B),四个模型趋势一致。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.18610](https://arxiv.org/abs/2604.18610) SpikeMLLM: Spike-based Multimodal Large Language Models via Modality-Specific Temporal Scales and Temporal Compression
- Locator: 4.1. Main Results
- Evidence: 4.1 节给出平均差距数字与时间步压缩幅度。
- Quote: “After incorporating MSTS and TC-LIF, at , the average performance gap to the FP16 baseline (across five benchmarks) is only 1.03% on Qwen2VL-7B and 0.72% on InternVL2-8B, while reducing the timestep from 15 to”
- Authors: han-xu; zhiyong-qin; di-shang; et al.

### EA-BRAIN-2026-0094

- Claim: 文本模态对时间步分配显著更敏感:同一 prefill 成本下,文本时间步不足导致 OCRBench 32、DocVQA 5.31 的严重退化,把时间步转给文本后恢复到 OCRBench 717、DocVQA 84.20。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.18610](https://arxiv.org/abs/2604.18610) SpikeMLLM: Spike-based Multimodal Large Language Models via Modality-Specific Temporal Scales and Temporal Compression
- Locator: 4.2. Ablation Study
- Evidence: 4.2 消融给出文本/视觉时间步分配的量化敏感性证据。
- Quote: “insufficient text timesteps (e.g., ) cause severe performance degradation (OCRBench: 32, DocVQA: 5.31), whereas allocating more timesteps to the text modality at the same cost (e.g., ) substantially recovers performance (OCRBench: 717, DocVQA: 84.20)”
- Authors: han-xu; zhiyong-qin; di-shang; et al.

### EA-BRAIN-2026-0095

- Claim: 部署导向协同设计:SMIC 28nm RTL 加速器实现 393.7 token/s 对 A800 FP16 43.5 token/s(9.06× 吞吐),系统功耗 7.13 W 对 184 W(25.8× 降低)。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.18610](https://arxiv.org/abs/2604.18610) SpikeMLLM: Spike-based Multimodal Large Language Models via Modality-Specific Temporal Scales and Temporal Compression
- Locator: 4.3. Deployment-oriented Co-designed System Study
- Evidence: 4.3 节给出吞吐与功耗对比数字。
- Quote: “the proposed design shows 9.06 higher throughput (393.7 token/s vs. 43.5 token/s). In terms of system power, the proposed design operates at 7.13 W, compared with 184 W for the GPU reference, corresponding to 25.8 lower power.”
- Authors: han-xu; zhiyong-qin; di-shang; et al.

### EA-BRAIN-2026-0020

- Claim: 作者提出设计新一代脉冲神经元的功能性视角:高效训练、自适应发放、架构兼容、脉冲驱动推理四性质必须同时满足,并据此指出 LIF 训练效率低、PSN 与主流脉冲 Transformer 架构兼容性存疑、ILIF/NILIF 缺乏膜电位自适应性。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12365](https://arxiv.org/abs/2604.12365) Adaptive Spiking Neurons for Vision and Language Modeling
- Locator: 1. Introduction
- Evidence: 引言以四性质主张与表 1 对既有神经元的逐一评估支撑该视角。
- Quote: “We argue that the four basic characteristics of spiking neurons—efficient training, adaptive firing, architecture compatibility, and spike-driven inference—must be considered simultaneously.”
- Authors: chenlin-zhou; sihang-guo; jiaqi-wang; et al.

### EA-BRAIN-2026-0021

- Claim: ImageNet-1k 上,同架构(Spikingformer-8-384,4 时间步)受控对比中 NASN 达 75.53% Top-1,超过 LIF 版 Spikingformer† 1.18 个点、超过 NILIF 版 0.12 个点,能耗折算 5.67 mJ。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12365](https://arxiv.org/abs/2604.12365) Adaptive Spiking Neurons for Vision and Language Modeling
- Locator: 4.1. ImageNet-1k Classification
- Evidence: 4.1 节正文与表 2 给出同架构三神经元对比。
- Quote: “Our model achieves 75.53 Top-1 accuracy, exceeding the baseline LIF-based Spikingformer † by 1.18 and outperforming NILIF-based Spikingformer † by 0.12 under the same architectural settings.”
- Authors: chenlin-zhou; sihang-guo; jiaqi-wang; et al.

### EA-BRAIN-2026-0023

- Claim: GLUE 上 NASN 版 WE-Spikingformer 平均 67.5%,比 NILIF 版高 1.2 个点;在 softmax-free 脉冲驱动类别内大幅超过 SpikeBERT(59.7%)与 LIF-BERT(34.6%),但作者承认保留 softmax 与 GeLU 的 SpikeLM 性能更高。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12365](https://arxiv.org/abs/2604.12365) Adaptive Spiking Neurons for Vision and Language Modeling
- Locator: 4.3. Natural language understanding
- Evidence: 4.3 节给出 GLUE 平均值与三类基线对比及 SpikeLM 定性说明。
- Quote: “Our method achieves an average accuracy of 67.5%, outperforming the NILIF version of WE-Spikingformer by 1.2%.”
- Authors: chenlin-zhou; sihang-guo; jiaqi-wang; et al.

### EA-BRAIN-2026-0024

- Claim: 扩展实验显示:参数从 0.4B 增至 1.0B 时 QAT 29.4→29.8、CRT 43.3→43.5(增益很小);预训练 token 从 0.1B 增至 0.5B 时 NASN(1.0B) 的 QAT 从 29.8 升至 35.5(提升 5.7)、CRT 从 43.5 升至 45.1,作者据此称方法可适应更大规模预训练。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.12365](https://arxiv.org/abs/2604.12365) Adaptive Spiking Neurons for Vision and Language Modeling
- Locator: 5.1. Discussion
- Evidence: 5.1 节给出参数与预训练数据两组扩展数字。
- Quote: “NASN (1.0B) with 0.1B tokens vs. NASN (1.0B) with 0.5B tokens. QAT: 29.8 vs. 35.5 ; CRT: 43.5 vs. 45.1 .”
- Authors: chenlin-zhou; sihang-guo; jiaqi-wang; et al.

### EA-BRAIN-2026-0044

- Claim: BiSpikCLM 是首个全二值脉冲、无 MatMul 的因果语言模型:SFSA 在注意力模块层面同时消除 softmax、指数函数与浮点乘法(表 1 中唯一三项全勾的解码器式模型),架构基于 OPT 家族,经 SpAD 从随机初始化训练,规模 1.3B。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13859](https://arxiv.org/abs/2605.13859) BiSpikCLM: A Spiking Language Model integrating Softmax-Free Spiking Attention and Spike-Aware Alignment Distillation
- Locator: 1 Introduction
- Evidence: 引言贡献第一条与表 1 属性对比共同支撑'first'声明与三属性勾选。
- Quote: “We propose BiSpikCLM , the first binary spiking MatMul-free causal language model equipped with a fully spike-driven attention mechanism. Our SFSA replaces the causal self-attention, which relies on floating-point operations and softmax, enabling efficient autoregressive language modeling with binary spikes.”
- Authors: sihang-guo; chenlin-zhou; jiaqi-wang; et al.

### EA-BRAIN-2026-0045

- Claim: BiSpikCLM-1.3B 仅用 10B 训练 token(OPT-1.3B 需 180B,约 5.6%)达到 42.19% 零样本平均准确率(4 时间步),接近 OPT-1.3B 的 49.73%,每次推理仅耗其 10.6% 能量;2 时间步时保持 41.33% 准确率与 5.88% 能量成本。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13859](https://arxiv.org/abs/2605.13859) BiSpikCLM: A Spiking Language Model integrating Softmax-Free Spiking Attention and Spike-Aware Alignment Distillation
- Locator: 1 Introduction
- Evidence: 引言贡献第三条给出完整的 token/精度/能量三元组对比。
- Quote: “With only 10B training tokens, significantly fewer than the 180B tokens used to train OPT-1.3B, our SpAD framework enables BiSpikCLM-1.3B to achieve 42.19% zero-shot accuracy on common reasoning benchmarks using 4 time steps, approaching the 49.73% of OPT-1.3B, while consuming just 10.6% of the energy per inference. Remarkably, even at 2 time steps, the model maintains 41.33% accuracy with only 5.88% of the energy cost.”
- Authors: sihang-guo; chenlin-zhou; jiaqi-wang; et al.

### EA-BRAIN-2026-0046

- Claim: 能耗折算(45nm 神经形态芯片仿真,SOPs 对 FLOPs):125M 规模 BiSpikCLM 每样本 9.43 mJ vs ANN 基线 126.01 mJ,同时保持 93% 以上精度;0.125B-1.3B 全规模仅 4.16%-5.87% 计算成本;时间步 2→4 在 125M 上把准确率从 36.05% 提到 36.50%。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13859](https://arxiv.org/abs/2605.13859) BiSpikCLM: A Spiking Language Model integrating Softmax-Free Spiking Attention and Spike-Aware Alignment Distillation
- Locator: 4.3 Energy Consumption
- Evidence: 4.3 节给出能耗折算方法与三组关键数字,并指出时间步-能耗权衡。
- Quote: “BiSpikCLM consumes an order of magnitude less energy than ANN baselines (e.g., 9.43 mJ vs. 126.01 mJ at 125M) while achieving over 93% of the accuracy. Across 0.125B–1.3B parameters, it maintains competitive performance at only 4.16%–5.87% of the computational cost.”
- Authors: sihang-guo; chenlin-zhou; jiaqi-wang; et al.

### EA-BRAIN-2026-0047

- Claim: 与 SpikeLLM 对比:BiSpikCLM 的 SNN/ANN 精度比率在各规模上稳定于 82%-95%,持续高于 SpikeLLM 的 65.41%-82.55%(如 BiSpikCLM 1.3B/T=4 为 42.19%/84.84%,SpikeLLM 7B/W2A16 为 49.92%/78.17%,70B/W2A16 为 60.47%/82.55%),且以更小模型与纯二值脉冲形式达成;作者归因于 spike-aware 蒸馏。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13859](https://arxiv.org/abs/2605.13859) BiSpikCLM: A Spiking Language Model integrating Softmax-Free Spiking Attention and Spike-Aware Alignment Distillation
- Locator: Appendix G Comparison with SpikeLLM
- Evidence: 附录 G 表 4 跨规模给出两路线的精度与 SNN/ANN 比率,正文总结 82-95% 对比结论。
- Quote: “Notably, the SNN/ANN ratio of BiSpikCLM is consistently higher (82–95%) than that of SpikeLLM, indicating that our spike-based models retain more of the original ANN performance. This improvement is largely attributed to our spike-aware knowledge distillation framework, which effectively transfers information from ANN teachers to spiking students.”
- Authors: sihang-guo; chenlin-zhou; jiaqi-wang; et al.

### EA-BRAIN-2026-0049

- Claim: 数据扩展实验:1.3B 模型训练 token 从 10B 增至 25B,零样本平均准确率从 41.33% 升至 44.39%(+3.06%);125M 从 1B 增至 5B 提升 1.05%(36.05%→37.10%);损失曲线平滑收敛,且 25B 版本能正确回答事实性问题(美国首都)而 10B 版本不能,表明架构对数据规模仍有正响应。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.13859](https://arxiv.org/abs/2605.13859) BiSpikCLM: A Spiking Language Model integrating Softmax-Free Spiking Attention and Spike-Aware Alignment Distillation
- Locator: Appendix M Effect of Training Scale and Conversational Ability
- Evidence: 附录 M 表 9/表 10 给出 token 扩展的定量增益与对话质量对比。
- Quote: “More impressively, the 1.3B model’s average accuracy increased by 3.06% when scaling from 10B to 25B tokens.”
- Authors: sihang-guo; chenlin-zhou; jiaqi-wang; et al.

### EA-BRAIN-2026-0110

- Claim: 该综述定位:既有 SNN 训练综述以描述性为主,方法散落在异构代码库(数据集、预处理、架构、优化细节与报告约定各异)中,无法提供标准化的并排评测;本文以'统一分类学综述+NeuroTrain 开源基准框架'双贡献填补该缺口。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.15058](https://arxiv.org/abs/2605.15058) NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework
- Locator: 1 Introduction
- Evidence: 引言把'公平比较难'归因于异构代码库与实验约定,并把基准化列为核心贡献以区别于常规综述。
- Quote: “Existing surveys are primarily descriptive: they synthesize ideas and trends, but typically cannot provide standardized, side-by-side evaluations because methods live in heterogeneous codebases with differing datasets, preprocessing pipelines, architectures, optimization details, and reporting conventions”
- Authors: alessio-caviglia; filippo-marostica; roberta-bardini; et al.

### EA-BRAIN-2026-0112

- Claim: STBP 式代理梯度 BPTT 管线已成为面向深度学习的 SNN 研究中最广泛采用的训练模板,因其可自然映射到现代自动微分框架并扩展到深层架构与大数据集。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.15058](https://arxiv.org/abs/2605.15058) NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework
- Locator: 4.2 Training Algorithms
- Evidence: 4.2 节在梳理 Lee/STBP/SuperSpike/SLAYER/EXODUS 谱系后给出'最广泛采用模板'判断,并指出其可扩展性来源。
- Quote: “the STBP -style surrogate-gradient BPTT pipeline has arguably become the most widely adopted template in deep-learning-oriented SNN research, largely because it maps naturally onto modern autodiff frameworks and scales to deep architectures and large datasets.”
- Authors: alessio-caviglia; filippo-marostica; roberta-bardini; et al.

### EA-BRAIN-2026-0115

- Claim: NeuroTrain 首发基准快照:在 8 个数据集(MNIST、F-MNIST、CIFAR-10、SVHN、N-MNIST、DVS Gesture、DVS CIFAR-10、SHD)上对可用 trainer 与 FC/RC/Conv 三类小规模架构做正交 campaign,每实验 20 epochs、Optuna 10 trials,整场约 850 GPU 小时;作者明确该快照不用于确立算法最终排名,完整结果以 GitHub 活资源维护。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.15058](https://arxiv.org/abs/2605.15058) NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework
- Locator: 5.4 Benchmarking framework
- Evidence: 5.4 节与图 4 说明给出快照实验设置、GPU 预算与数据集/架构覆盖,并声明结果不构成最终排名。
- Quote: “Each experiment was run for 20 epochs, and hyperparameter exploration was performed using Optuna with 10 trials per experiment for a total of about 850 GPU hours.”
- Authors: alessio-caviglia; filippo-marostica; roberta-bardini; et al.

### EA-BRAIN-2026-0026

- Claim: 作者提出免训练、即插即用的 NLSpiking 框架:把 Transformer 非线性(Softmax/SiLU/RMSNorm)分解为除法、指数、范数三个原语,用标准 LIF 群体计算加位缩放实现,与既有 ANN-to-SNN 转换管线兼容且无需任何微调。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.20289](https://arxiv.org/abs/2605.20289) Plug-and-Play Spiking Operators: Breaking the Nonlinearity Bottleneck in Spiking Transformers
- Locator: 1 Introduction
- Evidence: 引言给出问题陈述与肯定回答;第 4 节给出三个模块化构件的设计。
- Quote: “In this work, we answer this question affirmatively by developing training-free spike-based replacements that are compatible with standard LIF dynamics.”
- Authors: xinzhe-yuan; xiang-peng; bin-gu; et al.

### EA-BRAIN-2026-0027

- Claim: 模型级受控实验(只替换非线性算子、其余不变)显示平均精度变化可忽略:LLaMA-3-8B 为 -0.003、Mistral-7B 为 +0.000,SpikeLLM 转换的 LLaMA-2-7B(T=2,W2A16)为 -0.000,五项零样本任务逐项变化均在 ±0.008 内。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.20289](https://arxiv.org/abs/2605.20289) Plug-and-Play Spiking Operators: Breaking the Nonlinearity Bottleneck in Spiking Transformers
- Locator: 6.1 Function-Level Evaluation.
- Evidence: 表 1 给出四个 ANN LLM 与两个 SpikeLLM 转换模型的逐任务与平均精度变化。
- Quote: “ANN LLaMA-3-8B ( 8 ) Original 0.736 0.792 0.542 0.776 0.807 0.730 NLSpike ( ) -0.008 -0.000 +0.001 +0.000 -0.004 -0.003”
- Authors: xinzhe-yuan; xiang-peng; bin-gu; et al.

### EA-BRAIN-2026-0028

- Claim: 算子级(8-bit 量化)评测中,NLS-Softmax 在所有测试维度上取得最低平均误差且最大误差受整数实现约束;NLS-RMS 平均误差低于 blockwise(块 32/64)与 Sorbet 基线并跨维度稳定,而 blockwise 仅在维度对齐块划分时才准确。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.20289](https://arxiv.org/abs/2605.20289) Plug-and-Play Spiking Operators: Breaking the Nonlinearity Bottleneck in Spiking Transformers
- Locator: 5 Performance Analysis
- Evidence: 图 3/图 4 汇总算子级误差,正文与图注给出与基线的定性排序。
- Quote: “NLS-Softmax achieves the lowest mean error across dimensions while keeping bounded maximum error under integer-only implementation, and NLS-RMS yields lower mean errors than blockwise and Sorbet baselines with stable performance across dimensions.”
- Authors: xinzhe-yuan; xiang-peng; bin-gu; et al.

### EA-BRAIN-2026-0029

- Claim: 定理 5.1 证明三类非线性(Softmax/SiLU/RMSNorm)的总近似误差可加性分解为少量隔离项:查表式指数、脉冲除法与递归范数估计各贡献一个可控误差项,构成明确的精度-内存权衡,推荐设置下误差相对低精度推理的量化噪声可忽略,查表仅需 8/16 位条目。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.20289](https://arxiv.org/abs/2605.20289) Plug-and-Play Spiking Operators: Breaking the Nonlinearity Bottleneck in Spiking Transformers
- Locator: 5 Performance Analysis
- Evidence: 5 节给出定理 5.1 陈述、加性分解观察与推荐设置(含 LUT 内存讨论)。
- Quote: “A key observation from Theorem 5.1 is that, for all three nonlinearities, the total approximation error decomposes additively into a small number of well-isolated terms.”
- Authors: xinzhe-yuan; xiang-peng; bin-gu; et al.

### EA-BRAIN-2026-0086

- Claim: SpikeVLA 是首个基于 SNN 的 VLA 架构,把视觉编码(Spike-V,脉冲 Transformer+差分脉冲神经元)、多模态推理(Spike-L,LLaMA-8B+IF 神经元+token 级脉冲稀疏)与动作策略(Spike-A,拉普拉斯核群体编码+全连接 SNN+PPO)统一为事件驱动范式,作者明确定位为性能-能效权衡。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.27807](https://arxiv.org/abs/2606.27807) SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks
- Locator: 1 Introduction
- Evidence: 引言原句给出 first 声明与三模块定位;3.2-3.4 给出各模块设计。
- Quote: “To address these challenges, we propose SpikeVLA, the first VLA architecture built on spiking neural networks, which represents a trade-off between performance and efficiency, as shown in Fig. 1 . SpikeVLA consists of three complementary modules. Spike-V provides energy-efficient visual representations through event-driven spiking visual encoding.”
- Authors: ruiqi-song; dujun-nie; siyu-teng; et al.

### EA-BRAIN-2026-0087

- Claim: 在 VLN-CE R2R Val-Unseen(RGB-only、无路点)上,SpikeVLA 取得 NE 5.38/OS 63.4/SR 53.3/SPL 47.9,与最强 RGB 基线 NaVILA(5.28/61.5/53.9/49.3)竞争力相当(OS 更高、SR/SPL 略低),同时内存 6249.18MB(NaVILA 16119.98MB)、能耗 49.09J(141.25J)、ACEs 1196.16(3930.21)。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.27807](https://arxiv.org/abs/2606.27807) SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks
- Locator: 4.1 Experimental Setups
- Evidence: 表 1 完整给出方法行与资源效率列;正文称内存从 16.1GB 降到 6.2GB、能耗约为 NaVILA 的 34%。
- Quote: “NaVid ( 39 ) RGB. ✗ 5.47 49.0 37.0 35.0 14231.96 157.29 4376.68 UniNaVid ( 38 ) RGB. ✗ 5.58 53.3 47.0 42.7 14231.96 157.29 4376.68 NaVILA ( 8 ) RGB. ✗ 5.28 61.5 53.9 49.3 16119.98 141.25 3930.21 MapNav ( 40 ) RGB. ✗ 4.93 53.0 39.7 37.2 - - - SpikeVLA(ours) RGB. ✗ 5.38 63.4 53.3 47.9 6249.18 49.09 1196.16”
- Authors: ruiqi-song; dujun-nie; siyu-teng; et al.

### EA-BRAIN-2026-0088

- Claim: 与 INT4 量化 VLA 相比,SpikeVLA 在 R2R Val-Unseen 上精度更高(SR 53.3 vs 48.2、SPL 47.9 vs 43.6)、能耗更低(49.09J vs 72.49J)、内存更小(6.1GB vs 8.6GB),但理想化算术计算量 ACEs 更高(1196.16 vs 982.55)——脉冲化在精度-内存-能耗三 维优于 INT4,而在计算量维度不占优。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.27807](https://arxiv.org/abs/2606.27807) SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks
- Locator: 4.2 Main Results
- Evidence: 表 5 给出 FP16/INT4/SpikeVLA 三行完整对比,是少见的脉冲 vs 量化 VLA 直接对照。
- Quote: “Table 5 : Comparison with ANN quantized model. Method R2R Val-Unseen Resource Efficiency NE OS SR SPL Mem(GB) Eng(J) ACEs( ) NaVILA (FP16) 5.28 61.5 53.9 49.3 15.7 141.25 3930.21 NaVILA (INT4) 5.66 56.8 48.2 43.6 8.6 72.49 982.55 SpikeVLA 5.38 63.4 53.3 47.9 6.1 49.09 1196.16”
- Authors: ruiqi-song; dujun-nie; siyu-teng; et al.

### EA-BRAIN-2026-0068

- Claim: AIGOR 把神经元模型、数值格式、数据通路宽度、并行度与神经元在核/工作者间的划分设为实例生成时才解析的配置轴,而非对所有实例一次性固化,以此应对 SNN 硬件生态碎片化。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.03191](https://arxiv.org/abs/2607.03191) AIGOR: A Modular, Event-Driven Neuromorphic Architecture for Configurable SNN Inference
- Locator: 3 AIGOR Architecture
- Evidence: 第 3 节开篇明确结构选择在实例生成时设定,配置轴见其表 1。
- Quote: “The structural choices below, the neuron model, the numeric format, the datapath width, the degree of parallelism, and the partitioning of neurons across cores and workers, are set when an instance is generated rather than fixed once for all instances”
- Authors: pierpaolo-perticaroli; roberto-ammendola; andrea-biagioni; et al.

### EA-BRAIN-2026-0069

- Claim: 功能正确性实测:前馈分类器在 MNIST 测试集复现 snnTorch 参考精度 95%(25 时间步编码窗口);循环网络在 0.1 ms 时间步下复现 NEST 参考放电模式至 3 ms 模拟时间,最多 4 核单 FPGA、8 核跨两 FPGA。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.03191](https://arxiv.org/abs/2607.03191) AIGOR: A Modular, Event-Driven Neuromorphic Architecture for Configurable SNN Inference
- Locator: 6.1 Functional correctness
- Evidence: 6.1 节给出两个负载对软件参考的复现结果与跨 FPGA 核数。
- Quote: “On the feedforward benchmark, the deployed classifier reproduces the classification accuracy of its snnTorch reference ( 95% on the MNIST test set) at the 25-timestep encoding window. On the recurrent benchmark, the FPGA reproduces the firing pattern of the NEST reference over the exercised interval (up to 3 ms of simulated time at a 0.1 ms timestep), on up to 4 cores on a single FPGA and up to 8 cores across two FPGAs.”
- Authors: pierpaolo-perticaroli; roberto-ammendola; andrea-biagioni; et al.

### EA-BRAIN-2026-0071

- Claim: 吞吐实测与瓶颈:单核实例在 10,000 个 MNIST 样本上维持 568 样本/s(片上周期计数器测量);吞吐由每时间步脉冲负载决定,全连接规模下突触存储取回成为主导瓶颈。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.03191](https://arxiv.org/abs/2607.03191) AIGOR: A Modular, Event-Driven Neuromorphic Architecture for Configurable SNN Inference
- Locator: 6.2 Throughput
- Evidence: 6.2 节给出单核吞吐实测与瓶颈归因。
- Quote: “On the classifier, over 10,000 MNIST samples, the single-core instance sustains 568 samples/s, measured with an on-chip cycle counter.”
- Authors: pierpaolo-perticaroli; roberto-ammendola; andrea-biagioni; et al.

### EA-BRAIN-2026-0032

- Claim: 作者提出以可微脉冲时间离散化(DSTD)扩展到任意膜/突触时间常数 LIF 神经元的训练框架,并配合 synfire 链式时间正则构成 Syn-SNN;基准中密集前突触输入下峰值内存降低近两个数量级。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.14672](https://arxiv.org/abs/2607.14672) Scalable Training of Continuous-Time Spiking Neural Networks with Differentiable Spike-Time Discretization
- Locator: 1 Introduction
- Evidence: 引言汇总框架贡献与近两个数量级的内存收益;方法节给出机制。
- Quote: “In our benchmarks, these improvements included nearly two orders of magnitude lower peak memory consumption for dense presynaptic spike inputs.”
- Authors: yusuke-sakemi; tomoya-takeuchi; takeo-hosomi; et al.

### EA-BRAIN-2026-0033

- Claim: 单层 1000 LIF 神经元基准中,输入脉冲数达 6000 时 DSTD 相对精确脉冲时间计算的内存效率提升 60 到 150 倍;原因在于精确法必须为随前突触脉冲数增长的候选区间保留中间变量,而 DSTD 只用固定数目的区间。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.14672](https://arxiv.org/abs/2607.14672) Scalable Training of Continuous-Time Spiking Neural Networks with Differentiable Spike-Time Discretization
- Locator: 3 Experiments
- Evidence: 3 节报告内存/时间比值随输入规模的增长及 60-150 倍区间。
- Quote: “In particular, the improvement in memory efficiency is substantial: even for , which accurately approximates spike times, the memory efficiency improves by a factor of 60 to 150 when the number of inputs reaches 6000.”
- Authors: yusuke-sakemi; tomoya-takeuchi; takeo-hosomi; et al.

### EA-BRAIN-2026-0034

- Claim: 全部实验结果均在单张 NVIDIA GH200 120GB GPU 上获得;在该资源约束下训练出 9 层卷积 SNN(CIFAR-10)与 20 层卷积 SNN(Fashion-MNIST),而此前最深的 TTFS 16 层 CNN 报告需要 GPU 集群。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.14672](https://arxiv.org/abs/2607.14672) Scalable Training of Continuous-Time Spiking Neural Networks with Differentiable Spike-Time Discretization
- Locator: 3 Experiments
- Evidence: 3 节明示单 GPU 设置;附录 D 表 8 注明先前 16 层工作使用 GPU 集群。
- Quote: “All results in this paper were obtained using a single GPU (NVIDIA GH200 120GB).”
- Authors: yusuke-sakemi; tomoya-takeuchi; takeo-hosomi; et al.

### EA-BRAIN-2026-0035

- Claim: 基准对比:Syn-SNN-9 在 CIFAR-10 达 90.36%、Syn-SNN-20 在 Fashion-MNIST 达 92.33%,且两者均支持流水线操作;此前 TTFS 路线的 16 层 CNN 为 92.68%(CIFAR-10)、5 层 CNN 为 79.26%,均不支持流水线。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.14672](https://arxiv.org/abs/2607.14672) Scalable Training of Continuous-Time Spiking Neural Networks with Differentiable Spike-Time Discretization
- Locator: Appendix D Benchmarking
- Evidence: 附录 D 表 8 汇总各连续时间 SNN 的架构、流水线属性与精度。
- Quote: “Syn-SNN-20 (proposed) TTFS (DSTD) 20-layer CNN ( ) YES 92.33 % (F-MNIST) Syn-SNN-9 (proposed) TTFS (DSTD) 9-layer CNN ( , ) YES 90.36 % (CIFAR-10)”
- Authors: yusuke-sakemi; tomoya-takeuchi; takeo-hosomi; et al.

### EA-BRAIN-2026-0036

- Claim: synfire 链式时间正则通过逐层时间窗惩罚抑制死神经元问题并使流水线操作成为可能:下一数据样本可在末层神经元发放前输入,从而避免多层化导致的吞吐下降。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.14672](https://arxiv.org/abs/2607.14672) Scalable Training of Continuous-Time Spiking Neural Networks with Differentiable Spike-Time Discretization
- Locator: 2 Method
- Evidence: 2 Method 阐明时间惩罚与流水线机制;3 节以 20 层网络与 4 样本顺序输入演示。
- Quote: “Because the temporal penalty term encourages all neurons to fire, the dead neuron problem is suppressed. Furthermore, as shown in Fig. 1 (g), pipeline operation becomes possible, in which the next datum can be input before the neurons in the final layer fire.”
- Authors: yusuke-sakemi; tomoya-takeuchi; takeo-hosomi; et al.

### EA-BRAIN-2026-0050

- Claim: 提出 N-MDLM 模型类:由常规 MDLM 经量化与 IF 脉冲模型转换得到的神经形态块扩散语言模型,块并行去噪提高每参数访问的 token 产出、事件驱动稀疏同时削减计算与访存;并配套 token 级 roofline 分析框架,把块尺寸与激活稀疏对解码效率的联合效应统一刻画。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24841](https://arxiv.org/abs/2607.24841) Neuromorphic Diffusion Language Models: Addressing Compute and Memory Bottlenecks via Sparsity and Block Denoising
- Locator: I Introduction
- Evidence: 引言贡献列表三条:模型类、分析框架、实验验证。
- Quote: “The main contributions of this work are as follows: • Neuromorphic MDLM : We introduce N-MDLMs , a novel class of neuromorphic LLMs obtained via conversion of a conventional MDLM [ 3 ] based on quantization and integrate-and-fire (IF) spiking models [ 10 ] . • Analysis: We develop a token-level roofline-inspired analytical framework that characterizes the achievable decoding efficiency of N-MDLMs as a function of block size and activation sparsity, capturing the joint and synergistic effects of”
- Authors: dengyu-wu; clement-ruah; jiechen-chen; et al.

### EA-BRAIN-2026-0051

- Claim: 实验规模与设置:N-MDLM 基于 E2D2 编码器-解码器扩散架构(约 250M 参数),在 WMT 14 de-en 翻译数据上从预训练模型经量化转换管线后再用 Adam 微调一轮,脉冲过程以 bitwise 编码在 GPU 上仿真,实验取每去噪步解除一个 token 的设置。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24841](https://arxiv.org/abs/2607.24841) Neuromorphic Diffusion Language Models: Addressing Compute and Memory Bottlenecks via Sparsity and Block Denoising
- Locator: V-A Setup
- Evidence: V-A Setup 给出架构、参数量、数据集、仿真与微调设置。
- Quote: “For translation experiments on the WMT 14 de-en dataset [ 6 ] we adopt the efficient encoder-decoder diffusion (E2D2) architecture in [ 4 ] with encoder layers and decoder layers, embedding dimension and hidden intermediate dimension (approximately 250M parameters) [ 4 ] . The N-MDLM introduced in Sec. III-A is simulated on GPU using bitwise coding for time steps.”
- Authors: dengyu-wu; clement-ruah; jiechen-chen; et al.

### EA-BRAIN-2026-0052

- Claim: 核心结果(图 5,WMT 14 de-en、ICMS):N-MDLM 在归一化吞吐与每 token 能耗两项上同时优于 AR-LLM 与 MDLM,而 BLEU 仅轻微下降,即效率增益对翻译质量影响极小;能耗收益主要来自内存访问摊销,事件驱动计算进一步把最低能耗推到最高稀疏度处。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24841](https://arxiv.org/abs/2607.24841) Neuromorphic Diffusion Language Models: Addressing Compute and Memory Bottlenecks via Sparsity and Block Denoising
- Locator: V-C Results
- Evidence: V-C Results 图 4/5 段落:吞吐与能耗均按式(15)(16)估算,N-MDLM 双超基线且 BLEU 轻微下降。
- Quote: “The results show that neuromorphic masked diffusion language models (N-MDLMs) outperform AR-LLM and MDLM in terms of both throughput and energy efficiency, with only a slight drop in BLEU, indicating that the efficiency gains are achieved with minimal impact on translation quality.”
- Authors: dengyu-wu; clement-ruah; jiechen-chen; et al.

### EA-BRAIN-2026-0053

- Claim: 区制机制(图 3):在 OCMS(内存受限,GPU 类)上 MDLM 吞吐随块尺寸上升;但在 ICMS(片上内存、计算受限)上普通 MDLM 增大块尺寸不产生任何增益;N-MDLM 引入稀疏后同时降低计算与内存流量、把系统推回内存受限区,从而在普通 MDLM 无法改善的硬件上提取性能增益,吞吐随块尺寸增长并在进入计算受限区后饱和。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24841](https://arxiv.org/abs/2607.24841) Neuromorphic Diffusion Language Models: Addressing Compute and Memory Bottlenecks via Sparsity and Block Denoising
- Locator: V-C Results
- Evidence: V-C Results 图 3 段落完整给出 OCMS/ICMS 上 MDLM 与 N-MDLM 的区制对比与饱和行为。
- Quote: “In contrast, in the compute-bound regime of ICMS, increasing the block size does not yield gains for MDLM (solid line). This is because, in a compute-bound regime, the throughput is limited by the compute rate , and it does not benefit from amortizing memory access via diffusion. By introducing sparsity, N-MDLM reduces both computation and memory traffic.”
- Authors: dengyu-wu; clement-ruah; jiechen-chen; et al.

### EA-BRAIN-2026-0056

- Claim: SpiNNaker2 将处理元(核)数量从 SpiNNaker 的 18 个增加到 152 个,每个核配备专用加速器(矩阵乘、卷积、指数/对数),构成软件可编程的数字神经形态 many-core 平台。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24396](https://arxiv.org/abs/2607.24396) The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing
- Locator: 1 Introduction
- Evidence: 引言明确 18→152 的核数跃升与每核加速器配置。
- Quote: “Compared to the SpiNNaker chip, the number of processing elements (cores) is significantly increased from 18 to 152. Each core now includes dedicated accelerators for often-used functions, such as matrix multiplications, convolutions, as well as exponentials and logarithms.”
- Authors: stefan-scholze; johannes-partzsch; sebastian-hppner; et al.

### EA-BRAIN-2026-0057

- Claim: INT8 DNN 负载芯片实测:高能效档(150 MHz/0.5 V)2.281 TOPS@0.825 W 即 2.77 TOPS/W,高性能档(300 MHz/0.8 V)4.563 TOPS@2.219 W 即 2.06 TOPS/W;与 NorthPole(2.70)、Groq(2.73)、Jetson Orin Nano(2.68)等平台同表对比处于同一量级。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24396](https://arxiv.org/abs/2607.24396) The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing
- Locator: 4.3 Machine Learning Accelerator (MLA)
- Evidence: 表 3 完整给出自测(*)与他平台 INT8 推理的吞吐/功率/能效同表对比。
- Quote: “Table 3 : Comparison of SpiNNaker2 against different other INT8 inference platforms for DNN Platform Throughput [TOPS] Power [W] Efficiency [TOPS / W] SpiNNaker2 (150 MHz, 0.5 V) 2.281 * 0.825 * 2.77 SpiNNaker2 (300 MHz, 0.8 V) 4.563 * 2.219 * 2.06 Greenwaves GAP9 [ 47 ] 0.151 0.64 0.34 Coral EdgeTPU [ 47 ] 4 2 2.00 Intel Mobileye Eye Q5 [ 47 ] 12 5 2.40 Jetson Orin Nano [ 40 ] 67 25 2.68 IBM NorthPole [ 7 , 37 ] 200 74 2.70 Groq Tensor Streaming [ 47 ] 820 300 2.73 ARM Ethos N77 [ 47 ] 4.1 0.8”
- Authors: stefan-scholze; johannes-partzsch; sebastian-hppner; et al.

### EA-BRAIN-2026-0059

- Claim: DVS 手势深 SNN 实时仿真中,DVFS 自动性能档(Auto PL,1 ms tick)能耗 0.741 J,低于固定高性能档的 1.023 J 与低性能档的 2.010 J,三档准确率均为 92.04%,证明逐核自适应功耗管理可在不掉精度的情况下省能。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24396](https://arxiv.org/abs/2607.24396) The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing
- Locator: 4 Results
- Evidence: 表 4 给出三档性能管理的能耗与准确率完整对比。
- Quote: “Table 4 : SNN DVS gesture prediction on SpiNNaker2. Mode Low PL High PL Auto PL Simulation tick [s] 0.003 0.001 0.001 Energy [J] 2.010 1.023 0.741 Accuracy (%) 92.04 92.04 92.04”
- Authors: stefan-scholze; johannes-partzsch; sebastian-hppner; et al.

### EA-BRAIN-2026-0060

- Claim: 事件化 GRU(EGRU)语言模型单批量推理在 SpiNNaker2 上能耗 65 mJ,而 Nvidia A100 GPU 实现为 1.19 J,能量降低 18 倍,但执行时间延长 8 倍;同节还报告 EventProp 片上训练每步能耗仅为 RTX 4070 的 31%。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.24396](https://arxiv.org/abs/2607.24396) The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing
- Locator: 4.6 Event-Based Algorithms
- Evidence: 4.6 节给出 EGRU 65 mJ vs 1.19 J 与 8× 时延代价,以及 EventProp 31% 训练能耗两个实测引用。
- Quote: “Energy per inference for a language model reduced by a factor of 18 compared to a GPU implementation (65 mJ on SpiNNaker2 vs. 1.19 J on Nvidia A100), with the drawback of an 8x longer execution time.”
- Authors: stefan-scholze; johannes-partzsch; sebastian-hppner; et al.

### EA-BRAIN-2026-0098

- Claim: Sequence-SOD 的主要贡献是把'序列感知训练与评估'引入 SNN 目标检测:显式把膜电位当作模型的时序记忆,在序列内保持 SNN 内部状态、仅在独立序列间重置,并用包含多个时间点标签的完整事件序列训练,而非孤立单标签区间。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.26703](https://arxiv.org/abs/2607.26703) Sequence-SOD: Bio-inspired Sequence-aware Spiking Object Detection for Event Cameras
- Locator: page 2
- Evidence: 第 2 页贡献段原句定义序列感知策略与膜电位记忆定位;第 5 页给出损失在标签区间的分配机制。
- Quote: “The main contribution of this paper is a sequence-aware training and evaluation strategy for SNN-based object detec- tion that explicitly treats membrane potentials as the model’s temporal memory for continuous perception.”
- Authors: katharina-bendig; ren-schuster; didier-stricker

### EA-BRAIN-2026-0099

- Claim: 在完全相同的 SSD+Spiking DenseNet 架构上,序列感知训练(序列长 5)在所有测试长度上稳定优于单区间训练:test 1 为 25.26 vs 23.38、test full 为 25.30 vs 23.04(mAP);行人 AP 提升最大(14.72 vs 单区间 full 的 10.92),且单区间训练网络在 full 序列上反而退化,证明增益来自膜电位状态记忆而非数据量。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.26703](https://arxiv.org/abs/2607.26703) Sequence-SOD: Bio-inspired Sequence-aware Spiking Object Detection for Event Cameras
- Locator: page 7
- Evidence: 表 1 给出 strain{1,5}×stest{1,5,full} 全交叉的 mAP/AP50/AP75/APcar/APped。
- Quote: “1 1 125 23.38 47.23 20.97 35.39 11.36 1 5 125 23.63 47.74 21.02 35.42 11.83 1 full 125 23.04 45.89 20.68 35.17 10.92 5 1 125 25.26 50.98 21.88 36.09 14.43 5 5 125 25.31 50.99 21.89 36.05 14.57 5 full 125 25.30 51.49 21.91 35.87 14.72”
- Authors: katharina-bendig; ren-schuster; didier-stricker

### EA-BRAIN-2026-0101

- Claim: 理论能耗折算显示 SNN 相对等价 ANN 拓扑有大幅优势:整体推理能耗 ANN 12.17 mJ vs SNN 0.10 mJ(116×),其中骨干 199×(平均发放率 0.0235)、检测头 31×(0.0960);口径为 45nm CMOS 32-bit 浮点(EMult 3.7pJ、EAc 0.9pJ)乘以实测发放率。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.26703](https://arxiv.org/abs/2607.26703) Sequence-SOD: Bio-inspired Sequence-aware Spiking Object Detection for Event Cameras
- Locator: page 11
- Evidence: 表 4 给出 ANN/SNN 的 FLOPs、发放率、能耗(mJ)与倍率;第 9 页给出折算公式与工艺常数。
- Quote: “Table 4 Energy consumption of an ANN and a SNN Method Network F LOP sM ult F LOP sAc Rl E (mJ) EAN N EM ethod ANN Backbone 2295.49 M 2298.21 M − 10.56 1× Heads 351.32 M 351.32 M − 1.61 1× Overall 2646.81 M 2649.53 M − 12.17 1× SNN Backbone − 2298.21 M 0.0235 0.05 199× Heads − 351.32 M 0.0960 0.05 31× Overall − 2649.53 M 0.0296 0.10 116×”
- Authors: katharina-bendig; ren-schuster; didier-stricker

### EA-BRAIN-2026-0074

- Claim: 在三个皮层类器官的纵向 HD-MEA 记录上,校正采样率与刺激时间后发现:诱发反应是快速、近同步的全网络爆发而非向外传播波,峰潜伏期-距离无可测斜率,因此传播/整合深度类图指标(含消息传递定理检验)不适用于此类数据。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.28068](https://arxiv.org/abs/2607.28068) Stimulus-Evoked Network Dynamics in Human Cortical Organoids: From a Graph-Computational Framework to Repeated-Stimulation Depression
- Locator: 3.1 The evoked response is a near-synchronous network burst, not a propagating wave
- Evidence: 3.1 节直接检验定理 1 前提,结论为近同步爆发,原指标套件大多不适用(3.8)。
- Quote: “The evoked response was a near-synchronous, network-wide burst, not an outward-propagating wave. Hence (Eq. ( 13 )) did not index a real spreading process, and (Eq. ( 11 )), (Eq. ( 12 )), and the test were not applicable to these recordings.”
- Authors: esmaeil-s-nadimi; vinay-c-gogineni; jan-matthias-braun; et al.

### EA-BRAIN-2026-0075

- Claim: 重复日刺激使响应网络空间收缩:两个重复刺激类器官的响应电极阵列占比分别从 D1-D4 的 94%/99%/99%/99% 与 42%/72%/14%/100% 崩塌到 D7 的 9.5%(384 电极)与 12%(486 电极),而同龄首次刺激对照响应 3788 电极、占阵列 93%。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.28068](https://arxiv.org/abs/2607.28068) Stimulus-Evoked Network Dynamics in Human Cortical Organoids: From a Graph-Computational Framework to Repeated-Stimulation Depression
- Locator: 3.5 The responding network spatially contracts with repeated stimulation
- Evidence: 表 3 给出三类器官逐日响应电极数与阵列占比;对照 93% 与重复刺激 9.5%/12% 形成最清晰的对照分离。
- Quote: “Table 3: Responsive-electrode count and array fraction across days. Organoid D1 D2 D3 D4 D7 552 responsive 3852 4020 4037 4005 384 (% array) 94% 99% 99% 99% 9.5% 613 responsive 1711 2932 574 4048 486 (% array) 42% 72% 14% 100% 12% 612 control responsive — — — — 3788 (% array) — — — — 93%”
- Authors: esmaeil-s-nadimi; vinay-c-gogineni; jan-matthias-braun; et al.

### EA-BRAIN-2026-0076

- Claim: 会话级诱发响应/基线比显示重复刺激类器官在 D7 强度大幅下降(552: D1 1123→D7 206;613: D1 487→D7 268),而同龄刺激naïve对照产生数据集中最强反应(1914),证明 D7 抑郁由重复刺激历史而非发育成熟驱动。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.28068](https://arxiv.org/abs/2607.28068) Stimulus-Evoked Network Dynamics in Human Cortical Organoids: From a Graph-Computational Framework to Repeated-Stimulation Depression
- Locator: 3.2 Repeated stimulation depresses the evoked response across days
- Evidence: 表 2 给出三类器官逐日响应/基线比;对照 D7 的 1914 为全集最强,直接反证成熟解释。
- Quote: “Table 2: Session-level evoked response strength (response/baseline ratio). Organoid D1 D2 D3 D4 D7 552 (repeated) 1123 1411 1802 1450 206 613 (repeated) 487 897 230 1128 268 612 (single-stim control) — — — — 1914 The single-stimulation control isolates stimulation history from age.”
- Authors: esmaeil-s-nadimi; vinay-c-gogineni; jan-matthias-braun; et al.

### EA-BRAIN-2026-0116

- Claim: 该文主张:Bayesian reflex 由三项近期贝叶斯计算突破构成——椭球分解(任意后验的近精确 i.i.d. 采样)、带理论收敛保证的递归高斯过程(深层分层推断)、导数感知贝叶斯优化(生成模型参数与行动的高效学习)——三者组合使预测编码首次获得可扩展且精确的算法引擎。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.00492](https://arxiv.org/abs/2608.00492) The Bayesian Reflex: A Predictive Coding Engine for Artificial Intelligence
- Locator: 1 Introduction: From Predictive Coding to Artificial Intelligence
- Evidence: 引言明确列出三项创新并声称它们使 Bayesian reflex 与预测编码兼容;结论重申三支柱是预测编码核心机制的直接计算实例化。
- Quote: “Crucially, three innovations make the Bayesian reflex truly predictive‑coding‑compatible: the ellipsoidal decomposition framework for near‑exact i.i.d. sampling from arbitrary posteriors ( 5 ) , recursive Gaussian processes for deep hierarchical inference with theoretical convergence guarantees ( 2 ) , and – as we show in this paper – the integration of derivative‑aware Bayesian optimisation ( 15 ) that allows efficient learning of the generative model’s parameters and actions.”
- Authors: sourabh-bhattacharya

### EA-BRAIN-2026-0118

- Claim: 被引理论保证:递归高斯过程(RGP)后验在温和正则条件下具有一致性、近最优收敛速率与模型误设稳健性,并具备通用逼近性质——增加层数可使最小可达 KL 散度任意小,因为深层 GP 组合可逼近紧集上的任意连续函数。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2608.00492](https://arxiv.org/abs/2608.00492) The Bayesian Reflex: A Predictive Coding Engine for Artificial Intelligence
- Locator: 5.6 Theoretical Guarantees (from 2 )
- Evidence: 5.6 节转述被引工作(编号 2)的四项保证:一致性、近最优速率、误设收敛到最优近似、通用逼近。
- Quote: “Fourth, the RGP possesses a universal approximation property. By increasing the number of layers , the minimal achievable KL divergence can be made arbitrarily small, because deep compositions of GPs can approximate any continuous function on a compact set.”
- Authors: sourabh-bhattacharya

### EA-BRAIN-2026-0119

- Claim: 旗舰定量应用(转引自先前工作):把素数序列建模为非齐次 Poisson 过程并做序贯贝叶斯更新,用后验预测分布采样高不确定区域(主动推理式的探索-利用平衡),发现 259 个超过 1.4 亿的新素数,其中包括 184 个强 Mersenne 素数候选。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2608.00492](https://arxiv.org/abs/2608.00492) The Bayesian Reflex: A Predictive Coding Engine for Artificial Intelligence
- Locator: 7.2 Prime Number Discovery as Active Inference
- Evidence: 7.2 节转述被引工作(编号 3)的素数递归贝叶斯分析:后验预测采样导致 259 个新素数与 184 个强 Mersenne 候选的发现。
- Quote: “This led to the discovery of 259 new primes exceeding 140 million, including 184 strong Mersenne prime candidates.”
- Authors: sourabh-bhattacharya

### EA-BRAIN-2026-0063

- Claim: 转引实测锚点:IBM 34-tile PCM 模拟存内芯片报告最高 12.4 TOPS/W,但该值为芯片持续结果——含 tile 间通信与模拟外设电路,排除完整产品所需的辅助数字计算与 SRAM;64 核芯片单相低精度 63.1 TOPS/9.76 TOPS/W、四相高精度 16.1 TOPS/2.48 TOPS/W。因各来源测量边界不同,这些数值不可用于跨技术排名。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2608.03514](https://arxiv.org/abs/2608.03514) Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing
- Locator: 7.1 System-Level Benchmarking
- Evidence: 表 1 汇总转引 AIMC/光子加速器报告值与各自声明的测量边界,并明确不可排名。
- Quote: “AIMC (PCM, 34-tile chip, 14 nm) Energy efficiency Up to 12.4 TOPS/W Chip-sustained result including inter-tile communication and analogue peripheral circuitry, but excluding the auxiliary digital compute and SRAM required by a complete product [ 2 ] AIMC (PCM, 64-core chip, 14 nm) Throughput and energy efficiency 63.1 TOPS, 9.76 TOPS/W (one-phase, low precision); 16.1 TOPS, 2.48 TOPS/W (four-phase, high precision); 8-bit I/O”
- Authors: eiman-kanjo; varuna-de-silva

### EA-BRAIN-2026-0065

- Claim: 能耗核算主张:每突触操作能耗只对表征核心有意义,与常规数字系统比较必须使用每完成任务能耗;任务级分解需计入基线功率×执行时间、突触事件数、路由脉冲包数、神经元状态更新及存储/传感/主机开销,脉冲计数本身不决定系统能耗。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.03514](https://arxiv.org/abs/2608.03514) Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing
- Locator: 3.2 Activity-Dependent Energy
- Evidence: 3.2 节给出任务级能量分解框架并以 syn-op vs 任务能耗对照句收尾。
- Quote: “Energy per synaptic operation is informative for characterising a core, but energy per completed task is required for comparison with conventional digital systems”
- Authors: eiman-kanjo; varuna-de-silva

### EA-BRAIN-2026-0066

- Claim: 方向判断:模拟、光子与神经形态技术将作为数字治理系统内的专用引擎被采用,数字主机负责工作负载分配、内存、校准、验证与物理结果不可靠时的回退;采用将是增量式且负载特定的,近期机会集中在重复矩阵运算、稀疏时序处理与常开感知。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.03514](https://arxiv.org/abs/2608.03514) Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing
- Locator: 8 Bringing It Together: Pathways to Adoption
- Evidence: 第 8 节给出采用路径的总结性判断。
- Quote: “Analogue, photonic and neuromorphic technologies are therefore likely to be adopted as specialised engines within digitally governed systems. Digital hosts will typically manage workload allocation, memory, calibration, verification and fallback when a physical result is uncertain or unreliable.”
- Authors: eiman-kanjo; varuna-de-silva

### EA-BRAIN-2026-0085

- Claim: 框架成立以苛刻培养前提为条件:类器官需至少 60-90 天体外成熟以获得学习所需的细胞多样性与同步爆发等功能网络活动,且作者建议用 guided(如背侧前脑)或 semi-guided 协议替代 unguided 自组织协议,以在复杂性与批次间一致性之间取得平衡。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.04633](https://arxiv.org/abs/2509.04633) The Physical Basis of Prediction: World Model Formation in Neural Organoids via an LLM-Generated Curriculum
- Locator: 3.2 Biological substrates and embodiment
- Evidence: 3.2 节给出成熟周期、动态培养(轨道摇床/旋转生物反应器防缺氧坏死)与协议选择的工程约束。
- Quote: “Neural organoids require a protracted in vitro culture period, typically a minimum of 60-90 days, to develop the cellular diversity (including neurons, astrocytes, and other glia ( Porciúncula et al. 2021 ) ) and functional network activity, such as synchronized bursting, required for learning ( Fair et al. 2020 ; Giandomenico et al. 2021 ) .”
- Authors: brennen-hill

### EA-BRAIN-2026-0006

- Claim: 脉冲激活编码+INT8 权重联合部署后,在常识推理/MMLU/CMMLU 上平均性能下降约 2%(表 3 实测 1-3% 量级,如 7B 平均 0.6998→0.6875),精度近保持。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2509.05276](https://arxiv.org/abs/2509.05276) SpikingBrain: Spiking Brain-inspired Large Models
- Locator: 5.5 Analysis of Spiking Scheme
- Evidence: 5.5 节正文与表 3 给出脉冲方案前后完整数字。
- Quote: “evaluations on commonsense reasoning, MMLU, and CMMLU benchmarks indicate that the average performance drop under this scheme is limited to approximately 2% for both SpikingBrain-7B and SpikingBrain-76B, confirming its effectiveness in preserving accuracy.”
- Authors: yuqi-pan; yupeng-feng; jinghao-zhuang; et al.

### EA-BRAIN-2026-0016

- Claim: ImageNet(ResNet-34)上该离散化 4 时间步无 TET 达 70.52%(单次试验),超过 TEBN 68.28% 等先前方法,但被使用三元脉冲的 Ternary Spike(70.74%)以小差距超越;作者将此定位为'提高神经元动力学复杂度'这条生物合理替代路线的竞争力证据。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.05168](https://arxiv.org/abs/2510.05168) Discretized Quadratic Integrate-and-Fire Neuron Model for Deep Spiking Neural Networks
- Locator: 5.1 Comparison to Recent Works
- Evidence: 表 1 ImageNet 列与正文承认 Guo et al. 2024b 更优,并给出路线定位陈述。
- Quote: “The work of Guo et al. 2024b outperforms ours by a margin of , due to their use of ternary spikes to mitigate information loss and enhance accuracy. In contrast, our results demonstrate that increasing the complexity of neuron dynamics offers a competitive and biologically plausible alternative for improving performance.”
- Authors: eric-jahns; davi-moreno; milan-stojkov; et al.

### EA-BRAIN-2026-0019

- Claim: 训练稳定性来自从离散化参数集解析推导代理梯度窗口:在 tdBN 归一化假设下,定理 4.1 给出膜电位分布的均值与方差,据此计算窗口宽度以降低误选窗口与梯度失配风险——该方法的有效性以 tdBN 归一化假设为前提。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.05168](https://arxiv.org/abs/2510.05168) Discretized Quadratic Integrate-and-Fire Neuron Model for Deep Spiking Neural Networks
- Locator: 4.3 Surrogate Gradient Formulation
- Evidence: 4.3 节提出解析窗口计算并陈述动机;定理证明在附录 D。
- Quote: “To remedy this issue, we propose an analytical means to calculate the surrogate gradient window based on the parameter set of our QIF discretization.”
- Authors: eric-jahns; davi-moreno; milan-stojkov; et al.

### EA-BRAIN-2026-0107

- Claim: 条件性证据:基于 burst 三元编码(静默/单脉冲/burst)的 Burstprop,在 MNIST 图像分类上用数百神经元的网络取得与 BPTT 可比的低测试误差;该结论成立条件是小规模网络与 MNIST 级任务,尚不能外推到大规模或语言模型场景。
- Stance: `conditional` | Confidence: `citation-supported`
- Paper: [2511.04455](https://arxiv.org/abs/2511.04455) The brain as a blueprint: a survey of brain-inspired approaches to learning in artificial intelligence
- Locator: 2.3.5 Silence, single, and bursting activity: ternary code of biological neural networks
- Evidence: 2.3.5 节转述 Burstprop 在 MNIST 上与 BPTT 可比,网络规模为数百神经元,并被定位为可运行于神经形态硬件的学习方法。
- Quote: “Experimental results have shown that Burstprop can achieve low test classification errors on MNIST, with performance levels that are comparable to those obtained using backpropagation through time on the same network architectures.”
- Authors: guillaume-etter

### EA-BRAIN-2026-0022

- Claim: 问答任务(QAT)上,NASN 版 WD-SpikingFormer-0.4B 平均 29.4%(比同架构 NILIF 高 1.0),能耗折算 245.1 mJ 仅为 Qwen-1.5B(3398.3 mJ,平均 33.2%)的约 7%,呈现明显能耗-精度权衡而非精度追平。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.12365](https://arxiv.org/abs/2604.12365) Adaptive Spiking Neurons for Vision and Language Modeling
- Locator: 4.4. Question Answering Tasks
- Evidence: 4.4 节正文给出精度与能耗两组数字及权衡表述。
- Quote: “Compared to Qwen-1.5B, which utilizes the same pretraining setup as WE-Spikingformer, our model reduces energy consumption by an order of magnitude, requiring only 245.1 mJ compared to 3398.3 mJ (representing only 7% of the energy).”
- Authors: chenlin-zhou; sihang-guo; jiaqi-wang; et al.

### EA-BRAIN-2026-0111

- Claim: 局部性-性能权衡(条件性主张):局部学习规则减少全局通信与内存压力,契合低功耗神经形态硬件与在线适应;但在挑战性基准上,放宽局部性通常能提升训练性能——即局部规则的优势以基准精度为代价、以部署场景为条件。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.15058](https://arxiv.org/abs/2605.15058) NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework
- Locator: 1 Introduction
- Evidence: 引言以一句话给出局部性权衡的领域共识;2.5 节进一步从神经形态硬件架构约束论证局部规则的必然性。
- Quote: “Locality reduces global communication and memory pressure and aligns well with low-power neuromorphic hardware and online adaptation, yet relaxing locality often improves training performance on challenging benchmarks.”
- Authors: alessio-caviglia; filippo-marostica; roberta-bardini; et al.

### EA-BRAIN-2026-0030

- Claim: 扩展到 LLaMA3-70B(W8A8)时,NLS 转换在 T=1 平均 78.64 对直接 SNN 转换 78.85、T=2 为 78.82 对 78.97,差距随时间步增加而缩小;在 LLaMA2-7B/LLaMA3-8B 的 W6A6/W8A8 与 T=1/2/4 设置下同样保持可比精度,支持方法可扩展到 70B 规模。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.20289](https://arxiv.org/abs/2605.20289) Plug-and-Play Spiking Operators: Breaking the Nonlinearity Bottleneck in Spiking Transformers
- Locator: B.3 Model-Level Evaluation.
- Evidence: 附录 B.3 表 4 给出三个规模、两种量化、多个时间步的 SNN 与 NLS 对照。
- Quote: “Llama 3 70B PrefixQ - W8A8 79.32 85.65 62.37 82.79 84.11 78.85 DuQ - W8A8 80.82 84.83 63.48 85.73 84.39 79.85 SNN 1 W8A8 79.32 85.65 62.37 82.79 84.11 78.85 NLS 1 W8A8 78.85 85.71 62.54 82.20 83.90 78.64 SNN 2 W8A8 79.48 85.70 62.88 82.87 83.90 78.97 NLS 2 W8A8 79.08 85.60 62.88 82.62 83.90 78.82”
- Authors: xinzhe-yuan; xiang-peng; bin-gu; et al.

### EA-BRAIN-2026-0073

- Claim: 条件性口径:多节点同步方案仅在仿真中验证至 1000 核(3D torus),硬件实测上限为 2 FPGA;能耗数字(每突触操作/每推理)被作者明确限定为 AIGOR 配置间的相对比较,用于设计空间内按效率排序,而非对 ASIC 神经形态处理器的绝对主张。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.03191](https://arxiv.org/abs/2607.03191) AIGOR: A Modular, Event-Driven Neuromorphic Architecture for Configurable SNN Inference
- Locator: 7.5 Design-space characterization
- Evidence: 结论与 7.5 节分别声明千核仅为仿真验证、能耗仅作相对比较。
- Quote: “Reported in neuromorphic conventions, energy per synaptic operation ( /SOP) and energy per inference ( /inference), these figures are read as relative comparisons across AIGOR configurations, letting the design space be ranked by efficiency rather than compared as absolute claims against ASIC neuromorphic processors.”
- Authors: pierpaolo-perticaroli; roberto-ammendola; andrea-biagioni; et al.

### EA-BRAIN-2026-0054

- Claim: 区制依赖的边界条件(式 14 分析):当系统计算受限时,N-MDLM 的延迟增益与稀疏度线性成比例、与块尺寸无关;当系统内存受限时,增大块尺寸会稀释稀疏收益(有效数据加载稀疏度被块尺寸摊薄);增大块尺寸把系统推向计算受限、增大稀疏度推向内存受限,故最大稀疏收益需要高内存带宽系统(如近存计算神经形态器件)配合较大块尺寸。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.24841](https://arxiv.org/abs/2607.24841) Neuromorphic Diffusion Language Models: Addressing Compute and Memory Bottlenecks via Sparsity and Block Denoising
- Locator: IV-B Token Throughput
- Evidence: IV-B 节给出块尺寸×稀疏度的区制权衡与部署准则。
- Quote: “The expression ( 14 ) highlights a regime-dependent tradeoff between the block size and the sparsity level : when the system is compute-bound, the latency gains in N-MDLMs are linearly proportional to the sparsity level regardless of the block size . In contrast, when the system is in a memory-bound regime, increasing the block size reduces the benefits of sparsity, with the effective data-loading sparsity reduced to .”
- Authors: dengyu-wu; clement-ruah; jiechen-chen; et al.

### EA-BRAIN-2026-0058

- Claim: 边界:作者自述 SpiNNaker2 的 DNN 推理能效'与业界现有水平相当'仅当算子完全驻留片上 SRAM 时成立;层过大时有限 DRAM 带宽会降低加速器利用率,单芯片常规 DNN 负载可扩展性受限。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.24396](https://arxiv.org/abs/2607.24396) The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing
- Locator: 4.3 Machine Learning Accelerator (MLA)
- Evidence: 4.3 节与结论分别给出 SRAM 驻留条件与 DRAM 带宽限制两处作者自述。
- Quote: “Although designed mainly for neuromorphic applications, SpiNNaker2’s energy efficiency for deep neural network inference is comparable to the state of practice achieved by other platforms (see Tab. 3 ), when operators are allocated entirely in the on-chip SRAM.”
- Authors: stefan-scholze; johannes-partzsch; sebastian-hppner; et al.

### EA-BRAIN-2026-0103

- Claim: 边界:SNN 的能效优势是条件性的——能耗依赖具体数据集与相应发放率(ANN 恒定执行相同操作数),且该级能效只有在神经形态硬件上部署才能实现;论文全部训练/评估在 GPU 上以时间步仿真完成,40Hz 预测频率亦为依赖输入数据的理论值。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.26703](https://arxiv.org/abs/2607.26703) Sequence-SOD: Bio-inspired Sequence-aware Spiking Object Detection for Event Cameras
- Locator: page 10
- Evidence: 第 10 页能耗讨论原句给出两个条件;第 6 页自述理论频率依赖输入数据。
- Quote: “important to note however, that the energy consumption of SNNs depends on the specific dataset and the resulting spike rates in contrast to ANNs, which always execute the same number of operations. Moreover, SNNs can only achieve this level of energy efficiency, when deployed on neuromor- phic hardware.”
- Authors: katharina-bendig; ren-schuster; didier-stricker

### EA-BRAIN-2026-0077

- Claim: 跨天抑郁反映会话内耐力退化而非响应容量丧失:首试响应量级相对保留而会话均值塌缩;且刺激naïve对照在首次会话即出现强量级抑郁但无显著去同步,而重复刺激器官出现去同步——作者自己将其标为小样本下的 hypothesis,快速会话内抑郁是内在的、跨天成分才随刺激史累积。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.28068](https://arxiv.org/abs/2607.28068) Stimulus-Evoked Network Dynamics in Human Cortical Organoids: From a Graph-Computational Framework to Repeated-Stimulation Depression
- Locator: 3.3 Across-day depression reflects loss of within-session endurance, not capacity
- Evidence: 3.3 给出容量-耐力分离;3.4 给出量级抑郁与去同步的解离及对照证据,作者明示 hypothesis、given small n。
- Quote: “The network’s capacity to mount a strong initial daily response was largely preserved; however, the ability to sustain responses across the session was degraded.”
- Authors: esmaeil-s-nadimi; vinay-c-gogineni; jan-matthias-braun; et al.

### EA-BRAIN-2026-0064

- Claim: 条件性边界:神经形态架构是具有持续时序结构与稀疏变化负载(事件视觉、常开音频、雷达、触觉、生物信号、流式异常检测、闭环控制)的最强候选;但当密集静态输入需先转换为长脉冲序列、维持精度需要高发放率、或不支持算子频繁把执行交回主机时,收益不确定。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.03514](https://arxiv.org/abs/2608.03514) Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing
- Locator: 3.5 Workload Suitability and Evaluation
- Evidence: 3.5 节先列最强候选负载,再给出三类收益不确定情形。
- Quote: “Neuromorphic architectures are strongest candidates for workloads with persistent temporal structure and sparse changes, including event-based vision, always-on audio, radar, tactile sensing, biosignal analysis, streaming anomaly detection and closed-loop control.”
- Authors: eiman-kanjo; varuna-de-silva

### EA-BRAIN-2026-0007

- Claim: 作者自述边界:拼接短文本构造的长上下文训练数据对极限上下文性能提升有限,原生长文本数据是缩小与基座差距的关键;该负面结果限定了转换式路线的长上下文能力来源。
- Stance: `limit` | Confidence: `direct`
- Paper: [2509.05276](https://arxiv.org/abs/2509.05276) SpikingBrain: Spiking Brain-inspired Large Models
- Locator: 6 Discussion of Negative Results and Practical Challenges
- Evidence: 第 6 节负面结果讨论首条。
- Quote: “Training on concatenated short texts, as described in Section 3.4 , rather than native long-context data, resulted in limited improvements in long-context performance. This suggests that downstream performance at extreme context lengths depends strongly on both the quantity and quality of long-context training data.”
- Authors: yuqi-pan; yupeng-feng; jinghao-zhuang; et al.

### EA-BRAIN-2026-0018

- Claim: 路线边界:该 QIF 离散化依赖 tdBN 计算代理梯度,阻碍事件驱动反向传播;每次更新比 LIF 多一次乘法与一次加法,对神经形态芯片实际计算性能的影响不确定;额外超参数可能加大其他场景的训练难度。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.05168](https://arxiv.org/abs/2510.05168) Discretized Quadratic Integrate-and-Fire Neuron Model for Deep Spiking Neural Networks
- Locator: 6 Limitations
- Evidence: 限制一节明确列出三点,均由作者自述。
- Quote: “One limitation of our QIF discretization is its reliance on tdBN ( 6 ) for surrogate gradient calculation, which hinders event-driven backpropagation [ 34 ] since each tdBN layer performs normalization across both spatial and temporal dimensions.”
- Authors: eric-jahns; davi-moreno; milan-stojkov; et al.

### EA-BRAIN-2026-0108

- Claim: 边界:作者判断 von Neumann 架构终将无法胜任生物合理 AI 系统的实现,尤其是依赖 spike-based 学习规则的系统;且该类算法的进展最终受限于神经科学知识前沿,神经生理实验对 AI 从业者仍有重大价值。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.04455](https://arxiv.org/abs/2511.04455) The brain as a blueprint: a survey of brain-inspired approaches to learning in artificial intelligence
- Locator: Conclusions
- Evidence: 结论节把硬件约束与知识前沿约束并列为类脑算法推进的两道限制,同时肯定神经形态硬件的替代潜力。
- Quote: “Critically, von Neumann hardware will eventually be limited in its ability to implement biologically plausible artificial systems, in particular those that rely on spike-based learning rules.”
- Authors: guillaume-etter

### EA-BRAIN-2026-0042

- Claim: 路线边界(作者自述):模型仅 0.9B 参数、512-token 上下文;无 C-Eval/CMMLU 等定量基准与任何 Transformer 基线;仅中文;存在重复伪影且无推理能力;可解释性为相关性分析;神经形态平台(如 Intel Loihi)上的能效'严格定量评估仍是未来工作'。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.16148](https://arxiv.org/abs/2603.16148) NeuronSpark: A Spiking Neural Network Language Model with Selective State Space Dynamics
- Locator: Limitations
- Evidence: Limitations 节以编号列表自述五项局限,并单独声明能效未定量评估。
- Quote: “(1) 0.9B parameters, 512-token context. (2) No quantitative benchmarks (C-Eval, CMMLU) or Transformer baselines. (3) Chinese only. (4) Repetition artifacts and no reasoning capability. (5) Interpretability analyses are correlational, not causal. Energy efficiency. The spike-based hidden computation may be amenable to deployment on neuromorphic platforms (e.g., Intel Loihi ( 9 ) ), which could yield substantial energy savings. A rigorous quantitative evaluation remains future work.”
- Authors: zhengzheng-tang

### EA-BRAIN-2026-0043

- Claim: "纯 SNN"的通信边界:NeuronSpark 默认以浮点泄漏电流信号(而非二值脉冲)作为层间信号以规避二值尖峰对梯度流与表达的限制,泄漏重加权只应用于每层 2 个输入神经元、SNNFFN 中每层 2 个门/升维神经元与 1 个输出神经元;二值脉冲仅是内部事件过程,故其神经形态通信层外推需打折。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.16148](https://arxiv.org/abs/2603.16148) NeuronSpark: A Spiking Neural Network Language Model with Selective State Space Dynamics
- Locator: 3.3 Membrane Potential Leakage Activation
- Evidence: 3.3 节明确下游层消费浮点泄漏电流信号而非二值脉冲,并给出重加权适用的神经元清单。
- Quote: “In other words, unless explicitly stated otherwise, downstream layers consume floating-point leakage-current signals (bioelectric-state proxies) rather than binary spikes: (9) This quantity is the amount of membrane potential that will dissipate due to exponential decay before the next input arrives.”
- Authors: zhengzheng-tang

### EA-BRAIN-2026-0012

- Claim: 边界:SDLLM 属推理期即插即用转换而非训练出的 SNN;作者自述异步发放模式下维度过大会抬高芯片功耗与通信带宽需求;能耗数字为按突触操作折算而非芯片实测。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.16475](https://arxiv.org/abs/2604.16475) Spike-driven Large Language Model
- Locator: 6 Discussion
- Evidence: 讨论节给出异步模式带宽/功耗权衡;相关工作中明确无需训练 SNN;附录 A.2 为功率折算模型。
- Quote: “However, when the dimension becomes too large, it may increase power consumption and communication bandwidth requirements on the chip, a problem that can be optimized by adjusting the concurrency of”
- Authors: han-xu; xuerui-qiu; baiyu-chen; et al.

### EA-BRAIN-2026-0096

- Claim: 边界:常规整数-脉冲展开在极低时间步下所有模型严重退化(MiniCPM-V-2.6-8B OCRBench 掉到 35),近无损结论依赖 QuaRot+MSTS+TC-LIF 组合而非任意脉冲化方法。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.18610](https://arxiv.org/abs/2604.18610) SpikeMLLM: Spike-based Multimodal Large Language Models via Modality-Specific Temporal Scales and Temporal Compression
- Locator: 4.1. Main Results
- Evidence: 4.1 节报告低时间步配置下 SpikeMLLM(QuaRot) 各模型显著退化。
- Quote: “SpikeMLLM(QuaRot) achieves competitive performance at ; however, at the low timestep configuration , all models suffer significant performance degradation — for instance, the OCRBench score of MiniCPM-V-2.6-8B drops to 35 — indicating that aggressively reducing timesteps under conventional integer-to-spike unfolding significantly degrades representation capacity in multimodal settings.”
- Authors: han-xu; zhiyong-qin; di-shang; et al.

### EA-BRAIN-2026-0097

- Claim: 边界:加速器结果来自 Synopsys DC 在 SMIC 28nm 的综合估计与周期级仿真,非流片实测;GPU 对照仅 A800 FP16 批大小 1 配置。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.18610](https://arxiv.org/abs/2604.18610) SpikeMLLM: Spike-based Multimodal Large Language Models via Modality-Specific Temporal Scales and Temporal Compression
- Locator: 4.3. Deployment-oriented Co-designed System Study
- Evidence: 4.3 节方法学描述明确数字来自综合与仿真。
- Quote: “We implement the RTL design for SpikeMLLM and use Synopsys DC on SMIC 28nm CMOS technology to estimate logic area and power.”
- Authors: han-xu; zhiyong-qin; di-shang; et al.

### EA-BRAIN-2026-0025

- Claim: 路线边界:能耗数字全部为理论折算,未经真实神经形态硬件实测;且尽管在 19 个视觉/语言数据集上验证,作者自认尚未在 DVS 等神经形态任务上验证。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.12365](https://arxiv.org/abs/2604.12365) Adaptive Spiking Neurons for Vision and Language Modeling
- Locator: Limitation
- Evidence: Limitation 一节明确两条作者自述限制。
- Quote: “Our energy consumption estimates are based on theoretical calculations and do not include measurements on real neuromorphic hardware.”
- Authors: chenlin-zhou; sihang-guo; jiaqi-wang; et al.

### EA-BRAIN-2026-0048

- Claim: 路线边界(同规模量化 ANN 对比,表 8):BiSpikCLM-1.3B(T=4)平均 42.19%,与 BitNet 1.58-bit(42.66%)相当、高于 SmoothQuant W4A4(40.88%),但低于 OmniQuant W4A4(43.90%)与 TriLM 1.5B(43.16%);作者明确定位'主要贡献不是在精度上超越量化方法',并自述部分基准精度仍落后于大规模 ANN LLM。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.13859](https://arxiv.org/abs/2605.13859) BiSpikCLM: A Spiking Language Model integrating Softmax-Free Spiking Attention and Spike-Aware Alignment Distillation
- Locator: Appendix L Comparison with Quantized ANNs
- Evidence: 附录 L 表 8 给出与四种量化 LLM 的逐基准对比,正文明确不以精度超越量化为目标。
- Quote: “While quantized ANNs like 42 , 48 , and 20 may exhibit a marginal edge in accuracy, we emphasize that these represent fundamentally different methodological paradigms. Therefore, the primary contribution of our work is not to surpass quantization methods in accuracy, but to pioneer and validate a new, energy-efficient pathway for large language models.”
- Authors: sihang-guo; chenlin-zhou; jiaqi-wang; et al.

### EA-BRAIN-2026-0113

- Claim: 边界:尽管代理梯度训练成功扩展了 SNN 规模,该类梯度方法在所提分类学意义上基本非局部——空间上依赖全局误差传播,时间上需展开完整模拟时程并存储中间状态,因此在线学习在内存受限的神经形态硬件上仍是核心挑战。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.15058](https://arxiv.org/abs/2605.15058) NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework
- Locator: 4.2 Training Algorithms
- Evidence: 4.2 节结尾明确'fundamentally non-local',并给出 BPTT 内存足迹与更新锁定到序列末端的具体机制。
- Quote: “Despite these successes, most of these gradient-based methods share a common limitation regarding the proposed taxonomy: they are fundamentally non-local”
- Authors: alessio-caviglia; filippo-marostica; roberta-bardini; et al.

### EA-BRAIN-2026-0114

- Claim: 边界:ANN-to-SNN 转换路线虽然借成熟 ANN 工具链在静态视觉基准上取得历史最高精度、也是部署大型预训练模型的最易途径,但它把学习与脉冲动力学解耦——网络从不基于脉冲表示训练,因而限制时间编码利用、事件驱动输入适配与片上学习,且没有通往设备端自适应的路径。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.15058](https://arxiv.org/abs/2605.15058) NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework
- Locator: 4.2.2 ANN-to-SNN Conversion
- Evidence: 4.2.2 节先承认转换路线的精度与部署优势,再给出结构性限制并说明本文将其作为上界参照基线处理。
- Quote: “Conversion inherently decouples learning from spiking dynamics: the network never trains on spike-based representations, limiting its ability to exploit temporal coding, adapt to event-driven inputs, or perform on-chip learning.”
- Authors: alessio-caviglia; filippo-marostica; roberta-bardini; et al.

### EA-BRAIN-2026-0031

- Claim: 路线边界:作者自认目前缺乏在真实脉冲硬件上的端到端 LLM 部署,受算子、内存与精度-延迟约束;延迟消除跨域数据搬运的结论来自执行模型分析而非芯片实测。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.20289](https://arxiv.org/abs/2605.20289) Plug-and-Play Spiking Operators: Breaking the Nonlinearity Bottleneck in Spiking Transformers
- Locator: 7 Conclusion and Limitations
- Evidence: 结论与限制一节明确硬件部署缺口;6.4 节延迟分析基于执行模型。
- Quote: “A current limitation is the lack of end-to-end LLM deployment on real spiking hardware due to operator, memory, and accuracy–latency constraints.”
- Authors: xinzhe-yuan; xiang-peng; bin-gu; et al.

### EA-BRAIN-2026-0089

- Claim: 边界:低层闭环控制存在可见精度退化——SpikeVLA 线速度跟踪误差 0.42 vs NaVILA 0.23(约 1.8 倍),角速度误差 0.29 略优(vs 0.38),能耗 0.31µJ vs 5.80µJ;作者以'matches NaVILA overall, only minor differences'表述,但线速度误差接近两倍应视为该路线当前边界。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.27807](https://arxiv.org/abs/2606.27807) SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks
- Locator: 4.2 Main Results
- Evidence: 表 4 给出低层策略的线/角速度误差与资源效率;正文措辞偏乐观,表格数字显示线速度误差明显更大。
- Quote: “Table 4 : Closed-loop performance of the low-level policy. Method Linear Vel. Angular Vel. Resource Efficiency Error Error Mem(MB) Eng(µJ) ACEs( ) NaVILA 0.23 0.38 1.20 5.80 161.48 SpikeVLA 0.42 0.29 2.35 0.31 5.53”
- Authors: ruiqi-song; dujun-nie; siyu-teng; et al.

### EA-BRAIN-2026-0090

- Claim: 边界:脉冲动作策略的回报仍系统性低于 ANN 策略——四种群体编码核中拉普拉斯核最优(奖励 26.72、MEL 983.94),但全部低于 ANN 的 33.45(差距约 20%);模块逐个脉冲化时导航性能只有'适度退化'而计算与能耗单调下降,能效收益以一定控制性能为代价。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.27807](https://arxiv.org/abs/2606.27807) SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks
- Locator: 4.3 Ablation Study
- Evidence: 表 6 给出 ANN 与四种编码核 SNN 的奖励/MEL/资源对比;图 3 消融显示逐模块转换的性能-能耗权衡。
- Quote: “Table 6 : Rewards across different population encoders. MEL donates Mean Episode Length, where higher values indicate better survival and task persistence. Kernel Classes Rewards MEL Resource Efficiency Mem(MB) Eng(µJ) ACEs( ) ANN 33.45 976.81 1.20 5.80 161.48 Gaussian RBF kernel 23.10 973.11 2.35 0.41 7.34 Inverse Multiquadric kernel 22.73 939.35 2.35 0.68 12.06 Triangular kernel 25.15 966.29 2.35 0.25 4.42 Laplacian kernel 26.72 983.94 2.35 0.31 5.53”
- Authors: ruiqi-song; dujun-nie; siyu-teng; et al.

### EA-BRAIN-2026-0091

- Claim: 边界:作者自述 SpikeVLA 的能效与实时性在神经形态芯片上仍未验证,当前全部验证止于仿真与 GPU 平台;神经形态硬件验证被列为下一步工作,因此低功耗部署主张目前是潜力而非实证。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.27807](https://arxiv.org/abs/2606.27807) SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks
- Locator: 5 Conclusion
- Evidence: 结论局限段直陈神经形态芯片未验证;附录 A.2.3 确认能耗为 45nm 理论折算。
- Quote: “While SpikeVLA has demonstrated strong performance in simulations and on GPU platforms, its energy efficiency and real-time performance on neuromorphic chips remain unverified. Further validation on neuromorphic hardware will be the next step in our work.”
- Authors: ruiqi-song; dujun-nie; siyu-teng; et al.

### EA-BRAIN-2026-0070

- Claim: 定点精度边界:在代表性定点设置(32 总位、12 整数位)下,硬件仅在最多 2 ms 模拟时间内逐脉冲精确复现参考,之后定点舍入逐渐累积(退化为群体统计层面一致)。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.03191](https://arxiv.org/abs/2607.03191) AIGOR: A Modular, Event-Driven Neuromorphic Architecture for Configurable SNN Inference
- Locator: 6.1 Functional correctness
- Evidence: 6.1 节给出定点设置下的精确一致区间与舍入累积行为。
- Quote: “Under the representative fixed-point setting (32 total bits, 12 integer), the hardware reproduces the reference spike times exactly for up to 2 ms of simulated time”
- Authors: pierpaolo-perticaroli; roberto-ammendola; andrea-biagioni; et al.

### EA-BRAIN-2026-0072

- Claim: 资源边界实测:空间(工作者并行)组织下单核 2k 神经元仅神经元状态存储就占约 33% 器件 BRAM;全连接层突触随神经元数平方增长,同一 2k 神经元核携带 4M 突触,存 URAM 达器件 38% 并保持片上;2048 神经元单核约占器件 LUT 五分之一,再扩展受布局布线而非逻辑/存储容量限制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.03191](https://arxiv.org/abs/2607.03191) AIGOR: A Modular, Event-Driven Neuromorphic Architecture for Configurable SNN Inference
- Locator: 6.3 Resource utilization
- Evidence: 6.3 节给出状态/突触两类存储的不同缩放规律与后实现占用。
- Quote: “in the spatial organization every neuron datapath must read and write its own state in the same cycle, so each neuron’s state occupies an independent memory block, and a single core of 2k such neurons uses of order 33% of the device BRAM on state alone.”
- Authors: pierpaolo-perticaroli; roberto-ammendola; andrea-biagioni; et al.

### EA-BRAIN-2026-0037

- Claim: 路线边界:作者自认多层 SNN 训练机制的理论理解不足、Syn-SNN 需要大量超参数搜索才能达到高性能,且 DSTD 以小步数近似梯度训练的理论尚待检验;配合任务规模止于 CIFAR/F-MNIST 的事实,该路线的证据强度限于'机制可行'而非'大规模实用'。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.14672](https://arxiv.org/abs/2607.14672) Scalable Training of Continuous-Time Spiking Neural Networks with Differentiable Spike-Time Discretization
- Locator: 4 Discussion
- Evidence: 讨论节末段列出三条理论/实践限制;数据集设置见实验节。
- Quote: “For these reasons, SNNs, including Syn-SNNs, require extensive searches over many hyperparameter sets to achieve high learning performance.”
- Authors: yusuke-sakemi; tomoya-takeuchi; takeo-hosomi; et al.

### EA-BRAIN-2026-0055

- Claim: 验证边界(作者自述):本文吞吐/能耗结论止于仿真与分析层面,'未来工作将聚焦神经形态硬件上的验证'与块尺寸-稀疏度的自适应联合优化;结合估算方法(逐层实测稀疏度→理论 SOPs 与搬运比特→套用 OCMS/ICMS 硬件参数),该路线当前没有任何芯片实测数据。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.24841](https://arxiv.org/abs/2607.24841) Neuromorphic Diffusion Language Models: Addressing Compute and Memory Bottlenecks via Sparsity and Block Denoising
- Locator: VI Conclusions
- Evidence: 结论节未来工作句明确硬件验证缺口;V-B 1 说明吞吐/能耗为估算而非实测。
- Quote: “Future work will focus on validation on neuromorphic hardware and on adaptive strategies to jointly optimize and under varying system constraints.”
- Authors: dengyu-wu; clement-ruah; jiechen-chen; et al.

### EA-BRAIN-2026-0061

- Claim: 边界:当前 SNN 软件栈将全部神经元参数、状态变量与突触权重存于每 PE 的 SRAM,限制了可实现的网络规模;更长时间的仿真也因 SRAM 脉冲存储不足而不可行(DRAM 支持到位前该限制存在)。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.24396](https://arxiv.org/abs/2607.24396) The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing
- Locator: 4.4 Spiking Neural Networks (SNN)
- Evidence: 4.4 节作者自述 SRAM-only 存储限制网络规模与仿真时长。
- Quote: “In this work, all neuron parameters, state variables and synaptic weights are stored in the PE’s SRAM, which limits the size of the networks that can be implemented. This limitation will disappear once the DRAM is supported in the SNN software.”
- Authors: stefan-scholze; johannes-partzsch; sebastian-hppner; et al.

### EA-BRAIN-2026-0100

- Claim: 边界:在 Gen1 榜单上 Sequence-SOD 的最好成绩 26.88 mAP 仍显著低于 ANN/RNN 方法(RVT-B 47.2)与混合架构(HsVT-B 47.8、STMOD 44.3、SpikingViT 39.4),也低于较新 SNN 检测器(SpikeYOLO 40.4、SFOD 32.1);其价值在于同架构隔离验证序列训练(同基线 ODSNN 18.9 → 26.88),而非架构 SOTA。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.26703](https://arxiv.org/abs/2607.26703) Sequence-SOD: Bio-inspired Sequence-aware Spiking Object Detection for Event Cameras
- Locator: page 9
- Evidence: 表 3 给出 ANN/混合/SNN 三类检测器在 Gen1 的 mAP 与参数量;作者自述不与架构型方法竞争。
- Quote: “RVT-B [24] RNN/Trans. YOLOX [49] ✓ ✓ 50 47.2 18.5 RVT-S [24] RNN/Trans. YOLOX [49] ✓ ✓ 50 46.5 9.9 Hybrid SNN–ANN [34] Hybrid/RNN YOLOX [49] ✓ ✓ 50 43.0 7.7 HsVT-B [35] Hybrid/Trans. Head* ✓ * 50 47.8 17.2 EMS-YOLO [29] SNN YOLOv3 [47] ✗ ✗ * 26.7 6.2 Spiking CenterNet [31] SNN CenterNet ✗ * 100 22.9 13.0 SpikeFPN [33] SNN FPN ✗ * 60 22.3 22.0 STMOD [38] Hybrid/SNN ADH ✓ * 5 44.3 6.9 SFOD [30] SNN SSD ✗ ✓ 100 32.1 11.9 SpikingViT [32] Hybrid/SNN/Trans. YOLOX [49] ✓ ✓ 50 39.4 21.5 SpikeYOLO [36] S”
- Authors: katharina-bendig; ren-schuster; didier-stricker

### EA-BRAIN-2026-0102

- Claim: 边界(作者自述):SNN 检测器精度仍低于传统 ANN 与 RNN,本方法并未闭合该差距,只解决'孤立事件样本后重置网络状态'这一项局限;更好的训练方法、神经元模型与检测架构仍是开放问题。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.26703](https://arxiv.org/abs/2607.26703) Sequence-SOD: Bio-inspired Sequence-aware Spiking Object Detection for Event Cameras
- Locator: page 10
- Evidence: 讨论与局限节直陈精度差距未闭合与本研究定位。
- Quote: “Furthermore, SNNs still suffer from a lower accuracy compared to tra- ditional ANNs and Recurrent Neural Networks (RNNs). Our method does not close this gap completely. Instead, it addresses one limitation of previous SNN object detec - tors, namely the reset of the network state after isolated event samples.”
- Authors: katharina-bendig; ren-schuster; didier-stricker

### EA-BRAIN-2026-0078

- Claim: 边界:设计仅含两个重复刺激类器官与一个单刺激对照,结论属'可复现、对照支持的观察'而非群体级统计主张;且该研究不能裁决其他刺激协议下类器官是否支持结构化多跳计算——仅表明局灶单点协议下无可测传播。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.28068](https://arxiv.org/abs/2607.28068) Stimulus-Evoked Network Dynamics in Human Cortical Organoids: From a Graph-Computational Framework to Repeated-Stimulation Depression
- Locator: 4.7 Limitations
- Evidence: 4.7 节作者直陈样本局限与协议适用范围。
- Quote: “The design comprises two repeatedly-stimulated organoids and a single single-stimulation control; findings are therefore reproducible, control-supported observations rather than population-level statistical claims, and the control-based dissociation of stimulation history from maturation rests on one control organoid.”
- Authors: esmaeil-s-nadimi; vinay-c-gogineni; jan-matthias-braun; et al.

### EA-BRAIN-2026-0079

- Claim: 每日刺激条件化功能图在每会话仅 10 次试验的条件下不可靠估计:置换阈值接近空图,两种去趋势变体在密度、模块度、最大连通分量上分歧显著,作者因此不报告边级图统计——这是对把图论指标直接套用于类器官数据的方法学警示。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.28068](https://arxiv.org/abs/2607.28068) Stimulus-Evoked Network Dynamics in Human Cortical Organoids: From a Graph-Computational Framework to Repeated-Stimulation Depression
- Locator: 3.6 Per-day connectivity graphs were evaluated but are not reliable at
- Evidence: 3.6 节报告图构建被完整执行但不可靠,属负结果;摘要称其有方法学后果。
- Quote: “We therefore do not report edge-level graph statistics as primary results; and the robust network-level conclusions rest on (Eq. ( 20 )) and (Eq. ( 23 )). This is a limitation of trial count, not of the construction, as the graphs were built and evaluated for every organoid and day.”
- Authors: esmaeil-s-nadimi; vinay-c-gogineni; jan-matthias-braun; et al.

### EA-BRAIN-2026-0120

- Claim: 边界:椭球分解精确采样框架当前只扩展到数千维(演示规模为 160 维空间模型与 4776 维 normalizing flow);对具有数十亿参数的基础模型,需要稀疏椭球近似、层次椭球分解或变分-精确混合等进一步创新——预测编码引擎的'精确'主张止步于中小规模。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.00492](https://arxiv.org/abs/2608.00492) The Bayesian Reflex: A Predictive Coding Engine for Artificial Intelligence
- Locator: 8.3 Scalability and Open Challenges
- Evidence: 8.3 节给出当前演示规模(160 维与 4776 维)并明确十亿参数基础模型需要进一步创新;6.4 节补充需要稀疏 GP 近似等手段。
- Quote: “The ellipsoidal decomposition framework currently scales to dimensions of several thousand (as demonstrated on a 160‑dimensional spatial model and a 4776‑dimensional normalising flow). For foundation models with billions of parameters, further innovations are needed.”
- Authors: sourabh-bhattacharya

### EA-BRAIN-2026-0121

- Claim: 定位边界:作者自我警示——大脑不太可能实现 GP 回归所需的精确矩阵求逆,至多通过收敛到相同平衡点的神经动力学来近似;因此 Bayesian reflex 应被视为数学蓝图而非字面神经生物学模型,其'类脑'成分为计算原理层面的对应而非实现层面的等同。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.00492](https://arxiv.org/abs/2608.00492) The Bayesian Reflex: A Predictive Coding Engine for Artificial Intelligence
- Locator: 8.1 Biological Plausibility
- Evidence: 8.1 节先给出计算原语的生物类比(look-up table 类似 grid cell 编码、同心环带类似 centre-surround),再明确警示大脑不会做精确矩阵求逆,框架是数学蓝图。
- Quote: “Nevertheless, we caution that the brain is unlikely to implement the exact matrix inversions of GP regression; rather, it may approximate them through neural dynamics that converge to the same equilibrium points. The Bayesian reflex should be seen as a mathematical blueprint, not a literal neurobiological model.”
- Authors: sourabh-bhattacharya

### EA-BRAIN-2026-0062

- Claim: 边界:峰值每瓦操作数(TOPS/W)不足以比较使用不同表示、精度与工作条件的计算基底,且可能排除转换、控制、主机处理、散热与通信开销;作者主张未来进展应以部署系统指标而非孤立峰值 TOPS/W 声明来评估。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.03514](https://arxiv.org/abs/2608.03514) Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing
- Locator: 7.1 System-Level Benchmarking
- Evidence: 7.1 节开篇即给出峰值指标不足的两点理由(表示/精度/条件不同;边界排除项)。
- Quote: “Peak operations per watt is insufficient for comparing substrates that use different representations, precisions and operating conditions. It may also exclude conversion, control, host processing, cooling and communication.”
- Authors: eiman-kanjo; varuna-de-silva

### EA-BRAIN-2026-0084

- Claim: 边界:该文是纯前瞻框架,未报告任何类器官学习实验结果;作者自述生物基质固有变异性、有限寿命与发育随机性使可重复性成为核心挑战,类器官仍是黑箱,且当前 MEA 信息带宽比生物神经系统低多个数量级,可能约束可学习世界模型的复杂度。
- Stance: `gap` | Confidence: `direct`
- Paper: [2509.04633](https://arxiv.org/abs/2509.04633) The Physical Basis of Prediction: World Model Formation in Neural Organoids via an LLM-Generated Curriculum
- Locator: 5.2 Limitations and challenges
- Evidence: 5.2 节集中列出生物侧与接口侧挑战;全文无数据表与实验结果。
- Quote: “Furthermore, the information bandwidth of current MEA technology, while improving, is still orders of magnitude lower than that of biological nervous systems, potentially constraining the complexity of the world models that can be learned.”
- Authors: brennen-hill

### EA-BRAIN-2026-0109

- Claim: 缺口:持续学习中的灾难性遗忘仍是当前神经网络的重大挑战——在新任务上重训练通常会丢失先前知识;综述将结构改变、经验重放与实时振荡(theta 序列)等脑启发机制列为应对方向,但其中实时振荡机制仍属推测性假说。
- Stance: `gap` | Confidence: `direct`
- Paper: [2511.04455](https://arxiv.org/abs/2511.04455) The brain as a blueprint: a survey of brain-inspired approaches to learning in artificial intelligence
- Locator: 2.4 The continual learning challenge
- Evidence: 2.4 节把灾难性遗忘定位为当前网络的重大挑战;2.4.3 节自述该节探讨的是已知生理机制在持续学习中的'更推测性角色'。
- Quote: “This currently still poses a significant challenge for current neural networks, as re-training a model on new tasks will usually lead to the loss of previous knowledge”
- Authors: guillaume-etter

### EA-BRAIN-2026-0117

- Claim: 缺口:预测编码理论虽具解释力,但其实现长期受计算瓶颈阻碍——非线性分层模型的精确推断不可行,主流实现所用的 Laplace 近似对预测函数线性化并假设高斯后验,同时损失精确性与多峰捕捉能力,且在线学习所需的重复重优化难以保证。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.00492](https://arxiv.org/abs/2608.00492) The Bayesian Reflex: A Predictive Coding Engine for Artificial Intelligence
- Locator: 2.4 The Computational Bottleneck
- Evidence: 2.4 节把预测编码的瓶颈归结为精确推断不可行与在线更新难保证两点,并点名 Laplace 近似的主流实现损失精确性与多峰性。
- Quote: “For all its theoretical appeal, predictive coding faces a severe computational bottleneck: exact inference in non‑linear hierarchical models is intractable. The Laplace approximation (used in most implementations) linearises the prediction functions and assumes Gaussian posteriors, losing both exactness and the ability to capture multi‑modality.”
- Authors: sourabh-bhattacharya

### EA-BRAIN-2026-0067

- Claim: 评测缺口:作者指出模拟、光子与神经形态加速器应与强优化数字基线比较,而非与未优化的通用实现比较,且能耗边界应覆盖整个任务或任务周期(含传感、存储搬运、标定摊销、待机与执行)——现有报告普遍未满足该标准,构成领域评测空白。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.03514](https://arxiv.org/abs/2608.03514) Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing
- Locator: 6 Energy Efficiency as a System Property
- Evidence: 第 6 节给出强数字基线要求与任务/任务周期能量边界分解。
- Quote: “Analogue, photonic and neuromorphic accelerators should therefore be compared with a strong, optimised digital baseline rather than with an unoptimised general-purpose implementation.”
- Authors: eiman-kanjo; varuna-de-silva

## References

- `2509.04633` [The Physical Basis of Prediction: World Model Formation in Neural Organoids via an LLM-Generated Curriculum](https://arxiv.org/abs/2509.04633) (2025-09-04T19:51:00Z)
- `2509.05276` [SpikingBrain: Spiking Brain-inspired Large Models](https://arxiv.org/abs/2509.05276) (2025-09-05T17:34:00Z)
- `2510.05168` [Discretized Quadratic Integrate-and-Fire Neuron Model for Deep Spiking Neural Networks](https://arxiv.org/abs/2510.05168) (2025-10-05T02:30:10Z)
- `2511.04455` [The brain as a blueprint: a survey of brain-inspired approaches to learning in artificial intelligence](https://arxiv.org/abs/2511.04455) (2025-11-06T15:26:18Z)
- `2603.16148` [NeuronSpark: A Spiking Neural Network Language Model with Selective State Space Dynamics](https://arxiv.org/abs/2603.16148) (2026-03-17T06:01:05Z)
- `2604.12365` [Adaptive Spiking Neurons for Vision and Language Modeling](https://arxiv.org/abs/2604.12365) (2026-04-14T06:53:51Z)
- `2604.16475` [Spike-driven Large Language Model](https://arxiv.org/abs/2604.16475) (2026-04-11T17:58:35Z)
- `2604.18610` [SpikeMLLM: Spike-based Multimodal Large Language Models via Modality-Specific Temporal Scales and Temporal Compression](https://arxiv.org/abs/2604.18610) (2026-04-13T15:32:44Z)
- `2605.13859` [BiSpikCLM: A Spiking Language Model integrating Softmax-Free Spiking Attention and Spike-Aware Alignment Distillation](https://arxiv.org/abs/2605.13859) (2026-04-14T09:57:15Z)
- `2605.15058` [NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework](https://arxiv.org/abs/2605.15058) (2026-05-14T16:50:15Z)
- `2605.20289` [Plug-and-Play Spiking Operators: Breaking the Nonlinearity Bottleneck in Spiking Transformers](https://arxiv.org/abs/2605.20289) (2026-05-19T06:59:46Z)
- `2606.27807` [SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks](https://arxiv.org/abs/2606.27807) (2026-06-26T07:45:45Z)
- `2607.03191` [AIGOR: A Modular, Event-Driven Neuromorphic Architecture for Configurable SNN Inference](https://arxiv.org/abs/2607.03191) (2026-07-03T10:52:38Z)
- `2607.14672` [Scalable Training of Continuous-Time Spiking Neural Networks with Differentiable Spike-Time Discretization](https://arxiv.org/abs/2607.14672) (2026-07-16T07:18:24Z)
- `2607.24396` [The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing](https://arxiv.org/abs/2607.24396) (2026-07-27T13:13:02Z)
- `2607.24841` [Neuromorphic Diffusion Language Models: Addressing Compute and Memory Bottlenecks via Sparsity and Block Denoising](https://arxiv.org/abs/2607.24841) (2026-07-24T11:14:57Z)
- `2607.26703` [Sequence-SOD: Bio-inspired Sequence-aware Spiking Object Detection for Event Cameras](https://arxiv.org/abs/2607.26703) (2026-07-29T09:49:56Z)
- `2607.28068` [Stimulus-Evoked Network Dynamics in Human Cortical Organoids: From a Graph-Computational Framework to Repeated-Stimulation Depression](https://arxiv.org/abs/2607.28068) (2026-07-30T11:45:16Z)
- `2608.00492` [The Bayesian Reflex: A Predictive Coding Engine for Artificial Intelligence](https://arxiv.org/abs/2608.00492) (2026-08-01T07:32:39Z)
- `2608.03514` [Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing](https://arxiv.org/abs/2608.03514) (2026-08-04T11:57:50Z)
