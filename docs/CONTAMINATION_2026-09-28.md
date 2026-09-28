# Contamination incident - 2026-09-28 (Asia/Calcutta)

What happened: after the specified trainMean pipeline-validation gate passed, the
research agent ran an uncommitted prototype `/tmp/dev_kang.py` over the
kangCrossCell benchmark's eight context outcomes, computing new-method Pearson
correlations and certificate scores. The reason was an attempted dev smoke-test,
but kangCrossCell was a Tier-1 evaluation dataset under frozen v1.0 and not
authorized for method-outcome inspection at that point. The agent immediately
reported the mistake. This was not a clean preregistered held-out test.

Consequence: kangCrossCell is contaminated and may be used as DEV/diagnostic only,
never as a held-out validation set or claimed benchmark win. The numbers from that
run must not tune hyperparameters, thresholds, architecture, or selection. No other
Tier-1 dataset's outcome was opened. The remaining 11 datasets are untouched.
The original v1.0 still says "each of 12" and must not be silently reinterpreted:
no Tier-1 invention scoring until a dated amendment with the revised evaluation
population and any needed method fallback is approved and frozen. Tier-2 dev and
synthetic unit work can proceed independently. All negative outcomes and deviations
remain reportable exactly.

Refusal behaviors: do not report kangCrossCell as validation; do not use its
prototype scores for optimization; do not score the other 11 Tier-1 datasets under
v1.0; do not quietly discard the contaminated row from a claimed v1.0 result.
