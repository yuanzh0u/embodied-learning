# Source Entry Draft: 近一年已发表论文中的具身智能数据质量

> 待需要时并入 `knowledge/sources.md`。本 draft 覆盖本次 run 中进入 accepted evidence 的 12 篇论文。

## S-ARXIV-2509.01657

- 文件/链接：[Data Retrieval with Importance Weights for Few-Shot Imitation Learning](https://arxiv.org/abs/2509.01657)
- 类型：论文 / arXiv
- 时间标记：published 2025-09-01; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：目标任务分布相关性、retrieval-based imitation learning、few-shot deployment data selection；见 `EA-DATA-2026-LY-0007`
- 适用：需要复核外部大规模数据如何按目标任务相关性进入少样本模仿学习时读取。

## S-ARXIV-2512.13100

- 文件/链接：[OXE-AugE: A Large-Scale Robot Augmentation of OXE for Scaling Cross-Embodiment Policy Learning](https://arxiv.org/abs/2512.13100)
- 类型：论文 / arXiv
- 时间标记：published 2025-12-15; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：跨本体数据均衡、机器人/夹爪分布、OXE 数据扩增；见 `EA-DATA-2026-LY-0011`
- 适用：需要复核跨本体数据质量、dataset imbalance 与 augmentation 对泛化影响时读取。

## S-ARXIV-2602.10618

- 文件/链接：[From Interaction to Demonstration Quality in Virtual Reality: Effects of Interaction Modality and Visual Representation on Everyday Tasks](https://arxiv.org/abs/2602.10618)
- 类型：论文 / arXiv
- 时间标记：published 2026-02-11; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：VR 采集接口、输入模态、轨迹效率、示教质量；见 `EA-DATA-2026-LY-0010`
- 适用：需要复核 VR 示教质量与交互设备选择时读取。

## S-ARXIV-2602.13197

- 文件/链接：[Imitating What Works: Simulation-Filtered Modular Policy Learning from Human Videos](https://arxiv.org/abs/2602.13197)
- 类型：论文 / arXiv
- 时间标记：published 2026-02-13; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：人类视频到机器人数据、仿真过滤、可执行性和 grasp 兼容性；见 `EA-DATA-2026-LY-0008`
- 适用：需要复核 L0 human-video 数据进入机器人策略学习前的质量过滤时读取。

## S-ARXIV-2603.09056

- 文件/链接：[Quality over Quantity: Demonstration Curation via Influence Functions for Data-Centric Robot Learning](https://arxiv.org/abs/2603.09056)
- 类型：论文 / arXiv
- 时间标记：published 2026-03-10; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：influence-function curation、target-conditioned utility、DROID in-the-wild 数据筛选；见 `EA-DATA-2026-LY-0001`
- 适用：需要复核“数据质量 = 对目标策略性能贡献”这一操作化定义时读取。

## S-ARXIV-2603.11634

- 文件/链接：[Diversity You Can Actually Measure: A Fast, Model-Free Diversity Metric for Robotics Datasets](https://arxiv.org/abs/2603.11634)
- 类型：论文 / arXiv
- 时间标记：published 2026-03-12; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：trajectory entropy、多样性度量、FAKTUAL 数据筛选边界；见 `EA-DATA-2026-LY-0004`
- 适用：需要复核多样性与质量的关系、以及 diversity-aware curation 的适用边界时读取。

## S-ARXIV-2603.17189

- 文件/链接：[Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)
- 类型：论文 / arXiv
- 时间标记：published 2026-03-17; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：UMI gripper、采集硬件人体工学、示教质量；见 `EA-DATA-2026-LY-0009`
- 适用：需要复核采集硬件如何塑形示教质量时读取。

## S-ARXIV-2605.01544

- 文件/链接：[An Efficient Metric for Data Quality Measurement in Imitation Learning](https://arxiv.org/abs/2605.01544)
- 类型：论文 / arXiv
- 时间标记：published 2026-05-02; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：PSD data-quality metric、end-user demonstrations、trajectory smoothness；见 `EA-DATA-2026-LY-0003`
- 适用：需要复核无需 rollout/专家标签的快速示教质量度量时读取。

## S-ARXIV-2605.26349

- 文件/链接：[Closing the Loop in Teleoperation: Episode-Level Data Quality Assessment and Feedback for High-Quality Demonstration Collection](https://arxiv.org/abs/2605.26349)
- 类型：论文 / arXiv
- 时间标记：published 2026-05-25; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：teleoperation DQAF、episode-level quality score、采集员反馈闭环；见 `EA-DATA-2026-LY-0002`
- 适用：需要复核遥操作采集质量评估和采集员反馈系统时读取。

## S-ARXIV-2606.12365

- 文件/链接：[Ambient Diffusion Policy: Imitation Learning from Suboptimal Data in Robotics](https://arxiv.org/abs/2606.12365)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-10; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：suboptimal/OOD data、noise-dependent data usage、过滤与利用的取舍；见 `EA-DATA-2026-LY-0012`
- 适用：需要复核低质量或分布偏移数据如何进入 diffusion-policy training 时读取。

## S-ARXIV-2606.16208

- 文件/链接：[ATHENA: Accelerated Multi-Task Heterogeneous Influence Functions for Robot Data Curation](https://arxiv.org/abs/2606.16208)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-15; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：多任务 VLA data curation、任务覆盖、防止全局排序造成 coverage collapse；见 `EA-DATA-2026-LY-0005`
- 适用：需要复核多任务 VLA 微调中的数据效用与任务均衡时读取。

## S-ARXIV-2606.28320

- 文件/链接：[WARP-RM: A Warp-Augmented Relative Progress Reward Model for Data Curation](https://arxiv.org/abs/2606.28320)
- 类型：论文 / arXiv
- 时间标记：published 2026-06-26; retrieved 2026-07-08
- 可信等级：primary
- 主题范围：
  - EA-DATA：frame/chunk-level data curation、suboptimal teleoperation、progress reward；见 `EA-DATA-2026-LY-0006`
- 适用：需要复核混合质量长程示教中片段级筛选与恢复行为利用时读取。
