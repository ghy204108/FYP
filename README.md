# Label-wise Uncertainty Profiling for CheXpert Uncertain Labels

This repository contains a Final Year Project pilot experiment on label-wise uncertain-label handling for imbalanced multi-label chest X-ray classification using a CheXpert frontal-view subset.

The project asks whether a single teacher/probe model can provide useful score-distribution evidence for deciding how each pathology label should handle `uncertain` labels before training final strategy-specific models.

## Project Question

CheXpert-style labels include positive, negative, uncertain, and blank states. A single global rule such as treating all uncertain labels as 0, 1, ignored, or soft targets may be too coarse because different findings may have different uncertainty semantics.

This pilot tests a label-wise profiling workflow:

1. Build a frontal-only patient-level pilot subset.
2. Train a U-Ignore teacher/probe model.
3. Use teacher scores on `profile_val` to compare positive, negative, and uncertain score distributions for each label.
4. Assign each label to a Type A-D uncertainty profile.
5. Train final models under fixed strategies and the profile-guided strategy.
6. Compare held-out test performance.

## Pilot Scope

The current pilot uses 21,982 frontal images from six labels:

- Cardiomegaly
- Edema
- Consolidation
- Atelectasis
- Pneumothorax
- Pleural Effusion

Patient-level split:

| Split | Images |
|---|---:|
| Train | 13,205 |
| Profile validation | 4,377 |
| Test | 4,400 |

The pilot subset is intended to validate the methodology pipeline, not to claim state-of-the-art CheXpert performance.

## Method Overview

The teacher model is trained with U-Ignore:

- Positive labels: target 1, loss mask 1
- Negative labels: target 0, loss mask 1
- Uncertain labels: loss mask 0
- Blank labels: loss mask 0

The teacher is then used only as a probe. Its probabilities are not treated as ground truth. For each label, the project compares score distributions for:

- definite positive samples
- definite negative samples
- uncertain samples

The profiling stage computes distribution features such as median score, Wasserstein distance, overlap ratio, Mann-Whitney effect size, and teacher reliability metrics.

## Type A-D Strategy Mapping

| Type | Meaning | Final strategy |
|---|---|---|
| Type A | Uncertain samples are positive-like and teacher is reliable | U-One |
| Type B | Uncertain samples are negative-like and teacher is reliable | U-Zero |
| Type C | Uncertain samples are ambiguous or overlap both groups | U-Soft |
| Type D | Teacher is unreliable for that label | U-Ignore |

Current pilot mapping:

| Label | Type | Strategy |
|---|---|---|
| Cardiomegaly | Type A | U-One |
| Edema | Type A | U-One |
| Consolidation | Type A | U-One |
| Atelectasis | Type D | U-Ignore |
| Pneumothorax | Type C | U-Soft |
| Pleural Effusion | Type A | U-One |

## Main 5-Epoch Pilot Result

Held-out test results:

| Model | Test Macro AUPRC | Test Macro AUROC | Test Mean Brier | Test Mean ECE |
|---|---:|---:|---:|---:|
| U-Zero | 0.8300 | 0.8236 | 0.1757 | 0.1561 |
| U-One | 0.8538 | 0.8559 | 0.1322 | 0.0932 |
| U-Ignore | **0.8609** | **0.8616** | **0.1182** | **0.0522** |
| Profile-guided | 0.8554 | 0.8569 | 0.1261 | 0.0729 |

The profile-guided strategy improves over U-Zero and slightly outperforms U-One, but it does not outperform U-Ignore in this pilot. This suggests that teacher-score profiling provides meaningful but incomplete evidence for strategy selection. The current decision rules are useful for analysis and screening, but they are not yet strong enough to replace empirical validation.

## Repository Structure

```text
configs/
  pre_experiment.yaml              # Pilot configuration
data/
  pre_experiment_label_summary.csv # Aggregate subset label statistics
docs/
  experiment_pipeline.md           # End-to-end workflow
  teacher_model_analysis.md        # Teacher/probe analysis
  uncertainty_profile_analysis.md  # Type A-D profiling result
  final_results_analysis.md        # Final model comparison
  github_upload_notes.md           # What should/should not be uploaded
scripts/
  initial_analysis/                # Dataset preparation scripts
Teacher_model/
  teacher_reliability_profile_val.csv
uncertainty_profile/
  profile_features.csv
  strategy_mapping.csv
final_models/
  final_results_summary.csv
  final_results_per_label.csv
```

Raw CheXpert images, local row-level manifests with private paths, model checkpoints, and per-image prediction dumps should not be committed unless explicitly intended.

## Current Status

The pilot experiment is complete:

- teacher model trained successfully
- reliability table generated
- label-wise Type A-D profile generated
- fixed-strategy and profile-guided final models compared

The next recommended steps are:

1. Add an all U-Soft baseline, because the profile-guided strategy currently uses U-Soft for Pneumothorax.
2. Build a validation-oracle strategy table from fixed-strategy profile validation results.
3. Refine Type A rules, since positive-like score distributions did not always translate into better U-One final performance.
4. Repeat with multiple seeds if computation time allows.
