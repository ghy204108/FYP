# FYP 文献适配性分析

Topic: **Adaptive Uncertainty Labeling for Imbalanced Multi-label Chest X-ray Classification**

中文建议题目：**面向类别不平衡多标签胸片分类的自适应不确定标签处理方法研究**

分析范围：

- 本地参考文献目录：`E:\2026.04\Thesis\参考文献`
- 当前目录共读取到 22 个 PDF。
- 所有 PDF 均可读取首页/摘要级文本；没有发现完全无法读取的文件。
- 另外联网补充了近 5 年相关文献，重点放在 CheXpert uncertainty、report-derived labels、long-tailed multi-label CXR、calibration 和 label-wise reliability。

## 1. 总体判断

你的 topic **可行，而且文献基础已经比较扎实**。目前文献能支撑以下主线：

1. 胸部 X-ray 多标签分类是有研究价值的问题。
2. CheXpert 明确提供 uncertain labels，是你的核心数据集依据。
3. 现有研究已经比较过 U-Zero、U-One、U-Ignore、U-SelfTrained、U-MultiClass 等策略，所以你的 gap 不能写成“没人研究 uncertain label”。
4. 更清晰的 gap 应该是：**在 imbalanced multi-label setting 中，label prevalence、uncertainty burden、uncertain/positive ratio 如何共同影响 uncertain label handling，目前缺少系统研究。**
5. 你的 methodology 可以建立在 CheXpert uncertainty strategies、label smoothing、teacher/student pseudo-labeling、class-balanced loss、calibration evaluation 之上。

目前最需要补强的是：

- 更直接的 **multi-label imbalance loss** 文献，例如 Asymmetric Loss。
- 更直接的 **label-wise reliability / tail label noise** 文献。
- 更系统的 **calibration under imbalance** 和 **teacher prediction reliability** 文献。

## 2. 本地文献逐篇适配性分析

| Paper title | Year | Main contribution | Relevance to my topic | Which part of my FYP it supports | How I can use it in my literature review | Limitations / why it may not fully support my topic | Recommended citation sentence |
|---|---:|---|---|---|---|---|---|
| CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison | 2019 | 发布 CheXpert，包含 224,316 张胸片、14 个 observation labels，并显式标注 positive/negative/uncertain；比较 U-Ignore、U-Zero、U-One、U-SelfTrained、U-MultiClass。 | **Highly Relevant** | Dataset; Research background; Uncertainty / uncertain labels; Model / baseline; Methodology | 作为你的核心数据集和 baseline 依据。需要说明 CheXpert 已经证明不同 pathology 适合不同 uncertainty handling strategy。 | CheXpert 主要围绕 5 个 competition labels 和 AUROC 展开；没有系统分析 full imbalanced label set 中 prevalence 与 uncertainty burden 的交互影响。 | Irvin et al. (2019) introduced CheXpert as a large-scale CXR dataset with explicit uncertainty labels and showed that different pathologies benefit from different uncertainty handling strategies. |
| Interpreting chest X-rays via CNNs that exploit hierarchical disease dependencies and uncertainty labels | 2021 | 使用 CheXpert 训练多标签 CXR classifier，结合 disease hierarchy 和 label smoothing regularization 处理 uncertain samples。 | **Highly Relevant** | Methodology; Uncertainty / uncertain labels; Multi-label classification; Model / baseline | 可用于支持 soft label / label smoothing 对 uncertain labels 有价值，也可作为你 proposed soft-label strategy 的前置工作。 | 主要追求 high AUC 和 selected labels；没有针对 rare labels、uncertain/positive ratio 或 calibration 做系统研究。 | Pham et al. (2021) showed that label smoothing can be used to exploit uncertain labels in CheXpert-based multi-label CXR classification. |
| Learn To Be Uncertain: Leveraging Uncertain Labels In Chest X-rays With Bayesian Neural Networks | 2019 | 探索 radiology report uncertainty 与 Bayesian neural network predictive uncertainty 的关系，说明 uncertain labels 可帮助模型表达不确定性。 | **Highly Relevant** | Uncertainty / uncertain labels; Clinical AI reliability; Calibration-related motivation | 用于论证 uncertain labels 不应简单丢弃，因为它们包含诊断不确定性的信号。 | 偏 Bayesian uncertainty，不直接解决 long-tail imbalance；实验规模和方法深度有限。 | Yang et al. (2019) suggested that report-level uncertainty labels can help models produce more uncertainty-aware predictions rather than forcing overconfident binary decisions. |
| CXR-LT 2024: A MICCAI challenge on long-tailed, multi-label, and zero-shot disease classification from chest X-ray | 2025 | 总结 CXR-LT 2024 challenge，强调 CXR 中 long-tailed、multi-label、zero-shot disease classification 的挑战。 | **Highly Relevant** | Class imbalance / long-tail problem; Research gap; Evaluation metrics; Research significance | 用于证明 long-tailed multi-label CXR 是当前仍活跃的研究问题，rare labels 不能被 overall AUROC 掩盖。 | 重点是 challenge 和 zero-shot，不直接研究 CheXpert uncertain labels。 | Lin et al. (2025) demonstrated that long-tailed multi-label CXR classification remains a challenging and active benchmark problem. |
| Towards long-tailed, multi-label disease classification from chest X-ray: Overview of the CXR-LT challenge | 2024 | 提出/总结 CXR-LT challenge，聚焦 long-tailed multi-label thorax disease classification。 | **Highly Relevant** | Class imbalance / long-tail problem; Research value; Evaluation metrics | 用于支撑你的 common/medium/rare label grouping 和 macro/mAP/AUPRC 等指标选择。 | 数据主要基于 MIMIC-CXR/CXR-LT，不是 CheXpert uncertainty label handling。 | Holste et al. (2024) framed long-tailed multi-label CXR classification as a distinct challenge where rare diseases require dedicated evaluation. |
| Deep learning model calibration for improving performance in class-imbalanced medical image classification tasks | 2022 | 系统分析 class-imbalanced medical image classification 中 calibration 对模型性能和概率输出的影响。 | **Highly Relevant** | Calibration method; Clinical AI reliability; Class imbalance; Evaluation metrics | 非常适合支持你的附加评价：ECE、Brier score、reliability diagram；也可支撑“类别不平衡会影响置信度可靠性”。 | 不是 CheXpert uncertainty 专用；主要讨论 calibration，不直接提出 uncertain label strategy。 | Rajaraman et al. (2022) showed that calibration is important in class-imbalanced medical image classification because imbalance can bias predicted probabilities toward majority classes. |
| On Calibration of Modern Neural Networks | 2017 | 经典 calibration 论文，说明现代深度网络常常 poorly calibrated，并提出 temperature scaling。 | **Highly Relevant** | Calibration method; Clinical AI reliability; Teacher prediction reliability | 用于支撑 teacher prediction 不能盲目信任，soft target 中需要控制 teacher weight，或后续做 ECE/Brier。 | 非医学、非多标签、非 CheXpert；需要作为通用理论基础使用。 | Guo et al. (2017) established that high classification accuracy does not imply reliable probability calibration in modern neural networks. |
| The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets | 2015 | 说明 imbalanced datasets 中 PR curve / AUPRC 通常比 ROC 更能反映 positive class 表现。 | **Highly Relevant** | Evaluation metrics; Class imbalance / long-tail problem | 用于直接支撑你的评价指标：AUPRC、F1、Recall、Precision 不应缺席。 | 是通用 binary classification，不是 CXR；但对每个 CXR label 的 one-vs-rest evaluation 很适用。 | Saito and Rehmsmeier (2015) argued that precision-recall analysis is more informative than ROC analysis when positive samples are rare. |
| VisualCheXbert: Addressing the Discrepancy Between Radiology Report Labels and Image Labels | 2021 | 指出 report labels 与 image labels 存在 discrepancy，并提出 VisualCheXbert 改善 report-to-image label agreement。 | **Highly Relevant** | Research gap; Dataset; Uncertainty / uncertain labels; Clinical AI reliability | 用于说明 report-derived labels 不等于完美 image ground truth，uncertain labels 和 label quality 处理具有研究价值。 | 主要研究 report labeler，不直接训练你的 adaptive uncertainty strategy。 | Jain et al. (2021) showed that labels extracted from radiology reports may disagree with image-level expert labels, motivating more careful treatment of report-derived supervision. |
| CheXbert: Combining Automatic Labelers and Expert Annotations for Accurate Radiology Report Labeling Using BERT | 2020 | 使用 BERT 结合 rule-based labeler 和 expert annotations，提高 radiology report labeling。 | **Highly Relevant** | Dataset; Research background; Uncertainty labels; Label quality | 用于支撑 report-derived label quality 是 CXR AI 的核心问题。 | 不直接处理 image classifier 的 uncertain label training；偏 NLP labeler。 | Smit et al. (2020) demonstrated that improving radiology report labelers is important for generating more reliable supervision for CXR models. |
| Effect of Radiology Report Labeler Quality on Deep Learning Models for Chest-X-Ray Interpretation | 2021 | 比较 CheXpert、CheXbert、VisualCheXbert labelers，并证明 labeler quality 会影响 downstream CXR classifier。 | **Highly Relevant** | Research value / significance; Dataset; Uncertainty labels; Methodology motivation | 非常适合证明“标签处理方式会影响最终图像模型”，直接支撑你的 topic 价值。 | 研究重点是 labeler quality，不是 label-wise adaptive uncertainty soft labeling。 | Jain et al. (2021) found that better report labelers can lead to better downstream CXR image classifiers, showing that label quality directly affects model performance. |
| Hidden Stratification Causes Clinically Meaningful Failures in Machine Learning for Medical Imaging | 2020 | 说明 overall metrics 可能掩盖 clinically meaningful subgroups 的失败。 | **Moderately to Highly Relevant** | Evaluation metrics; Clinical AI reliability; Research gap | 用于支撑你做 label-wise、common/medium/rare、high uncertainty-burden group-wise evaluation。 | 不是 CheXpert uncertainty 或 class imbalance 专用，但评价思想非常相关。 | Oakden-Rayner et al. (2020) warned that aggregate medical imaging performance can hide clinically meaningful failures in important subgroups. |
| ChestX-ray8: Hospital-scale Chest X-ray Database and Benchmarks on Weakly-Supervised Classification and Localization | 2017 | 发布 ChestX-ray8/ChestX-ray14，推动大规模 report-mined CXR 多标签分类。 | **Moderately Relevant** | Research background; Dataset; Multi-label classification | 用于证明 CXR multi-label classification 是重要领域，也可介绍 weakly supervised report-derived labels。 | 没有 CheXpert-style uncertain labels；标签噪声问题较明显。 | Wang et al. (2017) established large-scale weakly supervised multi-label CXR classification as an important research direction. |
| PadChest: A large chest x-ray image dataset with multi-label annotated reports | 2020 | 发布包含大量 CXR、report labels、taxonomy 的多标签胸片数据集。 | **Moderately Relevant** | Research background; Dataset; Multi-label classification | 用于说明 CXR 多标签和 report-derived annotation 是广泛存在的问题。 | 不直接支持 CheXpert uncertainty handling；标签体系与 CheXpert 不完全一致。 | Bustos et al. (2020) provided further evidence that chest X-ray interpretation is naturally multi-label and depends heavily on report-derived annotations. |
| Class-Balanced Loss Based on Effective Number of Samples | 2019 | 提出基于 effective number of samples 的 class-balanced re-weighting。 | **Moderately to Highly Relevant** | Methodology; Class imbalance / long-tail problem; Model baseline | 可作为 rare label weighting 的方法依据，或作为 baseline/discussion。 | 主要是 multi-class long-tail classification，不是 multi-label CXR；需要改造成 per-label weighting。 | Cui et al. (2019) proposed class-balanced loss to address long-tailed data distributions by weighting classes according to the effective number of samples. |
| Learning Imbalanced Datasets with Label-Distribution-Aware Margin Loss | 2019 | 提出 LDAM 和 deferred re-weighting，改善 long-tailed recognition。 | **Moderately Relevant** | Class imbalance / long-tail problem; Methodology background | 用于理论上支撑 long-tail decision boundary / margin 问题。 | 主要用于 multi-class classification；直接迁移到 CheXpert multi-label BCE 不一定简单。 | Cao et al. (2019) showed that class imbalance affects decision boundaries and proposed margin-based training for long-tailed recognition. |
| When Does Label Smoothing Help? | 2019 | 分析 label smoothing 对泛化、校准和 distillation 的影响。 | **Moderately Relevant** | Methodology; Calibration method; Teacher prediction reliability | 用于解释 soft labels 可能改善校准，但也可能影响 teacher-student distillation。 | 是 multi-class 通用论文，不是 CXR，不是 uncertain labels；需要谨慎转述。 | Müller et al. (2019) showed that label smoothing can improve calibration but may reduce the informativeness of teacher logits for distillation. |
| Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results | 2017 | 提出 Mean Teacher，用 EMA teacher 生成 consistency targets。 | **Moderately Relevant** | Methodology; Teacher model; Pseudo-labeling | 可支撑 teacher-guided soft label 的思想来源，说明 teacher targets 可以稳定训练。 | 是 semi-supervised learning，不是 CXR uncertainty；不建议作为核心 gap 文献。 | Tarvainen and Valpola (2017) showed that teacher models based on weight averaging can provide stable targets for semi-supervised learning. |
| Self-training with Noisy Student improves ImageNet classification | 2020 | 使用 teacher 生成 pseudo labels，再训练 noisy student，提高 ImageNet 性能。 | **Moderately Relevant** | Methodology; Teacher model; Pseudo-labeling | 可作为 U-SelfTrained / teacher-guided relabeling 的通用方法依据。 | 非医学、非多标签；ImageNet 上的成功不等于 CheXpert 上一定有效。 | Xie et al. (2020) demonstrated that teacher-generated pseudo-labels can improve image classification when used to train a student model. |
| MixMatch: A Holistic Approach to Semi-Supervised Learning | 2019 | 结合 label guessing、MixUp、一致性正则的 semi-supervised learning 方法。 | **Slightly to Moderately Relevant** | Methodology background; Pseudo-labeling | 可少量用于 soft pseudo-label / label guessing 背景。 | 方法较复杂，与你的 FYP 主线不完全一致；不建议纳入主实验。 | Berthelot et al. (2019) used guessed soft labels for unlabeled data, providing background for soft pseudo-label training. |
| FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence | 2020 | 使用 weak augmentation 产生 high-confidence pseudo-label，并在 strong augmentation 上训练。 | **Slightly to Moderately Relevant** | Methodology background; Teacher/pseudo-label confidence | 可用于说明 pseudo-label confidence threshold 的思想。 | 你的 uncertain labels 不是 unlabeled data；FixMatch 可能让 topic 偏向 SSL。 | Sohn et al. (2020) highlighted the role of confidence-filtered pseudo-labels in semi-supervised learning. |
| Deep Learning for Medical Image Processing: Overview, Challenges and the Future | 2017/2018 | 综述深度学习在医学图像处理中的应用、挑战和未来方向。 | **Slightly Relevant** | Research background; Research significance | 可在 introduction 中一两句引用，说明医学影像 AI 的整体背景。 | 太宽泛，不能直接支撑你的 method、gap 或 CheXpert uncertainty。 | Razzak et al. provided a broad overview of deep learning challenges in medical image processing, including the dependence on expert interpretation and high-quality data. |

## 3. 按用途分类

### Core papers: 必须重点阅读和引用

| 文献 | 原因 |
|---|---|
| CheXpert | 你的核心数据集、uncertain label 定义、baseline strategy 全部来自这里。 |
| Pham et al. 2021 | 直接使用 CheXpert uncertainty labels，并用 label smoothing 支撑 soft-label 方向。 |
| Yang et al. 2019 | 证明 uncertain labels 可用于学习/表达模型不确定性。 |
| CXR-LT 2024 / CXR-LT 2025 | 支撑 long-tailed multi-label CXR 的研究价值。 |
| Rajaraman et al. 2022 | 支撑类别不平衡与 calibration / probability reliability 的关系。 |
| Guo et al. 2017 | calibration 理论基础。 |
| Saito and Rehmsmeier 2015 | 支撑不只使用 AUROC，还要使用 AUPRC / PR / F1 / Recall。 |
| VisualCheXbert / CheXbert / Labeler Quality | 支撑 report-derived labels、label quality、image-label discrepancy。 |

### Supporting papers: 可以用于背景或补充论证

| 文献 | 用法 |
|---|---|
| ChestX-ray8 | CXR 多标签弱监督分类背景。 |
| PadChest | 大规模多标签 CXR dataset 背景。 |
| Hidden Stratification | 支撑 subgroup / group-wise evaluation。 |
| Deep Learning for Medical Image Processing | Introduction 背景，少量使用。 |

### Methodology papers: 可以直接支撑实验方法

| 文献 | 可支撑的方法 |
|---|---|
| CheXpert | U-Zero、U-One、U-Ignore、U-SelfTrained、U-MultiClass baseline。 |
| Pham et al. 2021 | U-Soft / label smoothing。 |
| Class-Balanced Loss | label/group re-weighting。 |
| LDAM | long-tail margin/loss discussion。 |
| Mean Teacher | teacher prediction / stable target。 |
| Noisy Student | teacher-student pseudo-labeling。 |
| When Does Label Smoothing Help? | soft targets 与 calibration / distillation discussion。 |
| Guo et al. 2017 | temperature scaling、ECE、reliability diagram。 |
| Rajaraman et al. 2022 | calibration in imbalanced medical image classification。 |

### Weakly related papers: 相关性较弱，可少量使用或不用

| 文献 | 原因 |
|---|---|
| MixMatch | 太偏 semi-supervised learning，方法复杂，不是你的主线。 |
| FixMatch | 也是 SSL 主线，和 CheXpert uncertain label 不是同一问题。 |
| Deep Learning for Medical Image Processing | 背景太宽泛，不能支撑具体 gap。 |
| LDAM | 可讨论 long-tail，但直接用于 multi-label CheXpert 需要额外设计。 |

## 4. 这些文献能否回答你特别关注的问题

| 问题 | 是否能支持 | 主要支持文献 | 说明 |
|---|---|---|---|
| 胸部 X-ray 多标签分类是否有研究价值？ | **能，且很充分** | ChestX-ray8, PadChest, CheXpert, CXR-LT | 多个大型数据集和 challenge 都证明这是持续活跃的问题。 |
| 是否支持不只看 AUROC / AUPRC，还关注概率可靠性和校准？ | **能，但需要组织好论证** | Guo 2017, Rajaraman 2022, Yang 2019 | AUROC/AUPRC 衡量排序或分类性能，calibration 衡量概率可信度；二者不是一回事。 |
| 是否支持类别不平衡会影响模型置信度可靠性？ | **能** | Rajaraman 2022, Guo 2017, CXR-LT | Rajaraman 最直接：class-imbalanced medical image classification 中概率可能偏向 majority class。 |
| 是否能作为 methodology 参考，而不是只能作为背景？ | **能** | CheXpert, Pham 2021, Class-Balanced Loss, Mean Teacher, Noisy Student, Guo 2017 | 可以直接转化为 baseline、soft label、teacher prediction、calibration evaluation。 |

## 5. 近 5 年建议额外补充文献

以下是联网补充的近 5 年相关文献，建议加入 reference list。部分你已经下载到本地，仍列出官方链接方便引用。

| Paper | Year | DOI / arXiv / Official link | Why it is useful |
|---|---:|---|---|
| VisualCheXbert: Addressing the Discrepancy Between Radiology Report Labels and Image Labels | 2021 | https://arxiv.org/abs/2102.11467 | 支撑 report labels 与 image labels 的 discrepancy，是你的 uncertainty/label quality 动机。 |
| Effect of Radiology Report Labeler Quality on Deep Learning Models for Chest-X-Ray Interpretation | 2021 | https://arxiv.org/abs/2104.00793 | 直接证明 labeler quality 会影响 downstream CXR classifier。 |
| Asymmetric Loss for Multi-Label Classification | 2021 | DOI: 10.1109/ICCV48922.2021.00015；官方页：https://openaccess.thecvf.com/content/ICCV2021/html/Ridnik_Asymmetric_Loss_for_Multi-Label_Classification_ICCV_2021_paper.html | 建议补充。它非常适合作为 multi-label imbalance loss baseline / discussion。 |
| Deep learning model calibration for improving performance in class-imbalanced medical image classification tasks | 2022 | DOI: 10.1371/journal.pone.0262838；PubMed: https://pubmed.ncbi.nlm.nih.gov/35085334/ | 你关于 imbalance 与 calibration 的核心支撑。 |
| Towards long-tailed, multi-label disease classification from chest X-ray: Overview of the CXR-LT challenge | 2024 | DOI: 10.1016/j.media.2024.103224；arXiv: https://arxiv.org/abs/2310.16112 | 支撑 long-tailed multi-label CXR 的 research gap。 |
| Leveraging Multi-Annotator Label Uncertainties as Privileged Information for ARDS Detection in Chest X-ray Images | 2024 | DOI: 10.3390/bioengineering11020133；PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC10885868/ | 可补充“多标注者不确定性/label uncertainty 可作为监督信息”的医学 CXR 证据。 |
| CXR-LT 2024: A MICCAI challenge on long-tailed, multi-label, and zero-shot disease classification from chest X-ray | 2025 | arXiv: https://arxiv.org/abs/2506.07984 | 支撑最新 long-tail / zero-shot CXR 研究趋势。 |
| Label-wise reliability-aware classifier for robust chest X-ray multi-label classification | 2026 | DOI: 10.1016/j.eswa.2026.131438；ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0957417426003519 | 非常贴近你的 topic：label-wise reliability、tail-class vulnerability、report-derived noisy labels。建议重点读。 |
| Overview of the CXR-LT 2026 Challenge: Multi-Center Long-Tailed and Zero Shot Chest X-ray Classification | 2026 | arXiv: https://arxiv.org/abs/2602.22092 | 可作为最新背景，说明 long-tailed CXR 仍在扩展到 multi-center 和 open-world setting。 |

## 6. Missing papers needed

你目前还应补充以下类型的文献：

| 缺少类型 | 推荐关键词 | 为什么需要 |
|---|---|---|
| Multi-label imbalance loss | `asymmetric loss multi-label classification`, `focal loss multi-label classification`, `class-balanced loss multi-label medical imaging` | 支撑你的 weighted BCE / focal / ASL baseline。 |
| Label-wise noisy label learning | `label-wise reliability chest x-ray multi-label`, `partial label noise multi-label classification medical imaging` | 你的 topic 是 label-wise adaptive，不是 sample-wise denoising。 |
| Calibration for multi-label classification | `multi-label calibration neural networks`, `calibration sigmoid multi-label classification`, `expected calibration error multi-label` | Guo 是 multi-class，需要补 multi-label calibration。 |
| CheXpert uncertainty handling after 2021 | `CheXpert uncertain labels label smoothing`, `CheXpert uncertainty label handling U-Zero U-One U-Ignore`, `uncertain labels chest x-ray soft labels` | 找更贴近你方法的新论文。 |
| Teacher prediction reliability | `teacher student pseudo label calibration`, `confidence calibrated pseudo labels`, `self-training noisy labels calibration` | 支撑 teacher-guided soft target 中 teacher probability 的可信度问题。 |
| AUPRC / thresholding in medical imbalance | `AUPRC imbalanced medical image classification`, `precision recall rare disease classification`, `threshold tuning multi-label medical image` | 支撑 rare-label evaluation 和 threshold selection。 |

## 7. 对你的 topic、gap 和 methodology 的判断

### Topic 是否可行？

**可行。**  
CheXpert 有明确 uncertain labels，CXR-LT 说明 long-tailed multi-label CXR 是真实挑战，calibration 文献说明概率可靠性值得分析。你的 topic 不需要训练超大模型，只需要围绕 CheXpert 做清晰实验比较，适合 FYP。

### 目前文献支撑是否足够？

**基本足够，但还需要补强 3 类文献：**

1. Asymmetric Loss / Focal Loss 这类 multi-label imbalance loss。
2. Label-wise reliability / partial label noise 文献。
3. Multi-label calibration 文献。

### Research gap 是否清晰？

**清晰，但需要避免过度宣称。**

不建议写：

> Existing studies have not considered label-wise uncertainty handling.

更准确写法：

> CheXpert has compared several uncertainty handling strategies for selected clinically important labels. However, less attention has been paid to how label prevalence and uncertainty burden jointly affect uncertainty handling across imbalanced multi-label CXR labels, especially when evaluated with AUPRC, F1, Recall, and calibration metrics.

### Methodology 是否有足够文献支持？

**有。**

你的方法可以由以下文献链支撑：

- CheXpert：fixed uncertainty strategies。
- Pham 2021：label smoothing / soft labels。
- Noisy Student / Mean Teacher：teacher-guided pseudo-labeling。
- Class-Balanced Loss / ASL：class imbalance。
- Guo 2017 / Rajaraman 2022：calibration evaluation。
- Saito 2015：AUPRC / PR under imbalance。

## 8. 建议优化后的 research gap

建议写成：

> Existing CheXpert-based studies have shown that uncertain labels contain useful information and that different pathologies may benefit from different uncertainty handling strategies. However, most prior analyses focus on selected clinically important labels and primarily report discrimination metrics such as AUROC. In imbalanced multi-label CXR classification, labels differ greatly in positive prevalence, uncertain-label frequency, and uncertain-to-positive ratio. These differences may affect not only classification performance but also the reliability of predicted probabilities. Therefore, there remains a need to systematically analyze uncertainty handling under label imbalance and to design a label-wise adaptive soft-labeling strategy that combines label-level uncertainty burden with instance-level teacher predictions.

## 9. 建议优化后的 research objectives

1. To review existing studies on CheXpert uncertainty labels, multi-label CXR classification, long-tailed learning, pseudo-labeling, and model calibration.
2. To analyze the distribution of positive, negative, and uncertain labels in CheXpert, including label prevalence and uncertain-to-positive ratio.
3. To implement and compare fixed uncertainty handling strategies, including U-Zero, U-One, U-Ignore, and U-Soft.
4. To design a teacher-guided label-wise adaptive uncertainty soft labeling method that combines label-level uncertainty burden and instance-level teacher predictions.
5. To evaluate the proposed method using AUROC, AUPRC, F1, Precision, Recall, and optional calibration metrics such as ECE and Brier Score.
6. To conduct label-wise and group-wise analysis across common, medium, rare, and high-uncertainty-burden labels.

## 10. 建议 methodology direction

### Recommended main direction

使用题目：

> **Label-wise Adaptive Uncertainty Soft Labeling for Imbalanced Multi-label Chest X-ray Classification**

这个标题比原题更具体，也更容易让 examiner 看出你的 contribution。

### Experimental design

| Component | Recommended choice |
|---|---|
| Dataset | CheXpert |
| Model backbone | DenseNet121 or ResNet50 |
| Baselines | U-Zero, U-One, U-Ignore, U-Soft 0.5, U-SelfTrained |
| Proposed method | Label-wise Adaptive Uncertainty Soft Labeling |
| Label-level signal | positive prevalence, uncertain count, uncertain/positive ratio |
| Instance-level signal | teacher model prediction |
| Loss | Weighted BCE; optional ASL / focal loss as secondary baseline |
| Metrics | AUROC, AUPRC, F1, Precision, Recall |
| Calibration metrics | ECE, Brier Score, reliability diagram |
| Analysis | label-wise, common/medium/rare, low/high uncertainty burden |

### Proposed formula

For uncertain label of image `i` and disease label `l`:

```text
y_soft(i,l) = alpha_l * p_teacher(i,l) + (1 - alpha_l) * b_l
```

where:

- `p_teacher(i,l)` is the teacher model prediction.
- `b_l` is a label-level prior based on uncertainty burden.
- `alpha_l` controls how much the method trusts the teacher for each label group.

## 11. 最终建议

你的 topic 是合适的，不需要大改。建议把 contribution 写得更精准：

> 不是“首次研究 uncertain labels”，而是“在 CheXpert 已有 uncertainty strategy 基础上，进一步研究 label imbalance 和 uncertainty burden 如何影响 uncertain label handling，并提出 label-wise adaptive soft labeling”。

最推荐的最终题目：

> **Label-wise Adaptive Uncertainty Soft Labeling for Imbalanced Multi-label Chest X-ray Classification**

如果想更稳妥：

> **A Comparative Study of Adaptive Soft Labeling for Uncertain Labels in Imbalanced Multi-label Chest X-ray Classification**

建议你下一步重点读：

1. CheXpert
2. Pham et al. 2021
3. Rajaraman et al. 2022
4. Saito and Rehmsmeier 2015
5. VisualCheXbert
6. Effect of Report Labeler Quality
7. CXR-LT 2024 / 2025
8. Asymmetric Loss
9. Label-wise Reliability-aware Classifier for CXR

这些文献组合起来，已经足够支撑一个清晰、可实现、有研究价值的 FYP。

## 12. 本次联网使用的主要来源

- CheXbert: https://arxiv.org/abs/2004.09167
- VisualCheXbert: https://arxiv.org/abs/2102.11467
- Effect of Radiology Report Labeler Quality: https://arxiv.org/abs/2104.00793
- Asymmetric Loss: https://openaccess.thecvf.com/content/ICCV2021/html/Ridnik_Asymmetric_Loss_for_Multi-Label_Classification_ICCV_2021_paper.html
- CXR-LT 2024 overview: https://arxiv.org/abs/2310.16112
- CXR-LT 2024 MICCAI challenge paper: https://arxiv.org/abs/2506.07984
- Calibration in class-imbalanced medical image classification: https://pubmed.ncbi.nlm.nih.gov/35085334/
- Label-wise reliability-aware CXR classifier: https://www.sciencedirect.com/science/article/pii/S0957417426003519
- PR curve under imbalance: https://doi.org/10.1371/journal.pone.0118432
- Guo calibration paper: https://proceedings.mlr.press/v70/guo17a.html

