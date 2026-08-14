# LeWorldModel 技术谱系综述范围

## 用户输入

- 原始材料：`D:\Worksapce\hunter\docs\summaries\2026-07-24-li-wei-mentioned-models.md`
- 初始要求：按本仓库的知识与证据流程，系统梳理材料中的技术点。
- 范围调整：用户随后明确要求“主要是 LeWorldModel 这条线”。

原始材料属于访谈摘要与模型名称校准线索，不是论文级证据。其关于 LeWM
“高效、轻量、已经发布数月”等描述只用于形成研究问题；正式主张必须回到完整论文、
paper note、claim-support audit 与 accepted evidence。

## 主问题

LeWorldModel 如何把从像素学习的 JEPA 表征、动作条件潜空间动力学和在线规划连接成
可控闭环？它所谓的稳定、端到端、轻量和快规划分别由什么机制与实验支持，又在哪些
条件下会被潜空间几何、长程 rollout、目标代价或搜索分布失配所削弱？

## 技术主链

```text
pixels / video
  → predictive embedding / JEPA
  → anti-collapse regularization
  → action-conditioned latent dynamics
  → multi-step rollout
  → latent goal / cost
  → online search or amortized planning
  → receding-horizon control
  → closed-loop and decision-utility evaluation
```

## 子问题

1. LeWM 的 end-to-end from pixels 是否完全不依赖冻结视觉 backbone、EMA 或辅助监督？
2. SIGReg 如何防止坍塌；各向同性高斯先验是否会扭曲低维任务流形？
3. 训练目标是一阶预测还是多步预测；规划时 rollout 与训练 horizon 是否失配？
4. 动作怎样进入 predictor；潜状态是否区分不同动作后果？
5. 欧氏 latent distance 是否真的表示有限动作预算下的可达性与任务进度？
6. CEM/MPC 的计算成本来自哪里；前缀预测、可变长度预测或逆动力学能否减少搜索？
7. “快”比较的是模型前向、整次规划、每个控制周期还是任务总时长？
8. “稳定”比较的是不坍塌、损失曲线、跨 seed 方差还是超参数鲁棒性？
9. 预测误差、动作排序与闭环成功之间是否一致；何时会出现 predictive but not plannable？
10. 结论是否只在二维/仿真控制任务成立，还是已有真实机器人、长程和接触任务证据？

## 纳入边界

- 发现窗口：2026-01-24 至 2026-07-24。
- 指名基础论文可早于窗口纳入背景或机制证据，例如 LeJEPA、V-JEPA 2、DINO-WM、PLDM。
- 新正式证据只接受完整、可解析、非 OCR 全文。
- 每篇 accepted 论文必须有 validated paper note、精确 locator、通过的 claim-support audit。
- 既有证据只复用 catalog 指定的当前 reader-v2 / settled run。

## 降级主题

- V-JEPA 2：作为视频 JEPA 与动作适配的前序，不另做完整模型综述。
- DINOv3 / DINO-WM：只用于冻结通用表征与端到端任务表征的边界对照。
- MoE、Unified/One Model、VLA、强化学习：仅在解释系统接口或规划背景时出现，不占主轴。
- 无法可靠还原的 ASR 词（如“solar 策略”“V 二”）不进入证据图谱。

## 预期判断框架

最终不按论文顺序罗列，而按五个可证伪命题组织：

1. **训练稳定性**：简单的预测损失加分布正则能否稳定学到非坍塌潜空间。
2. **动作敏感性**：可预测表征是否同时保留控制相关、尤其是外生但任务相关的信息。
3. **长程动力学**：一步预测能否支持长时域 rollout，误差如何累积。
4. **规划接口**：latent distance、可达性、层级子目标与在线搜索是否匹配。
5. **系统效用**：参数量与规划速度优势能否转化为闭环成功、可靠性和部署价值。
