# Benchmark metric provenance and validation gate (2026-09-28)

The frozen v1.0 protocol stands. Its primary numeric metric is Pearson correlation
between predicted and observed pseudobulk deltas (higher is better). The benchmark
script names its call `pearson_distance`, but the released `distance5000` numbers and
`performance_top5000` `cor` column equal correlation, and its ranking favors larger
values. Modern and older released pertpy implementations inspected separately return
`1 - correlation` for `PearsonDistance`, so the code name alone cannot reproduce the
released artifact's numeric convention. We use the artifact's published numbers and
high-is-better ranking as the frozen target, not the name of the wrapper metric.
This discrepancy is a provenance limitation, not an unreported protocol change.

The preregistered, pre-scoring validation gate uses the Figshare kangCrossCell dataset
(13,576 cells x 5,000 genes), the trainMean source baseline, and the pinned benchmark
CSV. Reproduction: for each of eight cell contexts, mean treated expression in all
other contexts predicts the held-out context's treated expression; subtract the
held-out context's control mean from both the prediction and observed treated mean;
calculate Pearson correlation over all 5,000 genes. Mean across contexts =
0.5938344698408551. Pinned trainMean mean = 0.5925875. Absolute difference =
0.0012469698408551, below the prespecified 0.01 tolerance. Largest context-level
difference = 0.0057; differences are consistent with the authors' stochastic
cell generation. The score `1 - correlation` instead averages 0.406165530159145,
and would NOT reproduce 0.5926. No new method outcomes were scored for this gate.

Scripts: `scripts/reproduce_kang_cross_cell_gate.py` (requires anndata, scipy,
numpy, pandas, and an uncompressed copy of the public dataset; local absolute paths
in this initial research script should be made CLI arguments before external use).

Frozen sources:
- https://github.com/bm2-lab/scPerturBench/tree/698f8ff5ed19530bff171e4205be9b42a46a769d/Results/Cellular_context_ood
- https://github.com/bm2-lab/scPerturBench/blob/698f8ff5ed19530bff171e4205be9b42a46a769d/Cellular_context_generalization/o.o.d./calPerformance.py
- https://ndownloader.figshare.com/files/51509726
