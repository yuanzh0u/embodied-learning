# Review Packet: ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测

## Scope

- Topic: ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测
- Time range: 2026-02-07..2026-08-07
- Review style: `survey`
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-ALIGN`
- Evidence events: 15
- Topic cards: 2
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Orchestration Contract

- Main path: review mode -> planner -> candidate registry -> coverage/saturation -> complete HTML/PDF recovery -> paper reader -> review packet -> writer.
- Use `$embodied-ai-query-planner` for topic mapping and query planning.
- Use `$embodied-ai-literature-hub` for multi-round retrieval and complete HTML/text-layer-PDF recovery.
- Use `$embodied-ai-paper-reader` for deep reading, critical appraisal, claim verification, and evidence projection.
- This review packet is not a replacement for either upstream Skill.

## Evidence Core

- Accepted events: 15
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-ACTRT-2026-0003`, `EA-ACTRT-2026-0002`, `EA-ACTRT-2026-0005`, `EA-ACTRT-2026-0006`, `EA-ACTRT-2026-0007`, `EA-ACTRT-2026-0012`, `EA-ACTRT-2026-0015`, `EA-ACTRT-2026-0013`, `EA-ACTRT-2026-0014`, `EA-ACTRT-2026-0010`, `EA-ACTRT-2026-0009`, `EA-ACTRT-2026-0011`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

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

- `EA-MODEL` 模型与预训练: 机器人统一模型短中期更可能是“共享骨干 + 任务/本体适配器 + 连续动作专家”，而不是一个模型直接控制所有机器人。“反应式 VLA 已死”只对不显式检验动作后果的狭义策略成立；跨 run 证据更支持 VLA 语义/动作先验、动作条件世界模型、本体适配器与底层控制器组成的融合栈。近期突破不只是生成更长视频，而是把未来压缩成低频逻辑步骤、稀疏视觉子目标或结构化状态，并验证它与真实动作同步；BadWAM 说明“想象合理、动作错误”足以让系统失效。世界模型应先承担训练期教师、离线排序等低权限任务，再逐级争取在线规划权。Loco-manipulation 与多模态证据还表明，完整动作接口及按功能/时标分层的接触反馈会限制能力上限。预训练价值最终仍以目标任务闭环样本复杂度和真实成功率衡量。
  - VLA/RT-X/Octo/OpenVLA/π0 等说明视觉-语言-动作统一建模有迁移潜力。
  - Unified Scaling 的挑战在于数据、本体、动作空间、奖励和评估都不统一。
  - Benchmark 好成绩不等于真实世界鲁棒性，真实部署会遇到分布偏移和闭环误差累积。
  - 场景微调不理想时，可能是数据、动作接口、控制器、标定和失败恢复共同问题。
  - 预训练评估应做 ablation：从零训练、只用目标数据、预训练 + 微调、不同预训练来源。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。当前最可靠的应用位于权限阶梯低端：训练期 4D/几何教师、离线策略排序与淘汰、有本体锚定的数据/后训练，以及明确物理变量下的 what-if 检查；在线预演、直接控制和安全裁决需要逐级更强的真实闭环证据。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 6 |
| `conditional` | 条件成立 | 8 |
| `limit` | 限制/负面 | 1 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2602.23814: Action-Geometry Prediction with 3D Geometric Prior for Bimanual Manipulation | 2026-02-27 | support | EA-ACTRT-2026-0003 |
| 2603.15265: MoE-ACT: Scaling Multi-Task Bimanual Manipulation with Sparse Language-Conditioned Mixture-of-Experts Transformers | 2026-03-16 | support | EA-ACTRT-2026-0002 |
| 2603.17240: GigaWorld-Policy: An Efficient Action-Centered World--Action Model | 2026-03-18 | conditional | EA-ACTRT-2026-0015 |
| 2604.04161: Adaptive Action Chunking at Inference-time for Vision-Language-Action Models | 2026-04-05 | support | EA-ACTRT-2026-0005 |
| 2605.06222: When to Trust Imagination: Adaptive Action Execution for World Action Models | 2026-05-07 | conditional | EA-ACTRT-2026-0013 |
| 2605.21862: EvoScene-VLA: Evolving Scene Beliefs Inside the Action Decoder for Chunked Robot Control | 2026-05-21 | conditional | EA-ACTRT-2026-0014 |
| 2606.00537: PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking | 2026-05-30 | limit | EA-ACTRT-2026-0001 |
| 2606.01865: Set-Supervised Diffusion Policy: Learning Action-Chunking Diffusion through Corrections | 2026-06-01 | conditional | EA-ACTRT-2026-0010 |
| 2606.03847: Denoising Tells When to Replan: Denoising-Variance Adaptive Chunking for Flow-Based Robot Policies | 2026-06-02 | support | EA-ACTRT-2026-0006 |
| 2606.09811: AHA-WAM:Asynchronous Horizon-Adaptive World-Action Modeling with Observation-Guided Context Routing | 2026-06-08 | support | EA-ACTRT-2026-0007 |
| 2606.11408: Dynamic Execution Horizon Prediction for Chunk-based Robot Policies | 2026-06-09 | conditional | EA-ACTRT-2026-0009 |
| 2606.18589: DREAM-Chunk: Reactive Action Chunking with Latent World Model | 2026-06-17 | conditional | EA-ACTRT-2026-0011 |
| 2606.21600: VQActFlow: Vector-Quantized Action Mode Steering for Multi-Task Robot Manipulation | 2026-06-19 | conditional | EA-ACTRT-2026-0004 |
| 2607.08575: FabriVLA: A Lightweight Vision-Language-Action Model with Conformal Action Chunk Uncertainty | 2026-07-09 | conditional | EA-ACTRT-2026-0008 |
| 2608.03483: Continue or Replan? Bernoulli-Continuation Policy Learning for Adaptive Horizon Execution | 2026-08-04 | support | EA-ACTRT-2026-0012 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-ACTRT-2026-0003 | EA-MODEL | `support` | `direct` | 双臂动作分块可以与未来几何预测联合训练：策略融合 3D 几何潜变量、2D 语义和本体状态，并由扩散模型同时预测未来动作块与可解码的未来 3D 场景潜变量。 | 该方法把预训练 3D 几何基础模型作为 RGB 输入的空间先验，使用统一状态表示联合生成动作块和未来稠密点图，使动作学习显式感知双臂协调与场景几何演化。 (Abstract (full-text section)) | chongyang-xu; haipeng-li; shen-cheng; et al. | 2602.23814 |
| EA-ACTRT-2026-0002 | EA-MODEL | `support` | `direct` | 把 ACT 接入多任务双臂场景时，可在编码器加入稀疏专家路由，并用语言条件 FiLM 与多尺度交叉注意力约束动作解码，从而降低不同任务动作分布的相互干扰。 | MoE-ACT 保留 ACT 的动作分块骨架，以稀疏 MoE 分解多任务潜在动作分布，再用语言条件调制和多尺度视觉融合生成动作序列，并在 RoboTwin 2.0 与真实双臂设置中评测。 (Abstract (full-text section)) | kangjun-guo; haichao-liu; yanji-sun; et al. | 2603.15265 |
| EA-ACTRT-2026-0005 | EA-MODEL | `support` | `direct` | 动作块越长并不总是越好：长块降低闭环反应性，短块增加跨块模式跳变；AAC 用当前预测的动作熵在线调节执行块长度，以平衡一致性与反应性。 | AAC 针对带扩散动作头的 VLA 并行采样候选动作，用动作熵作为不确定性线索，在高不确定阶段缩短块、在低不确定阶段延长块。 (Abstract (full-text section)) | yuanchang-liang; xiaobo-wang; kai-wang; et al. | 2604.04161 |
| EA-ACTRT-2026-0006 | EA-MODEL | `support` | `direct` | 对流匹配动作策略，末端去噪步骤中干净动作估计的方差可作为重规划信号：DVAC 执行低方差稳定前缀，并在高方差未来动作被提交前重新观测与规划。 | DVAC 不增加训练模块，而是利用推理过程已有的去噪轨迹估计未来动作稳定性，并用局部滚动尺度校准阈值，在 RoboTwin、LIBERO、CALVIN 与实机任务中比较成功率和重规划开销。 (Abstract (full-text section)) | xiangdong-feng; yuxuan-cheng; chen-shi; et al. | 2606.03847 |
| EA-ACTRT-2026-0007 | EA-MODEL | `support` | `direct` | 世界预测与动作执行不必保持同一时间分辨率；AHA-WAM 将低频视频规划器与高频短动作块执行器解耦，并通过观测引导的上下文路由在闭环执行时复用长时世界上下文。 | 双 DiT 架构让视频分支维护滚动记忆，动作分支以较高频率查询该上下文并输出短动作块；视界偏移训练支持规划器与执行器不同步。 (Abstract (full-text section)) | jisong-cai; long-ling; shiwei-chu; et al. | 2606.09811 |
| EA-ACTRT-2026-0012 | EA-MODEL | `support` | `direct` | 固定执行视界会把重规划变成与任务阶段无关的周期调度；BCP 把视界选择分解为有序的继续/重规划决策，并用轨迹级强化学习同时优化成功与 VLA 调用效率。 | BCP 在冻结 VLA 上附加轻量 continuation head，复用动作块与视觉语言表征；其有序前缀结构与效率奖励避免把所有候选视界当成互不相关类别或退化为频繁重规划。 (Abstract (full-text section)) | weichen-xu; zhenhua-liu; lin-luo; et al. | 2608.03483 |
| EA-ACTRT-2026-0015 | EA-MODEL | `conditional` | `direct` | 世界动作模型可以在训练时联合学习动作块与未来视频、在部署时只解码动作：GigaWorld-Policy 用因果掩码阻止未来视频 token 反向影响动作 token，使视频生成成为可选推理分支。 | 该动作中心 WAM 以动作预测和视觉动力学共同监督共享模型，同时通过因果设计保留低时延动作解码路径，并在 RoboTwin 2.0 与真实机器人上评估。 (Abstract (full-text section)) | angen-ye; boyuan-wang; chaojun-ni; et al. | 2603.17240 |
| EA-ACTRT-2026-0013 | EA-MODEL | `conditional` | `direct` | 世界动作模型的执行长度可以由“想象—现实一致性”决定：FFDC 联合读取预测动作、预测视觉动态、真实观测和语言，继续执行可信片段并在偏差出现时提前重规划。 | FFDC 将自适应执行表述为未来—现实验证问题，使长视界效率与接触阶段反应性不再依赖一个固定块长度，并在 RoboTwin 与实机中同时评估成功、调用次数和时延。 (Abstract (full-text section)) | rui-wang; yue-zhang; jiehong-lin; et al. | 2605.06222 |
| EA-ACTRT-2026-0014 | EA-MODEL | `conditional` | `direct` | 跨动作块闭环控制需要保留由机器人自身动作更新的场景状态；EvoScene-VLA 让动作解码器同时输出动作块和紧凑场景更新，并在下一次视觉调用中用新观测校正这一先验。 | 循环场景前缀把上一块动作导致的接触、遮挡和物体移动带入下一控制调用；训练时用几何锚点与未来场景目标监督，部署时移除教师模块。 (Abstract (full-text section)) | chushan-zhang; ruihan-lu; jinguang-tong; et al. | 2605.21862 |
| EA-ACTRT-2026-0010 | EA-MODEL | `conditional` | `direct` | 交互纠错可从单步监督扩展到动作块集合监督：Set-Supervised Diffusion Policy 将正负动作块逐时刻构造成期望动作集合，再训练扩散策略生成落入该集合的动作块。 | 该方法不把一次人工纠错当作唯一精确标签，而是由正负动作对定义可接受动作区域，并用多次纠错逐步收紧动作块监督。 (IV-B Extending Desired Action Set to Action-Chunks) | zhaoting-li; gang-chen; javier-alonso-mora; et al. | 2606.01865 |
| EA-ACTRT-2026-0009 | EA-MODEL | `conditional` | `direct` | 执行视界可以由冻结动作策略之外的轻量模块学习：DEHP 用在线强化学习根据当前观测和预测动作块决定何时重规划，并在精细阶段缩短视界、自由空间运动中延长视界。 | DEHP 将动作生成与执行时机分离，只训练视界预测分支，从而能在不改基础行为克隆策略权重的情况下检验动态重规划的增益。 (Abstract (full-text section)) | yuchi-zhao; miroslav-bogdanovic; arjun-sohal; et al. | 2606.11408 |
| EA-ACTRT-2026-0011 | EA-MODEL | `conditional` | `direct` | 长动作块的开环脆弱性可以在块内缓解：DREAM-Chunk 并行采样多个候选动作块，用轻量潜在世界模型预测各自未来，并依据预测潜状态与真实观测的匹配在线选择动作。 | DREAM-Chunk 不微调基础策略，而用额外测试时计算维持多个可能轨迹，使机器人在随机动力学、执行误差和部分可观测条件下能够块内反应。 (Abstract (full-text section)) | wenxi-chen; kaidi-zhang; chi-lin; et al. | 2606.18589 |
| EA-ACTRT-2026-0004 | EA-MODEL | `conditional` | `direct` | 多任务动作分块不必只在连续空间直接回归；VQActFlow 先把动作块编码为离散代码，再用变分流匹配生成代码序列，使语言任务模式与场景可行性可以在推理时分别施加引导。 | 离散代码簿显式分离多模态动作模式，语言条件的 classifier-free guidance 选择任务模式，代码簿 critic 补充场景可行性信号。 (Abstract (full-text section)) | zhigen-zhao; mark-leggiero; yipu-chen; et al. | 2606.21600 |
| EA-ACTRT-2026-0008 | EA-MODEL | `conditional` | `direct` | 动作块的不确定性可以按“整个将执行前缀”联合校准，而非只估计单步误差；JCAC 为冻结策略增加轻量残差尺度头并输出具有用户指定覆盖水平的动作块集合。 | FabriVLA 的 JCAC 使用单次策略查询生成联合共形集合，可在动作执行前对整段前缀进行风险排序，为闭环部署增加可审计的不确定性接口。 (Abstract (full-text section)) | shiyuan-yang; borong-zhang; jizheng-zhang; et al. | 2607.08575 |
| EA-ACTRT-2026-0001 | EA-MODEL | `limit` | `direct` | 动作分块策略的预测长度与实际执行长度应分开配置；在 RoboTwin 2.0 等闭环任务中，固定执行视界具有任务依赖且非单调的风险，PACE 以动作速度曲线中的低速相位边界在线选择重规划点。 | PACE 只读取策略已经生成的动作块，以低速谷值标记阶段切换，在连贯运动中保持较长执行、在接触或阶段转换前更早重规划，不修改也不重训基础策略。 (Abstract (full-text section)) | junnan-nie; jiayi-li; jiachen-zhang; et al. | 2606.00537 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-ACTRT-2026-0003 | chongyang-xu; haipeng-li; shen-cheng; et al. | unlisted | `support` | 双臂动作分块可以与未来几何预测联合训练：策略融合 3D 几何潜变量、2D 语义和本体状态，并由扩散模型同时预测未来动作块与可解码的未来 3D 场景潜变量。 |
| EA-ACTRT-2026-0002 | kangjun-guo; haichao-liu; yanji-sun; et al. | unlisted | `support` | 把 ACT 接入多任务双臂场景时，可在编码器加入稀疏专家路由，并用语言条件 FiLM 与多尺度交叉注意力约束动作解码，从而降低不同任务动作分布的相互干扰。 |
| EA-ACTRT-2026-0005 | yuanchang-liang; xiaobo-wang; kai-wang; et al. | unlisted | `support` | 动作块越长并不总是越好：长块降低闭环反应性，短块增加跨块模式跳变；AAC 用当前预测的动作熵在线调节执行块长度，以平衡一致性与反应性。 |
| EA-ACTRT-2026-0006 | xiangdong-feng; yuxuan-cheng; chen-shi; et al. | unlisted | `support` | 对流匹配动作策略，末端去噪步骤中干净动作估计的方差可作为重规划信号：DVAC 执行低方差稳定前缀，并在高方差未来动作被提交前重新观测与规划。 |
| EA-ACTRT-2026-0007 | jisong-cai; long-ling; shiwei-chu; et al. | unlisted | `support` | 世界预测与动作执行不必保持同一时间分辨率；AHA-WAM 将低频视频规划器与高频短动作块执行器解耦，并通过观测引导的上下文路由在闭环执行时复用长时世界上下文。 |
| EA-ACTRT-2026-0012 | weichen-xu; zhenhua-liu; lin-luo; et al. | unlisted | `support` | 固定执行视界会把重规划变成与任务阶段无关的周期调度；BCP 把视界选择分解为有序的继续/重规划决策，并用轨迹级强化学习同时优化成功与 VLA 调用效率。 |
| EA-ACTRT-2026-0015 | angen-ye; boyuan-wang; chaojun-ni; et al. | unlisted | `conditional` | 世界动作模型可以在训练时联合学习动作块与未来视频、在部署时只解码动作：GigaWorld-Policy 用因果掩码阻止未来视频 token 反向影响动作 token，使视频生成成为可选推理分支。 |
| EA-ACTRT-2026-0013 | rui-wang; yue-zhang; jiehong-lin; et al. | unlisted | `conditional` | 世界动作模型的执行长度可以由“想象—现实一致性”决定：FFDC 联合读取预测动作、预测视觉动态、真实观测和语言，继续执行可信片段并在偏差出现时提前重规划。 |
| EA-ACTRT-2026-0014 | chushan-zhang; ruihan-lu; jinguang-tong; et al. | unlisted | `conditional` | 跨动作块闭环控制需要保留由机器人自身动作更新的场景状态；EvoScene-VLA 让动作解码器同时输出动作块和紧凑场景更新，并在下一次视觉调用中用新观测校正这一先验。 |
| EA-ACTRT-2026-0010 | zhaoting-li; gang-chen; javier-alonso-mora; et al. | unlisted | `conditional` | 交互纠错可从单步监督扩展到动作块集合监督：Set-Supervised Diffusion Policy 将正负动作块逐时刻构造成期望动作集合，再训练扩散策略生成落入该集合的动作块。 |
| EA-ACTRT-2026-0009 | yuchi-zhao; miroslav-bogdanovic; arjun-sohal; et al. | unlisted | `conditional` | 执行视界可以由冻结动作策略之外的轻量模块学习：DEHP 用在线强化学习根据当前观测和预测动作块决定何时重规划，并在精细阶段缩短视界、自由空间运动中延长视界。 |
| EA-ACTRT-2026-0011 | wenxi-chen; kaidi-zhang; chi-lin; et al. | unlisted | `conditional` | 长动作块的开环脆弱性可以在块内缓解：DREAM-Chunk 并行采样多个候选动作块，用轻量潜在世界模型预测各自未来，并依据预测潜状态与真实观测的匹配在线选择动作。 |
| EA-ACTRT-2026-0004 | zhigen-zhao; mark-leggiero; yipu-chen; et al. | unlisted | `conditional` | 多任务动作分块不必只在连续空间直接回归；VQActFlow 先把动作块编码为离散代码，再用变分流匹配生成代码序列，使语言任务模式与场景可行性可以在推理时分别施加引导。 |
| EA-ACTRT-2026-0008 | shiyuan-yang; borong-zhang; jizheng-zhang; et al. | unlisted | `conditional` | 动作块的不确定性可以按“整个将执行前缀”联合校准，而非只估计单步误差；JCAC 为冻结策略增加轻量残差尺度头并输出具有用户指定覆盖水平的动作块集合。 |
| EA-ACTRT-2026-0001 | junnan-nie; jiayi-li; jiachen-zhang; et al. | unlisted | `limit` | 动作分块策略的预测长度与实际执行长度应分开配置；在 RoboTwin 2.0 等闭环任务中，固定执行视界具有任务依赖且非单调的风险，PACE 以动作速度曲线中的低速相位边界在线选择重规划点。 |

## Synthesis Slots

### 共识/正向证据
- `EA-ACTRT-2026-0003`: 双臂动作分块可以与未来几何预测联合训练：策略融合 3D 几何潜变量、2D 语义和本体状态，并由扩散模型同时预测未来动作块与可解码的未来 3D 场景潜变量。
- `EA-ACTRT-2026-0002`: 把 ACT 接入多任务双臂场景时，可在编码器加入稀疏专家路由，并用语言条件 FiLM 与多尺度交叉注意力约束动作解码，从而降低不同任务动作分布的相互干扰。
- `EA-ACTRT-2026-0005`: 动作块越长并不总是越好：长块降低闭环反应性，短块增加跨块模式跳变；AAC 用当前预测的动作熵在线调节执行块长度，以平衡一致性与反应性。
- `EA-ACTRT-2026-0006`: 对流匹配动作策略，末端去噪步骤中干净动作估计的方差可作为重规划信号：DVAC 执行低方差稳定前缀，并在高方差未来动作被提交前重新观测与规划。
- `EA-ACTRT-2026-0007`: 世界预测与动作执行不必保持同一时间分辨率；AHA-WAM 将低频视频规划器与高频短动作块执行器解耦，并通过观测引导的上下文路由在闭环执行时复用长时世界上下文。
- `EA-ACTRT-2026-0012`: 固定执行视界会把重规划变成与任务阶段无关的周期调度；BCP 把视界选择分解为有序的继续/重规划决策，并用轨迹级强化学习同时优化成功与 VLA 调用效率。
### 条件成立
- `EA-ACTRT-2026-0015`: 世界动作模型可以在训练时联合学习动作块与未来视频、在部署时只解码动作：GigaWorld-Policy 用因果掩码阻止未来视频 token 反向影响动作 token，使视频生成成为可选推理分支。
- `EA-ACTRT-2026-0013`: 世界动作模型的执行长度可以由“想象—现实一致性”决定：FFDC 联合读取预测动作、预测视觉动态、真实观测和语言，继续执行可信片段并在偏差出现时提前重规划。
- `EA-ACTRT-2026-0014`: 跨动作块闭环控制需要保留由机器人自身动作更新的场景状态；EvoScene-VLA 让动作解码器同时输出动作块和紧凑场景更新，并在下一次视觉调用中用新观测校正这一先验。
- `EA-ACTRT-2026-0010`: 交互纠错可从单步监督扩展到动作块集合监督：Set-Supervised Diffusion Policy 将正负动作块逐时刻构造成期望动作集合，再训练扩散策略生成落入该集合的动作块。
- `EA-ACTRT-2026-0009`: 执行视界可以由冻结动作策略之外的轻量模块学习：DEHP 用在线强化学习根据当前观测和预测动作块决定何时重规划，并在精细阶段缩短视界、自由空间运动中延长视界。
- `EA-ACTRT-2026-0011`: 长动作块的开环脆弱性可以在块内缓解：DREAM-Chunk 并行采样多个候选动作块，用轻量潜在世界模型预测各自未来，并依据预测潜状态与真实观测的匹配在线选择动作。
- `EA-ACTRT-2026-0004`: 多任务动作分块不必只在连续空间直接回归；VQActFlow 先把动作块编码为离散代码，再用变分流匹配生成代码序列，使语言任务模式与场景可行性可以在推理时分别施加引导。
- `EA-ACTRT-2026-0008`: 动作块的不确定性可以按“整个将执行前缀”联合校准，而非只估计单步误差；JCAC 为冻结策略增加轻量残差尺度头并输出具有用户指定覆盖水平的动作块集合。
### 限制与失败模式
- `EA-ACTRT-2026-0001`: 动作分块策略的预测长度与实际执行长度应分开配置；在 RoboTwin 2.0 等闭环任务中，固定执行视界具有任务依赖且非单调的风险，PACE 以动作速度曲线中的低速相位边界在线选择重规划点。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-ACTRT-2026-0003` 双臂动作分块可以与未来几何预测联合训练：策略融合 3D 几何潜变量、2D 语义和本体状态，并由扩散模型同时预测未来动作块与可解码的未来 3D 场景潜变量。
  - `EA-ACTRT-2026-0002` 把 ACT 接入多任务双臂场景时，可在编码器加入稀疏专家路由，并用语言条件 FiLM 与多尺度交叉注意力约束动作解码，从而降低不同任务动作分布的相互干扰。
  - `EA-ACTRT-2026-0005` 动作块越长并不总是越好：长块降低闭环反应性，短块增加跨块模式跳变；AAC 用当前预测的动作熵在线调节执行块长度，以平衡一致性与反应性。
- Scientific memo preview: 《ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测: 先看证据边界，再谈一个可传播的反常识洞察。

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
