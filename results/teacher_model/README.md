# Teacher Model

This folder records the teacher/probe model check that was used before building the uncertainty profiles.

The teacher was trained with U-Ignore: definite positive and negative labels contributed to the loss, while uncertain and blank entries were masked. I use this model only as a probe for score distributions, not as a source of ground truth.

## File

| File | What it contains |
|---|---|
| `teacher_reliability_profile_val.csv` | Per-label reliability metrics measured on the profile validation split |

The per-image prediction files and the model checkpoint are kept local because they are generated artifacts and include local image paths.

## Reliability Summary

| Label | AUPRC | AUROC | ECE | P/N median separation | Reading |
|---|---:|---:|---:|---:|---|
| Cardiomegaly | 0.9539 | 0.9023 | 0.0337 | 0.6429 | reliable |
| Edema | 0.8991 | 0.8765 | 0.0652 | 0.6362 | reliable |
| Consolidation | 0.8717 | 0.9223 | 0.0483 | 0.8769 | reliable |
| Atelectasis | 0.8722 | 0.6446 | 0.0665 | 0.0579 | unreliable for P/N separation |
| Pneumothorax | 0.6125 | 0.8060 | 0.0363 | 0.3239 | usable but weaker |
| Pleural Effusion | 0.9524 | 0.9433 | 0.0305 | 0.9245 | reliable |

## Notes

The main warning is Atelectasis. Its AUPRC looks acceptable, but the teacher barely separates positive and negative cases by median score. This is exactly the kind of case where the profiling method should avoid making a confident hard-label decision.

This reliability check is therefore not just a performance report. It acts as a gatekeeper for the next step: labels with weak teacher evidence should be handled conservatively.
