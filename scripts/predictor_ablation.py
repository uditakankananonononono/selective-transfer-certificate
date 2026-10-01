"""Frozen known-outcome development predictor ablation. Sequential, bounded RAM."""
import argparse,gzip,hashlib,json,shutil,urllib.request
from pathlib import Path
import anndata as ad
import numpy as np
import pandas as pd
from selective_transfer.tier1 import frozen_keys
from selective_transfer.locking import extract_fold
from selective_transfer.scoring import score_verified_payload,assert_exact_keys
BASE=Path('/tmp/tier1-clean')
ROOT=Path(__file__).resolve().parents[1]
REF=Path('/tmp/deep-research/algorithm-invention/perturb-seq-track/baseline-refs/cellular_ood_distance5000.csv')
OUT=ROOT/'studies/predictor-ablation-2026-10-01'


def hashfile(path,kind='sha256'):
    h=hashlib.new(kind)
    with open(path,'rb') as f:
        for x in iter(lambda:f.read(1024*1024),b''):h.update(x)
    return h.hexdigest()


def new_predictors(keys,means,counts,genes):
    rows={'analytic_trainMean':[],'meanDelta':[]}
    for context,pert in keys.itertuples(index=False,name=None):
        train=sorted(c for c,p in means if p==pert and c!=context)
        if not train or any((c,'control') not in means for c in train):
            raise ValueError('Training-pool baseline equivalence gap')
        n=np.array([counts[(c,pert)] for c in train],dtype=float)
        absolute=np.stack([means[(c,pert)] for c in train])
        ctrl=np.stack([means[(c,'control')] for c in train])
        delta=absolute-ctrl
        predictions={'analytic_trainMean':np.average(absolute,axis=0,weights=n)-means[(context,'control')],
                     'meanDelta':delta.mean(axis=0)}
        for name,pred in predictions.items():
            rows[name].append(dict(context=context,perturbation=pert,delta=pred.tolist(),certificate=0.,training_contexts=len(train)))
    return rows


def run(ds):
    output=OUT/(ds+'.csv')
    if output.exists():print('PRESERVED',ds,flush=True);return
    f=next(x for x in json.load(open(BASE/'files.json'))['files'] if x['name']==ds+'.h5ad.gz')
    d=BASE/ds;compressed=d/'data.h5ad.gz';data=d/'data.h5ad'
    print('PREPARE',ds,flush=True)
    if not data.exists():
        if not compressed.exists() or compressed.stat().st_size!=f['size']:
            urllib.request.urlretrieve(f['download_url'],compressed)
        if hashfile(compressed,'md5')!=f['computed_md5']:raise ValueError('Official MD5 mismatch')
        with gzip.open(compressed,'rb') as src,open(data,'wb') as dest:shutil.copyfileobj(src,dest)
    lock=json.load(open(d/'prediction-lock-v1.2.json'))
    if hashfile(data)!=lock['payload']['dataset_sha256']:raise ValueError('Original dataset SHA differs')
    keys=frozen_keys(pd.read_csv(REF),ds)
    a=ad.read_h5ad(data,backed='r')
    try:
        allpred={'analytic_trainMean':[],'meanDelta':[]}
        for context in keys.outSample.unique():
            means,counts,genes=extract_fold(a,context)
            z=new_predictors(keys[keys.outSample==context],means,counts,genes)
            for name in allpred:allpred[name].extend(z[name])
        # Fixed full-dataset predictions before any new ablation score comparison.
        predfile=OUT/(ds+'-predictions.json')
        if predfile.exists():raise ValueError('Recover existing prediction file, do not overwrite')
        predfile.write_text(json.dumps({'dataset':ds,'genes':genes,'predictors':allpred},allow_nan=False))
        scored=[]
        for name,rows in allpred.items():
            payload=dict(dataset=ds,genes=genes,rows=rows)
            s=score_verified_payload(a,payload).assign(predictor=name)
            assert_exact_keys(s,keys.rename(columns={'outSample':'context','perturb':'perturbation'}).assign(dataset=ds))
            scored.append(s)
        original=pd.read_csv(ROOT/'results/tier1-v1.2'/f'{ds}.csv').assign(predictor='frozen_ridge')
        scored.append(original)
        result=pd.concat(scored,ignore_index=True);result.to_csv(output,index=False)
        print(result.groupby('predictor')[['pcc_delta','mse']].mean().to_json(),flush=True)
    finally:a.file.close()
    data.unlink()
    if compressed.exists():compressed.unlink()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--datasets',nargs='+',required=True)
    for ds in p.parse_args().datasets:run(ds)
