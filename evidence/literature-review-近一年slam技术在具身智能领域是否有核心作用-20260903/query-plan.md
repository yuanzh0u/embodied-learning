# Query Plan: 近一年SLAM技术在具身智能领域是否有核心作用

## Scope

- Knowledge IDs: EA-HARDWARE, EA-MODEL
- Families: none
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 128
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dynamic-slam-vla-intersection | dynamic-association | `all:SLAM AND all:"vision-language-action"` | 近一年出现直接讨论 SLAM 与 VLA 关系的论文（SLAM 作为 VLA 训练/评测/部署的隐形底座），静态分类法没有该交集。 |
| dynamic-gaussian-slam | dynamic-association | `all:"Gaussian splatting" AND all:SLAM` | 3DGS-SLAM 是近一年 SLAM 前沿主线之一（compact 3DGS dense SLAM、Splat-SLAM、LEG-SLAM），用于机器人实时建图。 |
| dynamic-gaussian-robotic-mapping | dynamic-association | `all:"Gaussian splatting" AND all:mapping AND all:robot` | GaussLite 等任务条件化在线 3DGS 建图把地图与具身任务耦合，是 SLAM 在具身侧的新形态。 |
| dynamic-mapless-navigation | dynamic-association | `all:mapless AND all:navigation AND all:robot` | mapless/map-free 导航是显式地图路线的主要反方证据来源。 |
| dynamic-spatial-memory-robot | dynamic-association | `all:"spatial memory" AND all:robot` | 隐式/结构化空间记忆（SRU、稀疏记忆导航）被提出替代显式 SLAM 地图，是核心作用之争的关键邻接家族。 |
| dynamic-language-map-navigation | dynamic-association | `all:"language map" AND all:navigation` | LAMP 等隐式语言场地图把语义地图神经化，覆盖 semantic SLAM 与语言导航的交叉。 |
| dynamic-slam-teleoperation | dynamic-association | `all:SLAM AND all:teleoperation` | SLAM 在数据采集侧（遥操作位姿恢复、手持采集器）的隐形角色，静态分类法仅从 UMI 角度覆盖。 |
| dynamic-slam-manipulation | dynamic-association | `all:SLAM AND all:manipulation` | 操作任务中 SLAM 的作用（物体级地图、位姿跟踪支撑抓取）是核心作用之争的操作侧证据。 |
| dynamic-endtoend-slam | dynamic-association | `all:"end-to-end" AND all:SLAM` | 端到端/深度 SLAM 路线检验学习化是否正在替代模块化 SLAM 栈。 |
| dynamic-worldmodel-pathplanning | dynamic-association | `all:"world model" AND all:"path planning" AND all:robot` | Target-Bench 等工作直接评测世界模型能否做 mapless 路径规划，是地图替代路线的评测证据。 |
| dynamic-spatial-intelligence | dynamic-association | `all:"spatial intelligence" AND all:robot` | spatial intelligence 是近一年把定位建图能力重新包装进具身基础模型话语的术语。 |
| dynamic-vo-foundation | dynamic-association | `all:"visual odometry" AND all:"foundation model"` | 基础模型化视觉里程计（学习化前端）检验 SLAM 前端是否被大模型吸收。 |
| persona-slam-engineer-robustness | persona-direct | `all:"visual SLAM" AND all:robustness` | SLAM 系统工程师：定位近一年 SLAM 鲁棒性进展本身 |
| persona-slam-engineer-neural-frontend | persona-method | `all:SLAM AND all:"neural" AND all:real-time` | SLAM 系统工程师：神经化组件（学习特征/匹配/深度）进入实时 SLAM 栈的证据 |
| persona-vla-implicit-navigation | persona-method | `all:"vision-language-action" AND all:navigation` | VLA 研究者：VLA 是否直接承担导航与空间任务 |
| persona-vla-mapfree | persona-limit | `all:"map-free" AND all:navigation` | VLA 研究者：map-free 路线声称无需显式地图即可导航 |
| persona-vla-worldmodel-replace-map | persona-limit | `all:"world model" AND all:mapping AND all:navigation` | VLA 研究者：世界模型是否以生成式地图替代 SLAM 建图 |
| persona-auditor-teleop-pose | persona-deploy | `all:teleoperation AND all:"pose tracking"` | 数据基础设施审计员：遥操作/示教采集中位姿跟踪的部署证据 |
| persona-auditor-ground-truth | persona-eval | `all:SLAM AND all:"ground truth"` | 数据基础设施审计员：SLAM 作为评测真值生产工具的可靠性边界 |
| persona-auditor-camera-relocalization | persona-deploy | `all:relocalization AND all:robot` | 数据基础设施审计员：相机重定位在机器人数据管线中的角色 |
| persona-counter-dynamic-failure | persona-limit | `all:SLAM AND all:failure AND all:dynamic` | 反面证据搜寻者：动态环境与失效模式证据 |
| persona-counter-implicit-memory | persona-limit | `all:"implicit memory" AND all:navigation` | 反面证据搜寻者：隐式记忆路线宣称替代显式地图的反方证据 |
| persona-basic-slam-robot | persona-direct | `all:SLAM AND all:robot AND all:embodied` | 基础事实覆盖者：SLAM 与具身智能的总体交集 |
| persona-basic-slam-survey | persona-direct | `all:"simultaneous localization and mapping" AND all:survey` | 基础事实覆盖者：近一年 SLAM 综述提供领域全景基础事实 |
| ea-hardware-teleop-device | core | `all:teleoperation AND all:"data collection" AND all:robot` | Find hardware routes used to collect robot demonstrations. |
| ea-hardware-slam-demonstration | tracking | `all:SLAM AND all:"robot manipulation" AND all:demonstration` | Capture tracking and reconstruction limitations in collection devices. |
| ea-hardware-arkit-tracking | tracking | `all:ARKit AND all:robot AND all:tracking` | Find low-cost pose-tracking and VIO routes relevant to data capture. |
| ea-hardware-handheld-gripper | device-language | `(all:"handheld gripper" OR all:"hand-held gripper") AND all:robot` | Catch UMI-like collection devices that may not use UMI in metadata. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | dynamic-slam-vla-intersection, dynamic-gaussian-slam, dynamic-gaussian-robotic-mapping, dynamic-mapless-navigation, dynamic-spatial-memory-robot, dynamic-language-map-navigation, dynamic-slam-teleoperation, dynamic-slam-manipulation, dynamic-endtoend-slam, dynamic-worldmodel-pathplanning, dynamic-spatial-intelligence, dynamic-vo-foundation, ea-hardware-handheld-gripper, ea-model-finetuning |
| direct-topic | 3 | persona-slam-engineer-robustness, persona-basic-slam-robot, persona-basic-slam-survey, ea-hardware-teleop-device, ea-model-vla, ea-model-named-foundation |
| mechanisms-and-interfaces | 3 | persona-slam-engineer-neural-frontend, persona-vla-implicit-navigation, ea-hardware-slam-demonstration, ea-hardware-arkit-tracking, ea-model-action-tokenization |
| limits-and-counterevidence | 3 | persona-vla-mapfree, persona-vla-worldmodel-replace-map, persona-counter-dynamic-failure, persona-counter-implicit-memory |
| deployment-and-operations | 3 | persona-auditor-teleop-pose, persona-auditor-camera-relocalization |
| evaluation-and-validation | 3 | persona-auditor-ground-truth |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dynamic-slam-vla-browser | `SLAM "vision-language-action" robot pose` | SLAM×VLA 交集在 arXiv 元数据中可能稀疏，浏览器检索覆盖博客与项目页。 |
| dynamic-slam-dead-debate-browser | `"SLAM" "embodied AI" role debate 2026` | 核实辩论双方近一年的公开措辞，仅作术语校准。 |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dynamic-slam-embodied-web | llm | `SLAM embodied AI "core role" 2026` | 校准正方措辞。 |
| dynamic-mapless-web | web-calibration | `mapless navigation "spatial memory" robot 2026` | 校准反方措辞。 |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dynamic-slam-vla-intersection | arxiv_api | web-calibration | high | `all:SLAM AND all:"vision-language-action"` | 近一年出现直接讨论 SLAM 与 VLA 关系的论文（SLAM 作为 VLA 训练/评测/部署的隐形底座），静态分类法没有该交集。 |
| dynamic-gaussian-slam | arxiv_api | web-calibration | high | `all:"Gaussian splatting" AND all:SLAM` | 3DGS-SLAM 是近一年 SLAM 前沿主线之一（compact 3DGS dense SLAM、Splat-SLAM、LEG-SLAM），用于机器人实时建图。 |
| dynamic-gaussian-robotic-mapping | arxiv_api | web-calibration | medium | `all:"Gaussian splatting" AND all:mapping AND all:robot` | GaussLite 等任务条件化在线 3DGS 建图把地图与具身任务耦合，是 SLAM 在具身侧的新形态。 |
| dynamic-mapless-navigation | arxiv_api | web-calibration | high | `all:mapless AND all:navigation AND all:robot` | mapless/map-free 导航是显式地图路线的主要反方证据来源。 |
| dynamic-spatial-memory-robot | arxiv_api | web-calibration | medium | `all:"spatial memory" AND all:robot` | 隐式/结构化空间记忆（SRU、稀疏记忆导航）被提出替代显式 SLAM 地图，是核心作用之争的关键邻接家族。 |
| dynamic-language-map-navigation | arxiv_api | web-calibration | medium | `all:"language map" AND all:navigation` | LAMP 等隐式语言场地图把语义地图神经化，覆盖 semantic SLAM 与语言导航的交叉。 |
| dynamic-slam-teleoperation | arxiv_api | llm | medium | `all:SLAM AND all:teleoperation` | SLAM 在数据采集侧（遥操作位姿恢复、手持采集器）的隐形角色，静态分类法仅从 UMI 角度覆盖。 |
| dynamic-slam-manipulation | arxiv_api | llm | medium | `all:SLAM AND all:manipulation` | 操作任务中 SLAM 的作用（物体级地图、位姿跟踪支撑抓取）是核心作用之争的操作侧证据。 |
| dynamic-endtoend-slam | arxiv_api | llm | medium | `all:"end-to-end" AND all:SLAM` | 端到端/深度 SLAM 路线检验学习化是否正在替代模块化 SLAM 栈。 |
| dynamic-worldmodel-pathplanning | arxiv_api | web-calibration | medium | `all:"world model" AND all:"path planning" AND all:robot` | Target-Bench 等工作直接评测世界模型能否做 mapless 路径规划，是地图替代路线的评测证据。 |
| dynamic-spatial-intelligence | arxiv_api | llm | medium | `all:"spatial intelligence" AND all:robot` | spatial intelligence 是近一年把定位建图能力重新包装进具身基础模型话语的术语。 |
| dynamic-vo-foundation | arxiv_api | llm | medium | `all:"visual odometry" AND all:"foundation model"` | 基础模型化视觉里程计（学习化前端）检验 SLAM 前端是否被大模型吸收。 |
| dynamic-slam-vla-browser | browser_fallback | web-calibration | medium | `SLAM "vision-language-action" robot pose` | SLAM×VLA 交集在 arXiv 元数据中可能稀疏，浏览器检索覆盖博客与项目页。 |
| dynamic-slam-dead-debate-browser | browser_fallback | llm | low | `"SLAM" "embodied AI" role debate 2026` | 核实辩论双方近一年的公开措辞，仅作术语校准。 |
| dynamic-slam-embodied-web | web_calibration | llm | low | `SLAM embodied AI "core role" 2026` | 校准正方措辞。 |
| dynamic-mapless-web | web_calibration | web-calibration | low | `mapless navigation "spatial memory" robot 2026` | 校准反方措辞。 |

## Personas

| ID | Name | Focus | Primary dimensions |
|---|---|---|---|
| P-SLAM-SYSTEM-ENGINEER | SLAM 系统工程师 | 从 SLAM 系统本体出发：近一年 SLAM 前端/后端在学习化、3DGS/神经隐式表示、实时性上的演进，以及这些形态是否被具身任务实际采用 | direct-topic, mechanisms-and-interfaces |
| P-VLA-RESEARCHER | VLA 与世界模型研究者 | 检验端到端具身模型是否正在内化空间能力（隐式记忆、mapless 导航、世界模型路径规划），从而绕开显式 SLAM 地图 | mechanisms-and-interfaces, limits-and-counterevidence |
| P-DATA-INFRA-AUDITOR | 数据基础设施审计员 | 清点 SLAM 在具身数据采集、位姿真值与评测协议中的隐形角色：遥操作位姿恢复、手持采集、SLAM-based ground truth、相机重定位 | deployment-and-operations, evaluation-and-validation |
| P-COUNTER-EVIDENCE-SEEKER | 反面证据搜寻者 | 主动寻找 SLAM 失效、被绕开、被替代的证据：动态环境失败、长时漂移、地图维护成本、map-free 路线的成功案例、SLAM 被降级为可插拔组件的部署实践 | limits-and-counterevidence |
| P-BASIC-FACTS | 基础事实覆盖者 | 广泛覆盖主题基础事实：SLAM 与机器人/具身智能的总体交集、综述、基准与教程性材料 | direct-topic |

## Persona Queries

| Label | Persona | Tier | Dimension | Query | Why |
|---|---|---|---|---|---|
| persona-slam-engineer-robustness | P-SLAM-SYSTEM-ENGINEER | persona-direct | direct-topic | `all:"visual SLAM" AND all:robustness` | SLAM 系统工程师：定位近一年 SLAM 鲁棒性进展本身 |
| persona-slam-engineer-neural-frontend | P-SLAM-SYSTEM-ENGINEER | persona-method | mechanisms-and-interfaces | `all:SLAM AND all:"neural" AND all:real-time` | SLAM 系统工程师：神经化组件（学习特征/匹配/深度）进入实时 SLAM 栈的证据 |
| persona-vla-implicit-navigation | P-VLA-RESEARCHER | persona-method | mechanisms-and-interfaces | `all:"vision-language-action" AND all:navigation` | VLA 研究者：VLA 是否直接承担导航与空间任务 |
| persona-vla-mapfree | P-VLA-RESEARCHER | persona-limit | limits-and-counterevidence | `all:"map-free" AND all:navigation` | VLA 研究者：map-free 路线声称无需显式地图即可导航 |
| persona-vla-worldmodel-replace-map | P-VLA-RESEARCHER | persona-limit | limits-and-counterevidence | `all:"world model" AND all:mapping AND all:navigation` | VLA 研究者：世界模型是否以生成式地图替代 SLAM 建图 |
| persona-auditor-teleop-pose | P-DATA-INFRA-AUDITOR | persona-deploy | deployment-and-operations | `all:teleoperation AND all:"pose tracking"` | 数据基础设施审计员：遥操作/示教采集中位姿跟踪的部署证据 |
| persona-auditor-ground-truth | P-DATA-INFRA-AUDITOR | persona-eval | evaluation-and-validation | `all:SLAM AND all:"ground truth"` | 数据基础设施审计员：SLAM 作为评测真值生产工具的可靠性边界 |
| persona-auditor-camera-relocalization | P-DATA-INFRA-AUDITOR | persona-deploy | deployment-and-operations | `all:relocalization AND all:robot` | 数据基础设施审计员：相机重定位在机器人数据管线中的角色 |
| persona-counter-dynamic-failure | P-COUNTER-EVIDENCE-SEEKER | persona-limit | limits-and-counterevidence | `all:SLAM AND all:failure AND all:dynamic` | 反面证据搜寻者：动态环境与失效模式证据 |
| persona-counter-implicit-memory | P-COUNTER-EVIDENCE-SEEKER | persona-limit | limits-and-counterevidence | `all:"implicit memory" AND all:navigation` | 反面证据搜寻者：隐式记忆路线宣称替代显式地图的反方证据 |
| persona-basic-slam-robot | P-BASIC-FACTS | persona-direct | direct-topic | `all:SLAM AND all:robot AND all:embodied` | 基础事实覆盖者：SLAM 与具身智能的总体交集 |
| persona-basic-slam-survey | P-BASIC-FACTS | persona-direct | direct-topic | `all:"simultaneous localization and mapping" AND all:survey` | 基础事实覆盖者：近一年 SLAM 综述提供领域全景基础事实 |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- web-calibration dynamic expansion (medium): 2026-09-03 校准：发现 SLAM-as-VLA-infrastructure（From Pixels to Actions: The Hidden Role of SLAM in VLA）、SLAM as embodied operator、3DGS-SLAM（GaussLite/LEG-SLAM/compact 3DGS SLAM）、mapless/implicit-memory 反方路线（SRU mapless RL、LAMP implicit language map、Target-Bench mapless world-model planning、PanoNav）等术语簇，均不在静态分类法中。
- llm dynamic expansion (medium): 主题为辩论型（SLAM 是否核心），需要同时覆盖正方（SLAM 作为位姿/地图基础设施）与反方（端到端隐式空间能力替代显式地图）术语。
