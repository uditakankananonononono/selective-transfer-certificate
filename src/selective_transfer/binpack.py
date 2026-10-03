"""Bin-packing replication harness (frozen design 2026-10-03)."""
import numpy as np, json, math

def gen(dist, seed):
    r = np.random.default_rng(seed)
    if dist == 'U150': n, cap = 500, 150; x = r.integers(20, 101, n)
    elif dist == 'W5k': n, cap = 5000, 100; x = np.clip(np.rint(45 * r.weibull(3.0, n)), 1, 100).astype(int)
    elif dist == 'U100': n, cap = 1000, 100; x = r.integers(20, 101, n)
    elif dist == 'LN': n, cap = 5000, 100; x = np.clip(np.rint(np.exp(r.normal(3.2, 0.6, n))), 1, 100).astype(int)
    elif dist == 'BM':
        n, cap = 5000, 100; c = r.random(n) < 0.5
        x = np.clip(np.rint(np.where(c, r.normal(25, 5, n), r.normal(70, 8, n))), 1, 100).astype(int)
    else: raise ValueError(dist)
    return dict(capacity=cap, items=[int(v) for v in x])

def l1(inst): return math.ceil(sum(inst['items']) / inst['capacity'])

def pack_notebook(inst, priority):
    """Exact notebook semantics: num_items bins, argmax over feasible, first index wins."""
    items, cap = inst['items'], inst['capacity']; bins = np.array([cap] * len(items))
    for it in items:
        valid = np.nonzero((bins - it) >= 0)[0]
        pr = priority(it, bins[valid]); b = valid[np.argmax(pr)]; bins[b] -= it
    return int((bins != cap).sum())

def pack_fast(inst, vprio):
    """Equivalent to notebook semantics for position-independent priority functions: used bins + one fresh bin."""
    items, cap = inst['items'], inst['capacity']; res = np.full(len(items) + 1, cap); used = 0
    for it in items:
        view = res[:used + 1]; valid = np.nonzero(view >= it)[0]
        pr = vprio(it, view[valid], cap); b = valid[np.argmax(pr)]; res[b] -= it
        if b == used: used += 1
    return used

def v_ff(it, b, cap): return -np.arange(len(b), dtype=float)
def v_bf(it, b, cap): return -(b - it).astype(float)
def v_wf(it, b, cap): return (b - it).astype(float)
def v_ab(kind, a, bb):
    def f(it, b, cap):
        d = (b - it).astype(float)
        low = b <= it + a
        mid = (~low) & ((b < it + bb) if kind != 'WF' else (b <= it + bb))
        if kind == 'FF': base = np.ones(len(b))
        elif kind == 'BF': base = 1.0 / np.maximum(d, 1e-9)
        else: base = np.where(b == cap, -1.0, -1.0 / np.maximum(d, 1e-9))
        return np.where(low, cap - b + 1.0, np.where(mid, -2.0, base))
    return f

def notebook_prio(vp):
    return lambda it, b: vp(it, b, notebook_prio.cap)
GRID = [(a, a + o) for a in (0, 1, 2, 3, 5, 8) for o in (1, 3, 6, 10, 15, 20, 30)]
KINDS = ('FF', 'BF', 'WF')
def excess(nb, inst): lb = l1(inst); return (nb - lb) / lb
