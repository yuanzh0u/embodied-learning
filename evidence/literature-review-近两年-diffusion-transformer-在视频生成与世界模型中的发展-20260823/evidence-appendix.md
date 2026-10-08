# Evidence Appendix: 近两年（2024-08至2026-08）Diffusion Transformer 在视频生成与世界模型中的发展

- Time range: 2024-08 至 2026-08
- Events: 69
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-DIT-2026-0001

- Claim: 在 Coinrun500k 上，AVID（71M）在不访问预训练权重的所有方法中获得最佳 Action Error Ratio（1.154），整体表现与需要权重的 ControlNet 相当。
- Stance: `support` | Confidence: `direct`
- Paper: [2410.12822](https://arxiv.org/abs/2410.12822) AVID: Adapting Video Diffusion Models to World Models
- Locator: 4.3 Results
- Evidence: 4.3 Results 的 Table 1 显示 Large AVID(71M) Action Err. Ratio 1.154，为列内 no-weight-access 方法最优；文本明言 71M 规模 AVID 对 ControlNet 多数指标第二、Action Error Ratio 最佳。
- Quote: “For the larger model size of 71M, AVID performs the second best for most metrics to ControlNet, but obtains the best performance for Action Error Ratio.”
- Authors: marc-rigter; tarun-gupta; agrin-hilmkil; et al.

### EA-DIT-2026-0010

- Claim: 组合泛化随 training 覆盖更多模板/物体组合而改善：DiT-XL 的 out-of-template 人工 abnormal 率从 6 模板的 67% 降至 60 模板的 10%；DiT-B（60 模板）为 24%，说明组合多样性与模型容量均关键。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.02385](https://arxiv.org/abs/2411.02385) How Far is Video Generation from World Model: A Physical Law Perspective
- Locator: 4.2 Scaling Law Observed for Combinatorial Generalization
- Evidence: 4.2 报 6→60 模板 abnormal 从 67%→10%，DiT-B 60 模板升至 24%，明言 'both model capacity and coverage of the combination space are crucial'。
- Quote: “the abnormal rate for human evaluation significantly reduces from 67% to 10%.”
- Authors: bingyi-kang; yang-yue; rui-lu; et al.

### EA-DIT-2026-0013

- Claim: 训练无关缓存 AdaCache-fast 在 Open-Sora 文生视频基线上取得最高 2.24x 推理加速（VBench 79.48 vs 基线 79.22，几乎无质量下降），优于 T-GATE 1.10x、PAB 1.34x 等既有训练无关方法。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.02397](https://arxiv.org/abs/2411.02397) Adaptive Caching for Faster Video Generation with Diffusion Transformers
- Locator: 5.2 Main results
- Evidence: 作者在 5.2 记录 AdaCache-fast 于 Open-Sora 上最高加速 2.24，质量 VBench 79.48 接近基线 79.22；与引言图1 '4.7 speedup (720p-2s)' 互补。
- Quote: “AdaCache-fast gives the highest acceleration of 2.24 with a slight drop in quality.”
- Authors: kumara-kahatapitiya; haozhe-liu; sen-he; et al.

### EA-DIT-2026-0015

- Claim: 用户 A/B 研究中，AdaCache 相对 PAB 在相近加速下获得更高偏好率（70%），且与未加速基线不可区分超过一半时间（41%）；运动正则化变体更受偏好（25% vs 14%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.02397](https://arxiv.org/abs/2411.02397) Adaptive Caching for Faster Video Generation with Diffusion Transformers
- Locator: 5.2 Main results
- Evidence: 5.2 的用户研究（50 题 x 36 用户共 1800 回应）报告 AdaCache 对 PAB 有 70% 偏好、41% 判定为与基线不可区分；w/ MoReg 偏好 25% vs 14%。
- Quote: “Between AdaCache and PAB, we see a clear win for our method (70%) while being extremely-similar to the baseline more than half the time (41%).”
- Authors: kumara-kahatapitiya; haozhe-liu; sen-he; et al.

### EA-DIT-2026-0020

- Claim: 视频 DiT 被系统实证确认存在缩放律：验证损失随模型尺寸与训练 token 呈可预测幂律，抽取优化条件下能与 LLM 式缩放律拟合对齐。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.17470](https://arxiv.org/abs/2411.17470) Towards Precise Scaling Laws for Video Diffusion Transformers
- Locator: page 1 (Abstract + 1. Introduction) / page 7 (Eq 15, Table 3)
- Evidence: 作者在摘要与引言声明 'We confirm the existence of scaling laws in video diffusion transformers'，并给出 L(T,N) 幂律通式与跨模型尺寸一致拟合（图 1、5），为本命题提供直接证据。
- Quote: “We confirm the existence of scaling laws”
- Authors: yuanyang-yin; yaqi-zhao; mingwu-zheng; et al.

### EA-DIT-2026-0021

- Claim: 视频 DiT 最优超参（batch size 与 learning rate）可被幂律预测：Bopt=2.1797e4·T^0.8080·N^0.1906、ηopt=0.0002·T^-0.0453·N^-0.1619；较 LLM，视频模型对 batch/lr 更敏感。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.17470](https://arxiv.org/abs/2411.17470) Towards Precise Scaling Laws for Video Diffusion Transformers
- Locator: page 6 (Table 1, Table 2) / page 13 (Table 4)
- Evidence: 作者由 Mini-Batch SGD 收敛分析推导 ηopt 依赖于 T 与 Bopt，Bopt 平衡梯度噪声与更新步数，拟合出 Bopt、ηopt 幂律（式 10、13），并在 1.07B/4B-10B token 网格搜索验证预测位置对应最低 validation loss（图 4）。
- Quote: “more sensitive to learning rate and batch size”
- Authors: yuanyang-yin; yaqi-zhao; mingwu-zheng; et al.

### EA-DIT-2026-0023

- Claim: 性能缩放通式 L(T,N)=(Tc/T)^αT+(Nc/N)^αN+L∞ 可在最优超参下预测任意模型尺寸与 compute 的 validation loss，外推验证偏差约 0.03%（1.07B/10B tokens）与 0.15%（0.72B/140B tokens）。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.17470](https://arxiv.org/abs/2411.17470) Towards Precise Scaling Laws for Video Diffusion Transformers
- Locator: page 7 (Eq 15, Table 3) / page 7 (Fig 5) / page 8 (4.3.2)
- Evidence: 式 15/21 拟合系数 Tc=0.0373, αT=0.2917, Nc=0.0082, αN=0.3188, L∞=0.4856（Table 3）。外推图 5b 报告 1.07B/10B 偏差 0.03%、0.72B/140B 偏差 0.15%；4.3.2 报告 MSE 由 4.31e-7 降至 2.35e-7（-45.5%，相对次优 hp）。
- Quote: “the deviations between our predicted and experimental results were”
- Authors: yuanyang-yin; yaqi-zhao; mingwu-zheng; et al.

### EA-DIT-2026-0026

- Claim: 综述以 '时空分布序列采样' 界定：空间一致性=分布内任意两点语义/视觉属性兼容（主体身份、场景布局、光照风格、颜色纹理、静态语义等），时间一致性=相邻样本平滑演化（表1 再细分为运动平滑/时序动态/闪烁抑制/动态语义）；时间一致性本质是序列生成的转移概率建模问题。
- Stance: `support` | Confidence: `direct`
- Paper: [2502.17863](https://arxiv.org/abs/2502.17863) A Survey: Spatiotemporal Consistency in Video Generation
- Locator: 1. Introduction
- Evidence: 1. Introduction 明确定义 Spatial/Temporal Consistency 并配 Table 1 维度分类与常见问题；作者视此为综述的核心贡献（'reformulating the problem from the perspective of sequence sampling'）。
- Quote: “Spatial Consistency is defined as the compatibility between any two sample points in the distribution regarding semantic and visual attributes, including stability in subject identity, scene layout, lighting style, and so forth. Temporal Consistency further requires smooth evolutionary transitions between adjacent samples in the sequence.”
- Authors: zhiyu-yin; kehai-chen; xuefeng-bai; et al.

### EA-DIT-2026-0027

- Claim: 综述将视频生成评测指标分为三大类：帧质量评估（像素/语义级，如 PSNR/SSIM/IS/FID/Aesthetic）、视频平滑评估（时间一致性/运动合理）、整体视频评估；并指出时间动力学类基准（ChronoMagic-Bench/T2VBench、MiraBench/DEVIL）专门用于评估时序一致性/逻辑与运动自然度。
- Stance: `support` | Confidence: `citation-supported`
- Paper: [2502.17863](https://arxiv.org/abs/2502.17863) A Survey: Spatiotemporal Consistency in Video Generation
- Locator: 7.2. Evaluation Metrics
- Evidence: 综述在其评测章节显著整理了三类指标与时间/空间基准，作为其系统综述的归纳而非自身实验；用时序动力学基准强调时间一致性/逻辑与运动自然。
- Quote: “Frame quality assessment focuses on the consistency of static spatial elements within individual frames.”
- Authors: zhiyu-yin; kehai-chen; xuefeng-bai; et al.

### EA-DIT-2026-0029

- Claim: Vid2World 通过 video diffusion causalization 与 causal action guidance 两个机制，把被动视频扩散模型转成支持自回归、动作条件生成的交互式世界模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.14357](https://arxiv.org/abs/2505.14357) Vid2World: Crafting Video Diffusion Models to Interactive World Models
- Locator: 6 Conclusion
- Evidence: 6 Conclusion 作者总结其方法贡献即为两机制的自回归动作条件生成，客观描述方法定位。
- Quote: “We propose Vid2World, introducing two key mechanisms—video diffusion causalization and causal action guidance—to support autoregressive, action-conditioned generation.”
- Authors: siqiao-huang; jialong-wu; qixing-zhou; et al.

### EA-DIT-2026-0030

- Claim: 消融显示对 Extrapolative 与 Masked 权重迁移，强制 action guidance 都带来更好性能（相对训练/推理中从不丢弃动作的对应版本）。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.14357](https://arxiv.org/abs/2505.14357) Vid2World: Crafting Video Diffusion Models to Interactive World Models
- Locator: 5.4 Ablation Study
- Evidence: 5.4 Ablation Study 报告：在 Extrapolative 与 Masked weight transfer 下，走 action guidance 的版本性能优于其从未丢弃动作的 counterpart。
- Quote: “we observe that for both Extrapolative Weight Transfer and Masked Weight Transfer, enforcing action guidance yields better performance compared to their counterpart, which have never dropped out action in training and inference.”
- Authors: siqiao-huang; jialong-wu; qixing-zhou; et al.

### EA-DIT-2026-0031

- Claim: Masked 与 Extrapolative 权重迁移都优于 Shift 权重迁移，且 Extrapolative 略优于 Masked，二者共同支撑 Vid2World 的性能。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.14357](https://arxiv.org/abs/2505.14357) Vid2World: Crafting Video Diffusion Models to Interactive World Models
- Locator: 5.4 Ablation Study
- Evidence: 5.4 Ablation Study 依表说明两种迁移优于 Shift，Extrapolative 略优于 Masked。
- Quote: “both Masked and Extrapolative Weight Transfer yield better performance than Shift Weight Transfer, and utilizing Extrapolative Weight Transfer yields slightly better outcomes compared to Masked Weight Transfer.”
- Authors: siqiao-huang; jialong-wu; qixing-zhou; et al.

### EA-DIT-2026-0034

- Claim: 在 300 帧长视频 world coherence 评估上，VRAG 以 SSIM 0.506 优于所有对比基线（DF-window20 0.466、YaRN 0.462、History Buffer 0.459、Frame Pack 0.421）。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.21996](https://arxiv.org/abs/2505.21996) VRAG: Learning World Models for Interactive Video Generation
- Locator: 4.3 World Coherence Results
- Evidence: 4.3 World Coherence Results 文本明言 VRAG 全面最佳，Tab. 1 给出 SSIM 0.506（其下所有基线均低于 0.466）。
- Quote: “Our VRAG method achieves the best performance across all metrics, demonstrating its superior ability to maintain world coherence in generated videos.”
- Authors: taiye-chen; xun-hu; zihan-ding; et al.

### EA-DIT-2026-0035

- Claim: 在 1200 帧 compounding error 评估中，VRAG 以平均 SSIM 0.349 优于所有基线（History Buffer 0.188、DF-window20 0.321、YaRN 0.316）。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.21996](https://arxiv.org/abs/2505.21996) VRAG: Learning World Models for Interactive Video Generation
- Locator: 4.4 Compounding Error Results
- Evidence: 4.4 Compounding Error Results 明言 VRAG SSIM 0.349 优于基线，History Buffer 仅 0.188（naive retrieval 未获 in-context 训练则失效）。
- Quote: “our VRAG method achieves superior performance with an SSIM score of 0.349, demonstrating better structural similarity preservation compared to baseline methods.”
- Authors: taiye-chen; xun-hu; zihan-ding; et al.

### EA-DIT-2026-0036

- Claim: 在真实世界数据集 RealEstate10K 上从 Diffusion Forcing Transformer (DFoT) 初始化仅 finetune 2 epochs（约 10% 原始训练量），VRAG 的记忆能力显著超 DFoT（SSIM 0.9116 vs 0.4436，FVD 221 vs 337.5）。
- Stance: `support` | Confidence: `direct`
- Paper: [2505.21996](https://arxiv.org/abs/2505.21996) VRAG: Learning World Models for Interactive Video Generation
- Locator: 4.6 Extension: Real World Setting
- Evidence: 4.6 Extension: Real World Setting 明言 2 epochs 后显著超越 DFoT，Tab. 4 给 SSIM/PSNR/LPIPS/FVD。
- Quote: “After fine-tuning for just 2 epochs (10% of the original training steps), our method significantly outperforms the DFoT baseline in terms of memorization capability.”
- Authors: taiye-chen; xun-hu; zihan-ding; et al.

### EA-DIT-2026-0044

- Claim: 统一训练无关框架（TempCache+AnnCA+AnnSA，FAST-AR）在 RollingForcing 长回卷上达最高 10.8x（LSH 10.7x）端到端加速并保持 FA3 级质量，而最优基线组合 FlowCache+RadialAttn 仅 4.4x 且质量崩坏。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.01801](https://arxiv.org/abs/2602.01801) Fast Autoregressive Video Diffusion and World Models with Temporal Cache Compression and Sparse Attention
- Locator: 7.1 Quantitative Results
- Evidence: 7.1 报告 All Ours-LSH/Quant 端到端达 10.7-10.8x 且保持 FA3 级质量，而 FlowCache+RadialAttn 仅 4.4x 并 'collapses in quality'；与表1一致。
- Quote: “Combining cache compression with SA/CA sparsity yields the strongest overall gains: All Ours-LSH/Quant achieves up to 10.7– 10.8 end-to-end speedup while preserving FA3-level quality, while the best baseline combination (FlowCache+RadialAttn) reaches only 4.4 and collapses in quality.”
- Authors: dvir-samuel; issar-tzachor; matan-levy; et al.

### EA-DIT-2026-0045

- Claim: TempCache（时间对应 KV 合并）把注意力 KV 缓存压缩到 ~16% 最小密度而保持 90-91% 注意力召回并匹配 dense 质量（VBench 84.1），而既有训练无关缓存 TeaCache/FlowCache 仅提供 1.1-1.3x 加速。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.01801](https://arxiv.org/abs/2602.01801) Fast Autoregressive Video Diffusion and World Models with Temporal Cache Compression and Sparse Attention
- Locator: 7.1 Quantitative Results
- Evidence: 7.1 报告 TempCache-LSH/Quant 把密度降到 16%-17%，recall 90-91%，质量匹配 dense（VBench 84.1），而 TeaCache/FlowCache 仅 1.1-1.3x。
- Quote: “both TempCache-LSH/Quant compress the KV cache aggressively (down to 16% Min Density) while preserving high attention recall ( 90–91%) and matching dense quality (VBench 84.1).”
- Authors: dvir-samuel; issar-tzachor; matan-levy; et al.

### EA-DIT-2026-0046

- Claim: 随回卷长度增长，dense 基线 FA3 吞吐持续下滑、峰值显存随 KV cache 扩张上升，而 FAST-AR 在 3000 帧回卷中维持近常数 FPS 且显存平坦（有界 cache）；该趋势在世界模型（LongVie2）上同样被观察到。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.01801](https://arxiv.org/abs/2602.01801) Fast Autoregressive Video Diffusion and World Models with Temporal Cache Compression and Sparse Attention
- Locator: 7.1 Quantitative Results
- Evidence: 7.1 及其图6 记录 FA3 与稀疏基线的吞吐随回卷下滑/显存上升，而本方法 FPS 与显存保持近常数（SA 稀疏使 attention 成本不随上下文增长）。
- Quote: “Peak GPU memory for the dense attention baseline and current approaches increases with the expanding KV cache, whereas our method stays constant.”
- Authors: dvir-samuel; issar-tzachor; matan-levy; et al.

### EA-DIT-2026-0047

- Claim: RealWonder 以物理仿真为中间表征，把连续的 3D 物理动作翻译为 optical flow 和 coarse RGB 预览来条件化视频生成器，从而绕过了'对连续无界动作 tokenize'与'收集 action-video 训练对'两大障碍（训练仅需 2D flow-video 对）。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05449](https://arxiv.org/abs/2603.05449) RealWonder: Real-Time Physical Action-Conditioned Video Generation
- Locator: 3 RealWonder
- Evidence: 作者在总览中明确：该架构规避两个根本障碍——用物理仿真器处理无界力/动作输入而免 tokenize，以及仅训练 flow-video 对应而免 action-video 对。
- Quote: “This architecture elegantly sidesteps two fundamental obstacles: it avoids tokenizing continuous actions by leveraging physics simulators that naturally handle unbounded force and action inputs”
- Authors: wei-liu; ziyu-chen; zizhang-li; et al.

### EA-DIT-2026-0048

- Claim: RealWonder 实现实时流式 action-conditioned 视频生成：13.2 FPS @480x832（单 GPU）、动作到结果延迟 0.73s，相较 PhysGaussian（4.84s 延迟/0.207 FPS）与不可流式的视频生成基线（<0.3 FPS）显著更快。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05449](https://arxiv.org/abs/2603.05449) RealWonder: Real-Time Physical Action-Conditioned Video Generation
- Locator: 4.1 Results
- Evidence: 4.1 报告 RealWonder 达成实时流式生成，Table 3 显示其 FPS 13.2、延迟 0.73s，远优于基线。
- Quote: “RealWonder achieves real-time streaming generation”
- Authors: wei-liu; ziyu-chen; zizhang-li; et al.

### EA-DIT-2026-0049

- Claim: 在自建 30 图评测集上，RealWonder 相对 PhysGaussian/CogVideoX-I2V/Tora 在所有指标上取得最佳或次佳，并在 2AFC 用户研究中被显著更偏好（尤其 Action Following 与 Physical Plausibility 维度），说明物理仿真桥条件下视频模型优于纯物理基或纯 2D 条件基线。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05449](https://arxiv.org/abs/2603.05449) RealWonder: Real-Time Physical Action-Conditioned Video Generation
- Locator: 4.1 Results
- Evidence: 4.1 报告 RealWonder best/second-best 于全部指标且显著更受偏好；表列 PhysReal 0.705 最高，Action Following 偏好率 88.4%/89.6%/83.9%。
- Quote: “RealWonder achieves the best or second best numbers across all metrics, and it is significantly more favored compared to other baselines”
- Authors: wei-liu; ziyu-chen; zizhang-li; et al.

### EA-DIT-2026-0050

- Claim: RealWonder 通过 Distribution Matching Distillation + Self-Forcing 把 flow 条件的多步教师蒸馏为 4 步 causal student，把控制直接注入起始噪声，从而支持实时流式；并用 KV cache（置于 RoPE 前）+ attention sink 缓解长视界漂移。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.05449](https://arxiv.org/abs/2603.05449) RealWonder: Real-Time Physical Action-Conditioned Video Generation
- Locator: 3.3 Real-Time Conditional Video Generation
- Evidence: 作者在 3.3 描述蒸馏为 4 步 causal student（DMD 反向 KL）+ Self-Forcing 自回归 rollout，并用 KV cache 于 RoPE 前 + attention sink 修复长序列质量退化。
- Quote: “we distill it into a causal student that generates frames sequentially in just 4 denoising steps”
- Authors: wei-liu; ziyu-chen; zizhang-li; et al.

### EA-DIT-2026-0053

- Claim: ACWM-DiT-S（latent bidirectional 视频 DiT + AdaLN 动作条件）在所有四类物理交互上取得强 InD 预测：简单、重复动力学近完美（Push Rope、Reacher），而大形变/大前景运动任务（Cloth Move、Stack Cube）InD 误差最高。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.08567](https://arxiv.org/abs/2605.08567) ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models
- Locator: 5.1 Main Results
- Evidence: 5.1 报告 ACWM-DiT-S 在四类物理上强 InD；简单任务近完美（Push Rope M-MSE 2.61/SSIM 0.988、Reacher M-MSE 5.63/SSIM 0.992），Cloth Move M-MSE 63.68 最高。
- Quote: “ACWM-DiT-S achieves strong in-distribution performance across all four physics categories. Environments with simpler, repetitive dynamics achieve the highest fidelity: Push Rope (M-MSE 2.61, SSIM 0.988) and Reacher (M-MSE 5.63, SSIM 0.992) are predicted with near-perfect structural similarity and low motion-region error”
- Authors: haotian-xue; yipu-chen; liqian-ma; et al.

### EA-DIT-2026-0055

- Claim: action-conditioning 机制消融表明：cross-attention 注入动作 token 在动作高维（Robot Arm）时显著优于 AdaLN（InD MSE 0.691 vs 1.434），而在低维任务（Push Cube/Push Rope）无益甚至略差；时间感知的 causal video VAE 全场景优于逐帧独立的 image VAE。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.08567](https://arxiv.org/abs/2605.08567) ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models
- Locator: 5.2 Ablation Studies
- Evidence: 5.2 报告 cross-attention 在高维动作（Robot Arm）上更好绑定 joint command 与 articulated motion，对低维无益；并报告 WanVAE（causal, 时间压缩）在 Pour Water/Robot Arm 上均优于 FLUX VAE。
- Quote: “cross-attention is most useful when actions are high-dimensional and require structured spatial-temporal grounding”
- Authors: haotian-xue; yipu-chen; liqian-ma; et al.

### EA-DIT-2026-0056

- Claim: ACWM-Phys 为 8 个环境设计受控、物理相关的 InD/OoD 分布偏移（未折叠的物体数量、workspace 范围、rope/cloth 尺寸、粒子数量、水位、goal 区域），作为 agentic 物理世界模型的评测方法学贡献。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.08567](https://arxiv.org/abs/2605.08567) ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models
- Locator: 4.1.2 In-Distribution and Out-of-Distribution Evaluation Protocols
- Evidence: 作者在方法设计部分说明其设计原则：每环境支持一个受控、物理动因的分布偏移，且因为全仿真而精确可复现、无传感器噪声，从而干净测量泛化 gap。
- Quote: “every environment supports a controlled, physically motivated distribution shift between the InD and OoD splits”
- Authors: haotian-xue; yipu-chen; liqian-ma; et al.

### EA-DIT-2026-0057

- Claim: SANA-WM 在作者自建 1 分钟基准的两轨迹 split 上取得更强 action-following：refined 输出 RotErr 4.50°/8.34°、CamMC 1.41/1.44，优于 Infinite-World/LingBot-World/HY-WorldPlay/Matrix-Game 3.0 等基线。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.15178](https://arxiv.org/abs/2605.15178) SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer
- Locator: 5.3. Main Results (Table 2, page 8)
- Evidence: 5.3 记录 refined 输出在 Simple/Hard 两 split 获最低 RotErr/CamMC，明确 'gives the strongest action following on both trajectory splits'，且优于大小型号基线；VBench 与 LingBot-World 相当（80.62/81.89）。
- Quote: “SANA-WM gives the strongest action following on both trajectory splits.”
- Authors: haoyi-zhu; haozhe-liu; yuyang-zhao; et al.

### EA-DIT-2026-0058

- Claim: SANA-WM 以 51.1GB/24.1 视频-时（8×H100）完成单 GPU/分钟级 720p 推理，refiner 全流程 74.7GB/22.0 视频-时仍比最快的 480p 基线快；distilled+NVFP4 变体在单 RTX 5090 上 34s 生成 60s 720p clip（宣称 36x 吞吐）。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.15178](https://arxiv.org/abs/2605.15178) SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer
- Locator: 5.3. Main Results (Table 2) & Abstract
- Evidence: 5.3 报 SANA-WM 51.1GB/24.1 视频-时、refiner 74.7GB/22.0 视频-时且 'still 3.7x faster than the fastest visible 480p baseline'；Abstract/蒸馏页报单 RTX 5090+NVFP4 34s/60s-720p 与 '36x higher throughput'。
- Quote: “SANA-WM fits in 51.1 GB and reaches 24.1 videos/hour; with the refiner, the full pipeline remains within the 80 GB H100 budget (74.7 GB) and reaches 22.0 videos/hour, still 3.7× faster than the fastest visible 480p baseline.”
- Authors: haoyi-zhu; haozhe-liu; yuyang-zhao; et al.

### EA-DIT-2026-0060

- Claim: RynnWorld-Teleop 用深度调制渲染的 21 关节手部骨骼动作表示（颜色与关节/骨骼直径按相机空间深度动态缩放）来编码精确手-物交互所需的 3D 结构线索，并投影为与目标视频 latent 时空对齐的控制 latent。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: 3.2 Depth-Aware Action Representation
- Evidence: 作者在 3.2 描述深度调制渲染以解决 2D 投影的深度歧义，产出的控制 latent 与目标视频 latent 时空对齐用于 grounding。
- Quote: “the depth-encoded color mapping and diameter of each joint and bone are dynamically scaled according to their camera-space depth”
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### EA-DIT-2026-0061

- Claim: RynnWorld-Teleop 通过分布对齐的 additive patch-embedding 把骨骼控制 latent 注入视频 DiT，并以零初始化的 gating scalar 保持与预训练视频流的统计兼容，从而在纳入动作条件时不破坏 base DiT 的生成先验。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: 3.3 Action-Conditioned Video Generation
- Evidence: 作者在 3.3 描述并行控制 patch-embedding 层、学习到的 scalar gate、均值/方差运行对齐，并 zero-init gating 以逐步纳入 pose 信号而不 destabilize 预训练权重
- Quote: “we adopt an additive patch-embedding scheme with distribution alignment”
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### EA-DIT-2026-0062

- Claim: 蒸馏因果学生模型实现实时单趟生成：4-step 条件流匹配，在单 H100 上 40.0 FPS（其中 Causal DiT 去噪约占 72% 延迟），明显超出现有 action-conditioned 世界模型数 Hz 的帧率，从而弥合传感-执行间隙。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: 5.2 Digital Teleoperation System Evaluation
- Evidence: 5.2 的延迟分析报告因果学生 4-step 达 40.0 fps（H100），分解为 skeletal encoding 5%/DiT denoising 72%/visual decode 23%，并称超出典型 - Hz。
- Quote: “Our distilled causal student model, optimized with a 4-step flow matching schedule, achieves a high throughput of 40.0 fps”
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### EA-DIT-2026-0063

- Claim: RynnWorld-Teleop 在 EgoDex-Test 与 Robotic-Test 上显著优于通用 I2V（Wan/CogVideoX）与 action-conditioned 世界模型（InterDyn/CosHand/Mask2IV）：如 FVD 585 vs vanilla SFT 1223、PSNR 26.08 vs 20.93，说明自定义深度骨骼条件 + 分布对齐优于简单 SFT 或现有 action-conditioned 基准。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: 5.3 Action-Conditioned World Model Evaluation
- Evidence: 5.3 报告其对通用 I2V 与 action-conditioned 模型的全面领先；vanilla SFT 基线 FVD 1223 vs 585、PSNR 20.93 vs 26.08 凸显专项条件化的重要性。
- Quote: “our method significantly outperforms both general-purpose I2V models and action conditioned video generation models”
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### EA-DIT-2026-0064

- Claim: 以 RynnWorld-Teleop 生成数据做数据引擎：纯由 300 生成 episode（无真实数据）训练的策略可 zero-shot 迁移到真机（Block Pushing 82.86%、Bimanual Lifting 77.14%），且用 300 生成数据增强 300 真实 episode 在几乎所有任务一致提升成功率（如 Lid Placement 某策略 +20%）。
- Stance: `support` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: 5.2 Digital Teleoperation System Evaluation
- Evidence: 5.2 报真机 4 任务成功率：生成-only 达竞争性成功率，增强真实数据在近全部任务一致提升，Lid Placement 提升最大。
- Quote: “augmenting 300 real-world episodes with 300 RynnWorld-Teleop-generated episodes leads to consistent performance gains across nearly all tasks”
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### EA-DIT-2026-0004

- Claim: 在 RT1 上，从零训练的 action-conditioned diffusion 得到最佳 Action Error Ratio（尽管视觉质量更低），说明动作一致性优先时 from-scratch 也可取胜。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2410.12822](https://arxiv.org/abs/2410.12822) AVID: Adapting Video Diffusion Models to World Models
- Locator: 6 Discussion
- Evidence: 6 Discussion 作者报告 RT1 上 from-scratch 方法 Action Error Ratio 最佳但视频视觉精度略低，据此 weaser 在 action-consistency-priority 场景选 from-scratch。
- Quote: “In the RT1 domain we found that training an action-conditioned diffusion model from scratch resulted in the best Action Error Ratio, despite the videos being less visually accurate.”
- Authors: marc-rigter; tarun-gupta; agrin-hilmkil; et al.

### EA-DIT-2026-0022

- Claim: 视频 DiT 最优模型尺寸服从 Nopt∝C^a 幂律，且拟合精确度强烈依赖超参最优性：最优超参下 Nopt(C) 斜率偏差 3.57%，固定次优超参下升至 30.26%（工资估最优模型尺寸）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2411.17470](https://arxiv.org/abs/2411.17470) Towards Precise Scaling Laws for Video Diffusion Transformers
- Locator: page 6 (Eq 14) / page 8-9 (4.3.1, Eq 18, Fig 7)
- Evidence: 经验 Nopt=1.5787·C^0.4146（式 14）；预测 N̂opt=0.8705·C^0.4294（optimal hp，式 18）。对比图 7：optimal hp 下指数差绝对值 0.0148→3.57% 偏差，固定次优 hp 下 0.1581→30.26% 偏差。结论是有条件的：必须先取最优超参。
- Quote: “The use of suboptimal hyperparameters leads to an overestimation of the optimal model size”
- Authors: yuanyang-yin; yaqi-zhao; mingwu-zheng; et al.

### EA-DIT-2026-0067

- Claim: 视频世界模型的物理一致性输出对文本提示敏感：5.2 显示在 bouncing-ball 任务上加 negative prompt 后不同模型的 QFI 发生变化（如 Cosmos3-Super-I2V 降至最低 12.50），因此对这些模型的物理评测结果受提示表述条件控制、不可视为提示无关的固有属性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2608.05948](https://arxiv.org/abs/2608.05948) GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models
- Locator: 5.2 World Models
- Evidence: 5.2 的 bouncing-ball 分析显式访问 negative-prompt 条件下的最低 QFI 12.50（其无负prompt对应值更高），说明提示条件改变物理一致性结果；对应 negative-prompt 消融设置在 3.3.1 阐述。
- Quote: “Cosmos3-Super-I2V with the negative prompt obtains the lowest QFI of 12.50, but its inferred acceleration is only”
- Authors: shuai-wang; yaxin-feng; xuekun-jiang; et al.

### EA-DIT-2026-0002

- Claim: AVID 虽免参数但需访问预训练模型去噪过程中的中间预测（latent 情形含 encoder/decoder 输出），这削弱其 closed-source '黑盒' 可移植性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2410.12822](https://arxiv.org/abs/2410.12822) AVID: Adapting Video Diffusion Models to World Models
- Locator: 6 Discussion
- Evidence: 作者在 Discussion 明言需要 denoising 中间输出与 latent 的 encoder/decoder 输出，且许多 closed-source API 不提供。
- Quote: “AVID does not require access to pretrained model weights, but it does require access to intermediate predictions during denoising, including the outputs of the encoder and decoder in the case of latent diffusion.”
- Authors: marc-rigter; tarun-gupta; agrin-hilmkil; et al.

### EA-DIT-2026-0003

- Claim: AVID adapter 针对特定预训练模型定制，不能在不同预训练模型间复用之，限制了通用性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2410.12822](https://arxiv.org/abs/2410.12822) AVID: Adapting Video Diffusion Models to World Models
- Locator: 6 Discussion
- Evidence: 作者在 Discussion 的 Limitations 直接声明 adapter 专属某一预训练模型，不能与其他模型组合。
- Quote: “AVID adapters are tailored to a specific pretrained model and therefore cannot be composed with different models.”
- Authors: marc-rigter; tarun-gupta; agrin-hilmkil; et al.

### EA-DIT-2026-0009

- Claim: 对 DiT 视频生成，ID 泛化随数据/模型缩放近完美且误差下降，而 OOD 泛化误差至少高一个数量级且不随缩放改善，说明 naive 缩放不足以让视频模型发现物理定律。
- Stance: `limit` | Confidence: `direct`
- Paper: [2411.02385](https://arxiv.org/abs/2411.02385) How Far is Video Generation from World Model: A Physical Law Perspective
- Locator: 1 Introduction
- Evidence: 作者在 Introduction/3.2 报告：三任务 ID 近完美、OOD 误差高一个量级且随数据/模型缩放变化高度随机，DiT-XL 亦无改善。
- Quote: “Consistently, we observe that the model achieves a near-perfect ID generalization across all tasks. However, the OOD generalization error does not improve with increased data and model size, revealing the limitations of scaling video generation models in handling OOD data.”
- Authors: bingyi-kang; yang-yue; rui-lu; et al.

### EA-DIT-2026-0011

- Claim: 视频模型的 OOD 泛化更接近 '案例式/记忆式'（color>size>velocity>shape 优先层次）而非常见普适物理规则，易受 training set 中的 deceptive 样本偏置。
- Stance: `limit` | Confidence: `direct`
- Paper: [2411.02385](https://arxiv.org/abs/2411.02385) How Far is Video Generation from World Model: A Physical Law Perspective
- Locator: 5.2 Memorization or Generalization
- Evidence: 5.2 用 uniform-motion 定向/双向训练实验显示模型被 deceptive 增广误导（低速球反向），判断其为 memorization/case-based；Introduction 给出颜色>大小>速度>形状优先层次。
- Quote: “Rather than abstracting universal rules, the model appears to rely on memorization and case-based imitation for OOD generalization.”
- Authors: bingyi-kang; yang-yue; rui-lu; et al.

### EA-DIT-2026-0014

- Claim: 高加速下 AdaCache 可引入时间不一致（伪影、运动、颜色），引入 Motion Regularization（按运动分配计算）在几乎不变加速（4.7x→4.5x）下显著缓解该类伪影。
- Stance: `limit` | Confidence: `direct`
- Paper: [2411.02397](https://arxiv.org/abs/2411.02397) Adaptive Caching for Faster Video Generation with Diffusion Transformers
- Locator: 5.3 Ablation study
- Evidence: 5.3 报告 AdaCache 高加速（4.7x，720p-2s@100步）可引入 over-time 不一致（artifacts/motion/color），MoReg 通过按运动比例分配计算避免大部分，代价为加速降至 4.5x。
- Quote: “Despite giving a 4.7 speedup, AdaCache can also introduce some inconsistencies over time ( e.g . artifacts, motion, color).”
- Authors: kumara-kahatapitiya; haozhe-liu; sen-he; et al.

### EA-DIT-2026-0024

- Claim: 本文所有缩放律结论以验证损失（validation loss，代理指标）作为唯一评测，未使用 FVD 等标准视频生成质量指标；作者自称因缺少统一标准视频质量指标而放弃外部基准。
- Stance: `limit` | Confidence: `direct`
- Paper: [2411.17470](https://arxiv.org/abs/2411.17470) Towards Precise Scaling Laws for Video Diffusion Transformers
- Locator: page 3 (Setup-Evaluation) / page 9 (Section 6)
- Evidence: 作者明确 'We did not include external benchmarks due to challenges in consistently aligning multiple video benchmarks'，且 limitations 承认 'evaluation focused on validation loss due to the lack of a standard metric for video generation quality'。故本证据卡限定其评测视角。
- Quote: “validation loss serves as an effective proxy for performance”
- Authors: yuanyang-yin; yaqi-zhao; mingwu-zheng; et al.

### EA-DIT-2026-0025

- Claim: 该缩放律在低分辨率（17 帧 256x256）、小模型（0.017B-1.07B、单骨干 Cross-DiT、单数据集 Panda-70M）、常量学习率设定上测得；作者声明其可能不适用更高分辨率/更大模型，且未探索分辨率与帧率影响。
- Stance: `limit` | Confidence: `direct`
- Paper: [2411.17470](https://arxiv.org/abs/2411.17470) Towards Precise Scaling Laws for Video Diffusion Transformers
- Locator: page 9 (Section 6) / page 13 (Sec A.1-A.2)
- Evidence: 实验设置（Sec A.1-A.2）与作者 limitation 双证：'our study on low-resolution, smaller models may not directly apply to higher-resolution, larger models, requiring new fitting. Additionally, we did not explore how video resolution and frame rate impact the scaling law.'
- Quote: “our study on low-resolution, smaller models may not directly apply to higher-resolution, larger models, requiring new fitting”
- Authors: yuanyang-yin; yaqi-zhao; mingwu-zheng; et al.

### EA-DIT-2026-0032

- Claim: 受算力限制，Vid2World 只能以相对轻量的视频扩散模型作为基础模型，未能验证更大规模基础模型的收益。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.14357](https://arxiv.org/abs/2505.14357) Vid2World: Crafting Video Diffusion Models to Interactive World Models
- Locator: 6 Conclusion
- Evidence: 6 Conclusion 作者自述算力约束导致仅用轻量基础模型，并希望更大规模带来更好性能。
- Quote: “due to computational resource constraints, we are limited to employing a relatively lightweight video diffusion model as the base model.”
- Authors: siqiao-huang; jialong-wu; qixing-zhou; et al.

### EA-DIT-2026-0033

- Claim: 因基础模型参数较大与扩散的迭代解码，Vid2World 相对 teacher-forcing 世界模型推理不快，成其下游部署（含对具身/强化学习）的制约。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.14357](https://arxiv.org/abs/2505.14357) Vid2World: Crafting Video Diffusion Models to Interactive World Models
- Locator: A.7 Extended Discussion on Utilizing Vid2World for Downstream Tasks
- Evidence: Appendix A.7 作者承认是转移物理先验的第一步，但因大参数与迭代扩散推理不如 teacher-forcing 快，且因算力未做 RL 训练。
- Quote: “due to the large parameter size of the pretrained model and the iterative process in diffusion, the model does not enjoy fast inference speed”
- Authors: siqiao-huang; jialong-wu; qixing-zhou; et al.

### EA-DIT-2026-0037

- Claim: 来自 LLM 的长上下文扩展技术（YaRN）与 naive History Buffer 不能有效转移到视频生成，因当前视频模型 in-context learning 能力有限。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.21996](https://arxiv.org/abs/2505.21996) VRAG: Learning World Models for Interactive Video Generation
- Locator: 5 Conclusions and Discussions
- Evidence: 作者在 4.3 与 Conclusion 指出 YaRN/History Buffer 未带来世界一致性提升，归因于视频模型 in-context 局限，解释为重要负面结果。
- Quote: “context enhancement techniques from LLMs fail to transfer effectively to the video generation domain, even with shared transformer backbones, due to the inherent limitations of in-context learning capabilities for video models.”
- Authors: taiye-chen; xun-hu; zihan-ding; et al.

### EA-DIT-2026-0038

- Claim: VRAG 受 GPU 内存与计算成本限制，memory buffer 大小与训练序列长度受限，可能削弱长视界一致性与性能，并限制 edge/资源受限部署。
- Stance: `limit` | Confidence: `direct`
- Paper: [2505.21996](https://arxiv.org/abs/2505.21996) VRAG: Learning World Models for Interactive Video Generation
- Locator: 5 Conclusions and Discussions
- Evidence: 5 Conclusion 的 Limitations 自述 GPU 内存限制 buffer 与序列长度，检索增强计算成本高，限制资源受限部署。
- Quote: “GPU memory constraints severely restricted memory buffer size and training sequence length, potentially impacting long-horizon consistency and model performance.”
- Authors: taiye-chen; xun-hu; zihan-ding; et al.

### EA-DIT-2026-0052

- Claim: ACWMs 的 OoD 泛化主要由有效任务复杂度而非物理类别驱动；模型在低维、几何结构明确的任务上泛化良好，在高-DoF 运动学、接触丰富的可变形任务上大幅下降，倾向于捕获视觉外观统计而非内部化底层物理定律。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.08567](https://arxiv.org/abs/2605.08567) ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models
- Locator: 1 Introduction
- Evidence: 作者在贡献点与结论中显式声明该发现：OoD 泛化由有效任务复杂度而非物理类别驱动，模型捕获 visual statistics 而非 physical laws。
- Quote: “We find that OoD generalization is driven primarily by task complexity rather than physics category”
- Authors: haotian-xue; yipu-chen; liqian-ma; et al.

### EA-DIT-2026-0054

- Claim: 最大的 InD→OoD 恶化出现在高维运动学（Robot Arm）与接触丰富的可变形（Cloth Move）任务：两者 M-MSE 大幅上升，显示对分布偏移最脆弱的物理机制是复杂关节运动与 deformable contact。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.08567](https://arxiv.org/abs/2605.08567) ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models
- Locator: 5.1 Main Results
- Evidence: Table 1 与 Gauge 一致显示：Cloth Move InD M-MSE 63.68→OoD 93.67、Robot Arm 13.45→53.80，是八环境中退步最大者。
- Quote: “Table 1 reports ACWM-DiT-S on all eight ACWM-Phys environments at 100k training steps and 50 inference steps”
- Authors: haotian-xue; yipu-chen; liqian-ma; et al.

### EA-DIT-2026-0059

- Claim: SANA-WM 作者自承其仍 scale-limited、缺乏显式 3D 场景记忆，并在动态场景、罕见视角或更长回卷中漂移；且部署上全 softmax 注意力在 60s 时 OOM，需混合 GDN/softmax 才可行。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.15178](https://arxiv.org/abs/2605.15178) SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer
- Locator: 6. Conclusion & Limitations (page 10) & 5.4 Ablation (page 9)
- Evidence: 6. Conclusion 明确 limitation：scale-limited、无显式 3D 记忆、动态/罕见视角/更长回卷漂移；5.4/Fig 7 指 all-softmax 于 60s OOM，近常数状态依赖递推/线性变体。
- Quote: “SANA-WM remains scale-limited, lacks explicit 3D scene memory, and can drift in dynamic scenes, rare viewpoints, or longer rollouts.”
- Authors: haoyi-zhu; haozhe-liu; yuyang-zhao; et al.

### EA-DIT-2026-0066

- Claim: GAUGE 在 5 个刚体任务上评测的 6 个 image-to-video 视频世界模型，其生成轨迹可以符合预期物理定律的结构形式，却恢复出错误的物理参数（加速度、动量传递效率、振荡周期/时相），说明视频世界模型的'视觉/结构合理性'与其'定量物理/时序准确度'是分离的、可独立失败的能力。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.05948](https://arxiv.org/abs/2608.05948) GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models
- Locator: 5.2 World Models
- Evidence: 5.2 显式区分'满足物理定律结构形式'与'恢复参数'为不同能力：bouncing-ball 上取得最低 QFI 的模型其推断加速度仍远低于重力加速度；slope-slider 上不同材料最佳 QFI 由不同模型取得。
- Quote: “satisfying the structural form of a physical law and recovering its parameters are distinct capabilities”
- Authors: shuai-wang; yaxin-feng; xuekun-jiang; et al.

### EA-DIT-2026-0068

- Claim: GAUGE 对 Isaac Sim、Genesis、Newton 在 14 个任务上的评测表明没有统一的物理引擎在多机制上一律精准：刚体接触/滑动、动态布料、体积形变等领域各有互补优势，最大 sim-to-real 差异出现在 impulsive contact（即时接触）、高加速度布料运动和 3D 体积形变。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.05948](https://arxiv.org/abs/2608.05948) GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models
- Locator: 5 Results
- Evidence: 5 Results 概括性结论：无引擎在刚体/布料/软体三机制中占优，残差 sim-to-real 误差主要来自动态接触、高加速度布料运动与三维形变；各引擎具体分工在 Table 3 交叉呈现。
- Quote: “Overall, no engine dominates across rigid, textile, and volumetric regimes. The results instead reveal complementary solver strengths and identify dynamic contact, high-acceleration cloth motion, and three-dimensional deformation as the main sources of residual sim-to-real error.”
- Authors: shuai-wang; yaxin-feng; xuekun-jiang; et al.

### EA-DIT-2026-0012

- Claim: 视觉表示存在歧义（如像素级尺寸差、相对位置判定），使仅靠视频（视觉）的视频生成模型在细粒度物理建模上出错，暗示仅靠视觉可能不足以做完整物理建模。
- Stance: `gap` | Confidence: `direct`
- Paper: [2411.02385](https://arxiv.org/abs/2411.02385) How Far is Video Generation from World Model: A Physical Law Perspective
- Locator: 5.5 Is Video Sufficient for Complete Physics Modeling?
- Evidence: 5.5 报告视觉歧义导致 gap 判定与相对位置判定出错，作者据此自承视觉单独可能不足以完成精确物理建模。
- Quote: “These findings suggest that relying solely on visual representations, may be inadequate for accurate physics modeling.”
- Authors: bingyi-kang; yang-yue; rui-lu; et al.

### EA-DIT-2026-0028

- Claim: 综述把 '长视频生成的长程时空一致性' 列为核心未解决问题：跨数千帧/多场景时难以同时保持主体身份/物体属性/环境状态统一，现有模型缺乏动态建模与时空记忆，且高维联合分布建模带来计算/训练稳定/推理效率挑战；是领域公认缺口（gover）。
- Stance: `gap` | Confidence: `citation-supported`
- Paper: [2502.17863](https://arxiv.org/abs/2502.17863) A Survey: Spatiotemporal Consistency in Video Generation
- Locator: 8. Future Directions and Challenges
- Evidence: 8. Future Directions 将该缺口归因于领域发展（演进至长视频/更复杂方向），概述对长时间一致的建模/记忆/计算瓶颈，作为其综述对领域趋势的概括而非自身实验（position）。
- Quote: “Existing generation models typically struggle to effectively capture such long-range dependencies, lacking the dynamic modeling and spatiotemporal memory capabilities required for complex and extended-duration relationships.”
- Authors: zhiyu-yin; kehai-chen; xuefeng-bai; et al.

### EA-DIT-2026-0051

- Claim: RealWonder 的目标是生成'物理合理'而非'严格物理正确'的视频：3D 场景重建的深度误差会导致次优仿真与视频结果；作者明确严格物理正确性（所有动力学严格服从物理定律）仍为未来方向，视频模型还会补偿仿真器缺失/伪影的动态（如合成水波）。
- Stance: `gap` | Confidence: `direct`
- Paper: [2603.05449](https://arxiv.org/abs/2603.05449) RealWonder: Real-Time Physical Action-Conditioned Video Generation
- Locator: 5 Conclusion
- Evidence: 作者在 5 Conclusion 与附录 Physical Plausibility 段显式声明该限制，界定其物理保真目标与严格正确性的落差。
- Quote: “Reconstructing 3D scenes can be inaccurate due to errors in depth estimation, leading to suboptimal simulation and video results”
- Authors: wei-liu; ziyu-chen; zizhang-li; et al.

### EA-DIT-2026-0065

- Claim: 作者明确限制：该模型在精细液体动力学或高可变形物体操作上仍偶尔困难，且桥接 embodiment 需按平台（per-platform）微调，限制其跨机器人队可扩展性——这构成数字遥操作数据引擎在物态复杂度与多本体泛化上的边界。
- Stance: `gap` | Confidence: `direct`
- Paper: [2607.06558](https://arxiv.org/abs/2607.06558) RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation
- Locator: 6 Conclusion
- Evidence: 作者在 6 Conclusion 的 Limitation 段落显式声明这两条限制，指向更丰富数据与 cross-embodiment 基础世界模型（kinematic descriptors 条件）。
- Quote: “the model occasionally struggles with complex physical phenomena such as fine-grained liquid dynamics or the manipulation of highly deformable objects”
- Authors: haoyu-zhao; xingyue-zhao; hangyu-li; et al.

### EA-DIT-2026-0069

- Claim: GAUGE 的世界模型评测 track 被严格限制在可由二维图像轨迹评估的刚体任务；作者明确指出该表示不足以评估布料与体积软体的分布式形变、深度变化、自遮挡与 self-contact，需要可靠 3D 坐标后才能扩展到这些机制。
- Stance: `gap` | Confidence: `direct`
- Paper: [2608.05948](https://arxiv.org/abs/2608.05948) GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models
- Locator: 3.3.1 Generation and Track
- Evidence: 作者在 3.3.1 显式说明因当前 world models 在 3D 一致性与可变形动力学上仍薄弱，故只聚焦 rigid-body 场景评估 6 个模型；此限定构成评测覆盖的读者侧边界。
- Quote: “Because current world models still struggle with 3D consistency and deformable-object dynamics, we focus on rigid-body scenarios to evaluate six models”
- Authors: shuai-wang; yaxin-feng; xuekun-jiang; et al.

### EA-DIT-2026-0005

- Claim: ARLON 在 VBench 上相对基线 OpenSora-V1.2 带来 Dynamic Degree +5.6、Aesthetic +4.8、Overall Consistency +11.9、Scene Consistency +6.4，但 Subject/Bkgrd Consistency 略降（↓1.1/↓0.8），Motion Smoothness 微升 ↑0.7；动态上升伴随 motion smoothness 轻微降低的 trade-off。
- Stance: `support` | Confidence: `direct`
- Paper: [2410.20502](https://arxiv.org/abs/2410.20502) ARLON: Boosting Diffusion Transformers with Autoregressive Models for Long Video Generation
- Locator: 4.2 Results and Discussions
- Evidence: 4.2 的 Table 2 高亮行 'ARLON (Ours) 52.8 ↑5.6 61.0 ↑4.8 ... 54.4 ↑11.9 89.8 ↑6.4' 与 '↑'/'↓' 标注给出各维度相对 OpenSora-V1.2 的增量；4.2 文本明说 'increase in dynamism leads to a slight reduction in motion smoothness, we consider this trade-off acceptable'。
- Quote: “ARLON (Ours) 52.8 ↑5.6 61.0 ↑4.8 61.0 ↑0.1 93.4 ↓1.1 97.1 ↓0.8 98.9 ↑0.7 99.4 ↓0.1 25.3 ↑0.7 27.3 ↑0.2 54.4 ↑11.9 89.8 ↑6.4”
- Authors: zongyi-li; shujie-hu; shujie-liu; et al.

### EA-DIT-2026-0006

- Claim: DiT 训练阶段使用更粗粒度的 latent（不同于推理压缩率）会产生更噪的视觉 latent，从而增强 DiT 对 AR 推理误差的容忍，维持生成视频的一致性与质量；配合 uncertainty sampling 进一步模拟 AR 预测方差。
- Stance: `support` | Confidence: `direct`
- Paper: [2410.20502](https://arxiv.org/abs/2410.20502) ARLON: Boosting Diffusion Transformers with Autoregressive Models for Long Video Generation
- Locator: 4.3 Ablation Study
- Evidence: 4.3 文本直接说明 coarser latent 训练使 DiT 'tolerate the errors, thereby improving its robustness'，并提及 uncertainty sampling；Table 3 及其附图佐证一致性/质量保持。
- Quote: “which could make the DiT model tolerate the errors, thereby improving its robustness, and maintaining the consistency and qualities of the generated videos”
- Authors: zongyi-li; shujie-hu; shujie-liu; et al.

### EA-DIT-2026-0016

- Claim: 在 latent channel 数 = 16 时，IV-VAE（108M）在 Kinetics-600 与 ActivityNet 上的重建指标为 FVD 2.97/2.01、PSNR 39.02/42.61、LPIPS 0.02280/0.01968，为对比方法中最佳（尤其 PSNR 与 LPIPS）。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.06449](https://arxiv.org/abs/2411.06449) Improved Video VAE for Latent Video Diffusion Model
- Locator: 4.3 Performance
- Evidence: 4.3 Performance 的 Table 1 第 IV-VAE 行（108M, FCR 4*8*8, Chn 16）给出上述数值；同表对比 CogX-VAE(215M,Chn16) Kinetics FVD 3.17 / PSNR 38.38，IV-VAE 更优，且文中明言 'best results on a latent channel number of 16'。
- Quote: “IV-VAE 108M 4*8*8 16 2.97 39.02 0.9685 0.02280 2.01 42.61 0.9722 0.01968”
- Authors: pingyu-wu; kai-zhu; yu-liu; et al.

### EA-DIT-2026-0017

- Claim: IV-VAE 在 Kinetics-600 与 ActivityNet 上分别把重建 FVD 比 OD-VAE 降低 2.68 与 2.02，且参数量不到 OD-VAE 的一半。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.06449](https://arxiv.org/abs/2411.06449) Improved Video VAE for Latent Video Diffusion Model
- Locator: 4.3 Performance
- Evidence: 4.3 Performance 文本直接报告 'we outperform OD-VAE by 2.68 and 2.02 FVD in Kinetics-600 and ActivityNet, respectively and with less than half the number of parameters'；OD-VAE 239M vs IV-VAE 108M 印证参数结论。
- Quote: “we outperform OD-VAE by 2.68 and 2.02 FVD in Kinetics-600 and ActivityNet, respectively and with less than half the number of parameters.”
- Authors: pingyu-wu; kai-zhu; yu-liu; et al.

### EA-DIT-2026-0018

- Claim: 组因果卷积在参数不变下显著提升基线/KTC 结构的重建与生成性能；KTC 用更小参数（127M→104M）改善时间压缩学习；TMPE 仅 +3M 参数增强运动感知。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.06449](https://arxiv.org/abs/2411.06449) Improved Video VAE for Latent Video Diffusion Model
- Locator: 4.4 Ablation Study
- Evidence: 4.4 Ablation Study 明确报告组因果卷积在参数不变时 'substantially improve the performance'，KTC 以小参数改善时间压缩，TMPE 只增加 3M 参数。
- Quote: “the implementation of the proposed group causal convolution can substantially improve the performance on both baseline and KTC structure with the parameter count unchanged. The results indicate that the reconstruction quality can be effectively improved by allowing the frames in the same frame group to interact bidirectionally.”
- Authors: pingyu-wu; kai-zhu; yu-liu; et al.

### EA-DIT-2026-0039

- Claim: 在 AR 视频生成训练中，AR-DF 的 temporal tube masking 在 VBench-Overall Consistency (OC) 0.249 与 Imaging Quality (IQ) 0.559 上同时优于 random masks（0.232/0.424）与 diffusion forcing masks（0.241/0.540），GenEval 基本持平（0.591）。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.08801](https://arxiv.org/abs/2507.08801) Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective
- Locator: 4.2 Comparison with Other Methods on Visual Generation
- Evidence: 4.2 的 Table 5 给出各训练法在 GenEval/OC/IQ 数值，AR-DF OC/IQ 最高；且 4.3 文本解释 loss reweighting 无法解决信息泄漏、diffusion forcing 仅缓解、tube masking 最适合视频，故结论为该结果的实际支撑。
- Quote: “Diffusion forcing masks 0.590 0.241 0.540 AR-DF 0.591 0.249 0.559”
- Authors: hangjie-yuan; weihua-chen; jun-cen; et al.

### EA-DIT-2026-0040

- Claim: 掩码并行预测相对 next-token 预测显著降低视频推理时延：单 H20 上视频生成从 next-token 960.0s 降到 mask-pred-with-KV-cache 77.8s；MM-RoPE 相对 1D RoPE 时延几乎不变（77.8s vs 75.1s, 1B）。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.08801](https://arxiv.org/abs/2507.08801) Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective
- Locator: 4.3 Analysis and Ablation Studies
- Evidence: 4.3 的 Table 6 给出对应时延：Next-Token 960.0s → Mask-pred w/o KV cache 383.0s → Mask-pred w/ KV cache 77.8s，以及 1D/M/MM-RoPE 三档均约 75-78s。
- Quote: “Next-Token Pred Mask Pred w/o KV Cache Mask Pred w/ KV Cache Video ( ) 960.0s 383.0s 77.8s”
- Authors: hangjie-yuan; weihua-chen; jun-cen; et al.

### EA-DIT-2026-0041

- Claim: Lumos-1 (3.6B) 在 VBench-I2V 上优于 VideoCrafter-I2V 并与使用 100M 视频、10000 H100 训练的 COSMOS-Video2World 相当，体现 AR 路线用较少数据/算力达到竞争力的结果。
- Stance: `support` | Confidence: `direct`
- Paper: [2507.08801](https://arxiv.org/abs/2507.08801) Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective
- Locator: 4.2 Comparison with Other Methods on Visual Generation
- Evidence: 4.2 文本直接报告 Lumos-1 'outperforms the popular VideoCrafter-I2V model and is on par with the leading COSMOS-Video2World model'，并明示后者资源差异（100M 视频、10000 H100 训练）。
- Quote: “Lumos-1 outperforms the popular VideoCrafter-I2V model and is on par with the leading COSMOS-Video2World model, which uses substantially more data (100M 10M) and training resources (10000 H100s 48 H20s), demonstrating the promising performance of Lumos-1”
- Authors: hangjie-yuan; weihua-chen; jun-cen; et al.

### EA-DIT-2026-0007

- Claim: 语义注入的层位置与类型影响 AR-条件对齐：把 AR 码注入 DiT 最后 14 层提供的布局信息不足（视频近似 baseline），而注入前层（first 3/8/14）使布局更好对齐 AR 码；adaptive-norm 注入比 MLP adapter 与 ControlNet 更均衡（ControlNet 动态最高但主体一致性差）。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2410.20502](https://arxiv.org/abs/2410.20502) ARLON: Boosting Diffusion Transformers with Autoregressive Models for Long Video Generation
- Locator: 4.3 Ablation Study
- Evidence: 4.3 消融给出注入层数对比（Figure 6：last 14 近似 baseline、first 14 最佳）与注入架构（adaptive norm 'strikes a more balanced performance across all criteria' vs ControlNet 动态高但主体一致差）。
- Quote: “The adaptive norm method, however, strikes a more balanced performance across all criteria.”
- Authors: zongyi-li; shujie-hu; shujie-liu; et al.

### EA-DIT-2026-0008

- Claim: ARLON 基于 OpenSora-V1.2 基底可能封顶视频质量上限，2K 分辨率训练因 AR token 序列过长而不可行，且精细物理手部动作拟真仍难——这三者构成 AR+DiT 混合路线的可扩展性与质量边界。
- Stance: `limit` | Confidence: `direct`
- Paper: [2410.20502](https://arxiv.org/abs/2410.20502) ARLON: Boosting Diffusion Transformers with Autoregressive Models for Long Video Generation
- Locator: A.4 Limitations
- Evidence: A.4 Limitations 作者逐条自述：'ARLON is built upon OpenSora-V1.2, which potentially caps the upper limit'；2K 下 'sequence length of AR codes will become excessively long, making both training and inference impractical'；以及手部精细动作拟真难。
- Quote: “First, ARLON is built upon OpenSora-V1.2, which potentially caps the upper limit of video quality. Nonetheless, this limitation can be mitigated by substituting the DiT model with more advanced alternatives, such as CogVideoX-5B or MovieGen.”
- Authors: zongyi-li; shujie-hu; shujie-liu; et al.

### EA-DIT-2026-0019

- Claim: IV-VAE 整体仍基于 UNet 架构，缺乏全局感受野；作者指出应把 DiT 或 Mamba 引入 video VAE（作为未来工作），说明现有视频 VAE 架构与 DiT 主干之间仍有架构鸿沟。
- Stance: `limit` | Confidence: `direct`
- Paper: [2411.06449](https://arxiv.org/abs/2411.06449) Improved Video VAE for Latent Video Diffusion Model
- Locator: 5 Limitation and Conclusion.
- Evidence: 作者在 Limitation 直接声明架构仍基于 UNet、经典 UNet 无全局感受野，并建议 'introducing new architectures such as Dit or Mamba into video VAE in future work'；这是对 Video VAE 与 DiT 结合缺位的关键自述边界。
- Quote: “The overall architecture of the proposed method is still based on UNet following SD image VAE without exploring on other architectures. Video VAE faces more and unique difficulties compared to image VAE, e.g. , as the video resolution increases, the need for receptive field increases for video VAE.”
- Authors: pingyu-wu; kai-zhu; yu-liu; et al.

### EA-DIT-2026-0042

- Claim: Lumos-1 的训练语料（60M 图像 + 10M 视频）相对最近含十亿级样本的 foundation models 明显偏小，因此在需要精细人体动作或高度复杂场景动力学的场景下欠泛化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2507.08801](https://arxiv.org/abs/2507.08801) Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective
- Locator: F.2 Limitations and Future Work Discussions
- Evidence: 作者在 F.2 明确以 modest 形容 60M 图/10M 视频语料相较于含 billions 样本的 foundation models，并指出精细人体动作/复杂动力学欠泛化；这是自述尺度边界。
- Quote: “Most prominently, its training corpus (60 million images and 10 million videos) is modest compared with datasets used by recent foundation models [ 70 , 34 ] , which usually contain billions of samples. Consequently, Lumos-1 can under-generalize in scenarios that require fine-grained human actions or highly intricate scene dynamics.”
- Authors: hangjie-yuan; weihua-chen; jun-cen; et al.

### EA-DIT-2026-0043

- Claim: AR-DF 推理必须在推理阶段使用与训练一致的 partial-context masking，省略该 mask 会显著损害质量（可见伪影与闪烁）。
- Stance: `limit` | Confidence: `direct`
- Paper: [2507.08801](https://arxiv.org/abs/2507.08801) Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective
- Locator: 4.3 Analysis and Ablation Studies
- Evidence: 4.3 说明 AR-DF 'requires the same partial-context masking at inference as during training; omitting these masks severely harms quality'，fig.8(b) 显示 without 的伪影/闪烁。
- Quote: “AR - DF requires the same partial - context masking at inference as during training; omitting these masks severely harms quality.”
- Authors: hangjie-yuan; weihua-chen; jun-cen; et al.

## References

- `2410.12822` [AVID: Adapting Video Diffusion Models to World Models](https://arxiv.org/abs/2410.12822) (2024-10-01)
- `2410.20502` [ARLON: Boosting Diffusion Transformers with Autoregressive Models for Long Video Generation](https://arxiv.org/abs/2410.20502) (2024-10-27)
- `2411.02385` [How Far is Video Generation from World Model: A Physical Law Perspective](https://arxiv.org/abs/2411.02385) (2024-11-04)
- `2411.02397` [Adaptive Caching for Faster Video Generation with Diffusion Transformers](https://arxiv.org/abs/2411.02397) (2024-11-04)
- `2411.06449` [Improved Video VAE for Latent Video Diffusion Model](https://arxiv.org/abs/2411.06449) (2024-11-10)
- `2411.17470` [Towards Precise Scaling Laws for Video Diffusion Transformers](https://arxiv.org/abs/2411.17470) (2024-11-25)
- `2502.17863` [A Survey: Spatiotemporal Consistency in Video Generation](https://arxiv.org/abs/2502.17863) (2025-02-25)
- `2505.14357` [Vid2World: Crafting Video Diffusion Models to Interactive World Models](https://arxiv.org/abs/2505.14357) (2025-05-20)
- `2505.21996` [VRAG: Learning World Models for Interactive Video Generation](https://arxiv.org/abs/2505.21996) (2025-05-28)
- `2507.08801` [Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective](https://arxiv.org/abs/2507.08801) (2025-07-11)
- `2602.01801` [Fast Autoregressive Video Diffusion and World Models with Temporal Cache Compression and Sparse Attention](https://arxiv.org/abs/2602.01801) (2026-02-02)
- `2603.05449` [RealWonder: Real-Time Physical Action-Conditioned Video Generation](https://arxiv.org/abs/2603.05449) (2026-03-05)
- `2605.08567` [ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models](https://arxiv.org/abs/2605.08567) (2026-05-09)
- `2605.15178` [SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer](https://arxiv.org/abs/2605.15178) (2026-05-14)
- `2607.06558` [RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation](https://arxiv.org/abs/2607.06558) (2026-07-07)
- `2608.05948` [GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models](https://arxiv.org/abs/2608.05948) (2026-08-06)
