# Evidence Appendix: Ego-Exo 后继研究：第三人称→第一人称视觉表征迁移的演进

- Time range: 2026-02-13..2026-08-13
- Events: 20
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-EGOEXO-2026-0001

- Claim: Ego-Exo 从大规模第三人称视频中挖掘 Ego-Score、Object-Score、Interaction-Map 三类 egocentric 信号，并以知识蒸馏损失在预训练时注入视频模型，从而无需配对或动作标注的 ego 视频。
- Stance: `support` | Confidence: `direct`
- Paper: [2104.07905](https://arxiv.org/abs/2104.07905) Ego-Exo: Transferring Visual Representations from Third-person to First-person Videos
- Locator: Abstract (full-text section)
- Evidence: 摘要与方法部分直接陈述该核心思想与三类辅助任务。
- Quote: “pre-training egocentric video models using large-scale third-person video datasets. Learning from purely egocentric data is limited by low dataset scale and diversity, while using purely exocentric (third-person) data introduces a large domain mismatch. Our idea is to discover latent signals in third-person video that are”
- Authors: yanghao-li; tushar-nagarajan; bo-xiong; et al.

### EA-EGOEXO-2026-0002

- Claim: Ego-Exo 在 Charades-Ego 上较 Kinetics 预训练基线提升 +3.26 mAP，并在 EPIC-Kitchens-100 取得当时 SOTA。
- Stance: `support` | Confidence: `direct`
- Paper: [2104.07905](https://arxiv.org/abs/2104.07905) Ego-Exo: Transferring Visual Representations from Third-person to First-person Videos
- Locator: 1 Introduction
- Evidence: 实验部分报告了相对标准预训练基线的提升幅度。
- Quote: “paradigm—by +3.26 mAP, and outperforms methods that specifically aim to bridge the domain gap between viewpoints. Finally, our pre-trained model achieves state-of-the-art results on EPIC-Kitchens-100 [ 11 ] , the largest available first-person dataset.”
- Authors: yanghao-li; tushar-nagarajan; bo-xiong; et al.

### EA-EGOEXO-2026-0007

- Claim: 该工作提出从 exocentric 视角的 affordance grounding：从第三人称人-物交互图像学习可供性知识并迁移到 egocentric 物体图像，仅用 affordance 标签监督，并构建 AGD20K 数据集。
- Stance: `support` | Confidence: `direct`
- Paper: [2203.09905](https://arxiv.org/abs/2203.09905) Learning Affordance Grounding from Exocentric Images
- Locator: Abstract (full-text section)
- Evidence: 摘要直接陈述该任务设定与数据集。
- Quote: “affordance grounding from exocentric view, i.e. , given exocentric human-object interaction and egocentric object images, learning the affordance knowledge of the object and transferring it to the egocentric image using only the affordance label as supervision. To this end, we devise”
- Authors: hongcheng-luo; wei-zhai; jing-zhang; et al.

### EA-EGOEXO-2026-0008

- Claim: 在 seen 设定下，该方法 KLD 较最佳 saliency 模型提升 17.2%，较 affordance grounding 模型提升 13.3%。
- Stance: `support` | Confidence: `direct`
- Paper: [2203.09905](https://arxiv.org/abs/2203.09905) Learning Affordance Grounding from Exocentric Images
- Locator: 5.2 Quantitative and Qualitative Comparisons
- Evidence: 实验部分报告相对各基线的提升幅度。
- Quote: “improves 17.2% compared to the best saliency model, 16.5% over the best weakly supervised object localization (WSOL) model, and 13.3% over the affordance grounding model in the “Seen” setting. Our method with the “Unseen” setting improves 10.2% compared to”
- Authors: hongcheng-luo; wei-zhai; jing-zhang; et al.

### EA-EGOEXO-2026-0016

- Claim: 该期刊版在会议版基础上引入 Cross-view Feature Transfer（CFT）模块，通过密集匹配显式建模人与人之间的 interaction bias，扩展 AGD20K 至 26,117 图像。
- Stance: `support` | Confidence: `direct`
- Paper: [2208.13196](https://arxiv.org/abs/2208.13196) Grounded Affordance from Exocentric View
- Locator: Abstract (full-text section)
- Evidence: 引言与摘要陈述 CFT 模块与 interaction bias 建模。
- Quote: ““interaction bias” between personas, mainly regarding different regions and views. To this end, we devise a cross-view affordance knowledge transfer framework that extracts affordance-specific features from exocentric interactions and transfers them to the egocentric”
- Authors: hongcheng-luo; wei-zhai; jing-zhang; et al.

### EA-EGOEXO-2026-0009

- Claim: LOCATE 提出部件级知识迁移：定位 exo 交互区域、用 PartSelect 选出物体部件原型，再以此监督 egocentric affordance grounding，仅用图像级标签弱监督。
- Stance: `support` | Confidence: `direct`
- Paper: [2303.09665](https://arxiv.org/abs/2303.09665) LOCATE: Localize and Transfer Object Parts for Weakly Supervised Affordance Grounding
- Locator: Abstract (full-text section)
- Evidence: 摘要与方法部分直接陈述部件级迁移机制。
- Quote: “transfer knowledge from images where an object is being used (exocentric images used for learning), to images where the object is inactive (egocentric ones used to test). To this end, we first find interaction areas and extract their feature embeddings. Then we learn to aggregate the embeddings into”
- Authors: gen-li; varun-jampani; deqing-sun; et al.

### EA-EGOEXO-2026-0010

- Claim: 在 unseen 设定下，LOCATE 较 SOTA 方法 Cross-view-AG+ 提升 KLD 20.4%、SIM 33.3%、NSS 31.2%。
- Stance: `support` | Confidence: `direct`
- Paper: [2303.09665](https://arxiv.org/abs/2303.09665) LOCATE: Localize and Transfer Object Parts for Weakly Supervised Affordance Grounding
- Locator: 4.2 Comparison to State-of-the-Art
- Evidence: 实验部分报告相对 Cross-view-AG+ 的提升。
- Quote: “improve the KLD by 20.4%, SIM by 33.3%, and NSS by 31.2% in the unseen setting. Cross-view-AG+ is an extended version of Cross-view-AG, but still performs the knowledge transfer based on global pooled embeddings at the image level, thus bringing only minor improvement.”
- Authors: gen-li; varun-jampani; deqing-sun; et al.

### EA-EGOEXO-2026-0011

- Claim: AE2 从 unpaired 的 ego-exo 视频学习细粒度视角不变表征：用 object-centric 编码器关注手与主动物体，以 DTW 时序对齐作自监督目标，并用反转帧作负样本对比正则。
- Stance: `support` | Confidence: `direct`
- Paper: [2306.05526](https://arxiv.org/abs/2306.05526) Learning Fine-grained View-Invariant Representations from Unpaired Ego-Exo Videos via Temporal Alignment
- Locator: 1 Introduction
- Evidence: 摘要与方法部分直接陈述三个关键设计。
- Quote: “unpaired data. In the unpaired setting, we know which human activity occurs in any given training sequence ( e.g. , pouring, breaking eggs), but they need not be collected simultaneously or in the same environment. The main idea of our self-supervised”
- Authors: zihui-xue; kristen-grauman

### EA-EGOEXO-2026-0012

- Claim: AE2 在四个数据集、regular 与 cross-view 设定上全面超越 SOTA（如 Break Eggs 动作相位分类 F1 66.23 vs 最佳基线 GTA 56.86）。
- Stance: `support` | Confidence: `direct`
- Paper: [2306.05526](https://arxiv.org/abs/2306.05526) Learning Fine-grained View-Invariant Representations from Unpaired Ego-Exo Videos via Temporal Alignment
- Locator: 5 Experiments
- Evidence: 实验表 1 报告各数据集分类/检索指标。
- Quote: “66.23 57.41 71.72 65.85 64.59 62.15 0.5109 0.6316 (B) Random Features 36.84 33.96 41.97 52.48 50.56 51.98 -0.0477 0.0050 ImageNet Features 41.59 39.93 45.52 54.09 27.31 43.21 -2.6681 0.0115 single-view TCN sermanet2018time 47.39 43.44 42.28 57.00”
- Authors: zihui-xue; kristen-grauman

### EA-EGOEXO-2026-0003

- Claim: Ego-Exo4D 是迄今最大的时间同步第一+第三人称视频数据集，共 1286 小时、740 名参与者、覆盖 8 个领域技能活动，并配多模态与专家评论等语言标注。
- Stance: `support` | Confidence: `direct`
- Paper: [2311.18259](https://arxiv.org/abs/2311.18259) Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person Perspectives
- Locator: Abstract (full-text section)
- Evidence: 摘要与数据集部分直接报告规模与模态。
- Quote: “1,286 hours of video combined. The multimodal nature of the dataset is unprecedented: the video is accompanied by multichannel audio, eye gaze, 3D point clouds, camera poses, IMU, and multiple paired language descriptions— including a novel “expert commentary” done by coaches”
- Authors: kristen-grauman; andrew-westbury; lorenzo-torresani; et al.

### EA-EGOEXO-2026-0004

- Claim: Ego-Exo4D 首次形式化 ego-exo relation 任务族（对象级对应 correspondence 与视角翻译 translation），使 first↔third-person 视角迁移成为可评测的基准任务。
- Stance: `support` | Confidence: `direct`
- Paper: [2311.18259](https://arxiv.org/abs/2311.18259) Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person Perspectives
- Locator: 1 Introduction
- Evidence: 基准任务部分定义 ego-exo relation 家族。
- Quote: “ego-exo relation , for relating the actions of a teacher (exo) to a learner (ego) by estimating semantic correspondences and translating viewpoints; 2. ego(-exo) recognition , for recognizing fine-grained keysteps and task structure; 3. ego(-exo) proficiency”
- Authors: kristen-grauman; andrew-westbury; lorenzo-torresani; et al.

### EA-EGOEXO-2026-0017

- Claim: 该工作用无标注的同步 exo-ego 视频对做知识蒸馏，把时序动作分割模型从 exo 迁移到 ego，无需任何 ego 标签，并在 Assembly101 与 EgoExo4D 上验证。
- Stance: `support` | Confidence: `direct`
- Paper: [2312.02638](https://arxiv.org/abs/2312.02638) Synchronization is All You Need: Exocentric-to-Egocentric Transfer for Temporal Action Segmentation with Unlabeled Synchronized Video Pairs
- Locator: Abstract (full-text section)
- Evidence: 摘要与方法部分直接陈述该设定与方法。
- Quote: “temporal action segmentation system initially designed for exocentric (fixed) cameras to an egocentric scenario, where wearable cameras capture video data. The conventional supervised approach requires the collection and labeling of a new set of egocentric videos to adapt”
- Authors: camillo-quattrocchi; antonino-furnari; daniele-di-mauro; et al.

### EA-EGOEXO-2026-0018

- Claim: 同步蒸馏最佳模型在 Assembly101 上与监督式 ego-oracle 相当（edit 28.59 vs 26.42），远超仅用 exo 数据的基线（edit 12.60）。
- Stance: `support` | Confidence: `direct`
- Paper: [2312.02638](https://arxiv.org/abs/2312.02638) Synchronization is All You Need: Exocentric-to-Egocentric Transfer for Temporal Action Segmentation with Unlabeled Synchronized Video Pairs
- Locator: 5.1 Performance of the Proposed Approach
- Evidence: 实验表 1 报告 edit 分数对比。
- Quote: “28.59 29.58 24.84 16.38 31.36 13 ✓ ✓ 28.13 28.75 24.16 15.79 32.67 14 Improvement w.r.t. baseline (line 10) Table 2 : Results for the v4 e4 view adaptation setting. Best results within groups are reported in bold. Best results among the adaptation”
- Authors: camillo-quattrocchi; antonino-furnari; daniele-di-mauro; et al.

### EA-EGOEXO-2026-0019

- Claim: EgoInstructor 用自动挖掘的 ego-exo 视频对训练跨视角检索模块，检索语义相关的第三人称教学视频作参考，增强 egocentric 视频描述。
- Stance: `support` | Confidence: `direct`
- Paper: [2401.00789](https://arxiv.org/abs/2401.00789) EgoInstructor: Retrieval-Augmented Egocentric Video Captioning
- Locator: Abstract (full-text section)
- Evidence: 摘要直接陈述检索增强框架。
- Quote: “retrieval-augmented multimodal captioning model that automatically retrieves semantically relevant third-person instructional videos to enhance the video captioning of egocentric videos, (2) for training the cross-view retrieval module, we devise an automatic”
- Authors: jilan-xu; yifei-huang; junlin-hou; et al.

### EA-EGOEXO-2026-0020

- Claim: EgoInstructor 的跨视角检索模块在 7 个 benchmark 上一致提升，如 InternVideo 在 CharadesEgo 上 Ego2Exo/Exo2Ego 分别提升 15.9% 与 7.7%。
- Stance: `support` | Confidence: `direct`
- Paper: [2401.00789](https://arxiv.org/abs/2401.00789) EgoInstructor: Retrieval-Augmented Egocentric Video Captioning
- Locator: 4.2.1 Results on Cross-view Retrieval
- Evidence: 实验部分报告跨视角检索提升幅度。
- Quote: “by 15.9% and 7.7% on CharadesEgo.”
- Authors: jilan-xu; yifei-huang; junlin-hou; et al.

### EA-EGOEXO-2026-0005

- Claim: EgoExoLearn 将 ego-exo 迁移推进到异步、异环境的演示跟随（demo-following）设定：个体观看 exo 演示后在佩戴 gaze 设备的情况下于不同环境复现程序性任务，共 120 小时。
- Stance: `support` | Confidence: `direct`
- Paper: [2403.16182](https://arxiv.org/abs/2403.16182) EgoExoLearn: A Dataset for Bridging Asynchronous Ego- and Exo-centric View of Procedural Activities in Real World
- Locator: Abstract (full-text section)
- Evidence: 摘要与数据收集部分直接描述该设定与规模。
- Quote: “asynchronous procedural actions from different viewpoints. To this end, we present benchmarks such as cross-view association, cross-view action planning, and cross-view referenced skill assessment, along with detailed analysis. We expect EgoExoLearn can”
- Authors: yifei-huang; guo-chen; jilan-xu; et al.

### EA-EGOEXO-2026-0015

- Claim: EgoExo-Fitness 提供 32 小时、1276 段同步 egocentric+exocentric 全身健身动作数据集，并引入技术关键点核验、自然语言评语、质量分等可解释动作评判标注。
- Stance: `support` | Confidence: `direct`
- Paper: [2406.08877](https://arxiv.org/abs/2406.08877) EgoExo-Fitness: Towards Egocentric and Exocentric Full-Body Action Understanding
- Locator: 1 Introduction
- Evidence: 摘要直接陈述数据集规模与标注。
- Quote: “synchronized egocentric and exocentric videos of fitness activities to support future work on egocentric full-body action understanding. (b) EgoExo-Fitness provides abundant annotations, including two-level temporal boundaries and interpretable action judgement. (c) We benchmark”
- Authors: yuan-ming-li; wei-jin-huang; an-lan-wang; et al.

### EA-EGOEXO-2026-0013

- Claim: ObjectRelator 针对 ego-exo 对象对应任务，用 MCFuse 融合文本描述与视觉掩码、XObjAlign 做自监督跨视角对象对齐，在 Ego-Exo4D 上取得 SOTA。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.19083](https://arxiv.org/abs/2411.19083) ObjectRelator: Enabling Cross-View Object Relation Understanding Across Ego-Centric and Exo-Centric Perspectives
- Locator: Abstract (full-text section)
- Evidence: 摘要与引言直接陈述方法与任务。
- Quote: “Bridging the gap between ego-centric and exo-centric views has been a long-standing question in computer vision. In this paper, we focus on the emerging Ego-Exo object correspondence task, which aims to understand object relations across ego-exo perspectives through segmentation. While numerous segmentation”
- Authors: yu-fu; runze-wang; bin-ren; et al.

### EA-EGOEXO-2026-0014

- Claim: ObjectRelator 在 Ego-Exo4D 对象对应任务上较 PSALM 提升 IoU：Ego2Exo 39.7→44.3，Exo2Ego 44.1→49.2。
- Stance: `support` | Confidence: `direct`
- Paper: [2411.19083](https://arxiv.org/abs/2411.19083) ObjectRelator: Enabling Cross-View Object Relation Understanding Across Ego-Centric and Exo-Centric Perspectives
- Locator: 4.1 Main Results on Ego-Exo4D
- Evidence: 主结果表 2 报告 IoU 对比。
- Quote: “improves the PSALM from 39.7 to 44.3 on Ego2Exo and from 44.1 to 49.2 on Exo2Ego. Regarding LE, CA, and VA, Our ObjectRelator consistently outperforms PSALM, achieving clear margins over all other competitors. These results well demonstrate the effectiveness of our approach. In”
- Authors: yu-fu; runze-wang; bin-ren; et al.

### EA-EGOEXO-2026-0006

- Claim: EgoExoLearn 的 cross-view association 基准显示，即使 co-training ego+exo 并使用 gaze，模型跨视角关联能力仍有限（Exo2Ego test 最高约 55.3% top-1），暴露出桥接异步 ego-exo 活动的显著 gap。
- Stance: `gap` | Confidence: `direct`
- Paper: [2403.16182](https://arxiv.org/abs/2403.16182) EgoExoLearn: A Dataset for Bridging Asynchronous Ego- and Exo-centric View of Procedural Activities in Real World
- Locator: 4.2.1 Cross-view association
- Evidence: 实验结果部分报告该基准的准确率并据此指出模型局限。
- Quote: “55.3 51.1 Table 3 : Association accuracy in the cross-view association benchmark. In the fine-tuned setting, we adopt three kinds of data sources for training, i.e. , ego-only, exo-only, and hybrid ego-exo data. By leveraging gaze information during”
- Authors: yifei-huang; guo-chen; jilan-xu; et al.

## References

- `2104.07905` [Ego-Exo: Transferring Visual Representations from Third-person to First-person Videos](https://arxiv.org/abs/2104.07905) (2021-04-16)
- `2203.09905` [Learning Affordance Grounding from Exocentric Images](https://arxiv.org/abs/2203.09905) (2022-03-18)
- `2208.13196` [Grounded Affordance from Exocentric View](https://arxiv.org/abs/2208.13196) (2022-08-28)
- `2303.09665` [LOCATE: Localize and Transfer Object Parts for Weakly Supervised Affordance Grounding](https://arxiv.org/abs/2303.09665) (2023-03-17)
- `2306.05526` [Learning Fine-grained View-Invariant Representations from Unpaired Ego-Exo Videos via Temporal Alignment](https://arxiv.org/abs/2306.05526) (2023-06-10)
- `2311.18259` [Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person Perspectives](https://arxiv.org/abs/2311.18259) (2023-11-30)
- `2312.02638` [Synchronization is All You Need: Exocentric-to-Egocentric Transfer for Temporal Action Segmentation with Unlabeled Synchronized Video Pairs](https://arxiv.org/abs/2312.02638) (2023-12-05)
- `2401.00789` [EgoInstructor: Retrieval-Augmented Egocentric Video Captioning](https://arxiv.org/abs/2401.00789) (2024-01-01)
- `2403.16182` [EgoExoLearn: A Dataset for Bridging Asynchronous Ego- and Exo-centric View of Procedural Activities in Real World](https://arxiv.org/abs/2403.16182) (2024-03-25)
- `2406.08877` [EgoExo-Fitness: Towards Egocentric and Exocentric Full-Body Action Understanding](https://arxiv.org/abs/2406.08877) (2024-06-13)
- `2411.19083` [ObjectRelator: Enabling Cross-View Object Relation Understanding Across Ego-Centric and Exo-Centric Perspectives](https://arxiv.org/abs/2411.19083) (2024-11-28)
