# Label-wise Uncertainty Profiling for CheXpert

This repository tracks the FYP experiment process for label-wise uncertain-label
strategy selection in imbalanced multi-label chest X-ray classification.

The project studies whether a single teacher/probe model can provide
label-wise score-distribution evidence for choosing how to handle uncertain
CheXpert-style labels before training every candidate final model.

## Current Scope

The current stage is a small-scale pre-experiment on a CheXpert subset of
21,982 images. The goal is to verify that the methodology pipeline is feasible:

1. Build a clean label matrix and split-aware manifests.
2. Train a teacher/probe model with `U-Ignore`.
3. Extract per-label positive, negative and uncertain score distributions.
4. Compute distribution features and teacher reliability indicators.
5. Map each label to a Type A-D uncertainty profile.
6. Compare a profile-guided strategy with fixed uncertain-label strategies.

## Repository Layout

```text
.
├── configs/                         # Reproducible experiment settings
├── data/                            # Pre-experiment aggregate summaries only
├── docs/                            # Protocol notes and methodology records
├── experiments/                     # Lightweight experiment logs
├── results/                         # Small result tables only
├── scripts/                         # Data preparation and experiment scripts
│   └── initial_analysis/            # Pilot subset construction scripts
└── README.md
```

## Data Policy

Raw CheXpert images, row-level manifests with local paths, checkpoints and
large outputs are intentionally excluded from GitHub. Only aggregate label
statistics and reproducible scripts should be committed.

## Pre-experiment Outputs

The pre-experiment should produce:

- `data/pre_experiment_label_summary.csv`
- `results/teacher_reliability.csv`
- `results/profile_features.csv`
- `results/strategy_mapping.csv`
- `results/final_results.csv` when final model comparison is run

## Notes

This repository is for algorithmic benchmarking and FYP documentation only.
Model outputs are not clinical diagnoses.

The scripts under `scripts/initial_analysis/` may contain local path defaults.
Update those paths before running them on another machine.
