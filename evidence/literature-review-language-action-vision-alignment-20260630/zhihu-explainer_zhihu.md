# 为什么“语言稀疏、动作连续、图像稠密”会让 VLA 对齐变难？

## TL;DR

这个问题不是“多喂点图文动作数据”就能解决。语言通常只告诉机器人目标，图像每帧给出海量细节，动作却必须连续、闭环、可执行。三者的粒度和物理含义不一致，才是 VLA 对齐的核心难点。

## 一句话解释

普通图文模型解决的是“这张图和这句话是否对应”。机器人 VLA 要解决的是“这句话指定的目标，在这段视觉变化中，应转化成哪条连续、可控、可安全执行的动作轨迹”。后者多了时间、控制器、本体、接触和失败恢复。

## 常见误区

误区一：语言已经输入模型，所以语言就参与了控制。LA4VLA 指出，VLA 训练中 dense 视觉—动作 supervision 可能压过 sparse 语言—动作 signal，模型看起来听懂指令，内部却可能依赖视觉捷径（[相关研究](https://arxiv.org/abs/2606.27295)）。

误区二：动作离散成 表征单元 后就和语言一样了。SA-VLA 说明，动作标记 还要解码成连续控制；同一个 表征单元 在不同机器人状态和接触条件下应该对应不同控制量（[相关研究](https://arxiv.org/abs/2606.30113)）。

误区三：视觉越密越好。Sparse2Act 和 SSI-Policy 的共同点不是增加视觉 表征单元，而是把视觉变成动作相关的几何/场景接口（[相关研究](https://arxiv.org/abs/2606.12759), 相关研究）。

## 真实机制

第一，增强语言-动作监督。LA4VLA 把轨迹拆成 atomic action segments 并配低层动作描述；ZR-0 用 dense embodied chain-of-thought 把场景、进度、计划、子任务和动作监督压到更细粒度（[相关研究](https://arxiv.org/abs/2606.27295), 相关研究）。

第二，给动作模块独立的物理先验。Learning Action Priors 先让 action module 从动作轨迹中学习 temporal motion structure，再接入 VLA 对齐；这等于承认 VLM 的视觉语言先验不会自动变成 运动先验（[相关研究](https://arxiv.org/abs/2606.26095)）。

第三，给视觉一个结构化出口。Sparse2Act 用 end-effector action 监督 3D 表征单元s；SSI-Policy 用 structured scene interface 连接 RGB、语言 grounding 和 motion trajectory（[相关研究](https://arxiv.org/abs/2606.12759), 相关研究）。

第四，把 action 从“命令”改写成“状态变化 + 适配器”。SPACE 指出，同一 action command 在不同机器人上可能产生不同 motion，所以用 Cartesian state delta 作为共享表示，再用 Action Adapter 落到目标机器人（[相关研究](https://arxiv.org/abs/2606.24049)）。

第五，补上视觉看不见的接触。Transferring Contact, Not Just Motion 说明，灵巧操作里对齐 motion 不等于对齐 contact；视觉自遮挡时需要力/触觉/本体感受（[相关研究](https://arxiv.org/abs/2606.15516)）。

## 结论

VLA 的下一步不是单纯更大的视觉语言模型，而是更好的接口工程：阶段级语言、动作先验、结构化视觉、状态条件 表征单元izer、跨本体 adapter、触觉/力闭环。把这几件事做好，模型才有机会从“看起来懂任务”走向“真的能稳定执行”。

## 一个反例：指令听懂了，动作仍然会错

设想机器人听到“把杯子轻轻放到盘子里”。语言层已经识别目标，视觉也定位了杯盘，但动作模块若把“轻轻”压缩成固定标记，在不同杯重和接触状态下仍输出同一速度，结果可能碰撞。这里不是语义理解失败，而是语言约束没有进入连续控制。

跨机器人时问题更明显。同一末端位移需要不同关节动作和控制频率；若数据只保存抽象动作名，模型会把平台差异误当成随机噪声。共享状态变化可以提供中间语义，具体控制仍需机器人适配器落地。

## 边界：接口更复杂也会引入新误差

阶段语言、结构化视觉和动作适配器都能降低对齐负担，却增加标注、感知与系统维护成本。单目深度可能漂移，阶段标签可能不准，适配器也会在新硬件上失配。评价一项改进时，需要同时报告闭环收益、延迟和新增故障点，不能只看离线动作误差。

## References

近六个月证据：LA4VLA ([2606.27295](https://arxiv.org/abs/2606.27295)); ZR-0 ([2606.30552](https://arxiv.org/abs/2606.30552)); SA-VLA ([2606.30113](https://arxiv.org/abs/2606.30113)); Sparse2Act ([2606.12759](https://arxiv.org/abs/2606.12759)); SSI-Policy ([2606.26800](https://arxiv.org/abs/2606.26800)); SPACE ([2606.24049](https://arxiv.org/abs/2606.24049)); Contact Not Just Motion ([2606.15516](https://arxiv.org/abs/2606.15516)).
