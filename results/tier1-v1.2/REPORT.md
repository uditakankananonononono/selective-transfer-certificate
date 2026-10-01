# Frozen Tier-1 v1.2 result - October 1, 2026

**Overall outcome: LOSS.** Full coverage fails on KaggleCrossPatient, crossPatient and sciplex3. The retained macro-risk clause passes, but both clauses are mandatory. No model changes were made after outcome opening.

All 11 datasets / 209 frozen units were scored from published locked predictions. PCC/MSE use all cells over 5,000 aligned genes, each unit rounded to four decimals, following the pre-outcome v1.2 clarification. Targets below are exact means from the pinned published artifact, not rounded preregistration display values.

| dataset | units | actual_coverage | full_pcc_delta | baseline_pcc_delta | full_pass | retained_pcc_delta | full_mse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Afriat | 4 | 1.0 | 0.9450999999999999 | 0.68675 | True | 0.9450999999999999 | 0.0015999999999999999 |
| Haber | 24 | 0.8333333333333334 | 0.7557833333333335 | 0.5007333333333334 | True | 0.75684 | 0.004491666666666667 |
| KaggleCrossCell | 24 | 0.8333333333333334 | 0.5425041666666667 | 0.42192500000000005 | True | 0.49814500000000006 | 0.006733333333333333 |
| KaggleCrossPatient | 30 | 0.8 | 0.5996799999999999 | 0.60979 | False | 0.7055124999999999 | 0.0031333333333333335 |
| McFarland | 42 | 0.8095238095238095 | 0.6398428571428572 | 0.38315238095238097 | True | 0.6895823529411765 | 0.007392857142857144 |
| Parekh | 30 | 0.8 | 0.2690633333333333 | 0.26403333333333334 | True | 0.32971249999999996 | 0.00283 |
| TCDD | 6 | 0.8333333333333334 | 0.7007833333333333 | 0.2391 | True | 0.67286 | 0.0034833333333333335 |
| crossPatient | 10 | 0.8 | 0.26263 | 0.35211 | False | 0.27465 | 0.00512 |
| crossSpecies | 4 | 1.0 | 0.5470999999999999 | 0.340325 | True | 0.5470999999999999 | 0.03497499999999999 |
| kangCrossPatient | 8 | 0.875 | 0.9764875 | 0.94865 | True | 0.9753714285714288 | 0.0016499999999999998 |
| sciplex3 | 27 | 0.8148148148148148 | 0.3148518518518519 | 0.3196259259259259 | False | 0.3476090909090909 | 0.005544444444444445 |

Macro baseline risk: 0.5394368205868207
Macro retained method risk: 0.38704701159802757
Relative risk reduction: 0.28249797413350003
All full-coverage clauses passed: False
Risk clause passed: True
Overall win: False

Retention worsened PCC on KaggleCrossCell, TCDD and kangCrossPatient. This is a selector negative, not suppressed by the aggregate risk result.

This result does not isolate the value of the certificate from the predictor: its frozen comparison is against the full-coverage published baseline, not matched-coverage baselines. A follow-up selection-value experiment requires a new dated design and untouched independent evaluation data. These 11 outcomes must never become fresh independent validation after tuning.

Tier-2 remains parked due to the two-development-line calibration limitation; its four held-out screens were not opened. kangCrossCell remains contaminated development-only and is absent from this result.

Publication independently verified by remote fetch at 6027b43611a1cc34cd4c75093cf971ed188c59ef before scoring, with all 21 protocol/source/ledger/lock blobs checked. publication_receipt.json records those facts. The receipt is provenance, not permission.

Sources: https://github.com/uditakankananonononono/selective-transfer-certificate ; https://github.com/bm2-lab/scPerturBench/tree/698f8ff5ed19530bff171e4205be9b42a46a769d/Results/Cellular_context_ood ; https://api.figshare.com/v2/articles/28143422

## Novelty correction

The original novelty pass missed PRESCRIBE's uncertainty-guided filtering and
GPerturb's Bayesian effect uncertainty. Confidence filtering per se is not a new
invention. See docs/PRIOR_ART_CORRECTION_2026-10-01.md. The exact donor-transfer
statistic/controlled follow-up remains unproven as a novel contribution.
