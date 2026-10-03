"""Stage 1 (streaming, low memory): per-line pseudobulks. Run from repo root."""
import sys, json, numpy as np, zipfile, os, csv, h5py, scipy.sparse as sp, shutil
sys.path.insert(0, 'src')
from selective_transfer.depmap_pilot import *
Z = '/tmp/pdl/single_cell_data.zip'; OUT = '/tmp/pdl/pb'; os.makedirs(OUT, exist_ok=True)
man = list(csv.DictReader(zipfile.ZipFile(Z).open('single_cell_data/raw_data_file_manifest.csv').read().decode().splitlines()))
line = sys.argv[1]; row = [r for r in man if r['CellLine'] == line][0]
zf = zipfile.ZipFile(Z); tmp = f'/tmp/pdl/x/{line}'; os.makedirs(tmp, exist_ok=True)
for k in ('GeneExpression', 'CRISPR'): zf.extract('single_cell_data/' + row[k], tmp)
f = h5py.File(f"{tmp}/single_cell_data/{row['GeneExpression']}", 'r')['matrix']
rawbc = [b.decode() for b in f['barcodes'][:]]
hdr = open(f"{tmp}/single_cell_data/{row['CRISPR']}").readline(4000).split(',')[1]
full = '-' in hdr  # suffixed guide headers (KYSE450, UMRC3): match on the full barcode; else strip -1
bc = np.array(rawbc if full else [b.split('-')[0] for b in rawbc]); nm = np.array([s.decode() for s in f['features/name'][:]])
names, gbc, G = read_guides(f"{tmp}/single_cell_data/{row['CRISPR']}", wanted=set(bc))
ng, nc = [int(v) for v in f['shape'][:]]; indptr = f['indptr'][:]
u, inv = np.unique(nm, return_inverse=True)
Mcol = sp.csr_matrix((np.ones(len(nm)), (inv, np.arange(len(nm)))), shape=(len(u), ng)); mt = np.array([s.startswith('MT-') for s in u])
CH = 3000
def chunks():
    for a in range(0, nc, CH):
        b = min(a + CH, nc); s0, s1 = indptr[a], indptr[b]
        X = sp.csc_matrix((f['data'][s0:s1], f['indices'][s0:s1], indptr[a:b + 1] - s0), shape=(ng, b - a))
        yield a, b, (Mcol @ X).tocsc()
tot = np.zeros(nc); mito = np.zeros(nc)
for a, b, X in chunks():
    tot[a:b] = np.asarray(X.sum(0)).ravel(); mito[a:b] = np.asarray(X[mt].sum(0)).ravel() / np.maximum(tot[a:b], 1)
lo, hi = np.quantile(tot, [0.01, 0.99]); qc = (mito < MITO_MAX) & (tot >= lo) & (tot <= hi)
gi = {b: i for i, b in enumerate(gbc)}; has = np.array([b in gi for b in bc])
lab = np.full(nc, '', dtype=object); w = np.where(has)[0]
lab[w] = assign_guides(G[:, [gi[bc[i]] for i in w]], names); lab[~qc] = ''
lab = np.array([('__ctrl__' if l.startswith('OR') else l) for l in lab], dtype=object)
cnt = {g: int((lab == g).sum()) for g in set(lab) if g}
keepg = [g for g, c in cnt.items() if c >= MIN_KO or g == '__ctrl__']
acc = {g: np.zeros(len(u)) for g in keepg}
for a, b, X in chunks():
    L = lab[a:b]
    for g in keepg:
        c = np.where(L == g)[0]
        if len(c): acc[g] += pseudobulk_logcp10k(X, c) * len(c)
res = {g: acc[g] / cnt[g] for g in keepg}
np.savez(f'{OUT}/{line}.npz', symbols=u, **res)
json.dump({'cells_total': int(nc), 'with_guide_matrix': int(has.sum()), 'qc_pass': int(qc.sum()), 'assigned': int((lab != '').sum()), 'counts': cnt}, open(f'{OUT}/{line}.json', 'w'))
shutil.rmtree(tmp); print(line, nc, int(has.sum()), int(qc.sum()), cnt.get('__ctrl__'), len(res) - 1, flush=True)
