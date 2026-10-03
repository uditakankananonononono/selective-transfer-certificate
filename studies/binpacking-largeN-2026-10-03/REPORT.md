# Larger-N bin-packing follow-up: results

Frozen design: FROZEN_DESIGN.md (live main ca88b7e). Replication/extension, no win clause, no deviations from the freeze. 30 fresh instances per class, ab variants frozen from the earlier tuning. Excess over L1 bound in %, mean [95% bootstrap CI over instances]. Equivalence check (fast vs notebook packer, 3 instances per class): 0 mismatches. U150 here is the generated OR-like class (n=500, capacity 150); OR1-OR4 were not rerun.

## Full matrix

| heuristic | W5k | U100 | LN | BM | U150 |
|---|---|---|---|---|---|
| BestFit | 4.10 [4.04, 4.17] | 7.02 [6.81, 7.25] | 1.78 [1.74, 1.81] | 5.16 [4.96, 5.36] | 5.17 [4.95, 5.41] |
| FirstFit | 4.47 [4.41, 4.53] | 8.10 [7.89, 8.33] | 1.87 [1.84, 1.91] | 5.40 [5.21, 5.60] | 5.72 [5.47, 5.99] |
| FunSearch-OR | 3.05 [3.02, 3.08] | 6.93 [6.71, 7.16] | 2.92 [2.90, 2.95] | 6.93 [6.78, 7.07] | 3.22 [2.93, 3.57] |
| FunSearch-Weibull | 0.72 [0.68, 0.76] | 10.31 [10.05, 10.58] | 0.75 [0.69, 0.81] | 14.84 [14.62, 15.06] | 12.77 [12.11, 13.46] |
| ab[BM] | 3.99 [3.94, 4.04] | 7.02 [6.80, 7.25] | 1.75 [1.71, 1.78] | 5.10 [4.88, 5.31] | 5.07 [4.83, 5.31] |
| ab[LN] | 2.99 [2.91, 3.08] | 10.55 [10.31, 10.81] | 0.27 [0.24, 0.31] | 7.35 [7.20, 7.51] | 10.79 [10.14, 11.50] |
| ab[U100] | 1.38 [1.34, 1.42] | 7.04 [6.80, 7.28] | 6.70 [6.41, 7.00] | 15.21 [15.05, 15.38] | 4.24 [3.83, 4.66] |
| ab[U150] | 2.17 [2.14, 2.20] | 6.73 [6.50, 6.95] | 2.17 [2.14, 2.20] | 9.17 [9.02, 9.31] | 3.11 [2.79, 3.43] |
| ab[W5k] | 0.71 [0.68, 0.75] | 8.31 [8.07, 8.54] | 0.67 [0.63, 0.72] | 11.57 [11.40, 11.72] | 8.55 [7.93, 9.24] |

## Paired differences in excess (percentage points, negative = first is better)

| comparison | mean diff [95% CI] |
|---|---|
| 1 FS-Weibull - BestFit | U100 | 3.29 [3.07, 3.50] |
| 1 FS-Weibull - BestFit | LN | -1.03 [-1.10, -0.95] |
| 1 FS-Weibull - BestFit | BM | 9.68 [9.41, 9.96] |
| 1 FS-Weibull - BestFit | U150 | 7.61 [7.02, 8.23] |
| 2 FS-OR - BestFit | W5k | -1.06 [-1.13, -0.98] |
| 2 FS-OR - BestFit | U100 | -0.09 [-0.19, 0.01] |
| 2 FS-OR - BestFit | LN | 1.15 [1.10, 1.19] |
| 2 FS-OR - BestFit | BM | 1.76 [1.65, 1.87] |
| 3 ab[W5k] - FS-Weibull | W5k | -0.01 [-0.05, 0.04] |
| 3 ab[U150] - FS-OR | U150 | -0.12 [-0.32, 0.10] |
| 4 ab[W5k] - BestFit | W5k | -3.39 [-3.46, -3.32] |
| 4 ab[U100] - BestFit | U100 | 0.02 [-0.19, 0.23] |
| 4 ab[LN] - BestFit | LN | -1.50 [-1.56, -1.45] |
| 4 ab[BM] - BestFit | BM | -0.07 [-0.12, -0.02] |
| 4 ab[U150] - BestFit | U150 | -2.06 [-2.33, -1.79] |
| 5 transfer ab[W5k] on U100 - ab[U100] on U100 | 1.26 [1.09, 1.44] |
| 5 transfer ab[W5k] on LN - ab[LN] on LN | 0.40 [0.35, 0.45] |
| 5 transfer ab[W5k] on BM - ab[BM] on BM | 6.47 [6.30, 6.63] |
| 5 transfer ab[W5k] on U150 - ab[U150] on U150 | 5.44 [4.86, 6.10] |
| 5 transfer ab[U100] on W5k - ab[W5k] on W5k | 0.67 [0.62, 0.71] |
| 5 transfer ab[U100] on LN - ab[LN] on LN | 6.43 [6.14, 6.73] |
| 5 transfer ab[U100] on BM - ab[BM] on BM | 10.11 [9.83, 10.39] |
| 5 transfer ab[U100] on U150 - ab[U150] on U150 | 1.13 [0.86, 1.41] |
| 5 transfer ab[LN] on W5k - ab[W5k] on W5k | 2.28 [2.20, 2.37] |
| 5 transfer ab[LN] on U100 - ab[U100] on U100 | 3.51 [3.28, 3.73] |
| 5 transfer ab[LN] on BM - ab[BM] on BM | 2.26 [2.12, 2.40] |
| 5 transfer ab[LN] on U150 - ab[U150] on U150 | 7.68 [7.11, 8.30] |
| 5 transfer ab[BM] on W5k - ab[W5k] on W5k | 3.28 [3.21, 3.34] |
| 5 transfer ab[BM] on U100 - ab[U100] on U100 | -0.03 [-0.24, 0.19] |
| 5 transfer ab[BM] on LN - ab[LN] on LN | 1.48 [1.42, 1.53] |
| 5 transfer ab[BM] on U150 - ab[U150] on U150 | 1.97 [1.66, 2.26] |
| 5 transfer ab[U150] on W5k - ab[W5k] on W5k | 1.46 [1.42, 1.49] |
| 5 transfer ab[U150] on U100 - ab[U100] on U100 | -0.32 [-0.48, -0.16] |
| 5 transfer ab[U150] on LN - ab[LN] on LN | 1.90 [1.86, 1.94] |
| 5 transfer ab[U150] on BM - ab[BM] on BM | 4.07 [3.93, 4.20] |

## Findings (descriptive)

1. Earlier findings replicate with tight CIs. FunSearch-Weibull is far worse than Best Fit off its class (U100 +3.29, BM +9.68, U150 +7.61 points) and better only on LN (-1.03). FunSearch-OR is better than Best Fit on W5k (-1.06), indistinguishable on U100 (-0.09 [-0.19, 0.01]), worse on LN (+1.15) and BM (+1.76).
2. Matched-distribution ab vs FunSearch: no detectable difference. ab[W5k] minus FunSearch-Weibull on W5k -0.01 [-0.05, 0.04]; ab[U150] minus FunSearch-OR on U150 -0.12 [-0.32, 0.10]. A grid-tuned two-parameter rule matches the evolved heuristic in-distribution here; this does not show it beating it.
3. Matched ab vs Best Fit: large gains where structure exists (W5k -3.39, LN -1.50, U150 -2.06), essentially none on U100 (0.02 [-0.19, 0.23], tuning found nothing) and a very small one on BM (-0.07 [-0.12, -0.02], near-Best-Fit variant).
4. Transfer gap is large and consistent: tuned ab variants lose between about 0.4 and 10 points off-distribution (e.g. ab[U100] on BM +10.11 vs the BM-tuned variant, ab[LN] on U150 +7.68). Two cases are slightly negative (ab[U150] on U100 -0.32 [-0.48, -0.16], ab[BM] on U100 -0.03), i.e. a non-matched variant marginally beats the U100-tuned one, which reflects that U100 tuning was uninformative.
5. Best Fit remains the only heuristic with no large regression on any of the five classes.

## Caveats
- Instances within a class share a generator, so CIs describe instance sampling, not generator misspecification. Our Weibull/OR-like generators are not guaranteed identical to the FunSearch paper generators.
- Paired comparisons are not multiplicity-corrected; all pre-listed comparisons are reported.
- No invention claim. Replicates and quantifies the Herrmann and Pallez point: simple tuned rules match evolved heuristics in-distribution, and both are distribution-fragile.
