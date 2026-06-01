# Results

This directory contains the lightweight result tables from the current pilot experiment. Large artifacts such as checkpoints, per-image prediction dumps, raw CheXpert images, and row-level manifests with local paths are intentionally kept out of Git.

## Directory Layout

```text
teacher_model/
  README.md
  teacher_reliability_profile_val.csv

uncertainty_profile/
  README.md
  profile_features.csv
  strategy_mapping.csv

final_models/
  README.md
  final_results_summary.csv
  final_results_per_label.csv
```

Each subfolder has its own README with more detail. This page gives the overall reading of the pilot results.

## Pipeline Summary

The experiment follows three stages:

1. Train a U-Ignore teacher/probe model.
2. Use teacher scores on the profile validation split to assign each label to a Type A-D uncertainty profile.
3. Train final models under fixed strategies and the profile-guided strategy, then compare them on the held-out test split.

The pilot uses six CheXpert labels:

- Cardiomegaly
- Edema
- Consolidation
- Atelectasis
- Pneumothorax
- Pleural Effusion

## Teacher Reliability

The teacher was reliable for most labels, but not equally reliable across all findings.

| Label | AUPRC | AUROC | ECE | P/N median separation | Reading |
|---|---:|---:|---:|---:|---|
| Cardiomegaly | 0.9539 | 0.9023 | 0.0337 | 0.6429 | reliable |
| Edema | 0.8991 | 0.8765 | 0.0652 | 0.6362 | reliable |
| Consolidation | 0.8717 | 0.9223 | 0.0483 | 0.8769 | reliable |
| Atelectasis | 0.8722 | 0.6446 | 0.0665 | 0.0579 | unreliable separation |
| Pneumothorax | 0.6125 | 0.8060 | 0.0363 | 0.3239 | weaker but usable |
| Pleural Effusion | 0.9524 | 0.9433 | 0.0305 | 0.9245 | reliable |

The main warning is Atelectasis. Although its AUPRC is not low, its AUROC and P/N median separation show that the teacher does not separate positive and negative Atelectasis samples well. This matters because the profiling method should not make a strong U-One or U-Zero decision when the teacher evidence is weak.

## Uncertainty Profile Mapping

The profile stage produced the following label-wise strategy recommendations:

| Label | Profile type | Strategy | Reason |
|---|---|---|---|
| Cardiomegaly | Type A | U-One | uncertain samples are positive-like |
| Edema | Type A | U-One | uncertain samples are positive-like |
| Consolidation | Type A | U-One | uncertain samples are positive-like |
| Atelectasis | Type D | U-Ignore | teacher P/N separability is too weak |
| Pneumothorax | Type C | U-Soft | uncertain samples overlap both positive and negative groups |
| Pleural Effusion | Type A | U-One | uncertain samples are positive-like |

This mapping supports the main motivation of the project: uncertain labels are not homogeneous across pathologies. Most labels looked positive-like in the teacher score space, but Atelectasis and Pneumothorax required more conservative handling.

## Final Model Comparison

The final comparison used 5 training epochs. Test metrics were computed only on definite positive and definite negative labels; uncertain and blank labels were masked out during evaluation.

| Model | Test Macro AUPRC | Test Macro AUROC | Test Mean Brier | Test Mean ECE |
|---|---:|---:|---:|---:|
| U-Zero | 0.8300 | 0.8236 | 0.1757 | 0.1561 |
| U-One | 0.8538 | 0.8559 | 0.1322 | 0.0932 |
| U-Ignore | **0.8609** | **0.8616** | **0.1182** | **0.0522** |
| Profile-guided | 0.8554 | 0.8569 | 0.1261 | 0.0729 |

The profile-guided model improves over U-Zero and slightly outperforms U-One, but it does not beat U-Ignore. U-Ignore is the strongest overall baseline in this pilot.

## Per-label Reading

| Label | Best model | Profile-guided AUPRC | Comment |
|---|---|---:|---|
| Cardiomegaly | U-One | 0.9484 | profile-guided is close, but all U-One is best |
| Edema | U-Ignore | 0.9059 | U-Ignore is slightly better |
| Consolidation | U-Ignore | 0.8606 | U-Ignore is clearly better |
| Atelectasis | Profile-guided | **0.8977** | supports the reliability gate |
| Pneumothorax | U-Ignore | 0.5687 | Type C/U-Soft needs more validation |
| Pleural Effusion | U-Ignore | 0.9510 | U-Ignore is strongest |

The clearest supportive case is Atelectasis. The teacher reliability check marked it as unsafe for hard relabeling, the profile mapped it to U-Ignore, and the profile-guided model achieved the best Atelectasis AUPRC. This suggests that the Type D reliability gate is useful.

The less successful cases are mainly Type A labels. Cardiomegaly behaves as expected: U-One is best and profile-guided is close. However, Edema, Consolidation, and Pleural Effusion were also mapped to U-One, yet U-Ignore performed better in the final comparison. This suggests that being positive-like in teacher score space does not always mean that uncertain samples should be hard-coded as positive during final training.

Pneumothorax also needs further checking. It was mapped to Type C/U-Soft because uncertain samples overlapped both positive and negative distributions, but the current final comparison did not include an all U-Soft baseline. Without that baseline, it is difficult to isolate whether U-Soft itself was helpful.

## Overall Interpretation

The pilot result is mixed, but useful.

The profile-guided method is not simply random: it avoids the weakest fixed strategy, U-Zero, and performs slightly better than U-One. However, it does not outperform the conservative U-Ignore baseline. This means the current profiling rules provide interpretable evidence, but they are not yet strong enough to replace empirical strategy comparison.

The main methodological lesson is that teacher-score distribution similarity should be treated as evidence, not as a final decision by itself. A label can look positive-like in score space while still benefiting from U-Ignore during final training. The reliability gate appears valuable, but the Type A rule likely needs to become more conservative.

## Why the Profile-guided Result May Be Weaker Than U-Ignore

Several factors may explain why the profile-guided model did not beat U-Ignore in this pilot.

First, the pilot subset is deliberately reduced. The teacher and final models were trained on a frontal-only subset rather than the full CheXpert training set. This makes the experiment feasible, but it also means the teacher score distributions and final model behavior may be less stable, especially for labels with limited negative or uncertain support.

Second, the current profile rules assume that if uncertain samples look close to positives in teacher-score space, they can be treated as hard positives. The final results suggest that this is too aggressive. Positive-like uncertain samples may still contain report noise, weak evidence, or borderline cases. U-Ignore may lose some useful supervision, but it also avoids writing noisy labels into the final model.

Third, the experiment used a single split and a single training seed. The gap between U-Ignore and profile-guided is small, around 0.0055 macro AUPRC, so part of the difference may come from sampling and optimization variability.

Finally, U-Ignore is a strong baseline for report-derived medical labels. Its advantage in this pilot is not only AUPRC, but also calibration: it has the best Brier score and ECE. This suggests that conservative handling of uncertain labels can produce more reliable probabilities in the current setting.

## Next Steps

The next experiment should:

1. Add an all U-Soft final-model baseline.
2. Build a validation-oracle mapping from the fixed-strategy models.
3. Compute profile-guided agreement and regret against the validation oracle.
4. Refine the Type A rule so that positive-like uncertainty is not always mapped to hard U-One.
5. Repeat the comparison with multiple seeds if computation time allows.
