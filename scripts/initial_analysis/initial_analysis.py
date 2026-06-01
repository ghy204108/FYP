import pandas as pd
from pathlib import Path

# 改成你自己的 train.csv 路径
train_csv = Path(r"E:\2026.04\Thesis\CheXpert Dataset\archive\train.csv")

df = pd.read_csv(train_csv)

labels = [
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

rows = []

for label in labels:
    s = df[label]

    rows.append({
        "Label": label,
        "Positive": int((s == 1).sum()),
        "Negative": int((s == 0).sum()),
        "Uncertain": int((s == -1).sum()),
        "Blank": int(s.isna().sum()),
        "Total": int(len(s)),
    })

summary = pd.DataFrame(rows)

print(summary.to_string(index=False))

summary.to_csv("label_distribution_all.csv", index=False, encoding="utf-8-sig")