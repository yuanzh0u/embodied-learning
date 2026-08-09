# New Evidence Summary

## Papers Processed: 20
## Events Generated: 25

## Supervision Types Identified

| Supervision Type | Papers | Key Finding |
|----------------|--------|-------------|
| **Tactile/Force** | 2606.09337 (TORL-VLA), 2601.20321 (TaF-VLA), 2607.18231 (FM-VLA), 2607.14609 (Rep-Aligned Tactile), 2607.22530 (ViTacWorld), 2603.19201 (OmniVTA), 2603.12665 (TacVLA), 2603.10871 (FG-CLTP), 2603.13315 (Bi-HIL) | Tactile and force/torque supervision is the most commonly needed non-action signal. Key forms include: wrench (6D force/torque) prediction, tactile-force contrastive alignment, force-based temporal memory (VAE), future tactile prediction as representation grounding, visuo-tactile world models, contact-aware gating, quantitative tactile tokenization, and bilateral control force recording. |
| **Geometric/3D** | 2607.12356 (VistaVLA), 2509.11125 (ManiVID-3D), 2606.08530 (GEAR-VLA), 2607.06564 (Lift3D-VLA), 2602.00937 (CLAMP), 2601.22988 (GEM3D) | 3D geometric supervision through point clouds, Gaussian primitives, multi-view feature rendering, self-supervised disentangled features, and GC-MAE (point cloud reconstruction + future geometry prediction) is needed for spatial reasoning, view generalization, and cross-embodiment transfer. |
| **Physics** | 2606.13886 (PhysVLA), 2603.00110 (PhysGen), 2603.23376 (ABot-PhysWorld) | Physics supervision takes multiple forms: Euler-Lagrange dynamics gates at inference, implicit physics from video pretraining, and physics-aware DPO post-training. All address the gap that VLA models trained on demonstrations do not inherently respect physical laws. |
| **Semantic/Language** | 2607.18709 (RoboInter1.5) | Dense intermediate representation annotations (subtasks, primitive skills, grounding, affordance, contact points, motion traces) serve as structured supervision for both action execution and world state prediction. |
| **Reward/RL** | 2602.12628 (RL-Co) | RL reward signals from simulation, combined with auxiliary supervised loss on real data, are needed to exploit closed-loop interaction beyond static SFT demonstrations and prevent catastrophic forgetting. |
| **Contrastive/Representation** | 2602.00937 (CLAMP), 2603.10871 (FG-CLTP) | Contrastive learning aligning 3D geometry, actions, text, and tactile representations provides pretraining supervision that improves fine-tuning efficiency and cross-sensor generalization. |
| **Safety/Corrective** | 2606.09337 (TORL-VLA) | Intervention-censored critics prevent credit assignment bias when learning from mixed policy-generated and human-intervention data. |

## Key Findings by Supervision Type

### 1. Tactile/Force Supervision (9 papers)

- **Wrench prediction** (TORL-VLA): Future wrench (6D force/torque) sequences serve as contact reference signals for online RL refinement. MoE fusion of wrench tokens is the most critical component.
- **Tactile-force alignment** (TaF-VLA): Contrastive learning aligns tactile sequences with physical force/torque in a VQ-VAE latent space. Temporal history and decoupled force modalities (pressure + wrench) are both necessary.
- **Force-based memory** (FM-VLA): VAE pretrained on force time series reconstruction compresses long-horizon force history into compact memory tokens. Force and state memory are complementary (25.9% and 40.7% alone vs 83.3% combined).
- **Future tactile prediction** (Rep-Aligned Tactile): Tactile prediction effectiveness depends on which representation it supervises. Intermediate action-expert features are optimal (74% vs 58% for VLM-side). Latent targets outperform raw tactile prediction.
- **Visuo-tactile world models** (ViTacWorld, OmniVTA): Predicting tactile outcomes conditioned on actions provides contact dynamics supervision. Tactile signals have smaller sim-to-real gap than visual signals. 60Hz reflexive correction closes the loop.
- **Contact-aware gating** (TacVLA): Tactile tokens should be selectively activated only during contact, avoiding noise during free-space motion.
- **Quantitative tactile tokenization** (FG-CLTP): Discrete numerical tokens (force magnitude, contact depth, area, principal axis) bridge qualitative semantics and quantitative physics, reducing regression MAE by 52.6%.
- **Bilateral control** (Bi-HIL): Force/torque recording from leader-follower teleoperation is essential for contact-rich tasks (0% success without force on peg-in-hole vs 80% with force).

### 2. Geometric/3D Supervision (6 papers)

- **3D Gaussian primitives** (VistaVLA): Semantic features distilled into Gaussian primitives via multi-view rendering provide scene-level spatial context. Raw depth input provides only limited improvement.
- **Self-supervised disentangled features** (ManiVID-3D): View-invariant 3D point cloud features learned through self-supervised alignment achieve 40.6% higher success under viewpoint variations.
- **Geometry-aware action representations** (GEAR-VLA): Semantic-aligned 3D backbone + embodiment canonicalization enables cross-embodiment generalization (85.9% on AgileX, 81.0% on unseen LDT-01).
- **GC-MAE** (Lift3D-VLA): Dual-objective self-supervised framework reconstructing current point cloud + predicting future geometric evolution enables VLA to internalize 3D structure and physical dynamics.
- **3D contrastive pretraining** (CLAMP): Contrastive learning aligning multi-view 3D renderings, actions, and text. Dynamic wrist views and pre-training both encoders and policy are critical.
- **Multi-view geometric supervision** (GEM3D): Point cloud reconstruction + Gaussian splatting under multi-view supervision, with distillation-based policy learning that preserves geometric knowledge better than direct fine-tuning.

### 3. Physics Supervision (3 papers)

- **Euler-Lagrange dynamics gate** (PhysVLA): Selective inference-time physics correction (fires only when dynamics residual exceeds threshold) improves success by up to 17% without retraining. Phase-aware FSM provides phase-specific corrections.
- **Implicit physics from video** (PhysGen): Pretrained video models serve as physics proxies, transferring implicit physical knowledge (object permanence, dynamics) without explicit physics engine supervision.
- **Physics-aware DPO** (ABot-PhysWorld): DPO post-training with decoupled physics discriminators suppresses physically implausible behaviors (object penetration, anti-gravity motion) in video world models.

### 4. Semantic/Language Supervision (1 paper)

- **Dense intermediate representations** (RoboInter1.5): 10+ types of per-frame annotations (subtasks, skills, grounding, affordance, contact points, motion traces) across 230k episodes serve as bidirectional supervision for action execution and world state prediction.

### 5. Reward/RL Supervision (1 paper)

- **Sim-real RL co-training** (RL-Co): RL reward from simulation exploits closed-loop interaction beyond static SFT. Auxiliary supervised loss on real data prevents catastrophic forgetting. +24% real-world success improvement.

### 6. Contrastive/Representation Supervision (2 papers)

- Contrastive learning aligning 3D geometry, actions, and text (CLAMP) or tactile and language (FG-CLTP) provides pretraining supervision that improves fine-tuning efficiency and cross-modal/cross-sensor generalization.

### 7. Safety/Corrective Supervision (1 paper)

- **Intervention-censored critic** (TORL-VLA): Prevents credit assignment bias in online RL with human interventions, blocking post-intervention success from propagating to preceding policy actions (AUC 0.999 for boundary risk separation).

## Cross-Cutting Insights

1. **Tactile/force supervision is the most frequently needed non-action signal** (9 of 20 papers), reflecting the field's recognition that vision-only policies are 'force-blind' for contact-rich tasks.
2. **3D geometric supervision is critical for spatial reasoning** (6 papers), with multiple approaches (Gaussian primitives, point cloud MAE, contrastive learning) all showing improvements over 2D-only baselines.
3. **Physics supervision can be injected at different stages**: training (DPO, video pretraining), inference (Euler-Lagrange gate, FSM), or both.
4. **The placement of supervision matters as much as the signal**: representation-aligned tactile grounding shows that where supervision is applied within the architecture determines its effectiveness.
5. **Supervision signals are complementary**: force + state memory, pixel-level + semantic-level physics, and multi-view + contrastive learning all show complementary benefits.
6. **Training-only supervision is viable**: Several approaches use supervision only during training (semantic masks, depth priors, force alignment) and discard it at inference, reducing deployment overhead.
