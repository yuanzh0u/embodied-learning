# 检索、筛选与覆盖边界

本轮为已归档智驾综述的增量扩展：原版本保留，新增理想系列论文专题。窗口2024-09-27至2026-09-27，保留7篇更早前序。沿用scoping阈值100候选、35完整非OCR全文、15正式论文证据，未降低门槛；单科研文体由用户明确指定。

原10批检索的1,672项发现池保留，在其后追加7批公司/机制定向检索，合计1,876项去重发现。**发现池不是1,876篇均经过人工筛选。** 采用目的性选择，结合项目家族、作者、技术接口、评测与反证覆盖。原39篇已恢复全文，新增9篇唯一全文，并把原来只恢复的U1升级为深读证据：最终48篇全文、30篇接纳、18篇仅恢复。

30篇均取得可解析的完整非OCR HTML，阅读问题、方法、关键实验/消融与限制及必要附录；不声称逐项复核全部图表和引用。新增10篇有笔记及20条审计主张，总计66条。原20篇46条复用不改写原run。所有来源固定版本和内容hash见extraction-provenance.json；版本链接不是对当前未固定HTML永久不变的承诺。

领域八篇核心工作保留：DriveVLM、EMMA、ORION、SimLingo、AutoVLA、Alpamayo-R1、Orion-Lite、DiffusionDrive。理想专题另以U1、Streaming Intent、DIAL作为连读中心，加入LinkVLA、ReflectDrive两种接口/约束对照，World4Drive、DrivingSphere、AnyScene补世界与数据，VLAFlow补机器人预训练机制，ME-VLM补驾驶理解与端侧底座。专题选篇不等于按品牌重排整个领域。

VLAFlow没有智驾实验，仅是用户新增要求下的相邻训练机制研究；不把机器人结果当驾驶增益。ME-VLM驾驶部分属于理解评测。MindLabel和MindSim不伪装成独立论文。其余发现项及未接受的理论/重建延伸见liauto-project-selection.json。

增量批次1—7的新增率依次为25/46、69/89、68/196、39/104、3/17、0/51、0/5。最后两批为不同作者/机制交集及底座家族核查，满足预先阈值，但这种局部查询饱和**不说明理想全部论文或整个智驾领域已经穷尽**。前面的宽查询仍发现大量新项，未伪称完成逐项排除。覆盖报告分别保留候选、全文、接纳、维度、饱和五项检查。

前一版实际API引文边保留citation-graph.json；新增原文提及与继承检查在liauto-citation-checks.json。只有DIAL原文明确基于U1等有实据关系可称技术继承；共同作者、方法相似和引用均不自动构成继承。

| 证据问题 | 原主线 | 理想增补 |
|---|---|---|
| 语言理解与决策 | LingoQA、DriveLM、EMMA | ME-VLM驾驶QA、Streaming Intent |
| 动作接口 | ORION、AutoVLA、Alpamayo | U1、LinkVLA |
| 训练监督与反馈 | DiMA、SimLingo、nuReasoning、MindDrive | DIAL、ReflectDrive、VLAFlow（机器人） |
| 世界表征与仿真 | 按需对照，不做世界模型全综述 | World4Drive、DrivingSphere、AnyScene |
| 评测反证 | NAVSIM、AD-MLP、忠实性审计 | 特权安全评分、开放环RFS、小留出集、非反应主体等边界 |

Tesla、Waymo、理想是3个单独工业案例，不抵扣论文门槛。工业/项目/人员来源逐项登记于supplement-sources.json。Tesla两条视频未恢复逐字稿；理想研究检查点到量产车型的映射未披露；缺项保留，不从相邻论文补猜。未运行模型复现实验。
