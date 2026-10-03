"""Sealed h2h replicate scoring (Addendum 2). Run once after both h2h npz exist."""
import sys, json, csv, numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'scripts')
from selective_transfer.depmap_pilot import *
from depmap_h2h_replicate import main_gset, meta, lines
D, idx, gset = main_gset(); rng = np.random.default_rng(20261002); rows = []; skipped = []
for L in ('UMRC3', 'KMRC20'):
    H = np.load(f'/tmp/pdl/h2h_{L}.npz'); hg = list(H['genes']); cnt = json.load(open(f'/tmp/pdl/h2h_{L}.json'))['counts']
    for g in sorted(k for k in H.files if k not in ('genes', '__ctrl__')):
        if g.startswith('Dup_') or g.startswith('d'): continue
        don = [d for d in lines if meta[d]['batch'] != meta[L]['batch'] and g in D[d].files]
        if len(don) < MIN_DONORS: skipped.append((L, g, len(don))); continue
        t = H[g] - H['__ctrl__']; m = np.array([s != g for s in hg])
        dd = {d: (D[d][g][[idx[d][s] for s in hg]] - D[d]['__ctrl__'][[idx[d][s] for s in hg]])[m] for d in don}; t = t[m]
        keep, ident = retain(dd); K = len(keep)
        B = np.mean([dd[d] for d in don], axis=0); M = np.mean([dd[d] for d in keep], axis=0)
        rm = [mse(np.mean([dd[don[i]] for i in rng.choice(len(don), K, replace=False)], axis=0), t) for _ in range(2000)]
        rows.append(dict(line=L, gene=g, n_ko=cnt.get(g), n_donors=len(don), K=K, identifiable=int(ident and K < len(don)), mse_M=mse(M, t), mse_B=mse(B, t), mse_Rnd=float(np.mean(rm)), pcc_M=pcc(M, t), pcc_B=pcc(B, t)))
with open('/tmp/pdl/h2h_units.csv', 'w') as f:
    w = csv.DictWriter(f, rows[0].keys()); w.writeheader(); w.writerows(rows)
def macro(rs, k):
    pl = {}
    for r in rs: pl.setdefault(r['line'], []).append(r[k])
    return float(np.mean([np.mean(v) for v in pl.values()])) if pl else float('nan')
idn = [r for r in rows if r['identifiable']]
mM, mR = macro(idn, 'mse_M'), macro(idn, 'mse_Rnd'); mMa, mBa = macro(rows, 'mse_M'), macro(rows, 'mse_B')
pl = {L: dict(n=len([r for r in rows if r['line'] == L]), mse_M=macro([r for r in rows if r['line'] == L], 'mse_M'), mse_B=macro([r for r in rows if r['line'] == L], 'mse_B')) for L in ('UMRC3', 'KMRC20')}
v = dict(n_units=len(rows), n_identifiable=len(idn), skipped_no_donors=skipped,
         A=dict(macro_M=mM, macro_Rnd=mR, rel_reduction=(mR - mM) / mR if idn else None, passes_10pct=bool(idn and (mR - mM) / mR >= .10)),
         B=dict(macro_M=mMa, macro_B=mBa, M_le_B=bool(mMa <= mBa)), per_line=pl)
v['reading'] = 'contradicts' if (v['A']['passes_10pct'] or v['B']['M_le_B']) else 'confirms'
json.dump(v, open('/tmp/pdl/h2h_verdict.json', 'w'), indent=1); print(json.dumps(v, indent=1))
