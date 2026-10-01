# Predictor ablation development result - October 1, 2026

No combined gate passes. This is a known-outcome development result on 11 datasets and 209 common units per predictor, not independent validation or an invention win. Both simplified predictors fail the all-dataset full-coverage clause. All frozen ridge scores are unchanged.

| Predictor | Full clauses passed | Macro risk reduction vs published baseline | Combined |
| --- | --- | --- | --- |
| analytic_trainMean | 5/11 | -1.78169914% | FAIL |
| frozen_ridge | 8/11 | 25.07044629% | FAIL |
| meanDelta | 7/11 | 21.63559251% | FAIL |

The dominant gain is subtracting training-context controls and transferring deltas rather than pooling absolute treated expression. meanDelta improves PCC over analytic absolute pooling on 8/11 datasets, but worsens Parekh, crossPatient and sciplex3. Ridge improves PCC over meanDelta on 7/11, ties Afriat, and worsens crossSpecies, KaggleCrossPatient and TCDD.

Hard negative: crossPatient meanDelta PCC 0.147280 vs ridge 0.262630 and analytic absolute 0.343330; the published target is 0.352110. No predictor rescues this dataset. meanDelta also fails Parekh, KaggleCrossPatient and sciplex3, so it is not a passing simplified replacement.

Analytic trainMean is the deterministic mean of the published cell-weighted absolute-expression generator, not its Gaussian sampled-cell realization. Deviations from released targets remain material on several datasets and are reported in contrasts.csv. It must not be sold as exact stochastic reproduction. No alternative baseline was substituted for the frozen targets.

Full MSE and mandatory predictor differences are in summary.csv and contrasts.csv; positive PCC differences are better, negative MSE differences are better. No outcome dropped, no tuning, all three previously failing datasets included.

Design hash edc6f55726aadc11e609b2ec9f6935ff3c8bafa10deb832eaa57ae728ac8dc9a, committed before new scores. Original official download MD5 and canonical dataset SHA were checked. One crossPatient fold-scanning call timed out before any output; recovery used a single grouped streaming pass over already exposed development outcomes, with identical predictor algebra and output-key checks. This changes I/O only, not eligibility/predictions/metrics.

Audit: 627 rows, exact common 209 keys per predictor, ridge unit PCC/MSE byte-numeric unchanged, no duplicates/nonfinite values, 33 synthetic tests pass. New full predictor vectors retained in private scratch; prediction_file_hashes.json records their hashes.

Original v1.2 LOSS and selector utility FAIL remain unchanged. Confidence filtering is prior art (PRESCRIBE); no current result establishes novelty.

Sources: https://github.com/uditakankananonononono/selective-transfer-certificate ; https://github.com/bm2-lab/scPerturBench/tree/698f8ff5ed19530bff171e4205be9b42a46a769d/Cellular_context_generalization ; https://api.figshare.com/v2/articles/28143422
