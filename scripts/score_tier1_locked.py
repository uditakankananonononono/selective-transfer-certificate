"""Verify fixed predictions and publication receipt before opening one dataset's outcomes.

Publication receipt must come from independently verified live repository state;
this CLI cannot authenticate a receipt's author or create permission to score.
"""
import argparse,hashlib,json
from pathlib import Path
import anndata as ad
import pandas as pd
from lock_tier1_predictions import filehash,sourcehash
from selective_transfer.locking import verify_lock
from selective_transfer.tier1 import frozen_keys
from selective_transfer.scoring import score_verified_payload,assert_exact_keys


def score(dataset,data,reference,lockpath,receiptpath,output):
    root=Path(__file__).resolve().parents[1]
    # Never overwrite an observed outcome or accidentally rescore it.
    if Path(output).exists():raise ValueError('Output exists: recover original result, do not rescore')
    lock=json.load(open(lockpath));receipt=json.load(open(receiptpath))
    protocol=hashlib.sha256(''.join(filehash(root/n) for n in [
        'PREREG_2026-09-28_SELECTIVE_TRANSFER_v1.0_FROZEN.md',
        'PREREG_2026-09-28_SELECTIVE_TRANSFER_v1.1_FROZEN.md',
        'PREREG_2026-10-01_SELECTIVE_TRANSFER_v1.2_FROZEN.md']).encode()).hexdigest()
    if receipt.get('repository')!='https://github.com/uditakankananonononono/selective-transfer-certificate':
        raise ValueError('Wrong publication repository')
    if receipt.get('protocol_sha256')!=protocol or receipt.get('prediction_locks',{}).get(dataset)!=lock['sha256']:
        raise ValueError('Publication receipt does not bind protocol and prediction lock')
    if not receipt.get('live_verified_commit') or not receipt.get('verified_at'):
        raise ValueError('Missing verified publication identity/time')
    if lock['payload']['dataset']!=dataset or filehash(reference)!=lock.get('reference_sha256'):
        raise ValueError('Wrong dataset/reference')
    keys=frozen_keys(pd.read_csv(reference),dataset)
    a=ad.read_h5ad(data,backed='r')
    try:
        payload=verify_lock(lock,keys,list(map(str,a.var_names)),filehash(data),protocol,sourcehash(root))
        rows=score_verified_payload(a,payload)
        expected=keys.rename(columns={'outSample':'context','perturb':'perturbation'}).assign(dataset=dataset)
        assert_exact_keys(rows,expected)
        rows.to_csv(output,index=False)
        print(json.dumps({'dataset':dataset,'units':len(rows),'output':str(output),
                          'full_pcc_delta':float(rows.pcc_delta.mean()),'full_mse':float(rows.mse.mean())}))
    finally:a.file.close()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ['dataset','data','reference','lock','publication-receipt','output']:p.add_argument('--'+flag,required=True)
    z=p.parse_args();score(z.dataset,z.data,z.reference,z.lock,z.publication_receipt,z.output)
