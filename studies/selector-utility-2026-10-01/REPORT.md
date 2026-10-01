# Selector utility development result, October 1, 2026

Combined descriptive gate: FAIL. The selector reduces same-predictor macro risk by 4.2431203%, below the frozen 10% threshold. The matched-mask predictor comparison passes. This is known-outcome development on a finite benchmark panel, not new independent confirmation or novelty.

Random expected fixed-method macro risk: 0.4041976022. Certificate-retained method risk: 0.3870470116. Published trainMean risk on the identical masks: 0.5278263997.

The previous 28.2497974% reduction compared the retained method with the full-coverage published baseline. It does not measure isolated selector value. The new 4.2431203% contrast compares against the exact uniform-random matched-K expectation for the SAME fixed method. No Monte Carlo best draw was selected.

| dataset | units | retained | actual_coverage | selector_identifiable | selector_risk_improvement | matched_predictor_risk_improvement | full_method_mse | retained_method_mse |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Afriat | 4 | 4 | 1.00000000 | False | 0.00000000 | 0.25835000 | 0.00160000 | 0.00160000 |
| Haber | 24 | 20 | 0.83333333 | True | 0.00105667 | 0.24749000 | 0.00449167 | 0.00506500 |
| KaggleCrossCell | 24 | 20 | 0.83333333 | True | -0.04435917 | 0.18302500 | 0.00673333 | 0.00530000 |
| KaggleCrossPatient | 30 | 24 | 0.80000000 | True | 0.10583250 | -0.00260833 | 0.00313333 | 0.00325417 |
| McFarland | 42 | 34 | 0.80952381 | True | 0.04973950 | 0.26941176 | 0.00739286 | 0.00785294 |
| Parekh | 30 | 24 | 0.80000000 | True | 0.06064917 | 0.02960000 | 0.00283000 | 0.00315833 |
| TCDD | 6 | 5 | 0.83333333 | True | -0.02792333 | 0.47798000 | 0.00348333 | 0.00350000 |
| crossPatient | 10 | 8 | 0.80000000 | True | 0.01202000 | -0.12901250 | 0.00512000 | 0.00517500 |
| crossSpecies | 4 | 4 | 1.00000000 | False | 0.00000000 | 0.20677500 | 0.03497500 | 0.03497500 |
| kangCrossPatient | 8 | 7 | 0.87500000 | True | -0.00111607 | 0.02577143 | 0.00165000 | 0.00171429 |
| sciplex3 | 27 | 22 | 0.81481481 | True | 0.03275724 | -0.01820909 | 0.00554444 | 0.00620000 |

Six of nine identifiable datasets improve under selection. KaggleCrossCell, TCDD and kangCrossPatient worsen. Afriat and crossSpecies abstain zero and are selector-nonidentifiable. Matched-mask predictor losses: KaggleCrossPatient, crossPatient, sciplex3.

Retention composition is unequal across contexts. It entirely removes HepatocytesCentral in TCDD, PW029 in crossPatient and Pat1015 in kangCrossPatient. sciplex3 retains A549 6/9, K562 9/9 and MCF7 7/9. KaggleCrossPatient retains Pat0 8/10, Pat1 7/10 and Pat2 9/10. Full before/after context composition is in context_composition.csv; context names include patients, cell types, lines and species, not uniformly donors. This dataset-level selection is not evidence of within-donor selection utility.

Retained method MSE increases on eight identifiable datasets (Haber, KaggleCrossPatient, McFarland, Parekh, TCDD, crossPatient, kangCrossPatient, sciplex3), and decreases on KaggleCrossCell. These are descriptive adverse-effect checks, not retrospective success criteria.

No rows dropped, no predictor/certificate changes, no new expression outcomes opened. All 209 exact units from 11 datasets included. The baseline artifact hash was verified. Independent arithmetic/mask/composition/locked-certificate audit passed; 31 synthetic tests pass. Original v1.2 LOSS and prior-art correction are unchanged.

Sources: https://github.com/uditakankananonononono/selective-transfer-certificate ; https://github.com/bm2-lab/scPerturBench/tree/698f8ff5ed19530bff171e4205be9b42a46a769d/Results/Cellular_context_ood ; https://arxiv.org/html/2510.07964
