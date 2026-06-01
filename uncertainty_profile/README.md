# Uncertainty Profile Results

This folder contains the label-wise uncertainty profile generated from teacher scores on the profile validation split.

## Purpose

The profiling stage compares the teacher-score distributions of:

- definite positive samples
- definite negative samples
- uncertain samples

The goal is to decide whether uncertain samples for each label are positive-like, negative-like, ambiguous, or unreliable.

## Files

| File | Description |
|---|---|
| `profile_features.csv` | Distribution features and reliability indicators for each label |
| `strategy_mapping.csv` | Final Type A-D assignment and strategy mapping |

## Type A-D Rules

| Type | Meaning | Strategy |
|---|---|---|
| Type A | Uncertain samples are positive-like and teacher evidence is reliable | U-One |
| Type B | Uncertain samples are negative-like and teacher evidence is reliable | U-Zero |
| Type C | Uncertain samples are ambiguous or overlap both positive and negative groups | U-Soft |
| Type D | Teacher evidence is unreliable | U-Ignore |

## Final Mapping

| Label | Profile type | Strategy | Main reason |
|---|---|---|---|
| Cardiomegaly | Type A | U-One | Uncertain scores are closer to positive scores |
| Edema | Type A | U-One | Uncertain scores are closer to positive scores |
| Consolidation | Type A | U-One | Uncertain scores are closer to positive scores |
| Atelectasis | Type D | U-Ignore | P/N teacher separability is too low |
| Pneumothorax | Type C | U-Soft | Uncertain scores overlap both positive and negative groups |
| Pleural Effusion | Type A | U-One | Uncertain scores are closer to positive scores |

## Key Observations

Most labels were classified as positive-like. This suggests that a global U-Zero strategy is likely too harsh for this pilot subset, because many uncertain samples appear closer to definite positives than definite negatives in teacher-score space.

Atelectasis is the important exception. Its uncertain scores look positive-like, but the teacher cannot separate positive and negative Atelectasis samples reliably. Because of this, the reliability gate overrides the positive-like signal and assigns Type D / U-Ignore.

Pneumothorax is assigned Type C / U-Soft because its uncertain samples sit between positive and negative groups and overlap both distributions.

## Stage Conclusion

The profile table supports the main research motivation: uncertain labels are not homogeneous across pathologies. However, later final-model results show that positive-like score distributions do not always mean that hard U-One training will be the best final strategy.
