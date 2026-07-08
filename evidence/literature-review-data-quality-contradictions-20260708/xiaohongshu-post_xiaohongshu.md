# 具身智能数据质量的主要矛盾：洞察短串

## Hook

具身智能数据质量的主要矛盾 最容易被讲成一句口号，但真正值钱的信息藏在证据条件里。

## 证据约束洞察

1. 4D时空推理若要从人类视频迁移到机器人控制，不能只收动作标签；它需要能描述物体如何在3D中随时间运动的密集点轨迹，并配少量机器人动作示教完成可执行落地。 ([EA-DATA-2026-4DDATA-0001](evidence-appendix.md#ea-data-2026-4ddata-0001); stance: `support`)
2. 面向4D生成式仿真的数据应把抽象动作展开成可控的机器人4D几何轨迹，并同时监督环境响应的RGB/pointmap序列。 ([EA-DATA-2026-4DDATA-0005](evidence-appendix.md#ea-data-2026-4ddata-0005); stance: `support`)
3. 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。 ([EA-TWM-2026-0005](evidence-appendix.md#ea-twm-2026-0005); stance: `support`)
4. 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。 ([EA-TWM-2026-0014](evidence-appendix.md#ea-twm-2026-0014); stance: `support`)
5. 4D世界模型的数据需求可以转化为“几何教师监督”：用预训练4D几何模型产生对应结构，让视频骨干在训练期学习深度、相机运动和物体运动。 ([EA-DATA-2026-4DDATA-0008](evidence-appendix.md#ea-data-2026-4ddata-0008); stance: `support`)

## 边界提醒

- Strong hook is allowed; stance/confidence cannot be upgraded.
- Any `conditional`, `limit`, or `gap` claim must stay visible in the thread.

## 依据来源

- Time range: 2026-01-08..2026-07-08

- Evidence sufficiency: formal-ready
- Paper-level sources: 34 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

- No immediate source gaps detected from loaded packet inputs.

## References

- `2602.06001` [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) (2026-02-05)
- `2602.09722` [Rethinking Visual-Language-Action Model Scaling: Alignment, Mixture, and Regularization](https://arxiv.org/abs/2602.09722) (2026-02-10)
- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.08485` [3PoinTr: 3D Point Tracks for Learning Manipulation from Unconstrained Human Videos](https://arxiv.org/abs/2603.08485) (2026-03-09)
- `2603.15257` [HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing](https://arxiv.org/abs/2603.15257) (2026-03-16)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189) (2026-03-17)
- `2603.19201` [OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation](https://arxiv.org/abs/2603.19201) (2026-03-19)
- `2604.07335` [TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks](https://arxiv.org/abs/2604.07335) (2026-04-08)
- `2605.07308` [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](https://arxiv.org/abs/2605.07308) (2026-05-08)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.12759` [Sparse2Act: Learning Action-Aligned Sparse 3D Representations for Cross-Domain Robot Manipulation](https://arxiv.org/abs/2606.12759) (2026-06-10)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)
- `2606.13877` [ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13877) (2026-06-11)
- `2606.14981` [Inference-time Policy Steering via Vision and Touch](https://arxiv.org/abs/2606.14981) (2026-06-12)
- `2606.15516` [Transferring Contact, Not Just Motion: Compliant Grasping Across Dexterous Hands](https://arxiv.org/abs/2606.15516) (2026-06-17)
- `2606.19161` [HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision](https://arxiv.org/abs/2606.19161) (2026-06-17)
- `2606.24049` [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049) (2026-06-23)
- `2606.26095` [Learning Action Priors for Cross-embodiment Robot Manipulation](https://arxiv.org/abs/2606.26095) (2026-06-24)
- `2606.26800` [SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation](https://arxiv.org/abs/2606.26800) (2026-06-25)
- `2606.27295` [LA4VLA: Learning to Act without Seeing via Language-Action Pretraining](https://arxiv.org/abs/2606.27295) (2026-06-25)
- `2606.30113` [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113) (2026-06-29)
- `2606.30456` [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](https://arxiv.org/abs/2606.30456) (2026-06-29)
- `2606.30552` [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](https://arxiv.org/abs/2606.30552) (2026-06-29)
- `2607.02642` [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (2026-07-02)
- `2607.02840` [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840) (2026-07-03)
- `2607.05390` [Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models](https://arxiv.org/abs/2607.05390) (2026-07-06)
- `2607.06442` [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](https://arxiv.org/abs/2607.06442) (2026-07-07)
- `2607.06558` [RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation](https://arxiv.org/abs/2607.06558) (2026-07-07)
- `2607.06564` [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](https://arxiv.org/abs/2607.06564) (2026-07-07)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
