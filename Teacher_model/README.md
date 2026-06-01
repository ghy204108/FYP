# Teacher Model Results

This folder contains the teacher/probe model outputs used for label-wise uncertainty profiling.

## Purpose

The teacher model was trained with the U-Ignore policy. Definite positive and definite negative labels contributed to the loss, while uncertain and blank labels were masked out. The teacher was not used as ground truth. It was used only as a probe to generate score distributions for positive, negative, and uncertain samples.

The main question at this stage was:

> Is the teacher reliable enough for each label to support score-distribution profiling?

## Files

| File | Description | GitHub status |
|---|---|---|
| `teacher_reliability_profile_val.csv` | Per-label reliability metrics on the profile validation split | uploaded |
| `teacher_profile_val_predictions.csv` | Per-image teacher scores on profile validation | local only, ignored |
| `teacher_test_predictions.csv` | Per-image teacher scores on test | local only, ignored |
| `checkpoints/best_teacher.pt` | Best teacher checkpoint | local only, ignored |

Only the reliability table is uploaded because the prediction files and checkpoint are generated artifacts and contain per-image local-path records.

## Reliability Summary

| Label | Pos | Neg | U | AUPRC | AUROC | ECE | P/N median separation |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cardiomegaly | 760 | 325 | 306 | 0.9539 | 0.9023 | 0.0337 | 0.6429 |
| Edema | 1024 | 645 | 416 | 0.8991 | 0.8765 | 0.0652 | 0.6362 |
| Consolidation | 444 | 725 | 804 | 0.8717 | 0.9223 | 0.0483 | 0.8769 |
| Atelectasis | 783 | 162 | 932 | 0.8722 | 0.6446 | 0.0665 | 0.0579 |
| Pneumothorax | 421 | 1066 | 192 | 0.6125 | 0.8060 | 0.0363 | 0.3239 |
| Pleural Effusion | 1525 | 911 | 390 | 0.9524 | 0.9433 | 0.0305 | 0.9245 |

## Interpretation

The teacher is reliable for Cardiomegaly, Edema, Consolidation, and Pleural Effusion. These labels have strong AUPRC/AUROC and clear median separation between positive and negative scores.

Atelectasis is the main reliability warning. Although its AUPRC is high, its AUROC is only 0.6446 and its positive-negative median separation is only 0.0579. This means the teacher assigns similarly high scores to both positive and negative Atelectasis samples, so the teacher should not be trusted to make a hard positive-like or negative-like uncertainty decision for this label.

Pneumothorax is moderately reliable but weaker than the other labels. Its AUPRC is lower, and its uncertain support is relatively small.

## Stage Conclusion

The teacher model is good enough to support profiling for most labels, but reliability gating is necessary. The Atelectasis result directly motivates the Type D / U-Ignore decision used later in the uncertainty profile.
