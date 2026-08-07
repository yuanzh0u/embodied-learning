# Evidence Appendix: ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测

- Time range: 2026-02-07..2026-08-07
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-ACTRT-2026-0003

- Claim: 双臂动作分块可以与未来几何预测联合训练：策略融合 3D 几何潜变量、2D 语义和本体状态，并由扩散模型同时预测未来动作块与可解码的未来 3D 场景潜变量。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.23814](https://arxiv.org/abs/2602.23814) Action-Geometry Prediction with 3D Geometric Prior for Bimanual Manipulation
- Locator: Abstract (full-text section)
- Evidence: 该方法把预训练 3D 几何基础模型作为 RGB 输入的空间先验，使用统一状态表示联合生成动作块和未来稠密点图，使动作学习显式感知双臂协调与场景几何演化。
- Quote: “Abstract Bimanual manipulation requires policies that can reason about 3D geometry, anticipate how it evolves under action, and generate smooth, coordinated motions. However, existing methods typically rely on 2D features with limited spatial awareness, or require explicit point clouds that are difficult to obtain reliably in real-world settings. At the same time, recent 3D geometric foundation models show that accurate and diverse 3D structure can be reconstructed directly from RGB images in a”
- Authors: chongyang-xu; haipeng-li; shen-cheng; et al.

### EA-ACTRT-2026-0002

- Claim: 把 ACT 接入多任务双臂场景时，可在编码器加入稀疏专家路由，并用语言条件 FiLM 与多尺度交叉注意力约束动作解码，从而降低不同任务动作分布的相互干扰。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.15265](https://arxiv.org/abs/2603.15265) MoE-ACT: Scaling Multi-Task Bimanual Manipulation with Sparse Language-Conditioned Mixture-of-Experts Transformers
- Locator: Abstract (full-text section)
- Evidence: MoE-ACT 保留 ACT 的动作分块骨架，以稀疏 MoE 分解多任务潜在动作分布，再用语言条件调制和多尺度视觉融合生成动作序列，并在 RoboTwin 2.0 与真实双臂设置中评测。
- Quote: “Abstract The ability of robots to handle multiple tasks under a unified policy is critical for deploying embodied intelligence in real-world household and industrial applications. However, out-of-distribution variation across tasks often causes severe task interference and negative transfer when training general robotic policies. To address this challenge, we propose a lightweight multi-task imitation learning framework for bimanual manipulation, termed Mixture-of-Experts-Enhanced Action Chunkin”
- Authors: kangjun-guo; haichao-liu; yanji-sun; et al.

### EA-ACTRT-2026-0005

- Claim: 动作块越长并不总是越好：长块降低闭环反应性，短块增加跨块模式跳变；AAC 用当前预测的动作熵在线调节执行块长度，以平衡一致性与反应性。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.04161](https://arxiv.org/abs/2604.04161) Adaptive Action Chunking at Inference-time for Vision-Language-Action Models
- Locator: Abstract (full-text section)
- Evidence: AAC 针对带扩散动作头的 VLA 并行采样候选动作，用动作熵作为不确定性线索，在高不确定阶段缩短块、在低不确定阶段延长块。
- Quote: “Abstract In Vision-Language-Action (VLA) models, action chunking ( i.e. , executing a sequence of actions without intermediate replanning) is a key technique to improve robotic manipulation abilities. However, a large chunk size reduces the model’s responsiveness to new information, while a small one increases the likelihood of mode-jumping, jerky behavior resulting from discontinuities between chunks. Therefore, selecting the optimal chunk size is an urgent demand to balance the model’s reactiv”
- Authors: yuanchang-liang; xiaobo-wang; kai-wang; et al.

### EA-ACTRT-2026-0006

- Claim: 对流匹配动作策略，末端去噪步骤中干净动作估计的方差可作为重规划信号：DVAC 执行低方差稳定前缀，并在高方差未来动作被提交前重新观测与规划。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.03847](https://arxiv.org/abs/2606.03847) Denoising Tells When to Replan: Denoising-Variance Adaptive Chunking for Flow-Based Robot Policies
- Locator: Abstract (full-text section)
- Evidence: DVAC 不增加训练模块，而是利用推理过程已有的去噪轨迹估计未来动作稳定性，并用局部滚动尺度校准阈值，在 RoboTwin、LIBERO、CALVIN 与实机任务中比较成功率和重规划开销。
- Quote: “Abstract Action chunking has become a common inference strategy for flow-based robot policies, improving action coherence by modeling multi-step temporal dependencies in demonstrations. However, the execution horizon is still typically set as an empirical fixed value, overlooking that predictable free-space motions and precision-critical interaction phases often require different replanning frequencies. In this work, we first show that the denoising process of flow-based policies contains an int”
- Authors: xiangdong-feng; yuxuan-cheng; chen-shi; et al.

### EA-ACTRT-2026-0007

- Claim: 世界预测与动作执行不必保持同一时间分辨率；AHA-WAM 将低频视频规划器与高频短动作块执行器解耦，并通过观测引导的上下文路由在闭环执行时复用长时世界上下文。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.09811](https://arxiv.org/abs/2606.09811) AHA-WAM:Asynchronous Horizon-Adaptive World-Action Modeling with Observation-Guided Context Routing
- Locator: Abstract (full-text section)
- Evidence: 双 DiT 架构让视频分支维护滚动记忆，动作分支以较高频率查询该上下文并输出短动作块；视界偏移训练支持规划器与执行器不同步。
- Quote: “Abstract World-action models have emerged as a promising paradigm for robot manipulation, jointly modeling visual scene dynamics and actions to inject physical priors into policy learning. However, existing world-action models couple world prediction and action execution at the same temporal resolution, forcing the world branch to model near-term frame variations that are redundant and weakly informative. We posit that strictly binding world prediction and action execution to the same temporal r”
- Authors: jisong-cai; long-ling; shiwei-chu; et al.

### EA-ACTRT-2026-0012

- Claim: 固定执行视界会把重规划变成与任务阶段无关的周期调度；BCP 把视界选择分解为有序的继续/重规划决策，并用轨迹级强化学习同时优化成功与 VLA 调用效率。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.03483](https://arxiv.org/abs/2608.03483) Continue or Replan? Bernoulli-Continuation Policy Learning for Adaptive Horizon Execution
- Locator: Abstract (full-text section)
- Evidence: BCP 在冻结 VLA 上附加轻量 continuation head，复用动作块与视觉语言表征；其有序前缀结构与效率奖励避免把所有候选视界当成互不相关类别或退化为频繁重规划。
- Quote: “Abstract Existing chunk-based Vision-Language-Action (VLA) models execute a fixed number of actions (i.e., execution horizon) before replanning, turning replanning into a task-agnostic periodic schedule that is independent of task progress. As a result, when no replanning boundary falls before a critical manipulation stage, it is executed from a stale chunk rather than a freshly replanned one. To address this limitation, we propose B ernoulli- C ontinuation P olicy ( BCP ), a lightweight, plug-a”
- Authors: weichen-xu; zhenhua-liu; lin-luo; et al.

### EA-ACTRT-2026-0015

- Claim: 世界动作模型可以在训练时联合学习动作块与未来视频、在部署时只解码动作：GigaWorld-Policy 用因果掩码阻止未来视频 token 反向影响动作 token，使视频生成成为可选推理分支。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.17240](https://arxiv.org/abs/2603.17240) GigaWorld-Policy: An Efficient Action-Centered World--Action Model
- Locator: Abstract (full-text section)
- Evidence: 该动作中心 WAM 以动作预测和视觉动力学共同监督共享模型，同时通过因果设计保留低时延动作解码路径，并在 RoboTwin 2.0 与真实机器人上评估。
- Quote: “Abstract World–Action Models (WAM) initialized from pre-trained video generation backbones have demonstrated remarkable potential for robot policy learning. However, existing approaches face two critical bottlenecks that hinder performance and deployment. First, jointly reasoning over future visual dynamics and corresponding actions incurs substantial inference overhead. Second, joint modeling often entangles visual and motion representations, making motion prediction accuracy heavily dependent”
- Authors: angen-ye; boyuan-wang; chaojun-ni; et al.

### EA-ACTRT-2026-0013

- Claim: 世界动作模型的执行长度可以由“想象—现实一致性”决定：FFDC 联合读取预测动作、预测视觉动态、真实观测和语言，继续执行可信片段并在偏差出现时提前重规划。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.06222](https://arxiv.org/abs/2605.06222) When to Trust Imagination: Adaptive Action Execution for World Action Models
- Locator: Abstract (full-text section)
- Evidence: FFDC 将自适应执行表述为未来—现实验证问题，使长视界效率与接触阶段反应性不再依赖一个固定块长度，并在 RoboTwin 与实机中同时评估成功、调用次数和时延。
- Quote: “Abstract World Action Models (WAMs) have recently emerged as a promising paradigm for robotic manipulation by jointly predicting future visual observations and future actions. However, current WAMs typically execute a fixed number of predicted actions after each model inference, leaving the robot blind to whether the imagined future remains consistent with the actual physical rollout. In this work, we formulate adaptive WAM execution as a future–reality verification problem: the robot should exe”
- Authors: rui-wang; yue-zhang; jiehong-lin; et al.

### EA-ACTRT-2026-0014

- Claim: 跨动作块闭环控制需要保留由机器人自身动作更新的场景状态；EvoScene-VLA 让动作解码器同时输出动作块和紧凑场景更新，并在下一次视觉调用中用新观测校正这一先验。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.21862](https://arxiv.org/abs/2605.21862) EvoScene-VLA: Evolving Scene Beliefs Inside the Action Decoder for Chunked Robot Control
- Locator: Abstract (full-text section)
- Evidence: 循环场景前缀把上一块动作导致的接触、遮挡和物体移动带入下一控制调用；训练时用几何锚点与未来场景目标监督，部署时移除教师模块。
- Quote: “Abstract Chunked vision-language-action (VLA) policies predict multi-step robot controls, conditioning each update on the current visual observation alone. Yet robot actions cause contact, occlusion, and object motion, and the geometry that later decisions depend on can change before the next visual update arrives. Spatial VLAs improve current-frame geometry. Temporal VLAs aggregate past frames. Neither maintains an action-updated scene prior across chunks. We argue for a persistent action-updat”
- Authors: chushan-zhang; ruihan-lu; jinguang-tong; et al.

### EA-ACTRT-2026-0010

- Claim: 交互纠错可从单步监督扩展到动作块集合监督：Set-Supervised Diffusion Policy 将正负动作块逐时刻构造成期望动作集合，再训练扩散策略生成落入该集合的动作块。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.01865](https://arxiv.org/abs/2606.01865) Set-Supervised Diffusion Policy: Learning Action-Chunking Diffusion through Corrections
- Locator: IV-B Extending Desired Action Set to Action-Chunks
- Evidence: 该方法不把一次人工纠错当作唯一精确标签，而是由正负动作对定义可接受动作区域，并用多次纠错逐步收紧动作块监督。
- Quote: “CLIC [ 19 ] shows that imitating a set of desired actions, constructed by a pair of positive and negative actions, achieves more robust behavior than imitating only the positive action. Building on this idea, we generalize the single-step desired action set to action-chunks. At step , under observation , we denote a positive and negative action-chunk as Given and the preceding positive actions , the action is better than for all . As we consider demonstration data or intervention feedback, to ma”
- Authors: zhaoting-li; gang-chen; javier-alonso-mora; et al.

### EA-ACTRT-2026-0009

- Claim: 执行视界可以由冻结动作策略之外的轻量模块学习：DEHP 用在线强化学习根据当前观测和预测动作块决定何时重规划，并在精细阶段缩短视界、自由空间运动中延长视界。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.11408](https://arxiv.org/abs/2606.11408) Dynamic Execution Horizon Prediction for Chunk-based Robot Policies
- Locator: Abstract (full-text section)
- Evidence: DEHP 将动作生成与执行时机分离，只训练视界预测分支，从而能在不改基础行为克隆策略权重的情况下检验动态重规划的增益。
- Quote: “Abstract Action chunking has become a standard design in modern robot policies, from diffusion/flow policies to vision-language-action models, where the policy predicts a sequence of actions and executes a fixed number of them instead of acting one step at a time. However, this paradigm relies on a key assumption: a fixed execution horizon. During chunk execution, the policy operates open-loop, which is particularly problematic for fine-grained manipulation tasks that require frequent replanning”
- Authors: yuchi-zhao; miroslav-bogdanovic; arjun-sohal; et al.

### EA-ACTRT-2026-0011

- Claim: 长动作块的开环脆弱性可以在块内缓解：DREAM-Chunk 并行采样多个候选动作块，用轻量潜在世界模型预测各自未来，并依据预测潜状态与真实观测的匹配在线选择动作。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.18589](https://arxiv.org/abs/2606.18589) DREAM-Chunk: Reactive Action Chunking with Latent World Model
- Locator: Abstract (full-text section)
- Evidence: DREAM-Chunk 不微调基础策略，而用额外测试时计算维持多个可能轨迹，使机器人在随机动力学、执行误差和部分可观测条件下能够块内反应。
- Quote: “Abstract Action chunking has become a common interface for vision-language-action (VLA) models, enabling low-frequency policy inference to drive high-frequency robot execution. However, once a chunk is committed, its open-loop execution can be brittle under stochastic dynamics, hardware execution errors, and partially observed state. We propose DREAM-Chunk , a test-time scaling method that augments chunking-based policies with a lightweight latent world model without requiring additional policy”
- Authors: wenxi-chen; kaidi-zhang; chi-lin; et al.

### EA-ACTRT-2026-0004

- Claim: 多任务动作分块不必只在连续空间直接回归；VQActFlow 先把动作块编码为离散代码，再用变分流匹配生成代码序列，使语言任务模式与场景可行性可以在推理时分别施加引导。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.21600](https://arxiv.org/abs/2606.21600) VQActFlow: Vector-Quantized Action Mode Steering for Multi-Task Robot Manipulation
- Locator: Abstract (full-text section)
- Evidence: 离散代码簿显式分离多模态动作模式，语言条件的 classifier-free guidance 选择任务模式，代码簿 critic 补充场景可行性信号。
- Quote: “Abstract Multi-task robot manipulation policies are challenging to learn from demonstration because traditionally a single network must select among qualitatively different action modes from a multimodal demonstration distribution, conditioned on language and visual context. A wrong mode selection means executing the wrong task or an action infeasible in the scene. Tokenizing continuous actions into a learned discrete codebook separates these modes at the representation level, offering structura”
- Authors: zhigen-zhao; mark-leggiero; yipu-chen; et al.

### EA-ACTRT-2026-0008

- Claim: 动作块的不确定性可以按“整个将执行前缀”联合校准，而非只估计单步误差；JCAC 为冻结策略增加轻量残差尺度头并输出具有用户指定覆盖水平的动作块集合。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.08575](https://arxiv.org/abs/2607.08575) FabriVLA: A Lightweight Vision-Language-Action Model with Conformal Action Chunk Uncertainty
- Locator: Abstract (full-text section)
- Evidence: FabriVLA 的 JCAC 使用单次策略查询生成联合共形集合，可在动作执行前对整段前缀进行风险排序，为闭环部署增加可审计的不确定性接口。
- Quote: “Abstract Vision-Language-Action (VLA) models have become a leading paradigm for general purpose robotic manipulation, but their computational cost and limited uncertainty awareness hinder practical deployment. We present FabriVLA, a lightweight VLA that fuses shallow and intermediate VLM layers to preserve fine-grained visual features, and gates self-attention among action tokens so that its flow matching head admits inter step structure only as far as training warrants. Trained end-to-end in a”
- Authors: shiyuan-yang; borong-zhang; jizheng-zhang; et al.

### EA-ACTRT-2026-0001

- Claim: 动作分块策略的预测长度与实际执行长度应分开配置；在 RoboTwin 2.0 等闭环任务中，固定执行视界具有任务依赖且非单调的风险，PACE 以动作速度曲线中的低速相位边界在线选择重规划点。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.00537](https://arxiv.org/abs/2606.00537) PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking
- Locator: Abstract (full-text section)
- Evidence: PACE 只读取策略已经生成的动作块，以低速谷值标记阶段切换，在连贯运动中保持较长执行、在接触或阶段转换前更早重规划，不修改也不重训基础策略。
- Quote: “Abstract Recent vision–language–action and diffusion-based robot policies often use action chunking, where each policy query predicts a sequence of future actions and the robot executes an open-loop prefix before re-querying. While this interface improves local motion continuity, deployment still requires choosing the execution horizon : how much of each predicted chunk should be executed before acquiring a new observation. However, our experiments show that success is strongly task-dependent an”
- Authors: junnan-nie; jiayi-li; jiachen-zhang; et al.

## References

- `2602.23814` [Action-Geometry Prediction with 3D Geometric Prior for Bimanual Manipulation](https://arxiv.org/abs/2602.23814) (2026-02-27)
- `2603.15265` [MoE-ACT: Scaling Multi-Task Bimanual Manipulation with Sparse Language-Conditioned Mixture-of-Experts Transformers](https://arxiv.org/abs/2603.15265) (2026-03-16)
- `2603.17240` [GigaWorld-Policy: An Efficient Action-Centered World--Action Model](https://arxiv.org/abs/2603.17240) (2026-03-18)
- `2604.04161` [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](https://arxiv.org/abs/2604.04161) (2026-04-05)
- `2605.06222` [When to Trust Imagination: Adaptive Action Execution for World Action Models](https://arxiv.org/abs/2605.06222) (2026-05-07)
- `2605.21862` [EvoScene-VLA: Evolving Scene Beliefs Inside the Action Decoder for Chunked Robot Control](https://arxiv.org/abs/2605.21862) (2026-05-21)
- `2606.00537` [PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking](https://arxiv.org/abs/2606.00537) (2026-05-30)
- `2606.01865` [Set-Supervised Diffusion Policy: Learning Action-Chunking Diffusion through Corrections](https://arxiv.org/abs/2606.01865) (2026-06-01)
- `2606.03847` [Denoising Tells When to Replan: Denoising-Variance Adaptive Chunking for Flow-Based Robot Policies](https://arxiv.org/abs/2606.03847) (2026-06-02)
- `2606.09811` [AHA-WAM:Asynchronous Horizon-Adaptive World-Action Modeling with Observation-Guided Context Routing](https://arxiv.org/abs/2606.09811) (2026-06-08)
- `2606.11408` [Dynamic Execution Horizon Prediction for Chunk-based Robot Policies](https://arxiv.org/abs/2606.11408) (2026-06-09)
- `2606.18589` [DREAM-Chunk: Reactive Action Chunking with Latent World Model](https://arxiv.org/abs/2606.18589) (2026-06-17)
- `2606.21600` [VQActFlow: Vector-Quantized Action Mode Steering for Multi-Task Robot Manipulation](https://arxiv.org/abs/2606.21600) (2026-06-19)
- `2607.08575` [FabriVLA: A Lightweight Vision-Language-Action Model with Conformal Action Chunk Uncertainty](https://arxiv.org/abs/2607.08575) (2026-07-09)
- `2608.03483` [Continue or Replan? Bernoulli-Continuation Policy Learning for Adaptive Horizon Execution](https://arxiv.org/abs/2608.03483) (2026-08-04)
