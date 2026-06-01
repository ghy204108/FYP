# Experiment Pipeline

This document describes the full pilot pipeline for label-wise uncertainty profiling on a CheXpert frontal-view subset.

## 1. Dataset Preparation

The pilot subset was created from CheXpert frontal-view images and split at patient level into:

| Split | Images |
|---|---:|
| Train | 13,205 |
| Profile validation | 4,377 |
| Test | 4,400 |

The selected labels are:

- Cardiomegaly
- Edema
- Consolidation
- Atelectasis
- Pneumothorax
- Pleural Effusion

The split design prevents patient leakage across train, profile validation, and test sets. The `profile_val` split is used for teacher reliability analysis, uncertainty profiling, threshold/rule application, and final-model checkpoint selection. The test split is reserved for held-out comparison.

## 2. Teacher/Probe Training

The teacher model is a DenseNet-121 initialized with ImageNet pretrained weights. It is trained with a U-Ignore policy:

| Raw label state | Target | Loss mask |
|---|---:|---:|
| Positive | 1.0 | 1 |
| Negative | 0.0 | 1 |
| Uncertain | 0.0 placeholder | 0 |
| Blank | 0.0 placeholder | 0 |

This avoids forcing uncertain labels into either positive or negative targets during the teacher stage.

The teacher is not treated as a diagnostic model or ground truth source. It is used as a distribution probe to generate score distributions for positive, negative, and uncertain samples.

Main outputs:

```text
Teacher_model/teacher_reliability_profile_val.csv
Teacher_model/teacher_profile_val_predictions.csv
Teacher_model/teacher_test_predictions.csv
Teacher_model/checkpoints/best_teacher.pt
```

Only the small reliability table is recommended for GitHub. The checkpoint and per-image prediction dumps are reproducible artifacts and can be kept local.

## 3. Label-wise Uncertainty Profiling

For each label, teacher scores on `profile_val` are separated by true state:

- definite positive
- definite negative
- uncertain

The profiling script computes:

- median and mean scores for P/N/U groups
- Wasserstein distance between uncertain and positive distributions
- Wasserstein distance between uncertain and negative distributions
- overlap ratios
- rank-biserial effect sizes
- teacher reliability indicators

The result is a Type A-D assignment:

| Type | Meaning | Strategy |
|---|---|---|
| Type A | positive-like uncertainty | U-One |
| Type B | negative-like uncertainty | U-Zero |
| Type C | ambiguous uncertainty | U-Soft |
| Type D | unreliable teacher evidence | U-Ignore |

Main outputs:

```text
uncertainty_profile/profile_features.csv
uncertainty_profile/strategy_mapping.csv
```

## 4. Final Model Comparison

Final models are trained using the same backbone and split but different uncertain-label strategies:

- U-Zero
- U-One
- U-Ignore
- Profile-guided

The all U-Soft baseline was not included in the current 5-epoch run, but it is recommended as a follow-up because the profile-guided mapping uses U-Soft for Pneumothorax.

During final-model evaluation, only definite positive and definite negative labels are used for metric computation. Uncertain and blank labels are masked out in validation/test metrics.

Main outputs:

```text
final_models/final_results_summary.csv
final_models/final_results_per_label.csv
```

## 5. Current Interpretation

The pipeline successfully produces non-trivial label-wise strategy assignments and completes held-out test evaluation.

The current results show that profile-guided strategy selection is better than U-Zero and slightly better than U-One, but U-Ignore remains the strongest baseline on the pilot subset. This indicates that teacher-score profiling is useful as an interpretable screening method, but the current rule set is not yet sufficient to reliably outperform a conservative fixed strategy.
