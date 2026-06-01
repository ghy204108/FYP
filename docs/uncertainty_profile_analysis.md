# Uncertainty Profile Analysis

This document summarizes the label-wise Type A-D uncertainty profile generated from teacher scores on the `profile_val` split.

## Profiling Features

For each label, uncertain samples were compared against definite positive and definite negative samples using:

- median score comparison
- Wasserstein distance
- overlap ratio
- rank-biserial effect size
- teacher reliability checks

The mapping rules use distribution evidence only if the teacher is reliable for that label. If teacher reliability fails, the label is conservatively assigned to Type D / U-Ignore.

## Final Type A-D Mapping

| Label | Type | Strategy | Main reason |
|---|---|---|---|
| Cardiomegaly | Type A | U-One | Uncertain scores are closer to positive; teacher is reliable |
| Edema | Type A | U-One | Uncertain scores are closer to positive; teacher is reliable |
| Consolidation | Type A | U-One | Uncertain scores are closer to positive; teacher is reliable |
| Atelectasis | Type D | U-Ignore | Teacher P/N separability is too low |
| Pneumothorax | Type C | U-Soft | Uncertain scores overlap both positive and negative groups |
| Pleural Effusion | Type A | U-One | Uncertain scores are closer to positive; teacher is reliable |

## Key Label Observations

### Cardiomegaly

Uncertain samples are clearly closer to positive samples than negative samples. The teacher is reliable, with AUPRC 0.9539 and P/N median separability 0.6429. This supports Type A / U-One.

### Edema

Uncertain samples are positive-like, and teacher reliability is acceptable. This supports Type A / U-One, although final model results later show that U-Ignore remains competitive.

### Consolidation

The uncertain distribution is strongly closer to the positive distribution, with high separation from negative samples. This supports Type A / U-One at the profiling stage.

### Atelectasis

Atelectasis is the strongest example of why teacher reliability matters. Its uncertain median score is high, but positive and negative score distributions are poorly separated. The P/N median separability is only 0.0579, so the label is assigned to Type D / U-Ignore.

### Pneumothorax

Pneumothorax uncertain samples lie between positive and negative distributions and overlap both groups. This supports Type C / U-Soft. However, this decision requires further validation because the final model comparison did not include an all U-Soft baseline.

### Pleural Effusion

Pleural Effusion has a strong teacher, and uncertain samples are closer to positive than negative samples. This supports Type A / U-One.

## Interpretation

The profiling stage confirms that uncertain labels are not homogeneous across pathologies. The six labels do not collapse into a single strategy:

- Four labels are Type A / U-One.
- One label is Type C / U-Soft.
- One label is Type D / U-Ignore.

This supports the motivation for label-wise uncertain-label handling. At the same time, the final model results show that positive-like score distributions do not always guarantee that hard U-One training will outperform U-Ignore.
