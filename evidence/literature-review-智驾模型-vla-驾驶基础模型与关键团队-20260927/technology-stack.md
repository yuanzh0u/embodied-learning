# 技术栈对照表

验证标签按实际协议填写。延迟/FPS为论文指定硬件和配置的报告值，本次没有复现实测；GPU名称不等于汽车计算平台。每行完整定位见同ID的论文笔记，方法细节未披露时不补猜。

| 工作 | 输入与数据 | 表征/骨干 | 推理、规划与输出 | 训练、后训练及数据迭代 | 验证层级 | 成本、开放程度及限制 |
|---|---|---|---|---|---|---|
| [UniAD](https://arxiv.org/abs/2212.10156v2) | 多相机时序、导航；nuScenes | BEVFormer；追踪/地图/运动/占据 query | ego query→路点→占据约束优化 | 感知预训练→全任务联合；中间任务显式监督 | 开放环规划及模块任务 | 多任务/历史计算高；[代码](https://github.com/OpenDriveLab/UniAD) |
| [Rethinking Open-Loop Evaluation / AD-MLP](https://arxiv.org/abs/2305.10430v2) | 自车历史、速度、加速度、未来导出的导航标签 | 小型 MLP；没有环境感知 | 未来位姿/路点 | 轨迹监督；分析轨迹偏置与碰撞栅格 | nuScenes 开放环反证 | 不可实际驾驶；V100 训练，不是部署推荐 |
| [NAVSIM](https://arxiv.org/abs/2406.15349v2) | OpenScene 相机/LiDAR与状态；筛掉简单和异常场景 | 评测框架，不固定骨干 | 初始一次预测→固定轨迹仿真→PDMS | 标准化划分/重训基线；非策略训练方法 | 非反应式，无策略重规划反馈 | 本文为1.x；[代码](https://github.com/autonomousvision/navsim) 当前版本须另锁定 |
| [LingoQA](https://arxiv.org/abs/2312.14115v4) | 前视视频；action/scenery QA | CLIP→Q-Former→Vicuna-7B | 视频问题→文字答案；Lingo-Judge 判答案 | 通用图文对齐→驾驶 QA；人工描述与自动扩写 | 驾驶理解/VQA，不输出驾驶轨迹 | 未报告本报告可对照的车端控制时延；Wayve 数据/评估器 |
| [DriveLM](https://arxiv.org/abs/2312.14150v3) | 前视图、QA 图；nuScenes/CARLA | BLIP-2；行为和 motion 独立 LoRA | 多轮图 QA→行为→离散路点 | 人工+规则 QA；PDM-lite 特权专家生成数据 | GVQA、开放环、跨域配置迁移 | 多轮推理慢；不能以 CARLA 数据宣称闭环 |
| [LMDrive](https://arxiv.org/abs/2312.07488v2) | 多相机+LiDAR+自然语言导航/提醒 | ResNet50/PointPillars→BEV→Q-Former→LLaMA 系 | MLP 路点与指令完成标志→PID控制 | 特权专家采集→模板/ChatGPT 指令；视觉预训练后训练接口 | CARLA LangAuto 交互闭环 | 模型冻结边界见§4.3；非实车部署 |
| [DriveVLM / DriveVLM-Dual](https://arxiv.org/abs/2402.12289v5) | 图像、导航与状态；SUP-AD/nuScenes | ViT+Qwen-VL；Dual 外接3D感知 | 场景/关键物体/分层规划→低频轨迹→高频规划器 | 场景描述/分析/动作监督；标注含私有数据 | 开放环、消融、实车展示 | 论文§6：双 OrinX 分工；VLM平均410ms，不能等同整车周期 |
| [EMMA](https://arxiv.org/abs/2410.23262v3) | 相机短历史+状态/导航文本；公开及内部驾驶数据 | Gemini1.0 Nano-1为主；统一语言空间 | 提示控制任务→数值文本轨迹/3D框/路网；可选CoT | 任务联合、内部预训练；关键物体/元决策监督 | 公开/内部离线任务及CoT消融 | 闭源骨干及内部数据；EMMA+和常规EMMA需分开 |
| [ORION](https://arxiv.org/abs/2503.19755v1) | 多相机历史、导航；Bench2Drive/Chat-B2D | EVA02-L→QT-Former记忆→Vicuna1.5 LoRA | planning token→VAE分布→GRU轨迹 | 视觉语言对齐→动作对齐→VQA/规划联合；自动QA | Bench2Drive交互闭环，另有nuScenes | 大视觉+LLM开销；[训练代码/数据](https://github.com/xiaomi-mlab/Orion) |
| [SimLingo](https://arxiv.org/abs/2503.09594v1) | 单相机、速度、目标点或高层指令；PDM-lite数据 | InternVL2-1B：InternViT300M+Qwen2-0.5B | 文字自回归；动作查询并行路径/速度路点→PID | 同场景多指令 Action Dreaming；QA/commentary/动作联合 | Bench2Drive闭环、VQA、语言动作测试 | [代码/数据/模型](https://github.com/RenzKa/simlingo)；官方榜BASE无语言 |
| [AutoVLA](https://arxiv.org/abs/2506.13757v3) | 前视多相机历史、状态和导航；多驾驶集 | Qwen2.5-VL3B；物理运动码本 | 同一自回归序列生成CoT及动作token；快/慢模式 | VLM自动推理标签→混合SFT→GRPO/长度约束 | 离线、NAVSIM非反应式；CARLA是SFT配置 | 高GPU需求；oracle best-of-N单列；[代码入口/数据待发](https://autovla.github.io/) |
| [Alpamayo-R1](https://arxiv.org/abs/2511.00088v2) | 多相机时序+ego；CoC与跨地区驾驶数据 | Cosmos-Reason；VLM KV cache→连续动作专家 | 训练用离散控制token；推理flow matching输出加速度/曲率并积分 | 人工/自动因果标签→动作注入/SFT→推理/一致性/轨迹奖励 | 离线、AlpaSim ego闭环（背景日志回放）、车载演示 | 论文RTX6000ProBlackwell延迟不可与Orin比；[release功能缺项](https://github.com/NVlabs/alpamayo) |
| [Orion-Lite](https://arxiv.org/abs/2604.08266v1) | 沿用ORION视觉输入/teacher特征与真值轨迹 | 冻结视觉与QT-Former；0.1B浅层decoder | 推理无提示/大LLM→planning feature→VAE规划 | 特征模仿+真值轨迹及规划约束联合；依赖VLA教师 | Bench2Drive闭环；训练配置消融 | 视觉成为瓶颈；模块150×不是系统150×；[当前已开源](https://github.com/tue-mps/Orion-Lite) |
| [DiffusionDrive](https://arxiv.org/abs/2411.15139v3) | NAVSIM前向三相机+栅格LiDAR；nuScenes另配置 | TransFuser R34；nuScenes用SparseDrive R50 | 锚点加噪→级联截断扩散→学习置信度top1 | 训练集K-means锚点；轨迹重建+分类监督；无需LLM | NAVSIM非反应式、nuScenes开放环 | 论文45FPS/RTX4090（NAVSIM配置），非车载认证；[两套权重](https://github.com/hustvl/DiffusionDrive) |
| [DiMA](https://arxiv.org/abs/2501.09757v1) | 多相机历史；nuScenes/DriveLM及扩展QA | 共享VAD/UniAD编码器；4类Q-Former接LLaVA7B | 默认视觉planner独立推理；Dual可选MLLM | 视觉预训→VQA/规划/重建/未来BEV/场景编辑/特征蒸馏 | 开放环全量、转弯与挑选长尾 | 训练大模型可不在车端运行；无闭环部署证明 |
| [OpenDriveVLA](https://arxiv.org/abs/2503.23463v2) | nuScenes相机/状态；多来源驾驶QA | R101+3D场景/agent/map查询→三projector→Qwen2.5 | 隐式推理；自回归文本路点 | 对齐→指令→交互→联合轨迹训练 | 驾驶问答与nuScenes开放环 | ST-P3/UniAD协议分开；ego输入和模型规模影响大 |
| [MindDrive (Fu et al.)](https://arxiv.org/abs/2512.13636v4) | 多相机+导航；Chat-B2D和规划QA | EVA02-L、Qwen0.5/3B；两套LoRA专家 | 离散纵横meta-actions→VAE+GRU路径/速度 | IL建立映射→CARLA rollout→PPO+KL更新决策/价值网络 | Bench2Drive交互闭环及奖励/轮数消融 | 32×A800训练，24仿真采集；无实车RL；不能与同名2512.04441混淆 |
| [nuReasoning / nuVLA](https://arxiv.org/abs/2605.31572v1) | Motional日志→难例挖掘；多相机、LiDAR、地图标签 | nuVLA：Qwen3-VL2B+flow-matching DiT | 测试关闭显式推理文字，输出5秒轨迹 | 自动空间/决策/反事实标注→人工复核纠错→语言与轨迹联合 | 理解与NPS开放环分开；Alpamayo为零样本 | 8×A100训练；有限城市；不是直接与NAVSIM同分制 |
| [Is VLA Reasoning Faithful?](https://arxiv.org/abs/2605.17268v2) | PhysicalAI-AV100片段、三随机种子 | 固定Alpamayo-R1-10B；关键词与运动学谓词 | 审计理由、实体、轨迹及扰动响应 | 不训练策略；小样本人工核验关键词提取 | 离线一致性/扰动分析 | 非道路安全统计；关键词/阈值和模型范围限制 |
| [FlashDrive](https://arxiv.org/abs/2608.12932v1) | PhysicalAI-AV连续滑窗；Alpamayo1.5为主 | 缓存视觉与KV；推测解码；动作flow步数复用 | W4A8 VLM、BF16动作专家、CUDA Graph | 流式适配动作专家、训练draft model；未重建底座 | 离线及100片段AlpaSim；Wrong Lane退化 | 论文同RTX PRO6000：717→151ms；配置不同，不与AR1原论文99ms横比 |
| [Tesla 企业披露](https://www.tesla.com/hr_hr/event/tesla-x-cvpr-2026) | 车队数据/视觉；筛选流程仅概述 | 2023视觉foundation到2026多模态pixels-to-actuation；具体骨干未披露 | end-to-end driving policy；执行接口细节未披露；未证实LLM在线参与 | 车队筛选；v14.3披露RL/视觉编码/编译运行时更新；标注与奖励细节缺失 | 产品/演示及公司自报；与论文基准分开 | 闭源；参数量/输入窗/损失/车端延迟分布缺项；视频生成是另列用途 |
| [Waymo 企业披露](https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving/) | 相机、LiDAR、雷达时序；驾驶数据 | sensor fusion encoder＋Gemini训练的driving VLM | 快慢表征→world decoder；Driver有轨迹验证层 | teacher/student；Simulator/Critic反馈；内外循环 | 公司公开生产与仿真流程，非本文独立验证 | Foundation/world/VLM功能交叉；闭源模块细节、车端具体规模缺项 |
