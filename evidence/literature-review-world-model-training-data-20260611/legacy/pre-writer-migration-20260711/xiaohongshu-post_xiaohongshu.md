# 世界模型训练数据：洞察短串

## Hook

世界模型训练数据 最容易被讲成一句口号，但真正值钱的信息藏在证据条件里。

## 证据约束洞察

1. A robot world model can be trained from a moderate-sized robot interaction dataset and then used to generate policy-training demonstrations, but its value depends on interaction-c... ([EA-DATA-2026-WMDATA-0001](evidence-appendix.md#ea-data-2026-wmdata-0001); stance: `support`)
2. World-model training and post-training data should include dense corrective trajectories around failure-prone states, not only successful demonstrations. ([EA-DATA-2026-WMDATA-0003](evidence-appendix.md#ea-data-2026-wmdata-0003); stance: `support`)
3. A world-model dataset must support prediction, not only policy imitation: it should expose how observations, objects, contacts, and robot states evolve under intervention, with mo... ([EA-DATA-2026-WMDATA-0014](evidence-appendix.md#ea-data-2026-wmdata-0014); stance: `support`)
4. Unified video-action world models benefit from heterogeneous interaction corpora that mix high-fidelity robot teleoperation, scalable UMI-style demonstrations, broad egocentric hu... ([EA-DATA-2026-WMDATA-0002](evidence-appendix.md#ea-data-2026-wmdata-0002); stance: `support`)
5. Embodiment-aware robot data synthesis should start from robot motion renderings or a small seed set of teleoperation demonstrations, because off-the-shelf generative models can ha... ([EA-DATA-2026-WMDATA-0005](evidence-appendix.md#ea-data-2026-wmdata-0005); stance: `conditional`)

## 边界提醒

- Strong hook is allowed; stance/confidence cannot be upgraded.
- Any `conditional`, `limit`, or `gap` claim must stay visible in the thread.

## 依据来源

- Time range: 2025-12-11..2026-06-11

- Evidence sufficiency: formal-ready
- Paper-level sources: 14 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

- No immediate source gaps detected from loaded packet inputs.

## References

- `2512.11797` [AnchorDream: Repurposing Video Diffusion for Embodiment-Aware Robot Data Synthesis](https://arxiv.org/abs/2512.11797) (2025-12-12)
- `2603.08546` [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546) (2026-03-09)
- `2604.11386` [ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation](https://arxiv.org/abs/2604.11386) (2026-04-13)
- `2604.21741` [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](https://arxiv.org/abs/2604.21741) (2026-04-23)
- `2605.20752` [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](https://arxiv.org/abs/2605.20752) (2026-05-20)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.27947` [SANTS: A State-Adaptive Scheduler for World Action Models](https://arxiv.org/abs/2605.27947) (2026-05-27)
- `2606.00113` [World Models for Robotic Manipulation: A Survey](https://arxiv.org/abs/2606.00113) (2026-05-27)
- `2606.00664` [SKIP: Sparse Keyframe Interpolation Paradigm for Efficient Embodied World Models](https://arxiv.org/abs/2606.00664) (2026-05-30)
- `2606.01027` [τ0-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.02577` [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](https://arxiv.org/abs/2606.02577) (2026-06-01)
- `2606.12072` [World Model Self-Distillation: Training World Models to Solve General Tasks](https://arxiv.org/abs/2606.12072) (2026-06-10)
- `2606.12217` [Making Foresight Actionable: Repurposing Representation Alignment in World Action Models](https://arxiv.org/abs/2606.12217) (2026-06-10)
- `2606.12403` [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](https://arxiv.org/abs/2606.12403) (2026-06-10)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
