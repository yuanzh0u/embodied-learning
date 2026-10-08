# 手部检测精度如何传导为机器人末端轨迹误差：无本体第一人称视频路线的误差链、阈值带与缓解谱系

## 研究边界

本备忘回答的问题是：在无本体（robot-free）ego-centric 人类视频中，手部检测/追踪精度如何影响重定向后机器人末端轨迹的精度与可用性，误差来自哪里、沿什么路径传播、可接受阈值是否存在、以及有哪些被验证的缓解手段。证据来自 2025 年 9 月至 2026 年 8 月间 86 篇通过质量门的论文（357 条接受事件），覆盖手部重建基准、ego 采集系统、重定向方法与下游策略学习四个层面。

本 run 不能确立的内容需要先声明：真正把"检测误差→下游成功率"做成受控因果实验的只有一项噪声注入研究（见下文剂量-响应一节）；绝大多数系统只报告任务成功率这一代理指标，不报告重定向轨迹相对真值的几何误差，因此"可接受阈值"只能以多个任务特定的锚点拼出量级带，而无法给出统一传递函数。

## 中心判断

手部检测误差对末端轨迹的影响既不是可以忽略的背景噪声，也不是不可逾越的硬约束，而是一条在多个环节可被截断、吸收或绕开的传导链——前提是工程上显式处理它。误差的下游代价由三个变量决定：误差落在链条的哪个环节（单目深度与坐标系是最大的放大器，接触建立阶段是最脆弱的下游环节）、任务的精度需求（阈值由任务几何而非固定常数决定）、以及训练配方的噪声容忍度（同一质量的手部标签在不同共训练设计下可以从净收益翻转为净损害）。当前 SOTA 单目手部估计的标签质量已经越过"有净迁移收益"的门槛，但与动捕级标签之间仍存在可测量的成功率差距；这个差距可以用传感锚定、几何后处理或表示层绕行来压缩，而不是只能靠等待更好的检测器。

## 检测端的真实地形：关节回归精度已经不是瓶颈，世界系定位与覆盖率才是

单帧手部重建在相机系内已相当精确。[WiLoR](https://arxiv.org/abs/2409.12259) 在手-物交互基准 HO3Dv2 上达到 PA-MPJPE 7.5mm，逐帧重建的帧间抖动也远低于前代（手腕根位移误差 RTE 0.07，HaMeR 为 2.92）。但 PA-MPJPE 是剔除全局变换后的对齐精度，它会掩盖对下游最致命的误差。[EgoForce](https://arxiv.org/abs/2605.12498) 的跨基准对比把这个脱节量化得很清楚：各方法的对齐精度都在 5.6-9.9mm，而绝对相机系定位误差从最好方法的 43.9-49.5mm 一路垮塌到"root-relative 预测+单目深度提升"路线的米级（HaMeR 加深度提升在 HOT3D 上达 4493.7mm）。世界系重建同样如此：[HaWoR](https://arxiv.org/abs/2501.02973) 在 HOT3D ego 序列上世界系 W-MPJPE 为 33.20mm，而手部出视野帧经学习补全后仍达 66.25mm，约为可见帧的两倍。[AoE](https://arxiv.org/abs/2602.23893) 的云端管线报告 PA-MPJPE 3.7-7.4mm，但弱纹理场景下相机轨迹的尺度无关误差退化到 16.2mm——手估准了，承载手的坐标系漂了。

比精度更硬的是覆盖率约束。一项用 ego 手部检测驱动 IK 重定向的对照研究（[Vision-Based Hand Shadowing](https://arxiv.org/abs/2603.11383)）给出了一组少见的可用性数字：结构化实验室里 MediaPipe 的右手检出率只有 77.3%，17.1% 的帧完全无检测；把检测器换成更强的 WiLoR 只挽回 3.5% 的帧，因为瓶颈是"手在 ego 视野里不可见"，检出后的 IK 目标转换率两个检测器都超过 95%。同一管线在实验室取得 86.7% 抓取成功率，到杂货店等野外环境跌到 9.3%，首要失效模式是周围物体遮挡手部。对读者的直接含义是：评估一条 ego 采集管线时，帧级检测覆盖率与出画率比 PA-MPJPE 更接近末端轨迹质量的真实上限。

## 误差的放大与传导：深度与坐标系是放大器，接触是显现处

从检测输出到机器人末端轨迹之间有三个系统性放大环节。第一个是单目深度与坐标系。[EgoZero](https://arxiv.org/abs/2505.20290) 的消融很说明问题：最优单目度量深度模型即使经场景内多个 ArUco 标记标定仍有超过 5cm 的深度误差，用估计深度替代三角化训练的策略在全部 7 个任务上无一例外失败（0/15）；同一作者承认组合后的动作标签仍含 1-2cm 误差，使策略无法解决高精度任务。坐标系级误差更具灾难性：[2602.09013](https://arxiv.org/abs/2602.09013) 报告 in-the-wild 视频不做重力对齐时倒茶成功率为 0%，对齐后与有外参标定的数据无显著差异。ego 路线还有两个特有污染源：头部自运动会混入以相机帧表达的手部轨迹量，以及逐帧形状推理不一致造成的尺度-深度歧义（[Dexterous Point Policy](https://arxiv.org/abs/2606.10614) 实测 HaWoR 在单条视频内手部尺度变化超过 10%，并向深度轴注入 30Hz 以上的高频噪声）。

第二个放大环节是重定向本身。人类采集数据集经重定向进入机器人训练存在约三分之一的验收损耗：[Dex1B](https://arxiv.org/abs/2506.17198) 报告 DexYCB 与 ARCTIC 重定向加噪后只有 62% 和 64% 的轨迹在仿真中达成任务目标。[X-Diffusion](https://arxiv.org/abs/2511.04671) 的朴素共训练对照中，约 50% 的人演示在 IK 重放后因运动学/动力学失败被人工丢弃。[Dex-X](https://arxiv.org/abs/2609.07747) 给出更尖锐的下限：单目视频重建的重定向轨迹直接开环回放，六类灵巧任务仿真平均成功率仅 5.2%。

第三个环节是接触。检测误差在自由空间段往往无害，在接触建立瞬间被放大为功能失败。[DemoBridge](https://arxiv.org/abs/2607.09519) 的表述值得记住：单视角参考位姿只精确到数毫米，当物体宽度接近夹爪开口时，这个偏移就足以漏抓——可接受阈值由任务几何决定，不是固定数值。[重定向目标设计的研究](https://arxiv.org/abs/2506.09384)同样发现，去掉指尖捏合项后机器人手无法闭合拇指-食指间隙，捏取类任务直接失败。腕部旋转是另一个公认弱点：[Translation as a Bridging Action](https://arxiv.org/abs/2606.28133) 指出预测器误差使人类腕部旋转尤其不可靠，直接把 6DoF 腕部动作回放到机器人会产生扭曲行为。

## 剂量-响应与阈值：没有普适毫米数，但有可操作的量级带

本领域唯一直接的因果证据来自一项共训练研究（[What Matters When Cotraining](https://arxiv.org/abs/2606.06627)）：以三角测量的手部为基准，注入按 SOTA 单目估计器误差分布拟合的标定噪声，迁移成功率从 0.0× 噪声的 48.3% 单调降到 0.5× 的 30.0% 与 1.0× 的 20.0%。参照系中该单目估计器（HaWoR）的世界系误差 W-MPJPE 达 161.85mm——这个数远大于直觉上"可用"的水平，因为其 1 秒预测视界内的手部关节平移常被深度噪声主导。然而同一批 HaWoR 标签做共训练仍得到 24.7% 成功率，高于纯机器人训练的 11.9%：噪声标签已过净收益门槛，但距三角测量标签的 41.5% 还差约 17 个百分点。这是本文推断的第一根支柱：手部质量对迁移有单调因果效应，但效应是渐变的，不存在"低于某精度就无用"的断崖。

阈值侧的证据是一组任务特定锚点，拼起来呈现清晰的分层结构。精密接触层：[HoMMI](https://arxiv.org/abs/2603.03243) 的深度噪声注入实验显示 1cm 标准差以内性能不变、20mm 时成功率从 90% 跌到 50%；[Video2Sim2Real](https://arxiv.org/abs/2606.08828) 报告规划路点 1-2cm 的末端位姿偏差即可导致精密任务失败，其对策是让蒸馏策略在物体位姿 ±5cm/±10° 的局部随机化下训练以获得鲁棒性；[TELEDEXTER](https://arxiv.org/abs/2607.11481) 训练时注入 ±5mm 指尖/物体位置噪声即可零样本迁移真机，可视为追踪噪声可接受预算的一个参考值。轨迹验收层：[Do as I Do](https://arxiv.org/abs/2606.19333) 把成功重定向定义为平均位置误差小于 0.1m、旋转小于 0.5rad，在 655 条含噪重建参考上达 71%；[Dex-X](https://arxiv.org/abs/2609.07747) 把全轨迹平均末端追踪误差超过 8cm 的演示变体直接排除出训练；[EgoRecovery](https://arxiv.org/abs/2607.19745) 对帧间跳变超过 30mm 或 20° 的帧做插值替换。表示与先验层：[EgoVLA](https://arxiv.org/abs/2507.12440) 未来腕部平移预测平均误差约 8cm，经机器人微调后仍有 77.78% 的短程任务成功率；[Dexterous Point Policy](https://arxiv.org/abs/2606.10614) 明确区分训练阶段——互联网规模预训练直接使用精度较低的现成关键点标签即可，任务微调集的关键点则必须准确；[EgoScale](https://arxiv.org/abs/2602.16710) 在 1k-20k 小时扫描中发现下游完成度随含噪人类数据量对数线性单调上升（0.30 到 0.71），即规模本身可以吸收标注噪声。综合起来：精密接触操作需要毫米到亚厘米级的上游精度，短程桌面任务容忍厘米级，预训练阶段的监督信号容忍分米级——这是一条量级带，不是一个阈值。

## 缓解谱系：四个层级，各有代价

证据中出现过的缓解手段可以按作用层级归成四类，它们的共同点是都有效，但没有一个能单独消除问题。

信号级处理最便宜也最不充分。时序平滑项、低通滤波、Savitzky-Golay 平滑、遮挡帧插值是几乎所有管线的标配（[EgoRecovery](https://arxiv.org/abs/2607.19745)、[ImMimic](https://arxiv.org/abs/2509.10952) 的三级吸收链、[Bunny-VisionPro](https://arxiv.org/abs/2407.03162) 的重定向目标时序惩罚项）。它能压掉高频抖动，但对"手根本不可见"的帧无能为力——无检测帧的信息是零，任何启发式都无法恢复。

几何与物理级修正针对的是"估计出来的轨迹物理上不可行"。接触优化把悬空/穿透的抓握拉回物体表面：[EgoAERO](https://arxiv.org/abs/2606.08057) 的有界接触修正将成功率从 36.2% 提到 49.5%，[2602.09013](https://arxiv.org/abs/2602.09013) 用 ContactOpt 把 20 物体平均抓握成功率从 30.7% 提到 63.75%。物理一致性约束的效果更大：[Video2Sim2Real](https://arxiv.org/abs/2606.08828) 中依赖预训练位姿估计直接校正的路线只有 15.7% 成功率，而对象中心关键帧锚定加策略蒸馏达 95.7%；[Do as I Do](https://arxiv.org/abs/2606.19333) 在含噪重建参考上加入 warmup、力扰动与 transition reward 后重定向成功率从 25% 升到 71%。

表示级处理改变的是"误差进入监督信号的形式"。只共享相对腕部平移而丢弃旋转监督，把共训练成功率从 12.5% 提到 22.5%（[Translation as a Bridging Action](https://arxiv.org/abs/2606.28133)）；[RealDexUMI](https://arxiv.org/abs/2606.06033) 只用 6-DoF 追踪位姿构造手部局部系相对动作标签，从设计上放宽了对全局帧精度的要求；[3PoinTr](https://arxiv.org/abs/2603.08485) 以 3D 点轨为中间表征绕开手部姿态估计，仅用 20 条机器人演示加每任务 50 段人类视频就在四个真机任务上达 75/80 的平均成功。[ImMimic](https://arxiv.org/abs/2509.10952) 的对照还提示动作空间映射整体优于视觉特征映射，且更类人的末端不一定更接近机器人可执行动作——人-机动作距离（而非形态相似度）才是迁移收益的预测变量。

训练级与硬件级是最后两道闸。训练级：[X-Diffusion](https://arxiv.org/abs/2511.04671) 只在加噪后人-机动作不可区分的扩散步纳入人类动作，平均成功率较跨本体基线高 16%；[EgoScaler](https://arxiv.org/abs/2509.21986) 的背景轨迹相似度过滤给出少见的质量-规模权衡数字——不过滤时 2 倍含噪数据反而使真机成功率下降约 16 个百分点（38.8 对 55.0）；[EgoBridge](https://arxiv.org/abs/2509.19626) 的域对齐在机器人数据未覆盖的行为区域取得 33% 成功率而基线全为 0。硬件级则是承认视觉链路的局限并绕行：[DexUMI](https://arxiv.org/abs/2505.21864) 用外骨骼编码器直读关节角，设计动机明确是消除视觉指尖追踪的误差；[DexDirect](https://arxiv.org/abs/2607.27784) 让被拖动的真实机器人记录臂部轨迹，同时间预算下成功演示 481 条对纯视觉方案的 28 条。折中方案是用传感锚定世界系而保留视觉的灵活性：[ActiveUMI](https://arxiv.org/abs/2510.01607) 的 VR 追踪回放相对位姿误差 4.0mm 对 UMI 视觉 SLAM 的 10.1mm（原文正文有一处主语笔误，图注数据为 ActiveUMI 更优），[HiFi-UMI](https://arxiv.org/abs/2607.25895) 的头戴双目惯性 SLAM 加标记块在约 2m 工作空间达 3mm 末端误差且仅用此类数据后训练的策略与遥操作后训练的差距在抽样噪声内，[EgoMI](https://arxiv.org/abs/2511.00153) 的系统对比表给出 UMI 8.855mm、AirExo-2 1.737mm、VR 手柄方案 2.126mm 的末端追踪误差谱。

## 条件与分歧

证据中有三处真实分歧，不宜抹平。其一，"精度是否重要"与所走的迁移路线强相关。[Phantom](https://arxiv.org/abs/2503.00779) 作者明确承认方法整体性能受限于手部姿态估计器；而 [Masquerade](https://arxiv.org/abs/2508.09976) 只用带噪 2D 手部关键点做编辑视频的辅助监督，人类视频比例从 0% 增到 100% 时成功率从 2% 单调升到 68%，[WIYH](https://arxiv.org/abs/2512.24310) 作者也明确说人类数据的下游收益来自动作多样性而非精度。本文的调和读法是：当手部信号只作表示层监督（预训练先验、辅助标签、视觉编辑锚点）时，低精度可被规模与过滤吸收；当手部轨迹经几何链路直接变成机器人动作标签时，精度是前置条件。其二，含噪人类标签是否有净收益取决于训练配方：同一批三角测量级标签，共享动作解码器的共训练设计只有 14.7-17.5% 成功率，而 token 级融合加本体专属编解码器达 41.5%——[该研究](https://arxiv.org/abs/2606.06627)论证大动作鸿沟下共享确定性解码器必然失败。其三，阈值结论不可跨任务外推：[EgoVLA](https://arxiv.org/abs/2507.12440) 的 8cm 腕部误差不妨碍短程任务，[EgoZero](https://arxiv.org/abs/2505.20290) 的 1-2cm 标签误差却已阻断高精度任务，两者都对，因为任务不同。

还需保留若干方法学警告。大量管线根本不报告轨迹几何精度，只给任务成功率代理，因此本文多数"噪声吸收"证据停留在任务层面；[Track2Act](https://arxiv.org/abs/2405.01527) 的点轨精度以同一现成追踪器的输出为训练监督与评估参照，存在同源循环；Dex1B 的重定向验收损耗对比混入了数据规模差异；所有阈值锚点都来自特定任务、本体与评测协议，直接搬到新设定前应重新标定。

## 可操作框架

| 任务精度需求 | 上游手部/腕部精度要求 | 推荐路线 | 代表锚点 |
|---|---|---|---|
| 预训练先验、表示监督 | 分米级可容忍 | 现成单目估计器 + 规模 + 降权/过滤 | EgoScale 20k 小时单调收益；Masquerade 2%→68% |
| 短程桌面抓取放置 | 厘米级 | 视觉链路 + 时序平滑 + 接触/物理后处理 | EgoVLA 8cm 仍 77.78%；EgoAERO 接触修正 +13.3pp |
| 精密接触（捏取、手内、插拔） | 毫米到亚厘米级 | 传感锚定世界系或编码器绕行 + 显式质量门 | HoMMI 1cm 深度噪声阈值；Dex-X 8cm 排除线；DexDirect 481 vs 28 |

## 研究空白与下一步

属于本 run 覆盖缺口的是：唯一直接的剂量-响应实验限于单一实验室的共训练设定，未覆盖灵巧手、移动操作与更长时程任务；多数 ego 采集系统（包括若干高引用管线）全程未量化手部追踪误差，"检测精度→末端轨迹"的传递函数在文献中基本未被直接测量。属于文献自认的缺口是：手部检测精度仍是系统性能的前置条件而非已被后处理解决的问题（多个管线在严重遮挡、快速运动、反光物体下退化）；接触密集阶段的误差预算如何分配、旋转监督如何在低噪声下恢复，均被作者列为未解方向。下一步最有杠杆的研究动作是：把噪声注入协议推广到更多任务族与本体，统一报告"腕部世界系误差 + 下游成功率"的双层口径，并把接触建立阶段单独作为误差预算的核算单元。

## 结论

这批证据改变的判断是：手部检测精度问题不应再被表述为"检测器够不够好"，而应表述为误差预算在传导链上的分配问题。单帧关节回归精度已够，世界系定位、覆盖率与接触阶段才是实际的约束；缓解手段谱系已经完整到可以让开发者按任务精度需求选择截断点——预训练靠规模吸收，桌面任务靠几何与物理后处理，精密接触靠传感锚定或硬件绕行。真正稀缺的不是更强的检测器，而是把检测误差当作可测量、可分配、可核算量的工程纪律。

## References

- [WiLoR: End-to-end 3D Hand Localization and Reconstruction in-the-wild](https://arxiv.org/abs/2409.12259)
- [HaWoR: World-Space Hand Motion Reconstruction from Egocentric Videos](https://arxiv.org/abs/2501.02973)
- [EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera](https://arxiv.org/abs/2605.12498)
- [AoE: Always-on Egocentric Human Video Collection for Embodied AI](https://arxiv.org/abs/2602.23893)
- [Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics](https://arxiv.org/abs/2603.11383)
- [EgoZero: Robot Learning from Smart Glasses](https://arxiv.org/abs/2505.20290)
- [Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction](https://arxiv.org/abs/2602.09013)
- [DemoBridge: A Simulation-in-the-Loop Toolkit for Single-View Human Demonstration Retargeting](https://arxiv.org/abs/2607.09519)
- [Dex1B: Learning with 1B Demonstrations for Dexterous Manipulation](https://arxiv.org/abs/2506.17198)
- [X-Diffusion: Training Diffusion Policies on Cross-Embodiment Human Demonstrations](https://arxiv.org/abs/2511.04671)
- [Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction](https://arxiv.org/abs/2609.07747)
- [Translation as a Bridging Action: Transferring Manipulation Skills from Humans to Robots](https://arxiv.org/abs/2606.28133)
- [What Matters When Cotraining Robot Manipulation Policies on Everyday Human Videos?](https://arxiv.org/abs/2606.06627)
- [Do as I Do: Dexterous Manipulation Data from Everyday Human Videos](https://arxiv.org/abs/2606.19333)
- [EgoRecovery: Acquiring Failure Recovery Ability Through Human Recovery Demonstration](https://arxiv.org/abs/2607.19745)
- [HoMMI: Learning Whole-Body Mobile Manipulation from Human Demonstrations](https://arxiv.org/abs/2603.03243)
- [Video2Sim2Real: Full-Stack Autonomous Dexterous Skill Acquisition from a Single Human Video](https://arxiv.org/abs/2606.08828)
- [Towards Human-level Dexterous Teleoperation (TELEDEXTER)](https://arxiv.org/abs/2607.11481)
- [EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos](https://arxiv.org/abs/2507.12440)
- [Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations](https://arxiv.org/abs/2606.10614)
- [EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data](https://arxiv.org/abs/2602.16710)
- [EgoAERO: Learning Dexterous Manipulation from a Single Egocentric Video without Object Assets](https://arxiv.org/abs/2606.08057)
- [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485)
- [Track2Act: Predicting Point Tracks from Internet Videos enables Generalizable Robot Manipulation](https://arxiv.org/abs/2405.01527)
- [ImMimic: Cross-Domain Imitation from Human Videos via Mapping and Interpolation](https://arxiv.org/abs/2509.10952)
- [Developing Vision-Language-Action Model from Egocentric Videos (EgoScaler)](https://arxiv.org/abs/2509.21986)
- [EgoBridge: Domain Adaptation for Generalizable Imitation from Egocentric Human Data](https://arxiv.org/abs/2509.19626)
- [RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning](https://arxiv.org/abs/2606.06033)
- [DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation](https://arxiv.org/abs/2505.21864)
- [DexDirect: Direct Kinesthetic Arm Guidance for Efficient Dexterous Demonstration Collection](https://arxiv.org/abs/2607.27784)
- [ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations](https://arxiv.org/abs/2510.01607)
- [HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone](https://arxiv.org/abs/2607.25895)
- [EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations](https://arxiv.org/abs/2511.00153)
- [Phantom: Training Robots Without Robots Using Only Human Videos](https://arxiv.org/abs/2503.00779)
- [Masquerade: Learning from In-the-wild Human Videos using Data-Editing](https://arxiv.org/abs/2508.09976)
- [World In Your Hands: A Large-Scale and Open-source Ecosystem for Learning Human-centric Manipulation in the Wild](https://arxiv.org/abs/2512.24310)
