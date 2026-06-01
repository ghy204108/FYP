# Data Directory

This directory should contain only aggregate statistics and small derived files.

Do not commit:

- raw CheXpert images
- row-level manifests containing local filesystem paths
- downloaded dataset archives
- train/validation/test image folders

Allowed examples:

- `pre_experiment_label_summary.csv`
- small manually reviewed label distribution summaries

Full-dataset aggregate summaries are not tracked in this pre-experiment
repository to avoid confusing them with the current subset experiment.
