<!-- Generated from FYP_Proposal_CN_Labelwise_Uncertainty_Profiling_Revised_Gap.docx for Codex preview. -->

THESIS PROPOSAL

面向类别不平衡多标签胸片分类的逐标签不确定性画像与标签处理策略选择研究

Label-wise Uncertainty Profiling for Strategy Selection in Imbalanced Multi-label Chest X-ray Classification

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

胸部X光片（Chest X-ray, CXR）是临床中使用最广泛的医学影像之一。随着CheXpert、MIMIC-CXR-JPG等大规模数据集的发布，深度学习模型已经能够在多标签胸片分类中取得较高的AUROC。然而，胸片分类的监督信号通常来自放射报告自动抽取，而报告中包含大量possible、cannot exclude、questionable等不确定表达。因此，训练标签并不总是明确的0/1 ground truth，而是包含report-derived uncertain labels。

现有研究已经证明，不确定标签的处理方式会显著影响模型性能。CheXpert原论文比较了U-Zero、U-One、U-Ignore、U-SelfTrained等策略，并发现不同病种标签可能适合不同策略（Irvin et al., 2019）。因此，本研究并不是简单再比较几种标签编码方式，而是希望在训练完整候选策略模型之前，为每个label建立uncertainty profile，并用该画像解释和预测其更合理的处理策略。

## 1.2 Problem Background

在CheXpert等大规模胸片数据集中，一张胸片通常对应多个疾病或观察标签，因此任务天然属于multi-label classification。CheXpert的标签来自放射报告自动抽取，并将报告中的possible、cannot exclude、questionable等表达编码为uncertain labels（Irvin et al., 2019）。这一设计使CheXpert成为研究胸片不确定标签处理的关键数据集，但也引出了一个已经被文献反复指出的问题：report-derived labels并不等同于image-level ground truth。CheXbert和VisualCheXbert相关研究表明，报告标签的抽取质量、报告文本表达方式以及图像证据之间存在不一致，这种不一致会传递到下游胸片分类模型中（Smit et al., 2020; Jain et al., 2021a; Jain et al., 2021b）。

已有研究并非没有处理uncertain labels。CheXpert原论文已经比较过U-Zero、U-One、U-Ignore、U-SelfTrained等策略，并发现不同pathologies会受益于不同的不确定标签处理方式（Irvin et al., 2019）。Pham et al. (2021)也进一步使用层级疾病依赖与label smoothing处理胸片不确定标签。因此，本研究的问题不是重新证明“不确定标签需要处理”，也不是简单再比较几种固定策略，而是进一步追问：为什么某个label应选择某种策略？是否可以在完整训练所有候选策略之前，根据该label的uncertain samples与definite positive/negative samples之间的分布关系，预测一个合理策略？

这一问题在类别不平衡和罕见标签场景下更重要。CXR-LT和LongTailCXR研究指出，胸片疾病标签具有明显的长尾分布，rare findings容易被common labels和大量negative labels掩盖（Holste et al., 2022; Holste et al., 2024; Lin et al., 2025）。多标签长尾学习文献也指出，label co-occurrence和negative dominance会影响模型优化（Wu et al., 2020; Ridnik et al., 2021）。如果teacher model在rare labels上本身不可靠或校准不足，直接使用teacher probability替代uncertain labels可能会把模型偏差传递给final model。Guo et al. (2017)、Rajaraman et al. (2022)和Cheng and Vasconcelos (2024)关于校准的研究进一步说明，teacher probability必须经过可靠性检查后才能作为策略选择依据。

## 1.3 Research Gap

现有研究已经为本课题奠定了明确基础：CheXpert提出report-derived uncertain labels，并比较了U-Zero、U-One、U-Ignore和U-SelfTrained等处理策略，结果显示不同pathology对策略的偏好并不一致（Irvin et al., 2019）；Pham et al. (2021)进一步说明soft label/label smoothing也可用于胸片不确定标签处理。由此可见，当前研究的关键问题已经从“是否需要处理uncertain labels”推进到“如何在具体label层面解释和选择处理策略”。

然而，现有策略选择大多依赖训练后的经验比较：研究者通常需要为候选处理方式分别训练模型，再在validation set上比较各label表现。这种brute-force empirical comparison虽然能够得到经验最优结果，但仍留下三个不足。第一，训练成本会随候选策略数量增加而上升；第二，它只能在训练完成后给出哪个策略更好，却难以解释uncertain samples为什么更接近positive、negative或ambiguous；第三，它较少把report-derived label discrepancy、long-tailed multi-label imbalance和teacher calibration这些已被后续文献强调的因素整合到策略选择机制中（Jain et al., 2021a; Holste et al., 2024; Cheng and Vasconcelos, 2024）。

因此，本研究的research gap可以表述为：在CheXpert-style imbalanced multi-label CXR classification中，仍缺少一种可解释的label-wise uncertainty profiling框架，能够在不穷举训练所有候选策略的前提下，利用teacher-score distribution、非参数分布相似度和teacher reliability检查，为每个label预测较合理的uncertain-label handling strategy。该gap位于CheXpert uncertain-label strategies、report-label discrepancy、long-tail CXR、calibration和noisy multi-label learning等研究方向的交叉处。

## 1.4 Aims and Objectives

本研究的总体目标是开发并评估一种面向类别不平衡多标签胸片分类的逐标签不确定性画像框架。该框架将以CheXpert为主要数据集，在已有uncertain-label strategy、report-derived label discrepancy、long-tailed CXR和model calibration文献的基础上，尝试使用teacher-score distributions和可靠性检验，在训练完整候选策略模型之前预测每个label更合理的不确定标签处理策略。

具体研究目标如下：

统计CheXpert各label中positive、negative和uncertain样本数量，并识别rare labels和high uncertainty-burden labels。

训练一个imbalance-aware teacher model，使其在多标签长尾胸片任务中尽可能减少majority labels和negative dominance的影响。

对每个label分别提取definite positive、definite negative和uncertain samples的teacher-score distributions。

使用Wasserstein distance、overlap ratio和Mann-Whitney U test构建逐标签uncertainty profile。

结合teacher的validation AUPRC、ECE和Brier score，判断每个label的teacher prediction是否足够可靠。

将labels划分为Type A（U-as-positive）、Type B（U-as-negative）、Type C（U-as-ambiguous）和Type D（U-as-unreliable），并据此选择U-One、U-Zero、U-Soft或U-Ignore等策略。

将profile-guided strategy与固定策略、teacher-soft/self-training策略以及oracle per-label best strategy进行比较，并使用AUROC、AUPRC、rare-label performance、ECE、Brier score、agreement和regret进行评估。

# CHAPTER 2
LITERATURE REVIEW

## 2.1 Introduction

本章将围绕本研究问题的文献来源进行综述，而不是单纯罗列相关技术。现有文献首先提供了本研究的任务基础：CheXpert明确提出了report-derived uncertain labels，并显示不同疾病标签会受益于不同的不确定标签处理策略（Irvin et al., 2019）；CheXbert、VisualCheXbert和报告标注器质量研究进一步说明，放射报告自动抽取标签与图像层面的真实证据之间存在差异，且这种差异会影响下游胸片分类模型（Smit et al., 2020; Jain et al., 2021a; Jain et al., 2021b）。因此，本研究的问题不是凭空假设uncertain labels有问题，而是建立在已有report-derived label discrepancy和uncertain-label strategy文献之上。

其次，CXR-LT、LongTailCXR和多标签长尾学习文献表明，胸片分类具有明显的long-tailed multi-label特征，rare labels和negative dominance会使普通BCE或统一标签策略产生偏向（Holste et al., 2022; Holste et al., 2024; Wu et al., 2020; Ridnik et al., 2021）。与此同时，校准文献指出高分类性能并不等于概率可靠，尤其在多标签和不平衡医学图像分类中，teacher probability需要被校准和验证（Guo et al., 2017; Rajaraman et al., 2022; Cheng and Vasconcelos, 2024）。基于这些文献，本研究将文献综述组织为五个方向：report-derived uncertainty、noisy multi-label CXR learning、long-tailed multi-label imbalance、teacher calibration/reliability，以及distribution-level profiling与非参数统计检验。表2.1总结了本研究将重点参考的25篇文献。

表2.1  与本研究相关的25篇核心文献综述矩阵

| 作者/年份 | 主要切入点 | 对本研究的具体支撑 | 局限与启示 |
| --- | --- | --- | --- |
| Irvin et al., 2019 | CheXpert数据集；报告抽取标签；U-Zero、U-One、U-Ignore、U-SelfTrained等不确定标签策略比较。 | 奠定本研究的数据集与问题起点，并证明不同pathology可能偏好不同uncertain-label strategy。 | 已有策略选择主要来自训练后的经验比较；本研究将进一步追问能否在完整训练候选策略前进行逐标签预测。 |
| Oakden-Rayner et al., 2019 | 医学影像模型中的hidden stratification与子群失败风险。 | 提醒整体AUROC可能掩盖少数病种、罕见亚型或高不确定性样本上的失败。 | 不直接研究CheXpert不确定标签，但为rare-label和label-wise分析的重要性提供风险依据。 |
| Jain et al., 2021a | VisualCheXbert；比较报告标签与图像证据之间的差异。 | 支撑report-derived labels不等同于image-level ground truth这一问题背景。 | 主要关注标签质量评估，不直接给出uncertain-label strategy selection方法。 |
| Jain et al., 2021b | 研究不同radiology report labeler质量对下游胸片分类模型的影响。 | 说明自动报告标注器误差会传递到分类模型，是本研究需要解释uncertain label来源的依据。 | 关注labeler质量与下游性能，本研究将其延伸到逐标签策略选择。 |
| Gao et al., 2024 | 多标注者胸片标签不确定性；ARDS场景中不同医生标注差异。 | 从人工标注角度说明医学影像标签不确定性并非单纯随机噪声。 | 场景不是CheXpert常规多标签分类，但可作为医学标签不确定性的背景证据。 |
| Chen et al., 2020 | CheXGCN；利用标签共现图结构提升胸片多标签分类。 | 说明CXR标签之间存在依赖关系，单独处理某个label时应注意multi-label co-occurrence背景。 | 重点是标签关系建模而非不确定标签；在本研究中作为多标签任务背景文献使用。 |
| Cheng & Vasconcelos, 2024 | 多标签深度网络校准；讨论multi-label setting下概率可靠性问题。 | 支撑本研究不能直接信任teacher probability，需引入ECE、Brier等可靠性检查。 | 不专门面向胸片，但其multi-label calibration问题与本研究teacher reliability高度相关。 |
| Smit et al., 2020 | CheXbert；使用BERT改进放射报告自动标注。 | 说明CheXpert-style标签来自NLP标注器，标签质量与报告表达直接影响监督信号。 | 更关注report labeler而非图像分类策略；本研究使用其支持report-derived label discrepancy。 |
| Cui et al., 2019 | Class-Balanced Loss；基于有效样本数处理类别不平衡。 | 为imbalance-aware teacher提供损失函数层面的经典依据。 | 原方法主要面向单标签/通用视觉长尾；在CXR多标签中需结合AUPRC和negative dominance验证。 |
| Guo et al., 2017 | 现代神经网络校准；温度缩放与ECE等校准评价。 | 为本研究评估teacher和final model概率可靠性提供基础文献。 | 不是医学影像或多标签专文，但校准问题是teacher-based profiling的必要前提。 |
| Rajaraman et al., 2022 | 不平衡医学图像分类中的校准与模型可靠性。 | 把校准问题放回医学影像和类别不平衡语境，支撑本研究关注ECE/Brier。 | 不直接处理CheXpert uncertain labels，但对rare-label teacher reliability很关键。 |
| Pham et al., 2021 | 胸片分类中的层级疾病依赖与label smoothing处理不确定标签。 | 说明soft/平滑式处理已经存在，因此本研究的创新应落在策略预测与解释，而不是简单soft label。 | 可以作为强相关基线或对照，但不能被本研究误写成尚未有人处理soft uncertainty。 |
| Ridnik et al., 2021 | Asymmetric Loss；针对多标签分类中的正负样本不平衡与易负样本。 | 为teacher和final model的multi-label imbalance-aware训练提供强基线。 | 通用多标签方法；用于CXR rare labels时仍需医学指标和校准验证。 |
| Saito & Rehmsmeier, 2015 | 在不平衡数据中讨论PR curve相对ROC curve的解释优势。 | 支撑本研究除AUROC外必须报告AUPRC，尤其是macro/rare-label AUPRC。 | 不是深度学习或医学影像论文，但对不平衡评价指标选择具有基础价值。 |
| Holste et al., 2024 | CXR-LT；长尾多标签胸片疾病分类基准。 | 直接支撑本研究强调long-tailed CXR、rare labels和整体指标掩盖问题。 | 重点在长尾基准与模型挑战；本研究将其与uncertain-label profiling结合。 |
| Lin et al., 2025 | CXR-LT 2024；罕见与零样本胸片疾病分类挑战。 | 作为最新进展，说明rare findings仍是CXR分类中的开放问题。 | 零样本问题不是本课题核心，因此在proposal中作为长尾背景而非主要方法来源。 |
| Yang et al., 2019 | 胸片不确定标签与贝叶斯神经网络/不确定性建模。 | 提示可以把模型不确定性与标签不确定性联系起来，为teacher reliability提供补充背景。 | 方法路线与本研究的分布画像不同；适合作为相关工作而非主要基线。 |
| Chen et al., 2023 | BoMD；面向report-derived noisy multi-label CXR labels的鲁棒学习。 | 说明胸片多标签噪声不能简单套用通用单标签噪声学习，是本研究重要近邻文献。 | 主要解决噪声标签鲁棒训练；本研究聚焦策略选择前的label-wise uncertainty profiling。 |
| Mann & Whitney, 1947 | Mann-Whitney U非参数检验。 | 为比较definite positive/negative/uncertain teacher-score distributions提供统计检验依据。 | 统计基础文献本身不涉及医学影像；在方法章节用于支撑非参数检验选择即可。 |
| Johnson et al., 2019 | MIMIC-CXR-JPG；大规模带标签胸片数据集。 | 提供CheXpert之外的可选外部验证数据集背景，并支持report-derived labels普遍存在。 | 本proposal以CheXpert为主；MIMIC-CXR-JPG可作为扩展验证而非核心数据集。 |
| Ye et al., 2026 | 逐标签可靠性感知的鲁棒胸片多标签分类。 | 非常贴近本研究的label-wise reliability思路，支撑逐标签分析优于统一噪声判断。 | 其目标偏向鲁棒分类器设计；本研究的区别是预测U-Zero/U-One/U-Soft/U-Ignore等处理策略。 |
| Holste et al., 2022 | LongTailCXR；长尾胸部疾病分类基准与分析。 | 为rare-label分组评价和长尾问题设定提供直接胸片文献依据。 | 偏benchmark与挑战定义；本研究将其作为评价设计和问题动机来源。 |
| Wu et al., 2020 | Distribution-Balanced Loss；长尾多标签分类中的类别分布重平衡。 | 为multi-label long-tail training提供核心方法参考，可用于teacher或final baseline。 | 通用视觉多标签方法；在CheXpert上需结合report-derived uncertainty进行验证。 |
| Rubner et al., 2000 | Earth Mover's Distance；图像检索中的分布距离度量。 | 为使用Wasserstein/EMD比较score distributions提供经典方法学来源。 | 原场景为图像检索；本研究将其用于teacher sigmoid score分布而非原始图像直方图。 |
| Damodaran et al., 2018 | DeepJDOT；最优传输用于深度表示与分布对齐。 | 说明最优传输思想可在深度学习特征/预测分布比较中发挥作用。 | 不是胸片或标签不确定性论文；作为Wasserstein思想进入深度学习的补充支撑。 |

## 2.2 Background Studies

第一类文献奠定了本研究的问题基础。Irvin et al. (2019)发布CheXpert并引入uncertain labels，同时比较了多种不确定标签处理策略，发现不同pathology适合不同策略。该结论直接说明统一策略不足，但也意味着本研究不能把“不同label需要不同strategy”作为新的gap。Pham et al. (2021)进一步将label smoothing用于胸片不确定标签处理，说明简单soft label也已经不是强创新。因此，本研究需要在已有策略处理基础上进一步提出可解释的strategy prediction框架。

第二类文献说明report-derived labels本身存在质量和语义差异。Smit et al. (2020)提出CheXbert，展示报告自动标注质量可以通过BERT和专家标注改进；Jain et al. (2021a)的VisualCheXbert进一步指出，报告标签与图像标签之间存在discrepancy；Jain et al. (2021b)则证明不同report labeler的质量会影响下游CXR classifier。这些研究共同说明，本研究中的uncertain labels并不是简单随机噪声，而是放射报告表达、自动标注器和图像证据之间差异的体现。

第三类文献关注噪声多标签胸片学习和逐标签可靠性。Chen et al. (2023)提出BoMD处理report-derived noisy multi-label CXR labels，说明传统multi-class noisy-label learning难以直接适配胸片多标签场景。Ye et al. (2026)提出label-wise reliability-aware classifier，并指出tail classes容易被粗粒度噪声检测方法误伤。这些研究与本课题非常接近，但它们主要关注噪声标签修正和鲁棒训练，而本研究关注的是如何用uncertainty profile预测U-Zero、U-One、U-Soft或U-Ignore等策略选择。

第四类文献说明长尾分布是本研究不能忽视的背景。Holste et al. (2022)和Holste et al. (2024)表明胸片疾病分类具有显著long-tailed distribution，罕见疾病标签在整体指标中容易被掩盖。Lin et al. (2025)的CXR-LT 2024进一步扩展了rare findings和zero-shot disease classification问题。与此同时，Cui et al. (2019)、Wu et al. (2020)和Ridnik et al. (2021)分别从class-balanced loss、distribution-balanced loss和asymmetric loss角度说明，不平衡和negative dominance会影响模型学习。由此可见，本研究中的teacher必须具备imbalance-aware设计，否则rare-label uncertainty profile可能被系统性误判。

第五类文献为teacher reliability提供依据。Guo et al. (2017)指出现代深度神经网络通常存在miscalibration问题；Rajaraman et al. (2022)说明在不平衡医学图像分类中，calibration与模型可靠性密切相关；Cheng and Vasconcelos (2024)进一步指出multi-label DNN calibration本身是独立问题，常见multi-label losses不一定产生可信概率。因此，本研究不会直接把teacher probability当成最终标签，而是将使用P/N separability、validation AUPRC、ECE和Brier score判断teacher对每个label是否可靠。

最后，分布相似度和统计检验文献支撑本研究的方法选择。Rubner et al. (2000)提出的Earth Mover's Distance说明分布之间的整体形状差异可以比简单均值或逐bin比较更有解释力；Damodaran et al. (2018)展示最优传输思想可用于深度表示分布对齐；Mann and Whitney (1947)提出的非参数检验适用于不假设正态分布的两组样本比较。由于teacher sigmoid scores常常偏态、长尾或两端极化，本研究使用Wasserstein distance、overlap ratio和Mann-Whitney U test来构建label-wise uncertainty profile具有明确的方法学依据。

# CHAPTER 3
RESEARCH METHODOLOGY

## 3.1 Research Framework

本研究将采用定量实验研究方法。整体流程如图3.1所示：首先在CheXpert训练集上统计每个label的positive、negative和uncertain比例；随后训练一个imbalance-aware teacher model；再用teacher对不同标签状态样本输出sigmoid scores，并构建逐标签score distributions；最后使用非参数分布相似度和可靠性指标给每个label分配Type A/B/C/D画像，并据此训练profile-guided final model。

图3.1  本研究的逐标签不确定性画像与策略选择框架

## 3.2 Data Collection and Preprocessing

本研究将以CheXpert作为主要数据集，因为它直接提供14个胸片观察标签，并显式包含positive、negative、uncertain和blank状态。数据预处理将包括图像尺寸统一、强度归一化、训练/验证/测试划分确认、以及label matrix构建。对于每个label，本研究将分别统计P、N、U和missing样本数量，并计算uncertain ratio、positive prevalence、tail index和有效样本数。

在实验设置上，本研究将优先使用CheXpert官方或常见验证划分进行模型选择，并在可能条件下使用MIMIC-CXR-JPG作为外部验证补充。若计算资源有限，外部验证将作为可选实验，不作为完成proposal目标的必要条件。

## 3.3 Imbalance-aware Teacher Model

teacher model的目的不是作为最终SOTA模型，而是为每个label提供相对可靠的score distributions。因此，teacher训练将采用U-Ignore作为初始标签处理方式，即uncertain samples不参与该label的loss，以减少将不确定监督强行编码为0或1带来的偏差。为了应对类别不平衡，模型将比较普通BCE、class-balanced loss、distribution-balanced loss或asymmetric loss中的一种或多种轻量实现。

teacher是否可用于某个label的profile inference，将由validation AUPRC、P/N separability、ECE和Brier score共同判断。如果某个rare label的teacher性能和校准均较差，该label将不会被强行映射为U-One或U-Zero，而会被归为Type D并采用更保守的U-Ignore策略。

## 3.4 Label-wise Uncertainty Profiling

对每个label，teacher将分别输出三组样本的预测分数：definite positive samples、definite negative samples和uncertain samples。本研究将把这三组分数视为经验分布，而不是只比较均值。对于uncertain distribution与positive/negative distribution之间的关系，本研究将计算Wasserstein distance、distribution overlap ratio、median score difference和Mann-Whitney U test显著性。

若uncertain distribution更接近positive distribution，并且与negative distribution显著分离，则该label可能属于Type A；若uncertain distribution更接近negative distribution，则可能属于Type B；若uncertain distribution位于positive和negative之间或与两者均有高重叠，则可能属于Type C；若teacher本身无法可靠区分P/N或校准过差，则属于Type D。该划分将避免把所有uncertain labels统一处理为0、1或0.5。

## 3.5 Strategy Mapping

| Profile Type | 分布特征 | 建议策略 | 解释 |
| --- | --- | --- | --- |
| Type A | U更接近P；与N分离 | U-One或teacher-soft | uncertain样本很可能包含真实阳性证据。 |
| Type B | U更接近N；与P分离 | U-Zero | uncertain表达更可能来自谨慎报告而非明确病灶。 |
| Type C | U位于P/N之间；或高度重叠 | U-Soft | 标签语义确实模糊，硬编码0或1风险较高。 |
| Type D | teacher P/N不可分；或校准差 | U-Ignore | teacher不可靠时不应把其偏差写入最终标签。 |

表3.1  逐标签不确定性画像类型与策略映射

## 3.6 Model Training and Evaluation

final model将使用profile-guided labels进行训练，并与固定策略（all U-Zero、all U-One、all U-Ignore、all U-Soft）、teacher-soft/self-training策略以及oracle per-label best strategy进行比较。oracle只作为上限参考，即通过完整训练候选策略后为每个label选择验证集表现最好的策略；本研究方法的目标是用更少的候选训练成本接近该上限，并提供可解释的label-wise选择依据。

主要评价指标包括：

Classification performance：macro/micro AUROC、macro/micro AUPRC、per-label AUPRC和rare-label AUPRC。

Calibration：ECE、adaptive ECE和Brier score，重点观察rare labels与high-uncertainty labels。

Strategy prediction quality：与oracle per-label strategy的agreement，以及相对于oracle的regret。

Robustness analysis：不同teacher loss、不同random seed和不同profile threshold下的敏感性分析。

# CHAPTER 4
PRELIMINARY FINDINGS

## 4.1 Preliminary Results and Discussions

目前本研究的初步发现来自文献分析而非完整实验结果。已有文献共同表明：CheXpert式不确定标签不是普通缺失值或随机噪声；多标签胸片分类同时受到report-derived label discrepancy、long-tailed class imbalance和model miscalibration影响。因此，如果只报告固定策略的AUROC，proposal的研究贡献会较弱；更合理的方向是建立可解释的label-wise profiling，并把策略选择从后验比较推进到训练前预测。

## 4.2 Literature Findings

CheXpert已经证明不同疾病标签可能适合不同uncertainty handling strategies，因此gap不能写成“没人研究不确定标签”。

CheXbert、VisualCheXbert和labeler quality研究说明report-derived labels与image evidence之间存在可测量差异。

CXR-LT和LongTailCXR证明胸片多标签任务具有显著长尾分布，rare-label表现需要被单独评价。

校准研究说明teacher probability可能不可靠，因此本研究必须加入ECE、Brier和P/N separability检查。

Wasserstein distance、overlap ratio和Mann-Whitney U test适合用于非正态、偏态或两端极化的score distribution比较。

## 4.3 Significance of Findings

本研究的意义在于把uncertain-label handling从单纯标签编码问题转化为逐标签语义与可靠性分析问题。若实验结果支持假设，本研究将能够说明：某个label的uncertain samples更接近positive、negative、ambiguous还是unreliable，并据此选择处理策略。这种解释比单纯报告某个固定策略得分更高更适合作为FYP Proposal的核心贡献。

## 4.4 Anticipated Results

预期profile-guided strategy不会在所有label上都超过oracle，因为oracle代表完整候选策略训练后的经验上限。但若本研究成功，profile-guided strategy应在整体macro AUPRC、rare-label AUPRC和calibration指标上优于多数固定策略，并在strategy agreement和regret方面接近oracle。对于teacher unreliable的Type D标签，采用U-Ignore预期将比盲目teacher-soft更稳健。

## 4.5 Conclusion

综上，本proposal提出了一种面向CheXpert-style imbalanced multi-label CXR classification的label-wise uncertainty profiling框架。该框架以已有文献中的真实缺口为基础：现有研究能够通过训练后比较发现不同label偏好的不确定标签策略，但缺少训练前、可解释、结合长尾与校准可靠性的策略预测机制。后续研究将围绕teacher训练、distribution profiling、strategy mapping和final model evaluation四个环节展开。

# References

Irvin, J., Rajpurkar, P., Ko, M., Yu, Y., Ciurea-Ilcus, S., Chute, C., Marklund, H., Haghgoo, B., Ball, R., Shpanskaya, K., Seekins, J., Mong, D. A., Halabi, S. S., Sandberg, J. K., Jones, R., Larson, D. B., Langlotz, C. P., Patel, B. N., Lungren, M. P., & Ng, A. Y. (2019). CheXpert: A large chest radiograph dataset with uncertainty labels and expert comparison. AAAI.

Oakden-Rayner, L., Dunnmon, J., Carneiro, G., & Re, C. (2019). Hidden stratification causes clinically meaningful failures in machine learning for medical imaging.

Jain, S., Agrawal, A., Saporta, A., Truong, S. Q. H., Duong, D. N., Bui, T., Chambon, P., Zhang, Y., Lungren, M. P., Ng, A. Y., Langlotz, C. P., & Rajpurkar, P. (2021a). VisualCheXbert: Addressing the discrepancy between radiology report labels and image labels. CHIL.

Jain, S., Agrawal, A., Saporta, A., Truong, S. Q. H., Duong, D. N., Bui, T., Chambon, P., Zhang, Y., Lungren, M. P., Ng, A. Y., Langlotz, C. P., & Rajpurkar, P. (2021b). Effect of radiology report labeler quality on deep learning models for chest X-ray classification. arXiv.

Gao, J., et al. (2024). Multi-rater label uncertainty in chest radiograph classification for acute respiratory distress syndrome. Bioengineering.

Chen, B., Li, J., Guo, X., & Lu, G. (2020). DualCheXNet/CheXGCN-style label co-occurrence learning for multi-label chest X-ray classification. IEEE Journal of Biomedical and Health Informatics.

Cheng, J., & Vasconcelos, N. (2024). Calibrating deep neural networks for multi-label classification. CVPR.

Smit, A., Jain, S., Rajpurkar, P., Pareek, A., Ng, A. Y., & Lungren, M. P. (2020). CheXbert: Combining automatic labelers and expert annotations for accurate radiology report labeling using BERT. EMNLP.

Cui, Y., Jia, M., Lin, T. Y., Song, Y., & Belongie, S. (2019). Class-balanced loss based on effective number of samples. CVPR.

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. ICML.

Rajaraman, S., et al. (2022). Model calibration and reliability for class-imbalanced medical image classification. PLOS.

Pham, H. H., Le, T. T., Tran, D. Q., Ngo, D. T., & Nguyen, H. Q. (2021). Interpreting chest X-rays via CNNs that exploit hierarchical disease dependencies and uncertainty labels. Neurocomputing.

Ridnik, T., Ben-Baruch, E., Zamir, N., Noy, A., Friedman, I., Protter, M., & Zelnik-Manor, L. (2021). Asymmetric loss for multi-label classification. ICCV.

Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PLOS ONE.

Holste, G., et al. (2024). CXR-LT: Multi-label long-tailed classification on chest X-rays. Medical Image Analysis.

Lin, C., et al. (2025). CXR-LT 2024: Long-tailed and zero-shot disease classification on chest X-rays. arXiv.

Yang, Y., et al. (2019). Uncertainty-aware chest X-ray classification with Bayesian neural networks and uncertain labels.

Chen, Z., et al. (2023). BoMD: Bag of multi-label descriptors for noisy chest X-ray classification with report-derived labels. ICCV.

Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. The Annals of Mathematical Statistics.

Johnson, A. E. W., Pollard, T. J., Greenbaum, N. R., Lungren, M. P., Deng, C. Y., Peng, Y., Lu, Z., Mark, R. G., Berkowitz, S. J., & Horng, S. (2019). MIMIC-CXR-JPG, a large publicly available database of labeled chest radiographs. arXiv.

Ye, X., et al. (2026). Label-wise reliability-aware learning for robust multi-label chest X-ray classification. Expert Systems with Applications.

Holste, G., et al. (2022). LongTailCXR: A long-tailed multi-label benchmark for chest X-ray disease classification. MICCAI Workshop.

Wu, T., Huang, Q., Liu, Z., Wang, Y., & Lin, D. (2020). Distribution-balanced loss for multi-label classification in long-tailed datasets. ECCV.

Rubner, Y., Tomasi, C., & Guibas, L. J. (2000). The Earth Mover's Distance as a metric for image retrieval. International Journal of Computer Vision.

Damodaran, B. B., Kellenberger, B., Flamary, R., Tuia, D., & Courty, N. (2018). DeepJDOT: Deep joint distribution optimal transport for unsupervised domain adaptation. ECCV.

# Appendix

附录A  初步项目计划

| 阶段 | 时间 | 主要任务 | 交付物 |
| --- | --- | --- | --- |
| Phase 1 | Week 1-2 | 复核文献、确定实验标签和数据划分。 | 最终proposal与文献矩阵。 |
| Phase 2 | Week 3-5 | 完成CheXpert预处理、统计P/N/U分布和rare-label分组。 | 数据统计表与预处理脚本。 |
| Phase 3 | Week 6-8 | 训练imbalance-aware teacher并评估AUPRC/ECE/Brier。 | teacher checkpoint和可靠性报告。 |
| Phase 4 | Week 9-10 | 构建Wasserstein、overlap和Mann-Whitney U profile。 | label-wise profile表。 |
| Phase 5 | Week 11-13 | 训练profile-guided final model及固定策略基线。 | 实验结果和消融分析。 |
| Phase 6 | Week 14 | 整理结果、撰写FYP最终报告。 | 最终论文与答辩材料。 |
