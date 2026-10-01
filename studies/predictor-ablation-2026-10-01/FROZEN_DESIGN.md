# Predictor ablation development study - October 1, 2026

Frozen before new predictor scores. All 11 datasets and 209 units are already
known-outcome development. This is not untouched independent validation, a new
invention win or a replacement for the frozen v1.2 LOSS. No dataset excluded,
no tuning, no changed gene set, no selector used in the primary comparison.

Three predictors, full coverage on exact original evaluation keys:
1. Cell-weighted absolute treated-expression mean over other contexts, minus
   target matched-control mean for delta scoring. This is the deterministic
   mean of the published trainMean baseline, NOT its randomly generated cells.
   Published trainMean adds Gaussian noise with target-control standard deviation;
   exact released unit scores need not equal this analytic reconstruction.
   Label our numbers deterministic analytic trainMean, retain released baseline
   scores as the external target, and report their differences without claiming
   exact stochastic reproduction.
2. Equal-context mean of training treated-minus-matched-control deltas,
   called meanDelta. Contexts contribute equally, not by treated-cell count.
3. Existing frozen ridge-corrected transfer, using original locked predictions
   and original scores unchanged. Lambda=1, original one-context fallback.

Full-cell delta PCC and expression MSE over all 5,000 unique aligned genes,
unit scores rounded to four decimals before aggregation, following v1.2.
Common eligible training contexts match the existing frozen ridge predictor:
other contexts with the perturbation and matched controls. For predictor 1,
if any other treated context lacks matched controls, explicitly report the
source-matching gap rather than silently label a subset published pooling.
Missing/no training, nonfinite or undefined metrics are failures, never silently
dropped. Canonical original data SHA and official download MD5 must match.

Descriptive gate for each simplified predictor: dataset-mean full PCC >= exact
pinned published trainMean target on EVERY one of 11 datasets, AND >=10% relative
reduction in equal-dataset macro risk against that same published target.
Report both clauses and every failure. The original frozen ridge is a comparator,
not a newly tested invention. No new overall win if either clause fails.

Mandatory ablations: ridge minus meanDelta; meanDelta minus cell-weighted absolute
pooling. Report full PCC and MSE per dataset, all original failed datasets,
unit-level outputs, and macro risks. Positive values in PCC differences mean
better; lower MSE is better. Also report analytic trainMean minus released target.
No population confidence claim from correlated rows. No post-score changes.

Sources: pinned source commit 698f8ff5ed19530bff171e4205be9b42a46a769d,
https://github.com/bm2-lab/scPerturBench/tree/698f8ff5ed19530bff171e4205be9b42a46a769d/Cellular_context_generalization
