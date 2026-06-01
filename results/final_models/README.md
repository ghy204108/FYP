# Final Models

This folder contains the 5-epoch comparison between fixed uncertain-label strategies and the profile-guided strategy.

The purpose of this stage was not to maximize CheXpert performance, but to check whether the label-wise profile gives a useful training strategy compared with simple fixed baselines.

## Files

| File | What it contains |
|---|---|
| `final_results_summary.csv` | Macro-level validation and test metrics for each final model |
| `final_results_per_label.csv` | Per-label validation and test metrics for each final model |

The checkpoints and per-image prediction files are kept local.

## Test Set Summary

| Model | Macro AUPRC | Macro AUROC | Mean Brier | Mean ECE |
|---|---:|---:|---:|---:|
| U-Zero | 0.8300 | 0.8236 | 0.1757 | 0.1561 |
| U-One | 0.8538 | 0.8559 | 0.1322 | 0.0932 |
| U-Ignore | **0.8609** | **0.8616** | **0.1182** | **0.0522** |
| Profile-guided | 0.8554 | 0.8569 | 0.1261 | 0.0729 |

## Per-label AUPRC

| Label | Best model | Profile-guided AUPRC | Comment |
|---|---|---:|---|
| Cardiomegaly | U-One | 0.9484 | profile-guided is close, but all U-One is best |
| Edema | U-Ignore | 0.9059 | U-Ignore is slightly better |
| Consolidation | U-Ignore | 0.8606 | U-Ignore is clearly better |
| Atelectasis | Profile-guided | **0.8977** | supports the Type D reliability gate |
| Pneumothorax | U-Ignore | 0.5687 | Type C/U-Soft needs more checking |
| Pleural Effusion | U-Ignore | 0.9510 | U-Ignore is strongest |

## Reading of the Result

The result is mixed, but still informative.

Profile-guided is better than U-Zero and slightly better than U-One, so the profile is not arbitrary. It avoids the weakest fixed strategy. However, it does not beat U-Ignore, which is the strongest overall baseline in this pilot.

The most encouraging label is Atelectasis. The teacher reliability check marked it as unsafe for hard relabeling, and the profile-guided model achieved the best Atelectasis AUPRC. This supports the value of keeping an explicit "unreliable teacher" case.

The main limitation is that positive-like uncertain distributions did not always translate into better U-One training. Edema, Consolidation, and Pleural Effusion looked positive-like in the profile, but U-Ignore performed better in the final comparison. This suggests that teacher-score similarity is useful evidence, but not sufficient on its own.

## Possible Reasons

There are several model-level reasons why profile-guided did not outperform U-Ignore.

The first is that the final model is trained as a joint multi-label network. Even though the uncertainty strategy is chosen per label, the DenseNet backbone is shared by all six outputs. This means a U-One decision for several labels can change the shared representation and affect labels that were assigned different strategies. The profile-guided model is therefore not just six independent binary classifiers stitched together.

The second reason is calibration. U-Ignore has the best test Brier score and ECE. This suggests that masking uncertain labels may produce less overconfident predictions than turning uncertain labels into hard targets. The profile-guided model improves over U-Zero and U-One overall, but its calibration is still weaker than U-Ignore.

The third reason is the Type C decision for Pneumothorax. The profile maps Pneumothorax to U-Soft, but this run did not include an all U-Soft baseline. Since Pneumothorax is also the hardest label by AUPRC, this missing baseline makes the Type C result hard to interpret. A fixed 0.5 soft target may also be too high for a label whose uncertain median teacher score is closer to 0.30.

The fourth reason is that macro AUPRC gives each label equal weight. This is appropriate for imbalanced multi-label evaluation, but it also means that a difficult label such as Pneumothorax can noticeably affect the macro score. The profile-guided model loses to U-Ignore on Pneumothorax, which contributes to the overall gap.

Overall, these results suggest that the Type A rule should be more conservative. A future rule should distinguish between "uncertain samples look positive-like" and "uncertain samples are safe to use as hard positive supervision."

## Current Takeaway

The pilot supports a cautious conclusion: label-wise profiling is useful for interpreting uncertain labels and screening out poor fixed strategies, but the current rules are not yet strong enough to replace empirical validation. A next run should add an all U-Soft baseline, construct a validation oracle, and refine the Type A rule.
