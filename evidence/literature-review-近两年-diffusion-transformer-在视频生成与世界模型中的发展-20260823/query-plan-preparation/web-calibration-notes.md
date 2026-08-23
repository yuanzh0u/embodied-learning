# Web Calibration Notes — Diffusion Transformer 视频/世界模型

> 校准时间：2026-08-23。来源：Explore 子代理网络检索（官方页 + arXiv + 第三方评测/追踪页）。
> 用途：补充检索方向与精读选篇候选提示。
> **口径红线**：本文件是候选提示，不是论文证据。下列 arXiv ID 均由网络检索返回，进入精读前必须用 arXiv 全文/官方仓库核验其真实性；凡标"待验证"者不得直接引用。

## 一、旗舰系统前沿（可作为背景 anchor）
- OpenAI Sora 2（2025-09-30，无官方 arXiv 技术报告；Sora 2 System Card 称"朝向更准确模拟物理世界复杂性"）
- Google Veo 3（latent diffusion，文本/图像→视频+音频；Veo 3 Model Card）
- DeepMind Genie 3（2025-08-05，交互式可导航 3D 环境世界模型，实时 720p/24fps）
- World Labs Marble（文本/图像/视频/粗3D布局→可探索 3D 世界，交互编辑）
- Meta Movie Gen（arXiv:2410.13720，Flow Matching/Transformer，30B，1080p/16s）
- 快手 Kling 3.0（长视频 2min/4K 口径为第三方）
- 字节 Seedance 2.0（arXiv:2506.09113，decoupled spatial+temporal 的 DiT）、Seedance 2.5（2026-07-31，30s 音视频一次生成）
- 阿里 Wan 2.1（arXiv:2503.20314，open video generative models）、Wan 2.7-Video（社区口径，待验证）

## 二、Diffusion Transformer 代表作（arXiv 全文，适合精读）
- Wan 2.1 arXiv:2503.20314
- HunyuanVideo 1.0 arXiv:2412.03603；HunyuanVideo 1.5 技术报告 arXiv:2511.18870（待验证）
- Open-Sora 2.0 arXiv:2503.09642
- CogVideoX arXiv:2408.06072（ICLR 2025）
- Latte arXiv:2401.03048（TMLR2025）
- W.A.L.T arXiv:2312.06662（统一 latent + window attention）
- SVD/SVD-XT arXiv:2408.15239
- Mochi-1（Genmo 博客口径，10B AsymmDiT，128× VAE 压缩；无官方 arXiv，"Mochi-1 Asymmetric Diffusion Transformer" arXiv:2410.15098 为社区对应，待验证）

## 三、评测基准与评测方法
- T2VPhysBench arXiv:2505.00337：第一性原理物理一致性评测
- WBench arXiv:2605.25874（待验证）：多轮交互视频世界模型，5 维 289 用例 1058 轮
- WorldLens（网站口径）："look real but behave unreal" 全谱评测
- WorldModelBench（项目页口径）：7 应用域 56 子域 + physics adherence
- WorldArena（网站口径）：具身世界模型（感知/数据引擎/策略评估/动作规划）
- T2VTextBench arXiv:2505.04946：文本控制能力
- Infinite-World arXiv:2602.02393（待验证）：1000-frame 交互世界模型 + VBench
- MagicWorld arXiv:2511.18886（待验证）：long-horizon stability + DMD 蒸馏
- MTV-World arXiv:2511.12882（待验证）：多视角轨迹显式运动控制

## 四、关键限制与机制讨论
- 物理一致性是硬伤：T2VPhysBench 显示即便要求违反物理，模型仍较差 → 模型未真正建模"不可能物理"
- Think Before You Diffuse：很晚才解码 video token 时形状/物理失败已发生
- WorldLens 结论：当前世界模型"看起来真实但行为不真实"，无单一模型全维领先
- 视频世界模型(action-conditioned、决策后果建模) vs 被动视频生成：可控性区别
- 实体保持：无显式 appearance condition 时重入对象身份丢失（WorldDirector 待验证）
- 交互时序：能生成交互但难控时机（HelloWorld TimeAcc 81.7% vs 其他 33.3%，待验证）
- 长视频一致性依赖 memory 机制（Infinite-World）
- 计算/部署：Magic 1-For-1 arXiv:2502.07701（step+CFG 蒸馏）、POSE arXiv:2508.21019（单步）、CausVid arXiv:2412.07772（few-step autoregressive 9.4FPS）、FastGen（博客口径 10-100×）、LWM arXiv:2402.08268（RingAttention 长上下文 AR）、DeltaToken（streaming encoder，项目页）

## 五、具身/机器人交叉（adjacent，链接 EA-4D/EA-EVAL）
- ABot-PhysWorld arXiv:2603.23376（待验证）：14B DiT 物理合理动作可控视频
- OSCAR arXiv:2606.04463（待验证）：omni-embodiment action-conditioned world model
- MoWM arXiv:2509.21797（待验证）：mixture-of-world-models，latent→pixel 指导
- MTV-World arXiv:2511.12882（待验证）
- World Model for Robot Learning Survey arXiv:2605.00080（待验证）
- WorldLens-Agent：distilled auto-evaluator 发现 "look real but behave unreal"

## 检索示例（用于第二轮补充）
见 `query-plan-preparation/dynamic-suggestions.json`。第二轮可按本校准加入：物理一致性基准、action-conditioning gap、视频 token/蒸馏路线、交互式世界模型基准。