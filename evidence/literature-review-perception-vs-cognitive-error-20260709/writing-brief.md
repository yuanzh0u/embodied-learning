# Writing Brief: 具身数据感知误差与认知误差区别

> 本文件是写作输入,不是交付物。三篇成稿由 LLM 依此撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 References/appendix 溯源。

## 范围

- Topic: 具身数据感知误差与认知误差区别
- Time range: 2026-01-09..2026-07-09
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `EA-MODEL`
- Paper-level sources: 15 / 5 (formal-ready)
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `EA-DATA`: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002)) ⟷ 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- `EA-MODEL`: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-PVC-2026-0001](evidence-appendix.md#ea-pvc-2026-0001)) ⟷ 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))
- `EA-MODEL`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-PVC-2026-0003](evidence-appendix.md#ea-pvc-2026-0003)) ⟷ 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005))
- `EA-MODEL`: 感知正确不等于执行正确:VLA 的视觉骨干在扰动场景下仍保持准确空间表征,失败瓶颈在动作头塌缩到记忆轨迹——即 latent perception 与 motor execution 解耦,这是可与感知误差区分的下游错误。 ([2606.09740](https://arxiv.org/abs/2606.09740) / [EA-PVC-2026-0004](evidence-appendix.md#ea-pvc-2026-0004)) ⟷ 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))
- `EA-MODEL`: 纯反应式 VLA 的长程推理、时序 credit assignment 与误差复合问题源于缺少显式预测结构;世界模型既可作决策期评估器(认知层验证),其像素级 rollout 的长程误差积累又是自身的感知型缺陷,需符号结构缓解。 ([2605.00080](https://arxiv.org/abs/2605.00080) / [EA-PVC-2026-0006](evidence-appendix.md#ea-pvc-2026-0006)) ⟷ 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005))
- `EA-MODEL`: 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。 ([2607.00673](https://arxiv.org/abs/2607.00673) / [EA-PVC-2026-0007](evidence-appendix.md#ea-pvc-2026-0007)) ⟷ 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (5 events)
- [`support`] 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002))
- [`support`] 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002))
- [`conditional`] 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- [`conditional`] 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))

### EA-EVAL (1 events)
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004))

### EA-MODEL (7 events)
- [`support`] 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-PVC-2026-0001](evidence-appendix.md#ea-pvc-2026-0001))
- [`support`] 纯反应式 VLA 的长程推理、时序 credit assignment 与误差复合问题源于缺少显式预测结构;世界模型既可作决策期评估器(认知层验证),其像素级 rollout 的长程误差积累又是自身的感知型缺陷,需符号结构缓解。 ([2605.00080](https://arxiv.org/abs/2605.00080) / [EA-PVC-2026-0006](evidence-appendix.md#ea-pvc-2026-0006))
- [`support`] 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-PVC-2026-0003](evidence-appendix.md#ea-pvc-2026-0003))
- [`support`] 感知正确不等于执行正确:VLA 的视觉骨干在扰动场景下仍保持准确空间表征,失败瓶颈在动作头塌缩到记忆轨迹——即 latent perception 与 motor execution 解耦,这是可与感知误差区分的下游错误。 ([2606.09740](https://arxiv.org/abs/2606.09740) / [EA-PVC-2026-0004](evidence-appendix.md#ea-pvc-2026-0004))
- [`support`] 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。 ([2607.00673](https://arxiv.org/abs/2607.00673) / [EA-PVC-2026-0007](evidence-appendix.md#ea-pvc-2026-0007))
- [`conditional`] 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005))
- [`conditional`] 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))

### EA-SENSOR (1 events)
- [`limit`] 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))

### EA-XEMBODIMENT (1 events)
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `conditional` 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `conditional` 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005))
- `conditional` 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))
- `limit` 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

## 三种风格的读者与语气

- `scientific-memo_keyan.md` 研究者读:中心论点 → 派生矛盾/机制(prose 小节) → 可操作框架 → 最短结论。引用密集,每个实质论断带论文链接。
- `zhihu-explainer_zhihu.md` 技术公众读:先破一个具体误区 → 讲机制(用比喻可以,升级 stance 不可以) → 给适用边界 → 延伸阅读。
- `xiaohongshu-post_xiaohongshu.md` 泛兴趣读者:一个钩子 → 3-5 条反常识洞察(每条一句话+论文链接) → 一句可见的 caveat → 一行来源说明。

## 引用速查

- **正文引用 = arXiv 论文链接**:`[2606.13877](https://arxiv.org/abs/2606.13877)` 或 `[SIEVE](https://arxiv.org/abs/2607.06442)`。读者点开即达论文。
- 事件级溯源留给 appendix:成稿正文不放 `evidence-appendix.md#...` 事件锚点;需要精确定位(章节/立场/置信)时,读者从 References 或 appendix 查。
- 本简报中每条证据给出 `论文链接 / 事件链接` 对:写作时**取前者入正文**,后者供你核对 locator 与 stance。
- 成稿末尾必须有 `## References` 节(去重论文清单,含链接);完整证据条目在 [evidence-appendix.md](evidence-appendix.md)。
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`
