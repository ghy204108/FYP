# Results

This directory contains the small result tables and stage-level notes from the current pilot experiment.

```text
teacher_model/
  README.md
  teacher_reliability_profile_val.csv

uncertainty_profile/
  README.md
  profile_features.csv
  strategy_mapping.csv

final_models/
  README.md
  final_results_summary.csv
  final_results_per_label.csv
```

The committed files are intentionally lightweight. Model checkpoints, per-image prediction dumps, raw CheXpert images, and row-level manifests with local paths are kept out of Git.
