# Data Directory

This directory should contain only aggregate statistics and small derived files.

Do not commit:

- raw CheXpert images
- row-level manifests containing local filesystem paths
- downloaded dataset archives
- train/validation/test image folders

Allowed examples:

- `chexpert_label_summary.csv`
- `chexpert_label_summary_frontal.csv`
- small manually reviewed label distribution summaries

