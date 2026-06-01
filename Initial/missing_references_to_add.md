# 需要补充的缺失文献清单

Topic: **Label-wise Adaptive Uncertainty Soft Labeling for Imbalanced Multi-label Chest X-ray Classification**

用途：补齐当前 `E:\2026.04\Thesis\参考文献` 里还不够强的三块支撑：

1. **multi-label calibration**
2. **teacher / pseudo-label confidence reliability**
3. **CheXpert / CXR noisy-label 与 uncertain-label handling**
4. **multi-label imbalance loss**

结论先说：你当前文件夹里的文献已经够写 proposal，但如果要让 Chapter 2 和 methodology 更稳，建议优先下载并阅读下面 **8 篇核心补充文献**。

## 1. 最优先补充的 8 篇

| Priority | Paper | Year | Link / DOI | 补充哪一块缺口 | 为什么建议加入 |
|---:|---|---:|---|---|---|
| 1 | **Towards Calibrated Multi-label Deep Neural Networks** | 2024 | CVPR official: https://openaccess.thecvf.com/content/CVPR2024/html/Cheng_Towards_Calibrated_Multi-label_Deep_Neural_Networks_CVPR_2024_paper.html | Multi-label calibration | 这是目前最直接补你缺口的文献。它明确说 multi-label DNN calibration 被研究不足，并指出 asymmetric losses 虽然提升不平衡多标签性能，但不一定产生 well-calibrated probabilities。 |
| 2 | **Asymmetric Loss for Multi-Label Classification** | 2021 | CVF official: https://openaccess.thecvf.com/content/ICCV2021/html/Ridnik_Asymmetric_Loss_for_Multi-Label_Classification_ICCV_2021_paper.html | Multi-label imbalance loss | 这是 multi-label imbalance 的强 baseline。你的 CheXpert 是多标签，negative labels 远多于 positive labels，这篇可以支撑为什么普通 BCE 不够。 |
| 3 | **Combating Medical Noisy Labels by Disentangled Distribution Learning and Consistency Regularization** | 2022 | ScienceDirect: https://www.sciencedirect.com/science/article/abs/pii/S0167739X22004228 | CheXpert noisy / uncertain labels | 这篇很贴近你的方向：医学图像 noisy labels、hard-soft label learning、consistency regularization，并在 CheXpert 上报告提升。适合支撑“soft label + noisy label robustness”。 |
| 4 | **Label-wise Reliability-aware Classifier for Robust Chest X-ray Multi-label Classification** | 2026 | DOI: https://doi.org/10.1016/j.eswa.2026.131438 | Label-wise reliability; tail-class vulnerability | 非常贴近你的 topic：report-derived noisy labels、tail classes、per-label reliability、CheXpert/PadChest/ChestX-ray14。注意当前记录显示最终卷期日期为 2026-05-25，属于在线可见/即将正式刊出文献。 |
| 5 | **Dynamic Correlation Learning and Regularization for Multi-Label Confidence Calibration** | 2024 | arXiv: https://arxiv.org/abs/2407.06844 | Multi-label confidence calibration | 用于补充 CVPR 2024 calibration 论文。它明确提出 Multi-Label Confidence Calibration，并强调 multi-label 中 label correlation 会影响 confidence reliability。 |
| 6 | **Semi-supervised Learning by Selective Training with Pseudo Labels via Confidence Estimation** | 2021 | arXiv: https://arxiv.org/abs/2103.08193 | Pseudo-label confidence reliability | 支撑 teacher-generated pseudo-label 不能全信，需要 confidence estimation / selective training。你的 teacher-guided soft labeling 可以引用它说明为什么要控制 teacher weight。 |
| 7 | **Meta Self-Refinement for Robust Learning with Weak Supervision** | 2023 | ACL Anthology PDF: https://aclanthology.org/2023.eacl-main.74.pdf | Noisy weak supervision; teacher error propagation | 这篇指出 weak supervision 中 teacher 可能拟合噪声并产生高置信错误 pseudo-label，导致 error propagation。很适合支撑你的 alpha / label prior 设计。 |
| 8 | **Classifier Calibration: A Survey on How to Assess and Improve Predicted Class Probabilities** | 2021 | arXiv: https://arxiv.org/abs/2112.10327 | Calibration survey | 用于 Chapter 2 里解释 calibration、ECE、Brier score、post-hoc calibration。比只引用 Guo 2017 更完整。 |

## 2. 每篇文献如何放进你的 FYP

| Paper | Relevance | 支撑位置 | 你可以怎么写 |
|---|---|---|---|
| Towards Calibrated Multi-label Deep Neural Networks | **Highly Relevant** | Evaluation metrics; Calibration method; Methodology discussion | “Recent work has shown that calibration in multi-label DNNs deserves special attention, because losses designed for imbalanced multi-label classification may improve accuracy but still produce poorly calibrated probabilities.” |
| Asymmetric Loss for Multi-Label Classification | **Highly Relevant** | Methodology; Baseline; Class imbalance | “Asymmetric loss is a strong multi-label imbalance baseline because it treats positive and negative labels differently, reducing the domination of abundant negative labels.” |
| Combating Medical Noisy Labels by Disentangled Distribution Learning and Consistency Regularization | **Highly Relevant** | Research gap; Methodology; Uncertain/noisy labels | “Medical CXR labels extracted from reports contain uncertainty and inconsistency; hybrid hard-soft label learning has been explored to improve robustness on CheXpert.” |
| Label-wise Reliability-aware Classifier for Robust CXR Multi-label Classification | **Highly Relevant** | Research gap; Label-wise method; Tail labels | “Recent CXR work shows that report-derived noisy labels can disproportionately harm tail classes and that per-label reliability modeling can improve robustness.” |
| Dynamic Correlation Learning and Regularization for Multi-Label Confidence Calibration | **Moderately to Highly Relevant** | Calibration; Multi-label confidence | “Multi-label calibration should consider label correlations, because multiple labels can co-exist and semantically confuse model confidence.” |
| Selective Training with Pseudo Labels via Confidence Estimation | **Moderately Relevant** | Teacher prediction reliability | “Pseudo-labels should be selected or weighted according to confidence, because incorrect pseudo-labels can degrade training.” |
| Meta Self-Refinement for Robust Learning with Weak Supervision | **Moderately Relevant** | Teacher-guided soft labeling; Weak supervision | “A fixed teacher trained on noisy weak labels may produce high-confidence wrong pseudo-labels, motivating adaptive or corrected teacher guidance.” |
| Classifier Calibration Survey | **Supporting** | Literature review; Calibration explanation | “Calibration evaluates whether predicted probabilities reflect empirical correctness, which is different from discrimination metrics such as AUROC.” |

## 3. 还可以选择性补充的文献

| Paper | Year | Link | 是否必须 | 用途 |
|---|---:|---|---|---|
| **Focal Loss for Dense Object Detection** | 2017 | CVF: https://openaccess.thecvf.com/content_iccv_2017/html/Lin_Focal_Loss_for_ICCV_2017_paper.html | 建议补 | 虽然不是 multi-label CXR，但它是 imbalance loss 的经典基础，可支撑 hard/easy example imbalance。 |
| **Confidence Regularized Self-Training** | 2019 | CVF PDF: https://openaccess.thecvf.com/content_ICCV_2019/papers/Zou_Confidence_Regularized_Self-Training_ICCV_2019_paper.pdf | 可选 | 说明 self-training 中 pseudo-label 可能 noisy，过度自信会导致 error propagation。 |
| **Robust Medical Image Classification from Noisy Labeled Data with Global and Local Representation Guided Co-training** | 2022 | arXiv: https://arxiv.org/abs/2205.04723 | 可选 | 医学图像 noisy-label robust learning，可用于背景，但不如 CheXpert-specific 文献直接。 |
| **Deep Learning for Condition Detection in Chest Radiographs: A Performance Comparison of Different Radiograph Views and Handling of Uncertain Labels** | 2023 | University page: https://researchprofiles.herts.ac.uk/en/publications/deep-learning-for-condition-detection-in-chest-radiographs-a-perf/ | 可选 | 使用 CheXpert 并处理 uncertain labels，可作为额外 CheXpert uncertainty 相关文献。 |
| **Expert Uncertainty and Severity Aware Chest X-Ray Classification by Multi-Relationship Graph Learning** | 2023 | arXiv: https://arxiv.org/abs/2309.03331 | 可选 | 支撑 expert uncertainty / severity-aware CXR classification，但方法可能偏复杂。 |
| **Limitations of Public Chest Radiography Datasets for Artificial Intelligence: Label Quality, Domain Shift, Bias and Evaluation Challenges** | 2025 | arXiv: https://arxiv.org/abs/2509.15107 | 可选 | 综述 public CXR datasets 的 label quality / uncertainty / bias / evaluation challenge。适合 discussion。 |

## 4. 按缺口对应关系整理

### 4.1 Multi-label calibration

最需要补：

1. **Towards Calibrated Multi-label Deep Neural Networks**
2. **Dynamic Correlation Learning and Regularization for Multi-Label Confidence Calibration**
3. **Classifier Calibration: A Survey on How to Assess and Improve Predicted Class Probabilities**

为什么重要：

- 你现在已有 Guo 2017 和 Rajaraman 2022，但 Guo 主要是 multi-class，Rajaraman 是 class-imbalanced medical image classification。
- 你的任务是 **multi-label CXR**，所以最好有一篇真正讲 multi-label calibration 的文献。
- CVPR 2024 那篇最关键，因为它还讨论了 asymmetric losses 与 calibration 的冲突，正好连接你的 imbalance + calibration 主题。

### 4.2 Teacher / pseudo-label confidence reliability

最需要补：

1. **Semi-supervised Learning by Selective Training with Pseudo Labels via Confidence Estimation**
2. **Meta Self-Refinement for Robust Learning with Weak Supervision**
3. **Confidence Regularized Self-Training**

为什么重要：

- 你的 proposed method 使用 `p_teacher(i,l)`。
- 但 teacher prediction 不一定可靠，尤其在 rare labels / high uncertainty burden labels 上。
- 所以你需要文献支持：pseudo-labels 可能 noisy，teacher confidence 需要估计、校准、筛选或降权。

### 4.3 CheXpert / CXR noisy-label and uncertain-label handling

最需要补：

1. **Combating Medical Noisy Labels by Disentangled Distribution Learning and Consistency Regularization**
2. **Label-wise Reliability-aware Classifier for Robust Chest X-ray Multi-label Classification**
3. **Deep Learning for Condition Detection in Chest Radiographs... Handling of Uncertain Labels**
4. **Expert Uncertainty and Severity Aware Chest-X-Ray Classification**

为什么重要：

- 你已有 CheXpert 原文、Pham label smoothing、Learn To Be Uncertain。
- 但还缺更近年、更直接把 CheXpert label uncertainty / noisy labels 作为训练问题处理的文献。
- 这些文献可以让你的 gap 更稳：不是泛泛说 uncertainty labels，而是说 **noisy/uncertain labels + tail labels + label-wise reliability**。

### 4.4 Multi-label imbalance loss

最需要补：

1. **Asymmetric Loss for Multi-Label Classification**
2. **Focal Loss for Dense Object Detection**
3. 已有的 **Class-Balanced Loss**
4. 已有的 **LDAM**

为什么重要：

- CheXpert 每个疾病标签都可以看成一个 binary classifier，但 positive/negative 极不平衡。
- Asymmetric Loss 比 LDAM 更贴近 multi-label setting。
- Focal Loss 可以作为 imbalance learning 的基础文献。

## 5. 我建议你下载到参考文献文件夹的优先顺序

如果你只想补最少数量，下载这 5 篇：

1. `Towards Calibrated Multi-label Deep Neural Networks`
2. `Asymmetric Loss for Multi-Label Classification`
3. `Combating Medical Noisy Labels by Disentangled Distribution Learning and Consistency Regularization`
4. `Label-wise Reliability-aware Classifier for Robust Chest X-ray Multi-label Classification`
5. `Semi-supervised Learning by Selective Training with Pseudo Labels via Confidence Estimation`

如果你想把 Chapter 2 写得更完整，再加：

6. `Dynamic Correlation Learning and Regularization for Multi-Label Confidence Calibration`
7. `Meta Self-Refinement for Robust Learning with Weak Supervision`
8. `Classifier Calibration: A Survey on How to Assess and Improve Predicted Class Probabilities`
9. `Focal Loss for Dense Object Detection`

## 6. 对你的 topic 的影响

补完这些文献后，你的 topic 会更稳，尤其是下面三句话可以更有依据：

1. **类别不平衡不仅影响分类性能，还可能影响 probability calibration。**  
   支撑：Rajaraman 2022 + Cheng & Vasconcelos 2024。

2. **multi-label setting 中，专门为 imbalance 设计的 loss 不一定带来可靠概率。**  
   支撑：Towards Calibrated Multi-label Deep Neural Networks。

3. **teacher prediction / pseudo-label 不能盲目信任，尤其在 noisy weak supervision 和 rare labels 下。**  
   支撑：Selective Training with Pseudo Labels + Meta Self-Refinement + Label-wise Reliability-aware CXR。

## 7. 建议更新后的 methodology 方向

建议你的 methodology 不要只写：

> Train teacher model and use its prediction as soft label.

应该改成：

> Train a teacher model to generate instance-level predictions for uncertain labels, but combine these predictions with a label-level uncertainty prior to reduce over-reliance on potentially miscalibrated or noisy teacher outputs, especially for rare and high-uncertainty-burden labels.

这句话会比单纯 U-SelfTrained 更强，因为它把三个文献线索连起来了：

- CheXpert: uncertain label handling
- CXR-LT / ASL: imbalance and rare labels
- Multi-label calibration / pseudo-label confidence: teacher prediction reliability

## 8. 最终建议

当前文件夹里的文献已经够交 proposal。  
如果要写正式 Chapter 2，我建议至少补充：

- **1 篇 multi-label calibration**：Towards Calibrated Multi-label Deep Neural Networks
- **1 篇 multi-label imbalance loss**：Asymmetric Loss
- **1 篇 CheXpert/CXR noisy-label handling**：Combating Medical Noisy Labels...
- **1 篇 label-wise reliability CXR**：Label-wise Reliability-aware Classifier...
- **1 篇 pseudo-label confidence**：Selective Training with Pseudo Labels...

这样你的 literature review 就不会只是“背景很多”，而是能直接支撑你的 proposed method。

