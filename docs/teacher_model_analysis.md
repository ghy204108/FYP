# Teacher Model Analysis

This document summarizes the teacher/probe model results from the pilot subset.

## Teacher Role

The teacher model was trained with U-Ignore and used only as a probe. Its purpose was to generate score distributions for positive, negative, and uncertain samples on the `profile_val` split.

The teacher probabilities are not used as ground truth labels. Instead, they provide evidence for whether uncertain samples appear positive-like, negative-like, ambiguous, or unreliable for each label.

## Reliability Metrics

Reliability was assessed per label using:

- AUPRC on definite positive/negative samples
- AUROC on definite positive/negative samples
- Brier score
- Expected calibration error
- Median positive-negative score separability
- Minimum support for positive, negative, and uncertain groups

## Profile Validation Reliability

| Label | Pos | Neg | U | AUPRC | AUROC | Brier | ECE | P/N Median Sep. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cardiomegaly | 760 | 325 | 306 | 0.9539 | 0.9023 | 0.1132 | 0.0337 | 0.6429 |
| Edema | 1024 | 645 | 416 | 0.8991 | 0.8765 | 0.1392 | 0.0652 | 0.6362 |
| Consolidation | 444 | 725 | 804 | 0.8717 | 0.9223 | 0.1051 | 0.0483 | 0.8769 |
| Atelectasis | 783 | 162 | 932 | 0.8722 | 0.6446 | 0.1381 | 0.0665 | 0.0579 |
| Pneumothorax | 421 | 1066 | 192 | 0.6125 | 0.8060 | 0.1555 | 0.0363 | 0.3239 |
| Pleural Effusion | 1525 | 911 | 390 | 0.9524 | 0.9433 | 0.0788 | 0.0305 | 0.9245 |

## Interpretation

The teacher is strong for Cardiomegaly, Edema, Consolidation, and Pleural Effusion. These labels have good AUPRC/AUROC and clear P/N median separation.

Atelectasis is the most important reliability warning. Although its AUPRC is high, its AUROC is low and its P/N median separability is only 0.0579. This means the teacher gives similarly high scores to positive and negative Atelectasis samples, so it should not be trusted to make a strong positive-like or negative-like uncertainty decision.

Pneumothorax is moderately reliable but weaker than the other labels. It has acceptable AUROC but low AUPRC compared with the other findings, and its uncertain group is relatively small.

## Methodological Implication

The teacher reliability gate is necessary. Without it, Atelectasis would appear positive-like based on uncertain median score alone, but the teacher's P/N separation is too weak to support a confident hard-label decision. This is why the final profile maps Atelectasis to Type D / U-Ignore.
