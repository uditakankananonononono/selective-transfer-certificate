# Selective transfer certificate

A preregistered experimental method for cross-context expression-response
prediction with an abstention certificate. The protocol is frozen in
`PREREG_2026-09-28_SELECTIVE_TRANSFER_v1.0_FROZEN.md` (SHA-256
`b0fc9904c668bbbc9ddfaff73e3ce5978560bab5bb7b81813b9b52751a82f399`).
No benchmark win has yet been measured. The benchmark baseline-only pipeline
validation passed; see `docs/METRIC_PROVENANCE_2026-09-28.md` for the exact
source/metric caveat. No held-out outcome has been scored.

Prototype code in `src/selective_transfer/core.py` operates on training-context
pseudobulk deltas and controls only. Its fitted transfer correction is a
one-dimensional Ridge per gene (lambda=1) on training leave-one-context-out
residuals; certificate is mean pairwise training-delta concordance shrunk by
minimum perturbed-cell count, with deterministic 80% rank retention. These
computational details need testing on development splits before any held-out
outcome scoring. Unit tests are synthetic.

Run tests: `PYTHONPATH=src python -m unittest discover -s tests -v`.
