"""Outcome-blind fold extraction and content-addressed prediction locks.

Locks bind the exact gene order, evaluation keys, dataset byte hash, source hash,
protocol hash, predictions and certificates. No target-treated matrix is read.
"""
import hashlib
import json
import numpy as np
from scipy import sparse
from .tier1 import predict


def extract_fold(adata, context, chunk_size=1000):
    if not 1 <= chunk_size <= 5000:
        raise ValueError('Invalid chunk size')
    genes = list(map(str, adata.var_names))
    if not genes or len(set(genes)) != len(genes):
        raise ValueError('Empty or duplicate gene identifiers')
    obs = adata.obs
    c = obs.condition1.astype(str).to_numpy()
    p = obs.condition2.astype(str).to_numpy()
    allowed = (c != context) | (p == 'control')
    indices = np.flatnonzero(allowed)
    labels = list(zip(c[indices], p[indices]))
    keys = sorted(set(labels))
    lookup = {k:i for i,k in enumerate(keys)}
    sums = np.zeros((len(keys), adata.n_vars), dtype=np.float64)
    counts = np.zeros(len(keys), dtype=np.int64)
    for start in range(0, len(indices), chunk_size):
        rows = indices[start:start+chunk_size]
        # Selection occurs before reading X, not after loading an outcome chunk.
        x = adata.X[rows, :]
        code = np.array([lookup[(c[i], p[i])] for i in rows])
        for group in np.unique(code):
            local = x[code == group]
            sums[group] += np.asarray(local.sum(axis=0)).reshape(-1)
            counts[group] += len(rows[code == group])
    if any(k[0] == context and k[1] != 'control' for k in keys):
        raise AssertionError('Target-treated outcome entered fold')
    return ({k:sums[i]/counts[i] for i,k in enumerate(keys)},
            {k:int(counts[i]) for i,k in enumerate(keys)}, genes)


def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':'),
                     allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def make_lock(dataset, keys, predictions, genes, dataset_sha256,
              protocol_sha256, source_sha256):
    from .evaluation import CLEAN_DATASETS
    if dataset not in CLEAN_DATASETS:
        raise ValueError('Not a clean dataset')
    if not genes or len(genes) != len(set(genes)):
        raise ValueError('Invalid gene order')
    expected = list(keys[['outSample','perturb']].itertuples(index=False, name=None))
    actual = [(r[0],r[1]) for r in predictions]
    if actual != expected or len(set(actual)) != len(actual):
        raise ValueError('Prediction keys do not match frozen keys')
    for digest in [dataset_sha256, protocol_sha256, source_sha256]:
        if len(digest) != 64 or any(ch not in '0123456789abcdef' for ch in digest):
            raise ValueError('Invalid provenance hash')
    rows = []
    for context, pert, delta, certificate, ntrain in predictions:
        d = np.asarray(delta, dtype=float)
        if d.shape != (len(genes),) or not np.isfinite(d).all():
            raise ValueError('Invalid prediction vector')
        if not np.isfinite(certificate) or ntrain < 1:
            raise ValueError('Invalid certificate or training count')
        rows.append(dict(context=context, perturbation=pert, delta=d.tolist(),
                         certificate=float(certificate), training_contexts=int(ntrain)))
    body = dict(schema=1, dataset=dataset, genes=genes, rows=rows,
                dataset_sha256=dataset_sha256, protocol_sha256=protocol_sha256,
                source_sha256=source_sha256)
    return {'sha256':canonical_hash(body), 'payload':body}


def verify_lock(lock, keys, genes, dataset_sha256, protocol_sha256, source_sha256):
    body = lock['payload']
    if canonical_hash(body) != lock['sha256']:
        raise ValueError('Prediction lock modified')
    if body['genes'] != list(genes):
        raise ValueError('Gene order differs from prediction lock')
    for field, value in [('dataset_sha256',dataset_sha256),
                         ('protocol_sha256',protocol_sha256),('source_sha256',source_sha256)]:
        if body[field] != value:
            raise ValueError('Provenance differs from prediction lock')
    expected = list(keys[['outSample','perturb']].itertuples(index=False,name=None))
    if [(r['context'],r['perturbation']) for r in body['rows']] != expected:
        raise ValueError('Evaluation keys differ from prediction lock')
    return body
