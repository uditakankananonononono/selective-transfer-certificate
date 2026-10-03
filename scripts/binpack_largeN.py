"""Larger-N follow-up per studies/binpacking-largeN-2026-10-03/FROZEN_DESIGN.md. Run from repo root."""
import sys, json, os, time, numpy as np
sys.path.insert(0, 'src')
from selective_transfer.binpack import *
OUT = '/tmp/pdl/binpack_largeN'; os.makedirs(OUT, exist_ok=True)
SD = {'W5k': 6100, 'U100': 7100, 'LN': 8100, 'BM': 9100, 'U150': 6500}
tuned = json.load(open('studies/binpacking-replication-2026-10-03/tuned.json'))
tests = {c: [gen(c, s0 + i) for i in range(30)] for c, s0 in SD.items()}
def fs_or(item, bins):
    def s(bin, item):
        d = bin - item
        for th, v in ((2, 4), (3, 3), (5, 2), (7, 1), (9, .9), (12, .95), (15, .97), (18, .98), (20, .98), (21, .98)):
            if d <= th: return v
        return .99
    return np.array([s(b, item) for b in bins])
def fs_w(item, bins):
    m = max(bins); score = (bins - m) ** 2 / item + bins ** 2 / (item ** 2); score += bins ** 2 / item ** 3
    score[bins > item] = -score[bins > item]; score[1:] -= score[:-1]; return score
fast = {'BestFit': v_bf, 'FirstFit': v_ff}
for d, t in tuned.items(): fast[f'ab[{d}]'] = v_ab(t['kind'], t['a'], t['b'])
bad = 0
for cls, insts in tests.items():
    for inst in insts[:3]:
        for name, vp in fast.items():
            nb = pack_notebook(inst, lambda it, b, vp=vp, c=inst['capacity']: vp(it, b, c))
            if nb != pack_fast(inst, vp): bad += 1
print('equivalence mismatches', bad, flush=True)
if bad: sys.exit(1)
ex = {}
for cls, insts in tests.items():
    lb = np.array([l1(i) for i in insts])
    for name, vp in fast.items(): ex[(name, cls)] = (np.array([pack_fast(i, vp) for i in insts]) - lb) / lb
    for name, f in (('FunSearch-OR', fs_or), ('FunSearch-Weibull', fs_w)):
        ex[(name, cls)] = (np.array([pack_notebook(i, f) for i in insts]) - lb) / lb; print(name, cls, time.strftime('%X'), flush=True)
rng = np.random.default_rng(20261003)
def boot(x):
    idx = rng.integers(0, len(x), (10000, len(x))); b = x[idx].mean(1); return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
res = {'matrix': {f'{h}|{c}': dict(zip(('mean', 'lo', 'hi'), boot(v)), per_instance_excess=v.tolist()) for (h, c), v in ex.items()}}
def pair(a, ca, b, cb): return dict(zip(('mean_diff', 'lo', 'hi'), boot(ex[(a, ca)] - ex[(b, cb)])))
P = {}
for c in ('U100', 'LN', 'BM', 'U150'): P[f'1 FS-Weibull - BestFit | {c}'] = pair('FunSearch-Weibull', c, 'BestFit', c)
for c in ('W5k', 'U100', 'LN', 'BM'): P[f'2 FS-OR - BestFit | {c}'] = pair('FunSearch-OR', c, 'BestFit', c)
P['3 ab[W5k] - FS-Weibull | W5k'] = pair('ab[W5k]', 'W5k', 'FunSearch-Weibull', 'W5k')
P['3 ab[U150] - FS-OR | U150'] = pair('ab[U150]', 'U150', 'FunSearch-OR', 'U150')
for c in SD: P[f'4 ab[{c}] - BestFit | {c}'] = pair(f'ab[{c}]', c, 'BestFit', c)
for d in SD:
    for c in SD:
        if c != d: P[f'5 transfer ab[{d}] on {c} - ab[{c}] on {c}'] = pair(f'ab[{d}]', c, f'ab[{c}]', c)
res['paired'] = P; json.dump(res, open(f'{OUT}/results.json', 'w'), indent=1); print('saved')
