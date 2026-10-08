# Writing Brief: 智驾模型与关键团队：VLA、驾驶基础模型及理想系列论文

> 本文件是写作输入,不是交付物。用户明确单科研文体，主文及理想专章交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;仅写科研备忘录，三张表及理想专章为同文体补充。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 智驾模型与关键团队：VLA、驾驶基础模型及理想系列论文
- Time range: 2024-09-27..2026-09-27; classic antecedents allowed
- Knowledge IDs: `EA-MODEL`, `EA-ALIGN`, `EA-EVAL`
- Review mode: scoping
- Paper-level sources: 30 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 66

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-MODEL`: UniAD 以任务 query 作为感知、预测和规划之间的可学习接口，并保留显式中间监督。 ([2212.10156](https://arxiv.org/abs/2212.10156) / [EA-AVMODEL-2026-0001](evidence-appendix.md#ea-avmodel-2026-0001)) ⟷ 无视觉 AD-MLP 在 nuScenes 开放环能取得有竞争力的轨迹结果，暴露指标与真实驾驶能力的落差。 ([2305.10430](https://arxiv.org/abs/2305.10430) / [EA-AVMODEL-2026-0003](evidence-appendix.md#ea-avmodel-2026-0003))
- `EA-MODEL`: LMDrive 将语言指令、相机和 LiDAR 特征映射为路点及指令完成标志，再由 PID 执行。 ([2312.07488](https://arxiv.org/abs/2312.07488) / [EA-AVMODEL-2026-0005](evidence-appendix.md#ea-avmodel-2026-0005)) ⟷ 占据栅格离散化会使真实记录轨迹被误判碰撞，栅格尺寸影响结果。 ([2305.10430](https://arxiv.org/abs/2305.10430) / [EA-AVMODEL-2026-0004](evidence-appendix.md#ea-avmodel-2026-0004))
- `EA-MODEL`: LingoQA 的对象是驾驶视频问答，配套学习式 Lingo-Judge，而非执行驾驶动作。 ([2312.14115](https://arxiv.org/abs/2312.14115) / [EA-AVMODEL-2026-0007](evidence-appendix.md#ea-avmodel-2026-0007)) ⟷ DriveLM-Agent 的论文规划验证仍为开放环；作者将闭环列为后续方向。 ([2312.14150](https://arxiv.org/abs/2312.14150) / [EA-AVMODEL-2026-0010](evidence-appendix.md#ea-avmodel-2026-0010))
- `EA-MODEL`: DriveLM 以有向 QA 图传递上下文，再将行为说明映射为离散轨迹 token。 ([2312.14150](https://arxiv.org/abs/2312.14150) / [EA-AVMODEL-2026-0009](evidence-appendix.md#ea-avmodel-2026-0009)) ⟷ NAVSIM 作者指出，高 PDMS 并不总对应高闭环分数，建议配合 CARLA 等闭环评测。 ([2406.15349](https://arxiv.org/abs/2406.15349) / [EA-AVMODEL-2026-0014](evidence-appendix.md#ea-avmodel-2026-0014))
- `EA-MODEL`: DriveVLM-Dual 将低频 VLM 轨迹交给传统规划器进行高频细化，两支异步协作。 ([2402.12289](https://arxiv.org/abs/2402.12289) / [EA-AVMODEL-2026-0011](evidence-appendix.md#ea-avmodel-2026-0011)) ⟷ 作者明确指出，人可读的辅助输出和驾驶动作并不保证始终一致。 ([2410.23262](https://arxiv.org/abs/2410.23262) / [EA-AVMODEL-2026-0017](evidence-appendix.md#ea-avmodel-2026-0017))
- `EA-MODEL`: NAVSIM 仅在初始帧调用规划策略，随后固定计划进行非反应式模拟，没有环境反馈给策略。 ([2406.15349](https://arxiv.org/abs/2406.15349) / [EA-AVMODEL-2026-0013](evidence-appendix.md#ea-avmodel-2026-0013)) ⟷ SimLingo 的消融未观察到未对齐语言任务对驾驶的明确正负影响；CoT 的驾驶收益也未达统计显著。 ([2503.09594](https://arxiv.org/abs/2503.09594) / [EA-AVMODEL-2026-0023](evidence-appendix.md#ea-avmodel-2026-0023))
- `EA-MODEL`: EMMA 将驾驶任务的非传感器输入和输出统一为文本，允许规划、检测和路网任务联合训练。 ([2410.23262](https://arxiv.org/abs/2410.23262) / [EA-AVMODEL-2026-0015](evidence-appendix.md#ea-avmodel-2026-0015)) ⟷ ORION 作者将大 VLM 的计算复杂度列为实时驾驶部署限制。 ([2503.19755](https://arxiv.org/abs/2503.19755) / [EA-AVMODEL-2026-0027](evidence-appendix.md#ea-avmodel-2026-0027))
- `EA-MODEL`: DiffusionDrive 从带噪轨迹锚点出发进行截断去噪，并以学习置信度选择最终轨迹。 ([2411.15139](https://arxiv.org/abs/2411.15139) / [EA-AVMODEL-2026-0018](evidence-appendix.md#ea-avmodel-2026-0018)) ⟷ OpenDriveVLA 当前规划评测仅为开放环，作者警告这可能高估鲁棒性。 ([2503.23463](https://arxiv.org/abs/2503.23463) / [EA-AVMODEL-2026-0029](evidence-appendix.md#ea-avmodel-2026-0029))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-MODEL (66 events)
- [`support`] UniAD 以任务 query 作为感知、预测和规划之间的可学习接口，并保留显式中间监督。 ([2212.10156](https://arxiv.org/abs/2212.10156) / [EA-AVMODEL-2026-0001](evidence-appendix.md#ea-avmodel-2026-0001))
- [`support`] LMDrive 将语言指令、相机和 LiDAR 特征映射为路点及指令完成标志，再由 PID 执行。 ([2312.07488](https://arxiv.org/abs/2312.07488) / [EA-AVMODEL-2026-0005](evidence-appendix.md#ea-avmodel-2026-0005))
- [`support`] LingoQA 的对象是驾驶视频问答，配套学习式 Lingo-Judge，而非执行驾驶动作。 ([2312.14115](https://arxiv.org/abs/2312.14115) / [EA-AVMODEL-2026-0007](evidence-appendix.md#ea-avmodel-2026-0007))
- [`support`] DriveLM 以有向 QA 图传递上下文，再将行为说明映射为离散轨迹 token。 ([2312.14150](https://arxiv.org/abs/2312.14150) / [EA-AVMODEL-2026-0009](evidence-appendix.md#ea-avmodel-2026-0009))
- [`support`] DriveVLM-Dual 将低频 VLM 轨迹交给传统规划器进行高频细化，两支异步协作。 ([2402.12289](https://arxiv.org/abs/2402.12289) / [EA-AVMODEL-2026-0011](evidence-appendix.md#ea-avmodel-2026-0011))
- [`support`] NAVSIM 仅在初始帧调用规划策略，随后固定计划进行非反应式模拟，没有环境反馈给策略。 ([2406.15349](https://arxiv.org/abs/2406.15349) / [EA-AVMODEL-2026-0013](evidence-appendix.md#ea-avmodel-2026-0013))
- [`support`] EMMA 将驾驶任务的非传感器输入和输出统一为文本，允许规划、检测和路网任务联合训练。 ([2410.23262](https://arxiv.org/abs/2410.23262) / [EA-AVMODEL-2026-0015](evidence-appendix.md#ea-avmodel-2026-0015))
- [`support`] DrivingSphere 把可控占据、视觉渲染与交通主体状态更新接成仿真闭环，区别于只生成固定视频。 ([2411.11252](https://arxiv.org/abs/2411.11252) / [EA-LIAUTO-2026-0001](evidence-appendix.md#ea-liauto-2026-0001))
- [`support`] DiffusionDrive 从带噪轨迹锚点出发进行截断去噪，并以学习置信度选择最终轨迹。 ([2411.15139](https://arxiv.org/abs/2411.15139) / [EA-AVMODEL-2026-0018](evidence-appendix.md#ea-avmodel-2026-0018))
- [`support`] DiMA 通过共享场景编码器、辅助任务和特征蒸馏训练视觉规划器，默认推理无需 LLM。 ([2501.09757](https://arxiv.org/abs/2501.09757) / [EA-AVMODEL-2026-0020](evidence-appendix.md#ea-avmodel-2026-0020))
- [`support`] SimLingo 用同一视觉场景的多种指令—轨迹配对，迫使模型学习语言对动作的影响。 ([2503.09594](https://arxiv.org/abs/2503.09594) / [EA-AVMODEL-2026-0022](evidence-appendix.md#ea-avmodel-2026-0022))
- [`support`] ORION 用 LLM 的 planning token 条件化 VAE 轨迹分布，并以 GRU 解码轨迹。 ([2503.19755](https://arxiv.org/abs/2503.19755) / [EA-AVMODEL-2026-0025](evidence-appendix.md#ea-avmodel-2026-0025))
- [`support`] OpenDriveVLA 将 scene、agent、map 三类结构化视觉 token 对齐到语言空间，并联合优化轨迹生成。 ([2503.23463](https://arxiv.org/abs/2503.23463) / [EA-AVMODEL-2026-0028](evidence-appendix.md#ea-avmodel-2026-0028))
- [`support`] AutoVLA 将驾驶运动码本扩展进 VLM 词表，以统一自回归过程生成推理和动作。 ([2506.13757](https://arxiv.org/abs/2506.13757) / [EA-AVMODEL-2026-0030](evidence-appendix.md#ea-avmodel-2026-0030))
- [`support`] World4Drive 用动作条件未来潜变量及学习式选择器评价多模式轨迹；测试期不访问真实未来 latent。 ([2507.00603](https://arxiv.org/abs/2507.00603) / [EA-LIAUTO-2026-0003](evidence-appendix.md#ea-liauto-2026-0003))
- [`support`] ReflectDrive 的反思由外部安全评分、本地搜索和离散扩散修补实现，不是自然语言反思文本。 ([2509.20109](https://arxiv.org/abs/2509.20109) / [EA-LIAUTO-2026-0005](evidence-appendix.md#ea-liauto-2026-0005))
- [`support`] Alpamayo-R1 在训练时使用离散动作 token，但推理轨迹由连续 flow-matching 动作专家解码。 ([2511.00088](https://arxiv.org/abs/2511.00088) / [EA-AVMODEL-2026-0033](evidence-appendix.md#ea-avmodel-2026-0033))
- [`support`] MindDrive 先学语言 meta-action 到轨迹的映射，再用 CARLA 交互回报及 PPO 优化决策专家。 ([2512.13636](https://arxiv.org/abs/2512.13636) / [EA-AVMODEL-2026-0036](evidence-appendix.md#ea-avmodel-2026-0036))
- [`support`] LinkVLA 增加动作到语言的理解目标，并用终点引导的粗到细动作生成连接语言与规划。 ([2603.01441](https://arxiv.org/abs/2603.01441) / [EA-LIAUTO-2026-0007](evidence-appendix.md#ea-liauto-2026-0007))
- [`support`] Orion-Lite 在推理时移除文本提示和大型 LLM，以轻量 transformer 模仿教师的 planning-token 表征。 ([2604.08266](https://arxiv.org/abs/2604.08266) / [EA-AVMODEL-2026-0038](evidence-appendix.md#ea-avmodel-2026-0038))
- [`support`] Streaming Intent 将语言推理解析为有限意图类别，再以意图条件控制连续动作生成。 ([2605.12622](https://arxiv.org/abs/2605.12622) / [EA-LIAUTO-2026-0009](evidence-appendix.md#ea-liauto-2026-0009))
- [`support`] MindVLA-U1 以共享 Transformer 和独立轻量输出头联合学习语言与连续动作，主实验的语言监督限于基础 VQA 和官方意图标签。 ([2605.12624](https://arxiv.org/abs/2605.12624) / [EA-LIAUTO-2026-0011](evidence-appendix.md#ea-liauto-2026-0011))
- [`support`] DIAL 明确继承 MindVLA-U1，先通过意图形成候选模式，再在同场景的跨意图采样组内进行强化学习。 ([2605.12625](https://arxiv.org/abs/2605.12625) / [EA-LIAUTO-2026-0013](evidence-appendix.md#ea-liauto-2026-0013))
- [`support`] AnyScene 将占据几何作为可控视频生成的中间约束，目标是扩展驾驶场景与传感器视角。 ([2605.26113](https://arxiv.org/abs/2605.26113) / [EA-LIAUTO-2026-0015](evidence-appendix.md#ea-liauto-2026-0015))
- [`support`] nuReasoning 的 nuVLA 在推理时关闭显式文字推理，训练期加入推理监督仍改善其开放环规划。 ([2605.31572](https://arxiv.org/abs/2605.31572) / [EA-AVMODEL-2026-0043](evidence-appendix.md#ea-avmodel-2026-0043))
- [`support`] VLAFlow 的语言目标主要作用于预训练，不能据此断言驾驶推理时必须生成语言。 ([2607.01586](https://arxiv.org/abs/2607.01586) / [EA-LIAUTO-2026-0018](evidence-appendix.md#ea-liauto-2026-0018))
- [`support`] FlashDrive 分别处理视觉重复编码、KV 预填充、串行推理和迭代动作解码四类延迟。 ([2608.12932](https://arxiv.org/abs/2608.12932) / [EA-AVMODEL-2026-0045](evidence-appendix.md#ea-avmodel-2026-0045))
- [`support`] ME-VLM 将具身与代理专家蒸馏到一个部署学生，推理期不是两个教师的集成。 ([2609.24526](https://arxiv.org/abs/2609.24526) / [EA-LIAUTO-2026-0019](evidence-appendix.md#ea-liauto-2026-0019))
- [`conditional`] UniAD 预测轨迹后，在推理时使用占据地图执行额外避碰优化。 ([2212.10156](https://arxiv.org/abs/2212.10156) / [EA-AVMODEL-2026-0002](evidence-appendix.md#ea-avmodel-2026-0002))
- [`conditional`] LMDrive 的连续多句指令比单句指令更困难，实验中的驾驶分数与路线完成率下降。 ([2312.07488](https://arxiv.org/abs/2312.07488) / [EA-AVMODEL-2026-0006](evidence-appendix.md#ea-avmodel-2026-0006))
- [`conditional`] LingoQA 研究发现多帧上下文有助区分动态交通、信号灯变化等单帧易错情形。 ([2312.14115](https://arxiv.org/abs/2312.14115) / [EA-AVMODEL-2026-0008](evidence-appendix.md#ea-avmodel-2026-0008))
- [`conditional`] 论文报告双 OrinX 的车载部署；VLM 与高频驾驶系统在不同处理器运行。 ([2402.12289](https://arxiv.org/abs/2402.12289) / [EA-AVMODEL-2026-0012](evidence-appendix.md#ea-avmodel-2026-0012))
- [`conditional`] EMMA 的内部数据消融中，场景描述对规划表现影响中性，而元决策和关键物体识别带来改善。 ([2410.23262](https://arxiv.org/abs/2410.23262) / [EA-AVMODEL-2026-0016](evidence-appendix.md#ea-avmodel-2026-0016))
- [`conditional`] DiffusionDrive 的主 NAVSIM 设置采用前向相机与栅格 LiDAR；nuScenes 实验采用另一骨干配置。 ([2411.15139](https://arxiv.org/abs/2411.15139) / [EA-AVMODEL-2026-0019](evidence-appendix.md#ea-avmodel-2026-0019))
- [`conditional`] DiMA 中仅把 VQA 和规划损失加到 BEV 特征上的朴素联合训练，收益并不一致。 ([2501.09757](https://arxiv.org/abs/2501.09757) / [EA-AVMODEL-2026-0021](evidence-appendix.md#ea-avmodel-2026-0021))
- [`conditional`] 官方 CARLA Leaderboard 仅测试 SimLingo-BASE；完整 SimLingo 的闭环驾驶在本地 Bench2Drive 检验。 ([2503.09594](https://arxiv.org/abs/2503.09594) / [EA-AVMODEL-2026-0024](evidence-appendix.md#ea-avmodel-2026-0024))
- [`conditional`] 在 ORION 的受控动作输出消融中，纯文本轨迹表现最弱；生成式轨迹接口优于相同骨干的 MLP 解码。 ([2503.19755](https://arxiv.org/abs/2503.19755) / [EA-AVMODEL-2026-0026](evidence-appendix.md#ea-avmodel-2026-0026))
- [`conditional`] World4Drive 的意图不是语言推理，而是轨迹词表聚类；它仍使用专家轨迹监督。 ([2507.00603](https://arxiv.org/abs/2507.00603) / [EA-LIAUTO-2026-0004](evidence-appendix.md#ea-liauto-2026-0004))
- [`conditional`] AlpaSim 闭环中自车重新渲染并执行控制，其他交通参与者沿日志轨迹回放。 ([2511.00088](https://arxiv.org/abs/2511.00088) / [EA-AVMODEL-2026-0035](evidence-appendix.md#ea-avmodel-2026-0035))
- [`conditional`] LinkVLA 的驾驶实验含 Bench2Drive 仿真闭环；其时延报告必须区分轨迹阶段与文字推理。 ([2603.01441](https://arxiv.org/abs/2603.01441) / [EA-LIAUTO-2026-0008](evidence-appendix.md#ea-liauto-2026-0008))
- [`conditional`] 在 Bench2Drive 消融中，特征蒸馏与真值轨迹监督结合优于任一单独信号。 ([2604.08266](https://arxiv.org/abs/2604.08266) / [EA-AVMODEL-2026-0039](evidence-appendix.md#ea-avmodel-2026-0039))
- [`conditional`] 推理标注教师使用过去和未来视频；这一标签生成条件不代表推理期车辆可以访问未来。 ([2605.12622](https://arxiv.org/abs/2605.12622) / [EA-LIAUTO-2026-0010](evidence-appendix.md#ea-liauto-2026-0010))
- [`conditional`] DIAL 的强化学习比较使用小规模重新划分的 RFS 验证序列，论文报告不能当作独立实车测试。 ([2605.12625](https://arxiv.org/abs/2605.12625) / [EA-LIAUTO-2026-0014](evidence-appendix.md#ea-liauto-2026-0014))
- [`conditional`] nuReasoning 先自动产生推理标注，再经人工检查和纠错；其验证仍以开放环为限。 ([2605.31572](https://arxiv.org/abs/2605.31572) / [EA-AVMODEL-2026-0044](evidence-appendix.md#ea-avmodel-2026-0044))
- [`conditional`] VLAFlow 通过受控训练范式比较研究语言与未来表征对动作迁移的作用，正文验证对象为机器人任务。 ([2607.01586](https://arxiv.org/abs/2607.01586) / [EA-LIAUTO-2026-0017](evidence-appendix.md#ea-liauto-2026-0017))
- [`conditional`] ME-VLM 的驾驶评测针对理解与问答；部署段的 W4A8 和预填充性能不证明完整驾驶策略闭环。 ([2609.24526](https://arxiv.org/abs/2609.24526) / [EA-LIAUTO-2026-0020](evidence-appendix.md#ea-liauto-2026-0020))
- [`limit`] 无视觉 AD-MLP 在 nuScenes 开放环能取得有竞争力的轨迹结果，暴露指标与真实驾驶能力的落差。 ([2305.10430](https://arxiv.org/abs/2305.10430) / [EA-AVMODEL-2026-0003](evidence-appendix.md#ea-avmodel-2026-0003))
- [`limit`] 占据栅格离散化会使真实记录轨迹被误判碰撞，栅格尺寸影响结果。 ([2305.10430](https://arxiv.org/abs/2305.10430) / [EA-AVMODEL-2026-0004](evidence-appendix.md#ea-avmodel-2026-0004))
- [`limit`] DriveLM-Agent 的论文规划验证仍为开放环；作者将闭环列为后续方向。 ([2312.14150](https://arxiv.org/abs/2312.14150) / [EA-AVMODEL-2026-0010](evidence-appendix.md#ea-avmodel-2026-0010))
- [`limit`] NAVSIM 作者指出，高 PDMS 并不总对应高闭环分数，建议配合 CARLA 等闭环评测。 ([2406.15349](https://arxiv.org/abs/2406.15349) / [EA-AVMODEL-2026-0014](evidence-appendix.md#ea-avmodel-2026-0014))
- [`limit`] 作者明确指出，人可读的辅助输出和驾驶动作并不保证始终一致。 ([2410.23262](https://arxiv.org/abs/2410.23262) / [EA-AVMODEL-2026-0017](evidence-appendix.md#ea-avmodel-2026-0017))
- [`limit`] DrivingSphere 报告的 UniAD 交互仿真路线完成度仍低；逼真度提升不等于策略可靠或已完成实车迁移。 ([2411.11252](https://arxiv.org/abs/2411.11252) / [EA-LIAUTO-2026-0002](evidence-appendix.md#ea-liauto-2026-0002))
- [`limit`] SimLingo 的消融未观察到未对齐语言任务对驾驶的明确正负影响；CoT 的驾驶收益也未达统计显著。 ([2503.09594](https://arxiv.org/abs/2503.09594) / [EA-AVMODEL-2026-0023](evidence-appendix.md#ea-avmodel-2026-0023))
- [`limit`] ORION 作者将大 VLM 的计算复杂度列为实时驾驶部署限制。 ([2503.19755](https://arxiv.org/abs/2503.19755) / [EA-AVMODEL-2026-0027](evidence-appendix.md#ea-avmodel-2026-0027))
- [`limit`] OpenDriveVLA 当前规划评测仅为开放环，作者警告这可能高估鲁棒性。 ([2503.23463](https://arxiv.org/abs/2503.23463) / [EA-AVMODEL-2026-0029](evidence-appendix.md#ea-avmodel-2026-0029))
- [`limit`] AutoVLA 的 NAVSIM best-of-N 结果依赖 oracle 选择，必须与可直接部署的单次预测分开。 ([2506.13757](https://arxiv.org/abs/2506.13757) / [EA-AVMODEL-2026-0031](evidence-appendix.md#ea-avmodel-2026-0031))
- [`limit`] AutoVLA 作者仍将 GPU 依赖、显存和计算成本列为实时应用限制。 ([2506.13757](https://arxiv.org/abs/2506.13757) / [EA-AVMODEL-2026-0032](evidence-appendix.md#ea-avmodel-2026-0032))
- [`limit`] ReflectDrive 单列使用真实未来主体轨迹评分的版本；其结果必须与恒速近似版本区分。 ([2509.20109](https://arxiv.org/abs/2509.20109) / [EA-LIAUTO-2026-0006](evidence-appendix.md#ea-liauto-2026-0006))
- [`limit`] 仅优化推理评分时，Alpamayo-R1 的 ADE 和推理—动作一致性会退化；联合一致性奖励改善这种取舍。 ([2511.00088](https://arxiv.org/abs/2511.00088) / [EA-AVMODEL-2026-0034](evidence-appendix.md#ea-avmodel-2026-0034))
- [`limit`] MindDrive 在线 RL 的训练轮数与闭环性能并非单调关系，过多更新会降低表现。 ([2512.13636](https://arxiv.org/abs/2512.13636) / [EA-AVMODEL-2026-0037](evidence-appendix.md#ea-avmodel-2026-0037))
- [`limit`] 移除 LLM 后，Orion-Lite 的主要推理瓶颈转移到重型视觉编码器。 ([2604.08266](https://arxiv.org/abs/2604.08266) / [EA-AVMODEL-2026-0040](evidence-appendix.md#ea-avmodel-2026-0040))
- [`limit`] MindVLA-U1 的规划、GRPO 和人类偏好结论仅在日志开放环成立，尚不支持反应式闭环或实车安全结论。 ([2605.12624](https://arxiv.org/abs/2605.12624) / [EA-LIAUTO-2026-0012](evidence-appendix.md#ea-liauto-2026-0012))
- [`limit`] 该审计发现 Alpamayo-R1 样本中存在声明减速或停车而轨迹继续的说明—动作不一致。 ([2605.17268](https://arxiv.org/abs/2605.17268) / [EA-AVMODEL-2026-0041](evidence-appendix.md#ea-avmodel-2026-0041))
- [`limit`] 该审计使用确定性关键词抽取，作者承认它会漏掉同义表达。 ([2605.17268](https://arxiv.org/abs/2605.17268) / [EA-AVMODEL-2026-0042](evidence-appendix.md#ea-avmodel-2026-0042))
- [`limit`] AnyScene 明确不建模交通流或反应式主体，其生成代理受固定 BEV 布局控制。 ([2605.26113](https://arxiv.org/abs/2605.26113) / [EA-LIAUTO-2026-0016](evidence-appendix.md#ea-liauto-2026-0016))
- [`limit`] FlashDrive 的 AlpaSim 评测并非所有指标均改善，其中 Wrong Lane 退化。 ([2608.12932](https://arxiv.org/abs/2608.12932) / [EA-AVMODEL-2026-0046](evidence-appendix.md#ea-avmodel-2026-0046))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` UniAD 预测轨迹后，在推理时使用占据地图执行额外避碰优化。 ([2212.10156](https://arxiv.org/abs/2212.10156) / [EA-AVMODEL-2026-0002](evidence-appendix.md#ea-avmodel-2026-0002))
- `conditional` LMDrive 的连续多句指令比单句指令更困难，实验中的驾驶分数与路线完成率下降。 ([2312.07488](https://arxiv.org/abs/2312.07488) / [EA-AVMODEL-2026-0006](evidence-appendix.md#ea-avmodel-2026-0006))
- `conditional` LingoQA 研究发现多帧上下文有助区分动态交通、信号灯变化等单帧易错情形。 ([2312.14115](https://arxiv.org/abs/2312.14115) / [EA-AVMODEL-2026-0008](evidence-appendix.md#ea-avmodel-2026-0008))
- `conditional` 论文报告双 OrinX 的车载部署；VLM 与高频驾驶系统在不同处理器运行。 ([2402.12289](https://arxiv.org/abs/2402.12289) / [EA-AVMODEL-2026-0012](evidence-appendix.md#ea-avmodel-2026-0012))
- `conditional` EMMA 的内部数据消融中，场景描述对规划表现影响中性，而元决策和关键物体识别带来改善。 ([2410.23262](https://arxiv.org/abs/2410.23262) / [EA-AVMODEL-2026-0016](evidence-appendix.md#ea-avmodel-2026-0016))
- `conditional` DiffusionDrive 的主 NAVSIM 设置采用前向相机与栅格 LiDAR；nuScenes 实验采用另一骨干配置。 ([2411.15139](https://arxiv.org/abs/2411.15139) / [EA-AVMODEL-2026-0019](evidence-appendix.md#ea-avmodel-2026-0019))
- `conditional` DiMA 中仅把 VQA 和规划损失加到 BEV 特征上的朴素联合训练，收益并不一致。 ([2501.09757](https://arxiv.org/abs/2501.09757) / [EA-AVMODEL-2026-0021](evidence-appendix.md#ea-avmodel-2026-0021))
- `conditional` 官方 CARLA Leaderboard 仅测试 SimLingo-BASE；完整 SimLingo 的闭环驾驶在本地 Bench2Drive 检验。 ([2503.09594](https://arxiv.org/abs/2503.09594) / [EA-AVMODEL-2026-0024](evidence-appendix.md#ea-avmodel-2026-0024))
- `conditional` 在 ORION 的受控动作输出消融中，纯文本轨迹表现最弱；生成式轨迹接口优于相同骨干的 MLP 解码。 ([2503.19755](https://arxiv.org/abs/2503.19755) / [EA-AVMODEL-2026-0026](evidence-appendix.md#ea-avmodel-2026-0026))
- `conditional` World4Drive 的意图不是语言推理，而是轨迹词表聚类；它仍使用专家轨迹监督。 ([2507.00603](https://arxiv.org/abs/2507.00603) / [EA-LIAUTO-2026-0004](evidence-appendix.md#ea-liauto-2026-0004))
- `conditional` AlpaSim 闭环中自车重新渲染并执行控制，其他交通参与者沿日志轨迹回放。 ([2511.00088](https://arxiv.org/abs/2511.00088) / [EA-AVMODEL-2026-0035](evidence-appendix.md#ea-avmodel-2026-0035))
- `conditional` LinkVLA 的驾驶实验含 Bench2Drive 仿真闭环；其时延报告必须区分轨迹阶段与文字推理。 ([2603.01441](https://arxiv.org/abs/2603.01441) / [EA-LIAUTO-2026-0008](evidence-appendix.md#ea-liauto-2026-0008))
- `conditional` 在 Bench2Drive 消融中，特征蒸馏与真值轨迹监督结合优于任一单独信号。 ([2604.08266](https://arxiv.org/abs/2604.08266) / [EA-AVMODEL-2026-0039](evidence-appendix.md#ea-avmodel-2026-0039))
- `conditional` 推理标注教师使用过去和未来视频；这一标签生成条件不代表推理期车辆可以访问未来。 ([2605.12622](https://arxiv.org/abs/2605.12622) / [EA-LIAUTO-2026-0010](evidence-appendix.md#ea-liauto-2026-0010))
- `conditional` DIAL 的强化学习比较使用小规模重新划分的 RFS 验证序列，论文报告不能当作独立实车测试。 ([2605.12625](https://arxiv.org/abs/2605.12625) / [EA-LIAUTO-2026-0014](evidence-appendix.md#ea-liauto-2026-0014))
- `conditional` nuReasoning 先自动产生推理标注，再经人工检查和纠错；其验证仍以开放环为限。 ([2605.31572](https://arxiv.org/abs/2605.31572) / [EA-AVMODEL-2026-0044](evidence-appendix.md#ea-avmodel-2026-0044))
- `conditional` VLAFlow 通过受控训练范式比较研究语言与未来表征对动作迁移的作用，正文验证对象为机器人任务。 ([2607.01586](https://arxiv.org/abs/2607.01586) / [EA-LIAUTO-2026-0017](evidence-appendix.md#ea-liauto-2026-0017))
- `conditional` ME-VLM 的驾驶评测针对理解与问答；部署段的 W4A8 和预填充性能不证明完整驾驶策略闭环。 ([2609.24526](https://arxiv.org/abs/2609.24526) / [EA-LIAUTO-2026-0020](evidence-appendix.md#ea-liauto-2026-0020))
- `limit` 无视觉 AD-MLP 在 nuScenes 开放环能取得有竞争力的轨迹结果，暴露指标与真实驾驶能力的落差。 ([2305.10430](https://arxiv.org/abs/2305.10430) / [EA-AVMODEL-2026-0003](evidence-appendix.md#ea-avmodel-2026-0003))
- `limit` 占据栅格离散化会使真实记录轨迹被误判碰撞，栅格尺寸影响结果。 ([2305.10430](https://arxiv.org/abs/2305.10430) / [EA-AVMODEL-2026-0004](evidence-appendix.md#ea-avmodel-2026-0004))
- `limit` DriveLM-Agent 的论文规划验证仍为开放环；作者将闭环列为后续方向。 ([2312.14150](https://arxiv.org/abs/2312.14150) / [EA-AVMODEL-2026-0010](evidence-appendix.md#ea-avmodel-2026-0010))
- `limit` NAVSIM 作者指出，高 PDMS 并不总对应高闭环分数，建议配合 CARLA 等闭环评测。 ([2406.15349](https://arxiv.org/abs/2406.15349) / [EA-AVMODEL-2026-0014](evidence-appendix.md#ea-avmodel-2026-0014))
- `limit` 作者明确指出，人可读的辅助输出和驾驶动作并不保证始终一致。 ([2410.23262](https://arxiv.org/abs/2410.23262) / [EA-AVMODEL-2026-0017](evidence-appendix.md#ea-avmodel-2026-0017))
- `limit` DrivingSphere 报告的 UniAD 交互仿真路线完成度仍低；逼真度提升不等于策略可靠或已完成实车迁移。 ([2411.11252](https://arxiv.org/abs/2411.11252) / [EA-LIAUTO-2026-0002](evidence-appendix.md#ea-liauto-2026-0002))
- `limit` SimLingo 的消融未观察到未对齐语言任务对驾驶的明确正负影响；CoT 的驾驶收益也未达统计显著。 ([2503.09594](https://arxiv.org/abs/2503.09594) / [EA-AVMODEL-2026-0023](evidence-appendix.md#ea-avmodel-2026-0023))
- `limit` ORION 作者将大 VLM 的计算复杂度列为实时驾驶部署限制。 ([2503.19755](https://arxiv.org/abs/2503.19755) / [EA-AVMODEL-2026-0027](evidence-appendix.md#ea-avmodel-2026-0027))
- `limit` OpenDriveVLA 当前规划评测仅为开放环，作者警告这可能高估鲁棒性。 ([2503.23463](https://arxiv.org/abs/2503.23463) / [EA-AVMODEL-2026-0029](evidence-appendix.md#ea-avmodel-2026-0029))
- `limit` AutoVLA 的 NAVSIM best-of-N 结果依赖 oracle 选择，必须与可直接部署的单次预测分开。 ([2506.13757](https://arxiv.org/abs/2506.13757) / [EA-AVMODEL-2026-0031](evidence-appendix.md#ea-avmodel-2026-0031))
- `limit` AutoVLA 作者仍将 GPU 依赖、显存和计算成本列为实时应用限制。 ([2506.13757](https://arxiv.org/abs/2506.13757) / [EA-AVMODEL-2026-0032](evidence-appendix.md#ea-avmodel-2026-0032))
- `limit` ReflectDrive 单列使用真实未来主体轨迹评分的版本；其结果必须与恒速近似版本区分。 ([2509.20109](https://arxiv.org/abs/2509.20109) / [EA-LIAUTO-2026-0006](evidence-appendix.md#ea-liauto-2026-0006))
- `limit` 仅优化推理评分时，Alpamayo-R1 的 ADE 和推理—动作一致性会退化；联合一致性奖励改善这种取舍。 ([2511.00088](https://arxiv.org/abs/2511.00088) / [EA-AVMODEL-2026-0034](evidence-appendix.md#ea-avmodel-2026-0034))
- `limit` MindDrive 在线 RL 的训练轮数与闭环性能并非单调关系，过多更新会降低表现。 ([2512.13636](https://arxiv.org/abs/2512.13636) / [EA-AVMODEL-2026-0037](evidence-appendix.md#ea-avmodel-2026-0037))
- `limit` 移除 LLM 后，Orion-Lite 的主要推理瓶颈转移到重型视觉编码器。 ([2604.08266](https://arxiv.org/abs/2604.08266) / [EA-AVMODEL-2026-0040](evidence-appendix.md#ea-avmodel-2026-0040))
- `limit` MindVLA-U1 的规划、GRPO 和人类偏好结论仅在日志开放环成立，尚不支持反应式闭环或实车安全结论。 ([2605.12624](https://arxiv.org/abs/2605.12624) / [EA-LIAUTO-2026-0012](evidence-appendix.md#ea-liauto-2026-0012))
- `limit` 该审计发现 Alpamayo-R1 样本中存在声明减速或停车而轨迹继续的说明—动作不一致。 ([2605.17268](https://arxiv.org/abs/2605.17268) / [EA-AVMODEL-2026-0041](evidence-appendix.md#ea-avmodel-2026-0041))
- `limit` 该审计使用确定性关键词抽取，作者承认它会漏掉同义表达。 ([2605.17268](https://arxiv.org/abs/2605.17268) / [EA-AVMODEL-2026-0042](evidence-appendix.md#ea-avmodel-2026-0042))
- `limit` AnyScene 明确不建模交通流或反应式主体，其生成代理受固定 BEV 布局控制。 ([2605.26113](https://arxiv.org/abs/2605.26113) / [EA-LIAUTO-2026-0016](evidence-appendix.md#ea-liauto-2026-0016))
- `limit` FlashDrive 的 AlpaSim 评测并非所有指标均改善，其中 Wrong Lane 退化。 ([2608.12932](https://arxiv.org/abs/2608.12932) / [EA-AVMODEL-2026-0046](evidence-appendix.md#ea-avmodel-2026-0046))

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
- Registered sources: not loaded
