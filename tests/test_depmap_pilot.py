import numpy as np, scipy.sparse as sp
from selective_transfer.depmap_pilot import *
def test_assign():
    c = np.array([[10, 3, 0], [0, 3, 0], [0, 0, 9]]); n = np.array(['A_v1_g1', 'B_v1_g1', 'C_v1_g1'])
    assert list(assign_guides(c, n)) == ['A', '', 'C']
def test_pb():
    X = sp.csc_matrix(np.array([[1, 3], [1, 1]])); v = pseudobulk_logcp10k(X, [0, 1])
    assert np.allclose(v, [(np.log1p(5000) + np.log1p(7500)) / 2, (np.log1p(5000) + np.log1p(2500)) / 2])
def test_retain():
    r = np.random.default_rng(0); b = r.normal(size=50)
    d = {i: b + .1 * r.normal(size=50) for i in range(4)}; d['x'] = -b
    k, ident = retain(d); assert ident and 'x' not in k
    k2, ident2 = retain({0: b, 1: -b, 2: r.normal(size=50)}); assert not ident2
def test_collapse():
    u, X = collapse_symbols(np.array(['a', 'b', 'a']), sp.csc_matrix(np.array([[1], [2], [3]])))
    assert list(u) == ['a', 'b'] and X.toarray().ravel().tolist() == [4, 2]
