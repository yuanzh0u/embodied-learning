#!/usr/bin/env python3
"""Emit deterministic arXiv query plans for common embodied-AI literature topics."""

from __future__ import annotations

import argparse
import json
import sys


QUERY_PLANS = {
    "umi-data-usability": {
        "topic": "UMI data usability",
        "minimum_candidate_count": 12,
        "notes": [
            "Use this for topics such as 'fast umi数据可用性'.",
            "If exact arXiv API queries are rate-limited, use the labels for web/arXiv-page fallback discovery.",
            "Candidate count is not accepted-evidence count; promote only papers with topic-relevant claims.",
        ],
        "queries": [
            {"label": "umi-exact", "tier": "exact-lineage", "query": 'all:"Universal Manipulation Interface"', "why": "Find the original UMI paper and papers that spell out the full method name."},
            {"label": "umi-abbrev", "tier": "exact-lineage", "query": "all:UMI AND all:robot", "why": "Catch UMI abbreviation in robot papers."},
            {"label": "umi-3d", "tier": "named-variant", "query": 'all:"UMI-3D" OR all:"UMI 3D"', "why": "Find 3D sensing extensions that discuss original UMI limitations."},
            {"label": "umi-ft", "tier": "named-variant", "query": 'all:"UMI-FT" OR (all:UMI AND all:"force/torque")', "why": "Find force/torque UMI variants for contact-rich data usability."},
            {"label": "dexumi", "tier": "named-variant", "query": 'all:DexUMI OR all:"Dex UMI"', "why": "Find dexterous UMI variants and embodiment-gap discussion."},
            {"label": "realdexumi", "tier": "named-variant", "query": 'all:RealDexUMI OR all:"RealDex UMI"', "why": "Find wearable dexterous UMI systems and retargeting-free data arguments."},
            {"label": "umi-on-legs", "tier": "named-variant", "query": 'all:"UMI-on-Legs" OR all:"UMI on Legs"', "why": "Find mobile/quadruped transfer papers using UMI demonstrations."},
            {"label": "handheld-gripper", "tier": "hardware-language", "query": 'all:"hand-held gripper" AND all:robot AND all:demonstration', "why": "Find papers that describe UMI-style hardware without naming UMI in the title."},
            {"label": "wrist-mounted-interface", "tier": "hardware-language", "query": 'all:"wrist-mounted" AND all:interface AND all:manipulation', "why": "Catch wrist-mounted data acquisition and sensing discussions."},
            {"label": "portable-data", "tier": "data-language", "query": 'all:portable AND all:"data collection" AND all:"robot manipulation"', "why": "Find portable data collection papers that may compare against UMI."},
            {"label": "in-the-wild-demo", "tier": "data-language", "query": 'all:"in-the-wild" AND all:"human demonstrations" AND all:robot', "why": "Find in-the-wild demonstration papers likely to discuss data usability."},
            {"label": "demo-quality", "tier": "limitations", "query": 'all:"demonstration quality" AND all:"robot learning"', "why": "Find explicit user burden and data quality evaluations."},
            {"label": "gripper-usability", "tier": "limitations", "query": 'all:usability AND all:gripper AND all:"robot learning"', "why": "Find negative/usability discussions of handheld gripper interfaces."},
            {"label": "slam-occlusion", "tier": "limitations", "query": 'all:occlusion AND all:SLAM AND all:"data collection" AND all:manipulation', "why": "Find sensing/SLAM limitations affecting data validity."},
            {"label": "latency-action", "tier": "policy-interface", "query": 'all:latency AND all:"action representation" AND all:manipulation', "why": "Find discussions around action interface and deployment mismatch."},
            {"label": "embodiment-gap", "tier": "transfer", "query": 'all:"embodiment gap" AND all:demonstration AND all:robot', "why": "Find data transfer papers that discuss when human/UMI data remains usable."},
            {"label": "teleop-il-data", "tier": "adjacent-data", "query": 'all:teleoperation AND all:"imitation learning" AND all:data', "why": "Find broader teleoperation data papers with UMI-relevant tradeoffs."},
            {"label": "diffusion-policy-demo", "tier": "adjacent-model", "query": 'all:"diffusion policy" AND all:demonstration AND all:robot', "why": "Model papers often discuss demonstration data quality and scale."},
            {"label": "vla-finetune-data", "tier": "adjacent-model", "query": 'all:"vision-language-action" AND all:"fine-tuning" AND all:data', "why": "VLA tuning papers may expose data usability issues."},
            {"label": "cross-embodiment-data", "tier": "transfer", "query": 'all:"cross-embodiment" AND all:manipulation AND all:data', "why": "Find papers about transferring data across robot bodies."},
        ],
    }
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, choices=sorted(QUERY_PLANS))
    parser.add_argument("--output", help="Write JSON to this path instead of stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rendered = json.dumps(QUERY_PLANS[args.topic], ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
