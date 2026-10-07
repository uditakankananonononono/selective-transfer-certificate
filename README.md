# Selective transfer certificate

A preregistered experimental method for cross-context expression-response
prediction with a rank-based abstention certificate. Original protocol:
`PREREG_2026-09-28_SELECTIVE_TRANSFER_v1.0_FROZEN.md` (SHA-256
`b0fc9904c668bbbc9ddfaff73e3ce5978560bab5bb7b81813b9b52751a82f399`).
The dated v1.1 amendment (SHA-256
`8fd3dbf0ae0c622a77befb78d95c1bfb27fc479db7acaa73a8e0cabe58f8b6bf`)
excludes one contaminated dataset and fixes a one-context edge case.

**Frozen Tier-1 v1.2 was scored on 2026-10-01 (11 datasets, 209 units) and the overall outcome is a LOSS** (`results/tier1-v1.2/REPORT.md`): full coverage fails on KaggleCrossPatient, crossPatient and sciplex3; the retained macro-risk clause passes (0.5394 baseline to 0.3870, 28.2% relative reduction) but both clauses are mandatory. Later development-side checks (DepMap pilot donor selector, sealed h2h replicate, bin-packing replication) are reported in the commit history and `docs/`; the donor-selector direction is closed as a measured negative. The v1.2 amendment is `PREREG_2026-10-01_SELECTIVE_TRANSFER_v1.2_FROZEN.md` (SHA-256 `f502bad84a07ecd55d5e8f0e63568ec002d5205f84eb18a97a49d337cd79ab8f`). The text below describes the v1.1 state and is partly historical.

**There is no measured independent benchmark win.** A trainMean-only baseline
pipeline gate passed. After it, the agent wrongly smoke-tested the prototype
against kangCrossCell outcomes. That makes kangCrossCell *development/diagnostic
only* and invalid as independent validation. The incident is disclosed in
`docs/CONTAMINATION_2026-09-28.md`; it cannot be erased or spun into a win.
The remaining 11 Tier-1 evaluation datasets are clean as of the v1.1 freeze.
A named historical benchmark function `pearson_distance` mismatches the numeric
released `cor` convention; see `docs/METRIC_PROVENANCE_2026-09-28.md`.

Tier-2 is **parked**, not won or lost. Its two single-gene development lines
cannot furnish a cross-line leave-one-line-out concordance certificate; its
third development set contains only gene combinations. No Tier-2 held-out file
has been touched. See `docs/TIER2_PARKED_2026-09-29.md`.

Prototype code in `src/selective_transfer/core.py` operates on training-context
pseudobulk deltas and controls only. The v1.1 one-context fallback sets ridge
correction to zero and certificate to -1. The Tier-1 evaluator enforces 11
clean datasets and actual achieved coverage under the frozen rules. Synthetic
tests pass; at the v1.1 freeze no clean held-out outcome had been scored; see the v1.2 result above.

Run tests in an environment with anndata/scipy/numpy/pandas:
`PYTHONPATH=src:. python -m unittest discover -s tests -v`.
