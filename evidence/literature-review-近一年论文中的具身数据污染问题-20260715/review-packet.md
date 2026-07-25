# Review Packet: 近一年论文中的具身数据污染问题

## Scope

- Topic: 近一年论文中的具身数据污染问题
- Time range: 2025-07-15..2026-07-15
- Review style: `survey`
- Knowledge IDs: `EA-DATA`, `EA-EVAL`, `EA-MODEL`
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
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: `EA-CONTAM-2026-0011`, `EA-CONTAM-2026-0013`, `EA-CONTAM-2026-0005`, `EA-CONTAM-2026-0012`, `EA-CONTAM-2026-0014`, `EA-CONTAM-2026-0008`, `EA-CONTAM-2026-0007`, `EA-CONTAM-2026-0003`, `EA-CONTAM-2026-0009`, `EA-CONTAM-2026-0001`, `EA-CONTAM-2026-0004`, `EA-CONTAM-2026-0010`
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
| `support` | 支持 | 2 |
| `conditional` | 条件成立 | 4 |
| `limit` | 限制/负面 | 9 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2510.03827: LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization | 2025-10-04 | limit | EA-CONTAM-2026-0007 |
| 2510.10932: DropVLA: An Action-Level Backdoor Attack on Vision-Language-Action Models | 2025-10-13 | limit | EA-CONTAM-2026-0003 |
| 2511.12149: AttackVLA: Benchmarking Adversarial and Backdoor Attacks on Vision-Language-Action Models | 2025-11-15 | limit | EA-CONTAM-2026-0009 |
| 2601.04266: State Backdoor: Towards Stealthy Real-world Poisoning Attack on Vision-Language-Action Model in State Space | 2026-01-07 | limit | EA-CONTAM-2026-0001 |
| 2601.14323: SilentDrift: Exploiting Action Chunking for Stealthy Backdoor Attacks on Vision-Language-Action Models | 2026-01-20 | limit | EA-CONTAM-2026-0004 |
| 2602.00500: Inject Once Survive Later: Backdooring Vision-Language-Action Models to Persist Through Downstream Fine-tuning | 2026-01-31 | limit | EA-CONTAM-2026-0010 |
| 2602.03153: When Attention Betrays: Erasing Backdoor Attacks in Robotic Policies by Reconstructing Visual Tokens | 2026-02-03 | conditional | EA-CONTAM-2026-0005 |
| 2606.04463: OSCAR: Omni-Embodiment Action-Conditioned World Model for Robotics | 2026-06-03 | support | EA-CONTAM-2026-0011 |
| 2606.04825: HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning | 2026-06-03 | conditional | EA-CONTAM-2026-0012 |
| 2606.09499: Targeting World Models to Compromise Robot Learning Pipelines | 2026-06-08 | limit | EA-CONTAM-2026-0006 |
| 2606.16208: ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation | 2026-06-15 | support | EA-CONTAM-2026-0013 |
| 2606.28320: WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation | 2026-06-26 | conditional | EA-CONTAM-2026-0014 |
| 2607.04146: !Imperio, smolVLA: The Implications of Data Poisoning on Open Source Robotics | 2026-07-05 | limit | EA-CONTAM-2026-0002 |
| 2607.06442: SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | limit | EA-CONTAM-2026-0015 |
| 2607.12571: TrustVLA: Mechanism-Guided Inference-Time Defense Against Vision-Language-Action Backdoors | 2026-07-14 | conditional | EA-CONTAM-2026-0008 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-CONTAM-2026-0011 | EA-DATA | `support` | `direct` | 具身视频语料的重复不能只按片段数理解：同一场景中的相似任务会膨胀数据规模却几乎不增加场景多样性，因此去重应同时检查视觉与轨迹冗余。 | OSCAR 先按视觉相似性聚类，再按轨迹相似性核验；同场景但轨迹显著不同的片段不判为重复。 (4.3 Semantic Deduplication) | zhuoyuan-wu; jun-gao | 2606.04463 |
| EA-CONTAM-2026-0013 | EA-DATA | `support` | `direct` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 | ATHENA 指出 VLA 性能不只取决于规模，也取决于 demonstration quality，大规模冗余数据甚至可能伤害性能；在六任务真实机器人设置中，naive global influence ranking 让 Stack Bowls 只保留 13 条示教，而 MII 结合 task-local 和 cross-task influence utilities 后保留分布更均衡。 (C.4 Retention Balan... | tao-xu; jiaxin-wang; runhao-zhang; et al. | 2606.16208 |
| EA-CONTAM-2026-0005 | EA-DATA | `conditional` | `direct` | 视觉后门可通过深层注意力和潜特征异常做推理时定位，但与场景语义自然融合的触发物依然是明显盲点。 | Bera 对圆形块和棋盘格触发保持较低攻击成功，但语义合理的红色瓶盖触发更难被异常 token 方法区分。 (VI-E Trigger Proportions, Poisoning Ratios and Types) | xuetao-li; pinhan-fu; wenke-huang; et al. | 2602.03153 |
| EA-CONTAM-2026-0012 | EA-DATA | `conditional` | `direct` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 | 数据质量段明确记录了控制环同步、时间戳缺口检查、损坏轨迹剔除和 action-state consistency 检查。 (3.2 Synchronization and Data Quality Control) | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | 2606.04825 |
| EA-CONTAM-2026-0014 | EA-DATA | `conditional` | `direct` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 | 论文指出长程遥操作包含 pauses、fumbles 和 recoveries，整条 episode 过滤会丢失 otherwise suboptimal executions 中嵌入的 high-advantage segments，也无法剪掉保留示教中的局部 hesitation；WARP-RM 学习 dense relative progress 并用 WARP-BC upweight high-advantage action... | justin-yu; andrew-goldberg; kavish-kondap; et al. | 2606.28320 |
| EA-CONTAM-2026-0008 | EA-DATA | `conditional` | `direct` | 后门防御应把检测、因果定位和恢复分开计账；干净校准的内部机制监控对视觉触发有效，但不覆盖状态、语义或自适应后门。 | TrustVLA 通过内部证据异常、反事实支撑定位和局部修复降低所测视觉后门，作者明确限定了所需访问权限与攻击类型。 (5 Conclusion) | pinhan-fu; xianda-guo; xuetao-li; et al. | 2607.12571 |
| EA-CONTAM-2026-0007 | EA-DATA | `limit` | `direct` | LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 | LIBERO-PRO 在保持逻辑可执行的前提下改变物体位置与任务，标准设置中的高分模型在这些轻微改变下近乎崩溃。 (5.2 Main Results) | xueyang-zhou; yangming-xu; guiyao-tie; et al. | 2510.03827 |
| EA-CONTAM-2026-0003 | EA-DATA | `limit` | `direct` | 仅看 episode 成功率会漏掉动作级污染：后门可在关键短时窗覆写夹爪等可复用低层动作，即使整体任务表现仍显得正常。 | DropVLA 表明受影响的不必是整条轨迹；攻击可瞄准触发后极短时窗的安全关键动作。 (V Discussion) | zonghuan-xu; jiayu-li; yunhan-zhao; et al. | 2510.10932 |
| EA-CONTAM-2026-0009 | EA-DATA | `limit` | `direct` | 污染后门可以不只让机器人“失败”，而是在触发时执行攻击者指定的长程动作序列；真机已显示可行性，但强度低于仿真。 | BackdoorVLA 在 7-DoF Franka 上通过物理物体与文本触发定向长程行为，并同时保留一部分无触发任务性能。 (4.4 Attacks in Real-World Settings) | jiayu-li; yunhan-zhao; xiang-zheng; et al. | 2511.12149 |
| EA-CONTAM-2026-0001 | EA-DATA | `limit` | `direct` | 具身污染不只能藏在图像或文本中：污染真实示教里的初始关节状态可形成隐蔽 VLA 后门，并绕过视觉预处理防御。 | State Backdoor 将物理可行的初始状态偏移与恶意动作关联；剪枝与图像压缩都未能有效消除攻击。 (VI-E Robustness Evaluation) | ji-guo; wenbo-jiang; yansong-lin; et al. | 2601.04266 |
| EA-CONTAM-2026-0004 | EA-DATA | `limit` | `direct` | Action chunking 与 delta-pose 积分会把平滑、微小的污染偏差在开环执行窗内积累成失败，使“轨迹看起来平滑”不再是安全证据。 | SilentDrift 利用 action chunk 内缺少视觉纠正的结构性弱点，让动力学连续的小偏差持续积累。 (3.2 Vulnerability of Action Chunking to Drift Accumulation) | bingxin-xu; yuzhang-shang; binghui-wang; et al. | 2601.14323 |
| EA-CONTAM-2026-0010 | EA-DATA | `limit` | `direct` | 下游只用干净数据微调不能证明 VLA 已经没有污染；植入微调不敏感模块的基模型后门可穿过用户端的干净适配。 | INFUSE 在基模型分发前定向污染微调不敏感模块，干净下游微调后仍保持显著后门行为。 (5.2 Main Results) | jianyi-zhou; yujie-wei; ruichen-zhen; et al. | 2602.00500 |
| EA-CONTAM-2026-0006 | EA-DATA | `limit` | `direct` | 世界模型使数据污染变成“二次激活”问题：表面安全的遥操数据可在生成扩增时转化为危险轨迹，并污染下游政策。 | 论文在文本条件与动作条件世界模型中操纵预测，使恶意行为只在合成轨迹阶段出现。 (4 Identifying Vulnerabilities in the Robot Learning Supply Chain) | ethan-rathbun; ahmed-agha; saaduddin-mahmud; et al. | 2606.09499 |
| EA-CONTAM-2026-0002 | EA-DATA | `limit` | `direct` | 开源机器人数据供应链对极小比例的 episode 级投毒很敏感：在该真实拾放实验中，3 条投毒 episode 混入 320 条干净 episode 即实现触发式完全拒绝服务。 | 投毒数据将触发词与固定关节位置绑定；攻击在触发词出现时失效，干净提示行为保持。 (Abstract, opening paragraph) | stefan-bhler; mark-schutera | 2607.04146 |
| EA-CONTAM-2026-0015 | EA-DATA | `limit` | `direct` | SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 | 引言的贡献列表同时说明了结构暴露、学习友好轨迹选择和半量数据超过全量训练的结果。 (Introduction) | changti-wu; bin-yu; zhaolong-shen; et al. | 2607.06442 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-CONTAM-2026-0011 | zhuoyuan-wu; jun-gao | unlisted | `support` | 具身视频语料的重复不能只按片段数理解：同一场景中的相似任务会膨胀数据规模却几乎不增加场景多样性，因此去重应同时检查视觉与轨迹冗余。 |
| EA-CONTAM-2026-0013 | tao-xu; jiaxin-wang; runhao-zhang; et al. | unlisted | `support` | 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 |
| EA-CONTAM-2026-0005 | xuetao-li; pinhan-fu; wenke-huang; et al. | unlisted | `conditional` | 视觉后门可通过深层注意力和潜特征异常做推理时定位，但与场景语义自然融合的触发物依然是明显盲点。 |
| EA-CONTAM-2026-0012 | amirhosein-alian; yongqiang-zhao; shiyi-gu; et al. | unlisted | `conditional` | HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 |
| EA-CONTAM-2026-0014 | justin-yu; andrew-goldberg; kavish-kondap; et al. | unlisted | `conditional` | 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 |
| EA-CONTAM-2026-0008 | pinhan-fu; xianda-guo; xuetao-li; et al. | unlisted | `conditional` | 后门防御应把检测、因果定位和恢复分开计账；干净校准的内部机制监控对视觉触发有效，但不覆盖状态、语义或自适应后门。 |
| EA-CONTAM-2026-0007 | xueyang-zhou; yangming-xu; guiyao-tie; et al. | unlisted | `limit` | LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。 |
| EA-CONTAM-2026-0003 | zonghuan-xu; jiayu-li; yunhan-zhao; et al. | unlisted | `limit` | 仅看 episode 成功率会漏掉动作级污染：后门可在关键短时窗覆写夹爪等可复用低层动作，即使整体任务表现仍显得正常。 |
| EA-CONTAM-2026-0009 | jiayu-li; yunhan-zhao; xiang-zheng; et al. | unlisted | `limit` | 污染后门可以不只让机器人“失败”，而是在触发时执行攻击者指定的长程动作序列；真机已显示可行性，但强度低于仿真。 |
| EA-CONTAM-2026-0001 | ji-guo; wenbo-jiang; yansong-lin; et al. | unlisted | `limit` | 具身污染不只能藏在图像或文本中：污染真实示教里的初始关节状态可形成隐蔽 VLA 后门，并绕过视觉预处理防御。 |
| EA-CONTAM-2026-0004 | bingxin-xu; yuzhang-shang; binghui-wang; et al. | unlisted | `limit` | Action chunking 与 delta-pose 积分会把平滑、微小的污染偏差在开环执行窗内积累成失败，使“轨迹看起来平滑”不再是安全证据。 |
| EA-CONTAM-2026-0010 | jianyi-zhou; yujie-wei; ruichen-zhen; et al. | unlisted | `limit` | 下游只用干净数据微调不能证明 VLA 已经没有污染；植入微调不敏感模块的基模型后门可穿过用户端的干净适配。 |
| EA-CONTAM-2026-0006 | ethan-rathbun; ahmed-agha; saaduddin-mahmud; et al. | unlisted | `limit` | 世界模型使数据污染变成“二次激活”问题：表面安全的遥操数据可在生成扩增时转化为危险轨迹，并污染下游政策。 |
| EA-CONTAM-2026-0002 | stefan-bhler; mark-schutera | unlisted | `limit` | 开源机器人数据供应链对极小比例的 episode 级投毒很敏感：在该真实拾放实验中，3 条投毒 episode 混入 320 条干净 episode 即实现触发式完全拒绝服务。 |
| EA-CONTAM-2026-0015 | changti-wu; bin-yu; zhaolong-shen; et al. | unlisted | `limit` | SIEVE 按可复用原语组合和转换接口分配选择预算，再优先保留各组合模式中稳定、中心的轨迹；论文报告其用 50% 示教和 50% 训练步数可优于全量训练。 |

## Synthesis Slots

### 共识/正向证据
- `EA-CONTAM-2026-0011`: 具身视频语料的重复不能只按片段数理解：同一场景中的相似任务会膨胀数据规模却几乎不增加场景多样性，因此去重应同时检查视觉与轨迹冗余。
- `EA-CONTAM-2026-0013`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
### 条件成立
- `EA-CONTAM-2026-0005`: 视觉后门可通过深层注意力和潜特征异常做推理时定位，但与场景语义自然融合的触发物依然是明显盲点。
- `EA-CONTAM-2026-0012`: HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。
- `EA-CONTAM-2026-0014`: 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。
- `EA-CONTAM-2026-0008`: 后门防御应把检测、因果定位和恢复分开计账；干净校准的内部机制监控对视觉触发有效，但不覆盖状态、语义或自适应后门。
### 限制与失败模式
- `EA-CONTAM-2026-0007`: LIBERO 标准协议中训练与评测任务过度接近，会让记忆固定布局与动作映射的 VLA 获得过度乐观的泛化结论。
- `EA-CONTAM-2026-0003`: 仅看 episode 成功率会漏掉动作级污染：后门可在关键短时窗覆写夹爪等可复用低层动作，即使整体任务表现仍显得正常。
- `EA-CONTAM-2026-0009`: 污染后门可以不只让机器人“失败”，而是在触发时执行攻击者指定的长程动作序列；真机已显示可行性，但强度低于仿真。
- `EA-CONTAM-2026-0001`: 具身污染不只能藏在图像或文本中：污染真实示教里的初始关节状态可形成隐蔽 VLA 后门，并绕过视觉预处理防御。
- `EA-CONTAM-2026-0004`: Action chunking 与 delta-pose 积分会把平滑、微小的污染偏差在开环执行窗内积累成失败，使“轨迹看起来平滑”不再是安全证据。
- `EA-CONTAM-2026-0010`: 下游只用干净数据微调不能证明 VLA 已经没有污染；植入微调不敏感模块的基模型后门可穿过用户端的干净适配。
- `EA-CONTAM-2026-0006`: 世界模型使数据污染变成“二次激活”问题：表面安全的遥操数据可在生成扩增时转化为危险轨迹，并污染下游政策。
- `EA-CONTAM-2026-0002`: 开源机器人数据供应链对极小比例的 episode 级投毒很敏感：在该真实拾放实验中，3 条投毒 episode 混入 320 条干净 episode 即实现触发式完全拒绝服务。

## Source Gaps

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-CONTAM-2026-0011` 具身视频语料的重复不能只按片段数理解：同一场景中的相似任务会膨胀数据规模却几乎不增加场景多样性，因此去重应同时检查视觉与轨迹冗余。
  - `EA-CONTAM-2026-0013` 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。
  - `EA-CONTAM-2026-0005` 视觉后门可通过深层注意力和潜特征异常做推理时定位，但与场景语义自然融合的触发物依然是明显盲点。
- Scientific memo preview: 《近一年论文中的具身数据污染问题》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年论文中的具身数据污染问题 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年论文中的具身数据污染问题: 先看证据边界，再谈一个可传播的反常识洞察。

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
