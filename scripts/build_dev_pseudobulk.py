"""Stream a DEVELOPMENT-only scPertEval H5AD to grouped expression means.

Never use this command on an evaluation or held-out dataset before the frozen
protocol permits it. This executable does not score any outcomes; it computes
sufficient statistics for the explicitly named development datasets only.
"""
import argparse
from pathlib import Path
import anndata as ad
import numpy as np
from scipy import sparse

DEV_NAMES = {'nadig25hepg2', 'replogle22k562', 'wessels23'}


def build(path: Path, output: Path, block_size: int = 1000):
    dataset = path.name.removesuffix('_processed_complete.h5ad')
    if dataset not in DEV_NAMES:
        raise ValueError(f'Not in frozen DEVELOPMENT list: {dataset}')
    if block_size <= 0 or block_size > 5000:
        raise ValueError('Block size must be in [1,5000]')
    a = ad.read_h5ad(path, backed='r')
    labels, codes = np.unique(a.obs['perturbation'].astype(str).to_numpy(), return_inverse=True)
    genes = a.var_names.astype(str).to_numpy()
    counts = np.bincount(codes, minlength=len(labels)).astype(np.int64)
    sums = np.zeros((len(labels), a.n_vars), dtype=np.float64)
    for start in range(0, a.n_obs, block_size):
        end = min(start + block_size, a.n_obs)
        block = a.X[start:end]
        local_labels, local_codes = np.unique(codes[start:end], return_inverse=True)
        indicator = sparse.csr_matrix((np.ones(end-start, dtype=np.float64),
                                       (local_codes, np.arange(end-start))),
                                      shape=(len(local_labels), end-start))
        partial = indicator @ block
        sums[local_labels] += partial.toarray() if sparse.issparse(partial) else partial
        if (start // block_size) % 30 == 0:
            print(f'{dataset}: {end}/{a.n_obs} cells', flush=True)
    if counts.sum() != a.n_obs or len(labels) != len(counts):
        raise AssertionError('Aggregation count mismatch')
    means = (sums / counts[:,None]).astype(np.float32)
    if not np.isfinite(means).all():
        raise AssertionError('Nonfinite pseudobulk mean')
    np.savez_compressed(output, dataset=dataset, labels=labels.astype(str), genes=genes.astype(str),
                        cell_counts=counts, mean_expression=means)
    print(f'{output} ({a.n_obs} cells, {len(labels)} labels, {len(genes)} genes)',flush=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--block-size',type=int,default=1000)
    args=p.parse_args()
    build(args.input,args.output,args.block_size)
