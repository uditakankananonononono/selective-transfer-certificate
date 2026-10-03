"""DepMap Perturb-seq pilot donor-selector study (frozen design + addendum 1)."""
import numpy as np, h5py, scipy.sparse as sp

MIN_KO, MIN_CTRL, MIN_DONORS, COS_T = 20, 100, 4, 0.2
UMI_FRAC, MIN_GUIDE_UMI, MITO_MAX = 0.8, 5, 0.25

def read_guides(path, wanted=None):
    """Guide x cell counts. If wanted (set of barcodes as written in header) is given, keep only those columns."""
    names, rows = [], []
    with open(path) as fh:
        bcs = fh.readline().rstrip('\n').split(',')[1:]
        sel = None if wanted is None else np.array([i for i, b in enumerate(bcs) if b in wanted])
        for l in fh:
            p = l.rstrip('\n').split(','); names.append(p[0]); v = np.array(p[1:], dtype=np.int32)
            rows.append(v if sel is None else v[sel])
    bcs = np.array(bcs)
    return np.array(names), (bcs if sel is None else bcs[sel]), np.vstack(rows)

def assign_guides(counts, names):
    """Return gene label per cell or '' (authors' rule: top guide >=80% of guide UMIs and >=5 UMIs)."""
    tot = counts.sum(0); top = counts.argmax(0); topv = counts[top, np.arange(counts.shape[1])]
    ok = (topv >= MIN_GUIDE_UMI) & (tot > 0) & (topv >= UMI_FRAC * np.maximum(tot, 1))
    genes = np.array([n.split('_')[0] for n in names])
    return np.where(ok, genes[top], '')

def read_ge(path):
    f = h5py.File(path, 'r')['matrix']
    bc = np.array([b.decode().split('-')[0] for b in f['barcodes'][:]])
    nm = np.array([s.decode() for s in f['features/name'][:]])
    shp = f['shape'][:]
    X = sp.csc_matrix((f['data'][:], f['indices'][:], f['indptr'][:]), shape=(shp[0], shp[1]))  # genes x cells
    return bc, nm, X

def collapse_symbols(nm, X):
    u, inv = np.unique(nm, return_inverse=True)
    M = sp.csr_matrix((np.ones(len(nm)), (inv, np.arange(len(nm)))), shape=(len(u), len(nm)))
    return u, (M @ X).tocsc()

def qc_mask(X, symbols):
    tot = np.asarray(X.sum(0)).ravel()
    mt = np.array([s.startswith('MT-') for s in symbols])
    mito = np.asarray(X[mt].sum(0)).ravel() / np.maximum(tot, 1)
    lo, hi = np.quantile(tot, [0.01, 0.99])
    return (mito < MITO_MAX) & (tot >= lo) & (tot <= hi)

def pseudobulk_logcp10k(X, cols):
    """Mean over cells of log1p(count/total*1e4)."""
    S = X[:, cols]; tot = np.asarray(S.sum(0)).ravel()
    S = S.multiply(1e4 / np.maximum(tot, 1)).tocsc(); S.data = np.log1p(S.data)
    return np.asarray(S.mean(1)).ravel()

def cosine(a, b):
    d = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / d) if d > 0 else 0.0

def retain(deltas):
    """deltas: dict donor->delta. Keep donors with cosine to mean of OTHER donors > COS_T. Identity if <3 pass."""
    ks = list(deltas); keep = []
    for k in ks:
        other = np.mean([deltas[j] for j in ks if j != k], axis=0)
        if cosine(deltas[k], other) > COS_T: keep.append(k)
    return (keep, True) if len(keep) >= 3 else (ks, False)

def mse(p, t): return float(np.mean((p - t) ** 2))
def pcc(p, t):
    if np.std(p) == 0 or np.std(t) == 0: return float('nan')
    return float(np.corrcoef(p, t)[0, 1])
