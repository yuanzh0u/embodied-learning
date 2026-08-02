# 机器人数据质量，不是“多采点数据”这么简单

这一版只保留已在完整正文中重新核对过的论文结论。


过去一年具身智能论文给出的信号很一致：机器人数据质量正在从“清洗坏轨迹”变成一整套闭环工程。好数据不是看起来干净，而是对目标策略真的有用（[Quality over Quantity](https://arxiv.org/abs/2603.09056)）。

💡 成功轨迹也可能是坏数据。遥操作 episode 即使成功，也可能动作抖、反复纠正、靠近关节极限；[DQAF](https://arxiv.org/abs/2605.26349) 和 PSD metric 都在把这种“成功但不好学”的轨迹变成可测指标。

💡 采集工具本身会改写数据质量。UMI gripper 的力分布和人体工学会影响示教表现，VR 的输入设备和可视化也会改变动作策略；所以数据质量不是采完之后才开始（[Influence of Gripper Design](https://arxiv.org/abs/2603.17189)）。

💡 坏数据不一定要整条删除。[WARP-RM](https://arxiv.org/abs/2606.28320) 认为次优长轨迹里可能藏着高价值恢复片段，Ambient Diffusion Policy 也主张控制 suboptimal data 在训练时怎么贡献，而不是一删了之。

💡 人类视频和跨本体数据都要过“可执行性”这一关。PSI 用仿真过滤人类视频中的不可达轨迹和 grasp 不兼容问题，OXE-AugE 则指出跨本体数据还要看 robot/gripper 分布是否均衡。

💡 **好筛选不是只删差样本，还要保留可复用结构。** [SIEVE](https://arxiv.org/abs/2607.06442) 用半量示教与半量训练步数超过全量训练，关键是它保留了原语组合和转换接口的覆盖。

⚠️ 一句话总结：具身智能的数据质量可以拆成五层：采集接口、轨迹健康、目标相关性、覆盖均衡、训练时利用方式。现在还没有一个统一基准能把所有任务一把尺子量完，所以最靠谱的做法是先把这些维度拆开记录，再用闭环成功率校准。

高质量不是一个静态分数，而是数据进入目标策略后产生的可验证收益。

📚 依据：[Quality over Quantity](https://arxiv.org/abs/2603.09056) · [DQAF](https://arxiv.org/abs/2605.26349) · [Gripper Design](https://arxiv.org/abs/2603.17189) · [WARP-RM](https://arxiv.org/abs/2606.28320) · [SIEVE](https://arxiv.org/abs/2607.06442)。
