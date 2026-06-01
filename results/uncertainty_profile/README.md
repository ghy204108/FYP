# Uncertainty Profile

This folder contains the label-wise uncertainty profile produced from teacher scores on the profile validation split.

The profile asks a simple question for each label: when CheXpert marks a sample as uncertain, does the trained probe score it more like a definite positive case, a definite negative case, an ambiguous case, or a case where the teacher is not reliable enough to decide?

## Files

| File | What it contains |
|---|---|
| `profile_features.csv` | Distribution features such as medians, Wasserstein distances, overlaps, effect sizes, and teacher reliability values |
| `strategy_mapping.csv` | The final Type A-D assignment and the corresponding uncertainty-handling strategy |

## Mapping Used in the Pilot

| Label | Type | Strategy | Short interpretation |
|---|---|---|---|
| Cardiomegaly | Type A | U-One | uncertain samples look positive-like |
| Edema | Type A | U-One | uncertain samples look positive-like |
| Consolidation | Type A | U-One | uncertain samples look positive-like |
| Atelectasis | Type D | U-Ignore | teacher evidence is not reliable enough |
| Pneumothorax | Type C | U-Soft | uncertain samples overlap both sides |
| Pleural Effusion | Type A | U-One | uncertain samples look positive-like |

## Notes

Most labels appear positive-like in the teacher score space. That is useful evidence against a global U-Zero rule, because treating every uncertain sample as negative would discard many cases that look closer to positive findings.

Atelectasis is the important exception. Its uncertain samples also receive high scores, but the teacher gives high scores to both positive and negative Atelectasis cases. The reliability gate therefore overrides the positive-like signal and maps Atelectasis to U-Ignore.

Pneumothorax is not cleanly positive-like or negative-like. Its uncertain scores sit between the two groups and overlap both, so it is mapped to U-Soft in the profile-guided model.

The profile is best read as evidence for strategy selection, not as a claim that the selected strategy must be optimal. The final model comparison tests that next.
