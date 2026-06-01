import math
from pathlib import Path

import numpy as np
import pandas as pd


# =========================
# 1. 修改这里
# =========================

INPUT_CSV = Path(r"E:\2026.04\Thesis\CheXpert Dataset\archive\train.csv")
OUT_DIR = Path(r"E:\2026.04\Thesis\CheXpert Dataset\archive")

SELECTED_LABELS = [
    "Cardiomegaly",
    "Edema",
    "Consolidation",
    "Atelectasis",
    "Pneumothorax",
    "Pleural Effusion",
]

SAMPLE_FRAC = 0.10
MIN_PER_STATE = 800
MAX_PER_STATE = 1500

TRAIN_RATIO = 0.60
VAL_RATIO = 0.20
TEST_RATIO = 0.20

RANDOM_SEED = 42


# =========================
# 2. 工具函数
# =========================

def extract_patient_id(path_value):
    parts = str(path_value).replace("\\", "/").split("/")
    for part in parts:
        if part.startswith("patient"):
            return part
    return None


def target_count(total_count):
    if total_count <= 0:
        return 0

    n = math.ceil(total_count * SAMPLE_FRAC)
    n = max(n, MIN_PER_STATE)
    n = min(n, MAX_PER_STATE)
    n = min(n, total_count)

    return n


# =========================
# 3. 读取数据
# =========================

OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_CSV)

required_cols = ["Path"] + SELECTED_LABELS
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"CSV 缺少这些列: {missing}")

# 只保留 Frontal
if "Frontal/Lateral" in df.columns:
    df = df[df["Frontal/Lateral"] == "Frontal"].copy()

# 提取 patient_id
if "patient_id" not in df.columns:
    df["patient_id"] = df["Path"].apply(extract_patient_id)

if df["patient_id"].isna().any():
    raise ValueError("有些 Path 无法解析 patient_id，请检查 Path 格式。")

print("Frontal images:", len(df))
print("Patients:", df["patient_id"].nunique())


# =========================
# 4. patient-level split
# =========================

rng = np.random.default_rng(RANDOM_SEED)

patients = np.array(sorted(df["patient_id"].unique()))
rng.shuffle(patients)

n_patients = len(patients)
n_train = int(n_patients * TRAIN_RATIO)
n_val = int(n_patients * VAL_RATIO)

train_patients = set(patients[:n_train])
val_patients = set(patients[n_train:n_train + n_val])
test_patients = set(patients[n_train + n_val:])

df["split"] = "test"
df.loc[df["patient_id"].isin(train_patients), "split"] = "train"
df.loc[df["patient_id"].isin(val_patients), "split"] = "profile_val"


# =========================
# 5. quota-based sampling
# =========================

state_map = {
    "Positive": 1,
    "Negative": 0,
    "Uncertain": -1,
}

split_ratio = {
    "train": TRAIN_RATIO,
    "profile_val": VAL_RATIO,
    "test": TEST_RATIO,
}

selected_indices = set()
quota_rows = []

for label in SELECTED_LABELS:
    for state_name, state_value in state_map.items():
        available_all = df[df[label] == state_value]
        total_available = len(available_all)
        total_target = target_count(total_available)

        quota_rows.append({
            "Label": label,
            "State": state_name,
            "Available_Frontal": total_available,
            "Target_Total": total_target,
        })

        for split_name, ratio in split_ratio.items():
            candidates = df[
                (df["split"] == split_name) &
                (df[label] == state_value)
            ]

            split_target = math.ceil(total_target * ratio)
            split_target = min(split_target, len(candidates))

            if split_target <= 0:
                print(f"[WARN] No samples for {split_name} / {label} / {state_name}")
                continue

            sampled = candidates.sample(
                n=split_target,
                random_state=RANDOM_SEED,
            )

            selected_indices.update(sampled.index.tolist())


subset = df.loc[sorted(selected_indices)].copy()


# =========================
# 6. leakage check
# =========================

leak_check = subset.groupby("patient_id")["split"].nunique()
leaked = leak_check[leak_check > 1]

if len(leaked) > 0:
    raise RuntimeError("发现 patient leakage，同一个 patient 出现在多个 split。")


# =========================
# 7. 输出 CSV
# =========================

subset.to_csv(OUT_DIR / "pilot_subset_all.csv", index=False, encoding="utf-8-sig")

for split_name in ["train", "profile_val", "test"]:
    part = subset[subset["split"] == split_name]
    part.to_csv(
        OUT_DIR / f"pilot_subset_{split_name}.csv",
        index=False,
        encoding="utf-8-sig",
    )


# =========================
# 8. 输出统计
# =========================

summary_rows = []

for split_name in ["all", "train", "profile_val", "test"]:
    part = subset if split_name == "all" else subset[subset["split"] == split_name]

    for label in SELECTED_LABELS:
        s = part[label]

        summary_rows.append({
            "Split": split_name,
            "Label": label,
            "Positive": int((s == 1).sum()),
            "Negative": int((s == 0).sum()),
            "Uncertain": int((s == -1).sum()),
            "Blank": int(s.isna().sum()),
            "Total_Images": int(len(part)),
        })

summary = pd.DataFrame(summary_rows)

quota = pd.DataFrame(quota_rows)

summary.to_csv(
    OUT_DIR / "pilot_subset_label_distribution.csv",
    index=False,
    encoding="utf-8-sig",
)

quota.to_csv(
    OUT_DIR / "sampling_quota.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nDone.")
print("Output:", OUT_DIR)
print("Subset images:", len(subset))
print("Subset patients:", subset["patient_id"].nunique())
print("\nLabel distribution:")
print(summary.to_string(index=False))