# Tier-2 development metadata and limitation - 2026-09-28

The two preregistered single-gene development lines were extracted with
`build_dev_pseudobulk.py`; their source raw files have been deleted after
SHA-256 checks. The private scratch summaries contain only grouped means,
counts and gene labels. No Tier-2 held-out files were touched.

| Dataset | cells | labels incl control | genes | source file SHA-256 |
|---|---:|---:|---:|---|
| nadig25hepg2 | 133,757 | 1,819 | 9,623 | `b25cd23e74b94c0fec44a00b8bdfd21673ad391068df56da9cf81f38bc692221` |
| replogle22k562 | 308,646 | 1,972 | 8,563 | `f381278e4deda43a757adcc26e89ca4bb8c2006401938dc82a79e9d222473c14` |

There are 7,595 shared gene labels and 1,511 shared single-gene perturbations.
The third development set, wessels23, contains two-gene combinations only,
so it does not add another cell-line measurement of any shared single gene
perturbation. That means development leave-one-line-out on the two single-
gene lines has only ONE training line: pairwise-concordance certificate is
undefined and cross-line ridge fitting has no meaningful calibration sample.
The frozen protocol's two-part win bar cannot be asserted on Tier-2 from this
metadata; no held-out line may be quietly converted to a dev line. This is an
unresolved design issue, not a negative measured benchmark result.

Sources:
- https://github.com/Virtual-Cell-Research-Community/scPertEval/blob/main/docs/user-guide/datasets.md
- https://storage.googleapis.com/scperteval/processed/nadig25hepg2_processed_complete.h5ad
- https://storage.googleapis.com/scperteval/processed/replogle22k562_processed_complete.h5ad
