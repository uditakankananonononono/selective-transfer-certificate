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

    if stage == 'eval':
        import time
        tuned = json.load(open(f'{OUT}/tuned.json')); orl = load_or()
        tests = {k: orl[k] for k in orl}
        for d in ('W5k', 'U100', 'LN', 'BM'): tests[d] = [gen(d, s) for s in SEEDS[d][1]]
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
        cap_of = lambda i: i['capacity']
        fast = {'BestFit': v_bf, 'FirstFit': v_ff}
        for d, t in tuned.items(): fast[f'ab[{d}]={t["kind"]}({t["a"]},{t["b"]})'] = v_ab(t['kind'], t['a'], t['b'])
        # validity check
        chk = []
        for cls, insts in tests.items():
            for inst in insts[:3]:
                for name, vp in fast.items():
                    nbk = pack_notebook(inst, lambda it, b, vp=vp, c=inst['capacity']: vp(it, b, c))
                    chk.append(dict(cls=cls, heur=name, fast=pack_fast(inst, vp), notebook=nbk))
        bad = [c for c in chk if c['fast'] != c['notebook']]
        print('equivalence checks', len(chk), 'mismatches', len(bad), flush=True)
        json.dump(dict(checks=chk), open(f'{OUT}/equivalence.json', 'w'))
        if bad: print(bad); sys.exit(1)
        bins = {}
        for cls, insts in tests.items():
            for name, vp in fast.items(): bins[(name, cls)] = [pack_fast(i, vp) for i in insts]
            for name, f in (('FunSearch-OR', fs_or), ('FunSearch-Weibull', fs_w)):
                bins[(name, cls)] = [pack_notebook(i, f) for i in insts]; print(name, cls, 'done', time.strftime('%X'), flush=True)
        rng = np.random.default_rng(20261003); out = {}
        for (name, cls), nb in bins.items():
            ex = np.array([(n - l1(i)) / l1(i) for n, i in zip(nb, tests[cls])])
            bs = rng.choice(ex, (10000, len(ex))).mean(1)
            out[f'{name}|{cls}'] = dict(mean=float(ex.mean()), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), n=len(ex), per_instance_bins=[int(x) for x in nb], per_instance_excess=[float(x) for x in ex])
        json.dump(out, open(f'{OUT}/results.json', 'w'), indent=1); print('saved')
