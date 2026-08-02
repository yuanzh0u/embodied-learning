# 机器人不是“看错了”，而是“没摸到真相”

这一版只保留已在完整正文中重新核对过的论文结论。


近半年具身智能论文里，一个很清楚的信号是：机器人失败不只是摄像头识别错了，更多是接触状态、局部扰动和模型不确定性没有被及时观测到。[TouchWorld](https://arxiv.org/abs/2607.07287) 把触觉用于预测和修正这类局部失败。

💡 视觉能告诉机器人“这是什么”，但不稳定地告诉它“手指和物体之间发生了什么”。滑移、力不匹配、接触稳定性这类状态需要触觉或力觉补上（[TouchWorld](https://arxiv.org/abs/2607.07287)）。

💡 遮挡、弱光、反光、透明物体会让位姿估计掉坑。[YOTO](https://arxiv.org/abs/2606.28899) 用单次触觉接触做 6-DoF 位姿估计，就是在补视觉不可靠时的最后一块物理证据。

💡 多传感器不是越多越好。RGB-S 需要处理标定和运动学误差；[Tactile-WAM](https://arxiv.org/abs/2606.26663) 还提醒，无约束触觉 token 可能污染视觉世界模型。

💡 真部署要看“它知不知道自己快失败”。[Perturbation-Based Uncertainty](https://arxiv.org/abs/2606.20754) 把模型的犹豫变成分布外失败检测信号。

💡 成功率会骗人。柔性物操作里，东西到了目标位置但滑了、掉了、变形了，也不能算可靠；[SoftVTBench](https://arxiv.org/abs/2607.04234) 因此把过程安全与任务完成分开评估。

⚠️ 边界是：这不是“所有任务都必须上触觉”，而是先按任务误差预算判断哪里不可观测，再决定补视觉、触觉、力觉、事件流，还是补评测指标。

判断一项方法是否有效，最后仍要回到真实动作结果。

📚 依据：[TouchWorld](https://arxiv.org/abs/2607.07287) · [YOTO](https://arxiv.org/abs/2606.28899) · [Tactile-WAM](https://arxiv.org/abs/2606.26663) · [Perturbation-Based Uncertainty](https://arxiv.org/abs/2606.20754) · [SoftVTBench](https://arxiv.org/abs/2607.04234)。
