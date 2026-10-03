"""Run the frozen bin-packing study. Run from repo root."""
import sys, json, numpy as np, itertools
sys.path.insert(0, 'src')
from selective_transfer.binpack import *
import urllib.request, re
OUT = '/tmp/pdl/binpack'; import os; os.makedirs(OUT, exist_ok=True)
SEEDS = {'U150': (range(1000, 1005), None), 'W5k': (range(2000, 2005), range(2100, 2105)), 'U100': (range(3000, 3005), range(3100, 3105)),
         'LN': (range(4000, 4005), range(4100, 4105)), 'BM': (range(5000, 5005), range(5100, 5105))}
def load_or():
    out = {}
    for k in (1, 2, 3, 4):
        t = open(f'/tmp/orlib{k}.txt').read().split(); p = 1; P = int(t[0]); insts = []
        for _ in range(P):
            name = t[p]; cap = int(t[p + 1]); n = int(t[p + 2]); p += 4  # name, cap, n, best-known
            insts.append(dict(name=name, capacity=cap, items=[int(v) for v in t[p:p + n]])); p += n
        out[f'OR{k}'] = insts
    return out
def mean_excess(insts, vp):
    return float(np.mean([excess(pack_fast(i, vp), i) for i in insts]))
def tune(dist):
    tr = [gen(dist, s) for s in SEEDS[dist][0]]; best = None
    for kind in KINDS:
        for a, b in GRID:
            e = mean_excess(tr, v_ab(kind, a, b))
            key = (round(e, 12), a, b, KINDS.index(kind))
            if best is None or key < best[0]: best = (key, kind, a, b, e)
    return dict(kind=best[1], a=best[2], b=best[3], train_excess=best[4])
if __name__ == '__main__':
    stage = sys.argv[1]
    if stage == 'tune':
        res = {d: tune(d) for d in SEEDS}; json.dump(res, open(f'{OUT}/tuned.json', 'w'), indent=1); print(json.dumps(res, indent=1))
