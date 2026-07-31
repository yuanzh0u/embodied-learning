# 机器人接上 Agent，就能进厂打工了吗？🤖

研究了 2026 年近半年 1,250 条候选、深读并审计 32 篇论文后，我的结论是：

**真正的变化不是“大模型直接控制所有关节”，而是机器人长出了一个任务操作系统。**

它开始负责：

✅ 理解目标、拆任务
✅ 调用导航/抓取/VLA 等技能
✅ 维护状态和长期记忆
✅ 判断刚才是否成功
✅ 失败后重试、换计划或找人

底层的平衡、力控、碰撞保护、急停，依然要交给实时控制和独立安全系统。

## 近半年 4 个真进展

💡 **1️⃣ 分层成主流**

慢速语义推理 → 中频 VLA/技能 → 高频实时控制。Figure Helix 02 的公开架构甚至是慢推理、200 Hz 策略、1 kHz 全身控制三层。但四分钟视频仍是厂商演示，不是量产 KPI。[Figure](https://www.figure.ai/news/helix-02)

💡 **2️⃣ 成功检测成了核心能力**

论文发现：机器人失败时，LLM 可能仍“相信自己成功”，还会把错误写进记忆。[论文](https://arxiv.org/abs/2603.03148) Google 的新具身推理模型也把 success detection 单列出来，决定重试还是继续。[DeepMind](https://deepmind.google/blog/gemini-robotics-er-1-6/)

💡 **3️⃣ 记忆从聊天记录变成世界状态**

结构化记录对象、场景、动作转移和技能后，真实桌面任务平均成功率从 56% 提到 84%，检索准确率从 68% 提到 98%。[论文](https://arxiv.org/abs/2606.29774)

💡 **4️⃣ Agent 开始管理机器人研发流程**

数据生成、仿真、训练、评测、部署都被包装成软件智能体可调用技能。这条路线可回放、可审计，可能比直接控制接触动作更早赚钱。[NVIDIA](https://nvidianews.nvidia.com/news/nvidia-releases-major-collection-of-open-source-agent-tools-and-skills-for-physical-ai)

## 但别把“演示”当“落地”⚠️

⚠️ 厂商视频、客户协议和持续生产是三种不同证据，不能混写。

我把产业成熟度分 5 级：

L0 联合研发
L1 厂商演示/内部试点
L2 客户现场验证
L3 持续商业运行
L4 跨客户规模经济已证实

近半年的大多数新闻还在 L1—L2。

- Figure：强演示 + 配送中心集成协议，尚无公开生产指标。
- POSCO × NC AI：仍是联合开发和数字孪生验证。[POSCO](https://newsroom.posco.com/en/posco-dx-nc-ai-physical-ai-based-launch-of-joint-development-of-industrial-robot-foundation-model/)
- Pudu：新模型叠加在成熟服务机器人业务上，但既有 13 万台装机 ≠ 新模型已部署 13 万台。[Pudu](https://www.pudurobotics.com/en/news/pudu-robotics-unveils-pudufm-1-0-embodied-intelligence-foundation-model)
- Agility Digit：目前最接近 L3，已在仓储/制造环境做料箱搬运等窄任务；订单、部署、收入仍要分开看。[AP](https://apnews.com/article/39f2356b9c1e167d0985b821f70079c5)

## 真正的卡点

❌ 工具调用太慢：有系统每 5—10 秒才出一个动作。[论文](https://arxiv.org/abs/2603.05621)
❌ 轮询式 Agent 不能随时抢停长动作。[论文](https://arxiv.org/abs/2602.13081)
❌ 提示词里的“注意安全”替代不了深度、触觉和力控。
❌ 记忆写错一次，后面可能一直错。
❌ “预测视频看着对”不代表实际动作对。

## 我对未来半年的判断

最先产生稳定价值的会是：

🏭 棕地工厂/仓库的窄工作流
🔍 巡检、清洁、配送
🧪 仿真、数据、评测、部署自动化

不是“机器人有多像人”，而是它能否把一件真实工作：

**连续做完｜结果可验证｜失败可恢复｜成本算得过来。**

#具身智能 #AI智能体 #机器人 #人形机器人 #VLA #PhysicalAI #工业自动化
