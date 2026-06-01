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

IMAGE_ROOT = r"E:\2026.04\Thesis\CheXpert Dataset\archive"

STRATEGY_MAPPING_PATH = r"D:\Codex\CodexProjects\FYP\uncertainty_profile\strategy_mapping.csv"

OUT_DIR = Path(r"D:\Codex\CodexProjects\FYP\final_models")

LABELS = [
    "Cardiomegaly",
    "Edema",
    "Consolidation",
    "Atelectasis",
    "Pneumothorax",
    "Pleural Effusion",
]

STRATEGIES = [
    "u_zero",
    "u_one",
    "u_ignore",
    "profile_guided",
]

IMAGE_PATH_COL_CANDIDATES = ["local_path", "Path", "path", "source_path", "relative_path"]

SEED = 42
IMAGE_SIZE = 224
BATCH_SIZE = 32

# First run with 1 for sanity check. Then change to 5 or 10.
EPOCHS = 5

LR = 1e-4
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

        prefix = "CheXpert-v1.0-small" + os.sep
        if raw.startswith(prefix):
            stripped = raw[len(prefix):]
            candidates.append(os.path.join(IMAGE_ROOT, stripped))

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    raise FileNotFoundError(
        "Image file not found.\n"
        f"Original CSV path: {path_value}\n"
        "Tried:\n" + "\n".join(candidates)
    )


def parse_label_value(x):
    if pd.isna(x):
        return np.nan

    if isinstance(x, str):
        x = x.strip()
        if x.lower() in ["blank", "", "nan", "none"]:
            return np.nan

    return float(x)


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


def masked_bce_with_logits(logits, targets, masks):
    loss = nn.functional.binary_cross_entropy_with_logits(
        logits,
        targets,
        reduction="none",
    )
    loss = loss * masks
    denom = masks.sum().clamp(min=1.0)
    return loss.sum() / denom


def load_profile_guided_mapping(path):
    df = pd.read_csv(path)

    if "label" not in df.columns or "strategy" not in df.columns:
        raise ValueError("strategy_mapping.csv must contain columns: label, strategy")

    mapping = {}
    for _, row in df.iterrows():
        label = row["label"]
        strategy = str(row["strategy"]).strip()

        if strategy == "U-One":
            mapping[label] = "u_one"
        elif strategy == "U-Zero":
            mapping[label] = "u_zero"
        elif strategy == "U-Soft":
            mapping[label] = "u_soft"
        elif strategy == "U-Ignore":
            mapping[label] = "u_ignore"
        else:
            raise ValueError(f"Unknown strategy in mapping: {strategy}")

    for label in LABELS:
        if label not in mapping:
            raise ValueError(f"Missing label in strategy mapping: {label}")

    return mapping


# =========================
# Label Encoding
# =========================

def encode_one_label(value, strategy):
    v = parse_label_value(value)

    if np.isnan(v):
        return 0.0, 0.0

    if v == 1.0:
        return 1.0, 1.0

    if v == 0.0:
        return 0.0, 1.0

    if v == -1.0:
        if strategy == "u_zero":
            return 0.0, 1.0
        if strategy == "u_one":
            return 1.0, 1.0
        if strategy == "u_soft":
            return 0.5, 1.0
        if strategy == "u_ignore":
            return 0.0, 0.0

    return 0.0, 0.0


def make_targets_and_masks(row, global_strategy, profile_mapping):
    targets = []
    masks = []

    for label in LABELS:
        if global_strategy == "profile_guided":
            label_strategy = profile_mapping[label]
        else:
            label_strategy = global_strategy

        target, mask = encode_one_label(row[label], label_strategy)
        targets.append(target)
        masks.append(mask)

    return np.array(targets, dtype=np.float32), np.array(masks, dtype=np.float32)


def make_eval_targets_and_masks(row):
    """
    Evaluation uses definite positive/negative only.
    Uncertain and blank are masked out.
    """
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
        else:
            targets.append(0.0)
            masks.append(0.0)

    return np.array(targets, dtype=np.float32), np.array(masks, dtype=np.float32)


# =========================
# Dataset
# =========================

class CheXpertFinalDataset(Dataset):
    def __init__(self, df, image_col, transform, global_strategy, profile_mapping, mode):
        self.df = df.reset_index(drop=True)
        self.image_col = image_col
        self.transform = transform
        self.global_strategy = global_strategy
        self.profile_mapping = profile_mapping
        self.mode = mode

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        image_path = resolve_image_path(row[self.image_col])
        image = Image.open(image_path).convert("RGB")
        image = self.transform(image)

        if self.mode == "train":
            targets, masks = make_targets_and_masks(
                row,
                self.global_strategy,
                self.profile_mapping,
            )
        else:
            targets, masks = make_eval_targets_and_masks(row)

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
# Prediction / Metrics
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

    for j, label in enumerate(LABELS):
        mask = pred["masks"][:, j] == 1
        y_true = pred["targets"][mask, j]
        y_prob = pred["probs"][mask, j]

        if len(np.unique(y_true)) < 2:
            continue

        scores.append(average_precision_score(y_true, y_prob))

    if not scores:
        return 0.0

    return float(np.mean(scores))


def compute_per_label_metrics(model_name, split_name, pred):
    rows = []

    for j, label in enumerate(LABELS):
        mask = pred["masks"][:, j] == 1
        y_true = pred["targets"][mask, j]
        y_prob = pred["probs"][mask, j]

        positive_count = int((y_true == 1).sum())
        negative_count = int((y_true == 0).sum())

        if len(np.unique(y_true)) >= 2:
            auprc = average_precision_score(y_true, y_prob)
            auroc = roc_auc_score(y_true, y_prob)
            brier = brier_score_loss(y_true, y_prob)
            ece = compute_ece(y_true, y_prob)
        else:
            auprc = np.nan
            auroc = np.nan
            brier = np.nan
            ece = np.nan

        rows.append({
            "model_name": model_name,
            "split": split_name,
            "label": label,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "auprc": auprc,
            "auroc": auroc,
            "brier": brier,
            "ece": ece,
        })

    return rows


def save_long_predictions(model_name, split_name, df, pred, out_path):
    rows = []

    for local_i, original_i in enumerate(pred["indices"]):
        row = df.iloc[original_i]
        image_path = resolve_image_path(row[IMAGE_COL])

        for j, label in enumerate(LABELS):
            rows.append({
                "model_name": model_name,
                "split": split_name,
                "image_path": image_path,
                "label": label,
                "true_state": get_true_state(row, label),
                "eval_mask": int(pred["masks"][local_i, j]),
                "score": float(pred["probs"][local_i, j]),
            })

    pd.DataFrame(rows).to_csv(out_path, index=False, encoding="utf-8-sig")


# =========================
# Training One Strategy
# =========================

def train_one_strategy(
    strategy,
    train_df,
    profile_val_df,
    test_df,
    image_col,
    profile_mapping,
    train_tf,
    eval_tf,
):
    print()
    print("=" * 80)
    print(f"Training final model: {strategy}")
    print("=" * 80)

    strategy_out = OUT_DIR / strategy
    checkpoint_dir = strategy_out / "checkpoints"
    strategy_out.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    train_ds = CheXpertFinalDataset(
        train_df,
        image_col,
        train_tf,
        strategy,
        profile_mapping,
        mode="train",
    )

    profile_val_ds = CheXpertFinalDataset(
        profile_val_df,
        image_col,
        eval_tf,
        strategy,
        profile_mapping,
        mode="eval",
    )

    test_ds = CheXpertFinalDataset(
        test_df,
        image_col,
        eval_tf,
        strategy,
        profile_mapping,
        mode="eval",
    )

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
    best_path = checkpoint_dir / "best.pt"

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

        profile_val_pred = predict(model, profile_val_loader)
        val_macro_auprc = compute_macro_auprc(profile_val_pred)

        print(
            f"[{strategy}] Epoch {epoch}/{EPOCHS} | "
            f"train_loss={train_loss:.4f} | "
            f"profile_val_macro_auprc={val_macro_auprc:.4f}"
        )

        if val_macro_auprc > best_val_macro_auprc:
            best_val_macro_auprc = val_macro_auprc

            torch.save({
                "model_state_dict": model.state_dict(),
                "strategy": strategy,
                "labels": LABELS,
                "image_size": IMAGE_SIZE,
                "best_val_macro_auprc": best_val_macro_auprc,
                "epoch": epoch,
            }, best_path)

            print(f"[{strategy}] Saved best checkpoint: {best_path}")

    ckpt = torch.load(best_path, map_location=DEVICE)
    model.load_state_dict(ckpt["model_state_dict"])

    profile_val_pred = predict(model, profile_val_loader)
    test_pred = predict(model, test_loader)

    save_long_predictions(
        strategy,
        "profile_val",
        profile_val_df,
        profile_val_pred,
        strategy_out / "profile_val_predictions.csv",
    )

    save_long_predictions(
        strategy,
        "test",
        test_df,
        test_pred,
        strategy_out / "test_predictions.csv",
    )

    profile_val_metrics = compute_per_label_metrics(strategy, "profile_val", profile_val_pred)
    test_metrics = compute_per_label_metrics(strategy, "test", test_pred)

    return {
        "strategy": strategy,
        "best_val_macro_auprc": best_val_macro_auprc,
        "profile_val_metrics": profile_val_metrics,
        "test_metrics": test_metrics,
    }


# =========================
# Main
# =========================

def main():
    seed_everything(SEED)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

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

    profile_mapping = load_profile_guided_mapping(STRATEGY_MAPPING_PATH)

    print("Device:", DEVICE)
    print("Image column:", IMAGE_COL)
    print("Image root:", IMAGE_ROOT)
    print("Train:", len(train_df))
    print("Profile val:", len(profile_val_df))
    print("Test:", len(test_df))
    print("Profile-guided mapping:")
    for label in LABELS:
        print(f"  {label}: {profile_mapping[label]}")

    # quick path check
    print("Checking first image path...")
    print(resolve_image_path(train_df.iloc[0][IMAGE_COL]))

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

    all_profile_val_metrics = []
    all_test_metrics = []
    summary_rows = []

    for strategy in STRATEGIES:
        result = train_one_strategy(
            strategy=strategy,
            train_df=train_df,
            profile_val_df=profile_val_df,
            test_df=test_df,
            image_col=IMAGE_COL,
            profile_mapping=profile_mapping,
            train_tf=train_tf,
            eval_tf=eval_tf,
        )

        all_profile_val_metrics.extend(result["profile_val_metrics"])
        all_test_metrics.extend(result["test_metrics"])

        test_df_metrics = pd.DataFrame(result["test_metrics"])
        profile_val_df_metrics = pd.DataFrame(result["profile_val_metrics"])

        summary_rows.append({
            "model_name": strategy,
            "best_profile_val_macro_auprc": result["best_val_macro_auprc"],
            "profile_val_macro_auprc": profile_val_df_metrics["auprc"].mean(),
            "profile_val_macro_auroc": profile_val_df_metrics["auroc"].mean(),
            "profile_val_mean_brier": profile_val_df_metrics["brier"].mean(),
            "profile_val_mean_ece": profile_val_df_metrics["ece"].mean(),
            "test_macro_auprc": test_df_metrics["auprc"].mean(),
            "test_macro_auroc": test_df_metrics["auroc"].mean(),
            "test_mean_brier": test_df_metrics["brier"].mean(),
            "test_mean_ece": test_df_metrics["ece"].mean(),
        })

    per_label = pd.DataFrame(all_profile_val_metrics + all_test_metrics)
    summary = pd.DataFrame(summary_rows)

    per_label.to_csv(
        OUT_DIR / "final_results_per_label.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary.to_csv(
        OUT_DIR / "final_results_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print()
    print("Saved:", OUT_DIR / "final_results_per_label.csv")
    print("Saved:", OUT_DIR / "final_results_summary.csv")
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()