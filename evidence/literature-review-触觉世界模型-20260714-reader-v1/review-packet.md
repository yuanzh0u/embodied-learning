# Review Packet: 触觉世界模型

## Scope

- Topic: 触觉世界模型
- Time range: 2026-01-14..2026-07-14
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-EVAL`, `EA-MODEL`, `EA-SENSOR`
- Evidence events: 15
- Topic cards: 0
- Registered source IDs available: not loaded

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 15
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-DATA-READ-0008`, `EA-DATA-READ-0005`, `EA-DATA-READ-0002`, `EA-DATA-READ-0006`, `EA-DATA-READ-0003`, `EA-DATA-READ-0004`, `EA-DATA-READ-0015`, `EA-DATA-READ-0001`, `EA-DATA-READ-0007`, `EA-DATA-READ-0014`, `EA-DATA-READ-0010`, `EA-DATA-READ-0011`
- Registered sources: not loaded

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Full text recovered: 15
- Structure mapped: 15
- Deep-read papers: 15
- Claim-verified papers: 15
- Accepted evidence papers: 15
- Paper-reading gate: passed
- Formal writing is allowed; continue reading if new batches still add material claim clusters.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- No topic cards provided.

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 7 |
| `conditional` | 条件成立 | 5 |
| `limit` | 限制/负面 | 2 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.06001: Visuo-Tactile World Models | 2026-02-05 | conditional | EA-DATA-READ-0001 |
| 2604.07335: TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks | 2026-04-08 | support | EA-DATA-READ-0008 |
| 2605.07308: AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models | 2026-05-08 | conditional | EA-DATA-READ-0007 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | support | EA-DATA-READ-0005 |
| 2606.08737: Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation | 2026-06-07 | support | EA-DATA-READ-0002 |
| 2606.08765: RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation | 2026-06-07 | conditional | EA-DATA-READ-0014 |
| 2606.11184: TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation | 2026-06-09 | support | EA-DATA-READ-0006 |
| 2606.13877: ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation | 2026-06-11 | support | EA-DATA-READ-0003 |
| 2606.14981: Inference-time Policy Steering via Vision and Touch | 2026-06-12 | support | EA-DATA-READ-0004 |
| 2606.16690: PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation | 2026-06-15 | limit | EA-DATA-READ-0009 |
| 2606.18043: Uncertainty Quantification for Flow-Based Vision-Language-Action Models | 2026-06-16 | support | EA-DATA-READ-0015 |
| 2606.26663: Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention | 2026-06-25 | conditional | EA-DATA-READ-0010 |
| 2606.30988: Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force | 2026-06-29 | conditional | EA-DATA-READ-0011 |
| 2607.04234: SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objec... | 2026-07-05 | limit | EA-DATA-READ-0012 |
| 2607.07196: Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators | 2026-07-08 | gap | EA-DATA-READ-0013 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-DATA-READ-0008 | EA-DATA | `support` | `direct` | TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 | 摘要明确列出精度/便携双模式采集、触觉恢复遥操作和人在环恢复数据。 (Abstract (full-text section)) | longyan-wu; jieji-ren; chenghang-jiang; et al. | 2604.07335 |
| EA-DATA-READ-0005 | EA-DATA | `support` | `direct` | 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 | HapTile 的每个夹爪手指安装视觉触觉传感器，接触会带来图像变化和 marker displacement；论文把 marker-motion 信号保存进数据集并用于 haptic feedback，实验也比较 vision-only、vision+tactile image 与 vision+tactile+marker 表征。 (4.2 Vision-Based Tactile Sensing and Marker Track... | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-DATA-READ-0002 | EA-DATA | `support` | `direct` | 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 | Dream-Tac 把 world action model 扩展到触觉，联合建模当前视觉、触觉、语言指令下的未来视觉观测、未来触觉观测和动作 chunk，并加入 contact-gated visuotactile fusion 与 contact-aware attention bias。 (Abstract (full-text section)) | yunfan-lou; yifan-ye; yankai-fu; et al. | 2606.08737 |
| EA-DATA-READ-0006 | EA-DATA | `support` | `direct` | 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 | TacForeSight 的 TacForceWM 从双指触觉观测出发，以高频腕部 force/torque 为条件预测短时域触觉 latent dynamics；ablation 中 wrist wrench 条件的未来触觉预测优于无条件版本，MSE 从 0.027 降到 0.017，cosine 从 0.954 提升到 0.992。 (IV-D 1 World Model Conditioning) | yujie-zang; yuhang-zheng; xian-nie; et al. | 2606.11184 |
| EA-DATA-READ-0003 | EA-DATA | `support` | `direct` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 | ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。 (Abstract (full-text section)) | zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al. | 2606.13877 |
| EA-DATA-READ-0004 | EA-DATA | `support` | `direct` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 | ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。 (5 Experiments) | yilin-wu; zilin-si; zeynep-temel; et al. | 2606.14981 |
| EA-DATA-READ-0015 | EA-DATA | `support` | `direct` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 | 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。 (Abstract (full-text section)) | ralf-rmer | 2606.18043 |
| EA-DATA-READ-0001 | EA-DATA | `conditional` | `direct` | VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 | 训练数据段明确列出了同步的本体状态、外部视频与双指触觉视频数据流。 (B.0.1 Training dataset) | carolina-higuera; sergio-arnaud; byron-boots; et al. | 2602.06001 |
| EA-DATA-READ-0007 | EA-DATA | `conditional` | `direct` | 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 | AT-VLA 把系统分为慢速视觉语言流和快速触觉流，慢速流负责任务理解和视觉定位，快速流以高频处理触觉反馈；作者采用 3:1 的快慢流频率比，并在真实接触丰富任务中验证 adaptive tactile injection、tactile gate、adaptive cross-attention 和 reaction dual-stream 的作用。 (5 Conclusion) | xiaoqi-li; muhe-cai; jiadong-xu; et al. | 2605.07308 |
| EA-DATA-READ-0014 | EA-DATA | `conditional` | `direct` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 | 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。 (Abstract (full-text section)) | shengcheng-luo | 2606.08765 |
| EA-DATA-READ-0010 | EA-DATA | `conditional` | `direct` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 | 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。 (Abstract (full-text section)) | siyu-wu; linjing-you; junjie-zhu; et al. | 2606.26663 |
| EA-DATA-READ-0011 | EA-DATA | `conditional` | `direct` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 | 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only po... | jaden-clark; changhao-wang; yihuai-gao; et al. | 2606.30988 |
| EA-DATA-READ-0009 | EA-DATA | `limit` | `direct` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 | 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差... | yanan-zhou; ranpeng-qiu; yincong-chen; et al. | 2606.16690 |
| EA-DATA-READ-0012 | EA-DATA | `limit` | `direct` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 | 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。 (1 Introduction) | bowen-jing; mingxin-wang; ruiyang-hao; et al. | 2607.04234 |
| EA-DATA-READ-0013 | EA-DATA | `gap` | `direct` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 | 作者指出机器人中 World Models 越来越被用于模拟动作后果并给出 success/safety verdict，但视频生成指标如 FVD 奖励视觉真实感，却忽略世界是否对 policy actions 正确响应；他们主张作为 test oracle 的 WM 需要先通过 accreditation，并提出 L0-L4 admissibility ladder。 (Abstract (full-text section)) | christian-oefinger | 2607.07196 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-DATA-READ-0008 | longyan-wu; jieji-ren; chenghang-jiang; et al. | unlisted | `support` | TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 |
| EA-DATA-READ-0005 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `support` | 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 |
| EA-DATA-READ-0002 | yunfan-lou; yifan-ye; yankai-fu; et al. | unlisted | `support` | 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 |
| EA-DATA-READ-0006 | yujie-zang; yuhang-zheng; xian-nie; et al. | unlisted | `support` | 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 |
| EA-DATA-READ-0003 | zhiyuan-zhang; pokuang-zhou; kaidi-zhang; et al. | unlisted | `support` | 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 |
| EA-DATA-READ-0004 | yilin-wu; zilin-si; zeynep-temel; et al. | unlisted | `support` | 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 |
| EA-DATA-READ-0015 | ralf-rmer | unlisted | `support` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 |
| EA-DATA-READ-0001 | carolina-higuera; sergio-arnaud; byron-boots; et al. | unlisted | `conditional` | VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 |
| EA-DATA-READ-0007 | xiaoqi-li; muhe-cai; jiadong-xu; et al. | unlisted | `conditional` | 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 |
| EA-DATA-READ-0014 | shengcheng-luo | unlisted | `conditional` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 |
| EA-DATA-READ-0010 | siyu-wu; linjing-you; junjie-zhu; et al. | unlisted | `conditional` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 |
| EA-DATA-READ-0011 | jaden-clark; changhao-wang; yihuai-gao; et al. | unlisted | `conditional` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 |
| EA-DATA-READ-0009 | yanan-zhou; ranpeng-qiu; yincong-chen; et al. | unlisted | `limit` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 |
| EA-DATA-READ-0012 | bowen-jing; mingxin-wang; ruiyang-hao; et al. | unlisted | `limit` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 |
| EA-DATA-READ-0013 | christian-oefinger | unlisted | `gap` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 |

## Synthesis Slots

### 共识/正向证据
- `EA-DATA-READ-0008`: TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。
- `EA-DATA-READ-0005`: 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
- `EA-DATA-READ-0002`: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
- `EA-DATA-READ-0006`: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。
- `EA-DATA-READ-0003`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- `EA-DATA-READ-0004`: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。
- `EA-DATA-READ-0015`: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
### 条件成立
- `EA-DATA-READ-0001`: VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。
- `EA-DATA-READ-0007`: 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。
- `EA-DATA-READ-0014`: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- `EA-DATA-READ-0010`: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- `EA-DATA-READ-0011`: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
### 限制与失败模式
- `EA-DATA-READ-0009`: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
- `EA-DATA-READ-0012`: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
### 开放问题
- `EA-DATA-READ-0013`: 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-DATA-READ-0008` TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。
  - `EA-DATA-READ-0005` 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
  - `EA-DATA-READ-0002` 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
- Scientific memo preview: 《触觉世界模型》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 触觉世界模型 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 触觉世界模型: 先看证据边界，再谈一个可传播的反常识洞察。

## Draft Outline

1. 研究边界与证据范围
2. 概念与问题结构
3. 主要共识
4. 条件、限制与分歧
5. 未解决问题
6. 对后续研究/项目的启发

## Traceability Checklist

- Cite event IDs for paper-specific claims.
- Cite stable source IDs for topic-card background.
- Mark cross-event synthesis as `inference` with a short reason.
- Do not cite candidate-only papers as accepted evidence.
- Open raw sources before using exact wording.
