# Proposal 修改日志与待确认清单

> 重要提醒：课程作业说明 PDF 写明，正式提交材料不得直接使用 AI 生成文本。本文件和 `revised_fyp_proposal_form_cn.md` 只能作为结构、论证和修改方向参考。正式提交前请用自己的语言重写，补充导师确认内容，并核对所有引用。

## 1. 已识别的正确 Proposal 格式

本次主要依据以下文件判断格式：

| 来源文件 | 用途 |
| --- | --- |
| `agent.md` | 项目内已整理的 FYP proposal 写作规则和课程材料摘要。 |
| `E:\2026.04\Thesis\5.1 Description of Coursework_v3.0-SWE-Project Proposal  Presentation 2026-04.pdf` | 作业说明、评分标准、字数范围、提交要求和评分 rubric。 |
| `E:\2026.04\Fundamental Research\Sample Undergraduate FYP Proposal Form with description.pdf` | 正式 proposal form 的 Section I-VI 结构。 |
| `E:\2026.04\Thesis\042025 Thesis Proposal Template.docx` | Thesis chapter 模板参考，但不作为本次 proposal form 的主格式。 |
| `improved_proposal.md` | 当前草稿的主要内容来源。 |
| `E:\2026.04\Thesis\参考文献` 和 `Initial/*.md` | 已收集文献、文献矩阵、topic feasibility report 和缺失文献建议。 |

正确的 proposal form 结构应包括：

1. Section I：学生信息
2. Section II：导师信息
3. Section III：企业/行业合作信息
4. Section IV：学生声明
5. Section V：导师审批
6. Section VI：项目报告 / 论文信息

Section VI 的内容顺序应为：

1. Title：题目
2. Commencement Date：开始日期
3. Academic Year / Semester：学年 / 学期
4. Introduction / Problem Statement：引言 / 问题陈述
5. Aims and Objectives：研究目标与具体目标
6. Background Study / Literature Review：背景研究 / 文献综述
7. Research Methodology & Ethics：研究方法与伦理
8. Rationale / Timeliness / Potential Project Significance：研究动机、时效性与项目意义
9. Expected Outcomes and/or Concluding Remarks：预期成果 / 总结性说明
10. Gantt Chart：甘特图
11. Resources：资源需求
12. Bibliography or Key References：参考文献
13. Appendix: Literature Review Synthesis Matrix：附录，文献综述综合矩阵

作业说明中的重点要求：

| 要求 | 具体说明 |
| --- | --- |
| 总字数 | 2000-3000 words，不包括题目、文内 citation 和参考文献；如导师允许，可略微超出。 |
| 题目 | 不超过 20 个英文单词。 |
| 引言 / 问题陈述 | 300-500 words，需要明确背景、问题和项目要解决的 gap。 |
| 研究目标与具体目标 | 100-200 words，目标应具体、可实现、可衡量，且彼此区分清楚。 |
| 文献综述 | 1000-1300 words，需要包含 literature review synthesis matrix。 |
| 研究方法与伦理 | 300-500 words，需要说明研究设计、方法、选择理由和伦理考虑。 |
| 项目意义 | 100-200 words，需要说明研究的重要性和时效性。 |
| 预期成果 | 200-300 words，需要是具体、可衡量的成果，例如系统、模型、框架、算法流程或改进方法。 |
| 参考文献 | 10-20 篇核心文献，使用 APA 格式。 |
| 项目计划 | 需要包含 Gantt chart。 |

## 2. 当前草稿与要求格式的差距

| 检查项目 | 当前草稿问题 | 已做修改 |
| --- | --- | --- |
| 整体结构 | `improved_proposal.md` 使用的是 thesis chapter 结构，例如 Chapter 1 Introduction、Chapter 2 Literature Review、Chapter 3 Methodology、Chapter 4 Preliminary Findings。 | 已改为正式 Undergraduate FYP Proposal Form 的 Section I-VI 结构。 |
| 行政信息 | 原草稿没有完整对应学生信息、导师信息、企业信息、学生声明和导师审批等表格。 | 已加入 Section I-V，并保留待填写占位符。 |
| Section VI 顺序 | 原草稿没有按照 proposal form 的顺序组织内容。 | 已按上传 PDF 的顺序重排全部内容。 |
| 研究范围 | 原方法部分内容很丰富，但范围偏大，包含 teacher、多个指标、oracle、calibration、profile thresholds 和较长讨论。 | 已保留核心想法，但把范围压缩为 CheXpert、一个 teacher、一个 backbone、四种固定策略、一个 profile-guided strategy 和 validation oracle reference。 |
| Research gap | 原草稿的 gap 较强，但分散在 chapter-style sections 中。 | 已压缩并前置到 problem statement 与 literature synthesis 中，重点改为“训练所有候选 final models 前的逐标签策略预测”，而不是笼统的 uncertain-label handling。 |
| Objectives | 原目标可用，但嵌在 thesis chapter 中，且细节偏多。 | 已改为一个总体 aim、三个 research questions 和四个可衡量 objectives。 |
| Literature review | 原文献综述较像 thesis chapter，篇幅和层次偏重。 | 已改为 proposal-level critical synthesis，同时保留你原稿中的小标题：CheXpert strategies、report-derived discrepancy、label-wise reliability、long-tail challenge、teacher reliability、distributional evidence。 |
| Methodology | 原方法部分太长，且 ethics 没有单独整合。 | 已重写为更紧凑的 methodology & ethics，包含实验阶段、数据划分、模型设置、profile mapping、评价指标和伦理说明。 |
| Expected outcomes | 原预期成果部分更像 preliminary findings 和结果预测。 | 已改为更具体的交付物：数据准备与标签策略生成模块、profiling pipeline、profile-guided final model、实验比较与 strategy selection guideline。 |
| Gantt chart 和 resources | 原草稿有 appendix 计划，但不在正式 form 的主要位置。 | 已加入主 proposal 的 Gantt chart 和 resources table。 |
| References | 部分文献条目不完整或需要核验。 | 已保留 10-20 篇核心参考文献，并对需要确认的 bibliographic details 做出标记。 |

## 3. 主要内容修改

1. 将原本的 thesis-style 草稿重构为上传文件要求的 SCDS Undergraduate FYP Proposal Form 结构。

2. 强化并收窄 problem statement：

   新版不再声称 uncertain labels 从未被研究。CheXpert 原论文已经比较过 uncertain-label strategies，并发现不同 pathology labels 对策略的偏好不同。新版 gap 改为：现有策略偏好通常需要在训练候选模型后才知道，而本 FYP 研究能否利用 teacher-assisted label-wise profile，在训练所有 final candidate models 之前解释并预测 strategy choice。

3. 控制本科 FYP 范围：

   新版以 CheXpert 作为唯一核心数据集，固定一个 backbone、一个 teacher model、四种 fixed strategies、一个 profile-guided strategy 和一个 validation oracle reference。外部数据集验证、大型基础模型、多 seed 大规模训练和真实临床部署都被明确放在核心范围之外。

4. 增强研究逻辑链：

   新版 proposal 的逻辑链为：report-derived uncertain labels -> label-wise strategy differences -> long-tailed imbalance -> teacher reliability risk -> need for label-wise uncertainty profiling -> experimental evaluation。

5. 加入更明确的 research questions：

   RQ1 关注 uncertain samples 的 teacher-score distribution 更像 positive、negative 还是 ambiguous。RQ2 评价 profile 是否能预测 validation-oracle strategy。RQ3 评价 profile-guided strategy 是否比固定策略更稳定。

6. 加入本地 CheXpert 初步统计作为动机：

   新版 problem statement 使用了本地 frontal CheXpert manifest 的初步统计，例如 Pneumonia、Atelectasis 和 Consolidation 的 uncertain ratio 较高。这能更好说明 uncertainty burden 在不同 labels 间差异明显。

7. 改进 methodology 与 ethics：

   新版方法部分包含 dataset preparation、patient-level split control、teacher model setup、score-distribution profiling、Type A-D mapping、evaluation metrics 和 ethical considerations。

8. 加入项目计划和资源需求：

   新版 proposal 包含从 2026 年 6 月到 2027 年 4 月的月度 Gantt chart，以及 dataset、software、hardware、references、supervision 和 risk control 等资源说明。

9. 加入引用核验提醒：

   对依赖具体文献细节的 claim 尽量保留 citation。对 bibliographic details 不完整的文献，已用 `[publication details to verify]` 或类似说明提醒后续核验。

## 4. 仍需导师确认或进一步决定的薄弱点

| 待确认项目 | 为什么重要 | 建议处理方式 |
| --- | --- | --- |
| 最终题目 | 已将题目改为 `Label-wise Strategy Selection for Uncertain Labels in Imbalanced Multi-label Chest X-ray Classification`。该题目不直接绑定 CheXpert，更像一个通用方法研究；CheXpert 将在 methodology 中作为主实验数据集说明。 | 与导师确认是否接受不在题目中写 CheXpert；若导师希望题目体现数据集，可改回带 CheXpert 的版本。 |
| 专业和个人信息 | Proposal form 需要准确填写行政信息。 | 填入姓名、学号、专业、导师姓名和 approval status。 |
| 中文草稿是否可作为最终语言 | 官方表格和作业说明为英文。 | 当前中文版仅用于预览和修改，正式提交前应翻译并改写成正式 academic English。 |
| 数据集版本 | 本地已有 CheXpert small manifest 和 frontal subset。 | 确认最终使用 all views、frontal views only，还是因为算力限制使用固定子集。 |
| 数据访问与授权 | CheXpert 有使用条款和数据访问要求。 | 确认你有权将该数据集用于 FYP，并在最终 proposal 中正确引用数据集和使用条款。 |
| Patient-level split | 这是防止 data leakage 的关键。 | 根据 manifest 检查 split implementation，确保同一 patient 不会同时出现在 train、profile-validation 和 test 中。 |
| 官方 validation / test labels | CheXpert public test labels 可能不能完整获得。 | 确认使用 official validation set、internal held-out split，还是两者结合。 |
| Backbone 选择 | DenseNet-121 和 ResNet-50 都合理，但同时做多个 backbone 会扩大范围。 | 与导师确认一个主 backbone，其余作为 future work。 |
| Teacher training strategy | U-Ignore teacher 逻辑合理，但对 definite samples 少的 labels 可能较弱。 | 确认 teacher 使用 U-Ignore、U-Soft，还是另一个更稳定的策略。 |
| Imbalance-aware loss | Asymmetric loss 更贴合 multi-label imbalance，但实现和调参会增加工作量。 | 决定主实验使用 BCE 保持简单，还是使用 asymmetric loss 增强 imbalance handling。 |
| Type A-D thresholds | 当前 thresholds 属于 operational design，还不是经验固定值。 | 让导师确认 threshold-tuning procedure，尤其是否只能在 profile-validation split 上设定。 |
| U-Soft target | 固定 0.5 简单，但在 rare labels 上可能高估 positive signal。 | 确认 U-Soft 使用固定 0.5、label-prevalence-based soft target，还是 teacher-calibrated soft target。 |
| Validation oracle | Oracle 适合作为 upper-bound reference，但训练成本较高，也可能 validation-overfit。 | 确认 oracle 是必做、选做，还是简化为 fixed baselines 中的 per-label best strategy。 |
| 评价指标 | 当前 proposal 优先使用 AUPRC 和 calibration。 | 确认是否也加入 F1、Recall、Precision，以便更符合 coursework 的可解释性。 |
| Gantt chart 日期 | 当前时间表假设从 2026 年 6 月到 2027 年 4 月。 | 根据实际 FYP calendar 修改月份和任务安排。 |
| Ethics statement | 公开去标识化数据通常风险较低，但学校可能仍要求 ethics declaration。 | 向导师确认是否需要正式 ethics approval 或 exemption。 |

## 5. 需要核验的参考文献与引用信息

当前 proposal 保留了以下文献，因为它们与研究主题相关；但部分 bibliographic details 需要在正式提交前核验：

| 文献 | 需要核验的问题 |
| --- | --- |
| Holste et al. (2022) | Workshop 名称、完整作者列表、页码和出版信息需要确认。 |
| Holste et al. (2024) | Volume、issue、article number 和完整作者列表需要确认。 |
| Lin et al. (2025) | 当前按 arXiv / preprint 处理；需要确认是否已有正式出版版本。 |
| Jain et al. (2021a) | VisualCheXbert 的正式发表 venue 和 bibliographic details 需要确认。 |
| Jain et al. (2021b) | 当前按 arXiv 处理；需要确认是否已有正式发表版本。 |
| Ye et al. (2026) | 这是本地文献集中较新的文献，需要仔细核验完整作者列表、volume、pages 和 DOI。 |
| 本地 CheXpert manifest statistics | 这些是本地 CSV summary 生成的初步统计，不是已发表文献。正式 proposal 中应写成 preliminary dataset audit results，而不是 literature facts。 |

## 6. 后续可考虑补充的引用

以下引用不是当前 proposal 必须加入的内容，但如果导师允许参考文献略多，可以增强最终英文版的支撑力度：

1. 保留 Cheng and Vasconcelos (2024) 这类专门讨论 multi-label calibration 的文献，因为它直接支撑 teacher reliability。
2. 如果最终方法直接使用 teacher probabilities，可以补充 pseudo-label confidence 或 selective training 相关文献。
3. 可以增加一篇 CheXpert / CXR noisy-label handling 文献，加强 noisy-label motivation。
4. 如果学校要求 data governance，可以加入 CheXpert 官方数据说明或数据许可引用。
5. 如果导师希望 methodology 更严谨，可以补充 patient-level split 或 medical imaging evaluation 相关方法文献。

## 7. 已生成文件

| 文件 | 用途 |
| --- | --- |
| `revised_fyp_proposal_form_cn.md` | 按上传 proposal form 结构重排后的中文版完整工作草稿。 |
| `proposal_change_log_and_weak_areas_cn.md` | 中文版格式诊断、修改日志、薄弱点和引用核验清单。 |
