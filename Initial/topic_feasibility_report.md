# Topic Feasibility Report

## 0. Topic 优化结论

根据你对 CheXpert 原论文的进一步核对，以及 Chapter 2 Literature Review 和 Chapter 4 FYP Research Proposal Writing 两份课件要求，建议最终 topic 使用一个更简洁、更适合正式 FYP proposal 的题目：

> **Adaptive Uncertainty Labeling for Imbalanced Multi-label Chest X-ray Classification**

中文：

> **面向类别不平衡多标签胸片分类的自适应不确定标签处理方法研究**

这个修改非常重要。CheXpert 原论文已经比较了不同 uncertain label handling strategies，并且发现不同 pathology 适合不同策略。因此，本 FYP 不能声称“现有研究没有 label-wise uncertainty handling”。更准确的 gap 应该是：

> CheXpert 已经在 5 个 competition labels 上做了 per-label uncertainty strategy comparison，并包含 U-SelfTrained 这类模型预测重标方法。但对于 imbalanced multi-label setting 中不同 label prevalence 与 uncertainty burden 的交互影响，尤其是如何结合 label-level uncertainty burden 和 instance-level teacher prediction 来生成 adaptive soft targets，并用 AUPRC/F1/Recall 进行系统评价，仍然研究不足。

本 topic 依然保留你的原始大方向：

- chest X-ray classification；
- medical AI；
- multi-label classification；
- class imbalance / long-tail；
- 模型训练；
- 实验比较；
- 可靠性/置信度分析可作为附加评价。

主贡献应从“重复比较 U-Zero/U-One/U-Ignore”变成：

> 在 CheXpert 既有 uncertainty handling 基础上，系统分析 label imbalance 与 uncertainty burden 对 uncertain label handling 的影响，并设计一种 teacher-guided label-wise adaptive uncertainty soft labeling strategy。

## 1. 与两份课件要求的匹配性

### 1.1 Chapter 2 Literature Review 要求

课件要求 literature review 需要：

- 不是简单文献列表；
- 要建立 theoretical grounding；
- 要比较现有方法；
- 要找 connections、contradictions 和 gaps；
- 要创建 synthesis matrix；
- 要说明你的研究如何填补 gap；
- topic 不能太泛。

本 topic 符合这些要求，因为它不是泛泛研究 “CXR classification”，而是聚焦在：

- CheXpert uncertain labels；
- U-Zero / U-One / U-Ignore / U-Soft / U-SelfTrained；
- label-wise differences；
- long-tailed label distribution；
- label imbalance and uncertainty-burden sensitivity；
- adaptive label handling strategy。

### 1.2 Chapter 4 Research Proposal 要求

课件要求 proposal 回答：

- What are you proposing to do?
- Why do this research?
- How do you plan to proceed?

本 topic 的回答如下：

| Proposal 要素 | 本 topic 的对应 |
|---|---|
| Proposed Title | Adaptive Uncertainty Labeling for Imbalanced Multi-label Chest X-ray Classification |
| Problem | CheXpert 已做 5 个 competition labels 的策略比较和 U-SelfTrained，但 label imbalance 与 uncertainty burden 如何共同影响 uncertain label handling 仍缺乏系统研究 |
| Aim | 研究 imbalanced labels 对 uncertain label handling 的敏感性，并提出 teacher-guided adaptive soft labeling strategy |
| Objectives | 文献综述、数据统计、baseline 构建、固定策略比较、自适应策略设计、分组评价 |
| Methodology | CheXpert + DenseNet/ResNet + U-Zero/U-One/U-Ignore/U-Soft + Proposed Adaptive |
| Significance | 改善 imbalanced/high-uncertainty-burden label learning，并提供更细粒度的 uncertain label 处理思路 |
| Expected Outcome | 一个可复现实验框架和一个本科可实现的 label-wise adaptive strategy |

## 2. Topic 的核心意思

CheXpert 这类胸片数据集里，不是所有标签都明确是 positive 或 negative。放射报告中经常出现：

- possible pneumonia；
- cannot exclude edema；
- questionable atelectasis；
- likely pleural effusion。

这些表述说明医生或报告系统对某个 finding 不确定。CheXpert 会把这种情况标为 `-1`，即 **uncertain label**。

训练模型时，uncertain label 不能直接当普通标签用。常见处理方式包括：

| 策略 | 含义 |
|---|---|
| U-Zero | 把 uncertain 当作 0 |
| U-One | 把 uncertain 当作 1 |
| U-Ignore | uncertain 不参与 loss |
| U-Soft | uncertain 当作 0.5 或其他 soft value |
| U-SelfTrained | 先训练模型，再用模型预测作为 pseudo-label |
| U-MultiClass | 把 negative / positive / uncertain 当成三分类 |

CheXpert 原论文已经比较过这些方法，并且已经发现不同 pathology 适合不同策略。所以本 FYP 不能只做：

> 比较 U-Zero、U-One、U-Ignore 哪个更好。

也不能写成：

> 现有研究没有考虑 label-wise uncertainty handling。

你的研究要更进一步、更具体：

> CheXpert 原论文主要关注 5 个 competition labels，而你的研究关注 imbalanced multi-label setting：不同标签的 positive samples、uncertain samples 和 uncertain/positive ratio 差异很大，因此不同标签可能对 uncertain label handling strategy 有不同敏感性。你的方法不是再手动选择 U-One/U-Zero，而是对每个 uncertain 样本生成 soft label。

本项目中的 proposed method 可以命名为：

> **LAUSL: Label-wise Adaptive Uncertainty Soft Labeling**

它结合两类信息：

- **Label-level prior**：这个 label 的 uncertain burden 有多重，例如 uncertain/positive ratio；
- **Instance-level teacher prediction**：对于某一张具体胸片，teacher model 认为它像 positive 还是 negative。

最终每个 uncertain label 都会变成一个 0 到 1 之间的 soft target，而不是统一变成 0、1、ignore 或 0.5。

## 3. Research Gap

### 3.1 已有研究已经做了什么

已有研究已经覆盖：

- CheXpert 数据集构建和 uncertain labels；
- U-Zero、U-One、U-Ignore、U-SelfTrained、U-MultiClass 等基本策略；
- CheXpert 原论文已经对 5 个 competition labels 做了 per-label uncertainty strategy comparison，并为最终模型选择不同策略；
- label smoothing 处理 uncertain labels；
- Bayesian uncertainty 与 report uncertainty 的关系；
- CXR-LT benchmark 对 long-tailed multi-label CXR 的定义；
- report labeler 质量对 downstream image model 的影响；
- CXR label correlation。

### 3.2 仍然存在的 gap

真正的 gap 不是“uncertain labels 没有人研究”，而是：

1. **label imbalance 与 uncertainty burden 的交互影响没有被充分系统分析**  
   CheXpert 原论文重点分析 5 个 clinically important and prevalent competition labels。对于其他标签，尤其是 rare labels 或 uncertain/positive ratio 很高的 labels，uncertain label handling 的影响没有被同等系统地研究。

2. **敏感性不一定只由 rarity 决定**  
   rare labels 本来 positive samples 少，但某些 common labels 也可能有很高的 uncertain/positive ratio。因此，本研究不预设 rare labels 一定最敏感，而是同时分析 label prevalence 和 uncertainty burden。

3. **现有研究较少做 common / medium / rare group-wise evaluation**  
   CheXpert 原论文按 5 个 selected labels 比较策略，但没有从 long-tailed learning 的角度把 labels 分成 common、medium、rare，再系统比较每组对 uncertainty handling 的敏感性。

4. **imbalance-sensitive metrics 使用不足**  
   CheXpert 原论文主要使用 AUROC。对于 imbalanced labels，尤其是 rare labels，AUPRC、F1、Recall 和 Precision 通常更能反映学习效果。

5. **teacher-guided adaptive soft labeling 仍有本科可做空间**  
   CheXpert 的 U-SelfTrained 使用模型预测重标 uncertain labels，但没有显式结合 label-level uncertainty burden，也没有系统评价不同 prevalence/uncertainty-burden label groups。本项目可以将 teacher prediction 与 label-level prior 结合，为每个 uncertain sample 生成 instance-specific soft target。

### 3.3 推荐 gap 表述

可以在 proposal 中写成：

> The CheXpert study has already compared several uncertainty label handling strategies, such as U-Zero, U-One, U-Ignore, U-SelfTrained, and U-MultiClass, and showed that different selected pathologies benefit from different strategies. However, its main uncertainty-handling analysis focused on five clinically important and relatively prevalent competition labels, with AUROC as the primary metric. Less attention has been paid to how label prevalence and uncertainty burden jointly affect uncertainty handling in imbalanced multi-label CXR classification. Therefore, this project proposes a teacher-guided label-wise adaptive uncertainty soft labeling method that combines label-level uncertainty burden with instance-level teacher predictions, and evaluates its effect using label-wise, common/medium/rare, and high-uncertainty-burden group analyses.

中文：

> CheXpert 原论文已经比较了多种不确定标签处理策略，并发现不同 selected pathologies 适合不同策略。但其核心分析集中在 5 个临床重要且相对常见的 competition labels，并主要使用 AUROC。对于类别不平衡多标签胸片分类中不同 prevalence 和 uncertainty burden 的标签，不确定标签处理方式的影响仍缺乏系统研究。本项目进一步提出 teacher-guided adaptive soft labeling：既考虑每个标签整体的不确定负担，也考虑每张图像的模型预测信号。

## 4. Topic 可行性评分

| 评估项 | 分数 | 解释 |
|---|---:|---|
| 技术可行性 | 4/5 | U-Zero、U-One、U-Ignore、U-Soft、teacher model prediction 和 soft-label student training 都可用 PyTorch 实现。 |
| 数据可获得性 | 5/5 | CheXpert 天然包含 uncertain labels，是最匹配的数据集。 |
| 实现难度 | 3/5 | 比单纯分类复杂，但比 hard negative contrastive learning 更稳。 |
| 评价方法清楚度 | 5/5 | 可用 AUROC、AUPRC、F1、Precision、Recall、mAP，并按 common/medium/rare 分组。 |
| 创新性 | 4/5 | CheXpert 已做 selected label 的 strategy comparison 和 U-SelfTrained；本项目创新在于结合 label-level uncertainty prior 与 teacher instance prediction，并系统分析 label imbalance 和 uncertainty burden。 |
| 学术价值 | 4/5 | uncertain labels、label imbalance 与 long-tail labels 都是医学影像真实问题。 |
| 风险程度 | 2/5 | 风险低于 hard negative；主要风险是 adaptive strategy 提升不明显。 |
| 一年内完成 | 5/5 | 范围控制后非常适合一年内完成。 |
| 适合作为 CS/SE FYP | 4/5 | 有模型训练、算法规则设计、实验比较和清晰产出。 |

总体判断：**A-：推荐作为 FYP topic。**

## 5. 建议最终定题

### 5.1 最推荐题目

**Adaptive Uncertainty Labeling for Imbalanced Multi-label Chest X-ray Classification**

中文：

**面向类别不平衡多标签胸片分类的自适应不确定标签处理方法研究**

### 5.2 更稳妥版本

**Label-wise Adaptive Uncertainty Soft Labeling for Imbalanced Multi-label Chest X-ray Classification**

这个标题更宽一点，适合你还没完全确定 adaptive rule 的时候。

### 5.3 更偏实验研究版本

**A Comparative Study of Teacher-guided Soft Labeling for Uncertain Labels in Imbalanced Chest X-ray Classification**

这个更保守，但贡献感稍弱。

## 6. Proposal 框架

### 6.1 Problem Statement

Chest X-ray classification is commonly formulated as a multi-label learning task because a single radiograph may contain multiple abnormal findings. Public datasets such as CheXpert provide large-scale labels extracted from radiology reports, including uncertain labels that indicate ambiguous or equivocal findings.

The original CheXpert study has already compared several uncertainty label handling strategies, such as mapping uncertain labels to negative, mapping them to positive, ignoring them, using self-training, or modeling uncertainty as a separate class. It also showed that different selected pathologies benefit from different strategies. However, this analysis mainly focused on five clinically important competition labels and used AUROC as the primary evaluation metric.

In imbalanced multi-label CXR classification, disease labels have different positive sample counts and different uncertain-to-positive ratios. For rare labels, mapping uncertain labels to zero may suppress already scarce positive evidence, mapping them to one may introduce noise, and ignoring them may discard useful supervision. However, uncertainty sensitivity may not be determined by rarity alone, because some common labels may also have high uncertainty burden. Although self-training can use model predictions to relabel uncertain cases, relying only on teacher predictions may be unreliable for labels with limited or ambiguous supervision.

Therefore, this project proposes a teacher-guided label-wise adaptive uncertainty soft labeling method. The method combines a label-level uncertainty prior, derived from each label's uncertainty burden, with instance-level teacher predictions to generate soft targets for uncertain labels. The project evaluates whether this approach improves performance for imbalanced, rare, or uncertainty-sensitive labels using AUROC, AUPRC, F1, Precision, and Recall.

### 6.2 Aim

To investigate how uncertainty label handling affects imbalanced labels in multi-label chest X-ray classification and to design a teacher-guided label-wise adaptive soft labeling method for uncertain labels.

### 6.3 Objectives

1. To review studies on CheXpert uncertain labels, CXR multi-label classification, long-tailed learning, and uncertainty handling strategies.
2. To analyze the distribution of positive, negative, and uncertain labels in CheXpert, with emphasis on label prevalence, uncertain/positive ratio, and uncertainty burden.
3. To implement and compare fixed uncertainty handling strategies, including U-Zero, U-One, U-Ignore, and U-Soft.
4. To design and evaluate a teacher-guided label-wise adaptive uncertainty soft labeling strategy.
5. To assess the impact of different strategies using label-wise, common/medium/rare group-wise, and high-uncertainty-burden group metrics.

### 6.4 Research Questions

1. How do different uncertainty label handling strategies affect labels with different prevalence and uncertainty burden in multi-label CXR classification?
2. Is uncertainty-handling sensitivity better explained by label rarity, uncertain/positive ratio, or their interaction?
3. Can teacher-guided label-wise adaptive uncertainty soft labeling improve performance for imbalanced or uncertainty-sensitive labels compared with fixed strategies such as U-Zero, U-One, U-Ignore, U-Soft, and U-SelfTrained?

### 6.5 Scope

Included:

- CheXpert as the main dataset.
- 8-14 CheXpert labels, depending on computational resources.
- One backbone model, preferably DenseNet121 or ResNet50.
- Fixed strategies: U-Zero, U-One, U-Ignore, U-Soft.
- Proposed strategy: teacher-guided label-wise adaptive uncertainty soft labeling.
- Evaluation using label-wise, common/medium/rare group-wise, and uncertainty-burden group-wise metrics.
- Optional reliability analysis using ECE, Brier Score, and high-confidence error rate.

Excluded:

- Clinical diagnosis claims.
- Real hospital deployment.
- Doctor-in-the-loop study.
- Full report labeling model development.
- Training large foundation models.
- Full multi-dataset generalization.
- Complex Bayesian deep learning as the main method.

### 6.6 Methodology Overview

1. **Literature review and synthesis matrix**  
   Review CheXpert, uncertainty label handling, long-tailed CXR classification, label noise, and medical image reliability.

2. **Dataset preparation**  
   Use CheXpert. Extract label columns and identify positive, negative, and uncertain values.

3. **Label distribution analysis**  
   For each label, compute:
   - positive count;
   - negative count;
   - uncertain count;
   - label prevalence;
   - uncertainty ratio;
   - uncertain/positive ratio.

4. **Label grouping**  
   Group labels into common, medium, and rare based on positive prevalence.

5. **Baseline model**  
   Train DenseNet121 or ResNet50 with sigmoid multi-label outputs.

6. **Fixed uncertainty handling experiments**  
   Train models using:
   - U-Zero;
   - U-One;
   - U-Ignore;
   - U-Soft.

7. **Teacher model training**  
   Train a teacher model using a stable baseline strategy such as U-Soft 0.5 or U-Ignore with class/label weighting. The teacher is used to produce instance-level predictions for uncertain labels.

8. **Label-level prior construction**  
   For each label, compute an uncertainty burden score:

   ```text
   q_l = U_l / (P_l + epsilon)
   ```

   Then map it to a label-level prior `b_l`:

   | q_l value | Interpretation | b_l |
   |---:|---|---:|
   | q_l < 0.5 | low uncertainty burden | 0.7 |
   | 0.5 <= q_l < 2 | moderate uncertainty burden | 0.5 |
   | q_l >= 2 | high uncertainty burden | 0.3 |

   This prior does not claim to estimate the true probability. It controls whether uncertain labels for a disease should be used more aggressively or conservatively.

9. **Adaptive soft-label generation**  
   For each uncertain label of image `i` and disease label `l`, generate:

   ```text
   y_soft(i,l) = alpha_l * p_teacher(i,l) + (1 - alpha_l) * b_l
   ```

   where:

   - `p_teacher(i,l)` is the teacher model prediction;
   - `b_l` is the label-level uncertainty prior;
   - `alpha_l` controls how much the method trusts the teacher.

   A simple group-based setting is:

   | Label group | alpha_l |
   |---|---:|
   | common | 0.7 |
   | medium | 0.5 |
   | rare | 0.3 |

   This means teacher predictions are trusted less for rare labels because the teacher may also be weak on rare positives.

10. **Student model training**  
   Train the final student model using the generated soft labels:

   ```text
   target = 1.0, if original label is positive
   target = 0.0, if original label is negative
   target = y_soft(i,l), if original label is uncertain
   ```

   Use weighted BCE:

   ```text
   Loss = sum_l w_l * BCE(pred_l, target_l)
   ```

   with higher weights for rare labels if needed:

   | Label group | w_l |
   |---|---:|
   | common | 1.0 |
   | medium | 1.5 |
   | rare | 2.0 |

11. **Evaluation**  
   Evaluate all strategies using AUROC, AUPRC, F1, Precision, Recall, and mAP.

12. **Group-wise analysis**  
   Compare performance across common, medium, and rare labels, and also across low/medium/high uncertainty-burden labels. Focus on whether improvements are linked to rarity, uncertainty burden, or both.

13. **Optional reliability analysis**  
   Compute ECE, Brier Score, and high-confidence error rate to see whether adaptive uncertainty handling affects confidence reliability.

### 6.7 Proposed Method Variants

#### Variant A: LAUSL-lite

Use only label-level prior:

```text
uncertain target = b_l
```

This is the simplest version and can be used as an ablation.

#### Variant B: LAUSL-teacher

Use teacher prediction only:

```text
uncertain target = p_teacher(i,l)
```

This is close to self-training and acts as another ablation.

#### Variant C: LAUSL-full

Use both teacher prediction and label-level prior:

```text
y_soft(i,l) = alpha_l * p_teacher(i,l) + (1 - alpha_l) * b_l
```

This is the recommended main method.

Advantage: strongest empirical performance.  
Risk: more training cost and potential overfitting to validation.

Recommended path:

> Start with Design A + B combined. If time allows, compare with Design C as an upper-bound adaptive strategy.

### 6.8 Evaluation Plan

Main metrics:

- AUROC;
- AUPRC;
- F1-score;
- Precision;
- Recall / Sensitivity;
- mAP.

Group-wise metrics:

- common labels average;
- medium labels average;
- rare labels average.

Key focus:

- rare-label AUPRC;
- rare-label F1;
- rare-label Recall;
- whether adaptive strategy improves rare labels without harming common labels too much.

Optional reliability metrics:

- ECE;
- Brier Score;
- high-confidence false positive rate.

### 6.9 Expected Contribution

This project is expected to contribute:

1. A focused literature synthesis on uncertain label handling in CXR classification.
2. A label distribution analysis of positive, negative, and uncertain labels in CheXpert.
3. A systematic comparison of fixed uncertainty handling strategies across common, medium, and rare labels.
4. A teacher-guided label-wise adaptive uncertainty soft labeling strategy.
5. Evidence on whether uncertainty-handling sensitivity is associated with label rarity, uncertainty burden, or their interaction.

This contribution is stronger than simply training a CXR classifier, because the project directly addresses how label uncertainty should be handled under long-tailed multi-label conditions.

### 6.10 Potential Project Significance

Uncertain labels are common in radiology-report-derived CXR datasets. Treating all uncertain labels in the same way may be inappropriate because different disease labels have different prevalence and uncertainty distributions. This issue is especially important for imbalanced labels, including rare labels and labels with high uncertain/positive ratios.

This project can provide a practical and reproducible approach for analyzing and handling uncertain labels more carefully in long-tailed CXR classification. It does not claim clinical deployment, but it can improve understanding of how label uncertainty affects model training.

### 6.11 Tools and Technologies

- Python;
- PyTorch;
- torchvision or timm;
- pandas / NumPy;
- scikit-learn;
- torchmetrics;
- matplotlib / seaborn;
- optional: Jupyter Notebook;
- optional: Weights & Biases or TensorBoard.

### 6.12 Dataset Recommendation

Main dataset:

- **CheXpert**, because it explicitly includes uncertain labels and is directly aligned with the topic.

Possible extension:

- **CXR-LT**, as literature motivation for long-tailed multi-label CXR. It may not be necessary as the main dataset.

Not recommended as main dataset:

- NIH ChestX-ray14, because it does not provide CheXpert-style uncertain labels.

### 6.13 Proposed Gantt Chart

| Phase | Month | Main Activities | Output |
|---|---|---|---|
| 1 | Month 1 | Finalize topic, keywords, and research questions | Confirmed proposal direction |
| 2 | Month 2 | Literature review and synthesis matrix | Draft Chapter 2 |
| 3 | Month 3 | Obtain CheXpert, inspect labels, analyze uncertainty distribution | Label statistics and grouping |
| 4 | Month 4 | Implement DenseNet/ResNet baseline and U-Zero | First baseline results |
| 5 | Month 5 | Implement U-One, U-Ignore, U-Soft | Fixed strategy comparison |
| 6 | Month 6 | Design adaptive strategy based on prevalence and uncertainty ratio | Proposed method |
| 7 | Month 7 | Train adaptive strategy and tune thresholds | Proposed method results |
| 8 | Month 8 | Conduct label-wise and group-wise evaluation | Tables and figures |
| 9 | Month 9 | Optional reliability analysis and discussion | ECE/Brier/HCE results |
| 10 | Month 10 | Thesis writing, revision, presentation | Final report and slides |

### 6.14 Suggested Report Chapter Structure

1. Introduction
2. Literature Review
3. Research Gap and Problem Formulation
4. Methodology
5. Implementation
6. Experiments and Results
7. Discussion
8. Conclusion and Future Work

## 7. Alternative Topic Options

### Option 1: Recommended

**Adaptive Uncertainty Labeling for Imbalanced Multi-label Chest X-ray Classification**

- Best balance of feasibility and research contribution after considering CheXpert's existing per-label comparison.
- Directly uses CheXpert uncertainty labels.
- Avoids collision with hard negative literature.

### Option 2: Safer

**Label-wise Adaptive Uncertainty Soft Labeling for Imbalanced Multi-label Chest X-ray Classification**

- Slightly broader.
- Good if long-tail emphasis needs to be softened.

### Option 3: More empirical

**A Comparative Study of Teacher-guided Soft Labeling for Uncertain Labels in Imbalanced Chest X-ray Classification**

- Very feasible.
- Less method contribution.

### Option 4: More advanced

**Uncertainty-ratio-aware Soft Labeling for Long-tailed Multi-label Chest X-ray Classification**

- More method-specific.
- Requires careful design of soft-label values.

## 8. Final Recommendation

最终建议题目：

> **Adaptive Uncertainty Labeling for Imbalanced Multi-label Chest X-ray Classification**

这个 topic 比 hard negative 方向更适合你目前的 FYP，因为：

- CheXpert 天然提供 uncertain labels；
- CheXpert 已经做过 selected labels 的 per-label strategy comparison 和 U-SelfTrained，因此本项目的 gap 更精确地落在 label imbalance、label-level uncertainty burden 和 teacher-guided adaptive soft labels；
- 文献基础清楚；
- gap 不需要硬凑；
- 实现难度适中；
- 你仍然需要训练模型；
- 你有自己的 adaptive strategy；
- 可评价、可展示、可写 proposal；
- 符合两份课件对 literature review 和 research proposal 的要求。

一句话总结：

> CheXpert 已经证明不同 selected pathologies 适合不同 uncertain label strategies；本项目进一步关注 imbalanced labels 和 high-uncertainty-burden labels，结合 label-level uncertainty burden 和 teacher model prediction，为 uncertain labels 生成 adaptive soft targets，并用 AUPRC、F1、Recall 等 imbalance-sensitive metrics 进行评价。
