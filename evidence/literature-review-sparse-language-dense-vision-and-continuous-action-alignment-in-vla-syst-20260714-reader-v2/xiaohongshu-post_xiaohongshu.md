# VLA 最难的不是“多模态”，是三种信号根本不同频

这一版只保留已在完整正文中重新核对过的论文结论。


机器人模型里，语言像任务单，图像像监控流，动作像电机控制。把它们都塞进 Transformer，不等于它们自动对齐。

💡 动作不是文字：action token 最后必须变成连续控制，同一个 token 在不同状态下不能含义固定。证据：SA-VLA [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](https://arxiv.org/abs/2606.30113)。

💡 **语言对齐要落到动作表示。** [ERVLA](https://arxiv.org/abs/2606.03784) 显示，末端运动/图像轨迹类 CoT 更有用，长文本前缀会累积误差。

💡 **稠密视觉要有结构化出口。** [SSI-Policy](https://arxiv.org/abs/2606.26800) 把 RGB、语言 grounding 和运动轨迹串成可查询的场景接口。

💡 **跨机器人不能共用“字面相同”的动作。** [SPACE](https://arxiv.org/abs/2606.24049) 指出，控制命令必须连同坐标系和本体语义一起对齐。

💡 **接触错误要进纠错回路。** [TACO](https://arxiv.org/abs/2607.02840) 用视频+力的未来预测，把真实失败改写成可训练的纠正片段。

⚠️ 现有结论主要来自近期机器人/VLA 预印本，跨任务、跨控制器和跨本体的独立复现仍有限。它们支持一个方向：VLA 要从“统一 token 输入输出”走向“语言、视觉、动作、接触各自有接口，再做显式对齐”。

判断对齐是否成功，最后要看语言约束有没有真实改变连续动作。

📚 依据：[论文1](https://arxiv.org/abs/2606.30113) · [论文2](https://arxiv.org/abs/2606.03784) · [论文3](https://arxiv.org/abs/2606.26800) · [论文4](https://arxiv.org/abs/2606.24049) · [论文5](https://arxiv.org/abs/2607.02840)。
