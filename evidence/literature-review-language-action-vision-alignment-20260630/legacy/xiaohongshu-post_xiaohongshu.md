# VLA 最难的不是“多模态”，是三种信号根本不同频

## Hook

机器人模型里，语言像任务单，图像像监控流，动作像电机控制。把它们都塞进 Transformer，不等于它们自动对齐。

## 5 个证据约束洞察

1. 语言太稀疏：很多轨迹只有一个任务指令，视觉-动作信号却逐帧出现，所以模型容易学视觉捷径。证据：LA4VLA `EA-ALIGN-2026-0008`。
2. 动作不是文字：action token 最后必须变成连续控制，同一个 token 在不同状态下不能含义固定。证据：SA-VLA `EA-ALIGN-2026-0004`。
3. 视觉太强也会坏事：真正有用的是 action-aligned 3D 或 structured scene interface，而不是无限堆图像 token。证据：Sparse2Act / SSI-Policy `EA-ALIGN-2026-0005`, `EA-ALIGN-2026-0006`。
4. VLM 不自带 motion prior：视觉语言先验强，不代表模型天然懂轨迹、速度、接触和控制。证据：Learning Action Priors `EA-ALIGN-2026-0003`。
5. 接触是盲区：灵巧操作里 motion 对齐不等于 contact 对齐，视觉遮挡后需要力/触觉/本体感受。证据：Transferring Contact, Not Just Motion `EA-ALIGN-2026-0009`。

## 边界提醒

这些结论主要来自 2025-12-30 到 2026-06-30 的机器人/VLA 论文。它们支持一个方向：VLA 要从“统一 token 输入输出”走向“语言、视觉、动作、接触各自有接口，再做显式对齐”。

## 来源

证据文件：`evidence.jsonl`。代表论文：LA4VLA ([2606.27295](https://arxiv.org/abs/2606.27295)); SA-VLA ([2606.30113](https://arxiv.org/abs/2606.30113)); Sparse2Act ([2606.12759](https://arxiv.org/abs/2606.12759)); SSI-Policy ([2606.26800](https://arxiv.org/abs/2606.26800)); Learning Action Priors ([2606.26095](https://arxiv.org/abs/2606.26095)).
