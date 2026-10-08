# 鱼眼与全景光学在具身智能中的近一年应用：收益分层、机制性代价与表示空间适配

## 研究边界

本备忘录回答一个问题：**2025 年 9 月至 2026 年 9 月，鱼眼镜头（以及作为其延伸的环视多鱼眼、双鱼眼拼接、360° 全景成像）在具身智能与机器人领域被如何使用，收益与代价的边界在哪里？**

证据基础为 51 篇经过全文精读与主张验证的 arXiv 论文，覆盖六个维度：直接应用（鱼眼 SLAM/里程计、腕装鱼眼数据采集）、机制（畸变建模与投影适配）、限制（深度退化、像素压缩、标定脆弱）、评测（环视鱼眼检测/占据/跟踪基准）、部署（嵌入式实时性、人形与四足平台）、邻接（常规相机的视角稳健性路线，作为对照）。证据分布为 support 436 条、conditional 91 条、limit 185 条、gap 34 条——负面与条件性证据合计超过三分之一，这决定了本备忘录的基调：宽视场的收益是真实的，但每一条收益都有可复述的失效条件。

本 run 无法确立的内容同样需要声明：多数闭环证据来自仿真或小样本真机（常见 15-20 次试验、无显著性检验）；部分系统不披露鱼眼 FoV 与畸变模型，光学层横向比较不可行；"全景优于窄视场"的若干对比缺少同等预算的多相机或全景相机基线，归因不完全干净。

## 中心判断

近一年的证据合起来支持一个可证伪的判断：**鱼眼光学在具身领域完成了从"感知外设"到"数据接口与策略输入"的角色升级——UMI 系数据采集把腕装鱼眼固化为事实标准，人形与移动操作把头装全景固化为全局上下文通道——但其收益严格分层：任务关键信息位于针孔视锥之外时收益最大（视野外操作从 0/20 到可用），信息在视锥内时收益趋零，动态物体密集时甚至为负；与此同时，宽视场的代价（像素压缩、深度退化、预训练域差、标定脆弱）是光学与几何层面的，不能靠工程优化消除。方法学的主轴因此从"图像空间矫正"转向"表示空间适配"——位置编码、校准 token、球面特征——用万级参数把透视预训练模型调回鱼眼域，这是本年度最清晰的增量。**

## 收益按"信息是否在视锥外"分层

宽 FoV 的收益不是均匀的，证据呈现清晰的单调结构。

**第一层：任务信息在视锥外，收益从无到有。** 人形操作系统 OmniDP 的四个视野外（beyond-FOV）任务上，三个窄视场相机基线全部 0/20 失败——不是精度差，是感知覆盖为零；OmniDP 借头装全景 LiDAR 达到 12/20、11/20、16/20 的可用水平，六任务总计 82/120 对基线最高的 25/120（[OmniDP](https://arxiv.org/abs/2603.05355)）。避碰实验更直接：物理障碍被刻意放在头装 RGB-D 相机视野之外，三个相机基线任务成功 0/20、碰撞 18-20/20，OmniDP 成功 14/20、碰撞 5/20。消融里移除全景输入，Hand Over 从 12/20 跌到 0/20。移动双臂平台上的 PanoVLA 同构：目标在机器人身后或两侧的长程任务中，仅用局部视角的 π0.5 端到端成功率 30.0%，接入顶装 360° 全景专家后 73.4%；分阶段看，"归还抹布"这类跨阶段重定位阶段，raw panorama 基线仅 26.7% 试验完成，全景专家 73.3%（[PanoVLA](https://arxiv.org/abs/2608.02257)）。

**第二层：信息在视锥内，收益压缩到噪声级。** PanoVLA 自己报告：在以单目标定位与短程抓放为主的 Move Pen 任务上，把 ERP 全景直接塞给 π0.5 的朴素基线与专门设计的 PanoVLA 成绩持平（SCR/SR 均 95.6%/86.7%）——全景信息冗余时，显式全景建模的边际收益消失。相机选型实证研究给出同一结论的另一面：腕装单鱼眼在六个操作任务上的平均成功率（特征贫乏背景 0.57、丰富背景 0.66）显著高于腕装单针孔（0.31/0.34），甚至高于双针孔（0.38/0.45）——但把背景从特征贫乏换到特征丰富，鱼眼的归一化得分增益 +0.39，针孔 +0.18，说明鱼眼的定位收益以环境视觉复杂度为条件（[Rethinking Camera Choice](https://arxiv.org/abs/2603.02139)）。该研究同时给出本年度最实用的正面数字：仅 8 个训练背景场景，鱼眼策略在完全未见场景上的零样本成功率即超过 95%——宽视场让策略"不得不"学习场景不变特征。

**第三层：宽视场纳入有害信息时，收益为负。** 单目 360° 里程计 360DVO 在其 Hard-06 拥挤桥面序列上被针孔方法反超：针孔裁切主要包含静态桥体结构，全景图像却纳入大量动态物体、拖累特征匹配（[360DVO](https://arxiv.org/abs/2601.02309)）。这是"宽 FoV 恒优"直觉的直接反例。

SLAM 一侧的分层数字同样干净。多鱼眼 LiDAR-视觉-惯性系统 Multi-LVI-SAM 在无纹理楼梯间（Newer College Stairs）与动态室内（M2DGR room 序列）中，FAST-LIO2、FAST-LIVO2、LVI-SAM 等单目或单传感器基线全部失效，四鱼眼融合取得 0.135/0.127 m RMSE；Hilti'2022 消融中没有任何单相机配置通过全部测试，全配置加外参补偿后全部通过且精度最优（[Multi-LVI-SAM](https://arxiv.org/abs/2509.05740)）。反过来，现成单目 LVIO 直接吃鱼眼数据会双重受损——LVI-SAM 的归一化平面后端用不上宽 FoV，鱼眼外围畸变又造成视觉-LiDAR 点云错位，在 Newer College 全部 8 条序列失效。这是"感知覆盖换鲁棒性"的最纯粹表述：相机数从一增到四，处理时间只增至 2.15 倍（[Multi-LVI-SAM](https://arxiv.org/abs/2509.05740)）。

## 代价是光学级的，不是工程级的

宽视场的四类代价在近一年被定量钉死，且都被证明源于成像几何本身。

**像素压缩不可逆。** 非线性投影把广角场景压进有限图像区域：鱼眼视图里物体的像素面积仅约为针孔对应物的 15%，且该信息熵损失发生在成像期、无法靠矫正恢复。把针孔 3D 检测器（BEVDet、PETR）经透视或柱面矫正迁移到鱼眼数据，FDS 仍下降超过 12 点（[Fisheye3DOD](https://arxiv.org/abs/2511.18695)）。作者承认的天花板很诚实：针孔图像给物体近十倍有效像素面积，期待鱼眼检测器达到可比精度"不现实"。

**深度估计系统性退化。** 鱼眼深度基准 WideDepth 测得：单目度量深度模型随 FoV 从 120° 扩到 195°，DepthAnythingV2 的 AbsRel 恶化 166%、δ1.25 跌 86.8%；最稳的 DepthPro 也 +9.0%/−4.1%；深度补全模型受影响小得多（NLSPN 仅 +5.92%），但所有补全模型在 AbsRel 上仍显著退化（[WideDepth](https://arxiv.org/abs/2605.24074)）。同基准还发现一个对部署很关键的错位：尽管动机强调操作需要亚厘米近场精度，基准深度分布 2-5m 占 74.7%、0-1m 仅 6.9%——"鱼眼深度支撑近场操作"的量化依据目前最薄弱。

**预训练域差是分布级的。** 在透视图像上训练的模型带着针孔归纳偏置（卷积平移不变性、位置编码的线性采样假设）：鱼眼变换使 5 个通用与机器人专用 VLM 在 4 个空间推理基准上一致退化（平均绝对降 4.0 点）；从标准视图训练切换到腕装鱼眼训练，π0.5 在 RoboTwin 上从 82.0% 降到 59.4%（[VISTA](https://arxiv.org/abs/2606.04708)）。全景侧更严重：透视范式直迁 360° 等距柱状输入发生"灾难性的空间推理崩溃"（[PanoAffordanceNet](https://arxiv.org/abs/2603.09760)），通用 MLLM 直读 ERP 的能力在观察者中心推理上整体偏弱（[PanoWorld](https://arxiv.org/abs/2605.13169)）。领域综述把这总结为双瓶颈：模型无法理解畸变特性 + 畸变使针孔标注工具失效、人工标注成本更高，二者共同拖慢数据集规模（[PANORAMA](https://arxiv.org/abs/2509.12989)）。

**标定在超广角区间结构性脆弱。** 受控实验中多鱼眼标定失败率随 FoV 骤增：180° 时 0-3%，220° 时 36-67%，240° 时 59-88%（[CO-Calib](https://arxiv.org/abs/2607.05777)）。更反直觉的是，把检测到的标靶点替换为完整真值观测后成功率反而从 68.1% 降到 53.7%——失败不能归咎于检测召回，而是底层优化在极端 FoV 下本身不稳定。占据预测一侧，OneOcc 在 5% 联合内外参噪声下 mIoU 从 32.23 跌到 16.75、近乎减半（[OneOcc](https://arxiv.org/abs/2511.03571)）。

计算代价则是可控但不为零：多鱼眼全景化每帧 2.15 倍单相机耗时（[Multi-LVI-SAM](https://arxiv.org/abs/2509.05740)）；全景反馈式跟踪管线只有纯检测器基线 1/4 到 1/5 的帧率（[OmniTrack++](https://arxiv.org/abs/2511.00510)）；360DVO 默认配置在 Jetson Orin 上 2 FPS，降到 1/4 分辨率换 17 FPS 但 ATE 恶化 21.6%（[360DVO](https://arxiv.org/abs/2601.02309)）。

## 适配路线：从图像空间转向表示空间

既然矫正既丢 FoV 又不能恢复信息，近一年的方法学增量集中在"让模型适配几何，而不是让图像适配模型"，形成三条各有硬边界的路线。

**路线一：原生几何建模。** 把畸变吸收进模型结构——FishRoPE 把位置编码换成极坐标 (θ,φ) 的投影式旋转位置编码，在同一冻结 DINOv2-B 下把 WoodScape 鱼眼检测从 2D RoPE 的 52.5 mAP 提到 54.2，BEV 分割 61.4 到 65.1 mIoU，且冻结骨干加 12.4M 可训练参数超过 29M 常规训练的 Swin-T（[FishRoPE](https://arxiv.org/abs/2604.10391)）。检测侧的 FisheyeBEVDet/FisheyePETR 在特征层做球面等距柱面建模，相对透视矫正基线 FDS 提升 4.5/6.2 点（[Fisheye3DOD](https://arxiv.org/abs/2511.18695)）。3D 重建侧，DirectFisheye-GS 直接消费原生鱼眼输入并用跨视图联合优化处理边缘漂浮物，绕开"先去畸变再训练"的黑边与插值伪影（[DirectFisheye-GS](https://arxiv.org/abs/2604.00648)）。SLAM 侧，Sphere-VIO 用统一球面表示吃异构多相机（[Sphere-VIO](https://arxiv.org/abs/2606.29910)），球面前端 USF 证明零样本跨镜头迁移时球面 DeepLab 比平面模型 mIoU 高 16.05 点（[USF](https://arxiv.org/abs/2511.18174)）。**硬边界：球面化以无旋转条件下的峰值精度为代价**——球面 YOLOv11 的 mAP@10 比平面版低约 10.1 点，三个分割骨干低 4-7.6 点；且向小 FoV 镜头反向迁移时平面模型更优（[USF](https://arxiv.org/abs/2511.18174)）。Sphere-VIO 也承认其在针孔基准 EuRoC 上落后 SchurVINS 与 ORB-SLAM3——球面 bearing 残差是为宽 FoV 多相机而非针孔场景最优（[Sphere-VIO](https://arxiv.org/abs/2606.29910)）。

**路线二：投影桥接。** 把鱼眼/全景重投影到预训练模型认识的中间表示：OneCanvas 把全景重投影成 BEV 式画布喂给 VLM，畸变被投影几何吸收（[OneCanvas](https://arxiv.org/abs/2606.19253)）；PanoVLA 的编码管线先把双目鱼眼球面重投影成 ERP 再走全景基础模型 MTPano（[PanoVLA](https://arxiv.org/abs/2608.02257)）；超低空 UAV 平台把多鱼眼分成扇区自适应分发（[多鱼眼 UAV 平台](https://arxiv.org/abs/2609.02319)）。**硬边界：透视裁剪（Center-PH）保深度但丢 FoV**——RayTun3R 把它的旋转误差从 3.27° 修到 1.11°，正说明裁剪丢掉的外围信息需要二次补救（[RayTun3R](https://arxiv.org/abs/2607.02711)）。

**路线三：表示空间轻量适配（本年度最清晰的增量）。** 冻结透视预训练主干，只改与几何绑定的少量组件：Fisheye3R 向 transformer 层插入可学习校准 token，在潜空间对齐鱼眼与透视特征——344,064 个可训练参数（LoRA r=32 需要其 24 倍），推理速度与显存完全不变，135 项跨模型跨数据集测试中仅用无标注透视数据的自监督方案即有 26 项提升超 50%，加鱼眼标注后达 77 项；KITTI360 上 MapAnything 位姿 AUC 从 0.428 修复到 0.917（[Fisheye3R](https://arxiv.org/abs/2603.28896)）。RayTun3R 更进一步把失配定位到位置编码：测量 DA3 预训练绝对位置编码的局部 Jacobian，发现它关于归一化半径几乎平坦——与针孔的位置无关结构一致；仅学习 10,752 个参数的 PE/RoPE 残差修正，就把 110°-200° 鱼眼数据集上的旋转误差降低 2-12 倍，零推理开销（[RayTun3R](https://arxiv.org/abs/2607.02711)）。数据侧的对应物是 VISTA：几何 warp 无法合成 180° 对角视锥之外的可信内容，改用扩散模型做语义感知的透视→鱼眼翻译，配合 8M 问答对的鱼眼域 VQA 协同训练——鱼眼域 VQA 把三任务成功率从 45.0% 提到 55.0%，而标准视图 VQA 反而压到 31.7%，辅助监督的视角域必须与动作观测域匹配（[VISTA](https://arxiv.org/abs/2606.04708)）。

**硬边界：合成畸变训练不足以弥合真实域差。** 户外 KITTI360 上，纯合成畸变的自监督方案把位姿 AUC 从 0.428 提到 0.540，含真实鱼眼数据的方案达 0.917（[Fisheye3R](https://arxiv.org/abs/2603.28896)）。本文推断：三条路线不是竞争关系而是栈式关系——投影桥接解决"喂进去"，令牌/编码适配解决"对得齐"，原生几何建模解决"学得好"，当前最经济的组合是前两者加少量真实鱼眼数据。

## 位置分工：腕装鱼眼做接口，头装全景做上下文，主动视角做兜底

近一年最产业化的变化是 UMI 生态把腕装鱼眼固化为**数据接口标准**：exUMI 保留腕装 GoPro 鱼眼并把相机前移以消除采集者身体遮挡，用 AR MoCap 加磁编码器替换视觉 SLAM 后数据处理成功率从不到 60% 升到接近 100%——替换的原因之一正是 ArUco 标记受鱼眼畸变影响贡献约 10% 预处理失败（[exUMI](https://arxiv.org/abs/2509.14688)）；FastUMI-100K 用同一接口规模化到十万级演示（[FastUMI-100K](https://arxiv.org/abs/2510.08022)）；HiFi-UMI 把每手升级为两个非平行鱼眼、约 200° 覆盖，微秒级 GPIO 同步，端到端 3mm 末端精度，并在三个 backbone 上证明零机器人 post-training 与同域遥操作匹配（差异 -2.5/+3.1/-0.6 个百分点，均在采样噪声内）、3,200 条演示后 Remote Insertion 饱和于 85%（[HiFi-UMI](https://arxiv.org/abs/2607.25895)）。

但腕装鱼眼-only 的脆弱性同年被钉死：同任务换新环境，仅双鱼眼腕相机的 UMI 配置成功率从 26% 跌到 6%（四个任务中三个 0%），固定头相机 16%，带主动移动第三视角的 ActiveUMI 保持 56%（[ActiveUMI](https://arxiv.org/abs/2510.01607)）。其结论已成本领域常用语：learning how to look 与 learning what to do 同等重要——腕装视角受操作需求而非感知目标约束，人类靠移动头部管理遮挡。主动感知路线的极端形式是机器人眼球 EyeVLA：固定相机（无论多宽）无法兼顾宽域覆盖与细粒度细节，读药瓶小字这类任务需要主动变焦（[EyeVLA](https://arxiv.org/abs/2511.15279)）。这构成对"宽 FoV 万能论"的机制性反驳：鱼眼解决的是覆盖问题，不解决分辨率问题——两者在像素预算下此消彼长。

头装/体装全景的分工由 OmniDP 与 PanoVLA 界定，但注意归因边界：OmniDP 的全景输入是头装 LiDAR 点云而非相机，其全部对比中没有全景相机基线——"全景 LiDAR 优于全景相机"未被检验（[OmniDP](https://arxiv.org/abs/2603.05355)）；四足与人形占据预测侧，全景相机-only 路线在含 LiDAR 配置面前明显偏弱（纯相机 5.53 mIoU，加 LiDAR 跳到 22.87，[VoxelHound](https://arxiv.org/abs/2603.13108)），单全景相机的 OneOcc 定位为导航与落脚点尺度、明确不覆盖精细接触（[OneOcc](https://arxiv.org/abs/2511.03571)）。内窥镜手术侧，PERSEUS 把鱼眼内窥镜的实时重建与语义结合用于气道与前列腺手术自动化，管线全程在针孔模型空间运行、不依赖深度相机（[PERSEUS](https://arxiv.org/abs/2509.13541)）。

对照路线也值得一提：不换镜头而修视角——视角规范化器把任意相机观测重投影到训练视角（[GS-VLA](https://arxiv.org/abs/2608.19066)）、跨视角动作一致性约束（[Cross-View Action Consistency](https://arxiv.org/abs/2608.06965)）、多视角混训加上下文系统辨识（[ICWM](https://arxiv.org/abs/2606.26025)）。这些工作全部以针孔或外参级变化为前提，鱼眼径向畸变不在其验证范围（GS-VLA 作者明确声明）。本文推断：它们与鱼眼路线解决的是同一痛点（相机配置漂移）的不同侧面——前者应对"同款镜头换了位置"，后者应对"镜头本身换了光学"，真实部署中两者叠加。

## 条件与分歧

中心判断在以下条件下减弱或需要限定：

- **剧烈运动与动态物体**：Multi-LVI-SAM 自认 Hard 序列中 LiDAR 子系统退化连带视觉；360DVO 的桥面反例。宽 FoV 不提供运动鲁棒性。
- **光照极端**：Hilti'2022 的强曝光与极暗楼梯间对视觉方法整体构成挑战；OneOcc 的全景相机方案在夜间落后 LiDAR 基线。
- **玻璃/透明材质**：Multi-LVI-SAM 在玻璃幕墙序列 RMSE 仍近 1m；WideDepth 把透明与反射表面直接掩码——高频困难场景在基准里系统性缺席。
- **证据质量**：Fisheye3DOD 全部鱼眼证据是 CARLA 合成（Kannala-Brandt 数学生成），向真实鱼眼硬件外推未经检验；GS-VLA 全仿真；OmniDP 与 PanoVLA 的 20/15 次试验协议无种子与方差报告，1-3 次成功的差距不可判定。
- **规格披露缺口**：FastUMI-100K 与 BifrostUMI 未披露 FoV、畸变模型与预处理流程，"策略消费的是原始畸变图还是校正图"无法判断——UMI 生态内部的光学层横向比较目前不可行。

## 可操作框架

| 部署场景 | 推荐光学配置 | 依据 | 已知边界 |
|---|---|---|---|
| 视野外目标操作 / 长程多阶段任务 | 头装全景（LiDAR 或相机+专家编码） | OmniDP 0/20→12-16/20；PanoVLA 30.0%→73.4% | 全景相机 vs 全景 LiDAR 优劣未对照 |
| 腕装操作确认 / 数据采集接口 | 单鱼眼 ≥155°，双非平行更优 | 相机选型研究 0.57 vs 0.31；HiFi-UMI 3mm/98% | 腕-only 对分布偏移最脆弱（26%→6%） |
| 无纹理/几何重复环境定位 | 多鱼眼+LiDAR 紧耦合 | Multi-LVI-SAM 楼梯间全基线失效 | 剧烈运动、玻璃幕墙仍受限 |
| 近场低速感知（泊车/仓储/配送） | 环视鱼眼 | Fisheye3DOD 近场 FDS 与针孔中距相当 | 远距与密集遮挡下降幅更大 |
| 度量深度关键任务 | 鱼眼+立体/补全，勿用单目直推 | WideDepth：单目 AbsRel +166% | 0-1m 近场证据密度最薄 |
| 透视预训练模型迁移 | 校准 token / PE 残差（万级参数） | Fisheye3R 344K 参数零开销；RayTun3R 2-12× | 真实域差仍需少量真实鱼眼数据 |

## 研究空白与下一步

文献自declare的空白与本次 run 覆盖缺口的区分如下。文献侧：(1) 完全同步的多传感器全景采集（RGB+LiDAR+音频+行为轨迹）仍然罕见，推理导向的全景评测刚起步（[PANORAMA](https://arxiv.org/abs/2509.12989)）；(2) 环视鱼眼 3D 检测在 Fisheye3DOD 之前是空白、其 4D 占据跟踪随后由 OccTrack360 补上，但后者受显存限制只兑现了一半评测范围（[OccTrack360](https://arxiv.org/abs/2603.08521)）；(3) 动态畸变的时序一致性、把全景特征整合进控制策略的"行动感知表示"被多篇明确列为开放问题。run 覆盖侧：本 run 的邻接维度以常规相机视角稳健性工作为主，未覆盖折反射（catadioptric）与事件相机鱼眼的专门文献；内窥镜与 UAV 只各有单篇代表作，子领域结论不宜外推。

对项目的启发按优先级：第一，若下游是 VLA/操作策略，鱼眼观测进入前的域适配（VQA 协同训练或校准 token）应被视为必选组件而非锦上添花——标准视图辅助监督会主动伤害策略（-13.3 个百分点）。第二，腕装鱼眼数据接口可以放心沿用（HiFi-UMI 已验证零机器人 post-training 可行），但部署侧必须补一条非腕装视觉通道。第三，任何"全景方案更好"的采购或立项论证，先核对对比里有没有同等预算的多相机或全景相机基线——本年度多个高影响结果缺这一格。

## 结论

近一年，鱼眼与全景光学在具身领域完成了角色升级：腕装鱼眼成为 UMI 系数据事实标准，头装全景成为人形与移动操作的全局上下文通道，环视鱼眼补上了 3D 检测与 4D 占据的基准空白。收益分层结构（视锥外从无到有、视锥内趋零、动态密集为负）与代价的光学级本质（像素压缩、深度退化、标定脆弱）同时被定量确立，方法学因此从图像空间矫正转向表示空间适配——位置编码残差与校准 token 以万级参数、零推理开销把透视预训练模型调回鱼眼域，是本年度最清晰的技术增量。下一年的看点不在更宽的镜头，而在真实鱼眼数据闭环（合成域差未弥合）、全景相机与全景 LiDAR 的受控对照、以及把"看得宽"变成"动得好"的行动感知表示。

## References

1. [Multi-LVI-SAM: A Robust LiDAR-Visual-Inertial Odometry for Multiple Fisheye Cameras](https://arxiv.org/abs/2509.05740) — 多鱼眼 LVIO，球面全景特征模型与外参补偿。
2. [PANORAMA: The Rise of Omnidirectional Vision in the Embodied AI Era](https://arxiv.org/abs/2509.12989) — 全向视觉领域综述，模型与数据双瓶颈、六阶段路线图。
3. [PERSEUS: Perception with Semantic Endoscopic Understanding and SLAM](https://arxiv.org/abs/2509.13541) — 鱼眼内窥镜实时重建与手术场景理解。
4. [exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation](https://arxiv.org/abs/2509.14688) — 腕装鱼眼+触觉的教学系统，AR MoCap 替换视觉 SLAM。
5. [Omni-LIVO: Robust RGB-Colored Multi-Camera Visual-Inertial-LiDAR Odometry](https://arxiv.org/abs/2509.15673) — 多相机环视 LIVO，拼接路线而非鱼眼单机光学。
6. [ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations](https://arxiv.org/abs/2510.01607) — 主动视角数据采集，腕-only 脆弱性的定量证据。
7. [FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset](https://arxiv.org/abs/2510.08022) — 十万级 UMI 式鱼眼数据集。
8. [OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback](https://arxiv.org/abs/2511.00510) — 环视多目标跟踪，双鱼眼拼接基准。
9. [OneOcc: Semantic Occupancy Prediction for Legged Robots with a Single Panoramic Camera](https://arxiv.org/abs/2511.03571) — 单全景相机腿式占据预测。
10. [Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception](https://arxiv.org/abs/2511.15279) — 机器人眼球与主动变焦感知。
11. [Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera](https://arxiv.org/abs/2511.18174) — 镜头无关球面前端，旋转等变与精度代价。
12. [Exploring Surround-View Fisheye Camera 3D Object Detection](https://arxiv.org/abs/2511.18695) — 环视鱼眼 3D 检测基准与像素压缩机制。
13. [360DVO: Deep Visual Odometry for Monocular 360-Degree Camera](https://arxiv.org/abs/2601.02309) — 单目全景深度里程计，动态物体反例与嵌入式代价。
14. [Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation](https://arxiv.org/abs/2603.02139) — 鱼眼 vs 针孔腕装操作实证。
15. [OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception](https://arxiv.org/abs/2603.05355) — 头装全景 LiDAR 的人形视野外操作。
16. [AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models](https://arxiv.org/abs/2603.05868) — 新视角合成式相机适配。
17. [RePer-360: Releasing Perspective Priors for 360° Depth Estimation via Self-Modulation](https://arxiv.org/abs/2603.05999) — 全景深度估计的自调制去透视先验。
18. [OccTrack360: 4D Panoptic Occupancy Tracking from Surround-View Fisheye Cameras](https://arxiv.org/abs/2603.08521) — 环视鱼眼 4D 占据跟踪基准。
19. [PanoAffordanceNet: Towards Holistic Affordance Grounding in 360° Indoor Environments](https://arxiv.org/abs/2603.09760) — 360° 可供性接地。
20. [Panoramic Multimodal Semantic Occupancy Prediction for Quadruped Robots](https://arxiv.org/abs/2603.13108) — 四足多模态全景占据（VoxelHound）。
21. [Panoramic Affordance Prediction](https://arxiv.org/abs/2603.15558) — 免训练全景可供性预测。
22. [OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation](https://arxiv.org/abs/2603.17351) — 全景 3D 感知与 token 高效导航推理。
23. [Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses](https://arxiv.org/abs/2603.28896) — 校准 token 的潜空间鱼眼适配。
24. [Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning](https://arxiv.org/abs/2604.00557) — 常规多相机视角扩展（对照路线）。
25. [DirectFisheye-GS: Enabling Native Fisheye Input in Gaussian Splatting](https://arxiv.org/abs/2604.00648) — 原生鱼眼高斯泼溅。
26. [PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset](https://arxiv.org/abs/2604.00852) — 双鱼眼拼接 UAV SLAM 与数据集。
27. [FishRoPE: Projective Rotary Position Embeddings for Omnidirectional Visual Perception](https://arxiv.org/abs/2604.10391) — 投影式旋转位置编码。
28. [RobotPan: A 360° Surround-View Robotic Vision System for Embodied Perception](https://arxiv.org/abs/2604.13476) — 环视重建系统。
29. [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089) — UMI 的 3D 扩展与 LiDAR 融合。
30. [BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation](https://arxiv.org/abs/2605.03452) — 腕装鱼眼到人形全身技能。
31. [PanoWorld: Towards Spatial Supersensing in 360° Panorama World](https://arxiv.org/abs/2605.13169) — 全景空间推理基准。
32. [WideDepth: Millimeter-Accurate Benchmark for Fisheye Depth Estimation](https://arxiv.org/abs/2605.24074) — 室内鱼眼深度基准与退化量化。
33. [VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training](https://arxiv.org/abs/2606.04708) — 鱼眼域适配与物理验证数据管线。
34. [OneCanvas: 3D Scene Understanding via Panoramic Reprojection](https://arxiv.org/abs/2606.19253) — 全景重投影画布。
35. [One Demo is Worth a Thousand Trajectories: Action-View Augmentation for Visuomotor Policies](https://arxiv.org/abs/2606.19586) — 鱼眼 eye-in-hand 视角增广。
36. [Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI](https://arxiv.org/abs/2606.22971) — 人形环视双目占据数据集。
37. [In-Context World Modeling for Robotic Control](https://arxiv.org/abs/2606.26025) — 上下文系统辨识应对相机配置漂移（对照路线）。
38. [Sphere-VIO: Fast and Robust Visual-Inertial Odometry via Unified Spherical Representation for Heterogeneous Multi-Camera Systems](https://arxiv.org/abs/2606.29910) — 异构多相机球面统一 VIO。
39. [RayTun3R: Online Camera Adaptation in 3D Foundation Models](https://arxiv.org/abs/2607.02711) — 位置编码残差适配与针孔偏置定位。
40. [Observation Quality Matters: Robust Multi-Fisheye Calibration via Failure-Oriented Analysis](https://arxiv.org/abs/2607.05777) — 多鱼眼标定失败机制分析（CO-Calib）。
41. [X-Lens: Real-Time Metric Depth Estimation with Heterogeneous Cameras](https://arxiv.org/abs/2607.12993) — 异构相机度量深度。
42. [HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone](https://arxiv.org/abs/2607.25895) — 高保真双鱼眼 UMI 与零机器人 post-training。
43. [Learning Panorama-Aware VLA for Mobile Manipulation with Whole-Body Teleoperation](https://arxiv.org/abs/2608.02257) — 全景专家 VLA（PanoVLA）。
44. [Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies](https://arxiv.org/abs/2608.06965) — 跨视角动作一致性（对照路线）。
45. [HUI360: A 360° Egocentric Dataset and Baselines for Human-Robot Interaction Anticipation](https://arxiv.org/abs/2608.11051) — 全景 ego HRI 数据集。
46. [GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting](https://arxiv.org/abs/2608.19066) — 视角规范化（对照路线，针孔前提）。
47. [Selective Cross-View Consistency for World Action Models](https://arxiv.org/abs/2608.21402) — 选择性跨视角一致性（对照路线）。
48. [One Policy, Many Embodiments: Unified Camera-Centric Action Geometry Pre-training](https://arxiv.org/abs/2608.26058) — 相机中心动作几何预训练。
49. [From Multi-Fisheye Sensing to Panoramic Perception: A Parallax-Aware Onboard Platform for Ultra-Low-Altitude UAVs](https://arxiv.org/abs/2609.02319) — 多鱼眼 UAV 全景平台。
50. [Spheriverse: 3D Scene Understanding from Spherical Observations in the Wild](https://arxiv.org/abs/2609.09012) — 球面观测 3D 场景理解基准（SphereOcc）。
