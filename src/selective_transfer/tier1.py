"""Pre-scoring Tier-1 extraction and held-out evaluation harness.

Only run on a clean benchmark dataset after freezing this script, model code,
key manifest, and outcome-exposure ledger. No real benchmark data is loaded by
this module's synthetic unit tests.
"""
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import pearsonr
from .core import ridge_corrected_transfer


def frozen_keys(csv: pd.DataFrame, dataset: str) -> pd.DataFrame:
    z=csv[(csv.DataSet==dataset)&(csv.method=='trainMean')&
          (csv.metric=='pearson_distance')&(csv.DEG==5000)]
    if z.empty or z.duplicated(['outSample','perturb']).any():
        raise ValueError('Missing or duplicate frozen evaluation keys')
    return z[['outSample','perturb']].sort_values(['outSample','perturb']).reset_index(drop=True)


def grouped_means(adata, chunk_size: int=1000) -> tuple[dict,dict]:
    """Bounded-RAM accumulation of context/perturbation means and counts."""
    if chunk_size<1 or chunk_size>5000:
        raise ValueError('chunk_size outside frozen compute range')
    labels=np.array(list(zip(adata.obs.condition1.astype(str),
                             adata.obs.condition2.astype(str))),dtype=object)
    keys=sorted(set(map(tuple, labels)))
    index={k:i for i,k in enumerate(keys)}
    codes=np.array([index[tuple(row)] for row in labels],dtype=np.int32)
    sums=np.zeros((len(keys),adata.n_vars),dtype=np.float64)
    counts=np.bincount(codes,minlength=len(keys)).astype(np.int64)
    for start in range(0,adata.n_obs,chunk_size):
        end=min(start+chunk_size,adata.n_obs)
        x=adata.X[start:end]
        local,inv=np.unique(codes[start:end],return_inverse=True)
        selector=sparse.csr_matrix((np.ones(end-start),
                                   (inv,np.arange(end-start))),shape=(len(local),end-start))
        chunk=selector@x
        sums[local] += chunk.toarray() if sparse.issparse(chunk) else chunk
    if counts.sum()!=adata.n_obs or np.any(counts==0):
        raise AssertionError('Invalid group count')
    return {k:sums[i]/counts[i] for i,k in enumerate(keys)},dict(zip(keys,counts))


def predict(keys: pd.DataFrame, means: dict, counts: dict):
    """Emit predictions and certificates without reading any held-out treated mean.

    Caller owns the outcome-exposure boundary and must not pass held-out
    treated outcomes to this function. The means dictionary is an internal
    grouped view; we only read training treated vectors and target controls.
    """
    predictions=[]
    for context,pert in keys[['outSample','perturb']].itertuples(index=False,name=None):
        target_control=means.get((context,'control'))
        if target_control is None:
            raise ValueError(f'Missing target control: {context}')
        training=sorted(c for (c,p) in means if p==pert and c!=context
                        and (c,'control') in means)
        if not training:
            raise ValueError(f'No training context for {pert} -> {context}')
        deltas=np.stack([means[(c,pert)]-means[(c,'control')] for c in training])
        controls=np.stack([means[(c,'control')] for c in training])
        numbers=np.array([counts[(c,pert)] for c in training])
        r=ridge_corrected_transfer(deltas,controls,target_control,numbers)
        predictions.append((context,pert,r.predicted_delta,r.certificate,r.contexts_used))
    return predictions


def score_predictions(predictions, means: dict):
    """The sole method-outcome opening boundary: compare to treated target mean."""
    rows=[]
    for context,pert,pred,certificate,ntrain in predictions:
        truth=means.get((context,pert))
        if truth is None:
            raise ValueError(f'Missing held-out outcome: {context}/{pert}')
        control=means[(context,'control')]
        actual=truth-control
        if len(actual)!=len(pred):
            raise ValueError('Gene mismatch')
        corr=float(pearsonr(pred,actual).statistic)
        mse=float(np.square((control+pred)-truth).mean())
        rows.append({'context':context,'perturbation':pert,
                     'pcc_delta':corr,'mse':mse,'certificate':certificate,
                     'training_contexts':ntrain})
    return pd.DataFrame(rows)
