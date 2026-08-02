# 触觉世界模型：机器人真正缺的不是眼睛，是“接触想象力”

这一版只保留已在完整正文中重新核对过的论文结论。


机器人看得再清楚，也不一定知道自己有没有摸到、会不会滑、力是不是太大。触觉世界模型要解决的，就是让机器人在动手前先预测接下来几百毫秒的接触变化（[Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001)）。

💡 触觉不是“近距离视觉”。它补的是接触、滑移、摩擦、局部变形、力变化这些视觉很难看到的状态。[Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) 展示了这种物理补充。

💡 不是加触觉就赢。[ContactWorld](https://arxiv.org/abs/2606.13877) 显示，空间结构、时间连续性和跨模态兼容性才是关键；真实机器人上触觉还会受标定和力推断噪声影响。

💡 力/力矩可能比指尖触觉更早报警。[TacForeSight](https://arxiv.org/abs/2606.11184) 用腕部力/力矩预测未来触觉潜在状态，在扰动任务里帮助机器人提前修正接触。

💡 数据比模型还难。[HapTile](https://arxiv.org/abs/2606.04825) 同时保留语言、视觉、触觉、状态、动作和触觉遥操数据；触觉世界模型吃的是交互过程，不是普通视频。

💡 真落地要进控制回路。[ViTaL](https://arxiv.org/abs/2606.14981) 用视觉—触觉潜在世界模型在推理期验证候选动作，而 OmniVTA 和 AT-VLA 分别强调反射式控制与高频触觉通道。

⚠️ 触觉世界模型最适合插入、旋拧、擦拭、柔顺接触、抓握恢复这些“最后几厘米”任务。它不是万能模块：传感器标定、跨硬件迁移、同步、控制频率和下游真实成功率，都会决定它到底有没有用。

是否值得增加触觉，最终要看它能否提前发现滑移、过力和接触丢失。

📚 依据：[Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) · [ContactWorld](https://arxiv.org/abs/2606.13877) · [TacForeSight](https://arxiv.org/abs/2606.11184) · [HapTile](https://arxiv.org/abs/2606.04825) · [ViTaL](https://arxiv.org/abs/2606.14981)。
