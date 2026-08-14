# Evidence Appendix: Jim Fan research trajectory: general agents, embodied intelligence, foundation models, and open-world learning

- Time range: 2010-01-01..2026-07-21
- Events: 17
- 每个事件一节,标题即锚点;trace-map 中的 event 链接跳转到这里。

### EA-JIMFAN-READ-0015

- Claim: DreamDojo uses large-scale egocentric human video and continuous latent actions to pretrain a robot world model, then reports bounded policy-evaluation and planning benefits after robot post-training.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2602.06949](https://arxiv.org/abs/2602.06949) DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos
- Locator: 4.7 Downstream Applications
- Evidence: Its policy-evaluation correlation is measured on 20 fruit-packing scenes; the paper also acknowledges optimistic simulation and coverage limitations.
- Quote: “the rank consistency between these two. Fig. ˜ 5(a) shows that DreamDojo ’s success rate has a strong linear correlation with real-world success rate (Pearson =0.995) and maintains a highly consistent ranking (MMRV=0.003), indicating that DreamDojo is able to serve as a reliable simulator for policy evaluation. (a) Real vs. DreamDojo success rates. (b) Model-based planning results. Figure 5 : Downstream applications. We show”
- Authors: shenyuan-gao; william-liang; kaiyuan-zheng; et al.

### EA-JIMFAN-READ-0013

- Claim: BadRobot demonstrates that embodied LLM systems can be jailbroken into unsafe actions and that two tested defenses only partially mitigate the attacks.
- Stance: `limit` | Confidence: `direct`
- Paper: [2407.20242](https://arxiv.org/abs/2407.20242) BadRobot: Jailbreaking Embodied LLM Agents in the Physical World
- Locator: 5 Mitigation, Challenges and Implications
- Evidence: The paper evaluates attacks in embodied-agent simulators and on physical robot setups; defense effects vary across attacks.
- Quote: “A higher indicates stronger alignment. Acting as an additional ‘firewall’, Tab. 3 shows that consistency validation reduces the MSR by on average but still cannot fully mitigate the strong impact of our BadRobot . Comprehensive world model. Xiang et al. ( 2024 ) fine-tunes LLMs using embodied experiences generated in a virtual environment. We evaluate BadRobot on these fine-tuned models (Tab. 3 ) and, although observing an drop in MSR,”
- Authors: hangtao-zhang; chenyu-zhu; xianlong-wang; et al.

### EA-JIMFAN-READ-0008

- Claim: MineDojo combines a large Minecraft task suite, internet-derived multimodal knowledge, and MineCLIP reward learning to support open-ended agent research.
- Stance: `support` | Confidence: `direct`
- Paper: [2206.08853](https://arxiv.org/abs/2206.08853) MineDojo: Building Open-Ended Embodied Agents with Internet-Scale Knowledge
- Locator: Page 9
- Evidence: MineCLIP is reported as competitive with manual rewards on selected programmatic tasks and more robust than vanilla CLIP under visual shifts.
- Quote: “nor manual reward is available for Creative tasks. • CLIPOpenAI: pre-trained OpenAI CLIP model that has not been ﬁnetuned on anyMINE DOJO videos. MINE CLIP is competitive with manual reward. For Programmatic tasks (ﬁrst 8 rows), RL agents guided by MINE CLIP achieve competitive performance as those trained by manual reward. In three of the tasks, they even outperform the hand-engineered reward functions, which rely on privi- leged simulator states unavailable”
- Authors: linxi-fan; guanzhi-wang; yunfan-jiang; et al.

### EA-JIMFAN-READ-0004

- Claim: iGibson provides interactive household simulation, sensor generation, domain randomization, planning, and demonstration tools, with a bounded LiDAR sim-to-real navigation result.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2012.02924](https://arxiv.org/abs/2012.02924) iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes
- Locator: Page 6
- Evidence: The platform broadens the experimental substrate for interactive embodied tasks, but its real-transfer evidence is narrow and materially below simulated success.
- Quote: “in obtaining RGB-based policies that are more generalizable to unseen scenes and textures. Finally, for PointGoal navigation based on LiDAR signals, the policy achieves 33% success rate in Rs int in iGibson, and 24% success rate in the real- world apartment. With only a 9% drop in performance and the failures mostly occurring in the same episodes (same pairs of the initial and goal locations in iGibson and real Fig. 6: Imitation learning from”
- Authors: bokui-shen; fei-xia; chengshu-li; et al.

### EA-JIMFAN-READ-0001

- Claim: The Ladder Network ablation shows that its components contribute unequally: lateral connections and reconstruction are especially important in the tested semi-supervised setting.
- Stance: `support` | Confidence: `direct`
- Paper: [1511.06430](https://arxiv.org/abs/1511.06430) Deconstructing the Ladder Network Architecture
- Locator: Page 8
- Evidence: This early work establishes an ablation-centered habit: unpack a successful architecture rather than treating the whole recipe as one indivisible advance.
- Quote: “regularization effect which helps generalization. This seems to be one of the most im- portant contributors to the performance on the fully supervised task. • The lateral connection is a vital component in the Lad- der architecture to the extent that removing it consid- erably deteriorates the performance for all of the semi- supervised tasks. • The precise choice of the combinator function has a less dramatic impact, although the vanilla combinator can be replaced”
- Authors: mohammad-pezeshki; linxi-fan; philemon-brakel; et al.

### EA-JIMFAN-READ-0002

- Claim: Deep Speech 2 links model progress to joint scaling of data, model size, high-performance training, and deployable inference rather than to architecture alone.
- Stance: `support` | Confidence: `direct`
- Paper: [1512.02595](https://arxiv.org/abs/1512.02595) Deep Speech 2: End-to-End Speech Recognition in English and Mandarin
- Locator: Page 23
- Evidence: The paper's importance for the trajectory is systems thinking: research throughput and serving constraints are treated as part of the learning system.
- Quote: “Normalization, evaluation of RNNs with larger strides with bigram outputs for English, searching through both bidirectional and unidirectional models. This exploration was powered by a well optimized, High Performance Computing inspired training system that allows us to train new, full-scale models on our large datasets in just a few days. Overall, we believe our results conﬁrm and exemplify the value of end-to-end Deep Learning meth- ods for speech recognition”
- Authors: dario-amodei; rishita-anubhai; eric-battenberg; et al.

### EA-JIMFAN-READ-0003

- Claim: SURREAL-System treats distributed-RL infrastructure as an experimental variable: replay sharding and actor batching remove concrete throughput bottlenecks.
- Stance: `support` | Confidence: `direct`
- Paper: [1909.12989](https://arxiv.org/abs/1909.12989) SURREAL-System: Fully-Integrated Stack for Distributed Deep Reinforcement Learning
- Locator: Page 8
- Evidence: The work connects scalable infrastructure, reproducibility, and robotics-suite evaluation in the transition from general ML systems to embodied learning.
- Quote: “on the Gym Cheetah environ- ment. Table 2 shows the number of experiences handled in total with 1, 3, and 5 sharded replays in presence of 128 actors. A single replay buffer can no longer handle all the actor outputs, becoming the bottleneck of the system. Three load-balanced replay buffers resolves congestion. More replays does not further improve overall throughput. 5.3 Batching Actors As described in Sec. 3.3, SURREAL -SYSTEM supports a ﬂexible scheduling”
- Authors: linxi-fan; yuke-zhu; jiren-zhu; et al.

### EA-JIMFAN-READ-0010

- Claim: Voyager's automatic curriculum, executable skill library, and iterative environment feedback jointly support sustained in-context exploration in Minecraft.
- Stance: `support` | Confidence: `direct`
- Paper: [2305.16291](https://arxiv.org/abs/2305.16291) Voyager: An Open-Ended Embodied Agent with Large Language Models
- Locator: 3.3 Evaluation Results
- Evidence: The system continues discovering items and transfers stored programs, while ablations show that curriculum, skills, feedback, and the chosen LLM all matter.
- Quote: “exploration. Results of exploration performance are shown in Fig. 1 . Voyager ’s superiority is evident in its ability to consistently make new strides, discovering 63 unique items within 160 prompting iterations, many novel items compared to its counterparts. On the other hand, AutoGPT lags considerably in discovering new items, while ReAct and Reflexion struggle to make significant progress, given the abstract nature of the open-ended exploration goal that is challenging”
- Authors: guanzhi-wang; yuqi-xie; yunfan-jiang; et al.

### EA-JIMFAN-READ-0005

- Claim: SECANT decouples policy optimization from robust visual representation learning by cloning a weakly augmented RL expert into a strongly augmented student.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2106.09678](https://arxiv.org/abs/2106.09678) SECANT: Self-Expert Cloning for Zero-Shot Generalization of Visual Policies
- Locator: Page 1
- Evidence: The method targets appearance shift across four domains and makes the expert/student separation the mechanism for zero-shot visual robustness.
- Quote: “robust representation learn- ing from policy optimization. Speciﬁcally, an expert policy is ﬁrst trained by RL from scratch with weak augmentations. A student network then learns to mimic the expert policy by supervised learning with strong augmentations, making its representation more robust against visual varia- tions compared to the expert. Extensive experi- ments demonstrate that SECANT signiﬁcantly ad- vances the state of the”
- Authors: linxi-fan; guanzhi-wang; de-an-huang; et al.

### EA-JIMFAN-READ-0006

- Claim: For the tested interactive tasks, sequential representation and pretrained transformer initialization matter more than whether the input sequence uses natural-language semantics.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2202.01771](https://arxiv.org/abs/2202.01771) Pre-Trained Language Models for Interactive Decision-Making
- Locator: Page 9
- Evidence: This qualifies a language-centric reading of the work: much of the transfer can come from sequential structure and pretrained weights.
- Quote: “rates of all approaches reach similar performance. This result indicates that the effectiveness of pre-trained LMs in compositional generalization is not unique to natural language strings, but can be leveraged from arbitrary encodings, although adapting the model to arbitrary encodings may require more training data. 7.2 Sequential Input Representation Table 5: Experiments on sequential inputs and weight initialization. Fine-tuning the pre-trained”
- Authors: shuang-li; xavier-puig; chris-paxton; et al.

### EA-JIMFAN-READ-0007

- Claim: MetaMorph shows that conditioning a transformer controller on morphology can support zero-shot transfer within a modular robot design space.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2203.11931](https://arxiv.org/abs/2203.11931) MetaMorph: Learning Universal Controllers with Transformers
- Locator: Page 7
- Evidence: The work moves from one-policy-per-robot toward a morphology-conditioned controller, while keeping the evidence inside simulated modular designs.
- Quote: “the performance of MetaMorph, just as they do in Transformer based image classiﬁcation. Finally, without access to the morphological information, MetaMorph-NM fails to learn a policy that can control diverse robot morphologies. All of this substantiates our central claim that morphological state information is necessary to learn successful control policies, although the kinematic graph need not be explicitly baked into neural architectures to learn”
- Authors: agrim-gupta; linxi-fan; surya-ganguli; et al.

### EA-JIMFAN-READ-0009

- Claim: VIMA's multimodal-prompt policy and object-centric tokenization improve data efficiency and progressive generalization on its simulated tabletop benchmark.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2210.03094](https://arxiv.org/abs/2210.03094) VIMA: General Robot Manipulation with Multimodal Prompts
- Locator: Page 7
- Evidence: The experiments support multimodal prompting and object-centric structure, but all methods still degrade on novel-task Level 4.
- Quote: “that learn directly from raw pixels, and Object Perceiver that downsamples the object sequence to a fixed number of tokens. just 1% of training data, VIMA already surpasses other variants trained with entire dataset. Finally, across all levels with just 10% of the data, VIMA can outperform other architectures trained with the full dataset by a significant margin. We hypothesize that the data efficiency can be attributed to the object-centric”
- Authors: yunfan-jiang; agrim-gupta; zichen-zhang; et al.

### EA-JIMFAN-READ-0011

- Claim: Eureka's evolutionary search over LLM-generated reward code reaches or exceeds human-designed rewards on most tasks in its simulated suites.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2310.12931](https://arxiv.org/abs/2310.12931) Eureka: Human-Level Reward Design via Coding Large Language Models
- Locator: 4.3 Results
- Evidence: Iterative reward reflection improves generated rewards beyond one-shot sampling, supporting an LLM-as-reward-engineer mechanism in simulation.
- Quote: “Figure 4 , we report the aggregate results on Dexterity and Isaac. Notably, \ourmethod exceeds or performs on par to human level on all Isaac tasks and 15 out of 20 tasks on Dexterity (see App. F for a per-task breakdown). In contrast, L2R, while comparable on low-dimensional tasks (e.g., CartPole, BallBalance), lags significantly behind on high-dimensional tasks. Despite being provided access to some of the same reward components as Human,”
- Authors: yecheng-jason-ma; william-liang; guanzhi-wang; et al.

### EA-JIMFAN-READ-0012

- Claim: DrEureka automates both reward and domain-randomization design for two real-robot settings, while plain Eureka fails the real locomotion transfer.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2406.01967](https://arxiv.org/abs/2406.01967) DrEureka: Language Model Guided Sim-To-Real Transfer
- Locator: VI-A Comparison to Pre-Existing Sim-to-Real Configurations
- Evidence: The negative plain-Eureka result is crucial: a reward adequate for simulation is not sufficient for sim-to-real transfer.
- Quote: “performance does not lag too far behind the best DrEureka configuration and still performs on par with or slightly better than Human-Designed . In contrast, the plain Eureka generated policy fails to walk in the real world, validating that a reward design algorithm suitable for simulation is not sufficient for sim-to-real transfer. More details about our experiments comparing DrEureka’s reward against ablations can be found in the Appendix. Similarly, for cube rotation, we see in”
- Authors: yecheng-jason-ma; william-liang; hung-ju-wang; et al.

### EA-JIMFAN-READ-0014

- Claim: GR00T N1 combines a vision-language System 2 with a diffusion-action System 1 and heterogeneous data, with bounded real humanoid manipulation results.
- Stance: `conditional` | Confidence: `direct`
- Paper: [2503.14734](https://arxiv.org/abs/2503.14734) GR00T N1: An Open Foundation Model for Generalist Humanoid Robots
- Locator: 4.4 Quantitative Results
- Evidence: The model is evaluated on two GR-1 bimanual settings using five objects and three trials per object, alongside broader simulated benchmarks.
- Quote: “target container. For each task, we evaluate the pretrained GR00T-N1-2B model using five different objects, with three trials per object. GR00T-N1-2B achieves a success rate of 76.6% (11.5/15) in the first coordinated setting and 73.3% (11/15) in the second setting involving novel object manipulation. 0.5 stands for grasping the object correctly but failing to place the object into the container. The high performance under these two evaluation”
- Authors: nvidia; johan-bjorck; fernando-castaeda; et al.

### EA-JIMFAN-READ-0016

- Claim: CaP-X shows that high-level robot primitives can inflate coding-agent success while masking failures in lower-level perception, geometry, and control reasoning.
- Stance: `limit` | Confidence: `direct`
- Paper: [2603.22435](https://arxiv.org/abs/2603.22435) CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation
- Locator: 3.3 Discussion
- Evidence: Performance rises with abstraction, but expressivity narrows; multi-turn execution feedback recovers part of the low-level performance gap.
- Quote: “newer architectures exhibit stronger capabilities, none yet match the success rate of human-crafted programs in a zero-shot Pass@1 setting. Takeaway 2: High-Level Abstractions Boost Performance but Limit Expressivity . Figure 3 shows a monotonic increase in task success as primitive abstraction increases, mirroring how prior Code-as-Policies (Liang et al. , 2023 ) approaches relying on high-level primitives report strong zero-shot performance. By collapsing low-level perception,”
- Authors: letian-fu; justin-yu; karim-el-refai; et al.

### EA-JIMFAN-READ-0017

- Claim: A 2026 position paper argues that VLAs and world models remain incomplete without interfaces for physical data, cross-embodiment retargeting, grounded consequences, rewards, and deployment feedback.
- Stance: `gap` | Confidence: `direct`
- Paper: [2606.06556](https://arxiv.org/abs/2606.06556) Robots Need More than VLA and World Models
- Locator: 3 The Missing Components for Physical Intelligence
- Evidence: This is counterevidence at the level of field framing, not an empirical falsification of any single Jim Fan paper.
- Quote: “## 3 The Missing Components for Physical Intelligence The survey above suggests that the next step in robotics is not simply to train larger policies, collect more demonstrations, or build more visually realistic simulators. These directions are necessary, but incomplete. What is missing is a set of components that transform broad physical experience into grounded, deployable robot”
- Authors: elis-karcini; faisal-mehrban; quang-nguyen; et al.

## References

- `1511.06430` [Deconstructing the Ladder Network Architecture](https://arxiv.org/abs/1511.06430) (2015-11-19)
- `1512.02595` [Deep Speech 2: End-to-End Speech Recognition in English and Mandarin](https://arxiv.org/abs/1512.02595) (2015-12-08)
- `1909.12989` [SURREAL-System: Fully-Integrated Stack for Distributed Deep Reinforcement Learning](https://arxiv.org/abs/1909.12989) (2019-09-27)
- `2012.02924` [iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes](https://arxiv.org/abs/2012.02924) (2020-12-05)
- `2106.09678` [SECANT: Self-Expert Cloning for Zero-Shot Generalization of Visual Policies](https://arxiv.org/abs/2106.09678) (2021-06-17)
- `2202.01771` [Pre-Trained Language Models for Interactive Decision-Making](https://arxiv.org/abs/2202.01771) (2022-02-03)
- `2203.11931` [MetaMorph: Learning Universal Controllers with Transformers](https://arxiv.org/abs/2203.11931) (2022-03-22)
- `2206.08853` [MineDojo: Building Open-Ended Embodied Agents with Internet-Scale Knowledge](https://arxiv.org/abs/2206.08853) (2022-06-17)
- `2210.03094` [VIMA: General Robot Manipulation with Multimodal Prompts](https://arxiv.org/abs/2210.03094) (2022-10-06)
- `2305.16291` [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) (2023-05-25)
- `2310.12931` [Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931) (2023-10-19)
- `2406.01967` [DrEureka: Language Model Guided Sim-To-Real Transfer](https://arxiv.org/abs/2406.01967) (2024-06-04)
- `2407.20242` [BadRobot: Jailbreaking Embodied LLM Agents in the Physical World](https://arxiv.org/abs/2407.20242) (2024-07-16)
- `2503.14734` [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734) (2025-03-18)
- `2602.06949` [DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos](https://arxiv.org/abs/2602.06949) (2026-02-06)
- `2603.22435` [CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation](https://arxiv.org/abs/2603.22435) (2026-03-23)
- `2606.06556` [Robots Need More than VLA and World Models](https://arxiv.org/abs/2606.06556) (2026-06-04)
