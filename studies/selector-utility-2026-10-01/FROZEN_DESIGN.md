# Development selector utility test, October 1, 2026

Frozen before calculating these new contrasts. This is known-outcome development,
not untouched independent validation, population superiority or algorithm novelty.
The original v1.2 LOSS is unchanged; PRESCRIBE prior-art correction stands.

Use all 209 existing locked/scored units from all eleven clean datasets.
No expression downloads, predictor changes, certificate tuning or row exclusions.
For each dataset retain N-floor(N/5) units under the frozen certificate order:
ascending certificate, perturbation ID, context ID; abstain lowest floor(N/5).
Full coverage and N<5 are selector-nonidentifiable, included in macro arithmetic
but explicitly labeled, not counted as successful selectors.

Contrast A: equal-dataset macro risk of certificate-retained fixed method versus
expected uniform-random matched-K retention of THAT SAME method. Expected uniform
risk equals full method risk, not the frozen published baseline risk.
Clause A: >=10% relative reduction in macro risk versus this random expectation.

Contrast B: retained method risk versus pinned published trainMean unit scores on
EXACTLY the same certificate masks. Clause B: retained method macro risk <= this
matched-mask trainMean macro risk. No mixing masks or replacing published scores.
All dataset differences, all losses, actual coverage and context composition
before/after retention are reported. Contexts are donor/cell-type/line/species
identifiers as provided; no blanket assumption that every context is a donor.

Unit PCC values are the already frozen four-decimal scores. Baseline scores come
verbatim from pinned cellular_ood_distance5000.csv, method=trainMean,
metric=pearson_distance, DEG=5000. Exact evaluation-key equality required.
Secondary adverse-effect check: full vs retained method MSE per dataset, using
same masks. No new MSE success threshold or retrospective primary substitution.
No confidence interval or population claim from correlated benchmark units.
