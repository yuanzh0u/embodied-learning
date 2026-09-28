# 主题卡更新建议（本次不直接改写主题卡）

- **EA-MODEL**：增加按语言参与阶段、动作接口与实际部署组件分类的驾驶案例；连接 DriveVLM、EMMA、ORION、AutoVLA、Alpamayo-R1、DiffusionDrive 与 Orion-Lite。Foundation/VLA/world-model 标签允许交叉。Tesla/Waymo 单独引用官方披露 ID，不能绑定伪造的论文事件。
- **EA-ALIGN**：补充 SimLingo 的动作对齐、EMMA 辅助监督消融、Alpamayo 推理—动作一致性奖励；把训练期语言蒸馏与推理期显式语言分开。MindDrive 的交互 PPO 与离线组奖励分开。
- **EA-EVAL**：增加驾驶 VQA、开放环、非反应式仿真、闭环仿真、实车演示的层级边界；特别保留 NAVSIM 初始帧单次策略调用与 SimLingo BASE/完整模型的协议区分。

正式更新时由卡片现有 frontmatter 的 source 字段链接本 run 的 evidence-appendix.md、trace-map.json 和各论文笔记；工业案例链接 industrial-sources.json。本文件是建议，不改变已有知识卡结论。

## 理想增补建议

- **EA-MODEL**：区分DriveVLM系统级分层、LinkVLA离散双向接口和U1共享连续动作；World4Drive的潜在世界选择器与AnyScene/DrivingSphere生成环境不是同一功能。
- **EA-ALIGN**：用Streaming Intent与DIAL说明意图作为候选分布控制变量；补VLAFlow受控比较，但标明机器人证据和驾驶迁移缺项。
- **EA-EVAL**：补RFS留出集选择检查点、ReflectDrive特权未来评分、生成场景非反应性、ME-VLM驾驶QA与策略闭环的边界。
- 工业与人员继续用补充来源稳定ID；不把理想量产VLA直接链接为某篇论文实现，也不从作者位置推定负责人。
