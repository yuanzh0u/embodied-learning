# 触觉世界模型：洞察短串

## Hook

触觉世界模型 最容易被讲成一句口号，但真正值钱的信息藏在证据条件里。

## 证据约束洞察

1. 可训练的触觉世界模型需要跨任务、跨物体、跨传感器的接触轨迹，而不是少量单任务触觉演示。 ([EA-TWM-2026-0005](evidence-appendix.md#ea-twm-2026-0005); stance: `support`)
2. 触觉世界模型的数据需求包括可执行性检查和真实失败恢复数据，因为成功演示不足以覆盖接触临界状态。 ([EA-TWM-2026-0014](evidence-appendix.md#ea-twm-2026-0014); stance: `support`)
3. 面向触觉世界模型的数据集应同时包含语言、动作、视觉、触觉、机器人状态和操作者接触反馈，而不是只保存触觉图像。 ([EA-TWM-2026-0013](evidence-appendix.md#ea-twm-2026-0013); stance: `support`)
4. 触觉世界模型至少需要时间同步的视觉、动作、机器人状态和多指触觉序列；但当前结果仍受传感器、场景和对象分布限制。 ([EA-TWM-2026-0004](evidence-appendix.md#ea-twm-2026-0004); stance: `conditional`)
5. 触觉世界模型必须在扰动与恢复数据上评估，否则会高估接触丰富任务的稳定性。 ([EA-TWM-2026-0008](evidence-appendix.md#ea-twm-2026-0008); stance: `support`)

## 边界提醒

- Strong hook is allowed; stance/confidence cannot be upgraded.
- Any `conditional`, `limit`, or `gap` claim must stay visible in the thread.

## 依据来源

- Time range: 2025-12-23..2026-06-23

- Evidence sufficiency: formal-ready
- Paper-level sources: 11 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.

## References

- `2602.06001` [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) (2026-02-05)
- `2603.15257` [HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing](https://arxiv.org/abs/2603.15257) (2026-03-16)
- `2603.19201` [OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation](https://arxiv.org/abs/2603.19201) (2026-03-19)
- `2604.07335` [TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks](https://arxiv.org/abs/2604.07335) (2026-04-08)
- `2605.07308` [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](https://arxiv.org/abs/2605.07308) (2026-05-08)
- `2606.04825` [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](https://arxiv.org/abs/2606.04825) (2026-06-03)
- `2606.08737` [Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2606.08737) (2026-06-07)
- `2606.11184` [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](https://arxiv.org/abs/2606.11184) (2026-06-09)
- `2606.13877` [ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13877) (2026-06-11)
- `2606.14981` [Inference-time Policy Steering via Vision and Touch](https://arxiv.org/abs/2606.14981) (2026-06-12)
- `2606.19161` [HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision](https://arxiv.org/abs/2606.19161) (2026-06-17)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
