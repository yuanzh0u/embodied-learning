# Writing Brief: 近一年 loco-manipulation 研究进展

> 本文件是写作输入,不是交付物。三篇成稿交由 `$embodied-ai-review-writer` 独立撰写:
> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;
> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。
> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 trace-map/appendix 溯源。

## 范围

- Topic: 近一年 loco-manipulation 研究进展
- Time range: 2025-07-19 至 2026-07-19
- Knowledge IDs: `EA-MODEL`, `EA-EVAL`, `EA-XEMBODIMENT`, `EA-SENSOR`
- Review mode: scoping
- Paper-level sources: 21 / 15 floor (not a cap)
- Coverage and saturation gate: passed
- Writing readiness: formal-ready
- Unresolved checks: none
- Accepted events: 21

## 中心论点候选(从张力对中提炼,不要照抄)

综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?
以下 support ⟷ limit/conditional 张力对是论点候选的原料:

- `EA-MODEL`: In simulation, the NSDF-conditioned policy maintained 100% success for standard-mass cylinders, cuboids and spheres, wh... ([2509.13534](https://arxiv.org/abs/2509.13534) / [EA-LOCOMANIP-2026-0005](evidence-appendix.md#ea-locomanip-2026-0005)) ⟷ On the real curtain task, neither image policy completed any of 10 trials; retrieval reached the curtain in 2/10, while... ([2507.21796](https://arxiv.org/abs/2507.21796) / [EA-LOCOMANIP-2026-0001](evidence-appendix.md#ea-locomanip-2026-0001))
- `EA-MODEL`: Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human v... ([2512.11047](https://arxiv.org/abs/2512.11047) / [EA-LOCOMANIP-2026-0006](evidence-appendix.md#ea-locomanip-2026-0006)) ⟷ Kitchen-R's reported execution evaluation always uses the ground-truth plan to isolate execution from planning error, s... ([2508.15663](https://arxiv.org/abs/2508.15663) / [EA-LOCOMANIP-2026-0004](evidence-appendix.md#ea-locomanip-2026-0004))
- `EA-MODEL`: In a 15-minute comparison, HuMI collected 62 episodes versus 28 for TWIST2, with 96.7% versus 64.3% acceptance; time pe... ([2602.06643](https://arxiv.org/abs/2602.06643) / [EA-LOCOMANIP-2026-0008](evidence-appendix.md#ea-locomanip-2026-0008)) ⟷ Cross-simulator smoothness was not a reliable robustness signal: MuJoCo drifted under default friction, while near-zero... ([2512.18938](https://arxiv.org/abs/2512.18938) / [EA-LOCOMANIP-2026-0007](evidence-appendix.md#ea-locomanip-2026-0007))
- `EA-MODEL`: With 100 robot and 300 human demonstrations, co-training scored 78% versus 59% for robot-only in-domain, and 82% versus... ([2602.10106](https://arxiv.org/abs/2602.10106) / [EA-LOCOMANIP-2026-0009](evidence-appendix.md#ea-locomanip-2026-0009)) ⟷ On two real-world tasks, the same controller achieved 98% and 100% success under teleoperation, versus 80% and 85% when... ([2508.10538](https://arxiv.org/abs/2508.10538) / [EA-LOCOMANIP-2026-0002](evidence-appendix.md#ea-locomanip-2026-0002))
- `EA-MODEL`: On hardware, Sumo uprighted a 15 kg tire—heavier than Spot arm's stated 11 kg lifting capacity—in 10/10 trials, averagi... ([2604.08508](https://arxiv.org/abs/2604.08508) / [EA-LOCOMANIP-2026-0019](evidence-appendix.md#ea-locomanip-2026-0019)) ⟷ For two-box pick-and-place, the solver found the first goal-satisfying feasible plan after 30 of 200 tree expansions, w... ([2508.14099](https://arxiv.org/abs/2508.14099) / [EA-LOCOMANIP-2026-0003](evidence-appendix.md#ea-locomanip-2026-0003))
- `EA-MODEL`: On real cupboard opening, WHOLE-MoMa succeeded in 17/25 trials (68%), versus 4/25 for its WBC generator and 8/25 for be... ([2604.12509](https://arxiv.org/abs/2604.12509) / [EA-LOCOMANIP-2026-0011](evidence-appendix.md#ea-locomanip-2026-0011)) ⟷ On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric de... ([2603.03279](https://arxiv.org/abs/2603.03279) / [EA-LOCOMANIP-2026-0018](evidence-appendix.md#ea-locomanip-2026-0018))
- `EA-MODEL`: Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-in... ([2604.27224](https://arxiv.org/abs/2604.27224) / [EA-LOCOMANIP-2026-0012](evidence-appendix.md#ea-locomanip-2026-0012)) ⟷ The study reports a depth-only mobile-manipulation policy whose risk sensitivity can be adjusted at runtime while retai... ([2603.04579](https://arxiv.org/abs/2603.04579) / [EA-LOCOMANIP-2026-0010](evidence-appendix.md#ea-locomanip-2026-0010))
- `EA-MODEL`: Across nine simulated tasks, data generated from one source demonstration raised average policy performance from 0.33 f... ([2605.27724](https://arxiv.org/abs/2605.27724) / [EA-LOCOMANIP-2026-0013](evidence-appendix.md#ea-locomanip-2026-0013)) ⟷ In zero-shot transfer, pick-and-place scored 9/10 in simulation and 8/10 on hardware; handover scored 10/10 in simulati... ([2606.08278](https://arxiv.org/abs/2606.08278) / [EA-LOCOMANIP-2026-0015](evidence-appendix.md#ea-locomanip-2026-0015))

## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)

### EA-MODEL (21 events)
- [`support`] In simulation, the NSDF-conditioned policy maintained 100% success for standard-mass cylinders, cuboids and spheres, while removing NSDF produced 0% across those shapes. ([2509.13534](https://arxiv.org/abs/2509.13534) / [EA-LOCOMANIP-2026-0005](evidence-appendix.md#ea-locomanip-2026-0005))
- [`support`] Removing the unified latent action model reduced success by 38.7 percentage points, indicating that action-free human video contributed useful priors in the evaluated tasks. ([2512.11047](https://arxiv.org/abs/2512.11047) / [EA-LOCOMANIP-2026-0006](evidence-appendix.md#ea-locomanip-2026-0006))
- [`support`] In a 15-minute comparison, HuMI collected 62 episodes versus 28 for TWIST2, with 96.7% versus 64.3% acceptance; time per acceptable episode fell to 30.0% of TWIST2. ([2602.06643](https://arxiv.org/abs/2602.06643) / [EA-LOCOMANIP-2026-0008](evidence-appendix.md#ea-locomanip-2026-0008))
- [`support`] With 100 robot and 300 human demonstrations, co-training scored 78% versus 59% for robot-only in-domain, and 82% versus 31% under generalization. ([2602.10106](https://arxiv.org/abs/2602.10106) / [EA-LOCOMANIP-2026-0009](evidence-appendix.md#ea-locomanip-2026-0009))
- [`support`] On hardware, Sumo uprighted a 15 kg tire—heavier than Spot arm's stated 11 kg lifting capacity—in 10/10 trials, averaging 9.2±4.7 seconds. ([2604.08508](https://arxiv.org/abs/2604.08508) / [EA-LOCOMANIP-2026-0019](evidence-appendix.md#ea-locomanip-2026-0019))
- [`support`] On real cupboard opening, WHOLE-MoMa succeeded in 17/25 trials (68%), versus 4/25 for its WBC generator and 8/25 for behavior cloning. ([2604.12509](https://arxiv.org/abs/2604.12509) / [EA-LOCOMANIP-2026-0011](evidence-appendix.md#ea-locomanip-2026-0011))
- [`support`] Adding tactile-command tracking at the low level raised insertion success from 0.70 to 0.85, full reorientation-plus-insertion from 0.60 to 0.80, and valve tightening from 0.80 to 0.85. ([2604.27224](https://arxiv.org/abs/2604.27224) / [EA-LOCOMANIP-2026-0012](evidence-appendix.md#ea-locomanip-2026-0012))
- [`support`] Across nine simulated tasks, data generated from one source demonstration raised average policy performance from 0.33 for DexMimicGen+ to 0.89 for HumanoidMimicGen. ([2605.27724](https://arxiv.org/abs/2605.27724) / [EA-LOCOMANIP-2026-0013](evidence-appendix.md#ea-locomanip-2026-0013))
- [`support`] In a staged real long-horizon task, TA-WBC completed five consecutive bottle-pick, stair-climb, disposal and return runs without falls or stumbles. ([2605.31343](https://arxiv.org/abs/2605.31343) / [EA-LOCOMANIP-2026-0014](evidence-appendix.md#ea-locomanip-2026-0014))
- [`support`] On four tasks held out from whole-body teleoperation, stationary same-embodiment co-training raised average task progress from 33% to 87%, close to a 94% 12-task teleoperation oracle. ([2606.22174](https://arxiv.org/abs/2606.22174) / [EA-LOCOMANIP-2026-0020](evidence-appendix.md#ea-locomanip-2026-0020))
- [`support`] In 10 matched hardware trials, tactile-informed TAC-LOCO achieved 90% dynamic loco-manipulation success versus 50% for Deep WBC with a fixed gripper. ([2607.10132](https://arxiv.org/abs/2607.10132) / [EA-LOCOMANIP-2026-0021](evidence-appendix.md#ea-locomanip-2026-0021))
- [`conditional`] On two real-world tasks, the same controller achieved 98% and 100% success under teleoperation, versus 80% and 85% when driven by a diffusion policy. ([2508.10538](https://arxiv.org/abs/2508.10538) / [EA-LOCOMANIP-2026-0002](evidence-appendix.md#ea-locomanip-2026-0002))
- [`conditional`] For two-box pick-and-place, the solver found the first goal-satisfying feasible plan after 30 of 200 tree expansions, with an average solve time of 52.3 seconds. ([2508.14099](https://arxiv.org/abs/2508.14099) / [EA-LOCOMANIP-2026-0003](evidence-appendix.md#ea-locomanip-2026-0003))
- [`conditional`] On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively. ([2603.03279](https://arxiv.org/abs/2603.03279) / [EA-LOCOMANIP-2026-0018](evidence-appendix.md#ea-locomanip-2026-0018))
- [`conditional`] The study reports a depth-only mobile-manipulation policy whose risk sensitivity can be adjusted at runtime while retaining task performance comparable to risk-neutral methods in simulation. ([2603.04579](https://arxiv.org/abs/2603.04579) / [EA-LOCOMANIP-2026-0010](evidence-appendix.md#ea-locomanip-2026-0010))
- [`conditional`] In zero-shot transfer, pick-and-place scored 9/10 in simulation and 8/10 on hardware; handover scored 10/10 in simulation and 8/10 on hardware. ([2606.08278](https://arxiv.org/abs/2606.08278) / [EA-LOCOMANIP-2026-0015](evidence-appendix.md#ea-locomanip-2026-0015))
- [`conditional`] Across three simulated BEHAVIOR-1K tasks, SERF achieved mean task progress of 63.5, 60.1 and 52.5, versus 40.7, 43.0 and 48.4 for the fine-tuned image-only PI0.5 baseline. ([2606.12956](https://arxiv.org/abs/2606.12956) / [EA-LOCOMANIP-2026-0016](evidence-appendix.md#ea-locomanip-2026-0016))
- [`conditional`] Under an unseen locked-joint fault at the most demanding placement height, FT-WBC retained 70% survival but only 45% task success, reflecting an explicit survival-first posture policy. ([2606.24466](https://arxiv.org/abs/2606.24466) / [EA-LOCOMANIP-2026-0017](evidence-appendix.md#ea-locomanip-2026-0017))
- [`limit`] On the real curtain task, neither image policy completed any of 10 trials; retrieval reached the curtain in 2/10, while behavior cloning did not reach it. ([2507.21796](https://arxiv.org/abs/2507.21796) / [EA-LOCOMANIP-2026-0001](evidence-appendix.md#ea-locomanip-2026-0001))
- [`limit`] Kitchen-R's reported execution evaluation always uses the ground-truth plan to isolate execution from planning error, so its module results are not direct evidence of end-to-end autonomy. ([2508.15663](https://arxiv.org/abs/2508.15663) / [EA-LOCOMANIP-2026-0004](evidence-appendix.md#ea-locomanip-2026-0004))
- [`limit`] Cross-simulator smoothness was not a reliable robustness signal: MuJoCo drifted under default friction, while near-zero stop error under tuned friction came from unrealistically high tangential imped... ([2512.18938](https://arxiv.org/abs/2512.18938) / [EA-LOCOMANIP-2026-0007](evidence-appendix.md#ea-locomanip-2026-0007))

## 必须保留的 caveat(任何风格都不得丢失或升级)

- `conditional` On two real-world tasks, the same controller achieved 98% and 100% success under teleoperation, versus 80% and 85% when driven by a diffusion policy. ([2508.10538](https://arxiv.org/abs/2508.10538) / [EA-LOCOMANIP-2026-0002](evidence-appendix.md#ea-locomanip-2026-0002))
- `conditional` For two-box pick-and-place, the solver found the first goal-satisfying feasible plan after 30 of 200 tree expansions, with an average solve time of 52.3 seconds. ([2508.14099](https://arxiv.org/abs/2508.14099) / [EA-LOCOMANIP-2026-0003](evidence-appendix.md#ea-locomanip-2026-0003))
- `conditional` On real G1 sparse-goal following, MoCap object state achieved 80% vertical and 90% lateral success, while egocentric depth achieved 50% and 60%, respectively. ([2603.03279](https://arxiv.org/abs/2603.03279) / [EA-LOCOMANIP-2026-0018](evidence-appendix.md#ea-locomanip-2026-0018))
- `conditional` The study reports a depth-only mobile-manipulation policy whose risk sensitivity can be adjusted at runtime while retaining task performance comparable to risk-neutral methods in simulation. ([2603.04579](https://arxiv.org/abs/2603.04579) / [EA-LOCOMANIP-2026-0010](evidence-appendix.md#ea-locomanip-2026-0010))
- `conditional` In zero-shot transfer, pick-and-place scored 9/10 in simulation and 8/10 on hardware; handover scored 10/10 in simulation and 8/10 on hardware. ([2606.08278](https://arxiv.org/abs/2606.08278) / [EA-LOCOMANIP-2026-0015](evidence-appendix.md#ea-locomanip-2026-0015))
- `conditional` Across three simulated BEHAVIOR-1K tasks, SERF achieved mean task progress of 63.5, 60.1 and 52.5, versus 40.7, 43.0 and 48.4 for the fine-tuned image-only PI0.5 baseline. ([2606.12956](https://arxiv.org/abs/2606.12956) / [EA-LOCOMANIP-2026-0016](evidence-appendix.md#ea-locomanip-2026-0016))
- `conditional` Under an unseen locked-joint fault at the most demanding placement height, FT-WBC retained 70% survival but only 45% task success, reflecting an explicit survival-first posture policy. ([2606.24466](https://arxiv.org/abs/2606.24466) / [EA-LOCOMANIP-2026-0017](evidence-appendix.md#ea-locomanip-2026-0017))
- `limit` On the real curtain task, neither image policy completed any of 10 trials; retrieval reached the curtain in 2/10, while behavior cloning did not reach it. ([2507.21796](https://arxiv.org/abs/2507.21796) / [EA-LOCOMANIP-2026-0001](evidence-appendix.md#ea-locomanip-2026-0001))
- `limit` Kitchen-R's reported execution evaluation always uses the ground-truth plan to isolate execution from planning error, so its module results are not direct evidence of end-to-end autonomy. ([2508.15663](https://arxiv.org/abs/2508.15663) / [EA-LOCOMANIP-2026-0004](evidence-appendix.md#ea-locomanip-2026-0004))
- `limit` Cross-simulator smoothness was not a reliable robustness signal: MuJoCo drifted under default friction, while near-zero stop error under tuned friction came from unrealistically high tangential imped... ([2512.18938](https://arxiv.org/abs/2512.18938) / [EA-LOCOMANIP-2026-0007](evidence-appendix.md#ea-locomanip-2026-0007))

## Writer handoff

- Use `$embodied-ai-review-writer` with this brief, the accepted evidence JSONL, and `evidence-appendix.md`.
- The writer loads only the requested style reference and drafts each style independently from this evidence model.
- Generate `trace-map.json`, then pass the writer's editorial quality audit before settlement.

## 引用速查

- **正文引用 = arXiv 论文链接**:`[2606.13877](https://arxiv.org/abs/2606.13877)` 或 `[SIEVE](https://arxiv.org/abs/2607.06442)`。读者点开即达论文。
- 事件级溯源留给 appendix:成稿正文不放 `evidence-appendix.md#...` 事件锚点;需要精确定位(章节/立场/置信)时,读者从 References 或 appendix 查。
- 本简报中每条证据给出 `论文链接 / 事件链接` 对:写作时**取前者入正文**,后者供你核对 locator 与 stance。
- Citation density and visible source format are style-specific; do not force a full bibliography into Xiaohongshu prose.
- 完整证据条目在 [evidence-appendix.md](evidence-appendix.md);事件映射由 `trace-map.json` 保存。
- Registered sources: `S-EMBODIED-DATA-FRAMEWORK`, `S-LOGISTICS-HUB-SURVEY`, `S-EA-QUESTIONS`, `S-ERR-COMPARE`, `S-PROJECT-CONTEXT`
