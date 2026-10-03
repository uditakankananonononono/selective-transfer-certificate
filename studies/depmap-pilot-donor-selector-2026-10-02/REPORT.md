# Result: DepMap Perturb-seq pilot donor selector (frozen dd0fac1 + addendum 854d823), scored once, 2026-10-03 IST

Overall: LOSS. Both clauses fail. This is an independent pre-outcome result on data no earlier study touched.

- Units: 1339 (gene x held-out line, >=4 other-batch donors); identifiable (selector changed the donor set): 823. 16 lines, 2000-gene set.
- Clause A (selector vs matched-K random, macro MSE): M 0.004440 vs Rnd 0.004175, relative reduction -6.35%, bootstrap 95% CI [-10.2%, -3.5%]. FAIL; the selector is worse than random.
- Clause B (M vs all-donor mean B): macro 0.004828 vs 0.004464 (M worse); M worse than B on 16/16 lines (2.3% on SLR23 to 13.2% on KYSE450). FAIL.
- Per-line MSE and unit rows: verdict.json, units.csv. Per-line cell/guide/QC counts: line_counts/.

## Implementation notes (mechanics, no outcome used)
1. KYSE450 and UMRC3 guide matrices carry "-1"/"-2" lane suffixes; matched on the full barcode (others match after stripping "-1"). First pass matched 0 cells on those two and was rerun with this fix before any scoring.
2. HKGZCC guide matrix exceeded memory on first pass; reader now keeps only barcodes present in the GE matrix. Same values.
3. Expression loaded in streaming chunks for memory. Same pseudobulk algebra.
4. The scoring script was lightly tidied (a convoluted delta line) after addendum publication and before scoring; semantics unchanged.
5. The authors' same-arm control restriction and arm-loss filtering were not applied (addendum limitation). Controls are 10 OR guides pooled.
6. Pearson per-unit values are in units.csv but are not a win clause.
7. h2h_data_formatted.zip and processed.zip were never opened.

## Interpretation
The cosine certificate (>0.2 vs leave-self-out donor mean) chooses donors that fit worse than the full donor mean on held-out lines.
Averaging more donors beats averaging a cosine-filtered subset here, consistent with variance reduction dominating relevance here. No invention claim.
Limitation: nested batch-lineage design, 90 genes only, essential-gene KOs with strong shared responses.

---
## Sealed h2h replicate (Addendum 2, live at 5bf8c22 before any h2h expression was read)
Scored once: 20 units (UMRC3, KMRC20 x 10 genes: MDM2, MTOR, MTPAP, MYC, PSMA1, SEC23IP, SMG6, TFRC, TXN, TYMS); PELO and VPS4A skipped (0 donors); 8 identifiable units.
- Clause A (descriptive): M 0.002230 vs matched-K random 0.002454, relative reduction +9.1% (below the 10% bar; direction opposite to the main screen, but 8 units in 2 lines, no CI).
- Clause B: M 0.008297 vs all-donor mean 0.008252, M worse (UMRC3 0.010627 vs 0.010605; KMRC20 0.005967 vs 0.005899).
- Pre-registered reading: "confirms" (both clauses fail). Small-n; the A sign flip is noted, not claimed.
Disclosures: h2h loader needed one pandas dtype fix before it ran (no values read); Dup_* guide columns excluded from controls and KOs per addendum 2; the scorer tidy before the main score is listed above.

## Closure: donor-selector direction (cosine-certificate retention)
Measured negative on two independent datasets: DepMap pilot main screen (-6.35% vs matched-K random, CI [-10.2%,-3.5%]; worse than all-donor mean on 16/16 lines) and the sealed deep rescreen (+9.1% descriptive, below 10%; M not better than B). Earlier Tier-1 selector-utility isolated gain was 4.24%, also below 10%.
Evidence commits (live chain): 966d54a pilot result, 3eaddeb code+tests, 5bf8c22 addendum 2. No invention claim for the cosine donor selector.
