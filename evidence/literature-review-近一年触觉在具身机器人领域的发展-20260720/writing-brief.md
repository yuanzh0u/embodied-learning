# Writing Brief: 近一年触觉在具身机器人领域的发展

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年触觉在具身机器人领域的发展
- Time range: 2025-07-20..2026-07-20
- Knowledge IDs: `EA-SENSOR`, `EA-DATA`, `EA-MODEL`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 23 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 24

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-READ-0002](evidence-appendix.md#ea-twm-read-0002)) ⟷ 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-TWM-READ-0009](evidence-appendix.md#ea-twm-read-0009))
- `EA-DATA`: 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-READ-0003](evidence-appendix.md#ea-twm-read-0003)) ⟷ 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))
- `EA-DATA`: 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-READ-0004](evidence-appendix.md#ea-twm-read-0004)) ⟷ VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-READ-0001](evidence-appendix.md#ea-twm-read-0001))
- `EA-DATA`: 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-READ-0005](evidence-appendix.md#ea-twm-read-0005)) ⟷ 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-READ-0007](evidence-appendix.md#ea-twm-read-0007))
- `EA-DATA`: 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-READ-0006](evidence-appendix.md#ea-twm-read-0006)) ⟷ 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-TWM-READ-0010](evidence-appendix.md#ea-twm-read-0010))
- `EA-DATA`: TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 ([2604.07335](https://arxiv.org/abs/2604.07335) / [EA-TWM-READ-0008](evidence-appendix.md#ea-twm-read-0008)) ⟷ 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-TWM-READ-0011](evidence-appendix.md#ea-twm-read-0011))
- `EA-DATA`: Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 ([2606.18043](https://arxiv.org/abs/2606.18043) / [EA-TWM-READ-0015](evidence-appendix.md#ea-twm-read-0015)) ⟷ 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-TWM-READ-0014](evidence-appendix.md#ea-twm-read-0014))
- `EA-DATA`: 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 ([2607.05390](https://arxiv.org/abs/2607.05390) / [EA-UMI-READ-0015](evidence-appendix.md#ea-umi-read-0015)) ⟷ UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose,... ([2601.09988](https://arxiv.org/abs/2601.09988) / [EA-UMI-READ-0002](evidence-appendix.md#ea-umi-read-0002))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (17 events)
- [`support`] TAMEn 用动捕精度模式与 VR 便携模式平衡数据质量和环境多样性，并把人在环的触觉可视化恢复数据纳入金字塔式数据配方。 ([2604.07335](https://arxiv.org/abs/2604.07335) / [EA-TWM-READ-0008](evidence-appendix.md#ea-twm-read-0008))
- [`support`] 触觉数据的有效形态不止原始 tactile image，还包括 marker displacement 等显式接触几何与滑移特征。 ([2606.04825](https://arxiv.org/abs/2606.04825) / [EA-TWM-READ-0005](evidence-appendix.md#ea-twm-read-0005))
- [`support`] 触觉世界模型可以被扩展为同时生成未来视觉、未来触觉和动作 chunk 的世界动作模型。 ([2606.08737](https://arxiv.org/abs/2606.08737) / [EA-TWM-READ-0002](evidence-appendix.md#ea-twm-read-0002))
- [`support`] 腕部六维力/力矩可作为未来触觉 latent 的先行条件，用于预测短时域接触变化。 ([2606.11184](https://arxiv.org/abs/2606.11184) / [EA-TWM-READ-0006](evidence-appendix.md#ea-twm-read-0006))
- [`support`] 在接触丰富操作中，触觉世界模型的关键不是简单增加模态，而是让表征同时具备空间结构、时间连续性和跨模态兼容性。 ([2606.13877](https://arxiv.org/abs/2606.13877) / [EA-TWM-READ-0003](evidence-appendix.md#ea-twm-read-0003))
- [`support`] 触觉世界模型也可以在推理期作为候选动作验证器，而不只是训练期的动态模型。 ([2606.14981](https://arxiv.org/abs/2606.14981) / [EA-TWM-READ-0004](evidence-appendix.md#ea-twm-read-0004))
- [`support`] Flow-based VLA 在真实部署时缺少置信度机制会形成安全与恢复缺口；velocity-field disagreement 可把动作预测的不可靠性转成失败检测和主动微调信号。 ([2606.18043](https://arxiv.org/abs/2606.18043) / [EA-TWM-READ-0015](evidence-appendix.md#ea-twm-read-0015))
- [`support`] 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 ([2607.05390](https://arxiv.org/abs/2607.05390) / [EA-UMI-READ-0015](evidence-appendix.md#ea-umi-read-0015))
- [`conditional`] UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only dat... ([2601.09988](https://arxiv.org/abs/2601.09988) / [EA-UMI-READ-0002](evidence-appendix.md#ea-umi-read-0002))
- [`conditional`] VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-READ-0001](evidence-appendix.md#ea-twm-read-0001))
- [`conditional`] 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-READ-0007](evidence-appendix.md#ea-twm-read-0007))
- [`conditional`] 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-TWM-READ-0014](evidence-appendix.md#ea-twm-read-0014))
- [`conditional`] 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-TWM-READ-0010](evidence-appendix.md#ea-twm-read-0010))
- [`conditional`] 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-TWM-READ-0011](evidence-appendix.md#ea-twm-read-0011))
- [`limit`] 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-TWM-READ-0009](evidence-appendix.md#ea-twm-read-0009))
- [`limit`] 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))
- [`gap`] 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 ([2607.07196](https://arxiv.org/abs/2607.07196) / [EA-TWM-READ-0013](evidence-appendix.md#ea-twm-read-0013))

### EA-MODEL (2 events)
- [`support`] Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to 0.85. ([2604.27224](https://arxiv.org/abs/2604.27224) / [EA-LOCOMANIP-2026-0012](evidence-appendix.md#ea-locomanip-2026-0012))
- [`support`] In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. ([2607.10132](https://arxiv.org/abs/2607.10132) / [EA-LOCOMANIP-2026-0021](evidence-appendix.md#ea-locomanip-2026-0021))

### EA-SENSOR (5 events)
- [`support`] 近一年触觉表征研究开始从小规模单任务管线走向大规模全手触觉—第一视角配对数据和多任务、任务级 OOD 基准；HT-Bench 以约 1000 万 RGB 帧、780 万触觉帧和 226 项任务测量接触结构、跨模态对齐与时间动态。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0001](evidence-appendix.md#ea-tactile-2026-0001))
- [`support`] 物体 6-DoF 位姿误差在遮挡、弱光、反光/透明表面下会让视觉方法失效；单次双触点触觉可作为视觉不可靠时的位姿观测补充。 ([2606.28899](https://arxiv.org/abs/2606.28899) / [EA-SENSORERR-READ-0010](evidence-appendix.md#ea-sensorerr-read-0010))
- [`support`] 触觉在灵巧操作中补足视觉/语言无法稳定观测的接触隐变量；滑移、力不匹配、接触稳定性等局部误差需要比语义规划更快的反馈通道。 ([2607.07287](https://arxiv.org/abs/2607.07287) / [EA-SENSORERR-READ-0012](evidence-appendix.md#ea-sensorerr-read-0012))
- [`limit`] HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0002](evidence-appendix.md#ea-tactile-2026-0002))
- [`limit`] TACO 用触觉感知世界模型联合预测未来视频和力序列，再将真实失败附近状态转成带纠正动作的想象片段，用于接触丰富任务的 VLA 后训练。 ([2607.02840](https://arxiv.org/abs/2607.02840) / [EA-SENSORERR-READ-0001](evidence-appendix.md#ea-sensorerr-read-0001))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only dat... ([2601.09988](https://arxiv.org/abs/2601.09988) / [EA-UMI-READ-0002](evidence-appendix.md#ea-umi-read-0002))
- `conditional` VT-WM 的训练序列同步记录腕部位姿、关节位置、外部视觉和两个指尖触觉视频，并使用时间戳对齐后降采样训练。 ([2602.06001](https://arxiv.org/abs/2602.06001) / [EA-TWM-READ-0001](evidence-appendix.md#ea-twm-read-0001))
- `conditional` 触觉信息用于 VLA 或世界模型时，低频视觉语言理解和高频触觉反馈应在架构上分离。 ([2605.07308](https://arxiv.org/abs/2605.07308) / [EA-TWM-READ-0007](evidence-appendix.md#ea-twm-read-0007))
- `conditional` 在视觉遮挡或视觉退化下，显式把触觉接触投影到图像域可以改善空间对齐；但这种收益依赖对运动学和标定误差导致的空间不确定性建模。 ([2606.08765](https://arxiv.org/abs/2606.08765) / [EA-TWM-READ-0014](evidence-appendix.md#ea-twm-read-0014))
- `conditional` 触觉不是简单加 token 就能提升；接触任务中的 RGB 未来可能视觉上合理但物理上不完整，而无约束触觉注入还可能污染视频和动作预测。 ([2606.26663](https://arxiv.org/abs/2606.26663) / [EA-TWM-READ-0010](evidence-appendix.md#ea-twm-read-0010))
- `conditional` 力觉/触觉/音频能揭示图像不可直接观测的交互状态；但这些模态硬件和任务依赖强，所以需要在少量多传感数据上适配既有视觉策略，而不是预训练时穷尽所有传感器。 ([2606.30988](https://arxiv.org/abs/2606.30988) / [EA-TWM-READ-0011](evidence-appendix.md#ea-twm-read-0011))
- `limit` 全局视觉异常、帧级变化或策略不确定性不足以判断感知误差是否会影响当前动作；部署监控需要把异常限定到 action chunk 将要使用的执行走廊。 ([2606.16690](https://arxiv.org/abs/2606.16690) / [EA-TWM-READ-0009](evidence-appendix.md#ea-twm-read-0009))
- `limit` 只看任务完成会低估传感器感知误差的真实风险；柔性物操作需要把安全交互、滑移/掉落和过度形变作为独立评测目标。 ([2607.04234](https://arxiv.org/abs/2607.04234) / [EA-TWM-READ-0012](evidence-appendix.md#ea-twm-read-0012))
- `gap` 世界模型/生成式仿真器不能仅凭视觉逼真度作为具身策略评测裁判；必须验证其是否按动作正确响应，并建立 admissibility/validation 梯度后才能把闭环判决当证据。 ([2607.07196](https://arxiv.org/abs/2607.07196) / [EA-TWM-READ-0013](evidence-appendix.md#ea-twm-read-0013))
- `limit` HT-Bench 的进步仍停留在表征层：当前四项任务没有直接测量真实机器人闭环操作，因此不能据此宣称策略或部署收益。 ([2606.19161](https://arxiv.org/abs/2606.19161) / [EA-TACTILE-2026-0002](evidence-appendix.md#ea-tactile-2026-0002))
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
