# 近一年类脑模型的发展:三条主线的证据强度分层

## 引言:热闹从何而来

过去一年(2025 年 8 月至 2026 年 8 月),脉冲神经网络(spiking neural network,SNN,以离散脉冲而非连续数值传递信息的网络)路线的热度有直接来源:它第一次在大模型主场上摆出成建制阵容。[SpikingBrain](https://arxiv.org/abs/2509.05276) 在国产 MetaX 集群上把脉冲大模型的稳定训练推到 76B 参数;[SDLLM](https://arxiv.org/abs/2604.16475) 消除了矩阵乘法、只以稀疏加法执行推理;[SpikeMLLM](https://arxiv.org/abs/2604.18610) 把脉冲化扩展到多模态大模型;[SpikeVLA](https://arxiv.org/abs/2606.27807) 给出首个脉冲视觉-语言-动作模型。与此同时,类器官智能(organoid intelligence,以体外培养的神经组织为计算基质的路线)出现了世界模型训练课程蓝图,预测编码拿到了新算法引擎。

热度背后的问题是:这些进展各自把验证强度推到了什么水平?本备忘录基于该时间窗内的 20 篇论文作答,按技术路线组织而非逐篇综述;只覆盖 arXiv 工作,不覆盖期刊或会议独家成果,不作超出证据的趋势预测,数字均按原论文口径转述。

## 中心判断

一年证据支持的判断是:类脑模型的三条主线处在完全不同、却极易被拉平的证据强度上。第一,转换式路线(把已训练的连续网络脉冲化改造再做持续预训练)已完成 7B 到 76B 的端到端工程验证,在通用基准上逼近连续基座——但这条路线的能耗证据全部来自折算或仿真,没有一份芯片实测。第二,神经元动力学与训练机制层面的生物合理改进,增益仍是 ImageNet、CIFAR 量级上零点几到一个百分点,且普遍以额外计算、超参数搜索或非局部训练为代价。第三,类器官智能与预测编码分别停留在"课程蓝图、零实验结果"与"数学框架、中小规模演示"的阶段。一句话:规模是实测的,能效是纸面的,机制增益是点级的,生物基质是前瞻的。本文由此推断:路线成败的关键变量不是基准精度能否继续追平,而是能耗主张能否通过神经形态硬件上的任务级实测。依据是:本批证据中精度类主张都已可复核,能耗类主张则无一例外停在折算口径。

## 规模化:转换式路线的三个台阶

工程上最重的证据来自 SpikingBrain:首个在非 NVIDIA 平台上大规模训练类脑大模型的公开工作,数百卡集群、76B 参数稳定训练、连续运行超两周无中断;MetaX C550 集群上 7B 模型训练达到 1558 TGS 与 23.4% 的模型算力利用率,与同配置 NVIDIA A800 的 25.8% 相当。性能侧,经 150B/160B token 的转换式持续预训练(算力不足从头训练的 2%),7B 版本在下游基准恢复基座约九成性能(MMLU 65.84,对 Qwen2.5 的 74.21);76B 混合 MoE 版本 MMLU 73.58,超过 Llama2-70B 的 69.57 与 Mixtral-8x7B 的 71.23。其实测加速均发生在常规硬件上:1M token 输入下首 token 延迟相对全注意力基线实测加速 26.5 倍(H100,十次平均;4M token 的超 100 倍为拟合曲线外推,基线在该长度无法实测),1B 压缩版本经 llama.cpp 量化后在 64k/128k/256k 序列长度上分别取得 4.04/7.52/15.39 倍解码加速。作者自报的边界清晰:拼接短文本构造的长上下文训练数据对极限上下文性能帮助有限,原生长文本数据才是缩小差距的关键;脉冲激活编码叠加 INT8 权重部署后,常识推理、MMLU 与 CMMLU 平均下降约 2%(实测 1-3% 量级)。

转换式路线内部分化出三种兑现方式。其一是推理期即插即用:SDLLM 在 LLaMA2-7B 上以 4bit 权重加 1.58bit 脉冲编码取得零样本问答平均 61.09、能耗 0.67J,超过最佳低位基线 DuQuant 的 60.57(3.97J),距全精度的 63.72(31.77J)约 2.6 个百分点;在更新的 Qwen2.5-14B 上平均 72.51,大幅高于同位宽 RTN 的 39.35 与 GPTQ 的 36.73——脉冲语义量化对更强基座的退化远小于常规量化。但作者自述其能耗数字按突触操作折算而非芯片实测,异步发放模式在维度过大时还会抬高芯片功耗与通信带宽需求。其二是多模态扩展:SpikeMLLM 在时间步从 15 压到 2 的激进设置下,对 FP16 基线的五基准平均差距仅 1.03%(Qwen2VL-7B)与 0.72%(InternVL2-8B),并揭示文本模态对时间步分配显著更敏感——时间步不足时 OCRBench 只有 32、DocVQA 5.31,把时间步转给文本后恢复到 717 与 84.20;其配套的 SMIC 28nm 加速器报告 393.7 token/s 对 A800 FP16 的 43.5(9.06 倍吞吐)、7.13W 对 184W,但该结果来自综合估计与周期级仿真而非流片实测,GPU 对照也仅是 A800 FP16 批大小 1 的单一配置。其三是算子级替换:[NLSpiking](https://arxiv.org/abs/2605.20289) 免训练地把 Softmax、SiLU、RMSNorm 分解为除法、指数、范数三个脉冲原语,在 LLaMA-3-8B 与 Mistral-7B 上的模型级精度变化仅为 -0.003 与 +0.000,并可扩展到 LLaMA3-70B(W8A8,T=1 时 78.64 对直接转换的 78.85);但作者承认尚无真实脉冲硬件上的端到端部署,延迟结论来自执行模型分析。

从零训练的脉冲语言模型仍是少数派。[BiSpikCLM](https://arxiv.org/abs/2605.13859) 以全二值脉冲、无矩阵乘的架构从随机初始化训练 1.3B 模型,仅用 10B token(OPT-1.3B 需 180B,约 5.6%)达到 42.19% 零样本平均准确率,接近 OPT-1.3B 的 49.73%,每次推理能耗为其 10.6%;其 SNN/ANN 精度比率稳定于 82%-95%,高于 SpikeLLM 的 65.41%-82.55%。训练 token 从 10B 增至 25B,准确率从 41.33% 升至 44.39%。但作者明确定位"主要贡献不是在精度上超越量化方法":同规模对比中它低于 OmniQuant W4A4 的 43.90% 与 TriLM 1.5B 的 43.16%,与 BitNet 1.58-bit 的 42.66% 相当。[NeuronSpark](https://arxiv.org/abs/2603.16148)-0.9B 则标定了从零训练的可行性条件:85,000 步预训练把损失从 9.0 降到 3.5,而七个消融变体的损失全部停滞在 7.0 以上——稳定化组件是该规模下可训练的必要条件。但该模型只有 512-token 上下文,没有 C-Eval/CMMLU 等定量基准与任何 Transformer 基线,仅支持中文;且其层间信号默认是浮点泄漏电流而非二值脉冲,向神经形态通信层的外推需要打折。

小结:规模化故事由转换式路线承担,基准恢复与训练稳定性已可复核;从零训练路线的上限是 1.3B,对标的是量化 ANN 而非全精度基座。而整条大模型路线的能耗数字无一例外是折算或仿真。

## 机制层:生物合理性的增益刻度

神经元模型方向的代表是 QIF(quadratic integrate-and-fire,二次积分发放)神经元的[首个深层 SNN 离散化](https://arxiv.org/abs/2510.05168):它能表达 LIF(leaky integrate-and-fire,漏积分发放)不具备的阈下振荡与输入变化敏感性,在 CIFAR-10/CIFAR-100 上配合 TET 损失以 4 时间步达 96.86%/80.62%,超过此前最佳直接训练方法。但其代价被作者逐条列出:依赖 tdBN 计算代理梯度(以时间步批量归一化近似梯度)、阻碍事件驱动反向传播,每次更新比 LIF 多一次乘法与一次加法,对神经形态芯片实际性能的影响不确定;其训练稳定性来自从离散化参数解析推导梯度窗口,而该推导以 tdBN 归一化假设为前提。在 ImageNet 上它以 70.52%(单次试验)超过 TEBN 的 68.28%,却被使用三元脉冲的 Ternary Spike 以 70.74% 小幅反超——生物合理路线在最大公开基准上的领先幅度不足半点。

自适应脉冲神经元 [NASN](https://arxiv.org/abs/2604.12365) 走功能性视角:高效训练、自适应发放、架构兼容、脉冲驱动推理四性质须同时满足。受控对比中它在 ImageNet-1k 达 75.53% Top-1,超过同架构 LIF 版 1.18 个点;GLUE 上 NASN 版 WE-Spikingformer 平均 67.5%,大幅超过 SpikeBERT 的 59.7% 与 LIF-BERT 的 34.6%,但保留 softmax 与 GeLU 的 SpikeLM 仍更高。更能说明刻度的是问答任务:NASN 版 0.4B 模型平均 29.4%,能耗折算 245.1 mJ 约为 Qwen-1.5B(3398.3 mJ)的 7%——这是明确的能耗-精度权衡而非精度追平。其扩展实验给出重要信号:参数从 0.4B 增至 1.0B 几乎无增益(29.4 到 29.8),预训练 token 从 0.1B 增至 0.5B 却带来 5.7 个点提升(29.8 到 35.5)——瓶颈在数据而非参数。作者同时自认:能耗数字全部为理论折算,尚未在 DVS(动态视觉传感器,事件相机)等神经形态任务上验证。

训练机制侧,[DSTD](https://arxiv.org/abs/2607.14672)(可微脉冲时间离散化)把连续时间 SNN 的训练内存开销降低 60-150 倍(单层 1000 神经元、6000 输入脉冲基准),使单张 GH200 即可训练 9 层卷积 SNN,而此前同路线 16 层网络需要 GPU 集群;配合 synfire 链式时间正则抑制死神经元并支持流水线操作。但作者自认多层训练机制的理论理解不足、需要大量超参数搜索,任务规模止于 CIFAR 与 Fashion-MNIST——该路线的证据强度是"机制可行"而非"大规模实用"。[NeuroTrain](https://arxiv.org/abs/2605.15058) 基准框架把机制层的结构性矛盾摆上台面:局部学习规则减少全局通信与内存压力、契合低功耗神经形态硬件与在线适应,但在挑战性基准上放宽局部性通常能提升性能;而被最广泛采用的代理梯度 BPTT 在空间上依赖全局误差传播、时间上需展开完整模拟时程并存储中间状态,在线学习在内存受限的硬件上仍是核心挑战;转换路线虽然最容易部署大型预训练模型,却把学习与脉冲动力学解耦,没有通往设备端自适应的路径。[脑启发学习综述](https://arxiv.org/abs/2511.04455)补充了机制层最有力的正面证据:仅共享权重符号的网络在 ImageNet 等数据集上已接近反向传播精度,固定反馈权重的 FW-DTP 常取得高于标准目标传播的性能——精确权重传输并非深度网络学习的必要条件;但 Burstprop 类局部规则目前只在数百神经元的 MNIST 级任务上与 BPTT 可比,尚不能外推到大规模或语言场景。其判断是:生物合理算法的进展最终受限于神经科学知识前沿。

## 硬件层:芯片实测与折算数字的分界线

本批证据中真正有芯片或 FPGA 实测的只有两项。[SpiNNaker2](https://arxiv.org/abs/2607.24396) 把处理元数量从上代 18 个增至 152 个,每核配备矩阵乘、卷积、指数/对数专用加速器;INT8 负载芯片实测高能效档 2.77 TOPS/W、高性能档 2.06 TOPS/W,与 NorthPole(2.70)、Groq(2.73)、Jetson Orin Nano(2.68)同表对比处于同一量级——但作者自述"与业界现有水平相当"仅在算子完全驻留片上 SRAM 时成立,层过大时 DRAM 带宽会拉低利用率。两个实测结果最有信息量:其一,DVS 手势深 SNN 实时仿真中,动态电压频率调节的自动档能耗 0.741J,低于固定高性能档的 1.023J 与低性能档的 2.010J,三档准确率均为 92.04%;其二,事件化 GRU 语言模型单批量推理在 SpiNNaker2 上能耗 65 mJ,对 A100 实现的 1.19J 降低 18 倍,但执行时间延长 8 倍——能效与延迟的交换一目了然。其软件栈将全部参数与状态存于每核 SRAM,可实现的网络规模因此受限。[AIGOR](https://arxiv.org/abs/2607.03191) 则把神经元模型、数值格式、数据通路宽度与并行度设为实例生成时才解析的配置轴,以应对 SNN 硬件生态碎片化:在 FPGA 上复现 snnTorch 的 MNIST 95% 精度,单核实测吞吐 568 样本/s;但多节点同步方案仅在仿真中验证至 1000 核,硬件实测上限是 2 块 FPGA,能耗数字被作者明确限定为配置间的相对比较而非对专用芯片的绝对主张,定点精度也只在 2 ms 模拟时间内逐脉冲精确。

系统级视角来自 [Beyond TOPS/W](https://arxiv.org/abs/2608.03514),它对能耗叙事的约束可能是全年最重要的一条:每突触操作能耗只对表征核心有意义,与常规数字系统比较必须使用每完成任务能耗,需计入基线功率乘执行时间、脉冲包路由、神经元状态更新与存储/传感/主机开销;峰值 TOPS/W 不足以比较使用不同表示、精度与工作条件的基底——例如 IBM 34-tile 模拟存内芯片的 12.4 TOPS/W 是含片间通信与模拟外设的持续结果,排除了辅助数字计算与 SRAM;各来源测量边界不同,数值不可用于跨技术排名。其方向判断是:模拟、光子与神经形态技术将作为数字系统内的专用引擎被增量式、负载特定地采用,近期机会集中在重复矩阵运算、稀疏时序处理与常开感知;并点名评测空白:现有报告普遍未与强优化数字基线做覆盖整个任务周期的能耗对比。神经形态扩散语言模型 [N-MDLM](https://arxiv.org/abs/2607.24841) 提供了区制分析的具体案例:约 250M 参数的块扩散模型经量化与脉冲转换后,归一化吞吐与每 token 能耗同时优于自回归与普通扩散基线,而 BLEU 仅轻微下降;但收益依赖硬件区制——计算受限时延迟增益与稀疏度线性相关、与块尺寸无关,内存受限时增大块尺寸会稀释稀疏收益,最大收益需要高内存带宽系统配合较大块尺寸——且全部结论止于仿真与分析,无芯片实测数据。

## 具身与多模态:用控制精度换能效的第一批样本

SpikeVLA 把脉冲化带入视觉-语言-动作模型,作者定位是性能-能效权衡。在 VLN-CE R2R Val-Unseen(RGB-only、无路点)上,其导航误差 5.38、成功率 53.3、SPL 47.9,与最强 RGB 基线 NaVILA(5.28/53.9/49.3)相当,同时内存 6.2GB 对 16.1GB、能耗 49.09J 对 141.25J;与 INT4 量化 VLA 相比,它在精度(SR 53.3 对 48.2)、能耗(49.09J 对 72.49J)与内存(6.1GB 对 8.6GB)三维占优,但理想化算术计算量反而更高(1196.16 对 982.55)。边界同样具体:线速度跟踪误差 0.42,对 NaVILA 的 0.23 接近两倍;脉冲动作策略的回报 26.72,低于 ANN 策略的 33.45 约 20%;能效与实时性在神经形态芯片上仍未验证,当前全部验证止于仿真与 GPU 平台——低功耗部署主张目前是潜力而非实证。事件相机目标检测侧,[Sequence-SOD](https://arxiv.org/abs/2607.26703) 的贡献是序列感知训练:把膜电位显式当作时序记忆,序列内保持 SNN 内部状态、仅在序列间重置,并用包含多个时间点标签的完整事件序列训练。同架构受控对比中,序列训练在所有测试长度上稳定优于单区间训练(完整序列 25.30 对 23.04 mAP,行人 AP 提升最大,14.72 对 10.92),且单区间训练网络在长序列上反而退化——增益来自状态记忆而非数据量。但其 Gen1 榜单最好成绩 26.88 mAP 仍显著低于 ANN/RNN 方法(RVT-B 47.2)与混合架构(HsVT-B 47.8),价值在同架构隔离验证(同基线 18.9 到 26.88)而非榜单名次;其 116 倍推理能耗优势是 45nm CMOS 口径的理论折算,依赖具体数据集的发放率,且只有部署到神经形态硬件才能兑现——论文全部训练与评估在 GPU 时间步仿真上完成,40Hz 预测频率也是依赖输入数据的理论值。

## 类器官与预测编码:从蓝图到首批对照观察

类器官方向最有雄心的文本是一份课程蓝图:[该文](https://arxiv.org/abs/2509.04633)为人类神经类器官设计了三个渐进复杂度的闭环环境(条件回避、一维捕食者-猎物、Pong 复刻),把强化学习奖惩转译为预测编码信号——奖励实现为可预测、低熵的电刺激(低频正弦波,或紫外解笼锁多巴胺),惩罚实现为不可预测、高熵的白噪声刺激——以预测误差驱动突触可塑性,作为自由能原理的直接检验;评估设计主张超越行为指标,用 fEPSP 斜率作突触强度代理(持续上升为长时程增强、下降为长时程抑制),辅以双光子钙成像与免疫组化;LLM 作为元控制器自动生成完整实验协议。但边界必须原样保留:这是纯前瞻框架,未报告任何类器官学习实验结果;框架成立以类器官至少 60-90 天体外成熟、采用引导式培养协议为条件;作者自述生物基质变异性与有限寿命使可重复性成为核心挑战,当前 MEA(多电极阵列)信息带宽比生物神经系统低多个数量级,可能约束可学习世界模型的复杂度。

与蓝图互补的是小样本实测:[另一项研究](https://arxiv.org/abs/2607.28068)在三个皮层类器官的纵向高密度 MEA 记录中发现,诱发反应是快速、近同步的全网络爆发而非向外传播波,峰潜伏期与距离无可测斜率——传播与整合深度类图指标不适用于此类数据。重复日刺激使响应网络空间持续收缩:到第七天,两个重复刺激类器官的响应电极占比分别只剩 9.5% 与 12%,而同龄首次刺激的对照类器官响应覆盖阵列 93%,证明这种抑郁由刺激历史而非发育成熟驱动。其边界必须保留:设计仅含两个重复刺激类器官加一个对照,属对照支持的观察而非群体级统计主张;每会话仅 10 次试验,功能图指标在该条件下不可靠,作者因此不报告边级图统计;跨天抑郁反映会话内耐力退化而非响应容量丧失的解释,是作者标注的小样本假说;该研究也不能裁决其他刺激协议下类器官是否支持结构化多跳计算。

预测编码的进展在算法层:[Bayesian Reflex](https://arxiv.org/abs/2608.00492) 把椭球分解采样、带收敛保证的递归高斯过程、导数感知贝叶斯优化组合起来,声称使预测编码首次获得可扩展且精确的算法引擎;其转引的旗舰应用把素数序列建模为非齐次泊松过程做序贯贝叶斯更新,发现了 259 个超过 1.4 亿的新素数(含 184 个强 Mersenne 素数候选)。但其自我限定同样重要:精确采样框架当前只扩展到数千维,对数十亿参数的基础模型需要稀疏化或层次化等进一步创新;作者明言大脑不太可能实现精确矩阵求逆,该框架应被视为数学蓝图而非字面的神经生物学模型——其"类脑"成分是计算原理层面的对应,不是实现层面的等同。预测编码主流实现依赖的拉普拉斯近似对预测函数线性化并假设高斯后验,损失精确性与多峰捕捉能力,这个长期计算瓶颈也只在中小规模上被暂时绕开。

## 结论:证据强度的分层与开放问题

把三条主线放回同一把尺子上,分层清晰。第一层,转换式脉冲大模型的规模与基准恢复已被端到端验证,包括训练稳定性与常规硬件上的推理加速;但神经形态优势本身未经实测。第二层,机制改进的增益以零点几到一个点计,且每项收益都附带条件——tdBN 归一化假设、大量超参数搜索、非局部训练,或者瓶颈在数据而非参数。第三层,能耗主张几乎全部停留在折算与仿真;唯一有芯片实测的 SpiNNaker2 给出的答案是"与业界现有水平相当"(附 SRAM 驻留条件),且附带 18 倍能耗对 8 倍延迟的交换。第四层,类器官智能与预测编码分别是零实验结果的课程蓝图与自我定位为数学蓝图的算法框架。开放问题也由证据直接给出:大模型路线尚未在 DVS 等神经形态任务上验证;SpikeVLA 与 N-MDLM 的硬件验证被列为未来工作;在线学习与内存受限硬件的矛盾、灾难性遗忘(实时振荡重放仍是推测性假说)、任务级能耗评测标准,以及类器官的可重复性与信息带宽约束,一年内都没有解法。中心判断的可证伪条件由此明确:若未来出现真实神经形态硬件上、按任务级口径实测的大模型级能耗优势,"能效是纸面的"这一层判断即失效;若从零训练路线在数 B 规模上仍保持数据正响应并追平全精度基座,机制层与大模型层的分层也需要重画。

## 研究边界声明

本备忘录引用的结论须与以下边界同读。折算或仿真而非实测:SDLLM 与 NASN 的能耗为折算,BiSpikCLM 为 45nm 芯片仿真,Sequence-SOD 的 116 倍为 45nm 折算且评估在 GPU 仿真完成,N-MDLM 止于仿真分析,NLSpiking 的延迟结论来自执行模型分析,SpikeVLA 验证止于仿真与 GPU。综合估计而非流片:SpikeMLLM 的加速器数字来自 SMIC 28nm 综合与周期级仿真,GPU 对照仅 A800 FP16 批大小 1。芯片或 FPGA 实测:仅 SpiNNaker2(能效、DVFS、EGRU 能耗)与 AIGOR(FPGA 复现与吞吐),分别附带 SRAM 驻留、2 ms 定点精度与 2 FPGA 上限条件。小样本、单次与外推:类器官刺激研究为两个重复刺激类器官加一个对照,跨天机制解释是作者标注的小样本假说;QIF 的 ImageNet 结果为单次试验;SpikingBrain 的 4M token 加速为拟合曲线外推;Sequence-SOD 的 40Hz 为依赖输入数据的理论值。尚未验证:大模型路线未在 DVS 等神经形态任务上验证;NeuronSpark 无定量基准与 Transformer 基线、层间信号为浮点泄漏电流;类器官课程论文未报告任何实验结果。

## References

1. [SpikingBrain: Spiking Brain-inspired Large Models](https://arxiv.org/abs/2509.05276)
2. [Spike-driven Large Language Model (SDLLM)](https://arxiv.org/abs/2604.16475)
3. [SpikeMLLM: Spike-based Multimodal Large Language Models via Modality-Specific Temporal Scales and Temporal Compression](https://arxiv.org/abs/2604.18610)
4. [BiSpikCLM: A Spiking Language Model integrating Softmax-Free Spiking Attention and Spike-Aware Alignment Distillation](https://arxiv.org/abs/2605.13859)
5. [Plug-and-Play Spiking Operators: Breaking the Nonlinearity Bottleneck in Spiking Transformers (NLSpiking)](https://arxiv.org/abs/2605.20289)
6. [NeuronSpark: A Spiking Neural Network Language Model with Selective State Space Dynamics](https://arxiv.org/abs/2603.16148)
7. [Discretized Quadratic Integrate-and-Fire Neuron Model for Deep Spiking Neural Networks](https://arxiv.org/abs/2510.05168)
8. [Adaptive Spiking Neurons for Vision and Language Modeling (NASN)](https://arxiv.org/abs/2604.12365)
9. [Scalable Training of Continuous-Time Spiking Neural Networks with Differentiable Spike-Time Discretization (DSTD)](https://arxiv.org/abs/2607.14672)
10. [NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework](https://arxiv.org/abs/2605.15058)
11. [The brain as a blueprint: a survey of brain-inspired approaches to learning in artificial intelligence](https://arxiv.org/abs/2511.04455)
12. [The SpiNNaker2 chip: a many-core platform for flexible and scalable brain-inspired computing](https://arxiv.org/abs/2607.24396)
13. [AIGOR: A Modular, Event-Driven Neuromorphic Architecture for Configurable SNN Inference](https://arxiv.org/abs/2607.03191)
14. [Beyond Peak TOPS/W: A System-Level Perspective on Hybrid Digital, Analogue and Neuromorphic Computing](https://arxiv.org/abs/2608.03514)
15. [Neuromorphic Diffusion Language Models: Addressing Compute and Memory Bottlenecks via Sparsity and Block Denoising (N-MDLM)](https://arxiv.org/abs/2607.24841)
16. [SpikeVLA: Vision-Language-Action Models with Spiking Neural Networks](https://arxiv.org/abs/2606.27807)
17. [Sequence-SOD: Bio-inspired Sequence-aware Spiking Object Detection for Event Cameras](https://arxiv.org/abs/2607.26703)
18. [The Physical Basis of Prediction: World Model Formation in Neural Organoids via an LLM-Generated Curriculum](https://arxiv.org/abs/2509.04633)
19. [Stimulus-Evoked Network Dynamics in Human Cortical Organoids: From a Graph-Computational Framework to Repeated-Stimulation Depression](https://arxiv.org/abs/2607.28068)
20. [The Bayesian Reflex: A Predictive Coding Engine for Artificial Intelligence](https://arxiv.org/abs/2608.00492)