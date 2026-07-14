# 为什么“语言稀疏、动作连续、图像稠密”会让 VLA 对齐变难？

## TL;DR

这一版不只核对摘要，而是对 15 篇入选论文逐篇阅读方法、结果与局限。下文只保留能在完整正文中重新定位的判断。

这个问题不是“多喂点图文动作数据”就能解决。语言通常只告诉机器人目标，图像每帧给出海量细节，动作却必须连续、闭环、可执行。三者的粒度和物理含义不一致，才是 VLA 对齐的核心难点。

## 一句话解释

普通图文模型解决的是“这张图和这句话是否对应”。机器人 VLA 要解决的是“这句话指定的目标，在这段视觉变化中，应转化成哪条连续、可控、可安全执行的动作轨迹”。后者多了时间、控制器、本体、接触和失败恢复。

## 常见误区

误区二：动作离散成 token 后就和语言一样了。SA-VLA 说明，action token 还要解码成连续控制；同一个 token 在不同机器人状态和接触条件下应该对应不同控制量（[相关研究](https://arxiv.org/abs/2606.30113)）。

## 真实机制

第四，把 action 从“命令”改写成“状态变化 + 适配器”。SPACE 指出，同一 action command 在不同机器人上可能产生不同 motion，所以用 Cartesian state delta 作为共享表示，再用 Action Adapter 落到目标机器人（[相关研究](https://arxiv.org/abs/2606.24049)）。

## 精读后，这个问题可以拆成四关

第一关是语言能否落到动作上。[稠密具身 CoT](https://arxiv.org/abs/2606.30552) 把任务进度、子任务和动作监督拉到更细粒度；[ERVLA](https://arxiv.org/abs/2606.03784) 进一步表明，有用的推理必须指向末端运动或图像轨迹，长文本 CoT 直接做动作前缀反而会累积误差。

第二关是动作 token 能否回到正确的连续控制。[SA-VLA](https://arxiv.org/abs/2606.30113) 提醒我们，固定 token 的物理含义会随状态变化；[SPACE](https://arxiv.org/abs/2606.24049) 又表明，换了机器人本体，同一命令也未必产生同一运动。

第三关是稠密视觉能否变成结构化场景接口，[SSI-Policy](https://arxiv.org/abs/2606.26800) 就在做这件事。第四关是 RGB 看不见的接触能否进入纠错回路，[TACO](https://arxiv.org/abs/2607.02840) 用视频—力联合世界模型生成失败后的纠正数据。所以，所谓“对齐”并非一个 loss，而是四个接口是否同时闭环。

## 结论

VLA 的下一步不是单纯更大的视觉语言模型，而是更好的接口工程：阶段级语言、动作先验、结构化视觉、状态条件 tokenizer、跨本体 adapter、触觉/力闭环。把这几件事做好，模型才有机会从“看起来懂任务”走向“真的能稳定执行”。

## 一个反例：指令听懂了，动作仍然会错

设想机器人听到“把杯子轻轻放到盘子里”。语言层已经识别目标，视觉也定位了杯盘，但动作模块若把“轻轻”压缩成固定标记，在不同杯重和接触状态下仍输出同一速度，结果可能碰撞。这里不是语义理解失败，而是语言约束没有进入连续控制。

跨机器人时问题更明显。同一末端位移需要不同关节动作和控制频率；若数据只保存抽象动作名，模型会把平台差异误当成随机噪声。共享状态变化可以提供中间语义，具体控制仍需机器人适配器落地。

## 边界：接口更复杂也会引入新误差

阶段语言、结构化视觉和动作适配器都能降低对齐负担，却增加标注、感知与系统维护成本。单目深度可能漂移，阶段标签可能不准，适配器也会在新硬件上失配。评价一项改进时，需要同时报告闭环收益、延迟和新增故障点，不能只看离线动作误差。

一个实用检查法是逐层替换：先给定正确阶段标签，再给定真实空间状态，最后给定可执行动作。哪一步替换让机器人恢复，就优先修哪一个接口。这样才能区分“没听懂”“没看准”和“动作落不了地”，避免把三种问题都塞进同一个对齐分数。

## 延伸阅读
- [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113)
- [SPACE: Enabling Learning from Cross-Robot Data Toward Generalist Policies](https://arxiv.org/abs/2606.24049)
- [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](https://arxiv.org/abs/2606.30552)
- [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](https://arxiv.org/abs/2606.03784)
- [SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation](https://arxiv.org/abs/2606.26800)
- [TACO: TActile World Model as a Self-COrrector forScalable VLA Post-Training](https://arxiv.org/abs/2607.02840)
