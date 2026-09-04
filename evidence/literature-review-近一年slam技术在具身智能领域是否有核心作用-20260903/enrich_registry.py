#!/usr/bin/env python3
"""Backfill titles, in-window flags, and query-plan dimension labels into the
candidate registry built from /tmp/slam-run browser exports (ws-export-1..18).

Run from the run directory:
  python3 enrich_registry.py
"""
import json
import re

TOPIC_LABELS = {
    "gaussian-slam": ["dynamic-gaussian-slam", "dynamic-gaussian-robotic-mapping"],
    "calibration": ["persona-basic-slam-survey", "dynamic-slam-vla-intersection"],
    "slam-vla": ["dynamic-slam-vla-intersection", "ea-model-vla"],
    "mapless": ["dynamic-mapless-navigation", "persona-vla-mapfree"],
    "spatial-memory": ["dynamic-spatial-memory-robot", "persona-counter-implicit-memory"],
    "slam-teleop": ["dynamic-slam-teleoperation", "ea-hardware-teleop-device", "persona-auditor-teleop-pose"],
    "slam-manipulation": ["dynamic-slam-manipulation"],
    "e2e-slam": ["dynamic-endtoend-slam", "persona-slam-engineer-neural-frontend"],
    "slam-dynamic": ["persona-counter-dynamic-failure", "persona-slam-engineer-robustness"],
    "slam-survey": ["persona-basic-slam-survey"],
    "mapfree-nav": ["persona-vla-mapfree", "dynamic-mapless-navigation"],
    "slam-benchmark": ["persona-auditor-ground-truth"],
    "spatial-intelligence": ["dynamic-spatial-intelligence", "ea-model-named-foundation"],
    "implicit-memory": ["persona-counter-implicit-memory"],
    "lifelong-map": ["persona-counter-dynamic-failure", "dynamic-spatial-memory-robot"],
    "nav-foundation": ["ea-model-vla", "dynamic-spatial-intelligence"],
    "semantic-mapping": ["dynamic-language-map-navigation", "persona-slam-engineer-neural-frontend"],
    "reloc-datacollection": ["ea-hardware-arkit-tracking", "persona-auditor-camera-relocalization"],
    "worldmodel-nav": ["dynamic-worldmodel-pathplanning", "persona-vla-worldmodel-replace-map"],
    "humanoid": ["ea-model-named-foundation"],
    "openreloc": ["persona-auditor-camera-relocalization", "ea-hardware-arkit-tracking"],
    "lidar-slam": ["persona-slam-engineer-robustness"],
    "vio": ["persona-slam-engineer-neural-frontend"],
    "uav-slam": ["persona-slam-engineer-robustness"],
    "topo-nav": ["dynamic-language-map-navigation", "dynamic-spatial-memory-robot"],
    "event-slam": ["persona-slam-engineer-robustness"],
    "vlm-spatial-fail": ["persona-counter-implicit-memory", "persona-vla-mapfree"],
    "slam-eval-benchmark": ["persona-auditor-ground-truth"],
    "nav-eval-benchmark": ["persona-auditor-ground-truth"],
    "slam-systems": ["persona-slam-engineer-robustness", "persona-basic-slam-robot"],
    "rgbd-slam": ["persona-slam-engineer-robustness", "persona-basic-slam-robot"],
    "slam-manipulation2": ["dynamic-slam-manipulation"],
    "worldmodel-nav2": ["dynamic-worldmodel-pathplanning", "persona-vla-worldmodel-replace-map"],
    "teleop2": ["ea-hardware-teleop-device", "persona-auditor-teleop-pose"],
    "loop-closure": ["persona-slam-engineer-robustness", "persona-basic-slam-robot"],
    "semantic-nav2": ["dynamic-language-map-navigation"],
    "vla-spatial-fail2": ["persona-vla-mapfree", "persona-counter-implicit-memory"],
    "vla-spatial-prior": ["dynamic-slam-vla-intersection", "ea-model-vla"],
    "3dgs-twin": ["dynamic-gaussian-robotic-mapping", "dynamic-slam-manipulation"],
    "hdmap-driving": ["dynamic-spatial-intelligence", "persona-counter-dynamic-failure"],
    "foundation-slam": ["persona-slam-engineer-neural-frontend", "dynamic-endtoend-slam"],
    "active-exploration": ["persona-basic-slam-robot", "dynamic-slam-manipulation"],
    "ego-video": ["dynamic-slam-teleoperation", "ea-hardware-slam-demonstration"],
    "human-mocap": ["ea-hardware-slam-demonstration", "persona-auditor-teleop-pose"],
    "droid-w": ["persona-slam-engineer-robustness", "persona-basic-slam-robot"],
    "scarf-slam": ["persona-slam-engineer-neural-frontend", "dynamic-endtoend-slam"],
    "visual-slam-repeat": ["persona-slam-engineer-robustness"],
    "mapless-repeat": ["persona-vla-mapfree", "dynamic-mapless-navigation"],
    "slam-role-repeat": ["persona-basic-slam-survey"],
    "semantic-map-repeat": ["dynamic-language-map-navigation"],
    "vpr-repeat": ["persona-auditor-camera-relocalization", "persona-auditor-ground-truth"],
    "tactile-repeat": ["dynamic-slam-manipulation"],
    "gs-slam-repeat": ["dynamic-gaussian-slam"],
    "worldmodel-repeat": ["dynamic-worldmodel-pathplanning", "persona-vla-worldmodel-replace-map"],
    "umi-3d": ["ea-hardware-slam-demonstration", "dynamic-slam-teleoperation"],
    "vla-nav": ["ea-model-vla", "dynamic-spatial-intelligence"],
    "saturation-r1a": ["dynamic-gaussian-slam"],
    "saturation-r1b": ["persona-basic-slam-survey"],
    "saturation-r2a": ["persona-slam-engineer-robustness"],
    "saturation-r2b": ["persona-vla-mapfree", "dynamic-mapless-navigation"],
}

ARXIV_ID = re.compile(r"arxiv\.org/(?:abs|html|pdf)/(\d{4}\.\d{4,5})")


def main():
    topic_ids = {}
    titles = {}
    for n in range(1, 19):
        for line in open(f"/tmp/slam-run/ws-export-{n}.jsonl"):
            d = json.loads(line)
            topic = d["source_url"].split(":")[-1]
            ids = topic_ids.setdefault(topic, set())
            for link in d.get("links", []):
                m = ARXIV_ID.search(link.get("href", ""))
                if m:
                    ids.add(m.group(1))
                    if m.group(1) not in titles and link.get("text"):
                        titles[m.group(1)] = link["text"]

    r = json.load(open("candidate-registry.json"))
    n_title, retagged, out_window = 0, 0, []
    for c in r["candidates"]:
        if not c["title"] and c["arxiv_id"] in titles:
            c["title"] = titles[c["arxiv_id"]]
            n_title += 1
        i = c["arxiv_id"]
        y, m = 2000 + int(i[:2]), int(i[2:4])
        in_window = (y == 2025 and m >= 9) or (y == 2026 and m <= 9)
        c["published"] = f"{y}-{m:02d}"
        c["month_inferred_from_id"] = True
        c["in_window"] = in_window
        if not in_window:
            out_window.append(i)
        labels = set()
        for topic, ids in topic_ids.items():
            if c["arxiv_id"] in ids:
                labels.update(TOPIC_LABELS.get(topic, []))
        if labels:
            for d in c.get("discoveries", []):
                if d.get("channel") == "browser":
                    d["query_labels"] = sorted(labels)
            retagged += 1

    json.dump(r, open("candidate-registry.json", "w"), ensure_ascii=False, indent=2)
    print(
        f"total={len(r['candidates'])} titles_backfilled={n_title} "
        f"retagged={retagged} out_of_window={out_window}"
    )


if __name__ == "__main__":
    main()
