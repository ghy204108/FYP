# Undergraduate FYP Proposal Form - 中文工作草稿

> 使用说明：课程说明 PDF 明确要求学生不得直接提交 AI 生成文本。本文件只能作为结构化修改草稿和写作参考；正式提交前请根据你的真实理解、导师意见、实验条件和学校要求重写、核对引用，并翻译为正式英文版本。

## Section I: Student's Information

| Item | Information |
| --- | --- |
| Full Name | [请填写姓名] |
| Student ID | [请填写学号] |
| Mobile | [请填写电话] |
| Email ID | [请填写邮箱] |
| Programme | Software Engineering (SWE) [请确认] |

## Section II: Supervisor's Information

| Item | Information |
| --- | --- |
| Approval Status | Proposed / Contacted / Approved / None [请确认] |
| Full Name | [请填写导师姓名] |
| Office Location | [请填写] |
| Office Extension | [请填写] |
| Email ID | [请填写] |

## Section III: Industry Information

| Item | Information |
| --- | --- |
| Approval Status | Not applicable |
| Company Name | Not applicable |
| Contact Person | Not applicable |
| Designation / Phone / Email | Not applicable |

## Section IV: Declaration by the Student

By signing this form, I confirm that I have read and will adhere to the Final Year Project Report/Thesis Guidelines of Xiamen University Malaysia as applicable to this application.

| Item | Information |
| --- | --- |
| Signature of Student | ____________________ |
| Date | ____________________ |

## Section V: Project Report / Thesis Supervisor Approval

| Item | Information |
| --- | --- |
| Name of Supervisor | [请填写] |
| Title / Position | [请填写] |
| Signature | ____________________ |
| Date | ____________________ |

# Section VI: Project Report / Thesis Information

## Title

**Label-wise Strategy Selection for Uncertain Labels in Imbalanced Multi-label Chest X-ray Classification**

中文题目：**面向类别不平衡多标签胸片分类的不确定标签逐标签策略选择研究**

## Commencement Date

June 2026 [请按学校实际 FYP 起始日期确认]

## Academic Year / Semester

Academic Year 2026/2027, Semester 1-2 [请确认]

## Introduction / Problem Statement

胸部 X 光片（Chest X-ray, CXR）分类通常属于多标签学习任务，因为一张胸片可能同时包含多个疾病或观察结果。Irvin et al. (2019) 发布的 CheXpert 是该领域的重要公开数据集之一，其标签由放射报告自动抽取，并显式包含 positive、negative、uncertain 和 blank 等状态。其中，uncertain labels 通常对应报告中的 possible、cannot exclude、questionable 等不确定表达；blank labels 则更谨慎地理解为未提及或缺失标签，而不应在未说明策略的情况下直接等同于 definite negative。Smit et al. (2020) 的 CheXbert 研究进一步说明，自动报告标注器的质量会影响 report-derived labels 的可靠性；Jain et al. (2021a) 则指出，report labels 与 image-level evidence 之间可能存在差异。因此，CheXpert 中的 uncertain labels 不只是简单噪声，也可能反映报告表达、标注规则和图像证据之间的不一致。

不确定标签处理策略（uncertain-label handling strategy）会直接影响 CheXpert-style CXR 分类模型的训练结果。Irvin et al. (2019) 在 CheXpert 原论文中比较了 U-Zero、U-One、U-Ignore、U-SelfTrained 和 U-MultiClass 等策略，并发现不同 pathology labels 中表现较优的处理方式并不一致。这一发现说明，不确定标签处理不应只依赖单一全局规则。然而，现有比较通常需要先分别训练基于不同 uncertain-label 处理策略的完整模型，再根据 validation performance 判断每个 label 更适合哪种策略。这种训练后选择方式能够得到经验结果，却较难解释 uncertain samples 为什么更接近 positive、negative 或 ambiguous，也难以在完整训练所有 strategy-specific models 之前提供可解释的前置推荐依据。

因此，本研究的核心 gap 是：在 imbalanced multi-label CXR classification 中，仍缺少一种用于 uncertain labels 的 label-wise uncertainty profiling 方法，能够在完整训练多个候选策略模型之前，对不同 pathology 的 uncertain samples 进行可解释分析，并为 uncertain-label strategy selection 提供 evidence-informed recommendation。仅统计每个 label 的 positive、negative 和 uncertain 数量，并不能判断 uncertain samples 在语义或模型预测空间中更接近 positive、negative 还是 ambiguous，因此需要进一步建立 uncertain samples 与 definite samples 之间的分布性证据。Holste et al. (2024) 关于 long-tailed CXR classification 的研究表明，胸片任务中的 rare labels 容易被整体指标掩盖；Saito and Rehmsmeier (2015) 也指出，在类别不平衡任务中，precision-recall based evaluation 往往比只看 ROC 更能反映少数类表现。这些发现说明，本研究需要采用 per-label、support-aware 和 PR-aware 的分析方式，而不是只依赖整体性能。初步数据审查也显示，不同 CheXpert labels 的 uncertainty burden 差异明显，例如部分 labels 的 uncertain proportion 远高于其他 labels，这进一步支持逐标签分析的必要性。

本研究将使用一个单次训练的 teacher model 作为辅助 profiling 的低成本 probe model，而不是把它视为最终诊断模型、ground truth source 或策略优劣的直接判定器。该 probe model 只用于提供 score-based evidence，帮助观察 uncertain samples 在模型预测空间中更接近 definite positive、definite negative，还是处于 ambiguous 区域。Cheng and Vasconcelos (2024) 说明 multi-label DNN calibration 需要专门关注，因此 probe scores 在本项目中只会与样本支持、分类表现和校准检查一起作为保守的推荐依据。基于上述问题，本项目旨在设计并评估一种轻量、可解释、可复现的 label-wise uncertainty profiling framework，用于在 CheXpert-style 多标签胸片分类中，为不同 pathology 的 uncertain-label handling strategy 提供训练前推荐依据。

## Aims and Objectives

本研究的总体目标是设计并评估一种面向 CheXpert-style 多标签胸片分类的逐标签不确定性画像框架。该框架将使用一个固定 teacher/probe model 为每个 label 生成 positive、negative 和 uncertain samples 的 score distributions，并结合分布相似度、效应量、重叠率、样本充分性和 score calibration 检查，为每个 label 推荐 U-One、U-Zero、U-Soft 或 U-Ignore 等处理策略。

本研究拟回答三个研究问题：

1. 不同 CheXpert labels 中的 uncertain samples 在 teacher-score distribution 上更接近 definite positive、definite negative，还是处于 ambiguous 区域？
2. 基于明确 decision rules 的 label-wise uncertainty profile 能否为 validation oracle 所选择的 per-label uncertain-label strategy 提供一致的前置推荐依据？
3. 与固定策略相比，profile-guided strategy 是否能在 held-out test set 上取得更稳定的 macro AUPRC、rare-label AUPRC 和 calibration 表现？

具体目标如下：

1. To analyze positive, negative, uncertain and missing label distributions in CheXpert, with emphasis on rare labels and high-uncertainty-burden labels.
2. To train a single imbalance-aware teacher/probe model and assess its label-wise classification performance, P/N separability, sample support and score calibration using AUPRC, P/N separability, minimum support, ECE and Brier score.
3. To design a reproducible label-wise uncertainty profiling algorithm using distribution distance, overlap ratio, median difference and non-parametric effect size.
4. To evaluate the profile-guided strategy against fixed uncertain-label strategies and a validation oracle upper bound using classification, calibration and strategy-recommendation metrics.

## Background Study / Literature Review

本研究的文献综述围绕一条主线展开：CheXpert-style CXR labels 由报告自动抽取而来，因此 uncertain labels 具有语义复杂性；已有研究已经证明不同 uncertain-label strategies 会影响模型表现，并且不同 pathology labels 可能偏好不同策略；然而，现有研究多依赖训练后的 empirical comparison，仍缺少一种在完整训练多个 strategy-specific models 之前，为 label-wise strategy selection 提供可解释证据的 profiling 机制。表 2.1 概括了各类文献之间的关系及其对本研究 gap 的支持。

| Theme | Key references | Synthesis for this study | Remaining limitation / gap |
| --- | --- | --- | --- |
| CheXpert uncertain-label strategies | Irvin et al. (2019); Pham et al. (2021) | 证明 uncertain-label handling 已被研究，且不同 pathology labels 可能需要不同策略。 | 主要通过训练后 validation performance 发现策略差异，对策略偏好的前置解释不足。 |
| Report-derived label discrepancy | Smit et al. (2020); Jain et al. (2021a, 2021b) | 解释 uncertain labels 的来源复杂性，说明 report labels 与 image evidence 之间可能不完全一致。 | 重点是 labeler quality 或 discrepancy analysis，不直接给出下游 strategy selection 规则。 |
| Noisy and label-wise CXR learning | Chen et al. (2020); Chen et al. (2023); Ye et al. (2026) | 支持 multi-label structure、report-derived noise 和 label-wise reliability 的重要性。 | 多数方法目标是 robust classifier 或 label correction，而非训练前的 strategy recommendation。 |
| Long-tailed and imbalanced evaluation | Holste et al. (2022, 2024); Lin et al. (2025); Wu et al. (2020); Ridnik et al. (2021); Saito & Rehmsmeier (2015) | 说明 rare labels、negative dominance 和 overall AUROC 掩盖问题会影响 strategy evaluation。 | 长尾研究通常不专门处理 uncertain-label strategy preference。 |
| Probe reliability and distribution evidence | Guo et al. (2017); Rajaraman et al. (2022); Cheng & Vasconcelos (2024); Rubner et al. (2000); Mann & Whitney (1947) | 支持 score-based profiling 需要同时考虑 discrimination、calibration、support 和 distribution comparison。 | 这些方法本身不能自动产生策略规则，需要被整合为可复查的 label-wise profiling framework。 |

### 2.2.1 Uncertain-label Strategies in CheXpert

CheXpert 将胸片多标签分类中的 uncertainty 问题具体化为一个可实验比较的训练选择。Irvin et al. (2019) 在发布包含 positive、negative、uncertain 和 blank labels 的大规模 CXR 数据集时，同时比较了 U-Zero、U-One、U-Ignore、U-SelfTrained 和 U-MultiClass 等 uncertain-label handling strategies。这里的策略差异并不是普通的数据清洗细节：U-Zero 假设 uncertain samples 更接近 negative，U-One 假设它们更接近 positive，U-Ignore 回避这类样本，self-training 和 multi-class 方案则尝试保留 uncertainty 本身。换言之，每一种策略都隐含了对 uncertain label 语义的判断。

真正有研究价值的地方在于，Irvin et al. (2019) 并没有给出一个对所有 pathology labels 都稳定最优的统一答案。某些 labels 可能从更积极地利用 uncertain samples 中受益，另一些 labels 则可能因为错误编码而受损。Pham et al. (2021) 采用 disease hierarchy 和 label smoothing 处理 uncertainty，提供了另一种思路：uncertainty 可以被软化建模，而不一定被强行压成 0 或 1。两类研究之间存在一个有用的张力：hard-label baselines 简单、可复现，却容易牺牲语义细节；soft 或 hierarchy-aware methods 更细腻，但引入了额外建模假设。现有结论多来自训练后的 performance comparison，尚不足以解释在训练前如何判断某个 label 更可能偏向哪一种策略。

### 2.2.2 Report-derived Labels and Image-label Discrepancy

CheXpert-style labels 的另一层复杂性来自其 report-derived nature。与人工直接查看图像后逐项标注不同，许多 CXR 数据集的标签来自放射报告抽取。Smit et al. (2020) 的 CheXbert 说明，改进自动报告标注器可以提升 report labels 的一致性和准确性；但 Jain et al. (2021a) 对 VisualCheXbert 的讨论又指出，报告标签与 image-level evidence 之间仍可能不一致。Jain et al. (2021b) 进一步显示，report labeler quality 会影响下游 CXR classifier。这里的关键矛盾是：更好的报告标注器可以减少文本抽取误差，却不能完全消除报告表达、图像证据和训练标签之间的错位。

这种错位使 uncertain labels 的含义变得不稳定。它们可能对应真实但表述谨慎的影像发现，也可能来自医生的保守措辞、自动规则对模糊短语的归类，或报告没有直接覆盖图像中可见的信息。Blank labels 同样不能被粗略等同为临床阴性；在模型训练中它们常被处理为未提及或非阳性样本，但这只是工程假设，不是医学真值。由此看，U-Zero、U-One、U-Soft 和 U-Ignore 不是四种等价编码，而是对 report-derived uncertainty 的四种解释路径。已有研究解释了标签来源的复杂性，却没有把这种复杂性进一步转化为 per-label training strategy 的选择依据。

### 2.2.3 Label-wise Reliability in Noisy CXR Learning

把 uncertain labels 视为 noisy labels 的一种形式是合理的，但 CXR 场景中的噪声并不符合许多通用 noisy-label learning 的简化假设。Chen et al. (2023) 的 BoMD 强调，report-derived noisy labels 出现在 multi-label setting 中，一个图像可能同时具有多个 finding，标签之间还会共现或相互影响。Chen et al. (2020) 的 label co-occurrence learning 从另一角度说明，CXR labels 不是完全独立的二元分类任务。若某个 uncertain label 被统一编码为 0 或 1，它影响的不只是该 label 的监督信号，也可能改变模型对相关 finding 的学习方向。

这类研究带来的启发并非“所有噪声都应被修正”，而是噪声处理需要注意 label-wise reliability。Ye et al. (2026) 讨论了低可靠标签和 tail classes 在鲁棒学习中的脆弱性，这一点与 uncertain-label strategy selection 直接相关：样本少、噪声高、共现关系复杂的 label 更容易被全局策略误伤。不过，鲁棒分类方法通常把重点放在提升最终模型表现，内部的纠错或重加权过程未必能解释某个 uncertain group 在语义上更接近 positive 还是 negative。换言之，robust learning 可以缓解噪声后果，却不必然回答训练前的策略选择问题。文献在这里留下的空间，是为每个 label 建立更明确的 reliability evidence，而不是仅依赖一个统一的噪声处理机制。

### 2.2.4 The Long-tail Challenge

长尾分布不是本项目的另一个独立研究目标，而是 uncertain-label strategy selection 必须面对的评价背景。Holste et al. (2022, 2024) 和 Lin et al. (2025) 表明，胸片多标签任务中常见 finding 与 rare findings 的样本量差异很大，rare labels 容易被 common labels 和大量 negatives 掩盖。Wu et al. (2020) 的 distribution-balanced loss 与 Ridnik et al. (2021) 的 asymmetric loss 也从一般 multi-label learning 角度说明，positive-negative imbalance 会影响优化方向。这些方法能改善长尾或不平衡训练，但它们处理的是 loss-level imbalance，并不直接说明 uncertain samples 应被看作阳性、阴性还是模糊样本。

在不确定标签语境中，长尾问题会放大策略选择的风险。对 positive support 很少的 pathology 而言，U-Zero 可能让本已稀缺的阳性信号进一步减少；U-One 可能提高召回但引入假阳性；U-Ignore 保守，却可能丢掉少数类最需要的训练信息；U-Soft 看似折中，但如果 uncertain samples 本身并不位于 positive 与 negative 之间，soft treatment 也可能只是把噪声平滑化。评价指标之间同样存在张力。整体 AUROC 可能因为大量 negative cases 而显得稳定，却无法充分反映 rare labels 的 precision-recall trade-off；Saito and Rehmsmeier (2015) 因此强调 PR curve 在不平衡任务中的价值。本研究后续比较 strategy-specific models 时，需要把 per-label AUPRC、macro AUPRC 和 rare-label AUPRC 放在核心位置，同时用 AUROC 作为补充，而不是让整体指标替代逐标签判断。

### 2.2.5 Teacher Reliability for Score-based Profiling

使用 teacher/probe model 进行 score-based profiling 有吸引力，也有风险。它的吸引力在于成本较低：在完整训练多个 strategy-specific models 之前，probe scores 可以先显示 uncertain samples 在分数空间中更接近 positive、negative，还是呈现中间或混合形态。但这种做法也容易被误用。如果把 teacher score 当作 pseudo-ground-truth，profiling 就会变成对探针模型偏差的再包装。因此，在本项目中，teacher/probe model 的角色应被限定为分布探针，而不是最终诊断模型或真值来源。

Calibration literature 正好揭示了这种限制。Guo et al. (2017) 指出现代深度网络可能出现 overconfidence 和 miscalibration；Rajaraman et al. (2022) 将这一问题放到 class-imbalanced medical image classification 中讨论，说明不平衡会影响概率解释；Cheng and Vasconcelos (2024) 进一步强调 multi-label calibration 与 multi-class calibration 并不等同。这里存在两个容易混淆的概念：AUPRC、P/N separability 和 minimum support 更偏向检查区分能力与样本支撑，ECE 和 Brier score 才更接近 calibration/reliability 检查。高 AUPRC 可以说明排序或区分能力较好，却不保证概率分数可靠；校准较好的模型也可能对某些 rare labels 缺少足够区分度。基于这种区分，probe evidence 应被分层使用：证据充分的 label 才进入明确推荐，证据不足的 label 应保留为保守类型，而不是被迫归入 U-Zero 或 U-One。

### 2.2.6 Distributional Evidence for Uncertainty Profiling

如果把 strategy preference 转化为训练前问题，核心就变成：uncertain samples 在可观测证据上更像哪一类样本。单纯报告 uncertain proportion 只能说明 burden 大小，不能说明方向性。Distribution comparison literature 可以补上这一层信息。Rubner et al. (2000) 的 Earth Mover's Distance 关注两个分布整体移动距离，适合衡量 uncertain distribution 与 positive 或 negative distribution 的接近程度；Mann and Whitney (1947) 的非参数检验不要求分数服从正态分布，适合处理 probe scores 常见的偏态、重叠或两端极化。与其把 uncertain label 当成一个固定类别，不如比较其 score distribution 与已知 positive/negative groups 之间的关系。

这里也存在方法层面的张力。显著性检验可以告诉研究者两个分布是否存在统计差异，但在 CheXpert 这类大样本数据中，p-value 很容易显著；相反，overlap ratio 或 effect size 更能反映差异是否有实际解释价值。Wasserstein distance 能捕捉整体位移，却可能忽略局部重叠；median difference 简洁直观，却不足以描述双峰或混合分布。基于这一限制，profiling 不适合依赖单一指标，而应组合 Wasserstein distance、overlap ratio、median difference、Mann-Whitney U test 和 effect size。若 uncertain samples 稳定靠近 positive group，可形成 U-One 或 soft-positive treatment 的证据；若靠近 negative group，则支持 U-Zero；若分布位于中间、高度重叠或证据方向不一致，则更适合 U-Soft、U-Ignore 或保守推荐。最终输出应是证据强度分层和可复查推荐，而非二元化的最佳策略断言。

这些文献共同形成了一条逐步收窄的研究脉络：CheXpert 证明 uncertain-label strategy 会影响模型表现；report-derived label 研究解释了 uncertainty 的语义来源为何复杂；noisy multi-label learning 和 long-tailed CXR literature 说明全局策略与整体指标都可能掩盖逐标签风险；calibration 与 distribution comparison 研究则为 score-based profiling 提供了必要工具。尚未被充分连接起来的是训练前解释机制：现有研究多能回答“哪种策略训练后表现更好”，但较少回答“某个 pathology label 在训练前为什么可能更偏向某种策略”。本项目的切入点正是将 probe score distribution、label-wise evidence check、calibration check 和 imbalance-aware evaluation 整合为可复查的 profiling framework，为 per-label uncertain-label strategy recommendation 提供依据。

## Research Methodology & Ethics

本研究采用定量、应用型的实验基准设计（quantitative applied benchmarking design），以 CheXpert 作为主要二手数据来源。研究重点是在同一数据集、相同划分和固定模型设置下，比较不同不确定标签处理策略，并评估一个逐标签的策略推荐方法。若计算资源不足，实验会预先收窄到正位片（frontal views）或部分核心标签。数据划分会按患者分离；训练集用于模型训练，验证集用于确定画像规则、阈值和 validation oracle，测试集只用于最终报告。

第一步是数据准备。本研究会整理图像路径、患者编号和标签矩阵，并区分 positive、negative、uncertain 和 blank 标签。基本统计包括每个标签的阳性比例、不确定比例和有效样本量，用来判断 rare labels 与高不确定标签。不同策略下的标签处理会提前固定：U-Zero 将 uncertain 视为 0，U-One 视为 1，U-Ignore 忽略该标签上的 uncertain 样本，U-Soft 使用固定 soft target。

第二步是训练一个教师/探针模型。为避免研究范围过大，模型结构不会作为主要比较对象；初步计划使用 ImageNet 预训练的 DenseNet-121。该模型优先采用 U-Ignore 训练，用来为每个标签生成 positive、negative 和 uncertain 样本的预测分数分布。探针模型会用验证集上的 AUPRC、阳性/阴性可分性和校准指标检查；证据不足的标签会保守处理。

核心方法是逐标签不确定性画像。对于每个标签，本研究会比较 uncertain 样本组与明确阳性、明确阴性样本组的分数分布，重点观察分布距离、重叠程度和效应量，而不是只看 uncertain 样本数量。若 uncertain 样本明显靠近阳性组，该标签倾向于 U-One；若更靠近阴性组，则倾向于 U-Zero；若两边高度重叠或探针证据不足，则倾向于 U-Soft 或 U-Ignore。探针模型只提供策略证据，不被视为医学真值。

最后，本研究会训练 profile-guided final model，并与 all U-Zero、all U-One、all U-Ignore 及资源允许时的 all U-Soft 比较。Validation oracle 指在训练并比较固定策略后，为每个标签从验证集表现最好的策略中选出参考答案；它代表训练后经验选择能达到的近似上限，用来衡量 profile-guided 方法在训练前推荐策略时能接近到什么程度。评价指标以 per-label AUPRC、macro AUPRC 和 rare-label AUPRC 为主，AUROC 作为辅助指标。F1-score、precision 和 recall 的阈值会在验证集上确定，不使用测试集调参。ECE 和 Brier score 用于辅助检查分数可靠性。伦理方面，本研究不收集新临床数据，也不把模型输出解释为临床诊断；所有结论只限于算法比较和 CheXpert 数据集内表现。

## Rationale and/or Timeliness / Potential Project Significance

本项目的研究价值来自三个方面。第一，它回应了 CheXpert-style 数据中的真实监督问题：uncertain labels 不是普通缺失值，也不是可以统一处理的随机噪声。通过逐标签分析，本研究能够解释不同 pathology labels 为什么可能适合不同策略。第二，本项目把长尾类别不平衡和 teacher reliability 纳入 uncertainty handling，而不是只比较整体 AUROC。这更符合医学影像分类中 rare-label failure 可能被平均指标掩盖的风险。第三，本研究的范围适合本科 FYP：它不训练大型基础模型，也不进行真实临床部署，而是集中在一个公开数据集、一个 teacher model、四种固定策略和一个 profile-guided strategy 上，能够形成清晰、可复现的实验产出。

## Expected Outcomes and/or Concluding Remarks

本研究预期产生四类具体成果。第一，实现一个可复现的 CheXpert 数据准备与标签策略生成模块，包括 patient-level data split、label matrix construction、P/N/U mask generation，以及 U-Zero、U-One、U-Ignore 和 U-Soft target generation。这一成果不是简单分析报告，而是后续模型训练可直接使用的实验基础。第二，实现一个 teacher-assisted label-wise uncertainty profiling pipeline，输出每个 label 的 distribution features、reliability indicators 和 Type A-D profile assignment。第三，构建并训练一个 profile-guided final model，使不同 labels 根据 profile 自动采用不同 uncertain-label handling strategies。第四，完成 profile-guided strategy 与固定策略的实验比较，报告 macro AUPRC、rare-label AUPRC、calibration metrics、oracle agreement 和 regret，并总结一个可复现的 strategy selection guideline，说明在什么条件下 uncertain samples 更适合被处理为 positive、negative、soft target 或 ignored。

预期结果不是证明 profile-guided strategy 在所有 labels 上都超过 validation oracle，因为 oracle 本身代表训练后经验选择的参考上限。更现实的目标是：profile-guided strategy 能在不完全依赖穷举训练所有候选 strategy-specific models 的情况下，接近 oracle 的部分选择结果，并在 rare labels 或 high-uncertainty-burden labels 上提供比统一固定策略更稳定的结果。如果实验结果不支持该假设，本研究仍可通过 per-label analysis 说明哪些标签和条件下 teacher-score profiling 不可靠，从而形成有价值的 negative findings 和 future work。

## Gantt Chart

| Activity | Jun 2026 | Jul 2026 | Aug 2026 | Sep 2026 | Oct 2026 | Nov 2026 | Dec 2026 | Jan 2027 | Feb 2027 | Mar 2027 | Apr 2027 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Proposal refinement and supervisor confirmation | X |  |  |  |  |  |  |  |  |  |  |
| Core literature review and synthesis matrix | X | X | X |  |  |  |  |  |  |  |  |
| CheXpert access, dataset audit and label statistics |  | X | X |  |  |  |  |  |  |  |  |
| Data preprocessing and patient-level split design |  |  | X | X |  |  |  |  |  |  |  |
| Teacher model and fixed-strategy baseline implementation |  |  |  | X | X |  |  |  |  |  |  |
| Teacher reliability and calibration analysis |  |  |  |  | X | X |  |  |  |  |  |
| Label-wise uncertainty profiling algorithm |  |  |  |  |  | X | X |  |  |  |  |
| Profile-guided final model and validation oracle comparison |  |  |  |  |  |  | X | X | X |  |  |
| Result analysis, error analysis and sensitivity checks |  |  |  |  |  |  |  |  | X | X |  |
| Final thesis writing, proofreading and presentation preparation |  |  |  |  |  |  |  |  |  | X | X |

## Resources

| Resource type | Required resources |
| --- | --- |
| Dataset | CheXpert dataset and existing local manifests; optional frontal-view subset for resource control. |
| Software | Python, PyTorch, torchvision/timm, scikit-learn, pandas, NumPy, SciPy, matplotlib/seaborn. |
| Hardware | GPU workstation or cloud GPU; sufficient storage for CheXpert images and intermediate checkpoints. |
| References | Core papers on CheXpert, report labelers, CXR long-tail learning, multi-label imbalance, calibration and distribution comparison. |
| Supervision | Supervisor guidance on scope, evaluation design, ethical requirements and final title. |
| Risk control | Patient-level split checking, fixed random seed where feasible, experiment logging, versioned configuration files. |

## Bibliography or Key References

Chen, B., Li, J., Lu, G., Yu, H., & Zhang, D. (2020). Label co-occurrence learning with graph convolutional networks for multi-label chest X-ray image classification. *IEEE Journal of Biomedical and Health Informatics, 24*(8), 2292-2302.

Chen, Y., Liu, F., Wang, H., Wang, C., Liu, Y., Tian, Y., & Carneiro, G. (2023). BoMD: Bag of multi-label descriptors for noisy chest X-ray classification. *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 21284-21295.

Cheng, J., & Vasconcelos, N. (2024). Towards calibrated multi-label deep neural networks. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 27589-27599.

Cui, Y., Jia, M., Lin, T. Y., Song, Y., & Belongie, S. (2019). Class-balanced loss based on effective number of samples. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 9268-9277.

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *Proceedings of the International Conference on Machine Learning*, 1321-1330.

Holste, G., Wang, S., Jiang, Z., Shen, T. C., Shih, G., Summers, R. M., Peng, Y., & Wang, Z. (2022). Long-tailed classification of thorax diseases on chest X-ray: A new benchmark study. *MICCAI Workshop*. [publication details to verify]

Holste, G., Zhou, Y., Wang, S., Jaiswal, A., Lin, M., et al. (2024). Towards long-tailed, multi-label disease classification from chest X-ray: Overview of the CXR-LT challenge. *Medical Image Analysis*. [volume/pages to verify]

Irvin, J., Rajpurkar, P., Ko, M., Yu, Y., Ciurea-Ilcus, S., Chute, C., Marklund, H., Haghgoo, B., Ball, R., Shpanskaya, K., Seekins, J., Mong, D. A., Halabi, S. S., Sandberg, J. K., Jones, R., Larson, D. B., Langlotz, C. P., Patel, B. N., Lungren, M. P., & Ng, A. Y. (2019). CheXpert: A large chest radiograph dataset with uncertainty labels and expert comparison. *Proceedings of the AAAI Conference on Artificial Intelligence, 33*(01), 590-597.

Jain, S., Agrawal, A., Saporta, A., Truong, S. Q. H., Duong, D. N., Bui, T., Chambon, P., Zhang, Y., Lungren, M. P., Ng, A. Y., Langlotz, C. P., & Rajpurkar, P. (2021a). VisualCheXbert: Addressing the discrepancy between radiology report labels and image labels. *Proceedings of the ACM Conference on Health, Inference, and Learning*. [publication details to verify]

Jain, S., Agrawal, A., Saporta, A., Truong, S. Q. H., Duong, D. N., Bui, T., Chambon, P., Zhang, Y., Lungren, M. P., Ng, A. Y., Langlotz, C. P., & Rajpurkar, P. (2021b). Effect of radiology report labeler quality on deep learning models for chest X-ray classification. *arXiv preprint arXiv:2104.00793*.

Lin, C., Holste, G., Zhou, Y., Wang, S., et al. (2025). CXR-LT 2024: A MICCAI challenge on long-tailed, multi-label, and zero-shot disease classification from chest X-ray. *arXiv preprint arXiv:2506.07984*. [publication details to verify]

Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. *The Annals of Mathematical Statistics, 18*(1), 50-60.

Pham, H. H., Le, T. T., Tran, D. Q., Ngo, D. T., & Nguyen, H. Q. (2021). Interpreting chest X-rays via CNNs that exploit hierarchical disease dependencies and uncertainty labels. *Neurocomputing, 437*, 186-194.

Rajaraman, S., Ganesan, P., & Antani, S. (2022). Deep learning model calibration for improving performance in class-imbalanced medical image classification tasks. *PLOS ONE, 17*(1), e0262838.

Ridnik, T., Ben-Baruch, E., Zamir, N., Noy, A., Friedman, I., Protter, M., & Zelnik-Manor, L. (2021). Asymmetric loss for multi-label classification. *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 82-91.

Rubner, Y., Tomasi, C., & Guibas, L. (2000). The Earth Mover's Distance as a metric for image retrieval. *International Journal of Computer Vision, 40*(2), 99-121.

Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE, 10*(3), e0118432.

Smit, A., Jain, S., Rajpurkar, P., Pareek, A., Ng, A. Y., & Lungren, M. P. (2020). Combining automatic labelers and expert annotations for accurate radiology report labeling using BERT. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing*, 1500-1519.

Wu, T., Huang, Q., Liu, Z., Wang, Y., & Lin, D. (2020). Distribution-balanced loss for multi-label classification in long-tailed datasets. *Proceedings of the European Conference on Computer Vision*, 162-178.

Ye, X., et al. (2026). Label-wise reliability-aware classifier for robust chest X-ray multi-label classification. *Expert Systems with Applications*. [full author list, volume and pages to verify]

# Appendix A: Literature Review Synthesis Matrix

| Paper | Main focus | Dataset / context | Relevance to this FYP | Limitation to note |
| --- | --- | --- | --- | --- |
| Irvin et al. (2019) | CheXpert dataset and uncertain-label strategies | CheXpert | Core dataset and strategy baseline. | Strategy preference is mainly found through post-training comparison. |
| Pham et al. (2021) | Hierarchical dependencies and uncertainty labels | CheXpert | Shows soft/uncertainty-aware CXR training already exists. | Not focused on pre-training strategy prediction. |
| Smit et al. (2020) | Radiology report labeling using BERT | CheXpert reports | Supports report-derived label quality issue. | Does not solve downstream strategy mapping. |
| Jain et al. (2021a) | Report-label and image-label discrepancy | CXR labels | Supports semantic gap between reports and image evidence. | Publication details should be checked before final submission. |
| Jain et al. (2021b) | Report labeler quality and downstream classifier | CXR datasets | Supports labeler-quality impact on CXR models. | Mainly evaluates labeler quality, not strategy selection. |
| Chen et al. (2023) | Noisy multi-label CXR classification | CXR data | Shows report-derived noisy labels require dedicated methods. | More about robust learning than explicit U-strategy mapping. |
| Ye et al. (2026) | Label-wise reliability-aware CXR classifier | ChestX-ray14, CheXpert, PadChest [to verify] | Supports label-wise reliability and tail-class vulnerability. | New paper; exact bibliographic details need confirmation. |
| Holste et al. (2022, 2024) | Long-tailed multi-label CXR | CXR-LT | Supports rare-label and long-tail evaluation. | Not focused on uncertain labels. |
| Ridnik et al. (2021) | Asymmetric loss for multi-label imbalance | General multi-label datasets | Supports imbalance-aware teacher training. | General vision method, needs CXR-specific evaluation. |
| Guo et al. (2017) | Neural network calibration | General image classification | Supports ECE and reliability discussion. | Not medical or multi-label specific. |
| Cheng & Vasconcelos (2024) | Multi-label DNN calibration | Multi-label classification | Direct support for multi-label calibration concern. | Not specific to CheXpert uncertain labels. |
| Saito & Rehmsmeier (2015) | PR curve vs ROC under imbalance | Binary imbalance evaluation | Supports AUPRC for rare-label analysis. | General methodological paper. |
| Rubner et al. (2000) | Earth Mover's Distance | Distribution/image retrieval | Supports distribution distance for score profiles. | Needs adaptation from image retrieval to teacher-score distributions. |
| Mann & Whitney (1947) | Non-parametric distribution comparison | Statistics | Supports non-normal score distribution comparison. | p-value should not be used alone for large datasets. |
