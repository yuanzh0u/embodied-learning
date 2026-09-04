#!/bin/bash
# Build reading packets + note templates for the selected deep-reading set.
set -e
RUN="/Users/eason/Documents/具身学习/work/literature-review-近一年slam技术在具身智能领域是否有核心作用-20260903"
SKILL="/Users/eason/Documents/具身学习/skills/embodied-ai-paper-reader/scripts"
Q="近一年SLAM技术在具身智能领域是否发挥核心作用？在具身数据采集、操作、导航、空间推理各环节，SLAM是不可或缺的基础设施，还是正被端到端基础模型、世界模型或隐式空间记忆替代？"

mkdir -p "$RUN/reading-packets" "$RUN/paper-notes"

build() {
  local id="$1"; local topic="$2"
  python3 "$SKILL/build_reading_packet.py" \
    --extraction "$RUN/extractions/$id.json" \
    --metadata "$RUN/paper-metadata/$id.json" \
    --review-question "$Q" \
    --topic-id "$topic" \
    --review-mode scoping \
    --output "$RUN/reading-packets/$id.md" \
    --note-template "$RUN/paper-notes/$id.json" >/dev/null && echo "packet: $id ($topic)"
}

# anchors (read by orchestrator)
build 2604.14089 EA-HARDWARE   # UMI-3D
build 2608.22896 EA-VLOC       # SuperMap
build 2511.17792 EA-MODEL      # Target-Bench
# SLAM frontier
build 2604.06830 EA-VLOC       # VGGT-SLAM++
build 2603.19076 EA-VLOC       # DROID-SLAM in the Wild
build 2512.25008 EA-VLOC       # FoundationSLAM
build 2604.12837 EA-VLOC       # GGD-SLAM
build 2602.05508 EA-VLOC       # VGGT-Motion
build 2606.00307 EA-VLOC       # ScaRF-SLAM
# semantic/language SLAM
build 2602.11862 EA-VLOC       # LAMP
build 2511.16144 EA-VLOC       # LEGO-SLAM
build 2603.16301 EA-4D         # OGScene3D
build 2606.30809 EA-VLOC       # GaussLite
# embodied data infra
build 2510.01607 EA-HARDWARE   # ActiveUMI
build 2509.02437 EA-HARDWARE   # U-ARM
build 2604.07331 EA-HARDWARE   # RoSHI
build 2605.05945 EA-HARDWARE   # MobileEgo Anywhere
# substitution: memory/world models/mapless
build 2604.16482 EA-MODEL      # Survey spatial memory
build 2511.06840 EA-MODEL      # PanoNav
build 2606.14879 EA-MODEL      # VANDERER
build 2604.07957 EA-MODEL      # WorldMAP
build 2602.01644 EA-MODEL      # Spatial AI Agents & World Models
# capability boundaries
build 2601.05529 EA-MODEL      # Before We Trust Them
build 2603.21577 EA-MODEL      # Mind over Space
build 2602.19710 EA-MODEL      # PoseVLA
build 2602.17659 EA-MODEL      # When Vision Overrides Language
# SLAM limits/benchmarks
build 2602.18174 EA-VLOC       # ScaleMaster
build 2604.24033 EA-VLOC       # Event-based SLAM benchmark
build 2607.03283 EA-MODEL      # Embodied Operators
echo "done: $(ls "$RUN/reading-packets" | wc -l) packets"
