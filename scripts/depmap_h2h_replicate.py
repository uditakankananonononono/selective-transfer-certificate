"""Sealed h2h replicate (Addendum 2). Run from repo root ONLY after addendum 2 is live. Usage: python scripts/depmap_h2h_replicate.py LINE"""
import sys, json, csv, os, zipfile, numpy as np, pandas as pd
sys.path.insert(0, 'src')
from selective_transfer.depmap_pilot import *
PB = '/tmp/pdl/pb'; META = '/tmp/pdl/metadata/cell_line_metadata.csv'
meta = {r['cell_line']: r for r in csv.DictReader(open(META))}; lines = sorted(meta)
def main_gset():
    D = {l: np.load(f'{PB}/{l}.npz') for l in lines}; C = {l: json.load(open(f'{PB}/{l}.json'))['counts'] for l in lines}
    common = set(D[lines[0]]['symbols'])
    for l in lines[1:]: common &= set(D[l]['symbols'])
    common = sorted(common); idx = {l: {s: i for i, s in enumerate(D[l]['symbols'])} for l in lines}
    pooled = np.mean([D[l]['__ctrl__'][[idx[l][s] for s in common]] for l in lines if C[l]['__ctrl__'] >= MIN_CTRL], axis=0)
    top = np.argsort(-pooled, kind='stable')[:2000]; return D, idx, [common[i] for i in top]
def guide_gene(c):
    return c.split('_')[1] if c.startswith('Cas9_') else c
def run(line):
    Z = '/tmp/pdl/h2h.zip'; tmp = '/tmp/pdl/x/h2h'; os.makedirs(tmp, exist_ok=True); zf = zipfile.ZipFile(Z)
    gp = f'h2h_data_formatted/{line}-Cas9_gex_matrix.csv'; cp = f'h2h_data_formatted/{line}-Cas9_crispr_matrix.csv'
    zf.extract(gp, tmp); zf.extract(cp, tmp)
    cr = pd.read_csv(f'{tmp}/{cp}', index_col=0).fillna(0); gcols = list(cr.columns)
    genes_of = np.array([guide_gene(c) for c in gcols]); valid = np.array([not (g.startswith('d') and g[1:2].isupper()) and g != 'Dup' and g.lower() not in ('aavs1',) and not g.startswith('Chr2') and 'non-targeting' not in g for g in genes_of])
    cm = cr.values.astype(float)  # all columns count toward the 80% rule; top guide must itself be a valid (target or OR) guide
    tot = cm.sum(1); top = cm.argmax(1); topv = cm[np.arange(len(cm)), top]
    ok = valid[top] & (topv >= MIN_GUIDE_UMI) & (tot > 0) & (topv >= UMI_FRAC * np.maximum(tot, 1))
    lab = pd.Series(np.where(ok, genes_of[top], ''), index=cr.index)
    D, idx, gset = main_gset(); gs = set(gset)
    hdr = pd.read_csv(f'{tmp}/{gp}', nrows=0, index_col=0).columns; hc = list(hdr)
    mtc = [i for i, s in enumerate(hc) if s.startswith('MT-')]; gix = {s: i for i, s in enumerate(hc)}
    use = [gix[s] for s in gset if s in gix]; usen = [s for s in gset if s in gix]
    allc = {}; ptot = {}; pmito = {}
    for pas in (1, 2):
        acc = {}; cnt = {}
        for ch in pd.read_csv(f'{tmp}/{gp}', index_col=0, chunksize=400, dtype=np.float32):
            v = ch.values; t = v.sum(1)
            if pas == 1:
                for b, tt, mm in zip(ch.index, t, v[:, mtc].sum(1) / np.maximum(t, 1)): ptot[b] = tt; pmito[b] = mm
            else:
                for i, b in enumerate(ch.index):
                    if b not in qcset: continue
                    g = lab.get(b, '')
                    if not g: continue
                    key = '__ctrl__' if g.startswith('OR') else g
                    x = np.log1p(v[i, use] / max(t[i], 1) * 1e4)
                    acc[key] = acc.get(key, 0) + x; cnt[key] = cnt.get(key, 0) + 1
        if pas == 1:
            tv = np.array(list(ptot.values())); lo, hi = np.quantile(tv, [.01, .99])
            qcset = {b for b in ptot if pmito[b] < MITO_MAX and lo <= ptot[b] <= hi}
    out = {'line': line, 'counts': cnt, 'genes_used': len(use)}
    np.savez(f'/tmp/pdl/h2h_{line}.npz', genes=np.array(usen), **{k: acc[k] / cnt[k] for k in acc if cnt[k] >= MIN_KO or k == '__ctrl__'})
    json.dump(out, open(f'/tmp/pdl/h2h_{line}.json', 'w')); os.remove(f'{tmp}/{gp}')
    print(line, cnt)
if __name__ == '__main__': run(sys.argv[1])
