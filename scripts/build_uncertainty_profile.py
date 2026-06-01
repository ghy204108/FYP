from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance, mannwhitneyu


# =========================
# Config
# =========================

PRED_PATH = Path(r"D:\Codex\CodexProjects\FYP\Teacher_model\teacher_profile_val_predictions.csv")
RELIABILITY_PATH = Path(r"D:\Codex\CodexProjects\FYP\Teacher_model\teacher_reliability_profile_val.csv")

OUT_DIR = Path(r"D:\Codex\CodexProjects\FYP\uncertainty_profile")
PROFILE_FEATURES_OUT = OUT_DIR / "profile_features.csv"
STRATEGY_MAPPING_OUT = OUT_DIR / "strategy_mapping.csv"

MIN_POSITIVE_SUPPORT = 100
MIN_NEGATIVE_SUPPORT = 100
MAX_ECE = 0.15
MIN_PN_SEPARABILITY = 0.20

HIGH_OVERLAP_THRESHOLD = 0.60
MIN_EFFECT_SIZE = 0.20
RELATIVE_DISTANCE_MARGIN = 0.20


# =========================
# Metrics
# =========================

def overlap_ratio(a, b, bins=50):
    a = np.asarray(a)
    b = np.asarray(b)

    if len(a) == 0 or len(b) == 0:
        return np.nan

    hist_a, edges = np.histogram(a, bins=bins, range=(0.0, 1.0), density=True)
    hist_b, _ = np.histogram(b, bins=edges, density=True)

    width = edges[1] - edges[0]
    overlap = np.minimum(hist_a, hist_b).sum() * width

    return float(overlap)


def rank_biserial_effect_size(a, b):
    """
    Positive value means scores in a tend to be larger than scores in b.
    """
    a = np.asarray(a)
    b = np.asarray(b)

    if len(a) == 0 or len(b) == 0:
        return np.nan, np.nan

    u_stat, p_value = mannwhitneyu(a, b, alternative="two-sided")
    n_a = len(a)
    n_b = len(b)

    rbc = (2.0 * u_stat) / (n_a * n_b) - 1.0

    return float(rbc), float(p_value)


def safe_float(x):
    try:
        return float(x)
    except Exception:
        return np.nan


# =========================
# Profile Feature Extraction
# =========================

def compute_profile_features(pred_df, reliability_df):
    rows = []

    labels = sorted(pred_df["label"].unique())

    reliability_df = reliability_df.copy()
    reliability_df["positive_count"] = reliability_df["positive_count"].apply(safe_float)
    reliability_df["negative_count"] = reliability_df["negative_count"].apply(safe_float)
    reliability_df["uncertain_count"] = reliability_df["uncertain_count"].apply(safe_float)
    reliability_df["auprc"] = reliability_df["auprc"].apply(safe_float)
    reliability_df["auroc"] = reliability_df["auroc"].apply(safe_float)
    reliability_df["brier"] = reliability_df["brier"].apply(safe_float)
    reliability_df["ece"] = reliability_df["ece"].apply(safe_float)
    reliability_df["pn_median_separability"] = reliability_df["pn_median_separability"].apply(safe_float)

    reliability_by_label = reliability_df.set_index("label").to_dict(orient="index")

    for label in labels:
        sub = pred_df[pred_df["label"] == label].copy()

        p_scores = sub[sub["true_state"] == "positive"]["score"].astype(float).to_numpy()
        n_scores = sub[sub["true_state"] == "negative"]["score"].astype(float).to_numpy()
        u_scores = sub[sub["true_state"] == "uncertain"]["score"].astype(float).to_numpy()

        rel = reliability_by_label.get(label, {})

        if len(p_scores) == 0 or len(n_scores) == 0 or len(u_scores) == 0:
            rows.append({
                "label": label,
                "n_positive": len(p_scores),
                "n_negative": len(n_scores),
                "n_uncertain": len(u_scores),
                "profile_status": "insufficient_groups",
            })
            continue

        d_u_p = wasserstein_distance(u_scores, p_scores)
        d_u_n = wasserstein_distance(u_scores, n_scores)

        if d_u_p < d_u_n:
            closer_to = "positive"
            relative_distance_margin = (d_u_n - d_u_p) / max(d_u_p, 1e-12)
        else:
            closer_to = "negative"
            relative_distance_margin = (d_u_p - d_u_n) / max(d_u_n, 1e-12)

        overlap_u_p = overlap_ratio(u_scores, p_scores)
        overlap_u_n = overlap_ratio(u_scores, n_scores)

        rbc_u_vs_n, mw_p_u_vs_n = rank_biserial_effect_size(u_scores, n_scores)
        rbc_u_vs_p, mw_p_u_vs_p = rank_biserial_effect_size(u_scores, p_scores)

        median_p = float(np.median(p_scores))
        median_n = float(np.median(n_scores))
        median_u = float(np.median(u_scores))

        row = {
            "label": label,

            "n_positive": len(p_scores),
            "n_negative": len(n_scores),
            "n_uncertain": len(u_scores),

            "median_positive": median_p,
            "median_negative": median_n,
            "median_uncertain": median_u,

            "mean_positive": float(np.mean(p_scores)),
            "mean_negative": float(np.mean(n_scores)),
            "mean_uncertain": float(np.mean(u_scores)),

            "wasserstein_u_positive": float(d_u_p),
            "wasserstein_u_negative": float(d_u_n),
            "closer_to": closer_to,
            "relative_distance_margin": float(relative_distance_margin),

            "overlap_u_positive": overlap_u_p,
            "overlap_u_negative": overlap_u_n,

            "rank_biserial_u_vs_negative": rbc_u_vs_n,
            "rank_biserial_u_vs_positive": rbc_u_vs_p,
            "mannwhitney_p_u_vs_negative": mw_p_u_vs_n,
            "mannwhitney_p_u_vs_positive": mw_p_u_vs_p,

            "teacher_auprc": rel.get("auprc", np.nan),
            "teacher_auroc": rel.get("auroc", np.nan),
            "teacher_brier": rel.get("brier", np.nan),
            "teacher_ece": rel.get("ece", np.nan),
            "teacher_pn_median_separability": rel.get("pn_median_separability", np.nan),

            "profile_status": "ok",
        }

        rows.append(row)

    return pd.DataFrame(rows)


# =========================
# Type A-D Mapping
# =========================

def assign_strategy(row):
    label = row["label"]

    n_positive = safe_float(row.get("n_positive"))
    n_negative = safe_float(row.get("n_negative"))
    n_uncertain = safe_float(row.get("n_uncertain"))

    ece = safe_float(row.get("teacher_ece"))
    pn_sep = safe_float(row.get("teacher_pn_median_separability"))

    closer_to = row.get("closer_to")
    margin = safe_float(row.get("relative_distance_margin"))

    overlap_up = safe_float(row.get("overlap_u_positive"))
    overlap_un = safe_float(row.get("overlap_u_negative"))

    rbc_u_vs_n = safe_float(row.get("rank_biserial_u_vs_negative"))
    rbc_u_vs_p = safe_float(row.get("rank_biserial_u_vs_positive"))

    reasons = []

    # Gate 1: sample support
    if n_positive < MIN_POSITIVE_SUPPORT:
        reasons.append(f"positive support too low ({n_positive} < {MIN_POSITIVE_SUPPORT})")

    if n_negative < MIN_NEGATIVE_SUPPORT:
        reasons.append(f"negative support too low ({n_negative} < {MIN_NEGATIVE_SUPPORT})")

    if n_uncertain <= 0:
        reasons.append("no uncertain samples")

    # Gate 2: teacher reliability
    if not np.isnan(ece) and ece > MAX_ECE:
        reasons.append(f"ECE too high ({ece:.3f} > {MAX_ECE})")

    if np.isnan(pn_sep) or pn_sep < MIN_PN_SEPARABILITY:
        reasons.append(f"P/N separability too low ({pn_sep:.3f} < {MIN_PN_SEPARABILITY})")

    if reasons:
        return pd.Series({
            "profile_type": "Type D",
            "strategy": "U-Ignore",
            "confidence": "low",
            "reason": "; ".join(reasons),
        })

    # Gate 3: ambiguous distribution
    if (
        overlap_up >= HIGH_OVERLAP_THRESHOLD
        and overlap_un >= HIGH_OVERLAP_THRESHOLD
    ):
        return pd.Series({
            "profile_type": "Type C",
            "strategy": "U-Soft",
            "confidence": "medium",
            "reason": (
                f"uncertain overlaps both positive and negative "
                f"(overlap U-P={overlap_up:.3f}, U-N={overlap_un:.3f})"
            ),
        })

    if closer_to == "positive":
        # U should be clearly higher than N if it is positive-like.
        effect_ok = (not np.isnan(rbc_u_vs_n)) and (rbc_u_vs_n >= MIN_EFFECT_SIZE)

        if margin >= RELATIVE_DISTANCE_MARGIN and effect_ok:
            return pd.Series({
                "profile_type": "Type A",
                "strategy": "U-One",
                "confidence": "high",
                "reason": (
                    f"uncertain closer to positive; distance margin={margin:.3f}; "
                    f"effect U vs N={rbc_u_vs_n:.3f}"
                ),
            })

    if closer_to == "negative":
        # U should be clearly lower than P if it is negative-like.
        effect_ok = (not np.isnan(rbc_u_vs_p)) and (rbc_u_vs_p <= -MIN_EFFECT_SIZE)

        if margin >= RELATIVE_DISTANCE_MARGIN and effect_ok:
            return pd.Series({
                "profile_type": "Type B",
                "strategy": "U-Zero",
                "confidence": "high",
                "reason": (
                    f"uncertain closer to negative; distance margin={margin:.3f}; "
                    f"effect U vs P={rbc_u_vs_p:.3f}"
                ),
            })

    return pd.Series({
        "profile_type": "Type C",
        "strategy": "U-Soft",
        "confidence": "medium",
        "reason": (
            "distribution direction is not strong enough for U-One or U-Zero; "
            f"closer_to={closer_to}, margin={margin:.3f}, "
            f"overlap U-P={overlap_up:.3f}, overlap U-N={overlap_un:.3f}"
        ),
    })


def main():
    pred_df = pd.read_csv(PRED_PATH)
    reliability_df = pd.read_csv(RELIABILITY_PATH)

    required_pred_cols = {"label", "true_state", "score"}
    missing_pred_cols = required_pred_cols - set(pred_df.columns)
    if missing_pred_cols:
        raise ValueError(f"Prediction file missing columns: {missing_pred_cols}")

    features = compute_profile_features(pred_df, reliability_df)
    mapping = features.apply(assign_strategy, axis=1)

    result = pd.concat(
        [
            features[[
                "label",
                "n_positive",
                "n_negative",
                "n_uncertain",
                "median_positive",
                "median_negative",
                "median_uncertain",
                "wasserstein_u_positive",
                "wasserstein_u_negative",
                "closer_to",
                "relative_distance_margin",
                "overlap_u_positive",
                "overlap_u_negative",
                "rank_biserial_u_vs_negative",
                "rank_biserial_u_vs_positive",
                "teacher_auprc",
                "teacher_auroc",
                "teacher_ece",
                "teacher_brier",
                "teacher_pn_median_separability",
            ]],
            mapping,
        ],
        axis=1,
    )

    features.to_csv(PROFILE_FEATURES_OUT, index=False, encoding="utf-8-sig")
    result.to_csv(STRATEGY_MAPPING_OUT, index=False, encoding="utf-8-sig")

    print("Saved:", PROFILE_FEATURES_OUT)
    print("Saved:", STRATEGY_MAPPING_OUT)
    print()
    print(result[[
        "label",
        "profile_type",
        "strategy",
        "confidence",
        "closer_to",
        "median_positive",
        "median_negative",
        "median_uncertain",
        "teacher_auprc",
        "teacher_auroc",
        "teacher_ece",
        "teacher_pn_median_separability",
        "reason",
    ]].to_string(index=False))


if __name__ == "__main__":
    main()