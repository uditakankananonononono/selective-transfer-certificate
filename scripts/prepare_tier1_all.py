"""Sequential official download/hash/prediction-lock pipeline; never scores."""
import hashlib,json,gzip,shutil,subprocess,sys
from pathlib import Path
import urllib.request
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('/tmp/tier1-clean')
REF=Path('/tmp/deep-research/algorithm-invention/perturb-seq-track/baseline-refs/cellular_ood_distance5000.csv')
import argparse
p=argparse.ArgumentParser();p.add_argument('--datasets',nargs='+',required=True)
selected=set(p.parse_args().datasets)
files=json.load(open(BASE/'files.json'))['files']
for f in sorted(files,key=lambda x:x['size']):
    dataset=f['name'].split('.')[0]
    if dataset not in selected or dataset in ['kangCrossCell','sciplex3']:continue
    directory=BASE/dataset; directory.mkdir(exist_ok=True)
    output=directory/'prediction-lock-v1.2.json'
    if output.exists():continue
    compressed=directory/'data.h5ad.gz'; data=directory/'data.h5ad'
    print(json.dumps({'stage':'download','dataset':dataset}),flush=True)
    if not compressed.exists() or compressed.stat().st_size != f['size']:
        urllib.request.urlretrieve(f['download_url'],compressed)
    h=hashlib.md5()
    with open(compressed,'rb') as src:
        for chunk in iter(lambda:src.read(1024*1024),b''):h.update(chunk)
    if h.hexdigest()!=f['computed_md5']:raise ValueError('Official MD5 mismatch')
    with gzip.open(compressed,'rb') as src,open(data,'wb') as dest:shutil.copyfileobj(src,dest)
    subprocess.run([sys.executable,str(ROOT/'scripts/lock_tier1_predictions.py'),
                    '--dataset',dataset,'--data',str(data),'--reference',str(REF),
                    '--output',str(output)],check=True)
    print(json.dumps({'stage':'locked','dataset':dataset,'bytes':data.stat().st_size}),flush=True)
    # Keep data for scoring; delete compressed duplicate to fit the disk budget.
    compressed.unlink()
