import argparse,gzip,json,shutil,urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import anndata as ad
from scripts.predictor_ablation import hashfile,BASE,REF,ROOT
from selective_transfer.tier1 import grouped_means,frozen_keys
from selective_transfer.robust_blend import select_blend
from selective_transfer.scoring import score_verified_payload,assert_exact_keys
OUT=ROOT/'studies/robust-blend-2026-10-01'

def run(ds):
    output=OUT/(ds+'.csv')
    if output.exists():print('PRESERVED',ds,flush=True);return
    d=BASE/ds;data=d/'data.h5ad';compressed=d/'data.h5ad.gz'
    f=next(x for x in json.load(open(BASE/'files.json'))['files'] if x['name']==ds+'.h5ad.gz')
    print('PREPARE',ds,flush=True)
    if not data.exists():
        if not compressed.exists() or compressed.stat().st_size!=f['size']:urllib.request.urlretrieve(f['download_url'],compressed)
        if hashfile(compressed,'md5')!=f['computed_md5']:raise ValueError('MD5 mismatch')
        with gzip.open(compressed,'rb') as src,open(data,'wb') as dest:shutil.copyfileobj(src,dest)
    lock=json.load(open(d/'prediction-lock-v1.2.json'))
    if hashfile(data)!=lock['payload']['dataset_sha256']:raise ValueError('Original SHA mismatch')
    a=ad.read_h5ad(data,backed='r')
    try:
        means,counts=grouped_means(a);genes=list(map(str,a.var_names));keys=frozen_keys(pd.read_csv(REF),ds)
        rows=[];diagnostics=[]
        for context,pert in keys.itertuples(index=False,name=None):
            train=sorted(c for c,p in means if p==pert and c!=context and (c,'control') in means)
            delta=np.stack([means[(c,pert)]-means[(c,'control')] for c in train])
            control=np.stack([means[(c,'control')] for c in train]);n=np.array([counts[(c,pert)] for c in train])
            pred,diag=select_blend(delta,control,n,means[(context,'control')])
            rows.append(dict(context=context,perturbation=pert,delta=pred.tolist(),certificate=0.,training_contexts=len(train)))
            diagnostics.append(dict(context=context,perturbation=pert,training_context_ids=train,**diag))
        predfile=OUT/(ds+'-predictions.json')
        with open(predfile,'x') as f:json.dump(dict(dataset=ds,genes=genes,rows=rows,diagnostics=diagnostics),f,allow_nan=False)
        result=score_verified_payload(a,dict(dataset=ds,genes=genes,rows=rows))
        assert_exact_keys(result,keys.rename(columns={'outSample':'context','perturb':'perturbation'}).assign(dataset=ds))
        result.to_csv(output,index=False)
        (OUT/(ds+'-selection.json')).write_text(json.dumps(diagnostics,indent=2)+'\n')
        print(json.dumps(dict(dataset=ds,units=len(rows),full_pcc=float(result.pcc_delta.mean()),mse=float(result.mse.mean()),fallbacks=sum(x['fallback'] for x in diagnostics))),flush=True)
    finally:a.file.close()
    data.unlink()
    if compressed.exists():compressed.unlink()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--datasets',nargs='+',required=True)
    for ds in p.parse_args().datasets:run(ds)
