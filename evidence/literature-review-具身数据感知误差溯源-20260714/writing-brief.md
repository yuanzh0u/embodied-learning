# Writing Brief: 具身数据感知误差溯源

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 具身数据感知误差溯源
- Time range: 2026-01-14..2026-07-14
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-EVAL`, `ERR-PATTERN`, `ERR-EMBODIED`
- Review mode: scoping
- Paper-level sources: 32 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 33

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002)) ⟷ VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- `EA-DATA`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001)) ⟷ 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `EA-DATA`: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002)) ⟷ 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `EA-DATA`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003)) ⟷ 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `EA-EVAL`: 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004)) ⟷ 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-EVAL-2026-0007](evidence-appendix.md#ea-eval-2026-0007))
- `EA-MODEL`: 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-PVC-2026-0001](evidence-appendix.md#ea-pvc-2026-0001)) ⟷ 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005))
- `EA-MODEL`: 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-PVC-2026-0003](evidence-appendix.md#ea-pvc-2026-0003)) ⟷ 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))
- `EA-MODEL`: 感知正确不等于执行正确:VLA 的视觉骨干在扰动场景下仍保持准确空间表征,失败瓶颈在动作头塌缩到记忆轨迹——即 latent perception 与 motor execution 解耦,这是可与感知误差区分的下游错误。 ([2606.09740](https://arxiv.org/abs/2606.09740) / [EA-PVC-2026-0004](evidence-appendix.md#ea-pvc-2026-0004)) ⟷ 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (11 events)
- [`support`] 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([2603.09056](https://arxiv.org/abs/2603.09056) / [EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001))
- [`support`] 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([2605.01544](https://arxiv.org/abs/2605.01544) / [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003))
- [`support`] 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([2605.26349](https://arxiv.org/abs/2605.26349) / [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002))
- [`support`] 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [EA-DATA-2026-DQ-0002](evidence-appendix.md#ea-data-2026-dq-0002))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- [`conditional`] 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- [`conditional`] 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- [`conditional`] 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- [`conditional`] 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))
- [`limit`] VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))

### EA-EVAL (3 events)
- [`support`] 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 ([2607.02642](https://arxiv.org/abs/2607.02642) / [EA-EVAL-2026-DQ-0004](evidence-appendix.md#ea-eval-2026-dq-0004))
- [`limit`] 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-EVAL-2026-0007](evidence-appendix.md#ea-eval-2026-0007))
- [`gap`] 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 ([2607.07196](https://arxiv.org/abs/2607.07196) / [EA-EVAL-2026-0012](evidence-appendix.md#ea-eval-2026-0012))

### EA-MODEL (7 events)
- [`support`] 长程规划、失败后自我纠正、少样本适应属于认知层能力;显式 CoT 能提升它们但推理延迟高,认知处理可以压缩为 latent 推理而保持规划与恢复能力。 ([2601.09708](https://arxiv.org/abs/2601.09708) / [EA-PVC-2026-0001](evidence-appendix.md#ea-pvc-2026-0001))
- [`support`] 纯反应式 VLA 的长程推理、时序 credit assignment 与误差复合问题源于缺少显式预测结构;世界模型既可作决策期评估器(认知层验证),其像素级 rollout 的长程误差积累又是自身的感知型缺陷,需符号结构缓解。 ([2605.00080](https://arxiv.org/abs/2605.00080) / [EA-PVC-2026-0006](evidence-appendix.md#ea-pvc-2026-0006))
- [`support`] 失败恢复可以把认知层(failure mode/recovery stage 判断与 reward 选择)与控制层(residual 纠正)分开;VLM 的失败分类错误由此成为与感知误差独立的认知误差来源。 ([2606.09630](https://arxiv.org/abs/2606.09630) / [EA-PVC-2026-0003](evidence-appendix.md#ea-pvc-2026-0003))
- [`support`] 感知正确不等于执行正确:VLA 的视觉骨干在扰动场景下仍保持准确空间表征,失败瓶颈在动作头塌缩到记忆轨迹——即 latent perception 与 motor execution 解耦,这是可与感知误差区分的下游错误。 ([2606.09740](https://arxiv.org/abs/2606.09740) / [EA-PVC-2026-0004](evidence-appendix.md#ea-pvc-2026-0004))
- [`support`] 感知没错计划也可能错:基于历史重建的地图在物理条件变化后失效,属于'未对未来世界状态做 what-if 推理'的认知/规划误差,与观测误差可区分;物理可行世界模型能在执行前暴露这类长程路线失败。 ([2607.00673](https://arxiv.org/abs/2607.00673) / [EA-PVC-2026-0007](evidence-appendix.md#ea-pvc-2026-0007))
- [`conditional`] 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005))
- [`conditional`] 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))

### EA-SENSOR (11 events)
- [`support`] Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 ([2606.18043](https://arxiv.org/abs/2606.18043) / [EA-SENSOR-2026-0004](evidence-appendix.md#ea-sensor-2026-0004))
- [`support`] VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 ([2606.20754](https://arxiv.org/abs/2606.20754) / [EA-SENSOR-2026-0003](evidence-appendix.md#ea-sensor-2026-0003))
- [`support`] 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 ([2606.28899](https://arxiv.org/abs/2606.28899) / [EA-SENSOR-2026-0006](evidence-appendix.md#ea-sensor-2026-0006))
- [`support`] RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 ([2606.29384](https://arxiv.org/abs/2606.29384) / [EA-SENSOR-2026-0011](evidence-appendix.md#ea-sensor-2026-0011))
- [`support`] 接触丰富任务中的小接触扰动会造成视觉难以发现的不可恢复失败；触觉世界模型可把真实失败转成可训练的局部纠正片段。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-0009](evidence-appendix.md#ea-sensor-2026-0009))
- [`support`] 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 ([2607.07287](https://arxiv.org/abs/2607.07287) / [EA-SENSOR-2026-0001](evidence-appendix.md#ea-sensor-2026-0001))
- [`conditional`] 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-SENSOR-2026-0002](evidence-appendix.md#ea-sensor-2026-0002))
- [`conditional`] 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-SENSOR-2026-0008](evidence-appendix.md#ea-sensor-2026-0008))
- [`conditional`] 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-SENSOR-2026-0010](evidence-appendix.md#ea-sensor-2026-0010))
- [`limit`] 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-SENSOR-2026-0005](evidence-appendix.md#ea-sensor-2026-0005))
- [`limit`] 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))

### EA-XEMBODIMENT (1 events)
- [`limit`] A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([2602.13197](https://arxiv.org/abs/2602.13197) / [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- `conditional` 点轨迹数据的瓶颈不是只在采集量，而在可见性、遮挡、深度和 embodiment 分割；真实操作中暂时被遮挡的关键物体点仍应保留监督信号。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-DATA-2026-4DDATA-0002](evidence-appendix.md#ea-data-2026-4ddata-0002))
- `conditional` 异构4D数据必须保留监督可靠性层级：机器人数据给可执行动作，人类/第一视角视频给视觉动态，UMI式数据给较弱的动作式信号，缺失模态不能强行当真值。 ([2606.01027](https://arxiv.org/abs/2606.01027) / [EA-DATA-2026-4DDATA-0010](evidence-appendix.md#ea-data-2026-4ddata-0010))
- `conditional` 多模态4D示教数据必须做同步、时间戳、动作-状态一致性、触觉标记跟踪和episode级切分；否则模型会混淆动作真值、接触信号和评测泄漏。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-DATA-2026-4DDATA-0018](evidence-appendix.md#ea-data-2026-4ddata-0018))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-DATA-2026-4DDATA-0014](evidence-appendix.md#ea-data-2026-4ddata-0014))
- `conditional` 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([2606.28320](https://arxiv.org/abs/2606.28320) / [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))
- `limit` VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 ([2607.06442](https://arxiv.org/abs/2607.06442) / [EA-DATA-2026-DQ-0001](evidence-appendix.md#ea-data-2026-dq-0001))
- `limit` 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-EVAL-2026-0007](evidence-appendix.md#ea-eval-2026-0007))
- `gap` 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 ([2607.07196](https://arxiv.org/abs/2607.07196) / [EA-EVAL-2026-0012](evidence-appendix.md#ea-eval-2026-0012))
- `conditional` 把视觉感知与动作推理解耦——假设感知已准确、让 LLM 专注 3D 空间中的动作推理——可以显著降低数据需求;但认知层误差会跨阶段传播,需要 inter-stage verification 拦截。 ([2602.21161](https://arxiv.org/abs/2602.21161) / [EA-PVC-2026-0005](evidence-appendix.md#ea-pvc-2026-0005))
- `conditional` 感知增强不自动带来更好的动作生成;高层语义推理只有转译成动作相关表示才有用,把 CoT 当动作前缀会引入 compounding errors,且 dense grounding 字段本身会受检测误差、标定偏差和遮挡污染。 ([2606.03784](https://arxiv.org/abs/2606.03784) / [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))
- `conditional` 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-SENSOR-2026-0002](evidence-appendix.md#ea-sensor-2026-0002))
- `conditional` 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-SENSOR-2026-0008](evidence-appendix.md#ea-sensor-2026-0008))
- `conditional` 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-SENSOR-2026-0010](evidence-appendix.md#ea-sensor-2026-0010))
- `limit` 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-SENSOR-2026-0005](evidence-appendix.md#ea-sensor-2026-0005))
- `limit` 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSOR-2026-DQ-0006](evidence-appendix.md#ea-sensor-2026-dq-0006))
- `limit` A recorded robot action is not a universal supervision signal: the same command can produce different motions across controllers, embodiments, hardware units, and deployment-time dynamics. ([2606.24049](https://arxiv.org/abs/2606.24049) / [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))

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
