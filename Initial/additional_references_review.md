# Additional Reference Review for FYP Topic

Topic: **Adaptive Uncertainty Labeling for Imbalanced Multi-label Chest X-ray Classification**

本文件用于补充检查现有参考文献，并整理新找到的、建议加入 Chapter 2 Literature Review 的文献。重点不是堆论文，而是让每篇文献都能服务于你的研究逻辑：CheXpert uncertain labels、类别不均衡、多标签 CXR、teacher-guided soft labels、label-wise/group-wise evaluation。

## 1. 对现有参考文献的判断

总体判断：你当前 `E:\2026.04\Thesis\参考文献` 里的文献方向是合适的，已经覆盖了 FYP 的核心背景。但是还不够完整，尤其缺少三类支撑：

1. 自动 report labeler 质量与 image label discrepancy 的文献。
2. 多标签长尾分类里更直接的 loss/evaluation 文献。
3. 为什么不能只看 AUROC、为什么要做 group-wise / subgroup evaluation 的文献。

| 现有文件 | 是否适合 | 建议用途 | 注意点 |
|---|---|---|---|
| `1.CheXpert.pdf` | 非常核心 | 数据集、uncertain label 定义、U-Zero/U-One/U-Ignore/U-SelfTrained/U-MultiClass baseline | 必须承认 CheXpert 已经做过 selected labels 的 uncertainty strategy comparison，gap 不能写成“没人研究 uncertain labels” |
| `labelsmooth提升AUc.pdf` | 核心 | label smoothing 处理 uncertain labels、hierarchical disease dependency | 可以支撑 soft label 思路，但它主要追求 5 个 selected labels 的 AUC，不等于你的 adaptive/group-wise 研究 |
| `证明uncertainlabel有用.pdf` | 合适 | 说明 uncertain labels 不应简单丢弃，可用于学习 predictive uncertainty | 更适合作为 supporting evidence，不是主方法基线 |
| `长尾，多标签.pdf` / `长尾，标签不均衡.pdf` | 非常合适 | long-tailed multi-label CXR 背景，说明 rare labels 是真实挑战 | 可用于解释为什么你的 evaluation 要看 common/medium/rare，而不是只看 overall AUROC |
| `NeurIPS-2019-learning-imbalanced...LDAM.pdf` | 合适但偏通用 | long-tail learning 基础、margin/loss 角度 | 不是 CXR 专用，可作为 imbalance theory，不建议作为主实验方法 |
| `teacher model.pdf` | 合适 | teacher/student self-training、pseudo-label 思路 | 与 CheXpert U-SelfTrained 有关联，可支撑 teacher-guided soft target |
| `Mean Teacher`, `MixMatch`, `FixMatch` | 可辅助 | semi-supervised/pseudo-label/consistency learning 背景 | 这些不是你的主线，Chapter 2 不宜占太多篇幅，否则 topic 会被写偏成 semi-supervised learning |
| `When does label smoothing help?` | 合适 | soft targets、calibration、label smoothing 的理论背景 | 注意它是 multi-class classification 背景，不是 CheXpert-specific |
| `ChestX-Ray8`, `PadChest` | 合适 | CXR multi-label dataset 背景、report-derived label 问题 | 它们不直接提供 CheXpert-style uncertain label handling，所以作为背景即可 |

## 2. 现有文献的主要缺口

你的当前文献能说明“这个方向能做”，但还需要补强下面几条论证链：

| 需要证明的点 | 当前是否足够 | 需要补充什么 |
|---|---|---|
| report-derived labels 本身有噪声和不确定性 | 部分足够 | CheXbert、VisualCheXbert、labeler quality 文献 |
| 改善 labeler 或 label treatment 会影响 downstream CXR classifier | 不够 | Effect of Radiology Report Labeler Quality on Deep Learning Models |
| multi-label imbalance 需要专门 loss 或 evaluation | 部分足够 | Asymmetric Loss、Class-Balanced Loss、Focal Loss |
| rare-label evaluation 不能只用 AUROC | 不够 | Precision-Recall / AUPRC 文献 |
| group-wise analysis 有必要 | 不够 | hidden stratification、underdiagnosis bias 文献 |
| soft label / teacher prediction 需要可靠性讨论 | 部分足够 | calibration 文献 |

## 3. 建议新增文献

### 3.1 CheXbert: Combining Automatic Labelers and Expert Annotations for Accurate Radiology Report Labeling Using BERT

- Authors: Smit et al.
- Year: 2020
- Link: https://arxiv.org/abs/2004.09167
- 研究内容：提出 CheXbert，用 biomedically pretrained BERT 结合 rule-based labeler 和 expert annotations 来提升 radiology report labeling。
- 与 topic 的关系：你的 CheXpert labels 来自 report labeler。CheXbert 说明自动 report labeling 本身是一个重要问题，也说明 report-derived labels 不是绝对 ground truth。
- 建议放在：`Report-derived labels and label uncertainty` 小节。
- 可用于论证：uncertain labels 和 label noise 不是数据清洗小问题，而是 CXR image model training 的核心监督信号问题。

### 3.2 VisualCheXbert: Addressing the Discrepancy Between Radiology Report Labels and Image Labels

- Authors: Jain et al.
- Year: 2021
- Link: https://arxiv.org/abs/2102.11467
- 研究内容：指出 radiologists labeling reports 和 radiologists labeling images 会有差异，并提出 VisualCheXbert 让 report labels 更接近 image labels。
- 与 topic 的关系：你的方法本质上是在处理 uncertain/report-derived labels 与图像真实状态之间的不确定映射。这篇能支撑“report uncertainty 不一定等于 image truth uncertainty”。
- 建议放在：`Limitations of report-derived supervision` 小节。
- 可用于论证：把 `-1` 统一变成 0/1/ignore 会过于粗糙，因为 report label 和 image label 之间存在系统性 discrepancy。

### 3.3 Effect of Radiology Report Labeler Quality on Deep Learning Models for Chest-X-Ray Interpretation

- Authors: Jain, Smit, Ng, Rajpurkar
- Year: 2021
- Link: https://arxiv.org/abs/2104.00793
- 研究内容：比较 CheXpert、CheXbert、VisualCheXbert labelers，并研究不同 report labeler 质量对 downstream CXR classifier 的影响。
- 与 topic 的关系：直接支持你的研究动机：训练标签如何处理会影响最终 CXR classifier。
- 建议放在：`Why uncertainty label handling matters` 小节。
- 可用于论证：你的 adaptive uncertainty soft labeling 不是只改标签格式，而是在改进训练监督信号。

### 3.4 Asymmetric Loss for Multi-Label Classification

- Authors: Ridnik et al.
- Year: 2021
- Link: https://openaccess.thecvf.com/content/ICCV2021/html/Ridnik_Asymmetric_Loss_for_Multi-Label_Classification_ICCV_2021_paper.html
- 研究内容：提出 ASL，对 positive 和 negative samples 使用不同的 loss 调制，解决 multi-label classification 中 negative labels 过多、positive labels 稀疏的问题。
- 与 topic 的关系：CheXpert 是 multi-label setting，每个 label 都有大量 negative。ASL 可作为 imbalance-aware baseline 或 discussion。
- 建议放在：`Imbalanced multi-label learning` 小节。
- 可用于论证：multi-label imbalance 不能只靠普通 BCE，需要考虑 positive/negative asymmetry。

### 3.5 Class-Balanced Loss Based on Effective Number of Samples

- Authors: Cui et al.
- Year: 2019
- Link: https://openaccess.thecvf.com/content_CVPR_2019/html/Cui_Class-Balanced_Loss_Based_on_Effective_Number_of_Samples_CVPR_2019_paper.html
- 研究内容：提出 effective number of samples，用更稳定的 class re-weighting 处理 long-tailed classification。
- 与 topic 的关系：可支撑你对 rare labels 加权或分组评估的合理性。
- 建议放在：`Class imbalance and long-tail learning` 小节。
- 可用于论证：rare labels 的问题不是简单样本少，而是有效监督信息不足。

### 3.6 Focal Loss for Dense Object Detection

- Authors: Lin et al.
- Year: 2017
- Link: https://openaccess.thecvf.com/content_iccv_2017/html/Lin_Focal_Loss_for_ICCV_2017_paper.html
- 研究内容：提出 Focal Loss，通过降低 easy negatives 的影响，让模型更关注 hard examples。
- 与 topic 的关系：虽然原文是 object detection，但它是 class imbalance loss 的经典基础；在 CXR multi-label binary heads 中也常被借鉴。
- 建议放在：`Imbalance-aware losses` 小节。
- 可用于论证：类别不均衡会让训练被多数/easy samples 主导。

### 3.7 The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets

- Authors: Saito and Rehmsmeier
- Year: 2015
- Link: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432
- 研究内容：分析在 imbalanced datasets 中 PR curve 通常比 ROC curve 更能反映 classifier 对 positive class 的实际表现。
- 与 topic 的关系：你的 proposal 计划加入 AUPRC、F1、Recall，这篇是最直接的评价指标依据。
- 建议放在：`Evaluation metrics for imbalanced labels` 小节。
- 可用于论证：CheXpert 原文主要看 AUROC，而你的 FYP 对 rare/high-uncertainty labels 需要补充 AUPRC/F1/Recall。

### 3.8 On Calibration of Modern Neural Networks

- Authors: Guo et al.
- Year: 2017
- Link: https://proceedings.mlr.press/v70/guo17a.html
- 研究内容：系统讨论现代神经网络 confidence calibration，并提出 temperature scaling 作为简单有效的校准方法。
- 与 topic 的关系：你的 teacher-guided soft label 使用 teacher prediction，teacher 的概率是否可靠会影响 soft target。
- 建议放在：`Reliability of teacher predictions` 或 optional `Calibration analysis` 小节。
- 可用于论证：teacher probability 不能盲目信任，因此你的 label-level prior 和 alpha 控制是合理的。

### 3.9 Deep Learning Model Calibration for Improving Performance in Class-Imbalanced Medical Image Classification Tasks

- Authors: Rajaraman, Ganesan, Antani
- Year: 2022
- Link: https://doi.org/10.1371/journal.pone.0262838
- 研究内容：研究 class-imbalanced medical image classification 中模型校准和 performance 的关系。
- 与 topic 的关系：比 Guo et al. 更贴近医学图像和不平衡场景。
- 建议放在：`Medical image reliability and calibration` 小节。
- 可用于论证：如果时间允许，ECE/Brier score 可作为 secondary evaluation，而不是主贡献。

### 3.10 Hidden Stratification Causes Clinically Meaningful Failures in Machine Learning for Medical Imaging

- Authors: Oakden-Rayner et al.
- Year: 2020
- Link: https://arxiv.org/abs/1909.12475
- 研究内容：说明 overall model performance 可能掩盖 clinically meaningful subgroups 的失败。
- 与 topic 的关系：你的 common/medium/rare 和 high/low uncertainty-burden group-wise evaluation 正是为了避免 overall metrics 掩盖 tail-label failure。
- 建议放在：`Group-wise evaluation and hidden failure modes` 小节。
- 可用于论证：只报告 macro/micro average 不足以说明模型是否真正改善了困难标签。

### 3.11 Underdiagnosis Bias of Artificial Intelligence Algorithms Applied to Chest Radiographs in Under-served Patient Populations

- Authors: Seyyed-Kalantari et al.
- Year: 2021
- Link: https://www.nature.com/articles/s41591-021-01595-0
- 研究内容：研究 CXR AI 在不同人群中可能出现 underdiagnosis bias。
- 与 topic 的关系：它不是 uncertainty label handling 论文，但能支持“医学影像模型需要 subgroup-level analysis”的论点。
- 建议放在：`Why average performance is insufficient` 小节。
- 可用于论证：医学 AI 中平均性能好不代表每个 subgroup/label group 都可靠。

### 3.12 MIMIC-CXR-JPG, a Large Publicly Available Database of Labeled Chest Radiographs

- Authors: Johnson et al.
- Year: 2019
- Link: https://arxiv.org/abs/1901.07042
- 研究内容：发布 MIMIC-CXR-JPG，包含大量 CXR 图像和由 report labelers 生成的 14 个 structured labels。
- 与 topic 的关系：可作为 CheXpert 外的重要 CXR report-derived label dataset，也支撑 CXR-LT 的数据来源背景。
- 建议放在：`Large-scale report-derived CXR datasets` 小节。
- 可用于论证：report-derived multi-label CXR 是领域常见设置，CheXpert 不是孤例。

### 3.13 VinDr-CXR: An Open Dataset of Chest X-rays with Radiologist's Annotations

- Authors: Nguyen et al.
- Year: 2022
- Link: https://www.nature.com/articles/s41597-022-01498-w
- 研究内容：提供 radiologist-annotated CXR 数据集，包含多种 findings/diagnoses 和人工标注流程。
- 与 topic 的关系：可用于对比 report-derived labels 与 expert image annotations 的不同价值。
- 建议放在：`CXR datasets and annotation quality` 小节。
- 可用于论证：高质量人工标注昂贵，因此大规模数据常依赖 report-derived labels，也就必须认真处理 label uncertainty。

## 4. 建议的 Chapter 2 结构

建议你不要按“每篇论文一段”写，而按下面逻辑组织：

1. **CXR multi-label classification and report-derived datasets**
   - ChestX-ray8, PadChest, CheXpert, MIMIC-CXR-JPG, VinDr-CXR。
2. **Uncertain labels in CheXpert**
   - CheXpert 原文、Pham label smoothing、Bayesian uncertainty paper。
3. **Label quality and report-image label discrepancy**
   - CheXbert、VisualCheXbert、labeler quality paper。
4. **Imbalanced and long-tailed multi-label CXR**
   - CXR-LT, LDAM, Class-Balanced Loss, Focal Loss, ASL。
5. **Teacher-guided soft labels and pseudo-labeling**
   - U-SelfTrained from CheXpert, Mean Teacher, Noisy Student；MixMatch/FixMatch 只简短带过。
6. **Evaluation under imbalance and hidden failure modes**
   - AUPRC/PR curve paper, hidden stratification, underdiagnosis bias。
7. **Research gap synthesis**
   - CheXpert 已经比较 selected labels 的 uncertainty strategies。
   - 但对于 full imbalanced multi-label setting，label prevalence、uncertainty burden、uncertain/positive ratio 与 uncertainty strategy sensitivity 的关系仍缺少系统分析。
   - 因此你的方法提出 teacher-guided label-wise adaptive uncertainty soft labeling，并用 label-wise/group-wise metrics 评估。

## 5. 最推荐新增到核心文献的 8 篇

如果 Chapter 2 篇幅有限，优先加入这 8 篇：

| 优先级 | 文献 | 为什么必须加 |
|---|---|---|
| 1 | CheXbert | 支撑 report-derived labels 和 labeler quality |
| 2 | VisualCheXbert | 支撑 report labels 与 image labels 的 discrepancy |
| 3 | Effect of Report Labeler Quality | 直接证明 labeler/label quality 会影响 downstream CXR classifier |
| 4 | Asymmetric Loss | 最贴近 multi-label imbalance 的 loss 文献 |
| 5 | Class-Balanced Loss | 支撑 rare-label weighting |
| 6 | Saito and Rehmsmeier 2015 | 支撑 AUPRC/F1/Recall 的评价选择 |
| 7 | Guo et al. 2017 | 支撑 teacher prediction calibration 问题 |
| 8 | Hidden Stratification | 支撑 group-wise evaluation 的必要性 |

## 6. 可直接写进 proposal 的文献缺口表述

Existing studies have established CheXpert as a large-scale CXR dataset with explicit uncertainty labels and have compared several uncertainty handling strategies for selected clinically important labels. Other studies have shown that label smoothing, Bayesian uncertainty, self-training, and report labeler improvement can help exploit uncertain or report-derived labels. Meanwhile, recent CXR-LT benchmarks show that CXR classification is naturally long-tailed and multi-label, where rare findings require imbalance-sensitive metrics such as AUPRC, F1, and Recall.

However, less attention has been paid to how label prevalence and uncertainty burden jointly affect the sensitivity of uncertain label handling strategies across imbalanced multi-label CXR labels. In particular, existing CheXpert-style uncertainty handling has not been fully evaluated through common/medium/rare label groups and high/low uncertainty-burden groups. This project therefore proposes a teacher-guided label-wise adaptive uncertainty soft labeling method that combines label-level uncertainty burden with instance-level teacher predictions.
