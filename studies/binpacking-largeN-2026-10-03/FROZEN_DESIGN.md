# Frozen design: larger-N follow-up to the bin-packing replication (2026-10-03)

Status: replication/extension follow-up, NOT an invention claim, no win clause. Purpose: tighten the CIs that were wide in the 5-instance-per-class replication (studies/binpacking-replication-2026-10-03, live main 3b885f2). Frozen before any new instance is generated or scored.

## Fixed inputs (no retuning)
- Heuristics: BestFit, FirstFit, FunSearch-OR, FunSearch-Weibull (as shipped, same code as the replication eval stage), and the five ab variants exactly as in studies/binpacking-replication-2026-10-03/tuned.json (sha256 4ba3bb87e769947d471eecb473a4713eb074553cb1a9efd20af7c0b6bd4f6758). No new tuning, no new heuristics, no change to code in src/selective_transfer/binpack.py.
- Generators: same gen() as the replication.

## New test instances (never used before; fresh seeds)
- W5k: seeds 6100-6129 (30 instances, n=5000)
- U100: 7100-7129 (30, n=1000)
- LN: 8100-8129 (30, n=5000)
- BM: 9100-9129 (30, n=5000)
- U150gen: gen('U150', seed) seeds 6500-6529 (30, n=500, capacity 150, OR-like distribution; extra to OR1-4 which are not rerun).
OR1-OR4 are not rerun (already n=20 each, exact, deterministic).
The earlier 5-instance test sets (seeds 2100.., 3100.., 4100.., 5100..) are not pooled and stay reported as-is.

## Metric and analysis
- Excess over L1 bound; mean per cell, 95% percentile bootstrap CI over instances (10000 samples, seed 20261003).
- Pre-registered paired comparisons (paired bootstrap of per-instance excess difference, same seed; report mean diff and CI, no multiplicity correction, all listed are reported win or lose):
  1. FunSearch-Weibull minus BestFit on U100, LN, BM, U150gen.
  2. FunSearch-OR minus BestFit on W5k, U100, LN, BM.
  3. Matched ab minus FunSearch: ab[W5k] minus FunSearch-Weibull on W5k; ab[U150] minus FunSearch-OR on U150gen.
  4. Matched ab minus BestFit on W5k, U100, LN, BM, U150gen.
  5. Transfer gap: for each tuned ab variant, its excess on every other class minus the excess of the ab variant tuned on that class.
- Full 9 heuristic x 5 class matrix reported, no cell omitted. Equivalence check repeated (fast packer vs notebook packer, 3 instances per class, BF/FF/ab variants); any mismatch stops the run and is reported.
- Claims limited to: replicates / does not replicate the replication's descriptive findings with tighter CIs, and the measured paired differences. A prior-replication finding that is not supported is stated as such.

## Disclosure
Any deviation from this document after publication is disclosed in REPORT.md. Compute: free, local, 2 cores; expected runtime under an hour.
