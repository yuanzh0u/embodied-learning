# Writing Brief: 近一年图像视觉定位方法的发展与挑战

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年图像视觉定位方法的发展与挑战
- Time range: 2025-07-15..2026-07-15
- Knowledge IDs: `EA-HARDWARE`, `EA-SENSOR`, `EA-EVAL`, `EA-4D`
- Review mode: scoping
- Paper-level sources: 15 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 15

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-HARDWARE`: 大场景SCR可通过同时约束视觉相似性与共视几何连接的全局描述子缓解感知别名和噪声图边，而不是只依赖局部特征或纯几何嵌入。 ([2512.17226](https://arxiv.org/abs/2512.17226) / [EA-VLOC-2026-0005](evidence-appendix.md#ea-vloc-2026-0005)) ⟷ 视觉定位评测的真值定义会显著改变结论：仅按相机位置接近判正，会在地形起伏或高度变化大时系统性高估VPR表现。 ([2603.04056](https://arxiv.org/abs/2603.04056) / [EA-VLOC-2026-0006](evidence-appendix.md#ea-vloc-2026-0006))
- `EA-SENSOR`: 在森林VPR中，把深度几何蒸馏进外观描述子可同时改善同序列与跨序列识别，说明几何先验是缓解重复纹理的一条有效方向。 ([2606.13206](https://arxiv.org/abs/2606.13206) / [EA-VLOC-2026-0013](evidence-appendix.md#ea-vloc-2026-0013)) ⟷ 多参考地点表示的收益具有分布条件：参考遍历覆盖查询变化时，判别压缩有效；极端视角且视觉重叠很少时，保留各参考描述子的策略更稳。 ([2605.30769](https://arxiv.org/abs/2605.30769) / [EA-VLOC-2026-0012](evidence-appendix.md#ea-vloc-2026-0012))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-HARDWARE (11 events)
- [`support`] 大场景SCR可通过同时约束视觉相似性与共视几何连接的全局描述子缓解感知别名和噪声图边，而不是只依赖局部特征或纯几何嵌入。 ([2512.17226](https://arxiv.org/abs/2512.17226) / [EA-VLOC-2026-0005](evidence-appendix.md#ea-vloc-2026-0005))
- [`conditional`] 3DGS特征场可把渲染和特征学习接入位姿细化，但定位可靠性仍受底层3DGS几何质量约束，弱纹理平坦场景会直接拖累结果。 ([2507.23569](https://arxiv.org/abs/2507.23569) / [EA-VLOC-2026-0001](evidence-appendix.md#ea-vloc-2026-0001))
- [`conditional`] 前馈式稀疏特征地图能把逐场景地图准备降到检索级别，但这一优势仍依赖选到相关参考图像；随机或均匀选择会导致准确率下降。 ([2510.00978](https://arxiv.org/abs/2510.00978) / [EA-VLOC-2026-0002](evidence-appendix.md#ea-vloc-2026-0002))
- [`conditional`] 重建先验可以改善ACE系场景坐标回归而不增加查询时延，但当前证据主要限于室内，户外需要重新设计深度分布与扩散先验数据。 ([2510.12387](https://arxiv.org/abs/2510.12387) / [EA-VLOC-2026-0003](evidence-appendix.md#ea-vloc-2026-0003))
- [`conditional`] 训练免费的相似度分布不确定性可作为VPR错误匹配拒绝器，但在极端重复场景中，仅看分数仍可能失效，需要几何线索补充。 ([2510.13464](https://arxiv.org/abs/2510.13464) / [EA-VLOC-2026-0004](evidence-appendix.md#ea-vloc-2026-0004))
- [`conditional`] 现代VPR不存在单一最优骨干：ViT更适合强感知别名和缺帧，CNN在实时系统中通常提供更好的检索质量—运行时间折中。 ([2603.13917](https://arxiv.org/abs/2603.13917) / [EA-VLOC-2026-0007](evidence-appendix.md#ea-vloc-2026-0007))
- [`limit`] 视觉定位评测的真值定义会显著改变结论：仅按相机位置接近判正，会在地形起伏或高度变化大时系统性高估VPR表现。 ([2603.04056](https://arxiv.org/abs/2603.04056) / [EA-VLOC-2026-0006](evidence-appendix.md#ea-vloc-2026-0006))
- [`limit`] 3DGS位姿细化不是全局纠错器：它高度依赖初始位姿质量，单一错误Top-1检索即使视觉相似也可能从场景错误一侧开始，局部细化难以恢复。 ([2603.16538](https://arxiv.org/abs/2603.16538) / [EA-VLOC-2026-0008](evidence-appendix.md#ea-vloc-2026-0008))
- [`limit`] VPR基准接近饱和时，固定地理半径标签本身会成为主要误差源：25米阈值可能忽略真实视觉重叠，使方法排名与可用定位不一致。 ([2604.22390](https://arxiv.org/abs/2604.22390) / [EA-VLOC-2026-0009](evidence-appendix.md#ea-vloc-2026-0009))
- [`limit`] 3DGS地图的照片真实度不等于定位几何可用性：冗余高斯及像素到高斯的多对一对应会削弱匹配鲁棒性并使PnP收敛不稳。 ([2605.07351](https://arxiv.org/abs/2605.07351) / [EA-VLOC-2026-0010](evidence-appendix.md#ea-vloc-2026-0010))
- [`limit`] 把场景存进SCR网络权重并不天然保护隐私：在可发出代理查询并读取三维预测时，攻击者能够聚合恢复场景几何和外观线索。 ([2606.31164](https://arxiv.org/abs/2606.31164) / [EA-VLOC-2026-0014](evidence-appendix.md#ea-vloc-2026-0014))

### EA-SENSOR (4 events)
- [`support`] 在森林VPR中，把深度几何蒸馏进外观描述子可同时改善同序列与跨序列识别，说明几何先验是缓解重复纹理的一条有效方向。 ([2606.13206](https://arxiv.org/abs/2606.13206) / [EA-VLOC-2026-0013](evidence-appendix.md#ea-vloc-2026-0013))
- [`conditional`] 多参考地点表示的收益具有分布条件：参考遍历覆盖查询变化时，判别压缩有效；极端视角且视觉重叠很少时，保留各参考描述子的策略更稳。 ([2605.30769](https://arxiv.org/abs/2605.30769) / [EA-VLOC-2026-0012](evidence-appendix.md#ea-vloc-2026-0012))
- [`conditional`] VPR正在从平均召回转向地理分布鲁棒性，但现有长尾建模仍主要按地理类样本数划分，尚不能代表地点本身的视觉难度。 ([2607.00090](https://arxiv.org/abs/2607.00090) / [EA-VLOC-2026-0015](evidence-appendix.md#ea-vloc-2026-0015))
- [`limit`] 跨条件VPR的安全性必须与覆盖率一起评估：重复且无信息的景观中，校准验证器可以靠全局拒识维持安全，但定位效用降为零。 ([2605.28048](https://arxiv.org/abs/2605.28048) / [EA-VLOC-2026-0011](evidence-appendix.md#ea-vloc-2026-0011))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` 3DGS特征场可把渲染和特征学习接入位姿细化，但定位可靠性仍受底层3DGS几何质量约束，弱纹理平坦场景会直接拖累结果。 ([2507.23569](https://arxiv.org/abs/2507.23569) / [EA-VLOC-2026-0001](evidence-appendix.md#ea-vloc-2026-0001))
- `conditional` 前馈式稀疏特征地图能把逐场景地图准备降到检索级别，但这一优势仍依赖选到相关参考图像；随机或均匀选择会导致准确率下降。 ([2510.00978](https://arxiv.org/abs/2510.00978) / [EA-VLOC-2026-0002](evidence-appendix.md#ea-vloc-2026-0002))
- `conditional` 重建先验可以改善ACE系场景坐标回归而不增加查询时延，但当前证据主要限于室内，户外需要重新设计深度分布与扩散先验数据。 ([2510.12387](https://arxiv.org/abs/2510.12387) / [EA-VLOC-2026-0003](evidence-appendix.md#ea-vloc-2026-0003))
- `conditional` 训练免费的相似度分布不确定性可作为VPR错误匹配拒绝器，但在极端重复场景中，仅看分数仍可能失效，需要几何线索补充。 ([2510.13464](https://arxiv.org/abs/2510.13464) / [EA-VLOC-2026-0004](evidence-appendix.md#ea-vloc-2026-0004))
- `conditional` 现代VPR不存在单一最优骨干：ViT更适合强感知别名和缺帧，CNN在实时系统中通常提供更好的检索质量—运行时间折中。 ([2603.13917](https://arxiv.org/abs/2603.13917) / [EA-VLOC-2026-0007](evidence-appendix.md#ea-vloc-2026-0007))
- `limit` 视觉定位评测的真值定义会显著改变结论：仅按相机位置接近判正，会在地形起伏或高度变化大时系统性高估VPR表现。 ([2603.04056](https://arxiv.org/abs/2603.04056) / [EA-VLOC-2026-0006](evidence-appendix.md#ea-vloc-2026-0006))
- `limit` 3DGS位姿细化不是全局纠错器：它高度依赖初始位姿质量，单一错误Top-1检索即使视觉相似也可能从场景错误一侧开始，局部细化难以恢复。 ([2603.16538](https://arxiv.org/abs/2603.16538) / [EA-VLOC-2026-0008](evidence-appendix.md#ea-vloc-2026-0008))
- `limit` VPR基准接近饱和时，固定地理半径标签本身会成为主要误差源：25米阈值可能忽略真实视觉重叠，使方法排名与可用定位不一致。 ([2604.22390](https://arxiv.org/abs/2604.22390) / [EA-VLOC-2026-0009](evidence-appendix.md#ea-vloc-2026-0009))
- `limit` 3DGS地图的照片真实度不等于定位几何可用性：冗余高斯及像素到高斯的多对一对应会削弱匹配鲁棒性并使PnP收敛不稳。 ([2605.07351](https://arxiv.org/abs/2605.07351) / [EA-VLOC-2026-0010](evidence-appendix.md#ea-vloc-2026-0010))
- `limit` 把场景存进SCR网络权重并不天然保护隐私：在可发出代理查询并读取三维预测时，攻击者能够聚合恢复场景几何和外观线索。 ([2606.31164](https://arxiv.org/abs/2606.31164) / [EA-VLOC-2026-0014](evidence-appendix.md#ea-vloc-2026-0014))
- `conditional` 多参考地点表示的收益具有分布条件：参考遍历覆盖查询变化时，判别压缩有效；极端视角且视觉重叠很少时，保留各参考描述子的策略更稳。 ([2605.30769](https://arxiv.org/abs/2605.30769) / [EA-VLOC-2026-0012](evidence-appendix.md#ea-vloc-2026-0012))
- `conditional` VPR正在从平均召回转向地理分布鲁棒性，但现有长尾建模仍主要按地理类样本数划分，尚不能代表地点本身的视觉难度。 ([2607.00090](https://arxiv.org/abs/2607.00090) / [EA-VLOC-2026-0015](evidence-appendix.md#ea-vloc-2026-0015))
- `limit` 跨条件VPR的安全性必须与覆盖率一起评估：重复且无信息的景观中，校准验证器可以靠全局拒识维持安全，但定位效用降为零。 ([2605.28048](https://arxiv.org/abs/2605.28048) / [EA-VLOC-2026-0011](evidence-appendix.md#ea-vloc-2026-0011))

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
