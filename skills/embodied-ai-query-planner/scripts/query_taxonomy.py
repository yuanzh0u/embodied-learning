#!/usr/bin/env python3
"""Deterministic embodied-AI query taxonomy for arXiv query planning.

This module is intentionally data-only. Build scripts can import the constants
and helpers without triggering network access, filesystem reads, or live
calibration.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

QueryEntry = dict[str, object]
Plan = dict[str, object]

TOPIC_ORDER = (
    "EA-DATA",
    "EA-SENSOR",
    "EA-HARDWARE",
    "EA-XEMBODIMENT",
    "EA-MODEL",
    "EA-EVAL",
    "EA-BIZ",
)

FAMILY_ORDER = (
    "umi",
    "droid-ego4d",
    "teleoperation-demo-quality",
    "vla",
    "sim2real",
    "world-model",
    "retargeting",
    "tactile-force",
    "last-centimeter",
    "industrial-deployment",
)

COMMON_CATEGORIES = ("cs.RO", "cs.AI", "cs.LG")
VISION_CATEGORIES = ("cs.RO", "cs.CV", "cs.LG")
SYSTEM_CATEGORIES = ("cs.RO", "eess.SY", "cs.AI")


def _entry(
    label: str,
    tier: str,
    query: str,
    why: str,
    suggested_categories: Iterable[str] | None = None,
) -> QueryEntry:
    entry: QueryEntry = {
        "label": label,
        "tier": tier,
        "query": query,
        "why": why,
    }
    if suggested_categories:
        entry["suggested_categories"] = list(suggested_categories)
    return entry


def _browser_entry(label: str, query: str, why: str) -> QueryEntry:
    return {
        "label": label,
        "query": query,
        "why": why,
    }


def _plan(
    key: str,
    title: str,
    kind: str,
    topic_ids: Iterable[str],
    queries: Iterable[QueryEntry],
    summary: str,
    browser_fallback_queries: Iterable[QueryEntry] | None = None,
    web_calibration_queries: Iterable[QueryEntry] | None = None,
) -> Plan:
    plan: Plan = {
        "key": key,
        "title": title,
        "kind": kind,
        "topic_ids": list(topic_ids),
        "summary": summary,
        "queries": list(queries),
    }
    if browser_fallback_queries:
        plan["browser_fallback_queries"] = list(browser_fallback_queries)
    if web_calibration_queries:
        plan["web_calibration_queries"] = list(web_calibration_queries)
    return plan


TOPIC_PLANS: dict[str, Plan] = {
    "EA-DATA": _plan(
        "EA-DATA",
        "Data collection and data quality",
        "topic",
        ("EA-DATA",),
        (
            _entry(
                "ea-data-robot-demonstrations",
                "core",
                'all:"robot demonstration" AND all:data',
                "Find papers that treat demonstrations as reusable robot-learning data.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-data-demonstration-quality",
                "quality",
                'all:"demonstration quality" AND all:"robot learning"',
                "Surface work that audits operator traces, consistency, and usable trajectory quality.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-data-in-the-wild",
                "collection-setting",
                'all:"in-the-wild" AND all:"robot manipulation"',
                "Capture natural-scene collection papers and their generalization tradeoffs.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-data-dataset-curation",
                "adjacent",
                'all:"dataset curation" AND all:"robot learning"',
                "Find dataset organization, filtering, metadata, and quality-control discussions.",
                COMMON_CATEGORIES,
            ),
        ),
        "Queries for robot data collection, demonstration usability, diversity, and quality auditing.",
    ),
    "EA-SENSOR": _plan(
        "EA-SENSOR",
        "Sensors and multimodal perception",
        "topic",
        ("EA-SENSOR",),
        (
            _entry(
                "ea-sensor-multimodal-policy",
                "core",
                'all:multimodal AND all:"robot manipulation" AND all:policy',
                "Find policy papers where sensor fusion affects manipulation behavior.",
                VISION_CATEGORIES,
            ),
            _entry(
                "ea-sensor-tactile-force",
                "contact",
                'all:tactile AND all:force AND all:"robot manipulation"',
                "Cover physical observability beyond RGB, especially contact and force cues.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "ea-sensor-point-cloud",
                "geometry",
                'all:"point cloud" AND all:"robot manipulation"',
                "Find 3D perception papers relevant to spatial constraints and pose-sensitive tasks.",
                VISION_CATEGORIES,
            ),
            _entry(
                "ea-sensor-occlusion",
                "limitation",
                'all:occlusion AND all:"robot perception" AND all:manipulation',
                "Expose perception failure cases where single-view RGB is insufficient.",
                VISION_CATEGORIES,
            ),
        ),
        "Queries for RGB, 3D, tactile, force, proprioceptive, and multimodal robot perception.",
    ),
    "EA-HARDWARE": _plan(
        "EA-HARDWARE",
        "Collection hardware and device routes",
        "topic",
        ("EA-HARDWARE",),
        (
            _entry(
                "ea-hardware-teleop-device",
                "core",
                'all:teleoperation AND all:"data collection" AND all:robot',
                "Find hardware routes used to collect robot demonstrations.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "ea-hardware-slam-demonstration",
                "tracking",
                'all:SLAM AND all:"robot manipulation" AND all:demonstration',
                "Capture tracking and reconstruction limitations in collection devices.",
                VISION_CATEGORIES,
            ),
            _entry(
                "ea-hardware-arkit-tracking",
                "tracking",
                'all:ARKit AND all:robot AND all:tracking',
                "Find low-cost pose-tracking and VIO routes relevant to data capture.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "ea-hardware-handheld-gripper",
                "device-language",
                '(all:"handheld gripper" OR all:"hand-held gripper") AND all:robot',
                "Catch UMI-like collection devices that may not use UMI in metadata.",
                SYSTEM_CATEGORIES,
            ),
        ),
        "Queries for collection devices, SLAM/tracking, handheld interfaces, and hardware cost tradeoffs.",
    ),
    "EA-XEMBODIMENT": _plan(
        "EA-XEMBODIMENT",
        "Cross-embodiment transfer",
        "topic",
        ("EA-XEMBODIMENT",),
        (
            _entry(
                "ea-xembodiment-cross-embodiment",
                "core",
                'all:"cross-embodiment" AND all:"robot manipulation"',
                "Find work that explicitly transfers skills or data across robot bodies.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-xembodiment-retargeting-dexterous",
                "retargeting",
                'all:retargeting AND all:"dexterous hand"',
                "Cover human hand to dexterous robot hand mapping and its limits.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "ea-xembodiment-human-to-robot",
                "transfer",
                'all:"human-to-robot" AND all:demonstration',
                "Find human demonstration transfer papers beyond exact robot teleoperation.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-xembodiment-action-representation",
                "representation",
                'all:"action representation" AND all:embodiment AND all:robot',
                "Expose latent actions, adapters, and interfaces that mediate embodiment mismatch.",
                COMMON_CATEGORIES,
            ),
        ),
        "Queries for retargeting, human-to-robot transfer, action spaces, and embodiment adapters.",
    ),
    "EA-MODEL": _plan(
        "EA-MODEL",
        "Models and pretraining",
        "topic",
        ("EA-MODEL",),
        (
            _entry(
                "ea-model-vla",
                "core",
                'all:"vision-language-action" AND all:robot',
                "Find VLA papers that connect perception, language, and robot action.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-model-named-foundation",
                "named-method",
                '(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot',
                "Capture named robot foundation model lineages and follow-on comparisons.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-model-finetuning",
                "transfer",
                'all:"robot foundation model" AND all:"fine-tuning"',
                "Find evidence about whether pretraining reduces target-task data needs.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-model-action-tokenization",
                "representation",
                'all:"action tokenization" AND all:robot',
                "Surface model papers where action interfaces determine transfer behavior.",
                COMMON_CATEGORIES,
            ),
        ),
        "Queries for VLA, robot foundation models, pretraining, fine-tuning, and action interfaces.",
    ),
    "EA-EVAL": _plan(
        "EA-EVAL",
        "Evaluation systems and world models",
        "topic",
        ("EA-EVAL",),
        (
            _entry(
                "ea-eval-closed-loop",
                "core",
                'all:"closed-loop" AND all:evaluation AND all:robot',
                "Find evaluations that measure deployed policy behavior rather than offline loss only.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "ea-eval-open-loop-benchmark",
                "benchmark",
                'all:"open-loop" AND all:benchmark AND all:robot',
                "Cover fast screening metrics and their mismatch with real execution.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-eval-world-model",
                "world-model",
                'all:"world model" AND all:"robot manipulation"',
                "Find predictive models used for robot planning, screening, or evaluation.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ea-eval-sim-real-correlation",
                "sim-real",
                'all:"sim-real" AND all:correlation AND all:robot',
                "Find work that compares simulation rankings against real robot outcomes.",
                SYSTEM_CATEGORIES,
            ),
        ),
        "Queries for open-loop, closed-loop, benchmark, simulation, and world-model evaluation.",
    ),
    "EA-BIZ": _plan(
        "EA-BIZ",
        "Commercialization and industrial deployment",
        "topic",
        ("EA-BIZ",),
        (
            _entry(
                "ea-biz-industrial-deployment",
                "core",
                'all:"industrial deployment" AND all:robot',
                "Find papers that discuss moving robot systems beyond lab demonstrations.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "ea-biz-reliability",
                "deployment",
                'all:reliability AND all:"robot manipulation" AND all:deployment',
                "Capture reliability, uptime, and operational risk discussions.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "ea-biz-cycle-time",
                "production",
                'all:"cycle time" AND all:robot AND all:automation',
                "Find production-throughput constraints that affect commercial viability.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "ea-biz-failure-recovery",
                "recovery",
                'all:"failure recovery" AND all:robot AND all:deployment',
                "Surface recovery and human takeover work that separates demos from deployment.",
                SYSTEM_CATEGORIES,
            ),
        ),
        "Queries for industrial adoption, reliability, cycle time, recovery, and ROI-adjacent constraints.",
    ),
}

FAMILY_PLANS: dict[str, Plan] = {
    "umi": _plan(
        "umi",
        "UMI family",
        "family",
        ("EA-DATA", "EA-HARDWARE", "EA-XEMBODIMENT"),
        (
            _entry(
                "umi-exact-lineage",
                "exact-lineage",
                'all:"Universal Manipulation Interface"',
                "Find the original UMI lineage and papers spelling out the full method name.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "umi-abbrev-robot-data",
                "exact-lineage",
                'all:UMI AND all:robot AND all:data',
                "Catch metadata that uses the UMI acronym without the expanded phrase.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "umi-named-variants",
                "named-variant",
                '(all:"UMI-3D" OR all:"UMI 3D" OR all:DexUMI OR all:RealDexUMI)',
                "Find named variants that expose 3D, dexterity, and wearable-data limitations.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "umi-force-torque",
                "sensor-extension",
                'all:UMI AND all:force AND all:torque',
                "Find UMI extensions for contact-rich or force-aware data collection.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "umi-handheld-gripper-language",
                "device-language",
                '(all:"handheld gripper" OR all:"hand-held gripper") AND all:demonstration',
                "Catch UMI-like handheld interfaces that may not mention the acronym.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "umi-usability-limitations",
                "limitation",
                'all:usability AND all:gripper AND all:"robot learning"',
                "Find papers that critique operator burden, gripper design, and data usability.",
                COMMON_CATEGORIES,
            ),
        ),
        "Named UMI lineage, variants, hardware language, force extensions, and usability limits.",
        (
            _browser_entry(
                "browser-umi-named-lineage",
                'site:arxiv.org/abs ("Universal Manipulation Interface" OR "UMI-FT" OR "UMI-3D" OR DexUMI OR RealDexUMI) robot manipulation',
                "Find UMI lineage and named variants through arXiv pages when API metadata search misses exact names.",
            ),
            _browser_entry(
                "browser-umi-usability-quality",
                'site:arxiv.org/abs (UMI OR "handheld gripper" OR "hand-held gripper") ("demonstration quality" OR usability OR ergonomics) "robot learning"',
                "Find negative or conditional UMI data-usability discussions around gripper design and operator burden.",
            ),
            _browser_entry(
                "browser-umi-sensing-transfer-limits",
                'site:arxiv.org/abs (UMI OR "Universal Manipulation Interface") (SLAM OR occlusion OR tactile OR force OR retargeting OR dexterous)',
                "Find UMI-adjacent limitation papers about sensing, tracking, force, tactile feedback, or embodiment transfer.",
            ),
        ),
    ),
    "droid-ego4d": _plan(
        "droid-ego4d",
        "DROID and Ego4D data family",
        "family",
        ("EA-DATA", "EA-HARDWARE", "EA-MODEL"),
        (
            _entry(
                "droid-robot-manipulation",
                "named-dataset",
                'all:DROID AND all:"robot manipulation"',
                "Find DROID robot data papers and reuse discussions.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "ego4d-robot-learning",
                "named-dataset",
                'all:Ego4D AND all:"robot learning"',
                "Catch robot-learning papers that draw on egocentric human video data.",
                VISION_CATEGORIES,
            ),
            _entry(
                "droid-ego-egocentric-video",
                "adjacent-data",
                'all:"egocentric video" AND all:"robot learning"',
                "Find human-observation data papers near Ego4D even when the dataset is not named.",
                VISION_CATEGORIES,
            ),
            _entry(
                "droid-ego-in-the-wild",
                "collection-setting",
                'all:"in-the-wild" AND all:"robot demonstration"',
                "Capture natural-environment data collection and scaling constraints.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "droid-ego-data-mixture",
                "data-mixture",
                'all:"data mixture" AND all:"robot learning"',
                "Find cross-dataset mixture papers that discuss data compatibility and noise.",
                COMMON_CATEGORIES,
            ),
        ),
        "Large robot and egocentric data sources, in-the-wild collection, and cross-dataset reuse.",
    ),
    "teleoperation-demo-quality": _plan(
        "teleoperation-demo-quality",
        "Teleoperation and demonstration quality",
        "family",
        ("EA-DATA", "EA-HARDWARE", "EA-EVAL"),
        (
            _entry(
                "teleop-imitation-learning",
                "core",
                'all:teleoperation AND all:"imitation learning" AND all:robot',
                "Find the main literature surface connecting teleoperation to robot policy learning.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "teleop-demonstration-quality",
                "quality",
                'all:"demonstration quality" AND all:"robot learning"',
                "Surface trace consistency, operator skill, and data acceptance criteria.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "teleop-operator-burden",
                "human-factor",
                'all:operator AND all:burden AND all:teleoperation',
                "Find papers about human workload and collection throughput.",
                ("cs.RO", "cs.HC", "cs.AI"),
            ),
            _entry(
                "teleop-latency",
                "system-limitation",
                'all:latency AND all:teleoperation AND all:robot',
                "Capture delay and synchronization limits that affect demonstration fidelity.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "teleop-action-interface",
                "policy-interface",
                'all:"action interface" AND all:robot AND all:demonstration',
                "Find work where action-space choices determine whether demonstrations transfer.",
                COMMON_CATEGORIES,
            ),
        ),
        "Teleoperation interfaces, operator burden, latency, and demonstration-data validity.",
    ),
    "vla": _plan(
        "vla",
        "Vision-language-action model family",
        "family",
        ("EA-MODEL", "EA-DATA", "EA-XEMBODIMENT", "EA-EVAL"),
        (
            _entry(
                "vla-core",
                "core",
                'all:"vision-language-action" AND all:robot',
                "Find VLA papers that directly model robot actions from vision and language.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "vla-named-models",
                "named-method",
                '(all:RT-X OR all:Octo OR all:OpenVLA) AND all:"robot learning"',
                "Catch named robot foundation model families and comparative work.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "vla-open-x-embodiment",
                "data-source",
                '(all:"Open X-Embodiment" OR all:"Open X Embodiment") AND all:robot',
                "Find cross-embodiment robot data mixtures that often form the real-robot layer of VLA data pyramids.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "vla-large-scale-robot-data",
                "data-scaling",
                'all:"large-scale" AND all:"robot data"',
                "Surface scaling and dataset-layer discussions for robot foundation models.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "vla-robot-foundation-action",
                "foundation-model",
                'all:"robot foundation model" AND all:action',
                "Find broader foundation-model papers whose metadata may not use VLA.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "vla-finetuning-policy",
                "transfer",
                'all:"fine-tuning" AND all:"robot policy"',
                "Surface evidence about target-task adaptation and data requirements.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "vla-data-mixture",
                "data-mixture",
                'all:"data mixture" AND all:"robot foundation model"',
                "Find mixture and dataset composition papers that explain scaling behavior.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "vla-negative-transfer",
                "limitation",
                'all:"negative transfer" AND all:robot AND all:policy',
                "Search for failure cases where broad pretraining hurts target deployment.",
                COMMON_CATEGORIES,
            ),
        ),
        "VLA, RT-X/Octo/OpenVLA-style models, fine-tuning, data mixtures, and transfer limits.",
        (
            _browser_entry(
                "browser-vla-named-models",
                'site:arxiv.org/abs ("vision-language-action" OR OpenVLA OR "RT-X" OR Octo) robot',
                "Find VLA and named robot foundation model papers when acronym or model names are sparse in API results.",
            ),
            _browser_entry(
                "browser-vla-data-mixtures",
                'site:arxiv.org/abs ("Open X-Embodiment" OR "robot foundation model" OR VLA) ("data mixture" OR "fine-tuning" OR "large-scale robot data")',
                "Find VLA data-layer, data-mixture, and fine-tuning discussions likely to mention data quality or scaling limits.",
            ),
            _browser_entry(
                "browser-vla-transfer-limits",
                'site:arxiv.org/abs (VLA OR "vision-language-action" OR OpenVLA) ("negative transfer" OR embodiment OR "action representation" OR "closed-loop")',
                "Find VLA limitation discussions around embodiment, action spaces, transfer, and closed-loop deployment.",
            ),
        ),
    ),
    "sim2real": _plan(
        "sim2real",
        "Sim2Real family",
        "family",
        ("EA-MODEL", "EA-EVAL", "EA-DATA"),
        (
            _entry(
                "sim2real-core",
                "core",
                '(all:sim2real OR all:"sim-to-real") AND all:robot',
                "Find the main simulation-to-real transfer literature surface.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "sim2real-real-validation",
                "validation",
                'all:"real robot" AND all:validation AND all:simulation',
                "Find papers that verify simulation claims against real robot runs.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "sim2real-synthetic-data",
                "data-generation",
                'all:"synthetic data" AND all:"robot manipulation"',
                "Capture synthetic-data pipelines used to reduce real collection cost.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "sim2real-domain-randomization",
                "method",
                'all:"domain randomization" AND all:"robot manipulation"',
                "Find robustification methods for visual and physical sim-to-real gaps.",
                VISION_CATEGORIES,
            ),
            _entry(
                "sim2real-correlation",
                "evaluation",
                'all:"sim-real" AND all:correlation AND all:evaluation',
                "Surface work that measures whether simulation rankings predict real performance.",
                SYSTEM_CATEGORIES,
            ),
        ),
        "Simulation transfer, synthetic data, real-robot validation, and sim-real correlation.",
        (
            _browser_entry(
                "browser-sim2real-core",
                'site:arxiv.org/abs (sim2real OR "sim-to-real" OR "simulation-to-real") robot',
                "Find sim-to-real papers through web/arXiv pages when API search under-recovers variants.",
            ),
            _browser_entry(
                "browser-sim2real-synthetic-validation",
                'site:arxiv.org/abs ("synthetic data" OR "domain randomization" OR simulation) ("real robot" OR validation) manipulation',
                "Find synthetic-data and domain-randomization papers that discuss whether simulated data transfers to real robots.",
            ),
            _browser_entry(
                "browser-sim2real-eval-gap",
                'site:arxiv.org/abs ("sim-real" OR "reality gap" OR "simulation gap") (correlation OR evaluation OR benchmark) robot',
                "Find simulation evaluation and reality-gap discussions that may not use the sim2real keyword.",
            ),
        ),
    ),
    "world-model": _plan(
        "world-model",
        "World-model family",
        "family",
        ("EA-EVAL", "EA-MODEL"),
        (
            _entry(
                "world-model-robot",
                "core",
                'all:"world model" AND all:robot',
                "Find robot papers that explicitly use world-model terminology.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "world-model-video-prediction",
                "prediction",
                'all:"video prediction" AND all:"robot manipulation"',
                "Capture predictive visual models used for planning or offline rollout.",
                VISION_CATEGORIES,
            ),
            _entry(
                "world-model-planning",
                "planning",
                'all:planning AND all:"world model" AND all:robot',
                "Find papers where a predictive model is used to choose actions.",
                COMMON_CATEGORIES,
            ),
            _entry(
                "world-model-contact",
                "physical-limitation",
                'all:contact AND all:"world model" AND all:manipulation',
                "Search for contact realism and physical executability limitations.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "world-model-long-horizon",
                "limitation",
                'all:"long-horizon" AND all:prediction AND all:robot',
                "Find long-horizon consistency and compounding-error discussions.",
                COMMON_CATEGORIES,
            ),
        ),
        "World models for robot prediction, planning, contact realism, and offline evaluation.",
    ),
    "retargeting": _plan(
        "retargeting",
        "Retargeting family",
        "family",
        ("EA-XEMBODIMENT", "EA-HARDWARE", "EA-SENSOR"),
        (
            _entry(
                "retargeting-robot-manipulation",
                "core",
                'all:retargeting AND all:"robot manipulation"',
                "Find the broad retargeting literature for manipulation tasks.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "retargeting-human-to-robot-mapping",
                "transfer",
                'all:"human-to-robot" AND all:mapping',
                "Capture human motion or hand data mapped onto robot embodiments.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "retargeting-dexterous-hand",
                "embodiment",
                'all:"dexterous hand" AND all:retargeting',
                "Find fine-grained human hand to dexterous hand transfer papers.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "retargeting-gripper-demonstration",
                "embodiment",
                'all:gripper AND all:"human demonstration" AND all:robot',
                "Search for lower-DOF gripper abstractions of human demonstrations.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "retargeting-morphology-gap",
                "limitation",
                'all:"morphology gap" AND all:robot',
                "Find papers that name embodiment mismatch as a transfer limit.",
                COMMON_CATEGORIES,
            ),
        ),
        "Human-to-robot mapping, dexterous-hand retargeting, gripper abstraction, and morphology gaps.",
    ),
    "tactile-force": _plan(
        "tactile-force",
        "Tactile and force family",
        "family",
        ("EA-SENSOR", "EA-DATA", "EA-BIZ"),
        (
            _entry(
                "tactile-force-tactile-manipulation",
                "core",
                'all:tactile AND all:"robot manipulation"',
                "Find tactile sensing papers tied to manipulation policies or control.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "tactile-force-force-torque",
                "force",
                'all:force AND all:torque AND all:robot',
                "Cover force/torque observability and low-dimensional contact feedback.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "tactile-force-slip-detection",
                "contact-state",
                'all:"slip detection" AND all:robot',
                "Find tactile and force cues for grasp stability and material interaction.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "tactile-force-contact-rich",
                "task-family",
                'all:"contact-rich" AND all:manipulation',
                "Surface high-contact tasks where vision-only policies often fail.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "tactile-force-sensor-fusion",
                "fusion",
                'all:"sensor fusion" AND all:tactile AND all:robot',
                "Find multimodal policies combining tactile, force, vision, or proprioception.",
                SYSTEM_CATEGORIES,
            ),
        ),
        "Tactile sensing, force/torque, slip, contact-rich manipulation, and multimodal fusion.",
    ),
    "last-centimeter": _plan(
        "last-centimeter",
        "Last-centimeter family",
        "family",
        ("EA-BIZ", "EA-SENSOR", "EA-EVAL"),
        (
            _entry(
                "last-centimeter-exact",
                "core",
                'all:"last centimeter" AND all:robot',
                "Catch papers that explicitly name the deployment bottleneck.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "last-centimeter-visual-servoing",
                "pre-contact",
                'all:"visual servoing" AND all:"robot manipulation"',
                "Find close-range pose correction before contact closure.",
                VISION_CATEGORIES,
            ),
            _entry(
                "last-centimeter-force-insertion",
                "contact",
                'all:"force control" AND all:insertion AND all:robot',
                "Surface insertion and compliant-contact methods for final alignment.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "last-centimeter-failure-recovery",
                "recovery",
                'all:"failure recovery" AND all:"robot manipulation"',
                "Find retry, recovery, and takeover strategies after near-goal failures.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "last-centimeter-fixture",
                "deployment-adjacent",
                '(all:fixture OR all:fixturing) AND all:robot AND all:insertion',
                "Capture fixture and workcell design that reduces contact uncertainty.",
                SYSTEM_CATEGORIES,
            ),
        ),
        "Final approach, contact transition, insertion, force control, recovery, and fixtures.",
    ),
    "industrial-deployment": _plan(
        "industrial-deployment",
        "Industrial deployment family",
        "family",
        ("EA-BIZ", "EA-EVAL", "EA-SENSOR"),
        (
            _entry(
                "industrial-deployment-core",
                "core",
                'all:"industrial robot" AND all:deployment',
                "Find deployment papers in manufacturing or production contexts.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "industrial-deployment-reliability",
                "reliability",
                'all:reliability AND all:robot AND all:deployment',
                "Capture uptime, fault tolerance, and long-run operational evidence.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "industrial-deployment-cycle-time",
                "production",
                'all:"cycle time" AND all:automation AND all:robot',
                "Find throughput constraints that affect ToB feasibility.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "industrial-deployment-yield",
                "production-quality",
                'all:yield AND all:robot AND all:manufacturing',
                "Surface quality and yield discussions beyond one-off success rate.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "industrial-deployment-acceptance-testing",
                "evaluation",
                'all:"acceptance testing" AND all:robot',
                "Find validation and acceptance language for production handoff.",
                SYSTEM_CATEGORIES,
            ),
            _entry(
                "industrial-deployment-roi",
                "business-adjacent",
                'all:ROI AND all:robot AND all:automation',
                "Search for cost or return-on-investment framing when present in technical metadata.",
                SYSTEM_CATEGORIES,
            ),
        ),
        "Reliability, throughput, yield, validation, recovery, and ROI-adjacent industrial constraints.",
    ),
}

_KEY_RANK = {key: index for index, key in enumerate((*TOPIC_ORDER, *FAMILY_ORDER))}


def _slug(value: str) -> str:
    folded = value.casefold()
    normalized = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "-", folded)
    return normalized.strip("-")


_CANONICAL_BY_SLUG = {
    _slug(key): key
    for key in (*TOPIC_ORDER, *FAMILY_ORDER)
}

_ALIAS_PAIRS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("data", ("EA-DATA",)),
    ("data collection", ("EA-DATA",)),
    ("data quality", ("EA-DATA",)),
    ("demonstration data", ("EA-DATA",)),
    ("robot demonstration", ("EA-DATA",)),
    ("trajectory quality", ("EA-DATA", "teleoperation-demo-quality")),
    ("dataset curation", ("EA-DATA",)),
    ("数据", ("EA-DATA",)),
    ("数据采集", ("EA-DATA",)),
    ("数据质量", ("EA-DATA",)),
    ("示教数据", ("EA-DATA",)),
    ("轨迹质量", ("EA-DATA", "teleoperation-demo-quality")),
    ("sensor", ("EA-SENSOR",)),
    ("sensors", ("EA-SENSOR",)),
    ("multimodal", ("EA-SENSOR",)),
    ("rgb", ("EA-SENSOR",)),
    ("depth", ("EA-SENSOR",)),
    ("point cloud", ("EA-SENSOR",)),
    ("force", ("EA-SENSOR", "tactile-force")),
    ("torque", ("EA-SENSOR", "tactile-force")),
    ("tactile", ("tactile-force", "EA-SENSOR")),
    ("proprioception", ("EA-SENSOR",)),
    ("occlusion", ("EA-SENSOR", "EA-DATA")),
    ("传感器", ("EA-SENSOR",)),
    ("多模态", ("EA-SENSOR",)),
    ("触觉", ("tactile-force", "EA-SENSOR")),
    ("力控", ("tactile-force", "EA-SENSOR")),
    ("点云", ("EA-SENSOR",)),
    ("硬件", ("EA-HARDWARE",)),
    ("采集硬件", ("EA-HARDWARE",)),
    ("hardware", ("EA-HARDWARE",)),
    ("collection device", ("EA-HARDWARE",)),
    ("tracking", ("EA-HARDWARE",)),
    ("slam", ("EA-HARDWARE",)),
    ("arkit", ("EA-HARDWARE",)),
    ("vr tracking", ("EA-HARDWARE", "teleoperation-demo-quality")),
    ("handheld gripper", ("umi", "EA-HARDWARE", "EA-DATA")),
    ("hand-held gripper", ("umi", "EA-HARDWARE", "EA-DATA")),
    ("指套", ("EA-HARDWARE", "retargeting")),
    ("手套", ("EA-HARDWARE", "retargeting")),
    ("cross embodiment", ("EA-XEMBODIMENT", "retargeting")),
    ("cross-embodiment", ("EA-XEMBODIMENT", "retargeting")),
    ("retargeting", ("retargeting", "EA-XEMBODIMENT")),
    ("embodiment adapter", ("EA-XEMBODIMENT",)),
    ("human to robot", ("retargeting", "EA-XEMBODIMENT")),
    ("human-to-robot", ("retargeting", "EA-XEMBODIMENT")),
    ("dexterous hand", ("retargeting", "EA-XEMBODIMENT")),
    ("gripper", ("EA-XEMBODIMENT", "EA-HARDWARE")),
    ("action space", ("EA-XEMBODIMENT", "EA-MODEL")),
    ("跨本体", ("EA-XEMBODIMENT", "retargeting")),
    ("人手迁移", ("retargeting", "EA-XEMBODIMENT")),
    ("灵巧手", ("retargeting", "EA-XEMBODIMENT")),
    ("夹爪", ("EA-XEMBODIMENT", "EA-HARDWARE")),
    ("model", ("EA-MODEL",)),
    ("pretraining", ("EA-MODEL",)),
    ("foundation model", ("EA-MODEL", "vla")),
    ("robot foundation model", ("EA-MODEL", "vla")),
    ("vla", ("vla", "EA-MODEL")),
    ("vision language action", ("vla", "EA-MODEL")),
    ("vision-language-action", ("vla", "EA-MODEL")),
    ("rt x", ("vla", "EA-MODEL")),
    ("rt-x", ("vla", "EA-MODEL")),
    ("octo", ("vla", "EA-MODEL")),
    ("openvla", ("vla", "EA-MODEL")),
    ("pi0", ("vla", "EA-MODEL")),
    ("fine tuning", ("EA-MODEL",)),
    ("fine-tuning", ("EA-MODEL",)),
    ("预训练", ("EA-MODEL",)),
    ("微调", ("EA-MODEL",)),
    ("机器人基础模型", ("EA-MODEL", "vla")),
    ("统一模型", ("EA-MODEL", "vla")),
    ("eval", ("EA-EVAL",)),
    ("evaluation", ("EA-EVAL",)),
    ("benchmark", ("EA-EVAL",)),
    ("open loop", ("EA-EVAL",)),
    ("open-loop", ("EA-EVAL",)),
    ("closed loop", ("EA-EVAL",)),
    ("closed-loop", ("EA-EVAL",)),
    ("world model", ("world-model", "EA-EVAL", "EA-MODEL")),
    ("sim real", ("sim2real", "EA-EVAL", "EA-MODEL")),
    ("sim-real", ("sim2real", "EA-EVAL", "EA-MODEL")),
    ("评测", ("EA-EVAL",)),
    ("评测体系", ("EA-EVAL",)),
    ("闭环评测", ("EA-EVAL",)),
    ("开放环评测", ("EA-EVAL",)),
    ("世界模型", ("world-model", "EA-EVAL", "EA-MODEL")),
    ("sim2real", ("sim2real", "EA-MODEL", "EA-EVAL")),
    ("sim-to-real", ("sim2real", "EA-MODEL", "EA-EVAL")),
    ("simulation to real", ("sim2real", "EA-MODEL", "EA-EVAL")),
    ("simulation data", ("sim2real", "EA-DATA", "EA-MODEL", "EA-EVAL")),
    ("simulation data limitation", ("sim2real", "EA-DATA", "EA-MODEL", "EA-EVAL")),
    ("simulation limitation", ("sim2real", "EA-EVAL", "EA-MODEL")),
    ("domain randomization", ("sim2real", "EA-MODEL", "EA-EVAL")),
    ("synthetic data", ("sim2real", "EA-DATA", "EA-MODEL")),
    ("仿真到现实", ("sim2real", "EA-MODEL", "EA-EVAL")),
    ("仿真评测", ("sim2real", "EA-EVAL")),
    ("仿真数据", ("sim2real", "EA-DATA", "EA-MODEL", "EA-EVAL")),
    ("仿真数据局限", ("sim2real", "EA-DATA", "EA-MODEL", "EA-EVAL")),
    ("仿真数据限制", ("sim2real", "EA-DATA", "EA-MODEL", "EA-EVAL")),
    ("仿真局限", ("sim2real", "EA-EVAL", "EA-MODEL")),
    ("仿真限制", ("sim2real", "EA-EVAL", "EA-MODEL")),
    ("commercialization", ("EA-BIZ",)),
    ("business", ("EA-BIZ",)),
    ("deployment", ("EA-BIZ", "industrial-deployment")),
    ("industrial", ("industrial-deployment", "EA-BIZ")),
    ("industrial deployment", ("industrial-deployment", "EA-BIZ")),
    ("roi", ("EA-BIZ", "industrial-deployment")),
    ("cycle time", ("industrial-deployment", "EA-BIZ")),
    ("yield", ("industrial-deployment", "EA-BIZ")),
    ("reliability", ("industrial-deployment", "EA-BIZ", "EA-EVAL")),
    ("last centimeter", ("last-centimeter", "EA-BIZ", "EA-SENSOR")),
    ("visual servoing", ("last-centimeter", "EA-SENSOR")),
    ("insertion", ("last-centimeter", "EA-SENSOR")),
    ("fixture", ("last-centimeter", "industrial-deployment", "EA-BIZ")),
    ("fixturing", ("last-centimeter", "industrial-deployment", "EA-BIZ")),
    ("商业化", ("EA-BIZ",)),
    ("工业落地", ("industrial-deployment", "EA-BIZ")),
    ("最后一厘米", ("last-centimeter", "EA-BIZ", "EA-SENSOR")),
    ("节拍", ("industrial-deployment", "EA-BIZ")),
    ("良率", ("industrial-deployment", "EA-BIZ")),
    ("umi", ("umi", "EA-DATA", "EA-HARDWARE")),
    ("universal manipulation interface", ("umi", "EA-DATA", "EA-HARDWARE")),
    ("fast umi", ("umi", "EA-DATA")),
    ("umi 3d", ("umi", "EA-DATA", "EA-HARDWARE")),
    ("umi-3d", ("umi", "EA-DATA", "EA-HARDWARE")),
    ("umi ft", ("umi", "EA-DATA", "EA-SENSOR")),
    ("umi-ft", ("umi", "EA-DATA", "EA-SENSOR")),
    ("dexumi", ("umi", "retargeting", "EA-XEMBODIMENT")),
    ("realdexumi", ("umi", "retargeting", "EA-XEMBODIMENT")),
    ("droid", ("droid-ego4d", "EA-DATA")),
    ("ego4d", ("droid-ego4d", "EA-DATA")),
    ("ego 4d", ("droid-ego4d", "EA-DATA")),
    ("egocentric video", ("droid-ego4d", "EA-DATA", "EA-SENSOR")),
    ("in the wild", ("droid-ego4d", "EA-DATA")),
    ("in-the-wild", ("droid-ego4d", "EA-DATA")),
    ("teleoperation", ("teleoperation-demo-quality", "EA-HARDWARE", "EA-DATA")),
    ("teleop", ("teleoperation-demo-quality", "EA-HARDWARE", "EA-DATA")),
    ("demo quality", ("teleoperation-demo-quality", "EA-DATA")),
    ("demonstration quality", ("teleoperation-demo-quality", "EA-DATA")),
    ("operator burden", ("teleoperation-demo-quality", "EA-HARDWARE")),
    ("latency", ("teleoperation-demo-quality", "EA-HARDWARE", "EA-EVAL")),
    ("action interface", ("teleoperation-demo-quality", "EA-XEMBODIMENT")),
    ("遥操作", ("teleoperation-demo-quality", "EA-HARDWARE", "EA-DATA")),
    ("示教质量", ("teleoperation-demo-quality", "EA-DATA")),
)

ALIASES: dict[str, tuple[str, ...]] = {
    _slug(alias): keys
    for alias, keys in _ALIAS_PAIRS
}

_SIMULATION_DATA_SIGNALS = (
    "simulation-data",
    "simulated-data",
    "synthetic-data",
    "simulation",
    "sim-to-real",
    "sim2real",
    "仿真数据",
    "合成数据",
    "模拟数据",
    "仿真",
)

_LIMITATION_SIGNALS = (
    "limitation",
    "limitations",
    "limit",
    "failure",
    "fail",
    "gap",
    "invalid",
    "breakdown",
    "局限",
    "限制",
    "失效",
    "失败",
    "缺陷",
    "不足",
    "鸿沟",
)

_VLA_SIGNALS = (
    "vla",
    "vision-language-action",
    "vision-language-action-model",
    "robot-foundation-model",
    "openvla",
    "rt-x",
    "机器人基础模型",
    "视觉语言动作",
)

_DATA_PYRAMID_SIGNALS = (
    "data-pyramid",
    "data-hierarchy",
    "data-stack",
    "data-scaling",
    "scaling-law",
    "large-scale-data",
    "data-mixture",
    "数据金字塔",
    "数据层级",
    "数据栈",
    "数据体系",
    "数据结构",
    "数据配比",
    "数据混合",
    "数据规模",
    "scaling",
)


def normalize_key(value: str) -> str:
    """Return a canonical taxonomy key for an exact key or alias.

    Unknown values are returned as a normalized slug so callers can decide
    whether to reject them, log them, or use them as local extension keys.
    """

    slug = _slug(value)
    if slug in _CANONICAL_BY_SLUG:
        return _CANONICAL_BY_SLUG[slug]
    keys = ALIASES.get(slug)
    if keys:
        return keys[0]
    return slug


def _matches_alias(alias_slug: str, text_slug: str) -> bool:
    if not alias_slug:
        return False
    if re.search(r"[\u4e00-\u9fff]", alias_slug):
        return alias_slug in text_slug
    pattern = rf"(?<![0-9a-z]){re.escape(alias_slug)}(?![0-9a-z])"
    return re.search(pattern, text_slug) is not None


def _rank_key(key: str) -> tuple[int, str]:
    return (_KEY_RANK.get(key, len(_KEY_RANK)), key)


def _contains_any(text_slug: str, signals: Iterable[str]) -> bool:
    return any(_slug(signal) in text_slug for signal in signals)


def _apply_associative_expansions(text_slug: str, keys: set[str]) -> None:
    """Add high-probability adjacent families that may discuss a topic indirectly."""

    simulation_data_limit = _contains_any(text_slug, _SIMULATION_DATA_SIGNALS) and _contains_any(
        text_slug, _LIMITATION_SIGNALS
    )
    if simulation_data_limit:
        # World-model papers often discuss the need for real-world data and the
        # brittleness of simulated or synthetic training data without naming
        # sim2real in metadata.
        keys.update(("world-model", "EA-MODEL", "EA-EVAL"))

    vla_data_pyramid = _contains_any(text_slug, _VLA_SIGNALS) and _contains_any(text_slug, _DATA_PYRAMID_SIGNALS)
    if vla_data_pyramid:
        # VLA data-pyramid questions usually need candidate papers from real
        # robot data, human/egocentric video, and synthetic/simulation layers,
        # even when a paper does not use "pyramid" in metadata.
        keys.update(("vla", "droid-ego4d", "sim2real", "EA-DATA", "EA-MODEL", "EA-EVAL"))


def infer_keys(topic_text: str) -> list[str]:
    """Infer matching topic and family keys from free-form Chinese or English text.

    The function uses only exact canonical-key checks and deterministic alias
    matching plus a small set of explicit associative expansions. It does not
    call a model, perform stemming, or use live web data.
    """

    text_slug = _slug(topic_text)
    if not text_slug:
        return []

    keys: set[str] = set()
    for canonical_slug, canonical_key in _CANONICAL_BY_SLUG.items():
        if _matches_alias(canonical_slug, text_slug):
            keys.add(canonical_key)

    for alias_slug, alias_keys in ALIASES.items():
        if _matches_alias(alias_slug, text_slug):
            keys.update(alias_keys)

    _apply_associative_expansions(text_slug, keys)

    return sorted(keys, key=_rank_key)


__all__ = [
    "ALIASES",
    "COMMON_CATEGORIES",
    "FAMILY_ORDER",
    "FAMILY_PLANS",
    "Plan",
    "QueryEntry",
    "SYSTEM_CATEGORIES",
    "TOPIC_ORDER",
    "TOPIC_PLANS",
    "VISION_CATEGORIES",
    "infer_keys",
    "normalize_key",
]
