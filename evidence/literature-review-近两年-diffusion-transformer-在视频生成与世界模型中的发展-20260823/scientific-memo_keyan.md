# 视频 Diffusion Transformer 通向世界模型:规模化、转型与物理一致性的边界

## 研究边界

本备忘录回答的问题是:近两年(2024-08 至 2026-08)Diffusion Transformer(DiT)在视频生成与世界模型方向的**能力如何演进**?本文聚焦三条主线——(1) DiT 在视频生成上的规模化是否成立;(2) 视频扩散如何被改造成动作条件的交互式世界模型;(3) 世界模型前进路上最硬的约束到底是什么(物理一致性、评测、实时部署)。

证据覆盖 6 个维度(直接主题、邻接迁移、限制与反证、评测与验证、部署与运营、机制与接口),共 16 篇经过完整非 OCR 全文精读并逐一通过 claim-support 审计的论文,递送 69 条已验证证据事件。**本综述不能确立的**:不覆盖非视频主干(纯自回归/LLM 视觉)的世界模型完整谱系;不提供可迁移到生产级机器人部署的结论;对超大规模(十亿参数以上)DiT 的世界模型收益,现有证据只到轻量基座,属于条件推断而非实测。

## 中心判断

视频 DiT 在过去两年完成了一次**可验证的规模化跃升和一次尚未完成的"世界模型"转型**。一方面,实验证实视频 DiT 存在预测性的幂律缩放律(validation loss 随模型与数据可预测下降),并据此可反推最优超参;另一方面,把视频扩散改造成动作条件世界模型的两条路线(免标记蒸馏与显式记忆检索)都在小规模上显著提升了交互一致性与数据效率,但在**物理定量正确性**上集体失效——生成轨迹形态可以"看起来对",恢复出的加速度、动量、振荡周期却系统性错误。综述的核心张力是:**规模化让"视觉像"越来越容易,却几乎没有让"物理对"变得更容易。**

这一判断可以被反驳:如果未来出现大尺度(十亿参数以上)DiT 世界模型在物理一致性评测上超过轻量基座的证据,或出现内置显式动力学约束而不再依赖纯视觉分布的架构,则本综述关于"规模化不减物理误差"的边界需要修订。现有证据(见下文限制章节)均来自小模型与代理指标,不构成对该可能性的事前排除。

## 核心机制一:规模化成立了——但用的是什么度量

视频 DiT 确有缩放律。在一项以 Cross-DiT(17 帧 256×256、Panda-70M 数据)为设定的系统实证中,验证损失随模型尺寸与训练 token 呈可预测幂律,且能给出最优 batch 大小 Bopt=2.18×10^4·T^0.81·N^0.19 与学习率 ηopt 的幂律表达([Towards Precise Scaling Laws for Video Diffusion Transformers](https://arxiv.org/abs/2411.17470))。最优模型尺寸服从 Nopt∝C^a,外推到 1.07B/10B tokens 偏差约 0.03%。

但必须同时读它的三个限定。第一,这一切的度量都是 **validation loss**,不是 FVD 或任何标准视频质量指标——作者因领域缺少统一质量基准而放弃了外部评测。第二,设定是低分辨率、小模型(0.017B–1.07B)、恒定学习率、单一 backbone。第三,也是最微妙的一点:**缩放律拟合的精确度强烈依赖超参最优性**——最优超参下 Nopt(C) 斜率偏差 3.57%,固定次优超参下涨到 30.26%。这意味着一份"用 loss 代理标定的 scaling 曲线"在真实的生产质量评估中能兑现多少,仍是条件性的。

把缩放律落到实处还需要看它的"前道"是否跟得上。视频 DiT 的 latent 来自 video VAE,而现有 video VAE(KV-VAE,108M)虽在重建上做到 SOTA(FVD 2.97@Kinetics-600、PSNR 39.02,参数量不到同级 OD-VAE 一半),整体仍是 UNet 架构、缺全局感受野,作者把"把 DiT/Mamba 引入 video VAE"明确列为未来工作([Improved Video VAE for Latent Video Diffusion Model](https://arxiv.org/abs/2411.06449))。也就是说,**DiT 主干的缩放可能迟早被脆弱的 latent 前端卡住**——这是架构层面留给该方向的一个真实缝隙。

## 核心机制二:"世界模型化"的两条路线与它们的共同拐点

把视频扩散从"生成视频"变成"据动作预测未来"的世界模型,证据库里有两条清晰路线。

**免参数/免权重的适配路线。** AVID 用 learned-mask 组合预训练噪声输出与 adapter,在 Coinrun500k 上以 71M 拿到 no-weight-access 方法最优 Action Error Ratio 1.154,整体与需要权重的 ControlNet 相当([AVID: Adapting Video Diffusion Models to World Models](https://arxiv.org/abs/2410.12822))。这条路的吸引力是迁移成本低,但它仍要求访问预训练模型去噪中间的预测(latent 情形还要 encoder/decoder 输出),对 closed-source 黑盒并不真"免访问";且 adapter 是针对特定预训练模型的,不能跨模型复用。**"免"字是打折的。**

**因果化路线。** Vid2World 通过把视频扩散因果化加动作引导,把被动生成转成自回归、动作条件的世界模型,跨机器人、CS:GO、RECON 三域验证([Vid2World: Crafting Video Diffusion Models to Interactive World Models](https://arxiv.org/abs/2505.14357))。VRAG 则走显式记忆检索 + 全局状态(坐标/朝向)条件,在 1200 帧 compounding error 上以 SSIM 0.349 全面领先基线,在 RealEstate10K 上从 Diffusion Forcing 初始化仅微调 2 epochs 就把 SSIM 从 0.4436 拉到 0.9116([VRAG: Learning World Models for Interactive Video Generation](https://arxiv.org/abs/2505.21996))——这是相当强的数据效率证据。

两条路线的共同拐点出现在**物理定量正确性**。GAUGE 在 5 个刚体任务、6 个 image-to-video 世界模型上评测发现:模型生成的轨迹**可以符合预期物理定律的结构形式,却恢复出错误的具体参数**——加速度、动量传递效率、振荡周期与时相都偏(物理拟合指标 QFI 高,但加速度远低于 g)([GAUGE: A Measurement-Grounded Benchmark](https://arxiv.org/abs/2608.05948))。换句话说,这些模型在"形态上的物理合理性"与"数值上的物理正确性"之间出现了可独立失败的分裂。这一点与较早的物理定律评测([How Far is Video Generation from World Model: A Physical Law Perspective](https://arxiv.org/abs/2411.02385))结论互为印证:ID 内泛化近完美且随缩放提升,但 OOD 误差高一个数量级且不随缩放改善;模型倾向"案例式/记忆式"泛化,而非内化普适物理规则,且部分视觉歧义让纯视频不足以做细粒度物理建模。

## 由证据推导的分歧:较新输入也带回旧的不一致

值得注意的一个非平凡结果:当动作条件被进一步做"实时 + 物理桥接"时,物理合理性的代价变得更加明确。RealWonder 以物理仿真为中间表征,把连续 3D 动作翻译成光流 + 粗 RGB 条件视频生成器,绕过动作 tokenize 与 action-video 对采集的障碍,实现了 13.2 FPS@480×832、延迟 0.73s 的实时生成([RealWonder: Real-Time Physical Action-Conditioned Video Generation](https://arxiv.org/abs/2603.05449));但作者明确这条线追求的是"物理合理"而非"严格物理正确",深度误差会导致次优仿真。ACWM-Phys 的系统评测进一步给出机制性结论:动作条件世界模型的 OOD 泛化**主要由有效任务复杂度而非物理类别驱动**,在高自由度运动学与接触丰富的可变形任务上大幅恶化,模型更像在捕获视觉外观统计而非内化底层物理([ACWM-Phys](https://arxiv.org/abs/2605.08567))。

当把这条因果链推进到数据引擎层面,证据出现一个关键而不完整的闭环:RynnWorld-Teleop 用深度调制的骨骼动作表示 + 分布对齐注入训练了一个 40 FPS 的 egocentric 世界模型,纯由生成数据训练的策略能 zero-shot 迁移真机(Block Pushing 82.86%),生成数据还能一致放大真实数据([RynnWorld-Teleop](https://arxiv.org/abs/2607.06558))。这就把"世界模型能不能当数据引擎"的答案推进到了"能",但同时埋下了后门:它评估的物理一致性是感知级(FVD/成功率),而非动力学真值——**数据策略把生成的"像"当成"对"来学习,延续的仍是上文那条形态-数值裂缝。**

## 条件与分歧

- **缩放律的适用域被严格限定。** 低分辨率小模型 + validation loss 代理 + 恒定学习率,且未探索分辨率/帧率。任何将其结论外推到生产级、十亿参数或 action-conditioned 世界模型的说法都是条件推断。
- **物理一致性是"结构对、参数错"的分裂能力。** 这不是某一篇论文的缺陷,而是跨 GAUGE、physics 评测、ACWM-Phys、RealWonder 的证据共识——但这也说明"视觉合理性"本身仍是可衡量的进步,不应被全盘否定。
- **动作条件的优劣依赖任务维度。** cross-attention 注入动作 token 在高维动作(Robot Arm MSE 0.691 vs AdaLN 1.434)显著更优,低维简单任务反而不如 AdaLN——没有普适最优的注入机制。
- **长程一致性仍缺公认解。** 综述把长程时空一致性列为核心未解决问题,LLM 式长上下文扩展(YaRN)与朴素历史缓冲在视频上不仅无效还可能有损;真实依赖显式记忆/状态或自回归缓存,且这类机制普遍受显存上限约束。
- **评测本身是提示敏感的。** 物理一致性输出对文本提示敏感(加 negative prompt 后物理拟合指标明显变化),这提示现有物理评测不能被视为提示无关的固有属性。

## 研究空白与下一步

把"本综述覆盖缺口"与"文献自身宣布的缺口"分开。

**文献宣布的缺口**(明确写在论文里):GAUGE 的世界模型评测 track 只覆盖可用二维图像轨迹评估的刚体任务,布料/体积软体的分布式形变、深度变化、自我遮挡需要可靠 3D 坐标后才能评估;SANA-WM 自承缺乏显式 3D 场景记忆、在动态/罕见/长场景漂移,全 softmax 注意力 60s 即 OOM。

**本综述覆盖缺口**(下一步待补):(1) 十亿参数以上 DiT 世界模型在物理一致性评测上的实证; (2) 把视频世界模型的感知级评估与真值物理评测在**同一**动作条件设定下对齐的实验(当前两者几乎总是分属不同测评体系); (3) 实时(action-conditioned、40FPS 级)对物理正确性的代价，现有实时系统明确放弃了严格物理正确性,缺一个量化的"实时×物理正确"权衡曲线。

## 结论

对研究者的判断影响可归结为三点:第一,DiT 视频生成已有可标定的缩放律,但当前标定依赖 loss 代理,决策时应意识到这一点;第二,世界模型化的两条路线(免适配、因果化)在小规模上都成立且数据效率可观,但它们的共同软肋是物理定量正确性——这正是真正的瓶颈;第三,把"视觉合理"当成"物理正确"来用是数据引擎路线的隐患,评估世界模型时必须在感知指标之外加上真值物理指标。**规模化让视频"越来越像",物理正确性则需要另一类约束——这应当成为下一阶段的评测与架构设计焦点。**

## References

1. [Towards Precise Scaling Laws for Video Diffusion Transformers](https://arxiv.org/abs/2411.17470)
2. [Improved Video VAE for Latent Video Diffusion Model](https://arxiv.org/abs/2411.06449)
3. [AVID: Adapting Video Diffusion Models to World Models](https://arxiv.org/abs/2410.12822)
4. [Vid2World: Crafting Video Diffusion Models to Interactive World Models](https://arxiv.org/abs/2505.14357)
5. [VRAG: Learning World Models for Interactive Video Generation](https://arxiv.org/abs/2505.21996)
6. [GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models](https://arxiv.org/abs/2608.05948)
7. [How Far is Video Generation from World Model: A Physical Law Perspective](https://arxiv.org/abs/2411.02385)
8. [ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models](https://arxiv.org/abs/2605.08567)
9. [RealWonder: Real-Time Physical Action-Conditioned Video Generation](https://arxiv.org/abs/2603.05449)
10. [RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation](https://arxiv.org/abs/2607.06558)
11. [SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer](https://arxiv.org/abs/2605.15178)
12. [A Survey: Spatiotemporal Consistency in Video Generation](https://arxiv.org/abs/2502.17863)
13. [ARLON: Boosting Diffusion Transformers with Autoregressive Models for Long Video Generation](https://arxiv.org/abs/2410.20502)
14. [Lumos-1: On Autoregressive Video Generation with Discrete Diffusion from a Unified Model Perspective](https://arxiv.org/abs/2507.08801)
15. [Adaptive Caching for Faster Video Generation with Diffusion Transformers](https://arxiv.org/abs/2411.02397)
16. [Fast Autoregressive Video Diffusion and World Models with Temporal Cache Compression and Sparse Attention](https://arxiv.org/abs/2602.01801)