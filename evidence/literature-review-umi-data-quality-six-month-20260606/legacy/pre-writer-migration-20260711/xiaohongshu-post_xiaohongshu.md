# UMI 数据质量：洞察短串

## Hook

UMI 数据质量 最容易被讲成一句口号，但真正值钱的信息藏在证据条件里。

## 证据约束洞察

1. UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision... ([UMI-6M-001](evidence-appendix.md#umi-6m-001); stance: `conditional`)
2. UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefu... ([UMI-6M-002](evidence-appendix.md#umi-6m-002); stance: `limit`)
3. UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical inter... ([UMI-6M-003](evidence-appendix.md#umi-6m-003); stance: `conditional`)
4. Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves... ([UMI-6M-004](evidence-appendix.md#umi-6m-004); stance: `limit`)
5. For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action space, avoiding retar... ([UMI-6M-005](evidence-appendix.md#umi-6m-005); stance: `support`)

## 边界提醒

- Strong hook is allowed; stance/confidence cannot be upgraded.
- Any `conditional`, `limit`, or `gap` claim must stay visible in the thread.

## 依据来源

- Time range: 2025-12-06..2026-06-06

- Evidence sufficiency: formal-ready
- Paper-level sources: 5 / 5
- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.

- No immediate source gaps detected from loaded packet inputs.

## References

- `2601.09988` [In-the-Wild Compliant Manipulation with UMI-FT](https://arxiv.org/abs/2601.09988)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)
- `2604.10647` [OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction](https://arxiv.org/abs/2604.10647)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089)
- `2606.06033` [RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning](https://arxiv.org/abs/2606.06033)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
