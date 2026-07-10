# 机器人数据质量，不是“多采点数据”这么简单

过去一年具身智能论文给出的信号很一致：机器人数据质量正在从“清洗坏轨迹”变成一整套闭环工程。好数据不是看起来干净，而是对目标策略真的有用 [EA-DATA-2026-LY-0001](evidence-appendix.md#ea-data-2026-ly-0001), [EA-DATA-2026-LY-0007](evidence-appendix.md#ea-data-2026-ly-0007)。

1. 成功轨迹也可能是坏数据。遥操作 episode 即使成功，也可能动作抖、反复纠正、靠近关节极限；DQAF 和 PSD metric 都在把这种“成功但不好学”的轨迹变成可测指标 [EA-DATA-2026-LY-0002](evidence-appendix.md#ea-data-2026-ly-0002), [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003)。

2. 多样性不是万能药。FAKTUAL 说明 diversity 可以帮机器人泛化，但也承认高多样性不保证高质量；ATHENA 进一步提醒，VLA 数据筛选还要防止某些任务被筛没了 [EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004), [EA-DATA-2026-LY-0005](evidence-appendix.md#ea-data-2026-ly-0005)。

3. 采集工具本身会改写数据质量。UMI gripper 的力分布和人体工学会影响示教表现，VR 的输入设备和可视化也会改变动作策略；所以数据质量不是采完之后才开始 [EA-DATA-2026-LY-0009](evidence-appendix.md#ea-data-2026-ly-0009), [EA-DATA-2026-LY-0010](evidence-appendix.md#ea-data-2026-ly-0010)。

4. 坏数据不一定要整条删除。WARP-RM 认为次优长轨迹里可能藏着高价值恢复片段，Ambient Diffusion Policy 也主张控制 suboptimal data 在训练时怎么贡献，而不是一删了之 [EA-DATA-2026-LY-0006](evidence-appendix.md#ea-data-2026-ly-0006), [EA-DATA-2026-LY-0012](evidence-appendix.md#ea-data-2026-ly-0012)。

5. 人类视频和跨本体数据都要过“可执行性”这一关。PSI 用仿真过滤人类视频中的不可达轨迹和 grasp 不兼容问题，OXE-AugE 则指出跨本体数据还要看 robot/gripper 分布是否均衡 [EA-DATA-2026-LY-0008](evidence-appendix.md#ea-data-2026-ly-0008), [EA-DATA-2026-LY-0011](evidence-appendix.md#ea-data-2026-ly-0011)。

一句话总结：具身智能的数据质量可以拆成五层，采集接口、轨迹健康、目标相关性、覆盖均衡、训练时利用方式。现在还没有一个统一 benchmark 能把所有任务一把尺子量完，所以最靠谱的做法是先把这些维度拆开记录，再用闭环成功率校准 [EA-DATA-2026-LY-0003](evidence-appendix.md#ea-data-2026-ly-0003), [EA-DATA-2026-LY-0004](evidence-appendix.md#ea-data-2026-ly-0004), [EA-DATA-2026-LY-0012](evidence-appendix.md#ea-data-2026-ly-0012)。

## References

- [2509.01657](https://arxiv.org/abs/2509.01657) IWR.
- [2512.13100](https://arxiv.org/abs/2512.13100) OXE-AugE.
- [2602.10618](https://arxiv.org/abs/2602.10618) VR demonstration quality.
- [2602.13197](https://arxiv.org/abs/2602.13197) PSI.
- [2603.09056](https://arxiv.org/abs/2603.09056) QoQ.
- [2603.11634](https://arxiv.org/abs/2603.11634) FAKTUAL.
- [2603.17189](https://arxiv.org/abs/2603.17189) UMI gripper design.
- [2605.01544](https://arxiv.org/abs/2605.01544) PSD metric.
- [2605.26349](https://arxiv.org/abs/2605.26349) DQAF.
- [2606.12365](https://arxiv.org/abs/2606.12365) Ambient Diffusion Policy.
- [2606.16208](https://arxiv.org/abs/2606.16208) ATHENA.
- [2606.28320](https://arxiv.org/abs/2606.28320) WARP-RM.
