# Frozen design: donor-selector value on the DepMap Perturb-seq pilot (16 lines x 100 genes)

Frozen 2026-10-02 (IST) BEFORE downloading single_cell_data.zip, processed.zip or h2h_data_formatted.zip.
Pre-freeze contact: only metadata.zip (md5 11ad26cc9c5ab272b80b20e0b97f86e0), data.zip (6bbe267ba864ef7ede1e15847bb6af90),
perturb-seq-depmap.zip (8cda38df1924aa8c5ed483b49d2fad06). No expression matrix opened.
Status: independent pre-outcome study on fresh data (not seen by any earlier study). Not a novelty claim; confidence filtering is
prior art (PRESCRIBE, GPerturb, see docs/PRIOR_ART_CORRECTION_2026-10-01.md).

Sources: bioRxiv 10.64898/2026.08.24.746802v1; figshare 10.6084/m9.figshare.33273600.v1 (data), 33282171.v1 (code).
Cell lines/batches: metadata/cell_line_metadata.csv (16 lines, batches apollo31-38).

## Data handling
1. Per line, raw counts. Controls = non-targeting guide cells as labeled in the line's manifest. Cell filtering = the authors' released
   filtering only; no extra filters.
2. Pseudobulk = mean of per-cell log1p(counts/total*1e4) over cells. Control reference is PER LINE (that line's own non-targeting cells).
3. Gene set = genes present in all 16 lines, then the 2000 with highest variance of line-level control pseudobulk across lines is NOT used
   (outcome-adjacent); instead the 2000 genes with highest mean control expression pooled over lines. Targeted genes are kept.
4. Delta(g, L) = pseudobulk(KO g in L) - control pseudobulk(L), over the 2000 genes.

## Units and donors
- Unit = (KO gene g, held-out line L). Eligible if >=20 KO cells for g in L, >=100 control cells in L.
- Donors for unit = lines in a DIFFERENT batch from L with >=20 KO cells for g and >=100 controls. Leave-batch-out is mandatory.
- Unit requires >=4 eligible donors, else excluded and listed. All exclusions and per-line coverage reported.
- The target KO gene's own expression is masked out of all scores (gene g removed from the 2000 for that unit).

## Predictors (no tuning, no fitting)
- M (method): L's control pseudobulk + mean of retained-donor deltas.
- B (baseline): L's control pseudobulk + mean of ALL eligible-donor deltas (equal weight).
- Rnd: matched-K random: same predictor, K = number retained, subsets drawn uniformly from eligible donors, 2000 draws, seed 20261002.

## Certificate (donor retention)
Donor d retained if cosine(delta_d, mean of other eligible donors' deltas) > 0.2 (fixed, not tuned). If fewer than 3 donors pass,
the unit uses the full eligible set (identity; excluded from selector-identifiable units but kept in B comparison).
Computed from donor data only, never from L's KO cells.

## Scores
Per unit: MSE of predicted vs true delta over the masked 2000 genes, and Pearson r of predicted vs true delta. Macro over units within
line, then over lines (lines equal weight). Also report per-line, per-batch, per-lineage.

## Win clauses (reported separately; both required for a win)
- A (selector value): macro MSE of M vs Rnd expectation on identifiable units: relative reduction >= 10% AND paired
  bootstrap over genes (10000, seed 20261002) 95% CI lower bound > 0.
- B (no harm vs baseline): M macro MSE <= B macro MSE, and M worse than B on no more than 4 of 16 lines.
Failure of either = overall LOSS. Every per-line negative is reported.

## Sealed
- h2h_data_formatted.zip (UMRC3/KMRC20 deep rescreen) is not opened until the main score is committed. Afterward it is a
  separate replicate check of the same frozen M, B, Rnd.
- No parameter, threshold, gene set or exclusion may change after single_cell_data.zip is opened. Deviations only as dated
  addenda, with the original result retained.
- Known confound: batch is nested with lineage; leave-batch-out removes same-batch donors but lineage confounding remains and is reported.
