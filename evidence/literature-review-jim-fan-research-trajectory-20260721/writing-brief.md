# Writing Brief: Jim Fan research trajectory: general agents, embodied intelligence, foundation models, and open-world learning

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: Jim Fan research trajectory: general agents, embodied intelligence, foundation models, and open-world learning
- Time range: 2010-01-01..2026-07-21
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-4D`, `EA-ALIGN`, `EA-DATA`
- Review mode: scoping
- Paper-level sources: 17 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 17

## 下一阶段写作决策

### 推荐中心论点

Jim Fan 署名工作的连续性，不宜写成“从游戏走向机器人”的简单时间线，更准确的表述是：团队持续把通用智能体所需的接口逐层外显——先解决规模化训练与实验系统，再处理视觉/形态/提示泛化，随后引入自动课程、程序技能和奖励设计，最后把 VLA、异构数据与 world model 接入真实机器人。每一次扩展都扩大了任务范围，也暴露出新的接口依赖：Minecraft API、仿真状态、高层 primitive、domain randomization、目标机器人 post-training 和短时实机评测。

这是一条“能力扩展与证据门槛同步上升”的路线，而不是一连串单向胜利。写作时应把 DrEureka 的 plain-Eureka 实机失败、CaP-X 的 abstraction masking、BadRobot 的安全缺口、DreamDojo 的 admissibility 边界放在主论证内部，不能集中到结尾的免责声明。

### 推荐结构

1. 身份与证据边界：Linxi Fan / Linxi "Jim" Fan；NVIDIA 归属；职称冲突；署名不等于个人贡献。
2. 规模化系统方法：Ladder、Deep Speech 2、SURREAL，解释为何这些非具身论文仍构成方法论前史。
3. 泛化接口的形成：iGibson、SECANT、LM interactive decision-making、MetaMorph、VIMA。
4. 开放世界 scaffold：MineDojo → Voyager，重点写任务、奖励、技能库和反馈，而不把 Minecraft 指标外推到物理世界。
5. 自动 reward 与 sim-to-real：Eureka → DrEureka，以 plain Eureka 实机失败作为转折点。
6. Physical AI stack：GR00T N1、DreamDojo、CaP-X，分析 VLA、world model、code agent 与人工接口之间的边界。
7. 影响与未决问题：只讨论可验证的机制继承；独立复现、下游采用、闭环寿命、安全和个人贡献留给下一阶段。

### 事实标签

- `confirmed`：官方身份/机构记录；论文元数据；经全文审计的论文内结果。
- `inference`：五阶段划分；“接口逐层外显”这一跨论文综合判断；与知识卡的映射。
- `disputed`：当前具体职位名称。
- `evidence gap`：个人模块贡献、独立复现、长期真实闭环、失败恢复、成本、安全、引用/传播与实际技术影响之间的关系。

### 绝对不要升级的表述

- 不写“Jim Fan 独立发明/证明”，除非有可核验的个人贡献声明。
- 不把 Minecraft、程序 primitive 或 simulator-state reward 的表现称为真实机器人通用智能。
- 不把 GR00T N1 的两项短时桌面任务写成 generalist humanoid 已被实机证明。
- 不把 DreamDojo 在 20 个水果装袋场景上的相关性写成 world model 已可普遍替代真实评测。
- 不用引用量、社交传播或公司演示替代技术有效性。

### 下一阶段研究问题

1. 代表性项目的独立复现与真实下游采用链。
2. API/primitive 抽象度对 agent 能力评测的混淆程度。
3. 真实、人类视频与合成数据的公平消融、负迁移和样本效率。
4. world-model admissibility 的 action/physics/failure/sim-real 门槛。
5. 基于贡献声明、代码与项目记录的个人—团队贡献图。

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-MODEL`: The Ladder Network ablation shows that its components contribute unequally: lateral connections and reconstruction are... ([1511.06430](https://arxiv.org/abs/1511.06430) / [EA-JIMFAN-READ-0001](evidence-appendix.md#ea-jimfan-read-0001)) ⟷ CaP-X shows that high-level robot primitives can inflate coding-agent success while masking failures in lower-level per... ([2603.22435](https://arxiv.org/abs/2603.22435) / [EA-JIMFAN-READ-0016](evidence-appendix.md#ea-jimfan-read-0016))
- `EA-MODEL`: Deep Speech 2 links model progress to joint scaling of data, model size, high-performance training, and deployable infe... ([1512.02595](https://arxiv.org/abs/1512.02595) / [EA-JIMFAN-READ-0002](evidence-appendix.md#ea-jimfan-read-0002)) ⟷ SECANT decouples policy optimization from robust visual representation learning by cloning a weakly augmented RL expert... ([2106.09678](https://arxiv.org/abs/2106.09678) / [EA-JIMFAN-READ-0005](evidence-appendix.md#ea-jimfan-read-0005))
- `EA-MODEL`: SURREAL-System treats distributed-RL infrastructure as an experimental variable: replay sharding and actor batching rem... ([1909.12989](https://arxiv.org/abs/1909.12989) / [EA-JIMFAN-READ-0003](evidence-appendix.md#ea-jimfan-read-0003)) ⟷ For the tested interactive tasks, sequential representation and pretrained transformer initialization matter more than... ([2202.01771](https://arxiv.org/abs/2202.01771) / [EA-JIMFAN-READ-0006](evidence-appendix.md#ea-jimfan-read-0006))
- `EA-MODEL`: Voyager's automatic curriculum, executable skill library, and iterative environment feedback jointly support sustained... ([2305.16291](https://arxiv.org/abs/2305.16291) / [EA-JIMFAN-READ-0010](evidence-appendix.md#ea-jimfan-read-0010)) ⟷ MetaMorph shows that conditioning a transformer controller on morphology can support zero-shot transfer within a modula... ([2203.11931](https://arxiv.org/abs/2203.11931) / [EA-JIMFAN-READ-0007](evidence-appendix.md#ea-jimfan-read-0007))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-4D (1 events)
- [`conditional`] DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and planning benefits after robot post-training. ([2602.06949](https://arxiv.org/abs/2602.06949) / [EA-JIMFAN-READ-0015](evidence-appendix.md#ea-jimfan-read-0015))

### EA-ALIGN (1 events)
- [`limit`] BadRobot demonstrates that embodied LLM systems can be jailbroken into unsafe actions and that two tested defenses only partially mitigate the attacks. ([2407.20242](https://arxiv.org/abs/2407.20242) / [EA-JIMFAN-READ-0013](evidence-appendix.md#ea-jimfan-read-0013))

### EA-DATA (1 events)
- [`support`] MineDojo combines a large Minecraft task suite, internet-derived multimodal knowledge, and MineCLIP reward learning to support open-ended agent research. ([2206.08853](https://arxiv.org/abs/2206.08853) / [EA-JIMFAN-READ-0008](evidence-appendix.md#ea-jimfan-read-0008))

### EA-EVAL (1 events)
- [`conditional`] iGibson provides interactive household simulation, sensor generation, domain randomization, planning, and demonstration tools, with a bounded LiDAR sim-to-real navigation result. ([2012.02924](https://arxiv.org/abs/2012.02924) / [EA-JIMFAN-READ-0004](evidence-appendix.md#ea-jimfan-read-0004))

### EA-MODEL (13 events)
- [`support`] The Ladder Network ablation shows that its components contribute unequally: lateral connections and reconstruction are especially important in the tested semi-supervised setting. ([1511.06430](https://arxiv.org/abs/1511.06430) / [EA-JIMFAN-READ-0001](evidence-appendix.md#ea-jimfan-read-0001))
- [`support`] Deep Speech 2 links model progress to joint scaling of data, model size, high-performance training, and deployable inference rather than to architecture alone. ([1512.02595](https://arxiv.org/abs/1512.02595) / [EA-JIMFAN-READ-0002](evidence-appendix.md#ea-jimfan-read-0002))
- [`support`] SURREAL-System treats distributed-RL infrastructure as an experimental variable: replay sharding and actor batching remove concrete throughput bottlenecks. ([1909.12989](https://arxiv.org/abs/1909.12989) / [EA-JIMFAN-READ-0003](evidence-appendix.md#ea-jimfan-read-0003))
- [`support`] Voyager's automatic curriculum, executable skill library, and iterative environment feedback jointly support sustained in-context exploration in Minecraft. ([2305.16291](https://arxiv.org/abs/2305.16291) / [EA-JIMFAN-READ-0010](evidence-appendix.md#ea-jimfan-read-0010))
- [`conditional`] SECANT decouples policy optimization from robust visual representation learning by cloning a weakly augmented RL expert into a strongly augmented student. ([2106.09678](https://arxiv.org/abs/2106.09678) / [EA-JIMFAN-READ-0005](evidence-appendix.md#ea-jimfan-read-0005))
- [`conditional`] For the tested interactive tasks, sequential representation and pretrained transformer initialization matter more than whether the input sequence uses natural-language semantics. ([2202.01771](https://arxiv.org/abs/2202.01771) / [EA-JIMFAN-READ-0006](evidence-appendix.md#ea-jimfan-read-0006))
- [`conditional`] MetaMorph shows that conditioning a transformer controller on morphology can support zero-shot transfer within a modular robot design space. ([2203.11931](https://arxiv.org/abs/2203.11931) / [EA-JIMFAN-READ-0007](evidence-appendix.md#ea-jimfan-read-0007))
- [`conditional`] VIMA's multimodal-prompt policy and object-centric tokenization improve data efficiency and progressive generalization on its simulated tabletop benchmark. ([2210.03094](https://arxiv.org/abs/2210.03094) / [EA-JIMFAN-READ-0009](evidence-appendix.md#ea-jimfan-read-0009))
- [`conditional`] Eureka's evolutionary search over LLM-generated reward code reaches or exceeds human-designed rewards on most tasks in its simulated suites. ([2310.12931](https://arxiv.org/abs/2310.12931) / [EA-JIMFAN-READ-0011](evidence-appendix.md#ea-jimfan-read-0011))
- [`conditional`] DrEureka automates both reward and domain-randomization design for two real-robot settings, while plain Eureka fails the real locomotion transfer. ([2406.01967](https://arxiv.org/abs/2406.01967) / [EA-JIMFAN-READ-0012](evidence-appendix.md#ea-jimfan-read-0012))
- [`conditional`] GR00T N1 combines a vision-language System 2 with a diffusion-action System 1 and heterogeneous data, with bounded real humanoid manipulation results. ([2503.14734](https://arxiv.org/abs/2503.14734) / [EA-JIMFAN-READ-0014](evidence-appendix.md#ea-jimfan-read-0014))
- [`limit`] CaP-X shows that high-level robot primitives can inflate coding-agent success while masking failures in lower-level perception, geometry, and control reasoning. ([2603.22435](https://arxiv.org/abs/2603.22435) / [EA-JIMFAN-READ-0016](evidence-appendix.md#ea-jimfan-read-0016))
- [`gap`] A 2026 position paper argues that VLAs and world models remain incomplete without interfaces for physical data, cross-embodiment retargeting, grounded consequences, rewards, and deployment feedback. ([2606.06556](https://arxiv.org/abs/2606.06556) / [EA-JIMFAN-READ-0017](evidence-appendix.md#ea-jimfan-read-0017))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and planning benefits after robot post-training. ([2602.06949](https://arxiv.org/abs/2602.06949) / [EA-JIMFAN-READ-0015](evidence-appendix.md#ea-jimfan-read-0015))
- `limit` BadRobot demonstrates that embodied LLM systems can be jailbroken into unsafe actions and that two tested defenses only partially mitigate the attacks. ([2407.20242](https://arxiv.org/abs/2407.20242) / [EA-JIMFAN-READ-0013](evidence-appendix.md#ea-jimfan-read-0013))
- `conditional` iGibson provides interactive household simulation, sensor generation, domain randomization, planning, and demonstration tools, with a bounded LiDAR sim-to-real navigation result. ([2012.02924](https://arxiv.org/abs/2012.02924) / [EA-JIMFAN-READ-0004](evidence-appendix.md#ea-jimfan-read-0004))
- `conditional` SECANT decouples policy optimization from robust visual representation learning by cloning a weakly augmented RL expert into a strongly augmented student. ([2106.09678](https://arxiv.org/abs/2106.09678) / [EA-JIMFAN-READ-0005](evidence-appendix.md#ea-jimfan-read-0005))
- `conditional` For the tested interactive tasks, sequential representation and pretrained transformer initialization matter more than whether the input sequence uses natural-language semantics. ([2202.01771](https://arxiv.org/abs/2202.01771) / [EA-JIMFAN-READ-0006](evidence-appendix.md#ea-jimfan-read-0006))
- `conditional` MetaMorph shows that conditioning a transformer controller on morphology can support zero-shot transfer within a modular robot design space. ([2203.11931](https://arxiv.org/abs/2203.11931) / [EA-JIMFAN-READ-0007](evidence-appendix.md#ea-jimfan-read-0007))
- `conditional` VIMA's multimodal-prompt policy and object-centric tokenization improve data efficiency and progressive generalization on its simulated tabletop benchmark. ([2210.03094](https://arxiv.org/abs/2210.03094) / [EA-JIMFAN-READ-0009](evidence-appendix.md#ea-jimfan-read-0009))
- `conditional` Eureka's evolutionary search over LLM-generated reward code reaches or exceeds human-designed rewards on most tasks in its simulated suites. ([2310.12931](https://arxiv.org/abs/2310.12931) / [EA-JIMFAN-READ-0011](evidence-appendix.md#ea-jimfan-read-0011))
- `conditional` DrEureka automates both reward and domain-randomization design for two real-robot settings, while plain Eureka fails the real locomotion transfer. ([2406.01967](https://arxiv.org/abs/2406.01967) / [EA-JIMFAN-READ-0012](evidence-appendix.md#ea-jimfan-read-0012))
- `conditional` GR00T N1 combines a vision-language System 2 with a diffusion-action System 1 and heterogeneous data, with bounded real humanoid manipulation results. ([2503.14734](https://arxiv.org/abs/2503.14734) / [EA-JIMFAN-READ-0014](evidence-appendix.md#ea-jimfan-read-0014))
- `limit` CaP-X shows that high-level robot primitives can inflate coding-agent success while masking failures in lower-level perception, geometry, and control reasoning. ([2603.22435](https://arxiv.org/abs/2603.22435) / [EA-JIMFAN-READ-0016](evidence-appendix.md#ea-jimfan-read-0016))
- `gap` A 2026 position paper argues that VLAs and world models remain incomplete without interfaces for physical data, cross-embodiment retargeting, grounded consequences, rewards, and deployment feedback. ([2606.06556](https://arxiv.org/abs/2606.06556) / [EA-JIMFAN-READ-0017](evidence-appendix.md#ea-jimfan-read-0017))

## Writer handoff

- Use `$embodied-ai-review-writer` with this brief, the accepted evidence JSONL, and `evidence-appendix.md`.
- The writer loads only the requested style reference and drafts each style independently from this evidence model.
- Generate `trace-map.json`, then pass the writer's editorial quality audit before settlement.

## 引用速查

- **正文引用 = 本轮 accepted evidence 中的 arXiv 论文链接**，例如 `[Voyager](https://arxiv.org/abs/2305.16291)` 或 `[DrEureka](https://arxiv.org/abs/2406.01967)`；读者点开即达论文。
- 事件级溯源留给 appendix:成稿正文不放 `evidence-appendix.md#...` 事件锚点;需要精确定位(章节/立场/置信)时,读者从 References 或 appendix 查。
- 本简报中每条证据给出 `论文链接 / 事件链接` 对:写作时**取前者入正文**,后者供你核对 locator 与 stance。
- Citation density and visible source format are style-specific; do not force a full bibliography into Xiaohongshu prose.
- 完整证据条目在 [evidence-appendix.md](evidence-appendix.md);事件映射由 `trace-map.json` 保存。
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`
