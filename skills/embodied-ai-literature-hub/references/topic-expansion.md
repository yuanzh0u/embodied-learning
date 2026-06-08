# Topic Expansion

Use this file to turn a user topic into a transparent arXiv search plan. Always record why each query exists.

## Default strategy

- Start with direct topic terms.
- Add adjacent embodied-AI surfaces that are likely to contain discussion of the topic.
- Prefer 4-8 focused queries over one giant query.
- Keep candidate search broad, but promote papers only when arXiv HTML正文 evidence contains a topic-relevant discussion.
- For named method families, run enough tiers to produce a real candidate pool. Fewer than 12 candidates means "expand or report blocker", not "topic is sparse".

## Static adjacency

| Knowledge ID | Direct terms | Adjacent searches likely to expose hidden discussion |
|---|---|---|
| `EA-DATA` | robot data, demonstration data, trajectory data, UMI, DROID, Ego4D, teleoperation | VLA fine-tuning, imitation learning, diffusion policy, robot foundation models, sim-to-real, synthetic data, dataset curation, data quality |
| `EA-SENSOR` | RGB, depth, point cloud, tactile, force, proprioception | occlusion, contact-rich manipulation, failure recovery, last centimeter, sensor fusion, real-world robustness |
| `EA-HARDWARE` | UMI, ARKit, SLAM, VR tracking, handheld gripper, teleoperation device | calibration, synchronization, embodiment mismatch, data collection cost, deployment constraints |
| `EA-XEMBODIMENT` | retargeting, cross-embodiment, embodiment adapter, dexterous hand, gripper | action representation, human-to-robot data transfer, morphology gap, dataset reuse |
| `EA-MODEL` | VLA, vision-language-action, RT-X, Octo, OpenVLA, robot foundation model | fine-tuning data, demonstration scale, data mixture, embodiment-specific adapter, negative transfer |
| `EA-EVAL` | benchmark, open-loop, closed-loop, world model, sim-real correlation | data validity, offline metric failure, real-robot validation, failure taxonomy |
| `EA-BIZ` | industrial deployment, ROI, cycle time, yield, reliability | data collection cost, acceptance testing, safety, operator takeover, edge cases |

## UMI/data query tiers

For topics like "UMI 数据可用性" or "fast umi 数据可用性", include:

Tier 1: exact UMI lineage and named variants.

- `all:"Universal Manipulation Interface"`
- `all:"UMI-3D" OR all:"UMI 3D"`
- `all:"UMI-FT" OR all:"force/torque" AND all:UMI`
- `all:"DexUMI" OR all:"Dex UMI"`
- `all:"RealDexUMI" OR all:"RealDex UMI"`
- `all:"UMI-on-Legs" OR all:"UMI on Legs"`

Tier 2: UMI hardware/data language.

- `all:UMI AND all:robot AND all:data`
- `all:UMI AND all:demonstration`
- `all:"hand-held gripper" AND all:robot AND all:demonstration`
- `all:"wrist-mounted" AND all:interface AND all:manipulation`
- `all:"portable" AND all:"data collection" AND all:"robot manipulation"`
- `all:"in-the-wild" AND all:"human demonstrations" AND all:robot`

Tier 3: data usability and limitations.

- `all:"demonstration quality" AND all:"robot learning"`
- `all:usability AND all:gripper AND all:"robot learning"`
- `all:occlusion AND all:SLAM AND all:"data collection" AND all:manipulation`
- `all:latency AND all:"action representation" AND all:manipulation`
- `all:"embodiment gap" AND all:demonstration AND all:robot`

Tier 4: method-adjacent papers likely to discuss UMI-style data usefulness.

- `all:teleoperation AND all:"imitation learning" AND all:data`
- `all:"diffusion policy" AND all:demonstration AND all:robot`
- `all:"vision-language-action" AND all:"fine-tuning" AND all:data`
- `all:"robot foundation model" AND all:data`
- `all:"synthetic data" AND all:"robot manipulation"`
- `all:"cross-embodiment" AND all:manipulation AND all:data`
- `all:"real-world demonstrations" AND all:"robot policy"`

Tier 5: author and citation expansion.

- Search follow-up papers by core UMI authors such as Shuran Song, Cheng Chi, Huy Ha, Zhenjia Xu, Chuer Pan, and direct UMI variant authors.
- Search papers that mention original UMI in abstract/full-text via Browser/web search when arXiv API metadata search misses them.
- Add cited papers only when they carry a core claim about data usability, embodiment transfer, sensing, latency, or demonstration quality.

Known UMI-family candidates to expect, subject to time range:

- `2402.10329` Universal Manipulation Interface.
- `2407.10353` UMI on Legs.
- `2505.21864` DexUMI.
- `2601.09988` UMI-FT.
- `2603.17189` Influence of Gripper Design on Human Demonstration Quality for Robot Learning.
- `2604.14089` UMI-3D.
- `2606.06033` RealDexUMI.

## Search notes

- arXiv full-text search is not available through the API; search metadata first, use Browser/web search as candidate fallback, then inspect arXiv HTML正文.
- Terms like `FAST-UMI` may not appear in arXiv metadata even if related UMI/data discussions appear in HTML正文.
- For Chinese user topics, translate the operative research terms into English query variants before searching.
