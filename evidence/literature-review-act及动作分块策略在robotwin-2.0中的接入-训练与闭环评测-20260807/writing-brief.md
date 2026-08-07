# Writing Brief: ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: ACT及动作分块策略在RoboTwin 2.0中的接入、训练与闭环评测
- Time range: 2026-02-07..2026-08-07
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-ALIGN`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-MODEL`: 把 ACT 接入多任务双臂场景时，可在编码器加入稀疏专家路由，并用语言条件 FiLM 与多尺度交叉注意力约束动作解码，从而降低不同任务动作分布的相互干扰。 ([2603.15265](https://arxiv.org/abs/2603.15265) / [EA-ACTRT-2026-0002](evidence-appendix.md#ea-actrt-2026-0002)) ⟷ 动作分块策略的预测长度与实际执行长度应分开配置；在 RoboTwin 2.0 等闭环任务中，固定执行视界具有任务依赖且非单调的风险，PACE 以动作速度曲线中的低速相位边界在线选择重规划点。 ([2606.00537](https://arxiv.org/abs/2606.00537) / [EA-ACTRT-2026-0001](evidence-appendix.md#ea-actrt-2026-0001))
- `EA-MODEL`: 双臂动作分块可以与未来几何预测联合训练：策略融合 3D 几何潜变量、2D 语义和本体状态，并由扩散模型同时预测未来动作块与可解码的未来 3D 场景潜变量。 ([2602.23814](https://arxiv.org/abs/2602.23814) / [EA-ACTRT-2026-0003](evidence-appendix.md#ea-actrt-2026-0003)) ⟷ 多任务动作分块不必只在连续空间直接回归；VQActFlow 先把动作块编码为离散代码，再用变分流匹配生成代码序列，使语言任务模式与场景可行性可以在推理时分别施加引导。 ([2606.21600](https://arxiv.org/abs/2606.21600) / [EA-ACTRT-2026-0004](evidence-appendix.md#ea-actrt-2026-0004))
- `EA-MODEL`: 动作块越长并不总是越好：长块降低闭环反应性，短块增加跨块模式跳变；AAC 用当前预测的动作熵在线调节执行块长度，以平衡一致性与反应性。 ([2604.04161](https://arxiv.org/abs/2604.04161) / [EA-ACTRT-2026-0005](evidence-appendix.md#ea-actrt-2026-0005)) ⟷ 动作块的不确定性可以按“整个将执行前缀”联合校准，而非只估计单步误差；JCAC 为冻结策略增加轻量残差尺度头并输出具有用户指定覆盖水平的动作块集合。 ([2607.08575](https://arxiv.org/abs/2607.08575) / [EA-ACTRT-2026-0008](evidence-appendix.md#ea-actrt-2026-0008))
- `EA-MODEL`: 对流匹配动作策略，末端去噪步骤中干净动作估计的方差可作为重规划信号：DVAC 执行低方差稳定前缀，并在高方差未来动作被提交前重新观测与规划。 ([2606.03847](https://arxiv.org/abs/2606.03847) / [EA-ACTRT-2026-0006](evidence-appendix.md#ea-actrt-2026-0006)) ⟷ 执行视界可以由冻结动作策略之外的轻量模块学习：DEHP 用在线强化学习根据当前观测和预测动作块决定何时重规划，并在精细阶段缩短视界、自由空间运动中延长视界。 ([2606.11408](https://arxiv.org/abs/2606.11408) / [EA-ACTRT-2026-0009](evidence-appendix.md#ea-actrt-2026-0009))
- `EA-MODEL`: 世界预测与动作执行不必保持同一时间分辨率；AHA-WAM 将低频视频规划器与高频短动作块执行器解耦，并通过观测引导的上下文路由在闭环执行时复用长时世界上下文。 ([2606.09811](https://arxiv.org/abs/2606.09811) / [EA-ACTRT-2026-0007](evidence-appendix.md#ea-actrt-2026-0007)) ⟷ 交互纠错可从单步监督扩展到动作块集合监督：Set-Supervised Diffusion Policy 将正负动作块逐时刻构造成期望动作集合，再训练扩散策略生成落入该集合的动作块。 ([2606.01865](https://arxiv.org/abs/2606.01865) / [EA-ACTRT-2026-0010](evidence-appendix.md#ea-actrt-2026-0010))
- `EA-MODEL`: 固定执行视界会把重规划变成与任务阶段无关的周期调度；BCP 把视界选择分解为有序的继续/重规划决策，并用轨迹级强化学习同时优化成功与 VLA 调用效率。 ([2608.03483](https://arxiv.org/abs/2608.03483) / [EA-ACTRT-2026-0012](evidence-appendix.md#ea-actrt-2026-0012)) ⟷ 长动作块的开环脆弱性可以在块内缓解：DREAM-Chunk 并行采样多个候选动作块，用轻量潜在世界模型预测各自未来，并依据预测潜状态与真实观测的匹配在线选择动作。 ([2606.18589](https://arxiv.org/abs/2606.18589) / [EA-ACTRT-2026-0011](evidence-appendix.md#ea-actrt-2026-0011))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-MODEL (15 events)
- [`support`] 双臂动作分块可以与未来几何预测联合训练：策略融合 3D 几何潜变量、2D 语义和本体状态，并由扩散模型同时预测未来动作块与可解码的未来 3D 场景潜变量。 ([2602.23814](https://arxiv.org/abs/2602.23814) / [EA-ACTRT-2026-0003](evidence-appendix.md#ea-actrt-2026-0003))
- [`support`] 把 ACT 接入多任务双臂场景时，可在编码器加入稀疏专家路由，并用语言条件 FiLM 与多尺度交叉注意力约束动作解码，从而降低不同任务动作分布的相互干扰。 ([2603.15265](https://arxiv.org/abs/2603.15265) / [EA-ACTRT-2026-0002](evidence-appendix.md#ea-actrt-2026-0002))
- [`support`] 动作块越长并不总是越好：长块降低闭环反应性，短块增加跨块模式跳变；AAC 用当前预测的动作熵在线调节执行块长度，以平衡一致性与反应性。 ([2604.04161](https://arxiv.org/abs/2604.04161) / [EA-ACTRT-2026-0005](evidence-appendix.md#ea-actrt-2026-0005))
- [`support`] 对流匹配动作策略，末端去噪步骤中干净动作估计的方差可作为重规划信号：DVAC 执行低方差稳定前缀，并在高方差未来动作被提交前重新观测与规划。 ([2606.03847](https://arxiv.org/abs/2606.03847) / [EA-ACTRT-2026-0006](evidence-appendix.md#ea-actrt-2026-0006))
- [`support`] 世界预测与动作执行不必保持同一时间分辨率；AHA-WAM 将低频视频规划器与高频短动作块执行器解耦，并通过观测引导的上下文路由在闭环执行时复用长时世界上下文。 ([2606.09811](https://arxiv.org/abs/2606.09811) / [EA-ACTRT-2026-0007](evidence-appendix.md#ea-actrt-2026-0007))
- [`support`] 固定执行视界会把重规划变成与任务阶段无关的周期调度；BCP 把视界选择分解为有序的继续/重规划决策，并用轨迹级强化学习同时优化成功与 VLA 调用效率。 ([2608.03483](https://arxiv.org/abs/2608.03483) / [EA-ACTRT-2026-0012](evidence-appendix.md#ea-actrt-2026-0012))
- [`conditional`] 世界动作模型可以在训练时联合学习动作块与未来视频、在部署时只解码动作：GigaWorld-Policy 用因果掩码阻止未来视频 token 反向影响动作 token，使视频生成成为可选推理分支。 ([2603.17240](https://arxiv.org/abs/2603.17240) / [EA-ACTRT-2026-0015](evidence-appendix.md#ea-actrt-2026-0015))
- [`conditional`] 世界动作模型的执行长度可以由“想象—现实一致性”决定：FFDC 联合读取预测动作、预测视觉动态、真实观测和语言，继续执行可信片段并在偏差出现时提前重规划。 ([2605.06222](https://arxiv.org/abs/2605.06222) / [EA-ACTRT-2026-0013](evidence-appendix.md#ea-actrt-2026-0013))
- [`conditional`] 跨动作块闭环控制需要保留由机器人自身动作更新的场景状态；EvoScene-VLA 让动作解码器同时输出动作块和紧凑场景更新，并在下一次视觉调用中用新观测校正这一先验。 ([2605.21862](https://arxiv.org/abs/2605.21862) / [EA-ACTRT-2026-0014](evidence-appendix.md#ea-actrt-2026-0014))
- [`conditional`] 交互纠错可从单步监督扩展到动作块集合监督：Set-Supervised Diffusion Policy 将正负动作块逐时刻构造成期望动作集合，再训练扩散策略生成落入该集合的动作块。 ([2606.01865](https://arxiv.org/abs/2606.01865) / [EA-ACTRT-2026-0010](evidence-appendix.md#ea-actrt-2026-0010))
- [`conditional`] 执行视界可以由冻结动作策略之外的轻量模块学习：DEHP 用在线强化学习根据当前观测和预测动作块决定何时重规划，并在精细阶段缩短视界、自由空间运动中延长视界。 ([2606.11408](https://arxiv.org/abs/2606.11408) / [EA-ACTRT-2026-0009](evidence-appendix.md#ea-actrt-2026-0009))
- [`conditional`] 长动作块的开环脆弱性可以在块内缓解：DREAM-Chunk 并行采样多个候选动作块，用轻量潜在世界模型预测各自未来，并依据预测潜状态与真实观测的匹配在线选择动作。 ([2606.18589](https://arxiv.org/abs/2606.18589) / [EA-ACTRT-2026-0011](evidence-appendix.md#ea-actrt-2026-0011))
- [`conditional`] 多任务动作分块不必只在连续空间直接回归；VQActFlow 先把动作块编码为离散代码，再用变分流匹配生成代码序列，使语言任务模式与场景可行性可以在推理时分别施加引导。 ([2606.21600](https://arxiv.org/abs/2606.21600) / [EA-ACTRT-2026-0004](evidence-appendix.md#ea-actrt-2026-0004))
- [`conditional`] 动作块的不确定性可以按“整个将执行前缀”联合校准，而非只估计单步误差；JCAC 为冻结策略增加轻量残差尺度头并输出具有用户指定覆盖水平的动作块集合。 ([2607.08575](https://arxiv.org/abs/2607.08575) / [EA-ACTRT-2026-0008](evidence-appendix.md#ea-actrt-2026-0008))
- [`limit`] 动作分块策略的预测长度与实际执行长度应分开配置；在 RoboTwin 2.0 等闭环任务中，固定执行视界具有任务依赖且非单调的风险，PACE 以动作速度曲线中的低速相位边界在线选择重规划点。 ([2606.00537](https://arxiv.org/abs/2606.00537) / [EA-ACTRT-2026-0001](evidence-appendix.md#ea-actrt-2026-0001))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 世界动作模型可以在训练时联合学习动作块与未来视频、在部署时只解码动作：GigaWorld-Policy 用因果掩码阻止未来视频 token 反向影响动作 token，使视频生成成为可选推理分支。 ([2603.17240](https://arxiv.org/abs/2603.17240) / [EA-ACTRT-2026-0015](evidence-appendix.md#ea-actrt-2026-0015))
- `conditional` 世界动作模型的执行长度可以由“想象—现实一致性”决定：FFDC 联合读取预测动作、预测视觉动态、真实观测和语言，继续执行可信片段并在偏差出现时提前重规划。 ([2605.06222](https://arxiv.org/abs/2605.06222) / [EA-ACTRT-2026-0013](evidence-appendix.md#ea-actrt-2026-0013))
- `conditional` 跨动作块闭环控制需要保留由机器人自身动作更新的场景状态；EvoScene-VLA 让动作解码器同时输出动作块和紧凑场景更新，并在下一次视觉调用中用新观测校正这一先验。 ([2605.21862](https://arxiv.org/abs/2605.21862) / [EA-ACTRT-2026-0014](evidence-appendix.md#ea-actrt-2026-0014))
- `conditional` 交互纠错可从单步监督扩展到动作块集合监督：Set-Supervised Diffusion Policy 将正负动作块逐时刻构造成期望动作集合，再训练扩散策略生成落入该集合的动作块。 ([2606.01865](https://arxiv.org/abs/2606.01865) / [EA-ACTRT-2026-0010](evidence-appendix.md#ea-actrt-2026-0010))
- `conditional` 执行视界可以由冻结动作策略之外的轻量模块学习：DEHP 用在线强化学习根据当前观测和预测动作块决定何时重规划，并在精细阶段缩短视界、自由空间运动中延长视界。 ([2606.11408](https://arxiv.org/abs/2606.11408) / [EA-ACTRT-2026-0009](evidence-appendix.md#ea-actrt-2026-0009))
- `conditional` 长动作块的开环脆弱性可以在块内缓解：DREAM-Chunk 并行采样多个候选动作块，用轻量潜在世界模型预测各自未来，并依据预测潜状态与真实观测的匹配在线选择动作。 ([2606.18589](https://arxiv.org/abs/2606.18589) / [EA-ACTRT-2026-0011](evidence-appendix.md#ea-actrt-2026-0011))
- `conditional` 多任务动作分块不必只在连续空间直接回归；VQActFlow 先把动作块编码为离散代码，再用变分流匹配生成代码序列，使语言任务模式与场景可行性可以在推理时分别施加引导。 ([2606.21600](https://arxiv.org/abs/2606.21600) / [EA-ACTRT-2026-0004](evidence-appendix.md#ea-actrt-2026-0004))
- `conditional` 动作块的不确定性可以按“整个将执行前缀”联合校准，而非只估计单步误差；JCAC 为冻结策略增加轻量残差尺度头并输出具有用户指定覆盖水平的动作块集合。 ([2607.08575](https://arxiv.org/abs/2607.08575) / [EA-ACTRT-2026-0008](evidence-appendix.md#ea-actrt-2026-0008))
- `limit` 动作分块策略的预测长度与实际执行长度应分开配置；在 RoboTwin 2.0 等闭环任务中，固定执行视界具有任务依赖且非单调的风险，PACE 以动作速度曲线中的低速相位边界在线选择重规划点。 ([2606.00537](https://arxiv.org/abs/2606.00537) / [EA-ACTRT-2026-0001](evidence-appendix.md#ea-actrt-2026-0001))

## Writer handoff

- Use `$embodied-ai-review-writer` with this brief, the accepted evidence JSONL, and `evidence-appendix.md`.
- The writer loads only the requested style reference and drafts each style independently from this evidence model.
- Generate `trace-map.json`, then pass the writer's editorial quality audit before settlement.

## 引用速查

- **正文引用 = arXiv 论文链接**:`[2606.13877](https://arxiv.org/abs/2606.13877)` 或 `[SIEVE](https://arxiv.org/abs/2607.06442)`。读者点开即达论文。
- 事件级溯源留给 appendix:成稿正文不放 `evidence-appendix.md#...` 事件锚点;需要精确定位(章节/立场/置信)时,读者从 References 或 appendix 查。
- 本简报中每条证据给出 `论文链接 / 事件链接` 对:写作时**取前者入正文**,后者供你核对 locator 与 stance。
- Citation density and visible source format are style-specific; do not force a full bibliography into Xiaohongshu prose.
- 完整证据条目在 [evidence-appendix.md](evidence-appendix.md);事件映射由 `trace-map.json` 保存。
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`
