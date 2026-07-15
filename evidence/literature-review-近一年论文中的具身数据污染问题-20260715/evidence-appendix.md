# Evidence Appendix: 近一年论文中的具身数据污染问题

- Time range: 2025-07-15..2026-07-15
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-CONTAM-2026-0011

- Claim: 具身视频语料的重复不能只按片段数理解：同一场景中的相似任务会膨胀数据规模却几乎不增加场景多样性，因此去重应同时检查视觉与轨迹冗余。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.04463](https://arxiv.org/abs/2606.04463) OSCAR: Omni-Embodiment Action-Conditioned World Model for Robotics
- Locator: 4.3 Semantic Deduplication
- Evidence: OSCAR 先按视觉相似性聚类，再按轨迹相似性核验；同场景但轨迹显著不同的片段不判为重复。
- Quote: “After the quality filters, we observe substantial redundancy in both robotics and egocentric human data: they often repeat many highly similar tasks in the same physical scene. This inflates the raw clip count while adding little scene diversity.”
- Authors: zhuoyuan-wu; jun-gao

### EA-CONTAM-2026-0013

- Claim: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation
- Locator: C.4 Retention Balance, Single-Task Curation, and Real-Robot Failure Modes
- Evidence: ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。
- Quote: “To further ablate the role of Multitask Influence Interaction (MII), we visualize the retained task distributions after data curation in Fig. 8 . We consider the six-task real-robot setting with 120 demonstrations per task and an overall retention ratio of 66.7%. Without MII, naively ranking demonstrations with a single global influence score results in a highly skewed retained set: Pick Fruits, Shelf Retrieval, and Wipe Board retain 115, 113, and 104 demonstrations, respectively, whereas Stack”
- Authors: tao-xu; jiaxin-wang; runhao-zhang; et al.

### EA-CONTAM-2026-0005

- Claim: 视觉后门可通过深层注意力和潜特征异常做推理时定位，但与场景语义自然融合的触发物依然是明显盲点。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.03153](https://arxiv.org/abs/2602.03153) When Attention Betrays: Erasing Backdoor Attacks in Robotic Policies by Reconstructing Visual Tokens
- Locator: VI-E Trigger Proportions, Poisoning Ratios and Types
- Evidence: Bera 对圆形块和棋盘格触发保持较低攻击成功，但语义合理的红色瓶盖触发更难被异常 token 方法区分。
- Quote: “In contrast, Bera mitigates circular block and checkerboard triggers, maintaining low ASR and stable performance. However, red bottle cap trigger fits the scenario semantics, leading to higher ASR and slight reductions in robustness, suggesting that semantically integrated triggers are more challenging to detect.”
- Authors: xuetao-li; pinhan-fu; wenke-huang; et al.

### EA-CONTAM-2026-0012

- Claim: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.04825](https://arxiv.org/abs/2606.04825) HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
- Locator: 3.2 Synchronization and Data Quality Control
- Evidence: 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。
- Quote: “All data modalities are synchronized through the robot control loop. For policy learning, actions are converted to a unified 7D end-effector delta representation (1) where are translational deltas, are rotational deltas, and is the gripper command. This decouples learning from the exact robot configuration, enabling cross-embodiment by focusing the policy on local contact adjustment from tactile feedback. Several quality checks are applied to every collected trajectory. Empty or corrupted trajec”
- Authors: amirhosein-alian; yongqiang-zhao; shiyi-gu; et al.

### EA-CONTAM-2026-0014

- Claim: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation
- Locator: Abstract (full-text section)
- Evidence: 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action chunks。
- Quote: “Abstract Scaling imitation learning requires large datasets, yet human teleoperation inevitably produces mixed-quality demonstrations containing hesitations and recoveries. Prior frame-level progress reward models supervise on absolute temporal progress proxies that suffer from label noise, or require costly human annotations to define subtask boundaries. We present WARP (Warp-Augmented Relative Progress), a novel fully self-supervised algorithm for learning dense, signed relative progress magni”
- Authors: justin-yu; andrew-goldberg; kavish-kondap; et al.

### EA-CONTAM-2026-0008

- Claim: 后门防御应把检测、因果定位和恢复分开计账；干净校准的内部机制监控对视觉触发有效，但不覆盖状态、语义或自适应后门。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.12571](https://arxiv.org/abs/2607.12571) TrustVLA: Mechanism-Guided Inference-Time Defense Against Vision-Language-Action Backdoors
- Locator: 5 Conclusion
- Evidence: TrustVLA 通过内部证据异常、反事实支撑定位和局部修复降低所测视觉后门，作者明确限定了所需访问权限与攻击类型。
- Quote: “TrustVLA targets visual-triggered VLA backdoors with self-hosted hidden-state access; recovery remains conditional on the compact-footprint hypothesis. Semantic or non-visual triggers, severe distribution shift, and adaptive attackers that mimic evidence while suppressing localization remain outside our robustness claim (Appendix A.1 ).”
- Authors: pinhan-fu; xianda-guo; xuetao-li; et al.

### EA-CONTAM-2026-0007

- Claim: LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.03827](https://arxiv.org/abs/2510.03827) LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization
- Locator: 5.2 Main Results
- Evidence: LIBERO-PRO 在保持逻辑可执行的前提下改变物体位置与任务，标准设置中的高分模型在这些轻微改变下近乎崩溃。
- Quote: “Despite achieving success rates above 90% on the standard LIBERO benchmark, models nearly collapse under changes to object positions or minor task modifications, even when constructed from training components.”
- Authors: xueyang-zhou; yangming-xu; guiyao-tie; et al.

### EA-CONTAM-2026-0003

- Claim: 仅看 episode 成功率会漏掉动作级污染：后门可在关键短时窗覆写夹爪等可复用低层动作，即使整体任务表现仍显得正常。
- Stance: `limit` | Confidence: `direct`
- Paper: [2510.10932](https://arxiv.org/abs/2510.10932) DropVLA: An Action-Level Backdoor Attack on Vision-Language-Action Models
- Locator: V Discussion
- Evidence: DropVLA 表明受影响的不必是整条轨迹；攻击可瞄准触发后极短时窗的安全关键动作。
- Quote: “Action-level backdoors are particularly hazardous because a trigger can override a safety-critical action within a short control window, inducing irreversible state transitions (e.g., unintended object release) even when episode-level task success remains high.”
- Authors: zonghuan-xu; jiayu-li; yunhan-zhao; et al.

### EA-CONTAM-2026-0009

- Claim: 污染后门可以不只让机器人“失败”，而是在触发时执行攻击者指定的长程动作序列；真机已显示可行性，但强度低于仿真。
- Stance: `limit` | Confidence: `direct`
- Paper: [2511.12149](https://arxiv.org/abs/2511.12149) AttackVLA: Benchmarking Adversarial and Backdoor Attacks on Vision-Language-Action Models
- Locator: 4.4 Attacks in Real-World Settings
- Evidence: BackdoorVLA 在 7-DoF Franka 上通过物理物体与文本触发定向长程行为，并同时保留一部分无触发任务性能。
- Quote: “BackdoorVLA attains an average of 50.00% while maintaining 60.00% clean performance. Although the real-world results are lower than their simulation counterparts, they still demonstrate that these attacks remain effective on a real-world robotic platform.”
- Authors: jiayu-li; yunhan-zhao; xiang-zheng; et al.

### EA-CONTAM-2026-0001

- Claim: 具身污染不只能藏在图像或文本中：污染真实示教里的初始关节状态可形成隐蔽 VLA 后门，并绕过视觉预处理防御。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.04266](https://arxiv.org/abs/2601.04266) State Backdoor: Towards Stealthy Real-world Poisoning Attack on Vision-Language-Action Model in State Space
- Locator: VI-E Robustness Evaluation
- Evidence: State Backdoor 将物理可行的初始状态偏移与恶意动作关联；剪枝与图像压缩都未能有效消除攻击。
- Quote: “State Backdoor consistently achieves an ASR above 90% across all pruning levels. However, as the pruning ratio increases, the model’s normal functionality degrades, making it impractical to prune further. Therefore, Fine-pruning fails to defend against State Backdoor.”
- Authors: ji-guo; wenbo-jiang; yansong-lin; et al.

### EA-CONTAM-2026-0004

- Claim: Action chunking 与 delta-pose 积分会把平滑、微小的污染偏差在开环执行窗内积累成失败，使“轨迹看起来平滑”不再是安全证据。
- Stance: `limit` | Confidence: `direct`
- Paper: [2601.14323](https://arxiv.org/abs/2601.14323) SilentDrift: Exploiting Action Chunking for Stealthy Backdoor Attacks on Vision-Language-Action Models
- Locator: 3.2 Vulnerability of Action Chunking to Drift Accumulation
- Evidence: SilentDrift 利用 action chunk 内缺少视觉纠正的结构性弱点，让动力学连续的小偏差持续积累。
- Quote: “The combination of action chunking and delta pose representations creates an intra-chunk visual open-loop that permits unbounded drift accumulation. This architectural design, intended to improve temporal consistency and reduce inference cost, inadvertently creates a systematic attack surface.”
- Authors: bingxin-xu; yuzhang-shang; binghui-wang; et al.

### EA-CONTAM-2026-0010

- Claim: 下游只用干净数据微调不能证明 VLA 已经没有污染；植入微调不敏感模块的基模型后门可穿过用户端的干净适配。
- Stance: `limit` | Confidence: `direct`
- Paper: [2602.00500](https://arxiv.org/abs/2602.00500) Inject Once Survive Later: Backdooring Vision-Language-Action Models to Persist Through Downstream Fine-tuning
- Locator: 5.2 Main Results
- Evidence: INFUSE 在基模型分发前定向污染微调不敏感模块，干净下游微调后仍保持显著后门行为。
- Quote: “INFUSE achieves an average ASR of 79.8% while maintaining clean performance (SR(w/o) = 28.3%) comparable to the normal model (29.3%), significantly outperforming BadVLA (36.6% ASR).”
- Authors: jianyi-zhou; yujie-wei; ruichen-zhen; et al.

### EA-CONTAM-2026-0006

- Claim: 世界模型使数据污染变成“二次激活”问题：表面安全的遥操数据可在生成扩增时转化为危险轨迹，并污染下游政策。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.09499](https://arxiv.org/abs/2606.09499) Targeting World Models to Compromise Robot Learning Pipelines
- Locator: 4 Identifying Vulnerabilities in the Robot Learning Supply Chain
- Evidence: 论文在文本条件与动作条件世界模型中操纵预测，使恶意行为只在合成轨迹阶段出现。
- Quote: “By targeting world models within the robot learning pipeline, malicious data providers can effectively implant dangerous behavior or altered transition dynamics into otherwise safe robot teleoperation data. This allows them to poison downstream robot policies while bypassing dataset-level safety checks.”
- Authors: ethan-rathbun; ahmed-agha; saaduddin-mahmud; et al.

### EA-CONTAM-2026-0002

- Claim: 开源机器人数据供应链对极小比例的 episode 级投毒很敏感：在该真实拾放实验中，3 条投毒 episode 混入 320 条干净 episode 即实现触发式完全拒绝服务。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.04146](https://arxiv.org/abs/2607.04146) !Imperio, smolVLA: The Implications of Data Poisoning on Open Source Robotics
- Locator: Abstract, opening paragraph
- Evidence: 投毒数据将触发词与固定关节位置绑定；攻击在触发词出现时失效，干净提示行为保持。
- Quote: “Three poisoned episodes in 320 clean episodes suffice for a complete denial of service.”
- Authors: stefan-bhler; mark-schutera

### EA-CONTAM-2026-0015

- Claim: SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。
- Stance: `limit` | Confidence: `direct`
- Paper: [2607.06442](https://arxiv.org/abs/2607.06442) SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models
- Locator: Introduction
- Evidence: 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。
- Quote: “Our contributions are as follows: • We propose a primitive-compositional view of trajectory utility, realized by Primitive Discovery and Structural Exposure Allocation, which allocate selection budgets according to reuse-aware primitive and transition exposure under diminishing returns. • We introduce Learning-Friendly Trajectory Selection, which selects medoid trajectories within each composition-pattern bucket to favor central, stable, and predictable realizations for behavior cloning. • We pr”
- Authors: changti-wu; bin-yu; zhaolong-shen; et al.

## References

- `2510.03827` [LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization](https://arxiv.org/abs/2510.03827) (2025-10-04)
- `2510.10932` [DropVLA: An Action-Level Backdoor Attack on Vision-Language-Action Models](https://arxiv.org/abs/2510.10932) (2025-10-13)
- `2511.12149` [AttackVLA: Benchmarking Adversarial and Backdoor Attacks on Vision-Language-Action Models](https://arxiv.org/abs/2511.12149) (2025-11-15)
- `2601.04266` [State Backdoor: Towards Stealthy Real-world Poisoning Attack on Vision-Language-Action Model in State Space](https://arxiv.org/abs/2601.04266) (2026-01-07)
- `2601.14323` [SilentDrift: Exploiting Action Chunking for Stealthy Backdoor Attacks on Vision-Language-Action Models](https://arxiv.org/abs/2601.14323) (2026-01-20)
- `2602.00500` [Inject Once Survive Later: Backdooring Vision-Language-Action Models to Persist Through Downstream Fine-tuning](https://arxiv.org/abs/2602.00500) (2026-01-31)
- `2602.03153` [When Attention Betrays: Erasing Backdoor Attacks in Robotic Policies by Reconstructing Visual Tokens](https://arxiv.org/abs/2602.03153) (2026-02-03)
- `2606.04463` [OSCAR: Omni-Embodiment Action-Conditioned World Model for Robotics](https://arxiv.org/abs/2606.04463) (2026-06-03)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.09499` [Targeting World Models to Compromise Robot Learning Pipelines](https://arxiv.org/abs/2606.09499) (2026-06-08)
- `2606.16208` [ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208) (2026-06-15)
- `2606.28320` [WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320) (2026-06-26)
- `2607.04146` [!Imperio, smolVLA: The Implications of Data Poisoning on Open Source Robotics](https://arxiv.org/abs/2607.04146) (2026-07-05)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
- `2607.12571` [TrustVLA: Mechanism-Guided Inference-Time Defense Against Vision-Language-Action Backdoors](https://arxiv.org/abs/2607.12571) (2026-07-14)
