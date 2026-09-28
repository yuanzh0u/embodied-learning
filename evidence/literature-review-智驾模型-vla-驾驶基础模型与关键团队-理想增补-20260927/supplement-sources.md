# 补充来源：工业披露、项目与人员

核查日：2026-09-27。来源记录与论文证据分开。

## IND-TESLA-2023

[CVPR 2023 workshop agenda](https://opendrivelab.com/cvpr2023/workshop/) · 2023-06-18

定位：Schedule: 09:45; Speakers: Phil Duan

演讲题为 Building Vision Foundation Models for Autonomous Driving；报告人 Phil Duan，议程列 Autopilot Vision Lead。

边界：只能证实演讲主题、日期与当时职衔，不能从题目推出具体架构。

## IND-TESLA-2026

[Tesla x CVPR 2026](https://www.tesla.com/hr_hr/event/tesla-x-cvpr-2026) · 2026-06-03

定位：Workshop Talk: 两场演讲及 Booth Highlights

Ashok Elluswamy，VP AI Software，报告多模态 pixels-to-actuation 模型的数据、训练和评测方法。；Phil Duan，Director of Engineering，报告端到端 driving policy 和车队数据筛选。；页面将 video generation 展示与 FSD end-to-end driving models 分列。

边界：页面是官方议程摘要，并非完整技术报告。演示标签 V14.2 只属于该活动页面，不当作截止日最新版本；未披露语言参与、骨干、动作编码、损失和具体模型规模。

## IND-TESLA-Q1-2026

[Tesla Q1 2026 Update / 8-K exhibit 99.1](https://ir.tesla.com/_flysystem/s3/sec/000162828026026551/tsla-20260422-gen.pdf) · 2026-04-22

定位：PDF physical page 11 (zero-based 10), report page 8, AI & Software

企业披露 FSD v14.3 于四月发布，更新 RL 训练阶段、视觉编码器、编译器和运行时。

边界：未披露可复核 RL 算法、奖励或训练数据；推理延迟改善是企业自报，本综述不据此宣称安全或独立效率优势。

## ORG-PHIL-DUAN

[Phil Duan personal homepage](https://www.philduan.com/) · undated; accessed 2026-09-27

定位：Biography paragraphs 1–2

本人称现任 Tesla AI Director of Engineering；带领 Robotaxi launch 和 FSD v14 AI development，此前共同牵头 v12/v13，并负责过数据、感知及 Occupancy Network。

边界：公开自述而非逐模块贡献审计；保留版本区分。

## IND-WAYMO-2025

[Demonstrably Safe AI For Autonomous Driving](https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving/) · 2025-12-09

定位：Foundation Model; Teacher to Student; Continuous Improvement

官方描述 sensor fusion encoder 与 Gemini-trained driving VLM 的快慢架构；world decoder 接收两者表征。；共享基础模型支持 Driver、Simulator、Critic；存在教师学生蒸馏与车端轨迹验证层。；官方描述仿真强化学习内循环和真实驾驶问题回收、改进、验证的外循环。

边界：企业技术披露；不把安全宣传、运营规模或教师学生配置当作独立验证；EMMA 论文配置不等于完整量产 Driver。

## IND-WAYMO-2026

[10 AI Lessons from Driving 200+ Million Fully Autonomous Miles](https://waymo.com/blog/2026/08/10ailessons/) · 2026-08-26

定位：Sections 3 and 7

官方继续强调较少的大模型、教师学生与快慢推理分工；VLM 提供语义提示，单独存在实时性和空间理解限制。

边界：未给每个车端模型版本的全部参数和可复现实验；文中里程与安全论断不用于跨公司排名。

## ORG-MINGXING-TAN

[DriveX 2026 speaker biography](https://drivex-workshop.github.io/cvpr2026/) · 2026-06-03

定位：Keynote 3: Mingxing Tan, Speaker Bio

议程列 Mingxing Tan 为 Waymo AI Research Director，负责 foundation 和 world models teams。

边界：仅证明活动时公开职衔；截至核查日未找到更新任命，不推断 EMMA 每个模块负责人。

## ORG-JYHJING-HWANG

[Jyh-Jing Hwang homepage](https://jyhjinghwang.github.io/) · undated; accessed 2026-09-27

定位：Opening biography

主页称 Research Scientist and Tech Lead Manager at Waymo Research。

边界：主页自述，无更新时间；研究角色不自动等于 EMMA 全项目负责人。

## ORG-HANG-ZHAO

[Hang Zhao homepage](https://hangzhaomit.github.io/) · undated; accessed 2026-09-27

定位：Opening biography

清华 IIIS 助理教授、MARS Lab PI、Galaxea 共同创始人。

边界：现职与 DriveVLM 发表时清华署名分别记录，不推断 Li Auto 内部分工。

## ORG-KATRIN-RENZ

[Katrin Renz homepage](https://www.katrinrenz.de/) · 2026-02 news; accessed 2026-09-27

定位：Biography; News 01/2026, 02/2026, 02/2024

2026 年一月完成博士答辩，二月宣布创办 physical AI startup；此前 Tübingen AVG 博士及 Wayve LINGO 实习。

边界：页面未在所读段落披露新公司名称；不要继续标成现任 Wayve 员工。

## ORG-ZHIYU-HUANG

[Zhiyu Huang homepage](https://mczhi.github.io/) · 2026-08 news; accessed 2026-09-27

定位：About; News 2026.08

现为 NCSU Assistant Professor、PARIS Lab director；此前 UCLA 博士后及 NVIDIA 实习。

边界：AutoVLA/nuReasoning 的 UCLA 发表署名保留，不回写成 NCSU。

## ORG-ZEWEI-ZHOU

[Zewei Zhou homepage](https://zewei-zhou.github.io/) · 2026-06 news; accessed 2026-09-27

定位：About; News 2026.06

UCLA Mobility Lab 博士生；主页列现 NVIDIA Research 实习及先前 Motional 实习。

边界：实习不是全职转任，不从共同作者推断个人贡献。

## ORG-DINGKANG-LIANG

[Dingkang Liang homepage](https://dk-liang.github.io/) · undated; accessed 2026-09-27

定位：Bio; Selected publications ORION/MindDrive

主页列华中科技大学 Assistant Professor；研究具身智能、三维视觉、世界模型。

边界：ORION 角色另由项目页明确署名，不由当前职位反推。

## ORG-ORION

[ORION project page](https://xiaomi-mlab.github.io/Orion/) · 2025 paper; accessed 2026-09-27

定位：Author block and footnotes

Haoyu Fu、Diankun Zhang、Zongchuang Zhao 等贡献；Dingkang Liang、Hongwei Xie 为 project lead；Xiang Bai 为 corresponding author。；Fu/Zhao 为华科，Zhang 为 Xiaomi EV；Liang 为华科，Xie 为 Xiaomi EV；Fu/Zhao 在小米实习期间完成。

边界：不把整个华科—小米合作作者表等同于单一公司团队；Hongwei Xie 现职以发表时机构为限。

## ORG-JING-GU

[Jing Gu university profile](https://research.tue.nl/en/persons/jing-gu/) · undated; accessed 2026-09-27

定位：Profile affiliation

Eindhoven University of Technology，Electrical Engineering / Mobile Perception Systems Lab，Doctoral Candidate。

边界：按同实验室和姓名结合论文身份；不合并检索中 Philips 同名人物。

## ORG-MARCO-PAVONE

[Marco Pavone Stanford profile](https://profiles.stanford.edu/marco-pavone) · undated; accessed 2026-09-27

定位：Bio; Academic Appointments

斯坦福航空航天副教授；NVIDIA Distinguished Research Scientist，负责自动驾驶研究。

边界：不同网页可能职衔更新不同，此处按指定学校页面记录；Alpamayo 分工以论文 A.1 为准。

## CODE-ALPAMAYO

[Alpamayo official repository](https://github.com/NVlabs/alpamayo) · README accessed 2026-09-27

定位：Updates; Requirements; Relationship with the Paper

AR1 于 CES2026 更名 Alpamayo1；2026-03 发布1.5；训练脚本迁移 alpamayo-recipes。；AR1 仓库给 SFT 权重与推理代码，RL 代码可用但该 release 无 RL 后训练权重；导航/VQA 功能也不全在该 release。

边界：main 是可变入口；本文不下载运行，不把论文全部实验功能当成所发权重功能。

## CODE-ORION-LITE

[Orion-Lite official repository](https://github.com/tue-mps/Orion-Lite) · README accessed 2026-09-27

定位：Links; Supported Features; Results and Checkpoints

当前已给训练、蒸馏采集、闭环评测和 HuggingFace checkpoints 入口。

边界：覆盖论文中的“接收后发布”旧承诺，但本次没有实际安装、下载权重或复跑。

## CODE-DIFFUSIONDRIVE

[DiffusionDrive official repository](https://github.com/hustvl/DiffusionDrive) · README accessed 2026-09-27

定位：Getting Started; Checkpoint

公开训练评测说明，NAVSIM 和 nuScenes 权重入口分列。

边界：不同骨干和数据配置分别标识；demo 不代替正式实车验证。

## CODE-AUTOVLA

[AutoVLA project page](https://autovla.github.io/) · accessed 2026-09-27

定位：Author block; Code/Data links

页面给 Code 链接，Data 标记 Coming Soon；Zhiyu Huang 被列为 project leader。

边界：论文脚注给 corresponding author，项目页给 project leader，分别保留；不把数据发布承诺当已开放。

## CODE-SIMLINGO

[SimLingo official repository](https://github.com/RenzKa/simlingo) · accessed 2026-09-27

定位：README release and setup

公开代码、模型和数据入口。

边界：复现状态是入口核验，不是已执行复现。

## IND-LIAUTO-20F-2025

[Li Auto 2025 Form 20-F](https://ir.lixiang.com/static-files/7f0f559e-1e07-4509-9214-19c5dfc7de92) · 2026-04-10

定位：Autonomous Driving, physical PDF pages 80–81 (zero-based 79–80), printed pages 77–78

企业披露 AD Max 的 VLA、车队数据流程与自研世界模型仿真/RL；M100 在报告时为2026规划。

边界：年度报告可支持公司公开技术方向；没有把 MindVLA-U1、LinkVLA 或各论文检查点逐一映射至量产车型。

## PROJ-MIND-OMNI

[Mind-Omni project family](https://mind-omni.github.io/) · undated; accessed 2026-09-27

定位：Main page: U1, Intent, DIAL, MindSim, AnyScene, MindLabel

项目主页将统一驾驶策略、意图控制、偏好后训练、场景生成与标注工具并列组织。

边界：项目导航不是这些模块已经端到端接通的实验证明。

## PROJ-MINDVLA-U1

[MindVLA-U1 official project](https://mind-omni.github.io/projects/u1/index.html) · undated; accessed 2026-09-27

定位：Title author block and affiliation/role legend

核对MindVLA-U1的作者、机构与明确标注的共同贡献/通信角色。

边界：项目页作者顺序可能与论文不同；发表版本以论文为准，角色仅按显式符号解释。

## PROJ-STREAMING-INTENT

[Streaming Intent official project](https://mind-omni.github.io/projects/intent/index.html) · undated; accessed 2026-09-27

定位：Title author block and affiliation/role legend

核对Streaming Intent的作者、机构与明确标注的共同贡献/通信角色。

边界：项目页作者顺序可能与论文不同；发表版本以论文为准，角色仅按显式符号解释。

## PROJ-DIAL

[DIAL official project](https://mind-omni.github.io/projects/dial/index.html) · undated; accessed 2026-09-27

定位：Title author block and affiliation/role legend

核对DIAL的作者、机构与明确标注的共同贡献/通信角色。

边界：项目页作者顺序可能与论文不同；发表版本以论文为准，角色仅按显式符号解释。

## PROJ-MINDLABEL

[MindLabel](https://mind-omni.github.io/projects/mindlabel/index.html) · undated; accessed 2026-09-27

定位：Pipeline / Research Scope

展示场景问答、意图与多候选动作标注流程；U1主实验只使用基础问答与官方意图。

边界：项目工具的丰富标签不能全部计入U1已验证训练配方；未独立下载复核数据规模。

## CODE-LIAUTO-ORG

[LiAutoAD GitHub organization](https://github.com/LiAutoAD) · undated; accessed 2026-09-27

定位：Organization README / Research

公开组织索引覆盖语言模型、端到端规划、重建和生成仿真方向。

边界：仓库收录及fork不证明独占所有权或具体个人贡献；仅用作候选发现。

## CODE-VLAFLOW

[VLAFlow official code](https://github.com/MindVLA-Team/VLAFlow) · undated; accessed 2026-09-27

定位：README / source tree

提供四种受控预训练范式的实现入口。

边界：源码入口已查看，但不声称全部数据、权重和硬件条件都已复现。

## ORG-KUN-ZHAN

[Kun Zhan personal homepage](https://zhankunliauto.github.io/) · updated 2026-09-14; accessed 2026-09-27

定位：About / Experience / Updates

主页自述为理想基础模型与自动驾驶负责人；列VLA、世界模型/RL、模型系统协同三个方向。

边界：个人公开职衔与方向自述；不把管理职责等同每篇论文实际技术负责人。

## ORG-YAN-XIE

[Yan Xie company biography](https://ir.lixiang.com/management/yan-xie/) · undated; accessed 2026-09-27

定位：Management biography

理想官网列谢炎为CTO，自2022年12月任职。

边界：公开公司职衔不证明对每个模型模块的具体贡献。

## ORG-BENJIN-ZHU

[Benjin Zhu homepage](https://benjin.me/) · undated; accessed 2026-09-27

定位：Biography / Work / News

主页列理想研究任职和清华博士后；2026年5月介绍Mind-Omni工作。

边界：Biography与Work职称文字不同，保留研究任职层级而不强行统一称谓；L4研究不等于L4量产。

## ORG-VICTOR-HUANG

[Victor Shea-Jay Huang homepage](https://jeixhuang.github.io/) · undated; accessed 2026-09-27

定位：Biography / Education

截至核查日主页列2026年8月起CUHK MMLab博士生。

边界：论文理想联合署名不自动证明当前全职雇佣关系。

## ORG-JIFENG-DAI

[Jifeng Dai homepage](https://jifengdai.org/) · undated; accessed 2026-09-27

定位：Biography

主页列清华长聘副教授。

边界：大学合作作者，不按理想员工统计。

## ORG-JUNFEI-ZHOU

[Junfei Zhou homepage](https://jeffreychou777.github.io/) · undated; accessed 2026-09-27

定位：About / Experience / Publications

西南交大硕士阶段；主页列2025年11月起理想实习及AnyScene共同第一作者。

边界：实习与全职关系分别记录；当前信息只截至核查日。
