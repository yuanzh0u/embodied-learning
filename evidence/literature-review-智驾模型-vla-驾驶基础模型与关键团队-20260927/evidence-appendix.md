# Evidence Appendix: 智驾模型-vla-驾驶基础模型与关键团队

- Time range: 2024-09-27..2026-09-27; classic antecedents allowed
- Events: 46
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-AVMODEL-2026-0001

- Claim: UniAD 以任务 query 作为感知、预测和规划之间的可学习接口，并保留显式中间监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2212.10156](https://arxiv.org/abs/2212.10156) Planning-oriented Autonomous Driving
- Locator: 2 Methodology
- Evidence: 方法逐项给出数据流；共享表征不意味着仅靠最终动作损失训练。
- Quote: “Queries play the role of connecting the pipeline”
- Authors: yihan-hu; jiazhi-yang; li-chen; et al.

### EA-AVMODEL-2026-0005

- Claim: LMDrive 将语言指令、相机和 LiDAR 特征映射为路点及指令完成标志，再由 PID 执行。
- Stance: `support` | Confidence: `direct`
- Paper: [2312.07488](https://arxiv.org/abs/2312.07488) LMDrive: Closed-Loop End-to-End Driving with Large Language Models
- Locator: 4.2 LLM for instruction-following auto driving
- Evidence: 原文执行链明确不是语言 token 直接驱动转向执行器。
- Quote: “use two PID controllers for latitudinal and longitudinal control”
- Authors: hao-shao; yuxuan-hu; letian-wang; et al.

### EA-AVMODEL-2026-0007

- Claim: LingoQA 的对象是驾驶视频问答，配套学习式 Lingo-Judge，而非执行驾驶动作。
- Stance: `support` | Confidence: `direct`
- Paper: [2312.14115](https://arxiv.org/abs/2312.14115) LingoQA: Visual Question Answering for Autonomous Driving
- Locator: 3 LingoQA Benchmark; 7 Conclusion
- Evidence: 问题、输出与评测对象均为 QA，没有控制输出证据。
- Quote: “benchmark for Visual Question Answering for autonomous driving”
- Authors: ana-maria-marcu; long-chen; jan-hnermann; et al.

### EA-AVMODEL-2026-0009

- Claim: DriveLM 以有向 QA 图传递上下文，再将行为说明映射为离散轨迹 token。
- Stance: `support` | Confidence: `direct`
- Paper: [2312.14150](https://arxiv.org/abs/2312.14150) DriveLM: Driving with Graph Visual Question Answering
- Locator: 3.1 Prompting with Context; 3.2 Trajectory Tokenization for Motion
- Evidence: motion 使用独立 LoRA，不能把多阶段流程压成一次统一解码。
- Quote: “with independent LoRA weights”
- Authors: chonghao-sima; katrin-renz; kashyap-chitta; et al.

### EA-AVMODEL-2026-0011

- Claim: DriveVLM-Dual 将低频 VLM 轨迹交给传统规划器进行高频细化，两支异步协作。
- Stance: `support` | Confidence: `direct`
- Paper: [2402.12289](https://arxiv.org/abs/2402.12289) DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models
- Locator: 3.5 DriveVLM-Dual
- Evidence: 该节明确给出优化式与神经规划器两种接入方式；结论只描述接口，不推断统一端到端训练。
- Quote: “the two branches operate asynchronously”
- Authors: xiaoyu-tian; junru-gu; bailin-li; et al.

### EA-AVMODEL-2026-0013

- Claim: NAVSIM 仅在初始帧调用规划策略，随后固定计划进行非反应式模拟，没有环境反馈给策略。
- Stance: `support` | Confidence: `direct`
- Paper: [2406.15349](https://arxiv.org/abs/2406.15349) NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking
- Locator: 3 NAVSIM: Non-Reactive Autonomous Vehicle Simulation
- Evidence: 协议直接排除了通常意义上的策略交互闭环。
- Quote: “driving agents are only queried in the initial frame”
- Authors: daniel-dauner; marcel-hallgarten; tianyu-li; et al.

### EA-AVMODEL-2026-0015

- Claim: EMMA 将驾驶任务的非传感器输入和输出统一为文本，允许规划、检测和路网任务联合训练。
- Stance: `support` | Confidence: `direct`
- Paper: [2410.23262](https://arxiv.org/abs/2410.23262) EMMA: End-to-End Multimodal Model for Autonomous Driving
- Locator: 2 Method
- Evidence: 方法节明确选择数值文本而非专门动作 token；多任务用途在 generalist 节得到说明。
- Quote: “the same unified language representation space”
- Authors: jyh-jing-hwang; runsheng-xu; hubert-lin; et al.

### EA-AVMODEL-2026-0018

- Claim: DiffusionDrive 从带噪轨迹锚点出发进行截断去噪，并以学习置信度选择最终轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.15139](https://arxiv.org/abs/2411.15139) DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving
- Locator: 3.3 Truncated Diffusion; 3.4 Architecture
- Evidence: 无需语言或视频未来生成即可学习多模式驾驶动作，构成非语言主线对照。
- Quote: “The final trajectory with the highest confidence score is selected”
- Authors: bencheng-liao; shaoyu-chen; haoran-yin; et al.

### EA-AVMODEL-2026-0020

- Claim: DiMA 通过共享场景编码器、辅助任务和特征蒸馏训练视觉规划器，默认推理无需 LLM。
- Stance: `support` | Confidence: `direct`
- Paper: [2501.09757](https://arxiv.org/abs/2501.09757) Distilling Multi-modal Large Language Models for Autonomous Driving
- Locator: 3.1 Vision-based Planner; 5 Experimental Results
- Evidence: 主方法与结果均明确无 LLM 推理；Dual 是另一个可选配置。
- Quote: “our approach does not rely on an LLM for inference”
- Authors: deepti-hegde; rajeev-yasarla; hong-cai; et al.

### EA-AVMODEL-2026-0022

- Claim: SimLingo 用同一视觉场景的多种指令—轨迹配对，迫使模型学习语言对动作的影响。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.09594](https://arxiv.org/abs/2503.09594) SimLingo: Vision-Only Closed-Loop Autonomous Driving with Language-Action Alignment
- Locator: 3.2 Datasets
- Evidence: Action Dreaming 部分解释了普通专家轨迹可由视觉猜出、从而忽略语言的混淆；多分支数据针对该问题。
- Quote: “forces the model to listen to the instruction”
- Authors: katrin-renz; long-chen; elahe-arani; et al.

### EA-AVMODEL-2026-0025

- Claim: ORION 用 LLM 的 planning token 条件化 VAE 轨迹分布，并以 GRU 解码轨迹。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.19755](https://arxiv.org/abs/2503.19755) ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation
- Locator: 3.3 Generative Planner
- Evidence: 原文明确 VAE 负责 reasoning/action 分布对齐，GRU 借鉴 GenAD；不是纯文本坐标生成。
- Quote: “we use the GRU decoder in GenAD”
- Authors: haoyu-fu; diankun-zhang; zongchuang-zhao; et al.

### EA-AVMODEL-2026-0028

- Claim: OpenDriveVLA 将 scene、agent、map 三类结构化视觉 token 对齐到语言空间，并联合优化轨迹生成。
- Stance: `support` | Confidence: `direct`
- Paper: [2503.23463](https://arxiv.org/abs/2503.23463) OpenDriveVLA: Towards End-to-end Autonomous Driving with Large Vision Language Action Model
- Locator: III-B Stage 1 - Hierarchical Vision-Language Alignment
- Evidence: 阶段一明确对三类 token 设独立 projector，后续阶段三联合训练；不能仅称通用图文 VLM。
- Quote: “three token-specific projectors”
- Authors: xingcheng-zhou; xuyuan-han; feng-yang; et al.

### EA-AVMODEL-2026-0030

- Claim: AutoVLA 将驾驶运动码本扩展进 VLM 词表，以统一自回归过程生成推理和动作。
- Stance: `support` | Confidence: `direct`
- Paper: [2506.13757](https://arxiv.org/abs/2506.13757) AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning
- Locator: 3.1 Framework
- Evidence: 框架节给出 K-disk 码本和扩展 token 的机制；区别于文本数值及外接连续解码头。
- Quote: “additional tokens (i.e., <action_0>”
- Authors: zewei-zhou; tianhui-cai; seth-z-zhao; et al.

### EA-AVMODEL-2026-0033

- Claim: Alpamayo-R1 在训练时使用离散动作 token，但推理轨迹由连续 flow-matching 动作专家解码。
- Stance: `support` | Confidence: `direct`
- Paper: [2511.00088](https://arxiv.org/abs/2511.00088) Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail
- Locator: 5.1 Action Modality Injection
- Evidence: 方法节明确区分训练和推理的动作表示，不能将其描述为纯自回归坐标输出。
- Quote: “we do not use discrete trajectory tokens”
- Authors: nvidia; unknown-author; yan-wang; et al.

### EA-AVMODEL-2026-0036

- Claim: MindDrive 先学语言 meta-action 到轨迹的映射，再用 CARLA 交互回报及 PPO 优化决策专家。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.13636](https://arxiv.org/abs/2512.13636) MindDrive: A Vision-Language-Action Model for Autonomous Driving via Online Reinforcement Learning
- Locator: 3.2 Language-Action Mapping; 3.3 Online RL for Action-Reasoning
- Evidence: 方法及算法明确回报来自实际 simulator rollout，优化的是决策分支和价值网络。
- Quote: “optimize the policy using the Proximal Policy Optimization”
- Authors: haoyu-fu; diankun-zhang; zongchuang-zhao; et al.

### EA-AVMODEL-2026-0038

- Claim: Orion-Lite 在推理时移除文本提示和大型 LLM，以轻量 transformer 模仿教师的 planning-token 表征。
- Stance: `support` | Confidence: `direct`
- Paper: [2604.08266](https://arxiv.org/abs/2604.08266) Orion-Lite: Distilling LLM Reasoning into Efficient Vision-Only Driving Models
- Locator: 3.2 State Embedding Extraction; 3.3 Lightweight Distillation Module
- Evidence: 原文明确学生删除文本提示、替换 LLM；仍继承教师视觉与时间模块。
- Quote: “we discard the text prompts entirely”
- Authors: jing-gu; niccol-cavagnero; gijs-dubbelman

### EA-AVMODEL-2026-0043

- Claim: nuReasoning 的 nuVLA 在推理时关闭显式文字推理，训练期加入推理监督仍改善其开放环规划。
- Stance: `support` | Confidence: `direct`
- Paper: [2605.31572](https://arxiv.org/abs/2605.31572) nuReasoning: A Reasoning-Centric Dataset and Benchmark for Long-Tail Autonomous Driving
- Locator: 5.3 Results on Planning Benchmark
- Evidence: 消融明确区分训练监督与推理输出，为语言参与阶段提供直接证据。
- Quote: “Explicit reasoning outputs are disabled at test time”
- Authors: zhiyu-huang; johnson-liu; rui-song; et al.

### EA-AVMODEL-2026-0045

- Claim: FlashDrive 分别处理视觉重复编码、KV 预填充、串行推理和迭代动作解码四类延迟。
- Stance: `support` | Confidence: `direct`
- Paper: [2608.12932](https://arxiv.org/abs/2608.12932) FlashDrive: Flash Vision-Language-Action Inference for Autonomous Driving
- Locator: 3 Method
- Evidence: 这是对 Alpamayo1.5 的明确工程继承，而非新驾驶策略从零训练。
- Quote: “four distinct ones (encode, prefill, decode, and action)”
- Authors: zekai-li; yihao-liang; hongfei-zhang; et al.

### EA-AVMODEL-2026-0002

- Claim: UniAD 预测轨迹后，在推理时使用占据地图执行额外避碰优化。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2212.10156](https://arxiv.org/abs/2212.10156) Planning-oriented Autonomous Driving
- Locator: 2.4 Planning
- Evidence: 原文区分可学习路点与推理优化，因此不能称像素直接到执行器的单一网络。
- Quote: “we optimize based on Newton’s method in inference only”
- Authors: yihan-hu; jiazhi-yang; li-chen; et al.

### EA-AVMODEL-2026-0006

- Claim: LMDrive 的连续多句指令比单句指令更困难，实验中的驾驶分数与路线完成率下降。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2312.07488](https://arxiv.org/abs/2312.07488) LMDrive: Closed-Loop End-to-End Driving with Large Language Models
- Locator: 6.2 Quantitative Results
- Evidence: 结论限制到 LangAuto-Sequential 的组合指令设置。
- Quote: “have a drop in the driving score and route completion ratio”
- Authors: hao-shao; yuxuan-hu; letian-wang; et al.

### EA-AVMODEL-2026-0008

- Claim: LingoQA 研究发现多帧上下文有助区分动态交通、信号灯变化等单帧易错情形。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2312.14115](https://arxiv.org/abs/2312.14115) LingoQA: Visual Question Answering for Autonomous Driving
- Locator: 5.2 Evaluation of SOTA Vision-Language Models
- Evidence: 人工与模型帧数分析支持视频理解必要性；不推断闭环驾驶效果。
- Quote: “misclassifying parked cars as engaged in traffic”
- Authors: ana-maria-marcu; long-chen; jan-hnermann; et al.

### EA-AVMODEL-2026-0012

- Claim: 论文报告双 OrinX 的车载部署；VLM 与高频驾驶系统在不同处理器运行。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2402.12289](https://arxiv.org/abs/2402.12289) DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models
- Locator: 6 Onboard Deployment and Testing
- Evidence: 部署节明确说明处理器分工和实车演示；不将演示当作无监督运营证明。
- Quote: “equipped with two OrinX processors”
- Authors: xiaoyu-tian; junru-gu; bailin-li; et al.

### EA-AVMODEL-2026-0016

- Claim: EMMA 的内部数据消融中，场景描述对规划表现影响中性，而元决策和关键物体识别带来改善。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2410.23262](https://arxiv.org/abs/2410.23262) EMMA: End-to-End Multimodal Model for Autonomous Driving
- Locator: 3.3 End-to-End Motion Planning with Chain-of-Thought Reasoning on Internal Dataset
- Evidence: 同一 CoT 消融直接比较组成部分；不泛化为所有语言描述均无效。
- Quote: “scene description has a neutral impact”
- Authors: jyh-jing-hwang; runsheng-xu; hubert-lin; et al.

### EA-AVMODEL-2026-0019

- Claim: DiffusionDrive 的主 NAVSIM 设置采用前向相机与栅格 LiDAR；nuScenes 实验采用另一骨干配置。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2411.15139](https://arxiv.org/abs/2411.15139) DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving
- Locator: 4.2 Implementation Detail; 4.7 Quantitative Comparison on nuScenes dataset
- Evidence: 不同实验的骨干与传感输入不能混成统一模型规格。
- Quote: “implement DiffusionDrive on top of SparseDrive”
- Authors: bencheng-liao; shaoyu-chen; haoran-yin; et al.

### EA-AVMODEL-2026-0021

- Claim: DiMA 中仅把 VQA 和规划损失加到 BEV 特征上的朴素联合训练，收益并不一致。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2501.09757](https://arxiv.org/abs/2501.09757) Distilling Multi-modal Large Language Models for Autonomous Driving
- Locator: 5.1 Ablation study.
- Evidence: 作者逐步消融显示结构化 token、蒸馏和辅助任务的重要性，不可把效果全归于加入语言。
- Quote: “inconsistent gains and drops in performance”
- Authors: deepti-hegde; rajeev-yasarla; hong-cai; et al.

### EA-AVMODEL-2026-0024

- Claim: 官方 CARLA Leaderboard 仅测试 SimLingo-BASE；完整 SimLingo 的闭环驾驶在本地 Bench2Drive 检验。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2503.09594](https://arxiv.org/abs/2503.09594) SimLingo: Vision-Only Closed-Loop Autonomous Driving with Language-Action Alignment
- Locator: 4.2 Implementation Details
- Evidence: 原文说明 leaderboard 关闭造成的提交差异，避免把 BASE 的无语言成绩标成 VLA 实证。
- Quote: “could not submit the final SimLingo”
- Authors: katrin-renz; long-chen; elahe-arani; et al.

### EA-AVMODEL-2026-0026

- Claim: 在 ORION 的受控动作输出消融中，纯文本轨迹表现最弱；生成式轨迹接口优于相同骨干的 MLP 解码。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2503.19755](https://arxiv.org/abs/2503.19755) ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation
- Locator: 4.5 Ablation Study
- Evidence: 仅描述同一实验内的接口比较；不据此判定所有双系统或扩散方法失败。
- Quote: “The plain text paradigm performs the worst”
- Authors: haoyu-fu; diankun-zhang; zongchuang-zhao; et al.

### EA-AVMODEL-2026-0035

- Claim: AlpaSim 闭环中自车重新渲染并执行控制，其他交通参与者沿日志轨迹回放。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2511.00088](https://arxiv.org/abs/2511.00088) Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail
- Locator: 6.1 Evaluation Protocol
- Evidence: 评测协议明示背景交通非反应式；该闭环有自车反馈但不是所有参与者可互动。
- Quote: “follow their recorded trajectories”
- Authors: nvidia; unknown-author; yan-wang; et al.

### EA-AVMODEL-2026-0039

- Claim: 在 Bench2Drive 消融中，特征蒸馏与真值轨迹监督结合优于任一单独信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.08266](https://arxiv.org/abs/2604.08266) Orion-Lite: Distilling LLM Reasoning into Efficient Vision-Only Driving Models
- Locator: 5.2 Ablation Study
- Evidence: 该节报告三种训练配置；结论限制在同教师、冻结视觉模块和该闭环基准。
- Quote: “a synergistic combination of latent feature distillation”
- Authors: jing-gu; niccol-cavagnero; gijs-dubbelman

### EA-AVMODEL-2026-0044

- Claim: nuReasoning 先自动产生推理标注，再经人工检查和纠错；其验证仍以开放环为限。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.31572](https://arxiv.org/abs/2605.31572) nuReasoning: A Reasoning-Centric Dataset and Benchmark for Long-Tail Autonomous Driving
- Locator: 3.3 Reasoning Annotation; 6 Conclusions
- Evidence: 数据质量流程和驾驶验证层级是不同维度，不能用人工审核推导实车安全。
- Quote: “benchmark focuses on open-loop evaluation”
- Authors: zhiyu-huang; johnson-liu; rui-song; et al.

### EA-AVMODEL-2026-0003

- Claim: 无视觉 AD-MLP 在 nuScenes 开放环能取得有竞争力的轨迹结果，暴露指标与真实驾驶能力的落差。
- Stance: `limit` | Confidence: `direct`
- Paper: [2305.10430](https://arxiv.org/abs/2305.10430) Rethinking the Open-Loop Evaluation of End-to-End Autonomous Driving in nuScenes
- Locator: 3.3 Main Results; 5 Conclusion and Limitations
- Evidence: 方法、结果和限制共同构成反证，不能将其当作量产方案。
- Quote: “merely an impractical toy incapable of functioning”
- Authors: jiang-tian-zhai; ze-feng; jinhao-du; et al.

### EA-AVMODEL-2026-0004

- Claim: 占据栅格离散化会使真实记录轨迹被误判碰撞，栅格尺寸影响结果。
- Stance: `limit` | Confidence: `direct`
- Paper: [2305.10430](https://arxiv.org/abs/2305.10430) Rethinking the Open-Loop Evaluation of End-to-End Autonomous Driving in nuScenes
- Locator: 4.2 Collision in Ground Truth
- Evidence: 该节比较不同栅格尺寸和实例，限定为所研究的碰撞指标实现。
- Quote: “resulting in collisions being falsely detected”
- Authors: jiang-tian-zhai; ze-feng; jinhao-du; et al.

### EA-AVMODEL-2026-0010

- Claim: DriveLM-Agent 的论文规划验证仍为开放环；作者将闭环列为后续方向。
- Stance: `limit` | Confidence: `direct`
- Paper: [2312.14150](https://arxiv.org/abs/2312.14150) DriveLM: Driving with Graph Visual Question Answering
- Locator: 6 Discussion
- Evidence: CARLA QA 数据与实际策略闭环验证是不同证据。
- Quote: “currently evaluated under an open-loop scheme”
- Authors: chonghao-sima; katrin-renz; kashyap-chitta; et al.

### EA-AVMODEL-2026-0014

- Claim: NAVSIM 作者指出，高 PDMS 并不总对应高闭环分数，建议配合 CARLA 等闭环评测。
- Stance: `limit` | Confidence: `direct`
- Paper: [2406.15349](https://arxiv.org/abs/2406.15349) NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking
- Locator: 5 Discussion
- Evidence: 作者限制节明确承认非反应性、错误累积和交通规则覆盖的不足。
- Quote: “A high PDMS does not always imply a high CLS”
- Authors: daniel-dauner; marcel-hallgarten; tianyu-li; et al.

### EA-AVMODEL-2026-0017

- Claim: 作者明确指出，人可读的辅助输出和驾驶动作并不保证始终一致。
- Stance: `limit` | Confidence: `direct`
- Paper: [2410.23262](https://arxiv.org/abs/2410.23262) EMMA: End-to-End Multimodal Model for Autonomous Driving
- Locator: A.5 Limitations, Risks, and Mitigations
- Evidence: 限制节直接否认输出一致性的保证，不能用解释流畅度替代动作忠实性。
- Quote: “there is no guarantee that these outputs”
- Authors: jyh-jing-hwang; runsheng-xu; hubert-lin; et al.

### EA-AVMODEL-2026-0023

- Claim: SimLingo 的消融未观察到未对齐语言任务对驾驶的明确正负影响；CoT 的驾驶收益也未达统计显著。
- Stance: `limit` | Confidence: `direct`
- Paper: [2503.09594](https://arxiv.org/abs/2503.09594) SimLingo: Vision-Only Closed-Loop Autonomous Driving with Language-Action Alignment
- Locator: 5 Conclusion and Limitations; 4.3 Results
- Evidence: 结果节与限制节共同限定增益归因：语言任务成绩不能自动证明驾驶增强。
- Quote: “statistically significant driving improvements”
- Authors: katrin-renz; long-chen; elahe-arani; et al.

### EA-AVMODEL-2026-0027

- Claim: ORION 作者将大 VLM 的计算复杂度列为实时驾驶部署限制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2503.19755](https://arxiv.org/abs/2503.19755) ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation
- Locator: 5 Conclusion
- Evidence: 结论直接承认实时部署问题，不能把仿真闭环分数等同车端可部署性。
- Quote: “limited by the high computational complexity”
- Authors: haoyu-fu; diankun-zhang; zongchuang-zhao; et al.

### EA-AVMODEL-2026-0029

- Claim: OpenDriveVLA 当前规划评测仅为开放环，作者警告这可能高估鲁棒性。
- Stance: `limit` | Confidence: `direct`
- Paper: [2503.23463](https://arxiv.org/abs/2503.23463) OpenDriveVLA: Towards End-to-end Autonomous Driving with Large Vision Language Action Model
- Locator: VIII-D 2 Current Limitations
- Evidence: 原文承认未捕捉交互反馈，问答与离线轨迹成绩不足以证明真实闭环能力。
- Quote: “may lead to overestimated robustness”
- Authors: xingcheng-zhou; xuyuan-han; feng-yang; et al.

### EA-AVMODEL-2026-0031

- Claim: AutoVLA 的 NAVSIM best-of-N 结果依赖 oracle 选择，必须与可直接部署的单次预测分开。
- Stance: `limit` | Confidence: `direct`
- Paper: [2506.13757](https://arxiv.org/abs/2506.13757) AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning
- Locator: 4.2 Main Results
- Evidence: 结果节明确说明六个候选的选择方式；这是评测可用信息差异，不是一般部署能力。
- Quote: “we use an oracle scorer”
- Authors: zewei-zhou; tianhui-cai; seth-z-zhao; et al.

### EA-AVMODEL-2026-0032

- Claim: AutoVLA 作者仍将 GPU 依赖、显存和计算成本列为实时应用限制。
- Stance: `limit` | Confidence: `direct`
- Paper: [2506.13757](https://arxiv.org/abs/2506.13757) AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning
- Locator: 5 Conclusions
- Evidence: 结论说明近实时与实用车端部署仍有差距，不把模型规模直接当部署证明。
- Quote: “it remains highly GPU-dependent”
- Authors: zewei-zhou; tianhui-cai; seth-z-zhao; et al.

### EA-AVMODEL-2026-0034

- Claim: 仅优化推理评分时，Alpamayo-R1 的 ADE 和推理—动作一致性会退化；联合一致性奖励改善这种取舍。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.00088](https://arxiv.org/abs/2511.00088) Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail
- Locator: 6.3 Improvements of Reasoning, Consistency, and Safety via RL Post-Training
- Evidence: 奖励消融明确报告反向变化，说明高语言评分本身不足以确保动作改善。
- Quote: “both the ADE metric and reasoning–action consistency degrade”
- Authors: nvidia; unknown-author; yan-wang; et al.

### EA-AVMODEL-2026-0037

- Claim: MindDrive 在线 RL 的训练轮数与闭环性能并非单调关系，过多更新会降低表现。
- Stance: `limit` | Confidence: `direct`
- Paper: [2512.13636](https://arxiv.org/abs/2512.13636) MindDrive: A Vision-Language-Action Model for Autonomous Driving via Online Reinforcement Learning
- Locator: 4.3 Ablation Studies
- Evidence: 消融直接观察退化；作者用灾难性遗忘解释，但该机制解释本身仍是推断。
- Quote: “further increasing the epochs substantially degrades performance”
- Authors: haoyu-fu; diankun-zhang; zongchuang-zhao; et al.

### EA-AVMODEL-2026-0040

- Claim: 移除 LLM 后，Orion-Lite 的主要推理瓶颈转移到重型视觉编码器。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.08266](https://arxiv.org/abs/2604.08266) Orion-Lite: Distilling LLM Reasoning into Efficient Vision-Only Driving Models
- Locator: 6 Limitations and Future Work
- Evidence: 限制节明确指出瓶颈迁移，模块加速不能等同整个系统同比加速。
- Quote: “becomes the primary computational bottleneck”
- Authors: jing-gu; niccol-cavagnero; gijs-dubbelman

### EA-AVMODEL-2026-0041

- Claim: 该审计发现 Alpamayo-R1 样本中存在声明减速或停车而轨迹继续的说明—动作不一致。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.17268](https://arxiv.org/abs/2605.17268) Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation in Autonomous Driving Models
- Locator: 5.3 Reasoning-Action Consistency (Phase 2B)
- Evidence: 只采纳实验观察，不将它当作所有 VLA 或量产系统的失败率。
- Quote: “claimed deceleration/stop with continuing trajectory”
- Authors: nicanor-mayumu; xiaoheng-deng; patrick-mukala

### EA-AVMODEL-2026-0042

- Claim: 该审计使用确定性关键词抽取，作者承认它会漏掉同义表达。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.17268](https://arxiv.org/abs/2605.17268) Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation in Autonomous Driving Models
- Locator: 7.1 Model and Dataset
- Evidence: 方法局限使其精确百分比不宜脱离阈值和标注协议使用。
- Quote: “may miss paraphrased mentions”
- Authors: nicanor-mayumu; xiaoheng-deng; patrick-mukala

### EA-AVMODEL-2026-0046

- Claim: FlashDrive 的 AlpaSim 评测并非所有指标均改善，其中 Wrong Lane 退化。
- Stance: `limit` | Confidence: `direct`
- Paper: [2608.12932](https://arxiv.org/abs/2608.12932) FlashDrive: Flash Vision-Language-Action Inference for Autonomous Driving
- Locator: 4.4 Closed-loop Evaluation
- Evidence: 作者结果包含退化指标，因此只能说特定设置保留总体质量，不能宣布安全无损。
- Quote: “The one metric that regresses is Wrong Lane”
- Authors: zekai-li; yihao-liang; hongfei-zhang; et al.

## References

- `2212.10156` [Planning-oriented Autonomous Driving](https://arxiv.org/abs/2212.10156) (2022-12-20)
- `2305.10430` [Rethinking the Open-Loop Evaluation of End-to-End Autonomous Driving in nuScenes](https://arxiv.org/abs/2305.10430) (2023-05-17)
- `2312.07488` [LMDrive: Closed-Loop End-to-End Driving with Large Language Models](https://arxiv.org/abs/2312.07488) (2023-12-12)
- `2312.14115` [LingoQA: Visual Question Answering for Autonomous Driving](https://arxiv.org/abs/2312.14115) (2023-12-21)
- `2312.14150` [DriveLM: Driving with Graph Visual Question Answering](https://arxiv.org/abs/2312.14150) (2023-12-21)
- `2402.12289` [DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models](https://arxiv.org/abs/2402.12289) (2024-02-19)
- `2406.15349` [NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking](https://arxiv.org/abs/2406.15349) (2024-06-21)
- `2410.23262` [EMMA: End-to-End Multimodal Model for Autonomous Driving](https://arxiv.org/abs/2410.23262) (2024-10-30)
- `2411.15139` [DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving](https://arxiv.org/abs/2411.15139) (2024-11-22)
- `2501.09757` [Distilling Multi-modal Large Language Models for Autonomous Driving](https://arxiv.org/abs/2501.09757) (2025-01-16)
- `2503.09594` [SimLingo: Vision-Only Closed-Loop Autonomous Driving with Language-Action Alignment](https://arxiv.org/abs/2503.09594) (2025-03-12)
- `2503.19755` [ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation](https://arxiv.org/abs/2503.19755) (2025-03-25)
- `2503.23463` [OpenDriveVLA: Towards End-to-end Autonomous Driving with Large Vision Language Action Model](https://arxiv.org/abs/2503.23463) (2025-03-30)
- `2506.13757` [AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning](https://arxiv.org/abs/2506.13757) (2025-06-16)
- `2511.00088` [Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail](https://arxiv.org/abs/2511.00088) (2025-10-30)
- `2512.13636` [MindDrive: A Vision-Language-Action Model for Autonomous Driving via Online Reinforcement Learning](https://arxiv.org/abs/2512.13636) (2025-12-15)
- `2604.08266` [Orion-Lite: Distilling LLM Reasoning into Efficient Vision-Only Driving Models](https://arxiv.org/abs/2604.08266) (2026-04-09)
- `2605.17268` [Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation in Autonomous Driving Models](https://arxiv.org/abs/2605.17268) (2026-05-17)
- `2605.31572` [nuReasoning: A Reasoning-Centric Dataset and Benchmark for Long-Tail Autonomous Driving](https://arxiv.org/abs/2605.31572) (2026-05-29)
- `2608.12932` [FlashDrive: Flash Vision-Language-Action Inference for Autonomous Driving](https://arxiv.org/abs/2608.12932) (2026-08-13)
