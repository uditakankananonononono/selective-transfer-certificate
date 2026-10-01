"""Lock all LOCO predictions without scoring or printing target outcomes."""
import argparse
import hashlib
import json
from pathlib import Path
import anndata as ad
import pandas as pd
from selective_transfer.tier1 import frozen_keys,predict
from selective_transfer.locking import extract_fold,make_lock


def filehash(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def sourcehash(root):
    names=['src/selective_transfer/core.py','src/selective_transfer/tier1.py',
           'src/selective_transfer/locking.py','scripts/lock_tier1_predictions.py']
    return hashlib.sha256(''.join(n+':'+filehash(root/n)+'\n' for n in names).encode()).hexdigest()


def run(dataset,path,reference,out):
    root=Path(__file__).resolve().parents[1]
    keys=frozen_keys(pd.read_csv(reference),dataset)
    a=ad.read_h5ad(path,backed='r')
    try:
        if a.n_vars != 5000:
            raise ValueError('DEG-5000 equality not established: input must have 5000 genes')
        predictions=[]
        for context in keys.outSample.unique():
            means,counts,genes=extract_fold(a,context)
            subset=keys[keys.outSample==context]
            predictions.extend(predict(subset,means,counts))
            del means,counts
        lock=make_lock(dataset,keys,predictions,genes,filehash(path),
                       filehash(root/'PREREG_2026-09-28_SELECTIVE_TRANSFER_v1.1_FROZEN.md'),
                       sourcehash(root))
        lock['reference_sha256']=filehash(reference)
        with open(out,'x') as f:json.dump(lock,f,sort_keys=True,allow_nan=False)
        print(json.dumps({'dataset':dataset,'units':len(predictions),'genes':len(genes),
                          'prediction_lock_sha256':lock['sha256'],
                          'outcomes_scored':0,'output':str(out)}))
    finally:a.file.close()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset',required=True);p.add_argument('--data',required=True)
    p.add_argument('--reference',required=True);p.add_argument('--output',required=True)
    z=p.parse_args();run(z.dataset,z.data,z.reference,z.output)
