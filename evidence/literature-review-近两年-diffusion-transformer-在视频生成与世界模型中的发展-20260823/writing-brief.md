# Writing Brief: 近两年（2024-08至2026-08）Diffusion Transformer 在视频生成与世界模型中的发展

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近两年（2024-08至2026-08）Diffusion Transformer 在视频生成与世界模型中的发展
- Time range: 2024-08 至 2026-08
- Knowledge IDs: unlisted
- Review mode: scoping
- Paper-level sources: 16 / 15 floor (not a cap)
- Coverage and saturation gate: blocked
- Writing readiness: preliminary
- Unresolved checks: saturation
- Accepted events: 69

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-4D`: 在 Coinrun500k 上，AVID（71M）在不访问预训练权重的所有方法中获得最佳 Action Error Ratio（1.154），整体表现与需要权重的 ControlNet 相当。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0001](evidence-appendix.md#ea-dit-2026-0001)) ⟷ AVID 虽免参数但需访问预训练模型去噪过程中的中间预测（latent 情形含 encoder/decoder 输出），这削弱其 closed-source '黑盒' 可移植性。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0002](evidence-appendix.md#ea-dit-2026-0002))
- `EA-4D`: 组合泛化随 training 覆盖更多模板/物体组合而改善：DiT-XL 的 out-of-template 人工 abnormal 率从 6 模板的 67% 降至 60 模板的 10%；DiT-B（60 模板）为 24%，说明组合多样性... ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0010](evidence-appendix.md#ea-dit-2026-0010)) ⟷ AVID adapter 针对特定预训练模型定制，不能在不同预训练模型间复用之，限制了通用性。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0003](evidence-appendix.md#ea-dit-2026-0003))
- `EA-4D`: 训练无关缓存 AdaCache-fast 在 Open-Sora 文生视频基线上取得最高 2.24x 推理加速（VBench 79.48 vs 基线 79.22，几乎无质量下降），优于 T-GATE 1.10x、PAB 1.34x 等既有... ([2411.02397](https://arxiv.org/abs/2411.02397) / [EA-DIT-2026-0013](evidence-appendix.md#ea-dit-2026-0013)) ⟷ 对 DiT 视频生成，ID 泛化随数据/模型缩放近完美且误差下降，而 OOD 泛化误差至少高一个数量级且不随缩放改善，说明 naive 缩放不足以让视频模型发现物理定律。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0009](evidence-appendix.md#ea-dit-2026-0009))
- `EA-4D`: 用户 A/B 研究中，AdaCache 相对 PAB 在相近加速下获得更高偏好率（70%），且与未加速基线不可区分超过一半时间（41%）；运动正则化变体更受偏好（25% vs 14%）。 ([2411.02397](https://arxiv.org/abs/2411.02397) / [EA-DIT-2026-0015](evidence-appendix.md#ea-dit-2026-0015)) ⟷ 视频模型的 OOD 泛化更接近 '案例式/记忆式'（color>size>velocity>shape 优先层次）而非常见普适物理规则，易受 training set 中的 deceptive 样本偏置。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0011](evidence-appendix.md#ea-dit-2026-0011))
- `EA-4D`: 视频 DiT 被系统实证确认存在缩放律：验证损失随模型尺寸与训练 token 呈可预测幂律，抽取优化条件下能与 LLM 式缩放律拟合对齐。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0020](evidence-appendix.md#ea-dit-2026-0020)) ⟷ 高加速下 AdaCache 可引入时间不一致（伪影、运动、颜色），引入 Motion Regularization（按运动分配计算）在几乎不变加速（4.7x→4.5x）下显著缓解该类伪影。 ([2411.02397](https://arxiv.org/abs/2411.02397) / [EA-DIT-2026-0014](evidence-appendix.md#ea-dit-2026-0014))
- `EA-4D`: 视频 DiT 最优超参（batch size 与 learning rate）可被幂律预测：Bopt=2.1797e4·T^0.8080·N^0.1906、ηopt=0.0002·T^-0.0453·N^-0.1619；较 LLM，视频模... ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0021](evidence-appendix.md#ea-dit-2026-0021)) ⟷ 本文所有缩放律结论以验证损失（validation loss，代理指标）作为唯一评测，未使用 FVD 等标准视频生成质量指标；作者自称因缺少统一标准视频质量指标而放弃外部基准。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0024](evidence-appendix.md#ea-dit-2026-0024))
- `EA-4D`: 性能缩放通式 L(T,N)=(Tc/T)^αT+(Nc/N)^αN+L∞ 可在最优超参下预测任意模型尺寸与 compute 的 validation loss，外推验证偏差约 0.03%（1.07B/10B tokens）与 0.15%（... ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0023](evidence-appendix.md#ea-dit-2026-0023)) ⟷ 该缩放律在低分辨率（17 帧 256x256）、小模型（0.017B-1.07B、单骨干 Cross-DiT、单数据集 Panda-70M）、常量学习率设定上测得；作者声明其可能不适用更高分辨率/更大模型，且未探索分辨率与帧率影响。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0025](evidence-appendix.md#ea-dit-2026-0025))
- `EA-4D`: 综述以 '时空分布序列采样' 界定：空间一致性=分布内任意两点语义/视觉属性兼容（主体身份、场景布局、光照风格、颜色纹理、静态语义等），时间一致性=相邻样本平滑演化（表1 再细分为运动平滑/时序动态/闪烁抑制/动态语义）；时间一致性本质是... ([2502.17863](https://arxiv.org/abs/2502.17863) / [EA-DIT-2026-0026](evidence-appendix.md#ea-dit-2026-0026)) ⟷ 受算力限制，Vid2World 只能以相对轻量的视频扩散模型作为基础模型，未能验证更大规模基础模型的收益。 ([2505.14357](https://arxiv.org/abs/2505.14357) / [EA-DIT-2026-0032](evidence-appendix.md#ea-dit-2026-0032))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-4D (56 events)
- [`support`] 在 Coinrun500k 上，AVID（71M）在不访问预训练权重的所有方法中获得最佳 Action Error Ratio（1.154），整体表现与需要权重的 ControlNet 相当。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0001](evidence-appendix.md#ea-dit-2026-0001))
- [`support`] 组合泛化随 training 覆盖更多模板/物体组合而改善：DiT-XL 的 out-of-template 人工 abnormal 率从 6 模板的 67% 降至 60 模板的 10%；DiT-B（60 模板）为 24%，说明组合多样性与模型容量均关键。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0010](evidence-appendix.md#ea-dit-2026-0010))
- [`support`] 训练无关缓存 AdaCache-fast 在 Open-Sora 文生视频基线上取得最高 2.24x 推理加速（VBench 79.48 vs 基线 79.22，几乎无质量下降），优于 T-GATE 1.10x、PAB 1.34x 等既有训练无关方法。 ([2411.02397](https://arxiv.org/abs/2411.02397) / [EA-DIT-2026-0013](evidence-appendix.md#ea-dit-2026-0013))
- [`support`] 用户 A/B 研究中，AdaCache 相对 PAB 在相近加速下获得更高偏好率（70%），且与未加速基线不可区分超过一半时间（41%）；运动正则化变体更受偏好（25% vs 14%）。 ([2411.02397](https://arxiv.org/abs/2411.02397) / [EA-DIT-2026-0015](evidence-appendix.md#ea-dit-2026-0015))
- [`support`] 视频 DiT 被系统实证确认存在缩放律：验证损失随模型尺寸与训练 token 呈可预测幂律，抽取优化条件下能与 LLM 式缩放律拟合对齐。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0020](evidence-appendix.md#ea-dit-2026-0020))
- [`support`] 视频 DiT 最优超参（batch size 与 learning rate）可被幂律预测：Bopt=2.1797e4·T^0.8080·N^0.1906、ηopt=0.0002·T^-0.0453·N^-0.1619；较 LLM，视频模型对 batch/lr 更敏感。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0021](evidence-appendix.md#ea-dit-2026-0021))
- [`support`] 性能缩放通式 L(T,N)=(Tc/T)^αT+(Nc/N)^αN+L∞ 可在最优超参下预测任意模型尺寸与 compute 的 validation loss，外推验证偏差约 0.03%（1.07B/10B tokens）与 0.15%（0.72B/140B tokens）。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0023](evidence-appendix.md#ea-dit-2026-0023))
- [`support`] 综述以 '时空分布序列采样' 界定：空间一致性=分布内任意两点语义/视觉属性兼容（主体身份、场景布局、光照风格、颜色纹理、静态语义等），时间一致性=相邻样本平滑演化（表1 再细分为运动平滑/时序动态/闪烁抑制/动态语义）；时间一致性本质是序列生成的转移概率建模问题。 ([2502.17863](https://arxiv.org/abs/2502.17863) / [EA-DIT-2026-0026](evidence-appendix.md#ea-dit-2026-0026))
- [`support`] 综述将视频生成评测指标分为三大类：帧质量评估（像素/语义级，如 PSNR/SSIM/IS/FID/Aesthetic）、视频平滑评估（时间一致性/运动合理）、整体视频评估；并指出时间动力学类基准（ChronoMagic-Bench/T2VBench、MiraBench/DEVIL）专门用于评估时序一致性/逻辑与运动自然度。 ([2502.17863](https://arxiv.org/abs/2502.17863) / [EA-DIT-2026-0027](evidence-appendix.md#ea-dit-2026-0027))
- [`support`] Vid2World 通过 video diffusion causalization 与 causal action guidance 两个机制，把被动视频扩散模型转成支持自回归、动作条件生成的交互式世界模型。 ([2505.14357](https://arxiv.org/abs/2505.14357) / [EA-DIT-2026-0029](evidence-appendix.md#ea-dit-2026-0029))
- [`support`] 消融显示对 Extrapolative 与 Masked 权重迁移，强制 action guidance 都带来更好性能（相对训练/推理中从不丢弃动作的对应版本）。 ([2505.14357](https://arxiv.org/abs/2505.14357) / [EA-DIT-2026-0030](evidence-appendix.md#ea-dit-2026-0030))
- [`support`] Masked 与 Extrapolative 权重迁移都优于 Shift 权重迁移，且 Extrapolative 略优于 Masked，二者共同支撑 Vid2World 的性能。 ([2505.14357](https://arxiv.org/abs/2505.14357) / [EA-DIT-2026-0031](evidence-appendix.md#ea-dit-2026-0031))
- [`support`] 在 300 帧长视频 world coherence 评估上，VRAG 以 SSIM 0.506 优于所有对比基线（DF-window20 0.466、YaRN 0.462、History Buffer 0.459、Frame Pack 0.421）。 ([2505.21996](https://arxiv.org/abs/2505.21996) / [EA-DIT-2026-0034](evidence-appendix.md#ea-dit-2026-0034))
- [`support`] 在 1200 帧 compounding error 评估中，VRAG 以平均 SSIM 0.349 优于所有基线（History Buffer 0.188、DF-window20 0.321、YaRN 0.316）。 ([2505.21996](https://arxiv.org/abs/2505.21996) / [EA-DIT-2026-0035](evidence-appendix.md#ea-dit-2026-0035))
- [`support`] 在真实世界数据集 RealEstate10K 上从 Diffusion Forcing Transformer (DFoT) 初始化仅 finetune 2 epochs（约 10% 原始训练量），VRAG 的记忆能力显著超 DFoT（SSIM 0.9116 vs 0.4436，FVD 221 vs 337.5）。 ([2505.21996](https://arxiv.org/abs/2505.21996) / [EA-DIT-2026-0036](evidence-appendix.md#ea-dit-2026-0036))
- [`support`] 统一训练无关框架（TempCache+AnnCA+AnnSA，FAST-AR）在 RollingForcing 长回卷上达最高 10.8x（LSH 10.7x）端到端加速并保持 FA3 级质量，而最优基线组合 FlowCache+RadialAttn 仅 4.4x 且质量崩坏。 ([2602.01801](https://arxiv.org/abs/2602.01801) / [EA-DIT-2026-0044](evidence-appendix.md#ea-dit-2026-0044))
- [`support`] TempCache（时间对应 KV 合并）把注意力 KV 缓存压缩到 ~16% 最小密度而保持 90-91% 注意力召回并匹配 dense 质量（VBench 84.1），而既有训练无关缓存 TeaCache/FlowCache 仅提供 1.1-1.3x 加速。 ([2602.01801](https://arxiv.org/abs/2602.01801) / [EA-DIT-2026-0045](evidence-appendix.md#ea-dit-2026-0045))
- [`support`] 随回卷长度增长，dense 基线 FA3 吞吐持续下滑、峰值显存随 KV cache 扩张上升，而 FAST-AR 在 3000 帧回卷中维持近常数 FPS 且显存平坦（有界 cache）；该趋势在世界模型（LongVie2）上同样被观察到。 ([2602.01801](https://arxiv.org/abs/2602.01801) / [EA-DIT-2026-0046](evidence-appendix.md#ea-dit-2026-0046))
- [`support`] RealWonder 以物理仿真为中间表征，把连续的 3D 物理动作翻译为 optical flow 和 coarse RGB 预览来条件化视频生成器，从而绕过了'对连续无界动作 tokenize'与'收集 action-video 训练对'两大障碍（训练仅需 2D flow-video 对）。 ([2603.05449](https://arxiv.org/abs/2603.05449) / [EA-DIT-2026-0047](evidence-appendix.md#ea-dit-2026-0047))
- [`support`] RealWonder 实现实时流式 action-conditioned 视频生成：13.2 FPS @480x832（单 GPU）、动作到结果延迟 0.73s，相较 PhysGaussian（4.84s 延迟/0.207 FPS）与不可流式的视频生成基线（<0.3 FPS）显著更快。 ([2603.05449](https://arxiv.org/abs/2603.05449) / [EA-DIT-2026-0048](evidence-appendix.md#ea-dit-2026-0048))
- [`support`] 在自建 30 图评测集上，RealWonder 相对 PhysGaussian/CogVideoX-I2V/Tora 在所有指标上取得最佳或次佳，并在 2AFC 用户研究中被显著更偏好（尤其 Action Following 与 Physical Plausibility 维度），说明物理仿真桥条件下视频模型优于纯物理基或纯 2D 条件基线。 ([2603.05449](https://arxiv.org/abs/2603.05449) / [EA-DIT-2026-0049](evidence-appendix.md#ea-dit-2026-0049))
- [`support`] RealWonder 通过 Distribution Matching Distillation + Self-Forcing 把 flow 条件的多步教师蒸馏为 4 步 causal student，把控制直接注入起始噪声，从而支持实时流式；并用 KV cache（置于 RoPE 前）+ attention sink 缓解长视界漂移。 ([2603.05449](https://arxiv.org/abs/2603.05449) / [EA-DIT-2026-0050](evidence-appendix.md#ea-dit-2026-0050))
- [`support`] ACWM-DiT-S（latent bidirectional 视频 DiT + AdaLN 动作条件）在所有四类物理交互上取得强 InD 预测：简单、重复动力学近完美（Push Rope、Reacher），而大形变/大前景运动任务（Cloth Move、Stack Cube）InD 误差最高。 ([2605.08567](https://arxiv.org/abs/2605.08567) / [EA-DIT-2026-0053](evidence-appendix.md#ea-dit-2026-0053))
- [`support`] action-conditioning 机制消融表明：cross-attention 注入动作 token 在动作高维（Robot Arm）时显著优于 AdaLN（InD MSE 0.691 vs 1.434），而在低维任务（Push Cube/Push Rope）无益甚至略差；时间感知的 causal video VAE 全场景优于逐帧独立的 image VAE。 ([2605.08567](https://arxiv.org/abs/2605.08567) / [EA-DIT-2026-0055](evidence-appendix.md#ea-dit-2026-0055))
- [`support`] ACWM-Phys 为 8 个环境设计受控、物理相关的 InD/OoD 分布偏移（未折叠的物体数量、workspace 范围、rope/cloth 尺寸、粒子数量、水位、goal 区域），作为 agentic 物理世界模型的评测方法学贡献。 ([2605.08567](https://arxiv.org/abs/2605.08567) / [EA-DIT-2026-0056](evidence-appendix.md#ea-dit-2026-0056))
- [`support`] SANA-WM 在作者自建 1 分钟基准的两轨迹 split 上取得更强 action-following：refined 输出 RotErr 4.50°/8.34°、CamMC 1.41/1.44，优于 Infinite-World/LingBot-World/HY-WorldPlay/Matrix-Game 3.0 等基线。 ([2605.15178](https://arxiv.org/abs/2605.15178) / [EA-DIT-2026-0057](evidence-appendix.md#ea-dit-2026-0057))
- [`support`] SANA-WM 以 51.1GB/24.1 视频-时（8×H100）完成单 GPU/分钟级 720p 推理，refiner 全流程 74.7GB/22.0 视频-时仍比最快的 480p 基线快；distilled+NVFP4 变体在单 RTX 5090 上 34s 生成 60s 720p clip（宣称 36x 吞吐）。 ([2605.15178](https://arxiv.org/abs/2605.15178) / [EA-DIT-2026-0058](evidence-appendix.md#ea-dit-2026-0058))
- [`support`] RynnWorld-Teleop 用深度调制渲染的 21 关节手部骨骼动作表示（颜色与关节/骨骼直径按相机空间深度动态缩放）来编码精确手-物交互所需的 3D 结构线索，并投影为与目标视频 latent 时空对齐的控制 latent。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DIT-2026-0060](evidence-appendix.md#ea-dit-2026-0060))
- [`support`] RynnWorld-Teleop 通过分布对齐的 additive patch-embedding 把骨骼控制 latent 注入视频 DiT，并以零初始化的 gating scalar 保持与预训练视频流的统计兼容，从而在纳入动作条件时不破坏 base DiT 的生成先验。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DIT-2026-0061](evidence-appendix.md#ea-dit-2026-0061))
- [`support`] 蒸馏因果学生模型实现实时单趟生成：4-step 条件流匹配，在单 H100 上 40.0 FPS（其中 Causal DiT 去噪约占 72% 延迟），明显超出现有 action-conditioned 世界模型数 Hz 的帧率，从而弥合传感-执行间隙。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DIT-2026-0062](evidence-appendix.md#ea-dit-2026-0062))
- [`support`] RynnWorld-Teleop 在 EgoDex-Test 与 Robotic-Test 上显著优于通用 I2V（Wan/CogVideoX）与 action-conditioned 世界模型（InterDyn/CosHand/Mask2IV）：如 FVD 585 vs vanilla SFT 1223、PSNR 26.08 vs 20.93，说明自定义深度骨骼条件 + 分布对齐优于简单 SF... ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DIT-2026-0063](evidence-appendix.md#ea-dit-2026-0063))
- [`support`] 以 RynnWorld-Teleop 生成数据做数据引擎：纯由 300 生成 episode（无真实数据）训练的策略可 zero-shot 迁移到真机（Block Pushing 82.86%、Bimanual Lifting 77.14%），且用 300 生成数据增强 300 真实 episode 在几乎所有任务一致提升成功率（如 Lid Placement 某策略 +20%）。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DIT-2026-0064](evidence-appendix.md#ea-dit-2026-0064))
- [`conditional`] 在 RT1 上，从零训练的 action-conditioned diffusion 得到最佳 Action Error Ratio（尽管视觉质量更低），说明动作一致性优先时 from-scratch 也可取胜。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0004](evidence-appendix.md#ea-dit-2026-0004))
- [`conditional`] 视频 DiT 最优模型尺寸服从 Nopt∝C^a 幂律，且拟合精确度强烈依赖超参最优性：最优超参下 Nopt(C) 斜率偏差 3.57%，固定次优超参下升至 30.26%（工资估最优模型尺寸）。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0022](evidence-appendix.md#ea-dit-2026-0022))
- [`conditional`] 视频世界模型的物理一致性输出对文本提示敏感：5.2 显示在 bouncing-ball 任务上加 negative prompt 后不同模型的 QFI 发生变化（如 Cosmos3-Super-I2V 降至最低 12.50），因此对这些模型的物理评测结果受提示表述条件控制、不可视为提示无关的固有属性。 ([2608.05948](https://arxiv.org/abs/2608.05948) / [EA-DIT-2026-0067](evidence-appendix.md#ea-dit-2026-0067))
- [`limit`] AVID 虽免参数但需访问预训练模型去噪过程中的中间预测（latent 情形含 encoder/decoder 输出），这削弱其 closed-source '黑盒' 可移植性。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0002](evidence-appendix.md#ea-dit-2026-0002))
- [`limit`] AVID adapter 针对特定预训练模型定制，不能在不同预训练模型间复用之，限制了通用性。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0003](evidence-appendix.md#ea-dit-2026-0003))
- [`limit`] 对 DiT 视频生成，ID 泛化随数据/模型缩放近完美且误差下降，而 OOD 泛化误差至少高一个数量级且不随缩放改善，说明 naive 缩放不足以让视频模型发现物理定律。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0009](evidence-appendix.md#ea-dit-2026-0009))
- [`limit`] 视频模型的 OOD 泛化更接近 '案例式/记忆式'（color>size>velocity>shape 优先层次）而非常见普适物理规则，易受 training set 中的 deceptive 样本偏置。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0011](evidence-appendix.md#ea-dit-2026-0011))
- [`limit`] 高加速下 AdaCache 可引入时间不一致（伪影、运动、颜色），引入 Motion Regularization（按运动分配计算）在几乎不变加速（4.7x→4.5x）下显著缓解该类伪影。 ([2411.02397](https://arxiv.org/abs/2411.02397) / [EA-DIT-2026-0014](evidence-appendix.md#ea-dit-2026-0014))
- [`limit`] 本文所有缩放律结论以验证损失（validation loss，代理指标）作为唯一评测，未使用 FVD 等标准视频生成质量指标；作者自称因缺少统一标准视频质量指标而放弃外部基准。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0024](evidence-appendix.md#ea-dit-2026-0024))
- [`limit`] 该缩放律在低分辨率（17 帧 256x256）、小模型（0.017B-1.07B、单骨干 Cross-DiT、单数据集 Panda-70M）、常量学习率设定上测得；作者声明其可能不适用更高分辨率/更大模型，且未探索分辨率与帧率影响。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0025](evidence-appendix.md#ea-dit-2026-0025))
- [`limit`] 受算力限制，Vid2World 只能以相对轻量的视频扩散模型作为基础模型，未能验证更大规模基础模型的收益。 ([2505.14357](https://arxiv.org/abs/2505.14357) / [EA-DIT-2026-0032](evidence-appendix.md#ea-dit-2026-0032))
- [`limit`] 因基础模型参数较大与扩散的迭代解码，Vid2World 相对 teacher-forcing 世界模型推理不快，成其下游部署（含对具身/强化学习）的制约。 ([2505.14357](https://arxiv.org/abs/2505.14357) / [EA-DIT-2026-0033](evidence-appendix.md#ea-dit-2026-0033))
- [`limit`] 来自 LLM 的长上下文扩展技术（YaRN）与 naive History Buffer 不能有效转移到视频生成，因当前视频模型 in-context learning 能力有限。 ([2505.21996](https://arxiv.org/abs/2505.21996) / [EA-DIT-2026-0037](evidence-appendix.md#ea-dit-2026-0037))
- [`limit`] VRAG 受 GPU 内存与计算成本限制，memory buffer 大小与训练序列长度受限，可能削弱长视界一致性与性能，并限制 edge/资源受限部署。 ([2505.21996](https://arxiv.org/abs/2505.21996) / [EA-DIT-2026-0038](evidence-appendix.md#ea-dit-2026-0038))
- [`limit`] ACWMs 的 OoD 泛化主要由有效任务复杂度而非物理类别驱动；模型在低维、几何结构明确的任务上泛化良好，在高-DoF 运动学、接触丰富的可变形任务上大幅下降，倾向于捕获视觉外观统计而非内部化底层物理定律。 ([2605.08567](https://arxiv.org/abs/2605.08567) / [EA-DIT-2026-0052](evidence-appendix.md#ea-dit-2026-0052))
- [`limit`] 最大的 InD→OoD 恶化出现在高维运动学（Robot Arm）与接触丰富的可变形（Cloth Move）任务：两者 M-MSE 大幅上升，显示对分布偏移最脆弱的物理机制是复杂关节运动与 deformable contact。 ([2605.08567](https://arxiv.org/abs/2605.08567) / [EA-DIT-2026-0054](evidence-appendix.md#ea-dit-2026-0054))
- [`limit`] SANA-WM 作者自承其仍 scale-limited、缺乏显式 3D 场景记忆，并在动态场景、罕见视角或更长回卷中漂移；且部署上全 softmax 注意力在 60s 时 OOM，需混合 GDN/softmax 才可行。 ([2605.15178](https://arxiv.org/abs/2605.15178) / [EA-DIT-2026-0059](evidence-appendix.md#ea-dit-2026-0059))
- [`limit`] GAUGE 在 5 个刚体任务上评测的 6 个 image-to-video 视频世界模型，其生成轨迹可以符合预期物理定律的结构形式，却恢复出错误的物理参数（加速度、动量传递效率、振荡周期/时相），说明视频世界模型的'视觉/结构合理性'与其'定量物理/时序准确度'是分离的、可独立失败的能力。 ([2608.05948](https://arxiv.org/abs/2608.05948) / [EA-DIT-2026-0066](evidence-appendix.md#ea-dit-2026-0066))
- [`limit`] GAUGE 对 Isaac Sim、Genesis、Newton 在 14 个任务上的评测表明没有统一的物理引擎在多机制上一律精准：刚体接触/滑动、动态布料、体积形变等领域各有互补优势，最大 sim-to-real 差异出现在 impulsive contact（即时接触）、高加速度布料运动和 3D 体积形变。 ([2608.05948](https://arxiv.org/abs/2608.05948) / [EA-DIT-2026-0068](evidence-appendix.md#ea-dit-2026-0068))
- [`gap`] 视觉表示存在歧义（如像素级尺寸差、相对位置判定），使仅靠视频（视觉）的视频生成模型在细粒度物理建模上出错，暗示仅靠视觉可能不足以做完整物理建模。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0012](evidence-appendix.md#ea-dit-2026-0012))
- [`gap`] 综述把 '长视频生成的长程时空一致性' 列为核心未解决问题：跨数千帧/多场景时难以同时保持主体身份/物体属性/环境状态统一，现有模型缺乏动态建模与时空记忆，且高维联合分布建模带来计算/训练稳定/推理效率挑战；是领域公认缺口（gover）。 ([2502.17863](https://arxiv.org/abs/2502.17863) / [EA-DIT-2026-0028](evidence-appendix.md#ea-dit-2026-0028))
- [`gap`] RealWonder 的目标是生成'物理合理'而非'严格物理正确'的视频：3D 场景重建的深度误差会导致次优仿真与视频结果；作者明确严格物理正确性（所有动力学严格服从物理定律）仍为未来方向，视频模型还会补偿仿真器缺失/伪影的动态（如合成水波）。 ([2603.05449](https://arxiv.org/abs/2603.05449) / [EA-DIT-2026-0051](evidence-appendix.md#ea-dit-2026-0051))
- [`gap`] 作者明确限制：该模型在精细液体动力学或高可变形物体操作上仍偶尔困难，且桥接 embodiment 需按平台（per-platform）微调，限制其跨机器人队可扩展性——这构成数字遥操作数据引擎在物态复杂度与多本体泛化上的边界。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DIT-2026-0065](evidence-appendix.md#ea-dit-2026-0065))
- [`gap`] GAUGE 的世界模型评测 track 被严格限制在可由二维图像轨迹评估的刚体任务；作者明确指出该表示不足以评估布料与体积软体的分布式形变、深度变化、自遮挡与 self-contact，需要可靠 3D 坐标后才能扩展到这些机制。 ([2608.05948](https://arxiv.org/abs/2608.05948) / [EA-DIT-2026-0069](evidence-appendix.md#ea-dit-2026-0069))

### EA-MODEL (13 events)
- [`support`] ARLON 在 VBench 上相对基线 OpenSora-V1.2 带来 Dynamic Degree +5.6、Aesthetic +4.8、Overall Consistency +11.9、Scene Consistency +6.4，但 Subject/Bkgrd Consistency 略降（↓1.1/↓0.8），Motion Smoothness 微升 ↑0.7；动态上升伴随 mo... ([2410.20502](https://arxiv.org/abs/2410.20502) / [EA-DIT-2026-0005](evidence-appendix.md#ea-dit-2026-0005))
- [`support`] DiT 训练阶段使用更粗粒度的 latent（不同于推理压缩率）会产生更噪的视觉 latent，从而增强 DiT 对 AR 推理误差的容忍，维持生成视频的一致性与质量；配合 uncertainty sampling 进一步模拟 AR 预测方差。 ([2410.20502](https://arxiv.org/abs/2410.20502) / [EA-DIT-2026-0006](evidence-appendix.md#ea-dit-2026-0006))
- [`support`] 在 latent channel 数 = 16 时，IV-VAE（108M）在 Kinetics-600 与 ActivityNet 上的重建指标为 FVD 2.97/2.01、PSNR 39.02/42.61、LPIPS 0.02280/0.01968，为对比方法中最佳（尤其 PSNR 与 LPIPS）。 ([2411.06449](https://arxiv.org/abs/2411.06449) / [EA-DIT-2026-0016](evidence-appendix.md#ea-dit-2026-0016))
- [`support`] IV-VAE 在 Kinetics-600 与 ActivityNet 上分别把重建 FVD 比 OD-VAE 降低 2.68 与 2.02，且参数量不到 OD-VAE 的一半。 ([2411.06449](https://arxiv.org/abs/2411.06449) / [EA-DIT-2026-0017](evidence-appendix.md#ea-dit-2026-0017))
- [`support`] 组因果卷积在参数不变下显著提升基线/KTC 结构的重建与生成性能；KTC 用更小参数（127M→104M）改善时间压缩学习；TMPE 仅 +3M 参数增强运动感知。 ([2411.06449](https://arxiv.org/abs/2411.06449) / [EA-DIT-2026-0018](evidence-appendix.md#ea-dit-2026-0018))
- [`support`] 在 AR 视频生成训练中，AR-DF 的 temporal tube masking 在 VBench-Overall Consistency (OC) 0.249 与 Imaging Quality (IQ) 0.559 上同时优于 random masks（0.232/0.424）与 diffusion forcing masks（0.241/0.540），GenEval 基本持平（0.59... ([2507.08801](https://arxiv.org/abs/2507.08801) / [EA-DIT-2026-0039](evidence-appendix.md#ea-dit-2026-0039))
- [`support`] 掩码并行预测相对 next-token 预测显著降低视频推理时延：单 H20 上视频生成从 next-token 960.0s 降到 mask-pred-with-KV-cache 77.8s；MM-RoPE 相对 1D RoPE 时延几乎不变（77.8s vs 75.1s, 1B）。 ([2507.08801](https://arxiv.org/abs/2507.08801) / [EA-DIT-2026-0040](evidence-appendix.md#ea-dit-2026-0040))
- [`support`] Lumos-1 (3.6B) 在 VBench-I2V 上优于 VideoCrafter-I2V 并与使用 100M 视频、10000 H100 训练的 COSMOS-Video2World 相当，体现 AR 路线用较少数据/算力达到竞争力的结果。 ([2507.08801](https://arxiv.org/abs/2507.08801) / [EA-DIT-2026-0041](evidence-appendix.md#ea-dit-2026-0041))
- [`conditional`] 语义注入的层位置与类型影响 AR-条件对齐：把 AR 码注入 DiT 最后 14 层提供的布局信息不足（视频近似 baseline），而注入前层（first 3/8/14）使布局更好对齐 AR 码；adaptive-norm 注入比 MLP adapter 与 ControlNet 更均衡（ControlNet 动态最高但主体一致性差）。 ([2410.20502](https://arxiv.org/abs/2410.20502) / [EA-DIT-2026-0007](evidence-appendix.md#ea-dit-2026-0007))
- [`limit`] ARLON 基于 OpenSora-V1.2 基底可能封顶视频质量上限，2K 分辨率训练因 AR token 序列过长而不可行，且精细物理手部动作拟真仍难——这三者构成 AR+DiT 混合路线的可扩展性与质量边界。 ([2410.20502](https://arxiv.org/abs/2410.20502) / [EA-DIT-2026-0008](evidence-appendix.md#ea-dit-2026-0008))
- [`limit`] IV-VAE 整体仍基于 UNet 架构，缺乏全局感受野；作者指出应把 DiT 或 Mamba 引入 video VAE（作为未来工作），说明现有视频 VAE 架构与 DiT 主干之间仍有架构鸿沟。 ([2411.06449](https://arxiv.org/abs/2411.06449) / [EA-DIT-2026-0019](evidence-appendix.md#ea-dit-2026-0019))
- [`limit`] Lumos-1 的训练语料（60M 图像 + 10M 视频）相对最近含十亿级样本的 foundation models 明显偏小，因此在需要精细人体动作或高度复杂场景动力学的场景下欠泛化。 ([2507.08801](https://arxiv.org/abs/2507.08801) / [EA-DIT-2026-0042](evidence-appendix.md#ea-dit-2026-0042))
- [`limit`] AR-DF 推理必须在推理阶段使用与训练一致的 partial-context masking，省略该 mask 会显著损害质量（可见伪影与闪烁）。 ([2507.08801](https://arxiv.org/abs/2507.08801) / [EA-DIT-2026-0043](evidence-appendix.md#ea-dit-2026-0043))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 在 RT1 上，从零训练的 action-conditioned diffusion 得到最佳 Action Error Ratio（尽管视觉质量更低），说明动作一致性优先时 from-scratch 也可取胜。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0004](evidence-appendix.md#ea-dit-2026-0004))
- `conditional` 视频 DiT 最优模型尺寸服从 Nopt∝C^a 幂律，且拟合精确度强烈依赖超参最优性：最优超参下 Nopt(C) 斜率偏差 3.57%，固定次优超参下升至 30.26%（工资估最优模型尺寸）。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0022](evidence-appendix.md#ea-dit-2026-0022))
- `conditional` 视频世界模型的物理一致性输出对文本提示敏感：5.2 显示在 bouncing-ball 任务上加 negative prompt 后不同模型的 QFI 发生变化（如 Cosmos3-Super-I2V 降至最低 12.50），因此对这些模型的物理评测结果受提示表述条件控制、不可视为提示无关的固有属性。 ([2608.05948](https://arxiv.org/abs/2608.05948) / [EA-DIT-2026-0067](evidence-appendix.md#ea-dit-2026-0067))
- `limit` AVID 虽免参数但需访问预训练模型去噪过程中的中间预测（latent 情形含 encoder/decoder 输出），这削弱其 closed-source '黑盒' 可移植性。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0002](evidence-appendix.md#ea-dit-2026-0002))
- `limit` AVID adapter 针对特定预训练模型定制，不能在不同预训练模型间复用之，限制了通用性。 ([2410.12822](https://arxiv.org/abs/2410.12822) / [EA-DIT-2026-0003](evidence-appendix.md#ea-dit-2026-0003))
- `limit` 对 DiT 视频生成，ID 泛化随数据/模型缩放近完美且误差下降，而 OOD 泛化误差至少高一个数量级且不随缩放改善，说明 naive 缩放不足以让视频模型发现物理定律。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0009](evidence-appendix.md#ea-dit-2026-0009))
- `limit` 视频模型的 OOD 泛化更接近 '案例式/记忆式'（color>size>velocity>shape 优先层次）而非常见普适物理规则，易受 training set 中的 deceptive 样本偏置。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0011](evidence-appendix.md#ea-dit-2026-0011))
- `limit` 高加速下 AdaCache 可引入时间不一致（伪影、运动、颜色），引入 Motion Regularization（按运动分配计算）在几乎不变加速（4.7x→4.5x）下显著缓解该类伪影。 ([2411.02397](https://arxiv.org/abs/2411.02397) / [EA-DIT-2026-0014](evidence-appendix.md#ea-dit-2026-0014))
- `limit` 本文所有缩放律结论以验证损失（validation loss，代理指标）作为唯一评测，未使用 FVD 等标准视频生成质量指标；作者自称因缺少统一标准视频质量指标而放弃外部基准。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0024](evidence-appendix.md#ea-dit-2026-0024))
- `limit` 该缩放律在低分辨率（17 帧 256x256）、小模型（0.017B-1.07B、单骨干 Cross-DiT、单数据集 Panda-70M）、常量学习率设定上测得；作者声明其可能不适用更高分辨率/更大模型，且未探索分辨率与帧率影响。 ([2411.17470](https://arxiv.org/abs/2411.17470) / [EA-DIT-2026-0025](evidence-appendix.md#ea-dit-2026-0025))
- `limit` 受算力限制，Vid2World 只能以相对轻量的视频扩散模型作为基础模型，未能验证更大规模基础模型的收益。 ([2505.14357](https://arxiv.org/abs/2505.14357) / [EA-DIT-2026-0032](evidence-appendix.md#ea-dit-2026-0032))
- `limit` 因基础模型参数较大与扩散的迭代解码，Vid2World 相对 teacher-forcing 世界模型推理不快，成其下游部署（含对具身/强化学习）的制约。 ([2505.14357](https://arxiv.org/abs/2505.14357) / [EA-DIT-2026-0033](evidence-appendix.md#ea-dit-2026-0033))
- `limit` 来自 LLM 的长上下文扩展技术（YaRN）与 naive History Buffer 不能有效转移到视频生成，因当前视频模型 in-context learning 能力有限。 ([2505.21996](https://arxiv.org/abs/2505.21996) / [EA-DIT-2026-0037](evidence-appendix.md#ea-dit-2026-0037))
- `limit` VRAG 受 GPU 内存与计算成本限制，memory buffer 大小与训练序列长度受限，可能削弱长视界一致性与性能，并限制 edge/资源受限部署。 ([2505.21996](https://arxiv.org/abs/2505.21996) / [EA-DIT-2026-0038](evidence-appendix.md#ea-dit-2026-0038))
- `limit` ACWMs 的 OoD 泛化主要由有效任务复杂度而非物理类别驱动；模型在低维、几何结构明确的任务上泛化良好，在高-DoF 运动学、接触丰富的可变形任务上大幅下降，倾向于捕获视觉外观统计而非内部化底层物理定律。 ([2605.08567](https://arxiv.org/abs/2605.08567) / [EA-DIT-2026-0052](evidence-appendix.md#ea-dit-2026-0052))
- `limit` 最大的 InD→OoD 恶化出现在高维运动学（Robot Arm）与接触丰富的可变形（Cloth Move）任务：两者 M-MSE 大幅上升，显示对分布偏移最脆弱的物理机制是复杂关节运动与 deformable contact。 ([2605.08567](https://arxiv.org/abs/2605.08567) / [EA-DIT-2026-0054](evidence-appendix.md#ea-dit-2026-0054))
- `limit` SANA-WM 作者自承其仍 scale-limited、缺乏显式 3D 场景记忆，并在动态场景、罕见视角或更长回卷中漂移；且部署上全 softmax 注意力在 60s 时 OOM，需混合 GDN/softmax 才可行。 ([2605.15178](https://arxiv.org/abs/2605.15178) / [EA-DIT-2026-0059](evidence-appendix.md#ea-dit-2026-0059))
- `limit` GAUGE 在 5 个刚体任务上评测的 6 个 image-to-video 视频世界模型，其生成轨迹可以符合预期物理定律的结构形式，却恢复出错误的物理参数（加速度、动量传递效率、振荡周期/时相），说明视频世界模型的'视觉/结构合理性'与其'定量物理/时序准确度'是分离的、可独立失败的能力。 ([2608.05948](https://arxiv.org/abs/2608.05948) / [EA-DIT-2026-0066](evidence-appendix.md#ea-dit-2026-0066))
- `limit` GAUGE 对 Isaac Sim、Genesis、Newton 在 14 个任务上的评测表明没有统一的物理引擎在多机制上一律精准：刚体接触/滑动、动态布料、体积形变等领域各有互补优势，最大 sim-to-real 差异出现在 impulsive contact（即时接触）、高加速度布料运动和 3D 体积形变。 ([2608.05948](https://arxiv.org/abs/2608.05948) / [EA-DIT-2026-0068](evidence-appendix.md#ea-dit-2026-0068))
- `gap` 视觉表示存在歧义（如像素级尺寸差、相对位置判定），使仅靠视频（视觉）的视频生成模型在细粒度物理建模上出错，暗示仅靠视觉可能不足以做完整物理建模。 ([2411.02385](https://arxiv.org/abs/2411.02385) / [EA-DIT-2026-0012](evidence-appendix.md#ea-dit-2026-0012))
- `gap` 综述把 '长视频生成的长程时空一致性' 列为核心未解决问题：跨数千帧/多场景时难以同时保持主体身份/物体属性/环境状态统一，现有模型缺乏动态建模与时空记忆，且高维联合分布建模带来计算/训练稳定/推理效率挑战；是领域公认缺口（gover）。 ([2502.17863](https://arxiv.org/abs/2502.17863) / [EA-DIT-2026-0028](evidence-appendix.md#ea-dit-2026-0028))
- `gap` RealWonder 的目标是生成'物理合理'而非'严格物理正确'的视频：3D 场景重建的深度误差会导致次优仿真与视频结果；作者明确严格物理正确性（所有动力学严格服从物理定律）仍为未来方向，视频模型还会补偿仿真器缺失/伪影的动态（如合成水波）。 ([2603.05449](https://arxiv.org/abs/2603.05449) / [EA-DIT-2026-0051](evidence-appendix.md#ea-dit-2026-0051))
- `gap` 作者明确限制：该模型在精细液体动力学或高可变形物体操作上仍偶尔困难，且桥接 embodiment 需按平台（per-platform）微调，限制其跨机器人队可扩展性——这构成数字遥操作数据引擎在物态复杂度与多本体泛化上的边界。 ([2607.06558](https://arxiv.org/abs/2607.06558) / [EA-DIT-2026-0065](evidence-appendix.md#ea-dit-2026-0065))
- `gap` GAUGE 的世界模型评测 track 被严格限制在可由二维图像轨迹评估的刚体任务；作者明确指出该表示不足以评估布料与体积软体的分布式形变、深度变化、自遮挡与 self-contact，需要可靠 3D 坐标后才能扩展到这些机制。 ([2608.05948](https://arxiv.org/abs/2608.05948) / [EA-DIT-2026-0069](evidence-appendix.md#ea-dit-2026-0069))
- `conditional` 语义注入的层位置与类型影响 AR-条件对齐：把 AR 码注入 DiT 最后 14 层提供的布局信息不足（视频近似 baseline），而注入前层（first 3/8/14）使布局更好对齐 AR 码；adaptive-norm 注入比 MLP adapter 与 ControlNet 更均衡（ControlNet 动态最高但主体一致性差）。 ([2410.20502](https://arxiv.org/abs/2410.20502) / [EA-DIT-2026-0007](evidence-appendix.md#ea-dit-2026-0007))
- `limit` ARLON 基于 OpenSora-V1.2 基底可能封顶视频质量上限，2K 分辨率训练因 AR token 序列过长而不可行，且精细物理手部动作拟真仍难——这三者构成 AR+DiT 混合路线的可扩展性与质量边界。 ([2410.20502](https://arxiv.org/abs/2410.20502) / [EA-DIT-2026-0008](evidence-appendix.md#ea-dit-2026-0008))
- `limit` IV-VAE 整体仍基于 UNet 架构，缺乏全局感受野；作者指出应把 DiT 或 Mamba 引入 video VAE（作为未来工作），说明现有视频 VAE 架构与 DiT 主干之间仍有架构鸿沟。 ([2411.06449](https://arxiv.org/abs/2411.06449) / [EA-DIT-2026-0019](evidence-appendix.md#ea-dit-2026-0019))
- `limit` Lumos-1 的训练语料（60M 图像 + 10M 视频）相对最近含十亿级样本的 foundation models 明显偏小，因此在需要精细人体动作或高度复杂场景动力学的场景下欠泛化。 ([2507.08801](https://arxiv.org/abs/2507.08801) / [EA-DIT-2026-0042](evidence-appendix.md#ea-dit-2026-0042))
- `limit` AR-DF 推理必须在推理阶段使用与训练一致的 partial-context masking，省略该 mask 会显著损害质量（可见伪影与闪烁）。 ([2507.08801](https://arxiv.org/abs/2507.08801) / [EA-DIT-2026-0043](evidence-appendix.md#ea-dit-2026-0043))

## Writer handoff

- Use `$embodied-ai-review-writer` with this brief, the accepted evidence JSONL, and `evidence-appendix.md`.
- The writer loads only the requested style reference and drafts each style independently from this evidence model.
- Generate `trace-map.json`, then pass the writer's editorial quality audit before settlement.

## 引用速查

- **正文引用 = arXiv 论文链接**:`[2606.13877](https://arxiv.org/abs/2606.13877)` 或 `[SIEVE](https://arxiv.org/abs/2607.06442)`。读者点开即达论文。
- 事件级溯源留给 appendix:成稿正文不放 `evidence-appendix.md#...` 事件锚点;需要精确定位(章节/立场/置信)时,读者从 References 或 appendix 查。
- 本简报中每条证据给出 `论文链接 / 事件链接` 对:写作时**取前者入正文**,后者供你核对 locator 与 stance。
- Citation density and visible source format are style-specific; do not force a full bibliography into Xiaohongshu prose.
- 完整证据条目在 [evidence-appendix.md](evidence-appendix.md);事件映射由 `trace-map.json` 保存。
- Registered sources: not loaded
