import argparse
import csv
from pathlib import Path


LABEL_COLUMNS = [
    "No Finding",
    "Enlarged Cardiomediastinum",
    "Cardiomegaly",
    "Lung Opacity",
    "Lung Lesion",
    "Edema",
    "Consolidation",
    "Pneumonia",
    "Atelectasis",
    "Pneumothorax",
    "Pleural Effusion",
    "Pleural Other",
    "Fracture",
    "Support Devices",
]


PREFIX = "CheXpert-v1.0-small/"


def normalize_label(value):
    value = (value or "").strip()
    return value if value else "blank"


def localize_path(dataset_root, source_path):
    rel = source_path.replace("\\", "/")
    if rel.startswith(PREFIX):
        rel = rel[len(PREFIX) :]
    return rel, dataset_root.joinpath(*rel.split("/"))


def parse_image_metadata(relative_path):
    parts = relative_path.replace("\\", "/").split("/")
    if len(parts) < 4:
        return {
            "split": "",
            "patient_id": "",
            "study_id": "",
            "image_name": parts[-1] if parts else "",
        }
    return {
        "split": parts[0],
        "patient_id": parts[1],
        "study_id": parts[2],
        "image_name": parts[-1],
    }


def read_source_rows(dataset_root, split_name, frontal_only):
    source_csv = dataset_root / f"{split_name}.csv"
    rows = []
    skipped_missing = 0
    skipped_invalid = 0

    with source_csv.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            relative_path, image_path = localize_path(dataset_root, raw["Path"])
            meta = parse_image_metadata(relative_path)

            if frontal_only and raw.get("Frontal/Lateral") != "Frontal":
                skipped_invalid += 1
                continue
            if meta["image_name"].startswith("._"):
                skipped_invalid += 1
                continue
            if not image_path.exists():
                skipped_missing += 1
                continue

            item = {
                "local_path": str(image_path),
                "relative_path": relative_path,
                "source_path": raw["Path"],
                "split": meta["split"],
                "patient_id": meta["patient_id"],
                "study_id": meta["study_id"],
                "image_name": meta["image_name"],
                "sex": raw.get("Sex", ""),
                "age": raw.get("Age", ""),
                "view": raw.get("Frontal/Lateral", ""),
                "ap_pa": raw.get("AP/PA", ""),
            }
            for label in LABEL_COLUMNS:
                item[label] = normalize_label(raw.get(label, ""))
            rows.append(item)

    return rows, skipped_missing, skipped_invalid


def summarize_labels(rows, split_name, rare_positive_threshold, support_threshold):
    summary = []
    total = len(rows)
    for label in LABEL_COLUMNS:
        counts = {"1.0": 0, "0.0": 0, "-1.0": 0, "blank": 0}
        for row in rows:
            counts[row[label]] = counts.get(row[label], 0) + 1

        positive = counts.get("1.0", 0)
        negative = counts.get("0.0", 0)
        uncertain = counts.get("-1.0", 0)
        blank = counts.get("blank", 0)
        available = positive + negative + uncertain
        definite_support = positive + negative

        summary.append(
            {
                "split": split_name,
                "label": label,
                "total": total,
                "positive": positive,
                "negative": negative,
                "uncertain": uncertain,
                "blank": blank,
                "available": available,
                "definite_support": definite_support,
                "positive_prevalence": positive / available if available else 0,
                "uncertain_ratio": uncertain / available if available else 0,
                "missing_ratio": blank / total if total else 0,
                "rare_positive_flag": positive < rare_positive_threshold,
                "cold_start_flag": definite_support < support_threshold,
            }
        )
    return summary


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Build clean manifest and label summary for CheXpert small."
    )
    parser.add_argument(
        "--dataset-root",
        default=r"E:\2026.04\Thesis\CheXpert Dataset\archive",
        help="Folder containing train.csv, valid.csv, train/, and valid/.",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory where manifest and summaries will be written.",
    )
    parser.add_argument(
        "--frontal-only",
        action="store_true",
        help="Keep only frontal images. Default keeps frontal and lateral images.",
    )
    parser.add_argument("--rare-positive-threshold", type=int, default=1000)
    parser.add_argument("--support-threshold", type=int, default=100)
    args = parser.parse_args()

    dataset_root = Path(args.dataset_root)
    output_dir = Path(args.output_dir)

    manifest_rows = []
    skipped = {}
    for split_name in ["train", "valid"]:
        rows, skipped_missing, skipped_invalid = read_source_rows(
            dataset_root, split_name, args.frontal_only
        )
        manifest_rows.extend(rows)
        skipped[split_name] = {
            "rows": len(rows),
            "missing_files": skipped_missing,
            "invalid_or_filtered": skipped_invalid,
        }

    manifest_fields = [
        "local_path",
        "relative_path",
        "source_path",
        "split",
        "patient_id",
        "study_id",
        "image_name",
        "sex",
        "age",
        "view",
        "ap_pa",
    ] + LABEL_COLUMNS

    suffix = "_frontal" if args.frontal_only else ""
    manifest_path = output_dir / f"chexpert_manifest{suffix}.csv"
    summary_path = output_dir / f"chexpert_label_summary{suffix}.csv"

    write_csv(manifest_path, manifest_rows, manifest_fields)

    summary_rows = []
    for split_name in ["train", "valid"]:
        split_rows = [row for row in manifest_rows if row["split"] == split_name]
        summary_rows.extend(
            summarize_labels(
                split_rows,
                split_name,
                args.rare_positive_threshold,
                args.support_threshold,
            )
        )
    summary_rows.extend(
        summarize_labels(
            manifest_rows,
            "all",
            args.rare_positive_threshold,
            args.support_threshold,
        )
    )
    summary_fields = [
        "split",
        "label",
        "total",
        "positive",
        "negative",
        "uncertain",
        "blank",
        "available",
        "definite_support",
        "positive_prevalence",
        "uncertain_ratio",
        "missing_ratio",
        "rare_positive_flag",
        "cold_start_flag",
    ]
    write_csv(summary_path, summary_rows, summary_fields)

    print(f"Wrote manifest: {manifest_path.resolve()}")
    print(f"Wrote label summary: {summary_path.resolve()}")
    for split_name, info in skipped.items():
        print(
            f"{split_name}: kept={info['rows']} "
            f"missing_files={info['missing_files']} "
            f"invalid_or_filtered={info['invalid_or_filtered']}"
        )


if __name__ == "__main__":
    main()
