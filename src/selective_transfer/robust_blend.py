"""Fixed-grid training-only LOCO robust blend. Known-outcome diagnostic."""
import numpy as np
from .core import ridge_corrected_transfer
WEIGHTS=tuple((i/4,j/4,(4-i-j)/4) for i in range(5) for j in range(5-i))


def components(d,c,counts,target):
    absolute=np.average(d+c,axis=0,weights=counts)-target
    mean=d.mean(axis=0)
    ridge=ridge_corrected_transfer(d,c,target,counts).predicted_delta
    return np.stack([absolute,mean,ridge])


def correlations(pred,truth):
    x=pred-pred.mean(axis=1,keepdims=True);y=truth-truth.mean()
    denom=np.linalg.norm(x,axis=1)*np.linalg.norm(y)
    return np.divide(x@y,denom,out=np.full(len(x),-1.),where=denom>0)


def select_blend(d,c,counts,target):
    d=np.asarray(d,dtype=float);c=np.asarray(c,dtype=float);counts=np.asarray(counts)
    if len(d)<3:
        r=ridge_corrected_transfer(d,c,target,counts)
        return r.predicted_delta,dict(weights=[0.,0.,1.],fallback=True,training_contexts=len(d),
                                      worst_training_pcc=None,mean_training_pcc=None)
    scores=[]
    for j in range(len(d)):
        allowed=np.arange(len(d))!=j
        cp=components(d[allowed],c[allowed],counts[allowed],c[j])
        scores.append(correlations(np.asarray(WEIGHTS)@cp,d[j]))
    scores=np.stack(scores,axis=1)
    worst=scores.min(axis=1);mean=scores.mean(axis=1)
    ix=min(range(len(WEIGHTS)),key=lambda k:(-worst[k],-mean[k],WEIGHTS[k]))
    full=components(d,c,counts,target)
    return np.asarray(WEIGHTS[ix])@full,dict(weights=list(WEIGHTS[ix]),fallback=False,
        training_contexts=len(d),worst_training_pcc=float(worst[ix]),mean_training_pcc=float(mean[ix]),
        grid_scores=[dict(weights=list(w),worst=float(worst[i]),mean=float(mean[i])) for i,w in enumerate(WEIGHTS)])
