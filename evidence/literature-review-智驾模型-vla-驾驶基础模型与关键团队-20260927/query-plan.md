# 智驾调研检索计划

范围：2024-09-27..2026-09-27；经典前序另批。保留原 planner 下限：100 候选、35 完整全文、15 accepted；最少 3 批、连续 2 批新增比例 ≤ 0.1。机器人泛词改为驾驶专属动态检索，原始输出见 query-plan-baseline.json。

## direct-driving-vla

`(all:"autonomous driving" OR all:"self-driving") AND (all:"vision language action" OR all:"VLA")`

## direct-driving-llm

`all:"autonomous driving" AND (all:"large language model" OR all:"vision language model")`

## mechanism-driving-reasoning

`all:"driving" AND (all:"chain of thought" OR all:"reasoning action" OR all:"dual system")`

## mechanism-language-training

`all:"driving" AND (all:"distillation" OR all:"language supervision" OR all:"language teacher")`

## limit-language-driving

`all:"driving" AND (all:"language model") AND (all:"failure" OR all:"hallucination" OR all:"limitations")`

## evaluation-language-driving

`all:"driving" AND (all:"language" OR all:"VLA") AND (all:"benchmark" OR all:"closed-loop" OR all:"evaluation")`

## deployment-driving-model

`all:"driving" AND (all:"foundation model" OR all:"VLA") AND (all:"real-time" OR all:"deployment" OR all:"real-world")`

## adjacent-end-to-end

`all:"autonomous driving" AND (all:"end-to-end" OR all:"foundation model")`

## adjacent-driving-language-data

`all:"driving" AND all:"language" AND (all:"dataset" OR all:"annotation")`
