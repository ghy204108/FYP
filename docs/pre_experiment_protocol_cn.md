# 预实验流程记录

本预实验的目标不是直接证明 profile-guided strategy 一定优于所有 baseline，而是验证整条 methodology pipeline 是否可执行、可复查、可复现。

## 1. 实验范围

当前使用原数据集约十分之一的子数据集，并按 patient-level separation 划分为：

- `train`
- `profile_val`
- `test`

当前重点标签：

- Cardiomegaly
- Edema
- Consolidation
- Atelectasis
- Pneumothorax
- Pleural Effusion

## 2. 标签状态

每个 label 保留四种状态：

- `P`: positive
- `N`: negative
- `U`: uncertain
- `B`: blank/missing

预实验中建议不要把 `Blank` 直接当作 definite negative。`Blank` 默认作为 missing/masked label 处理，只用于统计 missing ratio。

## 3. Teacher/Probe Model

Teacher model 用于生成逐标签 score distributions，不作为医学真值来源。

建议初始设置：

- backbone: ImageNet-pretrained DenseNet-121
- input size: 224 或 320
- teacher strategy: `U-Ignore`
- loss: masked BCE 作为 sanity check；跑通后再换 imbalance-aware loss

Teacher 训练标签处理：

| Original state | Target | Loss mask |
| --- | --- | --- |
| Positive | 1 | 1 |
| Negative | 0 | 1 |
| Uncertain | ignored | 0 |
| Blank | ignored | 0 |

## 4. Teacher Reliability

在 `profile_val` 上按 label 单独评估 teacher reliability。只使用明确的 positive/negative 样本计算：

- per-label AUPRC
- AUROC
- P/N separability
- ECE
- Brier score
- definite positive/negative support

若某 label 支撑样本不足、P/N 不可分或校准明显较差，则后续 mapping 中保守标记为 `Type D`。

## 5. Label-wise Uncertainty Profiling

对每个 label 提取三组 teacher scores：

- `scores_P`
- `scores_N`
- `scores_U`

计算 profile features：

- Wasserstein distance: `d(U, P)` 和 `d(U, N)`
- distribution overlap ratio
- median score gap
- Mann-Whitney U test
- rank-biserial effect size

判断原则：

| Profile Type | Evidence pattern | Strategy |
| --- | --- | --- |
| Type A | U 更接近 P，且 teacher 可靠 | U-One |
| Type B | U 更接近 N，且 teacher 可靠 | U-Zero |
| Type C | U 位于中间或与 P/N 高度重叠 | U-Soft |
| Type D | teacher 不可靠或 support 不足 | U-Ignore |

## 6. Final Model Comparison

预实验建议至少比较：

- all U-Zero
- all U-One
- all U-Ignore
- profile-guided

资源允许时加入：

- all U-Soft

所有 final models 应保持相同 backbone、preprocessing、train split、epoch 数和 evaluation protocol。

## 7. 预期产出

建议保留以下表格：

- `data/chexpert_label_summary*.csv`
- `results/teacher_reliability.csv`
- `results/profile_features.csv`
- `results/strategy_mapping.csv`
- `results/final_results.csv`

其中 `strategy_mapping.csv` 应包含每个 label 的 Type A-D 分类、推荐策略和主要证据指标，方便后续写入 FYP report。

