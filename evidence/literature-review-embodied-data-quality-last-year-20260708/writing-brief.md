# Writing Brief: 近一年已发表论文中的具身智能数据质量

> 本文件是写作输入,不是交付物。三篇成稿由 LLM 依此撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。

## 范围

- Topic: 近一年已发表论文中的具身智能数据质量
- Time range: 2025-07-08..2026-07-08
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-MODEL`, `EA-EVAL`
- Paper-level sources: 12 / 5 (formal-ready)
- Accepted events: 12

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-DATA`: 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001)) ⟷ 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 ([EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004))
- `EA-DATA`: 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002)) ⟷ 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))
- `EA-DATA`: 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003)) ⟷ 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- `EA-DATA`: 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([EA-DATA-2026-LY-0005](evidence-appendix.md#ea-data-2026-ly-0005)) ⟷ VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([EA-DATA-2026-LY-0010](evidence-appendix.md#ea-data-2026-ly-0010))
- `EA-DATA`: 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([EA-DATA-2026-LY-0007](evidence-appendix.md#ea-data-2026-ly-0007)) ⟷ 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 ([EA-DATA-2026-LY-0012](evidence-appendix.md#ea-data-2026-ly-0012))
- `EA-DATA`: 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 ([EA-DATA-2026-LY-0009](evidence-appendix.md#ea-data-2026-ly-0009)) ⟷ 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 ([EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004))
- `EA-DATA`: 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([EA-DATA-2026-LY-0011](evidence-appendix.md#ea-data-2026-ly-0011)) ⟷ 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-DATA (12 events)
- [`support`] 少样本部署场景下，外部大规模数据的“质量”主要取决于对目标任务分布的相关性；只按最近邻相似度检索会受噪声和先验数据分布偏差影响。 ([EA-DATA-2026-LY-0007](evidence-appendix.md#ea-data-2026-ly-0007))
- [`support`] 跨本体机器人数据的质量问题不只是轨迹数量，而是本体/夹爪分布是否均衡；高度不平衡的数据集会让策略过拟合少数 robot-scene 组合。 ([EA-DATA-2026-LY-0011](evidence-appendix.md#ea-data-2026-ly-0011))
- [`support`] 示教数据质量不应只用相似度、互信息或人工启发式代理指标定义；QoQ 将高质量轨迹定义为对目标验证示范 loss 降低和策略性能提升有直接贡献的数据。 ([EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001))
- [`support`] 示教数据质量会被采集硬件本身塑形；UMI 类手持 gripper 的力分布、重量和人体工学会影响任务表现、操作者负担和后续可学习策略。 ([EA-DATA-2026-LY-0009](evidence-appendix.md#ea-data-2026-ly-0009))
- [`support`] 面向部署环境的 end-user 示教，低质量常表现为过度纠正、振荡和突兀调整；轨迹功率谱密度 PSD 可作为无需 rollout、专家标签或重新训练的快速质量排序指标。 ([EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003))
- [`support`] 遥操作 episode 不能只按成功/失败验收；数据质量需要结合语义任务进度、运动平滑性、停顿、关节极限等遥测信号，并把反馈闭环给采集员。 ([EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002))
- [`support`] 在多任务 VLA 微调中，数据质量治理要同时考虑样本效用和任务覆盖；单一全局排序会让某些任务被几乎淘汰，导致任务级覆盖坍缩。 ([EA-DATA-2026-LY-0005](evidence-appendix.md#ea-data-2026-ly-0005))
- [`conditional`] VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([EA-DATA-2026-LY-0010](evidence-appendix.md#ea-data-2026-ly-0010))
- [`conditional`] 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- [`conditional`] 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 ([EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004))
- [`conditional`] 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 ([EA-DATA-2026-LY-0012](evidence-appendix.md#ea-data-2026-ly-0012))
- [`conditional`] 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` VR 示教质量依赖交互模态和视觉表示，并且不同任务会偏好不同输入配置；采集系统优化不能只追求沉浸感或视觉保真。 ([EA-DATA-2026-LY-0010](evidence-appendix.md#ea-data-2026-ly-0010))
- `conditional` 人类视频能扩大机器人学习数据来源，但其质量取决于机器人可执行性和任务兼容性；仿真过滤可把不可达、估计错误或 grasp 不兼容的轨迹排除或标注出来。 ([EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008))
- `conditional` 数据多样性是机器人模仿学习质量的一部分，但不能等同于质量本身；多样性最大化在无病态轨迹时有用，遇到有害或对抗性轨迹仍需结合质量筛选。 ([EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004))
- `conditional` 低质量或分布偏移数据并非一次性清洗后消失的问题；随着机器人数据规模扩大，如何有选择地利用 suboptimal data 会成为持续的数据质量治理问题。 ([EA-DATA-2026-LY-0012](evidence-appendix.md#ea-data-2026-ly-0012))
- `conditional` 混合质量的长程示教不应粗粒度整条丢弃；次优 episode 里可能含有高价值恢复片段，质量控制需要下探到 frame/chunk 级别的进展信号。 ([EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006))

## 三种风格的读者与语气

- `scientific-memo_keyan.md` 研究者读:中心论点 → 派生矛盾/机制(prose 小节) → 可操作框架 → 最短结论。引用密集,每个实质论断带 event 链接。
- `zhihu-explainer_zhihu.md` 技术公众读:先破一个具体误区 → 讲机制(用比喻可以,升级 stance 不可以) → 给适用边界 → 延伸阅读。
- `xiaohongshu-post_xiaohongshu.md` 泛兴趣读者:一个钩子 → 3-5 条反常识洞察(每条一句话+链接) → 一句可见的 caveat → 一行来源说明。

## 引用速查

- 事件锚点:`[EA-…-0001](evidence-appendix.md#ea--0001)`(锚 = event_id 小写)。appendix 与成稿同目录。
- 论文链接:`[2606.13877](https://arxiv.org/abs/2606.13877)`。
- 成稿末尾必须有 `## References` 节;完整证据条目在 [evidence-appendix.md](evidence-appendix.md)。
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`
