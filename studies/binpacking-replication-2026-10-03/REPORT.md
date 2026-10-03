# Bin-packing replication/extension: results

Frozen design: FROZEN_DESIGN.md (live main b8cffb7). Replication/extension, NOT an invention claim, no win clause. Excess over L1 bound, %, mean [95% bootstrap CI over instances, 10000 samples, seed 20261003]. OR1-OR4 = 20 OR-Library instances each; others 5 test instances each.

## Tuned ab variants (training instances only)

- U150: FF(a=5, b=25), train excess 3.19%
- W5k: WF(a=1, b=21), train excess 0.71%
- U100: FF(a=3, b=33), train excess 6.50%
- LN: WF(a=0, b=10), train excess 0.29%
- BM: FF(a=5, b=6), train excess 5.04%

## Full matrix (every cell)

| heuristic | OR1 | OR2 | OR3 | OR4 | W5k | U100 | LN | BM |
|---|---|---|---|---|---|---|---|---|
| BestFit | 5.80 [5.13, 6.52] | 6.06 [5.71, 6.43] | 5.37 [5.14, 5.60] | 4.94 [4.80, 5.08] | 4.08 [4.00, 4.16] | 7.33 [6.83, 7.74] | 1.76 [1.72, 1.80] | 5.02 [4.73, 5.37] |
| FirstFit | 6.41 [5.67, 7.16] | 6.44 [6.04, 6.86] | 5.74 [5.45, 6.03] | 5.23 [5.10, 5.36] | 4.40 [4.27, 4.56] | 8.35 [7.82, 8.88] | 1.87 [1.80, 1.93] | 5.35 [5.08, 5.61] |
| FunSearch-OR | 5.30 [4.58, 5.98] | 4.17 [3.58, 4.79] | 3.10 [2.81, 3.40] | 2.47 [2.33, 2.61] | 3.07 [2.99, 3.15] | 7.33 [6.89, 7.79] | 2.95 [2.89, 3.00] | 7.02 [6.77, 7.25] |
| FunSearch-Weibull | 29.25 [27.19, 31.38] | 19.85 [18.66, 21.05] | 12.77 [11.96, 13.57] | 8.13 [7.59, 8.65] | 0.63 [0.52, 0.74] | 10.45 [9.81, 11.21] | 0.60 [0.48, 0.79] | 15.18 [14.56, 15.71] |
| ab[BM]=FF(5,6) | 6.01 [5.36, 6.67] | 6.00 [5.56, 6.47] | 5.04 [4.81, 5.29] | 4.59 [4.47, 4.72] | 3.93 [3.86, 4.00] | 7.43 [7.00, 7.81] | 1.74 [1.64, 1.84] | 4.99 [4.72, 5.30] |
| ab[LN]=WF(0,10) | 17.10 [15.39, 18.80] | 13.77 [12.77, 14.78] | 10.63 [9.94, 11.31] | 8.14 [7.78, 8.52] | 3.08 [2.88, 3.33] | 10.79 [10.28, 11.30] | 0.34 [0.30, 0.38] | 7.60 [7.20, 7.96] |
| ab[U100]=FF(3,33) | 10.42 [9.40, 11.53] | 6.93 [6.17, 7.75] | 4.34 [3.90, 4.77] | 2.53 [2.27, 2.82] | 1.38 [1.33, 1.43] | 7.20 [6.74, 7.75] | 7.32 [6.89, 7.63] | 15.42 [14.70, 16.06] |
| ab[U150]=FF(5,25) | 6.41 [5.26, 7.53] | 4.47 [3.89, 5.07] | 2.95 [2.65, 3.25] | 2.10 [1.97, 2.22] | 2.15 [2.05, 2.22] | 7.20 [6.76, 7.77] | 2.18 [2.13, 2.24] | 9.39 [9.02, 9.67] |
| ab[W5k]=WF(1,21) | 15.58 [13.97, 17.16] | 11.66 [10.50, 12.88] | 8.52 [7.62, 9.39] | 6.40 [5.94, 6.86] | 0.71 [0.61, 0.81] | 8.68 [8.07, 9.42] | 0.73 [0.61, 0.84] | 11.81 [11.27, 12.18] |

## Validity check
168 fast-vs-notebook packer comparisons (BestFit, FirstFit, 5 ab variants, 3 instances per class): 0 mismatches (equivalence.json).

## Findings (descriptive)

1. Replication of published FunSearch numbers: FunSearch-OR on OR1-OR4 gives 5.30/4.17/3.10/2.47 vs Table 1 5.30/4.19/3.11/2.47; Best Fit 5.80/6.06/5.37/4.94 vs 5.81/6.06/5.37/4.94. FunSearch-Weibull on our W5k generator 0.63 vs 0.68 in Table 1 (generator not identical, so not claimed equal).
2. Pre-registered (1) FunSearch-Weibull vs BestFit off its training class: far worse on OR (29.25/19.85/12.77/8.13 vs 5.80/6.06/5.37/4.94), U100 (10.45 vs 7.33), BM (15.18 vs 5.02). On LN, which is similar in shape, it is better (0.60 vs 1.76).
   FunSearch-OR vs BestFit off its class: worse on LN (2.95 vs 1.76) and BM (7.02 vs 5.02); better on W5k (3.07 vs 4.08); equal on U100 (7.33).
3. Pre-registered (2) matched-distribution ab vs FunSearch: ab[U150]=FF(5,25) on OR1-OR4 gives 6.41/4.47/2.95/2.10 vs FunSearch-OR 5.30/4.17/3.10/2.47. Worse on OR1 and OR2 (point estimates, CIs overlap), CIs overlap on OR3, better on OR4 (non-overlapping CIs, 2.10 [1.97,2.22] vs 2.47 [2.33,2.61]). ab[W5k]=WF(1,21) 0.71 [0.61,0.81] vs FunSearch-Weibull 0.63 [0.52,0.74], overlapping. So a grid-tuned simple rule is competitive with the evolved heuristics in-distribution and better only on the largest OR set; a mixed, not decisive, replication of Herrmann & Pallez.
4. Pre-registered (3) transfer gap: every tuned ab variant degrades sharply off-distribution, e.g. ab[U100] on BM 15.42 vs matched ab[BM] 4.99; ab[LN] on OR1 17.10 vs ab[U150] 6.41. Tuned ab heuristics are about as distribution-fragile as FunSearch heuristics. ab[BM]=FF(5,6) is the one near-Best-Fit variant and transfers well.
5. No heuristic dominates: Best Fit is the safest across all eight classes; tuned or evolved heuristics win only in-distribution.

## Caveats
- Only 5 test instances per generated class; OR sets have 20. Item-level correlation within an instance is not modelled; CIs are over instances.
- U100 is a harder class for all heuristics (small n=1000, many large items).
- No post-freeze rule changes. Harness committed after freeze, before any test scoring; eval stage added and committed before scoring.
