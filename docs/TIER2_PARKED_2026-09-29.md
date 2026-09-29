# Tier-2 design verdict - PARKED (2026-09-29 IST)

This is a methodological dead-end under the FROZEN design, not a failed
benchmark experiment or an invitation to alter its targets after the fact.
The two preregistered single-gene development cell lines, replogle22k562 and
nadig25hepg2, share 1,511 perturbations and 7,595 genes. The third development
dataset, wessels23, has only two-gene combinations and does not supply an
independent third measurement of the single-gene effects. Leaving either
single-gene development line out gives only one training line. Mean pairwise
cross-context concordance is undefined with one line. The conservative one-line
fallback in v1.1 has certificate -1 for every perturbation, so it cannot rank
predictions or support the proposed selective-transfer calibration. Likewise,
with one remaining line there is no independent cross-line residual with which
to fit the ridge correction on a development-only leave-one-line-out split.

No Tier-2 held-out line (replogle22rpe1, nadig25jurkat, arch1, kaden25rpe1)
was downloaded or opened. No claimed Tier-2 win or loss was scored. The two
development datasets were streamed to grouped means; raw files were deleted.
See DEV_METADATA_2026-09-28.md for source hashes and exact counts.

Decision: Tier-2 scoring is PARKED under v1.0/v1.1. Do not secretly treat a
held-out dataset as development, or treat wessels23 combination labels as
single-gene cross-line measurements. A future separate attempt needs an
additional *independent* single-gene development line with sufficient
perturbation/gene overlap and a new dated preregistration, frozen before opening
any further held-out outcomes. The Tier-1 11-dataset track continues under
v1.1 and is not blocked by this verdict.
