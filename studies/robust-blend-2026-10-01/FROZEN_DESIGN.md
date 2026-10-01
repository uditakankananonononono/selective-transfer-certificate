# Training-only robust blend diagnostic - October 1, 2026

Known-outcome development consistency diagnostic, not an invention claim or
independent validation. All 11 datasets / 209 units, fixed original genes,
full-cell PCC/MSE with four-decimal unit rounding; no row exclusion or tuning.

For each target context and perturbation, training contexts have that perturbation
and matched controls and exclude the target. Three components: deterministic
cell-weighted absolute treated mean minus query control; equal-context mean
training deltas; original lambda=1 ridge-corrected transfer.
Weights (absolute, meanDelta, ridge) are nonnegative quarter steps summing to one:
all 15 simplex grid points. No grid expansion. At >=3 original training contexts,
outer-LOCO rebuilds all components from the reduced training pool, using the
omitted training context's controls to predict it. Ridge residual fitting and
control centering use reduced pool only. Undefined inner PCC is -1. Rank weights
by greatest minimum LOCO PCC, then greatest mean PCC, then ascending lexicographic
weight tuple. All inner scores use unrounded PCC. No held-out target treated
response enters selection. At <3 training contexts use original ridge prediction
and label nonadaptive fallback. No target-specific hand tuning or dataset lookup.

Lock predictions and selected weights before new outcome comparisons. Primary
comparison full-coverage, no certificate/retention. Report all dataset PCC/MSE,
fixed three-predictor contrasts, inner scores, selected weights and fallbacks.
No population inference from few correlated contexts.

Mandatory win clauses: full PCC >= exact frozen published trainMean target on
EVERY dataset, and >=10% relative reduction in equal-dataset macro risk versus
that baseline. Additionally crossPatient must improve over frozen ridge, with
no hidden newly harmed datasets: report every negative difference and define
no-harm strictly as dataset PCC >= frozen ridge on each dataset. All three gates
reported separately; diagnostic pass requires all. A clean negative narrows the
search; none of these known outcomes can become independent confirmation later.

Input data official MD5 plus original dataset SHA must match. Grouped means may
stream all already exposed development groups once for efficiency; this is not
an outcome-blind confirmation claim. Only training subsets enter model choice.
