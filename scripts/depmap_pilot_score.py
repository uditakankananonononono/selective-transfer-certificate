"""Stage 2: frozen scoring. Run once after all 16 lines are built."""
import sys, json, csv, itertools, numpy as np
sys.path.insert(0, 'src')
from selective_transfer.depmap_pilot import *
PB = '/tmp/pdl/pb'; META = '/tmp/pdl/metadata/cell_line_metadata.csv'
meta = {r['cell_line']: r for r in csv.DictReader(open(META))}; lines = sorted(meta)
D = {l: np.load(f'{PB}/{l}.npz') for l in lines}; C = {l: json.load(open(f'{PB}/{l}.json'))['counts'] for l in lines}
common = set(D[lines[0]]['symbols'])
for l in lines[1:]: common &= set(D[l]['symbols'])
common = sorted(common); idx = {l: {s: i for i, s in enumerate(D[l]['symbols'])} for l in lines}
ctrl = {l: D[l]['__ctrl__'][[idx[l][s] for s in common]] for l in lines}
pooled = np.mean([ctrl[l] for l in lines if C[l]['__ctrl__'] >= MIN_CTRL], axis=0)
top = np.argsort(-pooled, kind='stable')[:2000]; gset = [common[i] for i in top]
delta = {}
for l in lines:
    if C[l]['__ctrl__'] < MIN_CTRL: continue
    for g in D[l].files:
        if g in ('symbols', '__ctrl__') or g.startswith('OR'): continue
        ix = [idx[l][common[i]] for i in top]
        delta[(l, g)] = D[l][g][ix] - D[l]['__ctrl__'][ix]
genes = sorted(set(g for _, g in delta)); rng = np.random.default_rng(20261002); rows = []
for (l, g), tru in sorted(delta.items()):
    don = [d for d in lines if meta[d]['batch'] != meta[l]['batch'] and (d, g) in delta]
    if len(don) < MIN_DONORS: continue
    m = np.array([s != g for s in gset]); dd = {d: delta[(d, g)][m] for d in don}; t = tru[m]
    keep, ident = retain(dd); K = len(keep)
    B = np.mean([dd[d] for d in don], axis=0); M = np.mean([dd[d] for d in keep], axis=0)
    rm = [mse(np.mean([dd[don[i]] for i in rng.choice(len(don), K, replace=False)], axis=0), t) for _ in range(2000)]
    rows.append(dict(line=l, gene=g, n_donors=len(don), K=K, identifiable=int(ident and K < len(don)), mse_M=mse(M, t), mse_B=mse(B, t), mse_Rnd=float(np.mean(rm)),
                     pcc_M=pcc(M, t), pcc_B=pcc(B, t), batch=meta[l]['batch'], lineage=meta[l]['OncotreeLineage']))
with open('/tmp/pdl/units.csv', 'w') as f:
    w = csv.DictWriter(f, rows[0].keys()); w.writeheader(); w.writerows(rows)
def macro(rs, k):
    pl = {}
    for r in rs: pl.setdefault(r['line'], []).append(r[k])
    return float(np.mean([np.mean(v) for v in pl.values()])) if pl else float('nan')
idn = [r for r in rows if r['identifiable']]
mM, mR = macro(idn, 'mse_M'), macro(idn, 'mse_Rnd'); redA = (mR - mM) / mR
bs = []; rg = np.random.default_rng(20261002)
for _ in range(10000):
    gs = rg.choice(genes, len(genes)); wt = {g: (gs == g).sum() for g in genes}
    pm, pr = {}, {}
    for r in idn:
        w = wt[r['gene']]
        if w: pm.setdefault(r['line'], []).extend([r['mse_M']] * w); pr.setdefault(r['line'], []).extend([r['mse_Rnd']] * w)
    a = np.mean([np.mean(v) for v in pm.values()]); b = np.mean([np.mean(v) for v in pr.values()]); bs.append((b - a) / b)
ci = np.quantile(bs, [.025, .975]).tolist()
perline = {}
for l in lines:
    rs = [r for r in rows if r['line'] == l]
    if rs: perline[l] = dict(n=len(rs), mse_M=float(np.mean([r['mse_M'] for r in rs])), mse_B=float(np.mean([r['mse_B'] for r in rs])),
                             worse_than_B=float(np.mean([r['mse_M'] for r in rs])) > float(np.mean([r['mse_B'] for r in rs])))
mMa, mBa = macro(rows, 'mse_M'), macro(rows, 'mse_B'); nw = sum(v['worse_than_B'] for v in perline.values())
v = dict(n_units=len(rows), n_identifiable=len(idn), n_genes_set=len(gset), A=dict(macro_M=mM, macro_Rnd=mR, rel_reduction=redA, ci95=ci, pass_=bool(redA >= .10 and ci[0] > 0)),
         B=dict(macro_M=mMa, macro_B=mBa, lines_worse=nw, lines=len(perline), pass_=bool(mMa <= mBa and nw <= 4)), per_line=perline)
v['overall_win'] = v['A']['pass_'] and v['B']['pass_']
json.dump(v, open('/tmp/pdl/verdict.json', 'w'), indent=1); print(json.dumps({k: v[k] for k in v if k != 'per_line'}, indent=1))
