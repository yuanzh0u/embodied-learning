# Editorial plan and reader contract

- Reader: autonomous-driving researcher / technical lead mapping papers, implementation interfaces and public teams.
- Decision: choose which paper family to read or reproduce, and which organization to investigate, without conflating deployment architecture with language used during training.
- Thesis: action-relevant supervision and the language-to-action interface explain the evidence better than mutually exclusive VLA/foundation/world-model labels.
- Falsifier: matched-data, matched-compute closed-loop experiments show generic scene narration performs as well as action-aligned language supervision, or visual-only controls retain all measured long-tail benefits without the language teacher.
- Argument: language location → action interface and causal relevance → non-language controls and deployment → industrial disclosure → evaluation and people.
- Central examples: EMMA scene-description versus meta-decision ablation; SimLingo counterfactual instruction/action pairs; Alpamayo reasoning-only reward failure; Orion-Lite teacher/student.
- Counterclaims: online language can help some tasks; distillation does not prove language unnecessary during training; closed-source industrial achievements do not identify an architecture.
- Scope: one scientific memo explicitly requested by user; three comparison tables and relation diagram are supplements. No other writing styles.
- Editorial review: mechanism-based prose, explicit inference and falsifier, 8 core papers, 30 accepted references, separate Tesla/Waymo/Li Auto disclosure section, limitations and next experiment. Numeric leaderboard claims intentionally avoided.

## Li Auto focused supplement

- Reader question: infer the connected research program from mechanism-oriented papers, without inventing a unified production stack.
- Thesis: controllable action interfaces, structured candidates and feedback form the strongest connection; world/data tools and transferable foundations address adjacent bottlenecks.
- Running example: one road scene with multiple intents → continuous candidate modes → group preference updates; compare trajectory-cluster intents and external safety repair.
- Falsifier: matched driving data/compute controls erase the gain from semantic conditioning or auxiliary representations.
- Core reading cluster: U1 / Streaming Intent / DIAL; alternatives LinkVLA / ReflectDrive; world/data and cross-embodiment papers are bounded extensions.
- Boundary: VLAFlow has no driving experiment; ME-VLM driving is understanding; U1 family logged open-loop; industrial architecture mapping remains undisclosed.
- Sources: 10 newly accepted papers plus reused DriveVLM/NAVSIM anchors and separately audited project/person/company disclosures.
- Ending: specify missing controlled comparisons and production mapping, not a company ranking.
