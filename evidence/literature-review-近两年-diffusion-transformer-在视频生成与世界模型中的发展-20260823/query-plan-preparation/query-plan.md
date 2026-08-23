# Query Plan: 近两年 Diffusion Transformer 在视频生成与世界模型中的发展

## Scope

- Knowledge IDs: EA-EVAL, EA-MODEL
- Families: world-model
- Suggested categories: cs.AI, cs.CV, cs.LG, cs.RO, eess.SY
- Review mode: scoping
- Candidate floor (not a cap): 152
- Full-text floor: 35
- Accepted-paper floor: 15

## arXiv API Queries

| Label | Tier | Query | Why |
|---|---|---|---|
| dit-video-core | core | `all:"diffusion transformer" AND (all:"video generation" OR all:"video synthesis")` | Direct vocabulary for Diffusion Transformer applied to video generation. |
| dit-world-model-core | core | `all:"diffusion transformer" AND all:"world model"` | Diffusion Transformer used as a world model / video-world-model. |
| video-latent-diffusion-core | core | `all:"latent diffusion" AND (all:"video generation" OR all:"video world model")` | Latent video diffusion architecture that underlies DiT-video models. |
| sora-lineage | named-method | `all:"Sora" AND (all:"diffusion" OR all:"world model" OR all:"video")` | Sora demonstrated DiT on video and is a pivotal anchor even without public tech report completeness. |
| stv-lineage | named-method | `all:"Stable Video Diffusion"` | Stable Video Diffusion is a canonical video diffusion method and its successors (SVD-XT, Mochi, LongMoE) form a lineage. |
| genie-lineage | named-method | `all:"Genie" AND (all:"world model" OR all:"interactive")` | Genie / Genie 2 are action-conditioned video world models built on video generation. |
| hunyuan-cogvideo-opensora | named-method | `all:"HunyuanVideo" OR all:"CogVideoX" OR all:"Open-Sora"` | Modern open DiT video models that report architecture, scaling, and evaluation details. |
| veo-moviegen-kling-wan | named-method | `all:"Veo" OR all:"MovieGen" OR all:"Kling" OR all:"Wan"` | Nearer-term flagship video world-model/generation systems frequently benchmarked against. |
| dit-scaling-mechanism | mechanism | `all:"scaling" AND (all:"diffusion transformer" OR all:"diffusion" AND all:"video")` | Scaling-law evidence for diffusion transformers in video/world-model context. |
| rectified-flow-mechanism | mechanism | `all:"flow matching" OR all:"rectified flow"` | Flow matching / rectified flow is the training objective behind most current DiT-video and Sora-style models and shapes quality. |
| video-vae-mechanism | mechanism | `all:"video autoencoder" OR all:"spatiotemporal VAE" OR all:"3D VAE"` | Latent video compression/representation (3D VAE) is a core component on which DiT-video quality depends. |
| spatiotemporal-attention-mechanism | mechanism | `all:"spatiotemporal attention" AND (all:"video" OR all:"diffusion")` | Temporal/space-time attention design inside video DiT. |
| autoregressive-diffusion-hybrid-mechanism | mechanism | `all:"autoregressive" AND all:"diffusion" AND (all:"video" OR all:"token")` | Hybrid autoregressive+diffusion pipelines (e.g. W.A.L.T, next-token video models) competing with pure DiT. |
| physics-consistency-limitation | limitation | `all:"physics" AND all:"video generation" AND (all:"inconsistent" OR all:"violation" OR all:"dynamics")` | Core limitation: generated video lacks physical consistency/real dynamics. |
| temporal-consistency-limitation | limitation | `all:"temporal consistency" AND (all:"video generation" OR all:"world model" OR all:"diffusion")` | Limitation: temporal coherence and long-term consistency of generated video. |
| object-entity-persistence-limitation | limitation | `all:"entity" AND all:"persistence" AND all:"video"` | Limitation: object identity persistence and multimodal interaction in generated scenes. |
| action-conditioned-worldmodel-eval | evaluation | `all:"action-conditioned" AND (all:"world model" OR all:"video prediction" OR all:"planning")` | Evaluation surface: whether DiT-video world models are truly action-controllable and usable for planning. |
| video-world-model-review-eval | evaluation | `all:"video world model" AND (all:"benchmark" OR all:"evaluation" OR all:"survey")` | Evaluation: benchmarks and surveys for video world models. |
| video-reward-model-eval | evaluation | `all:"video reward model" OR all:"video quality assessment"` | Evaluation: reward/quality models for generated video, a practical gate. |
| long-horizon-consistency-eval | evaluation | `all:"long-horizon" AND (all:"video" OR all:"world model" OR all:"consistency")` | Evaluation: long-horizon rollouts and consistency in video world models. |
| inference-cost-deployment | deployment | `all:"diffusion" AND all:"video" AND (all:"accelerat" OR all:"distill" OR all:"efficien")` | Deployment: inference cost, sampling acceleration, and distillation of video diffusion. |
| real-time-distillation-deployment | deployment | `all:"distillation" AND all:"diffusion" AND (all:"video" OR all:"latent" OR all:"model")` | Deployment: one/few-step distillation for practical video generation throughput. |
| robot-video-worldmodel-adjacent | adjacent | `all:"video generation" AND all:"robot"` | Adjacent/embodied: video generation and world models for robotics (links to EA-4D/EA-EVAL). |
| latent-planning-worldmodel-adjacent | adjacent | `all:"latent" AND all:"planning" AND all:"world model"` | Adjacent: planning in the latent space of a video/diffusion world model. |
| video-generation-survey-adjacent | adjacent | `all:"video generation" AND all:"survey"` | Adjacent: surveys mapping the video generation field and its diffusion-transformer core. |
| world-model-robot | core | `all:"world model" AND all:robot` | Find robot papers that explicitly use world-model terminology. |
| world-model-video-prediction | prediction | `all:"video prediction" AND all:"robot manipulation"` | Capture predictive visual models used for planning or offline rollout. |
| world-model-planning | planning | `all:planning AND all:"world model" AND all:robot` | Find papers where a predictive model is used to choose actions. |
| world-model-contact | physical-limitation | `all:contact AND all:"world model" AND all:manipulation` | Search for contact realism and physical executability limitations. |
| world-model-long-horizon | limitation | `all:"long-horizon" AND all:prediction AND all:robot` | Find long-horizon consistency and compounding-error discussions. |
| ea-eval-closed-loop | core | `all:"closed-loop" AND all:evaluation AND all:robot` | Find evaluations that measure deployed policy behavior rather than offline loss only. |
| ea-eval-open-loop-benchmark | benchmark | `all:"open-loop" AND all:benchmark AND all:robot` | Cover fast screening metrics and their mismatch with real execution. |
| ea-eval-world-model | world-model | `all:"world model" AND all:"robot manipulation"` | Find predictive models used for robot planning, screening, or evaluation. |
| ea-eval-sim-real-correlation | sim-real | `all:"sim-real" AND all:correlation AND all:robot` | Find work that compares simulation rankings against real robot outcomes. |
| ea-model-vla | core | `all:"vision-language-action" AND all:robot` | Find VLA papers that connect perception, language, and robot action. |
| ea-model-named-foundation | named-method | `(all:RT-X OR all:Octo OR all:OpenVLA) AND all:robot` | Capture named robot foundation model lineages and follow-on comparisons. |
| ea-model-finetuning | transfer | `all:"robot foundation model" AND all:"fine-tuning"` | Find evidence about whether pretraining reduces target-task data needs. |
| ea-model-action-tokenization | representation | `all:"action tokenization" AND all:robot` | Surface model papers where action interfaces determine transfer behavior. |

## Coverage Dimensions

| Dimension | Minimum candidates | Query labels |
|---|---:|---|
| direct-topic | 3 | dit-video-core, dit-world-model-core, video-latent-diffusion-core, sora-lineage, stv-lineage, genie-lineage, hunyuan-cogvideo-opensora, veo-moviegen-kling-wan, world-model-robot, ea-eval-closed-loop, ea-model-vla, ea-model-named-foundation |
| adjacent-and-transfer | 3 | dit-scaling-mechanism, rectified-flow-mechanism, video-vae-mechanism, spatiotemporal-attention-mechanism, autoregressive-diffusion-hybrid-mechanism, robot-video-worldmodel-adjacent, latent-planning-worldmodel-adjacent, video-generation-survey-adjacent, world-model-video-prediction, world-model-planning, ea-eval-world-model, ea-model-finetuning |
| limits-and-counterevidence | 3 | physics-consistency-limitation, temporal-consistency-limitation, object-entity-persistence-limitation, world-model-contact, world-model-long-horizon |
| evaluation-and-validation | 3 | action-conditioned-worldmodel-eval, video-world-model-review-eval, video-reward-model-eval, long-horizon-consistency-eval, ea-eval-open-loop-benchmark, ea-eval-sim-real-correlation |
| deployment-and-operations | 3 | inference-cost-deployment, real-time-distillation-deployment |
| mechanisms-and-interfaces | 3 | ea-model-action-tokenization |

## Stopping Rule

- Minimum batches: 3
- Consecutive saturation rounds: 2
- Maximum new-unique rate at saturation: 10%
- Candidate, full-text, accepted-paper, and dimension floors must all pass.

## Browser Fallback Queries

| Label | Query | Why |
|---|---|---|
| dit-video-browser | `"diffusion transformer" "video generation" Sora` | Web fallback when arXiv under-recovers flagship DiT-video systems. |
| genie2-worldmodel-browser | `"Genie 2" OR "world model" interactive video` | Check action-conditioned video world-model systems outside arXiv. |

## Web Calibration Queries

| Label | Source | Query | Why |
|---|---|---|---|
| dit-video-calibration | llm | `Diffusion Transformer video generation world model 2025 advances` | Calibrate current DiT-video terminology and flagship systems. |

## Dynamic Suggestions

| Label | Channel | Source | Confidence | Query | Why |
|---|---|---|---|---|---|
| dit-video-core | arxiv_api | llm | high | `all:"diffusion transformer" AND (all:"video generation" OR all:"video synthesis")` | Direct vocabulary for Diffusion Transformer applied to video generation. |
| dit-world-model-core | arxiv_api | llm | high | `all:"diffusion transformer" AND all:"world model"` | Diffusion Transformer used as a world model / video-world-model. |
| video-latent-diffusion-core | arxiv_api | llm | high | `all:"latent diffusion" AND (all:"video generation" OR all:"video world model")` | Latent video diffusion architecture that underlies DiT-video models. |
| sora-lineage | arxiv_api | llm | medium | `all:"Sora" AND (all:"diffusion" OR all:"world model" OR all:"video")` | Sora demonstrated DiT on video and is a pivotal anchor even without public tech report completeness. |
| stv-lineage | arxiv_api | llm | high | `all:"Stable Video Diffusion"` | Stable Video Diffusion is a canonical video diffusion method and its successors (SVD-XT, Mochi, LongMoE) form a lineage. |
| genie-lineage | arxiv_api | llm | medium | `all:"Genie" AND (all:"world model" OR all:"interactive")` | Genie / Genie 2 are action-conditioned video world models built on video generation. |
| hunyuan-cogvideo-opensora | arxiv_api | llm | high | `all:"HunyuanVideo" OR all:"CogVideoX" OR all:"Open-Sora"` | Modern open DiT video models that report architecture, scaling, and evaluation details. |
| veo-moviegen-kling-wan | arxiv_api | llm | medium | `all:"Veo" OR all:"MovieGen" OR all:"Kling" OR all:"Wan"` | Nearer-term flagship video world-model/generation systems frequently benchmarked against. |
| dit-scaling-mechanism | arxiv_api | llm | medium | `all:"scaling" AND (all:"diffusion transformer" OR all:"diffusion" AND all:"video")` | Scaling-law evidence for diffusion transformers in video/world-model context. |
| rectified-flow-mechanism | arxiv_api | llm | high | `all:"flow matching" OR all:"rectified flow"` | Flow matching / rectified flow is the training objective behind most current DiT-video and Sora-style models and shapes quality. |
| video-vae-mechanism | arxiv_api | llm | medium | `all:"video autoencoder" OR all:"spatiotemporal VAE" OR all:"3D VAE"` | Latent video compression/representation (3D VAE) is a core component on which DiT-video quality depends. |
| spatiotemporal-attention-mechanism | arxiv_api | llm | medium | `all:"spatiotemporal attention" AND (all:"video" OR all:"diffusion")` | Temporal/space-time attention design inside video DiT. |
| autoregressive-diffusion-hybrid-mechanism | arxiv_api | llm | medium | `all:"autoregressive" AND all:"diffusion" AND (all:"video" OR all:"token")` | Hybrid autoregressive+diffusion pipelines (e.g. W.A.L.T, next-token video models) competing with pure DiT. |
| physics-consistency-limitation | arxiv_api | llm | medium | `all:"physics" AND all:"video generation" AND (all:"inconsistent" OR all:"violation" OR all:"dynamics")` | Core limitation: generated video lacks physical consistency/real dynamics. |
| temporal-consistency-limitation | arxiv_api | llm | medium | `all:"temporal consistency" AND (all:"video generation" OR all:"world model" OR all:"diffusion")` | Limitation: temporal coherence and long-term consistency of generated video. |
| object-entity-persistence-limitation | arxiv_api | llm | medium | `all:"entity" AND all:"persistence" AND all:"video"` | Limitation: object identity persistence and multimodal interaction in generated scenes. |
| action-conditioned-worldmodel-eval | arxiv_api | llm | medium | `all:"action-conditioned" AND (all:"world model" OR all:"video prediction" OR all:"planning")` | Evaluation surface: whether DiT-video world models are truly action-controllable and usable for planning. |
| video-world-model-review-eval | arxiv_api | llm | medium | `all:"video world model" AND (all:"benchmark" OR all:"evaluation" OR all:"survey")` | Evaluation: benchmarks and surveys for video world models. |
| video-reward-model-eval | arxiv_api | llm | medium | `all:"video reward model" OR all:"video quality assessment"` | Evaluation: reward/quality models for generated video, a practical gate. |
| long-horizon-consistency-eval | arxiv_api | llm | medium | `all:"long-horizon" AND (all:"video" OR all:"world model" OR all:"consistency")` | Evaluation: long-horizon rollouts and consistency in video world models. |
| inference-cost-deployment | arxiv_api | llm | medium | `all:"diffusion" AND all:"video" AND (all:"accelerat" OR all:"distill" OR all:"efficien")` | Deployment: inference cost, sampling acceleration, and distillation of video diffusion. |
| real-time-distillation-deployment | arxiv_api | llm | medium | `all:"distillation" AND all:"diffusion" AND (all:"video" OR all:"latent" OR all:"model")` | Deployment: one/few-step distillation for practical video generation throughput. |
| robot-video-worldmodel-adjacent | arxiv_api | llm | medium | `all:"video generation" AND all:"robot"` | Adjacent/embodied: video generation and world models for robotics (links to EA-4D/EA-EVAL). |
| latent-planning-worldmodel-adjacent | arxiv_api | llm | medium | `all:"latent" AND all:"planning" AND all:"world model"` | Adjacent: planning in the latent space of a video/diffusion world model. |
| video-generation-survey-adjacent | arxiv_api | llm | medium | `all:"video generation" AND all:"survey"` | Adjacent: surveys mapping the video generation field and its diffusion-transformer core. |
| dit-video-browser | browser_fallback | llm | medium | `"diffusion transformer" "video generation" Sora` | Web fallback when arXiv under-recovers flagship DiT-video systems. |
| genie2-worldmodel-browser | browser_fallback | llm | medium | `"Genie 2" OR "world model" interactive video` | Check action-conditioned video world-model systems outside arXiv. |
| dit-video-calibration | web_calibration | llm | medium | `Diffusion Transformer video generation world model 2025 advances` | Calibrate current DiT-video terminology and flagship systems. |

## Calibration Notes

- No live web calibration was provided; generated offline baseline query plan.

## Planner Notes

- llm dynamic expansion (medium): Agent inferred that a video/world-model Diffusion Transformer review needs both the generic DiT-video lineage (Sora/Stable Video Diffusion/Genie/Veo/HunyuanVideo/CogVideoX/Open-Sora) and the limitation/evaluation/action-conditioned world-model surfaces that static embodied taxonomy does not cover.
