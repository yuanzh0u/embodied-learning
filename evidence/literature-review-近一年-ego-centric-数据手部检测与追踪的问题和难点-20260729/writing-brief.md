# Writing Brief: 近一年 ego-centric 数据中手部检测与追踪的问题和难点

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年 ego-centric 数据中手部检测与追踪的问题和难点
- Time range: 2025-07-29 至 2026-07-29
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-4D`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 29

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 第一视角的相机坐标会把头部抖动与物体运动混合，稳定 HOI 追踪需要世界坐标锚定。 ([2601.01050](https://arxiv.org/abs/2601.01050) / [EA-EGOHAND-2026-0007](evidence-appendix.md#ea-egohand-2026-0007)) ⟷ 事件手追踪存在显著视角域差：第三视角模型直接用于第一视角时性能会严重下降。 ([2509.13883](https://arxiv.org/abs/2509.13883) / [EA-EGOHAND-2026-0001](evidence-appendix.md#ea-egohand-2026-0001))
- `EA-DATA`: Egocentric 手指自遮挡是高频现象：跨四个数据集，超过 20% 帧至少有一根手指高度遮挡。 ([2601.15516](https://arxiv.org/abs/2601.15516) / [EA-EGOHAND-2026-0009](evidence-appendix.md#ea-egohand-2026-0009)) ⟷ 受控数据上训练的 3D 手追踪器不能保证野外泛化；在 EgoExo-Hands 上的 MKPE 从域内约 9–11 mm 上升到 16.28 mm。 ([2510.02601](https://arxiv.org/abs/2510.02601) / [EA-EGOHAND-2026-0003](evidence-appendix.md#ea-egohand-2026-0003))
- `EA-DATA`: 单目头戴相机中，绝对 3D 手追踪同时受深度–尺度歧义、自遮挡与宽 FOV/鱼眼变形限制。 ([2605.12498](https://arxiv.org/abs/2605.12498) / [EA-EGOHAND-2026-0018](evidence-appendix.md#ea-egohand-2026-0018)) ⟷ 流式手追踪/预测中，素朴时序记忆可能比无记忆更差，因为背景 token 会检索并放大历史队列中的自回归误差。 ([2511.18127](https://arxiv.org/abs/2511.18127) / [EA-EGOHAND-2026-0005](evidence-appendix.md#ea-egohand-2026-0005))
- `EA-DATA`: Ego 双手追踪的观测质量具有左/右手与腕部/手指两个轴的异质性，不能用单一置信度概括。 ([2605.18553](https://arxiv.org/abs/2605.18553) / [EA-EGOHAND-2026-0020](evidence-appendix.md#ea-egohand-2026-0020)) ⟷ 自回归追踪/预测必须显式管理自身误差累积；被存入的错误可以被后续时刻再次检索并放大。 ([2511.18127](https://arxiv.org/abs/2511.18127) / [EA-EGOHAND-2026-0006](evidence-appendix.md#ea-egohand-2026-0006))
- `EA-DATA`: Egocentric 4D 手重建同时受移动相机、严重自遮挡、有限视角、快速手动与双手交互影响。 ([2606.19156](https://arxiv.org/abs/2606.19156) / [EA-EGOHAND-2026-0026](evidence-appendix.md#ea-egohand-2026-0026)) ⟷ 裸手预训练的视觉手追踪器在传感手套上存在大幅外观域差，每种新手套都可能需要新的适配数据。 ([2602.05159](https://arxiv.org/abs/2602.05159) / [EA-EGOHAND-2026-0011](evidence-appendix.md#ea-egohand-2026-0011))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (29 events)
- [`support`] 第一视角的相机坐标会把头部抖动与物体运动混合，稳定 HOI 追踪需要世界坐标锚定。 ([2601.01050](https://arxiv.org/abs/2601.01050) / [EA-EGOHAND-2026-0007](evidence-appendix.md#ea-egohand-2026-0007))
- [`support`] Egocentric 手指自遮挡是高频现象：跨四个数据集，超过 20% 帧至少有一根手指高度遮挡。 ([2601.15516](https://arxiv.org/abs/2601.15516) / [EA-EGOHAND-2026-0009](evidence-appendix.md#ea-egohand-2026-0009))
- [`support`] 单目头戴相机中，绝对 3D 手追踪同时受深度–尺度歧义、自遮挡与宽 FOV/鱼眼变形限制。 ([2605.12498](https://arxiv.org/abs/2605.12498) / [EA-EGOHAND-2026-0018](evidence-appendix.md#ea-egohand-2026-0018))
- [`support`] Ego 双手追踪的观测质量具有左/右手与腕部/手指两个轴的异质性，不能用单一置信度概括。 ([2605.18553](https://arxiv.org/abs/2605.18553) / [EA-EGOHAND-2026-0020](evidence-appendix.md#ea-egohand-2026-0020))
- [`support`] Egocentric 4D 手重建同时受移动相机、严重自遮挡、有限视角、快速手动与双手交互影响。 ([2606.19156](https://arxiv.org/abs/2606.19156) / [EA-EGOHAND-2026-0026](evidence-appendix.md#ea-egohand-2026-0026))
- [`conditional`] 在真实环境中获得精确 3D 手真值仍依赖多相机、同步、标定和重型移动采集硬件。 ([2510.02601](https://arxiv.org/abs/2510.02601) / [EA-EGOHAND-2026-0004](evidence-appendix.md#ea-egohand-2026-0004))
- [`conditional`] 开放词表世界坐标 HOI 恢复的精度目前以重型离线管线为代价，不等于可实时部署。 ([2601.01050](https://arxiv.org/abs/2601.01050) / [EA-EGOHAND-2026-0008](evidence-appendix.md#ea-egohand-2026-0008))
- [`conditional`] 手背皮肤形变只是条件性遮挡补充信号；手背不可见、低分辨率或快速运动会削弱其价值。 ([2601.15516](https://arxiv.org/abs/2601.15516) / [EA-EGOHAND-2026-0010](evidence-appendix.md#ea-egohand-2026-0010))
- [`conditional`] 当前纯合成数据不能替代真实 egocentric HOI 数据；它主要是少标签和域适应下的补充资源。 ([2603.29733](https://arxiv.org/abs/2603.29733) / [EA-EGOHAND-2026-0012](evidence-appendix.md#ea-egohand-2026-0012))
- [`conditional`] TouchMoment 的自动训练标注与手工标签平均相差 1.94 帧，这与严格评测容差处于同一量级。 ([2604.12343](https://arxiv.org/abs/2604.12343) / [EA-EGOHAND-2026-0015](evidence-appendix.md#ea-egohand-2026-0015))
- [`conditional`] 双目事件的几何增益以更高硬件、标定和算力成本为代价，超低功耗部署仍需压缩。 ([2605.12297](https://arxiv.org/abs/2605.12297) / [EA-EGOHAND-2026-0017](evidence-appendix.md#ea-egohand-2026-0017))
- [`conditional`] 视觉与 6-DoF IMU 的互补只有在准确同步下成立：视觉锚定全局位置，IMU 补足遮挡下的高频指部运动。 ([2605.21714](https://arxiv.org/abs/2605.21714) / [EA-EGOHAND-2026-0022](evidence-appendix.md#ea-egohand-2026-0022))
- [`limit`] 事件手追踪存在显著视角域差：第三视角模型直接用于第一视角时性能会严重下降。 ([2509.13883](https://arxiv.org/abs/2509.13883) / [EA-EGOHAND-2026-0001](evidence-appendix.md#ea-egohand-2026-0001))
- [`limit`] 受控数据上训练的 3D 手追踪器不能保证野外泛化；在 EgoExo-Hands 上的 MKPE 从域内约 9–11 mm 上升到 16.28 mm。 ([2510.02601](https://arxiv.org/abs/2510.02601) / [EA-EGOHAND-2026-0003](evidence-appendix.md#ea-egohand-2026-0003))
- [`limit`] 流式手追踪/预测中，素朴时序记忆可能比无记忆更差，因为背景 token 会检索并放大历史队列中的自回归误差。 ([2511.18127](https://arxiv.org/abs/2511.18127) / [EA-EGOHAND-2026-0005](evidence-appendix.md#ea-egohand-2026-0005))
- [`limit`] 自回归追踪/预测必须显式管理自身误差累积；被存入的错误可以被后续时刻再次检索并放大。 ([2511.18127](https://arxiv.org/abs/2511.18127) / [EA-EGOHAND-2026-0006](evidence-appendix.md#ea-egohand-2026-0006))
- [`limit`] 裸手预训练的视觉手追踪器在传感手套上存在大幅外观域差，每种新手套都可能需要新的适配数据。 ([2602.05159](https://arxiv.org/abs/2602.05159) / [EA-EGOHAND-2026-0011](evidence-appendix.md#ea-egohand-2026-0011))
- [`limit`] HOI-Synth 的证据是单帧检测证据，不包含轨迹连续性或时序追踪能力。 ([2603.29733](https://arxiv.org/abs/2603.29733) / [EA-EGOHAND-2026-0013](evidence-appendix.md#ea-egohand-2026-0013))
- [`limit`] 精确触碰时刻检测不是普通手检测；它还需区分强自运动、近距遮挡和视觉上几乎相同的近接触帧。 ([2604.12343](https://arxiv.org/abs/2604.12343) / [EA-EGOHAND-2026-0014](evidence-appendix.md#ea-egohand-2026-0014))
- [`limit`] 事件相机不会自动消除 egocentric 干扰：头部运动生成的背景事件会与手运动信号耦合。 ([2605.12297](https://arxiv.org/abs/2605.12297) / [EA-EGOHAND-2026-0016](evidence-appendix.md#ea-egohand-2026-0016))
- [`limit`] 跨镜头单网络仍依赖已标定 3D 训练数据和相机内参，不等于无标定野外泛化。 ([2605.12498](https://arxiv.org/abs/2605.12498) / [EA-EGOHAND-2026-0019](evidence-appendix.md#ea-egohand-2026-0019))
- [`limit`] 当上游视觉完全没有可靠观测锚点时，生成恢复只能产生合理先验，可能形成错误轨迹。 ([2605.18553](https://arxiv.org/abs/2605.18553) / [EA-EGOHAND-2026-0021](evidence-appendix.md#ea-egohand-2026-0021))
- [`limit`] 手套型多模态追踪会引入新的外观域差，且对不同手套布局和 IMU 规格的泛化尚未验证。 ([2605.21714](https://arxiv.org/abs/2605.21714) / [EA-EGOHAND-2026-0023](evidence-appendix.md#ea-egohand-2026-0023))
- [`limit`] 事件手检测的精度仍受慢变信号不可见与将事件流重新帧化的处理低效限制。 ([2606.10790](https://arxiv.org/abs/2606.10790) / [EA-EGOHAND-2026-0024](evidence-appendix.md#ea-egohand-2026-0024))
- [`limit`] Hand-4DGS 的定量结果排除了手大部分出框或上游无法正确检测双手的帧，因而不能外推到最难丢检场景。 ([2606.19156](https://arxiv.org/abs/2606.19156) / [EA-EGOHAND-2026-0027](evidence-appendix.md#ea-egohand-2026-0027))
- [`limit`] 将中心帧的接触标注传播到整个 clip 会受手边别错误和相机跳变污染，需保留每帧置信度。 ([2606.30598](https://arxiv.org/abs/2606.30598) / [EA-EGOHAND-2026-0029](evidence-appendix.md#ea-egohand-2026-0029))
- [`gap`] 真实事件数据缺少 3D 真值，导致该方法的真实 3D 指标无法被直接验证。 ([2509.13883](https://arxiv.org/abs/2509.13883) / [EA-EGOHAND-2026-0002](evidence-appendix.md#ea-egohand-2026-0002))
- [`gap`] 现有 EventEgoHands 仍缺少光照、肤色和活动多样性，真实数据覆盖是未解问题。 ([2606.10790](https://arxiv.org/abs/2606.10790) / [EA-EGOHAND-2026-0025](evidence-appendix.md#ea-egohand-2026-0025))
- [`gap`] 野外 egocentric 手物 3D 估计的主要数据瓶颈是重遮挡与接触歧义下缺少便宜、可扩展的 3D 监督。 ([2606.30598](https://arxiv.org/abs/2606.30598) / [EA-EGOHAND-2026-0028](evidence-appendix.md#ea-egohand-2026-0028))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 在真实环境中获得精确 3D 手真值仍依赖多相机、同步、标定和重型移动采集硬件。 ([2510.02601](https://arxiv.org/abs/2510.02601) / [EA-EGOHAND-2026-0004](evidence-appendix.md#ea-egohand-2026-0004))
- `conditional` 开放词表世界坐标 HOI 恢复的精度目前以重型离线管线为代价，不等于可实时部署。 ([2601.01050](https://arxiv.org/abs/2601.01050) / [EA-EGOHAND-2026-0008](evidence-appendix.md#ea-egohand-2026-0008))
- `conditional` 手背皮肤形变只是条件性遮挡补充信号；手背不可见、低分辨率或快速运动会削弱其价值。 ([2601.15516](https://arxiv.org/abs/2601.15516) / [EA-EGOHAND-2026-0010](evidence-appendix.md#ea-egohand-2026-0010))
- `conditional` 当前纯合成数据不能替代真实 egocentric HOI 数据；它主要是少标签和域适应下的补充资源。 ([2603.29733](https://arxiv.org/abs/2603.29733) / [EA-EGOHAND-2026-0012](evidence-appendix.md#ea-egohand-2026-0012))
- `conditional` TouchMoment 的自动训练标注与手工标签平均相差 1.94 帧，这与严格评测容差处于同一量级。 ([2604.12343](https://arxiv.org/abs/2604.12343) / [EA-EGOHAND-2026-0015](evidence-appendix.md#ea-egohand-2026-0015))
- `conditional` 双目事件的几何增益以更高硬件、标定和算力成本为代价，超低功耗部署仍需压缩。 ([2605.12297](https://arxiv.org/abs/2605.12297) / [EA-EGOHAND-2026-0017](evidence-appendix.md#ea-egohand-2026-0017))
- `conditional` 视觉与 6-DoF IMU 的互补只有在准确同步下成立：视觉锚定全局位置，IMU 补足遮挡下的高频指部运动。 ([2605.21714](https://arxiv.org/abs/2605.21714) / [EA-EGOHAND-2026-0022](evidence-appendix.md#ea-egohand-2026-0022))
- `limit` 事件手追踪存在显著视角域差：第三视角模型直接用于第一视角时性能会严重下降。 ([2509.13883](https://arxiv.org/abs/2509.13883) / [EA-EGOHAND-2026-0001](evidence-appendix.md#ea-egohand-2026-0001))
- `limit` 受控数据上训练的 3D 手追踪器不能保证野外泛化；在 EgoExo-Hands 上的 MKPE 从域内约 9–11 mm 上升到 16.28 mm。 ([2510.02601](https://arxiv.org/abs/2510.02601) / [EA-EGOHAND-2026-0003](evidence-appendix.md#ea-egohand-2026-0003))
- `limit` 流式手追踪/预测中，素朴时序记忆可能比无记忆更差，因为背景 token 会检索并放大历史队列中的自回归误差。 ([2511.18127](https://arxiv.org/abs/2511.18127) / [EA-EGOHAND-2026-0005](evidence-appendix.md#ea-egohand-2026-0005))
- `limit` 自回归追踪/预测必须显式管理自身误差累积；被存入的错误可以被后续时刻再次检索并放大。 ([2511.18127](https://arxiv.org/abs/2511.18127) / [EA-EGOHAND-2026-0006](evidence-appendix.md#ea-egohand-2026-0006))
- `limit` 裸手预训练的视觉手追踪器在传感手套上存在大幅外观域差，每种新手套都可能需要新的适配数据。 ([2602.05159](https://arxiv.org/abs/2602.05159) / [EA-EGOHAND-2026-0011](evidence-appendix.md#ea-egohand-2026-0011))
- `limit` HOI-Synth 的证据是单帧检测证据，不包含轨迹连续性或时序追踪能力。 ([2603.29733](https://arxiv.org/abs/2603.29733) / [EA-EGOHAND-2026-0013](evidence-appendix.md#ea-egohand-2026-0013))
- `limit` 精确触碰时刻检测不是普通手检测；它还需区分强自运动、近距遮挡和视觉上几乎相同的近接触帧。 ([2604.12343](https://arxiv.org/abs/2604.12343) / [EA-EGOHAND-2026-0014](evidence-appendix.md#ea-egohand-2026-0014))
- `limit` 事件相机不会自动消除 egocentric 干扰：头部运动生成的背景事件会与手运动信号耦合。 ([2605.12297](https://arxiv.org/abs/2605.12297) / [EA-EGOHAND-2026-0016](evidence-appendix.md#ea-egohand-2026-0016))
- `limit` 跨镜头单网络仍依赖已标定 3D 训练数据和相机内参，不等于无标定野外泛化。 ([2605.12498](https://arxiv.org/abs/2605.12498) / [EA-EGOHAND-2026-0019](evidence-appendix.md#ea-egohand-2026-0019))
- `limit` 当上游视觉完全没有可靠观测锚点时，生成恢复只能产生合理先验，可能形成错误轨迹。 ([2605.18553](https://arxiv.org/abs/2605.18553) / [EA-EGOHAND-2026-0021](evidence-appendix.md#ea-egohand-2026-0021))
- `limit` 手套型多模态追踪会引入新的外观域差，且对不同手套布局和 IMU 规格的泛化尚未验证。 ([2605.21714](https://arxiv.org/abs/2605.21714) / [EA-EGOHAND-2026-0023](evidence-appendix.md#ea-egohand-2026-0023))
- `limit` 事件手检测的精度仍受慢变信号不可见与将事件流重新帧化的处理低效限制。 ([2606.10790](https://arxiv.org/abs/2606.10790) / [EA-EGOHAND-2026-0024](evidence-appendix.md#ea-egohand-2026-0024))
- `limit` Hand-4DGS 的定量结果排除了手大部分出框或上游无法正确检测双手的帧，因而不能外推到最难丢检场景。 ([2606.19156](https://arxiv.org/abs/2606.19156) / [EA-EGOHAND-2026-0027](evidence-appendix.md#ea-egohand-2026-0027))
- `limit` 将中心帧的接触标注传播到整个 clip 会受手边别错误和相机跳变污染，需保留每帧置信度。 ([2606.30598](https://arxiv.org/abs/2606.30598) / [EA-EGOHAND-2026-0029](evidence-appendix.md#ea-egohand-2026-0029))
- `gap` 真实事件数据缺少 3D 真值，导致该方法的真实 3D 指标无法被直接验证。 ([2509.13883](https://arxiv.org/abs/2509.13883) / [EA-EGOHAND-2026-0002](evidence-appendix.md#ea-egohand-2026-0002))
- `gap` 现有 EventEgoHands 仍缺少光照、肤色和活动多样性，真实数据覆盖是未解问题。 ([2606.10790](https://arxiv.org/abs/2606.10790) / [EA-EGOHAND-2026-0025](evidence-appendix.md#ea-egohand-2026-0025))
- `gap` 野外 egocentric 手物 3D 估计的主要数据瓶颈是重遮挡与接触歧义下缺少便宜、可扩展的 3D 监督。 ([2606.30598](https://arxiv.org/abs/2606.30598) / [EA-EGOHAND-2026-0028](evidence-appendix.md#ea-egohand-2026-0028))

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
