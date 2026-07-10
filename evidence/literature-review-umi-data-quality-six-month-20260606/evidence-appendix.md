# Evidence Appendix: UMI 数据质量

- Time range: 2025-12-06..2026-06-06
- Events: 5
- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。

### UMI-6M-001

- Claim: UMI-style data is useful for contact-rich manipulation when the collection interface records force/torque, depth, pose, and grasp-force signals; the paper also implies that vision/trajectory-only data is insufficient for force-sensitive tasks.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2601.09988](https://arxiv.org/abs/2601.09988) In-the-Wild Compliant Manipulation with UMI-FT
- Locator: Abstract; V-B In-the-Wild Experiments
- Evidence: The HTML full text reports that UMI-FT mounts compact six-axis force/torque sensors on each finger, uses multimodal demonstrations to train adaptive compliance policies, and shows diverse in-the-wild data outperforming limited scene-diversity data in a skewer task.
- Authors: choi-hojung; hou-yifan; pan-chuer; et al.

### UMI-6M-002

- Claim: UMI data quality is not only a modeling issue; handheld gripper ergonomics and mechanics directly affect demonstration speed, damage, workload, and therefore downstream data usefulness.
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.17189](https://arxiv.org/abs/2603.17189) Influence of Gripper Design on Human Demonstration Quality for Robot Learning
- Locator: Abstract; II-A Performance and Usability Limitations; V Discussion; VI Conclusion
- Evidence: The HTML full text frames UMI grippers as promising data-collection tools but reports that concentrated-load grippers improve over distributed-load grippers while both remain slower and less effective than hands, with design refinements needed to reduce user burden and improve demonstration quality.
- Authors: georgadarellis-gina-l; beslic-natalija; lee-seonhun; et al.

### UMI-6M-003

- Claim: UMI-style data is a scalable foundation, but becomes substantially more useful for contact-rich tasks when upgraded from mainly visuomotor supervision to multimodal physical interaction data.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2604.10647](https://arxiv.org/abs/2604.10647) OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction
- Locator: Abstract; 1 Introduction; 2.1 Robot-free Interfaces; 2.5 Multimodal Policy Learning; 5 Conclusion
- Evidence: The HTML full text repeatedly identifies limited physical interaction signals as a bottleneck of existing UMI-like systems and proposes synchronized RGB, depth, trajectory, tactile sensing, internal grasping force, and external wrench data to improve contact-rich policy learning.
- Authors: luo-shaqi; li-yuanyuan; hu-youhao; et al.

### UMI-6M-004

- Claim: Original vision-only UMI data can fail to be useful in scenes with occlusion, dynamic changes, feature-poor regions, or tracking failure; adding LiDAR-centric 3D sensing improves data quality and expands the feasible task distribution.
- Stance: `limit` | Confidence: `direct`
- Paper: [2604.14089](https://arxiv.org/abs/2604.14089) UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
- Locator: Abstract; I Introduction; II-A UMI Variants and System Evolution; IV Evaluations
- Evidence: The HTML full text states that monocular visual SLAM makes UMI vulnerable to occlusions, dynamic scenes, and tracking failures, and reports that LiDAR-centric SLAM improves pose-estimation robustness and demonstration data quality under challenging real-world conditions.
- Authors: wang-ziming

### UMI-6M-005

- Claim: For dexterous manipulation, UMI-style data is most usable when collection and deployment share the same dexterous end-effector, sensing, contacts, and action space, avoiding retargeting and embodiment-conversion losses.
- Stance: `support` | Confidence: `direct`
- Paper: [2606.06033](https://arxiv.org/abs/2606.06033) RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning
- Locator: Abstract; 1 Introduction; 2.2 Dexterous Demonstration Interfaces; 3.3 Palm-Side Isomorphic Teleoperation Glove; A.1 Glove Sensing Interface
- Evidence: The HTML full text argues that retargeting and embodiment conversion can distort contact-rich interactions, then presents RealDexUMI as a retargeting-free wearable interface whose shared hand and sensing modules preserve deployment-aligned observations, tactile signals, contacts, and executable hand actions.
- Authors: xu-chaoyi; jiang-yixuan; huan-jiahui; et al.

## References

- `2601.09988` [In-the-Wild Compliant Manipulation with UMI-FT](https://arxiv.org/abs/2601.09988)
- `2603.17189` [Influence of Gripper Design on Human Demonstration Quality for Robot Learning](https://arxiv.org/abs/2603.17189)
- `2604.10647` [OmniUMI: Towards Physically Grounded Robot Learning via Human-Aligned Multimodal Interaction](https://arxiv.org/abs/2604.10647)
- `2604.14089` [UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception](https://arxiv.org/abs/2604.14089)
- `2606.06033` [RealDexUMI: A Wearable Universal Manipulation Interface for Dexterous Robot Learning](https://arxiv.org/abs/2606.06033)
