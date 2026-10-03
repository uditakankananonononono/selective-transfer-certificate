# Frozen design: bin-packing heuristic replication and distribution-shift study (NOT an invention claim)

Frozen 2026-10-03 IST BEFORE any instance was generated or scored by this study and before any OR1/OR2/OR4 file was read.
Prior contact (disclosed): reproduced FunSearch notebook numbers on OR3 and Weibull-5k (Best Fit 5.37/3.98, First Fit 5.74/4.23, FunSearch-OR 3.11 on OR3,
FunSearch-Weibull 0.68 on Weibull-5k, FunSearch-Weibull on OR3 12.77, FunSearch-OR on Weibull-5k 3.03). Those are the notebook's own datasets and are not reused as test data here except as a reproduction check.
Purpose: measured replication/extension of FunSearch (Nature 2023) and Herrmann & Pallez (arXiv 2510.27353). Expected outcome "ab-family beats FunSearch" would replicate their paper.

## Heuristics (all online, priority-based, argmax over feasible bins, first index wins ties)
- FirstFit, BestFit(=-(bin-item)), WorstFit; FunSearch-OR and FunSearch-Weibull exactly as in google-deepmind/funsearch bin_packing.ipynb, run through the notebook's online_binpack with all num_items bins.
- ab-FirstFit, ab-BestFit, ab-WorstFit exactly per Herrmann-Pallez Algorithms 4-6 (thresholds a, b; capacity = bin size).
- ab grid: a in {0,1,2,3,5,8}, b in {a+1, a+3, a+6, a+10, a+15, a+20, a+30} (a<b). Variant+a+b chosen by lowest mean excess on that distribution's TRAINING instances only; ties by smaller a, then b, then variant order FF,BF,WF.

## Instance sets (item sizes ints in [1,capacity]; numpy default_rng(seed))
Test seeds and sizes (each distribution: 5 test instances; training: 5 separate instances at seeds shown):
- U150: Uniform integers [20,100], capacity 150, n=500. train seeds 1000-1004.  Test: the 80 OR-Library instances OR1-OR4 (people.brunel.ac.uk/~mastjjb/jeb/orlib/files/binpack1..4.txt), scored as given.
- W5k: round(45*Weibull(3)), clipped [1,100], capacity 100, n=5000. train 2000-2004, test 2100-2104. (Our generator; FunSearch Appendix E.4 was not consulted, so absolute numbers are not claimed equal to Table 1.)
- U100: Uniform integers [20,100], capacity 100, n=1000. train 3000-3004, test 3100-3104.
- LN: round(exp(Normal(3.2,0.6))), clipped [1,100], capacity 100, n=5000. train 4000-4004, test 4100-4104.
- BM: half Normal(25,5), half Normal(70,8) (per-item fair coin), rounded, clipped [1,100], capacity 100, n=5000. train 5000-5004, test 5100-5104.
Heuristic transfer matrix: each ab-variant tuned on a training distribution is evaluated on every test set.

## Metric and reporting
- Excess = (bins used - L1 bound)/L1 bound, L1 = ceil(sum(items)/capacity). Mean per test class with 10000-sample bootstrap 95% CI over instances (seed 20261003).
- Report every (heuristic x test class) cell, including OR1-OR4 separately and per-instance FunSearch-vs-BestFit-vs-ab pairs. No cell omitted.
- Pre-registered descriptive comparisons: (1) FunSearch-Weibull vs BestFit on non-Weibull classes; (2) best ab (tuned on matching distribution) vs FunSearch-OR/Weibull on matching class; (3) ab transfer gap: ab tuned on class X vs ab tuned on test class.
- No win clause: this is a replication/extension. Any claim limited to "replicates/does not replicate" and measured cross-distribution deltas.
- Validity check: fast packer must equal the notebook packer on 3 sampled instances per class for Best Fit and ab-variants (identical bin counts), otherwise fix before reporting.
