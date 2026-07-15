# Evidence Appendix: 近一年图像视觉定位方法的发展与挑战

- Time range: 2025-07-15..2026-07-15
- Events: 15
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-VLOC-2026-0005

- Claim: 大场景SCR可通过同时约束视觉相似性与共视几何连接的全局描述子缓解感知别名和噪声图边，而不是只依赖局部特征或纯几何嵌入。
- Stance: `support` | Confidence: `direct`
- Paper: [2512.17226](https://arxiv.org/abs/2512.17226) Robust Scene Coordinate Regression via Geometrically-Consistent Global Descriptors
- Locator: 7 Conclusion
- Evidence: 结论明确将韧性提升归因于视觉内容和几何关系的联合建模。
- Quote: “Our method integrates both geometrical relationships and visual content to improve resilience to perceptual aliasing and noisy covisibility graphs.”
- Authors: son-tung-nguyen; alejandro-fontan; michael-milford; et al.

### EA-VLOC-2026-0001

- Claim: 3DGS特征场可把渲染和特征学习接入位姿细化，但定位可靠性仍受底层3DGS几何质量约束，弱纹理平坦场景会直接拖累结果。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2507.23569](https://arxiv.org/abs/2507.23569) Gaussian Splatting Feature Fields for Privacy-Preserving Visual Localization
- Locator: 5.1 Visual Localization
- Evidence: 作者在7Scenes的Stairs场景明确把退化归因于纹理缺失和平坦布局导致的初始3D结构质量差。
- Quote: “On Stairs, the Opacity Gaussian Field struggles due to its textureless and flat layout, yielding a poor results for the initial 3D structure that directly affects GSFFs-PR’s refinement framework.”
- Authors: maxime-pietrantoni; gabriela-csurka; torsten-sattler

### EA-VLOC-2026-0002

- Claim: 前馈式稀疏特征地图能把逐场景地图准备降到检索级别，但这一优势仍依赖选到相关参考图像；随机或均匀选择会导致准确率下降。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.00978](https://arxiv.org/abs/2510.00978) A Scene is Worth a Thousand Features: Feed-Forward Camera Localization from a Collection of Image Features
- Locator: page 10
- Evidence: 作者在限制实验中移除检索并改用随机/均匀参考，观察到FastForward准确率下降。
- Quote: “We observe the accuracy dropping from 51.4% to 47.8% (10cm, 10°).”
- Authors: axel-barroso-laguna; tommaso-cavallari; victor-adrian-prisacariu; et al.

### EA-VLOC-2026-0003

- Claim: 重建先验可以改善ACE系场景坐标回归而不增加查询时延，但当前证据主要限于室内，户外需要重新设计深度分布与扩散先验数据。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.12387](https://arxiv.org/abs/2510.12387) Scene Coordinate Reconstruction Priors
- Locator: 5 Conclusion
- Evidence: 结论同时报告性能增益、无查询时延代价和室内证据边界。
- Quote: “Limitations Our experiments have focused on indoor scenes, with results on a few outdoor scenes in the supplement.”
- Authors: wenjing-bian; axel-barroso-laguna; tommaso-cavallari; et al.

### EA-VLOC-2026-0004

- Claim: 训练免费的相似度分布不确定性可作为VPR错误匹配拒绝器，但在极端重复场景中，仅看分数仍可能失效，需要几何线索补充。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2510.13464](https://arxiv.org/abs/2510.13464) Through the Lens of Doubt: Robust and Efficient Uncertainty Estimation for Visual Place Recognition
- Locator: VII Conclusions and Future Work
- Evidence: 作者在结论明确指出分数依赖在极端重复场景中的退化。
- Quote: “While these metrics are highly effective, their reliance on similarity scores means performance may degrade in extremely repetitive scenes where geometric cues are necessary.”
- Authors: emily-miller; michael-milford; muhammad-burhan-hafez; et al.

### EA-VLOC-2026-0007

- Claim: 现代VPR不存在单一最优骨干：ViT更适合强感知别名和缺帧，CNN在实时系统中通常提供更好的检索质量—运行时间折中。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2603.13917](https://arxiv.org/abs/2603.13917) Evaluation of Visual Place Recognition Methods for Image Pair Retrieval in 3D Vision and Robotics
- Locator: 7 Conclusion
- Evidence: 结论依据三类数据集比较CNN与ViT并给出按场景选型建议。
- Quote: “In real-time scenarios, CNN-based methods appear preferable due to their favourable trade-off between retrieval quality and runtime, whereas ViT-based methods achieve higher retrieval performance in highly challenging scenes with strong perceptual aliasing and missing frames in image sequences.”
- Authors: dennis-haitz; athradi-shritish-shetty; michael-weinmann; et al.

### EA-VLOC-2026-0006

- Claim: 视觉定位评测的真值定义会显著改变结论：仅按相机位置接近判正，会在地形起伏或高度变化大时系统性高估VPR表现。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.04056](https://arxiv.org/abs/2603.04056) Long-Term Visual Localization in Dynamic Benthic Environments: A Dataset, Footprint-Based Ground Truth, and Visual Place Recognition Benchmark
- Locator: 5 Conclusion
- Evidence: 作者比较两套真值并发现足迹重叠与真实检索更一致。
- Quote: “Comparing our footprint-based ground truth to a traditional location-based ground truth shows that spatial proximity alone can systematically overestimate Recall@K, especially at sites with rugged terrain or large altitude variations, whereas the footprint-based ground truth is more aligned with actual VPR retrievals.”
- Authors: martin-kvisvik-larsen; oscar-pizarro

### EA-VLOC-2026-0008

- Claim: 3DGS位姿细化不是全局纠错器：它高度依赖初始位姿质量，单一错误Top-1检索即使视觉相似也可能从场景错误一侧开始，局部细化难以恢复。
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.16538](https://arxiv.org/abs/2603.16538) Rethinking Pose Refinement in 3D Gaussian Splatting under Pose Prior and Geometric Uncertainty
- Locator: A Leveraging Image Retrieval Prior
- Evidence: 作者在检索先验补充实验中明确说明细化只在初值附近局部调整。
- Quote: “Pose refinement in 3D Gaussian Splatting relies heavily on the quality of the initial pose prior, since the refinement module only adjusts the pose locally around this estimate.”
- Authors: mangyu-kong; jaewon-lee; seongwon-lee; et al.

### EA-VLOC-2026-0009

- Claim: VPR基准接近饱和时，固定地理半径标签本身会成为主要误差源：25米阈值可能忽略真实视觉重叠，使方法排名与可用定位不一致。
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.22390](https://arxiv.org/abs/2604.22390) Region Matters: Efficient and Reliable Region-Aware Visual Place Recognition
- Locator: 5 Discussion
- Evidence: 讨论明确指出当前任务标签忽视视觉重叠并放大歧义。
- Quote: “Current evaluations depend on the task-defined geographic threshold (25 meters), which often ignores visual overlap and exacerbates this label ambiguity.”
- Authors: shunpeng-chen; yukun-song; changwei-wang; et al.

### EA-VLOC-2026-0010

- Claim: 3DGS地图的照片真实度不等于定位几何可用性：冗余高斯及像素到高斯的多对一对应会削弱匹配鲁棒性并使PnP收敛不稳。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.07351](https://arxiv.org/abs/2605.07351) Disambiguating 2D-3D Correspondences in Gaussian Splatting-based Feature Fields for Visual Localization
- Locator: 5 Conclusion
- Evidence: 作者在结论把问题归结为照片度量GSFF与点式PnP对应的结构错配。
- Quote: “Yet photometrically optimized GSFFs are fundamentally ill-suited for 2D-3D matching, as redundant Gaussians and many-to-one pixel-Gaussian correspondences undermine both matching robustness and PnP convergence.”
- Authors: miso-lee; sangeek-hyun; yerim-jeon; et al.

### EA-VLOC-2026-0014

- Claim: 把场景存进SCR网络权重并不天然保护隐私：在可发出代理查询并读取三维预测时，攻击者能够聚合恢复场景几何和外观线索。
- Stance: `limit` | Confidence: `direct`
- Paper: [2606.31164](https://arxiv.org/abs/2606.31164) Seeing Through the Weights: Privacy Leakage in Scene Coordinate Regression
- Locator: 6 Conclusion
- Evidence: 论文结论明确说明代理查询与三维预测聚合可恢复几何和外观。
- Quote: “By issuing proxy queries and aggregating the returned 3D predictions, the proposed approach recovers both geometric structure and appearance cues.”
- Authors: oleksii-nasypanyi; jaemin-cho; utku-ozbulak; et al.

### EA-VLOC-2026-0013

- Claim: 在森林VPR中，把深度几何蒸馏进外观描述子可同时改善同序列与跨序列识别，说明几何先验是缓解重复纹理的一条有效方向。
- Stance: `support` | Confidence: `direct`
- Paper: [2606.13206](https://arxiv.org/abs/2606.13206) Visual Place Recognition in Forests with Depth-Aware Distillation
- Locator: III Results and Discussion
- Evidence: 作者直接报告DAD在两种评估中均超过仅外观SALAD。
- Quote: “DAD improves over the appearance-only SALAD baseline in both intra-sequence and inter-sequence evaluation.”
- Authors: walter-nedov; saimunur-rahman; kavindie-katuwandeniya; et al.

### EA-VLOC-2026-0012

- Claim: 多参考地点表示的收益具有分布条件：参考遍历覆盖查询变化时，判别压缩有效；极端视角且视觉重叠很少时，保留各参考描述子的策略更稳。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2605.30769](https://arxiv.org/abs/2605.30769) DisPlace: Discriminative Place Projections for Multi-Reference Visual Place Recognition
- Locator: VI Discussion and Conclusion
- Evidence: 作者在讨论中明确把收益与参考—查询变化代表性绑定，并指出极端视角的落后情形。
- Quote: “The results further reveal that the discriminative projection is most effective when the variation observed across the reference traversals is representative of the variation encountered at query time, particularly under appearance variation where descriptor changes exhibit structured and suppressible patterns.”
- Authors: dhyey-manish-rajani; michael-milford; tobias-fischer

### EA-VLOC-2026-0015

- Claim: VPR正在从平均召回转向地理分布鲁棒性，但现有长尾建模仍主要按地理类样本数划分，尚不能代表地点本身的视觉难度。
- Stance: `conditional` | Confidence: `direct`
- Paper: [2607.00090](https://arxiv.org/abs/2607.00090) Lost in the Tail: Addressing Geographic Imbalance in Urban Visual Place Recognition
- Locator: 5 Conclusion
- Evidence: 作者在结论明确承认当前长尾只按每类样本量定义。
- Quote: “Nevertheless, our current formulation defines the long-tail distribution based on sample count per geographic class , focusing on dataset-level imbalance.”
- Authors: zhiyao-shu; jiacheng-yang; yang-lu; et al.

### EA-VLOC-2026-0011

- Claim: 跨条件VPR的安全性必须与覆盖率一起评估：重复且无信息的景观中，校准验证器可以靠全局拒识维持安全，但定位效用降为零。
- Stance: `limit` | Confidence: `direct`
- Paper: [2605.28048](https://arxiv.org/abs/2605.28048) SAFEVPR: Patch-Based Conformal Verification for Safe Cross-Condition Sequence Visual Place Recognition
- Locator: VII-B When does it fail?
- Evidence: 作者把Nordland描述为已知但安全的边界，因为系统能检测无信息状态并整体拒绝。
- Quote: “We report Nordland as a known but safe boundary: the recipe self-detects uninformativeness and abstains globally.”
- Authors: ha-sier; jiaqiang-zhang; zhuo-zou; et al.

## References

- `2507.23569` [Gaussian Splatting Feature Fields for Privacy-Preserving Visual Localization](https://arxiv.org/abs/2507.23569) (2025-07-31)
- `2510.00978` [A Scene is Worth a Thousand Features: Feed-Forward Camera Localization from a Collection of Image Features](https://arxiv.org/abs/2510.00978) (2025-10-01)
- `2510.12387` [Scene Coordinate Reconstruction Priors](https://arxiv.org/abs/2510.12387) (2025-10-14)
- `2510.13464` [Through the Lens of Doubt: Robust and Efficient Uncertainty Estimation for Visual Place Recognition](https://arxiv.org/abs/2510.13464) (2025-10-15)
- `2512.17226` [Robust Scene Coordinate Regression via Geometrically-Consistent Global Descriptors](https://arxiv.org/abs/2512.17226) (2025-12-19)
- `2603.04056` [Long-Term Visual Localization in Dynamic Benthic Environments: A Dataset, Footprint-Based Ground Truth, and Visual Place Recognition Benchmark](https://arxiv.org/abs/2603.04056) (2026-03-04)
- `2603.13917` [Evaluation of Visual Place Recognition Methods for Image Pair Retrieval in 3D Vision and Robotics](https://arxiv.org/abs/2603.13917) (2026-03-14)
- `2603.16538` [Rethinking Pose Refinement in 3D Gaussian Splatting under Pose Prior and Geometric Uncertainty](https://arxiv.org/abs/2603.16538) (2026-03-17)
- `2604.22390` [Region Matters: Efficient and Reliable Region-Aware Visual Place Recognition](https://arxiv.org/abs/2604.22390) (2026-04-24)
- `2605.07351` [Disambiguating 2D-3D Correspondences in Gaussian Splatting-based Feature Fields for Visual Localization](https://arxiv.org/abs/2605.07351) (2026-05-08)
- `2605.28048` [SAFEVPR: Patch-Based Conformal Verification for Safe Cross-Condition Sequence Visual Place Recognition](https://arxiv.org/abs/2605.28048) (2026-05-27)
- `2605.30769` [DisPlace: Discriminative Place Projections for Multi-Reference Visual Place Recognition](https://arxiv.org/abs/2605.30769) (2026-05-29)
- `2606.13206` [Visual Place Recognition in Forests with Depth-Aware Distillation](https://arxiv.org/abs/2606.13206) (2026-06-11)
- `2606.31164` [Seeing Through the Weights: Privacy Leakage in Scene Coordinate Regression](https://arxiv.org/abs/2606.31164) (2026-06-30)
- `2607.00090` [Lost in the Tail: Addressing Geographic Imbalance in Urban Visual Place Recognition](https://arxiv.org/abs/2607.00090) (2026-06-30)
