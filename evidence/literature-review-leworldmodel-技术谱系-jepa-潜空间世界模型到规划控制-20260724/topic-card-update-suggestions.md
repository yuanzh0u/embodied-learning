# EA-MODEL / EA-EVAL / EA-4D 更新建议（未直接修改主题卡）

> 证据白名单：仅使用当前 run 的 `evidence-new/*.jsonl` 与 `reused-evidence.jsonl`。
>
> 规模：24 篇不重复论文、76 条已审核事件。访谈摘要只承担 `industry observation` 角色，不支持下列技术 claim。
>
> `inference: 是` 表示建议文本是跨事件综合或从结果推导出的知识卡级判断；`inference: 否` 表示基本保持单篇已审核事件的直接结论。所有建议仍须保留列出的适用边界。

## EA-MODEL：模型与预训练

### EA-MODEL-S1：把观察预训练与动作条件后训练拆开

- 建议 claim：从大规模观察视频获得可预测视觉表征，不等同于获得动作因果模型。V-JEPA 2 与 DreamDojo 路线都把观察预训练作为第一阶段，规划或控制能力还需要带机器人动作/状态的 action-conditioned post-training。
- 支持 event IDs：`EA-LEWM-READ-0081`、`EA-LEWM-READ-0082`、`EA-JIMFAN-READ-0015`、`EA-WMEVAL-READ-0013`
- 适用边界：直接证据来自 V-JEPA 2/V-JEPA 2-AC、DreamDojo 和接触操作讨论；不能据此声称所有观察预训练都必须采用同一种后训练结构，也不能把后训练后的控制结果归因给无动作视频阶段本身。
- inference：是（跨论文阶段划分综合）

### EA-MODEL-S2：可预测、稳定或各向同性，不自动等于可规划

- 建议 claim：世界模型潜空间除了稳定和可预测，还必须让不同动作产生可辨识的局部位移，并让目标代价反映有限时域可达性；动作差分解码、预算条件可达性和轨迹匹配度量分别修复了这一链路的不同环节。
- 支持 event IDs：`EA-LEWM-READ-0002`、`EA-LEWM-READ-0003`、`EA-LEWM-READ-0041`、`EA-LEWM-READ-0043`、`EA-LEWM-READ-0046`、`EA-LEWM-READ-0047`、`EA-LEWM-READ-0048`、`EA-LEWM-READ-0061`、`EA-LEWM-READ-0063`、`EA-LEWM-READ-0064`
- 适用边界：最强消融主要来自 stable-worldmodel 系列、TwoRoom、Wall、Push-T 等模拟协议；可达性标签仍依赖轨迹覆盖，动作敏感也不是任务成功的充分条件。
- inference：是（把表示正则、局部动作几何、目标度量与规划器串成机制链）

### EA-MODEL-S3：semantic latent 的优势是有条件的

- 建议 claim：在 Bridge V2 的受控 action-conditioned LDM 比较中，semantic latent 家族在策略内环成功、OOD 成功、CEM 动作恢复和潜变量任务信息上整体优于 reconstruction-aligned 家族；但 semantic latent 仍可能损失几何与接触精度，压缩适配器也可能牺牲精细控制几何。
- 支持 event IDs：`EA-LEWM-READ-0087`、`EA-LEWM-READ-0088`、`EA-LEWM-READ-0089`、`EA-LEWM-READ-0090`、`EA-LEWM-READ-0091`、`EA-LEWM-READ-0092`、`EA-LEWM-READ-0093`
- 适用边界：限定于 Bridge V2、共享 WidowX 本体、论文所测编码器与 DiT 协议；策略成功来自生成 rollout 内的固定 VLA 与部分 VLM 判断。不得扩展为 DINOv3 或任一单独编码器的通用排名。
- inference：是（同一受控研究的多轴结果综合）

### EA-MODEL-S4：预测目标可能系统性漏掉控制相关状态

- 建议 claim：若一个控制相关特征在时间上不可预测，纯 reward-free latent self-prediction 可能没有保留它的训练信号；单纯增加潜变量容量未必修复这种目标层遗漏。
- 支持 event IDs：`EA-LEWM-READ-0067`、`EA-LEWM-READ-0068`、`EA-LEWM-READ-0069`、`EA-LEWM-READ-0070`、`EA-LEWM-READ-0071`、`EA-LEWM-READ-0072`
- 适用边界：机制证据来自小型合成环境，尚未在大型预训练模型、标准机器人基准或真实数据上验证；应写成风险机制而非已证实的大模型普遍失败。
- inference：否（直接限制性证据的保守归纳）

### EA-MODEL-S5：LeJEPA 是表征学习前序，不是控制证据

- 建议 claim：LeJEPA 用 SIGReg 与多视图预测简化自监督训练并提供表征层理论与小模型验证；这些结果可解释 LeWorldModel 的正则化来源，但不能替代 action-conditioned dynamics、rollout、规划和闭环控制验证。
- 支持 event IDs：`EA-LEWM-READ-0026`、`EA-LEWM-READ-0027`、`EA-LEWM-READ-0028`、`EA-LEWM-READ-0029`、`EA-LEWM-READ-0030`、`EA-LEWM-READ-0031`、`EA-LEWM-READ-0001`、`EA-LEWM-READ-0002`
- 适用边界：LeJEPA 的主要实证是 ImageNet-10 冻结表征与小模型架构；从表征理论迁移到动作条件世界模型属于待验证步骤。
- inference：是（技术谱系连接）

## EA-EVAL：评测体系与世界模型

### EA-EVAL-S1：世界模型评估不能以视觉保真为唯一主轴

- 建议 claim：机器人世界模型至少要联合评估动作跟随、物理遵从、乐观偏差、长时程一致性、策略或规划效用以及推理效率；像素质量可以保留，但不能作为控制可用性的充分代理。
- 支持 event IDs：`EA-WMEVAL-READ-0004`、`EA-WMEVAL-READ-0010`、`EA-LEWM-READ-0088`、`EA-LEWM-READ-0089`、`EA-LEWM-READ-0090`
- 适用边界：不同论文的指标与数据集尚未形成统一标尺；家族级 Bridge V2 结果、MiraBench 评估主张和 WEAVER 的系统要求应作为互补维度，而非直接合并成单一总分。
- inference：是（跨评测框架综合）

### EA-EVAL-S2：评估时分离“表征—动力学—规划器”三层

- 建议 claim：诊断潜世界模型时，应分别测量编码器保留了多少动作/任务信息、生成动力学损失了多少信息，以及 planner/terminal selector 是否使用了正确的可达性度量；只报告最终成功率会掩盖故障层。
- 支持 event IDs：`EA-LEWM-READ-0089`、`EA-LEWM-READ-0043`、`EA-LEWM-READ-0046`、`EA-LEWM-READ-0047`、`EA-LEWM-READ-0048`、`EA-LEWM-READ-0063`
- 适用边界：IDM 与成功分类是探针，TRM/RC-aux 消融主要来自有限模拟协议；三层诊断框架需要在真实机器人上继续校准。
- inference：是（由多篇消融抽象出的评估分层）

### EA-EVAL-S3：生成 rollout 内的策略成功仍是代理指标

- 建议 claim：用世界模型 rollout 运行策略可用于低成本比较，但必须报告与真实结果的相关性、评估器偏差和 sim-real 边界；最好以真实机器人闭环结果作为锚点，而非把 VLM 判定的生成成功直接视为部署成功。
- 支持 event IDs：`EA-WMDATA-READ-0007`、`EA-LEWM-READ-0093`、`EA-LEWM-READ-0083`、`EA-LEWM-READ-0084`
- 适用边界：V-JEPA 2-AC 的真实部署只覆盖同类 Franka 与有限任务；Bridge V2 semantic-latent 研究没有逐模型真实机器人重放，二者不能直接横向排名。
- inference：是（把代理评估限制与真实部署锚点结合）

### EA-EVAL-S4：长时程评估必须区分 oracle subgoal 与生成 subgoal

- 建议 claim：层级结构本身不能证明长时程能力。评估应分别报告 oracle/轨迹内 subgoal、模型生成 subgoal、支持约束搜索、执行时重新规划和不同时间抽象尺度，否则容易把子目标可执行性与子目标生成能力混为一谈。
- 支持 event IDs：`EA-LEWM-READ-0051`、`EA-LEWM-READ-0052`、`EA-LEWM-READ-0053`、`EA-LEWM-READ-0054`、`EA-LEWM-READ-0085`、`EA-LEWM-READ-0003`
- 适用边界：Hi-LeWM 主分析集中于 Push-T；V-JEPA 2-AC 的约 16 秒时域和人工图像子目标属于另一部署协议，二者共同支持评估拆分，但不证明同一方法的效果。
- inference：是（跨协议评估要求）

### EA-EVAL-S5：效率指标要分账，并保持任务事件

- 建议 claim：世界模型的加速不能只按帧数、吞吐量或动力学前向时间评价；应把编码、动力学、候选打分、搜索更新和完整规划延迟分账。稀疏或并行预测还必须保留 approach、contact、grasp、release 等任务关键事件，并与闭环成功率共同报告。
- 支持 event IDs：`EA-WMEVAL-READ-0003`、`EA-WMEVAL-READ-0010`、`EA-LEWM-READ-0004`、`EA-LEWM-READ-0008`、`EA-LEWM-READ-0009`、`EA-LEWM-READ-0010`、`EA-LEWM-READ-0012`、`EA-LEWM-READ-0013`、`EA-LEWM-READ-0021`、`EA-LEWM-READ-0022`
- 适用边界：SKIP 的关键帧结论、WEAVER 的效率要求、LeWM/Fast-LeWM/GC-IDM 的规划时间来自不同系统；Fast-LeWM 的 4090/CEM 计时只支持同协议内分账，不能与 LeWM 原论文的绝对时间直接横比。建议作为共同评价原则，不合并跨协议数值。
- inference：是（跨系统效率原则）

## EA-4D：4D 时空推理与世界动态

### EA-4D-S1：4D 动态表征必须对动作差异敏感

- 建议 claim：面向控制的 4D 世界动态不能只描述“场景会怎么变化”，还要让相同历史下的不同动作产生可分离的潜位移；否则视频预测可以看似合理，却无法稳定反演动作或规划。
- 支持 event IDs：`EA-LEWM-READ-0081`、`EA-WMEVAL-READ-0013`、`EA-LEWM-READ-0061`、`EA-LEWM-READ-0062`、`EA-LEWM-READ-0063`、`EA-LEWM-READ-0064`、`EA-LEWM-READ-0065`、`EA-LEWM-READ-0066`
- 适用边界：Delta-JEPA 的动作敏感结果主要来自四个受控环境；动作可分离是必要诊断之一，不是任务控制的充分条件。
- inference：是（把静态/无动作预训练边界与局部动作几何综合）

### EA-4D-S2：几何监督应覆盖当前结构与短期演化

- 建议 claim：RGB 视频可通过 depth、pseudo-3D scene flow 或几何特征蒸馏补充 4D 监督，使世界模型同时表示当前三维结构与动作后的短期演化，而不是只追求二维视频外观。
- 支持 event IDs：`EA-WMDATA-READ-0008`、`EA-WMEVAL-READ-0005`
- 适用边界：直接证据来自 GaussianDream 与 GEM-4D 的特定表示和操作设置；不能推断任意深度或场景流伪标签都会提升闭环控制。
- inference：是（两种几何增强路线的共同抽象）

### EA-4D-S3：接触事件是时空压缩不能丢失的状态转折

- 建议 claim：接触丰富操作的 4D 表征与采样应保留 approach、contact、grasp、release 等稀疏事件，并让视觉—触觉特征同时具备空间结构、时间连续性和跨模态兼容性。
- 支持 event IDs：`EA-WMEVAL-READ-0003`、`EA-TWM-READ-0003`、`EA-TWM-READ-0004`
- 适用边界：触觉证据聚焦接触丰富操作；对无接触导航或纯视觉任务不应默认需要相同模态与事件定义。
- inference：是（关键帧与视觉—触觉证据综合）

### EA-4D-S4：层级时间抽象需要数据支持约束和在线重规划

- 建议 claim：高层 subgoal 或 macro-action 若脱离训练轨迹支持，容易发生时间错位和不可执行；经验 anchor、局部 residual 与在线 constrained replanning 是比无约束连续宏动作搜索更稳健的候选机制。
- 支持 event IDs：`EA-LEWM-READ-0051`、`EA-LEWM-READ-0052`、`EA-LEWM-READ-0053`、`EA-LEWM-READ-0054`、`EA-LEWM-READ-0085`
- 适用边界：正面证据主要在 Push-T 和特定 Hi-LeWM 变体；VQ macro-actions 与更高容量世界模型尚未充分评估，不能写成 hierarchy 的一般结论。
- inference：是（机制性综合）

### EA-4D-S5：视角与动作坐标系属于世界动态接口

- 建议 claim：在未标定单目相机下，如果机器人基座不可见，笛卡尔动作轴可能无法从图像唯一确定；4D 世界模型应显式记录或评估视角—基座—动作坐标关系，而不是默认视觉表征天然具备视角不变的控制几何。
- 支持 event IDs：`EA-LEWM-READ-0083`、`EA-LEWM-READ-0086`
- 适用边界：直接部署证据来自 V-JEPA 2-AC 的固定外部相机和 Franka 设置；“显式记录或评估”是工程建议，尚无该 run 内的对照实验确定最佳校准形式。
- inference：是（由部署限制推导的接口建议）

## 建议的人工合并顺序

1. 先审阅 EA-EVAL-S2 的三层评估框架，它可以作为其余 claim 的共同组织骨架。
2. 再将 EA-MODEL-S1/S2/S3 分别放入“训练阶段”“潜空间目标”“表征家族权衡”。
3. 最后把 EA-4D-S1/S3/S4/S5 放入“动作敏感性—接触事件—时间层级—坐标接口”的动态链。
4. 合并时保留所有 `inference: 是`、任务/本体边界与 event ID；不要把建议文本改写成无条件模型排名。
