# Query Plan: 类脑模型近一年的发展

## Scope

- Knowledge IDs: EA-MODEL
- Families: none
- Suggested categories: cs.AI, cs.LG, cs.RO
- Review mode: scoping
- Candidate floor (not a cap): 100
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| direct-brain-inspired-models | direct | `all:"brain-inspired" AND (all:model OR all:architecture)` | Direct surface for brain-inspired model papers. |
| direct-spiking-large-models | direct | `all:"spiking" AND (all:"large language model" OR all:LLM OR all:transformer)` | Spiking LLM/transformer is the fastest-moving subfamily of the past year (SpikeLLM, SpikingBrain, SpikeGPT lineage). |
| direct-neuromorphic-computing | direct | `all:"neuromorphic computing" OR all:"neuromorphic"` | Core neuromorphic computing surface covering models and co-designed hardware. |
| direct-brain-foundation-model | direct | `all:"brain" AND (all:"foundation model" OR all:"large brain model" OR all:"whole-brain")` | Brain-data foundation models (BrainLM lineage) and whole-brain modeling are a distinct direct surface. |
| mechanism-snn-training | mechanism | `all:"spiking neural network" AND (all:training OR all:"surrogate gradient" OR all:"conversion")` | Mechanism surface: how SNNs are trained (surrogate gradients, ANN-to-SNN conversion) governs model quality. |
| mechanism-bio-plausible-learning | mechanism | `all:"biologically plausible" AND (all:learning OR all:"spike-timing")` | STDP and bio-plausible learning rules are the algorithmic core of brain-inspired models. |
| mechanism-neural-dynamics | mechanism | `all:"neural dynamics" OR all:"oscillations" OR all:"predictive coding" OR all:"attractor"` | Brain-dynamics-inspired mechanisms (oscillation, predictive coding, attractors) emerged as a 2025-2026 differentiator (Rhythm-SNN). |
| mechanism-cognitive-architecture | mechanism | `all:"cognitive architecture" OR all:"cortical" OR all:"hippocampal" OR all:"hippocampus"` | Cortical/hippocampal architecture transfer (memory, continual learning, replay) is a mechanism surface. |
| limit-snn-scaling | limit | `all:"spiking neural network" AND (all:scalability OR all:limitation OR all:challenge OR all:bottleneck)` | Negative/limit evidence: accuracy gap vs ANN, training cost, scaling limits. |
| evaluation-snn-benchmark | evaluation | `all:"spiking" AND (all:benchmark OR all:"energy efficiency" OR all:accuracy OR all:evaluation)` | Evaluation surface: how brain-inspired models are measured (accuracy, energy, latency). |
| deployment-neuromorphic-hardware | deployment | `all:"neuromorphic" AND (all:chip OR all:hardware OR all:memristor OR all:processor)` | Deployment surface: Loihi-class chips, memristor/PCM systems, algorithm-hardware co-design. |
| deployment-event-robotics | deployment | `all:"event camera" OR (all:"spiking" AND (all:robot OR all:embodied OR all:"vision-language-action"))` | Event-driven sensing + spiking embodied models (NeuroVLA lineage) is the deployment-facing frontier. |
| adjacent-organoid-intelligence | adjacent | `all:"organoid intelligence" OR all:"organoid" AND all:"computing" OR all:"Brainoware"` | Adjacent surface: biological-computing hybrids using living neuronal cultures. |
| adjacent-active-inference | adjacent | `all:"active inference" OR all:"free energy principle" OR all:"free-energy"` | Adjacent theory family: brain-theoretic learning frameworks. |
| adjacent-bci-neural-data | adjacent | `all:"brain-computer interface" AND all:model` | Adjacent surface: neural-data models at the BCI boundary. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| adjacent-and-transfer | 3 | direct-brain-inspired-models, direct-spiking-large-models, direct-neuromorphic-computing, direct-brain-foundation-model, mechanism-snn-training, mechanism-bio-plausible-learning, mechanism-neural-dynamics, mechanism-cognitive-architecture, adjacent-organoid-intelligence, adjacent-active-inference, adjacent-bci-neural-data, ea-model-finetuning |
| limits-and-counterevidence | 3 | limit-snn-scaling |
| evaluation-and-validation | 3 | evaluation-snn-benchmark |
| deployment-and-operations | 3 | deployment-neuromorphic-hardware, deployment-event-robotics |
| direct-topic | 3 | ea-model-vla, ea-model-named-foundation |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| browser-spiking-llm-2026 | `spiking large language model 2026 arXiv` | Check for models not well indexed by arXiv API keyword search. |
| browser-brain-inspired-models-2026 | `brain-inspired model 2026 review survey` | Catch recent surveys framing the field's yearly development. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| calibrate-spikingbrain-family | llm-web-calibration | `SpikingBrain 2.0 BICLab spiking foundation model` | Calibrate naming of the CAS/BICLab spiking foundation-model family. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| direct-brain-inspired-models | arxiv_api | llm-web-calibration | medium | `all:"brain-inspired" AND (all:model OR all:architecture)` | Direct surface for brain-inspired model papers. |
| direct-spiking-large-models | arxiv_api | llm-web-calibration | high | `all:"spiking" AND (all:"large language model" OR all:LLM OR all:transformer)` | Spiking LLM/transformer is the fastest-moving subfamily of the past year (SpikeLLM, SpikingBrain, SpikeGPT lineage). |
| direct-neuromorphic-computing | arxiv_api | llm-web-calibration | medium | `all:"neuromorphic computing" OR all:"neuromorphic"` | Core neuromorphic computing surface covering models and co-designed hardware. |
| direct-brain-foundation-model | arxiv_api | llm-web-calibration | medium | `all:"brain" AND (all:"foundation model" OR all:"large brain model" OR all:"whole-brain")` | Brain-data foundation models (BrainLM lineage) and whole-brain modeling are a distinct direct surface. |
| mechanism-snn-training | arxiv_api | llm-web-calibration | high | `all:"spiking neural network" AND (all:training OR all:"surrogate gradient" OR all:"conversion")` | Mechanism surface: how SNNs are trained (surrogate gradients, ANN-to-SNN conversion) governs model quality. |
| mechanism-bio-plausible-learning | arxiv_api | llm-web-calibration | medium | `all:"biologically plausible" AND (all:learning OR all:"spike-timing")` | STDP and bio-plausible learning rules are the algorithmic core of brain-inspired models. |
| mechanism-neural-dynamics | arxiv_api | llm-web-calibration | medium | `all:"neural dynamics" OR all:"oscillations" OR all:"predictive coding" OR all:"attractor"` | Brain-dynamics-inspired mechanisms (oscillation, predictive coding, attractors) emerged as a 2025-2026 differentiator (Rhythm-SNN). |
| mechanism-cognitive-architecture | arxiv_api | llm-web-calibration | medium | `all:"cognitive architecture" OR all:"cortical" OR all:"hippocampal" OR all:"hippocampus"` | Cortical/hippocampal architecture transfer (memory, continual learning, replay) is a mechanism surface. |
| limit-snn-scaling | arxiv_api | llm-web-calibration | medium | `all:"spiking neural network" AND (all:scalability OR all:limitation OR all:challenge OR all:bottleneck)` | Negative/limit evidence: accuracy gap vs ANN, training cost, scaling limits. |
| evaluation-snn-benchmark | arxiv_api | llm-web-calibration | medium | `all:"spiking" AND (all:benchmark OR all:"energy efficiency" OR all:accuracy OR all:evaluation)` | Evaluation surface: how brain-inspired models are measured (accuracy, energy, latency). |
| deployment-neuromorphic-hardware | arxiv_api | llm-web-calibration | high | `all:"neuromorphic" AND (all:chip OR all:hardware OR all:memristor OR all:processor)` | Deployment surface: Loihi-class chips, memristor/PCM systems, algorithm-hardware co-design. |
| deployment-event-robotics | arxiv_api | llm-web-calibration | medium | `all:"event camera" OR (all:"spiking" AND (all:robot OR all:embodied OR all:"vision-language-action"))` | Event-driven sensing + spiking embodied models (NeuroVLA lineage) is the deployment-facing frontier. |
| adjacent-organoid-intelligence | arxiv_api | llm-web-calibration | medium | `all:"organoid intelligence" OR all:"organoid" AND all:"computing" OR all:"Brainoware"` | Adjacent surface: biological-computing hybrids using living neuronal cultures. |
| adjacent-active-inference | arxiv_api | llm-web-calibration | medium | `all:"active inference" OR all:"free energy principle" OR all:"free-energy"` | Adjacent theory family: brain-theoretic learning frameworks. |
| adjacent-bci-neural-data | arxiv_api | llm-web-calibration | low | `all:"brain-computer interface" AND all:model` | Adjacent surface: neural-data models at the BCI boundary. |
| browser-spiking-llm-2026 | browser_fallback | llm-web-calibration | medium | `spiking large language model 2026 arXiv` | Check for models not well indexed by arXiv API keyword search. |
| browser-brain-inspired-models-2026 | browser_fallback | llm-web-calibration | medium | `brain-inspired model 2026 review survey` | Catch recent surveys framing the field's yearly development. |
| calibrate-spikingbrain-family | web_calibration | llm-web-calibration | high | `SpikingBrain 2.0 BICLab spiking foundation model` | Calibrate naming of the CAS/BICLab spiking foundation-model family. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm-web-calibration dynamic expansion (medium): Topic 'brain-inspired models' is outside the static embodied-AI taxonomy. Calibration via web search (2026-08) surfaced: SpikingBrain/瞬悉 1.0 (CAS-IA + MetaX, 2025-09), SpikingBrain 2.0 (BICLab, 2026-04), SpikeLLM, NSLLM (algorithm-hardware co-design), Rhythm-SNN (Nat Commun 2025), NeuroVLA (brain-inspired embodied VLA), PKU memristor neural-dynamics chip (2026-07), organoid intelligence/Brainoware, Hebbian meta-learning for continual learning (AAAI-2026).
