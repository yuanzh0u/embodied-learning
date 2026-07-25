# Review Packet: 近一年图像视觉定位方法的发展与挑战

## Scope

- Topic: 近一年图像视觉定位方法的发展与挑战
- Time range: 2025-07-15..2026-07-15
- Review style: `survey`
- Knowledge IDs: `EA-HARDWARE`, `EA-SENSOR`, `EA-EVAL`, `EA-4D`
- Evidence events: 15
- Topic cards: 4
- Registered source IDs available: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

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
- Trace IDs: `EA-VLOC-2026-0005`, `EA-VLOC-2026-0001`, `EA-VLOC-2026-0002`, `EA-VLOC-2026-0003`, `EA-VLOC-2026-0004`, `EA-VLOC-2026-0007`, `EA-VLOC-2026-0006`, `EA-VLOC-2026-0008`, `EA-VLOC-2026-0009`, `EA-VLOC-2026-0010`, `EA-VLOC-2026-0014`, `EA-VLOC-2026-0013`
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

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

- `EA-HARDWARE` 采集硬件与设备路线: 采集硬件不会收敛到单一设备，而会收敛到少数数据协议和接口范式。单目适合规模化起步，双目/多目和 LiDAR 适合几何、遮挡、动态或弱纹理场景；ARKit/SLAM/Tracking 可作低成本位姿输入但不能当工业真值。UMI 的数据质量从采集器设计开始：人体工学、力分布、重量、刚度、传感器组合和部署端同构程度会直接改变示教速度、损伤、负担和可执行性。
  - 具身采集不必须双目，关键看任务是否依赖稳定几何、相对深度和遮挡恢复。
  - 行业偏好单目来自工程经济性：便宜、易标定、低带宽、易维护、适配视觉预训练。
  - 双目落地瓶颈是标定同步、弱纹理/反光匹配失败、深度噪声融合和系统成本。
  - ARKit 可用于低成本 VIO、位姿跟踪和快速原型，但不适合作唯一计量真值。
  - VR/AR tracking 是低成本人机输入，需记录置信度、丢踪事件和时间戳质量。
- `EA-SENSOR` 传感器与多模态感知: 视觉 backbone 是语义和几何主干，但不是完整机器人感知系统。具身感知误差还包括关键状态不可观测、时间/空间对齐、模态融合和评测错位。3D、触觉与力/力矩的价值在于补充遮挡、接触、滑移、材料和局部形变；触觉世界模型应预测动作条件下的接触演化，而不只是重建触觉图像。多模态建模的目标不是堆传感器，而是让每个模态在闭环中产生可验证收益且不污染已有先验。
  - RGB 会丢失深度、尺度、表面法向、6D 位姿、材料、摩擦、滑移和接触力等物理信息。
  - 3D/点云对插入、堆叠、精确抓取和空间约束任务收益更大。
  - 触觉与视觉是互补关系：视觉负责全局语义和接触前规划，触觉负责接触后的局部状态。
  - 力/力矩是低维全局受力，触觉是高维局部接触分布，两者不能混同。
  - 腕部相机能替代部分近距离视觉确认，但不能替代滑移、压力、摩擦和材料感知。
- `EA-4D` 4D 时空推理与世界动态: 具身智能中的 4D 不是单一模型类型，而是把 3D 几何、时间连续性、动作后果和动态记忆接入可执行闭环的能力集合。它既可以是 point tracks、pointmaps 或动态场景图等显式表征，也可以是训练期 privileged supervision、部署时 imagined rollout 和动作候选评分。高质量 4D 数据必须区分视觉动态、机器人动作、接触状态、失败恢复和奖励监督；视觉逼真度不能替代几何对应、动作忠实和真实闭环验证。
  - 动作标签说明“机器人怎么动”，但不完整说明“世界会怎样变化”；跨帧 3D point tracks 能补充世界动态监督。
  - 视频未来即使视觉合理，只要同一物理点跨帧漂移、接触关系不稳定，就难以抽取可靠动作。
  - 人类视频、UMI、真实机器人、失败 rollout 和伪 4D 标注能监督的字段不同，必须用 supervision mask 或字段白名单分级。
  - 世界模型从预测器走向部署时推理模块时，应执行候选动作生成、未来想象、进度/奖励估计和低质量动作修正。
  - 4D 场景图适合长期动态记忆和结构化查询，但受 SLAM、相似物体歧义、长序列成本和局部形变限制。
- `EA-EVAL` 评测体系与世界模型: 开放环评测适合快速筛模型，但不能替代闭环成功、安全过程和恢复能力。世界模型可以生成未来、筛选动作和降低真实试错成本，但成为策略评估器前必须证明 admissibility：不仅视觉连贯，还要动作忠实、物理约束正确、长程稳定、能识别失败并与真实排序相关。评测应分开记录预测保真与决策有效，防止“视频更真实”掩盖错误动作响应。
  - 机器人策略最终必须在真实或高保真仿真闭环中验证。
  - 交互任务难标准化，因为成功标准、初始条件、物理接触和人类偏好都随场景变化。
  - 除成功率外，应看效率、安全、稳定性、恢复能力、成本和质量。
  - 世界模型的瓶颈是物理可执行性、长期一致性、接触/摩擦/因果真实性和评估方法。
  - 成熟机器人系统可能由 VLA/策略模型、世界模型和底层控制器三层组成。

## Stance Distribution

| Stance | Meaning | Events |
|---|---|---|
| `support` | 支持 | 2 |
| `conditional` | 条件成立 | 7 |
| `limit` | 限制/负面 | 6 |

## Accepted Paper Inventory

| Paper | Published | Stances | Events |
|---|---|---|---|
| 2507.23569: Gaussian Splatting Feature Fields for Privacy-Preserving Visual Localization | 2025-07-31 | conditional | EA-VLOC-2026-0001 |
| 2510.00978: A Scene is Worth a Thousand Features: Feed-Forward Camera Localization from a Collection of Image Features | 2025-10-01 | conditional | EA-VLOC-2026-0002 |
| 2510.12387: Scene Coordinate Reconstruction Priors | 2025-10-14 | conditional | EA-VLOC-2026-0003 |
| 2510.13464: Through the Lens of Doubt: Robust and Efficient Uncertainty Estimation for Visual Place Recognition | 2025-10-15 | conditional | EA-VLOC-2026-0004 |
| 2512.17226: Robust Scene Coordinate Regression via Geometrically-Consistent Global Descriptors | 2025-12-19 | support | EA-VLOC-2026-0005 |
| 2603.04056: Long-Term Visual Localization in Dynamic Benthic Environments: A Dataset, Footprint-Based Ground Truth, and Visual Plac... | 2026-03-04 | limit | EA-VLOC-2026-0006 |
| 2603.13917: Evaluation of Visual Place Recognition Methods for Image Pair Retrieval in 3D Vision and Robotics | 2026-03-14 | conditional | EA-VLOC-2026-0007 |
| 2603.16538: Rethinking Pose Refinement in 3D Gaussian Splatting under Pose Prior and Geometric Uncertainty | 2026-03-17 | limit | EA-VLOC-2026-0008 |
| 2604.22390: Region Matters: Efficient and Reliable Region-Aware Visual Place Recognition | 2026-04-24 | limit | EA-VLOC-2026-0009 |
| 2605.07351: Disambiguating 2D-3D Correspondences in Gaussian Splatting-based Feature Fields for Visual Localization | 2026-05-08 | limit | EA-VLOC-2026-0010 |
| 2605.28048: SAFEVPR: Patch-Based Conformal Verification for Safe Cross-Condition Sequence Visual Place Recognition | 2026-05-27 | limit | EA-VLOC-2026-0011 |
| 2605.30769: DisPlace: Discriminative Place Projections for Multi-Reference Visual Place Recognition | 2026-05-29 | conditional | EA-VLOC-2026-0012 |
| 2606.13206: Visual Place Recognition in Forests with Depth-Aware Distillation | 2026-06-11 | support | EA-VLOC-2026-0013 |
| 2606.31164: Seeing Through the Weights: Privacy Leakage in Scene Coordinate Regression | 2026-06-30 | limit | EA-VLOC-2026-0014 |
| 2607.00090: Lost in the Tail: Addressing Geographic Imbalance in Urban Visual Place Recognition | 2026-06-30 | conditional | EA-VLOC-2026-0015 |

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| EA-VLOC-2026-0005 | EA-HARDWARE | `support` | `direct` | 大场景SCR可通过同时约束视觉相似性与共视几何连接的全局描述子缓解感知别名和噪声图边，而不是只依赖局部特征或纯几何嵌入。 | 结论明确将韧性提升归因于视觉内容和几何关系的联合建模。 (7 Conclusion) | son-tung-nguyen; alejandro-fontan; michael-milford; et al. | 2512.17226 |
| EA-VLOC-2026-0001 | EA-HARDWARE | `conditional` | `direct` | 3DGS特征场可把渲染和特征学习接入位姿细化，但定位可靠性仍受底层3DGS几何质量约束，弱纹理平坦场景会直接拖累结果。 | 作者在7Scenes的Stairs场景明确把退化归因于纹理缺失和平坦布局导致的初始3D结构质量差。 (5.1 Visual Localization) | maxime-pietrantoni; gabriela-csurka; torsten-sattler | 2507.23569 |
| EA-VLOC-2026-0002 | EA-HARDWARE | `conditional` | `direct` | 前馈式稀疏特征地图能把逐场景地图准备降到检索级别，但这一优势仍依赖选到相关参考图像；随机或均匀选择会导致准确率下降。 | 作者在限制实验中移除检索并改用随机/均匀参考，观察到FastForward准确率下降。 (page 10) | axel-barroso-laguna; tommaso-cavallari; victor-adrian-prisacariu; et al. | 2510.00978 |
| EA-VLOC-2026-0003 | EA-HARDWARE | `conditional` | `direct` | 重建先验可以改善ACE系场景坐标回归而不增加查询时延，但当前证据主要限于室内，户外需要重新设计深度分布与扩散先验数据。 | 结论同时报告性能增益、无查询时延代价和室内证据边界。 (5 Conclusion) | wenjing-bian; axel-barroso-laguna; tommaso-cavallari; et al. | 2510.12387 |
| EA-VLOC-2026-0004 | EA-HARDWARE | `conditional` | `direct` | 训练免费的相似度分布不确定性可作为VPR错误匹配拒绝器，但在极端重复场景中，仅看分数仍可能失效，需要几何线索补充。 | 作者在结论明确指出分数依赖在极端重复场景中的退化。 (VII Conclusions and Future Work) | emily-miller; michael-milford; muhammad-burhan-hafez; et al. | 2510.13464 |
| EA-VLOC-2026-0007 | EA-HARDWARE | `conditional` | `direct` | 现代VPR不存在单一最优骨干：ViT更适合强感知别名和缺帧，CNN在实时系统中通常提供更好的检索质量—运行时间折中。 | 结论依据三类数据集比较CNN与ViT并给出按场景选型建议。 (7 Conclusion) | dennis-haitz; athradi-shritish-shetty; michael-weinmann; et al. | 2603.13917 |
| EA-VLOC-2026-0006 | EA-HARDWARE | `limit` | `direct` | 视觉定位评测的真值定义会显著改变结论：仅按相机位置接近判正，会在地形起伏或高度变化大时系统性高估VPR表现。 | 作者比较两套真值并发现足迹重叠与真实检索更一致。 (5 Conclusion) | martin-kvisvik-larsen; oscar-pizarro | 2603.04056 |
| EA-VLOC-2026-0008 | EA-HARDWARE | `limit` | `direct` | 3DGS位姿细化不是全局纠错器：它高度依赖初始位姿质量，单一错误Top-1检索即使视觉相似也可能从场景错误一侧开始，局部细化难以恢复。 | 作者在检索先验补充实验中明确说明细化只在初值附近局部调整。 (A Leveraging Image Retrieval Prior) | mangyu-kong; jaewon-lee; seongwon-lee; et al. | 2603.16538 |
| EA-VLOC-2026-0009 | EA-HARDWARE | `limit` | `direct` | VPR基准接近饱和时，固定地理半径标签本身会成为主要误差源：25米阈值可能忽略真实视觉重叠，使方法排名与可用定位不一致。 | 讨论明确指出当前任务标签忽视视觉重叠并放大歧义。 (5 Discussion) | shunpeng-chen; yukun-song; changwei-wang; et al. | 2604.22390 |
| EA-VLOC-2026-0010 | EA-HARDWARE | `limit` | `direct` | 3DGS地图的照片真实度不等于定位几何可用性：冗余高斯及像素到高斯的多对一对应会削弱匹配鲁棒性并使PnP收敛不稳。 | 作者在结论把问题归结为照片度量GSFF与点式PnP对应的结构错配。 (5 Conclusion) | miso-lee; sangeek-hyun; yerim-jeon; et al. | 2605.07351 |
| EA-VLOC-2026-0014 | EA-HARDWARE | `limit` | `direct` | 把场景存进SCR网络权重并不天然保护隐私：在可发出代理查询并读取三维预测时，攻击者能够聚合恢复场景几何和外观线索。 | 论文结论明确说明代理查询与三维预测聚合可恢复几何和外观。 (6 Conclusion) | oleksii-nasypanyi; jaemin-cho; utku-ozbulak; et al. | 2606.31164 |
| EA-VLOC-2026-0013 | EA-SENSOR | `support` | `direct` | 在森林VPR中，把深度几何蒸馏进外观描述子可同时改善同序列与跨序列识别，说明几何先验是缓解重复纹理的一条有效方向。 | 作者直接报告DAD在两种评估中均超过仅外观SALAD。 (III Results and Discussion) | walter-nedov; saimunur-rahman; kavindie-katuwandeniya; et al. | 2606.13206 |
| EA-VLOC-2026-0012 | EA-SENSOR | `conditional` | `direct` | 多参考地点表示的收益具有分布条件：参考遍历覆盖查询变化时，判别压缩有效；极端视角且视觉重叠很少时，保留各参考描述子的策略更稳。 | 作者在讨论中明确把收益与参考—查询变化代表性绑定，并指出极端视角的落后情形。 (VI Discussion and Conclusion) | dhyey-manish-rajani; michael-milford; tobias-fischer | 2605.30769 |
| EA-VLOC-2026-0015 | EA-SENSOR | `conditional` | `direct` | VPR正在从平均召回转向地理分布鲁棒性，但现有长尾建模仍主要按地理类样本数划分，尚不能代表地点本身的视觉难度。 | 作者在结论明确承认当前长尾只按每类样本量定义。 (5 Conclusion) | zhiyao-shu; jiacheng-yang; yang-lu; et al. | 2607.00090 |
| EA-VLOC-2026-0011 | EA-SENSOR | `limit` | `direct` | 跨条件VPR的安全性必须与覆盖率一起评估：重复且无信息的景观中，校准验证器可以靠全局拒识维持安全，但定位效用降为零。 | 作者把Nordland描述为已知但安全的边界，因为系统能检测无信息状态并整体拒绝。 (VII-B When does it fail?) | ha-sier; jiaqiang-zhang; zhuo-zou; et al. | 2605.28048 |

## Author Stance Events

| Event | Authors | Institutions | Stance | Claim |
|---|---|---|---|---|
| EA-VLOC-2026-0005 | son-tung-nguyen; alejandro-fontan; michael-milford; et al. | unlisted | `support` | 大场景SCR可通过同时约束视觉相似性与共视几何连接的全局描述子缓解感知别名和噪声图边，而不是只依赖局部特征或纯几何嵌入。 |
| EA-VLOC-2026-0001 | maxime-pietrantoni; gabriela-csurka; torsten-sattler | unlisted | `conditional` | 3DGS特征场可把渲染和特征学习接入位姿细化，但定位可靠性仍受底层3DGS几何质量约束，弱纹理平坦场景会直接拖累结果。 |
| EA-VLOC-2026-0002 | axel-barroso-laguna; tommaso-cavallari; victor-adrian-prisacariu; et al. | unlisted | `conditional` | 前馈式稀疏特征地图能把逐场景地图准备降到检索级别，但这一优势仍依赖选到相关参考图像；随机或均匀选择会导致准确率下降。 |
| EA-VLOC-2026-0003 | wenjing-bian; axel-barroso-laguna; tommaso-cavallari; et al. | unlisted | `conditional` | 重建先验可以改善ACE系场景坐标回归而不增加查询时延，但当前证据主要限于室内，户外需要重新设计深度分布与扩散先验数据。 |
| EA-VLOC-2026-0004 | emily-miller; michael-milford; muhammad-burhan-hafez; et al. | unlisted | `conditional` | 训练免费的相似度分布不确定性可作为VPR错误匹配拒绝器，但在极端重复场景中，仅看分数仍可能失效，需要几何线索补充。 |
| EA-VLOC-2026-0007 | dennis-haitz; athradi-shritish-shetty; michael-weinmann; et al. | unlisted | `conditional` | 现代VPR不存在单一最优骨干：ViT更适合强感知别名和缺帧，CNN在实时系统中通常提供更好的检索质量—运行时间折中。 |
| EA-VLOC-2026-0006 | martin-kvisvik-larsen; oscar-pizarro | unlisted | `limit` | 视觉定位评测的真值定义会显著改变结论：仅按相机位置接近判正，会在地形起伏或高度变化大时系统性高估VPR表现。 |
| EA-VLOC-2026-0008 | mangyu-kong; jaewon-lee; seongwon-lee; et al. | unlisted | `limit` | 3DGS位姿细化不是全局纠错器：它高度依赖初始位姿质量，单一错误Top-1检索即使视觉相似也可能从场景错误一侧开始，局部细化难以恢复。 |
| EA-VLOC-2026-0009 | shunpeng-chen; yukun-song; changwei-wang; et al. | unlisted | `limit` | VPR基准接近饱和时，固定地理半径标签本身会成为主要误差源：25米阈值可能忽略真实视觉重叠，使方法排名与可用定位不一致。 |
| EA-VLOC-2026-0010 | miso-lee; sangeek-hyun; yerim-jeon; et al. | unlisted | `limit` | 3DGS地图的照片真实度不等于定位几何可用性：冗余高斯及像素到高斯的多对一对应会削弱匹配鲁棒性并使PnP收敛不稳。 |
| EA-VLOC-2026-0014 | oleksii-nasypanyi; jaemin-cho; utku-ozbulak; et al. | unlisted | `limit` | 把场景存进SCR网络权重并不天然保护隐私：在可发出代理查询并读取三维预测时，攻击者能够聚合恢复场景几何和外观线索。 |
| EA-VLOC-2026-0013 | walter-nedov; saimunur-rahman; kavindie-katuwandeniya; et al. | unlisted | `support` | 在森林VPR中，把深度几何蒸馏进外观描述子可同时改善同序列与跨序列识别，说明几何先验是缓解重复纹理的一条有效方向。 |
| EA-VLOC-2026-0012 | dhyey-manish-rajani; michael-milford; tobias-fischer | unlisted | `conditional` | 多参考地点表示的收益具有分布条件：参考遍历覆盖查询变化时，判别压缩有效；极端视角且视觉重叠很少时，保留各参考描述子的策略更稳。 |
| EA-VLOC-2026-0015 | zhiyao-shu; jiacheng-yang; yang-lu; et al. | unlisted | `conditional` | VPR正在从平均召回转向地理分布鲁棒性，但现有长尾建模仍主要按地理类样本数划分，尚不能代表地点本身的视觉难度。 |
| EA-VLOC-2026-0011 | ha-sier; jiaqiang-zhang; zhuo-zou; et al. | unlisted | `limit` | 跨条件VPR的安全性必须与覆盖率一起评估：重复且无信息的景观中，校准验证器可以靠全局拒识维持安全，但定位效用降为零。 |

## Synthesis Slots

### 共识/正向证据
- `EA-VLOC-2026-0005`: 大场景SCR可通过同时约束视觉相似性与共视几何连接的全局描述子缓解感知别名和噪声图边，而不是只依赖局部特征或纯几何嵌入。
- `EA-VLOC-2026-0013`: 在森林VPR中，把深度几何蒸馏进外观描述子可同时改善同序列与跨序列识别，说明几何先验是缓解重复纹理的一条有效方向。
### 条件成立
- `EA-VLOC-2026-0001`: 3DGS特征场可把渲染和特征学习接入位姿细化，但定位可靠性仍受底层3DGS几何质量约束，弱纹理平坦场景会直接拖累结果。
- `EA-VLOC-2026-0002`: 前馈式稀疏特征地图能把逐场景地图准备降到检索级别，但这一优势仍依赖选到相关参考图像；随机或均匀选择会导致准确率下降。
- `EA-VLOC-2026-0003`: 重建先验可以改善ACE系场景坐标回归而不增加查询时延，但当前证据主要限于室内，户外需要重新设计深度分布与扩散先验数据。
- `EA-VLOC-2026-0004`: 训练免费的相似度分布不确定性可作为VPR错误匹配拒绝器，但在极端重复场景中，仅看分数仍可能失效，需要几何线索补充。
- `EA-VLOC-2026-0007`: 现代VPR不存在单一最优骨干：ViT更适合强感知别名和缺帧，CNN在实时系统中通常提供更好的检索质量—运行时间折中。
- `EA-VLOC-2026-0012`: 多参考地点表示的收益具有分布条件：参考遍历覆盖查询变化时，判别压缩有效；极端视角且视觉重叠很少时，保留各参考描述子的策略更稳。
- `EA-VLOC-2026-0015`: VPR正在从平均召回转向地理分布鲁棒性，但现有长尾建模仍主要按地理类样本数划分，尚不能代表地点本身的视觉难度。
### 限制与失败模式
- `EA-VLOC-2026-0006`: 视觉定位评测的真值定义会显著改变结论：仅按相机位置接近判正，会在地形起伏或高度变化大时系统性高估VPR表现。
- `EA-VLOC-2026-0008`: 3DGS位姿细化不是全局纠错器：它高度依赖初始位姿质量，单一错误Top-1检索即使视觉相似也可能从场景错误一侧开始，局部细化难以恢复。
- `EA-VLOC-2026-0009`: VPR基准接近饱和时，固定地理半径标签本身会成为主要误差源：25米阈值可能忽略真实视觉重叠，使方法排名与可用定位不一致。
- `EA-VLOC-2026-0010`: 3DGS地图的照片真实度不等于定位几何可用性：冗余高斯及像素到高斯的多对一对应会削弱匹配鲁棒性并使PnP收敛不稳。
- `EA-VLOC-2026-0014`: 把场景存进SCR网络权重并不天然保护隐私：在可发出代理查询并读取三维预测时，攻击者能够聚合恢复场景几何和外观线索。
- `EA-VLOC-2026-0011`: 跨条件VPR的安全性必须与覆盖率一起评估：重复且无信息的景观中，校准验证器可以靠全局拒识维持安全，但定位效用降为零。

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## Style Menu

- Evidence sufficiency: formal-ready
- Paper-level sources: 15 / 15 floor (not a cap)
- Recommended default: all
- Core claims:
  - `EA-VLOC-2026-0005` 大场景SCR可通过同时约束视觉相似性与共视几何连接的全局描述子缓解感知别名和噪声图边，而不是只依赖局部特征或纯几何嵌入。
  - `EA-VLOC-2026-0001` 3DGS特征场可把渲染和特征学习接入位姿细化，但定位可靠性仍受底层3DGS几何质量约束，弱纹理平坦场景会直接拖累结果。
  - `EA-VLOC-2026-0002` 前馈式稀疏特征地图能把逐场景地图准备降到检索级别，但这一优势仍依赖选到相关参考图像；随机或均匀选择会导致准确率下降。
- Scientific memo preview: 《近一年图像视觉定位方法的发展与挑战》研究备忘录: evidence scope, claim map, disagreements, and gaps.
- Expert explainer preview: TL;DR: 近一年图像视觉定位方法的发展与挑战 的关键不在单点结论，而在证据条件和误区拆解。
- KOL thread preview: 近一年图像视觉定位方法的发展与挑战: 先看证据边界，再谈一个可传播的反常识洞察。

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
