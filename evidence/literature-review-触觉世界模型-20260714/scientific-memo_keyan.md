# 触觉世界模型研究备忘录

## 研究边界

本文聚焦“触觉世界模型”：机器人在接触丰富操作中，利用视觉、触觉、力/力矩、动作、语言或机器人状态来预测未来接触演化，并把预测用于规划、策略生成、推理期修正或闭环反射控制。时间范围为 2026 年 1 月 14 日至 7 月 14 日。本次范围综述从 867 条去重候选中核验 124 篇可用全文，并以 23 篇直接相关论文构成证据主干；检索覆盖世界模型、触觉表征、数据采集、控制接口、限制与迁移方向。

候选数量、全文数量、关键维度和连续低新增轮次均满足停止条件。无法取得可核验正文的候选不支撑结论，扫描件明确不在本次探索范围内。

## 核心结论

“触觉世界模型”不是把触觉图像塞进视觉世界模型，而是要建模接触状态如何随动作变化。现有证据显示，真正有用的触觉世界模型至少要同时处理四件事：接触变量表征、时间同步数据、动作条件预测、闭环使用接口；如果只增加一个触觉模态而不解决表征兼容和评测闭环，收益会不稳定（[ContactWorld](https://arxiv.org/abs/2606.13877), [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001)）。

## 问题结构

第一层是感知变量。RGB 看不到接触力、摩擦、滑移、材料和被遮挡局部几何；

本轮论文进一步把这个差异落到世界模型上：Visuo-Tactile World Models 用触觉 grounding 改善物体持续性和物理一致性，TacForeSight 用 wrist force/torque 条件化未来触觉潜在状态，HapTile 还把 marker displacement 作为显式接触几何和滑移线索保存（[相关研究](https://arxiv.org/abs/2602.06001), [相关研究](https://arxiv.org/abs/2606.11184), [相关研究](https://arxiv.org/abs/2606.04825)）。

第二层是表征与预测。ContactWorld 的关键结论是，触觉世界模型的收益依赖表征结构和跨模态兼容；点云和触觉力场组合在其 基准 中给出最强平均规划表现，但真实机器人附录也显示 TacDepth/TacFF 不总是稳定增益，原因包括标定和力推断噪声。Dream-Tac 则说明触觉信号是事件驱动、稀疏且随接触变化突增的，因此使用 contact gate 和 contact-aware attention，而不是把触觉当作持续视觉通道（ , [相关研究](https://arxiv.org/abs/2606.13877), [相关研究](https://arxiv.org/abs/2606.08737)）。

第三层是数据工程。Visuo-Tactile World Models 的小规模但完整数据包括 124 条遥操作演示、约 112k datapoints、8 个接触任务、成功和失败轨迹、本体状态、外部视频与四个 Digit 360 指尖视频；OmniVTA 扩展到 21,879 条轨迹、86 任务、126 对象和多传感器；HapTile 提供 1,726 条演示、38 任务、9 类技能、语言指令、15Hz 同步视觉/触觉/状态/动作；

TAMEn 进一步强调可执行性检查、MoCap/VR 双模式采集和人类介入恢复数据。由此可推断，触觉世界模型的数据需求不是“更多视频”，而是“可同步、可执行、含失败恢复、保留接触几何与力信号”的多模态交互数据（ [相关研究](https://arxiv.org/abs/2602.06001), [相关研究](https://arxiv.org/abs/2603.19201), [相关研究](https://arxiv.org/abs/2606.04825), [相关研究](https://arxiv.org/abs/2604.07335); these sources converge on data infrastructure rather than model-only scaling）。

第四层是闭环使用。OmniVTA 把预测的接触演化接到 60Hz reflexive tactile controller；TacForeSight 把预测触觉 潜在状态 作为 anticipatory contact priors；ViTaL 把 visuo-触觉潜在状态 world model 用于推理期候选动作验证；AT-VLA 则把视觉语言慢流和触觉快流分离，使用 3:1 快慢流比例处理接触反馈。

这些结果共同说明，触觉世界模型要有价值，通常需要进入控制回路，而不是只做离线视频或触觉预测分数（[相关研究](https://arxiv.org/abs/2603.19201), [相关研究](https://arxiv.org/abs/2606.11184), [相关研究](https://arxiv.org/abs/2606.14981), [相关研究](https://arxiv.org/abs/2605.07308)）。

## 主要共识

共识一：视觉世界模型在接触丰富任务中缺关键状态。遮挡、视觉别名、局部接触、滑移和微小力变化，会让纯视觉预测在“最后几厘米”失真；触觉提供的是局部物理状态，不只是另一个图像视角。Visuo-Tactile World Models、TacForeSight、HapTile 等论文从模型、预测和数据三侧直接支持这点（[相关研究](https://arxiv.org/abs/2602.06001), [相关研究](https://arxiv.org/abs/2606.11184), [相关研究](https://arxiv.org/abs/2606.04825)）。

共识二：模型必须显式尊重时间。触觉是接触事件驱动的，高速力/力矩可以先于指尖触觉变化，未来触觉 潜在状态 比当前触觉拼接更适合做 proactive control；同时长时域规划会放大接触预测误差。

这一结论在 TacForeSight、ContactWorld 和 Dream-Tac 中分别表现为 force-conditioned tactile foresight、long-horizon tactile importance 和 contact-gated attention（ [相关研究](https://arxiv.org/abs/2606.13877), [相关研究](https://arxiv.org/abs/2606.11184), [相关研究](https://arxiv.org/abs/2606.08737)）。

共识三：数据质量的定义必须包括闭环可用性。数据采集要同时管理硬件、同步、标定、动作、元数据和质量控制；TAMEn 对“成功演示不能代表可执行机器人行为”的批评尤其重要，因为接触丰富任务的临界失败往往来自力积累、早期滑移、局部变形或支撑不稳，这些状态只有真实物理交互和恢复数据才能覆盖（[相关研究](https://arxiv.org/abs/2604.07335)）。

共识四：评测必须从表征指标走向真实任务。HT-Bench 对触觉表征提出大规模检索、inpainting、视觉到触觉合成和多模态触觉预测评测，但作者也明确说这些不直接测量下游机器人表现。因此，触觉世界模型论文若只报告 reconstruction 或潜在状态 prediction，还不能证明它能改善接触丰富操作（[相关研究](https://arxiv.org/abs/2606.19161)）。

## 条件与分歧

触觉不是无条件增益。ContactWorld 的真实实验显示，点云对阀门旋拧很强，TacRGB 对图像视角有帮助，但 TacDepth/TacFF 在真实设置中并不总是稳定；作者把一部分原因归到传感器标定、深度和力推断噪声。这个结果提醒我们：触觉表示、视觉表示和动作模型 潜在状态 必须兼容，否则“多模态”可能变成噪声注入（ [相关研究](https://arxiv.org/abs/2606.13877);）。

在线触觉与离线触觉蒸馏代表两条部署路线。OmniVTA、TacForeSight、ViTaL 和 AT-VLA 偏向在线感知和实时修正；HapticVLA 则主张通过安全接触奖励与 tactile distillation，在推理期不依赖触觉传感器也能获得触觉 aware 行为。前者适合扰动丰富、接触不可预测的场景，后者适合硬件成本或跨平台复现压力大的场景；

两者不能简单互相替代（ [相关研究](https://arxiv.org/abs/2603.19201), [相关研究](https://arxiv.org/abs/2606.14981), [相关研究](https://arxiv.org/abs/2605.07308), [相关研究](https://arxiv.org/abs/2603.15257); deployment trade-off follows from sensing requirements）。

推理期使用世界模型会引入新的误差链。ViTaL 明确指出 潜在状态 world model 的保真度会影响候选动作验证，尤其是细微接触事件；触觉编码器的预训练规模也远小于现代视觉语言模型。这意味着“用世界模型挑动作”并不自动比行为克隆安全，除非评测覆盖 compounding error、接触误报/漏报和高频控制延迟（ [相关研究](https://arxiv.org/abs/2606.14981);）。

## 未解决问题

第一，跨传感器、跨手爪、跨材料的泛化仍不足。本轮强证据多来自 GelSight/Digit 360/vision-based tactile sensor/多传感器系统等具体硬件；OmniVTA 虽然引入多触觉传感器，但通用 tactile world model 是否能跨传感器迁移，仍需要更系统评测（ [相关研究](https://arxiv.org/abs/2603.19201), [相关研究](https://arxiv.org/abs/2606.19161); sensor heterogeneity remains unresolved in this run）。

第二，表征级 基准 与真实机器人成功率之间缺桥。HT-Bench 提供了大规模全手触觉表示评测，但限制部分说明还没有直接测下游机器人任务；ContactWorld、TacForeSight 等真实任务又通常规模小、硬件特定。下一步需要把 tactile retrieval、vision-to-touch synthesis、潜在状态 prediction 与插拔、旋拧、擦拭、抓握恢复等任务成功率关联起来（ [相关研究](https://arxiv.org/abs/2606.11184), [相关研究](https://arxiv.org/abs/2606.19161);）。

第三，触觉世界模型尚未形成统一的数据规范。HapTile 强调语言、动作、同步和 marker motion，TAMEn 强调可执行性与恢复，Visuo-Tactile World Models 强调成功/失败轨迹，OmniVTA 强调多任务多传感器。

可以推断，领域还在探索“最小充分数据单元”：究竟是 tactile image、tactile depth、force-field、marker displacement、6D wrench、object pose，还是它们的某种 潜在状态 组合（ [相关研究](https://arxiv.org/abs/2602.06001), [相关研究](https://arxiv.org/abs/2603.19201),  [相关研究](https://arxiv.org/abs/2606.04825); data schemas differ across sources）。

## 对后续研究的启发

如果要做“触觉世界模型”，建议把研究对象定义为“动作条件的接触未来预测”，而不是“视觉世界模型加触觉输入”。最低可行模型可以预测短时域 触觉潜在状态、contact mask/force-field 或 marker displacement，并把预测接到 MPC、policy steering 或动作 head；

TacForeSight 和 Dream-Tac 分别给了 force-conditioned 潜在状态 prediction 与 world-action generation 两种参考形态（ [相关研究](https://arxiv.org/abs/2606.11184),  [相关研究](https://arxiv.org/abs/2606.08737); model formulation follows from current strongest methods）。

数据采集上，建议设计“触觉世界模型数据五件套”：时间同步的视觉/触觉/动作/本体状态，至少一种 force 或 tactile-derived contact geometry，成功与失败演示，扰动恢复片段，机器人侧可执行性与闭环 replay 检查。

这个建议直接来自 Visuo-Tactile World Models、HapTile 和 TAMEn 对模型、数据与可执行性的共同约束（[相关研究](https://arxiv.org/abs/2602.06001), [相关研究](https://arxiv.org/abs/2606.04825), [相关研究](https://arxiv.org/abs/2604.07335)）。

评测上，建议使用四层指标：表征预测质量、接触事件识别、短时域控制修正、真实任务长期成功率。HT-Bench 可覆盖表征层，ContactWorld 覆盖规划层，TacForeSight 覆盖扰动恢复，ViTaL 暴露推理期误差累积问题；只有把这些层串起来，才能判断触觉世界模型是否真的改善数据效率、泛化和安全接触（ [相关研究](https://arxiv.org/abs/2606.13877), [相关研究](https://arxiv.org/abs/2606.11184), [相关研究](https://arxiv.org/abs/2606.14981), [相关研究](https://arxiv.org/abs/2606.19161); evaluation stack synthesis）。

## 中心判断的工程化表达

触觉世界模型应被定义为“动作条件下的接触状态预测器”，而不是增加触觉输入的视频模型。它至少要回答三件事：接触是否建立，接触如何随动作变化，预测能否在控制截止前改变动作。若只重建触觉图像，却不能改善滑移检测、恢复或安全施力，就没有证明世界模型的控制价值。

数据单元应围绕接触事件组织。每个片段需要同步视觉、触觉、力矩、本体状态和动作，标出首次接触、稳定抓取、滑移、脱离与恢复。成功演示之外，还要采集扰动和失败邻域；这些片段决定模型是否只会复现理想路径，还是能在真实偏差中修正。

模型接口也应分时标。语言与视觉负责低频任务理解，触觉和力负责高频局部修正；快速通道不必重复完整语义推理，慢速通道也不能忽略接触告警。分层结构能降低延迟，却要求两条通道共享时间和动作状态，否则融合会制造新的错误。

评测应从四级展开：预测能否识别接触事件，短时动作能否降低滑移或过力，长时任务能否稳定完成，跨传感器与材料是否仍然校准。表征分数可以帮助诊断，但不能替代真实控制结果。尤其要报告错误拒绝与不确定性，避免世界模型在细微接触上自信地给出错误建议。

部署路线可以分成在线感知和离线蒸馏。在线触觉适合扰动不可预测、接触风险高的任务；离线蒸馏适合硬件受限、环境稳定的场景。两者的选择取决于失败代价与状态可预测性，而不是单纯比较模型规模。

## References

- `S-TWM-001`: [ContactWorld](https://arxiv.org/abs/2606.13877)
- `S-TWM-002`: [TacForeSight](https://arxiv.org/abs/2606.11184)
- `S-TWM-003`: [OmniVTA](https://arxiv.org/abs/2603.19201)
- `S-TWM-004`: [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001)
- `S-TWM-005`: [Dream-Tac](https://arxiv.org/abs/2606.08737)
- `S-TWM-006`: [Inference-time Policy Steering via Vision and Touch](https://arxiv.org/abs/2606.14981)
- `S-TWM-007`: [HapTile](https://arxiv.org/abs/2606.04825)
- `S-TWM-008`: [TAMEn](https://arxiv.org/abs/2604.07335)
- `S-TWM-009`: [HT-Bench](https://arxiv.org/abs/2606.19161)
- `S-TWM-010`: [AT-VLA](https://arxiv.org/abs/2605.07308)
- `S-TWM-011`: [HapticVLA](https://arxiv.org/abs/2603.15257)
