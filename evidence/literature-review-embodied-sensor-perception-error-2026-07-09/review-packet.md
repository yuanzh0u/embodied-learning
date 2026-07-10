# Review Packet: 具身传感器感知误差

## Scope

- Topic: 具身传感器感知误差
- Time range: 2026-01-09..2026-07-09
- Review style: `survey`
- Knowledge IDs: `EA-SENSOR`, `EA-DATA`, `EA-EVAL`
- Evidence events: 12
- Topic cards: 3
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: planner -> hub -> review packet -> style menu.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for retrieval, HTML mining, and evidence promotion.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 12
- Stance labels: `conditional`, `gap`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-EVAL-2026-0007`, `EA-EVAL-2026-0012`, `EA-SENSOR-2026-0004`, `EA-SENSOR-2026-0003`, `EA-SENSOR-2026-0006`, `EA-SENSOR-2026-0011`, `EA-SENSOR-2026-0009`, `EA-SENSOR-2026-0001`, `EA-SENSOR-2026-0002`, `EA-SENSOR-2026-0008`, `EA-SENSOR-2026-0010`, `EA-SENSOR-2026-0005`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Evidence Sufficiency

- Evidence sufficiency: formal-ready
- Paper-level sources: 12 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

## Source Tiers

- No fallback source-tier records provided.

## Topic Card Context

- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是基础能力底座，但不是完整机器人感知系统。RGB 擅长语义和外观，弱于深度、接触、力、摩擦、滑移、材料和被遮挡几何。3D/点云在空间约束和精密操作中改变上限，触觉与力/力矩在接触闭环中提供视觉无法直接观测的状态。多模态建模的目标不是堆传感器，而是让每个模态对应可验证的控制收益。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-DATA` 数据采集与数据质量: 数据采集不是单纯堆轨迹，而是硬件、时间同步、标定、动作表示、元数据、采集员规范和质量审计组成的工程体系。UMI 更接近可学控制数据，Ego/Ego4D 更接近感知与任务先验，DROID 展示了自然场景大规模机器人数据的组织难度。无目标机器人本体阶段仍可积累任务、视觉、语义、可重定向轨迹和失败库，但不能直接等价为可部署策略数据，最终需要少量目标机器人锚点闭环校准。泛化任务优先任务/场景多样性，工业单任务优先数据精度、边界工况和失败恢复。遮挡、异构数据有效性和单视角限制必须用任务相关指标验证。
  - VR 遥操作主要采动作意图和视觉闭环，力反馈采集额外覆盖接触隐变量。
  - 触觉/力反馈对开放空间抓放不是总必要，但对插入、柔顺贴合、易碎物和滑移控制很重要。
  - 国内难复制 UMI/Ego/DROID 的核心难点是数据工程体系，而不是单个硬件原型。
  - 实验室数据适合原子技能和受控因果分析，自然场景数据决定跨场景和长尾泛化。
  - 少量轨迹阶段应先保证受控一致性，再有计划地引入关键变量多样性。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功率。闭环评测难在误差会改变后续观测并累积，还涉及硬件安全、任务重置、失败恢复和随机接触。当前没有覆盖全行业、全本体、全任务的统一评测体系，未来更可能按任务族分层。世界模型当前主要解决预测、想象和筛选问题，能辅助规划和降低试错成本，但还不能替代真实环境验证。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 6 |
| `conditional` | 条件成立 | 3 |
| `limit` | 限制/负面 | 2 |
| `gap` | 缺口 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2606.08765: RGB-S: Image-Aligned Tactile Saliency for Robust Dexterous Manipulation | 2026-06-07 | conditional | EA-SENSOR-2026-0002 |
| 2606.16690: PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation | 2026-06-15 | limit | EA-SENSOR-2026-0005 |
| 2606.18043: Uncertainty Quantification for Flow-Based Vision-Language-Action Models | 2026-06-16 | support | EA-SENSOR-2026-0004 |
| 2606.20754: Perturbation-Based Uncertainty for Failure Detection in Vision-Language-Action Models | 2026-06-18 | support | EA-SENSOR-2026-0003 |
| 2606.26663: Tactile-WAM: Touch-Aware World Action Model with Tactile Asymmetric Attention | 2026-06-25 | conditional | EA-SENSOR-2026-0008 |
| 2606.28899: You Only Touch Once: 6-DoF Object Pose Estimation from Single Tactile Contact | 2026-06-27 | support | EA-SENSOR-2026-0006 |
| 2606.29384: Event-VLA: Action-Conditioned Event Fusion for Robust Vision-Language-Action Model | 2026-06-28 | support | EA-SENSOR-2026-0011 |
| 2606.30988: Multisensory Continual Learning: Adapting Pretrained Visuomotor Policies to Force | 2026-06-29 | conditional | EA-SENSOR-2026-0010 |
| 2607.02840: TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | support | EA-SENSOR-2026-0009 |
| 2607.04234: SoftVTBench: A Safety-Aware Visuo-Tactile Benchmark for Physically Constrained Robotic Manipulation of Deformable Objec... | 2026-07-05 | limit | EA-EVAL-2026-0007 |
| 2607.07196: Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators | 2026-07-08 | gap | EA-EVAL-2026-0012 |
| 2607.07287: TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation | 2026-07-08 | support | EA-SENSOR-2026-0001 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-EVAL-2026-0007 | EA-EVAL | `limit` | `direct` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 | 作者指出现有 manipulation benchmarks 多以 success 为中心，很少评估执行过程是否物理安全；SoftVTBench 分开报告 Goal Success 和 Safety Success，后者要求无掉落并限制峰值形变。实验显示 success-only evaluation 会显著高估策略表现，而触觉感知可改善 Safety Success 并降低物体形变。 (arXiv HTML Abstract; 1... | bowen-jing | 2607.04234 |
| EA-EVAL-2026-0012 | EA-EVAL | `gap` | `direct` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 | 作者指出机器人中 World Models 越来越被用于模拟动作后果并给出 success/safety verdict，但视频生成指标如 FVD 奖励视觉真实感，却忽略世界是否对 policy actions 正确响应；他们主张作为 test oracle 的 WM 需要先通过 accreditation，并提出 L0-L4 admissibility ladder。 (arXiv HTML Abstract; I Introduc... | christian-oefinger | 2607.07196 |
| EA-SENSOR-2026-0004 | EA-SENSOR | `support` | `direct` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 | 作者将真实非平稳环境中的分布外场景描述为 VLA 可能“无预警失败”的关键限制，并提出用小 ensemble 的 velocity-field disagreement 量化 epistemic uncertainty；LIBERO 实验显示该不确定性与下游表现、失败检测和主动采样相关。 (arXiv HTML Abstract; 1 Introduction; Appendix B.4 Uncertainty Quantificat... | ralf-romer | 2606.18043 |
| EA-SENSOR-2026-0003 | EA-SENSOR | `support` | `direct` | VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 | 作者指出现代 VLA 常用回归或 flow-based action generation，缺少显式预测概率；他们通过对 transformer hidden activations 注入高斯扰动，利用扰动后动作预测分歧估计不确定性，并在 LIBERO/LIBERO-PRO 的分布偏移下提升失败检测。 (arXiv HTML Abstract; I Introduction; IV-D Main Results) | yousung-lee | 2606.20754 |
| EA-SENSOR-2026-0006 | EA-SENSOR | `support` | `direct` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 | 作者明确指出视觉位姿估计常在遮挡、差光照、反光或透明表面下失败，并提出 tactile-only pose estimation：把触觉接触表示成局部 3D 点云，结合校准传感器位姿恢复完整 6-DoF object pose；实验在视觉不可靠时优于视觉和几何基线。 (arXiv HTML Abstract; 1 Introduction; 4.2 6-DoF Object Pose Estimation under Occlusio... | pengfei-ye | 2606.28899 |
| EA-SENSOR-2026-0011 | EA-SENSOR | `support` | `direct` | RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 | 作者指出现有 VLA 往往假设稳定明亮的室内环境，而真实操作中 illumination shifts 会造成 degraded RGB observations；Event-VLA 将 degraded visibility 定义为 RGB-centric policies 的鲁棒性问题，并通过 action-query routing 将 event streams 融入 action representation，仿真和真实部署... | jiaxin-liu | 2606.29384 |
| EA-SENSOR-2026-0009 | EA-SENSOR | `support` | `direct` | 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。 | 作者指出 VLA 在 contact-rich tasks 中会被小接触扰动触发不可恢复失败，且这些失败常难以单靠视觉检测；TACO 用 tactile-aware world model 识别 failure-adjacent states、想象局部 correction segments 并标注可执行纠正动作，真实接触任务报告相对 base policy 的成功率提升。 (arXiv HTML Abstract; 1 Introd... | shengbang-liu | 2607.02840 |
| EA-SENSOR-2026-0001 | EA-SENSOR | `support` | `direct` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 | 作者把日常灵巧操作的误差来源明确落在滑移、错位、不稳定抓取和力不匹配上，并指出视觉/语言不能可靠揭示力、滑移和接触稳定性；其分层策略将视觉语言子任务规划、触觉世界模型预测和高频触觉残差修正分开。 (arXiv HTML Abstract; 1 Introduction) | jianyi-zhou | 2607.07287 |
| EA-SENSOR-2026-0002 | EA-SENSOR | `conditional` | `direct` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 | 作者称视觉观测不可靠或被遮挡时，稀疏异构触觉与稠密视觉表示的对齐是核心挑战；方法使用正运动学和相机标定投影触觉传感器位置，并用力调制高斯 saliency maps 建模运动学和标定误差带来的空间不确定性。 (arXiv HTML Abstract; 1 Introduction; 3.2 Force-Aware Kinematic Projection; 4.3 Ablation on RGB-S Design Choices) | shengcheng-luo | 2606.08765 |
| EA-SENSOR-2026-0008 | EA-SENSOR | `conditional` | `direct` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 | 作者指出 insertion、assembly、search、reorientation 依赖 slip、jamming、contact normals 和小对齐误差，这些状态在 RGB 中弱可见或不可见；同时他们定义 tactile pollution：无约束触觉 token 注入会迫使视觉 dynamics model 吸收稀疏局部事件式接触信号，从而退化视频和动作预测。 (arXiv HTML Abstract; I Intro... | siyu-wu | 2606.26663 |
| EA-SENSOR-2026-0010 | EA-SENSOR | `conditional` | `direct` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 | 作者称接触丰富任务常依赖 vision 之外的 sensory data，force、tactile 或 audio feedback 能揭示 images 中不可直接观察的 interaction states；但这些模态 hardware- and task-specific，且大规模多传感数据稀缺。他们提出 MuSe，将 limited multisensory data 融入 pretrained vision-only po... | jaden-clark | 2606.30988 |
| EA-SENSOR-2026-0005 | EA-SENSOR | `limit` | `direct` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 | 作者指出开放工作空间中移动物体、瞬时遮挡和目标运动附近扰动会让部署脆弱；现有 runtime monitors 往往依赖全局 observation anomalies、policy uncertainty 或 frame-level visual changes，难以区分任务相关执行风险和无害视觉变化。PATCH 通过 active action chunk 的 projected execution corridor 累计持续残差... | yanan-zhou | 2606.16690 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-EVAL-2026-0007 | bowen-jing | unlisted | `limit` | 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 |
| EA-EVAL-2026-0012 | christian-oefinger | unlisted | `gap` | 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 |
| EA-SENSOR-2026-0004 | ralf-romer | unlisted | `support` | Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 |
| EA-SENSOR-2026-0003 | yousung-lee | unlisted | `support` | VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 |
| EA-SENSOR-2026-0006 | pengfei-ye | unlisted | `support` | 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 |
| EA-SENSOR-2026-0011 | jiaxin-liu | unlisted | `support` | RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 |
| EA-SENSOR-2026-0009 | shengbang-liu | unlisted | `support` | 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。 |
| EA-SENSOR-2026-0001 | jianyi-zhou | unlisted | `support` | 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 |
| EA-SENSOR-2026-0002 | shengcheng-luo | unlisted | `conditional` | 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 |
| EA-SENSOR-2026-0008 | siyu-wu | unlisted | `conditional` | 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 |
| EA-SENSOR-2026-0010 | jaden-clark | unlisted | `conditional` | 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 |
| EA-SENSOR-2026-0005 | yanan-zhou | unlisted | `limit` | 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 |

## Synthesis Slots

### 共识/正向证据
- `EA-SENSOR-2026-0004`: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
- `EA-SENSOR-2026-0003`: VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。
- `EA-SENSOR-2026-0006`: 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。
- `EA-SENSOR-2026-0011`: RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。
- `EA-SENSOR-2026-0009`: 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。
- `EA-SENSOR-2026-0001`: 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。
### 条件成立
- `EA-SENSOR-2026-0002`: 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。
- `EA-SENSOR-2026-0008`: 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。
- `EA-SENSOR-2026-0010`: 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。
### 限制与失败模式
- `EA-EVAL-2026-0007`: 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
- `EA-SENSOR-2026-0005`: 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。
### 开放问题
- `EA-EVAL-2026-0012`: 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 12 / 5
- Recommended default: all
- Core claims:
  - `EA-EVAL-2026-0007` 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。
  - `EA-EVAL-2026-0012` 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。
  - `EA-SENSOR-2026-0004` Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。
- Scientific memo preview: 《具身传感器感知误差》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 具身传感器感知误差 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 具身传感器感知误差: 先看证据边界，再谈一个可传播的反常识洞察。

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
