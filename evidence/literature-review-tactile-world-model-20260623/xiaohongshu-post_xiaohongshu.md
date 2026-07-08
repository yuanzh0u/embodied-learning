# 触觉世界模型：机器人真正缺的不是眼睛，是“接触想象力”

## Hook

机器人看得再清楚，也不一定知道自己有没有摸到、会不会滑、力是不是太大。触觉世界模型要解决的，就是让机器人在动手前先预测接下来几百毫秒的接触变化（trace: `EA-TWM-2026-0003`, `EA-TWM-2026-0007`）。

## 证据约束洞察

1. 触觉不是“近距离视觉”。它补的是接触、滑移、摩擦、局部变形、力变化这些视觉很难看到的状态（`EA-SENSOR`; `EA-TWM-2026-0003`; stance: support）。

2. 不是加触觉就赢。ContactWorld 显示，空间结构、时间连续性和跨模态兼容性才是关键；真实机器人上触觉还会受标定和力推断噪声影响（`EA-TWM-2026-0001`, `EA-TWM-2026-0002`; stance: support/conditional）。

3. 力/力矩可能比指尖触觉更早报警。TacForeSight 用 wrist force/torque 预测未来触觉 latent，在扰动任务里帮助机器人提前修正接触（`EA-TWM-2026-0007`, `EA-TWM-2026-0008`; stance: support）。

4. 数据比模型还难。HapTile 有语言、视觉、触觉、状态、动作和 haptic teleoperation；TAMEn 强调失败恢复和可执行性检查。触觉世界模型吃的是交互过程，不是普通视频（`EA-TWM-2026-0013`, `EA-TWM-2026-0014`; stance: support）。

5. 真落地要进控制回路。OmniVTA 做 60Hz 反射式触觉控制，ViTaL 用世界模型在推理期验证候选动作，AT-VLA 把触觉做成高频快流（`EA-TWM-2026-0006`, `EA-TWM-2026-0011`, `EA-TWM-2026-0016`; stance: support/conditional）。

6. 现在还没到“通用触觉大模型”。HT-Bench 有 10M RGB frames 和 7.8M tactile frames，但目前很多评测仍是表征级；ViTaL 也提醒世界模型预测误差会影响细微接触判断（`EA-TWM-2026-0012`, `EA-TWM-2026-0015`; stance: limit/gap）。

## 边界提醒

触觉世界模型最适合插入、旋拧、擦拭、柔顺接触、抓握恢复这些“最后几厘米”任务。它不是万能模块：传感器标定、跨硬件迁移、同步、控制频率和下游真实成功率，都会决定它到底有没有用（trace: `EA-TWM-2026-0002`, `EA-TWM-2026-0015`; inference: deployment caveat from evidence）。

## 一句话判断

一篇触觉世界模型论文是否靠谱，看它有没有回答四个问题：预测什么接触变量、用什么同步数据、怎么接入动作闭环、有没有真实扰动和长时域评测（trace: `EA-TWM-2026-0001`, `EA-TWM-2026-0004`, `EA-TWM-2026-0008`, `EA-TWM-2026-0015`; inference: checklist synthesized from evidence）。

## 依据来源

核心来源：ContactWorld、TacForeSight、OmniVTA、Visuo-Tactile World Models、Dream-Tac、ViTaL、HapTile、TAMEn、HT-Bench、AT-VLA、HapticVLA。检索时间窗：2025-12-23 至 2026-06-23；证据文件：`evidence.jsonl`。
