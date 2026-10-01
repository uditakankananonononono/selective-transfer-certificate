# Training-only robust blend diagnostic - October 1, 2026

Overall diagnostic: FAIL. Training-only robust selection rescues crossPatient PCC, but does not clear all datasets and introduces PCC harms elsewhere. This is known-outcome development, not independent validation or invention.

Full baseline clauses: 9/11. Macro risk reduction: 26.88005764%. CrossPatient rescue: True. All-dataset no-harm vs ridge: False. Nonadaptive fallback: 126/209 units.

crossPatient improves from ridge PCC 0.262630 to blend 0.358510, exceeding published target 0.352110. Its MSE worsens from 0.005120 to 0.006230. This is a specific development rescue, not consistent dominance.

KaggleCrossPatient and sciplex3 still fail baseline targets. They have insufficient training contexts for the prespecified adaptive gate and retain exact original ridge predictions. Haber and kangCrossPatient suffer PCC harm vs ridge; all harms are in summary.csv.

The 15 quarter-step blends, worst-context then mean-PCC then lexicographic tie-breaking, and <3-context fallback were fixed before new scores. No target-treated outcome enters weight choice. All inner ridge residuals and component fits use outer-reduced training pools. Selection details for every unit and full 15-grid diagnostics are included. No grid/tie/eligibility change after outcomes.

All 209 keys included; fallback scores match original ridge exactly. Selected weights audited independently against recorded grid rankings. Full MSE, fixed-predictor contrasts, fallback distributions and prediction file hashes retained. 37 synthetic tests pass. A timed-out Afriat/crossSpecies call had completed both CSVs/locks before termination; outputs were verified and not rerun.

Interpretation: training-only robust selection is not universally falsified because it rescues the hard patient dataset, but it fails the cross-dataset consistency/no-harm claim. Few-context eligibility is a real boundary, not permission to tune those datasets. A new direction must preserve the rescue while handling low-context uncertainty without per-dataset knobs. Generic ensemble/model selection is prior art, not a novel method claim.

Source watching brief: https://arxiv.org/abs/2506.22641 was fetched in full and argues control-reference shifts can inflate delta correlations, offering WMSE/weighted delta R2. That is prior art for the critique and metric remedy; it does not establish that these benchmark gains are artifacts. No frozen metric changed. scPILOT/State context-transfer are relevant prior-art leads, not verified novelty gaps.

Original v1.2 LOSS, selector-utility FAIL, and predictor-ablation FAIL remain unchanged. Sources: https://github.com/uditakankananonononono/selective-transfer-certificate ; https://api.figshare.com/v2/articles/28143422 ; https://github.com/bm2-lab/scPerturBench/tree/698f8ff5ed19530bff171e4205be9b42a46a769d/Results/Cellular_context_ood
