"""Full-cell, four-decimal PCC/MSE evaluation AFTER prediction-lock verification."""
import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def selected_mean(adata, indices, chunk_size=1000):
    if not len(indices):raise ValueError('Empty outcome/control group')
    total=np.zeros(adata.n_vars,dtype=np.float64)
    for start in range(0,len(indices),chunk_size):
        x=adata.X[indices[start:start+chunk_size],:]
        total+=np.asarray(x.sum(axis=0)).reshape(-1)
    return total/len(indices)


def score_verified_payload(adata, payload):
    """Caller must verify payload provenance and publication before calling."""
    if list(map(str,adata.var_names)) != payload['genes'] or adata.n_vars != 5000:
        raise ValueError('DEG-5000 gene equivalence not established')
    c=adata.obs.condition1.astype(str).to_numpy()
    p=adata.obs.condition2.astype(str).to_numpy()
    controls={}
    rows=[]
    for r in payload['rows']:
        context=r['context'];pert=r['perturbation']
        if context not in controls:
            controls[context]=selected_mean(adata,np.flatnonzero((c==context)&(p=='control')))
        truth=selected_mean(adata,np.flatnonzero((c==context)&(p==pert)))
        actual=truth-controls[context]
        pred=np.asarray(r['delta'],dtype=np.float64)
        correlation=float(pearsonr(pred,actual).statistic)
        mse=float(np.square(pred-actual).mean())
        if not np.isfinite(correlation) or not np.isfinite(mse):
            raise ValueError('Undefined metric: do not silently drop evaluation unit')
        rows.append(dict(dataset=payload['dataset'],context=context,perturbation=pert,
                         pcc_delta=round(correlation,4),mse=round(mse,4),
                         certificate=r['certificate'],training_contexts=r['training_contexts']))
    return pd.DataFrame(rows)


def assert_exact_keys(scored, reference):
    expected={(str(ds),str(c),str(p)) for ds,c,p in
              reference[['dataset','context','perturbation']].itertuples(index=False,name=None)}
    actual=list(scored[['dataset','context','perturbation']].itertuples(index=False,name=None))
    if len(actual)!=len(set(actual)) or set(actual)!=expected:
        raise ValueError('Scored evaluation population differs from frozen reference keys')
