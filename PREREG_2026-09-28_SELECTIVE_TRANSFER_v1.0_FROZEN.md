# PREREGISTRATION v1.0 - FROZEN

- Date drafted: 2026-09-28 (Asia/Calcutta). Frozen: 2026-09-28 (Asia/Calcutta).
- Status: FROZEN v1.0. Any change after freezing requires a NEW dated amendment file,
  approved by the user before any outcome affected by the change is opened.
- Track: cross-context expression-response prediction with a selective transfer certificate.
- Rule: no held-out outcome is opened, scored, or inspected before this file's SHA-256 is
  recorded and the file is pushed to the track's repository.
- Supersedes: PREREG_2026-09-28_DRAFT.md (v0.1). Changes from draft, and why:
  (1) The draft assumed the Nature Methods 2025 benchmark published per-dataset numbers for
      the seven hosted screens under the unseen-context scenario. Verification on 2026-09-28
      showed this is FALSE: the benchmark's cellular-context (unseen-context) scenario covers
      12 OTHER datasets; the seven hosted screens appear, if at all, in its perturbation-
      generalization scenario (unseen perturbations, same context), which is not this claim.
      The design is therefore split into Tier 1 (published-verbatim frozen target) and
      Tier 2 (frozen recomputed baselines, labeled as such). The claim, abstention
      definition, win-bar shape, compute plan, and honest-reporting rules are unchanged.

## 1. Invention claim (unchanged from draft)

A method that, for a perturbation whose response is predicted in an UNSEEN context,
outputs (a) the predicted gene-level response and (b) a transfer certificate: a score
estimating whether the prediction is trustworthy in that context, with abstention below a
prespecified rank cutoff. The claim is NOT a new predictor architecture; it is a
selective-prediction layer with a measured coverage-risk win over the frozen target.

## 2. Prior-art pass (closed 2026-09-28)

Checked before freezing: the Nature Methods 2025 benchmark (27 methods, 29 datasets,
6 metrics, unseen-context scenario: https://www.nature.com/articles/s41592-025-02980-0);
GEARS; CPA; scGen; scFoundation; scDisInFact; biolord; scVIDR; scGPT; PerturBench
(NeurIPS 2025, arXiv 2408.10609); Bendidi et al. 2024 (arXiv 2410.13956); Ahlmann-Eltze
et al. 2025 (Nat Methods 22:1657-1661); PertEval-scFM (wenteler25a); D2R2 (arXiv
2608.15288); the scPertEval protocol package (bioRxiv 2026.07.23.740433); and the general
selective/conformal prediction literature (SCoRE, SCRC, CAP, selective conformal FCR
control, conformal abstention) plus its applications in other domains (protein structure
confidence, TCR-pMHC, medical QA abstention).
Finding: no published method reports a calibrated abstention / coverage-risk evaluation
for expression-response prediction in unseen contexts. The selective-prediction machinery
exists in general ML but has not been applied or measured on this benchmark surface.
Novelty claim survives this pass. Risk noted honestly: the individual components are
standard; the claimed novelty is the measured selective-prediction layer on this surface.

## 3. Tier 1: published-verbatim frozen target

Source of truth: bm2-lab/scPerturBench GitHub repository, pinned at HEAD commit
698f8ff5ed19530bff171e4205be9b42a46a769d (2026-09-14); Results files last changed in
commit 7a2f3378c217a09c5eb04f7d491453c583d3bf97 (2025-05-27). Pinned artifacts, SHA-256:
- Results/Cellular_context_ood/cellular_ood_distance5000.csv
  1c2794c1dc21e496c143d8b897f310663a5f2f0ec632cbc7a867bb590a3c4117
- Results/Cellular_context_ood/cellular_ood_distance0.csv
  12efcd56ee0ec43cd2316048a1721ce501b8e6669213c7134572565b960be3e7
- Results/Cellular_context_ood/cellular_ood_performance_top100.csv
  9e612498d94e664d5c33a373f4fd110ed2052615e3bbebcbd5dd49fe37439cc9
- Results/Cellular_context_ood/cellular_ood_performance_top5000.csv
  0f823413267049336398fcbb339d9625da82d1d7bd07ddc2431400fc7123a073
- Cellular_context_generalization/o.o.d./calPerformance.py
  979efef1f120c60d653080d99b81ac7f373be26886102cb3dcc36ca3aa0f759d
- Cellular_context_generalization/myUtil.py
  3f71a7f5f34ae7a2ebc1f57d59e828fb15b25324feb82bb5a46672b975336f9f

Setting: cellular-context generalization, o.o.d. (held-out context per dataset), 12
datasets (Afriat, Haber, KaggleCrossCell, KaggleCrossPatient, McFarland, Parekh, TCDD,
crossPatient, crossSpecies, kangCrossCell, kangCrossPatient, sciplex3), data from Figshare
article 28143422 ("Cellular context generalization datasets"; total ~1.87 GB compressed).
Held-out contexts (outSample values) are taken verbatim from the pinned results files.

Metrics (their pipeline, fixed): PCC-delta (their `pearson_distance`, computed on deltas
vs control mean over the DEG-5000 gene set; HIGHER is better - verified: it tracks the
published `cor` column) and MSE (their `mse`, DEG-5000). Computed with their
calPerformance.py code path (pertpy Distance, subsample 2000 cells, seed 42).

Frozen target numbers (dataset-mean over all [outSample, perturbation] rows in the pinned
distance5000 file; declared deterministic aggregation, verbatim from the pinned artifact):

| dataset | best simple baseline, PCC-delta | best simple baseline, MSE | best published method, PCC-delta | best published method, MSE |
|---|---|---|---|---|
| Afriat | trainMean 0.6867 | baseControl 0.0145 | inVAE 0.8968 | inVAE 0.0031 |
| Haber | trainMean 0.5007 | baseControl 0.0107 | inVAE 0.7320 | inVAE 0.0056 |
| KaggleCrossCell | trainMean 0.4219 | baseControl 0.0134 | scGen 0.4564 | inVAE 0.0060 |
| KaggleCrossPatient | trainMean 0.6098 | trainMean 0.0041 | trainMean 0.6098 | trVAE 0.0037 |
| McFarland | trainMean 0.3832 | baseControl 0.0150 | scPRAM 0.4663 | bioLord 0.0103 |
| Parekh | trainMean 0.2640 | baseControl 0.0030 | trVAE 0.3054 | baseControl 0.0030 |
| TCDD | trainMean 0.2391 | baseControl 0.0060 | inVAE 0.7295 | scVIDR 0.0040 |
| crossPatient | trainMean 0.3521 | baseControl 0.0054 | trainMean 0.3521 | inVAE 0.0047 |
| crossSpecies | trainMean 0.3403 | baseControl 0.0426 | scPRAM 0.5686 | scVIDR 0.0300 |
| kangCrossCell | trainMean 0.5926 | baseControl 0.0338 | trVAE 0.9107 | inVAE 0.0062 |
| kangCrossPatient | trainMean 0.9486 | trainMean 0.0033 | trVAE 0.9750 | trVAE 0.0016 |
| sciplex3 | trainMean 0.3196 | baseControl 0.0061 | trVAE 0.3709 | scVIDR 0.0051 |

The four simple baselines are trainMean, baseReg, baseControl, baseMLP (their README:
"10 published methods and the four baseline model"). The win target on the primary metric
is the BEST SIMPLE BASELINE (trainMean on PCC-delta everywhere), deliberately NOT the
weakest published method. Note honestly: on KaggleCrossPatient and crossPatient the simple
baseline also beats every published method on PCC-delta.

Pipeline-validation gate (fixed): before any Tier-1 scoring, our re-implementation of their
metric path is run on OUR trainMean reproduction for one dataset (kangCrossCell) and must
reproduce the pinned trainMean number within abs diff 0.01 on PCC-delta. This validates the
metric pipeline against a baseline, not an outcome. If it fails, the track pauses and
reports; no outcome scoring proceeds.

## 4. Tier 2: seven hosted screens, cross-line transfer (frozen RECOMPUTED baselines)

Verified 2026-09-28: no published per-dataset cross-line-transfer numbers exist for the
seven hosted screens. Tier-2 baselines are therefore RECOMPUTED with frozen, unit-tested
implementations before outcomes are opened, and are labeled "frozen recomputed", never
"published". Literature anchor for their strength: Ahlmann-Eltze 2025 (simple linear
baselines not yet beaten), Bendidi 2024 (PCA baseline dominates), and the Tier-1 table
itself (trainMean best simple everywhere; best overall on 2 of 12 datasets).

Datasets (roles unchanged from draft; sizes verified 2026-09-28):
DEVELOPMENT: replogle22k562 (2,430,512,332 B), nadig25hepg2 (1,236,448,196 B),
wessels23 (195,514,272 B; combos only, used only for combo-additivity development).
HELD-OUT: replogle22rpe1 (1,877,364,555 B), nadig25jurkat (2,004,474,709 B),
arch1 train split (4,377,281,643 B), kaden25rpe1 (5,641,728,720 B).
Evaluation unit: pseudobulk delta per perturbation vs matched controls. Split axis: cell
line / dataset. Certificate fitting uses ONLY development datasets. Held-out files are
downloaded, hashed, and untouched until scoring. arch1's external leaderboard splits are
not used.

Tier-2 frozen baselines (fixed): (a) zero-effect (delta = 0); (b) cross-line mean delta
for the same perturbation over training lines; (c) per-gene ridge transfer (lambda = 1.0)
fit on development leave-one-line-out splits.

## 5. Method spec (fixed hyperparameters)

Base transfer predictor: equal-weight cross-context mean delta per gene per perturbation,
plus a per-gene ridge correction (lambda = 1.0, fixed) fit on development
leave-one-context-out splits only. For Tier 1, imputed cells = control cells plus the
predicted delta, matching the benchmark harness (subsample 2000, seed 42).
Certificate score c(p, c*): shrunk cross-context concordance - mean pairwise Pearson of
the perturbation's delta across training contexts, multiplied by n/(n+5), n = minimum
perturbed-cell count for that perturbation across training contexts (capped at 2000).
Abstention: rank-based; within each held-out evaluation set, abstain on the lowest 20% of
certificate scores (80% coverage by construction; no fitted threshold, no held-out fitting).
Calibration curves are reported for description only and are fit on development data only.
Seeds: 42 everywhere. Any stochastic step logs its seed.

## 6. Win bar (fixed; one primary comparison, no metric shopping)

Primary metric: PCC-delta. Secondary: MSE (reported exactly; no win condition on it).
Tier 1 win requires BOTH:
  (a) full coverage (certificate disabled): dataset-mean PCC-delta >= the frozen
      best-simple-baseline number on EACH of the 12 datasets;
  (b) at 80% coverage: macro-averaged risk (1 - PCC-delta) across the 12 datasets at least
      10% relatively lower than the macro-averaged frozen best-simple-baseline risk.
Tier 2 win requires BOTH:
  (a) full coverage: per-held-out-dataset PCC-delta not worse than the best frozen
      recomputed baseline on that dataset;
  (b) at 80% coverage: mean risk across held-out datasets at least 10% relatively lower
      than the best frozen recomputed baseline's full-coverage risk.
Anything short of both, per tier, is a loss and is reported exactly. Negatives and nulls
are reported with the same precision as wins.

## 7. Compute plan (free-first, verified 2026-09-28)

Sandbox: ~20 GB free disk, ~1.5 GB available RAM, 2 cores. Tier 1 total ~1.87 GB
compressed. Tier 2 total 17.8 GB. Sequential download-process-delete; at most two Tier-2
datasets resident; anndata backed-mode chunked streaming (~5,000-cell chunks); peak
pseudobulk ~150 MB per dataset. Public HTTPS/Figshare only; no API keys; no paid services.
If any step exceeds local capacity, the step is redesigned or the track stops; it never
moves to paid compute.

## 8. Honest reporting (unchanged)

All held-out numbers, coverage, abstention rates, failures, and deviations are reported
verbatim. Deviations after freezing require a new dated amendment approved by the user
before affected outcomes are opened.

## 9. Remaining logistics (not protocol)

Repo: new dedicated repo under uditakankananonononono via key-ops routing (requested
2026-09-28). This file is pushed there before any scoring; its SHA-256 is recorded in the
freeze report.
