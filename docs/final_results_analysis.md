# Final Model Results Analysis

This document analyzes the 5-epoch final model comparison.

## Compared Strategies

The current final experiment trained four final models:

- U-Zero
- U-One
- U-Ignore
- Profile-guided

The all U-Soft baseline was not included in this run. It should be added in a follow-up because the profile-guided mapping uses U-Soft for Pneumothorax.

## Overall Test Results

| Model | Test Macro AUPRC | Test Macro AUROC | Test Mean Brier | Test Mean ECE |
|---|---:|---:|---:|---:|
| U-Zero | 0.8300 | 0.8236 | 0.1757 | 0.1561 |
| U-One | 0.8538 | 0.8559 | 0.1322 | 0.0932 |
| U-Ignore | **0.8609** | **0.8616** | **0.1182** | **0.0522** |
| Profile-guided | 0.8554 | 0.8569 | 0.1261 | 0.0729 |

## Main Finding

The profile-guided strategy improves over U-Zero and slightly outperforms U-One, but it does not outperform U-Ignore. U-Ignore is the strongest strategy in this pilot across macro AUPRC, macro AUROC, Brier score, and ECE.

This means the current method is useful but not yet sufficient as a replacement for strong fixed baselines. The result should be interpreted as a mixed but informative pilot finding.

## Per-label Test AUPRC

| Label | U-Zero | U-One | U-Ignore | Profile-guided | Best |
|---|---:|---:|---:|---:|---|
| Cardiomegaly | 0.9211 | **0.9534** | 0.9449 | 0.9484 | U-One |
| Edema | 0.8644 | 0.9096 | **0.9097** | 0.9059 | U-Ignore |
| Consolidation | 0.8180 | 0.8497 | **0.8722** | 0.8606 | U-Ignore |
| Atelectasis | 0.8562 | 0.8908 | 0.8909 | **0.8977** | Profile-guided |
| Pneumothorax | 0.5654 | 0.5655 | **0.5876** | 0.5687 | U-Ignore |
| Pleural Effusion | 0.9548 | 0.9537 | **0.9599** | 0.9510 | U-Ignore |

## What Worked

The method clearly avoids the weakest fixed strategy, U-Zero. This aligns with the profiling result: most uncertain distributions were closer to positive than negative, so treating all uncertain labels as negative is too harsh.

The Type D reliability gate is also supported by Atelectasis. The teacher could not reliably separate positive and negative Atelectasis samples, so the profile assigned U-Ignore. In the held-out test set, profile-guided achieved the best Atelectasis AUPRC among all compared strategies.

## What Did Not Work

The profile-guided model did not beat U-Ignore overall. This suggests that teacher-score similarity alone is not enough to decide when uncertain labels should be hard-coded as positive.

Several Type A labels were mapped to U-One because their uncertain distributions were positive-like, but U-Ignore still performed better for Edema, Consolidation, and Pleural Effusion on the test set.

Pneumothorax also needs further analysis. It was mapped to Type C / U-Soft because uncertain samples overlapped both positive and negative distributions, but the experiment did not include an all U-Soft baseline. This makes it difficult to isolate whether the U-Soft decision itself was weak or whether interaction with the other profile-guided label strategies affected performance.

## Current Conclusion

The current pilot supports a cautious conclusion:

> Label-wise teacher-assisted uncertainty profiling provides interpretable evidence and improves over some fixed strategies, especially U-Zero, but the current decision rules do not outperform the conservative U-Ignore baseline. The method is promising as a strategy-screening and analysis framework, but it requires rule refinement and additional validation before it can replace empirical strategy comparison.

## Recommended Follow-up Experiments

1. Add an all U-Soft final model baseline.
2. Build a validation-oracle mapping from profile-validation per-label results.
3. Compute profile-guided agreement and regret against the validation oracle.
4. Refine Type A rules to distinguish "positive-like distribution" from "safe to hard-code as positive".
5. Repeat the final comparison with multiple random seeds if computation time permits.
