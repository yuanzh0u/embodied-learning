# Literature Evidence Brief

- Generated: 2026-07-08T08:39:18.729192+00:00
- Evidence events: 6
- Stance counts: {'conditional': 1, 'limit': 2, 'support': 3}

## Claim Map

| Topic | Stance | Claim | Evidence | Paper | Authors |
|---|---|---|---|---|---|
| EA-DATA | limit | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | 论文指出大规模机器人示教池常含轨迹冗余、噪声示教、次优行为和任务覆盖不均；SIEVE 按可复用 primitive 与 transition 选择中心、稳定、适合模仿的轨迹，在多数据集和 VLA 模型上可用 50% 示教与 50% 训练步数超过全量训练。 (Abstract; Introduction; SIEVE; Conclusion) | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | changti-wu [unlisted], bin-yu [unlisted], zhaolong-shen [unlisted], shijie-lian [unlisted], xiaopeng-lin [unlisted], cong-huang [unlisted], zhirui-zhang [unlisted], lei-zhang [unlisted], kai-chen [unlisted] |
| EA-DATA | support | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | 论文将 2D VLA 的困难归因于几何理解和空间推理不足、3D 数据和强 3D encoder 稀缺、跨模态 lifting/projection 损失几何 fidelity；其 GC-MAE 用伪点云监督当前点云重建和未来几何演化，并在仿真与真实任务中提升成功率。 (Abstract; I Introduction; IV-C Geometry-Centric Masked Autoencoding; V-B Multi-Task on MetaWorld and RLBench) | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | jiaming-liu [unlisted], qingpo-wuwu [unlisted], nuowei-han [unlisted], hao-chen [unlisted], zhuoyang-liu [unlisted], fan-fei [unlisted], yueru-jia [unlisted], chenyang-gu [unlisted], yandong-guo [unlisted], boxin-shi [unlisted], shanghang-zhang [unlisted] |
| EA-DATA | conditional | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | 论文认为物理遥操作把每条示教绑定到操作者、硬件和固定 workspace，难覆盖长尾交互；RynnWorld-Teleop 用动作条件世界模型从手姿流生成机器人中心视频和可 retarget 的动作标签，作为模仿学习数据。但作者也列出细粒度液体/高形变物体和 per-platform fine-tuning 等限制。 (Abstract; 1 Introduction; 4 RynnWorld-Teleop as a Digital Teleoperation System; 6 Conclusion) | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | haoyu-zhao [unlisted], xingyue-zhao [unlisted], hangyu-li [unlisted], biao-gong [unlisted], kehan-li [unlisted], siteng-huang [unlisted], xin-li [unlisted], deli-zhao [unlisted], zhongyu-li [unlisted] |
| EA-EVAL | support | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | 论文指出真实机器人策略评估受硬件和人工监督限制，是基础模型迭代瓶颈；WMBench 用真实 teleoperation 数据和匹配 policy rollouts 构造评估，并分析 7 个视频世界模型、4 种动作表示和 324,000 余次模拟 rollout。其结论强调 evaluator 质量由长程 action-faithful rollout consistency、可迁移物理先验、动作编码、记忆和评估导向 post-training 共同决定。 (Abstract; 1 Introduction; 4.2 Evaluation Protocol; 5.2 How Do Pretraining and Training Data Matter?; 7 Discussion and Conclusion) | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | gigaworld-team [unlisted], angyuan-ma [unlisted], boyuan-wang [unlisted], bohan-li [unlisted], chaojun-ni [unlisted], guo-li [unlisted], guan-huang [unlisted], guosheng-zhao [unlisted], hao-li [unlisted], hengtao-li [unlisted], jingyu-liu [unlisted], jiwen-lu [unlisted], qiuping-deng [unlisted], tingdong-yu [unlisted], xuancheng-xu [unlisted], xinyu-zhou [unlisted], xiuwei-xu [unlisted], xinze-chen [unlisted], xiaofeng-wang [unlisted], xiaoyu-tian [unlisted], yang-wang [unlisted], yifan-chang [unlisted], yukun-zhou [unlisted], yun-ye [unlisted], zhenyu-wu [unlisted], zhanqian-wu [unlisted], zheng-zhu [unlisted] |
| EA-SENSOR | support | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | 论文认为形变物体有高维状态和复杂材料属性，接触诱发的局部形变常被末端执行器或物体遮挡；已有数据集常缺对象多样性、依赖合成数据，或缺高保真标注与接触形变。Deform360 采集 198 个日常物体、1,980 个交互序列、215 小时以上数据、41 个环视相机和双臂触觉 UMI gripper，并用 markerless 3D tracking 提取稠密几何与运动。 (Abstract; 1 Introduction; 2 Related Work; 5 Experiments; 7 Conclusion) | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | hongyu-li [unlisted], wanjia-fu [unlisted], xiaoyan-cong [unlisted], zekun-li [unlisted], binghao-huang [unlisted], hanxiao-jiang [unlisted], xintong-he [unlisted], yiqing-liang [unlisted], rao-fu [unlisted], tao-lu [unlisted], srinath-sridhar [unlisted], kevin-a-smith [unlisted], george-konidaris [unlisted], yunzhu-li [unlisted] |
| EA-SENSOR | limit | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | 论文指出 VLA 在接触丰富任务中会因轻微接触扰动产生不可恢复失败，这些失败难以从视觉单独检测；TACO 用 tactile-aware world model 将真实 rollout 中的失败邻近状态转成想象的视触觉纠正片段和可执行纠正动作，在真实接触任务中相对 base policy 提升 44 个百分点成功率。 (Abstract; 1 Introduction; 2 Related Work; 3 Method; 5 Conclusion and Limitations) | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | shengbang-liu [unlisted], yueru-jia [unlisted], yuyang-yan [unlisted], jiaming-liu [unlisted], xinran-zhang [unlisted], qiuxuan-feng [unlisted], yandong-guo [unlisted], shiji-zhou [unlisted], boxin-shi [unlisted], shanghang-zhang [unlisted] |

## Author Stance Events

| Author key | Institutions | Paper | Date | Claim | Stance |
|---|---|---|---|---|---|
| changti-wu | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| bin-yu | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| zhaolong-shen | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| shijie-lian | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| xiaopeng-lin | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| cong-huang | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| zhirui-zhang | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| lei-zhang | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| kai-chen | unlisted | SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models | 2026-07-07 | VLA 示教数据质量的关键不只是数量，而是减少冗余、噪声和覆盖不均，并保留可复用的行为结构；结构感知筛选能让更少数据优于全量训练。 | limit |
| jiaming-liu | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| qingpo-wuwu | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| nuowei-han | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| hao-chen | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| zhuoyang-liu | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| fan-fei | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| yueru-jia | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| chenyang-gu | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| yandong-guo | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| boxin-shi | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| shanghang-zhang | unlisted | Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation | 2026-07-07 | 物理操作中的高质量数据需要显式承载 3D 几何和时间动态；只依赖 2D 视觉预训练会在几何约束、遮挡、接触和动态一致性上丢信息。 | support |
| haoyu-zhao | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| xingyue-zhao | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| hangyu-li | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| biao-gong | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| kehan-li | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| siteng-huang | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| xin-li | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| deli-zhao | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| zhongyu-li | unlisted | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | 2026-07-07 | 扩展机器人数据的瓶颈正在从真实机器人示教转向可验证的生成式数据引擎：数字遥操作能降低硬件和场景约束，但仍要面对复杂物理、形变和本体微调限制。 | conditional |
| gigaworld-team | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| angyuan-ma | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| boyuan-wang | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| bohan-li | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| chaojun-ni | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| guo-li | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| guan-huang | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| guosheng-zhao | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| hao-li | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| hengtao-li | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| jingyu-liu | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| jiwen-lu | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| qiuping-deng | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| tingdong-yu | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| xuancheng-xu | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| xinyu-zhou | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| xiuwei-xu | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| xinze-chen | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| xiaofeng-wang | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| xiaoyu-tian | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| yang-wang | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| yifan-chang | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| yukun-zhou | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| yun-ye | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| zhenyu-wu | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| zhanqian-wu | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| zheng-zhu | unlisted | GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation | 2026-07-02 | 数据质量必须经闭环评估定义；对机器人世界模型来说，短期视觉真实感不如长程、动作忠实的 rollout 一致性更能决定其作为策略评估器的可靠性。 | support |
| hongyu-li | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| wanjia-fu | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| xiaoyan-cong | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| zekun-li | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| binghao-huang | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| hanxiao-jiang | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| xintong-he | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| yiqing-liang | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| rao-fu | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| tao-lu | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| srinath-sridhar | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| kevin-a-smith | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| george-konidaris | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| yunzhu-li | unlisted | Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models | 2026-07-06 | 软物体和形变场景中的数据质量主要受可观测性约束：必须同时记录多视角全局运动、触觉局部形变和可用于评测的 3D 轨迹。 | support |
| shengbang-liu | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| yueru-jia | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| yuyang-yan | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| jiaming-liu | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| xinran-zhang | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| qiuxuan-feng | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| yandong-guo | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| shiji-zhou | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| boxin-shi | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |
| shanghang-zhang | unlisted | TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training | 2026-07-03 | 接触丰富任务里的失败常是视觉不可见的局部接触扰动；仅用视觉世界模型会产生看似合理但接触不一致的轨迹，因此纠错数据需要触觉/力反馈参与。 | limit |

## Topic Card Update Suggestions

- Add only high-signal synthesis with source IDs; keep raw evidence in JSONL.
- Treat this as a candidate update list, not an automatic topic-card patch.
