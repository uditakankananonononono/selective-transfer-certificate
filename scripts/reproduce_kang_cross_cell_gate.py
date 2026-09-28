"""Pre-scoring benchmark baseline validation: public kangCrossCell/trainMean ONLY."""
import argparse
import anndata as ad
import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def validate(dataset, reference):
    a = ad.read_h5ad(dataset, backed='r')
    obs = a.obs
    X = np.asarray(a.X[:], dtype=np.float32)
    context = obs.condition1.to_numpy()
    stimulated = obs.condition2.to_numpy() == 'stimulated'
    rows = []
    for c in obs.condition1.unique():
        train = X[(context != c) & stimulated].mean(axis=0, dtype=np.float64)
        observed = X[(context == c) & stimulated].mean(axis=0, dtype=np.float64)
        control = X[(context == c) & ~stimulated].mean(axis=0, dtype=np.float64)
        score = float(pearsonr(train - control, observed - control).statistic)
        rows.append((c, score))
    benchmark = pd.read_csv(reference)
    target = benchmark[(benchmark.DataSet == 'kangCrossCell') &
                       (benchmark.method == 'trainMean') &
                       (benchmark.metric == 'pearson_distance') &
                       (benchmark.DEG == 5000)].set_index('outSample').performance
    if set(target.index) != {c for c, _ in rows}:
        raise ValueError('Benchmark context set does not match dataset')
    for c, score in rows:
        print(f'{c}: reproduced={score:.6f}; published={target[c]:.6f}; diff={score-target[c]:+.6f}')
    result = float(np.mean([score for _, score in rows]))
    diff = abs(result - float(target.mean()))
    print(f'MEAN reproduced={result:.9f}; published={target.mean():.9f}; abs_diff={diff:.9f}')
    if diff >= 0.01:
        raise AssertionError('Frozen pipeline gate FAILED; stop before outcome scoring')
    print('GATE PASS')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset', required=True, help='kangCrossCell uncompressed h5ad')
    p.add_argument('--reference', required=True, help='pinned cellular_ood_distance5000.csv')
    args = p.parse_args()
    validate(args.dataset, args.reference)
