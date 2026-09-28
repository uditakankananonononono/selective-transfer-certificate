# Preregistration amendment v1.1 - FROZEN

- Drafted and frozen: 2026-09-28 (Asia/Calcutta).
- Approved within the user's delegated decision scope before further Tier-1 outcome scoring.
- Supersedes v1.0 for all future Tier-1 scoring; v1.0 is retained as historical evidence.
- Original v1.0 remains verbatim and frozen in the repository for provenance.

## Why an amendment is necessary

1. A research-agent error on 2026-09-28 exposed new-method predictions and
   observed responses on kangCrossCell, which v1.0 designated as Tier-1 held-out.
   The exact incident is in `docs/CONTAMINATION_2026-09-28.md`. kangCrossCell is
   now DEV/diagnostic only; scores there are NOT independent validation and
   may NOT tune the method or count toward a win. Zero invention outcomes were
   opened for the other 11 Tier-1 datasets. Tier-2 held-out screens untouched.
2. The pinned benchmark has only TWO contexts for Afriat. For either held-out
   context, only one context remains in training, so pairwise-concordance
   certificate and LOCO ridge are undefined under the bare v1.0 method.
   This limitation was discovered from baseline metadata before Afriat data or
   outcomes were downloaded. An explicit edge-case rule is proposed below;
   it does not exclude Afriat or silently lower the win bar.

## Proposed protocol changes (everything else in v1.0 remains as written)

- Section 3 Tier-1 validation population: exclude kangCrossCell. The frozen
  published per-dataset simple-baseline targets for the other 11 datasets
  remain exactly as in the v1.0 table. kangCrossCell's row remains in v1.0
  as historical baseline documentation, but cannot be used to claim a win.
  The completed trainMean kangCrossCell baseline-only pipeline gate remains
  valid as a pipeline check, not a model-outcome validation.
- Section 5 one-training-context case: predict the training context's mean
  perturbation delta, with ridge correction identically ZERO; certificate
  score = -1 (lowest possible prior to shrinkage) for every affected
  perturbation. No observed held-out effect is used. This is a deliberately
  conservative lower-confidence fallback. All contexts with >=2 training
  contexts retain the originally specified model and certificate except that
  a ridge fit with two training contexts uses the same fixed lambda=1 rule.
- Section 5 small-set abstention: order candidate units by (certificate score
  ascending, perturbation identifier ascending, context identifier ascending)
  and abstain on floor(0.2 * N) units per held-out evaluation set. Where N<5,
  this abstains on zero, actual coverage 100%; report that actual rate rather
  than misleadingly call it 80%.
- Section 6 Tier-1 win bar: BOTH clauses are computed over the remaining 11
  held-out datasets, preserving full-coverage >= best simple baseline on
  EACH of those 11, and >=10% relative reduction in macro risk at intended
  80% retention. Report actual achieved coverage per dataset, especially
  small sets, and the corresponding macro risk with no hidden selection.
  For each dataset where floor(0.2 * N) = 0, compute the nominal 80%-retention
  clause at the actual achieved coverage (100%). Label that row "actual coverage:
  100%" in every result table and apply the same >=10% relative risk-reduction
  requirement without relaxation. For those small datasets the full-coverage
  and nominal 80%-retention clauses partially coincide by construction. Macro
  risk aggregates the eleven per-dataset risks at their actual achieved
  coverages, compared with the originally frozen full-coverage baseline macro
  risk; no hidden selection or baseline substitution is allowed.
- All outcomes, including losses, are reported. The contaminated kangCrossCell
  outcome is labeled exploratory/invalid for validation, never erased.

## Freeze and reporting status

This dated v1.1 amendment is FROZEN. No further changes to its evaluation
population, edge-case fallback, coverage rule, target baselines or win conditions
are permitted without a NEW dated amendment approved before the affected
outcomes are opened. The only new-method outcomes seen before this freeze were
on quarantined kangCrossCell and are exploratory/invalid for validation.
This document does not claim a measured benchmark win.
