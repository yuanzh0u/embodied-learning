# Topic-card update suggestions (not applied)

These are proposed deltas only. They should be reviewed before any topic card is edited.

## EA-MODEL

- Add a conditional judgment that foundation-agent scaling increasingly depends on explicit scaffolds and interfaces—morphology conditioning, object tokens, code primitives, diffusion action experts—not only a shared backbone.
- Add CaP-X as limit evidence: higher-level primitives can raise benchmark success while masking low-level perception, geometry, and control failures (`EA-JIMFAN-READ-0016`).
- Suggested anchors: `EA-JIMFAN-READ-0006`, `0007`, `0009`, `0014`, `0016`.

## EA-EVAL

- Add an explicit evaluation ladder separating game/API success, simulator-state success, matched sim-to-real transfer, bounded real-robot trials, and long-running real deployment.
- Add the plain-Eureka real-world failure as direct evidence that simulated reward quality is insufficient for sim-to-real (`EA-JIMFAN-READ-0012`).
- Add DreamDojo's 20-scene fruit-packing result as a bounded correlation study, not general world-model admissibility (`EA-JIMFAN-READ-0015`).

## EA-DATA

- Add human-video pretraining with latent proxy actions as a promising but field-limited supervision route: target-robot post-training remains necessary, and uncommon fast actions/multiview/retention remain gaps.
- Suggested anchors: `EA-JIMFAN-READ-0014`, `0015`.

## EA-ALIGN

- Add “primitive/API abstraction” as a fourth interface audit beside language→stage, vision→action, and action→controller: benchmark scores must disclose what reasoning and control are hidden inside primitives.
- Add GR00T N1's VLM System 2 + diffusion System 1 as a concrete dual-interface example, bounded to the paper's evaluated tasks.
- Suggested anchors: `EA-JIMFAN-READ-0014`, `0016`.

## EA-4D

- Add a warning that high sim-real policy-ranking correlation in one task family is insufficient for admissibility without contact/force fidelity, failure optimism, counterfactual validity, and cross-task replication.
- Suggested anchor: `EA-JIMFAN-READ-0015`; treat `EA-JIMFAN-READ-0017` as a position-paper gap, not empirical proof.
