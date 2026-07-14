# 机器人看得清清楚楚,照样把事搞砸——这不是矛盾

## Hook

最新的探针实验发现:机器人失败时,它的"眼睛"经常是无辜的。视觉系统把物体位置看得明明白白,是"手"固执地重复训练时背下来的老动作。"看"和"想"必须分开算账（[EA-PVC-2026-0004](evidence-appendix.md#ea-pvc-2026-0004)）。

## 证据约束洞察

💡 感知对≠行动对:探针直接读出 VLA 内部对物体位置的表征是准的,失败出在动作头塌缩回记忆轨迹——"看对了,做错了"是可测量的事实([ProbeAct](https://arxiv.org/abs/2606.09740); [EA-PVC-2026-0004](evidence-appendix.md#ea-pvc-2026-0004))

💡 想得多≠做得好:让机器人写长篇"思考过程"再行动,反而引入误差复合;推理只有翻译成动作语言(末端轨迹、空间参照)才有用([Revisiting ECoT](https://arxiv.org/abs/2606.03784); [EA-PVC-2026-0002](evidence-appendix.md#ea-pvc-2026-0002))

💡 "思考"可以压缩 89%:把冗长推理蒸馏成几个潜变量 token,长程规划和失败恢复能力不掉,延迟大降——认知是独立的、可优化的一层([Fast-ThinkAct](https://arxiv.org/abs/2601.09708); [EA-PVC-2026-0001](evidence-appendix.md#ea-pvc-2026-0001))

💡 判断错和做错是两个账户:恢复系统里,VLM 判断"失败到哪个阶段"判错了,和纠正动作执行不到位,是分开统计的两种错([ReCoVLA](https://arxiv.org/abs/2606.09630); [EA-PVC-2026-0003](evidence-appendix.md#ea-pvc-2026-0003))

💡 地图没错,计划也能错:重建的地形完全准确,但规划器不问"洪水之后这条路还在吗"——执行时路线直接消失([PVWM](https://arxiv.org/abs/2607.00673); [EA-PVC-2026-0007](evidence-appendix.md#ea-pvc-2026-0007))

## 边界提醒

⚠️ 两层可区分但不独立——认知依赖的物体框、抓手位置本身会被检测误差和遮挡污染;跨机器人时动作语义错配还会同时伪装成两种错([SPACE](https://arxiv.org/abs/2606.24049); [EA-ALIGN-2026-0010](evidence-appendix.md#ea-align-2026-0010))。先验感知、再查数据、最后归因认知。

## 依据来源

📚 15 条正文级证据事件(2026-01 至 2026-07 arXiv 论文),完整清单与每条证据的立场/定位见 [evidence-appendix.md](evidence-appendix.md)

## References

- [ProbeAct](https://arxiv.org/abs/2606.09740)
- [Revisiting Embodied Chain-of-Thought](https://arxiv.org/abs/2606.03784)
- [Fast-ThinkAct](https://arxiv.org/abs/2601.09708)
- [ReCoVLA](https://arxiv.org/abs/2606.09630)
- [Path Planning in Physically Viable World Models](https://arxiv.org/abs/2607.00673)
- [SPACE](https://arxiv.org/abs/2606.24049)
