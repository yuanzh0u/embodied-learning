# 精读选篇计划 — Diffusion Transformer 视频/世界模型

> 定位：scoping 综述，精读下限 15 篇。以下为预选精读集（约 19 篇），覆盖 6 维。
> 最终以全文恢复的 `evidence_eligible=True` 为准；若某篇不可读则替换为同维度替补。

## 目标精读集（arXiv ID → 维度）

### 机制 / 架构（microplan）
| ID | 论文 | 维度 |
|---|---|---|
| 2411.17470 | Towards Precise Scaling Laws for Video Diffusion Transformers | mechanisms/direct |
| 2411.06449 | Improved Video VAE for Latent Video Diffusion Model | mechanisms |
| 2502.01776 | Sparse VideoGen: Accelerating Video Diffusion Transformers with Spatial-Temporal Sparsity | mechanisms/deployment |

### 视频扩散 → 世界模型转型（核心命题）
| ID | 论文 | 维度 |
|---|---|---|
| 2410.12822 | AVID: Adapting Video Diffusion Models to World Models | direct/eval |
| 2505.14357 | Vid2World: Crafting Video Diffusion Models to Interactive World Models | direct/eval |
| 2505.21996 | VRAG: Learning World Models for Interactive Video Generation | direct |

### 物理一致性 / 评测（限制+评测）
| ID | 论文 | 维度 |
|---|---|---|
| 2411.02385 | How Far is Video Generation from World Model: A Physical Law Perspective | limits |
| 2608.05948 | GAUGE: Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models | evaluation |
| 2605.19242 | PhyWorld: Physics-Faithful World Model for Video Generation | limits |

### action-conditioned 世界模型（adjacent/具身）
| ID | 论文 | 维度 |
|---|---|---|
| 2605.08567 | ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models | eval/adjacent |
| 2603.05449 | RealWonder: Real-Time Physical Action-Conditioned Video Generation | adjacent |
| 2607.06558 | RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation | adjacent/embodied |

### 长视频 / 一致性
| ID | 论文 | 维度 |
|---|---|---|
| 2410.20502 | ARLON: Boosting Diffusion Transformers with Autoregressive Models for Long Video Generation | direct/limits |
| 2501.09019 | Ouroboros-Diffusion: Consistent Content in Tuning-free Long Video Diffusion | limits |
| 2605.15178 | SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer | deployment/direct |

### 自回归竞争路线（机制/直接）
| ID | 论文 | 维度 |
|---|---|---|
| 2507.08801 | Lumos-1: Autoregressive Video Generation with Discrete Diffusion | mechanisms |
| 2602.01801 | Fast Autoregressive Video Diffusion and World Models with Temporal Cache Compression | mechanisms/deployment |

### 部署 / 加速
| ID | 论文 | 维度 |
|---|---|---|
| 2411.02397 | Adaptive Caching for Faster Video Generation with Diffusion Transformers | deployment |

### 综述锚定
| ID | 论文 | 维度 |
|---|---|---|
| 2502.17863 | A Survey: Spatiotemporal Consistency in Video Generation | adjacent/synthesis |

## 替补（如不可读）
- 2412.04446 DiCoDe（AR+diffusion token）、2511.17470/2411.17470 scaling、2507.08801 Lumos
- 2505.14167 LMP、2412.13604 LongVie 2、2605.19242 PhyWorld 已在列