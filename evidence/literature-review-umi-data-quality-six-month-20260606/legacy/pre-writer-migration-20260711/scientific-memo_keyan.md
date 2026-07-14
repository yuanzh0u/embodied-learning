# UMI 数据质量研究备忘录

## 研究边界与证据范围

- Topic: UMI 数据质量
- Time range: 2025-12-06..2026-06-06
- Knowledge IDs: `EA-DATA`, `EA-SENSOR`, `EA-HARDWARE`, `EA-XEMBODIMENT`
- Paper-level sources: 5 / 5
- Output type: scientific-memo

## Evidence Core

- Accepted events: 5
- Stance labels: `conditional`, `limit`, `support`
- Confidence labels: `direct`
- Trace IDs: [UMI-6M-001](evidence-appendix.md#umi-6m-001), [UMI-6M-002](evidence-appendix.md#umi-6m-002), [UMI-6M-003](evidence-appendix.md#umi-6m-003), [UMI-6M-004](evidence-appendix.md#umi-6m-004), [UMI-6M-005](evidence-appendix.md#umi-6m-005)
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`

## Claim Map

| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |
|---|---|---|---|---|---|---|---|
| [UMI-6M-001](evidence-appendix.md#umi-6m-001) | EA-DATA | `conditional` | `direct` | UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision... | The HTML full text reports that UMI-FT mounts compact six-axis force/torque sensors on each finger, uses multimodal demonstrations to train adaptive compliance policies, and shows diverse in-the-wild data outperforming... | choi-hojung; hou-yifan; pan-chuer; et al. | [2601.09988](https://arxiv.org/abs/2601.09988) |
| [UMI-6M-002](evidence-appendix.md#umi-6m-002) | EA-DATA | `limit` | `direct` | UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefu... | The HTML full text frames UMI grippers as promising data-collection tools but reports that concentrated-load grippers improve over distributed-load grippers while both remain slower and less effective than hands, with d... | georgadarellis-gina-l; beslic-natalija; lee-seonhun; et al. | [2603.17189](https://arxiv.org/abs/2603.17189) |
| [UMI-6M-003](evidence-appendix.md#umi-6m-003) | EA-SENSOR | `conditional` | `direct` | UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical inter... | The HTML full text repeatedly identifies limited physical interaction signals as a bottleneck of existing UMI-like systems and proposes synchronized RGB, depth, trajectory, tactile sensing, internal grasping force, and... | luo-shaqi; li-yuanyuan; hu-youhao; et al. | [2604.10647](https://arxiv.org/abs/2604.10647) |
| [UMI-6M-004](evidence-appendix.md#umi-6m-004) | EA-SENSOR | `limit` | `direct` | Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves... | The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration d... | wang-ziming | [2604.14089](https://arxiv.org/abs/2604.14089) |
| [UMI-6M-005](evidence-appendix.md#umi-6m-005) | EA-XEMBODIMENT | `support` | `direct` | For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action space, avoiding retar... | The HTML full text argues that retargeting and embodiment conversion can distort contact-rich interactions, then presents RealDexUMI as a retargeting-free wearable interface whose shared hand and sensing modules preserv... | xu-chaoyi; jiang-yixuan; huan-jiahui; et al. | [2606.06033](https://arxiv.org/abs/2606.06033) |

## 主要综合

### 共识/正向证据
- [UMI-6M-005](evidence-appendix.md#umi-6m-005): For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action space, avoiding retargeting and embodiment-conversion losses.
### 条件成立
- [UMI-6M-001](evidence-appendix.md#umi-6m-001): UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only data is insufficient fo...
- [UMI-6M-003](evidence-appendix.md#umi-6m-003): UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data.
### 限制与失败模式
- [UMI-6M-002](evidence-appendix.md#umi-6m-002): UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefulness.
- [UMI-6M-004](evidence-appendix.md#umi-6m-004): Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible ta...

## Source Gaps

- No immediate source gaps detected from loaded packet inputs.

## References

- `2601.09988` [In-the-Wild Compliant Manipulation with UMI-FT](https://arxiv.org/abs/2601.09988)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)
- `2604.10647` [OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction](https://arxiv.org/abs/2604.10647)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089)
- `2606.06033` [RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning](https://arxiv.org/abs/2606.06033)

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。

## 研究启发与开放问题

- Treat support, conditional, limit, and gap events as separate signals before writing topic-card updates.
- Mark cross-event synthesis as `inference` unless a claim is directly backed by an event/source ID.
- Use topic-card update suggestions only after checking source gaps.
