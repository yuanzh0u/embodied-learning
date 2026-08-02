# Writing Brief: 近一年具身感知问题是否已有效解决

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年具身感知问题是否已有效解决
- Time range: 2025-07-14..2026-07-14
- Knowledge IDs: `EA-SENSOR`, `EA-4D`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 19 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 19

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [ERR-PVC-READ-0015](evidence-appendix.md#err-pvc-read-0015)) ⟷ 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))
- `EA-SENSOR`: 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 ([2607.07287](https://arxiv.org/abs/2607.07287) / [EA-SENSORERR-READ-0012](evidence-appendix.md#ea-sensorerr-read-0012)) ⟷ 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-SENSORERR-READ-0002](evidence-appendix.md#ea-sensorerr-read-0002))
- `EA-SENSOR`: VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 ([2606.20754](https://arxiv.org/abs/2606.20754) / [EA-SENSORERR-READ-0009](evidence-appendix.md#ea-sensorerr-read-0009)) ⟷ TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSORERR-READ-0001](evidence-appendix.md#ea-sensorerr-read-0001))
- `EA-SENSOR`: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 ([2606.18043](https://arxiv.org/abs/2606.18043) / [EA-SENSORERR-READ-0008](evidence-appendix.md#ea-sensorerr-read-0008)) ⟷ 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。 ([2601.08325](https://arxiv.org/abs/2601.08325) / [EA-PNAV-2026-0002](evidence-appendix.md#ea-pnav-2026-0002))
- `EA-SENSOR`: 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 ([2606.28899](https://arxiv.org/abs/2606.28899) / [EA-SENSORERR-READ-0010](evidence-appendix.md#ea-sensorerr-read-0010)) ⟷ OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 ([2603.11072](https://arxiv.org/abs/2603.11072) / [EA-PNAV-2026-0003](evidence-appendix.md#ea-pnav-2026-0003))
- `EA-SENSOR`: RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 ([2606.29384](https://arxiv.org/abs/2606.29384) / [EA-SENSORERR-READ-0011](evidence-appendix.md#ea-sensorerr-read-0011)) ⟷ 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 ([2605.14801](https://arxiv.org/abs/2605.14801) / [EA-PNAV-2026-0004](evidence-appendix.md#ea-pnav-2026-0004))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (3 events)
- [`support`] Lift3D-VLA 指出，纯 2D VLA 难以保真地表达可达性、遮挡、接触和随时间演化的几何约束，而现有 2D‑3D 转换又会损失几何保真度。 ([2607.06564](https://arxiv.org/abs/2607.06564) / [ERR-PVC-READ-0015](evidence-appendix.md#err-pvc-read-0015))
- [`conditional`] 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- [`limit`] 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))

### EA-SENSOR (16 events)
- [`support`] Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 ([2606.18043](https://arxiv.org/abs/2606.18043) / [EA-SENSORERR-READ-0008](evidence-appendix.md#ea-sensorerr-read-0008))
- [`support`] VLA 的感知-动作误差不只来自传感器本身，也来自分布外观测下模型无法给出可靠置信度；隐藏激活扰动产生的 epistemic signal 可用于失败检测。 ([2606.20754](https://arxiv.org/abs/2606.20754) / [EA-SENSORERR-READ-0009](evidence-appendix.md#ea-sensorerr-read-0009))
- [`support`] 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 ([2606.28899](https://arxiv.org/abs/2606.28899) / [EA-SENSORERR-READ-0010](evidence-appendix.md#ea-sensorerr-read-0010))
- [`support`] RGB-centric VLA 在照明变化导致的可见性退化下会暴露鲁棒性问题；事件流作为对照明更鲁棒、对运动敏感的补充观测，可以改善不同可见性水平下的动作预测。 ([2606.29384](https://arxiv.org/abs/2606.29384) / [EA-SENSORERR-READ-0011](evidence-appendix.md#ea-sensorerr-read-0011))
- [`support`] 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 ([2607.07287](https://arxiv.org/abs/2607.07287) / [EA-SENSORERR-READ-0012](evidence-appendix.md#ea-sensorerr-read-0012))
- [`conditional`] 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。 ([2601.08325](https://arxiv.org/abs/2601.08325) / [EA-PNAV-2026-0002](evidence-appendix.md#ea-pnav-2026-0002))
- [`conditional`] OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 ([2603.11072](https://arxiv.org/abs/2603.11072) / [EA-PNAV-2026-0003](evidence-appendix.md#ea-pnav-2026-0003))
- [`conditional`] 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 ([2605.14801](https://arxiv.org/abs/2605.14801) / [EA-PNAV-2026-0004](evidence-appendix.md#ea-pnav-2026-0004))
- [`conditional`] HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-SENSORERR-READ-0014](evidence-appendix.md#ea-sensorerr-read-0014))
- [`conditional`] 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-SENSORERR-READ-0007](evidence-appendix.md#ea-sensorerr-read-0007))
- [`conditional`] 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-SENSORERR-READ-0015](evidence-appendix.md#ea-sensorerr-read-0015))
- [`conditional`] 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-SENSORERR-READ-0003](evidence-appendix.md#ea-sensorerr-read-0003))
- [`conditional`] 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-SENSORERR-READ-0004](evidence-appendix.md#ea-sensorerr-read-0004))
- [`limit`] 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。 ([2606.10348](https://arxiv.org/abs/2606.10348) / [EA-PNAV-2026-0013](evidence-appendix.md#ea-pnav-2026-0013))
- [`limit`] 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-SENSORERR-READ-0002](evidence-appendix.md#ea-sensorerr-read-0002))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSORERR-READ-0001](evidence-appendix.md#ea-sensorerr-read-0001))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 3PoinTr 保留含暂时遮挡点的轨迹，只屏蔽不可见的单个点—时间损失，因而能继续利用操作中任务关键的物体点监督。 ([2603.08485](https://arxiv.org/abs/2603.08485) / [EA-4D-READ-0012](evidence-appendix.md#ea-4d-read-0012))
- `limit` 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))
- `conditional` 主动感知能改善固定视角VLA，但并未解决通用感知；论文在最难的组合泛化任务上仍报告明显退化。 ([2601.08325](https://arxiv.org/abs/2601.08325) / [EA-PNAV-2026-0002](evidence-appendix.md#ea-pnav-2026-0002))
- `conditional` OA-NBV证明机器人可以主动绕开遮挡获得更好观察，但作者明确把能力限定为单步视点选择，而非完整多视图感知。 ([2603.11072](https://arxiv.org/abs/2603.11072) / [EA-PNAV-2026-0003](evidence-appendix.md#ea-pnav-2026-0003))
- `conditional` 对零样本VLN而言，感知并非简单地“越准越已解决”：独立精度会出现边际饱和，而误检和框形变仍是关键失败源。 ([2605.14801](https://arxiv.org/abs/2605.14801) / [EA-PNAV-2026-0004](evidence-appendix.md#ea-pnav-2026-0004))
- `conditional` HapTile 的数据质量控制在机器人控制环中同步全部模态，检查空轨迹、损坏轨迹和时间戳缺口，并验证动作—状态一致性。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-SENSORERR-READ-0014](evidence-appendix.md#ea-sensorerr-read-0014))
- `conditional` 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-SENSORERR-READ-0007](evidence-appendix.md#ea-sensorerr-read-0007))
- `conditional` 如果目标包含扰动恢复，数据集必须显式收集nominal demonstrations和recovery interaction data；否则模型很难学习接触丢失后的再建立。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-SENSORERR-READ-0015](evidence-appendix.md#ea-sensorerr-read-0015))
- `conditional` 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-SENSORERR-READ-0003](evidence-appendix.md#ea-sensorerr-read-0003))
- `conditional` 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-SENSORERR-READ-0004](evidence-appendix.md#ea-sensorerr-read-0004))
- `limit` 开放词汇感知错误会形成系统性误导并持续污染地图与导航决策，因此标准检测能力并不等于具身感知已解决。 ([2606.10348](https://arxiv.org/abs/2606.10348) / [EA-PNAV-2026-0013](evidence-appendix.md#ea-pnav-2026-0013))
- `limit` 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-SENSORERR-READ-0002](evidence-appendix.md#ea-sensorerr-read-0002))
- `limit` TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSORERR-READ-0001](evidence-appendix.md#ea-sensorerr-read-0001))

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
