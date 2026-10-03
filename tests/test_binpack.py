import numpy as np
from selective_transfer.binpack import *
def test_equiv_small():
    inst = gen('U150', 7); inst['items'] = inst['items'][:120]
    for vp in (v_bf, v_ff, v_wf, v_ab('BF', 2, 10), v_ab('FF', 1, 7), v_ab('WF', 3, 20)):
        notebook_prio.cap = inst['capacity']
        assert pack_notebook(inst, lambda it, b, vp=vp: vp(it, b, inst['capacity'])) == pack_fast(inst, vp)
def test_l1(): assert l1(dict(capacity=10, items=[5, 6])) == 2
def test_gen_det(): assert gen('LN', 1) == gen('LN', 1) and gen('LN', 1) != gen('LN', 2)
