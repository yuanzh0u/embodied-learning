# JEPA Study Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Execute this plan task-by-task in the current session. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an eight-week Chinese JEPA course with traceable readings, runnable CPU-friendly labs, an optional official V-JEPA 2.1 path, and final research-synthesis artifacts.

**Architecture:** Keep all learning artifacts isolated under `work/jepa-study-20260724/`. Put reusable experiment logic in a small `jepa_lab` package, exercise it through tests and one cumulative tutorial notebook, and pair it with eight weekly lesson files plus assessment templates.

**Tech Stack:** Python 3.10+, PyTorch 2.x, NumPy, Matplotlib, pytest, Jupyter/nbformat.

## Global Constraints

- Target learner already works with VLA/world models but needs stronger MAE/DINO/Dreamer foundations.
- Schedule is eight weeks, about six hours per week, using four short lessons, one lab, and one review.
- Core labs must run on CPU; the official V-JEPA 2.1 section must be optional and Colab/Kaggle-oriented.
- Use Chinese explanations while retaining English technical terms, equations, and paper figure references.
- Treat course materials as learning drafts; do not update knowledge cards or accepted evidence.
- Do not modify existing public APIs or unrelated repository files.

---

### Task 1: Course shell and traceable syllabus

**Files:**
- Create: `work/jepa-study-20260724/README.md`
- Create: `work/jepa-study-20260724/learning-log.md`
- Create: `work/jepa-study-20260724/requirements.txt`

**Interfaces:**
- Consumes: the approved eight-week curriculum.
- Produces: navigation, setup commands, weekly rhythm, reading links, and a repeatable learning-log schema.

- [ ] Write the course navigation and explicit completion criteria.
- [ ] Record CPU and free-GPU setup paths with pinned minimum dependencies.
- [ ] Add a weekly log template covering concepts, evidence, experiment results, failures, and next actions.
- [ ] Verify every planned week and deliverable has a navigation entry.

### Task 2: Tiny JEPA data and model package

**Files:**
- Create: `work/jepa-study-20260724/jepa_lab/data.py`
- Create: `work/jepa-study-20260724/jepa_lab/models.py`
- Create: `work/jepa-study-20260724/jepa_lab/diagnostics.py`
- Create: `work/jepa-study-20260724/jepa_lab/__init__.py`
- Test: `work/jepa-study-20260724/tests/test_data_and_models.py`

**Interfaces:**
- Produces: `MovingDotDataset`, `render_point`, `TinyEncoder`, `ImageJEPA`, `VideoJEPA`, `ActionJEPA`, `update_ema`, `embedding_statistics`, and `linear_probe_accuracy`.

- [ ] Write tests for deterministic data generation, tensor shapes, stop-gradient targets, EMA updates, action sensitivity, and non-collapse statistics.
- [ ] Run tests and confirm they fail before implementation.
- [ ] Implement the smallest deterministic controlled-2D dataset and JEPA modules satisfying the tests.
- [ ] Run the focused tests and confirm they pass.

### Task 3: Training, rollout, and planning

**Files:**
- Create: `work/jepa-study-20260724/jepa_lab/training.py`
- Create: `work/jepa-study-20260724/jepa_lab/planning.py`
- Test: `work/jepa-study-20260724/tests/test_training_and_planning.py`

**Interfaces:**
- Consumes: modules from Task 2.
- Produces: `train_image_jepa`, `train_video_jepa`, `train_action_jepa`, `rollout_latents`, `cem_plan`, `random_policy`, and `evaluate_planner`.

- [ ] Write tests for finite losses, decreasing smoke-training loss, rollout shapes, bounded CEM actions, and planner improvement over random in a deterministic model.
- [ ] Run tests and confirm they fail before implementation.
- [ ] Implement seeded, CPU-sized training loops and CEM/MPC planning with separate prediction and control metrics.
- [ ] Run the focused tests and confirm they pass.

### Task 4: Eight weekly lesson packets

**Files:**
- Create: `work/jepa-study-20260724/weeks/week-01.md` through `week-08.md`

**Interfaces:**
- Consumes: primary-source paper links and lab APIs from Tasks 2–3.
- Produces: four short lessons, one lab, exercises, pitfalls, and exit checks for every week.

- [ ] Write Week 1–2 foundations and the unified MAE/DINO/Dreamer/JEPA comparison.
- [ ] Write Week 3–5 I-JEPA, V-JEPA, V-JEPA 2/2.1 lessons tied to runnable labs.
- [ ] Write Week 6–8 action conditioning, JEPA-WM planning, VLA integration, and research critique.
- [ ] Audit every substantive research statement for a primary-source link or mark it as course inference.

### Task 5: Cumulative tutorial notebook

**Files:**
- Create: `work/jepa-study-20260724/notebooks/jepa_progression.ipynb`

**Interfaces:**
- Consumes: the `jepa_lab` package and weekly lesson sequence.
- Produces: one top-to-bottom tutorial covering data, image JEPA, video JEPA, action JEPA, CEM planning, diagnostics, exercises, and an optional official V-JEPA 2.1 section.

- [ ] Scaffold a tutorial notebook with the bundled Jupyter helper.
- [ ] Add small, independently runnable cells with fixed seeds and tidy outputs.
- [ ] Add exercises followed by answer scaffolds, common pitfalls, and optional extensions.
- [ ] Execute the CPU path top-to-bottom and save concise outputs.
- [ ] Validate notebook structure and rerun from a clean kernel.

### Task 6: Final synthesis and complete verification

**Files:**
- Create: `work/jepa-study-20260724/final/research-memo-template.md`
- Create: `work/jepa-study-20260724/final/talk-outline.md`
- Create: `work/jepa-study-20260724/final/assessment-rubric.md`

**Interfaces:**
- Consumes: weekly outputs and experiment metrics.
- Produces: a 15-minute talk structure, a claim/inference-separated memo, and an objective assessment rubric.

- [ ] Add three-strength/three-limit/two-falsifiable-experiment requirements to the memo.
- [ ] Add timed talk sections and whiteboard prompts.
- [ ] Add architecture, comparison, representation, rollout, planning, and research-critique rubric items.
- [ ] Run all tests, execute the notebook, scan for broken internal links and placeholders, and report any environment-limited optional checks.
