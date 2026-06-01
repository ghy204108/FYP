<!-- Optimized from FYP_Proposal_CN_Labelwise_Uncertainty_Profiling_Revised_Gap.md. -->

THESIS PROPOSAL

面向类别不平衡多标签胸片分类的逐标签不确定性画像与处理策略选择研究

Label-wise Uncertainty Profiling for Uncertain-label Strategy Selection in Imbalanced Multi-label Chest X-ray Classification

| Student Name | [请填写姓名] |
| --- | --- |
| Student ID | [请填写学号] |
| Programme | Final Year Project / Computer Science |
| Supervisor | [请填写导师姓名] |
| Submission Date | May 2026 |

APRIL 2025 TEMPLATE STRUCTURE ADAPTED FOR CHINESE FYP PROPOSAL

# CHAPTER 1
INTRODUCTION

## 1.1 Introduction

胸部X光片（Chest X-ray, CXR）是临床筛查、急诊评估和住院随访中最常见的医学影像之一。CheXpert等大规模公开数据集推动了多标签胸片分类模型的发展，使深度学习模型能够同时预测多个观察结果或疾病标签（Irvin et al., 2019）。这类数据集的监督信号通常来自放射报告自动抽取流程，因此会受到报告措辞和自动标注器规则的影响。放射报告中常见的possible、cannot exclude、questionable等表达会被编码为uncertain labels。因此，训练标签包含positive、negative、uncertain和missing等状态，具有比二元0/1 ground truth更复杂的监督结构。

已有研究已经证明，不确定标签的处理方式会显著影响模型表现。CheXpert原论文比较了U-Zero、U-One、U-Ignore、U-SelfTrained和U-MultiClass等策略，并发现不同pathology对策略的偏好并不一致（Irvin et al., 2019）。这说明统一地把所有uncertain labels当作0、1或忽略，都可能对某些标签造成系统性偏差。与此同时，CheXbert、VisualCheXbert和report labeler quality相关研究进一步指出，report-derived labels与image-level evidence之间存在差异，自动报告标注器的误差也会传递到下游图像分类模型中（Smit et al., 2020; Jain et al., 2021a; Jain et al., 2021b）。

基于这些发现，本研究将问题进一步聚焦到策略选择机制本身：在训练所有候选final strategy models之前，是否可以利用一个teacher model为每个label建立可解释的uncertainty profile，并据此预测该label更适合采用U-One、U-Zero、U-Soft或U-Ignore等处理方式。该思路将uncertain-label handling从统一标签编码推进到逐标签的分布关系、长尾风险和teacher reliability分析。

## 1.2 Problem Background

CheXpert-style胸片分类任务具有三个相互交织的困难。第一，任务本身是multi-label classification，一张胸片可能同时对应多个观察结果。不同疾病标签之间还存在共现、层级或互斥关系，例如心影增大、肺水肿和胸腔积液在临床语义上具有相关性（Chen et al., 2020; Pham et al., 2021）。因此，某个label的不确定性处理可能影响模型学习其他相关label的特征。

第二，uncertain labels具有复杂的文本来源和语义来源。CheXpert通过规则系统从放射报告中抽取positive、negative和uncertain mentions，但这些report-derived labels并不总是等同于图像层面的确定证据（Irvin et al., 2019）。CheXbert说明更强的NLP模型可以改进报告标注质量，VisualCheXbert则进一步强调report labels和image labels之间存在discrepancy（Smit et al., 2020; Jain et al., 2021a）。因此，某个uncertain label可能反映了真实但不够明确的影像表现，也可能受到放射科医生谨慎措辞、报告上下文、自动标注器误差或疾病边界模糊的影响。这种来源差异使得uncertain samples不宜被简单地统一解释，而需要在具体label层面分析其更接近positive、negative还是ambiguous distribution。

第三，胸片标签分布具有明显的类别不平衡和长尾特征。CXR-LT和LongTailCXR研究表明，rare findings在大规模CXR数据集中占比很低，容易被common labels和大量negative labels掩盖（Holste et al., 2022; Holste et al., 2024; Lin et al., 2025）。在这种场景下，AUROC可能掩盖罕见标签的失败，而AUPRC、per-label analysis和rare-label performance更能反映不平衡任务中的实际风险（Saito & Rehmsmeier, 2015）。如果teacher model本身在rare labels上表现不可靠，直接使用teacher probability替代uncertain labels可能会把teacher bias写入final model。

这些背景共同指向一个核心需求：uncertain-label strategy selection需要从全局规则转向label-wise analysis。为此，本研究将分别分析每个label的positive、negative和uncertain样本分布，并在策略映射之前检查teacher model对该label的区分能力和校准可靠性。

## 1.3 Research Gap

现有文献已经提供了本研究的直接起点。CheXpert证明不同pathology可能适合不同的不确定标签处理策略；Pham et al. (2021)说明soft label和层级依赖可以用于不确定标签建模；BoMD和label-wise reliability-aware研究进一步关注report-derived noisy labels和逐标签可靠性问题（Chen et al., 2023; Ye et al., 2026）。在此基础上，本研究的gap集中于策略选择的前置解释机制：现有策略选择通常仍依赖训练后对多个final strategy models的经验比较，而利用单一teacher model提前预测label-wise uncertain-label strategy的机制仍不充分。

具体而言，现有研究仍留下三个不足。第一，候选策略通常需要分别训练final model并在validation set上比较表现，训练成本会随策略数量增加而上升。第二，训练后的最优策略只能说明“哪个策略得分更高”，但较难解释uncertain samples在预测分布上更接近definite positive、definite negative还是处于ambiguous区间。第三，策略选择过程对teacher reliability的处理仍不够明确，尤其在rare labels上，teacher probability如果未经可靠性检查，可能成为新的噪声来源（Guo et al., 2017; Rajaraman et al., 2022; Cheng & Vasconcelos, 2024）。

因此，本研究的research gap可以表述为：在CheXpert-style imbalanced multi-label CXR classification中，现有研究仍需要一种可解释、可复现的label-wise uncertainty profiling框架，以在训练所有候选final strategy models之前，利用单一teacher model的score distributions、分布相似度、效应量和teacher reliability指标，为每个label预测较合理的uncertain-label handling strategy。该gap聚焦于uncertain-label strategy selection，而report-derived label discrepancy、long-tailed imbalance和calibration作为该问题的关键背景与约束条件。

## 1.4 Aims and Objectives

本研究的总体目标是设计并评估一种面向类别不平衡多标签胸片分类的逐标签不确定性画像框架。该框架以CheXpert为唯一主实验数据集，使用一个固定backbone和一个teacher model生成每个label下positive、negative和uncertain样本的score distributions，并结合分布距离、效应量、重叠率和teacher reliability指标，为每个label选择更合适的不确定标签处理策略。

本研究拟回答以下研究问题：

RQ1：不同CheXpert labels中的uncertain samples在teacher-score distribution上是否更接近definite positive、definite negative或ambiguous区域？

RQ2：基于明确decision rules的label-wise uncertainty profile能否预测validation oracle所选择的per-label uncertain-label strategy？

RQ3：与固定策略相比，profile-guided strategy在held-out test set上的macro AUPRC、rare-label AUPRC和calibration表现是否更稳定？

具体研究目标如下：

1. To analyze the distribution of positive, negative, uncertain and missing labels in CheXpert, and identify rare labels and high-uncertainty-burden labels.

2. To train and validate a single teacher model for extracting label-wise score distributions, with reliability checks based on AUPRC, P/N separability, ECE, Brier score and minimum support.

3. To design a reproducible label-wise uncertainty profiling algorithm using Wasserstein distance, overlap ratio, median difference, Mann-Whitney U effect size and pre-defined decision rules to classify labels into positive-like, negative-like, ambiguous or unreliable uncertainty types.

4. To evaluate the profile-guided strategy against fixed uncertain-label strategies and validation oracle upper bound using classification, calibration and strategy-prediction metrics.

# CHAPTER 2
LITERATURE REVIEW

## 2.1 Introduction

本章的文献综述按照研究逻辑链组织。已有文献可分为六类：第一类是CheXpert-style report-derived uncertain labels，为本研究提供数据和问题起点；第二类是report labeler和image-label discrepancy，说明标签不确定性具有语义和标注来源；第三类是noisy multi-label CXR learning和逐标签可靠性，提供近邻方法；第四类是long-tailed multi-label classification，说明rare labels需要单独评价；第五类是calibration和teacher reliability，强调概率输出需要经过可靠性检验；第六类是分布距离、效应量和非参数统计检验，为uncertainty profile的构建提供方法学支撑。

这些文献共同覆盖了数据集、标签不确定性、报告标注差异、长尾分布、类别不平衡损失、校准、噪声多标签学习和分布比较方法。为了保持proposal范围可控，本研究将CheXpert作为唯一主实验数据集，并将外部数据集验证保留为future work。表2.1将核心文献按照“对本研究的功能”进行综合。

表2.1  核心文献功能矩阵

| 文献主题 | 代表文献 | 对本研究的支撑 | 对gap的启示 |
| --- | --- | --- | --- |
| CheXpert uncertain labels | Irvin et al. (2019) | 提供CheXpert数据集、14个观察标签和U-Zero/U-One/U-Ignore/U-SelfTrained等策略。 | 不同label偏好不同策略已被发现；本研究进一步关注策略偏好的解释与预测。 |
| Report-derived label discrepancy | Smit et al. (2020); Jain et al. (2021a, 2021b) | 说明报告标注器质量、报告语义和图像证据之间存在差异。 | uncertain label具有报告来源和图像证据之间的语义差异，需要结合预测分布进行解释。 |
| Noisy multi-label CXR learning | Chen et al. (2023); Ye et al. (2026) | 说明CXR多标签噪声学习需要逐标签或医学知识感知方法。 | 近邻研究偏向鲁棒分类或重标注；本研究聚焦策略选择前的profile inference。 |
| Label dependency | Chen et al. (2020); Pham et al. (2021) | 说明CXR labels存在共现和层级关系，soft/平滑处理已被研究。 | 相关研究提示，本研究的贡献重点应落在label-wise strategy selection及其解释机制。 |
| Long-tailed CXR | Holste et al. (2022, 2024); Lin et al. (2025) | 证明胸片疾病标签长尾明显，rare findings需要专门评价。 | profile和evaluation必须报告per-label和rare-label表现。 |
| Imbalance-aware learning | Cui et al. (2019); Wu et al. (2020); Ridnik et al. (2021) | 提供class-balanced、distribution-balanced和asymmetric loss等teacher训练候选。 | teacher若不处理不平衡，其profile可能偏向多数类和easy negatives。 |
| Calibration/reliability | Guo et al. (2017); Rajaraman et al. (2022); Cheng & Vasconcelos (2024) | 支撑ECE、Brier score和multi-label calibration检查。 | teacher probability需要经过可靠性检查；Type D/unreliable机制可降低偏差传递风险。 |
| Imbalanced evaluation | Saito & Rehmsmeier (2015) | 支撑AUPRC比AUROC更适合不平衡分类解释。 | final evaluation应重点报告macro/rare-label AUPRC，并结合AUROC进行完整评价。 |
| Distribution/statistical profiling | Mann & Whitney (1947); Rubner et al. (2000); Damodaran et al. (2018) | 支撑非参数检验、Wasserstein/EMD和分布比较思想。 | profile应结合分布形状、效应量、重叠率和中心趋势，以避免在大样本下只依赖p-value。 |

## 2.2 Literature Review

### 2.2.1 Uncertain-label Strategies in CheXpert

CheXpert为本研究提供了最直接的数据集与问题基础，因为它显式地将report-derived labels表示为positive、negative、uncertain和blank状态。Irvin et al. (2019)不仅发布了CheXpert数据集，也系统比较了U-Zero、U-One、U-Ignore和self-training等uncertain-label strategies。该研究的重要发现是，不同pathology对uncertainty handling的偏好并不一致：部分标签在把uncertain samples视为positive时表现更好，另一些标签则可能更适合其他处理方式。这一结果说明uncertain-label handling具有label-wise差异，也使CheXpert成为研究逐标签策略选择的合适起点。

不过，CheXpert原有策略比较主要依赖训练后validation performance来判断不同策略的效果。它能够显示“不同label可能需要不同策略”，但较少解释uncertain samples为什么在某些label上更接近positive、negative或ambiguous，也没有提供一种在训练所有候选final strategy models之前预测per-label strategy的机制。因此，本研究不是重复比较CheXpert中的固定策略，而是进一步追问这种label-wise strategy preference能否通过teacher-score distributions被解释和预测。要回答这一问题，首先需要理解CheXpert标签为什么会产生语义复杂的uncertainty。

### 2.2.2 Report-derived Labels and Image-label Discrepancy

uncertain label的语义复杂性很大程度上来自其report-derived nature。CheXpert中的标签主要从放射报告中自动抽取，而不是直接来自图像层面的人工标注。Smit et al. (2020)通过CheXbert说明，使用更强的NLP模型和专家标注可以改进report label质量，这表明自动标签抽取本身就是影响下游任务的重要方法因素。Jain et al. (2021a)进一步指出report labels和image labels之间可能存在discrepancy，Jain et al. (2021b)则显示report labeler质量会影响下游CXR classifier。综合来看，report-derived uncertainty可能来自放射科医生谨慎措辞、报告上下文、NLP labeler误差，也可能来自真实但不够明确的影像证据。

这些研究解释了uncertain labels为什么不应被简单视为统一含义的模糊标签，但它们的主要目标是改进或评估报告标注质量，而不是为下游图像分类中的U-Zero、U-One、U-Soft或U-Ignore选择提供规则。因此，report-label discrepancy文献能够说明uncertainty来源复杂，却不能直接回答每个label的uncertain samples应如何参与multi-label CXR training。这个不足将问题自然推向更接近模型训练的noisy-label CXR learning文献。

### 2.2.3 Label-wise Reliability in Noisy CXR Learning

近期noisy-label CXR研究已经从通用单标签噪声假设转向更贴合胸片任务的multi-label setting。Chen et al. (2023)提出BoMD用于report-derived noisy multi-label CXR classification，说明胸片标签噪声需要结合多标签结构进行处理。Ye et al. (2026)进一步强调label-wise reliability，尤其指出tail classes可能在粗粒度噪声检测或修正中受到损害。这些研究的重要贡献在于，它们把CXR噪声标签问题从统一噪声假设推进到label-wise reliability视角。

然而，BoMD和label-wise reliability-aware方法的主要目标仍然是学习更鲁棒的分类器或修正噪声标签本身。它们通常不直接输出U-Zero、U-One、U-Soft或U-Ignore这样的per-label strategy mapping，也不以减少候选final strategy models的穷举训练为目标。因此，本研究需要把label-wise reliability从“鲁棒训练结果”进一步前移为“策略选择依据”：在final model训练之前，利用teacher-score distributions判断每个label更适合哪一种uncertain-label strategy。这个前移在rare labels上尤其关键，因为长尾分布会进一步放大teacher和final model的不稳定性。

### 2.2.4 The Long-tail Challenge

CXR分类中的long-tailed label distribution是本研究必须考虑的重要背景。Holste et al. (2022, 2024)和Lin et al. (2025)表明，rare findings容易被common labels和大量negative examples掩盖。通用多标签不平衡方法，如class-balanced loss、distribution-balanced loss和asymmetric loss，也说明label frequency和easy negatives会影响模型优化方向（Cui et al., 2019; Wu et al., 2020; Ridnik et al., 2021）。这些文献提示，CXR模型评价不能只依赖整体AUROC；macro AUPRC、per-label AUPRC和rare-label AUPRC更能反映类别不平衡条件下的实际表现（Saito & Rehmsmeier, 2015）。

对本研究而言，long-tail的影响不仅体现在final model performance上，也直接影响teacher-score distributions的可信度。对于definite positive样本很少且uncertain ratio较高的label，teacher可能无法形成稳定的P/N/U分布关系，进而使profile mapping出现cold-start风险。因此，长尾文献不仅为rare-label evaluation提供依据，也说明teacher model需要imbalance-aware training，并且在profiling之前必须进行teacher reliability检查。

### 2.2.5 Teacher Reliability for Score-based Profiling

由于本研究依赖teacher model生成score distributions，teacher reliability是profile mapping成立的前提。Guo et al. (2017)指出现代神经网络可能存在miscalibration，Rajaraman et al. (2022)进一步将calibration问题与类别不平衡医学影像分类联系起来。Cheng and Vasconcelos (2024)则表明multi-label deep networks的calibration具有独立挑战，不能仅凭classification performance推断概率输出可靠。这些研究共同说明，teacher scores只有在分类能力、分布可分性和概率校准具有基本可靠性时，才适合作为strategy mapping的证据。

与此同时，calibration和reliability文献本身并不解决uncertain-label mapping问题。它们回答的是模型概率是否可信，而不是uncertain samples应被编码为positive、negative、soft target还是ignored。因此，本研究把teacher reliability作为使用score distributions之前的过滤条件，而不是最终贡献本身。可靠性检查之后，还需要一种能够比较P、N和U score distributions的profile方法，这就引出了distribution comparison和non-parametric statistics的作用。

### 2.2.6 Distributional Evidence for Uncertainty Profiling

本研究的profiling方法受到distribution comparison和non-parametric statistics文献的支持。Rubner et al. (2000)提出的Earth Mover's Distance可以从整体形状和移动距离角度比较分布；Damodaran et al. (2018)说明optimal transport思想可以用于深度学习中的分布对齐；Mann and Whitney (1947)提出的非参数检验适用于不假设score distributions服从正态分布的场景。这些方法之所以适合本研究，是因为teacher scores可能呈现偏态、重叠、双峰或两端极化。简单mean difference可能掩盖U distribution与P/N distribution之间的形状关系，也难以解释ambiguous cases。

同时，CheXpert规模较大，单纯依赖显著性检验会带来pseudo-significance风险，即实际差异很小的分布在大样本下仍可能产生显著p-value。因此，本研究只将Mann-Whitney p-value作为辅助证据，并结合rank-biserial effect size、overlap ratio和relative Wasserstein distance。这样的distributional measures不是为了增加方法复杂度，而是为了让Type A-D mapping建立在更可解释、可复查的分布证据上。

综合来看，现有研究已经说明uncertain-label handling存在label-wise差异，也提供了report-label discrepancy、noisy multi-label learning、long-tail evaluation、calibration和distribution comparison等关键基础。但这些研究要么在训练后发现策略差异，要么关注鲁棒分类或概率可靠性本身，仍缺少一种在训练所有候选final models之前，利用teacher-score distributions和reliability checks预测per-label uncertain-label strategy的可复现方法。

# CHAPTER 3
RESEARCH METHODOLOGY

## 3.1 Research Design and Framework

本研究采用quantitative experimental benchmarking design，并以secondary data analysis为基础。该研究设计适合本课题，因为研究问题需要在同一数据集、同一backbone和同一评价协议下，比较不同uncertain-label handling strategies的分类性能、校准表现和策略预测质量。研究逻辑偏deductive approach：已有文献表明CheXpert中的uncertain-label strategies存在label-wise差异，本研究据此提出teacher-assisted label-wise profiling方法，并通过CheXpert实验检验该方法能否预测per-label strategy并改善held-out test performance。

本研究的methodological framework将“策略选择”视为主要实验变量，将“label-wise uncertainty profile”视为中间决策机制，将“模型性能和策略预测质量”视为结果变量。具体而言，independent variable是uncertain-label handling strategy，包括U-Zero、U-One、U-Ignore、U-Soft和profile-guided strategy；decision mechanism是由teacher-score distributions、teacher reliability和decision rules构成的label-wise profile；dependent variables包括classification performance、calibration performance和strategy-prediction quality；control variables包括CheXpert数据集、固定backbone、固定teacher设置、相同data split、相同preprocessing和相同evaluation metrics。这样的框架使实验能够直接对应RQ1到RQ3：先分析uncertain samples的分布关系，再判断profile是否能预测validation oracle，最后评估profile-guided final model在held-out test set上的表现。

整体流程分为五个连续阶段。第一，构建CheXpert label matrix，统计每个label的positive、negative、uncertain和missing比例，并识别rare labels和high-uncertainty labels。第二，训练单一teacher model，用于生成每个label的score distributions。第三，对definite positive、definite negative和uncertain samples分别提取teacher scores，并计算分布相似度、重叠率、效应量和teacher reliability指标。第四，依据预定义decision rules将label分为Type A、Type B、Type C或Type D，并映射到相应的uncertain-label strategy。第五，训练profile-guided final model，并与固定策略和validation oracle upper bound进行比较。

图3.1  本研究的逐标签不确定性画像与策略选择框架

CheXpert labels -> P/N/U statistics -> Single teacher model -> Score distributions -> Distribution profiling + reliability check -> Decision rules -> Strategy mapping -> Final model evaluation

表3.1  本研究的概念与变量框架

| Component | Role in this study | Examples |
| --- | --- | --- |
| Independent variable | 被比较的uncertain-label处理方式 | U-Zero, U-One, U-Ignore, U-Soft, profile-guided strategy |
| Decision mechanism | 将label-wise profile映射为策略 | teacher-score distributions, reliability checks, Type A-D rules |
| Dependent variables | 评估模型和策略选择效果 | AUROC, AUPRC, rare-label AUPRC, ECE, Brier score, oracle agreement, regret |
| Control variables | 保持实验公平性和可比较性 | CheXpert split, backbone, teacher setting, image preprocessing, evaluation metrics |

## 3.2 Data Collection and Preprocessing

本研究以CheXpert作为唯一主实验数据集，因为它显式提供positive、negative、uncertain和blank状态，并且其不确定标签处理策略已经成为相关研究的重要基线（Irvin et al., 2019）。从研究方法角度看，CheXpert属于secondary research data，本研究不会进行新的临床数据采集或人工标注，而是在公开数据的基础上开展quantitative benchmarking和label-wise statistical analysis。

样本选择标准将以实验一致性和FYP可行性为原则。研究将纳入具有CheXpert目标观察标签的CXR images，并保留其positive、negative、uncertain和blank状态。若计算资源有限，实验将优先使用frontal views或预先定义的可复现实验子集；若使用子集，最终报告将记录抽样规则、label分布和排除条件。所有训练、验证和测试划分均需保持patient-level separation，以避免同一患者图像跨集合出现而造成data leakage。

数据划分将明确区分不同用途。training split用于训练teacher和final models；profile-validation split用于teacher calibration、profile threshold固定和validation oracle构造；held-out test set只用于最终模型比较，不参与teacher选择、threshold设定、oracle选择或任何策略调整。若官方test labels无法直接获得，本研究将从训练数据中划分train/profile-validation/held-out test，并保持相同的patient-level separation原则。

数据预处理包括图像尺寸统一、灰度/强度归一化、标签矩阵构建、数据划分确认，以及每个label的P/N/U/missing计数。对于每个label，本研究将计算positive prevalence、uncertain ratio、tail index和有效样本数。rare labels可根据positive prevalence或CXR-LT文献中的长尾分组思想定义；high-uncertainty labels则根据uncertain ratio排序确定。这些统计结果将作为teacher cold-start判断、rare-label evaluation和profile mapping的基础。

## 3.3 Imbalance-aware Teacher Model

teacher model主要用于生成label-wise score distributions，并为后续uncertainty profiling提供图像层面的预测证据。为控制FYP工作量和减少实验分支，本研究将固定一个backbone，例如DenseNet-121，并使用ImageNet预训练权重初始化。teacher采用U-Ignore策略训练，即在某个label上遇到uncertain samples时不计算该label的loss，从而避免在teacher阶段过早把uncertain labels硬编码为0或1。

由于CheXpert labels具有明显类别不平衡，teacher训练将采用一种固定的imbalance-aware loss，例如asymmetric loss，以降低common labels主导优化过程的风险。普通BCE可用于实现调试阶段的sanity check，但主实验不额外比较多个teacher losses或多个teacher architectures。这样安排能够使方法论重点保持在teacher-assisted profiling和strategy mapping上，同时让teacher具备处理rare labels的基本能力。

teacher reliability将按label单独评估，因为同一个teacher在common labels和rare labels上的可靠性可能存在明显差异。评估内容包括分类能力、P/N score distributions可分性、概率校准和minimum support。对于definite positive样本数过少、P/N分布不可分或calibration较差的label，本研究将其标记为cold-start/unreliable risk，并在后续mapping中保守归入Type D。teacher reliability、minimum support和effect size约束共同构成methodological risk-control mechanisms，用于减少teacher prediction不可靠、rare-label cold-start和大样本伪显著对profile mapping的影响。

## 3.4 Label-wise Uncertainty Profiling

完成teacher训练后，本研究将对每个label分别提取三组样本的teacher scores：definite positive samples、definite negative samples和uncertain samples。三组scores将被视为经验分布进行比较，因为uncertain samples可能与positive或negative分布部分重叠，也可能位于两者之间；若只比较均值，容易忽略分布形状、重叠区域和ambiguous cases。

profile feature的设计围绕两个问题展开：第一，U distribution在模型预测空间中更接近P还是N；第二，teacher scores是否足够可靠，能够支持这种判断。为回答第一个问题，本研究将计算U-P和U-N之间的Wasserstein distance、distribution overlap ratio、median score difference、Mann-Whitney U test和rank-biserial effect size。为回答第二个问题，本研究将同时记录P/N separability、ECE、Brier score和minimum support。这样的设计避免把uncertain-label profiling简化为单一统计量判断，也使每个label的strategy assignment能够被复查。

这些features将用于判断U distribution更接近P、N、二者之间的ambiguous区域，还是由于teacher不可靠而无法判断。为提高方法可复现性，本研究将采用预定义decision rules，将连续profile features转化为可执行的Type A-D分类规则。以下数值将作为initial operational thresholds。这些阈值并非理论常数，而是基于三个原则设定：保证每个label有足够样本支持、避免teacher calibration明显失真、以及要求统计差异具有可解释的实际效应。阈值将在profile-validation split上通过小范围敏感性分析检查稳定性，并在固定后用于held-out test evaluation；held-out test set不会用于调整任何阈值。

1. Minimum support rule：若某label的definite positive或definite negative样本数低于预设下限，例如少于100例，或validation AUPRC低于该label prevalence的两倍，则标记为Type D。

2. Reliability rule：若teacher的ECE高于0.15、Brier score明显高于同label的validation baseline，或P/N separability低于0.60，则标记为Type D。

3. Ambiguity rule：若U-P和U-N的overlap ratio均较高，例如均高于0.60，或rank-biserial effect size低于0.20，则标记为Type C。

4. Positive-like rule：若d(U,P) < d(U,N)，且相对距离差距超过20%，同时U与N之间具有中等以上effect size，则标记为Type A。

5. Negative-like rule：若d(U,N) < d(U,P)，且相对距离差距超过20%，同时U与P之间具有中等以上effect size，则标记为Type B。

Mann-Whitney U test的p-value只作为辅助证据。本研究将重点使用effect size和overlap ratio避免大样本下“统计显著但实际差异很小”的伪显著问题。最终报告中将提供每个label的profile feature table，使Type A-D划分能够被复查。

伪代码如下：

```text
For each label l:
  Compute P_l, N_l, U_l teacher-score distributions
  Compute d_UP, d_UN, overlap_UP, overlap_UN, median gaps, effect sizes
  If minimum support or teacher reliability fails:
      assign Type D and strategy U-Ignore
  Else if overlap_UP and overlap_UN are high or effect size is small:
      assign Type C and strategy U-Soft
  Else if d_UP is sufficiently smaller than d_UN:
      assign Type A and strategy U-One
  Else if d_UN is sufficiently smaller than d_UP:
      assign Type B and strategy U-Zero
  Else:
      assign Type C and strategy U-Soft
```

## 3.5 Strategy Mapping

根据3.4中的profile结果，每个label将被映射到一种uncertain-label handling strategy。该映射使用teacher score distributions作为策略选择证据，但不会把teacher probability直接写入最终训练标签；最终标签处理仍由Type A-D规则决定。表3.2总结了Type A-D profile与策略之间的对应关系。

表3.2  逐标签不确定性画像类型与策略映射

| Profile Type | 分布特征 | 建议策略 | 解释 |
| --- | --- | --- | --- |
| Type A: positive-like | U更接近P，且与N分离；teacher可靠 | U-One | uncertain样本可能包含真实阳性证据，硬置0会增加false negative风险。 |
| Type B: negative-like | U更接近N，且与P分离；teacher可靠 | U-Zero | uncertain表达更可能来自谨慎报告或弱证据，硬置1会增加false positive风险。 |
| Type C: ambiguous | U位于P/N之间，或与两者高度重叠 | U-Soft | 标签语义确实模糊，硬编码为0或1风险较高。 |
| Type D: unreliable | teacher P/N不可分，或calibration较差 | U-Ignore | 保守忽略uncertain samples可降低teacher偏差传递到final model的风险。 |

U-Soft将采用固定soft target，例如0.5，以避免把teacher probability直接写入final labels。该选择强调简单、可复现和避免teacher-bias propagation，但也存在局限：在positive prevalence极低的rare labels上，0.5可能高估uncertain samples中的阳性信号。因此，本研究将在rare-label AUPRC和calibration分析中单独观察Type C labels的表现，并在discussion中报告fixed 0.5对rare labels的潜在影响。对于Type D，本研究将优先采用U-Ignore，以保证方法在teacher reliability较低时有保守退路。

考虑到CXR labels之间存在共现和层级关系，本研究还将进行label-dependency consistency check，但该检查仅作为post-hoc explanatory analysis。具体做法是计算label co-occurrence matrix，并检查高度相关的labels是否被映射到明显冲突的策略类型。如果高度共现的labels出现相反策略，本研究将在结果分析中报告该现象，并通过final model的joint multi-label training观察其对整体性能和calibration的影响。该检查不会修改Type A-D策略映射，也不会引入额外的label-dependency correction mechanism，以避免扩大研究范围。

## 3.6 Model Training and Evaluation

final model将使用profile-guided labels进行训练，并与固定策略和validation oracle upper bound进行比较。所有final models将尽量使用相同backbone、preprocessing、training split和evaluation protocol，以保证策略差异是主要比较因素。

1. Fixed strategies: all U-Zero, all U-One, all U-Ignore and all U-Soft.

2. Profile-guided strategy: 根据Type A-D分别采用U-One、U-Zero、U-Soft或U-Ignore。

3. Validation oracle upper bound: 为每个label在profile-validation split上选择表现最好的候选策略，仅作为策略选择上限参考。

validation oracle本身属于评估阶段的reference upper bound，部署时无法直接获得。为了构造该oracle，本研究仍需训练固定候选策略模型，并在profile-validation split上为每个label选择表现最好的策略。因此，oracle的作用是提供训练后经验选择参照，用来衡量profile-guided method与穷举比较结果之间的差距。若profile-guided method在held-out test set上表现稳定，其实际价值在于减少未来面对新数据集或新标签集合时对完整候选final strategy models穷举训练的依赖。

主要评价指标包括三类。第一类是分类性能：macro/micro AUROC、macro/micro AUPRC、per-label AUPRC和rare-label AUPRC。由于任务类别不平衡，AUPRC和rare-label AUPRC将作为更重要的指标。第二类是校准性能：ECE、adaptive ECE和Brier score，用于观察profile-guided strategy是否改善概率可靠性。第三类是策略预测质量：与validation oracle per-label strategy的agreement，以及相对于oracle的regret。regret将分别报告validation regret和held-out test regret，以区分策略预测质量和最终模型泛化表现。同时，本研究会明确说明validation oracle可能存在validation overfitting；它代表profile-validation split上的经验上限，而不一定是真正的test oracle。

为控制FYP范围，主实验将固定一个backbone、一个teacher和一组预定义decision rules。鲁棒性分析将限制为必要的轻量检查，例如对关键阈值进行小范围扰动，并报告profile type是否发生频繁跳变。多seed训练、外部数据集验证和复杂消融将作为future work或扩展实验，不作为本proposal的核心交付。

## 3.7 Validity and Reliability Considerations

为提高研究设计的可信度，本研究将在internal validity、construct validity和experimental reliability三个方面进行控制。Internal validity主要通过数据划分控制：profile-validation split用于teacher calibration、decision rule固定和validation oracle构造；held-out test set只用于最终模型比较，不参与threshold tuning、oracle selection或任何策略调整。这样可以降低selection bias和test leakage风险。

Construct validity主要通过多维评价指标保证。由于本研究关注的不只是分类准确率，还包括策略选择质量和概率可靠性，因此评价将同时包含classification metrics、calibration metrics和strategy-prediction metrics。macro AUPRC和rare-label AUPRC用于反映类别不平衡下的模型表现；ECE和Brier score用于衡量概率可靠性；oracle agreement和regret用于衡量profile-guided strategy与validation oracle之间的差距。这样的指标设计与研究问题相对应，避免只用单一AUROC解释整体效果。

Experimental reliability将通过固定实验条件和可复现规则实现。主实验固定CheXpert数据集、backbone、teacher设置、preprocessing流程、decision rules和evaluation metrics；Type A-D mapping会输出每个label的profile feature table，方便复查策略分配过程。对于validation oracle overfitting、teacher cold-start和large-sample pseudo-significance等风险，本研究将通过held-out test reporting、minimum support rule、effect size和overlap ratio进行控制。上述措施使实验结果更容易被复现，也使方法局限能够在最终报告中被明确讨论。

# CHAPTER 4
PRELIMINARY FINDINGS

## 4.1 Preliminary Feasibility Findings

目前项目处于proposal阶段，模型训练尚未进行，因此本章不报告实验性能结果。现阶段的preliminary findings主要来自文献证据、数据可获得性分析和可执行实验设计。CheXpert公开提供带有positive、negative、uncertain和blank状态的多标签胸片数据，能够直接支持本研究的P/N/U label distribution analysis、uncertain-label strategy comparison和label-wise profiling实验（Irvin et al., 2019）。因此，本研究的第一项初步分析将聚焦于label distribution statistics：统计每个label的positive prevalence、uncertain ratio、missing ratio和definite sample support，并据此识别rare labels、high-uncertainty labels和cold-start risk labels。

表4.1  CheXpert初步标签分布分析计划

| Statistic | Computation | Purpose in this study |
| --- | --- | --- |
| Positive prevalence | Positive count / available label count | Identify rare labels and define rare-label AUPRC group. |
| Uncertain ratio | Uncertain count / available label count | Identify high-uncertainty-burden labels. |
| Definite sample support | Positive count + negative count | Detect labels where U-Ignore teacher may suffer from cold-start risk. |
| Missing ratio | Missing count / total image count | Assess whether missing labels may affect reliable profile construction. |
| P/N/U balance | Positive, negative and uncertain counts per label | Decide whether the label can enter Type A-C mapping or should be conservatively assigned to Type D. |

该统计表将作为后续实验的gatekeeping step。若某个label的definite positive或definite negative样本过少，该label会被标记为cold-start risk，并在profile mapping中优先进入Type D或进行单独分析。这样可以避免teacher在缺少有效监督信号时仍被用于强行判断uncertain samples的方向。

## 4.2 Literature-supported Design Findings

文献分析得到以下设计结论。第一，CheXpert已经证明不同pathology可能偏好不同uncertainty handling strategies，这为进一步研究策略预测机制提供了起点。第二，CheXbert、VisualCheXbert和report labeler quality研究说明report-derived labels与image evidence之间存在差异，因此uncertain labels需要结合图像预测分布进行解释。第三，CXR-LT和LongTailCXR证明胸片疾病标签具有明显长尾分布，rare-label表现需要单独评价。第四，calibration研究说明teacher probability可能存在可靠性风险，因此本研究将加入ECE、Brier score、P/N separability和minimum support检查。第五，Wasserstein distance、overlap ratio、effect size和Mann-Whitney U test适合用于非正态、偏态或两端极化的score distribution比较，其中p-value仅作为辅助证据。

## 4.3 Feasibility and Risk Control

本研究的可行性来自三个方面。第一，主实验只依赖CheXpert，不把外部数据集验证纳入核心交付，因此避免了额外数据授权、跨数据集标签对齐和额外计算资源带来的范围扩张。第二，模型设置被压缩为一个backbone和一个teacher model，主要比较对象也限制为四种固定策略、profile-guided strategy和validation oracle upper bound。第三，profile decision rules将在profile-validation split上固定，held-out test set只用于最终比较，从而降低selection bias。validation oracle也将在结果解释中被定位为validation reference upper bound，而非保证在test set上仍然最优的test oracle。

本研究也识别了三个主要方法风险。第一是teacher cold-start risk：对于definite samples极少且uncertain ratio很高的label，U-Ignore teacher可能缺少足够训练信号。对此，本研究加入minimum support rule，并将这类label优先标记为Type D。第二是large-sample pseudo-significance：CheXpert样本量较大，Mann-Whitney U test可能在实际分布高度重叠时仍产生显著p-value。对此，本研究要求同时满足effect size、overlap ratio和relative Wasserstein distance条件，避免只凭p-value进行硬切分。第三是validation oracle overfitting：oracle在profile-validation split上选择最优策略，但该策略在held-out test set上可能出现性能波动。对此，本研究将同时报告validation regret和held-out test regret，并把oracle解释为评估参考而不是最终真实上限。

## 4.4 Anticipated Results

由于validation oracle per-label strategy代表完整候选策略训练后的validation参考上限，profile-guided strategy的预期目标是以较低策略选择成本接近该参考上限。预期结果将分两层解释。第一层是strategy prediction quality：profile-guided mapping应与validation oracle在部分labels上达成较高agreement，并在regret上低于随机或单一固定策略选择。第二层是final model performance：profile-guided final model应在held-out test set上取得比多数固定策略更稳定的macro AUPRC、rare-label AUPRC和calibration表现。对于Type A标签，U-One可能减少false negatives；对于Type B标签，U-Zero可能减少false positives；对于Type C标签，U-Soft应比硬编码更稳健，但fixed 0.5在rare labels上可能带来阳性信号高估风险；对于Type D标签，U-Ignore预期可降低低可靠teacher带来的偏差传递风险。

## 4.5 Conclusion

综上，本proposal提出一种面向CheXpert-style imbalanced multi-label CXR classification的label-wise uncertainty profiling框架。该框架建立在已有文献的真实缺口之上：不同label可能需要不同uncertain-label strategies这一点已经被发现，但现有研究仍缺少一种在训练所有候选final strategy models之前、利用单一teacher model辅助预测per-label strategy的可解释机制。后续研究将围绕CheXpert标签统计、single-teacher训练、decision-rule-based profiling、strategy mapping和held-out test evaluation五个环节展开。项目范围在FYP阶段是可行的，因为核心实验集中在CheXpert、一个backbone、一个teacher、四种固定策略、profile-guided strategy和validation oracle upper bound上。

# References

Chen, B., Li, J., Lu, G., Yu, H., & Zhang, D. (2020). Label co-occurrence learning with graph convolutional networks for multi-label chest X-ray image classification. IEEE Journal of Biomedical and Health Informatics, 24(8), 2292-2302.

Chen, Y., Liu, F., Wang, H., Wang, C., Liu, Y., Tian, Y., & Carneiro, G. (2023). BoMD: Bag of multi-label descriptors for noisy chest X-ray classification. Proceedings of the IEEE/CVF International Conference on Computer Vision, 21284-21295.

Cheng, J., & Vasconcelos, N. (2024). Towards calibrated multi-label deep neural networks. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 27589-27599.

Cui, Y., Jia, M., Lin, T. Y., Song, Y., & Belongie, S. (2019). Class-balanced loss based on effective number of samples. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 9268-9277.

Damodaran, B. B., Kellenberger, B., Flamary, R., Tuia, D., & Courty, N. (2018). DeepJDOT: Deep joint distribution optimal transport for unsupervised domain adaptation. Proceedings of the European Conference on Computer Vision, 447-463.

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. Proceedings of the International Conference on Machine Learning, 1321-1330.

Holste, G., Zhou, Y., Wang, S., Jaiswal, A., Lin, M., et al. (2024). Towards long-tailed, multi-label disease classification from chest X-ray: Overview of the CXR-LT challenge. Medical Image Analysis.

Holste, G., Wang, S., Jiang, Z., Shen, T. C., Shih, G., Summers, R. M., Peng, Y., & Wang, Z. (2022). Long-tailed classification of thorax diseases on chest X-ray: A new benchmark study. MICCAI Workshop.

Irvin, J., Rajpurkar, P., Ko, M., Yu, Y., Ciurea-Ilcus, S., Chute, C., Marklund, H., Haghgoo, B., Ball, R., Shpanskaya, K., Seekins, J., Mong, D. A., Halabi, S. S., Sandberg, J. K., Jones, R., Larson, D. B., Langlotz, C. P., Patel, B. N., Lungren, M. P., & Ng, A. Y. (2019). CheXpert: A large chest radiograph dataset with uncertainty labels and expert comparison. Proceedings of the AAAI Conference on Artificial Intelligence, 33(01), 590-597.

Jain, S., Agrawal, A., Saporta, A., Truong, S. Q. H., Duong, D. N., Bui, T., Chambon, P., Zhang, Y., Lungren, M. P., Ng, A. Y., Langlotz, C. P., & Rajpurkar, P. (2021a). VisualCheXbert: Addressing the discrepancy between radiology report labels and image labels. Proceedings of the ACM Conference on Health, Inference, and Learning.

Jain, S., Agrawal, A., Saporta, A., Truong, S. Q. H., Duong, D. N., Bui, T., Chambon, P., Zhang, Y., Lungren, M. P., Ng, A. Y., Langlotz, C. P., & Rajpurkar, P. (2021b). Effect of radiology report labeler quality on deep learning models for chest X-ray classification. arXiv preprint arXiv:2104.00793.

Lin, C., Holste, G., Zhou, Y., Wang, S., et al. (2025). CXR-LT 2024: A MICCAI challenge on long-tailed, multi-label, and zero-shot disease classification from chest X-ray. arXiv preprint arXiv:2506.07984.

Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. The Annals of Mathematical Statistics, 18(1), 50-60.

Pham, H. H., Le, T. T., Tran, D. Q., Ngo, D. T., & Nguyen, H. Q. (2021). Interpreting chest X-rays via CNNs that exploit hierarchical disease dependencies and uncertainty labels. Neurocomputing, 437, 186-194.

Rajaraman, S., Ganesan, P., & Antani, S. (2022). Deep learning model calibration for improving performance in class-imbalanced medical image classification tasks. PLOS ONE, 17(1), e0262838.

Ridnik, T., Ben-Baruch, E., Zamir, N., Noy, A., Friedman, I., Protter, M., & Zelnik-Manor, L. (2021). Asymmetric loss for multi-label classification. Proceedings of the IEEE/CVF International Conference on Computer Vision, 82-91.

Rubner, Y., Tomasi, C., & Guibas, L. J. (2000). The Earth Mover's Distance as a metric for image retrieval. International Journal of Computer Vision, 40(2), 99-121.

Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PLOS ONE, 10(3), e0118432.

Smit, A., Jain, S., Rajpurkar, P., Pareek, A., Ng, A. Y., & Lungren, M. P. (2020). Combining automatic labelers and expert annotations for accurate radiology report labeling using BERT. Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, 1500-1519.

Wu, T., Huang, Q., Liu, Z., Wang, Y., & Lin, D. (2020). Distribution-balanced loss for multi-label classification in long-tailed datasets. Proceedings of the European Conference on Computer Vision, 162-178.

Ye, X., et al. (2026). Label-wise reliability-aware classifier for robust chest X-ray multi-label classification. Expert Systems with Applications.

# Appendix

附录A  初步项目计划

| 阶段 | 时间 | 主要任务 | 交付物 |
| --- | --- | --- | --- |
| Phase 1 | Week 1-2 | 复核核心文献、确认CheXpert访问方式、确定实验标签和划分。 | 最终proposal、核心文献矩阵、数据访问计划。 |
| Phase 2 | Week 3-5 | 完成图像预处理、label matrix构建、P/N/U/missing统计和rare-label分组。 | 数据统计表、预处理脚本、label分布分析。 |
| Phase 3 | Week 6-8 | 训练BCE teacher和imbalance-aware teacher，评估AUPRC/ECE/Brier/P-N separability。 | teacher checkpoint、per-label reliability报告。 |
| Phase 4 | Week 9-10 | 构建Wasserstein、overlap、median difference和Mann-Whitney U profile。 | label-wise uncertainty profile表、Type A-D映射。 |
| Phase 5 | Week 11-13 | 训练profile-guided final model、固定策略基线和validation oracle upper bound。 | 实验结果表、strategy agreement和regret分析。 |
| Phase 6 | Week 14 | 整理结果、撰写FYP报告和准备答辩材料。 | 最终论文、poster或slides、答辩材料。 |
