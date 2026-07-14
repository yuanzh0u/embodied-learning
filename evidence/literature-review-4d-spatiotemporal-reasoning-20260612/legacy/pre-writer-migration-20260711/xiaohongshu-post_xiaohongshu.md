# 4D 时空推理：洞察短串

## Hook

4D 时空推理 最容易被讲成一句口号，但真正值钱的信息藏在证据条件里。

## 证据约束洞察

1. Kinema4D's data strategy favors scalable 4D pseudo-annotation breadth over sub-millimeter geometric ground truth, which is presented as adequate for learning relative spatial cons... ([EA-DATA-2026-4D-0007](evidence-appendix.md#ea-data-2026-4d-0007); stance: `conditional`)
2. τ0-WM argues that broad human/egocentric video and UMI-style interaction data can train visual dynamics, but robot demonstrations are still needed for executable action grounding. ([EA-DATA-2026-4D-0011](evidence-appendix.md#ea-data-2026-4d-0011); stance: `conditional`)
3. Pri4R's ablations support the claim that temporally dense and metrically grounded 3D point tracks are a stronger world-dynamics supervision target than 2D tracks, goal-only predic... ([EA-EVAL-2026-4D-0004](evidence-appendix.md#ea-eval-2026-4d-0004); stance: `support`)
4. Kinema4D argues that robot-world interaction should be simulated as a 4D event: robot control is represented with kinematically correct 4D trajectories, while a generative model p... ([EA-EVAL-2026-4D-0006](evidence-appendix.md#ea-eval-2026-4d-0006); stance: `support`)
5. WEAVER defines useful robot world models by three joint requirements: fidelity to real outcomes, temporal consistency over long horizons, and enough efficiency for evaluation, imp... ([EA-EVAL-2026-4D-0013](evidence-appendix.md#ea-eval-2026-4d-0013); stance: `support`)

## 边界提醒

- Strong hook is allowed; stance/confidence cannot be upgraded.
- Any `conditional`, `limit`, or `gap` claim must stay visible in the thread.

## 依据来源

- Time range: 2025-12-12..2026-06-12

- Evidence sufficiency: formal-ready
- Paper-level sources: 10 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

- No immediate source gaps detected from loaded packet inputs.

## References

- `2603.01549` [Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation](https://arxiv.org/abs/2603.01549) (2026-03-02)
- `2603.13788` [ST-VLA: Enabling 4D-Aware Spatiotemporal Understanding for General Robot Manipulation](https://arxiv.org/abs/2603.13788) (2026-03-14)
- `2603.15467` [Evaluating Time Awareness and Cross-modal Active Perception of Large Models via 4D Escape Room Task](https://arxiv.org/abs/2603.15467) (2026-03-16)
- `2603.16669` [Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation](https://arxiv.org/abs/2603.16669) (2026-03-17)
- `2605.00121` [Predictive Spatio-Temporal Scene Graphs for Semi-Static Scenes](https://arxiv.org/abs/2605.00121) (2026-04-30)
- `2605.17682` [GEM: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning](https://arxiv.org/abs/2605.17682) (2026-05-17)
- `2605.22882` [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) (2026-05-20)
- `2605.29879` [DGSG-Mind: Dynamic 3D Gaussian Scene Graphs for Long-Term Scene Understanding and Grounding](https://arxiv.org/abs/2605.29879) (2026-05-28)
- `2606.01027` [$τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) (2026-05-31)
- `2606.13672` [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](https://arxiv.org/abs/2606.13672) (2026-06-11)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
