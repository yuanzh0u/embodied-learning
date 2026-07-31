# 近一年 egocentric 手部检测与追踪：瓶颈已从“看见手”转向“在观测断裂中维持真实轨迹”

## 研究边界

本调研关注 2025 年 7 月 29 日至 2026 年 7 月 29 日的第一视角数据，将“手部检测与追踪”定义为一条连续链路：从 2D 手框、关键点和左右手身份，到相机/世界坐标中的 3D 姿态、长时轨迹，再到手物接触与交互时刻。检索得到 172 篇去重候选，恢复 48 篇完整非 OCR 正文，对其中 15 篇进行深读和主张级校验。这是一次 scoping review，能回答近一年方法集中暴露的问题，但不代表所有会议和非 arXiv 工作的穷尽性计量。

## 中心判断

近一年的关键变化，不是单帧手检测又多了一个更强骨干网络，而是研究对象从“当前帧里的手”转向“与相机运动解耦、在遮挡和出框期间仍可信的 4D 手轨迹”。实际瓶颈是三种结构性困难的乘积：观测性会突然归零，头部自运动会污染手的表观运动，而真实环境中精确 3D 真值又昂贵且难扩展。因此，只提高可见帧上的精度，不能自动换来更好的追踪；必须同时管理坐标系、观测质量、时序误差和真值偏差。

## 一、遮挡不是少量异常帧，而是长时追踪的常态

手在第一视角里频繁出框，手指又会被手掌、物体或另一只手遮挡。这不是“多加一点数据增强”就能消掉的尾部问题。[DeltaDorsal](https://arxiv.org/abs/2601.15516) 在 ARCTIC、H2O、EgoExo4D 和 AssemblyHands 上的统计显示，超过 20% 的帧至少有一根手指高度遮挡。手背皮肤形变可以在部分手指不可见时提供间接线索，但论文也明确限定了适用条件：手背本身要可见，并且需要足够高的分辨率。

更难的是长连续丢失。[StableHand](https://arxiv.org/abs/2605.18553) 把左/右手与腕部/手指的观测质量分开建模，说明单一“整手置信度”会掩盖局部可信、局部已失效的状态。然而，当两只手同时缺少可靠观测锚点时，生成先验只能补出“合理”动作，无法保证是真实轨迹。这条边界很重要：平滑不等于正确，时序先验不能创造已消失的观测信息。

## 二、头部自运动使“手动了多少”变成坐标系问题

在相机坐标中，头部抖动、身体行走和真实手动会叠加。[EgoGrasp](https://arxiv.org/abs/2601.01050) 因此将手物运动恢复到世界坐标，用场景几何、相机位姿和接触关系进行联合优化。这能极大改善稳定性，但其 200 步采样和测试时优化也表明，“稳定的离线恢复”还不等于可穿戴设备上的实时追踪。

换用事件相机也不会自动解决自运动。[EgoEV-HandPose](https://arxiv.org/abs/2605.12297) 明确指出，头部运动会在背景产生大量事件，与手的高频信号纠缠；单目事件流仍有深度歧义。双目几何能够改善深度，但同时引入双目标定、算力和功耗成本。即使是 RGB，[EgoForce](https://arxiv.org/abs/2605.12498) 也显示单目绝对 3D 依然受深度—尺度歧义、鱼眼/宽视场畸变和相机内参依赖影响。因而，相机模型不是可以在训练结束后再补的工程细节，而是任务定义的一部分。

## 三、时序上下文既是解药，也是误差放大器

直觉上，为追踪器增加记忆应当比逐帧预测更好。但 [SFHand](https://arxiv.org/abs/2511.18127) 给出了反例：素朴记忆会检索到背景 token，并把已写入队列的自回归误差在后续帧再次放大，表现甚至可以差于无记忆模型。这说明时序模型必须同时回答三个问题：记什么、何时忘、上游观测不可信时是否应拒绝更新。

时序目标越精细，标注误差越不能被忽略。[TouchMoment](https://arxiv.org/abs/2604.12343) 要在强头动、近距离遮挡与“几乎接触”之间找到精确的首次触碰帧，评测容差严格到 0–2 帧；但它的大规模自动训练标注与手工标签平均差 1.94 帧。也就是说，标注噪声与评测容差处在同一量级。对这类任务，光报一个平均精度远远不够，标注时间不确定性必须进入评测解释。

## 四、真实性、精确 3D 真值和采集成本无法同时最优

第一视角数据有一个基本张力：越是真实、自然、可移动的场景，越难得到毫米级 3D 手真值。[Ego–Exo 移动采集架](https://arxiv.org/abs/2510.02601) 使用 8 个 exo 鱼眼相机、2 个 ego 相机、OptiTrack、硬件同步与标定，才将可验证的 3D 手标注带到移动场景。这种系统有力，但 8 公斤级采集装置本身也会改变参与者的行为和场景覆盖。

合成数据能扩展姿态和标注，但不能被当成真实数据的无条件替代。[HOI-Synth](https://arxiv.org/abs/2603.29733) 的跨数据集实验表明，合成数据在少量真实标注和域适应下有价值，但纯合成数据不能完全替代真实 HOI 数据；而且该证据是单帧分割/检测，并没有证明轨迹连续性。[EvHand-FPV](https://arxiv.org/abs/2509.13883) 的现实边界更直接：真实事件数据只有 2D 标注，因此真实 3D 性能无法直接验证，论文的 3D 评测只能留在合成域。

手物接触数据更难。[EPIC-Contact / HOPformer](https://arxiv.org/abs/2606.30598) 用中心帧人工接触标注向整段 clip 传播，扩大了野外 3D HOI 监督，但传播会被左右手辨识错误和相机跳变污染。这提示数据集不应只发布一个硬标签，还要保留生成路径、每帧置信度和可能的传播失效。

## 五、多模态不是免费的精度奖励

事件相机对快速运动、低光和低延迟有价值，但它对慢变信号不敏感，将事件流重新帧化又会损失异步表示的优势。[EventEgoHands](https://arxiv.org/abs/2606.10790) 用 RGB 视频经 v2e 合成事件，并主要依赖伪标签扩大手框数据；它对手检测有直接价值，但并不覆盖真实事件噪声、3D、左右手身份或长时追踪。

视觉–IMU 融合可以在遮挡下保留手指的高频运动，同时由视觉给腕部绝对位置提供锚点。[AVI-HT](https://arxiv.org/abs/2605.21714) 支持这种互补性，但也报告了对 IMU 噪声和时间对齐的敏感性。同时，手套会改变手的外观；[AirGlove](https://arxiv.org/abs/2602.05159) 表明，在裸手上预训练的追踪器遇到不同传感手套时性能会大幅下降。传感器增加的不只是信息，也有同步、标定、功耗、外观域差和跨设备泛化债务。

## 六、当前评测容易高估“真实可用的追踪”

一些方法已在可见帧上做到实时。例如 [Hand-4DGS](https://arxiv.org/abs/2606.19156) 报告约 60 FPS 的前馈式 4D 手重建。但它的定量评测排除了超过一半手框出界，或上游姿态器无法正确检测双手的帧。这不否定其在可评估区间的进步，但说明“成功帧内的 MPJPE”不能代表端到端可用性。

对追踪系统，评测至少要分开四层：可检测率，可见期间的 2D/3D 精度，遮挡或出框后的身份续接/重获取，以及在世界坐标中的长时漂移。如果一个数据集只标手框，它可以验证检测，但不能据此声称解决追踪；如果只在合成数据上有 3D 真值，真实 3D 性能就必须保留为未验证。

## 面向系统设计的可操作框架

| 层级 | 必须保留的数据 | 主指标 | 压力测试 | 不应被平均掉的失败 |
|---|---|---|---|---|
| 检测 | 全帧手框/掩码、出框状态 | recall、mAP、连续丢失长度 | 模糊、强自运动、低光、双手交叉 | 未检测帧被先排除 |
| 姿态 | 2D/3D 关键点、相机内参、标尺 | MPJPE/PA-MPJPE、腕部绝对误差 | 自遮挡、手物遮挡、鱼眼、跨设备 | 相对姿态很好但绝对深度错 |
| 追踪 | 身份、时间戳、观测质量、遮挡区间 | ID 续接、重获取延迟、漂移、加速误差 | 长时出框、双手交换、错误记忆回灌 | 先验补出平滑但错误的轨迹 |
| 接触/HOI | 手物接触、物体位姿、标注不确定性 | 触碰时刻误差、接触偏差、交互成功 | 近接触、手边别错误、相机跳变 | 轮廓吻合却接触关系错 |

## 研究空白与下一步

论文直接支持的空白有三个：真实事件数据的 3D 真值缺失；野外手物 3D 接触监督仍难以便宜扩展；新事件手数据集的光照、肤色和活动覆盖仍不足。

基于多篇证据，本文进一步推断，最值得投资的研究方向是“失败可观测的追踪”：模型应当显式输出左/右手、腕/指、位置/姿态的分解不确定性；在无观测锚点时区分“预测”和“观测”；评测从完整时间线起算，包括丢失和重获取。这个推断可被反证：如果一个仅优化可见帧单帧精度的模型，在未剪裁的真实长视频上同时显著降低身份中断、重获取延迟和世界轨迹漂移，那么显式失败建模的必要性就会减弱。

## 结论

Egocentric 手部追踪的实质已不再是一个独立检测器的问题，而是观测性、坐标系、时序不确定性、真值生产和端侧成本的联合问题。近一年的方法已经对遮挡恢复、世界坐标稳定、事件/惯性融合和野外接触监督提出了有效工具；但它们共同揭示的更重要结论是：没有任何一种新传感器或时序先验能无条件填补消失的观测。下一阶段应优先让数据和评测忠实保留失败，再让模型学会在失败中追踪。

## References

1. [EvHand-FPV: Efficient Event-Based 3D Hand Tracking from First-Person View](https://arxiv.org/abs/2509.13883)
2. [Towards Lightweight and Mobile Ground Truth Systems for Ego-Exo 3D Hand Tracking](https://arxiv.org/abs/2510.02601)
3. [SFHand: Language-Guided Streaming 3D Hand Forecasting](https://arxiv.org/abs/2511.18127)
4. [EgoGrasp: World-Space Hand-Object Interaction Recovery](https://arxiv.org/abs/2601.01050)
5. [DeltaDorsal: Hand Pose from Dorsal Skin Deformation](https://arxiv.org/abs/2601.15516)
6. [AirGlove: Appearance-Invariant Hand Tracking for Sensing Gloves](https://arxiv.org/abs/2602.05159)
7. [Leveraging Synthetic Data for Enhancing Egocentric Hand-Object Interaction Detection](https://arxiv.org/abs/2603.29733)
8. [Detecting Precise Hand Touch Moments in Egocentric Video](https://arxiv.org/abs/2604.12343)
9. [EgoEV-HandPose: Egocentric 3D Hand Pose Estimation and Gesture Recognition with Stereo Event Cameras](https://arxiv.org/abs/2605.12297)
10. [EgoForce: Forearm-Guided Camera-Space 3D Hand Pose](https://arxiv.org/abs/2605.12498)
11. [StableHand: Quality-Aware Flow Matching for World-Space Dual-Hand Motion Estimation](https://arxiv.org/abs/2605.18553)
12. [AVI-HT: Adaptive Vision-IMU Fusion for 3D Hand Tracking](https://arxiv.org/abs/2605.21714)
13. [A Multimodal RGB and Events Dataset for Hand Detection in First-Person View](https://arxiv.org/abs/2606.10790)
14. [Hand-4DGS: Feed-Forward 3D Gaussian Splatting for 4D Hand Reconstruction](https://arxiv.org/abs/2606.19156)
15. [Towards in-the-wild Egocentric 3D Hand-Object Pose Estimation](https://arxiv.org/abs/2606.30598)
