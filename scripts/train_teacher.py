import os
import random
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

import torchvision.transforms as T
import torchvision.models as models

from sklearn.metrics import average_precision_score, roc_auc_score, brier_score_loss


# =========================
# Config
# =========================

TRAIN_MANIFEST_PATH = r"E:\2026.04\Thesis\CheXpert Dataset\archive\subset_train.csv"
PROFILE_VAL_MANIFEST_PATH = r"E:\2026.04\Thesis\CheXpert Dataset\archive\subset_profile_val.csv"
TEST_MANIFEST_PATH = r"E:\2026.04\Thesis\CheXpert Dataset\archive\subset_test.csv"

# Your real CheXpert image root. If paths in CSV are relative, they will be joined with this root.
IMAGE_ROOT = r"E:\2026.04\Thesis\CheXpert Dataset\archive"

OUT_DIR = Path(r"D:\Codex\CodexProjects\FYP\results\teacher_model")

LABELS = [
    "Cardiomegaly",
    "Edema",
    "Consolidation",
    "Atelectasis",
    "Pneumothorax",
    "Pleural Effusion",
]

# Prefer local_path if it exists. If your CSV only has Path, this script will resolve it.
IMAGE_PATH_COL_CANDIDATES = ["local_path", "Path", "path", "source_path", "relative_path"]

SEED = 42
IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 5
LR = 1e-4

# On Windows, if DataLoader gives weird worker errors, set this to 0.
NUM_WORKERS = 4

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# =========================
# Utils
# =========================

def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def find_image_col(df):
    for col in IMAGE_PATH_COL_CANDIDATES:
        if col in df.columns:
            return col
    raise ValueError(f"No image path column found. Tried: {IMAGE_PATH_COL_CANDIDATES}")


def resolve_image_path(path_value):
    raw = str(path_value).strip().replace("/", os.sep).replace("\\", os.sep)

    if os.path.isabs(raw) and os.path.exists(raw):
        return raw

    candidates = []

    if os.path.isabs(raw):
        candidates.append(raw)
    else:
        candidates.append(os.path.join(IMAGE_ROOT, raw))

        # If CSV path is CheXpert-v1.0-small/train/... but local folder is archive/train/...
        stripped = raw
        prefix = "CheXpert-v1.0-small" + os.sep
        if stripped.startswith(prefix):
            stripped = stripped[len(prefix):]
            candidates.append(os.path.join(IMAGE_ROOT, stripped))

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    raise FileNotFoundError(
        "Image file not found.\n"
        f"Original CSV path: {path_value}\n"
        "Tried:\n" + "\n".join(candidates)
    )


def check_image_paths(df, image_col, n=20):
    print("Checking image paths...")
    sample = df.head(n)

    for i, row in sample.iterrows():
        resolved = resolve_image_path(row[image_col])
        if i < 3:
            print(f"  OK: {resolved}")

    print(f"Checked first {len(sample)} image paths successfully.")


def parse_label_value(x):
    if pd.isna(x):
        return np.nan

    if isinstance(x, str):
        x = x.strip()
        if x.lower() in ["blank", "", "nan", "none"]:
            return np.nan

    return float(x)


def make_targets_and_masks(row):
    targets = []
    masks = []

    for label in LABELS:
        v = parse_label_value(row[label])

        if np.isnan(v):
            targets.append(0.0)
            masks.append(0.0)
        elif v == 1.0:
            targets.append(1.0)
            masks.append(1.0)
        elif v == 0.0:
            targets.append(0.0)
            masks.append(1.0)
        elif v == -1.0:
            # U-Ignore: uncertain does not contribute to teacher loss.
            targets.append(0.0)
            masks.append(0.0)
        else:
            targets.append(0.0)
            masks.append(0.0)

    return np.array(targets, dtype=np.float32), np.array(masks, dtype=np.float32)


def get_true_state(row, label):
    v = parse_label_value(row[label])

    if np.isnan(v):
        return "blank"
    if v == 1.0:
        return "positive"
    if v == 0.0:
        return "negative"
    if v == -1.0:
        return "uncertain"

    return "unknown"


def masked_bce_with_logits(logits, targets, masks):
    loss = nn.functional.binary_cross_entropy_with_logits(
        logits,
        targets,
        reduction="none",
    )
    loss = loss * masks
    denom = masks.sum().clamp(min=1.0)
    return loss.sum() / denom


def compute_ece(y_true, y_prob, n_bins=10):
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)

    if len(y_prob) == 0:
        return np.nan

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]

        if i == n_bins - 1:
            mask = (y_prob >= lo) & (y_prob <= hi)
        else:
            mask = (y_prob >= lo) & (y_prob < hi)

        if mask.sum() == 0:
            continue

        conf = y_prob[mask].mean()
        acc = y_true[mask].mean()
        ece += (mask.sum() / len(y_prob)) * abs(acc - conf)

    return float(ece)


# =========================
# Dataset
# =========================

class CheXpertTeacherDataset(Dataset):
    def __init__(self, df, image_col, transform=None):
        self.df = df.reset_index(drop=True)
        self.image_col = image_col
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        image_path = resolve_image_path(row[self.image_col])
        image = Image.open(image_path).convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        targets, masks = make_targets_and_masks(row)

        return {
            "image": image,
            "targets": torch.tensor(targets, dtype=torch.float32),
            "masks": torch.tensor(masks, dtype=torch.float32),
            "index": idx,
        }


# =========================
# Model
# =========================

def build_model(num_labels):
    weights = models.DenseNet121_Weights.IMAGENET1K_V1
    model = models.densenet121(weights=weights)

    in_features = model.classifier.in_features
    model.classifier = nn.Linear(in_features, num_labels)

    return model


# =========================
# Eval / Prediction
# =========================

@torch.no_grad()
def predict(model, loader):
    model.eval()

    all_probs = []
    all_targets = []
    all_masks = []
    all_indices = []

    for batch in loader:
        images = batch["image"].to(DEVICE)

        logits = model(images)
        probs = torch.sigmoid(logits).cpu().numpy()

        all_probs.append(probs)
        all_targets.append(batch["targets"].numpy())
        all_masks.append(batch["masks"].numpy())
        all_indices.extend(batch["index"].numpy().tolist())

    return {
        "probs": np.concatenate(all_probs, axis=0),
        "targets": np.concatenate(all_targets, axis=0),
        "masks": np.concatenate(all_masks, axis=0),
        "indices": np.array(all_indices),
    }


def compute_macro_auprc(pred):
    scores = []

    for j in range(len(LABELS)):
        mask = pred["masks"][:, j] == 1
        y_true = pred["targets"][mask, j]
        y_prob = pred["probs"][mask, j]

        if len(np.unique(y_true)) < 2:
            continue

        scores.append(average_precision_score(y_true, y_prob))

    if not scores:
        return 0.0

    return float(np.mean(scores))


def save_long_predictions(df, pred, out_path):
    rows = []

    for local_i, original_i in enumerate(pred["indices"]):
        row = df.iloc[original_i]
        resolved_path = resolve_image_path(row[IMAGE_COL])

        for j, label in enumerate(LABELS):
            rows.append({
                "image_path": resolved_path,
                "original_path_value": row[IMAGE_COL],
                "split": row["split"],
                "label": label,
                "true_state": get_true_state(row, label),
                "score": float(pred["probs"][local_i, j]),
            })

    pd.DataFrame(rows).to_csv(out_path, index=False, encoding="utf-8-sig")


def save_reliability(df, pred, out_path):
    rows = []

    for j, label in enumerate(LABELS):
        states = df[label].apply(parse_label_value)

        positive_count = int((states == 1.0).sum())
        negative_count = int((states == 0.0).sum())
        uncertain_count = int((states == -1.0).sum())
        blank_count = int(states.isna().sum())

        mask = pred["masks"][:, j] == 1
        y_true = pred["targets"][mask, j]
        y_prob = pred["probs"][mask, j]

        if len(np.unique(y_true)) >= 2:
            auprc = average_precision_score(y_true, y_prob)
            auroc = roc_auc_score(y_true, y_prob)
            brier = brier_score_loss(y_true, y_prob)
            ece = compute_ece(y_true, y_prob)

            pos_scores = y_prob[y_true == 1]
            neg_scores = y_prob[y_true == 0]
            pn_separability = float(np.median(pos_scores) - np.median(neg_scores))
        else:
            auprc = np.nan
            auroc = np.nan
            brier = np.nan
            ece = np.nan
            pn_separability = np.nan

        rows.append({
            "label": label,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "uncertain_count": uncertain_count,
            "blank_count": blank_count,
            "auprc": auprc,
            "auroc": auroc,
            "brier": brier,
            "ece": ece,
            "pn_median_separability": pn_separability,
        })

    pd.DataFrame(rows).to_csv(out_path, index=False, encoding="utf-8-sig")


# =========================
# Main
# =========================

def main():
    seed_everything(SEED)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "checkpoints").mkdir(parents=True, exist_ok=True)

    train_df = pd.read_csv(TRAIN_MANIFEST_PATH)
    profile_val_df = pd.read_csv(PROFILE_VAL_MANIFEST_PATH)
    test_df = pd.read_csv(TEST_MANIFEST_PATH)

    train_df["split"] = "train"
    profile_val_df["split"] = "profile_val"
    test_df["split"] = "test"

    df = pd.concat([train_df, profile_val_df, test_df], ignore_index=True)

    global IMAGE_COL
    IMAGE_COL = find_image_col(df)

    for label in LABELS:
        if label not in df.columns:
            raise ValueError(f"Missing label column: {label}")

    print("Device:", DEVICE)
    print("Image column:", IMAGE_COL)
    print("Image root:", IMAGE_ROOT)
    print("Train:", len(train_df))
    print("Profile val:", len(profile_val_df))
    print("Test:", len(test_df))

    check_image_paths(train_df, IMAGE_COL, n=20)

    train_tf = T.Compose([
        T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        T.RandomHorizontalFlip(p=0.5),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]),
    ])

    eval_tf = T.Compose([
        T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]),
    ])

    train_ds = CheXpertTeacherDataset(train_df, IMAGE_COL, train_tf)
    profile_val_ds = CheXpertTeacherDataset(profile_val_df, IMAGE_COL, eval_tf)
    test_ds = CheXpertTeacherDataset(test_df, IMAGE_COL, eval_tf)

    train_loader = DataLoader(
        train_ds,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=(DEVICE == "cuda"),
    )

    profile_val_loader = DataLoader(
        profile_val_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(DEVICE == "cuda"),
    )

    test_loader = DataLoader(
        test_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(DEVICE == "cuda"),
    )

    model = build_model(num_labels=len(LABELS)).to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    best_val_macro_auprc = -1.0
    best_path = OUT_DIR / "checkpoints" / "best_teacher.pt"

    for epoch in range(1, EPOCHS + 1):
        model.train()

        running_loss = 0.0
        n_batches = 0

        for batch in train_loader:
            images = batch["image"].to(DEVICE)
            targets = batch["targets"].to(DEVICE)
            masks = batch["masks"].to(DEVICE)

            logits = model(images)
            loss = masked_bce_with_logits(logits, targets, masks)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            n_batches += 1

        train_loss = running_loss / max(n_batches, 1)

        val_pred = predict(model, profile_val_loader)
        val_macro_auprc = compute_macro_auprc(val_pred)

        print(
            f"Epoch {epoch}/{EPOCHS} | "
            f"train_loss={train_loss:.4f} | "
            f"profile_val_macro_auprc={val_macro_auprc:.4f}"
        )

        if val_macro_auprc > best_val_macro_auprc:
            best_val_macro_auprc = val_macro_auprc

            torch.save({
                "model_state_dict": model.state_dict(),
                "labels": LABELS,
                "image_size": IMAGE_SIZE,
                "best_val_macro_auprc": best_val_macro_auprc,
                "epoch": epoch,
                "image_col": IMAGE_COL,
                "image_root": IMAGE_ROOT,
            }, best_path)

            print(f"Saved best checkpoint: {best_path}")

    print("Loading best checkpoint...")
    ckpt = torch.load(best_path, map_location=DEVICE)
    model.load_state_dict(ckpt["model_state_dict"])

    profile_val_pred = predict(model, profile_val_loader)
    test_pred = predict(model, test_loader)

    save_long_predictions(
        profile_val_df,
        profile_val_pred,
        OUT_DIR / "teacher_profile_val_predictions.csv",
    )

    save_long_predictions(
        test_df,
        test_pred,
        OUT_DIR / "teacher_test_predictions.csv",
    )

    save_reliability(
        profile_val_df,
        profile_val_pred,
        OUT_DIR / "teacher_reliability_profile_val.csv",
    )

    print("Done.")
    print("Best profile_val macro AUPRC:", best_val_macro_auprc)
    print("Outputs saved to:", OUT_DIR)


if __name__ == "__main__":
    main()
