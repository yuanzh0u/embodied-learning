# 机器人不是“看错了”，而是“没摸到真相”

近半年具身智能论文里，一个很清楚的信号是：机器人失败不只是摄像头识别错了，更多是接触状态、局部扰动和模型不确定性没有被及时观测到。[2607.07287](https://arxiv.org/abs/2607.07287) Trace: [EA-SENSOR-2026-0001](evidence-appendix.md#ea-sensor-2026-0001).

1. 视觉能告诉机器人“这是什么”，但不稳定地告诉它“手指和物体之间发生了什么”。滑移、力不匹配、接触稳定性这类状态需要触觉/力觉补上。[2607.07287](https://arxiv.org/abs/2607.07287), [2606.30988](https://arxiv.org/abs/2606.30988) Trace: [EA-SENSOR-2026-0001](evidence-appendix.md#ea-sensor-2026-0001), [EA-SENSOR-2026-0010](evidence-appendix.md#ea-sensor-2026-0010).

2. 遮挡、弱光、反光、透明物体会让位姿估计掉坑。YOTO 用单次触觉接触做 6-DoF pose，就是在补视觉不可靠时的最后一块物理证据。[2606.28899](https://arxiv.org/abs/2606.28899) Trace: [EA-SENSOR-2026-0006](evidence-appendix.md#ea-sensor-2026-0006).

3. 多传感器不是越多越好。RGB-S 需要处理标定和运动学误差；Tactile-WAM 还提醒，无约束触觉 token 可能污染视觉世界模型。[2606.08765](https://arxiv.org/abs/2606.08765), [2606.26663](https://arxiv.org/abs/2606.26663) Trace: [EA-SENSOR-2026-0002](evidence-appendix.md#ea-sensor-2026-0002), [EA-SENSOR-2026-0008](evidence-appendix.md#ea-sensor-2026-0008).

4. 真部署要看“它知不知道自己快失败”。两篇 VLA 不确定性论文都在做这件事：把模型的犹豫变成失败检测信号。[2606.20754](https://arxiv.org/abs/2606.20754), [2606.18043](https://arxiv.org/abs/2606.18043) Trace: [EA-SENSOR-2026-0003](evidence-appendix.md#ea-sensor-2026-0003), [EA-SENSOR-2026-0004](evidence-appendix.md#ea-sensor-2026-0004).

5. 成功率会骗人。柔性物操作里，东西到了目标位置但滑了、掉了、变形了，也不能算可靠；世界模型视频很逼真，也不代表它能当闭环评测裁判。[2607.04234](https://arxiv.org/abs/2607.04234), [2607.07196](https://arxiv.org/abs/2607.07196) Trace: [EA-EVAL-2026-0007](evidence-appendix.md#ea-eval-2026-0007), [EA-EVAL-2026-0012](evidence-appendix.md#ea-eval-2026-0012).

一句话 caveat：这不是“所有任务都必须上触觉”，而是先按任务误差预算判断哪里不可观测，再决定补视觉、触觉、力觉、事件流，还是补评测指标。Trace: [EA-SENSOR-2026-0008](evidence-appendix.md#ea-sensor-2026-0008), [EA-EVAL-2026-0007](evidence-appendix.md#ea-eval-2026-0007).

## References

- [2606.08765](https://arxiv.org/abs/2606.08765) RGB-S.
- [2606.18043](https://arxiv.org/abs/2606.18043) Flow-based VLA uncertainty.
- [2606.20754](https://arxiv.org/abs/2606.20754) Perturbation-based VLA uncertainty.
- [2606.26663](https://arxiv.org/abs/2606.26663) Tactile-WAM.
- [2606.28899](https://arxiv.org/abs/2606.28899) YOTO tactile pose.
- [2606.30988](https://arxiv.org/abs/2606.30988) MuSe force adaptation.
- [2607.04234](https://arxiv.org/abs/2607.04234) SoftVTBench.
- [2607.07196](https://arxiv.org/abs/2607.07196) World-model admissibility.
- [2607.07287](https://arxiv.org/abs/2607.07287) TouchWorld.

完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。
