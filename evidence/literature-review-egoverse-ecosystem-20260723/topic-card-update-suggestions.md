# EgoVerse 结算后的知识库更新建议

本文件只提出更新建议；本轮不直接改写 topic cards，以保留“调查/综述先结算，知识卡再人工吸收”的边界。

## EA-DATA

- 新增 EgoVerse 数据规模与联盟式采集框架。
- 把“规模”与“目标对齐/锚定”拆成两个变量。
- 增加 MimicLabs/DROID 的负向结果：全量数据可能不如目标相关检索。
- 补充数据质量五层链条：采集硬件、感知可观测性、可执行性、选择、采集反馈闭环。

## EA-XEMBODIMENT

- 新增 EgoMimic 动作归一化消融。
- 新增 Emergence 的条件性迁移：模型预训练多样性决定人类数据是否可用。
- 新增 EgoVerse 的 aligned-anchor 机制与跨实验室边界。

## EA-EVAL

- 将跨实验室共享协议写成比单实验室更强、但弱于跨本体普遍泛化的证据层级。
- 强调离线人类动作预测损失必须通过真实机器人 rollout 校准。
- 增加失败、恢复、安全和长期成本指标。

## EA-MODEL

- 新增“模型前置能力 × 人类数据”的交互关系。
- 新增 EgoScale 的预训练—对齐中训练—机器人后训练三阶段配方。
- 把 1k–20k 扩量关系标记为 measured-range result，不外推。

## EA-BIZ

- 增加公司角色词表：数据提供、采集硬件、处理/标注、训练验证、机器人实验、平台基础设施、生态支持。
- 把 consortium member、数据供应商、论文作者、商业客户分开。
- 记录 Scale/Mecka 的数据重处理证据；Meta/Lightwheel 具体角色保持待确认。
- 非论文判断标记为 `industry-observation` 或 `inference`。

## 文献综述目录

- 建议新增 `LR-EGOVERSE`，路由到本 run 的 `run.json`、`review-packet.md`、`paper-note-index.json` 和 `evidence.jsonl`。
