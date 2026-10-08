# Coverage & Saturation Report

> **Run**: literature-review-近一年allocentric-representation在具身领域的应用-20260813
> **Review mode**: scoping
> **Time range**: 2025-08-13..2026-08-13
> **Date**: 2026-08-13

---

## 1. Candidate Pool Summary

| Metric | Value | Scoping Floor | Status |
|--------|-------|---------------|--------|
| Candidate papers | 18 | 100 | ⚠️ Below floor |
| Accepted papers | 15 | 15 | ✅ Met floor |
| Full-text recovered | 15 | 35 | ⚠️ Below floor |
| Evidence events | 43 | 15 | ✅ Met floor |

**Discovery method**: Web search (arXiv API unavailable for this run). Candidates discovered via targeted queries on Google Scholar, semantic search, and project page tracing.

---

## 2. Dimension Coverage

| Dimension | Papers | Events | Status |
|-----------|--------|--------|--------|
| Direct topic (allocentric in VLA) | 6 | 18 | ✅ |
| Mechanism (3D representation methods) | 4 | 8 | ✅ |
| Limitation (noise, hallucination, transfer) | 5 | 7 | ✅ |
| Evaluation (benchmarks, diagnostics) | 4 | 6 | ✅ |
| Deployment (real-world, cross-embodiment) | 2 | 2 | ⚠️ |
| Adjacent (surveys, ego-allocentric) | 3 | 2 | ✅ |

---

## 3. Knowledge Unit Coverage

| Knowledge ID | Title | Papers | Events |
|--------------|-------|--------|--------|
| ALLO-3DVLA | 3D representation in VLA | 6 | 16 |
| ALLO-OBJCENT | Object-centric representation | 2 | 4 |
| ALLO-SPATREASON | VLM spatial reasoning | 5 | 12 |
| ALLO-EGOALLOC | Ego-allocentric transformation | 3 | 7 |
| ALLO-SURVEY | Survey & taxonomy | 2 | 4 |

---

## 4. Saturation Assessment

| Round | New unique candidates | Saturation signal |
|-------|----------------------|-------------------|
| Round 1 (web search: allocentric + VLA) | 8 | — |
| Round 2 (web search: 3D representation + robot) | 6 | Diminishing returns |
| Round 3 (web search: spatial reasoning + VLM) | 4 | Near-saturated |

**Max new unique rate (round 3)**: 22% — above 10% threshold, but constrained by arXiv API unavailability rather than topic exhaustion.

---

## 5. Stance Distribution

| Stance | Count | Share |
|--------|-------|-------|
| support | 21 | 49% |
| gap | 11 | 26% |
| conditional | 6 | 14% |
| limit | 5 | 12% |

---

## 6. Confidence Distribution

| Confidence | Count | Share |
|------------|-------|-------|
| direct | 34 | 79% |
| inference | 9 | 21% |
| citation-supported | 0 | 0% |

---

## 7. Gate Assessment

| Gate | Result | Note |
|------|--------|------|
| Coverage (6 dimensions) | ✅ Pass | All 6 dimensions represented |
| Saturation (2 rounds) | ⚠️ Partial | 3 rounds conducted, but new-unique rate above threshold due to API constraint |
| Candidate floor (100) | ❌ Fail | 18 candidates (web search only) |
| Full-text floor (35) | ❌ Fail | 15 full texts (web search only) |
| Evidence floor (15) | ✅ Pass | 43 evidence events |
| Accepted paper floor (15) | ✅ Pass | 15 accepted papers |

**Overall**: Coverage and evidence gates pass. Candidate pool and full-text recovery are below scoping-mode floors due to arXiv API unavailability — conclusions are preliminary in nature.
