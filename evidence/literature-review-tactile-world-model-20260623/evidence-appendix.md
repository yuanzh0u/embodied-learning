# Evidence Appendix: 触觉世界模型

- Time range: 2025-12-23..2026-06-23
- Events: 18
- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。

### EA-TWM-2026-0005

- Claim: 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19201](https://arxiv.org/abs/2603.19201) OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation
- Locator: Figure 2; Section III The OmniViTac Dataset; Section III-A Hardware Setup and Data Collection System
- Evidence: OmniVTA 提出 OmniViTac 数据集，包含 21,879 条轨迹、86 个任务、126 个对象，覆盖擦拭、剥离、切割、抓取、装配、手内调整等六类物理接触模式，并使用 RGB-D、高频触觉和动作数据；系统支持多种触觉传感器并做时间对齐、可视化和人工核验。
- Authors: yuhang-zheng

### EA-TWM-2026-0014

- Claim: 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.07335](https://arxiv.org/abs/2604.07335) TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks
- Locator: Abstract; Section III-C Feasibility-Aware Data Acquisition Pipeline; Section III-D Pyramid-Structured Data Regime; Section IV Experiments
- Evidence: TAMEn 提出双模式采集管线：MoCap 精准模式和 VR in-the-wild 模式，并引入 feasibility-aware acquisition、触觉可视化 recovery teleoperation 和金字塔数据 regime；论文报告平均任务成功率从 34% 提升到 75%，且 tactile pretraining 从 55% 进一步到 65%。
- Authors: longyan-wu

### EA-TWM-2026-0013

- Claim: 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: Abstract; Section 3.1 Dataset Statistics; Section 3.2 Synchronization and Data Quality Control; Section 4 Data Collection Platform
- Evidence: HapTile 包含 1,726 条演示、38 个任务、9 类操作技能，由 9 名操作者通过带 haptic feedback 的遥操作接口采集；每条演示含语言指令、同步视觉、触觉、机器人状态和动作轨迹，15Hz 采样，总交互时长 750.33 分钟。
- Authors: amirhosein-alian

### EA-TWM-2026-0004

- Claim: 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.06001](https://arxiv.org/abs/2602.06001) Visuo-Tactile World Models
- Locator: Appendix B.0.1 Training Dataset; Appendix E Limitations
- Evidence: 该论文训练数据包含 124 条遥操作演示、约 112k datapoints、8 个接触丰富任务、成功与失败演示、proprioception、外部视频和四个 Digit 360 指尖视频，并通过时间戳同步后降采样到 6 FPS；限制部分说明评测主要在同场景同对象，触觉模态限于 Digit 360，CEM 规划成本高且以开环 action chunk 执行。
- Authors: carolina-higuera

### EA-TWM-2026-0008

- Claim: 触觉世界模型必须在扰动与恢复数据上评估，否则会高估接触丰富任务的稳定性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: Section IV-B Experimental Setup; Section IV-C Results; Section IV-D Ablation
- Evidence: TacForeSight 在五个任务和三类 in-process perturbation 上评测，并纳入 recovery demonstrations；完整模型平均成功率 79.0%，扰动设置平均 86.7%，去掉预测触觉或简单拼接力触觉都会削弱表现。
- Authors: yujie-zang

### EA-TWM-2026-0001

- Claim: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13877](https://arxiv.org/abs/2606.13877) ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation
- Locator: Abstract; Section 2.2 Sensory Modalities and Representation Structure; Section 3 What Representation Properties Matter
- Evidence: ContactWorld 在 12 个接触丰富任务上比较视觉与触觉表征；点云把平均规划成功率从腕部视角 20.7% 和前视 22.0% 提升到 32.1%，点云加触觉力场进一步到 36.1%。作者强调触觉效果取决于跨模态表征兼容，而非模态数量本身。
- Authors: zhiyuan-zhang

### EA-TWM-2026-0010

- Claim: 在触觉世界动作模型中，触觉融合需要对接触事件做门控，否则会把稀疏、事件驱动的触觉信号当作持续视觉信号处理。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: Abstract; Section 4.2 Performance on Real-World Experiments; Section 4.4 Contact Gate Behavior
- Evidence: Dream-Tac 的接触门控和 contact-aware attention 只在触觉变化明显时增强跨模态作用；作者报告六个真实接触丰富任务平均成功率 83.3%，高于 Cosmos-Policy 51.7%、ForceVLA 50.8% 等，并报告训练最高 2.9 倍、推理最高 1.8 倍加速。
- Authors: yunfan-lou

### EA-TWM-2026-0002

- Claim: 触觉在长时域规划中更重要，但在真实机器人上会受到触觉标定、深度与力推断噪声、预训练编码器兼容性等条件限制。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.13877](https://arxiv.org/abs/2606.13877) ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation
- Locator: Abstract; Appendix F.2 Tactile Representation Ablation; Appendix G Real-World Experiment
- Evidence: ContactWorld 报告触觉在长时域规划下更能缓解接触不确定性积累；真实阀门旋拧实验中，点云达到 90% 成功率，TacRGB 对图像视角有帮助，但 TacDepth/TacFF 不稳定，作者把差异归因于标记跟踪、深度、力推断和触觉标定噪声。
- Authors: zhiyuan-zhang

### EA-TWM-2026-0012

- Claim: 把触觉世界模型用于推理期修正时，预测误差会累积，且触觉编码器预训练规模仍明显小于现代视觉语言模型。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.14981](https://arxiv.org/abs/2606.14981) Inference-time Policy Steering via Vision and Touch
- Locator: Section 6 Conclusion and Limitations
- Evidence: ViTaL 的限制部分指出，latent world model 的保真度会影响验证，尤其是细微接触事件；触觉 verifier 受限于较小规模触觉编码器预训练，作者认为更大规模触觉预训练可能提升接触推理。
- Authors: yilin-wu

### EA-TWM-2026-0015

- Claim: 触觉表征评测正在扩展到大规模全手触觉和自我中心视觉，但多数评测仍停留在表征层，不能直接证明下游机器人性能。
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.19161](https://arxiv.org/abs/2606.19161) HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision
- Locator: Abstract; Section 3 HT-Bench; Section 6 Limitations and Future Work
- Evidence: HT-Bench 含 10M RGB frames、7.8M tactile frames、226 个任务，评估接触几何、视觉-触觉对齐和未见任务泛化，包括触觉检索、inpainting、vision-to-tactile synthesis 和 multimodal tactile prediction；限制部分说明当前评测不直接测量下游机器人表现。
- Authors: yuzhe-huang

### EA-TWM-2026-0003

- Claim: 把触觉作为接触 grounding 信号注入世界模型，可以改善被遮挡或视觉混淆场景中的物体持续性、物理一致性和零样本接触规划。
- Stance: `support` | Confidence: `direct`
- Paper: [2602.06001](https://arxiv.org/abs/2602.06001) Visuo-Tactile World Models
- Locator: Abstract; Section 3.1 What vision does not see; Section 3.2 Visuo-Tactile World Model
- Evidence: Visuo-Tactile World Models 使用外部视觉 latent、Digit 360 触觉 latent 和动作条件 transformer 预测未来；论文报告触觉 grounding 带来物体持续性 +33%、物理规律符合度 +29%，并在真实机器人接触丰富规划中最高提升 +35% 成功率。
- Authors: carolina-higuera

### EA-TWM-2026-0006

- Claim: 触觉世界模型的落地形态正在从被动观测转向预测接触演化并驱动快速反射式控制。
- Stance: `support` | Confidence: `direct`
- Paper: [2603.19201](https://arxiv.org/abs/2603.19201) OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation
- Locator: Abstract; Section I Introduction; Section IV Method; Section VI Conclusion
- Evidence: OmniVTA 由自监督触觉编码器、双流视觉-触觉世界模型、接触感知融合策略和 60Hz reflexive latent tactile controller 组成；作者称模型预测短时域接触演化，并在预测与观测触觉信号偏离时修正动作。
- Authors: yuhang-zheng

### EA-TWM-2026-0009

- Claim: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.08737](https://arxiv.org/abs/2606.08737) Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
- Locator: Abstract; Section 3.2 Dream-Tac Architecture; Section 3.4 Training Objective
- Evidence: Dream-Tac 把 world action model 扩展到触觉，联合建模当前视觉、触觉、语言指令下的未来视觉观测、未来触觉观测和动作 chunk，并加入 contact-gated visuotactile fusion 与 contact-aware attention bias。
- Authors: yunfan-lou

### EA-TWM-2026-0007

- Claim: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.11184](https://arxiv.org/abs/2606.11184) TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
- Locator: Abstract; Section III-A TacForceWM; Section IV-D Ablation
- Evidence: TacForeSight 的 TacForceWM 从双指触觉观测出发，以高频腕部 force/torque 为条件预测短时域触觉 latent dynamics；ablation 中 wrist wrench 条件的未来触觉预测优于无条件版本，MSE 从 0.027 降到 0.017，cosine 从 0.954 提升到 0.992。
- Authors: yujie-zang

### EA-TWM-2026-0011

- Claim: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.14981](https://arxiv.org/abs/2606.14981) Inference-time Policy Steering via Vision and Touch
- Locator: Abstract; Section 4 ViTaL; Section 5 Experiments
- Evidence: ViTaL 学习 visuo-tactile latent world model，结合视觉和文本条件触觉 verifier，对候选动作进行长时域视觉模式选择和短时域触觉 refinement；真实机器人任务包括 wiping、insertion 和 pipette transfer。
- Authors: yilin-wu

### EA-TWM-2026-0017

- Claim: 并非所有触觉能力都必须在推理期依赖触觉传感器；一条替代路线是离线学习安全接触奖励并蒸馏为可部署的触觉 token。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.15257](https://arxiv.org/abs/2603.15257) HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing
- Locator: Abstract; Section III Method; Section IV Experiments
- Evidence: HapticVLA 提出 Safety-Aware Reward-Weighted Flow Matching 和 Tactile Distillation，把惩罚过大抓取力和不良抓取轨迹的触觉奖励编码进 VLA；论文报告不使用推理期力传感器也达到 86.7% 平均成功率，并优于若干直接使用触觉反馈的 VLA 基线。
- Authors: konstantin-gubernatorov

### EA-TWM-2026-0016

- Claim: 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.07308](https://arxiv.org/abs/2605.07308) AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models
- Locator: Abstract; Section 3.3 Effective Tactile Reaction Dual-Stream; Section 4.4 Ablation Study
- Evidence: AT-VLA 把系统分为慢速视觉语言流和快速触觉流，慢速流负责任务理解和视觉定位，快速流以高频处理触觉反馈；作者采用 3:1 的快慢流频率比，并在真实接触丰富任务中验证 adaptive tactile injection、tactile gate、adaptive cross-attention 和 reaction dual-stream 的作用。
- Authors: xiaoqi-li

### EA-TWM-2026-0018

- Claim: 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: Section 4.2 Vision-Based Tactile Sensing and Marker Tracking; Section 5.2 Results and Discussion
- Evidence: HapTile 的每个夹爪手指安装视觉触觉传感器，接触会带来图像变化和 marker displacement；论文把 marker-motion 信号保存进数据集并用于 haptic feedback，实验也比较 vision-only、vision+tactile image 与 vision+tactile+marker 表征。
- Authors: amirhosein-alian

## References

- `2602.06001` [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) (2026-02-05)
- `2603.15257` [HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing](https://arxiv.org/abs/2603.15257) (2026-03-16)
- `2603.19201` [OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation](https://arxiv.org/abs/2603.19201) (2026-03-19)
- `2604.07335` [TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks](https://arxiv.org/abs/2604.07335) (2026-04-08)
- `2605.07308` [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](https://arxiv.org/abs/2605.07308) (2026-05-08)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.13877` [ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13877) (2026-06-11)
- `2606.14981` [Inference-time Policy Steering via Vision and Touch](https://arxiv.org/abs/2606.14981) (2026-06-12)
- `2606.19161` [HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision](https://arxiv.org/abs/2606.19161) (2026-06-17)
