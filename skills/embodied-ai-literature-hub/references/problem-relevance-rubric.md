# Problem-Relevance Rubric (stage 3)

The script's BM25 score is a **gate and a weak prior, never the verdict**. Stage 3 is
reading each of the ~50 retrieved papers' *judgment surface* (abstract + introduction +
related-work) and assigning a relevance tier per question. Use the tiers below, then
re-rank to a top **20**, then pick **10** for full-text reading.

## The four tiers

| Tier | Meaning | When to assign |
|---|---|---|
| **directly-addresses** | The paper *poses or solves* the specific question. | Its introduction frames the question as its problem, or its related-work/method (as visible in the surface) describes *how* the thing is done. |
| **contextualizes** | The paper discusses the question as prior work or motivation, but does not solve it. | Its related-work surveys the approaches to the question, or it treats the question as one of several baselines it compares against. |
| **adjacent** | Same general area (ego/exo, cross-view, multiview video), but the question itself is absent. | The keywords overlap, but the paper's actual problem is a different one. |
| **not-relevant** | No meaningful connection to the question. | Keyword collision only (e.g. "camera" in an unrelated setting). |

A `directly-addresses` paper is a stage-4 candidate. A `contextualizes` paper is often a
good *breadcrumb*: its related-work will point at the `directly-addresses` papers you
actually want (feed those back as new seeds).

## How to read the judgment surface

- **Abstract** — the claim. Tells you what the paper *claims* to do.
- **Introduction** — the motivation. Tells you whether the question is the paper's own
  problem or just context. "We address the problem of aligning first- and third-person
  views …" → `directly-addresses`; "Prior work aligned ego and exo views [refs]" →
  `contextualizes`.
- **Related-work** — the positioning. Tells you which prior approaches to the question the
  paper builds on; the references it cites for the question are your best next seeds.

## Worked cues for the ego-exo questions

For the example review, the three open questions are:

1. **How is the third-person (exocentric) camera configuration initialized?**
   `directly-addresses` = describes placing/calibrating the third-person (exo) camera(s)
   relative to the scene or the ego wearer — e.g. static rig placement, multi-view capture
   setup, exo-camera calibration/registration. A paper whose method says "we place K exo
   cameras around the scene and calibrate them via …" is tier 1. One that only says "we use
   synchronized exo-ego video" is `contextualizes` at best.
2. **How are first-person and third-person views aligned?**
   `directly-addresses` = proposes or evaluates an ego↔exo correspondence / cross-view
   alignment / view translation method (e.g. AE2's DTW temporal alignment, ObjectRelator's
   cross-view object alignment, Ego-Exo4D's ego-exo correspondence task). "We align
   first- and third-person views by …" → tier 1; merely benchmarking on cross-view
   retrieval → `contextualizes`.
3. **How are multiple third-person (multiview) cameras aligned?**
   `directly-addresses` = handles the alignment/registration *across multiple* third-person
   cameras (multi-camera extrinsic calibration, 3D reconstruction from multi-view, motion
   capture rig calibration). A single ego↔exo pair alignment does **not** answer this —
   that is `adjacent` for Q3 even if `directly-addresses` for Q2.

Assign a tier **per question**, not one per paper: a paper can be `directly-addresses` on
Q2 and `adjacent` on Q3.

## Stage 4 gate

Rank the ~50 to a top **20** by the tiers (prefer `directly-addresses`, then
`contextualizes`, then `adjacent`; drop `not-relevant`), then hand the **10** most
promising to `$embodied-ai-paper-reader` for full-text recovery, deep reading, and a
claim-support audit. Nothing here becomes evidence until that gate passes — the surface
read is a *screen*, not a verification.
