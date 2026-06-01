# Final Model Comparison

This folder contains the 5-epoch final model comparison between fixed uncertain-label strategies and the profile-guided strategy.

## Purpose

After the teacher-assisted uncertainty profile was generated, final models were trained using different uncertain-label handling strategies. The purpose was to test whether the profile-guided strategy improves held-out test performance compared with fixed strategies.

## Files

| File | Description |
|---|---|
| `final_results_summary.csv` | Macro-level validation and test metrics for each final model |
| `final_results_per_label.csv` | Per-label validation and test metrics for each final model |

Per-image prediction files and checkpoints are kept local and ignored by Git because they are large generated artifacts.

## Compared Strategies

| Model | Uncertain-label policy |
|---|---|
| `u_zero` | Treat all uncertain labels as 0 |
| `u_one` | Treat all uncertain labels as 1 |
| `u_ignore` | Mask all uncertain labels from the loss |
| `profile_guided` | Use label-wise strategies from `uncertainty_profile/strategy_mapping.csv` |

The all U-Soft baseline was not included in this run and is recommended as follow-up work.

## Overall Held-out Test Results

| Model | Test Macro AUPRC | Test Macro AUROC | Test Mean Brier | Test Mean ECE |
|---|---:|---:|---:|---:|
| U-Zero | 0.8300 | 0.8236 | 0.1757 | 0.1561 |
| U-One | 0.8538 | 0.8559 | 0.1322 | 0.0932 |
| U-Ignore | **0.8609** | **0.8616** | **0.1182** | **0.0522** |
| Profile-guided | 0.8554 | 0.8569 | 0.1261 | 0.0729 |

## Per-label Test AUPRC

| Label | U-Zero | U-One | U-Ignore | Profile-guided | Best |
|---|---:|---:|---:|---:|---|
| Cardiomegaly | 0.9211 | **0.9534** | 0.9449 | 0.9484 | U-One |
| Edema | 0.8644 | 0.9096 | **0.9097** | 0.9059 | U-Ignore |
| Consolidation | 0.8180 | 0.8497 | **0.8722** | 0.8606 | U-Ignore |
| Atelectasis | 0.8562 | 0.8908 | 0.8909 | **0.8977** | Profile-guided |
| Pneumothorax | 0.5654 | 0.5655 | **0.5876** | 0.5687 | U-Ignore |
| Pleural Effusion | 0.9548 | 0.9537 | **0.9599** | 0.9510 | U-Ignore |

## Interpretation

The profile-guided model improves over U-Zero and slightly outperforms U-One, but it does not outperform U-Ignore. U-Ignore is the strongest overall strategy in this pilot.

This is a mixed but useful result. It shows that the profile-guided strategy avoids the weakest fixed strategy, but the current decision rules are not strong enough to beat the conservative U-Ignore baseline.

The most supportive label-level result is Atelectasis. The profiling stage marked Atelectasis as Type D / U-Ignore because teacher reliability was weak, and profile-guided achieved the best test AUPRC for Atelectasis. This supports the value of the reliability gate.

The weaker results are mainly from Type A labels where uncertain samples looked positive-like, but U-Ignore still performed better in the final model. This suggests that score-distribution similarity alone is not sufficient to decide that uncertain labels should be hard-coded as positive.

## Stage Conclusion

The current pilot supports a cautious conclusion:

> Label-wise teacher-assisted uncertainty profiling provides interpretable evidence and improves over some fixed strategies, but it does not yet outperform the strongest fixed baseline. The method is promising as an analysis and strategy-screening framework, but its decision rules require refinement before replacing empirical strategy comparison.
